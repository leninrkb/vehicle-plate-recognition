import data_extraction as dx
import numpy as np

data = []
labels = []
dx.readImg("./dataset/Fnt", data, labels)

print(len(data))
print(len(labels))