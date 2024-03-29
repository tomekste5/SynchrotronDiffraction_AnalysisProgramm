from Tasks.Config import TaskConfigs
from IO import IO_Utils


import time

import numpy as np

from Multiprocessing.Pool import Pool
from IO.Parser import XRayDetectorDataParser

from libarys import EllipticalFit
import json

class EllipticalStrainFitTask():
    
    def runTask():
        pass
    def getDescription():
        pass
    def getFuncName():
        return TaskConfigs.EllipticalStrainFitTask_Config.taskName
    def getDependencies():
        pass
    def getInputParams():
        pass
        
    
    def doFit(callParams):
        """Does Elliptical Strain Fit or every file which is passed and writes results in the results dict.

        Args:
            callParams (list): [dictionary contains path to file, parameters required to do the fit, results from PseudoVoigtFit]
            
        """
        file, params, pseudoVoigtFitData,theta= callParams[:4]
        try:
            azimuthalAngles,x0,x0_err= np.array([pseudoVoigtFitData[i]["azimAngle"] for i in range(len(pseudoVoigtFitData))]),np.array([TaskConfigs.EllipticalStrainFitTask_Config.precision(pseudoVoigtFitData[i]["x0"]) for i in range(len(pseudoVoigtFitData))]),np.array([pseudoVoigtFitData[i]["x0_Err"] for i in range(len(pseudoVoigtFitData))])
            
            fitData = EllipticalFit.doFit(azimuthalAngles=azimuthalAngles,x0=x0,x0_err=x0_err,d0=params["d0"],wavelength=TaskConfigs.EllipticalStrainFitTask_Config.precision(params["wavelength"]),theta=theta)

            E=params["E_Modules"]
            poisson=params["Possion_Numbers"]

            strainXX = fitData["strainXX"]
            strainZZ = fitData["strainZZ"]
            strainXZ = fitData["strainXZ"]

            principalStresses = EllipticalFit.calculatePrincipalStresses(E=E,poissonNumbers=poisson,strainXX=strainXX,strainZZ=strainZZ,strainXZ=strainXZ)                
            
            params["results"][file] = [{"File":file,"Z_positions":params["Z_positions"][int(TaskConfigs.EllipticalStrainFitTask_Config.lambdaFileNr(file))-1],"X_positions":params["X_positions"][int(TaskConfigs.EllipticalStrainFitTask_Config.lambdaDirectoryNr(file))-1]}| fitData |principalStresses| {"FWHM":np.mean(np.array([pseudoVoigtFitData[i]["FWHM"] for i in range(len(pseudoVoigtFitData))])),"A":np.mean(np.array([pseudoVoigtFitData[i]["A"] for i in range(len(pseudoVoigtFitData))])),"x0":np.mean(np.array([pseudoVoigtFitData[i]["x0"] for i in range(len(pseudoVoigtFitData))]))}]
    
            params["logger"].info("Fitted File: " + file)
        except FileNotFoundError:
            params["logger"].error("FileNotFoundError: No such file or directory: " +file)   
    
    def fillQueue(funcRet,filePaths,queue,params,theta):
        """Fills the multiprocessing Queue with the files that are found in paths

        Args:
            funcRet (dictionary): Dictionary which contains the results of tasks defined as dependency´s in TaskConfig
            filePaths (list): paths to detector files or directory´s that contain detector files
            queue (Multiprocessing.Queue): Queue of multiprocessing pool
            params (dictionary): Dictionary that contains the Results array, parameters required for the AxisTransformationFit and the logger

        Returns:
            int: how many file need to be processed, referred by jobs.
        """
        
        
        nrOfTasks = 0
        loadedPickleFiles = {}
        for path in filePaths:
            for file in IO_Utils.getFilesThatEndwith(path,XRayDetectorDataParser.getAllowedFormats()):
                
                if(not TaskConfigs.peakFittingTask_Config.taskName in funcRet.keys() and not IO_Utils.getDirectory(file) in set(loadedPickleFiles)):
                    load_params  = {"file":file,"prefix":TaskConfigs.peakFittingTask_Config.fileName_prefix}
                    loadedPickleFiles =  loadedPickleFiles | TaskConfigs.EllipticalStrainFitTask_Config.loadFunction(load_params)
                    
                    
                if(TaskConfigs.peakFittingTask_Config.taskName in funcRet.keys() and file in funcRet[TaskConfigs.peakFittingTask_Config.taskName].keys()):
                    queue.put([EllipticalStrainFitTask.doFit,[file,params, funcRet[TaskConfigs.peakFittingTask_Config.taskName][file],theta]])
                else:
                    queue.put([EllipticalStrainFitTask.doFit,[file,params, loadedPickleFiles[file],theta]])
                    
                nrOfTasks +=1
                
                
        axisTranformationFit_settings = params["results"]["settings"][0] #
        voigtFit_settings = loadedPickleFiles["settings"][0] if loadedPickleFiles != {} else  funcRet[TaskConfigs.peakFittingTask_Config.taskName]["settings"][0]
        params["results"]["settings"] = [axisTranformationFit_settings | {TaskConfigs.peakFittingTask_Config.taskName:voigtFit_settings}]
        return nrOfTasks
    
    def runTask(gui,thetaAV,outputPath,elabFtwJson,filePaths,wavelength,peak,E,poissonNumbers,d0,Z_positions,X_positions,progressBars: list,pool: Pool,funcRet: dict):
        """Does a axisTransformation fit for every file to get strain/stress values in axis direction by using multiprocessing.

        Args:
            outputPath (string):  Path to directory where to store the single results file
            elabFtwJson (dictionary):  ELabFTWJson object which was used
            filePaths (list): Paths to detector files or directory´s that contain detector files
            wavelength (chosen precision): Wavelength used during the experiment
            peak (int): For which peak to calculate the lattice distance (Array index) 
            E (list): List of E-Modules for different lattice plane
            poissonNumbers (list): List of poisson numbers for different lattice plane
            d0 (chosen precision): lattice distance in unstressed state
            Z_positions (list): List of Z positions
            X_positions (_type_): List of X positions
            progressBars (list): Handle to progress bar on gui
            pool (Pool): multiprocessing pool
            funcRet (dict): Dictionary which contains the results of tasks PseudoVoigtFitTask

        Returns:
            dictionary: results in standardized format (See documentation)
        """
        execStart_time = time.time() 
        
        #get logger which is used by the manager
        logger = pool.getLogger()
        #settings up the logger filter (INFO,WARNING,ERROR)
        logger.setLevel(TaskConfigs.EllipticalStrainFitTask_Config.loggingLevel)
                
        logger.info("Starting Task %s..."%(TaskConfigs.EllipticalStrainFitTask_Config.taskName))
        
        m = pool.getManager()
                
        processQueue =pool.getQueue()
        
        eLabFtwInput = json.load(open(elabFtwJson)) if elabFtwJson != None else None
        
        params = {"logger":logger,"results":m.dict({"units":TaskConfigs.EllipticalStrainFitTask_Config.units,
                                                             "settings":[{"wavelength":wavelength,"E-Modules":E,"possions":poissonNumbers,"d0":d0} | {"ElabFtwJson":eLabFtwInput}]})
                         ,"d0":d0,"wavelength":wavelength,"Z_positions":Z_positions,"X_positions":X_positions,"E_Modules":E[peak],"Possion_Numbers":poissonNumbers[peak]}

        #To ensure processing doesnt start while filling the Queue (could result in blocking each other, so low speed)
        pool.idle()
        nrOfJobs = EllipticalStrainFitTask.fillQueue(funcRet,filePaths,processQueue,params,thetaAV[peak])
        
        #release the worker processes to start processing the jobs
        pool.start()
        
        while(len(params["results"].keys()) < nrOfJobs+2):
            time.sleep(0.1)
            progressBars[0]["value"] = (len(params["results"].keys())/(nrOfJobs+1) *100)
            logger.info("Reporting progress:    "+str(((len(params["results"].keys())/(nrOfJobs+1) *100)))+ "%")
            gui.update()
            
        progressBars[0]["value"] = 0
        AxisTransformationFit_results =dict(sorted(params["results"].items()))
        
        save_Params = {"outputPath":outputPath,"dict": AxisTransformationFit_results,"prefix":TaskConfigs.EllipticalStrainFitTask_Config.fileName_prefix,"precision":TaskConfigs.EllipticalStrainFitTask_Config.precision,"overwrite":False}
        for saveDict in TaskConfigs.EllipticalStrainFitTask_Config.saveFunctions:
            saveDict(save_Params)  
            
        logger.info("Finished Task in %ss"%(str(time.time()-execStart_time)))
        
        return AxisTransformationFit_results
    
