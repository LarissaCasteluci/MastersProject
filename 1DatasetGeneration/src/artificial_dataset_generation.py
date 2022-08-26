# https://pybullet.org/Bullet/phpBB3/viewtopic.php?p=42686

import logging
import kubric as kb
import numpy as np
from kubric.renderer.blender import Blender as KubricRenderer
from kubric.simulator.pybullet import PyBullet as KubricSimulator
from pathlib import Path
from typing import List


class ArtificialDatasetGeneration:
    """ Dataset for generating the artificial data"""
    scene: kb.Scene
    grasping_obj: kb.FileBasedObject
    rng: np.array
    velocity: np.array
    walls: List[kb.Cube]
    renderer: KubricRenderer
    simulator: KubricSimulator

    def __init__(self):
        # Scene framerate and length
        self.scene = kb.Scene(resolution=(256, 256))
        self.scene.frame_end = 20  # < numbers of frames to render
        self.scene.frame_rate = 1  # < rendering framerate
        self.scene.step_rate = 240  # < simulation total steps

        self.rng = np.random.default_rng()
        self.velocity = self.rng.uniform([-1, -1, 0], [1, 1, 0])

        self.path_name = "/1DatasetGeneration/output_pipeline/"



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

    def add_objects(self, asset_name: str):
        scale = 1  # scale = 0.04
        obj = kb.FileBasedObject(
          asset_id=asset_name,
          render_filename=f"/1DatasetGeneration/assets/{asset_name}.obj",
          bounds=((-1, -1, 0), (1, 1, 1)),
          position=(0, 0, 1), # position=(0, 0, 0.2),
          simulation_filename=f"/1DatasetGeneration/assets/{asset_name}.urdf",
          scale=(scale, scale, scale),
          material=kb.PrincipledBSDFMaterial(color=kb.random_hue_color()),
          velocity=self.velocity)

        self.scene += obj
        self.grasping_obj = obj

    def remove_objects(self):
        self.scene.remove(self.grasping_obj)

    def call_renderer(self):
        self.add_walls()

        self.renderer = KubricRenderer(self.scene)
        self.simulator = KubricSimulator(self.scene)

        spawn_region = [[-2, -2, 5], [2, 2, 10]]

        #self.renderer.save_state(self.path_name + "helloworld0.blend")
        kb.move_until_no_overlap(self.grasping_obj, self.simulator, spawn_region=spawn_region)
        self.simulator.run()

        # --- render (and save the blender file)
        self.renderer.save_state(self.path_name + "helloworld1.blend")
        frame = self.renderer.render()
        kb.write_image_dict(frame, self.path_name)
        self.remove_walls()

    def grasp_proposal_simulation(self):
        pass