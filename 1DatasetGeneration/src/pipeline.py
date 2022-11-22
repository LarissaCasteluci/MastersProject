# TODO: Add License

import logging
import glob
from pathlib import Path
from typing import Tuple, List
import os

from stereo_matching import StereoMatching
from artificial_dataset_generation import ArtificialDatasetGeneration
from dataset_generation_tools.data_exporters.jacquard_format import JacquardDataExporter
from dataset_generation_tools.grasp_proposal_generator.proposal_generator import ProposalGenerator, TypesGenerator
from dataset_generation_tools.base_data_structures.camera_conversions import camera2world_coordinates


def pipeline(urdf_path: str, obj_name: str):
    print(obj_name)

    frame_end: int = 5
    #frame_end: int = 20
    image_idx: int = frame_end - 1
    resolution: Tuple[int, int] = (300, 300)

    path = f"/1DatasetGeneration/outputs/tmp/{obj_name}"
    DatasetGen = ArtificialDatasetGeneration(path)
    DatasetGen.configure_new_scene(resolution, frame_end=frame_end)
    DatasetGen.config_scene()

    # Load Auxiliary Classes
    GraspProposal = ProposalGenerator(TypesGenerator.RANDOM, max_proposals=2)
    grasps = GraspProposal.generate_proposals(resolution)

    # Exporter = JacquardDataExporter(str(src_folder.parent / "outputs" / "jacquard_output1"))

    # 2. Loading the new objects from the assets folder
    DatasetGen.calculate_new_pos_and_quat()
    DatasetGen.add_grasping_object(obj_name)

    DatasetGen.move_until_no_overlap()
    # 3. Call renderer and generate data
    DatasetGen.call_renderer("/camera1")

    # Render second image
    DatasetGen.scene.remove(DatasetGen.camera_1)
    DatasetGen.scene += DatasetGen.camera_2
    DatasetGen.call_renderer("/camera2")

    # Choose image for stereo matching
    # stereo_matching = StereoMatching(path + "/camera1/rgba_00005.png",
    #                                 path + "/camera2/rgba_00005.png")

    DatasetGen.save_obj_pos_and_quat()
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

        DatasetGen.grasp_proposal_simulation(obj_name, grasp_in_world_coordinates)

    break
    # Use the Exporter to save the data to the correct folder


if __name__ == "__main__":
    logging.basicConfig(level="INFO")

    # Load the list of available
    src_folder: Path = Path(os.path.abspath(__file__)).parent
    path_assets: Path = src_folder.parent / "assets" / "grasp_objects"
    urdf_files: list[str] = glob.glob(str(path_assets) + '/*_docker.urdf')
    urdf_files.sort()
    n_files: int = len(urdf_files)

    urdf_path: str = urdf_files[i]
    obj_name: str = Path(urdf_path).stem[:2]



