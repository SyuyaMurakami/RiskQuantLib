#!/usr/bin/python
#coding = utf-8
import numpy as np
import copy
import multiprocessing as mp

import pandas as pd
from joblib import Parallel,delayed
from RiskQuantLib.Operation.loc import loc
from RiskQuantLib.Tool.strTool import changeSecurityListToStr

class listBase():

    def setAll(self,List):
        self.all = List
        self.__init_get_item__()

    def __getitem__(self, item):
        if type(item) == type(''):
            try:
                return [i for i in self.all if i.code == item][0]
            except Exception as e:
                return [getattr(i,item,np.nan) for i in self.all]
        elif isinstance(item,slice) or isinstance(item,int):
            return self.all[item]
        else:
            tmpList = [i for i in self.all if i.code in item]
            if len(tmpList)!=0:
                return tmpList
            else:
                propertyArray = [[getattr(i, j, np.nan) for i in self.all] for j in item]
                return dict(zip(item,propertyArray))

    def __iter__(self):
        self.__iterNum = 0
        return self

    def __next__(self):
        try:
            target = self.all[self.__iterNum]
            self.__iterNum += 1
            return target
        except:
            raise StopIteration

    def __add__(self, other, useObj = True):
        if useObj:
            tmpObj = copy.deepcopy(self)
            if type(other) == type([]):
                tmpObj.setAll(self.all + other)
            else:
                tmpObj.setAll(self.all + other.all)
            return tmpObj
        else:
            if type(other) == type([]):
                return self.all + other
            else:
                return self.all + other.all

    def __sub__(self, other, useObj = True):
        if useObj:
            tmpObj = copy.deepcopy(self)
            if type(other) == type([]):
                tmpObj.setAll([i for i in self.all if i not in other])
            else:
                tmpObj.setAll([i for i in self.all if i not in other.all])
            return tmpObj
        else:
            if type(other) == type([]):
                return [i for i in self.all if i not in other]
            else:
                return [i for i in self.all if i not in other.all]

    def __str__(self):
        try:
            return changeSecurityListToStr(self['code'])
        except:
            return ''

    def __len__(self):
        return len(self.all)

    def _sortIterator(self,sortObj):
        import pandas as pd
        sortList = [getattr(sortObj,i) if type(getattr(sortObj,i))!=type(pd.Series()) else len(getattr(sortObj,i)) for i in self._sortPropertyList]
        return tuple(sortList)

    def add(self,other, useObj = True):
        a = self.copy(deep=True)
        b = other.copy(deep=True)
        if useObj:
            return a+b
        else:
            return (a+b).all

    def sub(self, other, useObj=True):
        a = self.copy(deep=True)
        b = other.copy(deep=True)
        if useObj:
            return a - b
        else:
            return (a - b).all

    def uniqueCode(self,inplace = False, keep = 'First'):
        codeList = list(set([i.code for i in self.all]))
        if keep == 'First':
            keepIndex = 0
        elif keep == 'Last':
            keepIndex = -1
        else:
            print("uniqueCode Function Can Only Accept 'Keep' Parameter as First or Last")
            return None
        if inplace:
            self.setAll([[j for j in self.all if j.code == i][keepIndex] for i in codeList])
            return None
        else:
            return [[j for j in self.all if j.code == i][keepIndex] for i in codeList]

    def uniqueAttr(self,attrNameString,inplace = False, keep = 'First'):
        propertyValueList = list(set([getattr(i,attrNameString,np.nan) for i in self.all if hasattr(i,attrNameString)]))
        if keep == 'First':
            keepIndex = 0
        elif keep == 'Last':
            keepIndex = -1
        else:
            print("uniqueAttr Function Can Only Accept 'Keep' Parameter as First or Last")
            return None
        if inplace:
            self.setAll([[j for j in self.all if getattr(j,attrNameString) == i][keepIndex] for i in propertyValueList])
            return None
        else:
            return [[j for j in self.all if getattr(j,attrNameString) == i][keepIndex] for i in propertyValueList]

    def apply(self,applyFunction,*args):
        return Parallel(n_jobs=mp.cpu_count())(delayed(applyFunction)(i,*args) for i in self.all)

    def groupBy(self, attrName, useObj = True, inplace = True):
        if type(attrName) == type(''):
            attrName = [attrName]
        else:
            pass

        groupBy = pd.DataFrame(self[attrName+['index']])
        groupBy['obj'] = self.all
        df = groupBy.groupby(attrName)['obj']

        attrValueList = [[j for j in i] if type(i)==type(tuple()) else [i] for i in df.groups.keys()]
        securityList = [df.get_group(i).to_list() for i in df.groups.keys()]
        if useObj:
            if inplace:
                objList = [self.__new__(type(self)) for i in attrValueList]
                [i.__init__() for i in objList]
            else:
                objList = [self.copy(deep=True) for i in attrValueList]
            [i.setAll(j) for i,j in zip(objList,securityList)]
            [[setattr(j,attrName[q],i[q]) for q in range(len(attrName))] for i,j in zip(attrValueList,objList)]
            returnObj = self.__new__(type(self))
            returnObj.__init__()
            returnObj.setAll(objList)
            return returnObj
        else:
            return dict(zip(attrValueList,securityList))

    def sum(self,attrName,inplace = False):
        if inplace:
            setattr(self,attrName+'Sum',np.nansum([getattr(i,attrName,np.nan) for i in self.all]))
            return None
        else:
            return np.nansum([getattr(i,attrName,np.nan) for i in self.all])

    def mean(self,attrName,inplace=False):
        if inplace:
            setattr(self,attrName+'Mean',np.nanmean([getattr(i,attrName,np.nan) for i in self.all]))
            return None
        else:
            return np.nanmean([getattr(i,attrName,np.nan) for i in self.all])

    def std(self,attrName,inplace=False):
        if inplace:
            setattr(self,attrName+'Std',np.nanstd([getattr(i,attrName,np.nan) for i in self.all]))
            return None
        else:
            return np.nanstd([getattr(i,attrName,np.nan) for i in self.all])

    def execFunc(self,functionName,*args):
        try:
            if len(self.all)<1000:
                result = [getattr(i,functionName,lambda x:None)(*args) for i in self.all]
            else:
                result = Parallel(n_jobs=mp.cpu_count(),require='sharedmem')(delayed(getattr(i,functionName,lambda x:None))(*args) for i in self.all)
            return result
        except Exception as e:
            print('Execution Failed:', e)
            pass


    def copy(self,deep = True):
        if deep:
            tmp = copy.deepcopy(self)
            tmp.__init_get_item__()
            return tmp
        else:
            tmp = copy.copy(self)
            tmp.__init_get_item__()
            return tmp

    def sort(self,propertyList,reverse = False,inplace=False, useObj = True):
        if type(propertyList)!=type([]):
            self._sortPropertyList = [propertyList]
        else:
            self._sortPropertyList = propertyList
        if inplace:
            self.setAll(sorted(self.all,key=self._sortIterator,reverse=reverse))
            return None
        elif useObj:
            tmpObj = copy.deepcopy(self)
            tmpObj.setAll(sorted(self.all,key=self._sortIterator,reverse=reverse))
            return tmpObj
        else:
            return sorted(self.all,key=self._sortIterator,reverse=reverse)

    def fillna(self, propertyList, value, inplace=False, useObj = True):
        from RiskQuantLib.Tool.mathTool import isnan
        if type(propertyList)!=type([]):
            propertyList = [propertyList]
        else:
            pass
        if inplace:
            [[getattr(j,'set'+i[0].capitalize()+i[1:])(value) if hasattr(j,'set'+i[0].capitalize()+i[1:]) and (isnan(getattr(j,i)) or getattr(j, i)=='') else None for j in self.all if hasattr(j,i)] for i in propertyList]
            [[setattr(j,i,value) if hasattr(j, i) and (isnan(getattr(j, i)) or getattr(j, i)=='') else None for j in self.all if hasattr(j, i)] for i in propertyList]
        elif useObj:
            tmpObj = self.copy(deep=True)
            [[getattr(j,'set'+i[0].capitalize()+i[1:])(value) if hasattr(j,'set'+i[0].capitalize()+i[1:]) and (isnan(getattr(j,i)) or getattr(j, i)=='') else None for j in tmpObj.all if hasattr(j,i)] for i in propertyList]
            [[setattr(j,i,value) if hasattr(j, i) and (isnan(getattr(j, i)) or getattr(j, i)=='') else None for j in tmpObj.all if hasattr(j, i)] for i in propertyList]
            return tmpObj
        else:
            tmpList = copy.deepcopy(self.all)
            [[getattr(j,'set'+i[0].capitalize()+i[1:])(value) if hasattr(j,'set'+i[0].capitalize()+i[1:]) and (isnan(getattr(j,i)) or getattr(j, i)=='') else None for j in tmpList if hasattr(j,i)] for i in propertyList]
            [[setattr(j,i,value) if hasattr(j, i) and (isnan(getattr(j, i)) or getattr(j, i)=='') else None for j in tmpList if hasattr(j, i)] for i in propertyList]
            return tmpList

    def __init_get_item__(self):
        self.loc = loc(self.all)
        pass

    def __set_number_index__(self):
        [setattr(i,'numberIndex',j) for j,i in enumerate(self.all)]

    def setIndex(self, propertyNameString, inplace = True):
        if inplace:
            [i.setIndex(getattr(i,propertyNameString,np.nan)) for i in self.all]
            return None
        else:
            tmpObj = self.copy(deep=True)
            [i.setIndex(getattr(i,propertyNameString,np.nan)) for i in tmpObj.all]
            return tmpObj

    def dropIndex(self, inplace=True):
        if inplace:
            [delattr(i,'index') for i in self.all]
            return None
        else:
            tmpObj = self.copy(deep=True)
            [delattr(i,'index') for i in tmpObj.all]
            return tmpObj

    def reIndex(self, indexList, useObj = True, inplace = False):
        tmpList = [[j for j in self.all if j.index == i][0] for i in indexList]
        if inplace:
            self.setAll(tmpList)
            return None
        elif useObj:
            tmpObj = self.copy(deep=True)
            tmpObj.setAll(tmpList)
            return tmpObj
        else:
            return tmpList

    def resetIndex(self, inplace = True):
        if inplace:
            [j.setIndex(i) for i,j in enumerate(self.all)]
            return None
        else:
            tmpObj = self.copy(deep=True)
            [j.setIndex(i) for i, j in enumerate(tmpObj.all)]
            return tmpObj

    def str(self):
        return self.__str__()


    def rolling(self,windowNumber:int,useObj = True):
        rollingList = [self[max((i-windowNumber+1),0):(i+1)] for i in range(len(self))]
        if useObj:
            rollingObj = [self.__new__(type(self)) for i in range(len(self))]
            [i.__init__() for i in rollingObj]
            [i.setAll(j) for i,j in zip(rollingObj,rollingList)]
            [setattr(i,'_rolling',j) for i,j in zip(self.all,rollingObj)]
            [setattr(i, '_rolling_window', windowNumber) for i in self.all]
            returnObj = self.__new__(type(self))
            returnObj.__init__()
            returnObj.setAll(rollingObj)
            return returnObj
        else:
            return rollingList

    def new(self):
        tmpObj = self.__new__(type(self))
        tmpObj.__init__()
        return tmpObj

    def filter(self,filterFunction,useObj = True):
        resultList = [i for i in self.all if filterFunction(i)]
        if useObj:
            tmpObj = self.new()
            tmpObj.setAll(resultList)
            return tmpObj
        else:
            return resultList

    def join(self,anotherList,targetAttrName,filterFunction = lambda x,y:True):
        valueList = [[another for another in anotherList.all if filterFunction(this,another)] for this in self.all]
        valueObj = [anotherList.new() for i in self.all]
        [obj.setAll(value) for obj,value in zip(valueObj,valueList)]
        [setattr(i,targetAttrName,j) for i,j in zip(self.all,valueObj)]

    def scale(self,attrName,targetAttrName = '',filterFunction = lambda x:True,inplace = False):
        if targetAttrName=='':
            targetAttrName = 'scaled_'+attrName
        total = self.sum(attrName)
        objList = [i for i in self.all if filterFunction(i)]
        scaled = [getattr(i,attrName,np.nan)/total for i in objList]
        if inplace:
            [setattr(obj,targetAttrName,scaledValue) for obj,scaledValue in zip(self.all,scaled)]
        else:
            tmpObj = self.new()
            tmpObj.setAll(objList)
            [setattr(obj, targetAttrName, scaledValue) for obj, scaledValue in zip(tmpObj.all, scaled)]
            return tmpObj