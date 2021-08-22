#!/usr/bin/python
#coding = utf-8
import numpy as np

class setBaseList:

    def setIssuer(self,codeSeries,issuerSeries):
        issuerDict = dict(zip(codeSeries,issuerSeries))
        [i.setIssuer(issuerDict[i.code]) if i.code in issuerDict.keys() else i.setIssuer('') for i in self.all]

    def setHistoricalCost(self,codeSeries,costSeries):
        costDict = dict(zip(codeSeries,costSeries))
        [i.setHistoricalCost(costDict[i.code]) if i.code in costDict.keys() else i.setHistoricalCost(np.nan) for i in self.all]

    def setHoldingAmount(self,codeSeries,holdingAmountSeries):
        holdingAmountDict = dict(zip(codeSeries,holdingAmountSeries))
        [i.setHoldingAmount(holdingAmountDict[i.code]) if i.code in holdingAmountDict.keys() else i.setHoldingAmount(np.nan) for i in self.all]

    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here
    #-<Begin>
    #-<End>