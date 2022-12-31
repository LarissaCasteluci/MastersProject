from .base_data_exporter import BaseDataExporter
from ..base_data_structures.jacquard_data import GraspAnnotation
import numpy as np
import os, sys
from dataclasses import dataclass
from csv import writer
from typing import List
import shutil
from PIL import Image

class CSVWriter:
    def __init__(self, path: str):
        if not os.path.isfile(path):
            open(path, 'a').close()  # Create output file if it doesn't exist

        self.path = path

    def append(self, data):
        with open(self.path, 'a+', newline='') as f:
            csv_writer = writer(f, delimiter =';')
            csv_writer.writerow(data)


class JacquardDataExporter(BaseDataExporter):
    objects_id: list[int]
    save_path: str
    n_samples_per_object: int

    def __init__(self, save_path: str, obj_name: str, repeat: str):
        self.save_path = save_path
        self.obj_name = obj_name
        self.repeat = repeat

        self.csv_writer = CSVWriter(save_path + f"/{repeat}_{obj_name}_grasps.txt" )

    def save_images(self):
        # Copy images to final dataset

        # RGB image
        ## Necessary to convert RGBA image to RGB
        im = Image.open(f"/1DatasetGeneration/outputs/tmp/{self.obj_name}_{str(self.repeat)}/camera1/rgba_00004.png")
        imarray = np.array(im)
        imarray = imarray[:, :, :-1]
        im = Image.fromarray(imarray)
        im.save(self.save_path + f"/{self.repeat}_{self.obj_name}_RGB.png")

        # Perfect Depth
        shutil.copy(f"/1DatasetGeneration/outputs/tmp/{self.obj_name}_{str(self.repeat)}/camera1/depth_00004.tiff",
                    self.save_path + f"/{self.repeat}_{self.obj_name}_perfect_depth.tiff")
        # Mask
        shutil.copy(f"/1DatasetGeneration/outputs/tmp/{self.obj_name}_{str(self.repeat)}/camera1/segmentation_00004.png",
                    self.save_path + f"/{self.repeat}_{self.obj_name}_mask.png")

    def save_grasps(self, grasp_data: List[float]):
        # According to jacquard dataset, the grasp data must be:
        # x;y;theta in degrees;opening;jaws size;
        self.csv_writer.append(grasp_data)




