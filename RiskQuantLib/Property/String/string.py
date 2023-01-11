#!/usr/bin/python
#coding = utf-8
from RiskQuantLib.Property.property import property
class string(property):
    """
    string is an attribute type class, used as terminal nodes of data graph. It represents the type of data.
    """

    def __init__(self, value):
        super(string,self).__init__(value)

    #<string>
    #</string>
