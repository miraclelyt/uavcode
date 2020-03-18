# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 13:30:49 2019

@author: 01107255
"""

import math
from aerocalc import std_atm as ISA
import numpy as np
import matplotlib
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
from InitialSizing import *

class MISSION(InitialSizing):
    """用于计算各任务段功耗"""
    def __init__(self,grossmass):
        #继承IODATA的变量
        InitialSizing.__init__(self)
#        InitialSizing.plotws(self)
        self.gross_weight = grossmass*self.Weight_g
        self.SeaLevelDens_kgm3 = ISA.alt2density(0,alt_units='m',density_units='kg/m**3')
    def cruise(self,weight):
        """用于固定翼段巡航功耗"""
        cruiseAlt_m = self.Mission_TakeOff_Alt_m + self.Mission_TakeOff_Height_m + self.Mission_CVTClimbHeight_m
        cruise_rho = ISA.alt2density(cruiseAlt_m,alt_units='m',density_units='kg/m**3')
        Q_cruise = 0.5*self.SeaLevelDens_kgm3*self.Mission_CruisingSpeed_mpsIAS**2
        self.Mission_CruisingSpeed_mpsTAS = self.Mission_CruisingSpeed_mpsIAS*math.sqrt(self.SeaLevelDens_kgm3\
                                                      /cruise_rho)
        print('cruise_TAS={:0.1f} m/s'.format(self.Mission_CruisingSpeed_mpsTAS))
        Cruise_Ma = self.Mission_CruisingSpeed_mpsTAS/self.Engine_Soundspeed
        print('Cruise_Ma={:0.3f} '.format(Cruise_Ma))
        #推进螺旋桨需用功率
        self.thrust = (Q_cruise*self.Cd0/self.Wingload/self.Weight_g+self.k*self.Wingload*self.Weight_g/Q_cruise)*weight
        print('cruise_thrust={:0.1f} N'.format(self.thrust))
        area_prop = self.thrust/self.Weight_g/self.Engine_Prop_Diskload
        prop_radius = math.sqrt(area_prop/math.pi)
        dimeter_inch = prop_radius*2000/25.4
        print ('The suggest dimeter of the thrust prop: {:0.1f} inch'.format(dimeter_inch))
        #实际选用的螺旋桨取整数并大一号
        design_dimeter_inch = math.ceil(dimeter_inch)
        print ('The design dimeter of the prop: {:0.1f} inch'.format(design_dimeter_inch))
        self.prop_radius_ture = design_dimeter_inch*25.4/2.0/1000.0
        print('prop_radius_ture:{:0.3f}m'.format(self.prop_radius_ture))
        ture_area = math.pi*(self.prop_radius_ture)**2
        self.Engine_Prop_Diskload_cal = self.thrust/self.Weight_g/ture_area
        print ('The ture diskload: {:0.1f} kg/m2'.format(self.Engine_Prop_Diskload_cal))
        P_require = self.thrust*self.Mission_CruisingSpeed_mpsTAS
        print('P_cruise_motor_shaft={:0.1f} W'.format(P_require/self.Engine_Prop_Eta))
        #推进螺旋桨电功率
        P_motor = P_require/self.Engine_Prop_Eta/self.Engine_Prop_EtaMotor/self.Engine_Prop_EtaESC/self.Engine_Prop_EtaWire
        print('P_cruise_motor={:0.1f} W'.format(P_motor))
        self.cruise_time = (self.Mission_CruisingSail_km*1000-self.Climb_sail-self.descent_sail)/self.Mission_CruisingSpeed_mpsTAS
        print('cruise_time={:0.1f} s'.format(self.cruise_time))
        #巡航阶段耗能
        self.cruise_energy = (P_motor+self.Mission_Aviation_Power_w)*(self.Mission_CruisingSail_km*1000-self.Climb_sail-self.descent_sail)/self.Mission_CruisingSpeed_mpsTAS/3600
        print('cruise_energy={:0.1f} W·h'.format(self.cruise_energy))
        return self.cruise_energy
    def vtol(self,weight):
        """用于计算多旋翼状态起飞和降落段功耗"""
        #根据桨盘载荷预算一个螺旋桨直径
        area = weight/self.Weight_g/self.Engine_VT_Diskload/self.Engine_VT_Num
        prop_radius = math.sqrt(area/math.pi)
        dimeter_inch = prop_radius*2000/25.4
        print ('The suggest dimeter of the prop: {:0.3f} inch'.format(dimeter_inch))
        #实际选用的螺旋桨取整数并大一号
        design_dimeter_inch = math.ceil(dimeter_inch)
        print ('The design dimeter of the prop: {:0.1f} inch'.format(design_dimeter_inch))
        self.vt_prop_radius_ture = design_dimeter_inch*25.4/2.0/1000.0
        print('vt_prop_radius_ture:{:0.3f}m'.format(self.vt_prop_radius_ture))
        ture_area = math.pi*(self.vt_prop_radius_ture)**2
        self.Engine_VT_Diskload_cal = weight/self.Weight_g/self.Engine_VT_Num/ture_area
        print ('The ture diskload: {:0.3f} kg/m2'.format(self.Engine_VT_Diskload_cal))
        hover_rho = ISA.alt2density(self.Mission_TakeOff_Alt_m,alt_units='m',density_units='kg/m**3')
#        print('hover_rho:{:0.3f}kg/m3'.format(hover_rho))
#        T_sigle_motor_kg = weight/self.Weight_g/self.Engine_VT_Num
        self.P_single_motor = weight*math.sqrt(weight/math.pi/self.Engine_VT_Num/hover_rho/2.0)\
        /self.Engine_VT_Num/self.vt_prop_radius_ture/self.Engine_VT_FM
#        P_single_motor2 = T_sigle_motor_kg*1000/self.Engine_VT_GW
        self.gw_true = self.Engine_VT_FM*math.sqrt(2.0*hover_rho)*1000/math.sqrt\
        (self.Engine_VT_Diskload_cal*self.Weight_g)/self.Weight_g
        print('The true gw:{:0.3f}'.format(self.gw_true))
        print('The power of single motor_sharft:{:0.1f}W'.format(self.P_single_motor))
        #垂起动力系统总功耗
        self.P_VT_motor = self.Engine_VT_Num*self.P_single_motor/self.Engine_VT_FM_factor/self.Engine_VT_EtaMotor/self.Engine_VT_EtaESC/self.Engine_VT_EtaWire
        print('P_VT_motor={:0.1f} W'.format(self.P_VT_motor))
        #一次起降过程的能量消耗
        self.VTOL_energy = (self.P_VT_motor+self.Mission_Aviation_Power_w)*(self.Mission_TakeOff_Height_m/self.Mission_TakeOff_Speed_mps+self.Mission_Landing_Height_m\
                                     /self.Mission_Landing_Speed_mps)/3600
        print('VTOL_energy={:0.1f} W·h'.format(self.VTOL_energy))
        return self.VTOL_energy
    def climb(self,weight):
        """用于固定翼段爬升功耗"""
        climbAlt_m = self.Mission_TakeOff_Alt_m+self.Mission_TakeOff_Height_m
        climb_rho = ISA.alt2density(climbAlt_m,alt_units='m',density_units='kg/m**3')       
        Q_climb = 0.5* self.SeaLevelDens_kgm3*self.Mission_ClimbSpeed_mpsIAS**2
        self.Mission_ClimbSpeed_mpsTAS = self.Mission_ClimbSpeed_mpsIAS*math.sqrt(self.SeaLevelDens_kgm3\
                                                      /climb_rho)
        self.Mission_ROC = self.Mission_ClimbSpeed_mpsTAS* math.sin(self.Mission_ClimbAngle_deg*math.pi/180.0)
        self.climb_thrust = weight*(self.Cd0*Q_climb/self.Wingload/self.Weight_g + self.k*self.Wingload*self.Weight_g*\
        (1-(self.Mission_ROC/self.Mission_ClimbSpeed_mpsTAS)**2)/Q_climb+self.Mission_ROC/self.Mission_ClimbSpeed_mpsTAS)
        #推进螺旋桨需用功率
        print('climb_thrust={:0.1f} N'.format(self.climb_thrust))
        P_require = self.climb_thrust*self.Mission_ClimbSpeed_mpsTAS
            #推进螺旋桨电功率
        P_motor = P_require/self.Engine_Prop_Maxp_Eta/self.Engine_Min_EtaMotor/\
        self.Engine_Min_EtaESC/self.Engine_Min_EtaWire
        print('P_climb={:0.1f} W'.format(P_motor))
        #巡航阶段耗能
        self.Climb_Time = self.Mission_ClimbHeight_m/self.Mission_ROC
        print('Time_climb={:0.1f} s'.format(self.Climb_Time))
        self.Climb_sail = self.Mission_ClimbHeight_m/math.tan(self.Mission_ClimbAngle_deg*math.pi/180.0)
        print('Climb range={:0.1f} km'.format(self.Climb_sail/1000.0))
        self.Climb_energy = (P_motor+self.Mission_Aviation_Power_w)*self.Mission_ClimbHeight_m/self.Mission_ROC/3600
        print('Climb_energy={:0.1f} W·h'.format(self.Climb_energy))
        return self.Climb_energy
    def descent(self,weight):
        """用于固定翼段下降功耗"""
        descent_rho = ISA.alt2density(self.ROCAlt_m,alt_units='m',density_units='kg/m**3')       
        Q_descent = 0.5* self.SeaLevelDens_kgm3*self.Mission_ClimbSpeed_mpsIAS**2
        self.Mission_DescentSpeed_mpsTAS = self.Mission_DescentSpeed_mpsIAS*math.sqrt(self.SeaLevelDens_kgm3\
                                                      /descent_rho)
        decentAngle_min = math.atan2(1,self.Kmax)*180/math.pi
        decentAngle = math.asin(self.Mission_ROD/self.Mission_DescentSpeed_mpsTAS)*180/math.pi
        if decentAngle >= decentAngle_min:
            self.descent_energy = self.Mission_Aviation_Power_w*self.Mission_DesentHeight_m/self.Mission_ROD/3600 
            print("HAHAHAHA")
        else:
            thrust = weight*(self.Cd0*Q_descent/self.Wingload/self.Weight_g + self.k*self.Wingload*self.Weight_g*\
            (1-(self.Mission_ROD/self.Mission_DescentSpeed_mpsTAS)**2)/Q_descent-self.Mission_ROD/self.Mission_DescentSpeed_mpsTAS)
            #推进螺旋桨需用功率
            P_require = thrust*self.Mission_DescentSpeed_mpsTAS
            #推进螺旋桨电功率
            P_motor = P_require/(self.Engine_Prop_Eta)/(self.Engine_Prop_EtaMotor)/\
            (self.Engine_Prop_EtaESC)/(self.Engine_Prop_EtaWire)
            #巡航阶段耗能
            print('P_decent={:0.1f} W'.format(P_motor+self.Mission_Aviation_Power_w))
            self.descent_energy = (P_motor+self.Mission_Aviation_Power_w)*self.Mission_DesentHeight_m/self.Mission_ROD/3600
        self.descent_sail = self.Mission_DesentHeight_m/math.tan(decentAngle*math.pi/180)
        print('Descent range={:0.1f} km'.format(self.descent_sail/1000.0))
#        K_decent = 1/math.tan(decentAngle*math.pi/180)
        print('descent_energy={:0.1f} W·h'.format(self.descent_energy))
        return self.descent_energy
    def vt2c(self,weight):
        """用于多旋翼转固定翼过程功耗"""
        #先做一个近似，整个转换过程为尾推加悬停状态的平均功耗,目前该预估是偏小的
        #转换速度下的巡航功率
        Vt2cAlt_m = self.Mission_TakeOff_Alt_m + self.Mission_TakeOff_Height_m
        Vt2c_rho = ISA.alt2density(Vt2cAlt_m,alt_units='m',density_units='kg/m**3')
        Q_trans = 0.5*self.SeaLevelDens_kgm3*self.ApproachSpeed_mpsIAS**2
        self.Mission_ApproachSpeed_mpsTAS = self.ApproachSpeed_mpsIAS*math.sqrt(self.SeaLevelDens_kgm3\
                                                      /Vt2c_rho)
        #推进螺旋桨需用功率
        thrust = (Q_trans*self.Cd0/self.Wingload/self.Weight_g+self.k*self.Wingload*self.Weight_g/Q_trans)*weight
        P_require = thrust*self.Mission_ApproachSpeed_mpsTAS
        #推进螺旋桨电功率
        self.P_trans_prop_motor = P_require/self.Engine_Prop_Eta/self.Engine_Prop_EtaMotor/self.Engine_Prop_EtaESC/self.Engine_Prop_EtaWire
        self.P_trans = (self.P_trans_prop_motor+self.P_VT_motor)/2
        print('P_trans={:0.1f} W'.format(self.P_trans))
        self.Vt2c_energy = (self.P_trans+ self.Mission_Aviation_Power_w)* (self.Mission_ApproachSpeed_mpsTAS/self.Mission_FW_a_mps2+self.Mission_ApproachSpeed_mpsTAS\
                                           /-self.Mission_FW2VT_na_mps2)/3600
        print('Vt2c_energy={:0.1f} W·h'.format(self.Vt2c_energy))
        return self.Vt2c_energy
    def CVTclimb(self,weight):
        """用于计算盘旋爬升"""    
        #增加转换过程中的盘旋爬升的计算
        CVTClimbAlt_m = self.Mission_TakeOff_Alt_m + self.Mission_TakeOff_Height_m
        CVTclimb_rho = ISA.alt2density(CVTClimbAlt_m,alt_units='m',density_units='kg/m**3')       
        Q_CVTclimb = 0.5* self.SeaLevelDens_kgm3*self.Mission_CVTClimbSpeed_mpsIAS**2
        self.Mission_CVTClimbSpeed_mpsTAS = self.Mission_CVTClimbSpeed_mpsIAS*math.sqrt(self.SeaLevelDens_kgm3\
                                                      /CVTclimb_rho)
        self.Mission_n_cvtclimb = math.sqrt((self.Mission_CVTClimbSpeed_mpsTAS**2/self.Weight_g/self.Mission_CVTClimbRadius_m)**2+1)
        self.Mission_CVTROC = self.Mission_CVTClimbSpeed_mpsTAS* math.sin(self.Mission_CVTClimbAngle_deg*math.pi/180.0)
        CVTClimb_thrust = weight*(Q_CVTclimb*(self.Cd0/self.Wingload + self.Wingload*self.k*(self.Mission_n_cvtclimb/Q_CVTclimb)**2)+\
            self.Mission_CVTROC/self.Mission_CVTClimbSpeed_mpsTAS +\
            self.k*self.Wingload*(1-(self.Mission_CVTROC/self.Mission_CVTClimbSpeed_mpsTAS)**2)/Q_CVTclimb)
        print('CVTClimb_thrust={:0.1f} N'.format(CVTClimb_thrust))
        P_require = CVTClimb_thrust*self.Mission_CVTClimbSpeed_mpsTAS
            #推进螺旋桨电功率
        P_motor = P_require/self.Engine_Prop_Maxp_Eta/self.Engine_Min_EtaMotor/\
        self.Engine_Min_EtaESC/self.Engine_Min_EtaWire
        print('P_CVTclimb={:0.1f} W'.format(P_motor))
        #巡航阶段耗能
        self.CVTClimb_Time = self.Mission_CVTClimbHeight_m/self.Mission_CVTROC
        print('Time_CVTclimb={:0.1f} s'.format(self.CVTClimb_Time))
        self.Climb_sail = 0
#        self.Climb_sail = self.Mission_ClimbHeight_m/math.tan(self.Mission_ClimbAngle_deg*math.pi/180.0)
#        print('Climb range={:0.1f} km'.format(self.Climb_sail/1000.0))
        self.CVTClimb_energy = (P_motor+self.Mission_Aviation_Power_w)*self.CVTClimb_Time/3600
        print('CVTClimb_energy={:0.1f} W·h'.format(self.CVTClimb_energy))
        return self.CVTClimb_energy
    def CVTdescent(self,weight):
        """用于计算盘旋下降"""
        descent_rho = ISA.alt2density(self.ROCAlt_m,alt_units='m',density_units='kg/m**3')       
        Q_descent = 0.5* self.SeaLevelDens_kgm3*self.Mission_ClimbSpeed_mpsIAS**2
        self.Mission_DescentSpeed_mpsTAS = self.Mission_DescentSpeed_mpsIAS*math.sqrt(self.SeaLevelDens_kgm3\
                                                      /descent_rho)
        decentAngle_min = math.atan2(1,self.Kmax)*180/math.pi
        decentAngle = math.asin(self.Mission_ROD/self.Mission_DescentSpeed_mpsTAS)*180/math.pi
        if decentAngle >= decentAngle_min:
            self.descent_energy = self.Mission_Aviation_Power_w*self.Mission_DesentHeight_m/self.Mission_ROD/3600 
            print("HAHAHAHA")
        else:
            thrust = weight*(self.Cd0*Q_descent/self.Wingload/self.Weight_g + self.k*self.Wingload*self.Weight_g*\
            (1-(self.Mission_ROD/self.Mission_DescentSpeed_mpsTAS)**2)/Q_descent-self.Mission_ROD/self.Mission_DescentSpeed_mpsTAS)
            #推进螺旋桨需用功率
            P_require = thrust*self.Mission_DescentSpeed_mpsTAS
            #推进螺旋桨电功率
            P_motor = P_require/(self.Engine_Prop_Eta)/(self.Engine_Prop_EtaMotor)/\
            (self.Engine_Prop_EtaESC)/(self.Engine_Prop_EtaWire)
            #巡航阶段耗能
            print('P_decent={:0.1f} W'.format(P_motor+self.Mission_Aviation_Power_w))
            self.descent_energy = (P_motor+self.Mission_Aviation_Power_w)*self.Mission_DesentHeight_m/self.Mission_ROD/3600
        self.descent_sail = self.Mission_DesentHeight_m/math.tan(decentAngle*math.pi/180)
        print('Descent range={:0.1f} km'.format(self.descent_sail/1000.0))
#        K_decent = 1/math.tan(decentAngle*math.pi/180)
        print('descent_energy={:0.1f} W·h'.format(self.descent_energy))
        return self.descent_energy
#    def CVT(self):
#        """确定固定翼盘旋状态功耗值"""
#        
#        
#    def acc(self):
#        """用于固定翼加速/减速过程功耗"""        
#        #固定翼加速和减速近似为一个恒定加速度/减速度过程
    def battery_weight(self,mass):       
        weight = mass*self.Weight_g
        if self.Mission_model == 1:    
            battery_eng_true = self.Mission_Segment_num*(self.vtol(weight)+self.climb(weight)+self.descent(weight)+self.cruise(weight)+self.vt2c(weight))/self.Engine_Avi_Eta
            print('!!!!Battery_eng_used:{:0.3f}W.h'.format(battery_eng_true))
            self.battery_eng = battery_eng_true/(1-self.Mission_dump_factor*0.01)
            print('!!!!Battery_eng:{:0.3f}W.h'.format(self.battery_eng))
            self.bat_weight = self.battery_eng/self.Weight_battery_factor
            return self.bat_weight
        elif self.Mission_model == 2:
            battery_eng_true = self.Mission_Segment_num*(self.vtol(weight)+self.CVTclimb(weight)+self.CVTdescent(weight)+self.cruise(weight)+self.vt2c(weight))/self.Engine_Avi_Eta
            self.battery_eng = battery_eng_true/(1-self.Mission_dump_factor*0.01)
            self.bat_weight = self.battery_eng/self.Weight_battery_factor
            return self.bat_weight
        else:
            print('Input correct mission model factor!')
#    def plot_mission_seg(self):
#        """绘制飞机的任务剖面"""
#if __name__ == '__main__':
#        seg = MISSION(60)
#        seg.plotws()
#        seg.battery_weight(60)
#        print('Battery_weight={:0.2f} Kg'.format(seg.bat_weight))