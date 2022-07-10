# https://pybullet.org/Bullet/phpBB3/viewtopic.php?p=42686

import logging

import kubric as kb
import numpy as np
from kubric.renderer.blender import Blender as KubricRenderer
from kubric.simulator.pybullet import PyBullet as KubricSimulator
#

logging.basicConfig(level="INFO")

# --- create scene and attach a renderer to it
scene = kb.Scene(resolution=(256, 256))
scene.frame_end = 20   # < numbers of frames to render
scene.frame_rate = 1  # < rendering framerate
scene.step_rate = 240  # < simulation total steps
renderer = KubricRenderer(scene)
simulator = KubricSimulator(scene)

# --- populate the scene with objects, lights, cameras
scene += kb.Cube(name="floor",
                 scale=(10, 10, 0.1),
                 position=(0, 0, -0.3),
                 material=kb.FlatMaterial(),
                 static=True)

scene += kb.Cube(name="wall1",
                 scale=(0.1, 7, 1),
                 position=(7, 0, 0.5),
                 material=kb.FlatMaterial(),
                 static=True)

scene += kb.Cube(name="wall2",
                 scale=(0.1, 7, 1),
                 position=(-7, 0, 0.5),
                 material=kb.FlatMaterial(),
                 static=True)

scene += kb.Cube(name="wall3",
                 scale=(7, 0.1, 1),
                 position=(0, 7, 0.5),
                 material=kb.FlatMaterial(),
                 static=True)

scene += kb.Cube(name="wall4",
                 scale=(7, 0.1, 1),
                 position=(0, -7, 0.5),
                 material=kb.FlatMaterial(),
                 static=True)

scene += kb.DirectionalLight(name="sun",
                             position=(-1, -0.5, 3),
                             look_at=(0, 0, 0),
                             intensity=1.5)


scene += kb.PerspectiveCamera(name="camera",
                              position=(0, 0, 20),
                              look_at=(0, 0, 1))




############ ADD OBJECTS ###############################
rng = np.random.default_rng()
velocity = rng.uniform([-1, -1, 0], [1, 1, 0])

#scale = 0.04
scale=1
obj = kb.FileBasedObject(
  asset_id="G6",
  render_filename="/1DatasetGeneration/assets/visual_geometry.obj",
  bounds=((-1, -1, 0), (1, 1, 1)),
  #position=(0, 0, 0.2),
  position=(0, 0, 1),
  simulation_filename="/1DatasetGeneration/assets/teapot.urdf",
  scale=(scale, scale, scale),
  material=kb.PrincipledBSDFMaterial(color=kb.random_hue_color()),
  velocity=rng.uniform([-1, -1, 0], [1, 1, 0]))
 #velocity=rng.uniform([0,0,0], [0,0,0]))


scene += obj

spawn_region = [[-2, -2, 5], [2, 2, 10]]
renderer.save_state("/1DatasetGeneration/output/helloworld.blend")
kb.move_until_no_overlap(obj, simulator, spawn_region=spawn_region)
simulator.run()

# --- render (and save the blender file)
renderer.save_state("/1DatasetGeneration/output/helloworld.blend")
frame = renderer.render()
kb.write_image_dict(frame, "/1DatasetGeneration/output_teapot/")

# --- save the output as pngs
#kb.write_png(frame["rgba"], "/1DatasetGeneration/output/helloworld.png")
#kb.write_palette_png(frame["segmentation"], "/1DatasetGeneration/output/helloworld_segmentation.png")
#scale = kb.write_scaled_png(frame["depth"], "/1DatasetGeneration/output/helloworld_depth.png")
#logging.info("Depth scale: %s", scale)