#!/usr/bin/python
#coding = utf-8

import numpy as np

#<import>
#</import>

def percentage(dataList:list, pct:float):
    """
    This function returns the percentage of a list.

    Parameters
    ----------
    dataList : list
        The list holding data
    pct : float
        The percentage number. 99 means 99% percentage.

    Returns
    -------
    None
    """
    length = len(dataList)
    sortedData = sorted(dataList,reverse=True)
    return sortedData[int(pct/100*length)]

def interP1d(xList:list, yList:list, kind='linear'):
    """
    This function returns a cubic interpolate of two lists.
    It returns a model object, use model(newValue) to predict new value.

    Parameters
    ----------
    xList : list
        The X list
    yList : list
        The Y list
    kind : str
        The type of interpolation, can be 'linear', 'cubic', 'nearest'

    Returns
    -------
    model : object
        The scipy model, use model(newValue) to get predicted values.
    """
    from scipy.interpolate import interp1d
    x = np.array(xList)
    y = np.array(yList)
    model = interp1d(x,y,kind=kind,fill_value='extrapolate')
    return model


def linearRegressions(xArray:np.ndarray, yArray:np.ndarray):
    """
    This function returns a linear regression of multi-dimension array.

    Parameters
    ----------
    xArray : np.ndarray
        The X array, which has the shape of (n * k), n is the number of samples, k is the number of features
    yArray : np.ndarray
        The Y array, which has the shape of (n * 2), n is the number of samples

    Returns
    -------
    model : tuple
        The tuple of (coefList, intercept)
    """
    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    model.fit(xArray,yArray)
    return model.coef_[0], model.intercept_[0]


def linearRegression(xList:list, yList:list):
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
    model : tuple
        The tuple of (coef, intercept)
    """

    x = np.array(xList).reshape(-1,1)
    y = np.array(yList).reshape(-1,1)
    k, b = linearRegressions(x, y)
    return k[0], b


def maxDrawdown(dataList:list, relative: bool=True):
    """
    This function returns a max drawdown of given list.

    Parameters
    ----------
    dataList : list
        The data list
    relative : str
        The drawdown type. If true, the max drawdown will be a percentage relative to highest point,
        otherwise it will be a distance.

    Returns
    -------
    model : np.float64
        The max drawdown of given data.
    """
    data = np.array(dataList)
    cumMax = np.maximum.accumulate(data)
    drawdown = 1 - (data / cumMax) if relative else cumMax - data
    return np.max(drawdown)


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
    return True if type(x) == type(np.nan) and np.isnan(x) else False


#<mathTool>
#</mathTool>













