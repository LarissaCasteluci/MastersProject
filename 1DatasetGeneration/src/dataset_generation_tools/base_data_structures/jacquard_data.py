from dataclasses import dataclass
from enum import Enum
from .basic_types import pixels, degrees, centimeters


class JawsSizes(Enum):
    ONE_CENTIMETER = 1
    TWO_CENTIMETERS = 2
    THREE_CENTIMETERS = 3
    FOUR_CENTIMETERS = 4
    SIX_CENTIMETERS = 6


@dataclass
class GraspAnnotation:
    x: pixels
    y: pixels
    theta: degrees
    opening: centimeters
    jaws_size: JawsSizes

