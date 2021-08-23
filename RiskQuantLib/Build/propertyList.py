#!/usr/bin/python
#coding = utf-8
from RiskQuantLib.Build.buildFuction import *
import os

class propertyList():
    """
    propertyList() is a class to used to format attribute building information and commit building.
    This is the entrance of new attribute building action.
    """

    def __init__(self):
        """
        Any 'RiskQuantLib List' object should have self.all, which is a list to contain elements.
        """
        self.all = []

    def addProperty(self,propertyNameSeries,belongToSeries):
        """
        addProperty(self,propertyNameSeries,belongToSeries) is a function to add new attribute registrations.

        Parameters
        ----------
        propertyNameSeries : iterable object
            This variable must be an iterable object and each element should be a string, specifying
            the name of attributes.
        belongToSeries : iterable object
            This variable must be an iterable object and each element should be a string, specifying
            the instrument class name which the attributes belong to. Notice: All instrument name in
            RiskQuantLib should be capitalized with the first letter. The length of propertyNameSeries
            should be equal to that of belongToSeries.

        Returns
        -------
        None
        """
        from RiskQuantLib.Build.propertyObj import propertyObj
        self.all += [propertyObj(i) for i in propertyNameSeries]

        indexNameSeries = [str(nameIndex)+name for nameIndex,name in enumerate(propertyNameSeries)]
        belongToDict = dict(zip(indexNameSeries,belongToSeries))
        [i.setBelongTo(belongToDict[str(index)+i.name]) if str(index)+i.name in belongToDict.keys() else i.setBelongTo('') for index,i in enumerate(self.all)]

    def setPropertyType(self,nameSeries,belongToSeries,propertyTypeSeries):
        """
        setPropertyType(self,nameSeries,belongToSeries,propertyTypeSeries) is a function to set attribute types
        given attribute name and which instrument it belongs to.

        Parameters
        ----------
        nameSeries : iterable object
            This variable must be an iterable object and each element should be a string, specifying
            the name of attributes.
        belongToSeries : iterable object
            This variable must be an iterable object and each element should be a string, specifying
            the instrument class name which the attributes belong to. Notice: All instrument name in
            RiskQuantLib should be capitalized with the first letter.
        propertyTypeSeries : iterable object
            This variable must be an iterable object and each element should be a string, specifying
            attribute types.

            Notice: The length of propertyNameSeries should be equal to that of
            belongToSeries and propertyTypeSeries.

        Returns
        -------
        None
        """
        nameBelongToSeries = [name+belongTo for name,belongTo in zip(nameSeries,belongToSeries)]
        propertyTypeDict = dict(zip(nameBelongToSeries, propertyTypeSeries))
        [i.setPropertyType(propertyTypeDict[i.name+i.belongTo]) if (i.name+i.belongTo) in propertyTypeDict.keys() else i.setPropertyType('') for i in self.all]

    def buildFunction(self):
        """
        buildFunction(self) is a function to start generating source code of attribute setting function.
        """
        [i.buildFunction() for i in self.all]

    def buildTargetSourceFile(self):
        """
        buildTargetSourceFile(self) is a function to find which source code file the generated code should
        be written into.
        """
        [i.buildTargetSourceFile() for i in self.all]

    def commitForEachKind(self,propertyList:list,riskQuantLibProjectPath:str):
        """
        commitForEachKind(self,propertyList:list,riskQuantLibProjectPath:str) is a function to commit source
        code change for every instrument type.

        This function make sure that for one instrument, the file will only be open and written once, even if
        bunches of attributes are specified.

        Parameters
        ----------
        propertyList : list
            All attributes that need to be built into the same instrument.
        riskQuantLibProjectPath : str
            The RiskQuantLib project path where you want to commit this change.

        Returns
        -------
        None
        """
        codeList = [i.code for i in propertyList]
        listCodeList = [i.listCode for i in propertyList]
        if propertyList[0].sourceFilePath != '':
            commitObjectFunctionBuild(codeList,riskQuantLibProjectPath + os.sep + propertyList[0].sourceFilePath)
        if propertyList[0].sourceListFilePath != '':
            commitListFunctionBuild(listCodeList,riskQuantLibProjectPath + os.sep + propertyList[0].sourceListFilePath)

    def commit(self,projectPath:str):
        """
        commit(self,projectPath:str) is a function to commit bulding of attributes. It can only be called
        after you fill all information that building attributes need.

        Parameters
        ----------
        projectPath : str
            The RiskQuantLib project path where you want to commit this change.

        Returns
        -------
        None
        """
        pathList = [(i.sourceFilePath,i.sourceListFilePath) for i in self.all]
        pathList = list(set(pathList))
        buildClassification = [[j for j in self.all if j.sourceFilePath == i[0] and j.sourceListFilePath == i[1]] for i in pathList]
        [self.commitForEachKind(i,projectPath) for i in buildClassification]















