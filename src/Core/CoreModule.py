import time

from Utils.Param import Param
#from GUI import GUI
from Tasks.Config import TaskConfigs
from Tasks import TaskRegister

from Multiprocessing.Pool import Pool
taskRegister = TaskRegister.taskRegister


class Queue:

    def getTasksByName(self, taskReg, tasks):
        return dict([(i, taskReg[i]) for i in tasks if i in set(taskReg)])

    def graphParser(task, tasks, taskPrio):

        for secTask in tasks:
            if(task in set(tasks[secTask]["dependencies"])):
                taskPrio = Queue.graphParser(secTask, tasks, taskPrio)
        return taskPrio+1

    def getTaskPriority(self, tasks):
        taskPrioritys = []

        taskNames = [task for task in tasks]
        if(len(tasks) > 1):
            for task in tasks:
                taskPrioritys.append(Queue.graphParser(task, tasks, 0)-1)

            [x for _, x in sorted(zip(taskPrioritys, taskNames))]
            return [task for _, task in sorted(zip(taskPrioritys, taskNames), reverse=True)]
        else:
            [x for _, x in sorted(zip([0], taskNames))]
            return [task for _, task in sorted(zip([0], taskNames), reverse=True)]

    def parseTasks(self, params, pool, taskIdentifiers):
        tasks = self.getTasksByName(taskRegister, taskIdentifiers)
        executionOrder = self.getTaskPriority(tasks)
        for taskID in executionOrder:
            dependencies = tasks[taskID]["dependencies"]
            if(len(dependencies) == 0):
                dependencies = None
            else:
                dependencies = [dependency for dependency in dependencies if (dependencies[dependency] and dependency in set(tasks))]

            comp = [func(params) for func in tasks[taskID]["input_params"]]
            if(tasks[taskID]["MultiProcessing"]):
                comp.append(pool["pool"])
            tasks[taskID]["input_params"] = comp
            tasks[taskID]["dependencies"] = dependencies
        return tasks, executionOrder

    def addTasks(self, params, pool, tasks):
        self.__taskQueue = self.parseTasks(params, pool, tasks)

    def run(self):
        startExecTime = time.time()
        for taskName in self.__taskQueue[1]:
            retVal = dict()
            if(self.__taskQueue[0][taskName]["dependencies"] != None):
                for func in self.__taskQueue[0][taskName]["dependencies"]:
                    retVal[func] = self.__taskQueue[0][func]["return_val"]
                self.__taskQueue[0][taskName]["return_val"] = self.__taskQueue[0][taskName]["handle"](*self.__taskQueue[0][taskName]["input_params"], retVal)

            else:
                self.__taskQueue[0][taskName]["return_val"] = self.__taskQueue[0][taskName]["handle"](*self.__taskQueue[0][taskName]["input_params"])
            #print(self.__taskQueue[0][taskName]["return_val"]['F:/NextCloud/University/2. FS/EDV/Versuch3/Versuch3\\v3_insitu_00008\pilatus\/v3_insitu_00008_00004.cbf'])
        print("[INFO/MainProcess] (Task Queue) Total Execution time: " +
              str(time.time()-startExecTime))


class Core:

    def __init__(self):
        self.__guiParams = Param()
        self.__pool = Pool(4)
        #self.__gui =  GUI.GUI()

    def getSelfInstance(self):
        return self

    def run(self):
        taskQueue = Queue()
        taskQueue.addTasks(params=self.__guiParams, pool={
                           "pool": self.__pool}, tasks=self.__guiParams.getTasks())

        taskQueue.run()

    def shutdown(self):
        self.__pool.shutdown()

    def cancel(self):
        pass
