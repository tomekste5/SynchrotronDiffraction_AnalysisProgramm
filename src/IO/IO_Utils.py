import os

#return directory of file
def getDirectory(filePath):
    return os.path.split(filePath)[0]

#return all files in a directory (recursively) that end with specified fileType
def getFilesThatEndwith(path, fileTypes):
    graph = []
    for files in  os.walk(path):
        for file in files[2]:
            for fileType in fileTypes:
                if(file.lower().endswith(fileType)):
                        graph.append(files[0]+"/"+file)
    return path if os.path.isfile(path) else graph