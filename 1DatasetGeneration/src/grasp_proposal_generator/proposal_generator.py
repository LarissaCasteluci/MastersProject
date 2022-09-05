# TODO: Add License
from enum import Enum
from typing import List, Tuple
from ..base.jacquard import GraspAnnotation
import random


class TypesGenerator(Enum):
    RANDOM = 0


class ProposalGenerator:
    generator: TypesGenerator

    def __init__(self, generator: TypesGenerator):
        self.generator = generator

    def generate_proposals(self, size_image: Tuple[int, int], number_proposals: int): #-> List[GraspAnnotation]
        if self.generator == TypesGenerator.RANDOM:
            grasps = self._generate_random_proposals(size_image, number_proposals)

        return grasps


    def _generate_random_proposals(self, size_image: Tuple[int, int], number_proposals: int): #-> List[GraspAnnotation]

        for n in number_proposals:

            x