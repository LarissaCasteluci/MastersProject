import cv2
import numpy as np
import imageio

def get_camera_data_dummy():
    #im = imageio.imread("/home/larissa/MastersProject/2KukaExperiments/realsense_images/color_train_Color.png")
    #return np.zeros((640, 480)), np.zeros((640, 480))
    #return np.zeros((300, 300)), np.zeros((3, 300, 300))
    color = np.load("/home/larissa/MastersProject/2KukaExperiments/image_sample/rgb.npy")
    depth = np.load("/home/larissa/MastersProject/2KukaExperiments/image_sample/depth.npy")
    return depth, color


def run_inference_dummy():
    return 0, 0, 0


def calculate_perspective_camera_dummy():
    return 0, 0, 0


def tcp_control_dummy():
    return 0


def move_robot_dummy():
    return 0

