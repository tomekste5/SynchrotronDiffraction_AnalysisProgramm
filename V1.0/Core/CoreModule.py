import time

from Utils.Param import param
#from GUI import GUI
from Tasks import TaskRegister

from Multiprocessing.Pool import Pool
taskRegister = TaskRegister.taskRegister
from Core.Queue import Queue


class Core:

    def __init__(self):
        self.__guiParams = param()
        self.__pool = Pool(4)
        #self.__gui =  GUI.GUI()

    def getSelfInstance(self):
        return self
    def getParamObj(self):
        return self.__guiParams

    def run(self):
        execStart_time = time.time() 
        taskQueue = Queue(taskRegister,pool=self.__pool)
        taskQueue.addTasks(params=self.__guiParams, tasks=self.__guiParams.getTasks())

        taskQueue.run()
        print("(Task Queue) Total Execution time: " +str(time.time()-execStart_time))

    def shutdown(self):
        self.__pool.shutdown()

    def cancel(self):
        pass
