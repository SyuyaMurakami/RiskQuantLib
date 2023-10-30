import time
import pandas as pd

class timer:
    """
    This is a decorator which will count the time of a single function call.
    If this decorator is passed a prefix, it will print it along with running time of decorated function.
    """
    def __init__(self, prefix='None'):
        self.prefix = prefix

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            print("Function Hint: {} ; Run Time: {} sec ; Finished At: {}".format(self.prefix, round(time.time() - start,2), pd.Timestamp.today()))
            return result
        return wrapper
