#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.IndexList.base import baseList
from RiskQuantLib.Index.BondIndex.bondIndex import bondIndex
from RiskQuantLib.Set.IndexList.BondIndexList.bondIndexList import setBondIndexList

class bondIndexList(baseList,setBondIndexList):
    """
    This class is the list of bond index.
    """
    def __init__(self):
        super(bondIndexList, self).__init__()
        self.listType = 'Bond Index List'

    def addBondIndex(self, codeString:str, nameString:str, securityTypeString:str = 'Bond Index'):
        """
        Add a bond index object into this list.
        """
        tmpList = self.all + [bondIndex(codeString,nameString,securityTypeString)]
        self.setAll(tmpList)

    def addBondIndexSeries(self, indexCodeSeries, indexNameSeries, securityTypeString = 'Bond Index'):
        """
        Add bundles of bond index into this list.
        """
        bondSeries = [bondIndex(i,j,securityTypeString) for i,j in zip(indexCodeSeries,indexNameSeries)]
        tmpList = self.all + bondSeries
        self.setAll(tmpList)


