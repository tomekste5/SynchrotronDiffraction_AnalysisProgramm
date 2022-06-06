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

from IO.IO_Utils import SearchUtils

def writePickle_single(params):
    dictionary =  dict(params["dict"])
    overwrite = params["overwrite"]
    
    directoryPath_parsed = list(dictionary.keys())[1].replace("\\", "/").replace("//","/")
    fileName = "".join(re.split("_",re.split("/",directoryPath_parsed)[-3])[:-1])+".pickle"
    toFind = re.split("\\ |\/ |/",directoryPath_parsed)[-3]
    path  = SearchUtils.getResultDirectory(overwrite,toFind,directoryPath_parsed,fileName,True)

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
        
def loadPickle_eachDirectory(params):
        filePrefix = params["prefix"]
        filePath = params["file"]
        
        directory = SearchUtils.getDirectory(filePath)
        directory = directory.replace("\\", "/").replace("\\","/")
        filename = re.split("\\ |\/ |/",directory)[-2]
        filepath = directory +"/"+filename+"_"+filePrefix+".pickle"
        files = pickle.load(
                open(filepath, "rb"))
        return files