import sys
import numpy as np
import cv2
import tensorflow as tf
from keras.models import load_model
from goods_dic import goods
from gui.widget.ShowGoodsWidget import ShowGoodsWidget
from efficientnet import EfficientNetB5


import v4l2
import fcntl
import os
from fcntl import ioctl
# vd = open('/dev/video0', 'r')  # 打开视频设备文件
vd = os.open('/dev/video0', os.O_RDWR, 0)
cp = v4l2.v4l2_capability()  # 查询视频设备的能力
print(fcntl.ioctl(vd, v4l2.VIDIOC_QUERYCAP, cp))
print(cp.driver)  # 驱动名字
print(cp.card)  # 设备名字
fmt = v4l2.v4l2_fmtdesc()  # 查询视频设备的能力, 支持Motion-JPEG和YUYV4:2:2
fmt.index = 1
fmt.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE
print(fcntl.ioctl(vd, v4l2.VIDIOC_ENUM_FMT, fmt))
print(fmt.index, fmt.description)
print('------------------------------------------------')
# 控制曝光
ctrl = v4l2.v4l2_control()  # 括号漏了,各种报错...
ctrl.id = v4l2.V4L2_CID_EXPOSURE_AUTO

ctrl.value = v4l2.V4L2_EXPOSURE_MANUAL  # 只能是V4L2_EXPOSURE_MANUAL 或V4L2_EXPOSURE_APERTURE_PRIORITY
fcntl.ioctl(vd, v4l2.VIDIOC_S_CTRL, ctrl)
# print('exposure auto type: ', ctrl.value)
#
# ctrl1 = v4l2.v4l2_control()
# ctrl1.id = v4l2.V4L2_CID_EXPOSURE_ABSOLUTE
# ctrl1.value = 1
# fcntl.ioctl(vd, v4l2.VIDIOC_S_CTRL, ctrl1)
# fcntl.ioctl(vd, v4l2.VIDIOC_G_CTRL, ctrl1)
# print('exposure time: ', ctrl1.value)

# ctrl2 = v4l2.v4l2_control()
# ctrl2.id = v4l2.V4L2_CID_SHARPNESS
# ctrl2.value = 0
# fcntl.ioctl(vd, v4l2.VIDIOC_S_CTRL, ctrl2)

# ctrl3 = v4l2.v4l2_control()
# ctrl3.id = v4l2.V4L2_CID_AUTO_WHITE_BALANCE
# ctrl3.value = 0
# fcntl.ioctl(vd, v4l2.VIDIOC_S_CTRL, ctrl3)

# ctrl3 = v4l2.v4l2_control()
# ctrl3.id = v4l2.V4L2_CID_WHITE_BALANCE_TEMPERATURE
# ctrl3.value = 4600
# fcntl.ioctl(vd, v4l2.VIDIOC_S_CTRL, ctrl3)
# # print("temperature: ", ctrl3.value)


os.close(vd)



graph = tf.get_default_graph()

# model = load_model('./weights-50classes-Friday_re3-26.h5')
model = load_model('./weights-51classes-Qingdao-24-DGX.h5')
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_EXPOSURE, 25)
print('exposure: ', cap.get(cv2.CAP_PROP_EXPOSURE))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
Len = 957
xPoint = 50
yPoint = 430


def open_camera():
    ret, img = cap.read()
    ret, img = cap.read()
    img = img[xPoint:xPoint + Len, yPoint:yPoint + Len]
    # cv2.imshow(' ', img)
    # cv2.waitKey(1)
    return img

#     deviceList = MV_CC_DEVICE_INFO_LIST()
#     tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE
#
#     # ch:枚举设备 | en:Enum device
#     ret = MvCamera.MV_CC_EnumDevices(tlayerType, deviceList)
#     if ret != 0:
#         print("enum devices fail! ret[0x%x]" % ret)
#         sys.exit()
#
#     if deviceList.nDeviceNum == 0:
#         print("find no device!")
#         sys.exit()
#
#     print("Find %d devices!" % deviceList.nDeviceNum)
#
#     for i in range(0, deviceList.nDeviceNum):
#         mvcc_dev_info = cast(deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
#         if mvcc_dev_info.nTLayerType == MV_GIGE_DEVICE:
#             print("\ngige device: [%d]" % i)
#             strModeName = ""
#             for per in mvcc_dev_info.SpecialInfo.stGigEInfo.chModelName:
#                 strModeName = strModeName + chr(per)
#             print("device model name: %s" % strModeName)
#
#             nip1 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0xff000000) >> 24)
#             nip2 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x00ff0000) >> 16)
#             nip3 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x0000ff00) >> 8)
#             nip4 = (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x000000ff)
#             print("current ip: %d.%d.%d.%d\n" % (nip1, nip2, nip3, nip4))
#         elif mvcc_dev_info.nTLayerType == MV_USB_DEVICE:
#             print("\nu3v device: [%d]" % i)
#             strModeName = ""
#             for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chModelName:
#                 if per == 0:
#                     break
#                 strModeName = strModeName + chr(per)
#             print("device model name: %s" % strModeName)
#
#             strSerialNumber = ""
#             for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chSerialNumber:
#                 if per == 0:
#                     break
#                 strSerialNumber = strSerialNumber + chr(per)
#             print("user serial number: %s" % strSerialNumber)
#
#
#     if int(0) >= deviceList.nDeviceNum:
#         print("intput error!")
#         sys.exit()
#
#     # ch:创建相机实例 | en:Creat Camera Object
#     cam = MvCamera()
#
#     # ch:选择设备并创建句柄 | en:Select device and create handle
#     stDeviceList = cast(deviceList.pDeviceInfo[int(0)], POINTER(MV_CC_DEVICE_INFO)).contents
#
#     ret = cam.MV_CC_CreateHandle(stDeviceList)
#     if ret != 0:
#         print("create handle fail! ret[0x%x]" % ret)
#         sys.exit()
#
#     # ch:打开设备 | en:Open device
#     ret = cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
#     if ret != 0:
#         print("open device fail! ret[0x%x]" % ret)
#         sys.exit()
#
#     # ch:设置触发模式为off | en:Set trigger mode as off
#     ret = cam.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)
#     if ret != 0:
#         print("set trigger mode fail! ret[0x%x]" % ret)
#         sys.exit()
#
#     # ch:获取数据包大小 | en:Get payload size
#     stParam = MVCC_INTVALUE()
#     memset(byref(stParam), 0, sizeof(MVCC_INTVALUE))
#
#     ret = cam.MV_CC_GetIntValue("PayloadSize", stParam)
#     if ret != 0:
#         print("get payload size fail! ret[0x%x]" % ret)
#         sys.exit()
#     nPayloadSize = stParam.nCurValue
#
#     # ch:开始取流 | en:Start grab image
#     ret = cam.MV_CC_StartGrabbing()
#     if ret != 0:
#         print("start grabbing fail! ret[0x%x]" % ret)
#         sys.exit()
#
#     data_buf = (c_ubyte * nPayloadSize)()
#     stFrameInfo = MV_FRAME_OUT_INFO_EX()
#     memset(byref(stFrameInfo), 0, sizeof(stFrameInfo))
#
#
#      # data = ser.readline()
#     # print(data)
#     ret = cam.MV_CC_GetOneFrameTimeout(byref(data_buf), nPayloadSize, stFrameInfo, 1000)
#     temp = np.array(data_buf)
#     temp = temp.reshape(1024, 1280, 3)
#
#     image = temp[96:96 + 752, 384:384 + 752]
#
#     # ch:停止取流 | en:Stop grab image
#     ret = cam.MV_CC_StopGrabbing()
#     if ret != 0:
#         print("stop grabbing fail! ret[0x%x]" % ret)
#         del data_buf
#         sys.exit()
#
#     # ch:关闭设备 | Close device
#     ret = cam.MV_CC_CloseDevice()
#     if ret != 0:
#         print("close deivce fail! ret[0x%x]" % ret)
#         del data_buf
#         sys.exit()
#
#     # ch:销毁句柄 | Destroy handle
#     ret = cam.MV_CC_DestroyHandle()
#     return image


def predict(image):
    # mean = np.array([68.270325, 64.96664, 52.150787])
    mean = np.array([49.25, 50.16, 41.96])
    image = image[140:-140, 140:-140]
    test_img = cv2.resize(image, (456, 456))
    cv2.imwrite('now.jpg', test_img)
    # cv2.imshow(' ', test_img)
    # cv2.waitKey(0)
    test_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)
    test_img = test_img - mean
    test_img = test_img.reshape(-1, 456, 456, 3)
    global graph
    with graph.as_default():
        prediction = model.predict(test_img)
    print(prediction.shape)
    max1 = np.argmax(prediction, axis=1)
    print('predict: ', max1)
    print('score：', prediction[0][max1])
    prediction[0][max1[0]] = 0
    max2 = np.argmax(prediction, axis=1)
    prediction[0][max2[0]] = 0
    max3 = np.argmax(prediction, axis=1)
    prediction[0][max3[0]] = 0
    max4 = np.argmax(prediction, axis=1)

    dict = {'1st': max1, '2nd': max2, '3rd': max3, '4th': max4}


    return dict
