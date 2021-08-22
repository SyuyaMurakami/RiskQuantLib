#!/usr/bin/python
#coding = utf-8

import numpy as np
from RiskQuantLib.Set.Company.base import setBase

class setListedCompany(setBase):

    def calKMV(self, riskFreeRateNum, tenorNum, debtNum, equityNum, equitySigmaNum, shortTermDebt, longTermDebt, mixedRatio = 0.5):
        from RiskQuantLib.Model.KMV.kmv import kmv
        self.kmv = kmv(riskFreeRateNum,tenorNum,debtNum,equityNum,equitySigmaNum)
        self.kmv.calAssetAndAssetSigma()
        self.kmv.calDistanceToDefault(shortTermDebt,longTermDebt,mixedRatio)

    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here
    #-<Begin>
    #-<End>