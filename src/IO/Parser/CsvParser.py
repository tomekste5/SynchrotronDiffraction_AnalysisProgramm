import pandas as pd
import numpy as np
import re

from IO.IO_Utils import SearchUtils

eachDirectoryCSV_FileName = -2

def writeCSV_single(params):
    paramsCpy = params.copy()
    dictionary = paramsCpy["dict"]
    overwrite = paramsCpy["overwrite"]
    filePrefix = paramsCpy["prefix"]
    
    csvContent = list()
    
    if("units" in set(dictionary)):
        csvContent.extend(dictionary["units"])
        dictionary.pop("units")
        
    for file in sorted(dictionary):
        csvContent.extend(dictionary[file])
        
    directory = SearchUtils.getDirectory(file).replace("\\", "/").replace("\\","/")
    toFind = re.split("\\ |\/ |/",directory)[eachDirectoryCSV_FileName]
    fileName ="".join(re.split("_",toFind)[0:-1])+"_"+filePrefix+".csv"
    
    path  = SearchUtils.getResultDirectory(overwrite,toFind,directory,fileName)
    filePath = path +"/"+fileName   
    pd.DataFrame().from_records(csvContent,index=None).to_csv(filePath,index=False) 
        
def writeCSV_eachDirectory(params):
    paramsCpy = params.copy()
    dictionary = paramsCpy["dict"]
    filePrefix = paramsCpy["prefix"]
    sortedKeys = sorted(dictionary)
    currDirectory = SearchUtils.getDirectory(sortedKeys[0]) 
    csvContent = list()
    
            
    if("units" in set(dictionary)):
        csvContent.extend(dictionary["units"])
        dictionary.pop("units")
    
    for file in sortedKeys:
        if(currDirectory not in  file):
            df = pd.DataFrame().from_records(csvContent,index=None)
            directoryR = currDirectory.replace("\\", "/").replace("\\","/")
            filename = re.split("\\ |\/ |/",directoryR)[eachDirectoryCSV_FileName] +"_"+ filePrefix
            df.to_csv(directoryR +"/"
                        +filename+".csv",index=False)
            currDirectory = SearchUtils.getDirectory(file)
            csvContent = list()
            if("units" in set(dictionary)):
                csvContent.extend(dictionary["units"])
        csvContent.extend(dictionary[file])
    df = pd.DataFrame().from_records(csvContent,index=None)
    directoryR = currDirectory.replace("\\", "/").replace("\\","/")
    filename = re.split("\\ |\/ |/",directoryR)[eachDirectoryCSV_FileName] +"_"+ filePrefix
    df.to_csv(directoryR +"/"
                        +filename+".csv",index=False)
        
def writeCSV_eachFile(params):
    paramsCpy = params.copy()
    dictionary = paramsCpy["dict"]
    
    for directory in dictionary:
        for file in dictionary[directory]:
            df = pd.DataFrame().from_records(dictionary["units"])
            df = df.append(pd.DataFrame().from_records(dictionary[directory][file],index=None))

            df.to_csv(file.replace(file.split(".")[-1],"csv"),index=False) 
                