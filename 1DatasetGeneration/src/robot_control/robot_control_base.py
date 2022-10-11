from pathlib import Path
from typing import List


class RobotControlBase():
    def __init__(self, urdf_path_file):
        self.urdf_path_file: Path = urdf_path_file
        idx_robot_joints: List[int]
        idx_gripper_joints: List[int]

    def robot_control(self):
        raise NotImplementedError

    def gripper_control(self):
        raise NotImplementedError

