import cv2 as cv
import pickle 
import numpy as np
import matplotlib.pyplot as plt 

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

def show(mat, dim=3):
    plt.figure(figsize = (dim,dim))
    plt.axis("off")
    plt.imshow(mat, cmap = "gray")
    plt.show()
    