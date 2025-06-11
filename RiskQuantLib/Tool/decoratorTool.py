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

class confirmer:
    """
    This is a decorator which will require confirmation before calling the wrapped function.
    If this decorator is passed a notice, it will print it before require confirmation.
    """
    def __init__(self, prefix='This Is An Action That Can NOT Be Cancelled, Input Y/y To Confirm Or N/n To Deny:'):
        self.prefix = prefix

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            confirm = input(self.prefix)
            if confirm.lower() == 'y':
                print('Action Confirmed, Processing On-going')
                result = func(*args, **kwargs)
                return result
            else:
                print('Action Denied, Nothing Changed')
                return None
        return wrapper