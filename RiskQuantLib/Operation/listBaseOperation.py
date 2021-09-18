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
    """
    listBase() is the function class that makes all RiskQuantLib list object functional.
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
        self.__init_get_item__()

    def __getitem__(self, item):
        """
        This function makes RiqkQuantLib list object selectable. Use [] to call this function.
        Mixed index is used here. By calling [], you can index either element or attribute.

        Parameters
        ----------
        item : str or list or slice
            If a string is given, all elements will be examined, if 'code' attribute equals
            to the given string, return the first element that meets this requirement.

            If no element code meets this requirement, try to return a list of attribute
            value, whose name equals to the given string.

            If a slice or int number is given, this function behaves like iloc, returns the
            item-th element or a collection of elements.

            If a list is given, return all elements whose code in the given list. If no code
            in the given list, return a 2-dimension array of attribute values, where attribute
            name is in the given list.

        Returns
        -------
        None
        """
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
            return changeSecurityListToStr(self['code'])
        except:
            return ''

    def __len__(self):
        """
        This function returns the length of RiskQuantLib list.
        """
        return len(self.all)

    def _sortIterator(self,sortObj):
        import pandas as pd
        sortList = [getattr(sortObj,i) if type(getattr(sortObj,i))!=type(pd.Series()) else len(getattr(sortObj,i)) for i in self._sortPropertyList]
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
            return [[j for j in self.all if j.code == i][keepIndex] for i in codeList]

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
            return [[j for j in self.all if getattr(j,attrNameString) == i][keepIndex] for i in propertyValueList]

    def apply(self,applyFunction,*args):
        """
        This function will apply the given function to each element of RiskQuantLib list.
        Default settings will leave any change to element out. Your change to elements won't
        be kept. Only the result of applyFunction is returned.
        """
        return Parallel(n_jobs=mp.cpu_count())(delayed(applyFunction)(i,*args) for i in self.all)

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

    def execFunc(self,functionName,*args):
        """
        This function will execute instance function for every element in present RiskQuantLib list object,
        given the function name. If some elements don't have the function, a Null function will be used, and
        the result will skip the execution for that element.

        If the length of present list is not long, list comprehension will be used. If it's a long
        list, joblib will be used to establish multiple threads.

        Parameters
        ----------
        functionName : str
            The function that element has, and you want to call.
        """
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
        """
        Get a copy of present RiskQuantLib list object.
        """
        if deep:
            tmp = copy.deepcopy(self)
            tmp.__init_get_item__()
            return tmp
        else:
            tmp = copy.copy(self)
            tmp.__init_get_item__()
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
            self.setAll(sorted(self.all,key=self._sortIterator,reverse=reverse))
            return None
        elif useObj:
            tmpObj = copy.deepcopy(self)
            tmpObj.setAll(sorted(self.all,key=self._sortIterator,reverse=reverse))
            return tmpObj
        else:
            return sorted(self.all,key=self._sortIterator,reverse=reverse)

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

    def __init_get_item__(self):
        self.loc = loc(self.all)
        pass

    def __set_number_index__(self):
        [setattr(i,'numberIndex',j) for j,i in enumerate(self.all)]

    def setIndex(self, propertyNameString:str, inplace = True):
        """
        Set the index for each element, given attribute name. The index value will be set as the attribute value
        you choose.
        """
        if inplace:
            [i.setIndex(getattr(i,propertyNameString,np.nan)) for i in self.all]
            return None
        else:
            tmpObj = self.copy(deep=True)
            [i.setIndex(getattr(i,propertyNameString,np.nan)) for i in tmpObj.all]
            return tmpObj

    def dropIndex(self, inplace=True):
        """
        Delete index for each element.
        """
        if inplace:
            [delattr(i,'index') for i in self.all]
            return None
        else:
            tmpObj = self.copy(deep=True)
            [delattr(i,'index') for i in tmpObj.all]
            return tmpObj

    def reIndex(self, indexList:list, useObj = True, inplace = False):
        """
        Return a new RiskQuantLib list object whose elements are chosen according to
        the index, the index of new list element must be in th indexList to be included.
        If more than one elements meet requirement, only the first one will be kept.
        """
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
        """
        Reset the index as the n-th element of list.
        """
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
        """
        For each element, This function will collect the n elements before
        that element, create a new RiskQuantLib list object to holding it. The new list
        will be set as an attribute of '_rolling', thus the present element can reach to
        the information of its former elements.
        """
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

    def join(self,anotherList,targetAttrName : str,filterFunction = lambda x,y:True):
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

    def scale(self,attrName,targetAttrName = '',filterFunction = lambda x:True,inplace = False):
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

    def fromDF(self, df : pd.DataFrame, code :str = '', name:str = ''):
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
        if not hasattr(self,'elementClass'):
            print("The List Must Have Attribute Named elementClass To Call This Function.")
            return
        else:
            self.setAll([])
            instrumentNameString = self.elementClass.__name__
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
        if not hasattr(self,'elementClass'):
            print("The List Must Have Attribute Named elementClass To Call This Function.")
            return
        else:
            self.setAll([])
            instrumentNameString = self.elementClass.__name__
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

    def updateAttr(self, attrName : str, codeSeries, valueSeries):
        """
        This function will update the attribute value of elements whose code
        appears in given codeSeries. If code of element doesn't show in
        codeSeries, these elements will be skipped and not changed.

        Parameters
        ----------
        attrName : str
            The attribute whose value is exactly what you want to update.
        codeSeries : list
            An iterable object that contains codes of elements whose attribute need to be updated.
        valueSeries : list
            An iterable object that contains new values of attributes.

        Returns
        -------
        None
        """
        c_attrName = attrName[0].capitalize() + attrName[1:]
        tmpObj = self.filter(lambda x:x.code in list(codeSeries))
        getattr(tmpObj,'set'+c_attrName,lambda x,y:None)(codeSeries,valueSeries)

    def updateAttrFromDF(self, df: pd.DataFrame, code:str = ''):
        """
        This function will update attribute value of current list by passed dataframe.
        The column name of passes dataframe should be in English, and if current
        list has registered attribute whose name is the same with column name, it will
        be updated.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe that you want to update data from.
        code : str
            The column name of df that you used to mark rows. Elements whose code
            is in this column will be updated, and those not in this column will
            not be influenced. If blank, the index of df will be used as code.

        Returns
        -------
        None
        """
        if code == '':
            [self.updateAttr(col, df.index, df[col]) for col in df.columns]
        else:
            [self.updateAttr(col, df[code], df[col]) for col in df.columns]

    def updateAttrFromDict(self, attrName : str, codeValueDict : dict):
        """
        This function will update attribute value of current list by passed dict.
        The key of passes dict should be code string. If current list has registered
        attribute whose name is in keys of codeValueDict, it will be updated.

        Parameters
        ----------
        attrName : str
            The attribute whose value is exactly what you want to update.
        codeValueDict : dict
            A dict that maps code to value.

        Returns
        -------
        None
        """
        self.updateAttr(attrName,codeValueDict.keys(),codeValueDict.values())