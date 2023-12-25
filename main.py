import data_extraction as dx
import data_preparation as dp
import utils as ut
import numpy as np

data = []
labels = []
# pathDataset = "./dataset/new"
# pathDataset = "./dataset/Fnt"
# pathResizedDataset = "./dataset/new"

# dx.loadDataset(pathDataset, data, labels)
data = ut.loadData("data")
labels = ut.loadData("labels")
print(f"data type: {type(data[0])}")
# ut.imshow(data[0])
# ut.saveData("data", data)
# ut.saveData("labels", labels)


dp.binarizeData(data)
dx.writeDataset("./dataset/binary", data, labels)
# dx.resizeDataset(data, 28)
# dx.writeDataset(pathResizedDataset, data, labels)

print(len(data))
print(len(labels))