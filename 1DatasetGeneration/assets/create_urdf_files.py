import glob
from pathlib import Path
import xml.etree.ElementTree as ET

obj_files_path: Path = Path("/home/larissa/MastersProject/1DatasetGeneration/assets/convex_hull_tests")
obj_files: list[str] = glob.glob(str(obj_files_path) + '/*.obj')

for obj in obj_files:
    file_to_create = obj_files_path / (Path(obj).stem + ".urdf")
    root = ET.Element("robot", name=Path(obj).stem)
    link = ET.SubElement(root, "link", name="base")
    
    inertial = ET.SubElement(link, "inertial")
    origin = ET.SubElement(inertial, "origin", xyz="-0.0 -0.0 -0.0")
    mass = ET.SubElement(inertial, "mass", value="0.3227")
    inertia = ET.SubElement(inertial, "inertia",
        ixx="0.0244", ixy="0.0", ixz="0.0", iyy="0.0215",
        iyz="-0.0", izz="0.0305")
    
    visual = ET.SubElement(link, "visual")
    origin = ET.SubElement(visual, "origin", xyz="-0.0 -0.0 -0.0")
    geometry = ET.SubElement(visual, "geometry")
    mesh = ET.SubElement(geometry, "mesh", filename="/1DatasetGeneration/assets/grasp_objects/C0.obj")
    collision = ET.SubElement(link, "collision")
    origin = ET.SubElement(collision, "origin", xyz="0.0 0.0 0.0")
    geometry = ET.SubElement(collision, "geometry")
    mesh = ET.SubElement(geometry, "mesh", filename=obj[28:])

    tree = ET.ElementTree(root)
    ET.indent(tree, '  ')
    tree.write(file_to_create)
    print("saved ", file_to_create)




