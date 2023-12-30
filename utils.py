import cv2 as cv
import  pickle 
from scipy.spatial import distance
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

def resizeData(data:list, newsize:int):
    ''' resize each img from a list '''
    for i in range(len(data)):
        data[i] = cv.resize(data[i], (newsize, newsize))
    return data
    
def hamming_distance(x, y):
    return distance.hamming(x, y)

def flattenData(data):
    data = np.array(data)
    data = data.reshape(data.shape[0], -1)
    return data

def transformRect2Sqr(img, pad=10):
    height, width = img.shape
    diff = abs(height - width)
    if height > width:
        padding = ((0, 0), (diff // 2, diff - diff // 2))
    else:
        padding = ((diff // 2, diff - diff // 2), (0, 0))
    img = np.pad(img, padding, mode='constant', constant_values=0)
    top, bottom, left, right = [pad]*4
    img = cv.copyMakeBorder(img, top, bottom, left, right, cv.BORDER_CONSTANT, value=0)
    return img
    