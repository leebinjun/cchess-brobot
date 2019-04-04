import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')

from utils import *
import time
import numpy as np
import cv2
from vision.svm_classify import Identify



RED = 1
BLACK = 0

class Player:

    def __init__(self, color = RED):
        self.color = color
        
        self.current_board = np.zeros(90)  #记录当前轮红棋位置
        self.last_board    = np.zeros(90)  #记录上一轮红棋位置
        self.board = np.array([[1, 2, 3, 4, 5, 4, 3, 2, 1],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 6, 0, 0, 0, 0, 0, 6, 0],
                               [7, 0, 7, 0, 7, 0, 7, 0, 7],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype = np.int16)

        self.ident = Identify()
        self.cap = cv2.VideoCapture(0)
    
            
    def initial_board(self):
        # print("initial board")
        ret, img = self.cap.read()
        # 初始化board
        while ret is True:
            ret, img = self.cap.read()
            img_trans = perTrans(img)
            img_gray = cv2.cvtColor(img_trans, cv2.COLOR_BGR2GRAY)
            #霍夫变换圆检测
            circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 10,
                                       param1=40, param2=10, minRadius=19, maxRadius=20)
            #输出返回值，方便查看类型
            if type(circles) == None.__class__:
                continue
            # 更新current_board
            for circle in circles[0]:
                # 计算位置id
                x, y, r= int(circle[0]), int(circle[1]), int(circle[2])
                id_x = x // 50
                id_y = (4 - (y-230)//40) if y > 220 else (9 - (y-10)//40)
                id_x, id_y = id_x, 9-id_y
                img_sub = img_trans[y-10:y+10, x-10:x+10, :]
                res = self.ident.chessidentify_2(img_sub)
                if res[0] == 1:
                    self.last_board[id_x + id_y*9] = 1            
            # 初始化完成
            if sum(self.last_board) == 16:
                print("initial board .....\nDone.")
                break
        
    def update_board(self, isShow = False):
        ret, img = self.cap.read()
        # 更新board
        while ret is True:
            ret, img = self.cap.read()
            img_trans = perTrans(img)
            img_gray = cv2.cvtColor(img_trans, cv2.COLOR_BGR2GRAY)
            #霍夫变换圆检测
            circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 10,
                                       param1=40, param2=10, minRadius=19, maxRadius=20)
            
            img_circle = img_trans
            #输出返回值，方便查看类型
            if type(circles) == None.__class__:
                continue
            # 更新current_board
            self.current_board = np.zeros(90)  #当前轮红棋位置
            for circle in circles[0]:
                # 计算位置id
                x, y, r= int(circle[0]), int(circle[1]), int(circle[2])
                id_x = x // 50
                id_y = (4 - (y-230)//40) if y > 220 else (9 - (y-10)//40)
                id_x, id_y = id_x, 9-id_y
                img_sub = img_trans[y-10:y+10, x-10:x+10, :]
                res = self.ident.chessidentify_2(img_sub)
                if res[0] == 1:
                    self.current_board[id_x + id_y*9] = 1    
                img_circle = cv2.circle(img_circle, (x,y), r, (0,0,255), 1, 8, 0)
            if isShow:
                cv2.imshow('circle', img_circle)
            # 计算移动棋子，更新last_board
            # AI吃子时，应该更新last_board -1
            # print("sum:", sum(current_board))
            if sum(self.current_board) == sum(self.last_board):
                change_board = self.current_board - self.last_board
                id_new  =  np.where(change_board == 1)[0]
                id_last =  np.where(change_board == -1)[0]
                if id_new.size and id_last.size:
                    # print("id: ", id_new, id_last)
                    tmp = self.board[id_last//9 ,id_last%9]
                    self.board[id_new//9, id_new%9] = tmp
                    self.board[id_last//9, id_last%9] = 0
                    self.last_board = self.current_board
                    break
        print("board:")
        print(self.board)
    

if __name__ == "__main__":

    aplayer = Player()

    aplayer.initial_board()

    while True:
        aplayer.update_board()
        cv2.waitKey(500)



