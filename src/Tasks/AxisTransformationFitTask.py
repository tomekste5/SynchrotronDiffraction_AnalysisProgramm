from Tasks.Config import TaskConfigs
from IO import IO_Utils


import time

from Tasks.Task import Task
import numpy as np

from Multiprocessing.Pool import Pool
from IO.Parser import XRayDetectorDataParser

from libarys import AxisTransformFit

class AxisTransformationTask(Task):
    
    def runTask():
        pass
    def getDescription():
        pass
    def getFuncName():
        return TaskConfigs.AxisTransformFitTask_Config.taskName
    def getDependencies():
        pass
    def getInputParams():
        pass
        
    
    def doAxisTransformation(callParams):
        file, params, voigtFitData= callParams[:3]
        try:
            azimuthalAngles,x0,x0_err= np.array([voigtFitData[i]["azimAngle"] for i in range(len(voigtFitData))]),np.array([TaskConfigs.AxisTransformFitTask_Config.precision(voigtFitData[i]["x0"]) for i in range(len(voigtFitData))]),np.array([voigtFitData[i]["x0_Err"] for i in range(len(voigtFitData))])
            
            fitData = AxisTransformFit.doFit(azimuthalAngles=azimuthalAngles,x0=x0,x0_err=x0_err,d0=params["d0"],wavelength=TaskConfigs.AxisTransformFitTask_Config.precision(params["wavelength"]))

            E=params["E_Modules"]
            poisson=params["Possion_Numbers"]

            strainXX = fitData["strainXX"]
            strainZZ = fitData["strainZZ"]
            strainXZ = fitData["strainXZ"]

            principalStresses = AxisTransformFit.calculatePrincipalStresses(E=E,poisson=poisson,strainYY=strainXX,strainZZ=strainZZ,strainYZ=strainXZ)                
            
            params["results"][file] = [{"File":file,"Z_positions":params["Z_positions"][int(TaskConfigs.AxisTransformFitTask_Config.lambdaFileNr(file))-1],"X_positions":params["X_positions"][int(TaskConfigs.AxisTransformFitTask_Config.lambdaDirectoryNr(file))-1]}| fitData |principalStresses| {"FWHM":np.mean(np.array([voigtFitData[i]["FWHM"] for i in range(len(voigtFitData))])),"A":np.mean(np.array([voigtFitData[i]["A"] for i in range(len(voigtFitData))])),"x0":np.mean(np.array([voigtFitData[i]["x0"] for i in range(len(voigtFitData))]))}]
    
            params["logger"].info("Fitted File: " + file)
        except FileNotFoundError:
            params["logger"].error("FileNotFoundError: No such file or directory: " +file)   
    
    def fillQueue(funcRet,filePaths,queue,params):
        nrOfTasks = 0
        loadedPickleFiles = {}
        for path in filePaths:
            for file in IO_Utils.getFilesThatEndwith(path,XRayDetectorDataParser.getAllowedFormats()):
                
                if(not TaskConfigs.PseudoVoigtFitTask_Config.taskName in funcRet.keys() and not IO_Utils.getDirectory(file) in set(loadedPickleFiles)):
                    load_params  = {"file":file,"prefix":TaskConfigs.PseudoVoigtFitTask_Config.fileName_prefix}
                    loadedPickleFiles =  loadedPickleFiles | TaskConfigs.AxisTransformFitTask_Config.loadFunction(load_params)
                    
                    
                if(TaskConfigs.PseudoVoigtFitTask_Config.taskName in funcRet.keys() and file in funcRet[TaskConfigs.PseudoVoigtFitTask_Config.taskName].keys()):
                    queue.put([AxisTransformationTask.doAxisTransformation,[file,params, funcRet[TaskConfigs.PseudoVoigtFitTask_Config.taskName][file]]])
                else:
                    queue.put([AxisTransformationTask.doAxisTransformation,[file,params, loadedPickleFiles[file]]])
                    
                nrOfTasks +=1
                
                
        axisTranformationFit_settings = params["results"]["settings"][0] #
        voigtFit_settings = loadedPickleFiles[file]["settings"][0] if loadedPickleFiles != {} else  funcRet[TaskConfigs.PseudoVoigtFitTask_Config.taskName]["settings"][0]
        params["results"]["settings"] = [axisTranformationFit_settings | voigtFit_settings]
        return nrOfTasks
    
    def runTask(outputPath,filePaths,wavelength,peak,E,Possions,d0,Z_positions,X_positions,progressBars: list,pool: Pool,funcRet: dict):
        
        execStart_time = time.time() 
        
        #get logger which is used by the manager
        logger = pool.getLogger()
        #settings up the logger filter (INFO,WARNING,ERROR)
        logger.setLevel(TaskConfigs.AxisTransformFitTask_Config.loggingLevel)
                
        logger.info("Starting Task %s..."%(TaskConfigs.AxisTransformFitTask_Config.taskName))
        
        m = pool.getManager()
                
        processQueue =pool.getQueue()
        
        params = {"logger":logger,"results":m.dict({"units":TaskConfigs.AxisTransformFitTask_Config.units,
                                                             "settings":[{"wavelength":wavelength,"E-Modules":E,"possions":Possions,"d0":d0}]})
                         ,"d0":d0,"wavelength":wavelength,"Z_positions":Z_positions,"X_positions":X_positions,"E_Modules":E[peak],"Possion_Numbers":Possions[peak]}

        #To ensure processing doesnt start while filling the Queue (could result in blocking each other, so low speed)
        pool.idle()
        nrOfTasks = AxisTransformationTask.fillQueue(funcRet,filePaths,processQueue,params)
        
        #release the worker processes to start processing the jobs
        pool.start()
        
        while(len(params["results"].keys()) < nrOfTasks):
            time.sleep(1)
            logger.info("Reporting progress:    "+str(((len(params["results"].keys())/(nrOfTasks+1) *100)))+ "%")
            
        
        AxisTransformationFit_results =dict(sorted(params["results"].items()))
        
        save_Params = {"outputPath":outputPath,"dict": AxisTransformationFit_results,"prefix":TaskConfigs.AxisTransformFitTask_Config.fileName_prefix,"precision":TaskConfigs.AxisTransformFitTask_Config.precision,"overwrite":False}
        for saveDict in TaskConfigs.AxisTransformFitTask_Config.saveFunctions:
            saveDict(save_Params)  
            
        logger.info("Finished Task in %ss"%(str(time.time()-execStart_time)))
        
        return AxisTransformationFit_results
    
