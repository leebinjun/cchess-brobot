# 导入必要的库
import numpy as np
import cv2

from sklearn.cluster import KMeans   # 这里用scikit-learn库中的K-Means算法
import matplotlib.pyplot as plt      # 使用matplotlib显示图片
import argparse                      # 用argparse解析命令行参数

 
# feature2 用于提取颜色信息，区分红黑子
def centroid_histogram(clt):

    # print(len(clt.labels_))
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)

    # print(np.histogram(clt.labels_, bins = numLabels))
    (hist, _) = np.histogram(clt.labels_, bins = numLabels)


    hist = hist.astype("float")
    hist /= hist.sum()

    # print("hist:")
    # print(hist)

    return hist
 
def plot_colors(hist, centroids):

    bar = np.zeros((50, 300, 3), dtype = "uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
            color.astype("uint8").tolist(), -1)
        startX = endX

    return bar

def get_feature_2(img_path, img = None, color_num = 3, is_show = 0):

    if img_path == None:
        image = img
    else:
        # 加载图片
        image = cv2.imread(img_path)
    
    if type(image) == None.__class__:
        print("get_feature_2: input is None")
        return

    #从BGR转为RGB，matplotlib需要RGB格式
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    if type(image) == None.__class__:
        print("get_feature_2: input is None")
        return
        
    # 把mxn的矩阵像素转为一维像素
    image = image.reshape((image.shape[0] * image.shape[1], 3))
 
    # 使用KMeans算法找到图片的主要颜色
    clt = KMeans(n_clusters = color_num)
    clt.fit(image)
 
    # 绘制主要颜色条
    hist = centroid_histogram(clt)
    # print(hist)
    # print(clt.cluster_centers_)
    bar = plot_colors(hist, clt.cluster_centers_)
 
    # 显示
    if is_show == 1:
        # 显示原始图片
        plt.figure()
        plt.axis("off")
        plt.imshow(image)

        plt.figure()
        plt.axis("off")
        plt.imshow(bar)
        plt.show()

    # print(np.vstack((clt.cluster_centers_, hist)))
    fea =  np.vstack((clt.cluster_centers_, hist*255))
    fea = fea.flatten()
    # print(fea)
    return fea


# feature1 用于提取hog特征，区分类别
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

def get_feature_1(img_path, img = None):
    if img_path == None:
        #从BGR转为RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # print(img.shape)
    else:
        img = cv2.imread(img_path, 0)

    if type(img) == None.__class__:
        print("get_feature_1: input is None")
        return

    lbp = LBP(img)
    hog = HOG(img)
    sift = SIFT(img)
    # print(hog)
    # feature = np.hstack((lbp.flatten(), hog.flatten())) #将矩阵转换为一维数组
    feature = hog.flatten() #将矩阵转换为一维数组
    return feature

if __name__ == "__main__":
    img_path = r".\vision\test1554290784.3382103.jpg"
    get_feature_2(img_path, is_show = 1)
    get_feature_1(img_path)
    
