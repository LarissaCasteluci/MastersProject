import logging
import numpy as np
import time
import torch.utils.data
from models.common import post_process_output
from utils.dataset_processing import evaluation, grasp
from utils.data import get_dataset
from models.ggcnn2 import GGCNN2
import cv2
from utils.visualisation.gridshow import gridshow
logging.basicConfig(level=logging.INFO)


def call_inference(args):

    #net = torch.load(args.network)
    input_channels = 1*args.use_depth + 3*args.use_rgb
    net = GGCNN2(input_channels=input_channels)
    net.load_state_dict(torch.load(args.network))
    device = torch.device("cuda:0")
    net = net.to(device)

    # Load Dataset
    logging.info('Initializing ...')
    Dataset = get_dataset(args.dataset)

    inference = Dataset(args.depth, args.rgb,
                        include_depth=args.use_depth,
                        include_rgb=args.use_rgb)


    logging.info('Done')

    with torch.no_grad():
        net.eval()
        x = inference.return_x()
        logging.info(f'Processing Data!')
        xc = x.to(device)
        output = net(xc)

        q_img, ang_img, width_img = post_process_output(output[0][0][0][0],
                                                        output[0][0][0][1],
                                                        output[0][0][0][2],
                                                        output[0][0][0][3])

        grasps = grasp.detect_grasps(q_img,
                                     ang_img,
                                     width_img=width_img,
                                     no_grasps=args.n_grasps)

    if args.vis:
        evaluation.plot_output(args.rgb,
                               args.depth,
                               q_img,
                               ang_img,
                               no_grasps=args.n_grasps,
                               grasp_width_img=width_img)
        time.sleep(3)


    return grasps



