conda activate py3.7
python3 -m venv ./ros-venv
conda deactivate
conda deactivate
conda deactivate
source ./ros-venv/bin/activate
./ros-venv/bin/python3 -m pip install --upgrade pip
pip install numpy==1.21.5
pip install opencv-python==4.5.5.64
pip install matplotlib==3.5.1
pip install scikit-image==0.19.2
pip install imageio==2.16.1
pip install imagecodecs==2021.11.20
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113
pip install torchsummary==1.5.1
pip install tensorboardX==2.5
pip install rosinstall msgpack empy defusedxml netifaces
pip install pyrealsense2
