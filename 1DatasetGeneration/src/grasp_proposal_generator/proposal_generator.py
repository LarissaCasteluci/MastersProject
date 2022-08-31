# TODO: Add License
from enum import Enum
from typing import List


class TypesGenerator(Enum):
    RANDOM = 0


class ProposalGenerator:
    def __init__(self, generator: TypesGenerator):
        self.generator = generator


    def generate_proposals(self, number: int): #-> List[]
        pass


