#!/usr/bin/env python3

# KUKA API for ROS

# Marhc 2016 Saeid Mokaram  saeid.mokaram@gmail.com
# Sheffield Robotics    http://www.sheffieldrobotics.ac.uk/
# The university of sheffield   http://www.sheffield.ac.uk/

# This script generats a ROS node for comunicating with KUKA iiwa
# Dependencies: conf.txt, ROS server, Rospy, KUKA iiwa java SDK, KUKA iiwa robot.

#######################################################################################################################
from kuka_ros_node import *

if __name__ == '__main__':
    kuka_ros_node = kuka_iiwa_ros_node()  # Making a connection object.
    while (not kuka_ros_node.isReady):
        pass  # Wait until iiwa is connected zzz!
    print('Started')

    # Initializing Tool 1
    kuka_ros_node.send_command('setTool tool1')

    # Initializing
    kuka_ros_node.send_command('setJointAcceleration 1.0')
    kuka_ros_node.send_command('setJointVelocity 1.0')
    kuka_ros_node.send_command('setJointJerk 1.0')
    kuka_ros_node.send_command('setCartVelocity 10000')


    # Move close to a start position.
    kuka_ros_node.send_command('setPosition 0 49.43 0 -48.5 0 82.08 0')


    # Move to the exact start position.
    kuka_ros_node.send_command('setPositionXYZABC 700 0 300 -180 0 -180 ptp')  # ptp motions move with setJointAcceleration


    # Robot is compliant in XY plain.
    print('Robot is compliant in XY plain.')
    kuka_ros_node.send_command('setCompliance 10 10 5000 300 300 300')
    kuka_ros_node.send_command('sleep 10')  # Sleep 10s

    # Robot is compliant in YZ plain.
    print('Robot is compliant in YZ plain.')
    kuka_ros_node.send_command('setCompliance 5000 10 10 300 300 300')
    kuka_ros_node.send_command('sleep 10')  # Sleep 10s

    # Robot is compliant in rotation only.
    print('Robot is compliant in rotation only.')
    kuka_ros_node.send_command('setCompliance 5000 5000 5000 10 10 10')
    kuka_ros_node.send_command('sleep 10')  # Sleep 10s

    # Compliance OFF
    kuka_ros_node.send_command('resetCompliance')
