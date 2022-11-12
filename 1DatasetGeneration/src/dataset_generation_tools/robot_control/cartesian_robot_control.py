from pathlib import Path
from typing import List
import pybullet as p
import sys
from enum import Enum
from ..base_data_structures.basic_types import *


class JointState(Enum):
    STOPPED = 0
    MOVING = 1
    APPLY_FORCE = 2


class Joint:
    def __init__(self,  bodyUniqueId: int = -1,
                        jointIndex: int = -1,
                        targetVelocity: float = 0,
                        force: float = 0,
                        joint_type: str = "prismatic"):

        self._debug: bool = False
        self.bodyUniqueId: int = bodyUniqueId
        self.jointIndex: int = jointIndex
        self.targetVelocity: float = targetVelocity
        self.force: float = force
        self.joint_type: str = joint_type
        self.state_at_start_of_movement: float = self._joint_state()
        self.start_of_limit_range: dict = {"step": 0, "state": self._joint_state()}
        self.current_counter_for_timeout: int = 0
        self.current_simulation_step: int = 0
        self.joint_state: JointState = JointState.STOPPED

        if bodyUniqueId != -1 and jointIndex != -1:
            self._stop_joint()
        else:
            print("Define the bodyUniqueId and jointIndex!")
            sys.exit()

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, debug: bool):
        self._debug = debug

    def joint_control(self, goal: float, step: int, apply_force: bool):

        self.current_simulation_step = step

        state: float = self._joint_state()
        if abs(self.state_at_start_of_movement - goal) < 0.05:  # positioning precision
            direction = 0
        else:
            direction: float = (goal - self.state_at_start_of_movement)/abs(goal - self.state_at_start_of_movement)

        if self._debug:
            print("My state:", self.joint_state)
            print("goal:", goal)
            print("state:", state)

        # Positioning Stop
        if direction > 0:
            if goal > state:
                vel = self.targetVelocity
                self._move_joint(vel)
            else:
                self.state_at_start_of_movement = self._joint_state()
                self._stop_joint()
        elif direction < 0:
            if goal < state:
                vel = -self.targetVelocity
                self._move_joint(vel)
            else:
                self.state_at_start_of_movement = self._joint_state()
                self._stop_joint()
        else:
            self.state_at_start_of_movement = self._joint_state()
            self._stop_joint()

        # Force Stop
        if self.joint_state == JointState.MOVING:
            # btw cicles, if joint has not advanced enough, consider it stopped
            if abs(self.start_of_limit_range["state"] - self._joint_state()) < 0.01:
                self.current_counter_for_timeout += 1
            else:
                self.current_counter_for_timeout = 0
                self.start_of_limit_range["state"] = self._joint_state()

            if self.current_counter_for_timeout > 100:  # 100 steps to timeout

                if apply_force:
                    self._apply_force(vel)
                else:
                    self.state_at_start_of_movement = self._joint_state()
                    self._stop_joint()

    def _stop_joint(self):


        p.setJointMotorControl2(bodyUniqueId=self.bodyUniqueId,
                                jointIndex=self.jointIndex,
                                controlMode=p.VELOCITY_CONTROL,
                                targetVelocity=0.0,
                                force=self.force)

        self.joint_state: JointState = JointState.STOPPED
        self.current_counter_for_timeout = 0

    def _move_joint(self, velocity):

        if self._debug: print("move joint is called!")

        p.setJointMotorControl2(bodyUniqueId=self.bodyUniqueId,
                                jointIndex=self.jointIndex,
                                controlMode=p.VELOCITY_CONTROL,
                                targetVelocity=velocity,
                                force=self.force)

        if self.joint_state == JointState.STOPPED:
            self.start_of_limit_range["step"] = self.current_simulation_step
            self.start_of_limit_range["state"] = self._joint_state()

        self.joint_state: JointState = JointState.MOVING

    def _apply_force(self, velocity):

        p.setJointMotorControl2(bodyUniqueId=self.bodyUniqueId,
                                jointIndex=self.jointIndex,
                                controlMode=p.VELOCITY_CONTROL,
                                targetVelocity=velocity,
                                force=self.force)

        self.joint_state: JointState = JointState.APPLY_FORCE

    def _joint_state(self) -> float:
        if self.joint_type == "prismatic":
            return p.getJointState(bodyUniqueId=self.bodyUniqueId, jointIndex=self.jointIndex)[0]
        elif self.joint_type == "revolution":
            return p.getJointState(bodyUniqueId=self.bodyUniqueId, jointIndex=self.jointIndex)[0]


class Movements(Enum):
    GO_TO_INITIAL_POSITION = 0
    GO_TO_GRASP_POSITION = 1
    PERFORM_GRASP_PART_1 = 2
    PERFORM_GRASP_PART_2 = 3
    PERFORM_GRASP_PART_3 = 4
    GO_TO_DROP_POSITION_1 = 5
    GO_TO_DROP_POSITION_2 = 6
    GO_TO_DROP_POSITION_3 = 7
    DROP = 9
    FINISH = 10


class CartesianControl:
    _start_xyz: xyz_list
    _drop_xyz: xyz_list
    _grasp_position_xy: List[float]
    _grasp_position_z: List[float]
    _gripper_closed: List[float]
    _gripper_open: List[float]
    _gripper_angle: List[radians]
    _debug: bool
    _step_start_wait: int

    idx_robot_prismatic_joints: List[int]
    idx_robot_revolution_joints: List[int]
    idx_gripper_joints: List[int]
    is_in_movement: bool
    current_movement: Movements
    next_movement: Movements
    has_performed_grasp_pipeline: bool
    current_step: int = 0
    joints: List[Joint]

    def __init__(self, bodyUniqueId: int):

        # private
        self._start_xyz: xyz_list = [0, 0, 3]
        self._drop_xyz: xyz_list = [0, 2, 3]
        self._grasp_position_xy: List[float] = [1.7, -0.1]
        self._grasp_position_z: List[float] = [0.4]
        self._gripper_closed: List[float] = [-0.8, 0.8]
        self._gripper_open: List[float] = [0.0, 0.0]
        self._gripper_angle: List[radians] = [3.1415/2]
        self._debug: bool = False
        self. _step_start_wait: int = 0

        # public
        self.idx_robot_prismatic_joints: List[int] = [2, 3, 4]
        self.idx_robot_revolution_joints: List[int] = [5]
        self.idx_gripper_joints: List[int] = [6, 7]
        self.is_in_movement: bool = False
        self.current_movement: Movements = Movements.FINISH
        self.next_movement: Movements = Movements.GO_TO_INITIAL_POSITION
        self.has_performed_grasp_pipeline: bool = False
        self.current_step: int = 0

        self.joints: List[Joint] = [
                                     # 0 - joint_fix
                                     Joint(bodyUniqueId=bodyUniqueId,
                                           jointIndex=0,
                                           joint_type="fixed"),
                                     # 1 - base_zaxis_joint
                                     Joint(bodyUniqueId=bodyUniqueId,
                                           jointIndex=1,
                                           joint_type="fixed"),
                                     # 2 - z_axis_link_prismatic_joint
                                     Joint(bodyUniqueId=bodyUniqueId,
                                           jointIndex=2,
                                           targetVelocity=1,
                                           force=1000,
                                           joint_type="prismatic"),
                                     # 3 - x_axis_link_prismatic_joint
                                     Joint(bodyUniqueId=bodyUniqueId,
                                           jointIndex=3,
                                           targetVelocity=0.5,
                                           force=10,
                                           joint_type="prismatic"),
                                     # 4 - y_axis_link_prismatic_joint
                                     Joint(bodyUniqueId=bodyUniqueId,
                                           jointIndex=4,
                                           targetVelocity=0.5,
                                           force=10,
                                           joint_type="prismatic"),
                                    # 5 - base_gripper_revolution_joint
                                    Joint(bodyUniqueId=bodyUniqueId,
                                          jointIndex=5,
                                          targetVelocity=0.5,
                                          force=10,
                                          joint_type="revolution"),
                                    # 6 - hand_gripper_right_finger_joint
                                    Joint(bodyUniqueId=bodyUniqueId,
                                          jointIndex=6,
                                          targetVelocity=0.5,
                                          force=200,
                                          joint_type="prismatic"),
                                    # 7 - hand_gripper_left_finger_joint
                                    Joint(bodyUniqueId=bodyUniqueId,
                                          jointIndex=7,
                                          targetVelocity=0.5,
                                          force=200,
                                          joint_type="prismatic")
            ]

    @property
    def start_xyz(self):
        return self._start_xyz

    @start_xyz.setter
    def start_xyz(self, xyz: xyz_list):
        self._start_xyz = xyz

    @property
    def drop_xyz(self):
        return self._drop_xyz

    @drop_xyz.setter
    def drop_xyz(self, xyz: xyz_list):
        self._drop_xyz = xyz

    @property
    def grasp_xy(self):
        return [self._grasp_position_xy[0], self._grasp_position_xy[1] + 2]

    @grasp_xy.setter
    def grasp_xy(self, xy: List[float]):
        self._grasp_position_xy[0] = xy[0]
        self._grasp_position_xy[1] = xy[1] - 2

    @property
    def gripper_angle(self):
        return self._gripper_angle

    @gripper_angle.setter
    def gripper_angle(self, angle: float):
        self._gripper_angle = [angle]

    def reset_pipeline(self):
        self.has_performed_grasp_pipeline = False

    def perform_grasp_pipeline(self, step: int):

        self.current_step = step

        if self.has_performed_grasp_pipeline is True:
            return

        if (self.next_movement == Movements.GO_TO_INITIAL_POSITION and
            self.is_in_movement is False):

            self.is_in_movement = True
            self.current_movement = Movements.GO_TO_INITIAL_POSITION
            self.next_movement = Movements.GO_TO_GRASP_POSITION
            self._initial_position()
            print("GO_TO_INITIAL_POSITION")

        elif (self.next_movement == Movements.GO_TO_GRASP_POSITION and
              self.is_in_movement is False):

            self.is_in_movement = True
            self.current_movement = Movements.GO_TO_GRASP_POSITION
            self.next_movement = Movements.PERFORM_GRASP_PART_1
            self._go_to_grasp_position()
            print("GO_TO_GRASP_POSITION")

        elif (self.next_movement == Movements.PERFORM_GRASP_PART_1 and
              self.is_in_movement is False):

            self.is_in_movement = True
            self.current_movement = Movements.PERFORM_GRASP_PART_1
            self.next_movement = Movements.PERFORM_GRASP_PART_2
            self._perform_grasp_part_1()
            print("PERFORM_GRASP_PART_1")

        elif (self.next_movement == Movements.PERFORM_GRASP_PART_2 and
              self.is_in_movement is False):

            self.is_in_movement = True
            self.current_movement = Movements.PERFORM_GRASP_PART_2
            self.next_movement = Movements.PERFORM_GRASP_PART_3
            self._perform_grasp_part_2()
            print("PERFORM_GRASP_PART_2")

        elif (self.next_movement == Movements.PERFORM_GRASP_PART_3 and
              self.is_in_movement is False):

            self.is_in_movement = True
            self.current_movement = Movements.PERFORM_GRASP_PART_3
            self.next_movement = Movements.GO_TO_DROP_POSITION_1
            self._perform_grasp_part_3()
            print("PERFORM_GRASP_PART_3")

        elif (self.next_movement == Movements.GO_TO_DROP_POSITION_1 and
              self.is_in_movement is False):

            self.is_in_movement = True
            self.current_movement = Movements.GO_TO_DROP_POSITION_1
            self.next_movement = Movements.GO_TO_DROP_POSITION_2
            self._drop_position_1()
            print("GO_TO_DROP_POSITION_1")

        elif (self.next_movement == Movements.GO_TO_DROP_POSITION_2 and
              self.is_in_movement is False):

            self.is_in_movement = True
            self.current_movement = Movements.GO_TO_DROP_POSITION_2
            self.next_movement = Movements.GO_TO_DROP_POSITION_3
            self._drop_position_2()
            print("GO_TO_DROP_POSITION_2")

        elif (self.next_movement == Movements.GO_TO_DROP_POSITION_3 and
              self.is_in_movement is False):

            self.is_in_movement = True
            self.current_movement = Movements.GO_TO_DROP_POSITION_3
            self.next_movement = Movements.DROP
            self._drop_position_3()
            print("GO_TO_DROP_POSITION_3")

        elif (self.next_movement == Movements.DROP and
              self.is_in_movement is False):

            self.is_in_movement = True
            self.current_movement = Movements.DROP
            self.next_movement = Movements.FINISH
            self._drop()
            print("DROP")

        elif (self.next_movement == Movements.FINISH and
              self.is_in_movement is False):

            self.is_in_movement = True
            self.current_movement = Movements.FINISH
            self.next_movement = Movements.FINISH
            self.has_performed_grasp_pipeline = True
            print("has_performed_grasp_pipeline")

        if self.is_in_movement is True:

            if self.current_movement == Movements.GO_TO_INITIAL_POSITION:
                self._initial_position()
            elif self.current_movement == Movements.GO_TO_GRASP_POSITION:
                self._go_to_grasp_position()
            elif self.current_movement == Movements.PERFORM_GRASP_PART_1:
                self._perform_grasp_part_1()
            elif self.current_movement == Movements.PERFORM_GRASP_PART_2:
                self._perform_grasp_part_2()
            elif self.current_movement == Movements.PERFORM_GRASP_PART_3:
                self._perform_grasp_part_3()
            elif self.current_movement == Movements.GO_TO_DROP_POSITION_1:
                self._drop_position_1()
            elif self.current_movement == Movements.GO_TO_DROP_POSITION_2:
                self._drop_position_2()
            elif self.current_movement == Movements.GO_TO_DROP_POSITION_3:
                self._drop_position_3()
            elif self.current_movement == Movements.DROP:
                self._drop()

            are_all_joints_stopped = True
            for joint in self.joints:
                if joint.joint_state == JointState.MOVING:
                    are_all_joints_stopped = False

            if are_all_joints_stopped:
                self.is_in_movement = False

    def _initial_position(self):
        self.joints[2].joint_control(self._start_xyz[2], self.current_step, False)  # z
        self.joints[3].joint_control(self._start_xyz[0], self.current_step, False)  # x
        self.joints[4].joint_control(self._start_xyz[1], self.current_step, False)  # y

    def _go_to_grasp_position(self):
        self.joints[3].joint_control(self._grasp_position_xy[0], self.current_step, False)   # x
        self.joints[4].joint_control(self._grasp_position_xy[1], self.current_step, False)  # y

    def _perform_grasp_part_1(self):
        self.joints[5].joint_control(self._gripper_angle[0], self.current_step, False)  # revolution joint

    def _perform_grasp_part_2(self):
        self.joints[2].joint_control(self._grasp_position_z[0], self.current_step, False)  # z

    def _perform_grasp_part_3(self):
        self.joints[6].joint_control(self._gripper_closed[0], self.current_step, True)  # right
        self.joints[7].joint_control(self._gripper_closed[1], self.current_step, True)   # left

    def _drop_position_1(self):
        self.joints[2].joint_control(self._drop_xyz[2], self.current_step, False)  # z

    def _drop_position_2(self):
        self.joints[3].joint_control(self._drop_xyz[0], self.current_step, False)  # x
        self.joints[4].joint_control(self._drop_xyz[1], self.current_step, False)  # y

    def _drop_position_3(self):
        self.joints[5].joint_control(0, self.current_step, False)  # revolution joint

    def _drop(self):
        self.joints[6].joint_control(self._gripper_open[0], self.current_step, False)  # right
        self.joints[7].joint_control(self._gripper_open[1], self.current_step, False)  # left
