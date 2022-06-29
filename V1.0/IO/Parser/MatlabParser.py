from scipy.io import savemat
compression = False 

def writeMatV5_single(params):
    dictionary = params["dict"]
    fileName_prefix = params["prefix"]
    outputPath = params["outputPath"]
    
    savemat(file_name=outputPath+"/"+fileName_prefix+".mat",mdict=dictionary,format='5',do_compression=compression)
    
def writeMatV4_single(params):
    dictionary = params["dict"]
    fileName_prefix = params["prefix"]
    outputPath = params["outputPath"]
    
    savemat(file_name=outputPath+"/"+fileName_prefix+".mat",mdict=dictionary,format='4',do_compression=compression)