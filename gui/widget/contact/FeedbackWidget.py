# coding:utf-8

from PyQt5 import QtCore, QtGui, QtWidgets
from gui.widget.customerWidget import CustomerWidget
from gui.utils import utils
import config


class FeedbackWidget(CustomerWidget):
    __instance = None

    @staticmethod
    def get_instance():
        if FeedbackWidget.__instance is None:
            FeedbackWidget.__instance = FeedbackWidget()
        return FeedbackWidget.__instance

    def __init__(self):
        super().__init__()
        self.__init_UI()

    def __init_UI(self):
        self.resize(500, 400)

        self.top_widget = QtWidgets.QWidget()
        self.center_widget = QtWidgets.QLabel()
        self.bottom_widget = QtWidgets.QWidget()
        self.bottom_background_widget = QtWidgets.QWidget()

        main_layout = QtWidgets.QGridLayout()
        main_layout.addWidget(self.top_widget, 0, 0, 1, 1)
        main_layout.addWidget(self.center_widget, 1, 0, 4, 1)
        main_layout.addWidget(self.bottom_background_widget, 5, 0, 2, 1)
        main_layout.addWidget(self.bottom_widget, 5, 0, 2, 1)
        self.setLayout(main_layout)
        # self.setContentsMargins(0, 0, 0, 0)

        utils.set_background_opacity(widget=self.bottom_background_widget, background='black', opacity=0.5)

        self.bottom_layout = QtWidgets.QGridLayout()
        self.bottom_widget.setLayout(self.bottom_layout)
        # self.bottom_widget.setStyleSheet('background: black')
        self.sub_bottom_layout = QtWidgets.QHBoxLayout()
        self.sub_bottom_layout.setAlignment(QtCore.Qt.AlignLeft)
        app_icon_label = QtWidgets.QLabel()
        app_icon_label.setFixedSize(40, 40)
        pixMap = QtGui.QPixmap(config.APP_ICON).scaled(app_icon_label.width(), app_icon_label.height())
        app_icon_label.setPixmap(pixMap)
        app_name_label = QtWidgets.QLabel(config.APP_NAME)
        app_name_label.setStyleSheet('font-family: "Microsoft YaHei"; font-size:20px; color:white')
        app_version_label = QtWidgets.QLabel(config.APP_VERSION)
        app_version_label.setStyleSheet('font-family: "Microsoft YaHei"; font-size:14px; color:gray')
        self.sub_bottom_layout.addWidget(app_icon_label)
        self.sub_bottom_layout.addWidget(app_name_label)
        self.sub_bottom_layout.addWidget(app_version_label)

        email_layout = QtWidgets.QHBoxLayout()
        email_label = QtWidgets.QLabel('联系邮箱: zhanganguo@ruijie.com.cn')
        email_label.setStyleSheet('font-family: "Microsoft YaHei"; font-size:15px; color:white')
        email_layout.addWidget(email_label)

        telephone_layout = QtWidgets.QHBoxLayout()
        telephone_label = QtWidgets.QLabel('联系电话: +86 18850712420')
        telephone_label.setStyleSheet('font-family: "Microsoft YaHei"; font-size:15px; color:white')
        telephone_layout.addWidget(telephone_label)

        address_layout = QtWidgets.QHBoxLayout()
        address_label = QtWidgets.QLabel('联系地址: 福建省福州市仓山区金山大道618号 星网锐捷科技园, 350002')
        address_label.setStyleSheet('font-family: "Microsoft YaHei"; font-size:15px; color:white')
        address_layout.addWidget(address_label)

        self.feedback_layout = QtWidgets.QGridLayout()
        self.feedback_layout.addLayout(email_layout, 0, 0, 1, 1)
        self.feedback_layout.addLayout(telephone_layout, 1, 0, 1, 1)
        self.feedback_layout.addLayout(address_layout, 2, 0, 1, 1)

        self.bottom_layout.addLayout(self.sub_bottom_layout, 0, 0, 1, 1)
        self.bottom_layout.addLayout(self.feedback_layout, 0, 1, 1, 2)

    def paintEvent(self, event):
        utils.set_background_image(self, "asset/giada.png")


