import cv2 as cv
import numpy as np

d = 5
kernel = np.ones((d,d), np.float32) / (d*d)

def binarizeData(data:list):
    print("binarize data")
    for i in range(len(data)):
        data[i] = binarize(data[i])
    print("binarize data - done")
    
def binarize(img):
    _, res = cv.threshold(img, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    return res
    
def smooth(img):
    res = cv.filter2D(img, -1, kernel)
    return res

def findRectangle(img, bin, min_area=1500, max_area=600):
    contours, _ = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    plate = None
    for contour in contours:
        area = cv.contourArea(contour)
        x, y, w, h = cv.boundingRect(contour)
        epsilon = 0.09 * cv.arcLength(contour, True)
        apx = cv.approxPolyDP(contour, epsilon, True)
        if len(apx) == 4 and area > min_area:
            plate = bin[y:y+h, x:x+w]
    return plate

def edges(img):
    edges = cv.Canny(img,100,200)
    # edges = cv.dilate(edges, None, iterations=1)
    return edges

def chars(img):
    contours, _ = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    characters = []
    for contour in contours:
        area = cv.contourArea(contour)
        if area > 10:
            x, y, w, h = cv.boundingRect(contour)
            aspect_ratio = w / h
            print(aspect_ratio)
            if 0.4 <= aspect_ratio <= 0.58:  # 9:16
                ch = img[y:y+h, x:x+w]
                characters.append(ch)
    return characters


def accent(img):
    kernel = np.array([[-1,-1,-1], 
                    [-1, 9,-1],
                    [-1,-1,-1]])
    img = cv.filter2D(img, -1, kernel)
    return img
    
    
    

        