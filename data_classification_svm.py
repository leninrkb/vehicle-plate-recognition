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
svm_clf = svm.SVC(kernel='rbf', probability=True, verbose=True)
clf = OneVsRestClassifier(svm_clf, verbose=True)
clf.fit(x_train, y_train)
y_pred = clf.predict(x_test)
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
print("Precision:", metrics.precision_score(y_test, y_pred, average='macro'))
print("Recall:", metrics.recall_score(y_test, y_pred, average='macro'))


ut.saveData("svm",clf)
