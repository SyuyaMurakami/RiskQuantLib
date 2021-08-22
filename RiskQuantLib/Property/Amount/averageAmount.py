#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Property.Amount.amount import amount
from RiskQuantLib.Property.average import average
import numpy as np

class averageAmount(amount, average):
    def __init__(self, value, numberOfSamplesNum = np.nan):
        amount.__init__(self, value)
        average.__init__(self, numberOfSamplesNum)



