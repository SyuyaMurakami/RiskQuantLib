#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Build.buildInstrument import *

class instrumentObj():

    def __init__(self,instrumentNameString):
        self.name = instrumentNameString
        self.parentRQLClassName = ''
        self.parentQuantLibClassName = ''
        self.libraryName = ''
        self.defaultInstrumentType = ''

    def setInstrumentName(self,instrumentNameString):
        self.name = instrumentNameString

    def setParentRQLClassName(self,parentRQLClassNameString):
        if parentRQLClassNameString.find(',')!=-1:
            self.parentRQLClassName = parentRQLClassNameString.split(',')
        else:
            self.parentRQLClassName = parentRQLClassNameString

    def setParentQuantLibClassName(self,parentQuantLibClassNameString):
        if parentQuantLibClassNameString.find(',')!=-1:
            self.parentQuantLibClassName = parentQuantLibClassNameString.spit(',')
        else:
            self.parentQuantLibClassName = parentQuantLibClassNameString
            
    def setLibraryName(self,libraryNameString):
        if libraryNameString.find(',')!=-1:
            self.libraryName = libraryNameString.spit(',')
        else:
            self.libraryName = libraryNameString

    def setDefaultInstrumentType(self,defaultInstrumentTypeString):
        self.defaultInstrumentType = defaultInstrumentTypeString

    def commit(self, targetProjectPath = ''):
        buildInstrument(self.name,self.parentRQLClassName,self.parentQuantLibClassName,self.libraryName,self.defaultInstrumentType,targetProjectPath)














