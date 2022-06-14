import pandas as pd
import numpy as np
import re

from IO import IO_Utils

experimnentStrIdx = -2

def writeCSV_single(params):
    dictionary = params["dict"]
    overwrite = params["overwrite"]
    filePrefix = params["prefix"]
    path = params["outputPath"]
    
    csvContent = list()
    
    if("units" in set(dictionary)):
        csvContent.extend(dictionary["units"])
    """
    if("settings" in set(dictionary)):
        csvContent.extend(dictionary["settings"])
    """

    for file in dictionary:
        if("units" != file and "settings" != file):
            csvContent.extend(dictionary[file])
            
    fileName =filePrefix+".csv"
    filePath = path +"/"+fileName   
    pd.DataFrame().from_records(csvContent,index=None).to_csv(filePath,index=False) 
        
def writeCSV_eachDirectory(params):
    dictionary = params["dict"]
    filePrefix = params["prefix"]
    sortedDict = sorted(dictionary)
    currDirectory = IO_Utils.getDirectory(sortedDict[0]) 
    csvContent = list()
    
            
    if("units" in set(dictionary)):
        csvContent.extend(dictionary["units"])
        
    """
    if("settings" in set(dictionary)):
        csvContent.extend(dictionary["settings"])
    """

    
    for file in sortedDict:
        if("units" != file and "settings" != file):
            if(currDirectory not in  file):
                df = pd.DataFrame().from_records(csvContent,index=None)
                directoryR = currDirectory.replace("\\", "/").replace("\\","/")
                filename = re.split("\\ |\/ |/",directoryR)[experimnentStrIdx] +"_"+ filePrefix
                df.to_csv(directoryR +"/"
                            +filename+".csv",index=False)
                currDirectory = IO_Utils.getDirectory(file)
                csvContent = list()
                if("units" in set(dictionary)):
                    csvContent.extend(dictionary["units"])
            csvContent.extend(dictionary[file])
    df = pd.DataFrame().from_records(csvContent,index=None)
    directoryR = currDirectory.replace("\\", "/").replace("\\","/")
    filename = re.split("\\ |\/ |/",directoryR)[experimnentStrIdx] +"_"+ filePrefix
    df.to_csv(directoryR +"/"
                        +filename+".csv",index=False)
def writeCSV_settings(params):
    settings = params["settings"]
    """
    directory = IO_Utils.getDirectory(list(dictionary.keys())[0]).replace("\\", "/").replace("\\","/")
    toFind = re.split("\\ |\/ |/",directory)[eachDirectoryCSV_FileName]
    fileName ="".join(re.split("_",toFind)[0:-1])+"_"+filePrefix+".csv"
    
    path  = IO_Utils.getPathToResultDirectory(overwrite,toFind,directory,fileName)
    filePath = path +"/"+fileName   
    
    
    df = pd.DataFrame().from_records(settings,index=None)
    df.to_csv(filePath)
    """

#Deprecated
def writeCSV_eachFile(params):
    dictionary = params["dict"]
    
    for directory in dictionary:
        for file in dictionary[directory]:
            df = pd.DataFrame().from_records(dictionary["units"])
            df = df.append(pd.DataFrame().from_records(dictionary[directory][file],index=None))

            df.to_csv(file.replace(file.split(".")[-1],"csv"),index=False) 
                