from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import utils as ut
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import cv2 as cv



data = ut.loadData("data_binary")
labels = ut.loadData("labels")
test_size=0.001
print(len(data))
print(len(labels))
print(len(data)*test_size)

data = np.array(data)
data = data.reshape(data.shape[0], -1)

x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=test_size, random_state=42)

knn = KNeighborsClassifier(n_neighbors=1, metric=ut.hamming_distance)
knn.fit(data, labels)
ut.saveData("knn",knn)

predictions = knn.predict(x_test)
accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions, average='macro')

print(f'Accuracy: {accuracy}')
print(f'Precision: {precision}')










# img = cv.imread("./img/b.png", cv.IMREAD_GRAYSCALE)
# img = ut.transformRect2Sqr(img, pad=0)
# cv.imshow("1",img)
# # _, img = cv.threshold(img, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
# img = cv.resize(img, (28,28))
# cv.imshow("11",img)

# data = [img]
# data = np.array(data)
# data = data.reshape(data.shape[0], -1)
# knn = ut.loadData("knn")
# y = knn.predict(data)
# print(y)
# cv.waitKey(0)
# cv.destroyAllWindows()
