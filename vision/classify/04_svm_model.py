# 载入数据，训练svm模型

import numpy as np
from sklearn import datasets

'''载入数据'''
X_data = np.load(r'.\vision\classify\X_data.npy')
y_data = np.load(r'.\vision\classify\y_data.npy')
X = np.array(X_data)
y = np.array(y_data)

# # 降维
# print("before PCA:", X.shape)

# from sklearn.decomposition import PCA
# import numpy as np
# from sklearn.preprocessing import StandardScaler
# # feature normalization (feature scaling)
# X_scaler = StandardScaler()
# X = X_scaler.fit_transform(X)
# # PCA
# pca = PCA(n_components=0.9)# 保证降维后的数据保持90%的信息
# pca.fit(X)
# X = pca.transform(X)

# print("after PCA:", X.shape)


# print(type(X))
# print(X.shape,y.shape)
X = X.astype(np.float32)

'''分离数据'''
from sklearn import model_selection as ms
X_train, X_test, y_train, y_test = ms.train_test_split(
    X, y, test_size=0.2, random_state=42
)

for D in [4.7]:
    param = D
    print("param:", param)
    import cv2
    svm = cv2.ml.SVM_create()
    svm.setType(cv2.ml.SVM_C_SVC)
    svm.setDegree(D)
    svm.setKernel(cv2.ml.SVM_POLY)
    # svm.setKernel(cv2.ml.SVM_RBF)
    svm.setC(1)
    svm.setGamma(0.05)


    '''开始训练'''
    y_train = y_train.reshape(-1, 1)
    # print(y_train.shape)
    # print(X_train.shape)
    svm.train(X_train, cv2.ml.ROW_SAMPLE, y_train)
    svm.save(r'.\vision\classify\svmtest.mat')
    print ("Done\n")

    svm = cv2.ml.SVM_load(r'.\vision\classify\svmtest.mat')
    
    # svm2.load("svmtest.mat")
    # print(svm2)
    
    '''开始预测'''
    _, y_pred = svm.predict(X_test)
    # print(y_pred)
    # print(X_test)
    '''用scikit-learn的metrics模块计算准确率'''
    from sklearn import metrics
    print(metrics.accuracy_score(y_test, y_pred))
    for (a, b) in zip(y_test, y_pred):
        if a != int(b):
            print(a, b)



