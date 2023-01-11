#!/usr/bin/python
#coding = utf-8

import threading
#<import>
#</import>

exitFlag = 0

class functionMultiThread(threading.Thread):
    """
    This class is used to create multiple threads.
    """
    def __init__(self,threadID:str,name:str,q,function):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
        self.function = function

    def run(self):
        print("Starting "+self.name)
        self.function()
        print("Exiting "+self.name)

    #<functionMultiThread>
    #</functionMultiThread>

def multiThread(functionList:list):
    """
    This function will run all functions in the given functionList by multiple threads.

    Parameters
    ----------
    functionList : list
        A list holding all functions you want to run.
    """
    threadLock = threading.Lock()
    threadList = [functionMultiThread(i,str(i),i,functionList[i]) for i in range(len(functionList))]
    [i.start() for i in threadList]
    [i.join() for i in threadList]
    return 0

#<multiThreadTool>
#</multiThreadTool>












