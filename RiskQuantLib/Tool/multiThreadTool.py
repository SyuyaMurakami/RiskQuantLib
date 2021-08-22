#!/usr/bin/python
#coding = utf-8

import threading

exitFlag = 0

class functionMultiThread(threading.Thread):
    def __init__(self,threadID,name,q,function):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
        self.function = function

    def run(self):
        print("Starting "+self.name)
        self.function()
        print("Exiting "+self.name)

def multiThread(functionList):
    threadLock = threading.Lock()
    threadList = [functionMultiThread(i,str(i),i,functionList[i]) for i in range(len(functionList))]
    [i.start() for i in threadList]
    [i.join() for i in threadList]
    return 0














