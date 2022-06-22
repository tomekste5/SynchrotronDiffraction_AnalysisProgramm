#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 25 09:42:29 2022

@author: luca
"""

# imports

from distutils import command
import tkinter as tk
import tkinter.ttk as tkk
from tkinter import filedialog
import tkfilebrowser
import json

import sys
import os
import numpy as np

from Utils.Param import param
from Core.CoreModule import Core
    
    
# constance for all future inputs in the gui

precision = np.longdouble


# configuration of the gui


class GUI:
    def __init__(self, param: param, core: Core):
        
        
        # main settings of the interface
        
        gui_main = tk.Tk()
        gui_main.title("Synchrotron Projekt")
        gui_main.geometry("840x400")
        gui_main.resizable(width=0,height=0)
        
        
        # configuration of the labels and entrys for the integration settings
        
        labelIntegrationSettings = tk.Label(gui_main,text="Integration Settings: ",font="Arial 16")
        labelIntegrationSettings.place(x=20,y=20)
        
        labelnptazim = tk.Label(gui_main,text="Npt azimuthal: ",font="Arial 14 ")
        labelnptazim.place( x = 20 , y = 55 )
        valueEntrynptazim = tk.StringVar()
        Entrynptazim = tk.Entry(gui_main,textvariable = valueEntrynptazim)
        Entrynptazim.place( x = 155 , y = 53 , width = 100 , height = 25)
   
        labelRadSteps = tk.Label(gui_main,text="Npt radial",font="Arial 14 ")
        labelRadSteps.place( x = 20 , y = 85 )
        valueEntryRadSteps = tk.StringVar()
        EntryRadSteps = tk.Entry(gui_main,textvariable = valueEntryRadSteps)
        EntryRadSteps.place( x = 155 , y = 83 , width = 100 , height = 25)
        
        labelRadialRange = tk.Label(gui_main,text="Radial range: ",font="Arial 14 ")
        labelRadialRange.place( x = 20 , y = 115 )
        valueEntryRadialRange = tk.StringVar()
        EntryRadialRange = tk.Entry(gui_main,textvariable = valueEntryRadialRange)
        EntryRadialRange.place( x = 155 , y = 113 , width = 100 , height = 25)
        
        
        # configuration of the labels and entrys of the experiment constances
        
        labelExperimentConstance = tk.Label(gui_main,text="Experiment Constance: ",font="Arial 16")
        labelExperimentConstance.place(x=310,y=20)
        
        labelEModule = tk.Label(gui_main,text="E-Modules: ",font="Arial 14 ")
        labelEModule.place( x = 310 , y = 55 )
        valueEntryEModules = tk.StringVar()
        EntryEModules = tk.Entry(gui_main,textvariable=valueEntryEModules)
        EntryEModules.place( x = 430 , y = 53 , width = 100 , height = 25)
        
        labelPossionszahlen = tk.Label(gui_main,text="Poisson's ratio´s: ",font="Arial 14 ")
        labelPossionszahlen.place( x = 310 , y = 85 )
        valueEntryPossionszahlen = tk.StringVar()
        EntryPossionszahlen = tk.Entry(gui_main,textvariable = valueEntryPossionszahlen)
        EntryPossionszahlen.place( x = 430 , y = 83 , width = 100 , height = 25)
        
        labeld0 = tk.Label(gui_main,text="d0: ",font="Arial 14 ")
        labeld0.place( x = 310 , y = 115 )
        valueEntryd0 = tk.StringVar()
        Entryd0 = tk.Entry(gui_main,textvariable = valueEntryd0)
        Entryd0.place( x = 430 , y = 113 , width = 100 , height = 25)
        
        labelWavelength = tk.Label(gui_main,text="Wavelength: ",font="Arial 14 ")
        labelWavelength.place( x = 310 , y = 145 )
        varWaveLength = tk.StringVar() 
        EntryWavelength = tk.Entry(gui_main,textvariable=varWaveLength)
        EntryWavelength.place( x = 430 , y = 143 , width = 100 , height = 25)
        
        labelPositionsdatenX = tk.Label(gui_main,text="Positions X: ",font="Arial 14 ")
        labelPositionsdatenX.place( x = 310 , y = 175 )
        valueEntryPositionsdatenX = tk.StringVar()
        EntryPositionsdatenX = tk.Entry(gui_main,textvariable = valueEntryPositionsdatenX)
        EntryPositionsdatenX.place( x = 430 , y = 173 , width = 100 , height = 25)
        
        labelPositionsdatenY = tk.Label(gui_main,text="Positions Y: ",font="Arial 14 ")
        labelPositionsdatenY.place( x = 310 , y = 205 )
        valueEntryPositionsdatenY = tk.StringVar()
        EntryPositionsdatenY = tk.Entry(gui_main,textvariable = valueEntryPositionsdatenY)
        EntryPositionsdatenY.place( x = 430 , y = 203 , width = 100 , height = 25)
        

        # configuration of the labels and entrys for the analysis parameters
        
        labelAnalysisParams = tk.Label(gui_main,text="Analysis Parameters: ",font="Arial 16")
        labelAnalysisParams.place(x=590,y=20)
        
        labelStartTemp = tk.Label(gui_main,text="Temperature: ",font="Arial 14 ")
        labelStartTemp.place( x = 590 , y = 55 )
        valueEntryStartTemp = tk.StringVar()
        EntryStartTemp = tk.Entry(gui_main,textvariable = valueEntryStartTemp)
        EntryStartTemp.place( x = 710 , y = 53 , width = 100 , height = 25)
             
        labelThetaav = tk.Label(gui_main,text="Theta Av: ",font="Arial 14 ")
        labelThetaav.place( x = 590 , y = 85 )
        valueEntryThetaav = tk.StringVar()
        EntryThetaav = tk.Entry(gui_main,textvariable = valueEntryThetaav)
        EntryThetaav.place( x = 710 , y = 83 , width = 100 , height = 25)
        
        labelMinTheta = tk.Label(gui_main,text="Min. Theta: ",font="Arial 14 ")
        labelMinTheta.place( x = 590 , y = 115 )
        valueEntryMinTheta = tk.StringVar()
        EntryMinTheta = tk.Entry(gui_main,textvariable = valueEntryMinTheta)
        EntryMinTheta.place( x = 710 , y = 113 , width = 100 , height = 25)
        
        labelMaxTheta = tk.Label(gui_main,text="Max. Theta: ",font="Arial 14 ")
        labelMaxTheta.place( x = 590 , y = 145 )
        valueEntryMaxTheta = tk.StringVar()
        EntryMaxTheta = tk.Entry(gui_main,textvariable = valueEntryMaxTheta)
        EntryMaxTheta.place( x = 710 , y = 143 , width = 100 , height = 25)
         
        labelPeak = tk.Label(gui_main,text="Peak: ",font="Arial 14 ")
        labelPeak.place( x = 590 , y = 175 )
        valueEntryPeak = tk.StringVar()
        EntryPeak = tk.Entry(gui_main,textvariable = valueEntryPeak)
        EntryPeak.place( x = 710 , y = 173 , width = 100 , height = 25)
        
        
        # defining all methonds used in the buttons to chose input and output files
        
        def chooseOutputDirectory():
            outputDirectory = tkfilebrowser.askopendirnames()
            param.setOutputDirectory(outputDirectory)
            
        def openAzimJson():
            azimJsonPath = filedialog.askopenfilename()
            param.setPathToAzimJson(azimJsonPath)
            
        def selectDetectorData():
            cbfInputs = tkfilebrowser.askopendirnames()
            param.setDirectoryPaths(cbfInputs)
         
        def openELabFTW(): # CHANGED BY AZ
            elabJsonPath = filedialog.askopenfilename()
            with open(elabJsonPath, "r") as file:
                paramJson = dict(json.load(file))
            param.setElabFtwJson(paramJson)
        
        
        # buttons for input and ouput
        
        buttonLoadAzimJson = tk.Button(gui_main,text="Load Azim.json",font="Arial 14",command=openAzimJson)
        buttonLoadAzimJson.place(x=430,y=255,width=175,height=30)
        
        buttonChooseOutputDirectory = tk.Button(gui_main,text="Choose output directory",font="Arial 14",command=chooseOutputDirectory)
        buttonChooseOutputDirectory.place(x=625,y=255,width=175,height=30)
        
        buttonSelectCbfInputs = tk.Button(gui_main,text="Select Detector Binary´s",font="Arial 14",command=selectDetectorData)
        buttonSelectCbfInputs.place(x=235,y=255,width=175,height=30)
        
        buttonELabJson = tk.Button(gui_main,text="Load Elab",font="Arial 14", command = openELabFTW) # CHANGED BY AZ
        buttonELabJson.place(x=30,y=255,width=175,height=30)
        
        
        # starting the process and saving the values of every entry in the Param class
        
        def startProgressbar():
            eModules = [precision(eModule) for eModule in valueEntryEModules.split(",")]
            param.setEModules(eModules)
           
            possionszahlen = [precision(possionszahl) for possionszahl in valueEntryPossionszahlen.split(",")]
            param.setPoissonNumbers(possionszahlen)
            
            d0p = [precision(d0) for d0 in valueEntryd0.split(",")]
            param.setD0(d0p)
            
            wavelengthp = [precision(wavelenght) for wavelenght in varWaveLength.split(",")]
            param.setWavelenght(wavelengthp)
            
            positionsdatenxp = [precision(positionsdatenX) for positionsdatenX in valueEntryPositionsdatenX.split(",")]
            param.setPositionsX(positionsdatenxp)
            
            positionsdatenyp = [precision(positionsdatenY) for positionsdatenY in valueEntryPositionsdatenY.split(",")]
            param.setPositionsY(positionsdatenyp)
            
            starttempp = [precision(startTemp) for startTemp in valueEntryStartTemp.split(",")]
            param.setStartTemp(starttempp)
            
            thetaavp = [precision(thetaAV) for thetaAV in valueEntryThetaav.split(",")]
            param.thetaAV(thetaavp)
            
            minthetap = [precision(minThetaAV) for minThetaAV in valueEntryMinTheta.split(",")]
            param.setMinTheta(minthetap)
            
            maxthetap = [precision(maxThetaAV) for maxThetaAV in valueEntryMaxTheta.split(",")]
            param.setMaxTheta(maxthetap)
            
            peakp = [precision(peak) for peak in valueEntryPeak.split(",")]
            param.setPeak(peakp)
            
            radstepsp = [precision(radSteps) for radSteps in valueEntryRadSteps.split(",")]
            param.setRadSteps(radstepsp)
            
            radrangep = [precision(radRange) for radRange in valueEntryRadialRange.split(",")]
            param.setRadialRange(radrangep)
            
            core.run()
            progressbar.start()
            param.setProgressBarHandles()
            
            
        # defining method to stop the process and close the window, used in buttonStop
        
        def stopProgressbar():
            progressbar.stop()
            gui_main.destroy()
            
        
        # label for the progress bar
        
        labelProgessbar= tk.Label(gui_main,text="Progress: ",font="Artial 16")
        labelProgessbar.place(x= 20 ,y=300)
        
        
        # settings for the progress bar
        
        progressbarValue = tk.IntVar()
        progressbarValue.set(1)  
         
        progressbar = tkk.Progressbar(gui_main,orient="horizontal",mode="determinate",maximum=100,variable=progressbarValue)
        progressbar.place(x=115,y=300,width=695,height=30)
        
       
        # buttons to start and stop the process
        
        buttonStart = tk.Button(gui_main,text="Start",font="Arial 14",command=startProgressbar)
        buttonStart.place( x= 290 , y= 350, width=120, height= 30)
        
        buttonStop = tk.Button(gui_main,text="Stop",font="Arial 14",command=stopProgressbar)
        buttonStop.place(x=430,y=350,width=120,height=30)
        


    
        

        gui_main.mainloop()
        
#GUI(Param(),Core())
