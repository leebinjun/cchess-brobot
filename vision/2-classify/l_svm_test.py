# python opencv3.x中svm的模型保存与加载 - u011489887的专栏 - CSDN博客 https://blog.csdn.net/u011489887/article/details/80084338

import numpy as np
from sklearn import datasets
 
X,y = datasets.make_classification(n_samples=100,n_features=2,n_redundant=0,n_classes=2,random_state=7816)

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
svm.save("svmtest.mat")
print ("Done\n")

svm2 = cv2.ml.SVM_load("svmtest.mat")
 
# svm2.load("svmtest.mat")
# print(svm2)
'''开始预测'''
_, y_pred = svm.predict(X_test)
 
'''用scikit-learn的metrics模块计算准确率'''
from sklearn import metrics
print(metrics.accuracy_score(y_test, y_pred))

