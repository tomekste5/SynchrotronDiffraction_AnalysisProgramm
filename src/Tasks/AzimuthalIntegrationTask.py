import logging
import multiprocessing as mp
import os
import time
from multiprocessing import Process
from queue import Empty
from unittest import result

import pyFAI

from Tasks.Config import TaskConfigs
from IO.Parser import XRayDetectorDataParser
from IO.IO_Utils import SearchUtils
from Multiprocessing import Pool
from Tasks.Task import Task
from IO.Parser import XRayDetectorDataParser

class AzimuthalIntegrator:
        
        def __init__(self, settingJson, args):
            self.__pyFAI_azimIntegrator  = pyFAI.load(settingJson)
            self.__pyFAI_callArgs = args
        
        def integrate2D(self,data,filename):
            azimData = self.__pyFAI_azimIntegrator.integrate2d(data, npt_rad=self.__pyFAI_callArgs[0],npt_azim=self.__pyFAI_callArgs[1],radial_range=self.__pyFAI_callArgs[2],unit="2th_deg",filename=filename)
            return [*azimData]

class AzimuthalIntegrationTask(Task):
    def getDescription():
        return "Does things"
    def getFuncName():
        return "azimuthal_integration"
    def getDependencies():
        return {}
    
    
    def processFile(queue,params):
        while(True):
            try:
                path = queue.get(timeout=1)
                detectorData = TaskConfigs.AzimuthalIntegrationTask_Config.readFunction(path).data
                azimData = params["azimIntegrator"].integrate2D(detectorData,os.path.splitext(path)[0] + ".azim")
                params["returnVal"][path] = azimData
                params["logger"].info('Child process integrated File: ' + path)
            except Empty:
                break
            except FileNotFoundError:
                params["logger"].error("FileNotFoundError: No such file or directory: " +path)   
                
                
    def fillQueue(directoryPaths,queue,mode):
        for directory in directoryPaths:
            for filePath in SearchUtils.getFilesThatEndwith(directory,XRayDetectorDataParser.getAllowedFormats()):
                queue.put(filePath)
                        
    def runTask(npt_rad,npt_azim,radial_range,settingJson,directoryPaths,isMultiProcessingAllowed,mode,handles):   
            azimIntegrator = AzimuthalIntegrator(settingJson=settingJson,args = (npt_rad,npt_azim,radial_range))   
            workerPool = Pool.Pool(3)
            workerPool.start()
            """
            logger = mp.log_to_stderr()
            logger.setLevel(logging.INFO)
            
            m = mp.Manager()
            
            results = m.dict()
            queue = m.Queue()
            """
            manager = workerPool.getManager()
            logger = workerPool.getLogger()
            
            queue =  manager.Queue()
            params = manager.dict({"logger":logger,"azimIntegrator":azimIntegrator,"returnVal":manager.dict({"units":TaskConfigs.AzimuthalIntegrationTask_Config.units})})
            
            AzimuthalIntegrationTask.fillQueue(directoryPaths,queue,mode)

            workerPool.addTask([AzimuthalIntegrationTask.processFile,[queue,params]])
            executionStart = time.time()   
            """
            if(isMultiProcessingAllowed):
                numberOfProcesses = mp.cpu_count()-1                    
                
                workerProcesses = [] 
                for i in range(0,numberOfProcesses):
                    workerP = Process(target=AzimuthalIntegrationTask.processFile, args = (queue,logger,azimIntegrator,results))
                    workerP.daemon = True
                    workerP.start()  # Launch reader_p() as another proc
                    workerProcesses.append(workerP)
                
                for process in workerProcesses:
                    process.join()
            else:
                AzimuthalIntegrationTask.doIntegration()
            
            logger.info("Finished Task in %ss"%(str(time.time()-executionStart))) 
            del(m)
            """
            logger.info("Finished Task in %ss"%(str(time.time()-executionStart))) 
            results = dict(params["returnVal"])
            return results
            #Fill Queue with directory Paths
                # load file
