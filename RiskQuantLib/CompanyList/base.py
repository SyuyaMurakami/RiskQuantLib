#!/usr/bin/python
#coding = utf-8

import pandas as pd
from RiskQuantLib.Company.base import base as company
from RiskQuantLib.Set.CompanyList.base import setBase
from RiskQuantLib.Operation.listBaseOperation import listBase

class baseList(setBase,listBase):
    """
    This class is the basic company list class.
    """
    elementClass = company
    def __init__(self):
        self.all = []
        self.listType = 'Company List'
        self.__init_get_item__()

    def addCompany(self, codeString:str, nameString:str = '', companyTypeString:str = 'Company'):
        """
        Add a company object to company list.
        """
        tmpList = self.all + [company(codeString, nameString, companyTypeString)]
        self.setAll(tmpList)


    def addCompanySeries(self, CompanyCodeSeries, CompanyNameSeries = pd.Series(), companyTypeString = 'Company'):
        """
        Add lots of company objects to company list.
        """
        if CompanyNameSeries.empty:
            CompanySeries = [company(i, '', companyTypeString) for i in CompanyCodeSeries]
        else:
            CompanySeries = [company(i,j,companyTypeString) for i,j in zip(CompanyCodeSeries,CompanyNameSeries)]
        tmpList = self.all + CompanySeries
        self.setAll(tmpList)

    def addCompanyFromSecurityList(self,securityListObject):
        """
        Add company objects from a list of securities.
        """
        from RiskQuantLib.SecurityList.base import baseList as securityList
        registeredCompany = [i.code for i in self.all]
        registeredSecurity = [j for i in self.all for j in i.issuedSecurityList.all if hasattr(i,'issuedSecurityList')]
        registeredSecurityCode = [i.code for i in registeredSecurity]
        companyCodeList = [i.issuer for i in securityListObject.all if hasattr(i,'issuer')]
        companyCodeList = list(set([i for i in companyCodeList if i!='' and i not in registeredCompany]))
        CompanySeries = [company(i,'','') for i in companyCodeList] + self.all # generate a list of all companies
        securityWaitingToBeAdded = [i for i in securityListObject.all if i.code not in registeredSecurityCode]+registeredSecurity# generate all securities of companies
        issuedSecurity = [[j for j in securityWaitingToBeAdded if hasattr(j,'issuer') and j.issuer == i.code] for i in CompanySeries]# find securities belong to each company
        issuedSecurityList = [securityList() for i in CompanySeries]# generate a new securityList for each company
        [j.addSecurityList(i) for i,j in zip(issuedSecurity,issuedSecurityList)]# for each company, set securities into securityList
        [i.setIssuedSecurityList(j) for i,j in zip(CompanySeries,issuedSecurityList)]# set securityList as company object attribute
        [[j.setIssuerObject(i) for j in i.issuedSecurityList.all] for i in CompanySeries]# set company object as security attribute
        self.setAll([i for i in self.all if i.code not in [j.code for j in CompanySeries]] + CompanySeries)











