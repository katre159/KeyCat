import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

img = cv2.imread('idea_scratch_source.png',0)
img2 = img.copy()
template = cv2.imread('restore_default.png',0)
w, h = template.shape[::-1]

start_time = time.time()
img = img2.copy()
method = eval('cv2.TM_CCOEFF_NORMED')

# Apply template Matching
res = cv2.matchTemplate(img,template,method)
threshold = 0.8
loc = np.where( res >= threshold )
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

if max_val >= threshold:
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    cv2.rectangle(img,top_left, bottom_right, 255, 2)

    print("--- %s seconds ---" % (time.time() - start_time))

    plt.subplot(121),plt.imshow(res,cmap = 'gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(img,cmap = 'gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle('cv2.TM_CCOEFF_NORMED')

    plt.show()
else:
    print('Template does not match!')