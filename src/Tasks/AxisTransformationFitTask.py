from Tasks.Config import TaskConfigs
from IO import IO_Utils


from queue import Empty
import time

import multiprocessing as mp
from multiprocessing import Process
import logging


from Tasks.Task import Task
import numpy as np

from scipy.optimize import curve_fit
from Multiprocessing.Pool import Pool
from IO.Parser import XRayDetectorDataParser


class AxisTransformFit:
    def axisTransformFit(x,*p):
        eyy,ezz,eyz = p
        theta = 5.8*np.pi/180 #change!
        chi = x
        #'((sind(theta))^2)*(0)+((cosd(theta))^2)*((sind(chi))^2)*eyy+((cosd(theta))^2)*((cosd(chi))^2)*ezz-((sind(2*theta)))*((cosd(chi)))*0+((cosd(theta))^2)*((sind(2*chi)))*eyz'
        #((sind(2*theta)))*((cosd(chi)))*0+((cosd(theta))^2)*((sind(2*chi)))*eyz
        return ((np.cos(theta))**2)*((np.sin(chi))**2)*eyy+((np.cos(theta))**2)*((np.cos(chi))**2)*ezz+((np.cos(theta))**2)*((np.sin(2*chi)))*eyz

    def poly1(x,a, b, c):
        return a*x+b
    def doFit(azimuthalAngles,x0,x0_err,d0,wavelength):
        trashData_count = np.count_nonzero([(np.array(x0)/np.array(x0_err)) <= 0.01])
                
        if(trashData_count < len(azimuthalAngles)-6):
            strain = ((wavelength/(2*np.sin((x0/2)*np.pi/180)))-d0)/d0 #see brag eq
            par = curve_fit(AxisTransformFit.poly1,np.sin(azimuthalAngles*np.pi/180)**2,strain)[0]
            initialGuess = [par[0]+par[1],par[1],0]

            normalStrains, normalStrains_conv = curve_fit(AxisTransformFit.axisTransformFit,azimuthalAngles*np.pi/180,strain,initialGuess,ftol=10**(-12))
            normalStrains_err = np.sqrt(np.diag(normalStrains_conv))


                    
            return {"strainXX":normalStrains[0],"strainZZ":normalStrains[1],"strainXZ":normalStrains[2],"strainXX_Err":normalStrains_err[0],"strainZZ_Err":normalStrains_err[1],"strainXZ_Err":normalStrains_err[2]}
        else:
            return {"strainXX":0,"strainZZ":0,"strainXZ":0,"strainXX_Err":0,"strainZZ_Err":0,"strainXZ_Err":0}
    def getPrincipalStresses(E,poisson,strainYY,strainZZ,strainYZ):

            stressxx=(E/((1+poisson)*(1-2*poisson)))*((1-poisson)*strainYY)+(E/((1+poisson)*(1-2*poisson)))*((poisson)*strainZZ)+(E/((1+poisson)*(1-2*poisson)))*((poisson)*0)
            stresszz=(E/((1+poisson)*(1-2*poisson)))*((1-poisson)*strainZZ)+(E/((1+poisson)*(1-2*poisson)))*((poisson)*strainYY)+(E/((1+poisson)*(1-2*poisson)))*((poisson)*0)
            stressxz=(E/((1+poisson)*(1-2*poisson)))*((1-2*poisson)*strainYZ)


            stressxx=(E/((1+poisson)*(1-2*poisson)))*((1-poisson)*0)+(E/((1+poisson)*(1-2*poisson)))*((poisson)*strainZZ)+(E/((1+poisson)*(1-2*poisson)))*((poisson)*strainYY)

            stressmises=np.sqrt((1/2)*((stressxx-stressxx)**2+(stressxx-stresszz)**2+(stresszz-stressxx)**2+6*stressxz**2))

            stresshydro=(stressxx+stressxx+stresszz)/3

            return {"stressXX":stressxx,"stressZZ":stressxx,"stressXZ":stressxz,"stressHydro":stresshydro,"stressMises":stressmises}
        
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
        file, params, voigtFitData= callParams
        try:
            azimuthalAngles,x0,x0_err= np.array([voigtFitData[i]["azimAngle"] for i in range(len(voigtFitData))]),np.array([TaskConfigs.AxisTransformFitTask_Config.precision(voigtFitData[i]["x0"]) for i in range(len(voigtFitData))]),np.array([voigtFitData[i]["x0_Err"] for i in range(len(voigtFitData))])
            
            fitData = AxisTransformFit.doFit(azimuthalAngles=azimuthalAngles,x0=x0,x0_err=x0_err,d0=params["d0"],wavelength=TaskConfigs.AxisTransformFitTask_Config.precision(params["wavelength"]))

            E=params["E_Modules"]
            poisson=params["Possion_Numbers"]

            strainXX = fitData["strainXX"]
            strainZZ = fitData["strainZZ"]
            strainXZ = fitData["strainXZ"]

            principalStresses = AxisTransformFit.getPrincipalStresses(E=E,poisson=poisson,strainYY=strainXX,strainZZ=strainZZ,strainYZ=strainXZ)                
            
            params["returnVal"][file] = [{"File":file,"Z_positions":params["Z_positions"][int(TaskConfigs.AxisTransformFitTask_Config.lambdaFileNr(file))-1],"X_positions":params["X_positions"][int(TaskConfigs.AxisTransformFitTask_Config.lambdaDirectoryNr(file))-1]}| fitData |principalStresses| {"FWHM":np.mean(np.array([voigtFitData[i]["FWHM"] for i in range(len(voigtFitData))])),"A":np.mean(np.array([voigtFitData[i]["A"] for i in range(len(voigtFitData))])),"x0":np.mean(np.array([voigtFitData[i]["x0"] for i in range(len(voigtFitData))]))}]
    
            params["logger"].info("Fitted File: " + file)
        except Empty:
            pass
        except FileNotFoundError:
            params["logger"].error("FileNotFoundError: No such file or directory: " +file)   
    
    def fillQueue(funcRet,dataPaths,queue,params):
        nrOfTasks = 0
        reqFiles = {}
        for path in dataPaths:
            for file in IO_Utils.getFilesThatEndwith(path,XRayDetectorDataParser.getAllowedFormats()):
                if(not TaskConfigs.VoigtFitTask_Config.taskName in funcRet.keys() and not IO_Utils.getDirectory(file) in set(reqFiles)):
                    read_params  = {"file":file,"prefix":TaskConfigs.VoigtFitTask_Config.preFix}
                    reqFiles =  reqFiles | TaskConfigs.AxisTransformFitTask_Config.readFunction(read_params)
                if(TaskConfigs.VoigtFitTask_Config.taskName in funcRet.keys() and file in funcRet[TaskConfigs.VoigtFitTask_Config.taskName].keys()):
                    queue.put([AxisTransformationTask.doAxisTransformation,[file,params, funcRet[TaskConfigs.VoigtFitTask_Config.taskName][file]]])
                else:
                    queue.put([AxisTransformationTask.doAxisTransformation,[file,params, reqFiles[file]]])
                nrOfTasks +=1
        #out = params["settings"].append([reqFiles[file]["settings"] if reqFiles != {} else  funcRet[TaskConfigs.VoigtFitTask_Config.taskName]["settings"]])
        currSettings = params["returnVal"]["settings"][0]
        prevSettings = reqFiles[file]["settings"][0] if reqFiles != {} else  funcRet[TaskConfigs.VoigtFitTask_Config.taskName]["settings"][0]
        params["returnVal"]["settings"] = [currSettings | prevSettings]
        return nrOfTasks
    
    def runTask(outputPath,minTheta,dataPaths,wavelength,peak,E,Possions,d0,Z_positions,X_positions,handles: list,pool: Pool,funcRet: dict):
        
        execStart_time = time.time() 
        
        #get logger which is used by the manager
        logger = pool.getLogger()
        #settings up the logger filter (INFO,WARNING,ERROR)
        logger.setLevel(TaskConfigs.AxisTransformFitTask_Config.loggingLevel)
                
        logger.info("Starting Task %s..."%(TaskConfigs.AxisTransformFitTask_Config.taskName))
        
        m = pool.getManager()
                
        processQueue =pool.getQueue()
        
        params = m.dict({"logger":logger,"returnVal":m.dict({"units":TaskConfigs.AxisTransformFitTask_Config.units,
                                                             "settings":[{"wavelength":wavelength,"E-Modules":E,"possions":Possions,"d0":d0}]})
                         ,"d0":d0,"wavelength":wavelength,"Z_positions":Z_positions,"X_positions":X_positions,"E_Modules":E[peak],"Possion_Numbers":Possions[peak]})

        #To ensure processing doesnt start while filling the Queue (could result in blocking each other, so low speed)
        pool.idle()
        nrOfTasks = AxisTransformationTask.fillQueue(funcRet,dataPaths,processQueue,params)
        
        #release the worker processes to start processing the jobs
        pool.start()
        
        while(len(params["returnVal"].keys()) < nrOfTasks):
            time.sleep(1)
            logger.info("Reporting progress:    "+str(((len(params["returnVal"].keys())/(nrOfTasks+1) *100)))+ "%")
            #handles[0].set((len(params["returnVal"].keys())/(nrOfTasks+1) *100))
            
        
        AxisTransformationFit_results =dict(sorted(params["returnVal"].items()))
        
        save_Params = {"outputPath":outputPath,"dict": AxisTransformationFit_results,"prefix":TaskConfigs.AxisTransformFitTask_Config.preFix,"precision":TaskConfigs.AxisTransformFitTask_Config.precision,"overwrite":False}
        for saveDict in TaskConfigs.AxisTransformFitTask_Config.saveFunctions:
            saveDict(save_Params)  
            
        logger.info("Finished Task in %ss"%(str(time.time()-execStart_time)))
        
        return AxisTransformationFit_results
    
