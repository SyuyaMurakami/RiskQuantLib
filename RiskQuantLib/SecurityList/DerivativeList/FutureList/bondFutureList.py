#!/usr/bin/python
#coding = utf-8

import pandas as pd
from RiskQuantLib.SecurityList.DerivativeList.FutureList.futureList import futureList
from RiskQuantLib.Security.Derivative.Future.bondFuture import bondFuture
from RiskQuantLib.Set.SecurityList.DerivativeList.FutureList.bondFutureList import setBondFutureList


class bondFutureList(futureList,setBondFutureList):
    def __init__(self):
        super(bondFutureList, self).__init__()
        self.listType = 'Bond Future List'

    def addBondFuture(self, codeString, nameString, securityTypeString = 'Bond Future'):
        tmpList = self.all + [bondFuture(codeString,nameString,securityTypeString)]
        self.setAll(tmpList)

    def addBondFutureSeries(self, bondFutureCodeSeries, bondFutureNameSeries, securityTypeString = 'Bond Future'):
        bondFutureSeries = [bondFuture(i,j,securityTypeString) for i,j in zip(bondFutureCodeSeries,bondFutureNameSeries)]
        tmpList = self.all + bondFutureSeries
        self.setAll(tmpList)


