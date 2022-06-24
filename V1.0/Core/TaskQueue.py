class TaskQueue:
    def __init__(self,taskRegister,pool):
        """Initializes TaskQueue instance

        Args:
            taskRegister (dictionary): A Dictionary filled with information how to execute Tasks. For further Explanation see documentation or TaskRegister Module
            pool (Multiprocessing.Pool.Pool): Multiprocessing pool
        """
        self.__taskRegister = taskRegister
        self.__pool = pool

    def getTasksByName(taskReg, taskNames):
        """Returns subdictionary of TaskRegister for every task that matches with a name in taskNames. 

        Args:
            taskReg (dictionary): the TaskRegister
            taskNames (list): list of task names that will be searched in TaskRegister

        Returns:
            dictionary: A dictionary of all subdictionary of the tasks that matched a with one of the passed taskNames 
        """
        return dict([(i, taskReg[i]) for i in taskNames if i in set(taskReg)])

    def graphParser(taskOfInterest, tasks, taskPrio):
        """Return the number of tasks that are dependent of the taskOfInterest.
        Uses Recursion!

        Args:
            taskOfInterest (string): _description_
            tasks (dictionary): _description_
            taskPrio (int): _description_

        Returns:
            int: how many tasks are dependent on taskOfInterest
        """
        for secTask in tasks:
            if(taskOfInterest in set(tasks[secTask]["dependencies"])):
                taskPrio = TaskQueue.graphParser(secTask, tasks, taskPrio)
        return taskPrio+1

    def getExecutionOrder(tasks):
        """Returns tasks in an order where tasks that have the most tasks dependent on them are fist

        Args:
            tasks (dictionary): tasks to sort

        Returns:
            dictionary: A dictionary where the tasks are in right execution order
        """
        taskPrioritys = []

        taskNames = tasks.keys() #get task names
        if(len(tasks) > 1):
            for task in tasks:
                taskPrioritys.append(TaskQueue.graphParser(task, tasks, 0)-1)

            [x for _, x in sorted(zip(taskPrioritys, taskNames))]
            return [task for _, task in sorted(zip(taskPrioritys, taskNames), reverse=True)]
        else:
            [x for _, x in sorted(zip([0], taskNames))]
            return [task for _, task in sorted(zip([0], taskNames), reverse=True)]

    def parseTasks(self, params, taskNames):
        """Prepares the input data for  tasks function handle calls for tasks that were selected in the GUI.

        Args:
            params (Utils.Param.Param): A object that hols the parameters the were entered in the GUI
            taskNames (string): taskNames of tasks that were selected in the GUI

        Returns:
            dictionary: dictionary of tasks where the input is parsed
            dictionary: execution order
        """
        tasks = TaskQueue.getTasksByName(self.__taskRegister, taskNames)
        executionOrder = TaskQueue.getExecutionOrder(tasks)
        
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

    def addTasks(self, params, taskNames):
        """parses the tasks then stores them in the internal taskQueue variable

        Args:
            params (Utils.Param.Param): A object that hols the parameters the were entered in the GUI
            taskNames (string): taskNames of tasks that were selected in the GUI
        """
        self.__taskQueue = self.parseTasks(params, taskNames)

    def run(self):
        """When called it begins to execute the tasks in the taskQueue by calling there handles with the parsed input.
        """
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
               
               