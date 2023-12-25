import cv2 as cv

def binarizeData(data:list):
    print("binarize data")
    for i in range(len(data)):
        _, data[i] = cv.threshold(data[i], 200, 255, cv.THRESH_BINARY)
    print("binarize data - done")
        