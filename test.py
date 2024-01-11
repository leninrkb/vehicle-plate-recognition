from tensorflow.keras.models import load_model
import data_preparation as dp
import cv2 as cv
import utils as ut
def find_key(item):
    for key, _item in classes.items():
        if item == _item:
            return key
def predict(img):
    ut.show(img[0])
    y = loaded_model.predict(img)
    y = y.tolist()
    y = y[0]
    ids = list(range(36))
    y = list(zip(y, ids))
    y = sorted(y, key = lambda y: y[0])
    print(y[-1])
    r = find_key(y[-1][1])
    print(r)

classes = ut.loadData("./models/classes")
print(classes)
# ann 5 works well
# ann 6 works well
loaded_model = load_model("./models/ann_6")
loaded_model.summary()
img = cv.imread("/home/lenin/Documents/chars/b2.png", cv.IMREAD_GRAYSCALE)
_, img = cv.threshold(img, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
img = dp.prepare_img(img)
predict(img)
