#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Index.base import base
from RiskQuantLib.Set.Index.BondIndex.bondIndex import setBondIndex

class bondIndex(base,setBondIndex):
    def __init__(self,codeString,nameString,indexTypeString = 'Bond Index'):
        super(bondIndex,self).__init__(codeString,nameString,indexTypeString)



