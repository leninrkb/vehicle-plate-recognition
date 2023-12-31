import cv2 as cv
import  pickle 
import numpy as np

def imshow(mat):
    cv.imshow("IMG", mat)
    cv.waitKey(0)
    cv.destroyAllWindows()
    
def saveData(path, data):
    tpath = f"{path}.pkl"
    with open(tpath, "wb")as f:
        pickle.dump(data, f)
        
def loadData(path):
    tpath = f"{path}.pkl"
    data = None
    with open(tpath, "rb") as f:
        data = pickle.load(f)
    return data
    