#!/usr/bin/python
#coding = utf-8

import numpy as np
import pandas as pd

def decoratorQuery(queryFunction):
	"""
	This function deal with the issue that oracle can not query more than 1000 'IN' condition.
	"""

	def decoratedQueryFunction(*args):
		lenNum = len(args[1])
		if lenNum < 1000:
			return queryFunction(*args)
		else:
			splitNum = int(lenNum / 1000) + 1
			listSplit = [[j for index, j in enumerate(args[1]) if int(index / 1000) == i] for i in range(splitNum)]
			classRef = args[0]
			args = args[2:]
			result = [queryFunction(classRef, i, *args) for i in listSplit]
			return pd.concat(result)

	return decoratedQueryFunction


class getDataFromZYYX():
	def __init__(self,databaseNameString:str,hostAddress:str,port:int,userName:str,passWord:str):
		"""
		Initialize the connect to database.
		"""
		from RiskQuantLib.Tool.databaseTool import oracleTool
		self.databaseNameString = databaseNameString
		self.connect = oracleTool(databaseNameString=databaseNameString,hostAddress=hostAddress,port=port,userName=userName,passWord=passWord)

	@decoratorQuery
	def getStockEstNetProfit(self,stockCode:list,yearString:str,dateString:str):
		"""
		Get Expected Net Profit of analysts.

		Parameters
		----------
		stockCode:list
			The code of stocks that you want to estimate net profit. Each element of
			list should be a six-char string, like 000001.
		yearString:str
			Specify which year's net profit you want to estimate.
		dateString:str
			Specify the estimation date.

		Returns
		-------
		pd.DataFrame
		"""
		date = pd.Timestamp(dateString).strftime("%Y-%m-%d")
		baseSql = f"SELECT CFS.STOCK_CODE, CFS.CON_NP FROM "+self.databaseNameString+f".CON_FORECAST_STK CFS WHERE CFS.CON_YEAR = {yearString} AND CFS.CON_DATE = TO_DATE('{date}','yyyy-mm-dd')"
		index = "'" + "','".join(stockCode)+"'"
		sql = baseSql + f" AND CFS.STOCK_CODE IN ({index})"
		data = self.connect.readSql(sql)
		return data

	@decoratorQuery
	def getStockProfitNoticeDate(self,stockCode:list,dateString:str):
		"""
		Get the Profit Notice Date, given stock code.

		Parameters
		----------
		stockCode:list
			The code of stocks that you want to pull the date when profit notice
			is published. Each element of list should be a six-char string, like 000001.
		dateString:str
			Specify the analysis date. This function will take the quarter of this date
			as the accounting quarter of financial reports, and take the year of this date
			as the accounting year of financial reports. For each stock, the returned
			published date will be the publish date of this unique financial report.

		Returns
		-------
		pd.DataFrame
		"""
		date = pd.Timestamp(dateString)
		reportPeriod = date.quarter
		reportYear = date.year
		baseSql = f"SELECT FPF.STOCK_CODE, FPF.DECLARE_DATE, FPF.TOR_CEILING, FPF.TOR_FLOOR, FPF.ENTRYTIME FROM "+self.databaseNameString+f".FIN_PERFORMANCE_FORECAST FPF WHERE FPF.REPORT_YEAR = {reportYear} AND FPF.REPORT_PERIOD = {reportPeriod}"
		index = "'" + "','".join(stockCode)+"'"
		sql = baseSql + f" AND FPF.STOCK_CODE IN ({index})"
		data = self.connect.readSql(sql)
		return data

