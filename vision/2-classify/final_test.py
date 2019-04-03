import numpy as np
from sklearn import datasets
from utils import get_feature
import cv2



if __name__ == '__main__':
    img_path = r'.\vision\2-classify\data\1\test1554022732.042874.jpg'
    X_data = []
    X_data.append(get_feature(img_path))
    
    X = np.array(X_data)

    print(type(X))
    print(X.shape)
    X = X.astype(np.float32)

    # svm = cv2.ml.SVM_create()
    # svm.load("svmtest.mat")
    svm = cv2.ml.SVM_load(r".\vision\2-classify\svmtest.mat")


    '''开始预测'''
    print(X)
    print(svm.predict(X))
    _, y_pred = svm.predict(X)
    print(y_pred)




