import os 
import shutil
import cv2 as cv

def loadDataset(path, data:list, labels:list):
    ''' Read and load gray scale img '''
    print("loading data set")
    directories = os.listdir(path)
    for dirname in directories:
        tpath = f"{path}/{dirname}"
        filenames = os.listdir(tpath)
        for filename in filenames:
            imgray = cv.imread(f"{tpath}/{filename}", cv.IMREAD_GRAYSCALE)
            data.append(imgray)
            labels.append(dirname)
        print(f"loading current dir: {dirname}")
    print("loading data set - done")
        
def createEmptyDir(path):
    ''' create new dir, if exits delete current and create new empty one'''
    print("create empty dir")
    if os.path.isdir(path):
        shutil.rmtree(path)
        os.mkdir(path)
    else:
        os.mkdir(path)
    print("create empty dir - done")
    
    
def writeDataset(path, data:list, labels:list):
    ''' write dataset on specified dir '''
    createEmptyDir(path)
    print("writting dataset")
    datalen = len(data)
    labelslen = len(labels)
    if not datalen == labelslen:
        print(f"[ERROR]: check data. data: {datalen} ; labels: {labelslen}")
        return
    number = 1
    last = labels[0]
    for i in range(len(data)):
        current = labels[i]
        if not last == current:
            number = 1
            last = current
        tpath = f"{path}/{current}"
        if not os.path.isdir(tpath):
            os.mkdir(tpath)
            print(f"writting dir: {current}")
        tpath = f"{tpath}/{number}.png"
        cv.imwrite(tpath, data[i])
        number += 1
    print("writting dataset - done")
        
    
    