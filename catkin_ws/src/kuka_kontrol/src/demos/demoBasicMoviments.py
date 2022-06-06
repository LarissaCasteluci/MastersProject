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
while (not kuka_ros_node.isReady): pass
print('Started!')

# Initializing Tool 1
kuka_ros_node.send_command('setTool tool1')

# Initializing
kuka_ros_node.send_command('setJointAcceleration 1.0')  # If the JointAcceleration is not set, the defult value is 1.0.
kuka_ros_node.send_command('setJointVelocity 0.1')      # If the JointVelocity is not set, the defult value is 1.0.
kuka_ros_node.send_command('setJointJerk 1.0')          # If the JointJerk is not set, the defult value is 1.0.
kuka_ros_node.send_command('setCartVelocity 10000')     # If the CartVelocity is not set, the defult value is 100


## Set to start Position
kuka_ros_node.send_command('setPositionXYZABC 366 321 -319 0 0 0 ptp')  # ptp motions move with setJointAcceleration

# # Performing same motion slower (CartVelocity 100mm/s')
kuka_ros_node.send_command('setCartVelocity 100')  # This only controls the lin motions.
kuka_ros_node.send_command('setPositionXYZABC 366 321 -44 0 0 0 lin')  # lin motions move with CartVelocity


kuka_ros_node.send_command('setPositionXYZABC 641 170 -319 0 0 0 ptp')  # ptp motions move with setJointAcceleration
