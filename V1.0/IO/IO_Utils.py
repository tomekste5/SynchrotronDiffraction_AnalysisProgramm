import os

#return directory of file
def getDirectory(filePath):
    """Return the directory of given file

    Args:
        filePath (string): file path

    Returns:
        string: directory path
    """
    return os.path.split(filePath)[0]

#return all files in a directory (recursively) that end with specified fileType
def getFilesThatEndwith(path, fileTypes):
    """Returns all files that end with a specified file endings recursively

    Args:
        path (string): Path to directory where should be searched
        fileTypes (list): list of file endings that should be returned

    Raises:
        FileNotFoundError: When Nothing is found

    Returns:
        list: path to found files
    """
    graph = []
    for files in  os.walk(path):
        for file in files[2]:
            for fileType in fileTypes:
                if(file.lower().endswith(fileType)):
                        graph.append(files[0]+"/"+file)
    if graph == [] and not  os.path.isfile(path):
        raise FileNotFoundError
    if os.path.isfile(path):
        return [path]
    return graph