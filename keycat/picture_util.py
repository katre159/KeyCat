import numpy


def convert_picture_to_grayscale(picture):
    return picture.convert('L')


def convert_picture_to_numpy_array(picture):
    return numpy.asarray(picture, dtype=numpy.uint8)
