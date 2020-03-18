#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 19:44:20 2019

@author: 01107255
"""
import math
from aerocalc import std_atm as ISA
import numpy as np
import matplotlib
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
from IOdata import *

class InitialSizing(IODATA):
    """用于飞机地毯图绘制"""        
##########################################
#                 画图函数                # 
##########################################
    def __init__(self):
        #继承IODATA的变量
        IODATA.__init__(self)
        self.k = 1.0/4.0/self.Cd0/self.Kmax**2
        print ('cdi factor k={:0.3f}'.format(self.k))
        self.cl_design = 2.0*self.Kmax*self.Cd0
        print ('cl_design={:0.3f}'.format(self.cl_design))
        self.Ae_ = 4.0*self.Cd0*self.Kmax**2/3.1415/0.65
        print ('Ae_design={:0.1f}'.format(self.Ae_)) 
    def ConstraintPoly(WSl,TWl,Col,al):
        """绘制界限图块"""
        WSl.append(WSl[-1])
        TWl.append(0)
        WSl.append(0)
        TWl.append(0)
        WSl.append(0)
        TWl.append(TWl[-3])
        zp = [*zip(WSl,TWl)]
        pa = matplotlib.patches.Polygon(zp,closed=True,color=Col,alpha = al)
        return pa
    def PlotSetUp(Xmin, Xmax, Ymin, Ymax, Xlabel, Ylabel):
        """建立坐标轴"""
        pylab.ylim([Ymin,Ymax])
        pylab.xlim([Xmin,Xmax])
        pylab.ylabel(Ylabel)
        pylab.xlabel(Xlabel)
    def plotws(self): 
        """绘制地毯图主程序"""
#################################################
#                   计算密度                     #
################################################
        SeaLevelDens_kgm3 = ISA.alt2density(0,alt_units='m',density_units='kg/m**3')
        print ('ISA density at Sea level elevation: {:0.3f} kg/m^3'.format(SeaLevelDens_kgm3))
        ClimbAltDens_kgm3 = ISA.alt2density(self.ROCAlt_m,alt_units='m',density_units='kg/m**3')
        print ('ISA density at the climb constraint altitude: {:0.3f} kg/m^3'.format(ClimbAltDens_kgm3))
        CruisingAltDens_kgm3 = ISA.alt2density(self.CruisingAlt_m,alt_units='m',density_units='kg/m**3')
        print ('ISA density at cruising altitude: {:0.3f} kg/m^3'.format(CruisingAltDens_kgm3))
        TopOfFinalAppDens_kgm3 = ISA.alt2density(self.App_Alt_m,alt_units='m', density_units='kg/m**3')
        print ('ISA density at the top of the final approach: {:0.3f} kg/m^3'.format(TopOfFinalAppDens_kgm3))
        CVTClimbDens_kgm3 = ISA.alt2density(self.CVTClimbAlt_m,alt_units='m', density_units='kg/m**3')
        print ('ISA density at the CVTClimb approach: {:0.3f} kg/m^3'.format(CVTClimbDens_kgm3))
#################################################
#                   气动参数计算                  #
################################################
        self.StallSpeed_mpsIAS = self.ApproachSpeed_mpsIAS/self.ApproachSpeed2Stall
        print ('StallSpeed_mpsIAS={:0.1f} Pa'.format(self.StallSpeed_mpsIAS))
        q_cruise_Pa = 0.5*SeaLevelDens_kgm3*(self.CruisingSpeed_Maxavliable_mpsIAS**2)
        print ('qcruise={:0.1f} Pa'.format(q_cruise_Pa))
        q_cruise_design_Pa = 0.5*SeaLevelDens_kgm3*(self.CruisingSpeed_Design_mpsIAS**2)
        q_climb_Pa = 0.5*SeaLevelDens_kgm3*(self.ClimbSpeed_mpsIAS**2)
        print ('qclimb={:0.1f} Pa'.format(q_climb_Pa))
        q_CVT_Pa = 0.5*SeaLevelDens_kgm3*(self.CVTSpeed_mpsIAS**2)
        print ('qCVT={:0.1f} Pa'.format(q_CVT_Pa))
        q_Stall_Pa = 0.5*SeaLevelDens_kgm3*self.StallSpeed_mpsIAS**2
        print ('q_stall={:0.1f} Pa'.format(q_Stall_Pa))
        q_CVTClimb_Pa = 0.5*SeaLevelDens_kgm3*self.CVTClimbSpeed_mpsIAS**2
        print ('q_stall={:0.1f} Pa'.format(q_Stall_Pa))
        self.CruisingSpeed_Design_mpsTAS = self.CruisingSpeed_Design_mpsIAS*math.sqrt(SeaLevelDens_kgm3\
                                                      /CruisingAltDens_kgm3)
        print ('CruisingSpeed_mpsTAS={:0.1f} m/s'.format(self.CruisingSpeed_Design_mpsTAS))
        self.CVTSpeed_mpsTAS = self.CVTSpeed_mpsIAS*math.sqrt(SeaLevelDens_kgm3\
                                                      /CVTClimbDens_kgm3)
        print ('CVTSpeed_mpsTAS={:0.1f} m/s'.format(self.CVTSpeed_mpsTAS))
        self.ClimbSpeed_mpsTAS = self.ClimbSpeed_mpsIAS*math.sqrt(SeaLevelDens_kgm3\
                                                      /ClimbAltDens_kgm3)
        print ('ClimbSpeed_mpsTAS={:0.1f} m/s'.format(self.ClimbSpeed_mpsTAS))
        self.StallSpeed_mpsTAS =self.StallSpeed_mpsIAS*math.sqrt(SeaLevelDens_kgm3\
                                                      /TopOfFinalAppDens_kgm3)
        print ('StallSpeed_mpsTAS={:0.1f} m/s'.format(self.StallSpeed_mpsTAS))
        self.CVTClimbSpeed_mpsTAS = self.CVTClimbSpeed_mpsIAS*math.sqrt(SeaLevelDens_kgm3/CVTClimbDens_kgm3)
        print ('CVTClimbSpeed_mpsTAS={:0.1f}m/s'.format(self.CVTClimbSpeed_mpsTAS))
        self.n_cvt_ = math.sqrt((self.CVTSpeed_mpsTAS**2/self.Weight_g/self.CVTRadius_m)**2+1)
        print ('n_cvt_={:0.1f} '.format(self.n_cvt_))
        self.n_cvt_max = math.sqrt((self.CVTSpeed_mpsTAS**2/self.Weight_g/self.CVTRadius_Min_m)**2+1)
        print ('n_cvt_max={:0.1f} '.format(self.n_cvt_max))    
        self.n_cvtclimb = math.sqrt((self.CVTClimbSpeed_mpsTAS**2/self.Weight_g/self.CVTClimbRadius_m)**2+1)
        print ('n_cvtclimb={:0.1f} '.format(self.n_cvtclimb)) 
#################################################
#                   盘旋限制                     #
################################################
        Resolution = 2000
        Start_Pa = 0.1
        WSlistCVT_Pa = np.linspace(Start_Pa,8500,Resolution)
        TWlistCVT = []
        i = 0
        for WS in WSlistCVT_Pa:
            TW = q_CVT_Pa*(self.Cd0/WSlistCVT_Pa[i] + WSlistCVT_Pa[i]*self.k*(self.n_cvt_max/q_CVT_Pa)**2)
            TWlistCVT.append(TW)
            i = i + 1
        WSlistCVT_kgm2 = [x*0.101971621 for x in WSlistCVT_Pa]
        self.theta_deg_max = math.acos(1/self.n_cvt_max)*180/math.pi
        print ('THETA_max={:.0f}'u'\xb0'.format(self.theta_deg_max))
#################################################
#                   爬升限制                     #
################################################
        WSlistROC_Pa = np.linspace(Start_Pa,8500,Resolution)
        TWlistROC = []
        self.ROC = self.ClimbSpeed_mpsTAS * math.sin(self.ClimbAngle_deg*math.pi/180.0)
        print ('ROC_mpsTAS={:0.1f} m/s'.format(self.ROC))
        i = 0
        for WS in WSlistROC_Pa:
            TW = self.ROC/self.ClimbSpeed_mpsTAS + self.Cd0*q_climb_Pa\
            /WSlistROC_Pa[i] + self.k*WSlistROC_Pa[i]*(1-(self.ROC/self.ClimbSpeed_mpsTAS)**2)/q_climb_Pa
            TWlistROC.append(TW)
            i = i + 1
        WSlistROC_kgm2 = [x*0.101971621 for x in WSlistROC_Pa]
#################################################
#                   转换场长限制                  #
################################################
        WSlistGR_Pa = np.linspace(Start_Pa,8500,Resolution)
        TWlistGR = []
        i= 0
        for WS in WSlistGR_Pa:
            CLT = 2.0*WSlistGR_Pa[i]/SeaLevelDens_kgm3/self.ApproachSpeed_mpsIAS**2
            TW = WSlistGR_Pa[i]*self.ApproachSpeed2Stall**2/ClimbAltDens_kgm3/self.Weight_g/self.Clmax_avliable/self.App_lenth_m\
            + (self.Cd0 + self.k*CLT**2)/2.0/CLT
            TWlistGR.append(TW)
            i = i +1
        WSlistGR_kgm2 = [x*0.101971621 for x in WSlistGR_Pa]
#################################################
#                  巡航限制                      #
################################################
        WSlistCR_Pa = np.linspace(Start_Pa,8500,Resolution)
        TWlistCR = []
        i = 0
        for WS in WSlistCR_Pa:
            TW = q_cruise_Pa*self.Cd0*(1.0/WSlistCR_Pa[i])+ self.k*(1/q_cruise_Pa)*WSlistCR_Pa[i]
            TWlistCR.append(TW)
            i = i + 1
        WSlistCR_kgm2 = [x*0.101971621 for x in WSlistCR_Pa]
#################################################
#                   失速限制                     #
################################################
        WS_Stall_Pa = q_Stall_Pa*self.Clmax_avliable
        WS_Stall_kgm2 = WS_Stall_Pa*0.101971621
        print ('WS_APP={:03.2f} kg/m^2'.format(WS_Stall_kgm2))
        WSlistAPP_kgm2 = [WS_Stall_kgm2, self.WSmax_kgm2, self.WSmax_kgm2, WS_Stall_kgm2, WS_Stall_kgm2 ]
        TWlistAPP = [0, 0, self.TWmax, self.TWmax, 0 ]
#################################################
#                   考虑协调转弯抗风性能           #
###############################################
        WSlistCVT_Wind_Pa = np.linspace(Start_Pa,8500,Resolution)
        TWlistCVT_Wind = []
        self.theta_deg = math.acos(1/self.n_cvt_)*180/math.pi
        print ('THETA_max={:.0f}'u'\xb0'.format(self.theta_deg))
        self.CVTAntiWind_mpsTAS = self.CVTAntiWind_mpsIAS*math.sqrt(SeaLevelDens_kgm3/CruisingAltDens_kgm3)
        print ('CVTAntiWind_mpsTAS={:03.2f} m/s'.format(self.CVTAntiWind_mpsTAS))
        i = 0
        for WS in WSlistCVT_Wind_Pa:
            TW = q_CVT_Pa*(self.Cd0/WSlistCVT_Wind_Pa[i] + WSlistCVT_Wind_Pa[i]*self.k*(self.n_cvt_/q_CVT_Pa)**2)\
            + math.tan(self.theta_deg*math.pi/180.0)*(self.CVTAntiWind_mpsTAS+self.StallSpeed_mpsTAS)/math.pi/self.CVTSpeed_mpsTAS
            TWlistCVT_Wind.append(TW)
            i = i + 1
        WSlistCVT_Wind_kgm2 = [x*0.101971621 for x in WSlistCVT_Wind_Pa]     
#################################################
#                  盘旋爬升性能限制               #
###############################################
        Resolution = 2000
        Start_Pa = 0.1
        WSlistCVTClimb_Pa = np.linspace(Start_Pa,8500,Resolution)
        TWlistCVTClimb = []
        self.CVTROC = self.ClimbSpeed_mpsTAS * math.sin(self.CVTClimbAngle_deg*math.pi/180.0)
        print ('CVTROC_mpsTAS={:0.1f} m/s'.format(self.CVTROC))
        i = 0
        for WS in WSlistCVTClimb_Pa:
            TW = q_CVTClimb_Pa*(self.Cd0/WSlistCVTClimb_Pa[i] + WSlistCVTClimb_Pa[i]*self.k*(self.n_cvtclimb/q_CVTClimb_Pa)**2)+\
            self.CVTROC/self.CVTClimbSpeed_mpsTAS + self.k*WSlistCVTClimb_Pa[i]*(1-(self.CVTROC/self.CVTClimbSpeed_mpsTAS)**2)/q_CVTClimb_Pa
            TWlistCVTClimb.append(TW)
            i = i + 1
        WSlistCVTClimb_kgm2 = [x*0.101971621 for x in WSlistCVTClimb_Pa]
        self.theta_deg_cvtclimb = math.acos(1/self.n_cvtclimb)*180/math.pi
        print ('THETA_max={:.0f}'u'\xb0'.format(self.theta_deg_cvtclimb))
#################################################
#                   远航速度确定翼载               #
################################################
        WS_srange_Pa = q_cruise_design_Pa*math.sqrt(self.Cd0/self.k)
        WS_srange_kgm2 = WS_srange_Pa*0.101971621
        print ('WS_srange={:03.2f} kg/m^2'.format(WS_srange_kgm2))
        WSlist_srang = [WS_srange_kgm2,WS_srange_kgm2]
        TWlist_srang = [0,self.TWmax]
#################################################
#                   画图显示                     #
################################################
        figCOMP = plt.figure(figsize = (9,12))
        InitialSizing.PlotSetUp(0, self.WSmax_kgm2, 0, self.TWmax, '$W/S\,[\,kg/m^2]$', '$T/W$')
        axCOMP = figCOMP.add_subplot(111)
        ConstVeloTurnPoly = InitialSizing.ConstraintPoly(WSlistCVT_kgm2,TWlistCVT,'green',0.5)
        axCOMP.add_patch(ConstVeloTurnPoly)
        ConstVeloTurnPoly_Wind = InitialSizing.ConstraintPoly(WSlistCVT_Wind_kgm2,TWlistCVT_Wind,'brown',0.5)
        axCOMP.add_patch(ConstVeloTurnPoly_Wind)        
        RateOfClimbPoly = InitialSizing.ConstraintPoly(WSlistROC_kgm2,TWlistROC,'purple',0.5)
        axCOMP.add_patch(RateOfClimbPoly)
        CruisePoly = InitialSizing.ConstraintPoly(WSlistCR_kgm2,TWlistCR,'red',0.5)
        axCOMP.add_patch(CruisePoly)
        AppStallPoly = InitialSizing.ConstraintPoly(WSlistAPP_kgm2,TWlistAPP,'grey',0.6)
        axCOMP.add_patch(AppStallPoly)
        GRPoly = InitialSizing.ConstraintPoly(WSlistGR_kgm2,TWlistGR,'gold',0.5)
        axCOMP.add_patch(GRPoly)
#        CVTClimbPoly = InitialSizing.ConstraintPoly(WSlistCVTClimb_kgm2,TWlistCVTClimb,'blue',0.5)
#        axCOMP.add_patch(CVTClimbPoly)
        textstr = '\n The feasible aeroplane lives \n in this white space'
        axCOMP.text(0.15, 0.95, textstr, transform=axCOMP.transAxes, fontsize=12, verticalalignment='top')
        axCOMP.axes.xaxis.set_major_locator(plt.MultipleLocator(10.0))#设置x主坐标间隔 1
        axCOMP.axes.xaxis.set_minor_locator(plt.MultipleLocator(1.0))#设置x从坐标间隔 0.1
        axCOMP.axes.yaxis.set_major_locator(plt.MultipleLocator(0.1))#设置y主坐标间隔 1
        axCOMP.axes.yaxis.set_minor_locator(plt.MultipleLocator(0.01))#设置y从坐标间隔 0.1
        axCOMP.axes.grid(which='major', axis='x', linewidth=0.75, linestyle='-', color='black')#由每个x主坐标出发对x主坐标画垂直于x轴的线段
        axCOMP.axes.grid(which='minor', axis='x', linewidth=0.35, linestyle='-', color='black')#由每个x主坐标出发对x主坐标画垂直于x轴的线段
        axCOMP.axes.grid(which='major', axis='y', linewidth=0.75, linestyle='-', color='black')
        axCOMP.axes.grid(which='minor', axis='y', linewidth=0.35, linestyle='-', color='black')
        axCOMP.axes.set_xticks(range(0,int(self.WSmax_kgm2),5))
        axCOMP.axes.set_yticks(np.arange(0,self.TWmax,0.05))
        plt.plot(WSlist_srang,TWlist_srang,linewidth = 2.0, linestyle='--',color = 'm',label= 'Srange' )
        axCOMP.legend(['Srange','Turn','Turn-wind','Climb','Cruise', 'App Stall','Trans Lenth','CVTClimb'])
        taget = plt.ginput(1)
        lab = list(taget[0])
        plt.scatter(lab[0],lab[1],marker = '+',color = 'red',s = 40 ,label = '{:00.2f} Target dot'.format(i+1))
        textstr = 'Target dot Position:W/S={:03.2f} ,'.format(lab[0])+'T/W={:03.2f} '.format(lab[1])
        axCOMP.text(lab[0]/80,lab[1]/0.4, textstr, transform=axCOMP.transAxes, fontsize=12, verticalalignment='top')
        axCOMP.legend(['Srange','Turn','Turn-wind','Climb','Cruise', 'App Stall','Trans Lenth','CVTClimb','Target dot'], loc = 'best')
        self.Wingload = lab[0]
        self.TW_select = lab[1]
if __name__ == '__main__':
        run = InitialSizing() 
        run.plotws()
        print (run.Wingload)
        print (run.TW_select)


