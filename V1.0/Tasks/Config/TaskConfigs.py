import numpy as np
from IO.Parser import CsvParser,PickleParser,XRayDetectorDataParser,JsonParser
import logging
       
class AzimuthalIntegrationTask_Config():
    taskName = "azimuthal_integration"
    fileName_prefix = "AztimuthalIntegration"
    
    taskDescription = "Does things"
    taskDependencies = {}
    
    precision = np.longdouble
    units = [{"FilePath":"string","azimAngle":"°"}
             | {"LorCoeff":"unknown","A":"xray count","x0":"2 Theta","FWHM":"unknown","LorCoeff_Err":"unknown","A_Err":"xray count","x0_Err":"°","FWHM_Err":"unkown"}]
    
    loadFunction = XRayDetectorDataParser.loadDetectorFileRaw
    saveFunctions = [CsvParser.writeCSV_single,CsvParser.writeCSV_eachDirectory,PickleParser.writePickle_eachDirectory,PickleParser.writePickle_single,JsonParser.saveSettings_single]

    loggingLevel = logging.INFO
    
class PseudoVoigtFitTask_Config():
    taskName = "pseudoVoigt_fit"
    fileName_prefix = "pseudoVoigtFit"
    
    taskDescription = "Does things"
    taskDependencies = {AzimuthalIntegrationTask_Config.taskName :1}
    
    precision = np.longdouble
    units = [{"FilePath":"string","azimAngle":"°"}
             | {"LorCoeff":"unknown","A":"xray count","x0":"2 Theta","FWHM":"unknown","LorCoeff_Err":"unknown","A_Err":"xray count","x0_Err":"°","FWHM_Err":"unkown"}]
    
    loadFunction = XRayDetectorDataParser.loadAzimuthalIntegrationDataFile
    saveFunctions = [CsvParser.writeCSV_single,CsvParser.writeCSV_eachDirectory,PickleParser.writePickle_eachDirectory,PickleParser.writePickle_single,JsonParser.saveSettings_single,JsonParser.writeJson_single]
    
    loggingLevel = logging.INFO

class AxisTransformFitTask_Config():
    taskName = "axisTransform_fit"
    fileName_prefix = "AxisTransformFit"
    
    taskDescription = "Does things"
    taskDependencies = {PseudoVoigtFitTask_Config.taskName:1}
    
    precision = np.longdouble
    units = [{"File":"filepath","Z_positions":"mm","X_positions":"mm"}
             | {"strainYY":"1","strainZZ":"1","strainYZ":"1","strainYY_Err":"1","strainZZ_Err":"1","strainYZ_Err":"1"}
             | {"stressXX":"Pa","stressYY":"Pa","stressYZ":"Pa","stressHydro":"Pa","stressMises":"Pa"}
             | {"FWHM":"unknown","A":"1","x0":"2 Theta"}]
    
    loadFunction = PickleParser.loadPickle
    saveFunctions=[CsvParser.writeCSV_single,CsvParser.writeCSV_eachDirectory,PickleParser.writePickle_eachDirectory,PickleParser.writePickle_single,JsonParser.saveSettings_single,JsonParser.writeJson_single]
    
    lambdaFileNr = lambda path: path[-9:-4]
    lambdaDirectoryNr = lambda path: path[-15:-10]
    
    loggingLevel = logging.INFO
        