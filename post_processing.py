import utils as ut
import data_preparation as dp
import numpy as np
import cv2 as cv
import tensorflow as tf
from tensorflow.keras.models import load_model

# model = ut.loadData("./models/augmented_knn")
# model = ut.loadData("./models/knn")
# model = ut.loadData("./models/svm_poly")
# model = ut.loadData("svm_rbf")
model = load_model("./models/ann_7")
classes = ut.loadData("./models/classes")


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

def find_key(item):
    for key, _item in classes.items():
        if item == _item:
            return key
        
def ann_predict(data):
    data = [dp.transformRect2Sqr(img, pad=2) for img in data]
    dp.resizeData(data, 28)
    for i, c in enumerate(data):
        cv.imshow(f"char: {i}", c)
        cv.imwrite(f"./img/{i}.png",c)
    plate = []
    for mat in data:
        y = model.predict(np.array([mat], dtype=np.uint8))
        y = y.tolist()
        y = y[0]
        ids = list(range(36))
        y = list(zip(y, ids))
        y = sorted(y, key = lambda y: y[0])
        r = find_key(y[-1][1])
        plate.append(r)
    print(plate)
        
    

