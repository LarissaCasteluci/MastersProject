# TODO: Add License

import logging
import glob
from pathlib import Path
import random
from artificial_dataset_generation import ArtificialDatasetGeneration


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    DatasetGen = ArtificialDatasetGeneration()

    # Load the list of available
    path_assets = Path("/1DatasetGeneration/assets/")
    urdf_files = glob.glob( str(path_assets / '.urdf'))
    n_files =

    for i in range(1):  #



    # 2. Loading the new objects in the assets folder
    # 3. Call Simulation -> Wait until objects are stabilized (ADD walls!)
    # 4. Call Rendering
    # 5. Call Simulation -> Propose Random Grasps
    # 6. FOR loop
    # 7. For each proposal, try to perform the grasping (Can I delete the walls?) -> YES! use remove!
    # 8. If the grasps is acceptable, export data to data_exporter
    # 9. At the end Export Data to

    #DatasetGen.config_scene()
    #DatasetGen.run_simulation()
