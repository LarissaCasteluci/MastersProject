#!/usr/bin/env python3

# KUKA API for ROS

# Marhc 2016 Saeid Mokaram  saeid.mokaram@gmail.com
# Sheffield Robotics    http://www.sheffieldrobotics.ac.uk/
# The university of sheffield   http://www.sheffield.ac.uk/

# This script generats a ROS node for comunicating with KUKA iiwa
# Dependencies: conf.txt, ROS server, Rospy, KUKA iiwa java SDK, KUKA iiwa robot.

#######################################################################################################################
from kuka_ros_node import *
import scipy.spatial.distance as Dist

def MaxT1Speed(kuka_ros_node):
    kuka_ros_node.send_command('setJointAcceleration 1.0')
    kuka_ros_node.send_command('setJointVelocity 1.0')
    kuka_ros_node.send_command('setJointJerk 1.0')
    kuka_ros_node.send_command('setCartVelocity 1000')

def MaxT2Speed(kuka_ros_node):
    kuka_ros_node.send_command('setJointAcceleration 0.3')
    kuka_ros_node.send_command('setJointVelocity 1.0')
    kuka_ros_node.send_command('setJointJerk 0.1')
    kuka_ros_node.send_command('setCartVelocity 1000')

if __name__ == '__main__':
    kuka_ros_node = kuka_iiwa_ros_node()  # Making a connection object.
    while (not kuka_ros_node.isReady):
        pass  # Wait until iiwa is connected zzz!

    if kuka_ros_node.OperationMode[0] == 'T1':
        print('Hello Sheffield Robotics!')
        MaxT1Speed(kuka_ros_node)
    elif kuka_ros_node.OperationMode[0] == 'T2':
        MaxT2Speed(kuka_ros_node)
    else:
        print('The robot is in', kuka_ros_node.OperationMode[0], 'mode.')
        print('This demo is safe to work at T1 or T2 modes only.')
        exit()

    print('Started')

    # Initializing Tool 1
    kuka_ros_node.send_command('setTool tool1')

    # Initializing (max speed)



    # Move close to a start position.
    kuka_ros_node.send_command('setPosition 0 0 0 0 0 0 0')
    kuka_ros_node.send_command('setPosition 0 49.43 0 -48.5 0 82.08 0')
    while Dist.euclidean(kuka_ros_node.JointPosition[0], [0, 49.43, 0, -48.5, 0, 82.08, 0]) > 5: pass

    # Move to the exact start position.
    kuka_ros_node.send_command('setPositionXYZABC 700 0 300 -180 0 -180 ptp')  # ptp motions move with setJointAcceleration


    #################################################
    # Motion in YZ plain.

    # Performing an arch motion from [700, 0, 400] to [700, 0, 200] passing trough [700, 100, 300].
    kuka_ros_node.send_command('MoveCirc 700 100 200 -180 0 -180 700 0 100 -180 0 -180 0.1')  # MoveCirc motion move with CartVelocity

    # Performing a reverce arch motion from [700, 0, 200] to [700, 0, 400] passing trough [700, -100, 300].
    # my_client.send_command('setCartVelocity 100') # Performing same motion slower (CartVelocity 100mm/s')
    kuka_ros_node.send_command('MoveCirc 700 -100 200 -180 0 -180 700 0 300 -180 0 -180 0.1')  # MoveCirc motion move with CartVelocity

    #################################################
    # Motion in XY plain.

    # Performing an arch motion from [700, 0, 400] to [500, 0, 400] passing trough [600, 100, 400].

    kuka_ros_node.send_command('MoveCirc 600 100 300 -180 0 -180 500 0 300 -180 0 -180 0.1') # MoveCirc motion move with CartVelocity

    # Performing a reverce arch motion from [500, 0, 400] to [700, 0, 400] passing trough [600, -100, 400].
    # my_client.send_command('setCartVelocity 100') # Performing same motion slower (CartVelocity 100mm/s')
    kuka_ros_node.send_command('MoveCirc 600 -100 300 -180 0 -180 700 0 300 -180 0 -180 0.1') # MoveCirc motion move with CartVelocity


    #################################################
    # Motion in XYZ plain.

    # Performing an arch motion from [700, 0, 400] to [500, 0, 200] passing trough [600, 100, 300].

    kuka_ros_node.send_command(
        'MoveCirc 600 100 200 -180 0 -180 500 0 100 -180 0 -180 0.1')  # MoveCirc motion move with CartVelocity

    # Performing a reverce arch motion from [500, 0, 200] to [700, 0, 400] passing trough [600, -100, 300].
    # my_client.send_command('setCartVelocity 100') # Performing same motion slower (CartVelocity 100mm/s')
    kuka_ros_node.send_command(
        'MoveCirc 600 -100 200 -180 0 -180 700 0 300 -180 0 -180 0.1')  # MoveCirc motion move with CartVelocity
