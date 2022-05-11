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

# build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here
#-<Begin>
# 获取报告期末投资组合平均剩余期限时间序列
from windget import getMmAvgPtMSeries


# 获取报告期末投资组合平均剩余期限
from windget import getMmAvgPtM


# 获取报告期内投资组合平均剩余期限最高值时间序列
from windget import getMmAvgPtMMaxSeries


# 获取报告期内投资组合平均剩余期限最高值
from windget import getMmAvgPtMMax


# 获取报告期内投资组合平均剩余期限最低值时间序列
from windget import getMmAvgPtMMinSeries


# 获取报告期内投资组合平均剩余期限最低值
from windget import getMmAvgPtMMin


# 获取按信用评级的债券投资市值时间序列
from windget import getPrtBondByCreditRatingSeries


# 获取按信用评级的债券投资市值
from windget import getPrtBondByCreditRating


# 获取按信用评级的资产支持证券投资市值时间序列
from windget import getPrtAbsByCreditRatingSeries


# 获取按信用评级的资产支持证券投资市值
from windget import getPrtAbsByCreditRating


# 获取按信用评级的同业存单投资市值时间序列
from windget import getPrtNcdByCreditRatingSeries


# 获取按信用评级的同业存单投资市值
from windget import getPrtNcdByCreditRating


# 获取按信用评级的债券投资占基金资产净值比时间序列
from windget import getPrtBondByCreditRatingToNavSeries


# 获取按信用评级的债券投资占基金资产净值比
from windget import getPrtBondByCreditRatingToNav


# 获取按信用评级的资产支持证券投资占基金资产净值比时间序列
from windget import getPrtAbsByCreditRatingToNavSeries


# 获取按信用评级的资产支持证券投资占基金资产净值比
from windget import getPrtAbsByCreditRatingToNav


# 获取按信用评级的同业存单投资占基金资产净值比时间序列
from windget import getPrtNcdByCreditRatingToNavSeries


# 获取按信用评级的同业存单投资占基金资产净值比
from windget import getPrtNcdByCreditRatingToNav


# 获取债券估值(YY)时间序列
from windget import getInStYyBondValSeries


# 获取债券估值(YY)
from windget import getInStYyBondVal


# 获取债券估值历史(YY)时间序列
from windget import getInStYyBondValHisSeries


# 获取债券估值历史(YY)
from windget import getInStYyBondValHis


# 获取融资融券余额时间序列
from windget import getMrgBalSeries


# 获取融资融券余额
from windget import getMrgBal


# 获取融资融券担保股票市值时间序列
from windget import getMarginGuaranteedStocksMarketValueSeries


# 获取融资融券担保股票市值
from windget import getMarginGuaranteedStocksMarketValue


# 获取是否融资融券标的时间序列
from windget import getMarginOrNotSeries


# 获取是否融资融券标的
from windget import getMarginOrNot


# 获取区间融资融券余额均值时间序列
from windget import getMrgBalIntAvgSeries


# 获取区间融资融券余额均值
from windget import getMrgBalIntAvg


# 获取利息收入:融资融券业务时间序列
from windget import getStmNoteSec1511Series


# 获取利息收入:融资融券业务
from windget import getStmNoteSec1511


# 获取利息净收入:融资融券业务时间序列
from windget import getStmNoteSec1531Series


# 获取利息净收入:融资融券业务
from windget import getStmNoteSec1531


# 获取涨跌_期货历史同月时间序列
from windget import getHisChangeSeries


# 获取涨跌_期货历史同月
from windget import getHisChange


# 获取振幅_期货历史同月时间序列
from windget import getHisSwingSeries


# 获取振幅_期货历史同月
from windget import getHisSwing


# 获取收盘价_期货历史同月时间序列
from windget import getHisCloseSeries


# 获取收盘价_期货历史同月
from windget import getHisClose


# 获取开盘价_期货历史同月时间序列
from windget import getHisOpenSeries


# 获取开盘价_期货历史同月
from windget import getHisOpen


# 获取最高价_期货历史同月时间序列
from windget import getHisHighSeries


# 获取最高价_期货历史同月
from windget import getHisHigh


# 获取最低价_期货历史同月时间序列
from windget import getHisLowSeries


# 获取最低价_期货历史同月
from windget import getHisLow


# 获取结算价_期货历史同月时间序列
from windget import getHisSettleSeries


# 获取结算价_期货历史同月
from windget import getHisSettle


# 获取涨跌幅_期货历史同月时间序列
from windget import getHisPctChangeSeries


# 获取涨跌幅_期货历史同月
from windget import getHisPctChange


# 获取成交量_期货历史同月时间序列
from windget import getHisVolumeSeries


# 获取成交量_期货历史同月
from windget import getHisVolume


# 获取成交额_期货历史同月时间序列
from windget import getHisTurnoverSeries


# 获取成交额_期货历史同月
from windget import getHisTurnover


# 获取持仓量_期货历史同月时间序列
from windget import getHisOiSeries


# 获取持仓量_期货历史同月
from windget import getHisOi


# 获取前结算价_期货历史同月时间序列
from windget import getHisPreSettleSeries


# 获取前结算价_期货历史同月
from windget import getHisPreSettle


# 获取成交均价_期货历史同月时间序列
from windget import getHisAvgPriceSeries


# 获取成交均价_期货历史同月
from windget import getHisAvgPrice


# 获取持仓变化_期货历史同月时间序列
from windget import getHisOiChangeSeries


# 获取持仓变化_期货历史同月
from windget import getHisOiChange


# 获取收盘价(夜盘)_期货历史同月时间序列
from windget import getHisCloseNightSeries


# 获取收盘价(夜盘)_期货历史同月
from windget import getHisCloseNight


# 获取涨跌(结算价)_期货历史同月时间序列
from windget import getHisChangeSettlementSeries


# 获取涨跌(结算价)_期货历史同月
from windget import getHisChangeSettlement


# 获取涨跌幅(结算价)_期货历史同月时间序列
from windget import getHisPctChangeSettlementSeries


# 获取涨跌幅(结算价)_期货历史同月
from windget import getHisPctChangeSettlement


# 获取业绩预告摘要时间序列
from windget import getProfitNoticeAbstractSeries


# 获取业绩预告摘要
from windget import getProfitNoticeAbstract


# 获取业绩预告变动原因时间序列
from windget import getProfitNoticeReasonSeries


# 获取业绩预告变动原因
from windget import getProfitNoticeReason


# 获取业绩预告类型时间序列
from windget import getProfitNoticeStyleSeries


# 获取业绩预告类型
from windget import getProfitNoticeStyle


# 获取业绩预告最新披露日期时间序列
from windget import getProfitNoticeDateSeries


# 获取业绩预告最新披露日期
from windget import getProfitNoticeDate


# 获取业绩预告首次披露日期时间序列
from windget import getProfitNoticeFirstDateSeries


# 获取业绩预告首次披露日期
from windget import getProfitNoticeFirstDate


# 获取最新业绩预告报告期时间序列
from windget import getProfitNoticeLastRpTDateSeries


# 获取最新业绩预告报告期
from windget import getProfitNoticeLastRpTDate


# 获取单季度.业绩预告摘要(海外)时间序列
from windget import getQProfitNoticeAbstractSeries


# 获取单季度.业绩预告摘要(海外)
from windget import getQProfitNoticeAbstract


# 获取单季度.业绩预告类型(海外)时间序列
from windget import getQProfitNoticeStyleSeries


# 获取单季度.业绩预告类型(海外)
from windget import getQProfitNoticeStyle


# 获取单季度.业绩预告日期(海外)时间序列
from windget import getQProfitNoticeDateSeries


# 获取单季度.业绩预告日期(海外)
from windget import getQProfitNoticeDate


# 获取业绩快报最新披露日期时间序列
from windget import getPerformanceExpressLastDateSeries


# 获取业绩快报最新披露日期
from windget import getPerformanceExpressLastDate


# 获取业绩快报首次披露日期时间序列
from windget import getPerformanceExpressDateSeries


# 获取业绩快报首次披露日期
from windget import getPerformanceExpressDate


# 获取业绩快报.营业收入时间序列
from windget import getPerformanceExpressPerFExIncomeSeries


# 获取业绩快报.营业收入
from windget import getPerformanceExpressPerFExIncome


# 获取业绩快报.营业利润时间序列
from windget import getPerformanceExpressPerFExprOfItSeries


# 获取业绩快报.营业利润
from windget import getPerformanceExpressPerFExprOfIt


# 获取业绩快报.利润总额时间序列
from windget import getPerformanceExpressPerFExTotalProfitSeries


# 获取业绩快报.利润总额
from windget import getPerformanceExpressPerFExTotalProfit


# 获取业绩快报.归属母公司股东的净利润时间序列
from windget import getPerformanceExpressPerFExNetProfitToShareholderSeries


# 获取业绩快报.归属母公司股东的净利润
from windget import getPerformanceExpressPerFExNetProfitToShareholder


# 获取业绩快报.归属于上市公司股东的扣除非经常性损益的净利润时间序列
from windget import getPerformanceExpressNpdEdToShareholderSeries


# 获取业绩快报.归属于上市公司股东的扣除非经常性损益的净利润
from windget import getPerformanceExpressNpdEdToShareholder


# 获取业绩快报.每股收益EPS-基本时间序列
from windget import getPerformanceExpressPerFExEpsDilutedSeries


# 获取业绩快报.每股收益EPS-基本
from windget import getPerformanceExpressPerFExEpsDiluted


# 获取业绩快报.净资产收益率ROE-加权时间序列
from windget import getPerformanceExpressPerFExRoeDilutedSeries


# 获取业绩快报.净资产收益率ROE-加权
from windget import getPerformanceExpressPerFExRoeDiluted


# 获取业绩快报.总资产时间序列
from windget import getPerformanceExpressPerFExTotalAssetsSeries


# 获取业绩快报.总资产
from windget import getPerformanceExpressPerFExTotalAssets


# 获取业绩快报.净资产时间序列
from windget import getPerformanceExpressPerFExNetAssetsSeries


# 获取业绩快报.净资产
from windget import getPerformanceExpressPerFExNetAssets


# 获取业绩快报.同比增长率:营业收入时间序列
from windget import getPerformanceExpressOrYoYSeries


# 获取业绩快报.同比增长率:营业收入
from windget import getPerformanceExpressOrYoY


# 获取业绩快报.同比增长率:营业利润时间序列
from windget import getPerformanceExpressOpYoYSeries


# 获取业绩快报.同比增长率:营业利润
from windget import getPerformanceExpressOpYoY


# 获取业绩快报.同比增长率:利润总额时间序列
from windget import getPerformanceExpressEBtYoYSeries


# 获取业绩快报.同比增长率:利润总额
from windget import getPerformanceExpressEBtYoY


# 获取业绩快报.同比增长率:归属母公司股东的净利润时间序列
from windget import getPerformanceExpressNpYoYSeries


# 获取业绩快报.同比增长率:归属母公司股东的净利润
from windget import getPerformanceExpressNpYoY


# 获取业绩快报.同比增长率:归属于上市公司股东的扣除非经常性损益的净利润时间序列
from windget import getPerformanceExpressNpdEdYoYSeries


# 获取业绩快报.同比增长率:归属于上市公司股东的扣除非经常性损益的净利润
from windget import getPerformanceExpressNpdEdYoY


# 获取业绩快报.同比增长率:基本每股收益时间序列
from windget import getPerformanceExpressEpsYoYSeries


# 获取业绩快报.同比增长率:基本每股收益
from windget import getPerformanceExpressEpsYoY


# 获取业绩快报.同比增减:加权平均净资产收益率时间序列
from windget import getPerformanceExpressRoeYoYSeries


# 获取业绩快报.同比增减:加权平均净资产收益率
from windget import getPerformanceExpressRoeYoY


# 获取业绩快报.去年同期营业收入时间序列
from windget import getPerformanceExpressIncomeYaSeries


# 获取业绩快报.去年同期营业收入
from windget import getPerformanceExpressIncomeYa


# 获取业绩快报.去年同期营业利润时间序列
from windget import getPerformanceExpressProfitYaSeries


# 获取业绩快报.去年同期营业利润
from windget import getPerformanceExpressProfitYa


# 获取业绩快报.去年同期利润总额时间序列
from windget import getPerformanceExpressToTProfitYaSeries


# 获取业绩快报.去年同期利润总额
from windget import getPerformanceExpressToTProfitYa


# 获取业绩快报.去年同期净利润时间序列
from windget import getPerformanceExpressNetProfitYaSeries


# 获取业绩快报.去年同期净利润
from windget import getPerformanceExpressNetProfitYa


# 获取业绩快报.上年同期归属于上市公司股东的扣除非经常性损益的净利润时间序列
from windget import getPerformanceExpressNpdEdYaSeries


# 获取业绩快报.上年同期归属于上市公司股东的扣除非经常性损益的净利润
from windget import getPerformanceExpressNpdEdYa


# 获取业绩快报.去年同期每股收益时间序列
from windget import getPerformanceExpressEpsYaSeries


# 获取业绩快报.去年同期每股收益
from windget import getPerformanceExpressEpsYa


# 获取业绩快报.每股净资产时间序列
from windget import getPerformanceExpressBpSSeries


# 获取业绩快报.每股净资产
from windget import getPerformanceExpressBpS


# 获取业绩快报.期初净资产时间序列
from windget import getPerformanceExpressNetAssetsBSeries


# 获取业绩快报.期初净资产
from windget import getPerformanceExpressNetAssetsB


# 获取业绩快报.期初每股净资产时间序列
from windget import getPerformanceExpressBpSBSeries


# 获取业绩快报.期初每股净资产
from windget import getPerformanceExpressBpSB


# 获取业绩快报.比年初增长率:归属母公司的股东权益时间序列
from windget import getPerformanceExpressEqYGrowthSeries


# 获取业绩快报.比年初增长率:归属母公司的股东权益
from windget import getPerformanceExpressEqYGrowth


# 获取业绩快报.比年初增长率:归属于母公司股东的每股净资产时间序列
from windget import getPerformanceExpressBpSGrowthSeries


# 获取业绩快报.比年初增长率:归属于母公司股东的每股净资产
from windget import getPerformanceExpressBpSGrowth


# 获取业绩快报.比年初增长率:总资产时间序列
from windget import getPerformanceExpressToTAssetsGrowthSeries


# 获取业绩快报.比年初增长率:总资产
from windget import getPerformanceExpressToTAssetsGrowth


# 获取最新业绩快报报告期时间序列
from windget import getPerformanceExpressLastRpTDateSeries


# 获取最新业绩快报报告期
from windget import getPerformanceExpressLastRpTDate


# 获取年度可转债发行量时间序列
from windget import getRelatedCbYearlyAmountSeries


# 获取年度可转债发行量
from windget import getRelatedCbYearlyAmount


# 获取基金发行协调人时间序列
from windget import getIssueCoordinatorSeries


# 获取基金发行协调人
from windget import getIssueCoordinator


# 获取上市基金发行价格时间序列
from windget import getIssuePriceSeries


# 获取上市基金发行价格
from windget import getIssuePrice


# 获取基金分红收益_FUND时间序列
from windget import getStmIs82Series


# 获取基金分红收益_FUND
from windget import getStmIs82


# 获取基金规模时间序列
from windget import getFundFundScaleSeries


# 获取基金规模
from windget import getFundFundScale


# 获取基金规模(合计)时间序列
from windget import getNetAssetTotalSeries


# 获取基金规模(合计)
from windget import getNetAssetTotal


# 获取所属国民经济行业分类时间序列
from windget import getIndustryNcSeries


# 获取所属国民经济行业分类
from windget import getIndustryNc


# 获取管理层年度薪酬总额时间序列
from windget import getStmNoteMGmtBenSeries


# 获取管理层年度薪酬总额
from windget import getStmNoteMGmtBen


# 获取管理层增持价格时间序列
from windget import getHolderPriceMhSeries


# 获取管理层增持价格
from windget import getHolderPriceMh


# 获取中资中介机构持股数量时间序列
from windget import getShareCnSeries


# 获取中资中介机构持股数量
from windget import getShareCn


# 获取国际中介机构持股数量时间序列
from windget import getShareOsSeries


# 获取国际中介机构持股数量
from windget import getShareOs


# 获取中资中介机构持股占比时间序列
from windget import getSharePctCnSeries


# 获取中资中介机构持股占比
from windget import getSharePctCn


# 获取国际中介机构持股占比时间序列
from windget import getSharePctOsSeries


# 获取国际中介机构持股占比
from windget import getSharePctOs


# 获取香港本地中介机构持股数量时间序列
from windget import getShareHkSeries


# 获取香港本地中介机构持股数量
from windget import getShareHk


# 获取香港本地中介机构持股占比时间序列
from windget import getSharePctHkSeries


# 获取香港本地中介机构持股占比
from windget import getSharePctHk


# 获取机构调研家数时间序列
from windget import getIrNoIiSeries


# 获取机构调研家数
from windget import getIrNoIi


# 获取机构调研首日时间序列
from windget import getIrIRfdSeries


# 获取机构调研首日
from windget import getIrIRfd


# 获取机构调研最新日时间序列
from windget import getIrIrlDSeries


# 获取机构调研最新日
from windget import getIrIrlD


# 获取投资机构调研次数时间序列
from windget import getIrNoSoIiSeries


# 获取投资机构调研次数
from windget import getIrNoSoIi


# 获取投资机构调研家数时间序列
from windget import getIrNoIiiiSeries


# 获取投资机构调研家数
from windget import getIrNoIiii


# 获取外资机构调研次数时间序列
from windget import getIrNosOfISeries


# 获取外资机构调研次数
from windget import getIrNosOfI


# 获取外资机构调研家数时间序列
from windget import getIrNoIiFiSeries


# 获取外资机构调研家数
from windget import getIrNoIiFi


# 获取流通A股占总股本比例时间序列
from windget import getShareLiqAPctSeries


# 获取流通A股占总股本比例
from windget import getShareLiqAPct


# 获取限售A股占总股本比例时间序列
from windget import getShareRestrictedAPctSeries


# 获取限售A股占总股本比例
from windget import getShareRestrictedAPct


# 获取A股合计占总股本比例时间序列
from windget import getShareTotalAPctSeries


# 获取A股合计占总股本比例
from windget import getShareTotalAPct


# 获取流通B股占总股本比例时间序列
from windget import getShareLiqBPctSeries


# 获取流通B股占总股本比例
from windget import getShareLiqBPct


# 获取限售B股占总股本比例时间序列
from windget import getShareRestrictedBPctSeries


# 获取限售B股占总股本比例
from windget import getShareRestrictedBPct


# 获取B股合计占总股本比例时间序列
from windget import getShareTotalBPctSeries


# 获取B股合计占总股本比例
from windget import getShareTotalBPct


# 获取三板A股占总股本比例时间序列
from windget import getShareOtcAPctSeries


# 获取三板A股占总股本比例
from windget import getShareOtcAPct


# 获取三板B股占总股本比例时间序列
from windget import getShareOtcBPctSeries


# 获取三板B股占总股本比例
from windget import getShareOtcBPct


# 获取三板合计占总股本比例时间序列
from windget import getShareTotalOtcPctSeries


# 获取三板合计占总股本比例
from windget import getShareTotalOtcPct


# 获取香港上市股占总股本比例时间序列
from windget import getShareLiqHPctSeries


# 获取香港上市股占总股本比例
from windget import getShareLiqHPct


# 获取海外上市股占总股本比例时间序列
from windget import getShareOverSeaPctSeries


# 获取海外上市股占总股本比例
from windget import getShareOverSeaPct


# 获取流通股合计占总股本比例时间序列
from windget import getShareTradablePctSeries


# 获取流通股合计占总股本比例
from windget import getShareTradablePct


# 获取限售股合计占总股本比例时间序列
from windget import getShareRestrictedPctSeries


# 获取限售股合计占总股本比例
from windget import getShareRestrictedPct


# 获取自由流通股占总股本比例时间序列
from windget import getShareFreeFloatsHrPctSeries


# 获取自由流通股占总股本比例
from windget import getShareFreeFloatsHrPct


# 获取未平仓卖空数占总股本比例时间序列
from windget import getShortSellShortIntRestPctSeries


# 获取未平仓卖空数占总股本比例
from windget import getShortSellShortIntRestPct


# 获取股改前非流通股占总股本比例时间序列
from windget import getShareNonTradablePctSeries


# 获取股改前非流通股占总股本比例
from windget import getShareNonTradablePct


# 获取质押股份数量合计时间序列
from windget import getSharePledgedASeries


# 获取质押股份数量合计
from windget import getSharePledgedA


# 获取基金份额时间序列
from windget import getUnitTotalSeries


# 获取基金份额
from windget import getUnitTotal


# 获取基金份额(合计)时间序列
from windget import getUnitFundShareTotalSeries


# 获取基金份额(合计)
from windget import getUnitFundShareTotal


# 获取基金份额变化时间序列
from windget import getUnitChangeSeries


# 获取基金份额变化
from windget import getUnitChange


# 获取基金份额变化率时间序列
from windget import getUnitChangeRateSeries


# 获取基金份额变化率
from windget import getUnitChangeRate


# 获取基金份额持有人户数时间序列
from windget import getHolderNumberSeries


# 获取基金份额持有人户数
from windget import getHolderNumber


# 获取基金份额持有人户数(合计)时间序列
from windget import getFundHolderTotalNumberSeries


# 获取基金份额持有人户数(合计)
from windget import getFundHolderTotalNumber


# 获取基金份额变动日期时间序列
from windget import getUnitChangeDateSeries


# 获取基金份额变动日期
from windget import getUnitChangeDate


# 获取本期基金份额交易产生的基金净值变动数时间序列
from windget import getStmNavChange9Series


# 获取本期基金份额交易产生的基金净值变动数
from windget import getStmNavChange9


# 获取ETF基金份额折算日时间序列
from windget import getFundFundShareTranslationDateSeries


# 获取ETF基金份额折算日
from windget import getFundFundShareTranslationDate


# 获取ETF基金份额折算比例时间序列
from windget import getFundFundShareTranslationRatioSeries


# 获取ETF基金份额折算比例
from windget import getFundFundShareTranslationRatio


# 获取本期向基金份额持有人分配利润产生的基金净值变动数时间序列
from windget import getStmNavChange10Series


# 获取本期向基金份额持有人分配利润产生的基金净值变动数
from windget import getStmNavChange10


# 获取单季度.基金份额净值增长率时间序列
from windget import getQAnalNavReturnSeries


# 获取单季度.基金份额净值增长率
from windget import getQAnalNavReturn


# 获取单季度.基金份额净值增长率标准差时间序列
from windget import getQAnalStdNavReturnSeries


# 获取单季度.基金份额净值增长率标准差
from windget import getQAnalStdNavReturn


# 获取平均每户持有基金份额时间序列
from windget import getHolderAvgHoldingSeries


# 获取平均每户持有基金份额
from windget import getHolderAvgHolding


# 获取单季度.累计基金份额净值增长率时间序列
from windget import getQAnalAccumulatedNavReturnSeries


# 获取单季度.累计基金份额净值增长率
from windget import getQAnalAccumulatedNavReturn


# 获取单季度.加权平均基金份额本期利润时间序列
from windget import getQAnalAvgNetIncomePerUnitSeries


# 获取单季度.加权平均基金份额本期利润
from windget import getQAnalAvgNetIncomePerUnit


# 获取单季度.加权平均基金份额本期净收益时间序列
from windget import getQAnalAvgUnitIncomeSeries


# 获取单季度.加权平均基金份额本期净收益
from windget import getQAnalAvgUnitIncome


# 获取报告期末可供分配基金份额利润时间序列
from windget import getAnalDIsTriButAblePerUnitSeries


# 获取报告期末可供分配基金份额利润
from windget import getAnalDIsTriButAblePerUnit


# 获取单季度.报告期期末基金份额净值时间序列
from windget import getQAnalNavSeries


# 获取单季度.报告期期末基金份额净值
from windget import getQAnalNav


# 获取股东户数时间序列
from windget import getHolderNumSeries


# 获取股东户数
from windget import getHolderNum


# 获取机构持股数量合计时间序列
from windget import getHolderTotalByInStSeries


# 获取机构持股数量合计
from windget import getHolderTotalByInSt


# 获取机构持股比例合计时间序列
from windget import getHolderPctByInStSeries


# 获取机构持股比例合计
from windget import getHolderPctByInSt


# 获取上清所债券分类时间序列
from windget import getSHClearL1TypeSeries


# 获取上清所债券分类
from windget import getSHClearL1Type


# 获取标准券折算比例时间序列
from windget import getRateOfStdBndSeries


# 获取标准券折算比例
from windget import getRateOfStdBnd


# 获取转股条款时间序列
from windget import getClauseConversion2ToSharePriceAdjustItemSeries


# 获取转股条款
from windget import getClauseConversion2ToSharePriceAdjustItem


# 获取赎回条款时间序列
from windget import getClauseCallOptionRedeemItemSeries


# 获取赎回条款
from windget import getClauseCallOptionRedeemItem


# 获取时点赎回条款全文时间序列
from windget import getClauseCallOptionRedeemClauseSeries


# 获取时点赎回条款全文
from windget import getClauseCallOptionRedeemClause


# 获取巨额赎回条款时间序列
from windget import getMassRedemptionProvisionSeries


# 获取巨额赎回条款
from windget import getMassRedemptionProvision


# 获取是否有时点赎回条款时间序列
from windget import getClauseCallOptionIsWithTimeRedemptionClauseSeries


# 获取是否有时点赎回条款
from windget import getClauseCallOptionIsWithTimeRedemptionClause


# 获取条件回售条款全文时间序列
from windget import getClausePutOptionSellBackItemSeries


# 获取条件回售条款全文
from windget import getClausePutOptionSellBackItem


# 获取时点回售条款全文时间序列
from windget import getClausePutOptionTimePutBackClauseSeries


# 获取时点回售条款全文
from windget import getClausePutOptionTimePutBackClause


# 获取无条件回售条款时间序列
from windget import getClausePutOptionPutBackClauseSeries


# 获取无条件回售条款
from windget import getClausePutOptionPutBackClause


# 获取最新评级月份时间序列
from windget import getRatingLatestMonthSeries


# 获取最新评级月份
from windget import getRatingLatestMonth


# 获取发行人最新评级时间序列
from windget import getLatestIsSurerCreditRatingSeries


# 获取发行人最新评级
from windget import getLatestIsSurerCreditRating


# 获取发行人最新评级展望时间序列
from windget import getRatingOutlooksSeries


# 获取发行人最新评级展望
from windget import getRatingOutlooks


# 获取发行人最新评级日期时间序列
from windget import getLatestIsSurerCreditRatingDateSeries


# 获取发行人最新评级日期
from windget import getLatestIsSurerCreditRatingDate


# 获取发行人最新评级日期(指定机构)时间序列
from windget import getLatestRatingDateSeries


# 获取发行人最新评级日期(指定机构)
from windget import getLatestRatingDate


# 获取发行人最新评级变动方向时间序列
from windget import getRateLateIssuerChNgSeries


# 获取发行人最新评级变动方向
from windget import getRateLateIssuerChNg


# 获取发行人最新评级评级类型时间序列
from windget import getLatestIsSurerCreditRatingTypeSeries


# 获取发行人最新评级评级类型
from windget import getLatestIsSurerCreditRatingType


# 获取担保人最新评级时间序列
from windget import getLatestRatingOfGuarantorSeries


# 获取担保人最新评级
from windget import getLatestRatingOfGuarantor


# 获取担保人最新评级展望时间序列
from windget import getRateLateGuarantorFwdSeries


# 获取担保人最新评级展望
from windget import getRateLateGuarantorFwd


# 获取担保人最新评级日期时间序列
from windget import getRateLateGuarantorDateSeries


# 获取担保人最新评级日期
from windget import getRateLateGuarantorDate


# 获取担保人最新评级变动方向时间序列
from windget import getRateLateGuaranTorchNgSeries


# 获取担保人最新评级变动方向
from windget import getRateLateGuaranTorchNg


# 获取债券国际评级时间序列
from windget import getRateBond2Series


# 获取债券国际评级
from windget import getRateBond2


# 获取发行人国际评级时间序列
from windget import getIssuer2Series


# 获取发行人国际评级
from windget import getIssuer2


# 获取回购代码时间序列
from windget import getRepoCodeSeries


# 获取回购代码
from windget import getRepoCode


# 获取标的债券时间序列
from windget import getRepoUBondSeries


# 获取标的债券
from windget import getRepoUBond


# 获取发行时标的债券余额时间序列
from windget import getCrmUbonDouStandingAmountSeries


# 获取发行时标的债券余额
from windget import getCrmUbonDouStandingAmount


# 获取回购类型时间序列
from windget import getRepoTypeSeries


# 获取回购类型
from windget import getRepoType


# 获取回购天数时间序列
from windget import getRepoDaysSeries


# 获取回购天数
from windget import getRepoDays


# 获取凭证起始日时间序列
from windget import getCrmCarryDateSeries


# 获取凭证起始日
from windget import getCrmCarryDate


# 获取标的实体交易代码时间序列
from windget import getCrmSubjectCodeSeries


# 获取标的实体交易代码
from windget import getCrmSubjectCode


# 获取履约保障机制时间序列
from windget import getCrmPerformGuaranteeSeries


# 获取履约保障机制
from windget import getCrmPerformGuarantee


# 获取信用事件时间序列
from windget import getCrmCreditEventSeries


# 获取信用事件
from windget import getCrmCreditEvent


# 获取债券信用状态时间序列
from windget import getCreditBondCreditStatusSeries


# 获取债券信用状态
from windget import getCreditBondCreditStatus


# 获取发行人首次违约日时间序列
from windget import getIssuerFirstDefaultDateSeries


# 获取发行人首次违约日
from windget import getIssuerFirstDefaultDate


# 获取登记机构时间序列
from windget import getCrmRegisterAgencySeries


# 获取登记机构
from windget import getCrmRegisterAgency


# 获取标的实体时间序列
from windget import getCrmSubjectSeries


# 获取标的实体
from windget import getCrmSubject


# 获取发布机构时间序列
from windget import getCrmIssuerSeries


# 获取发布机构
from windget import getCrmIssuer


# 获取簿记建档日时间序列
from windget import getCrmBookkeepingDateSeries


# 获取簿记建档日
from windget import getCrmBookkeepingDate


# 获取付费方式时间序列
from windget import getCrmPaymentTermsSeries


# 获取付费方式
from windget import getCrmPaymentTerms


# 获取创设价格时间序列
from windget import getCrmStartingPriceSeries


# 获取创设价格
from windget import getCrmStartingPrice


# 获取创设批准文件编号时间序列
from windget import getCrmPermissionNumberSeries


# 获取创设批准文件编号
from windget import getCrmPermissionNumber


# 获取凭证登记日时间序列
from windget import getCrmDateOfRecordSeries


# 获取凭证登记日
from windget import getCrmDateOfRecord


# 获取第三方基金分类时间序列
from windget import getFundThirdPartyFundTypeSeries


# 获取第三方基金分类
from windget import getFundThirdPartyFundType


# 获取Wind封闭式开放式基金分类时间序列
from windget import getFundProdTypeOcWindSeries


# 获取Wind封闭式开放式基金分类
from windget import getFundProdTypeOcWind


# 获取基金经理时间序列
from windget import getFundFundManagerOfTradeDateSeries


# 获取基金经理
from windget import getFundFundManagerOfTradeDate


# 获取基金经理(现任)时间序列
from windget import getFundFundManagerSeries


# 获取基金经理(现任)
from windget import getFundFundManager


# 获取基金经理(历任)时间序列
from windget import getFundPRedFundManagerSeries


# 获取基金经理(历任)
from windget import getFundPRedFundManager


# 获取基金经理(成立)时间序列
from windget import getFundInceptionFundManagerSeries


# 获取基金经理(成立)
from windget import getFundInceptionFundManager


# 获取基金经理年限时间序列
from windget import getFundManagerManagerWorkingYearsSeries


# 获取基金经理年限
from windget import getFundManagerManagerWorkingYears


# 获取基金经理平均年限时间序列
from windget import getFundAverageWorkingYearsSeries


# 获取基金经理平均年限
from windget import getFundAverageWorkingYears


# 获取基金经理最大年限时间序列
from windget import getFundMaxWorkingYearsSeries


# 获取基金经理最大年限
from windget import getFundMaxWorkingYears


# 获取基金经理指数区间回报(算术平均)时间序列
from windget import getFundManagerIndexReturnSeries


# 获取基金经理指数区间回报(算术平均)
from windget import getFundManagerIndexReturn


# 获取基金经理指数收益标准差(算术平均)时间序列
from windget import getFundManagerIndexStDevSeries


# 获取基金经理指数收益标准差(算术平均)
from windget import getFundManagerIndexStDev


# 获取基金经理指数年化波动率(算术平均)时间序列
from windget import getFundManagerIndexStDevYearlySeries


# 获取基金经理指数年化波动率(算术平均)
from windget import getFundManagerIndexStDevYearly


# 获取基金经理指数最大回撤(算术平均)时间序列
from windget import getFundManagerIndexMaxDownsideSeries


# 获取基金经理指数最大回撤(算术平均)
from windget import getFundManagerIndexMaxDownside


# 获取基金经理指数区间回报(规模加权)时间序列
from windget import getFundManagerIndexWeightReturnSeries


# 获取基金经理指数区间回报(规模加权)
from windget import getFundManagerIndexWeightReturn


# 获取基金经理指数收益标准差(规模加权)时间序列
from windget import getFundManagerIndexWeightStDevSeries


# 获取基金经理指数收益标准差(规模加权)
from windget import getFundManagerIndexWeightStDev


# 获取基金经理指数年化波动率(规模加权)时间序列
from windget import getFundManagerIndexWeightStDevYearlySeries


# 获取基金经理指数年化波动率(规模加权)
from windget import getFundManagerIndexWeightStDevYearly


# 获取基金经理指数最大回撤(规模加权)时间序列
from windget import getFundManagerIndexWeightMaxDownsideSeries


# 获取基金经理指数最大回撤(规模加权)
from windget import getFundManagerIndexWeightMaxDownside


# 获取基金经理数时间序列
from windget import getFundCorpFundManagersNoSeries


# 获取基金经理数
from windget import getFundCorpFundManagersNo


# 获取基金经理成熟度时间序列
from windget import getFundCorpFundManagerMaturitySeries


# 获取基金经理成熟度
from windget import getFundCorpFundManagerMaturity


# 获取代管基金经理说明时间序列
from windget import getFundManagerProxyForManagerSeries


# 获取代管基金经理说明
from windget import getFundManagerProxyForManager


# 获取Beta(基金经理指数,算术平均)时间序列
from windget import getFundManagerIndexBetaSeries


# 获取Beta(基金经理指数,算术平均)
from windget import getFundManagerIndexBeta


# 获取Beta(基金经理指数,规模加权)时间序列
from windget import getFundManagerIndexWeightBetaSeries


# 获取Beta(基金经理指数,规模加权)
from windget import getFundManagerIndexWeightBeta


# 获取Alpha(基金经理指数,算术平均)时间序列
from windget import getFundManagerIndexAlphaSeries


# 获取Alpha(基金经理指数,算术平均)
from windget import getFundManagerIndexAlpha


# 获取Alpha(基金经理指数,规模加权)时间序列
from windget import getFundManagerIndexWeightAlphaSeries


# 获取Alpha(基金经理指数,规模加权)
from windget import getFundManagerIndexWeightAlpha


# 获取Sharpe(基金经理指数,算术平均)时间序列
from windget import getFundManagerIndexSharpeSeries


# 获取Sharpe(基金经理指数,算术平均)
from windget import getFundManagerIndexSharpe


# 获取Sharpe(基金经理指数,规模加权)时间序列
from windget import getFundManagerIndexWeightSharpeSeries


# 获取Sharpe(基金经理指数,规模加权)
from windget import getFundManagerIndexWeightSharpe


# 获取Treynor(基金经理指数,算术平均)时间序列
from windget import getFundManagerIndexTreyNorSeries


# 获取Treynor(基金经理指数,算术平均)
from windget import getFundManagerIndexTreyNor


# 获取Treynor(基金经理指数,规模加权)时间序列
from windget import getFundManagerIndexWeightTreyNorSeries


# 获取Treynor(基金经理指数,规模加权)
from windget import getFundManagerIndexWeightTreyNor


# 获取任职期限最长的现任基金经理时间序列
from windget import getFundManagerLongestFundManagerSeries


# 获取任职期限最长的现任基金经理
from windget import getFundManagerLongestFundManager


# 获取基金公司调研次数时间序列
from windget import getIrFcsSeries


# 获取基金公司调研次数
from windget import getIrFcs


# 获取基金公司调研家数时间序列
from windget import getIrNoFciSeries


# 获取基金公司调研家数
from windget import getIrNoFci


# 获取网下基金公司或其资管子公司配售数量时间序列
from windget import getFundReItsFmSSeries


# 获取网下基金公司或其资管子公司配售数量
from windget import getFundReItsFmS


# 获取网下基金公司或其资管子公司配售金额时间序列
from windget import getFundReItsFMmSeries


# 获取网下基金公司或其资管子公司配售金额
from windget import getFundReItsFMm


# 获取网下基金公司或其资管子公司配售份额占比时间序列
from windget import getFundReItsFMrSeries


# 获取网下基金公司或其资管子公司配售份额占比
from windget import getFundReItsFMr


# 获取网下基金公司或其资管计划配售数量时间序列
from windget import getFundReItsFmAsSeries


# 获取网下基金公司或其资管计划配售数量
from windget import getFundReItsFmAs


# 获取网下基金公司或其资管机构配售金额时间序列
from windget import getFundReItsFmAmSeries


# 获取网下基金公司或其资管机构配售金额
from windget import getFundReItsFmAm


# 获取网下基金公司或其资管计划配售份额占比时间序列
from windget import getFundReItsFMarSeries


# 获取网下基金公司或其资管计划配售份额占比
from windget import getFundReItsFMar


# 获取所属基金公司重仓行业市值时间序列
from windget import getPrtStockValueHoldingIndustryMktValue2Series


# 获取所属基金公司重仓行业市值
from windget import getPrtStockValueHoldingIndustryMktValue2


# 获取调研最多的基金公司时间序列
from windget import getIrTmRfcSeries


# 获取调研最多的基金公司
from windget import getIrTmRfc


# 获取开始交易日时间序列
from windget import getFtDateSeries


# 获取开始交易日
from windget import getFtDate


# 获取开始交易日(支持历史)时间序列
from windget import getFtDateNewSeries


# 获取开始交易日(支持历史)
from windget import getFtDateNew


# 获取最后交易日时间序列
from windget import getLastTradeDateSeries


# 获取最后交易日
from windget import getLastTradeDate


# 获取最后交易日(支持历史)时间序列
from windget import getLtDateNewSeries


# 获取最后交易日(支持历史)
from windget import getLtDateNew


# 获取最后交易日说明时间序列
from windget import getLtDatedSeries


# 获取最后交易日说明
from windget import getLtDated


# 获取最后交易日期时间序列
from windget import getLastTradingDateSeries


# 获取最后交易日期
from windget import getLastTradingDate


# 获取B股最后交易日时间序列
from windget import getDivLastTrDDateShareBSeries


# 获取B股最后交易日
from windget import getDivLastTrDDateShareB


# 获取(废弃)最后交易日时间序列
from windget import getLastTradingDaySeries


# 获取(废弃)最后交易日
from windget import getLastTradingDay


# 获取股权登记日(B股最后交易日)时间序列
from windget import getRightsIssueRegDateShareBSeries


# 获取股权登记日(B股最后交易日)
from windget import getRightsIssueRegDateShareB


# 获取最后交割日时间序列
from windget import getLastDeliveryDateSeries


# 获取最后交割日
from windget import getLastDeliveryDate


# 获取最后交割日(支持历史)时间序列
from windget import getLdDateNewSeries


# 获取最后交割日(支持历史)
from windget import getLdDateNew


# 获取交割月份时间序列
from windget import getDlMonthSeries


# 获取交割月份
from windget import getDlMonth


# 获取挂牌基准价时间序列
from windget import getLPriceSeries


# 获取挂牌基准价
from windget import getLPrice


# 获取期货交易手续费时间序列
from windget import getTransactionFeeSeries


# 获取期货交易手续费
from windget import getTransactionFee


# 获取期货交割手续费时间序列
from windget import getDeliveryFeeSeries


# 获取期货交割手续费
from windget import getDeliveryFee


# 获取期货平今手续费时间序列
from windget import getTodayPositionFeeSeries


# 获取期货平今手续费
from windget import getTodayPositionFee


# 获取交易品种时间序列
from windget import getScCodeSeries


# 获取交易品种
from windget import getScCode


# 获取交易保证金时间序列
from windget import getMarginSeries


# 获取交易保证金
from windget import getMargin


# 获取最初交易保证金时间序列
from windget import getFtMarginsSeries


# 获取最初交易保证金
from windget import getFtMargins


# 获取权益乘数(剔除客户交易保证金)时间序列
from windget import getStmNoteSec1853Series


# 获取权益乘数(剔除客户交易保证金)
from windget import getStmNoteSec1853


# 获取期货多头保证金(支持历史)时间序列
from windget import getLongMarginSeries


# 获取期货多头保证金(支持历史)
from windget import getLongMargin


# 获取期货空头保证金(支持历史)时间序列
from windget import getShortMarginSeries


# 获取期货空头保证金(支持历史)
from windget import getShortMargin


# 获取报价单位时间序列
from windget import getPunItSeries


# 获取报价单位
from windget import getPunIt


# 获取涨跌幅限制时间序列
from windget import getChangeLtSeries


# 获取涨跌幅限制
from windget import getChangeLt


# 获取涨跌幅限制(支持历史)时间序列
from windget import getChangeLtNewSeries


# 获取涨跌幅限制(支持历史)
from windget import getChangeLtNew


# 获取最小变动价位时间序列
from windget import getMfPriceSeries


# 获取最小变动价位
from windget import getMfPrice


# 获取最小变动价位(支持历史)时间序列
from windget import getMfPrice1Series


# 获取最小变动价位(支持历史)
from windget import getMfPrice1


# 获取标准合约上市日时间序列
from windget import getContractIssueDateSeries


# 获取标准合约上市日
from windget import getContractIssueDate


# 获取合约乘数时间序列
from windget import getExeRatioSeries


# 获取合约乘数
from windget import getExeRatio


# 获取合约月份说明时间序列
from windget import getCdMonthsSeries


# 获取合约月份说明
from windget import getCdMonths


# 获取最新交易时间说明时间序列
from windget import getTHoursSeries


# 获取最新交易时间说明
from windget import getTHours


# 获取交割日期说明时间序列
from windget import getDDateSeries


# 获取交割日期说明
from windget import getDDate


# 获取月合约代码时间序列
from windget import getTradeHisCodeSeries


# 获取月合约代码
from windget import getTradeHisCode


# 获取期货合约所属行业时间序列
from windget import getIndustryFuSeries


# 获取期货合约所属行业
from windget import getIndustryFu


# 获取期权代码(指定行权价)时间序列
from windget import getOptionsTradeCodeSeries


# 获取期权代码(指定行权价)
from windget import getOptionsTradeCode


# 获取平值期权代码时间序列
from windget import getAtmCodeSeries


# 获取平值期权代码
from windget import getAtmCode


# 获取期权交易代码时间序列
from windget import getTradeCodeSeries


# 获取期权交易代码
from windget import getTradeCode


# 获取标的代码时间序列
from windget import getUsCodeSeries


# 获取标的代码
from windget import getUsCode


# 获取标的简称时间序列
from windget import getUsNameSeries


# 获取标的简称
from windget import getUsName


# 获取基础资产/标的类型时间序列
from windget import getUsTypeSeries


# 获取基础资产/标的类型
from windget import getUsType


# 获取行权方式时间序列
from windget import getExeModeSeries


# 获取行权方式
from windget import getExeMode


# 获取行权类型时间序列
from windget import getExeTypeSeries


# 获取行权类型
from windget import getExeType


# 获取行权价格时间序列
from windget import getExePriceSeries


# 获取行权价格
from windget import getExePrice


# 获取股权激励行权价格时间序列
from windget import getHolderPriceStockBasedCompensationSeries


# 获取股权激励行权价格
from windget import getHolderPriceStockBasedCompensation


# 获取期权维持保证金(支持历史)时间序列
from windget import getMainTMarginSeries


# 获取期权维持保证金(支持历史)
from windget import getMainTMargin


# 获取总存续期时间序列
from windget import getTotalTmSeries


# 获取总存续期
from windget import getTotalTm


# 获取起始交易日期时间序列
from windget import getStartDateSeries


# 获取起始交易日期
from windget import getStartDate


# 获取起始行权日期时间序列
from windget import getExeStartDateSeries


# 获取起始行权日期
from windget import getExeStartDate


# 获取最后行权日期时间序列
from windget import getExeEnddateSeries


# 获取最后行权日期
from windget import getExeEnddate


# 获取交割方式时间序列
from windget import getSettlementMethodSeries


# 获取交割方式
from windget import getSettlementMethod


# 获取前收盘价时间序列
from windget import getPreCloseSeries


# 获取前收盘价
from windget import getPreClose


# 获取区间前收盘价时间序列
from windget import getPreClosePerSeries


# 获取区间前收盘价
from windget import getPreClosePer


# 获取标的前收盘价时间序列
from windget import getUsPreCloseSeries


# 获取标的前收盘价
from windget import getUsPreClose


# 获取正股区间前收盘价时间序列
from windget import getCbPqStockPreCloseSeries


# 获取正股区间前收盘价
from windget import getCbPqStockPreClose


# 获取开盘价时间序列
from windget import getOpenSeries


# 获取开盘价
from windget import getOpen


# 获取开盘价(不前推)时间序列
from windget import getOpen3Series


# 获取开盘价(不前推)
from windget import getOpen3


# 获取区间开盘价时间序列
from windget import getOpenPerSeries


# 获取区间开盘价
from windget import getOpenPer


# 获取标的开盘价时间序列
from windget import getUsOpenSeries


# 获取标的开盘价
from windget import getUsOpen


# 获取正股区间开盘价时间序列
from windget import getCbPqStockOpenSeries


# 获取正股区间开盘价
from windget import getCbPqStockOpen


# 获取上市首日开盘价时间序列
from windget import getIpoOpenSeries


# 获取上市首日开盘价
from windget import getIpoOpen


# 获取最高价时间序列
from windget import getHighSeries


# 获取最高价
from windget import getHigh


# 获取最高价(不前推)时间序列
from windget import getHigh3Series


# 获取最高价(不前推)
from windget import getHigh3


# 获取区间最高价时间序列
from windget import getHighPerSeries


# 获取区间最高价
from windget import getHighPer


# 获取区间最高价日时间序列
from windget import getHighDatePerSeries


# 获取区间最高价日
from windget import getHighDatePer


# 获取标的最高价时间序列
from windget import getUsHighSeries


# 获取标的最高价
from windget import getUsHigh


# 获取区间自最高价的最大跌幅时间序列
from windget import getPctChgLowestPerSeries


# 获取区间自最高价的最大跌幅
from windget import getPctChgLowestPer


# 获取正股区间最高价时间序列
from windget import getCbPqStockHighSeries


# 获取正股区间最高价
from windget import getCbPqStockHigh


# 获取上市首日最高价时间序列
from windget import getIpoHighSeries


# 获取上市首日最高价
from windget import getIpoHigh


# 获取被剔除的最高价申报量占比时间序列
from windget import getPohQeSeries


# 获取被剔除的最高价申报量占比
from windget import getPohQe


# 获取最新价较区间最高价跌幅(回撤)时间序列
from windget import getPctChgLowPerSeries


# 获取最新价较区间最高价跌幅(回撤)
from windget import getPctChgLowPer


# 获取LN(最近一个月最高价/最近一个月最低价)_PIT时间序列
from windget import getTechLnHighLow20DSeries


# 获取LN(最近一个月最高价/最近一个月最低价)_PIT
from windget import getTechLnHighLow20D


# 获取最低价时间序列
from windget import getLowSeries


# 获取最低价
from windget import getLow


# 获取最低价(不前推)时间序列
from windget import getLow3Series


# 获取最低价(不前推)
from windget import getLow3


# 获取区间最低价时间序列
from windget import getLowPerSeries


# 获取区间最低价
from windget import getLowPer


# 获取区间最低价日时间序列
from windget import getLowDatePerSeries


# 获取区间最低价日
from windget import getLowDatePer


# 获取标的最低价时间序列
from windget import getUsLowSeries


# 获取标的最低价
from windget import getUsLow


# 获取区间自最低价的最大涨幅时间序列
from windget import getPctChgHighestPerSeries


# 获取区间自最低价的最大涨幅
from windget import getPctChgHighestPer


# 获取正股区间最低价时间序列
from windget import getCbPqStockLowSeries


# 获取正股区间最低价
from windget import getCbPqStockLow


# 获取上市首日最低价时间序列
from windget import getIpoLowSeries


# 获取上市首日最低价
from windget import getIpoLow


# 获取预测涨跌幅(评级日,最低价)时间序列
from windget import getEstPctChangeSeries


# 获取预测涨跌幅(评级日,最低价)
from windget import getEstPctChange


# 获取收盘价时间序列
from windget import getCloseSeries


# 获取收盘价
from windget import getClose


# 获取收盘价(支持定点复权)时间序列
from windget import getClose2Series


# 获取收盘价(支持定点复权)
from windget import getClose2


# 获取收盘价(不前推)时间序列
from windget import getClose3Series


# 获取收盘价(不前推)
from windget import getClose3


# 获取收盘价(23:30)时间序列
from windget import getCloseFxSeries


# 获取收盘价(23:30)
from windget import getCloseFx


# 获取收盘价(美元)时间序列
from windget import getCloseUsdSeries


# 获取收盘价(美元)
from windget import getCloseUsd


# 获取收盘价(夜盘)时间序列
from windget import getCloseNightSeries


# 获取收盘价(夜盘)
from windget import getCloseNight


# 获取收盘价标准差时间序列
from windget import getRiskStDevCloseSeries


# 获取收盘价标准差
from windget import getRiskStDevClose


# 获取收盘价(全价)时间序列
from windget import getDirtyPriceSeries


# 获取收盘价(全价)
from windget import getDirtyPrice


# 获取收盘价(净价)时间序列
from windget import getCleanPriceSeries


# 获取收盘价(净价)
from windget import getCleanPrice


# 获取收盘价久期时间序列
from windget import getDurationSeries


# 获取收盘价久期
from windget import getDuration


# 获取收盘价修正久期时间序列
from windget import getModifiedDurationSeries


# 获取收盘价修正久期
from windget import getModifiedDuration


# 获取收盘价凸性时间序列
from windget import getConvexitySeries


# 获取收盘价凸性
from windget import getConvexity


# 获取区间收盘价时间序列
from windget import getClosePerSeries


# 获取区间收盘价
from windget import getClosePer


# 获取N日收盘价1/4分位数时间序列
from windget import get1StQuartIleSeries


# 获取N日收盘价1/4分位数
from windget import get1StQuartIle


# 获取N日收盘价中位数时间序列
from windget import getMedianSeries


# 获取N日收盘价中位数
from windget import getMedian


# 获取N日收盘价3/4分位数时间序列
from windget import get3RdQuartIleSeries


# 获取N日收盘价3/4分位数
from windget import get3RdQuartIle


# 获取标的收盘价时间序列
from windget import getUsCloseSeries


# 获取标的收盘价
from windget import getUsClose


# 获取5日收盘价三重指数平滑移动平均指标_PIT时间序列
from windget import getTechTrix5Series


# 获取5日收盘价三重指数平滑移动平均指标_PIT
from windget import getTechTrix5


# 获取推N日收盘价(债券)时间序列
from windget import getNQOriginCloseSeries


# 获取推N日收盘价(债券)
from windget import getNQOriginClose


# 获取推N日收盘价(当日结算价)时间序列
from windget import getNQCloseSeries


# 获取推N日收盘价(当日结算价)
from windget import getNQClose


# 获取10日收盘价三重指数平滑移动平均指标_PIT时间序列
from windget import getTechTrix10Series


# 获取10日收盘价三重指数平滑移动平均指标_PIT
from windget import getTechTrix10


# 获取涨跌幅(收盘价)时间序列
from windget import getPctChangeCloseSeries


# 获取涨跌幅(收盘价)
from windget import getPctChangeClose


# 获取正股区间收盘价时间序列
from windget import getCbPqStockCloseSeries


# 获取正股区间收盘价
from windget import getCbPqStockClose


# 获取区间最高收盘价时间序列
from windget import getMaxClosePerSeries


# 获取区间最高收盘价
from windget import getMaxClosePer


# 获取区间最低收盘价时间序列
from windget import getMinClosePerSeries


# 获取区间最低收盘价
from windget import getMinClosePer


# 获取区间最高收盘价日时间序列
from windget import getMaxCloseDatePerSeries


# 获取区间最高收盘价日
from windget import getMaxCloseDatePer


# 获取区间最低收盘价日时间序列
from windget import getMinCloseDatePerSeries


# 获取区间最低收盘价日
from windget import getMinCloseDatePer


# 获取N日日均收盘价(算术平均)时间序列
from windget import getAvgClosePerSeries


# 获取N日日均收盘价(算术平均)
from windget import getAvgClosePer


# 获取上市首日收盘价时间序列
from windget import getIpoCloseSeries


# 获取上市首日收盘价
from windget import getIpoClose


# 获取新股开板日收盘价时间序列
from windget import getIpoLimitUpOpenDateCloseSeries


# 获取新股开板日收盘价
from windget import getIpoLimitUpOpenDateClose


# 获取BBI除以收盘价_PIT时间序列
from windget import getTechBBicSeries


# 获取BBI除以收盘价_PIT
from windget import getTechBBic


# 获取上证固收平台收盘价时间序列
from windget import getCloseFixedIncomeSeries


# 获取上证固收平台收盘价
from windget import getCloseFixedIncome


# 获取正股区间最高收盘价时间序列
from windget import getCbPqStockHighCloseSeries


# 获取正股区间最高收盘价
from windget import getCbPqStockHighClose


# 获取正股区间最低收盘价时间序列
from windget import getCbPqStockLowCloseSeries


# 获取正股区间最低收盘价
from windget import getCbPqStockLowClose


# 获取成交量时间序列
from windget import getVolumeSeries


# 获取成交量
from windget import getVolume


# 获取成交量(含大宗交易)时间序列
from windget import getVolumEBTInSeries


# 获取成交量(含大宗交易)
from windget import getVolumEBTIn


# 获取成交量比上交易日增减时间序列
from windget import getOiVolumeCSeries


# 获取成交量比上交易日增减
from windget import getOiVolumeC


# 获取成交量进榜会员名称时间序列
from windget import getOiVNameSeries


# 获取成交量进榜会员名称
from windget import getOiVName


# 获取成交量认沽认购比率时间序列
from windget import getVolumeRatioSeries


# 获取成交量认沽认购比率
from windget import getVolumeRatio


# 获取成交量的5日指数移动平均_PIT时间序列
from windget import getTechVemA5Series


# 获取成交量的5日指数移动平均_PIT
from windget import getTechVemA5


# 获取成交量的10日指数移动平均_PIT时间序列
from windget import getTechVemA10Series


# 获取成交量的10日指数移动平均_PIT
from windget import getTechVemA10


# 获取成交量的12日指数移动平均_PIT时间序列
from windget import getTechVemA12Series


# 获取成交量的12日指数移动平均_PIT
from windget import getTechVemA12


# 获取成交量的26日指数移动平均_PIT时间序列
from windget import getTechVemA26Series


# 获取成交量的26日指数移动平均_PIT
from windget import getTechVemA26


# 获取成交量量指数平滑异同移动平均线_PIT时间序列
from windget import getTechVmaCdSeries


# 获取成交量量指数平滑异同移动平均线_PIT
from windget import getTechVmaCd


# 获取成交量比率_PIT时间序列
from windget import getTechVrSeries


# 获取成交量比率_PIT
from windget import getTechVr


# 获取成交量震荡_PIT时间序列
from windget import getTechVosCSeries


# 获取成交量震荡_PIT
from windget import getTechVosC


# 获取正成交量指标_PIT时间序列
from windget import getTechPvISeries


# 获取正成交量指标_PIT
from windget import getTechPvI


# 获取负成交量指标_PIT时间序列
from windget import getTechNViSeries


# 获取负成交量指标_PIT
from windget import getTechNVi


# 获取盘后成交量时间序列
from windget import getVolumeAHtSeries


# 获取盘后成交量
from windget import getVolumeAHt


# 获取区间成交量时间序列
from windget import getVolPerSeries


# 获取区间成交量
from windget import getVolPer


# 获取区间成交量(含大宗交易)时间序列
from windget import getPqBlockTradeVolumeSeries


# 获取区间成交量(含大宗交易)
from windget import getPqBlockTradeVolume


# 获取N日成交量时间序列
from windget import getVolNdSeries


# 获取N日成交量
from windget import getVolNd


# 获取标的成交量时间序列
from windget import getUsVolumeSeries


# 获取标的成交量
from windget import getUsVolume


# 获取会员成交量时间序列
from windget import getOiVolumeSeries


# 获取会员成交量
from windget import getOiVolume


# 获取品种成交量时间序列
from windget import getOptionVolumeSeries


# 获取品种成交量
from windget import getOptionVolume


# 获取认购成交量时间序列
from windget import getCallVolumeSeries


# 获取认购成交量
from windget import getCallVolume


# 获取认沽成交量时间序列
from windget import getPutVolumeSeries


# 获取认沽成交量
from windget import getPutVolume


# 获取10日成交量标准差_PIT时间序列
from windget import getTechVsTd10Series


# 获取10日成交量标准差_PIT
from windget import getTechVsTd10


# 获取20日成交量标准差_PIT时间序列
from windget import getTechVsTd20Series


# 获取20日成交量标准差_PIT
from windget import getTechVsTd20


# 获取正股区间成交量时间序列
from windget import getCbPqStockVolSeries


# 获取正股区间成交量
from windget import getCbPqStockVol


# 获取区间日均成交量时间序列
from windget import getAvgVolPerSeries


# 获取区间日均成交量
from windget import getAvgVolPer


# 获取区间盘后成交量时间序列
from windget import getPqVolumeAHtSeries


# 获取区间盘后成交量
from windget import getPqVolumeAHt


# 获取卖空量占成交量比率时间序列
from windget import getShortSellVolumePctSeries


# 获取卖空量占成交量比率
from windget import getShortSellVolumePct


# 获取VSTD成交量标准差时间序列
from windget import getVsTdSeries


# 获取VSTD成交量标准差
from windget import getVsTd


# 获取上市首日成交量时间序列
from windget import getIpoListDayVolumeSeries


# 获取上市首日成交量
from windget import getIpoListDayVolume


# 获取开盘集合竞价成交量时间序列
from windget import getOpenAuctionVolumeSeries


# 获取开盘集合竞价成交量
from windget import getOpenAuctionVolume


# 获取上证固收平台成交量时间序列
from windget import getVolumeFixedIncomeSeries


# 获取上证固收平台成交量
from windget import getVolumeFixedIncome


# 获取成交额时间序列
from windget import getAmtSeries


# 获取成交额
from windget import getAmt


# 获取成交额(含大宗交易)时间序列
from windget import getAmountBtInSeries


# 获取成交额(含大宗交易)
from windget import getAmountBtIn


# 获取成交额惯性_PIT时间序列
from windget import getTechAmount1M60Series


# 获取成交额惯性_PIT
from windget import getTechAmount1M60


# 获取盘后成交额时间序列
from windget import getAmountAHtSeries


# 获取盘后成交额
from windget import getAmountAHt


# 获取区间成交额时间序列
from windget import getAmtPerSeries


# 获取区间成交额
from windget import getAmtPer


# 获取区间成交额(含大宗交易)时间序列
from windget import getPqBlockTradeAmountsSeries


# 获取区间成交额(含大宗交易)
from windget import getPqBlockTradeAmounts


# 获取N日成交额时间序列
from windget import getAmtNdSeries


# 获取N日成交额
from windget import getAmtNd


# 获取标的成交额时间序列
from windget import getUsAmountSeries


# 获取标的成交额
from windget import getUsAmount


# 获取品种成交额时间序列
from windget import getOptionAmountSeries


# 获取品种成交额
from windget import getOptionAmount


# 获取认购成交额时间序列
from windget import getCallAmountSeries


# 获取认购成交额
from windget import getCallAmount


# 获取认沽成交额时间序列
from windget import getPutAmountSeries


# 获取认沽成交额
from windget import getPutAmount


# 获取正股区间成交额时间序列
from windget import getCbPqStockAmNtSeries


# 获取正股区间成交额
from windget import getCbPqStockAmNt


# 获取区间日均成交额时间序列
from windget import getAvgAmtPerSeries


# 获取区间日均成交额
from windget import getAvgAmtPer


# 获取区间盘后成交额时间序列
from windget import getPqAmountAHtSeries


# 获取区间盘后成交额
from windget import getPqAmountAHt


# 获取上市首日成交额时间序列
from windget import getIpoVolumeSeries


# 获取上市首日成交额
from windget import getIpoVolume


# 获取开盘集合竞价成交额时间序列
from windget import getOpenAuctionAmountSeries


# 获取开盘集合竞价成交额
from windget import getOpenAuctionAmount


# 获取成交笔数时间序列
from windget import getDealNumSeries


# 获取成交笔数
from windget import getDealNum


# 获取上证固收平台成交笔数时间序列
from windget import getDealNumFixedIncomeSeries


# 获取上证固收平台成交笔数
from windget import getDealNumFixedIncome


# 获取涨跌时间序列
from windget import getChgSeries


# 获取涨跌
from windget import getChg


# 获取涨跌幅时间序列
from windget import getPctChgSeries


# 获取涨跌幅
from windget import getPctChg


# 获取涨跌幅(债券)时间序列
from windget import getPctChgBSeries


# 获取涨跌幅(债券)
from windget import getPctChgB


# 获取涨跌(结算价)时间序列
from windget import getChgSettlementSeries


# 获取涨跌(结算价)
from windget import getChgSettlement


# 获取涨跌幅(结算价)时间序列
from windget import getPctChgSettlementSeries


# 获取涨跌幅(结算价)
from windget import getPctChgSettlement


# 获取涨跌停状态时间序列
from windget import getMaxUpOrDownSeries


# 获取涨跌停状态
from windget import getMaxUpOrDown


# 获取涨跌(中债)时间序列
from windget import getDQChangeCnBdSeries


# 获取涨跌(中债)
from windget import getDQChangeCnBd


# 获取涨跌幅(中债)时间序列
from windget import getDQPctChangeCnBdSeries


# 获取涨跌幅(中债)
from windget import getDQPctChangeCnBd


# 获取区间涨跌时间序列
from windget import getChgPerSeries


# 获取区间涨跌
from windget import getChgPer


# 获取区间涨跌幅时间序列
from windget import getPctChgPerSeries


# 获取区间涨跌幅
from windget import getPctChgPer


# 获取区间涨跌幅(包含上市首日涨跌幅)时间序列
from windget import getPctChgPer2Series


# 获取区间涨跌幅(包含上市首日涨跌幅)
from windget import getPctChgPer2


# 获取N日涨跌幅时间序列
from windget import getPctChgNdSeries


# 获取N日涨跌幅
from windget import getPctChgNd


# 获取区间涨跌(结算价)时间序列
from windget import getFsPqChangeSettlementSeries


# 获取区间涨跌(结算价)
from windget import getFsPqChangeSettlement


# 获取区间涨跌幅(结算价)时间序列
from windget import getFsPqPctChangeSettlementSeries


# 获取区间涨跌幅(结算价)
from windget import getFsPqPctChangeSettlement


# 获取估算涨跌幅时间序列
from windget import getWestReturnSeries


# 获取估算涨跌幅
from windget import getWestReturn


# 获取估算涨跌幅误差时间序列
from windget import getWestReturnErrorSeries


# 获取估算涨跌幅误差
from windget import getWestReturnError


# 获取标的涨跌时间序列
from windget import getUsChangeSeries


# 获取标的涨跌
from windget import getUsChange


# 获取标的涨跌幅时间序列
from windget import getUsPctChangeSeries


# 获取标的涨跌幅
from windget import getUsPctChange


# 获取近5日涨跌幅时间序列
from windget import getPctChg5DSeries


# 获取近5日涨跌幅
from windget import getPctChg5D


# 获取近1月涨跌幅时间序列
from windget import getPctChg1MSeries


# 获取近1月涨跌幅
from windget import getPctChg1M


# 获取近3月涨跌幅时间序列
from windget import getPctChg3MSeries


# 获取近3月涨跌幅
from windget import getPctChg3M


# 获取近6月涨跌幅时间序列
from windget import getPctChg6MSeries


# 获取近6月涨跌幅
from windget import getPctChg6M


# 获取近1年涨跌幅时间序列
from windget import getPctChg1YSeries


# 获取近1年涨跌幅
from windget import getPctChg1Y


# 获取重仓股涨跌幅时间序列
from windget import getPrtHeavilyHeldStocksPerChangeSeries


# 获取重仓股涨跌幅
from windget import getPrtHeavilyHeldStocksPerChange


# 获取净值异常涨跌幅说明时间序列
from windget import getFundAbnormalNavFluctuationSeries


# 获取净值异常涨跌幅说明
from windget import getFundAbnormalNavFluctuation


# 获取正股区间涨跌时间序列
from windget import getCbPqStockChgSeries


# 获取正股区间涨跌
from windget import getCbPqStockChg


# 获取正股区间涨跌幅时间序列
from windget import getCbPqStockPctChgSeries


# 获取正股区间涨跌幅
from windget import getCbPqStockPctChg


# 获取N日日均涨跌幅时间序列
from windget import getAvgPctChgNdSeries


# 获取N日日均涨跌幅
from windget import getAvgPctChgNd


# 获取近10日涨跌幅时间序列
from windget import getPctChg10DSeries


# 获取近10日涨跌幅
from windget import getPctChg10D


# 获取上市首日涨跌幅时间序列
from windget import getIpoPctChangeSeries


# 获取上市首日涨跌幅
from windget import getIpoPctChange


# 获取重仓债券涨跌幅时间序列
from windget import getPrtHeavilyHeldBondsPerChangeSeries


# 获取重仓债券涨跌幅
from windget import getPrtHeavilyHeldBondsPerChange


# 获取重仓基金涨跌幅时间序列
from windget import getPrtHeavilyHeldFundPerChangeSeries


# 获取重仓基金涨跌幅
from windget import getPrtHeavilyHeldFundPerChange


# 获取相对发行价涨跌时间序列
from windget import getRelIpoChgSeries


# 获取相对发行价涨跌
from windget import getRelIpoChg


# 获取相对发行价涨跌幅时间序列
from windget import getRelIpoPctChgSeries


# 获取相对发行价涨跌幅
from windget import getRelIpoPctChg


# 获取上市后N日涨跌幅时间序列
from windget import getIpoNpcTChangeSeries


# 获取上市后N日涨跌幅
from windget import getIpoNpcTChange


# 获取新股开板日涨跌幅时间序列
from windget import getIpoLimitUpOpenDatePctChangeSeries


# 获取新股开板日涨跌幅
from windget import getIpoLimitUpOpenDatePctChange


# 获取区间相对指数涨跌幅时间序列
from windget import getRelPctChangeSeries


# 获取区间相对指数涨跌幅
from windget import getRelPctChange


# 获取相对大盘区间涨跌幅时间序列
from windget import getPqRelPctChangeSeries


# 获取相对大盘区间涨跌幅
from windget import getPqRelPctChange


# 获取相对大盘N日涨跌幅时间序列
from windget import getNQRelPctChangeSeries


# 获取相对大盘N日涨跌幅
from windget import getNQRelPctChange


# 获取年迄今相对指数涨跌幅时间序列
from windget import getPqRelPctChangeYTdSeries


# 获取年迄今相对指数涨跌幅
from windget import getPqRelPctChangeYTd


# 获取近5日相对指数涨跌幅时间序列
from windget import getPqRelPctChange5DSeries


# 获取近5日相对指数涨跌幅
from windget import getPqRelPctChange5D


# 获取近1月相对指数涨跌幅时间序列
from windget import getPqRelPctChange1MSeries


# 获取近1月相对指数涨跌幅
from windget import getPqRelPctChange1M


# 获取近3月相对指数涨跌幅时间序列
from windget import getPqRelPctChange3MSeries


# 获取近3月相对指数涨跌幅
from windget import getPqRelPctChange3M


# 获取近6月相对指数涨跌幅时间序列
from windget import getPqRelPctChange6MSeries


# 获取近6月相对指数涨跌幅
from windget import getPqRelPctChange6M


# 获取近1年相对指数涨跌幅时间序列
from windget import getPqRelPctChange1YSeries


# 获取近1年相对指数涨跌幅
from windget import getPqRelPctChange1Y


# 获取本月至今相对指数涨跌幅时间序列
from windget import getPqRelPctChangeMTdSeries


# 获取本月至今相对指数涨跌幅
from windget import getPqRelPctChangeMTd


# 获取季度至今相对指数涨跌幅时间序列
from windget import getPqRelRelPctChangeMTdSeries


# 获取季度至今相对指数涨跌幅
from windget import getPqRelRelPctChangeMTd


# 获取近10日相对指数涨跌幅时间序列
from windget import getPqRelPctChange10DSeries


# 获取近10日相对指数涨跌幅
from windget import getPqRelPctChange10D


# 获取振幅时间序列
from windget import getSwingSeries


# 获取振幅
from windget import getSwing


# 获取区间振幅时间序列
from windget import getSwingPerSeries


# 获取区间振幅
from windget import getSwingPer


# 获取N日振幅时间序列
from windget import getSwingNdSeries


# 获取N日振幅
from windget import getSwingNd


# 获取标的振幅时间序列
from windget import getUsSwingSeries


# 获取标的振幅
from windget import getUsSwing


# 获取正股区间振幅时间序列
from windget import getCbPqStockSwingSeries


# 获取正股区间振幅
from windget import getCbPqStockSwing


# 获取区间日均振幅时间序列
from windget import getAvgSwingPerSeries


# 获取区间日均振幅
from windget import getAvgSwingPer


# 获取均价时间序列
from windget import getVWapSeries


# 获取均价
from windget import getVWap


# 获取标的均价时间序列
from windget import getUsAvgPriceSeries


# 获取标的均价
from windget import getUsAvgPrice


# 获取发行前均价时间序列
from windget import getIpoPrePriceSeries


# 获取发行前均价
from windget import getIpoPrePrice


# 获取正股区间均价时间序列
from windget import getCbPqStockAvgSeries


# 获取正股区间均价
from windget import getCbPqStockAvg


# 获取区间成交均价时间序列
from windget import getVWapPerSeries


# 获取区间成交均价
from windget import getVWapPer


# 获取区间成交均价(可复权)时间序列
from windget import getPqAvgPrice2Series


# 获取区间成交均价(可复权)
from windget import getPqAvgPrice2


# 获取N日成交均价时间序列
from windget import getNQAvgPriceSeries


# 获取N日成交均价
from windget import getNQAvgPrice


# 获取是否为算术平均价时间序列
from windget import getClauseResetReferencePriceIsAnVerAgeSeries


# 获取是否为算术平均价
from windget import getClauseResetReferencePriceIsAnVerAge


# 获取上市首日成交均价时间序列
from windget import getIpoAvgPriceSeries


# 获取上市首日成交均价
from windget import getIpoAvgPrice


# 获取上证固收平台平均价时间序列
from windget import getAvgPriceFixedIncomeSeries


# 获取上证固收平台平均价
from windget import getAvgPriceFixedIncome


# 获取新股开板日成交均价时间序列
from windget import getIpoLimitUpOpenDateAvgPriceSeries


# 获取新股开板日成交均价
from windget import getIpoLimitUpOpenDateAvgPrice


# 获取复权因子时间序列
from windget import getAdjFactorSeries


# 获取复权因子
from windget import getAdjFactor


# 获取基金净值复权因子时间序列
from windget import getNavAdjFactorSeries


# 获取基金净值复权因子
from windget import getNavAdjFactor


# 获取换手率时间序列
from windget import getTurnSeries


# 获取换手率
from windget import getTurn


# 获取换手率(基准.自由流通股本)时间序列
from windget import getFreeTurnSeries


# 获取换手率(基准.自由流通股本)
from windget import getFreeTurn


# 获取换手率相对波动率_PIT时间序列
from windget import getTechTurnoverRateVolatility20Series


# 获取换手率相对波动率_PIT
from windget import getTechTurnoverRateVolatility20


# 获取区间换手率时间序列
from windget import getTurnPerSeries


# 获取区间换手率
from windget import getTurnPer


# 获取区间换手率(基准.自由流通股本)时间序列
from windget import getTurnFreePerSeries


# 获取区间换手率(基准.自由流通股本)
from windget import getTurnFreePer


# 获取N日换手率时间序列
from windget import getTurnNdSeries


# 获取N日换手率
from windget import getTurnNd


# 获取标的换手率时间序列
from windget import getUsTurnSeries


# 获取标的换手率
from windget import getUsTurn


# 获取3个月换手率对数平均_PIT时间序列
from windget import getTechSToQSeries


# 获取3个月换手率对数平均_PIT
from windget import getTechSToQ


# 获取正股区间换手率时间序列
from windget import getCbPqStockTurnoverSeries


# 获取正股区间换手率
from windget import getCbPqStockTurnover


# 获取区间日均换手率时间序列
from windget import getPqAvgTurn2Series


# 获取区间日均换手率
from windget import getPqAvgTurn2


# 获取区间日均换手率(剔除无成交日期)时间序列
from windget import getAvgTurnPerSeries


# 获取区间日均换手率(剔除无成交日期)
from windget import getAvgTurnPer


# 获取区间日均换手率(基准.自由流通股本)时间序列
from windget import getAvgTurnFreePerSeries


# 获取区间日均换手率(基准.自由流通股本)
from windget import getAvgTurnFreePer


# 获取N日日均换手率时间序列
from windget import getAvgTurnNdSeries


# 获取N日日均换手率
from windget import getAvgTurnNd


# 获取上市首日换手率时间序列
from windget import getIpoTurnSeries


# 获取上市首日换手率
from windget import getIpoTurn


# 获取5日平均换手率_PIT时间序列
from windget import getTechTurnoverRate5Series


# 获取5日平均换手率_PIT
from windget import getTechTurnoverRate5


# 获取12个月换手率对数平均_PIT时间序列
from windget import getTechSToASeries


# 获取12个月换手率对数平均_PIT
from windget import getTechSToA


# 获取5日平均换手率/120日平均换手率_PIT时间序列
from windget import getTechTurn5DTurn120Series


# 获取5日平均换手率/120日平均换手率_PIT
from windget import getTechTurn5DTurn120


# 获取上市后N日换手率时间序列
from windget import getIpoNTurnSeries


# 获取上市后N日换手率
from windget import getIpoNTurn


# 获取10日平均换手率_PIT时间序列
from windget import getTechTurnoverRate10Series


# 获取10日平均换手率_PIT
from windget import getTechTurnoverRate10


# 获取20日平均换手率_PIT时间序列
from windget import getTechTurnoverRate20Series


# 获取20日平均换手率_PIT
from windget import getTechTurnoverRate20


# 获取60日平均换手率_PIT时间序列
from windget import getTechTurnoverRate60Series


# 获取60日平均换手率_PIT
from windget import getTechTurnoverRate60


# 获取10日平均换手率/120日平均换手率_PIT时间序列
from windget import getTechTurn10DTurn120Series


# 获取10日平均换手率/120日平均换手率_PIT
from windget import getTechTurn10DTurn120


# 获取20日平均换手率/120日平均换手率_PIT时间序列
from windget import getTechTurn20DTurn120Series


# 获取20日平均换手率/120日平均换手率_PIT
from windget import getTechTurn20DTurn120


# 获取正股区间平均换手率时间序列
from windget import getCbPqStockAveTurnoverSeries


# 获取正股区间平均换手率
from windget import getCbPqStockAveTurnover


# 获取120日平均换手率_PIT时间序列
from windget import getTechTurnoverRate120Series


# 获取120日平均换手率_PIT
from windget import getTechTurnoverRate120


# 获取240日平均换手率_PIT时间序列
from windget import getTechTurnoverRate240Series


# 获取240日平均换手率_PIT
from windget import getTechTurnoverRate240


# 获取基金报告期持仓换手率时间序列
from windget import getStyleRpTTurnSeries


# 获取基金报告期持仓换手率
from windget import getStyleRpTTurn


# 获取持仓量时间序列
from windget import getOiSeries


# 获取持仓量
from windget import getOi


# 获取持仓量变化时间序列
from windget import getOiChgSeries


# 获取持仓量变化
from windget import getOiChg


# 获取持仓量(商品指数)时间序列
from windget import getOiIndexSeries


# 获取持仓量(商品指数)
from windget import getOiIndex


# 获取持仓量变化(商品指数)时间序列
from windget import getOiChangeSeries


# 获取持仓量变化(商品指数)
from windget import getOiChange


# 获取持仓量(不前推)时间序列
from windget import getOi3Series


# 获取持仓量(不前推)
from windget import getOi3


# 获取持仓量认沽认购比率时间序列
from windget import getOiRatioSeries


# 获取持仓量认沽认购比率
from windget import getOiRatio


# 获取区间持仓量时间序列
from windget import getOiPerSeries


# 获取区间持仓量
from windget import getOiPer


# 获取品种持仓量时间序列
from windget import getOptionOiSeries


# 获取品种持仓量
from windget import getOptionOi


# 获取认购持仓量时间序列
from windget import getCallOiSeries


# 获取认购持仓量
from windget import getCallOi


# 获取认沽持仓量时间序列
from windget import getPutOiSeries


# 获取认沽持仓量
from windget import getPutOi


# 获取区间日均持仓量时间序列
from windget import getAvgOiPerSeries


# 获取区间日均持仓量
from windget import getAvgOiPer


# 获取持仓额(不计保证金)时间序列
from windget import getOiAmountNoMarginSeries


# 获取持仓额(不计保证金)
from windget import getOiAmountNoMargin


# 获取持仓额时间序列
from windget import getOiAmountSeries


# 获取持仓额
from windget import getOiAmount


# 获取前结算价时间序列
from windget import getPreSettleSeries


# 获取前结算价
from windget import getPreSettle


# 获取区间前结算价时间序列
from windget import getPreSettlePerSeries


# 获取区间前结算价
from windget import getPreSettlePer


# 获取结算价时间序列
from windget import getSettleSeries


# 获取结算价
from windget import getSettle


# 获取结算价(不前推)时间序列
from windget import getSettle3Series


# 获取结算价(不前推)
from windget import getSettle3


# 获取区间结算价时间序列
from windget import getSettlePerSeries


# 获取区间结算价
from windget import getSettlePer


# 获取加权平均结算价修正久期(中债)时间序列
from windget import getWeightModiDuraSeries


# 获取加权平均结算价修正久期(中债)
from windget import getWeightModiDura


# 获取加权平均结算价利差久期(中债)时间序列
from windget import getWeightSprDuraSeries


# 获取加权平均结算价利差久期(中债)
from windget import getWeightSprDura


# 获取加权平均结算价利率久期(中债)时间序列
from windget import getWeightInterestDurationSeries


# 获取加权平均结算价利率久期(中债)
from windget import getWeightInterestDuration


# 获取加权平均结算价基点价值(中债)时间序列
from windget import getWeightVoBpSeries


# 获取加权平均结算价基点价值(中债)
from windget import getWeightVoBp


# 获取加权平均结算价凸性(中债)时间序列
from windget import getWeightCNvXTySeries


# 获取加权平均结算价凸性(中债)
from windget import getWeightCNvXTy


# 获取加权平均结算价利差凸性(中债)时间序列
from windget import getWeightSPrcNxtSeries


# 获取加权平均结算价利差凸性(中债)
from windget import getWeightSPrcNxt


# 获取加权平均结算价利率凸性(中债)时间序列
from windget import getWeightInterestCNvXTySeries


# 获取加权平均结算价利率凸性(中债)
from windget import getWeightInterestCNvXTy


# 获取区间最低结算价时间序列
from windget import getLowSettlePerSeries


# 获取区间最低结算价
from windget import getLowSettlePer


# 获取区间最高结算价时间序列
from windget import getHighSettlePerSeries


# 获取区间最高结算价
from windget import getHighSettlePer


# 获取区间最高结算价日时间序列
from windget import getFsPqHighSwingDateSeries


# 获取区间最高结算价日
from windget import getFsPqHighSwingDate


# 获取区间最低结算价日时间序列
from windget import getFsPqLowSwingDateSeries


# 获取区间最低结算价日
from windget import getFsPqLowSwingDate


# 获取最近交易日期时间序列
from windget import getLasTradeDaySSeries


# 获取最近交易日期
from windget import getLasTradeDayS


# 获取最早交易日期时间序列
from windget import getFirsTradeDaySSeries


# 获取最早交易日期
from windget import getFirsTradeDayS


# 获取市场最近交易日时间序列
from windget import getLastTradeDaySeries


# 获取市场最近交易日
from windget import getLastTradeDay


# 获取交易状态时间序列
from windget import getTradeStatusSeries


# 获取交易状态
from windget import getTradeStatus


# 获取总市值时间序列
from windget import getValMvArdSeries


# 获取总市值
from windget import getValMvArd


# 获取总市值1时间序列
from windget import getEvSeries


# 获取总市值1
from windget import getEv


# 获取总市值2时间序列
from windget import getMktCapArdSeries


# 获取总市值2
from windget import getMktCapArd


# 获取总市值1(币种可选)时间序列
from windget import getEv3Series


# 获取总市值1(币种可选)
from windget import getEv3


# 获取总市值(不可回测)时间序列
from windget import getMktCapSeries


# 获取总市值(不可回测)
from windget import getMktCap


# 获取总市值(证监会算法)时间序列
from windget import getMktCapCsrCSeries


# 获取总市值(证监会算法)
from windget import getMktCapCsrC


# 获取总市值/EBITDA(TTM反推法)_PIT时间序列
from windget import getValMvToeBitDaTtMSeries


# 获取总市值/EBITDA(TTM反推法)_PIT
from windget import getValMvToeBitDaTtM


# 获取总市值/息税折旧及摊销前利润TTM行业相对值_PIT时间序列
from windget import getValPeBitDaInDuSwTtMSeries


# 获取总市值/息税折旧及摊销前利润TTM行业相对值_PIT
from windget import getValPeBitDaInDuSwTtM


# 获取参考总市值时间序列
from windget import getMvRefSeries


# 获取参考总市值
from windget import getMvRef


# 获取指数总市值时间序列
from windget import getValMvSeries


# 获取指数总市值
from windget import getValMv


# 获取备考总市值(并购后)时间序列
from windget import getMamVSeries


# 获取备考总市值(并购后)
from windget import getMamV


# 获取当日总市值/负债总计时间序列
from windget import getEquityToDebt2Series


# 获取当日总市值/负债总计
from windget import getEquityToDebt2


# 获取区间日均总市值时间序列
from windget import getAvgMvPerSeries


# 获取区间日均总市值
from windget import getAvgMvPer


# 获取所属申万一级行业的总市值/息税折旧及摊销前利润TTM均值_PIT时间序列
from windget import getValAvgPeBitDaSwSeries


# 获取所属申万一级行业的总市值/息税折旧及摊销前利润TTM均值_PIT
from windget import getValAvgPeBitDaSw


# 获取所属申万一级行业的总市值/息税折旧及摊销前利润TTM标准差_PIT时间序列
from windget import getValStdPeBitDaSwSeries


# 获取所属申万一级行业的总市值/息税折旧及摊销前利润TTM标准差_PIT
from windget import getValStdPeBitDaSw


# 获取担保证券市值占该证券总市值比重时间序列
from windget import getMarginMarketValueRatioSeries


# 获取担保证券市值占该证券总市值比重
from windget import getMarginMarketValueRatio


# 获取流通市值时间序列
from windget import getValMvCSeries


# 获取流通市值
from windget import getValMvC


# 获取流通市值(含限售股)时间序列
from windget import getMktCapFloatSeries


# 获取流通市值(含限售股)
from windget import getMktCapFloat


# 获取自由流通市值时间序列
from windget import getMktFreeSharesSeries


# 获取自由流通市值
from windget import getMktFreeShares


# 获取自由流通市值_PIT时间序列
from windget import getValFloatMvSeries


# 获取自由流通市值_PIT
from windget import getValFloatMv


# 获取对数流通市值_PIT时间序列
from windget import getValLnFloatMvSeries


# 获取对数流通市值_PIT
from windget import getValLnFloatMv


# 获取区间日均流通市值时间序列
from windget import getPqAvgMvNonRestrictedSeries


# 获取区间日均流通市值
from windget import getPqAvgMvNonRestricted


# 获取连续停牌天数时间序列
from windget import getSUspDaysSeries


# 获取连续停牌天数
from windget import getSUspDays


# 获取停牌原因时间序列
from windget import getSUspReasonSeries


# 获取停牌原因
from windget import getSUspReason


# 获取涨停价时间序列
from windget import getMaxUpSeries


# 获取涨停价
from windget import getMaxUp


# 获取跌停价时间序列
from windget import getMaxDownSeries


# 获取跌停价
from windget import getMaxDown


# 获取贴水时间序列
from windget import getDiscountSeries


# 获取贴水
from windget import getDiscount


# 获取贴水率时间序列
from windget import getDiscountRatioSeries


# 获取贴水率
from windget import getDiscountRatio


# 获取区间均贴水时间序列
from windget import getAvgDiscountPerSeries


# 获取区间均贴水
from windget import getAvgDiscountPer


# 获取区间均贴水率时间序列
from windget import getAvgDiscountRatioPerSeries


# 获取区间均贴水率
from windget import getAvgDiscountRatioPer


# 获取所属指数权重时间序列
from windget import getIndexWeightSeries


# 获取所属指数权重
from windget import getIndexWeight


# 获取交收方向(黄金现货)时间序列
from windget import getDirectionGoldSeries


# 获取交收方向(黄金现货)
from windget import getDirectionGold


# 获取交收量(黄金现货)时间序列
from windget import getDQuantityGoldSeries


# 获取交收量(黄金现货)
from windget import getDQuantityGold


# 获取开盘集合竞价成交价时间序列
from windget import getOpenAuctionPriceSeries


# 获取开盘集合竞价成交价
from windget import getOpenAuctionPrice


# 获取区间收盘最大涨幅时间序列
from windget import getPctChgHighPerSeries


# 获取区间收盘最大涨幅
from windget import getPctChgHighPer


# 获取区间交易天数时间序列
from windget import getTradeDaysPerSeries


# 获取区间交易天数
from windget import getTradeDaysPer


# 获取区间涨停天数时间序列
from windget import getLimitUpDaysPerSeries


# 获取区间涨停天数
from windget import getLimitUpDaysPer


# 获取区间跌停天数时间序列
from windget import getLimitDownDaysPerSeries


# 获取区间跌停天数
from windget import getLimitDownDaysPer


# 获取区间上涨天数时间序列
from windget import getPqUpDaysPerSeries


# 获取区间上涨天数
from windget import getPqUpDaysPer


# 获取区间下跌天数时间序列
from windget import getPqDownDaysPerSeries


# 获取区间下跌天数
from windget import getPqDownDaysPer


# 获取区间报价天数时间序列
from windget import getQuoteDaysPerSeries


# 获取区间报价天数
from windget import getQuoteDaysPer


# 获取区间持仓变化时间序列
from windget import getOiChgPerSeries


# 获取区间持仓变化
from windget import getOiChgPer


# 获取区间开盘净主动买入额时间序列
from windget import getMfAmtOpenPerSeries


# 获取区间开盘净主动买入额
from windget import getMfAmtOpenPer


# 获取区间尾盘净主动买入额时间序列
from windget import getMfAmtClosePerSeries


# 获取区间尾盘净主动买入额
from windget import getMfAmtClosePer


# 获取区间净主动买入量时间序列
from windget import getMfVolPerSeries


# 获取区间净主动买入量
from windget import getMfVolPer


# 获取区间净主动买入量占比时间序列
from windget import getMfVolRatioPerSeries


# 获取区间净主动买入量占比
from windget import getMfVolRatioPer


# 获取区间净主动买入额时间序列
from windget import getMfAmtPerSeries


# 获取区间净主动买入额
from windget import getMfAmtPer


# 获取区间净主动买入率(金额)时间序列
from windget import getMfAmtRatioPerSeries


# 获取区间净主动买入率(金额)
from windget import getMfAmtRatioPer


# 获取区间主力净流入天数时间序列
from windget import getMfdInFlowDaysSeries


# 获取区间主力净流入天数
from windget import getMfdInFlowDays


# 获取区间流入额时间序列
from windget import getMfBuyAmtSeries


# 获取区间流入额
from windget import getMfBuyAmt


# 获取区间流入量时间序列
from windget import getMfBuyVolSeries


# 获取区间流入量
from windget import getMfBuyVol


# 获取区间流出额时间序列
from windget import getMfSellAmtSeries


# 获取区间流出额
from windget import getMfSellAmt


# 获取区间流出量时间序列
from windget import getMfSellVolSeries


# 获取区间流出量
from windget import getMfSellVol


# 获取区间大宗交易上榜次数时间序列
from windget import getPqBlockTradeNumSeries


# 获取区间大宗交易上榜次数
from windget import getPqBlockTradeNum


# 获取区间大宗交易成交总量时间序列
from windget import getPqBlockTradeVolumeSeries


# 获取区间大宗交易成交总量
from windget import getPqBlockTradeVolume


# 获取区间大宗交易成交总额时间序列
from windget import getPqBlockTradeAmountSeries


# 获取区间大宗交易成交总额
from windget import getPqBlockTradeAmount


# 获取区间龙虎榜上榜次数时间序列
from windget import getPqAbnormalTradeNumSeries


# 获取区间龙虎榜上榜次数
from windget import getPqAbnormalTradeNum


# 获取区间龙虎榜买入额时间序列
from windget import getPqAbnormalTradeLpSeries


# 获取区间龙虎榜买入额
from windget import getPqAbnormalTradeLp


# 获取指定日相近交易日期时间序列
from windget import getTradeDaySeries


# 获取指定日相近交易日期
from windget import getTradeDay


# 获取区间净流入额时间序列
from windget import getPeriodMfNetInFlowSeries


# 获取区间净流入额
from windget import getPeriodMfNetInFlow


# 获取融资买入额时间序列
from windget import getMrgLongAmtSeries


# 获取融资买入额
from windget import getMrgLongAmt


# 获取区间融资买入额时间序列
from windget import getMrgLongAmtIntSeries


# 获取区间融资买入额
from windget import getMrgLongAmtInt


# 获取融资偿还额时间序列
from windget import getMrgLongRepaySeries


# 获取融资偿还额
from windget import getMrgLongRepay


# 获取区间融资偿还额时间序列
from windget import getMrgLongRepayIntSeries


# 获取区间融资偿还额
from windget import getMrgLongRepayInt


# 获取融资余额时间序列
from windget import getMrgLongBalSeries


# 获取融资余额
from windget import getMrgLongBal


# 获取区间融资余额均值时间序列
from windget import getMrgLongBalIntAvgSeries


# 获取区间融资余额均值
from windget import getMrgLongBalIntAvg


# 获取报告期内债券回购融资余额时间序列
from windget import getMmRepurchase1Series


# 获取报告期内债券回购融资余额
from windget import getMmRepurchase1


# 获取报告期末债券回购融资余额时间序列
from windget import getMmRepurchase2Series


# 获取报告期末债券回购融资余额
from windget import getMmRepurchase2


# 获取报告期内债券回购融资余额占基金资产净值比例时间序列
from windget import getMmRepurchase1ToNavSeries


# 获取报告期内债券回购融资余额占基金资产净值比例
from windget import getMmRepurchase1ToNav


# 获取报告期末债券回购融资余额占基金资产净值比例时间序列
from windget import getMmRepurchase2ToNavSeries


# 获取报告期末债券回购融资余额占基金资产净值比例
from windget import getMmRepurchase2ToNav


# 获取融券卖出量时间序列
from windget import getMrgShortVolSeries


# 获取融券卖出量
from windget import getMrgShortVol


# 获取区间融券卖出量时间序列
from windget import getMrgShortVolIntSeries


# 获取区间融券卖出量
from windget import getMrgShortVolInt


# 获取融券偿还量时间序列
from windget import getMrgShortVolRepaySeries


# 获取融券偿还量
from windget import getMrgShortVolRepay


# 获取区间融券偿还量时间序列
from windget import getMrgShortVolRepayIntSeries


# 获取区间融券偿还量
from windget import getMrgShortVolRepayInt


# 获取融券卖出额时间序列
from windget import getMarginSaleTradingAmountSeries


# 获取融券卖出额
from windget import getMarginSaleTradingAmount


# 获取区间融券卖出额时间序列
from windget import getMarginShortAmountIntSeries


# 获取区间融券卖出额
from windget import getMarginShortAmountInt


# 获取融券偿还额时间序列
from windget import getMarginSaleRepayAmountSeries


# 获取融券偿还额
from windget import getMarginSaleRepayAmount


# 获取区间融券偿还额时间序列
from windget import getMarginShortAmountRepayIntSeries


# 获取区间融券偿还额
from windget import getMarginShortAmountRepayInt


# 获取融券余量时间序列
from windget import getMrgShortVolBalSeries


# 获取融券余量
from windget import getMrgShortVolBal


# 获取区间融券余量均值时间序列
from windget import getMrgShortVolBalIntAvgSeries


# 获取区间融券余量均值
from windget import getMrgShortVolBalIntAvg


# 获取融券余额时间序列
from windget import getMrgShortBalSeries


# 获取融券余额
from windget import getMrgShortBal


# 获取区间融券余额均值时间序列
from windget import getMrgShortBalIntAvgSeries


# 获取区间融券余额均值
from windget import getMrgShortBalIntAvg


# 获取全日卖空金额时间序列
from windget import getShortSellTurnoverSeries


# 获取全日卖空金额
from windget import getShortSellTurnover


# 获取卖空金额占市场卖空总额比率时间序列
from windget import getShortSellTurnoverPctSeries


# 获取卖空金额占市场卖空总额比率
from windget import getShortSellTurnoverPct


# 获取全日卖空股数时间序列
from windget import getShortSellVolumeSeries


# 获取全日卖空股数
from windget import getShortSellVolume


# 获取卖空量占香港流通股百分比时间序列
from windget import getShortSellVolumeToHSharesSeries


# 获取卖空量占香港流通股百分比
from windget import getShortSellVolumeToHShares


# 获取未平仓卖空数时间序列
from windget import getShareShortSharesSeries


# 获取未平仓卖空数
from windget import getShareShortShares


# 获取未平仓卖空金额时间序列
from windget import getShareShortAmountSeries


# 获取未平仓卖空金额
from windget import getShareShortAmount


# 获取空头回补天数时间序列
from windget import getShortSellDaysToCoverSeries


# 获取空头回补天数
from windget import getShortSellDaysToCover


# 获取流入额时间序列
from windget import getMfdBuyAmtDSeries


# 获取流入额
from windget import getMfdBuyAmtD


# 获取净流入额时间序列
from windget import getMfNetInFlowSeries


# 获取净流入额
from windget import getMfNetInFlow


# 获取主力净流入额时间序列
from windget import getMfdInFlowMSeries


# 获取主力净流入额
from windget import getMfdInFlowM


# 获取主力净流入额占比时间序列
from windget import getMfdInFlowProportionMSeries


# 获取主力净流入额占比
from windget import getMfdInFlowProportionM


# 获取开盘主力净流入额时间序列
from windget import getMfdInFlowOpenMSeries


# 获取开盘主力净流入额
from windget import getMfdInFlowOpenM


# 获取尾盘主力净流入额时间序列
from windget import getMfdInFlowCloseMSeries


# 获取尾盘主力净流入额
from windget import getMfdInFlowCloseM


# 获取开盘主力净流入额占比时间序列
from windget import getMfdInFlowProportionOpenMSeries


# 获取开盘主力净流入额占比
from windget import getMfdInFlowProportionOpenM


# 获取尾盘主力净流入额占比时间序列
from windget import getMfdInFlowProportionCloseMSeries


# 获取尾盘主力净流入额占比
from windget import getMfdInFlowProportionCloseM


# 获取流出额时间序列
from windget import getMfdSellAmtDSeries


# 获取流出额
from windget import getMfdSellAmtD


# 获取流入量时间序列
from windget import getMfdBuyVolDSeries


# 获取流入量
from windget import getMfdBuyVolD


# 获取主力净流入量时间序列
from windget import getMfdBuyVolMSeries


# 获取主力净流入量
from windget import getMfdBuyVolM


# 获取主力净流入量占比时间序列
from windget import getMfdVolInFlowProportionMSeries


# 获取主力净流入量占比
from windget import getMfdVolInFlowProportionM


# 获取开盘主力净流入量时间序列
from windget import getMfdBuyVolOpenMSeries


# 获取开盘主力净流入量
from windget import getMfdBuyVolOpenM


# 获取尾盘主力净流入量时间序列
from windget import getMfdBuyVolCloseMSeries


# 获取尾盘主力净流入量
from windget import getMfdBuyVolCloseM


# 获取开盘主力净流入量占比时间序列
from windget import getMfdVolInFlowProportionOpenMSeries


# 获取开盘主力净流入量占比
from windget import getMfdVolInFlowProportionOpenM


# 获取尾盘主力净流入量占比时间序列
from windget import getMfdVolInFlowProportionCloseMSeries


# 获取尾盘主力净流入量占比
from windget import getMfdVolInFlowProportionCloseM


# 获取流出量时间序列
from windget import getMfdSellVolDSeries


# 获取流出量
from windget import getMfdSellVolD


# 获取净买入额时间序列
from windget import getMfdNetBuyAmtSeries


# 获取净买入额
from windget import getMfdNetBuyAmt


# 获取沪深港股通区间净买入额时间序列
from windget import getMfpSnInFlowSeries


# 获取沪深港股通区间净买入额
from windget import getMfpSnInFlow


# 获取净买入量时间序列
from windget import getMfdNetBuyVolSeries


# 获取净买入量
from windget import getMfdNetBuyVol


# 获取沪深港股通区间净买入量时间序列
from windget import getMfpSnInFlowAmtSeries


# 获取沪深港股通区间净买入量
from windget import getMfpSnInFlowAmt


# 获取沪深港股通区间净买入量(调整)时间序列
from windget import getMfpSnInFlowAmt2Series


# 获取沪深港股通区间净买入量(调整)
from windget import getMfpSnInFlowAmt2


# 获取流入单数时间序列
from windget import getMfdBuyOrDSeries


# 获取流入单数
from windget import getMfdBuyOrD


# 获取流出单数时间序列
from windget import getMfdSelLordSeries


# 获取流出单数
from windget import getMfdSelLord


# 获取主动买入额时间序列
from windget import getMfdBuyAmtASeries


# 获取主动买入额
from windget import getMfdBuyAmtA


# 获取主动买入额(全单)时间序列
from windget import getMfdBuyAmtAtSeries


# 获取主动买入额(全单)
from windget import getMfdBuyAmtAt


# 获取净主动买入额时间序列
from windget import getMfdNetBuyAmtASeries


# 获取净主动买入额
from windget import getMfdNetBuyAmtA


# 获取净主动买入额(全单)时间序列
from windget import getMfAmtSeries


# 获取净主动买入额(全单)
from windget import getMfAmt


# 获取净主动买入额占比时间序列
from windget import getMfdInFlowProportionASeries


# 获取净主动买入额占比
from windget import getMfdInFlowProportionA


# 获取开盘净主动买入额时间序列
from windget import getMfAmtOpenSeries


# 获取开盘净主动买入额
from windget import getMfAmtOpen


# 获取尾盘净主动买入额时间序列
from windget import getMfAmtCloseSeries


# 获取尾盘净主动买入额
from windget import getMfAmtClose


# 获取开盘净主动买入额占比时间序列
from windget import getMfdInFlowProportionOpenASeries


# 获取开盘净主动买入额占比
from windget import getMfdInFlowProportionOpenA


# 获取尾盘净主动买入额占比时间序列
from windget import getMfdInFlowProportionCloseASeries


# 获取尾盘净主动买入额占比
from windget import getMfdInFlowProportionCloseA


# 获取主动卖出额时间序列
from windget import getMfdSellAmtASeries


# 获取主动卖出额
from windget import getMfdSellAmtA


# 获取主动卖出额(全单)时间序列
from windget import getMfdSellAmtAtSeries


# 获取主动卖出额(全单)
from windget import getMfdSellAmtAt


# 获取主动买入量时间序列
from windget import getMfdBuyVolASeries


# 获取主动买入量
from windget import getMfdBuyVolA


# 获取主动买入量(全单)时间序列
from windget import getMfdBuyVolAtSeries


# 获取主动买入量(全单)
from windget import getMfdBuyVolAt


# 获取净主动买入量时间序列
from windget import getMfdNetBuyVolASeries


# 获取净主动买入量
from windget import getMfdNetBuyVolA


# 获取净主动买入量(全单)时间序列
from windget import getMfVolSeries


# 获取净主动买入量(全单)
from windget import getMfVol


# 获取净主动买入量占比时间序列
from windget import getMfVolRatioSeries


# 获取净主动买入量占比
from windget import getMfVolRatio


# 获取开盘净主动买入量占比时间序列
from windget import getMfdVolInFlowProportionOpenASeries


# 获取开盘净主动买入量占比
from windget import getMfdVolInFlowProportionOpenA


# 获取尾盘净主动买入量占比时间序列
from windget import getMfdVolInFlowProportionCloseASeries


# 获取尾盘净主动买入量占比
from windget import getMfdVolInFlowProportionCloseA


# 获取开盘资金净主动买入量时间序列
from windget import getMfdInFlowVolumeOpenASeries


# 获取开盘资金净主动买入量
from windget import getMfdInFlowVolumeOpenA


# 获取尾盘资金净主动买入量时间序列
from windget import getMfdInFlowVolumeCloseASeries


# 获取尾盘资金净主动买入量
from windget import getMfdInFlowVolumeCloseA


# 获取主动卖出量时间序列
from windget import getMfdSellVolASeries


# 获取主动卖出量
from windget import getMfdSellVolA


# 获取主动卖出量(全单)时间序列
from windget import getMfdSellVolAtSeries


# 获取主动卖出量(全单)
from windget import getMfdSellVolAt


# 获取净主动买入率(金额)时间序列
from windget import getMfAmtRatioSeries


# 获取净主动买入率(金额)
from windget import getMfAmtRatio


# 获取开盘净主动买入率(金额)时间序列
from windget import getMfdInFlowRateOpenASeries


# 获取开盘净主动买入率(金额)
from windget import getMfdInFlowRateOpenA


# 获取尾盘净主动买入率(金额)时间序列
from windget import getMfdInFlowRateCloseASeries


# 获取尾盘净主动买入率(金额)
from windget import getMfdInFlowRateCloseA


# 获取净主动买入率(量)时间序列
from windget import getMfdVolInFlowRateASeries


# 获取净主动买入率(量)
from windget import getMfdVolInFlowRateA


# 获取开盘净主动买入率(量)时间序列
from windget import getMfdVolInFlowRateOpenASeries


# 获取开盘净主动买入率(量)
from windget import getMfdVolInFlowRateOpenA


# 获取尾盘净主动买入率(量)时间序列
from windget import getMfdVolInFlowRateCloseASeries


# 获取尾盘净主动买入率(量)
from windget import getMfdVolInFlowRateCloseA


# 获取主力净流入率(金额)时间序列
from windget import getMfdInFlowRateMSeries


# 获取主力净流入率(金额)
from windget import getMfdInFlowRateM


# 获取开盘主力净流入率(金额)时间序列
from windget import getMfdInFlowRateOpenMSeries


# 获取开盘主力净流入率(金额)
from windget import getMfdInFlowRateOpenM


# 获取尾盘主力净流入率(金额)时间序列
from windget import getMfdInFlowRateCloseMSeries


# 获取尾盘主力净流入率(金额)
from windget import getMfdInFlowRateCloseM


# 获取主力净流入率(量)时间序列
from windget import getMfdVolInFlowRateMSeries


# 获取主力净流入率(量)
from windget import getMfdVolInFlowRateM


# 获取开盘主力净流入率(量)时间序列
from windget import getMfdVolInFlowRateOpenMSeries


# 获取开盘主力净流入率(量)
from windget import getMfdVolInFlowRateOpenM


# 获取尾盘主力净流入率(量)时间序列
from windget import getMfdVolInFlowRateCloseMSeries


# 获取尾盘主力净流入率(量)
from windget import getMfdVolInFlowRateCloseM


# 获取沪深港股通买入金额时间序列
from windget import getMfdSnBuyAmtSeries


# 获取沪深港股通买入金额
from windget import getMfdSnBuyAmt


# 获取沪深港股通卖出金额时间序列
from windget import getMfdSnSellAmtSeries


# 获取沪深港股通卖出金额
from windget import getMfdSnSellAmt


# 获取沪深港股通净买入金额时间序列
from windget import getMfdSnInFlowSeries


# 获取沪深港股通净买入金额
from windget import getMfdSnInFlow


# 获取沪深港股通区间净流入天数时间序列
from windget import getMfpSnInFlowDaysSeries


# 获取沪深港股通区间净流入天数
from windget import getMfpSnInFlowDays


# 获取沪深港股通区间净流出天数时间序列
from windget import getMfpSnOutflowDaysSeries


# 获取沪深港股通区间净流出天数
from windget import getMfpSnOutflowDays


# 获取沪深港股通持续净流入天数时间序列
from windget import getMfnSnInFlowDaysSeries


# 获取沪深港股通持续净流入天数
from windget import getMfnSnInFlowDays


# 获取沪深港股通持续净卖出天数时间序列
from windget import getMfnSnOutflowDaysSeries


# 获取沪深港股通持续净卖出天数
from windget import getMfnSnOutflowDays


# 获取外资买卖超时间序列
from windget import getInSHdQFIiExSeries


# 获取外资买卖超
from windget import getInSHdQFIiEx


# 获取外资买卖超市值时间序列
from windget import getInSHdQFIiExMvSeries


# 获取外资买卖超市值
from windget import getInSHdQFIiExMv


# 获取投信买卖超时间序列
from windget import getInSHdFundExSeries


# 获取投信买卖超
from windget import getInSHdFundEx


# 获取投信买卖超市值时间序列
from windget import getInSHdFundExMvSeries


# 获取投信买卖超市值
from windget import getInSHdFundExMv


# 获取自营买卖超时间序列
from windget import getInSHdDlrExSeries


# 获取自营买卖超
from windget import getInSHdDlrEx


# 获取自营买卖超市值时间序列
from windget import getInSHdDlrExMvSeries


# 获取自营买卖超市值
from windget import getInSHdDlrExMv


# 获取合计买卖超时间序列
from windget import getInSHdTtlExSeries


# 获取合计买卖超
from windget import getInSHdTtlEx


# 获取合计买卖超市值时间序列
from windget import getInSHdTtlExMvSeries


# 获取合计买卖超市值
from windget import getInSHdTtlExMv


# 获取外资买进数量时间序列
from windget import getInSHdQFIiBuySeries


# 获取外资买进数量
from windget import getInSHdQFIiBuy


# 获取外资卖出数量时间序列
from windget import getInSHdQFIiSellSeries


# 获取外资卖出数量
from windget import getInSHdQFIiSell


# 获取投信买进数量时间序列
from windget import getInSHdFundBuySeries


# 获取投信买进数量
from windget import getInSHdFundBuy


# 获取投信卖出数量时间序列
from windget import getInSHdFundSellSeries


# 获取投信卖出数量
from windget import getInSHdFundSell


# 获取自营商买进数量时间序列
from windget import getInSHdDlrBuySeries


# 获取自营商买进数量
from windget import getInSHdDlrBuy


# 获取自营商卖出数量时间序列
from windget import getInSHdDlrSellSeries


# 获取自营商卖出数量
from windget import getInSHdDlrSell


# 获取区间回报时间序列
from windget import getReturnSeries


# 获取区间回报
from windget import getReturn


# 获取规模同类排名(券商集合理财)时间序列
from windget import getFundQSimilarProductSimilarRankingSeries


# 获取规模同类排名(券商集合理财)
from windget import getFundQSimilarProductSimilarRanking


# 获取规模同类排名时间序列
from windget import getFundScaleRankingSeries


# 获取规模同类排名
from windget import getFundScaleRanking


# 获取下行风险同类排名时间序列
from windget import getRiskDownsideRiskRankingSeries


# 获取下行风险同类排名
from windget import getRiskDownsideRiskRanking


# 获取选时能力同类排名时间序列
from windget import getRiskTimeRankingSeries


# 获取选时能力同类排名
from windget import getRiskTimeRanking


# 获取选股能力同类排名时间序列
from windget import getRiskStockRankingSeries


# 获取选股能力同类排名
from windget import getRiskStockRanking


# 获取信息比率同类排名时间序列
from windget import getRiskInfoRatioRankingSeries


# 获取信息比率同类排名
from windget import getRiskInfoRatioRanking


# 获取跟踪误差同类排名时间序列
from windget import getRiskTrackErrorRankingSeries


# 获取跟踪误差同类排名
from windget import getRiskTrackErrorRanking


# 获取年化波动率同类排名时间序列
from windget import getRiskAnnualVolRankingSeries


# 获取年化波动率同类排名
from windget import getRiskAnnualVolRanking


# 获取平均持仓时间同类排名时间序列
from windget import getStyleAvgPositionTimeRankingSeries


# 获取平均持仓时间同类排名
from windget import getStyleAvgPositionTimeRanking


# 获取注册仓单数量时间序列
from windget import getStStockSeries


# 获取注册仓单数量
from windget import getStStock


# 获取企业价值(含货币资金)时间序列
from windget import getEv1Series


# 获取企业价值(含货币资金)
from windget import getEv1


# 获取企业价值(剔除货币资金)时间序列
from windget import getEv2Series


# 获取企业价值(剔除货币资金)
from windget import getEv2


# 获取资产总计/企业价值_PIT时间序列
from windget import getValTaToEvSeries


# 获取资产总计/企业价值_PIT
from windget import getValTaToEv


# 获取营业收入(TTM)/企业价值_PIT时间序列
from windget import getValOrToEvTtMSeries


# 获取营业收入(TTM)/企业价值_PIT
from windget import getValOrToEvTtM


# 获取应计利息(债券计算器)时间序列
from windget import getCalcAccruedSeries


# 获取应计利息(债券计算器)
from windget import getCalcAccrued


# 获取剩余存续期(交易日)时间序列
from windget import getPtMTradeDaySeries


# 获取剩余存续期(交易日)
from windget import getPtMTradeDay


# 获取剩余存续期(日历日)时间序列
from windget import getPtMDaySeries


# 获取剩余存续期(日历日)
from windget import getPtMDay


# 获取理论价格时间序列
from windget import getTheoryValueSeries


# 获取理论价格
from windget import getTheoryValue


# 获取内在价值时间序列
from windget import getIntrInCtValueSeries


# 获取内在价值
from windget import getIntrInCtValue


# 获取时间价值时间序列
from windget import getTimeValueSeries


# 获取时间价值
from windget import getTimeValue


# 获取标的30日历史波动率时间序列
from windget import getUnderlyingHisVol30DSeries


# 获取标的30日历史波动率
from windget import getUnderlyingHisVol30D


# 获取标的60日历史波动率时间序列
from windget import getUsHisVolSeries


# 获取标的60日历史波动率
from windget import getUsHisVol


# 获取标的90日历史波动率时间序列
from windget import getUnderlyingHisVol90DSeries


# 获取标的90日历史波动率
from windget import getUnderlyingHisVol90D


# 获取期权隐含波动率时间序列
from windget import getUsImpliedVolSeries


# 获取期权隐含波动率
from windget import getUsImpliedVol


# 获取历史波动率时间序列
from windget import getVolatilityRatioSeries


# 获取历史波动率
from windget import getVolatilityRatio


# 获取1个月130%价值状态隐含波动率时间序列
from windget import getIv1M1300Series


# 获取1个月130%价值状态隐含波动率
from windget import getIv1M1300


# 获取1个月120%价值状态隐含波动率时间序列
from windget import getIv1M1200Series


# 获取1个月120%价值状态隐含波动率
from windget import getIv1M1200


# 获取1个月110%价值状态隐含波动率时间序列
from windget import getIv1M1100Series


# 获取1个月110%价值状态隐含波动率
from windget import getIv1M1100


# 获取1个月105%价值状态隐含波动率时间序列
from windget import getIv1M1050Series


# 获取1个月105%价值状态隐含波动率
from windget import getIv1M1050


# 获取1个月102.5%价值状态隐含波动率时间序列
from windget import getIv1M1025Series


# 获取1个月102.5%价值状态隐含波动率
from windget import getIv1M1025


# 获取1个月100%价值状态隐含波动率时间序列
from windget import getIv1M1000Series


# 获取1个月100%价值状态隐含波动率
from windget import getIv1M1000


# 获取1个月97.5%价值状态隐含波动率时间序列
from windget import getIv1M975Series


# 获取1个月97.5%价值状态隐含波动率
from windget import getIv1M975


# 获取1个月95%价值状态隐含波动率时间序列
from windget import getIv1M950Series


# 获取1个月95%价值状态隐含波动率
from windget import getIv1M950


# 获取1个月90%价值状态隐含波动率时间序列
from windget import getIv1M900Series


# 获取1个月90%价值状态隐含波动率
from windget import getIv1M900


# 获取1个月80%价值状态隐含波动率时间序列
from windget import getIv1M800Series


# 获取1个月80%价值状态隐含波动率
from windget import getIv1M800


# 获取1个月60%价值状态隐含波动率时间序列
from windget import getIv1M600Series


# 获取1个月60%价值状态隐含波动率
from windget import getIv1M600


# 获取2个月130%价值状态隐含波动率时间序列
from windget import getIv2M1300Series


# 获取2个月130%价值状态隐含波动率
from windget import getIv2M1300


# 获取2个月120%价值状态隐含波动率时间序列
from windget import getIv2M1200Series


# 获取2个月120%价值状态隐含波动率
from windget import getIv2M1200


# 获取2个月110%价值状态隐含波动率时间序列
from windget import getIv2M1100Series


# 获取2个月110%价值状态隐含波动率
from windget import getIv2M1100


# 获取2个月105%价值状态隐含波动率时间序列
from windget import getIv2M1050Series


# 获取2个月105%价值状态隐含波动率
from windget import getIv2M1050


# 获取2个月102.5%价值状态隐含波动率时间序列
from windget import getIv2M1025Series


# 获取2个月102.5%价值状态隐含波动率
from windget import getIv2M1025


# 获取2个月100%价值状态隐含波动率时间序列
from windget import getIv2M1000Series


# 获取2个月100%价值状态隐含波动率
from windget import getIv2M1000


# 获取2个月97.5%价值状态隐含波动率时间序列
from windget import getIv2M975Series


# 获取2个月97.5%价值状态隐含波动率
from windget import getIv2M975


# 获取2个月95%价值状态隐含波动率时间序列
from windget import getIv2M950Series


# 获取2个月95%价值状态隐含波动率
from windget import getIv2M950


# 获取2个月90%价值状态隐含波动率时间序列
from windget import getIv2M900Series


# 获取2个月90%价值状态隐含波动率
from windget import getIv2M900


# 获取2个月80%价值状态隐含波动率时间序列
from windget import getIv2M800Series


# 获取2个月80%价值状态隐含波动率
from windget import getIv2M800


# 获取2个月60%价值状态隐含波动率时间序列
from windget import getIv2M600Series


# 获取2个月60%价值状态隐含波动率
from windget import getIv2M600


# 获取3个月130%价值状态隐含波动率时间序列
from windget import getIv3M1300Series


# 获取3个月130%价值状态隐含波动率
from windget import getIv3M1300


# 获取3个月120%价值状态隐含波动率时间序列
from windget import getIv3M1200Series


# 获取3个月120%价值状态隐含波动率
from windget import getIv3M1200


# 获取3个月110%价值状态隐含波动率时间序列
from windget import getIv3M1100Series


# 获取3个月110%价值状态隐含波动率
from windget import getIv3M1100


# 获取3个月105%价值状态隐含波动率时间序列
from windget import getIv3M1050Series


# 获取3个月105%价值状态隐含波动率
from windget import getIv3M1050


# 获取3个月102.5%价值状态隐含波动率时间序列
from windget import getIv3M1025Series


# 获取3个月102.5%价值状态隐含波动率
from windget import getIv3M1025


# 获取3个月100%价值状态隐含波动率时间序列
from windget import getIv3M1000Series


# 获取3个月100%价值状态隐含波动率
from windget import getIv3M1000


# 获取3个月97.5%价值状态隐含波动率时间序列
from windget import getIv3M975Series


# 获取3个月97.5%价值状态隐含波动率
from windget import getIv3M975


# 获取3个月95%价值状态隐含波动率时间序列
from windget import getIv3M950Series


# 获取3个月95%价值状态隐含波动率
from windget import getIv3M950


# 获取3个月90%价值状态隐含波动率时间序列
from windget import getIv3M900Series


# 获取3个月90%价值状态隐含波动率
from windget import getIv3M900


# 获取3个月80%价值状态隐含波动率时间序列
from windget import getIv3M800Series


# 获取3个月80%价值状态隐含波动率
from windget import getIv3M800


# 获取3个月60%价值状态隐含波动率时间序列
from windget import getIv3M600Series


# 获取3个月60%价值状态隐含波动率
from windget import getIv3M600


# 获取6个月130%价值状态隐含波动率时间序列
from windget import getIv6M1300Series


# 获取6个月130%价值状态隐含波动率
from windget import getIv6M1300


# 获取6个月120%价值状态隐含波动率时间序列
from windget import getIv6M1200Series


# 获取6个月120%价值状态隐含波动率
from windget import getIv6M1200


# 获取6个月110%价值状态隐含波动率时间序列
from windget import getIv6M1100Series


# 获取6个月110%价值状态隐含波动率
from windget import getIv6M1100


# 获取6个月105%价值状态隐含波动率时间序列
from windget import getIv6M1050Series


# 获取6个月105%价值状态隐含波动率
from windget import getIv6M1050


# 获取6个月102.5%价值状态隐含波动率时间序列
from windget import getIv6M1025Series


# 获取6个月102.5%价值状态隐含波动率
from windget import getIv6M1025


# 获取6个月100%价值状态隐含波动率时间序列
from windget import getIv6M1000Series


# 获取6个月100%价值状态隐含波动率
from windget import getIv6M1000


# 获取6个月97.5%价值状态隐含波动率时间序列
from windget import getIv6M975Series


# 获取6个月97.5%价值状态隐含波动率
from windget import getIv6M975


# 获取6个月95%价值状态隐含波动率时间序列
from windget import getIv6M950Series


# 获取6个月95%价值状态隐含波动率
from windget import getIv6M950


# 获取6个月90%价值状态隐含波动率时间序列
from windget import getIv6M900Series


# 获取6个月90%价值状态隐含波动率
from windget import getIv6M900


# 获取6个月80%价值状态隐含波动率时间序列
from windget import getIv6M800Series


# 获取6个月80%价值状态隐含波动率
from windget import getIv6M800


# 获取6个月60%价值状态隐含波动率时间序列
from windget import getIv6M600Series


# 获取6个月60%价值状态隐含波动率
from windget import getIv6M600


# 获取9个月130%价值状态隐含波动率时间序列
from windget import getIv9M1300Series


# 获取9个月130%价值状态隐含波动率
from windget import getIv9M1300


# 获取9个月120%价值状态隐含波动率时间序列
from windget import getIv9M1200Series


# 获取9个月120%价值状态隐含波动率
from windget import getIv9M1200


# 获取9个月110%价值状态隐含波动率时间序列
from windget import getIv9M1100Series


# 获取9个月110%价值状态隐含波动率
from windget import getIv9M1100


# 获取9个月105%价值状态隐含波动率时间序列
from windget import getIv9M1050Series


# 获取9个月105%价值状态隐含波动率
from windget import getIv9M1050


# 获取9个月102.5%价值状态隐含波动率时间序列
from windget import getIv9M1025Series


# 获取9个月102.5%价值状态隐含波动率
from windget import getIv9M1025


# 获取9个月100%价值状态隐含波动率时间序列
from windget import getIv9M1000Series


# 获取9个月100%价值状态隐含波动率
from windget import getIv9M1000


# 获取9个月97.5%价值状态隐含波动率时间序列
from windget import getIv9M975Series


# 获取9个月97.5%价值状态隐含波动率
from windget import getIv9M975


# 获取9个月95%价值状态隐含波动率时间序列
from windget import getIv9M950Series


# 获取9个月95%价值状态隐含波动率
from windget import getIv9M950


# 获取9个月90%价值状态隐含波动率时间序列
from windget import getIv9M900Series


# 获取9个月90%价值状态隐含波动率
from windget import getIv9M900


# 获取9个月80%价值状态隐含波动率时间序列
from windget import getIv9M800Series


# 获取9个月80%价值状态隐含波动率
from windget import getIv9M800


# 获取9个月60%价值状态隐含波动率时间序列
from windget import getIv9M600Series


# 获取9个月60%价值状态隐含波动率
from windget import getIv9M600


# 获取1年130%价值状态隐含波动率时间序列
from windget import getIv1Y1300Series


# 获取1年130%价值状态隐含波动率
from windget import getIv1Y1300


# 获取1年120%价值状态隐含波动率时间序列
from windget import getIv1Y1200Series


# 获取1年120%价值状态隐含波动率
from windget import getIv1Y1200


# 获取1年110%价值状态隐含波动率时间序列
from windget import getIv1Y1100Series


# 获取1年110%价值状态隐含波动率
from windget import getIv1Y1100


# 获取1年105%价值状态隐含波动率时间序列
from windget import getIv1Y1050Series


# 获取1年105%价值状态隐含波动率
from windget import getIv1Y1050


# 获取1年102.5%价值状态隐含波动率时间序列
from windget import getIv1Y1025Series


# 获取1年102.5%价值状态隐含波动率
from windget import getIv1Y1025


# 获取1年100%价值状态隐含波动率时间序列
from windget import getIv1Y1000Series


# 获取1年100%价值状态隐含波动率
from windget import getIv1Y1000


# 获取1年97.5%价值状态隐含波动率时间序列
from windget import getIv1Y975Series


# 获取1年97.5%价值状态隐含波动率
from windget import getIv1Y975


# 获取1年95%价值状态隐含波动率时间序列
from windget import getIv1Y950Series


# 获取1年95%价值状态隐含波动率
from windget import getIv1Y950


# 获取1年90%价值状态隐含波动率时间序列
from windget import getIv1Y900Series


# 获取1年90%价值状态隐含波动率
from windget import getIv1Y900


# 获取1年80%价值状态隐含波动率时间序列
from windget import getIv1Y800Series


# 获取1年80%价值状态隐含波动率
from windget import getIv1Y800


# 获取1年60%价值状态隐含波动率时间序列
from windget import getIv1Y600Series


# 获取1年60%价值状态隐含波动率
from windget import getIv1Y600


# 获取一致预测净利润(未来12个月)时间序列
from windget import getWestNetProfitFtmSeries


# 获取一致预测净利润(未来12个月)
from windget import getWestNetProfitFtm


# 获取一致预测净利润(未来12个月)的变化_1M_PIT时间序列
from windget import getWestNetProfitFtmChg1MSeries


# 获取一致预测净利润(未来12个月)的变化_1M_PIT
from windget import getWestNetProfitFtmChg1M


# 获取一致预测净利润(未来12个月)的变化_3M_PIT时间序列
from windget import getWestNetProfitFtmChg3MSeries


# 获取一致预测净利润(未来12个月)的变化_3M_PIT
from windget import getWestNetProfitFtmChg3M


# 获取一致预测净利润(未来12个月)的变化_6M_PIT时间序列
from windget import getWestNetProfitFtmChg6MSeries


# 获取一致预测净利润(未来12个月)的变化_6M_PIT
from windget import getWestNetProfitFtmChg6M


# 获取一致预测净利润(未来12个月)的变化率_1M_PIT时间序列
from windget import getWestNetProfitFtm1MSeries


# 获取一致预测净利润(未来12个月)的变化率_1M_PIT
from windget import getWestNetProfitFtm1M


# 获取一致预测净利润(未来12个月)的变化率_3M_PIT时间序列
from windget import getWestNetProfitFtm3MSeries


# 获取一致预测净利润(未来12个月)的变化率_3M_PIT
from windget import getWestNetProfitFtm3M


# 获取一致预测净利润(未来12个月)的变化率_6M_PIT时间序列
from windget import getWestNetProfitFtm6MSeries


# 获取一致预测净利润(未来12个月)的变化率_6M_PIT
from windget import getWestNetProfitFtm6M


# 获取一致预测净利润(未来12个月)与归属于母公司净利润(TTM)的差_PIT时间序列
from windget import getWestNetProfitDiffSeries


# 获取一致预测净利润(未来12个月)与归属于母公司净利润(TTM)的差_PIT
from windget import getWestNetProfitDiff


# 获取一致预测净利润(未来12个月)/归属于母公司的股东权益_PIT时间序列
from windget import getWestRoeFtmSeries


# 获取一致预测净利润(未来12个月)/归属于母公司的股东权益_PIT
from windget import getWestRoeFtm


# 获取一致预测净利润同比时间序列
from windget import getWestNetProfitYoYSeries


# 获取一致预测净利润同比
from windget import getWestNetProfitYoY


# 获取一致预测净利润同比(FY2比FY1)时间序列
from windget import getWestAvgNpYoYSeries


# 获取一致预测净利润同比(FY2比FY1)
from windget import getWestAvgNpYoY


# 获取一致预测净利润2年复合增长率时间序列
from windget import getWestNetProfitCAgrSeries


# 获取一致预测净利润2年复合增长率
from windget import getWestNetProfitCAgr


# 获取一致预测净利润1周变化率时间序列
from windget import getWestNProc1WSeries


# 获取一致预测净利润1周变化率
from windget import getWestNProc1W


# 获取一致预测净利润4周变化率时间序列
from windget import getWestNProc4WSeries


# 获取一致预测净利润4周变化率
from windget import getWestNProc4W


# 获取一致预测净利润13周变化率时间序列
from windget import getWestNProc13WSeries


# 获取一致预测净利润13周变化率
from windget import getWestNProc13W


# 获取一致预测净利润26周变化率时间序列
from windget import getWestNProc26WSeries


# 获取一致预测净利润26周变化率
from windget import getWestNProc26W


# 获取一致预测每股收益(未来12个月)时间序列
from windget import getWestEpsFtmSeries


# 获取一致预测每股收益(未来12个月)
from windget import getWestEpsFtm


# 获取一致预测每股收益(未来12个月)的变化_1M_PIT时间序列
from windget import getWestEpsFtmChg1MSeries


# 获取一致预测每股收益(未来12个月)的变化_1M_PIT
from windget import getWestEpsFtmChg1M


# 获取一致预测每股收益(未来12个月)的变化_3M_PIT时间序列
from windget import getWestEpsFtmChg3MSeries


# 获取一致预测每股收益(未来12个月)的变化_3M_PIT
from windget import getWestEpsFtmChg3M


# 获取一致预测每股收益(未来12个月)的变化_6M_PIT时间序列
from windget import getWestEpsFtmChg6MSeries


# 获取一致预测每股收益(未来12个月)的变化_6M_PIT
from windget import getWestEpsFtmChg6M


# 获取一致预测每股收益(未来12个月)的变化率_1M_PIT时间序列
from windget import getWestEpsFtm1MSeries


# 获取一致预测每股收益(未来12个月)的变化率_1M_PIT
from windget import getWestEpsFtm1M


# 获取一致预测每股收益(未来12个月)的变化率_3M_PIT时间序列
from windget import getWestEpsFtm3MSeries


# 获取一致预测每股收益(未来12个月)的变化率_3M_PIT
from windget import getWestEpsFtm3M


# 获取一致预测每股收益(未来12个月)的变化率_6M_PIT时间序列
from windget import getWestEpsFtm6MSeries


# 获取一致预测每股收益(未来12个月)的变化率_6M_PIT
from windget import getWestEpsFtm6M


# 获取一致预测每股收益(未来12个月)与EPS(TTM)的变化率_PIT时间序列
from windget import getWestEpsFtmGrowthSeries


# 获取一致预测每股收益(未来12个月)与EPS(TTM)的变化率_PIT
from windget import getWestEpsFtmGrowth


# 获取一致预测营业收入(未来12个月)时间序列
from windget import getWestSalesFtmSeries


# 获取一致预测营业收入(未来12个月)
from windget import getWestSalesFtm


# 获取一致预测营业收入(未来12个月)的变化_1M_PIT时间序列
from windget import getWestSalesFtmChg1MSeries


# 获取一致预测营业收入(未来12个月)的变化_1M_PIT
from windget import getWestSalesFtmChg1M


# 获取一致预测营业收入(未来12个月)的变化_3M_PIT时间序列
from windget import getWestSalesFtmChg3MSeries


# 获取一致预测营业收入(未来12个月)的变化_3M_PIT
from windget import getWestSalesFtmChg3M


# 获取一致预测营业收入(未来12个月)的变化_6M_PIT时间序列
from windget import getWestSalesFtmChg6MSeries


# 获取一致预测营业收入(未来12个月)的变化_6M_PIT
from windget import getWestSalesFtmChg6M


# 获取一致预测营业收入(未来12个月)的变化率_1M_PIT时间序列
from windget import getWestSalesFtm1MSeries


# 获取一致预测营业收入(未来12个月)的变化率_1M_PIT
from windget import getWestSalesFtm1M


# 获取一致预测营业收入(未来12个月)的变化率_3M_PIT时间序列
from windget import getWestSalesFtm3MSeries


# 获取一致预测营业收入(未来12个月)的变化率_3M_PIT
from windget import getWestSalesFtm3M


# 获取一致预测营业收入(未来12个月)的变化率_6M_PIT时间序列
from windget import getWestSalesFtm6MSeries


# 获取一致预测营业收入(未来12个月)的变化率_6M_PIT
from windget import getWestSalesFtm6M


# 获取一致预测营业收入同比时间序列
from windget import getWestSalesYoYSeries


# 获取一致预测营业收入同比
from windget import getWestSalesYoY


# 获取一致预测营业收入2年复合增长率时间序列
from windget import getWestSalesCAgrSeries


# 获取一致预测营业收入2年复合增长率
from windget import getWestSalesCAgr


# 获取一致预测每股现金流(未来12个月)时间序列
from windget import getWestAvgCpSFtmSeries


# 获取一致预测每股现金流(未来12个月)
from windget import getWestAvgCpSFtm


# 获取一致预测息税前利润(未来12个月)时间序列
from windget import getWestAvGebItFtmSeries


# 获取一致预测息税前利润(未来12个月)
from windget import getWestAvGebItFtm


# 获取一致预测息税前利润同比时间序列
from windget import getWestAvGebItYoYSeries


# 获取一致预测息税前利润同比
from windget import getWestAvGebItYoY


# 获取一致预测息税前利润年复合增长率时间序列
from windget import getWestAvGebItCAgrSeries


# 获取一致预测息税前利润年复合增长率
from windget import getWestAvGebItCAgr


# 获取一致预测息税折旧摊销前利润(未来12个月)时间序列
from windget import getWestAvGebItDaFtmSeries


# 获取一致预测息税折旧摊销前利润(未来12个月)
from windget import getWestAvGebItDaFtm


# 获取一致预测息税折旧摊销前利润同比时间序列
from windget import getWestAvGebItDaYoYSeries


# 获取一致预测息税折旧摊销前利润同比
from windget import getWestAvGebItDaYoY


# 获取一致预测息税折旧摊销前利润2年复合增长率时间序列
from windget import getWestAvGebItDaCAgrSeries


# 获取一致预测息税折旧摊销前利润2年复合增长率
from windget import getWestAvGebItDaCAgr


# 获取一致预测利润总额(未来12个月)时间序列
from windget import getWestAvGebTFtmSeries


# 获取一致预测利润总额(未来12个月)
from windget import getWestAvGebTFtm


# 获取一致预测利润总额同比时间序列
from windget import getWestAvGebTYoYSeries


# 获取一致预测利润总额同比
from windget import getWestAvGebTYoY


# 获取一致预测利润总额2年复合增长率时间序列
from windget import getWestAvGebTCAgrSeries


# 获取一致预测利润总额2年复合增长率
from windget import getWestAvGebTCAgr


# 获取一致预测营业利润(未来12个月)时间序列
from windget import getWestAvgOperatingProfitFtmSeries


# 获取一致预测营业利润(未来12个月)
from windget import getWestAvgOperatingProfitFtm


# 获取一致预测营业利润同比时间序列
from windget import getWestAvgOperatingProfitYoYSeries


# 获取一致预测营业利润同比
from windget import getWestAvgOperatingProfitYoY


# 获取一致预测营业利润2年复合增长率时间序列
from windget import getWestAvgOperatingProfitCAgrSeries


# 获取一致预测营业利润2年复合增长率
from windget import getWestAvgOperatingProfitCAgr


# 获取一致预测营业成本(未来12个月)时间序列
from windget import getWestAvgOcFtmSeries


# 获取一致预测营业成本(未来12个月)
from windget import getWestAvgOcFtm


# 获取一致预测营业成本同比时间序列
from windget import getWestAvgOcYoYSeries


# 获取一致预测营业成本同比
from windget import getWestAvgOcYoY


# 获取一致预测营业成本2年复合增长率时间序列
from windget import getWestAvgOcCAgrSeries


# 获取一致预测营业成本2年复合增长率
from windget import getWestAvgOcCAgr


# 获取每股收益预测机构家数时间序列
from windget import getEstInStNumSeries


# 获取每股收益预测机构家数
from windget import getEstInStNum


# 获取每股收益预测机构家数(可选类型)时间序列
from windget import getWestInStNumSeries


# 获取每股收益预测机构家数(可选类型)
from windget import getWestInStNum


# 获取预测每股收益平均值时间序列
from windget import getEstEpsSeries


# 获取预测每股收益平均值
from windget import getEstEps


# 获取预测每股收益平均值(币种转换)时间序列
from windget import getEstEps1Series


# 获取预测每股收益平均值(币种转换)
from windget import getEstEps1


# 获取预测每股收益平均值(可选类型)时间序列
from windget import getWestEpsSeries


# 获取预测每股收益平均值(可选类型)
from windget import getWestEps


# 获取预测每股收益平均值(可选类型,币种转换)时间序列
from windget import getWestEps1Series


# 获取预测每股收益平均值(可选类型,币种转换)
from windget import getWestEps1


# 获取预测每股收益最大值时间序列
from windget import getEstMaxEpsSeries


# 获取预测每股收益最大值
from windget import getEstMaxEps


# 获取预测每股收益最大值(币种转换)时间序列
from windget import getEstMaxEps1Series


# 获取预测每股收益最大值(币种转换)
from windget import getEstMaxEps1


# 获取预测每股收益最大值(可选类型)时间序列
from windget import getWestMaxEpsSeries


# 获取预测每股收益最大值(可选类型)
from windget import getWestMaxEps


# 获取预测每股收益最大值(可选类型,币种转换)时间序列
from windget import getWestMaxEps1Series


# 获取预测每股收益最大值(可选类型,币种转换)
from windget import getWestMaxEps1


# 获取预测每股收益最小值时间序列
from windget import getEstMinePsSeries


# 获取预测每股收益最小值
from windget import getEstMinePs


# 获取预测每股收益最小值(币种转换)时间序列
from windget import getEstMinePs1Series


# 获取预测每股收益最小值(币种转换)
from windget import getEstMinePs1


# 获取预测每股收益最小值(可选类型)时间序列
from windget import getWestMinePsSeries


# 获取预测每股收益最小值(可选类型)
from windget import getWestMinePs


# 获取预测每股收益最小值(可选类型,币种转换)时间序列
from windget import getWestMinePs1Series


# 获取预测每股收益最小值(可选类型,币种转换)
from windget import getWestMinePs1


# 获取预测每股收益中值时间序列
from windget import getEstMedianEpsSeries


# 获取预测每股收益中值
from windget import getEstMedianEps


# 获取预测每股收益中值(币种转换)时间序列
from windget import getEstMedianEps1Series


# 获取预测每股收益中值(币种转换)
from windget import getEstMedianEps1


# 获取预测每股收益中值(可选类型)时间序列
from windget import getWestMedianEpsSeries


# 获取预测每股收益中值(可选类型)
from windget import getWestMedianEps


# 获取预测每股收益中值(可选类型,币种转换)时间序列
from windget import getWestMedianEps1Series


# 获取预测每股收益中值(可选类型,币种转换)
from windget import getWestMedianEps1


# 获取预测每股收益标准差时间序列
from windget import getEstStdEpsSeries


# 获取预测每股收益标准差
from windget import getEstStdEps


# 获取预测每股收益标准差(币种转换)时间序列
from windget import getEstStdEps1Series


# 获取预测每股收益标准差(币种转换)
from windget import getEstStdEps1


# 获取预测每股收益标准差(可选类型)时间序列
from windget import getWestStdEpsSeries


# 获取预测每股收益标准差(可选类型)
from windget import getWestStdEps


# 获取预测每股收益标准差(可选类型,币种转换)时间序列
from windget import getWestStdEps1Series


# 获取预测每股收益标准差(可选类型,币种转换)
from windget import getWestStdEps1


# 获取预测营业收入平均值时间序列
from windget import getEstSalesSeries


# 获取预测营业收入平均值
from windget import getEstSales


# 获取预测营业收入平均值(币种转换)时间序列
from windget import getEstSales1Series


# 获取预测营业收入平均值(币种转换)
from windget import getEstSales1


# 获取预测营业收入平均值(可选类型)时间序列
from windget import getWestSalesSeries


# 获取预测营业收入平均值(可选类型)
from windget import getWestSales


# 获取预测营业收入平均值(可选类型,币种转换)时间序列
from windget import getWestSales1Series


# 获取预测营业收入平均值(可选类型,币种转换)
from windget import getWestSales1


# 获取预测营业收入最大值时间序列
from windget import getEstMaxSalesSeries


# 获取预测营业收入最大值
from windget import getEstMaxSales


# 获取预测营业收入最大值(币种转换)时间序列
from windget import getEstMaxSales1Series


# 获取预测营业收入最大值(币种转换)
from windget import getEstMaxSales1


# 获取预测营业收入最大值(可选类型)时间序列
from windget import getWestMaxSalesSeries


# 获取预测营业收入最大值(可选类型)
from windget import getWestMaxSales


# 获取预测营业收入最大值(可选类型,币种转换)时间序列
from windget import getWestMaxSales1Series


# 获取预测营业收入最大值(可选类型,币种转换)
from windget import getWestMaxSales1


# 获取预测营业收入最小值时间序列
from windget import getEstMinSalesSeries


# 获取预测营业收入最小值
from windget import getEstMinSales


# 获取预测营业收入最小值(币种转换)时间序列
from windget import getEstMinSales1Series


# 获取预测营业收入最小值(币种转换)
from windget import getEstMinSales1


# 获取预测营业收入最小值(可选类型)时间序列
from windget import getWestMinSalesSeries


# 获取预测营业收入最小值(可选类型)
from windget import getWestMinSales


# 获取预测营业收入最小值(可选类型,币种转换)时间序列
from windget import getWestMinSales1Series


# 获取预测营业收入最小值(可选类型,币种转换)
from windget import getWestMinSales1


# 获取预测营业收入中值时间序列
from windget import getEstMedianSalesSeries


# 获取预测营业收入中值
from windget import getEstMedianSales


# 获取预测营业收入中值(币种转换)时间序列
from windget import getEstMedianSales1Series


# 获取预测营业收入中值(币种转换)
from windget import getEstMedianSales1


# 获取预测营业收入中值(可选类型)时间序列
from windget import getWestMedianSalesSeries


# 获取预测营业收入中值(可选类型)
from windget import getWestMedianSales


# 获取预测营业收入中值(可选类型,币种转换)时间序列
from windget import getWestMedianSales1Series


# 获取预测营业收入中值(可选类型,币种转换)
from windget import getWestMedianSales1


# 获取预测营业收入标准差时间序列
from windget import getEstStdSalesSeries


# 获取预测营业收入标准差
from windget import getEstStdSales


# 获取预测营业收入标准差(币种转换)时间序列
from windget import getEstStdSales1Series


# 获取预测营业收入标准差(币种转换)
from windget import getEstStdSales1


# 获取预测营业收入标准差(可选类型)时间序列
from windget import getWestStdSalesSeries


# 获取预测营业收入标准差(可选类型)
from windget import getWestStdSales


# 获取预测营业收入标准差(可选类型,币种转换)时间序列
from windget import getWestStdSales1Series


# 获取预测营业收入标准差(可选类型,币种转换)
from windget import getWestStdSales1


# 获取预测净利润平均值时间序列
from windget import getEstNetProfitSeries


# 获取预测净利润平均值
from windget import getEstNetProfit


# 获取预测净利润平均值(币种转换)时间序列
from windget import getEstNetProfit1Series


# 获取预测净利润平均值(币种转换)
from windget import getEstNetProfit1


# 获取预测净利润平均值(可选类型)时间序列
from windget import getWestNetProfitSeries


# 获取预测净利润平均值(可选类型)
from windget import getWestNetProfit


# 获取预测净利润平均值(可选类型,币种转换)时间序列
from windget import getWestNetProfit1Series


# 获取预测净利润平均值(可选类型,币种转换)
from windget import getWestNetProfit1


# 获取预测净利润最大值时间序列
from windget import getEstMaxNetProfitSeries


# 获取预测净利润最大值
from windget import getEstMaxNetProfit


# 获取预测净利润最大值(币种转换)时间序列
from windget import getEstMaxNetProfit1Series


# 获取预测净利润最大值(币种转换)
from windget import getEstMaxNetProfit1


# 获取预测净利润最大值(可选类型)时间序列
from windget import getWestMaxNetProfitSeries


# 获取预测净利润最大值(可选类型)
from windget import getWestMaxNetProfit


# 获取预测净利润最大值(可选类型,币种转换)时间序列
from windget import getWestMaxNetProfit1Series


# 获取预测净利润最大值(可选类型,币种转换)
from windget import getWestMaxNetProfit1


# 获取预测净利润最小值时间序列
from windget import getEstMinNetProfitSeries


# 获取预测净利润最小值
from windget import getEstMinNetProfit


# 获取预测净利润最小值(币种转换)时间序列
from windget import getEstMinNetProfit1Series


# 获取预测净利润最小值(币种转换)
from windget import getEstMinNetProfit1


# 获取预测净利润最小值(可选类型)时间序列
from windget import getWestMinNetProfitSeries


# 获取预测净利润最小值(可选类型)
from windget import getWestMinNetProfit


# 获取预测净利润最小值(可选类型,币种转换)时间序列
from windget import getWestMinNetProfit1Series


# 获取预测净利润最小值(可选类型,币种转换)
from windget import getWestMinNetProfit1


# 获取预测净利润中值时间序列
from windget import getEstMedianNetProfitSeries


# 获取预测净利润中值
from windget import getEstMedianNetProfit


# 获取预测净利润中值(币种转换)时间序列
from windget import getEstMedianNetProfit1Series


# 获取预测净利润中值(币种转换)
from windget import getEstMedianNetProfit1


# 获取预测净利润中值(可选类型)时间序列
from windget import getWestMedianNetProfitSeries


# 获取预测净利润中值(可选类型)
from windget import getWestMedianNetProfit


# 获取预测净利润中值(可选类型,币种转换)时间序列
from windget import getWestMedianNetProfit1Series


# 获取预测净利润中值(可选类型,币种转换)
from windget import getWestMedianNetProfit1


# 获取预测净利润标准差时间序列
from windget import getEstStdNetProfitSeries


# 获取预测净利润标准差
from windget import getEstStdNetProfit


# 获取预测净利润标准差(币种转换)时间序列
from windget import getEstStdNetProfit1Series


# 获取预测净利润标准差(币种转换)
from windget import getEstStdNetProfit1


# 获取预测净利润标准差(可选类型)时间序列
from windget import getWestStdNetProfitSeries


# 获取预测净利润标准差(可选类型)
from windget import getWestStdNetProfit


# 获取预测净利润标准差(可选类型,币种转换)时间序列
from windget import getWestStdNetProfit1Series


# 获取预测净利润标准差(可选类型,币种转换)
from windget import getWestStdNetProfit1


# 获取预测利润总额平均值时间序列
from windget import getEstAvGebTSeries


# 获取预测利润总额平均值
from windget import getEstAvGebT


# 获取预测利润总额平均值(币种转换)时间序列
from windget import getEstAvGebT1Series


# 获取预测利润总额平均值(币种转换)
from windget import getEstAvGebT1


# 获取预测利润总额平均值(可选类型)时间序列
from windget import getWestAvGebTSeries


# 获取预测利润总额平均值(可选类型)
from windget import getWestAvGebT


# 获取预测利润总额平均值(可选类型,币种转换)时间序列
from windget import getWestAvGebT1Series


# 获取预测利润总额平均值(可选类型,币种转换)
from windget import getWestAvGebT1


# 获取预测利润总额最大值时间序列
from windget import getEstMaxEBtSeries


# 获取预测利润总额最大值
from windget import getEstMaxEBt


# 获取预测利润总额最大值(币种转换)时间序列
from windget import getEstMaxEBt1Series


# 获取预测利润总额最大值(币种转换)
from windget import getEstMaxEBt1


# 获取预测利润总额最大值(可选类型)时间序列
from windget import getWestMaxEBtSeries


# 获取预测利润总额最大值(可选类型)
from windget import getWestMaxEBt


# 获取预测利润总额最大值(可选类型,币种转换)时间序列
from windget import getWestMaxEBt1Series


# 获取预测利润总额最大值(可选类型,币种转换)
from windget import getWestMaxEBt1


# 获取预测利润总额最小值时间序列
from windget import getEstMinEBTSeries


# 获取预测利润总额最小值
from windget import getEstMinEBT


# 获取预测利润总额最小值(币种转换)时间序列
from windget import getEstMinEBT1Series


# 获取预测利润总额最小值(币种转换)
from windget import getEstMinEBT1


# 获取预测利润总额最小值(可选类型)时间序列
from windget import getWestMinEBTSeries


# 获取预测利润总额最小值(可选类型)
from windget import getWestMinEBT


# 获取预测利润总额最小值(可选类型,币种转换)时间序列
from windget import getWestMinEBT1Series


# 获取预测利润总额最小值(可选类型,币种转换)
from windget import getWestMinEBT1


# 获取预测利润总额中值时间序列
from windget import getEstMedianEBtSeries


# 获取预测利润总额中值
from windget import getEstMedianEBt


# 获取预测利润总额中值(币种转换)时间序列
from windget import getEstMedianEBt1Series


# 获取预测利润总额中值(币种转换)
from windget import getEstMedianEBt1


# 获取预测利润总额中值(可选类型)时间序列
from windget import getWestMedianEBtSeries


# 获取预测利润总额中值(可选类型)
from windget import getWestMedianEBt


# 获取预测利润总额中值(可选类型,币种转换)时间序列
from windget import getWestMedianEBt1Series


# 获取预测利润总额中值(可选类型,币种转换)
from windget import getWestMedianEBt1


# 获取预测利润总额标准差时间序列
from windget import getEstStDebtSeries


# 获取预测利润总额标准差
from windget import getEstStDebt


# 获取预测利润总额标准差(币种转换)时间序列
from windget import getEstStDebt1Series


# 获取预测利润总额标准差(币种转换)
from windget import getEstStDebt1


# 获取预测利润总额标准差(可选类型)时间序列
from windget import getWestStDebtSeries


# 获取预测利润总额标准差(可选类型)
from windget import getWestStDebt


# 获取预测利润总额标准差(可选类型,币种转换)时间序列
from windget import getWestStDebt1Series


# 获取预测利润总额标准差(可选类型,币种转换)
from windget import getWestStDebt1


# 获取预测营业利润平均值时间序列
from windget import getEstAvgOperatingProfitSeries


# 获取预测营业利润平均值
from windget import getEstAvgOperatingProfit


# 获取预测营业利润平均值(币种转换)时间序列
from windget import getEstAvgOperatingProfit1Series


# 获取预测营业利润平均值(币种转换)
from windget import getEstAvgOperatingProfit1


# 获取预测营业利润平均值(可选类型)时间序列
from windget import getWestAvgOperatingProfitSeries


# 获取预测营业利润平均值(可选类型)
from windget import getWestAvgOperatingProfit


# 获取预测营业利润平均值(可选类型,币种转换)时间序列
from windget import getWestAvgOperatingProfit1Series


# 获取预测营业利润平均值(可选类型,币种转换)
from windget import getWestAvgOperatingProfit1


# 获取预测营业利润最大值时间序列
from windget import getEstMaxOperatingProfitSeries


# 获取预测营业利润最大值
from windget import getEstMaxOperatingProfit


# 获取预测营业利润最大值(币种转换)时间序列
from windget import getEstMaxOperatingProfit1Series


# 获取预测营业利润最大值(币种转换)
from windget import getEstMaxOperatingProfit1


# 获取预测营业利润最大值(可选类型)时间序列
from windget import getWestMaxOperatingProfitSeries


# 获取预测营业利润最大值(可选类型)
from windget import getWestMaxOperatingProfit


# 获取预测营业利润最大值(可选类型,币种转换)时间序列
from windget import getWestMaxOperatingProfit1Series


# 获取预测营业利润最大值(可选类型,币种转换)
from windget import getWestMaxOperatingProfit1


# 获取预测营业利润最小值时间序列
from windget import getEstMinOperatingProfitSeries


# 获取预测营业利润最小值
from windget import getEstMinOperatingProfit


# 获取预测营业利润最小值(币种转换)时间序列
from windget import getEstMinOperatingProfit1Series


# 获取预测营业利润最小值(币种转换)
from windget import getEstMinOperatingProfit1


# 获取预测营业利润最小值(可选类型)时间序列
from windget import getWestMinOperatingProfitSeries


# 获取预测营业利润最小值(可选类型)
from windget import getWestMinOperatingProfit


# 获取预测营业利润最小值(可选类型,币种转换)时间序列
from windget import getWestMinOperatingProfit1Series


# 获取预测营业利润最小值(可选类型,币种转换)
from windget import getWestMinOperatingProfit1


# 获取预测营业利润中值时间序列
from windget import getEstMedianOperatingProfitSeries


# 获取预测营业利润中值
from windget import getEstMedianOperatingProfit


# 获取预测营业利润中值(币种转换)时间序列
from windget import getEstMedianOperatingProfit1Series


# 获取预测营业利润中值(币种转换)
from windget import getEstMedianOperatingProfit1


# 获取预测营业利润中值(可选类型)时间序列
from windget import getWestMedianOperatingProfitSeries


# 获取预测营业利润中值(可选类型)
from windget import getWestMedianOperatingProfit


# 获取预测营业利润中值(可选类型,币种转换)时间序列
from windget import getWestMedianOperatingProfit1Series


# 获取预测营业利润中值(可选类型,币种转换)
from windget import getWestMedianOperatingProfit1


# 获取预测营业利润标准差时间序列
from windget import getEstStdOperatingProfitSeries


# 获取预测营业利润标准差
from windget import getEstStdOperatingProfit


# 获取预测营业利润标准差(币种转换)时间序列
from windget import getEstStdOperatingProfit1Series


# 获取预测营业利润标准差(币种转换)
from windget import getEstStdOperatingProfit1


# 获取预测营业利润标准差(可选类型)时间序列
from windget import getWestStdOperatingProfitSeries


# 获取预测营业利润标准差(可选类型)
from windget import getWestStdOperatingProfit


# 获取预测营业利润标准差(可选类型,币种转换)时间序列
from windget import getWestStdOperatingProfit1Series


# 获取预测营业利润标准差(可选类型,币种转换)
from windget import getWestStdOperatingProfit1


# 获取营业收入调高家数时间序列
from windget import getEstSalesUpgradeSeries


# 获取营业收入调高家数
from windget import getEstSalesUpgrade


# 获取营业收入调高家数(可选类型)时间序列
from windget import getWestSalesUpgradeSeries


# 获取营业收入调高家数(可选类型)
from windget import getWestSalesUpgrade


# 获取营业收入调低家数时间序列
from windget import getEstSalesDowngradeSeries


# 获取营业收入调低家数
from windget import getEstSalesDowngrade


# 获取营业收入调低家数(可选类型)时间序列
from windget import getWestSalesDowngradeSeries


# 获取营业收入调低家数(可选类型)
from windget import getWestSalesDowngrade


# 获取营业收入维持家数时间序列
from windget import getEstSalesMaintainSeries


# 获取营业收入维持家数
from windget import getEstSalesMaintain


# 获取营业收入维持家数(可选类型)时间序列
from windget import getWestSalesMaintainSeries


# 获取营业收入维持家数(可选类型)
from windget import getWestSalesMaintain


# 获取净利润调高家数时间序列
from windget import getEstNetProfitUpgradeSeries


# 获取净利润调高家数
from windget import getEstNetProfitUpgrade


# 获取净利润调高家数(可选类型)时间序列
from windget import getWestNetProfitUpgradeSeries


# 获取净利润调高家数(可选类型)
from windget import getWestNetProfitUpgrade


# 获取净利润调低家数时间序列
from windget import getEstNetProfitDowngradeSeries


# 获取净利润调低家数
from windget import getEstNetProfitDowngrade


# 获取净利润调低家数(可选类型)时间序列
from windget import getWestNetProfitDowngradeSeries


# 获取净利润调低家数(可选类型)
from windget import getWestNetProfitDowngrade


# 获取净利润维持家数时间序列
from windget import getEstNetProfitMaintainSeries


# 获取净利润维持家数
from windget import getEstNetProfitMaintain


# 获取净利润维持家数(可选类型)时间序列
from windget import getWestNetProfitMaintainSeries


# 获取净利润维持家数(可选类型)
from windget import getWestNetProfitMaintain


# 获取预测净利润增长率时间序列
from windget import getEstYoYNetProfitSeries


# 获取预测净利润增长率
from windget import getEstYoYNetProfit


# 获取预测净利润增长率(可选类型)时间序列
from windget import getWestYoYNetProfitSeries


# 获取预测净利润增长率(可选类型)
from windget import getWestYoYNetProfit


# 获取预测营业收入增长率时间序列
from windget import getEstYoYSalesSeries


# 获取预测营业收入增长率
from windget import getEstYoYSales


# 获取预测营业收入增长率(可选类型)时间序列
from windget import getWestYoYSalesSeries


# 获取预测营业收入增长率(可选类型)
from windget import getWestYoYSales


# 获取综合评级(数值)时间序列
from windget import getRatingAvgSeries


# 获取综合评级(数值)
from windget import getRatingAvg


# 获取综合评级(数值)(可选类型)时间序列
from windget import getWRatingAvgDataSeries


# 获取综合评级(数值)(可选类型)
from windget import getWRatingAvgData


# 获取综合评级(中文)时间序列
from windget import getRatingAvgChNSeries


# 获取综合评级(中文)
from windget import getRatingAvgChN


# 获取综合评级(中文)(可选类型)时间序列
from windget import getWRatingAvgCnSeries


# 获取综合评级(中文)(可选类型)
from windget import getWRatingAvgCn


# 获取综合评级(英文)时间序列
from windget import getRatingAvGengSeries


# 获取综合评级(英文)
from windget import getRatingAvGeng


# 获取综合评级(英文)(可选类型)时间序列
from windget import getWRatingAvgEnSeries


# 获取综合评级(英文)(可选类型)
from windget import getWRatingAvgEn


# 获取评级机构家数时间序列
from windget import getRatingInStNumSeries


# 获取评级机构家数
from windget import getRatingInStNum


# 获取评级机构家数(可选类型)时间序列
from windget import getWRatingInStNumSeries


# 获取评级机构家数(可选类型)
from windget import getWRatingInStNum


# 获取评级调高家数时间序列
from windget import getRatingUpgradeSeries


# 获取评级调高家数
from windget import getRatingUpgrade


# 获取评级调高家数(可选类型)时间序列
from windget import getWRatingUpgradeSeries


# 获取评级调高家数(可选类型)
from windget import getWRatingUpgrade


# 获取评级调低家数时间序列
from windget import getRatingDowngradeSeries


# 获取评级调低家数
from windget import getRatingDowngrade


# 获取评级调低家数(可选类型)时间序列
from windget import getWRatingDowngradeSeries


# 获取评级调低家数(可选类型)
from windget import getWRatingDowngrade


# 获取评级维持家数时间序列
from windget import getRatingMaintainSeries


# 获取评级维持家数
from windget import getRatingMaintain


# 获取评级维持家数(可选类型)时间序列
from windget import getWRatingMaintainSeries


# 获取评级维持家数(可选类型)
from windget import getWRatingMaintain


# 获取评级买入家数时间序列
from windget import getRatingNumOfBuySeries


# 获取评级买入家数
from windget import getRatingNumOfBuy


# 获取评级买入家数(可选类型)时间序列
from windget import getWRatingNumOfBuySeries


# 获取评级买入家数(可选类型)
from windget import getWRatingNumOfBuy


# 获取评级增持家数时间序列
from windget import getRatingNumOfOutperformSeries


# 获取评级增持家数
from windget import getRatingNumOfOutperform


# 获取评级增持家数(可选类型)时间序列
from windget import getWRatingNumOfOutperformSeries


# 获取评级增持家数(可选类型)
from windget import getWRatingNumOfOutperform


# 获取评级中性家数时间序列
from windget import getRatingNumOfHoldSeries


# 获取评级中性家数
from windget import getRatingNumOfHold


# 获取评级中性家数(可选类型)时间序列
from windget import getWRatingNumOfHoldSeries


# 获取评级中性家数(可选类型)
from windget import getWRatingNumOfHold


# 获取评级减持家数时间序列
from windget import getRatingNumOfUnderPerformSeries


# 获取评级减持家数
from windget import getRatingNumOfUnderPerform


# 获取评级减持家数(可选类型)时间序列
from windget import getWRatingNumOfUnderPerformSeries


# 获取评级减持家数(可选类型)
from windget import getWRatingNumOfUnderPerform


# 获取评级卖出家数时间序列
from windget import getRatingNumOfSellSeries


# 获取评级卖出家数
from windget import getRatingNumOfSell


# 获取评级卖出家数(可选类型)时间序列
from windget import getWRatingNumOfSellSeries


# 获取评级卖出家数(可选类型)
from windget import getWRatingNumOfSell


# 获取一致预测目标价时间序列
from windget import getWRatingTargetPriceSeries


# 获取一致预测目标价
from windget import getWRatingTargetPrice


# 获取一致预测目标价(可选类型)时间序列
from windget import getTargetPriceAvgSeries


# 获取一致预测目标价(可选类型)
from windget import getTargetPriceAvg


# 获取一致预测目标价上升空间_PIT时间序列
from windget import getWestFReturnSeries


# 获取一致预测目标价上升空间_PIT
from windget import getWestFReturn


# 获取大事日期(大事后预测)时间序列
from windget import getEstEventDateSeries


# 获取大事日期(大事后预测)
from windget import getEstEventDate


# 获取营业收入预测机构家数(可选类型)时间序列
from windget import getWestInStNumSalesSeries


# 获取营业收入预测机构家数(可选类型)
from windget import getWestInStNumSales


# 获取净利润预测机构家数(可选类型)时间序列
from windget import getWestInStNumNpSeries


# 获取净利润预测机构家数(可选类型)
from windget import getWestInStNumNp


# 获取每股现金流预测机构家数(可选类型)时间序列
from windget import getWestInStNumCpSSeries


# 获取每股现金流预测机构家数(可选类型)
from windget import getWestInStNumCpS


# 获取每股股利预测机构家数(可选类型)时间序列
from windget import getWestInStNumDpsSeries


# 获取每股股利预测机构家数(可选类型)
from windget import getWestInStNumDps


# 获取息税前利润预测机构家数(可选类型)时间序列
from windget import getWestInStNumEbItSeries


# 获取息税前利润预测机构家数(可选类型)
from windget import getWestInStNumEbIt


# 获取息税折旧摊销前利润预测机构家数(可选类型)时间序列
from windget import getWestInStNumEbItDaSeries


# 获取息税折旧摊销前利润预测机构家数(可选类型)
from windget import getWestInStNumEbItDa


# 获取每股净资产预测机构家数(可选类型)时间序列
from windget import getWestInStNumBpSSeries


# 获取每股净资产预测机构家数(可选类型)
from windget import getWestInStNumBpS


# 获取利润总额预测机构家数(可选类型)时间序列
from windget import getWestInStNumEBtSeries


# 获取利润总额预测机构家数(可选类型)
from windget import getWestInStNumEBt


# 获取总资产收益率预测机构家数(可选类型)时间序列
from windget import getWestInStNumRoaSeries


# 获取总资产收益率预测机构家数(可选类型)
from windget import getWestInStNumRoa


# 获取净资产收益率预测机构家数(可选类型)时间序列
from windget import getWestInStNumRoeSeries


# 获取净资产收益率预测机构家数(可选类型)
from windget import getWestInStNumRoe


# 获取营业利润预测机构家数(可选类型)时间序列
from windget import getWestInStNumOpSeries


# 获取营业利润预测机构家数(可选类型)
from windget import getWestInStNumOp


# 获取预测营业成本平均值(可选类型)时间序列
from windget import getWestAvgOcSeries


# 获取预测营业成本平均值(可选类型)
from windget import getWestAvgOc


# 获取预测营业成本最大值(可选类型)时间序列
from windget import getWestMaxOcSeries


# 获取预测营业成本最大值(可选类型)
from windget import getWestMaxOc


# 获取预测营业成本最小值(可选类型)时间序列
from windget import getWestMinoCSeries


# 获取预测营业成本最小值(可选类型)
from windget import getWestMinoC


# 获取预测营业成本中值(可选类型)时间序列
from windget import getWestMediaOcSeries


# 获取预测营业成本中值(可选类型)
from windget import getWestMediaOc


# 获取预测营业成本标准差(可选类型)时间序列
from windget import getWestSToCSeries


# 获取预测营业成本标准差(可选类型)
from windget import getWestSToC


# 获取预测基准股本综合值(可选类型)时间序列
from windget import getWestAvgSharesSeries


# 获取预测基准股本综合值(可选类型)
from windget import getWestAvgShares


# 获取盈利修正比例(可选类型)时间序列
from windget import getErrWiSeries


# 获取盈利修正比例(可选类型)
from windget import getErrWi


# 获取未来3年净利润复合年增长率时间序列
from windget import getEstCAgrNpSeries


# 获取未来3年净利润复合年增长率
from windget import getEstCAgrNp


# 获取未来3年营业总收入复合年增长率时间序列
from windget import getEstCAgrSalesSeries


# 获取未来3年营业总收入复合年增长率
from windget import getEstCAgrSales


# 获取销售毛利率预测机构家数(可选类型)时间序列
from windget import getWestInStNumGmSeries


# 获取销售毛利率预测机构家数(可选类型)
from windget import getWestInStNumGm


# 获取预测营业成本平均值(可选类型,币种转换)时间序列
from windget import getWestAvgOc1Series


# 获取预测营业成本平均值(可选类型,币种转换)
from windget import getWestAvgOc1


# 获取预测营业成本最大值(可选类型,币种转换)时间序列
from windget import getWestMaxOc1Series


# 获取预测营业成本最大值(可选类型,币种转换)
from windget import getWestMaxOc1


# 获取预测营业成本最小值(可选类型,币种转换)时间序列
from windget import getWestMinoC1Series


# 获取预测营业成本最小值(可选类型,币种转换)
from windget import getWestMinoC1


# 获取预测营业成本中值(可选类型,币种转换)时间序列
from windget import getWestMediaOc1Series


# 获取预测营业成本中值(可选类型,币种转换)
from windget import getWestMediaOc1


# 获取预测营业成本标准差(可选类型,币种转换)时间序列
from windget import getWestSToC1Series


# 获取预测营业成本标准差(可选类型,币种转换)
from windget import getWestSToC1


# 获取前次最低目标价时间序列
from windget import getEstPreLowPriceInStSeries


# 获取前次最低目标价
from windget import getEstPreLowPriceInSt


# 获取前次最高目标价时间序列
from windget import getEstPreHighPriceInStSeries


# 获取前次最高目标价
from windget import getEstPreHighPriceInSt


# 获取本次最低目标价时间序列
from windget import getEstLowPriceInStSeries


# 获取本次最低目标价
from windget import getEstLowPriceInSt


# 获取本次最高目标价时间序列
from windget import getEstHighPriceInStSeries


# 获取本次最高目标价
from windget import getEstHighPriceInSt


# 获取机构投资评级(原始)时间序列
from windget import getEstOrGratingInStSeries


# 获取机构投资评级(原始)
from windget import getEstOrGratingInSt


# 获取机构投资评级(标准化得分)时间序列
from windget import getEstScoreRatingInStSeries


# 获取机构投资评级(标准化得分)
from windget import getEstScoreRatingInSt


# 获取机构投资评级(标准化评级)时间序列
from windget import getEstStdRatingInStSeries


# 获取机构投资评级(标准化评级)
from windget import getEstStdRatingInSt


# 获取机构最近评级时间时间序列
from windget import getEstNewRatingTimeInStSeries


# 获取机构最近评级时间
from windget import getEstNewRatingTimeInSt


# 获取机构最近预测时间时间序列
from windget import getEstEstNewTimeInStSeries


# 获取机构最近预测时间
from windget import getEstEstNewTimeInSt


# 获取机构预测营业收入时间序列
from windget import getEstSalesInStSeries


# 获取机构预测营业收入
from windget import getEstSalesInSt


# 获取机构预测净利润时间序列
from windget import getEstNetProfitInStSeries


# 获取机构预测净利润
from windget import getEstNetProfitInSt


# 获取机构预测每股收益时间序列
from windget import getEstEpsInStSeries


# 获取机构预测每股收益
from windget import getEstEpsInSt


# 获取机构首次评级时间时间序列
from windget import getEstFrStRatingTimeInStSeries


# 获取机构首次评级时间
from windget import getEstFrStRatingTimeInSt


# 获取评级研究员时间序列
from windget import getEstRatingAnalystSeries


# 获取评级研究员
from windget import getEstRatingAnalyst


# 获取预测研究员时间序列
from windget import getEstEstAnalystSeries


# 获取预测研究员
from windget import getEstEstAnalyst


# 获取内容时间序列
from windget import getEstRpTAbstractInStSeries


# 获取内容
from windget import getEstRpTAbstractInSt


# 获取报告标题时间序列
from windget import getEstRpTTitleInStSeries


# 获取报告标题
from windget import getEstRpTTitleInSt


# 获取预告净利润变动幅度(%)时间序列
from windget import getProfitNoticeChangeSeries


# 获取预告净利润变动幅度(%)
from windget import getProfitNoticeChange


# 获取去年同期每股收益时间序列
from windget import getProfitNoticeLaStepsSeries


# 获取去年同期每股收益
from windget import getProfitNoticeLaSteps


# 获取可分配利润时间序列
from windget import getStmNoteProfitApr3Series


# 获取可分配利润
from windget import getStmNoteProfitApr3


# 获取上年同期扣非净利润时间序列
from windget import getProfitNoticeLastYearDeductedProfitSeries


# 获取上年同期扣非净利润
from windget import getProfitNoticeLastYearDeductedProfit


# 获取上年同期营业收入时间序列
from windget import getProfitNoticeLastYearIncomeSeries


# 获取上年同期营业收入
from windget import getProfitNoticeLastYearIncome


# 获取上年同期扣除后营业收入时间序列
from windget import getProfitNoticeLastYearDeductedSalesSeries


# 获取上年同期扣除后营业收入
from windget import getProfitNoticeLastYearDeductedSales


# 获取预告基本每股收益下限时间序列
from windget import getProfitNoticeBasicEarnMaxSeries


# 获取预告基本每股收益下限
from windget import getProfitNoticeBasicEarnMax


# 获取预告基本每股收益上限时间序列
from windget import getProfitNoticeBasicEarnMinSeries


# 获取预告基本每股收益上限
from windget import getProfitNoticeBasicEarnMin


# 获取预告扣非后基本每股收益下限时间序列
from windget import getProfitNoticeDeductedEarnMinSeries


# 获取预告扣非后基本每股收益下限
from windget import getProfitNoticeDeductedEarnMin


# 获取预告扣非后基本每股收益上限时间序列
from windget import getProfitNoticeDeductedEarnMaxSeries


# 获取预告扣非后基本每股收益上限
from windget import getProfitNoticeDeductedEarnMax


# 获取上年同期扣非后基本每股收益时间序列
from windget import getProfitNoticeLastYearDeductedEarnSeries


# 获取上年同期扣非后基本每股收益
from windget import getProfitNoticeLastYearDeductedEarn


# 获取预告净利润上限时间序列
from windget import getProfitNoticeNetProfitMaxSeries


# 获取预告净利润上限
from windget import getProfitNoticeNetProfitMax


# 获取单季度.预告净利润上限(海外)时间序列
from windget import getQProfitNoticeNetProfitMaxSeries


# 获取单季度.预告净利润上限(海外)
from windget import getQProfitNoticeNetProfitMax


# 获取预告净利润下限时间序列
from windget import getProfitNoticeNetProfitMinSeries


# 获取预告净利润下限
from windget import getProfitNoticeNetProfitMin


# 获取单季度.预告净利润下限(海外)时间序列
from windget import getQProfitNoticeNetProfitMinSeries


# 获取单季度.预告净利润下限(海外)
from windget import getQProfitNoticeNetProfitMin


# 获取预告净利润同比增长上限时间序列
from windget import getProfitNoticeChangeMaxSeries


# 获取预告净利润同比增长上限
from windget import getProfitNoticeChangeMax


# 获取单季度.预告净利润同比增长上限(海外)时间序列
from windget import getQProfitNoticeChangeMaxSeries


# 获取单季度.预告净利润同比增长上限(海外)
from windget import getQProfitNoticeChangeMax


# 获取预告净利润同比增长下限时间序列
from windget import getProfitNoticeChangeMinSeries


# 获取预告净利润同比增长下限
from windget import getProfitNoticeChangeMin


# 获取单季度.预告净利润同比增长下限(海外)时间序列
from windget import getQProfitNoticeChangeMinSeries


# 获取单季度.预告净利润同比增长下限(海外)
from windget import getQProfitNoticeChangeMin


# 获取预告扣非净利润上限时间序列
from windget import getProfitNoticeDeductedProfitMaxSeries


# 获取预告扣非净利润上限
from windget import getProfitNoticeDeductedProfitMax


# 获取预告扣非净利润下限时间序列
from windget import getProfitNoticeDeductedProfitMinSeries


# 获取预告扣非净利润下限
from windget import getProfitNoticeDeductedProfitMin


# 获取预告扣非净利润同比增长上限时间序列
from windget import getProfitNoticeDeductedProfitYoYMaxSeries


# 获取预告扣非净利润同比增长上限
from windget import getProfitNoticeDeductedProfitYoYMax


# 获取预告扣非净利润同比增长下限时间序列
from windget import getProfitNoticeDeductedProfitYoYMinSeries


# 获取预告扣非净利润同比增长下限
from windget import getProfitNoticeDeductedProfitYoYMin


# 获取预告营业收入上限时间序列
from windget import getProfitNoticeIncomeMaxSeries


# 获取预告营业收入上限
from windget import getProfitNoticeIncomeMax


# 获取预告营业收入下限时间序列
from windget import getProfitNoticeIncomeMinSeries


# 获取预告营业收入下限
from windget import getProfitNoticeIncomeMin


# 获取预告扣除后营业收入上限时间序列
from windget import getProfitNoticeDeductedSalesMaxSeries


# 获取预告扣除后营业收入上限
from windget import getProfitNoticeDeductedSalesMax


# 获取预告扣除后营业收入下限时间序列
from windget import getProfitNoticeDeductedSalesMinSeries


# 获取预告扣除后营业收入下限
from windget import getProfitNoticeDeductedSalesMin


# 获取预告净营收上限(海外)时间序列
from windget import getProfitNoticeNetSalesMaxSeries


# 获取预告净营收上限(海外)
from windget import getProfitNoticeNetSalesMax


# 获取单季度.预告净营收上限(海外)时间序列
from windget import getQProfitNoticeNetSalesMaxSeries


# 获取单季度.预告净营收上限(海外)
from windget import getQProfitNoticeNetSalesMax


# 获取预告净营收下限(海外)时间序列
from windget import getProfitNoticeNetSalesMinSeries


# 获取预告净营收下限(海外)
from windget import getProfitNoticeNetSalesMin


# 获取单季度.预告净营收下限(海外)时间序列
from windget import getQProfitNoticeNetSalesMinSeries


# 获取单季度.预告净营收下限(海外)
from windget import getQProfitNoticeNetSalesMin


# 获取预告净营收同比增长上限(海外)时间序列
from windget import getProfitNoticeNetSalesYoYMaxSeries


# 获取预告净营收同比增长上限(海外)
from windget import getProfitNoticeNetSalesYoYMax


# 获取单季度.预告净营收同比增长上限(海外)时间序列
from windget import getQProfitNoticeNetSalesYoYMaxSeries


# 获取单季度.预告净营收同比增长上限(海外)
from windget import getQProfitNoticeNetSalesYoYMax


# 获取预告净营收同比增长下限(海外)时间序列
from windget import getProfitNoticeNetSalesYoYMinSeries


# 获取预告净营收同比增长下限(海外)
from windget import getProfitNoticeNetSalesYoYMin


# 获取单季度.预告净营收同比增长下限(海外)时间序列
from windget import getQProfitNoticeNetSalesYoYMinSeries


# 获取单季度.预告净营收同比增长下限(海外)
from windget import getQProfitNoticeNetSalesYoYMin


# 获取预告总营收上限(海外)时间序列
from windget import getProfitNoticeSalesMaxSeries


# 获取预告总营收上限(海外)
from windget import getProfitNoticeSalesMax


# 获取单季度.预告总营收上限(海外)时间序列
from windget import getQProfitNoticeSalesMaxSeries


# 获取单季度.预告总营收上限(海外)
from windget import getQProfitNoticeSalesMax


# 获取预告总营收下限(海外)时间序列
from windget import getProfitNoticeSalesMinSeries


# 获取预告总营收下限(海外)
from windget import getProfitNoticeSalesMin


# 获取单季度.预告总营收下限(海外)时间序列
from windget import getQProfitNoticeSalesMinSeries


# 获取单季度.预告总营收下限(海外)
from windget import getQProfitNoticeSalesMin


# 获取预告总营收同比增长上限(海外)时间序列
from windget import getProfitNoticeSalesYoYMaxSeries


# 获取预告总营收同比增长上限(海外)
from windget import getProfitNoticeSalesYoYMax


# 获取单季度.预告总营收同比增长上限(海外)时间序列
from windget import getQProfitNoticeSalesYoYMaxSeries


# 获取单季度.预告总营收同比增长上限(海外)
from windget import getQProfitNoticeSalesYoYMax


# 获取预告总营收同比增长下限(海外)时间序列
from windget import getProfitNoticeSalesYoYMinSeries


# 获取预告总营收同比增长下限(海外)
from windget import getProfitNoticeSalesYoYMin


# 获取单季度.预告总营收同比增长下限(海外)时间序列
from windget import getQProfitNoticeSalesYoYMinSeries


# 获取单季度.预告总营收同比增长下限(海外)
from windget import getQProfitNoticeSalesYoYMin


# 获取现金流量利息保障倍数时间序列
from windget import getOCFToInterestSeries


# 获取现金流量利息保障倍数
from windget import getOCFToInterest


# 获取每股现金流量净额(TTM)_PIT时间序列
from windget import getFaCfpSTtMSeries


# 获取每股现金流量净额(TTM)_PIT
from windget import getFaCfpSTtM


# 获取每股现金流量净额时间序列
from windget import getCfpSSeries


# 获取每股现金流量净额
from windget import getCfpS


# 获取每股现金流量净额_GSD时间序列
from windget import getWgsDCfpSSeries


# 获取每股现金流量净额_GSD
from windget import getWgsDCfpS


# 获取其他现金流量调整_GSD时间序列
from windget import getWgsDCashBalChgCfSeries


# 获取其他现金流量调整_GSD
from windget import getWgsDCashBalChgCf


# 获取企业自由现金流量FCFF时间序列
from windget import getFcFfSeries


# 获取企业自由现金流量FCFF
from windget import getFcFf


# 获取股权自由现金流量FCFE时间序列
from windget import getFcFeSeries


# 获取股权自由现金流量FCFE
from windget import getFcFe


# 获取股权自由现金流量FCFE_GSD时间序列
from windget import getWgsDFcFe2Series


# 获取股权自由现金流量FCFE_GSD
from windget import getWgsDFcFe2


# 获取企业自由现金流量_GSD时间序列
from windget import getWgsDFcFf2Series


# 获取企业自由现金流量_GSD
from windget import getWgsDFcFf2


# 获取企业自由现金流量_PIT时间序列
from windget import getFaFcFfSeries


# 获取企业自由现金流量_PIT
from windget import getFaFcFf


# 获取股权自由现金流量_PIT时间序列
from windget import getFaFcFeSeries


# 获取股权自由现金流量_PIT
from windget import getFaFcFe


# 获取增长率-净现金流量(TTM)_PIT时间序列
from windget import getFaNcGrTtMSeries


# 获取增长率-净现金流量(TTM)_PIT
from windget import getFaNcGrTtM


# 获取每股企业自由现金流量时间序列
from windget import getFcFFpsSeries


# 获取每股企业自由现金流量
from windget import getFcFFps


# 获取每股股东自由现金流量时间序列
from windget import getFcFEpsSeries


# 获取每股股东自由现金流量
from windget import getFcFEps


# 获取每股企业自由现金流量_GSD时间序列
from windget import getWgsDFcFFps2Series


# 获取每股企业自由现金流量_GSD
from windget import getWgsDFcFFps2


# 获取每股股东自由现金流量_GSD时间序列
from windget import getWgsDFcFEps2Series


# 获取每股股东自由现金流量_GSD
from windget import getWgsDFcFEps2


# 获取单季度.其他现金流量调整_GSD时间序列
from windget import getWgsDQfaCashBalChgCfSeries


# 获取单季度.其他现金流量调整_GSD
from windget import getWgsDQfaCashBalChgCf


# 获取每股企业自由现金流量_PIT时间序列
from windget import getFaFcFFpsSeries


# 获取每股企业自由现金流量_PIT
from windget import getFaFcFFps


# 获取每股股东自由现金流量_PIT时间序列
from windget import getFaFcFEpsSeries


# 获取每股股东自由现金流量_PIT
from windget import getFaFcFEps


# 获取经营活动产生现金流量净额/带息债务(TTM)_PIT时间序列
from windget import getFaOCFToInterestDebtTtMSeries


# 获取经营活动产生现金流量净额/带息债务(TTM)_PIT
from windget import getFaOCFToInterestDebtTtM


# 获取经营活动产生现金流量净额/净债务(TTM)_PIT时间序列
from windget import getFaOCFToNetDebtTtMSeries


# 获取经营活动产生现金流量净额/净债务(TTM)_PIT
from windget import getFaOCFToNetDebtTtM


# 获取经营活动产生的现金流量净额/营业收入时间序列
from windget import getOCFToOrSeries


# 获取经营活动产生的现金流量净额/营业收入
from windget import getOCFToOr


# 获取经营活动产生的现金流量净额/经营活动净收益时间序列
from windget import getOCFToOperateIncomeSeries


# 获取经营活动产生的现金流量净额/经营活动净收益
from windget import getOCFToOperateIncome


# 获取经营活动产生的现金流量净额占比时间序列
from windget import getOCFTOCFSeries


# 获取经营活动产生的现金流量净额占比
from windget import getOCFTOCF


# 获取投资活动产生的现金流量净额占比时间序列
from windget import getICfTOCFSeries


# 获取投资活动产生的现金流量净额占比
from windget import getICfTOCF


# 获取筹资活动产生的现金流量净额占比时间序列
from windget import getFcFTOCFSeries


# 获取筹资活动产生的现金流量净额占比
from windget import getFcFTOCF


# 获取经营活动产生的现金流量净额/负债合计时间序列
from windget import getOCFToDebtSeries


# 获取经营活动产生的现金流量净额/负债合计
from windget import getOCFToDebt


# 获取经营活动产生的现金流量净额/带息债务时间序列
from windget import getOCFToInterestDebtSeries


# 获取经营活动产生的现金流量净额/带息债务
from windget import getOCFToInterestDebt


# 获取经营活动产生的现金流量净额/流动负债时间序列
from windget import getOCFToShortDebtSeries


# 获取经营活动产生的现金流量净额/流动负债
from windget import getOCFToShortDebt


# 获取经营活动产生的现金流量净额/非流动负债时间序列
from windget import getOCFToLongDebtSeries


# 获取经营活动产生的现金流量净额/非流动负债
from windget import getOCFToLongDebt


# 获取经营活动产生的现金流量净额/净债务时间序列
from windget import getOCFToNetDebtSeries


# 获取经营活动产生的现金流量净额/净债务
from windget import getOCFToNetDebt


# 获取经营活动产生的现金流量净额(同比增长率)时间序列
from windget import getYoyOCFSeries


# 获取经营活动产生的现金流量净额(同比增长率)
from windget import getYoyOCF


# 获取经营活动产生的现金流量净额(N年,增长率)时间序列
from windget import getGrowthOCFSeries


# 获取经营活动产生的现金流量净额(N年,增长率)
from windget import getGrowthOCF


# 获取经营活动产生的现金流量净额/营业收入(TTM)时间序列
from windget import getOCFToOrTtM2Series


# 获取经营活动产生的现金流量净额/营业收入(TTM)
from windget import getOCFToOrTtM2


# 获取经营活动产生的现金流量净额/经营活动净收益(TTM)时间序列
from windget import getOCFToOperateIncomeTtM2Series


# 获取经营活动产生的现金流量净额/经营活动净收益(TTM)
from windget import getOCFToOperateIncomeTtM2


# 获取经营活动产生的现金流量净额/营业利润(TTM)时间序列
from windget import getOperateCashFlowToOpTtMSeries


# 获取经营活动产生的现金流量净额/营业利润(TTM)
from windget import getOperateCashFlowToOpTtM


# 获取经营活动产生的现金流量净额/营业收入_GSD时间序列
from windget import getWgsDOCFToSalesSeries


# 获取经营活动产生的现金流量净额/营业收入_GSD
from windget import getWgsDOCFToSales


# 获取经营活动产生的现金流量净额/经营活动净收益_GSD时间序列
from windget import getWgsDOCFToOperateIncomeSeries


# 获取经营活动产生的现金流量净额/经营活动净收益_GSD
from windget import getWgsDOCFToOperateIncome


# 获取经营活动产生的现金流量净额/流动负债_GSD时间序列
from windget import getWgsDOCFToLiqDebtSeries


# 获取经营活动产生的现金流量净额/流动负债_GSD
from windget import getWgsDOCFToLiqDebt


# 获取经营活动产生的现金流量净额/负债合计_GSD时间序列
from windget import getWgsDOCFToDebtSeries


# 获取经营活动产生的现金流量净额/负债合计_GSD
from windget import getWgsDOCFToDebt


# 获取经营活动产生的现金流量净额/带息债务_GSD时间序列
from windget import getWgsDOCFToInterestDebtSeries


# 获取经营活动产生的现金流量净额/带息债务_GSD
from windget import getWgsDOCFToInterestDebt


# 获取经营活动产生的现金流量净额/净债务_GSD时间序列
from windget import getWgsDOCFToNetDebtSeries


# 获取经营活动产生的现金流量净额/净债务_GSD
from windget import getWgsDOCFToNetDebt


# 获取经营活动产生的现金流量净额(同比增长率)_GSD时间序列
from windget import getWgsDYoyOCFSeries


# 获取经营活动产生的现金流量净额(同比增长率)_GSD
from windget import getWgsDYoyOCF


# 获取经营活动产生的现金流量净额(N年,增长率)_GSD时间序列
from windget import getWgsDGrowthOCFSeries


# 获取经营活动产生的现金流量净额(N年,增长率)_GSD
from windget import getWgsDGrowthOCF


# 获取经营活动产生的现金流量净额/经营活动净收益(TTM)_GSD时间序列
from windget import getOCFToOperateIncomeTtM3Series


# 获取经营活动产生的现金流量净额/经营活动净收益(TTM)_GSD
from windget import getOCFToOperateIncomeTtM3


# 获取经营活动产生的现金流量净额/营业利润(TTM)_GSD时间序列
from windget import getOperateCashFlowToOpTtM2Series


# 获取经营活动产生的现金流量净额/营业利润(TTM)_GSD
from windget import getOperateCashFlowToOpTtM2


# 获取经营活动产生的现金流量净额/营业收入(TTM)_GSD时间序列
from windget import getOCFToSalesTtM2Series


# 获取经营活动产生的现金流量净额/营业收入(TTM)_GSD
from windget import getOCFToSalesTtM2


# 获取经营活动产生的现金流量净额_GSD时间序列
from windget import getWgsDOperCfSeries


# 获取经营活动产生的现金流量净额_GSD
from windget import getWgsDOperCf


# 获取投资活动产生的现金流量净额_GSD时间序列
from windget import getWgsDInvestCfSeries


# 获取投资活动产生的现金流量净额_GSD
from windget import getWgsDInvestCf


# 获取筹资活动产生的现金流量净额_GSD时间序列
from windget import getWgsDFinCfSeries


# 获取筹资活动产生的现金流量净额_GSD
from windget import getWgsDFinCf


# 获取经营活动产生的现金流量净额差额(合计平衡项目)时间序列
from windget import getCfOperActNettingSeries


# 获取经营活动产生的现金流量净额差额(合计平衡项目)
from windget import getCfOperActNetting


# 获取经营活动产生的现金流量净额时间序列
from windget import getStm07CsReItsOperNetCashSeries


# 获取经营活动产生的现金流量净额
from windget import getStm07CsReItsOperNetCash


# 获取投资活动产生的现金流量净额差额(合计平衡项目)时间序列
from windget import getCfInvActNettingSeries


# 获取投资活动产生的现金流量净额差额(合计平衡项目)
from windget import getCfInvActNetting


# 获取投资活动产生的现金流量净额时间序列
from windget import getStm07CsReItsInvestNetCashSeries


# 获取投资活动产生的现金流量净额
from windget import getStm07CsReItsInvestNetCash


# 获取筹资活动产生的现金流量净额差额(合计平衡项目)时间序列
from windget import getCfFncActNettingSeries


# 获取筹资活动产生的现金流量净额差额(合计平衡项目)
from windget import getCfFncActNetting


# 获取筹资活动产生的现金流量净额时间序列
from windget import getStm07CsReItsFinanceNetCashSeries


# 获取筹资活动产生的现金流量净额
from windget import getStm07CsReItsFinanceNetCash


# 获取经营活动产生的现金流量净额/营业收入_PIT时间序列
from windget import getFaOCFToOrSeries


# 获取经营活动产生的现金流量净额/营业收入_PIT
from windget import getFaOCFToOr


# 获取经营活动产生的现金流量净额/营业收入(TTM)_PIT时间序列
from windget import getFaOCFToOrTtMSeries


# 获取经营活动产生的现金流量净额/营业收入(TTM)_PIT
from windget import getFaOCFToOrTtM


# 获取经营活动产生的现金流量净额/经营活动净收益(TTM)_PIT时间序列
from windget import getFaOCFTooAITtMSeries


# 获取经营活动产生的现金流量净额/经营活动净收益(TTM)_PIT
from windget import getFaOCFTooAITtM


# 获取经营活动产生的现金流量净额/营业利润(TTM)_PIT时间序列
from windget import getFaOCFToOpTtMSeries


# 获取经营活动产生的现金流量净额/营业利润(TTM)_PIT
from windget import getFaOCFToOpTtM


# 获取经营活动产生的现金流量净额/负债合计_PIT时间序列
from windget import getFaOCFToDebtSeries


# 获取经营活动产生的现金流量净额/负债合计_PIT
from windget import getFaOCFToDebt


# 获取经营活动产生的现金流量净额/营业收入(TTM,只有最新数据)时间序列
from windget import getOCFToOrTtMSeries


# 获取经营活动产生的现金流量净额/营业收入(TTM,只有最新数据)
from windget import getOCFToOrTtM


# 获取经营活动产生的现金流量净额/经营活动净收益(TTM,只有最新数据)时间序列
from windget import getOCFToOperateIncomeTtMSeries


# 获取经营活动产生的现金流量净额/经营活动净收益(TTM,只有最新数据)
from windget import getOCFToOperateIncomeTtM


# 获取间接法-经营活动现金流量净额差额(特殊报表科目)时间序列
from windget import getImNetCashFlowsOperActGapSeries


# 获取间接法-经营活动现金流量净额差额(特殊报表科目)
from windget import getImNetCashFlowsOperActGap


# 获取间接法-经营活动现金流量净额差额说明(特殊报表科目)时间序列
from windget import getImNetCashFlowsOperActGapDetailSeries


# 获取间接法-经营活动现金流量净额差额说明(特殊报表科目)
from windget import getImNetCashFlowsOperActGapDetail


# 获取间接法-经营活动现金流量净额差额(合计平衡项目)时间序列
from windget import getImNetCashFlowsOperActNettingSeries


# 获取间接法-经营活动现金流量净额差额(合计平衡项目)
from windget import getImNetCashFlowsOperActNetting


# 获取每股经营活动产生的现金流量净额(TTM)_PIT时间序列
from windget import getFaOcFpsTtMSeries


# 获取每股经营活动产生的现金流量净额(TTM)_PIT
from windget import getFaOcFpsTtM


# 获取每股经营活动产生的现金流量净额时间序列
from windget import getOcFpsSeries


# 获取每股经营活动产生的现金流量净额
from windget import getOcFps


# 获取每股经营活动产生的现金流量净额(同比增长率)时间序列
from windget import getYoyOCFpSSeries


# 获取每股经营活动产生的现金流量净额(同比增长率)
from windget import getYoyOCFpS


# 获取每股经营活动产生的现金流量净额(同比增长率)_GSD时间序列
from windget import getWgsDYoyOCFpSSeries


# 获取每股经营活动产生的现金流量净额(同比增长率)_GSD
from windget import getWgsDYoyOCFpS


# 获取其他投资活动产生的现金流量净额_GSD时间序列
from windget import getWgsDInvestOThCfSeries


# 获取其他投资活动产生的现金流量净额_GSD
from windget import getWgsDInvestOThCf


# 获取其他筹资活动产生的现金流量净额_GSD时间序列
from windget import getWgsDFinOThCfSeries


# 获取其他筹资活动产生的现金流量净额_GSD
from windget import getWgsDFinOThCf


# 获取单季度.经营活动产生的现金流量净额/营业收入时间序列
from windget import getQfaOCFToSalesSeries


# 获取单季度.经营活动产生的现金流量净额/营业收入
from windget import getQfaOCFToSales


# 获取单季度.经营活动产生的现金流量净额/经营活动净收益时间序列
from windget import getQfaOCFToOrSeries


# 获取单季度.经营活动产生的现金流量净额/经营活动净收益
from windget import getQfaOCFToOr


# 获取单季度.经营活动产生的现金流量净额占比时间序列
from windget import getOCFTOCFQfaSeries


# 获取单季度.经营活动产生的现金流量净额占比
from windget import getOCFTOCFQfa


# 获取单季度.投资活动产生的现金流量净额占比时间序列
from windget import getICfTOCFQfaSeries


# 获取单季度.投资活动产生的现金流量净额占比
from windget import getICfTOCFQfa


# 获取单季度.筹资活动产生的现金流量净额占比时间序列
from windget import getFcFTOCFQfaSeries


# 获取单季度.筹资活动产生的现金流量净额占比
from windget import getFcFTOCFQfa


# 获取单季度.经营活动产生的现金流量净额_GSD时间序列
from windget import getWgsDQfaOperCfSeries


# 获取单季度.经营活动产生的现金流量净额_GSD
from windget import getWgsDQfaOperCf


# 获取单季度.投资活动产生的现金流量净额_GSD时间序列
from windget import getWgsDQfaInvestCfSeries


# 获取单季度.投资活动产生的现金流量净额_GSD
from windget import getWgsDQfaInvestCf


# 获取单季度.筹资活动产生的现金流量净额_GSD时间序列
from windget import getWgsDQfaFinCfSeries


# 获取单季度.筹资活动产生的现金流量净额_GSD
from windget import getWgsDQfaFinCf


# 获取间接法-经营活动产生的现金流量净额时间序列
from windget import getImNetCashFlowsOperActSeries


# 获取间接法-经营活动产生的现金流量净额
from windget import getImNetCashFlowsOperAct


# 获取单季度.经营活动产生的现金流量净额时间序列
from windget import getQfaNetCashFlowsOperActSeries


# 获取单季度.经营活动产生的现金流量净额
from windget import getQfaNetCashFlowsOperAct


# 获取单季度.投资活动产生的现金流量净额时间序列
from windget import getQfaNetCashFlowsInvActSeries


# 获取单季度.投资活动产生的现金流量净额
from windget import getQfaNetCashFlowsInvAct


# 获取单季度.筹资活动产生的现金流量净额时间序列
from windget import getQfaNetCashFlowsFncActSeries


# 获取单季度.筹资活动产生的现金流量净额
from windget import getQfaNetCashFlowsFncAct


# 获取增长率-经营活动产生的现金流量净额(TTM)_PIT时间序列
from windget import getFaCFogRTtMSeries


# 获取增长率-经营活动产生的现金流量净额(TTM)_PIT
from windget import getFaCFogRTtM


# 获取增长率-筹资活动产生的现金流量净额(TTM)_PIT时间序列
from windget import getFaCffGrTtMSeries


# 获取增长率-筹资活动产生的现金流量净额(TTM)_PIT
from windget import getFaCffGrTtM


# 获取增长率-投资活动产生的现金流量净额(TTM)_PIT时间序列
from windget import getFaCFigRTtMSeries


# 获取增长率-投资活动产生的现金流量净额(TTM)_PIT
from windget import getFaCFigRTtM


# 获取单季度.其他投资活动产生的现金流量净额_GSD时间序列
from windget import getWgsDQfaInvestOThCfSeries


# 获取单季度.其他投资活动产生的现金流量净额_GSD
from windget import getWgsDQfaInvestOThCf


# 获取单季度.其他筹资活动产生的现金流量净额_GSD时间序列
from windget import getWgsDQfaFinOThCfSeries


# 获取单季度.其他筹资活动产生的现金流量净额_GSD
from windget import getWgsDQfaFinOThCf


# 获取单季度.间接法-经营活动产生的现金流量净额时间序列
from windget import getQfaImNetCashFlowsOperActSeries


# 获取单季度.间接法-经营活动产生的现金流量净额
from windget import getQfaImNetCashFlowsOperAct


# 获取权益乘数(杜邦分析)时间序列
from windget import getDupontAssetsToEquitySeries


# 获取权益乘数(杜邦分析)
from windget import getDupontAssetsToEquity


# 获取权益乘数(杜邦分析)_GSD时间序列
from windget import getWgsDDupontAssetsToEquitySeries


# 获取权益乘数(杜邦分析)_GSD
from windget import getWgsDDupontAssetsToEquity


# 获取主营构成(按行业)-项目名称时间序列
from windget import getSegmentIndustryItemSeries


# 获取主营构成(按行业)-项目名称
from windget import getSegmentIndustryItem


# 获取主营构成(按行业)-项目收入时间序列
from windget import getSegmentIndustrySales1Series


# 获取主营构成(按行业)-项目收入
from windget import getSegmentIndustrySales1


# 获取主营构成(按行业)-项目成本时间序列
from windget import getSegmentIndustryCost1Series


# 获取主营构成(按行业)-项目成本
from windget import getSegmentIndustryCost1


# 获取主营构成(按行业)-项目毛利时间序列
from windget import getSegmentIndustryProfit1Series


# 获取主营构成(按行业)-项目毛利
from windget import getSegmentIndustryProfit1


# 获取主营构成(按行业)-项目毛利率时间序列
from windget import getSegmentIndustryGpMarginSeries


# 获取主营构成(按行业)-项目毛利率
from windget import getSegmentIndustryGpMargin


# 获取主营构成(按产品)-项目名称时间序列
from windget import getSegmentProductItemSeries


# 获取主营构成(按产品)-项目名称
from windget import getSegmentProductItem


# 获取主营构成(按产品)-项目收入时间序列
from windget import getSegmentProductSales1Series


# 获取主营构成(按产品)-项目收入
from windget import getSegmentProductSales1


# 获取主营构成(按产品)-项目成本时间序列
from windget import getSegmentProductCost1Series


# 获取主营构成(按产品)-项目成本
from windget import getSegmentProductCost1


# 获取主营构成(按产品)-项目毛利时间序列
from windget import getSegmentProductProfit1Series


# 获取主营构成(按产品)-项目毛利
from windget import getSegmentProductProfit1


# 获取主营构成(按产品)-项目毛利率时间序列
from windget import getSegmentProductGpMarginSeries


# 获取主营构成(按产品)-项目毛利率
from windget import getSegmentProductGpMargin


# 获取主营构成(按地区)-项目名称时间序列
from windget import getSegmentRegionItemSeries


# 获取主营构成(按地区)-项目名称
from windget import getSegmentRegionItem


# 获取主营构成(按地区)-项目收入时间序列
from windget import getSegmentRegionSales1Series


# 获取主营构成(按地区)-项目收入
from windget import getSegmentRegionSales1


# 获取主营构成(按地区)-项目成本时间序列
from windget import getSegmentRegionCost1Series


# 获取主营构成(按地区)-项目成本
from windget import getSegmentRegionCost1


# 获取主营构成(按地区)-项目毛利时间序列
from windget import getSegmentRegionProfit1Series


# 获取主营构成(按地区)-项目毛利
from windget import getSegmentRegionProfit1


# 获取主营构成(按地区)-项目毛利率时间序列
from windget import getSegmentRegionGpMarginSeries


# 获取主营构成(按地区)-项目毛利率
from windget import getSegmentRegionGpMargin


# 获取主营构成(按行业)-项目收入(旧)时间序列
from windget import getSegmentIndustrySalesSeries


# 获取主营构成(按行业)-项目收入(旧)
from windget import getSegmentIndustrySales


# 获取主营构成(按行业)-项目成本(旧)时间序列
from windget import getSegmentIndustryCostSeries


# 获取主营构成(按行业)-项目成本(旧)
from windget import getSegmentIndustryCost


# 获取主营构成(按行业)-项目毛利(旧)时间序列
from windget import getSegmentIndustryProfitSeries


# 获取主营构成(按行业)-项目毛利(旧)
from windget import getSegmentIndustryProfit


# 获取主营构成(按产品)-项目收入(旧)时间序列
from windget import getSegmentProductSalesSeries


# 获取主营构成(按产品)-项目收入(旧)
from windget import getSegmentProductSales


# 获取主营构成(按产品)-项目成本(旧)时间序列
from windget import getSegmentProductCostSeries


# 获取主营构成(按产品)-项目成本(旧)
from windget import getSegmentProductCost


# 获取主营构成(按产品)-项目毛利(旧)时间序列
from windget import getSegmentProductProfitSeries


# 获取主营构成(按产品)-项目毛利(旧)
from windget import getSegmentProductProfit


# 获取主营构成(按地区)-项目收入(旧)时间序列
from windget import getSegmentRegionSalesSeries


# 获取主营构成(按地区)-项目收入(旧)
from windget import getSegmentRegionSales


# 获取主营构成(按地区)-项目成本(旧)时间序列
from windget import getSegmentRegionCostSeries


# 获取主营构成(按地区)-项目成本(旧)
from windget import getSegmentRegionCost


# 获取主营构成(按地区)-项目毛利(旧)时间序列
from windget import getSegmentRegionProfitSeries


# 获取主营构成(按地区)-项目毛利(旧)
from windget import getSegmentRegionProfit


# 获取审计意见类别时间序列
from windget import getStmNoteAuditCategorySeries


# 获取审计意见类别
from windget import getStmNoteAuditCategory


# 获取内控_审计意见类别时间序列
from windget import getStmNoteInAuditCategorySeries


# 获取内控_审计意见类别
from windget import getStmNoteInAuditCategory


# 获取资产减值准备时间序列
from windget import getProvDePrAssetsSeries


# 获取资产减值准备
from windget import getProvDePrAssets


# 获取资产减值准备(非经常性损益)时间序列
from windget import getStmNoteEoItems13Series


# 获取资产减值准备(非经常性损益)
from windget import getStmNoteEoItems13


# 获取固定资产减值准备合计时间序列
from windget import getStmNoteReserve21Series


# 获取固定资产减值准备合计
from windget import getStmNoteReserve21


# 获取固定资产减值准备-房屋、建筑物时间序列
from windget import getStmNoteReserve22Series


# 获取固定资产减值准备-房屋、建筑物
from windget import getStmNoteReserve22


# 获取固定资产减值准备-机器设备时间序列
from windget import getStmNoteReserve23Series


# 获取固定资产减值准备-机器设备
from windget import getStmNoteReserve23


# 获取固定资产减值准备-专用设备时间序列
from windget import getStmNoteReserve24Series


# 获取固定资产减值准备-专用设备
from windget import getStmNoteReserve24


# 获取固定资产减值准备-运输工具时间序列
from windget import getStmNoteReserve25Series


# 获取固定资产减值准备-运输工具
from windget import getStmNoteReserve25


# 获取固定资产减值准备-通讯设备时间序列
from windget import getStmNoteReserve26Series


# 获取固定资产减值准备-通讯设备
from windget import getStmNoteReserve26


# 获取固定资产减值准备-电子设备时间序列
from windget import getStmNoteReserve27Series


# 获取固定资产减值准备-电子设备
from windget import getStmNoteReserve27


# 获取固定资产减值准备-办公及其它设备时间序列
from windget import getStmNoteReserve28Series


# 获取固定资产减值准备-办公及其它设备
from windget import getStmNoteReserve28


# 获取固定资产减值准备-其它设备时间序列
from windget import getStmNoteReserve29Series


# 获取固定资产减值准备-其它设备
from windget import getStmNoteReserve29


# 获取无形资产减值准备时间序列
from windget import getStmNoteReserve30Series


# 获取无形资产减值准备
from windget import getStmNoteReserve30


# 获取无形资产减值准备-专利权时间序列
from windget import getStmNoteReserve31Series


# 获取无形资产减值准备-专利权
from windget import getStmNoteReserve31


# 获取无形资产减值准备-商标权时间序列
from windget import getStmNoteReserve32Series


# 获取无形资产减值准备-商标权
from windget import getStmNoteReserve32


# 获取无形资产减值准备-职工住房使用权时间序列
from windget import getStmNoteReserve33Series


# 获取无形资产减值准备-职工住房使用权
from windget import getStmNoteReserve33


# 获取无形资产减值准备-土地使用权时间序列
from windget import getStmNoteReserve34Series


# 获取无形资产减值准备-土地使用权
from windget import getStmNoteReserve34


# 获取计提投资资产减值准备时间序列
from windget import getStmNoteInvestmentIncome0007Series


# 获取计提投资资产减值准备
from windget import getStmNoteInvestmentIncome0007


# 获取单季度.资产减值准备时间序列
from windget import getQfaProvDePrAssetsSeries


# 获取单季度.资产减值准备
from windget import getQfaProvDePrAssets


# 获取土地使用权_GSD时间序列
from windget import getWgsDLandUseRightsSeries


# 获取土地使用权_GSD
from windget import getWgsDLandUseRights


# 获取土地使用权_原值时间序列
from windget import getStmNoteLandUseRights19Series


# 获取土地使用权_原值
from windget import getStmNoteLandUseRights19


# 获取土地使用权_累计摊销时间序列
from windget import getStmNoteLandUseRights20Series


# 获取土地使用权_累计摊销
from windget import getStmNoteLandUseRights20


# 获取土地使用权_减值准备时间序列
from windget import getStmNoteLandUseRights21Series


# 获取土地使用权_减值准备
from windget import getStmNoteLandUseRights21


# 获取土地使用权_账面价值时间序列
from windget import getStmNoteLandUseRights22Series


# 获取土地使用权_账面价值
from windget import getStmNoteLandUseRights22


# 获取买入返售金融资产时间序列
from windget import getPrtReverseRepoSeries


# 获取买入返售金融资产
from windget import getPrtReverseRepo


# 获取买入返售金融资产:证券时间序列
from windget import getStmNoteSPuAr0001Series


# 获取买入返售金融资产:证券
from windget import getStmNoteSPuAr0001


# 获取买入返售金融资产:票据时间序列
from windget import getStmNoteSPuAr0002Series


# 获取买入返售金融资产:票据
from windget import getStmNoteSPuAr0002


# 获取买入返售金融资产:贷款时间序列
from windget import getStmNoteSPuAr0003Series


# 获取买入返售金融资产:贷款
from windget import getStmNoteSPuAr0003


# 获取买入返售金融资产:信托及其他受益权时间序列
from windget import getStmNoteSPuAr0004Series


# 获取买入返售金融资产:信托及其他受益权
from windget import getStmNoteSPuAr0004


# 获取买入返售金融资产:长期应收款时间序列
from windget import getStmNoteSPuAr0005Series


# 获取买入返售金融资产:长期应收款
from windget import getStmNoteSPuAr0005


# 获取买入返售金融资产:其他担保物时间序列
from windget import getStmNoteSPuAr0006Series


# 获取买入返售金融资产:其他担保物
from windget import getStmNoteSPuAr0006


# 获取买入返售金融资产:减值准备时间序列
from windget import getStmNoteSPuAr0007Series


# 获取买入返售金融资产:减值准备
from windget import getStmNoteSPuAr0007


# 获取买入返售金融资产:股票质押式回购时间序列
from windget import getStmNoteSPuAr10001Series


# 获取买入返售金融资产:股票质押式回购
from windget import getStmNoteSPuAr10001


# 获取买入返售金融资产:约定购回式证券时间序列
from windget import getStmNoteSPuAr10002Series


# 获取买入返售金融资产:约定购回式证券
from windget import getStmNoteSPuAr10002


# 获取买入返售金融资产:债券买断式回购时间序列
from windget import getStmNoteSPuAr10003Series


# 获取买入返售金融资产:债券买断式回购
from windget import getStmNoteSPuAr10003


# 获取买入返售金融资产:债券质押式回购时间序列
from windget import getStmNoteSPuAr10004Series


# 获取买入返售金融资产:债券质押式回购
from windget import getStmNoteSPuAr10004


# 获取买入返售金融资产:债券回购时间序列
from windget import getStmNoteSPuAr10007Series


# 获取买入返售金融资产:债券回购
from windget import getStmNoteSPuAr10007


# 获取买入返售金融资产:其他时间序列
from windget import getStmNoteSPuAr10005Series


# 获取买入返售金融资产:其他
from windget import getStmNoteSPuAr10005


# 获取买入返售金融资产合计时间序列
from windget import getStmNoteSPuAr10006Series


# 获取买入返售金融资产合计
from windget import getStmNoteSPuAr10006


# 获取买入返售金融资产_FUND时间序列
from windget import getStmBs17Series


# 获取买入返售金融资产_FUND
from windget import getStmBs17


# 获取买入返售金融资产(交易所市场)_FUND时间序列
from windget import getStmBsRepoInExChMktSeries


# 获取买入返售金融资产(交易所市场)_FUND
from windget import getStmBsRepoInExChMkt


# 获取买入返售金融资产(银行间市场)_FUND时间序列
from windget import getStmBsRepoInInterBmkTSeries


# 获取买入返售金融资产(银行间市场)_FUND
from windget import getStmBsRepoInInterBmkT


# 获取买入返售金融资产收入_FUND时间序列
from windget import getStmIs3Series


# 获取买入返售金融资产收入_FUND
from windget import getStmIs3


# 获取可供出售金融资产时间序列
from windget import getFinAssetsAvailForSaleSeries


# 获取可供出售金融资产
from windget import getFinAssetsAvailForSale


# 获取可供出售金融资产:产生的利得/(损失)时间序列
from windget import getStmNoteFaaViableForSale0001Series


# 获取可供出售金融资产:产生的利得/(损失)
from windget import getStmNoteFaaViableForSale0001


# 获取可供出售金融资产:产生的所得税影响时间序列
from windget import getStmNoteFaaViableForSale0002Series


# 获取可供出售金融资产:产生的所得税影响
from windget import getStmNoteFaaViableForSale0002


# 获取可供出售金融资产:前期计入其他综合收益当期转入损益的金额时间序列
from windget import getStmNoteFaaViableForSale0003Series


# 获取可供出售金融资产:前期计入其他综合收益当期转入损益的金额
from windget import getStmNoteFaaViableForSale0003


# 获取可供出售金融资产公允价值变动时间序列
from windget import getStmNoteFaaViableForSale0004Series


# 获取可供出售金融资产公允价值变动
from windget import getStmNoteFaaViableForSale0004


# 获取可供出售金融资产减值损失时间序列
from windget import getStmNoteImpairmentLoss8Series


# 获取可供出售金融资产减值损失
from windget import getStmNoteImpairmentLoss8


# 获取处置可供出售金融资产净增加额时间序列
from windget import getNetInCrDispFinAssetsAvailSeries


# 获取处置可供出售金融资产净增加额
from windget import getNetInCrDispFinAssetsAvail


# 获取融出证券:可供出售金融资产时间序列
from windget import getStmNoteSecuritiesLending3Series


# 获取融出证券:可供出售金融资产
from windget import getStmNoteSecuritiesLending3


# 获取单季度.处置可供出售金融资产净增加额时间序列
from windget import getQfaNetInCrDispFinAssetsAvailSeries


# 获取单季度.处置可供出售金融资产净增加额
from windget import getQfaNetInCrDispFinAssetsAvail


# 获取融出证券合计时间序列
from windget import getStmNoteSecuritiesLending1Series


# 获取融出证券合计
from windget import getStmNoteSecuritiesLending1


# 获取融出证券:交易性金融资产时间序列
from windget import getStmNoteSecuritiesLending2Series


# 获取融出证券:交易性金融资产
from windget import getStmNoteSecuritiesLending2


# 获取融出证券:转融通融入证券时间序列
from windget import getStmNoteSecuritiesLending4Series


# 获取融出证券:转融通融入证券
from windget import getStmNoteSecuritiesLending4


# 获取融出证券:转融通融入证券余额时间序列
from windget import getStmNoteSecuritiesLending5Series


# 获取融出证券:转融通融入证券余额
from windget import getStmNoteSecuritiesLending5


# 获取融出证券:减值准备时间序列
from windget import getStmNoteSecuritiesLending6Series


# 获取融出证券:减值准备
from windget import getStmNoteSecuritiesLending6


# 获取现金及存放中央银行款项时间序列
from windget import getCashDepositsCentralBankSeries


# 获取现金及存放中央银行款项
from windget import getCashDepositsCentralBank


# 获取银行存款_FUND时间序列
from windget import getStmBs1Series


# 获取银行存款_FUND
from windget import getStmBs1


# 获取银行存款时间序列
from windget import getPrtCashSeries


# 获取银行存款
from windget import getPrtCash


# 获取银行存款占基金资产净值比时间序列
from windget import getPrtCashToNavSeries


# 获取银行存款占基金资产净值比
from windget import getPrtCashToNav


# 获取银行存款占基金资产总值比时间序列
from windget import getPrtCashToAssetSeries


# 获取银行存款占基金资产总值比
from windget import getPrtCashToAsset


# 获取银行存款市值增长率时间序列
from windget import getPrtCashValueGrowthSeries


# 获取银行存款市值增长率
from windget import getPrtCashValueGrowth


# 获取银行存款市值占基金资产净值比例增长时间序列
from windget import getPrtCashToNavGrowthSeries


# 获取银行存款市值占基金资产净值比例增长
from windget import getPrtCashToNavGrowth


# 获取货币资金-银行存款时间序列
from windget import getStmNoteBankDepositSeries


# 获取货币资金-银行存款
from windget import getStmNoteBankDeposit


# 获取货币资金/短期债务时间序列
from windget import getCashToStDebtSeries


# 获取货币资金/短期债务
from windget import getCashToStDebt


# 获取货币资金增长率时间序列
from windget import getYoYCashSeries


# 获取货币资金增长率
from windget import getYoYCash


# 获取货币资金/流动负债_GSD时间序列
from windget import getWgsDCashToLiqDebtSeries


# 获取货币资金/流动负债_GSD
from windget import getWgsDCashToLiqDebt


# 获取货币资金时间序列
from windget import getStm07BsReItsCashSeries


# 获取货币资金
from windget import getStm07BsReItsCash


# 获取货币资金合计时间序列
from windget import getStmNoteDpsT4412Series


# 获取货币资金合计
from windget import getStmNoteDpsT4412


# 获取货币资金-库存现金时间序列
from windget import getStmNoteCashInvaultSeries


# 获取货币资金-库存现金
from windget import getStmNoteCashInvault


# 获取借款合计时间序列
from windget import getStmNoteBorrow4512Series


# 获取借款合计
from windget import getStmNoteBorrow4512


# 获取短期借款时间序列
from windget import getStBorrowSeries


# 获取短期借款
from windget import getStBorrow


# 获取长期借款时间序列
from windget import getLtBorrowSeries


# 获取长期借款
from windget import getLtBorrow


# 获取质押借款时间序列
from windget import getPledgeLoanSeries


# 获取质押借款
from windget import getPledgeLoan


# 获取取得借款收到的现金时间序列
from windget import getCashRecpBorrowSeries


# 获取取得借款收到的现金
from windget import getCashRecpBorrow


# 获取短期借款小计时间序列
from windget import getStmNoteStBorrow4512Series


# 获取短期借款小计
from windget import getStmNoteStBorrow4512


# 获取长期借款小计时间序列
from windget import getStmNoteLtBorrow4512Series


# 获取长期借款小计
from windget import getStmNoteLtBorrow4512


# 获取短期借款_FUND时间序列
from windget import getStmBs70Series


# 获取短期借款_FUND
from windget import getStmBs70


# 获取长期借款/资产总计_PIT时间序列
from windget import getFaLtBorrowToAssetSeries


# 获取长期借款/资产总计_PIT
from windget import getFaLtBorrowToAsset


# 获取国际商业借款比率时间序列
from windget import getBusLoanRatioNSeries


# 获取国际商业借款比率
from windget import getBusLoanRatioN


# 获取国际商业借款比率(旧)时间序列
from windget import getBusLoanRatioSeries


# 获取国际商业借款比率(旧)
from windget import getBusLoanRatio


# 获取美元短期借款(折算人民币)时间序列
from windget import getStmNoteStBorrow4506Series


# 获取美元短期借款(折算人民币)
from windget import getStmNoteStBorrow4506


# 获取日元短期借款(折算人民币)时间序列
from windget import getStmNoteStBorrow4507Series


# 获取日元短期借款(折算人民币)
from windget import getStmNoteStBorrow4507


# 获取欧元短期借款(折算人民币)时间序列
from windget import getStmNoteStBorrow4508Series


# 获取欧元短期借款(折算人民币)
from windget import getStmNoteStBorrow4508


# 获取港币短期借款(折算人民币)时间序列
from windget import getStmNoteStBorrow4509Series


# 获取港币短期借款(折算人民币)
from windget import getStmNoteStBorrow4509


# 获取英镑短期借款(折算人民币)时间序列
from windget import getStmNoteStBorrow4510Series


# 获取英镑短期借款(折算人民币)
from windget import getStmNoteStBorrow4510


# 获取美元长期借款(折算人民币)时间序列
from windget import getStmNoteLtBorrow4506Series


# 获取美元长期借款(折算人民币)
from windget import getStmNoteLtBorrow4506


# 获取日元长期借款(折算人民币)时间序列
from windget import getStmNoteLtBorrow4507Series


# 获取日元长期借款(折算人民币)
from windget import getStmNoteLtBorrow4507


# 获取欧元长期借款(折算人民币)时间序列
from windget import getStmNoteLtBorrow4508Series


# 获取欧元长期借款(折算人民币)
from windget import getStmNoteLtBorrow4508


# 获取港币长期借款(折算人民币)时间序列
from windget import getStmNoteLtBorrow4509Series


# 获取港币长期借款(折算人民币)
from windget import getStmNoteLtBorrow4509


# 获取英镑长期借款(折算人民币)时间序列
from windget import getStmNoteLtBorrow4510Series


# 获取英镑长期借款(折算人民币)
from windget import getStmNoteLtBorrow4510


# 获取向中央银行借款时间序列
from windget import getBorrowCentralBankSeries


# 获取向中央银行借款
from windget import getBorrowCentralBank


# 获取向中央银行借款净增加额时间序列
from windget import getNetInCrLoansCentralBankSeries


# 获取向中央银行借款净增加额
from windget import getNetInCrLoansCentralBank


# 获取人民币短期借款时间序列
from windget import getStmNoteStBorrow4505Series


# 获取人民币短期借款
from windget import getStmNoteStBorrow4505


# 获取人民币长期借款时间序列
from windget import getStmNoteLtBorrow4505Series


# 获取人民币长期借款
from windget import getStmNoteLtBorrow4505


# 获取单季度.取得借款收到的现金时间序列
from windget import getQfaCashRecpBorrowSeries


# 获取单季度.取得借款收到的现金
from windget import getQfaCashRecpBorrow


# 获取其他货币短期借款(折算人民币)时间序列
from windget import getStmNoteStBorrow4511Series


# 获取其他货币短期借款(折算人民币)
from windget import getStmNoteStBorrow4511


# 获取其他货币长期借款(折算人民币)时间序列
from windget import getStmNoteLtBorrow4511Series


# 获取其他货币长期借款(折算人民币)
from windget import getStmNoteLtBorrow4511


# 获取一年内到期的长期借款时间序列
from windget import getStmNoteOthers7636Series


# 获取一年内到期的长期借款
from windget import getStmNoteOthers7636


# 获取单季度.向中央银行借款净增加额时间序列
from windget import getQfaNetInCrLoansCentralBankSeries


# 获取单季度.向中央银行借款净增加额
from windget import getQfaNetInCrLoansCentralBank


# 获取非经常性损益时间序列
from windget import getExtraordinarySeries


# 获取非经常性损益
from windget import getExtraordinary


# 获取非经常性损益项目小计时间序列
from windget import getStmNoteEoItems21Series


# 获取非经常性损益项目小计
from windget import getStmNoteEoItems21


# 获取非经常性损益项目合计时间序列
from windget import getStmNoteEoItems24Series


# 获取非经常性损益项目合计
from windget import getStmNoteEoItems24


# 获取非经常性损益_PIT时间序列
from windget import getFaNRglSeries


# 获取非经常性损益_PIT
from windget import getFaNRgl


# 获取扣除非经常性损益后的净利润(TTM)_PIT时间序列
from windget import getFaDeductProfitTtMSeries


# 获取扣除非经常性损益后的净利润(TTM)_PIT
from windget import getFaDeductProfitTtM


# 获取扣除非经常性损益后的净利润(同比增长率)时间序列
from windget import getDpYoYSeries


# 获取扣除非经常性损益后的净利润(同比增长率)
from windget import getDpYoY


# 获取扣除非经常性损益后的净利润(TTM)时间序列
from windget import getDeductedProfitTtM2Series


# 获取扣除非经常性损益后的净利润(TTM)
from windget import getDeductedProfitTtM2


# 获取扣除非经常性损益后的净利润时间序列
from windget import getDeductedProfitSeries


# 获取扣除非经常性损益后的净利润
from windget import getDeductedProfit


# 获取扣除非经常性损益后的净利润(TTM)_GSD时间序列
from windget import getDeductedProfitTtM3Series


# 获取扣除非经常性损益后的净利润(TTM)_GSD
from windget import getDeductedProfitTtM3


# 获取单季度.扣除非经常性损益后的净利润同比增长率时间序列
from windget import getDeductedProfitYoYSeries


# 获取单季度.扣除非经常性损益后的净利润同比增长率
from windget import getDeductedProfitYoY


# 获取市盈率PE(TTM,扣除非经常性损益)时间序列
from windget import getValPeDeductedTtMSeries


# 获取市盈率PE(TTM,扣除非经常性损益)
from windget import getValPeDeductedTtM


# 获取资产减值损失/营业总收入时间序列
from windget import getImpairToGrSeries


# 获取资产减值损失/营业总收入
from windget import getImpairToGr


# 获取资产减值损失/营业利润时间序列
from windget import getImpairToOpSeries


# 获取资产减值损失/营业利润
from windget import getImpairToOp


# 获取资产减值损失/营业总收入(TTM)时间序列
from windget import getImpairToGrTtM2Series


# 获取资产减值损失/营业总收入(TTM)
from windget import getImpairToGrTtM2


# 获取资产减值损失(TTM)时间序列
from windget import getImpairmentTtM2Series


# 获取资产减值损失(TTM)
from windget import getImpairmentTtM2


# 获取资产减值损失时间序列
from windget import getImpairLossAssetsSeries


# 获取资产减值损失
from windget import getImpairLossAssets


# 获取资产减值损失/营业总收入(TTM)_PIT时间序列
from windget import getFaImpairToGrTtMSeries


# 获取资产减值损失/营业总收入(TTM)_PIT
from windget import getFaImpairToGrTtM


# 获取资产减值损失(TTM)_PIT时间序列
from windget import getFaImpairLossTtMSeries


# 获取资产减值损失(TTM)_PIT
from windget import getFaImpairLossTtM


# 获取资产减值损失/营业总收入(TTM,只有最新数据)时间序列
from windget import getImpairToGrTtMSeries


# 获取资产减值损失/营业总收入(TTM,只有最新数据)
from windget import getImpairToGrTtM


# 获取资产减值损失(TTM,只有最新数据)时间序列
from windget import getImpairmentTtMSeries


# 获取资产减值损失(TTM,只有最新数据)
from windget import getImpairmentTtM


# 获取其他资产减值损失时间序列
from windget import getOtherAssetsImpairLossSeries


# 获取其他资产减值损失
from windget import getOtherAssetsImpairLoss


# 获取固定资产减值损失时间序列
from windget import getStmNoteImpairmentLoss10Series


# 获取固定资产减值损失
from windget import getStmNoteImpairmentLoss10


# 获取单季度.资产减值损失/营业利润时间序列
from windget import getImpairToOpQfaSeries


# 获取单季度.资产减值损失/营业利润
from windget import getImpairToOpQfa


# 获取单季度.资产减值损失时间序列
from windget import getQfaImpairLossAssetsSeries


# 获取单季度.资产减值损失
from windget import getQfaImpairLossAssets


# 获取单季度.其他资产减值损失时间序列
from windget import getQfaOtherImpairSeries


# 获取单季度.其他资产减值损失
from windget import getQfaOtherImpair


# 获取财务费用明细-利息支出时间序列
from windget import getStmNoteFineXp4Series


# 获取财务费用明细-利息支出
from windget import getStmNoteFineXp4


# 获取财务费用明细-利息收入时间序列
from windget import getStmNoteFineXp5Series


# 获取财务费用明细-利息收入
from windget import getStmNoteFineXp5


# 获取财务费用明细-利息资本化金额时间序列
from windget import getStmNoteFineXp13Series


# 获取财务费用明细-利息资本化金额
from windget import getStmNoteFineXp13


# 获取财务费用明细-汇兑损益时间序列
from windget import getStmNoteFineXp6Series


# 获取财务费用明细-汇兑损益
from windget import getStmNoteFineXp6


# 获取财务费用明细-手续费时间序列
from windget import getStmNoteFineXp7Series


# 获取财务费用明细-手续费
from windget import getStmNoteFineXp7


# 获取财务费用明细-其他时间序列
from windget import getStmNoteFineXp8Series


# 获取财务费用明细-其他
from windget import getStmNoteFineXp8


# 获取研发费用同比增长时间序列
from windget import getFaRdExpYoYSeries


# 获取研发费用同比增长
from windget import getFaRdExpYoY


# 获取研发费用_GSD时间序列
from windget import getWgsDRdExpSeries


# 获取研发费用_GSD
from windget import getWgsDRdExp


# 获取研发费用时间序列
from windget import getStm07IsReItsRdFeeSeries


# 获取研发费用
from windget import getStm07IsReItsRdFee


# 获取研发费用-工资薪酬时间序列
from windget import getStmNoteRdSalarySeries


# 获取研发费用-工资薪酬
from windget import getStmNoteRdSalary


# 获取研发费用-折旧摊销时间序列
from windget import getStmNoteRdDaSeries


# 获取研发费用-折旧摊销
from windget import getStmNoteRdDa


# 获取研发费用-租赁费时间序列
from windget import getStmNoteRdLeaseSeries


# 获取研发费用-租赁费
from windget import getStmNoteRdLease


# 获取研发费用-直接投入时间序列
from windget import getStmNoteRdInvSeries


# 获取研发费用-直接投入
from windget import getStmNoteRdInv


# 获取研发费用-其他时间序列
from windget import getStmNoteRdOthersSeries


# 获取研发费用-其他
from windget import getStmNoteRdOthers


# 获取研发费用占营业收入比例时间序列
from windget import getStmNoteRdExpCostToSalesSeries


# 获取研发费用占营业收入比例
from windget import getStmNoteRdExpCostToSales


# 获取单季度.研发费用_GSD时间序列
from windget import getWgsDQfaRdExpSeries


# 获取单季度.研发费用_GSD
from windget import getWgsDQfaRdExp


# 获取单季度.研发费用时间序列
from windget import getQfaRdExpSeries


# 获取单季度.研发费用
from windget import getQfaRdExp


# 获取所得税/利润总额时间序列
from windget import getTaxToEBTSeries


# 获取所得税/利润总额
from windget import getTaxToEBT


# 获取所得税(TTM)时间序列
from windget import getTaxTtMSeries


# 获取所得税(TTM)
from windget import getTaxTtM


# 获取所得税(TTM)_GSD时间序列
from windget import getTaxTtM2Series


# 获取所得税(TTM)_GSD
from windget import getTaxTtM2


# 获取所得税_GSD时间序列
from windget import getWgsDIncTaxSeries


# 获取所得税_GSD
from windget import getWgsDIncTax


# 获取所得税时间序列
from windget import getTaxSeries


# 获取所得税
from windget import getTax


# 获取所得税影响数时间序列
from windget import getStmNoteEoItems22Series


# 获取所得税影响数
from windget import getStmNoteEoItems22


# 获取所得税费用合计时间序列
from windget import getStmNoteIncomeTax6Series


# 获取所得税费用合计
from windget import getStmNoteIncomeTax6


# 获取所得税费用_FUND时间序列
from windget import getStmIs78Series


# 获取所得税费用_FUND
from windget import getStmIs78


# 获取所得税(TTM)_PIT时间序列
from windget import getFaTaxTtMSeries


# 获取所得税(TTM)_PIT
from windget import getFaTaxTtM


# 获取递延所得税资产时间序列
from windget import getDeferredTaxAssetsSeries


# 获取递延所得税资产
from windget import getDeferredTaxAssets


# 获取递延所得税负债时间序列
from windget import getDeferredTaxLiaBSeries


# 获取递延所得税负债
from windget import getDeferredTaxLiaB


# 获取递延所得税资产减少时间序列
from windget import getDecrDeferredIncTaxAssetsSeries


# 获取递延所得税资产减少
from windget import getDecrDeferredIncTaxAssets


# 获取递延所得税负债增加时间序列
from windget import getInCrDeferredIncTaxLiaBSeries


# 获取递延所得税负债增加
from windget import getInCrDeferredIncTaxLiaB


# 获取年末所得税率时间序列
from windget import getStmNoteTaxSeries


# 获取年末所得税率
from windget import getStmNoteTax


# 获取当期所得税:中国大陆时间序列
from windget import getStmNoteIncomeTax1Series


# 获取当期所得税:中国大陆
from windget import getStmNoteIncomeTax1


# 获取当期所得税:中国香港时间序列
from windget import getStmNoteIncomeTax2Series


# 获取当期所得税:中国香港
from windget import getStmNoteIncomeTax2


# 获取当期所得税:其他境外时间序列
from windget import getStmNoteIncomeTax3Series


# 获取当期所得税:其他境外
from windget import getStmNoteIncomeTax3


# 获取递延所得税时间序列
from windget import getStmNoteIncomeTax5Series


# 获取递延所得税
from windget import getStmNoteIncomeTax5


# 获取单季度.所得税_GSD时间序列
from windget import getWgsDQfaIncTaxSeries


# 获取单季度.所得税_GSD
from windget import getWgsDQfaIncTax


# 获取单季度.所得税时间序列
from windget import getQfaTaxSeries


# 获取单季度.所得税
from windget import getQfaTax


# 获取以前年度所得税调整时间序列
from windget import getStmNoteIncomeTax4Series


# 获取以前年度所得税调整
from windget import getStmNoteIncomeTax4


# 获取单季度.递延所得税资产减少时间序列
from windget import getQfaDeferredTaxAssetsDecrSeries


# 获取单季度.递延所得税资产减少
from windget import getQfaDeferredTaxAssetsDecr


# 获取单季度.递延所得税负债增加时间序列
from windget import getQfaInCrDeferredIncTaxLiaBSeries


# 获取单季度.递延所得税负债增加
from windget import getQfaInCrDeferredIncTaxLiaB


# 获取Beta(剔除所得税率)时间序列
from windget import getRiskBetaUnIncomeTaxRateSeries


# 获取Beta(剔除所得税率)
from windget import getRiskBetaUnIncomeTaxRate


# 获取商誉及无形资产_GSD时间序列
from windget import getWgsDGwIntangSeries


# 获取商誉及无形资产_GSD
from windget import getWgsDGwIntang


# 获取商誉时间序列
from windget import getGoodwillSeries


# 获取商誉
from windget import getGoodwill


# 获取商誉减值损失时间序列
from windget import getStmNoteImpairmentLoss6Series


# 获取商誉减值损失
from windget import getStmNoteImpairmentLoss6


# 获取商誉-账面价值时间序列
from windget import getStmNoteGoodwillDetailSeries


# 获取商誉-账面价值
from windget import getStmNoteGoodwillDetail


# 获取商誉-减值准备时间序列
from windget import getStmNoteGoodwillImpairmentSeries


# 获取商誉-减值准备
from windget import getStmNoteGoodwillImpairment


# 获取应付职工薪酬时间序列
from windget import getEMplBenPayableSeries


# 获取应付职工薪酬
from windget import getEMplBenPayable


# 获取应付职工薪酬合计:本期增加时间序列
from windget import getStmNoteEMplPayableAddSeries


# 获取应付职工薪酬合计:本期增加
from windget import getStmNoteEMplPayableAdd


# 获取应付职工薪酬合计:期初余额时间序列
from windget import getStmNoteEMplPayableSbSeries


# 获取应付职工薪酬合计:期初余额
from windget import getStmNoteEMplPayableSb


# 获取应付职工薪酬合计:期末余额时间序列
from windget import getStmNoteEMplPayableEbSeries


# 获取应付职工薪酬合计:期末余额
from windget import getStmNoteEMplPayableEb


# 获取应付职工薪酬合计:本期减少时间序列
from windget import getStmNoteEMplPayableDeSeries


# 获取应付职工薪酬合计:本期减少
from windget import getStmNoteEMplPayableDe


# 获取长期应付职工薪酬时间序列
from windget import getLtEMplBenPayableSeries


# 获取长期应付职工薪酬
from windget import getLtEMplBenPayable


# 获取营业税金及附加合计时间序列
from windget import getStmNoteTaxBusinessSeries


# 获取营业税金及附加合计
from windget import getStmNoteTaxBusiness


# 获取营业税金及附加(TTM)_PIT时间序列
from windget import getFaOperTaxTtMSeries


# 获取营业税金及附加(TTM)_PIT
from windget import getFaOperTaxTtM


# 获取其他营业税金及附加时间序列
from windget import getStmNoteTaxOThSeries


# 获取其他营业税金及附加
from windget import getStmNoteTaxOTh


# 获取定期报告披露日期时间序列
from windget import getStmIssuingDateSeries


# 获取定期报告披露日期
from windget import getStmIssuingDate


# 获取定期报告正报披露日期时间序列
from windget import getStmIssuingDateFsSeries


# 获取定期报告正报披露日期
from windget import getStmIssuingDateFs


# 获取定期报告预计披露日期时间序列
from windget import getStmPredictIssuingDateSeries


# 获取定期报告预计披露日期
from windget import getStmPredictIssuingDate


# 获取报告起始日期时间序列
from windget import getStmRpTSSeries


# 获取报告起始日期
from windget import getStmRpTS


# 获取报告截止日期时间序列
from windget import getStmRpTESeries


# 获取报告截止日期
from windget import getStmRpTE


# 获取最新报告期时间序列
from windget import getLatelyRdBtSeries


# 获取最新报告期
from windget import getLatelyRdBt


# 获取会计差错更正披露日期时间序列
from windget import getFaErrorCorrectionDateSeries


# 获取会计差错更正披露日期
from windget import getFaErrorCorrectionDate


# 获取是否存在会计差错更正时间序列
from windget import getFaErrorCorrectionOrNotSeries


# 获取是否存在会计差错更正
from windget import getFaErrorCorrectionOrNot


# 获取会计准则类型时间序列
from windget import getStmNoteAuditAmSeries


# 获取会计准则类型
from windget import getStmNoteAuditAm


# 获取业绩说明会时间时间序列
from windget import getPerformanceTimeSeries


# 获取业绩说明会时间
from windget import getPerformanceTime


# 获取业绩说明会日期时间序列
from windget import getPerformanceDateSeries


# 获取业绩说明会日期
from windget import getPerformanceDate


# 获取环境维度得分时间序列
from windget import getEsGEScoreWindSeries


# 获取环境维度得分
from windget import getEsGEScoreWind


# 获取社会维度得分时间序列
from windget import getEsGSScoreWindSeries


# 获取社会维度得分
from windget import getEsGSScoreWind


# 获取治理维度得分时间序列
from windget import getEsGGScoreWindSeries


# 获取治理维度得分
from windget import getEsGGScoreWind


# 获取发行费用合计时间序列
from windget import getIssueFeeFeeSumSeries


# 获取发行费用合计
from windget import getIssueFeeFeeSum


# 获取首发发行费用时间序列
from windget import getIpoExpense2Series


# 获取首发发行费用
from windget import getIpoExpense2


# 获取首发发行费用(旧)时间序列
from windget import getIpoExpenseSeries


# 获取首发发行费用(旧)
from windget import getIpoExpense


# 获取发行结果公告日时间序列
from windget import getCbListAnnoCeDateSeries


# 获取发行结果公告日
from windget import getCbListAnnoCeDate


# 获取基金获批注册日期时间序列
from windget import getFundApprovedDateSeries


# 获取基金获批注册日期
from windget import getFundApprovedDate


# 获取发行公告日时间序列
from windget import getIssueAnnouncedAteSeries


# 获取发行公告日
from windget import getIssueAnnouncedAte


# 获取发行公告日期时间序列
from windget import getTenderAnceDateSeries


# 获取发行公告日期
from windget import getTenderAnceDate


# 获取上网发行公告日时间序列
from windget import getFellowAnnCeDateSeries


# 获取上网发行公告日
from windget import getFellowAnnCeDate


# 获取发行日期时间序列
from windget import getIssueDateSeries


# 获取发行日期
from windget import getIssueDate


# 获取首发发行日期时间序列
from windget import getIpoIssueDateSeries


# 获取首发发行日期
from windget import getIpoIssueDate


# 获取定增发行日期时间序列
from windget import getFellowIssueDatePpSeries


# 获取定增发行日期
from windget import getFellowIssueDatePp


# 获取网上发行日期时间序列
from windget import getCbListDToNlSeries


# 获取网上发行日期
from windget import getCbListDToNl


# 获取网下向机构投资者发行日期时间序列
from windget import getCbListDateInStOffSeries


# 获取网下向机构投资者发行日期
from windget import getCbListDateInStOff


# 获取发行方式时间序列
from windget import getIssueTypeSeries


# 获取发行方式
from windget import getIssueType


# 获取首发发行方式时间序列
from windget import getIpoTypeSeries


# 获取首发发行方式
from windget import getIpoType


# 获取增发发行方式时间序列
from windget import getFellowIssueTypeSeries


# 获取增发发行方式
from windget import getFellowIssueType


# 获取发行对象时间序列
from windget import getIssueObjectSeries


# 获取发行对象
from windget import getIssueObject


# 获取增发发行对象时间序列
from windget import getFellowShareholdersSeries


# 获取增发发行对象
from windget import getFellowShareholders


# 获取发行份额时间序列
from windget import getIssueUnitSeries


# 获取发行份额
from windget import getIssueUnit


# 获取发行总份额时间序列
from windget import getIssueTotalUnitSeries


# 获取发行总份额
from windget import getIssueTotalUnit


# 获取发行规模时间序列
from windget import getFundReItsIssueSizeSeries


# 获取发行规模
from windget import getFundReItsIssueSize


# 获取实际发行规模时间序列
from windget import getFundActualScaleSeries


# 获取实际发行规模
from windget import getFundActualScale


# 获取发行总规模时间序列
from windget import getIssueTotalSizeSeries


# 获取发行总规模
from windget import getIssueTotalSize


# 获取基金发起人时间序列
from windget import getIssueInitiatorSeries


# 获取基金发起人
from windget import getIssueInitiator


# 获取基金主承销商时间序列
from windget import getIssueLeadUnderwriterSeries


# 获取基金主承销商
from windget import getIssueLeadUnderwriter


# 获取基金销售代理人时间序列
from windget import getIssueDeputySeries


# 获取基金销售代理人
from windget import getIssueDeputy


# 获取基金上市推荐人时间序列
from windget import getIssueNominatorSeries


# 获取基金上市推荐人
from windget import getIssueNominator


# 获取发行封闭期时间序列
from windget import getIssueOeClsPeriodSeries


# 获取发行封闭期
from windget import getIssueOeClsPeriod


# 获取成立条件-净认购份额时间序列
from windget import getIssueOeCNdNetPurchaseSeries


# 获取成立条件-净认购份额
from windget import getIssueOeCNdNetPurchase


# 获取成立条件-认购户数时间序列
from windget import getIssueOeCNdPurchasersSeries


# 获取成立条件-认购户数
from windget import getIssueOeCNdPurchasers


# 获取募集份额上限时间序列
from windget import getIssueOEfMaxCollectionSeries


# 获取募集份额上限
from windget import getIssueOEfMaxCollection


# 获取认购份额确认比例时间序列
from windget import getIssueOEfConfirmRatioSeries


# 获取认购份额确认比例
from windget import getIssueOEfConfirmRatio


# 获取开放式基金认购户数时间序列
from windget import getIssueOEfNumPurchasersSeries


# 获取开放式基金认购户数
from windget import getIssueOEfNumPurchasers


# 获取上市交易份额时间序列
from windget import getIssueEtFDealShareOnMarketSeries


# 获取上市交易份额
from windget import getIssueEtFDealShareOnMarket


# 获取网上现金发售代码时间序列
from windget import getIssueOnlineCashOfferingSymbolSeries


# 获取网上现金发售代码
from windget import getIssueOnlineCashOfferingSymbol


# 获取一级市场基金代码时间序列
from windget import getIssueFirstMarketFundCodeSeries


# 获取一级市场基金代码
from windget import getIssueFirstMarketFundCode


# 获取个人投资者认购方式时间序列
from windget import getIssueOEfMThDInDSeries


# 获取个人投资者认购方式
from windget import getIssueOEfMThDInD


# 获取个人投资者认购金额下限时间序列
from windget import getIssueOEfMinamTinDSeries


# 获取个人投资者认购金额下限
from windget import getIssueOEfMinamTinD


# 获取个人投资者认购金额上限时间序列
from windget import getIssueOEfMaxAmtInDSeries


# 获取个人投资者认购金额上限
from windget import getIssueOEfMaxAmtInD


# 获取个人投资者认购起始日时间序列
from windget import getIssueOEfStartDateInDSeries


# 获取个人投资者认购起始日
from windget import getIssueOEfStartDateInD


# 获取个人投资者认购终止日时间序列
from windget import getIssueOEfEnddateInDSeries


# 获取个人投资者认购终止日
from windget import getIssueOEfEnddateInD


# 获取封闭期机构投资者认购方式时间序列
from windget import getIssueOEfMThDInStSeries


# 获取封闭期机构投资者认购方式
from windget import getIssueOEfMThDInSt


# 获取机构投资者设立认购起始日时间序列
from windget import getIssueOEfStartDateInStSeries


# 获取机构投资者设立认购起始日
from windget import getIssueOEfStartDateInSt


# 获取机构投资者设立认购终止日时间序列
from windget import getIssueOEfDndDateInStSeries


# 获取机构投资者设立认购终止日
from windget import getIssueOEfDndDateInSt


# 获取封闭期机构投资者认购下限时间序列
from windget import getIssueOEfMinamTinStSeries


# 获取封闭期机构投资者认购下限
from windget import getIssueOEfMinamTinSt


# 获取封闭期机构投资者认购上限时间序列
from windget import getIssueOEfMaxAmtInStSeries


# 获取封闭期机构投资者认购上限
from windget import getIssueOEfMaxAmtInSt


# 获取封闭式基金认购数量时间序列
from windget import getIssueCefInIPurchaseSeries


# 获取封闭式基金认购数量
from windget import getIssueCefInIPurchase


# 获取封闭式基金超额认购倍数时间序列
from windget import getIssueCefOverSubSeries


# 获取封闭式基金超额认购倍数
from windget import getIssueCefOverSub


# 获取封闭式基金中签率时间序列
from windget import getIssueCefSuccRatioSeries


# 获取封闭式基金中签率
from windget import getIssueCefSuccRatio


# 获取是否提前开始募集时间序列
from windget import getIssueRaSingIsStartEarlySeries


# 获取是否提前开始募集
from windget import getIssueRaSingIsStartEarly


# 获取是否延期募集时间序列
from windget import getIssueRaSingIsStartDeferredSeries


# 获取是否延期募集
from windget import getIssueRaSingIsStartDeferred


# 获取是否提前结束募集时间序列
from windget import getIssueRaSingIsEndEarlySeries


# 获取是否提前结束募集
from windget import getIssueRaSingIsEndEarly


# 获取是否延长募集期时间序列
from windget import getIssueRaSingIsEndDeferredSeries


# 获取是否延长募集期
from windget import getIssueRaSingIsEndDeferred


# 获取认购天数时间序列
from windget import getIssueOEfDaysSeries


# 获取认购天数
from windget import getIssueOEfDays


# 获取单位年度分红时间序列
from windget import getDivPerUnitSeries


# 获取单位年度分红
from windget import getDivPerUnit


# 获取单位累计分红时间序列
from windget import getDivAccumulatedPerUnitSeries


# 获取单位累计分红
from windget import getDivAccumulatedPerUnit


# 获取年度分红总额时间序列
from windget import getDivPayOutSeries


# 获取年度分红总额
from windget import getDivPayOut


# 获取年度分红次数时间序列
from windget import getDivTimesSeries


# 获取年度分红次数
from windget import getDivTimes


# 获取累计分红总额时间序列
from windget import getDivAccumulatedPayOutSeries


# 获取累计分红总额
from windget import getDivAccumulatedPayOut


# 获取年度累计分红总额时间序列
from windget import getDivAuALaCcmDiv3Series


# 获取年度累计分红总额
from windget import getDivAuALaCcmDiv3


# 获取年度累计分红总额(已宣告)时间序列
from windget import getDivAuALaCcmDivArdSeries


# 获取年度累计分红总额(已宣告)
from windget import getDivAuALaCcmDivArd


# 获取年度累计分红总额(沪深)时间序列
from windget import getDivAuALaCcmDivSeries


# 获取年度累计分红总额(沪深)
from windget import getDivAuALaCcmDiv


# 获取累计分红次数时间序列
from windget import getDivAccumulatedTimesSeries


# 获取累计分红次数
from windget import getDivAccumulatedTimes


# 获取区间单位分红时间序列
from windget import getDivPeriodPerUnitSeries


# 获取区间单位分红
from windget import getDivPeriodPerUnit


# 获取区间分红总额时间序列
from windget import getDivPeriodPayOutSeries


# 获取区间分红总额
from windget import getDivPeriodPayOut


# 获取区间分红次数时间序列
from windget import getDivPeriodTimesSeries


# 获取区间分红次数
from windget import getDivPeriodTimes


# 获取分红条款时间序列
from windget import getDivClauseSeries


# 获取分红条款
from windget import getDivClause


# 获取区间诉讼次数时间序列
from windget import getCacLawsuitNumSeries


# 获取区间诉讼次数
from windget import getCacLawsuitNum


# 获取区间诉讼涉案金额时间序列
from windget import getCacLawsuitAmountSeries


# 获取区间诉讼涉案金额
from windget import getCacLawsuitAmount


# 获取区间违规处罚次数时间序列
from windget import getCacIllegalityNumSeries


# 获取区间违规处罚次数
from windget import getCacIllegalityNum


# 获取区间违规处罚金额时间序列
from windget import getCacIllegalityAmountSeries


# 获取区间违规处罚金额
from windget import getCacIllegalityAmount


# 获取未上市流通基金份数(封闭式)时间序列
from windget import getUnitNonTradableSeries


# 获取未上市流通基金份数(封闭式)
from windget import getUnitNonTradable


# 获取已上市流通基金份数(封闭式)时间序列
from windget import getUnitTradableSeries


# 获取已上市流通基金份数(封闭式)
from windget import getUnitTradable


# 获取基金资产总值时间序列
from windget import getPrtTotalAssetSeries


# 获取基金资产总值
from windget import getPrtTotalAsset


# 获取基金资产总值变动时间序列
from windget import getPrtTotalAssetChangeSeries


# 获取基金资产总值变动
from windget import getPrtTotalAssetChange


# 获取基金资产总值变动率时间序列
from windget import getPrtTotalAssetChangeRatioSeries


# 获取基金资产总值变动率
from windget import getPrtTotalAssetChangeRatio


# 获取基金净值占基金资产总值比时间序列
from windget import getPrtNavToAssetSeries


# 获取基金净值占基金资产总值比
from windget import getPrtNavToAsset


# 获取股票市值占基金资产总值比时间序列
from windget import getPrtStockToAssetSeries


# 获取股票市值占基金资产总值比
from windget import getPrtStockToAsset


# 获取债券市值占基金资产总值比时间序列
from windget import getPrtBondToAssetSeries


# 获取债券市值占基金资产总值比
from windget import getPrtBondToAsset


# 获取基金市值占基金资产总值比时间序列
from windget import getPrtFundToAssetSeries


# 获取基金市值占基金资产总值比
from windget import getPrtFundToAsset


# 获取权证市值占基金资产总值比时间序列
from windget import getPrtWarrantToAssetSeries


# 获取权证市值占基金资产总值比
from windget import getPrtWarrantToAsset


# 获取其他资产占基金资产总值比时间序列
from windget import getPrtOtherToAssetSeries


# 获取其他资产占基金资产总值比
from windget import getPrtOtherToAsset


# 获取国债市值占基金资产总值比时间序列
from windget import getPrtGovernmentBondToAssetSeries


# 获取国债市值占基金资产总值比
from windget import getPrtGovernmentBondToAsset


# 获取金融债市值占基金资产总值比时间序列
from windget import getPrtFinancialBondToAssetSeries


# 获取金融债市值占基金资产总值比
from windget import getPrtFinancialBondToAsset


# 获取企业债市值占基金资产总值比时间序列
from windget import getPrtCorporateBondsToAssetSeries


# 获取企业债市值占基金资产总值比
from windget import getPrtCorporateBondsToAsset


# 获取可转债市值占基金资产总值比时间序列
from windget import getPrtConvertibleBondToAssetSeries


# 获取可转债市值占基金资产总值比
from windget import getPrtConvertibleBondToAsset


# 获取分行业市值占基金资产总值比时间序列
from windget import getPrtStockValueIndustryToAsset2Series


# 获取分行业市值占基金资产总值比
from windget import getPrtStockValueIndustryToAsset2


# 获取重仓股市值占基金资产总值比时间序列
from windget import getPrtHeavilyHeldStockToAssetSeries


# 获取重仓股市值占基金资产总值比
from windget import getPrtHeavilyHeldStockToAsset


# 获取港股投资市值占基金资产总值比时间序列
from windget import getPrtHkStockToAssetSeries


# 获取港股投资市值占基金资产总值比
from windget import getPrtHkStockToAsset


# 获取买入返售证券占基金资产总值比例时间序列
from windget import getMmFReverseRepoToAssetSeries


# 获取买入返售证券占基金资产总值比例
from windget import getMmFReverseRepoToAsset


# 获取央行票据市值占基金资产总值比时间序列
from windget import getPrtCentralBankBillToAssetSeries


# 获取央行票据市值占基金资产总值比
from windget import getPrtCentralBankBillToAsset


# 获取重仓行业市值占基金资产总值比时间序列
from windget import getPrtStockValueTopIndustryToAsset2Series


# 获取重仓行业市值占基金资产总值比
from windget import getPrtStockValueTopIndustryToAsset2


# 获取重仓债券市值占基金资产总值比时间序列
from windget import getPrtHeavilyHeldBondToAssetSeries


# 获取重仓债券市值占基金资产总值比
from windget import getPrtHeavilyHeldBondToAsset


# 获取重仓基金市值占基金资产总值比时间序列
from windget import getPrtHeavilyHeldFundToAssetSeries


# 获取重仓基金市值占基金资产总值比
from windget import getPrtHeavilyHeldFundToAsset


# 获取政策性金融债市值占基金资产总值比时间序列
from windget import getPrtPFbToAssetSeries


# 获取政策性金融债市值占基金资产总值比
from windget import getPrtPFbToAsset


# 获取企业发行债券市值占基金资产总值比时间序列
from windget import getPrtCorporateBondToAssetSeries


# 获取企业发行债券市值占基金资产总值比
from windget import getPrtCorporateBondToAsset


# 获取重仓资产支持证券市值占基金资产总值比时间序列
from windget import getPrtHeavilyHeldAbsToAssetSeries


# 获取重仓资产支持证券市值占基金资产总值比
from windget import getPrtHeavilyHeldAbsToAsset


# 获取转融通证券出借业务市值占基金资产总值比时间序列
from windget import getPrtSecLendingValueToAssetSeries


# 获取转融通证券出借业务市值占基金资产总值比
from windget import getPrtSecLendingValueToAsset


# 获取基金资产净值时间序列
from windget import getPrtNetAssetSeries


# 获取基金资产净值
from windget import getPrtNetAsset


# 获取基金资产净值变动时间序列
from windget import getPrtNetAssetChangeSeries


# 获取基金资产净值变动
from windget import getPrtNetAssetChange


# 获取基金资产净值变动率时间序列
from windget import getPrtNetAssetChangeRatioSeries


# 获取基金资产净值变动率
from windget import getPrtNetAssetChangeRatio


# 获取报告期基金资产净值币种时间序列
from windget import getPrtCurrencySeries


# 获取报告期基金资产净值币种
from windget import getPrtCurrency


# 获取股票市值占基金资产净值比时间序列
from windget import getPrtStocktonAvSeries


# 获取股票市值占基金资产净值比
from windget import getPrtStocktonAv


# 获取债券市值占基金资产净值比时间序列
from windget import getPrtBondToNavSeries


# 获取债券市值占基金资产净值比
from windget import getPrtBondToNav


# 获取基金市值占基金资产净值比时间序列
from windget import getPrtFundToNavSeries


# 获取基金市值占基金资产净值比
from windget import getPrtFundToNav


# 获取权证市值占基金资产净值比时间序列
from windget import getPrtWarrantToNavSeries


# 获取权证市值占基金资产净值比
from windget import getPrtWarrantToNav


# 获取其他资产占基金资产净值比时间序列
from windget import getPrtOtherToNavSeries


# 获取其他资产占基金资产净值比
from windget import getPrtOtherToNav


# 获取股票市值占基金资产净值比例增长时间序列
from windget import getPrtStocktonAvGrowthSeries


# 获取股票市值占基金资产净值比例增长
from windget import getPrtStocktonAvGrowth


# 获取债券市值占基金资产净值比例增长时间序列
from windget import getPrtBondToNavGrowthSeries


# 获取债券市值占基金资产净值比例增长
from windget import getPrtBondToNavGrowth


# 获取基金市值占基金资产净值比例增长时间序列
from windget import getPrtFundToNavGrowthSeries


# 获取基金市值占基金资产净值比例增长
from windget import getPrtFundToNavGrowth


# 获取权证市值占基金资产净值比例增长时间序列
from windget import getPrtWarrantToNavGrowthSeries


# 获取权证市值占基金资产净值比例增长
from windget import getPrtWarrantToNavGrowth


# 获取国债市值占基金资产净值比时间序列
from windget import getPrtGovernmentBondToNavSeries


# 获取国债市值占基金资产净值比
from windget import getPrtGovernmentBondToNav


# 获取国债市值占基金资产净值比例增长时间序列
from windget import getPrtGovernmentBondToNavGrowthSeries


# 获取国债市值占基金资产净值比例增长
from windget import getPrtGovernmentBondToNavGrowth


# 获取金融债市值占基金资产净值比时间序列
from windget import getPrtFinancialBondToNavSeries


# 获取金融债市值占基金资产净值比
from windget import getPrtFinancialBondToNav


# 获取企业债市值占基金资产净值比时间序列
from windget import getPrtCorporateBondsToNavSeries


# 获取企业债市值占基金资产净值比
from windget import getPrtCorporateBondsToNav


# 获取可转债市值占基金资产净值比时间序列
from windget import getPrtConvertibleBondToNavSeries


# 获取可转债市值占基金资产净值比
from windget import getPrtConvertibleBondToNav


# 获取金融债市值占基金资产净值比例增长时间序列
from windget import getPrtFinancialBondToNavGrowthSeries


# 获取金融债市值占基金资产净值比例增长
from windget import getPrtFinancialBondToNavGrowth


# 获取企业债市值占基金资产净值比例增长时间序列
from windget import getPrtCorporateBondsToNavGrowthSeries


# 获取企业债市值占基金资产净值比例增长
from windget import getPrtCorporateBondsToNavGrowth


# 获取可转债市值占基金资产净值比例增长时间序列
from windget import getPrtConvertibleBondToNavGrowthSeries


# 获取可转债市值占基金资产净值比例增长
from windget import getPrtConvertibleBondToNavGrowth


# 获取分行业市值占基金资产净值比时间序列
from windget import getPrtStockValueIndustryToNav2Series


# 获取分行业市值占基金资产净值比
from windget import getPrtStockValueIndustryToNav2


# 获取分行业市值占基金资产净值比增长时间序列
from windget import getPrtStockValueIndustryToNavGrowth2Series


# 获取分行业市值占基金资产净值比增长
from windget import getPrtStockValueIndustryToNavGrowth2


# 获取分行业市值占基金资产净值比增长(Wind)时间序列
from windget import getPrtIndustryToNavGrowthWindSeries


# 获取分行业市值占基金资产净值比增长(Wind)
from windget import getPrtIndustryToNavGrowthWind


# 获取分行业市值占基金资产净值比增长(中信)时间序列
from windget import getPrtIndustryToNavGrowthCitiCSeries


# 获取分行业市值占基金资产净值比增长(中信)
from windget import getPrtIndustryToNavGrowthCitiC


# 获取分行业市值占基金资产净值比增长(申万)时间序列
from windget import getPrtIndustryToNavGrowthSwSeries


# 获取分行业市值占基金资产净值比增长(申万)
from windget import getPrtIndustryToNavGrowthSw


# 获取重仓股市值占基金资产净值比时间序列
from windget import getPrtHeavilyHeldStocktonAvSeries


# 获取重仓股市值占基金资产净值比
from windget import getPrtHeavilyHeldStocktonAv


# 获取各期限资产占基金资产净值比例时间序列
from windget import getMmFDifferentPtMToNavSeries


# 获取各期限资产占基金资产净值比例
from windget import getMmFDifferentPtMToNav


# 获取港股投资市值占基金资产净值比时间序列
from windget import getPrtHkStocktonAvSeries


# 获取港股投资市值占基金资产净值比
from windget import getPrtHkStocktonAv


# 获取买入返售证券占基金资产净值比例时间序列
from windget import getPrtReverseRepoToNavSeries


# 获取买入返售证券占基金资产净值比例
from windget import getPrtReverseRepoToNav


# 获取其他资产市值占基金资产净值比例增长时间序列
from windget import getPrtOtherToNavGrowthSeries


# 获取其他资产市值占基金资产净值比例增长
from windget import getPrtOtherToNavGrowth


# 获取同业存单市值占基金资产净值比时间序列
from windget import getPrtCdsToNavSeries


# 获取同业存单市值占基金资产净值比
from windget import getPrtCdsToNav


# 获取央行票据市值占基金资产净值比时间序列
from windget import getPrtCentralBankBillToNavSeries


# 获取央行票据市值占基金资产净值比
from windget import getPrtCentralBankBillToNav


# 获取中期票据市值占基金资产净值比时间序列
from windget import getPrtMtnToNavSeries


# 获取中期票据市值占基金资产净值比
from windget import getPrtMtnToNav


# 获取其他债券市值占基金资产净值比时间序列
from windget import getPrtOtherBondToNavSeries


# 获取其他债券市值占基金资产净值比
from windget import getPrtOtherBondToNav


# 获取央行票据市值占基金资产净值比例增长时间序列
from windget import getPrtCentralBankBillToNavGrowthSeries


# 获取央行票据市值占基金资产净值比例增长
from windget import getPrtCentralBankBillToNavGrowth


# 获取重仓行业市值占基金资产净值比时间序列
from windget import getPrtStockValueTopIndustryToNav2Series


# 获取重仓行业市值占基金资产净值比
from windget import getPrtStockValueTopIndustryToNav2


# 获取重仓债券市值占基金资产净值比时间序列
from windget import getPrtHeavilyHeldBondToNavSeries


# 获取重仓债券市值占基金资产净值比
from windget import getPrtHeavilyHeldBondToNav


# 获取重仓基金市值占基金资产净值比时间序列
from windget import getPrtHeavilyHeldFundToNavSeries


# 获取重仓基金市值占基金资产净值比
from windget import getPrtHeavilyHeldFundToNav


# 获取短期融资券市值占基金资产净值比时间序列
from windget import getPrtCpToNavSeries


# 获取短期融资券市值占基金资产净值比
from windget import getPrtCpToNav


# 获取分行业投资市值占基金资产净值比例(Wind全球行业)时间序列
from windget import getPrtGicSIndustryValueToNavSeries


# 获取分行业投资市值占基金资产净值比例(Wind全球行业)
from windget import getPrtGicSIndustryValueToNav


# 获取分行业投资市值占基金资产净值比(Wind)时间序列
from windget import getPrtIndustryValueToNavWindSeries


# 获取分行业投资市值占基金资产净值比(Wind)
from windget import getPrtIndustryValueToNavWind


# 获取分行业投资市值占基金资产净值比(中信)时间序列
from windget import getPrtIndustryValueToNavCitiCSeries


# 获取分行业投资市值占基金资产净值比(中信)
from windget import getPrtIndustryValueToNavCitiC


# 获取分行业投资市值占基金资产净值比(申万)时间序列
from windget import getPrtIndustryValueToNavSwSeries


# 获取分行业投资市值占基金资产净值比(申万)
from windget import getPrtIndustryValueToNavSw


# 获取单季度.报告期期末基金资产净值时间序列
from windget import getQAnalNetAssetSeries


# 获取单季度.报告期期末基金资产净值
from windget import getQAnalNetAsset


# 获取指数投资股票市值占基金资产净值比时间序列
from windget import getPrtStocktonAvPassiveInvestSeries


# 获取指数投资股票市值占基金资产净值比
from windget import getPrtStocktonAvPassiveInvest


# 获取积极投资股票市值占基金资产净值比时间序列
from windget import getPrtStocktonAvActiveInvestSeries


# 获取积极投资股票市值占基金资产净值比
from windget import getPrtStocktonAvActiveInvest


# 获取政策性金融债市值占基金资产净值比时间序列
from windget import getPrtPFbToNavSeries


# 获取政策性金融债市值占基金资产净值比
from windget import getPrtPFbToNav


# 获取企业发行债券市值占基金资产净值比时间序列
from windget import getPrtCorporateBondToNavSeries


# 获取企业发行债券市值占基金资产净值比
from windget import getPrtCorporateBondToNav


# 获取资产支持证券市值占基金资产净值比时间序列
from windget import getPrtAbsToNavSeries


# 获取资产支持证券市值占基金资产净值比
from windget import getPrtAbsToNav


# 获取货币市场工具市值占基金资产净值比时间序列
from windget import getPrtMMitoNavSeries


# 获取货币市场工具市值占基金资产净值比
from windget import getPrtMMitoNav


# 获取企业发行债券市值占基金资产净值比例增长时间序列
from windget import getPrtCorporateBondToNavGrowthSeries


# 获取企业发行债券市值占基金资产净值比例增长
from windget import getPrtCorporateBondToNavGrowth


# 获取重仓行业投资市值占基金资产净值比例(Wind全球行业)时间序列
from windget import getPrtTopGicSIndustryValueToNavSeries


# 获取重仓行业投资市值占基金资产净值比例(Wind全球行业)
from windget import getPrtTopGicSIndustryValueToNav


# 获取重仓行业投资市值占基金资产净值比(Wind)时间序列
from windget import getPrtTopIndustryValueToNavWindSeries


# 获取重仓行业投资市值占基金资产净值比(Wind)
from windget import getPrtTopIndustryValueToNavWind


# 获取重仓行业投资市值占基金资产净值比(中信)时间序列
from windget import getPrtTopIndustryValueToNavCitiCSeries


# 获取重仓行业投资市值占基金资产净值比(中信)
from windget import getPrtTopIndustryValueToNavCitiC


# 获取重仓行业投资市值占基金资产净值比(申万)时间序列
from windget import getPrtTopIndustryValueToNavSwSeries


# 获取重仓行业投资市值占基金资产净值比(申万)
from windget import getPrtTopIndustryValueToNavSw


# 获取国家/地区投资市值占基金资产净值比例(QDII)时间序列
from windget import getPrtQdIiCountryRegionInvestmentToNavSeries


# 获取国家/地区投资市值占基金资产净值比例(QDII)
from windget import getPrtQdIiCountryRegionInvestmentToNav


# 获取重仓资产支持证券市值占基金资产净值比时间序列
from windget import getPrtHeavilyHeldAbsToNavSeries


# 获取重仓资产支持证券市值占基金资产净值比
from windget import getPrtHeavilyHeldAbsToNav


# 获取转融通证券出借业务市值占基金资产净值比时间序列
from windget import getPrtSecLendingValueToNavSeries


# 获取转融通证券出借业务市值占基金资产净值比
from windget import getPrtSecLendingValueToNav


# 获取前N名重仓股票市值合计占基金资产净值比时间序列
from windget import getPrtTopNStocktonAvSeries


# 获取前N名重仓股票市值合计占基金资产净值比
from windget import getPrtTopNStocktonAv


# 获取前N名重仓债券市值合计占基金资产净值比时间序列
from windget import getPrtTop5ToNavSeries


# 获取前N名重仓债券市值合计占基金资产净值比
from windget import getPrtTop5ToNav


# 获取前N名重仓基金市值合计占基金资产净值比时间序列
from windget import getPrtTopNFundToNavSeries


# 获取前N名重仓基金市值合计占基金资产净值比
from windget import getPrtTopNFundToNav


# 获取报告期基金日均资产净值时间序列
from windget import getPrtAvgNetAssetSeries


# 获取报告期基金日均资产净值
from windget import getPrtAvgNetAsset


# 获取资产净值(合计)时间序列
from windget import getPrtFundNetAssetTotalSeries


# 获取资产净值(合计)
from windget import getPrtFundNetAssetTotal


# 获取资产净值是否为合并数据(最新)时间序列
from windget import getPrtMergedNavOrNotSeries


# 获取资产净值是否为合并数据(最新)
from windget import getPrtMergedNavOrNot


# 获取资产净值是否为合并数据(报告期)时间序列
from windget import getPrtMergedNavOrNot1Series


# 获取资产净值是否为合并数据(报告期)
from windget import getPrtMergedNavOrNot1


# 获取同类基金平均规模时间序列
from windget import getFundAvgFundScaleSeries


# 获取同类基金平均规模
from windget import getFundAvgFundScale


# 获取市场展望时间序列
from windget import getFundMarketOutlookSeries


# 获取市场展望
from windget import getFundMarketOutlook


# 获取市场分析时间序列
from windget import getFundMarketAnalysisSeries


# 获取市场分析
from windget import getFundMarketAnalysis


# 获取股票投资市值时间序列
from windget import getPrtStockValueSeries


# 获取股票投资市值
from windget import getPrtStockValue


# 获取分行业市值占股票投资市值比时间序列
from windget import getPrtStockValueIndustryTostock2Series


# 获取分行业市值占股票投资市值比
from windget import getPrtStockValueIndustryTostock2


# 获取重仓股市值占股票投资市值比时间序列
from windget import getPrtHeavilyHeldStockTostockSeries


# 获取重仓股市值占股票投资市值比
from windget import getPrtHeavilyHeldStockTostock


# 获取重仓行业市值占股票投资市值比时间序列
from windget import getPrtStockValueTopIndustryTostock2Series


# 获取重仓行业市值占股票投资市值比
from windget import getPrtStockValueTopIndustryTostock2


# 获取前N名重仓股票市值合计占股票投资市值比时间序列
from windget import getPrtTopNStockTostockSeries


# 获取前N名重仓股票市值合计占股票投资市值比
from windget import getPrtTopNStockTostock


# 获取指数投资股票市值时间序列
from windget import getPrtStockValuePassiveInvestSeries


# 获取指数投资股票市值
from windget import getPrtStockValuePassiveInvest


# 获取积极投资股票市值时间序列
from windget import getPrtStockValueActiveInvestSeries


# 获取积极投资股票市值
from windget import getPrtStockValueActiveInvest


# 获取港股投资市值时间序列
from windget import getPrtHkStockValueSeries


# 获取港股投资市值
from windget import getPrtHkStockValue


# 获取债券投资市值时间序列
from windget import getPrtBondValueSeries


# 获取债券投资市值
from windget import getPrtBondValue


# 获取国债市值占债券投资市值比时间序列
from windget import getPrtGovernmentBondToBondSeries


# 获取国债市值占债券投资市值比
from windget import getPrtGovernmentBondToBond


# 获取金融债市值占债券投资市值比时间序列
from windget import getPrtFinancialBondToBondSeries


# 获取金融债市值占债券投资市值比
from windget import getPrtFinancialBondToBond


# 获取企业债市值占债券投资市值比时间序列
from windget import getPrtCorporateBondsToBondSeries


# 获取企业债市值占债券投资市值比
from windget import getPrtCorporateBondsToBond


# 获取可转债市值占债券投资市值比时间序列
from windget import getPrtConvertibleBondToBondSeries


# 获取可转债市值占债券投资市值比
from windget import getPrtConvertibleBondToBond


# 获取央行票据市值占债券投资市值比时间序列
from windget import getPrtCentralBankBillToBondSeries


# 获取央行票据市值占债券投资市值比
from windget import getPrtCentralBankBillToBond


# 获取政策性金融债占债券投资市值比时间序列
from windget import getPrtPFbToBondSeries


# 获取政策性金融债占债券投资市值比
from windget import getPrtPFbToBond


# 获取同业存单市值占债券投资市值比时间序列
from windget import getPrtNcdToBondSeries


# 获取同业存单市值占债券投资市值比
from windget import getPrtNcdToBond


# 获取重仓债券市值占债券投资市值比时间序列
from windget import getPrtHeavilyHeldBondToBondSeries


# 获取重仓债券市值占债券投资市值比
from windget import getPrtHeavilyHeldBondToBond


# 获取企业发行债券市值占债券投资市值比时间序列
from windget import getPrtCorporateBondToBondSeries


# 获取企业发行债券市值占债券投资市值比
from windget import getPrtCorporateBondToBond


# 获取前N名重仓债券市值合计占债券投资市值比时间序列
from windget import getPrtTop5ToBondSeries


# 获取前N名重仓债券市值合计占债券投资市值比
from windget import getPrtTop5ToBond


# 获取基金投资市值时间序列
from windget import getPrtFundValueSeries


# 获取基金投资市值
from windget import getPrtFundValue


# 获取重仓基金市值占基金投资市值比时间序列
from windget import getPrtHeavilyHeldFundToFundSeries


# 获取重仓基金市值占基金投资市值比
from windget import getPrtHeavilyHeldFundToFund


# 获取前N名重仓基金市值合计占基金投资市值比时间序列
from windget import getPrtTopFundToFundSeries


# 获取前N名重仓基金市值合计占基金投资市值比
from windget import getPrtTopFundToFund


# 获取股指期货投资市值时间序列
from windget import getPrtSiFuturesSeries


# 获取股指期货投资市值
from windget import getPrtSiFutures


# 获取国债期货投资市值时间序列
from windget import getPrtGbFuturesSeries


# 获取国债期货投资市值
from windget import getPrtGbFutures


# 获取权证投资市值时间序列
from windget import getPrtWarrantValueSeries


# 获取权证投资市值
from windget import getPrtWarrantValue


# 获取转融通证券出借业务市值时间序列
from windget import getPrtSecLendingValueSeries


# 获取转融通证券出借业务市值
from windget import getPrtSecLendingValue


# 获取其他资产_GSD时间序列
from windget import getWgsDAssetsOThSeries


# 获取其他资产_GSD
from windget import getWgsDAssetsOTh


# 获取其他资产时间序列
from windget import getPrtOtherSeries


# 获取其他资产
from windget import getPrtOther


# 获取其他资产_FUND时间序列
from windget import getStmBs18Series


# 获取其他资产_FUND
from windget import getStmBs18


# 获取其他资产市值增长率时间序列
from windget import getPrtOtherValueGrowthSeries


# 获取其他资产市值增长率
from windget import getPrtOtherValueGrowth


# 获取股票市值增长率时间序列
from windget import getPrtStockValueGrowthSeries


# 获取股票市值增长率
from windget import getPrtStockValueGrowth


# 获取债券市值增长率时间序列
from windget import getPrtBondValueGrowthSeries


# 获取债券市值增长率
from windget import getPrtBondValueGrowth


# 获取企业发行债券市值增长率时间序列
from windget import getPrtCorporateBondGrowthSeries


# 获取企业发行债券市值增长率
from windget import getPrtCorporateBondGrowth


# 获取基金市值增长率时间序列
from windget import getPrtFundValueGrowthSeries


# 获取基金市值增长率
from windget import getPrtFundValueGrowth


# 获取权证市值增长率时间序列
from windget import getPrtWarrantValueGrowthSeries


# 获取权证市值增长率
from windget import getPrtWarrantValueGrowth


# 获取基金杠杆率时间序列
from windget import getPrtFoundLeverageSeries


# 获取基金杠杆率
from windget import getPrtFoundLeverage


# 获取国债市值时间序列
from windget import getPrtGovernmentBondSeries


# 获取国债市值
from windget import getPrtGovernmentBond


# 获取国债市值增长率时间序列
from windget import getPrtGovernmentBondGrowthSeries


# 获取国债市值增长率
from windget import getPrtGovernmentBondGrowth


# 获取同业存单市值时间序列
from windget import getPrtCdsSeries


# 获取同业存单市值
from windget import getPrtCds


# 获取央行票据市值时间序列
from windget import getPrtCentralBankBillSeries


# 获取央行票据市值
from windget import getPrtCentralBankBill


# 获取央行票据市值增长率时间序列
from windget import getPrtCentralBankBillGrowthSeries


# 获取央行票据市值增长率
from windget import getPrtCentralBankBillGrowth


# 获取金融债市值时间序列
from windget import getPrtFinancialBondSeries


# 获取金融债市值
from windget import getPrtFinancialBond


# 获取金融债市值增长率时间序列
from windget import getPrtFinancialBondGrowthSeries


# 获取金融债市值增长率
from windget import getPrtFinancialBondGrowth


# 获取政策性金融债市值时间序列
from windget import getPrtPFbValueSeries


# 获取政策性金融债市值
from windget import getPrtPFbValue


# 获取企业发行债券市值时间序列
from windget import getPrtCorporateBondSeries


# 获取企业发行债券市值
from windget import getPrtCorporateBond


# 获取企业债市值时间序列
from windget import getPrtCorporateBondsSeries


# 获取企业债市值
from windget import getPrtCorporateBonds


# 获取企业债市值增长率时间序列
from windget import getPrtCorporateBondsGrowthSeries


# 获取企业债市值增长率
from windget import getPrtCorporateBondsGrowth


# 获取短期融资券市值时间序列
from windget import getPrtCpValueSeries


# 获取短期融资券市值
from windget import getPrtCpValue


# 获取中期票据市值时间序列
from windget import getPrtMtnValueSeries


# 获取中期票据市值
from windget import getPrtMtnValue


# 获取可转债市值时间序列
from windget import getPrtConvertibleBondSeries


# 获取可转债市值
from windget import getPrtConvertibleBond


# 获取可转债市值增长率时间序列
from windget import getPrtConvertibleBondGrowthSeries


# 获取可转债市值增长率
from windget import getPrtConvertibleBondGrowth


# 获取资产支持证券市值时间序列
from windget import getPrtAbsValueSeries


# 获取资产支持证券市值
from windget import getPrtAbsValue


# 获取货币市场工具市值时间序列
from windget import getPrtMmIValueSeries


# 获取货币市场工具市值
from windget import getPrtMmIValue


# 获取其他债券市值时间序列
from windget import getPrtOtherBondSeries


# 获取其他债券市值
from windget import getPrtOtherBond


# 获取分行业投资市值时间序列
from windget import getPrtStockValueIndustry2Series


# 获取分行业投资市值
from windget import getPrtStockValueIndustry2


# 获取分行业投资市值(Wind全球行业)时间序列
from windget import getPrtGicSIndustryValueSeries


# 获取分行业投资市值(Wind全球行业)
from windget import getPrtGicSIndustryValue


# 获取分行业投资市值(Wind)时间序列
from windget import getPrtIndustryValueWindSeries


# 获取分行业投资市值(Wind)
from windget import getPrtIndustryValueWind


# 获取分行业投资市值(中信)时间序列
from windget import getPrtIndustryValueCitiCSeries


# 获取分行业投资市值(中信)
from windget import getPrtIndustryValueCitiC


# 获取分行业投资市值(申万)时间序列
from windget import getPrtIndustryValueSwSeries


# 获取分行业投资市值(申万)
from windget import getPrtIndustryValueSw


# 获取分行业市值增长率时间序列
from windget import getPrtStockValueIndustryValueGrowth2Series


# 获取分行业市值增长率
from windget import getPrtStockValueIndustryValueGrowth2


# 获取分行业市值增长率(Wind)时间序列
from windget import getPrtIndustryValueGrowthWindSeries


# 获取分行业市值增长率(Wind)
from windget import getPrtIndustryValueGrowthWind


# 获取分行业市值增长率(中信)时间序列
from windget import getPrtIndustryValueGrowthCitiCSeries


# 获取分行业市值增长率(中信)
from windget import getPrtIndustryValueGrowthCitiC


# 获取分行业市值增长率(申万)时间序列
from windget import getPrtIndustryValueGrowthSwSeries


# 获取分行业市值增长率(申万)
from windget import getPrtIndustryValueGrowthSw


# 获取重仓行业名称时间序列
from windget import getPrtStockValueTopIndustryName2Series


# 获取重仓行业名称
from windget import getPrtStockValueTopIndustryName2


# 获取重仓行业名称(Wind全球行业)时间序列
from windget import getPrtTopGicSIndustryNameSeries


# 获取重仓行业名称(Wind全球行业)
from windget import getPrtTopGicSIndustryName


# 获取重仓行业名称(Wind)时间序列
from windget import getPrtTopIndustryNameWindSeries


# 获取重仓行业名称(Wind)
from windget import getPrtTopIndustryNameWind


# 获取重仓行业名称(中信)时间序列
from windget import getPrtTopIndustryNameCitiCSeries


# 获取重仓行业名称(中信)
from windget import getPrtTopIndustryNameCitiC


# 获取重仓行业名称(申万)时间序列
from windget import getPrtTopIndustryNameSwSeries


# 获取重仓行业名称(申万)
from windget import getPrtTopIndustryNameSw


# 获取重仓行业代码时间序列
from windget import getPrtStockValueTopIndustrySymbol2Series


# 获取重仓行业代码
from windget import getPrtStockValueTopIndustrySymbol2


# 获取重仓行业市值时间序列
from windget import getPrtStockValueTopIndustryValue2Series


# 获取重仓行业市值
from windget import getPrtStockValueTopIndustryValue2


# 获取报告期末持有股票个数(中报、年报)时间序列
from windget import getPrtStockHoldingSeries


# 获取报告期末持有股票个数(中报、年报)
from windget import getPrtStockHolding


# 获取报告期不同持仓风格股票只数时间序列
from windget import getPrtShareNumStKhlDGStyleSeries


# 获取报告期不同持仓风格股票只数
from windget import getPrtShareNumStKhlDGStyle


# 获取重仓股股票名称时间序列
from windget import getPrtTopStockNameSeries


# 获取重仓股股票名称
from windget import getPrtTopStockName


# 获取重仓股股票代码时间序列
from windget import getPrtTopStockCodeSeries


# 获取重仓股股票代码
from windget import getPrtTopStockCode


# 获取最早重仓时间时间序列
from windget import getPrtTopStockDateSeries


# 获取最早重仓时间
from windget import getPrtTopStockDate


# 获取重仓股持股数量时间序列
from windget import getPrtTopStockQuantitySeries


# 获取重仓股持股数量
from windget import getPrtTopStockQuantity


# 获取重仓股持股市值时间序列
from windget import getPrtTopStockValueSeries


# 获取重仓股持股市值
from windget import getPrtTopStockValue


# 获取重仓股持仓变动时间序列
from windget import getPrtTopStockHoldingChangingSeries


# 获取重仓股持仓变动
from windget import getPrtTopStockHoldingChanging


# 获取重仓股持仓占流通股比例时间序列
from windget import getPrtTopProportionToFloatingSeries


# 获取重仓股持仓占流通股比例
from windget import getPrtTopProportionToFloating


# 获取重仓股票持有基金数时间序列
from windget import getPrtFundNoOfStocksSeries


# 获取重仓股票持有基金数
from windget import getPrtFundNoOfStocks


# 获取重仓股报告期重仓次数时间序列
from windget import getPrtTopStockHeldNoSeries


# 获取重仓股报告期重仓次数
from windget import getPrtTopStockHeldNo


# 获取报告期买入股票总成本时间序列
from windget import getPrtBuyStockCostSeries


# 获取报告期买入股票总成本
from windget import getPrtBuyStockCost


# 获取报告期卖出股票总收入时间序列
from windget import getPrtSellStockIncomeSeries


# 获取报告期卖出股票总收入
from windget import getPrtSellStockIncome


# 获取股票成交金额(分券商明细)时间序列
from windget import getPrtStockVolumeByBrokerSeries


# 获取股票成交金额(分券商明细)
from windget import getPrtStockVolumeByBroker


# 获取重仓债券名称时间序列
from windget import getPrtTopBondNameSeries


# 获取重仓债券名称
from windget import getPrtTopBondName


# 获取重仓债券代码时间序列
from windget import getPrtTopBondSymbolSeries


# 获取重仓债券代码
from windget import getPrtTopBondSymbol


# 获取重仓债券持仓数量时间序列
from windget import getPrtTopBondQuantitySeries


# 获取重仓债券持仓数量
from windget import getPrtTopBondQuantity


# 获取重仓债券持仓市值时间序列
from windget import getPrtTopBondValueSeries


# 获取重仓债券持仓市值
from windget import getPrtTopBondValue


# 获取重仓债券持仓变动时间序列
from windget import getPrtTopBondHoldingChangingSeries


# 获取重仓债券持仓变动
from windget import getPrtTopBondHoldingChanging


# 获取重仓债券持有基金数时间序列
from windget import getPrtFundNoOfBondsSeries


# 获取重仓债券持有基金数
from windget import getPrtFundNoOfBonds


# 获取重仓资产支持证券名称时间序列
from windget import getPrtTopAbsNameSeries


# 获取重仓资产支持证券名称
from windget import getPrtTopAbsName


# 获取重仓资产支持证券代码时间序列
from windget import getPrtTopAbsSymbolSeries


# 获取重仓资产支持证券代码
from windget import getPrtTopAbsSymbol


# 获取重仓资产支持证券持仓数量时间序列
from windget import getPrtTopAbsQuantitySeries


# 获取重仓资产支持证券持仓数量
from windget import getPrtTopAbsQuantity


# 获取重仓资产支持证券持有市值时间序列
from windget import getPrtTopAbsValueSeries


# 获取重仓资产支持证券持有市值
from windget import getPrtTopAbsValue


# 获取重仓资产支持证券持仓变动时间序列
from windget import getPrtTopAbsHoldingChangingSeries


# 获取重仓资产支持证券持仓变动
from windget import getPrtTopAbsHoldingChanging


# 获取重仓基金名称时间序列
from windget import getPrtTopFundNameSeries


# 获取重仓基金名称
from windget import getPrtTopFundName


# 获取重仓基金代码时间序列
from windget import getPrtTopFundCodeSeries


# 获取重仓基金代码
from windget import getPrtTopFundCode


# 获取重仓基金持仓数量时间序列
from windget import getPrtTopFundQuantitySeries


# 获取重仓基金持仓数量
from windget import getPrtTopFundQuantity


# 获取重仓基金持有市值时间序列
from windget import getPrtTopFundValueSeries


# 获取重仓基金持有市值
from windget import getPrtTopFundValue


# 获取重仓基金持仓变动时间序列
from windget import getPrtTopFundHoldingChangingSeries


# 获取重仓基金持仓变动
from windget import getPrtTopFundHoldingChanging


# 获取重仓基金持有基金数时间序列
from windget import getPrtFundNoOfFundsSeries


# 获取重仓基金持有基金数
from windget import getPrtFundNoOfFunds


# 获取报告期内偏离度的绝对值在0.25%(含)-0.5%间的次数时间序列
from windget import getMmFrequencyOfDeviationSeries


# 获取报告期内偏离度的绝对值在0.25%(含)-0.5%间的次数
from windget import getMmFrequencyOfDeviation


# 获取报告期内偏离度的最高值时间序列
from windget import getMmMaxDeviationSeries


# 获取报告期内偏离度的最高值
from windget import getMmMaxDeviation


# 获取报告期内偏离度的最低值时间序列
from windget import getMmmInDeviationSeries


# 获取报告期内偏离度的最低值
from windget import getMmmInDeviation


# 获取报告期内每个工作日偏离度的绝对值的简单平均值时间序列
from windget import getMmAvgDeviationSeries


# 获取报告期内每个工作日偏离度的绝对值的简单平均值
from windget import getMmAvgDeviation


# 获取资产估值时间序列
from windget import getFundReItsEValueSeries


# 获取资产估值
from windget import getFundReItsEValue


# 获取可供分配金额(预测)时间序列
from windget import getFundReItsDIsTrAmountFSeries


# 获取可供分配金额(预测)
from windget import getFundReItsDIsTrAmountF


# 获取派息率(预测)时间序列
from windget import getFundReItsDprFSeries


# 获取派息率(预测)
from windget import getFundReItsDprF


# 获取综合管理人员人数时间序列
from windget import getEmployeeAdminSeries


# 获取综合管理人员人数
from windget import getEmployeeAdmin


# 获取综合管理人员人数占比时间序列
from windget import getEmployeeAdminPctSeries


# 获取综合管理人员人数占比
from windget import getEmployeeAdminPct


# 获取综合成本率(产险)时间序列
from windget import getStmNoteInSur9Series


# 获取综合成本率(产险)
from windget import getStmNoteInSur9


# 获取综合偿付能力溢额时间序列
from windget import getQStmNoteInSur212507Series


# 获取综合偿付能力溢额
from windget import getQStmNoteInSur212507


# 获取综合偿付能力充足率时间序列
from windget import getQStmNoteInSur212508Series


# 获取综合偿付能力充足率
from windget import getQStmNoteInSur212508


# 获取综合流动比率:3个月内时间序列
from windget import getQStmNoteInSur212534Series


# 获取综合流动比率:3个月内
from windget import getQStmNoteInSur212534


# 获取综合流动比率:1年内时间序列
from windget import getQStmNoteInSur212535Series


# 获取综合流动比率:1年内
from windget import getQStmNoteInSur212535


# 获取综合流动比率:1年以上时间序列
from windget import getQStmNoteInSur212536Series


# 获取综合流动比率:1年以上
from windget import getQStmNoteInSur212536


# 获取综合流动比率:1-3年内时间序列
from windget import getQStmNoteInSur212537Series


# 获取综合流动比率:1-3年内
from windget import getQStmNoteInSur212537


# 获取综合流动比率:3-5年内时间序列
from windget import getQStmNoteInSur212538Series


# 获取综合流动比率:3-5年内
from windget import getQStmNoteInSur212538


# 获取综合流动比率:5年以上时间序列
from windget import getQStmNoteInSur212539Series


# 获取综合流动比率:5年以上
from windget import getQStmNoteInSur212539


# 获取综合收益_GSD时间序列
from windget import getWgsDComPrIncSeries


# 获取综合收益_GSD
from windget import getWgsDComPrInc


# 获取综合收益总额时间序列
from windget import getStm07IsReItsGeneralProfitSeries


# 获取综合收益总额
from windget import getStm07IsReItsGeneralProfit


# 获取市场综合3年评级时间序列
from windget import getRatingMarketAvgSeries


# 获取市场综合3年评级
from windget import getRatingMarketAvg


# 获取其他综合性收益_GSD时间序列
from windget import getWgsDComEqForExChSeries


# 获取其他综合性收益_GSD
from windget import getWgsDComEqForExCh


# 获取其他综合收益_BS时间序列
from windget import getOtherCompRehIncBsSeries


# 获取其他综合收益_BS
from windget import getOtherCompRehIncBs


# 获取其他综合收益时间序列
from windget import getOtherCompRehIncSeries


# 获取其他综合收益
from windget import getOtherCompRehInc


# 获取废水综合利用率时间序列
from windget import getEsGEwa01004Series


# 获取废水综合利用率
from windget import getEsGEwa01004


# 获取Wind综合评级时间序列
from windget import getRatingWindAvgSeries


# 获取Wind综合评级
from windget import getRatingWindAvg


# 获取单季度.综合收益_GSD时间序列
from windget import getWgsDQfaComPrIncSeries


# 获取单季度.综合收益_GSD
from windget import getWgsDQfaComPrInc


# 获取单季度.综合收益总额时间序列
from windget import getQfaToTCompRehIncSeries


# 获取单季度.综合收益总额
from windget import getQfaToTCompRehInc


# 获取最近一次风险综合评级类别时间序列
from windget import getQStmNoteInSur212529Series


# 获取最近一次风险综合评级类别
from windget import getQStmNoteInSur212529


# 获取归属普通股东综合收益_GSD时间序列
from windget import getWgsDCompRehIncParentCompSeries


# 获取归属普通股东综合收益_GSD
from windget import getWgsDCompRehIncParentComp


# 获取单季度.其他综合收益时间序列
from windget import getQfaOtherCompRehIncSeries


# 获取单季度.其他综合收益
from windget import getQfaOtherCompRehInc


# 获取租户认缴物业维护综合费_GSD时间序列
from windget import getWgsDTenantReImExpSeries


# 获取租户认缴物业维护综合费_GSD
from windget import getWgsDTenantReImExp


# 获取归属于少数股东的综合收益总额时间序列
from windget import getToTCompRehIncMinSHrhLDrSeries


# 获取归属于少数股东的综合收益总额
from windget import getToTCompRehIncMinSHrhLDr


# 获取Wind ESG综合得分时间序列
from windget import getEsGScoreWindSeries


# 获取Wind ESG综合得分
from windget import getEsGScoreWind


# 获取上海证券3年评级(综合评级)时间序列
from windget import getRatingShanghaiOverall3YSeries


# 获取上海证券3年评级(综合评级)
from windget import getRatingShanghaiOverall3Y


# 获取上海证券5年评级(综合评级)时间序列
from windget import getRatingShanghaiOverall5YSeries


# 获取上海证券5年评级(综合评级)
from windget import getRatingShanghaiOverall5Y


# 获取单季度.归属普通股东综合收益_GSD时间序列
from windget import getWgsDQfaCompRehIncParentCompSeries


# 获取单季度.归属普通股东综合收益_GSD
from windget import getWgsDQfaCompRehIncParentComp


# 获取归属于母公司普通股东综合收益总额时间序列
from windget import getToTCompRehIncParentCompSeries


# 获取归属于母公司普通股东综合收益总额
from windget import getToTCompRehIncParentComp


# 获取单季度.租户认缴物业维护综合费_GSD时间序列
from windget import getWgsDQfaTenantReImExpSeries


# 获取单季度.租户认缴物业维护综合费_GSD
from windget import getWgsDQfaTenantReImExp


# 获取单季度.归属于少数股东的综合收益总额时间序列
from windget import getQfaToTCompRehIncMinSHrhLDrSeries


# 获取单季度.归属于少数股东的综合收益总额
from windget import getQfaToTCompRehIncMinSHrhLDr


# 获取单季度.归属于母公司普通股东综合收益总额时间序列
from windget import getQfaToTCompRehIncParentCompSeries


# 获取单季度.归属于母公司普通股东综合收益总额
from windget import getQfaToTCompRehIncParentComp


# 获取以公允价值计量且其变动计入其他综合收益的金融资产时间序列
from windget import getFinAssetsChgCompRehIncSeries


# 获取以公允价值计量且其变动计入其他综合收益的金融资产
from windget import getFinAssetsChgCompRehInc


# 获取社会保险费:本期增加时间序列
from windget import getStmNoteSocialSecurityAddSeries


# 获取社会保险费:本期增加
from windget import getStmNoteSocialSecurityAdd


# 获取社会保险费:期初余额时间序列
from windget import getStmNoteSocialSecuritySbSeries


# 获取社会保险费:期初余额
from windget import getStmNoteSocialSecuritySb


# 获取社会保险费:期末余额时间序列
from windget import getStmNoteSocialSecurityEbSeries


# 获取社会保险费:期末余额
from windget import getStmNoteSocialSecurityEb


# 获取社会保险费:本期减少时间序列
from windget import getStmNoteSocialSecurityDeSeries


# 获取社会保险费:本期减少
from windget import getStmNoteSocialSecurityDe


# 获取社会价值投资联盟ESG评级时间序列
from windget import getEsGRatingCasViSeries


# 获取社会价值投资联盟ESG评级
from windget import getEsGRatingCasVi


# 获取统一社会信用代码时间序列
from windget import getRegisterNumberSeries


# 获取统一社会信用代码
from windget import getRegisterNumber


# 获取公司是否有独立的公司社会责任报告时间序列
from windget import getEsGMdc01002Series


# 获取公司是否有独立的公司社会责任报告
from windget import getEsGMdc01002


# 获取(停止)银河1年评级时间序列
from windget import getRatingYinHe1YSeries


# 获取(停止)银河1年评级
from windget import getRatingYinHe1Y


# 获取(停止)银河2年评级时间序列
from windget import getRatingYinHe2YSeries


# 获取(停止)银河2年评级
from windget import getRatingYinHe2Y


# 获取(停止)招商3年评级时间序列
from windget import getRatingZhaoShang3YSeries


# 获取(停止)招商3年评级
from windget import getRatingZhaoShang3Y


# 获取(停止)海通3年评级时间序列
from windget import getRatingHaiTong3YSeries


# 获取(停止)海通3年评级
from windget import getRatingHaiTong3Y


# 获取(停止)投资风格时间序列
from windget import getFundInvestStyleSeries


# 获取(停止)投资风格
from windget import getFundInvestStyle


# 获取(停止)所属国信行业名称时间序列
from windget import getIndustryGxSeries


# 获取(停止)所属国信行业名称
from windget import getIndustryGx


# 获取(停止)债券评分时间序列
from windget import getBondScoreSeries


# 获取(停止)债券评分
from windget import getBondScore


# 获取(停止)发行人评分时间序列
from windget import getIssuersCoreSeries


# 获取(停止)发行人评分
from windget import getIssuersCore


# 获取(停止)公司一句话介绍时间序列
from windget import getAbstractSeries


# 获取(停止)公司一句话介绍
from windget import getAbstract


# 获取(废弃)任职基金几何总回报时间序列
from windget import getFundManagerTotalGeometricReturnSeries


# 获取(废弃)任职基金几何总回报
from windget import getFundManagerTotalGeometricReturn


# 获取(废弃)净值价格时间序列
from windget import getFellowNetPriceSeries


# 获取(废弃)净值价格
from windget import getFellowNetPrice


# 获取(废弃)估值来源时间序列
from windget import getDefaultSourceSeries


# 获取(废弃)估值来源
from windget import getDefaultSource


# 获取(废弃)区间理论价时间序列
from windget import getTheOPricePerSeries


# 获取(废弃)区间理论价
from windget import getTheOPricePer


# 获取(废弃)基金投资收益时间序列
from windget import getStmIs83Series


# 获取(废弃)基金投资收益
from windget import getStmIs83


# 获取(废弃)累计关注人数_雪球时间序列
from windget import getXQACcmFocusSeries


# 获取(废弃)累计关注人数_雪球
from windget import getXQACcmFocus


# 获取(废弃)累计讨论次数_雪球时间序列
from windget import getXQACcmCommentsSeries


# 获取(废弃)累计讨论次数_雪球
from windget import getXQACcmComments


# 获取(废弃)累计交易分享数_雪球时间序列
from windget import getXQACcmSharesSeries


# 获取(废弃)累计交易分享数_雪球
from windget import getXQACcmShares


# 获取(废弃)一周新增关注_雪球时间序列
from windget import getXQFocusAddedSeries


# 获取(废弃)一周新增关注_雪球
from windget import getXQFocusAdded


# 获取(废弃)一周新增讨论数_雪球时间序列
from windget import getXQCommentsAddedSeries


# 获取(废弃)一周新增讨论数_雪球
from windget import getXQCommentsAdded


# 获取(废弃)一周新增交易分享数_雪球时间序列
from windget import getXQSharesAddedSeries


# 获取(废弃)一周新增交易分享数_雪球
from windget import getXQSharesAdded


# 获取(废弃)一周关注增长率_雪球时间序列
from windget import getXQWowFocusSeries


# 获取(废弃)一周关注增长率_雪球
from windget import getXQWowFocus


# 获取(废弃)一周讨论增长率_雪球时间序列
from windget import getXQWowCommentsSeries


# 获取(废弃)一周讨论增长率_雪球
from windget import getXQWowComments


# 获取(废弃)一周交易分享增长率_雪球时间序列
from windget import getXQWowSharesSeries


# 获取(废弃)一周交易分享增长率_雪球
from windget import getXQWowShares


# 获取(废弃)大股东类型时间序列
from windget import getShareCategorySeries


# 获取(废弃)大股东类型
from windget import getShareCategory


# 获取(废弃)所属证监会行业名称时间序列
from windget import getIndustryCsrC12Series


# 获取(废弃)所属证监会行业名称
from windget import getIndustryCsrC12


# 获取年度现金分红比例(沪深)时间序列
from windget import getDivPayOutRatioSeries


# 获取年度现金分红比例(沪深)
from windget import getDivPayOutRatio


# 获取非流通股(沪深)时间序列
from windget import getShareNonTradableSeries


# 获取非流通股(沪深)
from windget import getShareNonTradable


# 获取估价收益率(中证指数)(旧)时间序列
from windget import getYieldCsiSeries


# 获取估价收益率(中证指数)(旧)
from windget import getYieldCsi


# 获取估价净价(中证指数)(旧)时间序列
from windget import getNetCsiSeries


# 获取估价净价(中证指数)(旧)
from windget import getNetCsi


# 获取估价全价(中证指数)(旧)时间序列
from windget import getDirtyCsiSeries


# 获取估价全价(中证指数)(旧)
from windget import getDirtyCsi


# 获取估价修正久期(中证指数)(旧)时间序列
from windget import getModiDuraCsiSeries


# 获取估价修正久期(中证指数)(旧)
from windget import getModiDuraCsi


# 获取估价凸性(中证指数)(旧)时间序列
from windget import getCNvXTyCsiSeries


# 获取估价凸性(中证指数)(旧)
from windget import getCNvXTyCsi


# 获取首发募集资金净额(旧)时间序列
from windget import getIpoNetCollectionSeries


# 获取首发募集资金净额(旧)
from windget import getIpoNetCollection


# 获取首发价格(旧)时间序列
from windget import getIpoPriceSeries


# 获取首发价格(旧)
from windget import getIpoPrice


# 获取首发预计募集资金(旧)时间序列
from windget import getIpoExpectedCollectionSeries


# 获取首发预计募集资金(旧)
from windget import getIpoExpectedCollection


# 获取股东售股金额(旧)时间序列
from windget import getIpoCollectionOldSharesSeries


# 获取股东售股金额(旧)
from windget import getIpoCollectionOldShares


# 获取首发承销保荐费用(旧)时间序列
from windget import getIpoUsFeesSeries


# 获取首发承销保荐费用(旧)
from windget import getIpoUsFees


# 获取(废弃)是否费率优惠时间序列
from windget import getFundFeeDiscountOrNotSeries


# 获取(废弃)是否费率优惠
from windget import getFundFeeDiscountOrNot


# 获取(废弃)最低申购折扣费率时间序列
from windget import getFundMinPurchaseDiscountsSeries


# 获取(废弃)最低申购折扣费率
from windget import getFundMinPurchaseDiscounts


# 获取(废弃)最低定投折扣率时间序列
from windget import getFundMinaIpDiscountsSeries


# 获取(废弃)最低定投折扣率
from windget import getFundMinaIpDiscounts


# 获取(废弃)兼职人员比例时间序列
from windget import getEsGSem01003Series


# 获取(废弃)兼职人员比例
from windget import getEsGSem01003


# 获取(废弃)市盈率百分位时间序列
from windget import getValPepSeries


# 获取(废弃)市盈率百分位
from windget import getValPep


# 获取(废弃)基金盈利概率时间序列
from windget import getNavWinLossRatioSeries


# 获取(废弃)基金盈利概率
from windget import getNavWinLossRatio


# 获取(废弃)基金到期日时间序列
from windget import getFundMaturityDateSeries


# 获取(废弃)基金到期日
from windget import getFundMaturityDate


# 获取(废弃)成立日期时间序列
from windget import getFoundDateSeries


# 获取(废弃)成立日期
from windget import getFoundDate


# 获取(废弃)主办券商(持续督导)时间序列
from windget import getIpoLeadUndRNSeries


# 获取(废弃)主办券商(持续督导)
from windget import getIpoLeadUndRN


# 获取(废弃)公司独立董事(历任)时间序列
from windget import getFrMindPDirectorSeries


# 获取(废弃)公司独立董事(历任)
from windget import getFrMindPDirector


# 获取证券简称时间序列
from windget import getSecNameSeries


# 获取证券简称
from windget import getSecName


# 获取证券简称(支持历史)时间序列
from windget import getSecName1Series


# 获取证券简称(支持历史)
from windget import getSecName1


# 获取证券英文简称时间序列
from windget import getSecEnglishnameSeries


# 获取证券英文简称
from windget import getSecEnglishname


# 获取上市日期时间序列
from windget import getIpoDateSeries


# 获取上市日期
from windget import getIpoDate


# 获取借壳上市日期时间序列
from windget import getBackdoorDateSeries


# 获取借壳上市日期
from windget import getBackdoorDate


# 获取ETF上市日期时间序列
from windget import getFundEtFListedDateSeries


# 获取ETF上市日期
from windget import getFundEtFListedDate


# 获取REITs上市日期时间序列
from windget import getFundReItsListedDateSeries


# 获取REITs上市日期
from windget import getFundReItsListedDate


# 获取网下配售部分上市日期时间序列
from windget import getIpoJurisDateSeries


# 获取网下配售部分上市日期
from windget import getIpoJurisDate


# 获取向战略投资者配售部分上市日期时间序列
from windget import getIpoInStIsDateSeries


# 获取向战略投资者配售部分上市日期
from windget import getIpoInStIsDate


# 获取向机构投资者增发部分上市日期时间序列
from windget import getFellowInStListDateSeries


# 获取向机构投资者增发部分上市日期
from windget import getFellowInStListDate


# 获取交易所中文名称时间序列
from windget import getExchangeCnSeries


# 获取交易所中文名称
from windget import getExchangeCn


# 获取交易所英文简称时间序列
from windget import getExChEngSeries


# 获取交易所英文简称
from windget import getExChEng


# 获取上市板时间序列
from windget import getMktSeries


# 获取上市板
from windget import getMkt


# 获取证券存续状态时间序列
from windget import getSecStatusSeries


# 获取证券存续状态
from windget import getSecStatus


# 获取戴帽摘帽时间时间序列
from windget import getRiskAdmonitionDateSeries


# 获取戴帽摘帽时间
from windget import getRiskAdmonitionDate


# 获取摘牌日期时间序列
from windget import getDeListDateSeries


# 获取摘牌日期
from windget import getDeListDate


# 获取发行币种时间序列
from windget import getIssueCurrencyCodeSeries


# 获取发行币种
from windget import getIssueCurrencyCode


# 获取交易币种时间序列
from windget import getCurRSeries


# 获取交易币种
from windget import getCurR


# 获取B股市值(含限售股,交易币种)时间序列
from windget import getValBsHrMarketValue4Series


# 获取B股市值(含限售股,交易币种)
from windget import getValBsHrMarketValue4


# 获取B股市值(不含限售股,交易币种)时间序列
from windget import getValBsHrMarketValue2Series


# 获取B股市值(不含限售股,交易币种)
from windget import getValBsHrMarketValue2


# 获取交易结算模式时间序列
from windget import getFundSettlementModeSeries


# 获取交易结算模式
from windget import getFundSettlementMode


# 获取每股面值时间序列
from windget import getParValueSeries


# 获取每股面值
from windget import getParValue


# 获取发行时每股面值时间序列
from windget import getIpoParSeries


# 获取发行时每股面值
from windget import getIpoPar


# 获取每手股数时间序列
from windget import getLotSizeSeries


# 获取每手股数
from windget import getLotSize


# 获取交易单位时间序列
from windget import getTunItSeries


# 获取交易单位
from windget import getTunIt


# 获取所属国家或地区代码时间序列
from windget import getCountrySeries


# 获取所属国家或地区代码
from windget import getCountry


# 获取基期时间序列
from windget import getBaseDateSeries


# 获取基期
from windget import getBaseDate


# 获取基点时间序列
from windget import getBaseValueSeries


# 获取基点
from windget import getBaseValue


# 获取基点价值时间序列
from windget import getCalcPvbPSeries


# 获取基点价值
from windget import getCalcPvbP


# 获取估价基点价值(中债)时间序列
from windget import getVoBpCnBdSeries


# 获取估价基点价值(中债)
from windget import getVoBpCnBd


# 获取估价基点价值(上清所)时间序列
from windget import getVoBpShcSeries


# 获取估价基点价值(上清所)
from windget import getVoBpShc


# 获取平均基点价值时间序列
from windget import getAnalBasePointValueSeries


# 获取平均基点价值
from windget import getAnalBasePointValue


# 获取行权基点价值时间序列
from windget import getBaseValueIfExeSeries


# 获取行权基点价值
from windget import getBaseValueIfExe


# 获取计算浮息债隐含加息基点时间序列
from windget import getCalcFloatAddBpSeries


# 获取计算浮息债隐含加息基点
from windget import getCalcFloatAddBp


# 获取成份个数时间序列
from windget import getNumberOfConstituentsSeries


# 获取成份个数
from windget import getNumberOfConstituents


# 获取成份个数(支持历史)时间序列
from windget import getNumberOfConstituents2Series


# 获取成份个数(支持历史)
from windget import getNumberOfConstituents2


# 获取最早成份日期时间序列
from windget import getFirstDayOfConstituentsSeries


# 获取最早成份日期
from windget import getFirstDayOfConstituents


# 获取加权方式时间序列
from windget import getMethodologySeries


# 获取加权方式
from windget import getMethodology


# 获取证券简介时间序列
from windget import getRepoBriefingSeries


# 获取证券简介
from windget import getRepoBriefing


# 获取发布日期时间序列
from windget import getLaunchDateSeries


# 获取发布日期
from windget import getLaunchDate


# 获取证券曾用名时间序列
from windget import getPreNameSeries


# 获取证券曾用名
from windget import getPreName


# 获取上市地点时间序列
from windget import getExChCitySeries


# 获取上市地点
from windget import getExChCity


# 获取跟踪标的基金代码时间序列
from windget import getTrackedByFundsSeries


# 获取跟踪标的基金代码
from windget import getTrackedByFunds


# 获取上级行业指数代码时间序列
from windget import getSuperiorCodeSeries


# 获取上级行业指数代码
from windget import getSuperiorCode


# 获取证券代码时间序列
from windget import getTradeCodeSeries


# 获取证券代码
from windget import getTradeCode


# 获取证券代码变更日期时间序列
from windget import getCodeChangeDateSeries


# 获取证券代码变更日期
from windget import getCodeChangeDate


# 获取主证券代码时间序列
from windget import getAnchorBondSeries


# 获取主证券代码
from windget import getAnchorBond


# 获取主指数代码时间序列
from windget import getMajorIndexCodeSeries


# 获取主指数代码
from windget import getMajorIndexCode


# 获取副指数代码时间序列
from windget import getSubIndexCodeSeries


# 获取副指数代码
from windget import getSubIndexCode


# 获取跨市场代码时间序列
from windget import getRelationCodeSeries


# 获取跨市场代码
from windget import getRelationCode


# 获取公司债对应上市公司代码时间序列
from windget import getBcLcSeries


# 获取公司债对应上市公司代码
from windget import getBcLc


# 获取中债招标发行代码时间序列
from windget import getTendRstCodeSeries


# 获取中债招标发行代码
from windget import getTendRstCode


# 获取深交所分销代码时间序列
from windget import getSzSeDistRibCodeSeries


# 获取深交所分销代码
from windget import getSzSeDistRibCode


# 获取同公司可转债简称时间序列
from windget import getCbNameSeries


# 获取同公司可转债简称
from windget import getCbName


# 获取同公司美股简称时间序列
from windget import getUsShareNameSeries


# 获取同公司美股简称
from windget import getUsShareName


# 获取股票种类时间序列
from windget import getStockClassSeries


# 获取股票种类
from windget import getStockClass


# 获取发行制度时间序列
from windget import getIpoIssuingSystemSeries


# 获取发行制度
from windget import getIpoIssuingSystem


# 获取所属上市标准时间序列
from windget import getListsTdSeries


# 获取所属上市标准
from windget import getListsTd


# 获取北交所准入标准时间序列
from windget import getFeaturedListsTdSeries


# 获取北交所准入标准
from windget import getFeaturedListsTd


# 获取是否属于重要指数成份时间序列
from windget import getCompIndex2Series


# 获取是否属于重要指数成份
from windget import getCompIndex2


# 获取所属概念板块时间序列
from windget import getConceptSeries


# 获取所属概念板块
from windget import getConcept


# 获取所属规模风格类型时间序列
from windget import getScaleStyleSeries


# 获取所属规模风格类型
from windget import getScaleStyle


# 获取是否沪港通买入标的时间序列
from windget import getShScSeries


# 获取是否沪港通买入标的
from windget import getShSc


# 获取是否深港通买入标的时间序列
from windget import getShSc2Series


# 获取是否深港通买入标的
from windget import getShSc2


# 获取是否并行代码时间序列
from windget import getParallelCodeSeries


# 获取是否并行代码
from windget import getParallelCode


# 获取证券类型时间序列
from windget import getSecTypeSeries


# 获取证券类型
from windget import getSecType


# 获取是否借壳上市时间序列
from windget import getBackdoorSeries


# 获取是否借壳上市
from windget import getBackdoor


# 获取是否上市时间序列
from windget import getListSeries


# 获取是否上市
from windget import getList


# 获取是否上市公司时间序列
from windget import getListingOrNotSeries


# 获取是否上市公司
from windget import getListingOrNot


# 获取是否属于风险警示板时间序列
from windget import getRiskWarningSeries


# 获取是否属于风险警示板
from windget import getRiskWarning


# 获取指数风格时间序列
from windget import getOfficialStyleSeries


# 获取指数风格
from windget import getOfficialStyle


# 获取所属产业链板块时间序列
from windget import getChainSeries


# 获取所属产业链板块
from windget import getChain


# 获取所属大宗商品概念板块时间序列
from windget import getLargeCommoditySeries


# 获取所属大宗商品概念板块
from windget import getLargeCommodity


# 获取存托机构时间序列
from windget import getDepositAryBankSeries


# 获取存托机构
from windget import getDepositAryBank


# 获取主办券商(持续督导)时间序列
from windget import getIpoLeadUndRN1Series


# 获取主办券商(持续督导)
from windget import getIpoLeadUndRN1


# 获取做市商名称时间序列
from windget import getIpoMarketMakerSeries


# 获取做市商名称
from windget import getIpoMarketMaker


# 获取做市首日时间序列
from windget import getMarketMakeDateSeries


# 获取做市首日
from windget import getMarketMakeDate


# 获取交易类型时间序列
from windget import getTransferTypeSeries


# 获取交易类型
from windget import getTransferType


# 获取做市商家数时间序列
from windget import getNeEqMarketMakerNumSeries


# 获取做市商家数
from windget import getNeEqMarketMakerNum


# 获取挂牌园区时间序列
from windget import getNeEqParkSeries


# 获取挂牌园区
from windget import getNeEqPark


# 获取挂牌公告日时间序列
from windget import getNeEqListAnnDateSeries


# 获取挂牌公告日
from windget import getNeEqListAnnDate


# 获取转做市公告日时间序列
from windget import getNeEqMarketMakeAnnDateSeries


# 获取转做市公告日
from windget import getNeEqMarketMakeAnnDate


# 获取所属挂牌公司投资型行业名称时间序列
from windget import getIndustryNeeQgIcsSeries


# 获取所属挂牌公司投资型行业名称
from windget import getIndustryNeeQgIcs


# 获取所属挂牌公司投资型行业代码时间序列
from windget import getIndustryNeeQgIcsCodeInvSeries


# 获取所属挂牌公司投资型行业代码
from windget import getIndustryNeeQgIcsCodeInv


# 获取所属挂牌公司投资型行业板块代码时间序列
from windget import getIndustryNeeQgIcsCodeSeries


# 获取所属挂牌公司投资型行业板块代码
from windget import getIndustryNeeQgIcsCode


# 获取所属新三板概念类板块时间序列
from windget import getIndustryNeEqConceptSeries


# 获取所属新三板概念类板块
from windget import getIndustryNeEqConcept


# 获取所属分层时间序列
from windget import getNeEqLevelSeries


# 获取所属分层
from windget import getNeEqLevel


# 获取所属创新层标准时间序列
from windget import getNeEqStandardSeries


# 获取所属创新层标准
from windget import getNeEqStandard


# 获取挂牌企业上市辅导券商时间序列
from windget import getIpoTutorSeries


# 获取挂牌企业上市辅导券商
from windget import getIpoTutor


# 获取挂牌企业上市辅导开始日期时间序列
from windget import getIpoTutoringStartDateSeries


# 获取挂牌企业上市辅导开始日期
from windget import getIpoTutoringStartDate


# 获取挂牌企业上市辅导结束日期时间序列
from windget import getIpoTutoringEnddateSeries


# 获取挂牌企业上市辅导结束日期
from windget import getIpoTutoringEnddate


# 获取挂牌日时间序列
from windget import getNeEqListingDateSeries


# 获取挂牌日
from windget import getNeEqListingDate


# 获取创新层挂牌日时间序列
from windget import getNeEqListDateInnovationLevelSeries


# 获取创新层挂牌日
from windget import getNeEqListDateInnovationLevel


# 获取挂牌公司转板北交所前停牌日时间序列
from windget import getNeEqSuspensionDaySeries


# 获取挂牌公司转板北交所前停牌日
from windget import getNeEqSuspensionDay


# 获取公司中文名称时间序列
from windget import getCompNameSeries


# 获取公司中文名称
from windget import getCompName


# 获取公司英文名称时间序列
from windget import getCompNameEngSeries


# 获取公司英文名称
from windget import getCompNameEng


# 获取公司属性时间序列
from windget import getNature1Series


# 获取公司属性
from windget import getNature1


# 获取公司属性(旧)时间序列
from windget import getNatureSeries


# 获取公司属性(旧)
from windget import getNature


# 获取股东公司属性时间序列
from windget import getShareholderNatureSeries


# 获取股东公司属性
from windget import getShareholderNature


# 获取担保人公司属性时间序列
from windget import getAgencyGuarantorNatureSeries


# 获取担保人公司属性
from windget import getAgencyGuarantorNature


# 获取金融机构类型时间序列
from windget import getInstitutionTypeSeries


# 获取金融机构类型
from windget import getInstitutionType


# 获取企业规模时间序列
from windget import getCorpScaleSeries


# 获取企业规模
from windget import getCorpScale


# 获取上市公司(银行)类型时间序列
from windget import getBankTypeSeries


# 获取上市公司(银行)类型
from windget import getBankType


# 获取成立日期时间序列
from windget import getFoundDate1Series


# 获取成立日期
from windget import getFoundDate1


# 获取基金管理人成立日期时间序列
from windget import getFundCorpEstablishmentDateSeries


# 获取基金管理人成立日期
from windget import getFundCorpEstablishmentDate


# 获取注册资本时间序列
from windget import getRegCapitalSeries


# 获取注册资本
from windget import getRegCapital


# 获取注册资本币种时间序列
from windget import getRegCapitalCurSeries


# 获取注册资本币种
from windget import getRegCapitalCur


# 获取基金管理人注册资本时间序列
from windget import getFundCorpRegisteredCapitalSeries


# 获取基金管理人注册资本
from windget import getFundCorpRegisteredCapital


# 获取法定代表人时间序列
from windget import getChairmanSeries


# 获取法定代表人
from windget import getChairman


# 获取法定代表人(支持历史)时间序列
from windget import getLegalRepresentativeSeries


# 获取法定代表人(支持历史)
from windget import getLegalRepresentative


# 获取会计年结日时间序列
from windget import getFiscalDateSeries


# 获取会计年结日
from windget import getFiscalDate


# 获取经营范围时间序列
from windget import getBusinessSeries


# 获取经营范围
from windget import getBusiness


# 获取公司简介时间序列
from windget import getBriefingSeries


# 获取公司简介
from windget import getBriefing


# 获取股东公司简介时间序列
from windget import getShareholderBriefingSeries


# 获取股东公司简介
from windget import getShareholderBriefing


# 获取担保人公司简介时间序列
from windget import getAgencyGuarantorBriefingSeries


# 获取担保人公司简介
from windget import getAgencyGuarantorBriefing


# 获取主营产品类型时间序列
from windget import getMajorProductTypeSeries


# 获取主营产品类型
from windget import getMajorProductType


# 获取主营产品名称时间序列
from windget import getMajorProductNameSeries


# 获取主营产品名称
from windget import getMajorProductName


# 获取员工总数时间序列
from windget import getEmployeeSeries


# 获取员工总数
from windget import getEmployee


# 获取母公司员工人数时间序列
from windget import getEmployeePcSeries


# 获取母公司员工人数
from windget import getEmployeePc


# 获取所属行政区划时间序列
from windget import getAdministrativeDivisionSeries


# 获取所属行政区划
from windget import getAdministrativeDivision


# 获取所属行政区划代码时间序列
from windget import getAdminCodeSeries


# 获取所属行政区划代码
from windget import getAdminCode


# 获取所属证监会辖区时间序列
from windget import getCsrCJurisdictionSeries


# 获取所属证监会辖区
from windget import getCsrCJurisdiction


# 获取省份时间序列
from windget import getProvinceSeries


# 获取省份
from windget import getProvince


# 获取城市时间序列
from windget import getCitySeries


# 获取城市
from windget import getCity


# 获取基金管理人注册城市时间序列
from windget import getFundCorpCitySeries


# 获取基金管理人注册城市
from windget import getFundCorpCity


# 获取注册地址时间序列
from windget import getAddressSeries


# 获取注册地址
from windget import getAddress


# 获取基金管理人注册地址时间序列
from windget import getFundCorpAddressSeries


# 获取基金管理人注册地址
from windget import getFundCorpAddress


# 获取办公地址时间序列
from windget import getOfficeSeries


# 获取办公地址
from windget import getOffice


# 获取基金管理人办公地址时间序列
from windget import getFundCorpOfficeSeries


# 获取基金管理人办公地址
from windget import getFundCorpOffice


# 获取邮编时间序列
from windget import getZipCodeSeries


# 获取邮编
from windget import getZipCode


# 获取基金管理人邮编时间序列
from windget import getFundCorpZipSeries


# 获取基金管理人邮编
from windget import getFundCorpZip


# 获取公司电话时间序列
from windget import getPhoneSeries


# 获取公司电话
from windget import getPhone


# 获取公司传真时间序列
from windget import getFaxSeries


# 获取公司传真
from windget import getFax


# 获取公司电子邮件地址时间序列
from windget import getEmailSeries


# 获取公司电子邮件地址
from windget import getEmail


# 获取公司网站时间序列
from windget import getWebsiteSeries


# 获取公司网站
from windget import getWebsite


# 获取信息披露人时间序列
from windget import getDIsCloserSeries


# 获取信息披露人
from windget import getDIsCloser


# 获取信息指定披露媒体时间序列
from windget import getMediaSeries


# 获取信息指定披露媒体
from windget import getMedia


# 获取组织机构代码时间序列
from windget import getOrganizationCodeSeries


# 获取组织机构代码
from windget import getOrganizationCode


# 获取记账本位币时间序列
from windget import getReportCurSeries


# 获取记账本位币
from windget import getReportCur


# 获取发行人中文简称时间序列
from windget import getIssuerShortenedSeries


# 获取发行人中文简称
from windget import getIssuerShortened


# 获取主要产品及业务时间序列
from windget import getMainProductSeries


# 获取主要产品及业务
from windget import getMainProduct


# 获取公司曾用名时间序列
from windget import getCompPreNameSeries


# 获取公司曾用名
from windget import getCompPreName


# 获取是否发行可转债时间序列
from windget import getCbIssueOrNotSeries


# 获取是否发行可转债
from windget import getCbIssueOrNot


# 获取是否存在投票权差异时间序列
from windget import getVoteSeries


# 获取是否存在投票权差异
from windget import getVote


# 获取所属战略性新兴产业分类时间序列
from windget import getSeiSeries


# 获取所属战略性新兴产业分类
from windget import getSei


# 获取是否专精特新企业时间序列
from windget import getZJtXorNotSeries


# 获取是否专精特新企业
from windget import getZJtXorNot


# 获取所属证监会行业名称时间序列
from windget import getIndustryCsrC12NSeries


# 获取所属证监会行业名称
from windget import getIndustryCsrC12N


# 获取所属证监会行业名称(旧)时间序列
from windget import getIndustryCsrCSeries


# 获取所属证监会行业名称(旧)
from windget import getIndustryCsrC


# 获取所属证监会行业代码时间序列
from windget import getIndustryCsrCCode12Series


# 获取所属证监会行业代码
from windget import getIndustryCsrCCode12


# 获取所属证监会行业代码(旧)时间序列
from windget import getIndustryCsrCCodeSeries


# 获取所属证监会行业代码(旧)
from windget import getIndustryCsrCCode


# 获取所属申万行业名称时间序列
from windget import getIndustrySwSeries


# 获取所属申万行业名称
from windget import getIndustrySw


# 获取所属申万行业名称(2021)时间序列
from windget import getIndustrySw2021Series


# 获取所属申万行业名称(2021)
from windget import getIndustrySw2021


# 获取所属申万行业名称(港股)时间序列
from windget import getIndustrySwHkSeries


# 获取所属申万行业名称(港股)
from windget import getIndustrySwHk


# 获取所属申万行业名称(港股)(2021)时间序列
from windget import getIndustrySw2021HkSeries


# 获取所属申万行业名称(港股)(2021)
from windget import getIndustrySw2021Hk


# 获取所属申万行业代码时间序列
from windget import getIndustrySwCodeSeries


# 获取所属申万行业代码
from windget import getIndustrySwCode


# 获取所属申万行业代码(2021)时间序列
from windget import getIndustrySwCode2021Series


# 获取所属申万行业代码(2021)
from windget import getIndustrySwCode2021


# 获取所属申万行业代码(港股)时间序列
from windget import getIndustrySwCodeHkSeries


# 获取所属申万行业代码(港股)
from windget import getIndustrySwCodeHk


# 获取所属申万行业代码(港股)(2021)时间序列
from windget import getIndustrySwCode2021HkSeries


# 获取所属申万行业代码(港股)(2021)
from windget import getIndustrySwCode2021Hk


# 获取所属申万行业原始代码时间序列
from windget import getIndustrySwOriginCodeSeries


# 获取所属申万行业原始代码
from windget import getIndustrySwOriginCode


# 获取所属申万行业原始代码(2021)时间序列
from windget import getIndustrySwOriginCode2021Series


# 获取所属申万行业原始代码(2021)
from windget import getIndustrySwOriginCode2021


# 获取所属申万行业指数代码时间序列
from windget import getIndexCodeSwSeries


# 获取所属申万行业指数代码
from windget import getIndexCodeSw


# 获取所属中信行业名称时间序列
from windget import getIndustryCitiCSeries


# 获取所属中信行业名称
from windget import getIndustryCitiC


# 获取所属中信行业名称(港股)时间序列
from windget import getIndustryCitiCHkSeries


# 获取所属中信行业名称(港股)
from windget import getIndustryCitiCHk


# 获取所属中信行业代码时间序列
from windget import getIndustryCitiCCodeSeries


# 获取所属中信行业代码
from windget import getIndustryCitiCCode


# 获取所属中信行业代码(港股)时间序列
from windget import getIndustryCitiCCodeHkSeries


# 获取所属中信行业代码(港股)
from windget import getIndustryCitiCCodeHk


# 获取所属中信行业指数代码时间序列
from windget import getIndexCodeCitiCSeries


# 获取所属中信行业指数代码
from windget import getIndexCodeCitiC


# 获取所属中信证券港股通指数代码(港股)时间序列
from windget import getIndexCodeCitiCHkSeries


# 获取所属中信证券港股通指数代码(港股)
from windget import getIndexCodeCitiCHk


# 获取所属中信证券港股通指数名称(港股)时间序列
from windget import getIndexNameCitiCHkSeries


# 获取所属中信证券港股通指数名称(港股)
from windget import getIndexNameCitiCHk


# 获取所属中诚信行业名称时间序列
from windget import getIssuerIndustryCcXiSeries


# 获取所属中诚信行业名称
from windget import getIssuerIndustryCcXi


# 获取废弃行业时间序列
from windget import getIndustryGicS2Series


# 获取废弃行业
from windget import getIndustryGicS2


# 获取所属恒生行业名称时间序列
from windget import getIndustryHsSeries


# 获取所属恒生行业名称
from windget import getIndustryHs


# 获取所属行业名称(支持历史)时间序列
from windget import getIndustry2Series


# 获取所属行业名称(支持历史)
from windget import getIndustry2


# 获取所属行业代码(支持历史)时间序列
from windget import getIndustryCodeSeries


# 获取所属行业代码(支持历史)
from windget import getIndustryCode


# 获取所属行业板块名称(支持历史)时间序列
from windget import getIndustryNameSeries


# 获取所属行业板块名称(支持历史)
from windget import getIndustryName


# 获取所属中证行业名称时间序列
from windget import getIndustryCsiSeries


# 获取所属中证行业名称
from windget import getIndustryCsi


# 获取所属中证行业代码时间序列
from windget import getIndustryCsiCodeSeries


# 获取所属中证行业代码
from windget import getIndustryCsiCode


# 获取所属国民经济行业代码时间序列
from windget import getIndustryNcCodeSeries


# 获取所属国民经济行业代码
from windget import getIndustryNcCode


# 获取所属长江行业名称时间序列
from windget import getIndustryCJscSeries


# 获取所属长江行业名称
from windget import getIndustryCJsc


# 获取所属长江行业指数代码时间序列
from windget import getIndexCodeCJscSeries


# 获取所属长江行业指数代码
from windget import getIndexCodeCJsc


# 获取所属国证行业名称时间序列
from windget import getIndustryCnSeries


# 获取所属国证行业名称
from windget import getIndustryCn


# 获取所属国证行业代码时间序列
from windget import getIndustryCnCodeSeries


# 获取所属国证行业代码
from windget import getIndustryCnCode


# 获取所属国证行业指数代码时间序列
from windget import getIndexCodeCnSeries


# 获取所属国证行业指数代码
from windget import getIndexCodeCn


# 获取所属科创板主题行业时间序列
from windget import getThematicIndustrySibSeries


# 获取所属科创板主题行业
from windget import getThematicIndustrySib


# 获取董事长时间序列
from windget import getBoardChairmenSeries


# 获取董事长
from windget import getBoardChairmen


# 获取董事长薪酬时间序列
from windget import getStmNoteMGmtBenBcSeries


# 获取董事长薪酬
from windget import getStmNoteMGmtBenBc


# 获取总经理时间序列
from windget import getCeoSeries


# 获取总经理
from windget import getCeo


# 获取总经理薪酬时间序列
from windget import getStmNoteMGmtBenCeoSeries


# 获取总经理薪酬
from windget import getStmNoteMGmtBenCeo


# 获取基金管理人总经理时间序列
from windget import getFundCorpManagerSeries


# 获取基金管理人总经理
from windget import getFundCorpManager


# 获取董事会秘书时间序列
from windget import getDIsCloser1Series


# 获取董事会秘书
from windget import getDIsCloser1


# 获取董事会秘书薪酬时间序列
from windget import getStmNoteMGmtBenDIsCloserSeries


# 获取董事会秘书薪酬
from windget import getStmNoteMGmtBenDIsCloser


# 获取证券事务代表时间序列
from windget import getSar1Series


# 获取证券事务代表
from windget import getSar1


# 获取证券事务代表薪酬时间序列
from windget import getStmNoteMGmtBenSarSeries


# 获取证券事务代表薪酬
from windget import getStmNoteMGmtBenSar


# 获取财务总监时间序列
from windget import getCfOSeries


# 获取财务总监
from windget import getCfO


# 获取财务总监薪酬时间序列
from windget import getStmNoteMGmtBenCfOSeries


# 获取财务总监薪酬
from windget import getStmNoteMGmtBenCfO


# 获取公司独立董事(现任)时间序列
from windget import getCrtInDpDirectorSeries


# 获取公司独立董事(现任)
from windget import getCrtInDpDirector


# 获取公司独立董事(历任)时间序列
from windget import getSUciNdpDirectorSeries


# 获取公司独立董事(历任)
from windget import getSUciNdpDirector


# 获取公司董事时间序列
from windget import getDirectorSeries


# 获取公司董事
from windget import getDirector


# 获取公司董事(历任)时间序列
from windget import getSUcDirectorSeries


# 获取公司董事(历任)
from windget import getSUcDirector


# 获取公司监事时间序列
from windget import getSupervisorSeries


# 获取公司监事
from windget import getSupervisor


# 获取公司监事(历任)时间序列
from windget import getSUcSupervisorSeries


# 获取公司监事(历任)
from windget import getSUcSupervisor


# 获取公司高管时间序列
from windget import getExecutivesSeries


# 获取公司高管
from windget import getExecutives


# 获取公司高管(历任)时间序列
from windget import getSUcExecutivesSeries


# 获取公司高管(历任)
from windget import getSUcExecutives


# 获取金额前三的董事薪酬合计时间序列
from windget import getStmNoteMGmtBenTop3BSeries


# 获取金额前三的董事薪酬合计
from windget import getStmNoteMGmtBenTop3B


# 获取金额前三的高管薪酬合计时间序列
from windget import getStmNoteMGmtBenTop3MSeries


# 获取金额前三的高管薪酬合计
from windget import getStmNoteMGmtBenTop3M


# 获取董事会人数时间序列
from windget import getEmployeeBoardSeries


# 获取董事会人数
from windget import getEmployeeBoard


# 获取非独立董事人数时间序列
from windget import getEmployeeExecutiveDirectorSeries


# 获取非独立董事人数
from windget import getEmployeeExecutiveDirector


# 获取独立董事人数时间序列
from windget import getEmployeeInDpDirectorSeries


# 获取独立董事人数
from windget import getEmployeeInDpDirector


# 获取高管人数时间序列
from windget import getEmployeeMGmtSeries


# 获取高管人数
from windget import getEmployeeMGmt


# 获取核心技术人员人数时间序列
from windget import getEmployeeTechCoreSeries


# 获取核心技术人员人数
from windget import getEmployeeTechCore


# 获取审计机构时间序列
from windget import getAuditorSeries


# 获取审计机构
from windget import getAuditor


# 获取审计机构(支持历史)时间序列
from windget import getAuditor2Series


# 获取审计机构(支持历史)
from windget import getAuditor2


# 获取首发审计机构时间序列
from windget import getIpoAuditorSeries


# 获取首发审计机构
from windget import getIpoAuditor


# 获取法律顾问时间序列
from windget import getCloSeries


# 获取法律顾问
from windget import getClo


# 获取经办律师时间序列
from windget import getLiCSeries


# 获取经办律师
from windget import getLiC


# 获取首发经办律师时间序列
from windget import getIpoLawErSeries


# 获取首发经办律师
from windget import getIpoLawEr


# 获取资产评估机构时间序列
from windget import getFundReItSvaAgSeries


# 获取资产评估机构
from windget import getFundReItSvaAg


# 获取经办评估人员时间序列
from windget import getVicSeries


# 获取经办评估人员
from windget import getVic


# 获取主要往来银行时间序列
from windget import getBanksSeries


# 获取主要往来银行
from windget import getBanks


# 获取生产人员人数时间序列
from windget import getEmployeeProducerSeries


# 获取生产人员人数
from windget import getEmployeeProducer


# 获取生产人员人数占比时间序列
from windget import getEmployeeProducerPctSeries


# 获取生产人员人数占比
from windget import getEmployeeProducerPct


# 获取销售人员人数时间序列
from windget import getEmployeeSaleSeries


# 获取销售人员人数
from windget import getEmployeeSale


# 获取销售人员人数占比时间序列
from windget import getEmployeeSalePctSeries


# 获取销售人员人数占比
from windget import getEmployeeSalePct


# 获取客服人员人数时间序列
from windget import getEmployeeServerSeries


# 获取客服人员人数
from windget import getEmployeeServer


# 获取客服人员人数占比时间序列
from windget import getEmployeeServerPctSeries


# 获取客服人员人数占比
from windget import getEmployeeServerPct


# 获取技术人员人数时间序列
from windget import getEmployeeTechSeries


# 获取技术人员人数
from windget import getEmployeeTech


# 获取技术人员人数占比时间序列
from windget import getEmployeeTechPctSeries


# 获取技术人员人数占比
from windget import getEmployeeTechPct


# 获取财务人员人数时间序列
from windget import getEmployeeFinSeries


# 获取财务人员人数
from windget import getEmployeeFin


# 获取财务人员人数占比时间序列
from windget import getEmployeeFinPctSeries


# 获取财务人员人数占比
from windget import getEmployeeFinPct


# 获取人事人员人数时间序列
from windget import getEmployeeHrSeries


# 获取人事人员人数
from windget import getEmployeeHr


# 获取人事人员人数占比时间序列
from windget import getEmployeeHrPctSeries


# 获取人事人员人数占比
from windget import getEmployeeHrPct


# 获取行政人员人数时间序列
from windget import getEmployeeExCuSeries


# 获取行政人员人数
from windget import getEmployeeExCu


# 获取行政人员人数占比时间序列
from windget import getEmployeeExCuPctSeries


# 获取行政人员人数占比
from windget import getEmployeeExCuPct


# 获取风控稽核人员人数时间序列
from windget import getEmployeeRcSeries


# 获取风控稽核人员人数
from windget import getEmployeeRc


# 获取风控稽核人员人数占比时间序列
from windget import getEmployeeRcPctSeries


# 获取风控稽核人员人数占比
from windget import getEmployeeRcPct


# 获取采购仓储人员人数时间序列
from windget import getEmployeePurSeries


# 获取采购仓储人员人数
from windget import getEmployeePur


# 获取采购仓储人员人数占比时间序列
from windget import getEmployeePurPctSeries


# 获取采购仓储人员人数占比
from windget import getEmployeePurPct


# 获取其他人员人数时间序列
from windget import getEmployeeOThDeptSeries


# 获取其他人员人数
from windget import getEmployeeOThDept


# 获取博士人数时间序列
from windget import getEmployeePhdSeries


# 获取博士人数
from windget import getEmployeePhd


# 获取博士人数占比时间序列
from windget import getEmployeePhdPctSeries


# 获取博士人数占比
from windget import getEmployeePhdPct


# 获取硕士人数时间序列
from windget import getEmployeeMsSeries


# 获取硕士人数
from windget import getEmployeeMs


# 获取硕士人数占比时间序列
from windget import getEmployeeMsPctSeries


# 获取硕士人数占比
from windget import getEmployeeMsPct


# 获取本科人数时间序列
from windget import getEmployeeBaSeries


# 获取本科人数
from windget import getEmployeeBa


# 获取本科人数占比时间序列
from windget import getEmployeeBaPctSeries


# 获取本科人数占比
from windget import getEmployeeBaPct


# 获取专科人数时间序列
from windget import getEmployeeCollSeries


# 获取专科人数
from windget import getEmployeeColl


# 获取专科人数占比时间序列
from windget import getEmployeeCollPctSeries


# 获取专科人数占比
from windget import getEmployeeCollPct


# 获取高中及以下人数时间序列
from windget import getEmployeeHighschoolSeries


# 获取高中及以下人数
from windget import getEmployeeHighschool


# 获取高中及以下人数占比时间序列
from windget import getEmployeeHighschoolPctSeries


# 获取高中及以下人数占比
from windget import getEmployeeHighschoolPct


# 获取其他学历人数时间序列
from windget import getEmployeeOThDegreeSeries


# 获取其他学历人数
from windget import getEmployeeOThDegree


# 获取其他学历人数占比时间序列
from windget import getEmployeeOThDegreePctSeries


# 获取其他学历人数占比
from windget import getEmployeeOThDegreePct


# 获取其他专业人员人数占比时间序列
from windget import getEmployeeOThDeptPctSeries


# 获取其他专业人员人数占比
from windget import getEmployeeOThDeptPct


# 获取总股本时间序列
from windget import getTotalSharesSeries


# 获取总股本
from windget import getTotalShares


# 获取备考总股本(并购后)时间序列
from windget import getMaTotalSharesSeries


# 获取备考总股本(并购后)
from windget import getMaTotalShares


# 获取上市前总股本时间序列
from windget import getShareToTSharesPreSeries


# 获取上市前总股本
from windget import getShareToTSharesPre


# 获取首发后总股本(上市日)时间序列
from windget import getIpoToTCapAfterIssueSeries


# 获取首发后总股本(上市日)
from windget import getIpoToTCapAfterIssue


# 获取首发前总股本时间序列
from windget import getIpoToTCapBeforeIssueSeries


# 获取首发前总股本
from windget import getIpoToTCapBeforeIssue


# 获取预计发行后总股本时间序列
from windget import getIpoToTCapAfterIssueEstSeries


# 获取预计发行后总股本
from windget import getIpoToTCapAfterIssueEst


# 获取流通股东持股比例(相对总股本)时间序列
from windget import getHolderPctLiqSeries


# 获取流通股东持股比例(相对总股本)
from windget import getHolderPctLiq


# 获取自由流通股本时间序列
from windget import getFreeFloatSharesSeries


# 获取自由流通股本
from windget import getFreeFloatShares


# 获取三板合计时间序列
from windget import getShareTotalOtcSeries


# 获取三板合计
from windget import getShareTotalOtc


# 获取香港上市股时间序列
from windget import getShareHSeries


# 获取香港上市股
from windget import getShareH


# 获取海外上市股时间序列
from windget import getShareOverSeaSeries


# 获取海外上市股
from windget import getShareOverSea


# 获取流通股合计时间序列
from windget import getShareTotalTradableSeries


# 获取流通股合计
from windget import getShareTotalTradable


# 获取限售股合计时间序列
from windget import getShareTotalRestrictedSeries


# 获取限售股合计
from windget import getShareTotalRestricted


# 获取非流通股时间序列
from windget import getShareNonTradable2Series


# 获取非流通股
from windget import getShareNonTradable2


# 获取原非流通股股东有效申购户数时间序列
from windget import getCbResultEfInvestorNonTrAdSeries


# 获取原非流通股股东有效申购户数
from windget import getCbResultEfInvestorNonTrAd


# 获取原非流通股股东有效申购金额时间序列
from windget import getCbResultEfAmNtNonTrAdSeries


# 获取原非流通股股东有效申购金额
from windget import getCbResultEfAmNtNonTrAd


# 获取原非流通股股东获配金额时间序列
from windget import getCbResultRationAmtNonTrAdSeries


# 获取原非流通股股东获配金额
from windget import getCbResultRationAmtNonTrAd


# 获取优先股时间序列
from windget import getShareNtrDPrFShareSeries


# 获取优先股
from windget import getShareNtrDPrFShare


# 获取优先股_GSD时间序列
from windget import getWgsDPfDStKSeries


# 获取优先股_GSD
from windget import getWgsDPfDStK


# 获取优先股利及其他调整项_GSD时间序列
from windget import getWgsDDvdPfDAdjSeries


# 获取优先股利及其他调整项_GSD
from windget import getWgsDDvdPfDAdj


# 获取单季度.优先股利及其他调整项_GSD时间序列
from windget import getWgsDQfaDvdPfDAdjSeries


# 获取单季度.优先股利及其他调整项_GSD
from windget import getWgsDQfaDvdPfDAdj


# 获取其他权益工具:优先股时间序列
from windget import getOtherEquityInstrumentsPreSeries


# 获取其他权益工具:优先股
from windget import getOtherEquityInstrumentsPre


# 获取已发行数量时间序列
from windget import getShareIssuingSeries


# 获取已发行数量
from windget import getShareIssuing


# 获取流通股本时间序列
from windget import getShareIssuingMktSeries


# 获取流通股本
from windget import getShareIssuingMkt


# 获取限售股份(国家持股)时间序列
from windget import getShareRTdStateSeries


# 获取限售股份(国家持股)
from windget import getShareRTdState


# 获取限售股份(国有法人持股)时间序列
from windget import getShareRTdStateJurSeries


# 获取限售股份(国有法人持股)
from windget import getShareRTdStateJur


# 获取限售股份(其他内资持股合计)时间序列
from windget import getShareRTdSubOtherDomesSeries


# 获取限售股份(其他内资持股合计)
from windget import getShareRTdSubOtherDomes


# 获取限售股份(境内法人持股)时间序列
from windget import getShareRTdDomesJurSeries


# 获取限售股份(境内法人持股)
from windget import getShareRTdDomesJur


# 获取限售股份(机构配售股份)时间序列
from windget import getShareRTdInStSeries


# 获取限售股份(机构配售股份)
from windget import getShareRTdInSt


# 获取限售股份(境内自然人持股)时间序列
from windget import getShareRTdDomeSnpSeries


# 获取限售股份(境内自然人持股)
from windget import getShareRTdDomeSnp


# 获取限售股份(外资持股合计)时间序列
from windget import getShareRTdSubFrgNSeries


# 获取限售股份(外资持股合计)
from windget import getShareRTdSubFrgN


# 获取限售股份(境外法人持股)时间序列
from windget import getShareRTdFrgNJurSeries


# 获取限售股份(境外法人持股)
from windget import getShareRTdFrgNJur


# 获取限售股份(境外自然人持股)时间序列
from windget import getShareRTdFrgNNpSeries


# 获取限售股份(境外自然人持股)
from windget import getShareRTdFrgNNp


# 获取质押比例时间序列
from windget import getSharePledgedAPctSeries


# 获取质押比例
from windget import getSharePledgedAPct


# 获取无限售股份质押比例时间序列
from windget import getShareLiqAPledgedPctSeries


# 获取无限售股份质押比例
from windget import getShareLiqAPledgedPct


# 获取有限售股份质押比例时间序列
from windget import getShareRestrictedAPledgedPctSeries


# 获取有限售股份质押比例
from windget import getShareRestrictedAPledgedPct


# 获取无限售股份质押数量时间序列
from windget import getShareLiqAPledgedSeries


# 获取无限售股份质押数量
from windget import getShareLiqAPledged


# 获取有限售股份质押数量时间序列
from windget import getShareRestrictedAPledgedSeries


# 获取有限售股份质押数量
from windget import getShareRestrictedAPledged


# 获取质押待购回余量时间序列
from windget import getSharePledgedRepurchaseSeries


# 获取质押待购回余量
from windget import getSharePledgedRepurchase


# 获取限售解禁日期时间序列
from windget import getShareRTdUnlockingDateSeries


# 获取限售解禁日期
from windget import getShareRTdUnlockingDate


# 获取本期解禁数量时间序列
from windget import getShareTradableCurrentSeries


# 获取本期解禁数量
from windget import getShareTradableCurrent


# 获取未流通数量时间序列
from windget import getShareRTdBAnceSeries


# 获取未流通数量
from windget import getShareRTdBAnce


# 获取解禁数据类型时间序列
from windget import getShareRTdDataTypeSeries


# 获取解禁数据类型
from windget import getShareRTdDataType


# 获取指定日之后最近一次解禁数据类型时间序列
from windget import getShareRTdDataTypeFwdSeries


# 获取指定日之后最近一次解禁数据类型
from windget import getShareRTdDataTypeFwd


# 获取解禁股份性质时间序列
from windget import getShareTradableShareTypeSeries


# 获取解禁股份性质
from windget import getShareTradableShareType


# 获取指定日之后最近一次解禁股份性质时间序列
from windget import getShareTradableShareTypeFwdSeries


# 获取指定日之后最近一次解禁股份性质
from windget import getShareTradableShareTypeFwd


# 获取指定日之后最近一次解禁日期时间序列
from windget import getShareRTdUnlockingDateFwdSeries


# 获取指定日之后最近一次解禁日期
from windget import getShareRTdUnlockingDateFwd


# 获取指定日之后最近一次解禁数量时间序列
from windget import getShareTradableCurrentFwdSeries


# 获取指定日之后最近一次解禁数量
from windget import getShareTradableCurrentFwd


# 获取流通三板股时间序列
from windget import getShareOtcTradableSeries


# 获取流通三板股
from windget import getShareOtcTradable


# 获取流通股(控股股东或实际控制人)时间序列
from windget import getShareOtcTradableControllerSeries


# 获取流通股(控股股东或实际控制人)
from windget import getShareOtcTradableController


# 获取流通股(核心员工)时间序列
from windget import getShareOtcTradableBackboneSeries


# 获取流通股(核心员工)
from windget import getShareOtcTradableBackbone


# 获取流通股(其他)时间序列
from windget import getShareOtcTradableOthersSeries


# 获取流通股(其他)
from windget import getShareOtcTradableOthers


# 获取限售三板股时间序列
from windget import getShareOtcRestrictedSeries


# 获取限售三板股
from windget import getShareOtcRestricted


# 获取限售股份(控股股东或实际控制人)时间序列
from windget import getShareOtcRestrictedControllerSeries


# 获取限售股份(控股股东或实际控制人)
from windget import getShareOtcRestrictedController


# 获取限售股份(高管持股)时间序列
from windget import getShareRestrictedMSeries


# 获取限售股份(高管持股)
from windget import getShareRestrictedM


# 获取限售股份(核心员工)时间序列
from windget import getShareOtcRestrictedBackboneSeries


# 获取限售股份(核心员工)
from windget import getShareOtcRestrictedBackbone


# 获取限售股份(其他)时间序列
from windget import getShareOtcRestrictedOthersSeries


# 获取限售股份(其他)
from windget import getShareOtcRestrictedOthers


# 获取份额是否为合并数据时间序列
from windget import getUnitMergedSharesOrNotSeries


# 获取份额是否为合并数据
from windget import getUnitMergedSharesOrNot


# 获取持有份额是否为合并数据时间序列
from windget import getHolderMergedHoldingOrNotSeries


# 获取持有份额是否为合并数据
from windget import getHolderMergedHoldingOrNot


# 获取场内流通份额时间序列
from windget import getUnitFloorTradingSeries


# 获取场内流通份额
from windget import getUnitFloorTrading


# 获取当期场内流通份额变化时间序列
from windget import getUnitFloorTradingChangeSeries


# 获取当期场内流通份额变化
from windget import getUnitFloorTradingChange


# 获取报告期总申购份额时间序列
from windget import getUnitPurchaseSeries


# 获取报告期总申购份额
from windget import getUnitPurchase


# 获取报告期总赎回份额时间序列
from windget import getUnitRedemptionSeries


# 获取报告期总赎回份额
from windget import getUnitRedemption


# 获取报告期申购赎回净额时间序列
from windget import getUnitNetPurchaseSeries


# 获取报告期申购赎回净额
from windget import getUnitNetPurchase


# 获取单季度总申购份额时间序列
from windget import getUnitPurchaseQTySeries


# 获取单季度总申购份额
from windget import getUnitPurchaseQTy


# 获取单季度总赎回份额时间序列
from windget import getUnitRedemptionQTySeries


# 获取单季度总赎回份额
from windget import getUnitRedemptionQTy


# 获取单季度净申购赎回率时间序列
from windget import getUnitNetQuarterlyRatioSeries


# 获取单季度净申购赎回率
from windget import getUnitNetQuarterlyRatio


# 获取单季度申购赎回净额时间序列
from windget import getUnitNetPurchaseQTySeries


# 获取单季度申购赎回净额
from windget import getUnitNetPurchaseQTy


# 获取前十大股东持股比例合计时间序列
from windget import getHolderTop10PctSeries


# 获取前十大股东持股比例合计
from windget import getHolderTop10Pct


# 获取前十大股东持股数量合计时间序列
from windget import getHolderTop10QuantitySeries


# 获取前十大股东持股数量合计
from windget import getHolderTop10Quantity


# 获取前十大流通股东持股数量合计时间序列
from windget import getHolderTop10LiqQuantitySeries


# 获取前十大流通股东持股数量合计
from windget import getHolderTop10LiqQuantity


# 获取大股东累计质押数量时间序列
from windget import getSharePledgedAHolderSeries


# 获取大股东累计质押数量
from windget import getSharePledgedAHolder


# 获取大股东累计质押数量(旧)时间序列
from windget import getSharePledgedALargestHolderSeries


# 获取大股东累计质押数量(旧)
from windget import getSharePledgedALargestHolder


# 获取大股东累计质押数占持股数比例时间序列
from windget import getSharePledgedAPctHolderSeries


# 获取大股东累计质押数占持股数比例
from windget import getSharePledgedAPctHolder


# 获取大股东累计质押数占持股数比例(旧)时间序列
from windget import getSharePledgedAPctLargestHolderSeries


# 获取大股东累计质押数占持股数比例(旧)
from windget import getSharePledgedAPctLargestHolder


# 获取大股东累计冻结数量时间序列
from windget import getShareFrozenAHolderSeries


# 获取大股东累计冻结数量
from windget import getShareFrozenAHolder


# 获取大股东累计冻结数占持股数比例时间序列
from windget import getShareFrozenAPctHolderSeries


# 获取大股东累计冻结数占持股数比例
from windget import getShareFrozenAPctHolder


# 获取公布实际控制人名称时间序列
from windget import getHolderRpTControllerSeries


# 获取公布实际控制人名称
from windget import getHolderRpTController


# 获取实际控制人名称时间序列
from windget import getHolderControllerSeries


# 获取实际控制人名称
from windget import getHolderController


# 获取实际控制人属性时间序列
from windget import getHolderControllerAtTrSeries


# 获取实际控制人属性
from windget import getHolderControllerAtTr


# 获取机构股东名称时间序列
from windget import getHolderInstituteSeries


# 获取机构股东名称
from windget import getHolderInstitute


# 获取大股东名称时间序列
from windget import getHolderNameSeries


# 获取大股东名称
from windget import getHolderName


# 获取大股东持股数量时间序列
from windget import getHolderQuantitySeries


# 获取大股东持股数量
from windget import getHolderQuantity


# 获取大股东持股比例时间序列
from windget import getHolderPctSeries


# 获取大股东持股比例
from windget import getHolderPct


# 获取前5大股东持股比例之和_PIT时间序列
from windget import getHolderSumPctTop5Series


# 获取前5大股东持股比例之和_PIT
from windget import getHolderSumPctTop5


# 获取前5大股东持股比例平方之和_PIT时间序列
from windget import getHolderSumsQuPctTop5Series


# 获取前5大股东持股比例平方之和_PIT
from windget import getHolderSumsQuPctTop5


# 获取前10大股东持股比例平方之和_PIT时间序列
from windget import getHolderSumsQuPctTop10Series


# 获取前10大股东持股比例平方之和_PIT
from windget import getHolderSumsQuPctTop10


# 获取大股东持股股本性质时间序列
from windget import getHolderShareCategorySeries


# 获取大股东持股股本性质
from windget import getHolderShareCategory


# 获取大股东持有的限售股份数时间序列
from windget import getHolderQuantityRestrictedSeries


# 获取大股东持有的限售股份数
from windget import getHolderQuantityRestricted


# 获取大股东性质时间序列
from windget import getHolderNatureSeries


# 获取大股东性质
from windget import getHolderNature


# 获取机构股东类型时间序列
from windget import getHolderCategorySeries


# 获取机构股东类型
from windget import getHolderCategory


# 获取流通股东名称时间序列
from windget import getHolderLiqNameSeries


# 获取流通股东名称
from windget import getHolderLiqName


# 获取流通股东持股数量时间序列
from windget import getHolderLiqQuantitySeries


# 获取流通股东持股数量
from windget import getHolderLiqQuantity


# 获取流通股东持股比例时间序列
from windget import getHolderLiqPctSeries


# 获取流通股东持股比例
from windget import getHolderLiqPct


# 获取流通股东持股股本性质时间序列
from windget import getHolderLiqShareCategorySeries


# 获取流通股东持股股本性质
from windget import getHolderLiqShareCategory


# 获取户均持股数量时间序列
from windget import getHolderAvgNumSeries


# 获取户均持股数量
from windget import getHolderAvgNum


# 获取户均持股比例时间序列
from windget import getHolderAvgPctSeries


# 获取户均持股比例
from windget import getHolderAvgPct


# 获取户均持股比例半年增长率时间序列
from windget import getHolderHAvgPctChangeSeries


# 获取户均持股比例半年增长率
from windget import getHolderHAvgPctChange


# 获取户均持股比例季度增长率时间序列
from windget import getHolderQAvgPctChangeSeries


# 获取户均持股比例季度增长率
from windget import getHolderQAvgPctChange


# 获取相对上一报告期户均持股比例差时间序列
from windget import getHolderAvgPctChangeSeries


# 获取相对上一报告期户均持股比例差
from windget import getHolderAvgPctChange


# 获取户均持股数半年增长率时间序列
from windget import getHolderHAvgChangeSeries


# 获取户均持股数半年增长率
from windget import getHolderHAvgChange


# 获取户均持股数季度增长率时间序列
from windget import getHolderQAvgChangeSeries


# 获取户均持股数季度增长率
from windget import getHolderQAvgChange


# 获取基金持股数量时间序列
from windget import getHolderTotalByFundSeries


# 获取基金持股数量
from windget import getHolderTotalByFund


# 获取社保基金持股数量时间序列
from windget import getHolderTotalBySSFundSeries


# 获取社保基金持股数量
from windget import getHolderTotalBySSFund


# 获取券商持股数量时间序列
from windget import getHolderTotalByBySecSeries


# 获取券商持股数量
from windget import getHolderTotalByBySec


# 获取券商理财产品持股数量时间序列
from windget import getHolderTotalByByWMpSeries


# 获取券商理财产品持股数量
from windget import getHolderTotalByByWMp


# 获取阳光私募持股数量时间序列
from windget import getHolderTotalByHfSeries


# 获取阳光私募持股数量
from windget import getHolderTotalByHf


# 获取保险公司持股数量时间序列
from windget import getHolderTotalByInSurSeries


# 获取保险公司持股数量
from windget import getHolderTotalByInSur


# 获取企业年金持股数量时间序列
from windget import getHolderTotalByCorpPensionSeries


# 获取企业年金持股数量
from windget import getHolderTotalByCorpPension


# 获取信托公司持股数量时间序列
from windget import getHolderTotalByTrustCorpSeries


# 获取信托公司持股数量
from windget import getHolderTotalByTrustCorp


# 获取财务公司持股数量时间序列
from windget import getHolderTotalByFinanceCorpSeries


# 获取财务公司持股数量
from windget import getHolderTotalByFinanceCorp


# 获取银行持股数量时间序列
from windget import getHolderTotalByBankSeries


# 获取银行持股数量
from windget import getHolderTotalByBank


# 获取一般法人持股数量时间序列
from windget import getHolderTotalByGeneralCorpSeries


# 获取一般法人持股数量
from windget import getHolderTotalByGeneralCorp


# 获取非金融类上市公司持股数量时间序列
from windget import getHolderTotalByLnFCorpSeries


# 获取非金融类上市公司持股数量
from windget import getHolderTotalByLnFCorp


# 获取基金持股比例时间序列
from windget import getHolderPctByFundSeries


# 获取基金持股比例
from windget import getHolderPctByFund


# 获取社保基金持股比例时间序列
from windget import getHolderPctBySSFundSeries


# 获取社保基金持股比例
from windget import getHolderPctBySSFund


# 获取券商持股比例时间序列
from windget import getHolderPctBySecSeries


# 获取券商持股比例
from windget import getHolderPctBySec


# 获取券商理财产品持股比例时间序列
from windget import getHolderPctByByWMpSeries


# 获取券商理财产品持股比例
from windget import getHolderPctByByWMp


# 获取阳光私募持股比例时间序列
from windget import getHolderPctByHfSeries


# 获取阳光私募持股比例
from windget import getHolderPctByHf


# 获取保险公司持股比例时间序列
from windget import getHolderPctByInSurSeries


# 获取保险公司持股比例
from windget import getHolderPctByInSur


# 获取企业年金持股比例时间序列
from windget import getHolderPctByCorpPensionSeries


# 获取企业年金持股比例
from windget import getHolderPctByCorpPension


# 获取信托公司持股比例时间序列
from windget import getHolderPctByTrustCorpSeries


# 获取信托公司持股比例
from windget import getHolderPctByTrustCorp


# 获取财务公司持股比例时间序列
from windget import getHolderPctByFinanceCorpSeries


# 获取财务公司持股比例
from windget import getHolderPctByFinanceCorp


# 获取银行持股比例时间序列
from windget import getHolderPctByBankSeries


# 获取银行持股比例
from windget import getHolderPctByBank


# 获取一般法人持股比例时间序列
from windget import getHolderPctByGeneralCorpSeries


# 获取一般法人持股比例
from windget import getHolderPctByGeneralCorp


# 获取非金融类上市公司持股比例时间序列
from windget import getHolderPctByLnFCorpSeries


# 获取非金融类上市公司持股比例
from windget import getHolderPctByLnFCorp


# 获取持股机构数时间序列
from windget import getHolderNumISeries


# 获取持股机构数
from windget import getHolderNumI


# 获取持股基金数时间序列
from windget import getHolderNumFundSeries


# 获取持股基金数
from windget import getHolderNumFund


# 获取持股社保基金数时间序列
from windget import getHolderNumSSFundSeries


# 获取持股社保基金数
from windget import getHolderNumSSFund


# 获取持股保险公司数时间序列
from windget import getHolderNumInSurSeries


# 获取持股保险公司数
from windget import getHolderNumInSur


# 获取定向增发价格时间序列
from windget import getHolderPriceFellowOnSeries


# 获取定向增发价格
from windget import getHolderPriceFellowOn


# 获取大股东增持价格时间序列
from windget import getHolderPriceMajorShareholdersSeries


# 获取大股东增持价格
from windget import getHolderPriceMajorShareholders


# 获取员工持股计划买入价格时间序列
from windget import getHolderPriceEsOpSeries


# 获取员工持股计划买入价格
from windget import getHolderPriceEsOp


# 获取持有人户数是否为合并数据时间序列
from windget import getHolderMergedNumberOrNotSeries


# 获取持有人户数是否为合并数据
from windget import getHolderMergedNumberOrNot


# 获取机构投资者持有份额时间序列
from windget import getHolderInstitutionHoldingSeries


# 获取机构投资者持有份额
from windget import getHolderInstitutionHolding


# 获取机构投资者持有份额(合计)时间序列
from windget import getHolderInstitutionTotalHoldingSeries


# 获取机构投资者持有份额(合计)
from windget import getHolderInstitutionTotalHolding


# 获取机构投资者持有比例时间序列
from windget import getHolderInstitutionHoldingPctSeries


# 获取机构投资者持有比例
from windget import getHolderInstitutionHoldingPct


# 获取机构投资者持有比例(合计)时间序列
from windget import getHolderInstitutionTotalHoldingPctSeries


# 获取机构投资者持有比例(合计)
from windget import getHolderInstitutionTotalHoldingPct


# 获取管理人员工持有份额时间序列
from windget import getHolderMNgEmpHoldingSeries


# 获取管理人员工持有份额
from windget import getHolderMNgEmpHolding


# 获取管理人员工持有比例时间序列
from windget import getHolderMNgEmpHoldingPctSeries


# 获取管理人员工持有比例
from windget import getHolderMNgEmpHoldingPct


# 获取基金管理公司持有份额时间序列
from windget import getHolderCorpHoldingSeries


# 获取基金管理公司持有份额
from windget import getHolderCorpHolding


# 获取基金管理公司持有比例时间序列
from windget import getHolderCorpHoldingPctSeries


# 获取基金管理公司持有比例
from windget import getHolderCorpHoldingPct


# 获取个人投资者持有份额时间序列
from windget import getHolderPersonalHoldingSeries


# 获取个人投资者持有份额
from windget import getHolderPersonalHolding


# 获取个人投资者持有份额(合计)时间序列
from windget import getHolderPersonalTotalHoldingSeries


# 获取个人投资者持有份额(合计)
from windget import getHolderPersonalTotalHolding


# 获取个人投资者持有比例时间序列
from windget import getHolderPersonalHoldingPctSeries


# 获取个人投资者持有比例
from windget import getHolderPersonalHoldingPct


# 获取个人投资者持有比例(合计)时间序列
from windget import getHolderPersonalTotalHoldingPctSeries


# 获取个人投资者持有比例(合计)
from windget import getHolderPersonalTotalHoldingPct


# 获取前十大持有人持有份额合计时间序列
from windget import getFundHolderTop10HoldingSeries


# 获取前十大持有人持有份额合计
from windget import getFundHolderTop10Holding


# 获取前十大持有人持有份额合计(货币)时间序列
from windget import getFundHolderTop10HoldingMmFSeries


# 获取前十大持有人持有份额合计(货币)
from windget import getFundHolderTop10HoldingMmF


# 获取前十大持有人持有比例合计时间序列
from windget import getFundHolderTop10PctSeries


# 获取前十大持有人持有比例合计
from windget import getFundHolderTop10Pct


# 获取前十大持有人持有比例合计(货币)时间序列
from windget import getFundHolderTop10PctMmFSeries


# 获取前十大持有人持有比例合计(货币)
from windget import getFundHolderTop10PctMmF


# 获取单一投资者报告期末持有份额时间序列
from windget import getHolderSingleHoldingSeries


# 获取单一投资者报告期末持有份额
from windget import getHolderSingleHolding


# 获取单一投资者报告期末持有份额合计时间序列
from windget import getHolderSingleTotalHoldingSeries


# 获取单一投资者报告期末持有份额合计
from windget import getHolderSingleTotalHolding


# 获取单一投资者报告期末持有比例时间序列
from windget import getHolderSingleHoldingPctSeries


# 获取单一投资者报告期末持有比例
from windget import getHolderSingleHoldingPct


# 获取单一投资者报告期末持有比例合计时间序列
from windget import getHolderSingleTotalHoldingPctSeries


# 获取单一投资者报告期末持有比例合计
from windget import getHolderSingleTotalHoldingPct


# 获取合格投资者类型时间序列
from windget import getBondQualifiedInvestorSeries


# 获取合格投资者类型
from windget import getBondQualifiedInvestor


# 获取持有基金家数时间序列
from windget import getFundHoldFundsSeries


# 获取持有基金家数
from windget import getFundHoldFunds


# 获取基金持有数量合计占存量比时间序列
from windget import getFundHoldRatioOfPositionToAmNtSeries


# 获取基金持有数量合计占存量比
from windget import getFundHoldRatioOfPositionToAmNt


# 获取基金持有数量合计时间序列
from windget import getFundHoldPositionSeries


# 获取基金持有数量合计
from windget import getFundHoldPosition


# 获取持有人名称时间序列
from windget import getBondHolderNameSeries


# 获取持有人名称
from windget import getBondHolderName


# 获取第N名持有人名称时间序列
from windget import getFundHolderNameSeries


# 获取第N名持有人名称
from windget import getFundHolderName


# 获取第N名持有人名称(上市公告)时间序列
from windget import getFundHolderNameListingSeries


# 获取第N名持有人名称(上市公告)
from windget import getFundHolderNameListing


# 获取持有人持有比例时间序列
from windget import getBondHolderPctSeries


# 获取持有人持有比例
from windget import getBondHolderPct


# 获取第N名持有人持有比例时间序列
from windget import getFundHolderPctSeries


# 获取第N名持有人持有比例
from windget import getFundHolderPct


# 获取第N名持有人持有比例(上市公告)时间序列
from windget import getFundHolderPctListingSeries


# 获取第N名持有人持有比例(上市公告)
from windget import getFundHolderPctListing


# 获取第N名持有人持有比例(货币)时间序列
from windget import getFundHolderPctMmFSeries


# 获取第N名持有人持有比例(货币)
from windget import getFundHolderPctMmF


# 获取持有人持有数量时间序列
from windget import getBondHolderQuantitySeries


# 获取持有人持有数量
from windget import getBondHolderQuantity


# 获取持有基金名称时间序列
from windget import getFundHoldBondNamesSeries


# 获取持有基金名称
from windget import getFundHoldBondNames


# 获取基金持债市值时间序列
from windget import getFundHoldBondValueSeries


# 获取基金持债市值
from windget import getFundHoldBondValue


# 获取基金持债市值占发行量比时间序列
from windget import getFundHoldBondRatioSeries


# 获取基金持债市值占发行量比
from windget import getFundHoldBondRatio


# 获取沪(深)股通持股数量时间序列
from windget import getShareNSeries


# 获取沪(深)股通持股数量
from windget import getShareN


# 获取港股通持股数量时间序列
from windget import getShareHkSSeries


# 获取港股通持股数量
from windget import getShareHkS


# 获取沪市港股通持股数量时间序列
from windget import getShareHkShSeries


# 获取沪市港股通持股数量
from windget import getShareHkSh


# 获取深市港股通持股数量时间序列
from windget import getShareHkSzSeries


# 获取深市港股通持股数量
from windget import getShareHkSz


# 获取沪(深)股通持股占比时间序列
from windget import getSharePctNSeries


# 获取沪(深)股通持股占比
from windget import getSharePctN


# 获取沪(深)股通持股占自由流通股比例时间序列
from windget import getSharePctNToFreeFloatSeries


# 获取沪(深)股通持股占自由流通股比例
from windget import getSharePctNToFreeFloat


# 获取港股通持股占比时间序列
from windget import getSharePctHkSSeries


# 获取港股通持股占比
from windget import getSharePctHkS


# 获取沪市港股通持股占比时间序列
from windget import getSharePctHkShSeries


# 获取沪市港股通持股占比
from windget import getSharePctHkSh


# 获取深市港股通持股占比时间序列
from windget import getSharePctHkSzSeries


# 获取深市港股通持股占比
from windget import getSharePctHkSz


# 获取证券全称时间序列
from windget import getFullNameSeries


# 获取证券全称
from windget import getFullName


# 获取债务主体时间序列
from windget import getIssuerUpdatedSeries


# 获取债务主体
from windget import getIssuerUpdated


# 获取实际发行人时间序列
from windget import getIssuerActualSeries


# 获取实际发行人
from windget import getIssuerActual


# 获取债券初始面值时间序列
from windget import getParSeries


# 获取债券初始面值
from windget import getPar


# 获取债券最新面值时间序列
from windget import getLatestParSeries


# 获取债券最新面值
from windget import getLatestPar


# 获取发行总额时间序列
from windget import getIssueAmountSeries


# 获取发行总额
from windget import getIssueAmount


# 获取各级发行总额时间序列
from windget import getTrancheSeries


# 获取各级发行总额
from windget import getTranche


# 获取转债发行总额时间序列
from windget import getCbIssueAmountSeries


# 获取转债发行总额
from windget import getCbIssueAmount


# 获取计划发行总额时间序列
from windget import getIssueAmountPlanSeries


# 获取计划发行总额
from windget import getIssueAmountPlan


# 获取计划发行总额(文字)时间序列
from windget import getTenderAmountPlanSeries


# 获取计划发行总额(文字)
from windget import getTenderAmountPlan


# 获取实际发行总额时间序列
from windget import getTendRstAmountActSeries


# 获取实际发行总额
from windget import getTendRstAmountAct


# 获取各级占比时间序列
from windget import getTrancheRatioSeries


# 获取各级占比
from windget import getTrancheRatio


# 获取债券余额时间序列
from windget import getOutstandingBalanceSeries


# 获取债券余额
from windget import getOutstandingBalance


# 获取存量债券余额时间序列
from windget import getFinaTotalAmountSeries


# 获取存量债券余额
from windget import getFinaTotalAmount


# 获取存量债券余额(支持历史)时间序列
from windget import getFinalTotalAmOutAnytimeSeries


# 获取存量债券余额(支持历史)
from windget import getFinalTotalAmOutAnytime


# 获取存量债券余额(按期限)时间序列
from windget import getFinaMatSeries


# 获取存量债券余额(按期限)
from windget import getFinaMat


# 获取国债余额(做市后)时间序列
from windget import getTBondBalanceSeries


# 获取国债余额(做市后)
from windget import getTBondBalance


# 获取起息日期时间序列
from windget import getCarryDateSeries


# 获取起息日期
from windget import getCarryDate


# 获取计息截止日时间序列
from windget import getCarryEnddateSeries


# 获取计息截止日
from windget import getCarryEnddate


# 获取到期日期时间序列
from windget import getMaturityDateSeries


# 获取到期日期
from windget import getMaturityDate


# 获取债券期限(年)时间序列
from windget import getTermSeries


# 获取债券期限(年)
from windget import getTerm


# 获取债券期限(文字)时间序列
from windget import getTerm2Series


# 获取债券期限(文字)
from windget import getTerm2


# 获取利率类型时间序列
from windget import getInterestTypeSeries


# 获取利率类型
from windget import getInterestType


# 获取票面利率(发行时)时间序列
from windget import getCouponRateSeries


# 获取票面利率(发行时)
from windget import getCouponRate


# 获取利率说明时间序列
from windget import getCouponTxtSeries


# 获取利率说明
from windget import getCouponTxt


# 获取补偿利率说明时间序列
from windget import getClauseInterest6Series


# 获取补偿利率说明
from windget import getClauseInterest6


# 获取计息方式时间序列
from windget import getPaymentTypeSeries


# 获取计息方式
from windget import getPaymentType


# 获取计息基准时间序列
from windget import getActualBenchmarkSeries


# 获取计息基准
from windget import getActualBenchmark


# 获取息票品种时间序列
from windget import getCouponSeries


# 获取息票品种
from windget import getCoupon


# 获取凭证类别时间序列
from windget import getFormSeries


# 获取凭证类别
from windget import getForm


# 获取每年付息次数时间序列
from windget import getInterestFrequencySeries


# 获取每年付息次数
from windget import getInterestFrequency


# 获取年付息日时间序列
from windget import getPaymentDateSeries


# 获取年付息日
from windget import getPaymentDate


# 获取付息日说明时间序列
from windget import getCouponDateTxtSeries


# 获取付息日说明
from windget import getCouponDateTxt


# 获取是否免税时间序列
from windget import getTaxFreeSeries


# 获取是否免税
from windget import getTaxFree


# 获取税率时间序列
from windget import getTaxRateSeries


# 获取税率
from windget import getTaxRate


# 获取市价类型时间序列
from windget import getMktPriceTypeSeries


# 获取市价类型
from windget import getMktPriceType


# 获取兑付日时间序列
from windget import getRedemptionBeginningSeries


# 获取兑付日
from windget import getRedemptionBeginning


# 获取兑付登记日时间序列
from windget import getRedemptionRegBeginningSeries


# 获取兑付登记日
from windget import getRedemptionRegBeginning


# 获取兑付费率时间序列
from windget import getRedemptionFeeRationSeries


# 获取兑付费率
from windget import getRedemptionFeeRation


# 获取偿还方式时间序列
from windget import getRepaymentMethodSeries


# 获取偿还方式
from windget import getRepaymentMethod


# 获取偿付顺序时间序列
from windget import getPaymentOrderSeries


# 获取偿付顺序
from windget import getPaymentOrder


# 获取资产是否出表时间序列
from windget import getIsAssetOutSeries


# 获取资产是否出表
from windget import getIsAssetOut


# 获取计划管理人时间序列
from windget import getAbsSPvSeries


# 获取计划管理人
from windget import getAbsSPv


# 获取原始权益人时间序列
from windget import getFundReItsOriginalSeries


# 获取原始权益人
from windget import getFundReItsOriginal


# 获取原始权益人企业性质时间序列
from windget import getFundReItsOrComSeries


# 获取原始权益人企业性质
from windget import getFundReItsOrCom


# 获取穿透信用主体时间序列
from windget import getAbsPenetrateActRuAlDebtorSeries


# 获取穿透信用主体
from windget import getAbsPenetrateActRuAlDebtor


# 获取发行人(银行)类型时间序列
from windget import getIssuerBankTypeSeries


# 获取发行人(银行)类型
from windget import getIssuerBankType


# 获取最新交易日期时间序列
from windget import getRepoLastEstDateSeries


# 获取最新交易日期
from windget import getRepoLastEstDate


# 获取当前贷款笔数时间序列
from windget import getAbsCurrentLoanSeries


# 获取当前贷款笔数
from windget import getAbsCurrentLoan


# 获取当前贷款余额时间序列
from windget import getAbsCurrentLoansSeries


# 获取当前贷款余额
from windget import getAbsCurrentLoans


# 获取当前加权平均贷款剩余期限时间序列
from windget import getAbsCurrentWarmSeries


# 获取当前加权平均贷款剩余期限
from windget import getAbsCurrentWarm


# 获取当前加权平均贷款利率时间序列
from windget import getAbsCurrentWtGAvgRateSeries


# 获取当前加权平均贷款利率
from windget import getAbsCurrentWtGAvgRate


# 获取累计违约率时间序列
from windget import getAbsCumulativeDefaultRateSeries


# 获取累计违约率
from windget import getAbsCumulativeDefaultRate


# 获取严重拖欠率时间序列
from windget import getAbsDelinquencyRateSeries


# 获取严重拖欠率
from windget import getAbsDelinquencyRate


# 获取承销团成员时间序列
from windget import getAbsCreditNormalSeries


# 获取承销团成员
from windget import getAbsCreditNormal


# 获取主体行业时间序列
from windget import getAbsIndustrySeries


# 获取主体行业
from windget import getAbsIndustry


# 获取主体性质时间序列
from windget import getAbsIndustry1Series


# 获取主体性质
from windget import getAbsIndustry1


# 获取主体地区时间序列
from windget import getAbsProvinceSeries


# 获取主体地区
from windget import getAbsProvince


# 获取受托机构时间序列
from windget import getAbsAgencyTrustee1Series


# 获取受托机构
from windget import getAbsAgencyTrustee1


# 获取项目名称时间序列
from windget import getAbsFullNameProSeries


# 获取项目名称
from windget import getAbsFullNamePro


# 获取项目简称时间序列
from windget import getAbsNameProSeries


# 获取项目简称
from windget import getAbsNamePro


# 获取项目代码时间序列
from windget import getAbsProjectCodeSeries


# 获取项目代码
from windget import getAbsProjectCode


# 获取还本方式时间序列
from windget import getAbsPayBackSeries


# 获取还本方式
from windget import getAbsPayBack


# 获取提前还本方式时间序列
from windget import getPrepayMethodSeries


# 获取提前还本方式
from windget import getPrepayMethod


# 获取基础债务人时间序列
from windget import getAbsBorrowerSeries


# 获取基础债务人
from windget import getAbsBorrower


# 获取基础债务人行业时间序列
from windget import getAbsCoreIndustrySeries


# 获取基础债务人行业
from windget import getAbsCoreIndustry


# 获取基础债务人地区时间序列
from windget import getAbsCoreProvinceSeries


# 获取基础债务人地区
from windget import getAbsCoreProvince


# 获取基础债务人性质时间序列
from windget import getAbsCorePropertySeries


# 获取基础债务人性质
from windget import getAbsCoreProperty


# 获取早偿率时间序列
from windget import getAbsRecommendCprSeries


# 获取早偿率
from windget import getAbsRecommendCpr


# 获取加权平均期限时间序列
from windget import getAbsWeightedAverageMaturityWithPrepaySeries


# 获取加权平均期限
from windget import getAbsWeightedAverageMaturityWithPrepay


# 获取信用支持时间序列
from windget import getAbsCreditSupportSeries


# 获取信用支持
from windget import getAbsCreditSupport


# 获取项目余额时间序列
from windget import getAbsDealOutStStandingAmountSeries


# 获取项目余额
from windget import getAbsDealOutStStandingAmount


# 获取固定资金成本时间序列
from windget import getAbsFiExdCapitalCostRateSeries


# 获取固定资金成本
from windget import getAbsFiExdCapitalCostRate


# 获取次级每期收益率上限时间序列
from windget import getAbsCapYieldPerTermOfSubSeries


# 获取次级每期收益率上限
from windget import getAbsCapYieldPerTermOfSub


# 获取自持比例时间序列
from windget import getAbsSelfSustainingProportionSeries


# 获取自持比例
from windget import getAbsSelfSustainingProportion


# 获取法定到期日时间序列
from windget import getAbsLegalMaturitySeries


# 获取法定到期日
from windget import getAbsLegalMaturity


# 获取支付日时间序列
from windget import getAbsPaymentDateSeries


# 获取支付日
from windget import getAbsPaymentDate


# 获取首次支付日时间序列
from windget import getAbsFirstPaymentDateSeries


# 获取首次支付日
from windget import getAbsFirstPaymentDate


# 获取早偿预期到期日时间序列
from windget import getAbsExpectedMaturityWithPrepaySeries


# 获取早偿预期到期日
from windget import getAbsExpectedMaturityWithPrepay


# 获取初始起算日时间序列
from windget import getAbsCutoffDateSeries


# 获取初始起算日
from windget import getAbsCutoffDate


# 获取清算起始日时间序列
from windget import getAbsStartDateOfAssetClearingSeries


# 获取清算起始日
from windget import getAbsStartDateOfAssetClearing


# 获取清算结束日时间序列
from windget import getAbsEnddateOfAssetClearingSeries


# 获取清算结束日
from windget import getAbsEnddateOfAssetClearing


# 获取差额支付承诺人时间序列
from windget import getAbsDefIGuarantorSeries


# 获取差额支付承诺人
from windget import getAbsDefIGuarantor


# 获取专项计划托管人时间序列
from windget import getAbsTrusteeSeries


# 获取专项计划托管人
from windget import getAbsTrustee


# 获取资产服务机构时间序列
from windget import getAbsAssetServiceAgencySeries


# 获取资产服务机构
from windget import getAbsAssetServiceAgency


# 获取会计处理时间序列
from windget import getAccountTreatmentSeries


# 获取会计处理
from windget import getAccountTreatment


# 获取中债债券一级分类时间序列
from windget import getChinaBondL1TypeSeries


# 获取中债债券一级分类
from windget import getChinaBondL1Type


# 获取中债债券二级分类时间序列
from windget import getChinaBondL2TypeSeries


# 获取中债债券二级分类
from windget import getChinaBondL2Type


# 获取是否城投债(Wind)时间序列
from windget import getMunicipalBondWindSeries


# 获取是否城投债(Wind)
from windget import getMunicipalBondWind


# 获取是否城投债时间序列
from windget import getMunicipalBondSeries


# 获取是否城投债
from windget import getMunicipalBond


# 获取是否城投债(YY)时间序列
from windget import getMunicipalBondyYSeries


# 获取是否城投债(YY)
from windget import getMunicipalBondyY


# 获取城投行政级别(Wind)时间序列
from windget import getCityInvestmentBondGeoWindSeries


# 获取城投行政级别(Wind)
from windget import getCityInvestmentBondGeoWind


# 获取城投行政级别时间序列
from windget import getCityInvestmentBondGeoSeries


# 获取城投行政级别
from windget import getCityInvestmentBondGeo


# 获取是否跨市场交易时间序列
from windget import getMultiMktOrNotSeries


# 获取是否跨市场交易
from windget import getMultiMktOrNot


# 获取是否次级债时间序列
from windget import getSubordinateOrNotSeries


# 获取是否次级债
from windget import getSubordinateOrNot


# 获取是否混合资本债券时间序列
from windget import getMixCapitalSeries


# 获取是否混合资本债券
from windget import getMixCapital


# 获取是否增发时间序列
from windget import getIssueAdditionalSeries


# 获取是否增发
from windget import getIssueAdditional


# 获取增发债对应原债券时间序列
from windget import getAdditionalToSeries


# 获取增发债对应原债券
from windget import getAdditionalTo


# 获取是否永续债时间序列
from windget import getPerpetualOrNotSeries


# 获取是否永续债
from windget import getPerpetualOrNot


# 获取基准利率时间序列
from windget import getBaseRateSeries


# 获取基准利率
from windget import getBaseRate


# 获取基准利率确定方式时间序列
from windget import getCmBirSeries


# 获取基准利率确定方式
from windget import getCmBir


# 获取基准利率(发行时)时间序列
from windget import getBaseRate2Series


# 获取基准利率(发行时)
from windget import getBaseRate2


# 获取基准利率(指定日期)时间序列
from windget import getBaseRate3Series


# 获取基准利率(指定日期)
from windget import getBaseRate3


# 获取计算浮息债隐含基准利率时间序列
from windget import getCalcFloatBenchSeries


# 获取计算浮息债隐含基准利率
from windget import getCalcFloatBench


# 获取固定利差时间序列
from windget import getSpreadSeries


# 获取固定利差
from windget import getSpread


# 获取首个定价日时间序列
from windget import getIssueFirstPriceDateSeries


# 获取首个定价日
from windget import getIssueFirstPriceDate


# 获取票面利率(当期)时间序列
from windget import getCouponRate2Series


# 获取票面利率(当期)
from windget import getCouponRate2


# 获取票面利率(指定日期)时间序列
from windget import getCouponRate3Series


# 获取票面利率(指定日期)
from windget import getCouponRate3


# 获取行权后利差时间序列
from windget import getSpread2Series


# 获取行权后利差
from windget import getSpread2


# 获取保底利率时间序列
from windget import getInterestFloorSeries


# 获取保底利率
from windget import getInterestFloor


# 获取是否含权债时间序列
from windget import getEmbeddedOptSeries


# 获取是否含权债
from windget import getEmbeddedOpt


# 获取特殊条款时间序列
from windget import getClauseSeries


# 获取特殊条款
from windget import getClause


# 获取特殊条款(缩写)时间序列
from windget import getClauseAbbrSeries


# 获取特殊条款(缩写)
from windget import getClauseAbbr


# 获取指定条款文字时间序列
from windget import getClauseItemSeries


# 获取指定条款文字
from windget import getClauseItem


# 获取含权债行权期限时间序列
from windget import getExecMaturityEmbeddedSeries


# 获取含权债行权期限
from windget import getExecMaturityEmbedded


# 获取含权债期限特殊说明时间序列
from windget import getEObSpecialInStrutIonsSeries


# 获取含权债期限特殊说明
from windget import getEObSpecialInStrutIons


# 获取提前还本日时间序列
from windget import getPrepaymentDateSeries


# 获取提前还本日
from windget import getPrepaymentDate


# 获取提前还本比例时间序列
from windget import getPrepayPortionSeries


# 获取提前还本比例
from windget import getPrepayPortion


# 获取赎回日时间序列
from windget import getRedemptionDateSeries


# 获取赎回日
from windget import getRedemptionDate


# 获取回售日时间序列
from windget import getRepurchaseDateSeries


# 获取回售日
from windget import getRepurchaseDate


# 获取赎回价格时间序列
from windget import getClauseCallOptionRedemptionPriceSeries


# 获取赎回价格
from windget import getClauseCallOptionRedemptionPrice


# 获取赎回价格说明时间序列
from windget import getClauseCallOptionRedemptionMemoSeries


# 获取赎回价格说明
from windget import getClauseCallOptionRedemptionMemo


# 获取回售价格时间序列
from windget import getClausePutOptionResellingPriceSeries


# 获取回售价格
from windget import getClausePutOptionResellingPrice


# 获取回售价格说明时间序列
from windget import getClausePutOptionResellingPriceExplainAtionSeries


# 获取回售价格说明
from windget import getClausePutOptionResellingPriceExplainAtion


# 获取附加回售价格说明时间序列
from windget import getClausePutOptionAdditionalPriceMemoSeries


# 获取附加回售价格说明
from windget import getClausePutOptionAdditionalPriceMemo


# 获取回售代码时间序列
from windget import getPutCodeSeries


# 获取回售代码
from windget import getPutCode


# 获取回售登记起始日时间序列
from windget import getRepurchaseBeginDateSeries


# 获取回售登记起始日
from windget import getRepurchaseBeginDate


# 获取回售登记截止日时间序列
from windget import getRepurchaseEnddateSeries


# 获取回售登记截止日
from windget import getRepurchaseEnddate


# 获取行权资金到账日时间序列
from windget import getFunDarRialDateSeries


# 获取行权资金到账日
from windget import getFunDarRialDate


# 获取票面利率调整上限时间序列
from windget import getCouponAdjMaxSeries


# 获取票面利率调整上限
from windget import getCouponAdjMax


# 获取票面利率调整下限时间序列
from windget import getCouponAdjMinSeries


# 获取票面利率调整下限
from windget import getCouponAdjMin


# 获取赎回登记日时间序列
from windget import getClauseCallOptionRecordDateSeries


# 获取赎回登记日
from windget import getClauseCallOptionRecordDate


# 获取担保人时间序列
from windget import getAgencyGuarantorSeries


# 获取担保人
from windget import getAgencyGuarantor


# 获取担保人评级时间序列
from windget import getRateRateGuarantorSeries


# 获取担保人评级
from windget import getRateRateGuarantor


# 获取担保人评级展望时间序列
from windget import getRateFwdGuarantorSeries


# 获取担保人评级展望
from windget import getRateFwdGuarantor


# 获取担保人评级变动方向时间序列
from windget import getRateChNgGuarantorSeries


# 获取担保人评级变动方向
from windget import getRateChNgGuarantor


# 获取担保人评级评级机构时间序列
from windget import getRateAgencyGuarantorSeries


# 获取担保人评级评级机构
from windget import getRateAgencyGuarantor


# 获取再担保人时间序列
from windget import getAgencyReGuarantorSeries


# 获取再担保人
from windget import getAgencyReGuarantor


# 获取发行时担保人评级时间序列
from windget import getRateBeginGuarantorSeries


# 获取发行时担保人评级
from windget import getRateBeginGuarantor


# 获取担保方式时间序列
from windget import getAgencyGrNtTypeSeries


# 获取担保方式
from windget import getAgencyGrNtType


# 获取担保期限时间序列
from windget import getGuarTermSeries


# 获取担保期限
from windget import getGuarTerm


# 获取担保范围时间序列
from windget import getGuarRangeSeries


# 获取担保范围
from windget import getGuarRange


# 获取担保条款文字时间序列
from windget import getAgencyGrNtRangeSeries


# 获取担保条款文字
from windget import getAgencyGrNtRange


# 获取反担保情况时间序列
from windget import getCounterGuarSeries


# 获取反担保情况
from windget import getCounterGuar


# 获取标准券折算金额(每百元面值)时间序列
from windget import getCvnTPerHundredSeries


# 获取标准券折算金额(每百元面值)
from windget import getCvnTPerHundred


# 获取质押券代码时间序列
from windget import getCollateralCodeSeries


# 获取质押券代码
from windget import getCollateralCode


# 获取质押券简称时间序列
from windget import getCollateralNameSeries


# 获取质押券简称
from windget import getCollateralName


# 获取是否可质押时间序列
from windget import getFundPledGableOrNotSeries


# 获取是否可质押
from windget import getFundPledGableOrNot


# 获取报价式回购折算率(中证指数)时间序列
from windget import getRateOfStdBndCsiSeries


# 获取报价式回购折算率(中证指数)
from windget import getRateOfStdBndCsi


# 获取是否随存款利率调整时间序列
from windget import getClauseInterest5Series


# 获取是否随存款利率调整
from windget import getClauseInterest5


# 获取是否有利息补偿时间序列
from windget import getClauseInterest8Series


# 获取是否有利息补偿
from windget import getClauseInterest8


# 获取补偿利率时间序列
from windget import getClauseInterestCompensationInterestSeries


# 获取补偿利率
from windget import getClauseInterestCompensationInterest


# 获取补偿利率(公布)时间序列
from windget import getClauseCompensationInterestSeries


# 获取补偿利率(公布)
from windget import getClauseCompensationInterest


# 获取利息处理方式时间序列
from windget import getClauseProcessModeInterestSeries


# 获取利息处理方式
from windget import getClauseProcessModeInterest


# 获取正股代码时间序列
from windget import getUnderlyingCodeSeries


# 获取正股代码
from windget import getUnderlyingCode


# 获取正股简称时间序列
from windget import getUnderlyingNameSeries


# 获取正股简称
from windget import getUnderlyingName


# 获取相对转股期时间序列
from windget import getClauseConversion2RelativeSwapShareMonthSeries


# 获取相对转股期
from windget import getClauseConversion2RelativeSwapShareMonth


# 获取自愿转股起始日期时间序列
from windget import getClauseConversion2SwapShareStartDateSeries


# 获取自愿转股起始日期
from windget import getClauseConversion2SwapShareStartDate


# 获取自愿转股终止日期时间序列
from windget import getClauseConversion2SwapShareEnddateSeries


# 获取自愿转股终止日期
from windget import getClauseConversion2SwapShareEnddate


# 获取是否强制转股时间序列
from windget import getClauseConversion2IsForcedSeries


# 获取是否强制转股
from windget import getClauseConversion2IsForced


# 获取强制转股日时间序列
from windget import getClauseConversion2ForceConvertDateSeries


# 获取强制转股日
from windget import getClauseConversion2ForceConvertDate


# 获取强制转股价格时间序列
from windget import getClauseConversion2ForceConvertPriceSeries


# 获取强制转股价格
from windget import getClauseConversion2ForceConvertPrice


# 获取转股价格时间序列
from windget import getClauseConversion2SwapSharePriceSeries


# 获取转股价格
from windget import getClauseConversion2SwapSharePrice


# 获取转股代码时间序列
from windget import getClauseConversionCodeSeries


# 获取转股代码
from windget import getClauseConversionCode


# 获取转换比例时间序列
from windget import getClauseConversion2ConversionProportionSeries


# 获取转换比例
from windget import getClauseConversion2ConversionProportion


# 获取未转股余额时间序列
from windget import getClauseConversion2BondLotSeries


# 获取未转股余额
from windget import getClauseConversion2BondLot


# 获取未转股比例时间序列
from windget import getClauseConversion2BondProportionSeries


# 获取未转股比例
from windget import getClauseConversion2BondProportion


# 获取转股价随派息调整时间序列
from windget import getClauseConversion2ConversionProportionSeries


# 获取转股价随派息调整
from windget import getClauseConversion2ConversionProportion


# 获取特别向下修正条款全文时间序列
from windget import getClauseResetItemSeries


# 获取特别向下修正条款全文
from windget import getClauseResetItem


# 获取是否有特别向下修正条款时间序列
from windget import getClauseResetIsExitResetSeries


# 获取是否有特别向下修正条款
from windget import getClauseResetIsExitReset


# 获取特别修正起始时间时间序列
from windget import getClauseResetResetStartDateSeries


# 获取特别修正起始时间
from windget import getClauseResetResetStartDate


# 获取特别修正结束时间时间序列
from windget import getClauseResetResetPeriodEnddateSeries


# 获取特别修正结束时间
from windget import getClauseResetResetPeriodEnddate


# 获取重设触发计算最大时间区间时间序列
from windget import getClauseResetResetMaxTimespanSeries


# 获取重设触发计算最大时间区间
from windget import getClauseResetResetMaxTimespan


# 获取重设触发计算时间区间时间序列
from windget import getClauseResetResetTimespanSeries


# 获取重设触发计算时间区间
from windget import getClauseResetResetTimespan


# 获取触发比例时间序列
from windget import getClauseResetResetTriggerRatioSeries


# 获取触发比例
from windget import getClauseResetResetTriggerRatio


# 获取赎回触发比例时间序列
from windget import getClauseCallOptionTriggerProportionSeries


# 获取赎回触发比例
from windget import getClauseCallOptionTriggerProportion


# 获取回售触发比例时间序列
from windget import getClausePutOptionRedeemTriggerProportionSeries


# 获取回售触发比例
from windget import getClausePutOptionRedeemTriggerProportion


# 获取特别修正幅度时间序列
from windget import getClauseResetResetRangeSeries


# 获取特别修正幅度
from windget import getClauseResetResetRange


# 获取修正价格底线说明时间序列
from windget import getClauseResetStockPriceLowestLimitSeries


# 获取修正价格底线说明
from windget import getClauseResetStockPriceLowestLimit


# 获取修正次数限制时间序列
from windget import getClauseResetResetTimesLimitSeries


# 获取修正次数限制
from windget import getClauseResetResetTimesLimit


# 获取时点修正条款全文时间序列
from windget import getClauseResetTimePointClauseSeries


# 获取时点修正条款全文
from windget import getClauseResetTimePointClause


# 获取相对赎回期时间序列
from windget import getClauseCallOptionRelativeCallOptionPeriodSeries


# 获取相对赎回期
from windget import getClauseCallOptionRelativeCallOptionPeriod


# 获取每年可赎回次数时间序列
from windget import getClauseCallOptionRedemptionTimesPerYearSeries


# 获取每年可赎回次数
from windget import getClauseCallOptionRedemptionTimesPerYear


# 获取条件赎回起始日期时间序列
from windget import getClauseCallOptionConditionalRedeemStartDateSeries


# 获取条件赎回起始日期
from windget import getClauseCallOptionConditionalRedeemStartDate


# 获取条件赎回截止日期时间序列
from windget import getClauseCallOptionConditionalRedeemEnddateSeries


# 获取条件赎回截止日期
from windget import getClauseCallOptionConditionalRedeemEnddate


# 获取赎回触发计算最大时间区间时间序列
from windget import getClauseCallOptionRedeemMaxSpanSeries


# 获取赎回触发计算最大时间区间
from windget import getClauseCallOptionRedeemMaxSpan


# 获取赎回触发计算时间区间时间序列
from windget import getClauseCallOptionRedeemSpanSeries


# 获取赎回触发计算时间区间
from windget import getClauseCallOptionRedeemSpan


# 获取利息处理时间序列
from windget import getClausePutOptionInterestDisposingSeries


# 获取利息处理
from windget import getClausePutOptionInterestDisposing


# 获取时点赎回数时间序列
from windget import getClauseCallOptionTimeRedemptionTimesSeries


# 获取时点赎回数
from windget import getClauseCallOptionTimeRedemptionTimes


# 获取有条件赎回价时间序列
from windget import getConditionalCallPriceSeries


# 获取有条件赎回价
from windget import getConditionalCallPrice


# 获取到期赎回价时间序列
from windget import getMaturityCallPriceSeries


# 获取到期赎回价
from windget import getMaturityCallPrice


# 获取赎回触发价时间序列
from windget import getClauseCallOptionTriggerPriceSeries


# 获取赎回触发价
from windget import getClauseCallOptionTriggerPrice


# 获取赎回公告日时间序列
from windget import getClauseCallOptionNoticeDateSeries


# 获取赎回公告日
from windget import getClauseCallOptionNoticeDate


# 获取相对回售期时间序列
from windget import getClausePutOptionPutBackPeriodObSSeries


# 获取相对回售期
from windget import getClausePutOptionPutBackPeriodObS


# 获取条件回售起始日期时间序列
from windget import getClausePutOptionConditionalPutBackStartEnddateSeries


# 获取条件回售起始日期
from windget import getClausePutOptionConditionalPutBackStartEnddate


# 获取无条件回售起始日期时间序列
from windget import getClausePutOptionPutBackStartDateSeries


# 获取无条件回售起始日期
from windget import getClausePutOptionPutBackStartDate


# 获取条件回售截止日期时间序列
from windget import getClausePutOptionConditionalPutBackEnddateSeries


# 获取条件回售截止日期
from windget import getClausePutOptionConditionalPutBackEnddate


# 获取回售触发计算最大时间区间时间序列
from windget import getClausePutOptionPutBackTriggerMaxSpanSeries


# 获取回售触发计算最大时间区间
from windget import getClausePutOptionPutBackTriggerMaxSpan


# 获取回售触发计算时间区间时间序列
from windget import getClausePutOptionPutBackTriggerSpanSeries


# 获取回售触发计算时间区间
from windget import getClausePutOptionPutBackTriggerSpan


# 获取每年回售次数时间序列
from windget import getClausePutOptionPutBackTimesPerYearSeries


# 获取每年回售次数
from windget import getClausePutOptionPutBackTimesPerYear


# 获取无条件回售期时间序列
from windget import getClausePutOptionPutBackPeriodSeries


# 获取无条件回售期
from windget import getClausePutOptionPutBackPeriod


# 获取无条件回售结束日期时间序列
from windget import getClausePutOptionPutBackEnddateSeries


# 获取无条件回售结束日期
from windget import getClausePutOptionPutBackEnddate


# 获取无条件回售价时间序列
from windget import getClausePutOptionPutBackPriceSeries


# 获取无条件回售价
from windget import getClausePutOptionPutBackPrice


# 获取时点回售数时间序列
from windget import getClausePutOptionTimePutBackTimesSeries


# 获取时点回售数
from windget import getClausePutOptionTimePutBackTimes


# 获取附加回售条件时间序列
from windget import getClausePutOptionPutBackAdditionalConditionSeries


# 获取附加回售条件
from windget import getClausePutOptionPutBackAdditionalCondition


# 获取有条件回售价时间序列
from windget import getConditionalPutPriceSeries


# 获取有条件回售价
from windget import getConditionalPutPrice


# 获取回售触发价时间序列
from windget import getClausePutOptionTriggerPriceSeries


# 获取回售触发价
from windget import getClausePutOptionTriggerPrice


# 获取回售公告日时间序列
from windget import getClausePutOptionNoticeDateSeries


# 获取回售公告日
from windget import getClausePutOptionNoticeDate


# 获取发行时债项评级时间序列
from windget import getCreditRatingSeries


# 获取发行时债项评级
from windget import getCreditRating


# 获取发行时主体评级时间序列
from windget import getIssuerRatingSeries


# 获取发行时主体评级
from windget import getIssuerRating


# 获取发行时主体评级展望时间序列
from windget import getIssuerRatingOutlookSeries


# 获取发行时主体评级展望
from windget import getIssuerRatingOutlook


# 获取发行人委托评级机构时间序列
from windget import getRateCreditRatingAgencySeries


# 获取发行人委托评级机构
from windget import getRateCreditRatingAgency


# 获取发债主体评级机构时间序列
from windget import getIsSurerCreditRatingCompanySeries


# 获取发债主体评级机构
from windget import getIsSurerCreditRatingCompany


# 获取最新债项评级时间序列
from windget import getAmountSeries


# 获取最新债项评级
from windget import getAmount


# 获取最新债项评级日期时间序列
from windget import getRateLatestSeries


# 获取最新债项评级日期
from windget import getRateLatest


# 获取最新债项评级日期(指定机构)时间序列
from windget import getRateLatest1Series


# 获取最新债项评级日期(指定机构)
from windget import getRateLatest1


# 获取最新债项评级变动方向时间序列
from windget import getRateChangesOfRatingSeries


# 获取最新债项评级变动方向
from windget import getRateChangesOfRating


# 获取最新债项评级评级类型时间序列
from windget import getRateStyleSeries


# 获取最新债项评级评级类型
from windget import getRateStyle


# 获取发行人最新最低评级时间序列
from windget import getLowestIsSurerCreditRatingSeries


# 获取发行人最新最低评级
from windget import getLowestIsSurerCreditRating


# 获取债项评级时间序列
from windget import getRateRateBondSeries


# 获取债项评级
from windget import getRateRateBond


# 获取债项评级变动方向时间序列
from windget import getRateChNgBondSeries


# 获取债项评级变动方向
from windget import getRateChNgBond


# 获取债项评级机构时间序列
from windget import getRateAgencyBondSeries


# 获取债项评级机构
from windget import getRateAgencyBond


# 获取历史债项评级时间序列
from windget import getRateFormerSeries


# 获取历史债项评级
from windget import getRateFormer


# 获取(废弃)债项评级(YY)时间序列
from windget import getInStYyBondRatingSeries


# 获取(废弃)债项评级(YY)
from windget import getInStYyBondRating


# 获取主体评级时间序列
from windget import getLatestIsSurerCreditRating2Series


# 获取主体评级
from windget import getLatestIsSurerCreditRating2


# 获取主体评级展望时间序列
from windget import getRateFwdIssuerSeries


# 获取主体评级展望
from windget import getRateFwdIssuer


# 获取主体评级变动方向时间序列
from windget import getRateChNgIssuerSeries


# 获取主体评级变动方向
from windget import getRateChNgIssuer


# 获取主体评级评级机构时间序列
from windget import getRateAgencyIssuerSeries


# 获取主体评级评级机构
from windget import getRateAgencyIssuer


# 获取主体评级(YY)时间序列
from windget import getInStYyIssuerRatingSeries


# 获取主体评级(YY)
from windget import getInStYyIssuerRating


# 获取主体评级历史(YY)时间序列
from windget import getInStYyIssuerRatingHisSeries


# 获取主体评级历史(YY)
from windget import getInStYyIssuerRatingHis


# 获取指定日主体评级时间序列
from windget import getRateIssuerSeries


# 获取指定日主体评级
from windget import getRateIssuer


# 获取发债主体历史信用等级时间序列
from windget import getRateIssuerFormerSeries


# 获取发债主体历史信用等级
from windget import getRateIssuerFormer


# 获取最新授信额度时间序列
from windget import getCreditLineSeries


# 获取最新授信额度
from windget import getCreditLine


# 获取最新已使用授信额度时间序列
from windget import getCreditLineUsedSeries


# 获取最新已使用授信额度
from windget import getCreditLineUsed


# 获取最新未使用授信额度时间序列
from windget import getCreditLineUnusedSeries


# 获取最新未使用授信额度
from windget import getCreditLineUnused


# 获取历史已使用授信额度时间序列
from windget import getCreditLineUsed2Series


# 获取历史已使用授信额度
from windget import getCreditLineUsed2


# 获取历史授信额度时间序列
from windget import getCreditFormerLineSeries


# 获取历史授信额度
from windget import getCreditFormerLine


# 获取最新授信日期时间序列
from windget import getCreditLineDateSeries


# 获取最新授信日期
from windget import getCreditLineDate


# 获取最新担保余额时间序列
from windget import getGuarLatestBalanceSeries


# 获取最新担保余额
from windget import getGuarLatestBalance


# 获取最新对内担保余额时间序列
from windget import getGuarLatestInwardsSeries


# 获取最新对内担保余额
from windget import getGuarLatestInwards


# 获取最新对外担保余额时间序列
from windget import getGuarLatestOutwardsSeries


# 获取最新对外担保余额
from windget import getGuarLatestOutwards


# 获取历史担保余额时间序列
from windget import getGuarFormerBalanceSeries


# 获取历史担保余额
from windget import getGuarFormerBalance


# 获取对内担保余额时间序列
from windget import getGuarFormerInwardsSeries


# 获取对内担保余额
from windget import getGuarFormerInwards


# 获取对外担保余额时间序列
from windget import getGuarFormerOutwardsSeries


# 获取对外担保余额
from windget import getGuarFormerOutwards


# 获取实际可用剩余额度时间序列
from windget import getDCmUnuEsDAmountSeries


# 获取实际可用剩余额度
from windget import getDCmUnuEsDAmount


# 获取已使用注册额度时间序列
from windget import getDCmUeSdAmountSeries


# 获取已使用注册额度
from windget import getDCmUeSdAmount


# 获取首期发行截止日时间序列
from windget import getDCmFirstIssueEnddateSeries


# 获取首期发行截止日
from windget import getDCmFirstIssueEnddate


# 获取未使用注册会议日期时间序列
from windget import getDCmMeetingDataSeries


# 获取未使用注册会议日期
from windget import getDCmMeetingData


# 获取未使用额度有效期时间序列
from windget import getDCmExpirationDataSeries


# 获取未使用额度有效期
from windget import getDCmExpirationData


# 获取最新注册文件编号时间序列
from windget import getDCmNumberSeries


# 获取最新注册文件编号
from windget import getDCmNumber


# 获取未使用额度主承销商时间序列
from windget import getDCmUnderwriterSeries


# 获取未使用额度主承销商
from windget import getDCmUnderwriter


# 获取历史累计注册额度时间序列
from windget import getDCmAcCumAmountSeries


# 获取历史累计注册额度
from windget import getDCmAcCumAmount


# 获取区间发行债券总额时间序列
from windget import getFinaTotalAmount2Series


# 获取区间发行债券总额
from windget import getFinaTotalAmount2


# 获取区间发行债券数目时间序列
from windget import getFinaTotalNumberSeries


# 获取区间发行债券数目
from windget import getFinaTotalNumber


# 获取存量债券数目时间序列
from windget import getFinaRemainingNumberSeries


# 获取存量债券数目
from windget import getFinaRemainingNumber


# 获取基金简称时间序列
from windget import getFundInfoNameSeries


# 获取基金简称
from windget import getFundInfoName


# 获取基金简称(官方)时间序列
from windget import getNameOfficialSeries


# 获取基金简称(官方)
from windget import getNameOfficial


# 获取基金全称时间序列
from windget import getFundFullNameSeries


# 获取基金全称
from windget import getFundFullName


# 获取基金全称(英文)时间序列
from windget import getFundFullNameEnSeries


# 获取基金全称(英文)
from windget import getFundFullNameEn


# 获取基金场内简称时间序列
from windget import getFundExchangeShortnameSeries


# 获取基金场内简称
from windget import getFundExchangeShortname


# 获取基金扩位场内简称时间序列
from windget import getFundExchangeShortnameExtendSeries


# 获取基金扩位场内简称
from windget import getFundExchangeShortnameExtend


# 获取发行机构自编简称时间序列
from windget import getFundIssuerShortnameSeries


# 获取发行机构自编简称
from windget import getFundIssuerShortname


# 获取成立年限时间序列
from windget import getFundExistingYearSeries


# 获取成立年限
from windget import getFundExistingYear


# 获取基金最短持有期时间序列
from windget import getFundMinHoldingPeriodSeries


# 获取基金最短持有期
from windget import getFundMinHoldingPeriod


# 获取基金存续期时间序列
from windget import getFundPtMYearSeries


# 获取基金存续期
from windget import getFundPtMYear


# 获取剩余存续期时间序列
from windget import getFundPtMDaySeries


# 获取剩余存续期
from windget import getFundPtMDay


# 获取业绩比较基准时间序列
from windget import getFundBenchmarkSeries


# 获取业绩比较基准
from windget import getFundBenchmark


# 获取业绩比较基准变更说明时间序列
from windget import getFundChangeOfBenchmarkSeries


# 获取业绩比较基准变更说明
from windget import getFundChangeOfBenchmark


# 获取业绩比较基准增长率时间序列
from windget import getBenchReturnSeries


# 获取业绩比较基准增长率
from windget import getBenchReturn


# 获取报告期业绩比较基准增长率时间序列
from windget import getNavBenchReturnSeries


# 获取报告期业绩比较基准增长率
from windget import getNavBenchReturn


# 获取报告期业绩比较基准增长率标准差时间序列
from windget import getNavBenchStdDevSeries


# 获取报告期业绩比较基准增长率标准差
from windget import getNavBenchStdDev


# 获取单季度.业绩比较基准收益率时间序列
from windget import getQAnalBenchReturnSeries


# 获取单季度.业绩比较基准收益率
from windget import getQAnalBenchReturn


# 获取单季度.业绩比较基准收益率标准差时间序列
from windget import getQAnalStdBenchReturnSeries


# 获取单季度.业绩比较基准收益率标准差
from windget import getQAnalStdBenchReturn


# 获取基准指数代码时间序列
from windget import getFundBenchIndexCodeSeries


# 获取基准指数代码
from windget import getFundBenchIndexCode


# 获取投资目标时间序列
from windget import getFundInvestObjectSeries


# 获取投资目标
from windget import getFundInvestObject


# 获取投资范围时间序列
from windget import getFundInvestScopeSeries


# 获取投资范围
from windget import getFundInvestScope


# 获取投资品种比例限制时间序列
from windget import getFundInvestmentProportionSeries


# 获取投资品种比例限制
from windget import getFundInvestmentProportion


# 获取港股通股票投资比例说明时间序列
from windget import getFundHkScInvestmentProportionSeries


# 获取港股通股票投资比例说明
from windget import getFundHkScInvestmentProportion


# 获取投资理念时间序列
from windget import getFundInvestConceptionSeries


# 获取投资理念
from windget import getFundInvestConception


# 获取投资区域时间序列
from windget import getFundInvestmentRegionSeries


# 获取投资区域
from windget import getFundInvestmentRegion


# 获取主要投资区域说明时间序列
from windget import getFundInvestingRegionDescriptionSeries


# 获取主要投资区域说明
from windget import getFundInvestingRegionDescription


# 获取面值时间序列
from windget import getFundParValueSeries


# 获取面值
from windget import getFundParValue


# 获取是否初始基金时间序列
from windget import getFundInitialSeries


# 获取是否初始基金
from windget import getFundInitial


# 获取是否分级基金时间序列
from windget import getFundStructuredFundOrNotSeries


# 获取是否分级基金
from windget import getFundStructuredFundOrNot


# 获取是否定期开放基金时间序列
from windget import getFundReGulOpenFundOrNotSeries


# 获取是否定期开放基金
from windget import getFundReGulOpenFundOrNot


# 获取是否使用侧袋机制时间序列
from windget import getFundSidePocketFundOrNotSeries


# 获取是否使用侧袋机制
from windget import getFundSidePocketFundOrNot


# 获取产品异常状态时间序列
from windget import getFundExceptionStatusSeries


# 获取产品异常状态
from windget import getFundExceptionStatus


# 获取封闭运作期时间序列
from windget import getFundOperatePeriodClsSeries


# 获取封闭运作期
from windget import getFundOperatePeriodCls


# 获取预期收益率(文字)时间序列
from windget import getExpectedYieldSeries


# 获取预期收益率(文字)
from windget import getExpectedYield


# 获取基金转型说明时间序列
from windget import getFundFundTransitionSeries


# 获取基金转型说明
from windget import getFundFundTransition


# 获取基金估值方法时间序列
from windget import getFundValuationMethodSeries


# 获取基金估值方法
from windget import getFundValuationMethod


# 获取风险收益特征时间序列
from windget import getFundRiskReturnCharactersSeries


# 获取风险收益特征
from windget import getFundRiskReturnCharacters


# 获取市场风险提示时间序列
from windget import getMarketRiskSeries


# 获取市场风险提示
from windget import getMarketRisk


# 获取管理风险提示时间序列
from windget import getManagementRiskSeries


# 获取管理风险提示
from windget import getManagementRisk


# 获取技术风险提示时间序列
from windget import getTechnicalRiskSeries


# 获取技术风险提示
from windget import getTechnicalRisk


# 获取赎回风险提示时间序列
from windget import getRedemptionRiskSeries


# 获取赎回风险提示
from windget import getRedemptionRisk


# 获取其他风险提示时间序列
from windget import getOtherRisksSeries


# 获取其他风险提示
from windget import getOtherRisks


# 获取基金前端代码时间序列
from windget import getFundFrontendCodeSeries


# 获取基金前端代码
from windget import getFundFrontendCode


# 获取基金后端代码时间序列
from windget import getFundBackendCodeSeries


# 获取基金后端代码
from windget import getFundBackendCode


# 获取基金初始代码时间序列
from windget import getFundInitialCodeSeries


# 获取基金初始代码
from windget import getFundInitialCode


# 获取关联基金代码时间序列
from windget import getFundRelatedCodeSeries


# 获取关联基金代码
from windget import getFundRelatedCode


# 获取基金业协会编码时间序列
from windget import getFundAMacCodeSeries


# 获取基金业协会编码
from windget import getFundAMacCode


# 获取理财产品登记编码时间序列
from windget import getFundBWMpRecordCodeSeries


# 获取理财产品登记编码
from windget import getFundBWMpRecordCode


# 获取发行机构自编代码时间序列
from windget import getFundIssuerCodeSeries


# 获取发行机构自编代码
from windget import getFundIssuerCode


# 获取理财产品交易所代码时间序列
from windget import getFundExchangeCodeSeries


# 获取理财产品交易所代码
from windget import getFundExchangeCode


# 获取机构间私募产品报价系统编码时间序列
from windget import getFundPeQuotationCodeSeries


# 获取机构间私募产品报价系统编码
from windget import getFundPeQuotationCode


# 获取基金成立日时间序列
from windget import getFundSetUpdateSeries


# 获取基金成立日
from windget import getFundSetUpdate


# 获取基金到期日时间序列
from windget import getFundMaturityDate2Series


# 获取基金到期日
from windget import getFundMaturityDate2


# 获取基金暂停运作日时间序列
from windget import getFundDateSuspensionSeries


# 获取基金暂停运作日
from windget import getFundDateSuspension


# 获取基金恢复运作日时间序列
from windget import getFundDateResumptionSeries


# 获取基金恢复运作日
from windget import getFundDateResumption


# 获取开始托管日期时间序列
from windget import getFundCuStStartDateSeries


# 获取开始托管日期
from windget import getFundCuStStartDate


# 获取托管结束日期时间序列
from windget import getFundCusTendDateSeries


# 获取托管结束日期
from windget import getFundCusTendDate


# 获取互认基金批复日期时间序列
from windget import getFundRecognitionDateSeries


# 获取互认基金批复日期
from windget import getFundRecognitionDate


# 获取预计封闭期结束日时间序列
from windget import getFundExpectedEndingDaySeries


# 获取预计封闭期结束日
from windget import getFundExpectedEndingDay


# 获取预计下期开放日时间序列
from windget import getFundExpectedOpenDaySeries


# 获取预计下期开放日
from windget import getFundExpectedOpenDay


# 获取定开基金封闭起始日时间序列
from windget import getFundStartDateOfClosureSeries


# 获取定开基金封闭起始日
from windget import getFundStartDateOfClosure


# 获取定开基金上一开放日时间序列
from windget import getFundLastOpenDaySeries


# 获取定开基金上一开放日
from windget import getFundLastOpenDay


# 获取定开基金开放日(支持历史)时间序列
from windget import getFundOpenDaysSeries


# 获取定开基金开放日(支持历史)
from windget import getFundOpenDays


# 获取定开基金已开放次数时间序列
from windget import getFundNumOfOpenDaysSeries


# 获取定开基金已开放次数
from windget import getFundNumOfOpenDays


# 获取上市公告数据截止日期时间序列
from windget import getListDataDateSeries


# 获取上市公告数据截止日期
from windget import getListDataDate


# 获取基金管理人时间序列
from windget import getFundMGrCompSeries


# 获取基金管理人
from windget import getFundMGrComp


# 获取基金管理人简称时间序列
from windget import getFundCorpFundManagementCompanySeries


# 获取基金管理人简称
from windget import getFundCorpFundManagementCompany


# 获取基金管理人英文名称时间序列
from windget import getFundCorpNameEngSeries


# 获取基金管理人英文名称
from windget import getFundCorpNameEng


# 获取基金管理人法人代表时间序列
from windget import getFundCorpChairmanSeries


# 获取基金管理人法人代表
from windget import getFundCorpChairman


# 获取基金管理人电话时间序列
from windget import getFundCorpPhoneSeries


# 获取基金管理人电话
from windget import getFundCorpPhone


# 获取基金管理人传真时间序列
from windget import getFundCorpFaxSeries


# 获取基金管理人传真
from windget import getFundCorpFax


# 获取基金管理人电子邮箱时间序列
from windget import getFundCorpEmailSeries


# 获取基金管理人电子邮箱
from windget import getFundCorpEmail


# 获取基金管理人主页时间序列
from windget import getFundCorpWebsiteSeries


# 获取基金管理人主页
from windget import getFundCorpWebsite


# 获取基金管理人资产净值合计(非货币)时间序列
from windget import getPrtNonMoneyNetAssetsSeries


# 获取基金管理人资产净值合计(非货币)
from windget import getPrtNonMoneyNetAssets


# 获取基金管理人资产净值合计时间序列
from windget import getPrtFundCoTotalNetAssetsSeries


# 获取基金管理人资产净值合计
from windget import getPrtFundCoTotalNetAssets


# 获取基金管理人资产净值合计排名时间序列
from windget import getPrtFundCoTotalNetAssetsRankingSeries


# 获取基金管理人资产净值合计排名
from windget import getPrtFundCoTotalNetAssetsRanking


# 获取基金管理人资产净值合计变动率时间序列
from windget import getPrtFundCoTnaChangeRatioSeries


# 获取基金管理人资产净值合计变动率
from windget import getPrtFundCoTnaChangeRatio


# 获取基金托管人时间序列
from windget import getFundCustodianBankSeries


# 获取基金托管人
from windget import getFundCustodianBank


# 获取基金注册与过户登记人时间序列
from windget import getIssueRegistrarSeries


# 获取基金注册与过户登记人
from windget import getIssueRegistrar


# 获取财务顾问时间序列
from windget import getAgencyFAdvisorSeries


# 获取财务顾问
from windget import getAgencyFAdvisor


# 获取手续费及佣金收入:财务顾问业务时间序列
from windget import getStmNoteSec1504Series


# 获取手续费及佣金收入:财务顾问业务
from windget import getStmNoteSec1504


# 获取手续费及佣金净收入:财务顾问业务时间序列
from windget import getStmNoteSec1524Series


# 获取手续费及佣金净收入:财务顾问业务
from windget import getStmNoteSec1524


# 获取银行理财发行人时间序列
from windget import getFundWmIssuerSeries


# 获取银行理财发行人
from windget import getFundWmIssuer


# 获取境外投资顾问时间序列
from windget import getFundForeignInvestmentAdvisorSeries


# 获取境外投资顾问
from windget import getFundForeignInvestmentAdvisor


# 获取境外托管人时间序列
from windget import getFundForeignCustodianSeries


# 获取境外托管人
from windget import getFundForeignCustodian


# 获取律师事务所时间序列
from windget import getFundCounselorSeries


# 获取律师事务所
from windget import getFundCounselor


# 获取一级交易商时间序列
from windget import getFundPrimaryDealersSeries


# 获取一级交易商
from windget import getFundPrimaryDealers


# 获取基金类型时间序列
from windget import getFundTypeSeries


# 获取基金类型
from windget import getFundType


# 获取投资类型(一级分类)时间序列
from windget import getFundFirstInvestTypeSeries


# 获取投资类型(一级分类)
from windget import getFundFirstInvestType


# 获取投资类型(二级分类)时间序列
from windget import getFundInvestTypeSeries


# 获取投资类型(二级分类)
from windget import getFundInvestType


# 获取投资类型时间序列
from windget import getFundInvestType2Series


# 获取投资类型
from windget import getFundInvestType2


# 获取投资类型(支持历史)时间序列
from windget import getFundInvestTypeAnytimeSeries


# 获取投资类型(支持历史)
from windget import getFundInvestTypeAnytime


# 获取投资类型(英文)时间序列
from windget import getFundInvestTypeEngSeries


# 获取投资类型(英文)
from windget import getFundInvestTypeEng


# 获取基金风险等级时间序列
from windget import getFundRiskLevelSeries


# 获取基金风险等级
from windget import getFundRiskLevel


# 获取基金风险等级(公告口径)时间序列
from windget import getFundRiskLevelFilingSeries


# 获取基金风险等级(公告口径)
from windget import getFundRiskLevelFiling


# 获取基金分级类型时间序列
from windget import getFundSMfType2Series


# 获取基金分级类型
from windget import getFundSMfType2


# 获取同类基金数量时间序列
from windget import getFundSimilarFundNoSeries


# 获取同类基金数量
from windget import getFundSimilarFundNo


# 获取所属主题基金类别时间序列
from windget import getFundThemeTypeSeries


# 获取所属主题基金类别
from windget import getFundThemeType


# 获取所属主题基金类别(Wind概念)时间序列
from windget import getFundThemeTypeConceptSeries


# 获取所属主题基金类别(Wind概念)
from windget import getFundThemeTypeConcept


# 获取所属主题基金类别(Wind行业)时间序列
from windget import getFundThemeTypeIndustrySeries


# 获取所属主题基金类别(Wind行业)
from windget import getFundThemeTypeIndustry


# 获取所属主题基金类别(Wind股票指数)时间序列
from windget import getFundThemeTypeIndexSeries


# 获取所属主题基金类别(Wind股票指数)
from windget import getFundThemeTypeIndex


# 获取管理费率时间序列
from windget import getFundManagementFeeRatioSeries


# 获取管理费率
from windget import getFundManagementFeeRatio


# 获取管理费率(支持历史)时间序列
from windget import getFundManagementFeeRatio2Series


# 获取管理费率(支持历史)
from windget import getFundManagementFeeRatio2


# 获取浮动管理费率说明时间序列
from windget import getFundFloatingMgNtFeedEScripSeries


# 获取浮动管理费率说明
from windget import getFundFloatingMgNtFeedEScrip


# 获取受托人固定管理费率(信托)时间序列
from windget import getFundTrusteeMgNtFeeSeries


# 获取受托人固定管理费率(信托)
from windget import getFundTrusteeMgNtFee


# 获取投资顾问固定管理费率(信托)时间序列
from windget import getFundInvAdviserMgNtFeeSeries


# 获取投资顾问固定管理费率(信托)
from windget import getFundInvAdviserMgNtFee


# 获取是否收取浮动管理费时间序列
from windget import getFundFloatingMgNtFeeOrNotSeries


# 获取是否收取浮动管理费
from windget import getFundFloatingMgNtFeeOrNot


# 获取托管费率时间序列
from windget import getFundCustodianFeeRatioSeries


# 获取托管费率
from windget import getFundCustodianFeeRatio


# 获取托管费率(支持历史)时间序列
from windget import getFundCustodianFeeRatio2Series


# 获取托管费率(支持历史)
from windget import getFundCustodianFeeRatio2


# 获取销售服务费率时间序列
from windget import getFundSaleFeeRatioSeries


# 获取销售服务费率
from windget import getFundSaleFeeRatio


# 获取销售服务费率(支持历史)时间序列
from windget import getFundSaleFeeRatio2Series


# 获取销售服务费率(支持历史)
from windget import getFundSaleFeeRatio2


# 获取最高申购费率时间序列
from windget import getFundPurchaseFeeRatioSeries


# 获取最高申购费率
from windget import getFundPurchaseFeeRatio


# 获取最高赎回费率时间序列
from windget import getFundRedemptionFeeRatioSeries


# 获取最高赎回费率
from windget import getFundRedemptionFeeRatio


# 获取认购费率时间序列
from windget import getFundSubscriptionFeeSeries


# 获取认购费率
from windget import getFundSubscriptionFee


# 获取认购费率(支持历史)时间序列
from windget import getFundSubscriptionFee2Series


# 获取认购费率(支持历史)
from windget import getFundSubscriptionFee2


# 获取申购费率时间序列
from windget import getFundPurchaseFeeSeries


# 获取申购费率
from windget import getFundPurchaseFee


# 获取申购费率(支持历史)时间序列
from windget import getFundPurchaseFee2Series


# 获取申购费率(支持历史)
from windget import getFundPurchaseFee2


# 获取申购费率上限时间序列
from windget import getFundPChRedMPChMaxFeeSeries


# 获取申购费率上限
from windget import getFundPChRedMPChMaxFee


# 获取赎回费率时间序列
from windget import getFundRedemptionFeeSeries


# 获取赎回费率
from windget import getFundRedemptionFee


# 获取赎回费率(支持历史)时间序列
from windget import getFundRedemptionFee2Series


# 获取赎回费率(支持历史)
from windget import getFundRedemptionFee2


# 获取赎回费率上限时间序列
from windget import getFundPChRedMMaxRedMFeeSeries


# 获取赎回费率上限
from windget import getFundPChRedMMaxRedMFee


# 获取指数使用费率时间序列
from windget import getFundIndexUsageFeeRatioSeries


# 获取指数使用费率
from windget import getFundIndexUsageFeeRatio


# 获取申购赎回简称时间序列
from windget import getFundPurchaseAndRedemptionAbbreviationSeries


# 获取申购赎回简称
from windget import getFundPurchaseAndRedemptionAbbreviation


# 获取申购赎回状态时间序列
from windget import getFundDQStatusSeries


# 获取申购赎回状态
from windget import getFundDQStatus


# 获取申购状态时间序列
from windget import getFundPcHmStatusSeries


# 获取申购状态
from windget import getFundPcHmStatus


# 获取赎回状态时间序列
from windget import getFundRedMStatusSeries


# 获取赎回状态
from windget import getFundRedMStatus


# 获取申购起始日时间序列
from windget import getFundPChRedMPChStartDateSeries


# 获取申购起始日
from windget import getFundPChRedMPChStartDate


# 获取网下申购起始日期时间序列
from windget import getIpoOpStartDateSeries


# 获取网下申购起始日期
from windget import getIpoOpStartDate


# 获取单日大额申购限额时间序列
from windget import getFundPChRedMLargePChMaxAmtSeries


# 获取单日大额申购限额
from windget import getFundPChRedMLargePChMaxAmt


# 获取申购金额下限(场外)时间序列
from windget import getFundPChRedMPcHmInAmtSeries


# 获取申购金额下限(场外)
from windget import getFundPChRedMPcHmInAmt


# 获取申购金额下限(场内)时间序列
from windget import getFundPChRedMPcHmInAmtFloorSeries


# 获取申购金额下限(场内)
from windget import getFundPChRedMPcHmInAmtFloor


# 获取赎回起始日时间序列
from windget import getFundRedMStartDateSeries


# 获取赎回起始日
from windget import getFundRedMStartDate


# 获取单笔赎回份额下限时间序列
from windget import getFundPChRedMRedMmInAmtSeries


# 获取单笔赎回份额下限
from windget import getFundPChRedMRedMmInAmt


# 获取申购确认日时间序列
from windget import getFundPChConfirmDateSeries


# 获取申购确认日
from windget import getFundPChConfirmDate


# 获取赎回确认日时间序列
from windget import getFundRedMConfirmDateSeries


# 获取赎回确认日
from windget import getFundRedMConfirmDate


# 获取赎回划款日时间序列
from windget import getFundRedMarriAlDateSeries


# 获取赎回划款日
from windget import getFundRedMarriAlDate


# 获取旗下基金数时间序列
from windget import getFundCorpFundNoSeries


# 获取旗下基金数
from windget import getFundCorpFundNo


# 获取五星基金占比时间序列
from windget import getFundCorpFiveStarFundsPropSeries


# 获取五星基金占比
from windget import getFundCorpFiveStarFundsProp


# 获取四星基金占比时间序列
from windget import getFundCorpFourStarFundsPropSeries


# 获取四星基金占比
from windget import getFundCorpFourStarFundsProp


# 获取团队稳定性时间序列
from windget import getFundCorpTeamStabilitySeries


# 获取团队稳定性
from windget import getFundCorpTeamStability


# 获取跟踪指数代码时间序列
from windget import getFundTrackIndexCodeSeries


# 获取跟踪指数代码
from windget import getFundTrackIndexCode


# 获取跟踪指数名称时间序列
from windget import getFundTrackIndexNameSeries


# 获取跟踪指数名称
from windget import getFundTrackIndexName


# 获取日均跟踪偏离度阈值(业绩基准)时间序列
from windget import getFundTrackDeviationThresholdSeries


# 获取日均跟踪偏离度阈值(业绩基准)
from windget import getFundTrackDeviationThreshold


# 获取年化跟踪误差阈值(业绩基准)时间序列
from windget import getFundTrackErrorThresholdSeries


# 获取年化跟踪误差阈值(业绩基准)
from windget import getFundTrackErrorThreshold


# 获取分级基金类别时间序列
from windget import getFundSMfTypeSeries


# 获取分级基金类别
from windget import getFundSMfType


# 获取分级基金母基金代码时间序列
from windget import getFundSMfCodeSeries


# 获取分级基金母基金代码
from windget import getFundSMfCode


# 获取分级基金优先级代码时间序列
from windget import getFundSMfaCodeSeries


# 获取分级基金优先级代码
from windget import getFundSMfaCode


# 获取分级基金普通级代码时间序列
from windget import getFundSmFbCodeSeries


# 获取分级基金普通级代码
from windget import getFundSmFbCode


# 获取拆分比率时间序列
from windget import getFundSplitRatioSeries


# 获取拆分比率
from windget import getFundSplitRatio


# 获取分级份额占比时间序列
from windget import getFundSubShareProportionSeries


# 获取分级份额占比
from windget import getFundSubShareProportion


# 获取初始杠杆时间序列
from windget import getFundInitialLeverSeries


# 获取初始杠杆
from windget import getFundInitialLever


# 获取约定年收益率表达式时间序列
from windget import getFundAAyeIlDInfoSeries


# 获取约定年收益率表达式
from windget import getFundAAyeIlDInfo


# 获取是否配对转换时间序列
from windget import getFundPairConversionSeries


# 获取是否配对转换
from windget import getFundPairConversion


# 获取定期折算周期时间序列
from windget import getFundDiscountPeriodSeries


# 获取定期折算周期
from windget import getFundDiscountPeriod


# 获取定期折算条款时间序列
from windget import getFundDiscountMethodSeries


# 获取定期折算条款
from windget import getFundDiscountMethod


# 获取向上触点折算条款时间序列
from windget import getFundUpDiscountSeries


# 获取向上触点折算条款
from windget import getFundUpDiscount


# 获取向下触点折算条款时间序列
from windget import getFundDownDiscountSeries


# 获取向下触点折算条款
from windget import getFundDownDiscount


# 获取保本周期时间序列
from windget import getFundGuaranteedCycleSeries


# 获取保本周期
from windget import getFundGuaranteedCycle


# 获取保本周期起始日期时间序列
from windget import getFundGuaranteedCycleStartDateSeries


# 获取保本周期起始日期
from windget import getFundGuaranteedCycleStartDate


# 获取保本周期终止日期时间序列
from windget import getFundGuaranteedCycleEnddateSeries


# 获取保本周期终止日期
from windget import getFundGuaranteedCycleEnddate


# 获取保本费率时间序列
from windget import getFundGuaranteedFeeRateSeries


# 获取保本费率
from windget import getFundGuaranteedFeeRate


# 获取保证人时间序列
from windget import getFundWarrantOrSeries


# 获取保证人
from windget import getFundWarrantOr


# 获取保证人简介时间序列
from windget import getFundWarrantOrIntroductionSeries


# 获取保证人简介
from windget import getFundWarrantOrIntroduction


# 获取保本触发收益率时间序列
from windget import getFundGuaranteedTriggerRatioSeries


# 获取保本触发收益率
from windget import getFundGuaranteedTriggerRatio


# 获取保本触发机制说明时间序列
from windget import getFundGuaranteedTriggerTxtSeries


# 获取保本触发机制说明
from windget import getFundGuaranteedTriggerTxt


# 获取计划类型(券商集合理财)时间序列
from windget import getFundPlanTypeSeries


# 获取计划类型(券商集合理财)
from windget import getFundPlanType


# 获取是否提取业绩报酬(券商集合理财)时间序列
from windget import getFundPerformanceFeeOrNotSeries


# 获取是否提取业绩报酬(券商集合理财)
from windget import getFundPerformanceFeeOrNot


# 获取业绩报酬提取方法时间序列
from windget import getFundPerformanceFeeMethodSeries


# 获取业绩报酬提取方法
from windget import getFundPerformanceFeeMethod


# 获取管理费说明时间序列
from windget import getFundMgNtFeeExplainSeries


# 获取管理费说明
from windget import getFundMgNtFeeExplain


# 获取信托类别(信托)时间序列
from windget import getTrustTypeSeries


# 获取信托类别(信托)
from windget import getTrustType


# 获取信托投资领域时间序列
from windget import getTrustInvestFieldSeries


# 获取信托投资领域
from windget import getTrustInvestField


# 获取信托产品类别时间序列
from windget import getTrustSourceTypeSeries


# 获取信托产品类别
from windget import getTrustSourceType


# 获取预计年收益率(信托)时间序列
from windget import getFundExpectedRateOfReturnSeries


# 获取预计年收益率(信托)
from windget import getFundExpectedRateOfReturn


# 获取是否结构化产品(信托)时间序列
from windget import getFundStructuredOrNotSeries


# 获取是否结构化产品(信托)
from windget import getFundStructuredOrNot


# 获取受托人(信托)时间序列
from windget import getFundTrusteeSeries


# 获取受托人(信托)
from windget import getFundTrustee


# 获取证券经纪人(信托)时间序列
from windget import getFundSecuritiesBrokerSeries


# 获取证券经纪人(信托)
from windget import getFundSecuritiesBroker


# 获取发行地(信托)时间序列
from windget import getFundIssuingPlaceSeries


# 获取发行地(信托)
from windget import getFundIssuingPlace


# 获取浮动收益说明(信托)时间序列
from windget import getFundFloatingRateNoteSeries


# 获取浮动收益说明(信托)
from windget import getFundFloatingRateNote


# 获取一般受益权金额(信托)时间序列
from windget import getFundGeneralBeneficialAmountSeries


# 获取一般受益权金额(信托)
from windget import getFundGeneralBeneficialAmount


# 获取优先受益权金额(信托)时间序列
from windget import getFundPriorityBeneficialAmountSeries


# 获取优先受益权金额(信托)
from windget import getFundPriorityBeneficialAmount


# 获取委托资金比(优先/一般)(信托)时间序列
from windget import getFundPriorityToGeneralSeries


# 获取委托资金比(优先/一般)(信托)
from windget import getFundPriorityToGeneral


# 获取发行信托合同总数(信托)时间序列
from windget import getFundIssuedContractAmountSeries


# 获取发行信托合同总数(信托)
from windget import getFundIssuedContractAmount


# 获取信用增级情况时间序列
from windget import getAdvanceCreditDescSeries


# 获取信用增级情况
from windget import getAdvanceCreditDesc


# 获取预期收益率说明时间序列
from windget import getAnticipateYieldDescSeries


# 获取预期收益率说明
from windget import getAnticipateYieldDesc


# 获取信托项目关联企业名称时间序列
from windget import getTrustRelatedFirmSeries


# 获取信托项目关联企业名称
from windget import getTrustRelatedFirm


# 获取销售起始日期时间序列
from windget import getFundSubStartDateSeries


# 获取销售起始日期
from windget import getFundSubStartDate


# 获取销售截止日期时间序列
from windget import getFundSubEnddateSeries


# 获取销售截止日期
from windget import getFundSubEnddate


# 获取目标规模时间序列
from windget import getFundTargetScaleSeries


# 获取目标规模
from windget import getFundTargetScale


# 获取有效认购户数时间序列
from windget import getFundEffSubsCrHoleDerNoSeries


# 获取有效认购户数
from windget import getFundEffSubsCrHoleDerNo


# 获取最低参与金额时间序列
from windget import getFundMinBuyAmountSeries


# 获取最低参与金额
from windget import getFundMinBuyAmount


# 获取追加认购最低金额时间序列
from windget import getFundMinAddBuyAmountSeries


# 获取追加认购最低金额
from windget import getFundMinAddBuyAmount


# 获取管理人参与金额时间序列
from windget import getFundManagersBuyAmountSeries


# 获取管理人参与金额
from windget import getFundManagersBuyAmount


# 获取开放日说明时间序列
from windget import getFundOpenDayIllUsSeries


# 获取开放日说明
from windget import getFundOpenDayIllUs


# 获取封闭期说明时间序列
from windget import getFundCloseDayIllUsSeries


# 获取封闭期说明
from windget import getFundCloseDayIllUs


# 获取投资策略分类(一级)(私募)时间序列
from windget import getFundFirstInvestStrategySeries


# 获取投资策略分类(一级)(私募)
from windget import getFundFirstInvestStrategy


# 获取投资策略分类(二级)(私募)时间序列
from windget import getFundSecondInvestStrategySeries


# 获取投资策略分类(二级)(私募)
from windget import getFundSecondInvestStrategy


# 获取产品发行渠道时间序列
from windget import getIssueChannelSeries


# 获取产品发行渠道
from windget import getIssueChannel


# 获取投资顾问时间序列
from windget import getFundInvestmentAdvisorSeries


# 获取投资顾问
from windget import getFundInvestmentAdvisor


# 获取基金净值更新频率时间序列
from windget import getNavUpdateFrequencySeries


# 获取基金净值更新频率
from windget import getNavUpdateFrequency


# 获取基金净值完整度时间序列
from windget import getNavUpdateCompletenessSeries


# 获取基金净值完整度
from windget import getNavUpdateCompleteness


# 获取协会备案管理人在管规模时间序列
from windget import getFundManageScaleIntervalSeries


# 获取协会备案管理人在管规模
from windget import getFundManageScaleInterval


# 获取是否保本时间序列
from windget import getFundGuaranteedOrNotSeries


# 获取是否保本
from windget import getFundGuaranteedOrNot


# 获取银行理财风险等级(银行)时间序列
from windget import getFundLcRiskLevelSeries


# 获取银行理财风险等级(银行)
from windget import getFundLcRiskLevel


# 获取产品运作方式时间序列
from windget import getFundOperationModeSeries


# 获取产品运作方式
from windget import getFundOperationMode


# 获取业务模式时间序列
from windget import getFundBusinessModeSeries


# 获取业务模式
from windget import getFundBusinessMode


# 获取收益起始日时间序列
from windget import getFundReturnStartDateSeries


# 获取收益起始日
from windget import getFundReturnStartDate


# 获取收益终止日时间序列
from windget import getFundReturnEnddateSeries


# 获取收益终止日
from windget import getFundReturnEnddate


# 获取实际运作期限时间序列
from windget import getFundActualDurationSeries


# 获取实际运作期限
from windget import getFundActualDuration


# 获取委托金额上限时间序列
from windget import getFundMaxSubScripAmountSeries


# 获取委托金额上限
from windget import getFundMaxSubScripAmount


# 获取实际年化收益率时间序列
from windget import getFundActualAnnualYieldSeries


# 获取实际年化收益率
from windget import getFundActualAnnualYield


# 获取实际到期日时间序列
from windget import getFundActualMaturityDateSeries


# 获取实际到期日
from windget import getFundActualMaturityDate


# 获取付息方式说明时间序列
from windget import getFundInterestPayMethodSeries


# 获取付息方式说明
from windget import getFundInterestPayMethod


# 获取资金到账天数时间序列
from windget import getFundFundArrivalDaysSeries


# 获取资金到账天数
from windget import getFundFundArrivalDays


# 获取是否可提前终止时间序列
from windget import getFundEarlyTerminationOrNotSeries


# 获取是否可提前终止
from windget import getFundEarlyTerminationOrNot


# 获取提前终止条件时间序列
from windget import getFundCNdPreTerminationSeries


# 获取提前终止条件
from windget import getFundCNdPreTermination


# 获取申购赎回条件时间序列
from windget import getFundCNdpUrchRedemptionSeries


# 获取申购赎回条件
from windget import getFundCNdpUrchRedemption


# 获取收益挂钩标的时间序列
from windget import getFundUnderlyingTargetSeries


# 获取收益挂钩标的
from windget import getFundUnderlyingTarget


# 获取主要风险点时间序列
from windget import getFundMainRiskSeries


# 获取主要风险点
from windget import getFundMainRisk


# 获取资产类型时间序列
from windget import getFundReItsTypeSeries


# 获取资产类型
from windget import getFundReItsType


# 获取项目介绍时间序列
from windget import getFundReItsInfoSeries


# 获取项目介绍
from windget import getFundReItsInfo


# 获取询价区间上限时间序列
from windget import getFundReItsPriceMaxSeries


# 获取询价区间上限
from windget import getFundReItsPriceMax


# 获取询价区间下限时间序列
from windget import getFundReItsPriceMinSeries


# 获取询价区间下限
from windget import getFundReItsPriceMin


# 获取战略发售起始日时间序列
from windget import getFundReItsSIsTDateSeries


# 获取战略发售起始日
from windget import getFundReItsSIsTDate


# 获取战略发售截止日时间序列
from windget import getFundReItsSienDateSeries


# 获取战略发售截止日
from windget import getFundReItsSienDate


# 获取战略投资方认购份额时间序列
from windget import getFundReItsSiShareSubSeries


# 获取战略投资方认购份额
from windget import getFundReItsSiShareSub


# 获取战略配售份额时间序列
from windget import getFundReItsSiShareSeries


# 获取战略配售份额
from windget import getFundReItsSiShare


# 获取战略配售份额占比时间序列
from windget import getFundReItsSiShareRaSeries


# 获取战略配售份额占比
from windget import getFundReItsSiShareRa


# 获取战略投资方认购比例时间序列
from windget import getFundReItsSiRatioSeries


# 获取战略投资方认购比例
from windget import getFundReItsSiRatio


# 获取网下发售起始日时间序列
from windget import getFundReItsOffStDateSeries


# 获取网下发售起始日
from windget import getFundReItsOffStDate


# 获取网下发售截止日时间序列
from windget import getFundReItsOffendAteSeries


# 获取网下发售截止日
from windget import getFundReItsOffendAte


# 获取网下认购份额时间序列
from windget import getFundReItSoIsHareSeries


# 获取网下认购份额
from windget import getFundReItSoIsHare


# 获取网下配售份额时间序列
from windget import getFundReItsOffShareSeries


# 获取网下配售份额
from windget import getFundReItsOffShare


# 获取网下配售份额占比时间序列
from windget import getFundReItsOffShareRaSeries


# 获取网下配售份额占比
from windget import getFundReItsOffShareRa


# 获取网下投资方认购比例时间序列
from windget import getFundReItSoIRatioSeries


# 获取网下投资方认购比例
from windget import getFundReItSoIRatio


# 获取公众发售起始日时间序列
from windget import getFundReItsPbsTDateSeries


# 获取公众发售起始日
from windget import getFundReItsPbsTDate


# 获取公众发售截止日时间序列
from windget import getFundReItsPBenDateSeries


# 获取公众发售截止日
from windget import getFundReItsPBenDate


# 获取公众认购份额时间序列
from windget import getFundReItsPiShareSeries


# 获取公众认购份额
from windget import getFundReItsPiShare


# 获取公众配售份额时间序列
from windget import getFundReItsPbShareSeries


# 获取公众配售份额
from windget import getFundReItsPbShare


# 获取公众配售份额占比时间序列
from windget import getFundReItsPbShareRaSeries


# 获取公众配售份额占比
from windget import getFundReItsPbShareRa


# 获取公众投资方认购比例时间序列
from windget import getFundReItsPiRatioSeries


# 获取公众投资方认购比例
from windget import getFundReItsPiRatio


# 获取项目运营风险时间序列
from windget import getFundReItsOpRiskSeries


# 获取项目运营风险
from windget import getFundReItsOpRisk


# 获取资产名称时间序列
from windget import getFundReItsAsNameSeries


# 获取资产名称
from windget import getFundReItsAsName


# 获取资产所在地时间序列
from windget import getFundReItsLocationSeries


# 获取资产所在地
from windget import getFundReItsLocation


# 获取项目公司名称时间序列
from windget import getFundReItsComNameSeries


# 获取项目公司名称
from windget import getFundReItsComName


# 获取网下机构自营投资账户配售数量时间序列
from windget import getFundReItsPIsSeries


# 获取网下机构自营投资账户配售数量
from windget import getFundReItsPIs


# 获取网下机构自营投资账户配售金额时间序列
from windget import getFundReItsPimSeries


# 获取网下机构自营投资账户配售金额
from windget import getFundReItsPim


# 获取网下机构自营投资账户配售份额占比时间序列
from windget import getFundReItsPirSeries


# 获取网下机构自营投资账户配售份额占比
from windget import getFundReItsPir


# 获取网下私募基金配售数量时间序列
from windget import getFundReItsPfsSeries


# 获取网下私募基金配售数量
from windget import getFundReItsPfs


# 获取网下私募基金配售金额时间序列
from windget import getFundReItsPFmSeries


# 获取网下私募基金配售金额
from windget import getFundReItsPFm


# 获取网下私募基金配售份额占比时间序列
from windget import getFundReItsPFrSeries


# 获取网下私募基金配售份额占比
from windget import getFundReItsPFr


# 获取网下保险资金投资账户配售数量时间序列
from windget import getFundReItsIsSSeries


# 获取网下保险资金投资账户配售数量
from windget import getFundReItsIsS


# 获取网下保险资金投资账户配售金额时间序列
from windget import getFundReItsIsMSeries


# 获取网下保险资金投资账户配售金额
from windget import getFundReItsIsM


# 获取网下保险资金投资账户配售份额占比时间序列
from windget import getFundReItsIsRSeries


# 获取网下保险资金投资账户配售份额占比
from windget import getFundReItsIsR


# 获取网下集合信托计划配售数量时间序列
from windget import getFundReItsTrsSeries


# 获取网下集合信托计划配售数量
from windget import getFundReItsTrs


# 获取网下集合信托计划配售金额时间序列
from windget import getFundReItsTrmSeries


# 获取网下集合信托计划配售金额
from windget import getFundReItsTrm


# 获取网下集合信托计划配售份额占比时间序列
from windget import getFundReItsTrRSeries


# 获取网下集合信托计划配售份额占比
from windget import getFundReItsTrR


# 获取网下证券公司集合资产管理计划配售数量时间序列
from windget import getFundReItsScSSeries


# 获取网下证券公司集合资产管理计划配售数量
from windget import getFundReItsScS


# 获取网下证券公司集合资产管理计划配售金额时间序列
from windget import getFundReItsSCmSeries


# 获取网下证券公司集合资产管理计划配售金额
from windget import getFundReItsSCm


# 获取网下证券公司集合资产管理计划配售份额占比时间序列
from windget import getFundReItsSCrSeries


# 获取网下证券公司集合资产管理计划配售份额占比
from windget import getFundReItsSCr


# 获取网下证券公司单一资产管理计划配售数量时间序列
from windget import getFundReItsSCssSeries


# 获取网下证券公司单一资产管理计划配售数量
from windget import getFundReItsSCss


# 获取网下证券公司单一资产管理计划配售金额时间序列
from windget import getFundReItsScSmSeries


# 获取网下证券公司单一资产管理计划配售金额
from windget import getFundReItsScSm


# 获取网下证券公司单一资产管理计划配售份额占比时间序列
from windget import getFundReItsSCsrSeries


# 获取网下证券公司单一资产管理计划配售份额占比
from windget import getFundReItsSCsr


# 获取限售份额时间序列
from windget import getFundReItsLimitedShareSeries


# 获取限售份额
from windget import getFundReItsLimitedShare


# 获取估价收益率(%)(中债)时间序列
from windget import getYieldCnBdSeries


# 获取估价收益率(%)(中债)
from windget import getYieldCnBd


# 获取估价净价(中债)时间序列
from windget import getNetCnBdSeries


# 获取估价净价(中债)
from windget import getNetCnBd


# 获取估价全价(中债)时间序列
from windget import getDirtyCnBdSeries


# 获取估价全价(中债)
from windget import getDirtyCnBd


# 获取日终估价全价(中债)时间序列
from windget import getPriceCnBdSeries


# 获取日终估价全价(中债)
from windget import getPriceCnBd


# 获取估价修正久期(中债)时间序列
from windget import getModiDuraCnBdSeries


# 获取估价修正久期(中债)
from windget import getModiDuraCnBd


# 获取待偿年限(年)(中债)时间序列
from windget import getMatUCnBdSeries


# 获取待偿年限(年)(中债)
from windget import getMatUCnBd


# 获取应计利息(中债)时间序列
from windget import getAccruedInterestCnBdSeries


# 获取应计利息(中债)
from windget import getAccruedInterestCnBd


# 获取日终应计利息(中债)时间序列
from windget import getAccRIntDayEndCnBdSeries


# 获取日终应计利息(中债)
from windget import getAccRIntDayEndCnBd


# 获取估价利差久期(中债)时间序列
from windget import getSprDuraCnBdSeries


# 获取估价利差久期(中债)
from windget import getSprDuraCnBd


# 获取估价利率久期(中债)时间序列
from windget import getInterestDurationCnBdSeries


# 获取估价利率久期(中债)
from windget import getInterestDurationCnBd


# 获取点差收益率(中债)时间序列
from windget import getSpreadYieldCnBdSeries


# 获取点差收益率(中债)
from windget import getSpreadYieldCnBd


# 获取估价凸性(中债)时间序列
from windget import getCNvXTyCnBdSeries


# 获取估价凸性(中债)
from windget import getCNvXTyCnBd


# 获取估价利差凸性(中债)时间序列
from windget import getSPrcNxtCnBdSeries


# 获取估价利差凸性(中债)
from windget import getSPrcNxtCnBd


# 获取估价利率凸性(中债)时间序列
from windget import getInterestCNvXTyCnBdSeries


# 获取估价利率凸性(中债)
from windget import getInterestCNvXTyCnBd


# 获取加权平均结算收益率(%)(中债)时间序列
from windget import getMcYieldCnBdSeries


# 获取加权平均结算收益率(%)(中债)
from windget import getMcYieldCnBd


# 获取加权平均结算净价(中债)时间序列
from windget import getMCnetCnBdSeries


# 获取加权平均结算净价(中债)
from windget import getMCnetCnBd


# 获取加权平均结算全价(中债)时间序列
from windget import getMDirtyCnBdSeries


# 获取加权平均结算全价(中债)
from windget import getMDirtyCnBd


# 获取市场隐含评级(中债)时间序列
from windget import getRateLatestMirCnBdSeries


# 获取市场隐含评级(中债)
from windget import getRateLatestMirCnBd


# 获取市场历史隐含评级(中债)时间序列
from windget import getRateHistoricalMirCnBdSeries


# 获取市场历史隐含评级(中债)
from windget import getRateHistoricalMirCnBd


# 获取最新估值日期(中债)时间序列
from windget import getLastDateCnBdSeries


# 获取最新估值日期(中债)
from windget import getLastDateCnBd


# 获取估算的行权后票面利率时间序列
from windget import getExerciseCouponRateCnBdSeries


# 获取估算的行权后票面利率
from windget import getExerciseCouponRateCnBd


# 获取剩余本金(中债)时间序列
from windget import getLatestParCnBdSeries


# 获取剩余本金(中债)
from windget import getLatestParCnBd


# 获取估价收益率(中证指数)时间序列
from windget import getYieldCsi1Series


# 获取估价收益率(中证指数)
from windget import getYieldCsi1


# 获取估价净价(中证指数)时间序列
from windget import getNetCsi1Series


# 获取估价净价(中证指数)
from windget import getNetCsi1


# 获取估价全价(中证指数)时间序列
from windget import getDirtyCsi1Series


# 获取估价全价(中证指数)
from windget import getDirtyCsi1


# 获取估价修正久期(中证指数)时间序列
from windget import getModiDuraCsi1Series


# 获取估价修正久期(中证指数)
from windget import getModiDuraCsi1


# 获取应计利息(中证指数)时间序列
from windget import getAccruedInterestCsiSeries


# 获取应计利息(中证指数)
from windget import getAccruedInterestCsi


# 获取估价凸性(中证指数)时间序列
from windget import getCNvXTyCsi1Series


# 获取估价凸性(中证指数)
from windget import getCNvXTyCsi1


# 获取最新估值日期(中证指数)时间序列
from windget import getLastDateCsiSeries


# 获取最新估值日期(中证指数)
from windget import getLastDateCsi


# 获取隐含评级(中证指数)时间序列
from windget import getRateLatestMirCsiSeries


# 获取隐含评级(中证指数)
from windget import getRateLatestMirCsi


# 获取隐含违约率(中证指数)时间序列
from windget import getRateDefaultCsiSeries


# 获取隐含违约率(中证指数)
from windget import getRateDefaultCsi


# 获取可交换债估值(中证指数)时间序列
from windget import getEbValCsiSeries


# 获取可交换债估值(中证指数)
from windget import getEbValCsi


# 获取可交换债期权价值(中证指数)时间序列
from windget import getEbOptionValCsiSeries


# 获取可交换债期权价值(中证指数)
from windget import getEbOptionValCsi


# 获取可交换债纯债溢价率(中证指数)时间序列
from windget import getEbBondPreCsiSeries


# 获取可交换债纯债溢价率(中证指数)
from windget import getEbBondPreCsi


# 获取可交换债估值收益率(中证指数)时间序列
from windget import getEbValYieldCsiSeries


# 获取可交换债估值收益率(中证指数)
from windget import getEbValYieldCsi


# 获取可交换债转股溢价率(中证指数)时间序列
from windget import getEbConversionPreCsiSeries


# 获取可交换债转股溢价率(中证指数)
from windget import getEbConversionPreCsi


# 获取估价收益率(上清所)时间序列
from windget import getYieldShcSeries


# 获取估价收益率(上清所)
from windget import getYieldShc


# 获取估价净价(上清所)时间序列
from windget import getNetShcSeries


# 获取估价净价(上清所)
from windget import getNetShc


# 获取估价全价(上清所)时间序列
from windget import getDirtyShcSeries


# 获取估价全价(上清所)
from windget import getDirtyShc


# 获取估价修正久期(上清所)时间序列
from windget import getModiDuraShcSeries


# 获取估价修正久期(上清所)
from windget import getModiDuraShc


# 获取应计利息(上清所)时间序列
from windget import getAccruedInterestShcSeries


# 获取应计利息(上清所)
from windget import getAccruedInterestShc


# 获取估价凸性(上清所)时间序列
from windget import getCNvXTyShcSeries


# 获取估价凸性(上清所)
from windget import getCNvXTyShc


# 获取最新估值日期(上清所)时间序列
from windget import getLastDateShcSeries


# 获取最新估值日期(上清所)
from windget import getLastDateShc


# 获取指数值(中债)时间序列
from windget import getDQCloseCnBdSeries


# 获取指数值(中债)
from windget import getDQCloseCnBd


# 获取现券结算量(中债)时间序列
from windget import getDQAmountCnBdSeries


# 获取现券结算量(中债)
from windget import getDQAmountCnBd


# 获取平均市值法凸性时间序列
from windget import getAnalCapConvexitySeries


# 获取平均市值法凸性
from windget import getAnalCapConvexity


# 获取平均市值法久期时间序列
from windget import getAnalCapDurationSeries


# 获取平均市值法久期
from windget import getAnalCapDuration


# 获取平均市值法到期收益率时间序列
from windget import getAnalCapYTMSeries


# 获取平均市值法到期收益率
from windget import getAnalCapYTM


# 获取平均现金流法凸性时间序列
from windget import getAnalCashFlowConvexitySeries


# 获取平均现金流法凸性
from windget import getAnalCashFlowConvexity


# 获取平均现金流法久期时间序列
from windget import getAnalCashFlowDurationSeries


# 获取平均现金流法久期
from windget import getAnalCashFlowDuration


# 获取平均现金流法到期收益率时间序列
from windget import getAnalCashFlowYTMSeries


# 获取平均现金流法到期收益率
from windget import getAnalCashFlowYTM


# 获取平均派息率时间序列
from windget import getAnalIpRatioSeries


# 获取平均派息率
from windget import getAnalIpRatio


# 获取平均待偿期时间序列
from windget import getAnalPeriodSeries


# 获取平均待偿期
from windget import getAnalPeriod


# 获取上证固收平台成交金额时间序列
from windget import getAmountFixedIncomeSeries


# 获取上证固收平台成交金额
from windget import getAmountFixedIncome


# 获取双边买入净价(加权平均)时间序列
from windget import getBinetBidWtSeries


# 获取双边买入净价(加权平均)
from windget import getBinetBidWt


# 获取双边买入收益率(加权平均)时间序列
from windget import getBibiDrTWtSeries


# 获取双边买入收益率(加权平均)
from windget import getBibiDrTWt


# 获取双边卖出净价(加权平均)时间序列
from windget import getBinetAskWtSeries


# 获取双边卖出净价(加权平均)
from windget import getBinetAskWt


# 获取双边卖出收益率(加权平均)时间序列
from windget import getBiasKrTWtSeries


# 获取双边卖出收益率(加权平均)
from windget import getBiasKrTWt


# 获取双边买入净价(最优)时间序列
from windget import getBinetBidBstSeries


# 获取双边买入净价(最优)
from windget import getBinetBidBst


# 获取双边买入收益率(最优)时间序列
from windget import getBibiDrTBstSeries


# 获取双边买入收益率(最优)
from windget import getBibiDrTBst


# 获取双边卖出净价(最优)时间序列
from windget import getBinetAskBstSeries


# 获取双边卖出净价(最优)
from windget import getBinetAskBst


# 获取双边卖出收益率(最优)时间序列
from windget import getBiasKrTBstSeries


# 获取双边卖出收益率(最优)
from windget import getBiasKrTBst


# 获取双边报价笔数时间序列
from windget import getBIqTvOlmSeries


# 获取双边报价笔数
from windget import getBIqTvOlm


# 获取报价买入净价(算术平均)时间序列
from windget import getNetBidAvgSeries


# 获取报价买入净价(算术平均)
from windget import getNetBidAvg


# 获取报价买入收益率(算术平均)时间序列
from windget import getBidRtAvgSeries


# 获取报价买入收益率(算术平均)
from windget import getBidRtAvg


# 获取报价卖出净价(算术平均)时间序列
from windget import getNeTaskAvgSeries


# 获取报价卖出净价(算术平均)
from windget import getNeTaskAvg


# 获取报价卖出收益率(算术平均)时间序列
from windget import getAskRtAvgSeries


# 获取报价卖出收益率(算术平均)
from windget import getAskRtAvg


# 获取报价买入净价(最优)时间序列
from windget import getNetBidBstSeries


# 获取报价买入净价(最优)
from windget import getNetBidBst


# 获取报价买入收益率(最优)时间序列
from windget import getBidRtBstSeries


# 获取报价买入收益率(最优)
from windget import getBidRtBst


# 获取报价卖出净价(最优)时间序列
from windget import getNeTaskBstSeries


# 获取报价卖出净价(最优)
from windget import getNeTaskBst


# 获取报价卖出收益率(最优)时间序列
from windget import getAskRtBstSeries


# 获取报价卖出收益率(最优)
from windget import getAskRtBst


# 获取报价总笔数时间序列
from windget import getQtVolMSeries


# 获取报价总笔数
from windget import getQtVolM


# 获取区间成交金额时间序列
from windget import getPqAmountSeries


# 获取区间成交金额
from windget import getPqAmount


# 获取单位净值时间序列
from windget import getNavSeries


# 获取单位净值
from windget import getNav


# 获取单位净值币种时间序列
from windget import getFundNavCurSeries


# 获取单位净值币种
from windget import getFundNavCur


# 获取单位净值(不前推)时间序列
from windget import getNav2Series


# 获取单位净值(不前推)
from windget import getNav2


# 获取单位净值(支持转型基金)时间序列
from windget import getNavUnitTransformSeries


# 获取单位净值(支持转型基金)
from windget import getNavUnitTransform


# 获取复权单位净值时间序列
from windget import getNavAdjSeries


# 获取复权单位净值
from windget import getNavAdj


# 获取复权单位净值(不前推)时间序列
from windget import getNavAdj2Series


# 获取复权单位净值(不前推)
from windget import getNavAdj2


# 获取累计单位净值时间序列
from windget import getNavAccSeries


# 获取累计单位净值
from windget import getNavAcc


# 获取累计单位净值(支持转型基金)时间序列
from windget import getNavAccumulatedTransformSeries


# 获取累计单位净值(支持转型基金)
from windget import getNavAccumulatedTransform


# 获取复权单位净值(支持转型基金)时间序列
from windget import getNavAdjustedTransformSeries


# 获取复权单位净值(支持转型基金)
from windget import getNavAdjustedTransform


# 获取复权单位净值增长时间序列
from windget import getNavAdjChgSeries


# 获取复权单位净值增长
from windget import getNavAdjChg


# 获取累计单位净值增长时间序列
from windget import getNavAccChgSeries


# 获取累计单位净值增长
from windget import getNavAccChg


# 获取复权单位净值增长率时间序列
from windget import getNavAdjReturnSeries


# 获取复权单位净值增长率
from windget import getNavAdjReturn


# 获取累计单位净值增长率时间序列
from windget import getNavAccReturnSeries


# 获取累计单位净值增长率
from windget import getNavAccReturn


# 获取复权单位净值相对大盘增长率时间序列
from windget import getRelNavAdjReturnSeries


# 获取复权单位净值相对大盘增长率
from windget import getRelNavAdjReturn


# 获取当期复权单位净值增长率时间序列
from windget import getNavAdjReturn1Series


# 获取当期复权单位净值增长率
from windget import getNavAdjReturn1


# 获取区间最高单位净值时间序列
from windget import getNavHighPerSeries


# 获取区间最高单位净值
from windget import getNavHighPer


# 获取区间最高单位净值日时间序列
from windget import getFundHighestNavDateSeries


# 获取区间最高单位净值日
from windget import getFundHighestNavDate


# 获取区间最低单位净值时间序列
from windget import getNavLowPerSeries


# 获取区间最低单位净值
from windget import getNavLowPer


# 获取区间最低单位净值日时间序列
from windget import getFundLowestNavDateSeries


# 获取区间最低单位净值日
from windget import getFundLowestNavDate


# 获取区间最高复权单位净值时间序列
from windget import getNavAdjHighPerSeries


# 获取区间最高复权单位净值
from windget import getNavAdjHighPer


# 获取区间最高复权单位净值日时间序列
from windget import getFundHighestAdjNavDateSeries


# 获取区间最高复权单位净值日
from windget import getFundHighestAdjNavDate


# 获取区间最低复权单位净值时间序列
from windget import getNavAdjLowPerSeries


# 获取区间最低复权单位净值
from windget import getNavAdjLowPer


# 获取区间最低复权单位净值日时间序列
from windget import getFundLowestAdjNavDateSeries


# 获取区间最低复权单位净值日
from windget import getFundLowestAdjNavDate


# 获取区间最高累计单位净值时间序列
from windget import getNavAccHighPerSeries


# 获取区间最高累计单位净值
from windget import getNavAccHighPer


# 获取区间最高累计单位净值日时间序列
from windget import getFundHighestAcCumNavDateSeries


# 获取区间最高累计单位净值日
from windget import getFundHighestAcCumNavDate


# 获取区间最低累计单位净值时间序列
from windget import getNavAccLowPerSeries


# 获取区间最低累计单位净值
from windget import getNavAccLowPer


# 获取区间最低累计单位净值日时间序列
from windget import getFundLowestAcCumNavDateSeries


# 获取区间最低累计单位净值日
from windget import getFundLowestAcCumNavDate


# 获取自成立日起复权单位净值增长率时间序列
from windget import getSiNavAdjReturnSeries


# 获取自成立日起复权单位净值增长率
from windget import getSiNavAdjReturn


# 获取投连险卖出价时间序列
from windget import getNavSellPriceSeries


# 获取投连险卖出价
from windget import getNavSellPrice


# 获取最近基金净值日期时间序列
from windget import getNavDateSeries


# 获取最近基金净值日期
from windget import getNavDate


# 获取最新净值除权日时间序列
from windget import getNavExRightDateSeries


# 获取最新净值除权日
from windget import getNavExRightDate


# 获取基金净值公布类型时间序列
from windget import getNavPublishTypeSeries


# 获取基金净值公布类型
from windget import getNavPublishType


# 获取现金分红净值增长率时间序列
from windget import getNavDivReturnSeries


# 获取现金分红净值增长率
from windget import getNavDivReturn


# 获取区间净值超越基准收益率时间序列
from windget import getNavOverBenchReturnPerSeries


# 获取区间净值超越基准收益率
from windget import getNavOverBenchReturnPer


# 获取区间净值超越基准收益频率时间序列
from windget import getNavOverBenchReturnFrEqSeries


# 获取区间净值超越基准收益频率
from windget import getNavOverBenchReturnFrEq


# 获取区间净值超越基准收益频率(百分比)时间序列
from windget import getNavOverBenchReturnFrEq2Series


# 获取区间净值超越基准收益频率(百分比)
from windget import getNavOverBenchReturnFrEq2


# 获取近1周回报时间序列
from windget import getReturn1WSeries


# 获取近1周回报
from windget import getReturn1W


# 获取近1周回报排名时间序列
from windget import getPeriodReturnRanking1WSeries


# 获取近1周回报排名
from windget import getPeriodReturnRanking1W


# 获取近1月回报时间序列
from windget import getReturn1MSeries


# 获取近1月回报
from windget import getReturn1M


# 获取近1月回报排名时间序列
from windget import getPeriodReturnRanking1MSeries


# 获取近1月回报排名
from windget import getPeriodReturnRanking1M


# 获取近3月回报时间序列
from windget import getReturn3MSeries


# 获取近3月回报
from windget import getReturn3M


# 获取近3月回报排名时间序列
from windget import getPeriodReturnRanking3MSeries


# 获取近3月回报排名
from windget import getPeriodReturnRanking3M


# 获取近6月回报时间序列
from windget import getReturn6MSeries


# 获取近6月回报
from windget import getReturn6M


# 获取近6月回报排名时间序列
from windget import getPeriodReturnRanking6MSeries


# 获取近6月回报排名
from windget import getPeriodReturnRanking6M


# 获取近1年回报时间序列
from windget import getReturn1YSeries


# 获取近1年回报
from windget import getReturn1Y


# 获取近1年回报排名时间序列
from windget import getPeriodReturnRanking1YSeries


# 获取近1年回报排名
from windget import getPeriodReturnRanking1Y


# 获取近2年回报时间序列
from windget import getReturn2YSeries


# 获取近2年回报
from windget import getReturn2Y


# 获取近2年回报排名时间序列
from windget import getPeriodReturnRanking2YSeries


# 获取近2年回报排名
from windget import getPeriodReturnRanking2Y


# 获取近3年回报时间序列
from windget import getReturn3YSeries


# 获取近3年回报
from windget import getReturn3Y


# 获取近3年回报排名时间序列
from windget import getPeriodReturnRanking3YSeries


# 获取近3年回报排名
from windget import getPeriodReturnRanking3Y


# 获取近5年回报时间序列
from windget import getReturn5YSeries


# 获取近5年回报
from windget import getReturn5Y


# 获取近5年回报排名时间序列
from windget import getPeriodReturnRanking5YSeries


# 获取近5年回报排名
from windget import getPeriodReturnRanking5Y


# 获取近10年回报时间序列
from windget import getReturn10YSeries


# 获取近10年回报
from windget import getReturn10Y


# 获取近10年回报排名时间序列
from windget import getPeriodReturnRanking10YSeries


# 获取近10年回报排名
from windget import getPeriodReturnRanking10Y


# 获取今年以来回报时间序列
from windget import getReturnYTdSeries


# 获取今年以来回报
from windget import getReturnYTd


# 获取今年以来回报排名时间序列
from windget import getPeriodReturnRankingYTdSeries


# 获取今年以来回报排名
from windget import getPeriodReturnRankingYTd


# 获取成立以来回报时间序列
from windget import getReturnStdSeries


# 获取成立以来回报
from windget import getReturnStd


# 获取单月度回报时间序列
from windget import getReturnMSeries


# 获取单月度回报
from windget import getReturnM


# 获取单季度回报时间序列
from windget import getReturnQSeries


# 获取单季度回报
from windget import getReturnQ


# 获取单年度回报时间序列
from windget import getReturnYSeries


# 获取单年度回报
from windget import getReturnY


# 获取单年度回报排名时间序列
from windget import getPeriodReturnRankingYSeries


# 获取单年度回报排名
from windget import getPeriodReturnRankingY


# 获取同类基金区间平均收益率时间序列
from windget import getPeerFundAvgReturnPerSeries


# 获取同类基金区间平均收益率
from windget import getPeerFundAvgReturnPer


# 获取同类基金区间收益排名(字符串)时间序列
from windget import getPeerFundReturnRankPerSeries


# 获取同类基金区间收益排名(字符串)
from windget import getPeerFundReturnRankPer


# 获取同类基金区间收益排名(百分比)时间序列
from windget import getPeerFundReturnRankPropPerSeries


# 获取同类基金区间收益排名(百分比)
from windget import getPeerFundReturnRankPropPer


# 获取同类基金区间收益排名(百分比)(券商集合理财)时间序列
from windget import getPeerSamReturnRankPropPerSeries


# 获取同类基金区间收益排名(百分比)(券商集合理财)
from windget import getPeerSamReturnRankPropPer


# 获取同类基金区间收益排名(百分比)(阳光私募)时间序列
from windget import getPeerHfReturnRankPropPerSeries


# 获取同类基金区间收益排名(百分比)(阳光私募)
from windget import getPeerHfReturnRankPropPer


# 获取同类基金区间收益排名(券商集合理财)时间序列
from windget import getPeerSamReturnRankPerSeries


# 获取同类基金区间收益排名(券商集合理财)
from windget import getPeerSamReturnRankPer


# 获取同类基金区间收益排名(阳光私募)时间序列
from windget import getPeerHfReturnRankPerSeries


# 获取同类基金区间收益排名(阳光私募)
from windget import getPeerHfReturnRankPer


# 获取同类基金区间收益排名(阳光私募,投资策略)时间序列
from windget import getPeerHf2ReturnRankPerSeries


# 获取同类基金区间收益排名(阳光私募,投资策略)
from windget import getPeerHf2ReturnRankPer


# 获取报告期净值增长率时间序列
from windget import getNavReturnSeries


# 获取报告期净值增长率
from windget import getNavReturn


# 获取报告期净值增长率标准差时间序列
from windget import getNavStdDevReturnSeries


# 获取报告期净值增长率标准差
from windget import getNavStdDevReturn


# 获取报告期净值增长率减基准增长率时间序列
from windget import getNavBenchDevReturnSeries


# 获取报告期净值增长率减基准增长率
from windget import getNavBenchDevReturn


# 获取报告期净值增长率减基准增长率标准差时间序列
from windget import getNavStdDevNavBenchSeries


# 获取报告期净值增长率减基准增长率标准差
from windget import getNavStdDevNavBench


# 获取份额结转方式时间序列
from windget import getMmFCarryOverSeries


# 获取份额结转方式
from windget import getMmFCarryOver


# 获取份额结转日期类型时间序列
from windget import getMmFCarryOverDateSeries


# 获取份额结转日期类型
from windget import getMmFCarryOverDate


# 获取7日年化收益率时间序列
from windget import getMmFAnnualIZedYieldSeries


# 获取7日年化收益率
from windget import getMmFAnnualIZedYield


# 获取区间7日年化收益率均值时间序列
from windget import getMmFAvgAnnualIZedYieldSeries


# 获取区间7日年化收益率均值
from windget import getMmFAvgAnnualIZedYield


# 获取区间7日年化收益率方差时间序列
from windget import getMmFVarAnnualIZedYieldSeries


# 获取区间7日年化收益率方差
from windget import getMmFVarAnnualIZedYield


# 获取万份基金单位收益时间序列
from windget import getMmFUnitYieldSeries


# 获取万份基金单位收益
from windget import getMmFUnitYield


# 获取区间万份基金单位收益均值时间序列
from windget import getMmFAvgUnitYieldSeries


# 获取区间万份基金单位收益均值
from windget import getMmFAvgUnitYield


# 获取区间万份基金单位收益总值时间序列
from windget import getMmFTotalUnitYieldSeries


# 获取区间万份基金单位收益总值
from windget import getMmFTotalUnitYield


# 获取区间万份基金单位收益方差时间序列
from windget import getMmFVarUnitYieldSeries


# 获取区间万份基金单位收益方差
from windget import getMmFVarUnitYield


# 获取股息率(报告期)时间序列
from windget import getDividendYieldSeries


# 获取股息率(报告期)
from windget import getDividendYield


# 获取股息率(近12个月)时间序列
from windget import getDividendYield2Series


# 获取股息率(近12个月)
from windget import getDividendYield2


# 获取发布方股息率(近12个月)时间序列
from windget import getValDividendYield2IssuerSeries


# 获取发布方股息率(近12个月)
from windget import getValDividendYield2Issuer


# 获取市盈率百分位时间序列
from windget import getValPep2Series


# 获取市盈率百分位
from windget import getValPep2


# 获取市盈率分位数时间序列
from windget import getValPePercentileSeries


# 获取市盈率分位数
from windget import getValPePercentile


# 获取市净率分位数时间序列
from windget import getValPbPercentileSeries


# 获取市净率分位数
from windget import getValPbPercentile


# 获取股息率分位数时间序列
from windget import getValDividendPercentileSeries


# 获取股息率分位数
from windget import getValDividendPercentile


# 获取市销率分位数时间序列
from windget import getValPsPercentileSeries


# 获取市销率分位数
from windget import getValPsPercentile


# 获取市现率分位数时间序列
from windget import getValPcfPercentileSeries


# 获取市现率分位数
from windget import getValPcfPercentile


# 获取股权激励目标净利润时间序列
from windget import getTargetNpSeries


# 获取股权激励目标净利润
from windget import getTargetNp


# 获取量比时间序列
from windget import getVolRatioSeries


# 获取量比
from windget import getVolRatio


# 获取持买单量比上交易日增减时间序列
from windget import getOiLoiCSeries


# 获取持买单量比上交易日增减
from windget import getOiLoiC


# 获取持卖单量比上交易日增减时间序列
from windget import getOiSOicSeries


# 获取持卖单量比上交易日增减
from windget import getOiSOic


# 获取网下有效报价申购量比例时间序列
from windget import getIpoVsSharesPctSeries


# 获取网下有效报价申购量比例
from windget import getIpoVsSharesPct


# 获取网下高于有效报价上限的申购量比例时间序列
from windget import getIpoInvsSharesPctASeries


# 获取网下高于有效报价上限的申购量比例
from windget import getIpoInvsSharesPctA


# 获取近期创历史新低时间序列
from windget import getHistoryLowSeries


# 获取近期创历史新低
from windget import getHistoryLow


# 获取近期创历史新低次数时间序列
from windget import getHistoryLowDaysSeries


# 获取近期创历史新低次数
from windget import getHistoryLowDays


# 获取近期创阶段新高时间序列
from windget import getStageHighSeries


# 获取近期创阶段新高
from windget import getStageHigh


# 获取近期创历史新高时间序列
from windget import getHistoryHighSeries


# 获取近期创历史新高
from windget import getHistoryHigh


# 获取近期创历史新高次数时间序列
from windget import getHistoryHighDaysSeries


# 获取近期创历史新高次数
from windget import getHistoryHighDays


# 获取近期创阶段新低时间序列
from windget import getStageLowSeries


# 获取近期创阶段新低
from windget import getStageLow


# 获取连涨天数时间序列
from windget import getUpDaysSeries


# 获取连涨天数
from windget import getUpDays


# 获取连跌天数时间序列
from windget import getDownDaysSeries


# 获取连跌天数
from windget import getDownDays


# 获取向上有效突破均线时间序列
from windget import getBreakoutMaSeries


# 获取向上有效突破均线
from windget import getBreakoutMa


# 获取向下有效突破均线时间序列
from windget import getBreakdownMaSeries


# 获取向下有效突破均线
from windget import getBreakdownMa


# 获取成份创阶段新高数量时间序列
from windget import getTechAnalStageHighNumSeries


# 获取成份创阶段新高数量
from windget import getTechAnalStageHighNum


# 获取成份创阶段新低数量时间序列
from windget import getTechAnalStageLowNumSeries


# 获取成份创阶段新低数量
from windget import getTechAnalStageLowNum


# 获取均线多空头排列看涨看跌时间序列
from windget import getBullBearMaSeries


# 获取均线多空头排列看涨看跌
from windget import getBullBearMa


# 获取指数成份上涨数量时间序列
from windget import getTechUpNumSeries


# 获取指数成份上涨数量
from windget import getTechUpNum


# 获取指数成份下跌数量时间序列
from windget import getTechDownNumSeries


# 获取指数成份下跌数量
from windget import getTechDownNum


# 获取指数成份涨停数量时间序列
from windget import getTechLimitUpNumSeries


# 获取指数成份涨停数量
from windget import getTechLimitUpNum


# 获取指数成份跌停数量时间序列
from windget import getTechLimitDownNumSeries


# 获取指数成份跌停数量
from windget import getTechLimitDownNum


# 获取成份分红对指数影响时间序列
from windget import getDivCompIndexSeries


# 获取成份分红对指数影响
from windget import getDivCompIndex


# 获取平均收益率(年化,最近100周)时间序列
from windget import getAnnualYeIlD100WSeries


# 获取平均收益率(年化,最近100周)
from windget import getAnnualYeIlD100W


# 获取平均收益率(年化,最近24个月)时间序列
from windget import getAnnualYeIlD24MSeries


# 获取平均收益率(年化,最近24个月)
from windget import getAnnualYeIlD24M


# 获取平均收益率(年化,最近60个月)时间序列
from windget import getAnnualYeIlD60MSeries


# 获取平均收益率(年化,最近60个月)
from windget import getAnnualYeIlD60M


# 获取年化波动率(最近100周)时间序列
from windget import getAnnualStDeVr100WSeries


# 获取年化波动率(最近100周)
from windget import getAnnualStDeVr100W


# 获取年化波动率(最近24个月)时间序列
from windget import getAnnualStDeVr24MSeries


# 获取年化波动率(最近24个月)
from windget import getAnnualStDeVr24M


# 获取年化波动率(最近60个月)时间序列
from windget import getAnnualStDeVr60MSeries


# 获取年化波动率(最近60个月)
from windget import getAnnualStDeVr60M


# 获取平均收益率时间序列
from windget import getAvgReturnSeries


# 获取平均收益率
from windget import getAvgReturn


# 获取平均收益率(年化)时间序列
from windget import getAvgReturnYSeries


# 获取平均收益率(年化)
from windget import getAvgReturnY


# 获取平均收益率_FUND时间序列
from windget import getRiskAvgReturnSeries


# 获取平均收益率_FUND
from windget import getRiskAvgReturn


# 获取几何平均收益率时间序列
from windget import getRiskGemReturnSeries


# 获取几何平均收益率
from windget import getRiskGemReturn


# 获取贷款平均收益率_总计时间序列
from windget import getStmNoteBank720Series


# 获取贷款平均收益率_总计
from windget import getStmNoteBank720


# 获取贷款平均收益率_企业贷款及垫款时间序列
from windget import getStmNoteBank731Series


# 获取贷款平均收益率_企业贷款及垫款
from windget import getStmNoteBank731


# 获取贷款平均收益率_个人贷款及垫款时间序列
from windget import getStmNoteBank732Series


# 获取贷款平均收益率_个人贷款及垫款
from windget import getStmNoteBank732


# 获取贷款平均收益率_票据贴现时间序列
from windget import getStmNoteBank733Series


# 获取贷款平均收益率_票据贴现
from windget import getStmNoteBank733


# 获取贷款平均收益率_个人住房贷款时间序列
from windget import getStmNoteBank734Series


# 获取贷款平均收益率_个人住房贷款
from windget import getStmNoteBank734


# 获取贷款平均收益率_个人消费贷款时间序列
from windget import getStmNoteBank735Series


# 获取贷款平均收益率_个人消费贷款
from windget import getStmNoteBank735


# 获取贷款平均收益率_信用卡应收账款时间序列
from windget import getStmNoteBank736Series


# 获取贷款平均收益率_信用卡应收账款
from windget import getStmNoteBank736


# 获取贷款平均收益率_经营性贷款时间序列
from windget import getStmNoteBank737Series


# 获取贷款平均收益率_经营性贷款
from windget import getStmNoteBank737


# 获取贷款平均收益率_汽车贷款时间序列
from windget import getStmNoteBank738Series


# 获取贷款平均收益率_汽车贷款
from windget import getStmNoteBank738


# 获取贷款平均收益率_其他个人贷款时间序列
from windget import getStmNoteBank739Series


# 获取贷款平均收益率_其他个人贷款
from windget import getStmNoteBank739


# 获取贷款平均收益率_信用贷款时间序列
from windget import getStmNoteBank791Series


# 获取贷款平均收益率_信用贷款
from windget import getStmNoteBank791


# 获取贷款平均收益率_保证贷款时间序列
from windget import getStmNoteBank792Series


# 获取贷款平均收益率_保证贷款
from windget import getStmNoteBank792


# 获取贷款平均收益率_抵押贷款时间序列
from windget import getStmNoteBank793Series


# 获取贷款平均收益率_抵押贷款
from windget import getStmNoteBank793


# 获取贷款平均收益率_质押贷款时间序列
from windget import getStmNoteBank794Series


# 获取贷款平均收益率_质押贷款
from windget import getStmNoteBank794


# 获取贷款平均收益率_短期贷款时间序列
from windget import getStmNoteBank47Series


# 获取贷款平均收益率_短期贷款
from windget import getStmNoteBank47


# 获取贷款平均收益率_中长期贷款时间序列
from windget import getStmNoteBank49Series


# 获取贷款平均收益率_中长期贷款
from windget import getStmNoteBank49


# 获取区间收益率(年化)时间序列
from windget import getRiskAnnualIntervalYieldSeries


# 获取区间收益率(年化)
from windget import getRiskAnnualIntervalYield


# 获取最大回撤时间序列
from windget import getRiskMaxDownsideSeries


# 获取最大回撤
from windget import getRiskMaxDownside


# 获取最大回撤恢复天数时间序列
from windget import getRiskMaxDownsideRecoverDaysSeries


# 获取最大回撤恢复天数
from windget import getRiskMaxDownsideRecoverDays


# 获取最大回撤同类平均时间序列
from windget import getRiskSimLAvgMaxDownsideSeries


# 获取最大回撤同类平均
from windget import getRiskSimLAvgMaxDownside


# 获取最大回撤区间日期时间序列
from windget import getRiskMaxDownsideDateSeries


# 获取最大回撤区间日期
from windget import getRiskMaxDownsideDate


# 获取任期最大回撤时间序列
from windget import getFundManagerMaxDrawDownSeries


# 获取任期最大回撤
from windget import getFundManagerMaxDrawDown


# 获取波动率时间序列
from windget import getStDeVrSeries


# 获取波动率
from windget import getStDeVr


# 获取波动率(年化)时间序列
from windget import getStDeVrySeries


# 获取波动率(年化)
from windget import getStDeVry


# 获取年化波动率时间序列
from windget import getRiskStDevYearlySeries


# 获取年化波动率
from windget import getRiskStDevYearly


# 获取年化波动率同类平均时间序列
from windget import getRiskSimLAvgStDevYearlySeries


# 获取年化波动率同类平均
from windget import getRiskSimLAvgStDevYearly


# 获取交易量波动率_PIT时间序列
from windget import getTechVolumeVolatilitySeries


# 获取交易量波动率_PIT
from windget import getTechVolumeVolatility


# 获取转债隐含波动率时间序列
from windget import getImpliedVolSeries


# 获取转债隐含波动率
from windget import getImpliedVol


# 获取个股与市场波动率比值_PIT时间序列
from windget import getRiskVolatilityRatioSeries


# 获取个股与市场波动率比值_PIT
from windget import getRiskVolatilityRatio


# 获取252日残差收益波动率_PIT时间序列
from windget import getRiskReSidVol252Series


# 获取252日残差收益波动率_PIT
from windget import getRiskReSidVol252


# 获取标准差系数时间序列
from windget import getStDcOfSeries


# 获取标准差系数
from windget import getStDcOf


# 获取非系统风险时间序列
from windget import getRiskNonSYsRisk1Series


# 获取非系统风险
from windget import getRiskNonSYsRisk1


# 获取非系统风险_FUND时间序列
from windget import getRiskNonSYsRiskSeries


# 获取非系统风险_FUND
from windget import getRiskNonSYsRisk


# 获取剩余期限(天)时间序列
from windget import getDaySeries


# 获取剩余期限(天)
from windget import getDay


# 获取剩余期限(年)时间序列
from windget import getPtMYearSeries


# 获取剩余期限(年)
from windget import getPtMYear


# 获取行权剩余期限(年)时间序列
from windget import getTermIfExerciseSeries


# 获取行权剩余期限(年)
from windget import getTermIfExercise


# 获取特殊剩余期限说明时间序列
from windget import getTermNoteSeries


# 获取特殊剩余期限说明
from windget import getTermNote


# 获取特殊剩余期限时间序列
from windget import getTermNote1Series


# 获取特殊剩余期限
from windget import getTermNote1


# 获取加权剩余期限(按本息)时间序列
from windget import getWeightedRtSeries


# 获取加权剩余期限(按本息)
from windget import getWeightedRt


# 获取加权剩余期限(按本金)时间序列
from windget import getWeightedRt2Series


# 获取加权剩余期限(按本金)
from windget import getWeightedRt2


# 获取应计利息时间序列
from windget import getAccruedInterestSeries


# 获取应计利息
from windget import getAccruedInterest


# 获取指定日应计利息时间序列
from windget import getCalcAccRIntSeries


# 获取指定日应计利息
from windget import getCalcAccRInt


# 获取已计息天数时间序列
from windget import getAccruedDaysSeries


# 获取已计息天数
from windget import getAccruedDays


# 获取上一付息日时间序列
from windget import getAnalPreCupNSeries


# 获取上一付息日
from windget import getAnalPreCupN


# 获取下一付息日时间序列
from windget import getNxcUpnSeries


# 获取下一付息日
from windget import getNxcUpn


# 获取下一付息日久期时间序列
from windget import getNxcUpnDurationSeries


# 获取下一付息日久期
from windget import getNxcUpnDuration


# 获取距下一付息日天数时间序列
from windget import getNxcUpn2Series


# 获取距下一付息日天数
from windget import getNxcUpn2


# 获取长期停牌起始日时间序列
from windget import getPqSuspendStartDateSeries


# 获取长期停牌起始日
from windget import getPqSuspendStartDate


# 获取长期停牌截止日时间序列
from windget import getPqSuspendEnddateSeries


# 获取长期停牌截止日
from windget import getPqSuspendEnddate


# 获取收盘到期收益率时间序列
from windget import getYTMBSeries


# 获取收盘到期收益率
from windget import getYTMB


# 获取赎回收益率时间序列
from windget import getYTcSeries


# 获取赎回收益率
from windget import getYTc


# 获取回售收益率时间序列
from windget import getYTPSeries


# 获取回售收益率
from windget import getYTP


# 获取基准久期时间序列
from windget import getBDurationSeries


# 获取基准久期
from windget import getBDuration


# 获取行权基准久期时间序列
from windget import getBDurationIfExeSeries


# 获取行权基准久期
from windget import getBDurationIfExe


# 获取利差久期时间序列
from windget import getSDurationSeries


# 获取利差久期
from windget import getSDuration


# 获取行权利差久期时间序列
from windget import getSDurationIfExeSeries


# 获取行权利差久期
from windget import getSDurationIfExe


# 获取指定日现金流时间序列
from windget import getDailyCfSeries


# 获取指定日现金流
from windget import getDailyCf


# 获取指定日利息现金流时间序列
from windget import getDailyCfIntSeries


# 获取指定日利息现金流
from windget import getDailyCfInt


# 获取指定日本金现金流时间序列
from windget import getDailyCfPrInSeries


# 获取指定日本金现金流
from windget import getDailyCfPrIn


# 获取票面调整收益率时间序列
from windget import getRCyTmSeries


# 获取票面调整收益率
from windget import getRCyTm


# 获取价格算票面调整收益率时间序列
from windget import getCalcAdjYieldSeries


# 获取价格算票面调整收益率
from windget import getCalcAdjYield


# 获取下一行权日时间序列
from windget import getNxOptionDateSeries


# 获取下一行权日
from windget import getNxOptionDate


# 获取行权收益率时间序列
from windget import getYTMIfExeSeries


# 获取行权收益率
from windget import getYTMIfExe


# 获取行权久期时间序列
from windget import getDurationIfExerciseSeries


# 获取行权久期
from windget import getDurationIfExercise


# 获取行权修正久期时间序列
from windget import getModiDurationIfExeSeries


# 获取行权修正久期
from windget import getModiDurationIfExe


# 获取行权凸性时间序列
from windget import getConvexityIfExeSeries


# 获取行权凸性
from windget import getConvexityIfExe


# 获取行权基准凸性时间序列
from windget import getBConvexityIfExeSeries


# 获取行权基准凸性
from windget import getBConvexityIfExe


# 获取行权利差凸性时间序列
from windget import getSConvexityIfExeSeries


# 获取行权利差凸性
from windget import getSConvexityIfExe


# 获取1月久期时间序列
from windget import getDuration1MSeries


# 获取1月久期
from windget import getDuration1M


# 获取3月久期时间序列
from windget import getDuration3MSeries


# 获取3月久期
from windget import getDuration3M


# 获取6月久期时间序列
from windget import getDuration6MSeries


# 获取6月久期
from windget import getDuration6M


# 获取1年久期时间序列
from windget import getDuration1YSeries


# 获取1年久期
from windget import getDuration1Y


# 获取2年久期时间序列
from windget import getDuration2YSeries


# 获取2年久期
from windget import getDuration2Y


# 获取3年久期时间序列
from windget import getDuration3YSeries


# 获取3年久期
from windget import getDuration3Y


# 获取4年久期时间序列
from windget import getDuration4YSeries


# 获取4年久期
from windget import getDuration4Y


# 获取5年久期时间序列
from windget import getDuration5YSeries


# 获取5年久期
from windget import getDuration5Y


# 获取15年久期时间序列
from windget import getDuration15YSeries


# 获取15年久期
from windget import getDuration15Y


# 获取7年久期时间序列
from windget import getDuration7YSeries


# 获取7年久期
from windget import getDuration7Y


# 获取9年久期时间序列
from windget import getDuration9YSeries


# 获取9年久期
from windget import getDuration9Y


# 获取10年久期时间序列
from windget import getDuration10YSeries


# 获取10年久期
from windget import getDuration10Y


# 获取20年久期时间序列
from windget import getDuration20YSeries


# 获取20年久期
from windget import getDuration20Y


# 获取30年久期时间序列
from windget import getDuration30YSeries


# 获取30年久期
from windget import getDuration30Y


# 获取短边久期时间序列
from windget import getDurationShortSeries


# 获取短边久期
from windget import getDurationShort


# 获取长边久期时间序列
from windget import getDurationLongSeries


# 获取长边久期
from windget import getDurationLong


# 获取当期收益率时间序列
from windget import getCurYieldSeries


# 获取当期收益率
from windget import getCurYield


# 获取纯债到期收益率时间序列
from windget import getYTMCbSeries


# 获取纯债到期收益率
from windget import getYTMCb


# 获取纯债价值时间序列
from windget import getStrBValueSeries


# 获取纯债价值
from windget import getStrBValue


# 获取纯债溢价时间序列
from windget import getStrBPremiumSeries


# 获取纯债溢价
from windget import getStrBPremium


# 获取纯债溢价率时间序列
from windget import getStrBPremiumRatioSeries


# 获取纯债溢价率
from windget import getStrBPremiumRatio


# 获取转股价时间序列
from windget import getConVPriceSeries


# 获取转股价
from windget import getConVPrice


# 获取转股比例时间序列
from windget import getConVRatioSeries


# 获取转股比例
from windget import getConVRatio


# 获取转换价值时间序列
from windget import getConVValueSeries


# 获取转换价值
from windget import getConVValue


# 获取转股溢价时间序列
from windget import getConVPremiumSeries


# 获取转股溢价
from windget import getConVPremium


# 获取转股溢价率时间序列
from windget import getConVPremiumRatioSeries


# 获取转股溢价率
from windget import getConVPremiumRatio


# 获取转股市盈率时间序列
from windget import getConVpESeries


# 获取转股市盈率
from windget import getConVpE


# 获取转股市净率时间序列
from windget import getConVpBSeries


# 获取转股市净率
from windget import getConVpB


# 获取正股市盈率时间序列
from windget import getUnderlyingPeSeries


# 获取正股市盈率
from windget import getUnderlyingPe


# 获取正股市净率时间序列
from windget import getUnderlyingPbSeries


# 获取正股市净率
from windget import getUnderlyingPb


# 获取转股稀释率时间序列
from windget import getDiluteRateSeries


# 获取转股稀释率
from windget import getDiluteRate


# 获取对流通股稀释率时间序列
from windget import getLDiluteRateSeries


# 获取对流通股稀释率
from windget import getLDiluteRate


# 获取双低时间序列
from windget import getDoubleLowSeries


# 获取双低
from windget import getDoubleLow


# 获取转换因子时间序列
from windget import getTBfCVf2Series


# 获取转换因子
from windget import getTBfCVf2


# 获取转换因子(指定合约)时间序列
from windget import getTBfCVfSeries


# 获取转换因子(指定合约)
from windget import getTBfCVf


# 获取转换因子(主力合约)时间序列
from windget import getTBfCVf3Series


# 获取转换因子(主力合约)
from windget import getTBfCVf3


# 获取交割利息时间序列
from windget import getTBfInterestSeries


# 获取交割利息
from windget import getTBfInterest


# 获取区间利息时间序列
from windget import getTBfPaymentSeries


# 获取区间利息
from windget import getTBfPayment


# 获取交割成本时间序列
from windget import getTBfDeliverPriceSeries


# 获取交割成本
from windget import getTBfDeliverPrice


# 获取发票价格时间序列
from windget import getTBfInvoicePriceSeries


# 获取发票价格
from windget import getTBfInvoicePrice


# 获取期现价差时间序列
from windget import getTBfSpreadSeries


# 获取期现价差
from windget import getTBfSpread


# 获取基差时间序列
from windget import getTBfBasisSeries


# 获取基差
from windget import getTBfBasis


# 获取基差(股指期货)时间序列
from windget import getIfBasisSeries


# 获取基差(股指期货)
from windget import getIfBasis


# 获取基差年化收益率(股指期货)时间序列
from windget import getAnalBasisAnnualYieldSeries


# 获取基差年化收益率(股指期货)
from windget import getAnalBasisAnnualYield


# 获取基差率(股指期货)时间序列
from windget import getAnalBasisPercentSeries


# 获取基差率(股指期货)
from windget import getAnalBasisPercent


# 获取基差(商品期货)时间序列
from windget import getAnalBasisSeries


# 获取基差(商品期货)
from windget import getAnalBasis


# 获取基差率(商品期货)时间序列
from windget import getAnalBasisPercent2Series


# 获取基差率(商品期货)
from windget import getAnalBasisPercent2


# 获取净基差时间序列
from windget import getTBfNetBasisSeries


# 获取净基差
from windget import getTBfNetBasis


# 获取远期收益率时间序列
from windget import getTBfFyTmSeries


# 获取远期收益率
from windget import getTBfFyTm


# 获取全价算净价时间序列
from windget import getCalcCleanSeries


# 获取全价算净价
from windget import getCalcClean


# 获取净价算全价时间序列
from windget import getCalcDirtySeries


# 获取净价算全价
from windget import getCalcDirty


# 获取麦考利久期时间序列
from windget import getCalcDurationSeries


# 获取麦考利久期
from windget import getCalcDuration


# 获取修正久期时间序列
from windget import getCalcMDurationSeries


# 获取修正久期
from windget import getCalcMDuration


# 获取凸性时间序列
from windget import getCalcConVSeries


# 获取凸性
from windget import getCalcConV


# 获取对应到期收益率曲线代码时间序列
from windget import getYCCodeSeries


# 获取对应到期收益率曲线代码
from windget import getYCCode


# 获取收益率曲线(中债样本券)时间序列
from windget import getCalcChinaBondSeries


# 获取收益率曲线(中债样本券)
from windget import getCalcChinaBond


# 获取上海证券3年评级(夏普比率)时间序列
from windget import getRatingShanghaiSharpe3YSeries


# 获取上海证券3年评级(夏普比率)
from windget import getRatingShanghaiSharpe3Y


# 获取上海证券3年评级(择时能力)时间序列
from windget import getRatingShanghaiTiming3YSeries


# 获取上海证券3年评级(择时能力)
from windget import getRatingShanghaiTiming3Y


# 获取上海证券3年评级(选证能力)时间序列
from windget import getRatingShanghaiStocking3YSeries


# 获取上海证券3年评级(选证能力)
from windget import getRatingShanghaiStocking3Y


# 获取上海证券5年评级(夏普比率)时间序列
from windget import getRatingShanghaiSharpe5YSeries


# 获取上海证券5年评级(夏普比率)
from windget import getRatingShanghaiSharpe5Y


# 获取上海证券5年评级(择时能力)时间序列
from windget import getRatingShanghaiTiming5YSeries


# 获取上海证券5年评级(择时能力)
from windget import getRatingShanghaiTiming5Y


# 获取上海证券5年评级(选证能力)时间序列
from windget import getRatingShanghaiStocking5YSeries


# 获取上海证券5年评级(选证能力)
from windget import getRatingShanghaiStocking5Y


# 获取基金3年评级时间序列
from windget import getRating3YSeries


# 获取基金3年评级
from windget import getRating3Y


# 获取基金5年评级时间序列
from windget import getRating5YSeries


# 获取基金5年评级
from windget import getRating5Y


# 获取年化收益率时间序列
from windget import getRiskReturnYearlySeries


# 获取年化收益率
from windget import getRiskReturnYearly


# 获取年化收益率(工作日)时间序列
from windget import getRiskReturnYearlyTradeDateSeries


# 获取年化收益率(工作日)
from windget import getRiskReturnYearlyTradeDate


# 获取几何平均年化收益率时间序列
from windget import getFundManagerGeometricAnnualIZedYieldSeries


# 获取几何平均年化收益率
from windget import getFundManagerGeometricAnnualIZedYield


# 获取算术平均年化收益率时间序列
from windget import getFundManagerArithmeticAnnualIZedYieldSeries


# 获取算术平均年化收益率
from windget import getFundManagerArithmeticAnnualIZedYield


# 获取超越基准几何平均年化收益率时间序列
from windget import getFundManagerGeometricAvgAnnualYieldOverBenchSeries


# 获取超越基准几何平均年化收益率
from windget import getFundManagerGeometricAvgAnnualYieldOverBench


# 获取超越基准算术平均年化收益率时间序列
from windget import getFundManagerArithmeticAvgAnnualYieldOverBenchSeries


# 获取超越基准算术平均年化收益率
from windget import getFundManagerArithmeticAvgAnnualYieldOverBench


# 获取区间净值超越基准年化收益率时间序列
from windget import getRiskNavOverBenchAnnualReturnSeries


# 获取区间净值超越基准年化收益率
from windget import getRiskNavOverBenchAnnualReturn


# 获取区间收益率(工作日年化)时间序列
from windget import getRiskAnnualIntervalYieldTradeDateSeries


# 获取区间收益率(工作日年化)
from windget import getRiskAnnualIntervalYieldTradeDate


# 获取平均风险收益率时间序列
from windget import getRiskAvgRiskReturnSeries


# 获取平均风险收益率
from windget import getRiskAvgRiskReturn


# 获取几何平均风险收益率时间序列
from windget import getRiskGemAvgRiskReturnSeries


# 获取几何平均风险收益率
from windget import getRiskGemAvgRiskReturn


# 获取日跟踪偏离度(跟踪指数)时间序列
from windget import getRiskTrackDeviationTrackIndexSeries


# 获取日跟踪偏离度(跟踪指数)
from windget import getRiskTrackDeviationTrackIndex


# 获取区间跟踪偏离度均值(业绩基准)时间序列
from windget import getRiskAvgTrackDeviationBenchmarkSeries


# 获取区间跟踪偏离度均值(业绩基准)
from windget import getRiskAvgTrackDeviationBenchmark


# 获取区间跟踪偏离度均值(跟踪指数)时间序列
from windget import getRiskAvgTrackDeviationTrackIndexSeries


# 获取区间跟踪偏离度均值(跟踪指数)
from windget import getRiskAvgTrackDeviationTrackIndex


# 获取回撤(相对前期高点)时间序列
from windget import getRiskDownsideSeries


# 获取回撤(相对前期高点)
from windget import getRiskDownside


# 获取最大上涨时间序列
from windget import getRiskMaxUpsideSeries


# 获取最大上涨
from windget import getRiskMaxUpside


# 获取相关系数时间序列
from windget import getRiskCorreCoefficientSeries


# 获取相关系数
from windget import getRiskCorreCoefficient


# 获取相关系数(跟踪指数)时间序列
from windget import getRiskCorreCoefficientTrackIndexSeries


# 获取相关系数(跟踪指数)
from windget import getRiskCorreCoefficientTrackIndex


# 获取下跌相关系数_PIT时间序列
from windget import getTechDdNcrSeries


# 获取下跌相关系数_PIT
from windget import getTechDdNcr


# 获取个股与市场相关系数_PIT时间序列
from windget import getRiskHisRelationSeries


# 获取个股与市场相关系数_PIT
from windget import getRiskHisRelation


# 获取可决系数时间序列
from windget import getRiskR2Series


# 获取可决系数
from windget import getRiskR2


# 获取收益标准差时间序列
from windget import getRiskStDevSeries


# 获取收益标准差
from windget import getRiskStDev


# 获取收益标准差(年化)时间序列
from windget import getRiskAnnUstDevSeries


# 获取收益标准差(年化)
from windget import getRiskAnnUstDev


# 获取252日超额收益标准差_PIT时间序列
from windget import getRiskExStDev252Series


# 获取252日超额收益标准差_PIT
from windget import getRiskExStDev252


# 获取下行标准差时间序列
from windget import getRiskDownsideStDevSeries


# 获取下行标准差
from windget import getRiskDownsideStDev


# 获取上行标准差时间序列
from windget import getRiskUpsideStDevSeries


# 获取上行标准差
from windget import getRiskUpsideStDev


# 获取下行风险时间序列
from windget import getRiskDownsideRiskSeries


# 获取下行风险
from windget import getRiskDownsideRisk


# 获取下行风险同类平均时间序列
from windget import getRiskSimLAvgDownsideRiskSeries


# 获取下行风险同类平均
from windget import getRiskSimLAvgDownsideRisk


# 获取区间胜率时间序列
from windget import getWinRatioSeries


# 获取区间胜率
from windget import getWinRatio


# 获取基金组合久期时间序列
from windget import getRiskDurationSeries


# 获取基金组合久期
from windget import getRiskDuration


# 获取市场利率敏感性时间序列
from windget import getRiskInterestSensitivitySeries


# 获取市场利率敏感性
from windget import getRiskInterestSensitivity


# 获取选时能力时间序列
from windget import getRiskTimeSeries


# 获取选时能力
from windget import getRiskTime


# 获取选股能力时间序列
from windget import getRiskStockSeries


# 获取选股能力
from windget import getRiskStock


# 获取跟踪误差时间序列
from windget import getRiskTrackErrorSeries


# 获取跟踪误差
from windget import getRiskTrackError


# 获取跟踪误差(跟踪指数)时间序列
from windget import getRiskTrackErrorTrackIndexSeries


# 获取跟踪误差(跟踪指数)
from windget import getRiskTrackErrorTrackIndex


# 获取跟踪误差(年化)时间序列
from windget import getRiskAnNuTrackErrorSeries


# 获取跟踪误差(年化)
from windget import getRiskAnNuTrackError


# 获取信息比率时间序列
from windget import getRiskInfoRatioSeries


# 获取信息比率
from windget import getRiskInfoRatio


# 获取信息比率(年化)时间序列
from windget import getRiskAnNuInfoRatioSeries


# 获取信息比率(年化)
from windget import getRiskAnNuInfoRatio


# 获取风格系数时间序列
from windget import getStyleStyleCoefficientSeries


# 获取风格系数
from windget import getStyleStyleCoefficient


# 获取风格属性时间序列
from windget import getStyleStyleAttributeSeries


# 获取风格属性
from windget import getStyleStyleAttribute


# 获取市值-风格属性时间序列
from windget import getStyleMarketValueStyleAttributeSeries


# 获取市值-风格属性
from windget import getStyleMarketValueStyleAttribute


# 获取市值属性时间序列
from windget import getStyleMarketValueAttributeSeries


# 获取市值属性
from windget import getStyleMarketValueAttribute


# 获取平均持仓时间时间序列
from windget import getStyleAveragePositionTimeSeries


# 获取平均持仓时间
from windget import getStyleAveragePositionTime


# 获取平均持仓时间(半年)时间序列
from windget import getStyleHyAveragePositionTimeSeries


# 获取平均持仓时间(半年)
from windget import getStyleHyAveragePositionTime


# 获取投资集中度时间序列
from windget import getStyleInvConcentrationSeries


# 获取投资集中度
from windget import getStyleInvConcentration


# 获取佣金规模比时间序列
from windget import getStyleComMisAccountSeries


# 获取佣金规模比
from windget import getStyleComMisAccount


# 获取最高单月回报时间序列
from windget import getAbsoluteHighestMonthlyReturnSeries


# 获取最高单月回报
from windget import getAbsoluteHighestMonthlyReturn


# 获取最低单月回报时间序列
from windget import getAbsoluteLowestMonthlyReturnSeries


# 获取最低单月回报
from windget import getAbsoluteLowestMonthlyReturn


# 获取最低单月回报同类平均时间序列
from windget import getAbsoluteSimLAvgLowestMonthlyReturnSeries


# 获取最低单月回报同类平均
from windget import getAbsoluteSimLAvgLowestMonthlyReturn


# 获取连涨月数时间序列
from windget import getAbsoluteConUpsMonthSeries


# 获取连涨月数
from windget import getAbsoluteConUpsMonth


# 获取连跌月数时间序列
from windget import getAbsoluteCondOwnsMonthSeries


# 获取连跌月数
from windget import getAbsoluteCondOwnsMonth


# 获取最长连续上涨月数时间序列
from windget import getAbsoluteLongestConUpMonthSeries


# 获取最长连续上涨月数
from windget import getAbsoluteLongestConUpMonth


# 获取最长连续上涨整月涨幅时间序列
from windget import getAbsoluteMaxIncreaseOfUpMonthSeries


# 获取最长连续上涨整月涨幅
from windget import getAbsoluteMaxIncreaseOfUpMonth


# 获取最长连续下跌月数时间序列
from windget import getAbsoluteLongestConDownMonthSeries


# 获取最长连续下跌月数
from windget import getAbsoluteLongestConDownMonth


# 获取最长连续下跌整月跌幅时间序列
from windget import getAbsoluteMaxFallOfDownMonthSeries


# 获取最长连续下跌整月跌幅
from windget import getAbsoluteMaxFallOfDownMonth


# 获取上涨/下跌月数比时间序列
from windget import getAbsoluteUpDownMonthRatioSeries


# 获取上涨/下跌月数比
from windget import getAbsoluteUpDownMonthRatio


# 获取盈利百分比时间序列
from windget import getAbsoluteProfitMonthPerSeries


# 获取盈利百分比
from windget import getAbsoluteProfitMonthPer


# 获取区间盈利百分比时间序列
from windget import getAbsoluteProfitPerSeries


# 获取区间盈利百分比
from windget import getAbsoluteProfitPer


# 获取平均收益时间序列
from windget import getAbsoluteAvgIncomeSeries


# 获取平均收益
from windget import getAbsoluteAvgIncome


# 获取5年平均收益市值比_PIT时间序列
from windget import getFaPtToMvAvg5YSeries


# 获取5年平均收益市值比_PIT
from windget import getFaPtToMvAvg5Y


# 获取平均损失时间序列
from windget import getAbsoluteAvgLossSeries


# 获取平均损失
from windget import getAbsoluteAvgLoss


# 获取参数平均损失值ES时间序列
from windget import getRiskEspaRamSeries


# 获取参数平均损失值ES
from windget import getRiskEspaRam


# 获取历史平均损失值ES时间序列
from windget import getRiskEsHistoricalSeries


# 获取历史平均损失值ES
from windget import getRiskEsHistorical


# 获取月度复合回报时间序列
from windget import getAbsoluteMonthlyCompositeReturnSeries


# 获取月度复合回报
from windget import getAbsoluteMonthlyCompositeReturn


# 获取平均月度回报时间序列
from windget import getAbsoluteAvgMonthlyReturnSeries


# 获取平均月度回报
from windget import getAbsoluteAvgMonthlyReturn


# 获取最高季度回报时间序列
from windget import getAbsoluteHighestQuatreTurnSeries


# 获取最高季度回报
from windget import getAbsoluteHighestQuatreTurn


# 获取最低季度回报时间序列
from windget import getAbsoluteLowestQuatreTurnSeries


# 获取最低季度回报
from windget import getAbsoluteLowestQuatreTurn


# 获取剩余折算天数时间序列
from windget import getFundDaysToConversionSeries


# 获取剩余折算天数
from windget import getFundDaysToConversion


# 获取分级基金收益分配方式时间序列
from windget import getAnalSMfEarningSeries


# 获取分级基金收益分配方式
from windget import getAnalSMfEarning


# 获取隐含收益率时间序列
from windget import getAnalImpliedYieldSeries


# 获取隐含收益率
from windget import getAnalImpliedYield


# 获取整体折溢价率时间序列
from windget import getAnalTDiscountRatioSeries


# 获取整体折溢价率
from windget import getAnalTDiscountRatio


# 获取折溢价比率偏离系数时间序列
from windget import getAnalDIsRatioDeviSeries


# 获取折溢价比率偏离系数
from windget import getAnalDIsRatioDevi


# 获取净值杠杆时间序列
from windget import getAnalNavLeverSeries


# 获取净值杠杆
from windget import getAnalNavLever


# 获取价格杠杆时间序列
from windget import getAnalPriceLeverSeries


# 获取价格杠杆
from windget import getAnalPriceLever


# 获取名义资金成本时间序列
from windget import getAnalSmFbNamedCostSeries


# 获取名义资金成本
from windget import getAnalSmFbNamedCost


# 获取实际资金成本时间序列
from windget import getAnalSmFbFactualCostSeries


# 获取实际资金成本
from windget import getAnalSmFbFactualCost


# 获取下一定期折算日时间序列
from windget import getAnalNextDiscountDateSeries


# 获取下一定期折算日
from windget import getAnalNextDiscountDate


# 获取本期约定年收益率时间序列
from windget import getFundAgreedAnNuYieldSeries


# 获取本期约定年收益率
from windget import getFundAgreedAnNuYield


# 获取下期约定年收益率时间序列
from windget import getAnalNextAAYieldSeries


# 获取下期约定年收益率
from windget import getAnalNextAAYield


# 获取上折阈值时间序列
from windget import getAnalUpDiscountThresholdSeries


# 获取上折阈值
from windget import getAnalUpDiscountThreshold


# 获取下折阈值时间序列
from windget import getAnalDownDiscountThresholdSeries


# 获取下折阈值
from windget import getAnalDownDiscountThreshold


# 获取上折母基金需涨时间序列
from windget import getAnalUpDiscountPctChangeSeries


# 获取上折母基金需涨
from windget import getAnalUpDiscountPctChange


# 获取下折母基金需跌时间序列
from windget import getAnalDownDiscountPctChangeSeries


# 获取下折母基金需跌
from windget import getAnalDownDiscountPctChange


# 获取持买单量时间序列
from windget import getOiLoiSeries


# 获取持买单量
from windget import getOiLoi


# 获取持买单量(品种)时间序列
from windget import getOiLvOiSeries


# 获取持买单量(品种)
from windget import getOiLvOi


# 获取持买单量进榜会员名称时间序列
from windget import getOiLNameSeries


# 获取持买单量进榜会员名称
from windget import getOiLName


# 获取持买单量(品种)会员名称时间序列
from windget import getOiLvNameSeries


# 获取持买单量(品种)会员名称
from windget import getOiLvName


# 获取持卖单量时间序列
from windget import getOiSoISeries


# 获取持卖单量
from windget import getOiSoI


# 获取持卖单量(品种)时间序列
from windget import getOiSvOiSeries


# 获取持卖单量(品种)
from windget import getOiSvOi


# 获取持卖单量进榜会员名称时间序列
from windget import getOiSNameSeries


# 获取持卖单量进榜会员名称
from windget import getOiSName


# 获取持卖单量(品种)会员名称时间序列
from windget import getOiSvNameSeries


# 获取持卖单量(品种)会员名称
from windget import getOiSvName


# 获取净持仓(品种)时间序列
from windget import getOiNvOiSeries


# 获取净持仓(品种)
from windget import getOiNvOi


# 获取每股营业总收入时间序列
from windget import getGrpSSeries


# 获取每股营业总收入
from windget import getGrpS


# 获取每股营业总收入_GSD时间序列
from windget import getWgsDGrpS2Series


# 获取每股营业总收入_GSD
from windget import getWgsDGrpS2


# 获取每股营业总收入_PIT时间序列
from windget import getFaGrpSSeries


# 获取每股营业总收入_PIT
from windget import getFaGrpS


# 获取每股营业收入(TTM)_PIT时间序列
from windget import getOrPsTtMSeries


# 获取每股营业收入(TTM)_PIT
from windget import getOrPsTtM


# 获取每股营业收入时间序列
from windget import getOrPsSeries


# 获取每股营业收入
from windget import getOrPs


# 获取每股营业收入_GSD时间序列
from windget import getWgsDOrPsSeries


# 获取每股营业收入_GSD
from windget import getWgsDOrPs


# 获取每股营业收入_PIT时间序列
from windget import getFaOrPsSeries


# 获取每股营业收入_PIT
from windget import getFaOrPs


# 获取每股资本公积时间序列
from windget import getSurplusCapitalPsSeries


# 获取每股资本公积
from windget import getSurplusCapitalPs


# 获取每股资本公积_PIT时间序列
from windget import getFaCapSurPpSSeries


# 获取每股资本公积_PIT
from windget import getFaCapSurPpS


# 获取每股盈余公积时间序列
from windget import getSurplusReservePsSeries


# 获取每股盈余公积
from windget import getSurplusReservePs


# 获取每股盈余公积_PIT时间序列
from windget import getFaSppSSeries


# 获取每股盈余公积_PIT
from windget import getFaSppS


# 获取每股未分配利润时间序列
from windget import getUnDistributedPsSeries


# 获取每股未分配利润
from windget import getUnDistributedPs


# 获取每股未分配利润_PIT时间序列
from windget import getFaUnDistributedPsSeries


# 获取每股未分配利润_PIT
from windget import getFaUnDistributedPs


# 获取每股留存收益时间序列
from windget import getRetainedPsSeries


# 获取每股留存收益
from windget import getRetainedPs


# 获取每股留存收益_GSD时间序列
from windget import getWgsDRetainedPs2Series


# 获取每股留存收益_GSD
from windget import getWgsDRetainedPs2


# 获取每股留存收益_PIT时间序列
from windget import getFaRetainedPsSeries


# 获取每股留存收益_PIT
from windget import getFaRetainedPs


# 获取每股息税前利润时间序列
from windget import getEbItPsSeries


# 获取每股息税前利润
from windget import getEbItPs


# 获取每股息税前利润_GSD时间序列
from windget import getWgsDEbItPs2Series


# 获取每股息税前利润_GSD
from windget import getWgsDEbItPs2


# 获取年化净资产收益率时间序列
from windget import getRoeYearlySeries


# 获取年化净资产收益率
from windget import getRoeYearly


# 获取年化总资产报酬率时间序列
from windget import getRoa2YearlySeries


# 获取年化总资产报酬率
from windget import getRoa2Yearly


# 获取年化总资产净利率时间序列
from windget import getRoaYearlySeries


# 获取年化总资产净利率
from windget import getRoaYearly


# 获取销售净利率时间序列
from windget import getNetProfitMarginSeries


# 获取销售净利率
from windget import getNetProfitMargin


# 获取销售净利率(TTM)时间序列
from windget import getNetProfitMarginTtM2Series


# 获取销售净利率(TTM)
from windget import getNetProfitMarginTtM2


# 获取销售净利率_GSD时间序列
from windget import getWgsDNetProfitMarginSeries


# 获取销售净利率_GSD
from windget import getWgsDNetProfitMargin


# 获取销售净利率(TTM)_GSD时间序列
from windget import getNetProfitMarginTtM3Series


# 获取销售净利率(TTM)_GSD
from windget import getNetProfitMarginTtM3


# 获取销售净利率(TTM)_PIT时间序列
from windget import getFaNetProfitMarginTtMSeries


# 获取销售净利率(TTM)_PIT
from windget import getFaNetProfitMarginTtM


# 获取销售净利率(TTM,只有最新数据)时间序列
from windget import getNetProfitMarginTtMSeries


# 获取销售净利率(TTM,只有最新数据)
from windget import getNetProfitMarginTtM


# 获取扣非后销售净利率时间序列
from windget import getNetProfitMarginDeductedSeries


# 获取扣非后销售净利率
from windget import getNetProfitMarginDeducted


# 获取单季度.销售净利率时间序列
from windget import getQfaNetProfitMarginSeries


# 获取单季度.销售净利率
from windget import getQfaNetProfitMargin


# 获取单季度.销售净利率_GSD时间序列
from windget import getWgsDQfaNetProfitMarginSeries


# 获取单季度.销售净利率_GSD
from windget import getWgsDQfaNetProfitMargin


# 获取销售毛利率时间序列
from windget import getGrossProfitMarginSeries


# 获取销售毛利率
from windget import getGrossProfitMargin


# 获取销售毛利率(TTM)时间序列
from windget import getGrossProfitMarginTtM2Series


# 获取销售毛利率(TTM)
from windget import getGrossProfitMarginTtM2


# 获取销售毛利率_GSD时间序列
from windget import getWgsDGrossProfitMarginSeries


# 获取销售毛利率_GSD
from windget import getWgsDGrossProfitMargin


# 获取销售毛利率(TTM)_GSD时间序列
from windget import getGrossProfitMarginTtM3Series


# 获取销售毛利率(TTM)_GSD
from windget import getGrossProfitMarginTtM3


# 获取销售毛利率(TTM)_PIT时间序列
from windget import getFaGrossProfitMarginTtMSeries


# 获取销售毛利率(TTM)_PIT
from windget import getFaGrossProfitMarginTtM


# 获取销售毛利率(TTM,只有最新数据)时间序列
from windget import getGrossProfitMarginTtMSeries


# 获取销售毛利率(TTM,只有最新数据)
from windget import getGrossProfitMarginTtM


# 获取预测销售毛利率(GM)平均值(可选类型)时间序列
from windget import getWestAvgGmSeries


# 获取预测销售毛利率(GM)平均值(可选类型)
from windget import getWestAvgGm


# 获取预测销售毛利率(GM)最大值(可选类型)时间序列
from windget import getWestMaxGmSeries


# 获取预测销售毛利率(GM)最大值(可选类型)
from windget import getWestMaxGm


# 获取预测销售毛利率(GM)最小值(可选类型)时间序列
from windget import getWestMingMSeries


# 获取预测销售毛利率(GM)最小值(可选类型)
from windget import getWestMingM


# 获取预测销售毛利率(GM)中值(可选类型)时间序列
from windget import getWestMediaGmSeries


# 获取预测销售毛利率(GM)中值(可选类型)
from windget import getWestMediaGm


# 获取预测销售毛利率(GM)标准差值(可选类型)时间序列
from windget import getWestStdGmSeries


# 获取预测销售毛利率(GM)标准差值(可选类型)
from windget import getWestStdGm


# 获取单季度.销售毛利率时间序列
from windget import getQfaGrossProfitMarginSeries


# 获取单季度.销售毛利率
from windget import getQfaGrossProfitMargin


# 获取单季度.销售毛利率_GSD时间序列
from windget import getWgsDQfaGrossProfitMarginSeries


# 获取单季度.销售毛利率_GSD
from windget import getWgsDQfaGrossProfitMargin


# 获取销售成本率时间序列
from windget import getCogsToSalesSeries


# 获取销售成本率
from windget import getCogsToSales


# 获取销售成本率_GSD时间序列
from windget import getWgsDCogsToSalesSeries


# 获取销售成本率_GSD
from windget import getWgsDCogsToSales


# 获取销售成本率(TTM)_PIT时间序列
from windget import getFaSalesToCostTtMSeries


# 获取销售成本率(TTM)_PIT
from windget import getFaSalesToCostTtM


# 获取成本费用利润率时间序列
from windget import getNpToCostExpenseSeries


# 获取成本费用利润率
from windget import getNpToCostExpense


# 获取成本费用利润率(TTM)_PIT时间序列
from windget import getFaProtoCostTtMSeries


# 获取成本费用利润率(TTM)_PIT
from windget import getFaProtoCostTtM


# 获取单季度.成本费用利润率时间序列
from windget import getNpToCostExpenseQfaSeries


# 获取单季度.成本费用利润率
from windget import getNpToCostExpenseQfa


# 获取销售期间费用率时间序列
from windget import getExpenseToSalesSeries


# 获取销售期间费用率
from windget import getExpenseToSales


# 获取销售期间费用率(TTM)时间序列
from windget import getExpenseToSalesTtM2Series


# 获取销售期间费用率(TTM)
from windget import getExpenseToSalesTtM2


# 获取销售期间费用率(TTM)_GSD时间序列
from windget import getExpenseToSalesTtM3Series


# 获取销售期间费用率(TTM)_GSD
from windget import getExpenseToSalesTtM3


# 获取销售期间费用率(TTM)_PIT时间序列
from windget import getFaExpenseToSalesTtMSeries


# 获取销售期间费用率(TTM)_PIT
from windget import getFaExpenseToSalesTtM


# 获取销售期间费用率(TTM,只有最新数据)时间序列
from windget import getExpenseToSalesTtMSeries


# 获取销售期间费用率(TTM,只有最新数据)
from windget import getExpenseToSalesTtM


# 获取主营业务比率时间序列
from windget import getOpToEBTSeries


# 获取主营业务比率
from windget import getOpToEBT


# 获取单季度.主营业务比率时间序列
from windget import getOpToEBTQfaSeries


# 获取单季度.主营业务比率
from windget import getOpToEBTQfa


# 获取净利润/营业总收入时间序列
from windget import getProfitToGrSeries


# 获取净利润/营业总收入
from windget import getProfitToGr


# 获取净利润/营业总收入(TTM)时间序列
from windget import getProfitToGrTtM2Series


# 获取净利润/营业总收入(TTM)
from windget import getProfitToGrTtM2


# 获取净利润/营业总收入_GSD时间序列
from windget import getWgsDDupontNpToSalesSeries


# 获取净利润/营业总收入_GSD
from windget import getWgsDDupontNpToSales


# 获取净利润/营业总收入(TTM)_GSD时间序列
from windget import getProfitToGrTtM3Series


# 获取净利润/营业总收入(TTM)_GSD
from windget import getProfitToGrTtM3


# 获取净利润/营业总收入(TTM)_PIT时间序列
from windget import getFaProfitToGrTtMSeries


# 获取净利润/营业总收入(TTM)_PIT
from windget import getFaProfitToGrTtM


# 获取净利润/营业总收入(TTM,只有最新数据)时间序列
from windget import getProfitToGrTtMSeries


# 获取净利润/营业总收入(TTM,只有最新数据)
from windget import getProfitToGrTtM


# 获取单季度.净利润/营业总收入时间序列
from windget import getQfaProfitToGrSeries


# 获取单季度.净利润/营业总收入
from windget import getQfaProfitToGr


# 获取营业利润/营业总收入时间序列
from windget import getOpToGrSeries


# 获取营业利润/营业总收入
from windget import getOpToGr


# 获取营业利润/营业总收入(TTM)时间序列
from windget import getOpToGrTtM2Series


# 获取营业利润/营业总收入(TTM)
from windget import getOpToGrTtM2


# 获取营业利润/营业总收入_GSD时间序列
from windget import getWgsDOpToGrSeries


# 获取营业利润/营业总收入_GSD
from windget import getWgsDOpToGr


# 获取营业利润/营业总收入(TTM)_GSD时间序列
from windget import getOpToGrTtM3Series


# 获取营业利润/营业总收入(TTM)_GSD
from windget import getOpToGrTtM3


# 获取营业利润/营业总收入(TTM)_PIT时间序列
from windget import getFaOpToGrTtMSeries


# 获取营业利润/营业总收入(TTM)_PIT
from windget import getFaOpToGrTtM


# 获取营业利润/营业总收入(TTM,只有最新数据)时间序列
from windget import getOpToGrTtMSeries


# 获取营业利润/营业总收入(TTM,只有最新数据)
from windget import getOpToGrTtM


# 获取单季度.营业利润/营业总收入时间序列
from windget import getQfaOpToGrSeries


# 获取单季度.营业利润/营业总收入
from windget import getQfaOpToGr


# 获取息税前利润/营业总收入时间序列
from windget import getEbItToGrSeries


# 获取息税前利润/营业总收入
from windget import getEbItToGr


# 获取息税前利润/营业总收入_GSD时间序列
from windget import getWgsDDupontEbItToSalesSeries


# 获取息税前利润/营业总收入_GSD
from windget import getWgsDDupontEbItToSales


# 获取息税前利润/营业总收入(TTM)_PIT时间序列
from windget import getFaEbItToGrTtMSeries


# 获取息税前利润/营业总收入(TTM)_PIT
from windget import getFaEbItToGrTtM


# 获取营业总成本/营业总收入时间序列
from windget import getGcToGrSeries


# 获取营业总成本/营业总收入
from windget import getGcToGr


# 获取营业总成本/营业总收入(TTM)时间序列
from windget import getGcToGrTtM2Series


# 获取营业总成本/营业总收入(TTM)
from windget import getGcToGrTtM2


# 获取营业总成本/营业总收入_GSD时间序列
from windget import getWgsDGcToGrSeries


# 获取营业总成本/营业总收入_GSD
from windget import getWgsDGcToGr


# 获取营业总成本/营业总收入(TTM)_GSD时间序列
from windget import getGcToGrTtM3Series


# 获取营业总成本/营业总收入(TTM)_GSD
from windget import getGcToGrTtM3


# 获取营业总成本/营业总收入(TTM)_PIT时间序列
from windget import getFaOctoGrTtMSeries


# 获取营业总成本/营业总收入(TTM)_PIT
from windget import getFaOctoGrTtM


# 获取营业总成本/营业总收入(TTM,只有最新数据)时间序列
from windget import getGcToGrTtMSeries


# 获取营业总成本/营业总收入(TTM,只有最新数据)
from windget import getGcToGrTtM


# 获取单季度.营业总成本/营业总收入时间序列
from windget import getQfaGcToGrSeries


# 获取单季度.营业总成本/营业总收入
from windget import getQfaGcToGr


# 获取销售费用/营业总收入时间序列
from windget import getOperateExpenseToGrSeries


# 获取销售费用/营业总收入
from windget import getOperateExpenseToGr


# 获取销售费用/营业总收入(TTM)时间序列
from windget import getOperateExpenseToGrTtM2Series


# 获取销售费用/营业总收入(TTM)
from windget import getOperateExpenseToGrTtM2


# 获取销售费用/营业总收入_GSD时间序列
from windget import getWgsDOperateExpenseToGrSeries


# 获取销售费用/营业总收入_GSD
from windget import getWgsDOperateExpenseToGr


# 获取销售费用/营业总收入(TTM)_GSD时间序列
from windget import getOperateExpenseToGrTtM3Series


# 获取销售费用/营业总收入(TTM)_GSD
from windget import getOperateExpenseToGrTtM3


# 获取销售费用/营业总收入(TTM)_PIT时间序列
from windget import getFaSellExpenseToGrTtMSeries


# 获取销售费用/营业总收入(TTM)_PIT
from windget import getFaSellExpenseToGrTtM


# 获取销售费用/营业总收入(TTM,只有最新数据)时间序列
from windget import getOperateExpenseToGrTtMSeries


# 获取销售费用/营业总收入(TTM,只有最新数据)
from windget import getOperateExpenseToGrTtM


# 获取单季度.销售费用/营业总收入时间序列
from windget import getQfaSaleExpenseToGrSeries


# 获取单季度.销售费用/营业总收入
from windget import getQfaSaleExpenseToGr


# 获取管理费用/营业总收入时间序列
from windget import getAdminExpenseToGrSeries


# 获取管理费用/营业总收入
from windget import getAdminExpenseToGr


# 获取管理费用/营业总收入(TTM)时间序列
from windget import getAdminExpenseToGrTtM2Series


# 获取管理费用/营业总收入(TTM)
from windget import getAdminExpenseToGrTtM2


# 获取管理费用/营业总收入_GSD时间序列
from windget import getWgsDAdminExpenseToGrSeries


# 获取管理费用/营业总收入_GSD
from windget import getWgsDAdminExpenseToGr


# 获取管理费用/营业总收入(TTM)_GSD时间序列
from windget import getAdminExpenseToGrTtM3Series


# 获取管理费用/营业总收入(TTM)_GSD
from windget import getAdminExpenseToGrTtM3


# 获取管理费用/营业总收入(TTM)_PIT时间序列
from windget import getFaAdminExpenseToGrTtMSeries


# 获取管理费用/营业总收入(TTM)_PIT
from windget import getFaAdminExpenseToGrTtM


# 获取管理费用/营业总收入(TTM,只有最新数据)时间序列
from windget import getAdminExpenseToGrTtMSeries


# 获取管理费用/营业总收入(TTM,只有最新数据)
from windget import getAdminExpenseToGrTtM


# 获取单季度.管理费用/营业总收入时间序列
from windget import getQfaAdminExpenseToGrSeries


# 获取单季度.管理费用/营业总收入
from windget import getQfaAdminExpenseToGr


# 获取财务费用/营业总收入时间序列
from windget import getFinaExpenseToGrSeries


# 获取财务费用/营业总收入
from windget import getFinaExpenseToGr


# 获取财务费用/营业总收入(TTM)时间序列
from windget import getFinaExpenseToGrTtM2Series


# 获取财务费用/营业总收入(TTM)
from windget import getFinaExpenseToGrTtM2


# 获取财务费用/营业总收入_GSD时间序列
from windget import getWgsDFinaExpenseToGrSeries


# 获取财务费用/营业总收入_GSD
from windget import getWgsDFinaExpenseToGr


# 获取财务费用/营业总收入(TTM)_GSD时间序列
from windget import getFinaExpenseToGrTtM3Series


# 获取财务费用/营业总收入(TTM)_GSD
from windget import getFinaExpenseToGrTtM3


# 获取财务费用/营业总收入(TTM)_PIT时间序列
from windget import getFaFinaExpenseToGrTtMSeries


# 获取财务费用/营业总收入(TTM)_PIT
from windget import getFaFinaExpenseToGrTtM


# 获取财务费用/营业总收入(TTM,只有最新数据)时间序列
from windget import getFinaExpenseToGrTtMSeries


# 获取财务费用/营业总收入(TTM,只有最新数据)
from windget import getFinaExpenseToGrTtM


# 获取单季度.财务费用/营业总收入时间序列
from windget import getQfaFinaExpenseToGrSeries


# 获取单季度.财务费用/营业总收入
from windget import getQfaFinaExpenseToGr


# 获取经营活动净收益/利润总额时间序列
from windget import getOperateIncomeToEBTSeries


# 获取经营活动净收益/利润总额
from windget import getOperateIncomeToEBT


# 获取经营活动净收益/利润总额(TTM)时间序列
from windget import getOperateIncomeToEBTTtM2Series


# 获取经营活动净收益/利润总额(TTM)
from windget import getOperateIncomeToEBTTtM2


# 获取经营活动净收益/利润总额_GSD时间序列
from windget import getWgsDOperateIncomeToEBTSeries


# 获取经营活动净收益/利润总额_GSD
from windget import getWgsDOperateIncomeToEBT


# 获取经营活动净收益/利润总额(TTM)_GSD时间序列
from windget import getOperateIncomeToEBTTtM3Series


# 获取经营活动净收益/利润总额(TTM)_GSD
from windget import getOperateIncomeToEBTTtM3


# 获取经营活动净收益/利润总额_PIT时间序列
from windget import getFaOperIncomeToPbtSeries


# 获取经营活动净收益/利润总额_PIT
from windget import getFaOperIncomeToPbt


# 获取经营活动净收益/利润总额(TTM)_PIT时间序列
from windget import getFaOperIncomeToPbtTtMSeries


# 获取经营活动净收益/利润总额(TTM)_PIT
from windget import getFaOperIncomeToPbtTtM


# 获取经营活动净收益/利润总额(TTM,只有最新数据)时间序列
from windget import getOperateIncomeToEBTTtMSeries


# 获取经营活动净收益/利润总额(TTM,只有最新数据)
from windget import getOperateIncomeToEBTTtM


# 获取单季度.经营活动净收益/利润总额时间序列
from windget import getQfaOperateIncomeToEBTSeries


# 获取单季度.经营活动净收益/利润总额
from windget import getQfaOperateIncomeToEBT


# 获取价值变动净收益/利润总额时间序列
from windget import getInvestIncomeToEBTSeries


# 获取价值变动净收益/利润总额
from windget import getInvestIncomeToEBT


# 获取价值变动净收益/利润总额(TTM)时间序列
from windget import getInvestIncomeToEBTTtM2Series


# 获取价值变动净收益/利润总额(TTM)
from windget import getInvestIncomeToEBTTtM2


# 获取价值变动净收益/利润总额_GSD时间序列
from windget import getWgsDInvestIncomeToEBTSeries


# 获取价值变动净收益/利润总额_GSD
from windget import getWgsDInvestIncomeToEBT


# 获取价值变动净收益/利润总额(TTM)_GSD时间序列
from windget import getInvestIncomeToEBTTtM3Series


# 获取价值变动净收益/利润总额(TTM)_GSD
from windget import getInvestIncomeToEBTTtM3


# 获取价值变动净收益/利润总额(TTM)_PIT时间序列
from windget import getFaChgValueToPbtTtMSeries


# 获取价值变动净收益/利润总额(TTM)_PIT
from windget import getFaChgValueToPbtTtM


# 获取价值变动净收益/利润总额(TTM,只有最新数据)时间序列
from windget import getInvestIncomeToEBTTtMSeries


# 获取价值变动净收益/利润总额(TTM,只有最新数据)
from windget import getInvestIncomeToEBTTtM


# 获取单季度.价值变动净收益/利润总额时间序列
from windget import getQfaInvestIncomeToEBTSeries


# 获取单季度.价值变动净收益/利润总额
from windget import getQfaInvestIncomeToEBT


# 获取营业外收支净额/利润总额时间序列
from windget import getNonOperateProfitToEBTSeries


# 获取营业外收支净额/利润总额
from windget import getNonOperateProfitToEBT


# 获取营业外收支净额/利润总额(TTM)时间序列
from windget import getNonOperateProfitToEBTTtM2Series


# 获取营业外收支净额/利润总额(TTM)
from windget import getNonOperateProfitToEBTTtM2


# 获取营业外收支净额/利润总额_GSD时间序列
from windget import getWgsDNonOperateProfitToEBTSeries


# 获取营业外收支净额/利润总额_GSD
from windget import getWgsDNonOperateProfitToEBT


# 获取营业外收支净额/利润总额(TTM)_GSD时间序列
from windget import getNonOperateProfitToEBTTtM3Series


# 获取营业外收支净额/利润总额(TTM)_GSD
from windget import getNonOperateProfitToEBTTtM3


# 获取营业外收支净额/利润总额(TTM)_PIT时间序列
from windget import getFaNonOperProfitToPbtTtMSeries


# 获取营业外收支净额/利润总额(TTM)_PIT
from windget import getFaNonOperProfitToPbtTtM


# 获取营业外收支净额/利润总额(TTM,只有最新数据)时间序列
from windget import getNonOperateProfitToEBTTtMSeries


# 获取营业外收支净额/利润总额(TTM,只有最新数据)
from windget import getNonOperateProfitToEBTTtM


# 获取扣除非经常损益后的净利润/净利润时间序列
from windget import getDeductedProfitToProfitSeries


# 获取扣除非经常损益后的净利润/净利润
from windget import getDeductedProfitToProfit


# 获取扣除非经常损益后的净利润/净利润_GSD时间序列
from windget import getWgsDDeductedProfitToProfitSeries


# 获取扣除非经常损益后的净利润/净利润_GSD
from windget import getWgsDDeductedProfitToProfit


# 获取单季度.扣除非经常损益后的净利润/净利润时间序列
from windget import getQfaDeductedProfitToProfitSeries


# 获取单季度.扣除非经常损益后的净利润/净利润
from windget import getQfaDeductedProfitToProfit


# 获取销售商品提供劳务收到的现金/营业收入时间序列
from windget import getSalesCashIntoOrSeries


# 获取销售商品提供劳务收到的现金/营业收入
from windget import getSalesCashIntoOr


# 获取销售商品提供劳务收到的现金/营业收入(TTM)时间序列
from windget import getSalesCashIntoOrTtM2Series


# 获取销售商品提供劳务收到的现金/营业收入(TTM)
from windget import getSalesCashIntoOrTtM2


# 获取销售商品提供劳务收到的现金/营业收入_PIT时间序列
from windget import getFaSalesCashToOrSeries


# 获取销售商品提供劳务收到的现金/营业收入_PIT
from windget import getFaSalesCashToOr


# 获取销售商品提供劳务收到的现金/营业收入(TTM)_PIT时间序列
from windget import getFaSalesCashToOrTtMSeries


# 获取销售商品提供劳务收到的现金/营业收入(TTM)_PIT
from windget import getFaSalesCashToOrTtM


# 获取销售商品提供劳务收到的现金/营业收入(TTM,只有最新数据)时间序列
from windget import getSalesCashIntoOrTtMSeries


# 获取销售商品提供劳务收到的现金/营业收入(TTM,只有最新数据)
from windget import getSalesCashIntoOrTtM


# 获取单季度.销售商品提供劳务收到的现金/营业收入时间序列
from windget import getQfaSalesCashIntoOrSeries


# 获取单季度.销售商品提供劳务收到的现金/营业收入
from windget import getQfaSalesCashIntoOr


# 获取净利润现金含量时间序列
from windget import getFaNetProfitCashCoverSeries


# 获取净利润现金含量
from windget import getFaNetProfitCashCover


# 获取资本支出/折旧和摊销时间序列
from windget import getCapitalizedTodaSeries


# 获取资本支出/折旧和摊销
from windget import getCapitalizedToda


# 获取资本支出/折旧和摊销_GSD时间序列
from windget import getWgsDCapitalizedTodaSeries


# 获取资本支出/折旧和摊销_GSD
from windget import getWgsDCapitalizedToda


# 获取经营性现金净流量/营业总收入时间序列
from windget import getOCFToSalesSeries


# 获取经营性现金净流量/营业总收入
from windget import getOCFToSales


# 获取现金满足投资比率时间序列
from windget import getOCFToInvestStockDividendSeries


# 获取现金满足投资比率
from windget import getOCFToInvestStockDividend


# 获取现金营运指数时间序列
from windget import getOCFToOpSeries


# 获取现金营运指数
from windget import getOCFToOp


# 获取全部资产现金回收率时间序列
from windget import getOCFToAssetsSeries


# 获取全部资产现金回收率
from windget import getOCFToAssets


# 获取现金股利保障倍数时间序列
from windget import getOCFToDividendSeries


# 获取现金股利保障倍数
from windget import getOCFToDividend


# 获取现金股利保障倍数(TTM)_PIT时间序列
from windget import getFaCashDivCoverTtMSeries


# 获取现金股利保障倍数(TTM)_PIT
from windget import getFaCashDivCoverTtM


# 获取资产负债率时间序列
from windget import getDebtToAssetsSeries


# 获取资产负债率
from windget import getDebtToAssets


# 获取资产负债率_GSD时间序列
from windget import getWgsDDebtToAssetsSeries


# 获取资产负债率_GSD
from windget import getWgsDDebtToAssets


# 获取资产负债率_PIT时间序列
from windget import getFaDebtToAssetSeries


# 获取资产负债率_PIT
from windget import getFaDebtToAsset


# 获取净资产负债率时间序列
from windget import getFaDebtToEqYSeries


# 获取净资产负债率
from windget import getFaDebtToEqY


# 获取剔除预收账款的资产负债率(公告值)_GSD时间序列
from windget import getWgsDAnnouncedDeductedDebtToAssetsSeries


# 获取剔除预收账款的资产负债率(公告值)_GSD
from windget import getWgsDAnnouncedDeductedDebtToAssets


# 获取剔除预收款项后的资产负债率时间序列
from windget import getDeductedDebtToAssets2Series


# 获取剔除预收款项后的资产负债率
from windget import getDeductedDebtToAssets2


# 获取剔除预收款项后的资产负债率(公告口径)时间序列
from windget import getDeductedDebtToAssetsSeries


# 获取剔除预收款项后的资产负债率(公告口径)
from windget import getDeductedDebtToAssets


# 获取剔除预收账款后的资产负债率_GSD时间序列
from windget import getWgsDDeductedDebtToAssetsSeries


# 获取剔除预收账款后的资产负债率_GSD
from windget import getWgsDDeductedDebtToAssets


# 获取长期资本负债率时间序列
from windget import getLongDebtToLongCaptIAlSeries


# 获取长期资本负债率
from windget import getLongDebtToLongCaptIAl


# 获取长期资产适合率时间序列
from windget import getLongCapitalToInvestmentSeries


# 获取长期资产适合率
from windget import getLongCapitalToInvestment


# 获取权益乘数时间序列
from windget import getAssetsToEquitySeries


# 获取权益乘数
from windget import getAssetsToEquity


# 获取权益乘数_GSD时间序列
from windget import getWgsDAssetsToEquitySeries


# 获取权益乘数_GSD
from windget import getWgsDAssetsToEquity


# 获取股东权益比时间序列
from windget import getEquityToAssetSeries


# 获取股东权益比
from windget import getEquityToAsset


# 获取股东权益比率_PIT时间序列
from windget import getFaEquityAssetRadioSeries


# 获取股东权益比率_PIT
from windget import getFaEquityAssetRadio


# 获取流动资产/总资产时间序列
from windget import getCatoAssetsSeries


# 获取流动资产/总资产
from windget import getCatoAssets


# 获取流动资产/总资产_GSD时间序列
from windget import getWgsDCatoAssetsSeries


# 获取流动资产/总资产_GSD
from windget import getWgsDCatoAssets


# 获取非流动资产/总资产时间序列
from windget import getNcaToAssetsSeries


# 获取非流动资产/总资产
from windget import getNcaToAssets


# 获取非流动资产/总资产_GSD时间序列
from windget import getWgsDNcaToAssetsSeries


# 获取非流动资产/总资产_GSD
from windget import getWgsDNcaToAssets


# 获取流动负债权益比率时间序列
from windget import getCurrentDebtToEquitySeries


# 获取流动负债权益比率
from windget import getCurrentDebtToEquity


# 获取非流动负债权益比率时间序列
from windget import getLongDebtToEquitySeries


# 获取非流动负债权益比率
from windget import getLongDebtToEquity


# 获取有形资产/总资产时间序列
from windget import getTangibleAssetsToAssetsSeries


# 获取有形资产/总资产
from windget import getTangibleAssetsToAssets


# 获取有形资产/总资产_GSD时间序列
from windget import getWgsDTangibleAssetsToAssetsSeries


# 获取有形资产/总资产_GSD
from windget import getWgsDTangibleAssetsToAssets


# 获取归属母公司股东的权益/全部投入资本时间序列
from windget import getEquityToTotalCapitalSeries


# 获取归属母公司股东的权益/全部投入资本
from windget import getEquityToTotalCapital


# 获取带息债务/全部投入资本时间序列
from windget import getIntDebtToTotalCapSeries


# 获取带息债务/全部投入资本
from windget import getIntDebtToTotalCap


# 获取带息债务/全部投入资本_GSD时间序列
from windget import getWgsDInterestDebtToTotalCapitalSeries


# 获取带息债务/全部投入资本_GSD
from windget import getWgsDInterestDebtToTotalCapital


# 获取带息债务/全部投入资本_PIT时间序列
from windget import getFaInterestDebtToCapitalSeries


# 获取带息债务/全部投入资本_PIT
from windget import getFaInterestDebtToCapital


# 获取流动负债/负债合计时间序列
from windget import getCurrentDebtToDebtSeries


# 获取流动负债/负债合计
from windget import getCurrentDebtToDebt


# 获取流动负债/负债合计_GSD时间序列
from windget import getWgsDCurrentDebtToDebtSeries


# 获取流动负债/负债合计_GSD
from windget import getWgsDCurrentDebtToDebt


# 获取非流动负债/负债合计时间序列
from windget import getLongDebToDebtSeries


# 获取非流动负债/负债合计
from windget import getLongDebToDebt


# 获取非流动负债/负债合计_GSD时间序列
from windget import getWgsDLongDebToDebtSeries


# 获取非流动负债/负债合计_GSD
from windget import getWgsDLongDebToDebt


# 获取资本固定化比率时间序列
from windget import getNcaToEquitySeries


# 获取资本固定化比率
from windget import getNcaToEquity


# 获取有息负债率时间序列
from windget import getIbDebtRatioSeries


# 获取有息负债率
from windget import getIbDebtRatio


# 获取流动比率时间序列
from windget import getCurrentSeries


# 获取流动比率
from windget import getCurrent


# 获取流动比率_GSD时间序列
from windget import getWgsDCurrentSeries


# 获取流动比率_GSD
from windget import getWgsDCurrent


# 获取流动比率_PIT时间序列
from windget import getFaCurrentSeries


# 获取流动比率_PIT
from windget import getFaCurrent


# 获取速动比率时间序列
from windget import getQuickSeries


# 获取速动比率
from windget import getQuick


# 获取速动比率_GSD时间序列
from windget import getWgsDQuickSeries


# 获取速动比率_GSD
from windget import getWgsDQuick


# 获取速动比率_PIT时间序列
from windget import getFaQuickSeries


# 获取速动比率_PIT
from windget import getFaQuick


# 获取超速动比率_PIT时间序列
from windget import getFaSuperQuickSeries


# 获取超速动比率_PIT
from windget import getFaSuperQuick


# 获取保守速动比率时间序列
from windget import getCashRatioSeries


# 获取保守速动比率
from windget import getCashRatio


# 获取保守速动比率_GSD时间序列
from windget import getWgsDCashRatioSeries


# 获取保守速动比率_GSD
from windget import getWgsDCashRatio


# 获取现金比率时间序列
from windget import getCashToCurrentDebtSeries


# 获取现金比率
from windget import getCashToCurrentDebt


# 获取现金到期债务比时间序列
from windget import getOCFToQuickDebtSeries


# 获取现金到期债务比
from windget import getOCFToQuickDebt


# 获取产权比率时间序列
from windget import getDebtToEquitySeries


# 获取产权比率
from windget import getDebtToEquity


# 获取产权比率_GSD时间序列
from windget import getWgsDDebtToEquitySeries


# 获取产权比率_GSD
from windget import getWgsDDebtToEquity


# 获取产权比率_PIT时间序列
from windget import getFaDebtToEquitySeries


# 获取产权比率_PIT
from windget import getFaDebtToEquity


# 获取净负债率时间序列
from windget import getFaNetDebtRatioSeries


# 获取净负债率
from windget import getFaNetDebtRatio


# 获取净负债率_GSD时间序列
from windget import getWgsDNetDebtRatioSeries


# 获取净负债率_GSD
from windget import getWgsDNetDebtRatio


# 获取净负债率(公告值)_GSD时间序列
from windget import getWgsDNetDebtRatioArdSeries


# 获取净负债率(公告值)_GSD
from windget import getWgsDNetDebtRatioArd


# 获取归属母公司股东的权益/负债合计时间序列
from windget import getEquityToDebtSeries


# 获取归属母公司股东的权益/负债合计
from windget import getEquityToDebt


# 获取归属母公司股东的权益/负债合计_GSD时间序列
from windget import getWgsDEquityToDebtSeries


# 获取归属母公司股东的权益/负债合计_GSD
from windget import getWgsDEquityToDebt


# 获取归属母公司股东的权益/带息债务时间序列
from windget import getEquityToInterestDebtSeries


# 获取归属母公司股东的权益/带息债务
from windget import getEquityToInterestDebt


# 获取归属母公司股东的权益/带息债务_GSD时间序列
from windget import getWgsDEquityToInterestDebtSeries


# 获取归属母公司股东的权益/带息债务_GSD
from windget import getWgsDEquityToInterestDebt


# 获取归属母公司股东的权益/带息债务_PIT时间序列
from windget import getFaEquityToInterestDebtSeries


# 获取归属母公司股东的权益/带息债务_PIT
from windget import getFaEquityToInterestDebt


# 获取有形资产/负债合计时间序列
from windget import getTangibleAssetToDebtSeries


# 获取有形资产/负债合计
from windget import getTangibleAssetToDebt


# 获取有形资产/负债合计_GSD时间序列
from windget import getWgsDTangibleAssetToDebtSeries


# 获取有形资产/负债合计_GSD
from windget import getWgsDTangibleAssetToDebt


# 获取有形资产/带息债务时间序列
from windget import getTangAssetToIntDebtSeries


# 获取有形资产/带息债务
from windget import getTangAssetToIntDebt


# 获取有形资产/带息债务_GSD时间序列
from windget import getWgsDTangibleAssetToInterestDebtSeries


# 获取有形资产/带息债务_GSD
from windget import getWgsDTangibleAssetToInterestDebt


# 获取有形资产/净债务时间序列
from windget import getTangibleAssetToNetDebtSeries


# 获取有形资产/净债务
from windget import getTangibleAssetToNetDebt


# 获取有形资产/净债务_GSD时间序列
from windget import getWgsDTangibleAssetToNetDebtSeries


# 获取有形资产/净债务_GSD
from windget import getWgsDTangibleAssetToNetDebt


# 获取有形净值债务率时间序列
from windget import getDebtToTangibleEquitySeries


# 获取有形净值债务率
from windget import getDebtToTangibleEquity


# 获取有形净值债务率_PIT时间序列
from windget import getFaDebtToTangibleAFyBlSeries


# 获取有形净值债务率_PIT
from windget import getFaDebtToTangibleAFyBl


# 获取息税折旧摊销前利润/负债合计时间序列
from windget import getEbItDatoDebtSeries


# 获取息税折旧摊销前利润/负债合计
from windget import getEbItDatoDebt


# 获取息税折旧摊销前利润/负债合计_GSD时间序列
from windget import getWgsDEbItDatoDebtSeries


# 获取息税折旧摊销前利润/负债合计_GSD
from windget import getWgsDEbItDatoDebt


# 获取非筹资性现金净流量与流动负债的比率时间序列
from windget import getOcFicFToCurrentDebtSeries


# 获取非筹资性现金净流量与流动负债的比率
from windget import getOcFicFToCurrentDebt


# 获取非筹资性现金净流量与负债总额的比率时间序列
from windget import getOcFicFToDebtSeries


# 获取非筹资性现金净流量与负债总额的比率
from windget import getOcFicFToDebt


# 获取长期债务与营运资金比率时间序列
from windget import getLongDebtToWorkingCapitalSeries


# 获取长期债务与营运资金比率
from windget import getLongDebtToWorkingCapital


# 获取长期债务与营运资金比率_GSD时间序列
from windget import getWgsDLongDebtToWorkingCapitalSeries


# 获取长期债务与营运资金比率_GSD
from windget import getWgsDLongDebtToWorkingCapital


# 获取长期负债占比时间序列
from windget import getLongDebtToDebtSeries


# 获取长期负债占比
from windget import getLongDebtToDebt


# 获取净债务/股权价值时间序列
from windget import getNetDebtToEvSeries


# 获取净债务/股权价值
from windget import getNetDebtToEv


# 获取带息债务/股权价值时间序列
from windget import getInterestDebtToEvSeries


# 获取带息债务/股权价值
from windget import getInterestDebtToEv


# 获取营业周期时间序列
from windget import getTurnDaysSeries


# 获取营业周期
from windget import getTurnDays


# 获取营业周期_GSD时间序列
from windget import getWgsDTurnDaysSeries


# 获取营业周期_GSD
from windget import getWgsDTurnDays


# 获取营业周期(TTM)_PIT时间序列
from windget import getFaTurnDaysTtMSeries


# 获取营业周期(TTM)_PIT
from windget import getFaTurnDaysTtM


# 获取净营业周期时间序列
from windget import getNetTurnDaysSeries


# 获取净营业周期
from windget import getNetTurnDays


# 获取存货周转天数时间序列
from windget import getInvTurnDaysSeries


# 获取存货周转天数
from windget import getInvTurnDays


# 获取存货周转天数_GSD时间序列
from windget import getWgsDInvTurnDaysSeries


# 获取存货周转天数_GSD
from windget import getWgsDInvTurnDays


# 获取存货周转天数(TTM)_PIT时间序列
from windget import getFaInvTurnDaysTtMSeries


# 获取存货周转天数(TTM)_PIT
from windget import getFaInvTurnDaysTtM


# 获取应收账款周转天数时间序列
from windget import getArturNDaysSeries


# 获取应收账款周转天数
from windget import getArturNDays


# 获取应收账款周转天数_GSD时间序列
from windget import getWgsDArturNDaysSeries


# 获取应收账款周转天数_GSD
from windget import getWgsDArturNDays


# 获取应收账款周转天数(TTM)_PIT时间序列
from windget import getFaArturNDaysTtMSeries


# 获取应收账款周转天数(TTM)_PIT
from windget import getFaArturNDaysTtM


# 获取应付账款周转天数时间序列
from windget import getApTurnDaysSeries


# 获取应付账款周转天数
from windget import getApTurnDays


# 获取应付账款周转天数_GSD时间序列
from windget import getWgsDApTurnDaysSeries


# 获取应付账款周转天数_GSD
from windget import getWgsDApTurnDays


# 获取应付账款周转天数(TTM)_PIT时间序列
from windget import getFaApTurnDaysTtMSeries


# 获取应付账款周转天数(TTM)_PIT
from windget import getFaApTurnDaysTtM


# 获取存货周转率时间序列
from windget import getInvTurnSeries


# 获取存货周转率
from windget import getInvTurn


# 获取存货周转率_GSD时间序列
from windget import getWgsDInvTurnSeries


# 获取存货周转率_GSD
from windget import getWgsDInvTurn


# 获取存货周转率(TTM)_PIT时间序列
from windget import getFaInvTurnTtMSeries


# 获取存货周转率(TTM)_PIT
from windget import getFaInvTurnTtM


# 获取应收账款周转率时间序列
from windget import getArturNSeries


# 获取应收账款周转率
from windget import getArturN


# 获取应收账款周转率(含坏账准备)时间序列
from windget import getFaArturNReserveSeries


# 获取应收账款周转率(含坏账准备)
from windget import getFaArturNReserve


# 获取应收账款周转率_GSD时间序列
from windget import getWgsDArturNSeries


# 获取应收账款周转率_GSD
from windget import getWgsDArturN


# 获取应收账款周转率(TTM)_PIT时间序列
from windget import getFaArturNTtMSeries


# 获取应收账款周转率(TTM)_PIT
from windget import getFaArturNTtM


# 获取应收账款及应收票据周转率时间序列
from windget import getFaArnRTurnSeries


# 获取应收账款及应收票据周转率
from windget import getFaArnRTurn


# 获取流动资产周转率时间序列
from windget import getCaTurnSeries


# 获取流动资产周转率
from windget import getCaTurn


# 获取流动资产周转率_GSD时间序列
from windget import getWgsDCaTurnSeries


# 获取流动资产周转率_GSD
from windget import getWgsDCaTurn


# 获取流动资产周转率(TTM)_PIT时间序列
from windget import getFaCurRtAssetsTRateTtMSeries


# 获取流动资产周转率(TTM)_PIT
from windget import getFaCurRtAssetsTRateTtM


# 获取非流动资产周转率时间序列
from windget import getNonCurrentAssetsTurnSeries


# 获取非流动资产周转率
from windget import getNonCurrentAssetsTurn


# 获取营运资本周转率时间序列
from windget import getOperateCaptIAlTurnSeries


# 获取营运资本周转率
from windget import getOperateCaptIAlTurn


# 获取固定资产周转率时间序列
from windget import getFaTurnSeries


# 获取固定资产周转率
from windget import getFaTurn


# 获取固定资产周转率_GSD时间序列
from windget import getWgsDFaTurnSeries


# 获取固定资产周转率_GSD
from windget import getWgsDFaTurn


# 获取固定资产周转率(TTM)_PIT时间序列
from windget import getFaFaTurnTtMSeries


# 获取固定资产周转率(TTM)_PIT
from windget import getFaFaTurnTtM


# 获取总资产周转率时间序列
from windget import getAssetsTurnSeries


# 获取总资产周转率
from windget import getAssetsTurn


# 获取总资产周转率(TTM)时间序列
from windget import getTurnoverTtMSeries


# 获取总资产周转率(TTM)
from windget import getTurnoverTtM


# 获取总资产周转率_GSD时间序列
from windget import getWgsDAssetsTurnSeries


# 获取总资产周转率_GSD
from windget import getWgsDAssetsTurn


# 获取总资产周转率(TTM)_PIT时间序列
from windget import getFaTaTurnTtMSeries


# 获取总资产周转率(TTM)_PIT
from windget import getFaTaTurnTtM


# 获取应付账款周转率时间序列
from windget import getApTurnSeries


# 获取应付账款周转率
from windget import getApTurn


# 获取应付账款周转率_GSD时间序列
from windget import getWgsDApTurnSeries


# 获取应付账款周转率_GSD
from windget import getWgsDApTurn


# 获取应付账款周转率(TTM)_PIT时间序列
from windget import getFaApTurnTtMSeries


# 获取应付账款周转率(TTM)_PIT
from windget import getFaApTurnTtM


# 获取应付账款及应付票据周转率时间序列
from windget import getFaApNpTurnSeries


# 获取应付账款及应付票据周转率
from windget import getFaApNpTurn


# 获取现金周转率时间序列
from windget import getFaCashTurnRatioSeries


# 获取现金周转率
from windget import getFaCashTurnRatio


# 获取净利润(同比增长率)时间序列
from windget import getYoYProfitSeries


# 获取净利润(同比增长率)
from windget import getYoYProfit


# 获取净资产(同比增长率)时间序列
from windget import getYoYEquitySeries


# 获取净资产(同比增长率)
from windget import getYoYEquity


# 获取总负债(同比增长率)时间序列
from windget import getYoYDebtSeries


# 获取总负债(同比增长率)
from windget import getYoYDebt


# 获取总资产(同比增长率)时间序列
from windget import getYoYAssetsSeries


# 获取总资产(同比增长率)
from windget import getYoYAssets


# 获取营业收入(同比增长率)时间序列
from windget import getYoYOrSeries


# 获取营业收入(同比增长率)
from windget import getYoYOr


# 获取营业利润(同比增长率)时间序列
from windget import getYoyoPSeries


# 获取营业利润(同比增长率)
from windget import getYoyoP


# 获取营业利润(同比增长率)2时间序列
from windget import getYoyoP2Series


# 获取营业利润(同比增长率)2
from windget import getYoyoP2


# 获取利润总额(同比增长率)时间序列
from windget import getYOyEBTSeries


# 获取利润总额(同比增长率)
from windget import getYOyEBT


# 获取营业收入(同比增长率)_GSD时间序列
from windget import getWgsDYoYOrSeries


# 获取营业收入(同比增长率)_GSD
from windget import getWgsDYoYOr


# 获取营业利润(同比增长率)_GSD时间序列
from windget import getWgsDYoyoP2Series


# 获取营业利润(同比增长率)_GSD
from windget import getWgsDYoyoP2


# 获取利润总额(同比增长率)_GSD时间序列
from windget import getWgsDYOyEBTSeries


# 获取利润总额(同比增长率)_GSD
from windget import getWgsDYOyEBT


# 获取营业总收入(同比增长率)时间序列
from windget import getYoYTrSeries


# 获取营业总收入(同比增长率)
from windget import getYoYTr


# 获取现金净流量(同比增长率)时间序列
from windget import getYoYCfSeries


# 获取现金净流量(同比增长率)
from windget import getYoYCf


# 获取营业总收入(同比增长率)_GSD时间序列
from windget import getWgsDYoYTrSeries


# 获取营业总收入(同比增长率)_GSD
from windget import getWgsDYoYTr


# 获取基本每股收益(同比增长率)时间序列
from windget import getYoYepsBasicSeries


# 获取基本每股收益(同比增长率)
from windget import getYoYepsBasic


# 获取稀释每股收益(同比增长率)时间序列
from windget import getYoYepsDilutedSeries


# 获取稀释每股收益(同比增长率)
from windget import getYoYepsDiluted


# 获取单季度.净利润同比增长率时间序列
from windget import getQfaYoYProfitSeries


# 获取单季度.净利润同比增长率
from windget import getQfaYoYProfit


# 获取基本每股收益(同比增长率)_GSD时间序列
from windget import getWgsDYoYepsBasicSeries


# 获取基本每股收益(同比增长率)_GSD
from windget import getWgsDYoYepsBasic


# 获取稀释每股收益(同比增长率)_GSD时间序列
from windget import getWgsDYoYepsDilutedSeries


# 获取稀释每股收益(同比增长率)_GSD
from windget import getWgsDYoYepsDiluted


# 获取单季度.营业收入同比增长率时间序列
from windget import getQfaYoYSalesSeries


# 获取单季度.营业收入同比增长率
from windget import getQfaYoYSales


# 获取单季度.营业利润同比增长率时间序列
from windget import getQfaYoyoPSeries


# 获取单季度.营业利润同比增长率
from windget import getQfaYoyoP


# 获取单季度.营业总收入同比增长率时间序列
from windget import getQfaYoYGrSeries


# 获取单季度.营业总收入同比增长率
from windget import getQfaYoYGr


# 获取单季度.每股收益(同比增长率)时间序列
from windget import getQfaYoYepsSeries


# 获取单季度.每股收益(同比增长率)
from windget import getQfaYoYeps


# 获取单季度.现金净流量(同比增长率)时间序列
from windget import getQfaYoYCfSeries


# 获取单季度.现金净流量(同比增长率)
from windget import getQfaYoYCf


# 获取净资产收益率(摊薄)(同比增长率)时间序列
from windget import getYoYRoeSeries


# 获取净资产收益率(摊薄)(同比增长率)
from windget import getYoYRoe


# 获取净资产收益率(摊薄)(同比增长率)_GSD时间序列
from windget import getWgsDYoYRoeSeries


# 获取净资产收益率(摊薄)(同比增长率)_GSD
from windget import getWgsDYoYRoe


# 获取归属母公司股东的净利润(同比增长率)时间序列
from windget import getYoYNetProfitSeries


# 获取归属母公司股东的净利润(同比增长率)
from windget import getYoYNetProfit


# 获取归属母公司股东的净利润(同比增长率)_GSD时间序列
from windget import getWgsDYoYNetProfitSeries


# 获取归属母公司股东的净利润(同比增长率)_GSD
from windget import getWgsDYoYNetProfit


# 获取单季度.经营性现金净流量(同比增长率)时间序列
from windget import getQfaYoyOCFSeries


# 获取单季度.经营性现金净流量(同比增长率)
from windget import getQfaYoyOCF


# 获取单季度.归属母公司股东的净利润同比增长率时间序列
from windget import getQfaYoYNetProfitSeries


# 获取单季度.归属母公司股东的净利润同比增长率
from windget import getQfaYoYNetProfit


# 获取归属母公司股东的净利润-扣除非经常损益(同比增长率)时间序列
from windget import getYoYNetProfitDeductedSeries


# 获取归属母公司股东的净利润-扣除非经常损益(同比增长率)
from windget import getYoYNetProfitDeducted


# 获取归属母公司股东的净利润-扣除非经常损益(同比增长率)_GSD时间序列
from windget import getWgsDYoYNetProfitDeductedSeries


# 获取归属母公司股东的净利润-扣除非经常损益(同比增长率)_GSD
from windget import getWgsDYoYNetProfitDeducted


# 获取资产总计(相对年初增长率)时间序列
from windget import getYoYAssetsSeries


# 获取资产总计(相对年初增长率)
from windget import getYoYAssets


# 获取资产总计(相对年初增长率)_GSD时间序列
from windget import getWgsDYoYAssetsSeries


# 获取资产总计(相对年初增长率)_GSD
from windget import getWgsDYoYAssets


# 获取每股净资产(相对年初增长率)时间序列
from windget import getYoYbPsSeries


# 获取每股净资产(相对年初增长率)
from windget import getYoYbPs


# 获取每股净资产(相对年初增长率)_GSD时间序列
from windget import getWgsDYoYbPsSeries


# 获取每股净资产(相对年初增长率)_GSD
from windget import getWgsDYoYbPs


# 获取归属母公司股东的权益(相对年初增长率)时间序列
from windget import getYoYEquitySeries


# 获取归属母公司股东的权益(相对年初增长率)
from windget import getYoYEquity


# 获取归属母公司股东的权益(相对年初增长率)_GSD时间序列
from windget import getWgsDYoYEquitySeries


# 获取归属母公司股东的权益(相对年初增长率)_GSD
from windget import getWgsDYoYEquity


# 获取归属母公司股东的净利润/净利润时间序列
from windget import getDupontNpSeries


# 获取归属母公司股东的净利润/净利润
from windget import getDupontNp


# 获取归属母公司股东的净利润/净利润_GSD时间序列
from windget import getWgsDDupontNpSeries


# 获取归属母公司股东的净利润/净利润_GSD
from windget import getWgsDDupontNp


# 获取净利润/利润总额时间序列
from windget import getDupontTaxBurdenSeries


# 获取净利润/利润总额
from windget import getDupontTaxBurden


# 获取净利润/利润总额_GSD时间序列
from windget import getWgsDDupontTaxBurdenSeries


# 获取净利润/利润总额_GSD
from windget import getWgsDDupontTaxBurden


# 获取利润总额/息税前利润时间序列
from windget import getDupontIntBurdenSeries


# 获取利润总额/息税前利润
from windget import getDupontIntBurden


# 获取利润总额/息税前利润_GSD时间序列
from windget import getWgsDDupontIntBurdenSeries


# 获取利润总额/息税前利润_GSD
from windget import getWgsDDupontIntBurden


# 获取营运资本/总资产时间序列
from windget import getWorkingCapitalToAssetsSeries


# 获取营运资本/总资产
from windget import getWorkingCapitalToAssets


# 获取留存收益/总资产时间序列
from windget import getRetainedEarningsToAssetsSeries


# 获取留存收益/总资产
from windget import getRetainedEarningsToAssets


# 获取股东权益合计(含少数)/负债总计时间序列
from windget import getBookValueToDebtSeries


# 获取股东权益合计(含少数)/负债总计
from windget import getBookValueToDebt


# 获取营业收入/总资产时间序列
from windget import getRevenueToAssetsSeries


# 获取营业收入/总资产
from windget import getRevenueToAssets


# 获取逾期贷款_3个月以内时间序列
from windget import getStmNoteBank0001Series


# 获取逾期贷款_3个月以内
from windget import getStmNoteBank0001


# 获取逾期贷款_3个月至1年时间序列
from windget import getStmNoteBank0002Series


# 获取逾期贷款_3个月至1年
from windget import getStmNoteBank0002


# 获取逾期贷款_1年以上3年以内时间序列
from windget import getStmNoteBank0003Series


# 获取逾期贷款_1年以上3年以内
from windget import getStmNoteBank0003


# 获取逾期贷款_3年以上时间序列
from windget import getStmNoteBank0004Series


# 获取逾期贷款_3年以上
from windget import getStmNoteBank0004


# 获取逾期贷款合计时间序列
from windget import getStmNoteBank0005Series


# 获取逾期贷款合计
from windget import getStmNoteBank0005


# 获取主营业务收入时间序列
from windget import getStmNoteSeg1701Series


# 获取主营业务收入
from windget import getStmNoteSeg1701


# 获取主营业务成本时间序列
from windget import getStmNoteSeg1702Series


# 获取主营业务成本
from windget import getStmNoteSeg1702


# 获取资产管理业务收入时间序列
from windget import getStmNoteSec1543Series


# 获取资产管理业务收入
from windget import getStmNoteSec1543


# 获取资产管理业务净收入时间序列
from windget import getStmNoteSec1553Series


# 获取资产管理业务净收入
from windget import getStmNoteSec1553


# 获取资产管理费收入_GSD时间序列
from windget import getWgsDAumIncSeries


# 获取资产管理费收入_GSD
from windget import getWgsDAumInc


# 获取定向资产管理业务收入时间序列
from windget import getStmNoteAssetManageIncDSeries


# 获取定向资产管理业务收入
from windget import getStmNoteAssetManageIncD


# 获取集合资产管理业务收入时间序列
from windget import getStmNoteAssetManageIncCSeries


# 获取集合资产管理业务收入
from windget import getStmNoteAssetManageIncC


# 获取专项资产管理业务收入时间序列
from windget import getStmNoteAssetManageIncSSeries


# 获取专项资产管理业务收入
from windget import getStmNoteAssetManageIncS


# 获取单季度.资产管理费收入_GSD时间序列
from windget import getWgsDQfaAumIncSeries


# 获取单季度.资产管理费收入_GSD
from windget import getWgsDQfaAumInc


# 获取受托客户资产管理业务净收入时间序列
from windget import getNetIncCustomerAssetManagementBusinessSeries


# 获取受托客户资产管理业务净收入
from windget import getNetIncCustomerAssetManagementBusiness


# 获取单季度.受托客户资产管理业务净收入时间序列
from windget import getQfaNetIncCustomerAssetManagementBusinessSeries


# 获取单季度.受托客户资产管理业务净收入
from windget import getQfaNetIncCustomerAssetManagementBusiness


# 获取手续费及佣金收入:受托客户资产管理业务时间序列
from windget import getStmNoteSec1502Series


# 获取手续费及佣金收入:受托客户资产管理业务
from windget import getStmNoteSec1502


# 获取手续费及佣金净收入:受托客户资产管理业务时间序列
from windget import getStmNoteSec1522Series


# 获取手续费及佣金净收入:受托客户资产管理业务
from windget import getStmNoteSec1522


# 获取投资收益_FUND时间序列
from windget import getStmIs81Series


# 获取投资收益_FUND
from windget import getStmIs81


# 获取净投资收益率时间序列
from windget import getStmNoteInSur5Series


# 获取净投资收益率
from windget import getStmNoteInSur5


# 获取总投资收益率时间序列
from windget import getStmNoteInSur6Series


# 获取总投资收益率
from windget import getStmNoteInSur6


# 获取净投资收益时间序列
from windget import getStmNoteInvestmentIncome0004Series


# 获取净投资收益
from windget import getStmNoteInvestmentIncome0004


# 获取总投资收益时间序列
from windget import getStmNoteInvestmentIncome0010Series


# 获取总投资收益
from windget import getStmNoteInvestmentIncome0010


# 获取其他投资收益时间序列
from windget import getStmNoteInvestmentIncome0009Series


# 获取其他投资收益
from windget import getStmNoteInvestmentIncome0009


# 获取取得投资收益收到的现金时间序列
from windget import getCashRecpReturnInvestSeries


# 获取取得投资收益收到的现金
from windget import getCashRecpReturnInvest


# 获取股票投资收益_FUND时间序列
from windget import getStmIs1Series


# 获取股票投资收益_FUND
from windget import getStmIs1


# 获取基金投资收益_FUND时间序列
from windget import getStmIs75Series


# 获取基金投资收益_FUND
from windget import getStmIs75


# 获取债券投资收益_FUND时间序列
from windget import getStmIs2Series


# 获取债券投资收益_FUND
from windget import getStmIs2


# 获取权证投资收益_FUND时间序列
from windget import getStmIs201Series


# 获取权证投资收益_FUND
from windget import getStmIs201


# 获取单季度.取得投资收益收到的现金时间序列
from windget import getQfaCashRecpReturnInvestSeries


# 获取单季度.取得投资收益收到的现金
from windget import getQfaCashRecpReturnInvest


# 获取资产支持证券投资收益_FUND时间序列
from windget import getStmIs71Series


# 获取资产支持证券投资收益_FUND
from windget import getStmIs71


# 获取对联营企业和合营企业的投资收益时间序列
from windget import getIncInvestAsSocJVENtpSeries


# 获取对联营企业和合营企业的投资收益
from windget import getIncInvestAsSocJVENtp


# 获取单季度.对联营企业和合营企业的投资收益时间序列
from windget import getQfaIncInvestAsSocJVENtpSeries


# 获取单季度.对联营企业和合营企业的投资收益
from windget import getQfaIncInvestAsSocJVENtp


# 获取单季度.扣除非经常损益后的净利润时间序列
from windget import getQfaDeductedProfitSeries


# 获取单季度.扣除非经常损益后的净利润
from windget import getQfaDeductedProfit


# 获取单季度.经营活动净收益时间序列
from windget import getQfaOperateIncomeSeries


# 获取单季度.经营活动净收益
from windget import getQfaOperateIncome


# 获取单季度.价值变动净收益时间序列
from windget import getQfaInvestIncomeSeries


# 获取单季度.价值变动净收益
from windget import getQfaInvestIncome


# 获取单季度.净资产收益率(扣除非经常损益)时间序列
from windget import getQfaRoeDeductedSeries


# 获取单季度.净资产收益率(扣除非经常损益)
from windget import getQfaRoeDeducted


# 获取单季度.营业总收入环比增长率时间序列
from windget import getQfaCGrGrSeries


# 获取单季度.营业总收入环比增长率
from windget import getQfaCGrGr


# 获取单季度.营业收入环比增长率时间序列
from windget import getQfaCGrSalesSeries


# 获取单季度.营业收入环比增长率
from windget import getQfaCGrSales


# 获取单季度.营业利润环比增长率时间序列
from windget import getQfaCGroPSeries


# 获取单季度.营业利润环比增长率
from windget import getQfaCGroP


# 获取单季度.净利润环比增长率时间序列
from windget import getQfaCGrProfitSeries


# 获取单季度.净利润环比增长率
from windget import getQfaCGrProfit


# 获取单季度.归属母公司股东的净利润环比增长率时间序列
from windget import getQfaCGrNetProfitSeries


# 获取单季度.归属母公司股东的净利润环比增长率
from windget import getQfaCGrNetProfit


# 获取人均创收时间序列
from windget import getWgsDRevenuePpSeries


# 获取人均创收
from windget import getWgsDRevenuePp


# 获取人均创利时间序列
from windget import getWgsDProfitPpSeries


# 获取人均创利
from windget import getWgsDProfitPp


# 获取人均薪酬时间序列
from windget import getWgsDSalaryPpSeries


# 获取人均薪酬
from windget import getWgsDSalaryPp


# 获取增长率-营业收入(TTM)_PIT时间序列
from windget import getFaOrGrTtMSeries


# 获取增长率-营业收入(TTM)_PIT
from windget import getFaOrGrTtM


# 获取增长率-利润总额(TTM)_PIT时间序列
from windget import getFaTpGrTtMSeries


# 获取增长率-利润总额(TTM)_PIT
from windget import getFaTpGrTtM


# 获取增长率-营业利润(TTM)_PIT时间序列
from windget import getFaOiGrTtMSeries


# 获取增长率-营业利润(TTM)_PIT
from windget import getFaOiGrTtM


# 获取增长率-净利润(TTM)_PIT时间序列
from windget import getFaNpGrTtMSeries


# 获取增长率-净利润(TTM)_PIT
from windget import getFaNpGrTtM


# 获取增长率-归属母公司股东的净利润(TTM)_PIT时间序列
from windget import getFaNppCGrTtMSeries


# 获取增长率-归属母公司股东的净利润(TTM)_PIT
from windget import getFaNppCGrTtM


# 获取增长率-毛利率(TTM)_PIT时间序列
from windget import getFaGpmgRTtMSeries


# 获取增长率-毛利率(TTM)_PIT
from windget import getFaGpmgRTtM


# 获取增长率-总资产_PIT时间序列
from windget import getFaTagRSeries


# 获取增长率-总资产_PIT
from windget import getFaTagR


# 获取增长率-净资产_PIT时间序列
from windget import getFaNAgrSeries


# 获取增长率-净资产_PIT
from windget import getFaNAgr


# 获取5年收益增长率_PIT时间序列
from windget import getFaEGroSeries


# 获取5年收益增长率_PIT
from windget import getFaEGro


# 获取基金N日净值增长率时间序列
from windget import getNavReturnNdSeries


# 获取基金N日净值增长率
from windget import getNavReturnNd


# 获取净利润复合年增长率时间序列
from windget import getGrowthCAgrNetProfitSeries


# 获取净利润复合年增长率
from windget import getGrowthCAgrNetProfit


# 获取毛利(近1年增长率)_GSD时间序列
from windget import getWgsDGrowthGp1YSeries


# 获取毛利(近1年增长率)_GSD
from windget import getWgsDGrowthGp1Y


# 获取毛利(近3年增长率)_GSD时间序列
from windget import getWgsDGrowthGp3YSeries


# 获取毛利(近3年增长率)_GSD
from windget import getWgsDGrowthGp3Y


# 获取净利润复合年增长率_GSD时间序列
from windget import getWgsDCAgrNetProfitSeries


# 获取净利润复合年增长率_GSD
from windget import getWgsDCAgrNetProfit


# 获取5年营业收入增长率_PIT时间序列
from windget import getFaSGroSeries


# 获取5年营业收入增长率_PIT
from windget import getFaSGro


# 获取利润总额复合年增长率时间序列
from windget import getCAgrTotalProfitSeries


# 获取利润总额复合年增长率
from windget import getCAgrTotalProfit


# 获取净利润(N年,增长率)时间序列
from windget import getGrowthProfitSeries


# 获取净利润(N年,增长率)
from windget import getGrowthProfit


# 获取净利润(近1年增长率)_GSD时间序列
from windget import getWgsDGrowthNp1YSeries


# 获取净利润(近1年增长率)_GSD
from windget import getWgsDGrowthNp1Y


# 获取净利润(近3年增长率)_GSD时间序列
from windget import getWgsDGrowthNp3YSeries


# 获取净利润(近3年增长率)_GSD
from windget import getWgsDGrowthNp3Y


# 获取总资产(近1年增长率)_GSD时间序列
from windget import getWgsDGrowthAsset1YSeries


# 获取总资产(近1年增长率)_GSD
from windget import getWgsDGrowthAsset1Y


# 获取总资产(近3年增长率)_GSD时间序列
from windget import getWgsDGrowthAsset3YSeries


# 获取总资产(近3年增长率)_GSD
from windget import getWgsDGrowthAsset3Y


# 获取总负债(近1年增长率)_GSD时间序列
from windget import getWgsDGrowthDebt1YSeries


# 获取总负债(近1年增长率)_GSD
from windget import getWgsDGrowthDebt1Y


# 获取总负债(近3年增长率)_GSD时间序列
from windget import getWgsDGrowthDebt3YSeries


# 获取总负债(近3年增长率)_GSD
from windget import getWgsDGrowthDebt3Y


# 获取利润总额复合年增长率_GSD时间序列
from windget import getWgsDCAgrTotalProfitSeries


# 获取利润总额复合年增长率_GSD
from windget import getWgsDCAgrTotalProfit


# 获取近三年营收复合增长率时间序列
from windget import getIpoRevenueGrowthSeries


# 获取近三年营收复合增长率
from windget import getIpoRevenueGrowth


# 获取营业总收入复合年增长率时间序列
from windget import getGrowthCAgrTrSeries


# 获取营业总收入复合年增长率
from windget import getGrowthCAgrTr


# 获取营业收入(N年,增长率)时间序列
from windget import getGrowthOrSeries


# 获取营业收入(N年,增长率)
from windget import getGrowthOr


# 获取营业利润(N年,增长率)时间序列
from windget import getGrowthOpSeries


# 获取营业利润(N年,增长率)
from windget import getGrowthOp


# 获取利润总额(N年,增长率)时间序列
from windget import getGrowthEBtSeries


# 获取利润总额(N年,增长率)
from windget import getGrowthEBt


# 获取资产总计(N年,增长率)时间序列
from windget import getGrowthAssetsSeries


# 获取资产总计(N年,增长率)
from windget import getGrowthAssets


# 获取股东权益(N年,增长率)时间序列
from windget import getGrowthTotalEquitySeries


# 获取股东权益(N年,增长率)
from windget import getGrowthTotalEquity


# 获取营业利润(近1年增长率)_GSD时间序列
from windget import getWgsDGrowthOp1YSeries


# 获取营业利润(近1年增长率)_GSD
from windget import getWgsDGrowthOp1Y


# 获取营业利润(近3年增长率)_GSD时间序列
from windget import getWgsDGrowthOp3YSeries


# 获取营业利润(近3年增长率)_GSD
from windget import getWgsDGrowthOp3Y


# 获取税前利润(近1年增长率)_GSD时间序列
from windget import getWgsDGrowthEBt1YSeries


# 获取税前利润(近1年增长率)_GSD
from windget import getWgsDGrowthEBt1Y


# 获取税前利润(近3年增长率)_GSD时间序列
from windget import getWgsDGrowthEBt3YSeries


# 获取税前利润(近3年增长率)_GSD
from windget import getWgsDGrowthEBt3Y


# 获取营业总收入复合年增长率_GSD时间序列
from windget import getWgsDCAgrTrSeries


# 获取营业总收入复合年增长率_GSD
from windget import getWgsDCAgrTr


# 获取营业收入(N年,增长率)_GSD时间序列
from windget import getWgsDGrowthOrSeries


# 获取营业收入(N年,增长率)_GSD
from windget import getWgsDGrowthOr


# 获取营业利润(N年,增长率)_GSD时间序列
from windget import getWgsDGrowthOpSeries


# 获取营业利润(N年,增长率)_GSD
from windget import getWgsDGrowthOp


# 获取利润总额(N年,增长率)_GSD时间序列
from windget import getWgsDGrowthEBtSeries


# 获取利润总额(N年,增长率)_GSD
from windget import getWgsDGrowthEBt


# 获取资产总计(N年,增长率)_GSD时间序列
from windget import getWgsDGrowthAssetsSeries


# 获取资产总计(N年,增长率)_GSD
from windget import getWgsDGrowthAssets


# 获取股东权益(N年,增长率)_GSD时间序列
from windget import getWgsDGrowthTotalEquitySeries


# 获取股东权益(N年,增长率)_GSD
from windget import getWgsDGrowthTotalEquity


# 获取营业总收入(N年,增长率)时间序列
from windget import getGrowthGrSeries


# 获取营业总收入(N年,增长率)
from windget import getGrowthGr


# 获取营业总成本(N年,增长率)时间序列
from windget import getGrowthGcSeries


# 获取营业总成本(N年,增长率)
from windget import getGrowthGc


# 获取销售利润率(N年,增长率)时间序列
from windget import getGrowthProfitToSalesSeries


# 获取销售利润率(N年,增长率)
from windget import getGrowthProfitToSales


# 获取总营业收入(近1年增长率)_GSD时间序列
from windget import getWgsDGrowthSales1YSeries


# 获取总营业收入(近1年增长率)_GSD
from windget import getWgsDGrowthSales1Y


# 获取总营业收入(近3年增长率)_GSD时间序列
from windget import getWgsDGrowthSales3YSeries


# 获取总营业收入(近3年增长率)_GSD
from windget import getWgsDGrowthSales3Y


# 获取每股净资产(近1年增长率)_GSD时间序列
from windget import getWgsDGrowthBpS1YSeries


# 获取每股净资产(近1年增长率)_GSD
from windget import getWgsDGrowthBpS1Y


# 获取每股净资产(近3年增长率)_GSD时间序列
from windget import getWgsDGrowthBpS3YSeries


# 获取每股净资产(近3年增长率)_GSD
from windget import getWgsDGrowthBpS3Y


# 获取营业总收入(N年,增长率)_GSD时间序列
from windget import getWgsDGrowthGrSeries


# 获取营业总收入(N年,增长率)_GSD
from windget import getWgsDGrowthGr


# 获取营业总成本(N年,增长率)_GSD时间序列
from windget import getWgsDGrowthGcSeries


# 获取营业总成本(N年,增长率)_GSD
from windget import getWgsDGrowthGc


# 获取销售利润率(N年,增长率)_GSD时间序列
from windget import getWgsDGrowthProfitToSalesSeries


# 获取销售利润率(N年,增长率)_GSD
from windget import getWgsDGrowthProfitToSales


# 获取净资产收益率(N年,增长率)时间序列
from windget import getGrowthRoeSeries


# 获取净资产收益率(N年,增长率)
from windget import getGrowthRoe


# 获取股东权益合计(近1年增长率)_GSD时间序列
from windget import getWgsDGrowthTotalEquity1YSeries


# 获取股东权益合计(近1年增长率)_GSD
from windget import getWgsDGrowthTotalEquity1Y


# 获取股东权益合计(近3年增长率)_GSD时间序列
from windget import getWgsDGrowthTotalEquity3YSeries


# 获取股东权益合计(近3年增长率)_GSD
from windget import getWgsDGrowthTotalEquity3Y


# 获取基本每股收益(近1年增长率)_GSD时间序列
from windget import getWgsDGrowthEps1YSeries


# 获取基本每股收益(近1年增长率)_GSD
from windget import getWgsDGrowthEps1Y


# 获取基本每股收益(近3年增长率)_GSD时间序列
from windget import getWgsDGrowthEps3YSeries


# 获取基本每股收益(近3年增长率)_GSD
from windget import getWgsDGrowthEps3Y


# 获取净资产收益率(N年,增长率)_GSD时间序列
from windget import getWgsDGrowthRoeSeries


# 获取净资产收益率(N年,增长率)_GSD
from windget import getWgsDGrowthRoe


# 获取经营活动净收益(N年,增长率)时间序列
from windget import getGrowthOperateIncomeSeries


# 获取经营活动净收益(N年,增长率)
from windget import getGrowthOperateIncome


# 获取价值变动净收益(N年,增长率)时间序列
from windget import getGrowthInvestIncomeSeries


# 获取价值变动净收益(N年,增长率)
from windget import getGrowthInvestIncome


# 获取经营活动净收益(N年,增长率)_GSD时间序列
from windget import getWgsDGrowthOperateIncomeSeries


# 获取经营活动净收益(N年,增长率)_GSD
from windget import getWgsDGrowthOperateIncome


# 获取价值变动净收益(N年,增长率)_GSD时间序列
from windget import getWgsDGrowthInvestIncomeSeries


# 获取价值变动净收益(N年,增长率)_GSD
from windget import getWgsDGrowthInvestIncome


# 获取归属母公司股东的权益(N年,增长率)时间序列
from windget import getGrowthEquitySeries


# 获取归属母公司股东的权益(N年,增长率)
from windget import getGrowthEquity


# 获取归属母公司股东的权益(近1年增长率)_GSD时间序列
from windget import getWgsDGrowthEquity1YSeries


# 获取归属母公司股东的权益(近1年增长率)_GSD
from windget import getWgsDGrowthEquity1Y


# 获取归属母公司股东的权益(近3年增长率)_GSD时间序列
from windget import getWgsDGrowthEquity3YSeries


# 获取归属母公司股东的权益(近3年增长率)_GSD
from windget import getWgsDGrowthEquity3Y


# 获取归属母公司股东的权益(N年,增长率)_GSD时间序列
from windget import getWgsDGrowthEquitySeries


# 获取归属母公司股东的权益(N年,增长率)_GSD
from windget import getWgsDGrowthEquity


# 获取归属母公司股东的净利润(N年,增长率)时间序列
from windget import getGrowthNetProfitSeries


# 获取归属母公司股东的净利润(N年,增长率)
from windget import getGrowthNetProfit


# 获取归属母公司股东的净利润(N年,增长率)_GSD时间序列
from windget import getWgsDGrowthNetProfitSeries


# 获取归属母公司股东的净利润(N年,增长率)_GSD
from windget import getWgsDGrowthNetProfit


# 获取归属母公司股东的净利润-扣除非经常损益(N年,增长率)时间序列
from windget import getGrowthNetProfitDeductedSeries


# 获取归属母公司股东的净利润-扣除非经常损益(N年,增长率)
from windget import getGrowthNetProfitDeducted


# 获取资产差额(特殊报表科目)时间序列
from windget import getAssetsGapSeries


# 获取资产差额(特殊报表科目)
from windget import getAssetsGap


# 获取资产差额说明(特殊报表科目)时间序列
from windget import getAssetsGapDetailSeries


# 获取资产差额说明(特殊报表科目)
from windget import getAssetsGapDetail


# 获取资产差额(合计平衡项目)时间序列
from windget import getAssetsNettingSeries


# 获取资产差额(合计平衡项目)
from windget import getAssetsNetting


# 获取资产总计时间序列
from windget import getStm07BsReItsAllAssetsSeries


# 获取资产总计
from windget import getStm07BsReItsAllAssets


# 获取资产处置收益时间序列
from windget import getGainAssetDispositionsSeries


# 获取资产处置收益
from windget import getGainAssetDispositions


# 获取资产支持证券投资_FUND时间序列
from windget import getStmBs72Series


# 获取资产支持证券投资_FUND
from windget import getStmBs72


# 获取资产合计_FUND时间序列
from windget import getStmBs19Series


# 获取资产合计_FUND
from windget import getStmBs19


# 获取资产支持证券利息收入_FUND时间序列
from windget import getStmIs69Series


# 获取资产支持证券利息收入_FUND
from windget import getStmIs69


# 获取资产支持证券投资公允价值变动收益_FUND时间序列
from windget import getStmIs105Series


# 获取资产支持证券投资公允价值变动收益_FUND
from windget import getStmIs105


# 获取资产回报率(TTM)_PIT时间序列
from windget import getFaRoaTtMSeries


# 获取资产回报率(TTM)_PIT
from windget import getFaRoaTtM


# 获取资产总计_PIT时间序列
from windget import getFaToTAssetsSeries


# 获取资产总计_PIT
from windget import getFaToTAssets


# 获取资产总计(MRQ,只有最新数据)时间序列
from windget import getAssetMrQSeries


# 获取资产总计(MRQ,只有最新数据)
from windget import getAssetMrQ


# 获取净资产收益率ROE(平均)时间序列
from windget import getRoeAvgSeries


# 获取净资产收益率ROE(平均)
from windget import getRoeAvg


# 获取净资产收益率ROE(加权)时间序列
from windget import getRoeBasicSeries


# 获取净资产收益率ROE(加权)
from windget import getRoeBasic


# 获取净资产收益率ROE(摊薄)时间序列
from windget import getRoeDilutedSeries


# 获取净资产收益率ROE(摊薄)
from windget import getRoeDiluted


# 获取净资产收益率ROE(扣除/平均)时间序列
from windget import getRoeDeductedSeries


# 获取净资产收益率ROE(扣除/平均)
from windget import getRoeDeducted


# 获取净资产收益率ROE(扣除/加权)时间序列
from windget import getRoeExBasicSeries


# 获取净资产收益率ROE(扣除/加权)
from windget import getRoeExBasic


# 获取净资产收益率ROE(扣除/摊薄)时间序列
from windget import getRoeExDilutedSeries


# 获取净资产收益率ROE(扣除/摊薄)
from windget import getRoeExDiluted


# 获取净资产收益率ROE-增发条件时间序列
from windget import getRoeAddSeries


# 获取净资产收益率ROE-增发条件
from windget import getRoeAdd


# 获取总资产报酬率ROA时间序列
from windget import getRoa2Series


# 获取总资产报酬率ROA
from windget import getRoa2


# 获取总资产净利率ROA时间序列
from windget import getRoaSeries


# 获取总资产净利率ROA
from windget import getRoa


# 获取净资产收益率ROE时间序列
from windget import getRoeSeries


# 获取净资产收益率ROE
from windget import getRoe


# 获取净资产收益率(TTM)时间序列
from windget import getRoeTtM2Series


# 获取净资产收益率(TTM)
from windget import getRoeTtM2


# 获取净资产收益率(TTM,平均)时间序列
from windget import getFaRoeTtMAvgSeries


# 获取净资产收益率(TTM,平均)
from windget import getFaRoeTtMAvg


# 获取总资产报酬率(TTM)时间序列
from windget import getRoa2TtM2Series


# 获取总资产报酬率(TTM)
from windget import getRoa2TtM2


# 获取总资产净利率-不含少数股东损益(TTM)时间序列
from windget import getNetProfitToAssetsSeries


# 获取总资产净利率-不含少数股东损益(TTM)
from windget import getNetProfitToAssets


# 获取净资产收益率_GSD时间序列
from windget import getWgsDRoeSeries


# 获取净资产收益率_GSD
from windget import getWgsDRoe


# 获取净资产收益率ROE(摊薄)_GSD时间序列
from windget import getWgsDRoeDilutedSeries


# 获取净资产收益率ROE(摊薄)_GSD
from windget import getWgsDRoeDiluted


# 获取净资产收益率(扣除)_GSD时间序列
from windget import getWgsDRoeDeductedSeries


# 获取净资产收益率(扣除)_GSD
from windget import getWgsDRoeDeducted


# 获取净资产收益率ROE(扣除/摊薄)_GSD时间序列
from windget import getWgsDRoeExDilutedSeries


# 获取净资产收益率ROE(扣除/摊薄)_GSD
from windget import getWgsDRoeExDiluted


# 获取净资产收益率(年化)_GSD时间序列
from windget import getWgsDRoeYearlySeries


# 获取净资产收益率(年化)_GSD
from windget import getWgsDRoeYearly


# 获取总资产净利率_GSD时间序列
from windget import getWgsDRoaSeries


# 获取总资产净利率_GSD
from windget import getWgsDRoa


# 获取总资产净利率(年化)_GSD时间序列
from windget import getWgsDRoaYearlySeries


# 获取总资产净利率(年化)_GSD
from windget import getWgsDRoaYearly


# 获取总资产报酬率ROA_GSD时间序列
from windget import getWgsDRoa2Series


# 获取总资产报酬率ROA_GSD
from windget import getWgsDRoa2


# 获取总资产报酬率(年化)_GSD时间序列
from windget import getWgsDRoa2YearlySeries


# 获取总资产报酬率(年化)_GSD
from windget import getWgsDRoa2Yearly


# 获取净资产收益率(TTM)_GSD时间序列
from windget import getRoeTtM3Series


# 获取净资产收益率(TTM)_GSD
from windget import getRoeTtM3


# 获取总资产净利率(TTM)_GSD时间序列
from windget import getRoaTtM2Series


# 获取总资产净利率(TTM)_GSD
from windget import getRoaTtM2


# 获取总资产净利率-不含少数股东损益(TTM)_GSD时间序列
from windget import getNetProfitToAssets2Series


# 获取总资产净利率-不含少数股东损益(TTM)_GSD
from windget import getNetProfitToAssets2


# 获取总资产报酬率(TTM)_GSD时间序列
from windget import getRoa2TtM3Series


# 获取总资产报酬率(TTM)_GSD
from windget import getRoa2TtM3


# 获取总资产_GSD时间序列
from windget import getWgsDAssetsSeries


# 获取总资产_GSD
from windget import getWgsDAssets


# 获取净资产收益率(平均)_PIT时间序列
from windget import getFaRoeAvgSeries


# 获取净资产收益率(平均)_PIT
from windget import getFaRoeAvg


# 获取净资产收益率(加权)_PIT时间序列
from windget import getFaRoeWGtSeries


# 获取净资产收益率(加权)_PIT
from windget import getFaRoeWGt


# 获取净资产收益率(摊薄)_PIT时间序列
from windget import getFaRoeDilutedSeries


# 获取净资产收益率(摊薄)_PIT
from windget import getFaRoeDiluted


# 获取净资产收益率(扣除/加权)_PIT时间序列
from windget import getFaRoeExBasicSeries


# 获取净资产收益率(扣除/加权)_PIT
from windget import getFaRoeExBasic


# 获取净资产收益率(扣除/摊薄)_PIT时间序列
from windget import getFaRoeExDilutedSeries


# 获取净资产收益率(扣除/摊薄)_PIT
from windget import getFaRoeExDiluted


# 获取净资产收益率(TTM)_PIT时间序列
from windget import getFaRoeNpTtMSeries


# 获取净资产收益率(TTM)_PIT
from windget import getFaRoeNpTtM


# 获取总资产报酬率(TTM)_PIT时间序列
from windget import getFaRoaEbItTtMSeries


# 获取总资产报酬率(TTM)_PIT
from windget import getFaRoaEbItTtM


# 获取总资产净利率-不含少数股东损益(TTM)_PIT时间序列
from windget import getFaNetProfitToAssetsTtMSeries


# 获取总资产净利率-不含少数股东损益(TTM)_PIT
from windget import getFaNetProfitToAssetsTtM


# 获取净资产周转率(TTM)_PIT时间序列
from windget import getFaNaTurnTtMSeries


# 获取净资产周转率(TTM)_PIT
from windget import getFaNaTurnTtM


# 获取净资产收益率ROE(TTM,只有最新数据)时间序列
from windget import getRoeTtMSeries


# 获取净资产收益率ROE(TTM,只有最新数据)
from windget import getRoeTtM


# 获取总资产报酬率ROA(TTM,只有最新数据)时间序列
from windget import getRoa2TtMSeries


# 获取总资产报酬率ROA(TTM,只有最新数据)
from windget import getRoa2TtM


# 获取总资产净利率ROA(TTM,只有最新数据)时间序列
from windget import getRoaTtMSeries


# 获取总资产净利率ROA(TTM,只有最新数据)
from windget import getRoaTtM


# 获取固定资产投资扩张率时间序列
from windget import getYoYFixedAssetsSeries


# 获取固定资产投资扩张率
from windget import getYoYFixedAssets


# 获取有形资产时间序列
from windget import getTangibleAssetSeries


# 获取有形资产
from windget import getTangibleAsset


# 获取短期资产流动性比率(人民币)时间序列
from windget import getStAssetLiqRatioRMbNSeries


# 获取短期资产流动性比率(人民币)
from windget import getStAssetLiqRatioRMbN


# 获取短期资产流动性比率(本外币)时间序列
from windget import getStmNoteBankAssetLiqRatioSeries


# 获取短期资产流动性比率(本外币)
from windget import getStmNoteBankAssetLiqRatio


# 获取短期资产流动性比率(外币)时间序列
from windget import getStAssetLiqRatioNormBNSeries


# 获取短期资产流动性比率(外币)
from windget import getStAssetLiqRatioNormBN


# 获取生息资产时间序列
from windget import getStmNoteBank351Series


# 获取生息资产
from windget import getStmNoteBank351


# 获取生息资产收益率时间序列
from windget import getStmNoteBank58Series


# 获取生息资产收益率
from windget import getStmNoteBank58


# 获取生息资产平均余额时间序列
from windget import getStmNoteBank57Series


# 获取生息资产平均余额
from windget import getStmNoteBank57


# 获取短期资产流动性比率(人民币)(旧)时间序列
from windget import getStAssetLiqRatioRMbSeries


# 获取短期资产流动性比率(人民币)(旧)
from windget import getStAssetLiqRatioRMb


# 获取短期资产流动性比率(外币)(旧)时间序列
from windget import getStAssetLiqRatioNormBSeries


# 获取短期资产流动性比率(外币)(旧)
from windget import getStAssetLiqRatioNormB


# 获取其它资产时间序列
from windget import getStmNoteInSur7808Series


# 获取其它资产
from windget import getStmNoteInSur7808


# 获取认可资产时间序列
from windget import getQStmNoteInSur212512Series


# 获取认可资产
from windget import getQStmNoteInSur212512


# 获取有形资产_GSD时间序列
from windget import getWgsDTangibleAsset2Series


# 获取有形资产_GSD
from windget import getWgsDTangibleAsset2


# 获取流动资产合计_GSD时间序列
from windget import getWgsDAssetsCurRSeries


# 获取流动资产合计_GSD
from windget import getWgsDAssetsCurR


# 获取固定资产净值_GSD时间序列
from windget import getWgsDPpeNetSeries


# 获取固定资产净值_GSD
from windget import getWgsDPpeNet


# 获取合同资产时间序列
from windget import getContAssetsSeries


# 获取合同资产
from windget import getContAssets


# 获取流动资产差额(特殊报表科目)时间序列
from windget import getCurAssetsGapSeries


# 获取流动资产差额(特殊报表科目)
from windget import getCurAssetsGap


# 获取流动资产差额说明(特殊报表科目)时间序列
from windget import getCurAssetsGapDetailSeries


# 获取流动资产差额说明(特殊报表科目)
from windget import getCurAssetsGapDetail


# 获取流动资产差额(合计平衡项目)时间序列
from windget import getCurAssetsNettingSeries


# 获取流动资产差额(合计平衡项目)
from windget import getCurAssetsNetting


# 获取流动资产合计时间序列
from windget import getStm07BsReItsLiquidAssetSeries


# 获取流动资产合计
from windget import getStm07BsReItsLiquidAsset


# 获取固定资产(合计)时间序列
from windget import getFixAssetsToTSeries


# 获取固定资产(合计)
from windget import getFixAssetsToT


# 获取固定资产时间序列
from windget import getFixAssetsSeries


# 获取固定资产
from windget import getFixAssets


# 获取固定资产清理时间序列
from windget import getFixAssetsDispSeries


# 获取固定资产清理
from windget import getFixAssetsDisp


# 获取油气资产时间序列
from windget import getOilAndNaturalGasAssetsSeries


# 获取油气资产
from windget import getOilAndNaturalGasAssets


# 获取无形资产时间序列
from windget import getIntangAssetsSeries


# 获取无形资产
from windget import getIntangAssets


# 获取固定资产折旧、油气资产折耗、生产性生物资产折旧时间序列
from windget import getDePrFaCogADpBaSeries


# 获取固定资产折旧、油气资产折耗、生产性生物资产折旧
from windget import getDePrFaCogADpBa


# 获取无形资产摊销时间序列
from windget import getAMortIntangAssetsSeries


# 获取无形资产摊销
from windget import getAMortIntangAssets


# 获取固定资产报废损失时间序列
from windget import getLossSCrFaSeries


# 获取固定资产报废损失
from windget import getLossSCrFa


# 获取固定资产-原值时间序列
from windget import getStmNoteAssetDetail1Series


# 获取固定资产-原值
from windget import getStmNoteAssetDetail1


# 获取固定资产-累计折旧时间序列
from windget import getStmNoteAssetDetail2Series


# 获取固定资产-累计折旧
from windget import getStmNoteAssetDetail2


# 获取固定资产-减值准备时间序列
from windget import getStmNoteAssetDetail3Series


# 获取固定资产-减值准备
from windget import getStmNoteAssetDetail3


# 获取固定资产-净额时间序列
from windget import getStmNoteAssetDetail4Series


# 获取固定资产-净额
from windget import getStmNoteAssetDetail4


# 获取固定资产-净值时间序列
from windget import getStmNoteAvOfASeries


# 获取固定资产-净值
from windget import getStmNoteAvOfA


# 获取油气资产-原值时间序列
from windget import getStmNoteAssetDetail13Series


# 获取油气资产-原值
from windget import getStmNoteAssetDetail13


# 获取油气资产-累计折耗时间序列
from windget import getStmNoteAssetDetail14Series


# 获取油气资产-累计折耗
from windget import getStmNoteAssetDetail14


# 获取油气资产-减值准备时间序列
from windget import getStmNoteAssetDetail15Series


# 获取油气资产-减值准备
from windget import getStmNoteAssetDetail15


# 获取油气资产-净额时间序列
from windget import getStmNoteAssetDetail16Series


# 获取油气资产-净额
from windget import getStmNoteAssetDetail16


# 获取无形资产-原值时间序列
from windget import getStmNoteAssetDetail17Series


# 获取无形资产-原值
from windget import getStmNoteAssetDetail17


# 获取无形资产-累计摊销时间序列
from windget import getStmNoteAssetDetail18Series


# 获取无形资产-累计摊销
from windget import getStmNoteAssetDetail18


# 获取无形资产-减值准备时间序列
from windget import getStmNoteAssetDetail19Series


# 获取无形资产-减值准备
from windget import getStmNoteAssetDetail19


# 获取无形资产-净额时间序列
from windget import getStmNoteAssetDetail20Series


# 获取无形资产-净额
from windget import getStmNoteAssetDetail20


# 获取重仓资产支持证券Wind代码时间序列
from windget import getPrtTopAbsWindCodeSeries


# 获取重仓资产支持证券Wind代码
from windget import getPrtTopAbsWindCode


# 获取流动资产比率_PIT时间序列
from windget import getFaCurAssetsRatioSeries


# 获取流动资产比率_PIT
from windget import getFaCurAssetsRatio


# 获取固定资产比率_PIT时间序列
from windget import getFaFixedAssetToAssetSeries


# 获取固定资产比率_PIT
from windget import getFaFixedAssetToAsset


# 获取无形资产比率_PIT时间序列
from windget import getFaIntangAssetRatioSeries


# 获取无形资产比率_PIT
from windget import getFaIntangAssetRatio


# 获取有形资产_PIT时间序列
from windget import getFaTangibleAssetSeries


# 获取有形资产_PIT
from windget import getFaTangibleAsset


# 获取固定资产合计_PIT时间序列
from windget import getFaFixAssetsSeries


# 获取固定资产合计_PIT
from windget import getFaFixAssets


# 获取预测总资产收益率(ROA)平均值时间序列
from windget import getEstAvgRoaSeries


# 获取预测总资产收益率(ROA)平均值
from windget import getEstAvgRoa


# 获取预测总资产收益率(ROA)最大值时间序列
from windget import getEstMaxRoaSeries


# 获取预测总资产收益率(ROA)最大值
from windget import getEstMaxRoa


# 获取预测总资产收益率(ROA)最小值时间序列
from windget import getEstMinRoaSeries


# 获取预测总资产收益率(ROA)最小值
from windget import getEstMinRoa


# 获取预测总资产收益率(ROA)中值时间序列
from windget import getEstMedianRoaSeries


# 获取预测总资产收益率(ROA)中值
from windget import getEstMedianRoa


# 获取预测总资产收益率(ROA)标准差时间序列
from windget import getEstStdRoaSeries


# 获取预测总资产收益率(ROA)标准差
from windget import getEstStdRoa


# 获取预测净资产收益率(ROE)平均值时间序列
from windget import getEstAvgRoeSeries


# 获取预测净资产收益率(ROE)平均值
from windget import getEstAvgRoe


# 获取预测净资产收益率(ROE)最大值时间序列
from windget import getEstMaxRoeSeries


# 获取预测净资产收益率(ROE)最大值
from windget import getEstMaxRoe


# 获取预测净资产收益率(ROE)最小值时间序列
from windget import getEstMinRoeSeries


# 获取预测净资产收益率(ROE)最小值
from windget import getEstMinRoe


# 获取预测净资产收益率(ROE)中值时间序列
from windget import getEstMedianRoeSeries


# 获取预测净资产收益率(ROE)中值
from windget import getEstMedianRoe


# 获取预测净资产收益率(ROE)标准差时间序列
from windget import getEstStdRoeSeries


# 获取预测净资产收益率(ROE)标准差
from windget import getEstStdRoe


# 获取预测总资产收益率(ROA)平均值(可选类型)时间序列
from windget import getWestAvgRoaSeries


# 获取预测总资产收益率(ROA)平均值(可选类型)
from windget import getWestAvgRoa


# 获取预测总资产收益率(ROA)最大值(可选类型)时间序列
from windget import getWestMaxRoaSeries


# 获取预测总资产收益率(ROA)最大值(可选类型)
from windget import getWestMaxRoa


# 获取预测总资产收益率(ROA)最小值(可选类型)时间序列
from windget import getWestMinRoaSeries


# 获取预测总资产收益率(ROA)最小值(可选类型)
from windget import getWestMinRoa


# 获取预测总资产收益率(ROA)中值(可选类型)时间序列
from windget import getWestMedianRoaSeries


# 获取预测总资产收益率(ROA)中值(可选类型)
from windget import getWestMedianRoa


# 获取预测总资产收益率(ROA)标准差(可选类型)时间序列
from windget import getWestStdRoaSeries


# 获取预测总资产收益率(ROA)标准差(可选类型)
from windget import getWestStdRoa


# 获取预测净资产收益率(ROE)平均值(可选类型)时间序列
from windget import getWestAvgRoeSeries


# 获取预测净资产收益率(ROE)平均值(可选类型)
from windget import getWestAvgRoe


# 获取预测净资产收益率(ROE)最大值(可选类型)时间序列
from windget import getWestMaxRoeSeries


# 获取预测净资产收益率(ROE)最大值(可选类型)
from windget import getWestMaxRoe


# 获取预测净资产收益率(ROE)最小值(可选类型)时间序列
from windget import getWestMinRoeSeries


# 获取预测净资产收益率(ROE)最小值(可选类型)
from windget import getWestMinRoe


# 获取预测净资产收益率(ROE)中值(可选类型)时间序列
from windget import getWestMedianRoeSeries


# 获取预测净资产收益率(ROE)中值(可选类型)
from windget import getWestMedianRoe


# 获取预测净资产收益率(ROE)标准差(可选类型)时间序列
from windget import getWestStdRoeSeries


# 获取预测净资产收益率(ROE)标准差(可选类型)
from windget import getWestStdRoe


# 获取每股净资产BPS时间序列
from windget import getBpSSeries


# 获取每股净资产BPS
from windget import getBpS


# 获取每股净资产BPS(最新股本摊薄)时间序列
from windget import getBpSAdjustSeries


# 获取每股净资产BPS(最新股本摊薄)
from windget import getBpSAdjust


# 获取每股净资产BPS(最新公告)时间序列
from windget import getBpSNewSeries


# 获取每股净资产BPS(最新公告)
from windget import getBpSNew


# 获取非生息资产时间序列
from windget import getStmNoteBank421Series


# 获取非生息资产
from windget import getStmNoteBank421


# 获取表内外资产总额时间序列
from windget import getStmNoteSec33Series


# 获取表内外资产总额
from windget import getStmNoteSec33


# 获取总投资资产时间序列
from windget import getStmNoteInSur7809Series


# 获取总投资资产
from windget import getStmNoteInSur7809


# 获取每股净资产_GSD时间序列
from windget import getWgsDBpSSeries


# 获取每股净资产_GSD
from windget import getWgsDBpS


# 获取每股净资产(最新公告)_GSD时间序列
from windget import getWgsDBpSNewSeries


# 获取每股净资产(最新公告)_GSD
from windget import getWgsDBpSNew


# 获取平均净资产收益率_GSD时间序列
from windget import getWgsDDupontRoeSeries


# 获取平均净资产收益率_GSD
from windget import getWgsDDupontRoe


# 获取非流动资产合计_GSD时间序列
from windget import getWgsDAssetsLtSeries


# 获取非流动资产合计_GSD
from windget import getWgsDAssetsLt


# 获取使用权资产时间序列
from windget import getPropRightUseSeries


# 获取使用权资产
from windget import getPropRightUse


# 获取非流动资产差额(特殊报表科目)时间序列
from windget import getNonCurAssetsGapSeries


# 获取非流动资产差额(特殊报表科目)
from windget import getNonCurAssetsGap


# 获取非流动资产差额说明(特殊报表科目)时间序列
from windget import getNonCurAssetsGapDetailSeries


# 获取非流动资产差额说明(特殊报表科目)
from windget import getNonCurAssetsGapDetail


# 获取非流动资产差额(合计平衡项目)时间序列
from windget import getNonCurAssetsNettingSeries


# 获取非流动资产差额(合计平衡项目)
from windget import getNonCurAssetsNetting


# 获取非流动资产合计时间序列
from windget import getStm07BsReItsNonLiquidSeries


# 获取非流动资产合计
from windget import getStm07BsReItsNonLiquid


# 获取非流动资产处置净损失时间序列
from windget import getNetLossDispNonCurAssetSeries


# 获取非流动资产处置净损失
from windget import getNetLossDispNonCurAsset


# 获取使用权资产折旧时间序列
from windget import getDePrePropRightUseSeries


# 获取使用权资产折旧
from windget import getDePrePropRightUse


# 获取非流动资产处置损益时间序列
from windget import getStmNoteEoItems6Series


# 获取非流动资产处置损益
from windget import getStmNoteEoItems6


# 获取对数总资产_PIT时间序列
from windget import getValLnToTAssetsSeries


# 获取对数总资产_PIT
from windget import getValLnToTAssets


# 获取每股净资产_PIT时间序列
from windget import getFaBpSSeries


# 获取每股净资产_PIT
from windget import getFaBpS


# 获取现金流资产比-资产回报率(TTM)_PIT时间序列
from windget import getFaAccaTtMSeries


# 获取现金流资产比-资产回报率(TTM)_PIT
from windget import getFaAccaTtM


# 获取非流动资产比率_PIT时间序列
from windget import getFaNonCurAssetsRatioSeries


# 获取非流动资产比率_PIT
from windget import getFaNonCurAssetsRatio


# 获取债务总资产比_PIT时间序列
from windget import getFaDebtsAssetRatioSeries


# 获取债务总资产比_PIT
from windget import getFaDebtsAssetRatio


# 获取加权风险资产净额时间序列
from windget import getStmNoteBank133NSeries


# 获取加权风险资产净额
from windget import getStmNoteBank133N


# 获取加权风险资产净额(2013)时间序列
from windget import getStmNoteBankRWeightedAssetsSeries


# 获取加权风险资产净额(2013)
from windget import getStmNoteBankRWeightedAssets


# 获取加权风险资产净额(旧)时间序列
from windget import getStmNoteBank133Series


# 获取加权风险资产净额(旧)
from windget import getStmNoteBank133


# 获取受托管理资产总规模时间序列
from windget import getStmNoteAssetManageSeries


# 获取受托管理资产总规模
from windget import getStmNoteAssetManage


# 获取权益投资资产分红收入时间序列
from windget import getStmNoteInvestmentIncome0002Series


# 获取权益投资资产分红收入
from windget import getStmNoteInvestmentIncome0002


# 获取其他流动资产_GSD时间序列
from windget import getWgsDAssetsCurROThSeries


# 获取其他流动资产_GSD
from windget import getWgsDAssetsCurROTh


# 获取其他固定资产净值_GSD时间序列
from windget import getWgsDPpeNetOThSeries


# 获取其他固定资产净值_GSD
from windget import getWgsDPpeNetOTh


# 获取出售固定资产收到的现金_GSD时间序列
from windget import getWgsDAssetsBusCfSeries


# 获取出售固定资产收到的现金_GSD
from windget import getWgsDAssetsBusCf


# 获取其他流动资产时间序列
from windget import getOThCurAssetsSeries


# 获取其他流动资产
from windget import getOThCurAssets


# 获取代理业务资产时间序列
from windget import getAgencyBusAssetsSeries


# 获取代理业务资产
from windget import getAgencyBusAssets


# 获取独立账户资产时间序列
from windget import getIndependentAccTAssetsSeries


# 获取独立账户资产
from windget import getIndependentAccTAssets


# 获取衍生金融资产时间序列
from windget import getDerivativeFinAssetsSeries


# 获取衍生金融资产
from windget import getDerivativeFinAssets


# 获取处置固定资产、无形资产和其他长期资产收回的现金净额时间序列
from windget import getNetCashRecpDispFiOltASeries


# 获取处置固定资产、无形资产和其他长期资产收回的现金净额
from windget import getNetCashRecpDispFiOltA


# 获取购建固定资产、无形资产和其他长期资产支付的现金时间序列
from windget import getCashPayAcqConstFiOltASeries


# 获取购建固定资产、无形资产和其他长期资产支付的现金
from windget import getCashPayAcqConstFiOltA


# 获取处置固定资产、无形资产和其他长期资产的损失时间序列
from windget import getLossDispFiOltASeries


# 获取处置固定资产、无形资产和其他长期资产的损失
from windget import getLossDispFiOltA


# 获取单季度.资产处置收益时间序列
from windget import getQfaGainAssetDispositionsSeries


# 获取单季度.资产处置收益
from windget import getQfaGainAssetDispositions


# 获取非货币性资产交换损益时间序列
from windget import getStmNoteEoItems11Series


# 获取非货币性资产交换损益
from windget import getStmNoteEoItems11


# 获取衍生金融资产_FUND时间序列
from windget import getStmBs109Series


# 获取衍生金融资产_FUND
from windget import getStmBs109


# 获取新股申购资产规模报备日时间序列
from windget import getIpoAssetDateSeries


# 获取新股申购资产规模报备日
from windget import getIpoAssetDate


# 获取5年平均资产回报率_PIT时间序列
from windget import getFaRoaAvg5YSeries


# 获取5年平均资产回报率_PIT
from windget import getFaRoaAvg5Y


# 获取ABS基础资产分类时间序列
from windget import getAbsUnderlyingTypeSeries


# 获取ABS基础资产分类
from windget import getAbsUnderlyingType


# 获取预测每股净资产(BPS)平均值时间序列
from windget import getEstAvgBpSSeries


# 获取预测每股净资产(BPS)平均值
from windget import getEstAvgBpS


# 获取预测每股净资产(BPS)最大值时间序列
from windget import getEstMaxBpSSeries


# 获取预测每股净资产(BPS)最大值
from windget import getEstMaxBpS


# 获取预测每股净资产(BPS)最小值时间序列
from windget import getEstMinBpSSeries


# 获取预测每股净资产(BPS)最小值
from windget import getEstMinBpS


# 获取预测每股净资产(BPS)中值时间序列
from windget import getEstMedianBpSSeries


# 获取预测每股净资产(BPS)中值
from windget import getEstMedianBpS


# 获取预测每股净资产(BPS)标准差时间序列
from windget import getEstStdBpSSeries


# 获取预测每股净资产(BPS)标准差
from windget import getEstStdBpS


# 获取预测每股净资产(BPS)平均值(币种转换)时间序列
from windget import getEstAvgBpS1Series


# 获取预测每股净资产(BPS)平均值(币种转换)
from windget import getEstAvgBpS1


# 获取预测每股净资产(BPS)最大值(币种转换)时间序列
from windget import getEstMaxBpS1Series


# 获取预测每股净资产(BPS)最大值(币种转换)
from windget import getEstMaxBpS1


# 获取预测每股净资产(BPS)最小值(币种转换)时间序列
from windget import getEstMinBpS1Series


# 获取预测每股净资产(BPS)最小值(币种转换)
from windget import getEstMinBpS1


# 获取预测每股净资产(BPS)中值(币种转换)时间序列
from windget import getEstMedianBpS1Series


# 获取预测每股净资产(BPS)中值(币种转换)
from windget import getEstMedianBpS1


# 获取预测每股净资产(BPS)标准差(币种转换)时间序列
from windget import getEstStdBpS1Series


# 获取预测每股净资产(BPS)标准差(币种转换)
from windget import getEstStdBpS1


# 获取预测每股净资产(BPS)平均值(可选类型)时间序列
from windget import getWestAvgBpSSeries


# 获取预测每股净资产(BPS)平均值(可选类型)
from windget import getWestAvgBpS


# 获取预测每股净资产(BPS)最大值(可选类型)时间序列
from windget import getWestMaxBpSSeries


# 获取预测每股净资产(BPS)最大值(可选类型)
from windget import getWestMaxBpS


# 获取预测每股净资产(BPS)最小值(可选类型)时间序列
from windget import getWestMinBpSSeries


# 获取预测每股净资产(BPS)最小值(可选类型)
from windget import getWestMinBpS


# 获取预测每股净资产(BPS)中值(可选类型)时间序列
from windget import getWestMedianBpSSeries


# 获取预测每股净资产(BPS)中值(可选类型)
from windget import getWestMedianBpS


# 获取预测每股净资产(BPS)标准差(可选类型)时间序列
from windget import getWestStdBpSSeries


# 获取预测每股净资产(BPS)标准差(可选类型)
from windget import getWestStdBpS


# 获取预测每股净资产(BPS)平均值(可选类型,币种转换)时间序列
from windget import getWestAvgBpS1Series


# 获取预测每股净资产(BPS)平均值(可选类型,币种转换)
from windget import getWestAvgBpS1


# 获取预测每股净资产(BPS)最大值(可选类型,币种转换)时间序列
from windget import getWestMaxBpS1Series


# 获取预测每股净资产(BPS)最大值(可选类型,币种转换)
from windget import getWestMaxBpS1


# 获取预测每股净资产(BPS)最小值(可选类型,币种转换)时间序列
from windget import getWestMinBpS1Series


# 获取预测每股净资产(BPS)最小值(可选类型,币种转换)
from windget import getWestMinBpS1


# 获取预测每股净资产(BPS)中值(可选类型,币种转换)时间序列
from windget import getWestMedianBpS1Series


# 获取预测每股净资产(BPS)中值(可选类型,币种转换)
from windget import getWestMedianBpS1


# 获取预测每股净资产(BPS)标准差(可选类型,币种转换)时间序列
from windget import getWestStdBpS1Series


# 获取预测每股净资产(BPS)标准差(可选类型,币种转换)
from windget import getWestStdBpS1


# 获取预测每股净资产Surprise(可选类型)时间序列
from windget import getWestBpSSurpriseSeries


# 获取预测每股净资产Surprise(可选类型)
from windget import getWestBpSSurprise


# 获取预测每股净资产Surprise百分比(可选类型)时间序列
from windget import getWestBpSSurprisePctSeries


# 获取预测每股净资产Surprise百分比(可选类型)
from windget import getWestBpSSurprisePct


# 获取净资本/净资产时间序列
from windget import getStmNoteSec6Series


# 获取净资本/净资产
from windget import getStmNoteSec6


# 获取单季度.净资产收益率ROE时间序列
from windget import getQfaRoeSeries


# 获取单季度.净资产收益率ROE
from windget import getQfaRoe


# 获取单季度.总资产净利率ROA时间序列
from windget import getQfaRoaSeries


# 获取单季度.总资产净利率ROA
from windget import getQfaRoa


# 获取单季度.净资产收益率ROE_GSD时间序列
from windget import getWgsDQfaRoeSeries


# 获取单季度.净资产收益率ROE_GSD
from windget import getWgsDQfaRoe


# 获取单季度.总资产净利率ROA_GSD时间序列
from windget import getWgsDQfaRoaSeries


# 获取单季度.总资产净利率ROA_GSD
from windget import getWgsDQfaRoa


# 获取交易性金融资产_GSD时间序列
from windget import getWgsDInvestTradingSeries


# 获取交易性金融资产_GSD
from windget import getWgsDInvestTrading


# 获取其他非流动资产_GSD时间序列
from windget import getWgsDAssetsLtOThSeries


# 获取其他非流动资产_GSD
from windget import getWgsDAssetsLtOTh


# 获取消耗性生物资产时间序列
from windget import getConsumptiveBioAssetsSeries


# 获取消耗性生物资产
from windget import getConsumptiveBioAssets


# 获取生产性生物资产时间序列
from windget import getProductiveBioAssetsSeries


# 获取生产性生物资产
from windget import getProductiveBioAssets


# 获取其他非流动资产时间序列
from windget import getOThNonCurAssetsSeries


# 获取其他非流动资产
from windget import getOThNonCurAssets


# 获取生产性生物资产-原值时间序列
from windget import getStmNoteAssetDetail9Series


# 获取生产性生物资产-原值
from windget import getStmNoteAssetDetail9


# 获取生产性生物资产-累计折旧时间序列
from windget import getStmNoteAssetDetail10Series


# 获取生产性生物资产-累计折旧
from windget import getStmNoteAssetDetail10


# 获取生产性生物资产-减值准备时间序列
from windget import getStmNoteAssetDetail11Series


# 获取生产性生物资产-减值准备
from windget import getStmNoteAssetDetail11


# 获取生产性生物资产-净额时间序列
from windget import getStmNoteAssetDetail12Series


# 获取生产性生物资产-净额
from windget import getStmNoteAssetDetail12


# 获取交易性金融资产_FUND时间序列
from windget import getStmBs71Series


# 获取交易性金融资产_FUND
from windget import getStmBs71


# 获取长期负债/资产总计_PIT时间序列
from windget import getFaLtDebtToAssetSeries


# 获取长期负债/资产总计_PIT
from windget import getFaLtDebtToAsset


# 获取应付债券/资产总计_PIT时间序列
from windget import getFaBondsPayableToAssetSeries


# 获取应付债券/资产总计_PIT
from windget import getFaBondsPayableToAsset


# 获取信用风险加权资产(2013)时间序列
from windget import getStmNoteBankRWeightedAssetsCrSeries


# 获取信用风险加权资产(2013)
from windget import getStmNoteBankRWeightedAssetsCr


# 获取市场风险加权资产(2013)时间序列
from windget import getStmNoteBankRWeightedAssetsMrSeries


# 获取市场风险加权资产(2013)
from windget import getStmNoteBankRWeightedAssetsMr


# 获取操作风险加权资产(2013)时间序列
from windget import getStmNoteBankRWeightedAssetsOrSeries


# 获取操作风险加权资产(2013)
from windget import getStmNoteBankRWeightedAssetsOr


# 获取卖出回购金融资产款时间序列
from windget import getFundSalesFinAssetsRpSeries


# 获取卖出回购金融资产款
from windget import getFundSalesFinAssetsRp


# 获取融资租入固定资产时间序列
from windget import getFaFncLeasesSeries


# 获取融资租入固定资产
from windget import getFaFncLeases


# 获取单季度.固定资产折旧、油气资产折耗、生产性生物资产折旧时间序列
from windget import getQfaDePrFaCogADpBaSeries


# 获取单季度.固定资产折旧、油气资产折耗、生产性生物资产折旧
from windget import getQfaDePrFaCogADpBa


# 获取单季度.无形资产摊销时间序列
from windget import getQfaAMortIntangAssetsSeries


# 获取单季度.无形资产摊销
from windget import getQfaAMortIntangAssets


# 获取单季度.固定资产报废损失时间序列
from windget import getQfaLossSCrFaSeries


# 获取单季度.固定资产报废损失
from windget import getQfaLossSCrFa


# 获取担保总额占净资产比例时间序列
from windget import getStmNoteGuarantee6Series


# 获取担保总额占净资产比例
from windget import getStmNoteGuarantee6


# 获取卖出回购金融资产支出_FUND时间序列
from windget import getStmIs13Series


# 获取卖出回购金融资产支出_FUND
from windget import getStmIs13


# 获取一致预测每股净资产(FY1)时间序列
from windget import getWestAvgBpSFy1Series


# 获取一致预测每股净资产(FY1)
from windget import getWestAvgBpSFy1


# 获取一致预测每股净资产(FY2)时间序列
from windget import getWestAvgBpSFy2Series


# 获取一致预测每股净资产(FY2)
from windget import getWestAvgBpSFy2


# 获取一致预测每股净资产(FY3)时间序列
from windget import getWestAvgBpSFy3Series


# 获取一致预测每股净资产(FY3)
from windget import getWestAvgBpSFy3


# 获取利息收入:金融资产回购业务收入时间序列
from windget import getStmNoteSec1513Series


# 获取利息收入:金融资产回购业务收入
from windget import getStmNoteSec1513


# 获取房地产物业相关资产净值_GSD时间序列
from windget import getWgsDRealEstateNetSeries


# 获取房地产物业相关资产净值_GSD
from windget import getWgsDRealEstateNet


# 获取其他非流动金融资产时间序列
from windget import getOThNonCurFinaAssetSeries


# 获取其他非流动金融资产
from windget import getOThNonCurFinaAsset


# 获取处置交易性金融资产净增加额时间序列
from windget import getNetInCrDispTfaSeries


# 获取处置交易性金融资产净增加额
from windget import getNetInCrDispTfa


# 获取单季度.非流动资产处置净损失时间序列
from windget import getQfaNetLossDispNonCurAssetSeries


# 获取单季度.非流动资产处置净损失
from windget import getQfaNetLossDispNonCurAsset


# 获取单季度.使用权资产折旧时间序列
from windget import getQfaDePrePropRightUseSeries


# 获取单季度.使用权资产折旧
from windget import getQfaDePrePropRightUse


# 获取股东权益/固定资产_PIT时间序列
from windget import getFaEquityToFixedAssetSeries


# 获取股东权益/固定资产_PIT
from windget import getFaEquityToFixedAsset


# 获取利息净收入:金融资产回购业务收入时间序列
from windget import getStmNoteSec1533Series


# 获取利息净收入:金融资产回购业务收入
from windget import getStmNoteSec1533


# 获取单季度.出售固定资产收到的现金_GSD时间序列
from windget import getWgsDQfaAssetsBusCfSeries


# 获取单季度.出售固定资产收到的现金_GSD
from windget import getWgsDQfaAssetsBusCf


# 获取划分为持有待售的资产时间序列
from windget import getHfSAssetsSeries


# 获取划分为持有待售的资产
from windget import getHfSAssets


# 获取单季度.处置固定资产、无形资产和其他长期资产收回的现金净额时间序列
from windget import getQfaNetCashRecpDispFiOltASeries


# 获取单季度.处置固定资产、无形资产和其他长期资产收回的现金净额
from windget import getQfaNetCashRecpDispFiOltA


# 获取单季度.购建固定资产、无形资产和其他长期资产支付的现金时间序列
from windget import getQfaCashPayAcqConstFiOltASeries


# 获取单季度.购建固定资产、无形资产和其他长期资产支付的现金
from windget import getQfaCashPayAcqConstFiOltA


# 获取单季度.处置固定资产、无形资产和其他长期资产的损失时间序列
from windget import getQfaLossDispFiOltASeries


# 获取单季度.处置固定资产、无形资产和其他长期资产的损失
from windget import getQfaLossDispFiOltA


# 获取一年内到期的非流动资产时间序列
from windget import getNonCurAssetsDueWithin1YSeries


# 获取一年内到期的非流动资产
from windget import getNonCurAssetsDueWithin1Y


# 获取以摊余成本计量的金融资产时间序列
from windget import getFinAssetsAmortizedCostSeries


# 获取以摊余成本计量的金融资产
from windget import getFinAssetsAmortizedCost


# 获取以摊余成本计量的金融资产终止确认收益时间序列
from windget import getTerFinAsSIncomeSeries


# 获取以摊余成本计量的金融资产终止确认收益
from windget import getTerFinAsSIncome


# 获取单季度.融资租入固定资产时间序列
from windget import getQfaFaFncLeasesSeries


# 获取单季度.融资租入固定资产
from windget import getQfaFaFncLeases


# 获取存货明细-消耗性生物资产时间序列
from windget import getStmNoteInv9Series


# 获取存货明细-消耗性生物资产
from windget import getStmNoteInv9


# 获取单季度.处置交易性金融资产净增加额时间序列
from windget import getQfaNetInCrDispTfaSeries


# 获取单季度.处置交易性金融资产净增加额
from windget import getQfaNetInCrDispTfa


# 获取息税前利润(TTM)/总资产时间序列
from windget import getEbItToAssets2Series


# 获取息税前利润(TTM)/总资产
from windget import getEbItToAssets2


# 获取息税前利润(TTM)/总资产_GSD时间序列
from windget import getEbItToAssetsTtMSeries


# 获取息税前利润(TTM)/总资产_GSD
from windget import getEbItToAssetsTtM


# 获取持有(或处置)交易性金融资产和负债产生的公允价值变动损益时间序列
from windget import getStmNoteEoItems28Series


# 获取持有(或处置)交易性金融资产和负债产生的公允价值变动损益
from windget import getStmNoteEoItems28


# 获取单季度.以摊余成本计量的金融资产终止确认收益时间序列
from windget import getQfaTerFinAsSIncomeSeries


# 获取单季度.以摊余成本计量的金融资产终止确认收益
from windget import getQfaTerFinAsSIncome


# 获取ETF申购赎回最小申购赎回单位资产净值时间序列
from windget import getFundEtFPrMinnaVUnitSeries


# 获取ETF申购赎回最小申购赎回单位资产净值
from windget import getFundEtFPrMinnaVUnit


# 获取以公允价值计量且其变动计入当期损益的金融资产时间序列
from windget import getTradableFinAssetsSeries


# 获取以公允价值计量且其变动计入当期损益的金融资产
from windget import getTradableFinAssets


# 获取负债差额(特殊报表科目)时间序列
from windget import getLiaBGapSeries


# 获取负债差额(特殊报表科目)
from windget import getLiaBGap


# 获取负债差额说明(特殊报表科目)时间序列
from windget import getLiaBGapDetailSeries


# 获取负债差额说明(特殊报表科目)
from windget import getLiaBGapDetail


# 获取负债差额(合计平衡项目)时间序列
from windget import getLiaBNettingSeries


# 获取负债差额(合计平衡项目)
from windget import getLiaBNetting


# 获取负债合计时间序列
from windget import getStm07BsReItsAllDebtSeries


# 获取负债合计
from windget import getStm07BsReItsAllDebt


# 获取负债及股东权益差额(特殊报表科目)时间序列
from windget import getLiaBSHrhLDrEqYGapSeries


# 获取负债及股东权益差额(特殊报表科目)
from windget import getLiaBSHrhLDrEqYGap


# 获取负债及股东权益差额说明(特殊报表科目)时间序列
from windget import getLiaBSHrhLDrEqYGapDetailSeries


# 获取负债及股东权益差额说明(特殊报表科目)
from windget import getLiaBSHrhLDrEqYGapDetail


# 获取负债及股东权益差额(合计平衡项目)时间序列
from windget import getLiaBSHrhLDrEqYNettingSeries


# 获取负债及股东权益差额(合计平衡项目)
from windget import getLiaBSHrhLDrEqYNetting


# 获取负债及股东权益总计时间序列
from windget import getToTLiaBSHrhLDrEqYSeries


# 获取负债及股东权益总计
from windget import getToTLiaBSHrhLDrEqY


# 获取负债合计_FUND时间序列
from windget import getStmBs33Series


# 获取负债合计_FUND
from windget import getStmBs33


# 获取负债及持有人权益合计_FUND时间序列
from windget import getStmBs39Series


# 获取负债及持有人权益合计_FUND
from windget import getStmBs39


# 获取负债和所有者权益总计时间序列
from windget import getStm07BsReItsDebtEquitySeries


# 获取负债和所有者权益总计
from windget import getStm07BsReItsDebtEquity


# 获取负债合计_PIT时间序列
from windget import getFaToTliAbSeries


# 获取负债合计_PIT
from windget import getFaToTliAb


# 获取负债合计(MRQ,只有最新数据)时间序列
from windget import getDebtMrQSeries


# 获取负债合计(MRQ,只有最新数据)
from windget import getDebtMrQ


# 获取总负债_GSD时间序列
from windget import getWgsDLiAbsSeries


# 获取总负债_GSD
from windget import getWgsDLiAbs


# 获取总负债及总权益_GSD时间序列
from windget import getWgsDLiAbsStKhlDrSEqSeries


# 获取总负债及总权益_GSD
from windget import getWgsDLiAbsStKhlDrSEq


# 获取计息负债时间序列
from windget import getStmNoteBank381Series


# 获取计息负债
from windget import getStmNoteBank381


# 获取计息负债成本率时间序列
from windget import getStmNoteBank60Series


# 获取计息负债成本率
from windget import getStmNoteBank60


# 获取计息负债平均余额时间序列
from windget import getStmNoteBank59Series


# 获取计息负债平均余额
from windget import getStmNoteBank59


# 获取无息负债时间序列
from windget import getFaNoneInterestDebtSeries


# 获取无息负债
from windget import getFaNoneInterestDebt


# 获取认可负债时间序列
from windget import getQStmNoteInSur212513Series


# 获取认可负债
from windget import getQStmNoteInSur212513


# 获取合同负债_GSD时间序列
from windget import getWgsDLiAbsContractSeries


# 获取合同负债_GSD
from windget import getWgsDLiAbsContract


# 获取流动负债合计_GSD时间序列
from windget import getWgsDLiAbsCurRSeries


# 获取流动负债合计_GSD
from windget import getWgsDLiAbsCurR


# 获取其他负债_GSD时间序列
from windget import getWgsDLiAbsOThSeries


# 获取其他负债_GSD
from windget import getWgsDLiAbsOTh


# 获取合同负债时间序列
from windget import getContLiaBSeries


# 获取合同负债
from windget import getContLiaB


# 获取流动负债差额(特殊报表科目)时间序列
from windget import getCurLiaBGapSeries


# 获取流动负债差额(特殊报表科目)
from windget import getCurLiaBGap


# 获取流动负债差额说明(特殊报表科目)时间序列
from windget import getCurLiaBGapDetailSeries


# 获取流动负债差额说明(特殊报表科目)
from windget import getCurLiaBGapDetail


# 获取流动负债差额(合计平衡项目)时间序列
from windget import getCurLiaBNettingSeries


# 获取流动负债差额(合计平衡项目)
from windget import getCurLiaBNetting


# 获取流动负债合计时间序列
from windget import getStm07BsReItsLiquidDebtSeries


# 获取流动负债合计
from windget import getStm07BsReItsLiquidDebt


# 获取租赁负债时间序列
from windget import getLeaseObligationSeries


# 获取租赁负债
from windget import getLeaseObligation


# 获取预计负债时间序列
from windget import getProvisionsSeries


# 获取预计负债
from windget import getProvisions


# 获取其他负债时间序列
from windget import getOThLiaBSeries


# 获取其他负债
from windget import getOThLiaB


# 获取预计负债产生的损益时间序列
from windget import getStmNoteEoItems18Series


# 获取预计负债产生的损益
from windget import getStmNoteEoItems18


# 获取其他负债_FUND时间序列
from windget import getStmBs32Series


# 获取其他负债_FUND
from windget import getStmBs32


# 获取长期负债/营运资金_PIT时间序列
from windget import getFaUnCurDebtToWorkCapSeries


# 获取长期负债/营运资金_PIT
from windget import getFaUnCurDebtToWorkCap


# 获取非计息负债时间序列
from windget import getStmNoteBank431Series


# 获取非计息负债
from windget import getStmNoteBank431


# 获取净资本负债率时间序列
from windget import getStmNoteSec3Series


# 获取净资本负债率
from windget import getStmNoteSec3


# 获取非流动负债合计_GSD时间序列
from windget import getWgsDLiAbsLtSeries


# 获取非流动负债合计_GSD
from windget import getWgsDLiAbsLt


# 获取非流动负债差额(特殊报表科目)时间序列
from windget import getNonCurLiaBGapSeries


# 获取非流动负债差额(特殊报表科目)
from windget import getNonCurLiaBGap


# 获取非流动负债差额说明(特殊报表科目)时间序列
from windget import getNonCurLiaBGapDetailSeries


# 获取非流动负债差额说明(特殊报表科目)
from windget import getNonCurLiaBGapDetail


# 获取非流动负债差额(合计平衡项目)时间序列
from windget import getNonCurLiaBNettingSeries


# 获取非流动负债差额(合计平衡项目)
from windget import getNonCurLiaBNetting


# 获取非流动负债合计时间序列
from windget import getToTNonCurLiaBSeries


# 获取非流动负债合计
from windget import getToTNonCurLiaB


# 获取无息流动负债时间序列
from windget import getExInterestDebtCurrentSeries


# 获取无息流动负债
from windget import getExInterestDebtCurrent


# 获取无息流动负债_GSD时间序列
from windget import getWgsDExInterestDebtCurrentSeries


# 获取无息流动负债_GSD
from windget import getWgsDExInterestDebtCurrent


# 获取其他流动负债_GSD时间序列
from windget import getWgsDLiAbsCurROThSeries


# 获取其他流动负债_GSD
from windget import getWgsDLiAbsCurROTh


# 获取保险合同负债_GSD时间序列
from windget import getWgsDLiAbsInSurContractSeries


# 获取保险合同负债_GSD
from windget import getWgsDLiAbsInSurContract


# 获取投资合同负债_GSD时间序列
from windget import getWgsDLiAbsInvestContractSeries


# 获取投资合同负债_GSD
from windget import getWgsDLiAbsInvestContract


# 获取其他流动负债时间序列
from windget import getOThCurLiaBSeries


# 获取其他流动负债
from windget import getOThCurLiaB


# 获取代理业务负债时间序列
from windget import getAgencyBusLiaBSeries


# 获取代理业务负债
from windget import getAgencyBusLiaB


# 获取独立账户负债时间序列
from windget import getIndependentAccTLiaBSeries


# 获取独立账户负债
from windget import getIndependentAccTLiaB


# 获取衍生金融负债时间序列
from windget import getDerivativeFinLiaBSeries


# 获取衍生金融负债
from windget import getDerivativeFinLiaB


# 获取衍生金融负债_FUND时间序列
from windget import getStmBs74Series


# 获取衍生金融负债_FUND
from windget import getStmBs74


# 获取现金流动负债比(TTM)_PIT时间序列
from windget import getFaCFotoCurlIAbsTtMSeries


# 获取现金流动负债比(TTM)_PIT
from windget import getFaCFotoCurlIAbsTtM


# 获取现金流动负债比率_PIT时间序列
from windget import getFaCashToCurlIAbsSeries


# 获取现金流动负债比率_PIT
from windget import getFaCashToCurlIAbs


# 获取无息流动负债_PIT时间序列
from windget import getFaNicuRDebtSeries


# 获取无息流动负债_PIT
from windget import getFaNicuRDebt


# 获取无息非流动负债时间序列
from windget import getExInterestDebtNonCurrentSeries


# 获取无息非流动负债
from windget import getExInterestDebtNonCurrent


# 获取营业利润/负债合计_GSD时间序列
from windget import getWgsDOpToDebtSeries


# 获取营业利润/负债合计_GSD
from windget import getWgsDOpToDebt


# 获取无息非流动负债_GSD时间序列
from windget import getWgsDExInterestDebtNonCurrent2Series


# 获取无息非流动负债_GSD
from windget import getWgsDExInterestDebtNonCurrent2


# 获取交易性金融负债_GSD时间序列
from windget import getWgsDLiAbsTradingSeries


# 获取交易性金融负债_GSD
from windget import getWgsDLiAbsTrading


# 获取其他非流动负债_GSD时间序列
from windget import getWgsDLiAbsLtOThSeries


# 获取其他非流动负债_GSD
from windget import getWgsDLiAbsLtOTh


# 获取其他非流动负债时间序列
from windget import getOThNonCurLiaBSeries


# 获取其他非流动负债
from windget import getOThNonCurLiaB


# 获取交易性金融负债_FUND时间序列
from windget import getStmBs73Series


# 获取交易性金融负债_FUND
from windget import getStmBs73


# 获取无息非流动负债_PIT时间序列
from windget import getFaNinoCurDebtSeries


# 获取无息非流动负债_PIT
from windget import getFaNinoCurDebt


# 获取营业利润/流动负债_GSD时间序列
from windget import getWgsDOpToLiqDebtSeries


# 获取营业利润/流动负债_GSD
from windget import getWgsDOpToLiqDebt


# 获取递延收益-流动负债时间序列
from windget import getDeferredIncCurLiaBSeries


# 获取递延收益-流动负债
from windget import getDeferredIncCurLiaB


# 获取划分为持有待售的负债时间序列
from windget import getHfSLiaBSeries


# 获取划分为持有待售的负债
from windget import getHfSLiaB


# 获取递延收益-非流动负债时间序列
from windget import getDeferredIncNonCurLiaBSeries


# 获取递延收益-非流动负债
from windget import getDeferredIncNonCurLiaB


# 获取一年内到期的非流动负债时间序列
from windget import getNonCurLiaBDueWithin1YSeries


# 获取一年内到期的非流动负债
from windget import getNonCurLiaBDueWithin1Y


# 获取短期融资债(其他流动负债)时间序列
from windget import getStmNoteOthers7639Series


# 获取短期融资债(其他流动负债)
from windget import getStmNoteOthers7639


# 获取以公允价值计量且其变动计入当期损益的金融负债时间序列
from windget import getTradableFinLiaBSeries


# 获取以公允价值计量且其变动计入当期损益的金融负债
from windget import getTradableFinLiaB


# 获取所有者权益合计时间序列
from windget import getStm07BsReItsAllEquitySeries


# 获取所有者权益合计
from windget import getStm07BsReItsAllEquity


# 获取期初所有者权益(基金净值)时间序列
from windget import getStmNavChange1Series


# 获取期初所有者权益(基金净值)
from windget import getStmNavChange1


# 获取期末所有者权益(基金净值)时间序列
from windget import getStmNavChange11Series


# 获取期末所有者权益(基金净值)
from windget import getStmNavChange11


# 获取归属于母公司所有者权益合计时间序列
from windget import getStm07BsReItsEquitySeries


# 获取归属于母公司所有者权益合计
from windget import getStm07BsReItsEquity


# 获取归属于母公司所有者权益合计/全部投入资本_PIT时间序列
from windget import getFaEquityToCapitalSeries


# 获取归属于母公司所有者权益合计/全部投入资本_PIT
from windget import getFaEquityToCapital


# 获取现金及现金等价物净增加额_GSD时间序列
from windget import getWgsDChgCashCfSeries


# 获取现金及现金等价物净增加额_GSD
from windget import getWgsDChgCashCf


# 获取现金及现金等价物净增加额差额(特殊报表科目)时间序列
from windget import getNetInCrCashCashEquGapSeries


# 获取现金及现金等价物净增加额差额(特殊报表科目)
from windget import getNetInCrCashCashEquGap


# 获取现金及现金等价物净增加额差额说明(特殊报表科目)时间序列
from windget import getNetInCrCashCashEquGapDetailSeries


# 获取现金及现金等价物净增加额差额说明(特殊报表科目)
from windget import getNetInCrCashCashEquGapDetail


# 获取现金及现金等价物净增加额差额(合计平衡项目)时间序列
from windget import getNetInCrCashCashEquNettingSeries


# 获取现金及现金等价物净增加额差额(合计平衡项目)
from windget import getNetInCrCashCashEquNetting


# 获取现金及现金等价物净增加额时间序列
from windget import getStm07CsReItsCashAddSeries


# 获取现金及现金等价物净增加额
from windget import getStm07CsReItsCashAdd


# 获取单季度.现金及现金等价物净增加额_GSD时间序列
from windget import getWgsDQfaChgCashCfSeries


# 获取单季度.现金及现金等价物净增加额_GSD
from windget import getWgsDQfaChgCashCf


# 获取间接法-现金及现金等价物净增加额时间序列
from windget import getNetInCrCashCashEquImSeries


# 获取间接法-现金及现金等价物净增加额
from windget import getNetInCrCashCashEquIm


# 获取单季度.现金及现金等价物净增加额时间序列
from windget import getQfaNetInCrCashCashEquDmSeries


# 获取单季度.现金及现金等价物净增加额
from windget import getQfaNetInCrCashCashEquDm


# 获取单季度.间接法-现金及现金等价物净增加额时间序列
from windget import getQfaNetInCrCashCashEquImSeries


# 获取单季度.间接法-现金及现金等价物净增加额
from windget import getQfaNetInCrCashCashEquIm


# 获取营业总收入(TTM)_PIT时间序列
from windget import getFaGrTtMSeries


# 获取营业总收入(TTM)_PIT
from windget import getFaGrTtM


# 获取营业总收入(TTM)时间序列
from windget import getGrTtM2Series


# 获取营业总收入(TTM)
from windget import getGrTtM2


# 获取营业总收入(TTM)_GSD时间序列
from windget import getGrTtM3Series


# 获取营业总收入(TTM)_GSD
from windget import getGrTtM3


# 获取营业总收入时间序列
from windget import getStm07IsReItsSIncomeSeries


# 获取营业总收入
from windget import getStm07IsReItsSIncome


# 获取单季度.营业总收入时间序列
from windget import getQfaToTOperRevSeries


# 获取单季度.营业总收入
from windget import getQfaToTOperRev


# 获取EBITDA/营业总收入时间序列
from windget import getEbItDatoSalesSeries


# 获取EBITDA/营业总收入
from windget import getEbItDatoSales


# 获取EBITDA/营业总收入_GSD时间序列
from windget import getWgsDEbItDatoSalesSeries


# 获取EBITDA/营业总收入_GSD
from windget import getWgsDEbItDatoSales


# 获取营业收入(TTM)_VAL_PIT时间序列
from windget import getOrTtMSeries


# 获取营业收入(TTM)_VAL_PIT
from windget import getOrTtM


# 获取营业收入(TTM)时间序列
from windget import getOrTtM2Series


# 获取营业收入(TTM)
from windget import getOrTtM2


# 获取营业收入(TTM)_GSD时间序列
from windget import getOrTtM3Series


# 获取营业收入(TTM)_GSD
from windget import getOrTtM3


# 获取营业收入时间序列
from windget import getStm07IsReItsIncomeSeries


# 获取营业收入
from windget import getStm07IsReItsIncome


# 获取营业收入(TTM)_PIT时间序列
from windget import getFaOrTtMSeries


# 获取营业收入(TTM)_PIT
from windget import getFaOrTtM


# 获取总营业收入_GSD时间序列
from windget import getWgsDSalesSeries


# 获取总营业收入_GSD
from windget import getWgsDSales


# 获取总营业收入(公布值)_GSD时间序列
from windget import getArdIsSalesSeries


# 获取总营业收入(公布值)_GSD
from windget import getArdIsSales


# 获取预测营业收入Surprise(可选类型)时间序列
from windget import getWestSalesSurpriseSeries


# 获取预测营业收入Surprise(可选类型)
from windget import getWestSalesSurprise


# 获取预测营业收入Surprise百分比(可选类型)时间序列
from windget import getWestSalesSurprisePctSeries


# 获取预测营业收入Surprise百分比(可选类型)
from windget import getWestSalesSurprisePct


# 获取其他营业收入_GSD时间序列
from windget import getWgsDSalesOThSeries


# 获取其他营业收入_GSD
from windget import getWgsDSalesOTh


# 获取一致预测营业收入(FY1)时间序列
from windget import getWestSalesFy1Series


# 获取一致预测营业收入(FY1)
from windget import getWestSalesFy1


# 获取一致预测营业收入(FY2)时间序列
from windget import getWestSalesFy2Series


# 获取一致预测营业收入(FY2)
from windget import getWestSalesFy2


# 获取一致预测营业收入(FY3)时间序列
from windget import getWestSalesFy3Series


# 获取一致预测营业收入(FY3)
from windget import getWestSalesFy3


# 获取单季度.营业收入时间序列
from windget import getQfaOperRevSeries


# 获取单季度.营业收入
from windget import getQfaOperRev


# 获取一致预测营业收入(FY1)变化率_1M_PIT时间序列
from windget import getWestSalesFy11MSeries


# 获取一致预测营业收入(FY1)变化率_1M_PIT
from windget import getWestSalesFy11M


# 获取一致预测营业收入(FY1)变化率_3M_PIT时间序列
from windget import getWestSalesFy13MSeries


# 获取一致预测营业收入(FY1)变化率_3M_PIT
from windget import getWestSalesFy13M


# 获取一致预测营业收入(FY1)变化率_6M_PIT时间序列
from windget import getWestSalesFy16MSeries


# 获取一致预测营业收入(FY1)变化率_6M_PIT
from windget import getWestSalesFy16M


# 获取一致预测营业收入(FY1)的变化_1M_PIT时间序列
from windget import getWestSalesFy1Chg1MSeries


# 获取一致预测营业收入(FY1)的变化_1M_PIT
from windget import getWestSalesFy1Chg1M


# 获取一致预测营业收入(FY1)的变化_3M_PIT时间序列
from windget import getWestSalesFy1Chg3MSeries


# 获取一致预测营业收入(FY1)的变化_3M_PIT
from windget import getWestSalesFy1Chg3M


# 获取一致预测营业收入(FY1)的变化_6M_PIT时间序列
from windget import getWestSalesFy1Chg6MSeries


# 获取一致预测营业收入(FY1)的变化_6M_PIT
from windget import getWestSalesFy1Chg6M


# 获取一致预测营业收入(FY1)标准差_PIT时间序列
from windget import getWestStdSalesFy1Series


# 获取一致预测营业收入(FY1)标准差_PIT
from windget import getWestStdSalesFy1


# 获取一致预测营业收入(FY1)最大与一致预测营业收入(FY1)最小值的变化率_PIT时间序列
from windget import getWestSalesMaxMinFy1Series


# 获取一致预测营业收入(FY1)最大与一致预测营业收入(FY1)最小值的变化率_PIT
from windget import getWestSalesMaxMinFy1


# 获取营业利润/营业收入(TTM)时间序列
from windget import getOpToOrTtMSeries


# 获取营业利润/营业收入(TTM)
from windget import getOpToOrTtM


# 获取利润总额/营业收入(TTM)时间序列
from windget import getEBtToOrTtMSeries


# 获取利润总额/营业收入(TTM)
from windget import getEBtToOrTtM


# 获取营业利润/营业收入(TTM)_GSD时间序列
from windget import getOpToOrTtM2Series


# 获取营业利润/营业收入(TTM)_GSD
from windget import getOpToOrTtM2


# 获取利润总额/营业收入(TTM)_GSD时间序列
from windget import getEBtToOrTtM2Series


# 获取利润总额/营业收入(TTM)_GSD
from windget import getEBtToOrTtM2


# 获取单季度.总营业收入_GSD时间序列
from windget import getWgsDQfaSalesSeries


# 获取单季度.总营业收入_GSD
from windget import getWgsDQfaSales


# 获取营业利润/营业收入(TTM)_PIT时间序列
from windget import getFaOpToOrTtMSeries


# 获取营业利润/营业收入(TTM)_PIT
from windget import getFaOpToOrTtM


# 获取利润总额/营业收入(TTM)_PIT时间序列
from windget import getFaPbtToOrTtMSeries


# 获取利润总额/营业收入(TTM)_PIT
from windget import getFaPbtToOrTtM


# 获取单季度.其他营业收入_GSD时间序列
from windget import getWgsDQfaSalesOThSeries


# 获取单季度.其他营业收入_GSD
from windget import getWgsDQfaSalesOTh


# 获取研发支出总额占营业收入比例时间序列
from windget import getStmNoteRdExpToSalesSeries


# 获取研发支出总额占营业收入比例
from windget import getStmNoteRdExpToSales


# 获取归属母公司股东的净利润/营业收入(TTM)时间序列
from windget import getNetProfitToOrTtMSeries


# 获取归属母公司股东的净利润/营业收入(TTM)
from windget import getNetProfitToOrTtM


# 获取归属母公司股东的净利润/营业收入(TTM)_GSD时间序列
from windget import getNetProfitToOrTtM2Series


# 获取归属母公司股东的净利润/营业收入(TTM)_GSD
from windget import getNetProfitToOrTtM2


# 获取归属母公司股东的净利润/营业收入(TTM)_PIT时间序列
from windget import getFaNetProfitToOrTtMSeries


# 获取归属母公司股东的净利润/营业收入(TTM)_PIT
from windget import getFaNetProfitToOrTtM


# 获取利息收入合计时间序列
from windget import getStmNoteSec1510Series


# 获取利息收入合计
from windget import getStmNoteSec1510


# 获取利息收入:金融企业往来业务收入时间序列
from windget import getStmNoteSec1512Series


# 获取利息收入:金融企业往来业务收入
from windget import getStmNoteSec1512


# 获取利息收入_GSD时间序列
from windget import getWgsDIntIncSeries


# 获取利息收入_GSD
from windget import getWgsDIntInc


# 获取利息收入时间序列
from windget import getIntIncSeries


# 获取利息收入
from windget import getIntInc


# 获取利息收入_FUND时间序列
from windget import getStmIs80Series


# 获取利息收入_FUND
from windget import getStmIs80


# 获取非利息收入时间序列
from windget import getStmNoteBank411Series


# 获取非利息收入
from windget import getStmNoteBank411


# 获取非利息收入占比时间序列
from windget import getStmNoteBank30Series


# 获取非利息收入占比
from windget import getStmNoteBank30


# 获取贷款利息收入_总计时间序列
from windget import getStmNoteBank710Series


# 获取贷款利息收入_总计
from windget import getStmNoteBank710


# 获取贷款利息收入_企业贷款及垫款时间序列
from windget import getStmNoteBank721Series


# 获取贷款利息收入_企业贷款及垫款
from windget import getStmNoteBank721


# 获取贷款利息收入_个人贷款及垫款时间序列
from windget import getStmNoteBank722Series


# 获取贷款利息收入_个人贷款及垫款
from windget import getStmNoteBank722


# 获取贷款利息收入_票据贴现时间序列
from windget import getStmNoteBank723Series


# 获取贷款利息收入_票据贴现
from windget import getStmNoteBank723


# 获取贷款利息收入_个人住房贷款时间序列
from windget import getStmNoteBank724Series


# 获取贷款利息收入_个人住房贷款
from windget import getStmNoteBank724


# 获取贷款利息收入_个人消费贷款时间序列
from windget import getStmNoteBank725Series


# 获取贷款利息收入_个人消费贷款
from windget import getStmNoteBank725


# 获取贷款利息收入_信用卡应收账款时间序列
from windget import getStmNoteBank726Series


# 获取贷款利息收入_信用卡应收账款
from windget import getStmNoteBank726


# 获取贷款利息收入_经营性贷款时间序列
from windget import getStmNoteBank727Series


# 获取贷款利息收入_经营性贷款
from windget import getStmNoteBank727


# 获取贷款利息收入_汽车贷款时间序列
from windget import getStmNoteBank728Series


# 获取贷款利息收入_汽车贷款
from windget import getStmNoteBank728


# 获取贷款利息收入_其他个人贷款时间序列
from windget import getStmNoteBank729Series


# 获取贷款利息收入_其他个人贷款
from windget import getStmNoteBank729


# 获取贷款利息收入_信用贷款时间序列
from windget import getStmNoteBank781Series


# 获取贷款利息收入_信用贷款
from windget import getStmNoteBank781


# 获取贷款利息收入_保证贷款时间序列
from windget import getStmNoteBank782Series


# 获取贷款利息收入_保证贷款
from windget import getStmNoteBank782


# 获取贷款利息收入_抵押贷款时间序列
from windget import getStmNoteBank783Series


# 获取贷款利息收入_抵押贷款
from windget import getStmNoteBank783


# 获取贷款利息收入_质押贷款时间序列
from windget import getStmNoteBank784Series


# 获取贷款利息收入_质押贷款
from windget import getStmNoteBank784


# 获取贷款利息收入_短期贷款时间序列
from windget import getStmNoteBank841Series


# 获取贷款利息收入_短期贷款
from windget import getStmNoteBank841


# 获取贷款利息收入_中长期贷款时间序列
from windget import getStmNoteBank842Series


# 获取贷款利息收入_中长期贷款
from windget import getStmNoteBank842


# 获取存款利息收入_FUND时间序列
from windget import getStmIs6Series


# 获取存款利息收入_FUND
from windget import getStmIs6


# 获取债券利息收入_FUND时间序列
from windget import getStmIs5Series


# 获取债券利息收入_FUND
from windget import getStmIs5


# 获取其他利息收入_FUND时间序列
from windget import getStmIs76Series


# 获取其他利息收入_FUND
from windget import getStmIs76


# 获取单季度.利息收入_GSD时间序列
from windget import getWgsDQfaIntIncSeries


# 获取单季度.利息收入_GSD
from windget import getWgsDQfaIntInc


# 获取单季度.利息收入时间序列
from windget import getQfaInterestIncSeries


# 获取单季度.利息收入
from windget import getQfaInterestInc


# 获取财务费用:利息收入时间序列
from windget import getFinIntIncSeries


# 获取财务费用:利息收入
from windget import getFinIntInc


# 获取固定息证券投资利息收入时间序列
from windget import getStmNoteInvestmentIncome0001Series


# 获取固定息证券投资利息收入
from windget import getStmNoteInvestmentIncome0001


# 获取单季度.财务费用:利息收入时间序列
from windget import getQfaFinIntIncSeries


# 获取单季度.财务费用:利息收入
from windget import getQfaFinIntInc


# 获取已赚保费时间序列
from windget import getInSurPremUnearnedSeries


# 获取已赚保费
from windget import getInSurPremUnearned


# 获取净已赚保费_GSD时间序列
from windget import getWgsDPremiumsEarnedSeries


# 获取净已赚保费_GSD
from windget import getWgsDPremiumsEarned


# 获取单季度.已赚保费时间序列
from windget import getQfaInSurPremUnearnedSeries


# 获取单季度.已赚保费
from windget import getQfaInSurPremUnearned


# 获取单季度.净已赚保费_GSD时间序列
from windget import getWgsDQfaPremiumsEarnedSeries


# 获取单季度.净已赚保费_GSD
from windget import getWgsDQfaPremiumsEarned


# 获取手续费及佣金收入合计时间序列
from windget import getStmNoteSec1500Series


# 获取手续费及佣金收入合计
from windget import getStmNoteSec1500


# 获取手续费及佣金收入:证券经纪业务时间序列
from windget import getStmNoteSec1501Series


# 获取手续费及佣金收入:证券经纪业务
from windget import getStmNoteSec1501


# 获取手续费及佣金收入:证券承销业务时间序列
from windget import getStmNoteSec1503Series


# 获取手续费及佣金收入:证券承销业务
from windget import getStmNoteSec1503


# 获取手续费及佣金收入:保荐业务时间序列
from windget import getStmNoteSec1505Series


# 获取手续费及佣金收入:保荐业务
from windget import getStmNoteSec1505


# 获取手续费及佣金收入:投资咨询业务时间序列
from windget import getStmNoteSec1506Series


# 获取手续费及佣金收入:投资咨询业务
from windget import getStmNoteSec1506


# 获取手续费及佣金收入:期货经纪业务时间序列
from windget import getStmNoteSec1507Series


# 获取手续费及佣金收入:期货经纪业务
from windget import getStmNoteSec1507


# 获取手续费及佣金收入_GSD时间序列
from windget import getWgsDFeeComMIncSeries


# 获取手续费及佣金收入_GSD
from windget import getWgsDFeeComMInc


# 获取手续费及佣金收入时间序列
from windget import getHandlingChrGComMIncSeries


# 获取手续费及佣金收入
from windget import getHandlingChrGComMInc


# 获取单季度.手续费及佣金收入_GSD时间序列
from windget import getWgsDQfaFeeComMIncSeries


# 获取单季度.手续费及佣金收入_GSD
from windget import getWgsDQfaFeeComMInc


# 获取单季度.手续费及佣金收入时间序列
from windget import getQfaHandlingChrGComMIncSeries


# 获取单季度.手续费及佣金收入
from windget import getQfaHandlingChrGComMInc


# 获取保费业务收入时间序列
from windget import getToTPremIncSeries


# 获取保费业务收入
from windget import getToTPremInc


# 获取分保费收入时间序列
from windget import getReInSurIncSeries


# 获取分保费收入
from windget import getReInSurInc


# 获取单季度.分保费收入时间序列
from windget import getQfaReInSurIncSeries


# 获取单季度.分保费收入
from windget import getQfaReInSurInc


# 获取分出保费_GSD时间序列
from windget import getWgsDPremiumReInsurersSeries


# 获取分出保费_GSD
from windget import getWgsDPremiumReInsurers


# 获取分出保费时间序列
from windget import getPremCededSeries


# 获取分出保费
from windget import getPremCeded


# 获取单季度.分出保费_GSD时间序列
from windget import getWgsDQfaPremiumReInsurersSeries


# 获取单季度.分出保费_GSD
from windget import getWgsDQfaPremiumReInsurers


# 获取单季度.分出保费时间序列
from windget import getQfaPremCededSeries


# 获取单季度.分出保费
from windget import getQfaPremCeded


# 获取提取未到期责任准备金时间序列
from windget import getUnearnedPremRsRvWithdrawSeries


# 获取提取未到期责任准备金
from windget import getUnearnedPremRsRvWithdraw


# 获取单季度.提取未到期责任准备金时间序列
from windget import getQfaUnearnedPremRsRvSeries


# 获取单季度.提取未到期责任准备金
from windget import getQfaUnearnedPremRsRv


# 获取代理买卖证券业务净收入时间序列
from windget import getNetIncAgencyBusinessSeries


# 获取代理买卖证券业务净收入
from windget import getNetIncAgencyBusiness


# 获取单季度.代理买卖证券业务净收入时间序列
from windget import getQfaNetIncAgencyBusinessSeries


# 获取单季度.代理买卖证券业务净收入
from windget import getQfaNetIncAgencyBusiness


# 获取证券承销业务净收入时间序列
from windget import getNetIncUnderwritingBusinessSeries


# 获取证券承销业务净收入
from windget import getNetIncUnderwritingBusiness


# 获取单季度.证券承销业务净收入时间序列
from windget import getQfaNetIncUnderwritingBusinessSeries


# 获取单季度.证券承销业务净收入
from windget import getQfaNetIncUnderwritingBusiness


# 获取其他业务收入时间序列
from windget import getOtherOperIncSeries


# 获取其他业务收入
from windget import getOtherOperInc


# 获取其他业务收入(附注)时间序列
from windget import getStmNoteSeg1703Series


# 获取其他业务收入(附注)
from windget import getStmNoteSeg1703


# 获取单季度.其他业务收入时间序列
from windget import getQfaOtherOperIncSeries


# 获取单季度.其他业务收入
from windget import getQfaOtherOperInc


# 获取利息净收入合计时间序列
from windget import getStmNoteSec1530Series


# 获取利息净收入合计
from windget import getStmNoteSec1530


# 获取利息净收入:金融企业往来业务收入时间序列
from windget import getStmNoteSec1532Series


# 获取利息净收入:金融企业往来业务收入
from windget import getStmNoteSec1532


# 获取利息净收入_GSD时间序列
from windget import getWgsDIntIncNetSeries


# 获取利息净收入_GSD
from windget import getWgsDIntIncNet


# 获取利息净收入时间序列
from windget import getNetIntIncSeries


# 获取利息净收入
from windget import getNetIntInc


# 获取单季度.利息净收入_GSD时间序列
from windget import getWgsDQfaIntIncNetSeries


# 获取单季度.利息净收入_GSD
from windget import getWgsDQfaIntIncNet


# 获取单季度.利息净收入时间序列
from windget import getQfaNetIntIncSeries


# 获取单季度.利息净收入
from windget import getQfaNetIntInc


# 获取手续费及佣金净收入合计时间序列
from windget import getStmNoteSec1520Series


# 获取手续费及佣金净收入合计
from windget import getStmNoteSec1520


# 获取手续费及佣金净收入:证券经纪业务时间序列
from windget import getStmNoteSec1521Series


# 获取手续费及佣金净收入:证券经纪业务
from windget import getStmNoteSec1521


# 获取手续费及佣金净收入:证券承销业务时间序列
from windget import getStmNoteSec1523Series


# 获取手续费及佣金净收入:证券承销业务
from windget import getStmNoteSec1523


# 获取手续费及佣金净收入:保荐业务时间序列
from windget import getStmNoteSec1525Series


# 获取手续费及佣金净收入:保荐业务
from windget import getStmNoteSec1525


# 获取手续费及佣金净收入:投资咨询业务时间序列
from windget import getStmNoteSec1526Series


# 获取手续费及佣金净收入:投资咨询业务
from windget import getStmNoteSec1526


# 获取手续费及佣金净收入:期货经纪业务时间序列
from windget import getStmNoteSec1527Series


# 获取手续费及佣金净收入:期货经纪业务
from windget import getStmNoteSec1527


# 获取手续费及佣金净收入:其他业务时间序列
from windget import getStmNoteSec1554Series


# 获取手续费及佣金净收入:其他业务
from windget import getStmNoteSec1554


# 获取手续费及佣金净收入_GSD时间序列
from windget import getWgsDFeeComMIncNetSeries


# 获取手续费及佣金净收入_GSD
from windget import getWgsDFeeComMIncNet


# 获取手续费及佣金净收入时间序列
from windget import getNetFeeAndCommissionIncSeries


# 获取手续费及佣金净收入
from windget import getNetFeeAndCommissionInc


# 获取单季度.手续费及佣金净收入_GSD时间序列
from windget import getWgsDQfaFeeComMIncNetSeries


# 获取单季度.手续费及佣金净收入_GSD
from windget import getWgsDQfaFeeComMIncNet


# 获取单季度.手续费及佣金净收入时间序列
from windget import getQfaNetFeeAndCommissionIncSeries


# 获取单季度.手续费及佣金净收入
from windget import getQfaNetFeeAndCommissionInc


# 获取其他业务净收益时间序列
from windget import getNetOtherOperIncSeries


# 获取其他业务净收益
from windget import getNetOtherOperInc


# 获取单季度.其他业务净收益时间序列
from windget import getQfaNetOtherOperIncSeries


# 获取单季度.其他业务净收益
from windget import getQfaNetOtherOperInc


# 获取营业总成本(TTM)时间序列
from windget import getGcTtM2Series


# 获取营业总成本(TTM)
from windget import getGcTtM2


# 获取营业总成本(TTM)_GSD时间序列
from windget import getGcTtM3Series


# 获取营业总成本(TTM)_GSD
from windget import getGcTtM3


# 获取营业总成本时间序列
from windget import getStm07IsReItsSCostSeries


# 获取营业总成本
from windget import getStm07IsReItsSCost


# 获取营业总成本2时间序列
from windget import getOperatingCost2Series


# 获取营业总成本2
from windget import getOperatingCost2


# 获取营业总成本(TTM)_PIT时间序列
from windget import getFaGcTtMSeries


# 获取营业总成本(TTM)_PIT
from windget import getFaGcTtM


# 获取营业总成本(TTM,只有最新数据)时间序列
from windget import getGcTtMSeries


# 获取营业总成本(TTM,只有最新数据)
from windget import getGcTtM


# 获取单季度.营业总成本2时间序列
from windget import getQfaOperatingCost2Series


# 获取单季度.营业总成本2
from windget import getQfaOperatingCost2


# 获取单季度.营业总成本时间序列
from windget import getQfaToTOperCostSeries


# 获取单季度.营业总成本
from windget import getQfaToTOperCost


# 获取营业成本-非金融类(TTM)时间序列
from windget import getCostTtM2Series


# 获取营业成本-非金融类(TTM)
from windget import getCostTtM2


# 获取营业成本-非金融类(TTM)_GSD时间序列
from windget import getCostTtM3Series


# 获取营业成本-非金融类(TTM)_GSD
from windget import getCostTtM3


# 获取营业成本_GSD时间序列
from windget import getWgsDOperCostSeries


# 获取营业成本_GSD
from windget import getWgsDOperCost


# 获取营业成本时间序列
from windget import getStm07IsReItsCostSeries


# 获取营业成本
from windget import getStm07IsReItsCost


# 获取营业成本-非金融类(TTM)_PIT时间序列
from windget import getFaOcNfTtMSeries


# 获取营业成本-非金融类(TTM)_PIT
from windget import getFaOcNfTtM


# 获取营业成本-非金融类(TTM,只有最新数据)时间序列
from windget import getCostTtMSeries


# 获取营业成本-非金融类(TTM,只有最新数据)
from windget import getCostTtM


# 获取预测营业成本Surprise(可选类型)时间序列
from windget import getWestAvgOcSurpriseSeries


# 获取预测营业成本Surprise(可选类型)
from windget import getWestAvgOcSurprise


# 获取预测营业成本Surprise百分比(可选类型)时间序列
from windget import getWestAvgOcSurprisePctSeries


# 获取预测营业成本Surprise百分比(可选类型)
from windget import getWestAvgOcSurprisePct


# 获取一致预测营业成本(FY1)时间序列
from windget import getWestAvgOcFy1Series


# 获取一致预测营业成本(FY1)
from windget import getWestAvgOcFy1


# 获取一致预测营业成本(FY2)时间序列
from windget import getWestAvgOcFy2Series


# 获取一致预测营业成本(FY2)
from windget import getWestAvgOcFy2


# 获取一致预测营业成本(FY3)时间序列
from windget import getWestAvgOcFy3Series


# 获取一致预测营业成本(FY3)
from windget import getWestAvgOcFy3


# 获取单季度.营业成本_GSD时间序列
from windget import getWgsDQfaOperCostSeries


# 获取单季度.营业成本_GSD
from windget import getWgsDQfaOperCost


# 获取单季度.营业成本时间序列
from windget import getQfaOperCostSeries


# 获取单季度.营业成本
from windget import getQfaOperCost


# 获取利息支出(TTM)_GSD时间序列
from windget import getInterestExpenseTtM2Series


# 获取利息支出(TTM)_GSD
from windget import getInterestExpenseTtM2


# 获取利息支出_GSD时间序列
from windget import getWgsDIntExpSeries


# 获取利息支出_GSD
from windget import getWgsDIntExp


# 获取利息支出时间序列
from windget import getIntExpSeries


# 获取利息支出
from windget import getIntExp


# 获取利息支出_FUND时间序列
from windget import getStmIs72Series


# 获取利息支出_FUND
from windget import getStmIs72


# 获取利息支出(TTM)_PIT时间序列
from windget import getFaInterestExpenseTtMSeries


# 获取利息支出(TTM)_PIT
from windget import getFaInterestExpenseTtM


# 获取存款利息支出_存款总额时间序列
from windget import getStmNoteBank649Series


# 获取存款利息支出_存款总额
from windget import getStmNoteBank649


# 获取存款利息支出_个人定期存款时间序列
from windget import getStmNoteBank631Series


# 获取存款利息支出_个人定期存款
from windget import getStmNoteBank631


# 获取存款利息支出_个人活期存款时间序列
from windget import getStmNoteBank632Series


# 获取存款利息支出_个人活期存款
from windget import getStmNoteBank632


# 获取存款利息支出_公司定期存款时间序列
from windget import getStmNoteBank633Series


# 获取存款利息支出_公司定期存款
from windget import getStmNoteBank633


# 获取存款利息支出_公司活期存款时间序列
from windget import getStmNoteBank634Series


# 获取存款利息支出_公司活期存款
from windget import getStmNoteBank634


# 获取存款利息支出_其它存款时间序列
from windget import getStmNoteBank635Series


# 获取存款利息支出_其它存款
from windget import getStmNoteBank635


# 获取单季度.利息支出_GSD时间序列
from windget import getWgsDQfaIntExpSeries


# 获取单季度.利息支出_GSD
from windget import getWgsDQfaIntExp


# 获取单季度.利息支出时间序列
from windget import getQfaInterestExpSeries


# 获取单季度.利息支出
from windget import getQfaInterestExp


# 获取手续费及佣金支出时间序列
from windget import getHandlingChrGComMExpSeries


# 获取手续费及佣金支出
from windget import getHandlingChrGComMExp


# 获取单季度.手续费及佣金支出时间序列
from windget import getQfaHandlingChrGComMExpSeries


# 获取单季度.手续费及佣金支出
from windget import getQfaHandlingChrGComMExp


# 获取营业支出-金融类(TTM)时间序列
from windget import getExpenseTtM2Series


# 获取营业支出-金融类(TTM)
from windget import getExpenseTtM2


# 获取营业支出-金融类(TTM)_GSD时间序列
from windget import getExpenseTtM3Series


# 获取营业支出-金融类(TTM)_GSD
from windget import getExpenseTtM3


# 获取营业支出时间序列
from windget import getOperExpSeries


# 获取营业支出
from windget import getOperExp


# 获取营业支出-金融类(TTM)_PIT时间序列
from windget import getFaOEfTtMSeries


# 获取营业支出-金融类(TTM)_PIT
from windget import getFaOEfTtM


# 获取营业支出-金融类(TTM,只有最新数据)时间序列
from windget import getExpenseTtMSeries


# 获取营业支出-金融类(TTM,只有最新数据)
from windget import getExpenseTtM


# 获取总营业支出_GSD时间序列
from windget import getWgsDOperExpToTSeries


# 获取总营业支出_GSD
from windget import getWgsDOperExpToT


# 获取单季度.营业支出时间序列
from windget import getQfaOperExpSeries


# 获取单季度.营业支出
from windget import getQfaOperExp


# 获取单季度.总营业支出_GSD时间序列
from windget import getWgsDQfaOperExpToTSeries


# 获取单季度.总营业支出_GSD
from windget import getWgsDQfaOperExpToT


# 获取税金及附加时间序列
from windget import getStm07IsReItsTaxSeries


# 获取税金及附加
from windget import getStm07IsReItsTax


# 获取税金及附加_FUND时间序列
from windget import getStmIs26Series


# 获取税金及附加_FUND
from windget import getStmIs26


# 获取单季度.税金及附加时间序列
from windget import getQfaTaxesSurchargesOpsSeries


# 获取单季度.税金及附加
from windget import getQfaTaxesSurchargesOps


# 获取销售费用(TTM)时间序列
from windget import getOperateExpenseTtM2Series


# 获取销售费用(TTM)
from windget import getOperateExpenseTtM2


# 获取销售费用(TTM)_GSD时间序列
from windget import getOperateExpenseTtM3Series


# 获取销售费用(TTM)_GSD
from windget import getOperateExpenseTtM3


# 获取销售费用_GSD时间序列
from windget import getWgsDSalesExpSeries


# 获取销售费用_GSD
from windget import getWgsDSalesExp


# 获取销售费用时间序列
from windget import getStm07IsReItsSalesFeeSeries


# 获取销售费用
from windget import getStm07IsReItsSalesFee


# 获取销售费用(TTM)_PIT时间序列
from windget import getFaSellExpenseTtMSeries


# 获取销售费用(TTM)_PIT
from windget import getFaSellExpenseTtM


# 获取销售费用(TTM,只有最新数据)时间序列
from windget import getOperateExpenseTtMSeries


# 获取销售费用(TTM,只有最新数据)
from windget import getOperateExpenseTtM


# 获取单季度.销售费用时间序列
from windget import getQfaSellingDistExpSeries


# 获取单季度.销售费用
from windget import getQfaSellingDistExp


# 获取租赁费(销售费用)时间序列
from windget import getStmNoteOthers7630Series


# 获取租赁费(销售费用)
from windget import getStmNoteOthers7630


# 获取工资薪酬(销售费用)时间序列
from windget import getStmNoteOthers7626Series


# 获取工资薪酬(销售费用)
from windget import getStmNoteOthers7626


# 获取折旧摊销(销售费用)时间序列
from windget import getStmNoteOthers7628Series


# 获取折旧摊销(销售费用)
from windget import getStmNoteOthers7628


# 获取仓储运输费(销售费用)时间序列
from windget import getStmNoteOthers7632Series


# 获取仓储运输费(销售费用)
from windget import getStmNoteOthers7632


# 获取广告宣传推广费(销售费用)时间序列
from windget import getStmNoteOthers7633Series


# 获取广告宣传推广费(销售费用)
from windget import getStmNoteOthers7633


# 获取管理费用(TTM)时间序列
from windget import getAdminExpenseTtM2Series


# 获取管理费用(TTM)
from windget import getAdminExpenseTtM2


# 获取管理费用(TTM)_GSD时间序列
from windget import getAdminExpenseTtM3Series


# 获取管理费用(TTM)_GSD
from windget import getAdminExpenseTtM3


# 获取管理费用_GSD时间序列
from windget import getWgsDMgTExpSeries


# 获取管理费用_GSD
from windget import getWgsDMgTExp


# 获取管理费用时间序列
from windget import getStm07IsReItsManageFeeSeries


# 获取管理费用
from windget import getStm07IsReItsManageFee


# 获取管理费用(TTM)_PIT时间序列
from windget import getFaAdminExpenseTtMSeries


# 获取管理费用(TTM)_PIT
from windget import getFaAdminExpenseTtM


# 获取管理费用(TTM,只有最新数据)时间序列
from windget import getAdminExpenseTtMSeries


# 获取管理费用(TTM,只有最新数据)
from windget import getAdminExpenseTtM


# 获取单季度.管理费用时间序列
from windget import getQfaGerLAdminExpSeries


# 获取单季度.管理费用
from windget import getQfaGerLAdminExp


# 获取租赁费(管理费用)时间序列
from windget import getStmNoteOthers7631Series


# 获取租赁费(管理费用)
from windget import getStmNoteOthers7631


# 获取工资薪酬(管理费用)时间序列
from windget import getStmNoteOthers7627Series


# 获取工资薪酬(管理费用)
from windget import getStmNoteOthers7627


# 获取折旧摊销(管理费用)时间序列
from windget import getStmNoteOthers7629Series


# 获取折旧摊销(管理费用)
from windget import getStmNoteOthers7629


# 获取财务费用(TTM)时间序列
from windget import getFinaExpenseTtM2Series


# 获取财务费用(TTM)
from windget import getFinaExpenseTtM2


# 获取财务费用(TTM)_GSD时间序列
from windget import getFinaExpenseTtM3Series


# 获取财务费用(TTM)_GSD
from windget import getFinaExpenseTtM3


# 获取财务费用时间序列
from windget import getStm07IsReItsFinanceFeeSeries


# 获取财务费用
from windget import getStm07IsReItsFinanceFee


# 获取财务费用:利息费用时间序列
from windget import getFinIntExpSeries


# 获取财务费用:利息费用
from windget import getFinIntExp


# 获取财务费用_CS时间序列
from windget import getFinExpCsSeries


# 获取财务费用_CS
from windget import getFinExpCs


# 获取财务费用(TTM)_PIT时间序列
from windget import getFaFinaExpenseTtMSeries


# 获取财务费用(TTM)_PIT
from windget import getFaFinaExpenseTtM


# 获取财务费用(TTM,只有最新数据)时间序列
from windget import getFinaExpenseTtMSeries


# 获取财务费用(TTM,只有最新数据)
from windget import getFinaExpenseTtM


# 获取单季度.财务费用时间序列
from windget import getQfaFinExpIsSeries


# 获取单季度.财务费用
from windget import getQfaFinExpIs


# 获取单季度.财务费用:利息费用时间序列
from windget import getQfaFinIntExpSeries


# 获取单季度.财务费用:利息费用
from windget import getQfaFinIntExp


# 获取单季度.财务费用_CS时间序列
from windget import getQfaFinExpCsSeries


# 获取单季度.财务费用_CS
from windget import getQfaFinExpCs


# 获取信用减值损失时间序列
from windget import getCreditImpairLoss2Series


# 获取信用减值损失
from windget import getCreditImpairLoss2


# 获取单季度.信用减值损失时间序列
from windget import getQfaCreditImpairLoss2Series


# 获取单季度.信用减值损失
from windget import getQfaCreditImpairLoss2


# 获取退保金时间序列
from windget import getPrepaySurRSeries


# 获取退保金
from windget import getPrepaySurR


# 获取单季度.退保金时间序列
from windget import getQfaPrepaySurRSeries


# 获取单季度.退保金
from windget import getQfaPrepaySurR


# 获取赔付支出净额时间序列
from windget import getNetClaimExpSeries


# 获取赔付支出净额
from windget import getNetClaimExp


# 获取单季度.赔付支出净额时间序列
from windget import getQfaNetClaimExpSeries


# 获取单季度.赔付支出净额
from windget import getQfaNetClaimExp


# 获取提取保险责任准备金时间序列
from windget import getNetInSurContRsRvSeries


# 获取提取保险责任准备金
from windget import getNetInSurContRsRv


# 获取单季度.提取保险责任准备金时间序列
from windget import getQfaNetInSurContRsRvSeries


# 获取单季度.提取保险责任准备金
from windget import getQfaNetInSurContRsRv


# 获取保单红利支出时间序列
from windget import getDvdExpInsuredSeries


# 获取保单红利支出
from windget import getDvdExpInsured


# 获取单季度.保单红利支出时间序列
from windget import getQfaDvdExpInsuredSeries


# 获取单季度.保单红利支出
from windget import getQfaDvdExpInsured


# 获取分保费用时间序列
from windget import getReinsuranceExpSeries


# 获取分保费用
from windget import getReinsuranceExp


# 获取摊回分保费用时间序列
from windget import getReInSurExpRecoverableSeries


# 获取摊回分保费用
from windget import getReInSurExpRecoverable


# 获取单季度.分保费用时间序列
from windget import getQfaReinsuranceExpSeries


# 获取单季度.分保费用
from windget import getQfaReinsuranceExp


# 获取单季度.摊回分保费用时间序列
from windget import getQfaReInSurExpRecoverableSeries


# 获取单季度.摊回分保费用
from windget import getQfaReInSurExpRecoverable


# 获取摊回赔付支出时间序列
from windget import getClaimExpRecoverableSeries


# 获取摊回赔付支出
from windget import getClaimExpRecoverable


# 获取单季度.摊回赔付支出时间序列
from windget import getQfaClaimExpRecoverableSeries


# 获取单季度.摊回赔付支出
from windget import getQfaClaimExpRecoverable


# 获取摊回保险责任准备金时间序列
from windget import getInSurRsRvRecoverableSeries


# 获取摊回保险责任准备金
from windget import getInSurRsRvRecoverable


# 获取单季度.摊回保险责任准备金时间序列
from windget import getQfaInSurRsRvRecoverableSeries


# 获取单季度.摊回保险责任准备金
from windget import getQfaInSurRsRvRecoverable


# 获取其他业务成本时间序列
from windget import getOtherOperExpSeries


# 获取其他业务成本
from windget import getOtherOperExp


# 获取其他业务成本(附注)时间序列
from windget import getStmNoteSeg1704Series


# 获取其他业务成本(附注)
from windget import getStmNoteSeg1704


# 获取单季度.其他业务成本时间序列
from windget import getQfaOtherOperExpSeries


# 获取单季度.其他业务成本
from windget import getQfaOtherOperExp


# 获取其他经营净收益时间序列
from windget import getNetIncOtherOpsSeries


# 获取其他经营净收益
from windget import getNetIncOtherOps


# 获取单季度.其他经营净收益时间序列
from windget import getQfaNetIncOtherOpsSeries


# 获取单季度.其他经营净收益
from windget import getQfaNetIncOtherOps


# 获取公允价值变动净收益时间序列
from windget import getNetGainChgFvSeries


# 获取公允价值变动净收益
from windget import getNetGainChgFv


# 获取单季度.公允价值变动净收益时间序列
from windget import getQfaNetGainChgFvSeries


# 获取单季度.公允价值变动净收益
from windget import getQfaNetGainChgFv


# 获取投资净收益时间序列
from windget import getNetInvestIncSeries


# 获取投资净收益
from windget import getNetInvestInc


# 获取单季度.投资净收益时间序列
from windget import getQfaNetInvestIncSeries


# 获取单季度.投资净收益
from windget import getQfaNetInvestInc


# 获取净敞口套期收益时间序列
from windget import getNetExposureHedgeBenSeries


# 获取净敞口套期收益
from windget import getNetExposureHedgeBen


# 获取单季度.净敞口套期收益时间序列
from windget import getQfaNetExposureHedgeBenSeries


# 获取单季度.净敞口套期收益
from windget import getQfaNetExposureHedgeBen


# 获取汇兑净收益时间序列
from windget import getNetGainFxTransSeries


# 获取汇兑净收益
from windget import getNetGainFxTrans


# 获取单季度.汇兑净收益时间序列
from windget import getQfaNetGainFxTransSeries


# 获取单季度.汇兑净收益
from windget import getQfaNetGainFxTrans


# 获取其他收益时间序列
from windget import getOtherGrantsIncSeries


# 获取其他收益
from windget import getOtherGrantsInc


# 获取单季度.其他收益时间序列
from windget import getQfaOtherGrantsIncSeries


# 获取单季度.其他收益
from windget import getQfaOtherGrantsInc


# 获取营业利润差额(特殊报表科目)时间序列
from windget import getOpProfitGapSeries


# 获取营业利润差额(特殊报表科目)
from windget import getOpProfitGap


# 获取营业利润差额说明(特殊报表科目)时间序列
from windget import getOpProfitGapDetailSeries


# 获取营业利润差额说明(特殊报表科目)
from windget import getOpProfitGapDetail


# 获取营业利润差额(合计平衡项目)时间序列
from windget import getOpProfitNettingSeries


# 获取营业利润差额(合计平衡项目)
from windget import getOpProfitNetting


# 获取营业利润率(OPM)预测机构家数(可选类型)时间序列
from windget import getWestInStNumOpMSeries


# 获取营业利润率(OPM)预测机构家数(可选类型)
from windget import getWestInStNumOpM


# 获取营业利润/利润总额(TTM)时间序列
from windget import getTaxToOrTtMSeries


# 获取营业利润/利润总额(TTM)
from windget import getTaxToOrTtM


# 获取营业利润(TTM)时间序列
from windget import getOpTtM2Series


# 获取营业利润(TTM)
from windget import getOpTtM2


# 获取营业利润/利润总额_GSD时间序列
from windget import getWgsDOpToEBTSeries


# 获取营业利润/利润总额_GSD
from windget import getWgsDOpToEBT


# 获取营业利润/利润总额(TTM)_GSD时间序列
from windget import getOpToEBTTtM2Series


# 获取营业利润/利润总额(TTM)_GSD
from windget import getOpToEBTTtM2


# 获取营业利润(TTM)_GSD时间序列
from windget import getOpTtM3Series


# 获取营业利润(TTM)_GSD
from windget import getOpTtM3


# 获取营业利润_GSD时间序列
from windget import getWgsDEbItOperSeries


# 获取营业利润_GSD
from windget import getWgsDEbItOper


# 获取营业利润时间序列
from windget import getStm07IsReItsProfitSeries


# 获取营业利润
from windget import getStm07IsReItsProfit


# 获取营业利润/利润总额(TTM)_PIT时间序列
from windget import getFaOpToPbtTtMSeries


# 获取营业利润/利润总额(TTM)_PIT
from windget import getFaOpToPbtTtM


# 获取营业利润(TTM)_PIT时间序列
from windget import getFaOpTtMSeries


# 获取营业利润(TTM)_PIT
from windget import getFaOpTtM


# 获取营业利润(TTM,只有最新数据)时间序列
from windget import getOpTtMSeries


# 获取营业利润(TTM,只有最新数据)
from windget import getOpTtM


# 获取非营业利润/利润总额(TTM)_GSD时间序列
from windget import getNonOpToEBTTtMSeries


# 获取非营业利润/利润总额(TTM)_GSD
from windget import getNonOpToEBTTtM


# 获取非营业利润(TTM)_GSD时间序列
from windget import getNonOpTtMSeries


# 获取非营业利润(TTM)_GSD
from windget import getNonOpTtM


# 获取预测营业利润率(OPM)平均值(可选类型)时间序列
from windget import getWestAvGoPmSeries


# 获取预测营业利润率(OPM)平均值(可选类型)
from windget import getWestAvGoPm


# 获取预测营业利润率(OPM)最大值(可选类型)时间序列
from windget import getWestMaxOpMSeries


# 获取预测营业利润率(OPM)最大值(可选类型)
from windget import getWestMaxOpM


# 获取预测营业利润率(OPM)最小值(可选类型)时间序列
from windget import getWestMinoPmSeries


# 获取预测营业利润率(OPM)最小值(可选类型)
from windget import getWestMinoPm


# 获取预测营业利润率(OPM)中值(可选类型)时间序列
from windget import getWestMediaOpMSeries


# 获取预测营业利润率(OPM)中值(可选类型)
from windget import getWestMediaOpM


# 获取预测营业利润率(OPM)标准差值(可选类型)时间序列
from windget import getWestStDoPmSeries


# 获取预测营业利润率(OPM)标准差值(可选类型)
from windget import getWestStDoPm


# 获取预测营业利润Surprise(可选类型)时间序列
from windget import getWestAvgOperatingProfitSurpriseSeries


# 获取预测营业利润Surprise(可选类型)
from windget import getWestAvgOperatingProfitSurprise


# 获取预测营业利润Surprise百分比(可选类型)时间序列
from windget import getWestAvgOperatingProfitSurprisePctSeries


# 获取预测营业利润Surprise百分比(可选类型)
from windget import getWestAvgOperatingProfitSurprisePct


# 获取每股营业利润_PIT时间序列
from windget import getFaOppSSeries


# 获取每股营业利润_PIT
from windget import getFaOppS


# 获取每股营业利润(TTM)_PIT时间序列
from windget import getFaOppSTtMSeries


# 获取每股营业利润(TTM)_PIT
from windget import getFaOppSTtM


# 获取一致预测营业利润(FY1)时间序列
from windget import getWestAvgOperatingProfitFy1Series


# 获取一致预测营业利润(FY1)
from windget import getWestAvgOperatingProfitFy1


# 获取一致预测营业利润(FY2)时间序列
from windget import getWestAvgOperatingProfitFy2Series


# 获取一致预测营业利润(FY2)
from windget import getWestAvgOperatingProfitFy2


# 获取一致预测营业利润(FY3)时间序列
from windget import getWestAvgOperatingProfitFy3Series


# 获取一致预测营业利润(FY3)
from windget import getWestAvgOperatingProfitFy3


# 获取单季度.营业利润_GSD时间序列
from windget import getWgsDQfaEbItOperSeries


# 获取单季度.营业利润_GSD
from windget import getWgsDQfaEbItOper


# 获取单季度.营业利润时间序列
from windget import getQfaOpProfitSeries


# 获取单季度.营业利润
from windget import getQfaOpProfit


# 获取营业外收入时间序列
from windget import getNonOperRevSeries


# 获取营业外收入
from windget import getNonOperRev


# 获取单季度.营业外收入时间序列
from windget import getQfaNonOperRevSeries


# 获取单季度.营业外收入
from windget import getQfaNonOperRev


# 获取政府补助_营业外收入时间序列
from windget import getStmNoteOthers4504Series


# 获取政府补助_营业外收入
from windget import getStmNoteOthers4504


# 获取营业外支出时间序列
from windget import getNonOperExpSeries


# 获取营业外支出
from windget import getNonOperExp


# 获取单季度.营业外支出时间序列
from windget import getQfaNonOperExpSeries


# 获取单季度.营业外支出
from windget import getQfaNonOperExp


# 获取利润总额差额(特殊报表科目)时间序列
from windget import getProfitGapSeries


# 获取利润总额差额(特殊报表科目)
from windget import getProfitGap


# 获取利润总额差额说明(特殊报表科目)时间序列
from windget import getProfitGapDetailSeries


# 获取利润总额差额说明(特殊报表科目)
from windget import getProfitGapDetail


# 获取利润总额差额(合计平衡项目)时间序列
from windget import getProfitNettingSeries


# 获取利润总额差额(合计平衡项目)
from windget import getProfitNetting


# 获取利润总额(TTM)时间序列
from windget import getEBtTtM2Series


# 获取利润总额(TTM)
from windget import getEBtTtM2


# 获取利润总额(TTM)_GSD时间序列
from windget import getEBtTtM3Series


# 获取利润总额(TTM)_GSD
from windget import getEBtTtM3


# 获取利润总额时间序列
from windget import getStm07IsReItsSumProfitSeries


# 获取利润总额
from windget import getStm07IsReItsSumProfit


# 获取利润总额(TTM)_PIT时间序列
from windget import getFaEBtTtMSeries


# 获取利润总额(TTM)_PIT
from windget import getFaEBtTtM


# 获取利润总额(TTM,只有最新数据)时间序列
from windget import getEBtTtMSeries


# 获取利润总额(TTM,只有最新数据)
from windget import getEBtTtM


# 获取预测利润总额Surprise(可选类型)时间序列
from windget import getWestAvGebTSurpriseSeries


# 获取预测利润总额Surprise(可选类型)
from windget import getWestAvGebTSurprise


# 获取预测利润总额Surprise百分比(可选类型)时间序列
from windget import getWestAvGebTSurprisePctSeries


# 获取预测利润总额Surprise百分比(可选类型)
from windget import getWestAvGebTSurprisePct


# 获取税项/利润总额(TTM)时间序列
from windget import getTaxToEBTTtMSeries


# 获取税项/利润总额(TTM)
from windget import getTaxToEBTTtM


# 获取税项/利润总额_GSD时间序列
from windget import getWgsDTaxToEBTSeries


# 获取税项/利润总额_GSD
from windget import getWgsDTaxToEBT


# 获取税项/利润总额(TTM)_GSD时间序列
from windget import getTaxToEBTTtM2Series


# 获取税项/利润总额(TTM)_GSD
from windget import getTaxToEBTTtM2


# 获取税项/利润总额(TTM)_PIT时间序列
from windget import getFaTaxToProfitBtTtMSeries


# 获取税项/利润总额(TTM)_PIT
from windget import getFaTaxToProfitBtTtM


# 获取一致预测利润总额(FY1)时间序列
from windget import getWestAvGebTFy1Series


# 获取一致预测利润总额(FY1)
from windget import getWestAvGebTFy1


# 获取一致预测利润总额(FY2)时间序列
from windget import getWestAvGebTFy2Series


# 获取一致预测利润总额(FY2)
from windget import getWestAvGebTFy2


# 获取一致预测利润总额(FY3)时间序列
from windget import getWestAvGebTFy3Series


# 获取一致预测利润总额(FY3)
from windget import getWestAvGebTFy3


# 获取单季度.利润总额时间序列
from windget import getQfaToTProfitSeries


# 获取单季度.利润总额
from windget import getQfaToTProfit


# 获取未确认的投资损失_BS时间序列
from windget import getUnconfirmedInvestLossBsSeries


# 获取未确认的投资损失_BS
from windget import getUnconfirmedInvestLossBs


# 获取未确认的投资损失时间序列
from windget import getUnconfirmedInvestLossIsSeries


# 获取未确认的投资损失
from windget import getUnconfirmedInvestLossIs


# 获取未确认的投资损失_CS时间序列
from windget import getUnconfirmedInvestLossCsSeries


# 获取未确认的投资损失_CS
from windget import getUnconfirmedInvestLossCs


# 获取单季度.未确认的投资损失时间序列
from windget import getQfaUnconfirmedInvestLossIsSeries


# 获取单季度.未确认的投资损失
from windget import getQfaUnconfirmedInvestLossIs


# 获取单季度.未确认的投资损失_CS时间序列
from windget import getQfaUnconfirmedInvestLossCsSeries


# 获取单季度.未确认的投资损失_CS
from windget import getQfaUnconfirmedInvestLossCs


# 获取净利润差额(特殊报表科目)时间序列
from windget import getNetProfitIsGapSeries


# 获取净利润差额(特殊报表科目)
from windget import getNetProfitIsGap


# 获取净利润差额说明(特殊报表科目)时间序列
from windget import getNetProfitIsGapDetailSeries


# 获取净利润差额说明(特殊报表科目)
from windget import getNetProfitIsGapDetail


# 获取净利润差额(合计平衡项目)时间序列
from windget import getNetProfitIsNettingSeries


# 获取净利润差额(合计平衡项目)
from windget import getNetProfitIsNetting


# 获取净利润(TTM)_PIT时间序列
from windget import getFaProfitTtMSeries


# 获取净利润(TTM)_PIT
from windget import getFaProfitTtM


# 获取净利润(TTM)时间序列
from windget import getProfitTtM2Series


# 获取净利润(TTM)
from windget import getProfitTtM2


# 获取净利润(TTM)_GSD时间序列
from windget import getProfitTtM3Series


# 获取净利润(TTM)_GSD
from windget import getProfitTtM3


# 获取净利润(Non-GAAP)_GSD时间序列
from windget import getWgsDNoGaapProfitSeries


# 获取净利润(Non-GAAP)_GSD
from windget import getWgsDNoGaapProfit


# 获取净利润_GSD时间序列
from windget import getWgsDNetIncSeries


# 获取净利润_GSD
from windget import getWgsDNetInc


# 获取净利润_CS_GSD时间序列
from windget import getWgsDNetIncCfSeries


# 获取净利润_CS_GSD
from windget import getWgsDNetIncCf


# 获取净利润时间序列
from windget import getStm07IsReItsNetProfitSeries


# 获取净利润
from windget import getStm07IsReItsNetProfit


# 获取净利润_CS时间序列
from windget import getNetProfitCsSeries


# 获取净利润_CS
from windget import getNetProfitCs


# 获取净利润_FUND时间序列
from windget import getStmIs79Series


# 获取净利润_FUND
from windget import getStmIs79


# 获取净利润(合计)_FUND时间序列
from windget import getStmIs79TotalSeries


# 获取净利润(合计)_FUND
from windget import getStmIs79Total


# 获取备考净利润(FY0,并购后)时间序列
from windget import getManetProfitFy0Series


# 获取备考净利润(FY0,并购后)
from windget import getManetProfitFy0


# 获取备考净利润(FY1,并购后)时间序列
from windget import getManetProfitFy1Series


# 获取备考净利润(FY1,并购后)
from windget import getManetProfitFy1


# 获取备考净利润(FY2,并购后)时间序列
from windget import getManetProfitFy2Series


# 获取备考净利润(FY2,并购后)
from windget import getManetProfitFy2


# 获取备考净利润(FY3,并购后)时间序列
from windget import getManetProfitFy3Series


# 获取备考净利润(FY3,并购后)
from windget import getManetProfitFy3


# 获取预测净利润Surprise(可选类型)时间序列
from windget import getWestNetProfitSurpriseSeries


# 获取预测净利润Surprise(可选类型)
from windget import getWestNetProfitSurprise


# 获取预测净利润Surprise百分比(可选类型)时间序列
from windget import getWestNetProfitSurprisePctSeries


# 获取预测净利润Surprise百分比(可选类型)
from windget import getWestNetProfitSurprisePct


# 获取八季度净利润变化趋势_PIT时间序列
from windget import getFaEarnMom8QTrSeries


# 获取八季度净利润变化趋势_PIT
from windget import getFaEarnMom8QTr


# 获取一致预测净利润(FY1)时间序列
from windget import getWestNetProfitFy1Series


# 获取一致预测净利润(FY1)
from windget import getWestNetProfitFy1


# 获取一致预测净利润(FY2)时间序列
from windget import getWestNetProfitFy2Series


# 获取一致预测净利润(FY2)
from windget import getWestNetProfitFy2


# 获取一致预测净利润(FY3)时间序列
from windget import getWestNetProfitFy3Series


# 获取一致预测净利润(FY3)
from windget import getWestNetProfitFy3


# 获取持续经营净利润/税后利润(TTM)_GSD时间序列
from windget import getConnPToProfitTtMSeries


# 获取持续经营净利润/税后利润(TTM)_GSD
from windget import getConnPToProfitTtM


# 获取持续经营净利润(TTM)_GSD时间序列
from windget import getConnPTtMSeries


# 获取持续经营净利润(TTM)_GSD
from windget import getConnPTtM


# 获取单季度.净利润(Non-GAAP)_GSD时间序列
from windget import getWgsDQfaNoGaapProfitSeries


# 获取单季度.净利润(Non-GAAP)_GSD
from windget import getWgsDQfaNoGaapProfit


# 获取持续经营净利润_GSD时间序列
from windget import getWgsDContinueOperSeries


# 获取持续经营净利润_GSD
from windget import getWgsDContinueOper


# 获取单季度.净利润_GSD时间序列
from windget import getWgsDQfaNetIncSeries


# 获取单季度.净利润_GSD
from windget import getWgsDQfaNetInc


# 获取单季度.净利润_CS_GSD时间序列
from windget import getWgsDQfaNetIncCfSeries


# 获取单季度.净利润_CS_GSD
from windget import getWgsDQfaNetIncCf


# 获取持续经营净利润时间序列
from windget import getNetProfitContinuedSeries


# 获取持续经营净利润
from windget import getNetProfitContinued


# 获取终止经营净利润时间序列
from windget import getNetProfitDiscontinuedSeries


# 获取终止经营净利润
from windget import getNetProfitDiscontinued


# 获取单季度.净利润时间序列
from windget import getQfaNetProfitIsSeries


# 获取单季度.净利润
from windget import getQfaNetProfitIs


# 获取单季度.净利润_CS时间序列
from windget import getQfaNetProfitCsSeries


# 获取单季度.净利润_CS
from windget import getQfaNetProfitCs


# 获取本期实现净利润时间序列
from windget import getStmNoteProfitApr2Series


# 获取本期实现净利润
from windget import getStmNoteProfitApr2


# 获取一致预测净利润(FY1)变化率_1M_PIT时间序列
from windget import getWestNetProfitFy11MSeries


# 获取一致预测净利润(FY1)变化率_1M_PIT
from windget import getWestNetProfitFy11M


# 获取一致预测净利润(FY1)变化率_3M_PIT时间序列
from windget import getWestNetProfitFy13MSeries


# 获取一致预测净利润(FY1)变化率_3M_PIT
from windget import getWestNetProfitFy13M


# 获取一致预测净利润(FY1)变化率_6M_PIT时间序列
from windget import getWestNetProfitFy16MSeries


# 获取一致预测净利润(FY1)变化率_6M_PIT
from windget import getWestNetProfitFy16M


# 获取一致预测净利润(FY1)的变化_1M_PIT时间序列
from windget import getWestNetProfitFy1Chg1MSeries


# 获取一致预测净利润(FY1)的变化_1M_PIT
from windget import getWestNetProfitFy1Chg1M


# 获取一致预测净利润(FY1)的变化_3M_PIT时间序列
from windget import getWestNetProfitFy1Chg3MSeries


# 获取一致预测净利润(FY1)的变化_3M_PIT
from windget import getWestNetProfitFy1Chg3M


# 获取一致预测净利润(FY1)的变化_6M_PIT时间序列
from windget import getWestNetProfitFy1Chg6MSeries


# 获取一致预测净利润(FY1)的变化_6M_PIT
from windget import getWestNetProfitFy1Chg6M


# 获取一致预测净利润(FY1)标准差_PIT时间序列
from windget import getWestStdNetProfitFy1Series


# 获取一致预测净利润(FY1)标准差_PIT
from windget import getWestStdNetProfitFy1


# 获取一致预测净利润(FY1)最大与一致预测净利润(FY1)最小值的变化率_PIT时间序列
from windget import getWestNetProfitMaxMinFy1Series


# 获取一致预测净利润(FY1)最大与一致预测净利润(FY1)最小值的变化率_PIT
from windget import getWestNetProfitMaxMinFy1


# 获取非持续经营净利润(TTM)_GSD时间序列
from windget import getNonConnPTtMSeries


# 获取非持续经营净利润(TTM)_GSD
from windget import getNonConnPTtM


# 获取非持续经营净利润_GSD时间序列
from windget import getWgsDDiscOperSeries


# 获取非持续经营净利润_GSD
from windget import getWgsDDiscOper


# 获取归属普通股东净利润_GSD时间序列
from windget import getWgsDNetIncDilSeries


# 获取归属普通股东净利润_GSD
from windget import getWgsDNetIncDil


# 获取归属母公司股东的净利润(TTM)_VAL_PIT时间序列
from windget import getNetProfitTtMSeries


# 获取归属母公司股东的净利润(TTM)_VAL_PIT
from windget import getNetProfitTtM


# 获取归属母公司股东的净利润(TTM)时间序列
from windget import getNetProfitTtM2Series


# 获取归属母公司股东的净利润(TTM)
from windget import getNetProfitTtM2


# 获取归属母公司股东的净利润(TTM)_GSD时间序列
from windget import getNetProfitTtM3Series


# 获取归属母公司股东的净利润(TTM)_GSD
from windget import getNetProfitTtM3


# 获取扣除非经常损益后净利润_GSD时间序列
from windget import getWgsDDeductedProfitSeries


# 获取扣除非经常损益后净利润_GSD
from windget import getWgsDDeductedProfit


# 获取单季度.持续经营净利润_GSD时间序列
from windget import getWgsDQfaContinueOperSeries


# 获取单季度.持续经营净利润_GSD
from windget import getWgsDQfaContinueOper


# 获取归属母公司股东的净利润时间序列
from windget import getNpBelongToParComShSeries


# 获取归属母公司股东的净利润
from windget import getNpBelongToParComSh


# 获取单季度.持续经营净利润时间序列
from windget import getQfaNetProfitContinuedSeries


# 获取单季度.持续经营净利润
from windget import getQfaNetProfitContinued


# 获取单季度.终止经营净利润时间序列
from windget import getQfaNetProfitDiscontinuedSeries


# 获取单季度.终止经营净利润
from windget import getQfaNetProfitDiscontinued


# 获取归属母公司股东的净利润(TTM)_PIT时间序列
from windget import getFaNetProfitTtMSeries


# 获取归属母公司股东的净利润(TTM)_PIT
from windget import getFaNetProfitTtM


# 获取单季度.非持续经营净利润_GSD时间序列
from windget import getWgsDQfaDiscOperSeries


# 获取单季度.非持续经营净利润_GSD
from windget import getWgsDQfaDiscOper


# 获取单季度.归属普通股东净利润_GSD时间序列
from windget import getWgsDQfaNetIncDilSeries


# 获取单季度.归属普通股东净利润_GSD
from windget import getWgsDQfaNetIncDil


# 获取单季度.扣除非经常损益后净利润_GSD时间序列
from windget import getWgsDQfaDeductedProfitSeries


# 获取单季度.扣除非经常损益后净利润_GSD
from windget import getWgsDQfaDeductedProfit


# 获取单季度.归属母公司股东的净利润时间序列
from windget import getQfaNpBelongToParComShSeries


# 获取单季度.归属母公司股东的净利润
from windget import getQfaNpBelongToParComSh


# 获取本期经营活动产生的基金净值变动数(本期净利润)时间序列
from windget import getStmNavChange6Series


# 获取本期经营活动产生的基金净值变动数(本期净利润)
from windget import getStmNavChange6


# 获取少数股东损益(TTM)时间序列
from windget import getMinorityInterestTtMSeries


# 获取少数股东损益(TTM)
from windget import getMinorityInterestTtM


# 获取少数股东损益(TTM)_GSD时间序列
from windget import getMinorityInterestTtM2Series


# 获取少数股东损益(TTM)_GSD
from windget import getMinorityInterestTtM2


# 获取少数股东损益_GSD时间序列
from windget import getWgsDMinIntExpSeries


# 获取少数股东损益_GSD
from windget import getWgsDMinIntExp


# 获取少数股东损益时间序列
from windget import getMinorityIntIncSeries


# 获取少数股东损益
from windget import getMinorityIntInc


# 获取少数股东损益影响数时间序列
from windget import getStmNoteEoItems23Series


# 获取少数股东损益影响数
from windget import getStmNoteEoItems23


# 获取少数股东损益(TTM)_PIT时间序列
from windget import getFaMinInterestTtMSeries


# 获取少数股东损益(TTM)_PIT
from windget import getFaMinInterestTtM


# 获取单季度.少数股东损益_GSD时间序列
from windget import getWgsDQfaMinIntExpSeries


# 获取单季度.少数股东损益_GSD
from windget import getWgsDQfaMinIntExp


# 获取单季度.少数股东损益时间序列
from windget import getQfaMinorityIntIncSeries


# 获取单季度.少数股东损益
from windget import getQfaMinorityIntInc


# 获取基本每股收益_GSD时间序列
from windget import getWgsDEpsBasicSeries


# 获取基本每股收益_GSD
from windget import getWgsDEpsBasic


# 获取基本每股收益时间序列
from windget import getEpsBasicIsSeries


# 获取基本每股收益
from windget import getEpsBasicIs


# 获取基本每股收益_PIT时间序列
from windget import getFaEpsBasicSeries


# 获取基本每股收益_PIT
from windget import getFaEpsBasic


# 获取上年同期基本每股收益时间序列
from windget import getProfitNoticeLastYearBasicEarnSeries


# 获取上年同期基本每股收益
from windget import getProfitNoticeLastYearBasicEarn


# 获取单季度.基本每股收益EPS_GSD时间序列
from windget import getWgsDQfaEpsBasicSeries


# 获取单季度.基本每股收益EPS_GSD
from windget import getWgsDQfaEpsBasic


# 获取稀释每股收益_GSD时间序列
from windget import getWgsDEpsDilutedSeries


# 获取稀释每股收益_GSD
from windget import getWgsDEpsDiluted


# 获取稀释每股收益时间序列
from windget import getEpsDilutedIsSeries


# 获取稀释每股收益
from windget import getEpsDilutedIs


# 获取稀释每股收益_PIT时间序列
from windget import getFaEpsDilutedSeries


# 获取稀释每股收益_PIT
from windget import getFaEpsDiluted


# 获取单季度.稀释每股收益EPS_GSD时间序列
from windget import getWgsDQfaEpsDilutedSeries


# 获取单季度.稀释每股收益EPS_GSD
from windget import getWgsDQfaEpsDiluted


# 获取单季度.保费总收入时间序列
from windget import getQfaToTPremIncSeries


# 获取单季度.保费总收入
from windget import getQfaToTPremInc


# 获取单季度.毛利_GSD时间序列
from windget import getWgsDQfaGrossMargin2Series


# 获取单季度.毛利_GSD
from windget import getWgsDQfaGrossMargin2


# 获取单季度.毛利时间序列
from windget import getQfaGrossMarginSeries


# 获取单季度.毛利
from windget import getQfaGrossMargin


# 获取主营收入构成时间序列
from windget import getSegmentSalesSeries


# 获取主营收入构成
from windget import getSegmentSales


# 获取海外业务收入时间序列
from windget import getStmNoteSeg1501Series


# 获取海外业务收入
from windget import getStmNoteSeg1501


# 获取期初未分配利润时间序列
from windget import getStmNoteProfitApr1Series


# 获取期初未分配利润
from windget import getStmNoteProfitApr1


# 获取支付普通股股利时间序列
from windget import getStmNoteProfitApr4Series


# 获取支付普通股股利
from windget import getStmNoteProfitApr4


# 获取提取法定盈余公积时间序列
from windget import getStmNoteProfitApr5Series


# 获取提取法定盈余公积
from windget import getStmNoteProfitApr5


# 获取提取任意盈余公积时间序列
from windget import getStmNoteProfitApr6Series


# 获取提取任意盈余公积
from windget import getStmNoteProfitApr6


# 获取转增股本时间序列
from windget import getStmNoteProfitApr8Series


# 获取转增股本
from windget import getStmNoteProfitApr8


# 获取每股转增股本(已宣告)时间序列
from windget import getDivCapitalization2Series


# 获取每股转增股本(已宣告)
from windget import getDivCapitalization2


# 获取每股转增股本时间序列
from windget import getDivCapitalizationSeries


# 获取每股转增股本
from windget import getDivCapitalization


# 获取年末未分配利润时间序列
from windget import getStmNoteProfitApr9Series


# 获取年末未分配利润
from windget import getStmNoteProfitApr9


# 获取提取一般风险准备时间序列
from windget import getStmNoteProfitApr10Series


# 获取提取一般风险准备
from windget import getStmNoteProfitApr10


# 获取担保发生额合计时间序列
from windget import getStmNoteGuarantee1Series


# 获取担保发生额合计
from windget import getStmNoteGuarantee1


# 获取对控股子公司担保发生额合计时间序列
from windget import getStmNoteGuarantee4Series


# 获取对控股子公司担保发生额合计
from windget import getStmNoteGuarantee4


# 获取担保余额合计时间序列
from windget import getStmNoteGuarantee2Series


# 获取担保余额合计
from windget import getStmNoteGuarantee2


# 获取关联担保余额合计时间序列
from windget import getStmNoteGuarantee3Series


# 获取关联担保余额合计
from windget import getStmNoteGuarantee3


# 获取违规担保总额时间序列
from windget import getStmNoteGuarantee5Series


# 获取违规担保总额
from windget import getStmNoteGuarantee5


# 获取向关联方销售产品金额时间序列
from windget import getStmNoteAssociated1Series


# 获取向关联方销售产品金额
from windget import getStmNoteAssociated1


# 获取向关联方采购产品金额时间序列
from windget import getStmNoteAssociated2Series


# 获取向关联方采购产品金额
from windget import getStmNoteAssociated2


# 获取向关联方提供资金发生额时间序列
from windget import getStmNoteAssociated3Series


# 获取向关联方提供资金发生额
from windget import getStmNoteAssociated3


# 获取向关联方提供资金余额时间序列
from windget import getStmNoteAssociated4Series


# 获取向关联方提供资金余额
from windget import getStmNoteAssociated4


# 获取关联方向上市公司提供资金发生额时间序列
from windget import getStmNoteAssociated5Series


# 获取关联方向上市公司提供资金发生额
from windget import getStmNoteAssociated5


# 获取关联方向上市公司提供资金余额时间序列
from windget import getStmNoteAssociated6Series


# 获取关联方向上市公司提供资金余额
from windget import getStmNoteAssociated6


# 获取审计单位时间序列
from windget import getStmNoteAuditAgencySeries


# 获取审计单位
from windget import getStmNoteAuditAgency


# 获取内控_审计单位时间序列
from windget import getStmNoteInAuditAgencySeries


# 获取内控_审计单位
from windget import getStmNoteInAuditAgency


# 获取签字注册会计师时间序列
from windget import getStmNoteAuditCpaSeries


# 获取签字注册会计师
from windget import getStmNoteAuditCpa


# 获取当期实付审计费用时间序列
from windget import getStmNoteAuditExpenseSeries


# 获取当期实付审计费用
from windget import getStmNoteAuditExpense


# 获取审计报告披露日期时间序列
from windget import getStmNoteAuditDateSeries


# 获取审计报告披露日期
from windget import getStmNoteAuditDate


# 获取审计结果说明时间序列
from windget import getStmNoteAuditInterpretationSeries


# 获取审计结果说明
from windget import getStmNoteAuditInterpretation


# 获取内控_审计结果说明时间序列
from windget import getStmNoteInAuditInterpretationSeries


# 获取内控_审计结果说明
from windget import getStmNoteInAuditInterpretation


# 获取关键审计事项时间序列
from windget import getStmNoteAuditKamSeries


# 获取关键审计事项
from windget import getStmNoteAuditKam


# 获取内控_签字审计师时间序列
from windget import getStmNoteInAuditCpaSeries


# 获取内控_签字审计师
from windget import getStmNoteInAuditCpa


# 获取内控报告披露日期时间序列
from windget import getStmNoteInAuditIssuingDateSeries


# 获取内控报告披露日期
from windget import getStmNoteInAuditIssuingDate


# 获取存货明细-原材料时间序列
from windget import getStmNoteInv1Series


# 获取存货明细-原材料
from windget import getStmNoteInv1


# 获取存货明细-在产品时间序列
from windget import getStmNoteInv2Series


# 获取存货明细-在产品
from windget import getStmNoteInv2


# 获取存货明细-产成品时间序列
from windget import getStmNoteInv3Series


# 获取存货明细-产成品
from windget import getStmNoteInv3


# 获取存货明细-低值易耗品时间序列
from windget import getStmNoteInv4Series


# 获取存货明细-低值易耗品
from windget import getStmNoteInv4


# 获取存货明细-包装物时间序列
from windget import getStmNoteInv5Series


# 获取存货明细-包装物
from windget import getStmNoteInv5


# 获取存货明细-委托加工材料时间序列
from windget import getStmNoteInv6Series


# 获取存货明细-委托加工材料
from windget import getStmNoteInv6


# 获取存货明细-委托代销商品时间序列
from windget import getStmNoteInv7Series


# 获取存货明细-委托代销商品
from windget import getStmNoteInv7


# 获取存货明细-已加工未结算时间序列
from windget import getStmNoteInv8Series


# 获取存货明细-已加工未结算
from windget import getStmNoteInv8


# 获取存货明细-发出商品时间序列
from windget import getStmNoteInvGoodsShipSeries


# 获取存货明细-发出商品
from windget import getStmNoteInvGoodsShip


# 获取存货合计时间序列
from windget import getStmNoteInvToTSeries


# 获取存货合计
from windget import getStmNoteInvToT


# 获取应收账款余额时间序列
from windget import getStmNoteArTotalSeries


# 获取应收账款余额
from windget import getStmNoteArTotal


# 获取应收账款-金额时间序列
from windget import getStmNoteAr1Series


# 获取应收账款-金额
from windget import getStmNoteAr1


# 获取应收账款-比例时间序列
from windget import getStmNoteAr2Series


# 获取应收账款-比例
from windget import getStmNoteAr2


# 获取应收账款-坏账准备时间序列
from windget import getStmNoteAr3Series


# 获取应收账款-坏账准备
from windget import getStmNoteAr3


# 获取应收账款-坏账准备(按性质)时间序列
from windget import getStmNoteArCatSeries


# 获取应收账款-坏账准备(按性质)
from windget import getStmNoteArCat


# 获取应收账款-主要欠款人时间序列
from windget import getStmNoteArDebtorSeries


# 获取应收账款-主要欠款人
from windget import getStmNoteArDebtor


# 获取应收账款-主要欠款人名称时间序列
from windget import getStmNoteArDebtorNameSeries


# 获取应收账款-主要欠款人名称
from windget import getStmNoteArDebtorName


# 获取其他应收款-金额时间序列
from windget import getStmNoteOrSeries


# 获取其他应收款-金额
from windget import getStmNoteOr


# 获取坏账准备合计时间序列
from windget import getStmNoteReserve1Series


# 获取坏账准备合计
from windget import getStmNoteReserve1


# 获取坏账准备-应收账款时间序列
from windget import getStmNoteReserve2Series


# 获取坏账准备-应收账款
from windget import getStmNoteReserve2


# 获取坏账准备-其它应收款时间序列
from windget import getStmNoteReserve3Series


# 获取坏账准备-其它应收款
from windget import getStmNoteReserve3


# 获取短期投资跌价准备合计时间序列
from windget import getStmNoteReserve4Series


# 获取短期投资跌价准备合计
from windget import getStmNoteReserve4


# 获取短期投资跌价准备-股票投资时间序列
from windget import getStmNoteReserve5Series


# 获取短期投资跌价准备-股票投资
from windget import getStmNoteReserve5


# 获取短期投资跌价准备-债券投资时间序列
from windget import getStmNoteReserve6Series


# 获取短期投资跌价准备-债券投资
from windget import getStmNoteReserve6


# 获取存货跌价准备合计时间序列
from windget import getStmNoteReserve7Series


# 获取存货跌价准备合计
from windget import getStmNoteReserve7


# 获取存货跌价准备-库存商品时间序列
from windget import getStmNoteReserve8Series


# 获取存货跌价准备-库存商品
from windget import getStmNoteReserve8


# 获取存货跌价准备-原材料时间序列
from windget import getStmNoteReserve9Series


# 获取存货跌价准备-原材料
from windget import getStmNoteReserve9


# 获取存货跌价准备-产成品时间序列
from windget import getStmNoteReserve10Series


# 获取存货跌价准备-产成品
from windget import getStmNoteReserve10


# 获取存货跌价准备-低值易耗品时间序列
from windget import getStmNoteReserve11Series


# 获取存货跌价准备-低值易耗品
from windget import getStmNoteReserve11


# 获取存货跌价准备-开发成本时间序列
from windget import getStmNoteReserve12Series


# 获取存货跌价准备-开发成本
from windget import getStmNoteReserve12


# 获取存货跌价准备-包装物时间序列
from windget import getStmNoteReserve13Series


# 获取存货跌价准备-包装物
from windget import getStmNoteReserve13


# 获取存货跌价准备-在途物资时间序列
from windget import getStmNoteReserve14Series


# 获取存货跌价准备-在途物资
from windget import getStmNoteReserve14


# 获取存货跌价准备-在产品时间序列
from windget import getStmNoteReserve15Series


# 获取存货跌价准备-在产品
from windget import getStmNoteReserve15


# 获取存货跌价准备-开发产品时间序列
from windget import getStmNoteReserve16Series


# 获取存货跌价准备-开发产品
from windget import getStmNoteReserve16


# 获取存货跌价准备-自制半成品时间序列
from windget import getStmNoteReserve17Series


# 获取存货跌价准备-自制半成品
from windget import getStmNoteReserve17


# 获取长期投资减值准备合计时间序列
from windget import getStmNoteReserve18Series


# 获取长期投资减值准备合计
from windget import getStmNoteReserve18


# 获取长期投资减值准备-长期股权投资时间序列
from windget import getStmNoteReserve19Series


# 获取长期投资减值准备-长期股权投资
from windget import getStmNoteReserve19


# 获取长期投资减值准备-长期债权投资时间序列
from windget import getStmNoteReserve20Series


# 获取长期投资减值准备-长期债权投资
from windget import getStmNoteReserve20


# 获取在建工程减值准备时间序列
from windget import getStmNoteReserve35Series


# 获取在建工程减值准备
from windget import getStmNoteReserve35


# 获取委托贷款减值准备时间序列
from windget import getStmNoteReserve36Series


# 获取委托贷款减值准备
from windget import getStmNoteReserve36


# 获取自营证券跌价准备时间序列
from windget import getStmNoteReserve37Series


# 获取自营证券跌价准备
from windget import getStmNoteReserve37


# 获取贷款呆账准备时间序列
from windget import getStmNoteReserve38Series


# 获取贷款呆账准备
from windget import getStmNoteReserve38


# 获取投资性房地产-原值时间序列
from windget import getStmNoteAssetDetail5Series


# 获取投资性房地产-原值
from windget import getStmNoteAssetDetail5


# 获取投资性房地产-累计折旧时间序列
from windget import getStmNoteAssetDetail6Series


# 获取投资性房地产-累计折旧
from windget import getStmNoteAssetDetail6


# 获取投资性房地产-减值准备时间序列
from windget import getStmNoteAssetDetail7Series


# 获取投资性房地产-减值准备
from windget import getStmNoteAssetDetail7


# 获取投资性房地产-净额时间序列
from windget import getStmNoteAssetDetail8Series


# 获取投资性房地产-净额
from windget import getStmNoteAssetDetail8


# 获取存放中央银行法定准备金时间序列
from windget import getStmNoteCashDeposits1Series


# 获取存放中央银行法定准备金
from windget import getStmNoteCashDeposits1


# 获取存放中央银行超额存款准备金时间序列
from windget import getStmNoteCashDeposits2Series


# 获取存放中央银行超额存款准备金
from windget import getStmNoteCashDeposits2


# 获取人民币存款时间序列
from windget import getStmNoteDpsT4405Series


# 获取人民币存款
from windget import getStmNoteDpsT4405


# 获取美元存款(折算人民币)时间序列
from windget import getStmNoteDpsT4406Series


# 获取美元存款(折算人民币)
from windget import getStmNoteDpsT4406


# 获取日元存款(折算人民币)时间序列
from windget import getStmNoteDpsT4407Series


# 获取日元存款(折算人民币)
from windget import getStmNoteDpsT4407


# 获取欧元存款(折算人民币)时间序列
from windget import getStmNoteDpsT4408Series


# 获取欧元存款(折算人民币)
from windget import getStmNoteDpsT4408


# 获取港币存款(折算人民币)时间序列
from windget import getStmNoteDpsT4409Series


# 获取港币存款(折算人民币)
from windget import getStmNoteDpsT4409


# 获取英镑存款(折算人民币)时间序列
from windget import getStmNoteDpsT4410Series


# 获取英镑存款(折算人民币)
from windget import getStmNoteDpsT4410


# 获取其他货币存款(折算人民币)时间序列
from windget import getStmNoteDpsT4411Series


# 获取其他货币存款(折算人民币)
from windget import getStmNoteDpsT4411


# 获取一年内到期的应付债券时间序列
from windget import getStmNoteOthers7637Series


# 获取一年内到期的应付债券
from windget import getStmNoteOthers7637


# 获取税收返还、减免时间序列
from windget import getStmNoteEoItems7Series


# 获取税收返还、减免
from windget import getStmNoteEoItems7


# 获取政府补助时间序列
from windget import getStmNoteEoItems8Series


# 获取政府补助
from windget import getStmNoteEoItems8


# 获取资金占用费时间序列
from windget import getStmNoteEoItems9Series


# 获取资金占用费
from windget import getStmNoteEoItems9


# 获取企业合并产生的损益时间序列
from windget import getStmNoteEoItems10Series


# 获取企业合并产生的损益
from windget import getStmNoteEoItems10


# 获取委托投资损益时间序列
from windget import getStmNoteEoItems12Series


# 获取委托投资损益
from windget import getStmNoteEoItems12


# 获取债务重组损益时间序列
from windget import getStmNoteEoItems14Series


# 获取债务重组损益
from windget import getStmNoteEoItems14


# 获取企业重组费用时间序列
from windget import getStmNoteEoItems15Series


# 获取企业重组费用
from windget import getStmNoteEoItems15


# 获取交易产生的损益时间序列
from windget import getStmNoteEoItems16Series


# 获取交易产生的损益
from windget import getStmNoteEoItems16


# 获取同一控制下企业合并产生的子公司当期净损益时间序列
from windget import getStmNoteEoItems17Series


# 获取同一控制下企业合并产生的子公司当期净损益
from windget import getStmNoteEoItems17


# 获取单独进行减值测试的应收款项减值准备转回时间序列
from windget import getStmNoteEoItems29Series


# 获取单独进行减值测试的应收款项减值准备转回
from windget import getStmNoteEoItems29


# 获取对外委托贷款取得的收益时间序列
from windget import getStmNoteEoItems30Series


# 获取对外委托贷款取得的收益
from windget import getStmNoteEoItems30


# 获取公允价值法计量的投资性房地产价值变动损益时间序列
from windget import getStmNoteEoItems31Series


# 获取公允价值法计量的投资性房地产价值变动损益
from windget import getStmNoteEoItems31


# 获取法规要求一次性损益调整影响时间序列
from windget import getStmNoteEoItems32Series


# 获取法规要求一次性损益调整影响
from windget import getStmNoteEoItems32


# 获取受托经营取得的托管费收入时间序列
from windget import getStmNoteEoItems33Series


# 获取受托经营取得的托管费收入
from windget import getStmNoteEoItems33


# 获取其他营业外收支净额时间序列
from windget import getStmNoteEoItems19Series


# 获取其他营业外收支净额
from windget import getStmNoteEoItems19


# 获取中国证监会认定的其他项目时间序列
from windget import getStmNoteEoItems20Series


# 获取中国证监会认定的其他项目
from windget import getStmNoteEoItems20


# 获取坏账损失时间序列
from windget import getStmNoteImpairmentLoss4Series


# 获取坏账损失
from windget import getStmNoteImpairmentLoss4


# 获取存货跌价损失时间序列
from windget import getStmNoteImpairmentLoss5Series


# 获取存货跌价损失
from windget import getStmNoteImpairmentLoss5


# 获取发放贷款和垫款减值损失时间序列
from windget import getStmNoteImpairmentLoss7Series


# 获取发放贷款和垫款减值损失
from windget import getStmNoteImpairmentLoss7


# 获取持有至到期投资减值损失时间序列
from windget import getStmNoteImpairmentLoss9Series


# 获取持有至到期投资减值损失
from windget import getStmNoteImpairmentLoss9


# 获取本期费用化研发支出时间序列
from windget import getStmNoteRdExpCostSeries


# 获取本期费用化研发支出
from windget import getStmNoteRdExpCost


# 获取本期资本化研发支出时间序列
from windget import getStmNoteRdExpCapitalSeries


# 获取本期资本化研发支出
from windget import getStmNoteRdExpCapital


# 获取研发支出合计时间序列
from windget import getStmNoteRdExpSeries


# 获取研发支出合计
from windget import getStmNoteRdExp


# 获取研发人员数量时间序列
from windget import getStmNoteRdEmployeeSeries


# 获取研发人员数量
from windget import getStmNoteRdEmployee


# 获取研发人员数量占比时间序列
from windget import getStmNoteRdEmployeePctSeries


# 获取研发人员数量占比
from windget import getStmNoteRdEmployeePct


# 获取转融通融入资金时间序列
from windget import getStmNoteLoans1Series


# 获取转融通融入资金
from windget import getStmNoteLoans1


# 获取大客户名称时间序列
from windget import getStmNoteCustomerTop5Series


# 获取大客户名称
from windget import getStmNoteCustomerTop5


# 获取大客户销售收入时间序列
from windget import getStmNoteSalesTop5Series


# 获取大客户销售收入
from windget import getStmNoteSalesTop5


# 获取大客户销售收入占比时间序列
from windget import getStmNoteSalesPctTop5Series


# 获取大客户销售收入占比
from windget import getStmNoteSalesPctTop5


# 获取前五大客户销售收入总额时间序列
from windget import getStmNoteSalesTop5Series


# 获取前五大客户销售收入总额
from windget import getStmNoteSalesTop5


# 获取前五大客户销售收入占比时间序列
from windget import getStmNoteSalesTop5PctSeries


# 获取前五大客户销售收入占比
from windget import getStmNoteSalesTop5Pct


# 获取大供应商名称时间序列
from windget import getStmNoteSupplierTop5Series


# 获取大供应商名称
from windget import getStmNoteSupplierTop5


# 获取大供应商采购金额时间序列
from windget import getStmNotePurchaseTop5Series


# 获取大供应商采购金额
from windget import getStmNotePurchaseTop5


# 获取大供应商采购金额占比时间序列
from windget import getStmNotePurchasePctTop5Series


# 获取大供应商采购金额占比
from windget import getStmNotePurchasePctTop5


# 获取前五大供应商采购金额总额时间序列
from windget import getStmNotePurchaseTop5Series


# 获取前五大供应商采购金额总额
from windget import getStmNotePurchaseTop5


# 获取前五大供应商采购金额占比时间序列
from windget import getStmNotePurchaseTop5PctSeries


# 获取前五大供应商采购金额占比
from windget import getStmNotePurchaseTop5Pct


# 获取工资、奖金、津贴和补贴:本期增加时间序列
from windget import getStmNoteBenAddSeries


# 获取工资、奖金、津贴和补贴:本期增加
from windget import getStmNoteBenAdd


# 获取工资、奖金、津贴和补贴:期初余额时间序列
from windget import getStmNoteBenSbSeries


# 获取工资、奖金、津贴和补贴:期初余额
from windget import getStmNoteBenSb


# 获取工资、奖金、津贴和补贴:期末余额时间序列
from windget import getStmNoteBenEbSeries


# 获取工资、奖金、津贴和补贴:期末余额
from windget import getStmNoteBenEb


# 获取工资、奖金、津贴和补贴:本期减少时间序列
from windget import getStmNoteBenDeSeries


# 获取工资、奖金、津贴和补贴:本期减少
from windget import getStmNoteBenDe


# 获取工会经费和职工教育经费:本期增加时间序列
from windget import getStmNoteEduAndUnionFundsAddSeries


# 获取工会经费和职工教育经费:本期增加
from windget import getStmNoteEduAndUnionFundsAdd


# 获取工会经费和职工教育经费:期初余额时间序列
from windget import getStmNoteEduAndUnionFundsSbSeries


# 获取工会经费和职工教育经费:期初余额
from windget import getStmNoteEduAndUnionFundsSb


# 获取工会经费和职工教育经费:期末余额时间序列
from windget import getStmNoteEduAndUnionFundsEbSeries


# 获取工会经费和职工教育经费:期末余额
from windget import getStmNoteEduAndUnionFundsEb


# 获取工会经费和职工教育经费:本期减少时间序列
from windget import getStmNoteEduAndUnionFundsDeSeries


# 获取工会经费和职工教育经费:本期减少
from windget import getStmNoteEduAndUnionFundsDe


# 获取职工福利费:本期增加时间序列
from windget import getStmNoteWelfareAddSeries


# 获取职工福利费:本期增加
from windget import getStmNoteWelfareAdd


# 获取职工福利费:期初余额时间序列
from windget import getStmNoteWelfareSbSeries


# 获取职工福利费:期初余额
from windget import getStmNoteWelfareSb


# 获取职工福利费:期末余额时间序列
from windget import getStmNoteWelfareEbSeries


# 获取职工福利费:期末余额
from windget import getStmNoteWelfareEb


# 获取职工福利费:本期减少时间序列
from windget import getStmNoteWelfareDeSeries


# 获取职工福利费:本期减少
from windget import getStmNoteWelfareDe


# 获取住房公积金:本期增加时间序列
from windget import getStmNoteHousingFundAddSeries


# 获取住房公积金:本期增加
from windget import getStmNoteHousingFundAdd


# 获取住房公积金:期初余额时间序列
from windget import getStmNoteHousingFundSbSeries


# 获取住房公积金:期初余额
from windget import getStmNoteHousingFundSb


# 获取住房公积金:期末余额时间序列
from windget import getStmNoteHousingFundEbSeries


# 获取住房公积金:期末余额
from windget import getStmNoteHousingFundEb


# 获取住房公积金:本期减少时间序列
from windget import getStmNoteHousingFundDeSeries


# 获取住房公积金:本期减少
from windget import getStmNoteHousingFundDe


# 获取基本养老保险:本期增加时间序列
from windget import getStmNoteBasicPenAddSeries


# 获取基本养老保险:本期增加
from windget import getStmNoteBasicPenAdd


# 获取基本养老保险:期初余额时间序列
from windget import getStmNoteBasicPenSbSeries


# 获取基本养老保险:期初余额
from windget import getStmNoteBasicPenSb


# 获取基本养老保险:期末余额时间序列
from windget import getStmNoteBasicPenEbSeries


# 获取基本养老保险:期末余额
from windget import getStmNoteBasicPenEb


# 获取基本养老保险:本期减少时间序列
from windget import getStmNoteBasicPenDeSeries


# 获取基本养老保险:本期减少
from windget import getStmNoteBasicPenDe


# 获取生育保险费:本期增加时间序列
from windget import getStmNoteMaternityInSAddSeries


# 获取生育保险费:本期增加
from windget import getStmNoteMaternityInSAdd


# 获取生育保险费:期初余额时间序列
from windget import getStmNoteMaternityInSSbSeries


# 获取生育保险费:期初余额
from windget import getStmNoteMaternityInSSb


# 获取生育保险费:期末余额时间序列
from windget import getStmNoteMaternityInSEbSeries


# 获取生育保险费:期末余额
from windget import getStmNoteMaternityInSEb


# 获取生育保险费:本期减少时间序列
from windget import getStmNoteMaternityInSDeSeries


# 获取生育保险费:本期减少
from windget import getStmNoteMaternityInSDe


# 获取失业保险费:本期增加时间序列
from windget import getStmNoteUneMplInSAddSeries


# 获取失业保险费:本期增加
from windget import getStmNoteUneMplInSAdd


# 获取失业保险费:期初余额时间序列
from windget import getStmNoteUneMplInSSbSeries


# 获取失业保险费:期初余额
from windget import getStmNoteUneMplInSSb


# 获取失业保险费:期末余额时间序列
from windget import getStmNoteUneMplInSEbSeries


# 获取失业保险费:期末余额
from windget import getStmNoteUneMplInSEb


# 获取失业保险费:本期减少时间序列
from windget import getStmNoteUneMplInSDeSeries


# 获取失业保险费:本期减少
from windget import getStmNoteUneMplInSDe


# 获取医疗保险费:本期增加时间序列
from windget import getStmNoteMedInSAddSeries


# 获取医疗保险费:本期增加
from windget import getStmNoteMedInSAdd


# 获取医疗保险费:期初余额时间序列
from windget import getStmNoteMedInSSbSeries


# 获取医疗保险费:期初余额
from windget import getStmNoteMedInSSb


# 获取医疗保险费:期末余额时间序列
from windget import getStmNoteMedInSEbSeries


# 获取医疗保险费:期末余额
from windget import getStmNoteMedInSEb


# 获取医疗保险费:本期减少时间序列
from windget import getStmNoteMedInSDeSeries


# 获取医疗保险费:本期减少
from windget import getStmNoteMedInSDe


# 获取工伤保险费:本期增加时间序列
from windget import getStmNoteEMplInjuryInSAddSeries


# 获取工伤保险费:本期增加
from windget import getStmNoteEMplInjuryInSAdd


# 获取工伤保险费:期初余额时间序列
from windget import getStmNoteEMplInjuryInSSbSeries


# 获取工伤保险费:期初余额
from windget import getStmNoteEMplInjuryInSSb


# 获取工伤保险费:期末余额时间序列
from windget import getStmNoteEMplInjuryInSEbSeries


# 获取工伤保险费:期末余额
from windget import getStmNoteEMplInjuryInSEb


# 获取工伤保险费:本期减少时间序列
from windget import getStmNoteEMplInjuryInSDeSeries


# 获取工伤保险费:本期减少
from windget import getStmNoteEMplInjuryInSDe


# 获取消费税时间序列
from windget import getStmNoteTaxConsumptionSeries


# 获取消费税
from windget import getStmNoteTaxConsumption


# 获取城建税时间序列
from windget import getStmNoteTaxConstructionSeries


# 获取城建税
from windget import getStmNoteTaxConstruction


# 获取教育费附加时间序列
from windget import getStmNoteTaxEdeSupplementTarYSeries


# 获取教育费附加
from windget import getStmNoteTaxEdeSupplementTarY


# 获取土地使用税时间序列
from windget import getStmNoteTaxUrbanLandUseSeries


# 获取土地使用税
from windget import getStmNoteTaxUrbanLandUse


# 获取房产税时间序列
from windget import getStmNoteTaxBuildingSeries


# 获取房产税
from windget import getStmNoteTaxBuilding


# 获取印花税时间序列
from windget import getStmNoteTaxStampSeries


# 获取印花税
from windget import getStmNoteTaxStamp


# 获取单季度.基金利润时间序列
from windget import getQAnalIncomeSeries


# 获取单季度.基金利润
from windget import getQAnalIncome


# 获取单季度.基金利润(合计)时间序列
from windget import getQAnalTotalIncomeSeries


# 获取单季度.基金利润(合计)
from windget import getQAnalTotalIncome


# 获取单季度.报告期利润扣减当期公允价值变动损益后的净额时间序列
from windget import getQAnalDeCuteDNetIncomeSeries


# 获取单季度.报告期利润扣减当期公允价值变动损益后的净额
from windget import getQAnalDeCuteDNetIncome


# 获取单季度.超额收益率时间序列
from windget import getQAnalBenchDevReturnSeries


# 获取单季度.超额收益率
from windget import getQAnalBenchDevReturn


# 获取单季度.超额收益率标准差时间序列
from windget import getQAnalStdBenchDevReturnSeries


# 获取单季度.超额收益率标准差
from windget import getQAnalStdBenchDevReturn


# 获取报告期利润时间序列
from windget import getAnalIncomeSeries


# 获取报告期利润
from windget import getAnalIncome


# 获取报告期利润扣减当期公允价值变动损益后的净额时间序列
from windget import getAnalNetIncomeSeries


# 获取报告期利润扣减当期公允价值变动损益后的净额
from windget import getAnalNetIncome


# 获取报告期加权平均份额利润时间序列
from windget import getAnalAvgNetIncomePerUnitSeries


# 获取报告期加权平均份额利润
from windget import getAnalAvgNetIncomePerUnit


# 获取报告期末可供分配基金利润时间序列
from windget import getAnalDIsTriButAbleSeries


# 获取报告期末可供分配基金利润
from windget import getAnalDIsTriButAble


# 获取基金加权平均净值利润率时间序列
from windget import getAnalAvgNavReturnSeries


# 获取基金加权平均净值利润率
from windget import getAnalAvgNavReturn


# 获取基金申购款时间序列
from windget import getStmNavChange7Series


# 获取基金申购款
from windget import getStmNavChange7


# 获取基金申购款(实收基金)时间序列
from windget import getStmNavChange7PaidInCapitalSeries


# 获取基金申购款(实收基金)
from windget import getStmNavChange7PaidInCapital


# 获取基金赎回款时间序列
from windget import getStmNavChange8Series


# 获取基金赎回款
from windget import getStmNavChange8


# 获取基金赎回款(实收基金)时间序列
from windget import getStmNavChange8PaidInCapitalSeries


# 获取基金赎回款(实收基金)
from windget import getStmNavChange8PaidInCapital


# 获取信息披露费时间序列
from windget import getStmIs18Series


# 获取信息披露费
from windget import getStmIs18


# 获取首发信息披露费时间序列
from windget import getIpoIDcSeries


# 获取首发信息披露费
from windget import getIpoIDc


# 获取应收黄金合约拆借孳息时间序列
from windget import getStmBsGoldContractInterestSeries


# 获取应收黄金合约拆借孳息
from windget import getStmBsGoldContractInterest


# 获取交易佣金(合计值)时间序列
from windget import getCommissionTotalSeries


# 获取交易佣金(合计值)
from windget import getCommissionTotal


# 获取交易佣金(分券商明细)时间序列
from windget import getCommissionDetailedSeries


# 获取交易佣金(分券商明细)
from windget import getCommissionDetailed


# 获取应收票据及应收账款时间序列
from windget import getStm07BsReItsNotesSeries


# 获取应收票据及应收账款
from windget import getStm07BsReItsNotes


# 获取其他应收款(合计)时间序列
from windget import getStm07BsReItsOthersSeries


# 获取其他应收款(合计)
from windget import getStm07BsReItsOthers


# 获取投资性房地产租金收入时间序列
from windget import getStmNoteInvestmentIncome0003Series


# 获取投资性房地产租金收入
from windget import getStmNoteInvestmentIncome0003


# 获取投资性房地产时间序列
from windget import getStm07BsReItsRealEstateSeries


# 获取投资性房地产
from windget import getStm07BsReItsRealEstate


# 获取应付票据及应付账款时间序列
from windget import getStm07BsReItsPayableSeries


# 获取应付票据及应付账款
from windget import getStm07BsReItsPayable


# 获取预收款项_GSD时间序列
from windget import getWgsDPaymentUnearnedSeries


# 获取预收款项_GSD
from windget import getWgsDPaymentUnearned


# 获取预收款项时间序列
from windget import getStm07BsReItsRecIPtsSeries


# 获取预收款项
from windget import getStm07BsReItsRecIPts


# 获取应交税费时间序列
from windget import getStm07BsReItsTaxSeries


# 获取应交税费
from windget import getStm07BsReItsTax


# 获取其他应付款(合计)时间序列
from windget import getStm07BsReItsOtherPayableSeries


# 获取其他应付款(合计)
from windget import getStm07BsReItsOtherPayable


# 获取实收资本(或股本)时间序列
from windget import getStm07BsReItsPaidInSeries


# 获取实收资本(或股本)
from windget import getStm07BsReItsPaidIn


# 获取资本公积金时间序列
from windget import getStm07BsReItsCapitalReserveSeries


# 获取资本公积金
from windget import getStm07BsReItsCapitalReserve


# 获取盈余公积金时间序列
from windget import getStm07BsReItsSurplusSeries


# 获取盈余公积金
from windget import getStm07BsReItsSurplus


# 获取未分配利润时间序列
from windget import getStm07BsReItsUndIsTriRProfitSeries


# 获取未分配利润
from windget import getStm07BsReItsUndIsTriRProfit


# 获取未分配利润_FUND时间序列
from windget import getStmBs75Series


# 获取未分配利润_FUND
from windget import getStmBs75


# 获取经营活动现金流入小计时间序列
from windget import getStm07CsReItsOperCashInSeries


# 获取经营活动现金流入小计
from windget import getStm07CsReItsOperCashIn


# 获取单季度.经营活动现金流入小计时间序列
from windget import getQfaSToTCashInFlowsOperActSeries


# 获取单季度.经营活动现金流入小计
from windget import getQfaSToTCashInFlowsOperAct


# 获取经营活动现金流出小计时间序列
from windget import getStm07CsReItsOperCashOutSeries


# 获取经营活动现金流出小计
from windget import getStm07CsReItsOperCashOut


# 获取单季度.经营活动现金流出小计时间序列
from windget import getQfaSToTCashOutFlowsOperActSeries


# 获取单季度.经营活动现金流出小计
from windget import getQfaSToTCashOutFlowsOperAct


# 获取销售商品、提供劳务收到的现金时间序列
from windget import getStm07CsReItsSalesCashSeries


# 获取销售商品、提供劳务收到的现金
from windget import getStm07CsReItsSalesCash


# 获取单季度.销售商品、提供劳务收到的现金时间序列
from windget import getQfaCashRecpSgAndRsSeries


# 获取单季度.销售商品、提供劳务收到的现金
from windget import getQfaCashRecpSgAndRs


# 获取购买商品、接受劳务支付的现金时间序列
from windget import getStm07CsReItsBuyCashSeries


# 获取购买商品、接受劳务支付的现金
from windget import getStm07CsReItsBuyCash


# 获取单季度.购买商品、接受劳务支付的现金时间序列
from windget import getQfaCashPayGoodsPUrchSerVRecSeries


# 获取单季度.购买商品、接受劳务支付的现金
from windget import getQfaCashPayGoodsPUrchSerVRec


# 获取支付的各项税费时间序列
from windget import getStm07CsReItsTaxSeries


# 获取支付的各项税费
from windget import getStm07CsReItsTax


# 获取单季度.支付的各项税费时间序列
from windget import getQfaPayAllTyPTaxSeries


# 获取单季度.支付的各项税费
from windget import getQfaPayAllTyPTax


# 获取支付其他与经营活动有关的现金时间序列
from windget import getStm07CsReItsPaidCashSeries


# 获取支付其他与经营活动有关的现金
from windget import getStm07CsReItsPaidCash


# 获取单季度.支付其他与经营活动有关的现金时间序列
from windget import getQfaOtherCashPayRalOperActSeries


# 获取单季度.支付其他与经营活动有关的现金
from windget import getQfaOtherCashPayRalOperAct


# 获取投资活动现金流入小计时间序列
from windget import getStm07CsReItsInvestCashInSeries


# 获取投资活动现金流入小计
from windget import getStm07CsReItsInvestCashIn


# 获取单季度.投资活动现金流入小计时间序列
from windget import getQfaSToTCashInFlowsInvActSeries


# 获取单季度.投资活动现金流入小计
from windget import getQfaSToTCashInFlowsInvAct


# 获取投资活动现金流出小计时间序列
from windget import getStm07CsReItsInvestCashOutSeries


# 获取投资活动现金流出小计
from windget import getStm07CsReItsInvestCashOut


# 获取单季度.投资活动现金流出小计时间序列
from windget import getQfaSToTCashOutFlowsInvActSeries


# 获取单季度.投资活动现金流出小计
from windget import getQfaSToTCashOutFlowsInvAct


# 获取筹资活动现金流入小计时间序列
from windget import getStm07CsReItsFinanceCashInSeries


# 获取筹资活动现金流入小计
from windget import getStm07CsReItsFinanceCashIn


# 获取单季度.筹资活动现金流入小计时间序列
from windget import getQfaSToTCashInFlowsFncActSeries


# 获取单季度.筹资活动现金流入小计
from windget import getQfaSToTCashInFlowsFncAct


# 获取筹资活动现金流出小计时间序列
from windget import getStm07CsReItsFinanceCashOutSeries


# 获取筹资活动现金流出小计
from windget import getStm07CsReItsFinanceCashOut


# 获取单季度.筹资活动现金流出小计时间序列
from windget import getQfaSToTCashOutFlowsFncActSeries


# 获取单季度.筹资活动现金流出小计
from windget import getQfaSToTCashOutFlowsFncAct


# 获取季度报告披露日期时间序列
from windget import getFundStmIssuingDateQTySeries


# 获取季度报告披露日期
from windget import getFundStmIssuingDateQTy


# 获取中(年)报披露日期时间序列
from windget import getFundStmIssuingDateSeries


# 获取中(年)报披露日期
from windget import getFundStmIssuingDate


# 获取每股股利(税前)(已宣告)时间序列
from windget import getDivCashBeforeTax2Series


# 获取每股股利(税前)(已宣告)
from windget import getDivCashBeforeTax2


# 获取每股股利(税后)(已宣告)时间序列
from windget import getDivCashAfterTax2Series


# 获取每股股利(税后)(已宣告)
from windget import getDivCashAfterTax2


# 获取每股红股(已宣告)时间序列
from windget import getDivStock2Series


# 获取每股红股(已宣告)
from windget import getDivStock2


# 获取每股红股时间序列
from windget import getDivStockSeries


# 获取每股红股
from windget import getDivStock


# 获取每股股利(税后)时间序列
from windget import getDivCashAfterTaxSeries


# 获取每股股利(税后)
from windget import getDivCashAfterTax


# 获取区间每股股利(税后)时间序列
from windget import getDivCashPaidAfterTaxSeries


# 获取区间每股股利(税后)
from windget import getDivCashPaidAfterTax


# 获取每股股利(税前)时间序列
from windget import getDivCashBeforeTaxSeries


# 获取每股股利(税前)
from windget import getDivCashBeforeTax


# 获取区间每股股利(税前)时间序列
from windget import getDivCashPaidBeforeTaxSeries


# 获取区间每股股利(税前)
from windget import getDivCashPaidBeforeTax


# 获取每股分红送转时间序列
from windget import getDivCashAndStockSeries


# 获取每股分红送转
from windget import getDivCashAndStock


# 获取分红方案进度时间序列
from windget import getDivProgressSeries


# 获取分红方案进度
from windget import getDivProgress


# 获取分红对象时间序列
from windget import getDivObjectSeries


# 获取分红对象
from windget import getDivObject


# 获取是否分红时间序列
from windget import getDivIfDivSeries


# 获取是否分红
from windget import getDivIfDiv


# 获取分红基准股本时间序列
from windget import getDivSharesSeries


# 获取分红基准股本
from windget import getDivShares


# 获取现金分红总额时间序列
from windget import getStmNoteAuALaCcmDivSeries


# 获取现金分红总额
from windget import getStmNoteAuALaCcmDiv


# 获取年度现金分红总额时间序列
from windget import getDivAuAlCashDividendSeries


# 获取年度现金分红总额
from windget import getDivAuAlCashDividend


# 获取区间现金分红总额时间序列
from windget import getDivAuALaCcmDiv2Series


# 获取区间现金分红总额
from windget import getDivAuALaCcmDiv2


# 获取股权登记日时间序列
from windget import getDivRecordDateSeries


# 获取股权登记日
from windget import getDivRecordDate


# 获取B股股权登记日时间序列
from windget import getRightsIssueRecDateShareBSeries


# 获取B股股权登记日
from windget import getRightsIssueRecDateShareB


# 获取老股东配售股权登记日时间序列
from windget import getCbListRationChKindAteSeries


# 获取老股东配售股权登记日
from windget import getCbListRationChKindAte


# 获取向老股东配售股权登记日时间序列
from windget import getFellowRecordDateSeries


# 获取向老股东配售股权登记日
from windget import getFellowRecordDate


# 获取除权除息日时间序列
from windget import getDivExDateSeries


# 获取除权除息日
from windget import getDivExDate


# 获取派息日时间序列
from windget import getDivPayDateSeries


# 获取派息日
from windget import getDivPayDate


# 获取红股上市交易日时间序列
from windget import getDivTrDDateShareBSeries


# 获取红股上市交易日
from windget import getDivTrDDateShareB


# 获取预披露公告日时间序列
from windget import getDivPreDisclosureDateSeries


# 获取预披露公告日
from windget import getDivPreDisclosureDate


# 获取预案公告日时间序列
from windget import getRightsIssuePrePlanDateSeries


# 获取预案公告日
from windget import getRightsIssuePrePlanDate


# 获取董事会预案公告日时间序列
from windget import getRefRMkdPrePlanDateSeries


# 获取董事会预案公告日
from windget import getRefRMkdPrePlanDate


# 获取股东大会公告日时间序列
from windget import getCbWarAnnoDateMeetingSeries


# 获取股东大会公告日
from windget import getCbWarAnnoDateMeeting


# 获取分红实施公告日时间序列
from windget import getDivImpDateSeries


# 获取分红实施公告日
from windget import getDivImpDate


# 获取三年累计分红占比(再融资条件)时间序列
from windget import getDivDivPct3YearAccUSeries


# 获取三年累计分红占比(再融资条件)
from windget import getDivDivPct3YearAccU


# 获取上市以来分红率时间序列
from windget import getDivDivPctAccUSeries


# 获取上市以来分红率
from windget import getDivDivPctAccU


# 获取年度现金分红比例时间序列
from windget import getDivPayOutRatio2Series


# 获取年度现金分红比例
from windget import getDivPayOutRatio2


# 获取年度现金分红次数时间序列
from windget import getDivFrEqSeries


# 获取年度现金分红次数
from windget import getDivFrEq


# 获取年度累计单位分红时间序列
from windget import getDivAuALaCcmDivPerShareSeries


# 获取年度累计单位分红
from windget import getDivAuALaCcmDivPerShare


# 获取现金分红比例时间序列
from windget import getDivDividendRatioSeries


# 获取现金分红比例
from windget import getDivDividendRatio


# 获取首发上市日期时间序列
from windget import getIpoDateSeries


# 获取首发上市日期
from windget import getIpoDate


# 获取首发价格时间序列
from windget import getIpoPrice2Series


# 获取首发价格
from windget import getIpoPrice2


# 获取发行数量合计时间序列
from windget import getIpoAmountSeries


# 获取发行数量合计
from windget import getIpoAmount


# 获取新股发行数量时间序列
from windget import getIpoNewSharesSeries


# 获取新股发行数量
from windget import getIpoNewShares


# 获取股东售股数量时间序列
from windget import getIpoOldSharesSeries


# 获取股东售股数量
from windget import getIpoOldShares


# 获取老股转让比例时间序列
from windget import getIpoOldSharesRatioSeries


# 获取老股转让比例
from windget import getIpoOldSharesRatio


# 获取募集资金总额(含股东售股)时间序列
from windget import getIpoCollectionTotalSeries


# 获取募集资金总额(含股东售股)
from windget import getIpoCollectionTotal


# 获取首发募集资金时间序列
from windget import getIpoCollectionSeries


# 获取首发募集资金
from windget import getIpoCollection


# 获取首发募集资金净额时间序列
from windget import getIpoNetCollectionTureSeries


# 获取首发募集资金净额
from windget import getIpoNetCollectionTure


# 获取股东售股金额时间序列
from windget import getIpoCollectionOldShares2Series


# 获取股东售股金额
from windget import getIpoCollectionOldShares2


# 获取首发预计募集资金时间序列
from windget import getIpoExpectedCollection2Series


# 获取首发预计募集资金
from windget import getIpoExpectedCollection2


# 获取网上发行数量(回拨前)时间序列
from windget import getIpoPoCOnlineSeries


# 获取网上发行数量(回拨前)
from windget import getIpoPoCOnline


# 获取网下发行数量(回拨前)时间序列
from windget import getIpoPoCOfflineSeries


# 获取网下发行数量(回拨前)
from windget import getIpoPoCOffline


# 获取网上发行数量时间序列
from windget import getIssueIssueOlSeries


# 获取网上发行数量
from windget import getIssueIssueOl


# 获取网上发行数量(不含优先配售)时间序列
from windget import getCbListIssueVolOnLSeries


# 获取网上发行数量(不含优先配售)
from windget import getCbListIssueVolOnL


# 获取网下发行数量时间序列
from windget import getFellowOtcAmtSeries


# 获取网下发行数量
from windget import getFellowOtcAmt


# 获取网上发行有效申购数量时间序列
from windget import getIpoVsSharesSSeries


# 获取网上发行有效申购数量
from windget import getIpoVsSharesS


# 获取网上发行有效认购倍数时间序列
from windget import getIpoSubRatioSeries


# 获取网上发行有效认购倍数
from windget import getIpoSubRatio


# 获取国际发行有效申购数量时间序列
from windget import getIpoIntvsSharesSeries


# 获取国际发行有效申购数量
from windget import getIpoIntvsShares


# 获取国际发行有效申购倍数时间序列
from windget import getIpoIntSubRatioSeries


# 获取国际发行有效申购倍数
from windget import getIpoIntSubRatio


# 获取申报预披露日时间序列
from windget import getIpoWpIpReleasingDateSeries


# 获取申报预披露日
from windget import getIpoWpIpReleasingDate


# 获取招股公告日时间序列
from windget import getIpoPubOfFrDateSeries


# 获取招股公告日
from windget import getIpoPubOfFrDate


# 获取首发主承销商时间序列
from windget import getIpoLeadUndRSeries


# 获取首发主承销商
from windget import getIpoLeadUndR


# 获取首发保荐机构时间序列
from windget import getIpoSponsorSeries


# 获取首发保荐机构
from windget import getIpoSponsor


# 获取首发保荐机构(上市推荐人)时间序列
from windget import getIpoNominatorSeries


# 获取首发保荐机构(上市推荐人)
from windget import getIpoNominator


# 获取首发副主承销商时间序列
from windget import getIpoDeputyUndRSeries


# 获取首发副主承销商
from windget import getIpoDeputyUndR


# 获取首发保荐人律师时间序列
from windget import getIpoLegalAdvisorSeries


# 获取首发保荐人律师
from windget import getIpoLegalAdvisor


# 获取首发承销保荐费用时间序列
from windget import getIpoUsFees2Series


# 获取首发承销保荐费用
from windget import getIpoUsFees2


# 获取新股配售经纪佣金费率时间序列
from windget import getIpoCommissionRateSeries


# 获取新股配售经纪佣金费率
from windget import getIpoCommissionRate


# 获取首发审计费用时间序列
from windget import getIpoAuditFeeSeries


# 获取首发审计费用
from windget import getIpoAuditFee


# 获取首发法律费用时间序列
from windget import getIpoLawFeeSeries


# 获取首发法律费用
from windget import getIpoLawFee


# 获取是否行使超额配售权时间序列
from windget import getIpoGreenShoeSeries


# 获取是否行使超额配售权
from windget import getIpoGreenShoe


# 获取是否触发回拨机制时间序列
from windget import getIpoBackMechanismSeries


# 获取是否触发回拨机制
from windget import getIpoBackMechanism


# 获取计划发行总数时间序列
from windget import getIpoIsSuVolPlannedSeries


# 获取计划发行总数
from windget import getIpoIsSuVolPlanned


# 获取申购一手中签率时间序列
from windget import getIpoDTooRatioPlSeries


# 获取申购一手中签率
from windget import getIpoDTooRatioPl


# 获取稳购1手最低申购股数时间序列
from windget import getIpoMinSubscriptionPlSeries


# 获取稳购1手最低申购股数
from windget import getIpoMinSubscriptionPl


# 获取超额配售数量时间序列
from windget import getIpoOverAllotVolSeries


# 获取超额配售数量
from windget import getIpoOverAllotVol


# 获取公开发售甲组申购人数时间序列
from windget import getIpoSubNumASeries


# 获取公开发售甲组申购人数
from windget import getIpoSubNumA


# 获取公开发售乙组申购人数时间序列
from windget import getIpoSubNumBSeries


# 获取公开发售乙组申购人数
from windget import getIpoSubNumB


# 获取公开发售申购人数时间序列
from windget import getIpoSubNumSeries


# 获取公开发售申购人数
from windget import getIpoSubNum


# 获取首日上市数量时间序列
from windget import getIpoLStNumSeries


# 获取首日上市数量
from windget import getIpoLStNum


# 获取上市天数时间序列
from windget import getIpoListDaysSeries


# 获取上市天数
from windget import getIpoListDays


# 获取上市交易天数时间序列
from windget import getIpoTradeDaysSeries


# 获取上市交易天数
from windget import getIpoTradeDays


# 获取新股未开板涨停板天数时间序列
from windget import getIpoLimitUpDaysSeries


# 获取新股未开板涨停板天数
from windget import getIpoLimitUpDays


# 获取开板日时间序列
from windget import getIpoLimitUpOpenDateSeries


# 获取开板日
from windget import getIpoLimitUpOpenDate


# 获取网上发行中签率时间序列
from windget import getIpoCashRatioSeries


# 获取网上发行中签率
from windget import getIpoCashRatio


# 获取网上申购数量上限时间序列
from windget import getIpoSSharesUpLimitSeries


# 获取网上申购数量上限
from windget import getIpoSSharesUpLimit


# 获取网上申购资金上限时间序列
from windget import getIpoSAmtUpLimitSeries


# 获取网上申购资金上限
from windget import getIpoSAmtUpLimit


# 获取网上发行有效申购户数时间序列
from windget import getIpoCashEffAccSeries


# 获取网上发行有效申购户数
from windget import getIpoCashEffAcc


# 获取网上超额认购倍数时间序列
from windget import getIpoOvRSubRatioSeries


# 获取网上超额认购倍数
from windget import getIpoOvRSubRatio


# 获取网上冻结资金时间序列
from windget import getIpoBFundSeries


# 获取网上冻结资金
from windget import getIpoBFund


# 获取网上申购代码时间序列
from windget import getIpoPurchaseCodeSeries


# 获取网上申购代码
from windget import getIpoPurchaseCode


# 获取网上放弃认购数量时间序列
from windget import getIpoGiveUpSeries


# 获取网上放弃认购数量
from windget import getIpoGiveUp


# 获取网下申购配售比例时间序列
from windget import getIpoOtcCashPctSeries


# 获取网下申购配售比例
from windget import getIpoOtcCashPct


# 获取网下申购总量时间序列
from windget import getIpoOpVolumeSeries


# 获取网下申购总量
from windget import getIpoOpVolume


# 获取网下冻结资金时间序列
from windget import getIpoOpAmountSeries


# 获取网下冻结资金
from windget import getIpoOpAmount


# 获取网下有效报价下限时间序列
from windget import getIpoVsPriceMinSeries


# 获取网下有效报价下限
from windget import getIpoVsPriceMin


# 获取网下有效报价上限时间序列
from windget import getIpoVsPriceMaxSeries


# 获取网下有效报价上限
from windget import getIpoVsPriceMax


# 获取网下有效报价申购量时间序列
from windget import getIpoVsSharesSeries


# 获取网下有效报价申购量
from windget import getIpoVsShares


# 获取网下超额认购倍数时间序列
from windget import getFellowAmtToJurSeries


# 获取网下超额认购倍数
from windget import getFellowAmtToJur


# 获取网下超额认购倍数(回拨前)时间序列
from windget import getIpoVsRatioSeries


# 获取网下超额认购倍数(回拨前)
from windget import getIpoVsRatio


# 获取网下高于有效报价上限的申购量时间序列
from windget import getIpoInvsSharesASeries


# 获取网下高于有效报价上限的申购量
from windget import getIpoInvsSharesA


# 获取网下申购数量上限时间序列
from windget import getIpoOpUpLimitSeries


# 获取网下申购数量上限
from windget import getIpoOpUpLimit


# 获取网下申购数量下限时间序列
from windget import getIpoOpDownLimitSeries


# 获取网下申购数量下限
from windget import getIpoOpDownLimit


# 获取网下申购步长时间序列
from windget import getListStepSizeSubsCrOfFlSeries


# 获取网下申购步长
from windget import getListStepSizeSubsCrOfFl


# 获取网下申购报价数量时间序列
from windget import getIpoOpNumOffRingSeries


# 获取网下申购报价数量
from windget import getIpoOpNumOffRing


# 获取网下申购配售对象家数时间序列
from windget import getIpoOpNumOfPmtSeries


# 获取网下申购配售对象家数
from windget import getIpoOpNumOfPmt


# 获取网下申购询价对象家数时间序列
from windget import getIpoOpNumOfInQSeries


# 获取网下申购询价对象家数
from windget import getIpoOpNumOfInQ


# 获取网下询价机构获配数量时间序列
from windget import getIpoLotWinningNumberSeries


# 获取网下询价机构获配数量
from windget import getIpoLotWinningNumber


# 获取网下投资者获配数量时间序列
from windget import getIpoPSharesAbcSeries


# 获取网下投资者获配数量
from windget import getIpoPSharesAbc


# 获取网下投资者申购数量时间序列
from windget import getIpoOpVolumeAbcSeries


# 获取网下投资者申购数量
from windget import getIpoOpVolumeAbc


# 获取网下投资者获配家数时间序列
from windget import getIpoNInstitutionalAbcSeries


# 获取网下投资者获配家数
from windget import getIpoNInstitutionalAbc


# 获取网下投资者中签率时间序列
from windget import getIpoLotteryRateAbcSeries


# 获取网下投资者中签率
from windget import getIpoLotteryRateAbc


# 获取网下投资者配售数量占比时间序列
from windget import getIpoPSharesPctAbcSeries


# 获取网下投资者配售数量占比
from windget import getIpoPSharesPctAbc


# 获取网下投资者有效申购数量占比时间序列
from windget import getIpoVsSharesPctAbcSeries


# 获取网下投资者有效申购数量占比
from windget import getIpoVsSharesPctAbc


# 获取网下公募基金获配数量时间序列
from windget import getIpoPSharesMfSeries


# 获取网下公募基金获配数量
from windget import getIpoPSharesMf


# 获取网下社保基金获配数量时间序列
from windget import getIpoPSharesSSfSeries


# 获取网下社保基金获配数量
from windget import getIpoPSharesSSf


# 获取网下企业年金获配数量时间序列
from windget import getIpoPSharesSpSeries


# 获取网下企业年金获配数量
from windget import getIpoPSharesSp


# 获取网下保险资金获配数量时间序列
from windget import getIpoPSharesIfSeries


# 获取网下保险资金获配数量
from windget import getIpoPSharesIf


# 获取战略配售获配股份数时间序列
from windget import getIpoSiAllotmentSeries


# 获取战略配售获配股份数
from windget import getIpoSiAllotment


# 获取战略配售获配股份占比时间序列
from windget import getIpoSiAllotmentRatioSeries


# 获取战略配售获配股份占比
from windget import getIpoSiAllotmentRatio


# 获取主承销商战略获配股份数时间序列
from windget import getIpoUnderwriterAllotmentSeries


# 获取主承销商战略获配股份数
from windget import getIpoUnderwriterAllotment


# 获取主承销商战略获配股份占比时间序列
from windget import getIpoUnderwriterAllotmentRatioSeries


# 获取主承销商战略获配股份占比
from windget import getIpoUnderwriterAllotmentRatio


# 获取网下配售对象名称时间序列
from windget import getIpoAllotmentSubjectsSeries


# 获取网下配售对象名称
from windget import getIpoAllotmentSubjects


# 获取网下投资者分类限售配售方式时间序列
from windget import getIpoAllOtwaySeries


# 获取网下投资者分类限售配售方式
from windget import getIpoAllOtway


# 获取网下投资者分类配售限售比例时间序列
from windget import getIpoPShareRestrictPctSeries


# 获取网下投资者分类配售限售比例
from windget import getIpoPShareRestrictPct


# 获取网下申报价格加权平均数时间序列
from windget import getIpoWGtAvgPriceSeries


# 获取网下申报价格加权平均数
from windget import getIpoWGtAvgPrice


# 获取网下申报价格中位数时间序列
from windget import getIpoMedianPriceSeries


# 获取网下申报价格中位数
from windget import getIpoMedianPrice


# 获取初步询价申报价格时间序列
from windget import getIpoSubscriptionPriceSeries


# 获取初步询价申报价格
from windget import getIpoSubscriptionPrice


# 获取初步询价申报数量时间序列
from windget import getIpoSubscriptionSharesSeries


# 获取初步询价申报数量
from windget import getIpoSubscriptionShares


# 获取初步询价配售对象家数时间序列
from windget import getIpoInquirySeries


# 获取初步询价配售对象家数
from windget import getIpoInquiry


# 获取初步询价询价对象家数时间序列
from windget import getIpoInquiryInStSeries


# 获取初步询价询价对象家数
from windget import getIpoInquiryInSt


# 获取初步询价下限时间序列
from windget import getIpoSPriceMinSeries


# 获取初步询价下限
from windget import getIpoSPriceMin


# 获取初步询价上限时间序列
from windget import getIpoSPriceMaxSeries


# 获取初步询价上限
from windget import getIpoSPriceMax


# 获取初步询价申购总量时间序列
from windget import getIpoSSharesTSeries


# 获取初步询价申购总量
from windget import getIpoSSharesT


# 获取初步询价申购倍数(回拨前)时间序列
from windget import getIpoSRatioSeries


# 获取初步询价申购倍数(回拨前)
from windget import getIpoSRatio


# 获取询价市值计算参考日时间序列
from windget import getIpoInquiryMvCalDateSeries


# 获取询价市值计算参考日
from windget import getIpoInquiryMvCalDate


# 获取网下询价市值门槛时间序列
from windget import getIpoInquiryMvMinSeries


# 获取网下询价市值门槛
from windget import getIpoInquiryMvMin


# 获取网下询价市值门槛(A类)时间序列
from windget import getIpoInquiryMvMinASeries


# 获取网下询价市值门槛(A类)
from windget import getIpoInquiryMvMinA


# 获取网下询价市值门槛(主题与战略)时间序列
from windget import getIpoInquiryMvMinThemEstrTSeries


# 获取网下询价市值门槛(主题与战略)
from windget import getIpoInquiryMvMinThemEstrT


# 获取发行价格下限(底价)时间序列
from windget import getIpoPriceMinSeries


# 获取发行价格下限(底价)
from windget import getIpoPriceMin


# 获取发行价格上限时间序列
from windget import getIpoPriceMaxSeries


# 获取发行价格上限
from windget import getIpoPriceMax


# 获取首发承销方式时间序列
from windget import getIpoUndRTypeSeries


# 获取首发承销方式
from windget import getIpoUndRType


# 获取首发分销商时间序列
from windget import getIpoDistOrSeries


# 获取首发分销商
from windget import getIpoDistOr


# 获取首发国际协调人时间序列
from windget import getIpoInterCordTorSeries


# 获取首发国际协调人
from windget import getIpoInterCordTor


# 获取首发保荐人代表时间序列
from windget import getIpoSponsorRepresentativeSeries


# 获取首发保荐人代表
from windget import getIpoSponsorRepresentative


# 获取首发签字会计师时间序列
from windget import getIpoAuditCpaSeries


# 获取首发签字会计师
from windget import getIpoAuditCpa


# 获取首发经办律所时间序列
from windget import getIpoLawFirmSeries


# 获取首发经办律所
from windget import getIpoLawFirm


# 获取网下投资者报备截止日时间序列
from windget import getIpoApplicationDeadlineSeries


# 获取网下投资者报备截止日
from windget import getIpoApplicationDeadline


# 获取网下投资者报备截止时间时间序列
from windget import getIpoApplicationDeadlineTimeSeries


# 获取网下投资者报备截止时间
from windget import getIpoApplicationDeadlineTime


# 获取上市公告日时间序列
from windget import getIssueLiStanceSeries


# 获取上市公告日
from windget import getIssueLiStance


# 获取初步询价公告日时间序列
from windget import getIpoInQAnnCeDateSeries


# 获取初步询价公告日
from windget import getIpoInQAnnCeDate


# 获取初步询价起始日时间序列
from windget import getIpoInQStartDateSeries


# 获取初步询价起始日
from windget import getIpoInQStartDate


# 获取初步询价截止日时间序列
from windget import getIpoInQEnddateSeries


# 获取初步询价截止日
from windget import getIpoInQEnddate


# 获取初步询价结果公告日时间序列
from windget import getIpoInQResultDateSeries


# 获取初步询价结果公告日
from windget import getIpoInQResultDate


# 获取初步配售结果公告日时间序列
from windget import getIpoPReplacingDateSeries


# 获取初步配售结果公告日
from windget import getIpoPReplacingDate


# 获取网下申购截止日期时间序列
from windget import getIpoOpEnddateSeries


# 获取网下申购截止日期
from windget import getIpoOpEnddate


# 获取网下定价日时间序列
from windget import getIpoPDateSeries


# 获取网下定价日
from windget import getIpoPDate


# 获取网下申购缴款日时间序列
from windget import getIpoOffSubPayDateSeries


# 获取网下申购缴款日
from windget import getIpoOffSubPayDate


# 获取网上市值申购登记日时间序列
from windget import getIpoMvRegDateSeries


# 获取网上市值申购登记日
from windget import getIpoMvRegDate


# 获取网上中签结果公告日时间序列
from windget import getIpoRefundDateSeries


# 获取网上中签结果公告日
from windget import getIpoRefundDate


# 获取网上申购缴款日时间序列
from windget import getIpoCapPayDateSeries


# 获取网上申购缴款日
from windget import getIpoCapPayDate


# 获取现场推介起始日期时间序列
from windget import getIpoRsDateSSeries


# 获取现场推介起始日期
from windget import getIpoRsDateS


# 获取现场推介截止日期时间序列
from windget import getIpoRsDateESeries


# 获取现场推介截止日期
from windget import getIpoRsDateE


# 获取网下配售结果公告日时间序列
from windget import getIpoPlacingDateSeries


# 获取网下配售结果公告日
from windget import getIpoPlacingDate


# 获取其它发行起始日期时间序列
from windget import getIpoOtherStartDateSeries


# 获取其它发行起始日期
from windget import getIpoOtherStartDate


# 获取其它发行截止日期时间序列
from windget import getIpoOtherEnddateSeries


# 获取其它发行截止日期
from windget import getIpoOtherEnddate


# 获取辅导备案日时间序列
from windget import getIpoTutoringStartDateSeries


# 获取辅导备案日
from windget import getIpoTutoringStartDate


# 获取提交注册日时间序列
from windget import getIpoSubmitRegisTDateSeries


# 获取提交注册日
from windget import getIpoSubmitRegisTDate


# 获取注册成功日(证监会审核批文日)时间序列
from windget import getIpoRegisTDateSeries


# 获取注册成功日(证监会审核批文日)
from windget import getIpoRegisTDate


# 获取申报基准日时间序列
from windget import getIpoMrQDateSeries


# 获取申报基准日
from windget import getIpoMrQDate


# 获取网下报备起始日时间序列
from windget import getIpoOrStartDateSeries


# 获取网下报备起始日
from windget import getIpoOrStartDate


# 获取首发市盈率(摊薄)时间序列
from windget import getIpoDilutedPeSeries


# 获取首发市盈率(摊薄)
from windget import getIpoDilutedPe


# 获取首发市盈率(加权)时间序列
from windget import getIpoWeightedPeSeries


# 获取首发市盈率(加权)
from windget import getIpoWeightedPe


# 获取发行市净率时间序列
from windget import getIpoPbSeries


# 获取发行市净率
from windget import getIpoPb


# 获取首发时所属行业市盈率时间序列
from windget import getIpoIndustryPeSeries


# 获取首发时所属行业市盈率
from windget import getIpoIndustryPe


# 获取预计发行股数时间序列
from windget import getIpoAmountEstSeries


# 获取预计发行股数
from windget import getIpoAmountEst


# 获取预计募投项目投资总额时间序列
from windget import getIpoNetCollectionEstSeries


# 获取预计募投项目投资总额
from windget import getIpoNetCollectionEst


# 获取首发超募资金时间序列
from windget import getIpoBeyondActualColleCSeries


# 获取首发超募资金
from windget import getIpoBeyondActualColleC


# 获取售股股东应摊承销与保荐费用时间序列
from windget import getIpoUnderwritingFeesShareholderSeries


# 获取售股股东应摊承销与保荐费用
from windget import getIpoUnderwritingFeesShareholder


# 获取承销商认购余额时间序列
from windget import getIpoSubByDIsTrSeries


# 获取承销商认购余额
from windget import getIpoSubByDIsTr


# 获取回拨比例时间序列
from windget import getIpoReallocationPctSeries


# 获取回拨比例
from windget import getIpoReallocationPct


# 获取向战略投资者配售数量时间序列
from windget import getIpoAmtToInStInvestorSeries


# 获取向战略投资者配售数量
from windget import getIpoAmtToInStInvestor


# 获取其它发行数量时间序列
from windget import getIpoAmtToOtherSeries


# 获取其它发行数量
from windget import getIpoAmtToOther


# 获取近三年研发投入占比时间序列
from windget import getIpoRdInvestSeries


# 获取近三年研发投入占比
from windget import getIpoRdInvest


# 获取近三年研发投入累计额时间序列
from windget import getIpoInvestAmountSeries


# 获取近三年研发投入累计额
from windget import getIpoInvestAmount


# 获取研发人员占比时间序列
from windget import getIpoRdPersonSeries


# 获取研发人员占比
from windget import getIpoRdPerson


# 获取发明专利个数时间序列
from windget import getIpoInventionSeries


# 获取发明专利个数
from windget import getIpoInvention


# 获取近一年营收额时间序列
from windget import getIpoRevenueSeries


# 获取近一年营收额
from windget import getIpoRevenue


# 获取被剔除的申报量占比时间序列
from windget import getPoQeSeries


# 获取被剔除的申报量占比
from windget import getPoQe


# 获取增发进度时间序列
from windget import getFellowProgressSeries


# 获取增发进度
from windget import getFellowProgress


# 获取增发价格时间序列
from windget import getFellowPriceSeries


# 获取增发价格
from windget import getFellowPrice


# 获取增发数量时间序列
from windget import getFellowAmountSeries


# 获取增发数量
from windget import getFellowAmount


# 获取增发上市日时间序列
from windget import getFellowListedDateSeries


# 获取增发上市日
from windget import getFellowListedDate


# 获取增发募集资金时间序列
from windget import getFellowCollectionSeries


# 获取增发募集资金
from windget import getFellowCollection


# 获取区间增发募集资金合计时间序列
from windget import getFellowCollectionTSeries


# 获取区间增发募集资金合计
from windget import getFellowCollectionT


# 获取增发费用时间序列
from windget import getFellowExpenseSeries


# 获取增发费用
from windget import getFellowExpense


# 获取增发实际募集资金时间序列
from windget import getFellowNetCollectionSeries


# 获取增发实际募集资金
from windget import getFellowNetCollection


# 获取定向增发基准价格时间序列
from windget import getFellowBenchmarkPriceSeries


# 获取定向增发基准价格
from windget import getFellowBenchmarkPrice


# 获取定向增发预案价格相对基准价格比率时间序列
from windget import getFellowPriceToReservePriceSeries


# 获取定向增发预案价格相对基准价格比率
from windget import getFellowPriceToReservePrice


# 获取定向增发实际价格相对基准价格比率时间序列
from windget import getFellowPriceToBenchmarkPriceSeries


# 获取定向增发实际价格相对基准价格比率
from windget import getFellowPriceToBenchmarkPrice


# 获取区间定增次数时间序列
from windget import getFellowNSeries


# 获取区间定增次数
from windget import getFellowN


# 获取总中签率时间序列
from windget import getFellowTotalRatioSeries


# 获取总中签率
from windget import getFellowTotalRatio


# 获取公开发行中签率时间序列
from windget import getFellowPublicRatioSeries


# 获取公开发行中签率
from windget import getFellowPublicRatio


# 获取增发承销方式时间序列
from windget import getFellowUndRTypeSeries


# 获取增发承销方式
from windget import getFellowUndRType


# 获取增发主承销商时间序列
from windget import getFellowLeadUndRSeries


# 获取增发主承销商
from windget import getFellowLeadUndR


# 获取增发保荐机构(上市推荐人)时间序列
from windget import getFellowDeputyUndRSeries


# 获取增发保荐机构(上市推荐人)
from windget import getFellowDeputyUndR


# 获取增发分销商时间序列
from windget import getFellowNominatorSeries


# 获取增发分销商
from windget import getFellowNominator


# 获取总有效申购户数时间序列
from windget import getFellowDistOrSeries


# 获取总有效申购户数
from windget import getFellowDistOr


# 获取总有效申购股数时间序列
from windget import getFellowInterCodNatOrSeries


# 获取总有效申购股数
from windget import getFellowInterCodNatOr


# 获取总超额认购倍数时间序列
from windget import getFellowCashRatioSeries


# 获取总超额认购倍数
from windget import getFellowCashRatio


# 获取公开发行认购有效申购户数时间序列
from windget import getFellowCapRatioSeries


# 获取公开发行认购有效申购户数
from windget import getFellowCapRatio


# 获取公开发行比例认购有效申购股数时间序列
from windget import getFellowCashAmtSeries


# 获取公开发行比例认购有效申购股数
from windget import getFellowCashAmt


# 获取公开发行超额认购倍数时间序列
from windget import getFellowCashEffAccSeries


# 获取公开发行超额认购倍数
from windget import getFellowCashEffAcc


# 获取老股东优先配售有效申购户数时间序列
from windget import getFellowCapeFfAccSeries


# 获取老股东优先配售有效申购户数
from windget import getFellowCapeFfAcc


# 获取老股东优先配售有效申购股数时间序列
from windget import getFellowCapeFfAmtSeries


# 获取老股东优先配售有效申购股数
from windget import getFellowCapeFfAmt


# 获取其它公众投资者有效申购户数时间序列
from windget import getFellowSubAccByPubSeries


# 获取其它公众投资者有效申购户数
from windget import getFellowSubAccByPub


# 获取其它公众投资者有效申购股数时间序列
from windget import getFellowOverSubRatioSeries


# 获取其它公众投资者有效申购股数
from windget import getFellowOverSubRatio


# 获取网下机构投资者有效申购户数时间序列
from windget import getFellowAmtByPlacingSeries


# 获取网下机构投资者有效申购户数
from windget import getFellowAmtByPlacing


# 获取网下机构投资者有效申购股数时间序列
from windget import getFellowSubAmtByPlacingSeries


# 获取网下机构投资者有效申购股数
from windget import getFellowSubAmtByPlacing


# 获取网上向老股东优先配售数量时间序列
from windget import getFellowAmtToInStSeries


# 获取网上向老股东优先配售数量
from windget import getFellowAmtToInSt


# 获取网上向老股东优先配售比例时间序列
from windget import getFellowAmtToInCorpSeries


# 获取网上向老股东优先配售比例
from windget import getFellowAmtToInCorp


# 获取网下向老股东优先配售数量时间序列
from windget import getFellowOtcPreAmtOrgSeries


# 获取网下向老股东优先配售数量
from windget import getFellowOtcPreAmtOrg


# 获取向其它公众投资者配售数量时间序列
from windget import getFellowAmtOtherPubSeries


# 获取向其它公众投资者配售数量
from windget import getFellowAmtOtherPub


# 获取定向配售数量时间序列
from windget import getFellowAmtTargetedSeries


# 获取定向配售数量
from windget import getFellowAmtTargeted


# 获取向原流通股东定向配售数量时间序列
from windget import getFellowAmtOrgTradableSeries


# 获取向原流通股东定向配售数量
from windget import getFellowAmtOrgTradable


# 获取向基金配售数量时间序列
from windget import getFellowAmtFundSeries


# 获取向基金配售数量
from windget import getFellowAmtFund


# 获取网下发售比例时间序列
from windget import getFellowOtcAmtPctSeries


# 获取网下发售比例
from windget import getFellowOtcAmtPct


# 获取承销商认购余股时间序列
from windget import getRightsIssueSubByDIsTrSeries


# 获取承销商认购余股
from windget import getRightsIssueSubByDIsTr


# 获取增发公告日时间序列
from windget import getFellowOfferingDateSeries


# 获取增发公告日
from windget import getFellowOfferingDate


# 获取公开发行日时间序列
from windget import getFellowIssueDateSeries


# 获取公开发行日
from windget import getFellowIssueDate


# 获取向网下增发日期时间序列
from windget import getFellowOtcDateSeries


# 获取向网下增发日期
from windget import getFellowOtcDate


# 获取发审委通过公告日时间序列
from windget import getFellowIecApprovalDateSeries


# 获取发审委通过公告日
from windget import getFellowIecApprovalDate


# 获取向老股东配售缴款起始日时间序列
from windget import getFellowPayStartDateSeries


# 获取向老股东配售缴款起始日
from windget import getFellowPayStartDate


# 获取向老股东配售缴款截止日时间序列
from windget import getFellowPayEnddateSeries


# 获取向老股东配售缴款截止日
from windget import getFellowPayEnddate


# 获取增发获准日期时间序列
from windget import getFellowApprovalDateSeries


# 获取增发获准日期
from windget import getFellowApprovalDate


# 获取网上路演日时间序列
from windget import getFellowRoadshowDateSeries


# 获取网上路演日
from windget import getFellowRoadshowDate


# 获取非公开发行股票受理日时间序列
from windget import getHandlingDatePiSeries


# 获取非公开发行股票受理日
from windget import getHandlingDatePi


# 获取股份登记日时间序列
from windget import getFellowRegisterDateSeries


# 获取股份登记日
from windget import getFellowRegisterDate


# 获取公开发行数量时间序列
from windget import getFellowPubAmtSeries


# 获取公开发行数量
from windget import getFellowPubAmt


# 获取折扣率时间序列
from windget import getFellowDiscNtRatioSeries


# 获取折扣率
from windget import getFellowDiscNtRatio


# 获取回拨数量时间序列
from windget import getFellowTrnFfAmtSeries


# 获取回拨数量
from windget import getFellowTrnFfAmt


# 获取增发预案价上限时间序列
from windget import getFellowPriceMaxSeries


# 获取增发预案价上限
from windget import getFellowPriceMax


# 获取增发预案价下限时间序列
from windget import getFellowPriceMinSeries


# 获取增发预案价下限
from windget import getFellowPriceMin


# 获取增发市盈率(摊薄)时间序列
from windget import getFellowDilutedPeSeries


# 获取增发市盈率(摊薄)
from windget import getFellowDilutedPe


# 获取增发市盈率(加权)时间序列
from windget import getFellowWeightedPeSeries


# 获取增发市盈率(加权)
from windget import getFellowWeightedPe


# 获取增发预计募集资金时间序列
from windget import getEstimatedNetCollectionSeries


# 获取增发预计募集资金
from windget import getEstimatedNetCollection


# 获取配股进度时间序列
from windget import getRightsIssueProgressSeries


# 获取配股进度
from windget import getRightsIssueProgress


# 获取配股价格时间序列
from windget import getRightsIssuePriceSeries


# 获取配股价格
from windget import getRightsIssuePrice


# 获取配股募集资金时间序列
from windget import getRightsIssueCollectionSeries


# 获取配股募集资金
from windget import getRightsIssueCollection


# 获取区间配股募集资金合计时间序列
from windget import getRightsIssueCollectionTSeries


# 获取区间配股募集资金合计
from windget import getRightsIssueCollectionT


# 获取配股费用时间序列
from windget import getRightsIssueExpenseSeries


# 获取配股费用
from windget import getRightsIssueExpense


# 获取配股实际募集资金时间序列
from windget import getRightsIssueNetCollectionSeries


# 获取配股实际募集资金
from windget import getRightsIssueNetCollection


# 获取基准股本时间序列
from windget import getRightsIssueBaseShareSeries


# 获取基准股本
from windget import getRightsIssueBaseShare


# 获取每股配股数时间序列
from windget import getRightsIssuePerShareSeries


# 获取每股配股数
from windget import getRightsIssuePerShare


# 获取计划配股数时间序列
from windget import getRightsIssuePlanAmtSeries


# 获取计划配股数
from windget import getRightsIssuePlanAmt


# 获取实际配股数时间序列
from windget import getRightsIssueAmountSeries


# 获取实际配股数
from windget import getRightsIssueAmount


# 获取国有股实际配股数时间序列
from windget import getRightsIssueActLNumToStateSeries


# 获取国有股实际配股数
from windget import getRightsIssueActLNumToState


# 获取法人股实际配股数时间序列
from windget import getRightsIssueActLNumToJurSeries


# 获取法人股实际配股数
from windget import getRightsIssueActLNumToJur


# 获取职工股实际配股数时间序列
from windget import getRightsIssueActLNumToEmpSeries


# 获取职工股实际配股数
from windget import getRightsIssueActLNumToEmp


# 获取转配股实际配股数时间序列
from windget import getRightsIssueActLNumToTRsfSeries


# 获取转配股实际配股数
from windget import getRightsIssueActLNumToTRsf


# 获取已流通股实际配股数时间序列
from windget import getRightsIssueActLNumToTrDSeries


# 获取已流通股实际配股数
from windget import getRightsIssueActLNumToTrD


# 获取国有股理论配股数时间序列
from windget import getRightsIssueTheOrNumToStateSeries


# 获取国有股理论配股数
from windget import getRightsIssueTheOrNumToState


# 获取法人股理论配股数时间序列
from windget import getRightsIssueTheOrNumToJurSeries


# 获取法人股理论配股数
from windget import getRightsIssueTheOrNumToJur


# 获取职工股理论配股数时间序列
from windget import getRightsIssueTheOrNumToEmpSeries


# 获取职工股理论配股数
from windget import getRightsIssueTheOrNumToEmp


# 获取转配股理论配股数时间序列
from windget import getRightsIssueTheOrNumToTRsfSeries


# 获取转配股理论配股数
from windget import getRightsIssueTheOrNumToTRsf


# 获取已流通股理论配股数时间序列
from windget import getRightsIssueTheOrNumToTrDSeries


# 获取已流通股理论配股数
from windget import getRightsIssueTheOrNumToTrD


# 获取持股5%以上大股东持股数时间序列
from windget import getRightsIssueUp5PctNumSeries


# 获取持股5%以上大股东持股数
from windget import getRightsIssueUp5PctNum


# 获取持股5%以上的大股东理论认购股数时间序列
from windget import getRightsIssueUp5PctTheOrNumSeries


# 获取持股5%以上的大股东理论认购股数
from windget import getRightsIssueUp5PctTheOrNum


# 获取持股5%以上大股东认购股数时间序列
from windget import getRightsIssueUp5PctActLNumSeries


# 获取持股5%以上大股东认购股数
from windget import getRightsIssueUp5PctActLNum


# 获取配股除权日时间序列
from windget import getRightsIssueExDividendDateSeries


# 获取配股除权日
from windget import getRightsIssueExDividendDate


# 获取配股上市日时间序列
from windget import getRightsIssueListedDateSeries


# 获取配股上市日
from windget import getRightsIssueListedDate


# 获取缴款起始日时间序列
from windget import getTenderPaymentDateSeries


# 获取缴款起始日
from windget import getTenderPaymentDate


# 获取缴款终止日时间序列
from windget import getRightsIssuePayEnddateSeries


# 获取缴款终止日
from windget import getRightsIssuePayEnddate


# 获取配股获准公告日时间序列
from windget import getRightsIssueApprovedDateSeries


# 获取配股获准公告日
from windget import getRightsIssueApprovedDate


# 获取配股公告日时间序列
from windget import getRightsIssueAnnCeDateSeries


# 获取配股公告日
from windget import getRightsIssueAnnCeDate


# 获取配股受理日时间序列
from windget import getHandlingDateRsSeries


# 获取配股受理日
from windget import getHandlingDateRs


# 获取配股主承销商时间序列
from windget import getRightsIssueLeadUndRSeries


# 获取配股主承销商
from windget import getRightsIssueLeadUndR


# 获取配股方式时间序列
from windget import getRightsIssueTypeSeries


# 获取配股方式
from windget import getRightsIssueType


# 获取配股承销方式时间序列
from windget import getRightsIssueUndRTypeSeries


# 获取配股承销方式
from windget import getRightsIssueUndRType


# 获取配股分销商时间序列
from windget import getRightsIssueDeputyUndRSeries


# 获取配股分销商
from windget import getRightsIssueDeputyUndR


# 获取配股预案价上限时间序列
from windget import getRightsIssueMaxPricePrePlanSeries


# 获取配股预案价上限
from windget import getRightsIssueMaxPricePrePlan


# 获取配股预案价下限时间序列
from windget import getRightsIssueMinPricePrePlanSeries


# 获取配股预案价下限
from windget import getRightsIssueMinPricePrePlan


# 获取招投标日期时间序列
from windget import getTenderTenderDateSeries


# 获取招投标日期
from windget import getTenderTenderDate


# 获取发行起始日期时间序列
from windget import getIssueFirstIssueSeries


# 获取发行起始日期
from windget import getIssueFirstIssue


# 获取网上发行起始日期时间序列
from windget import getIssueFirstIssueOlSeries


# 获取网上发行起始日期
from windget import getIssueFirstIssueOl


# 获取发行截止日期时间序列
from windget import getIssueLastIssueSeries


# 获取发行截止日期
from windget import getIssueLastIssue


# 获取网上发行截止日期时间序列
from windget import getIssueLastIssueOlSeries


# 获取网上发行截止日期
from windget import getIssueLastIssueOl


# 获取分销起始日期时间序列
from windget import getTenderDistRibBeginSeries


# 获取分销起始日期
from windget import getTenderDistRibBegin


# 获取分销截至日期时间序列
from windget import getTenderDIsTribeNdSeries


# 获取分销截至日期
from windget import getTenderDIsTribeNd


# 获取缴款截止日时间序列
from windget import getTenderPayEnddateSeries


# 获取缴款截止日
from windget import getTenderPayEnddate


# 获取资金到账确认时间时间序列
from windget import getTenderConfirmDateSeries


# 获取资金到账确认时间
from windget import getTenderConfirmDate


# 获取债券过户时间时间序列
from windget import getTenderTransferDateSeries


# 获取债券过户时间
from windget import getTenderTransferDate


# 获取证监会/发改委批文日时间序列
from windget import getIssueOfficialDocDateSeries


# 获取证监会/发改委批文日
from windget import getIssueOfficialDocDate


# 获取发行注册日期时间序列
from windget import getIssueRegDateSeries


# 获取发行注册日期
from windget import getIssueRegDate


# 获取发行注册文件号时间序列
from windget import getIssueRegNumberSeries


# 获取发行注册文件号
from windget import getIssueRegNumber


# 获取发行注册额度时间序列
from windget import getIssueRegAmountSeries


# 获取发行注册额度
from windget import getIssueRegAmount


# 获取发行年度时间序列
from windget import getIssueIssueYearSeries


# 获取发行年度
from windget import getIssueIssueYear


# 获取发行期号时间序列
from windget import getIssueIssueNumberSeries


# 获取发行期号
from windget import getIssueIssueNumber


# 获取招标场所时间序列
from windget import getTenderExchangeSeries


# 获取招标场所
from windget import getTenderExchange


# 获取承销方式时间序列
from windget import getAgencyUnderWritTypeSeries


# 获取承销方式
from windget import getAgencyUnderWritType


# 获取发行价格时间序列
from windget import getIssueIssuePriceSeries


# 获取发行价格
from windget import getIssueIssuePrice


# 获取最终发行价格时间序列
from windget import getTendRstFinalPriceSeries


# 获取最终发行价格
from windget import getTendRstFinalPrice


# 获取网上发行认购数量限制说明时间序列
from windget import getIssueRarAIsOlSeries


# 获取网上发行认购数量限制说明
from windget import getIssueRarAIsOl


# 获取募集资金用途时间序列
from windget import getFundUseSeries


# 获取募集资金用途
from windget import getFundUse


# 获取招标方式时间序列
from windget import getTenderMethodSeries


# 获取招标方式
from windget import getTenderMethod


# 获取招标标的时间序列
from windget import getTenderObjectSeries


# 获取招标标的
from windget import getTenderObject


# 获取招标对象时间序列
from windget import getTenderAimInvStSeries


# 获取招标对象
from windget import getTenderAimInvSt


# 获取招标时间时间序列
from windget import getTenderTimeSeries


# 获取招标时间
from windget import getTenderTime


# 获取中标确定方式说明时间序列
from windget import getTenderExplanationSeries


# 获取中标确定方式说明
from windget import getTenderExplanation


# 获取竞争性招标总额时间序列
from windget import getTenderCmpTamNtSeries


# 获取竞争性招标总额
from windget import getTenderCmpTamNt


# 获取基本承销额度时间序列
from windget import getTenderUnderwritingSeries


# 获取基本承销额度
from windget import getTenderUnderwriting


# 获取基本承销额追加比例时间序列
from windget import getTenderAddRatioSeries


# 获取基本承销额追加比例
from windget import getTenderAddRatio


# 获取基本承销额增加权利时间序列
from windget import getTenderAdditiveRightsSeries


# 获取基本承销额增加权利
from windget import getTenderAdditiveRights


# 获取投标利率下限时间序列
from windget import getTenderThresholdSeries


# 获取投标利率下限
from windget import getTenderThreshold


# 获取投标利率上限时间序列
from windget import getTenderCeilingSeries


# 获取投标利率上限
from windget import getTenderCeiling


# 获取基本投标单位时间序列
from windget import getTenderTenderUnitSeries


# 获取基本投标单位
from windget import getTenderTenderUnit


# 获取每标位最低投标量时间序列
from windget import getTenderLowestAmNtSeries


# 获取每标位最低投标量
from windget import getTenderLowestAmNt


# 获取每标位最高投标量时间序列
from windget import getTenderHighestAmNtSeries


# 获取每标位最高投标量
from windget import getTenderHighestAmNt


# 获取投标说明时间序列
from windget import getTenderExpLnTenderSeries


# 获取投标说明
from windget import getTenderExpLnTender


# 获取是否发行失败时间序列
from windget import getIssueOkSeries


# 获取是否发行失败
from windget import getIssueOk


# 获取招标书编号时间序列
from windget import getTendRstDoCumTNumberSeries


# 获取招标书编号
from windget import getTendRstDoCumTNumber


# 获取缴款总金额时间序列
from windget import getTendRstPayAmountSeries


# 获取缴款总金额
from windget import getTendRstPayAmount


# 获取基本承购总额时间序列
from windget import getTendRstUnderwritingSeries


# 获取基本承购总额
from windget import getTendRstUnderwriting


# 获取招标总量时间序列
from windget import getTendRstAmNtSeries


# 获取招标总量
from windget import getTendRstAmNt


# 获取投标(申购)总量时间序列
from windget import getTendRstTenderAmountSeries


# 获取投标(申购)总量
from windget import getTendRstTenderAmount


# 获取应投家数时间序列
from windget import getTendRstOughtTenderSeries


# 获取应投家数
from windget import getTendRstOughtTender


# 获取投标家数时间序列
from windget import getTendRstInvestorTenderedSeries


# 获取投标家数
from windget import getTendRstInvestorTendered


# 获取有效投标(申购)家数时间序列
from windget import getTendRstEffectInvestorsSeries


# 获取有效投标(申购)家数
from windget import getTendRstEffectInvestors


# 获取投标笔数时间序列
from windget import getTendRstTendersSeries


# 获取投标笔数
from windget import getTendRstTenders


# 获取有效笔数时间序列
from windget import getTendRstEffectTenderSeries


# 获取有效笔数
from windget import getTendRstEffectTender


# 获取无效笔数时间序列
from windget import getTendRstInEffectTenderSeries


# 获取无效笔数
from windget import getTendRstInEffectTender


# 获取有效投标总量时间序列
from windget import getTendRstEffectAmNtSeries


# 获取有效投标总量
from windget import getTendRstEffectAmNt


# 获取最高投标价位时间序列
from windget import getTendRstHightestSeries


# 获取最高投标价位
from windget import getTendRstHightest


# 获取最低投标价位时间序列
from windget import getTendRstLowestSeries


# 获取最低投标价位
from windget import getTendRstLowest


# 获取中标总量时间序列
from windget import getTendRstWinningAmNtSeries


# 获取中标总量
from windget import getTendRstWinningAmNt


# 获取自营中标总量时间序列
from windget import getTendRstPrivateTradeSeries


# 获取自营中标总量
from windget import getTendRstPrivateTrade


# 获取边际中标价位中标总量时间序列
from windget import getTendRstMarGwInBidderSeries


# 获取边际中标价位中标总量
from windget import getTendRstMarGwInBidder


# 获取中标家数时间序列
from windget import getTendRstWinnerBidderSeries


# 获取中标家数
from windget import getTendRstWinnerBidder


# 获取中标笔数时间序列
from windget import getTendRstWinningBidderSeries


# 获取中标笔数
from windget import getTendRstWinningBidder


# 获取最高中标价位时间序列
from windget import getTendRstHightPriceSeries


# 获取最高中标价位
from windget import getTendRstHightPrice


# 获取最低中标价位时间序列
from windget import getTendRstLowPriceSeries


# 获取最低中标价位
from windget import getTendRstLowPrice


# 获取边际中标价位投标总量时间序列
from windget import getTendRstMargaMNtSeries


# 获取边际中标价位投标总量
from windget import getTendRstMargaMNt


# 获取参考收益率时间序列
from windget import getTendRstReferYieldSeries


# 获取参考收益率
from windget import getTendRstReferYield


# 获取最终票面利率时间序列
from windget import getTendRstFinAnCouponSeries


# 获取最终票面利率
from windget import getTendRstFinAnCoupon


# 获取全场中标利率时间序列
from windget import getTendRstBidRateSeries


# 获取全场中标利率
from windget import getTendRstBidRate


# 获取全场中标价格时间序列
from windget import getTendRstBidPriceSeries


# 获取全场中标价格
from windget import getTendRstBidPrice


# 获取全场中标利差时间序列
from windget import getTendRstBidSpreadSeries


# 获取全场中标利差
from windget import getTendRstBidSpread


# 获取超额认购倍数时间序列
from windget import getIpoOvRSubRatioSeries


# 获取超额认购倍数
from windget import getIpoOvRSubRatio


# 获取网上发行超额认购倍数(不含优先配售)时间序列
from windget import getCbListExcessPcHonLSeries


# 获取网上发行超额认购倍数(不含优先配售)
from windget import getCbListExcessPcHonL


# 获取主承销商时间序列
from windget import getAgencyLeadUnderwriterSeries


# 获取主承销商
from windget import getAgencyLeadUnderwriter


# 获取主承销商(简称)时间序列
from windget import getAgencyLeadUnderwritersNSeries


# 获取主承销商(简称)
from windget import getAgencyLeadUnderwritersN


# 获取副主承销商时间序列
from windget import getAgencyDeputyUnderwriterSeries


# 获取副主承销商
from windget import getAgencyDeputyUnderwriter


# 获取信用评估机构时间序列
from windget import getCreditRatingAgencySeries


# 获取信用评估机构
from windget import getCreditRatingAgency


# 获取簿记管理人时间序列
from windget import getAgencyBookRunnerSeries


# 获取簿记管理人
from windget import getAgencyBookRunner


# 获取分销商时间序列
from windget import getAgencyDistributorSeries


# 获取分销商
from windget import getAgencyDistributor


# 获取托管人时间序列
from windget import getAgencyTrusteeSeries


# 获取托管人
from windget import getAgencyTrustee


# 获取受托管理人时间序列
from windget import getAgencyBondTrusteeSeries


# 获取受托管理人
from windget import getAgencyBondTrustee


# 获取会计师事务所时间序列
from windget import getAgencyExAccountantSeries


# 获取会计师事务所
from windget import getAgencyExAccountant


# 获取上市保荐机构(上市推荐人)时间序列
from windget import getAgencyRecommendErSeries


# 获取上市保荐机构(上市推荐人)
from windget import getAgencyRecommendEr


# 获取账簿管理人(海外)时间序列
from windget import getAgencyBookkeeperSeries


# 获取账簿管理人(海外)
from windget import getAgencyBookkeeper


# 获取牵头经办人(海外)时间序列
from windget import getAgencyUnderwriterSeries


# 获取牵头经办人(海外)
from windget import getAgencyUnderwriter


# 获取集中簿记建档系统技术支持机构时间序列
from windget import getAgencyBookSupporterSeries


# 获取集中簿记建档系统技术支持机构
from windget import getAgencyBookSupporter


# 获取绿色债券认证机构时间序列
from windget import getAgencyCertificationSeries


# 获取绿色债券认证机构
from windget import getAgencyCertification


# 获取募集资金专项账户开户行时间序列
from windget import getAgencyFundBankSeries


# 获取募集资金专项账户开户行
from windget import getAgencyFundBank


# 获取发行费率时间序列
from windget import getIssueFeeSeries


# 获取发行费率
from windget import getIssueFee


# 获取承揽费时间序列
from windget import getTenderUnderwritingCostSeries


# 获取承揽费
from windget import getTenderUnderwritingCost


# 获取承销保荐费用时间序列
from windget import getIssueFeeUnderWRtspOnSeries


# 获取承销保荐费用
from windget import getIssueFeeUnderWRtspOn


# 获取会计师费用时间序列
from windget import getIssueFeeAcContSeries


# 获取会计师费用
from windget import getIssueFeeAcCont


# 获取律师费用时间序列
from windget import getIssueFeeLegalConsLSeries


# 获取律师费用
from windget import getIssueFeeLegalConsL


# 获取兑付手续费时间序列
from windget import getTenderCommissionChargeSeries


# 获取兑付手续费
from windget import getTenderCommissionCharge


# 获取发审委审批通过日期时间序列
from windget import getCbListPermitDateSeries


# 获取发审委审批通过日期
from windget import getCbListPermitDate


# 获取老股东配售日期时间序列
from windget import getCbListRationDateSeries


# 获取老股东配售日期
from windget import getCbListRationDate


# 获取老股东配售缴款日时间序列
from windget import getCbListRationPayMtDateSeries


# 获取老股东配售缴款日
from windget import getCbListRationPayMtDate


# 获取老股东配售说明时间序列
from windget import getCbResultExpLnRationSeries


# 获取老股东配售说明
from windget import getCbResultExpLnRation


# 获取老股东配售代码时间序列
from windget import getCbListRationCodeSeries


# 获取老股东配售代码
from windget import getCbListRationCode


# 获取老股东配售简称时间序列
from windget import getCbListRationNameSeries


# 获取老股东配售简称
from windget import getCbListRationName


# 获取老股东配售价格时间序列
from windget import getCbListRationPriceSeries


# 获取老股东配售价格
from windget import getCbListRationPrice


# 获取老股东配售比例分母时间序列
from windget import getCbListRationRatioDeSeries


# 获取老股东配售比例分母
from windget import getCbListRationRatioDe


# 获取每股配售额时间序列
from windget import getCbResultRationAmtSeries


# 获取每股配售额
from windget import getCbResultRationAmt


# 获取向老股东配售数量时间序列
from windget import getCbListRationVolSeries


# 获取向老股东配售数量
from windget import getCbListRationVol


# 获取老股东配售户数时间序列
from windget import getCbListOriginalsSeries


# 获取老股东配售户数
from windget import getCbListOriginals


# 获取网上发行申购代码时间序列
from windget import getCbListPChaseCodeOnLSeries


# 获取网上发行申购代码
from windget import getCbListPChaseCodeOnL


# 获取网上发行申购名称时间序列
from windget import getCbListPChNameOnLSeries


# 获取网上发行申购名称
from windget import getCbListPChNameOnL


# 获取网上发行申购价格时间序列
from windget import getCbListPChPriceOnLSeries


# 获取网上发行申购价格
from windget import getCbListPChPriceOnL


# 获取网下向机构投资者发行数量(不含优先配售)时间序列
from windget import getCbListVolInStOffSeries


# 获取网下向机构投资者发行数量(不含优先配售)
from windget import getCbListVolInStOff


# 获取定金比例时间序列
from windget import getCbResultRationCodeSeries


# 获取定金比例
from windget import getCbResultRationCode


# 获取网下申购下限时间序列
from windget import getListFloorSubsCrOfFlSeries


# 获取网下申购下限
from windget import getListFloorSubsCrOfFl


# 获取网下申购上限时间序列
from windget import getListLimitSubsCrOfFlSeries


# 获取网下申购上限
from windget import getListLimitSubsCrOfFl


# 获取网上申购下限时间序列
from windget import getListFloorSubsCroNlSeries


# 获取网上申购下限
from windget import getListFloorSubsCroNl


# 获取网上申购步长时间序列
from windget import getListStepSizeSubsCroNlSeries


# 获取网上申购步长
from windget import getListStepSizeSubsCroNl


# 获取网上申购上限时间序列
from windget import getListLimitSubsCroNlSeries


# 获取网上申购上限
from windget import getListLimitSubsCroNl


# 获取原流通股股东可配售额时间序列
from windget import getCbResultAVaiRationAmtTrAdSeries


# 获取原流通股股东可配售额
from windget import getCbResultAVaiRationAmtTrAd


# 获取原流通股股东有效申购户数时间序列
from windget import getCbResultEfInvestorsSeries


# 获取原流通股股东有效申购户数
from windget import getCbResultEfInvestors


# 获取原流通股股东有效申购金额时间序列
from windget import getCbResultEfSubsCrPamTSeries


# 获取原流通股股东有效申购金额
from windget import getCbResultEfSubsCrPamT


# 获取原流通股股东获配金额时间序列
from windget import getCbResultPlaceAmNttRadSeries


# 获取原流通股股东获配金额
from windget import getCbResultPlaceAmNttRad


# 获取网上有效申购户数时间序列
from windget import getCbResultEfSubsCRpoNlSeries


# 获取网上有效申购户数
from windget import getCbResultEfSubsCRpoNl


# 获取网上有效申购金额时间序列
from windget import getCbResultEfSubsCrPamToNlSeries


# 获取网上有效申购金额
from windget import getCbResultEfSubsCrPamToNl


# 获取网上获配金额时间序列
from windget import getCbResultRationAmToNlSeries


# 获取网上获配金额
from windget import getCbResultRationAmToNl


# 获取网上获配比例时间序列
from windget import getCbResultRationRatioOnLSeries


# 获取网上获配比例
from windget import getCbResultRationRatioOnL


# 获取网上中签率时间序列
from windget import getCbResultSuCrateOnLSeries


# 获取网上中签率
from windget import getCbResultSuCrateOnL


# 获取网下有效申购户数时间序列
from windget import getCbResultEfSubsCRpOffSeries


# 获取网下有效申购户数
from windget import getCbResultEfSubsCRpOff


# 获取网下有效申购金额时间序列
from windget import getCbResultEfSubsCrPamToFfSeries


# 获取网下有效申购金额
from windget import getCbResultEfSubsCrPamToFf


# 获取网下获配金额时间序列
from windget import getCbResultRationAmtOffSeries


# 获取网下获配金额
from windget import getCbResultRationAmtOff


# 获取网下中签率时间序列
from windget import getCbResultSuCrateOffSeries


# 获取网下中签率
from windget import getCbResultSuCrateOff


# 获取包销余额时间序列
from windget import getCbResultBalanceSeries


# 获取包销余额
from windget import getCbResultBalance


# 获取重仓行业投资市值(中信)时间序列
from windget import getPrtTopIndustryValueCitiCSeries


# 获取重仓行业投资市值(中信)
from windget import getPrtTopIndustryValueCitiC


# 获取重仓行业投资市值(申万)时间序列
from windget import getPrtTopIndustryValueSwSeries


# 获取重仓行业投资市值(申万)
from windget import getPrtTopIndustryValueSw


# 获取第三方审查机构时间序列
from windget import getEsGMdc01003Series


# 获取第三方审查机构
from windget import getEsGMdc01003


# 获取报告范围时间序列
from windget import getEsGMdc01004Series


# 获取报告范围
from windget import getEsGMdc01004


# 获取编制依据时间序列
from windget import getEsGMdc01005Series


# 获取编制依据
from windget import getEsGMdc01005


# 获取是否遵循/对照联交所标准时间序列
from windget import getEsGMdc01007Series


# 获取是否遵循/对照联交所标准
from windget import getEsGMdc01007


# 获取总温室气体排放时间序列
from windget import getEsGEem01004Series


# 获取总温室气体排放
from windget import getEsGEem01004


# 获取温室气体减排量时间序列
from windget import getEsGEem01008Series


# 获取温室气体减排量
from windget import getEsGEem01008


# 获取是否就气候变化机会进行讨论时间序列
from windget import getEsGEem01011Series


# 获取是否就气候变化机会进行讨论
from windget import getEsGEem01011


# 获取是否就气候变化风险进行讨论时间序列
from windget import getEsGEem01012Series


# 获取是否就气候变化风险进行讨论
from windget import getEsGEem01012


# 获取氮氧化物排放时间序列
from windget import getEsGEem02001Series


# 获取氮氧化物排放
from windget import getEsGEem02001


# 获取二氧化硫排放时间序列
from windget import getEsGEem02002Series


# 获取二氧化硫排放
from windget import getEsGEem02002


# 获取悬浮粒子/颗粒物时间序列
from windget import getEsGEem02003Series


# 获取悬浮粒子/颗粒物
from windget import getEsGEem02003


# 获取有害废弃物量时间序列
from windget import getEsGEem03001Series


# 获取有害废弃物量
from windget import getEsGEem03001


# 获取无害废弃物量时间序列
from windget import getEsGEem03002Series


# 获取无害废弃物量
from windget import getEsGEem03002


# 获取废弃物总量时间序列
from windget import getEsGEem03003Series


# 获取废弃物总量
from windget import getEsGEem03003


# 获取废弃物回收量时间序列
from windget import getEsGEem03004Series


# 获取废弃物回收量
from windget import getEsGEem03004


# 获取总能源消耗时间序列
from windget import getEsGEre01001Series


# 获取总能源消耗
from windget import getEsGEre01001


# 获取耗电总量时间序列
from windget import getEsGEre01002Series


# 获取耗电总量
from windget import getEsGEre01002


# 获取节省用电量时间序列
from windget import getEsGEre01003Series


# 获取节省用电量
from windget import getEsGEre01003


# 获取煤碳使用量时间序列
from windget import getEsGEre01004Series


# 获取煤碳使用量
from windget import getEsGEre01004


# 获取天然气消耗时间序列
from windget import getEsGEre01005Series


# 获取天然气消耗
from windget import getEsGEre01005


# 获取燃油消耗时间序列
from windget import getEsGEre01006Series


# 获取燃油消耗
from windget import getEsGEre01006


# 获取节能量时间序列
from windget import getEsGEre01007Series


# 获取节能量
from windget import getEsGEre01007


# 获取纸消耗量时间序列
from windget import getEsGEre02001Series


# 获取纸消耗量
from windget import getEsGEre02001


# 获取废纸回收量时间序列
from windget import getEsGEre02002Series


# 获取废纸回收量
from windget import getEsGEre02002


# 获取总用水量时间序列
from windget import getEsGEwa01001Series


# 获取总用水量
from windget import getEsGEwa01001


# 获取节省水量时间序列
from windget import getEsGEwa01002Series


# 获取节省水量
from windget import getEsGEwa01002


# 获取水循环与再利用的总量时间序列
from windget import getEsGEwa01003Series


# 获取水循环与再利用的总量
from windget import getEsGEwa01003


# 获取废水/污水排放量时间序列
from windget import getEsGEwa02002Series


# 获取废水/污水排放量
from windget import getEsGEwa02002


# 获取废水处理量时间序列
from windget import getEsGEwa02003Series


# 获取废水处理量
from windget import getEsGEwa02003


# 获取氨氮时间序列
from windget import getEsGEwa02004Series


# 获取氨氮
from windget import getEsGEwa02004


# 获取是否重点排污单位时间序列
from windget import getEsGEot01003Series


# 获取是否重点排污单位
from windget import getEsGEot01003


# 获取环保超标或其他违规次数时间序列
from windget import getEsGEot02002Series


# 获取环保超标或其他违规次数
from windget import getEsGEot02002


# 获取董事会规模时间序列
from windget import getEsGGBo01001Series


# 获取董事会规模
from windget import getEsGGBo01001


# 获取董事会出席率时间序列
from windget import getEsGGBo01002Series


# 获取董事会出席率
from windget import getEsGGBo01002


# 获取董事会召开数时间序列
from windget import getEsGGBo01003Series


# 获取董事会召开数
from windget import getEsGGBo01003


# 获取参加少于75%会议的董事人数时间序列
from windget import getEsGGBo01004Series


# 获取参加少于75%会议的董事人数
from windget import getEsGGBo01004


# 获取监事会召开数时间序列
from windget import getEsGGBo01005Series


# 获取监事会召开数
from windget import getEsGGBo01005


# 获取监事出席率时间序列
from windget import getEsGGBo01006Series


# 获取监事出席率
from windget import getEsGGBo01006


# 获取是否设有监事委员会主席时间序列
from windget import getEsGGBo01007Series


# 获取是否设有监事委员会主席
from windget import getEsGGBo01007


# 获取提名委员会会议数时间序列
from windget import getEsGGBo01008Series


# 获取提名委员会会议数
from windget import getEsGGBo01008


# 获取提名委员会会议出席率时间序列
from windget import getEsGGBo01010Series


# 获取提名委员会会议出席率
from windget import getEsGGBo01010


# 获取董事会成员受教育背景高于本科的比例时间序列
from windget import getEsGGBo01014Series


# 获取董事会成员受教育背景高于本科的比例
from windget import getEsGGBo01014


# 获取女性董事占比时间序列
from windget import getEsGGBo01015Series


# 获取女性董事占比
from windget import getEsGGBo01015


# 获取独立董事董事会会议出席率时间序列
from windget import getEsGGBo03001Series


# 获取独立董事董事会会议出席率
from windget import getEsGGBo03001


# 获取独立董事占董事会总人数的比例时间序列
from windget import getEsGGBo03002Series


# 获取独立董事占董事会总人数的比例
from windget import getEsGGBo03002


# 获取是否有股权激励计划时间序列
from windget import getEsGGpa02001Series


# 获取是否有股权激励计划
from windget import getEsGGpa02001


# 获取薪酬委员会会议出席率时间序列
from windget import getEsGGpa03002Series


# 获取薪酬委员会会议出席率
from windget import getEsGGpa03002


# 获取薪酬委员会会议数时间序列
from windget import getEsGGpa03003Series


# 获取薪酬委员会会议数
from windget import getEsGGpa03003


# 获取审计委员会会议次数时间序列
from windget import getEsGGad01001Series


# 获取审计委员会会议次数
from windget import getEsGGad01001


# 获取审计委员会会议出席率时间序列
from windget import getEsGGad01002Series


# 获取审计委员会会议出席率
from windget import getEsGGad01002


# 获取是否出具标准无保留意见时间序列
from windget import getEsGGad02002Series


# 获取是否出具标准无保留意见
from windget import getEsGGad02002


# 获取雇员总人数时间序列
from windget import getEsGSem01001Series


# 获取雇员总人数
from windget import getEsGSem01001


# 获取员工流失率/离职率时间序列
from windget import getEsGSem01002Series


# 获取员工流失率/离职率
from windget import getEsGSem01002


# 获取劳动合同签订率时间序列
from windget import getEsGSem01004Series


# 获取劳动合同签订率
from windget import getEsGSem01004


# 获取女性员工比例时间序列
from windget import getEsGSem01005Series


# 获取女性员工比例
from windget import getEsGSem01005


# 获取少数裔员工比例时间序列
from windget import getEsGSem01006Series


# 获取少数裔员工比例
from windget import getEsGSem01006


# 获取人均培训课时时间序列
from windget import getEsGSem02002Series


# 获取人均培训课时
from windget import getEsGSem02002


# 获取工伤率时间序列
from windget import getEsGSem03001Series


# 获取工伤率
from windget import getEsGSem03001


# 获取因工伤损失工作日数时间序列
from windget import getEsGSem03002Series


# 获取因工伤损失工作日数
from windget import getEsGSem03002


# 获取职业病发生率时间序列
from windget import getEsGSem03003Series


# 获取职业病发生率
from windget import getEsGSem03003


# 获取死亡事故数时间序列
from windget import getEsGSem03004Series


# 获取死亡事故数
from windget import getEsGSem03004


# 获取医保覆盖率时间序列
from windget import getEsGSem04001Series


# 获取医保覆盖率
from windget import getEsGSem04001


# 获取客户投诉数量时间序列
from windget import getEsGSpc01001Series


# 获取客户投诉数量
from windget import getEsGSpc01001


# 获取客户满意度时间序列
from windget import getEsGSpc01002Series


# 获取客户满意度
from windget import getEsGSpc01002


# 获取是否有客户反馈系统时间序列
from windget import getEsGSpc01003Series


# 获取是否有客户反馈系统
from windget import getEsGSpc01003


# 获取新增专利数时间序列
from windget import getEsGSpc02004Series


# 获取新增专利数
from windget import getEsGSpc02004


# 获取供应商数量时间序列
from windget import getEsGSch01001Series


# 获取供应商数量
from windget import getEsGSch01001


# 获取(废弃)接受ESG评估的供应商数量时间序列
from windget import getEsGSch02002Series


# 获取(废弃)接受ESG评估的供应商数量
from windget import getEsGSch02002


# 获取供应商本地化比例时间序列
from windget import getEsGSch01002Series


# 获取供应商本地化比例
from windget import getEsGSch01002


# 获取本地化采购支出占比时间序列
from windget import getEsGSch02001Series


# 获取本地化采购支出占比
from windget import getEsGSch02001


# 获取志愿服务时长时间序列
from windget import getEsGSco02001Series


# 获取志愿服务时长
from windget import getEsGSco02001


# 获取注册志愿者人数时间序列
from windget import getEsGSco02002Series


# 获取注册志愿者人数
from windget import getEsGSco02002


# 获取被调研总次数时间序列
from windget import getIrNosSeries


# 获取被调研总次数
from windget import getIrNos


# 获取特定对象调研次数时间序列
from windget import getIrNoSfSoSeries


# 获取特定对象调研次数
from windget import getIrNoSfSo


# 获取媒体(政府)调研家数时间序列
from windget import getIrNoMiSeries


# 获取媒体(政府)调研家数
from windget import getIrNoMi


# 获取个人调研家数时间序列
from windget import getIrNoPiSeries


# 获取个人调研家数
from windget import getIrNoPi


# 获取证券公司调研次数时间序列
from windget import getIrNosCbsCSeries


# 获取证券公司调研次数
from windget import getIrNosCbsC


# 获取证券公司调研家数时间序列
from windget import getIrNoiIsCSeries


# 获取证券公司调研家数
from windget import getIrNoiIsC


# 获取调研最多的证券公司时间序列
from windget import getIrTmsScSeries


# 获取调研最多的证券公司
from windget import getIrTmsSc


# 获取保险资管调研次数时间序列
from windget import getIrNoSoIamSeries


# 获取保险资管调研次数
from windget import getIrNoSoIam


# 获取保险资管调研家数时间序列
from windget import getIrNoiAmiSeries


# 获取保险资管调研家数
from windget import getIrNoiAmi


# 获取调研最多的保险资管时间序列
from windget import getIrTMriAmSeries


# 获取调研最多的保险资管
from windget import getIrTMriAm


# 获取调研最多的投资机构时间序列
from windget import getIrTMrIiSeries


# 获取调研最多的投资机构
from windget import getIrTMrIi


# 获取调研最多的外资机构时间序列
from windget import getIrTMrFiSeries


# 获取调研最多的外资机构
from windget import getIrTMrFi


# 获取其他公司调研次数时间序列
from windget import getIrNosBocSeries


# 获取其他公司调研次数
from windget import getIrNosBoc


# 获取其他公司调研家数时间序列
from windget import getIrNoIfOcSeries


# 获取其他公司调研家数
from windget import getIrNoIfOc


# 获取调研最多的其他公司时间序列
from windget import getIrOcMrSeries


# 获取调研最多的其他公司
from windget import getIrOcMr


# 获取出生年份时间序列
from windget import getFundManagerBirthYearSeries


# 获取出生年份
from windget import getFundManagerBirthYear


# 获取年龄时间序列
from windget import getFundManagerAgeSeries


# 获取年龄
from windget import getFundManagerAge


# 获取学历时间序列
from windget import getFundManagerEducationSeries


# 获取学历
from windget import getFundManagerEducation


# 获取国籍时间序列
from windget import getFundManagerNationalitySeries


# 获取国籍
from windget import getFundManagerNationality


# 获取简历时间序列
from windget import getFundManagerResumeSeries


# 获取简历
from windget import getFundManagerResume


# 获取性别时间序列
from windget import getFundManagerGenderSeries


# 获取性别
from windget import getFundManagerGender


# 获取任职日期时间序列
from windget import getFundManagerStartDateSeries


# 获取任职日期
from windget import getFundManagerStartDate


# 获取任职天数时间序列
from windget import getFundManagerOnThePostDaysSeries


# 获取任职天数
from windget import getFundManagerOnThePostDays


# 获取证券从业日期时间序列
from windget import getFundManagerStartDateOfManagerCareerSeries


# 获取证券从业日期
from windget import getFundManagerStartDateOfManagerCareer


# 获取历任基金数时间序列
from windget import getFundManagerPreviousFundNoSeries


# 获取历任基金数
from windget import getFundManagerPreviousFundNo


# 获取任职基金数时间序列
from windget import getFundManagerFundNoSeries


# 获取任职基金数
from windget import getFundManagerFundNo


# 获取任职基金代码时间序列
from windget import getFundManagerFundCodesSeries


# 获取任职基金代码
from windget import getFundManagerFundCodes


# 获取任职基金总规模时间序列
from windget import getFundManagerTotalNetAssetSeries


# 获取任职基金总规模
from windget import getFundManagerTotalNetAsset


# 获取任职基金总规模(支持历史)时间序列
from windget import getFundManagerTotalNetAsset2Series


# 获取任职基金总规模(支持历史)
from windget import getFundManagerTotalNetAsset2


# 获取离职日期时间序列
from windget import getFundManagerEnddateSeries


# 获取离职日期
from windget import getFundManagerEnddate


# 获取离任原因时间序列
from windget import getFundManagerResignationReasonSeries


# 获取离任原因
from windget import getFundManagerResignationReason


# 获取投资经理背景时间序列
from windget import getFundManagerBackgroundSeries


# 获取投资经理背景
from windget import getFundManagerBackground


# 获取任职基金获奖记录时间序列
from windget import getFundManagerAwardRecordSeries


# 获取任职基金获奖记录
from windget import getFundManagerAwardRecord


# 获取履任以来获奖总次数时间序列
from windget import getFundManagerAwardRecordNumSeries


# 获取履任以来获奖总次数
from windget import getFundManagerAwardRecordNum


# 获取超越基准总回报时间序列
from windget import getFundManagerTotalReturnOverBenchmarkSeries


# 获取超越基准总回报
from windget import getFundManagerTotalReturnOverBenchmark


# 获取任职年化回报时间序列
from windget import getNavPeriodicAnnualIZedReturnSeries


# 获取任职年化回报
from windget import getNavPeriodicAnnualIZedReturn


# 获取任期最大回报时间序列
from windget import getFundManagerMaxReturnSeries


# 获取任期最大回报
from windget import getFundManagerMaxReturn


# 获取现任基金最佳回报时间序列
from windget import getFundManagerBestPerformanceSeries


# 获取现任基金最佳回报
from windget import getFundManagerBestPerformance


# 获取资本项目规模维持率时间序列
from windget import getMaintenanceSeries


# 获取资本项目规模维持率
from windget import getMaintenance


# 获取毛利(TTM)时间序列
from windget import getGrossMarginTtM2Series


# 获取毛利(TTM)
from windget import getGrossMarginTtM2


# 获取毛利时间序列
from windget import getGrossMarginSeries


# 获取毛利
from windget import getGrossMargin


# 获取毛利(TTM)_GSD时间序列
from windget import getGrossMarginTtM3Series


# 获取毛利(TTM)_GSD
from windget import getGrossMarginTtM3


# 获取毛利_GSD时间序列
from windget import getWgsDGrossMargin2Series


# 获取毛利_GSD
from windget import getWgsDGrossMargin2


# 获取毛利(TTM)_PIT时间序列
from windget import getFaGpTtMSeries


# 获取毛利(TTM)_PIT
from windget import getFaGpTtM


# 获取毛利(TTM,只有最新数据)时间序列
from windget import getGrossMarginTtMSeries


# 获取毛利(TTM,只有最新数据)
from windget import getGrossMarginTtM


# 获取经营活动净收益(TTM)时间序列
from windget import getOperateIncomeTtM2Series


# 获取经营活动净收益(TTM)
from windget import getOperateIncomeTtM2


# 获取经营活动净收益时间序列
from windget import getOperateIncomeSeries


# 获取经营活动净收益
from windget import getOperateIncome


# 获取经营活动净收益(TTM)_GSD时间序列
from windget import getOperateIncomeTtM3Series


# 获取经营活动净收益(TTM)_GSD
from windget import getOperateIncomeTtM3


# 获取经营活动净收益_PIT时间序列
from windget import getFaOAIncomeSeries


# 获取经营活动净收益_PIT
from windget import getFaOAIncome


# 获取经营活动净收益(TTM)_PIT时间序列
from windget import getFaOperaCtIncomeTtMSeries


# 获取经营活动净收益(TTM)_PIT
from windget import getFaOperaCtIncomeTtM


# 获取经营活动净收益(TTM,只有最新数据)时间序列
from windget import getOperateIncomeTtMSeries


# 获取经营活动净收益(TTM,只有最新数据)
from windget import getOperateIncomeTtM


# 获取价值变动净收益(TTM)时间序列
from windget import getInvestIncomeTtM2Series


# 获取价值变动净收益(TTM)
from windget import getInvestIncomeTtM2


# 获取价值变动净收益时间序列
from windget import getInvestIncomeSeries


# 获取价值变动净收益
from windget import getInvestIncome


# 获取价值变动净收益(TTM)_GSD时间序列
from windget import getInvestIncomeTtM3Series


# 获取价值变动净收益(TTM)_GSD
from windget import getInvestIncomeTtM3


# 获取价值变动净收益(TTM)_PIT时间序列
from windget import getFaChavAlIncomeTtMSeries


# 获取价值变动净收益(TTM)_PIT
from windget import getFaChavAlIncomeTtM


# 获取价值变动净收益(TTM,只有最新数据)时间序列
from windget import getInvestIncomeTtMSeries


# 获取价值变动净收益(TTM,只有最新数据)
from windget import getInvestIncomeTtM


# 获取研发支出前利润时间序列
from windget import getEBrSeries


# 获取研发支出前利润
from windget import getEBr


# 获取全部投入资本时间序列
from windget import getInvestCapitalSeries


# 获取全部投入资本
from windget import getInvestCapital


# 获取全部投入资本_GSD时间序列
from windget import getWgsDInvestCapital2Series


# 获取全部投入资本_GSD
from windget import getWgsDInvestCapital2


# 获取全部投入资本_PIT时间序列
from windget import getFaInvestCapitalSeries


# 获取全部投入资本_PIT
from windget import getFaInvestCapital


# 获取营运资本时间序列
from windget import getWorkingCapitalSeries


# 获取营运资本
from windget import getWorkingCapital


# 获取营运资本_GSD时间序列
from windget import getWgsDWorkingCapital2Series


# 获取营运资本_GSD
from windget import getWgsDWorkingCapital2


# 获取营运资本变动_GSD时间序列
from windget import getWgsDWKCapChgSeries


# 获取营运资本变动_GSD
from windget import getWgsDWKCapChg


# 获取净营运资本时间序列
from windget import getNetworkingCapitalSeries


# 获取净营运资本
from windget import getNetworkingCapital


# 获取净营运资本_GSD时间序列
from windget import getWgsDNetworkingCapital2Series


# 获取净营运资本_GSD
from windget import getWgsDNetworkingCapital2


# 获取单季度.营运资本变动_GSD时间序列
from windget import getWgsDQfaWKCapChgSeries


# 获取单季度.营运资本变动_GSD
from windget import getWgsDQfaWKCapChg


# 获取留存收益时间序列
from windget import getRetainedEarningsSeries


# 获取留存收益
from windget import getRetainedEarnings


# 获取留存收益_GSD时间序列
from windget import getWgsDComEqRetainEarnSeries


# 获取留存收益_GSD
from windget import getWgsDComEqRetainEarn


# 获取留存收益_PIT时间序列
from windget import getFaRetainEarnSeries


# 获取留存收益_PIT
from windget import getFaRetainEarn


# 获取带息债务时间序列
from windget import getInterestDebtSeries


# 获取带息债务
from windget import getInterestDebt


# 获取带息债务_GSD时间序列
from windget import getWgsDInterestDebt2Series


# 获取带息债务_GSD
from windget import getWgsDInterestDebt2


# 获取带息债务_PIT时间序列
from windget import getFaInterestDebtSeries


# 获取带息债务_PIT
from windget import getFaInterestDebt


# 获取有形净值/带息债务_PIT时间序列
from windget import getFaTangibleAToInterestDebtSeries


# 获取有形净值/带息债务_PIT
from windget import getFaTangibleAToInterestDebt


# 获取EBITDA/带息债务时间序列
from windget import getEbItDatoInterestDebtSeries


# 获取EBITDA/带息债务
from windget import getEbItDatoInterestDebt


# 获取净债务时间序列
from windget import getNetDebtSeries


# 获取净债务
from windget import getNetDebt


# 获取净债务_GSD时间序列
from windget import getWgsDNetDebt2Series


# 获取净债务_GSD
from windget import getWgsDNetDebt2


# 获取净债务_PIT时间序列
from windget import getFaNetDebtSeries


# 获取净债务_PIT
from windget import getFaNetDebt


# 获取有形净值/净债务_PIT时间序列
from windget import getFaTangibleAssetToNetDebtSeries


# 获取有形净值/净债务_PIT
from windget import getFaTangibleAssetToNetDebt


# 获取当期计提折旧与摊销时间序列
from windget import getDaPerIdSeries


# 获取当期计提折旧与摊销
from windget import getDaPerId


# 获取当期计提折旧与摊销_GSD时间序列
from windget import getWgsDDa2Series


# 获取当期计提折旧与摊销_GSD
from windget import getWgsDDa2


# 获取贷款总额时间序列
from windget import getTotalLoanNSeries


# 获取贷款总额
from windget import getTotalLoanN


# 获取贷款总额(旧)时间序列
from windget import getTotalLoanSeries


# 获取贷款总额(旧)
from windget import getTotalLoan


# 获取正常-占贷款总额比时间序列
from windget import getStmNoteBank9506Series


# 获取正常-占贷款总额比
from windget import getStmNoteBank9506


# 获取关注-占贷款总额比时间序列
from windget import getStmNoteBank9507Series


# 获取关注-占贷款总额比
from windget import getStmNoteBank9507


# 获取次级-占贷款总额比时间序列
from windget import getStmNoteBank9508Series


# 获取次级-占贷款总额比
from windget import getStmNoteBank9508


# 获取可疑-占贷款总额比时间序列
from windget import getStmNoteBank9509Series


# 获取可疑-占贷款总额比
from windget import getStmNoteBank9509


# 获取损失-占贷款总额比时间序列
from windget import getStmNoteBank9510Series


# 获取损失-占贷款总额比
from windget import getStmNoteBank9510


# 获取存款总额时间序列
from windget import getTotalDepositNSeries


# 获取存款总额
from windget import getTotalDepositN


# 获取存款总额(旧)时间序列
from windget import getTotalDepositSeries


# 获取存款总额(旧)
from windget import getTotalDeposit


# 获取存款余额_存款总额时间序列
from windget import getStmNoteBank647Series


# 获取存款余额_存款总额
from windget import getStmNoteBank647


# 获取存款平均余额_存款总额时间序列
from windget import getStmNoteBank648Series


# 获取存款平均余额_存款总额
from windget import getStmNoteBank648


# 获取存款平均成本率_存款总额时间序列
from windget import getStmNoteBank646Series


# 获取存款平均成本率_存款总额
from windget import getStmNoteBank646


# 获取贷款减值准备时间序列
from windget import getBadDebtProvNSeries


# 获取贷款减值准备
from windget import getBadDebtProvN


# 获取贷款减值准备(旧)时间序列
from windget import getBadDebtProvSeries


# 获取贷款减值准备(旧)
from windget import getBadDebtProv


# 获取贷款损失准备充足率时间序列
from windget import getStmNoteBankArSeries


# 获取贷款损失准备充足率
from windget import getStmNoteBankAr


# 获取成本收入比时间序列
from windget import getStmNoteBank129NSeries


# 获取成本收入比
from windget import getStmNoteBank129N


# 获取成本收入比(旧)时间序列
from windget import getStmNoteBank129Series


# 获取成本收入比(旧)
from windget import getStmNoteBank129


# 获取存贷款比率时间序列
from windget import getLoanDePoRatioNSeries


# 获取存贷款比率
from windget import getLoanDePoRatioN


# 获取存贷款比率(人民币)时间序列
from windget import getLoanDePoRatioRMbNSeries


# 获取存贷款比率(人民币)
from windget import getLoanDePoRatioRMbN


# 获取存贷款比率(外币)时间序列
from windget import getLoanDePoRatioNormBNSeries


# 获取存贷款比率(外币)
from windget import getLoanDePoRatioNormBN


# 获取存贷款比率(旧)时间序列
from windget import getLoanDePoRatioSeries


# 获取存贷款比率(旧)
from windget import getLoanDePoRatio


# 获取存贷款比率(人民币)(旧)时间序列
from windget import getLoanDePoRatioRMbSeries


# 获取存贷款比率(人民币)(旧)
from windget import getLoanDePoRatioRMb


# 获取存贷款比率(外币)(旧)时间序列
from windget import getLoanDePoRatioNormBSeries


# 获取存贷款比率(外币)(旧)
from windget import getLoanDePoRatioNormB


# 获取不良贷款比率时间序列
from windget import getNPlRatioNSeries


# 获取不良贷款比率
from windget import getNPlRatioN


# 获取不良贷款比率(旧)时间序列
from windget import getNPlRatioSeries


# 获取不良贷款比率(旧)
from windget import getNPlRatio


# 获取不良贷款拨备覆盖率时间序列
from windget import getBadDebtProvCoverageNSeries


# 获取不良贷款拨备覆盖率
from windget import getBadDebtProvCoverageN


# 获取不良贷款拨备覆盖率(旧)时间序列
from windget import getBadDebtProvCoverageSeries


# 获取不良贷款拨备覆盖率(旧)
from windget import getBadDebtProvCoverage


# 获取拆出资金比率时间序列
from windget import getLendToBanksRatioNSeries


# 获取拆出资金比率
from windget import getLendToBanksRatioN


# 获取拆出资金比率(旧)时间序列
from windget import getLendToBanksRatioSeries


# 获取拆出资金比率(旧)
from windget import getLendToBanksRatio


# 获取拆入资金比率时间序列
from windget import getLoanFromBanksRatioNSeries


# 获取拆入资金比率
from windget import getLoanFromBanksRatioN


# 获取拆入资金比率(旧)时间序列
from windget import getLoanFromBanksRatioSeries


# 获取拆入资金比率(旧)
from windget import getLoanFromBanksRatio


# 获取备付金比率(人民币)时间序列
from windget import getReserveRatioRMbNSeries


# 获取备付金比率(人民币)
from windget import getReserveRatioRMbN


# 获取备付金比率(人民币)(旧)时间序列
from windget import getReserveRatioRMbSeries


# 获取备付金比率(人民币)(旧)
from windget import getReserveRatioRMb


# 获取备付金比率(外币)时间序列
from windget import getReserveRatioFcNSeries


# 获取备付金比率(外币)
from windget import getReserveRatioFcN


# 获取备付金比率(外币)(旧)时间序列
from windget import getReserveRatioFcSeries


# 获取备付金比率(外币)(旧)
from windget import getReserveRatioFc


# 获取不良贷款余额时间序列
from windget import getStmNoteBank26Series


# 获取不良贷款余额
from windget import getStmNoteBank26


# 获取不良贷款余额_企业贷款及垫款时间序列
from windget import getStmNoteBank691Series


# 获取不良贷款余额_企业贷款及垫款
from windget import getStmNoteBank691


# 获取不良贷款余额_个人贷款及垫款时间序列
from windget import getStmNoteBank692Series


# 获取不良贷款余额_个人贷款及垫款
from windget import getStmNoteBank692


# 获取不良贷款余额_票据贴现时间序列
from windget import getStmNoteBank693Series


# 获取不良贷款余额_票据贴现
from windget import getStmNoteBank693


# 获取不良贷款余额_个人住房贷款时间序列
from windget import getStmNoteBank694Series


# 获取不良贷款余额_个人住房贷款
from windget import getStmNoteBank694


# 获取不良贷款余额_个人消费贷款时间序列
from windget import getStmNoteBank695Series


# 获取不良贷款余额_个人消费贷款
from windget import getStmNoteBank695


# 获取不良贷款余额_信用卡应收账款时间序列
from windget import getStmNoteBank696Series


# 获取不良贷款余额_信用卡应收账款
from windget import getStmNoteBank696


# 获取不良贷款余额_经营性贷款时间序列
from windget import getStmNoteBank697Series


# 获取不良贷款余额_经营性贷款
from windget import getStmNoteBank697


# 获取不良贷款余额_汽车贷款时间序列
from windget import getStmNoteBank698Series


# 获取不良贷款余额_汽车贷款
from windget import getStmNoteBank698


# 获取不良贷款余额_其他个人贷款时间序列
from windget import getStmNoteBank699Series


# 获取不良贷款余额_其他个人贷款
from windget import getStmNoteBank699


# 获取不良贷款余额_总计时间序列
from windget import getStmNoteBank690Series


# 获取不良贷款余额_总计
from windget import getStmNoteBank690


# 获取不良贷款余额_信用贷款时间序列
from windget import getStmNoteBank751Series


# 获取不良贷款余额_信用贷款
from windget import getStmNoteBank751


# 获取不良贷款余额_保证贷款时间序列
from windget import getStmNoteBank752Series


# 获取不良贷款余额_保证贷款
from windget import getStmNoteBank752


# 获取不良贷款余额_抵押贷款时间序列
from windget import getStmNoteBank753Series


# 获取不良贷款余额_抵押贷款
from windget import getStmNoteBank753


# 获取不良贷款余额_质押贷款时间序列
from windget import getStmNoteBank754Series


# 获取不良贷款余额_质押贷款
from windget import getStmNoteBank754


# 获取不良贷款余额_短期贷款时间序列
from windget import getStmNoteBank811Series


# 获取不良贷款余额_短期贷款
from windget import getStmNoteBank811


# 获取不良贷款余额_中长期贷款时间序列
from windget import getStmNoteBank812Series


# 获取不良贷款余额_中长期贷款
from windget import getStmNoteBank812


# 获取不良贷款余额(按行业)时间序列
from windget import getStmNoteBank66Series


# 获取不良贷款余额(按行业)
from windget import getStmNoteBank66


# 获取中长期贷款比率(人民币)时间序列
from windget import getMedLongLoanRatioRMbNSeries


# 获取中长期贷款比率(人民币)
from windget import getMedLongLoanRatioRMbN


# 获取中长期贷款比率(人民币)(旧)时间序列
from windget import getMedLongLoanRatioRMbSeries


# 获取中长期贷款比率(人民币)(旧)
from windget import getMedLongLoanRatioRMb


# 获取中长期贷款比率(外币)时间序列
from windget import getMedLongLoanRatioFcNSeries


# 获取中长期贷款比率(外币)
from windget import getMedLongLoanRatioFcN


# 获取中长期贷款比率(外币)(旧)时间序列
from windget import getMedLongLoanRatioFcSeries


# 获取中长期贷款比率(外币)(旧)
from windget import getMedLongLoanRatioFc


# 获取利息回收率时间序列
from windget import getIntColRatioNSeries


# 获取利息回收率
from windget import getIntColRatioN


# 获取利息回收率(旧)时间序列
from windget import getIntColRatioSeries


# 获取利息回收率(旧)
from windget import getIntColRatio


# 获取境外资金运用比率时间序列
from windget import getForCaputRatioNSeries


# 获取境外资金运用比率
from windget import getForCaputRatioN


# 获取境外资金运用比率(旧)时间序列
from windget import getForCaputRatioSeries


# 获取境外资金运用比率(旧)
from windget import getForCaputRatio


# 获取单一最大客户贷款比例时间序列
from windget import getLargestCustomerLoanNSeries


# 获取单一最大客户贷款比例
from windget import getLargestCustomerLoanN


# 获取单一最大客户贷款比例(旧)时间序列
from windget import getLargestCustomerLoanSeries


# 获取单一最大客户贷款比例(旧)
from windget import getLargestCustomerLoan


# 获取最大十家客户贷款占资本净额比例时间序列
from windget import getTopTenCustomerLoanNSeries


# 获取最大十家客户贷款占资本净额比例
from windget import getTopTenCustomerLoanN


# 获取净息差时间序列
from windget import getStmNoteBank144NSeries


# 获取净息差
from windget import getStmNoteBank144N


# 获取净息差(公布值)时间序列
from windget import getStmNoteBank5444Series


# 获取净息差(公布值)
from windget import getStmNoteBank5444


# 获取净息差(旧)时间序列
from windget import getStmNoteBank144Series


# 获取净息差(旧)
from windget import getStmNoteBank144


# 获取净利差时间序列
from windget import getStmNoteBank147NSeries


# 获取净利差
from windget import getStmNoteBank147N


# 获取净利差(旧)时间序列
from windget import getStmNoteBank147Series


# 获取净利差(旧)
from windget import getStmNoteBank147


# 获取市场风险资本时间序列
from windget import getStmNoteBank341Series


# 获取市场风险资本
from windget import getStmNoteBank341


# 获取银行理财产品余额时间序列
from windget import getStmNoteBank1778Series


# 获取银行理财产品余额
from windget import getStmNoteBank1778


# 获取拨贷比时间序列
from windget import getStmNoteBank55Series


# 获取拨贷比
from windget import getStmNoteBank55


# 获取库存现金时间序列
from windget import getStmNoteBank5453Series


# 获取库存现金
from windget import getStmNoteBank5453


# 获取可用的稳定资金时间序列
from windget import getStmNoteBankAsFSeries


# 获取可用的稳定资金
from windget import getStmNoteBankAsF


# 获取所需的稳定资金时间序列
from windget import getStmNoteBankRsfSeries


# 获取所需的稳定资金
from windget import getStmNoteBankRsf


# 获取绿色信贷余额时间序列
from windget import getEsGGcbWindSeries


# 获取绿色信贷余额
from windget import getEsGGcbWind


# 获取最大十家客户贷款比例(旧)时间序列
from windget import getTopTenCustomerLoanSeries


# 获取最大十家客户贷款比例(旧)
from windget import getTopTenCustomerLoan


# 获取核心资本净额时间序列
from windget import getStmNoteBank132NSeries


# 获取核心资本净额
from windget import getStmNoteBank132N


# 获取核心资本净额(旧)时间序列
from windget import getStmNoteBank132Series


# 获取核心资本净额(旧)
from windget import getStmNoteBank132


# 获取资本净额时间序列
from windget import getStmNoteBank131NSeries


# 获取资本净额
from windget import getStmNoteBank131N


# 获取资本净额(2013)时间序列
from windget import getStmNoteBankNetEquityCapSeries


# 获取资本净额(2013)
from windget import getStmNoteBankNetEquityCap


# 获取资本净额(旧)时间序列
from windget import getStmNoteBank131Series


# 获取资本净额(旧)
from windget import getStmNoteBank131


# 获取一级资本净额(2013)时间序列
from windget import getStmNoteBankTier1CapSeries


# 获取一级资本净额(2013)
from windget import getStmNoteBankTier1Cap


# 获取核心一级资本净额(2013)时间序列
from windget import getStmNoteBankCoreTier1CapSeries


# 获取核心一级资本净额(2013)
from windget import getStmNoteBankCoreTier1Cap


# 获取核心资本充足率时间序列
from windget import getCoreCapIADeRatioNSeries


# 获取核心资本充足率
from windget import getCoreCapIADeRatioN


# 获取核心资本充足率(旧)时间序列
from windget import getCoreCapIADeRatioSeries


# 获取核心资本充足率(旧)
from windget import getCoreCapIADeRatio


# 获取资本充足率时间序列
from windget import getCapIADeRatioNSeries


# 获取资本充足率
from windget import getCapIADeRatioN


# 获取资本充足率(2013)时间序列
from windget import getStmNoteBankCapAdequacyRatioSeries


# 获取资本充足率(2013)
from windget import getStmNoteBankCapAdequacyRatio


# 获取资本充足率(旧)时间序列
from windget import getCapIADeRatioSeries


# 获取资本充足率(旧)
from windget import getCapIADeRatio


# 获取一级资本充足率(2013)时间序列
from windget import getStmNoteBankCapAdequacyRatioT1Series


# 获取一级资本充足率(2013)
from windget import getStmNoteBankCapAdequacyRatioT1


# 获取核心一级资本充足率(2013)时间序列
from windget import getStmNoteBankCapAdequacyRatioCt1Series


# 获取核心一级资本充足率(2013)
from windget import getStmNoteBankCapAdequacyRatioCt1


# 获取杠杆率时间序列
from windget import getStmNoteBank171Series


# 获取杠杆率
from windget import getStmNoteBank171


# 获取资本杠杆率时间序列
from windget import getStmNoteSec34Series


# 获取资本杠杆率
from windget import getStmNoteSec34


# 获取流动性覆盖率时间序列
from windget import getStmNoteBank172Series


# 获取流动性覆盖率
from windget import getStmNoteBank172


# 获取流动性覆盖率(券商)时间序列
from windget import getStmNoteSec35Series


# 获取流动性覆盖率(券商)
from windget import getStmNoteSec35


# 获取流动性覆盖率:基本情景时间序列
from windget import getQStmNoteInSur212540Series


# 获取流动性覆盖率:基本情景
from windget import getQStmNoteInSur212540


# 获取流动性覆盖率:公司整体:压力情景1时间序列
from windget import getQStmNoteInSur212541Series


# 获取流动性覆盖率:公司整体:压力情景1
from windget import getQStmNoteInSur212541


# 获取流动性覆盖率:公司整体:压力情景2时间序列
from windget import getQStmNoteInSur212542Series


# 获取流动性覆盖率:公司整体:压力情景2
from windget import getQStmNoteInSur212542


# 获取流动性覆盖率:独立账户:压力情景1时间序列
from windget import getQStmNoteInSur212543Series


# 获取流动性覆盖率:独立账户:压力情景1
from windget import getQStmNoteInSur212543


# 获取流动性覆盖率:独立账户:压力情景2时间序列
from windget import getQStmNoteInSur212544Series


# 获取流动性覆盖率:独立账户:压力情景2
from windget import getQStmNoteInSur212544


# 获取正常-金额时间序列
from windget import getStmNoteBank31Series


# 获取正常-金额
from windget import getStmNoteBank31


# 获取正常-迁徙率时间序列
from windget import getStmNoteBank9501Series


# 获取正常-迁徙率
from windget import getStmNoteBank9501


# 获取关注-金额时间序列
from windget import getStmNoteBank340Series


# 获取关注-金额
from windget import getStmNoteBank340


# 获取关注-迁徙率时间序列
from windget import getStmNoteBank9502Series


# 获取关注-迁徙率
from windget import getStmNoteBank9502


# 获取次级-金额时间序列
from windget import getStmNoteBank37Series


# 获取次级-金额
from windget import getStmNoteBank37


# 获取次级-迁徙率时间序列
from windget import getStmNoteBank9503Series


# 获取次级-迁徙率
from windget import getStmNoteBank9503


# 获取可疑-金额时间序列
from windget import getStmNoteBank40Series


# 获取可疑-金额
from windget import getStmNoteBank40


# 获取可疑-迁徙率时间序列
from windget import getStmNoteBank9504Series


# 获取可疑-迁徙率
from windget import getStmNoteBank9504


# 获取损失-金额时间序列
from windget import getStmNoteBank430Series


# 获取损失-金额
from windget import getStmNoteBank430


# 获取存款余额_个人存款时间序列
from windget import getStmNoteBank616Series


# 获取存款余额_个人存款
from windget import getStmNoteBank616


# 获取存款余额_个人定期存款时间序列
from windget import getStmNoteBank611Series


# 获取存款余额_个人定期存款
from windget import getStmNoteBank611


# 获取存款余额_个人活期存款时间序列
from windget import getStmNoteBank612Series


# 获取存款余额_个人活期存款
from windget import getStmNoteBank612


# 获取存款余额_公司存款时间序列
from windget import getStmNoteBank617Series


# 获取存款余额_公司存款
from windget import getStmNoteBank617


# 获取存款余额_公司定期存款时间序列
from windget import getStmNoteBank613Series


# 获取存款余额_公司定期存款
from windget import getStmNoteBank613


# 获取存款余额_公司活期存款时间序列
from windget import getStmNoteBank614Series


# 获取存款余额_公司活期存款
from windget import getStmNoteBank614


# 获取存款余额_其它存款时间序列
from windget import getStmNoteBank615Series


# 获取存款余额_其它存款
from windget import getStmNoteBank615


# 获取存款平均余额_个人定期存款时间序列
from windget import getStmNoteBank621Series


# 获取存款平均余额_个人定期存款
from windget import getStmNoteBank621


# 获取存款平均余额_个人活期存款时间序列
from windget import getStmNoteBank622Series


# 获取存款平均余额_个人活期存款
from windget import getStmNoteBank622


# 获取存款平均余额_公司定期存款时间序列
from windget import getStmNoteBank623Series


# 获取存款平均余额_公司定期存款
from windget import getStmNoteBank623


# 获取存款平均余额_公司活期存款时间序列
from windget import getStmNoteBank624Series


# 获取存款平均余额_公司活期存款
from windget import getStmNoteBank624


# 获取存款平均余额_其它存款时间序列
from windget import getStmNoteBank625Series


# 获取存款平均余额_其它存款
from windget import getStmNoteBank625


# 获取存款平均余额_企业存款时间序列
from windget import getStmNoteBank50Series


# 获取存款平均余额_企业存款
from windget import getStmNoteBank50


# 获取存款平均余额_储蓄存款时间序列
from windget import getStmNoteBank52Series


# 获取存款平均余额_储蓄存款
from windget import getStmNoteBank52


# 获取存款平均成本率_个人定期存款时间序列
from windget import getStmNoteBank641Series


# 获取存款平均成本率_个人定期存款
from windget import getStmNoteBank641


# 获取存款平均成本率_个人活期存款时间序列
from windget import getStmNoteBank642Series


# 获取存款平均成本率_个人活期存款
from windget import getStmNoteBank642


# 获取存款平均成本率_公司定期存款时间序列
from windget import getStmNoteBank643Series


# 获取存款平均成本率_公司定期存款
from windget import getStmNoteBank643


# 获取存款平均成本率_公司活期存款时间序列
from windget import getStmNoteBank644Series


# 获取存款平均成本率_公司活期存款
from windget import getStmNoteBank644


# 获取存款平均成本率_其它存款时间序列
from windget import getStmNoteBank645Series


# 获取存款平均成本率_其它存款
from windget import getStmNoteBank645


# 获取存款平均成本率_企业存款时间序列
from windget import getStmNoteBank51Series


# 获取存款平均成本率_企业存款
from windget import getStmNoteBank51


# 获取存款平均成本率_储蓄存款时间序列
from windget import getStmNoteBank53Series


# 获取存款平均成本率_储蓄存款
from windget import getStmNoteBank53


# 获取贷款余额_总计时间序列
from windget import getStmNoteBank680Series


# 获取贷款余额_总计
from windget import getStmNoteBank680


# 获取贷款余额_企业贷款及垫款时间序列
from windget import getStmNoteBank681Series


# 获取贷款余额_企业贷款及垫款
from windget import getStmNoteBank681


# 获取贷款余额_个人贷款及垫款时间序列
from windget import getStmNoteBank682Series


# 获取贷款余额_个人贷款及垫款
from windget import getStmNoteBank682


# 获取贷款余额_票据贴现时间序列
from windget import getStmNoteBank683Series


# 获取贷款余额_票据贴现
from windget import getStmNoteBank683


# 获取贷款余额_个人住房贷款时间序列
from windget import getStmNoteBank684Series


# 获取贷款余额_个人住房贷款
from windget import getStmNoteBank684


# 获取贷款余额_个人消费贷款时间序列
from windget import getStmNoteBank685Series


# 获取贷款余额_个人消费贷款
from windget import getStmNoteBank685


# 获取贷款余额_信用卡应收账款时间序列
from windget import getStmNoteBank686Series


# 获取贷款余额_信用卡应收账款
from windget import getStmNoteBank686


# 获取贷款余额_经营性贷款时间序列
from windget import getStmNoteBank687Series


# 获取贷款余额_经营性贷款
from windget import getStmNoteBank687


# 获取贷款余额_汽车贷款时间序列
from windget import getStmNoteBank688Series


# 获取贷款余额_汽车贷款
from windget import getStmNoteBank688


# 获取贷款余额_其他个人贷款时间序列
from windget import getStmNoteBank689Series


# 获取贷款余额_其他个人贷款
from windget import getStmNoteBank689


# 获取不良贷款率_企业贷款及垫款时间序列
from windget import getStmNoteBank701Series


# 获取不良贷款率_企业贷款及垫款
from windget import getStmNoteBank701


# 获取不良贷款率_个人贷款及垫款时间序列
from windget import getStmNoteBank702Series


# 获取不良贷款率_个人贷款及垫款
from windget import getStmNoteBank702


# 获取不良贷款率_票据贴现时间序列
from windget import getStmNoteBank703Series


# 获取不良贷款率_票据贴现
from windget import getStmNoteBank703


# 获取不良贷款率_个人住房贷款时间序列
from windget import getStmNoteBank704Series


# 获取不良贷款率_个人住房贷款
from windget import getStmNoteBank704


# 获取不良贷款率_个人消费贷款时间序列
from windget import getStmNoteBank705Series


# 获取不良贷款率_个人消费贷款
from windget import getStmNoteBank705


# 获取不良贷款率_信用卡应收账款时间序列
from windget import getStmNoteBank706Series


# 获取不良贷款率_信用卡应收账款
from windget import getStmNoteBank706


# 获取不良贷款率_经营性贷款时间序列
from windget import getStmNoteBank707Series


# 获取不良贷款率_经营性贷款
from windget import getStmNoteBank707


# 获取不良贷款率_汽车贷款时间序列
from windget import getStmNoteBank708Series


# 获取不良贷款率_汽车贷款
from windget import getStmNoteBank708


# 获取不良贷款率_其他个人贷款时间序列
from windget import getStmNoteBank709Series


# 获取不良贷款率_其他个人贷款
from windget import getStmNoteBank709


# 获取贷款平均余额_总计时间序列
from windget import getStmNoteBank700Series


# 获取贷款平均余额_总计
from windget import getStmNoteBank700


# 获取贷款平均余额_企业贷款及垫款时间序列
from windget import getStmNoteBank711Series


# 获取贷款平均余额_企业贷款及垫款
from windget import getStmNoteBank711


# 获取贷款平均余额_个人贷款及垫款时间序列
from windget import getStmNoteBank712Series


# 获取贷款平均余额_个人贷款及垫款
from windget import getStmNoteBank712


# 获取贷款平均余额_票据贴现时间序列
from windget import getStmNoteBank713Series


# 获取贷款平均余额_票据贴现
from windget import getStmNoteBank713


# 获取贷款平均余额_个人住房贷款时间序列
from windget import getStmNoteBank714Series


# 获取贷款平均余额_个人住房贷款
from windget import getStmNoteBank714


# 获取贷款平均余额_个人消费贷款时间序列
from windget import getStmNoteBank715Series


# 获取贷款平均余额_个人消费贷款
from windget import getStmNoteBank715


# 获取贷款平均余额_信用卡应收账款时间序列
from windget import getStmNoteBank716Series


# 获取贷款平均余额_信用卡应收账款
from windget import getStmNoteBank716


# 获取贷款平均余额_经营性贷款时间序列
from windget import getStmNoteBank717Series


# 获取贷款平均余额_经营性贷款
from windget import getStmNoteBank717


# 获取贷款平均余额_汽车贷款时间序列
from windget import getStmNoteBank718Series


# 获取贷款平均余额_汽车贷款
from windget import getStmNoteBank718


# 获取贷款平均余额_其他个人贷款时间序列
from windget import getStmNoteBank719Series


# 获取贷款平均余额_其他个人贷款
from windget import getStmNoteBank719


# 获取贷款余额_信用贷款时间序列
from windget import getStmNoteBank741Series


# 获取贷款余额_信用贷款
from windget import getStmNoteBank741


# 获取贷款余额_保证贷款时间序列
from windget import getStmNoteBank742Series


# 获取贷款余额_保证贷款
from windget import getStmNoteBank742


# 获取贷款余额_抵押贷款时间序列
from windget import getStmNoteBank743Series


# 获取贷款余额_抵押贷款
from windget import getStmNoteBank743


# 获取贷款余额_质押贷款时间序列
from windget import getStmNoteBank744Series


# 获取贷款余额_质押贷款
from windget import getStmNoteBank744


# 获取不良贷款率_总计时间序列
from windget import getStmNoteBank730Series


# 获取不良贷款率_总计
from windget import getStmNoteBank730


# 获取不良贷款率_信用贷款时间序列
from windget import getStmNoteBank761Series


# 获取不良贷款率_信用贷款
from windget import getStmNoteBank761


# 获取不良贷款率_保证贷款时间序列
from windget import getStmNoteBank762Series


# 获取不良贷款率_保证贷款
from windget import getStmNoteBank762


# 获取不良贷款率_抵押贷款时间序列
from windget import getStmNoteBank763Series


# 获取不良贷款率_抵押贷款
from windget import getStmNoteBank763


# 获取不良贷款率_质押贷款时间序列
from windget import getStmNoteBank764Series


# 获取不良贷款率_质押贷款
from windget import getStmNoteBank764


# 获取贷款平均余额_信用贷款时间序列
from windget import getStmNoteBank771Series


# 获取贷款平均余额_信用贷款
from windget import getStmNoteBank771


# 获取贷款平均余额_保证贷款时间序列
from windget import getStmNoteBank772Series


# 获取贷款平均余额_保证贷款
from windget import getStmNoteBank772


# 获取贷款平均余额_抵押贷款时间序列
from windget import getStmNoteBank773Series


# 获取贷款平均余额_抵押贷款
from windget import getStmNoteBank773


# 获取贷款平均余额_质押贷款时间序列
from windget import getStmNoteBank774Series


# 获取贷款平均余额_质押贷款
from windget import getStmNoteBank774


# 获取贷款余额_短期贷款时间序列
from windget import getStmNoteBank801Series


# 获取贷款余额_短期贷款
from windget import getStmNoteBank801


# 获取贷款余额_中长期贷款时间序列
from windget import getStmNoteBank802Series


# 获取贷款余额_中长期贷款
from windget import getStmNoteBank802


# 获取不良贷款率_短期贷款时间序列
from windget import getStmNoteBank821Series


# 获取不良贷款率_短期贷款
from windget import getStmNoteBank821


# 获取不良贷款率_中长期贷款时间序列
from windget import getStmNoteBank822Series


# 获取不良贷款率_中长期贷款
from windget import getStmNoteBank822


# 获取贷款平均余额_短期贷款时间序列
from windget import getStmNoteBank46Series


# 获取贷款平均余额_短期贷款
from windget import getStmNoteBank46


# 获取贷款平均余额_中长期贷款时间序列
from windget import getStmNoteBank48Series


# 获取贷款平均余额_中长期贷款
from windget import getStmNoteBank48


# 获取贷款余额(按行业)时间序列
from windget import getStmNoteBank65Series


# 获取贷款余额(按行业)
from windget import getStmNoteBank65


# 获取不良贷款率(按行业)时间序列
from windget import getStmNoteBank67Series


# 获取不良贷款率(按行业)
from windget import getStmNoteBank67


# 获取逾期保证贷款_3个月以内时间序列
from windget import getStmNoteBank0021Series


# 获取逾期保证贷款_3个月以内
from windget import getStmNoteBank0021


# 获取逾期保证贷款_3个月至1年时间序列
from windget import getStmNoteBank0022Series


# 获取逾期保证贷款_3个月至1年
from windget import getStmNoteBank0022


# 获取逾期保证贷款_1年以上3年以内时间序列
from windget import getStmNoteBank0023Series


# 获取逾期保证贷款_1年以上3年以内
from windget import getStmNoteBank0023


# 获取逾期保证贷款_3年以上时间序列
from windget import getStmNoteBank0024Series


# 获取逾期保证贷款_3年以上
from windget import getStmNoteBank0024


# 获取逾期保证贷款合计时间序列
from windget import getStmNoteBank0025Series


# 获取逾期保证贷款合计
from windget import getStmNoteBank0025


# 获取逾期信用贷款_3个月以内时间序列
from windget import getStmNoteBank0011Series


# 获取逾期信用贷款_3个月以内
from windget import getStmNoteBank0011


# 获取逾期信用贷款_3个月至1年时间序列
from windget import getStmNoteBank0012Series


# 获取逾期信用贷款_3个月至1年
from windget import getStmNoteBank0012


# 获取逾期信用贷款_1年以上3年以内时间序列
from windget import getStmNoteBank0013Series


# 获取逾期信用贷款_1年以上3年以内
from windget import getStmNoteBank0013


# 获取逾期信用贷款_3年以上时间序列
from windget import getStmNoteBank0014Series


# 获取逾期信用贷款_3年以上
from windget import getStmNoteBank0014


# 获取逾期信用贷款合计时间序列
from windget import getStmNoteBank0015Series


# 获取逾期信用贷款合计
from windget import getStmNoteBank0015


# 获取逾期抵押贷款_3个月以内时间序列
from windget import getStmNoteBank0031Series


# 获取逾期抵押贷款_3个月以内
from windget import getStmNoteBank0031


# 获取逾期抵押贷款_3个月至1年时间序列
from windget import getStmNoteBank0032Series


# 获取逾期抵押贷款_3个月至1年
from windget import getStmNoteBank0032


# 获取逾期抵押贷款_1年以上3年以内时间序列
from windget import getStmNoteBank0033Series


# 获取逾期抵押贷款_1年以上3年以内
from windget import getStmNoteBank0033


# 获取逾期抵押贷款_3年以上时间序列
from windget import getStmNoteBank0034Series


# 获取逾期抵押贷款_3年以上
from windget import getStmNoteBank0034


# 获取逾期抵押贷款合计时间序列
from windget import getStmNoteBank0035Series


# 获取逾期抵押贷款合计
from windget import getStmNoteBank0035


# 获取逾期票据贴现_3个月以内时间序列
from windget import getStmNoteBank0041Series


# 获取逾期票据贴现_3个月以内
from windget import getStmNoteBank0041


# 获取逾期票据贴现_3个月至1年时间序列
from windget import getStmNoteBank0042Series


# 获取逾期票据贴现_3个月至1年
from windget import getStmNoteBank0042


# 获取逾期票据贴现_1年以上3年以内时间序列
from windget import getStmNoteBank0043Series


# 获取逾期票据贴现_1年以上3年以内
from windget import getStmNoteBank0043


# 获取逾期票据贴现_3年以上时间序列
from windget import getStmNoteBank0044Series


# 获取逾期票据贴现_3年以上
from windget import getStmNoteBank0044


# 获取逾期票据贴现合计时间序列
from windget import getStmNoteBank0045Series


# 获取逾期票据贴现合计
from windget import getStmNoteBank0045


# 获取逾期质押贷款_3个月以内时间序列
from windget import getStmNoteBank0051Series


# 获取逾期质押贷款_3个月以内
from windget import getStmNoteBank0051


# 获取逾期质押贷款_3个月至1年时间序列
from windget import getStmNoteBank0052Series


# 获取逾期质押贷款_3个月至1年
from windget import getStmNoteBank0052


# 获取逾期质押贷款_1年以上3年以内时间序列
from windget import getStmNoteBank0053Series


# 获取逾期质押贷款_1年以上3年以内
from windget import getStmNoteBank0053


# 获取逾期质押贷款_3年以上时间序列
from windget import getStmNoteBank0054Series


# 获取逾期质押贷款_3年以上
from windget import getStmNoteBank0054


# 获取逾期质押贷款合计时间序列
from windget import getStmNoteBank0055Series


# 获取逾期质押贷款合计
from windget import getStmNoteBank0055


# 获取净资本时间序列
from windget import getStmNoteSec1Series


# 获取净资本
from windget import getStmNoteSec1


# 获取净资本比率时间序列
from windget import getStmNoteSec4Series


# 获取净资本比率
from windget import getStmNoteSec4


# 获取核心净资本时间序列
from windget import getStmNoteSec30Series


# 获取核心净资本
from windget import getStmNoteSec30


# 获取附属净资本时间序列
from windget import getStmNoteSec31Series


# 获取附属净资本
from windget import getStmNoteSec31


# 获取自营固定收益类证券/净资本时间序列
from windget import getStmNoteSec8Series


# 获取自营固定收益类证券/净资本
from windget import getStmNoteSec8


# 获取自营权益类证券及证券衍生品/净资本时间序列
from windget import getStmNoteSec7Series


# 获取自营权益类证券及证券衍生品/净资本
from windget import getStmNoteSec7


# 获取各项风险资本准备之和时间序列
from windget import getStmNoteSec32Series


# 获取各项风险资本准备之和
from windget import getStmNoteSec32


# 获取净稳定资金率时间序列
from windget import getStmNoteSec36Series


# 获取净稳定资金率
from windget import getStmNoteSec36


# 获取受托资金时间序列
from windget import getStmNoteSec2Series


# 获取受托资金
from windget import getStmNoteSec2


# 获取自营股票时间序列
from windget import getStmNoteSecOp2Series


# 获取自营股票
from windget import getStmNoteSecOp2


# 获取自营国债时间序列
from windget import getStmNoteSecOp3Series


# 获取自营国债
from windget import getStmNoteSecOp3


# 获取自营基金时间序列
from windget import getStmNoteSecOp4Series


# 获取自营基金
from windget import getStmNoteSecOp4


# 获取自营证可转债时间序列
from windget import getStmNoteSecOp5Series


# 获取自营证可转债
from windget import getStmNoteSecOp5


# 获取自营证券合计时间序列
from windget import getStmNoteSecOp1Series


# 获取自营证券合计
from windget import getStmNoteSecOp1


# 获取风险覆盖率时间序列
from windget import getStmNoteSec5Series


# 获取风险覆盖率
from windget import getStmNoteSec5


# 获取证券投资业务收入时间序列
from windget import getStmNoteSec1540Series


# 获取证券投资业务收入
from windget import getStmNoteSec1540


# 获取证券经纪业务收入时间序列
from windget import getStmNoteSec1541Series


# 获取证券经纪业务收入
from windget import getStmNoteSec1541


# 获取投资银行业务收入时间序列
from windget import getStmNoteSec1542Series


# 获取投资银行业务收入
from windget import getStmNoteSec1542


# 获取证券投资业务净收入时间序列
from windget import getStmNoteSec1550Series


# 获取证券投资业务净收入
from windget import getStmNoteSec1550


# 获取证券经纪业务净收入时间序列
from windget import getStmNoteSec1551Series


# 获取证券经纪业务净收入
from windget import getStmNoteSec1551


# 获取投资银行业务净收入时间序列
from windget import getStmNoteSec1552Series


# 获取投资银行业务净收入
from windget import getStmNoteSec1552


# 获取评估利率假设:风险贴现率时间序列
from windget import getStmNoteInSur7Series


# 获取评估利率假设:风险贴现率
from windget import getStmNoteInSur7


# 获取退保率时间序列
from windget import getStmNoteInSur8Series


# 获取退保率
from windget import getStmNoteInSur8


# 获取保单继续率(13个月)时间序列
from windget import getStmNoteInSur1Series


# 获取保单继续率(13个月)
from windget import getStmNoteInSur1


# 获取保单继续率(14个月)时间序列
from windget import getStmNoteInSur2Series


# 获取保单继续率(14个月)
from windget import getStmNoteInSur2


# 获取保单继续率(25个月)时间序列
from windget import getStmNoteInSur3Series


# 获取保单继续率(25个月)
from windget import getStmNoteInSur3


# 获取保单继续率(26个月)时间序列
from windget import getStmNoteInSur4Series


# 获取保单继续率(26个月)
from windget import getStmNoteInSur4


# 获取偿付能力充足率(产险)时间序列
from windget import getStmNoteInSur12Series


# 获取偿付能力充足率(产险)
from windget import getStmNoteInSur12


# 获取赔付率(产险)时间序列
from windget import getStmNoteInSur10Series


# 获取赔付率(产险)
from windget import getStmNoteInSur10


# 获取费用率(产险)时间序列
from windget import getStmNoteInSur11Series


# 获取费用率(产险)
from windget import getStmNoteInSur11


# 获取实际资本(产险)时间序列
from windget import getStmNoteInSur13NSeries


# 获取实际资本(产险)
from windget import getStmNoteInSur13N


# 获取实际资本(产险)(旧)时间序列
from windget import getStmNoteInSur13Series


# 获取实际资本(产险)(旧)
from windget import getStmNoteInSur13


# 获取最低资本(产险)时间序列
from windget import getStmNoteInSur14NSeries


# 获取最低资本(产险)
from windget import getStmNoteInSur14N


# 获取最低资本(产险)(旧)时间序列
from windget import getStmNoteInSur14Series


# 获取最低资本(产险)(旧)
from windget import getStmNoteInSur14


# 获取偿付能力充足率(寿险)时间序列
from windget import getStmNoteInSur15Series


# 获取偿付能力充足率(寿险)
from windget import getStmNoteInSur15


# 获取内含价值(寿险)时间序列
from windget import getStmNoteInSur16NSeries


# 获取内含价值(寿险)
from windget import getStmNoteInSur16N


# 获取内含价值(寿险)(旧)时间序列
from windget import getStmNoteInSur16Series


# 获取内含价值(寿险)(旧)
from windget import getStmNoteInSur16


# 获取新业务价值(寿险)时间序列
from windget import getStmNoteInSur17NSeries


# 获取新业务价值(寿险)
from windget import getStmNoteInSur17N


# 获取新业务价值(寿险)(旧)时间序列
from windget import getStmNoteInSur17Series


# 获取新业务价值(寿险)(旧)
from windget import getStmNoteInSur17


# 获取有效业务价值(寿险)时间序列
from windget import getStmNoteInSur18NSeries


# 获取有效业务价值(寿险)
from windget import getStmNoteInSur18N


# 获取有效业务价值(寿险)(旧)时间序列
from windget import getStmNoteInSur18Series


# 获取有效业务价值(寿险)(旧)
from windget import getStmNoteInSur18


# 获取实际资本(寿险)时间序列
from windget import getStmNoteInSur19NSeries


# 获取实际资本(寿险)
from windget import getStmNoteInSur19N


# 获取实际资本(寿险)(旧)时间序列
from windget import getStmNoteInSur19Series


# 获取实际资本(寿险)(旧)
from windget import getStmNoteInSur19


# 获取最低资本(寿险)时间序列
from windget import getStmNoteInSur20NSeries


# 获取最低资本(寿险)
from windget import getStmNoteInSur20N


# 获取最低资本(寿险)(旧)时间序列
from windget import getStmNoteInSur20Series


# 获取最低资本(寿险)(旧)
from windget import getStmNoteInSur20


# 获取定期存款(投资)时间序列
from windget import getStmNoteInSur7801Series


# 获取定期存款(投资)
from windget import getStmNoteInSur7801


# 获取债券投资时间序列
from windget import getStmNoteInSur7802Series


# 获取债券投资
from windget import getStmNoteInSur7802


# 获取债券投资成本_FUND时间序列
from windget import getStmBs8Series


# 获取债券投资成本_FUND
from windget import getStmBs8


# 获取债券投资_FUND时间序列
from windget import getStmBs7Series


# 获取债券投资_FUND
from windget import getStmBs7


# 获取债券投资公允价值变动收益_FUND时间序列
from windget import getStmIs102Series


# 获取债券投资公允价值变动收益_FUND
from windget import getStmIs102


# 获取基金投资时间序列
from windget import getStmNoteInSur7803Series


# 获取基金投资
from windget import getStmNoteInSur7803


# 获取基金投资_FUND时间序列
from windget import getStmBs201Series


# 获取基金投资_FUND
from windget import getStmBs201


# 获取基金投资成本_FUND时间序列
from windget import getStmBs202Series


# 获取基金投资成本_FUND
from windget import getStmBs202


# 获取基金投资公允价值变动收益_FUND时间序列
from windget import getStmIs104Series


# 获取基金投资公允价值变动收益_FUND
from windget import getStmIs104


# 获取股票投资时间序列
from windget import getStmNoteInSur7804Series


# 获取股票投资
from windget import getStmNoteInSur7804


# 获取股票投资成本_FUND时间序列
from windget import getStmBs5Series


# 获取股票投资成本_FUND
from windget import getStmBs5


# 获取股票投资_FUND时间序列
from windget import getStmBs4Series


# 获取股票投资_FUND
from windget import getStmBs4


# 获取股票投资公允价值变动收益_FUND时间序列
from windget import getStmIs101Series


# 获取股票投资公允价值变动收益_FUND
from windget import getStmIs101


# 获取前N大股票占全部股票投资比时间序列
from windget import getStyleTopNProportionToAllSharesSeries


# 获取前N大股票占全部股票投资比
from windget import getStyleTopNProportionToAllShares


# 获取股权投资时间序列
from windget import getStmNoteInSur7805Series


# 获取股权投资
from windget import getStmNoteInSur7805


# 获取长期股权投资时间序列
from windget import getLongTermEqYInvestSeries


# 获取长期股权投资
from windget import getLongTermEqYInvest


# 获取基建投资时间序列
from windget import getStmNoteInSur7806Series


# 获取基建投资
from windget import getStmNoteInSur7806


# 获取现金及现金等价物时间序列
from windget import getStmNoteInSur7807Series


# 获取现金及现金等价物
from windget import getStmNoteInSur7807


# 获取现金及现金等价物_GSD时间序列
from windget import getWgsDCCeSeries


# 获取现金及现金等价物_GSD
from windget import getWgsDCCe


# 获取现金及现金等价物期初余额_GSD时间序列
from windget import getWgsDCashBegBalCfSeries


# 获取现金及现金等价物期初余额_GSD
from windget import getWgsDCashBegBalCf


# 获取现金及现金等价物期末余额_GSD时间序列
from windget import getWgsDCashEndBalCfSeries


# 获取现金及现金等价物期末余额_GSD
from windget import getWgsDCashEndBalCf


# 获取期初现金及现金等价物余额时间序列
from windget import getCashCashEquBegPeriodSeries


# 获取期初现金及现金等价物余额
from windget import getCashCashEquBegPeriod


# 获取期末现金及现金等价物余额时间序列
from windget import getCashCashEquEndPeriodSeries


# 获取期末现金及现金等价物余额
from windget import getCashCashEquEndPeriod


# 获取每股现金及现金等价物余额_PIT时间序列
from windget import getFaCcEpsSeries


# 获取每股现金及现金等价物余额_PIT
from windget import getFaCcEps


# 获取期末现金及现金等价物_PIT时间序列
from windget import getFaCCeSeries


# 获取期末现金及现金等价物_PIT
from windget import getFaCCe


# 获取单季度.现金及现金等价物期初余额_GSD时间序列
from windget import getWgsDQfaCashBegBalCfSeries


# 获取单季度.现金及现金等价物期初余额_GSD
from windget import getWgsDQfaCashBegBalCf


# 获取单季度.现金及现金等价物期末余额_GSD时间序列
from windget import getWgsDQfaCashEndBalCfSeries


# 获取单季度.现金及现金等价物期末余额_GSD
from windget import getWgsDQfaCashEndBalCf


# 获取单季度.期末现金及现金等价物余额时间序列
from windget import getQfaCashCashEquEndPeriodSeries


# 获取单季度.期末现金及现金等价物余额
from windget import getQfaCashCashEquEndPeriod


# 获取集团内含价值时间序列
from windget import getStmNoteInSur30NSeries


# 获取集团内含价值
from windget import getStmNoteInSur30N


# 获取集团客户数时间序列
from windget import getStmNoteInSur7810Series


# 获取集团客户数
from windget import getStmNoteInSur7810


# 获取保险营销员人数时间序列
from windget import getStmNoteInSur7811Series


# 获取保险营销员人数
from windget import getStmNoteInSur7811


# 获取保险营销员每月人均首年保险业务收入时间序列
from windget import getStmNoteInSur7812Series


# 获取保险营销员每月人均首年保险业务收入
from windget import getStmNoteInSur7812


# 获取保险营销员每月人均寿险新保单件数时间序列
from windget import getStmNoteInSur7813Series


# 获取保险营销员每月人均寿险新保单件数
from windget import getStmNoteInSur7813


# 获取证券买卖收益时间序列
from windget import getStmNoteInvestmentIncome0005Series


# 获取证券买卖收益
from windget import getStmNoteInvestmentIncome0005


# 获取公允价值变动收益时间序列
from windget import getStmNoteInvestmentIncome0006Series


# 获取公允价值变动收益
from windget import getStmNoteInvestmentIncome0006


# 获取公允价值变动收益_FUND时间序列
from windget import getStmIs24Series


# 获取公允价值变动收益_FUND
from windget import getStmIs24


# 获取权证投资公允价值变动收益_FUND时间序列
from windget import getStmIs103Series


# 获取权证投资公允价值变动收益_FUND
from windget import getStmIs103


# 获取处置合营企业净收益时间序列
from windget import getStmNoteInvestmentIncome0008Series


# 获取处置合营企业净收益
from windget import getStmNoteInvestmentIncome0008


# 获取核心偿付能力溢额时间序列
from windget import getQStmNoteInSur212505Series


# 获取核心偿付能力溢额
from windget import getQStmNoteInSur212505


# 获取核心偿付能力充足率时间序列
from windget import getQStmNoteInSur212506Series


# 获取核心偿付能力充足率
from windget import getQStmNoteInSur212506


# 获取保险业务收入时间序列
from windget import getQStmNoteInSur212509Series


# 获取保险业务收入
from windget import getQStmNoteInSur212509


# 获取实际资本时间序列
from windget import getQStmNoteInSur212514Series


# 获取实际资本
from windget import getQStmNoteInSur212514


# 获取核心一级资本时间序列
from windget import getQStmNoteInSur212515Series


# 获取核心一级资本
from windget import getQStmNoteInSur212515


# 获取核心二级资本时间序列
from windget import getQStmNoteInSur212516Series


# 获取核心二级资本
from windget import getQStmNoteInSur212516


# 获取附属一级资本时间序列
from windget import getQStmNoteInSur212517Series


# 获取附属一级资本
from windget import getQStmNoteInSur212517


# 获取附属二级资本时间序列
from windget import getQStmNoteInSur212518Series


# 获取附属二级资本
from windget import getQStmNoteInSur212518


# 获取最低资本时间序列
from windget import getQStmNoteInSur212519Series


# 获取最低资本
from windget import getQStmNoteInSur212519


# 获取量化风险最低资本时间序列
from windget import getQStmNoteInSur212520Series


# 获取量化风险最低资本
from windget import getQStmNoteInSur212520


# 获取控制风险最低资本时间序列
from windget import getQStmNoteInSur212527Series


# 获取控制风险最低资本
from windget import getQStmNoteInSur212527


# 获取市场风险最低资本合计时间序列
from windget import getQStmNoteInSur212523Series


# 获取市场风险最低资本合计
from windget import getQStmNoteInSur212523


# 获取信用风险最低资本合计时间序列
from windget import getQStmNoteInSur212524Series


# 获取信用风险最低资本合计
from windget import getQStmNoteInSur212524


# 获取保险风险最低资本合计时间序列
from windget import getQStmNoteInSur212546Series


# 获取保险风险最低资本合计
from windget import getQStmNoteInSur212546


# 获取寿险业务保险风险最低资本合计时间序列
from windget import getQStmNoteInSur212521Series


# 获取寿险业务保险风险最低资本合计
from windget import getQStmNoteInSur212521


# 获取非寿险业务保险风险最低资本合计时间序列
from windget import getQStmNoteInSur212522Series


# 获取非寿险业务保险风险最低资本合计
from windget import getQStmNoteInSur212522


# 获取附加资本时间序列
from windget import getQStmNoteInSur212528Series


# 获取附加资本
from windget import getQStmNoteInSur212528


# 获取风险分散效应的资本要求增加时间序列
from windget import getQStmNoteInSur212525Series


# 获取风险分散效应的资本要求增加
from windget import getQStmNoteInSur212525


# 获取风险聚合效应的资本要求减少时间序列
from windget import getQStmNoteInSur212526Series


# 获取风险聚合效应的资本要求减少
from windget import getQStmNoteInSur212526


# 获取净现金流时间序列
from windget import getQStmNoteInSur212530Series


# 获取净现金流
from windget import getQStmNoteInSur212530


# 获取净现金流:报告日后第1年时间序列
from windget import getQStmNoteInSur212531Series


# 获取净现金流:报告日后第1年
from windget import getQStmNoteInSur212531


# 获取净现金流:报告日后第2年时间序列
from windget import getQStmNoteInSur212532Series


# 获取净现金流:报告日后第2年
from windget import getQStmNoteInSur212532


# 获取净现金流:报告日后第3年时间序列
from windget import getQStmNoteInSur212533Series


# 获取净现金流:报告日后第3年
from windget import getQStmNoteInSur212533


# 获取净现金流:报告日后第1年:未来1季度时间序列
from windget import getQStmNoteInSur212547Series


# 获取净现金流:报告日后第1年:未来1季度
from windget import getQStmNoteInSur212547


# 获取净现金流:报告日后第1年:未来2季度时间序列
from windget import getQStmNoteInSur212548Series


# 获取净现金流:报告日后第1年:未来2季度
from windget import getQStmNoteInSur212548


# 获取净现金流:报告日后第1年:未来3季度时间序列
from windget import getQStmNoteInSur212549Series


# 获取净现金流:报告日后第1年:未来3季度
from windget import getQStmNoteInSur212549


# 获取净现金流:报告日后第1年:未来4季度时间序列
from windget import getQStmNoteInSur212550Series


# 获取净现金流:报告日后第1年:未来4季度
from windget import getQStmNoteInSur212550


# 获取市现率PCF(经营性净现金流LYR)时间序列
from windget import getPcfOcFlyRSeries


# 获取市现率PCF(经营性净现金流LYR)
from windget import getPcfOcFlyR


# 获取受限资金_GSD时间序列
from windget import getWgsDFundRestrictedSeries


# 获取受限资金_GSD
from windget import getWgsDFundRestricted


# 获取受限资金时间序列
from windget import getFundRestrictedSeries


# 获取受限资金
from windget import getFundRestricted


# 获取应收票据时间序列
from windget import getNotesRcVSeries


# 获取应收票据
from windget import getNotesRcV


# 获取应收账款及票据_GSD时间序列
from windget import getWgsDRecEivNetSeries


# 获取应收账款及票据_GSD
from windget import getWgsDRecEivNet


# 获取应收账款时间序列
from windget import getAccTRcVSeries


# 获取应收账款
from windget import getAccTRcV


# 获取应收款项融资时间序列
from windget import getFinancingARSeries


# 获取应收款项融资
from windget import getFinancingAR


# 获取预付款项时间序列
from windget import getPrepaySeries


# 获取预付款项
from windget import getPrepay


# 获取应收股利时间序列
from windget import getDvdRcVSeries


# 获取应收股利
from windget import getDvdRcV


# 获取应收股利_FUND时间序列
from windget import getStmBs11Series


# 获取应收股利_FUND
from windget import getStmBs11


# 获取应收利息时间序列
from windget import getIntRcVSeries


# 获取应收利息
from windget import getIntRcV


# 获取应收利息_FUND时间序列
from windget import getStmBs12Series


# 获取应收利息_FUND
from windget import getStmBs12


# 获取其他应收款时间序列
from windget import getOThRcVSeries


# 获取其他应收款
from windget import getOThRcV


# 获取存货_GSD时间序列
from windget import getWgsDInventoriesSeries


# 获取存货_GSD
from windget import getWgsDInventories


# 获取存货时间序列
from windget import getInventoriesSeries


# 获取存货
from windget import getInventories


# 获取存货的减少时间序列
from windget import getDecrInventoriesSeries


# 获取存货的减少
from windget import getDecrInventories


# 获取单季度.存货的减少时间序列
from windget import getQfaDecrInventoriesSeries


# 获取单季度.存货的减少
from windget import getQfaDecrInventories


# 获取待摊费用时间序列
from windget import getDeferredExpSeries


# 获取待摊费用
from windget import getDeferredExp


# 获取待摊费用减少时间序列
from windget import getDecrDeferredExpSeries


# 获取待摊费用减少
from windget import getDecrDeferredExp


# 获取长期待摊费用时间序列
from windget import getLongTermDeferredExpSeries


# 获取长期待摊费用
from windget import getLongTermDeferredExp


# 获取长期待摊费用摊销时间序列
from windget import getAMortLtDeferredExpSeries


# 获取长期待摊费用摊销
from windget import getAMortLtDeferredExp


# 获取单季度.待摊费用减少时间序列
from windget import getQfaDecrDeferredExpSeries


# 获取单季度.待摊费用减少
from windget import getQfaDecrDeferredExp


# 获取单季度.长期待摊费用摊销时间序列
from windget import getQfaAMortLtDeferredExpSeries


# 获取单季度.长期待摊费用摊销
from windget import getQfaAMortLtDeferredExp


# 获取结算备付金时间序列
from windget import getSettleRsRvSeries


# 获取结算备付金
from windget import getSettleRsRv


# 获取结算备付金_FUND时间序列
from windget import getStmBs2Series


# 获取结算备付金_FUND
from windget import getStmBs2


# 获取拆出资金_GSD时间序列
from windget import getWgsDLendIbSeries


# 获取拆出资金_GSD
from windget import getWgsDLendIb


# 获取拆出资金时间序列
from windget import getLoansToOThBanksSeries


# 获取拆出资金
from windget import getLoansToOThBanks


# 获取融出资金时间序列
from windget import getMarginAccTSeries


# 获取融出资金
from windget import getMarginAccT


# 获取融出资金净增加额时间序列
from windget import getNetInCrLendingFundSeries


# 获取融出资金净增加额
from windget import getNetInCrLendingFund


# 获取应收保费_GSD时间序列
from windget import getWgsDRecEivInSurSeries


# 获取应收保费_GSD
from windget import getWgsDRecEivInSur


# 获取应收保费时间序列
from windget import getPremRcVSeries


# 获取应收保费
from windget import getPremRcV


# 获取应收分保账款时间序列
from windget import getRcVFromReInsurerSeries


# 获取应收分保账款
from windget import getRcVFromReInsurer


# 获取应收分保合同准备金时间序列
from windget import getRcVFromCededInSurContRsRvSeries


# 获取应收分保合同准备金
from windget import getRcVFromCededInSurContRsRv


# 获取应收款项合计_GSD时间序列
from windget import getWgsDRecEivToTSeries


# 获取应收款项合计_GSD
from windget import getWgsDRecEivToT


# 获取应收款项时间序列
from windget import getToTAccTRcVSeries


# 获取应收款项
from windget import getToTAccTRcV


# 获取应收款项类投资时间序列
from windget import getRcVInvestSeries


# 获取应收款项类投资
from windget import getRcVInvest


# 获取金融投资时间序列
from windget import getFinInvestSeries


# 获取金融投资
from windget import getFinInvest


# 获取债权投资时间序列
from windget import getDebtInvestSeries


# 获取债权投资
from windget import getDebtInvest


# 获取其他债权投资时间序列
from windget import getOThDebtInvestSeries


# 获取其他债权投资
from windget import getOThDebtInvest


# 获取其他权益工具投资时间序列
from windget import getOThEqYInstrumentsInvestSeries


# 获取其他权益工具投资
from windget import getOThEqYInstrumentsInvest


# 获取持有至到期投资_GSD时间序列
from windget import getWgsDInvestHtmSeries


# 获取持有至到期投资_GSD
from windget import getWgsDInvestHtm


# 获取持有至到期投资时间序列
from windget import getHeldToMTyInvestSeries


# 获取持有至到期投资
from windget import getHeldToMTyInvest


# 获取长期应收款时间序列
from windget import getLongTermRecSeries


# 获取长期应收款
from windget import getLongTermRec


# 获取在建工程(合计)时间序列
from windget import getConstInProgToTSeries


# 获取在建工程(合计)
from windget import getConstInProgToT


# 获取在建工程时间序列
from windget import getConstInProgSeries


# 获取在建工程
from windget import getConstInProg


# 获取工程物资时间序列
from windget import getProJMAtlSeries


# 获取工程物资
from windget import getProJMAtl


# 获取开发支出时间序列
from windget import getRAndDCostsSeries


# 获取开发支出
from windget import getRAndDCosts


# 获取发放贷款及垫款时间序列
from windget import getLoansAndAdvGrantedSeries


# 获取发放贷款及垫款
from windget import getLoansAndAdvGranted


# 获取存放同业和其它金融机构款项时间序列
from windget import getAssetDepOThBanksFinInStSeries


# 获取存放同业和其它金融机构款项
from windget import getAssetDepOThBanksFinInSt


# 获取贵金属时间序列
from windget import getPreciousMetalsSeries


# 获取贵金属
from windget import getPreciousMetals


# 获取应收分保未到期责任准备金时间序列
from windget import getRcVCededUnearnedPremRsRvSeries


# 获取应收分保未到期责任准备金
from windget import getRcVCededUnearnedPremRsRv


# 获取应收分保未决赔款准备金时间序列
from windget import getRcVCededClaimRsRvSeries


# 获取应收分保未决赔款准备金
from windget import getRcVCededClaimRsRv


# 获取应收分保寿险责任准备金时间序列
from windget import getRcVCededLifeInSurRsRvSeries


# 获取应收分保寿险责任准备金
from windget import getRcVCededLifeInSurRsRv


# 获取应收分保长期健康险责任准备金时间序列
from windget import getRcVCededLtHealthInSurRsRvSeries


# 获取应收分保长期健康险责任准备金
from windget import getRcVCededLtHealthInSurRsRv


# 获取保户质押贷款时间序列
from windget import getInsuredPledgeLoanSeries


# 获取保户质押贷款
from windget import getInsuredPledgeLoan


# 获取存出资本保证金时间序列
from windget import getCapMrgnPaidSeries


# 获取存出资本保证金
from windget import getCapMrgnPaid


# 获取定期存款时间序列
from windget import getTimeDepositsSeries


# 获取定期存款
from windget import getTimeDeposits


# 获取应收代位追偿款时间序列
from windget import getSubRRecSeries


# 获取应收代位追偿款
from windget import getSubRRec


# 获取存出保证金时间序列
from windget import getMrgnPaidSeries


# 获取存出保证金
from windget import getMrgnPaid


# 获取存出保证金_FUND时间序列
from windget import getStmBs3Series


# 获取存出保证金_FUND
from windget import getStmBs3


# 获取交易席位费时间序列
from windget import getSeatFeesExchangeSeries


# 获取交易席位费
from windget import getSeatFeesExchange


# 获取客户资金存款时间序列
from windget import getClientsCapDepositSeries


# 获取客户资金存款
from windget import getClientsCapDeposit


# 获取客户备付金时间序列
from windget import getClientsRsRvSettleSeries


# 获取客户备付金
from windget import getClientsRsRvSettle


# 获取应付票据时间序列
from windget import getNotesPayableSeries


# 获取应付票据
from windget import getNotesPayable


# 获取应付账款及票据_GSD时间序列
from windget import getWgsDPayAccTSeries


# 获取应付账款及票据_GSD
from windget import getWgsDPayAccT


# 获取应付账款时间序列
from windget import getAccTPayableSeries


# 获取应付账款
from windget import getAccTPayable


# 获取预收账款时间序列
from windget import getAdvFromCuStSeries


# 获取预收账款
from windget import getAdvFromCuSt


# 获取应付款项时间序列
from windget import getToTAccTPayableSeries


# 获取应付款项
from windget import getToTAccTPayable


# 获取应付利息时间序列
from windget import getIntPayableSeries


# 获取应付利息
from windget import getIntPayable


# 获取应付利息_FUND时间序列
from windget import getStmBs29Series


# 获取应付利息_FUND
from windget import getStmBs29


# 获取应付股利时间序列
from windget import getDvdPayableSeries


# 获取应付股利
from windget import getDvdPayable


# 获取其他应付款时间序列
from windget import getOThPayableSeries


# 获取其他应付款
from windget import getOThPayable


# 获取预提费用时间序列
from windget import getAccExpSeries


# 获取预提费用
from windget import getAccExp


# 获取预提费用增加时间序列
from windget import getInCrAccExpSeries


# 获取预提费用增加
from windget import getInCrAccExp


# 获取单季度.预提费用增加时间序列
from windget import getQfaInCrAccExpSeries


# 获取单季度.预提费用增加
from windget import getQfaInCrAccExp


# 获取应付短期债券时间序列
from windget import getStBondsPayableSeries


# 获取应付短期债券
from windget import getStBondsPayable


# 获取吸收存款及同业存放时间序列
from windget import getDepositReceivedIbDepositsSeries


# 获取吸收存款及同业存放
from windget import getDepositReceivedIbDeposits


# 获取拆入资金_GSD时间序列
from windget import getWgsDBorrowIbSeries


# 获取拆入资金_GSD
from windget import getWgsDBorrowIb


# 获取拆入资金时间序列
from windget import getLoansOThBanksSeries


# 获取拆入资金
from windget import getLoansOThBanks


# 获取拆入资金净增加额时间序列
from windget import getNetInCrLoansOtherBankSeries


# 获取拆入资金净增加额
from windget import getNetInCrLoansOtherBank


# 获取单季度.拆入资金净增加额时间序列
from windget import getQfaNetInCrLoansOtherBankSeries


# 获取单季度.拆入资金净增加额
from windget import getQfaNetInCrLoansOtherBank


# 获取向其他金融机构拆入资金净增加额时间序列
from windget import getNetInCrFundBOrrOfISeries


# 获取向其他金融机构拆入资金净增加额
from windget import getNetInCrFundBOrrOfI


# 获取单季度.向其他金融机构拆入资金净增加额时间序列
from windget import getQfaNetInCrFundBOrrOfISeries


# 获取单季度.向其他金融机构拆入资金净增加额
from windget import getQfaNetInCrFundBOrrOfI


# 获取应付手续费及佣金时间序列
from windget import getHandlingChargesComMPayableSeries


# 获取应付手续费及佣金
from windget import getHandlingChargesComMPayable


# 获取应付分保账款时间序列
from windget import getPayableToReInsurerSeries


# 获取应付分保账款
from windget import getPayableToReInsurer


# 获取保险合同准备金时间序列
from windget import getRsRvInSurContSeries


# 获取保险合同准备金
from windget import getRsRvInSurCont


# 获取代理买卖证券款时间序列
from windget import getActingTradingSecSeries


# 获取代理买卖证券款
from windget import getActingTradingSec


# 获取代理承销证券款时间序列
from windget import getActingUwSecSeries


# 获取代理承销证券款
from windget import getActingUwSec


# 获取应付债券时间序列
from windget import getBondsPayableSeries


# 获取应付债券
from windget import getBondsPayable


# 获取长期应付款(合计)时间序列
from windget import getLtPayableToTSeries


# 获取长期应付款(合计)
from windget import getLtPayableToT


# 获取长期应付款时间序列
from windget import getLtPayableSeries


# 获取长期应付款
from windget import getLtPayable


# 获取专项应付款时间序列
from windget import getSpecificItemPayableSeries


# 获取专项应付款
from windget import getSpecificItemPayable


# 获取同业和其它金融机构存放款项时间序列
from windget import getLiaBDepOThBanksFinInStSeries


# 获取同业和其它金融机构存放款项
from windget import getLiaBDepOThBanksFinInSt


# 获取吸收存款时间序列
from windget import getCuStBankDepSeries


# 获取吸收存款
from windget import getCuStBankDep


# 获取应付赔付款时间序列
from windget import getClaimsPayableSeries


# 获取应付赔付款
from windget import getClaimsPayable


# 获取应付保单红利时间序列
from windget import getDvdPayableInsuredSeries


# 获取应付保单红利
from windget import getDvdPayableInsured


# 获取存入保证金时间序列
from windget import getDepositReceivedSeries


# 获取存入保证金
from windget import getDepositReceived


# 获取保户储金及投资款时间序列
from windget import getInsuredDepositInvestSeries


# 获取保户储金及投资款
from windget import getInsuredDepositInvest


# 获取未到期责任准备金变动_GSD时间序列
from windget import getWgsDChgRsvUnearnedPremiumSeries


# 获取未到期责任准备金变动_GSD
from windget import getWgsDChgRsvUnearnedPremium


# 获取未到期责任准备金时间序列
from windget import getUnearnedPremRsRvSeries


# 获取未到期责任准备金
from windget import getUnearnedPremRsRv


# 获取单季度.未到期责任准备金变动_GSD时间序列
from windget import getWgsDQfaChgRsvUnearnedPremiumSeries


# 获取单季度.未到期责任准备金变动_GSD
from windget import getWgsDQfaChgRsvUnearnedPremium


# 获取未决赔款准备金变动_GSD时间序列
from windget import getWgsDChgRsvOutstandingLossSeries


# 获取未决赔款准备金变动_GSD
from windget import getWgsDChgRsvOutstandingLoss


# 获取未决赔款准备金时间序列
from windget import getOutLossRsRvSeries


# 获取未决赔款准备金
from windget import getOutLossRsRv


# 获取单季度.未决赔款准备金变动_GSD时间序列
from windget import getWgsDQfaChgRsvOutstandingLossSeries


# 获取单季度.未决赔款准备金变动_GSD
from windget import getWgsDQfaChgRsvOutstandingLoss


# 获取寿险责任准备金时间序列
from windget import getLifeInSurRsRvSeries


# 获取寿险责任准备金
from windget import getLifeInSurRsRv


# 获取长期健康险责任准备金时间序列
from windget import getLtHealthInSurVSeries


# 获取长期健康险责任准备金
from windget import getLtHealthInSurV


# 获取预收保费时间序列
from windget import getPremReceivedAdvSeries


# 获取预收保费
from windget import getPremReceivedAdv


# 获取应付短期融资款时间序列
from windget import getStFinLInStPayableSeries


# 获取应付短期融资款
from windget import getStFinLInStPayable


# 获取其他权益工具时间序列
from windget import getOtherEquityInstrumentsSeries


# 获取其他权益工具
from windget import getOtherEquityInstruments


# 获取其他权益工具:永续债时间序列
from windget import getPerpetualDebtSeries


# 获取其他权益工具:永续债
from windget import getPerpetualDebt


# 获取库存股_GSD时间序列
from windget import getWgsDTreAsStKSeries


# 获取库存股_GSD
from windget import getWgsDTreAsStK


# 获取库存股时间序列
from windget import getTSyStKSeries


# 获取库存股
from windget import getTSyStK


# 获取专项储备时间序列
from windget import getSpecialRsRvSeries


# 获取专项储备
from windget import getSpecialRsRv


# 获取一般风险准备时间序列
from windget import getProvNomRisksSeries


# 获取一般风险准备
from windget import getProvNomRisks


# 获取外币报表折算差额时间序列
from windget import getCnVdDiffForeignCurRStatSeries


# 获取外币报表折算差额
from windget import getCnVdDiffForeignCurRStat


# 获取股东权益差额(特殊报表科目)时间序列
from windget import getSHrhLDrEqYGapSeries


# 获取股东权益差额(特殊报表科目)
from windget import getSHrhLDrEqYGap


# 获取其他股东权益差额说明(特殊报表科目)时间序列
from windget import getSHrhLDrEqYGapDetailSeries


# 获取其他股东权益差额说明(特殊报表科目)
from windget import getSHrhLDrEqYGapDetail


# 获取股东权益差额(合计平衡项目)时间序列
from windget import getSHrhLDrEqYNettingSeries


# 获取股东权益差额(合计平衡项目)
from windget import getSHrhLDrEqYNetting


# 获取归属母公司股东的权益/投入资本_GSD时间序列
from windget import getWgsDEquityToTotalCapitalSeries


# 获取归属母公司股东的权益/投入资本_GSD
from windget import getWgsDEquityToTotalCapital


# 获取归属母公司股东的权益时间序列
from windget import getEqYBelongToParComShSeries


# 获取归属母公司股东的权益
from windget import getEqYBelongToParComSh


# 获取归属母公司股东的权益(MRQ,只有最新数据)时间序列
from windget import getEquityMrQSeries


# 获取归属母公司股东的权益(MRQ,只有最新数据)
from windget import getEquityMrQ


# 获取少数股东权益_GSD时间序列
from windget import getWgsDMinIntSeries


# 获取少数股东权益_GSD
from windget import getWgsDMinInt


# 获取少数股东权益时间序列
from windget import getMinorityIntSeries


# 获取少数股东权益
from windget import getMinorityInt


# 获取收到的税费返还时间序列
from windget import getRecpTaxRendsSeries


# 获取收到的税费返还
from windget import getRecpTaxRends


# 获取单季度.收到的税费返还时间序列
from windget import getQfaRecpTaxRendsSeries


# 获取单季度.收到的税费返还
from windget import getQfaRecpTaxRends


# 获取收到其他与经营活动有关的现金时间序列
from windget import getOtherCashRecpRalOperActSeries


# 获取收到其他与经营活动有关的现金
from windget import getOtherCashRecpRalOperAct


# 获取单季度.收到其他与经营活动有关的现金时间序列
from windget import getQfaOtherCashRecpRalOperActSeries


# 获取单季度.收到其他与经营活动有关的现金
from windget import getQfaOtherCashRecpRalOperAct


# 获取保户储金净增加额时间序列
from windget import getNetInCrInsuredDepSeries


# 获取保户储金净增加额
from windget import getNetInCrInsuredDep


# 获取单季度.保户储金净增加额时间序列
from windget import getQfaNetInCrInsuredDepSeries


# 获取单季度.保户储金净增加额
from windget import getQfaNetInCrInsuredDep


# 获取客户存款和同业存放款项净增加额时间序列
from windget import getNetInCrDepCobSeries


# 获取客户存款和同业存放款项净增加额
from windget import getNetInCrDepCob


# 获取单季度.客户存款和同业存放款项净增加额时间序列
from windget import getQfaNetInCrDepCobSeries


# 获取单季度.客户存款和同业存放款项净增加额
from windget import getQfaNetInCrDepCob


# 获取收取利息和手续费净增加额时间序列
from windget import getNetInCrIntHandlingChrGSeries


# 获取收取利息和手续费净增加额
from windget import getNetInCrIntHandlingChrG


# 获取单季度.收取利息和手续费净增加额时间序列
from windget import getQfaNetInCrIntHandlingChrGSeries


# 获取单季度.收取利息和手续费净增加额
from windget import getQfaNetInCrIntHandlingChrG


# 获取收到原保险合同保费取得的现金时间序列
from windget import getCashRecpPremOrigInCoSeries


# 获取收到原保险合同保费取得的现金
from windget import getCashRecpPremOrigInCo


# 获取单季度.收到原保险合同保费取得的现金时间序列
from windget import getQfaCashRecpPremOrigInCoSeries


# 获取单季度.收到原保险合同保费取得的现金
from windget import getQfaCashRecpPremOrigInCo


# 获取收到再保业务现金净额时间序列
from windget import getNetCashReceivedReinsUBusSeries


# 获取收到再保业务现金净额
from windget import getNetCashReceivedReinsUBus


# 获取单季度.收到再保业务现金净额时间序列
from windget import getQfaNetCashReceivedReinsUBusSeries


# 获取单季度.收到再保业务现金净额
from windget import getQfaNetCashReceivedReinsUBus


# 获取回购业务资金净增加额时间序列
from windget import getNetInCrRepUrchBusFundSeries


# 获取回购业务资金净增加额
from windget import getNetInCrRepUrchBusFund


# 获取单季度.回购业务资金净增加额时间序列
from windget import getQfaNetInCrRepUrchBusFundSeries


# 获取单季度.回购业务资金净增加额
from windget import getQfaNetInCrRepUrchBusFund


# 获取代理买卖证券收到的现金净额时间序列
from windget import getNetCashFromSeUriTiesSeries


# 获取代理买卖证券收到的现金净额
from windget import getNetCashFromSeUriTies


# 获取经营活动现金流入差额(特殊报表科目)时间序列
from windget import getCashInFlowsOperActGapSeries


# 获取经营活动现金流入差额(特殊报表科目)
from windget import getCashInFlowsOperActGap


# 获取经营活动现金流入差额说明(特殊报表科目)时间序列
from windget import getCashInFlowsOperActGapDetailSeries


# 获取经营活动现金流入差额说明(特殊报表科目)
from windget import getCashInFlowsOperActGapDetail


# 获取经营活动现金流入差额(合计平衡项目)时间序列
from windget import getCashInFlowsOperActNettingSeries


# 获取经营活动现金流入差额(合计平衡项目)
from windget import getCashInFlowsOperActNetting


# 获取以公允价值计量且其变动计入当期损益的金融工具净额时间序列
from windget import getNetFinaInstrumentsMeasuredAtFmVSeries


# 获取以公允价值计量且其变动计入当期损益的金融工具净额
from windget import getNetFinaInstrumentsMeasuredAtFmV


# 获取支付给职工以及为职工支付的现金时间序列
from windget import getCashPayBehEMplSeries


# 获取支付给职工以及为职工支付的现金
from windget import getCashPayBehEMpl


# 获取单季度.支付给职工以及为职工支付的现金时间序列
from windget import getQfaCashPayBehEMplSeries


# 获取单季度.支付给职工以及为职工支付的现金
from windget import getQfaCashPayBehEMpl


# 获取客户贷款及垫款净增加额时间序列
from windget import getNetInCrClientsLoanAdvSeries


# 获取客户贷款及垫款净增加额
from windget import getNetInCrClientsLoanAdv


# 获取单季度.客户贷款及垫款净增加额时间序列
from windget import getQfaNetInCrClientsLoanAdvSeries


# 获取单季度.客户贷款及垫款净增加额
from windget import getQfaNetInCrClientsLoanAdv


# 获取存放央行和同业款项净增加额时间序列
from windget import getNetInCrDepCBobSeries


# 获取存放央行和同业款项净增加额
from windget import getNetInCrDepCBob


# 获取单季度.存放央行和同业款项净增加额时间序列
from windget import getQfaNetInCrDepCBobSeries


# 获取单季度.存放央行和同业款项净增加额
from windget import getQfaNetInCrDepCBob


# 获取支付原保险合同赔付款项的现金时间序列
from windget import getCashPayClaimsOrigInCoSeries


# 获取支付原保险合同赔付款项的现金
from windget import getCashPayClaimsOrigInCo


# 获取单季度.支付原保险合同赔付款项的现金时间序列
from windget import getQfaCashPayClaimsOrigInCoSeries


# 获取单季度.支付原保险合同赔付款项的现金
from windget import getQfaCashPayClaimsOrigInCo


# 获取支付手续费的现金时间序列
from windget import getHandlingChrGPaidSeries


# 获取支付手续费的现金
from windget import getHandlingChrGPaid


# 获取单季度.支付手续费的现金时间序列
from windget import getQfaHandlingChrGPaidSeries


# 获取单季度.支付手续费的现金
from windget import getQfaHandlingChrGPaid


# 获取支付保单红利的现金时间序列
from windget import getComMInSurPlcYPaidSeries


# 获取支付保单红利的现金
from windget import getComMInSurPlcYPaid


# 获取单季度.支付保单红利的现金时间序列
from windget import getQfaComMInSurPlcYPaidSeries


# 获取单季度.支付保单红利的现金
from windget import getQfaComMInSurPlcYPaid


# 获取经营活动现金流出差额(特殊报表科目)时间序列
from windget import getCashOutFlowsOperActGapSeries


# 获取经营活动现金流出差额(特殊报表科目)
from windget import getCashOutFlowsOperActGap


# 获取经营活动现金流出差额说明(特殊报表科目)时间序列
from windget import getCashOutFlowsOperActGapDetailSeries


# 获取经营活动现金流出差额说明(特殊报表科目)
from windget import getCashOutFlowsOperActGapDetail


# 获取经营活动现金流出差额(合计平衡项目)时间序列
from windget import getCashOutFlowsOperActNettingSeries


# 获取经营活动现金流出差额(合计平衡项目)
from windget import getCashOutFlowsOperActNetting


# 获取收回投资收到的现金时间序列
from windget import getCashRecpDispWithDrWLInvestSeries


# 获取收回投资收到的现金
from windget import getCashRecpDispWithDrWLInvest


# 获取单季度.收回投资收到的现金时间序列
from windget import getQfaCashRecpDispWithDrWLInvestSeries


# 获取单季度.收回投资收到的现金
from windget import getQfaCashRecpDispWithDrWLInvest


# 获取处置子公司及其他营业单位收到的现金净额时间序列
from windget import getNetCashRecpDispSoBuSeries


# 获取处置子公司及其他营业单位收到的现金净额
from windget import getNetCashRecpDispSoBu


# 获取单季度.处置子公司及其他营业单位收到的现金净额时间序列
from windget import getQfaNetCashRecpDispSoBuSeries


# 获取单季度.处置子公司及其他营业单位收到的现金净额
from windget import getQfaNetCashRecpDispSoBu


# 获取收到其他与投资活动有关的现金时间序列
from windget import getOtherCashRecpRalInvActSeries


# 获取收到其他与投资活动有关的现金
from windget import getOtherCashRecpRalInvAct


# 获取单季度.收到其他与投资活动有关的现金时间序列
from windget import getQfaOtherCashRecpRalInvActSeries


# 获取单季度.收到其他与投资活动有关的现金
from windget import getQfaOtherCashRecpRalInvAct


# 获取投资活动现金流入差额(特殊报表科目)时间序列
from windget import getCashInFlowsInvActGapSeries


# 获取投资活动现金流入差额(特殊报表科目)
from windget import getCashInFlowsInvActGap


# 获取投资活动现金流入差额说明(特殊报表科目)时间序列
from windget import getCashInFlowsInvActGapDetailSeries


# 获取投资活动现金流入差额说明(特殊报表科目)
from windget import getCashInFlowsInvActGapDetail


# 获取投资活动现金流入差额(合计平衡项目)时间序列
from windget import getCashInFlowsInvActNettingSeries


# 获取投资活动现金流入差额(合计平衡项目)
from windget import getCashInFlowsInvActNetting


# 获取投资支付的现金时间序列
from windget import getCashPaidInvestSeries


# 获取投资支付的现金
from windget import getCashPaidInvest


# 获取单季度.投资支付的现金时间序列
from windget import getQfaCashPaidInvestSeries


# 获取单季度.投资支付的现金
from windget import getQfaCashPaidInvest


# 获取质押贷款净增加额时间序列
from windget import getNetInCrPledgeLoanSeries


# 获取质押贷款净增加额
from windget import getNetInCrPledgeLoan


# 获取单季度.质押贷款净增加额时间序列
from windget import getQfaNetInCrPledgeLoanSeries


# 获取单季度.质押贷款净增加额
from windget import getQfaNetInCrPledgeLoan


# 获取取得子公司及其他营业单位支付的现金净额时间序列
from windget import getNetCashPayAQuisSoBuSeries


# 获取取得子公司及其他营业单位支付的现金净额
from windget import getNetCashPayAQuisSoBu


# 获取单季度.取得子公司及其他营业单位支付的现金净额时间序列
from windget import getQfaNetCashPayAQuisSoBuSeries


# 获取单季度.取得子公司及其他营业单位支付的现金净额
from windget import getQfaNetCashPayAQuisSoBu


# 获取支付其他与投资活动有关的现金时间序列
from windget import getOtherCashPayRalInvActSeries


# 获取支付其他与投资活动有关的现金
from windget import getOtherCashPayRalInvAct


# 获取单季度.支付其他与投资活动有关的现金时间序列
from windget import getQfaOtherCashPayRalInvActSeries


# 获取单季度.支付其他与投资活动有关的现金
from windget import getQfaOtherCashPayRalInvAct


# 获取投资活动现金流出差额(特殊报表科目)时间序列
from windget import getCashOutFlowsInvActGapSeries


# 获取投资活动现金流出差额(特殊报表科目)
from windget import getCashOutFlowsInvActGap


# 获取投资活动现金流出差额说明(特殊报表科目)时间序列
from windget import getCashOutFlowsInvActGapDetailSeries


# 获取投资活动现金流出差额说明(特殊报表科目)
from windget import getCashOutFlowsInvActGapDetail


# 获取投资活动现金流出差额(合计平衡项目)时间序列
from windget import getCashOutFlowsInvActNettingSeries


# 获取投资活动现金流出差额(合计平衡项目)
from windget import getCashOutFlowsInvActNetting


# 获取吸收投资收到的现金时间序列
from windget import getCashRecpCapContribSeries


# 获取吸收投资收到的现金
from windget import getCashRecpCapContrib


# 获取单季度.吸收投资收到的现金时间序列
from windget import getQfaCashRecpCapContribSeries


# 获取单季度.吸收投资收到的现金
from windget import getQfaCashRecpCapContrib


# 获取子公司吸收少数股东投资收到的现金时间序列
from windget import getCashRecSAimsSeries


# 获取子公司吸收少数股东投资收到的现金
from windget import getCashRecSAims


# 获取单季度.子公司吸收少数股东投资收到的现金时间序列
from windget import getQfaCashRecSAimsSeries


# 获取单季度.子公司吸收少数股东投资收到的现金
from windget import getQfaCashRecSAims


# 获取收到其他与筹资活动有关的现金时间序列
from windget import getOtherCashRecpRalFncActSeries


# 获取收到其他与筹资活动有关的现金
from windget import getOtherCashRecpRalFncAct


# 获取单季度.收到其他与筹资活动有关的现金时间序列
from windget import getQfaOtherCashRecpRalFncActSeries


# 获取单季度.收到其他与筹资活动有关的现金
from windget import getQfaOtherCashRecpRalFncAct


# 获取发行债券收到的现金时间序列
from windget import getProcIssueBondsSeries


# 获取发行债券收到的现金
from windget import getProcIssueBonds


# 获取单季度.发行债券收到的现金时间序列
from windget import getQfaProcIssueBondsSeries


# 获取单季度.发行债券收到的现金
from windget import getQfaProcIssueBonds


# 获取筹资活动现金流入差额(特殊报表科目)时间序列
from windget import getCashInFlowsFncActGapSeries


# 获取筹资活动现金流入差额(特殊报表科目)
from windget import getCashInFlowsFncActGap


# 获取筹资活动现金流入差额说明(特殊报表科目)时间序列
from windget import getCashInFlowsFncActGapDetailSeries


# 获取筹资活动现金流入差额说明(特殊报表科目)
from windget import getCashInFlowsFncActGapDetail


# 获取筹资活动现金流入差额(合计平衡项目)时间序列
from windget import getCashInFlowsFncActNettingSeries


# 获取筹资活动现金流入差额(合计平衡项目)
from windget import getCashInFlowsFncActNetting


# 获取偿还债务支付的现金时间序列
from windget import getCashPrepayAmtBOrrSeries


# 获取偿还债务支付的现金
from windget import getCashPrepayAmtBOrr


# 获取单季度.偿还债务支付的现金时间序列
from windget import getQfaCashPrepayAmtBOrrSeries


# 获取单季度.偿还债务支付的现金
from windget import getQfaCashPrepayAmtBOrr


# 获取分配股利、利润或偿付利息支付的现金时间序列
from windget import getCashPayDistDpcpIntExpSeries


# 获取分配股利、利润或偿付利息支付的现金
from windget import getCashPayDistDpcpIntExp


# 获取单季度.分配股利、利润或偿付利息支付的现金时间序列
from windget import getQfaCashPayDistDpcpIntExpSeries


# 获取单季度.分配股利、利润或偿付利息支付的现金
from windget import getQfaCashPayDistDpcpIntExp


# 获取子公司支付给少数股东的股利、利润时间序列
from windget import getDvdProfitPaidScMsSeries


# 获取子公司支付给少数股东的股利、利润
from windget import getDvdProfitPaidScMs


# 获取单季度.子公司支付给少数股东的股利、利润时间序列
from windget import getQfaDvdProfitPaidScMsSeries


# 获取单季度.子公司支付给少数股东的股利、利润
from windget import getQfaDvdProfitPaidScMs


# 获取支付其他与筹资活动有关的现金时间序列
from windget import getOtherCashPayRalFncActSeries


# 获取支付其他与筹资活动有关的现金
from windget import getOtherCashPayRalFncAct


# 获取单季度.支付其他与筹资活动有关的现金时间序列
from windget import getQfaOtherCashPayRalFncActSeries


# 获取单季度.支付其他与筹资活动有关的现金
from windget import getQfaOtherCashPayRalFncAct


# 获取筹资活动现金流出差额(特殊报表科目)时间序列
from windget import getCashOutFlowsFncActGapSeries


# 获取筹资活动现金流出差额(特殊报表科目)
from windget import getCashOutFlowsFncActGap


# 获取筹资活动现金流出差额说明(特殊报表科目)时间序列
from windget import getCashOutFlowsFncActGapDetailSeries


# 获取筹资活动现金流出差额说明(特殊报表科目)
from windget import getCashOutFlowsFncActGapDetail


# 获取筹资活动现金流出差额(合计平衡项目)时间序列
from windget import getCashOutFlowsFncActNettingSeries


# 获取筹资活动现金流出差额(合计平衡项目)
from windget import getCashOutFlowsFncActNetting


# 获取汇率变动对现金的影响时间序列
from windget import getEffFxFluCashSeries


# 获取汇率变动对现金的影响
from windget import getEffFxFluCash


# 获取单季度.汇率变动对现金的影响时间序列
from windget import getQfaEffFxFluCashSeries


# 获取单季度.汇率变动对现金的影响
from windget import getQfaEffFxFluCash


# 获取公允价值变动损失时间序列
from windget import getLossFvChgSeries


# 获取公允价值变动损失
from windget import getLossFvChg


# 获取单季度.公允价值变动损失时间序列
from windget import getQfaLossFvChgSeries


# 获取单季度.公允价值变动损失
from windget import getQfaLossFvChg


# 获取投资损失时间序列
from windget import getInvestLossSeries


# 获取投资损失
from windget import getInvestLoss


# 获取单季度.投资损失时间序列
from windget import getQfaInvestLossSeries


# 获取单季度.投资损失
from windget import getQfaInvestLoss


# 获取经营性应收项目的减少时间序列
from windget import getDecrOperPayableSeries


# 获取经营性应收项目的减少
from windget import getDecrOperPayable


# 获取单季度.经营性应收项目的减少时间序列
from windget import getQfaDecrOperPayableSeries


# 获取单季度.经营性应收项目的减少
from windget import getQfaDecrOperPayable


# 获取经营性应付项目的增加时间序列
from windget import getInCrOperPayableSeries


# 获取经营性应付项目的增加
from windget import getInCrOperPayable


# 获取单季度.经营性应付项目的增加时间序列
from windget import getQfaInCrOperPayableSeries


# 获取单季度.经营性应付项目的增加
from windget import getQfaInCrOperPayable


# 获取其他短期投资_GSD时间序列
from windget import getWgsDInvestStOThSeries


# 获取其他短期投资_GSD
from windget import getWgsDInvestStOTh


# 获取其他长期投资_GSD时间序列
from windget import getWgsDInvestLtOThSeries


# 获取其他长期投资_GSD
from windget import getWgsDInvestLtOTh


# 获取其他投资_GSD时间序列
from windget import getWgsDInvestOThSeries


# 获取其他投资_GSD
from windget import getWgsDInvestOTh


# 获取其他储备_GSD时间序列
from windget import getWgsDRsvOtherSeries


# 获取其他储备_GSD
from windget import getWgsDRsvOther


# 获取其他营业费用合计_GSD时间序列
from windget import getWgsDToTExpOThSeries


# 获取其他营业费用合计_GSD
from windget import getWgsDToTExpOTh


# 获取其他非经营性损益_GSD时间序列
from windget import getWgsDNoOperIncSeries


# 获取其他非经营性损益_GSD
from windget import getWgsDNoOperInc


# 获取其他特殊项_GSD时间序列
from windget import getWgsDExoDSeries


# 获取其他特殊项_GSD
from windget import getWgsDExoD


# 获取其他非现金调整_GSD时间序列
from windget import getWgsDNonCashChgSeries


# 获取其他非现金调整_GSD
from windget import getWgsDNonCashChg


# 获取其他时间序列
from windget import getOthersSeries


# 获取其他
from windget import getOthers


# 获取其他收入_FUND时间序列
from windget import getStmIs9Series


# 获取其他收入_FUND
from windget import getStmIs9


# 获取其他费用_FUND时间序列
from windget import getStmIs37Series


# 获取其他费用_FUND
from windget import getStmIs37


# 获取单季度.其他特殊项_GSD时间序列
from windget import getWgsDQfaExoDSeries


# 获取单季度.其他特殊项_GSD
from windget import getWgsDQfaExoD


# 获取单季度.其他营业费用合计_GSD时间序列
from windget import getWgsDQfaToTExpOThSeries


# 获取单季度.其他营业费用合计_GSD
from windget import getWgsDQfaToTExpOTh


# 获取单季度.其他非经营性损益_GSD时间序列
from windget import getWgsDQfaNoOperIncSeries


# 获取单季度.其他非经营性损益_GSD
from windget import getWgsDQfaNoOperInc


# 获取单季度.其他非现金调整_GSD时间序列
from windget import getWgsDQfaNonCashChgSeries


# 获取单季度.其他非现金调整_GSD
from windget import getWgsDQfaNonCashChg


# 获取单季度.其他时间序列
from windget import getQfaOthersSeries


# 获取单季度.其他
from windget import getQfaOthers


# 获取债务转为资本时间序列
from windget import getConVDebtIntoCapSeries


# 获取债务转为资本
from windget import getConVDebtIntoCap


# 获取单季度.债务转为资本时间序列
from windget import getQfaConVDebtIntoCapSeries


# 获取单季度.债务转为资本
from windget import getQfaConVDebtIntoCap


# 获取一年内到期的可转换公司债券时间序列
from windget import getConVCorpBondsDueWithin1YSeries


# 获取一年内到期的可转换公司债券
from windget import getConVCorpBondsDueWithin1Y


# 获取单季度.一年内到期的可转换公司债券时间序列
from windget import getQfaConVCorpBondsDueWithin1YSeries


# 获取单季度.一年内到期的可转换公司债券
from windget import getQfaConVCorpBondsDueWithin1Y


# 获取现金的期末余额时间序列
from windget import getEndBalCashSeries


# 获取现金的期末余额
from windget import getEndBalCash


# 获取单季度.现金的期末余额时间序列
from windget import getQfaEndBalCashSeries


# 获取单季度.现金的期末余额
from windget import getQfaEndBalCash


# 获取现金的期初余额时间序列
from windget import getBegBalCashSeries


# 获取现金的期初余额
from windget import getBegBalCash


# 获取现金等价物的期末余额时间序列
from windget import getEndBalCashEquSeries


# 获取现金等价物的期末余额
from windget import getEndBalCashEqu


# 获取单季度.现金等价物的期末余额时间序列
from windget import getQfaEndBalCashEquSeries


# 获取单季度.现金等价物的期末余额
from windget import getQfaEndBalCashEqu


# 获取现金等价物的期初余额时间序列
from windget import getBegBalCashEquSeries


# 获取现金等价物的期初余额
from windget import getBegBalCashEqu


# 获取间接法-现金净增加额差额(特殊报表科目)时间序列
from windget import getImNetInCrCashCashEquGapSeries


# 获取间接法-现金净增加额差额(特殊报表科目)
from windget import getImNetInCrCashCashEquGap


# 获取间接法-现金净增加额差额说明(特殊报表科目)时间序列
from windget import getImNetInCrCashCashEquGapDetailSeries


# 获取间接法-现金净增加额差额说明(特殊报表科目)
from windget import getImNetInCrCashCashEquGapDetail


# 获取间接法-现金净增加额差额(合计平衡项目)时间序列
from windget import getImNetInCrCashCashEquNettingSeries


# 获取间接法-现金净增加额差额(合计平衡项目)
from windget import getImNetInCrCashCashEquNetting


# 获取网下QFII投资账户配售数量时间序列
from windget import getFundReItSqFsSeries


# 获取网下QFII投资账户配售数量
from windget import getFundReItSqFs


# 获取网下QFII投资账户配售金额时间序列
from windget import getFundReItSqFmSeries


# 获取网下QFII投资账户配售金额
from windget import getFundReItSqFm


# 获取网下QFII投资账户配售份额占比时间序列
from windget import getFundReItSqFrSeries


# 获取网下QFII投资账户配售份额占比
from windget import getFundReItSqFr


# 获取Delta时间序列
from windget import getDeltaSeries


# 获取Delta
from windget import getDelta


# 获取Delta(交易所)时间序列
from windget import getDeltaExChSeries


# 获取Delta(交易所)
from windget import getDeltaExCh


# 获取Gamma时间序列
from windget import getGammaSeries


# 获取Gamma
from windget import getGamma


# 获取Gamma(交易所)时间序列
from windget import getGammaExChSeries


# 获取Gamma(交易所)
from windget import getGammaExCh


# 获取Vega时间序列
from windget import getVegaSeries


# 获取Vega
from windget import getVega


# 获取Vega(交易所)时间序列
from windget import getVegaExChSeries


# 获取Vega(交易所)
from windget import getVegaExCh


# 获取Theta时间序列
from windget import getThetaSeries


# 获取Theta
from windget import getTheta


# 获取Theta(交易所)时间序列
from windget import getThetaExChSeries


# 获取Theta(交易所)
from windget import getThetaExCh


# 获取Rho时间序列
from windget import getRhoSeries


# 获取Rho
from windget import getRho


# 获取Rho(交易所)时间序列
from windget import getRhoExChSeries


# 获取Rho(交易所)
from windget import getRhoExCh


# 获取IOPV时间序列
from windget import getIoPvSeries


# 获取IOPV
from windget import getIoPv


# 获取IOPV溢折率时间序列
from windget import getNavIoPvDiscountRatioSeries


# 获取IOPV溢折率
from windget import getNavIoPvDiscountRatio


# 获取Alpha时间序列
from windget import getAlpha2Series


# 获取Alpha
from windget import getAlpha2


# 获取Alpha_FUND时间序列
from windget import getRiskAlphaSeries


# 获取Alpha_FUND
from windget import getRiskAlpha


# 获取Alpha(年化)时间序列
from windget import getRiskAnnualPhaSeries


# 获取Alpha(年化)
from windget import getRiskAnnualPha


# 获取Alpha同类平均时间序列
from windget import getRiskSimLAvgAlphaSeries


# 获取Alpha同类平均
from windget import getRiskSimLAvgAlpha


# 获取Alpha(年化)同类平均时间序列
from windget import getRiskSimLAvgAnnualPhaSeries


# 获取Alpha(年化)同类平均
from windget import getRiskSimLAvgAnnualPha


# 获取BETA值(最近100周)时间序列
from windget import getBeta100WSeries


# 获取BETA值(最近100周)
from windget import getBeta100W


# 获取BETA值(最近24个月)时间序列
from windget import getBeta24MSeries


# 获取BETA值(最近24个月)
from windget import getBeta24M


# 获取BETA值(最近60个月)时间序列
from windget import getBeta60MSeries


# 获取BETA值(最近60个月)
from windget import getBeta60M


# 获取Beta时间序列
from windget import getBetaSeries


# 获取Beta
from windget import getBeta


# 获取Beta(剔除财务杠杆)时间序列
from windget import getBetaDfSeries


# 获取Beta(剔除财务杠杆)
from windget import getBetaDf


# 获取Beta_FUND时间序列
from windget import getRiskBetaSeries


# 获取Beta_FUND
from windget import getRiskBeta


# 获取个股20日的beta值_PIT时间序列
from windget import getRiskBeta20Series


# 获取个股20日的beta值_PIT
from windget import getRiskBeta20


# 获取个股60日的beta值_PIT时间序列
from windget import getRiskBeta60Series


# 获取个股60日的beta值_PIT
from windget import getRiskBeta60


# 获取个股120日的beta值_PIT时间序列
from windget import getRiskBeta120Series


# 获取个股120日的beta值_PIT
from windget import getRiskBeta120


# 获取Beta同类平均时间序列
from windget import getRiskSimLAvgBetaSeries


# 获取Beta同类平均
from windget import getRiskSimLAvgBeta


# 获取Jensen时间序列
from windget import getJensenSeries


# 获取Jensen
from windget import getJensen


# 获取Jensen(年化)时间序列
from windget import getJensenYSeries


# 获取Jensen(年化)
from windget import getJensenY


# 获取Jensen_FUND时间序列
from windget import getRiskJensenSeries


# 获取Jensen_FUND
from windget import getRiskJensen


# 获取Jensen(年化)_FUND时间序列
from windget import getRiskAnNuJensenSeries


# 获取Jensen(年化)_FUND
from windget import getRiskAnNuJensen


# 获取IRR时间序列
from windget import getTBfIRrSeries


# 获取IRR
from windget import getTBfIRr


# 获取IRR(支持历史)时间序列
from windget import getTBfIRr2Series


# 获取IRR(支持历史)
from windget import getTBfIRr2


# 获取营业外收支净额(TTM)时间序列
from windget import getNonOperateProfitTtM2Series


# 获取营业外收支净额(TTM)
from windget import getNonOperateProfitTtM2


# 获取营业开支_GSD时间序列
from windget import getWgsDOperExpSeries


# 获取营业开支_GSD
from windget import getWgsDOperExp


# 获取运营资本_PIT时间序列
from windget import getFaWorkCapitalSeries


# 获取运营资本_PIT
from windget import getFaWorkCapital


# 获取营业外收支净额(TTM)_PIT时间序列
from windget import getFaNoOperProfitTtMSeries


# 获取营业外收支净额(TTM)_PIT
from windget import getFaNoOperProfitTtM


# 获取营业外收支净额(TTM,只有最新数据)时间序列
from windget import getNonOperateProfitTtMSeries


# 获取营业外收支净额(TTM,只有最新数据)
from windget import getNonOperateProfitTtM


# 获取自营业务收入_GSD时间序列
from windget import getWgsDTradeIncSeries


# 获取自营业务收入_GSD
from windget import getWgsDTradeInc


# 获取留存盈余比率(TTM)_PIT时间序列
from windget import getFaRetainedEarnTtMSeries


# 获取留存盈余比率(TTM)_PIT
from windget import getFaRetainedEarnTtM


# 获取BR意愿指标_PIT时间序列
from windget import getTechBrSeries


# 获取BR意愿指标_PIT
from windget import getTechBr


# 获取基金经营业绩_FUND时间序列
from windget import getStmIs25Series


# 获取基金经营业绩_FUND
from windget import getStmIs25


# 获取单季度.自营业务收入_GSD时间序列
from windget import getWgsDQfaTradeIncSeries


# 获取单季度.自营业务收入_GSD
from windget import getWgsDQfaTradeInc


# 获取ARBR人气意愿指标_PIT时间序列
from windget import getTechARbrSeries


# 获取ARBR人气意愿指标_PIT
from windget import getTechARbr


# 获取一致预测每股收益(FY2)与一致预测每股收益(FY1)的变化率_PIT时间序列
from windget import getWestEpsFyGrowthSeries


# 获取一致预测每股收益(FY2)与一致预测每股收益(FY1)的变化率_PIT
from windget import getWestEpsFyGrowth


# 获取一致预测每股收益(FY1)最大与一致预测每股收益(FY1)最小值的变化率_PIT时间序列
from windget import getWestEpsMaxMinFy1Series


# 获取一致预测每股收益(FY1)最大与一致预测每股收益(FY1)最小值的变化率_PIT
from windget import getWestEpsMaxMinFy1


# 获取Sharpe(年化)时间序列
from windget import getSharpeSeries


# 获取Sharpe(年化)
from windget import getSharpe


# 获取Sharpe时间序列
from windget import getRiskSharpeSeries


# 获取Sharpe
from windget import getRiskSharpe


# 获取Sharpe(年化)_FUND时间序列
from windget import getRiskAnNuSharpeSeries


# 获取Sharpe(年化)_FUND
from windget import getRiskAnNuSharpe


# 获取Sharpe同类平均时间序列
from windget import getRiskSimLAvgSharpeSeries


# 获取Sharpe同类平均
from windget import getRiskSimLAvgSharpe


# 获取Sharpe(年化)同类平均时间序列
from windget import getRiskSimLAvgAnNuSharpeSeries


# 获取Sharpe(年化)同类平均
from windget import getRiskSimLAvgAnNuSharpe


# 获取Treynor(年化)时间序列
from windget import getTreyNorSeries


# 获取Treynor(年化)
from windget import getTreyNor


# 获取Treynor时间序列
from windget import getRiskTreyNorSeries


# 获取Treynor
from windget import getRiskTreyNor


# 获取20日特诺雷比率_PIT时间序列
from windget import getRiskTreyNorRatio20Series


# 获取20日特诺雷比率_PIT
from windget import getRiskTreyNorRatio20


# 获取60日特诺雷比率_PIT时间序列
from windget import getRiskTreyNorRatio60Series


# 获取60日特诺雷比率_PIT
from windget import getRiskTreyNorRatio60


# 获取120日特诺雷比率_PIT时间序列
from windget import getRiskTreyNorRatio120Series


# 获取120日特诺雷比率_PIT
from windget import getRiskTreyNorRatio120


# 获取Treynor(年化)_FUND时间序列
from windget import getRiskAnNutReyNorSeries


# 获取Treynor(年化)_FUND
from windget import getRiskAnNutReyNor


# 获取Sortino时间序列
from windget import getRiskSortInOSeries


# 获取Sortino
from windget import getRiskSortInO


# 获取Sortino(年化)时间序列
from windget import getRiskAnNuSortInOSeries


# 获取Sortino(年化)
from windget import getRiskAnNuSortInO


# 获取Sortino同类平均时间序列
from windget import getRiskSimLAvgSortInOSeries


# 获取Sortino同类平均
from windget import getRiskSimLAvgSortInO


# 获取Sortino(年化)同类平均时间序列
from windget import getRiskSimLAvgAnNuSortInOSeries


# 获取Sortino(年化)同类平均
from windget import getRiskSimLAvgAnNuSortInO


# 获取Calmar时间序列
from windget import getRiskCalmaRSeries


# 获取Calmar
from windget import getRiskCalmaR


# 获取Sterling1时间序列
from windget import getRiskSterling1Series


# 获取Sterling1
from windget import getRiskSterling1


# 获取Sterling2时间序列
from windget import getRiskSterling2Series


# 获取Sterling2
from windget import getRiskSterling2


# 获取CTD时间序列
from windget import getTBfCTdSeries


# 获取CTD
from windget import getTBfCTd


# 获取CTD(支持历史)时间序列
from windget import getTBfCTd2Series


# 获取CTD(支持历史)
from windget import getTBfCTd2


# 获取市盈率PE(TTM)时间序列
from windget import getPeTtMSeries


# 获取市盈率PE(TTM)
from windget import getPeTtM


# 获取市销率PS(TTM)时间序列
from windget import getPsTtMSeries


# 获取市销率PS(TTM)
from windget import getPsTtM


# 获取每股收益EPS(TTM)时间序列
from windget import getEpsTtMSeries


# 获取每股收益EPS(TTM)
from windget import getEpsTtM


# 获取市盈率PE(TTM,剔除负值)时间序列
from windget import getValPeNonNegativeSeries


# 获取市盈率PE(TTM,剔除负值)
from windget import getValPeNonNegative


# 获取市盈率PE(TTM,中位数)时间序列
from windget import getValPeMedianSeries


# 获取市盈率PE(TTM,中位数)
from windget import getValPeMedian


# 获取投入资本回报率ROIC(TTM)时间序列
from windget import getRoiCTtM2Series


# 获取投入资本回报率ROIC(TTM)
from windget import getRoiCTtM2


# 获取息税前利润(TTM反推法)时间序列
from windget import getEbItTtM2Series


# 获取息税前利润(TTM反推法)
from windget import getEbItTtM2


# 获取投入资本回报率(TTM)_GSD时间序列
from windget import getRoiCTtM3Series


# 获取投入资本回报率(TTM)_GSD
from windget import getRoiCTtM3


# 获取息税前利润(TTM反推法)_GSD时间序列
from windget import getEbItTtM3Series


# 获取息税前利润(TTM反推法)_GSD
from windget import getEbItTtM3


# 获取息税前利润(TTM,只有最新数据)时间序列
from windget import getEbItTtMSeries


# 获取息税前利润(TTM,只有最新数据)
from windget import getEbItTtM


# 获取(废弃)投入资本回报率(TTM)时间序列
from windget import getRoiCTtMSeries


# 获取(废弃)投入资本回报率(TTM)
from windget import getRoiCTtM


# 获取区间最高PE(TTM)时间序列
from windget import getValPetTmHighSeries


# 获取区间最高PE(TTM)
from windget import getValPetTmHigh


# 获取区间最低PE(TTM)时间序列
from windget import getValPetTmLowSeries


# 获取区间最低PE(TTM)
from windget import getValPetTmLow


# 获取区间平均PE(TTM)时间序列
from windget import getValPetTmAvgSeries


# 获取区间平均PE(TTM)
from windget import getValPetTmAvg


# 获取区间最高PS(TTM)时间序列
from windget import getValPstTmHighSeries


# 获取区间最高PS(TTM)
from windget import getValPstTmHigh


# 获取区间最低PS(TTM)时间序列
from windget import getValPstTmLowSeries


# 获取区间最低PS(TTM)
from windget import getValPstTmLow


# 获取区间平均PS(TTM)时间序列
from windget import getValPstTmAvgSeries


# 获取区间平均PS(TTM)
from windget import getValPstTmAvg


# 获取投入资本回报率(TTM)时间序列
from windget import getRoiC2TtMSeries


# 获取投入资本回报率(TTM)
from windget import getRoiC2TtM


# 获取EBIT(TTM)时间序列
from windget import getEbIt2TtMSeries


# 获取EBIT(TTM)
from windget import getEbIt2TtM


# 获取投入资本回报率ROIC(TTM)_GSD时间序列
from windget import getRoiC2TtM2Series


# 获取投入资本回报率ROIC(TTM)_GSD
from windget import getRoiC2TtM2


# 获取EBIT(TTM)_GSD时间序列
from windget import getEbIt2TtM3Series


# 获取EBIT(TTM)_GSD
from windget import getEbIt2TtM3


# 获取市盈率PE(TTM,加权)时间序列
from windget import getValPeTtMwGtSeries


# 获取市盈率PE(TTM,加权)
from windget import getValPeTtMwGt


# 获取发布方市盈率PE(TTM)时间序列
from windget import getValPeTtMIssuerSeries


# 获取发布方市盈率PE(TTM)
from windget import getValPeTtMIssuer


# 获取市销率PS(TTM,加权)时间序列
from windget import getValPsTtMwGtSeries


# 获取市销率PS(TTM,加权)
from windget import getValPsTtMwGt


# 获取EBITDA(TTM反推法)时间序列
from windget import getEbItDaTtMSeries


# 获取EBITDA(TTM反推法)
from windget import getEbItDaTtM


# 获取EBITDA(TTM反推法)_GSD时间序列
from windget import getEbItDaTtM3Series


# 获取EBITDA(TTM反推法)_GSD
from windget import getEbItDaTtM3


# 获取资本报酬率(TTM)_PIT时间序列
from windget import getFaRocTtMSeries


# 获取资本报酬率(TTM)_PIT
from windget import getFaRocTtM


# 获取权益回报率(TTM)_PIT时间序列
from windget import getFaRoeTtMSeries


# 获取权益回报率(TTM)_PIT
from windget import getFaRoeTtM


# 获取市现率PCF(经营现金流TTM)时间序列
from windget import getPcfOCFTtMSeries


# 获取市现率PCF(经营现金流TTM)
from windget import getPcfOCFTtM


# 获取市现率PCF(现金净流量TTM)时间序列
from windget import getPcfNCfTtMSeries


# 获取市现率PCF(现金净流量TTM)
from windget import getPcfNCfTtM


# 获取EBITDA(TTM)时间序列
from windget import getEbItDa2TtMSeries


# 获取EBITDA(TTM)
from windget import getEbItDa2TtM


# 获取EBITDA(TTM)_GSD时间序列
from windget import getEbItDa2TtM2Series


# 获取EBITDA(TTM)_GSD
from windget import getEbItDa2TtM2


# 获取投入资本回报率(TTM)_PIT时间序列
from windget import getFaRoiCTtMSeries


# 获取投入资本回报率(TTM)_PIT
from windget import getFaRoiCTtM


# 获取EBIT(TTM)_PIT时间序列
from windget import getFaEbItTtMSeries


# 获取EBIT(TTM)_PIT
from windget import getFaEbItTtM


# 获取现金净流量(TTM)_PIT时间序列
from windget import getFaCashFlowTtMSeries


# 获取现金净流量(TTM)_PIT
from windget import getFaCashFlowTtM


# 获取现金净流量(TTM)时间序列
from windget import getCashFlowTtM2Series


# 获取现金净流量(TTM)
from windget import getCashFlowTtM2


# 获取现金净流量(TTM)_GSD时间序列
from windget import getCashFlowTtM3Series


# 获取现金净流量(TTM)_GSD
from windget import getCashFlowTtM3


# 获取EBITDA(TTM)_PIT时间序列
from windget import getFaEbItDaTtMSeries


# 获取EBITDA(TTM)_PIT
from windget import getFaEbItDaTtM


# 获取市现率PCF(经营现金流TTM,加权)时间序列
from windget import getValPcfOcFtTMwGtSeries


# 获取市现率PCF(经营现金流TTM,加权)
from windget import getValPcfOcFtTMwGt


# 获取营收市值比(TTM)_PIT时间序列
from windget import getValOrToMvTtMSeries


# 获取营收市值比(TTM)_PIT
from windget import getValOrToMvTtM


# 获取销售商品提供劳务收到的现金(TTM)时间序列
from windget import getSalesCashInttM2Series


# 获取销售商品提供劳务收到的现金(TTM)
from windget import getSalesCashInttM2


# 获取股利保障倍数(TTM)_PIT时间序列
from windget import getFaDivCoverTtMSeries


# 获取股利保障倍数(TTM)_PIT
from windget import getFaDivCoverTtM


# 获取投入资本回报率ROIC(TTM)_PIT时间序列
from windget import getFaRoiCebitTtMSeries


# 获取投入资本回报率ROIC(TTM)_PIT
from windget import getFaRoiCebitTtM


# 获取销售税金率(TTM)_PIT时间序列
from windget import getFaTaxRatioTtMSeries


# 获取销售税金率(TTM)_PIT
from windget import getFaTaxRatioTtM


# 获取销售商品提供劳务收到的现金(TTM,只有最新数据)时间序列
from windget import getSalesCashInttMSeries


# 获取销售商品提供劳务收到的现金(TTM,只有最新数据)
from windget import getSalesCashInttM


# 获取扣非后每股收益(TTM)时间序列
from windget import getEpsDeductedTtMSeries


# 获取扣非后每股收益(TTM)
from windget import getEpsDeductedTtM


# 获取息税前利润(TTM反推法)_PIT时间序列
from windget import getFaEbItUnVerTtMSeries


# 获取息税前利润(TTM反推法)_PIT
from windget import getFaEbItUnVerTtM


# 获取销售商品提供劳务收到的现金(TTM)_PIT时间序列
from windget import getFaSalesCashTtMSeries


# 获取销售商品提供劳务收到的现金(TTM)_PIT
from windget import getFaSalesCashTtM


# 获取期间费用(TTM)_GSD时间序列
from windget import getPeriodExpenseTtMSeries


# 获取期间费用(TTM)_GSD
from windget import getPeriodExpenseTtM


# 获取贝里比率(TTM)_PIT时间序列
from windget import getFaBerryRatioTtMSeries


# 获取贝里比率(TTM)_PIT
from windget import getFaBerryRatioTtM


# 获取收益市值比(TTM)_PIT时间序列
from windget import getFaProfitToMvTtMSeries


# 获取收益市值比(TTM)_PIT
from windget import getFaProfitToMvTtM


# 获取期间费用(TTM)_PIT时间序列
from windget import getFaPerExpenseTtMSeries


# 获取期间费用(TTM)_PIT
from windget import getFaPerExpenseTtM


# 获取投资活动现金净流量(TTM)时间序列
from windget import getInvestCashFlowTtM2Series


# 获取投资活动现金净流量(TTM)
from windget import getInvestCashFlowTtM2


# 获取投资活动现金净流量(TTM)_GSD时间序列
from windget import getInvestCashFlowTtM3Series


# 获取投资活动现金净流量(TTM)_GSD
from windget import getInvestCashFlowTtM3


# 获取EBITDA(TTM反推法)_PIT时间序列
from windget import getFaEbItDaInverTtMSeries


# 获取EBITDA(TTM反推法)_PIT
from windget import getFaEbItDaInverTtM


# 获取投资活动现金净流量(TTM,只有最新数据)时间序列
from windget import getInvestCashFlowTtMSeries


# 获取投资活动现金净流量(TTM,只有最新数据)
from windget import getInvestCashFlowTtM


# 获取经营活动现金净流量(TTM)_PIT时间序列
from windget import getFaOperaCtCashFlowTtMSeries


# 获取经营活动现金净流量(TTM)_PIT
from windget import getFaOperaCtCashFlowTtM


# 获取期间费用(TTM)时间序列
from windget import getPeriodExpenseTTtMSeries


# 获取期间费用(TTM)
from windget import getPeriodExpenseTTtM


# 获取利息费用(TTM)时间序列
from windget import getInterestExpenseTtMSeries


# 获取利息费用(TTM)
from windget import getInterestExpenseTtM


# 获取经营活动现金净流量(TTM)时间序列
from windget import getOperateCashFlowTtM2Series


# 获取经营活动现金净流量(TTM)
from windget import getOperateCashFlowTtM2


# 获取筹资活动现金净流量(TTM)时间序列
from windget import getFinanceCashFlowTtM2Series


# 获取筹资活动现金净流量(TTM)
from windget import getFinanceCashFlowTtM2


# 获取经营活动现金净流量(TTM)_GSD时间序列
from windget import getOperateCashFlowTtM3Series


# 获取经营活动现金净流量(TTM)_GSD
from windget import getOperateCashFlowTtM3


# 获取筹资活动现金净流量(TTM)_GSD时间序列
from windget import getFinanceCashFlowTtM3Series


# 获取筹资活动现金净流量(TTM)_GSD
from windget import getFinanceCashFlowTtM3


# 获取现金转换周期(TTM)_PIT时间序列
from windget import getFaCashCNvCycleTtMSeries


# 获取现金转换周期(TTM)_PIT
from windget import getFaCashCNvCycleTtM


# 获取筹资活动现金净流量(TTM,只有最新数据)时间序列
from windget import getFinanceCashFlowTtMSeries


# 获取筹资活动现金净流量(TTM,只有最新数据)
from windget import getFinanceCashFlowTtM


# 获取资金现金回收率(TTM)_PIT时间序列
from windget import getFaCashRecovRatioTtMSeries


# 获取资金现金回收率(TTM)_PIT
from windget import getFaCashRecovRatioTtM


# 获取投资活动现金净流量(TTM)_PIT时间序列
from windget import getFaInveActCashFlowTtMSeries


# 获取投资活动现金净流量(TTM)_PIT
from windget import getFaInveActCashFlowTtM


# 获取筹资活动现金净流量(TTM)_PIT时间序列
from windget import getFaFinaActCashFlowTtMSeries


# 获取筹资活动现金净流量(TTM)_PIT
from windget import getFaFinaActCashFlowTtM


# 获取每股EBITDA时间序列
from windget import getEbItDapSSeries


# 获取每股EBITDA
from windget import getEbItDapS


# 获取已获利息倍数(EBIT/利息费用)时间序列
from windget import getEbItToInterestSeries


# 获取已获利息倍数(EBIT/利息费用)
from windget import getEbItToInterest


# 获取EBITDA/利息费用时间序列
from windget import getEbItDatoInterestSeries


# 获取EBITDA/利息费用
from windget import getEbItDatoInterest


# 获取EBIT(反推法)时间序列
from windget import getEbItSeries


# 获取EBIT(反推法)
from windget import getEbIt


# 获取EBITDA(反推法)时间序列
from windget import getEbItDaSeries


# 获取EBITDA(反推法)
from windget import getEbItDa


# 获取EBIT时间序列
from windget import getEbIt2Series


# 获取EBIT
from windget import getEbIt2


# 获取EBITDA时间序列
from windget import getEbItDa2Series


# 获取EBITDA
from windget import getEbItDa2


# 获取EBITDA(公布值)_GSD时间序列
from windget import getIsEbItDaArdSeries


# 获取EBITDA(公布值)_GSD
from windget import getIsEbItDaArd


# 获取利息保障倍数_PIT时间序列
from windget import getFaEbItToInterestSeries


# 获取利息保障倍数_PIT
from windget import getFaEbItToInterest


# 获取全部债务/EBITDA时间序列
from windget import getTlToeBitDaSeries


# 获取全部债务/EBITDA
from windget import getTlToeBitDa


# 获取已获利息倍数(EBIT/利息费用)_GSD时间序列
from windget import getWgsDEbItToInterestSeries


# 获取已获利息倍数(EBIT/利息费用)_GSD
from windget import getWgsDEbItToInterest


# 获取息税前利润_GSD时间序列
from windget import getWgsDEbIt3Series


# 获取息税前利润_GSD
from windget import getWgsDEbIt3


# 获取息税折旧摊销前利润_GSD时间序列
from windget import getWgsDEbItDa2Series


# 获取息税折旧摊销前利润_GSD
from windget import getWgsDEbItDa2


# 获取EBIT(反推法)_GSD时间序列
from windget import getWgsDEbItSeries


# 获取EBIT(反推法)_GSD
from windget import getWgsDEbIt


# 获取EBITDA(反推法)_GSD时间序列
from windget import getWgsDEbItDaSeries


# 获取EBITDA(反推法)_GSD
from windget import getWgsDEbItDa


# 获取企业倍数(EV2/EBITDA)时间序列
from windget import getEv2ToEbItDaSeries


# 获取企业倍数(EV2/EBITDA)
from windget import getEv2ToEbItDa


# 获取预测息税前利润(EBIT)平均值时间序列
from windget import getEstAvGebItSeries


# 获取预测息税前利润(EBIT)平均值
from windget import getEstAvGebIt


# 获取预测息税前利润(EBIT)最大值时间序列
from windget import getEstMaxEbItSeries


# 获取预测息税前利润(EBIT)最大值
from windget import getEstMaxEbIt


# 获取预测息税前利润(EBIT)最小值时间序列
from windget import getEstMineBitSeries


# 获取预测息税前利润(EBIT)最小值
from windget import getEstMineBit


# 获取预测息税前利润(EBIT)标准差时间序列
from windget import getEstStDebitSeries


# 获取预测息税前利润(EBIT)标准差
from windget import getEstStDebit


# 获取预测息税折旧摊销前利润(EBITDA)平均值时间序列
from windget import getEstAvGebItDaSeries


# 获取预测息税折旧摊销前利润(EBITDA)平均值
from windget import getEstAvGebItDa


# 获取预测息税折旧摊销前利润(EBITDA)最大值时间序列
from windget import getEstMaxEbItDaSeries


# 获取预测息税折旧摊销前利润(EBITDA)最大值
from windget import getEstMaxEbItDa


# 获取预测息税折旧摊销前利润(EBITDA)最小值时间序列
from windget import getEstMineBitDaSeries


# 获取预测息税折旧摊销前利润(EBITDA)最小值
from windget import getEstMineBitDa


# 获取预测息税折旧摊销前利润(EBITDA)标准差时间序列
from windget import getEstStDebitDaSeries


# 获取预测息税折旧摊销前利润(EBITDA)标准差
from windget import getEstStDebitDa


# 获取预测息税前利润(EBIT)平均值(币种转换)时间序列
from windget import getEstAvGebIt1Series


# 获取预测息税前利润(EBIT)平均值(币种转换)
from windget import getEstAvGebIt1


# 获取预测息税前利润(EBIT)最大值(币种转换)时间序列
from windget import getEstMaxEbIt1Series


# 获取预测息税前利润(EBIT)最大值(币种转换)
from windget import getEstMaxEbIt1


# 获取预测息税前利润(EBIT)最小值(币种转换)时间序列
from windget import getEstMineBit1Series


# 获取预测息税前利润(EBIT)最小值(币种转换)
from windget import getEstMineBit1


# 获取预测息税前利润(EBIT)标准差(币种转换)时间序列
from windget import getEstStDebit1Series


# 获取预测息税前利润(EBIT)标准差(币种转换)
from windget import getEstStDebit1


# 获取预测息税折旧摊销前利润(EBITDA)平均值(币种转换)时间序列
from windget import getEstAvGebItDa1Series


# 获取预测息税折旧摊销前利润(EBITDA)平均值(币种转换)
from windget import getEstAvGebItDa1


# 获取预测息税折旧摊销前利润(EBITDA)最大值(币种转换)时间序列
from windget import getEstMaxEbItDa1Series


# 获取预测息税折旧摊销前利润(EBITDA)最大值(币种转换)
from windget import getEstMaxEbItDa1


# 获取预测息税折旧摊销前利润(EBITDA)最小值(币种转换)时间序列
from windget import getEstMineBitDa1Series


# 获取预测息税折旧摊销前利润(EBITDA)最小值(币种转换)
from windget import getEstMineBitDa1


# 获取预测息税折旧摊销前利润(EBITDA)标准差(币种转换)时间序列
from windget import getEstStDebitDa1Series


# 获取预测息税折旧摊销前利润(EBITDA)标准差(币种转换)
from windget import getEstStDebitDa1


# 获取企业倍数2(EV2/EBITDA)时间序列
from windget import getValEvToeBitDa2Series


# 获取企业倍数2(EV2/EBITDA)
from windget import getValEvToeBitDa2


# 获取一致预测息税前利润(FY1)时间序列
from windget import getWestAvGebItFy1Series


# 获取一致预测息税前利润(FY1)
from windget import getWestAvGebItFy1


# 获取一致预测息税前利润(FY2)时间序列
from windget import getWestAvGebItFy2Series


# 获取一致预测息税前利润(FY2)
from windget import getWestAvGebItFy2


# 获取一致预测息税前利润(FY3)时间序列
from windget import getWestAvGebItFy3Series


# 获取一致预测息税前利润(FY3)
from windget import getWestAvGebItFy3


# 获取一致预测息税折旧摊销前利润(FY1)时间序列
from windget import getWestAvGebItDaFy1Series


# 获取一致预测息税折旧摊销前利润(FY1)
from windget import getWestAvGebItDaFy1


# 获取一致预测息税折旧摊销前利润(FY2)时间序列
from windget import getWestAvGebItDaFy2Series


# 获取一致预测息税折旧摊销前利润(FY2)
from windget import getWestAvGebItDaFy2


# 获取一致预测息税折旧摊销前利润(FY3)时间序列
from windget import getWestAvGebItDaFy3Series


# 获取一致预测息税折旧摊销前利润(FY3)
from windget import getWestAvGebItDaFy3


# 获取预测息税前利润(EBIT)平均值(可选类型)时间序列
from windget import getWestAvGebItSeries


# 获取预测息税前利润(EBIT)平均值(可选类型)
from windget import getWestAvGebIt


# 获取预测息税前利润(EBIT)最大值(可选类型)时间序列
from windget import getWestMaxEbItSeries


# 获取预测息税前利润(EBIT)最大值(可选类型)
from windget import getWestMaxEbIt


# 获取预测息税前利润(EBIT)最小值(可选类型)时间序列
from windget import getWestMineBitSeries


# 获取预测息税前利润(EBIT)最小值(可选类型)
from windget import getWestMineBit


# 获取预测息税前利润(EBIT)标准差(可选类型)时间序列
from windget import getWestStDebitSeries


# 获取预测息税前利润(EBIT)标准差(可选类型)
from windget import getWestStDebit


# 获取预测息税折旧摊销前利润(EBITDA)平均值(可选类型)时间序列
from windget import getWestAvGebItDaSeries


# 获取预测息税折旧摊销前利润(EBITDA)平均值(可选类型)
from windget import getWestAvGebItDa


# 获取预测息税折旧摊销前利润(EBITDA)最大值(可选类型)时间序列
from windget import getWestMaxEbItDaSeries


# 获取预测息税折旧摊销前利润(EBITDA)最大值(可选类型)
from windget import getWestMaxEbItDa


# 获取预测息税折旧摊销前利润(EBITDA)最小值(可选类型)时间序列
from windget import getWestMineBitDaSeries


# 获取预测息税折旧摊销前利润(EBITDA)最小值(可选类型)
from windget import getWestMineBitDa


# 获取预测息税折旧摊销前利润(EBITDA)标准差(可选类型)时间序列
from windget import getWestStDebitDaSeries


# 获取预测息税折旧摊销前利润(EBITDA)标准差(可选类型)
from windget import getWestStDebitDa


# 获取预测息税前利润(EBIT)平均值(可选类型,币种转换)时间序列
from windget import getWestAvGebIt1Series


# 获取预测息税前利润(EBIT)平均值(可选类型,币种转换)
from windget import getWestAvGebIt1


# 获取预测息税前利润(EBIT)最大值(可选类型,币种转换)时间序列
from windget import getWestMaxEbIt1Series


# 获取预测息税前利润(EBIT)最大值(可选类型,币种转换)
from windget import getWestMaxEbIt1


# 获取预测息税前利润(EBIT)最小值(可选类型,币种转换)时间序列
from windget import getWestMineBit1Series


# 获取预测息税前利润(EBIT)最小值(可选类型,币种转换)
from windget import getWestMineBit1


# 获取预测息税前利润(EBIT)标准差(可选类型,币种转换)时间序列
from windget import getWestStDebit1Series


# 获取预测息税前利润(EBIT)标准差(可选类型,币种转换)
from windget import getWestStDebit1


# 获取预测息税折旧摊销前利润(EBITDA)平均值(可选类型,币种转换)时间序列
from windget import getWestAvGebItDa1Series


# 获取预测息税折旧摊销前利润(EBITDA)平均值(可选类型,币种转换)
from windget import getWestAvGebItDa1


# 获取预测息税折旧摊销前利润(EBITDA)最大值(可选类型,币种转换)时间序列
from windget import getWestMaxEbItDa1Series


# 获取预测息税折旧摊销前利润(EBITDA)最大值(可选类型,币种转换)
from windget import getWestMaxEbItDa1


# 获取预测息税折旧摊销前利润(EBITDA)最小值(可选类型,币种转换)时间序列
from windget import getWestMineBitDa1Series


# 获取预测息税折旧摊销前利润(EBITDA)最小值(可选类型,币种转换)
from windget import getWestMineBitDa1


# 获取预测息税折旧摊销前利润(EBITDA)标准差(可选类型,币种转换)时间序列
from windget import getWestStDebitDa1Series


# 获取预测息税折旧摊销前利润(EBITDA)标准差(可选类型,币种转换)
from windget import getWestStDebitDa1


# 获取预测息税前利润(EBIT)中值时间序列
from windget import getEstMedianEbItSeries


# 获取预测息税前利润(EBIT)中值
from windget import getEstMedianEbIt


# 获取预测息税折旧摊销前利润(EBITDA)中值时间序列
from windget import getEstMedianEbItDaSeries


# 获取预测息税折旧摊销前利润(EBITDA)中值
from windget import getEstMedianEbItDa


# 获取预测息税前利润(EBIT)中值(币种转换)时间序列
from windget import getEstMedianEbIt1Series


# 获取预测息税前利润(EBIT)中值(币种转换)
from windget import getEstMedianEbIt1


# 获取预测息税折旧摊销前利润(EBITDA)中值(币种转换)时间序列
from windget import getEstMedianEbItDa1Series


# 获取预测息税折旧摊销前利润(EBITDA)中值(币种转换)
from windget import getEstMedianEbItDa1


# 获取预测息税前利润(EBIT)中值(可选类型)时间序列
from windget import getWestMedianEbItSeries


# 获取预测息税前利润(EBIT)中值(可选类型)
from windget import getWestMedianEbIt


# 获取预测息税折旧摊销前利润(EBITDA)中值(可选类型)时间序列
from windget import getWestMedianEbItDaSeries


# 获取预测息税折旧摊销前利润(EBITDA)中值(可选类型)
from windget import getWestMedianEbItDa


# 获取预测息税前利润(EBIT)中值(可选类型,币种转换)时间序列
from windget import getWestMedianEbIt1Series


# 获取预测息税前利润(EBIT)中值(可选类型,币种转换)
from windget import getWestMedianEbIt1


# 获取预测息税折旧摊销前利润(EBITDA)中值(可选类型,币种转换)时间序列
from windget import getWestMedianEbItDa1Series


# 获取预测息税折旧摊销前利润(EBITDA)中值(可选类型,币种转换)
from windget import getWestMedianEbItDa1


# 获取梅斯线_PIT时间序列
from windget import getTechMassSeries


# 获取梅斯线_PIT
from windget import getTechMass


# 获取对数市值_PIT时间序列
from windget import getValLnMvSeries


# 获取对数市值_PIT
from windget import getValLnMv


# 获取每股股利_PIT时间序列
from windget import getFaDpsSeries


# 获取每股股利_PIT
from windget import getFaDps


# 获取账面杠杆_PIT时间序列
from windget import getFaBLevSeries


# 获取账面杠杆_PIT
from windget import getFaBLev


# 获取市场杠杆_PIT时间序列
from windget import getFaMLevSeries


# 获取市场杠杆_PIT
from windget import getFaMLev


# 获取股东权益_PIT时间序列
from windget import getFaToTEquitySeries


# 获取股东权益_PIT
from windget import getFaToTEquity


# 获取股价偏度_PIT时间序列
from windget import getTechSkewNessSeries


# 获取股价偏度_PIT
from windget import getTechSkewNess


# 获取下跌波动_PIT时间序列
from windget import getTechDDnsRSeries


# 获取下跌波动_PIT
from windget import getTechDDnsR


# 获取多空指数_PIT时间序列
from windget import getTechBbiSeries


# 获取多空指数_PIT
from windget import getTechBbi


# 获取多头力道_PIT时间序列
from windget import getTechBullPowerSeries


# 获取多头力道_PIT
from windget import getTechBullPower


# 获取空头力道_PIT时间序列
from windget import getTechBearPowerSeries


# 获取空头力道_PIT
from windget import getTechBearPower


# 获取佳庆指标_PIT时间序列
from windget import getTechCHaikInSeries


# 获取佳庆指标_PIT
from windget import getTechCHaikIn


# 获取阿隆指标_PIT时间序列
from windget import getTechAroOnSeries


# 获取阿隆指标_PIT
from windget import getTechAroOn


# 获取估波指标_PIT时间序列
from windget import getTechCoppockCurveSeries


# 获取估波指标_PIT
from windget import getTechCoppockCurve


# 获取终极指标_PIT时间序列
from windget import getTechUOsSeries


# 获取终极指标_PIT
from windget import getTechUOs


# 获取折旧和摊销_PIT时间序列
from windget import getFaDaSeries


# 获取折旧和摊销_PIT
from windget import getFaDa


# 获取5日乖离率_PIT时间序列
from windget import getTechBias5Series


# 获取5日乖离率_PIT
from windget import getTechBias5


# 获取能量潮指标_PIT时间序列
from windget import getTechObVSeries


# 获取能量潮指标_PIT
from windget import getTechObV


# 获取心理线指标_PIT时间序列
from windget import getTechPsySeries


# 获取心理线指标_PIT
from windget import getTechPsy


# 获取累积/派发线_PIT时间序列
from windget import getTechAdSeries


# 获取累积/派发线_PIT
from windget import getTechAd


# 获取均线价格比_PIT时间序列
from windget import getTechMa10CloseSeries


# 获取均线价格比_PIT
from windget import getTechMa10Close


# 获取波幅中位数_PIT时间序列
from windget import getTechDHiloSeries


# 获取波幅中位数_PIT
from windget import getTechDHilo


# 获取加权市净率_PIT时间序列
from windget import getValPbWGtSeries


# 获取加权市净率_PIT
from windget import getValPbWGt


# 获取对数市值立方_PIT时间序列
from windget import getValNlSizeSeries


# 获取对数市值立方_PIT
from windget import getValNlSize


# 获取现金流市值比_PIT时间序列
from windget import getFaCTopSeries


# 获取现金流市值比_PIT
from windget import getFaCTop


# 获取息前税后利润_PIT时间序列
from windget import getFaEbIAtSeries


# 获取息前税后利润_PIT
from windget import getFaEbIAt


# 获取6日变动速率_PIT时间序列
from windget import getTechRoc6Series


# 获取6日变动速率_PIT
from windget import getTechRoc6


# 获取下轨线(布林线)_PIT时间序列
from windget import getTechBollDownSeries


# 获取下轨线(布林线)_PIT
from windget import getTechBollDown


# 获取上轨线(布林线)_PIT时间序列
from windget import getTechBollUpSeries


# 获取上轨线(布林线)_PIT
from windget import getTechBollUp


# 获取10日乖离率_PIT时间序列
from windget import getTechBias10Series


# 获取10日乖离率_PIT
from windget import getTechBias10


# 获取20日乖离率_PIT时间序列
from windget import getTechBias20Series


# 获取20日乖离率_PIT
from windget import getTechBias20


# 获取60日乖离率_PIT时间序列
from windget import getTechBias60Series


# 获取60日乖离率_PIT
from windget import getTechBias60


# 获取5日顺势指标_PIT时间序列
from windget import getTechCci5Series


# 获取5日顺势指标_PIT
from windget import getTechCci5


# 获取相对离散指数_PIT时间序列
from windget import getTechRviSeries


# 获取相对离散指数_PIT
from windget import getTechRvi


# 获取相对强弱指标_PIT时间序列
from windget import getTechRsiSeries


# 获取相对强弱指标_PIT
from windget import getTechRsi


# 获取资金流量指标_PIT时间序列
from windget import getTechMfiSeries


# 获取资金流量指标_PIT
from windget import getTechMfi


# 获取AR人气指标_PIT时间序列
from windget import getTechArSeries


# 获取AR人气指标_PIT
from windget import getTechAr


# 获取CR能量指标_PIT时间序列
from windget import getTechCr20Series


# 获取CR能量指标_PIT
from windget import getTechCr20


# 获取市场能量指标_PIT时间序列
from windget import getTechCyFSeries


# 获取市场能量指标_PIT
from windget import getTechCyF


# 获取市场强弱指标_PIT时间序列
from windget import getTechCrySeries


# 获取市场强弱指标_PIT
from windget import getTechCry


# 获取艾达透视指标_PIT时间序列
from windget import getTechElderSeries


# 获取艾达透视指标_PIT
from windget import getTechElder


# 获取6日均幅指标_PIT时间序列
from windget import getTechATr6Series


# 获取6日均幅指标_PIT
from windget import getTechATr6


# 获取5日移动均线_PIT时间序列
from windget import getTechMa5Series


# 获取5日移动均线_PIT
from windget import getTechMa5


# 获取佳庆离散指标_PIT时间序列
from windget import getTechCHaikInvolSeries


# 获取佳庆离散指标_PIT
from windget import getTechCHaikInvol


# 获取Ulcer5_PIT时间序列
from windget import getTechUlcer5Series


# 获取Ulcer5_PIT
from windget import getTechUlcer5


# 获取阶段强势指标_PIT时间序列
from windget import getTechJdQs20Series


# 获取阶段强势指标_PIT
from windget import getTechJdQs20


# 获取阿隆向上指标_PIT时间序列
from windget import getTechAroOnUpSeries


# 获取阿隆向上指标_PIT
from windget import getTechAroOnUp


# 获取阿隆向下指标_PIT时间序列
from windget import getTechAroOnDownSeries


# 获取阿隆向下指标_PIT
from windget import getTechAroOnDown


# 获取20日收益方差_PIT时间序列
from windget import getRiskVariance20Series


# 获取20日收益方差_PIT
from windget import getRiskVariance20


# 获取60日收益方差_PIT时间序列
from windget import getRiskVariance60Series


# 获取60日收益方差_PIT
from windget import getRiskVariance60


# 获取20日损失方差_PIT时间序列
from windget import getRiskLossVariance20Series


# 获取20日损失方差_PIT
from windget import getRiskLossVariance20


# 获取60日损失方差_PIT时间序列
from windget import getRiskLossVariance60Series


# 获取60日损失方差_PIT
from windget import getRiskLossVariance60


# 获取12月累计收益_PIT时间序列
from windget import getRiskCumReturn12MSeries


# 获取12月累计收益_PIT
from windget import getRiskCumReturn12M


# 获取20日变动速率_PIT时间序列
from windget import getTechRoc20Series


# 获取20日变动速率_PIT
from windget import getTechRoc20


# 获取异同离差乖离率_PIT时间序列
from windget import getTechDBcdSeries


# 获取异同离差乖离率_PIT
from windget import getTechDBcd


# 获取10日顺势指标_PIT时间序列
from windget import getTechCci10Series


# 获取10日顺势指标_PIT
from windget import getTechCci10


# 获取20日顺势指标_PIT时间序列
from windget import getTechCci20Series


# 获取20日顺势指标_PIT
from windget import getTechCci20


# 获取88日顺势指标_PIT时间序列
from windget import getTechCci88Series


# 获取88日顺势指标_PIT
from windget import getTechCci88


# 获取收益相对金额比_PIT时间序列
from windget import getTechIlLiquiditySeries


# 获取收益相对金额比_PIT
from windget import getTechIlLiquidity


# 获取动态买卖气指标_PIT时间序列
from windget import getTechADtmSeries


# 获取动态买卖气指标_PIT
from windget import getTechADtm


# 获取6日能量潮指标_PIT时间序列
from windget import getTechObV6Series


# 获取6日能量潮指标_PIT
from windget import getTechObV6


# 获取20日资金流量_PIT时间序列
from windget import getTechMoneyFlow20Series


# 获取20日资金流量_PIT
from windget import getTechMoneyFlow20


# 获取12月相对强势_PIT时间序列
from windget import getTechRStr12Series


# 获取12月相对强势_PIT
from windget import getTechRStr12


# 获取24月相对强势_PIT时间序列
from windget import getTechRStr24Series


# 获取24月相对强势_PIT
from windget import getTechRStr24


# 获取14日均幅指标_PIT时间序列
from windget import getTechATr14Series


# 获取14日均幅指标_PIT
from windget import getTechATr14


# 获取10日移动均线_PIT时间序列
from windget import getTechMa10Series


# 获取10日移动均线_PIT
from windget import getTechMa10


# 获取20日移动均线_PIT时间序列
from windget import getTechMa20Series


# 获取20日移动均线_PIT
from windget import getTechMa20


# 获取60日移动均线_PIT时间序列
from windget import getTechMa60Series


# 获取60日移动均线_PIT
from windget import getTechMa60


# 获取Ulcer10_PIT时间序列
from windget import getTechUlcer10Series


# 获取Ulcer10_PIT
from windget import getTechUlcer10


# 获取市盈率PE(TTM)_PIT时间序列
from windget import getPeTtMSeries


# 获取市盈率PE(TTM)_PIT
from windget import getPeTtM


# 获取市销率PS(TTM)_PIT时间序列
from windget import getPsTtMSeries


# 获取市销率PS(TTM)_PIT
from windget import getPsTtM


# 获取股息率(近12个月)_PIT时间序列
from windget import getDividendYield2Series


# 获取股息率(近12个月)_PIT
from windget import getDividendYield2


# 获取120日收益方差_PIT时间序列
from windget import getRiskVariance120Series


# 获取120日收益方差_PIT
from windget import getRiskVariance120


# 获取20日正收益方差_PIT时间序列
from windget import getRiskGainVariance20Series


# 获取20日正收益方差_PIT
from windget import getRiskGainVariance20


# 获取60日正收益方差_PIT时间序列
from windget import getRiskGainVariance60Series


# 获取60日正收益方差_PIT
from windget import getRiskGainVariance60


# 获取120日损失方差_PIT时间序列
from windget import getRiskLossVariance120Series


# 获取120日损失方差_PIT
from windget import getRiskLossVariance120


# 获取钱德动量摆动指标_PIT时间序列
from windget import getTechCmOSeries


# 获取钱德动量摆动指标_PIT
from windget import getTechCmO


# 获取随机指标KDJ_K_PIT时间序列
from windget import getTechKDjKSeries


# 获取随机指标KDJ_K_PIT
from windget import getTechKDjK


# 获取随机指标KDJ_D_PIT时间序列
from windget import getTechKDjDSeries


# 获取随机指标KDJ_D_PIT
from windget import getTechKDjD


# 获取随机指标KDJ_J_PIT时间序列
from windget import getTechKDjJSeries


# 获取随机指标KDJ_J_PIT
from windget import getTechKDjJ


# 获取20日能量潮指标_PIT时间序列
from windget import getTechObV20Series


# 获取20日能量潮指标_PIT
from windget import getTechObV20


# 获取市场促进指数指标_PIT时间序列
from windget import getTechMktFacIInDSeries


# 获取市场促进指数指标_PIT
from windget import getTechMktFacIInD


# 获取12日变化率指数_PIT时间序列
from windget import getTechRc12Series


# 获取12日变化率指数_PIT
from windget import getTechRc12


# 获取24日变化率指数_PIT时间序列
from windget import getTechRc24Series


# 获取24日变化率指数_PIT
from windget import getTechRc24


# 获取6日收集派发指标_PIT时间序列
from windget import getTechAd6Series


# 获取6日收集派发指标_PIT
from windget import getTechAd6


# 获取6日简易波动指标_PIT时间序列
from windget import getTechEmV6Series


# 获取6日简易波动指标_PIT
from windget import getTechEmV6


# 获取120日移动均线_PIT时间序列
from windget import getTechMa120Series


# 获取120日移动均线_PIT
from windget import getTechMa120


# 获取5日指数移动均线_PIT时间序列
from windget import getTechEma5Series


# 获取5日指数移动均线_PIT
from windget import getTechEma5


# 获取方向标准离差指数_PIT时间序列
from windget import getTechDDiSeries


# 获取方向标准离差指数_PIT
from windget import getTechDDi


# 获取绝对偏差移动平均_PIT时间序列
from windget import getTechAPbMaSeries


# 获取绝对偏差移动平均_PIT
from windget import getTechAPbMa


# 获取累计振动升降指标_PIT时间序列
from windget import getTechAsISeries


# 获取累计振动升降指标_PIT
from windget import getTechAsI


# 获取市值/企业自由现金流_PIT时间序列
from windget import getValMvTOfCffSeries


# 获取市值/企业自由现金流_PIT
from windget import getValMvTOfCff


# 获取120日正收益方差_PIT时间序列
from windget import getRiskGainVariance120Series


# 获取120日正收益方差_PIT
from windget import getRiskGainVariance120


# 获取5年平均权益回报率_PIT时间序列
from windget import getFaRoeAvg5YSeries


# 获取5年平均权益回报率_PIT
from windget import getFaRoeAvg5Y


# 获取过去5日的价格动量_PIT时间序列
from windget import getTechRevs5Series


# 获取过去5日的价格动量_PIT
from windget import getTechRevs5


# 获取过去1年的价格动量_PIT时间序列
from windget import getTechRevs250Series


# 获取过去1年的价格动量_PIT
from windget import getTechRevs250


# 获取过去3年的价格动量_PIT时间序列
from windget import getTechRevs750Series


# 获取过去3年的价格动量_PIT
from windget import getTechRevs750


# 获取6日量变动速率指标_PIT时间序列
from windget import getTechVRoc6Series


# 获取6日量变动速率指标_PIT
from windget import getTechVRoc6


# 获取20日收集派发指标_PIT时间序列
from windget import getTechAd20Series


# 获取20日收集派发指标_PIT
from windget import getTechAd20


# 获取14日简易波动指标_PIT时间序列
from windget import getTechEmV14Series


# 获取14日简易波动指标_PIT
from windget import getTechEmV14


# 获取10日指数移动均线_PIT时间序列
from windget import getTechEma10Series


# 获取10日指数移动均线_PIT
from windget import getTechEma10


# 获取12日指数移动均线_PIT时间序列
from windget import getTechEma12Series


# 获取12日指数移动均线_PIT
from windget import getTechEma12


# 获取20日指数移动均线_PIT时间序列
from windget import getTechEma20Series


# 获取20日指数移动均线_PIT
from windget import getTechEma20


# 获取26日指数移动均线_PIT时间序列
from windget import getTechEma26Series


# 获取26日指数移动均线_PIT
from windget import getTechEma26


# 获取60日指数移动均线_PIT时间序列
from windget import getTechEma60Series


# 获取60日指数移动均线_PIT
from windget import getTechEma60


# 获取平滑异同移动平均线_PIT时间序列
from windget import getTechMacDSeries


# 获取平滑异同移动平均线_PIT
from windget import getTechMacD


# 获取算术平均滚动市盈率_PIT时间序列
from windget import getValPeAvgSeries


# 获取算术平均滚动市盈率_PIT
from windget import getValPeAvg


# 获取每股收益EPS(TTM)_PIT时间序列
from windget import getEpsTtMSeries


# 获取每股收益EPS(TTM)_PIT
from windget import getEpsTtM


# 获取市盈率PE行业相对值_PIT时间序列
from windget import getValPeInDuSwSeries


# 获取市盈率PE行业相对值_PIT
from windget import getValPeInDuSw


# 获取市净率PB行业相对值_PIT时间序列
from windget import getValPbInDuSwSeries


# 获取市净率PB行业相对值_PIT
from windget import getValPbInDuSw


# 获取市销率PS行业相对值_PIT时间序列
from windget import getValPsInDuSwSeries


# 获取市销率PS行业相对值_PIT
from windget import getValPsInDuSw


# 获取账面市值比行业相对值_PIT时间序列
from windget import getValBTopInDuSwSeries


# 获取账面市值比行业相对值_PIT
from windget import getValBTopInDuSw


# 获取20日收益损失方差比_PIT时间序列
from windget import getRiskGlVarianceRatio20Series


# 获取20日收益损失方差比_PIT
from windget import getRiskGlVarianceRatio20


# 获取60日收益损失方差比_PIT时间序列
from windget import getRiskGlVarianceRatio60Series


# 获取60日收益损失方差比_PIT
from windget import getRiskGlVarianceRatio60


# 获取个股收益的20日峰度_PIT时间序列
from windget import getRiskKurtOsIs20Series


# 获取个股收益的20日峰度_PIT
from windget import getRiskKurtOsIs20


# 获取个股收益的60日峰度_PIT时间序列
from windget import getRiskKurtOsIs60Series


# 获取个股收益的60日峰度_PIT
from windget import getRiskKurtOsIs60


# 获取过去10日的价格动量_PIT时间序列
from windget import getTechRevs10Series


# 获取过去10日的价格动量_PIT
from windget import getTechRevs10


# 获取过去20日的价格动量_PIT时间序列
from windget import getTechRevs20Series


# 获取过去20日的价格动量_PIT
from windget import getTechRevs20


# 获取过去3个月的价格动量_PIT时间序列
from windget import getTechRevs60Series


# 获取过去3个月的价格动量_PIT
from windget import getTechRevs60


# 获取过去6个月的价格动量_PIT时间序列
from windget import getTechRevs120Series


# 获取过去6个月的价格动量_PIT
from windget import getTechRevs120


# 获取CMO的中间因子SD_PIT时间序列
from windget import getTechChAndesDSeries


# 获取CMO的中间因子SD_PIT
from windget import getTechChAndesD


# 获取CMO的中间因子SU_PIT时间序列
from windget import getTechChanDesuSeries


# 获取CMO的中间因子SU_PIT
from windget import getTechChanDesu


# 获取6日成交金额的标准差_PIT时间序列
from windget import getTechTvsTd6Series


# 获取6日成交金额的标准差_PIT
from windget import getTechTvsTd6


# 获取12日量变动速率指标_PIT时间序列
from windget import getTechVRoc12Series


# 获取12日量变动速率指标_PIT
from windget import getTechVRoc12


# 获取120日指数移动均线_PIT时间序列
from windget import getTechEma120Series


# 获取120日指数移动均线_PIT
from windget import getTechEma120


# 获取市现率PCF行业相对值_PIT时间序列
from windget import getValPcfInDuSwSeries


# 获取市现率PCF行业相对值_PIT
from windget import getValPcfInDuSw


# 获取120日收益损失方差比_PIT时间序列
from windget import getRiskGlVarianceRatio120Series


# 获取120日收益损失方差比_PIT
from windget import getRiskGlVarianceRatio120


# 获取个股收益的120日峰度_PIT时间序列
from windget import getRiskKurtOsIs120Series


# 获取个股收益的120日峰度_PIT
from windget import getRiskKurtOsIs120


# 获取归属于母公司的股东权益_PIT时间序列
from windget import getFaEquitySeries


# 获取归属于母公司的股东权益_PIT
from windget import getFaEquity


# 获取过去5日收益率/行业均值_PIT时间序列
from windget import getTechRevs5InDu1Series


# 获取过去5日收益率/行业均值_PIT
from windget import getTechRevs5InDu1


# 获取20日成交金额的标准差_PIT时间序列
from windget import getTechTvsTd20Series


# 获取20日成交金额的标准差_PIT
from windget import getTechTvsTd20


# 获取DDI的中间因子DIZ_PIT时间序列
from windget import getTechDizSeries


# 获取DDI的中间因子DIZ_PIT
from windget import getTechDiz


# 获取DDI的中间因子DIF_PIT时间序列
from windget import getTechDIfSeries


# 获取DDI的中间因子DIF_PIT
from windget import getTechDIf


# 获取5日三重指数移动平均线_PIT时间序列
from windget import getTechTemA5Series


# 获取5日三重指数移动平均线_PIT
from windget import getTechTemA5


# 获取过去1个月收益率/行业均值_PIT时间序列
from windget import getTechRevs20InDu1Series


# 获取过去1个月收益率/行业均值_PIT
from windget import getTechRevs20InDu1


# 获取ADTM的中间因子SBM_PIT时间序列
from windget import getTechSBmSeries


# 获取ADTM的中间因子SBM_PIT
from windget import getTechSBm


# 获取ADTM的中间因子STM_PIT时间序列
from windget import getTechStmSeries


# 获取ADTM的中间因子STM_PIT
from windget import getTechStm


# 获取6日成交金额的移动平均值_PIT时间序列
from windget import getTechTvMa6Series


# 获取6日成交金额的移动平均值_PIT
from windget import getTechTvMa6


# 获取MACD的中间因子DEA_PIT时间序列
from windget import getTechDeASeries


# 获取MACD的中间因子DEA_PIT
from windget import getTechDeA


# 获取10日三重指数移动平均线_PIT时间序列
from windget import getTechTemA10Series


# 获取10日三重指数移动平均线_PIT
from windget import getTechTemA10


# 获取所属申万一级行业的PE均值_PIT时间序列
from windget import getValAvgPeSwSeries


# 获取所属申万一级行业的PE均值_PIT
from windget import getValAvgPeSw


# 获取所属申万一级行业的PB均值_PIT时间序列
from windget import getValAvgPbSwSeries


# 获取所属申万一级行业的PB均值_PIT
from windget import getValAvgPbSw


# 获取所属申万一级行业的PS均值_PIT时间序列
from windget import getValAvGpsSwSeries


# 获取所属申万一级行业的PS均值_PIT
from windget import getValAvGpsSw


# 获取30日120日回报方差比率_PIT时间序列
from windget import getRiskRevsVarRatioSeries


# 获取30日120日回报方差比率_PIT
from windget import getRiskRevsVarRatio


# 获取20日成交金额的移动平均值_PIT时间序列
from windget import getTechTvMa20Series


# 获取20日成交金额的移动平均值_PIT
from windget import getTechTvMa20


# 获取MACD的中间因子DIFF_PIT时间序列
from windget import getTechDiffSeries


# 获取MACD的中间因子DIFF_PIT
from windget import getTechDiff


# 获取与过去52 周股价最高点差距_PIT时间序列
from windget import getTechChgMaxSeries


# 获取与过去52 周股价最高点差距_PIT
from windget import getTechChgMax


# 获取归属母公司股东的股东权益(LF)_PIT时间序列
from windget import getEquityNewSeries


# 获取归属母公司股东的股东权益(LF)_PIT
from windget import getEquityNew


# 获取市盈率PE/过去一年PE的均值_PIT时间序列
from windget import getValPeToHist250Series


# 获取市盈率PE/过去一年PE的均值_PIT
from windget import getValPeToHist250


# 获取市现率PCF(经营现金流TTM)_PIT时间序列
from windget import getPcfOCFTtMSeries


# 获取市现率PCF(经营现金流TTM)_PIT
from windget import getPcfOCFTtM


# 获取市现率PCF(现金净流量TTM)_PIT时间序列
from windget import getPcfNCfTtMSeries


# 获取市现率PCF(现金净流量TTM)_PIT
from windget import getPcfNCfTtM


# 获取所属申万一级行业的PCF均值_PIT时间序列
from windget import getValAvgPcfSwSeries


# 获取所属申万一级行业的PCF均值_PIT
from windget import getValAvgPcfSw


# 获取所属申万一级行业的PE标准差_PIT时间序列
from windget import getValStdPeSwSeries


# 获取所属申万一级行业的PE标准差_PIT
from windget import getValStdPeSw


# 获取所属申万一级行业的PB标准差_PIT时间序列
from windget import getValStdPbSwSeries


# 获取所属申万一级行业的PB标准差_PIT
from windget import getValStdPbSw


# 获取所属申万一级行业的PS标准差_PIT时间序列
from windget import getValStDpsSwSeries


# 获取所属申万一级行业的PS标准差_PIT
from windget import getValStDpsSw


# 获取一致预测每股收益(FY1)标准差_PIT时间序列
from windget import getWestStdEpsFy1Series


# 获取一致预测每股收益(FY1)标准差_PIT
from windget import getWestStdEpsFy1


# 获取过去1个月的日收益率的最大值_PIT时间序列
from windget import getTechRevs1MMaxSeries


# 获取过去1个月的日收益率的最大值_PIT
from windget import getTechRevs1MMax


# 获取当前股价/过去1个月股价均值-1_PIT时间序列
from windget import getTechPrice1MSeries


# 获取当前股价/过去1个月股价均值-1_PIT
from windget import getTechPrice1M


# 获取当前股价/过去3个月股价均值-1_PIT时间序列
from windget import getTechPrice3MSeries


# 获取当前股价/过去3个月股价均值-1_PIT
from windget import getTechPrice3M


# 获取当前股价/过去1年的股价均值-1_PIT时间序列
from windget import getTechPrice1YSeries


# 获取当前股价/过去1年的股价均值-1_PIT
from windget import getTechPrice1Y


# 获取12M收益率的120D变化率_PIT时间序列
from windget import getTechRevs12M6MSeries


# 获取12M收益率的120D变化率_PIT
from windget import getTechRevs12M6M


# 获取VMACD的中间变量VDEA_PIT时间序列
from windget import getTechVDeASeries


# 获取VMACD的中间变量VDEA_PIT
from windget import getTechVDeA


# 获取上涨的股票占指数成份股的比例_PIT时间序列
from windget import getTechUpPctSeries


# 获取上涨的股票占指数成份股的比例_PIT
from windget import getTechUpPct


# 获取下跌的股票占指数成份股的比例_PIT时间序列
from windget import getTechDownPctSeries


# 获取下跌的股票占指数成份股的比例_PIT
from windget import getTechDownPct


# 获取涨停的股票占指数成份股的比例_PIT时间序列
from windget import getTechLimitUpPctSeries


# 获取涨停的股票占指数成份股的比例_PIT
from windget import getTechLimitUpPct


# 获取跌停的股票占指数成份股的比例_PIT时间序列
from windget import getTechLimitDownPctSeries


# 获取跌停的股票占指数成份股的比例_PIT
from windget import getTechLimitDownPct


# 获取市盈率PE/过去一个月PE的均值_PIT时间序列
from windget import getValPeToHist20Series


# 获取市盈率PE/过去一个月PE的均值_PIT
from windget import getValPeToHist20


# 获取市盈率PE/过去三个月PE的均值_PIT时间序列
from windget import getValPeToHist60Series


# 获取市盈率PE/过去三个月PE的均值_PIT
from windget import getValPeToHist60


# 获取市盈率PE/过去六个月PE的均值_PIT时间序列
from windget import getValPeToHist120Series


# 获取市盈率PE/过去六个月PE的均值_PIT
from windget import getValPeToHist120


# 获取所属申万一级行业的PCF标准差_PIT时间序列
from windget import getValStdPcfSwSeries


# 获取所属申万一级行业的PCF标准差_PIT
from windget import getValStdPcfSw


# 获取VMACD的中间变量VDIFF_PIT时间序列
from windget import getTechVDiffSeries


# 获取VMACD的中间变量VDIFF_PIT
from windget import getTechVDiff


# 获取威廉变异离散量(WVAD)6日均值_PIT时间序列
from windget import getTechMawVAdSeries


# 获取威廉变异离散量(WVAD)6日均值_PIT
from windget import getTechMawVAd


# 获取市盈率PE(TTM,扣除非经常性损益)_PIT时间序列
from windget import getValPeDeductedTtMSeries


# 获取市盈率PE(TTM,扣除非经常性损益)_PIT
from windget import getValPeDeductedTtM


# 获取一致预测每股收益(FY1)变化率_1M_PIT时间序列
from windget import getWestEpsFy11MSeries


# 获取一致预测每股收益(FY1)变化率_1M_PIT
from windget import getWestEpsFy11M


# 获取一致预测每股收益(FY1)变化率_3M_PIT时间序列
from windget import getWestEpsFy13MSeries


# 获取一致预测每股收益(FY1)变化率_3M_PIT
from windget import getWestEpsFy13M


# 获取一致预测每股收益(FY1)变化率_6M_PIT时间序列
from windget import getWestEpsFy16MSeries


# 获取一致预测每股收益(FY1)变化率_6M_PIT
from windget import getWestEpsFy16M


# 获取一致预测每股收益(FY1)的变化_1M_PIT时间序列
from windget import getWestEpsFy1Chg1MSeries


# 获取一致预测每股收益(FY1)的变化_1M_PIT
from windget import getWestEpsFy1Chg1M


# 获取一致预测每股收益(FY1)的变化_3M_PIT时间序列
from windget import getWestEpsFy1Chg3MSeries


# 获取一致预测每股收益(FY1)的变化_3M_PIT
from windget import getWestEpsFy1Chg3M


# 获取一致预测每股收益(FY1)的变化_6M_PIT时间序列
from windget import getWestEpsFy1Chg6MSeries


# 获取一致预测每股收益(FY1)的变化_6M_PIT
from windget import getWestEpsFy1Chg6M


# 获取过去6个月的动量-过去1个月的动量_PIT时间序列
from windget import getTechRevs6M20Series


# 获取过去6个月的动量-过去1个月的动量_PIT
from windget import getTechRevs6M20


# 获取过去12个月的动量-过去1个月的动量_PIT时间序列
from windget import getTechRevs12M20Series


# 获取过去12个月的动量-过去1个月的动量_PIT
from windget import getTechRevs12M20


# 获取所属申万一级行业的账面市值比行业均值_PIT时间序列
from windget import getValAvgBToMvSwSeries


# 获取所属申万一级行业的账面市值比行业均值_PIT
from windget import getValAvgBToMvSw


# 获取1-过去一个月收益率排名/股票总数的比值_PIT时间序列
from windget import getTechRank1MSeries


# 获取1-过去一个月收益率排名/股票总数的比值_PIT
from windget import getTechRank1M


# 获取所属申万一级行业的账面市值比行业标准差_PIT时间序列
from windget import getValStDbToMvSwSeries


# 获取所属申万一级行业的账面市值比行业标准差_PIT
from windget import getValStDbToMvSw


# 获取过去5日的价格动量-过去1个月的价格动量_PIT时间序列
from windget import getTechRevs5M20Series


# 获取过去5日的价格动量-过去1个月的价格动量_PIT
from windget import getTechRevs5M20


# 获取过去5日的价格动量-过去3个月的价格动量_PIT时间序列
from windget import getTechRevs5M60Series


# 获取过去5日的价格动量-过去3个月的价格动量_PIT
from windget import getTechRevs5M60


# 获取过去1个月交易量/过去3个月的平均交易量_PIT时间序列
from windget import getTechVolume1M60Series


# 获取过去1个月交易量/过去3个月的平均交易量_PIT
from windget import getTechVolume1M60


# 获取与过去1 个月、3个月、6 个月、12 个月股价平均涨幅_PIT时间序列
from windget import getTechChgAvgSeries


# 获取与过去1 个月、3个月、6 个月、12 个月股价平均涨幅_PIT
from windget import getTechChgAvg


# 获取当前交易量/过去1个月日均交易量*过去一个月的收益率_PIT时间序列
from windget import getTechVolUmN1MSeries


# 获取当前交易量/过去1个月日均交易量*过去一个月的收益率_PIT
from windget import getTechVolUmN1M


# 获取第N名持有人持有份额时间序列
from windget import getFundHolderHoldingSeries


# 获取第N名持有人持有份额
from windget import getFundHolderHolding


# 获取第N名持有人持有份额(上市公告)时间序列
from windget import getFundHolderHoldingListingSeries


# 获取第N名持有人持有份额(上市公告)
from windget import getFundHolderHoldingListing


# 获取第N名持有人类别(货币)时间序列
from windget import getFundHolderNameMmFSeries


# 获取第N名持有人类别(货币)
from windget import getFundHolderNameMmF


# 获取第N名持有人持有份额(货币)时间序列
from windget import getFundHolderHoldingMmFSeries


# 获取第N名持有人持有份额(货币)
from windget import getFundHolderHoldingMmF


# 获取是否FOF基金时间序列
from windget import getFundFOfFundOrNotSeries


# 获取是否FOF基金
from windget import getFundFOfFundOrNot


# 获取Wind产品类型时间序列
from windget import getFundProdTypeWindSeries


# 获取Wind产品类型
from windget import getFundProdTypeWind


# 获取关联ETFWind代码时间序列
from windget import getFundEtFWindCodeSeries


# 获取关联ETFWind代码
from windget import getFundEtFWindCode


# 获取ETF关联联接基金代码时间序列
from windget import getFundEtFFeederCodeSeries


# 获取ETF关联联接基金代码
from windget import getFundEtFFeederCode


# 获取ETF网上现金认购起始日时间序列
from windget import getFundNetworkCashBuyStartDateSeries


# 获取ETF网上现金认购起始日
from windget import getFundNetworkCashBuyStartDate


# 获取ETF网上现金认购截止日时间序列
from windget import getFundNetworkCashBuyEnddateSeries


# 获取ETF网上现金认购截止日
from windget import getFundNetworkCashBuyEnddate


# 获取ETF网上现金认购份额下限时间序列
from windget import getFundNetworkCashBuyShareDownLimitSeries


# 获取ETF网上现金认购份额下限
from windget import getFundNetworkCashBuyShareDownLimit


# 获取ETF网上现金认购份额上限时间序列
from windget import getFundNetworkCashBuyShareUpLimitSeries


# 获取ETF网上现金认购份额上限
from windget import getFundNetworkCashBuyShareUpLimit


# 获取ETF网下现金认购起始日时间序列
from windget import getFundOffNetworkBuyStartDateSeries


# 获取ETF网下现金认购起始日
from windget import getFundOffNetworkBuyStartDate


# 获取ETF网下现金认购截止日时间序列
from windget import getFundOffNetworkBuyEnddateSeries


# 获取ETF网下现金认购截止日
from windget import getFundOffNetworkBuyEnddate


# 获取ETF网下现金认购份额下限时间序列
from windget import getFundOffNetworkCashBuyShareDownLimitSeries


# 获取ETF网下现金认购份额下限
from windget import getFundOffNetworkCashBuyShareDownLimit


# 获取ETF网下股票认购起始日时间序列
from windget import getFundOffNetworkStockBuyStartDateSeries


# 获取ETF网下股票认购起始日
from windget import getFundOffNetworkStockBuyStartDate


# 获取ETF网下股票认购截止日时间序列
from windget import getFundOffNetworkStockBuyEnddateSeries


# 获取ETF网下股票认购截止日
from windget import getFundOffNetworkStockBuyEnddate


# 获取ETF网下股票认购份额下限时间序列
from windget import getFundOffNetworkStockBuyShareDownLimitSeries


# 获取ETF网下股票认购份额下限
from windget import getFundOffNetworkStockBuyShareDownLimit


# 获取ETF申购赎回现金差额时间序列
from windget import getFundEtFPrCashBalanceSeries


# 获取ETF申购赎回现金差额
from windget import getFundEtFPrCashBalance


# 获取ETF申购赎回最小申购赎回单位时间序列
from windget import getFundEtFPrMinnaVSeries


# 获取ETF申购赎回最小申购赎回单位
from windget import getFundEtFPrMinnaV


# 获取ETF申购赎回预估现金部分时间序列
from windget import getFundEtFPrEstCashSeries


# 获取ETF申购赎回预估现金部分
from windget import getFundEtFPrEstCash


# 获取ETF申购赎回现金替代比例上限(%)时间序列
from windget import getFundEtFPrCashRatioSeries


# 获取ETF申购赎回现金替代比例上限(%)
from windget import getFundEtFPrCashRatio


# 获取ETF申赎清单申购上限时间序列
from windget import getFundEtFPrMaxPurchaseSeries


# 获取ETF申赎清单申购上限
from windget import getFundEtFPrMaxPurchase


# 获取ETF申赎清单赎回上限时间序列
from windget import getFundEtFPrMinRedemptionSeries


# 获取ETF申赎清单赎回上限
from windget import getFundEtFPrMinRedemption


# 获取银行理财风险等级(Wind)时间序列
from windget import getFundLcRiskLevelWindSeries


# 获取银行理财风险等级(Wind)
from windget import getFundLcRiskLevelWind


# 获取未交税金_FUND时间序列
from windget import getStmBs127Series


# 获取未交税金_FUND
from windget import getStmBs127


# 获取应付收益_FUND时间序列
from windget import getStmBs30Series


# 获取应付收益_FUND
from windget import getStmBs30


# 获取实收基金_FUND时间序列
from windget import getStmBs34Series


# 获取实收基金_FUND
from windget import getStmBs34


# 获取收入合计_FUND时间序列
from windget import getStmIs10Series


# 获取收入合计_FUND
from windget import getStmIs10


# 获取股利收益_FUND时间序列
from windget import getStmIs4Series


# 获取股利收益_FUND
from windget import getStmIs4


# 获取汇兑收入_FUND时间序列
from windget import getStmIs77Series


# 获取汇兑收入_FUND
from windget import getStmIs77


# 获取费用合计_FUND时间序列
from windget import getStmIs22Series


# 获取费用合计_FUND
from windget import getStmIs22


# 获取交易费用_FUND时间序列
from windget import getStmIs73Series


# 获取交易费用_FUND
from windget import getStmIs73


# 获取审计费用_FUND时间序列
from windget import getStmIs19Series


# 获取审计费用_FUND
from windget import getStmIs19


# 获取应收申购款_FUND时间序列
from windget import getStmBs14Series


# 获取应收申购款_FUND
from windget import getStmBs14


# 获取应付赎回款_FUND时间序列
from windget import getStmBs26Series


# 获取应付赎回款_FUND
from windget import getStmBs26


# 获取基金管理费_FUND时间序列
from windget import getStmIs11Series


# 获取基金管理费_FUND
from windget import getStmIs11


# 获取客户维护费_FUND时间序列
from windget import getStmIs74Series


# 获取客户维护费_FUND
from windget import getStmIs74


# 获取基金托管费_FUND时间序列
from windget import getStmIs12Series


# 获取基金托管费_FUND
from windget import getStmIs12


# 获取应付交易费用_FUND时间序列
from windget import getStmBs24Series


# 获取应付交易费用_FUND
from windget import getStmBs24


# 获取衍生工具收益_FUND时间序列
from windget import getStmIs29Series


# 获取衍生工具收益_FUND
from windget import getStmIs29


# 获取应收证券清算款_FUND时间序列
from windget import getStmBs10Series


# 获取应收证券清算款_FUND
from windget import getStmBs10


# 获取卖出回购证券款_FUND时间序列
from windget import getStmBs28Series


# 获取卖出回购证券款_FUND
from windget import getStmBs28


# 获取应付证券清算款_FUND时间序列
from windget import getStmBs22Series


# 获取应付证券清算款_FUND
from windget import getStmBs22


# 获取应付基金管理费_FUND时间序列
from windget import getStmBs20Series


# 获取应付基金管理费_FUND
from windget import getStmBs20


# 获取应付基金托管费_FUND时间序列
from windget import getStmBs21Series


# 获取应付基金托管费_FUND
from windget import getStmBs21


# 获取应付销售服务费_FUND时间序列
from windget import getStmBs153Series


# 获取应付销售服务费_FUND
from windget import getStmBs153


# 获取持有人权益合计_FUND时间序列
from windget import getStmBs38Series


# 获取持有人权益合计_FUND
from windget import getStmBs38


# 获取基金销售服务费_FUND时间序列
from windget import getStmIs16Series


# 获取基金销售服务费_FUND
from windget import getStmIs16


# 获取重仓基金Wind代码时间序列
from windget import getPrtTopFundWindCodeSeries


# 获取重仓基金Wind代码
from windget import getPrtTopFundWindCode


# 获取ETF一级市场基金代码时间序列
from windget import getIssueFirstMarketFundCodeSeries


# 获取ETF一级市场基金代码
from windget import getIssueFirstMarketFundCode


# 获取国家/地区投资市值(QDII)时间序列
from windget import getPrtQdIiCountryRegionInvestmentSeries


# 获取国家/地区投资市值(QDII)
from windget import getPrtQdIiCountryRegionInvestment


# 获取ETF网上现金发售代码时间序列
from windget import getIssueOnlineCashOfferingSymbolSeries


# 获取ETF网上现金发售代码
from windget import getIssueOnlineCashOfferingSymbol


# 获取ETF申购赎回简称时间序列
from windget import getFundPurchaseAndRedemptionAbbreviationSeries


# 获取ETF申购赎回简称
from windget import getFundPurchaseAndRedemptionAbbreviation


# 获取ETF上市交易份额时间序列
from windget import getIssueEtFDealShareOnMarketSeries


# 获取ETF上市交易份额
from windget import getIssueEtFDealShareOnMarket


# 获取Wind代码时间序列
from windget import getWindCodeSeries


# 获取Wind代码
from windget import getWindCode


# 获取指数分类(Wind)时间序列
from windget import getWindTypeSeries


# 获取指数分类(Wind)
from windget import getWindType


# 获取Wind债券一级分类时间序列
from windget import getWindL1TypeSeries


# 获取Wind债券一级分类
from windget import getWindL1Type


# 获取Wind债券二级分类时间序列
from windget import getWindL2TypeSeries


# 获取Wind债券二级分类
from windget import getWindL2Type


# 获取同公司可转债Wind代码时间序列
from windget import getCbWindCodeSeries


# 获取同公司可转债Wind代码
from windget import getCbWindCode


# 获取所属Wind行业名称时间序列
from windget import getIndustryGicSSeries


# 获取所属Wind行业名称
from windget import getIndustryGicS


# 获取所属Wind行业代码时间序列
from windget import getIndustryGicSCodeSeries


# 获取所属Wind行业代码
from windget import getIndustryGicSCode


# 获取Wind自定义代码时间序列
from windget import getPreWindCodeSeries


# 获取Wind自定义代码
from windget import getPreWindCode


# 获取同公司GDRWind代码时间序列
from windget import getGdrWindCodeSeries


# 获取同公司GDRWind代码
from windget import getGdrWindCode


# 获取证券曾用Wind代码时间序列
from windget import getPreCodeSeries


# 获取证券曾用Wind代码
from windget import getPreCode


# 获取同公司港股Wind代码时间序列
from windget import getHshAreCodeSeries


# 获取同公司港股Wind代码
from windget import getHshAreCode


# 获取同公司A股Wind代码时间序列
from windget import getAShareWindCodeSeries


# 获取同公司A股Wind代码
from windget import getAShareWindCode


# 获取同公司B股Wind代码时间序列
from windget import getBShareWindCodeSeries


# 获取同公司B股Wind代码
from windget import getBShareWindCode


# 获取同公司美股Wind代码时间序列
from windget import getUsShareWindCodeSeries


# 获取同公司美股Wind代码
from windget import getUsShareWindCode


# 获取Wind3年评级时间序列
from windget import getRatingWind3YSeries


# 获取Wind3年评级
from windget import getRatingWind3Y


# 获取Wind5年评级时间序列
from windget import getRatingWind5YSeries


# 获取Wind5年评级
from windget import getRatingWind5Y


# 获取(停止)Wind1年评级时间序列
from windget import getRatingWind1YSeries


# 获取(停止)Wind1年评级
from windget import getRatingWind1Y


# 获取(停止)Wind2年评级时间序列
from windget import getRatingWind2YSeries


# 获取(停止)Wind2年评级
from windget import getRatingWind2Y


# 获取重仓行业投资市值(Wind全球行业)时间序列
from windget import getPrtTopGicSIndustryValueSeries


# 获取重仓行业投资市值(Wind全球行业)
from windget import getPrtTopGicSIndustryValue


# 获取基础证券Wind代码时间序列
from windget import getUnderlyingWindCode2Series


# 获取基础证券Wind代码
from windget import getUnderlyingWindCode2


# 获取所属Wind行业指数代码时间序列
from windget import getIndexCodeWindSeries


# 获取所属Wind行业指数代码
from windget import getIndexCodeWind


# 获取所属Wind行业指数代码(港股)时间序列
from windget import getIndexCodeWindHkSeries


# 获取所属Wind行业指数代码(港股)
from windget import getIndexCodeWindHk


# 获取所属Wind主题行业指数代码时间序列
from windget import getIndexCodeWindThematicSeries


# 获取所属Wind主题行业指数代码
from windget import getIndexCodeWindThematic


# 获取标的Wind代码时间序列
from windget import getUnderlyingWindCodeSeries


# 获取标的Wind代码
from windget import getUnderlyingWindCode


# 获取Wind ESG评级时间序列
from windget import getEsGRatingWindSeries


# 获取Wind ESG评级
from windget import getEsGRatingWind


# 获取重仓债券Wind代码时间序列
from windget import getPrtTopBondWindCodeSeries


# 获取重仓债券Wind代码
from windget import getPrtTopBondWindCode


# 获取重仓股股票Wind代码时间序列
from windget import getPrtTopStockWindCodeSeries


# 获取重仓股股票Wind代码
from windget import getPrtTopStockWindCode


# 获取ESG管理实践得分时间序列
from windget import getEsGMGmtScoreWindSeries


# 获取ESG管理实践得分
from windget import getEsGMGmtScoreWind


# 获取ESG争议事件得分时间序列
from windget import getEsGEventScoreWindSeries


# 获取ESG争议事件得分
from windget import getEsGEventScoreWind


# 获取所属Wind主题行业名称时间序列
from windget import getThematicIndustryWindSeries


# 获取所属Wind主题行业名称
from windget import getThematicIndustryWind


# 获取重仓行业投资市值(Wind)时间序列
from windget import getPrtTopIndustryValueWindSeries


# 获取重仓行业投资市值(Wind)
from windget import getPrtTopIndustryValueWind


# 获取价格算到期收益率(BC1)时间序列
from windget import getCalcYieldSeries


# 获取价格算到期收益率(BC1)
from windget import getCalcYield


# 获取每股经营现金净流量_GSD时间序列
from windget import getWgsDOcFpsSeries


# 获取每股经营现金净流量_GSD
from windget import getWgsDOcFps


# 获取每股派息_GSD时间序列
from windget import getWgsDDpsSeries


# 获取每股派息_GSD
from windget import getWgsDDps


# 获取每股收益-最新股本摊薄_GSD时间序列
from windget import getWgsDEpsAdjust2Series


# 获取每股收益-最新股本摊薄_GSD
from windget import getWgsDEpsAdjust2


# 获取每股收益-期末股本摊薄_GSD时间序列
from windget import getWgsDEpsDiluted3Series


# 获取每股收益-期末股本摊薄_GSD
from windget import getWgsDEpsDiluted3


# 获取投入资本回报率_GSD时间序列
from windget import getWgsDRoiCSeries


# 获取投入资本回报率_GSD
from windget import getWgsDRoiC


# 获取投入资本回报率(年化)_GSD时间序列
from windget import getWgsDRoiCYearlySeries


# 获取投入资本回报率(年化)_GSD
from windget import getWgsDRoiCYearly


# 获取投入资本回报率ROIC_GSD时间序列
from windget import getWgsDRoiC1Series


# 获取投入资本回报率ROIC_GSD
from windget import getWgsDRoiC1


# 获取权益性投资_GSD时间序列
from windget import getWgsDInvestEqSeries


# 获取权益性投资_GSD
from windget import getWgsDInvestEq


# 获取可供出售投资_GSD时间序列
from windget import getWgsDInvestAFsSeries


# 获取可供出售投资_GSD
from windget import getWgsDInvestAFs


# 获取抵押担保证券_GSD时间序列
from windget import getWgsDSecCollaSeries


# 获取抵押担保证券_GSD
from windget import getWgsDSecColla


# 获取客户贷款及垫款净额_GSD时间序列
from windget import getWgsDLoansNetSeries


# 获取客户贷款及垫款净额_GSD
from windget import getWgsDLoansNet


# 获取可供出售贷款_GSD时间序列
from windget import getWgsDLoansHfSSeries


# 获取可供出售贷款_GSD
from windget import getWgsDLoansHfS


# 获取递延保单获得成本_GSD时间序列
from windget import getWgsDDefPlcYAcqCostsSeries


# 获取递延保单获得成本_GSD
from windget import getWgsDDefPlcYAcqCosts


# 获取应收再保_GSD时间序列
from windget import getWgsDRecEivReInSurSeries


# 获取应收再保_GSD
from windget import getWgsDRecEivReInSur


# 获取其它应收款_GSD时间序列
from windget import getWgsDRecEivStOThSeries


# 获取其它应收款_GSD
from windget import getWgsDRecEivStOTh


# 获取抵押贷款与票据净额_GSD时间序列
from windget import getWgsDLoansMtGNetSeries


# 获取抵押贷款与票据净额_GSD
from windget import getWgsDLoansMtGNet


# 获取应交税金_GSD时间序列
from windget import getWgsDPayTaxSeries


# 获取应交税金_GSD
from windget import getWgsDPayTax


# 获取短期借贷及长期借贷当期到期部分_GSD时间序列
from windget import getWgsDDebtStSeries


# 获取短期借贷及长期借贷当期到期部分_GSD
from windget import getWgsDDebtSt


# 获取长期借贷_GSD时间序列
from windget import getWgsDDebtLtSeries


# 获取长期借贷_GSD
from windget import getWgsDDebtLt


# 获取总存款_GSD时间序列
from windget import getWgsDDepositsSeries


# 获取总存款_GSD
from windget import getWgsDDeposits


# 获取抵押担保融资_GSD时间序列
from windget import getWgsDFinCollaSeries


# 获取抵押担保融资_GSD
from windget import getWgsDFinColla


# 获取应付再保_GSD时间序列
from windget import getWgsDPayReInSurSeries


# 获取应付再保_GSD
from windget import getWgsDPayReInSur


# 获取普通股股本_GSD时间序列
from windget import getWgsDComEqParSeries


# 获取普通股股本_GSD
from windget import getWgsDComEqPar


# 获取储备_GSD时间序列
from windget import getWgsDRsvSeries


# 获取储备_GSD
from windget import getWgsDRsv


# 获取股本溢价_GSD时间序列
from windget import getWgsDAPicSeries


# 获取股本溢价_GSD
from windget import getWgsDAPic


# 获取普通股权益总额_GSD时间序列
from windget import getWgsDComEqPahOlderSeries


# 获取普通股权益总额_GSD
from windget import getWgsDComEqPahOlder


# 获取归属母公司股东权益_GSD时间序列
from windget import getWgsDComEqSeries


# 获取归属母公司股东权益_GSD
from windget import getWgsDComEq


# 获取股东权益合计_GSD时间序列
from windget import getWgsDStKhlDrSEqSeries


# 获取股东权益合计_GSD
from windget import getWgsDStKhlDrSEq


# 获取主营收入_GSD时间序列
from windget import getWgsDSalesOperSeries


# 获取主营收入_GSD
from windget import getWgsDSalesOper


# 获取共同发展公司损益_GSD时间序列
from windget import getWgsDGainJointlyControlledSeries


# 获取共同发展公司损益_GSD
from windget import getWgsDGainJointlyControlled


# 获取员工薪酬_GSD时间序列
from windget import getWgsDEMplBenSeries


# 获取员工薪酬_GSD
from windget import getWgsDEMplBen


# 获取交易账户净收入_GSD时间序列
from windget import getWgsDTradeIncNetSeries


# 获取交易账户净收入_GSD
from windget import getWgsDTradeIncNet


# 获取利息及股息收入_GSD时间序列
from windget import getWgsDIntInverStIncSeries


# 获取利息及股息收入_GSD
from windget import getWgsDIntInverStInc


# 获取已发生赔款净额_GSD时间序列
from windget import getWgsDClaimIncurredSeries


# 获取已发生赔款净额_GSD
from windget import getWgsDClaimIncurred


# 获取毛承保保费及保单费收入_GSD时间序列
from windget import getWgsDPremiumGrossSeries


# 获取毛承保保费及保单费收入_GSD
from windget import getWgsDPremiumGross


# 获取保单持有人利益_GSD时间序列
from windget import getWgsDPolicyHlDrBenSeries


# 获取保单持有人利益_GSD
from windget import getWgsDPolicyHlDrBen


# 获取保单获取成本和承保费用_GSD时间序列
from windget import getWgsDCostPolicyAcquisitionSeries


# 获取保单获取成本和承保费用_GSD
from windget import getWgsDCostPolicyAcquisition


# 获取扣除贷款损失准备前收入_GSD时间序列
from windget import getWgsDRevComMIncSeries


# 获取扣除贷款损失准备前收入_GSD
from windget import getWgsDRevComMInc


# 获取经纪佣金收入_GSD时间序列
from windget import getWgsDBrokerComMIncSeries


# 获取经纪佣金收入_GSD
from windget import getWgsDBrokerComMInc


# 获取承销与投资银行费收入_GSD时间序列
from windget import getWgsDUwIbIncSeries


# 获取承销与投资银行费收入_GSD
from windget import getWgsDUwIbInc


# 获取租金收入_GSD时间序列
from windget import getWgsDRevRentSeries


# 获取租金收入_GSD
from windget import getWgsDRevRent


# 获取房地产销售收入_GSD时间序列
from windget import getWgsDGainSaleRealEstateSeries


# 获取房地产销售收入_GSD
from windget import getWgsDGainSaleRealEstate


# 获取抵押贷款相关收入_GSD时间序列
from windget import getWgsDMtGIncSeries


# 获取抵押贷款相关收入_GSD
from windget import getWgsDMtGInc


# 获取销售、行政及一般费用_GSD时间序列
from windget import getWgsDSgaExpSeries


# 获取销售、行政及一般费用_GSD
from windget import getWgsDSgaExp


# 获取贷款损失准备_GSD时间序列
from windget import getWgsDProvLoanLossSeries


# 获取贷款损失准备_GSD
from windget import getWgsDProvLoanLoss


# 获取手续费及佣金开支_GSD时间序列
from windget import getWgsDFeeComMExpSeries


# 获取手续费及佣金开支_GSD
from windget import getWgsDFeeComMExp


# 获取权益性投资损益_GSD时间序列
from windget import getWgsDInvestGainSeries


# 获取权益性投资损益_GSD
from windget import getWgsDInvestGain


# 获取材料及相关费用_GSD时间序列
from windget import getWgsDExpMaterialsSeries


# 获取材料及相关费用_GSD
from windget import getWgsDExpMaterials


# 获取非经常项目前利润_GSD时间序列
from windget import getWgsDEBtExClUnusualItemsSeries


# 获取非经常项目前利润_GSD
from windget import getWgsDEBtExClUnusualItems


# 获取非经常项目损益_GSD时间序列
from windget import getWgsDUnusualItemsSeries


# 获取非经常项目损益_GSD
from windget import getWgsDUnusualItems


# 获取除税前利润_GSD时间序列
from windget import getWgsDIncPreTaxSeries


# 获取除税前利润_GSD
from windget import getWgsDIncPreTax


# 获取除税后利润_GSD时间序列
from windget import getWgsDNetProfitIsSeries


# 获取除税后利润_GSD
from windget import getWgsDNetProfitIs


# 获取折旧及摊销_GSD时间序列
from windget import getWgsDDaSeries


# 获取折旧及摊销_GSD
from windget import getWgsDDa


# 获取联营公司损益_GSD时间序列
from windget import getWgsDGainAssociatesSeries


# 获取联营公司损益_GSD
from windget import getWgsDGainAssociates


# 获取折旧与摊销_GSD时间序列
from windget import getWgsDDepExpCfSeries


# 获取折旧与摊销_GSD
from windget import getWgsDDepExpCf


# 获取资本性支出_GSD时间序列
from windget import getWgsDCapeXFfSeries


# 获取资本性支出_GSD
from windget import getWgsDCapeXFf


# 获取投资增加_GSD时间序列
from windget import getWgsDInvestPUrchCfSeries


# 获取投资增加_GSD
from windget import getWgsDInvestPUrchCf


# 获取投资减少_GSD时间序列
from windget import getWgsDInvestSaleCfSeries


# 获取投资减少_GSD
from windget import getWgsDInvestSaleCf


# 获取债务增加_GSD时间序列
from windget import getWgsDDebtIsSCfSeries


# 获取债务增加_GSD
from windget import getWgsDDebtIsSCf


# 获取债务减少_GSD时间序列
from windget import getWgsDDebtReDuctCfSeries


# 获取债务减少_GSD
from windget import getWgsDDebtReDuctCf


# 获取股本增加_GSD时间序列
from windget import getWgsDStKPUrchCfSeries


# 获取股本增加_GSD
from windget import getWgsDStKPUrchCf


# 获取股本减少_GSD时间序列
from windget import getWgsDStKSaleCfSeries


# 获取股本减少_GSD
from windget import getWgsDStKSaleCf


# 获取支付的股利合计_GSD时间序列
from windget import getWgsDDivCfSeries


# 获取支付的股利合计_GSD
from windget import getWgsDDivCf


# 获取汇率变动影响_GSD时间序列
from windget import getWgsDForExChCfSeries


# 获取汇率变动影响_GSD
from windget import getWgsDForExChCf


# 获取单季度.主营收入_GSD时间序列
from windget import getWgsDQfaSalesOperSeries


# 获取单季度.主营收入_GSD
from windget import getWgsDQfaSalesOper


# 获取单季度.共同发展公司损益_GSD时间序列
from windget import getWgsDQfaGainJointlyControlledSeries


# 获取单季度.共同发展公司损益_GSD
from windget import getWgsDQfaGainJointlyControlled


# 获取单季度.员工薪酬_GSD时间序列
from windget import getWgsDQfaEMplBenSeries


# 获取单季度.员工薪酬_GSD
from windget import getWgsDQfaEMplBen


# 获取单季度.折旧及摊销_GSD时间序列
from windget import getWgsDQfaDaSeries


# 获取单季度.折旧及摊销_GSD
from windget import getWgsDQfaDa


# 获取单季度.权益性投资损益_GSD时间序列
from windget import getWgsDQfaInvestGainSeries


# 获取单季度.权益性投资损益_GSD
from windget import getWgsDQfaInvestGain


# 获取单季度.材料及相关费用_GSD时间序列
from windget import getWgsDQfaExpMaterialsSeries


# 获取单季度.材料及相关费用_GSD
from windget import getWgsDQfaExpMaterials


# 获取单季度.联营公司损益_GSD时间序列
from windget import getWgsDQfaGainAssociatesSeries


# 获取单季度.联营公司损益_GSD
from windget import getWgsDQfaGainAssociates


# 获取单季度.销售、行政及一般费用_GSD时间序列
from windget import getWgsDQfaSgaExpSeries


# 获取单季度.销售、行政及一般费用_GSD
from windget import getWgsDQfaSgaExp


# 获取单季度.除税前利润_GSD时间序列
from windget import getWgsDQfaIncPreTaxSeries


# 获取单季度.除税前利润_GSD
from windget import getWgsDQfaIncPreTax


# 获取单季度.非经常项目前利润_GSD时间序列
from windget import getWgsDQfaEBtExClUnusualItemsSeries


# 获取单季度.非经常项目前利润_GSD
from windget import getWgsDQfaEBtExClUnusualItems


# 获取单季度.非经常项目损益_GSD时间序列
from windget import getWgsDQfaUnusualItemsSeries


# 获取单季度.非经常项目损益_GSD
from windget import getWgsDQfaUnusualItems


# 获取单季度.交易账户净收入_GSD时间序列
from windget import getWgsDQfaTradeIncNetSeries


# 获取单季度.交易账户净收入_GSD
from windget import getWgsDQfaTradeIncNet


# 获取单季度.手续费及佣金开支_GSD时间序列
from windget import getWgsDQfaFeeComMExpSeries


# 获取单季度.手续费及佣金开支_GSD
from windget import getWgsDQfaFeeComMExp


# 获取单季度.扣除贷款损失准备前收入_GSD时间序列
from windget import getWgsDQfaRevComMIncSeries


# 获取单季度.扣除贷款损失准备前收入_GSD
from windget import getWgsDQfaRevComMInc


# 获取单季度.保单持有人利益_GSD时间序列
from windget import getWgsDQfaPolicyHlDrBenSeries


# 获取单季度.保单持有人利益_GSD
from windget import getWgsDQfaPolicyHlDrBen


# 获取单季度.保单获取成本和承保费用_GSD时间序列
from windget import getWgsDQfaCostPolicyAcquisitionSeries


# 获取单季度.保单获取成本和承保费用_GSD
from windget import getWgsDQfaCostPolicyAcquisition


# 获取单季度.利息及股息收入_GSD时间序列
from windget import getWgsDQfaIntInverStIncSeries


# 获取单季度.利息及股息收入_GSD
from windget import getWgsDQfaIntInverStInc


# 获取单季度.已发生赔款净额_GSD时间序列
from windget import getWgsDQfaClaimIncurredSeries


# 获取单季度.已发生赔款净额_GSD
from windget import getWgsDQfaClaimIncurred


# 获取单季度.毛承保保费及保单费收入_GSD时间序列
from windget import getWgsDQfaPremiumGrossSeries


# 获取单季度.毛承保保费及保单费收入_GSD
from windget import getWgsDQfaPremiumGross


# 获取单季度.房地产销售收入_GSD时间序列
from windget import getWgsDQfaGainSaleRealEstateSeries


# 获取单季度.房地产销售收入_GSD
from windget import getWgsDQfaGainSaleRealEstate


# 获取单季度.抵押贷款相关收入_GSD时间序列
from windget import getWgsDQfaMtGIncSeries


# 获取单季度.抵押贷款相关收入_GSD
from windget import getWgsDQfaMtGInc


# 获取单季度.租金收入_GSD时间序列
from windget import getWgsDQfaRevRentSeries


# 获取单季度.租金收入_GSD
from windget import getWgsDQfaRevRent


# 获取单季度.经纪佣金收入_GSD时间序列
from windget import getWgsDQfaBrokerComMIncSeries


# 获取单季度.经纪佣金收入_GSD
from windget import getWgsDQfaBrokerComMInc


# 获取单季度.承销与投资银行费收入_GSD时间序列
from windget import getWgsDQfaUwIbIncSeries


# 获取单季度.承销与投资银行费收入_GSD
from windget import getWgsDQfaUwIbInc


# 获取单季度.贷款损失准备_GSD时间序列
from windget import getWgsDQfaProvLoanLossSeries


# 获取单季度.贷款损失准备_GSD
from windget import getWgsDQfaProvLoanLoss


# 获取单季度.折旧与摊销_GSD时间序列
from windget import getWgsDQfaDepExpCfSeries


# 获取单季度.折旧与摊销_GSD
from windget import getWgsDQfaDepExpCf


# 获取单季度.资本性支出_GSD时间序列
from windget import getWgsDQfaCapeXFfSeries


# 获取单季度.资本性支出_GSD
from windget import getWgsDQfaCapeXFf


# 获取单季度.投资增加_GSD时间序列
from windget import getWgsDQfaInvestPUrchCfSeries


# 获取单季度.投资增加_GSD
from windget import getWgsDQfaInvestPUrchCf


# 获取单季度.投资减少_GSD时间序列
from windget import getWgsDQfaInvestSaleCfSeries


# 获取单季度.投资减少_GSD
from windget import getWgsDQfaInvestSaleCf


# 获取单季度.债务增加_GSD时间序列
from windget import getWgsDQfaDebtIsSCfSeries


# 获取单季度.债务增加_GSD
from windget import getWgsDQfaDebtIsSCf


# 获取单季度.债务减少_GSD时间序列
from windget import getWgsDQfaDebtReDuctCfSeries


# 获取单季度.债务减少_GSD
from windget import getWgsDQfaDebtReDuctCf


# 获取单季度.股本增加_GSD时间序列
from windget import getWgsDQfaStKPUrchCfSeries


# 获取单季度.股本增加_GSD
from windget import getWgsDQfaStKPUrchCf


# 获取单季度.股本减少_GSD时间序列
from windget import getWgsDQfaStKSaleCfSeries


# 获取单季度.股本减少_GSD
from windget import getWgsDQfaStKSaleCf


# 获取单季度.支付的股利合计_GSD时间序列
from windget import getWgsDQfaDivCfSeries


# 获取单季度.支付的股利合计_GSD
from windget import getWgsDQfaDivCf


# 获取单季度.汇率变动影响_GSD时间序列
from windget import getWgsDQfaForExChCfSeries


# 获取单季度.汇率变动影响_GSD
from windget import getWgsDQfaForExChCf


# 获取永续债_合计_GSD时间序列
from windget import getArdBsPerpetualSeries


# 获取永续债_合计_GSD
from windget import getArdBsPerpetual


# 获取股权激励支出_GSD时间序列
from windget import getIsSharePaymentsSeries


# 获取股权激励支出_GSD
from windget import getIsSharePayments


# 获取市净率PB(MRQ,海外)时间序列
from windget import getPbMrQGsDSeries


# 获取市净率PB(MRQ,海外)
from windget import getPbMrQGsD


# 获取现金短债比(公告值)_GSD时间序列
from windget import getStDebtRatioSeries


# 获取现金短债比(公告值)_GSD
from windget import getStDebtRatio


# 获取永续债_归属于少数股东_GSD时间序列
from windget import getArdBsPerPMinSeries


# 获取永续债_归属于少数股东_GSD
from windget import getArdBsPerPMin


# 获取永续债_归属于母公司股东_GSD时间序列
from windget import getArdBsPerPParSeries


# 获取永续债_归属于母公司股东_GSD
from windget import getArdBsPerPPar


# 获取投资物业公允价值变动(公布值)_GSD时间序列
from windget import getArdIsInvestmentPropertySeries


# 获取投资物业公允价值变动(公布值)_GSD
from windget import getArdIsInvestmentProperty


# 获取一致预测ROE(FY1)时间序列
from windget import getWestAvgRoeFy1Series


# 获取一致预测ROE(FY1)
from windget import getWestAvgRoeFy1


# 获取一致预测ROE(FY2)时间序列
from windget import getWestAvgRoeFy2Series


# 获取一致预测ROE(FY2)
from windget import getWestAvgRoeFy2


# 获取一致预测ROE(FY3)时间序列
from windget import getWestAvgRoeFy3Series


# 获取一致预测ROE(FY3)
from windget import getWestAvgRoeFy3


# 获取一致预测ROE同比时间序列
from windget import getWestAvgRoeYoYSeries


# 获取一致预测ROE同比
from windget import getWestAvgRoeYoY


# 获取参考市盈率PE(LYR)时间序列
from windget import getPelYrRefSeries


# 获取参考市盈率PE(LYR)
from windget import getPelYrRef


# 获取市盈率PE(LYR)时间序列
from windget import getPeLyRSeries


# 获取市盈率PE(LYR)
from windget import getPeLyR


# 获取市净率PB(LYR)时间序列
from windget import getPbLyRSeries


# 获取市净率PB(LYR)
from windget import getPbLyR


# 获取市销率PS(LYR)时间序列
from windget import getPsLyRSeries


# 获取市销率PS(LYR)
from windget import getPsLyR


# 获取PER(LYR)时间序列
from windget import getValPerSeries


# 获取PER(LYR)
from windget import getValPer


# 获取市盈率PE(LYR,加权)时间序列
from windget import getValPeWGtSeries


# 获取市盈率PE(LYR,加权)
from windget import getValPeWGt


# 获取市现率PCF(现金净流量LYR)时间序列
from windget import getPcfNflYrSeries


# 获取市现率PCF(现金净流量LYR)
from windget import getPcfNflYr


# 获取区间最高PS(LYR)时间序列
from windget import getValPSlyRHighSeries


# 获取区间最高PS(LYR)
from windget import getValPSlyRHigh


# 获取区间最低PS(LYR)时间序列
from windget import getValPSlyRLowSeries


# 获取区间最低PS(LYR)
from windget import getValPSlyRLow


# 获取区间平均PS(LYR)时间序列
from windget import getValPSlyRAvgSeries


# 获取区间平均PS(LYR)
from windget import getValPSlyRAvg


# 获取市净率PB(LF,内地)时间序列
from windget import getPbLfSeries


# 获取市净率PB(LF,内地)
from windget import getPbLf


# 获取区间最高PB(LF)时间序列
from windget import getValPbHighSeries


# 获取区间最高PB(LF)
from windget import getValPbHigh


# 获取区间最低PB(LF)时间序列
from windget import getValPbLowSeries


# 获取区间最低PB(LF)
from windget import getValPbLow


# 获取区间平均PB(LF)时间序列
from windget import getValPbAvgSeries


# 获取区间平均PB(LF)
from windget import getValPbAvg


# 获取发布方市净率PB(LF)时间序列
from windget import getValPbLfIssuerSeries


# 获取发布方市净率PB(LF)
from windget import getValPbLfIssuer


# 获取一致预测每股股利(FY1)时间序列
from windget import getWestAvgDpsFy1Series


# 获取一致预测每股股利(FY1)
from windget import getWestAvgDpsFy1


# 获取一致预测每股股利(FY2)时间序列
from windget import getWestAvgDpsFy2Series


# 获取一致预测每股股利(FY2)
from windget import getWestAvgDpsFy2


# 获取一致预测每股股利(FY3)时间序列
from windget import getWestAvgDpsFy3Series


# 获取一致预测每股股利(FY3)
from windget import getWestAvgDpsFy3


# 获取一致预测每股现金流(FY1)时间序列
from windget import getWestAvgCpSFy1Series


# 获取一致预测每股现金流(FY1)
from windget import getWestAvgCpSFy1


# 获取一致预测每股现金流(FY2)时间序列
from windget import getWestAvgCpSFy2Series


# 获取一致预测每股现金流(FY2)
from windget import getWestAvgCpSFy2


# 获取一致预测每股现金流(FY3)时间序列
from windget import getWestAvgCpSFy3Series

#-<End>









