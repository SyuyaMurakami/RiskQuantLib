#!/usr/bin/python
#coding = utf-8
import numpy as np
from numbers import Integral
#<import>
#</import>

class loc():
    """
    This class is the function class for RiskQuantLib list to use loc function. It's similar to
    that in pandas. Use it by calling stockList.loc[index]. It returns the element in
    that list whose index equals given value.
    """
    #<init>
    def __init__(self,dataList:list):
        """
        Passing a list to initialize loc object.
        """
        self.all = dataList
    #</init>

    #<getitem>
    def __getitem__(self, item):
        """
        Return the element whose index equals given value. If item is a Slice object, return a list
        collection of elements.
        """
        if type(item) == type(''):
            return [i for i in self.all if hasattr(i, 'index') and i.index == item][0]
        else:
            try:
                return [[j for j in self.all if hasattr(j, 'index') and j.index == i][0] for i in item]
            except:
                return []
    #</getitem>
    #<loc>
    #</loc>