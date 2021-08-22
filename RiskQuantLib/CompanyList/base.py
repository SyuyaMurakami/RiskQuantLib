#!/usr/bin/python
#coding = utf-8

import pandas as pd
from RiskQuantLib.Company.base import base as company
from RiskQuantLib.Set.CompanyList.base import setBase
from RiskQuantLib.Operation.listBaseOperation import listBase

class base(setBase,listBase):
    def __init__(self):
        self.all = []
        self.listType = 'Company List'
        self.__init_get_item__()

    def addCompany(self, nameString, codeString = '', companyTypeString = 'Company'):
        tmpList = self.all + [company(nameString, codeString, companyTypeString)]
        self.setAll(tmpList)


    def addCompanySeries(self, CompanyNameSeries, CompanyCodeSeries = pd.Series(), companyTypeString = 'Company'):
        if CompanyCodeSeries.empty:
            CompanySeries = [company(i, '', companyTypeString) for i in CompanyNameSeries]
        else:
            CompanySeries = [company(i,j,companyTypeString) for i,j in zip(CompanyNameSeries,CompanyCodeSeries)]
        tmpList = self.all + CompanySeries
        self.setAll(tmpList)

    def addCompanyFromSecurityList(self,securityListObject):
        from RiskQuantLib.SecurityList.base import baseList as securityList
        registeredCompany = [i.name for i in self.all]
        registeredSecurity = [j for i in self.all for j in i.issuedSecurityList.all if hasattr(i,'issuedSecurityList')]
        registeredSecurityCode = [i.code for i in registeredSecurity]
        companyNameList = [i.issuer for i in securityListObject.all if hasattr(i,'issuer')]
        companyNameList = list(set([i for i in companyNameList if i!='' and i not in registeredCompany]))
        CompanySeries = [company(i,'','') for i in companyNameList] + self.all # 生成公司列表
        securityWaitingToBeAdded = [i for i in securityListObject.all if i.code not in registeredSecurityCode]+registeredSecurity# 生成新的待选证券池
        issuedSecurity = [[j for j in securityWaitingToBeAdded if hasattr(j,'issuer') and j.issuer == i.name] for i in CompanySeries]#找到每个公司对应的证券
        issuedSecurityList = [securityList() for i in CompanySeries]# 生成每个公司的证券列表
        [j.addSecurityList(i) for i,j in zip(issuedSecurity,issuedSecurityList)]# 将公司发行的证券填入公司的证券列表
        [i.setIssuedSecurityList(j) for i,j in zip(CompanySeries,issuedSecurityList)]# 将公司的证券列表挂载到公司
        [[j.setIssuerObject(i) for j in i.issuedSecurityList.all] for i in CompanySeries]# 将公司列表挂载到证券
        self.setAll([i for i in self.all if i.name not in [j.name for j in CompanySeries]] + CompanySeries)











