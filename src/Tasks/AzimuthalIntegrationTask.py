import os
import time

from Tasks.Config import TaskConfigs
from IO.Parser import XRayDetectorDataParser
from IO import IO_Utils
from Multiprocessing.Pool import Pool
from Tasks.Task import Task
from IO.Parser import XRayDetectorDataParser
import json
from libarys.AzimuthalIntegrator import AzimuthalIntegrator

class AzimuthalIntegrationTask(Task):
    def getDescription():
        return "Does things"
    def getFuncName():
        return "azimuthal_integration"
    def getDependencies():
        return {}
    
    def processFile(callParams):
        filePath, params,data,azimuthalIntegrator = callParams
        #azimuthalIntegrator = params["azimuthalIntegrator"]
        try:
            detectorData = TaskConfigs.AzimuthalIntegrationTask_Config.loadFunction(filePath)
            params["logger"].info('Starting to integrate: ' + (filePath))
            azimuthalIntegrationData = azimuthalIntegrator.integrate2D(detectorData,os.path.splitext(filePath)[0] + ".azim")

            params["results"][filePath] = azimuthalIntegrationData
            params["logger"].info('Child process integrated File: ' + filePath)
        except FileNotFoundError:
            params["logger"].error("FileNotFoundError: No such file or directory: " +filePath)   
                
                
    def fillQueue(paths,queue,params):
        nrOfJobs = 0
        for path in paths:
            for filePath in IO_Utils.getFilesThatEndwith(path,XRayDetectorDataParser.getAllowedFormats()):
                queue.put([AzimuthalIntegrationTask.processFile,[filePath,params,None]])
                #AzimuthalIntegrationTask.processFile([filePath,params,None])
                nrOfJobs +=1
        return nrOfJobs
                        
    def runTask(outputPath,npt_rad,npt_azim,radial_range,settingJson,filePaths: list,progressBars: list,pool:Pool): 
            executionStart = time.time()   
            azimuthalIntegrator = AzimuthalIntegrator(settingJson=settingJson,args = [npt_rad,npt_azim,radial_range])     
            
             #get logger which is used by the manager
            pool.reinitialize([azimuthalIntegrator],3)#very unclean
            logger = pool.getLogger()
            #settings up the logger filter (INFO,WARNING,ERROR)
            logger.setLevel(TaskConfigs.AzimuthalIntegrationTask_Config.loggingLevel)
            
            logger.info("Starting Task %s..."%(TaskConfigs.AzimuthalIntegrationTask_Config.taskName))
            
            
            manager = pool.getManager()
            
            queue =  pool.getQueue()
            settings = json.load(open(settingJson))
            params = {"logger":logger,"azimuthalIntegrator":None,
                                   "results":manager.dict({"units":TaskConfigs.AzimuthalIntegrationTask_Config.units,
                                    "settings":[{"pyFai_setting_json":settings}|{"npt_rad":npt_rad,"npt_azim":npt_azim,"radial_range":radial_range}]})
                                    }
            
            pool.idle()
            nrOfJobs =  AzimuthalIntegrationTask.fillQueue(filePaths,queue,params)
            pool.start()
            
            
            azimuthalIntegration_results =dict(sorted(params["results"].items()))
            
            while(len(params["results"].keys()) < nrOfJobs):
                time.sleep(1)
                logger.info("Reporting progress:    "+str(((len(params["results"].keys())/(nrOfJobs+1) *100)))+ "%")

            logger.info("Finished Task in %ss"%(str(time.time()-executionStart))) 
            
            return azimuthalIntegration_results