#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 25 09:42:29 2022

@author: luca
"""


import tkinter as tk
import tkinter.ttk as tkk

import sys
import os
import numpy as np
sys.path.append(os.path.abspath(os.getcwd()))

import Param

class Core:
    def run():
        pass
    def cancel():
        pass

precision = np.longdouble

class GUI:
    def __init__(self, param: Param, core: Core):
        gui_main = tk.Tk()
        gui_main.title("Synchrotron Projekt")
        gui_main.geometry("840x500")
        gui_main.resizable(width=0,height=0)
        
        labelIntegrationSettings = tk.Label(gui_main,text="Integration Settings: ",font="Arial 16")
        labelIntegrationSettings.place(x=20,y=20)
        
        labelnptazim = tk.Label(gui_main,text="Npt Azim: ",font="Arial 14 ")
        labelnptazim.place( x = 20 , y = 55 )
        Entrynptazim = tk.Entry()
        Entrynptazim.place( x = 155 , y = 53 , width = 100 , height = 25)
   
        labelRadSteps = tk.Label(gui_main,text="Radiation Steps: ",font="Arial 14 ")
        labelRadSteps.place( x = 20 , y = 85 )
        EntryRadSteps = tk.Entry()
        EntryRadSteps.place( x = 155 , y = 83 , width = 100 , height = 25)
        
        labelRadialRange = tk.Label(gui_main,text="Radial range: ",font="Arial 14 ")
        labelRadialRange.place( x = 20 , y = 115 )
        EntryRadialRange = tk.Entry()
        EntryRadialRange.place( x = 155 , y = 113 , width = 100 , height = 25)
        
        
        
        
        labelExperimentConstance = tk.Label(gui_main,text="Experiment Constance: ",font="Arial 16")
        labelExperimentConstance.place(x=310,y=20)
        
        labelEModule = tk.Label(gui_main,text="E-Module: ",font="Arial 14 ")
        labelEModule.place( x = 310 , y = 55 )
        valueEntryEModules = tk.StringVar()
        EntryEModules = tk.Entry(textvariable=valueEntryEModules)
        EntryEModules.place( x = 430 , y = 53 , width = 100 , height = 25)
        
        labelPossionszahlen = tk.Label(gui_main,text="Possionszahlen: ",font="Arial 14 ")
        labelPossionszahlen.place( x = 310 , y = 85 )
        EntryPossionszahlen = tk.Entry()
        EntryPossionszahlen.place( x = 430 , y = 83 , width = 100 , height = 25)
        
        labeld0 = tk.Label(gui_main,text="d0: ",font="Arial 14 ")
        labeld0.place( x = 310 , y = 115 )
        Entryd0 = tk.Entry()
        Entryd0.place( x = 430 , y = 113 , width = 100 , height = 25)
        
        labelWavelength = tk.Label(gui_main,text="Wavelength: ",font="Arial 14 ")
        labelWavelength.place( x = 310 , y = 145 )
        varWaveLength = tk.StringVar() 
        EntryWavelength = tk.Entry(textvariable=varWaveLength)

        EntryWavelength.place( x = 430 , y = 143 , width = 100 , height = 25)
        
        labelPositionsdatenX = tk.Label(gui_main,text="Positionsdaten X: ",font="Arial 14 ")
        labelPositionsdatenX.place( x = 310 , y = 175 )
        EntryPositionsdatenX = tk.Entry()
        EntryPositionsdatenX.place( x = 430 , y = 173 , width = 100 , height = 25)
        
        labelPositionsdatenY = tk.Label(gui_main,text="Positionsdaten Y: ",font="Arial 14 ")
        labelPositionsdatenY.place( x = 310 , y = 205 )
        EntryPositionsdatenY = tk.Entry()
        EntryPositionsdatenY.place( x = 430 , y = 203 , width = 100 , height = 25)
        
        
        
        
        labelAnalysisParams = tk.Label(gui_main,text="Analysis Parameters: ",font="Arial 16")
        labelAnalysisParams.place(x=590,y=20)
        
        labelStartTemp = tk.Label(gui_main,text="Starttemperature: ",font="Arial 14 ")
        labelStartTemp.place( x = 590 , y = 55 )
        EntryStartTemp = tk.Entry()
        EntryStartTemp.place( x = 710 , y = 53 , width = 100 , height = 25)
             
        labelThetaav = tk.Label(gui_main,text="Theta Av: ",font="Arial 14 ")
        labelThetaav.place( x = 590 , y = 85 )
        EntryThetaav = tk.Entry()
        EntryThetaav.place( x = 710 , y = 83 , width = 100 , height = 25)
        
        labelMinTheta = tk.Label(gui_main,text="Minimum Theta: ",font="Arial 14 ")
        labelMinTheta.place( x = 590 , y = 115 )
        EntryMinTheta = tk.Entry()
        EntryMinTheta.place( x = 710 , y = 113 , width = 100 , height = 25)
        
        labelMaxTheta = tk.Label(gui_main,text="Maximum Theta: ",font="Arial 14 ")
        labelMaxTheta.place( x = 590 , y = 145 )
        EntryMaxTheta = tk.Entry()
        EntryMaxTheta.place( x = 710 , y = 143 , width = 100 , height = 25)
         
        labelPeak = tk.Label(gui_main,text="Peak: ",font="Arial 14 ")
        labelPeak.place( x = 590 , y = 175 )
        EntryPeak = tk.Entry()
        EntryPeak.place( x = 710 , y = 173 , width = 100 , height = 25)
        
     
        
        
        buttonLoadParamsJson = tk.Button(gui_main,text="Load Params Json",font="Arial 14")
        buttonLoadParamsJson.place(x=40,y=255,width=160,height=30)
        
        buttonLoadAzimJson = tk.Button(gui_main,text="Load AzimJson",font="Arial 14")
        buttonLoadAzimJson.place(x=240,y=255,width=160,height=30)
        
        buttonLoadELabFtw = tk.Button(gui_main,text="Load ElabFtw",font="Arial 14")
        buttonLoadELabFtw.place(x=440,y=255,width=160,height=30)
        
        
        
        
        #Progressbar
        def startProgressbar():
            #2,3,4,5,5,6,2 -> [2,3,4,5,6]
            8.232523247234723849
            eModules = [precision(eModule) for eModule in valueEntryEModules.split(",")]
            Param.setEModules(eModules)
            core.run()
            
            progressbar.start()
            Param.setProgressBarHandles()
            
        def stopProgressbar():
            progressbar.stop()
            
        def incrementProgressbar():
            progressbarValue.set(progressbarValue()+1)
        
        labelProgessbar= tk.Label(gui_main,text="Progress: ",font="Artial 16")
        labelProgessbar.place(x= 20 ,y=400)
        
        progressbarValue = tk.IntVar(gui_main)
        progressbarValue.set(1)  
         
        progressbar = tkk.Progressbar(gui_main,orient="horizontal",mode="determinate",maximum=100,variable=progressbarValue)
        progressbar.place(x=115,y=400,width=695,height=30)
        
       
        buttonStart = tk.Button(gui_main,text="Start",font="Arial 14",command=startProgressbar)
        buttonStart.place( x= 290 , y= 450, width=120, height= 30)
        
        buttonStop = tk.Button(gui_main,text="Stop",font="Arial 14",command=stopProgressbar)
        buttonStop.place(x=430,y=450,width=120,height=30)
        
        buttonIncrement = tk.Button(gui_main,text="Increment Progressbar",font="Arial 14",command=incrementProgressbar())
        buttonIncrement.place(x=600,y=450,width=120,height=30)
        
        
#Checkbuttons und Progressbar kommen noch --> wohin und was?       
        
        
        gui_main.mainloop()
        
GUI(Param.Param(),Core())
