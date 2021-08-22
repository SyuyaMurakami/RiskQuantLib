#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Model.base import base
from copula import pyCopula
from copulae import GaussianCopula

class copula(base):
    def __init__(self,array):
        super(copula,self).__init__()
        self.cop = pyCopula.Copula(array)

    def generateSimulatedSample(self,numberOfSimulation):
        self.simulatedSamples = self.cop.gendata(numberOfSimulation)
        return self.simulatedSamples

class copulae(base):
    def __init__(self,dfCorrelation):
        super(copulae,self).__init__()
        self.cop = GaussianCopula(dfCorrelation.shape[1])
        self.cop[:] = dfCorrelation.values

    def generateSimulatedSample(self,numberOfSimulation):
        self.simulatedSamples = self.cop.random(numberOfSimulation)
        return self.simulatedSamples














