#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Build.buildPropertyType import *

class propertyTypeObj():
    """
    propertyTypeObj() is a class to store new propertyType class information. It is
    the entrance of single propertyType building.
    """

    def __init__(self,propertyTypeNameString:str):
        """
        Any propertyType class should have a name.

        Parameters
        ----------
        propertyTypeNameString : str
            The propertyType name you want to create class by.

        Returns
        -------
        None
        """
        self.name = propertyTypeNameString
        self.libraryName = ''

    def setPropertyTypeName(self,propertyTypeNameString:str):
        """
        setPropertyTypeName(self,propertyTypeNameString:str) if a function to set propertyType name information.

        Parameters
        ----------
        propertyTypeNameString : str
            The propertyType name you want to create class by.

        Returns
        -------
        None
        """
        self.name = propertyTypeNameString

    def setLibraryName(self,libraryNameString:str):
        """
        setLibraryName(self,libraryNameString:str) is a function to set library
        that you may use within new propertyType class file.

        Parameters
        ----------
        libraryNameString : str
            The library name you want the new propertyType class to include.
            If multiple libraries are specified, they are separated by ','(comma)

        Returns
        -------
        None
        """
        if libraryNameString.find(',')!=-1:
            self.libraryName = libraryNameString.split(',')
        else:
            self.libraryName = libraryNameString

    def commit(self, targetProjectPath:str = ''):
        """
        commit(self, targetProjectPath:str = '') is a function to commit .

        Parameters
        ----------
        targetProjectPath : str
            The RiskQuantLib project path where you want to commit propertyType creation.

        Returns
        -------
        None
        """
        buildPropertyType(self.name,self.libraryName,targetProjectPath)














