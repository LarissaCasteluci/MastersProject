"""
#   https://towardsdatascience.com/how-to-voxelize-meshes-and-point-clouds-in-python-ca94d403f81d
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
import pdb

#path = Path("/home/larissa/MastersProject/original_repos/egadevalset/egad_eval_set")
#file = "A1.obj"

path = Path("/workspaces/MastersProject/1DatasetGeneration/assets/grasp_objects")
obj_name = 'A0'
file = f"{obj_name}_visual.obj"
file_tmp_1 = f"{obj_name}_tmp1.obj"

coords = []

# Load file
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

# Save normalized file
with open(str(path.parent / 'correct_objects_coordinates_for_simulation'/ 'tmp'/ file_tmp_1), 'w') as f:
    for xyz in coords:
        f.write(f"v {xyz[0]} {xyz[1]} {xyz[2]}\n")
    
    for line in obj:
        r = re.search(r"(?:f)(.+)", line)
        if r:
            f.write(line)

# Voxelize
mesh = trimesh.load(str(path.parent / 'correct_objects_coordinates_for_simulation'/ 'tmp'/ file_tmp_1))
angel_voxel = mesh.voxelized(0.01)

pdb.set_trace()

print(angel_voxel.points) # Verify if it is ok



