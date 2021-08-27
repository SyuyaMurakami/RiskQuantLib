#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Set.Security.Fund.fund import setFund
from RiskQuantLib.Security.base import base

class fund(base,setFund):
    """
    fund is one of the five basic classes.
    """
    def __init__(self,codeString,nameString,securityTypeString = 'Fund'):
        super(fund,self).__init__(codeString,nameString,securityTypeString)







