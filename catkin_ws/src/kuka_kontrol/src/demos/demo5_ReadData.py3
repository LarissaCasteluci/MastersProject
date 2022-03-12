#!/usr/bin/env python3

# KUKA API for ROS
version = 'V15032017'

# Marhc 2016 Saeid Mokaram  saeid.mokaram@gmail.com
# Sheffield Robotics    http://www.sheffieldrobotics.ac.uk/
# The university of sheffield   http://www.sheffield.ac.uk/

# This script generats a ROS node for comunicating with KUKA iiwa
# Dependencies: conf.txt, ROS server, Rospy, KUKA iiwa java SDK, KUKA iiwa robot.

# This application is intended for floor mounted robots.
#######################################################################################################################
from kuka_ros_node import *
import time, os


# Making a connection object.
kuka_ros_node = kuka_iiwa_ros_node()

while (not kuka_ros_node.isReady):
    pass  # Wait until iiwa is connected zzz!

# Initializing Tool 1

print("Inicializando a ferramenta tool1")
kuka_ros_node.send_command('setTool tool1')

for i in range(1000):
    os.system('clear')
    print(cl_pink('\n=========================================='))
    print(cl_pink('<   <  < << SHEFFIELD ROBOTICS >> >  >   >'))
    print(cl_pink('=========================================='))
    print(cl_pink(' Read KUKA data demo'))
    print(cl_pink(' Version: ' + version))
    print(cl_pink('==========================================\n'))

    print('#####################################')
    print('OperationMode\t=', kuka_ros_node.OperationMode)  # True when a collision has accured.
    print('isCollision\t=', kuka_ros_node.isCollision)        # True when a collision has accured.
    print('isCompliance\t=', kuka_ros_node.isCompliance)      # True when robot is in Compliance mode.
    print('isMastered\t=', kuka_ros_node.isMastered)
    print('isready\t=', kuka_ros_node.isReady)                # True when robot is connected
    print('isReadyToMove\t=', kuka_ros_node.isReadyToMove)    # True when robot can move, e.g. when the safety key is pressed...
    print('isFinished\t=', kuka_ros_node.isFinished)    # Guess what

    print('ToolPosition\t=', kuka_ros_node.ToolPosition)      # Reading Tool cartesian position
    print('ToolForce\t=', kuka_ros_node.ToolForce)            # Reading Tool cartesian force
    print('ToolTorque\t=', kuka_ros_node.ToolTorque)          # Reading Tool cartesian torque

    print('JointAcceleration\t=', kuka_ros_node.JointAcceleration)    # Current joint acceleration
    print('JointJerk\t=', kuka_ros_node.JointJerk)                    # Current joint jerk
    print('JointPosition\t=', kuka_ros_node.JointPosition)            # Reading joints position
    print('JointVelocity\t=', kuka_ros_node.JointVelocity)            # Reading joints velocity
    print('#####################################')
    time.sleep(1)
