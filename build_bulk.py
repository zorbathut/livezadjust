
import os
import pprint
import subprocess

items = [
    ("config.petg.0.25mm.0.1mm.ini", "0.25mm/petg"),
    ("config.petg.0.40mm.0.2mm.ini", "0.40mm/petg"),
    ("config.petg.0.60mm.0.3mm.ini", "0.60mm/petg"),

    ("config.pla.0.25mm.0.1mm.ini", "0.25mm/pla"),
    ("config.pla.0.40mm.0.2mm.ini", "0.40mm/pla"),
    ("config.pla.0.60mm.0.3mm.ini", "0.60mm/pla"),
]

# List to hold the subprocesses
processes = []

# Start each program in parallel
for item in items:
    os.makedirs(f"output/{item[1]}", exist_ok=True)
    cli = ["python3", "build.py", f"{item[0]}", f"output/{item[1]}"]
    pprint.pprint(cli)
    process = subprocess.Popen(cli)
    processes.append(process)

# Wait for all processes to complete
for process in processes:
    process.wait()
