#!/usr/bin/python
#coding = utf-8
import numpy as np
from RiskQuantLib.SecurityList.BondList.bondList import bondList
from RiskQuantLib.Security.Bond.bondIndexUnderlyingBond import bondIndexUnderlyingBond
from RiskQuantLib.Set.SecurityList.BondList.bondIndexUnderlyingBondList import setBondIndexUnderlyingBondList

class bondIndexUnderlyingBondList(bondList,setBondIndexUnderlyingBondList):
    def __init__(self):
        super(bondIndexUnderlyingBondList,self).__init__()
        self.listType = 'Bond Index Underlying Bond List'

    def addBond(self, codeString, nameString, weightNum = np.nan, securityTypeString = 'Bond Index Underlying Bond'):
        underlyingBond = bondIndexUnderlyingBond(codeString,nameString,securityTypeString)
        underlyingBond.setWeight(weightNum)
        tmpList = self.all + [underlyingBond]
        self.setAll(tmpList)

    def addBondSeries(self, bondCodeSeries, bondNameSeries, bondWeightSeries = np.nan, securityTypeString = 'Bond Index Underlying Bond'):
        bondSeries = [bondIndexUnderlyingBond(i,j,securityTypeString) for i,j in zip(bondCodeSeries,bondNameSeries)]
        if not (type(bondWeightSeries)==type(np.nan) and np.isnan(bondWeightSeries)):
            [i.setWeight(j) for i,j in zip(bondSeries,bondWeightSeries)]
        tmpList = self.all + bondSeries
        self.setAll(tmpList)






