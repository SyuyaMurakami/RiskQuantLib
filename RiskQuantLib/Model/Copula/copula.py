#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Model.model import model

class copula(model):
    """
    Generate new samples following the same correlation relation, given a series of data.
    """
    def __init__(self,array):
        from copula import pyCopula
        super(copula,self).__init__()
        self.cop = pyCopula.Copula(array)

    def generateSimulatedSample(self,numberOfSimulation):
        self.simulatedSamples = self.cop.gendata(numberOfSimulation)
        return self.simulatedSamples

    #<copula>
    #</copula>

class copulae(model):
    """
    Generate new samples, given correlation matrix.
    """
    def __init__(self,dfCorrelation):
        from copulae import GaussianCopula
        super(copulae,self).__init__()
        self.cop = GaussianCopula(dfCorrelation.shape[1])
        self.cop[:] = dfCorrelation.values

    def generateSimulatedSample(self,numberOfSimulation):
        self.simulatedSamples = self.cop.random(numberOfSimulation)
        return self.simulatedSamples

    #<copulae>
    #</copulae>












