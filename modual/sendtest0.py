#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    simulate send data0 using CAN divece
'''

import struct
import time 

from PyQt5.QtCore import QThread, pyqtSignal
from ctypes import *

class _VCI_INIT_CONFIG(Structure):
    _fields_ = [('AccCode', c_ulong),
                ('AccMask', c_ulong),
                ('Reserved', c_ulong),
                ('Filter', c_ubyte),
                ('Timing0', c_ubyte),
                ('Timing1', c_ubyte),
                ('Mode', c_ubyte)]

class _VCI_CAN_OBJ(Structure):
    _fields_ = [('ID', c_uint),
                ('TimeStamp', c_uint),
                ('TimeFlag', c_ubyte),
                ('SendType', c_ubyte),
                ('RemoteFlag', c_ubyte),
                ('ExternFlag', c_ubyte),
                ('DataLen', c_ubyte),
                ('Data', c_ubyte*8),
                ('Reserved', c_ubyte*3)]

class sendClass(QThread):
    trigger = pyqtSignal()
    def __init__(self):
        super(sendClass, self).__init__()
        self.canLib = windll.LoadLibrary('./ControlCAN.dll')
        self.vic = _VCI_INIT_CONFIG()
        self.vic.AccCode = 0x00000000
        self.vic.AccMask = 0xffffffff
        self.vic.Filter = 0
        self.vic.Timing0 = 0x01
        self.vic.Timing1 = 0x1c
        self.vic.Mode = 0 
        self.vco = _VCI_CAN_OBJ()
        self.vco.ID = 0x0700
        # set send type 2 to self send self receive, to simulate send data
        self.vco.SendType = 2
        self.vco.RemoteFlag = 0
        self.vco.ExternFlag = 1
        self.vco.DataLen = 8
        self.vco.Data = (1, 0, 0, 0, 0, 0, 0, 1)
        # init CAN device. If get '1', excution alright
        print('打开设备: %d' % (self.canLib.VCI_OpenDevice(21, 0, 0)))
        print('设置波特率: %d' % (self.canLib.VCI_SetReference(21, 0, 0, 0, \
                                pointer(c_int(0x1C0008)))))
        print('初始化: %d' % (self.canLib.VCI_InitCAN(21, 0, 0, pointer(self.vic))))
        print('启动: %d' % (self.canLib.VCI_StartCAN(21, 0, 0)))
        print('清空缓冲区: %d' % (self.canLib.VCI_ClearBuffer(21, 0, 0)))

    def run(self):
        for i in range(3000):
            data = struct.pack('>i', i)
            self.vco.Data = (data[2], data[3], data[2], data[3], data[2], data[3], data[2], data[3])
            print('发送测试0: %d' % (self.canLib.VCI_Transmit(21, 0, 0, pointer(self.vco), 1)))
            # send data in 0.1 second interval
            time.sleep(0.1)