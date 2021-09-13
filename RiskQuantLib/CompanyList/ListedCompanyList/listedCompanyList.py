#!/usr/bin/python
#coding = utf-8

import pandas as pd
from RiskQuantLib.CompanyList.base import baseList
from RiskQuantLib.Company.ListedCompany.listedCompany import listedCompany
from RiskQuantLib.Set.CompanyList.ListedCompanyList.listedCompanyList import setListedCompanyList

class listedCompanyList(baseList,setListedCompanyList):
    """
    This class is the list of listed company.
    """
    def __init__(self):
        super(listedCompanyList,self).__init__()
        self.listType = 'Listed Company List'

    def addListedCompany(self, codeString:str, nameString:str = '', companyTypeString:str = 'Listed Company'):
        """
        Add a company object to list.
        """
        tmpList = self.all + [listedCompany(codeString, nameString, companyTypeString)]
        self.setAll(tmpList)

    def addListedCompanySeries(self, listedCompanyCodeSeries, listedCompanyNameSeries = pd.Series(), companyTypeString = 'Listed Company'):
        """
        Add lots of companies into list.
        """
        if listedCompanyNameSeries.empty:
            listedCompanySeries = [listedCompany(i, '', companyTypeString) for i in listedCompanyCodeSeries]
        else:
            listedCompanySeries = [listedCompany(i,j,companyTypeString) for i,j in zip(listedCompanyCodeSeries,listedCompanyNameSeries)]
        tmpList = self.all + listedCompanySeries
        self.setAll(tmpList)
