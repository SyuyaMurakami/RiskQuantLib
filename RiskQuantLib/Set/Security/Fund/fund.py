#!/usr/bin/python
#coding = utf-8
import numpy as np
import pandas as pd
from RiskQuantLib.Set.Security.base import setBase

class setFund(setBase):

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

    def setNav(self, navNum, effectiveDateTimeStamp = pd.Timestamp.now()):
        from RiskQuantLib.Property.Nav.nav import nav
        if not hasattr(self,'__nav'):
            self.__nav = nav(navNum)
            self.nav = self.__nav.value
        else:
            self.__nav.setValue(navNum)
            self.nav = self.__nav.value
        self.__nav.setEffectiveDate(effectiveDateTimeStamp)

    def setNavSeries(self,navSeries):
        self.navSeries = navSeries

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

    def setAUM(self,AUMNum):
        from RiskQuantLib.Property.Aum.aum import aum
        if not hasattr(self,'__AUM'):
            self.__AUM = aum(AUMNum)
            self.AUM = self.__AUM.value
        else:
            self.__AUM.setValue(AUMNum)
            self.AUM = self.__AUM.value

    def setStrategy(self,strategyString):
        self.strategy = strategyString

    def setManagementMode(self,managementModeString):
        self.managementMode = managementModeString

    def setRedemptionMode(self,redemptionModeString):
        self.redemptionMode = redemptionModeString


    def calHoldingNetMarketValue(self):
        self.holdingNetMarketValue = self.price * self.holdingAmount

    def calLiquidityByAmount(self, maxLiquiditionRatio = 0.3):
        self.liquidity = self.holdingAmount / (self.pastAverageDailyTradingAmount * maxLiquiditionRatio)

    def calLiquidityByVolume(self, maxLiquiditionRatio=0.3):
        self.liquidity = self.holdingNetMarketValue / (self.pastAverageDailyTradingVolume * maxLiquiditionRatio)

    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here
    #-<Begin>
    #-<End>