import cv2
import v4l2
import fcntl
import os
import time
from fcntl import ioctl
vd = open('/dev/video0', 'r')  # 打开视频设备文件
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
# ctrl1.value = 12
# fcntl.ioctl(vd, v4l2.VIDIOC_S_CTRL, ctrl1)
# fcntl.ioctl(vd, v4l2.VIDIOC_G_CTRL, ctrl1)
# print('exposure time: ', ctrl1.value)

# ctrl2 = v4l2.v4l2_control()
# ctrl2.id = v4l2.V4L2_CID_SHARPNESS
# ctrl2.value = 0
# fcntl.ioctl(vd, v4l2.VIDIOC_S_CTRL, ctrl2)
#
# ctrl3 = v4l2.v4l2_control()
# ctrl3.id = v4l2.V4L2_CID_WHITE_BALANCE_TEMPERATURE
# fcntl.ioctl(vd, v4l2.VIDIOC_G_CTRL, ctrl3)
# print("temperature: ", ctrl3.value)


cv2.namedWindow(' ', 256)
cap = cv2.VideoCapture(0)
print(cap.get(cv2.CAP_PROP_EXPOSURE))
cap.set(cv2.CAP_PROP_EXPOSURE, 25)
print(cap.get(cv2.CAP_PROP_EXPOSURE))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
Len = 957
xPoint = 50
yPoint = 430
count = 0
while 1:



    ret, img = cap.read()

    ctrl3 = v4l2.v4l2_control()
    ctrl3.id = v4l2.V4L2_CID_WHITE_BALANCE_TEMPERATURE
    fcntl.ioctl(vd, v4l2.VIDIOC_G_CTRL, ctrl3)
    print("temperature: ", ctrl3.value)
    # print(cap.get(cv2.CAP_PROP_EXPOSURE))
    img = img[xPoint:xPoint + Len, yPoint:yPoint + Len]
    WAITKEY= cv2.waitKey(1)
    if WAITKEY == ord('q'):
        cv2.imwrite('./3/'+str(time.time())+'.jpg', img)
        cv2.waitKey(500)
        count = count + 1
        print(count)
    if WAITKEY == 27:
        cap.release()
        break
    cv2.imshow(' ', img)


os.close(vd)