#!/usr/bin/python
#coding = utf-8
import os,sys,time
try:
    import pp
except Exception as e:
    command = r'''python '''+sys.path[0]+os.sep+'RiskQuantLib'+os.sep+'Tool'+os.sep+'pp-1.6.5'+os.sep+'setup.py install'
    os.popen(command)
    import pp

def parallelComputing(functionPointer,inputIterationList,functionDependencyTuple,libraryDependencyTuple,serverSecret = "123456"):
    # 初始化服务器
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

















