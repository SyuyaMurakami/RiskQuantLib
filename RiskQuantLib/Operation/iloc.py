#!/usr/bin/python
#coding = utf-8
import numpy as np
from numbers import Integral

class iloc():
    """
    This class is the function class for RiskQuantLib list to use iloc function. It's similar to
    that in pandas. Use it by calling stockList.iloc[number]. It returns the number-th element in
    that list.
    """
    def __init__(self,dataList:list):
        """
        Passing a list to initialize iloc object.
        """
        self.all = dataList

    def __getitem__(self, item):
        """
        Return the item-th element. If item is a Slice object, return a list collection of elements.
        """
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
