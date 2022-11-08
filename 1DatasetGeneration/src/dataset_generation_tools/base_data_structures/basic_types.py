from dataclasses import dataclass

pixels = float
degrees = float
meters = float


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