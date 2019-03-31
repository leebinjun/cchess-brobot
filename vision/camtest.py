import numpy
import cv2
import time

if __name__ == '__main__':
    
    cap = cv2.VideoCapture(0)
    cap.set(3, 680)
    cap.set(4, 1020)
    ret,img = cap.read()
    while ret is True:
        cv2.imshow("test",img)
        ret, img = cap.read()
        ch = cv2.waitKey(1)
        if ch == ord('q') :
            break
        if ch == ord('s') :
            print("save photo")
            # cv2.imwrite(".\\Data\\origin\\"+'test'+str(time.time())+'.jpg', img)
            cv2.imwrite('test'+str(time.time())+'.jpg', img)
            
    cv2.destroyAllWindows()

