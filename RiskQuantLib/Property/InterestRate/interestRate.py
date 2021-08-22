#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Property.NumberProperty.numberProperty import numberProperty

class interestRate(numberProperty):
    def __init__(self,value,unit = ''):
        super(interestRate,self).__init__(value,unit)



