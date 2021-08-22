#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Property.NumberProperty.numberProperty import numberProperty

class macaulayDuration(numberProperty):
    def __init__(self,value,unit = ''):
        super(macaulayDuration,self).__init__(value,unit)



