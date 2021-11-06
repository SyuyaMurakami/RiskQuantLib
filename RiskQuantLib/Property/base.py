#!/usr/bin/python
#coding = utf-8

class base:
    """
    This is the basic class of any kind of attribute, except string. Any attribute
    should have an effective date.
    """
    def __init__(self,value):
        self.value = value
        self.belongToObject = None
        self.belongToAttrName = ''

    def setBelongTo(self,belongToObject,belongToAttrName:str):
        self.belongToObject = belongToObject
        self.belongToAttrName = belongToAttrName

    def commit(self):
        if getattr(self,'belongToObject',None) and getattr(self,'belongToAttrName','')!='':
            setattr(self.belongToObject,self.belongToAttrName,self.value)

    def setValue(self,value):
        self.value = value

    def setEffectiveDate(self,effectiveDateTimeStamp):
        self.effectiveDate = effectiveDateTimeStamp


