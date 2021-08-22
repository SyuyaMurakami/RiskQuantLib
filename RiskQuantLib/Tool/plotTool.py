#!/usr/bin/python
#coding = utf-8

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['axes.unicode_minus'] = False
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']

def plotLine(df,titleStr,xLabelStr,yLabelStr,savePathStr):
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

def plotPie(df,titleStr,savePathStr):
	fig = plt.figure(figsize=(16,11))
	ax = fig.add_subplot(111)
	plt.pie(df,autopct='%3.2f%%',radius=0.8,labels=df.index)
	plt.title(titleStr)
	plt.savefig(savePathStr)
	plt.show()

def plotBar(df,titleStr,xLabelStr,yLabelStr,savePathStr):
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

def plotMultiBar(xSeries,yDataframe,xLabelStr,yLabelStr,titleStr,savePathStr):
	fig = plt.figure(figsize=(16,11))
	ax = fig.add_subplot(111)
	# 柱高
	yDict = {}
	for i in yDataframe.columns:
		yDict[i] = list(yDataframe[i])
	x = np.arange(yDataframe.shape[0])

	barWidth = 0.25
	tickLabel = list(xSeries)

	# 显示每个柱的具体高度
	for j,i in enumerate(yDict.values()):
		for q,p in zip(x,i):
			plt.text(q + 0.005+0.24*j, p +0.005, '%.0f' % p, ha='center',va='bottom')
		# 绘制柱状图
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











