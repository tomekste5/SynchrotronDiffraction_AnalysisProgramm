import logging
import multiprocessing as mp
import time
from multiprocessing import Process
from queue import Empty

import numpy as np
from scipy.optimize import curve_fit

from Tasks.Config import TaskConfigs
from IO.IO_Utils import DetectorDataParser
from IO.IO_Utils import IO
from IO.IO_Utils import SearchUtils
from Tasks.Task import Task

#make config struct



class PseudoVoigtFit:
        def gauss(x, *p):
            LorCoeff, A, x0,FWHM,a,b = p
            return (LorCoeff*A*(1/(1+((x-x0)/(FWHM/2))**2))+(1-LorCoeff)*A*np.exp(-np.log(2)*((x-x0)/(FWHM/2))**2))+a*x+b
        def doFit(intensity,twoTheta,thetaPeak):
                
            initialGuess =np.array([0, np.max(intensity)-np.min(intensity), thetaPeak*2, 0.028, 0, np.min(intensity)])
                
            param, error = curve_fit(PseudoVoigtFit.gauss,twoTheta,intensity,initialGuess,ftol=10**(-10))
            perr = np.sqrt(np.diag(error))
                
            return {"LorCoeff":param[0],"A":param[1],"x0":param[2],"FWHM":param[3],"LorCoeff_Err":perr[0],"A_Err":perr[1],"x0_Err":perr[2],"FWHM_Err":perr[3]}

class PseudoVoigtTask(Task):
    def getDescription():
        return TaskConfigs.VoigtFit_Config.description
    def getFuncName():
        return TaskConfigs.VoigtFit_Config.taskName  
    def getDependencies():
        return TaskConfigs.VoigtFit_Config.dependencies
    
                    
    def doPseudoVoigtFitting(q,params):
        while(True):
            try:
                azimIntegrationData = []
                path = q.get(timeout=1)
                #if(funcRet["azimuthal_integration"] == None or azimFile not in set(funcRet["azimuthal_integration"])):
                try:
                    azimIntegrationData =  params["funcRet"]["azimuthal_integration"][path]
                except KeyError or TypeError:
                    params = {"path":path, "precision":TaskConfigs.VoigtFitTask_Config.precision}
                    azimIntegrationData =TaskConfigs.VoigtFitTask_Config.readFunction(params)
                
                interval = (azimIntegrationData[1] < params["maxTheta"]) & (params["minTheta"] <azimIntegrationData[1])
                fitData = []
                for azimAngleIdx in range(len(azimIntegrationData[0])):  
                    input_data = [azimIntegrationData[0][azimAngleIdx][interval],azimIntegrationData[1][interval]]
                    azimAngle = np.round(azimIntegrationData[2][azimAngleIdx])
                    fitData.append({"FilePath":path.replace(path.split(".")[-1],"cbf"),"azimAngle":azimAngle} | PseudoVoigtFit.doFit(input_data[0],input_data[1],params["thetaPeak"]))
                    
                params["returnVal"][path.replace(path.split(".")[-1],"cbf")]=fitData
                
                IO.saveResultDictToFile(fitData,[mode for mode in TaskConfigs.VoigtFitTask_Config.modes if "MP" in mode],path=path)
     
                params["logger"].info("Fitted File: " + path)
            except Empty:
                break
            except FileNotFoundError:
                 params["logger"].error("FileNotFoundError: No such file or directory: " +path)   
    #def 
    def fillQueue(funcRet,directoryPaths,mode,queue):
        for path in directoryPaths:
            for filePath in SearchUtils.getFilesThatEndwith(path,".cbf"):
                if all([TaskConfigs.VoigtFitTask_Config.filenamePrefix not in file or mode for file in SearchUtils.getFilesThatEndwith(path,".csv")]):
                    queue.put(filePath)
    
    def runTask(minTheta,maxTheta,directoryPaths,isMultiProcessingAllowed,thetaAV,peak,mode,handles,funcRet):
            startExecTime = time.time() 
            
            m = mp.Manager()
            logger = mp.log_to_stderr()
            logger.setLevel(logging.INFO)
            queue = m.Queue()
            
            params = m.dict({"logger":logger,"funcRet":funcRet,"maxTheta":maxTheta,"minTheta":minTheta,"thetaPeak":thetaAV[peak],"returnVal":m.dict({"units":TaskConfigs.VoigtFitTask_Config.units})})
            
            PseudoVoigtTask.fillQueue(funcRet,directoryPaths,mode,queue)
        
            
            
            numberOfProcesses = mp.cpu_count()-1 if isMultiProcessingAllowed else 1
             
            
            workerProcesses = [] 
            for i in range(0,numberOfProcesses):
                workerP = Process(target=PseudoVoigtTask.doPseudoVoigtFitting, args = (queue,params))
                workerP.daemon = True
                workerP.start()  # Launch reader_p() as another proc
                workerProcesses.append(workerP)
            
            for process in workerProcesses:
                process.join()
            
            logger.info("Finished Task in %ss"%(str(time.time()-startExecTime))) 
            results  =dict(params["returnVal"])
            
            params = {"dict": results,"prefix":TaskConfigs.VoigtFitTask_Config.preFix,"precision":TaskConfigs.VoigtFitTask_Config.precision}
            for saveDict in TaskConfigs.VoigtFitTask_Config.saveFunctions:
                saveDict(params)  
                
            del(m)
            return results