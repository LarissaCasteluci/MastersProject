from .basic_types import BasicGrasp, BasicGraspInWorldCoordinates
from typing import Tuple, List


def camera2world_coordinates(image_size: Tuple[int, int],
                             world_size: Tuple[int, int],
                             grasp: BasicGrasp) -> BasicGraspInWorldCoordinates:

    x_position = grasp.x * world_size[0] / image_size[0]
    y_position = grasp.y * world_size[1] / image_size[1]

    return BasicGraspInWorldCoordinates(x_position,
                                        y_position,
                                        grasp.theta)


def world2camera_coordinates(image_size: Tuple[int, int],
                             world_size: Tuple[int, int],
                             position: List[float]) -> List[float]:

    x_position = position[0] * image_size[0] / world_size[0]
    y_position = position[1] * image_size[1] / world_size[1]

    return [x_position, y_position]