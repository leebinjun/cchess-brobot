import numpy as np
from utils import get_feature_1, get_feature_2
import cv2
import time

class Identify():
    
    _instance = None
    
    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Identify, cls).__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self, 
                 svm_1_path = r".\vision\svm_1.mat",
                 svm_2_path = r".\vision\svm_2.mat"):
        print("载入模型")
        print("start time:", time.time())
        if svm_1_path:
            self.svm_1 = cv2.ml.SVM_load(svm_1_path)
        if svm_2_path:
            self.svm_2 = cv2.ml.SVM_load(svm_2_path)
        print("end time:", time.time())

    def chessidentify_1(self, image):
        # 识别棋子
        '''开始预测'''
        X_data = []
        X_data.append(get_feature_1(None, img = image))
        X = np.array(X_data)
        X = X.astype(np.float32)
        # print(X)
        # print("start time:", time.time())
        _, y1_pred = self.svm_1.predict(X)
        # print(y1_pred)
        # print("end time:", time.time())
        return y1_pred
  
    def chessidentify_2(self, image):
        # 红黑二分类
        X_data = []
        X_data.append(get_feature_2(None, img = image))
        X = np.array(X_data)
        X = X.astype(np.float32)
        # print(X)
        # print("start time:", time.time())
        _, y2_pred = self.svm_2.predict(X)
        # print(y2_pred)
        # print("end time:", time.time())

        return y2_pred




if __name__ == '__main__':
   
    img_path = r".\vision\test1554290784.3382103.jpg"
    
    ident = Identify()
    
    img = cv2.imread(img_path)

    ret1, ret2 = ident.chessidentify_1(img)
    print("ret:", ret1, ret2)
