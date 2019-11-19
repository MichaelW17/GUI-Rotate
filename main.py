import sys
from PyQt5 import QtWidgets
from gui.MainWindow import MainUi
import serial
import cv2
import numpy as np


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())


