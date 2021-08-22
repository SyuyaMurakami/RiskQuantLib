#!/usr/bin/python
#coding = utf-8
import numpy as np
import pandas as pd
from RiskQuantLib.Set.Security.Bond.bond import setBond

class setBondIndexUnderlyingBond(setBond):

    def setWeight(self,weightNum,weightDateTimeStamp = pd.Timestamp.now()):
        from RiskQuantLib.Property.Weight.weight import weight
        if not hasattr(self,'__weight'):
            self.__weight = weight(weightNum)
            self.weight = self.__weight.value
        else:
            self.__weight.setValue(weightNum)
            self.weight = self.__weight.value
        self.__weight.setEffectiveDate(weightDateTimeStamp)

    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here
    #-<Begin>
    #-<End>