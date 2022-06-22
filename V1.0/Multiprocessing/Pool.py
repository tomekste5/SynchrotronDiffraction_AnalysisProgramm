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
    def __init__(self,numberOfProcesses):
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
            
            
    def reinitialize(self,itemsToPickle,numberOfProcesses):
        self.__killEvent.set()
        self.__idle.set()
        #wait for all processes to die
        while(all([process.is_alive() for process in self.__workerProcesses]) and len(self.__workerProcesses) != 0):
            pass
        self.__workerProcesses.clear()
        self.__killEvent.clear()
        for i in range(0,numberOfProcesses):
            workerP = Process(target=Pool.run, args = (self.__mainQueue,self.__killEvent,self.__idle,itemsToPickle))
            workerP.daemon = True
            workerP.start()
            self.__workerProcesses.append(workerP)
        
    def run(mainQueue,killEvent,idle,pickledItems):
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
        self.__idle.set()
    def start(self):
        self.__idle.clear()   
    def shutdown(self):
        self.__killEvent.set()
        for wP in self.__workerProcesses:
            wP.join()
        self.__rootLogger.info("Shutting down...")
        
    
    def getManager(self):
        return self.__manager
    
    def getQueue(self):
        return self.__mainQueue
    
    def getLogger(self):
        return self.__rootLogger
    
    def changeLoggingLevel(self,level):
        return self.__rootLogger.setLevel(level)

        