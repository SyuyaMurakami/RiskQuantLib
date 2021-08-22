#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Property.NumberProperty.numberProperty import numberProperty

class modifiedDuration(numberProperty):
    def __init__(self,value,unit = ''):
        super(modifiedDuration,self).__init__(value,unit)



