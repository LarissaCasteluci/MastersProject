from .base_data_exporter import BaseDataExporter
from ..base_data_structures.jacquard_data import GraspAnnotation
import numpy as np
import os, sys
from dataclasses import dataclass


@dataclass
class ObjectSample:
    index: int
    grasps_list: list[GraspAnnotation]
    perfect_depth: np.array
    rgb: np.array
    stereo_depth: np.array


@dataclass
class ObjectData:
    object_id: int
    object_data: list[ObjectSample]


class JacquardDataExporter(BaseDataExporter):
    objects_id: list[int]
    objects_generated_data: list[ObjectData]
    save_path: str
    n_samples_per_object: int

    def __init__(self, save_path: str, n_samples_per_object: int = 5):
        self.save_path = save_path
        self.n_samples_per_object = n_samples_per_object
        self.objects_generated_data = []

        if not os.path.isdir(self.save_path):
            os.mkdir(self.save_path)
        else:
            sys.exit("Output Folder already exists")


    def add_new_object(self):
        # generate new id for the object
        pass

    def save(self):
        pass




