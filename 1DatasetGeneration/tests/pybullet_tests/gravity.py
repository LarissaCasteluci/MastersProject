import pybullet as p
import time
import pybullet_data

physicsClient = p.connect(p.GUI)# p.DIRECT for non-graphical version

p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
p.setGravity(0,0,-9.81)

planeId = p.loadURDF('/home/larissa/Git/bullet3/data/plane.urdf')

cubeStartPos = [0,0,1]
cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])
#boxId = p.loadURDF('/home/larissa/Git/bullet3/data/r2d2.urdf', cubeStartPos, cubeStartOrientation)
#boxId = p.loadURDF('/home/larissa/MastersProject/1DatasetGeneration/assets/convex_hull_tests/C0_1_10000_true_flood_20_true.urdf', cubeStartPos, cubeStartOrientation)
boxId = p.loadURDF('/home/larissa/MastersProject/1DatasetGeneration/tests/pybullet_tests/cube.urdf', cubeStartPos, cubeStartOrientation)

for i in range(100000):
   p.stepSimulation()
   time.sleep(1./240.)
   cubePos, cubeOrn = p.getBasePositionAndOrientation(boxId)

print(cubePos, cubeOrn)

p.disconnect()