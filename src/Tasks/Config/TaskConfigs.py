import numpy as np
from IO.Parser import CsvParser,PickleParser,XRayDetectorDataParser
import logging
       
class AzimuthalIntegrationTask_Config():
    filenamePrefix = "AzimuthalIntegration_data_"
    taskName = "azimuthal_integration"
    description = "Does things"
    dependencies = {}
    paramsToExport = ["FilePath,Azim,LorCoeff","A","x0","FWHM","LorCoeff_Err","A_Err","x0_Err","FWHM_Err"]
    precision = np.longdouble
    preFix = "AztimuthalIntegration"
    readFunction = XRayDetectorDataParser.loadDetectorFileRaw
    saveFunctions = [CsvParser.writeCSV_single,CsvParser.writeCSV_eachDirectory,PickleParser.writePickle_eachDirectory,PickleParser.writePickle_single]
    units = [{"FilePath":"string","azimAngle":"°"}| {"LorCoeff":"unknown","A":"xray count","x0":"2 Theta","FWHM":"unknown","LorCoeff_Err":"unknown","A_Err":"xray count","x0_Err":"°","FWHM_Err":"unkown"}]
    loggingLevel = logging.INFO
    
class VoigtFitTask_Config():
    filenamePrefix = "PseudoVoigt_data_"
    taskName = "voigt_fit"
    description = "Does things"
    dependencies = {AzimuthalIntegrationTask_Config.taskName :1}
    paramsToExport = ["FilePath,Azim,LorCoeff","A","x0","FWHM","LorCoeff_Err","A_Err","x0_Err","FWHM_Err"]
    precision = np.longdouble
    preFix = "VoigtFit"
    readFunction = XRayDetectorDataParser.loadAzimuthalIntegrationDataFile
    saveFunctions = [CsvParser.writeCSV_single,CsvParser.writeCSV_eachDirectory,PickleParser.writePickle_eachDirectory,PickleParser.writePickle_single]
    units = [{"FilePath":"string","azimAngle":"°"}| {"LorCoeff":"unknown","A":"xray count","x0":"2 Theta","FWHM":"unknown","LorCoeff_Err":"unknown","A_Err":"xray count","x0_Err":"°","FWHM_Err":"unkown"}]
    loggingLevel = logging.INFO

class AxisTransformFitTask_Config():
    filenamePrefix = "elyptical_data_"
    taskName = "axisTransform_fit"
    description = "Does things"
    dependencies = {VoigtFitTask_Config.taskName:1}
    precision = np.longdouble
    readFunction = PickleParser.loadPickle
    saveFunctions=[CsvParser.writeCSV_single,CsvParser.writeCSV_eachDirectory,PickleParser.writePickle_eachDirectory,PickleParser.writePickle_single]
    lambdaFileNr = lambda path: path[-9:-4]
    lambdaDirectoryNr = lambda path: path[-15:-10]
    preFix = "AxisTransformFit"
    units = [{"File":"filepath","Z_positions":"mm","X_positions":"mm"} |{"strainYY":"1/1","strainZZ":"1/1","strainYZ":"1/1","strainYY_Err":"1/1","strainZZ_Err":"1/1","strainYZ_Err":"1/1"}|{"stressXX":"Pa","stressYY":"Pa","stressYZ":"Pa","stressHydro":"Pa","stressMises":"Pa"}| {"FWHM":"unknown","A":"xray count","x0":"2 Theta"}]
    loggingLevel = logging.INFO
        