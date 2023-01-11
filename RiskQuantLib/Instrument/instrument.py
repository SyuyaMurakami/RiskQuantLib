#!/usr/bin/python
#coding = utf-8
import numpy as np
import pandas as pd
from QuantLib import Instrument
from RiskQuantLib.Auto.Instrument.instrument import instrumentAuto

class instrument(Instrument,instrumentAuto):
    """
    This is the instrument basic class. Any instrument should inherit from this class.
    """
    def __init__(self,codeString,nameString,instrumentTypeString = 'Instrument'):
        self.code = codeString
        self.name = nameString
        self.instrumentType = instrumentTypeString

    def __getitem__(self, item):
        return getattr(self,item,np.nan)

    def __str__(self):
        return self.code

    def iniPricingModule(self,*args):
        Instrument.__init__(self,*args)

    #<instrument>
    #</instrument>
