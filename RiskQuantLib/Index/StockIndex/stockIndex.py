#!/usr/bin/python
#coding = utf-8


from RiskQuantLib.Index.base import base
from RiskQuantLib.Set.Index.StockIndex.stockIndex import setStockIndex

class stockIndex(base,setStockIndex):
    """
    This class is the index following stock market.
    """
    def __init__(self,codeString:str,nameString:str,indexTypeString:str = 'Stock Index'):
        super(stockIndex,self).__init__(codeString,nameString,indexTypeString)




