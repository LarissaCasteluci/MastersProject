import numpy as np
import cv2
from PIL import Image


class StereoMatching:
    def __init__(self, imgL_path, imgR_path):
        self.imgL = cv2.imread(imgL_path, cv2.IMREAD_GRAYSCALE)
        self.imgR = cv2.imread(imgR_path, cv2.IMREAD_GRAYSCALE)

    def generate_stereo_image(self, path_name: str):
        stereo = cv2.StereoSGBM_create(
                              numDisparities=2,
                              blockSize=1,
                              )
        disp: np.float32 = stereo.compute(self.imgL, self.imgR).astype(np.float32) / 16.0

        im = Image.fromarray(disp)
        im.save(path_name)