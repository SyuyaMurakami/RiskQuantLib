#!/usr/bin/python
#coding = utf-8
import numpy as np
from RiskQuantLib.SecurityList.base import baseList
from RiskQuantLib.Security.Fund.fund import fund
from RiskQuantLib.Set.SecurityList.FundList.fundList import setFundList

class fundList(baseList,setFundList):
    """
    fundList is one of the five basic list classes.
    """
    elementClass = fund
    def __init__(self):
        super(fundList,self).__init__()
        self.listType = 'Fund List'

    def addFund(self,codeString,nameString,securityTypeString = 'Fund'):
        tmpList = self.all + [fund(codeString,nameString,securityTypeString)]
        self.setAll(tmpList)

    def addFundSeries(self,fundCodeSeries,fundNameSeries,securityTypeString = 'Fund'):
        fundSeries = [fund(i,j,securityTypeString) for i,j in zip(fundCodeSeries,fundNameSeries)]
        tmpList = self.all + fundSeries
        self.setAll(tmpList)











