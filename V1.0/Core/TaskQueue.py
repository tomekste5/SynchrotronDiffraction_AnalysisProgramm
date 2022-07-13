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
        return dict([(i, dict(taskReg[i])) for i in taskNames if i in set(taskReg)])

    def graphParser(taskOfInterest, tasksToExecute, numberOfDependentTasks):
        """Return the number of tasks that are dependent of the taskOfInterest.
        Uses Recursion!

        Args:
            taskOfInterest (string): The task for which to search dependent tasks
            tasksToExecute (dictionary): dictionary with all tasks that need to be executed
            numberOfDependentTasks (int)

        Returns:
            int: how many tasks are dependent on taskOfInterest
        """
        for secTask in tasksToExecute: #Check for every task if it is dependent on the task of interest
            if(taskOfInterest in set(tasksToExecute[secTask]["dependencies"])):#if a task is found check how many tasks are dependent on that task and add the number to the numberOfDependentTasks of the taskOfInterest
                numberOfDependentTasks = TaskQueue.graphParser(secTask, tasksToExecute, numberOfDependentTasks)
        return numberOfDependentTasks+1

    def getExecutionOrder(tasksToExecute):
        """Returns tasks in an order where tasks that have the most tasks dependent on them are fist

        Args:
            tasksToExecute (dictionary): tasks to sort for execution order

        Returns:
            dictionary: A dictionary where the tasks are in right execution order
        """
        numberOfDependencys = []

        taskNames = tasksToExecute.keys() #get task names
        if(len(tasksToExecute) > 1):# if more than one task needs to be executed
            
            for task in tasksToExecute:#get for every task the numberOfDependentTasks
                numberOfDependencys.append(TaskQueue.graphParser(task, tasksToExecute, 0)-1)

            #sort the dictionary according to the numberOfDependentTasks (from HIGH to LOW) so that as much dependencies are fulfilled 
            [x for _, x in sorted(zip(numberOfDependencys, taskNames))]
            return [task for _, task in sorted(zip(numberOfDependencys, taskNames), reverse=True)]
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
        tasks = TaskQueue.getTasksByName(self.__taskRegister, taskNames) #select tasks that need to be executed from task register
        executionOrder = TaskQueue.getExecutionOrder(tasks) #get execution order
        
        for taskName in executionOrder:# for every task: check if multiprocessing core is needed, parse input parameters get number values instead of functions and remove dependencies that cant be fulfilled
            parsed_dependencies = tasks[taskName]["dependencies"]
            
            if(len(parsed_dependencies) == 0):
                parsed_dependencies = None
            else:
                parsed_dependencies = [dependency for dependency in parsed_dependencies if (parsed_dependencies[dependency] and dependency in set(tasks))]

            parsed_inputParams = [func(params) for func in tasks[taskName]["input_params"]]
            
            if(tasks[taskName]["MultiProcessing"]):
                parsed_inputParams.append(self.__pool)
                
            tasks[taskName]["input_params"] = parsed_inputParams
            tasks[taskName]["dependencies"] = parsed_dependencies
            
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
            if(tasks[taskName]["dependencies"] != None): #if Task has any dependencies that can be fulfilled
                
                for func in tasks[taskName]["dependencies"]: #collect return values of functions that were defined as dependencies and were executed as well
                    taskDependencies[func] = tasks[func]["return_val"]
                    
                #call handle of task 
                tasks[taskName]["return_val"] = tasks[taskName]["handle"](*tasks[taskName]["input_params"], taskDependencies) #call Task handle

            else:
               tasks[taskName]["return_val"] = tasks[taskName]["handle"](*tasks[taskName]["input_params"]) #call Task handle
        self.__taskQueue = []
               
               