from .basic_types import BasicGrasp, BasicGraspInWorldCoordinates
from typing import Tuple


def camera2world_coordinates(image_size: Tuple[int, int],
                             world_size: Tuple[int, int],
                             grasp: BasicGrasp) -> BasicGraspInWorldCoordinates:

    x_position = grasp.x * world_size[0] / image_size[0]
    y_position = grasp.y * world_size[1] / image_size[1]

    return BasicGraspInWorldCoordinates(x_position,
                                        y_position,
                                        BasicGrasp.theta)