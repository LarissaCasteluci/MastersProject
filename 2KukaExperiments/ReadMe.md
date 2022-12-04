# Kuka Experiments


Jacquard:
x;y;theta in degrees;opening;jaws size. 
583.90408; 479.20119; -66.2885; 135.0; 26.1855
y is toward the bottom of the image (and therefore the angle is horizontally mirrored). 
When the position is the same on multiple consecutive rows, 
the first one corresponds to the grasp with the 
default jaws size of 2 cm and the followings are just 
repetition of this grasp with different sizes.

Cornell:
253 319.7

- Segurança
- Aumentar o box da mesa

Train GG-CNNN Jacquard
``` bash
python3 train_ggcnn.py --network ggcnn2 --dataset jacquard --dataset-path /home/larissa/DATASETS/Jacquard \
--use-depth 1 --use_rgb 1  --epochs 100 --outdir training_network/models \
--logdir training_network/log \
--description default_jacquard
``` 



## Configure experiments with Kuka IIWA
1. Deactivate conda
2. Start running: "roscore"
3. "cd MastersProject/catkin_ws"
4. "catkin_make" -> build project
5. "cd catkin_ws"; "source devel/setup.zsh" -> find references to project
6. "rosrun kuka_kontrol server_V30032017.py3" 
7. "rosrun kuka_kontrol demo5_ReadData.py3"

SSH garra 172.31.1.171 porta 5500


## See robot configuration
- ROBOT_IP:6675

## TCP for tests
(x:0, y:0, z: 110 ):

## Procedures
1. [Calibration](#Calibration)
2. [Tests Procedures](#Tests Procedures)

## Calibration
- [ ] Find TCP ( Tool's TCP )
- [x] Calculate $\delta$ TCP and $\delta$ Camera
- [ ] Camera starts at 30 cm ( Save point as P0)
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



- Cartesian workspace monitoring
- Cartesian protected space monitoring
- Collision detection
- 9.3.9 - Safety oriented Tools
- (>>> 9.3.9.2 "Tool properties – Load data tab" Page 156)
- Fig. 9-7: Safety-oriented gripper
- (>>> 13.10.9 "Monitoring spaces" Page 248)
(>>> 13.10.13.2 "Collision detection" Page 261)


