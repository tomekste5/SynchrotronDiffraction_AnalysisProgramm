import logging
import multiprocessing as mp
import time
from multiprocessing import Process
from queue import Empty

import numpy as np
from scipy.optimize import curve_fit

from Tasks.Config import TaskConfigs
from IO import IO_Utils
from Tasks.Task import Task
from IO.Parser import XRayDetectorDataParser
from Multiprocessing.Pool import Pool

#make config struct



class VoigtFit:
        def gauss(x, *p):
            LorCoeff, A, x0,FWHM,a,b = p
            return (LorCoeff*A*(1/(1+((x-x0)/(FWHM/2))**2))+(1-LorCoeff)*A*np.exp(-np.log(2)*((x-x0)/(FWHM/2))**2))+a*x+b
        def doFit(intensity,twoTheta,thetaPeak):
                
            initialGuess =np.array([0, np.max(intensity)-np.min(intensity), thetaPeak*2, 0.028, 0, np.min(intensity)])
                
            param, error = curve_fit(VoigtFit.gauss,twoTheta,intensity,initialGuess,ftol=10**(-10))
            perr = np.sqrt(np.diag(error))
                
            return {"LorCoeff":param[0],"A":param[1],"x0":param[2],"FWHM":param[3],"LorCoeff_Err":perr[0],"A_Err":perr[1],"x0_Err":perr[2],"FWHM_Err":perr[3]}

class VoigtFitTask(Task):
    def getDescription():
        return TaskConfigs.VoigtFitTask_Config.description
    def getFuncName():
        return TaskConfigs.VoigtFitTask_Config.taskName 
    def getDependencies():
        return TaskConfigs.VoigtFitTask_Config.dependencies
    
                    
    def doPseudoVoigtFitting(callParams):
        path,params,data = callParams
        try:
            if(data != None):
                azimIntegrationData =  data
            else:
                readParams = {"path":path.replace(path.split(".")[-1],"azim"), "precision":TaskConfigs.VoigtFitTask_Config.precision}
                azimIntegrationData =TaskConfigs.VoigtFitTask_Config.readFunction(readParams)
            
            interval = (azimIntegrationData[1] < params["maxTheta"]) & (params["minTheta"] <azimIntegrationData[1])
            fitData = []
            for azimAngle in range(len(azimIntegrationData[0])):  
                input_data = [azimIntegrationData[0][azimAngle][interval],azimIntegrationData[1][interval]]
                azimAngle = TaskConfigs.VoigtFitTask_Config.precision(np.round(azimIntegrationData[2][azimAngle]))
                fitData.append({"FilePath":path.replace(path.split(".")[-1],"cbf"),"azimAngle":azimAngle} | VoigtFit.doFit(input_data[0],input_data[1],params["thetaPeak"]))
                
            params["returnVal"][path]=fitData
    
            params["logger"].info("Fitted File: " + path)
        except Empty:
            pass
        except FileNotFoundError:
                params["logger"].error("FileNotFoundError: No such file or directory: " +path)   
    #def 
    def fillQueue(funcRet,directoryPaths,queue,params):
        nrOfTasks = 0
        for path in directoryPaths:
            for filePath in IO_Utils.getFilesThatEndwith(path,XRayDetectorDataParser.getAllowedFormats()):
                if(nrOfTasks == 142):
                    print("test")
                try:
                    queue.put([VoigtFitTask.doPseudoVoigtFitting, [filePath,params,funcRet[TaskConfigs.AzimuthalIntegrationTask_Config.taskName][filePath]]])
                except KeyError:
                    queue.put([VoigtFitTask.doPseudoVoigtFitting, [filePath,params,None]])
                nrOfTasks +=1
        return nrOfTasks
    
    def runTask(minTheta,maxTheta,directoryPaths: list,thetaAV,peak,handles: list,pool: Pool,funcRet: dict):
        execTime_start = time.time() 
        
        logger = pool.getLogger()
        logger.setLevel(TaskConfigs.VoigtFitTask_Config.loggingLevel)
        
        logger.info("Starting Task %s..."%(TaskConfigs.VoigtFitTask_Config.taskName))
        
        m = pool.getManager()
        queue = pool.getQueue()
        
        params = m.dict({"logger":logger,"maxTheta":maxTheta,"minTheta":minTheta,"thetaPeak":thetaAV[peak],"returnVal":m.dict({"units":TaskConfigs.VoigtFitTask_Config.units,
                                                                                                                               "settings":{"minTheta":minTheta,"maxTheta":maxTheta,"peak":peak,"thetaAV":thetaAV}})})
        
        #To ensure processing doesnt start while filling the Queue (could result in blocking each other, so low speed)
        pool.idle()
        #Fill pool queue with jobs
        nrOfTasks =  VoigtFitTask.fillQueue(funcRet,directoryPaths,queue,params)
        #Release the worker processes to start processing the jobs
        pool.start()
        
        while(len(params["returnVal"].keys()) < nrOfTasks):
            time.sleep(1)
            logger.info("Reporting progress:    "+str(((len(params["returnVal"].keys())/(nrOfTasks+1) *100)))+ "%")
            #handles[0].set((len(params["returnVal"].keys())/(nrOfTasks+1) *100))
        
        voigtFit_results =dict(sorted(params["returnVal"].items()))
        
        save_params = {"dict": voigtFit_results,"prefix":TaskConfigs.VoigtFitTask_Config.preFix,"precision":TaskConfigs.VoigtFitTask_Config.precision,"overwrite":False}
        for saveDict in TaskConfigs.VoigtFitTask_Config.saveFunctions:
            saveDict(save_params)  
            
        logger.info("Finished Task in %ss"%(str(time.time()-execTime_start))) 
        return voigtFit_results
