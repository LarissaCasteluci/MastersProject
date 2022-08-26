# https://pybullet.org/Bullet/phpBB3/viewtopic.php?p=42686

import logging
import kubric as kb
import numpy as np
from kubric.renderer.blender import Blender as KubricRenderer
from kubric.simulator.pybullet import PyBullet as KubricSimulator
from pathlib import Path


class ArtificialDatasetGeneration:
    """ Dataset for generating the artificial data"""
    scene: kb.Scene
    control_obj: kb.FileBasedObject

    def __init__(self):
        # Scene framerate and length
        self.scene = kb.Scene(resolution=(256, 256))
        self.scene.frame_end = 20  # < numbers of frames to render
        self.scene.frame_rate = 1  # < rendering framerate
        self.scene.step_rate = 240  # < simulation total steps


    def config_scene(self):
        self.scene += kb.Cube(name="floor", scale=(10, 10, 0.1),
                         position=(0, 0, -0.3), material=kb.FlatMaterial(),
                         static=True)

        self.scene += kb.Cube(name="wall1", scale=(0.1, 7, 1),
                         position=(7, 0, 0.5), material=kb.FlatMaterial(),
                         static=True)

        self.scene += kb.Cube(name="wall2", scale=(0.1, 7, 1),
                         position=(-7, 0, 0.5), material=kb.FlatMaterial(),
                         static=True)

        self.scene += kb.Cube(name="wall3", scale=(7, 0.1, 1),
                         position=(0, 7, 0.5), material=kb.FlatMaterial(),
                         static=True)

        self.scene += kb.Cube(name="wall4", scale=(7, 0.1, 1),
                         position=(0, -7, 0.5), material=kb.FlatMaterial(),
                         static=True)

        self.scene += kb.DirectionalLight(name="sun", position=(-1, -0.5, 3),
                                     look_at=(0, 0, 0), intensity=1.5)


        self.scene += kb.PerspectiveCamera(name="camera",
                                           position=(0, 0, 20),
                                           look_at=(0, 0, 1))

        ############ ADD OBJECTS ###############################
        rng = np.random.default_rng()
        velocity = rng.uniform([-1, -1, 0], [1, 1, 0])

        #scale = 0.04
        scale = 1
        obj = kb.FileBasedObject(
          asset_id="G6",
          render_filename="/1DatasetGeneration/assets/visual_geometry.obj",
          bounds=((-1, -1, 0), (1, 1, 1)),
          position=(0, 0, 1), # position=(0, 0, 0.2),
          simulation_filename="/1DatasetGeneration/assets/teapot.urdf",
          scale=(scale, scale, scale),
          material=kb.PrincipledBSDFMaterial(color=kb.random_hue_color()),
          velocity=rng.uniform([-1, -1, 0], [1, 1, 0])) #velocity=rng.uniform([0,0,0], [0,0,0]))

        self.scene += obj
        self.control_obj = obj


    def run_simulation(self):
        renderer = KubricRenderer(self.scene)
        simulator = KubricSimulator(self.scene)

        spawn_region = [[-2, -2, 5], [2, 2, 10]]

        path_name = "/1DatasetGeneration/output_pipeline/"
        renderer.save_state(path_name + "helloworld0.blend")
        kb.move_until_no_overlap(self.control_obj, simulator, spawn_region=spawn_region)
        simulator.run()

        # --- render (and save the blender file)
        renderer.save_state(path_name + "helloworld1.blend")
        frame = renderer.render()
        kb.write_image_dict(frame, path_name)


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    DatasetGen = ArtificialDatasetGeneration()

    DatasetGen.config_scene()
    DatasetGen.run_simulation()
