#!/usr/bin/python
#coding = utf-8
import os

class instrumentList():
    """
    instrumentList() is a class used to format instrument building information and commit building.
    This is the entrance of new instrument building action.
    """

    def __init__(self):
        """
        Any 'RiskQuantLib List' object should have self.all, which is a list to contain elements.
        """
        self.all = []

    def addInstrument(self,instrumentNameSeries):
        """
        addInstrument(self,instrumentNameSeries) is a function to add new instrument registrations.

        Parameters
        ----------
        instrumentNameSeries : iterable object
            This variable must be an iterable object and each element should be a string, specifying
            the name of instruments.

        Returns
        -------
        None
        """
        from RiskQuantLib.Build.instrumentObj import instrumentObj
        self.all += [instrumentObj(i) for i in instrumentNameSeries]

    def setParentRQLClassName(self,instrumentNameSeries,parentRQLClassNameSeries):
        """
        setParentRQLClassName(self,instrumentNameSeries,parentRQLClassNameSeries) is a function to
        set parent RiskQuantLib class of new instrument.

        Parameters
        ----------
        instrumentNameSeries : iterable object
            This variable must be an iterable object and each element should be a string, specifying
            the name of instruments.
        parentRQLClassNameSeries : iterable object
            This variable must be an iterable object and each element should be a string, specifying
            the RiskQuantLib class name which instruments inherit from. If multiple classes are parents,
            they should be within one string, separated by ','. Note: The length of parentRQLClassNameSeries
            must be equal to that of instrumentNameSeries.

        Returns
        -------
        None
        """
        tmpDict = dict(zip(instrumentNameSeries,parentRQLClassNameSeries))
        [i.setParentRQLClassName(tmpDict[i.name]) if i.name in tmpDict.keys() else i.setParentRQLClassName('') for i in self.all]


    def setParentQuantLibClassName(self,instrumentNameSeries,parentQuantLibClassNameSeries):
        """
        setParentQuantLibClassName(self,instrumentNameSeries,parentQuantLibClassNameSeries) is a function to
        set parent QuantLib class of new instrument.

        Parameters
        ----------
        instrumentNameSeries : iterable object
            This variable must be an iterable object and each element should be a string, specifying
            the name of instruments.
        parentQuantLibClassNameSeries : iterable object
            This variable must be an iterable object and each element should be a string, specifying
            the QuantLib class name which instruments inherit from. If multiple classes are parents,
            they should be within one string, separated by ','. Note: The length of parentQuantLibClassNameSeries
            must be equal to that of instrumentNameSeries.

        Returns
        -------
        None
        """
        tmpDict = dict(zip(instrumentNameSeries,parentQuantLibClassNameSeries))
        [i.setParentQuantLibClassName(tmpDict[i.name]) if i.name in tmpDict.keys() else i.setParentQuantLibClassName('') for i in self.all]

    def setLibraryName(self,instrumentNameSeries,libraryNameSeries):
        """
        setLibraryName(self,instrumentNameSeries,libraryNameSeries) is a function to
        set other library you want to use in new instrument class.

        Parameters
        ----------
        instrumentNameSeries : iterable object
            This variable must be an iterable object and each element should be a string, specifying
            the name of instruments.
        libraryNameSeries : iterable object
            This variable must be an iterable object and each element should be a string, specifying
            the library you want to include in instrument class file. If multiple classes are included,
            they should be within one string, separated by ','. Note: The length of libraryNameSeries
            must be equal to that of instrumentNameSeries.

        Returns
        -------
        None
        """
        tmpDict = dict(zip(instrumentNameSeries,libraryNameSeries))
        [i.setLibraryName(tmpDict[i.name]) if i.name in tmpDict.keys() else i.setLibraryName('') for i in self.all]

    def setDefaultInstrumentType(self,instrumentNameSeries,defaultInstrumentTypeSeries):
        """
        setDefaultInstrumentType(self,instrumentNameSeries,defaultInstrumentTypeSeries) is a function to
        set default instrument type you want to mark new instrument class as.

        Parameters
        ----------
        instrumentNameSeries : iterable object
            This variable must be an iterable object and each element should be a string, specifying
            the name of instruments.
        defaultInstrumentTypeSeries : iterable object
            This variable must be an iterable object and each element should be a string, specifying
            the type you want to mark instrument as. Note: The length of defaultInstrumentTypeSeries
            must be equal to that of instrumentNameSeries.

        Returns
        -------
        None
        """
        tmpDict = dict(zip(instrumentNameSeries,defaultInstrumentTypeSeries))
        [i.setDefaultInstrumentType(tmpDict[i.name]) if i.name in tmpDict.keys() else i.setDefaultInstrumentType('') for i in self.all]

    def commit(self,targetProjectPath:str = ''):
        """
        commit(self,targetProjectPath:str = '') is a function to
        commit building of new instruments.

        Parameters
        ----------
        targetProjectPath : str
            The RiskQuantLib project path where you want to build new instruments.

        Returns
        -------
        None
        """
        from RiskQuantLib.Build.buildInstrument import clearInstrumentPath
        from RiskQuantLib.Build.buildShortcut import buildShortcut,commitShortcut,clearShortcut
        clearInstrumentPath(targetProjectPath)
        [i.commit(targetProjectPath) for i in self.all]
        clearShortcut(targetProjectPath)
        shortcut = buildShortcut([i.name for i in self.all])
        commitShortcut(shortcut,targetProjectPath)














