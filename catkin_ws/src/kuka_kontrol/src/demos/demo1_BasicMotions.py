#!/usr/bin/env python3

# KUKA API for ROS

# Marhc 2016 Saeid Mokaram  saeid.mokaram@gmail.com
# Sheffield Robotics    http://www.sheffieldrobotics.ac.uk/
# The university of sheffield   http://www.sheffield.ac.uk/

# This script generats a ROS node for comunicating with KUKA iiwa
# Dependencies: conf.txt, ROS server, Rospy, KUKA iiwa java SDK, KUKA iiwa robot.

# This application is intended for floor mounted robots.
#######################################################################################################################
from kuka_ros_node import *

# Making a connection object.
kuka_ros_node = kuka_iiwa_ros_node()

# Wait until iiwa is connected zzz!
while (not kuka_ros_node.isready): pass
print('Started!')

# Initializing Tool 1
kuka_ros_node.send_command('setTool tool1')

# Initializing
kuka_ros_node.send_command('setJointAcceleration 1.0')  # If the JointAcceleration is not set, the defult value is 1.0.
kuka_ros_node.send_command('setJointVelocity 1.0')      # If the JointVelocity is not set, the defult value is 1.0.
kuka_ros_node.send_command('setJointJerk 1.0')          # If the JointJerk is not set, the defult value is 1.0.
kuka_ros_node.send_command('setCartVelocity 10000')     # If the CartVelocity is not set, the defult value is 100


# Move close to a start position.
kuka_ros_node.send_command('setPosition 0 49.43 0 -48.5 0 82.08 0')


# Move to the exact start position.
kuka_ros_node.send_command('setPositionXYZABC 700 0 300 -180 0 -180 ptp')  # ptp motions move with setJointAcceleration


# Performing three lin motions with max posible speed.
kuka_ros_node.send_command('setPositionXYZABC 500 100 400 - - - lin')  # lin motions move with CartVelocity
kuka_ros_node.send_command('setPositionXYZABC - -100 350 - - - lin')
kuka_ros_node.send_command('setPositionXYZABC 700 0 300 - - - lin')


# Performing same motion slower (CartVelocity 50mm/s')
kuka_ros_node.send_command('setCartVelocity 50')  # This only controls the lin motions.

kuka_ros_node.send_command('setPositionXYZABC 500 100 400 - - - lin')  # lin motions move with CartVelocity
kuka_ros_node.send_command('setPositionXYZABC - -100 350 - - - lin')
kuka_ros_node.send_command('setPositionXYZABC 700 0 300 - - - lin')
