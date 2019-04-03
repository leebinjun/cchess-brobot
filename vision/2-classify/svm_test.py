import numpy as np
from sklearn import datasets
from data_pre import X_data, y_data


# X,y = datasets.make_classification(n_samples=100,n_features=2,n_redundant=0,n_classes=2,random_state=7816)
X = np.array(X_data)
y = np.array(y_data)


print(type(X))
print(X.shape,y.shape)
X = X.astype(np.float32)
y = y * 2 - 1
'''分离数据'''
from sklearn import model_selection as ms
X_train, X_test, y_train, y_test = ms.train_test_split(
    X, y, test_size=0.2, random_state=42
)
import cv2
svm = cv2.ml.SVM_create()
svm.setKernel(cv2.ml.SVM_LINEAR)
'''开始训练'''

y_train = y_train.reshape(-1, 1)
print(y_train.shape)
print(X_train.shape)
svm.train(X_train, cv2.ml.ROW_SAMPLE, y_train)
svm.save(r".\vision\2-classify\svmtest.mat")
print ("Done\n")

svm = cv2.ml.SVM_load(r".\vision\2-classify\svmtest.mat")
 
# svm2.load("svmtest.mat")
# print(svm2)
'''开始预测'''
_, y_pred = svm.predict(X_test)
print(y_pred)
print(X_test)
'''用scikit-learn的metrics模块计算准确率'''
from sklearn import metrics
print(metrics.accuracy_score(y_test, y_pred))

