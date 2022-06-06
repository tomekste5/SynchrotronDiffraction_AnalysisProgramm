from Tasks.Config import TaskConfigs
from Tasks.TaskRegister import taskRegister
class Task():
    def runTask():
        raise NotImplementedError
    def getDescription():
        raise NotImplementedError
    def getFuncName():
        raise NotImplementedError  
    def getDependencies():
        raise NotImplementedError
    def getInputParams():
        raise NotImplementedError
        