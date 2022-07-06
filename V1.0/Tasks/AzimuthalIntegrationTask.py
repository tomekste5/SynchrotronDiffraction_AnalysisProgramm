import os
import time

from Tasks.Config import TaskConfigs
from IO.Parser import XRayDetectorDataParser
from IO import IO_Utils
from Multiprocessing.Pool import Pool
from IO.Parser import XRayDetectorDataParser
import json
from libarys.AzimuthalIntegrator import AzimuthalIntegrator

class AzimuthalIntegrationTask():
    """_summary_
    
    """
    def getDescription():
        return "Does things"
    def getFuncName():
        return "azimuthal_integration"
    def getDependencies():
        return {}
    
    def processFile(callParams):
        """does azimuthal integration for file which is passed and writes results in the results dict.

        Keyword arguments:
        callParams -- is a list which consists of [the filepath, param object,None,and a instance of a setup azimuthal integrator (see PyFAI documentation:https://pyfai.readthedocs.io/en/master/api/pyFAI.html#module-pyFAI.azimuthalIntegrator)] 
        """
        filePath, params,data,azimuthalIntegrator = callParams
        try:
            detectorData = TaskConfigs.AzimuthalIntegrationTask_Config.loadFunction(filePath)
            azimuthalIntegrationData = azimuthalIntegrator.integrate2D(detectorData,os.path.splitext(filePath)[0] + ".azim")

            params["results"][filePath] = azimuthalIntegrationData
            params["logger"].info('Child process integrated File: ' + filePath)
        except FileNotFoundError:
            params["logger"].error("FileNotFoundError: No such file or directory: " +filePath)   
                
                
    def fillQueue(paths,queue,params):
        """Fills the multiprocessing Queue with the files that are found in paths.

        Keyword arguments:
        paths -- path to detector files or directories filled with detector files
        queue--  Queue of multiprocessing pool
        """
        
        nrOfJobs = 0
        for path in paths:
            files = IO_Utils.getFilesThatEndwith(path,XRayDetectorDataParser.getAllowedFormats())

            for filePath in files:
                queue.put([AzimuthalIntegrationTask.processFile,[filePath,params,None]])
                #AzimuthalIntegrationTask.processFile([filePath,params,None])
                nrOfJobs +=1
        return nrOfJobs
                        
    def runTask(gui,outputPath,elabFtwJson,npt_rad,npt_azim,radial_range,azimIntegrator_settingJson,filePaths: list,progressBars: list,pool:Pool): 
            """Does a azimuthal integration for every detector file in filePaths using multiprocessing.

            Keyword arguments:
            outputPath -- Path to directory where to store the single results file
            elabFtwJson -- ELabFTWJson object which was used
            filePaths -- paths to detector files or directory´s that contain detector files
            progressBars -- handle to progress bar on gui
            pool -- multiprocessing pool
            
            
            npt_rad -- Number of points for radial integration
            npt_azim -- Number of points for 2D integration
            radial_range -- Radial range in which to integrate 
            azimIntegrator_settingJson -- Path to json file which contains the settings for the azimuthalIntegrator
            
            For more Information see: https://pyfai.readthedocs.io/en/master/api/pyFAI.html#module-pyFAI.azimuthalIntegrator 
            
            """ 

        
            executionStart = time.time()   
            azimuthalIntegrator = AzimuthalIntegrator(azimIntegrator_settingJson=azimIntegrator_settingJson,args = [npt_rad,npt_azim,radial_range])     
            
             #get logger which is used by the manager
            pool.reinitialize([azimuthalIntegrator],3)#very unclean
            logger = pool.getLogger()
            #settings up the logger filter (INFO,WARNING,ERROR)
            logger.setLevel(TaskConfigs.AzimuthalIntegrationTask_Config.loggingLevel)
            
            logger.info("Starting Task %s..."%(TaskConfigs.AzimuthalIntegrationTask_Config.taskName))
            
            
            manager = pool.getManager()
            
            queue =  pool.getQueue()
            settings = json.load(open(azimIntegrator_settingJson))
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
                progressBars[0]["value"] = (len(params["results"].keys())/(nrOfJobs+1) *100)
                logger.info("Reporting progress:    "+str(((len(params["results"].keys())/(nrOfJobs+1) *100)))+ "%")
                gui.update()

            logger.info("Finished Task in %ss"%(str(time.time()-executionStart))) 
            
            return azimuthalIntegration_results