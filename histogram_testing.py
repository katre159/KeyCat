import cv2
from matplotlib import pyplot as plt

image = cv2.imread('black_dl.png', cv2.IMREAD_GRAYSCALE)
image2 = cv2.imread('green_dl.png', cv2.IMREAD_GRAYSCALE)
image3 = cv2.imread('blue_gr_dl.png', cv2.IMREAD_GRAYSCALE)
GRAY_SCALE = [0]
mask = None
FULL_SCALE = [256]
ranges = [0, 256]

hist = cv2.calcHist([image], GRAY_SCALE, mask, FULL_SCALE, ranges)
cv2.imshow('image',image)
cv2.waitKey(0)
cv2.destroyAllWindows()
plt.hist(image.ravel(),256,[0,256]); plt.show()