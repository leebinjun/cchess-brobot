# 导入必要的库
import numpy as np
import cv2

from sklearn.cluster import KMeans   # 这里用scikit-learn库中的K-Means算法
import matplotlib.pyplot as plt      # 使用matplotlib显示图片
import argparse                      # 用argparse解析命令行参数

 
def centroid_histogram(clt):

    print(len(clt.labels_))
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)

    print(np.histogram(clt.labels_, bins = numLabels))
    (hist, _) = np.histogram(clt.labels_, bins = numLabels)


    hist = hist.astype("float")
    hist /= hist.sum()

    print("hist:")
    print(hist)

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


def get_feature(img_path, color_num = 3, is_show = 0):

    # 加载图片并从BGR转为RGB，matplotlib需要RGB格式
    image = cv2.imread(img_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

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



if __name__ == "__main__":
    img_path = r"0.jpg"
    get_feature(img_path, is_show = 1)
    
