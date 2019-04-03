# import cv2



# img = cv2.imread("1.jpg")
# img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
# HVS_hist = cv2.calcHist([img],[0,1,2],None,[16,4,4],[0,180,0,256,0,256])
# print(HVS_hist)
# HVS_hist = cv2.normalize(HVS_hist,HVS_hist).flatten()
# print(HVS_hist)


import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('0.jpg',0) #直接读为灰度图像
#opencv方法读取-cv2.calcHist（速度最快）
#图像，通道[0]-灰度图，掩膜-无，灰度级，像素范围
hist_cv = cv2.calcHist([img],[0],None,[256],[0,256])
#numpy方法读取-np.histogram()
hist_np,bins = np.histogram(img.ravel(),256,[0,256])
#numpy的另一种方法读取-np.bincount()（速度=10倍法2）
hist_np2 = np.bincount(img.ravel(),minlength=256)
plt.subplot(221),plt.imshow(img,'gray')
plt.subplot(222),plt.plot(hist_cv)
plt.subplot(223),plt.plot(hist_np)
plt.subplot(224),plt.plot(hist_np2)
plt.show()

