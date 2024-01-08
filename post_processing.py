import utils as ut
import data_preparation as dp
import numpy as np
import cv2 as cv

model = ut.loadData("./augmented_knn")
# model = ut.loadData("knn")
# model = ut.loadData("svm_poly")
# model = ut.loadData("svm_rbf")

def main(data):
    print("starting classifier...")
    data = [dp.accent(img) for img in data]
    data = [dp.transformRect2Sqr(img, pad=10) for img in data]
    dp.resizeData(data, 28)
    for i, c in enumerate(data):
        cv.imshow(f"char: {i}", c)
        cv.imwrite(f"./img/{i}.png",c)
    data = dp.flattenData(data)
    y = model.predict(data)
    print(y)
    

