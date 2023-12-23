import os 
import cv2 as cv

def readImg(path, data:list, labels:list):
    directories = os.listdir(path)
    for dirname in directories:
        tpath = f"{path}/{dirname}"
        filenames = os.listdir(tpath)
        for filename in filenames:
            imgray = cv.imread(f"{tpath}/{filename}", cv.IMREAD_GRAYSCALE)
            data.append(imgray)
            labels.append(dirname)
    return (data, labels)