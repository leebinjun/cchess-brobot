# 测试视觉，输出局面
# ident.chessidentify_1(img_sub) ->[[2]] 识别棋子类别， 准确率有待提升
# ident.chessidentify_2(img_sub) ->[[1]] 识别棋子红黑
# board 为红棋局面

import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')

from utils import *
import time
import numpy as np
import cv2
from vision.svm_classify import Identify

current_board = np.zeros(90)  #记录当前轮红棋位置
last_board    = np.zeros(90)  #记录上一轮红棋位置

board = np.array([[1, 2, 3, 4, 5, 4, 3, 2, 1],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 6, 0, 0, 0, 0, 0, 6, 0],
                  [7, 0, 7, 0, 7, 0, 7, 0, 7],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype = np.int16)

def drawRect(image):
    global current_board
    global last_board   
    global board   

    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray',img_gray)
    
    #霍夫变换圆检测
    circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 10,
                               param1=40, param2=10, minRadius=19, maxRadius=20)
    #输出返回值，方便查看类型
    if type(circles) == None.__class__:
        return

    img_circle = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    current_board = np.zeros(90)  #当前轮红棋位置
    # 更新current_board
    for circle in circles[0]:
        # 计算位置id
        x, y, r = int(circle[0]), int(circle[1]), int(circle[2])
        id_x = x // 50
        id_y = (4 - (y-230)//40) if y > 220 else (9 - (y-10)//40)
        id_x, id_y = id_x, 9-id_y
        # print("id: ", id_x, id_y)

        img_sub = image[y-10:y+10, x-10:x+10, :]
        res = ident.chessidentify_2(img_sub)
        if res[0] == 1: 
            current_board[id_x + id_y*9] = 1

        img_circle = cv2.circle(img_circle, (x,y), r, (0,0,255), 1, 8, 0)

    cv2.imshow('circle', img_circle)

    # print("board:::")
    # print(current_board)
    # print(last_board)

    # 计算移动棋子，更新last_board
    # AI吃子时，应该更新last_board -1
    print("sum:", sum(current_board))
    if sum(current_board) == sum(last_board):
        change_board = current_board - last_board
        id_new  =  np.where(change_board == 1)[0]
        id_last =  np.where(change_board == -1)[0]
        if id_new.size and id_last.size:
            # print("id: ", id_new, id_last)
            # 22,19
            # print(board[id_last//9, id_last%9])
            tmp = board[id_last//9 ,id_last%9]
            board[id_new//9, id_new%9] = tmp
            board[id_last//9, id_last%9] = 0
        last_board = current_board

    print("board:")
    print(board)
   
    cv2.waitKey(500)


if __name__ == '__main__':
    
    # python .\vision\test.py  点点，确定棋盘位置并截图，
    # 更新.\cchessgame\utils.py中perTrans参数points = [(90, 463), (538, 463), (90, 23), (538, 23)]
    
    # 初始化分类器
    ident = Identify()
    # 打开摄像头
    cap = cv2.VideoCapture(0)
    ret,img = cap.read()
    # 初始化board
    while ret is True:
        ret,img = cap.read()
        image = perTrans(img)
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #霍夫变换圆检测
        circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 10,
                                param1=40, param2=10, minRadius=19, maxRadius=20)
        #输出返回值，方便查看类型
        if type(circles) == None.__class__:
            continue
        img_circle = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # 更新current_board
        for circle in circles[0]:
            # 计算位置id
            x, y, r= int(circle[0]), int(circle[1]), int(circle[2])
            id_x = x // 50
            id_y = (4 - (y-230)//40) if y > 220 else (9 - (y-10)//40)
            id_x, id_y = id_x, 9-id_y

            img_sub = image[y-10:y+10, x-10:x+10, :]
            res = ident.chessidentify_2(img_sub)
            if res[0] == 1:
                # print("iiidd:", id_x, id_y) 
                current_board[id_x + id_y*9] = 1
                last_board[id_x + id_y*9] = 1

            img_circle = cv2.circle(img_circle, (x,y), r, (0,0,255), 1, 8, 0)

        cv2.imshow('circle', img_circle)
        
        # 初始化完成
        if sum(current_board) == 16 and sum(last_board) == 16:
            print("initial board .....\nDone.")
            break


    ret,img = cap.read()
    while ret is True:
        
        cv2.imshow("imag",img)
        ret, img = cap.read()
        
        ch = cv2.waitKey(5)
        if ch == ord('q') :
            break
        if ch == ord('s') :
            print("save photo")
            # cv2.imwrite(r"C:\Users\SadAngel\Desktop\myworkplace\CCAI\Data\origin\test"+str(time.time())+'.jpg', img)
            # cv2.imwrite(r"C:\Users\SadAngel\Desktop\myworkplace\CCAI\Data\origin\test"+str(time.time())+'.jpg', img_trans)
        
        img_trans = perTrans(img)
        cv2.imshow("perTrans_rst",img_trans)

        drawRect(img_trans)

    cv2.destroyAllWindows()
