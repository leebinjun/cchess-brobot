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
    X, y, test_size=0.3, random_state=42
)

for D in [0.05]:
    param = D
    print("param:", param)
    import cv2
    svm = cv2.ml.SVM_create()
    svm.setType(cv2.ml.SVM_C_SVC)
    svm.setDegree(4.8)
    # Kernel（核函数）：执行数据转换，根据标签或输出找出分离数据的过程。linear rbf poly……
    svm.setKernel(cv2.ml.SVM_POLY)
    # C: 错误项的惩罚参数 C。它还控制平滑决策边界和正确分类训练点之间的权衡。
    svm.setC(1)
    # gamma：rbf 函数、Poly 函数和 S 型函数的系数。gamma 值越大，SVM 就会倾向于越准确的划分每一个训练集里的数据，这会导致泛化误差较大和过拟合问题。
    svm.setGamma(D)


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
    # for (a, b) in zip(y_test, y_pred):
    #     if a != int(b):
    #         print(a, b)



