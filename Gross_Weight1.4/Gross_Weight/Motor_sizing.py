# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 14:38:03 2019
V1.1 
1.增加转换场长评估
2.增加转弯风速对推重比要求评估
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

class MOTORSIZING(IODATA):
    def  __init__(self):
        IODATA.__init__(self)
        self.rho_fe = 7800.0
        self.rho_prop = (2*1.75+3*0.35)*1000/5
    def vtolmotor(self,radius_prop,p_single_motor):
        print(' radius_prop={:0.1f} m'.format(radius_prop))
        p_singlemax_motor = p_single_motor*self.Engine_VT_TW*math.sqrt(2)
        P_VT_MAX = p_singlemax_motor/self.Engine_VT_EtaMotor/self.Engine_VT_EtaESC/self.Engine_VT_EtaWire
        print(' P_singlemax_motor_sharft={:0.1f} W'.format(p_singlemax_motor))
        print(' P_vt_max_motor={:0.1f} W'.format(P_VT_MAX))
        max_omig_rads = self.Engine_Soundspeed*self.Engine_Prop_tipspeed_Ma/radius_prop
        print(' max_n_VT={:0.1f} Radps'.format(max_omig_rads))
        omig_max_rpm = math.ceil(max_omig_rads*60/2/math.pi)
        print(' max_n_VT={:0.1f} RPM'.format(omig_max_rpm))
        omig_VT_rpm = omig_max_rpm/math.sqrt(2.0)
        print(' n_VT={:0.1f} RPM'.format(omig_VT_rpm))
#        torque_max = p_singlemax_motor/max_omig_rads
#        volum_vt_motor = torque_max * math.pi/self.Engine_VT_TRV/4.0
#        mass_vt_motor = 2.0*volum_vt_motor*self.rho_fe/3000
#        print(' mass_vt_motor={:0.1f} g'.format(mass_vt_motor*1000))
#        mass_vt_esc = self.Engine_VT_ESC_factor * mass_vt_motor
#        print(' mass_vt_esc={:0.1f} g'.format(mass_vt_esc*1000))
#        mass_vt_prop = self.rho_prop*math.pi* radius_prop * radius_prop *self.Engine_VT_Prop_factor*self.Engine_VT_Prop_h/1000
#        print(' mass_vt_prop={:0.1f} g'.format(mass_vt_prop*1000))
        mass_vt_motor = P_VT_MAX/self.Engine_VT_Motor_Weightfactor/1000
        print(' mass_vt_motor={:0.1f} g'.format(mass_vt_motor*1000))
        mass_vt_esc =  P_VT_MAX/self.Engine_ESCFOC_Weightfactor/1000
        print(' mass_vt_esc={:0.1f} g'.format(mass_vt_esc*1000))
        mass_vt_prop = math.pi* radius_prop * radius_prop *self.Engine_Prop_Weightfactor/1000
        print(' mass_vt_prop={:0.1f} g'.format(mass_vt_prop*1000)) 
        self.mass_vt_engin = self.Engine_VT_Num*(mass_vt_motor+mass_vt_esc+mass_vt_prop)
        return self.mass_vt_engin
    def tmotor(self,radius_prop,TW,grossmass):
        #根据螺旋桨直径求解最大转速rad/s
        grossweight = grossmass * self.Weight_g
        omig_max_rad = self.Engine_Soundspeed*self.Engine_Prop_tipspeed_Ma/radius_prop
        cruise_rho = ISA.alt2density(self.CruisingAlt_m,alt_units='m',density_units='kg/m**3')
        omig_max_rpm = math.ceil(omig_max_rad*60/2/math.pi)
        print(' max_n_prop={:0.1f} RPM'.format(omig_max_rpm))
        #螺旋桨最大轴功率由设计状态下的推重比得到
        p_prop_max_shaft = grossweight*TW*self.CruisingSpeed_Maxavliable_mpsIAS*math.sqrt(1.225/cruise_rho)/self.Engine_Prop_Maxp_Eta
        print(' P_prop_max_Shaft={:0.1f} W'.format(p_prop_max_shaft))
        #电机的扭矩
        P_prop_MAX = p_prop_max_shaft/self.Engine_Min_EtaMotor/self.Engine_Min_EtaESC/self.Engine_Min_EtaWire
        print(' P_prop_max_motor={:0.1f} W'.format(P_prop_MAX))
#        torque_prop_max = p_prop_max_shaft/omig_max_rad
#        volum_prop_motor = torque_prop_max*math.pi/self.Engine_Prop_TRV/4.0
#        mass_prop_motor = 2.0*volum_prop_motor*self.rho_fe/3000
#        print(' mass_prop_motor={:0.1f} g'.format(mass_prop_motor*1000))
#        mass_prop_esc = self.Engine_VT_ESC_factor * mass_prop_motor
#        print(' mass_prop_esc={:0.1f} g'.format(mass_prop_esc*1000))
#        mass_prop = self.rho_prop*math.pi* radius_prop * radius_prop *self.Engine_VT_Prop_factor*self.Engine_VT_Prop_h/1000
#        print(' mass_prop={:0.1f} g'.format(mass_prop*1000))
        mass_prop_motor = P_prop_MAX/self.Engine_Prop_Motor_Weightfactor/1000
        print(' mass_prop_motor={:0.1f} g'.format(mass_prop_motor*1000))
        mass_prop_esc = P_prop_MAX/self.Engine_ESCFOC_Weightfactor/1000
        print(' mass_prop_esc={:0.1f} g'.format(mass_prop_esc*1000))
        mass_prop = math.pi* radius_prop * radius_prop * self.Engine_Prop_Weightfactor/1000
        print(' mass_prop={:0.1f} g'.format(mass_prop*1000))
        self.mass_prop_engin = mass_prop_motor+mass_prop_esc+mass_prop
        return self.mass_prop_engin
#if __name__ == '__main__':
#        seg = MISSION(35.5)
#        seg.plotws()
#        seg.battery_weight(35.5)
#        print('Battery_weight={:0.2f} Kg'.format(seg.bat_weight))
#        motor = MOTORSIZING()
#        mass_vt = motor.vtolmotor(seg.vt_prop_radius_ture,seg.P_single_motor)
#        print('mass_vt:{:0.3} kg'.format(mass_vt))
#        mass_prop = motor.tmotor(seg.prop_radius_ture,seg.TW_select,seg.gross_weight)
        
