#!/usr/bin/python
#coding = utf-8

class average:
    """
    This is the base class of average. Inherit from this class will make
    attribute into the average version.
    """
    def __init__(self,numberOfSamplesNum):
        self.numberOfSamples = numberOfSamplesNum

    def setNumberOfSamples(self,numberOfSamplesNum):
        self.numberOfSamples = numberOfSamplesNum

