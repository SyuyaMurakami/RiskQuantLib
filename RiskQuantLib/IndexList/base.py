#!/usr/bin/python
#coding = utf-8
from RiskQuantLib.Index.base import base as index
from QuantLib import Index
from RiskQuantLib.Set.IndexList.base import setBase
from RiskQuantLib.Operation.listBaseOperation import listBase

class base(Index,setBase,listBase):
    def __init__(self):
        self.all = []
        self.__init_get_item__()

    def addIndexList(self,indexObjList):
        tmpList = self.all + indexObjList
        self.setAll(tmpList)

    def addIndex(self,indexCodeString,indexNameString,indexTypeString = 'Index'):
        tmpList = self.all + [index(indexCodeString,indexNameString,indexTypeString)]
        self.setAll(tmpList)

    def addIndexSeries(self,indexCodeSeries,indexNameSeries,indexTypeString = 'Index'):
        tmpList = self.all + [index(i,j,indexTypeString) for i,j in zip(indexCodeSeries,indexNameSeries)]
        self.setAll(tmpList)














