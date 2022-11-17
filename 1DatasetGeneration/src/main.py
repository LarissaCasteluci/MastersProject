# TODO: Add License

import logging
import glob
from pathlib import Path
from typing import Tuple, List
import os
from artificial_dataset_generation import ArtificialDatasetGeneration
from dataset_generation_tools.data_exporters.jacquard_format import JacquardDataExporter
from dataset_generation_tools.grasp_proposal_generator.proposal_generator import ProposalGenerator, TypesGenerator
from dataset_generation_tools.base_data_structures.camera_conversions import camera2world_coordinates


if __name__ == "__main__":
    logging.basicConfig(level="INFO")

    # Load the list of available
    src_folder: Path = Path(os.path.abspath(__file__)).parent
    path_assets: Path = src_folder.parent / "assets" / "grasp_objects"
    urdf_files: list[str] = glob.glob(str(path_assets) + '/*_docker.urdf')
    urdf_files.sort()
    n_files: int = len(urdf_files)

    frame_end: int = 2
    #frame_end: int = 20
    image_idx: int = frame_end - 1
    resolution: Tuple[int, int] = (300, 300)

    DatasetGen = ArtificialDatasetGeneration('tmp')
    DatasetGen.configure_new_scene(resolution, frame_end=frame_end)
    DatasetGen.config_scene()

    for i in [0, 1]: #range(len(urdf_files)):  # Number of objects of be generated
        urdf_path: str = urdf_files[i]
        obj_name: str = Path(urdf_path).stem[:2]
        print(obj_name)

        # Load Auxiliary Classes
        GraspProposal = ProposalGenerator(TypesGenerator.RANDOM, max_proposals=2)
        grasps = GraspProposal.generate_proposals(resolution)

        # Exporter = JacquardDataExporter(str(src_folder.parent / "outputs" / "jacquard_output1"))

        # 2. Loading the new objects from the assets folder
        #DatasetGen.calculate_new_pos_and_quat()
        DatasetGen.grasping_object_pos = [4, 4, 0]
        DatasetGen.grasping_object_quat = [1, 0, 0, 0]
        DatasetGen.add_grasping_object(obj_name)

        # 3. Call renderer and generate data
        DatasetGen.call_renderer()

        break
        DatasetGen.remove_grasping_object()

        DatasetGen.save_obj_pos_and_quat()
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



