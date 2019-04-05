import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')

from utils import *
import time
import numpy as np
import cv2
from vision.svm_classify import Identify
from strategy.moonfish.moonfish_strategy import StrategyMoonfish
from strategy.cyclone.cyclone_strategy import StrategyCyclone
from pybrobot.brobot import Brobot
import pybrobot.config as config

RED = 1
BLACK = 0

class Player:

    def __init__(self, color = RED):
        self.color = color
        
        self.board = []
        self.current_board = np.zeros(90)  #记录当前轮红棋位置
        self.last_board    = np.zeros(90)  #记录上一轮红棋位置
        self.board_w = np.array([[1, 2, 3, 4, 5, 4, 3, 2, 1],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 6, 0, 0, 0, 0, 0, 6, 0],
                                 [7, 0, 7, 0, 7, 0, 7, 0, 7],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype = np.int16)
        self.board_b = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [7, 0, 7, 0, 7, 0, 7, 0, 7],
                                 [0, 6, 0, 0, 0, 0, 0, 6, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [1, 2, 3, 4, 5, 4, 3, 2, 1]], dtype = np.int16)
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

    # 由视觉获取当前红棋局面
    def update_board_w(self, isShow = False):
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
                # assert img_sub.shape == (20, 20, 3)
                if img_sub.shape != (20, 20, 3):
                    break
                res = self.ident.chessidentify_2(img_sub)
                if res[0] == 1:
                    self.current_board[id_x + id_y*9] = 1    
                img_circle = cv2.circle(img_circle, (x,y), r, (0,0,255), 1, 8, 0)
            if isShow:
                cv2.imshow('circle', img_circle)
            # 计算移动棋子，更新last_board
            # AI吃子时，应该更新last_board -1
            # print("sum:", sum(current_board))
            if sum(self.current_board) == sum(self.last_board) or sum(self.current_board) == sum(self.last_board)-1:
                change_board = self.current_board - self.last_board
                id_new  =  np.where(change_board == 1)[0]
                id_last =  np.where(change_board == -1)[0]
                if id_new.size == 1 and id_last.size == 1:
                    # print("id: ", id_new, id_last)
                    tmp = self.board_w[id_last//9, id_last%9]
                    self.board_w[id_new//9, id_new%9] = tmp
                    self.board_w[id_last//9, id_last%9] = 0
                    self.last_board = self.current_board
                    break
        print("board_w:")
        print(self.board_w)

    # 由策略更新局面，得到机械臂运动目标
    def update_board_b(self, move, isShow = False):
        
        for i in range(10):
            for j in range(9):
                # 红棋吃子的情况
                if self.board[i][j].isupper() and self.board_b[i][j] != 0:
                    self.board_b[i][j] = 0

        new_y  = ord(move[2]) - ord('a')
        new_x  = int(move[3])
        last_y = ord(move[0]) - ord('a') 
        last_x = int(move[1])            
       
        tmp = self.board_b[last_x, last_y]
        self.board_b[new_x, new_y] = tmp
        self.board_b[last_x, last_y] = 0
        
        print("board_b:")
        print(self.board_b)

        flag_capture = False
        # 判读黑棋是否吃子
        if self.board[new_x][new_y].isupper():
            flag_capture = True

        # 如果黑棋吃子，根据capture_list更新红棋last_board
        if flag_capture:
            self.last_board[new_x*9+new_y] = 0 

        return [new_y, new_x, last_y, last_x], flag_capture

    # 由局面board生成ucci通信局面描述字符串
    def board_to_situation(self):
        adict = {1:'r', 2:'n', 3:'b', 4:'a', 5:'k', 6:'c', 7:'p', 0:'0'}
        self.board = []
        # 考虑黑子被吃子情况，先红后黑！！！
        for i in range(10):
            self.board.append([])
            for j in range(9):
                tmp = adict.get(self.board_w[i, j]).upper()
                self.board[i].append(tmp)
        for i in range(10):
            for j in range(9):
                if self.board[i][j] == '0':
                    self.board[i][j] = adict.get(self.board_b[i, j])
        # print("board_b:", self.board_b)
        # print("board_w:", self.board_w)
        import pprint
        print("board:")
        pprint.pprint(self.board)
        situation = []
        for i in range(10):
            count = 0
            for j in range(8,-1, -1):
                if self.board[i][j] != '0':
                    if count != 0:
                        situation.append(str(count))
                        situation.append(self.board[i][j])
                        count = 0
                    else:
                        situation.append(self.board[i][j])
                else:
                    count += 1
            if count != 0:
                situation.append(str(count))
            situation.append("/")
        situation = situation[:-1]
        situation.reverse()
        res = "".join(situation)
        # print(res)
        return res

if __name__ == "__main__":

    aplayer = Player()
    # amoonfish = StrategyMoonfish()
    amoonfish = StrategyCyclone()
    aplayer.initial_board()
    device = Brobot(port='com3', isShow=False)
    device.connect()
    device.set_control_signal(config.CTRL_BEGIN)
    device.set_speedrate(config.SPEEDRATE)
    device.go_ready_pos()

    while True:
        aplayer.update_board_w(isShow = True)
        cv2.waitKey(500)
        situation = aplayer.board_to_situation()
        print(situation)
        # situation = "rCbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/7C1/9/RNBAKABNR"
        move = amoonfish.get_move(position=situation, times = 10000, depth = 10, show_thinking = True)
        print(move)
        alist, flag_capture = aplayer.update_board_b(move)
        device.move(alist, capture = flag_capture, isShow=True)
        situation = aplayer.board_to_situation()
        cv2.waitKey(500)
        







