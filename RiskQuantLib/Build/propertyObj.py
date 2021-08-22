#!/usr/bin/python
#coding = utf-8
import os
from RiskQuantLib.Build.buildFuction import *
from RiskQuantLib.Build.pathObj import pathObj as PO

class propertyObj():
    pathObj = PO()
    pathDict = pathObj.pathDict
    listPathDict = pathObj.listPathDict

    def __init__(self,propertyNameString):
        self.name = propertyNameString

    def setPropertyName(self,propertyNameString):
        self.name = propertyNameString

    def setBelongTo(self,belongToString):
        self.belongTo = belongToString

    def setPropertyType(self,propertyTypeString):
        self.propertyType = propertyTypeString

    def buildFunction(self):
        if self.propertyType == 'String':
            self.code = buildStringFunction(self.name)
            self.listCode = buildListSetFunction1D(self.name)
        elif self.propertyType == 'Number':
            self.code = buildNumberFunction(self.name)
            self.listCode = buildListSetFunction1D(self.name)
        elif self.propertyType == 'Any':
            self.code = buildBaseFunction(self.name)
            self.listCode = buildListSetFunction1D(self.name)
        elif self.propertyType == 'Series':
            self.code = buildBaseFunction(self.name)
            self.listCode = buildListSetFunction2D(self.name)
        else:
            return

    def buildTargetSourceFile(self):
        if self.belongTo in self.pathDict.keys():
            self.sourceFilePath = self.pathDict[self.belongTo]
        else:
            self.sourceFilePath = ''
        if self.belongTo in self.listPathDict.keys():
            self.sourceListFilePath = self.listPathDict[self.belongTo]
        else:
            self.sourceListFilePath = ''


















