#!/usr/bin/python
#coding = utf-8
import numpy as np
from RiskQuantLib.SecurityList.StockList.stockList import stockList
from RiskQuantLib.Security.Stock.stockIndexUnderlyingStock import stockIndexUnderlyingStock
from RiskQuantLib.Set.SecurityList.StockList.stockIndexUnderlyingStockList import setStockIndexUnderlyingStockList

class stockIndexUnderlyingStockList(stockList,setStockIndexUnderlyingStockList):
    elementClass = stockIndexUnderlyingStock
    def __init__(self):
        super(stockIndexUnderlyingStockList,self).__init__()
        self.listType = 'Stock Index Underlying Stock List'

    def addStock(self, codeString, nameString, weightNum = np.nan, securityTypeString = 'Stock Index Underlying Stock'):
        underlyingStock = stockIndexUnderlyingStock(codeString,nameString,securityTypeString)
        underlyingStock.setWeight(weightNum)
        tmpList = self.all+[underlyingStock]
        self.setAll(tmpList)

    def addStockSeries(self, stockCodeSeries, stockNameSeries, stockWeightSeries = np.nan, securityTypeString = 'Stock Index Underlying Stock'):
        stockSeries = [stockIndexUnderlyingStock(i,j,securityTypeString) for i,j in zip(stockCodeSeries,stockNameSeries)]
        if not (type(stockWeightSeries)==type(np.nan) and np.isnan(stockWeightSeries)):
            [i.setWeight(j) for i,j in zip(stockSeries,stockWeightSeries)]
        tmpList = self.all + stockSeries
        self.setAll(tmpList)






