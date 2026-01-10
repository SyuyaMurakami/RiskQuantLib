#!/usr/bin/python
#coding = utf-8

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#<import>
#</import>

def plotLine(df: pd.DataFrame, titleStr: str, xLabelStr: str, yLabelStr: str, savePathStr: str, show: bool = False):
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
    show : bool
        Show it in browser. If false, it will only save file into disk.

    Returns
    -------
    None
    """
    fig = px.line(df, title=titleStr)
    fig.update_layout(
        hovermode=False,
        autosize=True,
        legend_title_text='',
        title = {
            'text': titleStr,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=20)
        },
        xaxis_title=xLabelStr,
        yaxis_title=yLabelStr,
        xaxis=dict(domain=[0.03, 0.97]),
        yaxis=dict(domain=[0.03, 0.97]), 
        margin=dict(l=120, r=120, t=90, b=100),
        legend=dict(x=1.01, y=0.98, xanchor='left', yanchor='top'),
    )
    fig.update_xaxes(tickangle=45, tickfont=dict(size=10), title=dict(standoff=40))
    fig.update_yaxes(title=dict(standoff=40))
    fig.write_image(savePathStr, width=1920, height=1080)
    fig.show() if show else None

def plotBar(df: pd.DataFrame, titleStr: str, xLabelStr: str, yLabelStr: str, savePathStr: str, show: bool = False):
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
    show : bool
        Show it in browser. If false, it will only save file into disk.

    Returns
    -------
    None
    """
    fig = px.bar(df, barmode='group', title=titleStr)
    fig.update_layout(
        hovermode=False,
        autosize=True,
        legend_title_text='',
        title = {
            'text': titleStr,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=20)
        },
        xaxis_title=xLabelStr,
        yaxis_title=yLabelStr,
        xaxis=dict(domain=[0.03, 0.97]),
        yaxis=dict(domain=[0.03, 0.97]), 
        margin=dict(l=120, r=120, t=90, b=100),
        legend=dict(x=1.01, y=0.98, xanchor='left', yanchor='top'),
    )
    fig.update_xaxes(tickangle=45, tickfont=dict(size=10), title=dict(standoff=40))
    fig.update_yaxes(title=dict(standoff=40))
    fig.write_image(savePathStr, width=1920, height=1080)
    fig.show() if show else None

def plotPie(sr: pd.Series, titleStr: str, savePathStr: str, show: bool = False):
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
    show : bool
        Show it in browser. If false, it will only save file into disk.

    Returns
    -------
    None
    """
    fig = px.pie(
        sr, 
        values=sr,
        names=sr.index,
        title=titleStr,
        hole=0.7
    )
    fig.update_traces(
        hoverinfo='skip',
        textposition='outside', 
        textinfo='percent+label',
        textfont_size=20,
        domain=dict(x=[0.1, 0.9], y=[0.1, 0.9]), 
    )
    fig.update_layout(
        hovermode=False,
        autosize=True,
        legend_title_text='',
        title = {
            'text': titleStr,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=20)
        },
        margin=dict(l=150, r=150, t=70, b=90),
        legend=dict(x=0.8, y=0.87, xanchor='left', yanchor='top'),
    )
    fig.write_image(savePathStr, width=1920, height=1080)
    fig.show() if show else None

def plot3DScatter(array: np.ndarray, xLabelStr: str, yLabelStr: str, zLabelStr: str, titleStr: str, savePathStr: str, show: bool = False):
    """
    Plot a 3D scatter chart.

    Parameters
    ----------
    array : np.ndarray
        An array with 3 columns, like [[x1, y1, z1],[x2,y2,z2]].
    xLabelStr : str
        The name of x axis.
    yLabelStr : str
        The name of y axis. 
    zLabelStr : str
        The name of z axis.   
    titleStr : str
        The chart title.
    savePathStr : str
        The path where you want to save the chart
    show : bool
        Show it in browser. If false, it will only save file into disk.

    Returns
    -------
    None
    """
    df = pd.DataFrame(array, columns=[xLabelStr, yLabelStr, zLabelStr])
    fig = px.scatter_3d(
        df, 
        x=xLabelStr, 
        y=yLabelStr, 
        z=zLabelStr,
        title=titleStr
    )
    fig.update_traces(
        marker=dict(
            size=2,
            opacity=0.7,
            line=dict(width=0)
        )
    )
    fig.update_layout(
        hovermode=False,
        autosize=True,
        title={
            'text': titleStr,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=20)
        },
        scene=dict(
            xaxis=dict(title=xLabelStr),
            yaxis=dict(title=yLabelStr),
            zaxis=dict(title=zLabelStr),
            aspectmode='cube',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5), projection=dict(type='perspective')),
        ),
        margin=dict(l=0, r=0, b=0, t=50),
    )
    fig.write_image(savePathStr, width=1920, height=1080)
    fig.show() if show else None

def plot3DSurface(x: np.ndarray, y: np.ndarray, z: np.ndarray, xLabelStr: str, yLabelStr: str, zLabelStr: str, titleStr: str, savePathStr: str, show: bool = False):
    """
    Plot a 3D surface chart.

    Parameters
    ----------
    x : np.ndarray
        One-dimension array, whose length equals the column number of z.
    y : np.ndarray
        One-dimension array, whose length equals the row number of z.
    z : np.ndarray
        Two-dimensions array, which contains the value of surface.
    xLabelStr : str
        The name of x axis.
    yLabelStr : str
        The name of y axis. 
    zLabelStr : str
        The name of z axis.   
    titleStr : str
        The chart title.
    savePathStr : str
        The path where you want to save the chart
    show : bool
        Show it in browser. If false, it will only save file into disk.

    Returns
    -------
    None
    """
    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y, colorscale='plotly3')])
    fig.update_traces(
        hoverinfo='skip',
        colorbar=dict(title=zLabelStr,thickness=20,len=0.5,x=0.8,xanchor='left',yanchor='middle',),
    )
    fig.update_layout(
        hovermode=False,
        autosize=True,
        title={
            'text': titleStr,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=20)
        },
        scene=dict(
            xaxis=dict(title=xLabelStr),
            yaxis=dict(title=yLabelStr),
            zaxis=dict(title=zLabelStr),
            aspectmode='cube', 
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5), 
                projection=dict(type='perspective')
            ),
        ),
        margin=dict(l=0, r=0, b=0, t=50),
    )
    fig.write_image(savePathStr, width=1920, height=1080)
    fig.show() if show else None






#<plotTool>
#</plotTool>




