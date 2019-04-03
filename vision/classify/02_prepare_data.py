# 开摄像头，找圆，截图，准备数据



import cv2
import argparse

cap = cv2.VideoCapture(0)
cap.set(3, 640)
print(cap.get(3))
cap.set(4, 480)
ret,img = cap.read()
while ret is True:
    
    ret, img = cap.read()
    print(img.shape)
    cv2.imshow("origin",img)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray',img_gray)
    
    #霍夫变换圆检测
    circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 10,
                               param1=40, param2=10, minRadius=19, maxRadius=20)
    # #输出返回值，方便查看类型
    # print(circles)
    if type(circles) == None.__class__:
        continue

    #输出检测到圆的个数
    # print(len(circles[0]))
 
    img_circle = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #根据检测到圆的信息，画出每一个圆
    for circle in circles[0]:
        #圆的基本信息
        # print(circle)
        #坐标行列(就是圆心)
        x, y, r= int(circle[0]), int(circle[1]), int(circle[2])
        #在原图用指定颜色圈出圆，参数设定为int所以圈画存在误差
        img_circle = cv2.circle(img_circle, (x,y), r, (0,0,255), 1, 8, 0)
    #显示新图像
    cv2.imshow('circle', img_circle)
 

    key = cv2.waitKey(2)
    if key == ord('q') or key == 27:
        break

    if key == ord('s'): # 截图获取数据sssssssss
        #根据检测到圆的信息，画出每一个圆
        for circle in circles[0]:
            # circle = circles[0][1]
            #圆的基本信息
            print(circle[2])
            #坐标行列(就是圆心)
            x, y = int(circle[0]), int(circle[1])
            #在原图用指定颜色圈出圆，参数设定为int所以圈画存在误差
            print(img.shape)
            img_sub=img[y-10:y+10, x-10:x+10, :]
            import time
            cv2.imwrite(r"test"+str(time.time())+'.jpg', img_sub)
        cv2.imshow('sub',img_sub)
    
cv2.destroyAllWindows()

