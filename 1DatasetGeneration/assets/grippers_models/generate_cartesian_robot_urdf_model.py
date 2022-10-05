import random
import xml.etree.ElementTree as ET
import os

materials = [["blue", "0 0 0.6 1"],
            ["yellow", "1 1 0.5 1"],
            ["green", "0.5 1 0 1"],
            ["light_red", "0.9 0 0 1"],
            ["white", "1 1 1 1"],
            ["grey", "0.8 0.8 0.8 1"],
            ["black", "0 0 0 1"]]

def convert_to_str(alist):
    s = ""
    for e in alist:
        s += str(e)
        s += " "
    s = s[:-1]
    return s

def configure_joint_basic(robot, name, type, parent, child):
    joint = ET.SubElement(robot, "joint", name=name, type=type)
    parent = ET.SubElement(joint, "parent", link=parent)
    child = ET.SubElement(joint, "child", link=child)



def configure_joint(robot, name, type, parent, child, origin_data, axis_data, limits):
    joint = ET.SubElement(robot, "joint", name=name, type=type)
    parent = ET.SubElement(joint, "parent", link=parent)
    child = ET.SubElement(joint, "child", link=child)
    origin = ET.SubElement(joint, "origin", xyz=origin_data[0], rpy=origin_data[1])
    axis = ET.SubElement(joint, "axis", xyz=axis_data[0])
    limits = ET.SubElement(joint, "limit", effort=limits[0], velocity=limits[1], lower=limits[2], upper=limits[3])



def configure_link(robot, name, origin_data, geometry_shape, geometry_data, mass_value):
    link = ET.SubElement(robot, "link", name=name)
    collision = ET.SubElement(link, "collision")
    c_origin = ET.SubElement(collision, "origin", xyz=origin_data[0], rpy=origin_data[1])
    c_geometry = ET.SubElement(collision, "geometry")
    visual = ET.SubElement(link, "visual")
    v_origin = ET.SubElement(visual, "origin", xyz=origin_data[0], rpy=origin_data[1])
    v_geometry = ET.SubElement(visual, "geometry")

    if geometry_shape == "box":
        shape = ET.SubElement(c_geometry, geometry_shape, size=geometry_data[0])
        shape = ET.SubElement(v_geometry, geometry_shape, size=geometry_data[0])
    elif geometry_shape == "cylinder":
        shape = ET.SubElement(c_geometry, geometry_shape, length=geometry_data[0], radius=geometry_data[1])
        shape = ET.SubElement(v_geometry, geometry_shape, length=geometry_data[0], radius=geometry_data[1])

    name_material = materials[random.randint(0, len(materials) - 1)][0]
    m = ET.SubElement(visual, "material", name=name_material)

    inertial = ET.SubElement(link, "inertial")
    i_origin = ET.SubElement(inertial, "origin", xyz=origin_data[0], rpy=origin_data[1])
    mass = ET.SubElement(inertial, "mass", value=mass_value)
    inertia = ET.SubElement(inertial, "inertia", ixx="0.001", ixy="0", ixz="0", iyy="0.001", iyz="0", izz="0.01")



if __name__ == "__main__":
    robot = ET.Element("robot", name="cartesian")

    for material in materials:
        m = ET.SubElement(robot, "material", name=material[0])
        color = ET.SubElement(m, "color", rgba=material[1])

    # Base
    world = ET.SubElement(robot, "link", name="world")

    base_position = [0, 0, -1]
    configure_joint_basic(robot, "joint_fix", "fixed", "world", "world_base")
    configure_link(robot, "world_base", origin_data=[convert_to_str(base_position), "0 0 0"],
                                        geometry_shape="box",
                                        geometry_data=["0.2 0.2 0.1"],
                                        mass_value="1")

    # Joint: Base -> Z-Axis
    configure_joint_basic(robot, "base_zaxis_joint", "fixed", "world_base", "z_axis_link")

    # Z-Axis
    height = 4
    z_axis_link_position = [0, 0, 0]
    z_axis_link_position[0] = base_position[0]
    z_axis_link_position[1] = base_position[1]
    z_axis_link_position[2] = base_position[2] + height/2
    configure_link(robot, "z_axis_link", origin_data=[convert_to_str(z_axis_link_position), "0 0 0"],
                                        geometry_shape="box",
                                        geometry_data=[f"0.2 0.2 {height}"],
                                        mass_value="1")
    # Joint: Z-Axis -> X-Axis
    configure_joint(robot, "z_axis_link_prismatic_joint", "prismatic", "z_axis_link", "x_axis_link",
                    origin_data=[f"0 0 {str(z_axis_link_position[2] - height/2)}", "0 0 0"],
                    axis_data=["0 0 1"],
                    limits=["100",
                            "100",
                            str(z_axis_link_position[2] - height/2),
                            str(z_axis_link_position[2] + height/2)])

    width = 4
    x_axis_link_position = [0, 0, 0]
    x_axis_link_position[0] = z_axis_link_position[0] + width/2
    x_axis_link_position[1] = z_axis_link_position[1]
    x_axis_link_position[2] = z_axis_link_position[2]

    # X-Axis
    configure_link(robot, "x_axis_link", origin_data=[convert_to_str(x_axis_link_position), "0 0 0"],
                                        geometry_shape="box",
                                        geometry_data=[f"{width} 0.2 0.2"],
                                        mass_value="1")

    # Joint: X-Axis -> Y-Axis
    joint_link_position = [0, 0, 0]
    joint_link_position[0] = z_axis_link_position[0] - width/2
    joint_link_position[1] = z_axis_link_position[1]
    joint_link_position[2] = z_axis_link_position[2]
    configure_joint(robot, "x_axis_link_prismatic_joint", "prismatic", "x_axis_link", "y_axis_link",
                    origin_data=[str(joint_link_position), "0 0 0"], axis_data=["1 0 0"],
                    limits=["100",
                            "100",
                            str(z_axis_link_position[0]),
                            str(z_axis_link_position[0] + width)])

    # Y-Axis
    width = 4
    y_axis_link_position = [0, 0, 0]
    y_axis_link_position[0] = x_axis_link_position[0] - width / 2
    y_axis_link_position[1] = x_axis_link_position[1] + width / 2
    y_axis_link_position[2] = x_axis_link_position[2] - 1

    configure_link(robot, "y_axis_link", origin_data=[convert_to_str(y_axis_link_position), "0 0 0"],
                   geometry_shape="box",
                   geometry_data=[f"0.2 {width} 0.2"],
                   mass_value="1")

    # Joint: Y-Axis -> Base Gripper
    joint_link_position = [0, 0, 0]
    joint_link_position[0] = y_axis_link_position[0]
    joint_link_position[1] = y_axis_link_position[1]
    joint_link_position[2] = y_axis_link_position[2]
    configure_joint(robot, "y_axis_link_prismatic_joint", "prismatic", "y_axis_link", "base_gripper",
                    origin_data=[str(joint_link_position), "0 0 0"], axis_data=["0 1 0"],
                    limits=["100",
                            "100",
                            f"{-width/2}",
                            f"{width/2}"])

    # Base Gripper
    base_gripper_link_position = [0, 0, 0]
    base_gripper_link_position[0] = y_axis_link_position[0]
    base_gripper_link_position[1] = y_axis_link_position[1] - width/2
    base_gripper_link_position[2] = y_axis_link_position[2] - 0.2

    configure_link(robot, "base_gripper", origin_data=[convert_to_str(base_gripper_link_position), "0 0 0"],
                   geometry_shape="box",
                   geometry_data=[f"1 1 0.1"],
                   mass_value="1")

    # Joint: Base gripper -> Hand Gripper
    configure_joint(robot, "base_gripper_revolution_joint", "continuous", "base_gripper", "hand_gripper",
                    origin_data=[convert_to_str(base_gripper_link_position), "0 0 0"], axis_data=["0 0 1"],
                    limits=["100",
                            "100",
                            "-1.5708",
                            "1.5708"])

    # Gripper: hand
    hand_gripper_link_position = [0, 0, 0]
    hand_gripper_link_position[0] = base_gripper_link_position[0]
    hand_gripper_link_position[1] = base_gripper_link_position[1]
    hand_gripper_link_position[2] = base_gripper_link_position[2] - 0.1

    configure_link(robot, "hand_gripper",
                   origin_data=[convert_to_str(hand_gripper_link_position), "0 0 0"],
                   geometry_shape="box",
                   geometry_data=[f"2 1 0.1"],
                   mass_value="1")

    # Joint: Hand gripper -> Right Finger
    configure_joint(robot, "hand_gripper_right_finger_joint", "prismatic", "hand_gripper", "right_finger",
                    origin_data=[convert_to_str(base_gripper_link_position), "0 0 0"], axis_data=["1 0 0"],
                    limits=["100",
                            "100",
                            "-1",
                            "0"])

    # Gripper: Right Finger
    right_finger_gripper_link_position = [0, 0, 0]
    right_finger_gripper_link_position[0] = hand_gripper_link_position[0] + 1
    right_finger_gripper_link_position[1] = hand_gripper_link_position[1]
    right_finger_gripper_link_position[2] = hand_gripper_link_position[2] - 0.35

    configure_link(robot, "right_finger",
                   origin_data=[convert_to_str(right_finger_gripper_link_position), "0 0 0"],
                   geometry_shape="box",
                   geometry_data=[f"0.1 1 1"],
                   mass_value="1")

    # Joint: Hand gripper -> Left Finger
    configure_joint(robot, "hand_gripper_left_finger_joint", "prismatic", "hand_gripper", "left_finger",
                    origin_data=[convert_to_str(base_gripper_link_position), "0 0 0"], axis_data=["1 0 0"],
                    limits=["100",
                            "100",
                            "0",
                            "1"])

    # Gripper: Right Finger
    left_finger_gripper_link_position = [0, 0, 0]
    left_finger_gripper_link_position[0] = hand_gripper_link_position[0] - 1
    left_finger_gripper_link_position[1] = hand_gripper_link_position[1]
    left_finger_gripper_link_position[2] = hand_gripper_link_position[2] - 0.35

    configure_link(robot, "left_finger",
                   origin_data=[convert_to_str(left_finger_gripper_link_position), "0 0 0"],
                   geometry_shape="box",
                   geometry_data=[f"0.1 1 1"],
                   mass_value="1")

    tree = ET.ElementTree(robot)
    ET.indent(tree, '  ')

    file_to_create = "cartesian.urdf"
    tree.write(file_to_create)
    print("saved ", file_to_create)
