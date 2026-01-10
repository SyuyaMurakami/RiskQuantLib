#!/usr/bin/python
#coding = utf-8
import sys
import copy
import traceback
import numpy as np
import pandas as pd
from collections.abc import Iterable
from RiskQuantLib.Operation.vectorization import vectorization

#<import>
#</import>

class operation(object):
    """
    operation() is the function class that makes all RiskQuantLib list object functional.
    Any RiskQuantLib list class should inherit from this class to own certain functions,
    such as groupBy, execFunc, etc.

    Users can define their own functions here to set new attribute function to
    RiskQuantLib list class.
    """

    def setAll(self,List:list):
        """
        Update all elements by the list of new elements. Old elements will be deleted.

        Parameters
        ----------
        List : list
            A collection of RiskQuantLib instrument objects.

        Returns
        -------
        None
        """
        self.all = List

    def _tunnelingGetitem(self, attrName):
        """
        Find the attribute of elements in present list which meet requirements and
        find elements of that attribute, if it is iterable. If this attribute
        is not iterable, it returns collection of this attribute itself.
        """
        subIndex = None
        if type(attrName)==type(''):
            filter = lambda x:True
        elif type(attrName)==type(()) and len(attrName)==2:
            if hasattr(attrName[1],"__call__"):
                filter = attrName[1]
            else:
                filter = lambda x: True
                subIndex = attrName[1]
            attrName = attrName[0]
        elif type(attrName)==type(()) and len(attrName)>=3:
            if hasattr(attrName[1],"__call__"):
                filter = attrName[1]
                subIndex = attrName[2]
            else:
                filter = attrName[2]
                subIndex = attrName[1]
            attrName = attrName[0]
        else:
            attrName = attrName[0]
            filter = lambda x:True
        if (not type(subIndex)==type(None)) or subIndex:
            try:
                tmp = [getattr(i,attrName) for i in self.all if hasattr(i, attrName)]
                thisLayer = sorted(set(tmp),key=tmp.index)
            except:
                thisLayer = [getattr(i, attrName) for i in self.all if hasattr(i, attrName)]
            if type(subIndex) == slice:
                try:
                    tmp = [j for i in thisLayer if hasattr(i,'__getitem__') for j in i[subIndex] if isinstance(i[subIndex],Iterable)]
                    nextLayer = sorted(set(tmp),key=tmp.index)
                except:
                    nextLayer = [j for i in thisLayer if hasattr(i,'__getitem__') for j in i[subIndex] if isinstance(i[subIndex],Iterable)]
            else:
                nextLayer = [i[subIndex] if hasattr(i,'__getitem__') else i for i in thisLayer]
            if len(nextLayer)==0:
                tmp = operation()
                tmp.setAll([i for i in thisLayer if filter(i)])
                return tmp
            else:
                tmp = operation()
                tmp.setAll([i for i in nextLayer if filter(i)])
                return tmp
        else:
            tmp = operation()
            thisLayer = [getattr(i, attrName,np.nan) for i in self.all]
            tmp.setAll([i for i in thisLayer if filter(i)])
            return tmp
    def __getitem__(self, item):
        """
        This function makes RiqkQuantLib list object selectable. Use [] to call this function.
        Mixed index is used here. By calling [], you can index either element or attribute, or
        elements of attribute.

        Parameters
        ----------
        item : str or list or slice or tuple
            If a string is given, all elements will be examined, if 'code' attribute equals
            to the given string, return the first element that meets this requirement.

            If no element code meets this requirement, try to return a operation object,
            holding values of attribute whose name equals to the given string.

            If a slice or int number is given, this function behaves like iloc, returns the
            item-th element or a collection of elements.

            If a list is given, return all elements whose code in the given list. If no code
            in the given list, return a 2-dimension array of attribute values, where attribute
            name is in the given list.

            If a tuple is given, it returns a operation object, but the elements of this object
            depends on how you specify your parameter. For the first element of tuple, it must be
            a string, specify the attribute you want to choose.

            For the second element of tuple, you can pass a lambda function or any
            function into tuple, if you do this, the function will be used to filter your results.

            For the second element of tuple, you can also pass a slice. If you pass a slice into
            tuple, RiskQuantLib will assume the attribute value is iterable, and again, get the
            element of the attribute with this slice.

            If you want to select some elements of the attribute, and do it for every element of
            present list, and filter your result. You may pass a slice and a function at the same
            time. In this case, your tuple has three elements.

        Returns
        -------
        None
        """
        if type(item) == type(''):
            try:
                return [i for i in self.all if i.code == item][0]
            except Exception as e:
                return self._tunnelingGetitem(item)
        elif isinstance(item,tuple):
            return self._tunnelingGetitem(item)
        elif isinstance(item,int):
            return self.all[item]
        elif isinstance(item,slice):
            tmp = operation()
            tmp.setAll(self.all[item])
            return tmp
        else:
            tmpList = [i for i in self.all if hasattr(i, 'code') and i.code in item]
            if len(tmpList)!=0:
                tmp = operation()
                tmp.setAll(tmpList)
                return tmp
            else:
                propertyArray = [[getattr(i, j, np.nan) for i in self.all] for j in item]
                return dict(zip(item,propertyArray))

    def __iter__(self):
        i = 0
        try:
            while True:
                v = self.all[i]
                yield v
                i += 1
        except IndexError:
            return

    def __add__(self, other, useObj = True):
        """
        Add a RiskQuantLib list object to a list or another RiskQuantLib list object.
        All attributes of the RiskQuantLib list will be neglected, only elements will be added to
        the merged list.

        This use shallow copy. After add finish, all elements refer to the original
        elements. Change to the original will render to changes of the results. If
        you want to use a deep copy add, call '.add()' rather than use '+'.

        Parameters
        ----------
        other : list or RiskQuantLib list
            The other RiskQuantLib list object or a collection of RiskQuantLib instrument object.
        useObj : bool
            If true, return a RiskQuantLib list object; if false, return a list.

        Returns
        -------
        list or RiskQuantLib list
        """
        if useObj:
            tmpObj = self.new()
            if type(other) is list:
                tmpObj.setAll(self.all + other)
            else:
                tmpObj.setAll(self.all + other.all)
            return tmpObj
        else:
            if type(other) is list:
                return self.all + other
            else:
                return self.all + other.all

    def __sub__(self, other, useObj = True):
        """
        Subtract a list or another RiskQuantLib list object from a RiskQuantLib list object.
        All attributes of the RiskQuantLib list will be neglected, only elements will be subtracted
        from the first list.

        This use shallow copy. After sub finish, all elements refer to the original
        elements. Change to the original will render to changes of the results. If
        you want to use a deep copy sub, call '.sub()' rather than use '-'.

        Parameters
        ----------
        other : list or RiskQuantLib list
            The other RiskQuantLib list object or a collection of RiskQuantLib instrument object.
        useObj : bool
            If true, return a RiskQuantLib list object; if false, return a list.

        Returns
        -------
        list or RiskQuantLib list
        """
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
        """
        This returns a list of string, showing the code of each element.
        """
        try:
            return ','.join(self['code'])
        except:
            return ''

    def __len__(self):
        """
        This function returns the length of RiskQuantLib list.
        """
        return len(self.all)

    def _sortIterator(self,sortObj):
        import pandas as pd
        sortList = [getattr(sortObj,i) if type(getattr(sortObj,i))!=type(pd.Series(dtype=float)) else len(getattr(sortObj,i)) for i in self._sortPropertyList]
        return tuple(sortList)

    def add(self,other, useObj = True):
        """
        This function uses deep copy. It returns the addition of copies of two RiskQuantLib lists.
        """
        a = self.copy(deep=True)
        b = other.copy(deep=True)
        if useObj:
            return a+b
        else:
            return (a+b).all

    def sub(self, other, useObj=True):
        """
        This function uses deep copy. It returns the subtraction of copies of two RiskQuantLib lists.
        """
        a = self.copy(deep=True)
        b = other.copy(deep=True)
        if useObj:
            return a - b
        else:
            return (a - b).all

    def uniqueCode(self,inplace = False, keep = 'First'):
        """
        This function returns a RiskQuantLib list object, where the code value
        is unique.

        Parameters
        ----------
        inplace : bool
            If true, operation will done in present list object.
            If false, operation will done in a copy of present list object.
        keep : str
            Only support 'First' or 'Last'. If multiple elements have the same
            code value. The first or last element will be kept, given your choice.

        Returns
        -------
        RiskQuantLib list object
        """
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
            result = self.new()
            result.setAll([[j for j in self.all if j.code == i][keepIndex] for i in codeList])
            return result

    def uniqueAttr(self,attrNameString:str,inplace = False, keep = 'First'):
        """
        This function returns a RiskQuantLib list object, where the attribute value
        is unique.

        Parameters
        ----------
        attrNameString :str
            The attribute name that you want to get the unique value list from.
        inplace : bool
            If true, operation will done in present list object.
            If false, operation will done in a copy of present list object.
        keep : str
            Only support 'First' or 'Last'. If multiple elements have the same
            attribute value. The first or last element will be kept, given your choice.

        Returns
        -------
        RiskQuantLib list object
        """
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
            result = self.new()
            result.setAll([[j for j in self.all if getattr(j,attrNameString) == i][keepIndex] for i in propertyValueList])
            return result

    def apply(self,applyFunction,*args):
        """
        This function will apply the given function to each element of RiskQuantLib list.
        """
        result = [applyFunction(i,*args) for i in self.all]
        tmp = operation()
        tmp.setAll(result)
        return tmp

    def groupBy(self, attrName:str, useObj = True, inplace = True):
        """
        This function use pandas.DataFrame.groupby as engine. Its behavior is totally
        the same with pandas.

        Parameters
        ----------
        attrName : str
            The attribute that you want to group data by.
        useObj : bool
            If true, return a RiskQuantLib list object, each element of which is also a
            RiskQuantLib list object. Each element will be marked by setting the attribute
            as the common value.
        inplace : bool
            If true, operation will be done in present RiskQuantLib list object.
        """
        if type(attrName) == type(''):
            attrName = [attrName]
        else:
            pass

        groupBy = pd.DataFrame(self[attrName+['index']])
        groupBy['obj'] = self.all
        df = groupBy.groupby(attrName)['obj']

        kvList = [([j for j in k] if type(k) is tuple else [k], v.to_list()) for k, v in df]
        attrValueList = [i[0] for i in kvList]
        securityList = [i[1] for i in kvList]

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

    def groupByFunc(self, func, useObj = True, inplace = True):
        """
        This function use pandas.DataFrame.groupby as engine. Its behavior is totally
        the same with pandas.

        Parameters
        ----------
        func : function
            Elements will be divided into groups by the return values of this function.
        useObj : bool
            If true, return a RiskQuantLib list object, each element of which is also a
            RiskQuantLib list object. Each element will be marked by setting the attribute
            as the common value.
        inplace : bool
            If true, operation will be done in present RiskQuantLib list object.
        """
        attrValue = self.apply(func)
        groupBy = attrValue.toDF()
        groupBy.columns = [i if type(i)==str else "groupByAttr"+str(i) for i in groupBy.columns]
        attrName = groupBy.columns.to_list()
        groupBy['index'] = self['index']
        groupBy['obj'] = self.all
        df = groupBy.groupby(attrName)['obj']

        kvList = [([j for j in k] if type(k) is tuple else [k], v.to_list()) for k, v in df]
        attrValueList = [i[0] for i in kvList]
        securityList = [i[1] for i in kvList]

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

    def sum(self,attrName:str,inplace = False):
        """
        This function will sum the value of each element, given the attribute name.
        If some elements don't have the attribute, an numpy.nan will be used, and
        the result will skip this value.

        Parameters
        ----------
        attrName : str
            The attribute name whose value you want to sum.
        inplace : bool
            If true, the 'attributeSum' property will be added to present object.
        """
        if inplace:
            setattr(self,attrName+'Sum',np.nansum([getattr(i,attrName,np.nan) for i in self.all]))
            return None
        else:
            return np.nansum([getattr(i,attrName,np.nan) for i in self.all])

    def mean(self,attrName:str,inplace=False):
        """
        This function will average the value of each element, given the attribute name.
        If some elements don't have the attribute, an numpy.nan will be used, and
        the result will skip this value when calculating mean.

        Parameters
        ----------
        attrName : str
            The attribute name whose value you want to average.
        inplace : bool
            If true, the 'attributeMean' property will be added to present object.
        """
        if inplace:
            setattr(self,attrName+'Mean',np.nanmean([getattr(i,attrName,np.nan) for i in self.all]))
            return None
        else:
            return np.nanmean([getattr(i,attrName,np.nan) for i in self.all])

    def std(self,attrName:str,inplace=False):
        """
        This function will calculate the standard deviation of value of each element,
        given the attribute name. If some elements don't have the attribute, an numpy.nan will be used, and
        the result will skip this value.

        Parameters
        ----------
        attrName : str
            The attribute name whose value you want to calculate standard deviation.
        inplace : bool
            If true, the 'attributeStd' property will be added to present object.
        """
        if inplace:
            setattr(self,attrName+'Std',np.nanstd([getattr(i,attrName,np.nan) for i in self.all]))
            return None
        else:
            return np.nanstd([getattr(i,attrName,np.nan) for i in self.all])

    def execFunc(self,functionName,*args,**kwargs):
        """
        This function will execute instance function for every element in present RiskQuantLib list object,
        given the function name. If some elements don't have the function, a Null function will be used, and
        the result will skip the execution for that element.

        Parameters
        ----------
        functionName : str
            The function that element has, and you want to call.
        """
        try:
            result = [getattr(i,functionName,lambda *arg, **kwarg:None)(*args, **kwargs) for i in self.all]
            tmp = operation()
            tmp.setAll(result)
            return tmp
        except Exception as e:
            print('Execution Failed As Follows:', file=sys.stderr)
            print('Instrument Type:', self.__class__.__name__, file=sys.stderr)
            print('Function Name:', functionName, file=sys.stderr)
            print('Exception Info:', e, file=sys.stderr)
            traceback.print_exc()

    def paraFunc(self, functionName, *args, **kwargs):
        """
        This function will execute instance function for every element in present RiskQuantLib list object by parallel,
        which means elements will be serialized and sent to different processes.

        If some elements don't have the function which named as you specify, a Null function will be used, and
        the result will skip the execution for that element.

        The call will be delayed until you run currentRiskQuantLibList.paraRun().

        Parameters
        ----------
        functionName : str
            The function that element has, and you want to call.

        Returns
        -------
        operation
        """
        self._paraQueue = [] if not hasattr(self, "_paraQueue") else self._paraQueue
        self._paraQueue.append((functionName, args, kwargs))
        return self

    def paraRun(self, nJobs: int = -1):
        """
        This is the trigger of run paralleled function for every element in this RiskQuantLib list. Before you use
        this function, you should call someList.paraFunc('functionName') for more than one time to tell RiskQuantLib
        what function you want to parallel.

        Returns
        -------
        operation
        """
        self._paraQueue = [] if not hasattr(self, "_paraQueue") else self._paraQueue

        def _coll(obj):
            paraTmp = [getattr(obj, functionName, lambda *arg, **kwarg:None)(*args, **kwargs) for functionName,args,kwargs in self._paraQueue]
            return paraTmp

        from joblib import Parallel, delayed

        try:
            result = Parallel(n_jobs=nJobs)(delayed(_coll)(i) for i in self.all)
            tmp = operation()
            tmp.setAll(result)
            self._paraQueue = []
            return tmp
        except Exception as e:
            print('Parallel Failed:', e)
            pass

    def vecApply(self, lambdaFunction=lambda x: None):
        """
        This function is like operation.apply, it will apply the given function to each 
        element of RiskQuantLib list. The passed function should be one-parameter function,
        whose parameter represents the element of current RiskQuantLib list.

        The difference is this function will try to vectorize the calculation to speed up.
        It will convert the attribute to np.array and operate mathematical calculation.

        Notice: Only Pure Mathematic Function can be vectorized, this is to say, any logic key word
        of python, like 'in', 'if', 'for', etc, can Not be used in passed function. If must be pure
        math formula. Luckily, all numpy function can be used. If you want to do some logistic calculation,
        you should make sure you write function as logic-matrix-like.

        Returns
        -------
        operation
        """
        allElement = self.all
        if len(allElement) != 0:
            dynamicClass = type('tmp', (vectorization,), {'lambdaFuncName': lambdaFunction})
            dynamicObj = dynamicClass(allElement)
            result = super(vectorization, dynamicObj).__getattribute__('lambdaFuncName')()
            del dynamicObj, dynamicClass
            return self if result is None else result
        else:
            return self

    def vecFunc(self, functionName, *args, **kwargs):
        """
        This function is like operation.execFunc, it will call the given function of each 
        element of RiskQuantLib list. The passed function should be the attribute function 
        of element of current RiskQuantLib List.

        The difference is this function will try to vectorize the calculation to speed up.
        It will convert the attribute to np.array and operate mathematical calculation.

        Notice: Only Pure Mathematic Function can be vectorized, this is to say, any logic key word
        of python, like 'in', 'if', 'for', etc, can Not be used in passed function. If must be pure
        math formula. Luckily, all numpy function can be used. If you want to do some logistic calculation,
        you should make sure you write function as logic-matrix-like.

        Returns
        -------
        operation
        """
        allElement = self.all
        if len(allElement) != 0:
            functionObj = getattr(type(allElement[0]), functionName, lambda *argsSub, **kwargsSub: None)
            functionObjName = functionName + 'Attribute'
            dynamicClass = type(functionName, (vectorization,), {functionObjName: functionObj})
            dynamicObj = dynamicClass(allElement)
            result = super(vectorization, dynamicObj).__getattribute__(functionObjName)(*args, **kwargs)
            del dynamicObj, dynamicClass
            return self if result is None else result
        else:
            return self

    def copy(self,deep = True):
        """
        Get a copy of present RiskQuantLib list object.
        """
        if deep:
            tmp = copy.deepcopy(self)
            return tmp
        else:
            tmp = copy.copy(self)
            return tmp

    def sort(self,propertyList:list,reverse = False,inplace=False, useObj = True):
        """
        Sort the present RiskQuantLib list by attributes. You can also sort it by a single
        attribute.
        """
        if type(propertyList)!=type([]):
            self._sortPropertyList = [propertyList]
        else:
            self._sortPropertyList = propertyList

        if inplace:
            sortBy = pd.DataFrame(self[self._sortPropertyList])
            sortBy['obj'] = self.all
            df = sortBy.sort_values(by=self._sortPropertyList, ascending=not reverse)
            sortedList = df['obj'].to_list()
            self.setAll(sortedList)
            return None
        elif useObj:
            tmpObj = copy.deepcopy(self)
            sortBy = pd.DataFrame(tmpObj[self._sortPropertyList])
            sortBy['obj'] = tmpObj.all
            df = sortBy.sort_values(by=self._sortPropertyList, ascending=not reverse)
            sortedList = df['obj'].to_list()
            tmpObj.setAll(sortedList)
            return tmpObj
        else:
            sortBy = pd.DataFrame(self[self._sortPropertyList])
            sortBy['obj'] = self.all
            df = sortBy.sort_values(by=self._sortPropertyList, ascending=not reverse)
            return df['obj'].to_list()

    def fillna(self, propertyList:list, value, inplace=False, useObj = True):
        """
        Fill the nan value or blank string will the given value.
        If attribute doesn't exist, nothing will be done.
        You can fill the nan value by single attribute or a list of attributes.
        """
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

    def reIndex(self, attrName: str, indexList: list, useObj: bool = True, inplace: bool = False):
        """
        Return a new RiskQuantLib list object whose elements are chosen according to
        the index, the index of new list element must be in th indexList to be included.
        If more than one elements meet requirement, only the first one will be kept.
        """
        tmpList = [[j for j in self.all if getattr(j, attrName, np.nan) == i][0] for i in indexList]
        if inplace:
            self.setAll(tmpList)
            return None
        elif useObj:
            tmpObj = self.copy(deep=True)
            tmpObj.setAll(tmpList)
            return tmpObj
        else:
            return tmpList

    def str(self):
        return self.__str__()

    def rolling(self, windowNumber: int, useObj: bool = True):
        """
        For each element, This function will collect the n elements before
        that element, create a new RiskQuantLib list object to holding it. The new list
        will be set as an attribute of 'rolling', thus the present element can reach to
        the information of its former elements.
        """
        rollingList = [self[max((i-windowNumber+1),0):(i+1)] for i in range(len(self))]
        if useObj:
            rollingObj = [self.__new__(type(self)) for i in range(len(self))]
            [i.__init__() for i in rollingObj]
            [i.setAll(j) for i,j in zip(rollingObj,rollingList)]
            [setattr(i,'rolling',j) for i,j in zip(self.all,rollingObj)]
            [setattr(i, 'rollingWindow', windowNumber) for i in self.all]
            returnObj = self.__new__(type(self))
            returnObj.__init__()
            returnObj.setAll(rollingObj)
            return returnObj
        else:
            return rollingList

    def new(self):
        """
        Return a totally new RiskQuantLib list object like this.
        """
        tmpObj = self.__new__(type(self))
        tmpObj.__init__()
        return tmpObj

    def filter(self,filterFunction,useObj = True):
        """
        Return a RiskQuantLib list object given the fiter function.
        This is used to choose some elements which meet your requirements.
        """
        resultList = [i for i in self.all if filterFunction(i)]
        if useObj:
            tmpObj = self.new()
            tmpObj.setAll(resultList)
            return tmpObj
        else:
            return resultList

    def head(self, numberOfElement:int):
        """
        Get the first numberOfElement elements of the list.
        """
        return self[:numberOfElement]

    def tail(self, numberOfElement:int):
        """
        Get the last numberOfElement elements of the list.
        """
        return self[(-1 * numberOfElement):]

    def haveAttr(self, attrName):
        """
        Get the elements which have certain attributes, if passed a list, the elements which have all
        attributes in the list will be returned, otherwise an empty list will be returned.
        """
        if type(attrName)==str:
            return self.filter(lambda x:hasattr(x, attrName))
        elif type(attrName)==list:
            return self.filter(lambda x:sum([hasattr(x, i) for i in attrName])==len(attrName))
        else:
            return self.filter(lambda x:False)

    def isIn(self, anotherList):
        """
        Find the elements which are also in the given list. Use these elements to generate a
        new RiskQuantLib list and return it. anotherList can be any iterable object.
        """
        return self.filter(lambda x: x in set(anotherList))

    def isNotIn(self, anotherList):
        """
        Find the elements which are not in the given list. Use these elements to generate a
        new RiskQuantLib list and return it. anotherList can be any iterable object.
        """
        return self.filter(lambda x: x not in set(anotherList))

    def union(self, anotherList):
        """
        Find the elements which are in the given list or in the current list. Use these elements
        to generate a new RiskQuantLib list and return it. anotherList can be any iterable object.
        """
        return self.isNotIn(anotherList) + anotherList

    def match(self, anotherList, targetAttrName: str, matchFunctionOnLeft=lambda x: True, matchFunctionOnRight=lambda y: True):
        """
        For each element in current rqlList, find all elements that meet requirement
        matchFunctionOnRight(element_in_another_list) == matchFunctionOnLeft(element_in_this_list)
        from another RiskQuantLib list object. The elements meeting requirement will be set as an attribute
        of element_in_this_list.

        This function is very like rqlList.join, the only difference is that this function is
        vectorized, thus run with faster speed. Of cause, this function has some drawbacks, it
        can not deal with complicated relation which is described as coupled equation, while
        rqlList.join can do it.

        Parameters
        ----------
        anotherList : RiskQuantLib list or list
            Another list object, holding elements waiting to be selected.
        targetAttrName : str
            The attribute name that you want to use to mark collected elements from another list.
        matchFunctionOnLeft : function
            This function has and only has one parameter, which stands for element in current list.
        matchFunctionOnRight : function
            This function has and only has one parameter, which stands for element in another list.
        """
        anotherMatchArray = np.array([matchFunctionOnRight(another) for another in anotherList])
        thisMatchArray = np.array([matchFunctionOnLeft(this) for this in self.all]).reshape(-1, 1)
        targetObjIDArray = np.apply_along_axis(lambda x: x == anotherMatchArray, 1, thisMatchArray)

        anotherObjIndexArray = np.array(range(len(anotherList.all)))
        matchedValueList = [[anotherList.all[idx] for idx in anotherObjIndexArray[targetIDList]] for targetIDList in targetObjIDArray]

        matchedObjList = [anotherList.new() for _ in range(len(self.all))]
        [matchedObj.setAll(matchedValue) for matchedObj,matchedValue in zip(matchedObjList, matchedValueList)]
        [setattr(this, targetAttrName, matchedObj) for this, matchedObj in zip(self.all, matchedObjList)]

    def link(self, anotherList, targetAttrNameOnLeft: str, targetAttrNameOnRight: str, matchFunctionOnLeft=lambda x: True, matchFunctionOnRight=lambda y: True):
        """
        For each element in current rqlList, find all elements that meet requirement
        matchFunctionOnRight(element_in_another_list) == matchFunctionOnLeft(element_in_this_list)
        from another RiskQuantLib list object. The elements meeting requirement will be set as an attribute
        of element_in_this_list.

        After this is done, for each element in another rqlList, find all elements that meet requirement
        matchFunctionOnLeft(element_in_this_list) == matchFunctionOnRight(element_in_another_list)
        from current RiskQuantLib list object. The elements meeting requirement will be set as an attribute
        of element_in_another_list.

        Parameters
        ----------
        anotherList : RiskQuantLib list or list
            Another list object, holding elements waiting to be selected.
        targetAttrNameOnLeft : str
            The attribute name of present list that you want to use to mark collected elements from another list.
        targetAttrNameOnRight : str
            The attribute name of another list that you want to use to mark collected elements from present list.
        matchFunctionOnLeft : function
            This function has and only has one parameter, which stands for element in current list.
        matchFunctionOnRight : function
            This function has and only has one parameter, which stands for element in another list.
        """
        self.match(anotherList, targetAttrNameOnLeft, matchFunctionOnLeft, matchFunctionOnRight)
        anotherList.match(self, targetAttrNameOnRight, matchFunctionOnRight, matchFunctionOnLeft)

    def join(self, anotherList, targetAttrName: str, filterFunction = lambda x,y:True):
        """
        For each element, find all elements that meet requirements from another RiskQuantLib
        list object. The elements meeting requirement will be set as an attribute of present
        list.

        This function is very like pandas.DataFrame.merge.

        Parameters
        ----------
        anotherList : RiskQuantLib list or list
            Another list object, holding elements waiting to be selected.
        targetAttrName : str
            The attribute name that you want to use to mark collected elements from another list.
        filterFunction : function
            This function has two parameter, left and right, and must return a bool value.
            If true is returned, the element will be added. False means not added.

        """
        valueList = [[another for another in anotherList.all if filterFunction(this,another)] for this in self.all]
        valueObj = [anotherList.new() for i in self.all]
        [obj.setAll(value) for obj,value in zip(valueObj,valueList)]
        [setattr(i,targetAttrName,j) for i,j in zip(self.all,valueObj)]

    def connect(self, anotherList, targetAttrNameOnLeft: str, targetAttrNameOnRight: str, filterFunction = lambda x,y:True, unsymmetrical = False, filterFunctionOnLeft = lambda presentList, anotherList: True, filterFunctionOnRight=lambda presentList,anotherList: True):
        """
        For each element, find all elements that meet requirements from another RiskQuantLib
        list object. The elements meeting requirement will be set as an attribute of present
        list.

        After this is down, for each element of another RiskQuantLib, find all elements that
        meet requirements from present RiskQuantLib list object. The elements meeting requirement
        will be set as an attribute of another list.

        This function actually calls join twice, but it switch the position of two RiskQuantLib
        list in the second call.


        Parameters
        ----------
        anotherList : RiskQuantLib list or list
            Another list object, holding elements waiting to be selected.
        targetAttrNameOnLeft : str
            The attribute name of present list that you want to use to mark collected elements from another list.
        filterFunction : function
            This function has two parameter, left and right, and must return a bool value.
            If true is returned, the element will be added to each other. False means not added.
        unsymmetrical : bool
            If true, different rules will be used when join two list, where filterFunctionOnLeft will be used
            when present list join another list, and filterFunctionOnRight will be used when another list join
            present list.
        filterFunctionOnLeft : function
            This function has two parameter, presentList and anotherList, and must return a bool value.
            If true is returned, the element from another list will be added to present list. False means not added.
        targetAttrNameOnRight : str
            The attribute name of another list that you want to use to mark collected elements from present list.
        filterFunctionOnRight : function
            This function has two parameter, presentList and anotherList, and must return a bool value.
            If true is returned, the element from present list will be added to another list. False means not added.


        Returns
        -------
        None
        """
        if unsymmetrical:
            def adjustedFilterFunctionOnRight(x,y):
                return filterFunctionOnRight(y,x)
            self.join(anotherList,targetAttrNameOnLeft,filterFunctionOnLeft)
            anotherList.join(self,targetAttrNameOnRight,adjustedFilterFunctionOnRight)
        else:
            def adjustedFilterFunctionOnRight(x,y):
                return filterFunction(y,x)
            self.join(anotherList,targetAttrNameOnLeft,filterFunction)
            anotherList.join(self,targetAttrNameOnRight,adjustedFilterFunctionOnRight)

    def scale(self, attrName: str, targetAttrName: str = '', filterFunction = lambda x: True, inplace: bool = False):
        """
        For each element, find the attribute value and calculate the portion of each element to the sum,
        given attribute name.

        After calling this function, a 'scaled_attrName' attribute will be added to each element.

        This function is very like pandas.DataFrame.groupby.agg.

        Parameters
        ----------
        attrName :str
            The attribute which you want to scale.
        targetAttrName : str
            The attribute name that you want to use to mark the portion of element.
        filterFunction : function
            This function has one parameter, element, and must return a bool value.
            If true is returned, the element will be include when process scale.
            False means not included.

        """
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

    def merge(self, anotherList, how : str, on = lambda x,y:True, inplace = False):
        """
        This function will merge two RiskQuantLib list object. This function should only
        be used when washing data. After merge, any change to source list will or will not
        influence merge result, depending on python copy mechanism. This won't be a problem
        if data flows by single direction. However, troubles will come when you wish to
        change the origin to influence the merge result list, after merge action.

        In short, do not change the origin list once you merge them, any change should be
        done by merged result.

        If 'on' function can not identify the only element to merge, all unique attributes
        of the elements that meet requirement will be added to present list element.
        (Unique means this attribute only appears once in the list element, the others
        don't have it.) If the attribute appears more than one times, only the first will
        be added.

        It's like pandas.DataFrame.merge, but not totally the same. In RiskQuantLib,
        listA.merge(listB) is not the same from listB.merge(listA), even if you specify
        the same value of parameter 'how' and 'on'.

        No matter what value parameter 'how' is given, attributes of elements in anotherList that
        meet requirement of 'on' will be added as attributes of elements in present list. The
        attributes who have the same name in both lists won't be copied, which means you can't
        merge two lists twice. (In the second time you merge them, the first list object has all
        attributes that anotherList has, so all attributes will be skipped, no attribute will be
        copied.)

        If how == 'inner', only the elements in the present list who have relative elements
        in anotherList will be returned.

        If how == 'outer', all elements in presentList, plus elements from anotherList that
        don't have relative elements in present list will be returned.

        If how == 'left', all elements in presentList will be returned.

        if how == 'right', the elements in the present list who have relative elements
        in anotherList, plus elements from anotherList that don't have relative elements
        in present list will be returned.

        """
        def trySetAttr(obj,attrName,attrValue):
            try:
                setattr(obj,attrName,attrValue)
            except:
                pass
        if inplace:
            leftList = self.all
            rightList = anotherList
        else:
            leftList = self.copy(deep=True).all
            rightList = copy.deepcopy(anotherList)
        inner = [{'left':left,'right':right} for left in leftList for right in rightList if on(left,right)]
        leftInner = list(set([pair['left'] for pair in inner]))
        rightInner = list(set([pair['right'] for pair in inner]))
        leftResidual = [i for i in leftList if i not in leftInner]
        rightResidual = [i for i in rightList if i not in rightInner]
        if len(leftInner) == len(inner):
            [[trySetAttr(element['left'],attr,getattr(element['right'],attr,np.nan)) if not hasattr(element['left'],attr) else None for attr in dir(element['right'])] for element in inner]
        else:
            for element in inner:
                [trySetAttr(element['left'], attr, getattr(element['right'], attr, np.nan)) if not hasattr(element['left'], attr) else None for attr in dir(element['right'])]
        tmpObj = self.new()
        if how == 'outer':
            tmpObj.setAll(leftInner+leftResidual+rightResidual)
        elif how == 'inner':
            tmpObj.setAll(leftInner)
        elif how == 'left':
            tmpObj.setAll(leftInner + leftResidual)
        elif how == 'right':
            tmpObj.setAll(leftInner + rightResidual)
        return tmpObj

    def zip(self, attrNameList : list, *args):
        """
        This function will convert the values of given attribute into a zip object.
        If you also pass an external list or other iterable object, it will zip that
        list with the value of given internal attribute.

        Parameters
        ----------
        attrNameList : str or list
            The attribute name whose values you want to zip.
        args : list or iterable
            External iterable object, whose value is zipped with internal attribute values.

        Returns
        -------
        zip object
        """
        argsMerged = tuple([self[attrName] for attrName in attrNameList] + [i for i in args])
        return zip(*argsMerged)

    def toDict(self, attrNameAsKey : str, attrNameAsValue : str):
        """
        This function will return a dict, given the attribute name whose values are used as dict key,
        and attribute name whose values are used as dict value.

        Parameters
        ----------
        attrNameAsKey : str
            The attribute name whose values you want to use as dict keys.
        attrNameAsValue : str
            The attribute name whose values you want to use as dict values.

        Returns
        -------
        dict
        """
        return dict(self.zip([attrNameAsKey, attrNameAsValue]))

    def toSeries(self, attrNameAsValue : str = '', attrNameAsIndex : str = '', nameString : str = '', index = None):
        """
        This function will return a pandas.Series object, given the attribute name whose values are used as series
        value, and attribute name whose values are used as series index. You can also pass a string to identify the
        name of series.

        If you don't pass any attribute name, this function will use all elements themselves in this list to form
        a Series.

        Parameters
        ----------
        attrNameAsValue : str
            The attribute name whose values you want to use as series value.
        attrNameAsIndex : str
            The attribute name whose values you want to use as series index.
        nameString : str
            The name of series.
        index : list or operation
            The index list. If you do not specify the attribute name used as index, you can pass a list as index manually.

        Returns
        -------
        pd.Series
        """
        if len(self)==0:
            return pd.Series(dtype=float, name=nameString)
        if attrNameAsValue == '':
            result = pd.Series(self.all, index=index, name=nameString) if index else pd.Series(self.all, name=nameString)
        elif attrNameAsIndex == '':
            result = pd.Series(self[attrNameAsValue], name=nameString, index=index) if index else pd.Series(self[attrNameAsValue], name=nameString)
        else:
            result = pd.Series(self[attrNameAsValue], index = self[attrNameAsIndex], name = nameString)
        return result

    def toDF(self, attrNameList : str or list = '', attrNameAsIndex : str = '', index = None):
        """
        This function will return a pandas.DataFrame object, given the attribute name whose values are used as dataframe
        value, and attribute name whose values are used as dataframe index.

        If you don't pass any attribute name, this function will use all elements themselves in this list to form
        a dataframe.

        Parameters
        ----------
        attrNameList : str or list
            The attribute name whose values you want to use as dataframe value.
        attrNameAsIndex : str
            The attribute name whose values you want to use as dataframe index.
        index : list or operation
            The index list. If you do not specify the attribute name used as index, you can pass a list as index manually.

        Returns
        -------
        pd.DataFrame
        """
        if attrNameList == '':
            result = pd.DataFrame(self.all, index=index) if index else pd.DataFrame(self.all)
            return result
        elif type(attrNameList) == str:
            attrNameList = [attrNameList]
        result = pd.DataFrame(self[attrNameList])
        if attrNameAsIndex == '':
            dfIndex = index if index else result.index
        else:
            dfIndex = self[attrNameAsIndex]
        result.index = dfIndex
        return result


    def toArray(self, attrNameList : str or list = ''):
        """
        This function will return a numpy.ndarray object, given the attribute name whose values are used as array
        value.

        If you don't pass any attribute name, this function will use all elements themselves in this list to form
        an array.

        Parameters
        ----------
        attrNameList : str or list
            The attribute name whose values you want to use as array value.

        Returns
        -------
        np.ndarray
        """
        if attrNameList == '':
            return np.array(self.all)
        elif type(attrNameList) == str:
            attrNameList = [attrNameList]
        return self.toDF(attrNameList).values

    def toList(self, attrNameList: str or list = ''):
        """
        This function will return a list object, given the attribute name whose values are used as list
        value.

        If you don't pass any attribute name, this function will use all elements themselves in this list to form
        a new list.

        Parameters
        ----------
        attrNameList : str or list
            The attribute name whose values you want to use as list value.

        Returns
        -------
        list
        """
        if attrNameList == '':
            return self.all
        elif type(attrNameList) == str:
            attrNameList = [attrNameList]
        return [[getattr(ele,attr,np.nan) for attr in attrNameList] for ele in self]

    def fromDF(self, df: pd.DataFrame, code: str = '', name: str = ''):
        """
        This function will convert a dataframe to RiskQuantLib list object. If
        there is already elements in present list, all elements will be deleted.

        The column name of dataframe should be in English, and this function
        will try to set it to element attribute if there exists the attribute
        with the same name. That is, this function will only set value of
        registered attribute. If not registered in current list class, it
        will be skipped.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe you want to pull data from.
        code : str
            The column name that you want to mark as 'code' attribute.
        name : str
            The column name that you want to mark as 'name' attribute.

        Returns
        -------
        RiskQuantLib List
        """
        if not hasattr(self,'__elementClass__'):
            print("The List Must Have Attribute Named __elementClass__ To Call This Function.")
            return
        else:
            self.setAll([])
            instrumentNameString = self.__elementClass__.__name__
            c_instrumentNameString = instrumentNameString[0].capitalize() + instrumentNameString[1:]
            if code == '' and name == '':
                getattr(self, 'add' + c_instrumentNameString + 'Series', lambda x,y:None)(df.index,df.index)
            elif code!='' and name!='':
                getattr(self, 'add' + c_instrumentNameString + 'Series', lambda x, y: None)(df[code], df[name])
            elif code!='':
                getattr(self, 'add' + c_instrumentNameString + 'Series', lambda x, y: None)(df[code], df[code])
            elif name!='':
                getattr(self, 'add' + c_instrumentNameString + 'Series', lambda x, y: None)(df[name], df[name])
            else:
                pass
            def trySetAttr(attrName,pdseries):
                try:
                    c_attrName = attrName[0].capitalize() + attrName[1:]
                    if hasattr(self,'set'+c_attrName):
                        getattr(self, 'set'+c_attrName, lambda x,y:None)(self['code'],pdseries)
                    else:
                        pass
                except:
                    pass
            [trySetAttr(col,df[col]) for col in df.columns]
            return self

    def addFromDF(self, df : pd.DataFrame, code :str = '', name:str = ''):
        """
        This function will add elements from a dataframe. If there is already
        elements in present list, all elements will be kept, while new elements
        will be added.

        The column name of dataframe should be in English, and this function
        will try to set it to element attribute if there exists the attribute
        with the same name. That is, this function will only set value of
        registered attribute. If not registered in current list class, it
        will be skipped.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe you want to pull data from.
        code : str
            The column name that you want to mark as 'code' attribute.
        name : str
            The column name that you want to mark as 'name' attribute.

        Returns
        -------
        RiskQuantLib List
        """
        tmpList = self.new()
        tmpList.fromDF(df = df, code=code,name=name)
        self.setAll(self.all + tmpList.all)

    def fromIterable(self, iterable:list, code :str = '', name:str = ''):
        """
        This function will convert an iterable to RiskQuantLib list object. If
        there is already elements in present list, all elements will be deleted.

        This function will only set value of registered attribute. If not
        registered in current list class, it will be skipped.

        Parameters
        ----------
        iterable : list
            The iterable object you want to pull data from.
        code : str
            The attribute name of iterable that you want to
            mark as 'code' in RiskQuantLib List Object.
        name : str
            The attribute name of iterable that you want to
            mark as 'name' in RiskQuantLib List Object.

        Returns
        -------
        RiskQuantLib List
        """
        if not hasattr(self,'__elementClass__'):
            print("The List Must Have Attribute Named __elementClass__ To Call This Function.")
            return
        else:
            self.setAll([])
            instrumentNameString = self.__elementClass__.__name__
            c_instrumentNameString = instrumentNameString[0].capitalize() + instrumentNameString[1:]
            if code == '' and name == '':
                getattr(self, 'add' + c_instrumentNameString + 'Series', lambda x,y:None)([str(index) for index,obj in enumerate(iterable)],[str(index) for index,obj in enumerate(iterable)])
            elif code!='' and name!='':
                getattr(self, 'add' + c_instrumentNameString + 'Series', lambda x, y: None)([getattr(obj,code,str(index)) for index,obj in enumerate(iterable)], [getattr(obj,name,str(index)) for index,obj in enumerate(iterable)])
            elif code!='':
                getattr(self, 'add' + c_instrumentNameString + 'Series', lambda x, y: None)([getattr(obj,code,str(index)) for index,obj in enumerate(iterable)], [getattr(obj,code,str(index)) for index,obj in enumerate(iterable)])
            elif name!='':
                getattr(self, 'add' + c_instrumentNameString + 'Series', lambda x, y: None)([getattr(obj,name,str(index)) for index,obj in enumerate(iterable)], [getattr(obj,name,str(index)) for index,obj in enumerate(iterable)])
            else:
                pass
            def trySetAttr(obj,attrName,attrValue):
                try:
                    c_attrName = attrName[0].capitalize() + attrName[1:]
                    if hasattr(obj,'set'+c_attrName):
                        getattr(obj, 'set'+c_attrName, lambda x:None)(attrValue)
                    else:
                        pass
                except:
                    pass
            [[trySetAttr(instrumentObj,attr,getattr(obj,attr,np.nan)) for attr in dir(obj)] for obj,instrumentObj in zip(iterable,self.all)]
            return self

    def addFromIterable(self, iterable:list, code :str = '', name:str = ''):
        """
        This function will add elements from an iterable object. If there is already
        elements in present list, all elements will be kept, while new elements
        will be added.

        This function will only set value of registered attribute. If not
        registered in current list class, it will be skipped.

        Parameters
        ----------
        iterable : list
            The iterable object you want to pull data from.
        code : str
            The attribute name of iterable that you want to
            mark as 'code' in RiskQuantLib List Object.
        name : str
            The attribute name of iterable that you want to
            mark as 'name' in RiskQuantLib List Object.

        Returns
        -------
        RiskQuantLib List
        """
        tmpList = self.new()
        tmpList.fromIterable(iterable=iterable, code=code,name=name)
        self.setAll(self.all + tmpList.all)

    def updateAttr(self, attrName : str, codeSeries, valueSeries, byAttr = 'code'):
        """
        This function will update the attribute value of elements whose code
        appears in given codeSeries. If code of element doesn't show in
        codeSeries, these elements will be skipped and not changed.

        If the attribute is not registered, it will be created.

        Parameters
        ----------
        attrName : str
            The attribute whose value is exactly what you want to update.
        codeSeries : list
            An iterable object that contains codes of elements whose attribute need to be updated.
        valueSeries : list
            An iterable object that contains new values of attributes.
        byAttr : str
            The attribute that is used to index element in this list. By default, this attribute is code.
            But you can specify another attribute A, if you do it, this function will update the attribute
            value of elements whose attribute A appears in given codeSeries.

        Returns
        -------
        None
        """
        def setAttr(totalList,attrNameNotRegistered,codeSeriesNotRegistered,valueSeriesNotRegistered,byAttrNotRegistered):
            index = set(codeSeriesNotRegistered)
            updateList = totalList.filter(lambda x: getattr(x, byAttrNotRegistered, np.nan) in index)
            setDict = dict(zip(codeSeriesNotRegistered,valueSeriesNotRegistered))
            [setattr(i,attrNameNotRegistered,setDict[getattr(i,byAttrNotRegistered,np.nan)]) for i in updateList]
            newCreated = totalList.filter(lambda x:not hasattr(x,attrNameNotRegistered))
            [setattr(i,attrNameNotRegistered,np.nan) for i in newCreated]
        c_attrName = attrName[0].capitalize() + attrName[1:]
        getattr(self,'set'+c_attrName,lambda x,y,z,k:setAttr(self,attrName,x,y,z))(codeSeries,valueSeries,byAttr,True)


    def updateAttrFromSeries(self, sr: pd.Series, attrName = '', byAttr = 'code'):
        """
        This function will update attribute value of current list by passed series.
        The name of passes series should be in English, and if current
        list has registered attribute whose name is the same with column name, it will
        be updated. If the attribute is not registered, it will be created.

        Parameters
        ----------
        sr : pd.Series
            The series that you want to update data from.
        attrName : str
            The attribute whose value is exactly what you want to update.
        byAttr : str
            The attribute that is used to index element in this list. By default, this attribute is code.
            But you can specify another attribute A, if you do it, this function will update the attribute
            value of elements whose attribute A appears in df[code] or df.index.

        Returns
        -------
        None
        """
        attrName = sr.name if attrName=='' else attrName
        if attrName:
            self.updateAttr(attrName, sr.index, sr.values, byAttr=byAttr)
        else:
            raise ValueError("Can not update from a series without name if you don't pass an attrName.")

    def updateAttrFromDF(self, df: pd.DataFrame, code:str = '', byAttr = 'code'):
        """
        This function will update attribute value of current list by passed dataframe.
        The column name of passes dataframe should be in English, and if current
        list has registered attribute whose name is the same with column name, it will
        be updated. If the attribute is not registered, it will be created.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe that you want to update data from.
        code : str
            A column name of df that you used to mark rows. Elements whose code
            is in this column will be updated, and those not in this column will
            not be influenced. If blank, the index of df will be used as code.
        byAttr : str
            The attribute that is used to index element in this list. By default, this attribute is code.
            But you can specify another attribute A, if you do it, this function will update the attribute
            value of elements whose attribute A appears in df[code] or df.index.

        Returns
        -------
        None
        """
        if code == '':
            [self.updateAttr(col, df.index, df[col], byAttr=byAttr) for col in df.columns]
        else:
            [self.updateAttr(col, df[code], df[col], byAttr=byAttr) for col in df.columns]

    def updateAttrFromArray(self, array: np.ndarray, codeList: list, attributeNameList: str or list, byAttr = 'code'):
        """
        This function will update attribute value of current list by passed array.
        You have to identify that each column of array belongs to which attribute, and
        each row of array represents which element.

        The row number of passed array must equal to length of codeList, and the column
        number of passed array must equal to length of attributeNameList.

        If the attribute are not registered, the attribute will be created.

        Parameters
        ----------
        array : np.ndarray
            The array you which want to update this list from.
        codeList : list
            The code of element whose attribute will be updated by this function. Those whose code
            is not specified in this list will not be influenced. The length of this list must equal
            to the row number of passed array.
        attributeNameList : str or list
            The attribute that you want to update. Those attribute in this list will be updated, and those
            are not in this list will not be influenced.
        byAttr : str
            The attribute that is used to index element in this list. By default, this attribute is code.
            But you can specify another attribute A, if you do it, this function will update the attribute
            value of elements whose attribute A appears in given codeList.

        Returns
        -------
        None
        """
        attributeNameList = [attributeNameList] if type(attributeNameList)==str else attributeNameList
        [self.updateAttr(attr, codeList, array[:,index], byAttr=byAttr) for index,attr in enumerate(attributeNameList)]

    def updateAttrFromDict(self, attrName : str, codeValueDict : dict, byAttr = 'code'):
        """
        This function will update attribute value of current list by passed dict.
        The key of passes dict should be code string. If current list has registered
        attribute whose name is in keys of codeValueDict, it will be updated. If the attribute
        is not registered, it will be created.

        Parameters
        ----------
        attrName : str
            The attribute whose value is exactly what you want to update.
        codeValueDict : dict
            A dict that maps code to value.
        byAttr : str
            The attribute that is used to index element in this list. By default, this attribute is code.
            But you can specify another attribute A, if you do it, this function will update the attribute
            value of elements whose attribute A appears in given codeValueDict.

        Returns
        -------
        None
        """
        self.updateAttr(attrName,codeValueDict.keys(),codeValueDict.values(), byAttr=byAttr)

    #<operation>
    #</operation>
