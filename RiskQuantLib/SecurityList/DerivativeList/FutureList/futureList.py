#!/usr/bin/python
#coding = utf-8

import pandas as pd
from RiskQuantLib.SecurityList.DerivativeList.derivativeList import derivativeList
from RiskQuantLib.Security.Derivative.Future.future import future
from RiskQuantLib.Set.SecurityList.DerivativeList.FutureList.futureList import setFutureList


class futureList(derivativeList,setFutureList):
    def __init__(self):
        super(futureList, self).__init__()
        self.listType = 'Future List'

    def addFuture(self, codeString, nameString, securityTypeString = 'Future'):
        tmpList = self.all+[future(codeString,nameString,securityTypeString)]
        self.setAll(tmpList)

    def addFutureSeries(self, futureCodeSeries, futureNameSeries, securityTypeString = 'Future'):
        futureSeries = [future(i,j,securityTypeString) for i,j in zip(futureCodeSeries,futureNameSeries)]
        tmpList = self.all + futureSeries
        self.setAll(tmpList)


