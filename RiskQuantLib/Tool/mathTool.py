#!/usr/bin/python
#coding = utf-8

import numpy as np
#<import>
#</import>

def percentageOfSeries(dataList:list,percentage:float):
    """
    This function returns the percentage of a list.

    Parameters
    ----------
    dataList : list
        The list holding data
    percentage : float
        The percentage number. 99 means 99% percentage.

    Returns
    -------
    None
    """
    length = len(dataList)
    sortedData = sorted(dataList,reverse=True)
    return sortedData[int(percentage/100*length)]

def interP1d(xList:list,yList:list,Kind='cubic'):
    """
    This function returns a cubic interpolate of two lists.

    Parameters
    ----------
    xList : list
        The X list
    yList : list
        The Y list

    Returns
    -------
    model : object
        The scipy model.
    """
    from scipy.interpolate import interp1d
    x = np.array(xList)
    y = np.array(yList)
    model = interp1d(x,y,kind=Kind,fill_value='extrapolate')
    return model

def linearRegression(xList:list,yList:list):
    """
    This function returns a linear regression of two lists.

    Parameters
    ----------
    xList : list
        The X list
    yList : list
        The Y list

    Returns
    -------
    model : object
        The scipy model.
    """
    from sklearn.linear_model import LinearRegression
    x = np.array(xList).reshape(-1,1)
    y = np.array(yList).reshape(-1,1)

    model = LinearRegression()
    model.fit(x,y)
    return model

def maxDropDown(dataList:list,valueType:str = 'Relative'):
    """
    This function returns a max dropdown of given list.

    Parameters
    ----------
    dataList : list
        The data list
    valueType : str
        The drop down type. 'Relative' or 'Absolute' can be used.

    Returns
    -------
    model : np.float
        The max drop down of given data.
    """
    dropDownList = []
    for i,j in enumerate(dataList):
        historySeries = dataList[:i+1]
        if valueType == 'Relative':
            dropDownList.append(np.nanmin([0,j/np.nanmax(historySeries)-1]))
        elif valueType == 'Absolute':
            dropDownList.append(np.nanmin([0, j - np.nanmax(historySeries)]))
        else:
            print("valueType can only be Relative or Absolute")
            return np.nan
    return np.nanmin(dropDownList)

def isnan(x):
    """
    This function returns a bool value of given data.

    Parameters
    ----------
    x : Any
        This is the data you want to tell whether it is a nan.

    Returns
    -------
    bool
    """
    if type(x) == type(np.nan) and np.isnan(x):
        return True
    else:
        return False

#<mathTool>
#</mathTool>













