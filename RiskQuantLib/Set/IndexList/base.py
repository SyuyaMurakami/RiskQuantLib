#!/usr/bin/python
#coding = utf-8
import numpy as np
class setBase:

    def setIssuer(self,codeSeries,issuerSeries):
        issuerDict = dict(zip(codeSeries,issuerSeries))
        [i.setIssuer(issuerDict[i.code]) if i.code in issuerDict.keys() else i.setIssuer('') for i in self.all]


    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here
    #-<Begin>
    #-<End>