
import numpy as np
import cv2
from matplotlib import pyplot as plt

queryImage = cv2.imread('test1554012104.4980133.jpg',0)
trainingImage = cv2.imread('1.png',0)

# 只使用SIFT 或 SURF 检测角点
sift = cv2.xfeatures2d.SIFT_create()
# sift = cv2.xfeatures2d.SURF_create(float(4000))
kp1, des1 = sift.detectAndCompute(queryImage,None)
kp2, des2 = sift.detectAndCompute(trainingImage,None)

# 设置FLANN匹配器参数
# algorithm设置可参考https://docs.opencv.org/3.1.0/dc/d8c/namespacecvflann.html
indexParams = dict(algorithm=0, trees=5)
searchParams = dict(checks=50)
# 定义FLANN匹配器
flann = cv2.FlannBasedMatcher(indexParams,searchParams)
# 使用 KNN 算法实现匹配
matches = flann.knnMatch(des1,des2,k=2)

# 根据matches生成相同长度的matchesMask列表，列表元素为[0,0]
matchesMask = [[0,0] for i in range(len(matches))]

# 去除错误匹配
for i,(m,n) in enumerate(matches):
    if m.distance < 0.7*n.distance:
        matchesMask[i] = [1,0]

# 将图像显示
# matchColor是两图的匹配连接线，连接线与matchesMask相关
# singlePointColor是勾画关键点
drawParams = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   matchesMask = matchesMask,
                   flags = 0)
resultImage = cv2.drawMatchesKnn(queryImage,kp1,trainingImage,kp2,matches,None,**drawParams)
plt.imshow(resultImage,),plt.show()
