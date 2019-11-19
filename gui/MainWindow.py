# coding:utf-8

from PyQt5 import QtCore, QtGui, QtWidgets

import sys, os
import qtawesome
import asyncio
from gui.widget.contact.AboutSystem import AboutSystemWidget
from gui.widget.contact.FeedbackWidget import FeedbackWidget
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
import config
from camera import *
import time

image = 0


class MainUi(QtWidgets.QMainWindow):
    mouse_event_signal = QtCore.pyqtSignal(int, object)

    def __init__(self):
        super().__init__()

        self.__init_UI()

        self.original_window_geometry = self.geometry()

        self.current_active_widget = None
        self.mouse_event_signal.connect(self.__mouse_event)
        self.show_content_widget(command_id=0)

    def __init_UI(self):



        self.resize(1024, 768)
        self.setWindowIcon(QtGui.QIcon(config.APP_ICON))
        self.setWindowIconText(config.APP_NAME)
        self.setWhatsThis(config.APP_NAME)
        self.setWindowTitle(config.APP_NAME)

        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局

        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.title_widget = TitleWidget(self.mouse_event_signal)  # 顶部显示部件
        self.title_widget.setObjectName('title_widget')
        self.title_widget.setStyleSheet('''background:#C92141;''')

        self.title_layout = QtWidgets.QGridLayout()
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_layout.setSpacing(0)
        self.title_widget.setLayout(self.title_layout)

        self.bottom_widget = QtWidgets.QWidget()    # 底部部分
        self.bottom_widget.setObjectName('bottom_widget')
        self.bottom_widget.setStyleSheet('''background:#C92141''')
        self.bottom_layout = QtWidgets.QHBoxLayout()
        self.bottom_widget.setLayout(self.bottom_layout)

        self.start_button = QtWidgets.QPushButton('启  动')
        self.start_button.setObjectName('start_button')
        self.start_button.setFixedWidth(100)
        self.start_button.clicked.connect(self.start_button_clicked)
        # self.bottom_layout.addWidget(self.start_button)

        self.content_widget = QtWidgets.QWidget()
        self.content_widget.setObjectName('content_widget')
        self.content_layout = QtWidgets.QHBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_widget.setLayout(self.content_layout)

        self.main_layout.addWidget(self.title_widget, 0, 0, 1, 12)
        self.main_layout.addWidget(self.content_widget, 1, 0, 12, 12)
        self.main_layout.addWidget(self.bottom_widget, 13, 0, 1, 12)
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        self.icon_widget = QtWidgets.QWidget()  # 顶部显示控件
        self.icon_widget.setObjectName('icon_widget')
        self.icon_widget.setStyleSheet('''border-top-left-radius:10px;''')
        self.icon_layout = QtWidgets.QHBoxLayout()
        self.icon_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.icon_widget.setLayout(self.icon_layout)

        app_icon = QtWidgets.QLabel()
        app_icon.setFixedSize(40, 40)
        pixMap = QtGui.QPixmap(config.APP_ICON).scaled(app_icon.width(), app_icon.height())
        app_icon.setPixmap(pixMap)
        app_name = QtWidgets.QLabel(config.APP_NAME)
        app_name.setStyleSheet('font-family: "Microsoft YaHei"; font-size:35px;')
        self.icon_layout.addWidget(app_icon)
        self.icon_layout.addWidget(app_name)

        self.control_widget = QtWidgets.QWidget()  # 顶部控制控件
        self.control_widget.setObjectName('top_control_widget')
        self.control_widget.setStyleSheet('''border-top-right-radius:10px;''')
        self.control_layout = QtWidgets.QGridLayout()
        self.control_widget.setLayout(self.control_layout)
        self.control_widget.resize(100, 40)

        self.left_close = QtWidgets.QPushButton("")  # 关闭按钮
        self.left_visit = QtWidgets.QPushButton("")  # 空白按钮
        self.left_mini = QtWidgets.QPushButton("")  # 最小化按钮
        self.control_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.control_layout.addWidget(self.left_close, 0, 2, 1, 1)
        self.control_layout.addWidget(self.left_visit, 0, 1, 1, 1)

        self.title_layout.addWidget(self.icon_widget, 0, 0, 1, 9)
        self.title_layout.addWidget(self.control_widget, 0, 11, 1, 1)

        self.left_close.setFixedSize(20, 20)  # 设置关闭按钮的大小
        self.left_visit.setFixedSize(20, 20)  # 设置按钮大小
        self.left_mini.setFixedSize(20, 20)  # 设置最小化按钮大小
        self.left_close.setToolTip('最小化')
        self.left_visit.setToolTip('适中大小')
        self.left_mini.setToolTip('最大化')
        self.left_close.clicked.connect(self.__close_window)
        self.left_visit.clicked.connect(self.__resize_window)
        self.left_mini.clicked.connect(self.__maximal_window)

        self.setWindowOpacity(1.0)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        self.main_layout.setSpacing(0)

        self.__load_qss_stylesheet()
        self.__set_tray_function()

    def __load_qss_stylesheet(self):
        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_visit.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

        self.bottom_widget.setStyleSheet('''
            QWidget#bottom_widget{
                color:#232C51;
                background:#C92141;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-bottom-right-radius:10px;
                border-bottom-left-radius:10px;
            }
            ''')

        self.setStyleSheet('''
            QWidget#content_widget{
                background:white;
                border-top:1px solid white;
            }
            QWidget#top_widget{
                border-top:1px solid white;
                background:#87CEFA;
            }
            QPushButton#start_button{
                border: none;
                color: #FFFFFF;
                border-radius: 10px;
                min-width: 150px;
                min-height: 50px;
                background-color: #3672A4;
                font-size: 20px;
                font-family: Microsoft YaHei;
            }
            QPushButton#start_button:hover{
                background-color:#266294;
            }
        ''')

    def start_button_clicked(self):
        start_time = time.time()

        image = open_camera()
        # cv2.imshow(' ', img)
        # cv2.waitKey(1)
        test = predict(image)
        print(time.time()-start_time)
        self.current_active_widget.send_results(test)

    def __set_tray_function(self):
        self.tray = QtWidgets.QSystemTrayIcon() # 创建系统托盘对象
        self.tray.setIcon(QtGui.QIcon(config.APP_ICON))  # 设置系统托盘图标
        self.tray.setToolTip(config.APP_NAME)
        self.tray_menu = QtWidgets.QMenu(QtWidgets.QApplication.desktop())  # 创建菜单
        self.RestoreAction = QtWidgets.QAction(u'还 原 ', self, triggered=self.show)  # 添加一级菜单动作选项(还原主窗口)
        self.QuitAction = QtWidgets.QAction(u'退 出 ', self, triggered=self.close)  # 添加一级菜单动作选项(退出程序)
        self.tray_menu.addAction(self.RestoreAction)  # 为菜单添加动作
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(self.QuitAction)
        self.tray.setContextMenu(self.tray_menu)  # 设置系统托盘菜单

    def __mouse_event(self, command_id, mouseEvent):
        if command_id is 1:
            self.m_Position = mouseEvent.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            mouseEvent.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标
        elif command_id is 2:
            self.move(mouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            mouseEvent.accept()
        elif command_id is 3:
            self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def __close_window(self):
        self.showMinimized()

    def __resize_window(self):
        self.setGeometry(self.original_window_geometry)
        desktop = QtWidgets.QApplication.desktop()
        x = (desktop.width() - self.width()) // 2
        y = (desktop.height() - self.height()) // 2
        self.move(x, y)

    def __maximal_window(self):
        # 得到桌面控件
        desktop = QtWidgets.QApplication.desktop()
        # 得到屏幕可显示尺寸
        rect = desktop.screenGeometry()
        # 设置窗口尺寸
        self.setGeometry(rect)

    def execute_clicked_command(self, command_id):
        self.switch_button_style(command_id)
        self.show_content_widget(command_id)

    def switch_button_style(self, command_id):
        left_button_group = [self.left_button_video, self.left_button_1, self.left_button_2, self.left_button_3,
                             self.left_button_4, self.left_button_5, self.left_button_6, self.left_button_7,
                             self.left_button_9]
        if command_id is 0:
            for left_button in left_button_group:
                left_button.setStyleSheet('background:none')
        else:
            for left_button_index, left_button in enumerate(left_button_group):
                if left_button_index is command_id - 1:
                    left_button.setStyleSheet('background:#4A708B')
                else:
                    left_button.setStyleSheet('background:none')

    def show_content_widget(self, command_id):
        if command_id is 0:
            selected_widget_class = ShowGoodsWidget
        else:
            selected_widget_class = None

        if selected_widget_class is not None:
            if self.current_active_widget is not None:
                self.current_active_widget.hide()

            content_widget = selected_widget_class.get_instance()
            self.content_layout.addWidget(content_widget)
            self.current_active_widget = content_widget
            self.current_active_widget.show()


class TitleWidget(QtWidgets.QWidget):
    def __init__(self, mouse_event_signal):
        super().__init__()
        self.mouse_event_signal = mouse_event_signal

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.mouse_event_signal.emit(1, QMouseEvent)

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.m_flag = True
            self.mouse_event_signal.emit(2, QMouseEvent)

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.mouse_event_signal.emit(3, QMouseEvent)