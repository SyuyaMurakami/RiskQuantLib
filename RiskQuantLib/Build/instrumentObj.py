#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Build.buildInstrument import *

class instrumentObj():
    """
    instrumentObj() is a class to store new instrument class information. It is
    the entrance of single instrument building.
    """

    def __init__(self,instrumentNameString:str):
        """
        Any instrument class should have a name.

        Parameters
        ----------
        instrumentNameString : str
            The instrument name you want to create class by.

        Returns
        -------
        None
        """
        self.name = instrumentNameString
        self.parentRQLClassName = ''
        self.parentQuantLibClassName = ''
        self.libraryName = ''
        self.defaultInstrumentType = ''

    def setInstrumentName(self,instrumentNameString:str):
        """
        setInstrumentName(self,instrumentNameString:str) if a function to set instrument name information.

        Parameters
        ----------
        instrumentNameString : str
            The instrument name you want to create class by.

        Returns
        -------
        None
        """
        self.name = instrumentNameString

    def setParentRQLClassName(self,parentRQLClassNameString:str):
        """
        setParentRQLClassName(self,parentRQLClassNameString:str) is a function to set parent RiskQuantLib
        classes that new instrument inherits from.

        Parameters
        ----------
        parentRQLClassNameString : str
            The instrument name you want the new instrument class to inherit from.
            If multiple parent classes are specified, they are separated by ','(comma)

        Returns
        -------
        None
        """
        if parentRQLClassNameString.find(',')!=-1:
            self.parentRQLClassName = parentRQLClassNameString.split(',')
        else:
            self.parentRQLClassName = parentRQLClassNameString

    def setParentQuantLibClassName(self,parentQuantLibClassNameString:str):
        """
        setParentQuantLibClassName(self,parentQuantLibClassNameString:str) is a function to set parent QuantLib
        classes that new instrument inherits from.

        Parameters
        ----------
        parentQuantLibClassNameString : str
            The instrument name you want the new instrument class to inherit from.
            If multiple parent classes are specified, they are separated by ','(comma)

        Returns
        -------
        None
        """
        if parentQuantLibClassNameString.find(',')!=-1:
            self.parentQuantLibClassName = parentQuantLibClassNameString.split(',')
        else:
            self.parentQuantLibClassName = parentQuantLibClassNameString
            
    def setLibraryName(self,libraryNameString:str):
        """
        setLibraryName(self,libraryNameString:str) is a function to set library
        that you may use within new instrument class file.

        Parameters
        ----------
        libraryNameString : str
            The library name you want the new instrument class to include.
            If multiple libraries are specified, they are separated by ','(comma)

        Returns
        -------
        None
        """
        if libraryNameString.find(',')!=-1:
            self.libraryName = libraryNameString.split(',')
        else:
            self.libraryName = libraryNameString

    def setDefaultInstrumentType(self,defaultInstrumentTypeString:str):
        """
        setDefaultInstrumentType(self,defaultInstrumentTypeString:str) is a function to set default
        class type that you want to mark the new instrument class as.

        Parameters
        ----------
        defaultInstrumentTypeString : str
            The class type that you want to mark the new instrument class as.

        Returns
        -------
        None
        """
        self.defaultInstrumentType = defaultInstrumentTypeString

    def commit(self, targetProjectPath:str = ''):
        """
        commit(self, targetProjectPath:str = '') is a function to commit .

        Parameters
        ----------
        targetProjectPath : str
            The RiskQuantLib project path where you want to commit instrument creation.

        Returns
        -------
        None
        """
        buildInstrument(self.name,self.parentRQLClassName,self.parentQuantLibClassName,self.libraryName,self.defaultInstrumentType,targetProjectPath)














