#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Property.MarketValue.marketValue import marketValue
from RiskQuantLib.Property.average import average
import numpy as np

class averageMarketValue(marketValue,average):
    def __init__(self,value,unit = 'RMB',numberOfSamplesNum = np.nan):
        marketValue.__init__(self, value, unit)
        average.__init__(self, numberOfSamplesNum)



