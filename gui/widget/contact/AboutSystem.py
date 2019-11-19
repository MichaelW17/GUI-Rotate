# coding:utf-8

from PyQt5 import QtCore, QtGui, QtWidgets
from gui.utils import utils
from gui.widget.customerWidget import CustomerWidget
import config


class AboutSystemWidget(CustomerWidget):
    __instance = None

    @staticmethod
    def get_instance():
        if AboutSystemWidget.__instance is None:
            AboutSystemWidget.__instance = AboutSystemWidget()
        return AboutSystemWidget.__instance

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
        self.sub_bottom_layout = QtWidgets.QHBoxLayout()
        self.sub_bottom_layout.setAlignment(QtCore.Qt.AlignLeft)
        app_icon_label = QtWidgets.QLabel()
        app_icon_label.setFixedSize(40, 40)
        pixMap = QtGui.QPixmap(config.APP_ICON).scaled(app_icon_label.width(), app_icon_label.height())
        app_icon_label.setPixmap(pixMap)
        app_name_label = QtWidgets.QLabel(config.APP_NAME)
        app_name_label.setStyleSheet('font-family: "Microsoft YaHei"; font-size:20Spx; color:white')
        app_version_label = QtWidgets.QLabel(config.APP_VERSION)
        app_version_label.setStyleSheet('font-family: "Microsoft YaHei"; font-size:14px; color:gray')
        self.sub_bottom_layout.addWidget(app_icon_label)
        self.sub_bottom_layout.addWidget(app_name_label)
        self.sub_bottom_layout.addWidget(app_version_label)

        self.supplyer_name_label = QtWidgets.QLabel('GIADA信息技术 // 支持：锐捷网络股份有限公司 人工智能GROUP')
        self.supplyer_name_label.setStyleSheet('font-family: "Microsoft YaHei"; font-size:15px; color:gray')
        self.supplyer_name_label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

        self.bottom_layout.addLayout(self.sub_bottom_layout, 0, 0, 1, 1)
        self.bottom_layout.addWidget(self.supplyer_name_label, 0, 1, 1, 2)

    def paintEvent(self, event):
        utils.set_background_image(self, "asset/giada.png")


