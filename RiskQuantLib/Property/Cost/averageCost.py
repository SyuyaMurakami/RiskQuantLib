#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Property.Cost.cost import cost
from RiskQuantLib.Property.average import average
import numpy as np

class averageCost(cost,average):
    def __init__(self,value,unit = 'RMB',numberOfSamplesNum = np.nan):
        cost.__init__(self, value, unit)
        average.__init__(self, numberOfSamplesNum)



