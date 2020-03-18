# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 17:34:25 2019

@author: 01107255
"""

import xlrd
#import InitialSizing

class IODATA(object):
    """读取Excel表的输入参数和将相关参数输出到EXCEL表中"""
    def __init__(self):
        '''读取EXCEL表中的所有输入参数，并将输入参数作为内建参数保存'''
        file_case='Design-parameters_2.50.xlsx'    
        data = xlrd.open_workbook(file_case)
        table = data.sheet_by_name(u'bas_info')
        cols_name = table.col_values(1)
        cols_value = table.col_values(2)
        m = len(cols_name)
        for i in range(m):
            if isinstance(cols_value[i],float):
                name = cols_name[i]
                value = str(cols_value[i])
                exec('self.'+name+'='+value)
if __name__ == '__main__':
    readxlr = IODATA()
    print(readxlr.Kmax)