import fabio
import numpy as np

def loadDetectorFileRaw(path):
    return fabio.open(path)
def loadAzimuthalIntegrationDataFile(params):
    azimuthalIntegrationData = []
    pathToAzimuthalFile = params["path"]
    precision = params["precision"]
    
    
    azimuthalFile = loadDetectorFileRaw(pathToAzimuthalFile)
    deltaTheta = -precision(azimuthalFile.header["2th_deg_min"]) + precision(azimuthalFile.header["2th_deg_max"])
    deltaChi = -precision(azimuthalFile.header["chi_min"])+precision(azimuthalFile.header["chi_max"])
    azimuthalIntegrationData.append(azimuthalFile.data)
    azimuthalIntegrationData.append(np.arange(precision(azimuthalFile.header["2th_deg_min"]),precision(azimuthalFile.header["2th_deg_max"]),deltaTheta/precision(azimuthalFile.header["Dim_1"])))
    azimuthalIntegrationData.append(np.arange(precision(azimuthalFile.header["chi_min"]),precision(azimuthalFile.header["chi_max"]),deltaChi/precision(azimuthalFile.header["Dim_2"])))
    
    return azimuthalIntegrationData
    
def getAllowedFormats():
    return [".cbf",".tif"]