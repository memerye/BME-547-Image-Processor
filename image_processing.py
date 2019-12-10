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

    def constr(self):
        start = time()
        img_min = self.image.min()
        img_max = self.image.max()
        img_constr = 255*((self.image-img_min)/(img_max-img_min))
        img_constr_uint8 = convert_image_to_uint8(img_constr)
        return img_constr_uint8, time()-start

    def logcom(self):
        start = time()
        img_log = exposure.adjust_log(self.image)
        img_log_uint8 = convert_image_to_uint8(img_log)
        return img_log_uint8, time()-start

    def invert(self):
        start = time()
        img_invert = 255-self.image
        img_invert_uint8 = convert_image_to_uint8(img_invert)
        return img_invert_uint8, time()-start

    def plotimages(self, img_raw, img_processed):
        plt.subplot(2, 2, 1)
        plt.imshow(img_raw)
        plt.title("Raw Image")
        plt.subplot(6, 2, 7)
        img_hist, img_bins = exposure.histogram(img_raw[::][0], 3)
        plt.plot(img_bins, img_hist, 'r')
        plt.subplot(6, 2, 9)
        img_hist, img_bins = exposure.histogram(img_raw[::][1], 3)
        plt.plot(img_bins, img_hist, 'g')
        plt.subplot(6, 2, 11)
        img_hist, img_bins = exposure.histogram(img_raw[::][2], 3)
        plt.plot(img_bins, img_hist, 'b')
        plt.subplot(2, 2, 2)
        plt.imshow(img_processed)
        plt.title("Processed Image")
        plt.subplot(6, 2, 8)
        img_eq_hist, img_eq_bins = exposure.histogram(img_processed[::][0], 3)
        plt.plot(img_eq_bins, img_eq_hist, 'r')
        plt.subplot(6, 2, 10)
        img_eq_hist, img_eq_bins = exposure.histogram(img_processed[::][1], 3)
        plt.plot(img_eq_bins, img_eq_hist, 'g')
        plt.subplot(6, 2, 12)
        img_eq_hist, img_eq_bins = exposure.histogram(img_processed[::][2], 3)
        plt.plot(img_eq_bins, img_eq_hist, 'b')
        plt.show()
        return None


if __name__ == "__main__":
    root = "/Users/liangyu/Downloads/Docs/BME/BME547/Lecture/" \
           "image_processer/101_ObjectCategories/bonsai"
    path = [root+'/image_0014.jpg', root+'/image_0015.jpg',
            root+'/image_0016.jpg']
    images = []
    for i in path:
        image = io.imread(i)
        images.append(image)
        I = ImageProcessing(image)
        img = I.image
        shape = I.shape
        length = I.__len__()
        img_processed, run_time = I.invert()
        print(type(img))
        print(shape)
        print(length)
        print(run_time)
        I.plotimages(img, img_processed)
