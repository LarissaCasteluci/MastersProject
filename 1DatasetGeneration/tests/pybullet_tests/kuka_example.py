import os
import time
import math
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pybullet as p
import pybullet_data
import cv2
import imageio_ffmpeg
from base64 import b64encode


class M:
    freq = 0.002
    target_pos = lambda t, freq: [0.45, 0.00 + 0.1 * math.sin(2 * 3.14 * freq * t), 0.35 + 0.1 * math.cos(2 * 3.14 * freq * t)]


class C:
    cam_target_pos = [0, 0, 0]
    cam_distance = 2.0
    cam_yaw, cam_pitch, cam_roll = 50, -30.0, 0
    cam_width, cam_height = 480, 360
    cam_up, cam_up_axis_idx, cam_near_plane, cam_far_plane, cam_fov = [0, 0, 1], 2, 0.01, 100, 60


class KukaExample:
    def __init__(self):
        p.connect(p.GUI)  # or p.GUI for graphical version
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -10)

        self.plane_id = p.loadURDF("plane.urdf")
        self.kuka_id = p.loadURDF("kuka_iiwa/model.urdf")
        self.num_joints = p.getNumJoints(self.kuka_id)
        self.kuka_end_effector_idx = 6

        self.vid = imageio_ffmpeg.write_frames('vid.mp4', (C.cam_width, C.cam_height), fps=30)
        self.vid.send(None)  # seed the video writer with a blank frame

    def __del__(self):
        self.vid.close()
        p.disconnect()

    def simulate(self):
        for t in range(4000):
            print(f'\rtimestep {t}...', end='')

            if t % 8 == 0:  # PyBullet default simulation time step is 240fps.
                cam_view_matrix = p.computeViewMatrixFromYawPitchRoll(C.cam_target_pos,
                                                                      C.cam_distance,
                                                                      C.cam_yaw,
                                                                      C.cam_pitch,
                                                                      C.cam_roll,
                                                                      C.cam_up_axis_idx)

                cam_projection_matrix = p.computeProjectionMatrixFOV(C.cam_fov,
                                                                     C.cam_width * 1. / C.cam_height,
                                                                     C.cam_near_plane,
                                                                     C.cam_far_plane)

                image = p.getCameraImage(C.cam_width, C.cam_height, cam_view_matrix, cam_projection_matrix)[2][:, :, :3]

                self.vid.send(np.ascontiguousarray(image))

            joint_poses = p.calculateInverseKinematics(self.kuka_id, self.kuka_end_effector_idx, M.target_pos(t, M.freq))

            for j in range(self.num_joints):
                p.setJointMotorControl2(bodyIndex=self.kuka_id, jointIndex=j,
                                        controlMode=p.POSITION_CONTROL, targetPosition=joint_poses[j])

            p.stepSimulation()

        plt.imshow(Image.fromarray(image))  # show the last frame



if __name__ == "__main__":

    example = KukaExample()
    example.simulate()


