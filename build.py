import subprocess
import sys
import re
import os
import time

coarserange = 0.5
finerange = 0.2

def run(command):
    print(" ".join(command))
    subprocess.run(command, check=True)

def wait_for_stable_file(filepath, poll_interval=1):
    """
    Blocks until the specified file exists and its size hasn't changed for 1 second.

    Parameters:
        filepath (str): Path to the file to monitor.
        poll_interval (int): Interval in seconds to poll the file size. Default is 1 second.
    """
    
    # Wait until the file exists
    while not os.path.exists(filepath):
        time.sleep(poll_interval)
    
    last_size = os.path.getsize(filepath)
    size_changed = True
    
    while size_changed:
        time.sleep(poll_interval)
        current_size = os.path.getsize(filepath)
        
        if current_size == last_size:
            size_changed = False
        else:
            last_size = current_size

def generate_gcode(input_prefix, config_file, parameters=""):
    original_scad = f"{input_prefix}.scad"
    stl = f"{input_prefix}.stl"
    gcode = f"{input_prefix}_original.gcode"

    target_scad = f"intermediate.scad"

    # Prepend parameters to original_scad
    with open(original_scad, "r") as f:
        original_content = parameters + f.read()
    with open(target_scad, "w") as f:
        f.write(original_content)
    
    # Convert OpenSCAD to STL
    try:
        run(["openscad", "-o", stl, target_scad, "-p", "parameters.scad"])
    except subprocess.CalledProcessError:
        print(f"Error converting {original_scad} to STL.")
        sys.exit(1)

    # Slice STL to GCODE using PrusaSlicer
    # PrusaSlicer, annoyingly, does not block, so we do a dance to ensure the file has been written fully
    if os.path.exists(gcode):
        os.remove(gcode)

    try:
        run(["flatpak", "run", "com.prusa3d.PrusaSlicer", "--load", config_file, "-g", "-o", gcode, stl])
        wait_for_stable_file(gcode)
    except subprocess.CalledProcessError:
        print(f"Error slicing {stl} to gcode.")
        sys.exit(1)
    
def mirror_y(input_file, output_file):
    with open(input_file, 'r') as infile:
        content = infile.read()

    # Split content based on ;LAYER_CHANGE
    parts = content.split(';LAYER_CHANGE', 1)
    prefix = parts[0] + ';LAYER_CHANGE' if len(parts) > 1 else parts[0]
    main_content = parts[1] if len(parts) > 1 else ''

    # Find all words that match the pattern Y<number>
    matches = re.findall(r'Y(-?\d+\.\d+)', main_content)
    numbers = [float(match) for match in matches]

    # Calculate the midpoint
    midpoint = (min(numbers) + max(numbers)) / 2

    # Replace each matched word with its mirrored value around the midpoint
    def replace_func(match):
        value = float(match.group(1))
        mirrored_value = midpoint + (midpoint - value)
        return 'Y{:.3f}'.format(mirrored_value)

    modified_content = re.sub(r'Y(-?\d+\.\d+)', replace_func, main_content)

    # Write to the output file
    with open(output_file, 'w') as outfile:
        outfile.write(prefix + modified_content)

class UnionFind:
    def __init__(self):
        self.parent = {}
        self.rank = {}

    def make_set(self, x):
        self.parent[x] = x
        self.rank[x] = 0

    def find(self, x):
        if x != self.parent[x]:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return

        if self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_x] = root_y
            if self.rank[root_x] == self.rank[root_y]:
                self.rank[root_y] += 1

def offset(input_file, output_file, offset_array):
    OFFSET = 7

    with open(input_file, 'r') as infile:
        content = infile.read()

    matches = re.findall(r'Y(-?\d+\.\d+)', content)
    numbers = [float(match) for match in matches if float(match) >= 10]

    if not numbers:
        return

    clusters = []
    cluster = [numbers[0]]
    lowest_seen_y = numbers[0] - OFFSET

    for num in numbers[1:]:
        if num >= lowest_seen_y - 1:
            cluster.append(num)
            lowest_seen_y = min(lowest_seen_y, num)
        else:
            clusters.append(cluster)
            cluster = [num]
            lowest_seen_y = num - OFFSET

    if cluster:
        clusters.append(cluster)

    current_cluster_index = -1
    encountered_Y = False
    last_z = 0

    with open(output_file, 'w') as outfile:
        for line in content.splitlines():
            if "Y" in line and not encountered_Y:
                y_value = re.search(r'Y(-?\d+\.\d+)', line)
                if y_value and float(y_value.group(1)) >= 10:
                    encountered_Y = True
                    current_cluster_index = 0

            if encountered_Y and current_cluster_index < len(clusters) and "Z" in line:
                z_value = re.search(r'Z(-?\d*\.\d+)', line)
                if z_value:
                    original_z = float(z_value.group(1))
                    last_z = original_z
                    modified_z = original_z + offset_array[current_cluster_index]
                    line = line.replace(f"Z{z_value.group(1)}", f"Z{modified_z:.3f}")

            outfile.write(line + "\n")

            if encountered_Y and "Y" in line:
                y_value = re.search(r'Y(-?\d+\.\d+)', line)
                if y_value and float(y_value.group(1)) not in clusters[current_cluster_index]:
                    outfile.write("; CLUSTER SHIFT\n")
                    current_cluster_index += 1
                    outfile.write(f"G1 Z{last_z + offset_array[current_cluster_index]}\n")

def deskirt(input_file, output_file):
    with open(input_file, 'r') as infile:
        content = infile.read()

    # Replace 'skirts = 1' with 'skirts = 0'
    modified_content = content.replace('skirts = 1', 'skirts = 0')

    # Write the modified content to the output file
    with open(output_file, 'w') as outfile:
        outfile.write(modified_content)

def generate_adjustment(output_file, config_munged, offset_array, adjust = 0):
    visarray = []
    for num in offset_array:
        show = num + adjust
        if show < 0:
            visarray += ["ERROR"]
        else:
            visarray += ["{:+.3f}".format(show)]

    generate_gcode("23_general_adjust", config_munged, parameters="tags = [\n" + ",\n".join([f'"{item}"' for item in visarray]) + "\n];")
    offset("23_general_adjust_original.gcode", output_file, offset_array)

if __name__ == "__main__":
    config = "config.petg.0.4mm.0.2mm.ini"
    config_munged = "config.ini"

    deskirt(config, config_munged)

    generate_gcode("1_initial_adjust", config_munged)

    # prusaslicer outputs from far-away to near, which makes it hard to see what's going on, so we flip it around
    mirror_y("1_initial_adjust_original.gcode", "1_initial_adjust.gcode")

    generate_adjustment("2_coarse_adjust.gcode", config_munged, [i * coarserange / 10 + finerange / 2 for i in range(0, 11, 1)], -finerange / 2)
    generate_adjustment("3_fine_adjust.gcode", config_munged, [i * finerange / 10 for i in range(0, 11, 1)])


