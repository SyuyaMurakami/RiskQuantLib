#!/usr/bin/python
#coding = utf-8
import numpy as np
import pandas as pd
from RiskQuantLib.Set.Security.base import setBase
from RiskQuantLib.Tool.strTool import getLastTradingDate

class setStock(setBase):

    def setPrice(self,priceNum,priceDateTimeStamp = pd.Timestamp.now()):
        from RiskQuantLib.Property.Price.price import price
        if not hasattr(self,'__price'):
            self.__price = price(priceNum)
            self.price = self.__price.value
        else:
            self.__price.setValue(priceNum)
            self.price = self.__price.value
        self.__price.setEffectiveDate(priceDateTimeStamp)

    def setFaceValue(self,faceValueNum):
        from RiskQuantLib.Property.FaceValue.faceValue import faceValue
        if not hasattr(self,'__faceValue'):
            self.__faceValue = faceValue(faceValueNum)
            self.faceValue = self.__faceValue.value
        else:
            self.__faceValue.setValue(faceValueNum)
            self.faceValue = self.__faceValue.value

    def setBeta(self,betaNum):
        from RiskQuantLib.Property.Beta.beta import beta
        if not hasattr(self,'__beta'):
            self.__beta = beta(betaNum)
            self.beta = self.__beta.value
        else:
            self.__beta.setValue(betaNum)
            self.beta = self.__beta.value

    def setIndustrySection(self,industrySectionString):
        self.industrySection = industrySectionString

    def setPastAverageDailyTradingAmount(self,pastAverageDailyTradingAmountNum):
        from RiskQuantLib.Property.Amount.averageAmount import averageAmount
        if not hasattr(self,'__pastAverageDailyTradingAmount'):
            self.__pastAverageDailyTradingAmount = averageAmount(pastAverageDailyTradingAmountNum)
            self.pastAverageDailyTradingAmount = self.__pastAverageDailyTradingAmount.value
        else:
            self.__pastAverageDailyTradingAmount.setValue(pastAverageDailyTradingAmountNum)
            self.pastAverageDailyTradingAmount = self.__pastAverageDailyTradingAmount.value

    def setPastAverageDailyTradingVolume(self,pastAverageDailyTradingVolumeNum):
        from RiskQuantLib.Property.MarketValue.averageMarketValue import averageMarketValue
        if not hasattr(self,'__pastAverageDailyTradingVolume'):
            self.__pastAverageDailyTradingVolume = averageMarketValue(pastAverageDailyTradingVolumeNum)
            self.pastAverageDailyTradingVolume = self.__pastAverageDailyTradingVolume.value
        else:
            self.__pastAverageDailyTradingVolume.setValue(pastAverageDailyTradingVolumeNum)
            self.pastAverageDailyTradingVolume = self.__pastAverageDailyTradingVolume.value

    def setClose(self, closeNum, closeDateTimeStamp = pd.Timestamp.now()):
        from RiskQuantLib.Property.Price.price import price
        if not hasattr(self,'__close'):
            self.__close = price(closeNum)
            self.close = self.__close.value
        else:
            self.__close.setValue(closeNum)
            self.close = self.__close.value
        self.__close.setEffectiveDate(closeDateTimeStamp)

    def setPreTradingDayClose(self, preTradingDayCloseNum, preTradingDayTimeStamp = getLastTradingDate(pd.Timestamp.now())):
        from RiskQuantLib.Property.Price.price import price
        if not hasattr(self,'__preTradingDayClose'):
            self.__preTradingDayClose = price(preTradingDayCloseNum)
            self.preTradingDayClose = self.__preTradingDayClose.value
        else:
            self.__preTradingDayClose.setValue(preTradingDayCloseNum)
            self.preTradingDayClose = self.__preTradingDayClose.value
        self.__preTradingDayClose.setEffectiveDate(preTradingDayTimeStamp)

    def calHoldingNetMarketValue(self):
        self.holdingNetMarketValue = self.price * self.holdingAmount

    def calEquityDelta(self):
        self.delta = self.holdingNetMarketValue

    def calLiquidityByAmount(self, maxLiquiditionRatio = 0.3):
        self.liquidity = self.holdingAmount / (self.pastAverageDailyTradingAmount * maxLiquiditionRatio)

    def calLiquidityByVolume(self, maxLiquiditionRatio=0.3):
        self.liquidity = self.holdingNetMarketValue / (self.pastAverageDailyTradingVolume * maxLiquiditionRatio)

    def calGainAndLoss(self):
        import numpy as np
        if hasattr(self, 'holdingAmount') and hasattr(self, 'lastDayHoldingAmount') and self.holdingAmount == self.lastDayHoldingAmount:
            try:
                self.gainAndLoss = self.holdingNetMarketValue - self.lastDayHoldingAmount * self.preTradingDayClose
            except Exception as e:
                self.gainAndLoss = np.nan
        else:
            try:
                self.gainAndLoss = self.holdingNetMarketValue - self.lastDayHoldingAmount * self.preTradingDayClose - self.lastDayBuyInMarketValue
            except Exception as e:
                self.gainAndLoss = np.nan

    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here
    #-<Begin>
    #-<End>