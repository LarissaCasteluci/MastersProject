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
import subprocess
from pathlib import Path
import re
import numpy as np
import trimesh
import numpy as np
import pdb
import matplotlib.pyplot as plt

path = Path("/home/larissa/MastersProject/original_repos/egadevalset/egad_eval_set")
file = "A1.obj"
file_tmp_1 = f"A1_tmp1.obj"

#path = Path("/workspaces/MastersProject/1DatasetGeneration/assets/grasp_objects")
#obj_name = 'A1'
#file = f"{obj_name}_visual.obj"
#file_tmp_1 = f"{obj_name}_tmp1.obj"

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


path = Path("/home/larissa/MastersProject/1DatasetGeneration/assets/grasp_objects")
# Save normalized file
with open(str(path.parent / 'correct_objects_coordinates_for_simulation'/ 'tmp'/ file_tmp_1), 'w') as f:
    for xyz in coords:
        f.write(f"v {xyz[0]} {xyz[1]} {xyz[2]}\n")
    
    for line in obj:
        r = re.search(r"(?:f)(.+)", line)
        if r:
            f.write(line)

# Voxelize
mesh = trimesh.load(str(path.parent / 'correct_objects_coordinates_for_simulation'/'tmp'/ file_tmp_1))
angel_voxel = mesh.voxelized(0.01)
#print(angel_voxel.points) # Verify if it is ok

# Calculate Center of Mass
n_points = len(angel_voxel.points)
m = 1 / n_points
cm = [0, 0, 0]

for n in angel_voxel.points:
    cm[0] += m*n[0]
    cm[1] += m*n[1]
    cm[2] += m*n[2]

print(cm)

x, y, z = [], [], []
for n in angel_voxel.points:
    x.append(n[0])
    y.append(n[1])
    z.append(n[2])

xn, yn, zn = [], [], []
for n in range(len(x)):
    xn.append(x[n] - cm[0])
    yn.append(y[n] - cm[1])
    zn.append(z[n] - cm[2])

print("xn:", max(xn) - min(xn))
print("yn:", max(yn) - min(yn))
print("zn:", max(zn) - min(zn))

norm_coords = np.asarray([xn, yn, zn])
coords = np.transpose(norm_coords)
Ix = sum(m*(coords[1]**2 + coords[2]**2))
Iy = sum(m*(coords[0]**2 + coords[2]**2))
Iz = sum(m*(coords[0]**2 + coords[1]**2))
Ixy = sum(m*coords[0]*coords[1])
Iyz = sum(m*coords[1]*coords[2])
Ixz = sum(m*coords[0]*coords[2])

I = np.array([[Ix, Ixy, Ixz],[Ixy, Iy, Iyz],[Ixz, Iyz, Iz]])
print(I)

# VDHC
h, r, s, f, v, p, l = 1, 10000, "true", "flood", 128, "true", "false"
original_file = "/home/larissa/MastersProject/1DatasetGeneration/assets/correct_objects_coordinates_for_simulation/tmp/A0_tmp1.obj"
obj = "A0_collision.obj"

process = subprocess.Popen(
    f"/home/larissa/Git/v-hacd/app/TestVHACD {original_file} -h {h} -r {r} -s {s} -f {f} -v {v} -p {p} -l {l}",
    shell=True, stdout=subprocess.PIPE)

process.wait()
print(process.communicate())
print(process.returncode)

process2 = subprocess.Popen(
    f"mv /home/larissa/MastersProject/1DatasetGeneration/assets/correct_objects_coordinates_for_simulation/decomp.obj " +
    f"/home/larissa/MastersProject/1DatasetGeneration/assets/correct_objects_coordinates_for_simulation/tmp/{obj}_{h}_{r}_{s}_{f}_{v}_{p}.obj",
    shell=True, stdout=subprocess.PIPE)
process2.wait()