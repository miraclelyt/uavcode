# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 19:13:22 2020

@author: miracle
"""
import math
import tkinter as tk
import tkinter.messagebox as mbox
from turtle import *

global Airspeed
AirSpeed=26#巡航空速，m/s
#WindSpeed=5#风速，m/s

window = tk.Tk()
window.title('任务可行性评估')
window.geometry('600x500') 

l1 = tk.Label(window, text='总航程(km)', bg='grey', font=('Arial', 12), width=30, height=2)
TotalRange = tk.IntVar()
Totalrange = tk.Entry(window, show=None, font=('Arial', 14),textvariable=TotalRange)

l2 = tk.Label(window, text='固定翼爬升高度(m)', bg='grey', font=('Arial', 12), width=30, height=2)
HeightTakeoff = tk.IntVar()
Heighttakeoff = tk.Entry(window, show=None, font=('Arial', 14),textvariable=HeightTakeoff)

l3 = tk.Label(window, text='固定翼下降高度(m)', bg='grey', font=('Arial', 12), width=30, height=2)
HeightFixClimb = tk.IntVar()
HeightFixclimb = tk.Entry(window, show=None, font=('Arial', 14),textvariable=HeightFixClimb)

l4 = tk.Label(window, text='旋翼起飞高度(m)', bg='grey', font=('Arial', 12), width=30, height=2)
HeightFixDescend = tk.IntVar()
HeightFixdescend = tk.Entry(window, show=None, font=('Arial', 14),textvariable=HeightFixDescend)

l5 = tk.Label(window, text='旋翼下降高度(m)', bg='grey', font=('Arial', 12), width=30, height=2)
HeightLanding = tk.IntVar()
Heightlanding = tk.Entry(window, show=None, font=('Arial', 14),textvariable=HeightLanding)

l6 = tk.Label(window, text='风速(m/s)', bg='grey', font=('Arial', 12), width=30, height=2)
WindSpeed_ini = tk.IntVar()
Windspeed_ini = tk.Entry(window, show=None, font=('Arial', 14),textvariable=WindSpeed_ini)


l1.pack()    
Totalrange.pack()

l4.pack()
Heighttakeoff.pack()

l2.pack()
HeightFixclimb.pack()

l3.pack()
HeightFixdescend.pack()

l5.pack()
Heightlanding.pack()

l6.pack()
Windspeed_ini.pack()

def toint():
    global TotalRange_int,HeightTakeoff_int,HeightFixClimb_int,HeightFixDescend_int,HeightLanding_int,WindSpeed
    
    TotalRange_int = int(TotalRange.get())

    HeightTakeoff_int = int(HeightTakeoff.get())

    HeightFixClimb_int = int(HeightFixClimb.get())

    HeightFixDescend_int = int(HeightFixDescend.get())

    HeightLanding_int = int(HeightLanding.get())
    
    WindSpeed = int(WindSpeed_ini.get())
########    画布
#   
##    screensize(canvwidth=TotalRange_int*1005, canvheight=None, bg=None)
#    left(90)
#    forward(HeightTakeoff_int/10)
#    right(90)
#    forward(600/10)
#    left(4.4)
#    forward(HeightFixClimb_int/10/math.asin(4.4/180*math.pi))
#    right(4.4)
##    forward(TotalRange_int*1000-HeightFixClimb_int/math.asin(4.4/180*math.pi)-HeightFixDescend_int/math.asin(8.75/180*math.pi))
#    forward(TotalRange_int*5)
#    right(8.75)
#    forward(HeightFixDescend_int/10/math.asin(8.75/180*math.pi))
#    left(8.75)
#    forward(1000/10)
#    right(90)
#    forward(HeightLanding_int/10)
################################################################################################

class Range(object):

    def __init__(self):
        #任务剖面输入
        self.TotalRange=TotalRange_int#总航程，km,用于任务可行性评估，不用于航程计算

        self.HeightTakeoff=HeightTakeoff_int#旋翼起飞高度，m
        self.HeightFixClimb=HeightFixClimb_int#固定翼爬升高度，m
        self.HeightFixDescend=HeightFixDescend_int#固定翼下降高度,m
        self.HeightLanding=HeightLanding_int#旋翼降落高度，m
        
        
        #一般不需修改
        self.Rm=36#Ah
        self.Voltage=50.05#电压体制，V
        self.EnergySaveRatio=0.15#剩余能量比例
        self.ClimbRate=2#旋翼爬升率，m/s
        self.LandingRate=2#旋翼下降率，m/s 
        self.FixClimbRate=2#固定翼爬升率，m/s
        self.FixDescendRate=2#固定翼下降率，m/s
        self.TimeMC2FW=12#切换时间，经验值，s
        self.TimeFW2MC=30#切换时间，经验值，s
        self.TimeFixClimb=self.HeightFixClimb/self.FixClimbRate#固定翼爬升时间，等于固定翼爬升高度/2，s
        self.TimeFixDescend=self.HeightFixDescend/self.FixDescendRate#固定翼下降时间，等于固定翼下降高度/2，s
        self.RangeCruise=self.TotalRange-(self.TimeFixClimb*AirSpeed+self.TimeFixDescend*AirSpeed)/1000#巡航航程，km,用于任务可行性评估，不用于航程计算
        self.RangeCruise_HW=self.TotalRange-(self.TimeFixClimb*(AirSpeed-WindSpeed)+self.TimeFixDescend*(AirSpeed-WindSpeed))/1000#巡航航程，km,用于任务可行性评估，不用于航程计算
        
    def Expected(self):
        #################################计算电池重量
        WeightTakeoff=38 #无人机起飞重量,kg
        num=1 #起降次数             
#        WeightStructureRatio=0.35 #结构重量系数
#        WeightStructure=WeightTakeoff*WeightStructureRatio#结构重量，kg
#        WeightAvionics=2#机载设备重量，kg
#        WeightCruisePower=1.4#巡航动力系统重量，kg
#        WeightRotorPower=4.4#旋翼动力系统重量,kg
#        WeightWiring=1.5#线束重量，kg
#        WeightPayload=0.8#载重，kg
#        WeightElse=0#其他重量，kg
#        WeightBattery=WeightTakeoff-WeightStructure-WeightAvionics-WeightCruisePower-WeightRotorPower-WeightWiring-WeightPayload-WeightElse
#        WeightBattery=9.95#电池重量，kg
        
        #####################################计算飞行可用电量
#        EnergyDensity=180#锂电池能量密度，Wh/kg
#        self.EnergySaveRatio=0.15#剩余能量比例
        
        deg2rad=math.pi/180
#        Energy=WeightBattery*EnergyDensity#电池输出总能量，Wh
        Energy=self.Rm*self.Voltage#电池输出总能量，Wh
        EfficiencyElectricityDis=0.99#分电板效率
        EnergyFlight=Energy*(1-self.EnergySaveRatio)*EfficiencyElectricityDis#飞行可用能量,Wh
        
        ####################################计算起降阶段用电量
#        self.Voltage=50#电压体制，V
        PowerAvionics=30#航电设备需用功率，W
        ForceEfficiency=5.3#四旋翼电机螺旋桨综合力效,g/W
        FM=0.7
        Density=1.225
        InclineAngle=10#电机倾斜角度，°
        
#        self.HeightTakeoff=100#旋翼起高度，m
#        self.ClimbRate=2#旋翼爬升率，m/s
#        self.TimeMC2FW=12#起飞旋翼向固定翼转换时间，s
#        self.TimeFW2MC=30.0#降落固定翼向旋翼转换时间，s
#        self.HeightLanding=100#旋翼降落高度，m
#        self.LandingRate=1#旋翼下降率，m/s
        
        DiskLoad=(FM/(1/2/Density)**0.5/9.8**1.5/(ForceEfficiency/1000))**2#盘载，kg/m2
        EfficiencyRotorESC=0.94#旋翼电调效率
        PowerRotor=(WeightTakeoff*1000/math.cos(InclineAngle*deg2rad))/(ForceEfficiency*EfficiencyRotorESC)#悬停输出功率，W
        
        def PowerWiringConsumption(Voltage,ResistanceCruise,Power):
            Current=Power/Voltage
            PowerConsumption=Current**2*ResistanceCruise
            return PowerConsumption
        
        ResistanceRotor=0.018#单根旋翼供电线路电阻，欧姆
        PowerRotorWiring=4*PowerWiringConsumption(self.Voltage,ResistanceRotor,PowerRotor/4.0)#悬停状态线损功率,W
        PowerTakeoffLanding=PowerRotor+PowerRotorWiring+PowerAvionics#起降状态功率
        CurrentRotor=PowerTakeoffLanding/self.Voltage#悬停电流
               
        TimeTakeoff=self.HeightTakeoff/self.ClimbRate+10#爬升时间,s  假定航向调整需要10s
        Timelanding=(self.HeightLanding-20)/self.LandingRate+17/1.5+6+20#降落时间，假定最后3m需6s，旋翼飞到降落点需20s
        TimeRotor=TimeTakeoff+self.TimeMC2FW+self.TimeFW2MC+Timelanding#旋翼状态时间，s
        TimeRotorH=TimeRotor/3600.0#量纲转换，旋翼状态时间，h
        EnergyTakeoffLanding=PowerTakeoffLanding*TimeRotorH#起降能量需求，Wh
    
        ########################根据前飞可用电量计算航程
        g=9.8#重力加速度，m/s2
        K=14#巡航升阻比
        
        
        Drag=WeightTakeoff*g/K#巡航阻力,N        
        PowerPropeller=Drag*AirSpeed#螺旋桨输出功率，W
        
                
        EfficiencyCriusePropeller=0.68#推进螺旋桨效率
        EfficiencyCriuseMotor=0.88#推进电机效率
        EfficiencyCriuseESC=0.94#推进电调效率
        PowerCruiseBoost=PowerPropeller/(EfficiencyCriusePropeller*EfficiencyCriuseMotor*EfficiencyCriuseESC)#巡航推进功率
        ResistanceCruise=0.0162#巡航推进电路电阻，欧姆
        PowerCriuseWiring=PowerWiringConsumption(self.Voltage,ResistanceCruise,(PowerCruiseBoost+PowerAvionics))#巡航状态线损功率,W
        PowerCruise=PowerCruiseBoost+PowerCriuseWiring+PowerAvionics#巡航功率,W
        CurrentCruise=PowerCruise/self.Voltage#巡航电流,A
        

        PowerPropellerClimb=(Drag+WeightTakeoff*g*math.sin(math.atan(self.FixClimbRate/AirSpeed)))*AirSpeed#爬升功率
        PowerClimbBoost=PowerPropellerClimb/(EfficiencyCriusePropeller*EfficiencyCriuseMotor*EfficiencyCriuseESC)#爬升推进功率
        PowerClimbWiring=PowerWiringConsumption(self.Voltage,ResistanceCruise,(PowerClimbBoost+PowerAvionics))#爬升线损功率,W
        PowerClimb=PowerClimbBoost+PowerClimbWiring+PowerAvionics#爬升功率,W
        EnergyClimb=PowerClimb*self.TimeFixClimb/3600#爬升耗能，wh
        RangeClimb=self.TimeFixClimb*AirSpeed/1000#爬升航程，km
        
        if Drag-WeightTakeoff*g*math.sin(math.atan(self.FixClimbRate/AirSpeed)) > 0:
            PowerPropellerDescend=(Drag-WeightTakeoff*g*math.sin(math.atan(self.FixClimbRate/AirSpeed)))*AirSpeed#下滑功率
        else:
            PowerPropellerDescend=0
        PowerDescendBoost=PowerPropellerDescend/(EfficiencyCriusePropeller*EfficiencyCriuseMotor*EfficiencyCriuseESC)#下滑推进功率
        PowerDescendWiring=PowerWiringConsumption(self.Voltage,ResistanceCruise,(PowerDescendBoost+PowerAvionics))#下滑线损功率,W
        PowerDescend=PowerDescendBoost+PowerDescendWiring+PowerAvionics#下滑功率,W
        EnergyDescend=PowerDescend*self.TimeFixDescend/3600#下滑耗能，wh
        RangeDescend=self.TimeFixDescend*AirSpeed/1000#下滑航程，km
        
        EnergyCruise=EnergyFlight-(EnergyTakeoffLanding+EnergyClimb+EnergyDescend)*num#巡航可用电量，Wh
        TimeCruise=EnergyCruise/PowerCruise#续航时间,h
        TimeCruiseMin=TimeCruise*60.0#续航时间，min
        RangeExpected=AirSpeed*3.6*TimeCruise+RangeDescend+RangeClimb+(self.TimeMC2FW*AirSpeed/2+self.TimeFW2MC*AirSpeed/2)/1000#航程，km
        
        ################任务可行性评估
        #无风
        TimeCruiseMFA=self.RangeCruise*1000/AirSpeed/3600
        EnergyCruiseMFA=TimeCruiseMFA*PowerCruise#wh
        EnergyConsumptionExpected=(EnergyTakeoffLanding+EnergyCruiseMFA+EnergyClimb+EnergyDescend)/self.Voltage
        
        #逆风headwind
        TimeCruiseMFA_HW=self.RangeCruise_HW*1000/(AirSpeed-WindSpeed)/3600
        EnergyCruiseMFA_HW=TimeCruiseMFA_HW*PowerCruise#wh
        EnergyConsumptionExpected_HW=(EnergyTakeoffLanding+EnergyCruiseMFA_HW+EnergyClimb+EnergyDescend)/self.Voltage
        
        return RangeExpected,EnergyConsumptionExpected,EnergyConsumptionExpected_HW#,PowerCruise#,WeightBattery,TimeCruiseMin,PowerCruise,PowerTakeoffLanding,EnergyCruise,DiskLoad

    def Typical(self):
        TimeRotorClimb=self.HeightTakeoff/self.ClimbRate+10#垂起时间，s  假定航向调整需10s
        TimeRotorDescend=(self.HeightLanding-20)/self.LandingRate+17/1.5+6+20#垂降时间，s
#        self.TimeMC2FW=12#切换时间，经验值，s
#        self.TimeFW2MC=30#切换时间，经验值，s
        
        PowerRotorClimb_Typical=7500#旋翼爬升典型功耗，经验值，W
#        PowerRotorClimb_Max=8473#旋翼爬升最大功耗，经验值，W
        
        PowerMC2FW_Typical=7864#切换典型功耗，经验值，W
#        PowerMC2FW_Max=9264#切换最大功耗，经验值，W

        PowerFixClimb_Typical=2660#固定翼爬升典型功耗，经验值，W
#        PowerFixClimb_Max=3564#固定翼爬升最大功耗，经验值，W
        
        PowerFixCruise_Typical=1376#固定翼盘旋典型功耗，经验值，W
#        PowerFixCruise_Max=1624#固定翼盘旋最大功耗，经验值，W
        
        PowerFixDescend_Typical=589#固定翼下降典型功耗，经验值，W
#        PowerFixDescend_Max=977#固定翼下降最大功耗，经验值，W
        
        PowerFW2MC_Typical=3353#切换典型功耗，经验值，W
#        PowerFW2MC_Max=4733#切换最大功耗，经验值，W
        
        PowerRotorDescend_Typical=6180#旋翼下降典型功耗，经验值，W
#        PowerRotorDescend_Max=6846#旋翼下降最大功耗，经验值，W
        
        Energy=self.Rm*self.Voltage#电池输出总能量，Wh#wh
        TimeCruise_Typical=(Energy*(1-self.EnergySaveRatio)-(PowerRotorClimb_Typical*TimeRotorClimb\
                            +PowerMC2FW_Typical*self.TimeMC2FW+PowerFixClimb_Typical*self.TimeFixClimb+\
                            PowerFixDescend_Typical*self.TimeFixDescend+PowerFW2MC_Typical*self.TimeFW2MC\
                            +PowerRotorDescend_Typical*TimeRotorDescend)/3600)/PowerFixCruise_Typical
        RangeCruise_Typical=TimeCruise_Typical*3600*AirSpeed/1000
        Range_Typical=(self.TimeMC2FW*AirSpeed/2+self.TimeFW2MC*AirSpeed/2+self.TimeFixClimb*AirSpeed+self.TimeFixDescend*AirSpeed)/1000+RangeCruise_Typical       
        
        #######任务可行性评估  
        
        TimeCruise_TypicalMFA=self.RangeCruise*1000/AirSpeed#巡航时间,s
        EnergyConsumption_Typical=(PowerRotorClimb_Typical*TimeRotorClimb+PowerMC2FW_Typical*self.TimeMC2FW\
                                   +PowerFixClimb_Typical*self.TimeFixClimb+PowerFixDescend_Typical*self.TimeFixDescend\
                                   +PowerFW2MC_Typical*self.TimeFW2MC+PowerRotorDescend_Typical*TimeRotorDescend\
                                   +TimeCruise_TypicalMFA*PowerFixCruise_Typical)/3600/self.Voltage
        EnergyRemain_Typical=Energy/self.Voltage-EnergyConsumption_Typical
        
        #逆风headwind
        TimeCruise_TypicalMFA_HW=self.RangeCruise_HW*1000/(AirSpeed-WindSpeed)#巡航时间,s
        aa=PowerRotorClimb_Typical*TimeRotorClimb
        EnergyConsumption_Typical_HW=(PowerRotorClimb_Typical*TimeRotorClimb+PowerMC2FW_Typical*self.TimeMC2FW\
                                   +PowerFixClimb_Typical*self.TimeFixClimb+PowerFixDescend_Typical*self.TimeFixDescend\
                                   +PowerFW2MC_Typical*self.TimeFW2MC+PowerRotorDescend_Typical*TimeRotorDescend\
                                   +TimeCruise_TypicalMFA_HW*PowerFixCruise_Typical)/3600/self.Voltage
        EnergyRemain_Typical_HW=Energy/self.Voltage-EnergyConsumption_Typical_HW
        
        return Range_Typical,EnergyConsumption_Typical,EnergyConsumption_Typical_HW
    
###########################################################################################  
  
def answer():        
    mbox.showinfo(title='任务可行性评估', message='理论计算航程为%.2fkm，理论计算典型单次起降耗电为%.2fah，理论计算逆风%.1fm/s单次起降耗电为%.2fah;\n实际典型航程为%.2fkm，实际典型单次起降耗电为%.2fah,实际逆风%.1fm/s单次起降耗电为%.2fah'%(Range().Expected()[0],Range().Expected()[1],WindSpeed,Range().Expected()[2],Range().Typical()[0],Range().Typical()[1],WindSpeed,Range().Typical()[2]))

clickButton1 = tk.Button(window,text="Firstly, click Here",command=toint)
clickButton2 = tk.Button(window,text="Then, click Here",command=answer)
clickButton1.pack()
clickButton2.pack()

window.mainloop()
