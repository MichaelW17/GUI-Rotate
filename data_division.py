import cv2
import os

path = 'D:/Dataset/lilscale50/origin/'
myClasses = os.listdir(path)
print(myClasses)


for i in myClasses:
    count = 0
    mydata = os.listdir(path + i)
    print('class: ', i)
    num = 0
    for j in mydata:
        num += 1
        print('num: ', num)
        img = cv2.imread(path + i + '/' + j)

        if count == 7:
            count = 0
        if count <= 4:
            cv2.imwrite('D:/Dataset/lilscale50/Train/' + i + '/' + i + '_' + str(num) + '.jpg', img)
        elif count == 5:
            cv2.imwrite('D:/Dataset/lilscale50/Val/'   + i + '/' + i + '_' + str(num) + '.jpg', img)
        elif count == 6:
            cv2.imwrite('D:/Dataset/lilscale50/Test/'  + i + '/' + i + '_' + str(num) + '.jpg', img)

        count = count + 1