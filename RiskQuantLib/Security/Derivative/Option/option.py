#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Set.Security.Derivative.Option.option import setOption
from RiskQuantLib.Security.Derivative.derivative import derivative
from QuantLib import Option

class option(derivative, Option, setOption):
    def __init__(self,codeString,nameString,securityTypeString = 'Option'):
        derivative.__init__(self,codeString,nameString,securityTypeString)

    def iniPricingModule(self,*args):
        Option.__init__(self, *args)





