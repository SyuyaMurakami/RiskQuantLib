#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Set.Security.Derivative.Future.bondFuture import setBondFuture
from RiskQuantLib.Security.Derivative.Future.future import future

class bondFuture(future, setBondFuture):
    def __init__(self,codeString,nameString,securityTypeString = 'Bond Future'):
        future.__init__(self,codeString,nameString,securityTypeString)







