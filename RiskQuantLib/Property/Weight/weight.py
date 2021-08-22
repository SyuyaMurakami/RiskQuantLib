#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Property.NumberProperty.numberProperty import numberProperty

class weight(numberProperty):
    def __init__(self,value,unit = 'Number'):
        super(weight,self).__init__(value,unit)



