import numpy as np
from IO.Parser import CsvParser, MatlabParser,PickleParser,XRayDetectorDataParser,JsonParser
import logging



class AzimuthalIntegrationTask_Config():
    taskName = "azimuthal_integration" #used to identify the task 
    fileName_prefix = "AztimuthalIntegration"#prefix that is used for file that are written by this task 
    
    taskDescription = "Does a azimuthal integration of XDR-Detector data" #short Description currently unimplemented
    taskDependencies = {} #define if Task is dependent on other tasks following structure: [taskname:1] or [taskname:0] when the return values should always be ignored and instead load the written files with the results. 
    
    precision = np.float64 #which datatype to use !ONLY NUMPY DATATYPES!
    units = [{"FilePath":"string","azimAngle":"°"} #Units
             | {"LorCoeff":"unknown","A":"xray count","x0":"2 Theta","FWHM":"unknown","LorCoeff_Err":"unknown","A_Err":"xray count","x0_Err":"°","FWHM_Err":"unkown"}]
    
    
    loadFunction = XRayDetectorDataParser.loadDetectorFileRaw #function that is used to load the detector File
    
        
    #Since all Task have a standardized output (See Documentation) every parser function that was written for that type can be used for any Task!
    saveFunctions = [CsvParser.writeCSV_single,CsvParser.writeCSV_eachDirectory,PickleParser.writePickle_eachDirectory,PickleParser.writePickle_single,JsonParser.saveSettings_single] #Functions to call when saving the results 

    loggingLevel = logging.INFO #logging level
    
    
class peakFittingTask_Config():
    taskName = "peak_fit"
    fileName_prefix = "peakFitting"
    
    taskDescription = "Does a fit of a PseudoVoigt function to accurately fit peak in 2 Theta domain"
    taskDependencies = {AzimuthalIntegrationTask_Config.taskName :1}
    
    precision = np.float64
    units = [{"FilePath":"string","azimAngle":"°"}
             | {"LorCoeff":"unknown","A":"xray count","x0":"2 Theta","FWHM":"unknown","LorCoeff_Err":"unknown","A_Err":"xray count","x0_Err":"°","FWHM_Err":"unkown"}]
    
    loadFunction = XRayDetectorDataParser.loadAzimuthalIntegrationDataFile
    saveFunctions = [CsvParser.writeCSV_single,CsvParser.writeCSV_eachDirectory,PickleParser.writePickle_eachDirectory,PickleParser.writePickle_single,JsonParser.saveSettings_single,JsonParser.writeJson_single]
    
    loggingLevel = logging.INFO

class EllipticalStrainFitTask_Config():
    taskName = "ellipticalStrain_fit"
    fileName_prefix = "ellipticalStrain_Fit"
    
    taskDescription = "Does a fit of the strain ellipse to get strain values in xx,zz,xz axis and calculates stresses"
    taskDependencies = {peakFittingTask_Config.taskName:1}
    
    precision = np.float64
    units = [{"File":"filepath","Z_positions":"mm","X_positions":"mm"}
             | {"strainYY":"1","strainZZ":"1","strainYZ":"1","strainYY_Err":"1","strainZZ_Err":"1","strainYZ_Err":"1"}
             | {"stressXX":"Pa","stressYY":"Pa","stressYZ":"Pa","stressHydro":"Pa","stressMises":"Pa"}
             | {"FWHM":"unknown","A":"1","x0":"2 Theta"}]
    
    loadFunction = PickleParser.loadPickle
    saveFunctions=[CsvParser.writeCSV_single,CsvParser.writeCSV_eachDirectory,PickleParser.writePickle_eachDirectory,PickleParser.writePickle_single,JsonParser.saveSettings_single,JsonParser.writeJson_single]
    
    lambdaFileNr = lambda path: path[-9:-4] #to eval Z pos  (index of Z pos array )
    lambdaDirectoryNr = lambda path: path[-15:-10] #to eval X pos (index of X pos array )
    
    loggingLevel = logging.INFO
        