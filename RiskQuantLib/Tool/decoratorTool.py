#!/usr/bin/python
#coding = utf-8

import time
import inspect
import numpy as np
import pandas as pd
from functools import wraps
from typing import Optional, Sequence, Callable, Any, List, TypeVar

#<import>
#</import>

F = TypeVar('F', bound=Callable[..., Any])

class timer(object):
    """
    This is a decorator which will count the time of a single function call.
    If this decorator is passed a prefix, it will print it along with running time of decorated function.
    """
    def __init__(self, prefix: str='None'):
        self.prefix = prefix

    def __call__(self, func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start = time.time()
            result = func(*args, **kwargs)
            print("Function Hint: {} ; Run Time: {} sec ; Finished At: {}".format(self.prefix, round(time.time() - start,2), pd.Timestamp.today()))
            return result
        return wrapper

    #<timer>
    #</timer>

class confirmer(object):
    """
    This is a decorator which will require confirmation before calling the wrapped function.
    If this decorator is passed a notice, it will print it before require confirmation.
    """
    def __init__(self, prefix: str='This Is An Action That Can NOT Be Cancelled, Input Y/y To Confirm Or N/n To Deny:'):
        self.prefix = prefix

    def __call__(self, func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            confirm = input(self.prefix)
            if confirm.lower() == 'y':
                print('Action Confirmed, Processing On-going')
                result = func(*args, **kwargs)
                return result
            else:
                print('Action Denied, Nothing Changed')
                return None
        return wrapper

    #<confirmer>
    #</confirmer>

class checker(object):
    """
    This is a decorator which will check every parameter what is passed into a function. By default,
    this decorator does nothing.
    """
    def __init__(self, argIndexList: Optional[List[int]] = None, argKeyList: Optional[List[str]] = None, argIterableIndexList: Optional[List[int]] = None, argIterableKeyList: Optional[List[str]] = None):
        self.argIndexSet = set(argIndexList) if argIndexList else {}
        self.argKeySet = set(argKeyList) if argKeyList else {}
        self.argIterableIndexSet = set(argIterableIndexList) if argIterableIndexList else {}
        self.argIterableKeySet = set(argIterableKeyList) if argIterableKeyList else {}

    def __call__(self, func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            return func(*args, **kwargs)
        return wrapper

    #<checker>
    #</checker>

class stringTimestampConverter(checker):
    """
    This is a decorator which will try to convert string into pandas.Timestamp.
    It is used when a function require a pandas.Timestamp parameter, after decorated by this, it
    allows to pass a string into parameter.

    If a function is typed as func(x: pandas.Timestamp, y: pandas.Timestamp, z: List[pandas.Timestamp], m: List[pandas.Timestamp]),
    then you can decorate it by @stringTimestampConverter(argIndexList=[0,1], argKeyList=['x','y'], argIterableIndexList=[2,3], argIterableKeyList=['z','m'])
    """
    @staticmethod
    def convertStrToTimestamp(arg: Optional[Any] = None):
        return pd.Timestamp(arg) if isinstance(arg, str) else arg

    @staticmethod
    def convertStrListToTimestampList(arg: Optional[Sequence] = None):
        return [stringTimestampConverter.convertStrToTimestamp(a) for a in arg] if arg else arg

    def __call__(self, func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            argsNew = [stringTimestampConverter.convertStrToTimestamp(arg) if idx in self.argIndexSet else stringTimestampConverter.convertStrListToTimestampList(arg) if idx in self.argIterableIndexSet else arg for idx,arg in enumerate(args)]
            kwargsNew = {k: (stringTimestampConverter.convertStrToTimestamp(kwargs[k]) if k in self.argKeySet else stringTimestampConverter.convertStrListToTimestampList(kwargs[k]) if k in self.argIterableKeySet else kwargs[k]) for k in kwargs}
            return func(*argsNew, **kwargsNew)
        return wrapper

    #<stringTimestampConverter>
    #</stringTimestampConverter>

class valueAsserter(checker):
    """
    This is a decorator which will assert that some parameter must have certain values. If passed
    with other values, exception will be raised. If a parameter is an iterable, then check every element.

    If you want to require the value of the second parameter of a function into 1 or 2, all other values should be invalid,
    then decorate it by @valueAsserter(argIndexList=[1],value={1,2}).
    """
    @staticmethod
    def assertValue(arg: Optional[Any] = None, value: Optional[set] = None, argName: Optional[str] = None, funcName: Optional[str] = None):
        validated = (arg in value) if value else True
        if not validated:
            raise ValueError(f"Parameter '{argName}' in function '{funcName}' has an invalid value: '{arg}'. Allowed values are: {value}")

    @staticmethod
    def assertValueList(arg: Optional[Sequence] = None, value: Optional[set] = None, argName: Optional[str] = None, funcName: Optional[str] = None):
        validated = np.all([i in value for i in arg]) if arg and value else True
        if not validated:
            raise ValueError(f"Parameter '{argName}' in function '{funcName}' has at least an invalid value in its element: '{arg}'. Allowed values of element are: {value}")

    def __init__(self, argIndexList: Optional[List[int]] = None, argKeyList: Optional[List[str]] = None, argIterableIndexList: Optional[List[int]] = None, argIterableKeyList: Optional[List[str]] = None, value: Optional[set] = None):
        super(valueAsserter, self).__init__(argIndexList=argIndexList, argKeyList=argKeyList, argIterableIndexList=argIterableIndexList, argIterableKeyList=argIterableKeyList)
        self.value = value

    def __call__(self, func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            funcName = func.__name__
            argNameList = list(inspect.signature(func).parameters.keys())
            [valueAsserter.assertValue(arg, self.value, argNameList[idx], funcName) if idx in self.argIndexSet else valueAsserter.assertValueList(arg, self.value, argNameList[idx], funcName) if idx in self.argIterableIndexSet else None for idx,arg in enumerate(args)]
            [(valueAsserter.assertValue(kwargs[k], self.value, k, funcName) if k in self.argKeySet else valueAsserter.assertValueList(kwargs[k], self.value, k, funcName) if k in self.argIterableKeySet else None) for k in kwargs]
            return func(*args, **kwargs)
        return wrapper

    #<valueAsserter>
    #</valueAsserter>

class freezer(object):
    """
    This is a decorator which will freeze all parameters except the first one.

    If you have a function typed as func(x, y, z, m), you can convert it into a single-parameter function by passing y, z, m into
    it before x is determined. You can do this by @freezer(y=1, z=2, m=3), then just call func(43), it will be totally the same
    as func(x=43, y=1, z=2, m=3)
    """
    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs

    def __call__(self, func: F) -> F:
        @wraps(func)
        def wrapper(argFirst) -> Any:
            return func(argFirst, *self.args, **self.kwargs)
        return wrapper

    #<freezer>
    #</freezer>

#<decoratorTool>
#</decoratorTool>
