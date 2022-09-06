import glob
from pathlib import Path
import xml.etree.ElementTree as ET

obj_files_path: Path = Path("/home/larissa/MastersProject/1DatasetGeneration/assets/convex_hull_tests")
obj_files: list[str] = glob.glob(str(obj_files_path) + '/*.obj')

for obj in obj_files:
    mytree = ET.parse(obj_files_path / (Path(obj).stem + ".xml"))

