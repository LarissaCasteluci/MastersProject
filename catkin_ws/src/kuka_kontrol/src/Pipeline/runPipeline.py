#!/usr/bin/env python3

import sys
import time
import rospy
from pathlib import Path
from kuka_ros_node import *
from camera import RealSenseCamera
from dummys import *
from inference_ggcnn import call_inference


class Arguments:
    def __init__(self):
        pass


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


def run_inference(args):  # returns x, y, alpha in image coordinates
    call_inference(args)




def calculate_perspective_camera():  # return x, y, alpha in world coordinates
    pass


def move_robot_XYZABC(position, mode):

    print('Started')
    kuka.send_command(f'setPositionXYZABC {position} {mode}')
    time.sleep(1)

    for i in range(100):
        print(f'isFinished? {kuka.isFinished}')
        time.sleep(1)
        if kuka.isFinished[0] : break
        if i == 99:
            print("max tries achieved")
            sys.exit()
        print(f"sleeped for {i} seconds")


    print('Finished')


def tcp_control():
    pass


def main():

    ### Set robot's configuration
    # Initial Position
    # Tool's size
    tool_s = 110  # size in z-axis in mm
    ip = f'-95 -500 {str(290 + tool_s)} - - -'
    n_experiments = 1

    set_robot_configurations()


    ### Set network's configuration
    network_name = 'ggcnn'
    args = Arguments()
    if network_name == "ggcnn":
        # Inference GG-CNN
        args.network_name = "ggcnn"
        args.network = str(Path())  # Path to weights

        # Dataset & Data & Training
        args.dataset = "realsense_inference"  # dataset format
        args.use_depth = 1  # Use depth
        args.use_rgb = 1  # use rgb
        args.ds_rotate = 0.0  # Shift the start point of the dataset to use a different test/train split
        args.num_workers = 8  # Dataset workers
        args.n_grasps = 1  # Number of grasps to consider per image
        #args.iou_eval = 'store_true'  # Compute success based on IoU metric
        #args.jacquard_output = 'store_true'  # Jacquard-dataset style output
        #args.vis = 'store_true'  # Visualise the network output'


    for i in range(n_experiments):
        #move_robot_XYZABC(ip, "ptp")
        move_robot_dummy()

        #args.depth, args.rgb = get_camera_data()  # Get camera Data ( Image )
        args.depth, args.rgb = get_camera_data_dummy()

        run_inference(args)
        #run_inference_dummy()

        #calculate_perspective_camera()
        calculate_perspective_camera_dummy()

        # TODO: Calculate grasp point based on what is received from the network
        gp = f'-95 -500 {str(0 + tool_s)} - - -'  # Grasp point --> this will be received from the network
        #move_robot_XYZABC(gp, "lin")
        move_robot_dummy()

        tcp_control_dummy()

        dp = f'100 -500 {str(290 + tool_s)} - - -'  # Drop Point
        #move_robot_XYZABC(dp, "ptp")
        move_robot_dummy()

        tcp_control_dummy()


if __name__ == "__main__":

    global kuka
    kuka = kuka_iiwa_ros_node()

    main()

