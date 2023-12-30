import utils as ut
import numpy as np
import cv2 as cv

knn = ut.loadData("knn")

def main(data):
    data = [ut.transformRect2Sqr(img, pad=5) for img in data]
    data = ut.resizeData(data, 28)
    for i, c in enumerate(data):
        cv.imshow(f"char: {i}", c)
        cv.imwrite(f"./img/{i}.png",c)
    data = ut.flattenData(data)
    y = knn.predict(data)
    print(y, end="\n-------\n")
    

