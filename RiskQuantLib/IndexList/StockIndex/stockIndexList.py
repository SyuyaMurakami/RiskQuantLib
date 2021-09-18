#!/usr/bin/python
#coding = utf-8


from RiskQuantLib.IndexList.base import baseList
from RiskQuantLib.Index.StockIndex.stockIndex import stockIndex
from RiskQuantLib.Set.IndexList.StockIndexList.stockIndexList import setStockIndexList

class stockIndexList(baseList,setStockIndexList):
    """
    This class is the list of stock index.
    """
    elementClass = stockIndex
    def __init__(self):
        super(stockIndexList, self).__init__()
        self.listType = 'Stock Index List'

    def addStockIndex(self, codeString:str, nameString:str, securityTypeString:str = 'Stock Index'):
        """
        Add a single stock index object into this list.
        """
        tmpList = self.all + [stockIndex(codeString,nameString,securityTypeString)]
        self.setAll(tmpList)

    def addStockIndexSeries(self, indexCodeSeries, indexNameSeries, securityTypeString = 'Stock Index'):
        """
        Add a series of stock index objects into this list.
        """
        bondSeries = [stockIndex(i,j,securityTypeString) for i,j in zip(indexCodeSeries,indexNameSeries)]
        tmpList = self.all + bondSeries
        self.setAll(tmpList)



