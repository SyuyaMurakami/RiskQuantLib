#!/usr/bin/python
#coding = utf-8
import numpy as np
import QuantLib as ql
from QuantLib import InterestRate
from RiskQuantLib.Set.InterestRate.base import setBase

class base(InterestRate,setBase):
    def __init__(self,codeString,nameString,interestRateNum,interestTenor,interestRateTypeString = '',dayCount = ql.Actual365Fixed(), compounding = ql.Compounded, frequency = ql.Annual):
        self.code = codeString
        self.name = nameString
        self.interestRateType = interestRateTypeString

        self.setInterestRate(interestRateNum)
        self.setTenor(interestTenor)

        self.dayCount = dayCount
        self.compounding = compounding
        self.frequency = frequency

    def iniInterestObj(self):
        args = (self.interestRate,self.dayCount,self.compounding,self.frequency)
        InterestRate.__init__(self,*args)

    def iniPricingModule(self, interestRateNum = np.nan ,dayCount = ql.Actual365Fixed(), compounding = ql.Compounded, frequency = ql.Annual):
        if type(interestRateNum)==type(np.nan) and np.isnan(interestRateNum):
            pass
        else:
            self.setInterestRate(interestRateNum)
        self.setDayCount(dayCount)
        self.setCompounding(compounding)
        self.setFrequency(frequency)

        self.iniInterestObj()








