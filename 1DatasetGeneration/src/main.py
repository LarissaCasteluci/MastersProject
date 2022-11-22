import subprocess
import glob
from pathlib import Path
from typing import Tuple, List
import os

if __name__ == "__main__":
    # Load the list of available
    src_folder: Path = Path(os.path.abspath(__file__)).parent
    path_assets: Path = src_folder.parent / "assets" / "grasp_objects"
    urdf_files: list[str] = glob.glob(str(path_assets) + '/*_docker.urdf')
    urdf_files.sort()
    n_files: int = len(urdf_files)

    for i in range(len(urdf_files)):

        process = subprocess.Popen(f'cd /home/larissa/MastersProject && '\
                                    'docker run --rm --interactive '\
                                    '--user $(id -u):$(id -g) '\
                                    '--volume "$(pwd)/original_repos/kubric:/kubric" '\
                                    '--volume "$(pwd)/1DatasetGeneration:/1DatasetGeneration" '\
                                    'kubruntu-modified ' \
                                    '/usr/bin/python3 /1DatasetGeneration/src/pipeline.py ',
                                   shell=True,
                                   stdout=subprocess.PIPE)

        process.wait()
        print(process.communicate())
        print(process.returncode)

        break
