from IO.IO_Utils import DetectorDataParser, SearchUtils, IO


from queue import Empty
import time

import multiprocessing as mp
from multiprocessing import Process
import logging
from Tasks.VoigtFitTask import PseudoVoigt_Config


from Tasks.Task import Task
import numpy as np
import mmap

from scipy.optimize import curve_fit


class Config():
    filenamePrefix = "elyptical_data_"
    taskName = "elyptical_fit"
    description = "Does things"
    dependencies = {PseudoVoigt_Config.taskName:1}
    precision = np.longdouble
    readMode = ["multipleD_pickle"]
    modes=["single_csv"]
    lambdaFileNr = lambda path: path[-9:-4]
    lambdaDirectoryNr = lambda path: path[-15:-10]
    preFix = "axisTransform"
    units = [{"File":"filepath","Z_pos":"mm","x_pos":"mm"} |{"strainYY":"1/1","strainZZ":"1/1","strainYZ":"1/1","strainYY_Err":"1/1","strainZZ_Err":"1/1","strainYZ_Err":"1/1"}|{"stressXX":"Pa","stressYY":"Pa","stressYZ":"Pa","stressHydro":"Pa","stressMises":"Pa"}| {"FWHM":"unknown","A":"xray count" }] 
    


class AxisTransformFit():
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
            strain = ((wavelength/(2*np.sin((x0/2)*np.pi/180)))-d0)/d0
            par = curve_fit(AxisTransformFit.poly1,np.sin(azimuthalAngles*np.pi/180)**2,strain)[0]
            initialGuess = [par[0]+par[1],par[1],0]

            normalStrains, normalStrains_conv = curve_fit(AxisTransformFit.axisTransformFit,azimuthalAngles*np.pi/180,strain,initialGuess,ftol=10**(-12))
            normalStrains_err = np.sqrt(np.diag(normalStrains_conv))
                    
            return {"strainYY":normalStrains[0],"strainZZ":normalStrains[1],"strainYZ":normalStrains[2],"strainYY_Err":normalStrains_err[0],"strainZZ_Err":normalStrains_err[1],"strainYZ_Err":normalStrains_err[2]}
        else:
            return {"strainYY":0,"strainZZ":0,"strainYZ":0,"strainYY_Err":0,"strainZZ_Err":0,"strainYZ_Err":0}

class AxisTransformationTask:
    
    def doAxisTransformation(q,params):
        while(True):
            try:
                directory,file = q.get(timeout=1)
                #if(funcRet["azimuthal_integration"] == None or azimFile not in set(funcRet["azimuthal_integration"])):
                try:
                    pseudoFitData =  params["funcRet"]["pseudoVoigt_fit"][file]
                except KeyError or TypeError:
                    pseudoFitData = params["reqFiles"][file]
                    
                azimuthalAngles,x0,x0_err= np.array([pseudoFitData[i]["azimAngle"] for i in range(len(pseudoFitData))]),np.array([pseudoFitData[i]["x0"] for i in range(len(pseudoFitData))]),np.array([pseudoFitData[i]["x0_Err"] for i in range(len(pseudoFitData))])
                
                fitData = AxisTransformFit.doFit(azimuthalAngles=azimuthalAngles,x0=x0,x0_err=x0_err,d0=params["d0"],wavelength=Config.precision(params["wavelength"]))
 
                E=params["dxxxE"]
                poisson=params["dxxxP"]

                strainYY = fitData["strainYY"]
                strainZZ = fitData["strainZZ"]
                strainYZ = fitData["strainYZ"]

                stressyy=(E/((1+poisson)*(1-2*poisson)))*((1-poisson)*strainYY)+(E/((1+poisson)*(1-2*poisson)))*((poisson)*strainZZ)+(E/((1+poisson)*(1-2*poisson)))*((poisson)*0)
                stresszz=(E/((1+poisson)*(1-2*poisson)))*((1-poisson)*strainZZ)+(E/((1+poisson)*(1-2*poisson)))*((poisson)*strainYY)+(E/((1+poisson)*(1-2*poisson)))*((poisson)*0)
                stressyz=(E/((1+poisson)*(1-2*poisson)))*((1-2*poisson)*strainYZ)


                stressxx=(E/((1+poisson)*(1-2*poisson)))*((1-poisson)*0)+(E/((1+poisson)*(1-2*poisson)))*((poisson)*strainZZ)+(E/((1+poisson)*(1-2*poisson)))*((poisson)*strainYY)

                stressmises=np.sqrt((1/2)*((stressxx-stressyy)**2+(stressyy-stresszz)**2+(stresszz-stressxx)**2+6*stressyz**2))

                stresshydro=(stressxx+stressyy+stresszz)/3

                
                
                params["returnVal"][file] = [{"File":file,"Z_positions":params["Z_positions"][int(Config.lambdaFileNr(file))-1],"Y_positions":params["Y_positions"][int(Config.lambdaDirectoryNr(file))-1]}| fitData | {"stressXX":stressxx,"stressYY":stressyy,"stressYZ":stressyz,"stressHydro":stresshydro,"stressMises":stressmises} | {"FWHM":np.mean(np.array([pseudoFitData[i]["FWHM"] for i in range(len(pseudoFitData))])),"A":np.mean(np.array([pseudoFitData[i]["A"] for i in range(len(pseudoFitData))]))}]
     
                params["logger"].info("Fitted File: " + file)
            except Empty:
                break
            except FileNotFoundError:
                params["logger"].error("FileNotFoundError: No such file or directory: " +file)   
    
    def fillQueue(funcRet,directoryPaths,mode,queue):
        reqFiles = {}
        for path in directoryPaths:
            for file in SearchUtils.getFilesThatEndwith(path,".cbf"):
                queue.put([SearchUtils.getDirectory(file),file])
                if(not PseudoVoigt_Config.taskName in funcRet.keys() and not SearchUtils.getDirectory(file) in set(reqFiles)):
                    reqFiles =  reqFiles | IO.loadDict(file,Config.readMode[0],args={"prefix":PseudoVoigt_Config.preFix})
        return reqFiles
    
    def runTask(minTheta,directoryPaths,isMultiProcessingAllowed,wavelength,peak,E,Possions,d0,Z_positions,Y_positions,handles,funcRet):
        startExecTime = time.time() 
                
        m = mp.Manager()
        logger = mp.log_to_stderr()
        logger.setLevel(logging.INFO)
                
        processQueue = m.Queue()

        reqFiles = AxisTransformationTask.fillQueue(funcRet,directoryPaths,1,processQueue)
            
        params = m.dict({"reqFiles":reqFiles,"logger":logger,"returnVal":m.dict({"units":Config.units}),"funcRet":funcRet,"d0":d0,"wavelength":wavelength,"Z_positions":Z_positions,"Y_positions":Y_positions,"dxxxE":E[peak],"dxxxP":Possions[peak]})
                
        numberOfProcesses = mp.cpu_count()-1 if isMultiProcessingAllowed else 1
                
                
        workerProcesses = [] 
        for i in range(0,numberOfProcesses):
            workerP = Process(target=AxisTransformationTask.doAxisTransformation, args = (processQueue,params))
            workerP.daemon = True
            workerP.start()  # Launch reader_p() as another proc
            workerProcesses.append(workerP)
                
        for process in workerProcesses:
            process.join()
        #PseudoVoigtFit_CSVParser.writeResultsToCSV(results,Config.filenamePrefix)f
        logger.info("Finished Task in %ss"%(str(time.time()-startExecTime))) 
        results = dict(params["returnVal"])
        IO.saveResultDictToFile(results,modes=Config.modes,args={"prefix":Config.preFix})      
        del(m)
        return results
