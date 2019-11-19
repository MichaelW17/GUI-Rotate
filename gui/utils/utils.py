from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect
from PyQt5 import QtGui


def set_color(widget: QWidget, color):
    painter = QtGui.QPainter(widget)
    # todo 1 设置背景颜色
    painter.setBrush(color)
    painter.drawRect(widget.rect())


def set_background_image(widget: QWidget, image_path):
    painter = QtGui.QPainter(widget)

    # todo 2 设置背景图片，平铺到整个窗口，随着窗口改变而改变
    pixmap = QtGui.QPixmap(image_path)
    painter.drawPixmap(widget.rect(), pixmap)


def set_background_opacity(widget: QWidget, background, opacity: float):
    widget.setStyleSheet('''background:'''+background+''';''')
    opacityEffect = QGraphicsOpacityEffect()
    opacityEffect.setOpacity(opacity)
    widget.setGraphicsEffect(opacityEffect)
