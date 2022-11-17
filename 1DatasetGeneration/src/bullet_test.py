import pybullet as p
import time
import pybullet_data

from dataset_generation_tools.robot_control.cartesian_robot_control import CartesianControl, Movements
from dataset_generation_tools.grasp_proposal_generator.grasp_proposal_types import TypesGenerator
from dataset_generation_tools.grasp_proposal_generator.proposal_generator import ProposalGenerator
from dataset_generation_tools.base_data_structures.camera_conversions import camera2world_coordinates
from dataset_generation_tools.base_data_structures.basic_types import *

pybullet_data_path: str = "/home/larissa/Git/bullet3/data/"
obj_path: str = "/home/larissa/MastersProject/1DatasetGeneration/assets/grasp_objects/"
gripper_path: str = "/home/larissa/MastersProject/1DatasetGeneration/assets/grippers_models/"

physicsClient: id = p.connect(p.GUI)
simulation_time: id = 60
image_size = (300, 300)
world_size = (4, 4)

cubeStartOrientation: quaternion_tuple = p.getQuaternionFromEuler([0, 0, 0])

generator: ProposalGenerator = ProposalGenerator(TypesGenerator.RANDOM)
grasps: List[BasicGrasp] = generator.generate_proposals(image_size)

for grasp in grasps:

    g = camera2world_coordinates(image_size, world_size, grasp)
    print("GRASP:", g.x, g.y, g.theta)

    p.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
    p.setGravity(0, 0, -9.8)
    planeId: id = p.loadURDF(pybullet_data_path + "plane.urdf")

    cartesian: id = p.loadURDF(gripper_path + "cartesian.urdf", [0, 0, 1], cubeStartOrientation)
    robot: CartesianControl = CartesianControl(cartesian)

    for step in range(simulation_time * 240):
        p.stepSimulation()
        time.sleep(1. / 240.)

        if robot.is_in_movement == False and robot.current_movement == Movements.GO_TO_INITIAL_POSITION:
            boxId: id = p.loadURDF(obj_path + "A1.urdf", [5, 5, 0.3], cubeStartOrientation)

        if robot.is_in_movement == False and robot.current_movement == Movements.GO_TO_DROP_POSITION_2:
            Pos, _ = p.getBasePositionAndOrientation(boxId)
            print(Pos)

        robot.grasp_xy = [g.x, g.y]
        robot.gripper_angle = g.theta
        robot.perform_grasp_pipeline(step)
        if robot.has_performed_grasp_pipeline:
            break

    robot.reset_pipeline()
    p.resetSimulation(physicsClient)

p.disconnect()
