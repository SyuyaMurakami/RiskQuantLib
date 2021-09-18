#!/usr/bin/python
#coding = utf-8

import pandas as pd
from RiskQuantLib.SecurityList.base import baseList
from RiskQuantLib.Security.Derivative.derivative import derivative
from RiskQuantLib.Set.SecurityList.DerivativeList.derivativeList import setDerivativeList


class derivativeList(baseList,setDerivativeList):
    """
    derivativeList is one of the five basic list classes.
    """
    elementClass = derivative
    def __init__(self):
        super(derivativeList, self).__init__()
        self.listType = 'Derivative List'

    def addDerivative(self, codeString, nameString, securityTypeString = 'Derivative'):
        tmpList = self.all+[derivative(codeString,nameString,securityTypeString)]
        self.setAll(tmpList)

    def addDerivativeSeries(self, derivativeCodeSeries, derivativeNameSeries, securityTypeString = 'Derivative'):
        derivativeSeries = [derivative(i,j,securityTypeString) for i,j in zip(derivativeCodeSeries,derivativeNameSeries)]
        tmpList = self.all + derivativeSeries
        self.setAll(tmpList)


