#!/usr/bin/python
#coding = utf-8

import pandas as pd
from RiskQuantLib.CompanyList.base import base
from RiskQuantLib.Company.ListedCompany.listedCompany import listedCompany
from RiskQuantLib.Set.CompanyList.ListedCompanyList.listedCompanyList import setListedCompanyList

class listedCompanyList(base,setListedCompanyList):
    """
    This class is the list of listed company.
    Different from security list, company list use 'name' as key attribute, rather than 'code'.
    """
    def __init__(self):
        super(listedCompanyList,self).__init__()
        self.listType = 'Listed Company List'

    def addListedCompany(self, nameString:str, codeString:str = '', companyTypeString:str = 'Listed Company'):
        """
        Add a company object to list.
        """
        tmpList = self.all + [listedCompany(nameString, codeString, companyTypeString)]
        self.setAll(tmpList)

    def addListedCompanySeries(self, listedCompanyNameSeries, listedCompanyCodeSeries = pd.Series(), companyTypeString = 'Listed Company'):
        """
        Add lots of companies into list.
        """
        if listedCompanyCodeSeries.empty:
            listedCompanySeries = [listedCompany(i, '', companyTypeString) for i in listedCompanyNameSeries]
        else:
            listedCompanySeries = [listedCompany(i,j,companyTypeString) for i,j in zip(listedCompanyNameSeries,listedCompanyCodeSeries)]
        tmpList = self.all + listedCompanySeries
        self.setAll(tmpList)
