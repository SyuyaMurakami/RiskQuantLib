#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Property.NumberProperty.numberProperty import numberProperty

class cost(numberProperty):
    def __init__(self,value,unit = 'RMB'):
        super(cost,self).__init__(value,unit)



