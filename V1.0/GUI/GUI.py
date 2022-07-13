#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 25 09:42:29 2022

@author: luca
"""

# imports

from ast import Str
import tkinter as tk
import tkinter.ttk as tkk
from tkinter import filedialog
import json

import os
import numpy as np
import tkfilebrowser

from Utils.Param import Param
from Core.CoreModule import Core

# constants for all future inputs in the gui
precision = np.float64


# configuration of the gui
class GUI:
    def __init__(self, param: Param, core: Core):
        """Initializes graphical user interface object

        Args:
            param (Params object): stores all parameters
            core (Core object): current instance object
        """
        
        gui_main = tk.Tk()
        gui_message = tk.Tk()
        gui_main.title("Synchrotron Data Stress Analysis")
        gui_message.title("Attention!")
        gui_main.geometry("1200x490")

        labelEntryTip = tk.Label(gui_message, text = "Small fields are for floats with dot, no comma! Wide fields are for arrays of floats with dot, separated by commas!", font = ("Arial", 14, "italic"))
        labelEntryTip.grid(row = 0, column=0)
        
        # configuration of the labels and entries for the integration settings
        
        labelIntegrationSettings = tk.Label(gui_main,text="Integration Settings: ",font="Arial 16")
        labelIntegrationSettings.grid(row=1,column=1,pady=14)
        
        labelnptazim = tk.Label(gui_main,text="Nbpt azimuthal (1): ",font="Arial 14 ")
        labelnptazim.grid(row=2,column=1,sticky=tk.W)
        valueEntrynptazim = tk.StringVar()
        Entrynptazim = tk.Entry(gui_main,textvariable = valueEntrynptazim,width=15)
        Entrynptazim.grid(row=2,column=2,sticky=tk.W)
   
        labelRadSteps = tk.Label(gui_main,text="Nbpt radial (1): ",font="Arial 14 ")
        labelRadSteps.grid(row=3,column=1,sticky=tk.W)
        valueEntryRadSteps = tk.StringVar()
        EntryRadSteps = tk.Entry(gui_main,textvariable = valueEntryRadSteps,width=15)
        EntryRadSteps.grid(row=3,column=2,sticky=tk.W)
        
        labelRadialRange = tk.Label(gui_main,text="Radial range [start, end] (2 Theta (°)): ",font="Arial 14 ")
        labelRadialRange.grid(row=4,column=1,sticky=tk.W)
        valueEntryRadialRange = tk.StringVar()
        EntryRadialRange = tk.Entry(gui_main,textvariable = valueEntryRadialRange,width=15)
        EntryRadialRange.grid(row=4,column=2,sticky=tk.W)
        
        
        # configuration of the labels and entrys of the experiment Constants
        
        labelExperimentConstants = tk.Label(gui_main,text="Experiment Constants: ",font="Arial 16")
        labelExperimentConstants.grid(row=1,column=3,sticky=tk.W,pady=14)
        
        labelEModule = tk.Label(gui_main,text="E-Modulus Array (Pa): ",font="Arial 14 ")
        labelEModule.grid(row=2,column=3,sticky=tk.W)
        valueEntryEModules = tk.StringVar()
        EntryEModules = tk.Entry(gui_main,textvariable=valueEntryEModules,width=30)
        EntryEModules.grid(row=2,column=4,sticky=tk.W)
        
        labelPossionszahlen = tk.Label(gui_main,text="Poisson's Ratio Array (1): ",font="Arial 14 ")
        labelPossionszahlen.grid(row=3,column=3,sticky=tk.W)
        valueEntryPossionszahlen = tk.StringVar()
        EntryPossionszahlen = tk.Entry(gui_main,textvariable = valueEntryPossionszahlen,width=30)
        EntryPossionszahlen.grid(row=3,column=4,sticky=tk.W)
        
        labeld0 = tk.Label(gui_main,text="d0 (m): ",font="Arial 14 ")
        labeld0.grid(row=4,column=3,sticky=tk.W)
        valueEntryd0 = tk.StringVar()
        Entryd0 = tk.Entry(gui_main,textvariable = valueEntryd0,width=15)
        Entryd0.grid(row=4,column=4,sticky=tk.W)
        
        labelWavelength = tk.Label(gui_main,text="Wavelength (m): ",font="Arial 14 ")
        labelWavelength.grid(row=5,column=3,sticky=tk.W)
        varWaveLength = tk.StringVar() 
        EntryWavelength = tk.Entry(gui_main,textvariable=varWaveLength,width=15)
        EntryWavelength.grid(row=5,column=4,sticky=tk.W)
        
        labelPositionsdatenX = tk.Label(gui_main,text="Position X Array (mm): ",font="Arial 14 ")
        labelPositionsdatenX.grid(row=6,column=3,sticky=tk.W)
        valueEntryPositionsdatenX = tk.StringVar()
        EntryPositionsdatenX = tk.Entry(gui_main,textvariable = valueEntryPositionsdatenX,width=30)
        EntryPositionsdatenX.grid(row=6,column=4,sticky=tk.W)
        
        labelPositionsdatenZ = tk.Label(gui_main,text="Position Z Array (mm): ",font="Arial 14 ")
        labelPositionsdatenZ.grid(row=7,column=3,sticky=tk.W)
        valueEntryPositionsdatenZ = tk.StringVar()
        EntryPositionsdatenZ = tk.Entry(gui_main,textvariable = valueEntryPositionsdatenZ,width=30)
        EntryPositionsdatenZ.grid(row=7,column=4,sticky=tk.W)

        # configuration of the labels and entrys for the analysis parameters
        
        labelAnalysisParams = tk.Label(gui_main,text="Analysis Parameters: ",font="Arial 16")
        labelAnalysisParams.grid(row=1,column=5,sticky=tk.W,pady=14)
        
        labelStartTemp = tk.Label(gui_main,text="Temperature (C°): ",font="Arial 14 ")
        labelStartTemp.grid(row=2,column=5,sticky=tk.W)
        valueEntryStartTemp = tk.StringVar()
        EntryStartTemp = tk.Entry(gui_main,textvariable = valueEntryStartTemp,width=15)
        EntryStartTemp.grid(row=2,column=6,sticky=tk.W)
             
        labelThetaav = tk.Label(gui_main,text="Theta Av Array (Theta (°)): ",font="Arial 14 ")
        labelThetaav.grid(row=3,column=5,sticky=tk.W)
        valueEntryThetaav = tk.StringVar()
        EntryThetaav = tk.Entry(gui_main,textvariable = valueEntryThetaav,width=30)
        EntryThetaav.grid(row=3,column=6,sticky=tk.W)
        
        labelMinTheta = tk.Label(gui_main,text="Min. Theta (2 Theta (°)): ",font="Arial 14 ")
        labelMinTheta.grid(row=4,column=5,sticky=tk.W)
        valueEntryMinTheta = tk.StringVar()
        EntryMinTheta = tk.Entry(gui_main,textvariable = valueEntryMinTheta,width=15)
        EntryMinTheta.grid(row=4,column=6,sticky=tk.W)
        
        labelMaxTheta = tk.Label(gui_main,text="Max. Theta  (2 Theta (°)): ",font="Arial 14 ")
        labelMaxTheta.grid(row=5,column=5,sticky=tk.W)
        valueEntryMaxTheta = tk.StringVar()
        EntryMaxTheta = tk.Entry(gui_main,textvariable = valueEntryMaxTheta,width=15)
        EntryMaxTheta.grid(row=5,column=6,sticky=tk.W)
         
        labelPeak = tk.Label(gui_main,text="Peak index (1): ",font="Arial 14 ")
        labelPeak.grid(row=6,column=5,sticky=tk.W)
        valueEntryPeak = tk.StringVar()
        EntryPeak = tk.Entry(gui_main,textvariable = valueEntryPeak,width=15)
        EntryPeak.grid(row=6,column=6,sticky=tk.W)

        
        # defining vars used in the checkbuttons
    
        
        varPeakFitting = tk.IntVar()
        varAzimuthalIntegration = tk.IntVar()
        varEllipticalStrainFit = tk.IntVar()
        checkBoxVars = [varAzimuthalIntegration,varEllipticalStrainFit,varPeakFitting]
        
        #Checkbuttons
        
        CheckbuttonPseudoVoigtFit = tk.Checkbutton(gui_main,text="Peak Fitting",font="Arial 14",variable=varPeakFitting)
        CheckbuttonPseudoVoigtFit.grid(row=11,column=3,columnspan=2)
        
        CheckbuttonAzimuthalIntegration = tk.Checkbutton(gui_main,text="Azimuthal Integration",font="Arial 14",variable=varAzimuthalIntegration)
        CheckbuttonAzimuthalIntegration.grid(row=11,column=2,columnspan=2)

        CheckbuttonEllipticalStrainFit = tk.Checkbutton(gui_main,text="Elliptical Strain Fit",font="Arial 14",variable=varEllipticalStrainFit)
        CheckbuttonEllipticalStrainFit.grid(row=11,column=4,columnspan=2)


        # set default cell width and height

        col_count, row_count = gui_main.grid_size()

        for col in range(col_count):
            gui_main.grid_columnconfigure(col, minsize=20)

        for row in range(row_count):
            gui_main.grid_rowconfigure(row, minsize=20)

        
        def var_states():
            selectedTasks = []
            for taskName, isSelected in zip(["azimuthal_integration","ellipticalStrain_fit","peak_fit"],checkBoxVars):
                if(isSelected.get()):
                    selectedTasks.append(taskName)
            
            param.setTasks(selectedTasks)


        
        # defining all methonds used in the buttons to chose input and output files
        
        def chooseOutputDirectory():
            outputDirectory = filedialog.askdirectory()
            param.setOutputDirectory(outputDirectory)
            
        def openAzimJson():
            azimJsonFile = filedialog.askopenfile()
            azimJson = dict(json.load(azimJsonFile))
            if Entrynptazim.get() == "":
                Entrynptazim.insert(0, azimJson["nbpt_azim"])
                EntryRadSteps.insert(0, azimJson["nbpt_rad"])
                EntryRadialRange.insert(0, ",".join(map(str, (azimJson["radial_range_min"], azimJson["radial_range_max"]))))
            param.setPathToAzimJson(os.path.abspath(azimJsonFile.name))
            
        def selectDetectorData():
            cbfInputs = tkfilebrowser.askopendirnames()
            param.setDirectoryPaths(cbfInputs)
         
         
         
        def openELabFTW():
            elabJsonPath = filedialog.askopenfilename()
            with open(elabJsonPath, "r") as file:
                paramJson = dict(json.load(file))
            if EntryPositionsdatenX.get() == "":
                EntryPositionsdatenX.insert(0,",".join(map(str,np.arange(paramJson["pos_insitu"]["x_start"]["value"],paramJson["pos_insitu"]["x_end"]["value"],paramJson["pos_insitu"]["x_step"]["value"]/1000))))
                EntryPositionsdatenZ.insert(0,",".join(map(str,np.arange(paramJson["pos_insitu"]["z_start"]["value"],paramJson["pos_insitu"]["z_end"]["value"],paramJson["pos_insitu"]["z_step"]["value"]/1000))))
            #param.setDirectoryPaths(paramJson["datafiles"].keys()) TODO:uncomment
            param.setElabFtwJson(elabJsonPath)
        
        
        # buttons for input and ouput
        
        buttonLoadAzimJson = tk.Button(gui_main,text="Load azim.json",font="Arial 14",command=openAzimJson,width=22,height=1)
        buttonLoadAzimJson.grid(row=9,column=2,sticky=tk.W)
        
        buttonChooseOutputDirectory = tk.Button(gui_main,text="Choose output directory",font="Arial 14",width=22,height=1,command =chooseOutputDirectory)
        buttonChooseOutputDirectory.grid(row=9,column=3,sticky=tk.W)
        
        buttonSelectCbfInputs = tk.Button(gui_main,text="Load XRD-Datafiles",font="Arial 14",width=22,height=1,command =selectDetectorData)
        buttonSelectCbfInputs.grid(row=9,column=4,sticky=tk.W)
        
        buttonELabJson = tk.Button(gui_main,text="Load elab_param.json",font="Arial 14", command = openELabFTW,width=22,height=1)
        buttonELabJson.grid(row=9,column=5,sticky=tk.W)


        # filter input for syntax errors
        #TODO 


        # apply default values

        if True:
            Entrynptazim.insert(0, "72")
            EntryRadSteps.insert(0, "2084")
            EntryRadialRange.insert(0, "1, 10")
    
            EntryEModules.insert(0, "220000,165000,220000,220000,181000,148000")
            EntryPossionszahlen.insert(0, "0.28,0.33,0.28,0.28,0.32,0.25")
            Entryd0.insert(0, "0.11684")
            EntryWavelength.insert(0, "0.012037300291262137")
            EntryPositionsdatenX.insert(0, ",".join(map(str, np.linspace(-7.06,-7.36,16))))
            EntryPositionsdatenZ.insert(0, "20, 25, 28, 29, 30, 31, 32, 35, 40")
            
            EntryStartTemp.insert(0, "20")
            EntryThetaav.insert(0, "1.25,2.5,2.94748158,3.5,3.9,4.3")
            EntryMinTheta.insert(0, "5.5")
            EntryMaxTheta.insert(0, "6.5")
            EntryPeak.insert(0, "2")

        
        # starting the process and saving the values of every entry in the Param class
        
        def startProgressbar():
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
            
            positionsdatenZp = [precision(positionsdatenZ) for positionsdatenZ in EntryPositionsdatenZ.get().split(",")]
            param.setPositionsY(positionsdatenZp)
            
            starttempp = precision(EntryStartTemp.get().split(","))[0]
            param.setStartTemp(starttempp)
            
            param.setGUIInstance(gui_main)
            
            thetaavp = [precision(thetaAV) for thetaAV in EntryThetaav.get().split(",")]
            param.thetaAV(thetaavp)
            
            minthetap = precision(EntryMinTheta.get().split(","))[0]
            param.setMinTheta(minthetap)
            
            maxthetap = precision(EntryMaxTheta.get().split(","))[0]
            param.setMaxTheta(maxthetap)
            
            peakp = int(EntryPeak.get())
            param.setPeak(peakp)

            radstepsp = int(EntryRadSteps.get())
            param.setRadSteps(radstepsp)
            
            radrangep = [precision(radRange) for radRange in EntryRadialRange.get().split(",")]
            param.setRadialRange(tuple(radrangep))

            nptAzim =  int(Entrynptazim.get())
            param.setNptAzim(nptAzim)
            
            progressbar.start()
            param.setProgressBarHandles([progressbar])
            var_states()
            
            core.run()
            
            
        # defining method to stop the process and close the window, used in buttonStop
        
        def stopProgressbar():
            progressbar.stop()
            core.shutdown()
            gui_main.quit()
            
        
        # label for the progress bar
        
        labelProgessbar= tk.Label(gui_main,text="Progress: ",font="Artial 16")
        labelProgessbar.grid(row=13,column=1)
        
        
        # settings for the progress bar
         
        progressbar = tkk.Progressbar(gui_main,orient="horizontal",mode="determinate",maximum=100,length=100)
        progressbar.grid(row=13,column=2,columnspan=5,sticky=tk.W)
        
       
        # buttons to start and stop the process
        
        buttonStart = tk.Button(gui_main,text="Start",font="Arial 14",command=startProgressbar,width=22,height=2)
        buttonStart.grid(row=15,column=3,padx=5)
        
        buttonStop = tk.Button(gui_main,text="Stop",font="Arial 14",command=stopProgressbar,width=22,height=2)
        buttonStop.grid(row=15,column=4,padx=5)
        


    
        

        gui_main.mainloop()
        
