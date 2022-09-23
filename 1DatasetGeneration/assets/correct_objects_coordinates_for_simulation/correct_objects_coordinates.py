"""
    Correct Wavefront object format ( .obj ) for simulation
    1. Decrease size ( Make biggest size == 1 )
    2. Voxelize
    3. Calculate center of mass
    4. Centralize data around CM
    5. Calculate Moment of Inertia
    6. V_HACD
    7. Generate URDF File
    8. Run Simulation and test!
"""

from pathlib import Path
import re
import numpy as np
import trimesh

path = Path("/home/larissa/MastersProject/original_repos/egadevalset/egad_eval_set")
file = "A1.obj"

coords = []

with open(str(path / file), 'r') as f:
    obj = f.readlines()

for line in obj:
    r = re.search(r"(?:v)(.+)", line)
    if r:
        line = line[2:]
        coords_in_str = line.split(" ")
        coords.append([float(coords_in_str[0]), float(coords_in_str[1]), float(coords_in_str[2])])

coords = np.asarray(coords)

x, y, z = coords[0:3]
norm = max([(np.max(x) - np.min(x)), (np.max(y) - np.min(y)), (np.max(z) - np.min(z))])
coords = coords / norm
print(coords)

mesh = trimesh.l