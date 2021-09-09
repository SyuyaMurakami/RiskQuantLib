#!/usr/bin/python
#coding = utf-8

import numpy as np
import pandas as pd

class getDataFromJYDB():
	def __init__(self,databaseNameString:str,hostAddress:str,port:int,userName:str,passWord:str):
		from RiskQuantLib.Tool.databaseTool import oracleTool
		self.connect = oracleTool(databaseNameString=databaseNameString,hostAddress=hostAddress,port=port,userName=userName,passWord=passWord)

	@staticmethod
	def decoratorQuery(queryFunction):
		"""
		This function deal with the issue that oracle can not query more than 1000 'IN' condition.
		"""
		def decoratedQueryFunction(*args):
			lenNum = len(args[0])
			if lenNum < 1000:
				return queryFunction(*args)
			else:
				splitNum = int(lenNum/1000)+1
				listSplit = [[j for index,j in enumerate(args[0]) if int(index/1000)==i] for i in range(splitNum)]
				args = args[1:]
				result = [queryFunction(i,*args) for i in listSplit]
				return pd.concat(result)
		return decoratedQueryFunction

	@decoratorQuery
	def getSwIndexClose(self,indexCode:list,date:pd.Timestamp):
		"""
		This function returns the close point of ShenWan industry level one index.

		Parameters
		----------
		indexCode : list
			The list of index code.
		date : pd.Timestamp
			The date you want to draw data on.

		Returns
		-------
		pd.DataFrame
		"""
		date = date.strftime("%Y-%m-%d")
		baseSql = f"SELECT s.SECUCODE, s.SECUABBR, qs.TRADINGDAY, qs.CLOSEPRICE FROM JYDB.QT_SYWGINDEXQUOTE qs JOIN JYDB.SECUMAIN s ON qs.INNERCODE = s.INNERCODE WHERE qs.TRADINGDAY = TO_DATE('{date}', 'yyyy-mm-dd')"
		index = "'"+"','".join(indexCode)+"'"
		sql = baseSql + f" AND s.SECUCODE in ({index})"
		data = self.connect.readSql(sql)
		return data

	def getFundAccNav(self,fund : str, date : pd.Timestamp):
		"""
		This function returns fund net asset value after interest adjust.

		Parameters
		----------
		fund : str
			Fund code.
		date : pd.Timestamp
			The date you need to pull the data on.

		Returns
		-------
		pd.DataFrame
		"""
		date = date.strftime("%Y-%m-%d")
		sql = f"SELECT s.SECUCODE , s.SECUABBR, mf.TRADINGDAY, UNITNVRESTORED FROM JYDB.MF_FUNDNETVALUERE mf JOIN JYDB.SECUMAIN s ON mf.INNERCODE = s.INNERCODE WHERE SECUCODE = '{fund}' AND mf.TRADINGDAY = TO_DATE('{date}','yyyy-mm-dd')"
		data = self.connect.readSql(sql)
		return data

	def getFundStockTopTen(self,fund : str, date : pd.Timestamp):
		"""
		This function returns top ten stock holdings of a mutual fund.

		Parameters
		----------
		fund : str
			Fund code.
		date : pd.Timestamp
			The date you need to pull the data on.

		Returns
		-------
		pd.DataFrame
		"""
		date = date.strftime("%Y-%m-%d")
		sql = f"SELECT s.SECUCODE , s.SECUABBR, mk.REPORTDATE, mk.SERIALNUMBER, s2.SECUCODE AS stockcode, s2.SECUABBR AS stockname, mk.RATIOINNV FROM JYDB.MF_KEYSTOCKPORTFOLIO mk JOIN JYDB.SECUMAIN s ON mk.INNERCODE = s.INNERCODE JOIN JYDB.SECUMAIN s2 ON mk.STOCKINNERCODE = s2.INNERCODE WHERE s.SECUCODE = '{fund}' AND mk.REPORTDATE = TO_DATE('{date}','yyyy-mm-dd')"
		data = self.connect.readSql(sql)
		return data

	@decoratorQuery
	def getSecurityCodeAndNameAbbr(self, securityList : list):
		"""
		This function will return the code and name abbr in JYDB.

		Parameters
		----------
		securityList : list
			A string list contains security code.

		Returns
		-------
		pd.DataFrame
		"""
		baseSql = f"SELECT s.SECUCODE, s.SECUABBR FROM JYDB.SECUMAIN s WHERE"
		securities = "'" + "','".join(securityList) + "'"
		sql = baseSql + f" SECUCODE IN ({securities})"
		data = self.connect.readSql(sql)
		return data

	@decoratorQuery
	def getSwIndustryAStockBelongTo(self, securityList: list):
		"""
		This function will return the Shen Wan industry section of stock in JYDB. However, it only
		applies to A share in China.

		Parameters
		----------
		securityList : list
			A string list contains security code.

		Returns
		-------
		pd.DataFrame
		"""
		baseSql = f"SELECT s.SECUCODE, s.SECUABBR, le.FirstIndustryName FROM JYDB.LC_EXGINDUSTRY le JOIN JYDB.SECUMAIN s ON le.COMPANYCODE = s.COMPANYCODE WHERE STANDARD  = 24 AND s.SecuCategory = 1 AND le.canceldate is null"
		securities = "'" + "','".join(securityList) + "'"
		sql = baseSql + f" AND SECUCODE IN ({securities})"
		data = self.connect.readSql(sql)
		return data

	@decoratorQuery
	def getSwIndustrySTARStockBelongTo(self, securityList: list):
		"""
		This function will return the Shen Wan industry section of stock in JYDB. However, it only
		applies to STAR share in China.

		Parameters
		----------
		securityList : list
			A string list contains security code.

		Returns
		-------
		pd.DataFrame
		"""
		baseSql = f"SELECT s.SECUCODE, s.SECUABBR, le.FirstIndustryName FROM JYDB.LC_STIBEXGINDUSTRY le JOIN JYDB.SECUMAIN s ON le.COMPANYCODE = s.COMPANYCODE WHERE STANDARD  = 24 AND s.SecuCategory = 1 AND le.canceldate is null"
		securities = "'" + "','".join(securityList) + "'"
		sql = baseSql + f" AND SECUCODE IN ({securities})"
		data = self.connect.readSql(sql)
		return data

	@decoratorQuery
	def getStockMarketPlate(self, securityList: list):
		"""
		This function will return the exchange trading plate of stock in JYDB.

		Parameters
		----------
		securityList : list
			A string list contains security code.

		Returns
		-------
		pd.DataFrame
		"""
		baseSql = f"SELECT s.SECUCODE, s.SECUABBR, cs.MS FROM JYDB.CT_SYSTEMCONST cs JOIN JYDB.SECUMAIN s ON cs.DM = s.LISTEDSECTOR WHERE LB = 207"
		securities = "'" + "','".join(securityList) + "'"
		sql = baseSql + f" AND SECUCODE IN ({securities})"
		data = self.connect.readSql(sql)
		return data

	@decoratorQuery
	def getStockTradingMarket(self, securityList: list):
		"""
		This function will return the exchange where stock is trading in JYDB.

		Parameters
		----------
		securityList : list
			A string list contains security code.

		Returns
		-------
		pd.DataFrame
		"""
		baseSql = f"SELECT s.SECUCODE, s.SECUABBR, cs.MS FROM JYDB.CT_SYSTEMCONST cs JOIN JYDB.SECUMAIN s ON cs.DM = s.SECUMARKET WHERE LB = 201"
		securities = "'" + "','".join(securityList) + "'"
		sql = baseSql + f" AND SECUCODE IN ({securities})"
		data = self.connect.readSql(sql)
		return data

	@decoratorQuery
	def getIssuer(self, securityList: list):
		"""
		This function returns the issuer of each security.

		Parameters
		----------
		securityList : list
			A string list contains security code.

		Returns
		-------
		pd.DataFrame
		"""
		baseSql = f"SELECT s.SECUCODE, s.SECUABBR, li.CHINAME FROM JYDB.LC_INSTIARCHIVE li JOIN JYDB.SECUMAIN s ON s.COMPANYCODE = li.COMPANYCODE WHERE "
		securities = "'" + "','".join(securityList) + "'"
		sql = baseSql + f"SECUCODE IN ({securities})"
		data = self.connect.readSql(sql)
		return data

	@decoratorQuery
	def getTotalMktValueOfAStock(self, securityList: list, date : pd.Timestamp):
		"""
		This function returns the total outlying market value of each stock, but it only applies in A
		share, China.

		Parameters
		----------
		securityList : list
			A string list contains security code.
		date : pd.Timestamp
			The date you want to pull the data on.

		Returns
		-------
		pd.DataFrame
		"""
		date = date.strftime("%Y-%m-%d")
		baseSql = f"SELECT s.SECUCODE, s.SECUABBR, qp.NEGOTIABLEMV FROM JYDB.QT_PERFORMANCE qp JOIN JYDB.SECUMAIN s ON s.INNERCODE = qp.INNERCODE WHERE qp.TRADINGDAY = TO_DATE('"+date+"','yyyy-mm-dd')"
		securities = "'" + "','".join(securityList) + "'"
		sql = baseSql + f" AND SECUCODE IN ({securities})"
		data = self.connect.readSql(sql)
		return data

	@decoratorQuery
	def getTotalMktValueOfSTARStock(self, securityList: list, date : pd.Timestamp):
		"""
		This function returns the total outlying market value of each stock, but it only applies in STAR, China.

		Parameters
		----------
		securityList : list
			A string list contains security code.
		date : pd.Timestamp
			The date you want to pull the data on.

		Returns
		-------
		pd.DataFrame
		"""
		date = date.strftime("%Y-%m-%d")
		baseSql = f"SELECT s.SECUCODE, s.SECUABBR, qp.NEGOTIABLEMV FROM JYDB.LC_STIBPERFORMANCE qp JOIN JYDB.SECUMAIN s ON s.INNERCODE = qp.INNERCODE WHERE qp.TRADINGDAY = TO_DATE('"+date+"','yyyy-mm-dd')"
		securities = "'" + "','".join(securityList) + "'"
		sql = baseSql + f" AND SECUCODE IN ({securities})"
		data = self.connect.readSql(sql)
		return data