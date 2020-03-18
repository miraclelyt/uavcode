# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 10:55:23 2019

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

class PERFORMANCE(GROSSWIGHT):
    """该类用于计算总体设计完成的相关性能"""
    def __init__(self):
        GROSSWIGHT.__init__(self)
        self.SeaLevelDens_kgm3 = ISA.alt2density(0,alt_units='m',density_units='kg/m**3')
    def srange(self,payload,velocity,altitude):
        """求解不同带载的情况下不同海拔和速度下的飞机航程"""
        gw = GROSSWIGHT()
        gw.cal_grossweight(45.0)
        print('*****************************************')
        self.true_grossweight = (gw.Weight_grossmass_kg-self.Weight_Payload+payload)*self.Weight_g
        print('Performance Grossweight :{:0.1f} N'.format(self.true_grossweight))
        self.true_wingload = self.true_grossweight*gw.Wingload/self.Weight_g/gw.Weight_grossmass_kg
        print('true_wingload :{:0.1f} kg/m2'.format(self.true_wingload))
        #################计算垂起阶段能量
        hover_rho = ISA.alt2density(self.Performance_Alt,alt_units='m',density_units='kg/m**3')
        P_single_motor = self.true_grossweight*math.sqrt(self.true_grossweight/math.pi/self.Engine_VT_Num/hover_rho/2.0)\
        /self.Engine_VT_Num/gw.vt_prop_radius_ture/self.Engine_VT_FM
        gw_true = self.Engine_VT_FM*math.sqrt(2.0*hover_rho)*1000/math.sqrt\
        (gw.Engine_VT_Diskload_cal*self.Weight_g)/self.Weight_g
        print('Performance gw:{:0.3f}'.format(gw_true))
        print('Performance single motor_sharft:{:0.1f}W'.format(P_single_motor))
        #垂起动力系统总功耗
        P_VT_motor = self.Engine_VT_Num*P_single_motor/self.Engine_VT_FM_factor/self.Engine_VT_EtaMotor/self.Engine_VT_EtaESC/self.Engine_VT_EtaWire
        print('Performance_VT_motor={:0.1f} W'.format(P_VT_motor))
        #一次起降过程的能量消耗
        VTOL_energy = (P_VT_motor+self.Mission_Aviation_Power_w)*(self.Performance_TakeOff_Height_m/self.Mission_TakeOff_Speed_mps+self.Performance_Landing_Height_m\
                                     /self.Mission_Landing_Speed_mps)/3600
        print('Performance_VTOL_energy={:0.1f} W·h'.format(VTOL_energy))
        #################计算爬升阶段能量
        climbAlt_m = self.Performance_Alt+self.Performance_TakeOff_Height_m+self.Performance_ClimbHeight_m/2.0
        climb_rho = ISA.alt2density(climbAlt_m,alt_units='m',density_units='kg/m**3')       
        Q_climb = 0.5* self.SeaLevelDens_kgm3*self.Performance_Velocity_mpsIAS**2
        Performance_ClimbSpeed_mpsTAS = self.Performance_Velocity_mpsIAS*math.sqrt(self.SeaLevelDens_kgm3\
                                                      /climb_rho)
        Performance_ROC = Performance_ClimbSpeed_mpsTAS* math.sin(self.Performance_ClimbAngle_deg*math.pi/180.0)
        print('Performance climb_ROC={:0.1f} mps'.format(Performance_ROC))
        climb_thrust = self.true_grossweight*(self.Cd0*Q_climb/self.true_wingload/self.Weight_g + gw.k*self.true_wingload*self.Weight_g*\
        (1-(Performance_ROC/Performance_ClimbSpeed_mpsTAS)**2)/Q_climb+Performance_ROC/Performance_ClimbSpeed_mpsTAS)
        #推进螺旋桨需用功率
        print('Performance climb_thrust={:0.1f} N'.format(climb_thrust))
        P_require = climb_thrust*Performance_ClimbSpeed_mpsTAS
        #推进螺旋桨电功率
#        P_motor = P_require/self.Engine_Prop_Maxp_Eta/self.Engine_Min_EtaMotor/\
#        self.Engine_Min_EtaESC/self.Engine_Min_EtaWire
        P_motor = P_require/self.Engine_Prop_Maxp_Eta
        print('Power_climb={:0.1f} W'.format(P_motor))
        #爬升阶段耗能
        Climb_Time = self.Performance_ClimbHeight_m/Performance_ROC
        print('Time_climb={:0.1f} s'.format(Climb_Time))
        Climb_sail = self.Performance_ClimbHeight_m/math.tan(self.Performance_ClimbAngle_deg*math.pi/180.0)
        print('Climb range={:0.1f} km'.format(Climb_sail/1000.0))
        Climb_energy = (P_motor+self.Mission_Aviation_Power_w)*self.Performance_ClimbHeight_m/Performance_ROC/3600
        print('Climb_energy={:0.1f} W·h'.format(Climb_energy))
        ############计算下降阶段能量
        descent_rho = ISA.alt2density(climbAlt_m,alt_units='m',density_units='kg/m**3')       
        Performance_DescentSpeed_mpsTAS = self.Performance_Velocity_mpsIAS*math.sqrt(self.SeaLevelDens_kgm3\
                                                      /descent_rho)
        decentAngle_min = math.atan2(1,self.Kmax)*180/math.pi
        Performance_ROD = Performance_DescentSpeed_mpsTAS * math.sin(decentAngle_min*math.pi/180.0)
        print(' Performance_ROD={:0.1f}mps'.format(Performance_ROD))
#        decentAngle = math.asin(self.Performance_ROD/Performance_DescentSpeed_mpsTAS)*180/math.pi
#        if decentAngle >= decentAngle_min:
        descent_energy = self.Mission_Aviation_Power_w*self.Performance_DesentHeight_m/Performance_ROD/3600 
#        else:
#            thrust = weight*(self.Cd0*Q_descent/self.Wingload/self.Weight_g + self.k*self.Wingload*self.Weight_g*\
#            (1-(self.Mission_ROD/self.Mission_DescentSpeed_mpsTAS)**2)/Q_descent-self.Mission_ROD/self.Mission_DescentSpeed_mpsTAS)
#            #推进螺旋桨需用功率
#            P_require = thrust*self.Mission_DescentSpeed_mpsTAS
#            #推进螺旋桨电功率
#            P_motor = P_require/(self.Engine_Prop_Eta)/(self.Engine_Prop_EtaMotor)/\
#            (self.Engine_Prop_EtaESC)/(self.Engine_Prop_EtaWire)
        descent_sail = self.Performance_DesentHeight_m/math.tan(decentAngle_min*math.pi/180)
        print('Descent range={:0.1f} km'.format(descent_sail/1000.0))
#        K_decent = 1/math.tan(decentAngle*math.pi/180)
        print('descent_energy={:0.1f} W·h'.format(descent_energy))
        ##########计算转换阶段能量
        Vt2cAlt_m = self.Performance_Alt + self.Performance_TakeOff_Height_m
        Vt2c_rho = ISA.alt2density(Vt2cAlt_m,alt_units='m',density_units='kg/m**3')
        Q_trans = 0.5*self.SeaLevelDens_kgm3*self.ApproachSpeed_mpsIAS**2
        self.Mission_ApproachSpeed_mpsTAS = self.ApproachSpeed_mpsIAS*math.sqrt(self.SeaLevelDens_kgm3\
                                                      /Vt2c_rho)
        #推进螺旋桨需用功率
        thrust = (Q_trans*self.Cd0/self.true_wingload/self.Weight_g+gw.k*self.true_wingload*self.Weight_g/Q_trans)*self.true_grossweight
        P_require = thrust*self.Mission_ApproachSpeed_mpsTAS
        #推进螺旋桨电功率
        P_trans_prop_motor = P_require/self.Engine_Prop_Eta/self.Engine_Prop_EtaMotor/self.Engine_Prop_EtaESC/self.Engine_Prop_EtaWire
        P_trans = (P_trans_prop_motor+P_VT_motor)/2
        print('P_trans={:0.1f} W'.format(P_trans))
        Vt2c_energy = (P_trans+ self.Mission_Aviation_Power_w)* (self.Mission_ApproachSpeed_mpsTAS/self.Mission_FW_a_mps2+self.Mission_ApproachSpeed_mpsTAS\
                                           /-self.Mission_FW2VT_na_mps2)/3600
        print('VT2c_energy={:0.1f} W·h'.format(Vt2c_energy))
        ######计算巡航段耗能
        cruiseAlt_m = self.Performance_Alt+self.Performance_TakeOff_Height_m+self.Performance_ClimbHeight_m
        cruise_rho = ISA.alt2density(cruiseAlt_m,alt_units='m',density_units='kg/m**3')
        Q_cruise = 0.5*self.SeaLevelDens_kgm3*self.Performance_Velocity_mpsIAS**2
        Performance_CruisingSpeed_mpsTAS = self.Performance_Velocity_mpsIAS*math.sqrt(self.SeaLevelDens_kgm3\
                                                      /cruise_rho)
        print('cruise_TAS={:0.1f} m/s'.format(Performance_CruisingSpeed_mpsTAS))
#        Cruise_Ma = Performance_CruisingSpeed_mpsTAS/self.Engine_Soundspeed
#        print('Cruise_Ma={:0.3f} '.format(Cruise_Ma))
        #推进螺旋桨需用功率
        thrust = (Q_cruise*self.Cd0/self.true_wingload/self.Weight_g+gw.k*self.true_wingload*self.Weight_g/Q_cruise)*self.true_grossweight
        print('Performance_cruise_thrust={:0.1f} N'.format(thrust))
        clcd = self.true_grossweight/thrust
        print('Cruise clcd={:0.1f}'.format(clcd))
        P_require = thrust*Performance_CruisingSpeed_mpsTAS
        print('P_cruise_motor_shaft={:0.1f} W'.format(P_require/self.Engine_Prop_Eta))
        #推进螺旋桨电功率
        P_motor = P_require/self.Engine_Prop_Eta/self.Engine_Prop_EtaMotor/self.Engine_Prop_EtaESC/self.Engine_Prop_EtaWire
        print('P_cruise_motor={:0.1f} W'.format(P_motor))
        P_curise = P_motor+self.Mission_Aviation_Power_w
        print('Curise_power:{:0.1f} W'.format(P_curise))
        ###########用于巡航的电能
        battery_eng_avi = gw.battery_eng * (1-self.Performance_dump_factor*0.01)
        battery_eng_rem = battery_eng_avi*self.Engine_Avi_Eta-VTOL_energy-Climb_energy-descent_energy-Vt2c_energy
        #计算巡航段航程
        curise_time = battery_eng_rem/P_curise
        print('Curise_time:{:0.1f} min'.format(curise_time*60.0))
        curise_srange = Performance_CruisingSpeed_mpsTAS * curise_time * 3.6
        print('Curise_range:{:0.1f} km'.format(curise_srange))
        #返回总航程
        total_range = Climb_sail/1000.0 + descent_sail/1000.0 + curise_srange
        print('Total range:{:0.1f} km'.format(total_range))
        return total_range
if __name__ == '__main__':
    run = PERFORMANCE()
    run.srange(run.Performance_Payload,run.Performance_Velocity_mpsIAS,run.Performance_Alt)