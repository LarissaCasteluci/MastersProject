# Kubric Dataset Generation

Original Paper: 
Github: https://github.com/google-research/kubric

The Dataset Generation was made by using the Kubric.

Command for using kubric in this path, from the root of the project:

``` bash
cd /home/larissa/MastersProject
docker run --rm --interactive \
           --user $(id -u):$(id -g) \
           --volume "$(pwd)/original_repos/kubric:/kubric" \
           --volume "$(pwd)/1DatasetGeneration:/1DatasetGeneration" \
           kubricdockerhub/kubruntu \
           /usr/bin/python3 /1DatasetGeneration/src/main.py
```

Step by step in Development:
- [X] Try to load models to kubrik
- [X] Try to load textures
- [X] Configure Camera
- [X] Load Object and Table
- [X] Simulate Object until it is on a stable pose
- [X] Load Texture
- [X] Render Images
- [ ] Create Random Grasps Proposals ( Truly Random?)
- For grasp in grasp_proposals:
- [ ] Simulate grasp 1: Load Gripper Object
- [ ] Simulate Grasp 2: Try to Perform grasp
- [ ] Simulate Grasp 3: Elevate the Object
Until all grasp_proposals have been evaluated. 


## References
- [How to Run RViz](https://admantium.medium.com/robot-operating-system-how-to-start-the-robot-simulation-tool-rviz-540179e92b6b)
- [Ros Tutorial](http://wiki.ros.org/urdf/Tutorials/Building%20a%20Visual%20Robot%20Model%20with%20URDF%20from%20Scratch)

``` bash
roslaunch urdf_tutorial display.launch model:=/home/larissa/MastersProject/1DatasetGeneration/assets/gripper.urdf

```
