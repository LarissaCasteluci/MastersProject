#!/usr/bin/env python3

import rospy
from kuka_ros_node import *
from camera import RealSenseCamera
from dummys import *


def set_robot_configurations():

    while not kuka.isReady: pass
    print('Started!')

    kuka.send_command('setTool tool1')

    # Define Slow velocities
    acc, vel, jerk, carvel = 0.5, 0.1, 0.5, 50
    kuka.send_command(f'setJointAcceleration {acc}')
    kuka.send_command(f'setJointVelocity {vel}')
    kuka.send_command(f'setJointJerk {jerk}')
    kuka.send_command(f'setCartVelocity {carvel}')


def get_camera_data():  # returns Images
    camera = RealSenseCamera
    depth, color = RealSenseCamera.get_single_frame()
    return depth, color


def run_inference(neuralnetwork, depth, color):  # returns x,y, alpha in image coordinates

    pass


def calculate_perspective_camera():  # return x, y, alpha in world coordinates
    pass


def move_robot(position, mode):

    kuka.send_command(f'setPositionXYZABC {position} {mode}')


def tcp_control():
    pass


def main():

    # Initial Position
    ip = f'366 321 -319 0 0 0'
    n_experiments = 1

    set_robot_configurations()

    for i in range(n_experiments):
        kuka.send_command(f'setPositionXYZABC {ip} ptp')

        #get_camera_data()  # Get camera Data ( Image )
        get_camera_data_dummy()

        #run_inference(network)  # Get
        run_inference_dummy()

        #calculate_perspective_camera()
        calculate_perspective_camera_dummy()

        # TODO: Calculate grasp point based on what is received from the network
        gp = f'366 321 -44 0 0 0'  # Grasp point --> this will be received from the network
        move_robot(gp, "lin")

        tcp_control_dummy()

        dp = f'641 170 -319 0 0 0'  # Drop Point
        move_robot(dp, "ptp")

        tcp_control_dummy()


if __name__ == "__main__":

    global kuka
    kuka = kuka_iiwa_ros_node()

    main()

