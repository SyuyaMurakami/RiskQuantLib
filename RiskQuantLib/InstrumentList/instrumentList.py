#!/usr/bin/python
# coding = utf-8
import numpy as np
import pandas as pd
from RiskQuantLib.Instrument.instrument import instrument
from RiskQuantLib.Operation.operation import operation
from RiskQuantLib.Auto.InstrumentList.instrumentList import instrumentListAuto
#<import>
#</import>

class instrumentList(operation, instrumentListAuto):
    """
    This is the basic list class. Any instrument list class should inherit from this.
    """
    __elementClass__ = instrument

    #<init>
    def __init__(self):
        self.all = []
        self.listType = 'Instrument List'
    #</init>

    #<addList>
    def addInstrumentList(self, instrumentObjList):
        tmpList = self.all + instrumentObjList
        self.setAll(tmpList)
    #</addList>

    #<add>
    def addInstrument(self, instrumentCodeString, instrumentNameString, instrumentTypeString=''):
        tmpList = self.all + [instrument(instrumentCodeString, instrumentNameString, instrumentTypeString)]
        self.setAll(tmpList)
    #</add>

    #<addSeries>
    def addInstrumentSeries(self, instrumentCodeSeries, instrumentNameSeries, instrumentTypeString=''):
        instrumentSeries = [instrument(i, j, instrumentTypeString) for i, j in zip(instrumentCodeSeries, instrumentNameSeries)]
        tmpList = self.all + instrumentSeries
        self.setAll(tmpList)
    #</addSeries>

    #<instrumentList>
    #</instrumentList>