#Make all Directories for the projects
mkdir GGCNN
mkdir DexNet2
mkdir DenseObjectNet

#Download GG-CNN 
cd original_repos/GGCNN
git clone https://github.com/dougsm/ggcnn.git

#Download DexNet Family
cd ../DexNet2
git clone https://github.com/BerkeleyAutomation/gqcnn

#Download DenseObjectNet
cd ../DenseObjectNet
git clone https://github.com/RobotLocomotion/pytorch-dense-correspondence
