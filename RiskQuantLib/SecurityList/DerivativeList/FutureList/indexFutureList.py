#!/usr/bin/python
#coding = utf-8

import pandas as pd
from RiskQuantLib.SecurityList.DerivativeList.FutureList.futureList import futureList
from RiskQuantLib.Security.Derivative.Future.indexFuture import indexFuture
from RiskQuantLib.Set.SecurityList.DerivativeList.FutureList.indexFutureList import setIndexFutureList


class indexFutureList(futureList,setIndexFutureList):
    def __init__(self):
        super(indexFutureList, self).__init__()
        self.listType = 'Index Future List'

    def addIndexFuture(self, codeString, nameString, securityTypeString = 'Index Future'):
        tmpList = self.all + [indexFuture(codeString,nameString,securityTypeString)]
        self.setAll(tmpList)

    def addIndexFutureSeries(self, indexFutureCodeSeries, indexFutureNameSeries, securityTypeString = 'Index Future'):
        indexFutureSeries = [indexFuture(i,j,securityTypeString) for i,j in zip(indexFutureCodeSeries,indexFutureNameSeries)]
        tmpList = self.all + indexFutureSeries
        self.setAll(tmpList)


