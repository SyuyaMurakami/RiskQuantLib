#!/usr/bin/python
#coding = utf-8
import numpy as np
from numbers import Integral

class iloc():
    def __init__(self,dataList):
        self.all = dataList

    def __getitem__(self, item):
        if np.isscalar(item):
            return self.all[item]
        elif isinstance(item, slice):
            is_integer_slice = any(
                isinstance(i, Integral) for i in (item.start, item.step, item.stop)
            )
            # Slicing with integer labels is always iloc based except for a
            # float indexer for some reason
            if is_integer_slice:
                return self.all[item]
            else:
                return []
