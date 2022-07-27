from enum import Enum


class TestTypes(Enum):
    RGB_AND_DEPTH = 1
    ONLY_DEPTH = 2


class Arguments:
    def __init__(self, network_name, test_type):
        if network_name == "ggcnn2":
            # Inference GG-CNN
            self.network_name = "ggcnn2"
            if test_type == TestTypes.RGB_AND_DEPTH:  # Path to weights
                self.network = '/home/larissa/MastersProject/catkin_ws/src/kuka_kontrol/src/Pipeline/weights/epoch_18_iou_0.90_statedict.pt'
            elif test_type == TestTypes.ONLY_DEPTH:
                self.network = '/home/larissa/MastersProject/catkin_ws/src/kuka_kontrol/src/Pipeline/weights/epoch_07_iou_0.86_statedict.pt'  # Path to weights

            # Dataset & Data & Training
            self.dataset = "realsense_inference"  # dataset format
            self.use_depth = 1  # Use depth
            if test_type == TestTypes.RGB_AND_DEPTH:
                self.use_rgb = 1
            elif test_type == TestTypes.ONLY_DEPTH:
                self.use_rgb = 0
            self.ds_rotate = 0.0  # Shift the start point of the dataset to use a different test/train split
            self.num_workers = 1  # Dataset workers
            self.n_grasps = 1  # Number of grasps to consider per image
            self.vis = True
            self.save = False


