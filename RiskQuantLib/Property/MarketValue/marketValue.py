#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Property.NumberProperty.numberProperty import numberProperty

class marketValue(numberProperty):
    def __init__(self,value,unit = 'RMB'):
        super(marketValue,self).__init__(value,unit)



