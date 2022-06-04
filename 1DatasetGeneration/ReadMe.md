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
           /usr/bin/python3 /1DatasetGeneration/kubric_hello_world.py
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

