# Kuka Experiments

- Segurança
- Aumentar o box da mesa


TODO
- Adicionar kill applicação iiwa

## Configure experiments with Kuka IIWA
1. Deactivate conda
2. Start running: "roscore"
3. "cd MasterProject/catkin_ws"
4. "catkin_make" -> build project
5. "cd catkin_ws"; "source devel/setup.zsh" -> find references to project
6. "rosrun kuka_kontrol server_V30032017.py3" 
7. "rosrun kuka_kontrol demo5_ReadData.py3"


## See robot configuration
- ROBOT_IP:6675

## TCP for tests
(x:0, y:0, z: 110 ):

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



- Cartesian workspace monitoring
- Cartesian protected space monitoring
- Collision detection
- 9.3.9 - Safety oriented Tools
- (>>> 9.3.9.2 "Tool properties – Load data tab" Page 156)
- Fig. 9-7: Safety-oriented gripper
- (>>> 13.10.9 "Monitoring spaces" Page 248)
(>>> 13.10.13.2 "Collision detection" Page 261)

 >>> torch.cuda.get_device_name(0)
/home/larissa/MastersProject/2KukaExperiments/ros-venv/lib/python3.7/site-packages/torch/cuda/__init__.py:145: UserWarning: 
NVIDIA GeForce RTX 3050 Laptop GPU with CUDA capability sm_86 is not compatible with the current PyTorch installation.
The current PyTorch install supports CUDA capabilities sm_37 sm_50 sm_60 sm_70.
If you want to use the NVIDIA GeForce RTX 3050 Laptop GPU GPU with PyTorch, please check the instructions at https://pytorch.org/get-started/locally/

  warnings.warn(incompatible_device_warn.format(device_name, capability, " ".join(arch_list), device_name))
'NVIDIA GeForce RTX 3050 Laptop GPU'

