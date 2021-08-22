#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Set.Security.Derivative.Future.future import setFuture
from RiskQuantLib.Security.Derivative.derivative import derivative

class future(derivative, setFuture):
    def __init__(self,codeString,nameString,securityTypeString = 'Future'):
        derivative.__init__(self,codeString,nameString,securityTypeString)







