# 点点，截取象棋棋盘

import time
import numpy as np
import cv2

def perTrans(img, points):
    # points: U L D R 4 points
    dst = np.float32([[0,0],[0,299],[299,0],[299,299]])
    src = np.float32(points)
    M = cv2.getPerspectiveTransform(src, dst)
    T = cv2.warpPerspective(img,M,(300,300))
    ROI = np.zeros((300,300,3),np.uint8)
    ROI[0:,0:300] = T
    cv2.imshow('rst_image', ROI)
    # return ROI

global img
global point
points = []
num = 0

def on_mouse(event, x, y, flags, param):
    global img, point, points, num
    img2 = img.copy()
    if event == cv2.EVENT_LBUTTONDOWN:         #左键点击
        point = (x, y)
        points.append(point)
        num += 1
        print(num)
        cv2.circle(img2, point, 10, (0,255,0), 5)
        cv2.imshow('image', img2)
        if num == 4:
            print(points)
            num = 0
            perTrans( img2, points)
            points.clear()

def main():
    global img
    # img = cv2.imread('test1.jpg')
    # cv2.namedWindow('image')
    # cv2.setMouseCallback('image', on_mouse)
    # cv2.imshow('image', img)
    # cv2.waitKey(0)

    cap = cv2.VideoCapture(0)
    ret,img = cap.read()
    while ret is True:
        
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', on_mouse)
        cv2.imshow('image', img)
        ret, img = cap.read()
        
        ch = cv2.waitKey(5)
        if ch == ord('q') :
            break
        if ch == ord('s') :
            print("save photo")
            cv2.imwrite(r".\vision" + '\\' + str(time.time())+'.jpg', img)
            cv2.imwrite(r".\vision" + '\\' + str(time.time())+'.jpg', img_trans)
        



if __name__ == '__main__':
    main()
