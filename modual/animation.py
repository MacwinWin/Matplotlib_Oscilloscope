#! /usr/bin/env python3
# coding: utf-8

'''
    dynamic update 3 plots
'''

import sys
import os

import matplotlib
from matplotlib.animation import FuncAnimation
 
class animationClass():
    def __init__(self, canvas, ui):
        self.ui = ui
        self.canvas = canvas
        self.y_voltage = []
        self.y_current = []
        self.y_power = []
        self.x_time = []
        self.on_start()
    def update_line(self, i):
        self.y_voltage = []
        self.y_current = []
        self.y_power = []
        self.x_time = []
        try:
            with open('data0.txt', 'r') as f:
                data = f.read()
                lines = data.split('\n')
                for line in lines:
                    if len(line) > 1:
                        voltage, current, power, time = line.split(',')
                        self.y_voltage.append(float(voltage))
                        self.y_current.append(float(current))
                        self.y_power.append(float(power))
                        self.x_time.append(float(time))
        except:
            print('no .txt file!')
        self.canvas.ax1.clear()
        self.canvas.ax2.clear()
        self.canvas.ax3.clear()
        self.canvas.ax1.plot(self.x_time, self.y_voltage)
        self.canvas.ax2.plot(self.x_time, self.y_current)
        self.canvas.ax3.plot(self.x_time, self.y_power)
 
    def on_start(self):
        self.ani = FuncAnimation(self.canvas.figure, self.update_line, interval=300, repeat = False)
