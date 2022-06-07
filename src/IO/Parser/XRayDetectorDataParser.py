import fabio
import numpy as np

def loadDetectorFileRaw(path):
    return fabio.open(path)
def loadAzimuthalIntegrationDataFile(params):
    data = []
    azimPath = params["path"]
    precision = params["precision"]
    
    
    azimFile = loadDetectorFileRaw(azimPath)
    deltaTheta = -precision(azimFile.header["2th_deg_min"]) + precision(azimFile.header["2th_deg_max"])
    deltaChi = -precision(azimFile.header["chi_min"])+precision(azimFile.header["chi_max"])
    data.append(azimFile.data)
    data.append(np.arange(precision(azimFile.header["2th_deg_min"]),precision(azimFile.header["2th_deg_max"]),deltaTheta/precision(azimFile.header["Dim_1"])))
    data.append(np.arange(precision(azimFile.header["chi_min"]),precision(azimFile.header["chi_max"]),deltaChi/precision(azimFile.header["Dim_2"])))
    
    return data
    
def getAllowedFormats():
    return [".cbf",".tif"]