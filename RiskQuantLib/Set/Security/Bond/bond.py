#!/usr/bin/python
#coding = utf-8
import numpy as np
import pandas as pd
from RiskQuantLib.Set.Security.base import setBase

class setBond(setBase):

    def setCleanPrice(self,cleanPriceNum,cleanPriceDateTimeStamp = pd.Timestamp.now()):
        from RiskQuantLib.Property.Price.price import price
        if not hasattr(self,'__cleanPrice'):
            self.__cleanPrice = price(cleanPriceNum)
            self.cleanPrice = self.__cleanPrice.value
        else:
            self.__cleanPrice.setValue(cleanPriceNum)
            self.cleanPrice = self.__cleanPrice.value
        self.__cleanPrice.setEffectiveDate(cleanPriceDateTimeStamp)

    def setDirtyPrice(self,dirtyPriceNum,dirtyPriceDateTimeStamp = pd.Timestamp.now()):
        from RiskQuantLib.Property.Price.price import price
        if not hasattr(self,'__dirtyPrice'):
            self.__dirtyPrice = price(dirtyPriceNum)
            self.dirtyPrice = self.__dirtyPrice.value
        else:
            self.__dirtyPrice.setValue(dirtyPriceNum)
            self.dirtyPrice = self.__dirtyPrice.value
        self.__dirtyPrice.setEffectiveDate(dirtyPriceDateTimeStamp)

    def setFaceValue(self,faceValueNum):
        from RiskQuantLib.Property.FaceValue.faceValue import faceValue
        if not hasattr(self,'__faceValue'):
            self.__faceValue = faceValue(faceValueNum)
            self.faceValue = self.__faceValue.value
        else:
            self.__faceValue.setValue(faceValueNum)
            self.faceValue = self.__faceValue.value

    def setDv01(self,dv01Num):
        from RiskQuantLib.Property.Dv01.dv01 import dv01
        if not hasattr(self,'__dv01'):
            self.__dv01 = dv01(dv01Num)
            self.dv01 = self.__dv01.value
        else:
            self.__dv01.setValue(dv01Num)
            self.dv01 = self.__dv01.value

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


    def calHoldingNetMarketValue(self):
        self.holdingNetMarketValue = self.cleanPrice * self.holdingAmount

    def calHoldingFullMarketValue(self):
        self.holdingFullMarketValue = self.dirtyPrice * self.holdingAmount

    def calLiquidityByAmount(self, maxLiquiditionRatio = 0.3):
        self.liquidity = self.holdingAmount / (self.pastAverageDailyTradingAmount * maxLiquiditionRatio)

    def calLiquidityByVolume(self, maxLiquiditionRatio=0.3):
        self.liquidity = self.holdingNetMarketValue / (self.pastAverageDailyTradingVolume * maxLiquiditionRatio)


    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here
    #-<Begin>
    #-<End>