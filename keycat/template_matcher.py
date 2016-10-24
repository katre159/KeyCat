import cv2
import numpy as np


def is_template_selected(template_image, area):
    template = np.asarray(template_image, dtype=np.uint8)
    img = np.asarray(area, dtype=np.uint8)

    method = eval('cv2.TM_CCOEFF_NORMED')

    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)
    threshold = 0.8
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        return True
    else:
        return False
