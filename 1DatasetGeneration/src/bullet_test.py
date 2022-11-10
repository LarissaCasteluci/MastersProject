import pybullet as p
import time
import pybullet_data
from typing import List, Tuple
from dataset_generation_tools.robot_control.cartesian_robot_control import CartesianControl
from dataset_generation_tools.grasp_proposal_generator.grasp_proposal_types import TypesGenerator
from dataset_generation_tools.grasp_proposal_generator.proposal_generator import ProposalGenerator
from dataset_generation_tools.base_data_structures.camera_conversions import camera2world_coordinates
from dataset_generation_tools.base_data_structures.basic_types import *

pybullet_data_path: str = "/home/larissa/Git/bullet3/data/"
obj_path: str = "/home/larissa/MastersProject/1DatasetGeneration/assets/grasp_objects/"
gripper_path: str = "/home/larissa/MastersProject/1DatasetGeneration/assets/grippers_models/"

physicsClient: id = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
p.setGravity(0, 0, -10)
simulation_time: id = 60

planeId: id = p.loadURDF(pybullet_data_path + "plane.urdf")

cubeStartPos: xyz_list = [0, 0, 1]
cubeStartOrientation: quaternion_tuple = p.getQuaternionFromEuler([0, 0, 0])
cartesian: id = p.loadURDF(gripper_path + "cartesian.urdf", cubeStartPos, cubeStartOrientation)
boxId2: id = p.loadURDF(obj_path + "G2.urdf", [2, 2, 1], cubeStartOrientation)

robot: CartesianControl = CartesianControl(cartesian)

for n in range(p.getNumJoints(cartesian)):
   print(f"Information Joint {n}", p.getJointInfo(cartesian, n))

# Initialize classes
generator: ProposalGenerator = ProposalGenerator(TypesGenerator.RANDOM)
grasps: List[BasicGrasp] = generator.generate_proposals((300, 300))
world_size = [4, 4]

for grasp in grasps:

    print("GRASP:", grasp.x, grasp.y, grasp.theta)

    for step in range(simulation_time*240):
        p.stepSimulation()
        time.sleep(1./240.)
        cubePos, cubeOrn = p.getBasePositionAndOrientation(cartesian)

        #robot.grasp_xy = [grasp.x, grasp.y]
        robot.perform_grasp_pipeline(step)

    break
    p.resetSimulation(physicsClient)

p.disconnect()
