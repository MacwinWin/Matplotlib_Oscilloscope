#! /usr/bin/env python3
# coding: utf-8


import sys
import os
import random

import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QWidget, QTextBrowser, QLineEdit, QPushButton
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

from modual import animation, read, sendtest1, sendtest0
 
#using matplotlib canvas which can add to qt layout
class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=38, height=6):
        fig = Figure(figsize=(width, height))
 
        self.ax1 = fig.add_subplot(311)
        self.ax2 = fig.add_subplot(312)
        self.ax3 = fig.add_subplot(313)
        # tight layout to remove white places
        fig.set_tight_layout(True)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
 
class ApplicationWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        QMainWindow.resize(self,1500,900)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")
        self.main_widget = QtWidgets.QWidget(self)
 
        vbox = QtWidgets.QVBoxLayout(self.main_widget)
        # set canvas size
        self.canvas = MyMplCanvas(self.main_widget,width=12, height=12)

        vbox.addWidget(self.canvas)
 
        self.textBrowser = QTextBrowser(self)

        vbox.addWidget(self.textBrowser)

        self.setLayout(vbox)
        # make the cursor always focus the newset line
        self.textBrowser.textChanged.connect(lambda:self.textBrowser.moveCursor(QtGui.QTextCursor.End))
 
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        # dynamic update the plot
        self.plot = animation.animationClass(self.canvas, self)
        # read data thread
        self.read = read.readClass(self)
        self.read.start()
        # simulate send date0 thread
        self.sendtest0 = sendtest0.sendClass()
        self.sendtest0.start()
        # simulate send data1 thread
        self.sendtest1 = sendtest1.sendClass()
        self.sendtest1.start()

if __name__ == "__main__":
    App = QApplication(sys.argv)
    aw = ApplicationWindow()
    # show the max size at the beginning
    aw.showMaximized()
    App.exit()
    sys.exit(App.exec_())