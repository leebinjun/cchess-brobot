# 中国象棋程序《象棋旋风》 http://www.xqbase.com/league/xqcyclone.htm

import sys
sys.path.append(r".\strategy\cyclone")
# import time
# import os
exepath = r".\strategy\cyclone\cyclone.exe"
cmd1 = "position fen rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/4C1C1/9/RNBAKABNR b - - 0 1 "
cmd2 = "go time 20000"
# cmd2 = "ucci"
# os.system(exepath)
import time

import subprocess
subproc = subprocess.Popen([r"C:\Users\Administrator\Desktop\brobotmatch\Python\cchess-brobot\strategy\cyclone\cyclone.exe"], stdin=subprocess.PIPE,stdout=subprocess.PIPE, shell=True)
time.sleep(0.5)
print('start')
subproc.stdin.write(b'ucci\n')
# ret = subproc.communicate()
com = bytes(cmd1, encoding = "utf8")
ret = subproc.communicate(com)
print(ret)
com = bytes(cmd2, encoding = "utf8")
ret = subproc.communicate(com)
print(ret)
subproc.stdin.write(com)
time.sleep(0.5)
ret = subproc.communicate()
print(ret)
print('end')


# result = os.popen(inputstr)
# print(result.read())
# astr = result.read()
# print(astr)
    # alist = astr.split()
    # alist = alist[:1]
    # print(alist)

    