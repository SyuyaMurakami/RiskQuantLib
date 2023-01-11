#!/usr/bin/python
#coding = utf-8
import numpy as np
import pandas as pd
from QuantLib import Instrument
from RiskQuantLib.Auto.Instrument.instrument import instrumentAuto
#<import>
#</import>

class instrument(Instrument,instrumentAuto):
    """
    This is the instrument basic class. Any instrument should inherit from this class.
    """
    #<init>
    def __init__(self,codeString,nameString,instrumentTypeString = 'Instrument'):
        self.code = codeString
        self.name = nameString
        self.instrumentType = instrumentTypeString
    #</init>

    #<getitem>
    def __getitem__(self, item):
        return getattr(self,item,np.nan)
    #</getitem>

    #<str>
    def __str__(self):
        return self.code
    #</str>

    #<initQuantLib>
    def iniPricingModule(self,*args):
        Instrument.__init__(self,*args)
    #</initQuantLib>

    #<instrument>
    #</instrument>
