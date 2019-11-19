import serial
import time
import numpy as np
from queue import Queue
command = bytes([0, 5, 2, 5, 12])

class myScale:

    def __init__(self):
        portx = "/dev/ttyUSB0"  # 端口号
        bps = 19200  # 波特率
        timex = 0.5
        self.ser = serial.Serial(portx, bps)
        self.IniWeight = 0.0
        self.state = 0
        self.weight = 0

    def Weighting(self):
        self.ser.write(command)
        bytes_result = self.ser.read(18)  # 串口返回bytes型数据
        str_result = [b for b in bytes_result]  # 先转换成16进制的字符型list
        result = np.array(str_result, dtype=np.uint16)
        weight1 = result[7] + 256 * result[6] + 256 * 256 * result[5]  # 第6~8位是重量
        weight2 = result[16] + 256 * result[15] + 256 * 256 * result[14]  # 第6~8位是重量
        if str_result[4] == 0xE3 or str_result[4] == 0x63:  # 这一位是分度值
            weight1 *= 0.001
            weight2 *= 0.001
        elif str_result[4] == 0xE4 or str_result[4] == 0x64:  # 这一位是分度值
            weight1 *= 0.002
            weight2 *= 0.002
        elif str_result[4] == 0xE5 or str_result[4] == 0x65:  # 这一位是分度值
            weight1 *= 0.005
            weight2 *= 0.005
        elif str_result[4] == 0xE6 or str_result[4] == 0x66:  # 这一位是分度值
            weight1 *= 0.01
            weight2 *= 0.01
        Total_Weight = (weight1 + weight2 - self.IniWeight)
        Total_Weight = round(Total_Weight, 2)
        if abs(Total_Weight < 0.2):
            Total_Weight = 0.0
        return Total_Weight

    def WeightState(self):
        myQueue = Queue(5)

        while 1:
            while not myQueue.full():
                myQueue.put(self.Weighting())
            myQueue.get()
            self.weight = self.Weighting()
            myQueue.put(self.weight)
            myArray = np.asarray(myQueue.queue)
            max = myArray.max()
            min = myArray.min()
            if max == min and max == 0:
                self.state = 0
            elif max != min:
                self.state = 1
            elif max == min and max != 0:
                self.state = 2
            else:
                self.state = 3
            # print('weight = ', self.weight, 'state = ', self.state)


            time.sleep(0.05)

    def setIniWeight(self):
        self.IniWeight = self.Weighting()

import serial.tools.list_ports
port_list = list(serial.tools.list_ports.comports())
for i in range(0, len(port_list)):
    #
    print(port_list[i])
# test = myScale()
# test.setIniWeight()
# test.WeightState()