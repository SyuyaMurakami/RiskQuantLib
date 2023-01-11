#!/usr/bin/python
#coding = utf-8

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
#<import>
#</import>

matplotlib.rcParams['axes.unicode_minus'] = False
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']

def plotLine(df:pd.DataFrame,titleStr:str,xLabelStr:str,yLabelStr:str,savePathStr:str):
    """
    Plot a multiple line graph.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe you want to plot. Each column is a series. Values must be number.
    titleStr : str
        The graph title.
    xLabelStr : str
        The x label
    yLabelStr : str
        The y label
    savePathStr : str
        The path where you want to save the graph

    Returns
    -------
    None
    """
    fig = plt.figure(figsize=(16,11))
    ax = fig.add_subplot(111)
    plt.plot(df)
    plt.xlabel(xLabelStr)
    plt.ylabel(yLabelStr)
    plt.xticks(rotation=45,fontsize=7)
    plt.title(titleStr)
    plt.legend(df.columns.to_list())
    plt.savefig(savePathStr)
    plt.show()

def plotPie(df:pd.DataFrame,titleStr:str,savePathStr:str):
    """
    Plot a pie chart.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe you want to plot. Each column is a series. Values must be number.
    titleStr : str
        The chart title.
    savePathStr : str
        The path where you want to save the chart

    Returns
    -------
    None
    """
    fig = plt.figure(figsize=(16,11))
    ax = fig.add_subplot(111)
    plt.pie(df,autopct='%3.2f%%',radius=0.8,labels=df.index)
    plt.title(titleStr)
    plt.savefig(savePathStr)
    plt.show()

def plotBar(df:pd.DataFrame,titleStr:str,xLabelStr:str,yLabelStr:str,savePathStr:str):
    """
    Plot a bar chart.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe you want to plot. Each column is a series. Values must be number.
    titleStr : str
        The chart title.
    xLabelStr : str
        The x label
    yLabelStr : str
        The y label
    savePathStr : str
        The path where you want to save the chart

    Returns
    -------
    None
    """
    fig = plt.figure(figsize=(16,11))
    ax = fig.add_subplot(111)
    for i in df.columns:
        plt.bar(df.index,df[i])
    plt.xlabel(xLabelStr)
    plt.ylabel(yLabelStr)
    plt.xticks(rotation=45,fontsize=7)
    plt.title(titleStr)
    plt.legend(df.columns.to_list())
    plt.savefig(savePathStr)
    plt.show()

def plotMultiBar(xSeries:pd.Series,yDataframe:pd.DataFrame,xLabelStr:str,yLabelStr:str,titleStr:str,savePathStr:str):
    """
    Plot a bar chart.

    Parameters
    ----------
    xSeries : pd.Series
        The series you want to use as x axis.
    yDataframe : pd.DataFrame
        The dataframe you want to plot. Each column is a series. Value must be number.
    titleStr : str
        The chart title.
    xLabelStr : str
        The x label
    yLabelStr : str
        The y label
    savePathStr : str
        The path where you want to save the chart

    Returns
    -------
    None
    """
    fig = plt.figure(figsize=(16,11))
    ax = fig.add_subplot(111)
    # height of the bar
    yDict = {}
    for i in yDataframe.columns:
        yDict[i] = list(yDataframe[i])
    x = np.arange(yDataframe.shape[0])

    barWidth = 0.25
    tickLabel = list(xSeries)

    # show the height of bar
    for j,i in enumerate(yDict.values()):
        for q,p in zip(x,i):
            plt.text(q + 0.005+0.24*j, p +0.005, '%.0f' % p, ha='center',va='bottom')
        # plot bar
        plt.bar([o+barWidth*j for o in x], i, barWidth,align="center",label=list(yDict.keys())[j],alpha=0.5)

    plt.xlabel(xLabelStr)
    plt.ylabel(yLabelStr)
    plt.title(titleStr)
    plt.xticks(x + barWidth / yDataframe.shape[0],tickLabel,rotation=45,fontsize=7)
    plt.legend()
    plt.savefig(savePathStr)
    plt.show()


def plot3DScatter(array,xLabelStr,yLabelStr,zLabelStr,titleStr,savePathStr):
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure(figsize=(16,11))
    ax = Axes3D(fig)
    ax.scatter3D(array[:, 0], array[:, 1], array[:, 2])
    ax.set_xlabel(xLabelStr)
    ax.set_ylabel(yLabelStr)
    ax.set_zlabel(zLabelStr)
    plt.title(titleStr)
    plt.legend()
    plt.savefig(savePathStr)
    plt.show()

#<plotTool>
#</plotTool>









