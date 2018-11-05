# -*- coding: utf-8 -*- 
import os
import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt
import cv2 
import time 

from datetime import datetime
# Root directory of the project 
ROOT_DIR = os.path.abspath("../../")

# Import Mask RCNN 
sys.path.append(ROOT_DIR)
# To find local version of the library 
from mrcnn.config import Config
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
# Import COCO config 
sys.path.append(os.path.join(ROOT_DIR, "samples/coco/")) 
# To find local version from samples.coco import coco


MODEL_DIR=os.path.join(ROOT_DIR,"logs")
COCO_MODEL_PATH=os.path.join(ROOT_DIR,"new.h5")

if not os.path.exists(COCO_MODEL_PATH):
	utils.download_trained_weights(COCO_MODEL_PATH)
	print("---------------not coco")


IMAGE_DIR=os.path.join(ROOT_DIR,"images")

class ShapesConfig(Config):
    """Configuration for training on the toy shapes dataset.
    Derives from the base Config class and overrides values specific
    to the toy shapes dataset.
    """
    # Give the configuration a recognizable name
    NAME = "shapes"

    # Train on 1 GPU and 8 images per GPU. We can put multiple images on each
    # GPU because the images are small. Batch size is 8 (GPUs * images/GPU).
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

    # Number of classes (including background)
    NUM_CLASSES = 1 + 1  # background + 3 shapes

    # Use small images for faster training. Set the limits of the small side
    # the large side, and that determines the image shape.
    IMAGE_MIN_DIM = 800
    IMAGE_MAX_DIM = 1280

    # Use smaller anchors because our image and objects are small
    RPN_ANCHOR_SCALES = (8 * 6, 16 * 6, 32 * 6, 64 * 6, 128 * 6)  # anchor side in pixels

    # Reduce training ROIs per image because the images are small and have
    # few objects. Aim to allow ROI sampling to pick 33% positive ROIs.
    TRAIN_ROIS_PER_IMAGE = 16

    # Use a small epoch since the data is simple
    STEPS_PER_EPOCH = 100

    # use small validation steps since the epoch is small
    VALIDATION_STEPS = 5

class InferenceConfig(ShapesConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()

# Recreate the model in inference mode
model = modellib.MaskRCNN(mode="inference", 
                          config=config,
                          model_dir=MODEL_DIR)

model.load_weights(COCO_MODEL_PATH,by_name=True)

class_names=['BG','food']
file_names=next(os.walk(IMAGE_DIR))[2]
image=skimage.io.imread(os.path.join(IMAGE_DIR,random.choice(file_names)))

a=datetime.now()
results=model.detect([image],verbose=1)
b=datetime.now()

print("time= ",(b-a).seconds)

r = results[0]
visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], 
                            class_names, r['scores'])

