# Kuka Experiments

TODO
- Adicionar kill applicação iiwa

## Configure experiments with Kuka IIWA
1. Deactivate conda
2. Start running: "roscore"
3. "cd MasterProject/catkin_ws"
4. "cd catkin_ws"; "catkin_make" -> build project
5. "cd catkin_ws"; "source devel/setup.zsh" -> find references to project
6. "rosrun kuka_kontrol server_V30032017.py" 
7. "rosrun kuka_kontrol demo5_ReadData.py"


## See robot configuration
- ROBOT_IP:6675

## TCP for tests
(x:0, y:0, z: 110 )

## Procedures
1. [Calibration](#Calibration)
2. [Tests Procedures](#Tests Procedures)

## Calibration
- [ ] Find TCP ( Tool's TCP )
- [ ] Calculate $\delta$ TCP and $\delta$ Camera
- [ ] Camera starts at 40 cm ( Save point as P0)
- [ ] Define point of dropout (Save Point as PD)
- [ ] Save The Two Points in the project

## Tests Procedures
- [ ] Start at P0
- [ ] Capture Image Data
- [ ] Run Image thru Neural Network
- [ ] Get Best Grasp
- [ ] Calculate Inverse Kinematics 
- [ ] Perform Grasping ( Gripper decides how much it should close)
- [ ] Elevate Object
- [ ] Move object to Point Pd and Drop it
