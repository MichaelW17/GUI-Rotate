# coding:utf-8

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel

from gui.utils import utils
from gui.widget.customerWidget import CustomerWidget
import goods_dic
import config
import time
import camera
from PyQt5.QtCore import *
from scaling_sensor import *
import threading


class BtnLabel(QLabel):

    def __init__(self, parent=None):
        super(BtnLabel, self).__init__(parent)
        self.if_mouse_press = False
        self.first_candidate_image_path = ' '
        self.now_candidate_image_path = ' '
        self.first_candidate_price = 0
        self.now_candidate_price = 0
        self.first_candidate_name = ' '
        self.now_candidate_name = ' '
        self.changeFlag = 0

    def mousePressEvent(self, e):
        if self.first_candidate_image_path != ' ':
            jpg = QtGui.QPixmap(self.first_candidate_image_path).scaled(self.width(), self.height())
            self.setPixmap(jpg)
            self.changeFlag = 1

    def changePath(self, path1, path2):
        self.first_candidate_image_path = path1
        self.now_candidate_image_path = path2

    def changePrice(self, price1, price2):
        self.first_candidate_price = price1
        self.now_candidate_price = price2

    def changeName(self, name1, name2):
        self.first_candidate_name = name1
        self.now_candidate_name = name2

    def pathChange(self):
        path = self.first_candidate_image_path
        self.first_candidate_image_path = self.now_candidate_image_path
        self.now_candidate_image_path = path

        price = self.first_candidate_price
        self.first_candidate_price = self.now_candidate_price
        self.now_candidate_price = price

        name = self.first_candidate_name
        self.first_candidate_name = self.now_candidate_name
        self.now_candidate_name = name

    def changeFirstPath(self, path, price, name):
        self.first_candidate_image_path = path
        self.first_candidate_price = price
        self.first_candidate_name = name

class ShowGoodsWidget(CustomerWidget):
    sku_price_title_label: QLabel
    sku_weight_title_label: QLabel
    __instance = None

    @staticmethod
    def get_instance():
        if ShowGoodsWidget.__instance is None:
            ShowGoodsWidget.__instance = ShowGoodsWidget()
        return ShowGoodsWidget.__instance

    def __init__(self):
        super().__init__()
        self.__init_UI()
        self._setStylesheet()

        self.Scale = myScale()
        self.Scale.setIniWeight()

        t1 = threading.Thread(target=self.Scale.WeightState, args=())
        t1.setDaemon(True)
        t1.start()

        t2 = threading.Thread(target=self.UpdateGUI, args=())
        t2.setDaemon(True)
        t2.start()

    def UpdateGUI(self):
        Trigger = 0
        while 1:
            self.sku_weight_label.setText(str(self.Scale.weight) + 'kg')
            if self.Scale.state == 0:
               self.set_image(self.first_candidate_image,'welcome.jpg')
               self.set_image(self.second_candidate_image, 'blank.jpg')
               self.set_image(self.third_candidate_image, 'blank.jpg')
               self.set_image(self.forth_candidate_image, 'blank.jpg')
               self.set_name(self.sku_name_label, ' ')
               self.set_name(self.sku_price_label, '0.0元')

               Trigger = 0
            if self.Scale.state == 2 and Trigger == 0:
                start_time = time.time()
                image = camera.open_camera()
                test = camera.predict(image)
                print(time.time() - start_time)
                self.send_results(test, self.Scale.weight)
                Trigger = 1

            if self.second_candidate_image.changeFlag == 1:
                self.set_name(self.sku_price_label, str(self.second_candidate_image.now_candidate_price)+'元')
                self.set_image(self.first_candidate_image, self.second_candidate_image.now_candidate_image_path)
                self.set_name(self.sku_name_label, self.second_candidate_image.now_candidate_name)

                self.third_candidate_image.changeFirstPath(self.second_candidate_image.now_candidate_image_path, self.second_candidate_image.now_candidate_price, self.second_candidate_image.now_candidate_name)
                self.forth_candidate_image.changeFirstPath(self.second_candidate_image.now_candidate_image_path, self.second_candidate_image.now_candidate_price, self.second_candidate_image.now_candidate_name)
                self.second_candidate_image.pathChange()
                self.second_candidate_image.changeFlag = 0

            elif self.third_candidate_image.changeFlag == 1:
                self.set_name(self.sku_price_label, str(self.third_candidate_image.now_candidate_price)+'元')
                self.set_image(self.first_candidate_image, self.third_candidate_image.now_candidate_image_path)
                self.set_name(self.sku_name_label, self.third_candidate_image.now_candidate_name)
                self.second_candidate_image.changeFirstPath(self.third_candidate_image.now_candidate_image_path, self.third_candidate_image.now_candidate_price, self.third_candidate_image.now_candidate_name)
                self.forth_candidate_image.changeFirstPath(self.third_candidate_image.now_candidate_image_path, self.third_candidate_image.now_candidate_price, self.third_candidate_image.now_candidate_name)
                self.third_candidate_image.pathChange()
                self.third_candidate_image.changeFlag = 0

            elif self.forth_candidate_image.changeFlag == 1:
                self.set_name(self.sku_price_label, str(self.forth_candidate_image.now_candidate_price)+'元')
                self.set_name(self.sku_name_label, self.forth_candidate_image.now_candidate_name)
                self.set_image(self.first_candidate_image, self.forth_candidate_image.now_candidate_image_path)
                self.second_candidate_image.changeFirstPath(self.forth_candidate_image.now_candidate_image_path, self.forth_candidate_image.now_candidate_price, self.forth_candidate_image.now_candidate_name)
                self.third_candidate_image.changeFirstPath(self.forth_candidate_image.now_candidate_image_path, self.forth_candidate_image.now_candidate_price, self.forth_candidate_image.now_candidate_name)
                self.forth_candidate_image.pathChange()
                self.forth_candidate_image.changeFlag = 0


    def __init_UI(self):
        self.resize(1024, 768)
        self.left_widget = QtWidgets.QWidget()
        self.right_widget = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QGridLayout()
        self.content_layout.addWidget(self.left_widget, 0, 0, 1, 3)
        self.content_layout.addWidget(self.right_widget, 0, 3, 1, 3)
        self.setLayout(self.content_layout)

        self.left_layout = QtWidgets.QGridLayout()
        self.right_layout = QtWidgets.QGridLayout()
        self.left_widget.setLayout(self.left_layout)
        self.right_widget.setLayout(self.right_layout)

        self.first_candidate_image = QtWidgets.QLabel()
        self.first_candidate_image.setFixedSize(430, 430)
        # self.set_image(self.first_candidate_image, 'asset/sku/1.jpg')  # 临时样例，请修改
        self.second_candidate_image = BtnLabel()
        self.second_candidate_image.setFixedSize(120, 120)
        # self.set_image(self.second_candidate_image, 'asset/sku/2.jpg')
        self.third_candidate_image = BtnLabel()
        self.third_candidate_image.setFixedSize(120, 120)
        # self.set_image(self.third_candidate_image, 'asset/sku/3.jpg')
        self.forth_candidate_image = BtnLabel()
        self.forth_candidate_image.setFixedSize(120, 120)
        # self.set_image(self.forth_candidate_image, 'asset/sku/4.jpg')
        self.left_layout.addWidget(self.first_candidate_image, 0, 0, 3, 3, alignment=Qt.AlignCenter)
        self.left_layout.addWidget(self.second_candidate_image, 3, 0, 1, 1, alignment=Qt.AlignCenter)
        self.left_layout.addWidget(self.third_candidate_image, 3, 1, 1, 1, alignment=Qt.AlignCenter)
        self.left_layout.addWidget(self.forth_candidate_image, 3, 2, 1, 1, alignment=Qt.AlignCenter)


        self.sku_name_title_label = QtWidgets.QLabel('品名：')
        self.sku_name_title_label.setObjectName('title_label')

        self.sku_name_label = QtWidgets.QLabel(' ')
        self.sku_name_label.setObjectName('content_label')
        self.sku_name_title_label.setFixedHeight(80)
        self.sku_name_label.setFixedHeight(80)



        self.sku_weight_title_label = QtWidgets.QLabel('重量：')
        self.sku_weight_title_label.setObjectName('title_label')
        self.sku_weight_label = QtWidgets.QLabel(' ')
        self.sku_weight_label.setObjectName('content_label')
        self.sku_weight_title_label.setFixedHeight(80)
        self.sku_weight_label.setFixedSize(350,80)


        self.sku_price_title_label = QtWidgets.QLabel('总价:')
        self.sku_price_title_label.setObjectName('title_label')
        self.sku_price_label = QtWidgets.QLabel(' ')
        self.sku_price_label.setObjectName('content_label')
        self.sku_price_title_label.setFixedHeight(80)
        self.sku_price_label.setFixedHeight(80)

        self.sku_name_title_label.setStyleSheet(
            "QLabel{background-color:#DADADA;"
            "border:0px groove gray;border-radius:20px;padding:2px 4px;}")

        self.sku_name_label.setStyleSheet(
            "QLabel{background-color:#DADADA;"
            "border:0px groove gray; border-radius:20px;padding:2px 4px;}")

        self.sku_weight_title_label.setStyleSheet(
            "QLabel{background-color:#DADADA;"
            "border:0px groove gray; border-radius:20px;padding:2px 4px;}")

        self.sku_weight_label.setStyleSheet(
            "QLabel{background-color:#DADADA;"
            "border:0px groove gray; border-radius:20px;padding:2px 4px;}")

        self.sku_price_title_label.setStyleSheet(
            "QLabel{background-color:#DADADA;"
            "border:0px groove gray; border-radius:20px;padding:2px 4px;}")

        self.sku_price_label.setStyleSheet(
            "QLabel{background-color:#DADADA;"
            "border:0px groove gray; border-radius:20px;padding:2px 4px;}")

        # self.right_layout.addWidget(QtWidgets.QLabel(), 0, 2, 1, 6)

        self.right_layout.addWidget(self.sku_name_title_label, 1, 2, 2, 6)
        self.right_layout.addWidget(self.sku_name_label, 1, 6, 2, 6)

        self.right_layout.addWidget(self.sku_weight_title_label, 3, 2, 2, 6)
        self.right_layout.addWidget(self.sku_weight_label, 3, 6, 2, 6)
        # self.right_layout.addWidget(QtWidgets.QLabel(), 6, 2, 2, 6)

        self.right_layout.addWidget(self.sku_price_title_label, 5, 2, 2, 6)
        self.right_layout.addWidget(self.sku_price_label, 5, 6, 2, 6)

        self.Ruijie_label = QtWidgets.QLabel()
        self.right_layout.addWidget(self.Ruijie_label, 7, 7, 2, 6)
        self.Ruijie_label.setFixedSize(230, 40)
        self.set_image(self.Ruijie_label, 'ruijie.jpg')

    def send_results(self, goods, weight):

        """
        :param weight:
        :param goods: 检测结果，包含了最可能的商品，以及后续有可能的三种其它商品，格式为：{
            '1st': {'score': xx.xx, 'id': adsadsad23},
            '2nd' {'score'....}}
        }]
        :return:
        """

        first_candidate = goods['1st']
        first_candidate_info = self.get_goods_info_by_id(first_candidate)
        self.set_image(self.first_candidate_image, first_candidate_info['path'])
        # h, w, c = image.shape
        # image = np.transpose(image, (1, 0, 2)).copy()
        # image = QtGui.QImage(image.data, w, h, 3*w, QtGui.QImage.Format_RGB888).rgbSwapped()
        # self.first_candidate_image.setPixmap(QtGui.QPixmap.fromImage(image).scaled(self.first_candidate_image.width(), self.first_candidate_image.height()))
        self.set_name(self.sku_name_label, first_candidate_info['name'])

        self.set_name(self.sku_price_label, str(round(first_candidate_info['price'] * weight, 2)) + '元')

        # 20191106: force refresh
        # 得到桌面控件
        desktop = QtWidgets.QApplication.desktop()
        # 得到屏幕可显示尺寸
        rect = desktop.screenGeometry()
        # 设置窗口尺寸
        self.setGeometry(rect)

        second_candidate = goods['2nd']
        second_candidate_info = self.get_goods_info_by_id(second_candidate)
        self.set_image(self.second_candidate_image, second_candidate_info['path'])

        third_candidate = goods['3rd']
        third_candidate_info = self.get_goods_info_by_id(third_candidate)
        self.set_image(self.third_candidate_image, third_candidate_info['path'])

        fourth_candidate = goods['4th']
        fourth_candidate_info = self.get_goods_info_by_id(fourth_candidate)
        self.set_image(self.forth_candidate_image, fourth_candidate_info['path'])


        self.second_candidate_image.changePath(first_candidate_info['path'], second_candidate_info['path'])
        self.third_candidate_image.changePath(first_candidate_info['path'], third_candidate_info['path'])
        self.forth_candidate_image.changePath(first_candidate_info['path'], fourth_candidate_info['path'])

        self.second_candidate_image.changePrice(first_candidate_info['price'], second_candidate_info['price'])
        self.third_candidate_image.changePrice(first_candidate_info['price'], third_candidate_info['price'])
        self.forth_candidate_image.changePrice(first_candidate_info['price'], fourth_candidate_info['price'])

        self.second_candidate_image.changeName(first_candidate_info['name'], second_candidate_info['name'])
        self.third_candidate_image.changeName(first_candidate_info['name'], third_candidate_info['name'])
        self.forth_candidate_image.changeName(first_candidate_info['name'], fourth_candidate_info['name'])










    def get_goods_info_by_id(self, id):
        # print(goods_dic.goods[str(id[0])][1])
        # print(goods_dic.goods[str(id[0])][0])
        goods_info = {'name': goods_dic.goods[str(id[0])][1], 'path': goods_dic.goods[str(id[0])][0], 'price': goods_dic.goods[str(id[0])][2]}
        return goods_info

    def set_image(self, label, image_path):
        jpg = QtGui.QPixmap(image_path).scaled(label.width(), label.height())
        label.setPixmap(jpg)

    def set_name(self, label, name):
        label.setText(name)

    def _setStylesheet(self):
        self.setStyleSheet(
            '''
            QLabel#content_label{
                font-size:38px;
                font-family: Microsoft YaHei;
            }
            QLabel#title_label{
                font-size: 38px;
                font-family: Microsoft YaHei;
            }
            QLabel#title{
                font-size: 60px;
                font-family: Microsoft YaHei;
            }
            '''
        )

