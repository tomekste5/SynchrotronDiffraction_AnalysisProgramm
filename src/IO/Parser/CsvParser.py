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
    
    path  = SearchUtils.getResultDirectory(overwrite,toFind,directory,fileName)
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
                