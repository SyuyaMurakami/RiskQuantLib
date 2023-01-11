#!/usr/bin/python
#coding = utf-8
import numpy as np
from scipy.optimize import fsolve
from scipy.stats import norm
from RiskQuantLib.Model.model import model
#<import>
#</import>

class kmv(model):
    """
    kmv(base) is a class to calculate KMV relative parameters, including Asset Volatility, Asset Value,
    Distance to Default.
    """
    #<init>
    def __init__(self, riskFreeRateNum:float, tenorNum:float, debtNum:float, equityNum:float, equitySigmaNum:float):
        """
        You must specify risk free rate, tenor, debt value, equity value and equity volatility to
        initialize KMV object.
        """
        super(kmv,self).__init__()
        self.riskFreeRate = riskFreeRateNum
        self.tenor = tenorNum
        self.debt = debtNum
        self.equity = equityNum
        self.equitySigma = equitySigmaNum
    #</init>

    def BSfunction(self, i):
        """
        A BS function used in KMV model.
        """
        riskFreeRate, tenor, debt, equity, equitySigma = self.riskFreeRate, self.tenor, self.debt, self.equity, self.equitySigma
        asset, assetSigma = i[0], i[1]
        d1 = (np.log(asset / debt) + (riskFreeRate + 0.5*assetSigma*assetSigma)*tenor)/(assetSigma*np.sqrt(tenor))
        d2 = d1 - assetSigma*np.sqrt(tenor)
        return [asset*norm.cdf(d1) - debt*np.exp(-1*riskFreeRate*tenor)*norm.cdf(d2) - equity, norm.cdf(d1) * asset * assetSigma / equity - equitySigma]

    def calAssetAndAssetSigma(self):
        """
        Calculate asset value and volatility of asset value
        """
        r = fsolve(self.BSfunction, [self.debt+self.equity, 0.5*self.equitySigma])
        self.asset = r[0]
        self.assetSigma = r[1]

    def calDistanceToDefault(self, shortTermDebtNum:float, longTermDebtNum:float, mixedRatioNum=0.5):
        """
        Calculate distance to default given short term debt and long term debt and mixed ratio.
        """
        self.defaultPoint = shortTermDebtNum + mixedRatioNum * longTermDebtNum
        self.defaultDistance = (self.asset - self.defaultPoint)/(self.asset * self.assetSigma)

    #<kmv>
    #</kmv>









