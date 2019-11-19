import sys
from PyQt5 import QtWidgets
from gui.MainWindow import MainUi

import threading
import serial
# import tensorflow as tf
# from keras.models import load_model
# sys.path.append("C:\\Program Files (x86)\\MVS\\Development\\Samples\\Python\\MvImport")
# from MvCameraControl_class import *
import cv2
import numpy as np

image=np.zeros(shape=(752,752))


def start_button_clicked(self):
    print('dasdasdasdaswd')


def open_camera():
    deviceList = MV_CC_DEVICE_INFO_LIST()
    tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE

    # ch:枚举设备 | en:Enum device
    ret = MvCamera.MV_CC_EnumDevices(tlayerType, deviceList)
    if ret != 0:
        print("enum devices fail! ret[0x%x]" % ret)
        sys.exit()

    if deviceList.nDeviceNum == 0:
        print("find no device!")
        sys.exit()

    print("Find %d devices!" % deviceList.nDeviceNum)

    for i in range(0, deviceList.nDeviceNum):
        mvcc_dev_info = cast(deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
        if mvcc_dev_info.nTLayerType == MV_GIGE_DEVICE:
            print("\ngige device: [%d]" % i)
            strModeName = ""
            for per in mvcc_dev_info.SpecialInfo.stGigEInfo.chModelName:
                strModeName = strModeName + chr(per)
            print("device model name: %s" % strModeName)

            nip1 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0xff000000) >> 24)
            nip2 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x00ff0000) >> 16)
            nip3 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x0000ff00) >> 8)
            nip4 = (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x000000ff)
            print("current ip: %d.%d.%d.%d\n" % (nip1, nip2, nip3, nip4))
        elif mvcc_dev_info.nTLayerType == MV_USB_DEVICE:
            print("\nu3v device: [%d]" % i)
            strModeName = ""
            for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chModelName:
                if per == 0:
                    break
                strModeName = strModeName + chr(per)
            print("device model name: %s" % strModeName)

            strSerialNumber = ""
            for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chSerialNumber:
                if per == 0:
                    break
                strSerialNumber = strSerialNumber + chr(per)
            print("user serial number: %s" % strSerialNumber)

    nConnectionNum = input("please input the number of the device to connect:")

    if int(nConnectionNum) >= deviceList.nDeviceNum:
        print("intput error!")
        sys.exit()

    # ch:创建相机实例 | en:Creat Camera Object
    cam = MvCamera()

    # ch:选择设备并创建句柄 | en:Select device and create handle
    stDeviceList = cast(deviceList.pDeviceInfo[int(nConnectionNum)], POINTER(MV_CC_DEVICE_INFO)).contents

    ret = cam.MV_CC_CreateHandle(stDeviceList)
    if ret != 0:
        print("create handle fail! ret[0x%x]" % ret)
        sys.exit()

    # ch:打开设备 | en:Open device
    ret = cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
    if ret != 0:
        print("open device fail! ret[0x%x]" % ret)
        sys.exit()

    # ch:设置触发模式为off | en:Set trigger mode as off
    ret = cam.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)
    if ret != 0:
        print("set trigger mode fail! ret[0x%x]" % ret)
        sys.exit()

    # ch:获取数据包大小 | en:Get payload size
    stParam = MVCC_INTVALUE()
    memset(byref(stParam), 0, sizeof(MVCC_INTVALUE))

    ret = cam.MV_CC_GetIntValue("PayloadSize", stParam)
    if ret != 0:
        print("get payload size fail! ret[0x%x]" % ret)
        sys.exit()
    nPayloadSize = stParam.nCurValue

    # ch:开始取流 | en:Start grab image
    ret = cam.MV_CC_StartGrabbing()
    if ret != 0:
        print("start grabbing fail! ret[0x%x]" % ret)
        sys.exit()

    data_buf = (c_ubyte * nPayloadSize)()
    stFrameInfo = MV_FRAME_OUT_INFO_EX()
    memset(byref(stFrameInfo), 0, sizeof(stFrameInfo))
    while True:
        ret = cam.MV_CC_GetOneFrameTimeout(byref(data_buf), nPayloadSize, stFrameInfo, 1000)
        temp = np.array(data_buf)
        temp = temp.reshape(1024, 1280, 3)
        image = temp[96:96 + 752, 384:384 + 752]
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # ch:停止取流 | en:Stop grab image
    ret = cam.MV_CC_StopGrabbing()
    if ret != 0:
        print("stop grabbing fail! ret[0x%x]" % ret)
        del data_buf
        sys.exit()

    # ch:关闭设备 | Close device
    ret = cam.MV_CC_CloseDevice()
    if ret != 0:
        print("close deivce fail! ret[0x%x]" % ret)
        del data_buf
        sys.exit()

    # ch:销毁句柄 | Destroy handle
    ret = cam.MV_CC_DestroyHandle()
    if ret != 0:
        print("destroy handle fail! ret[0x%x]" % ret)


if __name__ == '__main__':
    # model = load_model('C:/Users/Super/Desktop/智能电子秤/model/resnet101_25_20190603_1805.h5')
    t1 = threading.Thread(target=open_camera, args=())
    t1.setDaemon(True)
    t1.start()

    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Smart-electronic-meter")
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())

