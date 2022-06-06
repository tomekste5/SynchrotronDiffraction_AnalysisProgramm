from multiprocessing import Process
import multiprocessing as mp
from queue import Empty
import logging
from socket import timeout
from matplotlib.pyplot import flag

from sympy import true

import multiprocessing.managers as managers

import multiprocessing.managers
"""
def AutoProxy(token, serializer, manager=None, authkey=None,
              exposed=None, incref=True, manager_owned=False):
    '''
    Return an auto-proxy for `token`
    '''
    _Client = multiprocessing.managers.listener_client[serializer][1]

    if exposed is None:
        conn = _Client(token.address, authkey=authkey)
        try:
            exposed = dispatch(conn, None, 'get_methods', (token,))
        finally:
            conn.close()

    if authkey is None and manager is not None:
        authkey = manager._authkey
    if authkey is None:
        authkey = multiprocessing.process.current_process().authkey

    ProxyType = multiprocessing.managers.MakeProxyType('AutoProxy[%s]' % token.typeid, exposed)
    proxy = ProxyType(token, serializer, manager=manager, authkey=authkey,
                      incref=incref, manager_owned=manager_owned)
    proxy._isauto = True
    return proxy

multiprocessing.managers.AutoProxy = AutoProxy
"""
class Pool():
    def __init__(self,numberOfProcesses):
        self.__manager = mp.Manager()
        self.__logger = mp.log_to_stderr()
        
        self.__logger.setLevel(logging.INFO)
        self.__mainQueue = self.__manager.Queue()
        self.__queues = []
        self__flag = true                  
                
        self.__workerProcesses = [] 
        for i in range(0,numberOfProcesses):
            workerP = Process(target=Pool.runTasks, args = (self,self.__mainQueue,self__flag))
            workerP.daemon = True
            self.__workerProcesses.append(workerP)
            
    #[taskMethod,logger, [inputvar]]
    def addTask(self, task):
        self.__queues.append(task[1][0])
        self.__mainQueue.put([len(self.__queues),task[0],task[1][1]])
    def getManager(self):
        return self.__manager
    def runTasks(self,mainQueue,flag):
        while (flag):
            queueId,doTask, inputVar = mainQueue.get()
            doTask(self.__queues[queueId],inputVar)
                
    def getNewQueue(self):
        return self.__manager.Queue()
    
    def changeLoggingLevel(self,level):
        return self.__logger.setLevel(level)
    def start(self):
        for workerP in self.__workerProcesses:
            workerP.start()
    def getLogger(self):
        return self.__logger
                
        