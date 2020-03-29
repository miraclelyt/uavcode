# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 19:45:27 2020

@author: 01384599
"""


###########################--------------------------------------------------------
#import math,os
#from shutil import copyfile
import re
import math
import xlwt
from tkinter import *
from tkinter import filedialog
import tkinter.messagebox

#import numpy as np
#import matplotlib.pyplot as plt

def main():
# In[]    
    def selectkmlfile():
        global kmlpath
        kmlpath = filedialog.askopenfilename(title='选择kml文件', filetypes=[('KML','*.kml'), ('All Files', '*')])
        print(kmlpath)
        text1.insert(INSERT,kmlpath)
# In[]         
    def closeThisWindow():
        root.destroy()
# In[] 
    def doProcess():
        global coordinates,kmlfilepath,planfilename
        ##########################-------------解析kml文件
        kmlpath_split=kmlpath.split('/')
        kmlpath_split_front=kmlpath_split[:-1]
        kmlfilepath=''
        for x in kmlpath_split_front:
            kmlfilepath=kmlfilepath+x
            kmlfilepath=kmlfilepath+'\\'
        kmlfilename=kmlpath_split[-1]
        planfilename=kmlpath_split[-1].split('.')
#        copyfile(kmlfilepath+kmlfilename,kmlfilepath+kmlfilename+'.txt')
        
        with open(kmlfilepath+kmlfilename,'r',encoding='utf-8') as kml:
            kmllines=kml.readlines()
        m=0
        for x in kmllines:
            if re.search('\t+<coordinates>\n',x)==None:
                m=m+1
            else:
                break
        
        coordinates=kmllines[m+1]
        coordinates=coordinates.split(' ')
        coordinates[0]=coordinates[0].strip('\t')
        if coordinates[-1]=='\n':
            coordinates.pop()
        
        for (i,x) in zip(range(len(coordinates)),tuple(coordinates)):
            coordinates[i]=x.split(',')
            
        
        
        ###########################写入plan文件
        
        
        
        n=1
        
        planheadlines=['{ \n','    "divertItems": [\n','    ],\n','    "endPoint": "--",\n','    "firmwareType": 18,\n','    "groundStation": "SFGroundControl",\n','    "items": [\n']
        
        planwpTline=['        {\n','            "autoContinue": true,\n','            "command": 22,\n',
                               '            "coordinate": [\n','                %s,\n'%coordinates[0][1],
                               '                %s,\n'%coordinates[0][0],'                50\n','            ],\n',
                               '            "doJumpId": 0,\n','            "frame": 3,\n','            "params": [\n',
                               '                15,\n','                0,\n','                0,\n','                0\n',
                               '            ],\n','            "type": "SimpleItem"\n','        },\n']
        planwpLline=['        {\n','            "autoContinue": true,\n','            "command": 21,\n',
                               '            "coordinate": [\n','                %s,\n'%coordinates[-1][1],
                               '                %s,\n'%coordinates[-1][0],'                50\n','            ],\n',
                               '            "doJumpId": %s,\n'%n,'            "frame": 3,\n','            "params": [\n',
                               '                0,\n','                0,\n','                0,\n','                0\n',
                               '            ],\n','            "type": "SimpleItem"\n','        }\n']
        plantaillines=['    ],\n','    "missionName": "--",\n','    "startPoint": "--",\n','    "version": 2,\n','    "visualId": "0,0,0"\n','}\n']
        
        
        with open(kmlfilepath+planfilename[0]+'.plan','w',encoding='utf-8') as plan:
            for x in planheadlines:
                plan.write(x)
            for x in planwpTline:
                plan.write(x)
            while n<=len(coordinates):
                planwplines=['        {\n','            "autoContinue": true,\n','            "command": 16,\n',
                               '            "coordinate": [\n','                %s,\n'%coordinates[n-1][1],
                               '                %s,\n'%coordinates[n-1][0],'                50\n','            ],\n',
                               '            "doJumpId": %s,\n'%n,'            "frame": 3,\n','            "params": [\n',
                               '                0,\n','                0,\n','                0,\n','                0\n',
                               '            ],\n','            "type": "SimpleItem"\n','        },\n']
                for x in planwplines:
                    plan.write(x)
                n=n+1
            for x in planwpLline:
                plan.write(x)
            for x in plantaillines:
                plan.write(x)
        tkinter.messagebox.showinfo('提示','已将kml文件转换为plan文件')
 # In[]        
    def geodistance():
        n=0
        distance=[]
        i=0
        while i < (len(coordinates)-1): 
            lng1, lat1, lng2, lat2 = map(math.radians, [float(coordinates[i][0]), float(coordinates[i][1]), float(coordinates[i+1][0]), float(coordinates[i+1][1])]) # 经纬度转换成弧度
            dlon=lng2-lng1
            dlat=lat2-lat1
            a=math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2 
#            distance=2*math.asin(math.sqrt(a))*6371*1000 # 地球平均半径，6371km
            distance.append(round(2*math.asin(math.sqrt(a))*6371*1000/1000,3))
            i=i+1
        distance.append(0)
#        return distance
        
        # 创建一个workbook 设置编码
        workbook = xlwt.Workbook()#encoding = 'utf-8'
        # 创建一个worksheet
        worksheet = workbook.add_sheet('航点间距')
        
        # 写入excel
        # 参数对应 行, 列, 值
#        m,n=1,1
        for (m,x) in zip(range(len(coordinates)),coordinates):
            for (n,y) in zip(range(len(x)),x):
                worksheet.write(m+1,n+1, label = y)
        
        for (m,x) in zip(range(len(distance)),distance):
            worksheet.write(m+1,len(coordinates[0])+1, label = x)
#            worksheet.write(m+1,3, label = z)
        # 保存
        workbook.save(kmlfilepath+planfilename[0]+'.xls')
        tkinter.messagebox.showinfo('提示','已生成xls文件')
        
        
        
        
        
#        coordinates_arr=np.array(coordinates)
#        fig = plt.figure(1)
#        ax = fig.gca()
#        figure = ax.plot(coordinates_arr[:,0], coordinates_arr[:,1] , c='r')
#        plt.show()
        

    #初始化
    root=Tk()

    #设置窗体标题
    root.title('Python KML TO PLAN')

    #设置窗口大小和位置
    root.geometry('500x300+570+200')


    label1=Label(root,text='请选择文件:')
    text1=Entry(root,bg='white',width=45)
    button1=Button(root,text='浏览',width=8,command=selectkmlfile)
    button2=Button(root,text='生成plan',width=8,command=doProcess)
    button3=Button(root,text='生成xls',width=8,command=geodistance)
    button4=Button(root,text='退出',width=8,command=closeThisWindow)
 

    label1.pack()
    text1.pack()
    button1.pack()
    button2.pack()
    button3.pack() 
    button4.pack() 

    label1.place(x=30,y=30)
    text1.place(x=100,y=30)
    button1.place(x=390,y=26)
    button2.place(x=110,y=80)
    button3.place(x=210,y=80)
    button4.place(x=310,y=80)
    root.mainloop() 
    

if __name__=="__main__":
    main()


