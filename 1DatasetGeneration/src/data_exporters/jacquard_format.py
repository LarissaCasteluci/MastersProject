from base_data_exporter import BaseDataExporter
import numpy as np
from dataclasses import dataclass

pixels = float
degrees = float
centimeters = float


@dataclass
class GraspAnnotation:
    x: pixels
    y: pixels
    theta: degrees
    opening: centimeters
    jaws_size: centimeters


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
    object_id: int
    annotations_list: list[ObjectData]
    save_path: str
    n_samples_per_object: int

    def __init__(self, save_path: str, n_samples_per_object: int = 5):
        self.save_path = save_path
        self.n_samples_per_object = n_samples_per_object
        self.annotations_list = []

    def add_new_object(self):
        pass

    def save(self):
        pass



