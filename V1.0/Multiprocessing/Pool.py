from multiprocessing import Process
import multiprocessing as mp
from queue import Empty
import logging
from logging.handlers import RotatingFileHandler

fileHandlerPref = RotatingFileHandler
filename = "Logs/Core.log"
format = '[%(levelname)s/%(processName)s] %(asctime)s %(filename)s %(message)s'

#format = '[%(levelname)s/%(processName)s] %(message)s'

class Pool():
    """A multiprocessing pool which can be used by any Task as long the job can be processed by calling one function.
    If that is given  different jobs have to be put in the mainQueue by poolInstance.getQueue(self).put([functionTOcall,[callParameters]])
    If a Task requires a object to be present in the forked interpreters and not via a proxy the reinitialize() function has to be used
    
    The pool uses the multiprocessing Library for further information on Queues,Managers etc. see https://docs.python.org/3/library/multiprocessing.html
    For more information about logging see: https://docs.python.org/3/howto/logging.html
    """

    def __init__(self,numberOfProcesses):
        """Initializes the multiprocessing.manager, logger and start the processes

        Args:
            numberOfProcesses (int): how much processes should be started
        """
        self.__rootLogger = mp.log_to_stderr()
        self.__rootLogger.setLevel(logging.INFO)
        self.__manager = mp.Manager()
        self.__killEvent = self.__manager.Event()
        self.__idle = self.__manager.Event()
        self.__mainQueue =   self.__manager.Queue() 
                    
    
        self.__workerProcesses = [] 
        
        self.__killEvent.clear()
        self.__idle.set()
        for i in range(0,numberOfProcesses):
            workerP = Process(target=Pool.run, args = (self.__mainQueue,self.__killEvent,self.__idle,[]))
            workerP.daemon = True
            workerP.start()
            self.__workerProcesses.append(workerP)
            
            
    def reinitialize(self,objectsToPickle,numberOfProcesses):
        """kills all processes then starts <numberOfProcesses> processes with  the objects in objectsToPickle.

        Args:
            objectsToPickle (list): list of objects that have to be pickled in the forked interpreters
            numberOfProcesses (int): how much processes to start
        """
        self.__killEvent.set()
        self.__idle.set()
        #wait for all processes to die
        while(all([process.is_alive() for process in self.__workerProcesses]) and len(self.__workerProcesses) != 0):
            pass
        self.__workerProcesses.clear()
        self.__killEvent.clear()
        for i in range(0,numberOfProcesses):
            workerP = Process(target=Pool.run, args = (self.__mainQueue,self.__killEvent,self.__idle,objectsToPickle))
            workerP.daemon = True
            workerP.start()
            self.__workerProcesses.append(workerP)
        
    def run(mainQueue,killEvent,idle,pickledItems):
        """Function that gets called by the processes. When the mainQueue is filled with jobs in
        the following structure:
        [functionHandle, callParams]
        Processes when not set to idle  will then call functionHandle(callParams) until they get killed or the Queue is Empty
        

        Args:
            mainQueue (Multiprocessing.Queue): A Queue
            killEvent (Multiprocessing.Event): When set Processes will exit run() and exit
            idle (Multiprocessing.Event): When set Processes wont start processing jobs in mainQueue
            pickledItems (list): a list of pickled items that need to be passed to the job function
        """
        #logger = mp.log_to_stderr()
        
        while (not killEvent.is_set()):
            try:
                taskFunc,data = mainQueue.get(timeout=0.01)
                data.extend(pickledItems)
                taskFunc(data)
            except Empty:
                while(idle.is_set() and not killEvent.is_set()):
                    #logger.info("Idling...")
                    pass
    
    
    def idle(self):
        """Sets idle event
        """
        self.__idle.set()
    def start(self):
        """Clears idle event resulting in processes start processing jobs in the mainQueue
        """
        self.__idle.clear()   
    def shutdown(self):
        """Sets kill Event and waits for all processes to exit
        """
        self.__killEvent.set()
        for wP in self.__workerProcesses:
            wP.join()
        self.__rootLogger.info("Shutting down...")
        
    
    def getManager(self):
        """returns Manager

        Returns:
            multiprocessing.Manager: A Manager
        """
        return self.__manager
    
    def getQueue(self):
        """Returns main Queue

        Returns:
            multiprocessing.Queue: returns the mainQueue
        """
        return self.__mainQueue
    
    def getLogger(self):
        """Return the logger

        Returns:
            logging.logger: returns the logger
        """
        return self.__rootLogger
    
    def changeLoggingLevel(self,level):
        """changes the logging/filter level of the logger
        There are:
        INFO
        WARNING
        ERROR

        Args:
            level (int): filter level of logger

        Returns:
            logging.Logger: logger with changed logging level
        """
        return self.__rootLogger.setLevel(level)

        