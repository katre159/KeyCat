import cv2
import numpy as np
import abc
from keycat.picture_util import *


class AbstractTemplateMatcher(object):

    @abc.abstractmethod
    def get_template_location(self, template, picture):
        pass


class CCOEFFNORMEDTemplateMatcher(AbstractTemplateMatcher):

    def get_template_location(self, template, picture):
        picture = convert_picture_to_grayscale(picture)
        picture_array = convert_picture_to_numpy_array(picture)

        method = eval('cv2.TM_CCOEFF_NORMED')

        res = cv2.matchTemplate(picture_array, template, method)
        threshold = 0.8
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if max_val >= threshold:
            return max_loc
        else:
            return None


