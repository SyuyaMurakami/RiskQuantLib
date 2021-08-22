#!/usr/bin/python
#coding = utf-8


from RiskQuantLib.Company.base import base
from RiskQuantLib.Set.Company.ListedCompany.listedCompany import setListedCompany

class listedCompany(base,setListedCompany):
    def __init__(self,nameString,codeString='',companyTypeString = 'Listed Company'):
        super(listedCompany,self).__init__(nameString,codeString,companyTypeString)



