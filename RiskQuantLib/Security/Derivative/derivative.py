#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Set.Security.Derivative.derivative import setDerivative
from RiskQuantLib.Security.base import base

class derivative(base, setDerivative):
    """
    derivative is one of the five basic classes.
    """
    def __init__(self,codeString,nameString,securityTypeString = 'Derivative'):
        base.__init__(self,codeString,nameString,securityTypeString)







