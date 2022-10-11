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
import os
import subprocess
from pathlib import Path
import re
import trimesh
import numpy as np
import xml.etree.ElementTree as ET


path = Path("/home/larissa/MastersProject/original_repos/egadevalset/egad_eval_set")
save_path = Path("/home/larissa/MastersProject/1DatasetGeneration/assets/grasp_objects")
o = "A7"
file = f"{o}.obj"
file_tmp_1 = f"{o}_tmp1.obj"
file_visual = f"{o}_visual.obj"
hh, rr, ss, ff, vv, pp, ll = 150, 100000, "true", "flood", 64, "true", "false"

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

x = coords[:, 0]
y = coords[:, 1]
z = coords[:, 2]

norm = max([(np.max(x) - np.min(x)), (np.max(y) - np.min(y)), (np.max(z) - np.min(z))])
print(norm)
coords = coords / norm

# Save normalized file
with open(str(save_path / file_tmp_1), 'w') as f:
    for xyz in coords:
        f.write(f"v {xyz[0]} {xyz[1]} {xyz[2]}\n")

    for line in obj:
        r = re.search(r"(?:f)(.+)", line)
        if r:
            f.write(line)

# Voxelize
mesh = trimesh.load(str(save_path / file_tmp_1))
angel_voxel = mesh.voxelized(0.01)

# Calculate Center of Mass
n_points = len(angel_voxel.points)
m = 1 / n_points
cm = [0, 0, 0]

for n in angel_voxel.points:
    cm[0] += m*n[0]
    cm[1] += m*n[1]
    cm[2] += m*n[2]

print(cm)

x = angel_voxel.points[:,0]
y = angel_voxel.points[:,1]
z = angel_voxel.points[:,2]

xn = coords[:, 0] - cm[0]
yn = coords[:, 1] - cm[1]
zn = coords[:, 2] - cm[2]

print("xn:", max(xn) - min(xn))
print("yn:", max(yn) - min(yn))
print("zn:", max(zn) - min(zn))

print("max xn:", max(xn))
print("max yn:", max(yn))
print("max zn:", max(zn))

print("min xn:", min(xn))
print("min yn:", min(yn))
print("min zn:", min(zn))

norm_coords = np.asarray([xn, yn, zn])
coords = np.transpose(norm_coords)
x = coords[:, 0]
y = coords[:, 1]
z = -coords[:, 2]
Ix = m*(np.dot(y.transpose(), y) + np.dot(z.transpose(), z))
Iy = m*(np.dot(x.transpose(), x) + np.dot(z.transpose(), z))
Iz = m*(np.dot(x.transpose(), x) + np.dot(y.transpose(), y))
Ixy = m*(np.dot(x.transpose(), y))
Iyz = m*(np.dot(y.transpose(), z))
Ixz = m*(np.dot(x.transpose(), z))

I = np.array([[Ix, -Ixy, -Ixz], [-Ixy, Iy, -Iyz], [-Ixz, -Iyz, Iz]])
print(I)

#Make sure we remove tmp file
os.remove(str(save_path / file_tmp_1))

# Save obj
with open(str(save_path / file_visual), 'w') as f:
    f.write("mtllib shinyred.mtl\n\n")
    for n in range(len(xn)):
        f.write(f"v {xn[n]} {yn[n]} {zn[n]}\n")

    f.write("\nusemtl shinyred\n\n")
    for line in obj:
        r = re.search(r"(?:f)(.+)", line)
        if r:
            f.write(line)

# VDHC
original_file = str(save_path / file_visual)

process = subprocess.Popen(
    f"/home/larissa/Git/v-hacd/app/TestVHACD {original_file} -h {hh} -r {rr} -s {ss} -f {ff} -v {vv} -p {pp} -l {ll}",
    shell=True, stdout=subprocess.PIPE)

process.wait()
print(process.communicate())
print(process.returncode)

process2 = subprocess.Popen(
    f"mv /home/larissa/MastersProject/1DatasetGeneration/assets/grasp_objects/decomp.obj " +
    f"/home/larissa/MastersProject/1DatasetGeneration/assets/grasp_objects/{o}_{hh}_{rr}_{ss}_{ff}_{vv}_{pp}.obj",
    shell=True, stdout=subprocess.PIPE)
process2.wait()

process3 = subprocess.Popen(
    f"rm /home/larissa/MastersProject/1DatasetGeneration/assets/grasp_objects/decomp.stl ",shell=True, stdout=subprocess.PIPE)
process3.wait()


file_to_create = str(save_path /(o + ".urdf"))


inertial = ET.SubElement(link, "inertial")
origin = ET.SubElement(inertial, "origin", xyz="-0.0 -0.0 -0.0")
mass = ET.SubElement(inertial, "mass", value="1")
inertia = ET.SubElement(inertial, "inertia",
                        ixx=str(Ix), ixy=str(-Ixy), ixz=str(-Ixz), iyy=str(Iy),
                        iyz=str(-Iyz), izz=str(Iz))

visual = ET.SubElement(link, "visual")
origin = ET.SubElement(visual, "origin", xyz="-0.0 -0.0 -0.0")
geometry = ET.SubElement(visual, "geometry")
mesh = ET.SubElement(geometry, "mesh", filename=str(save_path / file_visual))
collision = ET.SubElement(link, "collision")
origin = ET.SubElement(collision, "origin", xyz="0.0 0.0 0.0")
geometry = ET.SubElement(collision, "geometry")
mesh = ET.SubElement(geometry, "mesh", filename=str(save_path) + f"/{o}_{hh}_{rr}_{ss}_{ff}_{vv}_{pp}.obj")

tree = ET.ElementTree(root)
ET.indent(tree, '  ')
tree.write(file_to_create)
print("saved ", file_to_create)
