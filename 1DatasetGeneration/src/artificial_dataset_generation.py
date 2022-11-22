# https://pybullet.org/Bullet/phpBB3/viewtopic.php?p=42686

import kubric as kb
import numpy as np
from kubric.renderer.blender import Blender as KubricRenderer
from dataset_generation_tools.simulators.pybullet_simulator import PyBullet as KubricSimulator
from dataset_generation_tools.base_data_structures.basic_types import *
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
                 output_dir: str):

        self.rng = np.random.default_rng()
        self.velocity = self.rng.uniform([-1, -1, 0], [1, 1, 0])

        self.path_name = output_dir
        if os.path.isdir(self.path_name):
            shutil.rmtree(self.path_name)

        self.walls = []

        self.grasping_object_pos = [2, 2, 1]
        self.grasping_object_quat = [0, 0, 0, 0]

        self.camera_1 = kb.PerspectiveCamera(name="camera_1",
                                             position=(2, 2, 7),
                                             look_at=(2, 2, 1))

        self.camera_2 = kb.PerspectiveCamera(name="camera_2",
                                             position=(2.05, 2, 7),
                                             look_at=(2.05, 2, 1))


    def configure_new_scene(self, resolution: Tuple[int, int] = (256, 256),
                            frame_end: int = 20,
                            frame_rate: int = 1,
                            step_rate: int = 240):

        self.scene = kb.Scene(resolution=resolution)
        # Scene framerate and length
        self.scene.frame_end = frame_end  # < numbers of frames to render
        self.scene.frame_rate = frame_rate  # < rendering framerate
        self.scene.step_rate = step_rate  # < simulation total steps

        self.renderer = KubricRenderer(self.scene)
        self.simulator = KubricSimulator(self.scene)


    def calculate_new_pos_and_quat(self):
        self.grasping_object_pos = [3.5 - 3*self.rng.random(),
                                    3.5 - 3*self.rng.random(),
                                    2]

        self.grasping_object_quat = [self.rng.random(),
                                     self.rng.random(),
                                     self.rng.random(),
                                     self.rng.random()]

    def save_obj_pos_and_quat(self):
        self.grasping_object_pos = self.grasping_obj.position
        self.grasping_object_quat = self.grasping_obj.quaternion

    def config_scene(self):
        self.scene += kb.Cube(name="floor", scale=(20, 20, 0.1),
                              position=(0, 0, -0.3), material=kb.FlatMaterial(),
                              static=True)

        self.scene += kb.DirectionalLight(name="sun", position=(2, 2, 7),
                                     look_at=(2, 2, 0), intensity=1.5)


        self.scene += self.camera_1


        self.scene += kb.Cube(name="1", scale=(0.1, 0.1, 0.1), position=(0, 0, 1.5), static=True)
        self.scene += kb.Cube(name="2", scale=(0.1, 0.1, 0.1), position=(4, 0, 1.5), static=True)
        self.scene += kb.Cube(name="3", scale=(0.1, 0.1, 0.1), position=(0, 4, 1.5), static=True)
        self.scene += kb.Cube(name="4", scale=(0.1, 0.1, 0.1), position=(4, 4, 1.5), static=True)


        self.walls.append(kb.Cube(name="wall1", scale=(0.05, 2, 1),
                                  position=(4, 2, 0.5), material=kb.FlatMaterial(),
                                  static=True))

        self.walls.append(kb.Cube(name="wall2", scale=(0.05, 2, 1),
                                  position=(0, 2, 0.5), material=kb.FlatMaterial(),
                                  static=True))

        self.walls.append(kb.Cube(name="wall3", scale=(2, 0.01, 1),
                                  position=(2, 0, 0.5), material=kb.FlatMaterial(),
                                  static=True))

        self.walls.append(kb.Cube(name="wall4", scale=(2, 0.01, 1),
                                  position=(2, 4, 0.5), material=kb.FlatMaterial(),
                                  static=True))

    def add_walls(self):
        for wall in self.walls:
            self.scene += wall

    def remove_walls(self):
        for wall in self.walls:
            self.scene.remove(wall)

    def add_grasping_object(self, asset_name: str):
        scale = 1
        obj = kb.FileBasedObject(
          asset_id=asset_name,
          render_filename=f"/1DatasetGeneration/assets/grasp_objects/{asset_name}_visual.obj",
          position=self.grasping_object_pos,
          quaternion=self.grasping_object_quat,
          simulation_filename=f"/1DatasetGeneration/assets/grasp_objects/{asset_name}_docker.urdf",
          scale=(scale, scale, scale),
          material=kb.PrincipledBSDFMaterial(color=kb.random_hue_color(), specular=0),
          velocity=self.velocity)

        self.scene += obj
        self.grasping_obj = obj


    def remove_grasping_object(self):
        self.scene.remove(self.grasping_obj)


    def move_until_no_overlap(self):
        self.add_walls()

        spawn_region = [[0, 0, 0], [4, 4, 2.5]]

        kb.move_until_no_overlap(self.grasping_obj, self.simulator, spawn_region=spawn_region)
        self.simulator.run()
        #self.remove_walls()

    def call_renderer(self, camera):

        path_name = self.path_name + camera

        # Remove output folder to make sure the data generated is new
        if os.path.isdir(path_name):
            shutil.rmtree(path_name)

        #frame = self.renderer.render(return_layers=("rgba", "depth", "segmentation"))
        frame = self.renderer.render()
        kb.write_image_dict(frame, path_name)

        self.renderer.save_state(path_name + "/test.blend")

    def grasp_proposal_simulation(self,
                                  obj_name: str,
                                  grasp_in_world_coordinates: BasicGraspInWorldCoordinates):

        self.simulator.run_grasp_simulation(obj_name,
                                            grasp_in_world_coordinates,
                                            self.grasping_object_pos,
                                            self.grasping_object_quat)

