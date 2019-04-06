import sys
sys.path.append(r".\pybrobot")

from message import Message
import config

import serial
import threading
import time

def getparams(x):
        if x >= 0:
            # num = '{:0>4s}'.format(str(hex(x))[2:])
            res = bytearray([0x00, int(x/256), int(x%256), int(100*x%100)])
        else:
            x = -x
            res = bytearray([0x01, int(x/256), int(x%256), int(100*x%100)])
        # print(res)
        return res

class Brobot(threading.Thread):
    on = True
    x = 0.0
    y = 0.0
    z = 0.0
    pieceboard_id = 0

    def __init__(self, port, isShow=False):
        threading.Thread.__init__(self)
        self.isShow = isShow
        self.lock = threading.Lock()
        self.ser = serial.Serial(port,
                                 baudrate=115200,
                                 parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE,
                                 bytesize=serial.EIGHTBITS)
        is_open = self.ser.isOpen()
        if self.isShow:
            print('pydobot: %s open' % self.ser.name if is_open else 'failed to open serial port')
        self.go_ready_pos()
        self.start()

    def run(self):
        while self.on:
            self._get_pose()
            time.sleep(1)

    def close(self):
        self.on = False
        self.lock.acquire()
        self.ser.close()
        if self.isShow:
            print('pydobot: %s closed' % self.ser.name)
        self.lock.release()

    def send_command(self, msg):
        self.lock.acquire()
        self._send_message(msg)
        response = self._read_message()
        self.lock.release()
        return response

    def _send_message(self, msg):
        time.sleep(0.1)
        if self.isShow:
            print('brobot: >>', msg)
        self.ser.write(msg.bytes())

    def _read_message(self):
        time.sleep(0.1)
        messssssage = self.ser.read_all()
        # msg_len = 35 =  len("BB BB 1F 0A 50 11 01 00 84 0E 01 01 B0 5F 00 00 96 00 01 00 10 61 00 00 1C 0D 00 00 14 3D 00 00 4E 26 FB ") / 3
        if len(messssssage) < 35: #msg_len:
            return
        # print("messssssage: ", messssssage)
        whereBBBB = messssssage.find(b"\xBB\xbb")
        if len(messssssage) - whereBBBB > 35 and whereBBBB != -1:
            message = messssssage[whereBBBB:whereBBBB+35]
            # print("message: ", message)
            msg = Message(message)
            if self.isShow:
                print('brobot: <<', msg)
            return msg
        return

    def _get_pose(self):
        response = self._read_message()
        # print("response:", response)
        if response == None:
            return response
        # print("response.params: ", response.params)
        
        def getparams(params):
            x = params[1]*256 + params[2]
            x = x + params[3]/100
            # print("x:", x)
            if params[0] == 0x01:
                return -x
            return x
      
        self.x = getparams(response.params[1:5])
        self.y = getparams(response.params[5:9])
        self.z = getparams(response.params[9:13])
        if self.isShow:
            print("brobot: x:%03.2f y:%03.2f z:%03.2f " % (self.x, self.y, self.z))
       
        return response

    def print_pose(self):
        print("brobot pose: x:%03.2f y:%03.2f z:%03.2f " % (self.x, self.y, self.z))

    def connect(self):
        # 空闲未连接状态,
        # 发送 BB BB 03 00 01 01 FE, 连接机械臂
        msg = Message()
        msg.len = 3
        msg.id = 0
        msg.ctrl = 0x01
        msg.params = bytearray([0x01])
        self._send_message(msg)

    def disconnect(self):
        # 空闲连接状态,
        # 发送 BB BB 03 00 01 00 FF, 断开机械臂连接
        msg = Message()
        msg.len = 3
        msg.id = 0
        msg.ctrl = 0x01
        msg.params = bytearray([0x00])
        self._send_message(msg)

    def set_control_signal(self, signal = config.CTRL_BEGIN):
        # 设置任务 开始/暂停/继续/取消/结束 信号
        # BB BB 03 41 03 01 BB 开始
        # BB BB 03 41 03 05 B7 结束
        msg = Message()
        msg.len = 3
        msg.id = 65
        msg.ctrl = 0x03
        msg.params = bytearray([signal])
        self._send_message(msg)
    
    def set_speedrate(self, speedrate = config.SPEEDRATE):
        # 设置速率  
        # BB BB 06 42 03 00 00 01 00 BA
        msg = Message()
        msg.len = 6
        msg.id = 66
        msg.ctrl = 0x03
        msg.params = bytearray([])
        msg.params.extend(getparams(speedrate))
        self._send_message(msg)
        # ans = msg.bytes()
        # print("speed: ", ans[4:].replace(r"\0x", " "))

    def go_ptop_move(self):
        pass

    def go_door_move(self, height, pos: (float, float, float)):
        # 到某一点 door  
        # Header | Len | ID | Ctrl | Float doorheight | x           | y           | z           | CheckSum 
        # BB BB  | 12  | 48 |  04  |   00 00 1E 00    | 00 00 96 00 | 01 01 90 00 | 00 00 91 00 |   DD
        x, y, z = pos
        msg = Message()
        msg.len = 18
        msg.id = 72
        msg.ctrl = 0x04
        msg.params = bytearray([])
        msg.params.extend(getparams(height))
        msg.params.extend(getparams(x))
        msg.params.extend(getparams(y))
        msg.params.extend(getparams(z))
        # ans = msg.bytes()
        # print("door move: ", ans[4:].replace(r"\0x", " "))
        self._send_message(msg)
    
    def go_ready_pos(self):
        # 每次完成下棋运动，到按键确认位置准备
        # 回零(定义在按键位置，门型运动)
        # BB BB 12 48 04 00 00 32 00 01 00 EC 49 01 00 B4 40 00 00 94 25 9E
        msg = Message()
        msg.header   = bytes([0xBB, 0xBB])
        msg.len = 18
        msg.id = 72
        msg.ctrl = 0x04
        msg.params = bytearray([])
        height = 50
        msg.params.extend(getparams(height))
        # BB BB 12 48 04 00 00 32 00 | 01 00 C0 30 | 01 00 92 0D | 00 00 84 3A | 33
        msg.params.extend(bytearray([0x01, 0x00, 0xC0, 0x30,
                                     0x01, 0x00, 0x92, 0x0D,
                                     0x00, 0x00, 0x84, 0x3A ]))
        # command = msg.bytes() 
        # print("button: ", command[4:].replace(r"\0x", " "))
        self._send_message(msg)

    def go_air_pump(self, signal = config.PUMP_SUCK):
        # 气泵
        # 吸气   BB BB 03 BF 04 01 3C
        # 停     BB BB 03 BF 04 00 3D
        # 吹气   BB BB 03 BF 04 02 3B
        msg = Message()
        msg.len = 3
        msg.id = 191
        msg.ctrl = 0x04
        msg.params = bytearray([signal])
        self._send_message(msg)
        # ans = msg.bytes()
        # print("sucker: ", ans[4:].replace(r"\0x", " "))

    # 判断机械臂是否运动到目标点
    def isMoveOver(self , xx, yy, zz, error_value):
        count = 0
        while True:
            time.sleep(0.05)
            count += 1
            # 机械臂理论坐标误差在0.5mm以内,实际误差控制在2mm以内
            if (self.x >= xx - error_value and self.x <= xx + error_value) and (self.y >= yy - error_value and self.y <= yy + error_value) and (self.z >= zz - error_value and self.z <= zz + error_value):
                break
            if count == 600:
                print("isMoveOver too long time.")
                self.set_control_signal(config.CTRL_END)
                self.set_control_signal(config.CTRL_BEGIN)
                time.sleep(1)
                break

    # 机械臂走子：吃子 拿子 落子
    def move(self, alist, capture = False, isShow = False):
        [new_y, new_x, last_y, last_x] = alist
        new_id  = (9-new_x)*9 + new_y
        last_id = (9-last_x)*9 + last_y

        self.print_pose()
        
        # 吃子的情况
        if capture:
            idx = self.pieceboard_id
            self.pieceboard_id += 1
            (x, y) = config.CHESSBOARD[new_id]
            pos = (x, y, 135)
            self.go_door_move( 30, pos)
            self.isMoveOver(x, y, 135, 1)
            self.go_air_pump(config.PUMP_SUCK)
            time.sleep(0.5)
            (x, y) = config.PIECEBOARD[idx]
            pos = (x, y, 132)
            self.go_door_move( 30, pos)
            self.isMoveOver(x, y, 132, 1)
            self.go_air_pump(config.PUMP_STOP)

        self.print_pose()
        (x, y) = config.CHESSBOARD[last_id]
        pos = (x, y, 132)
        self.go_door_move( 30, pos)
        self.isMoveOver(x, y, 132, 1)
        self.go_air_pump(config.PUMP_SUCK)
        time.sleep(0.5)
        (x, y) = config.CHESSBOARD[new_id]
        pos = (x, y, 135)
        self.go_door_move( 30, pos)
        self.isMoveOver(x, y, 135, 1)
        self.go_air_pump(config.PUMP_STOP)
        time.sleep(0.5)
        self.go_ready_pos()
        time.sleep(5)
        if isShow:
            print("move done.")




if __name__ == "__main__":
   
    device = Brobot(port='com3', isShow=True)

    device.connect()
    device.set_speedrate(config.SPEEDRATE)
    device.set_control_signal(config.CTRL_BEGIN)
    device.go_ready_pos()
    time.sleep(5)

    # 连续查看坐标
    times = 50 #s
    for i in range(times):
        time.sleep(1)
        device.print_pose()
    
    # # 测试times次定点运动
    # times = 3
    # device.connect()
    # device.set_control_signal(config.CTRL_BEGIN)

    # for i in range(time):
    #     device.print_pose()
    #     idx = int(input("input:"))
    #     (x, y) = config.CHESSBOARD[idx]
    #     pos = (x, y, 135)
    #     device.go_door_move( 30, pos)

    # device.set_control_signal(config.CTRL_END)
    # device.disconnect()

    # # 测试times次走子运动
    # times = 3
    # device.connect()
    # device.set_control_signal(config.CTRL_BEGIN)
    # device.set_speedrate(config.SPEEDRATE)

    # for i in range(times):
    #     device.print_pose()
    #     idx = int(input("input:"))
    #     (x, y) = config.PIECEBOARD[i]
    #     pos = (x, y, 132)
    #     device.go_door_move( 30, pos)
    #     device.isMoveOver(x, y, 132, 2)
    #     device.go_air_pump(config.PUMP_SUCK)
    #     time.sleep(0.5)
    #     (x, y) = config.CHESSBOARD[idx]
    #     pos = (x, y, 135)
    #     device.go_door_move( 30, pos)
    #     device.isMoveOver(x, y, 135, 1)
    #     device.go_air_pump(config.PUMP_STOP)
    #     time.sleep(0.5)
    #     device.go_ready_pos()

    device.set_control_signal(config.CTRL_END)
    device.disconnect()
    
    
    device.close()



