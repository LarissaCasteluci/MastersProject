import cv2
import numpy as np
import imageio

def get_camera_data_dummy():
    #im = imageio.imread("/home/larissa/MastersProject/2KukaExperiments/realsense_images/color_train_Color.png")
    # posso fazer 480, 480?
    #return np.zeros((640, 480)), np.zeros((640, 480))
    return np.zeros((300, 300)), np.zeros((3, 300, 300))


def run_inference_dummy():
    return 0, 0, 0


def calculate_perspective_camera_dummy():
    return 0, 0, 0


def tcp_control_dummy():
    return 0


def move_robot_dummy():
    return 0

