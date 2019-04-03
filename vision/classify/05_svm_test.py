import cv2
import numpy as np

def LBP(image):
    W, H = image.shape                    #获得图像长宽
    xx = [-1,  0,  1, 1, 1, 0, -1, -1]
    yy = [-1, -1, -1, 0, 1, 1,  1,  0]    #xx, yy 主要作用对应顺时针旋转时,相对中点的相对值.
    res = np.zeros((W - 2, H - 2),dtype="uint8")  #创建0数组,显而易见维度原始图像的长宽分别减去2，并且类型一定的是uint8,无符号8位,opencv图片的存储格式.
    for i in range(1, W - 2):
        for j in range(1, H - 2):
            temp = ""
            for m in range(8):
                Xtemp = xx[m] + i    
                Ytemp = yy[m] + j    #分别获得对应坐标点
                if image[Xtemp, Ytemp] > image[i, j]: #像素比较
                    temp = temp + '1'
                else:
                    temp = temp + '0'
            #print int(temp, 2)
            res[i - 1][j - 1] =int(temp, 2)   #写入结果中
    return res

def SIFT(image):
    sift = cv2.xfeatures2d.SIFT_create()
    kp, des = sift.detectAndCompute(image, None)
    # print("kp, des: ", kp, des)
    return des

def HOG(image):
    winSize = (20,20)
    blockSize = (2,2)
    blockStride = (1,1)
    cellSize = (2,2)
    nbins = 9
    derivAperture = 1
    winSigma = 4.
    histogramNormType = 0
    L2HysThreshold = 2.0000000000000001e-01
    gammaCorrection = 0
    nlevels = 64
    hog = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nbins,derivAperture,winSigma,
                            histogramNormType,L2HysThreshold,gammaCorrection,nlevels)
    #compute(img[, winStride[, padding[, locations]]]) -> descriptors
    winStride = (2,2)
    padding = (2,2)
    locations = ((0,0),)
    hist = hog.compute(image,winStride,padding,locations)
    return hist

def get_feature(filepath):
    img = cv2.imread(filepath, 0)
    lbp = LBP(img)
    hog = HOG(img)
    sift = SIFT(img)
    # print(hog)
    # feature = np.hstack((lbp.flatten(), hog.flatten())) #将矩阵转换为一维数组
    feature = hog.flatten() #将矩阵转换为一维数组
    return feature


if __name__ == '__main__':
    img_path = r".\vision\classify\data\50\test1554022823.2650917.jpg"
    X_data = []
    X_data.append(get_feature(img_path))
    
    X = np.array(X_data)

    print(type(X))
    print(X.shape)
    X = X.astype(np.float32)

    # svm = cv2.ml.SVM_create()
    # svm.load("svmtest.mat")
    svm = cv2.ml.SVM_load(r".\vision\classify\svmtest.mat")


    '''开始预测'''
    import time
    print(X)
    print("start time:", time.time())
    print(svm.predict(X))
    _, y_pred = svm.predict(X)
    print(y_pred)
    print("end time:", time.time())


