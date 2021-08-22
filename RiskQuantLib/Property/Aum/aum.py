#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Property.NumberProperty.numberProperty import numberProperty

class aum(numberProperty):
    def __init__(self,value,unit = 'RMB'):
        super(aum,self).__init__(value,unit)



