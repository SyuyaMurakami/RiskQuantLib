#!/usr/bin/python
#coding = utf-8

import numpy as np
import pandas as pd

#<import>
#</import>

def findFirstNotNanValueOfSeries(sr: pd.Series):
    """
    Return the first not nan value of a pandas.Series object.
    """
    notNan = sr.dropna()
    return np.nan if notNan.empty else notNan.iloc[0]


def resetIndexByFirstNotNanValue(df:pd.DataFrame, dropFirst: bool = False, inplace: bool=True):
    """
    Reset index by the first not nan value.
    """
    if inplace:
        df.dropna(axis=0,how='all',inplace=True)
        df.index = df.apply(findFirstNotNanValueOfSeries,axis=1)
        return df.drop(columns=[df.columns[0]], inplace=True) if dropFirst else None
    else:
        tmp = df.dropna(axis=0,how='all',inplace=False)
        tmp.index = tmp.apply(findFirstNotNanValueOfSeries, axis=1)
        return tmp.drop(columns=[df.columns[0]]) if dropFirst else tmp


#<frameTool>
#</frameTool>

