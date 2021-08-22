#!/usr/bin/python
#coding = utf-8
from RiskQuantLib.Build.buildFuction import *
import os

class propertyList():

    def __init__(self):
        self.all = []

    def addProperty(self,propertyNameSeries,belongToSeries):
        from RiskQuantLib.Build.propertyObj import propertyObj
        self.all += [propertyObj(i) for i in propertyNameSeries]

        indexNameSeries = [str(nameIndex)+name for nameIndex,name in enumerate(propertyNameSeries)]
        belongToDict = dict(zip(indexNameSeries,belongToSeries))
        [i.setBelongTo(belongToDict[str(index)+i.name]) if str(index)+i.name in belongToDict.keys() else i.setBelongTo('') for index,i in enumerate(self.all)]

    def setPropertyType(self,nameSeries,belongToSeries,propertyTypeSeries):
        nameBelongToSeries = [name+belongTo for name,belongTo in zip(nameSeries,belongToSeries)]
        propertyTypeDict = dict(zip(nameBelongToSeries, propertyTypeSeries))
        [i.setPropertyType(propertyTypeDict[i.name+i.belongTo]) if (i.name+i.belongTo) in propertyTypeDict.keys() else i.setPropertyType('') for i in self.all]

    def buildFunction(self):
        [i.buildFunction() for i in self.all]

    def buildTargetSourceFile(self):
        [i.buildTargetSourceFile() for i in self.all]

    def commitForEachKind(self,propertyList,riskQuantLibProjectPath):
        codeList = [i.code for i in propertyList]
        listCodeList = [i.listCode for i in propertyList]
        if propertyList[0].sourceFilePath != '':
            commitObjectFunctionBuild(codeList,riskQuantLibProjectPath + os.sep + propertyList[0].sourceFilePath)
        if propertyList[0].sourceListFilePath != '':
            commitListFunctionBuild(listCodeList,riskQuantLibProjectPath + os.sep + propertyList[0].sourceListFilePath)
        # print()

    def commit(self,projectPath):
        pathList = [(i.sourceFilePath,i.sourceListFilePath) for i in self.all]
        pathList = list(set(pathList))
        buildClassification = [[j for j in self.all if j.sourceFilePath == i[0] and j.sourceListFilePath == i[1]] for i in pathList]
        [self.commitForEachKind(i,projectPath) for i in buildClassification]
        # print()















