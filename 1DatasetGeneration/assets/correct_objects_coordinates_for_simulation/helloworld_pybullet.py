import pybullet as p
import time
import pybullet_data

pybullet_data_path = "/home/larissa/Git/bullet3/data/"
obj_path = "/home/larissa/MastersProject/1DatasetGeneration/assets/grasp_objects/"
gripper_path = "/home/larissa/MastersProject/1DatasetGeneration/assets/grippers_models/"

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
p.setGravity(0,0,-10)
simulation_time = 60


planeId = p.loadURDF(pybullet_data_path + "plane.urdf")

cubeStartPos = [0, 0, 1]
cubeStartOrientation = p.getQuaternionFromEuler([0, 0, 0])
cartesian = p.loadURDF(gripper_path + "cartesian.urdf", cubeStartPos, cubeStartOrientation)
boxId2 = p.loadURDF(obj_path + "A6.urdf", [2, 2, 1], cubeStartOrientation)

for n in range(p.getNumJoints(cartesian)):
   print(f"Information Joint {n}", p.getJointInfo(cartesian, n))

p.setJointMotorControl2(bodyUniqueId=cartesian,
                           jointIndex=2,
                           controlMode=p.VELOCITY_CONTROL,
                           targetVelocity=1,
                           force=100)

p.setJointMotorControl2(bodyUniqueId=cartesian,
                           jointIndex=3,
                           controlMode=p.VELOCITY_CONTROL,
                           targetVelocity=0.5,
                           force=10)

jointPosition=0
for i in range(simulation_time*240):
    p.stepSimulation()
    time.sleep(1./240.)
    cubePos, cubeOrn = p.getBasePositionAndOrientation(cartesian)

    if p.getJointState(bodyUniqueId=cartesian, jointIndex=3)[0] > 2:

        p.setJointMotorControl2(bodyUniqueId=cartesian,
                                jointIndex=3,
                                controlMode=p.VELOCITY_CONTROL,
                                targetVelocity=0.0,
                                force=10.0)

        p.setJointMotorControl2(bodyUniqueId=cartesian,
                                jointIndex=2,
                                controlMode=p.VELOCITY_CONTROL,
                                targetVelocity=-0.1,
                                force=100)

        if p.getJointState(bodyUniqueId=cartesian, jointIndex=2)[0] < 0.8:
            p.setJointMotorControl2(bodyUniqueId=cartesian,
                                    jointIndex=2,
                                    controlMode=p.VELOCITY_CONTROL,
                                    targetVelocity=0,
                                    force=100)


p.disconnect()
