#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Set.Security.Derivative.Future.indexFuture import setIndexFuture
from RiskQuantLib.Security.Derivative.Future.future import future

class indexFuture(future, setIndexFuture):
    def __init__(self,codeString,nameString,securityTypeString = 'Index Future'):
        future.__init__(self,codeString,nameString,securityTypeString)







