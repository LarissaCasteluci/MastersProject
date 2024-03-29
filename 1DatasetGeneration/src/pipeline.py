# TODO: Add License

import logging
import glob
import pdb
from pathlib import Path
from typing import Tuple, List
import os
import argparse
import sys

from stereo_matching import StereoMatching
from artificial_dataset_generation import ArtificialDatasetGeneration
from dataset_generation_tools.data_exporters.jacquard_format import JacquardDataExporter, MetaDataSave
from dataset_generation_tools.grasp_proposal_generator.proposal_generator import ProposalGenerator, TypesGenerator
from dataset_generation_tools.base_data_structures.camera_conversions import camera2world_coordinates, world2camera_coordinates


def pipeline(obj_name: str, repeat: int):
    print(obj_name)
    repeat: str = str(repeat)

    frame_end: int = 5
    #frame_end: int = 20
    image_idx: int = frame_end - 1
    resolution: Tuple[int, int] = (1024, 1024)

    path = f"/1DatasetGeneration/outputs/tmp/{obj_name}_{str(repeat)}"
    DatasetGen = ArtificialDatasetGeneration(path)
    DatasetGen.configure_new_scene(resolution, frame_end=frame_end)
    DatasetGen.config_scene()

    out_path = str(src_folder.parent / "outputs" / "jacquard_format_output" / f"{obj_name}")
    Path(out_path).mkdir(parents=True, exist_ok=True)

    Exporter = JacquardDataExporter(out_path, obj_name, repeat)
    metadata = MetaDataSave(out_path, obj_name, repeat)

    # 2. Loading the new objects from the assets folder
    DatasetGen.calculate_new_pos_and_quat()
    DatasetGen.add_grasping_object(obj_name)
    DatasetGen.move_until_no_overlap()

    DatasetGen.save_obj_pos_and_quat() # Save object position and Quaternion

    GraspProposal = ProposalGenerator(TypesGenerator.GAUSSIAN,
                                      max_proposals=100)
    obj_pos_in_image = world2camera_coordinates(resolution, (4, 4), DatasetGen.grasping_object_pos)

    grasps = GraspProposal.generate_proposals(resolution,
                                              obj_pos_in_image
                                              )


    # 3. Call renderer and generate data
    DatasetGen.call_renderer("/camera1")

    # Render second image
    DatasetGen.scene.remove(DatasetGen.camera_1)
    DatasetGen.scene += DatasetGen.camera_2
    DatasetGen.call_renderer("/camera2")

    # Choose image for stereo matching
    stereo_matching = StereoMatching(path + "/camera1/rgba_00004.png",
                                     path + "/camera2/rgba_00004.png")

    stereo_matching.generate_stereo_image(str(src_folder.parent /
                                              "outputs" /
                                              "jacquard_format_output" /
                                              f"{obj_name}" /
                                              f"{repeat}_{obj_name}_stereo_depth.tiff"))

    Exporter.save_images()
    metadata.save_obj_pos_and_quat(DatasetGen.grasping_object_pos,
                                   DatasetGen.grasping_object_quat)

    DatasetGen.remove_grasping_object()

    # Save grasping object position
    end_position: List[float] = DatasetGen.grasping_object_pos
    end_quat: List[float] = DatasetGen.grasping_object_quat

    print("POSITION:", end_position)

    # Try to perform grasps
    for grasp in grasps:
        # Configure new scene for each simulation
        DatasetGen.grasping_object_pos = end_position
        DatasetGen.grasping_object_quat = end_quat
        grasp_in_world_coordinates = camera2world_coordinates(resolution, (4, 4), grasp)

        print("grasp:", grasp_in_world_coordinates)

        is_grasp_sucessfull = DatasetGen.grasp_proposal_simulation(obj_name, grasp_in_world_coordinates)

        # Use the Exporter to save the data to the correct folder
        if is_grasp_sucessfull:
            Exporter.save_grasps([(1024 - grasp.x), 1024 - grasp.y, grasp.theta*180, 400.0, 400.0])




if __name__ == "__main__":
    logging.basicConfig(level="INFO")

    # Load the list of available
    src_folder: Path = Path(os.path.abspath(__file__)).parent
    path_assets: Path = src_folder.parent / "assets" / "grasp_objects"
    urdf_files: list[str] = glob.glob(str(path_assets) + '/*_docker.urdf')
    urdf_files.sort()
    n_files: int = len(urdf_files)

    parser = argparse.ArgumentParser(
                    prog='pipeline',
                    description='starts the pipeline for generating artificial data',
                    epilog='Text at the bottom of help')

    parser.add_argument('-obj', action='store', type=str, required=True)
    parser.add_argument('-repeat', action='store', type=str, required=True)
    args = parser.parse_args()

    pipeline(args.obj, args.repeat)







