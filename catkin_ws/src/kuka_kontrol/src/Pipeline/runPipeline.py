#!/usr/bin/env python3
import sys
import time
from kuka_ros_node import *
from camera import RealSenseCamera
from dummys import *
from utils.dataset_processing.image import Image, DepthImage
from inference_ggcnn import call_inference
import matplotlib.pyplot as plt
from Arguments import TestTypes, Arguments  # Test Configurations
import pyrealsense2 as rs
from utils.dataset_processing.grasp import Grasp as GraspGGCNN2
import signal
from gripper_control import GripperControl


def signal_handler(sig, frame):
    sys.exit(0)


OUTPUT_SIZE = 300


def format_depth_data(depth):
    if type(depth) == str:
        depth_img = DepthImage.from_tiff(depth)
    elif type(depth) == np.ndarray:
        depth_img = DepthImage(depth)
    else:
        raise Exception("This type is not implemented")
    depth_img.rotate(0)
    depth_img.normalise()
    depth_img.zoom(1.0)
    depth_img.resize((480, 640))
    return depth_img.img


def format_rgb_data(color):
    if type(color) == str:
        rgb_img = Image.from_file(color)
    elif type(color) == np.ndarray:
        rgb_img = Image(color)
    else:
        raise Exception("This type is not implemented")
    rgb_img.rotate(0)
    rgb_img.zoom(1.0)
    rgb_img.resize((480, 640))
    rgb_img.normalise()
    rgb_img.img = rgb_img.img.transpose((2, 0, 1))
    return rgb_img.img


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


def show_images(color_image):
    imgplot = plt.imshow(color_image.transpose((1, 2, 0)))
    plt.show()


def read_jacquard_data():
    color_path = "/home/larissa/DATASETS/Jacquard/3f278036c8757f62f6405aff89e48d03/3_3f278036c8757f62f6405aff89e48d03_RGB.png"
    depth_path = "/home/larissa/DATASETS/Jacquard/3f278036c8757f62f6405aff89e48d03/3_3f278036c8757f62f6405aff89e48d03_perfect_depth.tiff"
    color = format_rgb_data(color_path)
    depth = format_depth_data(depth_path)
    return depth, color


def get_camera_data(camera: RealSenseCamera):  # returns Images
    #depth, color = camera.get_single_frame()
    depth, color, color_intrinsics = camera.align_depth2color()
    color = format_rgb_data(color)
    depth = format_depth_data(depth)
    return depth, color, color_intrinsics


def run_inference(args):  # returns x, y, alpha in image coordinates
    grasps = call_inference(args)
    return grasps[0]


def calculate_perspective_camera(color_intrinsics, grasp: GraspGGCNN2):  # return x, y, alpha in world coordinates
    return rs.rs2_deproject_pixel_to_point(color_intrinsics,
                                           [grasp.center[1], grasp.center[0]], 0.3)


def move_robot_XYZABC(position, mode):

    print('Started')
    kuka.send_command(f'setPositionXYZABC {position} {mode}')
    time.sleep(1)

    for i in range(100):
        print(f'isFinished? {kuka.isFinished}')
        time.sleep(1)
        if kuka.isFinished[0]: break
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
    tool_s: int = 110  # size in z-axis in mm
    initial_point = [-75, 700, 430]
    ip: str = f'{initial_point[0]} {initial_point[1]} {initial_point[2] - tool_s} 0 0 179'  # X Y Z A B C
    n_experiments: int = 1

    set_robot_configurations()

    ### Set network's configuration
    network_name: str = 'ggcnn2'
    test_type: TestTypes = TestTypes.RGB_AND_DEPTH
    args: Arguments = Arguments(network_name, test_type)

    # Initialize camera
    camera: RealSenseCamera = RealSenseCamera()

    # Connect to gripper
    gripper: GripperControl = GripperControl("172.31.1.171", 5500)
    gripper.connect()


    for i in range(n_experiments):
        move_robot_XYZABC(ip, "ptp")  # move_robot_dummy()
        gripper.command_calibration()

        args.depth, args.rgb, color_intrinsics = get_camera_data(camera)  # Get camera Data ( Image )
        if args.save:
            np.save("/home/larissa/MastersProject/2KukaExperiments/image_sample/rgb.npy", args.rgb)
            np.save("/home/larissa/MastersProject/2KukaExperiments/image_sample/depth.npy", args.depth)
        show_images(args.rgb)
        #args.depth, args.rgb = get_camera_data_dummy()
        #args.depth, args.rgb = read_jacquard_data()

        grasp: GraspGGCNN2 = run_inference(args)
        print("Grasp Proposal is image coordinates: ", grasp.center[1], grasp.center[0])

        grasp_w = calculate_perspective_camera(color_intrinsics, grasp) #calculate_perspective_camera_dummy()
        print("Grasp Proposal in world coordinates: ", grasp_w)

        gp1: str = f'{initial_point[0]} {initial_point[1]} {300 - tool_s} 0 0 179'  # X Y Z A B C
        move_robot_XYZABC(gp1, "lin")
        print("Finished Part 1")

        gp: str = f'{initial_point[0] - grasp_w[0]*1000 + 40} {initial_point[1] + grasp_w[1]*1000 -110} {250 - tool_s} 0 0 179'  # X Y Z A B C
        move_robot_XYZABC(gp, "lin")

        print("Finished Part 2")
        # TODO: Calculate grasp point based on what is received from the network
        #gp = f'-95 -500 {str(0 + tool_s)} - - -'  # Grasp point --> this will be received from the network
        #move_robot_XYZABC(gp, "lin")
        move_robot_dummy()

        tcp_control_dummy()

        dp = f'100 -500 {str(290 + tool_s)} - - -'  # Drop Point
        #move_robot_XYZABC(dp, "ptp")
        move_robot_dummy()

        tcp_control_dummy()


if __name__ == "__main__":

    signal.signal(signal.SIGINT, signal_handler)

    global kuka
    kuka = kuka_iiwa_ros_node()

    main()

