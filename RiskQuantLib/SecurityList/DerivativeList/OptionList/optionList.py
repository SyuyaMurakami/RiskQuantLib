#!/usr/bin/python
#coding = utf-8

import pandas as pd
from RiskQuantLib.SecurityList.DerivativeList.derivativeList import derivativeList
from RiskQuantLib.Security.Derivative.Option.option import option
from RiskQuantLib.Set.SecurityList.DerivativeList.OptionList.optionList import setOptionList


class optionList(derivativeList,setOptionList):
    elementClass = option
    def __init__(self):
        super(optionList, self).__init__()
        self.listType = 'Option List'

    def addOption(self, codeString, nameString, securityTypeString = 'Option'):
        tmpList = self.all + [option(codeString,nameString,securityTypeString)]
        self.setAll(tmpList)

    def addOptionSeries(self, optionCodeSeries, optionNameSeries, securityTypeString = 'Option'):
        optionSeries = [option(i,j,securityTypeString) for i,j in zip(optionCodeSeries,optionNameSeries)]
        tmpList = self.all + optionSeries
        self.setAll(tmpList)


