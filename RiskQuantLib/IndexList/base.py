#!/usr/bin/python
#coding = utf-8
from RiskQuantLib.Index.base import base as index
from QuantLib import Index
from RiskQuantLib.Set.IndexList.base import setBase
from RiskQuantLib.Operation.listBaseOperation import listBase

class baseList(Index,setBase,listBase):
    """
    This class the list of index.
    """
    elementClass = index
    def __init__(self):
        self.all = []
        self.listType = 'Index List'
        self.__init_get_item__()

    def addIndexList(self,indexObjList:list):
        """
        Add bundles of index into this list.
        """
        tmpList = self.all + indexObjList
        self.setAll(tmpList)

    def addIndex(self,indexCodeString:str,indexNameString:str,indexTypeString:str = 'Index'):
        """
        Add a single index object into this list.
        """
        tmpList = self.all + [index(indexCodeString,indexNameString,indexTypeString)]
        self.setAll(tmpList)

    def addIndexSeries(self,indexCodeSeries,indexNameSeries,indexTypeString = 'Index'):
        """
        Add a series of index into this list.
        """
        tmpList = self.all + [index(i,j,indexTypeString) for i,j in zip(indexCodeSeries,indexNameSeries)]
        self.setAll(tmpList)














