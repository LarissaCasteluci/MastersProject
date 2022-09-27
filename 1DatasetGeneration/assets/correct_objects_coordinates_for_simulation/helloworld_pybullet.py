import pybullet as p
import time
import pybullet_data

pybullet_data_path = "/home/larissa/Git/bullet3/data/"
obj_path = "/home/larissa/MastersProject/1DatasetGeneration/assets/correct_objects_coordinates_for_simulation/tmp/"
physicsClient = p.connect(p.GUI)# p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
p.setGravity(0,0,-10)
planeId = p.loadURDF(pybullet_data_path + "plane.urdf")
cubeStartPos = [0,0,1]
cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])
boxId = p.loadURDF(obj_path + "A0.urdf", cubeStartPos, cubeStartOrientation)

for i in range(100000):
   p.stepSimulation()
   time.sleep(1./240.)
   cubePos, cubeOrn = p.getBasePositionAndOrientation(boxId)

print(cubePos,cubeOrn)

p.disconnect()
