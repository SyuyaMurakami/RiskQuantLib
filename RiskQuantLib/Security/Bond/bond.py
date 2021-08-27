#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Set.Security.Bond.bond import setBond
from RiskQuantLib.Security.base import base
from QuantLib import Bond

class bond(base, Bond, setBond):
    """
    bond is one of the five basic classes.
    """
    def __init__(self,codeString,nameString,securityTypeString = 'Bond'):
        base.__init__(self,codeString,nameString,securityTypeString)

    def iniPricingModule(self,*args):
        Bond.__init__(self,*args)






