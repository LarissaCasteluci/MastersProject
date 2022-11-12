# TODO: Add License

import logging
import glob
from pathlib import Path
import random
import os
from artificial_dataset_generation import ArtificialDatasetGeneration
from dataset_generation_tools.data_exporters.jacquard_format import JacquardDataExporter
from dataset_generation_tools.grasp_proposal_generator.proposal_generator import ProposalGenerator, TypesGenerator
from typing import Tuple


if __name__ == "__main__":
    logging.basicConfig(level="INFO")

    # Load the list of available
    src_folder: Path = Path(os.path.abspath(__file__)).parent
    path_assets: Path = src_folder.parent / "assets" / "grasp_objects"
    urdf_files: list[str] = glob.glob(str(path_assets) + '/*.urdf')
    n_files: int = len(urdf_files)

    frame_end: int = 20
    image_idx: int = frame_end - 1
    resolution: Tuple[int, int] = (300, 300)

    # Load Auxiliary Classes
    GraspProposal = ProposalGenerator(TypesGenerator.RANDOM)
    #Exporter = JacquardDataExporter(str(src_folder.parent / "outputs" / "jacquard_output1"))
    DatasetGen = ArtificialDatasetGeneration('tmp', frame_end=frame_end)
    DatasetGen.config_scene()

    for i in range(1):  # Number of objects of be generated
        urdf_path: str = urdf_files[i]
        obj_name: str = Path(urdf_path).stem

        # 2. Loading the new objects in the assets folder
        DatasetGen.add_objects(obj_name)

        for n in range(1):
        #for n in range(Exporter.n_samples_per_object):
            # 3. Call Simulation -> Wait until objects are stabilized (ADD walls!)
            # 4. Call Rendering
            DatasetGen.call_renderer()

            #Load


            # 5. Call Simulation -> Propose Random Grasps
            # 6. FOR loop
            # 7. For each proposal, try to perform the grasping (Can I delete the walls?) -> YES! use remove!
            # 8. If the grasps is acceptable, export data to data_exporter
            # 9. At the end Export Data to

            #DatasetGen.run_simulation()
