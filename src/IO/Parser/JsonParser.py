import json
from IO import IO_Utils
import re
import numpy as np
import pickle
import os

eachDirectoryCSV_FileName = -2

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



eachDirectoryPickle_FileName = -2

def writeJson_single(params):
    
    dictionary = params["dict"]
    overwrite = params["overwrite"]
    filePrefix = params["prefix"]
    path = params["outputPath"]
    

    fileName =filePrefix+".json"
    

    filePath = path+"/"+fileName
    json.dump(dictionary,open(filePath, "w"),cls=NpEncoder)
    
def writeJson_eachDirectory(params):
        
    filePrefix = params["prefix"]
    dictionary = params["dict"]
    overwrite = params["overwrite"]
    
    currentDirectory = IO_Utils.getDirectory(list(dictionary.keys())[0])
    
    
    dictToPickle = {}
    if("units" in set(dictionary)):
        dictToPickle["units"] =  dictionary["units"]
        
    if("settings" in set(dictionary)):
        dictToPickle["settings"] =  dictionary["settings"]
    
    for file in dictionary:
        if(currentDirectory not in file and file != "units" and file != "settings"):
            directory_parsed = currentDirectory.replace("\\", "/").replace("//","/")
            
            fileName = re.split("\\ |\/ |/",directory_parsed)[eachDirectoryPickle_FileName]+"_"+filePrefix+".json"
            
            filePath = directory_parsed+"/"+fileName
            
            if(not os.path.exists(filePath) or overwrite):
                pickle.dump(dictToPickle,open(filePath, "wb"))
                
            currentDirectory = IO_Utils.getDirectory(file)
            dictToPickle = {}
            
            if("units" in set(dictionary)):
                dictToPickle["units"] =  dictionary["units"]
        
            if("settings" in set(dictionary)):
                dictToPickle["settings"] =  dictionary["settings"]

            
            
        dictToPickle[file] = dictionary[file]
        
    directory_parsed = currentDirectory.replace("\\", "/").replace("//","/")
    
    fileName = re.split("\\ |\/ |/",directory_parsed)[eachDirectoryPickle_FileName]+"_"+filePrefix+".json"
    
    filePath = directory_parsed+"/"+fileName
    
    if(not os.path.exists(filePath) or overwrite):
        json.dump(dictToPickle,open(filePath, "w"),cls=NpEncoder)
        