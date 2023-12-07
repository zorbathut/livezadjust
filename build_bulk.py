
import os
import pprint
import subprocess

items = [
    ("config.petg.0.2mm.0.04mm.ini", "0.2mm/petg"),
    ("config.petg.0.4mm.0.2mm.ini", "0.4mm/petg"),
    ("config.petg.0.6mm.0.3mm.ini", "0.6mm/petg"),

    ("config.pla.0.4mm.0.2mm.ini", "0.4mm/pla"),
    ("config.pla.0.6mm.0.3mm.ini", "0.6mm/pla"),
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
