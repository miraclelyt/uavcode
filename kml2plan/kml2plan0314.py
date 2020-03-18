# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 19:45:27 2020

@author: 01384599
"""

import math,os
from shutil import copyfile
#from folium import plugins
#import folium
import re

#filename=input('请输入文件名称（不带文件扩展名）：')
#
#filepath=input('请输入文件路径：')

kmlfilename='未命名路径'
kmlfilepath='d:\\user\\01384599\\desktop'

copyfile(kmlfilepath+'\\'+kmlfilename+'.kml',kmlfilepath+'\\'+kmlfilename+'.txt')

with open(kmlfilepath+'\\'+kmlfilename+'.txt','r',encoding='utf-8') as kml:
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



n=1

planheadlines=['{ \n','    "divertItems": [\n','    ],\n','    "endPoint": "--",\n','    "firmwareType": 18,\n','    "groundStation": "SFGroundControl",\n','    "items": [\n']
#planwplines=['        {\n','            "autoContinue": true,\n','            "command": 16,\n',
#                       '            "coordinate": [\n','                %s,\n'%coordinates[n-1][1],
#                       '                %s,\n'%coordinates[n-1][0],'                50\n','            ],\n',
#                       '            "doJumpId": %s,\n'%n,'            "frame": 3,\n','            "params": [\n',
#                       '                0,\n','                0,\n','                0,\n','                0\n',
#                       '            ],\n','            "type": "SimpleItem"\n','        },\n']
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


with open('d:\\user\\01384599\\desktop\\11111.plan','w',encoding='utf-8') as plan:
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

#    lon_lat[i]=coordinates[i].pop()
#m = folium.Map([30.1833, 120.2833], zoom_start=5)
#for (i,x) in coorndinates:
#    lon_lat
#lon_lat=coordinates[0:][:1]
#route = folium.PolyLine(
#  zuobiao,
#  weight=10,
#  color='orange',
#  opacity=0.8
#).add_to(m)
