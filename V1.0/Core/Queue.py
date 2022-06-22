class Queue:
    def __init__(self,taskRegister,pool):
        self.__taskRegister = taskRegister
        self.__pool = pool

    def getTasksByName(taskReg, tasks):
        return dict([(i, taskReg[i]) for i in tasks if i in set(taskReg)])

    def graphParser(task, tasks, taskPrio):

        for secTask in tasks:
            if(task in set(tasks[secTask]["dependencies"])):
                taskPrio = Queue.graphParser(secTask, tasks, taskPrio)
        return taskPrio+1

    def getExecutionOrder(tasks):
        taskPrioritys = []

        taskNames = tasks.keys() #get task names
        if(len(tasks) > 1):
            for task in tasks:
                taskPrioritys.append(Queue.graphParser(task, tasks, 0)-1)

            [x for _, x in sorted(zip(taskPrioritys, taskNames))]
            return [task for _, task in sorted(zip(taskPrioritys, taskNames), reverse=True)]
        else:
            [x for _, x in sorted(zip([0], taskNames))]
            return [task for _, task in sorted(zip([0], taskNames), reverse=True)]

    def parseTasks(self, params, taskIdentifiers):
        tasks = Queue.getTasksByName(self.__taskRegister, taskIdentifiers)
        executionOrder = Queue.getExecutionOrder(tasks)
        
        for taskName in executionOrder:
            dependencies = tasks[taskName]["dependencies"]
            if(len(dependencies) == 0):
                dependencies = None
            else:
                dependencies = [dependency for dependency in dependencies if (dependencies[dependency] and dependency in set(tasks))]

            comp = [func(params) for func in tasks[taskName]["input_params"]]
            if(tasks[taskName]["MultiProcessing"]):
                comp.append(self.__pool)
            tasks[taskName]["input_params"] = comp
            tasks[taskName]["dependencies"] = dependencies
        return tasks, executionOrder

    def addTasks(self, params, tasks):
        self.__taskQueue = self.parseTasks(params, tasks)

    def run(self):
        tasks,taskExecutionOrder = self.__taskQueue
        
        for taskName in taskExecutionOrder:
            taskDependencies = {}
            #if task has dependencies on return values of other tasks, call run with these
            if(tasks[taskName]["dependencies"] != None):
                
                for func in tasks[taskName]["dependencies"]:
                    taskDependencies[func] = tasks[func]["return_val"]
                    
                #call handle of task 
                tasks[taskName]["return_val"] = tasks[taskName]["handle"](*tasks[taskName]["input_params"], taskDependencies)

            else:
               tasks[taskName]["return_val"] = tasks[taskName]["handle"](*tasks[taskName]["input_params"])
               
               