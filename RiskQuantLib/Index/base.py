#!/usr/bin/python
#coding = utf-8

from QuantLib import Index
from RiskQuantLib.Set.Index.base import setBase

class base(Index,setBase):
    """
    This is the basic class of index.
    """
    def __init__(self,codeString:str,nameString:str,indexTypeString:str = ''):
        """
        Only call this function won't initialize QuantLib pricing module. iniPricingModule()
        must be called to initialize pricing module.
        """
        self.code = codeString
        self.name = nameString
        self.indexType = indexTypeString

    def iniPricingModule(self,*args):
        """
        Calling this function will initialize QuantLib pricing module.
        """
        Index.__init__(self,*args)














