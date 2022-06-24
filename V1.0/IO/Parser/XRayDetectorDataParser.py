import fabio
import numpy as np

def loadDetectorFileRaw(path):
    """Loads Detector file

    Args:
        path (string): path to detector file

    Returns:
        fabioimage: return the data in an fabioimage
    """
    return fabio.open(path)
def loadAzimuthalIntegrationDataFile(params):
    """Loads a .azim file and returns it in the format required by PseudoVoigtFitTask 

    Args:
        params (dictionary): setup parameters see source code

    Returns:
        dictionary: Returns azimuthal integration in required format
    """
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
    """Returns a list of detector file types that are supported by this software

    Returns:
        list: list of supported file endings
    """
    return [".cbf",".tif"] #fabio is capeble of many more types and this software as well expect types that use multiimages