#!/usr/bin/python
#coding = utf-8

import pandas as pd
from RiskQuantLib.SecurityList.base import baseList
from RiskQuantLib.Security.Bond.bond import bond
from RiskQuantLib.Set.SecurityList.BondList.bondList import setBondList


class bondList(baseList,setBondList):
    """
    bondList is one of the five basic list classes.
    """
    def __init__(self):
        super(bondList, self).__init__()
        self.listType = 'Bond List'

    def addBond(self, codeString, nameString, securityTypeString = 'Bond'):
        tmpList = self.all + [bond(codeString,nameString,securityTypeString)]
        self.setAll(tmpList)

    def addBondSeries(self, bondCodeSeries, bondNameSeries, securityTypeString = 'Bond'):
        bondSeries = [bond(i,j,securityTypeString) for i,j in zip(bondCodeSeries,bondNameSeries)]
        tmpList = self.all + bondSeries
        self.setAll(tmpList)


