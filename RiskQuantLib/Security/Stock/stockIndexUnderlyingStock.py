#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Set.Security.Stock.stockIndexUnderlyingStock import setStockIndexUnderlyingStock
from RiskQuantLib.Security.Stock.stock import stock

class stockIndexUnderlyingStock(stock,setStockIndexUnderlyingStock):
    def __init__(self,codeString,nameString,securityTypeString = 'Stock Index Underlying Stock'):
        super(stockIndexUnderlyingStock,self).__init__(codeString,nameString,securityTypeString)





