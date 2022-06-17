import json
from IO import IO_Utils
import numpy as np
import pickle
import os

def saveSettings_single(params):
    dictionary = params["dict"]
    settings = dictionary["settings"][0]
    outputPath = params["outputPath"]
    filePrefix = params["prefix"]
    
    
    fileName =filePrefix+"_Settings"+".json"
    
    filePath = outputPath +"/"+fileName   
    
    json.dump(settings,open(filePath,"w"))
    

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def writeJson_single(params):
    
    dictionary = params["dict"]
    filePrefix = params["prefix"]
    outputPath = params["outputPath"]
    

    fileName =filePrefix+".json"
    

    filePath = outputPath+"/"+fileName
    json.dump(dictionary,open(filePath, "w"),cls=NpEncoder)
    
def writeJson_eachDirectory(params):
        
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
        