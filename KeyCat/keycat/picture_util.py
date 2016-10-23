import numpy as np


def convert_picture_to_grayscale(picture):
    return picture.convert('L')


def convert_picture_to_numpy_array(picture):
    return np.asarray(picture, dtype=np.uint8)
