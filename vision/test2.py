
import time
import numpy as np
import cv2
from svm_classify import Identify

def perTrans(img, points = [(88, 475), (538, 475), (88, 38), (538, 38)]):
    # points: U L D R 4 points
    dst = np.float32([[0,0],[0,439],[439,0],[439,439]])
    src = np.float32(points)
    M = cv2.getPerspectiveTransform(src, dst)
    T = cv2.warpPerspective(img,M,(440,440))
    ROI = np.zeros((440,440,3),np.uint8)
    ROI[0:,0:440] = T
    return ROI


def drawRect(image):
    
    board = np.zeros((9, 10, 3))
    board_ret = np.zeros((9, 10))
    
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray',img_gray)
    
    #霍夫变换圆检测
    circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 10,
                               param1=40, param2=10, minRadius=19, maxRadius=20)
    #输出返回值，方便查看类型
    if type(circles) == None.__class__:
        return

    img_circle = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    for circle in circles[0]:
        print(circle)
        x, y, r= int(circle[0]), int(circle[1]), int(circle[2])
        # 计算位置id
        id_x = x // 50
        id_y = (4 - (y-230)//40) if y > 220 else (9 - (y-10)//40)
        print("id", id_x, id_y)

        # img_sub = image[y-10:y+10, x-10:x+10, :]
        # res = ident.chessidentify_2(img_sub)
        # print(res)
        
        # board[id_x][id_y] = res[0]

        img_circle = cv2.circle(img_circle, (x,y), r, (0,0,255), 1, 8, 0)
        # import time
        # cv2.imwrite(r".\vision\classify\data\test" +str(time.time())+'.jpg', img_sub)

    cv2.imshow('circle', img_circle)


    # print("board:")
    # print(board_ret)
   
    # cv2.waitKey(3000)




if __name__ == '__main__':
    
    ident = Identify()

    cap = cv2.VideoCapture(0)
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

