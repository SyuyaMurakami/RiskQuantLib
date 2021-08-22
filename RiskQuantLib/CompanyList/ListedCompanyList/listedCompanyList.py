#!/usr/bin/python
#coding = utf-8

import pandas as pd
from RiskQuantLib.CompanyList.base import base
from RiskQuantLib.Company.ListedCompany.listedCompany import listedCompany
from RiskQuantLib.Set.CompanyList.ListedCompanyList.listedCompanyList import setListedCompanyList

class listedCompanyList(base,setListedCompanyList):
    def __init__(self):
        super(listedCompanyList,self).__init__()
        self.listType = 'Listed Company List'

    def addListedCompany(self, nameString, codeString = '', companyTypeString = 'Listed Company'):
        tmpList = self.all + [listedCompany(nameString, codeString, companyTypeString)]
        self.setAll(tmpList)

    def addListedCompanySeries(self, listedCompanyNameSeries, listedCompanyCodeSeries = pd.Series(), companyTypeString = 'Listed Company'):
        if listedCompanyCodeSeries.empty:
            listedCompanySeries = [listedCompany(i, '', companyTypeString) for i in listedCompanyNameSeries]
        else:
            listedCompanySeries = [listedCompany(i,j,companyTypeString) for i,j in zip(listedCompanyNameSeries,listedCompanyCodeSeries)]
        tmpList = self.all + listedCompanySeries
        self.setAll(tmpList)
