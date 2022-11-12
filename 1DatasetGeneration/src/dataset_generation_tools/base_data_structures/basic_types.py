from dataclasses import dataclass
from typing import List, Tuple

# Coordinate Types
xyz_list = List[float]
quaternion_tuple = Tuple[float]

# Pybullet types
id = int

radians = float
pixels = float
degrees = float
meters = float
centimeters = float

# @dataclass
# class xyz:
#     x: meters
#     y: meters
#     z: meters
#
#     @
#     def __init__(self, xyz_list : List[float, float, float]):



@dataclass
class BasicGrasp:
    x: pixels
    y: pixels
    theta: degrees


@dataclass
class BasicGraspInWorldCoordinates:
    x: meters
    y: meters
    theta: degrees