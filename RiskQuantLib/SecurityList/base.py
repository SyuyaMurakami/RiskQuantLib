#!/usr/bin/python
#coding = utf-8
import numpy as np
import copy
from RiskQuantLib.Set.SecurityList.base import setBaseList
from RiskQuantLib.Operation.listBaseOperation import listBase
from RiskQuantLib.Security.base import base as securityBase

class baseList(setBaseList,listBase):
    """
    This is the basic list class. Any security list class should inherit from this.
    """
    elementClass = securityBase
    def __init__(self):
        self.all = []
        self.listType = 'Security List'
        self.__init_get_item__()

    def addSecurityList(self,securityObjList):
        tmpList = self.all+securityObjList
        self.setAll(tmpList)

    def addSecurity(self,securityCodeString,securityNameString,securityTypeString=''):
        tmpList = self.all+[securityBase(securityCodeString,securityNameString,securityTypeString)]
        self.setAll(tmpList)

    def addSecuritySeries(self,securityCodeSeries,securityNameSeries,securityTypeString = ''):
        securitySeries = [securityBase(i,j,securityTypeString) for i,j in zip(securityCodeSeries,securityNameSeries)]
        tmpList = self.all+securitySeries
        self.setAll(tmpList)


