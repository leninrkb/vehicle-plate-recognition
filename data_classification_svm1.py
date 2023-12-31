from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import metrics
from sklearn.multiclass import OneVsRestClassifier
import utils as ut
import numpy as np

data = ut.loadData("data_binary")
labels = ut.loadData("labels")
data = np.array(data)
data = data.reshape(data.shape[0], -1)

x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

model = svm.SVC(C = 1, kernel='linear', verbose=True)
model.fit(x_train, y_train)

print("haciendo prediccion")
y_pred = model.predict(x_test[0:10])
y_test = y_test[0:10]
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
print("Precision:", metrics.precision_score(y_test, y_pred, average='macro'))
print("Recall:", metrics.recall_score(y_test, y_pred, average='macro'))


ut.saveData("svm1",model)
