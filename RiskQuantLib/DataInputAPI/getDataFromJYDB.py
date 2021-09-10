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

	@decoratorQuery
	def getBondSubType(self, securityList: list):
		"""
		This function returns the sub type of each bond.

		Parameters
		----------
		securityList : list
			A string list contains security code.

		Returns
		-------
		pd.DataFrame
		"""
		baseSql = f"SELECT s.SECUCODE, s.SECUABBR, cs.MS FROM (JYDB.BOND_BASICINFO bb JOIN JYDB.SECUMAIN s ON s.INNERCODE = bb.INNERCODE) JOIN JYDB.CT_SYSTEMCONST cs ON bb.BONDNATURE = cs.DM WHERE LB='1243'"
		securities = "'" + "','".join(securityList) + "'"
		sql = baseSql + f" AND SECUCODE IN ({securities})"
		data = self.connect.readSql(sql)
		return data

	@decoratorQuery
	def getIssuerRating(self, securityList : list, method = 'CBR', crsystem = 'domestic'):
		"""
		This function returns the issuer rating of issuer.

		Parameters
		----------
		securityList : list
			A list of bond.
		method : str
			Credit rating method, can be 'CBR' or 'Other'.
		crsystem : str
			Name of credit rating system, can be 'domestic', 'foreign' or 'all'.

		Returns
		-------
		pd.DataFrame
		"""
		crsystem_dict = {'domestic':'(1)','foreign':'(2)','all':'(1,2)'}
		baseSql = f"SELECT s.SECUCODE, s.SECUABBR, bc.CRDATE, cs.MS, bc.CRASNAME, bc.CRSYSTEM FROM (JYDB.BOND_COMCREDITGRADING bc JOIN JYDB.SECUMAIN s ON s.COMPANYCODE = bc.COMPANYCODE) JOIN JYDB.CT_SYSTEMCONST cs ON bc.CRCODE = cs.DM WHERE LB IN (1372,2069,2070,2071,2276) AND IVALUE<>3 AND bc.CRSYSTEM IN "+crsystem_dict[crsystem]
		securities = "'" + "','".join(securityList) + "'"
		sql = baseSql + f" AND SECUCODE IN ({securities}) ORDER BY CRDATE"
		data = self.connect.readSql(sql)
		if method == 'CBR':
			data = data[data['crasname']=='中债资信评估有限责任公司']
			data['codeName'] = data['secucode']+data['secuabbr']
			return data.groupby('codeName').apply(lambda x:x[x.crdate == max(x.crdate)])
		else:
			data = data[data['crasname'] != '中债资信评估有限责任公司']
			data['codeName'] = data['secucode'] + data['secuabbr']
			return data.groupby('codeName').apply(lambda x: x[x.crdate == max(x.crdate)])

	@decoratorQuery
	def getBondCBRImpliedRating(self,  securityList: list, date : pd.Timestamp):
		"""
		This function returns the CBR implied rating of bond.

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
		baseSql = f"SELECT s.SECUCODE, s.SECUABBR, bc.UPDATETIME, cs.MS FROM (JYDB.BOND_CBMIR bc JOIN JYDB.SECUMAIN s ON s.INNERCODE = bc.INNERCODE) JOIN JYDB.CT_SYSTEMCONST cs ON bc.IMPLIEDGRADE = cs.DM WHERE LB = 2080 AND UPDATETIME LIKE TO_DATE('" + date + "','yyyy-mm-dd')"
		securities = "'" + "','".join(securityList) + "'"
		sql = baseSql + f" AND SECUCODE IN ({securities})"
		data = self.connect.readSql(sql)
		return data

	@decoratorQuery
	def getBondRating(self, securityList: list):
		"""
		This function returns the rating of each bond.

		Parameters
		----------
		securityList : list
			A string list contains security code.

		Returns
		-------
		pd.DataFrame
		"""
		baseSql = f"SELECT s.SECUCODE, s.SECUABBR, bb.CREDITRATING, bb.CRAS FROM JYDB.BOND_BASICINFO bb JOIN JYDB.SECUMAIN s ON s.INNERCODE = bb.INNERCODE WHERE "
		securities = "'" + "','".join(securityList) + "'"
		sql = baseSql + f" SECUCODE IN ({securities})"
		data = self.connect.readSql(sql)
		return data

	@decoratorQuery
	def getBondCouponRate(self, securityList: list):
		"""
		This function returns the coupon rate of each bond.

		Parameters
		----------
		securityList : list
			A string list contains security code.

		Returns
		-------
		pd.DataFrame
		"""
		baseSql = f"SELECT s.SECUCODE, s.SECUABBR, bb.COUPONRATE FROM JYDB.BOND_BASICINFO bb JOIN JYDB.SECUMAIN s ON s.INNERCODE = bb.INNERCODE WHERE "
		securities = "'" + "','".join(securityList) + "'"
		sql = baseSql + f" SECUCODE IN ({securities})"
		data = self.connect.readSql(sql)
		return data

	@decoratorQuery
	def getBondMaturity(self, securityList: list):
		"""
		This function returns the maturity of each bond.

		Parameters
		----------
		securityList : list
			A string list contains security code.

		Returns
		-------
		pd.DataFrame
		"""
		baseSql = f"SELECT s.SECUCODE, s.SECUABBR, bb.MATURITY FROM JYDB.BOND_BASICINFO bb JOIN JYDB.SECUMAIN s ON s.INNERCODE = bb.INNERCODE WHERE "
		securities = "'" + "','".join(securityList) + "'"
		sql = baseSql + f" SECUCODE IN ({securities})"
		data = self.connect.readSql(sql)
		return data

	@decoratorQuery
	def getBondDuration(self, securityList: list, date : pd.Timestamp):
		"""
		This function returns the valuation duration of each bond.

		Parameters
		----------
		securityList : list
			A string list contains security code.

		Returns
		-------
		pd.DataFrame
		"""
		date = date.strftime("%Y-%m-%d")
		baseSql = f"SELECT s.SECUCODE, s.SECUABBR, bc.VPADURATION, bc.ENDDATE FROM JYDB.BOND_CBVALUATIONALL bc JOIN JYDB.SECUMAIN s ON s.INNERCODE = bc.INNERCODE WHERE ENDDATE LIKE TO_DATE('"+ date + "','yyyy-mm-dd')"
		securities = "'" + "','".join(securityList) + "'"
		sql = baseSql + f" AND SECUCODE IN ({securities})"
		data = self.connect.readSql(sql)
		data.drop_duplicates(inplace=True)
		return data

	@decoratorQuery
	def getBondYTM(self, securityList: list, date : pd.Timestamp):
		"""
		This function returns the valuation YTM of each bond.

		Parameters
		----------
		securityList : list
			A string list contains security code.

		Returns
		-------
		pd.DataFrame
		"""
		date = date.strftime("%Y-%m-%d")
		baseSql = f"SELECT s.SECUCODE, s.SECUABBR, bc.VPYIELD, bc.ENDDATE FROM JYDB.BOND_CBVALUATIONALL bc JOIN JYDB.SECUMAIN s ON s.INNERCODE = bc.INNERCODE WHERE ENDDATE LIKE TO_DATE('"+ date + "','yyyy-mm-dd')"
		securities = "'" + "','".join(securityList) + "'"
		sql = baseSql + f" AND SECUCODE IN ({securities})"
		data = self.connect.readSql(sql)
		data.drop_duplicates(inplace=True)
		return data

	def getAllPublicFund(self, date : pd.Timestamp):
		"""
		This function returns all public fund, given a date.

		Parameters
		----------
		date : pd.Timestamp
			The date you want to pull data on.

		Returns
		-------
		pd.DataFrame
		"""
		date = date.strftime("%Y-%m-%d")
		baseSql = f"SELECT s.SECUCODE, s.SECUABBR FROM JYDB.MF_FUNDARCHIVES mf JOIN JYDB.SECUMAIN s ON s.INNERCODE = mf.INNERCODE WHERE STARTDATE IS NULL OR (TO_DATE('"+ date + "','yyyy-mm-dd')<EXPIREDATE AND TO_DATE('" + date + "','yyyy-mm-dd')>STARTDATE)"
		data = self.connect.readSql(baseSql)
		data.drop_duplicates(inplace=True)
		return data

	@decoratorQuery
	def getFundSubType(self, securityList: list):
		"""
		This function returns the sub type of each fund.

		Parameters
		----------
		securityList : list
			A string list contains security code.

		Returns
		-------
		pd.DataFrame
		"""
		baseSql = f"SELECT s.SECUCODE, s.SECUABBR, cs.MS FROM (JYDB.MF_FUNDARCHIVES mf JOIN JYDB.SECUMAIN s ON s.INNERCODE = mf.INNERCODE) JOIN JYDB.CT_SYSTEMCONST cs ON mf.FUNDTYPECODE = cs.DM WHERE LB = 1249 AND DM IN(1101,1103,1105,1107,1109,1199,1200)"
		securities = "'" + "','".join(securityList) + "'"
		sql = baseSql + f" AND SECUCODE IN ({securities})"
		data = self.connect.readSql(sql)
		data.drop_duplicates(inplace=True)
		return data

	@decoratorQuery
	def getFundInvestmentStyle(self, securityList: list):
		"""
		This function returns the investment style of each fund.

		Parameters
		----------
		securityList : list
			A string list contains security code.

		Returns
		-------
		pd.DataFrame
		"""
		baseSql = f"SELECT s.SECUCODE, s.SECUABBR, cs.MS FROM (JYDB.MF_FUNDARCHIVES mf JOIN JYDB.SECUMAIN s ON s.INNERCODE = mf.INNERCODE) JOIN JYDB.CT_SYSTEMCONST cs ON mf.INVESTMENTTYPE = cs.DM WHERE LB = 1094"
		securities = "'" + "','".join(securityList) + "'"
		sql = baseSql + f" AND SECUCODE IN ({securities})"
		data = self.connect.readSql(sql)
		data.drop_duplicates(inplace=True)
		return data

	@decoratorQuery
	def getFutureUnderlying(self, securityList: list):
		"""
		This function returns the underlying of each future.

		Parameters
		----------
		securityList : list
			A string list contains security code.

		Returns
		-------
		pd.DataFrame
		"""
		baseSql = f"SELECT fc.CONTRACTCODE, fc.CONTRACTABBR, cp.PRODUCTNAME, cs.MS FROM (JYDB.FUT_CONTRACTMAIN fc JOIN JYDB.CT_PRODUCT cp ON fc.OPTIONCODE = cp.PRODUCTCODE) JOIN JYDB.CT_SYSTEMCONST cs ON fc.CONTRACTTYPE = cs.DM WHERE PRODUCTCATEGORY = 326 AND PRODUCTCODE NOT IN (383) AND LB = 1461"
		securities = "'" + "','".join(securityList) + "'"
		sql = baseSql + f" AND CONTRACTCODE IN ({securities})"
		data = self.connect.readSql(sql)
		data.drop_duplicates(inplace=True)
		return data

	def getSwIndustryName(self):
		"""
		This function returns the name of shen wan industry level one.

		Returns
		-------
		pd.DataFrame
		"""
		sql = "SELECT DISTINCT FIRSTINDUSTRYNAME FROM JYDB.LC_EXGINDUSTRY WHERE STANDARD = 24"
		data = self.connect.readSql(sql)
		return data

	def getIndexConstitute(self, index : str, date: pd.Timestamp):
		"""
		This function will return the index constitution.

		Parameters
		----------
		index : str
			Index code.
		date : pd.Timestamp
			The date you want to pull your data on.

		Returns
		-------
		pd.DataFrame
		"""
		date = date.strftime("%Y-%m-%d")
		baseSql = f"SELECT s.SECUCODE, s.SECUABBR, s2.SECUCODE AS STOCKCODE, s2.SECUABBR AS STOCKNAME, WEIGHT, ENDDATE FROM JYDB.LC_INDEXCOMPONENTSWEIGHT li JOIN JYDB.SECUMAIN s ON s.INNERCODE = li.INDEXCODE JOIN JYDB.SECUMAIN s2 ON li.INNERCODE = s2.INNERCODE WHERE s.SECUCODE = '{index}' AND li.ENDDATE = (SELECT max(li.ENDDATE) FROM JYDB.LC_INDEXCOMPONENTSWEIGHT li JOIN JYDB.SECUMAIN s ON li.INDEXCODE = s.INNERCODE WHERE SECUCODE = '{index}' AND li.ENDDATE <= TO_DATE('{date}','yyyy-mm-dd'))"
		data = self.connect.readSql(baseSql)
		data.weight /= 100
		return data

	@decoratorQuery
	def getStockClose(self, securityList: list, date : pd.Timestamp):
		"""
		This function returns the close price of each stock.

		Parameters
		----------
		securityList : list
			A string list contains security code.
		date : pd.Timestamp
			The date you want to pull data on.

		Returns
		-------
		pd.DataFrame
		"""
		date = date.strftime("%Y-%m-%d")
		baseSql = f"SELECT s.SECUCODE, s.SECUABBR, qd.CLOSEPRICE, qd.PREVCLOSEPRICE, qd.TRADINGDAY FROM JYDB.QT_DAILYQUOTE qd JOIN JYDB.SECUMAIN s ON s.INNERCODE = qd.INNERCODE WHERE s.SECUCATEGORY = 1 AND qd.TRADINGDAY LIKE TO_DATE('"+ date + "','yyyy-mm-dd')"
		securities = "'" + "','".join(securityList) + "'"
		sql = baseSql + f" AND SECUCODE IN ({securities})"
		data = self.connect.readSql(sql)
		data.drop_duplicates(inplace=True)
		return data

	@decoratorQuery
	def getTreasureBondYieldCurve(self, date : pd.Timestamp):
		"""
		This function will return the China treasure bond yield curve in inter-bank market.

		Parameters
		----------
		date : pd.Timestamp
			The date you want to pull your data on.

		Returns
		-------
		pd.DataFrame
		"""
		date = date.strftime("%Y-%m-%d")
		baseSql = f"SELECT BC.UPDATETIME, BC.CURVETYPE, BC.YEARSTOMATURITY, BC.YIELD FROM JYDB.BOND_CBYIELDCURVEOPEN BC WHERE BC.CURVECODE = 10 AND BC.UPDATETIME LIKE TO_DATE('{date}', 'yyyy-mm-dd')"
		data = self.connect.readSql(baseSql)
		return data