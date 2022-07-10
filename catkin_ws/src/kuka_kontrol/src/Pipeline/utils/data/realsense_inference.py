import os
import glob

from .grasp_data import GraspDatasetBase
from utils.dataset_processing import grasp, image
import numpy as np
import torch

#class RealSenseData(GraspDatasetBase):
class RealSenseData():
    """
    Dataset wrapper for the Jacquard dataset.
    """
    def __init__(self, depth, image, include_depth, include_rgb):
        """
        :param kwargs: kwargs for GraspDatasetBase
        """
        self.depth = depth
        self.image = image
        self.include_depth = include_depth
        self.include_rgb = include_rgb

    def return_x(self):

        depth_img = self.get_depth()
        rgb_img = self.get_rgb()

        if self.include_depth and self.include_rgb:
            x = self.numpy_to_torch(
                np.expand_dims(
                    np.concatenate(
                        (np.expand_dims(depth_img, 0), rgb_img), 0)
                , 0)
            )
        elif self.include_depth:
            x = self.numpy_to_torch(depth_img)
        elif self.include_rgb:
            x = self.numpy_to_torch(rgb_img)
        else:
            raise Exception("no include_depth or include_rgb defined")

        return x

    def __len__(self):
        return 1

    @staticmethod
    def numpy_to_torch(s):
        if len(s.shape) == 2:
            return torch.from_numpy(np.expand_dims(s, 0).astype(np.float32))
        else:
            return torch.from_numpy(s.astype(np.float32))

    def get_gtbb(self, idx=0, rot=0, zoom=1.0):
        return 0

    def get_depth(self, idx=0, rot=0, zoom=1.0):
        return self.depth

    def get_rgb(self, idx=0, rot=0, zoom=1.0, normalise=True):
        return self.image

    def get_jname(self, idx):
        return 'grasp_inference'