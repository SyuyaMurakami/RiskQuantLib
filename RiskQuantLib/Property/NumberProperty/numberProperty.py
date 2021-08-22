#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Property.base import base

class numberProperty(base):
    def __init__(self,value,unit = ''):
        super(numberProperty,self).__init__(value)
        self.unit = unit

    def setUnit(self,unitString):
        self.unit = unitString

