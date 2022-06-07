import os
import pickle
import re

from IO.IO_Utils import SearchUtils

eachDirectoryPickle_FileName = -2

def writePickle_single(params):
    
    paramsCpy = params.copy()
    dictionary = paramsCpy["dict"]
    overwrite = paramsCpy["overwrite"]
    filePrefix = paramsCpy["prefix"]
    
    
    directoryPath_parsed = list(dictionary.keys())[1].replace("\\", "/").replace("//","/")
    toFind = re.split("\\ |\/ |/",directoryPath_parsed)[eachDirectoryPickle_FileName]
    
    fileName ="".join(re.split("_",toFind)[0:-1])+"_"+filePrefix+".pickle"
    
    path  = SearchUtils.getResultDirectory(overwrite,toFind,directoryPath_parsed,fileName,True)

    filePath = path+"/"+fileName
    pickle.dump(dictionary,open(filePath, "wb"))
    
def writePickle_eachDirectory(params):
    paramsCpy = params.copy()
        
    filePrefix = paramsCpy["prefix"]
    dictionary = paramsCpy["dict"]
    overwrite = paramsCpy["overwrite"]
    sortedKeys = sorted(dictionary)
    
    currentDirectory = SearchUtils.getDirectory(sortedKeys[0])
    
    
    dictToPickle = {}
    
    for file in sortedKeys:
        if(currentDirectory not in file):
            directory_parsed = currentDirectory.replace("\\", "/").replace("//","/")
            
            fileName = re.split("\\ |\/ |/",directory_parsed)[eachDirectoryPickle_FileName]+"_"+filePrefix+".pickle"
            
            filePath = directory_parsed+"/"+fileName
            
            if(not os.path.exists(filePath) or overwrite):
                pickle.dump(dictToPickle,open(filePath, "wb"))
                
            currentDirectory = SearchUtils.getDirectory(file)
            dictToPickle = {}
            
        dictToPickle[file] = dictionary[file]
        
    directory_parsed = currentDirectory.replace("\\", "/").replace("//","/")
    
    fileName = re.split("\\ |\/ |/",directory_parsed)[eachDirectoryPickle_FileName]+"_"+filePrefix+".pickle"
    
    filePath = directory_parsed+"/"+fileName
    
    if(not os.path.exists(filePath) or overwrite):
        pickle.dump(dictToPickle,open(filePath, "wb"))
        
def loadPickle_eachDirectory(params):
        paramsCpy = params.copy()
        filePrefix = paramsCpy["prefix"]
        filePath = paramsCpy["file"]
        
        directory = SearchUtils.getDirectory(filePath)
        directory = directory.replace("\\", "/").replace("\\","/")
        
        filename = re.split("\\ |\/ |/",directory)[eachDirectoryPickle_FileName]
        filepath = directory +"/"+filename+"_"+filePrefix+".pickle"
        
        files = pickle.load(
                open(filepath, "rb"))
        
        return files