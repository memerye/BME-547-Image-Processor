# image_processing.py
import numpy as np
from skimage import io, exposure
from time import time
import matplotlib.pyplot as plt

# Ignore warnings
import warnings
warnings.filterwarnings("ignore")


def convert_image_to_uint8(array):
    if array.dtype == np.float:
        if array.max() <= 1:
            result = 255*array
        else:
            result = array
        return result.astype(np.uint8)
    else:
        return array.astype(np.uint8)


class ImageProcessing(object):
    def __init__(self, image):
        self.image = convert_image_to_uint8(image)
        self.shape = image.shape

    def __len__(self):
        return len(self.image)

    def histeq(self):
        start = time()
        img_eq = exposure.equalize_hist(self.image)
        img_eq_uint8 = convert_image_to_uint8(img_eq)
        return img_eq_uint8, time()-start
