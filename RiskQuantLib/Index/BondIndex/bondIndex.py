#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Index.base import base
from RiskQuantLib.Set.Index.BondIndex.bondIndex import setBondIndex

class bondIndex(base,setBondIndex):
    """
    This class is the index following bond market.
    """
    def __init__(self,codeString:str,nameString:str,indexTypeString:str = 'Bond Index'):
        super(bondIndex,self).__init__(codeString,nameString,indexTypeString)



