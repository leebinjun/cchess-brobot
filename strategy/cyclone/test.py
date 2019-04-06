# 电脑象棋引擎排名表        http://www.xqbase.com/league/ranklist.htm
# 中国象棋程序《象棋旋风》  http://www.xqbase.com/league/xqcyclone.htm
# Python 3 利用 subprocess 实现管道( pipe )交互操作读/写通信 - _Suwings - 博客园 https://www.cnblogs.com/suwings/p/6216279.html


import sys
sys.path.append(r".\strategy\cyclone")

import subprocess
import time

exepath = r".\strategy\cyclone\cyclone.exe"
p = subprocess.Popen(exepath, stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
ret = p.stdout.readline()
print(ret)

p.stdin.write('position fen rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/4C2C1/9/RNBAKABNR b - - 0 1\r\n'.encode('GBK'))
p.stdin.write('go time 20000\r\n'.encode('GBK'))
p.stdin.flush()

while True:
    ret = p.stdout.readline()
    print(ret)
    if ret.decode()[:8] == 'bestmove':
        ans = ret.decode()[9:13]
        break
print("ans", ans)
