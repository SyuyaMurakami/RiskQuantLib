#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Set.Company.base import setBase

class base(setBase):
    """
    This is the company base class. Any company object should be initialized with name and code.
    Different from security class, company class use 'name' as key attribute, rather than 'code'.
    """
    def __init__(self,nameString:str,codeString:str='',companyTypeString:str = ''):
        self.name = nameString
        self.code = codeString
        self.companyType = companyTypeString











