import os
import pickle
import re

from IO import IO_Utils

eachDirectoryPickle_FileName = -2

def writePickle_single(params):
    """Pickles the entire result dictionary in the defined outputDirectory

    Args:
        params (dictionary): Required Keys: dict,prefix,outputPath
    """
    
    dictionary = params["dict"]
    filePrefix = params["prefix"]
    outputPath = params["outputPath"]
    

    fileName =filePrefix+".pickle"
    

    filePath = outputPath+"/"+fileName
    pickle.dump(dictionary,open(filePath, "wb"))
    
def writePickle_eachDirectory(params):
    """Pickles the corresponding part of the result dictionary in the directory where the raw files of that part lie.
    

    Args:
        params (dictionary): Required Keys: "prefix" -for filename , "dict" - dictionary to store, "overwrite" - deprecated 
    """
        
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
        """Loads pickle file

        Args:
            params (dictionary): Required keys: "prefix","file"

        Returns:
            _type_: _description_
        """
        filePrefix = params["prefix"]
        filePath = params["file"]
        
        directory = IO_Utils.getDirectory(filePath)
        directory = directory.replace("\\", "/").replace("\\","/")
        
        filepath = directory +"/"+filePrefix+".pickle"
        
        files = pickle.load(
                open(filepath, "rb"))
        
        return files