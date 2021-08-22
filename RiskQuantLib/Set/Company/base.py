#!/usr/bin/python
#coding = utf-8
import numpy as np

class setBase():

    def setCode(self,codeString):
        self.code = codeString

    def setName(self,nameString):
        self.name = nameString

    def setCompanyType(self,companyTypeString):
        self.companyType = companyTypeString

    def setSubCompanyType(self,subCompanyType):
        self.subCompanyType = subCompanyType

    def setEstDate(self,estDateTimeStamp):
        self.estDate = estDateTimeStamp

    def setParentCompany(self,parentCompanyObject):
        self.parentCompany = parentCompanyObject

    def setChildCompany(self,childCompanyObject):
        self.childCompany = childCompanyObject

    def setIssuedSecurityList(self,issuedSecurityListObject):
        self.issuedSecurityList = issuedSecurityListObject

    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here
    #-<Begin>
    #-<End>