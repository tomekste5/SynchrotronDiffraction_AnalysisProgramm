import time

from Utils.Param import Param
#from GUI import GUI
from Tasks import TaskRegister

from Multiprocessing.Pool import Pool
taskRegister = TaskRegister.taskRegister
from Core.TaskQueue import TaskQueue


class Core:

    def __init__(self):
        """Initializes Param instance where the gui will later fill all enrolled parameters
           Then inits the multiprocessing pool with 4 processes and finally starts the GUI.
        """
        self.__guiParams = Param()
        self.__pool = Pool(4)
        #self.__gui =  GUI.GUI()

    def getSelfInstance(self):
        """_summary_

        Returns:
            Core: returns instance of itself
        """
        return self
    def getParamObj(self):
        """ 

        Returns:
            Param: Returns param object
        """
        return self.__guiParams

    def run(self):
        """When called adds all tasks that were selected in params instance by the gui to the taskqueue then start it
        """
        execStart_time = time.time() 
        taskQueue = TaskQueue(taskRegister,pool=self.__pool)
        taskQueue.addTasks(params=self.__guiParams, taskNames=self.__guiParams.getTasks())

        taskQueue.run()
        print("(Task Queue) Total Execution time: " +str(time.time()-execStart_time))

    def shutdown(self):
        """Kills multiprocessing pool  
        """
        self.__pool.shutdown()