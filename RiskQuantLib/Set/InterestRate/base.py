#!/usr/bin/python
#coding = utf-8
import numpy as np
import pandas as pd
from RiskQuantLib.Property.NumberProperty.numberProperty import numberProperty
from RiskQuantLib.Property.InterestRate.interestRate import interestRate

class setBase:

    def setCode(self,codeString):
        self.code = codeString

    def setName(self,nameString):
        self.name = nameString

    def setInterestRateType(self,interestRateTypeString):
        self.interestRateType = interestRateTypeString

    def setSubInterestRateType(self,subInterestRateType):
        self.subInterestRateType = subInterestRateType

    def setInterestRate(self,interestRateNum,interestRateDateTimeStamp = pd.Timestamp.now()):
        if not hasattr(self,'__interestRate'):
            self.__interestRate = interestRate(interestRateNum)
            self.interestRate = self.__interestRate.value
        else:
            self.__interestRate.setValue(interestRateNum)
        self.__interestRate.setEffectiveDate(interestRateDateTimeStamp)

    def setTenor(self,tenorValue,unitString='Year'):
        if not hasattr(self,'__tenor'):
            self.__tenor = numberProperty(tenorValue, unitString)
            self.tenor = self.__tenor.value
        else:
            self.__tenor.setValue(tenorValue)
            self.__tenor.setUnit(unitString)

    def setDayCount(self,dayCountObject):
        self.dayCount = dayCountObject

    def setCompounding(self,compoundingObject):
        self.compounding = compoundingObject

    def setFrequency(self,frequencyObject):
        self.frequency = frequencyObject

    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here
    #-<Begin>
    #-<End>