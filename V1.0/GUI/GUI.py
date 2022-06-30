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
from typing_extensions import IntVar
import numpy as np

from Utils.Param import Param
from Core.CoreModule import Core

# constance for all future inputs in the gui

precision = np.longdouble


# configuration of the gui


class GUI:
    def __init__(self, param: Param, core: Core):
        
        
        # main settings of the interface
        
        gui_main = tk.Tk()
        gui_main.title("Synchrotron Projekt")
        gui_main.geometry("1200x490")
        #gui_main.resizable(width=0,height=0)

        
        # configuration of the labels and entrys for the integration settings
        
        labelIntegrationSettings = tk.Label(gui_main,text="Integration Settings: ",font="Arial 16")
        labelIntegrationSettings.grid(row=0,column=1,pady=14)
        
        labelnptazim = tk.Label(gui_main,text="Npt azimuthal: ",font="Arial 14 ")
        labelnptazim.grid(row=1,column=1,sticky=tk.W)
        valueEntrynptazim = tk.StringVar()
        Entrynptazim = tk.Entry(gui_main,textvariable = valueEntrynptazim,width=15)
        Entrynptazim.grid(row=1,column=2,sticky=tk.W)
   
        labelRadSteps = tk.Label(gui_main,text="Npt radial: ",font="Arial 14 ")
        labelRadSteps.grid(row=2,column=1,sticky=tk.W)
        valueEntryRadSteps = tk.StringVar()
        EntryRadSteps = tk.Entry(gui_main,textvariable = valueEntryRadSteps,width=15)
        EntryRadSteps.grid(row=2,column=2,sticky=tk.W)
        
        labelRadialRange = tk.Label(gui_main,text="Radial range: ",font="Arial 14 ")
        labelRadialRange.grid(row=3,column=1,sticky=tk.W)
        valueEntryRadialRange = tk.StringVar()
        EntryRadialRange = tk.Entry(gui_main,textvariable = valueEntryRadialRange,width=15)
        EntryRadialRange.grid(row=3,column=2,sticky=tk.W)
        
        
        # configuration of the labels and entrys of the experiment constances
        
        labelExperimentConstance = tk.Label(gui_main,text="Experiment Constance: ",font="Arial 16")
        labelExperimentConstance.grid(row=0,column=3,sticky=tk.W,pady=14)
        
        labelEModule = tk.Label(gui_main,text="E-Modules: ",font="Arial 14 ")
        labelEModule.grid(row=1,column=3,sticky=tk.W)
        valueEntryEModules = tk.StringVar()
        EntryEModules = tk.Entry(gui_main,textvariable=valueEntryEModules,width=15)
        EntryEModules.grid(row=1,column=4,sticky=tk.W)
        
        labelPossionszahlen = tk.Label(gui_main,text="Poisson's ratio´s: ",font="Arial 14 ")
        labelPossionszahlen.grid(row=2,column=3,sticky=tk.W)
        valueEntryPossionszahlen = tk.StringVar()
        EntryPossionszahlen = tk.Entry(gui_main,textvariable = valueEntryPossionszahlen,width=15)
        EntryPossionszahlen.grid(row=2,column=4,sticky=tk.W)
        
        labeld0 = tk.Label(gui_main,text="d0: ",font="Arial 14 ")
        labeld0.grid(row=3,column=3,sticky=tk.W)
        valueEntryd0 = tk.StringVar()
        Entryd0 = tk.Entry(gui_main,textvariable = valueEntryd0,width=15)
        Entryd0.grid(row=3,column=4,sticky=tk.W)
        
        labelWavelength = tk.Label(gui_main,text="Wavelength: ",font="Arial 14 ")
        labelWavelength.grid(row=4,column=3,sticky=tk.W)
        varWaveLength = tk.StringVar() 
        EntryWavelength = tk.Entry(gui_main,textvariable=varWaveLength,width=15)
        EntryWavelength.grid(row=4,column=4,sticky=tk.W)
        
        labelPositionsdatenX = tk.Label(gui_main,text="Positions X: ",font="Arial 14 ")
        labelPositionsdatenX.grid(row=5,column=3,sticky=tk.W)
        valueEntryPositionsdatenX = tk.StringVar()
        EntryPositionsdatenX = tk.Entry(gui_main,textvariable = valueEntryPositionsdatenX,width=15)
        EntryPositionsdatenX.grid(row=5,column=4,sticky=tk.W)
        
        labelPositionsdatenY = tk.Label(gui_main,text="Positions Y: ",font="Arial 14 ")
        labelPositionsdatenY.grid(row=6,column=3,sticky=tk.W)
        valueEntryPositionsdatenY = tk.StringVar()
        EntryPositionsdatenY = tk.Entry(gui_main,textvariable = valueEntryPositionsdatenY,width=15)
        EntryPositionsdatenY.grid(row=6,column=4,sticky=tk.W)
        

        # configuration of the labels and entrys for the analysis parameters
        
        labelAnalysisParams = tk.Label(gui_main,text="Analysis Parameters: ",font="Arial 16")
        labelAnalysisParams.grid(row=0,column=5,sticky=tk.W,pady=14)
        
        labelStartTemp = tk.Label(gui_main,text="Temperature: ",font="Arial 14 ")
        labelStartTemp.grid(row=1,column=5,sticky=tk.W)
        valueEntryStartTemp = tk.StringVar()
        EntryStartTemp = tk.Entry(gui_main,textvariable = valueEntryStartTemp,width=15)
        EntryStartTemp.grid(row=1,column=6,sticky=tk.W)
             
        labelThetaav = tk.Label(gui_main,text="Theta Av: ",font="Arial 14 ")
        labelThetaav.grid(row=2,column=5,sticky=tk.W)
        valueEntryThetaav = tk.StringVar()
        EntryThetaav = tk.Entry(gui_main,textvariable = valueEntryThetaav,width=15)
        EntryThetaav.grid(row=2,column=6,sticky=tk.W)
        
        labelMinTheta = tk.Label(gui_main,text="Min. Theta: ",font="Arial 14 ")
        labelMinTheta.grid(row=3,column=5,sticky=tk.W)
        valueEntryMinTheta = tk.StringVar()
        EntryMinTheta = tk.Entry(gui_main,textvariable = valueEntryMinTheta,width=15)
        EntryMinTheta.grid(row=3,column=6,sticky=tk.W)
        
        labelMaxTheta = tk.Label(gui_main,text="Max. Theta: ",font="Arial 14 ")
        labelMaxTheta.grid(row=4,column=5,sticky=tk.W)
        valueEntryMaxTheta = tk.StringVar()
        EntryMaxTheta = tk.Entry(gui_main,textvariable = valueEntryMaxTheta,width=15)
        EntryMaxTheta.grid(row=4,column=6,sticky=tk.W)
         
        labelPeak = tk.Label(gui_main,text="Peak: ",font="Arial 14 ")
        labelPeak.grid(row=5,column=5,sticky=tk.W)
        valueEntryPeak = tk.StringVar()
        EntryPeak = tk.Entry(gui_main,textvariable = valueEntryPeak,width=15)
        EntryPeak.grid(row=5,column=6,sticky=tk.W)
        
        
        # empty labels to create space between actual elements
        
        labelclear11 = tk.Label(gui_main,text="    ")
        labelclear11.grid(row=1,column=0)
        labelclear12 = tk.Label(gui_main,text="    ")
        labelclear12.grid(row=2,column=0)
        labelclear13 = tk.Label(gui_main,text="    ")
        labelclear13.grid(row=3,column=0)
        labelclear14 = tk.Label(gui_main,text="    ")
        labelclear14.grid(row=4,column=0)
        labelclear15 = tk.Label(gui_main,text="    ")
        labelclear15.grid(row=5,column=0)
        labelclear16 = tk.Label(gui_main,text="    ")
        labelclear16.grid(row=6,column=0)
        labelclear17 = tk.Label(gui_main,text="    ")
        labelclear17.grid(row=7,column=0)
        labelclear18 = tk.Label(gui_main,text="    ")
        labelclear18.grid(row=8,column=0)
        labelclear19 = tk.Label(gui_main,text="    ")
        labelclear19.grid(row=9,column=0)
        labelclear20 = tk.Label(gui_main,text="    ")
        labelclear20.grid(row=10,column=0)
        labelclear21 = tk.Label(gui_main,text="    ")
        labelclear21.grid(row=11,column=0)
        labelclear22 = tk.Label(gui_main,text="    ")
        labelclear22.grid(row=12,column=0)
        labelclear23 = tk.Label(gui_main,text="    ")
        labelclear23.grid(row=13,column=0)
        labelclear24 = tk.Label(gui_main,text="    ")
        labelclear24.grid(row=14,column=0)
        labelclear25 = tk.Label(gui_main,text="    ")
        labelclear25.grid(row=15,column=0)

        
        # defining vars used in the checkbuttons
    
        
        varPseudoVoigtFit = tk.IntVar()
        varAzimuthalIntegration = tk.IntVar()
        varAxistransformation = tk.IntVar()
        checkBoxVars = [varAzimuthalIntegration,varAxistransformation,varPseudoVoigtFit]
        
        #Checkbuttons
        
        CheckbuttonPseudoVoigtFit = tk.Checkbutton(gui_main,text="PseudoVoigt Fit",font="Arial 14",variable=varPseudoVoigtFit)
        CheckbuttonPseudoVoigtFit.grid(row=11,column=2,columnspan=2)
        
        CheckbuttonAzimuthalIntegration = tk.Checkbutton(gui_main,text="Azimuthal Integration",font="Arial 14",variable=varAzimuthalIntegration)
        CheckbuttonAzimuthalIntegration.grid(row=11,column=4,columnspan=2)

        CheckbuttonAxistransformation = tk.Checkbutton(gui_main,text="Axistransformation",font="Arial 14",variable=varAxistransformation)
        CheckbuttonAxistransformation.grid(row=11,column=3,columnspan=2)
        
        def var_states():
            selectedTasks = []
            for taskName, isSelected in zip(["azimuthal_integration","axisTransform_fit","pseudoVoigt_fit"],checkBoxVars):
                if(isSelected):
                    selectedTasks.append(taskName)
            
            param.setTasks(selectedTasks)


        
        # defining all methonds used in the buttons to chose input and output files
        
        def chooseOutputDirectory():
            outputDirectory = filedialog.askdirectory()
            param.setOutputDirectory(outputDirectory)
            
        def openAzimJson():
            azimJsonPath = filedialog.askopenfile()
            param.setPathToAzimJson(os.path.abspath(azimJsonPath.name))
            
        def selectDetectorData():
            cbfInputs = tkfilebrowser.askopendirnames()
            param.setDirectoryPaths(cbfInputs)
         
         
        def openELabFTW(): # CHANGED BY AZ
            elabJsonPath = filedialog.askopenfilename()
            with open(elabJsonPath, "r") as file:
                paramJson = dict(json.load(file))
            arr = np.arange(paramJson["pos_insitu"]["x_start"]["value"],paramJson["pos_insitu"]["x_end"]["value"],paramJson["pos_insitu"]["x_step"]["value"]/1000)
            ad = ",".join(map(str,np.arange(paramJson["pos_insitu"]["x_start"]["value"],paramJson["pos_insitu"]["x_end"]["value"],paramJson["pos_insitu"]["x_step"]["value"]/1000)))
            EntryPositionsdatenX.insert(0,",".join(map(str,np.arange(paramJson["pos_insitu"]["x_start"]["value"],paramJson["pos_insitu"]["x_end"]["value"],paramJson["pos_insitu"]["x_step"]["value"]/1000))))
            EntryPositionsdatenY.insert(0,",".join(map(str,np.arange(paramJson["pos_insitu"]["z_start"]["value"],paramJson["pos_insitu"]["z_end"]["value"],paramJson["pos_insitu"]["z_step"]["value"]/1000))))
            param.setDirectoryPaths(paramJson["datafiles"].keys())
            param.setElabFtwJson(paramJson)
        
        
        # buttons for input and ouput
        
        buttonLoadAzimJson = tk.Button(gui_main,text="Load Azim.json",font="Arial 14",command=openAzimJson,width=22,height=1)
        buttonLoadAzimJson.grid(row=9,column=2,sticky=tk.W)
        
        buttonChooseOutputDirectory = tk.Button(gui_main,text="Choose output directory",font="Arial 14",width=22,height=1,command =chooseOutputDirectory)
        buttonChooseOutputDirectory.grid(row=9,column=3,sticky=tk.W)
        
        buttonSelectCbfInputs = tk.Button(gui_main,text="Select Detector Binary´s",font="Arial 14",width=22,height=1,command =selectDetectorData)
        buttonSelectCbfInputs.grid(row=9,column=4,sticky=tk.W)
        
        buttonELabJson = tk.Button(gui_main,text="Load Elab",font="Arial 14", command = openELabFTW,width=22,height=1)
        buttonELabJson.grid(row=9,column=5,sticky=tk.W)
        
        
        # starting the process and saving the values of every entry in the Param class
        
        def startProgressbar():
            array = EntryEModules.get().split(",")
            emoduls = [precision(emodul) for emodul in EntryEModules.get().split(",")]
            param.setEModules(emoduls)
            
            possionszahlen = [precision(possionszahl) for possionszahl in EntryPossionszahlen.get().split(",")]
            param.setPoissonNumbers(possionszahlen)
            
            d0p = precision(Entryd0.get().split(","))[0]
            param.setD0(d0p)
            
            wavelengthp = precision(EntryWavelength.get().split(","))[0]
            param.setWavelength(wavelengthp)
            
            positionsdatenxp = [precision(positionsdatenX) for positionsdatenX in EntryPositionsdatenX.get().split(",")]
            param.setPositionsX(positionsdatenxp)
            
            positionsdatenyp = [precision(positionsdatenY) for positionsdatenY in EntryPositionsdatenY.get().split(",")]
            param.setPositionsY(positionsdatenyp)
            
            starttempp = precision(EntryStartTemp.get().split(","))[0]
            param.setStartTemp(starttempp)
            
            thetaavp = [precision(thetaAV) for thetaAV in EntryThetaav.get().split(",")]
            param.thetaAV(thetaavp)
            
            minthetap = precision(EntryMinTheta.get().split(","))[0]
            param.setMinTheta(minthetap)
            
            maxthetap = precision(EntryMaxTheta.get().split(","))[0]
            param.setMaxTheta(maxthetap)
            
            peakp = precision([EntryPeak.get()])[0]
            param.setPeak(peakp)
            test = EntryRadSteps.get()
            radstepsp = np.array(Entrynptazim.get().split(","),dtype='|S10').astype(np.longdouble)[0]
            print(radstepsp)
            param.setRadSteps(radstepsp)
            
            radrangep = [precision(radRange) for radRange in EntryRadialRange.get().split(",")]
            param.setRadialRange(tuple(radrangep))
            nptAzim =  np.array(Entrynptazim.get().split(","),dtype='|S10').astype(np.longdouble)[0].item()
            print(nptAzim)
            param.setNptAzim(nptAzim)
            
            progressbar.start()
            param.setProgressBarHandles([progressbar])
            var_states()
            
            core.run()
            
            
        # defining method to stop the process and close the window, used in buttonStop
        
        def stopProgressbar():
            progressbar.stop()
            gui_main.quit()
            
        
        # label for the progress bar
        
        labelProgessbar= tk.Label(gui_main,text="Progress: ",font="Artial 16")
        labelProgessbar.grid(row=13,column=1)
        
        
        # settings for the progress bar
        
        progressbarValue = tk.IntVar()
        progressbarValue.set(1)  
         
        progressbar = tkk.Progressbar(gui_main,orient="horizontal",mode="determinate",maximum=100,variable=progressbarValue,length=920)
        progressbar.grid(row=13,column=2,columnspan=5,sticky=tk.W)
        
       
        # buttons to start and stop the process
        
        buttonStart = tk.Button(gui_main,text="Start",font="Arial 14",command=startProgressbar,width=22,height=2)
        buttonStart.grid(row=15,column=3,padx=5)
        
        buttonStop = tk.Button(gui_main,text="Stop",font="Arial 14",command=stopProgressbar,width=22,height=2)
        buttonStop.grid(row=15,column=4,padx=5)
        


    
        

        gui_main.mainloop()
        
