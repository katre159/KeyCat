import cv2
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

img = cv2.imread('sublime.png')

edges = cv2.Canny(img, 210, 255)
copy = edges.copy()

img2, contours, hierarchy = cv2.findContours(copy, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

image = 0

for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True) #Removes tiny deviations, tries to go for straight lines.
    if len(approx) == 4: #Lines, should be square.
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 10:
            print("Width and height: ", w, h)
            image = img[y:y+h, x:x+w]

cv2.imshow('image', img)
cv2.imshow('edges', edges)
cv2.imshow('area', image)

gray_area = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
(thresh, im_bw) = cv2.threshold(gray_area, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
cv2.imwrite('area.png', image)

textImage = Image.open('area.png')

text = pytesseract.image_to_string(textImage)

print(text)

cv2.waitKey(0)
cv2.destroyAllWindows()