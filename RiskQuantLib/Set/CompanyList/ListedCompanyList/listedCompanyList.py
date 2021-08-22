#!/usr/bin/python
#coding = utf-8
import numpy as np
import pandas as pd
from RiskQuantLib.Set.CompanyList.base import setBase

class setListedCompanyList(setBase):

    def calKMV(self, companyNameSeries, riskFreeRateSeries, tenorSeries, debtSeries, equitySeries, equitySigmaSeries, shortTermDebtSeries, longTermDebtSeries, mixedRatioSeries = pd.Series()):
        if mixedRatioSeries.empty:
            mixedRatioDict = dict(zip(companyNameSeries,[0.5 for i in range(len(companyNameSeries))]))
        else:
            mixedRatioDict = dict(zip(companyNameSeries,mixedRatioSeries))
        riskFreeRateDict = dict(zip(companyNameSeries,riskFreeRateSeries))
        tenorDict = dict(zip(companyNameSeries,tenorSeries))
        debtDict = dict(zip(companyNameSeries,debtSeries))
        equityDict = dict(zip(companyNameSeries,equitySeries))
        equitySigmaDict = dict(zip(companyNameSeries,equitySigmaSeries))
        shortTermDebtDict = dict(zip(companyNameSeries,shortTermDebtSeries))
        longTermDebtDict = dict(zip(companyNameSeries,longTermDebtSeries))
        [i.calKMV(riskFreeRateDict[i.name],tenorDict[i.name],debtDict[i.name],equityDict[i.name],equitySigmaDict[i.name],shortTermDebtDict[i.name],longTermDebtDict[i.name],mixedRatioDict[i.name]) if i.name in mixedRatioDict.keys() else -1 for i in self.all]

    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here
    #-<Begin>
    #-<End>