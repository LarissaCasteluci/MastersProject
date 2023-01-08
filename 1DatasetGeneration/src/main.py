import subprocess
import glob
from pathlib import Path
from typing import Tuple, List
import os
import time

if __name__ == "__main__":
    # Load the list of available
    src_folder: Path = Path(os.path.abspath(__file__)).parent
    path_assets: Path = src_folder.parent / "assets" / "grasp_objects"
    urdf_files: List[str] = glob.glob(str(path_assets) + '/*_docker.urdf')
    urdf_files.sort()
    n_files: int = len(urdf_files)
    number_of_samples = 5

    processes = []
    for n, urdf_path in enumerate(urdf_files):

        if n < 20:
            continue

        obj_name: str = Path(urdf_path).stem[:2]

        for repeat in range(number_of_samples):
            process = subprocess.Popen(f'cd /home/larissa/MastersProject && '\
                                        'docker run --rm '\
                                        '--user $(id -u):$(id -g) '\
                                        '--volume "$(pwd)/original_repos/kubric:/kubric" '\
                                        '--volume "$(pwd)/1DatasetGeneration:/1DatasetGeneration" '\
                                        'kubruntu-modified ' \
                                        f'/usr/bin/python3 /1DatasetGeneration/src/pipeline.py -obj {obj_name} -repeat {repeat}',
                                       shell=True,
                                       stdout=subprocess.PIPE)

            # process.wait()
            # break
            processes.append(process)

        # break


        if (n + 1) % 3 == 0:
            for p in processes:
                p.wait()

            # break
            processes = []


    for p in processes:
        p.wait()

