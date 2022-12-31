# TODO: Add License
from typing import Tuple, List
import numpy as np
from .grasp_proposal_types import TypesGenerator
from ..base_data_structures.basic_types import BasicGrasp
import math


class ProposalGenerator:
    generator: TypesGenerator
    #rng: np.Generator
    max_proposals: int

    def __init__(self, generator: TypesGenerator,
                       max_proposals: int = 100):

        self.generator = generator
        self.rng = np.random.default_rng()
        self.max_proposals = max_proposals

    def generate_proposals(self,
                           size_image: Tuple[int, int],
                           obj_position: List[float] = [0, 0, 0]
                           ) -> List[BasicGrasp]:

        if self.generator == TypesGenerator.RANDOM:
            grasps = self._generate_random_proposals(size_image)
        else:
            grasps = self._generate_gaussian_proposals(size_image, obj_position)

        return grasps

    def _generate_random_proposals(self,
                                   size_image: Tuple[int, int]) -> List[BasicGrasp]:
        grasps = []
        for n in range(self.max_proposals):
            grasp = BasicGrasp(self.rng.random()*size_image[0],
                               self.rng.random()*size_image[1],
                               self.rng.random()*math.pi)

            grasps.append(grasp)

        return grasps

    def _generate_gaussian_proposals(self,
                                     size_image: Tuple[int, int],
                                     obj_position: List[float]): #-> List[BasicGrasp]
        grasps = []
        for n in range(self.max_proposals):
            x_gauss = math.floor(self.rng.normal(obj_position[0], math.ceil(size_image[0]*0.1)))
            y_gauss = math.floor(self.rng.normal(obj_position[1], math.ceil(size_image[1]*0.1)))
            angle = self.rng.random()*math.pi

            grasp = BasicGrasp(x_gauss,
                               y_gauss,
                               angle)

            grasps.append(grasp)

        return grasps
