#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Property.NumberProperty.numberProperty import numberProperty

class price(numberProperty):
    def __init__(self,value,unit = 'RMB'):
        super(price,self).__init__(value,unit)



