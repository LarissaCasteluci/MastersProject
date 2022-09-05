import sys
import os
import itertools
import subprocess
import time

file = "~/MastersProject/1DatasetGeneration/assets/grasp_objects/A0_visual.obj"

#-h <n>                  : Maximum number of output convex hulls. Default is 32
#-r <voxelresolution>    : Total number of voxels to use. Default is 100,000
#-e <volumeErrorPercent> : Volume error allowed as a percentage. Default is 1%
#-d <maxRecursionDepth>  : Maximum recursion depth. Default value is 10.
#-s <true/false>         : Whether or not to shrinkwrap output to source mesh. Default is true.
#-f <fillMode>           : Fill mode. Default is 'flood', also 'surface' and 'raycast' are valid.
#-v <maxHullVertCount>   : Maximum number of vertices in the output convex hull. Default value is 64
#-a <true/false>         : Whether or not to run asynchronously. Default is 'true'
#-l <minEdgeLength>      : Minimum size of a voxel edge. Default value is 2 voxels.
#-p <true/false>         : If false, splits hulls in the middle. If true, tries to find optimal split plane location. False by default.
#-o <obj/stl>            : Export the convex hulls as a series of wavefront OBJ files or STL files.
#-l <true/false>         : If set to false, no logging will be displayed.

# Parameters
lh = [ 10, 15, 20, 25, 30, 32, 35, 40]
lr = [10000, 50000, 80000, 100000, 120000]
ls = ["true", "false"]
lf = ["flood", "surface", "raycast"]
lv = [32, 48, 64, 80]
lp = ["true", "false"]
l = "false"

params = [lh, lr, ls, lf, lv, lp]

permutations = list(itertools.product(*params))

for i in permutations:
    h, r, s, f, v, p = i

    process = subprocess.Popen(f"/home/larissa/Git/v-hacd/app/TestVHACD {file} -h {h} -r {r} -s {s} -f {f} -v {v} -p {p} -l {l}",
                               shell=True, stdout=subprocess.PIPE)

    process.wait()
    print(process.communicate())
    print(process.returncode)

    process2 = subprocess.Popen(f"mv /home/larissa/MastersProject/1DatasetGeneration/assets/decomp.obj /home/larissa/MastersProject/1DatasetGeneration/assets/convex_hull_tests/A0_{h}_{r}_{s}_{f}_{v}_{p}.obj",
                               shell=True, stdout=subprocess.PIPE)
    process2.wait()
