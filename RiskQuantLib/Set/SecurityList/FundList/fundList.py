#!/usr/bin/python
#coding = utf-8
import numpy as np
from RiskQuantLib.Set.SecurityList.base import setBaseList

class setFundList(setBaseList):

    def setNav(self, codeSeries, navSeries):
        navDict = dict(zip(codeSeries, navSeries))
        [i.setNav(navDict[i.code]) if i.code in navDict.keys() else i.setNav(np.nan) for i in self.all]

    def setNavSeries(self,navDataFrame):
        import pandas as pd
        fundCodeList = navDataFrame.columns.to_list()
        [i.setNavSeries(navDataFrame[i.code]) if i.code in fundCodeList else i.setNavSeries(pd.Series()) for i in self.all]

    def setStrategyType(self,codeSeries,strategyTypeSeries):
        strategyTypeDict = dict(zip(codeSeries,strategyTypeSeries))
        [i.setStrategy(strategyTypeDict[i.code]) if i.code in strategyTypeDict.keys() else i.setStrategy('') for i in self.all]

    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here
    #-<Begin>
    #-<End>