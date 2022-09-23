import kubric as kb
import numpy as np
import glob
from pathlib import Path
from kubric.renderer.blender import Blender as KubricRenderer
from pybullet_simulator import PyBullet as KubricSimulator
import csv
import time

if __name__ == "__main__":
    obj_files_path: Path = Path("/1DatasetGeneration/assets/convex_hull_tests")
    obj_files: list[str] = glob.glob(str(obj_files_path) + '/*.urdf')

    ranker_file = open('/1DatasetGeneration/assets/ranker.csv', 'w')
    writer = csv.writer(ranker_file)
    header = ["file", "q0", "q1", "q2", "q3", "sumq"]
    writer.writerow(header)

    scene = kb.Scene(resolution=(256, 256))
    scene.frame_end = 50  # < numbers of frames to render
    scene.frame_rate = 12  # < rendering framerate
    scene.step_rate = 7200  # < simulation total steps

    scene += kb.Cube(name="floor", scale=(100, 100, 0.1),
                     position=(0, 0, -0.3), material=kb.FlatMaterial(),
                     static=True)

#    scene += kb.Cube(name="wall1", scale=(0.1, 7, 1),
#                     position=(7, 0, 0.5), material=kb.FlatMaterial(),
#                     static=True)

#    scene += kb.Cube(name="wall2", scale=(0.1, 7, 1),
#                     position=(-7, 0, 0.5), material=kb.FlatMaterial(),
#                     static=True)

#    scene += kb.Cube(name="wall3", scale=(7, 0.1, 1),
#                     position=(0, 7, 0.5), material=kb.FlatMaterial(),
#                     static=True)

#    scene += kb.Cube(name="wall4", scale=(7, 0.1, 1),
#                     position=(0, -7, 0.5), material=kb.FlatMaterial(),
#                     static=True)

    scene += kb.DirectionalLight(name="sun", position=(-1, -0.5, 3),
                                 look_at=(0, 0, 0), intensity=15)

    scene += kb.PerspectiveCamera(name="camera",
                                  position=(0, 0, 400),
                                  look_at=(0, 0, 1))

    ############ ADD OBJECTS ###############################
    rng = np.random.default_rng()
    velocity = rng.uniform([-1, -1, 0], [1, 1, 0])

    renderer = KubricRenderer(scene)
    simulator = KubricSimulator(scene)

    previous_obj = []
    for i, obj in enumerate(obj_files):
        data = []
        data.append(obj)

        if i == 0:
            pass
        else:
            scene.remove(previous_obj)

        scale = 1
        #scale = 3
        obj = kb.FileBasedObject(
              asset_id=obj,
              render_filename="/1DatasetGeneration/assets/grasp_objects/C0.obj",
              #render_filename="/1DatasetGeneration/assets/grasp_objects/samples/teapot_visual.obj",
              simulation_filename="/1DatasetGeneration/assets/convex_hull_tests/C0_1_10000_true_flood_20_true.urdf",
              #simulation_filename="/1DatasetGeneration/assets/grasp_objects/samples/teapot.urdf",
              scale=(scale, scale, scale),
              material=kb.PrincipledBSDFMaterial(color=kb.random_hue_color()),
              #mass=1,
              #friction=0.9,
              #restitution=0.01,
              #bounds=((-1, -1, -1), (1, 1, 1))
        )

        cube = kb.Cube(scale=30, velocity=velocity, material=kb.PrincipledBSDFMaterial(color=kb.random_hue_color()))
        #scene += cube
        scene += obj
        previous_obj = obj

        path_name = "/1DatasetGeneration/outputs/output_tests_20220921"
        spawn_region = [[-20, -20, -50], [20, 20, 100]]
        kb.move_until_no_overlap(obj, simulator, spawn_region=spawn_region)
        simulator.run()

        data.append(simulator.quaternion_sum[0])
        data.append(simulator.quaternion_sum[1])
        data.append(simulator.quaternion_sum[2])
        data.append(simulator.quaternion_sum[3])
        data.append(simulator.quaternion_sum[0] + simulator.quaternion_sum[1] + simulator.quaternion_sum[2] + simulator.quaternion_sum[3])
        print(i, ": ", simulator.quaternion_sum[0] + simulator.quaternion_sum[1] + simulator.quaternion_sum[2] + simulator.quaternion_sum[3])

        writer.writerow(data)

        frame = renderer.render()
        kb.write_image_dict(frame, path_name)
        renderer.save_state("/1DatasetGeneration/outputs/output_tests_20220921/helloworld1.blend")

        break
