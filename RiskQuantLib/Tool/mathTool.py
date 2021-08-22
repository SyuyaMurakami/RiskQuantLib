#!/usr/bin/python
#coding = utf-8

import numpy as np

def percentageOfSeries(dataList,percentage):# 求分位数
	length = len(dataList)
	sortedData = sorted(dataList,reverse=True)
	return sortedData[int(percentage/100*length)]

def interP1d(xList,yList,Kind='cubic'):# 三次线性插值
	from scipy.interpolate import interp1d
	x = np.array(xList)
	y = np.array(yList)
	model = interp1d(x,y,kind=Kind,fill_value='extrapolate')
	return model

def linearRegression(xList,yList):# 线性回归
	from sklearn.linear_model import LinearRegression
	x = np.array(xList).reshape(-1,1)
	y = np.array(yList).reshape(-1,1)

	model = LinearRegression()
	model.fit(x,y)
	return model

def maxDropDown(dataList,valueType = 'Relative'):
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
	if type(x) == type(np.nan) and np.isnan(x):
		return True
	else:
		return False















