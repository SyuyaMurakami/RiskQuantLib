#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Set.Company.base import setBase

class base(setBase):
    """
    This is the company base class. Any company object should be initialized with code and name.
    """
    def __init__(self,codeString:str,nameString:str='',companyTypeString:str = ''):
        self.code = codeString
        self.name = nameString
        self.companyType = companyTypeString











