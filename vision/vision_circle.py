# 调整霍夫圆环检测参数
# trackbar参数范围待调整，否则会导致cv2.HoughCircles参数错误

from __future__ import print_function
import cv2 as cv
import cv2 as cv2
import argparse


min_value = 1
max_value = 200

minDist = 10
param1  = 10
param2  = 10
minRadius = 10
maxRadius = 20


param1_name = 'minDist'
param2_name = 'param1'
param3_name = 'param2'
param4_name = 'minRadius'
param5_name = 'maxRadius'

def on_param1_thresh_trackbar(val):
    global minDist
    minDist = max(val, 0)
    cv.setTrackbarPos(param1_name, window_detection_name, minDist)

def on_param2_thresh_trackbar(val):
    global param1
    param1 = max(val, 0)
    cv.setTrackbarPos(param2_name, window_detection_name, param1)

def on_param3_thresh_trackbar(val):
    global param2
    param2 = max(val, 0)
    cv.setTrackbarPos(param3_name, window_detection_name, param2)

def on_param4_thresh_trackbar(val):
    global minRadius
    global maxRadius
    minRadius = val
    minRadius = min(maxRadius-1, minRadius)
    cv.setTrackbarPos(param4_name, window_detection_name, minRadius)

def on_param5_thresh_trackbar(val):
    global minRadius
    global maxRadius
    maxRadius = val
    maxRadius = max(maxRadius, minRadius+1)
    cv.setTrackbarPos(param5_name, window_detection_name, maxRadius)

parser = argparse.ArgumentParser(description='Code for Thresholding Operations using inRange tutorial.')
parser.add_argument('--camera', help='Camera devide number.', default=0, type=int)
args = parser.parse_args()

cap = cv.VideoCapture(args.camera)

window_trackbar_name = "Params"
cv.namedWindow(window_trackbar_name)
cv.createTrackbar(param1_name, window_trackbar_name, min_value, max_value, on_param1_thresh_trackbar)
cv.createTrackbar(param2_name, window_trackbar_name, min_value, max_value, on_param2_thresh_trackbar)
cv.createTrackbar(param3_name, window_trackbar_name, min_value, max_value, on_param3_thresh_trackbar)
cv.createTrackbar(param4_name, window_trackbar_name, min_value, max_value, on_param4_thresh_trackbar)
cv.createTrackbar(param5_name, window_trackbar_name, min_value, max_value, on_param5_thresh_trackbar)

while True:
    ## [while]
    ret, frame = cap.read()
    if frame is None:
        break

    ret, img = cap.read()
    # cv2.imshow('1',img)
    #降噪（模糊处理用来减少瑕疵点）
    # result = cv2.blur(img, (5,5))
    # cv2.imshow('2',result)
    #灰度化,就是去色（类似老式照片）
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # cv2.imshow('3',gray)
    
    #param1的具体实现，用于边缘检测   
    # canny = cv2.Canny(img, 40, 80)  
    # cv2.imshow('4', canny) 
    
    #霍夫变换圆检测
    a,b,c,d,e = minDist, param1, param2, minRadius, maxRadius
    # circles= cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,10,param1=40,param2=20,minRadius=15,maxRadius=20)
    # cv2.HoughCircles(image, method, dp, minDist, circles=None, param1=None, param2=None, minRadius=None, maxRadius=None)
    circles= cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,a,param1=b,param2=c,minRadius=d,maxRadius=e)
    #输出返回值，方便查看类型
    print(circles)
    if type(circles) == None.__class__:
        continue

    #输出检测到圆的个数
    print(len(circles[0]))
 
    #根据检测到圆的信息，画出每一个圆
    for circle in circles[0]:
        #圆的基本信息
        print(circle[2])
        #坐标行列(就是圆心)
        x=int(circle[0])
        y=int(circle[1])
        #半径
        r=int(circle[2])
        #在原图用指定颜色圈出圆，参数设定为int所以圈画存在误差
        img=cv2.circle(img,(x,y),r,(0,0,255),1,8,0)
    #显示新图像
    cv2.imshow('Result',img)
 
    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        break

cv2.destroyAllWindows()
        





