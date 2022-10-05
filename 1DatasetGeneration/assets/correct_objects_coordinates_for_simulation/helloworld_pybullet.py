import pybullet as p
import time
import pybullet_data

pybullet_data_path = "/home/larissa/Git/bullet3/data/"
obj_path = "/home/larissa/MastersProject/1DatasetGeneration/assets/grasp_objects/"
gripper_path = "/home/larissa/MastersProject/1DatasetGeneration/assets/grippers_models/"
physicsClient = p.connect(p.GUI)# p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
p.setGravity(0,0,-10)
planeId = p.loadURDF(pybullet_data_path + "plane.urdf")
cubeStartPos = [0,0,1]
cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])
cartesian = p.loadURDF(gripper_path + "cartesian.urdf", cubeStartPos, cubeStartOrientation)
boxId2 = p.loadURDF(obj_path + "A6.urdf", [2, 2, 1], cubeStartOrientation)

for n in range(p.getNumJoints(cartesian)):
   print(f"Information Joint {n}", p.getJointInfo(cartesian, n))

p.setJointMotorControl2(bodyUniqueId=cartesian,
                           jointIndex=2,
                           controlMode=p.POSITION_CONTROL,
                           targetPosition=3.5,
                           targetVelocity=0.1,
                           force=100)

p.setJointMotorControl2(bodyUniqueId=cartesian,
                           jointIndex=3,
                           controlMode=p.POSITION_CONTROL,
                           targetPosition=2,
                           targetVelocity=0.05,
                           force=1)

for i in range(100000):
   p.stepSimulation()
   time.sleep(1./240.)
   cubePos, cubeOrn = p.getBasePositionAndOrientation(cartesian)



print(cubePos,cubeOrn)

p.disconnect()
