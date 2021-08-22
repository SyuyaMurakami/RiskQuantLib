#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Property.NumberProperty.numberProperty import numberProperty

class nav(numberProperty):
    def __init__(self,value,unit = 'RMB'):
        super(nav,self).__init__(value,unit)



