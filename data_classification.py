from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import utils as ut
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import cv2 as cv



X = ut.loadData("data_binary")
y = ut.loadData("labels")

X = np.array(X)
X = X.reshape(X.shape[0], -1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

knn = KNeighborsClassifier(n_neighbors=1, metric=ut.hamming_distance)
knn.fit(X, y)
# predictions = knn.predict(X_test[0:1])

# y_test = y_test[0:1]
# accuracy = accuracy_score(y_test, predictions)
# precision = precision_score(y_test, predictions, average='macro')
# recall = recall_score(y_test, predictions, average='macro')
# f1 = f1_score(y_test, predictions, average='macro')

# print(f'Accuracy: {accuracy}')
# print(f'Precision: {precision}')
# print(f'Recall: {recall}')
# print(f'F1 Score: {f1}')

ut.saveData("knn",knn)








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
