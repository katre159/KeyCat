import cv2

im_gray = cv2.imread('downloads_highlight.png', cv2.IMREAD_GRAYSCALE)
(thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
cv2.imwrite('bw_downloads_highlight.png', im_bw)