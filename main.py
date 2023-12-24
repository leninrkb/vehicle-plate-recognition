import data_extraction as dx
import numpy as np

data = []
labels = []
pathDataset = "./dataset/Fnt"
pathResizedDataset = "./dataset/new"

dx.loadDataset(pathDataset, data, labels)
dx.resizeDataset(data, 28)
dx.writeDataset(pathResizedDataset, data, labels)

print(len(data))
print(len(labels))