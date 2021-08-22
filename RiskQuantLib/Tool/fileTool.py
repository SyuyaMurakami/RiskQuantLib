#!/usr/bin/python
#coding = utf-8

import time, os, datetime

def modifyDateIsToday(filePath,mode='M'):
	if mode == 'M':
		modifyDate = os.path.getmtime(filePath)
	elif mode=='C':
		modifyDate = os.path.getctime(filePath)
	else:
		print("Mode Error")
		return
	datetimeModifyDate = datetime.datetime.utcfromtimestamp(modifyDate).strftime("%Y--%m--%d")
	datetimeDateNow = datetime.datetime.now().strftime("%Y--%m--%d")
	if datetimeModifyDate == datetimeDateNow:
		return True
	else:
		return False

def waitForFile(filePath,fileNameKeyWord):
	fileListInPath = [i for i in os.listdir(filePath) if i.find(fileNameKeyWord)!=-1]
	while len(fileListInPath)==0:
		time.sleep(2)
		fileListInPath = [i for i in os.listdir(filePath) if i.find(fileNameKeyWord)!=-1]
	return 0

def dumpVariable(variable,filePath):
	import pickle as pkl
	pkl.dump(variable,open(filePath,"wb"))

def dumpDictToJson(dictVariable,filePath):
	import json
	json.dump(dictVariable,open(filePath,"w",encoding='UTF-8'),ensure_ascii=False)

def clearCachePklFile(filePath):
	print("Clearing Cache in "+filePath)
	fileListInPath = [i for i in os.listdir(filePath) if i.find('.pkl')!=-1]
	while len(fileListInPath)!=0:
		os.system('del "'+filePath+os.sep+'*.pkl"')
		fileListInPath  = [i for i in os.listdir(filePath) if i.find('.pkl')!=-1]
	time.sleep(2)

def findFirstNotNanValueOfSeries(x):
	import numpy as np
	for i in x.values:
		if type(i)==type(np.nan) and np.isnan(i):
			pass
		else:
			return i
	return np.nan

def resetIndexByFirstNotNanValue(df,dropFirst = False):
	df.dropna(axis=0,how='all',inplace=True)
	df.index = df.apply(findFirstNotNanValueOfSeries,axis=1)
	if dropFirst:
		df.drop(columns=[df.columns[0]],inplace=True)

def louverBox(target_df,groupBy = '',insertTo = ''):
	import numpy as np
	tmp_df = target_df.copy()
	groupName  = tmp_df[groupBy].unique()[0]
	tmp_df.reset_index(drop=True, inplace=True)
	tmp_df = tmp_df.drop(columns=[groupBy])
	tmp_df['IF_ASSEMBLE'] = False

	insertList = [np.nansum(tmp_df[i]) if tmp_df[i].dtypes!=np.object else np.nan for i in tmp_df.columns]
	insertList[tmp_df.columns.to_list().index(insertTo)] = groupName
	insertList[tmp_df.columns.to_list().index("IF_ASSEMBLE")] = True
	if tmp_df.shape[0]!=1:
		tmp_df.loc[-1] = insertList
	else:
		tmp_df[insertTo] = groupName
		tmp_df['IF_ASSEMBLE'] = True

	tmp_df.drop_duplicates(inplace=True,keep='first')
	tmp_df.sort_index(inplace=True)
	tmp_df.reset_index(drop=True,inplace=True)
	return tmp_df

def dataFrameLouverBox(df,groupBy='',insertTo=''):
	if insertTo not in df.columns.to_list():
		df[insertTo] = ''
	result = df.groupby(groupBy).apply(lambda x:louverBox(x,groupBy=groupBy,insertTo=insertTo))
	result.reset_index(drop=True,inplace=True)
	return result

def generateFileDictFromPath(filePathString, targetDict = {}, onlyExcel = True):
	import pandas as pd
	fileList = os.listdir(filePathString)
	if onlyExcel:
		fileList = [i for i in fileList if i.find('.xlsx')!=-1 or i.find('.xls')!=-1]
		excelList = [pd.read_excel(filePathString+os.sep+i,index_col=None) for i in fileList]
		fileDict = dict(zip(fileList,excelList))
		[resetIndexByFirstNotNanValue(fileDict[i]) for i in fileList]
		targetDict[filePathString] = dict(zip(fileList,[fileDict[i].to_dict(orient='dict') for i in fileList]))
		return targetDict
	else:
		targetDict[filePathString] = fileList
		return targetDict

def generateDataFrameFromDict(inputDict, dateString, fileNameString, columnNameString):
	import pandas as pd
	df = pd.DataFrame([inputDict.keys(),inputDict.values()], index=['ROW','VALUE']).T
	df['PATH'] = dateString
	df['FILE'] = fileNameString
	df['COLUMN'] = columnNameString
	return df

def compressExcel(filePathString, outputPathString, subDictionary = True):
	import pandas as pd
	import operator
	from functools import reduce
	if subDictionary:
		dirList = [i for i in os.listdir(filePathString) if i.find('.')==-1]
		subDictionaryDict = {}
		[generateFileDictFromPath(filePathString+os.sep+i,subDictionaryDict) for i in dirList]
		dfArray = [[[generateDataFrameFromDict(subDictionaryDict[i][j][k],dateString=i,fileNameString=j,columnNameString=k) for k in subDictionaryDict[i][j].keys()] for j in subDictionaryDict[i].keys()] for i in subDictionaryDict.keys()]
		dfList = reduce(operator.add,dfArray)
		dfList = reduce(operator.add,dfList)
		result = pd.concat(dfList)
		result.reset_index(drop=True,inplace=True)
		result[['PATH','FILE','COLUMN','ROW','VALUE']].to_excel(outputPathString,index=0)
	else:
		dictionaryDict = {}
		generateFileDictFromPath(filePathString,dictionaryDict)
		dfArray = [[[generateDataFrameFromDict(dictionaryDict[i][j][k],dateString=i,fileNameString=j,columnNameString=k) for k in dictionaryDict[i][j].keys()] for j in dictionaryDict[i].keys()] for i in dictionaryDict.keys()]
		dfList = reduce(operator.add,dfArray)
		dfList = reduce(operator.add,dfList)
		result = pd.concat(dfList)
		result.reset_index(drop=True,inplace=True)
		result[['PATH','FILE','COLUMN','ROW','VALUE']].to_excel(outputPathString,index=0)











