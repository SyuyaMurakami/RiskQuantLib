#!/usr/bin/python
#coding = utf-8
import numpy as np
import QuantLib as ql
from QuantLib import InterestRate
from RiskQuantLib.Set.InterestRate.base import setBase

class base(InterestRate,setBase):
    """
    This is a class of interestrate.
    """
    def __init__(self,codeString:str,nameString:str,interestRateNum:float,interestTenor:float,interestRateTypeString = '',dayCount = ql.Actual365Fixed(), compounding = ql.Compounded, frequency = ql.Annual):
        """
        You must specify interest code, insterest name, interest value, interest tenor to initialize an
        interest object.

        Default day count convention is Actual365Fixed. Default compounding is Compounded.
        Default compounding frequency is Annual.

        """
        self.code = codeString
        self.name = nameString
        self.interestRateType = interestRateTypeString

        self.setInterestRate(interestRateNum)
        self.setTenor(interestTenor)

        self.dayCount = dayCount
        self.compounding = compounding
        self.frequency = frequency

    def iniInterestObj(self):
        """
        Calling this function will initialize QuantLib module with present attribute value.
        """
        args = (self.interestRate,self.dayCount,self.compounding,self.frequency)
        InterestRate.__init__(self,*args)

    def iniPricingModule(self, interestRateNum = np.nan ,dayCount = ql.Actual365Fixed(), compounding = ql.Compounded, frequency = ql.Annual):
        """
        Calling this function will initialize QuantLib module, given attribute value.
        """
        if type(interestRateNum)==type(np.nan) and np.isnan(interestRateNum):
            pass
        else:
            self.setInterestRate(interestRateNum)
        self.setDayCount(dayCount)
        self.setCompounding(compounding)
        self.setFrequency(frequency)

        self.iniInterestObj()








