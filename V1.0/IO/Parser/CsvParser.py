import pandas as pd

from IO import IO_Utils

experimnentStrIdx = -2

def writeCSV_single(params):
    """Writes dictionary to a single csv file in the defined output directory.

    Args:
        params (dictionary): Required keys: "dict", "prefix","outputPath"
    """
    dictionary = params["dict"]
    fileName_prefix = params["prefix"]
    outputPath = params["outputPath"]
    
    csvContent = list()
    
    if("units" in set(dictionary)):
        csvContent.extend(dictionary["units"])

    for file in dictionary:
        if("units" != file and "settings" != file):
            csvContent.extend(dictionary[file])
            
    fileName =fileName_prefix+".csv"
    filePath = outputPath +"/"+fileName   
    pd.DataFrame().from_records(csvContent,index=None).to_csv(filePath,index=False) 
        
def writeCSV_eachDirectory(params):
    """write a csv in each directory with the corresponding part of the result dictionary

    Args:
        params (dictionary): Required keys: "dict","prefix" - filename
    """
    dictionary = params["dict"]
    filePrefix = params["prefix"]
    currentDirectory = IO_Utils.getDirectory(sorted(dictionary)[0]) 
    
    csvContent = list()
    
            
    if("units" in set(dictionary)):
        csvContent.extend(dictionary["units"])
        

    
    for file in dictionary:
        if("units" != file and "settings" != file):
            if(currentDirectory not in  file):
                #write file
                directoryData = pd.DataFrame().from_records(csvContent,index=None)
                
                currentDirectory = currentDirectory.replace("\\", "/").replace("\\","/")
                fileName = filePrefix + ".csv"
                filePath = currentDirectory +"/"+fileName
                
                directoryData.to_csv(filePath,index=False)
                
                
                currentDirectory = IO_Utils.getDirectory(file)
                #reset csvContent
                csvContent = list()
                
                if("units" in set(dictionary)):
                    csvContent.extend(dictionary["units"])
                    
            csvContent.extend(dictionary[file])
            
            
    directoryData = pd.DataFrame().from_records(csvContent,index=None)
    currentDirectory = currentDirectory.replace("\\", "/").replace("\\","/")
    fileName = filePrefix + ".csv"
    filePath = currentDirectory +"/"+fileName
                
    directoryData.to_csv(filePath,index=False)

#Deprecated
def writeCSV_eachFile(params):
    """write for each detector file a csv file with the corresponding results

    Args:
        params (dictionary): Required keys: "dict"
    """
    dictionary = params["dict"]
    
    for directory in dictionary:
        for file in dictionary[directory]:
            df = pd.DataFrame().from_records(dictionary["units"])
            df = df.append(pd.DataFrame().from_records(dictionary[directory][file],index=None))

            df.to_csv(file.replace(file.split(".")[-1],"csv"),index=False) 
                