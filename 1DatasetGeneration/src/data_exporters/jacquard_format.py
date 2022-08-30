from base_data_exporter import BaseDataExporter
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


class JacquardDataExporter(BaseDataExporter):
    annotations_list: list[GraspAnnotation]
    save_path: str
    n_samples_per_object: int

    def __init__(self, n_samples_per_object=5):
        self.n_samples_per_object = n_samples_per_object

