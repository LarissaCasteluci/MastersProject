# https://pybullet.org/Bullet/phpBB3/viewtopic.php?p=42686

import kubric as kb
import numpy as np
from kubric.renderer.blender import Blender as KubricRenderer
from dataset_generation_tools.simulators.pybullet_simulator import PyBullet as KubricSimulator
from typing import List, Tuple
import shutil
import os


class ArtificialDatasetGeneration:
    """ Dataset for generating the artificial data"""
    scene: kb.Scene
    renderer: KubricRenderer
    simulator: KubricSimulator
    grasping_obj: kb.FileBasedObject
    rng: np.array
    velocity: np.array
    walls: List[kb.Cube]
    grasping_object_pos: List[float]
    grasping_object_quat: List[float]


    def __init__(self,
                 output_dir: str,
                 resolution: Tuple[int, int] = (256, 256),
                 frame_end: int = 20,
                 frame_rate: int = 1,
                 step_rate: int = 240):

        # Scene framerate and length
        self.scene = kb.Scene(resolution=resolution)
        self.scene.frame_end = frame_end  # < numbers of frames to render
        self.scene.frame_rate = frame_rate  # < rendering framerate
        self.scene.step_rate = step_rate  # < simulation total steps

        self.rng = np.random.default_rng()
        self.velocity = self.rng.uniform([-1, -1, 0], [1, 1, 0])

        self.path_name = f"/1DatasetGeneration/outputs/{output_dir}"
        if os.path.isdir(self.path_name):
            shutil.rmtree(self.path_name)

        self.walls = []

        self.grasping_object_pos = [0, 0, 1]
        self.grasping_object_quat = [0, 0, 0, 0]

    def config_scene(self):
        self.scene += kb.Cube(name="floor", scale=(10, 10, 0.1),
                         position=(0, 0, -0.3), material=kb.FlatMaterial(),
                         static=True)

        self.scene += kb.DirectionalLight(name="sun", position=(-1, -0.5, 3),
                                     look_at=(0, 0, 0), intensity=1.5)


        self.scene += kb.PerspectiveCamera(name="camera",
                                           position=(0, 0, 20),
                                           look_at=(0, 0, 1))

        self.walls.append(kb.Cube(name="wall1", scale=(0.1, 7, 1),
                         position=(7, 0, 0.5), material=kb.FlatMaterial(),
                         static=True))

        self.walls.append(kb.Cube(name="wall2", scale=(0.1, 7, 1),
                         position=(-7, 0, 0.5), material=kb.FlatMaterial(),
                         static=True))

        self.walls.append(kb.Cube(name="wall3", scale=(7, 0.1, 1),
                         position=(0, 7, 0.5), material=kb.FlatMaterial(),
                         static=True))

        self.walls.append(kb.Cube(name="wall4", scale=(7, 0.1, 1),
                         position=(0, -7, 0.5), material=kb.FlatMaterial(),
                         static=True))

    def add_walls(self):
        for wall in self.walls:
            self.scene += wall

    def remove_walls(self):
        for wall in self.walls:
            self.scene.remove(wall)

    def add_grasping_object(self, asset_name: str):
        scale = 5
        obj = kb.FileBasedObject(
          asset_id=asset_name,
          render_filename=f"/1DatasetGeneration/assets/grasp_objects/{asset_name}_visual.obj",
          bounds=((-1, -1, 0), (1, 1, 1)),
          #position=tuple(self.grasping_object_pos),
          position=(0, 0, 1),
          #quaternion=self.grasping_object_quat,
          simulation_filename=f"/1DatasetGeneration/assets/grasp_objects/{asset_name}_docker.urdf",
          scale=(scale, scale, scale),
          material=kb.PrincipledBSDFMaterial(color=kb.random_hue_color()),
          velocity=self.velocity)

        self.scene += obj
        self.grasping_obj = obj

        print("visual:", os.path.isfile(f"/1DatasetGeneration/assets/grasp_objects/{asset_name}_visual.obj"))
        print("visual:", os.path.isfile(f"/1DatasetGeneration/assets/grasp_objects/{asset_name}.urdf"))

    def remove_grasping_object(self):
        self.scene.remove(self.grasping_obj)

    def call_renderer(self):

        # Remove output folder to make sure the data generated is new
        if os.path.isdir(self.path_name):
            shutil.rmtree(self.path_name)

        self.add_walls()

        self.renderer = KubricRenderer(self.scene)
        self.simulator = KubricSimulator(self.scene)

        spawn_region = [[-2, -2, 5], [2, 2, 10]]

        #kb.move_until_no_overlap(self.grasping_obj, self.simulator, spawn_region=spawn_region)
        self.simulator.run()

        #self.renderer.save_state(self.path_name + "helloworld1.blend")
        frame = self.renderer.render()
        kb.write_image_dict(frame, self.path_name)
        self.remove_walls()

    def grasp_proposal_simulation(self):
        pass
