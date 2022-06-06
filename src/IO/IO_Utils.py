from fileinput import filename
from cv2 import sort
import fabio
import os
import pandas as pd
from sympy import false, true
import mmap
import csv
import numpy as np
import pickle
import bz2 
import re
import shutil

class SearchUtils:
    def getDirectory(filePath):
        return os.path.split(filePath)[0]

    def getFilesThatEndwith(path, fileType):
        graph = []
        for files in os.walk(path):
            for file in files[2]:
                if(file.lower().endswith(fileType)):
                        graph.append(path+"/"+file)
        return graph
    def getResultDirectory(overwrite,toFind,directory,fileName, newRUN = True):
        idx = directory.find(toFind)
        resDirectory = directory[:idx]+"".join(re.split("_",toFind)[0:-1])+"_Results_"
        runNr = 0
        run_resDirectory = resDirectory + "Run" + f"{runNr:03}"
        
        if(os.path.exists(run_resDirectory+"/") or not newRUN):
            return run_resDirectory
        
        elif(not overwrite and newRUN):
            while(os.path.exists(run_resDirectory)):
                run_resDirectory = resDirectory + ("Run"+f"{runNr:03}")
                runNr +=1
        else:
            shutil.rmtree(resDirectory)     
        os.makedirs(run_resDirectory)
        return run_resDirectory

"""
class IO:
        
    def loadDict(path, mode,args={}):
        loadModes = {"single_pickle":IO.preloadPickle_eachDirectory,"multipleD_pickle":IO.preloadPickle_eachDirectory,
                 "single_csv":IO.preloadPickle_eachDirectory,
                 "multiple_csv":IO.writeCSV_eachFile,
                 "multipleD_csv":IO.preloadPickle_eachDirectory
                 }#put into settings
        params = {"file":path} |args
        return loadModes[mode](params)
    
    
    
    def getResultDirectory(overwrite,toFind,directory,fileName, newRUN = True):
        idx = directory.find(toFind)
        resDirectory = directory[:idx]+"".join(re.split("_",toFind)[0:-1])+"_Results_"
        runNr = 0
        run_resDirectory = resDirectory + "Run" + f"{runNr:03}"
        
        if(os.path.exists(run_resDirectory+"/") or not newRUN):
            return run_resDirectory
        
        elif(not overwrite and newRUN):
            while(os.path.exists(run_resDirectory)):
                run_resDirectory = resDirectory + ("Run"+f"{runNr:03}")
                runNr +=1
        else:
            shutil.rmtree(resDirectory)     
        os.makedirs(run_resDirectory)
        return run_resDirectory
    
    
    def writeCSV_single(params):
        dictionary = params["dict"]
        overwrite = params["overwrite"]
        filePrefix = params["prefix"]
        
        csvContent = list()
        
        if("units" in set(dictionary)):
            csvContent.extend(dictionary["units"])
            dictionary.pop("units")
        for file in sorted(dictionary):
            csvContent.extend(dictionary[file])
        df = pd.DataFrame().from_records(csvContent,index=None)
        directory = SearchUtils.getDirectory(file).replace("\\", "/").replace("\\","/")
        toFind = re.split("\\ |\/ |/",directory)[-2]
        fileName ="".join(re.split("_",toFind)[0:-1])+"_"+filePrefix+".csv"
        
        path  = IO.getResultDirectory(overwrite,toFind,directory,fileName)
        filePath = path +"/"+fileName   
        df.to_csv(filePath,index=false) 
            
    def writeCSV_eachDirectory(params):
        dictionary = params["dict"]
        filePrefix = params["prefix"]
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
                filename = re.split("\\ |\/ |/",directoryR)[-2] +"_"+ filePrefix
                df.to_csv(directoryR +"/"
                            +filename+".csv",index=false)
                currDirectory = SearchUtils.getDirectory(file)
                csvContent = list()
                if("units" in set(dictionary)):
                    csvContent.extend(dictionary["units"])
            csvContent.extend(dictionary[file])
        df = pd.DataFrame().from_records(csvContent,index=None)
        directoryR = currDirectory.replace("\\", "/").replace("\\","/")
        filename = re.split("\\ |\/ |/",directoryR)[-2] +"_"+ filePrefix
        df.to_csv(directoryR +"/"
                            +filename+".csv",index=false)
            
    def writeCSV_eachFile(params):
        dictionary = params["dict"]
        for directory in dictionary:
            for file in dictionary[directory]:
                df = pd.DataFrame().from_records(dictionary[directory][file],index=None)

                df.to_csv(file.replace(file.split(".")[-1],"csv"),index=false) 
                

    def preloadPickle_eachDirectory(params):
        filePrefix = params["prefix"]
        filePath = params["file"]
        
        directory = SearchUtils.getDirectory(filePath)
        directory = directory.replace("\\", "/").replace("\\","/")
        filename = re.split("\\ |\/ |/",directory)[-2]
        filepath = directory +"/"+filename+"_"+filePrefix+".pickle"
        files = pickle.load(
                open(filepath, "rb"))
        return files
    
    def writePickle_single(params):
        dictionary =  dict(params["dict"])
        overwrite = params["overwrite"]
        
        directoryPath_parsed = list(dictionary.keys())[1].replace("\\", "/").replace("//","/")
        fileName = "".join(re.split("_",re.split("/",directoryPath_parsed)[-3])[:-1])+".pickle"
        toFind = re.split("\\ |\/ |/",directoryPath_parsed)[-3]
        path  = IO.getResultDirectory(overwrite,toFind,directoryPath_parsed,fileName,True)

        filePath = path+"/"+fileName
        pickle.dump(dictionary,open(filePath, "wb"))
        
    def writePickle_eachDirectory(params):
        currentDirectory = SearchUtils.getDirectory(sorted(params["dict"])[0])
        filePrefix = params["prefix"]
        content = dict()
        for file in sorted(params["dict"]):
            if(currentDirectory not in file):
                directoryPath_parsed = currentDirectory.replace("\\", "/").replace("//","/")
                fileName = re.split("\\ |\/ |/",directoryPath_parsed)[-2]+"_"+filePrefix+".pickle"
                filePath = directoryPath_parsed+"/"+fileName
                if(not os.path.exists(filePath) or params["overwrite"]):
                    pickle.dump(content,open(filePath, "wb"))
                currentDirectory = SearchUtils.getDirectory(file)
                content = dict()
            content[file] = params["dict"][file]
        directoryPath_parsed = currentDirectory.replace("\\", "/").replace("//","/")
        fileName = re.split("\\ |\/ |/",directoryPath_parsed)[-2]+"_"+filePrefix+".pickle"
        filePath = directoryPath_parsed+"/"+fileName
        if(not os.path.exists(filePath) or params["overwrite"]):
            pickle.dump(content,open(filePath, "wb"))
            
    
    def saveResultDictToFile(dicts,modes,path="",overwrite=False, args={}):
        defModes = {"single_pickle":IO.writePickle_single,"multipleD_pickle":IO.writePickle_eachDirectory,
                 "single_csv":IO.writeCSV_single,
                 "multiple_csv":IO.writeCSV_eachFile,
                 "multipleD_csv":IO.writeCSV_eachDirectory
                 }#put into settings
        params = {"dict":dicts,"path":path,"overwrite":overwrite} | args
        for mode in modes:
            defModes[mode](params)
"""