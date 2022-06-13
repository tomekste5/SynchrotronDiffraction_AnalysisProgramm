import os
import time
from multiprocessing import Process

import pyFAI
from sympy import rad

from Tasks.Config import TaskConfigs
from IO.Parser import XRayDetectorDataParser
from IO import IO_Utils
from Multiprocessing.Pool import Pool
from Tasks.Task import Task
from IO.Parser import XRayDetectorDataParser

class AzimuthalIntegrator:

        def __init__(self, settingJson, args):
            self.__pyFAI_azimIntegrator  = pyFAI.load(settingJson)
            self.__pyFAI_callArgs = args
        
        def integrate2D(self,data,filename):
            azimData = self.__pyFAI_azimIntegrator.integrate2d_ng(data=data, npt_rad=self.__pyFAI_callArgs[0],npt_azim=self.__pyFAI_callArgs[1],radial_range=self.__pyFAI_callArgs[2],unit="2th_deg",filename=filename)
            return [*azimData]

class AzimuthalIntegrationTask(Task):
    def getDescription():
        return "Does things"
    def getFuncName():
        return "azimuthal_integration"
    def getDependencies():
        return {}
    
    
    def processFile(callParams):
        path, params,data = callParams
        azimIntegrator = params["azimIntegrator"]
        try:
            detectorData = TaskConfigs.AzimuthalIntegrationTask_Config.readFunction(path).data
            params["logger"].info('Starting to integrate: ' + (path))
            azimData = azimIntegrator.integrate2D(detectorData,os.path.splitext(path)[0] + ".azim")
            params["returnVal"][path] = azimData
            params["logger"].info('Child process integrated File: ' + path)
        except FileNotFoundError:
            params["logger"].error("FileNotFoundError: No such file or directory: " +path)   
                
                
    def fillQueue(dataPaths,queue,params):
        nrOfJobs = 0
        for directory in dataPaths:
            for filePath in IO_Utils.getFilesThatEndwith(directory,XRayDetectorDataParser.getAllowedFormats()):
                queue.put([AzimuthalIntegrationTask.processFile,[filePath,params,None]])
                nrOfJobs +=1
        return nrOfJobs
                        
    def runTask(npt_rad,npt_azim,radial_range,settingJson,dataPaths: list,handles: list,pool:Pool): 
            executionStart = time.time()     
            
             #get logger which is used by the manager
            logger = pool.getLogger()
            #settings up the logger filter (INFO,WARNING,ERROR)
            logger.setLevel(TaskConfigs.AzimuthalIntegrationTask_Config.loggingLevel)
            
            logger.info("Starting Task %s..."%(TaskConfigs.AzimuthalIntegrationTask_Config.taskName))
            
            azimIntegrator = AzimuthalIntegrator(settingJson=settingJson,args = [npt_rad,npt_azim,radial_range])   
            
            manager = pool.getManager()
            
            queue =  pool.getQueue()
            params = manager.dict({"logger":logger,"azimIntegrator":azimIntegrator,"returnVal":manager.dict({"units":TaskConfigs.AzimuthalIntegrationTask_Config.units,
                                                                                                             "settings":{"npt_rad":npt_rad,"npt_azim":npt_azim,"radial_range":radial_range,"pyFai_settings":settingJson}})})
            
            pool.idle()
            nrOfJobs =  AzimuthalIntegrationTask.fillQueue(dataPaths,queue,params)
            pool.start()
            
            
            azimuthalIntegration_results =dict(sorted(params["returnVal"].items()))
            
            while(len(params["returnVal"].keys()) < nrOfJobs):
                time.sleep(1)
                logger.info("Reporting progress:    "+str(((len(params["returnVal"].keys())/(nrOfJobs+1) *100)))+ "%")
                #handles[0].set((len(params["returnVal"].keys())/(nrOfTasks+1) *100))

            logger.info("Finished Task in %ss"%(str(time.time()-executionStart))) 
            
            return azimuthalIntegration_results
            #Fill Queue with directory Paths
                # load file
