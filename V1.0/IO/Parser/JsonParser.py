import json
from IO import IO_Utils
import numpy as np
import pickle
import os

class NpEncoder(json.JSONEncoder):
    """Makes Json.dump able to save numpy datatypes"""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def saveSettings_single(params):
    """Saves dictionary that contains the parameters that where used for the process step in defined output path

    Args:
        params (dictionary): Required keys: "dict","outputPath","prefix" - filename
    """
    
    dictionary = params["dict"]
    settings = dictionary["settings"][0]
    outputPath = params["outputPath"]
    filePrefix = params["prefix"]
    
    
    fileName =filePrefix+"_Settings"+".json"
    
    filePath = outputPath +"/"+fileName   
    
    json.dump(settings,open(filePath,"w"))

def writeJson_single(params):
    """Write dictionary to single json in defined output directory

    Args:
        params (dictionary): Required Keys: "dict", "prefix","outputPath"
    """
    
    dictionary = params["dict"]
    filePrefix = params["prefix"]
    outputPath = params["outputPath"]
    

    fileName =filePrefix+".json"
    

    filePath = outputPath+"/"+fileName
    json.dump(dictionary,open(filePath, "w"),cls=NpEncoder)
    
def writeJson_eachDirectory(params):
    """Writes a json file in each directory with the corresponding part in the results dictionary.

    Args:
        params (dictionary): Required keys: "prefix", "dict"
    """
        
    filePrefix = params["prefix"]
    dictionary = params["dict"]
    
    currentDirectory = IO_Utils.getDirectory(list(dictionary.keys())[0])
    
    
    pickleContent = {}
    #check if keywords like units or settings are present
    if("units" in set(dictionary)):
        pickleContent["units"] =  dictionary["units"]
        
    if("settings" in set(dictionary)):
        pickleContent["settings"] =  dictionary["settings"]
    
    
    for file in dictionary:
        if(currentDirectory not in file and file != "units" and file != "settings"):
            #pickle pickle content for currDirectory
            currentDirectory = currentDirectory.replace("\\", "/").replace("//","/")
            
            fileName = filePrefix+".json"
            
            filePath = currentDirectory+"/"+fileName
            
            if(not os.path.exists(filePath)):
                pickle.dump(pickleContent,open(filePath, "wb"))
            
            
            
            #start new pickle content for new directory   
            currentDirectory = IO_Utils.getDirectory(file)
            pickleContent = {}
            
            if("units" in set(dictionary)):
                pickleContent["units"] =  dictionary["units"]
        
            if("settings" in set(dictionary)):
                pickleContent["settings"] =  dictionary["settings"]

            
            
        pickleContent[file] = dictionary[file]
        
    currentDirectory = currentDirectory.replace("\\", "/").replace("//","/")
    
    fileName = filePrefix+".json"
    
    filePath = currentDirectory+"/"+fileName
    
    if(not os.path.exists(filePath)):
        json.dump(pickleContent,open(filePath, "w"),cls=NpEncoder)
        