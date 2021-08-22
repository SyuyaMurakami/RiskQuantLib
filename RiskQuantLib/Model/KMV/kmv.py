#!/usr/bin/python
#coding = utf-8
import numpy as np
from scipy.optimize import fsolve
from scipy.stats import norm
from RiskQuantLib.Model.base import base

class kmv(base):
    def __init__(self, riskFreeRateNum, tenorNum, debtNum, equityNum, equitySigmaNum):
        super(kmv,self).__init__()
        self.riskFreeRate = riskFreeRateNum
        self.tenor = tenorNum
        self.debt = debtNum
        self.equity = equityNum
        self.equitySigma = equitySigmaNum

    def BSfunction(self, i):
        riskFreeRate, tenor, debt, equity, equitySigma = self.riskFreeRate, self.tenor, self.debt, self.equity, self.equitySigma
        asset, assetSigma = i[0], i[1]
        d1 = (np.log(asset / debt) + (riskFreeRate + 0.5*assetSigma*assetSigma)*tenor)/(assetSigma*np.sqrt(tenor))
        d2 = d1 - assetSigma*np.sqrt(tenor)
        return [asset*norm.cdf(d1) - debt*np.exp(-1*riskFreeRate*tenor)*norm.cdf(d2) - equity, norm.cdf(d1) * asset * assetSigma / equity - equitySigma]

    def calAssetAndAssetSigma(self):
        r = fsolve(self.BSfunction, [self.debt+self.equity, 0.5*self.equitySigma])
        self.asset = r[0]
        self.assetSigma = r[1]

    def calDistanceToDefault(self, shortTermDebtNum, longTermDebtNum, mixedRatioNum=0.5):
        self.defaultPoint = shortTermDebtNum + mixedRatioNum * longTermDebtNum
        self.defaultDistance = (self.asset - self.defaultPoint)/(self.asset * self.assetSigma)











