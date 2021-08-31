#!/usr/bin/python
#coding = utf-8
import os,sys,time
try:
    import pp
except Exception as e:
    command = r'''python '''+sys.path[0]+os.sep+'RiskQuantLib'+os.sep+'Tool'+os.sep+'pp-1.6.5'+os.sep+'setup.py install'
    os.popen(command)
    import pp

def parallelComputing(functionPointer,inputIterationList:list,functionDependencyTuple:tuple,libraryDependencyTuple:tuple,serverSecret:str = "123456"):
    """
    Call a function by multiple processes. Each process can accept a different input.

    Parameters
    ----------
    functionPointer : function
        The function name.
    inputIterationList : list
        A list holding inputs. Each element is a input for single process.
    functionDependencyTuple : tuple
        A tuple of string, telling the dependency of function.
    libraryDependencyTuple : tuple
        A tuple of string, telling the dependency of library.
    serverSecret: str
        A string used to communicate with in two computers.

    Returns
    -------
    resultDict : dict
        A dict whose key is input and value is the return of function.
    """
    ppservers = ()
    if len(sys.argv) >1:
        ncpus = int(sys.argv[1])
        jobServer = pp.Server(ncpus,ppservers = ppservers,secret=serverSecret)
    else:
        jobServer = pp.Server(ppservers=ppservers, secret=serverSecret)
    print("pp available cores：",jobServer.get_ncpus(),"workers")
    startTime = time.time()
    resultDict = {}
    result = [(input,jobServer.submit(functionPointer,(input,),functionDependencyTuple,libraryDependencyTuple)) for input in inputIterationList]
    for input,job in result:
        resultDict[input] = job()
    print("Time Consumed:",time.time()-startTime,"s")
    jobServer.print_stats()
    return resultDict

















