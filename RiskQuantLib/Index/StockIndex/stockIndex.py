#!/usr/bin/python
#coding = utf-8


from RiskQuantLib.Index.base import base
from RiskQuantLib.Set.Index.StockIndex.stockIndex import setStockIndex

class stockIndex(base,setStockIndex):
    def __init__(self,codeString,nameString,indexTypeString = 'Stock Index'):
        super(stockIndex,self).__init__(codeString,nameString,indexTypeString)




