#!/usr/bin/python
#coding = utf-8

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Callable, Tuple, Any, Optional

#<import>
#</import>


def multiThread(functionList: List[Callable], argsList: List[Tuple] = None, kwargsList: List[Dict] = None, workerNumber: Optional[int] = None) -> List[Any]:
    """
    Run callables by multi-thread. It will pass the first element of argList as parameter of the first function, pass
    the second element of argList as parameter of the second function, etc. It returns a list of results.

    Parameters
    ----------
    functionList : List[Callable]
        A list of callables.
    argsList : List[Tuple]
        A list of parameters, like [(arg1, arg2), (arg3,)]
    kwargsList : List[Dict]
        A list of parameters, like [{argName1:argValue1, argName2:argValue2}, {argName3:argValue3}]
    workerNumber : Optional[int]
        Max number of core used.

    Returns
    -------
    List[Any]
        The results of every function.
    """
    numberThread = len(functionList)
    argsList = [tuple() for _ in range(numberThread)] if argsList is None else argsList
    kwargsList = [dict() for _ in range(numberThread)] if kwargsList is None else kwargsList
    assert numberThread == len(argsList) == len(kwargsList)
    results = [None for _ in range(numberThread)]

    with ThreadPoolExecutor(max_workers=workerNumber) as executor:
        futureDict = {executor.submit(func, *args, **kwargs): i for i, (func, args, kwargs) in enumerate(zip(functionList, argsList, kwargsList))}
        for future in as_completed(futureDict):
            index = futureDict[future]
            try:
                results[index] = future.result()
            except Exception as e:
                results[index] = e
                print(f"Task at index {index} ({functionList[index].__name__}) failed with error: {e}")

    return results

#<threadTool>
#</threadTool>












