#!/usr/bin/python
#coding = utf-8

class base:
    """
    This is the basic class of any attribute, except string. Any attribute
    should have an effective date.
    """
    def __init__(self,value):
        self.value = value

    def setValue(self,value):
        self.value = value

    def setEffectiveDate(self,effectiveDateTimeStamp):
        self.effectiveDate = effectiveDateTimeStamp


