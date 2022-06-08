from multiprocessing import Process
import multiprocessing as mp
from queue import Empty
import logging
from logging.handlers import RotatingFileHandler
from socket import timeout
from matplotlib.pyplot import flag

from sympy import true

import multiprocessing.managers as managers
import sys

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
            workerP = Process(target=Pool.runTasks, args = (self.__mainQueue,self.__killEvent,self.__idle))
            workerP.daemon = True
            workerP.start()
            self.__workerProcesses.append(workerP)
        
    def addTask(self, task):
        self.__mainQueue.put([task[0],task[1]])
    def getManager(self):
        return self.__manager
    def runTasks(mainQueue,killEvent,idle):
        #logger = mp.log_to_stderr()
        
        while (not killEvent.is_set()):
            try:
                taskFunc,data = mainQueue.get_nowait()
                taskFunc(data)
            except Empty:
                while(idle.is_set()):
                    #logger.info("Idling...")
                    pass
                
    def getQueue(self):
        return self.__mainQueue
    
    def changeLoggingLevel(self,level):
        return self.__rootLogger.setLevel(level)
    def startWorkers(self):
        pass
    def getLogger(self):
        return self.__rootLogger
    def idle(self):
        self.__idle.set()
    def start(self):
        self.__idle.clear()
        self.__mainQueue.join()        
        