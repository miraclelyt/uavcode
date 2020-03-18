# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 22:17:23 2019

@author: 01107255
"""

import math
from aerocalc import std_atm as ISA
import numpy as np
import matplotlib
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
from mission import *
from IOdata import *
from Gross_Weight import *
import xlwt                            #导入模块
wb = xlwt.Workbook(encoding = 'ascii')  #创建新的Excel（新的workbook），建议还是用ascii编码
ws = wb.add_sheet('weng')               #创建新的表单weng
ws.write(0, 0, label = 'hello')         #在（0,0）加入hello
ws.write(0, 1, label = 'world')         #在（0,1）加入world
ws.write(1, 0, label = '你好')
wb.save('weng.xls')                     #保存为weng.xls文件

class OUTPUT(object):
    """输出总体设计参数到EXCEL表中"""
    def __init__(self):
        '''进行初步初始化'''
        