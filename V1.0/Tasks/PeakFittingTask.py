import time

import numpy as np

from Tasks.Config import TaskConfigs
from IO import IO_Utils
from IO.Parser import XRayDetectorDataParser
from Multiprocessing.Pool import Pool
from libarys import PseudoVoigtFit


class PeakFittingTask():
    def getDescription():
        return TaskConfigs.peakFittingTask_Config.taskDescription
    def getFuncName():
        return TaskConfigs.peakFittingTask_Config.taskName 
    def getDependencies():
        return TaskConfigs.peakFittingTask_Config.taskDependencies
    
                    
    def doPeakFitting(callParams):
        """Does pseudo-voigt fit for every file which is passed and writes results in the results dict.

        Args:
            callParams (list): [dictionary contains path to file, parameters required to do the fit, results from azimuthal integration]
            
        """
        
        
        filePath,params,azimuthalIntegrationData = callParams[:3]
        try:
            #if azimuthalIntegrationData not loaded yet load it
            if(azimuthalIntegrationData == None):
                pathToAzimFile =filePath.replace(filePath.split(".")[-1],"azim")
                loadParams = {"path":pathToAzimFile, "precision":TaskConfigs.peakFittingTask_Config.precision}
                azimuthalIntegrationData =TaskConfigs.peakFittingTask_Config.loadFunction(loadParams) #use load function defined in tasks configs
            
            interval = (azimuthalIntegrationData[1] < params["maxTheta"]) & (params["minTheta"] <azimuthalIntegrationData[1]) # get theta interval from minTheta to maxTheta
            
            row_fitData = []
            for azimuthalAngle in range(len(azimuthalIntegrationData[0])):  
                intensitys = azimuthalIntegrationData[0][azimuthalAngle][interval]
                thetaAngles = azimuthalIntegrationData[1][interval]
                
                azimuthalAngle = np.round(azimuthalIntegrationData[2][azimuthalAngle]).astype(TaskConfigs.peakFittingTask_Config.precision)
                
                row_fitData.append({"FilePath":filePath,"azimAngle":azimuthalAngle} | PseudoVoigtFit.doFit(intensitys,thetaAngles,params["thetaPeak"]))
                
            params["results"][filePath]=row_fitData
    
            params["logger"].info("Fitted File: " + filePath)
        except FileNotFoundError:
                params["logger"].error("FileNotFoundError: No such file or directory: " +filePath)   


    def fillQueue(funcRet,filePaths,queue,params):
        """Fills the multiprocessing Queue with the files that are found in paths

        Args:
            funcRet (dictionary): Dictionary which contains the results of tasks defined as dependency´s in TaskConfig
            filePaths (list): paths to detector files or directory´s that contain detector files
            queue (Multiprocessing.Queue): Queue of multiprocessing pool
            params (dictionary): Dictionary that contains the Results array, parameters required for the AxisTransformationFit and the logger

        Returns:
            int: how many file need to be processed, referred by jobs.
        """
        
        
        nrOfJobs = 0
        for path in filePaths:
            for filePath in IO_Utils.getFilesThatEndwith(path,XRayDetectorDataParser.getAllowedFormats()):
                try:
                    queue.put([PeakFittingTask.doPeakFitting, [filePath,params,funcRet[TaskConfigs.AzimuthalIntegrationTask_Config.taskName][filePath]]])
                except KeyError:
                    queue.put([PeakFittingTask.doPeakFitting, [filePath,params,None]])
                nrOfJobs +=1
                
        azimuthalIntegration_settings = params["results"]["settings"][0]
        pseudoVoigtFit_settings = funcRet[TaskConfigs.AzimuthalIntegrationTask_Config.taskName]["settings"][0] if TaskConfigs.AzimuthalIntegrationTask_Config.taskName in set(funcRet) else  {}
        params["results"]["settings"] = [azimuthalIntegration_settings | pseudoVoigtFit_settings]
        
        return nrOfJobs
    
    def runTask(gui,outputPath,elabFtwJson,minTheta,maxTheta,filePaths: list,thetaAV,peak,progressBars: list,pool: Pool,funcRet: dict):
        """Does a pseudo-Voigt fit for every file by using multiprocessing.

        Args:
            outputPath (string):  Path to directory where to store the single results file
            elabFtwJson (dictionary):  ELabFTWJson object which was used
            minTheta (chosen precision): Start value of Interval which is to Fit 
            maxTheta (chosen precision): End value of Interval which is to Fit 
            filePaths (list):  Paths to detector files or directory´s that contain detector files
            thetaAV (list): _description_
            peak (int): For which peak to calculate the lattice distance (Array index) 
            progressBar (list): _description_
            pool (Pool):  Handle to progress bar on gui
            funcRet (dict): Dictionary which contains the results of azimuthalIntegrationTask

        Returns:
            dictionary:  results in standardized format (See documentation)
        """
        
        execTime_start = time.time() 
        
        logger = pool.getLogger()
        logger.setLevel(TaskConfigs.peakFittingTask_Config.loggingLevel)
        
        logger.info("Starting Task %s..."%(TaskConfigs.peakFittingTask_Config.taskName))
        
        manager = pool.getManager()
        queue = pool.getQueue()
        
        results = manager.dict({"units":TaskConfigs.peakFittingTask_Config.units,"settings":[{"minTheta":minTheta,"maxTheta":maxTheta,"peak":peak,"thetaAV":thetaAV}]})
        
        params = {"logger":logger,"maxTheta":maxTheta,"minTheta":minTheta,"thetaPeak":thetaAV[int(peak)],"results":results}
        
        #To ensure processing doesnt start while filling the Queue (could result in blocking each other, so low speed)
        pool.idle()
        #Fill pool queue with jobs
        nrOfJobs =  PeakFittingTask.fillQueue(funcRet,filePaths,queue,params)
        #Release the worker processes to start processing the jobs
        pool.start()
        
        while(len(params["results"].keys()) < nrOfJobs+2):
            time.sleep(0.1)
            progressBars[0]["value"] = (len(params["results"].keys())/(nrOfJobs+1) *100)
            logger.info("Reporting progress:    "+str(((len(params["results"].keys())/(nrOfJobs+1) *100)))+ "%")
            gui.update()
        progressBars[0]["value"] = 0
        pseudoVoigtFit_results =dict(sorted(params["results"].items()))
        
        save_params = {"outputPath":outputPath,"dict": pseudoVoigtFit_results,"prefix":TaskConfigs.peakFittingTask_Config.fileName_prefix,"precision":TaskConfigs.peakFittingTask_Config.precision,"overwrite":False}
        for saveDict in TaskConfigs.peakFittingTask_Config.saveFunctions:
            saveDict(save_params)  
            
        logger.info("Finished Task in %ss"%(str(time.time()-execTime_start))) 
        return pseudoVoigtFit_results
