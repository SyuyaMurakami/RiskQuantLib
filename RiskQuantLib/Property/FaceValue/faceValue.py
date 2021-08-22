#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Property.NumberProperty.numberProperty import numberProperty

class faceValue(numberProperty):
    def __init__(self,value,unit = 'RMB'):
        super(faceValue,self).__init__(value,unit)



