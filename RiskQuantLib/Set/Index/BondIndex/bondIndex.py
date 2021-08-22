#!/usr/bin/python
#coding = utf-8
import numpy as np
import pandas as pd
from RiskQuantLib.Set.Index.base import setBase
from RiskQuantLib.Tool.strTool import getLastTradingDate

class setBondIndex(setBase):

    def setPrice(self,priceNum,priceDateTimeStamp = pd.Timestamp.now()):
        from RiskQuantLib.Property.Price.price import price
        if not hasattr(self,'__price'):
            self.__price = price(priceNum)
            self.price = self.__price.value
        else:
            self.__price.setValue(priceNum)
        self.__price.setEffectiveDate(priceDateTimeStamp)

    def setClose(self, closeNum, closeDateTimeStamp = pd.Timestamp.now()):
        from RiskQuantLib.Property.Price.price import price
        if not hasattr(self,'__close'):
            self.__close = price(closeNum)
            self.close = self.__close.value
        else:
            self.__close.setValue(closeNum)
        self.__close.setEffectiveDate(closeDateTimeStamp)

    def setPreTradingDayClose(self, preTradingDayCloseNum, preTradingDayTimeStamp = getLastTradingDate(pd.Timestamp.now())):
        from RiskQuantLib.Property.Price.price import price
        if not hasattr(self,'__preTradingDayClose'):
            self.__preTradingDayClose = price(preTradingDayCloseNum)
            self.preTradingDayClose = self.__preTradingDayClose.value
        else:
            self.__preTradingDayClose.setValue(preTradingDayCloseNum)
        self.__preTradingDayClose.setEffectiveDate(preTradingDayTimeStamp)

    def setUnderlyingBond(self,underlyingBondCodeString,underlyingBondNameString,underlyingBondWeightString):
        from RiskQuantLib.SecurityList.BondList.bondIndexUnderlyingBondList import bondIndexUnderlyingBondList
        self.underlyingBondList = bondIndexUnderlyingBondList()
        self.underlyingBondList.addBondSeries(underlyingBondCodeString,underlyingBondNameString,underlyingBondWeightString)

    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here
    #-<Begin>
    #-<End>