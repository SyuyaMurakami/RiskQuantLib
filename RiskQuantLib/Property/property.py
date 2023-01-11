#!/usr/bin/python
#coding = utf-8

#<import>
#</import>

class property(object):
    """
    This is the basic class of any kind of attribute, except string. Any attribute
    should have an effective date.
    """
    #<init>
    def __init__(self,value):
        self.value = value
        self.belongToObject = None
        self.belongToAttrName = ''
    #</init>

    #<setBelongTo>
    def setBelongTo(self,belongToObject,belongToAttrName:str):
        self.belongToObject = belongToObject
        self.belongToAttrName = belongToAttrName
    #</setBelongTo>

    #<commit>
    def commit(self):
        if getattr(self,'belongToObject',None) and getattr(self,'belongToAttrName','')!='':
            setattr(self.belongToObject,self.belongToAttrName,self.value)
    #</commit>

    #<setValue>
    def setValue(self,value):
        self.value = value
    #</setValue>

    #<setEffectiveDate>
    def setEffectiveDate(self,effectiveDateTimeStamp):
        self.effectiveDate = effectiveDateTimeStamp
    #</setEffectiveDate>

    #<property>
    #</property>
