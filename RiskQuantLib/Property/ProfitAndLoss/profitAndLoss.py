#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Property.NumberProperty.numberProperty import numberProperty

class profitAndLoss(numberProperty):
    def __init__(self,value,unit = 'RMB'):
        super(profitAndLoss,self).__init__(value,unit)



