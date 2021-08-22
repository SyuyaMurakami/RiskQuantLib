#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.IndexList.base import base
from RiskQuantLib.Index.BondIndex.bondIndex import bondIndex
from RiskQuantLib.Set.IndexList.BondIndexList.bondIndexList import setBondIndexList

class bondIndexList(base,setBondIndexList):
    def __init__(self):
        super(bondIndexList, self).__init__()
        self.listType = 'Bond Index List'

    def addBondIndex(self, codeString, nameString, securityTypeString = 'Bond Index'):
        tmpList = self.all + [bondIndex(codeString,nameString,securityTypeString)]
        self.setAll(tmpList)

    def addBondIndexSeries(self, indexCodeSeries, indexNameSeries, securityTypeString = 'Bond Index'):
        bondSeries = [bondIndex(i,j,securityTypeString) for i,j in zip(indexCodeSeries,indexNameSeries)]
        tmpList = self.all + bondSeries
        self.setAll(tmpList)


