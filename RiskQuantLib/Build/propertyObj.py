#!/usr/bin/python
#coding = utf-8
import os,importlib
import sys
from RiskQuantLib.Build.buildFuction import *

class propertyObj():
    """
    propertyObj() is a class that store attribute building information and commit buildings.
    """
    pathObj = None
    pathDict = None
    listPathDict = None

    def __init__(self,propertyNameString:str,targetProjectPath = ''):
        """
        Any attribute should have a name.
        """
        self.name = propertyNameString
        targetProjectPath = sys.path[0] if targetProjectPath == '' else targetProjectPath
        spec = importlib.util.spec_from_file_location('pathObj', targetProjectPath + os.sep + 'RiskQuantLib' + os.sep + "Build" + os.sep + "pathObj.py")
        PO = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(PO)
        self.pathObj = PO.pathObj()
        self.pathDict = self.pathObj.pathDict
        self.listPathDict = self.pathObj.listPathDict

    def setPropertyName(self,propertyNameString:str):
        """
        setPropertyName(self,propertyNameString:str) is a function to set attribute name.

        Parameters
        ----------
        propertyNameString : str
            the attribute name you want to build attribute by.

        Returns
        -------
        None
        """
        self.name = propertyNameString

    def setBelongTo(self,belongToString:str):
        """
        setBelongTo(self,belongToString:str) is a function to set which instrument
        the attribute belongs to.

        Parameters
        ----------
        belongToString : str
            the instrument name you want the attribute to belong to.

        Returns
        -------
        None
        """
        self.belongTo = belongToString

    def setPropertyType(self,propertyTypeString:str):
        """
        setPropertyType(self,propertyTypeString:str) is a function to set the attribute
        value type.

        Parameters
        ----------
        propertyTypeString : str
            The type of attribute value.

        Returns
        -------
        None
        """
        self.propertyType = propertyTypeString

    def buildFunction(self):
        """
        buildFunction(self) is a function to generate source code of attribute set function.
        """
        if self.propertyType == 'String':
            self.code = buildStringFunction(self.name)
            self.listCode = buildListSetFunction1D(self.name,variableType='Str')
        elif self.propertyType == 'Number':
            self.code = buildNumberFunction(self.name)
            self.listCode = buildListSetFunction1D(self.name,variableType='Num')
        elif self.propertyType == 'Any':
            self.code = buildBaseFunction(self.name)
            self.listCode = buildListSetFunction1D(self.name,variableType='Base')
        elif self.propertyType == 'Series':
            self.code = buildBaseFunction(self.name)
            self.listCode = buildListSetFunction2D(self.name)
        else:
            self.code = buildSelfDefinedTypeFunction(self.name,self.propertyType)
            self.listCode = buildListSetFunction1D(self.name,variableType='Base')

    def buildTargetSourceFile(self):
        """
        buildTargetSourceFile(self) is a function to find which source file the generated code
        should be written into.
        """
        if self.belongTo in self.pathDict.keys():
            self.sourceFilePath = self.pathDict[self.belongTo]
        else:
            self.sourceFilePath = ''
        if self.belongTo in self.listPathDict.keys():
            self.sourceListFilePath = self.listPathDict[self.belongTo]
        else:
            self.sourceListFilePath = ''


















