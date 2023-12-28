import cv2 as cv
import numpy as np
import data_preparation as dp
import pytesseract as pt
import data_preparation as dp

img = cv.imread("./img/sample.png")
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ch = dp.chars(img)
for id, im in enumerate(ch):
    cv.imshow(f"{id}",im)


cv.waitKey(0)
cv.destroyAllWindows()