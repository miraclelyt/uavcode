# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 13:39:57 2020

@author: 01384599
"""

import math
def geodistance(lng1,lat1,lng2,lat2):
    lng1, lat1, lng2, lat2 = map(math.radians, [float(lng1), float(lat1), float(lng2), float(lat2)]) # 经纬度转换成弧度
    dlon=lng2-lng1
    dlat=lat2-lat1
    a=math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2 
    distance=2*math.asin(math.sqrt(a))*6371*1000 # 地球平均半径，6371km
    distance=round(distance/1000,3)
    return distance
geodistance(113.8031662,22.6529138,113.8413145,22.6672456)
#geodistance(114.7219828,26.0846054,114.7221717,26.0754419)

    

