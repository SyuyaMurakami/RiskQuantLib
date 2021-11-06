#!/usr/bin/python
#coding = utf-8

import numpy as np
import pandas as pd
from WindPy import w

w.start(waitTime=60)

def getHistoricalPCTReturn(securityString,startDateString,endDateString):
	startDate = pd.Timestamp(startDateString)
	endDate = pd.Timestamp(endDateString)
	windData = w.wsd(securityString,"pct_chg",startDate.strftime("%Y-%m-%d"),endDate.strftime("%Y-%m-%d"),"",usedf=True)
	return windData[1].fillna(np.nan)

def getHistoricalClose(securityString,startDateString,endDateString):
	startDate = pd.Timestamp(startDateString)
	endDate = pd.Timestamp(endDateString)
	windData = w.wsd(securityString,"close",startDate.strftime("%Y-%m-%d"),endDate.strftime("%Y-%m-%d"),"",usedf=True)
	return windData[1].fillna(np.nan)

def getFundHistoricalNav(securityString,startDateString,endDateString):
	startDate = pd.Timestamp(startDateString)
	endDate = pd.Timestamp(endDateString)
	windData = w.wsd(securityString,"nav",startDate.strftime("%Y-%m-%d"),endDate.strftime("%Y-%m-%d"),"",usedf=True)
	return windData[1].fillna(np.nan)

def getBondHTMAtDate(securityString,dateString,yieldType='yield_shc'):
	date = pd.Timestamp(dateString)
	if yieldType in ['yield_shc','yield_cnbd','yield_csi1','yield_cfets']:
		windData = w.wss(securityString,yieldType,"tradeDate="+date.strftime("%Y%m%d")+";credibility=1",usedf=True)
		return windData[1].fillna(np.nan)
	elif yieldType == 'YTM_ifexe':
		windData = w.wss(securityString, yieldType, "tradeDate=" + date.strftime("%Y%m%d"), usedf=True)
		return windData[1].fillna(np.nan)
	else:
		return pd.DataFrame()

def getYieldCurve(securityString,startDateString,endDateString):
	startDate = pd.Timestamp(startDateString)
	endDate = pd.Timestamp(endDateString)
	windData = w.edb(securityString,startDate.strftime("%Y-%m-%d"),endDate.strftime("%Y-%m-%d"),"Fill=Previous",usedf=True)
	return windData[1].fillna(np.nan)

def getCTD(securityString,startDateString,endDateString,exchangeType="NIB",TradingCalendar = "CFFEX"):
	startDate = pd.Timestamp(startDateString)
	endDate = pd.Timestamp(endDateString)
	windData = w.wsd(securityString,"tbf_CTD2",startDate.strftime("%Y-%m-%d"),endDate.strftime("%Y-%m-%d"),"exchangeType="+exchangeType+r";bondPriceType=1;TradingCalendar="+TradingCalendar,usedf=True)
	return windData[1].fillna(np.nan)

def getSettlementPrice(securityString,startDateString,endDateString):
	startDate = pd.Timestamp(startDateString)
	endDate = pd.Timestamp(endDateString)
	windData = w.wsd(securityString,"settle",startDate.strftime("%Y-%m-%d"),endDate.strftime("%Y-%m-%d"),"",usedf=True)
	return windData[1].fillna(np.nan)

def convertMonthNumberToString(monthNumber):
	if len(str(int(monthNumber)))==1:
		return '0'+str(int(monthNumber))
	elif len(str(int(monthNumber)))==2:
		return str(int(monthNumber))
	else:
		return ''

def generateDateStringOfPastMonths(month,startDate=pd.Timestamp.now()):
	yearStanding = startDate.year
	monthStanding  = startDate.month
	dateString = [str(yearStanding)+convertMonthNumberToString(monthStanding)]
	for i in range(month):
		if monthStanding == 1:
			monthStanding = 13
			yearStanding = yearStanding - 1
		monthStanding = monthStanding - 1
		dateString.append(str(yearStanding)+convertMonthNumberToString(monthStanding))
	return dateString

def getHistoricalReturnOfIndexFuture(futureCodePastMonth,dataStartDateString,dataEndDateString,futuresCodeList = [],futuresDateStartDate=pd.Timestamp.now()):
	codeDateString = generateDateStringOfPastMonths(futureCodePastMonth,startDate=futuresDateStartDate)
	dfDict = {}
	for i in futuresCodeList:
		futureFullCodeList = [i.split('--')[0]+j[2:]+i.split('--')[1] for j in codeDateString]
		futureFullCodeString = ''.join([j+',' for j in futureFullCodeList]).strip(',')
		dfDict[i] = getCTD(futureFullCodeString,dataStartDateString,dataEndDateString)
	return dfDict

def getCTDOfBondIndexFuture(futureCodePastMonth,dataStartDateString,dataEndDateString,futureCodeList = [],futureDateStartDate = pd.Timestamp.now()):
	dataStartDate = pd.Timestamp(dataStartDateString)
	dataEndDate = pd.Timestamp(dataEndDateString)
	codeDateString = generateDateStringOfPastMonths(futureCodePastMonth,startDate=futureDateStartDate)
	dfDict = {}
	for i in futureCodeList:
		futureFullCodeList = [i.split('--')[0]+j[2:]+i.split('--')[1] for j in codeDateString]
		futureFullCodeString = ''.join([j+',' for j in futureFullCodeList]).strip(',')
		dfDict[i] = getCTD(futureFullCodeString,dataStartDate.strftime("%Y%m%d"),dataEndDate.strftime("%Y%m%d"))
	return dfDict

def getHistoricalReturnOfIndex(indexCodeString,dataStartDateString,dataEndDateString):
	dataStartDate = pd.Timestamp(dataStartDateString)
	dataEndDate = pd.Timestamp(dataEndDateString)
	result = getHistoricalPCTReturn(indexCodeString,dataStartDate.strftime("%Y%m%d"),dataEndDate.strftime("%Y%m%d"))
	return result

def getStockIndustrySection(stockListString,codeType = "industry_gics",industryType = 2):
	windData = w.wss(stockListString,codeType,"industryType="+str(industryType),usedf=True)
	return windData[1].fillna(np.nan)

def getStockListedDate(stockListString):
	windData = w.wss(stockListString, "ipo_date", usedf=True)
	return windData[1].fillna(np.nan)

def getStockProfitNoticeDate(stockListString,dateString):
	date = pd.Timestamp(dateString)
	windData = w.wss(stockListString, "profitnotice_date,profitnotice_netprofitmax,profitnotice_netprofitmin", "rptDate="+date.strftime("%Y%m%d")+";unit=1",usedf=True)
	return windData[1].fillna(np.nan)

def getStockEstNetProfit(stockListString,yearString,dateString):
	date = pd.Timestamp(dateString)
	windData = w.wss(stockListString, "est_netprofit","unit=1;year="+yearString+";tradeDate="+date.strftime("%Y%m%d"),usedf=True)
	return windData[1].fillna(np.nan)

def getCompanyFinancialReportPredictPublishDate(stockListString,dateString):
	date = pd.Timestamp(dateString)
	windData = w.wss(stockListString, "stm_predict_issuingdate", "rptDate="+date.strftime("%Y%m%d")+";unit=1",usedf=True)
	return windData[1].fillna(np.nan)

def getAllStockOfSector(dateString,windSectorID = 'a001010100000000'):
	date = pd.Timestamp(dateString)
	windData = w.wset("sectorconstituent","date="+date.strftime("%Y-%m-%d")+";sectorid="+windSectorID,usedf=True)
	return windData[1].fillna(np.nan)

def getStockTotalMarketValue(stockString,startDateString,endDateString):
	startDate = pd.Timestamp(startDateString)
	endDate = pd.Timestamp(endDateString)
	windData = w.wsd(stockString,"ev",startDate.strftime("%Y-%m-%d"),endDate.strftime("%Y-%m-%d"),"unit=1",usedf=True)
	return windData[1].fillna(np.nan)

def getStockDailyTradingAmount(stockString,startDateString,endDateString):
	startDate = pd.Timestamp(startDateString)
	endDate = pd.Timestamp(endDateString)
	windData = w.wsd(stockString,"amt",startDate.strftime("%Y-%m-%d"),endDate.strftime("%Y-%m-%d"),"",usedf=True)
	return windData[1].fillna(np.nan)


def getUnlockedShareDetail(stockListString,dateString):
	date = pd.Timestamp(dateString)
	windData = w.wss(stockListString, "share_rtd_unlockingdate_fwd,share_tradable_current_fwd,share_tradable_sharetype_fwd", "tradeDate="+date.strftime("%Y%m%d")+";unit=1",usedf=True)
	return windData[1].fillna(np.nan)

def getAmountOfFreeTradedShare(stockListString,dateString):
	date = pd.Timestamp(dateString)
	windData = w.wss(stockListString, "free_float_shares", "unit=1;tradeDate="+date.strftime("%Y%m%d"),usedf=True)
	return windData[1].fillna(np.nan)

def getStockPERelativeToIndustryAverage(stockListString,dateString):
	date = pd.Timestamp(dateString)
	windData = w.wss(stockListString, "val_peindu_sw", "tradeDate="+date.strftime("%Y%m%d"),usedf=True)
	return windData[1].fillna(np.nan)

def getWhetherCanBeShorted(stockListString,dateString):
	date = pd.Timestamp(dateString)
	windData = w.wss(stockListString, "marginornot", "tradeDate="+date.strftime("%Y%m%d"),usedf=True)
	return windData[1].fillna(np.nan)

def getIndexConstituteStockWeight(indexString,baseDateString):
	baseDate = pd.Timestamp(baseDateString)
	windData = w.wset("indexconstituent","date="+baseDate.strftime("%Y-%m-%d")+";windcode="+indexString,usedf=True)
	return windData[1].fillna(np.nan)

def getIssuerName(securityString):
	windData = w.wss(securityString,"comp_name",usedf=True)
	return windData[1].fillna(np.nan)

def getIssuerCity(securityString,tradeDateString):
	tradeDate = pd.Timestamp(tradeDateString)
	windData = w.wss(securityString,"province","adminType=1;tradeDate="+tradeDate.strftime("%Y%m%d"),usedf=True)
	return windData[1].fillna(np.nan)

def getBondCouponRate(securityString,couponRateType = 'couponrate2'):
	windData = w.wss(securityString,couponRateType,usedf=True)
	return windData[1].fillna(np.nan)

def getTradingDayAndPreTradingDayClose(securityString,tradeDateString):
	tradeDate = pd.Timestamp(tradeDateString)
	windData = w.wss(securityString,"pre_close,close","tradeDate="+tradeDate.strftime("%Y%m%d")+";priceAdj=U;cycle=D",usedf=True)
	return windData[1].fillna(np.nan)

def getBondWindClassificationType(securityString,classificationType = "windl2type"):
	windData = w.wss(securityString,classificationType,usedf=True)
	return windData[1].fillna(np.nan)

def getSecurityName(securityString):
	windData = w.wss(securityString, "sec_name",usedf=True)
	return windData[1].fillna(np.nan)

def getAvergaeTradingAmount(securityString,startDateString,endDateString):
	startDate = pd.Timestamp(startDateString)
	endDate = pd.Timestamp(endDateString)
	windData = w.wss(securityString,"vol_per,avg_vol_per","unit=1;startDate="+startDate.strftime("%Y%m%d")+";endDate="+endDate.strftime("%Y%m%d"),usedf=True)
	return windData[1].fillna(np.nan)

def getBondIssuranceInfo(securityString):
	windData = w.wss(securityString,"agency_underwrittype,issue_firstissue,issue_lastissue,abs_creditnormal",usedf=True)
	windData.rename(columns=dict(zip(windData.columns,['承销方式','发行起始日期','发行截止日期','承销团成员'])),inplace=True)
	return windData[1].fillna(np.nan)

def getSecurityFromTheSameIssuer(securityString):
	windData = w.wset("identicalissuer","windcode="+securityString+";field=windcode,secname,issuedate,bondtype")
	issuerName = w.wss(securityString,"issuerupdated")
	df = pd.DataFrame(windData.Data,columns=windData.Codes,index=windData.Fields).T
	df['Issuer'] = issuerName.Data[0][0]
	return df.fillna(np.nan)

def getIndexFutureForwardPremiumSeries(securityString,startDateString,endDateString):
	startDate = pd.Timestamp(startDateString)
	endDate = pd.Timestamp(endDateString)
	windData = w.wsd(securityString,"if_basis",startDate.strftime("%Y-%m-%d"),endDate.strftime("%Y-%m-%d"),"",usedf=True)
	return windData[1].fillna(np.nan)

def getMaturityDate(securityString):
	windData = w.wss(securityString,"maturitydate",usedf=True)
	return windData[1].fillna(np.nan)

def getOptionExerciseDateOfBond(securityString):
	windData = w.wss(securityString,"repurchasedate,redemptiondate",usedf=True)
	return windData[1].fillna(np.nan)












