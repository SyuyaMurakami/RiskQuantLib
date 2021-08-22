#!/usr/bin/python
#coding = utf-8
import os

class instrumentList():

    def __init__(self):
        self.all = []

    def addInstrument(self,instrumentNameSeries):
        from RiskQuantLib.Build.instrumentObj import instrumentObj
        self.all += [instrumentObj(i) for i in instrumentNameSeries]

    def setParentRQLClassName(self,instrumentNameSeries,parentRQLClassNameSeries):
        tmpDict = dict(zip(instrumentNameSeries,parentRQLClassNameSeries))
        [i.setParentRQLClassName(tmpDict[i.name]) if i.name in tmpDict.keys() else i.setParentRQLClassName('') for i in self.all]


    def setParentQuantLibClassName(self,instrumentNameSeries,parentQuantLibClassNameSeries):
        tmpDict = dict(zip(instrumentNameSeries,parentQuantLibClassNameSeries))
        [i.setParentQuantLibClassName(tmpDict[i.name]) if i.name in tmpDict.keys() else i.setParentQuantLibClassName('') for i in self.all]

    def setLibraryName(self,instrumentNameSeries,libraryNameSeries):
        tmpDict = dict(zip(instrumentNameSeries,libraryNameSeries))
        [i.setLibraryName(tmpDict[i.name]) if i.name in tmpDict.keys() else i.setLibraryName('') for i in self.all]

    def setDefaultInstrumentType(self,instrumentNameSeries,defaultInstrumentTypeSeries):
        tmpDict = dict(zip(instrumentNameSeries,defaultInstrumentTypeSeries))
        [i.setDefaultInstrumentType(tmpDict[i.name]) if i.name in tmpDict.keys() else i.setDefaultInstrumentType('') for i in self.all]

    def commit(self,targetProjectPath = ''):
        from RiskQuantLib.Build.buildInstrument import clearInstrumentPath
        from RiskQuantLib.Build.buildShortcut import buildShortcut,commitShortcut,clearShortcut
        clearInstrumentPath(targetProjectPath)
        [i.commit(targetProjectPath) for i in self.all]
        clearShortcut(targetProjectPath)
        shortcut = buildShortcut([i.name for i in self.all])
        commitShortcut(shortcut,targetProjectPath)














