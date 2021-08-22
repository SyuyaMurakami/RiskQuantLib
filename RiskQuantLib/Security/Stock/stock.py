#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Security.base import base
from RiskQuantLib.Set.Security.Stock.stock import setStock

class stock(base,setStock):
    def __init__(self,codeString,nameString,securityTypeString = 'Stock'):
        super(stock,self).__init__(codeString,nameString,securityTypeString)






