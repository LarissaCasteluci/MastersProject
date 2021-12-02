##### Download repositories ########################## 
#Make all Directories for the projects
mkdir GGCNN
mkdir DexNet2
mkdir DenseObjectNet

#Download GG-CNN 
cd original_repos/GGCNN
git clone https://github.com/dougsm/ggcnn.git
conda activate ggcnn
pip install -r requirements.txt

#Download DexNet Family
cd ../DexNet2
git clone https://github.com/BerkeleyAutomation/gqcnn
conda activate dexnet2
pip install .

#Download DenseObjectNet
cd ../DenseObjectNet
git clone https://github.com/RobotLocomotion/pytorch-dense-correspondence

###### Configure Datasets ##########################
cd ../../Datasets

if [ ! -d "Jacquard" ]; then
  # Download Here: 
  mkdir Jacquard
fi

if [ ! -d "Cornell" ]; then
  # Download Here: 
  mkdir Cornell
fi

if [ ! -d "DexNet2" ]; then
  # Download Here: https://berkeley.app.box.com/s/6mnb2bzi5zfa7qpwyn7uq5atb7vbztng/folder/40676204986
  mkdir DexNet2
fi

if [ ! -d "DenseCorrespondence" ]; then 
  mkdir original_repos/DenseObjectNet/DenseCorrespondence
  #TODO : Testar se o download do Dataset é melhor por wget ou o script python 
  #cd pytorch-dense-correspondence
  #conda activate densecorrespondence
  #python config/download_pdc_data.py config/dense_correspondence/dataset/composite/caterpillar_upright.yaml ~/MastersProject/
  # wget -q https://data.csail.mit.edu/labelfusion/pdccompressed/evaluation_labeled_data_compressed.tar.gz
fi

if [ ! -d "EGAD!" ]; then
  mkdir EGAD
fi

if [ ! -d "MYEGAD" ]; then
  mkdir MYEGAD
fi



