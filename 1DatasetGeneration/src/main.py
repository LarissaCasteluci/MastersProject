# TODO: Add License

import logging
import glob
from pathlib import Path
import random
import os
from artificial_dataset_generation import ArtificialDatasetGeneration


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    DatasetGen = ArtificialDatasetGeneration()
    DatasetGen.config_scene()

    # Load the list of available
    path_assets = Path(os.path.abspath(__file__)).parent.parent / "assets"
    urdf_files = glob.glob(str(path_assets) + '/*.urdf')
    n_files = len(urdf_files)

    for i in range(1):  #
        x: int = random.randint(0, n_files - 1)
        urdf_path: str = urdf_files[x]
        obj_name: str = Path(urdf_path).stem
        DatasetGen.add_objects(obj_name)
        DatasetGen.call_renderer()


    # 2. Loading the new objects in the assets folder
    # 3. Call Simulation -> Wait until objects are stabilized (ADD walls!)
    # 4. Call Rendering
    # 5. Call Simulation -> Propose Random Grasps
    # 6. FOR loop
    # 7. For each proposal, try to perform the grasping (Can I delete the walls?) -> YES! use remove!
    # 8. If the grasps is acceptable, export data to data_exporter
    # 9. At the end Export Data to

    #DatasetGen.run_simulation()
