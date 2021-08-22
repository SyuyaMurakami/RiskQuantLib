#!/usr/bin/python
#coding = utf-8


from RiskQuantLib.IndexList.base import base
from RiskQuantLib.Index.StockIndex.stockIndex import stockIndex
from RiskQuantLib.Set.IndexList.StockIndexList.stockIndexList import setStockIndexList

class stockIndexList(base,setStockIndexList):
    def __init__(self):
        super(stockIndexList, self).__init__()
        self.listType = 'Stock Index List'

    def addStockIndex(self, codeString, nameString, securityTypeString = 'Stock Index'):
        tmpList = self.all + [stockIndex(codeString,nameString,securityTypeString)]
        self.setAll(tmpList)

    def addStockIndexSeries(self, indexCodeSeries, indexNameSeries, securityTypeString = 'Stock Index'):
        bondSeries = [stockIndex(i,j,securityTypeString) for i,j in zip(indexCodeSeries,indexNameSeries)]
        tmpList = self.all + bondSeries
        self.setAll(tmpList)



