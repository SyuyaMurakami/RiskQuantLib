#!/usr/bin/python
#coding = utf-8
import numpy as np
import pandas as pd
from RiskQuantLib.Tool.strTool import getLastTradingDate

class setBase():

    def setCode(self,codeString):
        self.code = codeString

    def setName(self,nameString):
        self.name = nameString

    def setIndex(self,indexString):
        self.index = indexString

    def setSubSecurityType(self,subSecurityType):
        self.subSecurityType = subSecurityType

    def setIssuer(self,issuerString):
        self.issuer = issuerString

    def setIssuerObject(self,issuerObject):
        self.issuerObject = issuerObject

    def setIssuerIndustrySection(self,issuerIndustrySectionString):
        self.issuerIndustrySection = issuerIndustrySectionString

    def setIssuerLocation(self,issuerLocationString):
        self.issuerLocation = issuerLocationString

    def setIssuerCode(self,issuerCodeString):
        self.issuerCode = issuerCodeString

    def setHoldingAmount(self,holdingAmountNum,holdingDateTimeStamp = pd.Timestamp.now()):
        from RiskQuantLib.Property.Amount.amount import amount
        if not hasattr(self,'__holdingAmount'):
            self.__holdingAmount = amount(holdingAmountNum)
            self.holdingAmount = self.__holdingAmount.value
        else:
            self.__holdingAmount.setValue(holdingAmountNum)
            self.holdingAmount = self.__holdingAmount.value
        self.__holdingAmount.setEffectiveDate(holdingDateTimeStamp)

    def setLastDayHoldingAmount(self,lastDayHoldingAmountNum,lastDayTimeStamp = getLastTradingDate(pd.Timestamp.now())):
        from RiskQuantLib.Property.Amount.amount import amount
        if not hasattr(self,'__lastDayHoldingAmount'):
            self.__lastDayHoldingAmount = amount(lastDayHoldingAmountNum)
            self.lastDayHoldingAmount = self.__lastDayHoldingAmount.value
        else:
            self.__lastDayHoldingAmount.setValue(lastDayHoldingAmountNum)
            self.lastDayHoldingAmount = self.__lastDayHoldingAmount.value
        self.__lastDayHoldingAmount.setEffectiveDate(lastDayTimeStamp)

    def setIssueDate(self,issueDateTimeStamp):
        self.issueDate = issueDateTimeStamp

    def setLatestBuyinDate(self,latestBuyinDate):
        self.latestBuyinDate = latestBuyinDate

    def setTotalNetMarketValue(self, totalNetMarketValueNum, dateTimeStamp=pd.Timestamp.now()):
        from RiskQuantLib.Property.MarketValue.marketValue import marketValue
        if not hasattr(self, '__totalNetMarketValue'):
            self.__totalNetMarketValue = marketValue(totalNetMarketValueNum)
            self.totalNetMarketValue = self.__totalNetMarketValue.value
        else:
            self.__totalNetMarketValue.setValue(totalNetMarketValueNum)
            self.totalNetMarketValue = self.__totalNetMarketValue.value
        self.__totalNetMarketValue.setEffectiveDate(dateTimeStamp)

    def setHoldingNetMarketValue(self, holdingNetMarketValueNum, dateTimeStamp=pd.Timestamp.now()):
        from RiskQuantLib.Property.MarketValue.marketValue import marketValue
        if not hasattr(self, '__holdingNetMarketValue'):
            self.__holdingNetMarketValue = marketValue(holdingNetMarketValueNum)
            self.holdingNetMarketValue = self.__holdingNetMarketValue.value
        else:
            self.__holdingNetMarketValue.setValue(holdingNetMarketValueNum)
            self.holdingNetMarketValue = self.__holdingNetMarketValue.value
        self.__holdingNetMarketValue.setEffectiveDate(dateTimeStamp)

    def setDaysOfCashingOut(self,daysOfCashingOutNum):
        self.daysOfCashingOut = daysOfCashingOutNum

    def setLatestTradingDate(self,latestTradingDateTimeStamp):
        self.latestTradingDate = latestTradingDateTimeStamp

    def setLastDayBuyInMarketValue(self, lastDayBuyInMarketValueNum, lastDayTimeStamp = getLastTradingDate(pd.Timestamp.now())):
        from RiskQuantLib.Property.MarketValue.marketValue import marketValue
        if not hasattr(self, '__lastDayBuyInMarketValue'):
            self.__lastDayBuyInMarketValue = marketValue(lastDayBuyInMarketValueNum)
            self.lastDayBuyInMarketValue = self.__lastDayBuyInMarketValue.value
        else:
            self.__lastDayBuyInMarketValue.setValue(lastDayBuyInMarketValueNum)
            self.lastDayBuyInMarketValue = self.__lastDayBuyInMarketValue.value
        self.__lastDayBuyInMarketValue.setEffectiveDate(lastDayTimeStamp)

    def setHistoricalCost(self,historicalCostNum):
        from RiskQuantLib.Property.Cost.cost import cost
        if not hasattr(self, '__historicalCost'):
            self.__historicalCost = cost(historicalCostNum)
            self.historicalCost = self.__historicalCost.value
        else:
            self.__historicalCost.setValue(historicalCostNum)
            self.historicalCost = self.__historicalCost.value

    def setProfitAndLoss(self, profitAndLossNum):
        from RiskQuantLib.Property.ProfitAndLoss.profitAndLoss import profitAndLoss
        if not hasattr(self, '__profitAndLoss'):
            self.__profitAndLoss = profitAndLoss(profitAndLossNum)
            self.profitAndLoss = self.__profitAndLoss.value
        else:
            self.__profitAndLoss.setValue(profitAndLossNum)
            self.profitAndLoss = self.__profitAndLoss.value

    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here
    #-<Begin>
    #-<End>