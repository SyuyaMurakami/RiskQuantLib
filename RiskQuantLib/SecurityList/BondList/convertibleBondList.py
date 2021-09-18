#!/usr/bin/python
#coding = utf-8

import pandas as pd
from RiskQuantLib.SecurityList.BondList.bondList import bondList
from RiskQuantLib.Security.Bond.convertibleBond import convertibleBond
from RiskQuantLib.Set.SecurityList.BondList.convertibleBondList import setConvertibleBondList


class convertibleBondList(bondList,setConvertibleBondList):
    elementClass = convertibleBond
    def __init__(self):
        super(convertibleBondList, self).__init__()
        self.listType = 'Convertible Bond List'

    def addConvertibleBond(self, codeString, nameString, securityTypeString = 'Convertible Bond'):
        tmpList = self.all + [convertibleBond(codeString,nameString,securityTypeString)]
        self.setAll(tmpList)

    def addConvertibleBondSeries(self, convertibleBondCodeSeries, convertibleBondNameSeries, securityTypeString = 'Convertible Bond'):
        convertibleBondSeries = [convertibleBond(i,j,securityTypeString) for i,j in zip(convertibleBondCodeSeries,convertibleBondNameSeries)]
        tmpList = self.all + convertibleBondSeries
        self.setAll(tmpList)


