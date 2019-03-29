'''
1 通信参数
USB转串口   COM3   115200, 8, 1, None

2 协议
指令包
                   payload
Header   Len   |   ID   Ctrl   Params   |   CheckSum

反馈包
                   payload
Header   Len   |   ID   Ctrl   Error   Params   |   CheckSum


checkSum校验
1.将负载帧（Payload）中的所有内容按照字节（8 位）的方式逐字节的相加，得到一个
结果 R（8 位）；
2. 对结果 R（8 位）求二补数，存入校验字节中。
3. 二补数：Two’s complanment 。对于一个 N 位的数字，其二补数等于 28 减去该数。

'''

import struct
import config

def str2hex(s):
    odata = 0
    su =s.upper()
    for c in su:
        tmp=ord(c)
        if tmp <= ord('9') :
            odata = odata << 4
            odata += tmp - ord('0')
        elif ord('A') <= tmp <= ord('F'):
            odata = odata << 4
            odata += tmp - ord('A') + 10
    return odata


class Message:
    def __init__(self, b=None):
        if b is None:
            self.header = bytes([0xBB, 0xBB])
            self.len = 0x00
            self.ctrl = 0x00
            self.params = bytes([])
            self.checksum = None
        else:
            self.header = b[0:2]
            self.len = b[2]
            self.id = b[3]
            self.ctrl = b[4]
            self.params = b[5:-1]
            self.checksum = b[-1:][0]

    def __repr__(self):
        return "Message()"

    def __str__(self):
        self.refresh()
        ret = "%s:%d:%d:%d:%s:%s" % (self.header.hex(), self.len, self.id, self.ctrl, self.params.hex(), self.checksum)
        return ret.upper()

    # 计算校验码，并更新长度
    def refresh(self):
        if self.checksum is None:
            self.checksum = self.id + self.ctrl
            for i in range(len(self.params)):
                self.checksum += self.params[i]
            self.checksum = self.checksum % 256
            self.checksum = 2 ** 8 - self.checksum
            self.checksum = self.checksum % 256
            self.len = 0x02 + len(self.params)

    def bytes(self):
        self.refresh()
        if len(self.params) > 0:
            command = bytearray([0xBB, 0xBB, self.len, self.id, self.ctrl])
            command.extend(self.params)
            command.append(self.checksum)
        else:
            command = bytes([0xBB, 0xBB, self.len, self.id, self.ctrl, self.checksum])
        res = ["{:0>2s}".format(hex(int(i))[2:].upper()) for i in command]
        res = 'b\\0x' + '\\0x'.join(res)
        # 本页运行调试，返回res；机械臂类调用，返回command
        if __name__ == "__main__":
            # print("command: ", command)
            return res
        else:
            # print("command: ", command)
            return command


if __name__ == "__main__":
    
    def getparams(x):
        if x >= 0:
            # num = '{:0>4s}'.format(str(hex(x))[2:])
            res = bytearray([0x00, int(x/256), int(x%256), int(100*x%100)])
        else:
            x = -x
            res = bytearray([0x01, int(x/256), int(x%256), int(100*x%100)])
        # print(res)
        return res

    # 连接机械臂
    msg = Message()
    msg.header   = bytes([0xBB, 0xBB])
    msg.len      = 3
    msg.id       = 0
    msg.ctrl     = 0x01
    msg.params   = bytes([0x01])
    # print(msg.bytes())
    command = msg.bytes()  
    print("connect: ", command[4:].replace(r"\0x", " "))

    # 按键确认位置
    msg = Message()
    msg.header   = bytes([0xBB, 0xBB])
    msg.len = 18
    msg.id = 72
    msg.ctrl = 0x04
    msg.params = bytearray([])
    height = 50
    msg.params.extend(getparams(height))
    msg.params.extend(bytearray([0x01, 0x00, 0xEC, 0x49,
                                 0x01, 0x00, 0xB4, 0x40,
                                 0x00, 0x00, 0x94, 0x25 ]))
    command = msg.bytes()
    print("button: ", command[4:].replace(r"\0x", " "))

    # 气泵
    msg = Message()
    msg.len = 3
    msg.id = 191
    msg.ctrl = 0x04
    msg.params = bytearray([0x01]) # 吸气     BB BB 03 BF 04 01 3C
    # msg.params = bytearray([0x00]) # 停     BB BB 03 BF 04 00 3D
    # msg.params = bytearray([0x02]) # 吹气   BB BB 03 BF 04 02 3B
    ans = msg.bytes()
    print("sucker: ", ans[4:].replace(r"\0x", " "))


    # 速率  
    # BB BB 06 42 03 00 00 01 00 BA
    msg = Message()
    msg.len = 6
    msg.id = 66
    msg.ctrl = 0x03
    msg.params = bytearray([])
    speedrate = 1
    msg.params.extend(getparams(speedrate))
    ans = msg.bytes()
    print("speed: ", ans[4:].replace(r"\0x", " "))


    #到某一点 door  
    # BB BB 12 48 04 00 00 1E 00 00 00 96 00 01 01 90 00 00 00 91 00 DD
    msg = Message()
    msg.len = 18
    msg.id = 72
    msg.ctrl = 0x04
    msg.params = bytearray([])
    # height,x,y,z = 50, 160, -210, 150
    height,(x,y),z = 10, config.POS_BOARD_RIGHTDOWN, 150
    msg.params.extend(getparams(height))
    msg.params.extend(getparams(x))
    msg.params.extend(getparams(y))
    msg.params.extend(getparams(z))
    ans = msg.bytes()
    print("door move: ", ans[4:].replace(r"\0x", " "))

    # TODO：@libing 不好用
    #到某一点 PtoP
    msg = Message()
    msg.len = 0x0F
    msg.id = 68
    msg.ctrl = 0x04
    msg.params = bytearray([])
    mode = 0x01
    msg.params.extend(bytearray([mode]))
    x,y,z = -100, -400, 250
    msg.params.extend(getparams(x))
    msg.params.extend(getparams(y))
    msg.params.extend(getparams(z))
    # print(msg.params)
    ans = msg.bytes()
    print("topoint move: ", ans[4:].replace(r"\0x", " "))

    #到某一点 相对当前点
    msg = Message()
    msg.len = 14
    msg.id = 71
    msg.ctrl = 0x04
    msg.params = bytearray([])
    x,y,z = 0, -10, 0
    msg.params.extend(getparams(x))
    msg.params.extend(getparams(y))
    msg.params.extend(getparams(z))
    ans = msg.bytes()
    print("relative move: ", ans[4:].replace(r"\0x", " "))







# 按键确认位置
# BB BB 1F 0A 50 01 | 01 00 EC 49 | 01 00 B4 40 | 00 00 94 25 | 01 00 34 41 00 00 43 46 00 00 33 12 00 00 0B 26 4C 

# 空闲未连接状态,
# 发送 BB BB 03 00 01 01 FE, 连接机械臂

# 空闲连接状态,
# 发送 BB BB 03 00 01 00 FF, 断开机械臂连接


# 吸气    BB BB 03 BF 04 01 3C
# 停     BB BB 03 BF 04 00 3D
# 吹气   BB BB 03 BF 04 02 3B
# 速率  
# BB BB 06 42 03 00 00 01 00 BA
# 回零
# BB BB 02 79 04 83
# 任务结束
# BB BB 03 41 03 05 B7
# 任务开始
# BB BB 03 41 03 01 BB


# 连接机械臂
# BB BB 03 00 01 01 FE
# 任务开始
# BB BB 03 41 03 01 BB
# 速率  
# BB BB 06 42 03 00 00 01 00 BA
# 回零(定义在按键位置，门型运动)
# BB BB 12 48 04 00 00 32 00 01 00 EC 49 01 00 B4 40 00 00 94 25 9E
# ptp运动(不好用)
# door运动
# BB BB 12 48 04 00 00 1E 00 00 00 64 00 01 01 90 00 00 00 91 00 0F
# 气泵
# 吸气   BB BB 03 BF 04 01 3C
# 停     BB BB 03 BF 04 00 3D
# 吹气   BB BB 03 BF 04 02 3B
# 任务结束
# BB BB 03 41 03 05 B7
# 断开机械臂连接
# BB BB 03 00 01 00 FF
