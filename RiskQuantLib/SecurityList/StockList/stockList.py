#!/usr/bin/python
#coding = utf-8

import pandas as pd
from RiskQuantLib.SecurityList.base import baseList
from RiskQuantLib.Security.Stock.stock import stock
from RiskQuantLib.Set.SecurityList.StockList.stockList import setStockList


class stockList(baseList,setStockList):
    """
    stockList is one of the five basic list classes.
    """
    elementClass = stock
    def __init__(self):
        super(stockList,self).__init__()
        self.listType = 'Stock List'

    def addStock(self,codeString,nameString,securityTypeString = 'Stock'):
        tmpList = self.all+[stock(codeString,nameString,securityTypeString)]
        self.setAll(tmpList)

    def addStockSeries(self,stockCodeSeries,stockNameSeries,securityTypeString = 'Stock'):
        stockSeries = [stock(i,j,securityTypeString) for i,j in zip(stockCodeSeries,stockNameSeries)]
        tmpList = self.all + stockSeries
        self.setAll(tmpList)


