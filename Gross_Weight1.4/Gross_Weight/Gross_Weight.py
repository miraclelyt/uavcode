4# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 16:36:02 2019
V1.1 
1.增加转换场长评估
2.增加转弯风速对推重比要求评估
3.增加爬升角指定
4.将爬升、下降过程中的航程计入总航程
5.修改线材重量系数
5.增加重量迭代初始值遍历操作
V1.2
1、增加性能计算代码，包含在任意巡航速度状态下的航程和爬升率；
2、增加输出类，将计算值输出到Excel表格中；
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
from InitialSizing import *
from Motor_sizing import *
class GROSSWIGHT(IODATA):
    """起飞总重迭代"""
    def __init__(self):
        IODATA.__init__(self)
        self.Grossmass = []
        self.Batterymass = []
        self.Enginemass = []
        self.Engfactor = []
    def cal_grossweight(self,guessmass):
        self.Weight_grossmass_kg = guessmass
        init = MISSION(self.Weight_grossmass_kg)
#        init.plotws()
        init.Wingload = self.Wingload_select
        init.TW_select = self.TW_select
        motor = MOTORSIZING()
        for i in range(1,200):
            print('############################################')
            print("This is the {:0.0f} times inter".format(i))
            self.flag = False
            init.battery_weight(self.Weight_grossmass_kg)
            mass_vt = motor.vtolmotor(init.vt_prop_radius_ture,init.P_single_motor)
            mass_prop = motor.tmotor(init.prop_radius_ture,init.TW_select,self.Weight_grossmass_kg)
            cal_grossmass_kg = init.bat_weight + mass_vt + mass_prop + self.Weight_Str_factor*self.Weight_grossmass_kg\
            +self.Weight_Wire_factor*self.Weight_grossmass_kg+ self.Weight_Payload + self.Weight_Avi_kg
            if math.fabs(self.Weight_grossmass_kg-cal_grossmass_kg)>0.15:
                self.Weight_grossmass_kg = cal_grossmass_kg
                if self.Weight_grossmass_kg>10000:
                    break
                print("The battery mass is ={:0.3f} kg".format(init.bat_weight))
                print("The VTLO Engine mass is ={:0.3f} kg".format(mass_vt))
                print("The Thrust Engine mass is ={:0.3f} kg".format(mass_prop))
                print("The updata mass is ={:0.3f} kg".format(self.Weight_grossmass_kg))
            else:
                self.bat_factor = init.bat_weight/self.Weight_grossmass_kg
                self.eng_factor = (mass_vt + mass_prop)/self.Weight_grossmass_kg
                self.Grossmass.append(self.Weight_grossmass_kg)
                self.Batterymass.append(init.bat_weight)
                self.Enginemass.append(mass_vt + mass_prop)
                self.Engfactor.append(self.eng_factor)
                self.flag = True
                self.vt_prop_radius_ture = init.vt_prop_radius_ture
                self.Engine_VT_Diskload_cal = init.Engine_Prop_Diskload_cal
                self.Wingload = init.Wingload
                self.k = init.k
                self.battery_eng = init.battery_eng
                print("Finish,the grossweight is ={:0.3f} kg".format(self.Weight_grossmass_kg))
                print("The structure mass is ={:0.3f} kg".format(self.Weight_Str_factor*self.Weight_grossmass_kg))
                print("The battery mass is ={:0.3f} kg".format(init.bat_weight))
                print("The battery factor is ={:0.3f} ".format(self.bat_factor))
                print("The VTLO Engine mass is ={:0.3f} kg".format(mass_vt))
                print("The Thrust Engine mass is ={:0.3f} kg".format(mass_prop))
                print("The Engine factor is ={:0.3f} ".format(self.eng_factor))
                print("The Wire mass is ={:0.3f} ".format(self.Weight_Wire_factor*self.Weight_grossmass_kg))
                print("The Payload factor is ={:0.3f} ".format(self.Weight_Payload/self.Weight_grossmass_kg))
                print("Cruise cl/cd is = {:0.3f}".format(self.Weight_grossmass_kg*self.Weight_g/init.thrust))
                break
if __name__ == '__main__':
    run = GROSSWIGHT()
    run.cal_grossweight(60.0)
#    Initmin = 1
#    Initmax = 60
#    guessmass = range(Initmin,Initmax,1)
#    Initguessmass = []
#    i = 0
#    x = 0
#    for m in guessmass:
#        run.cal_grossweight(guessmass[i])
#        if run.flag:
#            Initguessmass.append(guessmass[i])
#            x = x + 1
#        i = i + 1
#    print('The inter finsh {:0.0f} times'.format(x))
#    fig = plt.figure()
#    ax1 = fig.add_subplot(221)
#    ax2 = fig.add_subplot(222)
#    ax3 = fig.add_subplot(223)
#    ax4 = fig.add_subplot(224)
#    ax1.set(xlim=[Initmin,Initmax],ylim= [0,100],title = 'Grossmass VS initmass',ylabel = 'Grossmass',xlabel = 'Initmass')
#    ax1.plot(Initguessmass,run.Grossmass,linewidth = 2.0, linestyle='-',color = 'red',label= 'Grossmass')
#    ax2.set(xlim=[Initmin,Initmax],ylim= [0,100],title = 'Batterymass VS initmass',ylabel = 'Batterymass',xlabel = 'Initmass')
#    ax2.plot(Initguessmass,run.Batterymass,linewidth = 2.0, linestyle='-',color = 'green',label= 'Batterymass')   
#    ax3.set(xlim=[Initmin,Initmax],ylim= [0,100],title = 'Enginemass VS initmass',ylabel = 'Enginemass',xlabel = 'Initmass')
#    ax3.plot(Initguessmass,run.Enginemass,linewidth = 2.0, linestyle='-',color = 'gold',label= 'Enginemass')
#    ax4.set(xlim=[Initmin,Initmax],ylim= [0,1],title = 'Engfactor VS initmass',ylabel = 'Engfactor',xlabel = 'Initmass')
#    ax4.plot(Initguessmass,run.Engfactor,linewidth = 2.0, linestyle='-',color = 'black',label= 'Grossmass')    
#    plt.show()