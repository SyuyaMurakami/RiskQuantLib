#!/usr/bin/python
#coding = utf-8
import numpy as np
from numbers import Integral

class loc():
    def __init__(self,dataList):
        self.all = dataList

    def __getitem__(self, item):
        if type(item) == type(''):
            return [i for i in self.all if hasattr(i, 'index') and i.index == item][0]
        else:
            try:
                return [[j for j in self.all if hasattr(j, 'index') and j.index == i][0] for i in item]
            except:
                return []
