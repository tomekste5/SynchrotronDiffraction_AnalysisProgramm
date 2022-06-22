import os
import pickle
import re

from IO import IO_Utils

eachDirectoryPickle_FileName = -2

def writePickle_single(params):
    
    dictionary = params["dict"]
    filePrefix = params["prefix"]
    outputPath = params["outputPath"]
    

    fileName =filePrefix+".pickle"
    

    filePath = outputPath+"/"+fileName
    pickle.dump(dictionary,open(filePath, "wb"))
    
def writePickle_eachDirectory(params):
        
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
            
            fileName = filePrefix+".pickle"
            
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
    
    fileName = filePrefix+".pickle"
    
    filePath = directory_parsed+"/"+fileName
    
    if(not os.path.exists(filePath) or overwrite):
        pickle.dump(dictToPickle,open(filePath, "wb"))
        
def loadPickle(params):
        filePrefix = params["prefix"]
        filePath = params["file"]
        
        directory = IO_Utils.getDirectory(filePath)
        directory = directory.replace("\\", "/").replace("\\","/")
        
        filepath = directory +"/"+filePrefix+".pickle"
        
        files = pickle.load(
                open(filepath, "rb"))
        
        return files