#!/usr/bin/python
#coding = utf-8

from QuantLib import Index
from RiskQuantLib.Set.Index.base import setBase

class base(Index,setBase):
    def __init__(self,codeString,nameString,indexTypeString = ''):
        self.code = codeString
        self.name = nameString
        self.indexType = indexTypeString

    def iniPricingModule(self,*args):
        Index.__init__(self,*args)














