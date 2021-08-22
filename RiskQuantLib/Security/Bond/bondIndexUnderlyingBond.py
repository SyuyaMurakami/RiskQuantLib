#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Set.Security.Bond.bondIndexUnderlyingBond import setBondIndexUnderlyingBond
from RiskQuantLib.Security.Bond.bond import bond

class bondIndexUnderlyingBond(bond,setBondIndexUnderlyingBond):
    def __init__(self,codeString,nameString,securityTypeString = 'Bond Index Underlying Bond'):
        super(bondIndexUnderlyingBond,self).__init__(codeString,nameString,securityTypeString)





