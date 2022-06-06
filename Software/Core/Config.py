import numpy as np

class TaskConfigs():
    class AxisTransformFitTask_Config():
        filenamePrefix = "elyptical_data_"
        taskName = "elyptical_fit"
        description = "Does things"
        dependencies = {TaskConfigs.VoigtFitTask_Config:1}
        precision = np.longdouble
        readMode = ["multipleD_pickle"]
        modes=["single_csv"]
        lambdaFileNr = lambda path: path[-9:-4]
        lambdaDirectoryNr = lambda path: path[-15:-10]
        preFix = "axisTransform"
        units = [{"File":"filepath","Z_pos":"mm","x_pos":"mm"} |{"strainYY":"1/1","strainZZ":"1/1","strainYZ":"1/1","strainYY_Err":"1/1","strainZZ_Err":"1/1","strainYZ_Err":"1/1"}|{"stressXX":"Pa","stressYY":"Pa","stressYZ":"Pa","stressHydro":"Pa","stressMises":"Pa"}| {"FWHM":"unknown","A":"xray count" }] 
    
    class VoigtFitTask_Config():
        filenamePrefix = "PseudoVoigt_data_"
        taskName = "pseudoVoigt_fit"
        description = "Does things"
        dependencies = {AzimuthalIntegrationTask.getFuncName():1}
        paramsToExport = ["FilePath,Azim,LorCoeff","A","x0","FWHM","LorCoeff_Err","A_Err","x0_Err","FWHM_Err"]
        precision = np.longdouble
        preFix = "pseudoVoigt"
        modes = ["single_csv","multipleD_csv","multipleD_pickle"]
        units = [{"FilePath":"string","azimAngle":"°"}| {"LorCoeff":"unknown","A":"xray count","x0":"°","FWHM":"unknown","LorCoeff_Err":"unknown","A_Err":"xray count","x0_Err":"°","FWHM_Err":"unkown"}]
        
    class AzimuthalIntegrationTask_Config():
        filenamePrefix = "AzimuthalIntegration_data_"
        taskName = "azimuthal_integration"
        description = "Does things"
        dependencies = {}
        paramsToExport = ["FilePath,Azim,LorCoeff","A","x0","FWHM","LorCoeff_Err","A_Err","x0_Err","FWHM_Err"]
        precision = np.longdouble
        preFix = "pseudoVoigt"
        modes = ["single_csv","multipleD_csv","multipleD_pickle"]
        units = [{"FilePath":"string","azimAngle":"°"}| {"LorCoeff":"unknown","A":"xray count","x0":"°","FWHM":"unknown","LorCoeff_Err":"unknown","A_Err":"xray count","x0_Err":"°","FWHM_Err":"unkown"}]