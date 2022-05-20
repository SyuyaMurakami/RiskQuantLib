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
# 获取报告期末投资组合平均剩余期限时间序列 -> getMmAvgPtMSeries


# 获取报告期末投资组合平均剩余期限 -> getMmAvgPtM


# 获取报告期内投资组合平均剩余期限最高值时间序列 -> getMmAvgPtMMaxSeries


# 获取报告期内投资组合平均剩余期限最高值 -> getMmAvgPtMMax


# 获取报告期内投资组合平均剩余期限最低值时间序列 -> getMmAvgPtMMinSeries


# 获取报告期内投资组合平均剩余期限最低值 -> getMmAvgPtMMin


# 获取按信用评级的债券投资市值时间序列 -> getPrtBondByCreditRatingSeries


# 获取按信用评级的债券投资市值 -> getPrtBondByCreditRating


# 获取按信用评级的资产支持证券投资市值时间序列 -> getPrtAbsByCreditRatingSeries


# 获取按信用评级的资产支持证券投资市值 -> getPrtAbsByCreditRating


# 获取按信用评级的同业存单投资市值时间序列 -> getPrtNcdByCreditRatingSeries


# 获取按信用评级的同业存单投资市值 -> getPrtNcdByCreditRating


# 获取按信用评级的债券投资占基金资产净值比时间序列 -> getPrtBondByCreditRatingToNavSeries


# 获取按信用评级的债券投资占基金资产净值比 -> getPrtBondByCreditRatingToNav


# 获取按信用评级的资产支持证券投资占基金资产净值比时间序列 -> getPrtAbsByCreditRatingToNavSeries


# 获取按信用评级的资产支持证券投资占基金资产净值比 -> getPrtAbsByCreditRatingToNav


# 获取按信用评级的同业存单投资占基金资产净值比时间序列 -> getPrtNcdByCreditRatingToNavSeries


# 获取按信用评级的同业存单投资占基金资产净值比 -> getPrtNcdByCreditRatingToNav


# 获取债券估值(YY)时间序列 -> getInStYyBondValSeries


# 获取债券估值(YY) -> getInStYyBondVal


# 获取债券估值历史(YY)时间序列 -> getInStYyBondValHisSeries


# 获取债券估值历史(YY) -> getInStYyBondValHis


# 获取融资融券余额时间序列 -> getMrgBalSeries


# 获取融资融券余额 -> getMrgBal


# 获取融资融券担保股票市值时间序列 -> getMarginGuaranteedStocksMarketValueSeries


# 获取融资融券担保股票市值 -> getMarginGuaranteedStocksMarketValue


# 获取是否融资融券标的时间序列 -> getMarginOrNotSeries


# 获取是否融资融券标的 -> getMarginOrNot


# 获取区间融资融券余额均值时间序列 -> getMrgBalIntAvgSeries


# 获取区间融资融券余额均值 -> getMrgBalIntAvg


# 获取利息收入:融资融券业务时间序列 -> getStmNoteSec1511Series


# 获取利息收入:融资融券业务 -> getStmNoteSec1511


# 获取利息净收入:融资融券业务时间序列 -> getStmNoteSec1531Series


# 获取利息净收入:融资融券业务 -> getStmNoteSec1531


# 获取涨跌_期货历史同月时间序列 -> getHisChangeSeries


# 获取涨跌_期货历史同月 -> getHisChange


# 获取振幅_期货历史同月时间序列 -> getHisSwingSeries


# 获取振幅_期货历史同月 -> getHisSwing


# 获取收盘价_期货历史同月时间序列 -> getHisCloseSeries


# 获取收盘价_期货历史同月 -> getHisClose


# 获取开盘价_期货历史同月时间序列 -> getHisOpenSeries


# 获取开盘价_期货历史同月 -> getHisOpen


# 获取最高价_期货历史同月时间序列 -> getHisHighSeries


# 获取最高价_期货历史同月 -> getHisHigh


# 获取最低价_期货历史同月时间序列 -> getHisLowSeries


# 获取最低价_期货历史同月 -> getHisLow


# 获取结算价_期货历史同月时间序列 -> getHisSettleSeries


# 获取结算价_期货历史同月 -> getHisSettle


# 获取涨跌幅_期货历史同月时间序列 -> getHisPctChangeSeries


# 获取涨跌幅_期货历史同月 -> getHisPctChange


# 获取成交量_期货历史同月时间序列 -> getHisVolumeSeries


# 获取成交量_期货历史同月 -> getHisVolume


# 获取成交额_期货历史同月时间序列 -> getHisTurnoverSeries


# 获取成交额_期货历史同月 -> getHisTurnover


# 获取持仓量_期货历史同月时间序列 -> getHisOiSeries


# 获取持仓量_期货历史同月 -> getHisOi


# 获取前结算价_期货历史同月时间序列 -> getHisPreSettleSeries


# 获取前结算价_期货历史同月 -> getHisPreSettle


# 获取成交均价_期货历史同月时间序列 -> getHisAvgPriceSeries


# 获取成交均价_期货历史同月 -> getHisAvgPrice


# 获取持仓变化_期货历史同月时间序列 -> getHisOiChangeSeries


# 获取持仓变化_期货历史同月 -> getHisOiChange


# 获取收盘价(夜盘)_期货历史同月时间序列 -> getHisCloseNightSeries


# 获取收盘价(夜盘)_期货历史同月 -> getHisCloseNight


# 获取涨跌(结算价)_期货历史同月时间序列 -> getHisChangeSettlementSeries


# 获取涨跌(结算价)_期货历史同月 -> getHisChangeSettlement


# 获取涨跌幅(结算价)_期货历史同月时间序列 -> getHisPctChangeSettlementSeries


# 获取涨跌幅(结算价)_期货历史同月 -> getHisPctChangeSettlement


# 获取业绩预告摘要时间序列 -> getProfitNoticeAbstractSeries


# 获取业绩预告摘要 -> getProfitNoticeAbstract


# 获取业绩预告变动原因时间序列 -> getProfitNoticeReasonSeries


# 获取业绩预告变动原因 -> getProfitNoticeReason


# 获取业绩预告类型时间序列 -> getProfitNoticeStyleSeries


# 获取业绩预告类型 -> getProfitNoticeStyle


# 获取业绩预告最新披露日期时间序列 -> getProfitNoticeDateSeries


# 获取业绩预告最新披露日期 -> getProfitNoticeDate


# 获取业绩预告首次披露日期时间序列 -> getProfitNoticeFirstDateSeries


# 获取业绩预告首次披露日期 -> getProfitNoticeFirstDate


# 获取最新业绩预告报告期时间序列 -> getProfitNoticeLastRpTDateSeries


# 获取最新业绩预告报告期 -> getProfitNoticeLastRpTDate


# 获取单季度.业绩预告摘要(海外)时间序列 -> getQProfitNoticeAbstractSeries


# 获取单季度.业绩预告摘要(海外) -> getQProfitNoticeAbstract


# 获取单季度.业绩预告类型(海外)时间序列 -> getQProfitNoticeStyleSeries


# 获取单季度.业绩预告类型(海外) -> getQProfitNoticeStyle


# 获取单季度.业绩预告日期(海外)时间序列 -> getQProfitNoticeDateSeries


# 获取单季度.业绩预告日期(海外) -> getQProfitNoticeDate


# 获取业绩快报最新披露日期时间序列 -> getPerformanceExpressLastDateSeries


# 获取业绩快报最新披露日期 -> getPerformanceExpressLastDate


# 获取业绩快报首次披露日期时间序列 -> getPerformanceExpressDateSeries


# 获取业绩快报首次披露日期 -> getPerformanceExpressDate


# 获取业绩快报.营业收入时间序列 -> getPerformanceExpressPerFExIncomeSeries


# 获取业绩快报.营业收入 -> getPerformanceExpressPerFExIncome


# 获取业绩快报.营业利润时间序列 -> getPerformanceExpressPerFExprOfItSeries


# 获取业绩快报.营业利润 -> getPerformanceExpressPerFExprOfIt


# 获取业绩快报.利润总额时间序列 -> getPerformanceExpressPerFExTotalProfitSeries


# 获取业绩快报.利润总额 -> getPerformanceExpressPerFExTotalProfit


# 获取业绩快报.归属母公司股东的净利润时间序列 -> getPerformanceExpressPerFExNetProfitToShareholderSeries


# 获取业绩快报.归属母公司股东的净利润 -> getPerformanceExpressPerFExNetProfitToShareholder


# 获取业绩快报.归属于上市公司股东的扣除非经常性损益的净利润时间序列 -> getPerformanceExpressNpdEdToShareholderSeries


# 获取业绩快报.归属于上市公司股东的扣除非经常性损益的净利润 -> getPerformanceExpressNpdEdToShareholder


# 获取业绩快报.每股收益EPS-基本时间序列 -> getPerformanceExpressPerFExEpsDilutedSeries


# 获取业绩快报.每股收益EPS-基本 -> getPerformanceExpressPerFExEpsDiluted


# 获取业绩快报.净资产收益率ROE-加权时间序列 -> getPerformanceExpressPerFExRoeDilutedSeries


# 获取业绩快报.净资产收益率ROE-加权 -> getPerformanceExpressPerFExRoeDiluted


# 获取业绩快报.总资产时间序列 -> getPerformanceExpressPerFExTotalAssetsSeries


# 获取业绩快报.总资产 -> getPerformanceExpressPerFExTotalAssets


# 获取业绩快报.净资产时间序列 -> getPerformanceExpressPerFExNetAssetsSeries


# 获取业绩快报.净资产 -> getPerformanceExpressPerFExNetAssets


# 获取业绩快报.同比增长率:营业收入时间序列 -> getPerformanceExpressOrYoYSeries


# 获取业绩快报.同比增长率:营业收入 -> getPerformanceExpressOrYoY


# 获取业绩快报.同比增长率:营业利润时间序列 -> getPerformanceExpressOpYoYSeries


# 获取业绩快报.同比增长率:营业利润 -> getPerformanceExpressOpYoY


# 获取业绩快报.同比增长率:利润总额时间序列 -> getPerformanceExpressEBtYoYSeries


# 获取业绩快报.同比增长率:利润总额 -> getPerformanceExpressEBtYoY


# 获取业绩快报.同比增长率:归属母公司股东的净利润时间序列 -> getPerformanceExpressNpYoYSeries


# 获取业绩快报.同比增长率:归属母公司股东的净利润 -> getPerformanceExpressNpYoY


# 获取业绩快报.同比增长率:归属于上市公司股东的扣除非经常性损益的净利润时间序列 -> getPerformanceExpressNpdEdYoYSeries


# 获取业绩快报.同比增长率:归属于上市公司股东的扣除非经常性损益的净利润 -> getPerformanceExpressNpdEdYoY


# 获取业绩快报.同比增长率:基本每股收益时间序列 -> getPerformanceExpressEpsYoYSeries


# 获取业绩快报.同比增长率:基本每股收益 -> getPerformanceExpressEpsYoY


# 获取业绩快报.同比增减:加权平均净资产收益率时间序列 -> getPerformanceExpressRoeYoYSeries


# 获取业绩快报.同比增减:加权平均净资产收益率 -> getPerformanceExpressRoeYoY


# 获取业绩快报.去年同期营业收入时间序列 -> getPerformanceExpressIncomeYaSeries


# 获取业绩快报.去年同期营业收入 -> getPerformanceExpressIncomeYa


# 获取业绩快报.去年同期营业利润时间序列 -> getPerformanceExpressProfitYaSeries


# 获取业绩快报.去年同期营业利润 -> getPerformanceExpressProfitYa


# 获取业绩快报.去年同期利润总额时间序列 -> getPerformanceExpressToTProfitYaSeries


# 获取业绩快报.去年同期利润总额 -> getPerformanceExpressToTProfitYa


# 获取业绩快报.去年同期净利润时间序列 -> getPerformanceExpressNetProfitYaSeries


# 获取业绩快报.去年同期净利润 -> getPerformanceExpressNetProfitYa


# 获取业绩快报.上年同期归属于上市公司股东的扣除非经常性损益的净利润时间序列 -> getPerformanceExpressNpdEdYaSeries


# 获取业绩快报.上年同期归属于上市公司股东的扣除非经常性损益的净利润 -> getPerformanceExpressNpdEdYa


# 获取业绩快报.去年同期每股收益时间序列 -> getPerformanceExpressEpsYaSeries


# 获取业绩快报.去年同期每股收益 -> getPerformanceExpressEpsYa


# 获取业绩快报.每股净资产时间序列 -> getPerformanceExpressBpSSeries


# 获取业绩快报.每股净资产 -> getPerformanceExpressBpS


# 获取业绩快报.期初净资产时间序列 -> getPerformanceExpressNetAssetsBSeries


# 获取业绩快报.期初净资产 -> getPerformanceExpressNetAssetsB


# 获取业绩快报.期初每股净资产时间序列 -> getPerformanceExpressBpSBSeries


# 获取业绩快报.期初每股净资产 -> getPerformanceExpressBpSB


# 获取业绩快报.比年初增长率:归属母公司的股东权益时间序列 -> getPerformanceExpressEqYGrowthSeries


# 获取业绩快报.比年初增长率:归属母公司的股东权益 -> getPerformanceExpressEqYGrowth


# 获取业绩快报.比年初增长率:归属于母公司股东的每股净资产时间序列 -> getPerformanceExpressBpSGrowthSeries


# 获取业绩快报.比年初增长率:归属于母公司股东的每股净资产 -> getPerformanceExpressBpSGrowth


# 获取业绩快报.比年初增长率:总资产时间序列 -> getPerformanceExpressToTAssetsGrowthSeries


# 获取业绩快报.比年初增长率:总资产 -> getPerformanceExpressToTAssetsGrowth


# 获取最新业绩快报报告期时间序列 -> getPerformanceExpressLastRpTDateSeries


# 获取最新业绩快报报告期 -> getPerformanceExpressLastRpTDate


# 获取年度可转债发行量时间序列 -> getRelatedCbYearlyAmountSeries


# 获取年度可转债发行量 -> getRelatedCbYearlyAmount


# 获取基金发行协调人时间序列 -> getIssueCoordinatorSeries


# 获取基金发行协调人 -> getIssueCoordinator


# 获取上市基金发行价格时间序列 -> getIssuePriceSeries


# 获取上市基金发行价格 -> getIssuePrice


# 获取基金分红收益_FUND时间序列 -> getStmIs82Series


# 获取基金分红收益_FUND -> getStmIs82


# 获取基金规模时间序列 -> getFundFundScaleSeries


# 获取基金规模 -> getFundFundScale


# 获取基金规模(合计)时间序列 -> getNetAssetTotalSeries


# 获取基金规模(合计) -> getNetAssetTotal


# 获取所属国民经济行业分类时间序列 -> getIndustryNcSeries


# 获取所属国民经济行业分类 -> getIndustryNc


# 获取管理层年度薪酬总额时间序列 -> getStmNoteMGmtBenSeries


# 获取管理层年度薪酬总额 -> getStmNoteMGmtBen


# 获取管理层增持价格时间序列 -> getHolderPriceMhSeries


# 获取管理层增持价格 -> getHolderPriceMh


# 获取中资中介机构持股数量时间序列 -> getShareCnSeries


# 获取中资中介机构持股数量 -> getShareCn


# 获取国际中介机构持股数量时间序列 -> getShareOsSeries


# 获取国际中介机构持股数量 -> getShareOs


# 获取中资中介机构持股占比时间序列 -> getSharePctCnSeries


# 获取中资中介机构持股占比 -> getSharePctCn


# 获取国际中介机构持股占比时间序列 -> getSharePctOsSeries


# 获取国际中介机构持股占比 -> getSharePctOs


# 获取香港本地中介机构持股数量时间序列 -> getShareHkSeries


# 获取香港本地中介机构持股数量 -> getShareHk


# 获取香港本地中介机构持股占比时间序列 -> getSharePctHkSeries


# 获取香港本地中介机构持股占比 -> getSharePctHk


# 获取机构调研家数时间序列 -> getIrNoIiSeries


# 获取机构调研家数 -> getIrNoIi


# 获取机构调研首日时间序列 -> getIrIRfdSeries


# 获取机构调研首日 -> getIrIRfd


# 获取机构调研最新日时间序列 -> getIrIrlDSeries


# 获取机构调研最新日 -> getIrIrlD


# 获取投资机构调研次数时间序列 -> getIrNoSoIiSeries


# 获取投资机构调研次数 -> getIrNoSoIi


# 获取投资机构调研家数时间序列 -> getIrNoIiiiSeries


# 获取投资机构调研家数 -> getIrNoIiii


# 获取外资机构调研次数时间序列 -> getIrNosOfISeries


# 获取外资机构调研次数 -> getIrNosOfI


# 获取外资机构调研家数时间序列 -> getIrNoIiFiSeries


# 获取外资机构调研家数 -> getIrNoIiFi


# 获取流通A股占总股本比例时间序列 -> getShareLiqAPctSeries


# 获取流通A股占总股本比例 -> getShareLiqAPct


# 获取限售A股占总股本比例时间序列 -> getShareRestrictedAPctSeries


# 获取限售A股占总股本比例 -> getShareRestrictedAPct


# 获取A股合计占总股本比例时间序列 -> getShareTotalAPctSeries


# 获取A股合计占总股本比例 -> getShareTotalAPct


# 获取流通B股占总股本比例时间序列 -> getShareLiqBPctSeries


# 获取流通B股占总股本比例 -> getShareLiqBPct


# 获取限售B股占总股本比例时间序列 -> getShareRestrictedBPctSeries


# 获取限售B股占总股本比例 -> getShareRestrictedBPct


# 获取B股合计占总股本比例时间序列 -> getShareTotalBPctSeries


# 获取B股合计占总股本比例 -> getShareTotalBPct


# 获取三板A股占总股本比例时间序列 -> getShareOtcAPctSeries


# 获取三板A股占总股本比例 -> getShareOtcAPct


# 获取三板B股占总股本比例时间序列 -> getShareOtcBPctSeries


# 获取三板B股占总股本比例 -> getShareOtcBPct


# 获取三板合计占总股本比例时间序列 -> getShareTotalOtcPctSeries


# 获取三板合计占总股本比例 -> getShareTotalOtcPct


# 获取香港上市股占总股本比例时间序列 -> getShareLiqHPctSeries


# 获取香港上市股占总股本比例 -> getShareLiqHPct


# 获取海外上市股占总股本比例时间序列 -> getShareOverSeaPctSeries


# 获取海外上市股占总股本比例 -> getShareOverSeaPct


# 获取流通股合计占总股本比例时间序列 -> getShareTradablePctSeries


# 获取流通股合计占总股本比例 -> getShareTradablePct


# 获取限售股合计占总股本比例时间序列 -> getShareRestrictedPctSeries


# 获取限售股合计占总股本比例 -> getShareRestrictedPct


# 获取自由流通股占总股本比例时间序列 -> getShareFreeFloatsHrPctSeries


# 获取自由流通股占总股本比例 -> getShareFreeFloatsHrPct


# 获取未平仓卖空数占总股本比例时间序列 -> getShortSellShortIntRestPctSeries


# 获取未平仓卖空数占总股本比例 -> getShortSellShortIntRestPct


# 获取股改前非流通股占总股本比例时间序列 -> getShareNonTradablePctSeries


# 获取股改前非流通股占总股本比例 -> getShareNonTradablePct


# 获取质押股份数量合计时间序列 -> getSharePledgedASeries


# 获取质押股份数量合计 -> getSharePledgedA


# 获取基金份额时间序列 -> getUnitTotalSeries


# 获取基金份额 -> getUnitTotal


# 获取基金份额(合计)时间序列 -> getUnitFundShareTotalSeries


# 获取基金份额(合计) -> getUnitFundShareTotal


# 获取基金份额变化时间序列 -> getUnitChangeSeries


# 获取基金份额变化 -> getUnitChange


# 获取基金份额变化率时间序列 -> getUnitChangeRateSeries


# 获取基金份额变化率 -> getUnitChangeRate


# 获取基金份额持有人户数时间序列 -> getHolderNumberSeries


# 获取基金份额持有人户数 -> getHolderNumber


# 获取基金份额持有人户数(合计)时间序列 -> getFundHolderTotalNumberSeries


# 获取基金份额持有人户数(合计) -> getFundHolderTotalNumber


# 获取基金份额变动日期时间序列 -> getUnitChangeDateSeries


# 获取基金份额变动日期 -> getUnitChangeDate


# 获取本期基金份额交易产生的基金净值变动数时间序列 -> getStmNavChange9Series


# 获取本期基金份额交易产生的基金净值变动数 -> getStmNavChange9


# 获取ETF基金份额折算日时间序列 -> getFundFundShareTranslationDateSeries


# 获取ETF基金份额折算日 -> getFundFundShareTranslationDate


# 获取ETF基金份额折算比例时间序列 -> getFundFundShareTranslationRatioSeries


# 获取ETF基金份额折算比例 -> getFundFundShareTranslationRatio


# 获取本期向基金份额持有人分配利润产生的基金净值变动数时间序列 -> getStmNavChange10Series


# 获取本期向基金份额持有人分配利润产生的基金净值变动数 -> getStmNavChange10


# 获取单季度.基金份额净值增长率时间序列 -> getQAnalNavReturnSeries


# 获取单季度.基金份额净值增长率 -> getQAnalNavReturn


# 获取单季度.基金份额净值增长率标准差时间序列 -> getQAnalStdNavReturnSeries


# 获取单季度.基金份额净值增长率标准差 -> getQAnalStdNavReturn


# 获取平均每户持有基金份额时间序列 -> getHolderAvgHoldingSeries


# 获取平均每户持有基金份额 -> getHolderAvgHolding


# 获取单季度.累计基金份额净值增长率时间序列 -> getQAnalAccumulatedNavReturnSeries


# 获取单季度.累计基金份额净值增长率 -> getQAnalAccumulatedNavReturn


# 获取单季度.加权平均基金份额本期利润时间序列 -> getQAnalAvgNetIncomePerUnitSeries


# 获取单季度.加权平均基金份额本期利润 -> getQAnalAvgNetIncomePerUnit


# 获取单季度.加权平均基金份额本期净收益时间序列 -> getQAnalAvgUnitIncomeSeries


# 获取单季度.加权平均基金份额本期净收益 -> getQAnalAvgUnitIncome


# 获取报告期末可供分配基金份额利润时间序列 -> getAnalDIsTriButAblePerUnitSeries


# 获取报告期末可供分配基金份额利润 -> getAnalDIsTriButAblePerUnit


# 获取单季度.报告期期末基金份额净值时间序列 -> getQAnalNavSeries


# 获取单季度.报告期期末基金份额净值 -> getQAnalNav


# 获取股东户数时间序列 -> getHolderNumSeries


# 获取股东户数 -> getHolderNum


# 获取机构持股数量合计时间序列 -> getHolderTotalByInStSeries


# 获取机构持股数量合计 -> getHolderTotalByInSt


# 获取机构持股比例合计时间序列 -> getHolderPctByInStSeries


# 获取机构持股比例合计 -> getHolderPctByInSt


# 获取上清所债券分类时间序列 -> getSHClearL1TypeSeries


# 获取上清所债券分类 -> getSHClearL1Type


# 获取标准券折算比例时间序列 -> getRateOfStdBndSeries


# 获取标准券折算比例 -> getRateOfStdBnd


# 获取转股条款时间序列 -> getClauseConversion2ToSharePriceAdjustItemSeries


# 获取转股条款 -> getClauseConversion2ToSharePriceAdjustItem


# 获取赎回条款时间序列 -> getClauseCallOptionRedeemItemSeries


# 获取赎回条款 -> getClauseCallOptionRedeemItem


# 获取时点赎回条款全文时间序列 -> getClauseCallOptionRedeemClauseSeries


# 获取时点赎回条款全文 -> getClauseCallOptionRedeemClause


# 获取巨额赎回条款时间序列 -> getMassRedemptionProvisionSeries


# 获取巨额赎回条款 -> getMassRedemptionProvision


# 获取是否有时点赎回条款时间序列 -> getClauseCallOptionIsWithTimeRedemptionClauseSeries


# 获取是否有时点赎回条款 -> getClauseCallOptionIsWithTimeRedemptionClause


# 获取条件回售条款全文时间序列 -> getClausePutOptionSellBackItemSeries


# 获取条件回售条款全文 -> getClausePutOptionSellBackItem


# 获取时点回售条款全文时间序列 -> getClausePutOptionTimePutBackClauseSeries


# 获取时点回售条款全文 -> getClausePutOptionTimePutBackClause


# 获取无条件回售条款时间序列 -> getClausePutOptionPutBackClauseSeries


# 获取无条件回售条款 -> getClausePutOptionPutBackClause


# 获取最新评级月份时间序列 -> getRatingLatestMonthSeries


# 获取最新评级月份 -> getRatingLatestMonth


# 获取发行人最新评级时间序列 -> getLatestIsSurerCreditRatingSeries


# 获取发行人最新评级 -> getLatestIsSurerCreditRating


# 获取发行人最新评级展望时间序列 -> getRatingOutlooksSeries


# 获取发行人最新评级展望 -> getRatingOutlooks


# 获取发行人最新评级日期时间序列 -> getLatestIsSurerCreditRatingDateSeries


# 获取发行人最新评级日期 -> getLatestIsSurerCreditRatingDate


# 获取发行人最新评级日期(指定机构)时间序列 -> getLatestRatingDateSeries


# 获取发行人最新评级日期(指定机构) -> getLatestRatingDate


# 获取发行人最新评级变动方向时间序列 -> getRateLateIssuerChNgSeries


# 获取发行人最新评级变动方向 -> getRateLateIssuerChNg


# 获取发行人最新评级评级类型时间序列 -> getLatestIsSurerCreditRatingTypeSeries


# 获取发行人最新评级评级类型 -> getLatestIsSurerCreditRatingType


# 获取担保人最新评级时间序列 -> getLatestRatingOfGuarantorSeries


# 获取担保人最新评级 -> getLatestRatingOfGuarantor


# 获取担保人最新评级展望时间序列 -> getRateLateGuarantorFwdSeries


# 获取担保人最新评级展望 -> getRateLateGuarantorFwd


# 获取担保人最新评级日期时间序列 -> getRateLateGuarantorDateSeries


# 获取担保人最新评级日期 -> getRateLateGuarantorDate


# 获取担保人最新评级变动方向时间序列 -> getRateLateGuaranTorchNgSeries


# 获取担保人最新评级变动方向 -> getRateLateGuaranTorchNg


# 获取债券国际评级时间序列 -> getRateBond2Series


# 获取债券国际评级 -> getRateBond2


# 获取发行人国际评级时间序列 -> getIssuer2Series


# 获取发行人国际评级 -> getIssuer2


# 获取回购代码时间序列 -> getRepoCodeSeries


# 获取回购代码 -> getRepoCode


# 获取标的债券时间序列 -> getRepoUBondSeries


# 获取标的债券 -> getRepoUBond


# 获取发行时标的债券余额时间序列 -> getCrmUbonDouStandingAmountSeries


# 获取发行时标的债券余额 -> getCrmUbonDouStandingAmount


# 获取回购类型时间序列 -> getRepoTypeSeries


# 获取回购类型 -> getRepoType


# 获取回购天数时间序列 -> getRepoDaysSeries


# 获取回购天数 -> getRepoDays


# 获取凭证起始日时间序列 -> getCrmCarryDateSeries


# 获取凭证起始日 -> getCrmCarryDate


# 获取标的实体交易代码时间序列 -> getCrmSubjectCodeSeries


# 获取标的实体交易代码 -> getCrmSubjectCode


# 获取履约保障机制时间序列 -> getCrmPerformGuaranteeSeries


# 获取履约保障机制 -> getCrmPerformGuarantee


# 获取信用事件时间序列 -> getCrmCreditEventSeries


# 获取信用事件 -> getCrmCreditEvent


# 获取债券信用状态时间序列 -> getCreditBondCreditStatusSeries


# 获取债券信用状态 -> getCreditBondCreditStatus


# 获取发行人首次违约日时间序列 -> getIssuerFirstDefaultDateSeries


# 获取发行人首次违约日 -> getIssuerFirstDefaultDate


# 获取登记机构时间序列 -> getCrmRegisterAgencySeries


# 获取登记机构 -> getCrmRegisterAgency


# 获取标的实体时间序列 -> getCrmSubjectSeries


# 获取标的实体 -> getCrmSubject


# 获取发布机构时间序列 -> getCrmIssuerSeries


# 获取发布机构 -> getCrmIssuer


# 获取簿记建档日时间序列 -> getCrmBookkeepingDateSeries


# 获取簿记建档日 -> getCrmBookkeepingDate


# 获取付费方式时间序列 -> getCrmPaymentTermsSeries


# 获取付费方式 -> getCrmPaymentTerms


# 获取创设价格时间序列 -> getCrmStartingPriceSeries


# 获取创设价格 -> getCrmStartingPrice


# 获取创设批准文件编号时间序列 -> getCrmPermissionNumberSeries


# 获取创设批准文件编号 -> getCrmPermissionNumber


# 获取凭证登记日时间序列 -> getCrmDateOfRecordSeries


# 获取凭证登记日 -> getCrmDateOfRecord


# 获取第三方基金分类时间序列 -> getFundThirdPartyFundTypeSeries


# 获取第三方基金分类 -> getFundThirdPartyFundType


# 获取Wind封闭式开放式基金分类时间序列 -> getFundProdTypeOcWindSeries


# 获取Wind封闭式开放式基金分类 -> getFundProdTypeOcWind


# 获取基金经理时间序列 -> getFundFundManagerOfTradeDateSeries


# 获取基金经理 -> getFundFundManagerOfTradeDate


# 获取基金经理(现任)时间序列 -> getFundFundManagerSeries


# 获取基金经理(现任) -> getFundFundManager


# 获取基金经理(历任)时间序列 -> getFundPRedFundManagerSeries


# 获取基金经理(历任) -> getFundPRedFundManager


# 获取基金经理(成立)时间序列 -> getFundInceptionFundManagerSeries


# 获取基金经理(成立) -> getFundInceptionFundManager


# 获取基金经理年限时间序列 -> getFundManagerManagerWorkingYearsSeries


# 获取基金经理年限 -> getFundManagerManagerWorkingYears


# 获取基金经理平均年限时间序列 -> getFundAverageWorkingYearsSeries


# 获取基金经理平均年限 -> getFundAverageWorkingYears


# 获取基金经理最大年限时间序列 -> getFundMaxWorkingYearsSeries


# 获取基金经理最大年限 -> getFundMaxWorkingYears


# 获取基金经理指数区间回报(算术平均)时间序列 -> getFundManagerIndexReturnSeries


# 获取基金经理指数区间回报(算术平均) -> getFundManagerIndexReturn


# 获取基金经理指数收益标准差(算术平均)时间序列 -> getFundManagerIndexStDevSeries


# 获取基金经理指数收益标准差(算术平均) -> getFundManagerIndexStDev


# 获取基金经理指数年化波动率(算术平均)时间序列 -> getFundManagerIndexStDevYearlySeries


# 获取基金经理指数年化波动率(算术平均) -> getFundManagerIndexStDevYearly


# 获取基金经理指数最大回撤(算术平均)时间序列 -> getFundManagerIndexMaxDownsideSeries


# 获取基金经理指数最大回撤(算术平均) -> getFundManagerIndexMaxDownside


# 获取基金经理指数区间回报(规模加权)时间序列 -> getFundManagerIndexWeightReturnSeries


# 获取基金经理指数区间回报(规模加权) -> getFundManagerIndexWeightReturn


# 获取基金经理指数收益标准差(规模加权)时间序列 -> getFundManagerIndexWeightStDevSeries


# 获取基金经理指数收益标准差(规模加权) -> getFundManagerIndexWeightStDev


# 获取基金经理指数年化波动率(规模加权)时间序列 -> getFundManagerIndexWeightStDevYearlySeries


# 获取基金经理指数年化波动率(规模加权) -> getFundManagerIndexWeightStDevYearly


# 获取基金经理指数最大回撤(规模加权)时间序列 -> getFundManagerIndexWeightMaxDownsideSeries


# 获取基金经理指数最大回撤(规模加权) -> getFundManagerIndexWeightMaxDownside


# 获取基金经理数时间序列 -> getFundCorpFundManagersNoSeries


# 获取基金经理数 -> getFundCorpFundManagersNo


# 获取基金经理成熟度时间序列 -> getFundCorpFundManagerMaturitySeries


# 获取基金经理成熟度 -> getFundCorpFundManagerMaturity


# 获取代管基金经理说明时间序列 -> getFundManagerProxyForManagerSeries


# 获取代管基金经理说明 -> getFundManagerProxyForManager


# 获取Beta(基金经理指数,算术平均)时间序列 -> getFundManagerIndexBetaSeries


# 获取Beta(基金经理指数,算术平均) -> getFundManagerIndexBeta


# 获取Beta(基金经理指数,规模加权)时间序列 -> getFundManagerIndexWeightBetaSeries


# 获取Beta(基金经理指数,规模加权) -> getFundManagerIndexWeightBeta


# 获取Alpha(基金经理指数,算术平均)时间序列 -> getFundManagerIndexAlphaSeries


# 获取Alpha(基金经理指数,算术平均) -> getFundManagerIndexAlpha


# 获取Alpha(基金经理指数,规模加权)时间序列 -> getFundManagerIndexWeightAlphaSeries


# 获取Alpha(基金经理指数,规模加权) -> getFundManagerIndexWeightAlpha


# 获取Sharpe(基金经理指数,算术平均)时间序列 -> getFundManagerIndexSharpeSeries


# 获取Sharpe(基金经理指数,算术平均) -> getFundManagerIndexSharpe


# 获取Sharpe(基金经理指数,规模加权)时间序列 -> getFundManagerIndexWeightSharpeSeries


# 获取Sharpe(基金经理指数,规模加权) -> getFundManagerIndexWeightSharpe


# 获取Treynor(基金经理指数,算术平均)时间序列 -> getFundManagerIndexTreyNorSeries


# 获取Treynor(基金经理指数,算术平均) -> getFundManagerIndexTreyNor


# 获取Treynor(基金经理指数,规模加权)时间序列 -> getFundManagerIndexWeightTreyNorSeries


# 获取Treynor(基金经理指数,规模加权) -> getFundManagerIndexWeightTreyNor


# 获取任职期限最长的现任基金经理时间序列 -> getFundManagerLongestFundManagerSeries


# 获取任职期限最长的现任基金经理 -> getFundManagerLongestFundManager


# 获取基金公司调研次数时间序列 -> getIrFcsSeries


# 获取基金公司调研次数 -> getIrFcs


# 获取基金公司调研家数时间序列 -> getIrNoFciSeries


# 获取基金公司调研家数 -> getIrNoFci


# 获取网下基金公司或其资管子公司配售数量时间序列 -> getFundReItsFmSSeries


# 获取网下基金公司或其资管子公司配售数量 -> getFundReItsFmS


# 获取网下基金公司或其资管子公司配售金额时间序列 -> getFundReItsFMmSeries


# 获取网下基金公司或其资管子公司配售金额 -> getFundReItsFMm


# 获取网下基金公司或其资管子公司配售份额占比时间序列 -> getFundReItsFMrSeries


# 获取网下基金公司或其资管子公司配售份额占比 -> getFundReItsFMr


# 获取网下基金公司或其资管计划配售数量时间序列 -> getFundReItsFmAsSeries


# 获取网下基金公司或其资管计划配售数量 -> getFundReItsFmAs


# 获取网下基金公司或其资管机构配售金额时间序列 -> getFundReItsFmAmSeries


# 获取网下基金公司或其资管机构配售金额 -> getFundReItsFmAm


# 获取网下基金公司或其资管计划配售份额占比时间序列 -> getFundReItsFMarSeries


# 获取网下基金公司或其资管计划配售份额占比 -> getFundReItsFMar


# 获取所属基金公司重仓行业市值时间序列 -> getPrtStockValueHoldingIndustryMktValue2Series


# 获取所属基金公司重仓行业市值 -> getPrtStockValueHoldingIndustryMktValue2


# 获取调研最多的基金公司时间序列 -> getIrTmRfcSeries


# 获取调研最多的基金公司 -> getIrTmRfc


# 获取开始交易日时间序列 -> getFtDateSeries


# 获取开始交易日 -> getFtDate


# 获取开始交易日(支持历史)时间序列 -> getFtDateNewSeries


# 获取开始交易日(支持历史) -> getFtDateNew


# 获取最后交易日时间序列 -> getLastTradeDateSeries


# 获取最后交易日 -> getLastTradeDate


# 获取最后交易日(支持历史)时间序列 -> getLtDateNewSeries


# 获取最后交易日(支持历史) -> getLtDateNew


# 获取最后交易日说明时间序列 -> getLtDatedSeries


# 获取最后交易日说明 -> getLtDated


# 获取最后交易日期时间序列 -> getLastTradingDateSeries


# 获取最后交易日期 -> getLastTradingDate


# 获取B股最后交易日时间序列 -> getDivLastTrDDateShareBSeries


# 获取B股最后交易日 -> getDivLastTrDDateShareB


# 获取(废弃)最后交易日时间序列 -> getLastTradingDaySeries


# 获取(废弃)最后交易日 -> getLastTradingDay


# 获取股权登记日(B股最后交易日)时间序列 -> getRightsIssueRegDateShareBSeries


# 获取股权登记日(B股最后交易日) -> getRightsIssueRegDateShareB


# 获取最后交割日时间序列 -> getLastDeliveryDateSeries


# 获取最后交割日 -> getLastDeliveryDate


# 获取最后交割日(支持历史)时间序列 -> getLdDateNewSeries


# 获取最后交割日(支持历史) -> getLdDateNew


# 获取交割月份时间序列 -> getDlMonthSeries


# 获取交割月份 -> getDlMonth


# 获取挂牌基准价时间序列 -> getLPriceSeries


# 获取挂牌基准价 -> getLPrice


# 获取期货交易手续费时间序列 -> getTransactionFeeSeries


# 获取期货交易手续费 -> getTransactionFee


# 获取期货交割手续费时间序列 -> getDeliveryFeeSeries


# 获取期货交割手续费 -> getDeliveryFee


# 获取期货平今手续费时间序列 -> getTodayPositionFeeSeries


# 获取期货平今手续费 -> getTodayPositionFee


# 获取交易品种时间序列 -> getScCodeSeries


# 获取交易品种 -> getScCode


# 获取交易保证金时间序列 -> getMarginSeries


# 获取交易保证金 -> getMargin


# 获取最初交易保证金时间序列 -> getFtMarginsSeries


# 获取最初交易保证金 -> getFtMargins


# 获取权益乘数(剔除客户交易保证金)时间序列 -> getStmNoteSec1853Series


# 获取权益乘数(剔除客户交易保证金) -> getStmNoteSec1853


# 获取期货多头保证金(支持历史)时间序列 -> getLongMarginSeries


# 获取期货多头保证金(支持历史) -> getLongMargin


# 获取期货空头保证金(支持历史)时间序列 -> getShortMarginSeries


# 获取期货空头保证金(支持历史) -> getShortMargin


# 获取报价单位时间序列 -> getPunItSeries


# 获取报价单位 -> getPunIt


# 获取涨跌幅限制时间序列 -> getChangeLtSeries


# 获取涨跌幅限制 -> getChangeLt


# 获取涨跌幅限制(支持历史)时间序列 -> getChangeLtNewSeries


# 获取涨跌幅限制(支持历史) -> getChangeLtNew


# 获取最小变动价位时间序列 -> getMfPriceSeries


# 获取最小变动价位 -> getMfPrice


# 获取最小变动价位(支持历史)时间序列 -> getMfPrice1Series


# 获取最小变动价位(支持历史) -> getMfPrice1


# 获取标准合约上市日时间序列 -> getContractIssueDateSeries


# 获取标准合约上市日 -> getContractIssueDate


# 获取合约乘数时间序列 -> getExeRatioSeries


# 获取合约乘数 -> getExeRatio


# 获取合约月份说明时间序列 -> getCdMonthsSeries


# 获取合约月份说明 -> getCdMonths


# 获取最新交易时间说明时间序列 -> getTHoursSeries


# 获取最新交易时间说明 -> getTHours


# 获取交割日期说明时间序列 -> getDDateSeries


# 获取交割日期说明 -> getDDate


# 获取月合约代码时间序列 -> getTradeHisCodeSeries


# 获取月合约代码 -> getTradeHisCode


# 获取期货合约所属行业时间序列 -> getIndustryFuSeries


# 获取期货合约所属行业 -> getIndustryFu


# 获取期权代码(指定行权价)时间序列 -> getOptionsTradeCodeSeries


# 获取期权代码(指定行权价) -> getOptionsTradeCode


# 获取平值期权代码时间序列 -> getAtmCodeSeries


# 获取平值期权代码 -> getAtmCode


# 获取期权交易代码时间序列 -> getTradeCodeSeries


# 获取期权交易代码 -> getTradeCode


# 获取标的代码时间序列 -> getUsCodeSeries


# 获取标的代码 -> getUsCode


# 获取标的简称时间序列 -> getUsNameSeries


# 获取标的简称 -> getUsName


# 获取基础资产/标的类型时间序列 -> getUsTypeSeries


# 获取基础资产/标的类型 -> getUsType


# 获取行权方式时间序列 -> getExeModeSeries


# 获取行权方式 -> getExeMode


# 获取行权类型时间序列 -> getExeTypeSeries


# 获取行权类型 -> getExeType


# 获取行权价格时间序列 -> getExePriceSeries


# 获取行权价格 -> getExePrice


# 获取股权激励行权价格时间序列 -> getHolderPriceStockBasedCompensationSeries


# 获取股权激励行权价格 -> getHolderPriceStockBasedCompensation


# 获取期权维持保证金(支持历史)时间序列 -> getMainTMarginSeries


# 获取期权维持保证金(支持历史) -> getMainTMargin


# 获取总存续期时间序列 -> getTotalTmSeries


# 获取总存续期 -> getTotalTm


# 获取起始交易日期时间序列 -> getStartDateSeries


# 获取起始交易日期 -> getStartDate


# 获取起始行权日期时间序列 -> getExeStartDateSeries


# 获取起始行权日期 -> getExeStartDate


# 获取最后行权日期时间序列 -> getExeEnddateSeries


# 获取最后行权日期 -> getExeEnddate


# 获取交割方式时间序列 -> getSettlementMethodSeries


# 获取交割方式 -> getSettlementMethod


# 获取前收盘价时间序列 -> getPreCloseSeries


# 获取前收盘价 -> getPreClose


# 获取区间前收盘价时间序列 -> getPreClosePerSeries


# 获取区间前收盘价 -> getPreClosePer


# 获取标的前收盘价时间序列 -> getUsPreCloseSeries


# 获取标的前收盘价 -> getUsPreClose


# 获取正股区间前收盘价时间序列 -> getCbPqStockPreCloseSeries


# 获取正股区间前收盘价 -> getCbPqStockPreClose


# 获取开盘价时间序列 -> getOpenSeries


# 获取开盘价 -> getOpen


# 获取开盘价(不前推)时间序列 -> getOpen3Series


# 获取开盘价(不前推) -> getOpen3


# 获取区间开盘价时间序列 -> getOpenPerSeries


# 获取区间开盘价 -> getOpenPer


# 获取标的开盘价时间序列 -> getUsOpenSeries


# 获取标的开盘价 -> getUsOpen


# 获取正股区间开盘价时间序列 -> getCbPqStockOpenSeries


# 获取正股区间开盘价 -> getCbPqStockOpen


# 获取上市首日开盘价时间序列 -> getIpoOpenSeries


# 获取上市首日开盘价 -> getIpoOpen


# 获取最高价时间序列 -> getHighSeries


# 获取最高价 -> getHigh


# 获取最高价(不前推)时间序列 -> getHigh3Series


# 获取最高价(不前推) -> getHigh3


# 获取区间最高价时间序列 -> getHighPerSeries


# 获取区间最高价 -> getHighPer


# 获取区间最高价日时间序列 -> getHighDatePerSeries


# 获取区间最高价日 -> getHighDatePer


# 获取标的最高价时间序列 -> getUsHighSeries


# 获取标的最高价 -> getUsHigh


# 获取区间自最高价的最大跌幅时间序列 -> getPctChgLowestPerSeries


# 获取区间自最高价的最大跌幅 -> getPctChgLowestPer


# 获取正股区间最高价时间序列 -> getCbPqStockHighSeries


# 获取正股区间最高价 -> getCbPqStockHigh


# 获取上市首日最高价时间序列 -> getIpoHighSeries


# 获取上市首日最高价 -> getIpoHigh


# 获取被剔除的最高价申报量占比时间序列 -> getPohQeSeries


# 获取被剔除的最高价申报量占比 -> getPohQe


# 获取最新价较区间最高价跌幅(回撤)时间序列 -> getPctChgLowPerSeries


# 获取最新价较区间最高价跌幅(回撤) -> getPctChgLowPer


# 获取LN(最近一个月最高价/最近一个月最低价)_PIT时间序列 -> getTechLnHighLow20DSeries


# 获取LN(最近一个月最高价/最近一个月最低价)_PIT -> getTechLnHighLow20D


# 获取最低价时间序列 -> getLowSeries


# 获取最低价 -> getLow


# 获取最低价(不前推)时间序列 -> getLow3Series


# 获取最低价(不前推) -> getLow3


# 获取区间最低价时间序列 -> getLowPerSeries


# 获取区间最低价 -> getLowPer


# 获取区间最低价日时间序列 -> getLowDatePerSeries


# 获取区间最低价日 -> getLowDatePer


# 获取标的最低价时间序列 -> getUsLowSeries


# 获取标的最低价 -> getUsLow


# 获取区间自最低价的最大涨幅时间序列 -> getPctChgHighestPerSeries


# 获取区间自最低价的最大涨幅 -> getPctChgHighestPer


# 获取正股区间最低价时间序列 -> getCbPqStockLowSeries


# 获取正股区间最低价 -> getCbPqStockLow


# 获取上市首日最低价时间序列 -> getIpoLowSeries


# 获取上市首日最低价 -> getIpoLow


# 获取预测涨跌幅(评级日,最低价)时间序列 -> getEstPctChangeSeries


# 获取预测涨跌幅(评级日,最低价) -> getEstPctChange


# 获取收盘价时间序列 -> getCloseSeries


# 获取收盘价 -> getClose


# 获取收盘价(支持定点复权)时间序列 -> getClose2Series


# 获取收盘价(支持定点复权) -> getClose2


# 获取收盘价(不前推)时间序列 -> getClose3Series


# 获取收盘价(不前推) -> getClose3


# 获取收盘价(23:30)时间序列 -> getCloseFxSeries


# 获取收盘价(23:30) -> getCloseFx


# 获取收盘价(美元)时间序列 -> getCloseUsdSeries


# 获取收盘价(美元) -> getCloseUsd


# 获取收盘价(夜盘)时间序列 -> getCloseNightSeries


# 获取收盘价(夜盘) -> getCloseNight


# 获取收盘价标准差时间序列 -> getRiskStDevCloseSeries


# 获取收盘价标准差 -> getRiskStDevClose


# 获取收盘价(全价)时间序列 -> getDirtyPriceSeries


# 获取收盘价(全价) -> getDirtyPrice


# 获取收盘价(净价)时间序列 -> getCleanPriceSeries


# 获取收盘价(净价) -> getCleanPrice


# 获取收盘价久期时间序列 -> getDurationSeries


# 获取收盘价久期 -> getDuration


# 获取收盘价修正久期时间序列 -> getModifiedDurationSeries


# 获取收盘价修正久期 -> getModifiedDuration


# 获取收盘价凸性时间序列 -> getConvexitySeries


# 获取收盘价凸性 -> getConvexity


# 获取区间收盘价时间序列 -> getClosePerSeries


# 获取区间收盘价 -> getClosePer


# 获取N日收盘价1/4分位数时间序列 -> get1StQuartIleSeries


# 获取N日收盘价1/4分位数 -> get1StQuartIle


# 获取N日收盘价中位数时间序列 -> getMedianSeries


# 获取N日收盘价中位数 -> getMedian


# 获取N日收盘价3/4分位数时间序列 -> get3RdQuartIleSeries


# 获取N日收盘价3/4分位数 -> get3RdQuartIle


# 获取标的收盘价时间序列 -> getUsCloseSeries


# 获取标的收盘价 -> getUsClose


# 获取5日收盘价三重指数平滑移动平均指标_PIT时间序列 -> getTechTrix5Series


# 获取5日收盘价三重指数平滑移动平均指标_PIT -> getTechTrix5


# 获取推N日收盘价(债券)时间序列 -> getNQOriginCloseSeries


# 获取推N日收盘价(债券) -> getNQOriginClose


# 获取推N日收盘价(当日结算价)时间序列 -> getNQCloseSeries


# 获取推N日收盘价(当日结算价) -> getNQClose


# 获取10日收盘价三重指数平滑移动平均指标_PIT时间序列 -> getTechTrix10Series


# 获取10日收盘价三重指数平滑移动平均指标_PIT -> getTechTrix10


# 获取涨跌幅(收盘价)时间序列 -> getPctChangeCloseSeries


# 获取涨跌幅(收盘价) -> getPctChangeClose


# 获取正股区间收盘价时间序列 -> getCbPqStockCloseSeries


# 获取正股区间收盘价 -> getCbPqStockClose


# 获取区间最高收盘价时间序列 -> getMaxClosePerSeries


# 获取区间最高收盘价 -> getMaxClosePer


# 获取区间最低收盘价时间序列 -> getMinClosePerSeries


# 获取区间最低收盘价 -> getMinClosePer


# 获取区间最高收盘价日时间序列 -> getMaxCloseDatePerSeries


# 获取区间最高收盘价日 -> getMaxCloseDatePer


# 获取区间最低收盘价日时间序列 -> getMinCloseDatePerSeries


# 获取区间最低收盘价日 -> getMinCloseDatePer


# 获取N日日均收盘价(算术平均)时间序列 -> getAvgClosePerSeries


# 获取N日日均收盘价(算术平均) -> getAvgClosePer


# 获取上市首日收盘价时间序列 -> getIpoCloseSeries


# 获取上市首日收盘价 -> getIpoClose


# 获取新股开板日收盘价时间序列 -> getIpoLimitUpOpenDateCloseSeries


# 获取新股开板日收盘价 -> getIpoLimitUpOpenDateClose


# 获取BBI除以收盘价_PIT时间序列 -> getTechBBicSeries


# 获取BBI除以收盘价_PIT -> getTechBBic


# 获取上证固收平台收盘价时间序列 -> getCloseFixedIncomeSeries


# 获取上证固收平台收盘价 -> getCloseFixedIncome


# 获取正股区间最高收盘价时间序列 -> getCbPqStockHighCloseSeries


# 获取正股区间最高收盘价 -> getCbPqStockHighClose


# 获取正股区间最低收盘价时间序列 -> getCbPqStockLowCloseSeries


# 获取正股区间最低收盘价 -> getCbPqStockLowClose


# 获取成交量时间序列 -> getVolumeSeries


# 获取成交量 -> getVolume


# 获取成交量(含大宗交易)时间序列 -> getVolumEBTInSeries


# 获取成交量(含大宗交易) -> getVolumEBTIn


# 获取成交量比上交易日增减时间序列 -> getOiVolumeCSeries


# 获取成交量比上交易日增减 -> getOiVolumeC


# 获取成交量进榜会员名称时间序列 -> getOiVNameSeries


# 获取成交量进榜会员名称 -> getOiVName


# 获取成交量认沽认购比率时间序列 -> getVolumeRatioSeries


# 获取成交量认沽认购比率 -> getVolumeRatio


# 获取成交量的5日指数移动平均_PIT时间序列 -> getTechVemA5Series


# 获取成交量的5日指数移动平均_PIT -> getTechVemA5


# 获取成交量的10日指数移动平均_PIT时间序列 -> getTechVemA10Series


# 获取成交量的10日指数移动平均_PIT -> getTechVemA10


# 获取成交量的12日指数移动平均_PIT时间序列 -> getTechVemA12Series


# 获取成交量的12日指数移动平均_PIT -> getTechVemA12


# 获取成交量的26日指数移动平均_PIT时间序列 -> getTechVemA26Series


# 获取成交量的26日指数移动平均_PIT -> getTechVemA26


# 获取成交量量指数平滑异同移动平均线_PIT时间序列 -> getTechVmaCdSeries


# 获取成交量量指数平滑异同移动平均线_PIT -> getTechVmaCd


# 获取成交量比率_PIT时间序列 -> getTechVrSeries


# 获取成交量比率_PIT -> getTechVr


# 获取成交量震荡_PIT时间序列 -> getTechVosCSeries


# 获取成交量震荡_PIT -> getTechVosC


# 获取正成交量指标_PIT时间序列 -> getTechPvISeries


# 获取正成交量指标_PIT -> getTechPvI


# 获取负成交量指标_PIT时间序列 -> getTechNViSeries


# 获取负成交量指标_PIT -> getTechNVi


# 获取盘后成交量时间序列 -> getVolumeAHtSeries


# 获取盘后成交量 -> getVolumeAHt


# 获取区间成交量时间序列 -> getVolPerSeries


# 获取区间成交量 -> getVolPer


# 获取区间成交量(含大宗交易)时间序列 -> getPqBlockTradeVolumeSeries


# 获取区间成交量(含大宗交易) -> getPqBlockTradeVolume


# 获取N日成交量时间序列 -> getVolNdSeries


# 获取N日成交量 -> getVolNd


# 获取标的成交量时间序列 -> getUsVolumeSeries


# 获取标的成交量 -> getUsVolume


# 获取会员成交量时间序列 -> getOiVolumeSeries


# 获取会员成交量 -> getOiVolume


# 获取品种成交量时间序列 -> getOptionVolumeSeries


# 获取品种成交量 -> getOptionVolume


# 获取认购成交量时间序列 -> getCallVolumeSeries


# 获取认购成交量 -> getCallVolume


# 获取认沽成交量时间序列 -> getPutVolumeSeries


# 获取认沽成交量 -> getPutVolume


# 获取10日成交量标准差_PIT时间序列 -> getTechVsTd10Series


# 获取10日成交量标准差_PIT -> getTechVsTd10


# 获取20日成交量标准差_PIT时间序列 -> getTechVsTd20Series


# 获取20日成交量标准差_PIT -> getTechVsTd20


# 获取正股区间成交量时间序列 -> getCbPqStockVolSeries


# 获取正股区间成交量 -> getCbPqStockVol


# 获取区间日均成交量时间序列 -> getAvgVolPerSeries


# 获取区间日均成交量 -> getAvgVolPer


# 获取区间盘后成交量时间序列 -> getPqVolumeAHtSeries


# 获取区间盘后成交量 -> getPqVolumeAHt


# 获取卖空量占成交量比率时间序列 -> getShortSellVolumePctSeries


# 获取卖空量占成交量比率 -> getShortSellVolumePct


# 获取VSTD成交量标准差时间序列 -> getVsTdSeries


# 获取VSTD成交量标准差 -> getVsTd


# 获取上市首日成交量时间序列 -> getIpoListDayVolumeSeries


# 获取上市首日成交量 -> getIpoListDayVolume


# 获取开盘集合竞价成交量时间序列 -> getOpenAuctionVolumeSeries


# 获取开盘集合竞价成交量 -> getOpenAuctionVolume


# 获取上证固收平台成交量时间序列 -> getVolumeFixedIncomeSeries


# 获取上证固收平台成交量 -> getVolumeFixedIncome


# 获取成交额时间序列 -> getAmtSeries


# 获取成交额 -> getAmt


# 获取成交额(含大宗交易)时间序列 -> getAmountBtInSeries


# 获取成交额(含大宗交易) -> getAmountBtIn


# 获取成交额惯性_PIT时间序列 -> getTechAmount1M60Series


# 获取成交额惯性_PIT -> getTechAmount1M60


# 获取盘后成交额时间序列 -> getAmountAHtSeries


# 获取盘后成交额 -> getAmountAHt


# 获取区间成交额时间序列 -> getAmtPerSeries


# 获取区间成交额 -> getAmtPer


# 获取区间成交额(含大宗交易)时间序列 -> getPqBlockTradeAmountsSeries


# 获取区间成交额(含大宗交易) -> getPqBlockTradeAmounts


# 获取N日成交额时间序列 -> getAmtNdSeries


# 获取N日成交额 -> getAmtNd


# 获取标的成交额时间序列 -> getUsAmountSeries


# 获取标的成交额 -> getUsAmount


# 获取品种成交额时间序列 -> getOptionAmountSeries


# 获取品种成交额 -> getOptionAmount


# 获取认购成交额时间序列 -> getCallAmountSeries


# 获取认购成交额 -> getCallAmount


# 获取认沽成交额时间序列 -> getPutAmountSeries


# 获取认沽成交额 -> getPutAmount


# 获取正股区间成交额时间序列 -> getCbPqStockAmNtSeries


# 获取正股区间成交额 -> getCbPqStockAmNt


# 获取区间日均成交额时间序列 -> getAvgAmtPerSeries


# 获取区间日均成交额 -> getAvgAmtPer


# 获取区间盘后成交额时间序列 -> getPqAmountAHtSeries


# 获取区间盘后成交额 -> getPqAmountAHt


# 获取上市首日成交额时间序列 -> getIpoVolumeSeries


# 获取上市首日成交额 -> getIpoVolume


# 获取开盘集合竞价成交额时间序列 -> getOpenAuctionAmountSeries


# 获取开盘集合竞价成交额 -> getOpenAuctionAmount


# 获取成交笔数时间序列 -> getDealNumSeries


# 获取成交笔数 -> getDealNum


# 获取上证固收平台成交笔数时间序列 -> getDealNumFixedIncomeSeries


# 获取上证固收平台成交笔数 -> getDealNumFixedIncome


# 获取涨跌时间序列 -> getChgSeries


# 获取涨跌 -> getChg


# 获取涨跌幅时间序列 -> getPctChgSeries


# 获取涨跌幅 -> getPctChg


# 获取涨跌幅(债券)时间序列 -> getPctChgBSeries


# 获取涨跌幅(债券) -> getPctChgB


# 获取涨跌(结算价)时间序列 -> getChgSettlementSeries


# 获取涨跌(结算价) -> getChgSettlement


# 获取涨跌幅(结算价)时间序列 -> getPctChgSettlementSeries


# 获取涨跌幅(结算价) -> getPctChgSettlement


# 获取涨跌停状态时间序列 -> getMaxUpOrDownSeries


# 获取涨跌停状态 -> getMaxUpOrDown


# 获取涨跌(中债)时间序列 -> getDQChangeCnBdSeries


# 获取涨跌(中债) -> getDQChangeCnBd


# 获取涨跌幅(中债)时间序列 -> getDQPctChangeCnBdSeries


# 获取涨跌幅(中债) -> getDQPctChangeCnBd


# 获取区间涨跌时间序列 -> getChgPerSeries


# 获取区间涨跌 -> getChgPer


# 获取区间涨跌幅时间序列 -> getPctChgPerSeries


# 获取区间涨跌幅 -> getPctChgPer


# 获取区间涨跌幅(包含上市首日涨跌幅)时间序列 -> getPctChgPer2Series


# 获取区间涨跌幅(包含上市首日涨跌幅) -> getPctChgPer2


# 获取N日涨跌幅时间序列 -> getPctChgNdSeries


# 获取N日涨跌幅 -> getPctChgNd


# 获取区间涨跌(结算价)时间序列 -> getFsPqChangeSettlementSeries


# 获取区间涨跌(结算价) -> getFsPqChangeSettlement


# 获取区间涨跌幅(结算价)时间序列 -> getFsPqPctChangeSettlementSeries


# 获取区间涨跌幅(结算价) -> getFsPqPctChangeSettlement


# 获取估算涨跌幅时间序列 -> getWestReturnSeries


# 获取估算涨跌幅 -> getWestReturn


# 获取估算涨跌幅误差时间序列 -> getWestReturnErrorSeries


# 获取估算涨跌幅误差 -> getWestReturnError


# 获取标的涨跌时间序列 -> getUsChangeSeries


# 获取标的涨跌 -> getUsChange


# 获取标的涨跌幅时间序列 -> getUsPctChangeSeries


# 获取标的涨跌幅 -> getUsPctChange


# 获取近5日涨跌幅时间序列 -> getPctChg5DSeries


# 获取近5日涨跌幅 -> getPctChg5D


# 获取近1月涨跌幅时间序列 -> getPctChg1MSeries


# 获取近1月涨跌幅 -> getPctChg1M


# 获取近3月涨跌幅时间序列 -> getPctChg3MSeries


# 获取近3月涨跌幅 -> getPctChg3M


# 获取近6月涨跌幅时间序列 -> getPctChg6MSeries


# 获取近6月涨跌幅 -> getPctChg6M


# 获取近1年涨跌幅时间序列 -> getPctChg1YSeries


# 获取近1年涨跌幅 -> getPctChg1Y


# 获取重仓股涨跌幅时间序列 -> getPrtHeavilyHeldStocksPerChangeSeries


# 获取重仓股涨跌幅 -> getPrtHeavilyHeldStocksPerChange


# 获取净值异常涨跌幅说明时间序列 -> getFundAbnormalNavFluctuationSeries


# 获取净值异常涨跌幅说明 -> getFundAbnormalNavFluctuation


# 获取正股区间涨跌时间序列 -> getCbPqStockChgSeries


# 获取正股区间涨跌 -> getCbPqStockChg


# 获取正股区间涨跌幅时间序列 -> getCbPqStockPctChgSeries


# 获取正股区间涨跌幅 -> getCbPqStockPctChg


# 获取N日日均涨跌幅时间序列 -> getAvgPctChgNdSeries


# 获取N日日均涨跌幅 -> getAvgPctChgNd


# 获取近10日涨跌幅时间序列 -> getPctChg10DSeries


# 获取近10日涨跌幅 -> getPctChg10D


# 获取上市首日涨跌幅时间序列 -> getIpoPctChangeSeries


# 获取上市首日涨跌幅 -> getIpoPctChange


# 获取重仓债券涨跌幅时间序列 -> getPrtHeavilyHeldBondsPerChangeSeries


# 获取重仓债券涨跌幅 -> getPrtHeavilyHeldBondsPerChange


# 获取重仓基金涨跌幅时间序列 -> getPrtHeavilyHeldFundPerChangeSeries


# 获取重仓基金涨跌幅 -> getPrtHeavilyHeldFundPerChange


# 获取相对发行价涨跌时间序列 -> getRelIpoChgSeries


# 获取相对发行价涨跌 -> getRelIpoChg


# 获取相对发行价涨跌幅时间序列 -> getRelIpoPctChgSeries


# 获取相对发行价涨跌幅 -> getRelIpoPctChg


# 获取上市后N日涨跌幅时间序列 -> getIpoNpcTChangeSeries


# 获取上市后N日涨跌幅 -> getIpoNpcTChange


# 获取新股开板日涨跌幅时间序列 -> getIpoLimitUpOpenDatePctChangeSeries


# 获取新股开板日涨跌幅 -> getIpoLimitUpOpenDatePctChange


# 获取区间相对指数涨跌幅时间序列 -> getRelPctChangeSeries


# 获取区间相对指数涨跌幅 -> getRelPctChange


# 获取相对大盘区间涨跌幅时间序列 -> getPqRelPctChangeSeries


# 获取相对大盘区间涨跌幅 -> getPqRelPctChange


# 获取相对大盘N日涨跌幅时间序列 -> getNQRelPctChangeSeries


# 获取相对大盘N日涨跌幅 -> getNQRelPctChange


# 获取年迄今相对指数涨跌幅时间序列 -> getPqRelPctChangeYTdSeries


# 获取年迄今相对指数涨跌幅 -> getPqRelPctChangeYTd


# 获取近5日相对指数涨跌幅时间序列 -> getPqRelPctChange5DSeries


# 获取近5日相对指数涨跌幅 -> getPqRelPctChange5D


# 获取近1月相对指数涨跌幅时间序列 -> getPqRelPctChange1MSeries


# 获取近1月相对指数涨跌幅 -> getPqRelPctChange1M


# 获取近3月相对指数涨跌幅时间序列 -> getPqRelPctChange3MSeries


# 获取近3月相对指数涨跌幅 -> getPqRelPctChange3M


# 获取近6月相对指数涨跌幅时间序列 -> getPqRelPctChange6MSeries


# 获取近6月相对指数涨跌幅 -> getPqRelPctChange6M


# 获取近1年相对指数涨跌幅时间序列 -> getPqRelPctChange1YSeries


# 获取近1年相对指数涨跌幅 -> getPqRelPctChange1Y


# 获取本月至今相对指数涨跌幅时间序列 -> getPqRelPctChangeMTdSeries


# 获取本月至今相对指数涨跌幅 -> getPqRelPctChangeMTd


# 获取季度至今相对指数涨跌幅时间序列 -> getPqRelRelPctChangeMTdSeries


# 获取季度至今相对指数涨跌幅 -> getPqRelRelPctChangeMTd


# 获取近10日相对指数涨跌幅时间序列 -> getPqRelPctChange10DSeries


# 获取近10日相对指数涨跌幅 -> getPqRelPctChange10D


# 获取振幅时间序列 -> getSwingSeries


# 获取振幅 -> getSwing


# 获取区间振幅时间序列 -> getSwingPerSeries


# 获取区间振幅 -> getSwingPer


# 获取N日振幅时间序列 -> getSwingNdSeries


# 获取N日振幅 -> getSwingNd


# 获取标的振幅时间序列 -> getUsSwingSeries


# 获取标的振幅 -> getUsSwing


# 获取正股区间振幅时间序列 -> getCbPqStockSwingSeries


# 获取正股区间振幅 -> getCbPqStockSwing


# 获取区间日均振幅时间序列 -> getAvgSwingPerSeries


# 获取区间日均振幅 -> getAvgSwingPer


# 获取均价时间序列 -> getVWapSeries


# 获取均价 -> getVWap


# 获取标的均价时间序列 -> getUsAvgPriceSeries


# 获取标的均价 -> getUsAvgPrice


# 获取发行前均价时间序列 -> getIpoPrePriceSeries


# 获取发行前均价 -> getIpoPrePrice


# 获取正股区间均价时间序列 -> getCbPqStockAvgSeries


# 获取正股区间均价 -> getCbPqStockAvg


# 获取区间成交均价时间序列 -> getVWapPerSeries


# 获取区间成交均价 -> getVWapPer


# 获取区间成交均价(可复权)时间序列 -> getPqAvgPrice2Series


# 获取区间成交均价(可复权) -> getPqAvgPrice2


# 获取N日成交均价时间序列 -> getNQAvgPriceSeries


# 获取N日成交均价 -> getNQAvgPrice


# 获取是否为算术平均价时间序列 -> getClauseResetReferencePriceIsAnVerAgeSeries


# 获取是否为算术平均价 -> getClauseResetReferencePriceIsAnVerAge


# 获取上市首日成交均价时间序列 -> getIpoAvgPriceSeries


# 获取上市首日成交均价 -> getIpoAvgPrice


# 获取上证固收平台平均价时间序列 -> getAvgPriceFixedIncomeSeries


# 获取上证固收平台平均价 -> getAvgPriceFixedIncome


# 获取新股开板日成交均价时间序列 -> getIpoLimitUpOpenDateAvgPriceSeries


# 获取新股开板日成交均价 -> getIpoLimitUpOpenDateAvgPrice


# 获取复权因子时间序列 -> getAdjFactorSeries


# 获取复权因子 -> getAdjFactor


# 获取基金净值复权因子时间序列 -> getNavAdjFactorSeries


# 获取基金净值复权因子 -> getNavAdjFactor


# 获取换手率时间序列 -> getTurnSeries


# 获取换手率 -> getTurn


# 获取换手率(基准.自由流通股本)时间序列 -> getFreeTurnSeries


# 获取换手率(基准.自由流通股本) -> getFreeTurn


# 获取换手率相对波动率_PIT时间序列 -> getTechTurnoverRateVolatility20Series


# 获取换手率相对波动率_PIT -> getTechTurnoverRateVolatility20


# 获取区间换手率时间序列 -> getTurnPerSeries


# 获取区间换手率 -> getTurnPer


# 获取区间换手率(基准.自由流通股本)时间序列 -> getTurnFreePerSeries


# 获取区间换手率(基准.自由流通股本) -> getTurnFreePer


# 获取N日换手率时间序列 -> getTurnNdSeries


# 获取N日换手率 -> getTurnNd


# 获取标的换手率时间序列 -> getUsTurnSeries


# 获取标的换手率 -> getUsTurn


# 获取3个月换手率对数平均_PIT时间序列 -> getTechSToQSeries


# 获取3个月换手率对数平均_PIT -> getTechSToQ


# 获取正股区间换手率时间序列 -> getCbPqStockTurnoverSeries


# 获取正股区间换手率 -> getCbPqStockTurnover


# 获取区间日均换手率时间序列 -> getPqAvgTurn2Series


# 获取区间日均换手率 -> getPqAvgTurn2


# 获取区间日均换手率(剔除无成交日期)时间序列 -> getAvgTurnPerSeries


# 获取区间日均换手率(剔除无成交日期) -> getAvgTurnPer


# 获取区间日均换手率(基准.自由流通股本)时间序列 -> getAvgTurnFreePerSeries


# 获取区间日均换手率(基准.自由流通股本) -> getAvgTurnFreePer


# 获取N日日均换手率时间序列 -> getAvgTurnNdSeries


# 获取N日日均换手率 -> getAvgTurnNd


# 获取上市首日换手率时间序列 -> getIpoTurnSeries


# 获取上市首日换手率 -> getIpoTurn


# 获取5日平均换手率_PIT时间序列 -> getTechTurnoverRate5Series


# 获取5日平均换手率_PIT -> getTechTurnoverRate5


# 获取12个月换手率对数平均_PIT时间序列 -> getTechSToASeries


# 获取12个月换手率对数平均_PIT -> getTechSToA


# 获取5日平均换手率/120日平均换手率_PIT时间序列 -> getTechTurn5DTurn120Series


# 获取5日平均换手率/120日平均换手率_PIT -> getTechTurn5DTurn120


# 获取上市后N日换手率时间序列 -> getIpoNTurnSeries


# 获取上市后N日换手率 -> getIpoNTurn


# 获取10日平均换手率_PIT时间序列 -> getTechTurnoverRate10Series


# 获取10日平均换手率_PIT -> getTechTurnoverRate10


# 获取20日平均换手率_PIT时间序列 -> getTechTurnoverRate20Series


# 获取20日平均换手率_PIT -> getTechTurnoverRate20


# 获取60日平均换手率_PIT时间序列 -> getTechTurnoverRate60Series


# 获取60日平均换手率_PIT -> getTechTurnoverRate60


# 获取10日平均换手率/120日平均换手率_PIT时间序列 -> getTechTurn10DTurn120Series


# 获取10日平均换手率/120日平均换手率_PIT -> getTechTurn10DTurn120


# 获取20日平均换手率/120日平均换手率_PIT时间序列 -> getTechTurn20DTurn120Series


# 获取20日平均换手率/120日平均换手率_PIT -> getTechTurn20DTurn120


# 获取正股区间平均换手率时间序列 -> getCbPqStockAveTurnoverSeries


# 获取正股区间平均换手率 -> getCbPqStockAveTurnover


# 获取120日平均换手率_PIT时间序列 -> getTechTurnoverRate120Series


# 获取120日平均换手率_PIT -> getTechTurnoverRate120


# 获取240日平均换手率_PIT时间序列 -> getTechTurnoverRate240Series


# 获取240日平均换手率_PIT -> getTechTurnoverRate240


# 获取基金报告期持仓换手率时间序列 -> getStyleRpTTurnSeries


# 获取基金报告期持仓换手率 -> getStyleRpTTurn


# 获取持仓量时间序列 -> getOiSeries


# 获取持仓量 -> getOi


# 获取持仓量变化时间序列 -> getOiChgSeries


# 获取持仓量变化 -> getOiChg


# 获取持仓量(商品指数)时间序列 -> getOiIndexSeries


# 获取持仓量(商品指数) -> getOiIndex


# 获取持仓量变化(商品指数)时间序列 -> getOiChangeSeries


# 获取持仓量变化(商品指数) -> getOiChange


# 获取持仓量(不前推)时间序列 -> getOi3Series


# 获取持仓量(不前推) -> getOi3


# 获取持仓量认沽认购比率时间序列 -> getOiRatioSeries


# 获取持仓量认沽认购比率 -> getOiRatio


# 获取区间持仓量时间序列 -> getOiPerSeries


# 获取区间持仓量 -> getOiPer


# 获取品种持仓量时间序列 -> getOptionOiSeries


# 获取品种持仓量 -> getOptionOi


# 获取认购持仓量时间序列 -> getCallOiSeries


# 获取认购持仓量 -> getCallOi


# 获取认沽持仓量时间序列 -> getPutOiSeries


# 获取认沽持仓量 -> getPutOi


# 获取区间日均持仓量时间序列 -> getAvgOiPerSeries


# 获取区间日均持仓量 -> getAvgOiPer


# 获取持仓额(不计保证金)时间序列 -> getOiAmountNoMarginSeries


# 获取持仓额(不计保证金) -> getOiAmountNoMargin


# 获取持仓额时间序列 -> getOiAmountSeries


# 获取持仓额 -> getOiAmount


# 获取前结算价时间序列 -> getPreSettleSeries


# 获取前结算价 -> getPreSettle


# 获取区间前结算价时间序列 -> getPreSettlePerSeries


# 获取区间前结算价 -> getPreSettlePer


# 获取结算价时间序列 -> getSettleSeries


# 获取结算价 -> getSettle


# 获取结算价(不前推)时间序列 -> getSettle3Series


# 获取结算价(不前推) -> getSettle3


# 获取区间结算价时间序列 -> getSettlePerSeries


# 获取区间结算价 -> getSettlePer


# 获取加权平均结算价修正久期(中债)时间序列 -> getWeightModiDuraSeries


# 获取加权平均结算价修正久期(中债) -> getWeightModiDura


# 获取加权平均结算价利差久期(中债)时间序列 -> getWeightSprDuraSeries


# 获取加权平均结算价利差久期(中债) -> getWeightSprDura


# 获取加权平均结算价利率久期(中债)时间序列 -> getWeightInterestDurationSeries


# 获取加权平均结算价利率久期(中债) -> getWeightInterestDuration


# 获取加权平均结算价基点价值(中债)时间序列 -> getWeightVoBpSeries


# 获取加权平均结算价基点价值(中债) -> getWeightVoBp


# 获取加权平均结算价凸性(中债)时间序列 -> getWeightCNvXTySeries


# 获取加权平均结算价凸性(中债) -> getWeightCNvXTy


# 获取加权平均结算价利差凸性(中债)时间序列 -> getWeightSPrcNxtSeries


# 获取加权平均结算价利差凸性(中债) -> getWeightSPrcNxt


# 获取加权平均结算价利率凸性(中债)时间序列 -> getWeightInterestCNvXTySeries


# 获取加权平均结算价利率凸性(中债) -> getWeightInterestCNvXTy


# 获取区间最低结算价时间序列 -> getLowSettlePerSeries


# 获取区间最低结算价 -> getLowSettlePer


# 获取区间最高结算价时间序列 -> getHighSettlePerSeries


# 获取区间最高结算价 -> getHighSettlePer


# 获取区间最高结算价日时间序列 -> getFsPqHighSwingDateSeries


# 获取区间最高结算价日 -> getFsPqHighSwingDate


# 获取区间最低结算价日时间序列 -> getFsPqLowSwingDateSeries


# 获取区间最低结算价日 -> getFsPqLowSwingDate


# 获取最近交易日期时间序列 -> getLasTradeDaySSeries


# 获取最近交易日期 -> getLasTradeDayS


# 获取最早交易日期时间序列 -> getFirsTradeDaySSeries


# 获取最早交易日期 -> getFirsTradeDayS


# 获取市场最近交易日时间序列 -> getLastTradeDaySeries


# 获取市场最近交易日 -> getLastTradeDay


# 获取交易状态时间序列 -> getTradeStatusSeries


# 获取交易状态 -> getTradeStatus


# 获取总市值时间序列 -> getValMvArdSeries


# 获取总市值 -> getValMvArd


# 获取总市值1时间序列 -> getEvSeries


# 获取总市值1 -> getEv


# 获取总市值2时间序列 -> getMktCapArdSeries


# 获取总市值2 -> getMktCapArd


# 获取总市值1(币种可选)时间序列 -> getEv3Series


# 获取总市值1(币种可选) -> getEv3


# 获取总市值(不可回测)时间序列 -> getMktCapSeries


# 获取总市值(不可回测) -> getMktCap


# 获取总市值(证监会算法)时间序列 -> getMktCapCsrCSeries


# 获取总市值(证监会算法) -> getMktCapCsrC


# 获取总市值/EBITDA(TTM反推法)_PIT时间序列 -> getValMvToeBitDaTtMSeries


# 获取总市值/EBITDA(TTM反推法)_PIT -> getValMvToeBitDaTtM


# 获取总市值/息税折旧及摊销前利润TTM行业相对值_PIT时间序列 -> getValPeBitDaInDuSwTtMSeries


# 获取总市值/息税折旧及摊销前利润TTM行业相对值_PIT -> getValPeBitDaInDuSwTtM


# 获取参考总市值时间序列 -> getMvRefSeries


# 获取参考总市值 -> getMvRef


# 获取指数总市值时间序列 -> getValMvSeries


# 获取指数总市值 -> getValMv


# 获取备考总市值(并购后)时间序列 -> getMamVSeries


# 获取备考总市值(并购后) -> getMamV


# 获取当日总市值/负债总计时间序列 -> getEquityToDebt2Series


# 获取当日总市值/负债总计 -> getEquityToDebt2


# 获取区间日均总市值时间序列 -> getAvgMvPerSeries


# 获取区间日均总市值 -> getAvgMvPer


# 获取所属申万一级行业的总市值/息税折旧及摊销前利润TTM均值_PIT时间序列 -> getValAvgPeBitDaSwSeries


# 获取所属申万一级行业的总市值/息税折旧及摊销前利润TTM均值_PIT -> getValAvgPeBitDaSw


# 获取所属申万一级行业的总市值/息税折旧及摊销前利润TTM标准差_PIT时间序列 -> getValStdPeBitDaSwSeries


# 获取所属申万一级行业的总市值/息税折旧及摊销前利润TTM标准差_PIT -> getValStdPeBitDaSw


# 获取担保证券市值占该证券总市值比重时间序列 -> getMarginMarketValueRatioSeries


# 获取担保证券市值占该证券总市值比重 -> getMarginMarketValueRatio


# 获取流通市值时间序列 -> getValMvCSeries


# 获取流通市值 -> getValMvC


# 获取流通市值(含限售股)时间序列 -> getMktCapFloatSeries


# 获取流通市值(含限售股) -> getMktCapFloat


# 获取自由流通市值时间序列 -> getMktFreeSharesSeries


# 获取自由流通市值 -> getMktFreeShares


# 获取自由流通市值_PIT时间序列 -> getValFloatMvSeries


# 获取自由流通市值_PIT -> getValFloatMv


# 获取对数流通市值_PIT时间序列 -> getValLnFloatMvSeries


# 获取对数流通市值_PIT -> getValLnFloatMv


# 获取区间日均流通市值时间序列 -> getPqAvgMvNonRestrictedSeries


# 获取区间日均流通市值 -> getPqAvgMvNonRestricted


# 获取连续停牌天数时间序列 -> getSUspDaysSeries


# 获取连续停牌天数 -> getSUspDays


# 获取停牌原因时间序列 -> getSUspReasonSeries


# 获取停牌原因 -> getSUspReason


# 获取涨停价时间序列 -> getMaxUpSeries


# 获取涨停价 -> getMaxUp


# 获取跌停价时间序列 -> getMaxDownSeries


# 获取跌停价 -> getMaxDown


# 获取贴水时间序列 -> getDiscountSeries


# 获取贴水 -> getDiscount


# 获取贴水率时间序列 -> getDiscountRatioSeries


# 获取贴水率 -> getDiscountRatio


# 获取区间均贴水时间序列 -> getAvgDiscountPerSeries


# 获取区间均贴水 -> getAvgDiscountPer


# 获取区间均贴水率时间序列 -> getAvgDiscountRatioPerSeries


# 获取区间均贴水率 -> getAvgDiscountRatioPer


# 获取所属指数权重时间序列 -> getIndexWeightSeries


# 获取所属指数权重 -> getIndexWeight


# 获取交收方向(黄金现货)时间序列 -> getDirectionGoldSeries


# 获取交收方向(黄金现货) -> getDirectionGold


# 获取交收量(黄金现货)时间序列 -> getDQuantityGoldSeries


# 获取交收量(黄金现货) -> getDQuantityGold


# 获取开盘集合竞价成交价时间序列 -> getOpenAuctionPriceSeries


# 获取开盘集合竞价成交价 -> getOpenAuctionPrice


# 获取区间收盘最大涨幅时间序列 -> getPctChgHighPerSeries


# 获取区间收盘最大涨幅 -> getPctChgHighPer


# 获取区间交易天数时间序列 -> getTradeDaysPerSeries


# 获取区间交易天数 -> getTradeDaysPer


# 获取区间涨停天数时间序列 -> getLimitUpDaysPerSeries


# 获取区间涨停天数 -> getLimitUpDaysPer


# 获取区间跌停天数时间序列 -> getLimitDownDaysPerSeries


# 获取区间跌停天数 -> getLimitDownDaysPer


# 获取区间上涨天数时间序列 -> getPqUpDaysPerSeries


# 获取区间上涨天数 -> getPqUpDaysPer


# 获取区间下跌天数时间序列 -> getPqDownDaysPerSeries


# 获取区间下跌天数 -> getPqDownDaysPer


# 获取区间报价天数时间序列 -> getQuoteDaysPerSeries


# 获取区间报价天数 -> getQuoteDaysPer


# 获取区间持仓变化时间序列 -> getOiChgPerSeries


# 获取区间持仓变化 -> getOiChgPer


# 获取区间开盘净主动买入额时间序列 -> getMfAmtOpenPerSeries


# 获取区间开盘净主动买入额 -> getMfAmtOpenPer


# 获取区间尾盘净主动买入额时间序列 -> getMfAmtClosePerSeries


# 获取区间尾盘净主动买入额 -> getMfAmtClosePer


# 获取区间净主动买入量时间序列 -> getMfVolPerSeries


# 获取区间净主动买入量 -> getMfVolPer


# 获取区间净主动买入量占比时间序列 -> getMfVolRatioPerSeries


# 获取区间净主动买入量占比 -> getMfVolRatioPer


# 获取区间净主动买入额时间序列 -> getMfAmtPerSeries


# 获取区间净主动买入额 -> getMfAmtPer


# 获取区间净主动买入率(金额)时间序列 -> getMfAmtRatioPerSeries


# 获取区间净主动买入率(金额) -> getMfAmtRatioPer


# 获取区间主力净流入天数时间序列 -> getMfdInFlowDaysSeries


# 获取区间主力净流入天数 -> getMfdInFlowDays


# 获取区间流入额时间序列 -> getMfBuyAmtSeries


# 获取区间流入额 -> getMfBuyAmt


# 获取区间流入量时间序列 -> getMfBuyVolSeries


# 获取区间流入量 -> getMfBuyVol


# 获取区间流出额时间序列 -> getMfSellAmtSeries


# 获取区间流出额 -> getMfSellAmt


# 获取区间流出量时间序列 -> getMfSellVolSeries


# 获取区间流出量 -> getMfSellVol


# 获取区间大宗交易上榜次数时间序列 -> getPqBlockTradeNumSeries


# 获取区间大宗交易上榜次数 -> getPqBlockTradeNum


# 获取区间大宗交易成交总额时间序列 -> getPqBlockTradeAmountSeries


# 获取区间大宗交易成交总额 -> getPqBlockTradeAmount


# 获取区间龙虎榜上榜次数时间序列 -> getPqAbnormalTradeNumSeries


# 获取区间龙虎榜上榜次数 -> getPqAbnormalTradeNum


# 获取区间龙虎榜买入额时间序列 -> getPqAbnormalTradeLpSeries


# 获取区间龙虎榜买入额 -> getPqAbnormalTradeLp


# 获取指定日相近交易日期时间序列 -> getTradeDaySeries


# 获取指定日相近交易日期 -> getTradeDay


# 获取区间净流入额时间序列 -> getPeriodMfNetInFlowSeries


# 获取区间净流入额 -> getPeriodMfNetInFlow


# 获取融资买入额时间序列 -> getMrgLongAmtSeries


# 获取融资买入额 -> getMrgLongAmt


# 获取区间融资买入额时间序列 -> getMrgLongAmtIntSeries


# 获取区间融资买入额 -> getMrgLongAmtInt


# 获取融资偿还额时间序列 -> getMrgLongRepaySeries


# 获取融资偿还额 -> getMrgLongRepay


# 获取区间融资偿还额时间序列 -> getMrgLongRepayIntSeries


# 获取区间融资偿还额 -> getMrgLongRepayInt


# 获取融资余额时间序列 -> getMrgLongBalSeries


# 获取融资余额 -> getMrgLongBal


# 获取区间融资余额均值时间序列 -> getMrgLongBalIntAvgSeries


# 获取区间融资余额均值 -> getMrgLongBalIntAvg


# 获取报告期内债券回购融资余额时间序列 -> getMmRepurchase1Series


# 获取报告期内债券回购融资余额 -> getMmRepurchase1


# 获取报告期末债券回购融资余额时间序列 -> getMmRepurchase2Series


# 获取报告期末债券回购融资余额 -> getMmRepurchase2


# 获取报告期内债券回购融资余额占基金资产净值比例时间序列 -> getMmRepurchase1ToNavSeries


# 获取报告期内债券回购融资余额占基金资产净值比例 -> getMmRepurchase1ToNav


# 获取报告期末债券回购融资余额占基金资产净值比例时间序列 -> getMmRepurchase2ToNavSeries


# 获取报告期末债券回购融资余额占基金资产净值比例 -> getMmRepurchase2ToNav


# 获取融券卖出量时间序列 -> getMrgShortVolSeries


# 获取融券卖出量 -> getMrgShortVol


# 获取区间融券卖出量时间序列 -> getMrgShortVolIntSeries


# 获取区间融券卖出量 -> getMrgShortVolInt


# 获取融券偿还量时间序列 -> getMrgShortVolRepaySeries


# 获取融券偿还量 -> getMrgShortVolRepay


# 获取区间融券偿还量时间序列 -> getMrgShortVolRepayIntSeries


# 获取区间融券偿还量 -> getMrgShortVolRepayInt


# 获取融券卖出额时间序列 -> getMarginSaleTradingAmountSeries


# 获取融券卖出额 -> getMarginSaleTradingAmount


# 获取区间融券卖出额时间序列 -> getMarginShortAmountIntSeries


# 获取区间融券卖出额 -> getMarginShortAmountInt


# 获取融券偿还额时间序列 -> getMarginSaleRepayAmountSeries


# 获取融券偿还额 -> getMarginSaleRepayAmount


# 获取区间融券偿还额时间序列 -> getMarginShortAmountRepayIntSeries


# 获取区间融券偿还额 -> getMarginShortAmountRepayInt


# 获取融券余量时间序列 -> getMrgShortVolBalSeries


# 获取融券余量 -> getMrgShortVolBal


# 获取区间融券余量均值时间序列 -> getMrgShortVolBalIntAvgSeries


# 获取区间融券余量均值 -> getMrgShortVolBalIntAvg


# 获取融券余额时间序列 -> getMrgShortBalSeries


# 获取融券余额 -> getMrgShortBal


# 获取区间融券余额均值时间序列 -> getMrgShortBalIntAvgSeries


# 获取区间融券余额均值 -> getMrgShortBalIntAvg


# 获取全日卖空金额时间序列 -> getShortSellTurnoverSeries


# 获取全日卖空金额 -> getShortSellTurnover


# 获取卖空金额占市场卖空总额比率时间序列 -> getShortSellTurnoverPctSeries


# 获取卖空金额占市场卖空总额比率 -> getShortSellTurnoverPct


# 获取全日卖空股数时间序列 -> getShortSellVolumeSeries


# 获取全日卖空股数 -> getShortSellVolume


# 获取卖空量占香港流通股百分比时间序列 -> getShortSellVolumeToHSharesSeries


# 获取卖空量占香港流通股百分比 -> getShortSellVolumeToHShares


# 获取未平仓卖空数时间序列 -> getShareShortSharesSeries


# 获取未平仓卖空数 -> getShareShortShares


# 获取未平仓卖空金额时间序列 -> getShareShortAmountSeries


# 获取未平仓卖空金额 -> getShareShortAmount


# 获取空头回补天数时间序列 -> getShortSellDaysToCoverSeries


# 获取空头回补天数 -> getShortSellDaysToCover


# 获取流入额时间序列 -> getMfdBuyAmtDSeries


# 获取流入额 -> getMfdBuyAmtD


# 获取净流入额时间序列 -> getMfNetInFlowSeries


# 获取净流入额 -> getMfNetInFlow


# 获取主力净流入额时间序列 -> getMfdInFlowMSeries


# 获取主力净流入额 -> getMfdInFlowM


# 获取主力净流入额占比时间序列 -> getMfdInFlowProportionMSeries


# 获取主力净流入额占比 -> getMfdInFlowProportionM


# 获取开盘主力净流入额时间序列 -> getMfdInFlowOpenMSeries


# 获取开盘主力净流入额 -> getMfdInFlowOpenM


# 获取尾盘主力净流入额时间序列 -> getMfdInFlowCloseMSeries


# 获取尾盘主力净流入额 -> getMfdInFlowCloseM


# 获取开盘主力净流入额占比时间序列 -> getMfdInFlowProportionOpenMSeries


# 获取开盘主力净流入额占比 -> getMfdInFlowProportionOpenM


# 获取尾盘主力净流入额占比时间序列 -> getMfdInFlowProportionCloseMSeries


# 获取尾盘主力净流入额占比 -> getMfdInFlowProportionCloseM


# 获取流出额时间序列 -> getMfdSellAmtDSeries


# 获取流出额 -> getMfdSellAmtD


# 获取流入量时间序列 -> getMfdBuyVolDSeries


# 获取流入量 -> getMfdBuyVolD


# 获取主力净流入量时间序列 -> getMfdBuyVolMSeries


# 获取主力净流入量 -> getMfdBuyVolM


# 获取主力净流入量占比时间序列 -> getMfdVolInFlowProportionMSeries


# 获取主力净流入量占比 -> getMfdVolInFlowProportionM


# 获取开盘主力净流入量时间序列 -> getMfdBuyVolOpenMSeries


# 获取开盘主力净流入量 -> getMfdBuyVolOpenM


# 获取尾盘主力净流入量时间序列 -> getMfdBuyVolCloseMSeries


# 获取尾盘主力净流入量 -> getMfdBuyVolCloseM


# 获取开盘主力净流入量占比时间序列 -> getMfdVolInFlowProportionOpenMSeries


# 获取开盘主力净流入量占比 -> getMfdVolInFlowProportionOpenM


# 获取尾盘主力净流入量占比时间序列 -> getMfdVolInFlowProportionCloseMSeries


# 获取尾盘主力净流入量占比 -> getMfdVolInFlowProportionCloseM


# 获取流出量时间序列 -> getMfdSellVolDSeries


# 获取流出量 -> getMfdSellVolD


# 获取净买入额时间序列 -> getMfdNetBuyAmtSeries


# 获取净买入额 -> getMfdNetBuyAmt


# 获取沪深港股通区间净买入额时间序列 -> getMfpSnInFlowSeries


# 获取沪深港股通区间净买入额 -> getMfpSnInFlow


# 获取净买入量时间序列 -> getMfdNetBuyVolSeries


# 获取净买入量 -> getMfdNetBuyVol


# 获取沪深港股通区间净买入量时间序列 -> getMfpSnInFlowAmtSeries


# 获取沪深港股通区间净买入量 -> getMfpSnInFlowAmt


# 获取沪深港股通区间净买入量(调整)时间序列 -> getMfpSnInFlowAmt2Series


# 获取沪深港股通区间净买入量(调整) -> getMfpSnInFlowAmt2


# 获取流入单数时间序列 -> getMfdBuyOrDSeries


# 获取流入单数 -> getMfdBuyOrD


# 获取流出单数时间序列 -> getMfdSelLordSeries


# 获取流出单数 -> getMfdSelLord


# 获取主动买入额时间序列 -> getMfdBuyAmtASeries


# 获取主动买入额 -> getMfdBuyAmtA


# 获取主动买入额(全单)时间序列 -> getMfdBuyAmtAtSeries


# 获取主动买入额(全单) -> getMfdBuyAmtAt


# 获取净主动买入额时间序列 -> getMfdNetBuyAmtASeries


# 获取净主动买入额 -> getMfdNetBuyAmtA


# 获取净主动买入额(全单)时间序列 -> getMfAmtSeries


# 获取净主动买入额(全单) -> getMfAmt


# 获取净主动买入额占比时间序列 -> getMfdInFlowProportionASeries


# 获取净主动买入额占比 -> getMfdInFlowProportionA


# 获取开盘净主动买入额时间序列 -> getMfAmtOpenSeries


# 获取开盘净主动买入额 -> getMfAmtOpen


# 获取尾盘净主动买入额时间序列 -> getMfAmtCloseSeries


# 获取尾盘净主动买入额 -> getMfAmtClose


# 获取开盘净主动买入额占比时间序列 -> getMfdInFlowProportionOpenASeries


# 获取开盘净主动买入额占比 -> getMfdInFlowProportionOpenA


# 获取尾盘净主动买入额占比时间序列 -> getMfdInFlowProportionCloseASeries


# 获取尾盘净主动买入额占比 -> getMfdInFlowProportionCloseA


# 获取主动卖出额时间序列 -> getMfdSellAmtASeries


# 获取主动卖出额 -> getMfdSellAmtA


# 获取主动卖出额(全单)时间序列 -> getMfdSellAmtAtSeries


# 获取主动卖出额(全单) -> getMfdSellAmtAt


# 获取主动买入量时间序列 -> getMfdBuyVolASeries


# 获取主动买入量 -> getMfdBuyVolA


# 获取主动买入量(全单)时间序列 -> getMfdBuyVolAtSeries


# 获取主动买入量(全单) -> getMfdBuyVolAt


# 获取净主动买入量时间序列 -> getMfdNetBuyVolASeries


# 获取净主动买入量 -> getMfdNetBuyVolA


# 获取净主动买入量(全单)时间序列 -> getMfVolSeries


# 获取净主动买入量(全单) -> getMfVol


# 获取净主动买入量占比时间序列 -> getMfVolRatioSeries


# 获取净主动买入量占比 -> getMfVolRatio


# 获取开盘净主动买入量占比时间序列 -> getMfdVolInFlowProportionOpenASeries


# 获取开盘净主动买入量占比 -> getMfdVolInFlowProportionOpenA


# 获取尾盘净主动买入量占比时间序列 -> getMfdVolInFlowProportionCloseASeries


# 获取尾盘净主动买入量占比 -> getMfdVolInFlowProportionCloseA


# 获取开盘资金净主动买入量时间序列 -> getMfdInFlowVolumeOpenASeries


# 获取开盘资金净主动买入量 -> getMfdInFlowVolumeOpenA


# 获取尾盘资金净主动买入量时间序列 -> getMfdInFlowVolumeCloseASeries


# 获取尾盘资金净主动买入量 -> getMfdInFlowVolumeCloseA


# 获取主动卖出量时间序列 -> getMfdSellVolASeries


# 获取主动卖出量 -> getMfdSellVolA


# 获取主动卖出量(全单)时间序列 -> getMfdSellVolAtSeries


# 获取主动卖出量(全单) -> getMfdSellVolAt


# 获取净主动买入率(金额)时间序列 -> getMfAmtRatioSeries


# 获取净主动买入率(金额) -> getMfAmtRatio


# 获取开盘净主动买入率(金额)时间序列 -> getMfdInFlowRateOpenASeries


# 获取开盘净主动买入率(金额) -> getMfdInFlowRateOpenA


# 获取尾盘净主动买入率(金额)时间序列 -> getMfdInFlowRateCloseASeries


# 获取尾盘净主动买入率(金额) -> getMfdInFlowRateCloseA


# 获取净主动买入率(量)时间序列 -> getMfdVolInFlowRateASeries


# 获取净主动买入率(量) -> getMfdVolInFlowRateA


# 获取开盘净主动买入率(量)时间序列 -> getMfdVolInFlowRateOpenASeries


# 获取开盘净主动买入率(量) -> getMfdVolInFlowRateOpenA


# 获取尾盘净主动买入率(量)时间序列 -> getMfdVolInFlowRateCloseASeries


# 获取尾盘净主动买入率(量) -> getMfdVolInFlowRateCloseA


# 获取主力净流入率(金额)时间序列 -> getMfdInFlowRateMSeries


# 获取主力净流入率(金额) -> getMfdInFlowRateM


# 获取开盘主力净流入率(金额)时间序列 -> getMfdInFlowRateOpenMSeries


# 获取开盘主力净流入率(金额) -> getMfdInFlowRateOpenM


# 获取尾盘主力净流入率(金额)时间序列 -> getMfdInFlowRateCloseMSeries


# 获取尾盘主力净流入率(金额) -> getMfdInFlowRateCloseM


# 获取主力净流入率(量)时间序列 -> getMfdVolInFlowRateMSeries


# 获取主力净流入率(量) -> getMfdVolInFlowRateM


# 获取开盘主力净流入率(量)时间序列 -> getMfdVolInFlowRateOpenMSeries


# 获取开盘主力净流入率(量) -> getMfdVolInFlowRateOpenM


# 获取尾盘主力净流入率(量)时间序列 -> getMfdVolInFlowRateCloseMSeries


# 获取尾盘主力净流入率(量) -> getMfdVolInFlowRateCloseM


# 获取沪深港股通买入金额时间序列 -> getMfdSnBuyAmtSeries


# 获取沪深港股通买入金额 -> getMfdSnBuyAmt


# 获取沪深港股通卖出金额时间序列 -> getMfdSnSellAmtSeries


# 获取沪深港股通卖出金额 -> getMfdSnSellAmt


# 获取沪深港股通净买入金额时间序列 -> getMfdSnInFlowSeries


# 获取沪深港股通净买入金额 -> getMfdSnInFlow


# 获取沪深港股通区间净流入天数时间序列 -> getMfpSnInFlowDaysSeries


# 获取沪深港股通区间净流入天数 -> getMfpSnInFlowDays


# 获取沪深港股通区间净流出天数时间序列 -> getMfpSnOutflowDaysSeries


# 获取沪深港股通区间净流出天数 -> getMfpSnOutflowDays


# 获取沪深港股通持续净流入天数时间序列 -> getMfnSnInFlowDaysSeries


# 获取沪深港股通持续净流入天数 -> getMfnSnInFlowDays


# 获取沪深港股通持续净卖出天数时间序列 -> getMfnSnOutflowDaysSeries


# 获取沪深港股通持续净卖出天数 -> getMfnSnOutflowDays


# 获取外资买卖超时间序列 -> getInSHdQFIiExSeries


# 获取外资买卖超 -> getInSHdQFIiEx


# 获取外资买卖超市值时间序列 -> getInSHdQFIiExMvSeries


# 获取外资买卖超市值 -> getInSHdQFIiExMv


# 获取投信买卖超时间序列 -> getInSHdFundExSeries


# 获取投信买卖超 -> getInSHdFundEx


# 获取投信买卖超市值时间序列 -> getInSHdFundExMvSeries


# 获取投信买卖超市值 -> getInSHdFundExMv


# 获取自营买卖超时间序列 -> getInSHdDlrExSeries


# 获取自营买卖超 -> getInSHdDlrEx


# 获取自营买卖超市值时间序列 -> getInSHdDlrExMvSeries


# 获取自营买卖超市值 -> getInSHdDlrExMv


# 获取合计买卖超时间序列 -> getInSHdTtlExSeries


# 获取合计买卖超 -> getInSHdTtlEx


# 获取合计买卖超市值时间序列 -> getInSHdTtlExMvSeries


# 获取合计买卖超市值 -> getInSHdTtlExMv


# 获取外资买进数量时间序列 -> getInSHdQFIiBuySeries


# 获取外资买进数量 -> getInSHdQFIiBuy


# 获取外资卖出数量时间序列 -> getInSHdQFIiSellSeries


# 获取外资卖出数量 -> getInSHdQFIiSell


# 获取投信买进数量时间序列 -> getInSHdFundBuySeries


# 获取投信买进数量 -> getInSHdFundBuy


# 获取投信卖出数量时间序列 -> getInSHdFundSellSeries


# 获取投信卖出数量 -> getInSHdFundSell


# 获取自营商买进数量时间序列 -> getInSHdDlrBuySeries


# 获取自营商买进数量 -> getInSHdDlrBuy


# 获取自营商卖出数量时间序列 -> getInSHdDlrSellSeries


# 获取自营商卖出数量 -> getInSHdDlrSell


# 获取区间回报时间序列 -> getReturnSeries


# 获取区间回报 -> getReturn


# 获取规模同类排名(券商集合理财)时间序列 -> getFundQSimilarProductSimilarRankingSeries


# 获取规模同类排名(券商集合理财) -> getFundQSimilarProductSimilarRanking


# 获取规模同类排名时间序列 -> getFundScaleRankingSeries


# 获取规模同类排名 -> getFundScaleRanking


# 获取下行风险同类排名时间序列 -> getRiskDownsideRiskRankingSeries


# 获取下行风险同类排名 -> getRiskDownsideRiskRanking


# 获取选时能力同类排名时间序列 -> getRiskTimeRankingSeries


# 获取选时能力同类排名 -> getRiskTimeRanking


# 获取选股能力同类排名时间序列 -> getRiskStockRankingSeries


# 获取选股能力同类排名 -> getRiskStockRanking


# 获取信息比率同类排名时间序列 -> getRiskInfoRatioRankingSeries


# 获取信息比率同类排名 -> getRiskInfoRatioRanking


# 获取跟踪误差同类排名时间序列 -> getRiskTrackErrorRankingSeries


# 获取跟踪误差同类排名 -> getRiskTrackErrorRanking


# 获取年化波动率同类排名时间序列 -> getRiskAnnualVolRankingSeries


# 获取年化波动率同类排名 -> getRiskAnnualVolRanking


# 获取平均持仓时间同类排名时间序列 -> getStyleAvgPositionTimeRankingSeries


# 获取平均持仓时间同类排名 -> getStyleAvgPositionTimeRanking


# 获取注册仓单数量时间序列 -> getStStockSeries


# 获取注册仓单数量 -> getStStock


# 获取企业价值(含货币资金)时间序列 -> getEv1Series


# 获取企业价值(含货币资金) -> getEv1


# 获取企业价值(剔除货币资金)时间序列 -> getEv2Series


# 获取企业价值(剔除货币资金) -> getEv2


# 获取资产总计/企业价值_PIT时间序列 -> getValTaToEvSeries


# 获取资产总计/企业价值_PIT -> getValTaToEv


# 获取营业收入(TTM)/企业价值_PIT时间序列 -> getValOrToEvTtMSeries


# 获取营业收入(TTM)/企业价值_PIT -> getValOrToEvTtM


# 获取应计利息(债券计算器)时间序列 -> getCalcAccruedSeries


# 获取应计利息(债券计算器) -> getCalcAccrued


# 获取剩余存续期(交易日)时间序列 -> getPtMTradeDaySeries


# 获取剩余存续期(交易日) -> getPtMTradeDay


# 获取剩余存续期(日历日)时间序列 -> getPtMDaySeries


# 获取剩余存续期(日历日) -> getPtMDay


# 获取理论价格时间序列 -> getTheoryValueSeries


# 获取理论价格 -> getTheoryValue


# 获取内在价值时间序列 -> getIntrInCtValueSeries


# 获取内在价值 -> getIntrInCtValue


# 获取时间价值时间序列 -> getTimeValueSeries


# 获取时间价值 -> getTimeValue


# 获取标的30日历史波动率时间序列 -> getUnderlyingHisVol30DSeries


# 获取标的30日历史波动率 -> getUnderlyingHisVol30D


# 获取标的60日历史波动率时间序列 -> getUsHisVolSeries


# 获取标的60日历史波动率 -> getUsHisVol


# 获取标的90日历史波动率时间序列 -> getUnderlyingHisVol90DSeries


# 获取标的90日历史波动率 -> getUnderlyingHisVol90D


# 获取期权隐含波动率时间序列 -> getUsImpliedVolSeries


# 获取期权隐含波动率 -> getUsImpliedVol


# 获取历史波动率时间序列 -> getVolatilityRatioSeries


# 获取历史波动率 -> getVolatilityRatio


# 获取1个月130%价值状态隐含波动率时间序列 -> getIv1M1300Series


# 获取1个月130%价值状态隐含波动率 -> getIv1M1300


# 获取1个月120%价值状态隐含波动率时间序列 -> getIv1M1200Series


# 获取1个月120%价值状态隐含波动率 -> getIv1M1200


# 获取1个月110%价值状态隐含波动率时间序列 -> getIv1M1100Series


# 获取1个月110%价值状态隐含波动率 -> getIv1M1100


# 获取1个月105%价值状态隐含波动率时间序列 -> getIv1M1050Series


# 获取1个月105%价值状态隐含波动率 -> getIv1M1050


# 获取1个月102.5%价值状态隐含波动率时间序列 -> getIv1M1025Series


# 获取1个月102.5%价值状态隐含波动率 -> getIv1M1025


# 获取1个月100%价值状态隐含波动率时间序列 -> getIv1M1000Series


# 获取1个月100%价值状态隐含波动率 -> getIv1M1000


# 获取1个月97.5%价值状态隐含波动率时间序列 -> getIv1M975Series


# 获取1个月97.5%价值状态隐含波动率 -> getIv1M975


# 获取1个月95%价值状态隐含波动率时间序列 -> getIv1M950Series


# 获取1个月95%价值状态隐含波动率 -> getIv1M950


# 获取1个月90%价值状态隐含波动率时间序列 -> getIv1M900Series


# 获取1个月90%价值状态隐含波动率 -> getIv1M900


# 获取1个月80%价值状态隐含波动率时间序列 -> getIv1M800Series


# 获取1个月80%价值状态隐含波动率 -> getIv1M800


# 获取1个月60%价值状态隐含波动率时间序列 -> getIv1M600Series


# 获取1个月60%价值状态隐含波动率 -> getIv1M600


# 获取2个月130%价值状态隐含波动率时间序列 -> getIv2M1300Series


# 获取2个月130%价值状态隐含波动率 -> getIv2M1300


# 获取2个月120%价值状态隐含波动率时间序列 -> getIv2M1200Series


# 获取2个月120%价值状态隐含波动率 -> getIv2M1200


# 获取2个月110%价值状态隐含波动率时间序列 -> getIv2M1100Series


# 获取2个月110%价值状态隐含波动率 -> getIv2M1100


# 获取2个月105%价值状态隐含波动率时间序列 -> getIv2M1050Series


# 获取2个月105%价值状态隐含波动率 -> getIv2M1050


# 获取2个月102.5%价值状态隐含波动率时间序列 -> getIv2M1025Series


# 获取2个月102.5%价值状态隐含波动率 -> getIv2M1025


# 获取2个月100%价值状态隐含波动率时间序列 -> getIv2M1000Series


# 获取2个月100%价值状态隐含波动率 -> getIv2M1000


# 获取2个月97.5%价值状态隐含波动率时间序列 -> getIv2M975Series


# 获取2个月97.5%价值状态隐含波动率 -> getIv2M975


# 获取2个月95%价值状态隐含波动率时间序列 -> getIv2M950Series


# 获取2个月95%价值状态隐含波动率 -> getIv2M950


# 获取2个月90%价值状态隐含波动率时间序列 -> getIv2M900Series


# 获取2个月90%价值状态隐含波动率 -> getIv2M900


# 获取2个月80%价值状态隐含波动率时间序列 -> getIv2M800Series


# 获取2个月80%价值状态隐含波动率 -> getIv2M800


# 获取2个月60%价值状态隐含波动率时间序列 -> getIv2M600Series


# 获取2个月60%价值状态隐含波动率 -> getIv2M600


# 获取3个月130%价值状态隐含波动率时间序列 -> getIv3M1300Series


# 获取3个月130%价值状态隐含波动率 -> getIv3M1300


# 获取3个月120%价值状态隐含波动率时间序列 -> getIv3M1200Series


# 获取3个月120%价值状态隐含波动率 -> getIv3M1200


# 获取3个月110%价值状态隐含波动率时间序列 -> getIv3M1100Series


# 获取3个月110%价值状态隐含波动率 -> getIv3M1100


# 获取3个月105%价值状态隐含波动率时间序列 -> getIv3M1050Series


# 获取3个月105%价值状态隐含波动率 -> getIv3M1050


# 获取3个月102.5%价值状态隐含波动率时间序列 -> getIv3M1025Series


# 获取3个月102.5%价值状态隐含波动率 -> getIv3M1025


# 获取3个月100%价值状态隐含波动率时间序列 -> getIv3M1000Series


# 获取3个月100%价值状态隐含波动率 -> getIv3M1000


# 获取3个月97.5%价值状态隐含波动率时间序列 -> getIv3M975Series


# 获取3个月97.5%价值状态隐含波动率 -> getIv3M975


# 获取3个月95%价值状态隐含波动率时间序列 -> getIv3M950Series


# 获取3个月95%价值状态隐含波动率 -> getIv3M950


# 获取3个月90%价值状态隐含波动率时间序列 -> getIv3M900Series


# 获取3个月90%价值状态隐含波动率 -> getIv3M900


# 获取3个月80%价值状态隐含波动率时间序列 -> getIv3M800Series


# 获取3个月80%价值状态隐含波动率 -> getIv3M800


# 获取3个月60%价值状态隐含波动率时间序列 -> getIv3M600Series


# 获取3个月60%价值状态隐含波动率 -> getIv3M600


# 获取6个月130%价值状态隐含波动率时间序列 -> getIv6M1300Series


# 获取6个月130%价值状态隐含波动率 -> getIv6M1300


# 获取6个月120%价值状态隐含波动率时间序列 -> getIv6M1200Series


# 获取6个月120%价值状态隐含波动率 -> getIv6M1200


# 获取6个月110%价值状态隐含波动率时间序列 -> getIv6M1100Series


# 获取6个月110%价值状态隐含波动率 -> getIv6M1100


# 获取6个月105%价值状态隐含波动率时间序列 -> getIv6M1050Series


# 获取6个月105%价值状态隐含波动率 -> getIv6M1050


# 获取6个月102.5%价值状态隐含波动率时间序列 -> getIv6M1025Series


# 获取6个月102.5%价值状态隐含波动率 -> getIv6M1025


# 获取6个月100%价值状态隐含波动率时间序列 -> getIv6M1000Series


# 获取6个月100%价值状态隐含波动率 -> getIv6M1000


# 获取6个月97.5%价值状态隐含波动率时间序列 -> getIv6M975Series


# 获取6个月97.5%价值状态隐含波动率 -> getIv6M975


# 获取6个月95%价值状态隐含波动率时间序列 -> getIv6M950Series


# 获取6个月95%价值状态隐含波动率 -> getIv6M950


# 获取6个月90%价值状态隐含波动率时间序列 -> getIv6M900Series


# 获取6个月90%价值状态隐含波动率 -> getIv6M900


# 获取6个月80%价值状态隐含波动率时间序列 -> getIv6M800Series


# 获取6个月80%价值状态隐含波动率 -> getIv6M800


# 获取6个月60%价值状态隐含波动率时间序列 -> getIv6M600Series


# 获取6个月60%价值状态隐含波动率 -> getIv6M600


# 获取9个月130%价值状态隐含波动率时间序列 -> getIv9M1300Series


# 获取9个月130%价值状态隐含波动率 -> getIv9M1300


# 获取9个月120%价值状态隐含波动率时间序列 -> getIv9M1200Series


# 获取9个月120%价值状态隐含波动率 -> getIv9M1200


# 获取9个月110%价值状态隐含波动率时间序列 -> getIv9M1100Series


# 获取9个月110%价值状态隐含波动率 -> getIv9M1100


# 获取9个月105%价值状态隐含波动率时间序列 -> getIv9M1050Series


# 获取9个月105%价值状态隐含波动率 -> getIv9M1050


# 获取9个月102.5%价值状态隐含波动率时间序列 -> getIv9M1025Series


# 获取9个月102.5%价值状态隐含波动率 -> getIv9M1025


# 获取9个月100%价值状态隐含波动率时间序列 -> getIv9M1000Series


# 获取9个月100%价值状态隐含波动率 -> getIv9M1000


# 获取9个月97.5%价值状态隐含波动率时间序列 -> getIv9M975Series


# 获取9个月97.5%价值状态隐含波动率 -> getIv9M975


# 获取9个月95%价值状态隐含波动率时间序列 -> getIv9M950Series


# 获取9个月95%价值状态隐含波动率 -> getIv9M950


# 获取9个月90%价值状态隐含波动率时间序列 -> getIv9M900Series


# 获取9个月90%价值状态隐含波动率 -> getIv9M900


# 获取9个月80%价值状态隐含波动率时间序列 -> getIv9M800Series


# 获取9个月80%价值状态隐含波动率 -> getIv9M800


# 获取9个月60%价值状态隐含波动率时间序列 -> getIv9M600Series


# 获取9个月60%价值状态隐含波动率 -> getIv9M600


# 获取1年130%价值状态隐含波动率时间序列 -> getIv1Y1300Series


# 获取1年130%价值状态隐含波动率 -> getIv1Y1300


# 获取1年120%价值状态隐含波动率时间序列 -> getIv1Y1200Series


# 获取1年120%价值状态隐含波动率 -> getIv1Y1200


# 获取1年110%价值状态隐含波动率时间序列 -> getIv1Y1100Series


# 获取1年110%价值状态隐含波动率 -> getIv1Y1100


# 获取1年105%价值状态隐含波动率时间序列 -> getIv1Y1050Series


# 获取1年105%价值状态隐含波动率 -> getIv1Y1050


# 获取1年102.5%价值状态隐含波动率时间序列 -> getIv1Y1025Series


# 获取1年102.5%价值状态隐含波动率 -> getIv1Y1025


# 获取1年100%价值状态隐含波动率时间序列 -> getIv1Y1000Series


# 获取1年100%价值状态隐含波动率 -> getIv1Y1000


# 获取1年97.5%价值状态隐含波动率时间序列 -> getIv1Y975Series


# 获取1年97.5%价值状态隐含波动率 -> getIv1Y975


# 获取1年95%价值状态隐含波动率时间序列 -> getIv1Y950Series


# 获取1年95%价值状态隐含波动率 -> getIv1Y950


# 获取1年90%价值状态隐含波动率时间序列 -> getIv1Y900Series


# 获取1年90%价值状态隐含波动率 -> getIv1Y900


# 获取1年80%价值状态隐含波动率时间序列 -> getIv1Y800Series


# 获取1年80%价值状态隐含波动率 -> getIv1Y800


# 获取1年60%价值状态隐含波动率时间序列 -> getIv1Y600Series


# 获取1年60%价值状态隐含波动率 -> getIv1Y600


# 获取一致预测净利润(未来12个月)时间序列 -> getWestNetProfitFtmSeries


# 获取一致预测净利润(未来12个月) -> getWestNetProfitFtm


# 获取一致预测净利润(未来12个月)的变化_1M_PIT时间序列 -> getWestNetProfitFtmChg1MSeries


# 获取一致预测净利润(未来12个月)的变化_1M_PIT -> getWestNetProfitFtmChg1M


# 获取一致预测净利润(未来12个月)的变化_3M_PIT时间序列 -> getWestNetProfitFtmChg3MSeries


# 获取一致预测净利润(未来12个月)的变化_3M_PIT -> getWestNetProfitFtmChg3M


# 获取一致预测净利润(未来12个月)的变化_6M_PIT时间序列 -> getWestNetProfitFtmChg6MSeries


# 获取一致预测净利润(未来12个月)的变化_6M_PIT -> getWestNetProfitFtmChg6M


# 获取一致预测净利润(未来12个月)的变化率_1M_PIT时间序列 -> getWestNetProfitFtm1MSeries


# 获取一致预测净利润(未来12个月)的变化率_1M_PIT -> getWestNetProfitFtm1M


# 获取一致预测净利润(未来12个月)的变化率_3M_PIT时间序列 -> getWestNetProfitFtm3MSeries


# 获取一致预测净利润(未来12个月)的变化率_3M_PIT -> getWestNetProfitFtm3M


# 获取一致预测净利润(未来12个月)的变化率_6M_PIT时间序列 -> getWestNetProfitFtm6MSeries


# 获取一致预测净利润(未来12个月)的变化率_6M_PIT -> getWestNetProfitFtm6M


# 获取一致预测净利润(未来12个月)与归属于母公司净利润(TTM)的差_PIT时间序列 -> getWestNetProfitDiffSeries


# 获取一致预测净利润(未来12个月)与归属于母公司净利润(TTM)的差_PIT -> getWestNetProfitDiff


# 获取一致预测净利润(未来12个月)/归属于母公司的股东权益_PIT时间序列 -> getWestRoeFtmSeries


# 获取一致预测净利润(未来12个月)/归属于母公司的股东权益_PIT -> getWestRoeFtm


# 获取一致预测净利润同比时间序列 -> getWestNetProfitYoYSeries


# 获取一致预测净利润同比 -> getWestNetProfitYoY


# 获取一致预测净利润同比(FY2比FY1)时间序列 -> getWestAvgNpYoYSeries


# 获取一致预测净利润同比(FY2比FY1) -> getWestAvgNpYoY


# 获取一致预测净利润2年复合增长率时间序列 -> getWestNetProfitCAgrSeries


# 获取一致预测净利润2年复合增长率 -> getWestNetProfitCAgr


# 获取一致预测净利润1周变化率时间序列 -> getWestNProc1WSeries


# 获取一致预测净利润1周变化率 -> getWestNProc1W


# 获取一致预测净利润4周变化率时间序列 -> getWestNProc4WSeries


# 获取一致预测净利润4周变化率 -> getWestNProc4W


# 获取一致预测净利润13周变化率时间序列 -> getWestNProc13WSeries


# 获取一致预测净利润13周变化率 -> getWestNProc13W


# 获取一致预测净利润26周变化率时间序列 -> getWestNProc26WSeries


# 获取一致预测净利润26周变化率 -> getWestNProc26W


# 获取一致预测每股收益(未来12个月)时间序列 -> getWestEpsFtmSeries


# 获取一致预测每股收益(未来12个月) -> getWestEpsFtm


# 获取一致预测每股收益(未来12个月)的变化_1M_PIT时间序列 -> getWestEpsFtmChg1MSeries


# 获取一致预测每股收益(未来12个月)的变化_1M_PIT -> getWestEpsFtmChg1M


# 获取一致预测每股收益(未来12个月)的变化_3M_PIT时间序列 -> getWestEpsFtmChg3MSeries


# 获取一致预测每股收益(未来12个月)的变化_3M_PIT -> getWestEpsFtmChg3M


# 获取一致预测每股收益(未来12个月)的变化_6M_PIT时间序列 -> getWestEpsFtmChg6MSeries


# 获取一致预测每股收益(未来12个月)的变化_6M_PIT -> getWestEpsFtmChg6M


# 获取一致预测每股收益(未来12个月)的变化率_1M_PIT时间序列 -> getWestEpsFtm1MSeries


# 获取一致预测每股收益(未来12个月)的变化率_1M_PIT -> getWestEpsFtm1M


# 获取一致预测每股收益(未来12个月)的变化率_3M_PIT时间序列 -> getWestEpsFtm3MSeries


# 获取一致预测每股收益(未来12个月)的变化率_3M_PIT -> getWestEpsFtm3M


# 获取一致预测每股收益(未来12个月)的变化率_6M_PIT时间序列 -> getWestEpsFtm6MSeries


# 获取一致预测每股收益(未来12个月)的变化率_6M_PIT -> getWestEpsFtm6M


# 获取一致预测每股收益(未来12个月)与EPS(TTM)的变化率_PIT时间序列 -> getWestEpsFtmGrowthSeries


# 获取一致预测每股收益(未来12个月)与EPS(TTM)的变化率_PIT -> getWestEpsFtmGrowth


# 获取一致预测营业收入(未来12个月)时间序列 -> getWestSalesFtmSeries


# 获取一致预测营业收入(未来12个月) -> getWestSalesFtm


# 获取一致预测营业收入(未来12个月)的变化_1M_PIT时间序列 -> getWestSalesFtmChg1MSeries


# 获取一致预测营业收入(未来12个月)的变化_1M_PIT -> getWestSalesFtmChg1M


# 获取一致预测营业收入(未来12个月)的变化_3M_PIT时间序列 -> getWestSalesFtmChg3MSeries


# 获取一致预测营业收入(未来12个月)的变化_3M_PIT -> getWestSalesFtmChg3M


# 获取一致预测营业收入(未来12个月)的变化_6M_PIT时间序列 -> getWestSalesFtmChg6MSeries


# 获取一致预测营业收入(未来12个月)的变化_6M_PIT -> getWestSalesFtmChg6M


# 获取一致预测营业收入(未来12个月)的变化率_1M_PIT时间序列 -> getWestSalesFtm1MSeries


# 获取一致预测营业收入(未来12个月)的变化率_1M_PIT -> getWestSalesFtm1M


# 获取一致预测营业收入(未来12个月)的变化率_3M_PIT时间序列 -> getWestSalesFtm3MSeries


# 获取一致预测营业收入(未来12个月)的变化率_3M_PIT -> getWestSalesFtm3M


# 获取一致预测营业收入(未来12个月)的变化率_6M_PIT时间序列 -> getWestSalesFtm6MSeries


# 获取一致预测营业收入(未来12个月)的变化率_6M_PIT -> getWestSalesFtm6M


# 获取一致预测营业收入同比时间序列 -> getWestSalesYoYSeries


# 获取一致预测营业收入同比 -> getWestSalesYoY


# 获取一致预测营业收入2年复合增长率时间序列 -> getWestSalesCAgrSeries


# 获取一致预测营业收入2年复合增长率 -> getWestSalesCAgr


# 获取一致预测每股现金流(未来12个月)时间序列 -> getWestAvgCpSFtmSeries


# 获取一致预测每股现金流(未来12个月) -> getWestAvgCpSFtm


# 获取一致预测息税前利润(未来12个月)时间序列 -> getWestAvGebItFtmSeries


# 获取一致预测息税前利润(未来12个月) -> getWestAvGebItFtm


# 获取一致预测息税前利润同比时间序列 -> getWestAvGebItYoYSeries


# 获取一致预测息税前利润同比 -> getWestAvGebItYoY


# 获取一致预测息税前利润年复合增长率时间序列 -> getWestAvGebItCAgrSeries


# 获取一致预测息税前利润年复合增长率 -> getWestAvGebItCAgr


# 获取一致预测息税折旧摊销前利润(未来12个月)时间序列 -> getWestAvGebItDaFtmSeries


# 获取一致预测息税折旧摊销前利润(未来12个月) -> getWestAvGebItDaFtm


# 获取一致预测息税折旧摊销前利润同比时间序列 -> getWestAvGebItDaYoYSeries


# 获取一致预测息税折旧摊销前利润同比 -> getWestAvGebItDaYoY


# 获取一致预测息税折旧摊销前利润2年复合增长率时间序列 -> getWestAvGebItDaCAgrSeries


# 获取一致预测息税折旧摊销前利润2年复合增长率 -> getWestAvGebItDaCAgr


# 获取一致预测利润总额(未来12个月)时间序列 -> getWestAvGebTFtmSeries


# 获取一致预测利润总额(未来12个月) -> getWestAvGebTFtm


# 获取一致预测利润总额同比时间序列 -> getWestAvGebTYoYSeries


# 获取一致预测利润总额同比 -> getWestAvGebTYoY


# 获取一致预测利润总额2年复合增长率时间序列 -> getWestAvGebTCAgrSeries


# 获取一致预测利润总额2年复合增长率 -> getWestAvGebTCAgr


# 获取一致预测营业利润(未来12个月)时间序列 -> getWestAvgOperatingProfitFtmSeries


# 获取一致预测营业利润(未来12个月) -> getWestAvgOperatingProfitFtm


# 获取一致预测营业利润同比时间序列 -> getWestAvgOperatingProfitYoYSeries


# 获取一致预测营业利润同比 -> getWestAvgOperatingProfitYoY


# 获取一致预测营业利润2年复合增长率时间序列 -> getWestAvgOperatingProfitCAgrSeries


# 获取一致预测营业利润2年复合增长率 -> getWestAvgOperatingProfitCAgr


# 获取一致预测营业成本(未来12个月)时间序列 -> getWestAvgOcFtmSeries


# 获取一致预测营业成本(未来12个月) -> getWestAvgOcFtm


# 获取一致预测营业成本同比时间序列 -> getWestAvgOcYoYSeries


# 获取一致预测营业成本同比 -> getWestAvgOcYoY


# 获取一致预测营业成本2年复合增长率时间序列 -> getWestAvgOcCAgrSeries


# 获取一致预测营业成本2年复合增长率 -> getWestAvgOcCAgr


# 获取每股收益预测机构家数时间序列 -> getEstInStNumSeries


# 获取每股收益预测机构家数 -> getEstInStNum


# 获取每股收益预测机构家数(可选类型)时间序列 -> getWestInStNumSeries


# 获取每股收益预测机构家数(可选类型) -> getWestInStNum


# 获取预测每股收益平均值时间序列 -> getEstEpsSeries


# 获取预测每股收益平均值 -> getEstEps


# 获取预测每股收益平均值(币种转换)时间序列 -> getEstEps1Series


# 获取预测每股收益平均值(币种转换) -> getEstEps1


# 获取预测每股收益平均值(可选类型)时间序列 -> getWestEpsSeries


# 获取预测每股收益平均值(可选类型) -> getWestEps


# 获取预测每股收益平均值(可选类型,币种转换)时间序列 -> getWestEps1Series


# 获取预测每股收益平均值(可选类型,币种转换) -> getWestEps1


# 获取预测每股收益最大值时间序列 -> getEstMaxEpsSeries


# 获取预测每股收益最大值 -> getEstMaxEps


# 获取预测每股收益最大值(币种转换)时间序列 -> getEstMaxEps1Series


# 获取预测每股收益最大值(币种转换) -> getEstMaxEps1


# 获取预测每股收益最大值(可选类型)时间序列 -> getWestMaxEpsSeries


# 获取预测每股收益最大值(可选类型) -> getWestMaxEps


# 获取预测每股收益最大值(可选类型,币种转换)时间序列 -> getWestMaxEps1Series


# 获取预测每股收益最大值(可选类型,币种转换) -> getWestMaxEps1


# 获取预测每股收益最小值时间序列 -> getEstMinePsSeries


# 获取预测每股收益最小值 -> getEstMinePs


# 获取预测每股收益最小值(币种转换)时间序列 -> getEstMinePs1Series


# 获取预测每股收益最小值(币种转换) -> getEstMinePs1


# 获取预测每股收益最小值(可选类型)时间序列 -> getWestMinePsSeries


# 获取预测每股收益最小值(可选类型) -> getWestMinePs


# 获取预测每股收益最小值(可选类型,币种转换)时间序列 -> getWestMinePs1Series


# 获取预测每股收益最小值(可选类型,币种转换) -> getWestMinePs1


# 获取预测每股收益中值时间序列 -> getEstMedianEpsSeries


# 获取预测每股收益中值 -> getEstMedianEps


# 获取预测每股收益中值(币种转换)时间序列 -> getEstMedianEps1Series


# 获取预测每股收益中值(币种转换) -> getEstMedianEps1


# 获取预测每股收益中值(可选类型)时间序列 -> getWestMedianEpsSeries


# 获取预测每股收益中值(可选类型) -> getWestMedianEps


# 获取预测每股收益中值(可选类型,币种转换)时间序列 -> getWestMedianEps1Series


# 获取预测每股收益中值(可选类型,币种转换) -> getWestMedianEps1


# 获取预测每股收益标准差时间序列 -> getEstStdEpsSeries


# 获取预测每股收益标准差 -> getEstStdEps


# 获取预测每股收益标准差(币种转换)时间序列 -> getEstStdEps1Series


# 获取预测每股收益标准差(币种转换) -> getEstStdEps1


# 获取预测每股收益标准差(可选类型)时间序列 -> getWestStdEpsSeries


# 获取预测每股收益标准差(可选类型) -> getWestStdEps


# 获取预测每股收益标准差(可选类型,币种转换)时间序列 -> getWestStdEps1Series


# 获取预测每股收益标准差(可选类型,币种转换) -> getWestStdEps1


# 获取预测营业收入平均值时间序列 -> getEstSalesSeries


# 获取预测营业收入平均值 -> getEstSales


# 获取预测营业收入平均值(币种转换)时间序列 -> getEstSales1Series


# 获取预测营业收入平均值(币种转换) -> getEstSales1


# 获取预测营业收入平均值(可选类型)时间序列 -> getWestSalesSeries


# 获取预测营业收入平均值(可选类型) -> getWestSales


# 获取预测营业收入平均值(可选类型,币种转换)时间序列 -> getWestSales1Series


# 获取预测营业收入平均值(可选类型,币种转换) -> getWestSales1


# 获取预测营业收入最大值时间序列 -> getEstMaxSalesSeries


# 获取预测营业收入最大值 -> getEstMaxSales


# 获取预测营业收入最大值(币种转换)时间序列 -> getEstMaxSales1Series


# 获取预测营业收入最大值(币种转换) -> getEstMaxSales1


# 获取预测营业收入最大值(可选类型)时间序列 -> getWestMaxSalesSeries


# 获取预测营业收入最大值(可选类型) -> getWestMaxSales


# 获取预测营业收入最大值(可选类型,币种转换)时间序列 -> getWestMaxSales1Series


# 获取预测营业收入最大值(可选类型,币种转换) -> getWestMaxSales1


# 获取预测营业收入最小值时间序列 -> getEstMinSalesSeries


# 获取预测营业收入最小值 -> getEstMinSales


# 获取预测营业收入最小值(币种转换)时间序列 -> getEstMinSales1Series


# 获取预测营业收入最小值(币种转换) -> getEstMinSales1


# 获取预测营业收入最小值(可选类型)时间序列 -> getWestMinSalesSeries


# 获取预测营业收入最小值(可选类型) -> getWestMinSales


# 获取预测营业收入最小值(可选类型,币种转换)时间序列 -> getWestMinSales1Series


# 获取预测营业收入最小值(可选类型,币种转换) -> getWestMinSales1


# 获取预测营业收入中值时间序列 -> getEstMedianSalesSeries


# 获取预测营业收入中值 -> getEstMedianSales


# 获取预测营业收入中值(币种转换)时间序列 -> getEstMedianSales1Series


# 获取预测营业收入中值(币种转换) -> getEstMedianSales1


# 获取预测营业收入中值(可选类型)时间序列 -> getWestMedianSalesSeries


# 获取预测营业收入中值(可选类型) -> getWestMedianSales


# 获取预测营业收入中值(可选类型,币种转换)时间序列 -> getWestMedianSales1Series


# 获取预测营业收入中值(可选类型,币种转换) -> getWestMedianSales1


# 获取预测营业收入标准差时间序列 -> getEstStdSalesSeries


# 获取预测营业收入标准差 -> getEstStdSales


# 获取预测营业收入标准差(币种转换)时间序列 -> getEstStdSales1Series


# 获取预测营业收入标准差(币种转换) -> getEstStdSales1


# 获取预测营业收入标准差(可选类型)时间序列 -> getWestStdSalesSeries


# 获取预测营业收入标准差(可选类型) -> getWestStdSales


# 获取预测营业收入标准差(可选类型,币种转换)时间序列 -> getWestStdSales1Series


# 获取预测营业收入标准差(可选类型,币种转换) -> getWestStdSales1


# 获取预测净利润平均值时间序列 -> getEstNetProfitSeries


# 获取预测净利润平均值 -> getEstNetProfit


# 获取预测净利润平均值(币种转换)时间序列 -> getEstNetProfit1Series


# 获取预测净利润平均值(币种转换) -> getEstNetProfit1


# 获取预测净利润平均值(可选类型)时间序列 -> getWestNetProfitSeries


# 获取预测净利润平均值(可选类型) -> getWestNetProfit


# 获取预测净利润平均值(可选类型,币种转换)时间序列 -> getWestNetProfit1Series


# 获取预测净利润平均值(可选类型,币种转换) -> getWestNetProfit1


# 获取预测净利润最大值时间序列 -> getEstMaxNetProfitSeries


# 获取预测净利润最大值 -> getEstMaxNetProfit


# 获取预测净利润最大值(币种转换)时间序列 -> getEstMaxNetProfit1Series


# 获取预测净利润最大值(币种转换) -> getEstMaxNetProfit1


# 获取预测净利润最大值(可选类型)时间序列 -> getWestMaxNetProfitSeries


# 获取预测净利润最大值(可选类型) -> getWestMaxNetProfit


# 获取预测净利润最大值(可选类型,币种转换)时间序列 -> getWestMaxNetProfit1Series


# 获取预测净利润最大值(可选类型,币种转换) -> getWestMaxNetProfit1


# 获取预测净利润最小值时间序列 -> getEstMinNetProfitSeries


# 获取预测净利润最小值 -> getEstMinNetProfit


# 获取预测净利润最小值(币种转换)时间序列 -> getEstMinNetProfit1Series


# 获取预测净利润最小值(币种转换) -> getEstMinNetProfit1


# 获取预测净利润最小值(可选类型)时间序列 -> getWestMinNetProfitSeries


# 获取预测净利润最小值(可选类型) -> getWestMinNetProfit


# 获取预测净利润最小值(可选类型,币种转换)时间序列 -> getWestMinNetProfit1Series


# 获取预测净利润最小值(可选类型,币种转换) -> getWestMinNetProfit1


# 获取预测净利润中值时间序列 -> getEstMedianNetProfitSeries


# 获取预测净利润中值 -> getEstMedianNetProfit


# 获取预测净利润中值(币种转换)时间序列 -> getEstMedianNetProfit1Series


# 获取预测净利润中值(币种转换) -> getEstMedianNetProfit1


# 获取预测净利润中值(可选类型)时间序列 -> getWestMedianNetProfitSeries


# 获取预测净利润中值(可选类型) -> getWestMedianNetProfit


# 获取预测净利润中值(可选类型,币种转换)时间序列 -> getWestMedianNetProfit1Series


# 获取预测净利润中值(可选类型,币种转换) -> getWestMedianNetProfit1


# 获取预测净利润标准差时间序列 -> getEstStdNetProfitSeries


# 获取预测净利润标准差 -> getEstStdNetProfit


# 获取预测净利润标准差(币种转换)时间序列 -> getEstStdNetProfit1Series


# 获取预测净利润标准差(币种转换) -> getEstStdNetProfit1


# 获取预测净利润标准差(可选类型)时间序列 -> getWestStdNetProfitSeries


# 获取预测净利润标准差(可选类型) -> getWestStdNetProfit


# 获取预测净利润标准差(可选类型,币种转换)时间序列 -> getWestStdNetProfit1Series


# 获取预测净利润标准差(可选类型,币种转换) -> getWestStdNetProfit1


# 获取预测利润总额平均值时间序列 -> getEstAvGebTSeries


# 获取预测利润总额平均值 -> getEstAvGebT


# 获取预测利润总额平均值(币种转换)时间序列 -> getEstAvGebT1Series


# 获取预测利润总额平均值(币种转换) -> getEstAvGebT1


# 获取预测利润总额平均值(可选类型)时间序列 -> getWestAvGebTSeries


# 获取预测利润总额平均值(可选类型) -> getWestAvGebT


# 获取预测利润总额平均值(可选类型,币种转换)时间序列 -> getWestAvGebT1Series


# 获取预测利润总额平均值(可选类型,币种转换) -> getWestAvGebT1


# 获取预测利润总额最大值时间序列 -> getEstMaxEBtSeries


# 获取预测利润总额最大值 -> getEstMaxEBt


# 获取预测利润总额最大值(币种转换)时间序列 -> getEstMaxEBt1Series


# 获取预测利润总额最大值(币种转换) -> getEstMaxEBt1


# 获取预测利润总额最大值(可选类型)时间序列 -> getWestMaxEBtSeries


# 获取预测利润总额最大值(可选类型) -> getWestMaxEBt


# 获取预测利润总额最大值(可选类型,币种转换)时间序列 -> getWestMaxEBt1Series


# 获取预测利润总额最大值(可选类型,币种转换) -> getWestMaxEBt1


# 获取预测利润总额最小值时间序列 -> getEstMinEBTSeries


# 获取预测利润总额最小值 -> getEstMinEBT


# 获取预测利润总额最小值(币种转换)时间序列 -> getEstMinEBT1Series


# 获取预测利润总额最小值(币种转换) -> getEstMinEBT1


# 获取预测利润总额最小值(可选类型)时间序列 -> getWestMinEBTSeries


# 获取预测利润总额最小值(可选类型) -> getWestMinEBT


# 获取预测利润总额最小值(可选类型,币种转换)时间序列 -> getWestMinEBT1Series


# 获取预测利润总额最小值(可选类型,币种转换) -> getWestMinEBT1


# 获取预测利润总额中值时间序列 -> getEstMedianEBtSeries


# 获取预测利润总额中值 -> getEstMedianEBt


# 获取预测利润总额中值(币种转换)时间序列 -> getEstMedianEBt1Series


# 获取预测利润总额中值(币种转换) -> getEstMedianEBt1


# 获取预测利润总额中值(可选类型)时间序列 -> getWestMedianEBtSeries


# 获取预测利润总额中值(可选类型) -> getWestMedianEBt


# 获取预测利润总额中值(可选类型,币种转换)时间序列 -> getWestMedianEBt1Series


# 获取预测利润总额中值(可选类型,币种转换) -> getWestMedianEBt1


# 获取预测利润总额标准差时间序列 -> getEstStDebtSeries


# 获取预测利润总额标准差 -> getEstStDebt


# 获取预测利润总额标准差(币种转换)时间序列 -> getEstStDebt1Series


# 获取预测利润总额标准差(币种转换) -> getEstStDebt1


# 获取预测利润总额标准差(可选类型)时间序列 -> getWestStDebtSeries


# 获取预测利润总额标准差(可选类型) -> getWestStDebt


# 获取预测利润总额标准差(可选类型,币种转换)时间序列 -> getWestStDebt1Series


# 获取预测利润总额标准差(可选类型,币种转换) -> getWestStDebt1


# 获取预测营业利润平均值时间序列 -> getEstAvgOperatingProfitSeries


# 获取预测营业利润平均值 -> getEstAvgOperatingProfit


# 获取预测营业利润平均值(币种转换)时间序列 -> getEstAvgOperatingProfit1Series


# 获取预测营业利润平均值(币种转换) -> getEstAvgOperatingProfit1


# 获取预测营业利润平均值(可选类型)时间序列 -> getWestAvgOperatingProfitSeries


# 获取预测营业利润平均值(可选类型) -> getWestAvgOperatingProfit


# 获取预测营业利润平均值(可选类型,币种转换)时间序列 -> getWestAvgOperatingProfit1Series


# 获取预测营业利润平均值(可选类型,币种转换) -> getWestAvgOperatingProfit1


# 获取预测营业利润最大值时间序列 -> getEstMaxOperatingProfitSeries


# 获取预测营业利润最大值 -> getEstMaxOperatingProfit


# 获取预测营业利润最大值(币种转换)时间序列 -> getEstMaxOperatingProfit1Series


# 获取预测营业利润最大值(币种转换) -> getEstMaxOperatingProfit1


# 获取预测营业利润最大值(可选类型)时间序列 -> getWestMaxOperatingProfitSeries


# 获取预测营业利润最大值(可选类型) -> getWestMaxOperatingProfit


# 获取预测营业利润最大值(可选类型,币种转换)时间序列 -> getWestMaxOperatingProfit1Series


# 获取预测营业利润最大值(可选类型,币种转换) -> getWestMaxOperatingProfit1


# 获取预测营业利润最小值时间序列 -> getEstMinOperatingProfitSeries


# 获取预测营业利润最小值 -> getEstMinOperatingProfit


# 获取预测营业利润最小值(币种转换)时间序列 -> getEstMinOperatingProfit1Series


# 获取预测营业利润最小值(币种转换) -> getEstMinOperatingProfit1


# 获取预测营业利润最小值(可选类型)时间序列 -> getWestMinOperatingProfitSeries


# 获取预测营业利润最小值(可选类型) -> getWestMinOperatingProfit


# 获取预测营业利润最小值(可选类型,币种转换)时间序列 -> getWestMinOperatingProfit1Series


# 获取预测营业利润最小值(可选类型,币种转换) -> getWestMinOperatingProfit1


# 获取预测营业利润中值时间序列 -> getEstMedianOperatingProfitSeries


# 获取预测营业利润中值 -> getEstMedianOperatingProfit


# 获取预测营业利润中值(币种转换)时间序列 -> getEstMedianOperatingProfit1Series


# 获取预测营业利润中值(币种转换) -> getEstMedianOperatingProfit1


# 获取预测营业利润中值(可选类型)时间序列 -> getWestMedianOperatingProfitSeries


# 获取预测营业利润中值(可选类型) -> getWestMedianOperatingProfit


# 获取预测营业利润中值(可选类型,币种转换)时间序列 -> getWestMedianOperatingProfit1Series


# 获取预测营业利润中值(可选类型,币种转换) -> getWestMedianOperatingProfit1


# 获取预测营业利润标准差时间序列 -> getEstStdOperatingProfitSeries


# 获取预测营业利润标准差 -> getEstStdOperatingProfit


# 获取预测营业利润标准差(币种转换)时间序列 -> getEstStdOperatingProfit1Series


# 获取预测营业利润标准差(币种转换) -> getEstStdOperatingProfit1


# 获取预测营业利润标准差(可选类型)时间序列 -> getWestStdOperatingProfitSeries


# 获取预测营业利润标准差(可选类型) -> getWestStdOperatingProfit


# 获取预测营业利润标准差(可选类型,币种转换)时间序列 -> getWestStdOperatingProfit1Series


# 获取预测营业利润标准差(可选类型,币种转换) -> getWestStdOperatingProfit1


# 获取营业收入调高家数时间序列 -> getEstSalesUpgradeSeries


# 获取营业收入调高家数 -> getEstSalesUpgrade


# 获取营业收入调高家数(可选类型)时间序列 -> getWestSalesUpgradeSeries


# 获取营业收入调高家数(可选类型) -> getWestSalesUpgrade


# 获取营业收入调低家数时间序列 -> getEstSalesDowngradeSeries


# 获取营业收入调低家数 -> getEstSalesDowngrade


# 获取营业收入调低家数(可选类型)时间序列 -> getWestSalesDowngradeSeries


# 获取营业收入调低家数(可选类型) -> getWestSalesDowngrade


# 获取营业收入维持家数时间序列 -> getEstSalesMaintainSeries


# 获取营业收入维持家数 -> getEstSalesMaintain


# 获取营业收入维持家数(可选类型)时间序列 -> getWestSalesMaintainSeries


# 获取营业收入维持家数(可选类型) -> getWestSalesMaintain


# 获取净利润调高家数时间序列 -> getEstNetProfitUpgradeSeries


# 获取净利润调高家数 -> getEstNetProfitUpgrade


# 获取净利润调高家数(可选类型)时间序列 -> getWestNetProfitUpgradeSeries


# 获取净利润调高家数(可选类型) -> getWestNetProfitUpgrade


# 获取净利润调低家数时间序列 -> getEstNetProfitDowngradeSeries


# 获取净利润调低家数 -> getEstNetProfitDowngrade


# 获取净利润调低家数(可选类型)时间序列 -> getWestNetProfitDowngradeSeries


# 获取净利润调低家数(可选类型) -> getWestNetProfitDowngrade


# 获取净利润维持家数时间序列 -> getEstNetProfitMaintainSeries


# 获取净利润维持家数 -> getEstNetProfitMaintain


# 获取净利润维持家数(可选类型)时间序列 -> getWestNetProfitMaintainSeries


# 获取净利润维持家数(可选类型) -> getWestNetProfitMaintain


# 获取预测净利润增长率时间序列 -> getEstYoYNetProfitSeries


# 获取预测净利润增长率 -> getEstYoYNetProfit


# 获取预测净利润增长率(可选类型)时间序列 -> getWestYoYNetProfitSeries


# 获取预测净利润增长率(可选类型) -> getWestYoYNetProfit


# 获取预测营业收入增长率时间序列 -> getEstYoYSalesSeries


# 获取预测营业收入增长率 -> getEstYoYSales


# 获取预测营业收入增长率(可选类型)时间序列 -> getWestYoYSalesSeries


# 获取预测营业收入增长率(可选类型) -> getWestYoYSales


# 获取综合评级(数值)时间序列 -> getRatingAvgSeries


# 获取综合评级(数值) -> getRatingAvg


# 获取综合评级(数值)(可选类型)时间序列 -> getWRatingAvgDataSeries


# 获取综合评级(数值)(可选类型) -> getWRatingAvgData


# 获取综合评级(中文)时间序列 -> getRatingAvgChNSeries


# 获取综合评级(中文) -> getRatingAvgChN


# 获取综合评级(中文)(可选类型)时间序列 -> getWRatingAvgCnSeries


# 获取综合评级(中文)(可选类型) -> getWRatingAvgCn


# 获取综合评级(英文)时间序列 -> getRatingAvGengSeries


# 获取综合评级(英文) -> getRatingAvGeng


# 获取综合评级(英文)(可选类型)时间序列 -> getWRatingAvgEnSeries


# 获取综合评级(英文)(可选类型) -> getWRatingAvgEn


# 获取评级机构家数时间序列 -> getRatingInStNumSeries


# 获取评级机构家数 -> getRatingInStNum


# 获取评级机构家数(可选类型)时间序列 -> getWRatingInStNumSeries


# 获取评级机构家数(可选类型) -> getWRatingInStNum


# 获取评级调高家数时间序列 -> getRatingUpgradeSeries


# 获取评级调高家数 -> getRatingUpgrade


# 获取评级调高家数(可选类型)时间序列 -> getWRatingUpgradeSeries


# 获取评级调高家数(可选类型) -> getWRatingUpgrade


# 获取评级调低家数时间序列 -> getRatingDowngradeSeries


# 获取评级调低家数 -> getRatingDowngrade


# 获取评级调低家数(可选类型)时间序列 -> getWRatingDowngradeSeries


# 获取评级调低家数(可选类型) -> getWRatingDowngrade


# 获取评级维持家数时间序列 -> getRatingMaintainSeries


# 获取评级维持家数 -> getRatingMaintain


# 获取评级维持家数(可选类型)时间序列 -> getWRatingMaintainSeries


# 获取评级维持家数(可选类型) -> getWRatingMaintain


# 获取评级买入家数时间序列 -> getRatingNumOfBuySeries


# 获取评级买入家数 -> getRatingNumOfBuy


# 获取评级买入家数(可选类型)时间序列 -> getWRatingNumOfBuySeries


# 获取评级买入家数(可选类型) -> getWRatingNumOfBuy


# 获取评级增持家数时间序列 -> getRatingNumOfOutperformSeries


# 获取评级增持家数 -> getRatingNumOfOutperform


# 获取评级增持家数(可选类型)时间序列 -> getWRatingNumOfOutperformSeries


# 获取评级增持家数(可选类型) -> getWRatingNumOfOutperform


# 获取评级中性家数时间序列 -> getRatingNumOfHoldSeries


# 获取评级中性家数 -> getRatingNumOfHold


# 获取评级中性家数(可选类型)时间序列 -> getWRatingNumOfHoldSeries


# 获取评级中性家数(可选类型) -> getWRatingNumOfHold


# 获取评级减持家数时间序列 -> getRatingNumOfUnderPerformSeries


# 获取评级减持家数 -> getRatingNumOfUnderPerform


# 获取评级减持家数(可选类型)时间序列 -> getWRatingNumOfUnderPerformSeries


# 获取评级减持家数(可选类型) -> getWRatingNumOfUnderPerform


# 获取评级卖出家数时间序列 -> getRatingNumOfSellSeries


# 获取评级卖出家数 -> getRatingNumOfSell


# 获取评级卖出家数(可选类型)时间序列 -> getWRatingNumOfSellSeries


# 获取评级卖出家数(可选类型) -> getWRatingNumOfSell


# 获取一致预测目标价时间序列 -> getWRatingTargetPriceSeries


# 获取一致预测目标价 -> getWRatingTargetPrice


# 获取一致预测目标价(可选类型)时间序列 -> getTargetPriceAvgSeries


# 获取一致预测目标价(可选类型) -> getTargetPriceAvg


# 获取一致预测目标价上升空间_PIT时间序列 -> getWestFReturnSeries


# 获取一致预测目标价上升空间_PIT -> getWestFReturn


# 获取大事日期(大事后预测)时间序列 -> getEstEventDateSeries


# 获取大事日期(大事后预测) -> getEstEventDate


# 获取营业收入预测机构家数(可选类型)时间序列 -> getWestInStNumSalesSeries


# 获取营业收入预测机构家数(可选类型) -> getWestInStNumSales


# 获取净利润预测机构家数(可选类型)时间序列 -> getWestInStNumNpSeries


# 获取净利润预测机构家数(可选类型) -> getWestInStNumNp


# 获取每股现金流预测机构家数(可选类型)时间序列 -> getWestInStNumCpSSeries


# 获取每股现金流预测机构家数(可选类型) -> getWestInStNumCpS


# 获取每股股利预测机构家数(可选类型)时间序列 -> getWestInStNumDpsSeries


# 获取每股股利预测机构家数(可选类型) -> getWestInStNumDps


# 获取息税前利润预测机构家数(可选类型)时间序列 -> getWestInStNumEbItSeries


# 获取息税前利润预测机构家数(可选类型) -> getWestInStNumEbIt


# 获取息税折旧摊销前利润预测机构家数(可选类型)时间序列 -> getWestInStNumEbItDaSeries


# 获取息税折旧摊销前利润预测机构家数(可选类型) -> getWestInStNumEbItDa


# 获取每股净资产预测机构家数(可选类型)时间序列 -> getWestInStNumBpSSeries


# 获取每股净资产预测机构家数(可选类型) -> getWestInStNumBpS


# 获取利润总额预测机构家数(可选类型)时间序列 -> getWestInStNumEBtSeries


# 获取利润总额预测机构家数(可选类型) -> getWestInStNumEBt


# 获取总资产收益率预测机构家数(可选类型)时间序列 -> getWestInStNumRoaSeries


# 获取总资产收益率预测机构家数(可选类型) -> getWestInStNumRoa


# 获取净资产收益率预测机构家数(可选类型)时间序列 -> getWestInStNumRoeSeries


# 获取净资产收益率预测机构家数(可选类型) -> getWestInStNumRoe


# 获取营业利润预测机构家数(可选类型)时间序列 -> getWestInStNumOpSeries


# 获取营业利润预测机构家数(可选类型) -> getWestInStNumOp


# 获取预测营业成本平均值(可选类型)时间序列 -> getWestAvgOcSeries


# 获取预测营业成本平均值(可选类型) -> getWestAvgOc


# 获取预测营业成本最大值(可选类型)时间序列 -> getWestMaxOcSeries


# 获取预测营业成本最大值(可选类型) -> getWestMaxOc


# 获取预测营业成本最小值(可选类型)时间序列 -> getWestMinoCSeries


# 获取预测营业成本最小值(可选类型) -> getWestMinoC


# 获取预测营业成本中值(可选类型)时间序列 -> getWestMediaOcSeries


# 获取预测营业成本中值(可选类型) -> getWestMediaOc


# 获取预测营业成本标准差(可选类型)时间序列 -> getWestSToCSeries


# 获取预测营业成本标准差(可选类型) -> getWestSToC


# 获取预测基准股本综合值(可选类型)时间序列 -> getWestAvgSharesSeries


# 获取预测基准股本综合值(可选类型) -> getWestAvgShares


# 获取盈利修正比例(可选类型)时间序列 -> getErrWiSeries


# 获取盈利修正比例(可选类型) -> getErrWi


# 获取未来3年净利润复合年增长率时间序列 -> getEstCAgrNpSeries


# 获取未来3年净利润复合年增长率 -> getEstCAgrNp


# 获取未来3年营业总收入复合年增长率时间序列 -> getEstCAgrSalesSeries


# 获取未来3年营业总收入复合年增长率 -> getEstCAgrSales


# 获取销售毛利率预测机构家数(可选类型)时间序列 -> getWestInStNumGmSeries


# 获取销售毛利率预测机构家数(可选类型) -> getWestInStNumGm


# 获取预测营业成本平均值(可选类型,币种转换)时间序列 -> getWestAvgOc1Series


# 获取预测营业成本平均值(可选类型,币种转换) -> getWestAvgOc1


# 获取预测营业成本最大值(可选类型,币种转换)时间序列 -> getWestMaxOc1Series


# 获取预测营业成本最大值(可选类型,币种转换) -> getWestMaxOc1


# 获取预测营业成本最小值(可选类型,币种转换)时间序列 -> getWestMinoC1Series


# 获取预测营业成本最小值(可选类型,币种转换) -> getWestMinoC1


# 获取预测营业成本中值(可选类型,币种转换)时间序列 -> getWestMediaOc1Series


# 获取预测营业成本中值(可选类型,币种转换) -> getWestMediaOc1


# 获取预测营业成本标准差(可选类型,币种转换)时间序列 -> getWestSToC1Series


# 获取预测营业成本标准差(可选类型,币种转换) -> getWestSToC1


# 获取前次最低目标价时间序列 -> getEstPreLowPriceInStSeries


# 获取前次最低目标价 -> getEstPreLowPriceInSt


# 获取前次最高目标价时间序列 -> getEstPreHighPriceInStSeries


# 获取前次最高目标价 -> getEstPreHighPriceInSt


# 获取本次最低目标价时间序列 -> getEstLowPriceInStSeries


# 获取本次最低目标价 -> getEstLowPriceInSt


# 获取本次最高目标价时间序列 -> getEstHighPriceInStSeries


# 获取本次最高目标价 -> getEstHighPriceInSt


# 获取机构投资评级(原始)时间序列 -> getEstOrGratingInStSeries


# 获取机构投资评级(原始) -> getEstOrGratingInSt


# 获取机构投资评级(标准化得分)时间序列 -> getEstScoreRatingInStSeries


# 获取机构投资评级(标准化得分) -> getEstScoreRatingInSt


# 获取机构投资评级(标准化评级)时间序列 -> getEstStdRatingInStSeries


# 获取机构投资评级(标准化评级) -> getEstStdRatingInSt


# 获取机构最近评级时间时间序列 -> getEstNewRatingTimeInStSeries


# 获取机构最近评级时间 -> getEstNewRatingTimeInSt


# 获取机构最近预测时间时间序列 -> getEstEstNewTimeInStSeries


# 获取机构最近预测时间 -> getEstEstNewTimeInSt


# 获取机构预测营业收入时间序列 -> getEstSalesInStSeries


# 获取机构预测营业收入 -> getEstSalesInSt


# 获取机构预测净利润时间序列 -> getEstNetProfitInStSeries


# 获取机构预测净利润 -> getEstNetProfitInSt


# 获取机构预测每股收益时间序列 -> getEstEpsInStSeries


# 获取机构预测每股收益 -> getEstEpsInSt


# 获取机构首次评级时间时间序列 -> getEstFrStRatingTimeInStSeries


# 获取机构首次评级时间 -> getEstFrStRatingTimeInSt


# 获取评级研究员时间序列 -> getEstRatingAnalystSeries


# 获取评级研究员 -> getEstRatingAnalyst


# 获取预测研究员时间序列 -> getEstEstAnalystSeries


# 获取预测研究员 -> getEstEstAnalyst


# 获取内容时间序列 -> getEstRpTAbstractInStSeries


# 获取内容 -> getEstRpTAbstractInSt


# 获取报告标题时间序列 -> getEstRpTTitleInStSeries


# 获取报告标题 -> getEstRpTTitleInSt


# 获取预告净利润变动幅度(%)时间序列 -> getProfitNoticeChangeSeries


# 获取预告净利润变动幅度(%) -> getProfitNoticeChange


# 获取去年同期每股收益时间序列 -> getProfitNoticeLaStepsSeries


# 获取去年同期每股收益 -> getProfitNoticeLaSteps


# 获取可分配利润时间序列 -> getStmNoteProfitApr3Series


# 获取可分配利润 -> getStmNoteProfitApr3


# 获取上年同期扣非净利润时间序列 -> getProfitNoticeLastYearDeductedProfitSeries


# 获取上年同期扣非净利润 -> getProfitNoticeLastYearDeductedProfit


# 获取上年同期营业收入时间序列 -> getProfitNoticeLastYearIncomeSeries


# 获取上年同期营业收入 -> getProfitNoticeLastYearIncome


# 获取上年同期扣除后营业收入时间序列 -> getProfitNoticeLastYearDeductedSalesSeries


# 获取上年同期扣除后营业收入 -> getProfitNoticeLastYearDeductedSales


# 获取预告基本每股收益下限时间序列 -> getProfitNoticeBasicEarnMaxSeries


# 获取预告基本每股收益下限 -> getProfitNoticeBasicEarnMax


# 获取预告基本每股收益上限时间序列 -> getProfitNoticeBasicEarnMinSeries


# 获取预告基本每股收益上限 -> getProfitNoticeBasicEarnMin


# 获取预告扣非后基本每股收益下限时间序列 -> getProfitNoticeDeductedEarnMinSeries


# 获取预告扣非后基本每股收益下限 -> getProfitNoticeDeductedEarnMin


# 获取预告扣非后基本每股收益上限时间序列 -> getProfitNoticeDeductedEarnMaxSeries


# 获取预告扣非后基本每股收益上限 -> getProfitNoticeDeductedEarnMax


# 获取上年同期扣非后基本每股收益时间序列 -> getProfitNoticeLastYearDeductedEarnSeries


# 获取上年同期扣非后基本每股收益 -> getProfitNoticeLastYearDeductedEarn


# 获取预告净利润上限时间序列 -> getProfitNoticeNetProfitMaxSeries


# 获取预告净利润上限 -> getProfitNoticeNetProfitMax


# 获取单季度.预告净利润上限(海外)时间序列 -> getQProfitNoticeNetProfitMaxSeries


# 获取单季度.预告净利润上限(海外) -> getQProfitNoticeNetProfitMax


# 获取预告净利润下限时间序列 -> getProfitNoticeNetProfitMinSeries


# 获取预告净利润下限 -> getProfitNoticeNetProfitMin


# 获取单季度.预告净利润下限(海外)时间序列 -> getQProfitNoticeNetProfitMinSeries


# 获取单季度.预告净利润下限(海外) -> getQProfitNoticeNetProfitMin


# 获取预告净利润同比增长上限时间序列 -> getProfitNoticeChangeMaxSeries


# 获取预告净利润同比增长上限 -> getProfitNoticeChangeMax


# 获取单季度.预告净利润同比增长上限(海外)时间序列 -> getQProfitNoticeChangeMaxSeries


# 获取单季度.预告净利润同比增长上限(海外) -> getQProfitNoticeChangeMax


# 获取预告净利润同比增长下限时间序列 -> getProfitNoticeChangeMinSeries


# 获取预告净利润同比增长下限 -> getProfitNoticeChangeMin


# 获取单季度.预告净利润同比增长下限(海外)时间序列 -> getQProfitNoticeChangeMinSeries


# 获取单季度.预告净利润同比增长下限(海外) -> getQProfitNoticeChangeMin


# 获取预告扣非净利润上限时间序列 -> getProfitNoticeDeductedProfitMaxSeries


# 获取预告扣非净利润上限 -> getProfitNoticeDeductedProfitMax


# 获取预告扣非净利润下限时间序列 -> getProfitNoticeDeductedProfitMinSeries


# 获取预告扣非净利润下限 -> getProfitNoticeDeductedProfitMin


# 获取预告扣非净利润同比增长上限时间序列 -> getProfitNoticeDeductedProfitYoYMaxSeries


# 获取预告扣非净利润同比增长上限 -> getProfitNoticeDeductedProfitYoYMax


# 获取预告扣非净利润同比增长下限时间序列 -> getProfitNoticeDeductedProfitYoYMinSeries


# 获取预告扣非净利润同比增长下限 -> getProfitNoticeDeductedProfitYoYMin


# 获取预告营业收入上限时间序列 -> getProfitNoticeIncomeMaxSeries


# 获取预告营业收入上限 -> getProfitNoticeIncomeMax


# 获取预告营业收入下限时间序列 -> getProfitNoticeIncomeMinSeries


# 获取预告营业收入下限 -> getProfitNoticeIncomeMin


# 获取预告扣除后营业收入上限时间序列 -> getProfitNoticeDeductedSalesMaxSeries


# 获取预告扣除后营业收入上限 -> getProfitNoticeDeductedSalesMax


# 获取预告扣除后营业收入下限时间序列 -> getProfitNoticeDeductedSalesMinSeries


# 获取预告扣除后营业收入下限 -> getProfitNoticeDeductedSalesMin


# 获取预告净营收上限(海外)时间序列 -> getProfitNoticeNetSalesMaxSeries


# 获取预告净营收上限(海外) -> getProfitNoticeNetSalesMax


# 获取单季度.预告净营收上限(海外)时间序列 -> getQProfitNoticeNetSalesMaxSeries


# 获取单季度.预告净营收上限(海外) -> getQProfitNoticeNetSalesMax


# 获取预告净营收下限(海外)时间序列 -> getProfitNoticeNetSalesMinSeries


# 获取预告净营收下限(海外) -> getProfitNoticeNetSalesMin


# 获取单季度.预告净营收下限(海外)时间序列 -> getQProfitNoticeNetSalesMinSeries


# 获取单季度.预告净营收下限(海外) -> getQProfitNoticeNetSalesMin


# 获取预告净营收同比增长上限(海外)时间序列 -> getProfitNoticeNetSalesYoYMaxSeries


# 获取预告净营收同比增长上限(海外) -> getProfitNoticeNetSalesYoYMax


# 获取单季度.预告净营收同比增长上限(海外)时间序列 -> getQProfitNoticeNetSalesYoYMaxSeries


# 获取单季度.预告净营收同比增长上限(海外) -> getQProfitNoticeNetSalesYoYMax


# 获取预告净营收同比增长下限(海外)时间序列 -> getProfitNoticeNetSalesYoYMinSeries


# 获取预告净营收同比增长下限(海外) -> getProfitNoticeNetSalesYoYMin


# 获取单季度.预告净营收同比增长下限(海外)时间序列 -> getQProfitNoticeNetSalesYoYMinSeries


# 获取单季度.预告净营收同比增长下限(海外) -> getQProfitNoticeNetSalesYoYMin


# 获取预告总营收上限(海外)时间序列 -> getProfitNoticeSalesMaxSeries


# 获取预告总营收上限(海外) -> getProfitNoticeSalesMax


# 获取单季度.预告总营收上限(海外)时间序列 -> getQProfitNoticeSalesMaxSeries


# 获取单季度.预告总营收上限(海外) -> getQProfitNoticeSalesMax


# 获取预告总营收下限(海外)时间序列 -> getProfitNoticeSalesMinSeries


# 获取预告总营收下限(海外) -> getProfitNoticeSalesMin


# 获取单季度.预告总营收下限(海外)时间序列 -> getQProfitNoticeSalesMinSeries


# 获取单季度.预告总营收下限(海外) -> getQProfitNoticeSalesMin


# 获取预告总营收同比增长上限(海外)时间序列 -> getProfitNoticeSalesYoYMaxSeries


# 获取预告总营收同比增长上限(海外) -> getProfitNoticeSalesYoYMax


# 获取单季度.预告总营收同比增长上限(海外)时间序列 -> getQProfitNoticeSalesYoYMaxSeries


# 获取单季度.预告总营收同比增长上限(海外) -> getQProfitNoticeSalesYoYMax


# 获取预告总营收同比增长下限(海外)时间序列 -> getProfitNoticeSalesYoYMinSeries


# 获取预告总营收同比增长下限(海外) -> getProfitNoticeSalesYoYMin


# 获取单季度.预告总营收同比增长下限(海外)时间序列 -> getQProfitNoticeSalesYoYMinSeries


# 获取单季度.预告总营收同比增长下限(海外) -> getQProfitNoticeSalesYoYMin


# 获取现金流量利息保障倍数时间序列 -> getOCFToInterestSeries


# 获取现金流量利息保障倍数 -> getOCFToInterest


# 获取每股现金流量净额(TTM)_PIT时间序列 -> getFaCfpSTtMSeries


# 获取每股现金流量净额(TTM)_PIT -> getFaCfpSTtM


# 获取每股现金流量净额时间序列 -> getCfpSSeries


# 获取每股现金流量净额 -> getCfpS


# 获取每股现金流量净额_GSD时间序列 -> getWgsDCfpSSeries


# 获取每股现金流量净额_GSD -> getWgsDCfpS


# 获取其他现金流量调整_GSD时间序列 -> getWgsDCashBalChgCfSeries


# 获取其他现金流量调整_GSD -> getWgsDCashBalChgCf


# 获取企业自由现金流量FCFF时间序列 -> getFcFfSeries


# 获取企业自由现金流量FCFF -> getFcFf


# 获取股权自由现金流量FCFE时间序列 -> getFcFeSeries


# 获取股权自由现金流量FCFE -> getFcFe


# 获取股权自由现金流量FCFE_GSD时间序列 -> getWgsDFcFe2Series


# 获取股权自由现金流量FCFE_GSD -> getWgsDFcFe2


# 获取企业自由现金流量_GSD时间序列 -> getWgsDFcFf2Series


# 获取企业自由现金流量_GSD -> getWgsDFcFf2


# 获取企业自由现金流量_PIT时间序列 -> getFaFcFfSeries


# 获取企业自由现金流量_PIT -> getFaFcFf


# 获取股权自由现金流量_PIT时间序列 -> getFaFcFeSeries


# 获取股权自由现金流量_PIT -> getFaFcFe


# 获取增长率-净现金流量(TTM)_PIT时间序列 -> getFaNcGrTtMSeries


# 获取增长率-净现金流量(TTM)_PIT -> getFaNcGrTtM


# 获取每股企业自由现金流量时间序列 -> getFcFFpsSeries


# 获取每股企业自由现金流量 -> getFcFFps


# 获取每股股东自由现金流量时间序列 -> getFcFEpsSeries


# 获取每股股东自由现金流量 -> getFcFEps


# 获取每股企业自由现金流量_GSD时间序列 -> getWgsDFcFFps2Series


# 获取每股企业自由现金流量_GSD -> getWgsDFcFFps2


# 获取每股股东自由现金流量_GSD时间序列 -> getWgsDFcFEps2Series


# 获取每股股东自由现金流量_GSD -> getWgsDFcFEps2


# 获取单季度.其他现金流量调整_GSD时间序列 -> getWgsDQfaCashBalChgCfSeries


# 获取单季度.其他现金流量调整_GSD -> getWgsDQfaCashBalChgCf


# 获取每股企业自由现金流量_PIT时间序列 -> getFaFcFFpsSeries


# 获取每股企业自由现金流量_PIT -> getFaFcFFps


# 获取每股股东自由现金流量_PIT时间序列 -> getFaFcFEpsSeries


# 获取每股股东自由现金流量_PIT -> getFaFcFEps


# 获取经营活动产生现金流量净额/带息债务(TTM)_PIT时间序列 -> getFaOCFToInterestDebtTtMSeries


# 获取经营活动产生现金流量净额/带息债务(TTM)_PIT -> getFaOCFToInterestDebtTtM


# 获取经营活动产生现金流量净额/净债务(TTM)_PIT时间序列 -> getFaOCFToNetDebtTtMSeries


# 获取经营活动产生现金流量净额/净债务(TTM)_PIT -> getFaOCFToNetDebtTtM


# 获取经营活动产生的现金流量净额/营业收入时间序列 -> getOCFToOrSeries


# 获取经营活动产生的现金流量净额/营业收入 -> getOCFToOr


# 获取经营活动产生的现金流量净额/经营活动净收益时间序列 -> getOCFToOperateIncomeSeries


# 获取经营活动产生的现金流量净额/经营活动净收益 -> getOCFToOperateIncome


# 获取经营活动产生的现金流量净额占比时间序列 -> getOCFTOCFSeries


# 获取经营活动产生的现金流量净额占比 -> getOCFTOCF


# 获取投资活动产生的现金流量净额占比时间序列 -> getICfTOCFSeries


# 获取投资活动产生的现金流量净额占比 -> getICfTOCF


# 获取筹资活动产生的现金流量净额占比时间序列 -> getFcFTOCFSeries


# 获取筹资活动产生的现金流量净额占比 -> getFcFTOCF


# 获取经营活动产生的现金流量净额/负债合计时间序列 -> getOCFToDebtSeries


# 获取经营活动产生的现金流量净额/负债合计 -> getOCFToDebt


# 获取经营活动产生的现金流量净额/带息债务时间序列 -> getOCFToInterestDebtSeries


# 获取经营活动产生的现金流量净额/带息债务 -> getOCFToInterestDebt


# 获取经营活动产生的现金流量净额/流动负债时间序列 -> getOCFToShortDebtSeries


# 获取经营活动产生的现金流量净额/流动负债 -> getOCFToShortDebt


# 获取经营活动产生的现金流量净额/非流动负债时间序列 -> getOCFToLongDebtSeries


# 获取经营活动产生的现金流量净额/非流动负债 -> getOCFToLongDebt


# 获取经营活动产生的现金流量净额/净债务时间序列 -> getOCFToNetDebtSeries


# 获取经营活动产生的现金流量净额/净债务 -> getOCFToNetDebt


# 获取经营活动产生的现金流量净额(同比增长率)时间序列 -> getYoyOCFSeries


# 获取经营活动产生的现金流量净额(同比增长率) -> getYoyOCF


# 获取经营活动产生的现金流量净额(N年,增长率)时间序列 -> getGrowthOCFSeries


# 获取经营活动产生的现金流量净额(N年,增长率) -> getGrowthOCF


# 获取经营活动产生的现金流量净额/营业收入(TTM)时间序列 -> getOCFToOrTtM2Series


# 获取经营活动产生的现金流量净额/营业收入(TTM) -> getOCFToOrTtM2


# 获取经营活动产生的现金流量净额/经营活动净收益(TTM)时间序列 -> getOCFToOperateIncomeTtM2Series


# 获取经营活动产生的现金流量净额/经营活动净收益(TTM) -> getOCFToOperateIncomeTtM2


# 获取经营活动产生的现金流量净额/营业利润(TTM)时间序列 -> getOperateCashFlowToOpTtMSeries


# 获取经营活动产生的现金流量净额/营业利润(TTM) -> getOperateCashFlowToOpTtM


# 获取经营活动产生的现金流量净额/营业收入_GSD时间序列 -> getWgsDOCFToSalesSeries


# 获取经营活动产生的现金流量净额/营业收入_GSD -> getWgsDOCFToSales


# 获取经营活动产生的现金流量净额/经营活动净收益_GSD时间序列 -> getWgsDOCFToOperateIncomeSeries


# 获取经营活动产生的现金流量净额/经营活动净收益_GSD -> getWgsDOCFToOperateIncome


# 获取经营活动产生的现金流量净额/流动负债_GSD时间序列 -> getWgsDOCFToLiqDebtSeries


# 获取经营活动产生的现金流量净额/流动负债_GSD -> getWgsDOCFToLiqDebt


# 获取经营活动产生的现金流量净额/负债合计_GSD时间序列 -> getWgsDOCFToDebtSeries


# 获取经营活动产生的现金流量净额/负债合计_GSD -> getWgsDOCFToDebt


# 获取经营活动产生的现金流量净额/带息债务_GSD时间序列 -> getWgsDOCFToInterestDebtSeries


# 获取经营活动产生的现金流量净额/带息债务_GSD -> getWgsDOCFToInterestDebt


# 获取经营活动产生的现金流量净额/净债务_GSD时间序列 -> getWgsDOCFToNetDebtSeries


# 获取经营活动产生的现金流量净额/净债务_GSD -> getWgsDOCFToNetDebt


# 获取经营活动产生的现金流量净额(同比增长率)_GSD时间序列 -> getWgsDYoyOCFSeries


# 获取经营活动产生的现金流量净额(同比增长率)_GSD -> getWgsDYoyOCF


# 获取经营活动产生的现金流量净额(N年,增长率)_GSD时间序列 -> getWgsDGrowthOCFSeries


# 获取经营活动产生的现金流量净额(N年,增长率)_GSD -> getWgsDGrowthOCF


# 获取经营活动产生的现金流量净额/经营活动净收益(TTM)_GSD时间序列 -> getOCFToOperateIncomeTtM3Series


# 获取经营活动产生的现金流量净额/经营活动净收益(TTM)_GSD -> getOCFToOperateIncomeTtM3


# 获取经营活动产生的现金流量净额/营业利润(TTM)_GSD时间序列 -> getOperateCashFlowToOpTtM2Series


# 获取经营活动产生的现金流量净额/营业利润(TTM)_GSD -> getOperateCashFlowToOpTtM2


# 获取经营活动产生的现金流量净额/营业收入(TTM)_GSD时间序列 -> getOCFToSalesTtM2Series


# 获取经营活动产生的现金流量净额/营业收入(TTM)_GSD -> getOCFToSalesTtM2


# 获取经营活动产生的现金流量净额_GSD时间序列 -> getWgsDOperCfSeries


# 获取经营活动产生的现金流量净额_GSD -> getWgsDOperCf


# 获取投资活动产生的现金流量净额_GSD时间序列 -> getWgsDInvestCfSeries


# 获取投资活动产生的现金流量净额_GSD -> getWgsDInvestCf


# 获取筹资活动产生的现金流量净额_GSD时间序列 -> getWgsDFinCfSeries


# 获取筹资活动产生的现金流量净额_GSD -> getWgsDFinCf


# 获取经营活动产生的现金流量净额差额(合计平衡项目)时间序列 -> getCfOperActNettingSeries


# 获取经营活动产生的现金流量净额差额(合计平衡项目) -> getCfOperActNetting


# 获取经营活动产生的现金流量净额时间序列 -> getStm07CsReItsOperNetCashSeries


# 获取经营活动产生的现金流量净额 -> getStm07CsReItsOperNetCash


# 获取投资活动产生的现金流量净额差额(合计平衡项目)时间序列 -> getCfInvActNettingSeries


# 获取投资活动产生的现金流量净额差额(合计平衡项目) -> getCfInvActNetting


# 获取投资活动产生的现金流量净额时间序列 -> getStm07CsReItsInvestNetCashSeries


# 获取投资活动产生的现金流量净额 -> getStm07CsReItsInvestNetCash


# 获取筹资活动产生的现金流量净额差额(合计平衡项目)时间序列 -> getCfFncActNettingSeries


# 获取筹资活动产生的现金流量净额差额(合计平衡项目) -> getCfFncActNetting


# 获取筹资活动产生的现金流量净额时间序列 -> getStm07CsReItsFinanceNetCashSeries


# 获取筹资活动产生的现金流量净额 -> getStm07CsReItsFinanceNetCash


# 获取经营活动产生的现金流量净额/营业收入_PIT时间序列 -> getFaOCFToOrSeries


# 获取经营活动产生的现金流量净额/营业收入_PIT -> getFaOCFToOr


# 获取经营活动产生的现金流量净额/营业收入(TTM)_PIT时间序列 -> getFaOCFToOrTtMSeries


# 获取经营活动产生的现金流量净额/营业收入(TTM)_PIT -> getFaOCFToOrTtM


# 获取经营活动产生的现金流量净额/经营活动净收益(TTM)_PIT时间序列 -> getFaOCFTooAITtMSeries


# 获取经营活动产生的现金流量净额/经营活动净收益(TTM)_PIT -> getFaOCFTooAITtM


# 获取经营活动产生的现金流量净额/营业利润(TTM)_PIT时间序列 -> getFaOCFToOpTtMSeries


# 获取经营活动产生的现金流量净额/营业利润(TTM)_PIT -> getFaOCFToOpTtM


# 获取经营活动产生的现金流量净额/负债合计_PIT时间序列 -> getFaOCFToDebtSeries


# 获取经营活动产生的现金流量净额/负债合计_PIT -> getFaOCFToDebt


# 获取经营活动产生的现金流量净额/营业收入(TTM,只有最新数据)时间序列 -> getOCFToOrTtMSeries


# 获取经营活动产生的现金流量净额/营业收入(TTM,只有最新数据) -> getOCFToOrTtM


# 获取经营活动产生的现金流量净额/经营活动净收益(TTM,只有最新数据)时间序列 -> getOCFToOperateIncomeTtMSeries


# 获取经营活动产生的现金流量净额/经营活动净收益(TTM,只有最新数据) -> getOCFToOperateIncomeTtM


# 获取间接法-经营活动现金流量净额差额(特殊报表科目)时间序列 -> getImNetCashFlowsOperActGapSeries


# 获取间接法-经营活动现金流量净额差额(特殊报表科目) -> getImNetCashFlowsOperActGap


# 获取间接法-经营活动现金流量净额差额说明(特殊报表科目)时间序列 -> getImNetCashFlowsOperActGapDetailSeries


# 获取间接法-经营活动现金流量净额差额说明(特殊报表科目) -> getImNetCashFlowsOperActGapDetail


# 获取间接法-经营活动现金流量净额差额(合计平衡项目)时间序列 -> getImNetCashFlowsOperActNettingSeries


# 获取间接法-经营活动现金流量净额差额(合计平衡项目) -> getImNetCashFlowsOperActNetting


# 获取每股经营活动产生的现金流量净额(TTM)_PIT时间序列 -> getFaOcFpsTtMSeries


# 获取每股经营活动产生的现金流量净额(TTM)_PIT -> getFaOcFpsTtM


# 获取每股经营活动产生的现金流量净额时间序列 -> getOcFpsSeries


# 获取每股经营活动产生的现金流量净额 -> getOcFps


# 获取每股经营活动产生的现金流量净额(同比增长率)时间序列 -> getYoyOCFpSSeries


# 获取每股经营活动产生的现金流量净额(同比增长率) -> getYoyOCFpS


# 获取每股经营活动产生的现金流量净额(同比增长率)_GSD时间序列 -> getWgsDYoyOCFpSSeries


# 获取每股经营活动产生的现金流量净额(同比增长率)_GSD -> getWgsDYoyOCFpS


# 获取其他投资活动产生的现金流量净额_GSD时间序列 -> getWgsDInvestOThCfSeries


# 获取其他投资活动产生的现金流量净额_GSD -> getWgsDInvestOThCf


# 获取其他筹资活动产生的现金流量净额_GSD时间序列 -> getWgsDFinOThCfSeries


# 获取其他筹资活动产生的现金流量净额_GSD -> getWgsDFinOThCf


# 获取单季度.经营活动产生的现金流量净额/营业收入时间序列 -> getQfaOCFToSalesSeries


# 获取单季度.经营活动产生的现金流量净额/营业收入 -> getQfaOCFToSales


# 获取单季度.经营活动产生的现金流量净额/经营活动净收益时间序列 -> getQfaOCFToOrSeries


# 获取单季度.经营活动产生的现金流量净额/经营活动净收益 -> getQfaOCFToOr


# 获取单季度.经营活动产生的现金流量净额占比时间序列 -> getOCFTOCFQfaSeries


# 获取单季度.经营活动产生的现金流量净额占比 -> getOCFTOCFQfa


# 获取单季度.投资活动产生的现金流量净额占比时间序列 -> getICfTOCFQfaSeries


# 获取单季度.投资活动产生的现金流量净额占比 -> getICfTOCFQfa


# 获取单季度.筹资活动产生的现金流量净额占比时间序列 -> getFcFTOCFQfaSeries


# 获取单季度.筹资活动产生的现金流量净额占比 -> getFcFTOCFQfa


# 获取单季度.经营活动产生的现金流量净额_GSD时间序列 -> getWgsDQfaOperCfSeries


# 获取单季度.经营活动产生的现金流量净额_GSD -> getWgsDQfaOperCf


# 获取单季度.投资活动产生的现金流量净额_GSD时间序列 -> getWgsDQfaInvestCfSeries


# 获取单季度.投资活动产生的现金流量净额_GSD -> getWgsDQfaInvestCf


# 获取单季度.筹资活动产生的现金流量净额_GSD时间序列 -> getWgsDQfaFinCfSeries


# 获取单季度.筹资活动产生的现金流量净额_GSD -> getWgsDQfaFinCf


# 获取间接法-经营活动产生的现金流量净额时间序列 -> getImNetCashFlowsOperActSeries


# 获取间接法-经营活动产生的现金流量净额 -> getImNetCashFlowsOperAct


# 获取单季度.经营活动产生的现金流量净额时间序列 -> getQfaNetCashFlowsOperActSeries


# 获取单季度.经营活动产生的现金流量净额 -> getQfaNetCashFlowsOperAct


# 获取单季度.投资活动产生的现金流量净额时间序列 -> getQfaNetCashFlowsInvActSeries


# 获取单季度.投资活动产生的现金流量净额 -> getQfaNetCashFlowsInvAct


# 获取单季度.筹资活动产生的现金流量净额时间序列 -> getQfaNetCashFlowsFncActSeries


# 获取单季度.筹资活动产生的现金流量净额 -> getQfaNetCashFlowsFncAct


# 获取增长率-经营活动产生的现金流量净额(TTM)_PIT时间序列 -> getFaCFogRTtMSeries


# 获取增长率-经营活动产生的现金流量净额(TTM)_PIT -> getFaCFogRTtM


# 获取增长率-筹资活动产生的现金流量净额(TTM)_PIT时间序列 -> getFaCffGrTtMSeries


# 获取增长率-筹资活动产生的现金流量净额(TTM)_PIT -> getFaCffGrTtM


# 获取增长率-投资活动产生的现金流量净额(TTM)_PIT时间序列 -> getFaCFigRTtMSeries


# 获取增长率-投资活动产生的现金流量净额(TTM)_PIT -> getFaCFigRTtM


# 获取单季度.其他投资活动产生的现金流量净额_GSD时间序列 -> getWgsDQfaInvestOThCfSeries


# 获取单季度.其他投资活动产生的现金流量净额_GSD -> getWgsDQfaInvestOThCf


# 获取单季度.其他筹资活动产生的现金流量净额_GSD时间序列 -> getWgsDQfaFinOThCfSeries


# 获取单季度.其他筹资活动产生的现金流量净额_GSD -> getWgsDQfaFinOThCf


# 获取单季度.间接法-经营活动产生的现金流量净额时间序列 -> getQfaImNetCashFlowsOperActSeries


# 获取单季度.间接法-经营活动产生的现金流量净额 -> getQfaImNetCashFlowsOperAct


# 获取权益乘数(杜邦分析)时间序列 -> getDupontAssetsToEquitySeries


# 获取权益乘数(杜邦分析) -> getDupontAssetsToEquity


# 获取权益乘数(杜邦分析)_GSD时间序列 -> getWgsDDupontAssetsToEquitySeries


# 获取权益乘数(杜邦分析)_GSD -> getWgsDDupontAssetsToEquity


# 获取主营构成(按行业)-项目名称时间序列 -> getSegmentIndustryItemSeries


# 获取主营构成(按行业)-项目名称 -> getSegmentIndustryItem


# 获取主营构成(按行业)-项目收入时间序列 -> getSegmentIndustrySales1Series


# 获取主营构成(按行业)-项目收入 -> getSegmentIndustrySales1


# 获取主营构成(按行业)-项目成本时间序列 -> getSegmentIndustryCost1Series


# 获取主营构成(按行业)-项目成本 -> getSegmentIndustryCost1


# 获取主营构成(按行业)-项目毛利时间序列 -> getSegmentIndustryProfit1Series


# 获取主营构成(按行业)-项目毛利 -> getSegmentIndustryProfit1


# 获取主营构成(按行业)-项目毛利率时间序列 -> getSegmentIndustryGpMarginSeries


# 获取主营构成(按行业)-项目毛利率 -> getSegmentIndustryGpMargin


# 获取主营构成(按产品)-项目名称时间序列 -> getSegmentProductItemSeries


# 获取主营构成(按产品)-项目名称 -> getSegmentProductItem


# 获取主营构成(按产品)-项目收入时间序列 -> getSegmentProductSales1Series


# 获取主营构成(按产品)-项目收入 -> getSegmentProductSales1


# 获取主营构成(按产品)-项目成本时间序列 -> getSegmentProductCost1Series


# 获取主营构成(按产品)-项目成本 -> getSegmentProductCost1


# 获取主营构成(按产品)-项目毛利时间序列 -> getSegmentProductProfit1Series


# 获取主营构成(按产品)-项目毛利 -> getSegmentProductProfit1


# 获取主营构成(按产品)-项目毛利率时间序列 -> getSegmentProductGpMarginSeries


# 获取主营构成(按产品)-项目毛利率 -> getSegmentProductGpMargin


# 获取主营构成(按地区)-项目名称时间序列 -> getSegmentRegionItemSeries


# 获取主营构成(按地区)-项目名称 -> getSegmentRegionItem


# 获取主营构成(按地区)-项目收入时间序列 -> getSegmentRegionSales1Series


# 获取主营构成(按地区)-项目收入 -> getSegmentRegionSales1


# 获取主营构成(按地区)-项目成本时间序列 -> getSegmentRegionCost1Series


# 获取主营构成(按地区)-项目成本 -> getSegmentRegionCost1


# 获取主营构成(按地区)-项目毛利时间序列 -> getSegmentRegionProfit1Series


# 获取主营构成(按地区)-项目毛利 -> getSegmentRegionProfit1


# 获取主营构成(按地区)-项目毛利率时间序列 -> getSegmentRegionGpMarginSeries


# 获取主营构成(按地区)-项目毛利率 -> getSegmentRegionGpMargin


# 获取主营构成(按行业)-项目收入(旧)时间序列 -> getSegmentIndustrySalesSeries


# 获取主营构成(按行业)-项目收入(旧) -> getSegmentIndustrySales


# 获取主营构成(按行业)-项目成本(旧)时间序列 -> getSegmentIndustryCostSeries


# 获取主营构成(按行业)-项目成本(旧) -> getSegmentIndustryCost


# 获取主营构成(按行业)-项目毛利(旧)时间序列 -> getSegmentIndustryProfitSeries


# 获取主营构成(按行业)-项目毛利(旧) -> getSegmentIndustryProfit


# 获取主营构成(按产品)-项目收入(旧)时间序列 -> getSegmentProductSalesSeries


# 获取主营构成(按产品)-项目收入(旧) -> getSegmentProductSales


# 获取主营构成(按产品)-项目成本(旧)时间序列 -> getSegmentProductCostSeries


# 获取主营构成(按产品)-项目成本(旧) -> getSegmentProductCost


# 获取主营构成(按产品)-项目毛利(旧)时间序列 -> getSegmentProductProfitSeries


# 获取主营构成(按产品)-项目毛利(旧) -> getSegmentProductProfit


# 获取主营构成(按地区)-项目收入(旧)时间序列 -> getSegmentRegionSalesSeries


# 获取主营构成(按地区)-项目收入(旧) -> getSegmentRegionSales


# 获取主营构成(按地区)-项目成本(旧)时间序列 -> getSegmentRegionCostSeries


# 获取主营构成(按地区)-项目成本(旧) -> getSegmentRegionCost


# 获取主营构成(按地区)-项目毛利(旧)时间序列 -> getSegmentRegionProfitSeries


# 获取主营构成(按地区)-项目毛利(旧) -> getSegmentRegionProfit


# 获取审计意见类别时间序列 -> getStmNoteAuditCategorySeries


# 获取审计意见类别 -> getStmNoteAuditCategory


# 获取内控_审计意见类别时间序列 -> getStmNoteInAuditCategorySeries


# 获取内控_审计意见类别 -> getStmNoteInAuditCategory


# 获取资产减值准备时间序列 -> getProvDePrAssetsSeries


# 获取资产减值准备 -> getProvDePrAssets


# 获取资产减值准备(非经常性损益)时间序列 -> getStmNoteEoItems13Series


# 获取资产减值准备(非经常性损益) -> getStmNoteEoItems13


# 获取固定资产减值准备合计时间序列 -> getStmNoteReserve21Series


# 获取固定资产减值准备合计 -> getStmNoteReserve21


# 获取固定资产减值准备-房屋、建筑物时间序列 -> getStmNoteReserve22Series


# 获取固定资产减值准备-房屋、建筑物 -> getStmNoteReserve22


# 获取固定资产减值准备-机器设备时间序列 -> getStmNoteReserve23Series


# 获取固定资产减值准备-机器设备 -> getStmNoteReserve23


# 获取固定资产减值准备-专用设备时间序列 -> getStmNoteReserve24Series


# 获取固定资产减值准备-专用设备 -> getStmNoteReserve24


# 获取固定资产减值准备-运输工具时间序列 -> getStmNoteReserve25Series


# 获取固定资产减值准备-运输工具 -> getStmNoteReserve25


# 获取固定资产减值准备-通讯设备时间序列 -> getStmNoteReserve26Series


# 获取固定资产减值准备-通讯设备 -> getStmNoteReserve26


# 获取固定资产减值准备-电子设备时间序列 -> getStmNoteReserve27Series


# 获取固定资产减值准备-电子设备 -> getStmNoteReserve27


# 获取固定资产减值准备-办公及其它设备时间序列 -> getStmNoteReserve28Series


# 获取固定资产减值准备-办公及其它设备 -> getStmNoteReserve28


# 获取固定资产减值准备-其它设备时间序列 -> getStmNoteReserve29Series


# 获取固定资产减值准备-其它设备 -> getStmNoteReserve29


# 获取无形资产减值准备时间序列 -> getStmNoteReserve30Series


# 获取无形资产减值准备 -> getStmNoteReserve30


# 获取无形资产减值准备-专利权时间序列 -> getStmNoteReserve31Series


# 获取无形资产减值准备-专利权 -> getStmNoteReserve31


# 获取无形资产减值准备-商标权时间序列 -> getStmNoteReserve32Series


# 获取无形资产减值准备-商标权 -> getStmNoteReserve32


# 获取无形资产减值准备-职工住房使用权时间序列 -> getStmNoteReserve33Series


# 获取无形资产减值准备-职工住房使用权 -> getStmNoteReserve33


# 获取无形资产减值准备-土地使用权时间序列 -> getStmNoteReserve34Series


# 获取无形资产减值准备-土地使用权 -> getStmNoteReserve34


# 获取计提投资资产减值准备时间序列 -> getStmNoteInvestmentIncome0007Series


# 获取计提投资资产减值准备 -> getStmNoteInvestmentIncome0007


# 获取单季度.资产减值准备时间序列 -> getQfaProvDePrAssetsSeries


# 获取单季度.资产减值准备 -> getQfaProvDePrAssets


# 获取土地使用权_GSD时间序列 -> getWgsDLandUseRightsSeries


# 获取土地使用权_GSD -> getWgsDLandUseRights


# 获取土地使用权_原值时间序列 -> getStmNoteLandUseRights19Series


# 获取土地使用权_原值 -> getStmNoteLandUseRights19


# 获取土地使用权_累计摊销时间序列 -> getStmNoteLandUseRights20Series


# 获取土地使用权_累计摊销 -> getStmNoteLandUseRights20


# 获取土地使用权_减值准备时间序列 -> getStmNoteLandUseRights21Series


# 获取土地使用权_减值准备 -> getStmNoteLandUseRights21


# 获取土地使用权_账面价值时间序列 -> getStmNoteLandUseRights22Series


# 获取土地使用权_账面价值 -> getStmNoteLandUseRights22


# 获取买入返售金融资产时间序列 -> getPrtReverseRepoSeries


# 获取买入返售金融资产 -> getPrtReverseRepo


# 获取买入返售金融资产:证券时间序列 -> getStmNoteSPuAr0001Series


# 获取买入返售金融资产:证券 -> getStmNoteSPuAr0001


# 获取买入返售金融资产:票据时间序列 -> getStmNoteSPuAr0002Series


# 获取买入返售金融资产:票据 -> getStmNoteSPuAr0002


# 获取买入返售金融资产:贷款时间序列 -> getStmNoteSPuAr0003Series


# 获取买入返售金融资产:贷款 -> getStmNoteSPuAr0003


# 获取买入返售金融资产:信托及其他受益权时间序列 -> getStmNoteSPuAr0004Series


# 获取买入返售金融资产:信托及其他受益权 -> getStmNoteSPuAr0004


# 获取买入返售金融资产:长期应收款时间序列 -> getStmNoteSPuAr0005Series


# 获取买入返售金融资产:长期应收款 -> getStmNoteSPuAr0005


# 获取买入返售金融资产:其他担保物时间序列 -> getStmNoteSPuAr0006Series


# 获取买入返售金融资产:其他担保物 -> getStmNoteSPuAr0006


# 获取买入返售金融资产:减值准备时间序列 -> getStmNoteSPuAr0007Series


# 获取买入返售金融资产:减值准备 -> getStmNoteSPuAr0007


# 获取买入返售金融资产:股票质押式回购时间序列 -> getStmNoteSPuAr10001Series


# 获取买入返售金融资产:股票质押式回购 -> getStmNoteSPuAr10001


# 获取买入返售金融资产:约定购回式证券时间序列 -> getStmNoteSPuAr10002Series


# 获取买入返售金融资产:约定购回式证券 -> getStmNoteSPuAr10002


# 获取买入返售金融资产:债券买断式回购时间序列 -> getStmNoteSPuAr10003Series


# 获取买入返售金融资产:债券买断式回购 -> getStmNoteSPuAr10003


# 获取买入返售金融资产:债券质押式回购时间序列 -> getStmNoteSPuAr10004Series


# 获取买入返售金融资产:债券质押式回购 -> getStmNoteSPuAr10004


# 获取买入返售金融资产:债券回购时间序列 -> getStmNoteSPuAr10007Series


# 获取买入返售金融资产:债券回购 -> getStmNoteSPuAr10007


# 获取买入返售金融资产:其他时间序列 -> getStmNoteSPuAr10005Series


# 获取买入返售金融资产:其他 -> getStmNoteSPuAr10005


# 获取买入返售金融资产合计时间序列 -> getStmNoteSPuAr10006Series


# 获取买入返售金融资产合计 -> getStmNoteSPuAr10006


# 获取买入返售金融资产_FUND时间序列 -> getStmBs17Series


# 获取买入返售金融资产_FUND -> getStmBs17


# 获取买入返售金融资产(交易所市场)_FUND时间序列 -> getStmBsRepoInExChMktSeries


# 获取买入返售金融资产(交易所市场)_FUND -> getStmBsRepoInExChMkt


# 获取买入返售金融资产(银行间市场)_FUND时间序列 -> getStmBsRepoInInterBmkTSeries


# 获取买入返售金融资产(银行间市场)_FUND -> getStmBsRepoInInterBmkT


# 获取买入返售金融资产收入_FUND时间序列 -> getStmIs3Series


# 获取买入返售金融资产收入_FUND -> getStmIs3


# 获取可供出售金融资产时间序列 -> getFinAssetsAvailForSaleSeries


# 获取可供出售金融资产 -> getFinAssetsAvailForSale


# 获取可供出售金融资产:产生的利得/(损失)时间序列 -> getStmNoteFaaViableForSale0001Series


# 获取可供出售金融资产:产生的利得/(损失) -> getStmNoteFaaViableForSale0001


# 获取可供出售金融资产:产生的所得税影响时间序列 -> getStmNoteFaaViableForSale0002Series


# 获取可供出售金融资产:产生的所得税影响 -> getStmNoteFaaViableForSale0002


# 获取可供出售金融资产:前期计入其他综合收益当期转入损益的金额时间序列 -> getStmNoteFaaViableForSale0003Series


# 获取可供出售金融资产:前期计入其他综合收益当期转入损益的金额 -> getStmNoteFaaViableForSale0003


# 获取可供出售金融资产公允价值变动时间序列 -> getStmNoteFaaViableForSale0004Series


# 获取可供出售金融资产公允价值变动 -> getStmNoteFaaViableForSale0004


# 获取可供出售金融资产减值损失时间序列 -> getStmNoteImpairmentLoss8Series


# 获取可供出售金融资产减值损失 -> getStmNoteImpairmentLoss8


# 获取处置可供出售金融资产净增加额时间序列 -> getNetInCrDispFinAssetsAvailSeries


# 获取处置可供出售金融资产净增加额 -> getNetInCrDispFinAssetsAvail


# 获取融出证券:可供出售金融资产时间序列 -> getStmNoteSecuritiesLending3Series


# 获取融出证券:可供出售金融资产 -> getStmNoteSecuritiesLending3


# 获取单季度.处置可供出售金融资产净增加额时间序列 -> getQfaNetInCrDispFinAssetsAvailSeries


# 获取单季度.处置可供出售金融资产净增加额 -> getQfaNetInCrDispFinAssetsAvail


# 获取融出证券合计时间序列 -> getStmNoteSecuritiesLending1Series


# 获取融出证券合计 -> getStmNoteSecuritiesLending1


# 获取融出证券:交易性金融资产时间序列 -> getStmNoteSecuritiesLending2Series


# 获取融出证券:交易性金融资产 -> getStmNoteSecuritiesLending2


# 获取融出证券:转融通融入证券时间序列 -> getStmNoteSecuritiesLending4Series


# 获取融出证券:转融通融入证券 -> getStmNoteSecuritiesLending4


# 获取融出证券:转融通融入证券余额时间序列 -> getStmNoteSecuritiesLending5Series


# 获取融出证券:转融通融入证券余额 -> getStmNoteSecuritiesLending5


# 获取融出证券:减值准备时间序列 -> getStmNoteSecuritiesLending6Series


# 获取融出证券:减值准备 -> getStmNoteSecuritiesLending6


# 获取现金及存放中央银行款项时间序列 -> getCashDepositsCentralBankSeries


# 获取现金及存放中央银行款项 -> getCashDepositsCentralBank


# 获取银行存款_FUND时间序列 -> getStmBs1Series


# 获取银行存款_FUND -> getStmBs1


# 获取银行存款时间序列 -> getPrtCashSeries


# 获取银行存款 -> getPrtCash


# 获取银行存款占基金资产净值比时间序列 -> getPrtCashToNavSeries


# 获取银行存款占基金资产净值比 -> getPrtCashToNav


# 获取银行存款占基金资产总值比时间序列 -> getPrtCashToAssetSeries


# 获取银行存款占基金资产总值比 -> getPrtCashToAsset


# 获取银行存款市值增长率时间序列 -> getPrtCashValueGrowthSeries


# 获取银行存款市值增长率 -> getPrtCashValueGrowth


# 获取银行存款市值占基金资产净值比例增长时间序列 -> getPrtCashToNavGrowthSeries


# 获取银行存款市值占基金资产净值比例增长 -> getPrtCashToNavGrowth


# 获取货币资金-银行存款时间序列 -> getStmNoteBankDepositSeries


# 获取货币资金-银行存款 -> getStmNoteBankDeposit


# 获取货币资金/短期债务时间序列 -> getCashToStDebtSeries


# 获取货币资金/短期债务 -> getCashToStDebt


# 获取货币资金增长率时间序列 -> getYoYCashSeries


# 获取货币资金增长率 -> getYoYCash


# 获取货币资金/流动负债_GSD时间序列 -> getWgsDCashToLiqDebtSeries


# 获取货币资金/流动负债_GSD -> getWgsDCashToLiqDebt


# 获取货币资金时间序列 -> getStm07BsReItsCashSeries


# 获取货币资金 -> getStm07BsReItsCash


# 获取货币资金合计时间序列 -> getStmNoteDpsT4412Series


# 获取货币资金合计 -> getStmNoteDpsT4412


# 获取货币资金-库存现金时间序列 -> getStmNoteCashInvaultSeries


# 获取货币资金-库存现金 -> getStmNoteCashInvault


# 获取借款合计时间序列 -> getStmNoteBorrow4512Series


# 获取借款合计 -> getStmNoteBorrow4512


# 获取短期借款时间序列 -> getStBorrowSeries


# 获取短期借款 -> getStBorrow


# 获取长期借款时间序列 -> getLtBorrowSeries


# 获取长期借款 -> getLtBorrow


# 获取质押借款时间序列 -> getPledgeLoanSeries


# 获取质押借款 -> getPledgeLoan


# 获取取得借款收到的现金时间序列 -> getCashRecpBorrowSeries


# 获取取得借款收到的现金 -> getCashRecpBorrow


# 获取短期借款小计时间序列 -> getStmNoteStBorrow4512Series


# 获取短期借款小计 -> getStmNoteStBorrow4512


# 获取长期借款小计时间序列 -> getStmNoteLtBorrow4512Series


# 获取长期借款小计 -> getStmNoteLtBorrow4512


# 获取短期借款_FUND时间序列 -> getStmBs70Series


# 获取短期借款_FUND -> getStmBs70


# 获取长期借款/资产总计_PIT时间序列 -> getFaLtBorrowToAssetSeries


# 获取长期借款/资产总计_PIT -> getFaLtBorrowToAsset


# 获取国际商业借款比率时间序列 -> getBusLoanRatioNSeries


# 获取国际商业借款比率 -> getBusLoanRatioN


# 获取国际商业借款比率(旧)时间序列 -> getBusLoanRatioSeries


# 获取国际商业借款比率(旧) -> getBusLoanRatio


# 获取美元短期借款(折算人民币)时间序列 -> getStmNoteStBorrow4506Series


# 获取美元短期借款(折算人民币) -> getStmNoteStBorrow4506


# 获取日元短期借款(折算人民币)时间序列 -> getStmNoteStBorrow4507Series


# 获取日元短期借款(折算人民币) -> getStmNoteStBorrow4507


# 获取欧元短期借款(折算人民币)时间序列 -> getStmNoteStBorrow4508Series


# 获取欧元短期借款(折算人民币) -> getStmNoteStBorrow4508


# 获取港币短期借款(折算人民币)时间序列 -> getStmNoteStBorrow4509Series


# 获取港币短期借款(折算人民币) -> getStmNoteStBorrow4509


# 获取英镑短期借款(折算人民币)时间序列 -> getStmNoteStBorrow4510Series


# 获取英镑短期借款(折算人民币) -> getStmNoteStBorrow4510


# 获取美元长期借款(折算人民币)时间序列 -> getStmNoteLtBorrow4506Series


# 获取美元长期借款(折算人民币) -> getStmNoteLtBorrow4506


# 获取日元长期借款(折算人民币)时间序列 -> getStmNoteLtBorrow4507Series


# 获取日元长期借款(折算人民币) -> getStmNoteLtBorrow4507


# 获取欧元长期借款(折算人民币)时间序列 -> getStmNoteLtBorrow4508Series


# 获取欧元长期借款(折算人民币) -> getStmNoteLtBorrow4508


# 获取港币长期借款(折算人民币)时间序列 -> getStmNoteLtBorrow4509Series


# 获取港币长期借款(折算人民币) -> getStmNoteLtBorrow4509


# 获取英镑长期借款(折算人民币)时间序列 -> getStmNoteLtBorrow4510Series


# 获取英镑长期借款(折算人民币) -> getStmNoteLtBorrow4510


# 获取向中央银行借款时间序列 -> getBorrowCentralBankSeries


# 获取向中央银行借款 -> getBorrowCentralBank


# 获取向中央银行借款净增加额时间序列 -> getNetInCrLoansCentralBankSeries


# 获取向中央银行借款净增加额 -> getNetInCrLoansCentralBank


# 获取人民币短期借款时间序列 -> getStmNoteStBorrow4505Series


# 获取人民币短期借款 -> getStmNoteStBorrow4505


# 获取人民币长期借款时间序列 -> getStmNoteLtBorrow4505Series


# 获取人民币长期借款 -> getStmNoteLtBorrow4505


# 获取单季度.取得借款收到的现金时间序列 -> getQfaCashRecpBorrowSeries


# 获取单季度.取得借款收到的现金 -> getQfaCashRecpBorrow


# 获取其他货币短期借款(折算人民币)时间序列 -> getStmNoteStBorrow4511Series


# 获取其他货币短期借款(折算人民币) -> getStmNoteStBorrow4511


# 获取其他货币长期借款(折算人民币)时间序列 -> getStmNoteLtBorrow4511Series


# 获取其他货币长期借款(折算人民币) -> getStmNoteLtBorrow4511


# 获取一年内到期的长期借款时间序列 -> getStmNoteOthers7636Series


# 获取一年内到期的长期借款 -> getStmNoteOthers7636


# 获取单季度.向中央银行借款净增加额时间序列 -> getQfaNetInCrLoansCentralBankSeries


# 获取单季度.向中央银行借款净增加额 -> getQfaNetInCrLoansCentralBank


# 获取非经常性损益时间序列 -> getExtraordinarySeries


# 获取非经常性损益 -> getExtraordinary


# 获取非经常性损益项目小计时间序列 -> getStmNoteEoItems21Series


# 获取非经常性损益项目小计 -> getStmNoteEoItems21


# 获取非经常性损益项目合计时间序列 -> getStmNoteEoItems24Series


# 获取非经常性损益项目合计 -> getStmNoteEoItems24


# 获取非经常性损益_PIT时间序列 -> getFaNRglSeries


# 获取非经常性损益_PIT -> getFaNRgl


# 获取扣除非经常性损益后的净利润(TTM)_PIT时间序列 -> getFaDeductProfitTtMSeries


# 获取扣除非经常性损益后的净利润(TTM)_PIT -> getFaDeductProfitTtM


# 获取扣除非经常性损益后的净利润(同比增长率)时间序列 -> getDpYoYSeries


# 获取扣除非经常性损益后的净利润(同比增长率) -> getDpYoY


# 获取扣除非经常性损益后的净利润(TTM)时间序列 -> getDeductedProfitTtM2Series


# 获取扣除非经常性损益后的净利润(TTM) -> getDeductedProfitTtM2


# 获取扣除非经常性损益后的净利润时间序列 -> getDeductedProfitSeries


# 获取扣除非经常性损益后的净利润 -> getDeductedProfit


# 获取扣除非经常性损益后的净利润(TTM)_GSD时间序列 -> getDeductedProfitTtM3Series


# 获取扣除非经常性损益后的净利润(TTM)_GSD -> getDeductedProfitTtM3


# 获取单季度.扣除非经常性损益后的净利润同比增长率时间序列 -> getDeductedProfitYoYSeries


# 获取单季度.扣除非经常性损益后的净利润同比增长率 -> getDeductedProfitYoY


# 获取市盈率PE(TTM,扣除非经常性损益)时间序列 -> getValPeDeductedTtMSeries


# 获取市盈率PE(TTM,扣除非经常性损益) -> getValPeDeductedTtM


# 获取资产减值损失/营业总收入时间序列 -> getImpairToGrSeries


# 获取资产减值损失/营业总收入 -> getImpairToGr


# 获取资产减值损失/营业利润时间序列 -> getImpairToOpSeries


# 获取资产减值损失/营业利润 -> getImpairToOp


# 获取资产减值损失/营业总收入(TTM)时间序列 -> getImpairToGrTtM2Series


# 获取资产减值损失/营业总收入(TTM) -> getImpairToGrTtM2


# 获取资产减值损失(TTM)时间序列 -> getImpairmentTtM2Series


# 获取资产减值损失(TTM) -> getImpairmentTtM2


# 获取资产减值损失时间序列 -> getImpairLossAssetsSeries


# 获取资产减值损失 -> getImpairLossAssets


# 获取资产减值损失/营业总收入(TTM)_PIT时间序列 -> getFaImpairToGrTtMSeries


# 获取资产减值损失/营业总收入(TTM)_PIT -> getFaImpairToGrTtM


# 获取资产减值损失(TTM)_PIT时间序列 -> getFaImpairLossTtMSeries


# 获取资产减值损失(TTM)_PIT -> getFaImpairLossTtM


# 获取资产减值损失/营业总收入(TTM,只有最新数据)时间序列 -> getImpairToGrTtMSeries


# 获取资产减值损失/营业总收入(TTM,只有最新数据) -> getImpairToGrTtM


# 获取资产减值损失(TTM,只有最新数据)时间序列 -> getImpairmentTtMSeries


# 获取资产减值损失(TTM,只有最新数据) -> getImpairmentTtM


# 获取其他资产减值损失时间序列 -> getOtherAssetsImpairLossSeries


# 获取其他资产减值损失 -> getOtherAssetsImpairLoss


# 获取固定资产减值损失时间序列 -> getStmNoteImpairmentLoss10Series


# 获取固定资产减值损失 -> getStmNoteImpairmentLoss10


# 获取单季度.资产减值损失/营业利润时间序列 -> getImpairToOpQfaSeries


# 获取单季度.资产减值损失/营业利润 -> getImpairToOpQfa


# 获取单季度.资产减值损失时间序列 -> getQfaImpairLossAssetsSeries


# 获取单季度.资产减值损失 -> getQfaImpairLossAssets


# 获取单季度.其他资产减值损失时间序列 -> getQfaOtherImpairSeries


# 获取单季度.其他资产减值损失 -> getQfaOtherImpair


# 获取财务费用明细-利息支出时间序列 -> getStmNoteFineXp4Series


# 获取财务费用明细-利息支出 -> getStmNoteFineXp4


# 获取财务费用明细-利息收入时间序列 -> getStmNoteFineXp5Series


# 获取财务费用明细-利息收入 -> getStmNoteFineXp5


# 获取财务费用明细-利息资本化金额时间序列 -> getStmNoteFineXp13Series


# 获取财务费用明细-利息资本化金额 -> getStmNoteFineXp13


# 获取财务费用明细-汇兑损益时间序列 -> getStmNoteFineXp6Series


# 获取财务费用明细-汇兑损益 -> getStmNoteFineXp6


# 获取财务费用明细-手续费时间序列 -> getStmNoteFineXp7Series


# 获取财务费用明细-手续费 -> getStmNoteFineXp7


# 获取财务费用明细-其他时间序列 -> getStmNoteFineXp8Series


# 获取财务费用明细-其他 -> getStmNoteFineXp8


# 获取研发费用同比增长时间序列 -> getFaRdExpYoYSeries


# 获取研发费用同比增长 -> getFaRdExpYoY


# 获取研发费用_GSD时间序列 -> getWgsDRdExpSeries


# 获取研发费用_GSD -> getWgsDRdExp


# 获取研发费用时间序列 -> getStm07IsReItsRdFeeSeries


# 获取研发费用 -> getStm07IsReItsRdFee


# 获取研发费用-工资薪酬时间序列 -> getStmNoteRdSalarySeries


# 获取研发费用-工资薪酬 -> getStmNoteRdSalary


# 获取研发费用-折旧摊销时间序列 -> getStmNoteRdDaSeries


# 获取研发费用-折旧摊销 -> getStmNoteRdDa


# 获取研发费用-租赁费时间序列 -> getStmNoteRdLeaseSeries


# 获取研发费用-租赁费 -> getStmNoteRdLease


# 获取研发费用-直接投入时间序列 -> getStmNoteRdInvSeries


# 获取研发费用-直接投入 -> getStmNoteRdInv


# 获取研发费用-其他时间序列 -> getStmNoteRdOthersSeries


# 获取研发费用-其他 -> getStmNoteRdOthers


# 获取研发费用占营业收入比例时间序列 -> getStmNoteRdExpCostToSalesSeries


# 获取研发费用占营业收入比例 -> getStmNoteRdExpCostToSales


# 获取单季度.研发费用_GSD时间序列 -> getWgsDQfaRdExpSeries


# 获取单季度.研发费用_GSD -> getWgsDQfaRdExp


# 获取单季度.研发费用时间序列 -> getQfaRdExpSeries


# 获取单季度.研发费用 -> getQfaRdExp


# 获取所得税/利润总额时间序列 -> getTaxToEBTSeries


# 获取所得税/利润总额 -> getTaxToEBT


# 获取所得税(TTM)时间序列 -> getTaxTtMSeries


# 获取所得税(TTM) -> getTaxTtM


# 获取所得税(TTM)_GSD时间序列 -> getTaxTtM2Series


# 获取所得税(TTM)_GSD -> getTaxTtM2


# 获取所得税_GSD时间序列 -> getWgsDIncTaxSeries


# 获取所得税_GSD -> getWgsDIncTax


# 获取所得税时间序列 -> getTaxSeries


# 获取所得税 -> getTax


# 获取所得税影响数时间序列 -> getStmNoteEoItems22Series


# 获取所得税影响数 -> getStmNoteEoItems22


# 获取所得税费用合计时间序列 -> getStmNoteIncomeTax6Series


# 获取所得税费用合计 -> getStmNoteIncomeTax6


# 获取所得税费用_FUND时间序列 -> getStmIs78Series


# 获取所得税费用_FUND -> getStmIs78


# 获取所得税(TTM)_PIT时间序列 -> getFaTaxTtMSeries


# 获取所得税(TTM)_PIT -> getFaTaxTtM


# 获取递延所得税资产时间序列 -> getDeferredTaxAssetsSeries


# 获取递延所得税资产 -> getDeferredTaxAssets


# 获取递延所得税负债时间序列 -> getDeferredTaxLiaBSeries


# 获取递延所得税负债 -> getDeferredTaxLiaB


# 获取递延所得税资产减少时间序列 -> getDecrDeferredIncTaxAssetsSeries


# 获取递延所得税资产减少 -> getDecrDeferredIncTaxAssets


# 获取递延所得税负债增加时间序列 -> getInCrDeferredIncTaxLiaBSeries


# 获取递延所得税负债增加 -> getInCrDeferredIncTaxLiaB


# 获取年末所得税率时间序列 -> getStmNoteTaxSeries


# 获取年末所得税率 -> getStmNoteTax


# 获取当期所得税:中国大陆时间序列 -> getStmNoteIncomeTax1Series


# 获取当期所得税:中国大陆 -> getStmNoteIncomeTax1


# 获取当期所得税:中国香港时间序列 -> getStmNoteIncomeTax2Series


# 获取当期所得税:中国香港 -> getStmNoteIncomeTax2


# 获取当期所得税:其他境外时间序列 -> getStmNoteIncomeTax3Series


# 获取当期所得税:其他境外 -> getStmNoteIncomeTax3


# 获取递延所得税时间序列 -> getStmNoteIncomeTax5Series


# 获取递延所得税 -> getStmNoteIncomeTax5


# 获取单季度.所得税_GSD时间序列 -> getWgsDQfaIncTaxSeries


# 获取单季度.所得税_GSD -> getWgsDQfaIncTax


# 获取单季度.所得税时间序列 -> getQfaTaxSeries


# 获取单季度.所得税 -> getQfaTax


# 获取以前年度所得税调整时间序列 -> getStmNoteIncomeTax4Series


# 获取以前年度所得税调整 -> getStmNoteIncomeTax4


# 获取单季度.递延所得税资产减少时间序列 -> getQfaDeferredTaxAssetsDecrSeries


# 获取单季度.递延所得税资产减少 -> getQfaDeferredTaxAssetsDecr


# 获取单季度.递延所得税负债增加时间序列 -> getQfaInCrDeferredIncTaxLiaBSeries


# 获取单季度.递延所得税负债增加 -> getQfaInCrDeferredIncTaxLiaB


# 获取Beta(剔除所得税率)时间序列 -> getRiskBetaUnIncomeTaxRateSeries


# 获取Beta(剔除所得税率) -> getRiskBetaUnIncomeTaxRate


# 获取商誉及无形资产_GSD时间序列 -> getWgsDGwIntangSeries


# 获取商誉及无形资产_GSD -> getWgsDGwIntang


# 获取商誉时间序列 -> getGoodwillSeries


# 获取商誉 -> getGoodwill


# 获取商誉减值损失时间序列 -> getStmNoteImpairmentLoss6Series


# 获取商誉减值损失 -> getStmNoteImpairmentLoss6


# 获取商誉-账面价值时间序列 -> getStmNoteGoodwillDetailSeries


# 获取商誉-账面价值 -> getStmNoteGoodwillDetail


# 获取商誉-减值准备时间序列 -> getStmNoteGoodwillImpairmentSeries


# 获取商誉-减值准备 -> getStmNoteGoodwillImpairment


# 获取应付职工薪酬时间序列 -> getEMplBenPayableSeries


# 获取应付职工薪酬 -> getEMplBenPayable


# 获取应付职工薪酬合计:本期增加时间序列 -> getStmNoteEMplPayableAddSeries


# 获取应付职工薪酬合计:本期增加 -> getStmNoteEMplPayableAdd


# 获取应付职工薪酬合计:期初余额时间序列 -> getStmNoteEMplPayableSbSeries


# 获取应付职工薪酬合计:期初余额 -> getStmNoteEMplPayableSb


# 获取应付职工薪酬合计:期末余额时间序列 -> getStmNoteEMplPayableEbSeries


# 获取应付职工薪酬合计:期末余额 -> getStmNoteEMplPayableEb


# 获取应付职工薪酬合计:本期减少时间序列 -> getStmNoteEMplPayableDeSeries


# 获取应付职工薪酬合计:本期减少 -> getStmNoteEMplPayableDe


# 获取长期应付职工薪酬时间序列 -> getLtEMplBenPayableSeries


# 获取长期应付职工薪酬 -> getLtEMplBenPayable


# 获取营业税金及附加合计时间序列 -> getStmNoteTaxBusinessSeries


# 获取营业税金及附加合计 -> getStmNoteTaxBusiness


# 获取营业税金及附加(TTM)_PIT时间序列 -> getFaOperTaxTtMSeries


# 获取营业税金及附加(TTM)_PIT -> getFaOperTaxTtM


# 获取其他营业税金及附加时间序列 -> getStmNoteTaxOThSeries


# 获取其他营业税金及附加 -> getStmNoteTaxOTh


# 获取定期报告披露日期时间序列 -> getStmIssuingDateSeries


# 获取定期报告披露日期 -> getStmIssuingDate


# 获取定期报告正报披露日期时间序列 -> getStmIssuingDateFsSeries


# 获取定期报告正报披露日期 -> getStmIssuingDateFs


# 获取定期报告预计披露日期时间序列 -> getStmPredictIssuingDateSeries


# 获取定期报告预计披露日期 -> getStmPredictIssuingDate


# 获取报告起始日期时间序列 -> getStmRpTSSeries


# 获取报告起始日期 -> getStmRpTS


# 获取报告截止日期时间序列 -> getStmRpTESeries


# 获取报告截止日期 -> getStmRpTE


# 获取最新报告期时间序列 -> getLatelyRdBtSeries


# 获取最新报告期 -> getLatelyRdBt


# 获取会计差错更正披露日期时间序列 -> getFaErrorCorrectionDateSeries


# 获取会计差错更正披露日期 -> getFaErrorCorrectionDate


# 获取是否存在会计差错更正时间序列 -> getFaErrorCorrectionOrNotSeries


# 获取是否存在会计差错更正 -> getFaErrorCorrectionOrNot


# 获取会计准则类型时间序列 -> getStmNoteAuditAmSeries


# 获取会计准则类型 -> getStmNoteAuditAm


# 获取业绩说明会时间时间序列 -> getPerformanceTimeSeries


# 获取业绩说明会时间 -> getPerformanceTime


# 获取业绩说明会日期时间序列 -> getPerformanceDateSeries


# 获取业绩说明会日期 -> getPerformanceDate


# 获取环境维度得分时间序列 -> getEsGEScoreWindSeries


# 获取环境维度得分 -> getEsGEScoreWind


# 获取社会维度得分时间序列 -> getEsGSScoreWindSeries


# 获取社会维度得分 -> getEsGSScoreWind


# 获取治理维度得分时间序列 -> getEsGGScoreWindSeries


# 获取治理维度得分 -> getEsGGScoreWind


# 获取发行费用合计时间序列 -> getIssueFeeFeeSumSeries


# 获取发行费用合计 -> getIssueFeeFeeSum


# 获取首发发行费用时间序列 -> getIpoExpense2Series


# 获取首发发行费用 -> getIpoExpense2


# 获取首发发行费用(旧)时间序列 -> getIpoExpenseSeries


# 获取首发发行费用(旧) -> getIpoExpense


# 获取发行结果公告日时间序列 -> getCbListAnnoCeDateSeries


# 获取发行结果公告日 -> getCbListAnnoCeDate


# 获取基金获批注册日期时间序列 -> getFundApprovedDateSeries


# 获取基金获批注册日期 -> getFundApprovedDate


# 获取发行公告日时间序列 -> getIssueAnnouncedAteSeries


# 获取发行公告日 -> getIssueAnnouncedAte


# 获取发行公告日期时间序列 -> getTenderAnceDateSeries


# 获取发行公告日期 -> getTenderAnceDate


# 获取上网发行公告日时间序列 -> getFellowAnnCeDateSeries


# 获取上网发行公告日 -> getFellowAnnCeDate


# 获取发行日期时间序列 -> getIssueDateSeries


# 获取发行日期 -> getIssueDate


# 获取首发发行日期时间序列 -> getIpoIssueDateSeries


# 获取首发发行日期 -> getIpoIssueDate


# 获取定增发行日期时间序列 -> getFellowIssueDatePpSeries


# 获取定增发行日期 -> getFellowIssueDatePp


# 获取网上发行日期时间序列 -> getCbListDToNlSeries


# 获取网上发行日期 -> getCbListDToNl


# 获取网下向机构投资者发行日期时间序列 -> getCbListDateInStOffSeries


# 获取网下向机构投资者发行日期 -> getCbListDateInStOff


# 获取发行方式时间序列 -> getIssueTypeSeries


# 获取发行方式 -> getIssueType


# 获取首发发行方式时间序列 -> getIpoTypeSeries


# 获取首发发行方式 -> getIpoType


# 获取增发发行方式时间序列 -> getFellowIssueTypeSeries


# 获取增发发行方式 -> getFellowIssueType


# 获取发行对象时间序列 -> getIssueObjectSeries


# 获取发行对象 -> getIssueObject


# 获取增发发行对象时间序列 -> getFellowShareholdersSeries


# 获取增发发行对象 -> getFellowShareholders


# 获取发行份额时间序列 -> getIssueUnitSeries


# 获取发行份额 -> getIssueUnit


# 获取发行总份额时间序列 -> getIssueTotalUnitSeries


# 获取发行总份额 -> getIssueTotalUnit


# 获取发行规模时间序列 -> getFundReItsIssueSizeSeries


# 获取发行规模 -> getFundReItsIssueSize


# 获取实际发行规模时间序列 -> getFundActualScaleSeries


# 获取实际发行规模 -> getFundActualScale


# 获取发行总规模时间序列 -> getIssueTotalSizeSeries


# 获取发行总规模 -> getIssueTotalSize


# 获取基金发起人时间序列 -> getIssueInitiatorSeries


# 获取基金发起人 -> getIssueInitiator


# 获取基金主承销商时间序列 -> getIssueLeadUnderwriterSeries


# 获取基金主承销商 -> getIssueLeadUnderwriter


# 获取基金销售代理人时间序列 -> getIssueDeputySeries


# 获取基金销售代理人 -> getIssueDeputy


# 获取基金上市推荐人时间序列 -> getIssueNominatorSeries


# 获取基金上市推荐人 -> getIssueNominator


# 获取发行封闭期时间序列 -> getIssueOeClsPeriodSeries


# 获取发行封闭期 -> getIssueOeClsPeriod


# 获取成立条件-净认购份额时间序列 -> getIssueOeCNdNetPurchaseSeries


# 获取成立条件-净认购份额 -> getIssueOeCNdNetPurchase


# 获取成立条件-认购户数时间序列 -> getIssueOeCNdPurchasersSeries


# 获取成立条件-认购户数 -> getIssueOeCNdPurchasers


# 获取募集份额上限时间序列 -> getIssueOEfMaxCollectionSeries


# 获取募集份额上限 -> getIssueOEfMaxCollection


# 获取认购份额确认比例时间序列 -> getIssueOEfConfirmRatioSeries


# 获取认购份额确认比例 -> getIssueOEfConfirmRatio


# 获取开放式基金认购户数时间序列 -> getIssueOEfNumPurchasersSeries


# 获取开放式基金认购户数 -> getIssueOEfNumPurchasers


# 获取上市交易份额时间序列 -> getIssueEtFDealShareOnMarketSeries


# 获取上市交易份额 -> getIssueEtFDealShareOnMarket


# 获取网上现金发售代码时间序列 -> getIssueOnlineCashOfferingSymbolSeries


# 获取网上现金发售代码 -> getIssueOnlineCashOfferingSymbol


# 获取一级市场基金代码时间序列 -> getIssueFirstMarketFundCodeSeries


# 获取一级市场基金代码 -> getIssueFirstMarketFundCode


# 获取个人投资者认购方式时间序列 -> getIssueOEfMThDInDSeries


# 获取个人投资者认购方式 -> getIssueOEfMThDInD


# 获取个人投资者认购金额下限时间序列 -> getIssueOEfMinamTinDSeries


# 获取个人投资者认购金额下限 -> getIssueOEfMinamTinD


# 获取个人投资者认购金额上限时间序列 -> getIssueOEfMaxAmtInDSeries


# 获取个人投资者认购金额上限 -> getIssueOEfMaxAmtInD


# 获取个人投资者认购起始日时间序列 -> getIssueOEfStartDateInDSeries


# 获取个人投资者认购起始日 -> getIssueOEfStartDateInD


# 获取个人投资者认购终止日时间序列 -> getIssueOEfEnddateInDSeries


# 获取个人投资者认购终止日 -> getIssueOEfEnddateInD


# 获取封闭期机构投资者认购方式时间序列 -> getIssueOEfMThDInStSeries


# 获取封闭期机构投资者认购方式 -> getIssueOEfMThDInSt


# 获取机构投资者设立认购起始日时间序列 -> getIssueOEfStartDateInStSeries


# 获取机构投资者设立认购起始日 -> getIssueOEfStartDateInSt


# 获取机构投资者设立认购终止日时间序列 -> getIssueOEfDndDateInStSeries


# 获取机构投资者设立认购终止日 -> getIssueOEfDndDateInSt


# 获取封闭期机构投资者认购下限时间序列 -> getIssueOEfMinamTinStSeries


# 获取封闭期机构投资者认购下限 -> getIssueOEfMinamTinSt


# 获取封闭期机构投资者认购上限时间序列 -> getIssueOEfMaxAmtInStSeries


# 获取封闭期机构投资者认购上限 -> getIssueOEfMaxAmtInSt


# 获取封闭式基金认购数量时间序列 -> getIssueCefInIPurchaseSeries


# 获取封闭式基金认购数量 -> getIssueCefInIPurchase


# 获取封闭式基金超额认购倍数时间序列 -> getIssueCefOverSubSeries


# 获取封闭式基金超额认购倍数 -> getIssueCefOverSub


# 获取封闭式基金中签率时间序列 -> getIssueCefSuccRatioSeries


# 获取封闭式基金中签率 -> getIssueCefSuccRatio


# 获取是否提前开始募集时间序列 -> getIssueRaSingIsStartEarlySeries


# 获取是否提前开始募集 -> getIssueRaSingIsStartEarly


# 获取是否延期募集时间序列 -> getIssueRaSingIsStartDeferredSeries


# 获取是否延期募集 -> getIssueRaSingIsStartDeferred


# 获取是否提前结束募集时间序列 -> getIssueRaSingIsEndEarlySeries


# 获取是否提前结束募集 -> getIssueRaSingIsEndEarly


# 获取是否延长募集期时间序列 -> getIssueRaSingIsEndDeferredSeries


# 获取是否延长募集期 -> getIssueRaSingIsEndDeferred


# 获取认购天数时间序列 -> getIssueOEfDaysSeries


# 获取认购天数 -> getIssueOEfDays


# 获取单位年度分红时间序列 -> getDivPerUnitSeries


# 获取单位年度分红 -> getDivPerUnit


# 获取单位累计分红时间序列 -> getDivAccumulatedPerUnitSeries


# 获取单位累计分红 -> getDivAccumulatedPerUnit


# 获取年度分红总额时间序列 -> getDivPayOutSeries


# 获取年度分红总额 -> getDivPayOut


# 获取年度分红次数时间序列 -> getDivTimesSeries


# 获取年度分红次数 -> getDivTimes


# 获取累计分红总额时间序列 -> getDivAccumulatedPayOutSeries


# 获取累计分红总额 -> getDivAccumulatedPayOut


# 获取年度累计分红总额时间序列 -> getDivAuALaCcmDiv3Series


# 获取年度累计分红总额 -> getDivAuALaCcmDiv3


# 获取年度累计分红总额(已宣告)时间序列 -> getDivAuALaCcmDivArdSeries


# 获取年度累计分红总额(已宣告) -> getDivAuALaCcmDivArd


# 获取年度累计分红总额(沪深)时间序列 -> getDivAuALaCcmDivSeries


# 获取年度累计分红总额(沪深) -> getDivAuALaCcmDiv


# 获取累计分红次数时间序列 -> getDivAccumulatedTimesSeries


# 获取累计分红次数 -> getDivAccumulatedTimes


# 获取区间单位分红时间序列 -> getDivPeriodPerUnitSeries


# 获取区间单位分红 -> getDivPeriodPerUnit


# 获取区间分红总额时间序列 -> getDivPeriodPayOutSeries


# 获取区间分红总额 -> getDivPeriodPayOut


# 获取区间分红次数时间序列 -> getDivPeriodTimesSeries


# 获取区间分红次数 -> getDivPeriodTimes


# 获取分红条款时间序列 -> getDivClauseSeries


# 获取分红条款 -> getDivClause


# 获取区间诉讼次数时间序列 -> getCacLawsuitNumSeries


# 获取区间诉讼次数 -> getCacLawsuitNum


# 获取区间诉讼涉案金额时间序列 -> getCacLawsuitAmountSeries


# 获取区间诉讼涉案金额 -> getCacLawsuitAmount


# 获取区间违规处罚次数时间序列 -> getCacIllegalityNumSeries


# 获取区间违规处罚次数 -> getCacIllegalityNum


# 获取区间违规处罚金额时间序列 -> getCacIllegalityAmountSeries


# 获取区间违规处罚金额 -> getCacIllegalityAmount


# 获取未上市流通基金份数(封闭式)时间序列 -> getUnitNonTradableSeries


# 获取未上市流通基金份数(封闭式) -> getUnitNonTradable


# 获取已上市流通基金份数(封闭式)时间序列 -> getUnitTradableSeries


# 获取已上市流通基金份数(封闭式) -> getUnitTradable


# 获取基金资产总值时间序列 -> getPrtTotalAssetSeries


# 获取基金资产总值 -> getPrtTotalAsset


# 获取基金资产总值变动时间序列 -> getPrtTotalAssetChangeSeries


# 获取基金资产总值变动 -> getPrtTotalAssetChange


# 获取基金资产总值变动率时间序列 -> getPrtTotalAssetChangeRatioSeries


# 获取基金资产总值变动率 -> getPrtTotalAssetChangeRatio


# 获取基金净值占基金资产总值比时间序列 -> getPrtNavToAssetSeries


# 获取基金净值占基金资产总值比 -> getPrtNavToAsset


# 获取股票市值占基金资产总值比时间序列 -> getPrtStockToAssetSeries


# 获取股票市值占基金资产总值比 -> getPrtStockToAsset


# 获取债券市值占基金资产总值比时间序列 -> getPrtBondToAssetSeries


# 获取债券市值占基金资产总值比 -> getPrtBondToAsset


# 获取基金市值占基金资产总值比时间序列 -> getPrtFundToAssetSeries


# 获取基金市值占基金资产总值比 -> getPrtFundToAsset


# 获取权证市值占基金资产总值比时间序列 -> getPrtWarrantToAssetSeries


# 获取权证市值占基金资产总值比 -> getPrtWarrantToAsset


# 获取其他资产占基金资产总值比时间序列 -> getPrtOtherToAssetSeries


# 获取其他资产占基金资产总值比 -> getPrtOtherToAsset


# 获取国债市值占基金资产总值比时间序列 -> getPrtGovernmentBondToAssetSeries


# 获取国债市值占基金资产总值比 -> getPrtGovernmentBondToAsset


# 获取金融债市值占基金资产总值比时间序列 -> getPrtFinancialBondToAssetSeries


# 获取金融债市值占基金资产总值比 -> getPrtFinancialBondToAsset


# 获取企业债市值占基金资产总值比时间序列 -> getPrtCorporateBondsToAssetSeries


# 获取企业债市值占基金资产总值比 -> getPrtCorporateBondsToAsset


# 获取可转债市值占基金资产总值比时间序列 -> getPrtConvertibleBondToAssetSeries


# 获取可转债市值占基金资产总值比 -> getPrtConvertibleBondToAsset


# 获取分行业市值占基金资产总值比时间序列 -> getPrtStockValueIndustryToAsset2Series


# 获取分行业市值占基金资产总值比 -> getPrtStockValueIndustryToAsset2


# 获取重仓股市值占基金资产总值比时间序列 -> getPrtHeavilyHeldStockToAssetSeries


# 获取重仓股市值占基金资产总值比 -> getPrtHeavilyHeldStockToAsset


# 获取港股投资市值占基金资产总值比时间序列 -> getPrtHkStockToAssetSeries


# 获取港股投资市值占基金资产总值比 -> getPrtHkStockToAsset


# 获取买入返售证券占基金资产总值比例时间序列 -> getMmFReverseRepoToAssetSeries


# 获取买入返售证券占基金资产总值比例 -> getMmFReverseRepoToAsset


# 获取央行票据市值占基金资产总值比时间序列 -> getPrtCentralBankBillToAssetSeries


# 获取央行票据市值占基金资产总值比 -> getPrtCentralBankBillToAsset


# 获取重仓行业市值占基金资产总值比时间序列 -> getPrtStockValueTopIndustryToAsset2Series


# 获取重仓行业市值占基金资产总值比 -> getPrtStockValueTopIndustryToAsset2


# 获取重仓债券市值占基金资产总值比时间序列 -> getPrtHeavilyHeldBondToAssetSeries


# 获取重仓债券市值占基金资产总值比 -> getPrtHeavilyHeldBondToAsset


# 获取重仓基金市值占基金资产总值比时间序列 -> getPrtHeavilyHeldFundToAssetSeries


# 获取重仓基金市值占基金资产总值比 -> getPrtHeavilyHeldFundToAsset


# 获取政策性金融债市值占基金资产总值比时间序列 -> getPrtPFbToAssetSeries


# 获取政策性金融债市值占基金资产总值比 -> getPrtPFbToAsset


# 获取企业发行债券市值占基金资产总值比时间序列 -> getPrtCorporateBondToAssetSeries


# 获取企业发行债券市值占基金资产总值比 -> getPrtCorporateBondToAsset


# 获取重仓资产支持证券市值占基金资产总值比时间序列 -> getPrtHeavilyHeldAbsToAssetSeries


# 获取重仓资产支持证券市值占基金资产总值比 -> getPrtHeavilyHeldAbsToAsset


# 获取转融通证券出借业务市值占基金资产总值比时间序列 -> getPrtSecLendingValueToAssetSeries


# 获取转融通证券出借业务市值占基金资产总值比 -> getPrtSecLendingValueToAsset


# 获取基金资产净值时间序列 -> getPrtNetAssetSeries


# 获取基金资产净值 -> getPrtNetAsset


# 获取基金资产净值变动时间序列 -> getPrtNetAssetChangeSeries


# 获取基金资产净值变动 -> getPrtNetAssetChange


# 获取基金资产净值变动率时间序列 -> getPrtNetAssetChangeRatioSeries


# 获取基金资产净值变动率 -> getPrtNetAssetChangeRatio


# 获取报告期基金资产净值币种时间序列 -> getPrtCurrencySeries


# 获取报告期基金资产净值币种 -> getPrtCurrency


# 获取股票市值占基金资产净值比时间序列 -> getPrtStocktonAvSeries


# 获取股票市值占基金资产净值比 -> getPrtStocktonAv


# 获取债券市值占基金资产净值比时间序列 -> getPrtBondToNavSeries


# 获取债券市值占基金资产净值比 -> getPrtBondToNav


# 获取基金市值占基金资产净值比时间序列 -> getPrtFundToNavSeries


# 获取基金市值占基金资产净值比 -> getPrtFundToNav


# 获取权证市值占基金资产净值比时间序列 -> getPrtWarrantToNavSeries


# 获取权证市值占基金资产净值比 -> getPrtWarrantToNav


# 获取其他资产占基金资产净值比时间序列 -> getPrtOtherToNavSeries


# 获取其他资产占基金资产净值比 -> getPrtOtherToNav


# 获取股票市值占基金资产净值比例增长时间序列 -> getPrtStocktonAvGrowthSeries


# 获取股票市值占基金资产净值比例增长 -> getPrtStocktonAvGrowth


# 获取债券市值占基金资产净值比例增长时间序列 -> getPrtBondToNavGrowthSeries


# 获取债券市值占基金资产净值比例增长 -> getPrtBondToNavGrowth


# 获取基金市值占基金资产净值比例增长时间序列 -> getPrtFundToNavGrowthSeries


# 获取基金市值占基金资产净值比例增长 -> getPrtFundToNavGrowth


# 获取权证市值占基金资产净值比例增长时间序列 -> getPrtWarrantToNavGrowthSeries


# 获取权证市值占基金资产净值比例增长 -> getPrtWarrantToNavGrowth


# 获取国债市值占基金资产净值比时间序列 -> getPrtGovernmentBondToNavSeries


# 获取国债市值占基金资产净值比 -> getPrtGovernmentBondToNav


# 获取国债市值占基金资产净值比例增长时间序列 -> getPrtGovernmentBondToNavGrowthSeries


# 获取国债市值占基金资产净值比例增长 -> getPrtGovernmentBondToNavGrowth


# 获取金融债市值占基金资产净值比时间序列 -> getPrtFinancialBondToNavSeries


# 获取金融债市值占基金资产净值比 -> getPrtFinancialBondToNav


# 获取企业债市值占基金资产净值比时间序列 -> getPrtCorporateBondsToNavSeries


# 获取企业债市值占基金资产净值比 -> getPrtCorporateBondsToNav


# 获取可转债市值占基金资产净值比时间序列 -> getPrtConvertibleBondToNavSeries


# 获取可转债市值占基金资产净值比 -> getPrtConvertibleBondToNav


# 获取金融债市值占基金资产净值比例增长时间序列 -> getPrtFinancialBondToNavGrowthSeries


# 获取金融债市值占基金资产净值比例增长 -> getPrtFinancialBondToNavGrowth


# 获取企业债市值占基金资产净值比例增长时间序列 -> getPrtCorporateBondsToNavGrowthSeries


# 获取企业债市值占基金资产净值比例增长 -> getPrtCorporateBondsToNavGrowth


# 获取可转债市值占基金资产净值比例增长时间序列 -> getPrtConvertibleBondToNavGrowthSeries


# 获取可转债市值占基金资产净值比例增长 -> getPrtConvertibleBondToNavGrowth


# 获取分行业市值占基金资产净值比时间序列 -> getPrtStockValueIndustryToNav2Series


# 获取分行业市值占基金资产净值比 -> getPrtStockValueIndustryToNav2


# 获取分行业市值占基金资产净值比增长时间序列 -> getPrtStockValueIndustryToNavGrowth2Series


# 获取分行业市值占基金资产净值比增长 -> getPrtStockValueIndustryToNavGrowth2


# 获取分行业市值占基金资产净值比增长(Wind)时间序列 -> getPrtIndustryToNavGrowthWindSeries


# 获取分行业市值占基金资产净值比增长(Wind) -> getPrtIndustryToNavGrowthWind


# 获取分行业市值占基金资产净值比增长(中信)时间序列 -> getPrtIndustryToNavGrowthCitiCSeries


# 获取分行业市值占基金资产净值比增长(中信) -> getPrtIndustryToNavGrowthCitiC


# 获取分行业市值占基金资产净值比增长(申万)时间序列 -> getPrtIndustryToNavGrowthSwSeries


# 获取分行业市值占基金资产净值比增长(申万) -> getPrtIndustryToNavGrowthSw


# 获取重仓股市值占基金资产净值比时间序列 -> getPrtHeavilyHeldStocktonAvSeries


# 获取重仓股市值占基金资产净值比 -> getPrtHeavilyHeldStocktonAv


# 获取各期限资产占基金资产净值比例时间序列 -> getMmFDifferentPtMToNavSeries


# 获取各期限资产占基金资产净值比例 -> getMmFDifferentPtMToNav


# 获取港股投资市值占基金资产净值比时间序列 -> getPrtHkStocktonAvSeries


# 获取港股投资市值占基金资产净值比 -> getPrtHkStocktonAv


# 获取买入返售证券占基金资产净值比例时间序列 -> getPrtReverseRepoToNavSeries


# 获取买入返售证券占基金资产净值比例 -> getPrtReverseRepoToNav


# 获取其他资产市值占基金资产净值比例增长时间序列 -> getPrtOtherToNavGrowthSeries


# 获取其他资产市值占基金资产净值比例增长 -> getPrtOtherToNavGrowth


# 获取同业存单市值占基金资产净值比时间序列 -> getPrtCdsToNavSeries


# 获取同业存单市值占基金资产净值比 -> getPrtCdsToNav


# 获取央行票据市值占基金资产净值比时间序列 -> getPrtCentralBankBillToNavSeries


# 获取央行票据市值占基金资产净值比 -> getPrtCentralBankBillToNav


# 获取中期票据市值占基金资产净值比时间序列 -> getPrtMtnToNavSeries


# 获取中期票据市值占基金资产净值比 -> getPrtMtnToNav


# 获取其他债券市值占基金资产净值比时间序列 -> getPrtOtherBondToNavSeries


# 获取其他债券市值占基金资产净值比 -> getPrtOtherBondToNav


# 获取央行票据市值占基金资产净值比例增长时间序列 -> getPrtCentralBankBillToNavGrowthSeries


# 获取央行票据市值占基金资产净值比例增长 -> getPrtCentralBankBillToNavGrowth


# 获取重仓行业市值占基金资产净值比时间序列 -> getPrtStockValueTopIndustryToNav2Series


# 获取重仓行业市值占基金资产净值比 -> getPrtStockValueTopIndustryToNav2


# 获取重仓债券市值占基金资产净值比时间序列 -> getPrtHeavilyHeldBondToNavSeries


# 获取重仓债券市值占基金资产净值比 -> getPrtHeavilyHeldBondToNav


# 获取重仓基金市值占基金资产净值比时间序列 -> getPrtHeavilyHeldFundToNavSeries


# 获取重仓基金市值占基金资产净值比 -> getPrtHeavilyHeldFundToNav


# 获取短期融资券市值占基金资产净值比时间序列 -> getPrtCpToNavSeries


# 获取短期融资券市值占基金资产净值比 -> getPrtCpToNav


# 获取分行业投资市值占基金资产净值比例(Wind全球行业)时间序列 -> getPrtGicSIndustryValueToNavSeries


# 获取分行业投资市值占基金资产净值比例(Wind全球行业) -> getPrtGicSIndustryValueToNav


# 获取分行业投资市值占基金资产净值比(Wind)时间序列 -> getPrtIndustryValueToNavWindSeries


# 获取分行业投资市值占基金资产净值比(Wind) -> getPrtIndustryValueToNavWind


# 获取分行业投资市值占基金资产净值比(中信)时间序列 -> getPrtIndustryValueToNavCitiCSeries


# 获取分行业投资市值占基金资产净值比(中信) -> getPrtIndustryValueToNavCitiC


# 获取分行业投资市值占基金资产净值比(申万)时间序列 -> getPrtIndustryValueToNavSwSeries


# 获取分行业投资市值占基金资产净值比(申万) -> getPrtIndustryValueToNavSw


# 获取单季度.报告期期末基金资产净值时间序列 -> getQAnalNetAssetSeries


# 获取单季度.报告期期末基金资产净值 -> getQAnalNetAsset


# 获取指数投资股票市值占基金资产净值比时间序列 -> getPrtStocktonAvPassiveInvestSeries


# 获取指数投资股票市值占基金资产净值比 -> getPrtStocktonAvPassiveInvest


# 获取积极投资股票市值占基金资产净值比时间序列 -> getPrtStocktonAvActiveInvestSeries


# 获取积极投资股票市值占基金资产净值比 -> getPrtStocktonAvActiveInvest


# 获取政策性金融债市值占基金资产净值比时间序列 -> getPrtPFbToNavSeries


# 获取政策性金融债市值占基金资产净值比 -> getPrtPFbToNav


# 获取企业发行债券市值占基金资产净值比时间序列 -> getPrtCorporateBondToNavSeries


# 获取企业发行债券市值占基金资产净值比 -> getPrtCorporateBondToNav


# 获取资产支持证券市值占基金资产净值比时间序列 -> getPrtAbsToNavSeries


# 获取资产支持证券市值占基金资产净值比 -> getPrtAbsToNav


# 获取货币市场工具市值占基金资产净值比时间序列 -> getPrtMMitoNavSeries


# 获取货币市场工具市值占基金资产净值比 -> getPrtMMitoNav


# 获取企业发行债券市值占基金资产净值比例增长时间序列 -> getPrtCorporateBondToNavGrowthSeries


# 获取企业发行债券市值占基金资产净值比例增长 -> getPrtCorporateBondToNavGrowth


# 获取重仓行业投资市值占基金资产净值比例(Wind全球行业)时间序列 -> getPrtTopGicSIndustryValueToNavSeries


# 获取重仓行业投资市值占基金资产净值比例(Wind全球行业) -> getPrtTopGicSIndustryValueToNav


# 获取重仓行业投资市值占基金资产净值比(Wind)时间序列 -> getPrtTopIndustryValueToNavWindSeries


# 获取重仓行业投资市值占基金资产净值比(Wind) -> getPrtTopIndustryValueToNavWind


# 获取重仓行业投资市值占基金资产净值比(中信)时间序列 -> getPrtTopIndustryValueToNavCitiCSeries


# 获取重仓行业投资市值占基金资产净值比(中信) -> getPrtTopIndustryValueToNavCitiC


# 获取重仓行业投资市值占基金资产净值比(申万)时间序列 -> getPrtTopIndustryValueToNavSwSeries


# 获取重仓行业投资市值占基金资产净值比(申万) -> getPrtTopIndustryValueToNavSw


# 获取国家/地区投资市值占基金资产净值比例(QDII)时间序列 -> getPrtQdIiCountryRegionInvestmentToNavSeries


# 获取国家/地区投资市值占基金资产净值比例(QDII) -> getPrtQdIiCountryRegionInvestmentToNav


# 获取重仓资产支持证券市值占基金资产净值比时间序列 -> getPrtHeavilyHeldAbsToNavSeries


# 获取重仓资产支持证券市值占基金资产净值比 -> getPrtHeavilyHeldAbsToNav


# 获取转融通证券出借业务市值占基金资产净值比时间序列 -> getPrtSecLendingValueToNavSeries


# 获取转融通证券出借业务市值占基金资产净值比 -> getPrtSecLendingValueToNav


# 获取前N名重仓股票市值合计占基金资产净值比时间序列 -> getPrtTopNStocktonAvSeries


# 获取前N名重仓股票市值合计占基金资产净值比 -> getPrtTopNStocktonAv


# 获取前N名重仓债券市值合计占基金资产净值比时间序列 -> getPrtTop5ToNavSeries


# 获取前N名重仓债券市值合计占基金资产净值比 -> getPrtTop5ToNav


# 获取前N名重仓基金市值合计占基金资产净值比时间序列 -> getPrtTopNFundToNavSeries


# 获取前N名重仓基金市值合计占基金资产净值比 -> getPrtTopNFundToNav


# 获取报告期基金日均资产净值时间序列 -> getPrtAvgNetAssetSeries


# 获取报告期基金日均资产净值 -> getPrtAvgNetAsset


# 获取资产净值(合计)时间序列 -> getPrtFundNetAssetTotalSeries


# 获取资产净值(合计) -> getPrtFundNetAssetTotal


# 获取资产净值是否为合并数据(最新)时间序列 -> getPrtMergedNavOrNotSeries


# 获取资产净值是否为合并数据(最新) -> getPrtMergedNavOrNot


# 获取资产净值是否为合并数据(报告期)时间序列 -> getPrtMergedNavOrNot1Series


# 获取资产净值是否为合并数据(报告期) -> getPrtMergedNavOrNot1


# 获取同类基金平均规模时间序列 -> getFundAvgFundScaleSeries


# 获取同类基金平均规模 -> getFundAvgFundScale


# 获取市场展望时间序列 -> getFundMarketOutlookSeries


# 获取市场展望 -> getFundMarketOutlook


# 获取市场分析时间序列 -> getFundMarketAnalysisSeries


# 获取市场分析 -> getFundMarketAnalysis


# 获取股票投资市值时间序列 -> getPrtStockValueSeries


# 获取股票投资市值 -> getPrtStockValue


# 获取分行业市值占股票投资市值比时间序列 -> getPrtStockValueIndustryTostock2Series


# 获取分行业市值占股票投资市值比 -> getPrtStockValueIndustryTostock2


# 获取重仓股市值占股票投资市值比时间序列 -> getPrtHeavilyHeldStockTostockSeries


# 获取重仓股市值占股票投资市值比 -> getPrtHeavilyHeldStockTostock


# 获取重仓行业市值占股票投资市值比时间序列 -> getPrtStockValueTopIndustryTostock2Series


# 获取重仓行业市值占股票投资市值比 -> getPrtStockValueTopIndustryTostock2


# 获取前N名重仓股票市值合计占股票投资市值比时间序列 -> getPrtTopNStockTostockSeries


# 获取前N名重仓股票市值合计占股票投资市值比 -> getPrtTopNStockTostock


# 获取指数投资股票市值时间序列 -> getPrtStockValuePassiveInvestSeries


# 获取指数投资股票市值 -> getPrtStockValuePassiveInvest


# 获取积极投资股票市值时间序列 -> getPrtStockValueActiveInvestSeries


# 获取积极投资股票市值 -> getPrtStockValueActiveInvest


# 获取港股投资市值时间序列 -> getPrtHkStockValueSeries


# 获取港股投资市值 -> getPrtHkStockValue


# 获取债券投资市值时间序列 -> getPrtBondValueSeries


# 获取债券投资市值 -> getPrtBondValue


# 获取国债市值占债券投资市值比时间序列 -> getPrtGovernmentBondToBondSeries


# 获取国债市值占债券投资市值比 -> getPrtGovernmentBondToBond


# 获取金融债市值占债券投资市值比时间序列 -> getPrtFinancialBondToBondSeries


# 获取金融债市值占债券投资市值比 -> getPrtFinancialBondToBond


# 获取企业债市值占债券投资市值比时间序列 -> getPrtCorporateBondsToBondSeries


# 获取企业债市值占债券投资市值比 -> getPrtCorporateBondsToBond


# 获取可转债市值占债券投资市值比时间序列 -> getPrtConvertibleBondToBondSeries


# 获取可转债市值占债券投资市值比 -> getPrtConvertibleBondToBond


# 获取央行票据市值占债券投资市值比时间序列 -> getPrtCentralBankBillToBondSeries


# 获取央行票据市值占债券投资市值比 -> getPrtCentralBankBillToBond


# 获取政策性金融债占债券投资市值比时间序列 -> getPrtPFbToBondSeries


# 获取政策性金融债占债券投资市值比 -> getPrtPFbToBond


# 获取同业存单市值占债券投资市值比时间序列 -> getPrtNcdToBondSeries


# 获取同业存单市值占债券投资市值比 -> getPrtNcdToBond


# 获取重仓债券市值占债券投资市值比时间序列 -> getPrtHeavilyHeldBondToBondSeries


# 获取重仓债券市值占债券投资市值比 -> getPrtHeavilyHeldBondToBond


# 获取企业发行债券市值占债券投资市值比时间序列 -> getPrtCorporateBondToBondSeries


# 获取企业发行债券市值占债券投资市值比 -> getPrtCorporateBondToBond


# 获取前N名重仓债券市值合计占债券投资市值比时间序列 -> getPrtTop5ToBondSeries


# 获取前N名重仓债券市值合计占债券投资市值比 -> getPrtTop5ToBond


# 获取基金投资市值时间序列 -> getPrtFundValueSeries


# 获取基金投资市值 -> getPrtFundValue


# 获取重仓基金市值占基金投资市值比时间序列 -> getPrtHeavilyHeldFundToFundSeries


# 获取重仓基金市值占基金投资市值比 -> getPrtHeavilyHeldFundToFund


# 获取前N名重仓基金市值合计占基金投资市值比时间序列 -> getPrtTopFundToFundSeries


# 获取前N名重仓基金市值合计占基金投资市值比 -> getPrtTopFundToFund


# 获取股指期货投资市值时间序列 -> getPrtSiFuturesSeries


# 获取股指期货投资市值 -> getPrtSiFutures


# 获取国债期货投资市值时间序列 -> getPrtGbFuturesSeries


# 获取国债期货投资市值 -> getPrtGbFutures


# 获取权证投资市值时间序列 -> getPrtWarrantValueSeries


# 获取权证投资市值 -> getPrtWarrantValue


# 获取转融通证券出借业务市值时间序列 -> getPrtSecLendingValueSeries


# 获取转融通证券出借业务市值 -> getPrtSecLendingValue


# 获取其他资产_GSD时间序列 -> getWgsDAssetsOThSeries


# 获取其他资产_GSD -> getWgsDAssetsOTh


# 获取其他资产时间序列 -> getPrtOtherSeries


# 获取其他资产 -> getPrtOther


# 获取其他资产_FUND时间序列 -> getStmBs18Series


# 获取其他资产_FUND -> getStmBs18


# 获取其他资产市值增长率时间序列 -> getPrtOtherValueGrowthSeries


# 获取其他资产市值增长率 -> getPrtOtherValueGrowth


# 获取股票市值增长率时间序列 -> getPrtStockValueGrowthSeries


# 获取股票市值增长率 -> getPrtStockValueGrowth


# 获取债券市值增长率时间序列 -> getPrtBondValueGrowthSeries


# 获取债券市值增长率 -> getPrtBondValueGrowth


# 获取企业发行债券市值增长率时间序列 -> getPrtCorporateBondGrowthSeries


# 获取企业发行债券市值增长率 -> getPrtCorporateBondGrowth


# 获取基金市值增长率时间序列 -> getPrtFundValueGrowthSeries


# 获取基金市值增长率 -> getPrtFundValueGrowth


# 获取权证市值增长率时间序列 -> getPrtWarrantValueGrowthSeries


# 获取权证市值增长率 -> getPrtWarrantValueGrowth


# 获取基金杠杆率时间序列 -> getPrtFoundLeverageSeries


# 获取基金杠杆率 -> getPrtFoundLeverage


# 获取国债市值时间序列 -> getPrtGovernmentBondSeries


# 获取国债市值 -> getPrtGovernmentBond


# 获取国债市值增长率时间序列 -> getPrtGovernmentBondGrowthSeries


# 获取国债市值增长率 -> getPrtGovernmentBondGrowth


# 获取同业存单市值时间序列 -> getPrtCdsSeries


# 获取同业存单市值 -> getPrtCds


# 获取央行票据市值时间序列 -> getPrtCentralBankBillSeries


# 获取央行票据市值 -> getPrtCentralBankBill


# 获取央行票据市值增长率时间序列 -> getPrtCentralBankBillGrowthSeries


# 获取央行票据市值增长率 -> getPrtCentralBankBillGrowth


# 获取金融债市值时间序列 -> getPrtFinancialBondSeries


# 获取金融债市值 -> getPrtFinancialBond


# 获取金融债市值增长率时间序列 -> getPrtFinancialBondGrowthSeries


# 获取金融债市值增长率 -> getPrtFinancialBondGrowth


# 获取政策性金融债市值时间序列 -> getPrtPFbValueSeries


# 获取政策性金融债市值 -> getPrtPFbValue


# 获取企业发行债券市值时间序列 -> getPrtCorporateBondSeries


# 获取企业发行债券市值 -> getPrtCorporateBond


# 获取企业债市值时间序列 -> getPrtCorporateBondsSeries


# 获取企业债市值 -> getPrtCorporateBonds


# 获取企业债市值增长率时间序列 -> getPrtCorporateBondsGrowthSeries


# 获取企业债市值增长率 -> getPrtCorporateBondsGrowth


# 获取短期融资券市值时间序列 -> getPrtCpValueSeries


# 获取短期融资券市值 -> getPrtCpValue


# 获取中期票据市值时间序列 -> getPrtMtnValueSeries


# 获取中期票据市值 -> getPrtMtnValue


# 获取可转债市值时间序列 -> getPrtConvertibleBondSeries


# 获取可转债市值 -> getPrtConvertibleBond


# 获取可转债市值增长率时间序列 -> getPrtConvertibleBondGrowthSeries


# 获取可转债市值增长率 -> getPrtConvertibleBondGrowth


# 获取资产支持证券市值时间序列 -> getPrtAbsValueSeries


# 获取资产支持证券市值 -> getPrtAbsValue


# 获取货币市场工具市值时间序列 -> getPrtMmIValueSeries


# 获取货币市场工具市值 -> getPrtMmIValue


# 获取其他债券市值时间序列 -> getPrtOtherBondSeries


# 获取其他债券市值 -> getPrtOtherBond


# 获取分行业投资市值时间序列 -> getPrtStockValueIndustry2Series


# 获取分行业投资市值 -> getPrtStockValueIndustry2


# 获取分行业投资市值(Wind全球行业)时间序列 -> getPrtGicSIndustryValueSeries


# 获取分行业投资市值(Wind全球行业) -> getPrtGicSIndustryValue


# 获取分行业投资市值(Wind)时间序列 -> getPrtIndustryValueWindSeries


# 获取分行业投资市值(Wind) -> getPrtIndustryValueWind


# 获取分行业投资市值(中信)时间序列 -> getPrtIndustryValueCitiCSeries


# 获取分行业投资市值(中信) -> getPrtIndustryValueCitiC


# 获取分行业投资市值(申万)时间序列 -> getPrtIndustryValueSwSeries


# 获取分行业投资市值(申万) -> getPrtIndustryValueSw


# 获取分行业市值增长率时间序列 -> getPrtStockValueIndustryValueGrowth2Series


# 获取分行业市值增长率 -> getPrtStockValueIndustryValueGrowth2


# 获取分行业市值增长率(Wind)时间序列 -> getPrtIndustryValueGrowthWindSeries


# 获取分行业市值增长率(Wind) -> getPrtIndustryValueGrowthWind


# 获取分行业市值增长率(中信)时间序列 -> getPrtIndustryValueGrowthCitiCSeries


# 获取分行业市值增长率(中信) -> getPrtIndustryValueGrowthCitiC


# 获取分行业市值增长率(申万)时间序列 -> getPrtIndustryValueGrowthSwSeries


# 获取分行业市值增长率(申万) -> getPrtIndustryValueGrowthSw


# 获取重仓行业名称时间序列 -> getPrtStockValueTopIndustryName2Series


# 获取重仓行业名称 -> getPrtStockValueTopIndustryName2


# 获取重仓行业名称(Wind全球行业)时间序列 -> getPrtTopGicSIndustryNameSeries


# 获取重仓行业名称(Wind全球行业) -> getPrtTopGicSIndustryName


# 获取重仓行业名称(Wind)时间序列 -> getPrtTopIndustryNameWindSeries


# 获取重仓行业名称(Wind) -> getPrtTopIndustryNameWind


# 获取重仓行业名称(中信)时间序列 -> getPrtTopIndustryNameCitiCSeries


# 获取重仓行业名称(中信) -> getPrtTopIndustryNameCitiC


# 获取重仓行业名称(申万)时间序列 -> getPrtTopIndustryNameSwSeries


# 获取重仓行业名称(申万) -> getPrtTopIndustryNameSw


# 获取重仓行业代码时间序列 -> getPrtStockValueTopIndustrySymbol2Series


# 获取重仓行业代码 -> getPrtStockValueTopIndustrySymbol2


# 获取重仓行业市值时间序列 -> getPrtStockValueTopIndustryValue2Series


# 获取重仓行业市值 -> getPrtStockValueTopIndustryValue2


# 获取报告期末持有股票个数(中报、年报)时间序列 -> getPrtStockHoldingSeries


# 获取报告期末持有股票个数(中报、年报) -> getPrtStockHolding


# 获取报告期不同持仓风格股票只数时间序列 -> getPrtShareNumStKhlDGStyleSeries


# 获取报告期不同持仓风格股票只数 -> getPrtShareNumStKhlDGStyle


# 获取重仓股股票名称时间序列 -> getPrtTopStockNameSeries


# 获取重仓股股票名称 -> getPrtTopStockName


# 获取重仓股股票代码时间序列 -> getPrtTopStockCodeSeries


# 获取重仓股股票代码 -> getPrtTopStockCode


# 获取最早重仓时间时间序列 -> getPrtTopStockDateSeries


# 获取最早重仓时间 -> getPrtTopStockDate


# 获取重仓股持股数量时间序列 -> getPrtTopStockQuantitySeries


# 获取重仓股持股数量 -> getPrtTopStockQuantity


# 获取重仓股持股市值时间序列 -> getPrtTopStockValueSeries


# 获取重仓股持股市值 -> getPrtTopStockValue


# 获取重仓股持仓变动时间序列 -> getPrtTopStockHoldingChangingSeries


# 获取重仓股持仓变动 -> getPrtTopStockHoldingChanging


# 获取重仓股持仓占流通股比例时间序列 -> getPrtTopProportionToFloatingSeries


# 获取重仓股持仓占流通股比例 -> getPrtTopProportionToFloating


# 获取重仓股票持有基金数时间序列 -> getPrtFundNoOfStocksSeries


# 获取重仓股票持有基金数 -> getPrtFundNoOfStocks


# 获取重仓股报告期重仓次数时间序列 -> getPrtTopStockHeldNoSeries


# 获取重仓股报告期重仓次数 -> getPrtTopStockHeldNo


# 获取报告期买入股票总成本时间序列 -> getPrtBuyStockCostSeries


# 获取报告期买入股票总成本 -> getPrtBuyStockCost


# 获取报告期卖出股票总收入时间序列 -> getPrtSellStockIncomeSeries


# 获取报告期卖出股票总收入 -> getPrtSellStockIncome


# 获取股票成交金额(分券商明细)时间序列 -> getPrtStockVolumeByBrokerSeries


# 获取股票成交金额(分券商明细) -> getPrtStockVolumeByBroker


# 获取重仓债券名称时间序列 -> getPrtTopBondNameSeries


# 获取重仓债券名称 -> getPrtTopBondName


# 获取重仓债券代码时间序列 -> getPrtTopBondSymbolSeries


# 获取重仓债券代码 -> getPrtTopBondSymbol


# 获取重仓债券持仓数量时间序列 -> getPrtTopBondQuantitySeries


# 获取重仓债券持仓数量 -> getPrtTopBondQuantity


# 获取重仓债券持仓市值时间序列 -> getPrtTopBondValueSeries


# 获取重仓债券持仓市值 -> getPrtTopBondValue


# 获取重仓债券持仓变动时间序列 -> getPrtTopBondHoldingChangingSeries


# 获取重仓债券持仓变动 -> getPrtTopBondHoldingChanging


# 获取重仓债券持有基金数时间序列 -> getPrtFundNoOfBondsSeries


# 获取重仓债券持有基金数 -> getPrtFundNoOfBonds


# 获取重仓资产支持证券名称时间序列 -> getPrtTopAbsNameSeries


# 获取重仓资产支持证券名称 -> getPrtTopAbsName


# 获取重仓资产支持证券代码时间序列 -> getPrtTopAbsSymbolSeries


# 获取重仓资产支持证券代码 -> getPrtTopAbsSymbol


# 获取重仓资产支持证券持仓数量时间序列 -> getPrtTopAbsQuantitySeries


# 获取重仓资产支持证券持仓数量 -> getPrtTopAbsQuantity


# 获取重仓资产支持证券持有市值时间序列 -> getPrtTopAbsValueSeries


# 获取重仓资产支持证券持有市值 -> getPrtTopAbsValue


# 获取重仓资产支持证券持仓变动时间序列 -> getPrtTopAbsHoldingChangingSeries


# 获取重仓资产支持证券持仓变动 -> getPrtTopAbsHoldingChanging


# 获取重仓基金名称时间序列 -> getPrtTopFundNameSeries


# 获取重仓基金名称 -> getPrtTopFundName


# 获取重仓基金代码时间序列 -> getPrtTopFundCodeSeries


# 获取重仓基金代码 -> getPrtTopFundCode


# 获取重仓基金持仓数量时间序列 -> getPrtTopFundQuantitySeries


# 获取重仓基金持仓数量 -> getPrtTopFundQuantity


# 获取重仓基金持有市值时间序列 -> getPrtTopFundValueSeries


# 获取重仓基金持有市值 -> getPrtTopFundValue


# 获取重仓基金持仓变动时间序列 -> getPrtTopFundHoldingChangingSeries


# 获取重仓基金持仓变动 -> getPrtTopFundHoldingChanging


# 获取重仓基金持有基金数时间序列 -> getPrtFundNoOfFundsSeries


# 获取重仓基金持有基金数 -> getPrtFundNoOfFunds


# 获取报告期内偏离度的绝对值在0.25%(含)-0.5%间的次数时间序列 -> getMmFrequencyOfDeviationSeries


# 获取报告期内偏离度的绝对值在0.25%(含)-0.5%间的次数 -> getMmFrequencyOfDeviation


# 获取报告期内偏离度的最高值时间序列 -> getMmMaxDeviationSeries


# 获取报告期内偏离度的最高值 -> getMmMaxDeviation


# 获取报告期内偏离度的最低值时间序列 -> getMmmInDeviationSeries


# 获取报告期内偏离度的最低值 -> getMmmInDeviation


# 获取报告期内每个工作日偏离度的绝对值的简单平均值时间序列 -> getMmAvgDeviationSeries


# 获取报告期内每个工作日偏离度的绝对值的简单平均值 -> getMmAvgDeviation


# 获取资产估值时间序列 -> getFundReItsEValueSeries


# 获取资产估值 -> getFundReItsEValue


# 获取可供分配金额(预测)时间序列 -> getFundReItsDIsTrAmountFSeries


# 获取可供分配金额(预测) -> getFundReItsDIsTrAmountF


# 获取派息率(预测)时间序列 -> getFundReItsDprFSeries


# 获取派息率(预测) -> getFundReItsDprF


# 获取综合管理人员人数时间序列 -> getEmployeeAdminSeries


# 获取综合管理人员人数 -> getEmployeeAdmin


# 获取综合管理人员人数占比时间序列 -> getEmployeeAdminPctSeries


# 获取综合管理人员人数占比 -> getEmployeeAdminPct


# 获取综合成本率(产险)时间序列 -> getStmNoteInSur9Series


# 获取综合成本率(产险) -> getStmNoteInSur9


# 获取综合偿付能力溢额时间序列 -> getQStmNoteInSur212507Series


# 获取综合偿付能力溢额 -> getQStmNoteInSur212507


# 获取综合偿付能力充足率时间序列 -> getQStmNoteInSur212508Series


# 获取综合偿付能力充足率 -> getQStmNoteInSur212508


# 获取综合流动比率:3个月内时间序列 -> getQStmNoteInSur212534Series


# 获取综合流动比率:3个月内 -> getQStmNoteInSur212534


# 获取综合流动比率:1年内时间序列 -> getQStmNoteInSur212535Series


# 获取综合流动比率:1年内 -> getQStmNoteInSur212535


# 获取综合流动比率:1年以上时间序列 -> getQStmNoteInSur212536Series


# 获取综合流动比率:1年以上 -> getQStmNoteInSur212536


# 获取综合流动比率:1-3年内时间序列 -> getQStmNoteInSur212537Series


# 获取综合流动比率:1-3年内 -> getQStmNoteInSur212537


# 获取综合流动比率:3-5年内时间序列 -> getQStmNoteInSur212538Series


# 获取综合流动比率:3-5年内 -> getQStmNoteInSur212538


# 获取综合流动比率:5年以上时间序列 -> getQStmNoteInSur212539Series


# 获取综合流动比率:5年以上 -> getQStmNoteInSur212539


# 获取综合收益_GSD时间序列 -> getWgsDComPrIncSeries


# 获取综合收益_GSD -> getWgsDComPrInc


# 获取综合收益总额时间序列 -> getStm07IsReItsGeneralProfitSeries


# 获取综合收益总额 -> getStm07IsReItsGeneralProfit


# 获取市场综合3年评级时间序列 -> getRatingMarketAvgSeries


# 获取市场综合3年评级 -> getRatingMarketAvg


# 获取其他综合性收益_GSD时间序列 -> getWgsDComEqForExChSeries


# 获取其他综合性收益_GSD -> getWgsDComEqForExCh


# 获取其他综合收益_BS时间序列 -> getOtherCompRehIncBsSeries


# 获取其他综合收益_BS -> getOtherCompRehIncBs


# 获取其他综合收益时间序列 -> getOtherCompRehIncSeries


# 获取其他综合收益 -> getOtherCompRehInc


# 获取废水综合利用率时间序列 -> getEsGEwa01004Series


# 获取废水综合利用率 -> getEsGEwa01004


# 获取Wind综合评级时间序列 -> getRatingWindAvgSeries


# 获取Wind综合评级 -> getRatingWindAvg


# 获取单季度.综合收益_GSD时间序列 -> getWgsDQfaComPrIncSeries


# 获取单季度.综合收益_GSD -> getWgsDQfaComPrInc


# 获取单季度.综合收益总额时间序列 -> getQfaToTCompRehIncSeries


# 获取单季度.综合收益总额 -> getQfaToTCompRehInc


# 获取最近一次风险综合评级类别时间序列 -> getQStmNoteInSur212529Series


# 获取最近一次风险综合评级类别 -> getQStmNoteInSur212529


# 获取归属普通股东综合收益_GSD时间序列 -> getWgsDCompRehIncParentCompSeries


# 获取归属普通股东综合收益_GSD -> getWgsDCompRehIncParentComp


# 获取单季度.其他综合收益时间序列 -> getQfaOtherCompRehIncSeries


# 获取单季度.其他综合收益 -> getQfaOtherCompRehInc


# 获取租户认缴物业维护综合费_GSD时间序列 -> getWgsDTenantReImExpSeries


# 获取租户认缴物业维护综合费_GSD -> getWgsDTenantReImExp


# 获取归属于少数股东的综合收益总额时间序列 -> getToTCompRehIncMinSHrhLDrSeries


# 获取归属于少数股东的综合收益总额 -> getToTCompRehIncMinSHrhLDr


# 获取Wind ESG综合得分时间序列 -> getEsGScoreWindSeries


# 获取Wind ESG综合得分 -> getEsGScoreWind


# 获取上海证券3年评级(综合评级)时间序列 -> getRatingShanghaiOverall3YSeries


# 获取上海证券3年评级(综合评级) -> getRatingShanghaiOverall3Y


# 获取上海证券5年评级(综合评级)时间序列 -> getRatingShanghaiOverall5YSeries


# 获取上海证券5年评级(综合评级) -> getRatingShanghaiOverall5Y


# 获取单季度.归属普通股东综合收益_GSD时间序列 -> getWgsDQfaCompRehIncParentCompSeries


# 获取单季度.归属普通股东综合收益_GSD -> getWgsDQfaCompRehIncParentComp


# 获取归属于母公司普通股东综合收益总额时间序列 -> getToTCompRehIncParentCompSeries


# 获取归属于母公司普通股东综合收益总额 -> getToTCompRehIncParentComp


# 获取单季度.租户认缴物业维护综合费_GSD时间序列 -> getWgsDQfaTenantReImExpSeries


# 获取单季度.租户认缴物业维护综合费_GSD -> getWgsDQfaTenantReImExp


# 获取单季度.归属于少数股东的综合收益总额时间序列 -> getQfaToTCompRehIncMinSHrhLDrSeries


# 获取单季度.归属于少数股东的综合收益总额 -> getQfaToTCompRehIncMinSHrhLDr


# 获取单季度.归属于母公司普通股东综合收益总额时间序列 -> getQfaToTCompRehIncParentCompSeries


# 获取单季度.归属于母公司普通股东综合收益总额 -> getQfaToTCompRehIncParentComp


# 获取以公允价值计量且其变动计入其他综合收益的金融资产时间序列 -> getFinAssetsChgCompRehIncSeries


# 获取以公允价值计量且其变动计入其他综合收益的金融资产 -> getFinAssetsChgCompRehInc


# 获取社会保险费:本期增加时间序列 -> getStmNoteSocialSecurityAddSeries


# 获取社会保险费:本期增加 -> getStmNoteSocialSecurityAdd


# 获取社会保险费:期初余额时间序列 -> getStmNoteSocialSecuritySbSeries


# 获取社会保险费:期初余额 -> getStmNoteSocialSecuritySb


# 获取社会保险费:期末余额时间序列 -> getStmNoteSocialSecurityEbSeries


# 获取社会保险费:期末余额 -> getStmNoteSocialSecurityEb


# 获取社会保险费:本期减少时间序列 -> getStmNoteSocialSecurityDeSeries


# 获取社会保险费:本期减少 -> getStmNoteSocialSecurityDe


# 获取社会价值投资联盟ESG评级时间序列 -> getEsGRatingCasViSeries


# 获取社会价值投资联盟ESG评级 -> getEsGRatingCasVi


# 获取统一社会信用代码时间序列 -> getRegisterNumberSeries


# 获取统一社会信用代码 -> getRegisterNumber


# 获取公司是否有独立的公司社会责任报告时间序列 -> getEsGMdc01002Series


# 获取公司是否有独立的公司社会责任报告 -> getEsGMdc01002


# 获取(停止)银河1年评级时间序列 -> getRatingYinHe1YSeries


# 获取(停止)银河1年评级 -> getRatingYinHe1Y


# 获取(停止)银河2年评级时间序列 -> getRatingYinHe2YSeries


# 获取(停止)银河2年评级 -> getRatingYinHe2Y


# 获取(停止)招商3年评级时间序列 -> getRatingZhaoShang3YSeries


# 获取(停止)招商3年评级 -> getRatingZhaoShang3Y


# 获取(停止)海通3年评级时间序列 -> getRatingHaiTong3YSeries


# 获取(停止)海通3年评级 -> getRatingHaiTong3Y


# 获取(停止)投资风格时间序列 -> getFundInvestStyleSeries


# 获取(停止)投资风格 -> getFundInvestStyle


# 获取(停止)所属国信行业名称时间序列 -> getIndustryGxSeries


# 获取(停止)所属国信行业名称 -> getIndustryGx


# 获取(停止)债券评分时间序列 -> getBondScoreSeries


# 获取(停止)债券评分 -> getBondScore


# 获取(停止)发行人评分时间序列 -> getIssuersCoreSeries


# 获取(停止)发行人评分 -> getIssuersCore


# 获取(停止)公司一句话介绍时间序列 -> getAbstractSeries


# 获取(停止)公司一句话介绍 -> getAbstract


# 获取(废弃)任职基金几何总回报时间序列 -> getFundManagerTotalGeometricReturnSeries


# 获取(废弃)任职基金几何总回报 -> getFundManagerTotalGeometricReturn


# 获取(废弃)净值价格时间序列 -> getFellowNetPriceSeries


# 获取(废弃)净值价格 -> getFellowNetPrice


# 获取(废弃)估值来源时间序列 -> getDefaultSourceSeries


# 获取(废弃)估值来源 -> getDefaultSource


# 获取(废弃)区间理论价时间序列 -> getTheOPricePerSeries


# 获取(废弃)区间理论价 -> getTheOPricePer


# 获取(废弃)基金投资收益时间序列 -> getStmIs83Series


# 获取(废弃)基金投资收益 -> getStmIs83


# 获取(废弃)累计关注人数_雪球时间序列 -> getXQACcmFocusSeries


# 获取(废弃)累计关注人数_雪球 -> getXQACcmFocus


# 获取(废弃)累计讨论次数_雪球时间序列 -> getXQACcmCommentsSeries


# 获取(废弃)累计讨论次数_雪球 -> getXQACcmComments


# 获取(废弃)累计交易分享数_雪球时间序列 -> getXQACcmSharesSeries


# 获取(废弃)累计交易分享数_雪球 -> getXQACcmShares


# 获取(废弃)一周新增关注_雪球时间序列 -> getXQFocusAddedSeries


# 获取(废弃)一周新增关注_雪球 -> getXQFocusAdded


# 获取(废弃)一周新增讨论数_雪球时间序列 -> getXQCommentsAddedSeries


# 获取(废弃)一周新增讨论数_雪球 -> getXQCommentsAdded


# 获取(废弃)一周新增交易分享数_雪球时间序列 -> getXQSharesAddedSeries


# 获取(废弃)一周新增交易分享数_雪球 -> getXQSharesAdded


# 获取(废弃)一周关注增长率_雪球时间序列 -> getXQWowFocusSeries


# 获取(废弃)一周关注增长率_雪球 -> getXQWowFocus


# 获取(废弃)一周讨论增长率_雪球时间序列 -> getXQWowCommentsSeries


# 获取(废弃)一周讨论增长率_雪球 -> getXQWowComments


# 获取(废弃)一周交易分享增长率_雪球时间序列 -> getXQWowSharesSeries


# 获取(废弃)一周交易分享增长率_雪球 -> getXQWowShares


# 获取(废弃)大股东类型时间序列 -> getShareCategorySeries


# 获取(废弃)大股东类型 -> getShareCategory


# 获取(废弃)所属证监会行业名称时间序列 -> getIndustryCsrC12Series


# 获取(废弃)所属证监会行业名称 -> getIndustryCsrC12


# 获取年度现金分红比例(沪深)时间序列 -> getDivPayOutRatioSeries


# 获取年度现金分红比例(沪深) -> getDivPayOutRatio


# 获取非流通股(沪深)时间序列 -> getShareNonTradableSeries


# 获取非流通股(沪深) -> getShareNonTradable


# 获取估价收益率(中证指数)(旧)时间序列 -> getYieldCsiSeries


# 获取估价收益率(中证指数)(旧) -> getYieldCsi


# 获取估价净价(中证指数)(旧)时间序列 -> getNetCsiSeries


# 获取估价净价(中证指数)(旧) -> getNetCsi


# 获取估价全价(中证指数)(旧)时间序列 -> getDirtyCsiSeries


# 获取估价全价(中证指数)(旧) -> getDirtyCsi


# 获取估价修正久期(中证指数)(旧)时间序列 -> getModiDuraCsiSeries


# 获取估价修正久期(中证指数)(旧) -> getModiDuraCsi


# 获取估价凸性(中证指数)(旧)时间序列 -> getCNvXTyCsiSeries


# 获取估价凸性(中证指数)(旧) -> getCNvXTyCsi


# 获取首发募集资金净额(旧)时间序列 -> getIpoNetCollectionSeries


# 获取首发募集资金净额(旧) -> getIpoNetCollection


# 获取首发价格(旧)时间序列 -> getIpoPriceSeries


# 获取首发价格(旧) -> getIpoPrice


# 获取首发预计募集资金(旧)时间序列 -> getIpoExpectedCollectionSeries


# 获取首发预计募集资金(旧) -> getIpoExpectedCollection


# 获取股东售股金额(旧)时间序列 -> getIpoCollectionOldSharesSeries


# 获取股东售股金额(旧) -> getIpoCollectionOldShares


# 获取首发承销保荐费用(旧)时间序列 -> getIpoUsFeesSeries


# 获取首发承销保荐费用(旧) -> getIpoUsFees


# 获取(废弃)是否费率优惠时间序列 -> getFundFeeDiscountOrNotSeries


# 获取(废弃)是否费率优惠 -> getFundFeeDiscountOrNot


# 获取(废弃)最低申购折扣费率时间序列 -> getFundMinPurchaseDiscountsSeries


# 获取(废弃)最低申购折扣费率 -> getFundMinPurchaseDiscounts


# 获取(废弃)最低定投折扣率时间序列 -> getFundMinaIpDiscountsSeries


# 获取(废弃)最低定投折扣率 -> getFundMinaIpDiscounts


# 获取(废弃)兼职人员比例时间序列 -> getEsGSem01003Series


# 获取(废弃)兼职人员比例 -> getEsGSem01003


# 获取(废弃)市盈率百分位时间序列 -> getValPepSeries


# 获取(废弃)市盈率百分位 -> getValPep


# 获取(废弃)基金盈利概率时间序列 -> getNavWinLossRatioSeries


# 获取(废弃)基金盈利概率 -> getNavWinLossRatio


# 获取(废弃)基金到期日时间序列 -> getFundMaturityDateSeries


# 获取(废弃)基金到期日 -> getFundMaturityDate


# 获取(废弃)成立日期时间序列 -> getFoundDateSeries


# 获取(废弃)成立日期 -> getFoundDate


# 获取(废弃)主办券商(持续督导)时间序列 -> getIpoLeadUndRNSeries


# 获取(废弃)主办券商(持续督导) -> getIpoLeadUndRN


# 获取(废弃)公司独立董事(历任)时间序列 -> getFrMindPDirectorSeries


# 获取(废弃)公司独立董事(历任) -> getFrMindPDirector


# 获取证券简称时间序列 -> getSecNameSeries


# 获取证券简称 -> getSecName


# 获取证券简称(支持历史)时间序列 -> getSecName1Series


# 获取证券简称(支持历史) -> getSecName1


# 获取证券英文简称时间序列 -> getSecEnglishnameSeries


# 获取证券英文简称 -> getSecEnglishname


# 获取上市日期时间序列 -> getIpoDateSeries


# 获取上市日期 -> getIpoDate


# 获取借壳上市日期时间序列 -> getBackdoorDateSeries


# 获取借壳上市日期 -> getBackdoorDate


# 获取ETF上市日期时间序列 -> getFundEtFListedDateSeries


# 获取ETF上市日期 -> getFundEtFListedDate


# 获取REITs上市日期时间序列 -> getFundReItsListedDateSeries


# 获取REITs上市日期 -> getFundReItsListedDate


# 获取网下配售部分上市日期时间序列 -> getIpoJurisDateSeries


# 获取网下配售部分上市日期 -> getIpoJurisDate


# 获取向战略投资者配售部分上市日期时间序列 -> getIpoInStIsDateSeries


# 获取向战略投资者配售部分上市日期 -> getIpoInStIsDate


# 获取向机构投资者增发部分上市日期时间序列 -> getFellowInStListDateSeries


# 获取向机构投资者增发部分上市日期 -> getFellowInStListDate


# 获取交易所中文名称时间序列 -> getExchangeCnSeries


# 获取交易所中文名称 -> getExchangeCn


# 获取交易所英文简称时间序列 -> getExChEngSeries


# 获取交易所英文简称 -> getExChEng


# 获取上市板时间序列 -> getMktSeries


# 获取上市板 -> getMkt


# 获取证券存续状态时间序列 -> getSecStatusSeries


# 获取证券存续状态 -> getSecStatus


# 获取戴帽摘帽时间时间序列 -> getRiskAdmonitionDateSeries


# 获取戴帽摘帽时间 -> getRiskAdmonitionDate


# 获取摘牌日期时间序列 -> getDeListDateSeries


# 获取摘牌日期 -> getDeListDate


# 获取发行币种时间序列 -> getIssueCurrencyCodeSeries


# 获取发行币种 -> getIssueCurrencyCode


# 获取交易币种时间序列 -> getCurRSeries


# 获取交易币种 -> getCurR


# 获取B股市值(含限售股,交易币种)时间序列 -> getValBsHrMarketValue4Series


# 获取B股市值(含限售股,交易币种) -> getValBsHrMarketValue4


# 获取B股市值(不含限售股,交易币种)时间序列 -> getValBsHrMarketValue2Series


# 获取B股市值(不含限售股,交易币种) -> getValBsHrMarketValue2


# 获取交易结算模式时间序列 -> getFundSettlementModeSeries


# 获取交易结算模式 -> getFundSettlementMode


# 获取每股面值时间序列 -> getParValueSeries


# 获取每股面值 -> getParValue


# 获取发行时每股面值时间序列 -> getIpoParSeries


# 获取发行时每股面值 -> getIpoPar


# 获取每手股数时间序列 -> getLotSizeSeries


# 获取每手股数 -> getLotSize


# 获取交易单位时间序列 -> getTunItSeries


# 获取交易单位 -> getTunIt


# 获取所属国家或地区代码时间序列 -> getCountrySeries


# 获取所属国家或地区代码 -> getCountry


# 获取基期时间序列 -> getBaseDateSeries


# 获取基期 -> getBaseDate


# 获取基点时间序列 -> getBaseValueSeries


# 获取基点 -> getBaseValue


# 获取基点价值时间序列 -> getCalcPvbPSeries


# 获取基点价值 -> getCalcPvbP


# 获取估价基点价值(中债)时间序列 -> getVoBpCnBdSeries


# 获取估价基点价值(中债) -> getVoBpCnBd


# 获取估价基点价值(上清所)时间序列 -> getVoBpShcSeries


# 获取估价基点价值(上清所) -> getVoBpShc


# 获取平均基点价值时间序列 -> getAnalBasePointValueSeries


# 获取平均基点价值 -> getAnalBasePointValue


# 获取行权基点价值时间序列 -> getBaseValueIfExeSeries


# 获取行权基点价值 -> getBaseValueIfExe


# 获取计算浮息债隐含加息基点时间序列 -> getCalcFloatAddBpSeries


# 获取计算浮息债隐含加息基点 -> getCalcFloatAddBp


# 获取成份个数时间序列 -> getNumberOfConstituentsSeries


# 获取成份个数 -> getNumberOfConstituents


# 获取成份个数(支持历史)时间序列 -> getNumberOfConstituents2Series


# 获取成份个数(支持历史) -> getNumberOfConstituents2


# 获取最早成份日期时间序列 -> getFirstDayOfConstituentsSeries


# 获取最早成份日期 -> getFirstDayOfConstituents


# 获取加权方式时间序列 -> getMethodologySeries


# 获取加权方式 -> getMethodology


# 获取证券简介时间序列 -> getRepoBriefingSeries


# 获取证券简介 -> getRepoBriefing


# 获取发布日期时间序列 -> getLaunchDateSeries


# 获取发布日期 -> getLaunchDate


# 获取证券曾用名时间序列 -> getPreNameSeries


# 获取证券曾用名 -> getPreName


# 获取上市地点时间序列 -> getExChCitySeries


# 获取上市地点 -> getExChCity


# 获取跟踪标的基金代码时间序列 -> getTrackedByFundsSeries


# 获取跟踪标的基金代码 -> getTrackedByFunds


# 获取上级行业指数代码时间序列 -> getSuperiorCodeSeries


# 获取上级行业指数代码 -> getSuperiorCode


# 获取证券代码变更日期时间序列 -> getCodeChangeDateSeries


# 获取证券代码变更日期 -> getCodeChangeDate


# 获取主证券代码时间序列 -> getAnchorBondSeries


# 获取主证券代码 -> getAnchorBond


# 获取主指数代码时间序列 -> getMajorIndexCodeSeries


# 获取主指数代码 -> getMajorIndexCode


# 获取副指数代码时间序列 -> getSubIndexCodeSeries


# 获取副指数代码 -> getSubIndexCode


# 获取跨市场代码时间序列 -> getRelationCodeSeries


# 获取跨市场代码 -> getRelationCode


# 获取公司债对应上市公司代码时间序列 -> getBcLcSeries


# 获取公司债对应上市公司代码 -> getBcLc


# 获取中债招标发行代码时间序列 -> getTendRstCodeSeries


# 获取中债招标发行代码 -> getTendRstCode


# 获取深交所分销代码时间序列 -> getSzSeDistRibCodeSeries


# 获取深交所分销代码 -> getSzSeDistRibCode


# 获取同公司可转债简称时间序列 -> getCbNameSeries


# 获取同公司可转债简称 -> getCbName


# 获取同公司美股简称时间序列 -> getUsShareNameSeries


# 获取同公司美股简称 -> getUsShareName


# 获取股票种类时间序列 -> getStockClassSeries


# 获取股票种类 -> getStockClass


# 获取发行制度时间序列 -> getIpoIssuingSystemSeries


# 获取发行制度 -> getIpoIssuingSystem


# 获取所属上市标准时间序列 -> getListsTdSeries


# 获取所属上市标准 -> getListsTd


# 获取北交所准入标准时间序列 -> getFeaturedListsTdSeries


# 获取北交所准入标准 -> getFeaturedListsTd


# 获取是否属于重要指数成份时间序列 -> getCompIndex2Series


# 获取是否属于重要指数成份 -> getCompIndex2


# 获取所属概念板块时间序列 -> getConceptSeries


# 获取所属概念板块 -> getConcept


# 获取所属规模风格类型时间序列 -> getScaleStyleSeries


# 获取所属规模风格类型 -> getScaleStyle


# 获取是否沪港通买入标的时间序列 -> getShScSeries


# 获取是否沪港通买入标的 -> getShSc


# 获取是否深港通买入标的时间序列 -> getShSc2Series


# 获取是否深港通买入标的 -> getShSc2


# 获取是否并行代码时间序列 -> getParallelCodeSeries


# 获取是否并行代码 -> getParallelCode


# 获取证券类型时间序列 -> getSecTypeSeries


# 获取证券类型 -> getSecType


# 获取是否借壳上市时间序列 -> getBackdoorSeries


# 获取是否借壳上市 -> getBackdoor


# 获取是否上市时间序列 -> getListSeries


# 获取是否上市 -> getList


# 获取是否上市公司时间序列 -> getListingOrNotSeries


# 获取是否上市公司 -> getListingOrNot


# 获取是否属于风险警示板时间序列 -> getRiskWarningSeries


# 获取是否属于风险警示板 -> getRiskWarning


# 获取指数风格时间序列 -> getOfficialStyleSeries


# 获取指数风格 -> getOfficialStyle


# 获取所属产业链板块时间序列 -> getChainSeries


# 获取所属产业链板块 -> getChain


# 获取所属大宗商品概念板块时间序列 -> getLargeCommoditySeries


# 获取所属大宗商品概念板块 -> getLargeCommodity


# 获取存托机构时间序列 -> getDepositAryBankSeries


# 获取存托机构 -> getDepositAryBank


# 获取主办券商(持续督导)时间序列 -> getIpoLeadUndRN1Series


# 获取主办券商(持续督导) -> getIpoLeadUndRN1


# 获取做市商名称时间序列 -> getIpoMarketMakerSeries


# 获取做市商名称 -> getIpoMarketMaker


# 获取做市首日时间序列 -> getMarketMakeDateSeries


# 获取做市首日 -> getMarketMakeDate


# 获取交易类型时间序列 -> getTransferTypeSeries


# 获取交易类型 -> getTransferType


# 获取做市商家数时间序列 -> getNeEqMarketMakerNumSeries


# 获取做市商家数 -> getNeEqMarketMakerNum


# 获取挂牌园区时间序列 -> getNeEqParkSeries


# 获取挂牌园区 -> getNeEqPark


# 获取挂牌公告日时间序列 -> getNeEqListAnnDateSeries


# 获取挂牌公告日 -> getNeEqListAnnDate


# 获取转做市公告日时间序列 -> getNeEqMarketMakeAnnDateSeries


# 获取转做市公告日 -> getNeEqMarketMakeAnnDate


# 获取所属挂牌公司投资型行业名称时间序列 -> getIndustryNeeQgIcsSeries


# 获取所属挂牌公司投资型行业名称 -> getIndustryNeeQgIcs


# 获取所属挂牌公司投资型行业代码时间序列 -> getIndustryNeeQgIcsCodeInvSeries


# 获取所属挂牌公司投资型行业代码 -> getIndustryNeeQgIcsCodeInv


# 获取所属挂牌公司投资型行业板块代码时间序列 -> getIndustryNeeQgIcsCodeSeries


# 获取所属挂牌公司投资型行业板块代码 -> getIndustryNeeQgIcsCode


# 获取所属新三板概念类板块时间序列 -> getIndustryNeEqConceptSeries


# 获取所属新三板概念类板块 -> getIndustryNeEqConcept


# 获取所属分层时间序列 -> getNeEqLevelSeries


# 获取所属分层 -> getNeEqLevel


# 获取所属创新层标准时间序列 -> getNeEqStandardSeries


# 获取所属创新层标准 -> getNeEqStandard


# 获取挂牌企业上市辅导券商时间序列 -> getIpoTutorSeries


# 获取挂牌企业上市辅导券商 -> getIpoTutor


# 获取挂牌企业上市辅导开始日期时间序列 -> getIpoTutoringStartDateSeries


# 获取挂牌企业上市辅导开始日期 -> getIpoTutoringStartDate


# 获取挂牌企业上市辅导结束日期时间序列 -> getIpoTutoringEnddateSeries


# 获取挂牌企业上市辅导结束日期 -> getIpoTutoringEnddate


# 获取挂牌日时间序列 -> getNeEqListingDateSeries


# 获取挂牌日 -> getNeEqListingDate


# 获取创新层挂牌日时间序列 -> getNeEqListDateInnovationLevelSeries


# 获取创新层挂牌日 -> getNeEqListDateInnovationLevel


# 获取挂牌公司转板北交所前停牌日时间序列 -> getNeEqSuspensionDaySeries


# 获取挂牌公司转板北交所前停牌日 -> getNeEqSuspensionDay


# 获取公司中文名称时间序列 -> getCompNameSeries


# 获取公司中文名称 -> getCompName


# 获取公司英文名称时间序列 -> getCompNameEngSeries


# 获取公司英文名称 -> getCompNameEng


# 获取公司属性时间序列 -> getNature1Series


# 获取公司属性 -> getNature1


# 获取公司属性(旧)时间序列 -> getNatureSeries


# 获取公司属性(旧) -> getNature


# 获取股东公司属性时间序列 -> getShareholderNatureSeries


# 获取股东公司属性 -> getShareholderNature


# 获取担保人公司属性时间序列 -> getAgencyGuarantorNatureSeries


# 获取担保人公司属性 -> getAgencyGuarantorNature


# 获取金融机构类型时间序列 -> getInstitutionTypeSeries


# 获取金融机构类型 -> getInstitutionType


# 获取企业规模时间序列 -> getCorpScaleSeries


# 获取企业规模 -> getCorpScale


# 获取上市公司(银行)类型时间序列 -> getBankTypeSeries


# 获取上市公司(银行)类型 -> getBankType


# 获取成立日期时间序列 -> getFoundDate1Series


# 获取成立日期 -> getFoundDate1


# 获取基金管理人成立日期时间序列 -> getFundCorpEstablishmentDateSeries


# 获取基金管理人成立日期 -> getFundCorpEstablishmentDate


# 获取注册资本时间序列 -> getRegCapitalSeries


# 获取注册资本 -> getRegCapital


# 获取注册资本币种时间序列 -> getRegCapitalCurSeries


# 获取注册资本币种 -> getRegCapitalCur


# 获取基金管理人注册资本时间序列 -> getFundCorpRegisteredCapitalSeries


# 获取基金管理人注册资本 -> getFundCorpRegisteredCapital


# 获取法定代表人时间序列 -> getChairmanSeries


# 获取法定代表人 -> getChairman


# 获取法定代表人(支持历史)时间序列 -> getLegalRepresentativeSeries


# 获取法定代表人(支持历史) -> getLegalRepresentative


# 获取会计年结日时间序列 -> getFiscalDateSeries


# 获取会计年结日 -> getFiscalDate


# 获取经营范围时间序列 -> getBusinessSeries


# 获取经营范围 -> getBusiness


# 获取公司简介时间序列 -> getBriefingSeries


# 获取公司简介 -> getBriefing


# 获取股东公司简介时间序列 -> getShareholderBriefingSeries


# 获取股东公司简介 -> getShareholderBriefing


# 获取担保人公司简介时间序列 -> getAgencyGuarantorBriefingSeries


# 获取担保人公司简介 -> getAgencyGuarantorBriefing


# 获取主营产品类型时间序列 -> getMajorProductTypeSeries


# 获取主营产品类型 -> getMajorProductType


# 获取主营产品名称时间序列 -> getMajorProductNameSeries


# 获取主营产品名称 -> getMajorProductName


# 获取员工总数时间序列 -> getEmployeeSeries


# 获取员工总数 -> getEmployee


# 获取母公司员工人数时间序列 -> getEmployeePcSeries


# 获取母公司员工人数 -> getEmployeePc


# 获取所属行政区划时间序列 -> getAdministrativeDivisionSeries


# 获取所属行政区划 -> getAdministrativeDivision


# 获取所属行政区划代码时间序列 -> getAdminCodeSeries


# 获取所属行政区划代码 -> getAdminCode


# 获取所属证监会辖区时间序列 -> getCsrCJurisdictionSeries


# 获取所属证监会辖区 -> getCsrCJurisdiction


# 获取省份时间序列 -> getProvinceSeries


# 获取省份 -> getProvince


# 获取城市时间序列 -> getCitySeries


# 获取城市 -> getCity


# 获取基金管理人注册城市时间序列 -> getFundCorpCitySeries


# 获取基金管理人注册城市 -> getFundCorpCity


# 获取注册地址时间序列 -> getAddressSeries


# 获取注册地址 -> getAddress


# 获取基金管理人注册地址时间序列 -> getFundCorpAddressSeries


# 获取基金管理人注册地址 -> getFundCorpAddress


# 获取办公地址时间序列 -> getOfficeSeries


# 获取办公地址 -> getOffice


# 获取基金管理人办公地址时间序列 -> getFundCorpOfficeSeries


# 获取基金管理人办公地址 -> getFundCorpOffice


# 获取邮编时间序列 -> getZipCodeSeries


# 获取邮编 -> getZipCode


# 获取基金管理人邮编时间序列 -> getFundCorpZipSeries


# 获取基金管理人邮编 -> getFundCorpZip


# 获取公司电话时间序列 -> getPhoneSeries


# 获取公司电话 -> getPhone


# 获取公司传真时间序列 -> getFaxSeries


# 获取公司传真 -> getFax


# 获取公司电子邮件地址时间序列 -> getEmailSeries


# 获取公司电子邮件地址 -> getEmail


# 获取公司网站时间序列 -> getWebsiteSeries


# 获取公司网站 -> getWebsite


# 获取信息披露人时间序列 -> getDIsCloserSeries


# 获取信息披露人 -> getDIsCloser


# 获取信息指定披露媒体时间序列 -> getMediaSeries


# 获取信息指定披露媒体 -> getMedia


# 获取组织机构代码时间序列 -> getOrganizationCodeSeries


# 获取组织机构代码 -> getOrganizationCode


# 获取记账本位币时间序列 -> getReportCurSeries


# 获取记账本位币 -> getReportCur


# 获取发行人中文简称时间序列 -> getIssuerShortenedSeries


# 获取发行人中文简称 -> getIssuerShortened


# 获取主要产品及业务时间序列 -> getMainProductSeries


# 获取主要产品及业务 -> getMainProduct


# 获取公司曾用名时间序列 -> getCompPreNameSeries


# 获取公司曾用名 -> getCompPreName


# 获取是否发行可转债时间序列 -> getCbIssueOrNotSeries


# 获取是否发行可转债 -> getCbIssueOrNot


# 获取是否存在投票权差异时间序列 -> getVoteSeries


# 获取是否存在投票权差异 -> getVote


# 获取所属战略性新兴产业分类时间序列 -> getSeiSeries


# 获取所属战略性新兴产业分类 -> getSei


# 获取是否专精特新企业时间序列 -> getZJtXorNotSeries


# 获取是否专精特新企业 -> getZJtXorNot


# 获取所属证监会行业名称时间序列 -> getIndustryCsrC12NSeries


# 获取所属证监会行业名称 -> getIndustryCsrC12N


# 获取所属证监会行业名称(旧)时间序列 -> getIndustryCsrCSeries


# 获取所属证监会行业名称(旧) -> getIndustryCsrC


# 获取所属证监会行业代码时间序列 -> getIndustryCsrCCode12Series


# 获取所属证监会行业代码 -> getIndustryCsrCCode12


# 获取所属证监会行业代码(旧)时间序列 -> getIndustryCsrCCodeSeries


# 获取所属证监会行业代码(旧) -> getIndustryCsrCCode


# 获取所属申万行业名称时间序列 -> getIndustrySwSeries


# 获取所属申万行业名称 -> getIndustrySw


# 获取所属申万行业名称(2021)时间序列 -> getIndustrySw2021Series


# 获取所属申万行业名称(2021) -> getIndustrySw2021


# 获取所属申万行业名称(港股)时间序列 -> getIndustrySwHkSeries


# 获取所属申万行业名称(港股) -> getIndustrySwHk


# 获取所属申万行业名称(港股)(2021)时间序列 -> getIndustrySw2021HkSeries


# 获取所属申万行业名称(港股)(2021) -> getIndustrySw2021Hk


# 获取所属申万行业代码时间序列 -> getIndustrySwCodeSeries


# 获取所属申万行业代码 -> getIndustrySwCode


# 获取所属申万行业代码(2021)时间序列 -> getIndustrySwCode2021Series


# 获取所属申万行业代码(2021) -> getIndustrySwCode2021


# 获取所属申万行业代码(港股)时间序列 -> getIndustrySwCodeHkSeries


# 获取所属申万行业代码(港股) -> getIndustrySwCodeHk


# 获取所属申万行业代码(港股)(2021)时间序列 -> getIndustrySwCode2021HkSeries


# 获取所属申万行业代码(港股)(2021) -> getIndustrySwCode2021Hk


# 获取所属申万行业原始代码时间序列 -> getIndustrySwOriginCodeSeries


# 获取所属申万行业原始代码 -> getIndustrySwOriginCode


# 获取所属申万行业原始代码(2021)时间序列 -> getIndustrySwOriginCode2021Series


# 获取所属申万行业原始代码(2021) -> getIndustrySwOriginCode2021


# 获取所属申万行业指数代码时间序列 -> getIndexCodeSwSeries


# 获取所属申万行业指数代码 -> getIndexCodeSw


# 获取所属中信行业名称时间序列 -> getIndustryCitiCSeries


# 获取所属中信行业名称 -> getIndustryCitiC


# 获取所属中信行业名称(港股)时间序列 -> getIndustryCitiCHkSeries


# 获取所属中信行业名称(港股) -> getIndustryCitiCHk


# 获取所属中信行业代码时间序列 -> getIndustryCitiCCodeSeries


# 获取所属中信行业代码 -> getIndustryCitiCCode


# 获取所属中信行业代码(港股)时间序列 -> getIndustryCitiCCodeHkSeries


# 获取所属中信行业代码(港股) -> getIndustryCitiCCodeHk


# 获取所属中信行业指数代码时间序列 -> getIndexCodeCitiCSeries


# 获取所属中信行业指数代码 -> getIndexCodeCitiC


# 获取所属中信证券港股通指数代码(港股)时间序列 -> getIndexCodeCitiCHkSeries


# 获取所属中信证券港股通指数代码(港股) -> getIndexCodeCitiCHk


# 获取所属中信证券港股通指数名称(港股)时间序列 -> getIndexNameCitiCHkSeries


# 获取所属中信证券港股通指数名称(港股) -> getIndexNameCitiCHk


# 获取所属中诚信行业名称时间序列 -> getIssuerIndustryCcXiSeries


# 获取所属中诚信行业名称 -> getIssuerIndustryCcXi


# 获取废弃行业时间序列 -> getIndustryGicS2Series


# 获取废弃行业 -> getIndustryGicS2


# 获取所属恒生行业名称时间序列 -> getIndustryHsSeries


# 获取所属恒生行业名称 -> getIndustryHs


# 获取所属行业名称(支持历史)时间序列 -> getIndustry2Series


# 获取所属行业名称(支持历史) -> getIndustry2


# 获取所属行业代码(支持历史)时间序列 -> getIndustryCodeSeries


# 获取所属行业代码(支持历史) -> getIndustryCode


# 获取所属行业板块名称(支持历史)时间序列 -> getIndustryNameSeries


# 获取所属行业板块名称(支持历史) -> getIndustryName


# 获取所属中证行业名称时间序列 -> getIndustryCsiSeries


# 获取所属中证行业名称 -> getIndustryCsi


# 获取所属中证行业代码时间序列 -> getIndustryCsiCodeSeries


# 获取所属中证行业代码 -> getIndustryCsiCode


# 获取所属国民经济行业代码时间序列 -> getIndustryNcCodeSeries


# 获取所属国民经济行业代码 -> getIndustryNcCode


# 获取所属长江行业名称时间序列 -> getIndustryCJscSeries


# 获取所属长江行业名称 -> getIndustryCJsc


# 获取所属长江行业指数代码时间序列 -> getIndexCodeCJscSeries


# 获取所属长江行业指数代码 -> getIndexCodeCJsc


# 获取所属国证行业名称时间序列 -> getIndustryCnSeries


# 获取所属国证行业名称 -> getIndustryCn


# 获取所属国证行业代码时间序列 -> getIndustryCnCodeSeries


# 获取所属国证行业代码 -> getIndustryCnCode


# 获取所属国证行业指数代码时间序列 -> getIndexCodeCnSeries


# 获取所属国证行业指数代码 -> getIndexCodeCn


# 获取所属科创板主题行业时间序列 -> getThematicIndustrySibSeries


# 获取所属科创板主题行业 -> getThematicIndustrySib


# 获取董事长时间序列 -> getBoardChairmenSeries


# 获取董事长 -> getBoardChairmen


# 获取董事长薪酬时间序列 -> getStmNoteMGmtBenBcSeries


# 获取董事长薪酬 -> getStmNoteMGmtBenBc


# 获取总经理时间序列 -> getCeoSeries


# 获取总经理 -> getCeo


# 获取总经理薪酬时间序列 -> getStmNoteMGmtBenCeoSeries


# 获取总经理薪酬 -> getStmNoteMGmtBenCeo


# 获取基金管理人总经理时间序列 -> getFundCorpManagerSeries


# 获取基金管理人总经理 -> getFundCorpManager


# 获取董事会秘书时间序列 -> getDIsCloser1Series


# 获取董事会秘书 -> getDIsCloser1


# 获取董事会秘书薪酬时间序列 -> getStmNoteMGmtBenDIsCloserSeries


# 获取董事会秘书薪酬 -> getStmNoteMGmtBenDIsCloser


# 获取证券事务代表时间序列 -> getSar1Series


# 获取证券事务代表 -> getSar1


# 获取证券事务代表薪酬时间序列 -> getStmNoteMGmtBenSarSeries


# 获取证券事务代表薪酬 -> getStmNoteMGmtBenSar


# 获取财务总监时间序列 -> getCfOSeries


# 获取财务总监 -> getCfO


# 获取财务总监薪酬时间序列 -> getStmNoteMGmtBenCfOSeries


# 获取财务总监薪酬 -> getStmNoteMGmtBenCfO


# 获取公司独立董事(现任)时间序列 -> getCrtInDpDirectorSeries


# 获取公司独立董事(现任) -> getCrtInDpDirector


# 获取公司独立董事(历任)时间序列 -> getSUciNdpDirectorSeries


# 获取公司独立董事(历任) -> getSUciNdpDirector


# 获取公司董事时间序列 -> getDirectorSeries


# 获取公司董事 -> getDirector


# 获取公司董事(历任)时间序列 -> getSUcDirectorSeries


# 获取公司董事(历任) -> getSUcDirector


# 获取公司监事时间序列 -> getSupervisorSeries


# 获取公司监事 -> getSupervisor


# 获取公司监事(历任)时间序列 -> getSUcSupervisorSeries


# 获取公司监事(历任) -> getSUcSupervisor


# 获取公司高管时间序列 -> getExecutivesSeries


# 获取公司高管 -> getExecutives


# 获取公司高管(历任)时间序列 -> getSUcExecutivesSeries


# 获取公司高管(历任) -> getSUcExecutives


# 获取金额前三的董事薪酬合计时间序列 -> getStmNoteMGmtBenTop3BSeries


# 获取金额前三的董事薪酬合计 -> getStmNoteMGmtBenTop3B


# 获取金额前三的高管薪酬合计时间序列 -> getStmNoteMGmtBenTop3MSeries


# 获取金额前三的高管薪酬合计 -> getStmNoteMGmtBenTop3M


# 获取董事会人数时间序列 -> getEmployeeBoardSeries


# 获取董事会人数 -> getEmployeeBoard


# 获取非独立董事人数时间序列 -> getEmployeeExecutiveDirectorSeries


# 获取非独立董事人数 -> getEmployeeExecutiveDirector


# 获取独立董事人数时间序列 -> getEmployeeInDpDirectorSeries


# 获取独立董事人数 -> getEmployeeInDpDirector


# 获取高管人数时间序列 -> getEmployeeMGmtSeries


# 获取高管人数 -> getEmployeeMGmt


# 获取核心技术人员人数时间序列 -> getEmployeeTechCoreSeries


# 获取核心技术人员人数 -> getEmployeeTechCore


# 获取审计机构时间序列 -> getAuditorSeries


# 获取审计机构 -> getAuditor


# 获取审计机构(支持历史)时间序列 -> getAuditor2Series


# 获取审计机构(支持历史) -> getAuditor2


# 获取首发审计机构时间序列 -> getIpoAuditorSeries


# 获取首发审计机构 -> getIpoAuditor


# 获取法律顾问时间序列 -> getCloSeries


# 获取法律顾问 -> getClo


# 获取经办律师时间序列 -> getLiCSeries


# 获取经办律师 -> getLiC


# 获取首发经办律师时间序列 -> getIpoLawErSeries


# 获取首发经办律师 -> getIpoLawEr


# 获取资产评估机构时间序列 -> getFundReItSvaAgSeries


# 获取资产评估机构 -> getFundReItSvaAg


# 获取经办评估人员时间序列 -> getVicSeries


# 获取经办评估人员 -> getVic


# 获取主要往来银行时间序列 -> getBanksSeries


# 获取主要往来银行 -> getBanks


# 获取生产人员人数时间序列 -> getEmployeeProducerSeries


# 获取生产人员人数 -> getEmployeeProducer


# 获取生产人员人数占比时间序列 -> getEmployeeProducerPctSeries


# 获取生产人员人数占比 -> getEmployeeProducerPct


# 获取销售人员人数时间序列 -> getEmployeeSaleSeries


# 获取销售人员人数 -> getEmployeeSale


# 获取销售人员人数占比时间序列 -> getEmployeeSalePctSeries


# 获取销售人员人数占比 -> getEmployeeSalePct


# 获取客服人员人数时间序列 -> getEmployeeServerSeries


# 获取客服人员人数 -> getEmployeeServer


# 获取客服人员人数占比时间序列 -> getEmployeeServerPctSeries


# 获取客服人员人数占比 -> getEmployeeServerPct


# 获取技术人员人数时间序列 -> getEmployeeTechSeries


# 获取技术人员人数 -> getEmployeeTech


# 获取技术人员人数占比时间序列 -> getEmployeeTechPctSeries


# 获取技术人员人数占比 -> getEmployeeTechPct


# 获取财务人员人数时间序列 -> getEmployeeFinSeries


# 获取财务人员人数 -> getEmployeeFin


# 获取财务人员人数占比时间序列 -> getEmployeeFinPctSeries


# 获取财务人员人数占比 -> getEmployeeFinPct


# 获取人事人员人数时间序列 -> getEmployeeHrSeries


# 获取人事人员人数 -> getEmployeeHr


# 获取人事人员人数占比时间序列 -> getEmployeeHrPctSeries


# 获取人事人员人数占比 -> getEmployeeHrPct


# 获取行政人员人数时间序列 -> getEmployeeExCuSeries


# 获取行政人员人数 -> getEmployeeExCu


# 获取行政人员人数占比时间序列 -> getEmployeeExCuPctSeries


# 获取行政人员人数占比 -> getEmployeeExCuPct


# 获取风控稽核人员人数时间序列 -> getEmployeeRcSeries


# 获取风控稽核人员人数 -> getEmployeeRc


# 获取风控稽核人员人数占比时间序列 -> getEmployeeRcPctSeries


# 获取风控稽核人员人数占比 -> getEmployeeRcPct


# 获取采购仓储人员人数时间序列 -> getEmployeePurSeries


# 获取采购仓储人员人数 -> getEmployeePur


# 获取采购仓储人员人数占比时间序列 -> getEmployeePurPctSeries


# 获取采购仓储人员人数占比 -> getEmployeePurPct


# 获取其他人员人数时间序列 -> getEmployeeOThDeptSeries


# 获取其他人员人数 -> getEmployeeOThDept


# 获取博士人数时间序列 -> getEmployeePhdSeries


# 获取博士人数 -> getEmployeePhd


# 获取博士人数占比时间序列 -> getEmployeePhdPctSeries


# 获取博士人数占比 -> getEmployeePhdPct


# 获取硕士人数时间序列 -> getEmployeeMsSeries


# 获取硕士人数 -> getEmployeeMs


# 获取硕士人数占比时间序列 -> getEmployeeMsPctSeries


# 获取硕士人数占比 -> getEmployeeMsPct


# 获取本科人数时间序列 -> getEmployeeBaSeries


# 获取本科人数 -> getEmployeeBa


# 获取本科人数占比时间序列 -> getEmployeeBaPctSeries


# 获取本科人数占比 -> getEmployeeBaPct


# 获取专科人数时间序列 -> getEmployeeCollSeries


# 获取专科人数 -> getEmployeeColl


# 获取专科人数占比时间序列 -> getEmployeeCollPctSeries


# 获取专科人数占比 -> getEmployeeCollPct


# 获取高中及以下人数时间序列 -> getEmployeeHighschoolSeries


# 获取高中及以下人数 -> getEmployeeHighschool


# 获取高中及以下人数占比时间序列 -> getEmployeeHighschoolPctSeries


# 获取高中及以下人数占比 -> getEmployeeHighschoolPct


# 获取其他学历人数时间序列 -> getEmployeeOThDegreeSeries


# 获取其他学历人数 -> getEmployeeOThDegree


# 获取其他学历人数占比时间序列 -> getEmployeeOThDegreePctSeries


# 获取其他学历人数占比 -> getEmployeeOThDegreePct


# 获取其他专业人员人数占比时间序列 -> getEmployeeOThDeptPctSeries


# 获取其他专业人员人数占比 -> getEmployeeOThDeptPct


# 获取总股本时间序列 -> getTotalSharesSeries


# 获取总股本 -> getTotalShares


# 获取备考总股本(并购后)时间序列 -> getMaTotalSharesSeries


# 获取备考总股本(并购后) -> getMaTotalShares


# 获取上市前总股本时间序列 -> getShareToTSharesPreSeries


# 获取上市前总股本 -> getShareToTSharesPre


# 获取首发后总股本(上市日)时间序列 -> getIpoToTCapAfterIssueSeries


# 获取首发后总股本(上市日) -> getIpoToTCapAfterIssue


# 获取首发前总股本时间序列 -> getIpoToTCapBeforeIssueSeries


# 获取首发前总股本 -> getIpoToTCapBeforeIssue


# 获取预计发行后总股本时间序列 -> getIpoToTCapAfterIssueEstSeries


# 获取预计发行后总股本 -> getIpoToTCapAfterIssueEst


# 获取流通股东持股比例(相对总股本)时间序列 -> getHolderPctLiqSeries


# 获取流通股东持股比例(相对总股本) -> getHolderPctLiq


# 获取自由流通股本时间序列 -> getFreeFloatSharesSeries


# 获取自由流通股本 -> getFreeFloatShares


# 获取三板合计时间序列 -> getShareTotalOtcSeries


# 获取三板合计 -> getShareTotalOtc


# 获取香港上市股时间序列 -> getShareHSeries


# 获取香港上市股 -> getShareH


# 获取海外上市股时间序列 -> getShareOverSeaSeries


# 获取海外上市股 -> getShareOverSea


# 获取流通股合计时间序列 -> getShareTotalTradableSeries


# 获取流通股合计 -> getShareTotalTradable


# 获取限售股合计时间序列 -> getShareTotalRestrictedSeries


# 获取限售股合计 -> getShareTotalRestricted


# 获取非流通股时间序列 -> getShareNonTradable2Series


# 获取非流通股 -> getShareNonTradable2


# 获取原非流通股股东有效申购户数时间序列 -> getCbResultEfInvestorNonTrAdSeries


# 获取原非流通股股东有效申购户数 -> getCbResultEfInvestorNonTrAd


# 获取原非流通股股东有效申购金额时间序列 -> getCbResultEfAmNtNonTrAdSeries


# 获取原非流通股股东有效申购金额 -> getCbResultEfAmNtNonTrAd


# 获取原非流通股股东获配金额时间序列 -> getCbResultRationAmtNonTrAdSeries


# 获取原非流通股股东获配金额 -> getCbResultRationAmtNonTrAd


# 获取优先股时间序列 -> getShareNtrDPrFShareSeries


# 获取优先股 -> getShareNtrDPrFShare


# 获取优先股_GSD时间序列 -> getWgsDPfDStKSeries


# 获取优先股_GSD -> getWgsDPfDStK


# 获取优先股利及其他调整项_GSD时间序列 -> getWgsDDvdPfDAdjSeries


# 获取优先股利及其他调整项_GSD -> getWgsDDvdPfDAdj


# 获取单季度.优先股利及其他调整项_GSD时间序列 -> getWgsDQfaDvdPfDAdjSeries


# 获取单季度.优先股利及其他调整项_GSD -> getWgsDQfaDvdPfDAdj


# 获取其他权益工具:优先股时间序列 -> getOtherEquityInstrumentsPreSeries


# 获取其他权益工具:优先股 -> getOtherEquityInstrumentsPre


# 获取已发行数量时间序列 -> getShareIssuingSeries


# 获取已发行数量 -> getShareIssuing


# 获取流通股本时间序列 -> getShareIssuingMktSeries


# 获取流通股本 -> getShareIssuingMkt


# 获取限售股份(国家持股)时间序列 -> getShareRTdStateSeries


# 获取限售股份(国家持股) -> getShareRTdState


# 获取限售股份(国有法人持股)时间序列 -> getShareRTdStateJurSeries


# 获取限售股份(国有法人持股) -> getShareRTdStateJur


# 获取限售股份(其他内资持股合计)时间序列 -> getShareRTdSubOtherDomesSeries


# 获取限售股份(其他内资持股合计) -> getShareRTdSubOtherDomes


# 获取限售股份(境内法人持股)时间序列 -> getShareRTdDomesJurSeries


# 获取限售股份(境内法人持股) -> getShareRTdDomesJur


# 获取限售股份(机构配售股份)时间序列 -> getShareRTdInStSeries


# 获取限售股份(机构配售股份) -> getShareRTdInSt


# 获取限售股份(境内自然人持股)时间序列 -> getShareRTdDomeSnpSeries


# 获取限售股份(境内自然人持股) -> getShareRTdDomeSnp


# 获取限售股份(外资持股合计)时间序列 -> getShareRTdSubFrgNSeries


# 获取限售股份(外资持股合计) -> getShareRTdSubFrgN


# 获取限售股份(境外法人持股)时间序列 -> getShareRTdFrgNJurSeries


# 获取限售股份(境外法人持股) -> getShareRTdFrgNJur


# 获取限售股份(境外自然人持股)时间序列 -> getShareRTdFrgNNpSeries


# 获取限售股份(境外自然人持股) -> getShareRTdFrgNNp


# 获取质押比例时间序列 -> getSharePledgedAPctSeries


# 获取质押比例 -> getSharePledgedAPct


# 获取无限售股份质押比例时间序列 -> getShareLiqAPledgedPctSeries


# 获取无限售股份质押比例 -> getShareLiqAPledgedPct


# 获取有限售股份质押比例时间序列 -> getShareRestrictedAPledgedPctSeries


# 获取有限售股份质押比例 -> getShareRestrictedAPledgedPct


# 获取无限售股份质押数量时间序列 -> getShareLiqAPledgedSeries


# 获取无限售股份质押数量 -> getShareLiqAPledged


# 获取有限售股份质押数量时间序列 -> getShareRestrictedAPledgedSeries


# 获取有限售股份质押数量 -> getShareRestrictedAPledged


# 获取质押待购回余量时间序列 -> getSharePledgedRepurchaseSeries


# 获取质押待购回余量 -> getSharePledgedRepurchase


# 获取限售解禁日期时间序列 -> getShareRTdUnlockingDateSeries


# 获取限售解禁日期 -> getShareRTdUnlockingDate


# 获取本期解禁数量时间序列 -> getShareTradableCurrentSeries


# 获取本期解禁数量 -> getShareTradableCurrent


# 获取未流通数量时间序列 -> getShareRTdBAnceSeries


# 获取未流通数量 -> getShareRTdBAnce


# 获取解禁数据类型时间序列 -> getShareRTdDataTypeSeries


# 获取解禁数据类型 -> getShareRTdDataType


# 获取指定日之后最近一次解禁数据类型时间序列 -> getShareRTdDataTypeFwdSeries


# 获取指定日之后最近一次解禁数据类型 -> getShareRTdDataTypeFwd


# 获取解禁股份性质时间序列 -> getShareTradableShareTypeSeries


# 获取解禁股份性质 -> getShareTradableShareType


# 获取指定日之后最近一次解禁股份性质时间序列 -> getShareTradableShareTypeFwdSeries


# 获取指定日之后最近一次解禁股份性质 -> getShareTradableShareTypeFwd


# 获取指定日之后最近一次解禁日期时间序列 -> getShareRTdUnlockingDateFwdSeries


# 获取指定日之后最近一次解禁日期 -> getShareRTdUnlockingDateFwd


# 获取指定日之后最近一次解禁数量时间序列 -> getShareTradableCurrentFwdSeries


# 获取指定日之后最近一次解禁数量 -> getShareTradableCurrentFwd


# 获取流通三板股时间序列 -> getShareOtcTradableSeries


# 获取流通三板股 -> getShareOtcTradable


# 获取流通股(控股股东或实际控制人)时间序列 -> getShareOtcTradableControllerSeries


# 获取流通股(控股股东或实际控制人) -> getShareOtcTradableController


# 获取流通股(核心员工)时间序列 -> getShareOtcTradableBackboneSeries


# 获取流通股(核心员工) -> getShareOtcTradableBackbone


# 获取流通股(其他)时间序列 -> getShareOtcTradableOthersSeries


# 获取流通股(其他) -> getShareOtcTradableOthers


# 获取限售三板股时间序列 -> getShareOtcRestrictedSeries


# 获取限售三板股 -> getShareOtcRestricted


# 获取限售股份(控股股东或实际控制人)时间序列 -> getShareOtcRestrictedControllerSeries


# 获取限售股份(控股股东或实际控制人) -> getShareOtcRestrictedController


# 获取限售股份(高管持股)时间序列 -> getShareRestrictedMSeries


# 获取限售股份(高管持股) -> getShareRestrictedM


# 获取限售股份(核心员工)时间序列 -> getShareOtcRestrictedBackboneSeries


# 获取限售股份(核心员工) -> getShareOtcRestrictedBackbone


# 获取限售股份(其他)时间序列 -> getShareOtcRestrictedOthersSeries


# 获取限售股份(其他) -> getShareOtcRestrictedOthers


# 获取份额是否为合并数据时间序列 -> getUnitMergedSharesOrNotSeries


# 获取份额是否为合并数据 -> getUnitMergedSharesOrNot


# 获取持有份额是否为合并数据时间序列 -> getHolderMergedHoldingOrNotSeries


# 获取持有份额是否为合并数据 -> getHolderMergedHoldingOrNot


# 获取场内流通份额时间序列 -> getUnitFloorTradingSeries


# 获取场内流通份额 -> getUnitFloorTrading


# 获取当期场内流通份额变化时间序列 -> getUnitFloorTradingChangeSeries


# 获取当期场内流通份额变化 -> getUnitFloorTradingChange


# 获取报告期总申购份额时间序列 -> getUnitPurchaseSeries


# 获取报告期总申购份额 -> getUnitPurchase


# 获取报告期总赎回份额时间序列 -> getUnitRedemptionSeries


# 获取报告期总赎回份额 -> getUnitRedemption


# 获取报告期申购赎回净额时间序列 -> getUnitNetPurchaseSeries


# 获取报告期申购赎回净额 -> getUnitNetPurchase


# 获取单季度总申购份额时间序列 -> getUnitPurchaseQTySeries


# 获取单季度总申购份额 -> getUnitPurchaseQTy


# 获取单季度总赎回份额时间序列 -> getUnitRedemptionQTySeries


# 获取单季度总赎回份额 -> getUnitRedemptionQTy


# 获取单季度净申购赎回率时间序列 -> getUnitNetQuarterlyRatioSeries


# 获取单季度净申购赎回率 -> getUnitNetQuarterlyRatio


# 获取单季度申购赎回净额时间序列 -> getUnitNetPurchaseQTySeries


# 获取单季度申购赎回净额 -> getUnitNetPurchaseQTy


# 获取前十大股东持股比例合计时间序列 -> getHolderTop10PctSeries


# 获取前十大股东持股比例合计 -> getHolderTop10Pct


# 获取前十大股东持股数量合计时间序列 -> getHolderTop10QuantitySeries


# 获取前十大股东持股数量合计 -> getHolderTop10Quantity


# 获取前十大流通股东持股数量合计时间序列 -> getHolderTop10LiqQuantitySeries


# 获取前十大流通股东持股数量合计 -> getHolderTop10LiqQuantity


# 获取大股东累计质押数量时间序列 -> getSharePledgedAHolderSeries


# 获取大股东累计质押数量 -> getSharePledgedAHolder


# 获取大股东累计质押数量(旧)时间序列 -> getSharePledgedALargestHolderSeries


# 获取大股东累计质押数量(旧) -> getSharePledgedALargestHolder


# 获取大股东累计质押数占持股数比例时间序列 -> getSharePledgedAPctHolderSeries


# 获取大股东累计质押数占持股数比例 -> getSharePledgedAPctHolder


# 获取大股东累计质押数占持股数比例(旧)时间序列 -> getSharePledgedAPctLargestHolderSeries


# 获取大股东累计质押数占持股数比例(旧) -> getSharePledgedAPctLargestHolder


# 获取大股东累计冻结数量时间序列 -> getShareFrozenAHolderSeries


# 获取大股东累计冻结数量 -> getShareFrozenAHolder


# 获取大股东累计冻结数占持股数比例时间序列 -> getShareFrozenAPctHolderSeries


# 获取大股东累计冻结数占持股数比例 -> getShareFrozenAPctHolder


# 获取公布实际控制人名称时间序列 -> getHolderRpTControllerSeries


# 获取公布实际控制人名称 -> getHolderRpTController


# 获取实际控制人名称时间序列 -> getHolderControllerSeries


# 获取实际控制人名称 -> getHolderController


# 获取实际控制人属性时间序列 -> getHolderControllerAtTrSeries


# 获取实际控制人属性 -> getHolderControllerAtTr


# 获取机构股东名称时间序列 -> getHolderInstituteSeries


# 获取机构股东名称 -> getHolderInstitute


# 获取大股东名称时间序列 -> getHolderNameSeries


# 获取大股东名称 -> getHolderName


# 获取大股东持股数量时间序列 -> getHolderQuantitySeries


# 获取大股东持股数量 -> getHolderQuantity


# 获取大股东持股比例时间序列 -> getHolderPctSeries


# 获取大股东持股比例 -> getHolderPct


# 获取前5大股东持股比例之和_PIT时间序列 -> getHolderSumPctTop5Series


# 获取前5大股东持股比例之和_PIT -> getHolderSumPctTop5


# 获取前5大股东持股比例平方之和_PIT时间序列 -> getHolderSumsQuPctTop5Series


# 获取前5大股东持股比例平方之和_PIT -> getHolderSumsQuPctTop5


# 获取前10大股东持股比例平方之和_PIT时间序列 -> getHolderSumsQuPctTop10Series


# 获取前10大股东持股比例平方之和_PIT -> getHolderSumsQuPctTop10


# 获取大股东持股股本性质时间序列 -> getHolderShareCategorySeries


# 获取大股东持股股本性质 -> getHolderShareCategory


# 获取大股东持有的限售股份数时间序列 -> getHolderQuantityRestrictedSeries


# 获取大股东持有的限售股份数 -> getHolderQuantityRestricted


# 获取大股东性质时间序列 -> getHolderNatureSeries


# 获取大股东性质 -> getHolderNature


# 获取机构股东类型时间序列 -> getHolderCategorySeries


# 获取机构股东类型 -> getHolderCategory


# 获取流通股东名称时间序列 -> getHolderLiqNameSeries


# 获取流通股东名称 -> getHolderLiqName


# 获取流通股东持股数量时间序列 -> getHolderLiqQuantitySeries


# 获取流通股东持股数量 -> getHolderLiqQuantity


# 获取流通股东持股比例时间序列 -> getHolderLiqPctSeries


# 获取流通股东持股比例 -> getHolderLiqPct


# 获取流通股东持股股本性质时间序列 -> getHolderLiqShareCategorySeries


# 获取流通股东持股股本性质 -> getHolderLiqShareCategory


# 获取户均持股数量时间序列 -> getHolderAvgNumSeries


# 获取户均持股数量 -> getHolderAvgNum


# 获取户均持股比例时间序列 -> getHolderAvgPctSeries


# 获取户均持股比例 -> getHolderAvgPct


# 获取户均持股比例半年增长率时间序列 -> getHolderHAvgPctChangeSeries


# 获取户均持股比例半年增长率 -> getHolderHAvgPctChange


# 获取户均持股比例季度增长率时间序列 -> getHolderQAvgPctChangeSeries


# 获取户均持股比例季度增长率 -> getHolderQAvgPctChange


# 获取相对上一报告期户均持股比例差时间序列 -> getHolderAvgPctChangeSeries


# 获取相对上一报告期户均持股比例差 -> getHolderAvgPctChange


# 获取户均持股数半年增长率时间序列 -> getHolderHAvgChangeSeries


# 获取户均持股数半年增长率 -> getHolderHAvgChange


# 获取户均持股数季度增长率时间序列 -> getHolderQAvgChangeSeries


# 获取户均持股数季度增长率 -> getHolderQAvgChange


# 获取基金持股数量时间序列 -> getHolderTotalByFundSeries


# 获取基金持股数量 -> getHolderTotalByFund


# 获取社保基金持股数量时间序列 -> getHolderTotalBySSFundSeries


# 获取社保基金持股数量 -> getHolderTotalBySSFund


# 获取券商持股数量时间序列 -> getHolderTotalByBySecSeries


# 获取券商持股数量 -> getHolderTotalByBySec


# 获取券商理财产品持股数量时间序列 -> getHolderTotalByByWMpSeries


# 获取券商理财产品持股数量 -> getHolderTotalByByWMp


# 获取阳光私募持股数量时间序列 -> getHolderTotalByHfSeries


# 获取阳光私募持股数量 -> getHolderTotalByHf


# 获取保险公司持股数量时间序列 -> getHolderTotalByInSurSeries


# 获取保险公司持股数量 -> getHolderTotalByInSur


# 获取企业年金持股数量时间序列 -> getHolderTotalByCorpPensionSeries


# 获取企业年金持股数量 -> getHolderTotalByCorpPension


# 获取信托公司持股数量时间序列 -> getHolderTotalByTrustCorpSeries


# 获取信托公司持股数量 -> getHolderTotalByTrustCorp


# 获取财务公司持股数量时间序列 -> getHolderTotalByFinanceCorpSeries


# 获取财务公司持股数量 -> getHolderTotalByFinanceCorp


# 获取银行持股数量时间序列 -> getHolderTotalByBankSeries


# 获取银行持股数量 -> getHolderTotalByBank


# 获取一般法人持股数量时间序列 -> getHolderTotalByGeneralCorpSeries


# 获取一般法人持股数量 -> getHolderTotalByGeneralCorp


# 获取非金融类上市公司持股数量时间序列 -> getHolderTotalByLnFCorpSeries


# 获取非金融类上市公司持股数量 -> getHolderTotalByLnFCorp


# 获取基金持股比例时间序列 -> getHolderPctByFundSeries


# 获取基金持股比例 -> getHolderPctByFund


# 获取社保基金持股比例时间序列 -> getHolderPctBySSFundSeries


# 获取社保基金持股比例 -> getHolderPctBySSFund


# 获取券商持股比例时间序列 -> getHolderPctBySecSeries


# 获取券商持股比例 -> getHolderPctBySec


# 获取券商理财产品持股比例时间序列 -> getHolderPctByByWMpSeries


# 获取券商理财产品持股比例 -> getHolderPctByByWMp


# 获取阳光私募持股比例时间序列 -> getHolderPctByHfSeries


# 获取阳光私募持股比例 -> getHolderPctByHf


# 获取保险公司持股比例时间序列 -> getHolderPctByInSurSeries


# 获取保险公司持股比例 -> getHolderPctByInSur


# 获取企业年金持股比例时间序列 -> getHolderPctByCorpPensionSeries


# 获取企业年金持股比例 -> getHolderPctByCorpPension


# 获取信托公司持股比例时间序列 -> getHolderPctByTrustCorpSeries


# 获取信托公司持股比例 -> getHolderPctByTrustCorp


# 获取财务公司持股比例时间序列 -> getHolderPctByFinanceCorpSeries


# 获取财务公司持股比例 -> getHolderPctByFinanceCorp


# 获取银行持股比例时间序列 -> getHolderPctByBankSeries


# 获取银行持股比例 -> getHolderPctByBank


# 获取一般法人持股比例时间序列 -> getHolderPctByGeneralCorpSeries


# 获取一般法人持股比例 -> getHolderPctByGeneralCorp


# 获取非金融类上市公司持股比例时间序列 -> getHolderPctByLnFCorpSeries


# 获取非金融类上市公司持股比例 -> getHolderPctByLnFCorp


# 获取持股机构数时间序列 -> getHolderNumISeries


# 获取持股机构数 -> getHolderNumI


# 获取持股基金数时间序列 -> getHolderNumFundSeries


# 获取持股基金数 -> getHolderNumFund


# 获取持股社保基金数时间序列 -> getHolderNumSSFundSeries


# 获取持股社保基金数 -> getHolderNumSSFund


# 获取持股保险公司数时间序列 -> getHolderNumInSurSeries


# 获取持股保险公司数 -> getHolderNumInSur


# 获取定向增发价格时间序列 -> getHolderPriceFellowOnSeries


# 获取定向增发价格 -> getHolderPriceFellowOn


# 获取大股东增持价格时间序列 -> getHolderPriceMajorShareholdersSeries


# 获取大股东增持价格 -> getHolderPriceMajorShareholders


# 获取员工持股计划买入价格时间序列 -> getHolderPriceEsOpSeries


# 获取员工持股计划买入价格 -> getHolderPriceEsOp


# 获取持有人户数是否为合并数据时间序列 -> getHolderMergedNumberOrNotSeries


# 获取持有人户数是否为合并数据 -> getHolderMergedNumberOrNot


# 获取机构投资者持有份额时间序列 -> getHolderInstitutionHoldingSeries


# 获取机构投资者持有份额 -> getHolderInstitutionHolding


# 获取机构投资者持有份额(合计)时间序列 -> getHolderInstitutionTotalHoldingSeries


# 获取机构投资者持有份额(合计) -> getHolderInstitutionTotalHolding


# 获取机构投资者持有比例时间序列 -> getHolderInstitutionHoldingPctSeries


# 获取机构投资者持有比例 -> getHolderInstitutionHoldingPct


# 获取机构投资者持有比例(合计)时间序列 -> getHolderInstitutionTotalHoldingPctSeries


# 获取机构投资者持有比例(合计) -> getHolderInstitutionTotalHoldingPct


# 获取管理人员工持有份额时间序列 -> getHolderMNgEmpHoldingSeries


# 获取管理人员工持有份额 -> getHolderMNgEmpHolding


# 获取管理人员工持有比例时间序列 -> getHolderMNgEmpHoldingPctSeries


# 获取管理人员工持有比例 -> getHolderMNgEmpHoldingPct


# 获取基金管理公司持有份额时间序列 -> getHolderCorpHoldingSeries


# 获取基金管理公司持有份额 -> getHolderCorpHolding


# 获取基金管理公司持有比例时间序列 -> getHolderCorpHoldingPctSeries


# 获取基金管理公司持有比例 -> getHolderCorpHoldingPct


# 获取个人投资者持有份额时间序列 -> getHolderPersonalHoldingSeries


# 获取个人投资者持有份额 -> getHolderPersonalHolding


# 获取个人投资者持有份额(合计)时间序列 -> getHolderPersonalTotalHoldingSeries


# 获取个人投资者持有份额(合计) -> getHolderPersonalTotalHolding


# 获取个人投资者持有比例时间序列 -> getHolderPersonalHoldingPctSeries


# 获取个人投资者持有比例 -> getHolderPersonalHoldingPct


# 获取个人投资者持有比例(合计)时间序列 -> getHolderPersonalTotalHoldingPctSeries


# 获取个人投资者持有比例(合计) -> getHolderPersonalTotalHoldingPct


# 获取前十大持有人持有份额合计时间序列 -> getFundHolderTop10HoldingSeries


# 获取前十大持有人持有份额合计 -> getFundHolderTop10Holding


# 获取前十大持有人持有份额合计(货币)时间序列 -> getFundHolderTop10HoldingMmFSeries


# 获取前十大持有人持有份额合计(货币) -> getFundHolderTop10HoldingMmF


# 获取前十大持有人持有比例合计时间序列 -> getFundHolderTop10PctSeries


# 获取前十大持有人持有比例合计 -> getFundHolderTop10Pct


# 获取前十大持有人持有比例合计(货币)时间序列 -> getFundHolderTop10PctMmFSeries


# 获取前十大持有人持有比例合计(货币) -> getFundHolderTop10PctMmF


# 获取单一投资者报告期末持有份额时间序列 -> getHolderSingleHoldingSeries


# 获取单一投资者报告期末持有份额 -> getHolderSingleHolding


# 获取单一投资者报告期末持有份额合计时间序列 -> getHolderSingleTotalHoldingSeries


# 获取单一投资者报告期末持有份额合计 -> getHolderSingleTotalHolding


# 获取单一投资者报告期末持有比例时间序列 -> getHolderSingleHoldingPctSeries


# 获取单一投资者报告期末持有比例 -> getHolderSingleHoldingPct


# 获取单一投资者报告期末持有比例合计时间序列 -> getHolderSingleTotalHoldingPctSeries


# 获取单一投资者报告期末持有比例合计 -> getHolderSingleTotalHoldingPct


# 获取合格投资者类型时间序列 -> getBondQualifiedInvestorSeries


# 获取合格投资者类型 -> getBondQualifiedInvestor


# 获取持有基金家数时间序列 -> getFundHoldFundsSeries


# 获取持有基金家数 -> getFundHoldFunds


# 获取基金持有数量合计占存量比时间序列 -> getFundHoldRatioOfPositionToAmNtSeries


# 获取基金持有数量合计占存量比 -> getFundHoldRatioOfPositionToAmNt


# 获取基金持有数量合计时间序列 -> getFundHoldPositionSeries


# 获取基金持有数量合计 -> getFundHoldPosition


# 获取持有人名称时间序列 -> getBondHolderNameSeries


# 获取持有人名称 -> getBondHolderName


# 获取第N名持有人名称时间序列 -> getFundHolderNameSeries


# 获取第N名持有人名称 -> getFundHolderName


# 获取第N名持有人名称(上市公告)时间序列 -> getFundHolderNameListingSeries


# 获取第N名持有人名称(上市公告) -> getFundHolderNameListing


# 获取持有人持有比例时间序列 -> getBondHolderPctSeries


# 获取持有人持有比例 -> getBondHolderPct


# 获取第N名持有人持有比例时间序列 -> getFundHolderPctSeries


# 获取第N名持有人持有比例 -> getFundHolderPct


# 获取第N名持有人持有比例(上市公告)时间序列 -> getFundHolderPctListingSeries


# 获取第N名持有人持有比例(上市公告) -> getFundHolderPctListing


# 获取第N名持有人持有比例(货币)时间序列 -> getFundHolderPctMmFSeries


# 获取第N名持有人持有比例(货币) -> getFundHolderPctMmF


# 获取持有人持有数量时间序列 -> getBondHolderQuantitySeries


# 获取持有人持有数量 -> getBondHolderQuantity


# 获取持有基金名称时间序列 -> getFundHoldBondNamesSeries


# 获取持有基金名称 -> getFundHoldBondNames


# 获取基金持债市值时间序列 -> getFundHoldBondValueSeries


# 获取基金持债市值 -> getFundHoldBondValue


# 获取基金持债市值占发行量比时间序列 -> getFundHoldBondRatioSeries


# 获取基金持债市值占发行量比 -> getFundHoldBondRatio


# 获取沪(深)股通持股数量时间序列 -> getShareNSeries


# 获取沪(深)股通持股数量 -> getShareN


# 获取港股通持股数量时间序列 -> getShareHkSSeries


# 获取港股通持股数量 -> getShareHkS


# 获取沪市港股通持股数量时间序列 -> getShareHkShSeries


# 获取沪市港股通持股数量 -> getShareHkSh


# 获取深市港股通持股数量时间序列 -> getShareHkSzSeries


# 获取深市港股通持股数量 -> getShareHkSz


# 获取沪(深)股通持股占比时间序列 -> getSharePctNSeries


# 获取沪(深)股通持股占比 -> getSharePctN


# 获取沪(深)股通持股占自由流通股比例时间序列 -> getSharePctNToFreeFloatSeries


# 获取沪(深)股通持股占自由流通股比例 -> getSharePctNToFreeFloat


# 获取港股通持股占比时间序列 -> getSharePctHkSSeries


# 获取港股通持股占比 -> getSharePctHkS


# 获取沪市港股通持股占比时间序列 -> getSharePctHkShSeries


# 获取沪市港股通持股占比 -> getSharePctHkSh


# 获取深市港股通持股占比时间序列 -> getSharePctHkSzSeries


# 获取深市港股通持股占比 -> getSharePctHkSz


# 获取证券全称时间序列 -> getFullNameSeries


# 获取证券全称 -> getFullName


# 获取债务主体时间序列 -> getIssuerUpdatedSeries


# 获取债务主体 -> getIssuerUpdated


# 获取实际发行人时间序列 -> getIssuerActualSeries


# 获取实际发行人 -> getIssuerActual


# 获取债券初始面值时间序列 -> getParSeries


# 获取债券初始面值 -> getPar


# 获取债券最新面值时间序列 -> getLatestParSeries


# 获取债券最新面值 -> getLatestPar


# 获取发行总额时间序列 -> getIssueAmountSeries


# 获取发行总额 -> getIssueAmount


# 获取各级发行总额时间序列 -> getTrancheSeries


# 获取各级发行总额 -> getTranche


# 获取转债发行总额时间序列 -> getCbIssueAmountSeries


# 获取转债发行总额 -> getCbIssueAmount


# 获取计划发行总额时间序列 -> getIssueAmountPlanSeries


# 获取计划发行总额 -> getIssueAmountPlan


# 获取计划发行总额(文字)时间序列 -> getTenderAmountPlanSeries


# 获取计划发行总额(文字) -> getTenderAmountPlan


# 获取实际发行总额时间序列 -> getTendRstAmountActSeries


# 获取实际发行总额 -> getTendRstAmountAct


# 获取各级占比时间序列 -> getTrancheRatioSeries


# 获取各级占比 -> getTrancheRatio


# 获取债券余额时间序列 -> getOutstandingBalanceSeries


# 获取债券余额 -> getOutstandingBalance


# 获取存量债券余额时间序列 -> getFinaTotalAmountSeries


# 获取存量债券余额 -> getFinaTotalAmount


# 获取存量债券余额(支持历史)时间序列 -> getFinalTotalAmOutAnytimeSeries


# 获取存量债券余额(支持历史) -> getFinalTotalAmOutAnytime


# 获取存量债券余额(按期限)时间序列 -> getFinaMatSeries


# 获取存量债券余额(按期限) -> getFinaMat


# 获取国债余额(做市后)时间序列 -> getTBondBalanceSeries


# 获取国债余额(做市后) -> getTBondBalance


# 获取起息日期时间序列 -> getCarryDateSeries


# 获取起息日期 -> getCarryDate


# 获取计息截止日时间序列 -> getCarryEnddateSeries


# 获取计息截止日 -> getCarryEnddate


# 获取到期日期时间序列 -> getMaturityDateSeries


# 获取到期日期 -> getMaturityDate


# 获取债券期限(年)时间序列 -> getTermSeries


# 获取债券期限(年) -> getTerm


# 获取债券期限(文字)时间序列 -> getTerm2Series


# 获取债券期限(文字) -> getTerm2


# 获取利率类型时间序列 -> getInterestTypeSeries


# 获取利率类型 -> getInterestType


# 获取票面利率(发行时)时间序列 -> getCouponRateSeries


# 获取票面利率(发行时) -> getCouponRate


# 获取利率说明时间序列 -> getCouponTxtSeries


# 获取利率说明 -> getCouponTxt


# 获取补偿利率说明时间序列 -> getClauseInterest6Series


# 获取补偿利率说明 -> getClauseInterest6


# 获取计息方式时间序列 -> getPaymentTypeSeries


# 获取计息方式 -> getPaymentType


# 获取计息基准时间序列 -> getActualBenchmarkSeries


# 获取计息基准 -> getActualBenchmark


# 获取息票品种时间序列 -> getCouponSeries


# 获取息票品种 -> getCoupon


# 获取凭证类别时间序列 -> getFormSeries


# 获取凭证类别 -> getForm


# 获取每年付息次数时间序列 -> getInterestFrequencySeries


# 获取每年付息次数 -> getInterestFrequency


# 获取年付息日时间序列 -> getPaymentDateSeries


# 获取年付息日 -> getPaymentDate


# 获取付息日说明时间序列 -> getCouponDateTxtSeries


# 获取付息日说明 -> getCouponDateTxt


# 获取是否免税时间序列 -> getTaxFreeSeries


# 获取是否免税 -> getTaxFree


# 获取税率时间序列 -> getTaxRateSeries


# 获取税率 -> getTaxRate


# 获取市价类型时间序列 -> getMktPriceTypeSeries


# 获取市价类型 -> getMktPriceType


# 获取兑付日时间序列 -> getRedemptionBeginningSeries


# 获取兑付日 -> getRedemptionBeginning


# 获取兑付登记日时间序列 -> getRedemptionRegBeginningSeries


# 获取兑付登记日 -> getRedemptionRegBeginning


# 获取兑付费率时间序列 -> getRedemptionFeeRationSeries


# 获取兑付费率 -> getRedemptionFeeRation


# 获取偿还方式时间序列 -> getRepaymentMethodSeries


# 获取偿还方式 -> getRepaymentMethod


# 获取偿付顺序时间序列 -> getPaymentOrderSeries


# 获取偿付顺序 -> getPaymentOrder


# 获取资产是否出表时间序列 -> getIsAssetOutSeries


# 获取资产是否出表 -> getIsAssetOut


# 获取计划管理人时间序列 -> getAbsSPvSeries


# 获取计划管理人 -> getAbsSPv


# 获取原始权益人时间序列 -> getFundReItsOriginalSeries


# 获取原始权益人 -> getFundReItsOriginal


# 获取原始权益人企业性质时间序列 -> getFundReItsOrComSeries


# 获取原始权益人企业性质 -> getFundReItsOrCom


# 获取穿透信用主体时间序列 -> getAbsPenetrateActRuAlDebtorSeries


# 获取穿透信用主体 -> getAbsPenetrateActRuAlDebtor


# 获取发行人(银行)类型时间序列 -> getIssuerBankTypeSeries


# 获取发行人(银行)类型 -> getIssuerBankType


# 获取最新交易日期时间序列 -> getRepoLastEstDateSeries


# 获取最新交易日期 -> getRepoLastEstDate


# 获取当前贷款笔数时间序列 -> getAbsCurrentLoanSeries


# 获取当前贷款笔数 -> getAbsCurrentLoan


# 获取当前贷款余额时间序列 -> getAbsCurrentLoansSeries


# 获取当前贷款余额 -> getAbsCurrentLoans


# 获取当前加权平均贷款剩余期限时间序列 -> getAbsCurrentWarmSeries


# 获取当前加权平均贷款剩余期限 -> getAbsCurrentWarm


# 获取当前加权平均贷款利率时间序列 -> getAbsCurrentWtGAvgRateSeries


# 获取当前加权平均贷款利率 -> getAbsCurrentWtGAvgRate


# 获取累计违约率时间序列 -> getAbsCumulativeDefaultRateSeries


# 获取累计违约率 -> getAbsCumulativeDefaultRate


# 获取严重拖欠率时间序列 -> getAbsDelinquencyRateSeries


# 获取严重拖欠率 -> getAbsDelinquencyRate


# 获取承销团成员时间序列 -> getAbsCreditNormalSeries


# 获取承销团成员 -> getAbsCreditNormal


# 获取主体行业时间序列 -> getAbsIndustrySeries


# 获取主体行业 -> getAbsIndustry


# 获取主体性质时间序列 -> getAbsIndustry1Series


# 获取主体性质 -> getAbsIndustry1


# 获取主体地区时间序列 -> getAbsProvinceSeries


# 获取主体地区 -> getAbsProvince


# 获取受托机构时间序列 -> getAbsAgencyTrustee1Series


# 获取受托机构 -> getAbsAgencyTrustee1


# 获取项目名称时间序列 -> getAbsFullNameProSeries


# 获取项目名称 -> getAbsFullNamePro


# 获取项目简称时间序列 -> getAbsNameProSeries


# 获取项目简称 -> getAbsNamePro


# 获取项目代码时间序列 -> getAbsProjectCodeSeries


# 获取项目代码 -> getAbsProjectCode


# 获取还本方式时间序列 -> getAbsPayBackSeries


# 获取还本方式 -> getAbsPayBack


# 获取提前还本方式时间序列 -> getPrepayMethodSeries


# 获取提前还本方式 -> getPrepayMethod


# 获取基础债务人时间序列 -> getAbsBorrowerSeries


# 获取基础债务人 -> getAbsBorrower


# 获取基础债务人行业时间序列 -> getAbsCoreIndustrySeries


# 获取基础债务人行业 -> getAbsCoreIndustry


# 获取基础债务人地区时间序列 -> getAbsCoreProvinceSeries


# 获取基础债务人地区 -> getAbsCoreProvince


# 获取基础债务人性质时间序列 -> getAbsCorePropertySeries


# 获取基础债务人性质 -> getAbsCoreProperty


# 获取早偿率时间序列 -> getAbsRecommendCprSeries


# 获取早偿率 -> getAbsRecommendCpr


# 获取加权平均期限时间序列 -> getAbsWeightedAverageMaturityWithPrepaySeries


# 获取加权平均期限 -> getAbsWeightedAverageMaturityWithPrepay


# 获取信用支持时间序列 -> getAbsCreditSupportSeries


# 获取信用支持 -> getAbsCreditSupport


# 获取项目余额时间序列 -> getAbsDealOutStStandingAmountSeries


# 获取项目余额 -> getAbsDealOutStStandingAmount


# 获取固定资金成本时间序列 -> getAbsFiExdCapitalCostRateSeries


# 获取固定资金成本 -> getAbsFiExdCapitalCostRate


# 获取次级每期收益率上限时间序列 -> getAbsCapYieldPerTermOfSubSeries


# 获取次级每期收益率上限 -> getAbsCapYieldPerTermOfSub


# 获取自持比例时间序列 -> getAbsSelfSustainingProportionSeries


# 获取自持比例 -> getAbsSelfSustainingProportion


# 获取法定到期日时间序列 -> getAbsLegalMaturitySeries


# 获取法定到期日 -> getAbsLegalMaturity


# 获取支付日时间序列 -> getAbsPaymentDateSeries


# 获取支付日 -> getAbsPaymentDate


# 获取首次支付日时间序列 -> getAbsFirstPaymentDateSeries


# 获取首次支付日 -> getAbsFirstPaymentDate


# 获取早偿预期到期日时间序列 -> getAbsExpectedMaturityWithPrepaySeries


# 获取早偿预期到期日 -> getAbsExpectedMaturityWithPrepay


# 获取初始起算日时间序列 -> getAbsCutoffDateSeries


# 获取初始起算日 -> getAbsCutoffDate


# 获取清算起始日时间序列 -> getAbsStartDateOfAssetClearingSeries


# 获取清算起始日 -> getAbsStartDateOfAssetClearing


# 获取清算结束日时间序列 -> getAbsEnddateOfAssetClearingSeries


# 获取清算结束日 -> getAbsEnddateOfAssetClearing


# 获取差额支付承诺人时间序列 -> getAbsDefIGuarantorSeries


# 获取差额支付承诺人 -> getAbsDefIGuarantor


# 获取专项计划托管人时间序列 -> getAbsTrusteeSeries


# 获取专项计划托管人 -> getAbsTrustee


# 获取资产服务机构时间序列 -> getAbsAssetServiceAgencySeries


# 获取资产服务机构 -> getAbsAssetServiceAgency


# 获取会计处理时间序列 -> getAccountTreatmentSeries


# 获取会计处理 -> getAccountTreatment


# 获取中债债券一级分类时间序列 -> getChinaBondL1TypeSeries


# 获取中债债券一级分类 -> getChinaBondL1Type


# 获取中债债券二级分类时间序列 -> getChinaBondL2TypeSeries


# 获取中债债券二级分类 -> getChinaBondL2Type


# 获取是否城投债(Wind)时间序列 -> getMunicipalBondWindSeries


# 获取是否城投债(Wind) -> getMunicipalBondWind


# 获取是否城投债时间序列 -> getMunicipalBondSeries


# 获取是否城投债 -> getMunicipalBond


# 获取是否城投债(YY)时间序列 -> getMunicipalBondyYSeries


# 获取是否城投债(YY) -> getMunicipalBondyY


# 获取城投行政级别(Wind)时间序列 -> getCityInvestmentBondGeoWindSeries


# 获取城投行政级别(Wind) -> getCityInvestmentBondGeoWind


# 获取城投行政级别时间序列 -> getCityInvestmentBondGeoSeries


# 获取城投行政级别 -> getCityInvestmentBondGeo


# 获取是否跨市场交易时间序列 -> getMultiMktOrNotSeries


# 获取是否跨市场交易 -> getMultiMktOrNot


# 获取是否次级债时间序列 -> getSubordinateOrNotSeries


# 获取是否次级债 -> getSubordinateOrNot


# 获取是否混合资本债券时间序列 -> getMixCapitalSeries


# 获取是否混合资本债券 -> getMixCapital


# 获取是否增发时间序列 -> getIssueAdditionalSeries


# 获取是否增发 -> getIssueAdditional


# 获取增发债对应原债券时间序列 -> getAdditionalToSeries


# 获取增发债对应原债券 -> getAdditionalTo


# 获取是否永续债时间序列 -> getPerpetualOrNotSeries


# 获取是否永续债 -> getPerpetualOrNot


# 获取基准利率时间序列 -> getBaseRateSeries


# 获取基准利率 -> getBaseRate


# 获取基准利率确定方式时间序列 -> getCmBirSeries


# 获取基准利率确定方式 -> getCmBir


# 获取基准利率(发行时)时间序列 -> getBaseRate2Series


# 获取基准利率(发行时) -> getBaseRate2


# 获取基准利率(指定日期)时间序列 -> getBaseRate3Series


# 获取基准利率(指定日期) -> getBaseRate3


# 获取计算浮息债隐含基准利率时间序列 -> getCalcFloatBenchSeries


# 获取计算浮息债隐含基准利率 -> getCalcFloatBench


# 获取固定利差时间序列 -> getSpreadSeries


# 获取固定利差 -> getSpread


# 获取首个定价日时间序列 -> getIssueFirstPriceDateSeries


# 获取首个定价日 -> getIssueFirstPriceDate


# 获取票面利率(当期)时间序列 -> getCouponRate2Series


# 获取票面利率(当期) -> getCouponRate2


# 获取票面利率(指定日期)时间序列 -> getCouponRate3Series


# 获取票面利率(指定日期) -> getCouponRate3


# 获取行权后利差时间序列 -> getSpread2Series


# 获取行权后利差 -> getSpread2


# 获取保底利率时间序列 -> getInterestFloorSeries


# 获取保底利率 -> getInterestFloor


# 获取是否含权债时间序列 -> getEmbeddedOptSeries


# 获取是否含权债 -> getEmbeddedOpt


# 获取特殊条款时间序列 -> getClauseSeries


# 获取特殊条款 -> getClause


# 获取特殊条款(缩写)时间序列 -> getClauseAbbrSeries


# 获取特殊条款(缩写) -> getClauseAbbr


# 获取指定条款文字时间序列 -> getClauseItemSeries


# 获取指定条款文字 -> getClauseItem


# 获取含权债行权期限时间序列 -> getExecMaturityEmbeddedSeries


# 获取含权债行权期限 -> getExecMaturityEmbedded


# 获取含权债期限特殊说明时间序列 -> getEObSpecialInStrutIonsSeries


# 获取含权债期限特殊说明 -> getEObSpecialInStrutIons


# 获取提前还本日时间序列 -> getPrepaymentDateSeries


# 获取提前还本日 -> getPrepaymentDate


# 获取提前还本比例时间序列 -> getPrepayPortionSeries


# 获取提前还本比例 -> getPrepayPortion


# 获取赎回日时间序列 -> getRedemptionDateSeries


# 获取赎回日 -> getRedemptionDate


# 获取回售日时间序列 -> getRepurchaseDateSeries


# 获取回售日 -> getRepurchaseDate


# 获取赎回价格时间序列 -> getClauseCallOptionRedemptionPriceSeries


# 获取赎回价格 -> getClauseCallOptionRedemptionPrice


# 获取赎回价格说明时间序列 -> getClauseCallOptionRedemptionMemoSeries


# 获取赎回价格说明 -> getClauseCallOptionRedemptionMemo


# 获取回售价格时间序列 -> getClausePutOptionResellingPriceSeries


# 获取回售价格 -> getClausePutOptionResellingPrice


# 获取回售价格说明时间序列 -> getClausePutOptionResellingPriceExplainAtionSeries


# 获取回售价格说明 -> getClausePutOptionResellingPriceExplainAtion


# 获取附加回售价格说明时间序列 -> getClausePutOptionAdditionalPriceMemoSeries


# 获取附加回售价格说明 -> getClausePutOptionAdditionalPriceMemo


# 获取回售代码时间序列 -> getPutCodeSeries


# 获取回售代码 -> getPutCode


# 获取回售登记起始日时间序列 -> getRepurchaseBeginDateSeries


# 获取回售登记起始日 -> getRepurchaseBeginDate


# 获取回售登记截止日时间序列 -> getRepurchaseEnddateSeries


# 获取回售登记截止日 -> getRepurchaseEnddate


# 获取行权资金到账日时间序列 -> getFunDarRialDateSeries


# 获取行权资金到账日 -> getFunDarRialDate


# 获取票面利率调整上限时间序列 -> getCouponAdjMaxSeries


# 获取票面利率调整上限 -> getCouponAdjMax


# 获取票面利率调整下限时间序列 -> getCouponAdjMinSeries


# 获取票面利率调整下限 -> getCouponAdjMin


# 获取赎回登记日时间序列 -> getClauseCallOptionRecordDateSeries


# 获取赎回登记日 -> getClauseCallOptionRecordDate


# 获取担保人时间序列 -> getAgencyGuarantorSeries


# 获取担保人 -> getAgencyGuarantor


# 获取担保人评级时间序列 -> getRateRateGuarantorSeries


# 获取担保人评级 -> getRateRateGuarantor


# 获取担保人评级展望时间序列 -> getRateFwdGuarantorSeries


# 获取担保人评级展望 -> getRateFwdGuarantor


# 获取担保人评级变动方向时间序列 -> getRateChNgGuarantorSeries


# 获取担保人评级变动方向 -> getRateChNgGuarantor


# 获取担保人评级评级机构时间序列 -> getRateAgencyGuarantorSeries


# 获取担保人评级评级机构 -> getRateAgencyGuarantor


# 获取再担保人时间序列 -> getAgencyReGuarantorSeries


# 获取再担保人 -> getAgencyReGuarantor


# 获取发行时担保人评级时间序列 -> getRateBeginGuarantorSeries


# 获取发行时担保人评级 -> getRateBeginGuarantor


# 获取担保方式时间序列 -> getAgencyGrNtTypeSeries


# 获取担保方式 -> getAgencyGrNtType


# 获取担保期限时间序列 -> getGuarTermSeries


# 获取担保期限 -> getGuarTerm


# 获取担保范围时间序列 -> getGuarRangeSeries


# 获取担保范围 -> getGuarRange


# 获取担保条款文字时间序列 -> getAgencyGrNtRangeSeries


# 获取担保条款文字 -> getAgencyGrNtRange


# 获取反担保情况时间序列 -> getCounterGuarSeries


# 获取反担保情况 -> getCounterGuar


# 获取标准券折算金额(每百元面值)时间序列 -> getCvnTPerHundredSeries


# 获取标准券折算金额(每百元面值) -> getCvnTPerHundred


# 获取质押券代码时间序列 -> getCollateralCodeSeries


# 获取质押券代码 -> getCollateralCode


# 获取质押券简称时间序列 -> getCollateralNameSeries


# 获取质押券简称 -> getCollateralName


# 获取是否可质押时间序列 -> getFundPledGableOrNotSeries


# 获取是否可质押 -> getFundPledGableOrNot


# 获取报价式回购折算率(中证指数)时间序列 -> getRateOfStdBndCsiSeries


# 获取报价式回购折算率(中证指数) -> getRateOfStdBndCsi


# 获取是否随存款利率调整时间序列 -> getClauseInterest5Series


# 获取是否随存款利率调整 -> getClauseInterest5


# 获取是否有利息补偿时间序列 -> getClauseInterest8Series


# 获取是否有利息补偿 -> getClauseInterest8


# 获取补偿利率时间序列 -> getClauseInterestCompensationInterestSeries


# 获取补偿利率 -> getClauseInterestCompensationInterest


# 获取补偿利率(公布)时间序列 -> getClauseCompensationInterestSeries


# 获取补偿利率(公布) -> getClauseCompensationInterest


# 获取利息处理方式时间序列 -> getClauseProcessModeInterestSeries


# 获取利息处理方式 -> getClauseProcessModeInterest


# 获取正股代码时间序列 -> getUnderlyingCodeSeries


# 获取正股代码 -> getUnderlyingCode


# 获取正股简称时间序列 -> getUnderlyingNameSeries


# 获取正股简称 -> getUnderlyingName


# 获取相对转股期时间序列 -> getClauseConversion2RelativeSwapShareMonthSeries


# 获取相对转股期 -> getClauseConversion2RelativeSwapShareMonth


# 获取自愿转股起始日期时间序列 -> getClauseConversion2SwapShareStartDateSeries


# 获取自愿转股起始日期 -> getClauseConversion2SwapShareStartDate


# 获取自愿转股终止日期时间序列 -> getClauseConversion2SwapShareEnddateSeries


# 获取自愿转股终止日期 -> getClauseConversion2SwapShareEnddate


# 获取是否强制转股时间序列 -> getClauseConversion2IsForcedSeries


# 获取是否强制转股 -> getClauseConversion2IsForced


# 获取强制转股日时间序列 -> getClauseConversion2ForceConvertDateSeries


# 获取强制转股日 -> getClauseConversion2ForceConvertDate


# 获取强制转股价格时间序列 -> getClauseConversion2ForceConvertPriceSeries


# 获取强制转股价格 -> getClauseConversion2ForceConvertPrice


# 获取转股价格时间序列 -> getClauseConversion2SwapSharePriceSeries


# 获取转股价格 -> getClauseConversion2SwapSharePrice


# 获取转股代码时间序列 -> getClauseConversionCodeSeries


# 获取转股代码 -> getClauseConversionCode


# 获取转换比例时间序列 -> getClauseConversion2ConversionProportionSeries


# 获取转换比例 -> getClauseConversion2ConversionProportion


# 获取未转股余额时间序列 -> getClauseConversion2BondLotSeries


# 获取未转股余额 -> getClauseConversion2BondLot


# 获取未转股比例时间序列 -> getClauseConversion2BondProportionSeries


# 获取未转股比例 -> getClauseConversion2BondProportion


# 获取特别向下修正条款全文时间序列 -> getClauseResetItemSeries


# 获取特别向下修正条款全文 -> getClauseResetItem


# 获取是否有特别向下修正条款时间序列 -> getClauseResetIsExitResetSeries


# 获取是否有特别向下修正条款 -> getClauseResetIsExitReset


# 获取特别修正起始时间时间序列 -> getClauseResetResetStartDateSeries


# 获取特别修正起始时间 -> getClauseResetResetStartDate


# 获取特别修正结束时间时间序列 -> getClauseResetResetPeriodEnddateSeries


# 获取特别修正结束时间 -> getClauseResetResetPeriodEnddate


# 获取重设触发计算最大时间区间时间序列 -> getClauseResetResetMaxTimespanSeries


# 获取重设触发计算最大时间区间 -> getClauseResetResetMaxTimespan


# 获取重设触发计算时间区间时间序列 -> getClauseResetResetTimespanSeries


# 获取重设触发计算时间区间 -> getClauseResetResetTimespan


# 获取触发比例时间序列 -> getClauseResetResetTriggerRatioSeries


# 获取触发比例 -> getClauseResetResetTriggerRatio


# 获取赎回触发比例时间序列 -> getClauseCallOptionTriggerProportionSeries


# 获取赎回触发比例 -> getClauseCallOptionTriggerProportion


# 获取回售触发比例时间序列 -> getClausePutOptionRedeemTriggerProportionSeries


# 获取回售触发比例 -> getClausePutOptionRedeemTriggerProportion


# 获取特别修正幅度时间序列 -> getClauseResetResetRangeSeries


# 获取特别修正幅度 -> getClauseResetResetRange


# 获取修正价格底线说明时间序列 -> getClauseResetStockPriceLowestLimitSeries


# 获取修正价格底线说明 -> getClauseResetStockPriceLowestLimit


# 获取修正次数限制时间序列 -> getClauseResetResetTimesLimitSeries


# 获取修正次数限制 -> getClauseResetResetTimesLimit


# 获取时点修正条款全文时间序列 -> getClauseResetTimePointClauseSeries


# 获取时点修正条款全文 -> getClauseResetTimePointClause


# 获取相对赎回期时间序列 -> getClauseCallOptionRelativeCallOptionPeriodSeries


# 获取相对赎回期 -> getClauseCallOptionRelativeCallOptionPeriod


# 获取每年可赎回次数时间序列 -> getClauseCallOptionRedemptionTimesPerYearSeries


# 获取每年可赎回次数 -> getClauseCallOptionRedemptionTimesPerYear


# 获取条件赎回起始日期时间序列 -> getClauseCallOptionConditionalRedeemStartDateSeries


# 获取条件赎回起始日期 -> getClauseCallOptionConditionalRedeemStartDate


# 获取条件赎回截止日期时间序列 -> getClauseCallOptionConditionalRedeemEnddateSeries


# 获取条件赎回截止日期 -> getClauseCallOptionConditionalRedeemEnddate


# 获取赎回触发计算最大时间区间时间序列 -> getClauseCallOptionRedeemMaxSpanSeries


# 获取赎回触发计算最大时间区间 -> getClauseCallOptionRedeemMaxSpan


# 获取赎回触发计算时间区间时间序列 -> getClauseCallOptionRedeemSpanSeries


# 获取赎回触发计算时间区间 -> getClauseCallOptionRedeemSpan


# 获取利息处理时间序列 -> getClausePutOptionInterestDisposingSeries


# 获取利息处理 -> getClausePutOptionInterestDisposing


# 获取时点赎回数时间序列 -> getClauseCallOptionTimeRedemptionTimesSeries


# 获取时点赎回数 -> getClauseCallOptionTimeRedemptionTimes


# 获取有条件赎回价时间序列 -> getConditionalCallPriceSeries


# 获取有条件赎回价 -> getConditionalCallPrice


# 获取到期赎回价时间序列 -> getMaturityCallPriceSeries


# 获取到期赎回价 -> getMaturityCallPrice


# 获取赎回触发价时间序列 -> getClauseCallOptionTriggerPriceSeries


# 获取赎回触发价 -> getClauseCallOptionTriggerPrice


# 获取赎回公告日时间序列 -> getClauseCallOptionNoticeDateSeries


# 获取赎回公告日 -> getClauseCallOptionNoticeDate


# 获取相对回售期时间序列 -> getClausePutOptionPutBackPeriodObSSeries


# 获取相对回售期 -> getClausePutOptionPutBackPeriodObS


# 获取条件回售起始日期时间序列 -> getClausePutOptionConditionalPutBackStartEnddateSeries


# 获取条件回售起始日期 -> getClausePutOptionConditionalPutBackStartEnddate


# 获取无条件回售起始日期时间序列 -> getClausePutOptionPutBackStartDateSeries


# 获取无条件回售起始日期 -> getClausePutOptionPutBackStartDate


# 获取条件回售截止日期时间序列 -> getClausePutOptionConditionalPutBackEnddateSeries


# 获取条件回售截止日期 -> getClausePutOptionConditionalPutBackEnddate


# 获取回售触发计算最大时间区间时间序列 -> getClausePutOptionPutBackTriggerMaxSpanSeries


# 获取回售触发计算最大时间区间 -> getClausePutOptionPutBackTriggerMaxSpan


# 获取回售触发计算时间区间时间序列 -> getClausePutOptionPutBackTriggerSpanSeries


# 获取回售触发计算时间区间 -> getClausePutOptionPutBackTriggerSpan


# 获取每年回售次数时间序列 -> getClausePutOptionPutBackTimesPerYearSeries


# 获取每年回售次数 -> getClausePutOptionPutBackTimesPerYear


# 获取无条件回售期时间序列 -> getClausePutOptionPutBackPeriodSeries


# 获取无条件回售期 -> getClausePutOptionPutBackPeriod


# 获取无条件回售结束日期时间序列 -> getClausePutOptionPutBackEnddateSeries


# 获取无条件回售结束日期 -> getClausePutOptionPutBackEnddate


# 获取无条件回售价时间序列 -> getClausePutOptionPutBackPriceSeries


# 获取无条件回售价 -> getClausePutOptionPutBackPrice


# 获取时点回售数时间序列 -> getClausePutOptionTimePutBackTimesSeries


# 获取时点回售数 -> getClausePutOptionTimePutBackTimes


# 获取附加回售条件时间序列 -> getClausePutOptionPutBackAdditionalConditionSeries


# 获取附加回售条件 -> getClausePutOptionPutBackAdditionalCondition


# 获取有条件回售价时间序列 -> getConditionalPutPriceSeries


# 获取有条件回售价 -> getConditionalPutPrice


# 获取回售触发价时间序列 -> getClausePutOptionTriggerPriceSeries


# 获取回售触发价 -> getClausePutOptionTriggerPrice


# 获取回售公告日时间序列 -> getClausePutOptionNoticeDateSeries


# 获取回售公告日 -> getClausePutOptionNoticeDate


# 获取发行时债项评级时间序列 -> getCreditRatingSeries


# 获取发行时债项评级 -> getCreditRating


# 获取发行时主体评级时间序列 -> getIssuerRatingSeries


# 获取发行时主体评级 -> getIssuerRating


# 获取发行时主体评级展望时间序列 -> getIssuerRatingOutlookSeries


# 获取发行时主体评级展望 -> getIssuerRatingOutlook


# 获取发行人委托评级机构时间序列 -> getRateCreditRatingAgencySeries


# 获取发行人委托评级机构 -> getRateCreditRatingAgency


# 获取发债主体评级机构时间序列 -> getIsSurerCreditRatingCompanySeries


# 获取发债主体评级机构 -> getIsSurerCreditRatingCompany


# 获取最新债项评级时间序列 -> getAmountSeries


# 获取最新债项评级 -> getAmount


# 获取最新债项评级日期时间序列 -> getRateLatestSeries


# 获取最新债项评级日期 -> getRateLatest


# 获取最新债项评级日期(指定机构)时间序列 -> getRateLatest1Series


# 获取最新债项评级日期(指定机构) -> getRateLatest1


# 获取最新债项评级变动方向时间序列 -> getRateChangesOfRatingSeries


# 获取最新债项评级变动方向 -> getRateChangesOfRating


# 获取最新债项评级评级类型时间序列 -> getRateStyleSeries


# 获取最新债项评级评级类型 -> getRateStyle


# 获取发行人最新最低评级时间序列 -> getLowestIsSurerCreditRatingSeries


# 获取发行人最新最低评级 -> getLowestIsSurerCreditRating


# 获取债项评级时间序列 -> getRateRateBondSeries


# 获取债项评级 -> getRateRateBond


# 获取债项评级变动方向时间序列 -> getRateChNgBondSeries


# 获取债项评级变动方向 -> getRateChNgBond


# 获取债项评级机构时间序列 -> getRateAgencyBondSeries


# 获取债项评级机构 -> getRateAgencyBond


# 获取历史债项评级时间序列 -> getRateFormerSeries


# 获取历史债项评级 -> getRateFormer


# 获取(废弃)债项评级(YY)时间序列 -> getInStYyBondRatingSeries


# 获取(废弃)债项评级(YY) -> getInStYyBondRating


# 获取主体评级时间序列 -> getLatestIsSurerCreditRating2Series


# 获取主体评级 -> getLatestIsSurerCreditRating2


# 获取主体评级展望时间序列 -> getRateFwdIssuerSeries


# 获取主体评级展望 -> getRateFwdIssuer


# 获取主体评级变动方向时间序列 -> getRateChNgIssuerSeries


# 获取主体评级变动方向 -> getRateChNgIssuer


# 获取主体评级评级机构时间序列 -> getRateAgencyIssuerSeries


# 获取主体评级评级机构 -> getRateAgencyIssuer


# 获取主体评级(YY)时间序列 -> getInStYyIssuerRatingSeries


# 获取主体评级(YY) -> getInStYyIssuerRating


# 获取主体评级历史(YY)时间序列 -> getInStYyIssuerRatingHisSeries


# 获取主体评级历史(YY) -> getInStYyIssuerRatingHis


# 获取指定日主体评级时间序列 -> getRateIssuerSeries


# 获取指定日主体评级 -> getRateIssuer


# 获取发债主体历史信用等级时间序列 -> getRateIssuerFormerSeries


# 获取发债主体历史信用等级 -> getRateIssuerFormer


# 获取最新授信额度时间序列 -> getCreditLineSeries


# 获取最新授信额度 -> getCreditLine


# 获取最新已使用授信额度时间序列 -> getCreditLineUsedSeries


# 获取最新已使用授信额度 -> getCreditLineUsed


# 获取最新未使用授信额度时间序列 -> getCreditLineUnusedSeries


# 获取最新未使用授信额度 -> getCreditLineUnused


# 获取历史已使用授信额度时间序列 -> getCreditLineUsed2Series


# 获取历史已使用授信额度 -> getCreditLineUsed2


# 获取历史授信额度时间序列 -> getCreditFormerLineSeries


# 获取历史授信额度 -> getCreditFormerLine


# 获取最新授信日期时间序列 -> getCreditLineDateSeries


# 获取最新授信日期 -> getCreditLineDate


# 获取最新担保余额时间序列 -> getGuarLatestBalanceSeries


# 获取最新担保余额 -> getGuarLatestBalance


# 获取最新对内担保余额时间序列 -> getGuarLatestInwardsSeries


# 获取最新对内担保余额 -> getGuarLatestInwards


# 获取最新对外担保余额时间序列 -> getGuarLatestOutwardsSeries


# 获取最新对外担保余额 -> getGuarLatestOutwards


# 获取历史担保余额时间序列 -> getGuarFormerBalanceSeries


# 获取历史担保余额 -> getGuarFormerBalance


# 获取对内担保余额时间序列 -> getGuarFormerInwardsSeries


# 获取对内担保余额 -> getGuarFormerInwards


# 获取对外担保余额时间序列 -> getGuarFormerOutwardsSeries


# 获取对外担保余额 -> getGuarFormerOutwards


# 获取实际可用剩余额度时间序列 -> getDCmUnuEsDAmountSeries


# 获取实际可用剩余额度 -> getDCmUnuEsDAmount


# 获取已使用注册额度时间序列 -> getDCmUeSdAmountSeries


# 获取已使用注册额度 -> getDCmUeSdAmount


# 获取首期发行截止日时间序列 -> getDCmFirstIssueEnddateSeries


# 获取首期发行截止日 -> getDCmFirstIssueEnddate


# 获取未使用注册会议日期时间序列 -> getDCmMeetingDataSeries


# 获取未使用注册会议日期 -> getDCmMeetingData


# 获取未使用额度有效期时间序列 -> getDCmExpirationDataSeries


# 获取未使用额度有效期 -> getDCmExpirationData


# 获取最新注册文件编号时间序列 -> getDCmNumberSeries


# 获取最新注册文件编号 -> getDCmNumber


# 获取未使用额度主承销商时间序列 -> getDCmUnderwriterSeries


# 获取未使用额度主承销商 -> getDCmUnderwriter


# 获取历史累计注册额度时间序列 -> getDCmAcCumAmountSeries


# 获取历史累计注册额度 -> getDCmAcCumAmount


# 获取区间发行债券总额时间序列 -> getFinaTotalAmount2Series


# 获取区间发行债券总额 -> getFinaTotalAmount2


# 获取区间发行债券数目时间序列 -> getFinaTotalNumberSeries


# 获取区间发行债券数目 -> getFinaTotalNumber


# 获取存量债券数目时间序列 -> getFinaRemainingNumberSeries


# 获取存量债券数目 -> getFinaRemainingNumber


# 获取基金简称时间序列 -> getFundInfoNameSeries


# 获取基金简称 -> getFundInfoName


# 获取基金简称(官方)时间序列 -> getNameOfficialSeries


# 获取基金简称(官方) -> getNameOfficial


# 获取基金全称时间序列 -> getFundFullNameSeries


# 获取基金全称 -> getFundFullName


# 获取基金全称(英文)时间序列 -> getFundFullNameEnSeries


# 获取基金全称(英文) -> getFundFullNameEn


# 获取基金场内简称时间序列 -> getFundExchangeShortnameSeries


# 获取基金场内简称 -> getFundExchangeShortname


# 获取基金扩位场内简称时间序列 -> getFundExchangeShortnameExtendSeries


# 获取基金扩位场内简称 -> getFundExchangeShortnameExtend


# 获取发行机构自编简称时间序列 -> getFundIssuerShortnameSeries


# 获取发行机构自编简称 -> getFundIssuerShortname


# 获取成立年限时间序列 -> getFundExistingYearSeries


# 获取成立年限 -> getFundExistingYear


# 获取基金最短持有期时间序列 -> getFundMinHoldingPeriodSeries


# 获取基金最短持有期 -> getFundMinHoldingPeriod


# 获取基金存续期时间序列 -> getFundPtMYearSeries


# 获取基金存续期 -> getFundPtMYear


# 获取剩余存续期时间序列 -> getFundPtMDaySeries


# 获取剩余存续期 -> getFundPtMDay


# 获取业绩比较基准时间序列 -> getFundBenchmarkSeries


# 获取业绩比较基准 -> getFundBenchmark


# 获取业绩比较基准变更说明时间序列 -> getFundChangeOfBenchmarkSeries


# 获取业绩比较基准变更说明 -> getFundChangeOfBenchmark


# 获取业绩比较基准增长率时间序列 -> getBenchReturnSeries


# 获取业绩比较基准增长率 -> getBenchReturn


# 获取报告期业绩比较基准增长率时间序列 -> getNavBenchReturnSeries


# 获取报告期业绩比较基准增长率 -> getNavBenchReturn


# 获取报告期业绩比较基准增长率标准差时间序列 -> getNavBenchStdDevSeries


# 获取报告期业绩比较基准增长率标准差 -> getNavBenchStdDev


# 获取单季度.业绩比较基准收益率时间序列 -> getQAnalBenchReturnSeries


# 获取单季度.业绩比较基准收益率 -> getQAnalBenchReturn


# 获取单季度.业绩比较基准收益率标准差时间序列 -> getQAnalStdBenchReturnSeries


# 获取单季度.业绩比较基准收益率标准差 -> getQAnalStdBenchReturn


# 获取基准指数代码时间序列 -> getFundBenchIndexCodeSeries


# 获取基准指数代码 -> getFundBenchIndexCode


# 获取投资目标时间序列 -> getFundInvestObjectSeries


# 获取投资目标 -> getFundInvestObject


# 获取投资范围时间序列 -> getFundInvestScopeSeries


# 获取投资范围 -> getFundInvestScope


# 获取投资品种比例限制时间序列 -> getFundInvestmentProportionSeries


# 获取投资品种比例限制 -> getFundInvestmentProportion


# 获取港股通股票投资比例说明时间序列 -> getFundHkScInvestmentProportionSeries


# 获取港股通股票投资比例说明 -> getFundHkScInvestmentProportion


# 获取投资理念时间序列 -> getFundInvestConceptionSeries


# 获取投资理念 -> getFundInvestConception


# 获取投资区域时间序列 -> getFundInvestmentRegionSeries


# 获取投资区域 -> getFundInvestmentRegion


# 获取主要投资区域说明时间序列 -> getFundInvestingRegionDescriptionSeries


# 获取主要投资区域说明 -> getFundInvestingRegionDescription


# 获取面值时间序列 -> getFundParValueSeries


# 获取面值 -> getFundParValue


# 获取是否初始基金时间序列 -> getFundInitialSeries


# 获取是否初始基金 -> getFundInitial


# 获取是否分级基金时间序列 -> getFundStructuredFundOrNotSeries


# 获取是否分级基金 -> getFundStructuredFundOrNot


# 获取是否定期开放基金时间序列 -> getFundReGulOpenFundOrNotSeries


# 获取是否定期开放基金 -> getFundReGulOpenFundOrNot


# 获取是否使用侧袋机制时间序列 -> getFundSidePocketFundOrNotSeries


# 获取是否使用侧袋机制 -> getFundSidePocketFundOrNot


# 获取产品异常状态时间序列 -> getFundExceptionStatusSeries


# 获取产品异常状态 -> getFundExceptionStatus


# 获取封闭运作期时间序列 -> getFundOperatePeriodClsSeries


# 获取封闭运作期 -> getFundOperatePeriodCls


# 获取预期收益率(文字)时间序列 -> getExpectedYieldSeries


# 获取预期收益率(文字) -> getExpectedYield


# 获取基金转型说明时间序列 -> getFundFundTransitionSeries


# 获取基金转型说明 -> getFundFundTransition


# 获取基金估值方法时间序列 -> getFundValuationMethodSeries


# 获取基金估值方法 -> getFundValuationMethod


# 获取风险收益特征时间序列 -> getFundRiskReturnCharactersSeries


# 获取风险收益特征 -> getFundRiskReturnCharacters


# 获取市场风险提示时间序列 -> getMarketRiskSeries


# 获取市场风险提示 -> getMarketRisk


# 获取管理风险提示时间序列 -> getManagementRiskSeries


# 获取管理风险提示 -> getManagementRisk


# 获取技术风险提示时间序列 -> getTechnicalRiskSeries


# 获取技术风险提示 -> getTechnicalRisk


# 获取赎回风险提示时间序列 -> getRedemptionRiskSeries


# 获取赎回风险提示 -> getRedemptionRisk


# 获取其他风险提示时间序列 -> getOtherRisksSeries


# 获取其他风险提示 -> getOtherRisks


# 获取基金前端代码时间序列 -> getFundFrontendCodeSeries


# 获取基金前端代码 -> getFundFrontendCode


# 获取基金后端代码时间序列 -> getFundBackendCodeSeries


# 获取基金后端代码 -> getFundBackendCode


# 获取基金初始代码时间序列 -> getFundInitialCodeSeries


# 获取基金初始代码 -> getFundInitialCode


# 获取关联基金代码时间序列 -> getFundRelatedCodeSeries


# 获取关联基金代码 -> getFundRelatedCode


# 获取基金业协会编码时间序列 -> getFundAMacCodeSeries


# 获取基金业协会编码 -> getFundAMacCode


# 获取理财产品登记编码时间序列 -> getFundBWMpRecordCodeSeries


# 获取理财产品登记编码 -> getFundBWMpRecordCode


# 获取发行机构自编代码时间序列 -> getFundIssuerCodeSeries


# 获取发行机构自编代码 -> getFundIssuerCode


# 获取理财产品交易所代码时间序列 -> getFundExchangeCodeSeries


# 获取理财产品交易所代码 -> getFundExchangeCode


# 获取机构间私募产品报价系统编码时间序列 -> getFundPeQuotationCodeSeries


# 获取机构间私募产品报价系统编码 -> getFundPeQuotationCode


# 获取基金成立日时间序列 -> getFundSetUpdateSeries


# 获取基金成立日 -> getFundSetUpdate


# 获取基金到期日时间序列 -> getFundMaturityDate2Series


# 获取基金到期日 -> getFundMaturityDate2


# 获取基金暂停运作日时间序列 -> getFundDateSuspensionSeries


# 获取基金暂停运作日 -> getFundDateSuspension


# 获取基金恢复运作日时间序列 -> getFundDateResumptionSeries


# 获取基金恢复运作日 -> getFundDateResumption


# 获取开始托管日期时间序列 -> getFundCuStStartDateSeries


# 获取开始托管日期 -> getFundCuStStartDate


# 获取托管结束日期时间序列 -> getFundCusTendDateSeries


# 获取托管结束日期 -> getFundCusTendDate


# 获取互认基金批复日期时间序列 -> getFundRecognitionDateSeries


# 获取互认基金批复日期 -> getFundRecognitionDate


# 获取预计封闭期结束日时间序列 -> getFundExpectedEndingDaySeries


# 获取预计封闭期结束日 -> getFundExpectedEndingDay


# 获取预计下期开放日时间序列 -> getFundExpectedOpenDaySeries


# 获取预计下期开放日 -> getFundExpectedOpenDay


# 获取定开基金封闭起始日时间序列 -> getFundStartDateOfClosureSeries


# 获取定开基金封闭起始日 -> getFundStartDateOfClosure


# 获取定开基金上一开放日时间序列 -> getFundLastOpenDaySeries


# 获取定开基金上一开放日 -> getFundLastOpenDay


# 获取定开基金开放日(支持历史)时间序列 -> getFundOpenDaysSeries


# 获取定开基金开放日(支持历史) -> getFundOpenDays


# 获取定开基金已开放次数时间序列 -> getFundNumOfOpenDaysSeries


# 获取定开基金已开放次数 -> getFundNumOfOpenDays


# 获取上市公告数据截止日期时间序列 -> getListDataDateSeries


# 获取上市公告数据截止日期 -> getListDataDate


# 获取基金管理人时间序列 -> getFundMGrCompSeries


# 获取基金管理人 -> getFundMGrComp


# 获取基金管理人简称时间序列 -> getFundCorpFundManagementCompanySeries


# 获取基金管理人简称 -> getFundCorpFundManagementCompany


# 获取基金管理人英文名称时间序列 -> getFundCorpNameEngSeries


# 获取基金管理人英文名称 -> getFundCorpNameEng


# 获取基金管理人法人代表时间序列 -> getFundCorpChairmanSeries


# 获取基金管理人法人代表 -> getFundCorpChairman


# 获取基金管理人电话时间序列 -> getFundCorpPhoneSeries


# 获取基金管理人电话 -> getFundCorpPhone


# 获取基金管理人传真时间序列 -> getFundCorpFaxSeries


# 获取基金管理人传真 -> getFundCorpFax


# 获取基金管理人电子邮箱时间序列 -> getFundCorpEmailSeries


# 获取基金管理人电子邮箱 -> getFundCorpEmail


# 获取基金管理人主页时间序列 -> getFundCorpWebsiteSeries


# 获取基金管理人主页 -> getFundCorpWebsite


# 获取基金管理人资产净值合计(非货币)时间序列 -> getPrtNonMoneyNetAssetsSeries


# 获取基金管理人资产净值合计(非货币) -> getPrtNonMoneyNetAssets


# 获取基金管理人资产净值合计时间序列 -> getPrtFundCoTotalNetAssetsSeries


# 获取基金管理人资产净值合计 -> getPrtFundCoTotalNetAssets


# 获取基金管理人资产净值合计排名时间序列 -> getPrtFundCoTotalNetAssetsRankingSeries


# 获取基金管理人资产净值合计排名 -> getPrtFundCoTotalNetAssetsRanking


# 获取基金管理人资产净值合计变动率时间序列 -> getPrtFundCoTnaChangeRatioSeries


# 获取基金管理人资产净值合计变动率 -> getPrtFundCoTnaChangeRatio


# 获取基金托管人时间序列 -> getFundCustodianBankSeries


# 获取基金托管人 -> getFundCustodianBank


# 获取基金注册与过户登记人时间序列 -> getIssueRegistrarSeries


# 获取基金注册与过户登记人 -> getIssueRegistrar


# 获取财务顾问时间序列 -> getAgencyFAdvisorSeries


# 获取财务顾问 -> getAgencyFAdvisor


# 获取手续费及佣金收入:财务顾问业务时间序列 -> getStmNoteSec1504Series


# 获取手续费及佣金收入:财务顾问业务 -> getStmNoteSec1504


# 获取手续费及佣金净收入:财务顾问业务时间序列 -> getStmNoteSec1524Series


# 获取手续费及佣金净收入:财务顾问业务 -> getStmNoteSec1524


# 获取银行理财发行人时间序列 -> getFundWmIssuerSeries


# 获取银行理财发行人 -> getFundWmIssuer


# 获取境外投资顾问时间序列 -> getFundForeignInvestmentAdvisorSeries


# 获取境外投资顾问 -> getFundForeignInvestmentAdvisor


# 获取境外托管人时间序列 -> getFundForeignCustodianSeries


# 获取境外托管人 -> getFundForeignCustodian


# 获取律师事务所时间序列 -> getFundCounselorSeries


# 获取律师事务所 -> getFundCounselor


# 获取一级交易商时间序列 -> getFundPrimaryDealersSeries


# 获取一级交易商 -> getFundPrimaryDealers


# 获取基金类型时间序列 -> getFundTypeSeries


# 获取基金类型 -> getFundType


# 获取投资类型(一级分类)时间序列 -> getFundFirstInvestTypeSeries


# 获取投资类型(一级分类) -> getFundFirstInvestType


# 获取投资类型(二级分类)时间序列 -> getFundInvestTypeSeries


# 获取投资类型(二级分类) -> getFundInvestType


# 获取投资类型时间序列 -> getFundInvestType2Series


# 获取投资类型 -> getFundInvestType2


# 获取投资类型(支持历史)时间序列 -> getFundInvestTypeAnytimeSeries


# 获取投资类型(支持历史) -> getFundInvestTypeAnytime


# 获取投资类型(英文)时间序列 -> getFundInvestTypeEngSeries


# 获取投资类型(英文) -> getFundInvestTypeEng


# 获取基金风险等级时间序列 -> getFundRiskLevelSeries


# 获取基金风险等级 -> getFundRiskLevel


# 获取基金风险等级(公告口径)时间序列 -> getFundRiskLevelFilingSeries


# 获取基金风险等级(公告口径) -> getFundRiskLevelFiling


# 获取基金分级类型时间序列 -> getFundSMfType2Series


# 获取基金分级类型 -> getFundSMfType2


# 获取同类基金数量时间序列 -> getFundSimilarFundNoSeries


# 获取同类基金数量 -> getFundSimilarFundNo


# 获取所属主题基金类别时间序列 -> getFundThemeTypeSeries


# 获取所属主题基金类别 -> getFundThemeType


# 获取所属主题基金类别(Wind概念)时间序列 -> getFundThemeTypeConceptSeries


# 获取所属主题基金类别(Wind概念) -> getFundThemeTypeConcept


# 获取所属主题基金类别(Wind行业)时间序列 -> getFundThemeTypeIndustrySeries


# 获取所属主题基金类别(Wind行业) -> getFundThemeTypeIndustry


# 获取所属主题基金类别(Wind股票指数)时间序列 -> getFundThemeTypeIndexSeries


# 获取所属主题基金类别(Wind股票指数) -> getFundThemeTypeIndex


# 获取管理费率时间序列 -> getFundManagementFeeRatioSeries


# 获取管理费率 -> getFundManagementFeeRatio


# 获取管理费率(支持历史)时间序列 -> getFundManagementFeeRatio2Series


# 获取管理费率(支持历史) -> getFundManagementFeeRatio2


# 获取浮动管理费率说明时间序列 -> getFundFloatingMgNtFeedEScripSeries


# 获取浮动管理费率说明 -> getFundFloatingMgNtFeedEScrip


# 获取受托人固定管理费率(信托)时间序列 -> getFundTrusteeMgNtFeeSeries


# 获取受托人固定管理费率(信托) -> getFundTrusteeMgNtFee


# 获取投资顾问固定管理费率(信托)时间序列 -> getFundInvAdviserMgNtFeeSeries


# 获取投资顾问固定管理费率(信托) -> getFundInvAdviserMgNtFee


# 获取是否收取浮动管理费时间序列 -> getFundFloatingMgNtFeeOrNotSeries


# 获取是否收取浮动管理费 -> getFundFloatingMgNtFeeOrNot


# 获取托管费率时间序列 -> getFundCustodianFeeRatioSeries


# 获取托管费率 -> getFundCustodianFeeRatio


# 获取托管费率(支持历史)时间序列 -> getFundCustodianFeeRatio2Series


# 获取托管费率(支持历史) -> getFundCustodianFeeRatio2


# 获取销售服务费率时间序列 -> getFundSaleFeeRatioSeries


# 获取销售服务费率 -> getFundSaleFeeRatio


# 获取销售服务费率(支持历史)时间序列 -> getFundSaleFeeRatio2Series


# 获取销售服务费率(支持历史) -> getFundSaleFeeRatio2


# 获取最高申购费率时间序列 -> getFundPurchaseFeeRatioSeries


# 获取最高申购费率 -> getFundPurchaseFeeRatio


# 获取最高赎回费率时间序列 -> getFundRedemptionFeeRatioSeries


# 获取最高赎回费率 -> getFundRedemptionFeeRatio


# 获取认购费率时间序列 -> getFundSubscriptionFeeSeries


# 获取认购费率 -> getFundSubscriptionFee


# 获取认购费率(支持历史)时间序列 -> getFundSubscriptionFee2Series


# 获取认购费率(支持历史) -> getFundSubscriptionFee2


# 获取申购费率时间序列 -> getFundPurchaseFeeSeries


# 获取申购费率 -> getFundPurchaseFee


# 获取申购费率(支持历史)时间序列 -> getFundPurchaseFee2Series


# 获取申购费率(支持历史) -> getFundPurchaseFee2


# 获取申购费率上限时间序列 -> getFundPChRedMPChMaxFeeSeries


# 获取申购费率上限 -> getFundPChRedMPChMaxFee


# 获取赎回费率时间序列 -> getFundRedemptionFeeSeries


# 获取赎回费率 -> getFundRedemptionFee


# 获取赎回费率(支持历史)时间序列 -> getFundRedemptionFee2Series


# 获取赎回费率(支持历史) -> getFundRedemptionFee2


# 获取赎回费率上限时间序列 -> getFundPChRedMMaxRedMFeeSeries


# 获取赎回费率上限 -> getFundPChRedMMaxRedMFee


# 获取指数使用费率时间序列 -> getFundIndexUsageFeeRatioSeries


# 获取指数使用费率 -> getFundIndexUsageFeeRatio


# 获取申购赎回简称时间序列 -> getFundPurchaseAndRedemptionAbbreviationSeries


# 获取申购赎回简称 -> getFundPurchaseAndRedemptionAbbreviation


# 获取申购赎回状态时间序列 -> getFundDQStatusSeries


# 获取申购赎回状态 -> getFundDQStatus


# 获取申购状态时间序列 -> getFundPcHmStatusSeries


# 获取申购状态 -> getFundPcHmStatus


# 获取赎回状态时间序列 -> getFundRedMStatusSeries


# 获取赎回状态 -> getFundRedMStatus


# 获取申购起始日时间序列 -> getFundPChRedMPChStartDateSeries


# 获取申购起始日 -> getFundPChRedMPChStartDate


# 获取网下申购起始日期时间序列 -> getIpoOpStartDateSeries


# 获取网下申购起始日期 -> getIpoOpStartDate


# 获取单日大额申购限额时间序列 -> getFundPChRedMLargePChMaxAmtSeries


# 获取单日大额申购限额 -> getFundPChRedMLargePChMaxAmt


# 获取申购金额下限(场外)时间序列 -> getFundPChRedMPcHmInAmtSeries


# 获取申购金额下限(场外) -> getFundPChRedMPcHmInAmt


# 获取申购金额下限(场内)时间序列 -> getFundPChRedMPcHmInAmtFloorSeries


# 获取申购金额下限(场内) -> getFundPChRedMPcHmInAmtFloor


# 获取赎回起始日时间序列 -> getFundRedMStartDateSeries


# 获取赎回起始日 -> getFundRedMStartDate


# 获取单笔赎回份额下限时间序列 -> getFundPChRedMRedMmInAmtSeries


# 获取单笔赎回份额下限 -> getFundPChRedMRedMmInAmt


# 获取申购确认日时间序列 -> getFundPChConfirmDateSeries


# 获取申购确认日 -> getFundPChConfirmDate


# 获取赎回确认日时间序列 -> getFundRedMConfirmDateSeries


# 获取赎回确认日 -> getFundRedMConfirmDate


# 获取赎回划款日时间序列 -> getFundRedMarriAlDateSeries


# 获取赎回划款日 -> getFundRedMarriAlDate


# 获取旗下基金数时间序列 -> getFundCorpFundNoSeries


# 获取旗下基金数 -> getFundCorpFundNo


# 获取五星基金占比时间序列 -> getFundCorpFiveStarFundsPropSeries


# 获取五星基金占比 -> getFundCorpFiveStarFundsProp


# 获取四星基金占比时间序列 -> getFundCorpFourStarFundsPropSeries


# 获取四星基金占比 -> getFundCorpFourStarFundsProp


# 获取团队稳定性时间序列 -> getFundCorpTeamStabilitySeries


# 获取团队稳定性 -> getFundCorpTeamStability


# 获取跟踪指数代码时间序列 -> getFundTrackIndexCodeSeries


# 获取跟踪指数代码 -> getFundTrackIndexCode


# 获取跟踪指数名称时间序列 -> getFundTrackIndexNameSeries


# 获取跟踪指数名称 -> getFundTrackIndexName


# 获取日均跟踪偏离度阈值(业绩基准)时间序列 -> getFundTrackDeviationThresholdSeries


# 获取日均跟踪偏离度阈值(业绩基准) -> getFundTrackDeviationThreshold


# 获取年化跟踪误差阈值(业绩基准)时间序列 -> getFundTrackErrorThresholdSeries


# 获取年化跟踪误差阈值(业绩基准) -> getFundTrackErrorThreshold


# 获取分级基金类别时间序列 -> getFundSMfTypeSeries


# 获取分级基金类别 -> getFundSMfType


# 获取分级基金母基金代码时间序列 -> getFundSMfCodeSeries


# 获取分级基金母基金代码 -> getFundSMfCode


# 获取分级基金优先级代码时间序列 -> getFundSMfaCodeSeries


# 获取分级基金优先级代码 -> getFundSMfaCode


# 获取分级基金普通级代码时间序列 -> getFundSmFbCodeSeries


# 获取分级基金普通级代码 -> getFundSmFbCode


# 获取拆分比率时间序列 -> getFundSplitRatioSeries


# 获取拆分比率 -> getFundSplitRatio


# 获取分级份额占比时间序列 -> getFundSubShareProportionSeries


# 获取分级份额占比 -> getFundSubShareProportion


# 获取初始杠杆时间序列 -> getFundInitialLeverSeries


# 获取初始杠杆 -> getFundInitialLever


# 获取约定年收益率表达式时间序列 -> getFundAAyeIlDInfoSeries


# 获取约定年收益率表达式 -> getFundAAyeIlDInfo


# 获取是否配对转换时间序列 -> getFundPairConversionSeries


# 获取是否配对转换 -> getFundPairConversion


# 获取定期折算周期时间序列 -> getFundDiscountPeriodSeries


# 获取定期折算周期 -> getFundDiscountPeriod


# 获取定期折算条款时间序列 -> getFundDiscountMethodSeries


# 获取定期折算条款 -> getFundDiscountMethod


# 获取向上触点折算条款时间序列 -> getFundUpDiscountSeries


# 获取向上触点折算条款 -> getFundUpDiscount


# 获取向下触点折算条款时间序列 -> getFundDownDiscountSeries


# 获取向下触点折算条款 -> getFundDownDiscount


# 获取保本周期时间序列 -> getFundGuaranteedCycleSeries


# 获取保本周期 -> getFundGuaranteedCycle


# 获取保本周期起始日期时间序列 -> getFundGuaranteedCycleStartDateSeries


# 获取保本周期起始日期 -> getFundGuaranteedCycleStartDate


# 获取保本周期终止日期时间序列 -> getFundGuaranteedCycleEnddateSeries


# 获取保本周期终止日期 -> getFundGuaranteedCycleEnddate


# 获取保本费率时间序列 -> getFundGuaranteedFeeRateSeries


# 获取保本费率 -> getFundGuaranteedFeeRate


# 获取保证人时间序列 -> getFundWarrantOrSeries


# 获取保证人 -> getFundWarrantOr


# 获取保证人简介时间序列 -> getFundWarrantOrIntroductionSeries


# 获取保证人简介 -> getFundWarrantOrIntroduction


# 获取保本触发收益率时间序列 -> getFundGuaranteedTriggerRatioSeries


# 获取保本触发收益率 -> getFundGuaranteedTriggerRatio


# 获取保本触发机制说明时间序列 -> getFundGuaranteedTriggerTxtSeries


# 获取保本触发机制说明 -> getFundGuaranteedTriggerTxt


# 获取计划类型(券商集合理财)时间序列 -> getFundPlanTypeSeries


# 获取计划类型(券商集合理财) -> getFundPlanType


# 获取是否提取业绩报酬(券商集合理财)时间序列 -> getFundPerformanceFeeOrNotSeries


# 获取是否提取业绩报酬(券商集合理财) -> getFundPerformanceFeeOrNot


# 获取业绩报酬提取方法时间序列 -> getFundPerformanceFeeMethodSeries


# 获取业绩报酬提取方法 -> getFundPerformanceFeeMethod


# 获取管理费说明时间序列 -> getFundMgNtFeeExplainSeries


# 获取管理费说明 -> getFundMgNtFeeExplain


# 获取信托类别(信托)时间序列 -> getTrustTypeSeries


# 获取信托类别(信托) -> getTrustType


# 获取信托投资领域时间序列 -> getTrustInvestFieldSeries


# 获取信托投资领域 -> getTrustInvestField


# 获取信托产品类别时间序列 -> getTrustSourceTypeSeries


# 获取信托产品类别 -> getTrustSourceType


# 获取预计年收益率(信托)时间序列 -> getFundExpectedRateOfReturnSeries


# 获取预计年收益率(信托) -> getFundExpectedRateOfReturn


# 获取是否结构化产品(信托)时间序列 -> getFundStructuredOrNotSeries


# 获取是否结构化产品(信托) -> getFundStructuredOrNot


# 获取受托人(信托)时间序列 -> getFundTrusteeSeries


# 获取受托人(信托) -> getFundTrustee


# 获取证券经纪人(信托)时间序列 -> getFundSecuritiesBrokerSeries


# 获取证券经纪人(信托) -> getFundSecuritiesBroker


# 获取发行地(信托)时间序列 -> getFundIssuingPlaceSeries


# 获取发行地(信托) -> getFundIssuingPlace


# 获取浮动收益说明(信托)时间序列 -> getFundFloatingRateNoteSeries


# 获取浮动收益说明(信托) -> getFundFloatingRateNote


# 获取一般受益权金额(信托)时间序列 -> getFundGeneralBeneficialAmountSeries


# 获取一般受益权金额(信托) -> getFundGeneralBeneficialAmount


# 获取优先受益权金额(信托)时间序列 -> getFundPriorityBeneficialAmountSeries


# 获取优先受益权金额(信托) -> getFundPriorityBeneficialAmount


# 获取委托资金比(优先/一般)(信托)时间序列 -> getFundPriorityToGeneralSeries


# 获取委托资金比(优先/一般)(信托) -> getFundPriorityToGeneral


# 获取发行信托合同总数(信托)时间序列 -> getFundIssuedContractAmountSeries


# 获取发行信托合同总数(信托) -> getFundIssuedContractAmount


# 获取信用增级情况时间序列 -> getAdvanceCreditDescSeries


# 获取信用增级情况 -> getAdvanceCreditDesc


# 获取预期收益率说明时间序列 -> getAnticipateYieldDescSeries


# 获取预期收益率说明 -> getAnticipateYieldDesc


# 获取信托项目关联企业名称时间序列 -> getTrustRelatedFirmSeries


# 获取信托项目关联企业名称 -> getTrustRelatedFirm


# 获取销售起始日期时间序列 -> getFundSubStartDateSeries


# 获取销售起始日期 -> getFundSubStartDate


# 获取销售截止日期时间序列 -> getFundSubEnddateSeries


# 获取销售截止日期 -> getFundSubEnddate


# 获取目标规模时间序列 -> getFundTargetScaleSeries


# 获取目标规模 -> getFundTargetScale


# 获取有效认购户数时间序列 -> getFundEffSubsCrHoleDerNoSeries


# 获取有效认购户数 -> getFundEffSubsCrHoleDerNo


# 获取最低参与金额时间序列 -> getFundMinBuyAmountSeries


# 获取最低参与金额 -> getFundMinBuyAmount


# 获取追加认购最低金额时间序列 -> getFundMinAddBuyAmountSeries


# 获取追加认购最低金额 -> getFundMinAddBuyAmount


# 获取管理人参与金额时间序列 -> getFundManagersBuyAmountSeries


# 获取管理人参与金额 -> getFundManagersBuyAmount


# 获取开放日说明时间序列 -> getFundOpenDayIllUsSeries


# 获取开放日说明 -> getFundOpenDayIllUs


# 获取封闭期说明时间序列 -> getFundCloseDayIllUsSeries


# 获取封闭期说明 -> getFundCloseDayIllUs


# 获取投资策略分类(一级)(私募)时间序列 -> getFundFirstInvestStrategySeries


# 获取投资策略分类(一级)(私募) -> getFundFirstInvestStrategy


# 获取投资策略分类(二级)(私募)时间序列 -> getFundSecondInvestStrategySeries


# 获取投资策略分类(二级)(私募) -> getFundSecondInvestStrategy


# 获取产品发行渠道时间序列 -> getIssueChannelSeries


# 获取产品发行渠道 -> getIssueChannel


# 获取投资顾问时间序列 -> getFundInvestmentAdvisorSeries


# 获取投资顾问 -> getFundInvestmentAdvisor


# 获取基金净值更新频率时间序列 -> getNavUpdateFrequencySeries


# 获取基金净值更新频率 -> getNavUpdateFrequency


# 获取基金净值完整度时间序列 -> getNavUpdateCompletenessSeries


# 获取基金净值完整度 -> getNavUpdateCompleteness


# 获取协会备案管理人在管规模时间序列 -> getFundManageScaleIntervalSeries


# 获取协会备案管理人在管规模 -> getFundManageScaleInterval


# 获取是否保本时间序列 -> getFundGuaranteedOrNotSeries


# 获取是否保本 -> getFundGuaranteedOrNot


# 获取银行理财风险等级(银行)时间序列 -> getFundLcRiskLevelSeries


# 获取银行理财风险等级(银行) -> getFundLcRiskLevel


# 获取产品运作方式时间序列 -> getFundOperationModeSeries


# 获取产品运作方式 -> getFundOperationMode


# 获取业务模式时间序列 -> getFundBusinessModeSeries


# 获取业务模式 -> getFundBusinessMode


# 获取收益起始日时间序列 -> getFundReturnStartDateSeries


# 获取收益起始日 -> getFundReturnStartDate


# 获取收益终止日时间序列 -> getFundReturnEnddateSeries


# 获取收益终止日 -> getFundReturnEnddate


# 获取实际运作期限时间序列 -> getFundActualDurationSeries


# 获取实际运作期限 -> getFundActualDuration


# 获取委托金额上限时间序列 -> getFundMaxSubScripAmountSeries


# 获取委托金额上限 -> getFundMaxSubScripAmount


# 获取实际年化收益率时间序列 -> getFundActualAnnualYieldSeries


# 获取实际年化收益率 -> getFundActualAnnualYield


# 获取实际到期日时间序列 -> getFundActualMaturityDateSeries


# 获取实际到期日 -> getFundActualMaturityDate


# 获取付息方式说明时间序列 -> getFundInterestPayMethodSeries


# 获取付息方式说明 -> getFundInterestPayMethod


# 获取资金到账天数时间序列 -> getFundFundArrivalDaysSeries


# 获取资金到账天数 -> getFundFundArrivalDays


# 获取是否可提前终止时间序列 -> getFundEarlyTerminationOrNotSeries


# 获取是否可提前终止 -> getFundEarlyTerminationOrNot


# 获取提前终止条件时间序列 -> getFundCNdPreTerminationSeries


# 获取提前终止条件 -> getFundCNdPreTermination


# 获取申购赎回条件时间序列 -> getFundCNdpUrchRedemptionSeries


# 获取申购赎回条件 -> getFundCNdpUrchRedemption


# 获取收益挂钩标的时间序列 -> getFundUnderlyingTargetSeries


# 获取收益挂钩标的 -> getFundUnderlyingTarget


# 获取主要风险点时间序列 -> getFundMainRiskSeries


# 获取主要风险点 -> getFundMainRisk


# 获取资产类型时间序列 -> getFundReItsTypeSeries


# 获取资产类型 -> getFundReItsType


# 获取项目介绍时间序列 -> getFundReItsInfoSeries


# 获取项目介绍 -> getFundReItsInfo


# 获取询价区间上限时间序列 -> getFundReItsPriceMaxSeries


# 获取询价区间上限 -> getFundReItsPriceMax


# 获取询价区间下限时间序列 -> getFundReItsPriceMinSeries


# 获取询价区间下限 -> getFundReItsPriceMin


# 获取战略发售起始日时间序列 -> getFundReItsSIsTDateSeries


# 获取战略发售起始日 -> getFundReItsSIsTDate


# 获取战略发售截止日时间序列 -> getFundReItsSienDateSeries


# 获取战略发售截止日 -> getFundReItsSienDate


# 获取战略投资方认购份额时间序列 -> getFundReItsSiShareSubSeries


# 获取战略投资方认购份额 -> getFundReItsSiShareSub


# 获取战略配售份额时间序列 -> getFundReItsSiShareSeries


# 获取战略配售份额 -> getFundReItsSiShare


# 获取战略配售份额占比时间序列 -> getFundReItsSiShareRaSeries


# 获取战略配售份额占比 -> getFundReItsSiShareRa


# 获取战略投资方认购比例时间序列 -> getFundReItsSiRatioSeries


# 获取战略投资方认购比例 -> getFundReItsSiRatio


# 获取网下发售起始日时间序列 -> getFundReItsOffStDateSeries


# 获取网下发售起始日 -> getFundReItsOffStDate


# 获取网下发售截止日时间序列 -> getFundReItsOffendAteSeries


# 获取网下发售截止日 -> getFundReItsOffendAte


# 获取网下认购份额时间序列 -> getFundReItSoIsHareSeries


# 获取网下认购份额 -> getFundReItSoIsHare


# 获取网下配售份额时间序列 -> getFundReItsOffShareSeries


# 获取网下配售份额 -> getFundReItsOffShare


# 获取网下配售份额占比时间序列 -> getFundReItsOffShareRaSeries


# 获取网下配售份额占比 -> getFundReItsOffShareRa


# 获取网下投资方认购比例时间序列 -> getFundReItSoIRatioSeries


# 获取网下投资方认购比例 -> getFundReItSoIRatio


# 获取公众发售起始日时间序列 -> getFundReItsPbsTDateSeries


# 获取公众发售起始日 -> getFundReItsPbsTDate


# 获取公众发售截止日时间序列 -> getFundReItsPBenDateSeries


# 获取公众发售截止日 -> getFundReItsPBenDate


# 获取公众认购份额时间序列 -> getFundReItsPiShareSeries


# 获取公众认购份额 -> getFundReItsPiShare


# 获取公众配售份额时间序列 -> getFundReItsPbShareSeries


# 获取公众配售份额 -> getFundReItsPbShare


# 获取公众配售份额占比时间序列 -> getFundReItsPbShareRaSeries


# 获取公众配售份额占比 -> getFundReItsPbShareRa


# 获取公众投资方认购比例时间序列 -> getFundReItsPiRatioSeries


# 获取公众投资方认购比例 -> getFundReItsPiRatio


# 获取项目运营风险时间序列 -> getFundReItsOpRiskSeries


# 获取项目运营风险 -> getFundReItsOpRisk


# 获取资产名称时间序列 -> getFundReItsAsNameSeries


# 获取资产名称 -> getFundReItsAsName


# 获取资产所在地时间序列 -> getFundReItsLocationSeries


# 获取资产所在地 -> getFundReItsLocation


# 获取项目公司名称时间序列 -> getFundReItsComNameSeries


# 获取项目公司名称 -> getFundReItsComName


# 获取网下机构自营投资账户配售数量时间序列 -> getFundReItsPIsSeries


# 获取网下机构自营投资账户配售数量 -> getFundReItsPIs


# 获取网下机构自营投资账户配售金额时间序列 -> getFundReItsPimSeries


# 获取网下机构自营投资账户配售金额 -> getFundReItsPim


# 获取网下机构自营投资账户配售份额占比时间序列 -> getFundReItsPirSeries


# 获取网下机构自营投资账户配售份额占比 -> getFundReItsPir


# 获取网下私募基金配售数量时间序列 -> getFundReItsPfsSeries


# 获取网下私募基金配售数量 -> getFundReItsPfs


# 获取网下私募基金配售金额时间序列 -> getFundReItsPFmSeries


# 获取网下私募基金配售金额 -> getFundReItsPFm


# 获取网下私募基金配售份额占比时间序列 -> getFundReItsPFrSeries


# 获取网下私募基金配售份额占比 -> getFundReItsPFr


# 获取网下保险资金投资账户配售数量时间序列 -> getFundReItsIsSSeries


# 获取网下保险资金投资账户配售数量 -> getFundReItsIsS


# 获取网下保险资金投资账户配售金额时间序列 -> getFundReItsIsMSeries


# 获取网下保险资金投资账户配售金额 -> getFundReItsIsM


# 获取网下保险资金投资账户配售份额占比时间序列 -> getFundReItsIsRSeries


# 获取网下保险资金投资账户配售份额占比 -> getFundReItsIsR


# 获取网下集合信托计划配售数量时间序列 -> getFundReItsTrsSeries


# 获取网下集合信托计划配售数量 -> getFundReItsTrs


# 获取网下集合信托计划配售金额时间序列 -> getFundReItsTrmSeries


# 获取网下集合信托计划配售金额 -> getFundReItsTrm


# 获取网下集合信托计划配售份额占比时间序列 -> getFundReItsTrRSeries


# 获取网下集合信托计划配售份额占比 -> getFundReItsTrR


# 获取网下证券公司集合资产管理计划配售数量时间序列 -> getFundReItsScSSeries


# 获取网下证券公司集合资产管理计划配售数量 -> getFundReItsScS


# 获取网下证券公司集合资产管理计划配售金额时间序列 -> getFundReItsSCmSeries


# 获取网下证券公司集合资产管理计划配售金额 -> getFundReItsSCm


# 获取网下证券公司集合资产管理计划配售份额占比时间序列 -> getFundReItsSCrSeries


# 获取网下证券公司集合资产管理计划配售份额占比 -> getFundReItsSCr


# 获取网下证券公司单一资产管理计划配售数量时间序列 -> getFundReItsSCssSeries


# 获取网下证券公司单一资产管理计划配售数量 -> getFundReItsSCss


# 获取网下证券公司单一资产管理计划配售金额时间序列 -> getFundReItsScSmSeries


# 获取网下证券公司单一资产管理计划配售金额 -> getFundReItsScSm


# 获取网下证券公司单一资产管理计划配售份额占比时间序列 -> getFundReItsSCsrSeries


# 获取网下证券公司单一资产管理计划配售份额占比 -> getFundReItsSCsr


# 获取限售份额时间序列 -> getFundReItsLimitedShareSeries


# 获取限售份额 -> getFundReItsLimitedShare


# 获取估价收益率(%)(中债)时间序列 -> getYieldCnBdSeries


# 获取估价收益率(%)(中债) -> getYieldCnBd


# 获取估价净价(中债)时间序列 -> getNetCnBdSeries


# 获取估价净价(中债) -> getNetCnBd


# 获取估价全价(中债)时间序列 -> getDirtyCnBdSeries


# 获取估价全价(中债) -> getDirtyCnBd


# 获取日终估价全价(中债)时间序列 -> getPriceCnBdSeries


# 获取日终估价全价(中债) -> getPriceCnBd


# 获取估价修正久期(中债)时间序列 -> getModiDuraCnBdSeries


# 获取估价修正久期(中债) -> getModiDuraCnBd


# 获取待偿年限(年)(中债)时间序列 -> getMatUCnBdSeries


# 获取待偿年限(年)(中债) -> getMatUCnBd


# 获取应计利息(中债)时间序列 -> getAccruedInterestCnBdSeries


# 获取应计利息(中债) -> getAccruedInterestCnBd


# 获取日终应计利息(中债)时间序列 -> getAccRIntDayEndCnBdSeries


# 获取日终应计利息(中债) -> getAccRIntDayEndCnBd


# 获取估价利差久期(中债)时间序列 -> getSprDuraCnBdSeries


# 获取估价利差久期(中债) -> getSprDuraCnBd


# 获取估价利率久期(中债)时间序列 -> getInterestDurationCnBdSeries


# 获取估价利率久期(中债) -> getInterestDurationCnBd


# 获取点差收益率(中债)时间序列 -> getSpreadYieldCnBdSeries


# 获取点差收益率(中债) -> getSpreadYieldCnBd


# 获取估价凸性(中债)时间序列 -> getCNvXTyCnBdSeries


# 获取估价凸性(中债) -> getCNvXTyCnBd


# 获取估价利差凸性(中债)时间序列 -> getSPrcNxtCnBdSeries


# 获取估价利差凸性(中债) -> getSPrcNxtCnBd


# 获取估价利率凸性(中债)时间序列 -> getInterestCNvXTyCnBdSeries


# 获取估价利率凸性(中债) -> getInterestCNvXTyCnBd


# 获取加权平均结算收益率(%)(中债)时间序列 -> getMcYieldCnBdSeries


# 获取加权平均结算收益率(%)(中债) -> getMcYieldCnBd


# 获取加权平均结算净价(中债)时间序列 -> getMCnetCnBdSeries


# 获取加权平均结算净价(中债) -> getMCnetCnBd


# 获取加权平均结算全价(中债)时间序列 -> getMDirtyCnBdSeries


# 获取加权平均结算全价(中债) -> getMDirtyCnBd


# 获取市场隐含评级(中债)时间序列 -> getRateLatestMirCnBdSeries


# 获取市场隐含评级(中债) -> getRateLatestMirCnBd


# 获取市场历史隐含评级(中债)时间序列 -> getRateHistoricalMirCnBdSeries


# 获取市场历史隐含评级(中债) -> getRateHistoricalMirCnBd


# 获取最新估值日期(中债)时间序列 -> getLastDateCnBdSeries


# 获取最新估值日期(中债) -> getLastDateCnBd


# 获取估算的行权后票面利率时间序列 -> getExerciseCouponRateCnBdSeries


# 获取估算的行权后票面利率 -> getExerciseCouponRateCnBd


# 获取剩余本金(中债)时间序列 -> getLatestParCnBdSeries


# 获取剩余本金(中债) -> getLatestParCnBd


# 获取估价收益率(中证指数)时间序列 -> getYieldCsi1Series


# 获取估价收益率(中证指数) -> getYieldCsi1


# 获取估价净价(中证指数)时间序列 -> getNetCsi1Series


# 获取估价净价(中证指数) -> getNetCsi1


# 获取估价全价(中证指数)时间序列 -> getDirtyCsi1Series


# 获取估价全价(中证指数) -> getDirtyCsi1


# 获取估价修正久期(中证指数)时间序列 -> getModiDuraCsi1Series


# 获取估价修正久期(中证指数) -> getModiDuraCsi1


# 获取应计利息(中证指数)时间序列 -> getAccruedInterestCsiSeries


# 获取应计利息(中证指数) -> getAccruedInterestCsi


# 获取估价凸性(中证指数)时间序列 -> getCNvXTyCsi1Series


# 获取估价凸性(中证指数) -> getCNvXTyCsi1


# 获取最新估值日期(中证指数)时间序列 -> getLastDateCsiSeries


# 获取最新估值日期(中证指数) -> getLastDateCsi


# 获取隐含评级(中证指数)时间序列 -> getRateLatestMirCsiSeries


# 获取隐含评级(中证指数) -> getRateLatestMirCsi


# 获取隐含违约率(中证指数)时间序列 -> getRateDefaultCsiSeries


# 获取隐含违约率(中证指数) -> getRateDefaultCsi


# 获取可交换债估值(中证指数)时间序列 -> getEbValCsiSeries


# 获取可交换债估值(中证指数) -> getEbValCsi


# 获取可交换债期权价值(中证指数)时间序列 -> getEbOptionValCsiSeries


# 获取可交换债期权价值(中证指数) -> getEbOptionValCsi


# 获取可交换债纯债溢价率(中证指数)时间序列 -> getEbBondPreCsiSeries


# 获取可交换债纯债溢价率(中证指数) -> getEbBondPreCsi


# 获取可交换债估值收益率(中证指数)时间序列 -> getEbValYieldCsiSeries


# 获取可交换债估值收益率(中证指数) -> getEbValYieldCsi


# 获取可交换债转股溢价率(中证指数)时间序列 -> getEbConversionPreCsiSeries


# 获取可交换债转股溢价率(中证指数) -> getEbConversionPreCsi


# 获取估价收益率(上清所)时间序列 -> getYieldShcSeries


# 获取估价收益率(上清所) -> getYieldShc


# 获取估价净价(上清所)时间序列 -> getNetShcSeries


# 获取估价净价(上清所) -> getNetShc


# 获取估价全价(上清所)时间序列 -> getDirtyShcSeries


# 获取估价全价(上清所) -> getDirtyShc


# 获取估价修正久期(上清所)时间序列 -> getModiDuraShcSeries


# 获取估价修正久期(上清所) -> getModiDuraShc


# 获取应计利息(上清所)时间序列 -> getAccruedInterestShcSeries


# 获取应计利息(上清所) -> getAccruedInterestShc


# 获取估价凸性(上清所)时间序列 -> getCNvXTyShcSeries


# 获取估价凸性(上清所) -> getCNvXTyShc


# 获取最新估值日期(上清所)时间序列 -> getLastDateShcSeries


# 获取最新估值日期(上清所) -> getLastDateShc


# 获取指数值(中债)时间序列 -> getDQCloseCnBdSeries


# 获取指数值(中债) -> getDQCloseCnBd


# 获取现券结算量(中债)时间序列 -> getDQAmountCnBdSeries


# 获取现券结算量(中债) -> getDQAmountCnBd


# 获取平均市值法凸性时间序列 -> getAnalCapConvexitySeries


# 获取平均市值法凸性 -> getAnalCapConvexity


# 获取平均市值法久期时间序列 -> getAnalCapDurationSeries


# 获取平均市值法久期 -> getAnalCapDuration


# 获取平均市值法到期收益率时间序列 -> getAnalCapYTMSeries


# 获取平均市值法到期收益率 -> getAnalCapYTM


# 获取平均现金流法凸性时间序列 -> getAnalCashFlowConvexitySeries


# 获取平均现金流法凸性 -> getAnalCashFlowConvexity


# 获取平均现金流法久期时间序列 -> getAnalCashFlowDurationSeries


# 获取平均现金流法久期 -> getAnalCashFlowDuration


# 获取平均现金流法到期收益率时间序列 -> getAnalCashFlowYTMSeries


# 获取平均现金流法到期收益率 -> getAnalCashFlowYTM


# 获取平均派息率时间序列 -> getAnalIpRatioSeries


# 获取平均派息率 -> getAnalIpRatio


# 获取平均待偿期时间序列 -> getAnalPeriodSeries


# 获取平均待偿期 -> getAnalPeriod


# 获取上证固收平台成交金额时间序列 -> getAmountFixedIncomeSeries


# 获取上证固收平台成交金额 -> getAmountFixedIncome


# 获取双边买入净价(加权平均)时间序列 -> getBinetBidWtSeries


# 获取双边买入净价(加权平均) -> getBinetBidWt


# 获取双边买入收益率(加权平均)时间序列 -> getBibiDrTWtSeries


# 获取双边买入收益率(加权平均) -> getBibiDrTWt


# 获取双边卖出净价(加权平均)时间序列 -> getBinetAskWtSeries


# 获取双边卖出净价(加权平均) -> getBinetAskWt


# 获取双边卖出收益率(加权平均)时间序列 -> getBiasKrTWtSeries


# 获取双边卖出收益率(加权平均) -> getBiasKrTWt


# 获取双边买入净价(最优)时间序列 -> getBinetBidBstSeries


# 获取双边买入净价(最优) -> getBinetBidBst


# 获取双边买入收益率(最优)时间序列 -> getBibiDrTBstSeries


# 获取双边买入收益率(最优) -> getBibiDrTBst


# 获取双边卖出净价(最优)时间序列 -> getBinetAskBstSeries


# 获取双边卖出净价(最优) -> getBinetAskBst


# 获取双边卖出收益率(最优)时间序列 -> getBiasKrTBstSeries


# 获取双边卖出收益率(最优) -> getBiasKrTBst


# 获取双边报价笔数时间序列 -> getBIqTvOlmSeries


# 获取双边报价笔数 -> getBIqTvOlm


# 获取报价买入净价(算术平均)时间序列 -> getNetBidAvgSeries


# 获取报价买入净价(算术平均) -> getNetBidAvg


# 获取报价买入收益率(算术平均)时间序列 -> getBidRtAvgSeries


# 获取报价买入收益率(算术平均) -> getBidRtAvg


# 获取报价卖出净价(算术平均)时间序列 -> getNeTaskAvgSeries


# 获取报价卖出净价(算术平均) -> getNeTaskAvg


# 获取报价卖出收益率(算术平均)时间序列 -> getAskRtAvgSeries


# 获取报价卖出收益率(算术平均) -> getAskRtAvg


# 获取报价买入净价(最优)时间序列 -> getNetBidBstSeries


# 获取报价买入净价(最优) -> getNetBidBst


# 获取报价买入收益率(最优)时间序列 -> getBidRtBstSeries


# 获取报价买入收益率(最优) -> getBidRtBst


# 获取报价卖出净价(最优)时间序列 -> getNeTaskBstSeries


# 获取报价卖出净价(最优) -> getNeTaskBst


# 获取报价卖出收益率(最优)时间序列 -> getAskRtBstSeries


# 获取报价卖出收益率(最优) -> getAskRtBst


# 获取报价总笔数时间序列 -> getQtVolMSeries


# 获取报价总笔数 -> getQtVolM


# 获取区间成交金额时间序列 -> getPqAmountSeries


# 获取区间成交金额 -> getPqAmount


# 获取单位净值时间序列 -> getNavSeries


# 获取单位净值 -> getNav


# 获取单位净值币种时间序列 -> getFundNavCurSeries


# 获取单位净值币种 -> getFundNavCur


# 获取单位净值(不前推)时间序列 -> getNav2Series


# 获取单位净值(不前推) -> getNav2


# 获取单位净值(支持转型基金)时间序列 -> getNavUnitTransformSeries


# 获取单位净值(支持转型基金) -> getNavUnitTransform


# 获取复权单位净值时间序列 -> getNavAdjSeries


# 获取复权单位净值 -> getNavAdj


# 获取复权单位净值(不前推)时间序列 -> getNavAdj2Series


# 获取复权单位净值(不前推) -> getNavAdj2


# 获取累计单位净值时间序列 -> getNavAccSeries


# 获取累计单位净值 -> getNavAcc


# 获取累计单位净值(支持转型基金)时间序列 -> getNavAccumulatedTransformSeries


# 获取累计单位净值(支持转型基金) -> getNavAccumulatedTransform


# 获取复权单位净值(支持转型基金)时间序列 -> getNavAdjustedTransformSeries


# 获取复权单位净值(支持转型基金) -> getNavAdjustedTransform


# 获取复权单位净值增长时间序列 -> getNavAdjChgSeries


# 获取复权单位净值增长 -> getNavAdjChg


# 获取累计单位净值增长时间序列 -> getNavAccChgSeries


# 获取累计单位净值增长 -> getNavAccChg


# 获取复权单位净值增长率时间序列 -> getNavAdjReturnSeries


# 获取复权单位净值增长率 -> getNavAdjReturn


# 获取累计单位净值增长率时间序列 -> getNavAccReturnSeries


# 获取累计单位净值增长率 -> getNavAccReturn


# 获取复权单位净值相对大盘增长率时间序列 -> getRelNavAdjReturnSeries


# 获取复权单位净值相对大盘增长率 -> getRelNavAdjReturn


# 获取当期复权单位净值增长率时间序列 -> getNavAdjReturn1Series


# 获取当期复权单位净值增长率 -> getNavAdjReturn1


# 获取区间最高单位净值时间序列 -> getNavHighPerSeries


# 获取区间最高单位净值 -> getNavHighPer


# 获取区间最高单位净值日时间序列 -> getFundHighestNavDateSeries


# 获取区间最高单位净值日 -> getFundHighestNavDate


# 获取区间最低单位净值时间序列 -> getNavLowPerSeries


# 获取区间最低单位净值 -> getNavLowPer


# 获取区间最低单位净值日时间序列 -> getFundLowestNavDateSeries


# 获取区间最低单位净值日 -> getFundLowestNavDate


# 获取区间最高复权单位净值时间序列 -> getNavAdjHighPerSeries


# 获取区间最高复权单位净值 -> getNavAdjHighPer


# 获取区间最高复权单位净值日时间序列 -> getFundHighestAdjNavDateSeries


# 获取区间最高复权单位净值日 -> getFundHighestAdjNavDate


# 获取区间最低复权单位净值时间序列 -> getNavAdjLowPerSeries


# 获取区间最低复权单位净值 -> getNavAdjLowPer


# 获取区间最低复权单位净值日时间序列 -> getFundLowestAdjNavDateSeries


# 获取区间最低复权单位净值日 -> getFundLowestAdjNavDate


# 获取区间最高累计单位净值时间序列 -> getNavAccHighPerSeries


# 获取区间最高累计单位净值 -> getNavAccHighPer


# 获取区间最高累计单位净值日时间序列 -> getFundHighestAcCumNavDateSeries


# 获取区间最高累计单位净值日 -> getFundHighestAcCumNavDate


# 获取区间最低累计单位净值时间序列 -> getNavAccLowPerSeries


# 获取区间最低累计单位净值 -> getNavAccLowPer


# 获取区间最低累计单位净值日时间序列 -> getFundLowestAcCumNavDateSeries


# 获取区间最低累计单位净值日 -> getFundLowestAcCumNavDate


# 获取自成立日起复权单位净值增长率时间序列 -> getSiNavAdjReturnSeries


# 获取自成立日起复权单位净值增长率 -> getSiNavAdjReturn


# 获取投连险卖出价时间序列 -> getNavSellPriceSeries


# 获取投连险卖出价 -> getNavSellPrice


# 获取最近基金净值日期时间序列 -> getNavDateSeries


# 获取最近基金净值日期 -> getNavDate


# 获取最新净值除权日时间序列 -> getNavExRightDateSeries


# 获取最新净值除权日 -> getNavExRightDate


# 获取基金净值公布类型时间序列 -> getNavPublishTypeSeries


# 获取基金净值公布类型 -> getNavPublishType


# 获取现金分红净值增长率时间序列 -> getNavDivReturnSeries


# 获取现金分红净值增长率 -> getNavDivReturn


# 获取区间净值超越基准收益率时间序列 -> getNavOverBenchReturnPerSeries


# 获取区间净值超越基准收益率 -> getNavOverBenchReturnPer


# 获取区间净值超越基准收益频率时间序列 -> getNavOverBenchReturnFrEqSeries


# 获取区间净值超越基准收益频率 -> getNavOverBenchReturnFrEq


# 获取区间净值超越基准收益频率(百分比)时间序列 -> getNavOverBenchReturnFrEq2Series


# 获取区间净值超越基准收益频率(百分比) -> getNavOverBenchReturnFrEq2


# 获取近1周回报时间序列 -> getReturn1WSeries


# 获取近1周回报 -> getReturn1W


# 获取近1周回报排名时间序列 -> getPeriodReturnRanking1WSeries


# 获取近1周回报排名 -> getPeriodReturnRanking1W


# 获取近1月回报时间序列 -> getReturn1MSeries


# 获取近1月回报 -> getReturn1M


# 获取近1月回报排名时间序列 -> getPeriodReturnRanking1MSeries


# 获取近1月回报排名 -> getPeriodReturnRanking1M


# 获取近3月回报时间序列 -> getReturn3MSeries


# 获取近3月回报 -> getReturn3M


# 获取近3月回报排名时间序列 -> getPeriodReturnRanking3MSeries


# 获取近3月回报排名 -> getPeriodReturnRanking3M


# 获取近6月回报时间序列 -> getReturn6MSeries


# 获取近6月回报 -> getReturn6M


# 获取近6月回报排名时间序列 -> getPeriodReturnRanking6MSeries


# 获取近6月回报排名 -> getPeriodReturnRanking6M


# 获取近1年回报时间序列 -> getReturn1YSeries


# 获取近1年回报 -> getReturn1Y


# 获取近1年回报排名时间序列 -> getPeriodReturnRanking1YSeries


# 获取近1年回报排名 -> getPeriodReturnRanking1Y


# 获取近2年回报时间序列 -> getReturn2YSeries


# 获取近2年回报 -> getReturn2Y


# 获取近2年回报排名时间序列 -> getPeriodReturnRanking2YSeries


# 获取近2年回报排名 -> getPeriodReturnRanking2Y


# 获取近3年回报时间序列 -> getReturn3YSeries


# 获取近3年回报 -> getReturn3Y


# 获取近3年回报排名时间序列 -> getPeriodReturnRanking3YSeries


# 获取近3年回报排名 -> getPeriodReturnRanking3Y


# 获取近5年回报时间序列 -> getReturn5YSeries


# 获取近5年回报 -> getReturn5Y


# 获取近5年回报排名时间序列 -> getPeriodReturnRanking5YSeries


# 获取近5年回报排名 -> getPeriodReturnRanking5Y


# 获取近10年回报时间序列 -> getReturn10YSeries


# 获取近10年回报 -> getReturn10Y


# 获取近10年回报排名时间序列 -> getPeriodReturnRanking10YSeries


# 获取近10年回报排名 -> getPeriodReturnRanking10Y


# 获取今年以来回报时间序列 -> getReturnYTdSeries


# 获取今年以来回报 -> getReturnYTd


# 获取今年以来回报排名时间序列 -> getPeriodReturnRankingYTdSeries


# 获取今年以来回报排名 -> getPeriodReturnRankingYTd


# 获取成立以来回报时间序列 -> getReturnStdSeries


# 获取成立以来回报 -> getReturnStd


# 获取单月度回报时间序列 -> getReturnMSeries


# 获取单月度回报 -> getReturnM


# 获取单季度回报时间序列 -> getReturnQSeries


# 获取单季度回报 -> getReturnQ


# 获取单年度回报时间序列 -> getReturnYSeries


# 获取单年度回报 -> getReturnY


# 获取单年度回报排名时间序列 -> getPeriodReturnRankingYSeries


# 获取单年度回报排名 -> getPeriodReturnRankingY


# 获取同类基金区间平均收益率时间序列 -> getPeerFundAvgReturnPerSeries


# 获取同类基金区间平均收益率 -> getPeerFundAvgReturnPer


# 获取同类基金区间收益排名(字符串)时间序列 -> getPeerFundReturnRankPerSeries


# 获取同类基金区间收益排名(字符串) -> getPeerFundReturnRankPer


# 获取同类基金区间收益排名(百分比)时间序列 -> getPeerFundReturnRankPropPerSeries


# 获取同类基金区间收益排名(百分比) -> getPeerFundReturnRankPropPer


# 获取同类基金区间收益排名(百分比)(券商集合理财)时间序列 -> getPeerSamReturnRankPropPerSeries


# 获取同类基金区间收益排名(百分比)(券商集合理财) -> getPeerSamReturnRankPropPer


# 获取同类基金区间收益排名(百分比)(阳光私募)时间序列 -> getPeerHfReturnRankPropPerSeries


# 获取同类基金区间收益排名(百分比)(阳光私募) -> getPeerHfReturnRankPropPer


# 获取同类基金区间收益排名(券商集合理财)时间序列 -> getPeerSamReturnRankPerSeries


# 获取同类基金区间收益排名(券商集合理财) -> getPeerSamReturnRankPer


# 获取同类基金区间收益排名(阳光私募)时间序列 -> getPeerHfReturnRankPerSeries


# 获取同类基金区间收益排名(阳光私募) -> getPeerHfReturnRankPer


# 获取同类基金区间收益排名(阳光私募,投资策略)时间序列 -> getPeerHf2ReturnRankPerSeries


# 获取同类基金区间收益排名(阳光私募,投资策略) -> getPeerHf2ReturnRankPer


# 获取报告期净值增长率时间序列 -> getNavReturnSeries


# 获取报告期净值增长率 -> getNavReturn


# 获取报告期净值增长率标准差时间序列 -> getNavStdDevReturnSeries


# 获取报告期净值增长率标准差 -> getNavStdDevReturn


# 获取报告期净值增长率减基准增长率时间序列 -> getNavBenchDevReturnSeries


# 获取报告期净值增长率减基准增长率 -> getNavBenchDevReturn


# 获取报告期净值增长率减基准增长率标准差时间序列 -> getNavStdDevNavBenchSeries


# 获取报告期净值增长率减基准增长率标准差 -> getNavStdDevNavBench


# 获取份额结转方式时间序列 -> getMmFCarryOverSeries


# 获取份额结转方式 -> getMmFCarryOver


# 获取份额结转日期类型时间序列 -> getMmFCarryOverDateSeries


# 获取份额结转日期类型 -> getMmFCarryOverDate


# 获取7日年化收益率时间序列 -> getMmFAnnualIZedYieldSeries


# 获取7日年化收益率 -> getMmFAnnualIZedYield


# 获取区间7日年化收益率均值时间序列 -> getMmFAvgAnnualIZedYieldSeries


# 获取区间7日年化收益率均值 -> getMmFAvgAnnualIZedYield


# 获取区间7日年化收益率方差时间序列 -> getMmFVarAnnualIZedYieldSeries


# 获取区间7日年化收益率方差 -> getMmFVarAnnualIZedYield


# 获取万份基金单位收益时间序列 -> getMmFUnitYieldSeries


# 获取万份基金单位收益 -> getMmFUnitYield


# 获取区间万份基金单位收益均值时间序列 -> getMmFAvgUnitYieldSeries


# 获取区间万份基金单位收益均值 -> getMmFAvgUnitYield


# 获取区间万份基金单位收益总值时间序列 -> getMmFTotalUnitYieldSeries


# 获取区间万份基金单位收益总值 -> getMmFTotalUnitYield


# 获取区间万份基金单位收益方差时间序列 -> getMmFVarUnitYieldSeries


# 获取区间万份基金单位收益方差 -> getMmFVarUnitYield


# 获取股息率(报告期)时间序列 -> getDividendYieldSeries


# 获取股息率(报告期) -> getDividendYield


# 获取股息率(近12个月)时间序列 -> getDividendYield2Series


# 获取股息率(近12个月) -> getDividendYield2


# 获取发布方股息率(近12个月)时间序列 -> getValDividendYield2IssuerSeries


# 获取发布方股息率(近12个月) -> getValDividendYield2Issuer


# 获取市盈率百分位时间序列 -> getValPep2Series


# 获取市盈率百分位 -> getValPep2


# 获取市盈率分位数时间序列 -> getValPePercentileSeries


# 获取市盈率分位数 -> getValPePercentile


# 获取市净率分位数时间序列 -> getValPbPercentileSeries


# 获取市净率分位数 -> getValPbPercentile


# 获取股息率分位数时间序列 -> getValDividendPercentileSeries


# 获取股息率分位数 -> getValDividendPercentile


# 获取市销率分位数时间序列 -> getValPsPercentileSeries


# 获取市销率分位数 -> getValPsPercentile


# 获取市现率分位数时间序列 -> getValPcfPercentileSeries


# 获取市现率分位数 -> getValPcfPercentile


# 获取股权激励目标净利润时间序列 -> getTargetNpSeries


# 获取股权激励目标净利润 -> getTargetNp


# 获取量比时间序列 -> getVolRatioSeries


# 获取量比 -> getVolRatio


# 获取持买单量比上交易日增减时间序列 -> getOiLoiCSeries


# 获取持买单量比上交易日增减 -> getOiLoiC


# 获取持卖单量比上交易日增减时间序列 -> getOiSOicSeries


# 获取持卖单量比上交易日增减 -> getOiSOic


# 获取网下有效报价申购量比例时间序列 -> getIpoVsSharesPctSeries


# 获取网下有效报价申购量比例 -> getIpoVsSharesPct


# 获取网下高于有效报价上限的申购量比例时间序列 -> getIpoInvsSharesPctASeries


# 获取网下高于有效报价上限的申购量比例 -> getIpoInvsSharesPctA


# 获取近期创历史新低时间序列 -> getHistoryLowSeries


# 获取近期创历史新低 -> getHistoryLow


# 获取近期创历史新低次数时间序列 -> getHistoryLowDaysSeries


# 获取近期创历史新低次数 -> getHistoryLowDays


# 获取近期创阶段新高时间序列 -> getStageHighSeries


# 获取近期创阶段新高 -> getStageHigh


# 获取近期创历史新高时间序列 -> getHistoryHighSeries


# 获取近期创历史新高 -> getHistoryHigh


# 获取近期创历史新高次数时间序列 -> getHistoryHighDaysSeries


# 获取近期创历史新高次数 -> getHistoryHighDays


# 获取近期创阶段新低时间序列 -> getStageLowSeries


# 获取近期创阶段新低 -> getStageLow


# 获取连涨天数时间序列 -> getUpDaysSeries


# 获取连涨天数 -> getUpDays


# 获取连跌天数时间序列 -> getDownDaysSeries


# 获取连跌天数 -> getDownDays


# 获取向上有效突破均线时间序列 -> getBreakoutMaSeries


# 获取向上有效突破均线 -> getBreakoutMa


# 获取向下有效突破均线时间序列 -> getBreakdownMaSeries


# 获取向下有效突破均线 -> getBreakdownMa


# 获取成份创阶段新高数量时间序列 -> getTechAnalStageHighNumSeries


# 获取成份创阶段新高数量 -> getTechAnalStageHighNum


# 获取成份创阶段新低数量时间序列 -> getTechAnalStageLowNumSeries


# 获取成份创阶段新低数量 -> getTechAnalStageLowNum


# 获取均线多空头排列看涨看跌时间序列 -> getBullBearMaSeries


# 获取均线多空头排列看涨看跌 -> getBullBearMa


# 获取指数成份上涨数量时间序列 -> getTechUpNumSeries


# 获取指数成份上涨数量 -> getTechUpNum


# 获取指数成份下跌数量时间序列 -> getTechDownNumSeries


# 获取指数成份下跌数量 -> getTechDownNum


# 获取指数成份涨停数量时间序列 -> getTechLimitUpNumSeries


# 获取指数成份涨停数量 -> getTechLimitUpNum


# 获取指数成份跌停数量时间序列 -> getTechLimitDownNumSeries


# 获取指数成份跌停数量 -> getTechLimitDownNum


# 获取成份分红对指数影响时间序列 -> getDivCompIndexSeries


# 获取成份分红对指数影响 -> getDivCompIndex


# 获取平均收益率(年化,最近100周)时间序列 -> getAnnualYeIlD100WSeries


# 获取平均收益率(年化,最近100周) -> getAnnualYeIlD100W


# 获取平均收益率(年化,最近24个月)时间序列 -> getAnnualYeIlD24MSeries


# 获取平均收益率(年化,最近24个月) -> getAnnualYeIlD24M


# 获取平均收益率(年化,最近60个月)时间序列 -> getAnnualYeIlD60MSeries


# 获取平均收益率(年化,最近60个月) -> getAnnualYeIlD60M


# 获取年化波动率(最近100周)时间序列 -> getAnnualStDeVr100WSeries


# 获取年化波动率(最近100周) -> getAnnualStDeVr100W


# 获取年化波动率(最近24个月)时间序列 -> getAnnualStDeVr24MSeries


# 获取年化波动率(最近24个月) -> getAnnualStDeVr24M


# 获取年化波动率(最近60个月)时间序列 -> getAnnualStDeVr60MSeries


# 获取年化波动率(最近60个月) -> getAnnualStDeVr60M


# 获取平均收益率时间序列 -> getAvgReturnSeries


# 获取平均收益率 -> getAvgReturn


# 获取平均收益率(年化)时间序列 -> getAvgReturnYSeries


# 获取平均收益率(年化) -> getAvgReturnY


# 获取平均收益率_FUND时间序列 -> getRiskAvgReturnSeries


# 获取平均收益率_FUND -> getRiskAvgReturn


# 获取几何平均收益率时间序列 -> getRiskGemReturnSeries


# 获取几何平均收益率 -> getRiskGemReturn


# 获取贷款平均收益率_总计时间序列 -> getStmNoteBank720Series


# 获取贷款平均收益率_总计 -> getStmNoteBank720


# 获取贷款平均收益率_企业贷款及垫款时间序列 -> getStmNoteBank731Series


# 获取贷款平均收益率_企业贷款及垫款 -> getStmNoteBank731


# 获取贷款平均收益率_个人贷款及垫款时间序列 -> getStmNoteBank732Series


# 获取贷款平均收益率_个人贷款及垫款 -> getStmNoteBank732


# 获取贷款平均收益率_票据贴现时间序列 -> getStmNoteBank733Series


# 获取贷款平均收益率_票据贴现 -> getStmNoteBank733


# 获取贷款平均收益率_个人住房贷款时间序列 -> getStmNoteBank734Series


# 获取贷款平均收益率_个人住房贷款 -> getStmNoteBank734


# 获取贷款平均收益率_个人消费贷款时间序列 -> getStmNoteBank735Series


# 获取贷款平均收益率_个人消费贷款 -> getStmNoteBank735


# 获取贷款平均收益率_信用卡应收账款时间序列 -> getStmNoteBank736Series


# 获取贷款平均收益率_信用卡应收账款 -> getStmNoteBank736


# 获取贷款平均收益率_经营性贷款时间序列 -> getStmNoteBank737Series


# 获取贷款平均收益率_经营性贷款 -> getStmNoteBank737


# 获取贷款平均收益率_汽车贷款时间序列 -> getStmNoteBank738Series


# 获取贷款平均收益率_汽车贷款 -> getStmNoteBank738


# 获取贷款平均收益率_其他个人贷款时间序列 -> getStmNoteBank739Series


# 获取贷款平均收益率_其他个人贷款 -> getStmNoteBank739


# 获取贷款平均收益率_信用贷款时间序列 -> getStmNoteBank791Series


# 获取贷款平均收益率_信用贷款 -> getStmNoteBank791


# 获取贷款平均收益率_保证贷款时间序列 -> getStmNoteBank792Series


# 获取贷款平均收益率_保证贷款 -> getStmNoteBank792


# 获取贷款平均收益率_抵押贷款时间序列 -> getStmNoteBank793Series


# 获取贷款平均收益率_抵押贷款 -> getStmNoteBank793


# 获取贷款平均收益率_质押贷款时间序列 -> getStmNoteBank794Series


# 获取贷款平均收益率_质押贷款 -> getStmNoteBank794


# 获取贷款平均收益率_短期贷款时间序列 -> getStmNoteBank47Series


# 获取贷款平均收益率_短期贷款 -> getStmNoteBank47


# 获取贷款平均收益率_中长期贷款时间序列 -> getStmNoteBank49Series


# 获取贷款平均收益率_中长期贷款 -> getStmNoteBank49


# 获取区间收益率(年化)时间序列 -> getRiskAnnualIntervalYieldSeries


# 获取区间收益率(年化) -> getRiskAnnualIntervalYield


# 获取最大回撤时间序列 -> getRiskMaxDownsideSeries


# 获取最大回撤 -> getRiskMaxDownside


# 获取最大回撤恢复天数时间序列 -> getRiskMaxDownsideRecoverDaysSeries


# 获取最大回撤恢复天数 -> getRiskMaxDownsideRecoverDays


# 获取最大回撤同类平均时间序列 -> getRiskSimLAvgMaxDownsideSeries


# 获取最大回撤同类平均 -> getRiskSimLAvgMaxDownside


# 获取最大回撤区间日期时间序列 -> getRiskMaxDownsideDateSeries


# 获取最大回撤区间日期 -> getRiskMaxDownsideDate


# 获取任期最大回撤时间序列 -> getFundManagerMaxDrawDownSeries


# 获取任期最大回撤 -> getFundManagerMaxDrawDown


# 获取波动率时间序列 -> getStDeVrSeries


# 获取波动率 -> getStDeVr


# 获取波动率(年化)时间序列 -> getStDeVrySeries


# 获取波动率(年化) -> getStDeVry


# 获取年化波动率时间序列 -> getRiskStDevYearlySeries


# 获取年化波动率 -> getRiskStDevYearly


# 获取年化波动率同类平均时间序列 -> getRiskSimLAvgStDevYearlySeries


# 获取年化波动率同类平均 -> getRiskSimLAvgStDevYearly


# 获取交易量波动率_PIT时间序列 -> getTechVolumeVolatilitySeries


# 获取交易量波动率_PIT -> getTechVolumeVolatility


# 获取转债隐含波动率时间序列 -> getImpliedVolSeries


# 获取转债隐含波动率 -> getImpliedVol


# 获取个股与市场波动率比值_PIT时间序列 -> getRiskVolatilityRatioSeries


# 获取个股与市场波动率比值_PIT -> getRiskVolatilityRatio


# 获取252日残差收益波动率_PIT时间序列 -> getRiskReSidVol252Series


# 获取252日残差收益波动率_PIT -> getRiskReSidVol252


# 获取标准差系数时间序列 -> getStDcOfSeries


# 获取标准差系数 -> getStDcOf


# 获取非系统风险时间序列 -> getRiskNonSYsRisk1Series


# 获取非系统风险 -> getRiskNonSYsRisk1


# 获取非系统风险_FUND时间序列 -> getRiskNonSYsRiskSeries


# 获取非系统风险_FUND -> getRiskNonSYsRisk


# 获取剩余期限(天)时间序列 -> getDaySeries


# 获取剩余期限(天) -> getDay


# 获取剩余期限(年)时间序列 -> getPtMYearSeries


# 获取剩余期限(年) -> getPtMYear


# 获取行权剩余期限(年)时间序列 -> getTermIfExerciseSeries


# 获取行权剩余期限(年) -> getTermIfExercise


# 获取特殊剩余期限说明时间序列 -> getTermNoteSeries


# 获取特殊剩余期限说明 -> getTermNote


# 获取特殊剩余期限时间序列 -> getTermNote1Series


# 获取特殊剩余期限 -> getTermNote1


# 获取加权剩余期限(按本息)时间序列 -> getWeightedRtSeries


# 获取加权剩余期限(按本息) -> getWeightedRt


# 获取加权剩余期限(按本金)时间序列 -> getWeightedRt2Series


# 获取加权剩余期限(按本金) -> getWeightedRt2


# 获取应计利息时间序列 -> getAccruedInterestSeries


# 获取应计利息 -> getAccruedInterest


# 获取指定日应计利息时间序列 -> getCalcAccRIntSeries


# 获取指定日应计利息 -> getCalcAccRInt


# 获取已计息天数时间序列 -> getAccruedDaysSeries


# 获取已计息天数 -> getAccruedDays


# 获取上一付息日时间序列 -> getAnalPreCupNSeries


# 获取上一付息日 -> getAnalPreCupN


# 获取下一付息日时间序列 -> getNxcUpnSeries


# 获取下一付息日 -> getNxcUpn


# 获取下一付息日久期时间序列 -> getNxcUpnDurationSeries


# 获取下一付息日久期 -> getNxcUpnDuration


# 获取距下一付息日天数时间序列 -> getNxcUpn2Series


# 获取距下一付息日天数 -> getNxcUpn2


# 获取长期停牌起始日时间序列 -> getPqSuspendStartDateSeries


# 获取长期停牌起始日 -> getPqSuspendStartDate


# 获取长期停牌截止日时间序列 -> getPqSuspendEnddateSeries


# 获取长期停牌截止日 -> getPqSuspendEnddate


# 获取收盘到期收益率时间序列 -> getYTMBSeries


# 获取收盘到期收益率 -> getYTMB


# 获取赎回收益率时间序列 -> getYTcSeries


# 获取赎回收益率 -> getYTc


# 获取回售收益率时间序列 -> getYTPSeries


# 获取回售收益率 -> getYTP


# 获取基准久期时间序列 -> getBDurationSeries


# 获取基准久期 -> getBDuration


# 获取行权基准久期时间序列 -> getBDurationIfExeSeries


# 获取行权基准久期 -> getBDurationIfExe


# 获取利差久期时间序列 -> getSDurationSeries


# 获取利差久期 -> getSDuration


# 获取行权利差久期时间序列 -> getSDurationIfExeSeries


# 获取行权利差久期 -> getSDurationIfExe


# 获取指定日现金流时间序列 -> getDailyCfSeries


# 获取指定日现金流 -> getDailyCf


# 获取指定日利息现金流时间序列 -> getDailyCfIntSeries


# 获取指定日利息现金流 -> getDailyCfInt


# 获取指定日本金现金流时间序列 -> getDailyCfPrInSeries


# 获取指定日本金现金流 -> getDailyCfPrIn


# 获取票面调整收益率时间序列 -> getRCyTmSeries


# 获取票面调整收益率 -> getRCyTm


# 获取价格算票面调整收益率时间序列 -> getCalcAdjYieldSeries


# 获取价格算票面调整收益率 -> getCalcAdjYield


# 获取下一行权日时间序列 -> getNxOptionDateSeries


# 获取下一行权日 -> getNxOptionDate


# 获取行权收益率时间序列 -> getYTMIfExeSeries


# 获取行权收益率 -> getYTMIfExe


# 获取行权久期时间序列 -> getDurationIfExerciseSeries


# 获取行权久期 -> getDurationIfExercise


# 获取行权修正久期时间序列 -> getModiDurationIfExeSeries


# 获取行权修正久期 -> getModiDurationIfExe


# 获取行权凸性时间序列 -> getConvexityIfExeSeries


# 获取行权凸性 -> getConvexityIfExe


# 获取行权基准凸性时间序列 -> getBConvexityIfExeSeries


# 获取行权基准凸性 -> getBConvexityIfExe


# 获取行权利差凸性时间序列 -> getSConvexityIfExeSeries


# 获取行权利差凸性 -> getSConvexityIfExe


# 获取1月久期时间序列 -> getDuration1MSeries


# 获取1月久期 -> getDuration1M


# 获取3月久期时间序列 -> getDuration3MSeries


# 获取3月久期 -> getDuration3M


# 获取6月久期时间序列 -> getDuration6MSeries


# 获取6月久期 -> getDuration6M


# 获取1年久期时间序列 -> getDuration1YSeries


# 获取1年久期 -> getDuration1Y


# 获取2年久期时间序列 -> getDuration2YSeries


# 获取2年久期 -> getDuration2Y


# 获取3年久期时间序列 -> getDuration3YSeries


# 获取3年久期 -> getDuration3Y


# 获取4年久期时间序列 -> getDuration4YSeries


# 获取4年久期 -> getDuration4Y


# 获取5年久期时间序列 -> getDuration5YSeries


# 获取5年久期 -> getDuration5Y


# 获取15年久期时间序列 -> getDuration15YSeries


# 获取15年久期 -> getDuration15Y


# 获取7年久期时间序列 -> getDuration7YSeries


# 获取7年久期 -> getDuration7Y


# 获取9年久期时间序列 -> getDuration9YSeries


# 获取9年久期 -> getDuration9Y


# 获取10年久期时间序列 -> getDuration10YSeries


# 获取10年久期 -> getDuration10Y


# 获取20年久期时间序列 -> getDuration20YSeries


# 获取20年久期 -> getDuration20Y


# 获取30年久期时间序列 -> getDuration30YSeries


# 获取30年久期 -> getDuration30Y


# 获取短边久期时间序列 -> getDurationShortSeries


# 获取短边久期 -> getDurationShort


# 获取长边久期时间序列 -> getDurationLongSeries


# 获取长边久期 -> getDurationLong


# 获取当期收益率时间序列 -> getCurYieldSeries


# 获取当期收益率 -> getCurYield


# 获取纯债到期收益率时间序列 -> getYTMCbSeries


# 获取纯债到期收益率 -> getYTMCb


# 获取纯债价值时间序列 -> getStrBValueSeries


# 获取纯债价值 -> getStrBValue


# 获取纯债溢价时间序列 -> getStrBPremiumSeries


# 获取纯债溢价 -> getStrBPremium


# 获取纯债溢价率时间序列 -> getStrBPremiumRatioSeries


# 获取纯债溢价率 -> getStrBPremiumRatio


# 获取转股价时间序列 -> getConVPriceSeries


# 获取转股价 -> getConVPrice


# 获取转股比例时间序列 -> getConVRatioSeries


# 获取转股比例 -> getConVRatio


# 获取转换价值时间序列 -> getConVValueSeries


# 获取转换价值 -> getConVValue


# 获取转股溢价时间序列 -> getConVPremiumSeries


# 获取转股溢价 -> getConVPremium


# 获取转股溢价率时间序列 -> getConVPremiumRatioSeries


# 获取转股溢价率 -> getConVPremiumRatio


# 获取转股市盈率时间序列 -> getConVpESeries


# 获取转股市盈率 -> getConVpE


# 获取转股市净率时间序列 -> getConVpBSeries


# 获取转股市净率 -> getConVpB


# 获取正股市盈率时间序列 -> getUnderlyingPeSeries


# 获取正股市盈率 -> getUnderlyingPe


# 获取正股市净率时间序列 -> getUnderlyingPbSeries


# 获取正股市净率 -> getUnderlyingPb


# 获取转股稀释率时间序列 -> getDiluteRateSeries


# 获取转股稀释率 -> getDiluteRate


# 获取对流通股稀释率时间序列 -> getLDiluteRateSeries


# 获取对流通股稀释率 -> getLDiluteRate


# 获取双低时间序列 -> getDoubleLowSeries


# 获取双低 -> getDoubleLow


# 获取转换因子时间序列 -> getTBfCVf2Series


# 获取转换因子 -> getTBfCVf2


# 获取转换因子(指定合约)时间序列 -> getTBfCVfSeries


# 获取转换因子(指定合约) -> getTBfCVf


# 获取转换因子(主力合约)时间序列 -> getTBfCVf3Series


# 获取转换因子(主力合约) -> getTBfCVf3


# 获取交割利息时间序列 -> getTBfInterestSeries


# 获取交割利息 -> getTBfInterest


# 获取区间利息时间序列 -> getTBfPaymentSeries


# 获取区间利息 -> getTBfPayment


# 获取交割成本时间序列 -> getTBfDeliverPriceSeries


# 获取交割成本 -> getTBfDeliverPrice


# 获取发票价格时间序列 -> getTBfInvoicePriceSeries


# 获取发票价格 -> getTBfInvoicePrice


# 获取期现价差时间序列 -> getTBfSpreadSeries


# 获取期现价差 -> getTBfSpread


# 获取基差时间序列 -> getTBfBasisSeries


# 获取基差 -> getTBfBasis


# 获取基差(股指期货)时间序列 -> getIfBasisSeries


# 获取基差(股指期货) -> getIfBasis


# 获取基差年化收益率(股指期货)时间序列 -> getAnalBasisAnnualYieldSeries


# 获取基差年化收益率(股指期货) -> getAnalBasisAnnualYield


# 获取基差率(股指期货)时间序列 -> getAnalBasisPercentSeries


# 获取基差率(股指期货) -> getAnalBasisPercent


# 获取基差(商品期货)时间序列 -> getAnalBasisSeries


# 获取基差(商品期货) -> getAnalBasis


# 获取基差率(商品期货)时间序列 -> getAnalBasisPercent2Series


# 获取基差率(商品期货) -> getAnalBasisPercent2


# 获取净基差时间序列 -> getTBfNetBasisSeries


# 获取净基差 -> getTBfNetBasis


# 获取远期收益率时间序列 -> getTBfFyTmSeries


# 获取远期收益率 -> getTBfFyTm


# 获取全价算净价时间序列 -> getCalcCleanSeries


# 获取全价算净价 -> getCalcClean


# 获取净价算全价时间序列 -> getCalcDirtySeries


# 获取净价算全价 -> getCalcDirty


# 获取麦考利久期时间序列 -> getCalcDurationSeries


# 获取麦考利久期 -> getCalcDuration


# 获取修正久期时间序列 -> getCalcMDurationSeries


# 获取修正久期 -> getCalcMDuration


# 获取凸性时间序列 -> getCalcConVSeries


# 获取凸性 -> getCalcConV


# 获取对应到期收益率曲线代码时间序列 -> getYCCodeSeries


# 获取对应到期收益率曲线代码 -> getYCCode


# 获取收益率曲线(中债样本券)时间序列 -> getCalcChinaBondSeries


# 获取收益率曲线(中债样本券) -> getCalcChinaBond


# 获取上海证券3年评级(夏普比率)时间序列 -> getRatingShanghaiSharpe3YSeries


# 获取上海证券3年评级(夏普比率) -> getRatingShanghaiSharpe3Y


# 获取上海证券3年评级(择时能力)时间序列 -> getRatingShanghaiTiming3YSeries


# 获取上海证券3年评级(择时能力) -> getRatingShanghaiTiming3Y


# 获取上海证券3年评级(选证能力)时间序列 -> getRatingShanghaiStocking3YSeries


# 获取上海证券3年评级(选证能力) -> getRatingShanghaiStocking3Y


# 获取上海证券5年评级(夏普比率)时间序列 -> getRatingShanghaiSharpe5YSeries


# 获取上海证券5年评级(夏普比率) -> getRatingShanghaiSharpe5Y


# 获取上海证券5年评级(择时能力)时间序列 -> getRatingShanghaiTiming5YSeries


# 获取上海证券5年评级(择时能力) -> getRatingShanghaiTiming5Y


# 获取上海证券5年评级(选证能力)时间序列 -> getRatingShanghaiStocking5YSeries


# 获取上海证券5年评级(选证能力) -> getRatingShanghaiStocking5Y


# 获取基金3年评级时间序列 -> getRating3YSeries


# 获取基金3年评级 -> getRating3Y


# 获取基金5年评级时间序列 -> getRating5YSeries


# 获取基金5年评级 -> getRating5Y


# 获取年化收益率时间序列 -> getRiskReturnYearlySeries


# 获取年化收益率 -> getRiskReturnYearly


# 获取年化收益率(工作日)时间序列 -> getRiskReturnYearlyTradeDateSeries


# 获取年化收益率(工作日) -> getRiskReturnYearlyTradeDate


# 获取几何平均年化收益率时间序列 -> getFundManagerGeometricAnnualIZedYieldSeries


# 获取几何平均年化收益率 -> getFundManagerGeometricAnnualIZedYield


# 获取算术平均年化收益率时间序列 -> getFundManagerArithmeticAnnualIZedYieldSeries


# 获取算术平均年化收益率 -> getFundManagerArithmeticAnnualIZedYield


# 获取超越基准几何平均年化收益率时间序列 -> getFundManagerGeometricAvgAnnualYieldOverBenchSeries


# 获取超越基准几何平均年化收益率 -> getFundManagerGeometricAvgAnnualYieldOverBench


# 获取超越基准算术平均年化收益率时间序列 -> getFundManagerArithmeticAvgAnnualYieldOverBenchSeries


# 获取超越基准算术平均年化收益率 -> getFundManagerArithmeticAvgAnnualYieldOverBench


# 获取区间净值超越基准年化收益率时间序列 -> getRiskNavOverBenchAnnualReturnSeries


# 获取区间净值超越基准年化收益率 -> getRiskNavOverBenchAnnualReturn


# 获取区间收益率(工作日年化)时间序列 -> getRiskAnnualIntervalYieldTradeDateSeries


# 获取区间收益率(工作日年化) -> getRiskAnnualIntervalYieldTradeDate


# 获取平均风险收益率时间序列 -> getRiskAvgRiskReturnSeries


# 获取平均风险收益率 -> getRiskAvgRiskReturn


# 获取几何平均风险收益率时间序列 -> getRiskGemAvgRiskReturnSeries


# 获取几何平均风险收益率 -> getRiskGemAvgRiskReturn


# 获取日跟踪偏离度(跟踪指数)时间序列 -> getRiskTrackDeviationTrackIndexSeries


# 获取日跟踪偏离度(跟踪指数) -> getRiskTrackDeviationTrackIndex


# 获取区间跟踪偏离度均值(业绩基准)时间序列 -> getRiskAvgTrackDeviationBenchmarkSeries


# 获取区间跟踪偏离度均值(业绩基准) -> getRiskAvgTrackDeviationBenchmark


# 获取区间跟踪偏离度均值(跟踪指数)时间序列 -> getRiskAvgTrackDeviationTrackIndexSeries


# 获取区间跟踪偏离度均值(跟踪指数) -> getRiskAvgTrackDeviationTrackIndex


# 获取回撤(相对前期高点)时间序列 -> getRiskDownsideSeries


# 获取回撤(相对前期高点) -> getRiskDownside


# 获取最大上涨时间序列 -> getRiskMaxUpsideSeries


# 获取最大上涨 -> getRiskMaxUpside


# 获取相关系数时间序列 -> getRiskCorreCoefficientSeries


# 获取相关系数 -> getRiskCorreCoefficient


# 获取相关系数(跟踪指数)时间序列 -> getRiskCorreCoefficientTrackIndexSeries


# 获取相关系数(跟踪指数) -> getRiskCorreCoefficientTrackIndex


# 获取下跌相关系数_PIT时间序列 -> getTechDdNcrSeries


# 获取下跌相关系数_PIT -> getTechDdNcr


# 获取个股与市场相关系数_PIT时间序列 -> getRiskHisRelationSeries


# 获取个股与市场相关系数_PIT -> getRiskHisRelation


# 获取可决系数时间序列 -> getRiskR2Series


# 获取可决系数 -> getRiskR2


# 获取收益标准差时间序列 -> getRiskStDevSeries


# 获取收益标准差 -> getRiskStDev


# 获取收益标准差(年化)时间序列 -> getRiskAnnUstDevSeries


# 获取收益标准差(年化) -> getRiskAnnUstDev


# 获取252日超额收益标准差_PIT时间序列 -> getRiskExStDev252Series


# 获取252日超额收益标准差_PIT -> getRiskExStDev252


# 获取下行标准差时间序列 -> getRiskDownsideStDevSeries


# 获取下行标准差 -> getRiskDownsideStDev


# 获取上行标准差时间序列 -> getRiskUpsideStDevSeries


# 获取上行标准差 -> getRiskUpsideStDev


# 获取下行风险时间序列 -> getRiskDownsideRiskSeries


# 获取下行风险 -> getRiskDownsideRisk


# 获取下行风险同类平均时间序列 -> getRiskSimLAvgDownsideRiskSeries


# 获取下行风险同类平均 -> getRiskSimLAvgDownsideRisk


# 获取区间胜率时间序列 -> getWinRatioSeries


# 获取区间胜率 -> getWinRatio


# 获取基金组合久期时间序列 -> getRiskDurationSeries


# 获取基金组合久期 -> getRiskDuration


# 获取市场利率敏感性时间序列 -> getRiskInterestSensitivitySeries


# 获取市场利率敏感性 -> getRiskInterestSensitivity


# 获取选时能力时间序列 -> getRiskTimeSeries


# 获取选时能力 -> getRiskTime


# 获取选股能力时间序列 -> getRiskStockSeries


# 获取选股能力 -> getRiskStock


# 获取跟踪误差时间序列 -> getRiskTrackErrorSeries


# 获取跟踪误差 -> getRiskTrackError


# 获取跟踪误差(跟踪指数)时间序列 -> getRiskTrackErrorTrackIndexSeries


# 获取跟踪误差(跟踪指数) -> getRiskTrackErrorTrackIndex


# 获取跟踪误差(年化)时间序列 -> getRiskAnNuTrackErrorSeries


# 获取跟踪误差(年化) -> getRiskAnNuTrackError


# 获取信息比率时间序列 -> getRiskInfoRatioSeries


# 获取信息比率 -> getRiskInfoRatio


# 获取信息比率(年化)时间序列 -> getRiskAnNuInfoRatioSeries


# 获取信息比率(年化) -> getRiskAnNuInfoRatio


# 获取风格系数时间序列 -> getStyleStyleCoefficientSeries


# 获取风格系数 -> getStyleStyleCoefficient


# 获取风格属性时间序列 -> getStyleStyleAttributeSeries


# 获取风格属性 -> getStyleStyleAttribute


# 获取市值-风格属性时间序列 -> getStyleMarketValueStyleAttributeSeries


# 获取市值-风格属性 -> getStyleMarketValueStyleAttribute


# 获取市值属性时间序列 -> getStyleMarketValueAttributeSeries


# 获取市值属性 -> getStyleMarketValueAttribute


# 获取平均持仓时间时间序列 -> getStyleAveragePositionTimeSeries


# 获取平均持仓时间 -> getStyleAveragePositionTime


# 获取平均持仓时间(半年)时间序列 -> getStyleHyAveragePositionTimeSeries


# 获取平均持仓时间(半年) -> getStyleHyAveragePositionTime


# 获取投资集中度时间序列 -> getStyleInvConcentrationSeries


# 获取投资集中度 -> getStyleInvConcentration


# 获取佣金规模比时间序列 -> getStyleComMisAccountSeries


# 获取佣金规模比 -> getStyleComMisAccount


# 获取最高单月回报时间序列 -> getAbsoluteHighestMonthlyReturnSeries


# 获取最高单月回报 -> getAbsoluteHighestMonthlyReturn


# 获取最低单月回报时间序列 -> getAbsoluteLowestMonthlyReturnSeries


# 获取最低单月回报 -> getAbsoluteLowestMonthlyReturn


# 获取最低单月回报同类平均时间序列 -> getAbsoluteSimLAvgLowestMonthlyReturnSeries


# 获取最低单月回报同类平均 -> getAbsoluteSimLAvgLowestMonthlyReturn


# 获取连涨月数时间序列 -> getAbsoluteConUpsMonthSeries


# 获取连涨月数 -> getAbsoluteConUpsMonth


# 获取连跌月数时间序列 -> getAbsoluteCondOwnsMonthSeries


# 获取连跌月数 -> getAbsoluteCondOwnsMonth


# 获取最长连续上涨月数时间序列 -> getAbsoluteLongestConUpMonthSeries


# 获取最长连续上涨月数 -> getAbsoluteLongestConUpMonth


# 获取最长连续上涨整月涨幅时间序列 -> getAbsoluteMaxIncreaseOfUpMonthSeries


# 获取最长连续上涨整月涨幅 -> getAbsoluteMaxIncreaseOfUpMonth


# 获取最长连续下跌月数时间序列 -> getAbsoluteLongestConDownMonthSeries


# 获取最长连续下跌月数 -> getAbsoluteLongestConDownMonth


# 获取最长连续下跌整月跌幅时间序列 -> getAbsoluteMaxFallOfDownMonthSeries


# 获取最长连续下跌整月跌幅 -> getAbsoluteMaxFallOfDownMonth


# 获取上涨/下跌月数比时间序列 -> getAbsoluteUpDownMonthRatioSeries


# 获取上涨/下跌月数比 -> getAbsoluteUpDownMonthRatio


# 获取盈利百分比时间序列 -> getAbsoluteProfitMonthPerSeries


# 获取盈利百分比 -> getAbsoluteProfitMonthPer


# 获取区间盈利百分比时间序列 -> getAbsoluteProfitPerSeries


# 获取区间盈利百分比 -> getAbsoluteProfitPer


# 获取平均收益时间序列 -> getAbsoluteAvgIncomeSeries


# 获取平均收益 -> getAbsoluteAvgIncome


# 获取5年平均收益市值比_PIT时间序列 -> getFaPtToMvAvg5YSeries


# 获取5年平均收益市值比_PIT -> getFaPtToMvAvg5Y


# 获取平均损失时间序列 -> getAbsoluteAvgLossSeries


# 获取平均损失 -> getAbsoluteAvgLoss


# 获取参数平均损失值ES时间序列 -> getRiskEspaRamSeries


# 获取参数平均损失值ES -> getRiskEspaRam


# 获取历史平均损失值ES时间序列 -> getRiskEsHistoricalSeries


# 获取历史平均损失值ES -> getRiskEsHistorical


# 获取月度复合回报时间序列 -> getAbsoluteMonthlyCompositeReturnSeries


# 获取月度复合回报 -> getAbsoluteMonthlyCompositeReturn


# 获取平均月度回报时间序列 -> getAbsoluteAvgMonthlyReturnSeries


# 获取平均月度回报 -> getAbsoluteAvgMonthlyReturn


# 获取最高季度回报时间序列 -> getAbsoluteHighestQuatreTurnSeries


# 获取最高季度回报 -> getAbsoluteHighestQuatreTurn


# 获取最低季度回报时间序列 -> getAbsoluteLowestQuatreTurnSeries


# 获取最低季度回报 -> getAbsoluteLowestQuatreTurn


# 获取剩余折算天数时间序列 -> getFundDaysToConversionSeries


# 获取剩余折算天数 -> getFundDaysToConversion


# 获取分级基金收益分配方式时间序列 -> getAnalSMfEarningSeries


# 获取分级基金收益分配方式 -> getAnalSMfEarning


# 获取隐含收益率时间序列 -> getAnalImpliedYieldSeries


# 获取隐含收益率 -> getAnalImpliedYield


# 获取整体折溢价率时间序列 -> getAnalTDiscountRatioSeries


# 获取整体折溢价率 -> getAnalTDiscountRatio


# 获取折溢价比率偏离系数时间序列 -> getAnalDIsRatioDeviSeries


# 获取折溢价比率偏离系数 -> getAnalDIsRatioDevi


# 获取净值杠杆时间序列 -> getAnalNavLeverSeries


# 获取净值杠杆 -> getAnalNavLever


# 获取价格杠杆时间序列 -> getAnalPriceLeverSeries


# 获取价格杠杆 -> getAnalPriceLever


# 获取名义资金成本时间序列 -> getAnalSmFbNamedCostSeries


# 获取名义资金成本 -> getAnalSmFbNamedCost


# 获取实际资金成本时间序列 -> getAnalSmFbFactualCostSeries


# 获取实际资金成本 -> getAnalSmFbFactualCost


# 获取下一定期折算日时间序列 -> getAnalNextDiscountDateSeries


# 获取下一定期折算日 -> getAnalNextDiscountDate


# 获取本期约定年收益率时间序列 -> getFundAgreedAnNuYieldSeries


# 获取本期约定年收益率 -> getFundAgreedAnNuYield


# 获取下期约定年收益率时间序列 -> getAnalNextAAYieldSeries


# 获取下期约定年收益率 -> getAnalNextAAYield


# 获取上折阈值时间序列 -> getAnalUpDiscountThresholdSeries


# 获取上折阈值 -> getAnalUpDiscountThreshold


# 获取下折阈值时间序列 -> getAnalDownDiscountThresholdSeries


# 获取下折阈值 -> getAnalDownDiscountThreshold


# 获取上折母基金需涨时间序列 -> getAnalUpDiscountPctChangeSeries


# 获取上折母基金需涨 -> getAnalUpDiscountPctChange


# 获取下折母基金需跌时间序列 -> getAnalDownDiscountPctChangeSeries


# 获取下折母基金需跌 -> getAnalDownDiscountPctChange


# 获取持买单量时间序列 -> getOiLoiSeries


# 获取持买单量 -> getOiLoi


# 获取持买单量(品种)时间序列 -> getOiLvOiSeries


# 获取持买单量(品种) -> getOiLvOi


# 获取持买单量进榜会员名称时间序列 -> getOiLNameSeries


# 获取持买单量进榜会员名称 -> getOiLName


# 获取持买单量(品种)会员名称时间序列 -> getOiLvNameSeries


# 获取持买单量(品种)会员名称 -> getOiLvName


# 获取持卖单量时间序列 -> getOiSoISeries


# 获取持卖单量 -> getOiSoI


# 获取持卖单量(品种)时间序列 -> getOiSvOiSeries


# 获取持卖单量(品种) -> getOiSvOi


# 获取持卖单量进榜会员名称时间序列 -> getOiSNameSeries


# 获取持卖单量进榜会员名称 -> getOiSName


# 获取持卖单量(品种)会员名称时间序列 -> getOiSvNameSeries


# 获取持卖单量(品种)会员名称 -> getOiSvName


# 获取净持仓(品种)时间序列 -> getOiNvOiSeries


# 获取净持仓(品种) -> getOiNvOi


# 获取每股营业总收入时间序列 -> getGrpSSeries


# 获取每股营业总收入 -> getGrpS


# 获取每股营业总收入_GSD时间序列 -> getWgsDGrpS2Series


# 获取每股营业总收入_GSD -> getWgsDGrpS2


# 获取每股营业总收入_PIT时间序列 -> getFaGrpSSeries


# 获取每股营业总收入_PIT -> getFaGrpS


# 获取每股营业收入(TTM)_PIT时间序列 -> getOrPsTtMSeries


# 获取每股营业收入(TTM)_PIT -> getOrPsTtM


# 获取每股营业收入时间序列 -> getOrPsSeries


# 获取每股营业收入 -> getOrPs


# 获取每股营业收入_GSD时间序列 -> getWgsDOrPsSeries


# 获取每股营业收入_GSD -> getWgsDOrPs


# 获取每股营业收入_PIT时间序列 -> getFaOrPsSeries


# 获取每股营业收入_PIT -> getFaOrPs


# 获取每股资本公积时间序列 -> getSurplusCapitalPsSeries


# 获取每股资本公积 -> getSurplusCapitalPs


# 获取每股资本公积_PIT时间序列 -> getFaCapSurPpSSeries


# 获取每股资本公积_PIT -> getFaCapSurPpS


# 获取每股盈余公积时间序列 -> getSurplusReservePsSeries


# 获取每股盈余公积 -> getSurplusReservePs


# 获取每股盈余公积_PIT时间序列 -> getFaSppSSeries


# 获取每股盈余公积_PIT -> getFaSppS


# 获取每股未分配利润时间序列 -> getUnDistributedPsSeries


# 获取每股未分配利润 -> getUnDistributedPs


# 获取每股未分配利润_PIT时间序列 -> getFaUnDistributedPsSeries


# 获取每股未分配利润_PIT -> getFaUnDistributedPs


# 获取每股留存收益时间序列 -> getRetainedPsSeries


# 获取每股留存收益 -> getRetainedPs


# 获取每股留存收益_GSD时间序列 -> getWgsDRetainedPs2Series


# 获取每股留存收益_GSD -> getWgsDRetainedPs2


# 获取每股留存收益_PIT时间序列 -> getFaRetainedPsSeries


# 获取每股留存收益_PIT -> getFaRetainedPs


# 获取每股息税前利润时间序列 -> getEbItPsSeries


# 获取每股息税前利润 -> getEbItPs


# 获取每股息税前利润_GSD时间序列 -> getWgsDEbItPs2Series


# 获取每股息税前利润_GSD -> getWgsDEbItPs2


# 获取年化净资产收益率时间序列 -> getRoeYearlySeries


# 获取年化净资产收益率 -> getRoeYearly


# 获取年化总资产报酬率时间序列 -> getRoa2YearlySeries


# 获取年化总资产报酬率 -> getRoa2Yearly


# 获取年化总资产净利率时间序列 -> getRoaYearlySeries


# 获取年化总资产净利率 -> getRoaYearly


# 获取销售净利率时间序列 -> getNetProfitMarginSeries


# 获取销售净利率 -> getNetProfitMargin


# 获取销售净利率(TTM)时间序列 -> getNetProfitMarginTtM2Series


# 获取销售净利率(TTM) -> getNetProfitMarginTtM2


# 获取销售净利率_GSD时间序列 -> getWgsDNetProfitMarginSeries


# 获取销售净利率_GSD -> getWgsDNetProfitMargin


# 获取销售净利率(TTM)_GSD时间序列 -> getNetProfitMarginTtM3Series


# 获取销售净利率(TTM)_GSD -> getNetProfitMarginTtM3


# 获取销售净利率(TTM)_PIT时间序列 -> getFaNetProfitMarginTtMSeries


# 获取销售净利率(TTM)_PIT -> getFaNetProfitMarginTtM


# 获取销售净利率(TTM,只有最新数据)时间序列 -> getNetProfitMarginTtMSeries


# 获取销售净利率(TTM,只有最新数据) -> getNetProfitMarginTtM


# 获取扣非后销售净利率时间序列 -> getNetProfitMarginDeductedSeries


# 获取扣非后销售净利率 -> getNetProfitMarginDeducted


# 获取单季度.销售净利率时间序列 -> getQfaNetProfitMarginSeries


# 获取单季度.销售净利率 -> getQfaNetProfitMargin


# 获取单季度.销售净利率_GSD时间序列 -> getWgsDQfaNetProfitMarginSeries


# 获取单季度.销售净利率_GSD -> getWgsDQfaNetProfitMargin


# 获取销售毛利率时间序列 -> getGrossProfitMarginSeries


# 获取销售毛利率 -> getGrossProfitMargin


# 获取销售毛利率(TTM)时间序列 -> getGrossProfitMarginTtM2Series


# 获取销售毛利率(TTM) -> getGrossProfitMarginTtM2


# 获取销售毛利率_GSD时间序列 -> getWgsDGrossProfitMarginSeries


# 获取销售毛利率_GSD -> getWgsDGrossProfitMargin


# 获取销售毛利率(TTM)_GSD时间序列 -> getGrossProfitMarginTtM3Series


# 获取销售毛利率(TTM)_GSD -> getGrossProfitMarginTtM3


# 获取销售毛利率(TTM)_PIT时间序列 -> getFaGrossProfitMarginTtMSeries


# 获取销售毛利率(TTM)_PIT -> getFaGrossProfitMarginTtM


# 获取销售毛利率(TTM,只有最新数据)时间序列 -> getGrossProfitMarginTtMSeries


# 获取销售毛利率(TTM,只有最新数据) -> getGrossProfitMarginTtM


# 获取预测销售毛利率(GM)平均值(可选类型)时间序列 -> getWestAvgGmSeries


# 获取预测销售毛利率(GM)平均值(可选类型) -> getWestAvgGm


# 获取预测销售毛利率(GM)最大值(可选类型)时间序列 -> getWestMaxGmSeries


# 获取预测销售毛利率(GM)最大值(可选类型) -> getWestMaxGm


# 获取预测销售毛利率(GM)最小值(可选类型)时间序列 -> getWestMingMSeries


# 获取预测销售毛利率(GM)最小值(可选类型) -> getWestMingM


# 获取预测销售毛利率(GM)中值(可选类型)时间序列 -> getWestMediaGmSeries


# 获取预测销售毛利率(GM)中值(可选类型) -> getWestMediaGm


# 获取预测销售毛利率(GM)标准差值(可选类型)时间序列 -> getWestStdGmSeries


# 获取预测销售毛利率(GM)标准差值(可选类型) -> getWestStdGm


# 获取单季度.销售毛利率时间序列 -> getQfaGrossProfitMarginSeries


# 获取单季度.销售毛利率 -> getQfaGrossProfitMargin


# 获取单季度.销售毛利率_GSD时间序列 -> getWgsDQfaGrossProfitMarginSeries


# 获取单季度.销售毛利率_GSD -> getWgsDQfaGrossProfitMargin


# 获取销售成本率时间序列 -> getCogsToSalesSeries


# 获取销售成本率 -> getCogsToSales


# 获取销售成本率_GSD时间序列 -> getWgsDCogsToSalesSeries


# 获取销售成本率_GSD -> getWgsDCogsToSales


# 获取销售成本率(TTM)_PIT时间序列 -> getFaSalesToCostTtMSeries


# 获取销售成本率(TTM)_PIT -> getFaSalesToCostTtM


# 获取成本费用利润率时间序列 -> getNpToCostExpenseSeries


# 获取成本费用利润率 -> getNpToCostExpense


# 获取成本费用利润率(TTM)_PIT时间序列 -> getFaProtoCostTtMSeries


# 获取成本费用利润率(TTM)_PIT -> getFaProtoCostTtM


# 获取单季度.成本费用利润率时间序列 -> getNpToCostExpenseQfaSeries


# 获取单季度.成本费用利润率 -> getNpToCostExpenseQfa


# 获取销售期间费用率时间序列 -> getExpenseToSalesSeries


# 获取销售期间费用率 -> getExpenseToSales


# 获取销售期间费用率(TTM)时间序列 -> getExpenseToSalesTtM2Series


# 获取销售期间费用率(TTM) -> getExpenseToSalesTtM2


# 获取销售期间费用率(TTM)_GSD时间序列 -> getExpenseToSalesTtM3Series


# 获取销售期间费用率(TTM)_GSD -> getExpenseToSalesTtM3


# 获取销售期间费用率(TTM)_PIT时间序列 -> getFaExpenseToSalesTtMSeries


# 获取销售期间费用率(TTM)_PIT -> getFaExpenseToSalesTtM


# 获取销售期间费用率(TTM,只有最新数据)时间序列 -> getExpenseToSalesTtMSeries


# 获取销售期间费用率(TTM,只有最新数据) -> getExpenseToSalesTtM


# 获取主营业务比率时间序列 -> getOpToEBTSeries


# 获取主营业务比率 -> getOpToEBT


# 获取单季度.主营业务比率时间序列 -> getOpToEBTQfaSeries


# 获取单季度.主营业务比率 -> getOpToEBTQfa


# 获取净利润/营业总收入时间序列 -> getProfitToGrSeries


# 获取净利润/营业总收入 -> getProfitToGr


# 获取净利润/营业总收入(TTM)时间序列 -> getProfitToGrTtM2Series


# 获取净利润/营业总收入(TTM) -> getProfitToGrTtM2


# 获取净利润/营业总收入_GSD时间序列 -> getWgsDDupontNpToSalesSeries


# 获取净利润/营业总收入_GSD -> getWgsDDupontNpToSales


# 获取净利润/营业总收入(TTM)_GSD时间序列 -> getProfitToGrTtM3Series


# 获取净利润/营业总收入(TTM)_GSD -> getProfitToGrTtM3


# 获取净利润/营业总收入(TTM)_PIT时间序列 -> getFaProfitToGrTtMSeries


# 获取净利润/营业总收入(TTM)_PIT -> getFaProfitToGrTtM


# 获取净利润/营业总收入(TTM,只有最新数据)时间序列 -> getProfitToGrTtMSeries


# 获取净利润/营业总收入(TTM,只有最新数据) -> getProfitToGrTtM


# 获取单季度.净利润/营业总收入时间序列 -> getQfaProfitToGrSeries


# 获取单季度.净利润/营业总收入 -> getQfaProfitToGr


# 获取营业利润/营业总收入时间序列 -> getOpToGrSeries


# 获取营业利润/营业总收入 -> getOpToGr


# 获取营业利润/营业总收入(TTM)时间序列 -> getOpToGrTtM2Series


# 获取营业利润/营业总收入(TTM) -> getOpToGrTtM2


# 获取营业利润/营业总收入_GSD时间序列 -> getWgsDOpToGrSeries


# 获取营业利润/营业总收入_GSD -> getWgsDOpToGr


# 获取营业利润/营业总收入(TTM)_GSD时间序列 -> getOpToGrTtM3Series


# 获取营业利润/营业总收入(TTM)_GSD -> getOpToGrTtM3


# 获取营业利润/营业总收入(TTM)_PIT时间序列 -> getFaOpToGrTtMSeries


# 获取营业利润/营业总收入(TTM)_PIT -> getFaOpToGrTtM


# 获取营业利润/营业总收入(TTM,只有最新数据)时间序列 -> getOpToGrTtMSeries


# 获取营业利润/营业总收入(TTM,只有最新数据) -> getOpToGrTtM


# 获取单季度.营业利润/营业总收入时间序列 -> getQfaOpToGrSeries


# 获取单季度.营业利润/营业总收入 -> getQfaOpToGr


# 获取息税前利润/营业总收入时间序列 -> getEbItToGrSeries


# 获取息税前利润/营业总收入 -> getEbItToGr


# 获取息税前利润/营业总收入_GSD时间序列 -> getWgsDDupontEbItToSalesSeries


# 获取息税前利润/营业总收入_GSD -> getWgsDDupontEbItToSales


# 获取息税前利润/营业总收入(TTM)_PIT时间序列 -> getFaEbItToGrTtMSeries


# 获取息税前利润/营业总收入(TTM)_PIT -> getFaEbItToGrTtM


# 获取营业总成本/营业总收入时间序列 -> getGcToGrSeries


# 获取营业总成本/营业总收入 -> getGcToGr


# 获取营业总成本/营业总收入(TTM)时间序列 -> getGcToGrTtM2Series


# 获取营业总成本/营业总收入(TTM) -> getGcToGrTtM2


# 获取营业总成本/营业总收入_GSD时间序列 -> getWgsDGcToGrSeries


# 获取营业总成本/营业总收入_GSD -> getWgsDGcToGr


# 获取营业总成本/营业总收入(TTM)_GSD时间序列 -> getGcToGrTtM3Series


# 获取营业总成本/营业总收入(TTM)_GSD -> getGcToGrTtM3


# 获取营业总成本/营业总收入(TTM)_PIT时间序列 -> getFaOctoGrTtMSeries


# 获取营业总成本/营业总收入(TTM)_PIT -> getFaOctoGrTtM


# 获取营业总成本/营业总收入(TTM,只有最新数据)时间序列 -> getGcToGrTtMSeries


# 获取营业总成本/营业总收入(TTM,只有最新数据) -> getGcToGrTtM


# 获取单季度.营业总成本/营业总收入时间序列 -> getQfaGcToGrSeries


# 获取单季度.营业总成本/营业总收入 -> getQfaGcToGr


# 获取销售费用/营业总收入时间序列 -> getOperateExpenseToGrSeries


# 获取销售费用/营业总收入 -> getOperateExpenseToGr


# 获取销售费用/营业总收入(TTM)时间序列 -> getOperateExpenseToGrTtM2Series


# 获取销售费用/营业总收入(TTM) -> getOperateExpenseToGrTtM2


# 获取销售费用/营业总收入_GSD时间序列 -> getWgsDOperateExpenseToGrSeries


# 获取销售费用/营业总收入_GSD -> getWgsDOperateExpenseToGr


# 获取销售费用/营业总收入(TTM)_GSD时间序列 -> getOperateExpenseToGrTtM3Series


# 获取销售费用/营业总收入(TTM)_GSD -> getOperateExpenseToGrTtM3


# 获取销售费用/营业总收入(TTM)_PIT时间序列 -> getFaSellExpenseToGrTtMSeries


# 获取销售费用/营业总收入(TTM)_PIT -> getFaSellExpenseToGrTtM


# 获取销售费用/营业总收入(TTM,只有最新数据)时间序列 -> getOperateExpenseToGrTtMSeries


# 获取销售费用/营业总收入(TTM,只有最新数据) -> getOperateExpenseToGrTtM


# 获取单季度.销售费用/营业总收入时间序列 -> getQfaSaleExpenseToGrSeries


# 获取单季度.销售费用/营业总收入 -> getQfaSaleExpenseToGr


# 获取管理费用/营业总收入时间序列 -> getAdminExpenseToGrSeries


# 获取管理费用/营业总收入 -> getAdminExpenseToGr


# 获取管理费用/营业总收入(TTM)时间序列 -> getAdminExpenseToGrTtM2Series


# 获取管理费用/营业总收入(TTM) -> getAdminExpenseToGrTtM2


# 获取管理费用/营业总收入_GSD时间序列 -> getWgsDAdminExpenseToGrSeries


# 获取管理费用/营业总收入_GSD -> getWgsDAdminExpenseToGr


# 获取管理费用/营业总收入(TTM)_GSD时间序列 -> getAdminExpenseToGrTtM3Series


# 获取管理费用/营业总收入(TTM)_GSD -> getAdminExpenseToGrTtM3


# 获取管理费用/营业总收入(TTM)_PIT时间序列 -> getFaAdminExpenseToGrTtMSeries


# 获取管理费用/营业总收入(TTM)_PIT -> getFaAdminExpenseToGrTtM


# 获取管理费用/营业总收入(TTM,只有最新数据)时间序列 -> getAdminExpenseToGrTtMSeries


# 获取管理费用/营业总收入(TTM,只有最新数据) -> getAdminExpenseToGrTtM


# 获取单季度.管理费用/营业总收入时间序列 -> getQfaAdminExpenseToGrSeries


# 获取单季度.管理费用/营业总收入 -> getQfaAdminExpenseToGr


# 获取财务费用/营业总收入时间序列 -> getFinaExpenseToGrSeries


# 获取财务费用/营业总收入 -> getFinaExpenseToGr


# 获取财务费用/营业总收入(TTM)时间序列 -> getFinaExpenseToGrTtM2Series


# 获取财务费用/营业总收入(TTM) -> getFinaExpenseToGrTtM2


# 获取财务费用/营业总收入_GSD时间序列 -> getWgsDFinaExpenseToGrSeries


# 获取财务费用/营业总收入_GSD -> getWgsDFinaExpenseToGr


# 获取财务费用/营业总收入(TTM)_GSD时间序列 -> getFinaExpenseToGrTtM3Series


# 获取财务费用/营业总收入(TTM)_GSD -> getFinaExpenseToGrTtM3


# 获取财务费用/营业总收入(TTM)_PIT时间序列 -> getFaFinaExpenseToGrTtMSeries


# 获取财务费用/营业总收入(TTM)_PIT -> getFaFinaExpenseToGrTtM


# 获取财务费用/营业总收入(TTM,只有最新数据)时间序列 -> getFinaExpenseToGrTtMSeries


# 获取财务费用/营业总收入(TTM,只有最新数据) -> getFinaExpenseToGrTtM


# 获取单季度.财务费用/营业总收入时间序列 -> getQfaFinaExpenseToGrSeries


# 获取单季度.财务费用/营业总收入 -> getQfaFinaExpenseToGr


# 获取经营活动净收益/利润总额时间序列 -> getOperateIncomeToEBTSeries


# 获取经营活动净收益/利润总额 -> getOperateIncomeToEBT


# 获取经营活动净收益/利润总额(TTM)时间序列 -> getOperateIncomeToEBTTtM2Series


# 获取经营活动净收益/利润总额(TTM) -> getOperateIncomeToEBTTtM2


# 获取经营活动净收益/利润总额_GSD时间序列 -> getWgsDOperateIncomeToEBTSeries


# 获取经营活动净收益/利润总额_GSD -> getWgsDOperateIncomeToEBT


# 获取经营活动净收益/利润总额(TTM)_GSD时间序列 -> getOperateIncomeToEBTTtM3Series


# 获取经营活动净收益/利润总额(TTM)_GSD -> getOperateIncomeToEBTTtM3


# 获取经营活动净收益/利润总额_PIT时间序列 -> getFaOperIncomeToPbtSeries


# 获取经营活动净收益/利润总额_PIT -> getFaOperIncomeToPbt


# 获取经营活动净收益/利润总额(TTM)_PIT时间序列 -> getFaOperIncomeToPbtTtMSeries


# 获取经营活动净收益/利润总额(TTM)_PIT -> getFaOperIncomeToPbtTtM


# 获取经营活动净收益/利润总额(TTM,只有最新数据)时间序列 -> getOperateIncomeToEBTTtMSeries


# 获取经营活动净收益/利润总额(TTM,只有最新数据) -> getOperateIncomeToEBTTtM


# 获取单季度.经营活动净收益/利润总额时间序列 -> getQfaOperateIncomeToEBTSeries


# 获取单季度.经营活动净收益/利润总额 -> getQfaOperateIncomeToEBT


# 获取价值变动净收益/利润总额时间序列 -> getInvestIncomeToEBTSeries


# 获取价值变动净收益/利润总额 -> getInvestIncomeToEBT


# 获取价值变动净收益/利润总额(TTM)时间序列 -> getInvestIncomeToEBTTtM2Series


# 获取价值变动净收益/利润总额(TTM) -> getInvestIncomeToEBTTtM2


# 获取价值变动净收益/利润总额_GSD时间序列 -> getWgsDInvestIncomeToEBTSeries


# 获取价值变动净收益/利润总额_GSD -> getWgsDInvestIncomeToEBT


# 获取价值变动净收益/利润总额(TTM)_GSD时间序列 -> getInvestIncomeToEBTTtM3Series


# 获取价值变动净收益/利润总额(TTM)_GSD -> getInvestIncomeToEBTTtM3


# 获取价值变动净收益/利润总额(TTM)_PIT时间序列 -> getFaChgValueToPbtTtMSeries


# 获取价值变动净收益/利润总额(TTM)_PIT -> getFaChgValueToPbtTtM


# 获取价值变动净收益/利润总额(TTM,只有最新数据)时间序列 -> getInvestIncomeToEBTTtMSeries


# 获取价值变动净收益/利润总额(TTM,只有最新数据) -> getInvestIncomeToEBTTtM


# 获取单季度.价值变动净收益/利润总额时间序列 -> getQfaInvestIncomeToEBTSeries


# 获取单季度.价值变动净收益/利润总额 -> getQfaInvestIncomeToEBT


# 获取营业外收支净额/利润总额时间序列 -> getNonOperateProfitToEBTSeries


# 获取营业外收支净额/利润总额 -> getNonOperateProfitToEBT


# 获取营业外收支净额/利润总额(TTM)时间序列 -> getNonOperateProfitToEBTTtM2Series


# 获取营业外收支净额/利润总额(TTM) -> getNonOperateProfitToEBTTtM2


# 获取营业外收支净额/利润总额_GSD时间序列 -> getWgsDNonOperateProfitToEBTSeries


# 获取营业外收支净额/利润总额_GSD -> getWgsDNonOperateProfitToEBT


# 获取营业外收支净额/利润总额(TTM)_GSD时间序列 -> getNonOperateProfitToEBTTtM3Series


# 获取营业外收支净额/利润总额(TTM)_GSD -> getNonOperateProfitToEBTTtM3


# 获取营业外收支净额/利润总额(TTM)_PIT时间序列 -> getFaNonOperProfitToPbtTtMSeries


# 获取营业外收支净额/利润总额(TTM)_PIT -> getFaNonOperProfitToPbtTtM


# 获取营业外收支净额/利润总额(TTM,只有最新数据)时间序列 -> getNonOperateProfitToEBTTtMSeries


# 获取营业外收支净额/利润总额(TTM,只有最新数据) -> getNonOperateProfitToEBTTtM


# 获取扣除非经常损益后的净利润/净利润时间序列 -> getDeductedProfitToProfitSeries


# 获取扣除非经常损益后的净利润/净利润 -> getDeductedProfitToProfit


# 获取扣除非经常损益后的净利润/净利润_GSD时间序列 -> getWgsDDeductedProfitToProfitSeries


# 获取扣除非经常损益后的净利润/净利润_GSD -> getWgsDDeductedProfitToProfit


# 获取单季度.扣除非经常损益后的净利润/净利润时间序列 -> getQfaDeductedProfitToProfitSeries


# 获取单季度.扣除非经常损益后的净利润/净利润 -> getQfaDeductedProfitToProfit


# 获取销售商品提供劳务收到的现金/营业收入时间序列 -> getSalesCashIntoOrSeries


# 获取销售商品提供劳务收到的现金/营业收入 -> getSalesCashIntoOr


# 获取销售商品提供劳务收到的现金/营业收入(TTM)时间序列 -> getSalesCashIntoOrTtM2Series


# 获取销售商品提供劳务收到的现金/营业收入(TTM) -> getSalesCashIntoOrTtM2


# 获取销售商品提供劳务收到的现金/营业收入_PIT时间序列 -> getFaSalesCashToOrSeries


# 获取销售商品提供劳务收到的现金/营业收入_PIT -> getFaSalesCashToOr


# 获取销售商品提供劳务收到的现金/营业收入(TTM)_PIT时间序列 -> getFaSalesCashToOrTtMSeries


# 获取销售商品提供劳务收到的现金/营业收入(TTM)_PIT -> getFaSalesCashToOrTtM


# 获取销售商品提供劳务收到的现金/营业收入(TTM,只有最新数据)时间序列 -> getSalesCashIntoOrTtMSeries


# 获取销售商品提供劳务收到的现金/营业收入(TTM,只有最新数据) -> getSalesCashIntoOrTtM


# 获取单季度.销售商品提供劳务收到的现金/营业收入时间序列 -> getQfaSalesCashIntoOrSeries


# 获取单季度.销售商品提供劳务收到的现金/营业收入 -> getQfaSalesCashIntoOr


# 获取净利润现金含量时间序列 -> getFaNetProfitCashCoverSeries


# 获取净利润现金含量 -> getFaNetProfitCashCover


# 获取资本支出/折旧和摊销时间序列 -> getCapitalizedTodaSeries


# 获取资本支出/折旧和摊销 -> getCapitalizedToda


# 获取资本支出/折旧和摊销_GSD时间序列 -> getWgsDCapitalizedTodaSeries


# 获取资本支出/折旧和摊销_GSD -> getWgsDCapitalizedToda


# 获取经营性现金净流量/营业总收入时间序列 -> getOCFToSalesSeries


# 获取经营性现金净流量/营业总收入 -> getOCFToSales


# 获取现金满足投资比率时间序列 -> getOCFToInvestStockDividendSeries


# 获取现金满足投资比率 -> getOCFToInvestStockDividend


# 获取现金营运指数时间序列 -> getOCFToOpSeries


# 获取现金营运指数 -> getOCFToOp


# 获取全部资产现金回收率时间序列 -> getOCFToAssetsSeries


# 获取全部资产现金回收率 -> getOCFToAssets


# 获取现金股利保障倍数时间序列 -> getOCFToDividendSeries


# 获取现金股利保障倍数 -> getOCFToDividend


# 获取现金股利保障倍数(TTM)_PIT时间序列 -> getFaCashDivCoverTtMSeries


# 获取现金股利保障倍数(TTM)_PIT -> getFaCashDivCoverTtM


# 获取资产负债率时间序列 -> getDebtToAssetsSeries


# 获取资产负债率 -> getDebtToAssets


# 获取资产负债率_GSD时间序列 -> getWgsDDebtToAssetsSeries


# 获取资产负债率_GSD -> getWgsDDebtToAssets


# 获取资产负债率_PIT时间序列 -> getFaDebtToAssetSeries


# 获取资产负债率_PIT -> getFaDebtToAsset


# 获取净资产负债率时间序列 -> getFaDebtToEqYSeries


# 获取净资产负债率 -> getFaDebtToEqY


# 获取剔除预收账款的资产负债率(公告值)_GSD时间序列 -> getWgsDAnnouncedDeductedDebtToAssetsSeries


# 获取剔除预收账款的资产负债率(公告值)_GSD -> getWgsDAnnouncedDeductedDebtToAssets


# 获取剔除预收款项后的资产负债率时间序列 -> getDeductedDebtToAssets2Series


# 获取剔除预收款项后的资产负债率 -> getDeductedDebtToAssets2


# 获取剔除预收款项后的资产负债率(公告口径)时间序列 -> getDeductedDebtToAssetsSeries


# 获取剔除预收款项后的资产负债率(公告口径) -> getDeductedDebtToAssets


# 获取剔除预收账款后的资产负债率_GSD时间序列 -> getWgsDDeductedDebtToAssetsSeries


# 获取剔除预收账款后的资产负债率_GSD -> getWgsDDeductedDebtToAssets


# 获取长期资本负债率时间序列 -> getLongDebtToLongCaptIAlSeries


# 获取长期资本负债率 -> getLongDebtToLongCaptIAl


# 获取长期资产适合率时间序列 -> getLongCapitalToInvestmentSeries


# 获取长期资产适合率 -> getLongCapitalToInvestment


# 获取权益乘数时间序列 -> getAssetsToEquitySeries


# 获取权益乘数 -> getAssetsToEquity


# 获取权益乘数_GSD时间序列 -> getWgsDAssetsToEquitySeries


# 获取权益乘数_GSD -> getWgsDAssetsToEquity


# 获取股东权益比时间序列 -> getEquityToAssetSeries


# 获取股东权益比 -> getEquityToAsset


# 获取股东权益比率_PIT时间序列 -> getFaEquityAssetRadioSeries


# 获取股东权益比率_PIT -> getFaEquityAssetRadio


# 获取流动资产/总资产时间序列 -> getCatoAssetsSeries


# 获取流动资产/总资产 -> getCatoAssets


# 获取流动资产/总资产_GSD时间序列 -> getWgsDCatoAssetsSeries


# 获取流动资产/总资产_GSD -> getWgsDCatoAssets


# 获取非流动资产/总资产时间序列 -> getNcaToAssetsSeries


# 获取非流动资产/总资产 -> getNcaToAssets


# 获取非流动资产/总资产_GSD时间序列 -> getWgsDNcaToAssetsSeries


# 获取非流动资产/总资产_GSD -> getWgsDNcaToAssets


# 获取流动负债权益比率时间序列 -> getCurrentDebtToEquitySeries


# 获取流动负债权益比率 -> getCurrentDebtToEquity


# 获取非流动负债权益比率时间序列 -> getLongDebtToEquitySeries


# 获取非流动负债权益比率 -> getLongDebtToEquity


# 获取有形资产/总资产时间序列 -> getTangibleAssetsToAssetsSeries


# 获取有形资产/总资产 -> getTangibleAssetsToAssets


# 获取有形资产/总资产_GSD时间序列 -> getWgsDTangibleAssetsToAssetsSeries


# 获取有形资产/总资产_GSD -> getWgsDTangibleAssetsToAssets


# 获取归属母公司股东的权益/全部投入资本时间序列 -> getEquityToTotalCapitalSeries


# 获取归属母公司股东的权益/全部投入资本 -> getEquityToTotalCapital


# 获取带息债务/全部投入资本时间序列 -> getIntDebtToTotalCapSeries


# 获取带息债务/全部投入资本 -> getIntDebtToTotalCap


# 获取带息债务/全部投入资本_GSD时间序列 -> getWgsDInterestDebtToTotalCapitalSeries


# 获取带息债务/全部投入资本_GSD -> getWgsDInterestDebtToTotalCapital


# 获取带息债务/全部投入资本_PIT时间序列 -> getFaInterestDebtToCapitalSeries


# 获取带息债务/全部投入资本_PIT -> getFaInterestDebtToCapital


# 获取流动负债/负债合计时间序列 -> getCurrentDebtToDebtSeries


# 获取流动负债/负债合计 -> getCurrentDebtToDebt


# 获取流动负债/负债合计_GSD时间序列 -> getWgsDCurrentDebtToDebtSeries


# 获取流动负债/负债合计_GSD -> getWgsDCurrentDebtToDebt


# 获取非流动负债/负债合计时间序列 -> getLongDebToDebtSeries


# 获取非流动负债/负债合计 -> getLongDebToDebt


# 获取非流动负债/负债合计_GSD时间序列 -> getWgsDLongDebToDebtSeries


# 获取非流动负债/负债合计_GSD -> getWgsDLongDebToDebt


# 获取资本固定化比率时间序列 -> getNcaToEquitySeries


# 获取资本固定化比率 -> getNcaToEquity


# 获取有息负债率时间序列 -> getIbDebtRatioSeries


# 获取有息负债率 -> getIbDebtRatio


# 获取流动比率时间序列 -> getCurrentSeries


# 获取流动比率 -> getCurrent


# 获取流动比率_GSD时间序列 -> getWgsDCurrentSeries


# 获取流动比率_GSD -> getWgsDCurrent


# 获取流动比率_PIT时间序列 -> getFaCurrentSeries


# 获取流动比率_PIT -> getFaCurrent


# 获取速动比率时间序列 -> getQuickSeries


# 获取速动比率 -> getQuick


# 获取速动比率_GSD时间序列 -> getWgsDQuickSeries


# 获取速动比率_GSD -> getWgsDQuick


# 获取速动比率_PIT时间序列 -> getFaQuickSeries


# 获取速动比率_PIT -> getFaQuick


# 获取超速动比率_PIT时间序列 -> getFaSuperQuickSeries


# 获取超速动比率_PIT -> getFaSuperQuick


# 获取保守速动比率时间序列 -> getCashRatioSeries


# 获取保守速动比率 -> getCashRatio


# 获取保守速动比率_GSD时间序列 -> getWgsDCashRatioSeries


# 获取保守速动比率_GSD -> getWgsDCashRatio


# 获取现金比率时间序列 -> getCashToCurrentDebtSeries


# 获取现金比率 -> getCashToCurrentDebt


# 获取现金到期债务比时间序列 -> getOCFToQuickDebtSeries


# 获取现金到期债务比 -> getOCFToQuickDebt


# 获取产权比率时间序列 -> getDebtToEquitySeries


# 获取产权比率 -> getDebtToEquity


# 获取产权比率_GSD时间序列 -> getWgsDDebtToEquitySeries


# 获取产权比率_GSD -> getWgsDDebtToEquity


# 获取产权比率_PIT时间序列 -> getFaDebtToEquitySeries


# 获取产权比率_PIT -> getFaDebtToEquity


# 获取净负债率时间序列 -> getFaNetDebtRatioSeries


# 获取净负债率 -> getFaNetDebtRatio


# 获取净负债率_GSD时间序列 -> getWgsDNetDebtRatioSeries


# 获取净负债率_GSD -> getWgsDNetDebtRatio


# 获取净负债率(公告值)_GSD时间序列 -> getWgsDNetDebtRatioArdSeries


# 获取净负债率(公告值)_GSD -> getWgsDNetDebtRatioArd


# 获取归属母公司股东的权益/负债合计时间序列 -> getEquityToDebtSeries


# 获取归属母公司股东的权益/负债合计 -> getEquityToDebt


# 获取归属母公司股东的权益/负债合计_GSD时间序列 -> getWgsDEquityToDebtSeries


# 获取归属母公司股东的权益/负债合计_GSD -> getWgsDEquityToDebt


# 获取归属母公司股东的权益/带息债务时间序列 -> getEquityToInterestDebtSeries


# 获取归属母公司股东的权益/带息债务 -> getEquityToInterestDebt


# 获取归属母公司股东的权益/带息债务_GSD时间序列 -> getWgsDEquityToInterestDebtSeries


# 获取归属母公司股东的权益/带息债务_GSD -> getWgsDEquityToInterestDebt


# 获取归属母公司股东的权益/带息债务_PIT时间序列 -> getFaEquityToInterestDebtSeries


# 获取归属母公司股东的权益/带息债务_PIT -> getFaEquityToInterestDebt


# 获取有形资产/负债合计时间序列 -> getTangibleAssetToDebtSeries


# 获取有形资产/负债合计 -> getTangibleAssetToDebt


# 获取有形资产/负债合计_GSD时间序列 -> getWgsDTangibleAssetToDebtSeries


# 获取有形资产/负债合计_GSD -> getWgsDTangibleAssetToDebt


# 获取有形资产/带息债务时间序列 -> getTangAssetToIntDebtSeries


# 获取有形资产/带息债务 -> getTangAssetToIntDebt


# 获取有形资产/带息债务_GSD时间序列 -> getWgsDTangibleAssetToInterestDebtSeries


# 获取有形资产/带息债务_GSD -> getWgsDTangibleAssetToInterestDebt


# 获取有形资产/净债务时间序列 -> getTangibleAssetToNetDebtSeries


# 获取有形资产/净债务 -> getTangibleAssetToNetDebt


# 获取有形资产/净债务_GSD时间序列 -> getWgsDTangibleAssetToNetDebtSeries


# 获取有形资产/净债务_GSD -> getWgsDTangibleAssetToNetDebt


# 获取有形净值债务率时间序列 -> getDebtToTangibleEquitySeries


# 获取有形净值债务率 -> getDebtToTangibleEquity


# 获取有形净值债务率_PIT时间序列 -> getFaDebtToTangibleAFyBlSeries


# 获取有形净值债务率_PIT -> getFaDebtToTangibleAFyBl


# 获取息税折旧摊销前利润/负债合计时间序列 -> getEbItDatoDebtSeries


# 获取息税折旧摊销前利润/负债合计 -> getEbItDatoDebt


# 获取息税折旧摊销前利润/负债合计_GSD时间序列 -> getWgsDEbItDatoDebtSeries


# 获取息税折旧摊销前利润/负债合计_GSD -> getWgsDEbItDatoDebt


# 获取非筹资性现金净流量与流动负债的比率时间序列 -> getOcFicFToCurrentDebtSeries


# 获取非筹资性现金净流量与流动负债的比率 -> getOcFicFToCurrentDebt


# 获取非筹资性现金净流量与负债总额的比率时间序列 -> getOcFicFToDebtSeries


# 获取非筹资性现金净流量与负债总额的比率 -> getOcFicFToDebt


# 获取长期债务与营运资金比率时间序列 -> getLongDebtToWorkingCapitalSeries


# 获取长期债务与营运资金比率 -> getLongDebtToWorkingCapital


# 获取长期债务与营运资金比率_GSD时间序列 -> getWgsDLongDebtToWorkingCapitalSeries


# 获取长期债务与营运资金比率_GSD -> getWgsDLongDebtToWorkingCapital


# 获取长期负债占比时间序列 -> getLongDebtToDebtSeries


# 获取长期负债占比 -> getLongDebtToDebt


# 获取净债务/股权价值时间序列 -> getNetDebtToEvSeries


# 获取净债务/股权价值 -> getNetDebtToEv


# 获取带息债务/股权价值时间序列 -> getInterestDebtToEvSeries


# 获取带息债务/股权价值 -> getInterestDebtToEv


# 获取营业周期时间序列 -> getTurnDaysSeries


# 获取营业周期 -> getTurnDays


# 获取营业周期_GSD时间序列 -> getWgsDTurnDaysSeries


# 获取营业周期_GSD -> getWgsDTurnDays


# 获取营业周期(TTM)_PIT时间序列 -> getFaTurnDaysTtMSeries


# 获取营业周期(TTM)_PIT -> getFaTurnDaysTtM


# 获取净营业周期时间序列 -> getNetTurnDaysSeries


# 获取净营业周期 -> getNetTurnDays


# 获取存货周转天数时间序列 -> getInvTurnDaysSeries


# 获取存货周转天数 -> getInvTurnDays


# 获取存货周转天数_GSD时间序列 -> getWgsDInvTurnDaysSeries


# 获取存货周转天数_GSD -> getWgsDInvTurnDays


# 获取存货周转天数(TTM)_PIT时间序列 -> getFaInvTurnDaysTtMSeries


# 获取存货周转天数(TTM)_PIT -> getFaInvTurnDaysTtM


# 获取应收账款周转天数时间序列 -> getArturNDaysSeries


# 获取应收账款周转天数 -> getArturNDays


# 获取应收账款周转天数_GSD时间序列 -> getWgsDArturNDaysSeries


# 获取应收账款周转天数_GSD -> getWgsDArturNDays


# 获取应收账款周转天数(TTM)_PIT时间序列 -> getFaArturNDaysTtMSeries


# 获取应收账款周转天数(TTM)_PIT -> getFaArturNDaysTtM


# 获取应付账款周转天数时间序列 -> getApTurnDaysSeries


# 获取应付账款周转天数 -> getApTurnDays


# 获取应付账款周转天数_GSD时间序列 -> getWgsDApTurnDaysSeries


# 获取应付账款周转天数_GSD -> getWgsDApTurnDays


# 获取应付账款周转天数(TTM)_PIT时间序列 -> getFaApTurnDaysTtMSeries


# 获取应付账款周转天数(TTM)_PIT -> getFaApTurnDaysTtM


# 获取存货周转率时间序列 -> getInvTurnSeries


# 获取存货周转率 -> getInvTurn


# 获取存货周转率_GSD时间序列 -> getWgsDInvTurnSeries


# 获取存货周转率_GSD -> getWgsDInvTurn


# 获取存货周转率(TTM)_PIT时间序列 -> getFaInvTurnTtMSeries


# 获取存货周转率(TTM)_PIT -> getFaInvTurnTtM


# 获取应收账款周转率时间序列 -> getArturNSeries


# 获取应收账款周转率 -> getArturN


# 获取应收账款周转率(含坏账准备)时间序列 -> getFaArturNReserveSeries


# 获取应收账款周转率(含坏账准备) -> getFaArturNReserve


# 获取应收账款周转率_GSD时间序列 -> getWgsDArturNSeries


# 获取应收账款周转率_GSD -> getWgsDArturN


# 获取应收账款周转率(TTM)_PIT时间序列 -> getFaArturNTtMSeries


# 获取应收账款周转率(TTM)_PIT -> getFaArturNTtM


# 获取应收账款及应收票据周转率时间序列 -> getFaArnRTurnSeries


# 获取应收账款及应收票据周转率 -> getFaArnRTurn


# 获取流动资产周转率时间序列 -> getCaTurnSeries


# 获取流动资产周转率 -> getCaTurn


# 获取流动资产周转率_GSD时间序列 -> getWgsDCaTurnSeries


# 获取流动资产周转率_GSD -> getWgsDCaTurn


# 获取流动资产周转率(TTM)_PIT时间序列 -> getFaCurRtAssetsTRateTtMSeries


# 获取流动资产周转率(TTM)_PIT -> getFaCurRtAssetsTRateTtM


# 获取非流动资产周转率时间序列 -> getNonCurrentAssetsTurnSeries


# 获取非流动资产周转率 -> getNonCurrentAssetsTurn


# 获取营运资本周转率时间序列 -> getOperateCaptIAlTurnSeries


# 获取营运资本周转率 -> getOperateCaptIAlTurn


# 获取固定资产周转率时间序列 -> getFaTurnSeries


# 获取固定资产周转率 -> getFaTurn


# 获取固定资产周转率_GSD时间序列 -> getWgsDFaTurnSeries


# 获取固定资产周转率_GSD -> getWgsDFaTurn


# 获取固定资产周转率(TTM)_PIT时间序列 -> getFaFaTurnTtMSeries


# 获取固定资产周转率(TTM)_PIT -> getFaFaTurnTtM


# 获取总资产周转率时间序列 -> getAssetsTurnSeries


# 获取总资产周转率 -> getAssetsTurn


# 获取总资产周转率(TTM)时间序列 -> getTurnoverTtMSeries


# 获取总资产周转率(TTM) -> getTurnoverTtM


# 获取总资产周转率_GSD时间序列 -> getWgsDAssetsTurnSeries


# 获取总资产周转率_GSD -> getWgsDAssetsTurn


# 获取总资产周转率(TTM)_PIT时间序列 -> getFaTaTurnTtMSeries


# 获取总资产周转率(TTM)_PIT -> getFaTaTurnTtM


# 获取应付账款周转率时间序列 -> getApTurnSeries


# 获取应付账款周转率 -> getApTurn


# 获取应付账款周转率_GSD时间序列 -> getWgsDApTurnSeries


# 获取应付账款周转率_GSD -> getWgsDApTurn


# 获取应付账款周转率(TTM)_PIT时间序列 -> getFaApTurnTtMSeries


# 获取应付账款周转率(TTM)_PIT -> getFaApTurnTtM


# 获取应付账款及应付票据周转率时间序列 -> getFaApNpTurnSeries


# 获取应付账款及应付票据周转率 -> getFaApNpTurn


# 获取现金周转率时间序列 -> getFaCashTurnRatioSeries


# 获取现金周转率 -> getFaCashTurnRatio


# 获取净利润(同比增长率)时间序列 -> getYoYProfitSeries


# 获取净利润(同比增长率) -> getYoYProfit


# 获取净资产(同比增长率)时间序列 -> getYoYEquitySeries


# 获取净资产(同比增长率) -> getYoYEquity


# 获取总负债(同比增长率)时间序列 -> getYoYDebtSeries


# 获取总负债(同比增长率) -> getYoYDebt


# 获取总资产(同比增长率)时间序列 -> getYoYAssetsSeries


# 获取总资产(同比增长率) -> getYoYAssets


# 获取营业收入(同比增长率)时间序列 -> getYoYOrSeries


# 获取营业收入(同比增长率) -> getYoYOr


# 获取营业利润(同比增长率)时间序列 -> getYoyoPSeries


# 获取营业利润(同比增长率) -> getYoyoP


# 获取营业利润(同比增长率)2时间序列 -> getYoyoP2Series


# 获取营业利润(同比增长率)2 -> getYoyoP2


# 获取利润总额(同比增长率)时间序列 -> getYOyEBTSeries


# 获取利润总额(同比增长率) -> getYOyEBT


# 获取营业收入(同比增长率)_GSD时间序列 -> getWgsDYoYOrSeries


# 获取营业收入(同比增长率)_GSD -> getWgsDYoYOr


# 获取营业利润(同比增长率)_GSD时间序列 -> getWgsDYoyoP2Series


# 获取营业利润(同比增长率)_GSD -> getWgsDYoyoP2


# 获取利润总额(同比增长率)_GSD时间序列 -> getWgsDYOyEBTSeries


# 获取利润总额(同比增长率)_GSD -> getWgsDYOyEBT


# 获取营业总收入(同比增长率)时间序列 -> getYoYTrSeries


# 获取营业总收入(同比增长率) -> getYoYTr


# 获取现金净流量(同比增长率)时间序列 -> getYoYCfSeries


# 获取现金净流量(同比增长率) -> getYoYCf


# 获取营业总收入(同比增长率)_GSD时间序列 -> getWgsDYoYTrSeries


# 获取营业总收入(同比增长率)_GSD -> getWgsDYoYTr


# 获取基本每股收益(同比增长率)时间序列 -> getYoYepsBasicSeries


# 获取基本每股收益(同比增长率) -> getYoYepsBasic


# 获取稀释每股收益(同比增长率)时间序列 -> getYoYepsDilutedSeries


# 获取稀释每股收益(同比增长率) -> getYoYepsDiluted


# 获取单季度.净利润同比增长率时间序列 -> getQfaYoYProfitSeries


# 获取单季度.净利润同比增长率 -> getQfaYoYProfit


# 获取基本每股收益(同比增长率)_GSD时间序列 -> getWgsDYoYepsBasicSeries


# 获取基本每股收益(同比增长率)_GSD -> getWgsDYoYepsBasic


# 获取稀释每股收益(同比增长率)_GSD时间序列 -> getWgsDYoYepsDilutedSeries


# 获取稀释每股收益(同比增长率)_GSD -> getWgsDYoYepsDiluted


# 获取单季度.营业收入同比增长率时间序列 -> getQfaYoYSalesSeries


# 获取单季度.营业收入同比增长率 -> getQfaYoYSales


# 获取单季度.营业利润同比增长率时间序列 -> getQfaYoyoPSeries


# 获取单季度.营业利润同比增长率 -> getQfaYoyoP


# 获取单季度.营业总收入同比增长率时间序列 -> getQfaYoYGrSeries


# 获取单季度.营业总收入同比增长率 -> getQfaYoYGr


# 获取单季度.每股收益(同比增长率)时间序列 -> getQfaYoYepsSeries


# 获取单季度.每股收益(同比增长率) -> getQfaYoYeps


# 获取单季度.现金净流量(同比增长率)时间序列 -> getQfaYoYCfSeries


# 获取单季度.现金净流量(同比增长率) -> getQfaYoYCf


# 获取净资产收益率(摊薄)(同比增长率)时间序列 -> getYoYRoeSeries


# 获取净资产收益率(摊薄)(同比增长率) -> getYoYRoe


# 获取净资产收益率(摊薄)(同比增长率)_GSD时间序列 -> getWgsDYoYRoeSeries


# 获取净资产收益率(摊薄)(同比增长率)_GSD -> getWgsDYoYRoe


# 获取归属母公司股东的净利润(同比增长率)时间序列 -> getYoYNetProfitSeries


# 获取归属母公司股东的净利润(同比增长率) -> getYoYNetProfit


# 获取归属母公司股东的净利润(同比增长率)_GSD时间序列 -> getWgsDYoYNetProfitSeries


# 获取归属母公司股东的净利润(同比增长率)_GSD -> getWgsDYoYNetProfit


# 获取单季度.经营性现金净流量(同比增长率)时间序列 -> getQfaYoyOCFSeries


# 获取单季度.经营性现金净流量(同比增长率) -> getQfaYoyOCF


# 获取单季度.归属母公司股东的净利润同比增长率时间序列 -> getQfaYoYNetProfitSeries


# 获取单季度.归属母公司股东的净利润同比增长率 -> getQfaYoYNetProfit


# 获取归属母公司股东的净利润-扣除非经常损益(同比增长率)时间序列 -> getYoYNetProfitDeductedSeries


# 获取归属母公司股东的净利润-扣除非经常损益(同比增长率) -> getYoYNetProfitDeducted


# 获取归属母公司股东的净利润-扣除非经常损益(同比增长率)_GSD时间序列 -> getWgsDYoYNetProfitDeductedSeries


# 获取归属母公司股东的净利润-扣除非经常损益(同比增长率)_GSD -> getWgsDYoYNetProfitDeducted


# 获取资产总计(相对年初增长率)_GSD时间序列 -> getWgsDYoYAssetsSeries


# 获取资产总计(相对年初增长率)_GSD -> getWgsDYoYAssets


# 获取每股净资产(相对年初增长率)时间序列 -> getYoYbPsSeries


# 获取每股净资产(相对年初增长率) -> getYoYbPs


# 获取每股净资产(相对年初增长率)_GSD时间序列 -> getWgsDYoYbPsSeries


# 获取每股净资产(相对年初增长率)_GSD -> getWgsDYoYbPs


# 获取归属母公司股东的权益(相对年初增长率)_GSD时间序列 -> getWgsDYoYEquitySeries


# 获取归属母公司股东的权益(相对年初增长率)_GSD -> getWgsDYoYEquity


# 获取归属母公司股东的净利润/净利润时间序列 -> getDupontNpSeries


# 获取归属母公司股东的净利润/净利润 -> getDupontNp


# 获取归属母公司股东的净利润/净利润_GSD时间序列 -> getWgsDDupontNpSeries


# 获取归属母公司股东的净利润/净利润_GSD -> getWgsDDupontNp


# 获取净利润/利润总额时间序列 -> getDupontTaxBurdenSeries


# 获取净利润/利润总额 -> getDupontTaxBurden


# 获取净利润/利润总额_GSD时间序列 -> getWgsDDupontTaxBurdenSeries


# 获取净利润/利润总额_GSD -> getWgsDDupontTaxBurden


# 获取利润总额/息税前利润时间序列 -> getDupontIntBurdenSeries


# 获取利润总额/息税前利润 -> getDupontIntBurden


# 获取利润总额/息税前利润_GSD时间序列 -> getWgsDDupontIntBurdenSeries


# 获取利润总额/息税前利润_GSD -> getWgsDDupontIntBurden


# 获取营运资本/总资产时间序列 -> getWorkingCapitalToAssetsSeries


# 获取营运资本/总资产 -> getWorkingCapitalToAssets


# 获取留存收益/总资产时间序列 -> getRetainedEarningsToAssetsSeries


# 获取留存收益/总资产 -> getRetainedEarningsToAssets


# 获取股东权益合计(含少数)/负债总计时间序列 -> getBookValueToDebtSeries


# 获取股东权益合计(含少数)/负债总计 -> getBookValueToDebt


# 获取营业收入/总资产时间序列 -> getRevenueToAssetsSeries


# 获取营业收入/总资产 -> getRevenueToAssets


# 获取逾期贷款_3个月以内时间序列 -> getStmNoteBank0001Series


# 获取逾期贷款_3个月以内 -> getStmNoteBank0001


# 获取逾期贷款_3个月至1年时间序列 -> getStmNoteBank0002Series


# 获取逾期贷款_3个月至1年 -> getStmNoteBank0002


# 获取逾期贷款_1年以上3年以内时间序列 -> getStmNoteBank0003Series


# 获取逾期贷款_1年以上3年以内 -> getStmNoteBank0003


# 获取逾期贷款_3年以上时间序列 -> getStmNoteBank0004Series


# 获取逾期贷款_3年以上 -> getStmNoteBank0004


# 获取逾期贷款合计时间序列 -> getStmNoteBank0005Series


# 获取逾期贷款合计 -> getStmNoteBank0005


# 获取主营业务收入时间序列 -> getStmNoteSeg1701Series


# 获取主营业务收入 -> getStmNoteSeg1701


# 获取主营业务成本时间序列 -> getStmNoteSeg1702Series


# 获取主营业务成本 -> getStmNoteSeg1702


# 获取资产管理业务收入时间序列 -> getStmNoteSec1543Series


# 获取资产管理业务收入 -> getStmNoteSec1543


# 获取资产管理业务净收入时间序列 -> getStmNoteSec1553Series


# 获取资产管理业务净收入 -> getStmNoteSec1553


# 获取资产管理费收入_GSD时间序列 -> getWgsDAumIncSeries


# 获取资产管理费收入_GSD -> getWgsDAumInc


# 获取定向资产管理业务收入时间序列 -> getStmNoteAssetManageIncDSeries


# 获取定向资产管理业务收入 -> getStmNoteAssetManageIncD


# 获取集合资产管理业务收入时间序列 -> getStmNoteAssetManageIncCSeries


# 获取集合资产管理业务收入 -> getStmNoteAssetManageIncC


# 获取专项资产管理业务收入时间序列 -> getStmNoteAssetManageIncSSeries


# 获取专项资产管理业务收入 -> getStmNoteAssetManageIncS


# 获取单季度.资产管理费收入_GSD时间序列 -> getWgsDQfaAumIncSeries


# 获取单季度.资产管理费收入_GSD -> getWgsDQfaAumInc


# 获取受托客户资产管理业务净收入时间序列 -> getNetIncCustomerAssetManagementBusinessSeries


# 获取受托客户资产管理业务净收入 -> getNetIncCustomerAssetManagementBusiness


# 获取单季度.受托客户资产管理业务净收入时间序列 -> getQfaNetIncCustomerAssetManagementBusinessSeries


# 获取单季度.受托客户资产管理业务净收入 -> getQfaNetIncCustomerAssetManagementBusiness


# 获取手续费及佣金收入:受托客户资产管理业务时间序列 -> getStmNoteSec1502Series


# 获取手续费及佣金收入:受托客户资产管理业务 -> getStmNoteSec1502


# 获取手续费及佣金净收入:受托客户资产管理业务时间序列 -> getStmNoteSec1522Series


# 获取手续费及佣金净收入:受托客户资产管理业务 -> getStmNoteSec1522


# 获取投资收益_FUND时间序列 -> getStmIs81Series


# 获取投资收益_FUND -> getStmIs81


# 获取净投资收益率时间序列 -> getStmNoteInSur5Series


# 获取净投资收益率 -> getStmNoteInSur5


# 获取总投资收益率时间序列 -> getStmNoteInSur6Series


# 获取总投资收益率 -> getStmNoteInSur6


# 获取净投资收益时间序列 -> getStmNoteInvestmentIncome0004Series


# 获取净投资收益 -> getStmNoteInvestmentIncome0004


# 获取总投资收益时间序列 -> getStmNoteInvestmentIncome0010Series


# 获取总投资收益 -> getStmNoteInvestmentIncome0010


# 获取其他投资收益时间序列 -> getStmNoteInvestmentIncome0009Series


# 获取其他投资收益 -> getStmNoteInvestmentIncome0009


# 获取取得投资收益收到的现金时间序列 -> getCashRecpReturnInvestSeries


# 获取取得投资收益收到的现金 -> getCashRecpReturnInvest


# 获取股票投资收益_FUND时间序列 -> getStmIs1Series


# 获取股票投资收益_FUND -> getStmIs1


# 获取基金投资收益_FUND时间序列 -> getStmIs75Series


# 获取基金投资收益_FUND -> getStmIs75


# 获取债券投资收益_FUND时间序列 -> getStmIs2Series


# 获取债券投资收益_FUND -> getStmIs2


# 获取权证投资收益_FUND时间序列 -> getStmIs201Series


# 获取权证投资收益_FUND -> getStmIs201


# 获取单季度.取得投资收益收到的现金时间序列 -> getQfaCashRecpReturnInvestSeries


# 获取单季度.取得投资收益收到的现金 -> getQfaCashRecpReturnInvest


# 获取资产支持证券投资收益_FUND时间序列 -> getStmIs71Series


# 获取资产支持证券投资收益_FUND -> getStmIs71


# 获取对联营企业和合营企业的投资收益时间序列 -> getIncInvestAsSocJVENtpSeries


# 获取对联营企业和合营企业的投资收益 -> getIncInvestAsSocJVENtp


# 获取单季度.对联营企业和合营企业的投资收益时间序列 -> getQfaIncInvestAsSocJVENtpSeries


# 获取单季度.对联营企业和合营企业的投资收益 -> getQfaIncInvestAsSocJVENtp


# 获取单季度.扣除非经常损益后的净利润时间序列 -> getQfaDeductedProfitSeries


# 获取单季度.扣除非经常损益后的净利润 -> getQfaDeductedProfit


# 获取单季度.经营活动净收益时间序列 -> getQfaOperateIncomeSeries


# 获取单季度.经营活动净收益 -> getQfaOperateIncome


# 获取单季度.价值变动净收益时间序列 -> getQfaInvestIncomeSeries


# 获取单季度.价值变动净收益 -> getQfaInvestIncome


# 获取单季度.净资产收益率(扣除非经常损益)时间序列 -> getQfaRoeDeductedSeries


# 获取单季度.净资产收益率(扣除非经常损益) -> getQfaRoeDeducted


# 获取单季度.营业总收入环比增长率时间序列 -> getQfaCGrGrSeries


# 获取单季度.营业总收入环比增长率 -> getQfaCGrGr


# 获取单季度.营业收入环比增长率时间序列 -> getQfaCGrSalesSeries


# 获取单季度.营业收入环比增长率 -> getQfaCGrSales


# 获取单季度.营业利润环比增长率时间序列 -> getQfaCGroPSeries


# 获取单季度.营业利润环比增长率 -> getQfaCGroP


# 获取单季度.净利润环比增长率时间序列 -> getQfaCGrProfitSeries


# 获取单季度.净利润环比增长率 -> getQfaCGrProfit


# 获取单季度.归属母公司股东的净利润环比增长率时间序列 -> getQfaCGrNetProfitSeries


# 获取单季度.归属母公司股东的净利润环比增长率 -> getQfaCGrNetProfit


# 获取人均创收时间序列 -> getWgsDRevenuePpSeries


# 获取人均创收 -> getWgsDRevenuePp


# 获取人均创利时间序列 -> getWgsDProfitPpSeries


# 获取人均创利 -> getWgsDProfitPp


# 获取人均薪酬时间序列 -> getWgsDSalaryPpSeries


# 获取人均薪酬 -> getWgsDSalaryPp


# 获取增长率-营业收入(TTM)_PIT时间序列 -> getFaOrGrTtMSeries


# 获取增长率-营业收入(TTM)_PIT -> getFaOrGrTtM


# 获取增长率-利润总额(TTM)_PIT时间序列 -> getFaTpGrTtMSeries


# 获取增长率-利润总额(TTM)_PIT -> getFaTpGrTtM


# 获取增长率-营业利润(TTM)_PIT时间序列 -> getFaOiGrTtMSeries


# 获取增长率-营业利润(TTM)_PIT -> getFaOiGrTtM


# 获取增长率-净利润(TTM)_PIT时间序列 -> getFaNpGrTtMSeries


# 获取增长率-净利润(TTM)_PIT -> getFaNpGrTtM


# 获取增长率-归属母公司股东的净利润(TTM)_PIT时间序列 -> getFaNppCGrTtMSeries


# 获取增长率-归属母公司股东的净利润(TTM)_PIT -> getFaNppCGrTtM


# 获取增长率-毛利率(TTM)_PIT时间序列 -> getFaGpmgRTtMSeries


# 获取增长率-毛利率(TTM)_PIT -> getFaGpmgRTtM


# 获取增长率-总资产_PIT时间序列 -> getFaTagRSeries


# 获取增长率-总资产_PIT -> getFaTagR


# 获取增长率-净资产_PIT时间序列 -> getFaNAgrSeries


# 获取增长率-净资产_PIT -> getFaNAgr


# 获取5年收益增长率_PIT时间序列 -> getFaEGroSeries


# 获取5年收益增长率_PIT -> getFaEGro


# 获取基金N日净值增长率时间序列 -> getNavReturnNdSeries


# 获取基金N日净值增长率 -> getNavReturnNd


# 获取净利润复合年增长率时间序列 -> getGrowthCAgrNetProfitSeries


# 获取净利润复合年增长率 -> getGrowthCAgrNetProfit


# 获取毛利(近1年增长率)_GSD时间序列 -> getWgsDGrowthGp1YSeries


# 获取毛利(近1年增长率)_GSD -> getWgsDGrowthGp1Y


# 获取毛利(近3年增长率)_GSD时间序列 -> getWgsDGrowthGp3YSeries


# 获取毛利(近3年增长率)_GSD -> getWgsDGrowthGp3Y


# 获取净利润复合年增长率_GSD时间序列 -> getWgsDCAgrNetProfitSeries


# 获取净利润复合年增长率_GSD -> getWgsDCAgrNetProfit


# 获取5年营业收入增长率_PIT时间序列 -> getFaSGroSeries


# 获取5年营业收入增长率_PIT -> getFaSGro


# 获取利润总额复合年增长率时间序列 -> getCAgrTotalProfitSeries


# 获取利润总额复合年增长率 -> getCAgrTotalProfit


# 获取净利润(N年,增长率)时间序列 -> getGrowthProfitSeries


# 获取净利润(N年,增长率) -> getGrowthProfit


# 获取净利润(近1年增长率)_GSD时间序列 -> getWgsDGrowthNp1YSeries


# 获取净利润(近1年增长率)_GSD -> getWgsDGrowthNp1Y


# 获取净利润(近3年增长率)_GSD时间序列 -> getWgsDGrowthNp3YSeries


# 获取净利润(近3年增长率)_GSD -> getWgsDGrowthNp3Y


# 获取总资产(近1年增长率)_GSD时间序列 -> getWgsDGrowthAsset1YSeries


# 获取总资产(近1年增长率)_GSD -> getWgsDGrowthAsset1Y


# 获取总资产(近3年增长率)_GSD时间序列 -> getWgsDGrowthAsset3YSeries


# 获取总资产(近3年增长率)_GSD -> getWgsDGrowthAsset3Y


# 获取总负债(近1年增长率)_GSD时间序列 -> getWgsDGrowthDebt1YSeries


# 获取总负债(近1年增长率)_GSD -> getWgsDGrowthDebt1Y


# 获取总负债(近3年增长率)_GSD时间序列 -> getWgsDGrowthDebt3YSeries


# 获取总负债(近3年增长率)_GSD -> getWgsDGrowthDebt3Y


# 获取利润总额复合年增长率_GSD时间序列 -> getWgsDCAgrTotalProfitSeries


# 获取利润总额复合年增长率_GSD -> getWgsDCAgrTotalProfit


# 获取近三年营收复合增长率时间序列 -> getIpoRevenueGrowthSeries


# 获取近三年营收复合增长率 -> getIpoRevenueGrowth


# 获取营业总收入复合年增长率时间序列 -> getGrowthCAgrTrSeries


# 获取营业总收入复合年增长率 -> getGrowthCAgrTr


# 获取营业收入(N年,增长率)时间序列 -> getGrowthOrSeries


# 获取营业收入(N年,增长率) -> getGrowthOr


# 获取营业利润(N年,增长率)时间序列 -> getGrowthOpSeries


# 获取营业利润(N年,增长率) -> getGrowthOp


# 获取利润总额(N年,增长率)时间序列 -> getGrowthEBtSeries


# 获取利润总额(N年,增长率) -> getGrowthEBt


# 获取资产总计(N年,增长率)时间序列 -> getGrowthAssetsSeries


# 获取资产总计(N年,增长率) -> getGrowthAssets


# 获取股东权益(N年,增长率)时间序列 -> getGrowthTotalEquitySeries


# 获取股东权益(N年,增长率) -> getGrowthTotalEquity


# 获取营业利润(近1年增长率)_GSD时间序列 -> getWgsDGrowthOp1YSeries


# 获取营业利润(近1年增长率)_GSD -> getWgsDGrowthOp1Y


# 获取营业利润(近3年增长率)_GSD时间序列 -> getWgsDGrowthOp3YSeries


# 获取营业利润(近3年增长率)_GSD -> getWgsDGrowthOp3Y


# 获取税前利润(近1年增长率)_GSD时间序列 -> getWgsDGrowthEBt1YSeries


# 获取税前利润(近1年增长率)_GSD -> getWgsDGrowthEBt1Y


# 获取税前利润(近3年增长率)_GSD时间序列 -> getWgsDGrowthEBt3YSeries


# 获取税前利润(近3年增长率)_GSD -> getWgsDGrowthEBt3Y


# 获取营业总收入复合年增长率_GSD时间序列 -> getWgsDCAgrTrSeries


# 获取营业总收入复合年增长率_GSD -> getWgsDCAgrTr


# 获取营业收入(N年,增长率)_GSD时间序列 -> getWgsDGrowthOrSeries


# 获取营业收入(N年,增长率)_GSD -> getWgsDGrowthOr


# 获取营业利润(N年,增长率)_GSD时间序列 -> getWgsDGrowthOpSeries


# 获取营业利润(N年,增长率)_GSD -> getWgsDGrowthOp


# 获取利润总额(N年,增长率)_GSD时间序列 -> getWgsDGrowthEBtSeries


# 获取利润总额(N年,增长率)_GSD -> getWgsDGrowthEBt


# 获取资产总计(N年,增长率)_GSD时间序列 -> getWgsDGrowthAssetsSeries


# 获取资产总计(N年,增长率)_GSD -> getWgsDGrowthAssets


# 获取股东权益(N年,增长率)_GSD时间序列 -> getWgsDGrowthTotalEquitySeries


# 获取股东权益(N年,增长率)_GSD -> getWgsDGrowthTotalEquity


# 获取营业总收入(N年,增长率)时间序列 -> getGrowthGrSeries


# 获取营业总收入(N年,增长率) -> getGrowthGr


# 获取营业总成本(N年,增长率)时间序列 -> getGrowthGcSeries


# 获取营业总成本(N年,增长率) -> getGrowthGc


# 获取销售利润率(N年,增长率)时间序列 -> getGrowthProfitToSalesSeries


# 获取销售利润率(N年,增长率) -> getGrowthProfitToSales


# 获取总营业收入(近1年增长率)_GSD时间序列 -> getWgsDGrowthSales1YSeries


# 获取总营业收入(近1年增长率)_GSD -> getWgsDGrowthSales1Y


# 获取总营业收入(近3年增长率)_GSD时间序列 -> getWgsDGrowthSales3YSeries


# 获取总营业收入(近3年增长率)_GSD -> getWgsDGrowthSales3Y


# 获取每股净资产(近1年增长率)_GSD时间序列 -> getWgsDGrowthBpS1YSeries


# 获取每股净资产(近1年增长率)_GSD -> getWgsDGrowthBpS1Y


# 获取每股净资产(近3年增长率)_GSD时间序列 -> getWgsDGrowthBpS3YSeries


# 获取每股净资产(近3年增长率)_GSD -> getWgsDGrowthBpS3Y


# 获取营业总收入(N年,增长率)_GSD时间序列 -> getWgsDGrowthGrSeries


# 获取营业总收入(N年,增长率)_GSD -> getWgsDGrowthGr


# 获取营业总成本(N年,增长率)_GSD时间序列 -> getWgsDGrowthGcSeries


# 获取营业总成本(N年,增长率)_GSD -> getWgsDGrowthGc


# 获取销售利润率(N年,增长率)_GSD时间序列 -> getWgsDGrowthProfitToSalesSeries


# 获取销售利润率(N年,增长率)_GSD -> getWgsDGrowthProfitToSales


# 获取净资产收益率(N年,增长率)时间序列 -> getGrowthRoeSeries


# 获取净资产收益率(N年,增长率) -> getGrowthRoe


# 获取股东权益合计(近1年增长率)_GSD时间序列 -> getWgsDGrowthTotalEquity1YSeries


# 获取股东权益合计(近1年增长率)_GSD -> getWgsDGrowthTotalEquity1Y


# 获取股东权益合计(近3年增长率)_GSD时间序列 -> getWgsDGrowthTotalEquity3YSeries


# 获取股东权益合计(近3年增长率)_GSD -> getWgsDGrowthTotalEquity3Y


# 获取基本每股收益(近1年增长率)_GSD时间序列 -> getWgsDGrowthEps1YSeries


# 获取基本每股收益(近1年增长率)_GSD -> getWgsDGrowthEps1Y


# 获取基本每股收益(近3年增长率)_GSD时间序列 -> getWgsDGrowthEps3YSeries


# 获取基本每股收益(近3年增长率)_GSD -> getWgsDGrowthEps3Y


# 获取净资产收益率(N年,增长率)_GSD时间序列 -> getWgsDGrowthRoeSeries


# 获取净资产收益率(N年,增长率)_GSD -> getWgsDGrowthRoe


# 获取经营活动净收益(N年,增长率)时间序列 -> getGrowthOperateIncomeSeries


# 获取经营活动净收益(N年,增长率) -> getGrowthOperateIncome


# 获取价值变动净收益(N年,增长率)时间序列 -> getGrowthInvestIncomeSeries


# 获取价值变动净收益(N年,增长率) -> getGrowthInvestIncome


# 获取经营活动净收益(N年,增长率)_GSD时间序列 -> getWgsDGrowthOperateIncomeSeries


# 获取经营活动净收益(N年,增长率)_GSD -> getWgsDGrowthOperateIncome


# 获取价值变动净收益(N年,增长率)_GSD时间序列 -> getWgsDGrowthInvestIncomeSeries


# 获取价值变动净收益(N年,增长率)_GSD -> getWgsDGrowthInvestIncome


# 获取归属母公司股东的权益(N年,增长率)时间序列 -> getGrowthEquitySeries


# 获取归属母公司股东的权益(N年,增长率) -> getGrowthEquity


# 获取归属母公司股东的权益(近1年增长率)_GSD时间序列 -> getWgsDGrowthEquity1YSeries


# 获取归属母公司股东的权益(近1年增长率)_GSD -> getWgsDGrowthEquity1Y


# 获取归属母公司股东的权益(近3年增长率)_GSD时间序列 -> getWgsDGrowthEquity3YSeries


# 获取归属母公司股东的权益(近3年增长率)_GSD -> getWgsDGrowthEquity3Y


# 获取归属母公司股东的权益(N年,增长率)_GSD时间序列 -> getWgsDGrowthEquitySeries


# 获取归属母公司股东的权益(N年,增长率)_GSD -> getWgsDGrowthEquity


# 获取归属母公司股东的净利润(N年,增长率)时间序列 -> getGrowthNetProfitSeries


# 获取归属母公司股东的净利润(N年,增长率) -> getGrowthNetProfit


# 获取归属母公司股东的净利润(N年,增长率)_GSD时间序列 -> getWgsDGrowthNetProfitSeries


# 获取归属母公司股东的净利润(N年,增长率)_GSD -> getWgsDGrowthNetProfit


# 获取归属母公司股东的净利润-扣除非经常损益(N年,增长率)时间序列 -> getGrowthNetProfitDeductedSeries


# 获取归属母公司股东的净利润-扣除非经常损益(N年,增长率) -> getGrowthNetProfitDeducted


# 获取资产差额(特殊报表科目)时间序列 -> getAssetsGapSeries


# 获取资产差额(特殊报表科目) -> getAssetsGap


# 获取资产差额说明(特殊报表科目)时间序列 -> getAssetsGapDetailSeries


# 获取资产差额说明(特殊报表科目) -> getAssetsGapDetail


# 获取资产差额(合计平衡项目)时间序列 -> getAssetsNettingSeries


# 获取资产差额(合计平衡项目) -> getAssetsNetting


# 获取资产总计时间序列 -> getStm07BsReItsAllAssetsSeries


# 获取资产总计 -> getStm07BsReItsAllAssets


# 获取资产处置收益时间序列 -> getGainAssetDispositionsSeries


# 获取资产处置收益 -> getGainAssetDispositions


# 获取资产支持证券投资_FUND时间序列 -> getStmBs72Series


# 获取资产支持证券投资_FUND -> getStmBs72


# 获取资产合计_FUND时间序列 -> getStmBs19Series


# 获取资产合计_FUND -> getStmBs19


# 获取资产支持证券利息收入_FUND时间序列 -> getStmIs69Series


# 获取资产支持证券利息收入_FUND -> getStmIs69


# 获取资产支持证券投资公允价值变动收益_FUND时间序列 -> getStmIs105Series


# 获取资产支持证券投资公允价值变动收益_FUND -> getStmIs105


# 获取资产回报率(TTM)_PIT时间序列 -> getFaRoaTtMSeries


# 获取资产回报率(TTM)_PIT -> getFaRoaTtM


# 获取资产总计_PIT时间序列 -> getFaToTAssetsSeries


# 获取资产总计_PIT -> getFaToTAssets


# 获取资产总计(MRQ,只有最新数据)时间序列 -> getAssetMrQSeries


# 获取资产总计(MRQ,只有最新数据) -> getAssetMrQ


# 获取净资产收益率ROE(平均)时间序列 -> getRoeAvgSeries


# 获取净资产收益率ROE(平均) -> getRoeAvg


# 获取净资产收益率ROE(加权)时间序列 -> getRoeBasicSeries


# 获取净资产收益率ROE(加权) -> getRoeBasic


# 获取净资产收益率ROE(摊薄)时间序列 -> getRoeDilutedSeries


# 获取净资产收益率ROE(摊薄) -> getRoeDiluted


# 获取净资产收益率ROE(扣除/平均)时间序列 -> getRoeDeductedSeries


# 获取净资产收益率ROE(扣除/平均) -> getRoeDeducted


# 获取净资产收益率ROE(扣除/加权)时间序列 -> getRoeExBasicSeries


# 获取净资产收益率ROE(扣除/加权) -> getRoeExBasic


# 获取净资产收益率ROE(扣除/摊薄)时间序列 -> getRoeExDilutedSeries


# 获取净资产收益率ROE(扣除/摊薄) -> getRoeExDiluted


# 获取净资产收益率ROE-增发条件时间序列 -> getRoeAddSeries


# 获取净资产收益率ROE-增发条件 -> getRoeAdd


# 获取总资产报酬率ROA时间序列 -> getRoa2Series


# 获取总资产报酬率ROA -> getRoa2


# 获取总资产净利率ROA时间序列 -> getRoaSeries


# 获取总资产净利率ROA -> getRoa


# 获取净资产收益率ROE时间序列 -> getRoeSeries


# 获取净资产收益率ROE -> getRoe


# 获取净资产收益率(TTM)时间序列 -> getRoeTtM2Series


# 获取净资产收益率(TTM) -> getRoeTtM2


# 获取净资产收益率(TTM,平均)时间序列 -> getFaRoeTtMAvgSeries


# 获取净资产收益率(TTM,平均) -> getFaRoeTtMAvg


# 获取总资产报酬率(TTM)时间序列 -> getRoa2TtM2Series


# 获取总资产报酬率(TTM) -> getRoa2TtM2


# 获取总资产净利率-不含少数股东损益(TTM)时间序列 -> getNetProfitToAssetsSeries


# 获取总资产净利率-不含少数股东损益(TTM) -> getNetProfitToAssets


# 获取净资产收益率_GSD时间序列 -> getWgsDRoeSeries


# 获取净资产收益率_GSD -> getWgsDRoe


# 获取净资产收益率ROE(摊薄)_GSD时间序列 -> getWgsDRoeDilutedSeries


# 获取净资产收益率ROE(摊薄)_GSD -> getWgsDRoeDiluted


# 获取净资产收益率(扣除)_GSD时间序列 -> getWgsDRoeDeductedSeries


# 获取净资产收益率(扣除)_GSD -> getWgsDRoeDeducted


# 获取净资产收益率ROE(扣除/摊薄)_GSD时间序列 -> getWgsDRoeExDilutedSeries


# 获取净资产收益率ROE(扣除/摊薄)_GSD -> getWgsDRoeExDiluted


# 获取净资产收益率(年化)_GSD时间序列 -> getWgsDRoeYearlySeries


# 获取净资产收益率(年化)_GSD -> getWgsDRoeYearly


# 获取总资产净利率_GSD时间序列 -> getWgsDRoaSeries


# 获取总资产净利率_GSD -> getWgsDRoa


# 获取总资产净利率(年化)_GSD时间序列 -> getWgsDRoaYearlySeries


# 获取总资产净利率(年化)_GSD -> getWgsDRoaYearly


# 获取总资产报酬率ROA_GSD时间序列 -> getWgsDRoa2Series


# 获取总资产报酬率ROA_GSD -> getWgsDRoa2


# 获取总资产报酬率(年化)_GSD时间序列 -> getWgsDRoa2YearlySeries


# 获取总资产报酬率(年化)_GSD -> getWgsDRoa2Yearly


# 获取净资产收益率(TTM)_GSD时间序列 -> getRoeTtM3Series


# 获取净资产收益率(TTM)_GSD -> getRoeTtM3


# 获取总资产净利率(TTM)_GSD时间序列 -> getRoaTtM2Series


# 获取总资产净利率(TTM)_GSD -> getRoaTtM2


# 获取总资产净利率-不含少数股东损益(TTM)_GSD时间序列 -> getNetProfitToAssets2Series


# 获取总资产净利率-不含少数股东损益(TTM)_GSD -> getNetProfitToAssets2


# 获取总资产报酬率(TTM)_GSD时间序列 -> getRoa2TtM3Series


# 获取总资产报酬率(TTM)_GSD -> getRoa2TtM3


# 获取总资产_GSD时间序列 -> getWgsDAssetsSeries


# 获取总资产_GSD -> getWgsDAssets


# 获取净资产收益率(平均)_PIT时间序列 -> getFaRoeAvgSeries


# 获取净资产收益率(平均)_PIT -> getFaRoeAvg


# 获取净资产收益率(加权)_PIT时间序列 -> getFaRoeWGtSeries


# 获取净资产收益率(加权)_PIT -> getFaRoeWGt


# 获取净资产收益率(摊薄)_PIT时间序列 -> getFaRoeDilutedSeries


# 获取净资产收益率(摊薄)_PIT -> getFaRoeDiluted


# 获取净资产收益率(扣除/加权)_PIT时间序列 -> getFaRoeExBasicSeries


# 获取净资产收益率(扣除/加权)_PIT -> getFaRoeExBasic


# 获取净资产收益率(扣除/摊薄)_PIT时间序列 -> getFaRoeExDilutedSeries


# 获取净资产收益率(扣除/摊薄)_PIT -> getFaRoeExDiluted


# 获取净资产收益率(TTM)_PIT时间序列 -> getFaRoeNpTtMSeries


# 获取净资产收益率(TTM)_PIT -> getFaRoeNpTtM


# 获取总资产报酬率(TTM)_PIT时间序列 -> getFaRoaEbItTtMSeries


# 获取总资产报酬率(TTM)_PIT -> getFaRoaEbItTtM


# 获取总资产净利率-不含少数股东损益(TTM)_PIT时间序列 -> getFaNetProfitToAssetsTtMSeries


# 获取总资产净利率-不含少数股东损益(TTM)_PIT -> getFaNetProfitToAssetsTtM


# 获取净资产周转率(TTM)_PIT时间序列 -> getFaNaTurnTtMSeries


# 获取净资产周转率(TTM)_PIT -> getFaNaTurnTtM


# 获取净资产收益率ROE(TTM,只有最新数据)时间序列 -> getRoeTtMSeries


# 获取净资产收益率ROE(TTM,只有最新数据) -> getRoeTtM


# 获取总资产报酬率ROA(TTM,只有最新数据)时间序列 -> getRoa2TtMSeries


# 获取总资产报酬率ROA(TTM,只有最新数据) -> getRoa2TtM


# 获取总资产净利率ROA(TTM,只有最新数据)时间序列 -> getRoaTtMSeries


# 获取总资产净利率ROA(TTM,只有最新数据) -> getRoaTtM


# 获取固定资产投资扩张率时间序列 -> getYoYFixedAssetsSeries


# 获取固定资产投资扩张率 -> getYoYFixedAssets


# 获取有形资产时间序列 -> getTangibleAssetSeries


# 获取有形资产 -> getTangibleAsset


# 获取短期资产流动性比率(人民币)时间序列 -> getStAssetLiqRatioRMbNSeries


# 获取短期资产流动性比率(人民币) -> getStAssetLiqRatioRMbN


# 获取短期资产流动性比率(本外币)时间序列 -> getStmNoteBankAssetLiqRatioSeries


# 获取短期资产流动性比率(本外币) -> getStmNoteBankAssetLiqRatio


# 获取短期资产流动性比率(外币)时间序列 -> getStAssetLiqRatioNormBNSeries


# 获取短期资产流动性比率(外币) -> getStAssetLiqRatioNormBN


# 获取生息资产时间序列 -> getStmNoteBank351Series


# 获取生息资产 -> getStmNoteBank351


# 获取生息资产收益率时间序列 -> getStmNoteBank58Series


# 获取生息资产收益率 -> getStmNoteBank58


# 获取生息资产平均余额时间序列 -> getStmNoteBank57Series


# 获取生息资产平均余额 -> getStmNoteBank57


# 获取短期资产流动性比率(人民币)(旧)时间序列 -> getStAssetLiqRatioRMbSeries


# 获取短期资产流动性比率(人民币)(旧) -> getStAssetLiqRatioRMb


# 获取短期资产流动性比率(外币)(旧)时间序列 -> getStAssetLiqRatioNormBSeries


# 获取短期资产流动性比率(外币)(旧) -> getStAssetLiqRatioNormB


# 获取其它资产时间序列 -> getStmNoteInSur7808Series


# 获取其它资产 -> getStmNoteInSur7808


# 获取认可资产时间序列 -> getQStmNoteInSur212512Series


# 获取认可资产 -> getQStmNoteInSur212512


# 获取有形资产_GSD时间序列 -> getWgsDTangibleAsset2Series


# 获取有形资产_GSD -> getWgsDTangibleAsset2


# 获取流动资产合计_GSD时间序列 -> getWgsDAssetsCurRSeries


# 获取流动资产合计_GSD -> getWgsDAssetsCurR


# 获取固定资产净值_GSD时间序列 -> getWgsDPpeNetSeries


# 获取固定资产净值_GSD -> getWgsDPpeNet


# 获取合同资产时间序列 -> getContAssetsSeries


# 获取合同资产 -> getContAssets


# 获取流动资产差额(特殊报表科目)时间序列 -> getCurAssetsGapSeries


# 获取流动资产差额(特殊报表科目) -> getCurAssetsGap


# 获取流动资产差额说明(特殊报表科目)时间序列 -> getCurAssetsGapDetailSeries


# 获取流动资产差额说明(特殊报表科目) -> getCurAssetsGapDetail


# 获取流动资产差额(合计平衡项目)时间序列 -> getCurAssetsNettingSeries


# 获取流动资产差额(合计平衡项目) -> getCurAssetsNetting


# 获取流动资产合计时间序列 -> getStm07BsReItsLiquidAssetSeries


# 获取流动资产合计 -> getStm07BsReItsLiquidAsset


# 获取固定资产(合计)时间序列 -> getFixAssetsToTSeries


# 获取固定资产(合计) -> getFixAssetsToT


# 获取固定资产时间序列 -> getFixAssetsSeries


# 获取固定资产 -> getFixAssets


# 获取固定资产清理时间序列 -> getFixAssetsDispSeries


# 获取固定资产清理 -> getFixAssetsDisp


# 获取油气资产时间序列 -> getOilAndNaturalGasAssetsSeries


# 获取油气资产 -> getOilAndNaturalGasAssets


# 获取无形资产时间序列 -> getIntangAssetsSeries


# 获取无形资产 -> getIntangAssets


# 获取固定资产折旧、油气资产折耗、生产性生物资产折旧时间序列 -> getDePrFaCogADpBaSeries


# 获取固定资产折旧、油气资产折耗、生产性生物资产折旧 -> getDePrFaCogADpBa


# 获取无形资产摊销时间序列 -> getAMortIntangAssetsSeries


# 获取无形资产摊销 -> getAMortIntangAssets


# 获取固定资产报废损失时间序列 -> getLossSCrFaSeries


# 获取固定资产报废损失 -> getLossSCrFa


# 获取固定资产-原值时间序列 -> getStmNoteAssetDetail1Series


# 获取固定资产-原值 -> getStmNoteAssetDetail1


# 获取固定资产-累计折旧时间序列 -> getStmNoteAssetDetail2Series


# 获取固定资产-累计折旧 -> getStmNoteAssetDetail2


# 获取固定资产-减值准备时间序列 -> getStmNoteAssetDetail3Series


# 获取固定资产-减值准备 -> getStmNoteAssetDetail3


# 获取固定资产-净额时间序列 -> getStmNoteAssetDetail4Series


# 获取固定资产-净额 -> getStmNoteAssetDetail4


# 获取固定资产-净值时间序列 -> getStmNoteAvOfASeries


# 获取固定资产-净值 -> getStmNoteAvOfA


# 获取油气资产-原值时间序列 -> getStmNoteAssetDetail13Series


# 获取油气资产-原值 -> getStmNoteAssetDetail13


# 获取油气资产-累计折耗时间序列 -> getStmNoteAssetDetail14Series


# 获取油气资产-累计折耗 -> getStmNoteAssetDetail14


# 获取油气资产-减值准备时间序列 -> getStmNoteAssetDetail15Series


# 获取油气资产-减值准备 -> getStmNoteAssetDetail15


# 获取油气资产-净额时间序列 -> getStmNoteAssetDetail16Series


# 获取油气资产-净额 -> getStmNoteAssetDetail16


# 获取无形资产-原值时间序列 -> getStmNoteAssetDetail17Series


# 获取无形资产-原值 -> getStmNoteAssetDetail17


# 获取无形资产-累计摊销时间序列 -> getStmNoteAssetDetail18Series


# 获取无形资产-累计摊销 -> getStmNoteAssetDetail18


# 获取无形资产-减值准备时间序列 -> getStmNoteAssetDetail19Series


# 获取无形资产-减值准备 -> getStmNoteAssetDetail19


# 获取无形资产-净额时间序列 -> getStmNoteAssetDetail20Series


# 获取无形资产-净额 -> getStmNoteAssetDetail20


# 获取重仓资产支持证券Wind代码时间序列 -> getPrtTopAbsWindCodeSeries


# 获取重仓资产支持证券Wind代码 -> getPrtTopAbsWindCode


# 获取流动资产比率_PIT时间序列 -> getFaCurAssetsRatioSeries


# 获取流动资产比率_PIT -> getFaCurAssetsRatio


# 获取固定资产比率_PIT时间序列 -> getFaFixedAssetToAssetSeries


# 获取固定资产比率_PIT -> getFaFixedAssetToAsset


# 获取无形资产比率_PIT时间序列 -> getFaIntangAssetRatioSeries


# 获取无形资产比率_PIT -> getFaIntangAssetRatio


# 获取有形资产_PIT时间序列 -> getFaTangibleAssetSeries


# 获取有形资产_PIT -> getFaTangibleAsset


# 获取固定资产合计_PIT时间序列 -> getFaFixAssetsSeries


# 获取固定资产合计_PIT -> getFaFixAssets


# 获取预测总资产收益率(ROA)平均值时间序列 -> getEstAvgRoaSeries


# 获取预测总资产收益率(ROA)平均值 -> getEstAvgRoa


# 获取预测总资产收益率(ROA)最大值时间序列 -> getEstMaxRoaSeries


# 获取预测总资产收益率(ROA)最大值 -> getEstMaxRoa


# 获取预测总资产收益率(ROA)最小值时间序列 -> getEstMinRoaSeries


# 获取预测总资产收益率(ROA)最小值 -> getEstMinRoa


# 获取预测总资产收益率(ROA)中值时间序列 -> getEstMedianRoaSeries


# 获取预测总资产收益率(ROA)中值 -> getEstMedianRoa


# 获取预测总资产收益率(ROA)标准差时间序列 -> getEstStdRoaSeries


# 获取预测总资产收益率(ROA)标准差 -> getEstStdRoa


# 获取预测净资产收益率(ROE)平均值时间序列 -> getEstAvgRoeSeries


# 获取预测净资产收益率(ROE)平均值 -> getEstAvgRoe


# 获取预测净资产收益率(ROE)最大值时间序列 -> getEstMaxRoeSeries


# 获取预测净资产收益率(ROE)最大值 -> getEstMaxRoe


# 获取预测净资产收益率(ROE)最小值时间序列 -> getEstMinRoeSeries


# 获取预测净资产收益率(ROE)最小值 -> getEstMinRoe


# 获取预测净资产收益率(ROE)中值时间序列 -> getEstMedianRoeSeries


# 获取预测净资产收益率(ROE)中值 -> getEstMedianRoe


# 获取预测净资产收益率(ROE)标准差时间序列 -> getEstStdRoeSeries


# 获取预测净资产收益率(ROE)标准差 -> getEstStdRoe


# 获取预测总资产收益率(ROA)平均值(可选类型)时间序列 -> getWestAvgRoaSeries


# 获取预测总资产收益率(ROA)平均值(可选类型) -> getWestAvgRoa


# 获取预测总资产收益率(ROA)最大值(可选类型)时间序列 -> getWestMaxRoaSeries


# 获取预测总资产收益率(ROA)最大值(可选类型) -> getWestMaxRoa


# 获取预测总资产收益率(ROA)最小值(可选类型)时间序列 -> getWestMinRoaSeries


# 获取预测总资产收益率(ROA)最小值(可选类型) -> getWestMinRoa


# 获取预测总资产收益率(ROA)中值(可选类型)时间序列 -> getWestMedianRoaSeries


# 获取预测总资产收益率(ROA)中值(可选类型) -> getWestMedianRoa


# 获取预测总资产收益率(ROA)标准差(可选类型)时间序列 -> getWestStdRoaSeries


# 获取预测总资产收益率(ROA)标准差(可选类型) -> getWestStdRoa


# 获取预测净资产收益率(ROE)平均值(可选类型)时间序列 -> getWestAvgRoeSeries


# 获取预测净资产收益率(ROE)平均值(可选类型) -> getWestAvgRoe


# 获取预测净资产收益率(ROE)最大值(可选类型)时间序列 -> getWestMaxRoeSeries


# 获取预测净资产收益率(ROE)最大值(可选类型) -> getWestMaxRoe


# 获取预测净资产收益率(ROE)最小值(可选类型)时间序列 -> getWestMinRoeSeries


# 获取预测净资产收益率(ROE)最小值(可选类型) -> getWestMinRoe


# 获取预测净资产收益率(ROE)中值(可选类型)时间序列 -> getWestMedianRoeSeries


# 获取预测净资产收益率(ROE)中值(可选类型) -> getWestMedianRoe


# 获取预测净资产收益率(ROE)标准差(可选类型)时间序列 -> getWestStdRoeSeries


# 获取预测净资产收益率(ROE)标准差(可选类型) -> getWestStdRoe


# 获取每股净资产BPS时间序列 -> getBpSSeries


# 获取每股净资产BPS -> getBpS


# 获取每股净资产BPS(最新股本摊薄)时间序列 -> getBpSAdjustSeries


# 获取每股净资产BPS(最新股本摊薄) -> getBpSAdjust


# 获取每股净资产BPS(最新公告)时间序列 -> getBpSNewSeries


# 获取每股净资产BPS(最新公告) -> getBpSNew


# 获取非生息资产时间序列 -> getStmNoteBank421Series


# 获取非生息资产 -> getStmNoteBank421


# 获取表内外资产总额时间序列 -> getStmNoteSec33Series


# 获取表内外资产总额 -> getStmNoteSec33


# 获取总投资资产时间序列 -> getStmNoteInSur7809Series


# 获取总投资资产 -> getStmNoteInSur7809


# 获取每股净资产_GSD时间序列 -> getWgsDBpSSeries


# 获取每股净资产_GSD -> getWgsDBpS


# 获取每股净资产(最新公告)_GSD时间序列 -> getWgsDBpSNewSeries


# 获取每股净资产(最新公告)_GSD -> getWgsDBpSNew


# 获取平均净资产收益率_GSD时间序列 -> getWgsDDupontRoeSeries


# 获取平均净资产收益率_GSD -> getWgsDDupontRoe


# 获取非流动资产合计_GSD时间序列 -> getWgsDAssetsLtSeries


# 获取非流动资产合计_GSD -> getWgsDAssetsLt


# 获取使用权资产时间序列 -> getPropRightUseSeries


# 获取使用权资产 -> getPropRightUse


# 获取非流动资产差额(特殊报表科目)时间序列 -> getNonCurAssetsGapSeries


# 获取非流动资产差额(特殊报表科目) -> getNonCurAssetsGap


# 获取非流动资产差额说明(特殊报表科目)时间序列 -> getNonCurAssetsGapDetailSeries


# 获取非流动资产差额说明(特殊报表科目) -> getNonCurAssetsGapDetail


# 获取非流动资产差额(合计平衡项目)时间序列 -> getNonCurAssetsNettingSeries


# 获取非流动资产差额(合计平衡项目) -> getNonCurAssetsNetting


# 获取非流动资产合计时间序列 -> getStm07BsReItsNonLiquidSeries


# 获取非流动资产合计 -> getStm07BsReItsNonLiquid


# 获取非流动资产处置净损失时间序列 -> getNetLossDispNonCurAssetSeries


# 获取非流动资产处置净损失 -> getNetLossDispNonCurAsset


# 获取使用权资产折旧时间序列 -> getDePrePropRightUseSeries


# 获取使用权资产折旧 -> getDePrePropRightUse


# 获取非流动资产处置损益时间序列 -> getStmNoteEoItems6Series


# 获取非流动资产处置损益 -> getStmNoteEoItems6


# 获取对数总资产_PIT时间序列 -> getValLnToTAssetsSeries


# 获取对数总资产_PIT -> getValLnToTAssets


# 获取每股净资产_PIT时间序列 -> getFaBpSSeries


# 获取每股净资产_PIT -> getFaBpS


# 获取现金流资产比-资产回报率(TTM)_PIT时间序列 -> getFaAccaTtMSeries


# 获取现金流资产比-资产回报率(TTM)_PIT -> getFaAccaTtM


# 获取非流动资产比率_PIT时间序列 -> getFaNonCurAssetsRatioSeries


# 获取非流动资产比率_PIT -> getFaNonCurAssetsRatio


# 获取债务总资产比_PIT时间序列 -> getFaDebtsAssetRatioSeries


# 获取债务总资产比_PIT -> getFaDebtsAssetRatio


# 获取加权风险资产净额时间序列 -> getStmNoteBank133NSeries


# 获取加权风险资产净额 -> getStmNoteBank133N


# 获取加权风险资产净额(2013)时间序列 -> getStmNoteBankRWeightedAssetsSeries


# 获取加权风险资产净额(2013) -> getStmNoteBankRWeightedAssets


# 获取加权风险资产净额(旧)时间序列 -> getStmNoteBank133Series


# 获取加权风险资产净额(旧) -> getStmNoteBank133


# 获取受托管理资产总规模时间序列 -> getStmNoteAssetManageSeries


# 获取受托管理资产总规模 -> getStmNoteAssetManage


# 获取权益投资资产分红收入时间序列 -> getStmNoteInvestmentIncome0002Series


# 获取权益投资资产分红收入 -> getStmNoteInvestmentIncome0002


# 获取其他流动资产_GSD时间序列 -> getWgsDAssetsCurROThSeries


# 获取其他流动资产_GSD -> getWgsDAssetsCurROTh


# 获取其他固定资产净值_GSD时间序列 -> getWgsDPpeNetOThSeries


# 获取其他固定资产净值_GSD -> getWgsDPpeNetOTh


# 获取出售固定资产收到的现金_GSD时间序列 -> getWgsDAssetsBusCfSeries


# 获取出售固定资产收到的现金_GSD -> getWgsDAssetsBusCf


# 获取其他流动资产时间序列 -> getOThCurAssetsSeries


# 获取其他流动资产 -> getOThCurAssets


# 获取代理业务资产时间序列 -> getAgencyBusAssetsSeries


# 获取代理业务资产 -> getAgencyBusAssets


# 获取独立账户资产时间序列 -> getIndependentAccTAssetsSeries


# 获取独立账户资产 -> getIndependentAccTAssets


# 获取衍生金融资产时间序列 -> getDerivativeFinAssetsSeries


# 获取衍生金融资产 -> getDerivativeFinAssets


# 获取处置固定资产、无形资产和其他长期资产收回的现金净额时间序列 -> getNetCashRecpDispFiOltASeries


# 获取处置固定资产、无形资产和其他长期资产收回的现金净额 -> getNetCashRecpDispFiOltA


# 获取购建固定资产、无形资产和其他长期资产支付的现金时间序列 -> getCashPayAcqConstFiOltASeries


# 获取购建固定资产、无形资产和其他长期资产支付的现金 -> getCashPayAcqConstFiOltA


# 获取处置固定资产、无形资产和其他长期资产的损失时间序列 -> getLossDispFiOltASeries


# 获取处置固定资产、无形资产和其他长期资产的损失 -> getLossDispFiOltA


# 获取单季度.资产处置收益时间序列 -> getQfaGainAssetDispositionsSeries


# 获取单季度.资产处置收益 -> getQfaGainAssetDispositions


# 获取非货币性资产交换损益时间序列 -> getStmNoteEoItems11Series


# 获取非货币性资产交换损益 -> getStmNoteEoItems11


# 获取衍生金融资产_FUND时间序列 -> getStmBs109Series


# 获取衍生金融资产_FUND -> getStmBs109


# 获取新股申购资产规模报备日时间序列 -> getIpoAssetDateSeries


# 获取新股申购资产规模报备日 -> getIpoAssetDate


# 获取5年平均资产回报率_PIT时间序列 -> getFaRoaAvg5YSeries


# 获取5年平均资产回报率_PIT -> getFaRoaAvg5Y


# 获取ABS基础资产分类时间序列 -> getAbsUnderlyingTypeSeries


# 获取ABS基础资产分类 -> getAbsUnderlyingType


# 获取预测每股净资产(BPS)平均值时间序列 -> getEstAvgBpSSeries


# 获取预测每股净资产(BPS)平均值 -> getEstAvgBpS


# 获取预测每股净资产(BPS)最大值时间序列 -> getEstMaxBpSSeries


# 获取预测每股净资产(BPS)最大值 -> getEstMaxBpS


# 获取预测每股净资产(BPS)最小值时间序列 -> getEstMinBpSSeries


# 获取预测每股净资产(BPS)最小值 -> getEstMinBpS


# 获取预测每股净资产(BPS)中值时间序列 -> getEstMedianBpSSeries


# 获取预测每股净资产(BPS)中值 -> getEstMedianBpS


# 获取预测每股净资产(BPS)标准差时间序列 -> getEstStdBpSSeries


# 获取预测每股净资产(BPS)标准差 -> getEstStdBpS


# 获取预测每股净资产(BPS)平均值(币种转换)时间序列 -> getEstAvgBpS1Series


# 获取预测每股净资产(BPS)平均值(币种转换) -> getEstAvgBpS1


# 获取预测每股净资产(BPS)最大值(币种转换)时间序列 -> getEstMaxBpS1Series


# 获取预测每股净资产(BPS)最大值(币种转换) -> getEstMaxBpS1


# 获取预测每股净资产(BPS)最小值(币种转换)时间序列 -> getEstMinBpS1Series


# 获取预测每股净资产(BPS)最小值(币种转换) -> getEstMinBpS1


# 获取预测每股净资产(BPS)中值(币种转换)时间序列 -> getEstMedianBpS1Series


# 获取预测每股净资产(BPS)中值(币种转换) -> getEstMedianBpS1


# 获取预测每股净资产(BPS)标准差(币种转换)时间序列 -> getEstStdBpS1Series


# 获取预测每股净资产(BPS)标准差(币种转换) -> getEstStdBpS1


# 获取预测每股净资产(BPS)平均值(可选类型)时间序列 -> getWestAvgBpSSeries


# 获取预测每股净资产(BPS)平均值(可选类型) -> getWestAvgBpS


# 获取预测每股净资产(BPS)最大值(可选类型)时间序列 -> getWestMaxBpSSeries


# 获取预测每股净资产(BPS)最大值(可选类型) -> getWestMaxBpS


# 获取预测每股净资产(BPS)最小值(可选类型)时间序列 -> getWestMinBpSSeries


# 获取预测每股净资产(BPS)最小值(可选类型) -> getWestMinBpS


# 获取预测每股净资产(BPS)中值(可选类型)时间序列 -> getWestMedianBpSSeries


# 获取预测每股净资产(BPS)中值(可选类型) -> getWestMedianBpS


# 获取预测每股净资产(BPS)标准差(可选类型)时间序列 -> getWestStdBpSSeries


# 获取预测每股净资产(BPS)标准差(可选类型) -> getWestStdBpS


# 获取预测每股净资产(BPS)平均值(可选类型,币种转换)时间序列 -> getWestAvgBpS1Series


# 获取预测每股净资产(BPS)平均值(可选类型,币种转换) -> getWestAvgBpS1


# 获取预测每股净资产(BPS)最大值(可选类型,币种转换)时间序列 -> getWestMaxBpS1Series


# 获取预测每股净资产(BPS)最大值(可选类型,币种转换) -> getWestMaxBpS1


# 获取预测每股净资产(BPS)最小值(可选类型,币种转换)时间序列 -> getWestMinBpS1Series


# 获取预测每股净资产(BPS)最小值(可选类型,币种转换) -> getWestMinBpS1


# 获取预测每股净资产(BPS)中值(可选类型,币种转换)时间序列 -> getWestMedianBpS1Series


# 获取预测每股净资产(BPS)中值(可选类型,币种转换) -> getWestMedianBpS1


# 获取预测每股净资产(BPS)标准差(可选类型,币种转换)时间序列 -> getWestStdBpS1Series


# 获取预测每股净资产(BPS)标准差(可选类型,币种转换) -> getWestStdBpS1


# 获取预测每股净资产Surprise(可选类型)时间序列 -> getWestBpSSurpriseSeries


# 获取预测每股净资产Surprise(可选类型) -> getWestBpSSurprise


# 获取预测每股净资产Surprise百分比(可选类型)时间序列 -> getWestBpSSurprisePctSeries


# 获取预测每股净资产Surprise百分比(可选类型) -> getWestBpSSurprisePct


# 获取净资本/净资产时间序列 -> getStmNoteSec6Series


# 获取净资本/净资产 -> getStmNoteSec6


# 获取单季度.净资产收益率ROE时间序列 -> getQfaRoeSeries


# 获取单季度.净资产收益率ROE -> getQfaRoe


# 获取单季度.总资产净利率ROA时间序列 -> getQfaRoaSeries


# 获取单季度.总资产净利率ROA -> getQfaRoa


# 获取单季度.净资产收益率ROE_GSD时间序列 -> getWgsDQfaRoeSeries


# 获取单季度.净资产收益率ROE_GSD -> getWgsDQfaRoe


# 获取单季度.总资产净利率ROA_GSD时间序列 -> getWgsDQfaRoaSeries


# 获取单季度.总资产净利率ROA_GSD -> getWgsDQfaRoa


# 获取交易性金融资产_GSD时间序列 -> getWgsDInvestTradingSeries


# 获取交易性金融资产_GSD -> getWgsDInvestTrading


# 获取其他非流动资产_GSD时间序列 -> getWgsDAssetsLtOThSeries


# 获取其他非流动资产_GSD -> getWgsDAssetsLtOTh


# 获取消耗性生物资产时间序列 -> getConsumptiveBioAssetsSeries


# 获取消耗性生物资产 -> getConsumptiveBioAssets


# 获取生产性生物资产时间序列 -> getProductiveBioAssetsSeries


# 获取生产性生物资产 -> getProductiveBioAssets


# 获取其他非流动资产时间序列 -> getOThNonCurAssetsSeries


# 获取其他非流动资产 -> getOThNonCurAssets


# 获取生产性生物资产-原值时间序列 -> getStmNoteAssetDetail9Series


# 获取生产性生物资产-原值 -> getStmNoteAssetDetail9


# 获取生产性生物资产-累计折旧时间序列 -> getStmNoteAssetDetail10Series


# 获取生产性生物资产-累计折旧 -> getStmNoteAssetDetail10


# 获取生产性生物资产-减值准备时间序列 -> getStmNoteAssetDetail11Series


# 获取生产性生物资产-减值准备 -> getStmNoteAssetDetail11


# 获取生产性生物资产-净额时间序列 -> getStmNoteAssetDetail12Series


# 获取生产性生物资产-净额 -> getStmNoteAssetDetail12


# 获取交易性金融资产_FUND时间序列 -> getStmBs71Series


# 获取交易性金融资产_FUND -> getStmBs71


# 获取长期负债/资产总计_PIT时间序列 -> getFaLtDebtToAssetSeries


# 获取长期负债/资产总计_PIT -> getFaLtDebtToAsset


# 获取应付债券/资产总计_PIT时间序列 -> getFaBondsPayableToAssetSeries


# 获取应付债券/资产总计_PIT -> getFaBondsPayableToAsset


# 获取信用风险加权资产(2013)时间序列 -> getStmNoteBankRWeightedAssetsCrSeries


# 获取信用风险加权资产(2013) -> getStmNoteBankRWeightedAssetsCr


# 获取市场风险加权资产(2013)时间序列 -> getStmNoteBankRWeightedAssetsMrSeries


# 获取市场风险加权资产(2013) -> getStmNoteBankRWeightedAssetsMr


# 获取操作风险加权资产(2013)时间序列 -> getStmNoteBankRWeightedAssetsOrSeries


# 获取操作风险加权资产(2013) -> getStmNoteBankRWeightedAssetsOr


# 获取卖出回购金融资产款时间序列 -> getFundSalesFinAssetsRpSeries


# 获取卖出回购金融资产款 -> getFundSalesFinAssetsRp


# 获取融资租入固定资产时间序列 -> getFaFncLeasesSeries


# 获取融资租入固定资产 -> getFaFncLeases


# 获取单季度.固定资产折旧、油气资产折耗、生产性生物资产折旧时间序列 -> getQfaDePrFaCogADpBaSeries


# 获取单季度.固定资产折旧、油气资产折耗、生产性生物资产折旧 -> getQfaDePrFaCogADpBa


# 获取单季度.无形资产摊销时间序列 -> getQfaAMortIntangAssetsSeries


# 获取单季度.无形资产摊销 -> getQfaAMortIntangAssets


# 获取单季度.固定资产报废损失时间序列 -> getQfaLossSCrFaSeries


# 获取单季度.固定资产报废损失 -> getQfaLossSCrFa


# 获取担保总额占净资产比例时间序列 -> getStmNoteGuarantee6Series


# 获取担保总额占净资产比例 -> getStmNoteGuarantee6


# 获取卖出回购金融资产支出_FUND时间序列 -> getStmIs13Series


# 获取卖出回购金融资产支出_FUND -> getStmIs13


# 获取一致预测每股净资产(FY1)时间序列 -> getWestAvgBpSFy1Series


# 获取一致预测每股净资产(FY1) -> getWestAvgBpSFy1


# 获取一致预测每股净资产(FY2)时间序列 -> getWestAvgBpSFy2Series


# 获取一致预测每股净资产(FY2) -> getWestAvgBpSFy2


# 获取一致预测每股净资产(FY3)时间序列 -> getWestAvgBpSFy3Series


# 获取一致预测每股净资产(FY3) -> getWestAvgBpSFy3


# 获取利息收入:金融资产回购业务收入时间序列 -> getStmNoteSec1513Series


# 获取利息收入:金融资产回购业务收入 -> getStmNoteSec1513


# 获取房地产物业相关资产净值_GSD时间序列 -> getWgsDRealEstateNetSeries


# 获取房地产物业相关资产净值_GSD -> getWgsDRealEstateNet


# 获取其他非流动金融资产时间序列 -> getOThNonCurFinaAssetSeries


# 获取其他非流动金融资产 -> getOThNonCurFinaAsset


# 获取处置交易性金融资产净增加额时间序列 -> getNetInCrDispTfaSeries


# 获取处置交易性金融资产净增加额 -> getNetInCrDispTfa


# 获取单季度.非流动资产处置净损失时间序列 -> getQfaNetLossDispNonCurAssetSeries


# 获取单季度.非流动资产处置净损失 -> getQfaNetLossDispNonCurAsset


# 获取单季度.使用权资产折旧时间序列 -> getQfaDePrePropRightUseSeries


# 获取单季度.使用权资产折旧 -> getQfaDePrePropRightUse


# 获取股东权益/固定资产_PIT时间序列 -> getFaEquityToFixedAssetSeries


# 获取股东权益/固定资产_PIT -> getFaEquityToFixedAsset


# 获取利息净收入:金融资产回购业务收入时间序列 -> getStmNoteSec1533Series


# 获取利息净收入:金融资产回购业务收入 -> getStmNoteSec1533


# 获取单季度.出售固定资产收到的现金_GSD时间序列 -> getWgsDQfaAssetsBusCfSeries


# 获取单季度.出售固定资产收到的现金_GSD -> getWgsDQfaAssetsBusCf


# 获取划分为持有待售的资产时间序列 -> getHfSAssetsSeries


# 获取划分为持有待售的资产 -> getHfSAssets


# 获取单季度.处置固定资产、无形资产和其他长期资产收回的现金净额时间序列 -> getQfaNetCashRecpDispFiOltASeries


# 获取单季度.处置固定资产、无形资产和其他长期资产收回的现金净额 -> getQfaNetCashRecpDispFiOltA


# 获取单季度.购建固定资产、无形资产和其他长期资产支付的现金时间序列 -> getQfaCashPayAcqConstFiOltASeries


# 获取单季度.购建固定资产、无形资产和其他长期资产支付的现金 -> getQfaCashPayAcqConstFiOltA


# 获取单季度.处置固定资产、无形资产和其他长期资产的损失时间序列 -> getQfaLossDispFiOltASeries


# 获取单季度.处置固定资产、无形资产和其他长期资产的损失 -> getQfaLossDispFiOltA


# 获取一年内到期的非流动资产时间序列 -> getNonCurAssetsDueWithin1YSeries


# 获取一年内到期的非流动资产 -> getNonCurAssetsDueWithin1Y


# 获取以摊余成本计量的金融资产时间序列 -> getFinAssetsAmortizedCostSeries


# 获取以摊余成本计量的金融资产 -> getFinAssetsAmortizedCost


# 获取以摊余成本计量的金融资产终止确认收益时间序列 -> getTerFinAsSIncomeSeries


# 获取以摊余成本计量的金融资产终止确认收益 -> getTerFinAsSIncome


# 获取单季度.融资租入固定资产时间序列 -> getQfaFaFncLeasesSeries


# 获取单季度.融资租入固定资产 -> getQfaFaFncLeases


# 获取存货明细-消耗性生物资产时间序列 -> getStmNoteInv9Series


# 获取存货明细-消耗性生物资产 -> getStmNoteInv9


# 获取单季度.处置交易性金融资产净增加额时间序列 -> getQfaNetInCrDispTfaSeries


# 获取单季度.处置交易性金融资产净增加额 -> getQfaNetInCrDispTfa


# 获取息税前利润(TTM)/总资产时间序列 -> getEbItToAssets2Series


# 获取息税前利润(TTM)/总资产 -> getEbItToAssets2


# 获取息税前利润(TTM)/总资产_GSD时间序列 -> getEbItToAssetsTtMSeries


# 获取息税前利润(TTM)/总资产_GSD -> getEbItToAssetsTtM


# 获取持有(或处置)交易性金融资产和负债产生的公允价值变动损益时间序列 -> getStmNoteEoItems28Series


# 获取持有(或处置)交易性金融资产和负债产生的公允价值变动损益 -> getStmNoteEoItems28


# 获取单季度.以摊余成本计量的金融资产终止确认收益时间序列 -> getQfaTerFinAsSIncomeSeries


# 获取单季度.以摊余成本计量的金融资产终止确认收益 -> getQfaTerFinAsSIncome


# 获取ETF申购赎回最小申购赎回单位资产净值时间序列 -> getFundEtFPrMinnaVUnitSeries


# 获取ETF申购赎回最小申购赎回单位资产净值 -> getFundEtFPrMinnaVUnit


# 获取以公允价值计量且其变动计入当期损益的金融资产时间序列 -> getTradableFinAssetsSeries


# 获取以公允价值计量且其变动计入当期损益的金融资产 -> getTradableFinAssets


# 获取负债差额(特殊报表科目)时间序列 -> getLiaBGapSeries


# 获取负债差额(特殊报表科目) -> getLiaBGap


# 获取负债差额说明(特殊报表科目)时间序列 -> getLiaBGapDetailSeries


# 获取负债差额说明(特殊报表科目) -> getLiaBGapDetail


# 获取负债差额(合计平衡项目)时间序列 -> getLiaBNettingSeries


# 获取负债差额(合计平衡项目) -> getLiaBNetting


# 获取负债合计时间序列 -> getStm07BsReItsAllDebtSeries


# 获取负债合计 -> getStm07BsReItsAllDebt


# 获取负债及股东权益差额(特殊报表科目)时间序列 -> getLiaBSHrhLDrEqYGapSeries


# 获取负债及股东权益差额(特殊报表科目) -> getLiaBSHrhLDrEqYGap


# 获取负债及股东权益差额说明(特殊报表科目)时间序列 -> getLiaBSHrhLDrEqYGapDetailSeries


# 获取负债及股东权益差额说明(特殊报表科目) -> getLiaBSHrhLDrEqYGapDetail


# 获取负债及股东权益差额(合计平衡项目)时间序列 -> getLiaBSHrhLDrEqYNettingSeries


# 获取负债及股东权益差额(合计平衡项目) -> getLiaBSHrhLDrEqYNetting


# 获取负债及股东权益总计时间序列 -> getToTLiaBSHrhLDrEqYSeries


# 获取负债及股东权益总计 -> getToTLiaBSHrhLDrEqY


# 获取负债合计_FUND时间序列 -> getStmBs33Series


# 获取负债合计_FUND -> getStmBs33


# 获取负债及持有人权益合计_FUND时间序列 -> getStmBs39Series


# 获取负债及持有人权益合计_FUND -> getStmBs39


# 获取负债和所有者权益总计时间序列 -> getStm07BsReItsDebtEquitySeries


# 获取负债和所有者权益总计 -> getStm07BsReItsDebtEquity


# 获取负债合计_PIT时间序列 -> getFaToTliAbSeries


# 获取负债合计_PIT -> getFaToTliAb


# 获取负债合计(MRQ,只有最新数据)时间序列 -> getDebtMrQSeries


# 获取负债合计(MRQ,只有最新数据) -> getDebtMrQ


# 获取总负债_GSD时间序列 -> getWgsDLiAbsSeries


# 获取总负债_GSD -> getWgsDLiAbs


# 获取总负债及总权益_GSD时间序列 -> getWgsDLiAbsStKhlDrSEqSeries


# 获取总负债及总权益_GSD -> getWgsDLiAbsStKhlDrSEq


# 获取计息负债时间序列 -> getStmNoteBank381Series


# 获取计息负债 -> getStmNoteBank381


# 获取计息负债成本率时间序列 -> getStmNoteBank60Series


# 获取计息负债成本率 -> getStmNoteBank60


# 获取计息负债平均余额时间序列 -> getStmNoteBank59Series


# 获取计息负债平均余额 -> getStmNoteBank59


# 获取无息负债时间序列 -> getFaNoneInterestDebtSeries


# 获取无息负债 -> getFaNoneInterestDebt


# 获取认可负债时间序列 -> getQStmNoteInSur212513Series


# 获取认可负债 -> getQStmNoteInSur212513


# 获取合同负债_GSD时间序列 -> getWgsDLiAbsContractSeries


# 获取合同负债_GSD -> getWgsDLiAbsContract


# 获取流动负债合计_GSD时间序列 -> getWgsDLiAbsCurRSeries


# 获取流动负债合计_GSD -> getWgsDLiAbsCurR


# 获取其他负债_GSD时间序列 -> getWgsDLiAbsOThSeries


# 获取其他负债_GSD -> getWgsDLiAbsOTh


# 获取合同负债时间序列 -> getContLiaBSeries


# 获取合同负债 -> getContLiaB


# 获取流动负债差额(特殊报表科目)时间序列 -> getCurLiaBGapSeries


# 获取流动负债差额(特殊报表科目) -> getCurLiaBGap


# 获取流动负债差额说明(特殊报表科目)时间序列 -> getCurLiaBGapDetailSeries


# 获取流动负债差额说明(特殊报表科目) -> getCurLiaBGapDetail


# 获取流动负债差额(合计平衡项目)时间序列 -> getCurLiaBNettingSeries


# 获取流动负债差额(合计平衡项目) -> getCurLiaBNetting


# 获取流动负债合计时间序列 -> getStm07BsReItsLiquidDebtSeries


# 获取流动负债合计 -> getStm07BsReItsLiquidDebt


# 获取租赁负债时间序列 -> getLeaseObligationSeries


# 获取租赁负债 -> getLeaseObligation


# 获取预计负债时间序列 -> getProvisionsSeries


# 获取预计负债 -> getProvisions


# 获取其他负债时间序列 -> getOThLiaBSeries


# 获取其他负债 -> getOThLiaB


# 获取预计负债产生的损益时间序列 -> getStmNoteEoItems18Series


# 获取预计负债产生的损益 -> getStmNoteEoItems18


# 获取其他负债_FUND时间序列 -> getStmBs32Series


# 获取其他负债_FUND -> getStmBs32


# 获取长期负债/营运资金_PIT时间序列 -> getFaUnCurDebtToWorkCapSeries


# 获取长期负债/营运资金_PIT -> getFaUnCurDebtToWorkCap


# 获取非计息负债时间序列 -> getStmNoteBank431Series


# 获取非计息负债 -> getStmNoteBank431


# 获取净资本负债率时间序列 -> getStmNoteSec3Series


# 获取净资本负债率 -> getStmNoteSec3


# 获取非流动负债合计_GSD时间序列 -> getWgsDLiAbsLtSeries


# 获取非流动负债合计_GSD -> getWgsDLiAbsLt


# 获取非流动负债差额(特殊报表科目)时间序列 -> getNonCurLiaBGapSeries


# 获取非流动负债差额(特殊报表科目) -> getNonCurLiaBGap


# 获取非流动负债差额说明(特殊报表科目)时间序列 -> getNonCurLiaBGapDetailSeries


# 获取非流动负债差额说明(特殊报表科目) -> getNonCurLiaBGapDetail


# 获取非流动负债差额(合计平衡项目)时间序列 -> getNonCurLiaBNettingSeries


# 获取非流动负债差额(合计平衡项目) -> getNonCurLiaBNetting


# 获取非流动负债合计时间序列 -> getToTNonCurLiaBSeries


# 获取非流动负债合计 -> getToTNonCurLiaB


# 获取无息流动负债时间序列 -> getExInterestDebtCurrentSeries


# 获取无息流动负债 -> getExInterestDebtCurrent


# 获取无息流动负债_GSD时间序列 -> getWgsDExInterestDebtCurrentSeries


# 获取无息流动负债_GSD -> getWgsDExInterestDebtCurrent


# 获取其他流动负债_GSD时间序列 -> getWgsDLiAbsCurROThSeries


# 获取其他流动负债_GSD -> getWgsDLiAbsCurROTh


# 获取保险合同负债_GSD时间序列 -> getWgsDLiAbsInSurContractSeries


# 获取保险合同负债_GSD -> getWgsDLiAbsInSurContract


# 获取投资合同负债_GSD时间序列 -> getWgsDLiAbsInvestContractSeries


# 获取投资合同负债_GSD -> getWgsDLiAbsInvestContract


# 获取其他流动负债时间序列 -> getOThCurLiaBSeries


# 获取其他流动负债 -> getOThCurLiaB


# 获取代理业务负债时间序列 -> getAgencyBusLiaBSeries


# 获取代理业务负债 -> getAgencyBusLiaB


# 获取独立账户负债时间序列 -> getIndependentAccTLiaBSeries


# 获取独立账户负债 -> getIndependentAccTLiaB


# 获取衍生金融负债时间序列 -> getDerivativeFinLiaBSeries


# 获取衍生金融负债 -> getDerivativeFinLiaB


# 获取衍生金融负债_FUND时间序列 -> getStmBs74Series


# 获取衍生金融负债_FUND -> getStmBs74


# 获取现金流动负债比(TTM)_PIT时间序列 -> getFaCFotoCurlIAbsTtMSeries


# 获取现金流动负债比(TTM)_PIT -> getFaCFotoCurlIAbsTtM


# 获取现金流动负债比率_PIT时间序列 -> getFaCashToCurlIAbsSeries


# 获取现金流动负债比率_PIT -> getFaCashToCurlIAbs


# 获取无息流动负债_PIT时间序列 -> getFaNicuRDebtSeries


# 获取无息流动负债_PIT -> getFaNicuRDebt


# 获取无息非流动负债时间序列 -> getExInterestDebtNonCurrentSeries


# 获取无息非流动负债 -> getExInterestDebtNonCurrent


# 获取营业利润/负债合计_GSD时间序列 -> getWgsDOpToDebtSeries


# 获取营业利润/负债合计_GSD -> getWgsDOpToDebt


# 获取无息非流动负债_GSD时间序列 -> getWgsDExInterestDebtNonCurrent2Series


# 获取无息非流动负债_GSD -> getWgsDExInterestDebtNonCurrent2


# 获取交易性金融负债_GSD时间序列 -> getWgsDLiAbsTradingSeries


# 获取交易性金融负债_GSD -> getWgsDLiAbsTrading


# 获取其他非流动负债_GSD时间序列 -> getWgsDLiAbsLtOThSeries


# 获取其他非流动负债_GSD -> getWgsDLiAbsLtOTh


# 获取其他非流动负债时间序列 -> getOThNonCurLiaBSeries


# 获取其他非流动负债 -> getOThNonCurLiaB


# 获取交易性金融负债_FUND时间序列 -> getStmBs73Series


# 获取交易性金融负债_FUND -> getStmBs73


# 获取无息非流动负债_PIT时间序列 -> getFaNinoCurDebtSeries


# 获取无息非流动负债_PIT -> getFaNinoCurDebt


# 获取营业利润/流动负债_GSD时间序列 -> getWgsDOpToLiqDebtSeries


# 获取营业利润/流动负债_GSD -> getWgsDOpToLiqDebt


# 获取递延收益-流动负债时间序列 -> getDeferredIncCurLiaBSeries


# 获取递延收益-流动负债 -> getDeferredIncCurLiaB


# 获取划分为持有待售的负债时间序列 -> getHfSLiaBSeries


# 获取划分为持有待售的负债 -> getHfSLiaB


# 获取递延收益-非流动负债时间序列 -> getDeferredIncNonCurLiaBSeries


# 获取递延收益-非流动负债 -> getDeferredIncNonCurLiaB


# 获取一年内到期的非流动负债时间序列 -> getNonCurLiaBDueWithin1YSeries


# 获取一年内到期的非流动负债 -> getNonCurLiaBDueWithin1Y


# 获取短期融资债(其他流动负债)时间序列 -> getStmNoteOthers7639Series


# 获取短期融资债(其他流动负债) -> getStmNoteOthers7639


# 获取以公允价值计量且其变动计入当期损益的金融负债时间序列 -> getTradableFinLiaBSeries


# 获取以公允价值计量且其变动计入当期损益的金融负债 -> getTradableFinLiaB


# 获取所有者权益合计时间序列 -> getStm07BsReItsAllEquitySeries


# 获取所有者权益合计 -> getStm07BsReItsAllEquity


# 获取期初所有者权益(基金净值)时间序列 -> getStmNavChange1Series


# 获取期初所有者权益(基金净值) -> getStmNavChange1


# 获取期末所有者权益(基金净值)时间序列 -> getStmNavChange11Series


# 获取期末所有者权益(基金净值) -> getStmNavChange11


# 获取归属于母公司所有者权益合计时间序列 -> getStm07BsReItsEquitySeries


# 获取归属于母公司所有者权益合计 -> getStm07BsReItsEquity


# 获取归属于母公司所有者权益合计/全部投入资本_PIT时间序列 -> getFaEquityToCapitalSeries


# 获取归属于母公司所有者权益合计/全部投入资本_PIT -> getFaEquityToCapital


# 获取现金及现金等价物净增加额_GSD时间序列 -> getWgsDChgCashCfSeries


# 获取现金及现金等价物净增加额_GSD -> getWgsDChgCashCf


# 获取现金及现金等价物净增加额差额(特殊报表科目)时间序列 -> getNetInCrCashCashEquGapSeries


# 获取现金及现金等价物净增加额差额(特殊报表科目) -> getNetInCrCashCashEquGap


# 获取现金及现金等价物净增加额差额说明(特殊报表科目)时间序列 -> getNetInCrCashCashEquGapDetailSeries


# 获取现金及现金等价物净增加额差额说明(特殊报表科目) -> getNetInCrCashCashEquGapDetail


# 获取现金及现金等价物净增加额差额(合计平衡项目)时间序列 -> getNetInCrCashCashEquNettingSeries


# 获取现金及现金等价物净增加额差额(合计平衡项目) -> getNetInCrCashCashEquNetting


# 获取现金及现金等价物净增加额时间序列 -> getStm07CsReItsCashAddSeries


# 获取现金及现金等价物净增加额 -> getStm07CsReItsCashAdd


# 获取单季度.现金及现金等价物净增加额_GSD时间序列 -> getWgsDQfaChgCashCfSeries


# 获取单季度.现金及现金等价物净增加额_GSD -> getWgsDQfaChgCashCf


# 获取间接法-现金及现金等价物净增加额时间序列 -> getNetInCrCashCashEquImSeries


# 获取间接法-现金及现金等价物净增加额 -> getNetInCrCashCashEquIm


# 获取单季度.现金及现金等价物净增加额时间序列 -> getQfaNetInCrCashCashEquDmSeries


# 获取单季度.现金及现金等价物净增加额 -> getQfaNetInCrCashCashEquDm


# 获取单季度.间接法-现金及现金等价物净增加额时间序列 -> getQfaNetInCrCashCashEquImSeries


# 获取单季度.间接法-现金及现金等价物净增加额 -> getQfaNetInCrCashCashEquIm


# 获取营业总收入(TTM)_PIT时间序列 -> getFaGrTtMSeries


# 获取营业总收入(TTM)_PIT -> getFaGrTtM


# 获取营业总收入(TTM)时间序列 -> getGrTtM2Series


# 获取营业总收入(TTM) -> getGrTtM2


# 获取营业总收入(TTM)_GSD时间序列 -> getGrTtM3Series


# 获取营业总收入(TTM)_GSD -> getGrTtM3


# 获取营业总收入时间序列 -> getStm07IsReItsSIncomeSeries


# 获取营业总收入 -> getStm07IsReItsSIncome


# 获取单季度.营业总收入时间序列 -> getQfaToTOperRevSeries


# 获取单季度.营业总收入 -> getQfaToTOperRev


# 获取EBITDA/营业总收入时间序列 -> getEbItDatoSalesSeries


# 获取EBITDA/营业总收入 -> getEbItDatoSales


# 获取EBITDA/营业总收入_GSD时间序列 -> getWgsDEbItDatoSalesSeries


# 获取EBITDA/营业总收入_GSD -> getWgsDEbItDatoSales


# 获取营业收入(TTM)_VAL_PIT时间序列 -> getOrTtMSeries


# 获取营业收入(TTM)_VAL_PIT -> getOrTtM


# 获取营业收入(TTM)时间序列 -> getOrTtM2Series


# 获取营业收入(TTM) -> getOrTtM2


# 获取营业收入(TTM)_GSD时间序列 -> getOrTtM3Series


# 获取营业收入(TTM)_GSD -> getOrTtM3


# 获取营业收入时间序列 -> getStm07IsReItsIncomeSeries


# 获取营业收入 -> getStm07IsReItsIncome


# 获取营业收入(TTM)_PIT时间序列 -> getFaOrTtMSeries


# 获取营业收入(TTM)_PIT -> getFaOrTtM


# 获取总营业收入_GSD时间序列 -> getWgsDSalesSeries


# 获取总营业收入_GSD -> getWgsDSales


# 获取总营业收入(公布值)_GSD时间序列 -> getArdIsSalesSeries


# 获取总营业收入(公布值)_GSD -> getArdIsSales


# 获取预测营业收入Surprise(可选类型)时间序列 -> getWestSalesSurpriseSeries


# 获取预测营业收入Surprise(可选类型) -> getWestSalesSurprise


# 获取预测营业收入Surprise百分比(可选类型)时间序列 -> getWestSalesSurprisePctSeries


# 获取预测营业收入Surprise百分比(可选类型) -> getWestSalesSurprisePct


# 获取其他营业收入_GSD时间序列 -> getWgsDSalesOThSeries


# 获取其他营业收入_GSD -> getWgsDSalesOTh


# 获取一致预测营业收入(FY1)时间序列 -> getWestSalesFy1Series


# 获取一致预测营业收入(FY1) -> getWestSalesFy1


# 获取一致预测营业收入(FY2)时间序列 -> getWestSalesFy2Series


# 获取一致预测营业收入(FY2) -> getWestSalesFy2


# 获取一致预测营业收入(FY3)时间序列 -> getWestSalesFy3Series


# 获取一致预测营业收入(FY3) -> getWestSalesFy3


# 获取单季度.营业收入时间序列 -> getQfaOperRevSeries


# 获取单季度.营业收入 -> getQfaOperRev


# 获取一致预测营业收入(FY1)变化率_1M_PIT时间序列 -> getWestSalesFy11MSeries


# 获取一致预测营业收入(FY1)变化率_1M_PIT -> getWestSalesFy11M


# 获取一致预测营业收入(FY1)变化率_3M_PIT时间序列 -> getWestSalesFy13MSeries


# 获取一致预测营业收入(FY1)变化率_3M_PIT -> getWestSalesFy13M


# 获取一致预测营业收入(FY1)变化率_6M_PIT时间序列 -> getWestSalesFy16MSeries


# 获取一致预测营业收入(FY1)变化率_6M_PIT -> getWestSalesFy16M


# 获取一致预测营业收入(FY1)的变化_1M_PIT时间序列 -> getWestSalesFy1Chg1MSeries


# 获取一致预测营业收入(FY1)的变化_1M_PIT -> getWestSalesFy1Chg1M


# 获取一致预测营业收入(FY1)的变化_3M_PIT时间序列 -> getWestSalesFy1Chg3MSeries


# 获取一致预测营业收入(FY1)的变化_3M_PIT -> getWestSalesFy1Chg3M


# 获取一致预测营业收入(FY1)的变化_6M_PIT时间序列 -> getWestSalesFy1Chg6MSeries


# 获取一致预测营业收入(FY1)的变化_6M_PIT -> getWestSalesFy1Chg6M


# 获取一致预测营业收入(FY1)标准差_PIT时间序列 -> getWestStdSalesFy1Series


# 获取一致预测营业收入(FY1)标准差_PIT -> getWestStdSalesFy1


# 获取一致预测营业收入(FY1)最大与一致预测营业收入(FY1)最小值的变化率_PIT时间序列 -> getWestSalesMaxMinFy1Series


# 获取一致预测营业收入(FY1)最大与一致预测营业收入(FY1)最小值的变化率_PIT -> getWestSalesMaxMinFy1


# 获取营业利润/营业收入(TTM)时间序列 -> getOpToOrTtMSeries


# 获取营业利润/营业收入(TTM) -> getOpToOrTtM


# 获取利润总额/营业收入(TTM)时间序列 -> getEBtToOrTtMSeries


# 获取利润总额/营业收入(TTM) -> getEBtToOrTtM


# 获取营业利润/营业收入(TTM)_GSD时间序列 -> getOpToOrTtM2Series


# 获取营业利润/营业收入(TTM)_GSD -> getOpToOrTtM2


# 获取利润总额/营业收入(TTM)_GSD时间序列 -> getEBtToOrTtM2Series


# 获取利润总额/营业收入(TTM)_GSD -> getEBtToOrTtM2


# 获取单季度.总营业收入_GSD时间序列 -> getWgsDQfaSalesSeries


# 获取单季度.总营业收入_GSD -> getWgsDQfaSales


# 获取营业利润/营业收入(TTM)_PIT时间序列 -> getFaOpToOrTtMSeries


# 获取营业利润/营业收入(TTM)_PIT -> getFaOpToOrTtM


# 获取利润总额/营业收入(TTM)_PIT时间序列 -> getFaPbtToOrTtMSeries


# 获取利润总额/营业收入(TTM)_PIT -> getFaPbtToOrTtM


# 获取单季度.其他营业收入_GSD时间序列 -> getWgsDQfaSalesOThSeries


# 获取单季度.其他营业收入_GSD -> getWgsDQfaSalesOTh


# 获取研发支出总额占营业收入比例时间序列 -> getStmNoteRdExpToSalesSeries


# 获取研发支出总额占营业收入比例 -> getStmNoteRdExpToSales


# 获取归属母公司股东的净利润/营业收入(TTM)时间序列 -> getNetProfitToOrTtMSeries


# 获取归属母公司股东的净利润/营业收入(TTM) -> getNetProfitToOrTtM


# 获取归属母公司股东的净利润/营业收入(TTM)_GSD时间序列 -> getNetProfitToOrTtM2Series


# 获取归属母公司股东的净利润/营业收入(TTM)_GSD -> getNetProfitToOrTtM2


# 获取归属母公司股东的净利润/营业收入(TTM)_PIT时间序列 -> getFaNetProfitToOrTtMSeries


# 获取归属母公司股东的净利润/营业收入(TTM)_PIT -> getFaNetProfitToOrTtM


# 获取利息收入合计时间序列 -> getStmNoteSec1510Series


# 获取利息收入合计 -> getStmNoteSec1510


# 获取利息收入:金融企业往来业务收入时间序列 -> getStmNoteSec1512Series


# 获取利息收入:金融企业往来业务收入 -> getStmNoteSec1512


# 获取利息收入_GSD时间序列 -> getWgsDIntIncSeries


# 获取利息收入_GSD -> getWgsDIntInc


# 获取利息收入时间序列 -> getIntIncSeries


# 获取利息收入 -> getIntInc


# 获取利息收入_FUND时间序列 -> getStmIs80Series


# 获取利息收入_FUND -> getStmIs80


# 获取非利息收入时间序列 -> getStmNoteBank411Series


# 获取非利息收入 -> getStmNoteBank411


# 获取非利息收入占比时间序列 -> getStmNoteBank30Series


# 获取非利息收入占比 -> getStmNoteBank30


# 获取贷款利息收入_总计时间序列 -> getStmNoteBank710Series


# 获取贷款利息收入_总计 -> getStmNoteBank710


# 获取贷款利息收入_企业贷款及垫款时间序列 -> getStmNoteBank721Series


# 获取贷款利息收入_企业贷款及垫款 -> getStmNoteBank721


# 获取贷款利息收入_个人贷款及垫款时间序列 -> getStmNoteBank722Series


# 获取贷款利息收入_个人贷款及垫款 -> getStmNoteBank722


# 获取贷款利息收入_票据贴现时间序列 -> getStmNoteBank723Series


# 获取贷款利息收入_票据贴现 -> getStmNoteBank723


# 获取贷款利息收入_个人住房贷款时间序列 -> getStmNoteBank724Series


# 获取贷款利息收入_个人住房贷款 -> getStmNoteBank724


# 获取贷款利息收入_个人消费贷款时间序列 -> getStmNoteBank725Series


# 获取贷款利息收入_个人消费贷款 -> getStmNoteBank725


# 获取贷款利息收入_信用卡应收账款时间序列 -> getStmNoteBank726Series


# 获取贷款利息收入_信用卡应收账款 -> getStmNoteBank726


# 获取贷款利息收入_经营性贷款时间序列 -> getStmNoteBank727Series


# 获取贷款利息收入_经营性贷款 -> getStmNoteBank727


# 获取贷款利息收入_汽车贷款时间序列 -> getStmNoteBank728Series


# 获取贷款利息收入_汽车贷款 -> getStmNoteBank728


# 获取贷款利息收入_其他个人贷款时间序列 -> getStmNoteBank729Series


# 获取贷款利息收入_其他个人贷款 -> getStmNoteBank729


# 获取贷款利息收入_信用贷款时间序列 -> getStmNoteBank781Series


# 获取贷款利息收入_信用贷款 -> getStmNoteBank781


# 获取贷款利息收入_保证贷款时间序列 -> getStmNoteBank782Series


# 获取贷款利息收入_保证贷款 -> getStmNoteBank782


# 获取贷款利息收入_抵押贷款时间序列 -> getStmNoteBank783Series


# 获取贷款利息收入_抵押贷款 -> getStmNoteBank783


# 获取贷款利息收入_质押贷款时间序列 -> getStmNoteBank784Series


# 获取贷款利息收入_质押贷款 -> getStmNoteBank784


# 获取贷款利息收入_短期贷款时间序列 -> getStmNoteBank841Series


# 获取贷款利息收入_短期贷款 -> getStmNoteBank841


# 获取贷款利息收入_中长期贷款时间序列 -> getStmNoteBank842Series


# 获取贷款利息收入_中长期贷款 -> getStmNoteBank842


# 获取存款利息收入_FUND时间序列 -> getStmIs6Series


# 获取存款利息收入_FUND -> getStmIs6


# 获取债券利息收入_FUND时间序列 -> getStmIs5Series


# 获取债券利息收入_FUND -> getStmIs5


# 获取其他利息收入_FUND时间序列 -> getStmIs76Series


# 获取其他利息收入_FUND -> getStmIs76


# 获取单季度.利息收入_GSD时间序列 -> getWgsDQfaIntIncSeries


# 获取单季度.利息收入_GSD -> getWgsDQfaIntInc


# 获取单季度.利息收入时间序列 -> getQfaInterestIncSeries


# 获取单季度.利息收入 -> getQfaInterestInc


# 获取财务费用:利息收入时间序列 -> getFinIntIncSeries


# 获取财务费用:利息收入 -> getFinIntInc


# 获取固定息证券投资利息收入时间序列 -> getStmNoteInvestmentIncome0001Series


# 获取固定息证券投资利息收入 -> getStmNoteInvestmentIncome0001


# 获取单季度.财务费用:利息收入时间序列 -> getQfaFinIntIncSeries


# 获取单季度.财务费用:利息收入 -> getQfaFinIntInc


# 获取已赚保费时间序列 -> getInSurPremUnearnedSeries


# 获取已赚保费 -> getInSurPremUnearned


# 获取净已赚保费_GSD时间序列 -> getWgsDPremiumsEarnedSeries


# 获取净已赚保费_GSD -> getWgsDPremiumsEarned


# 获取单季度.已赚保费时间序列 -> getQfaInSurPremUnearnedSeries


# 获取单季度.已赚保费 -> getQfaInSurPremUnearned


# 获取单季度.净已赚保费_GSD时间序列 -> getWgsDQfaPremiumsEarnedSeries


# 获取单季度.净已赚保费_GSD -> getWgsDQfaPremiumsEarned


# 获取手续费及佣金收入合计时间序列 -> getStmNoteSec1500Series


# 获取手续费及佣金收入合计 -> getStmNoteSec1500


# 获取手续费及佣金收入:证券经纪业务时间序列 -> getStmNoteSec1501Series


# 获取手续费及佣金收入:证券经纪业务 -> getStmNoteSec1501


# 获取手续费及佣金收入:证券承销业务时间序列 -> getStmNoteSec1503Series


# 获取手续费及佣金收入:证券承销业务 -> getStmNoteSec1503


# 获取手续费及佣金收入:保荐业务时间序列 -> getStmNoteSec1505Series


# 获取手续费及佣金收入:保荐业务 -> getStmNoteSec1505


# 获取手续费及佣金收入:投资咨询业务时间序列 -> getStmNoteSec1506Series


# 获取手续费及佣金收入:投资咨询业务 -> getStmNoteSec1506


# 获取手续费及佣金收入:期货经纪业务时间序列 -> getStmNoteSec1507Series


# 获取手续费及佣金收入:期货经纪业务 -> getStmNoteSec1507


# 获取手续费及佣金收入_GSD时间序列 -> getWgsDFeeComMIncSeries


# 获取手续费及佣金收入_GSD -> getWgsDFeeComMInc


# 获取手续费及佣金收入时间序列 -> getHandlingChrGComMIncSeries


# 获取手续费及佣金收入 -> getHandlingChrGComMInc


# 获取单季度.手续费及佣金收入_GSD时间序列 -> getWgsDQfaFeeComMIncSeries


# 获取单季度.手续费及佣金收入_GSD -> getWgsDQfaFeeComMInc


# 获取单季度.手续费及佣金收入时间序列 -> getQfaHandlingChrGComMIncSeries


# 获取单季度.手续费及佣金收入 -> getQfaHandlingChrGComMInc


# 获取保费业务收入时间序列 -> getToTPremIncSeries


# 获取保费业务收入 -> getToTPremInc


# 获取分保费收入时间序列 -> getReInSurIncSeries


# 获取分保费收入 -> getReInSurInc


# 获取单季度.分保费收入时间序列 -> getQfaReInSurIncSeries


# 获取单季度.分保费收入 -> getQfaReInSurInc


# 获取分出保费_GSD时间序列 -> getWgsDPremiumReInsurersSeries


# 获取分出保费_GSD -> getWgsDPremiumReInsurers


# 获取分出保费时间序列 -> getPremCededSeries


# 获取分出保费 -> getPremCeded


# 获取单季度.分出保费_GSD时间序列 -> getWgsDQfaPremiumReInsurersSeries


# 获取单季度.分出保费_GSD -> getWgsDQfaPremiumReInsurers


# 获取单季度.分出保费时间序列 -> getQfaPremCededSeries


# 获取单季度.分出保费 -> getQfaPremCeded


# 获取提取未到期责任准备金时间序列 -> getUnearnedPremRsRvWithdrawSeries


# 获取提取未到期责任准备金 -> getUnearnedPremRsRvWithdraw


# 获取单季度.提取未到期责任准备金时间序列 -> getQfaUnearnedPremRsRvSeries


# 获取单季度.提取未到期责任准备金 -> getQfaUnearnedPremRsRv


# 获取代理买卖证券业务净收入时间序列 -> getNetIncAgencyBusinessSeries


# 获取代理买卖证券业务净收入 -> getNetIncAgencyBusiness


# 获取单季度.代理买卖证券业务净收入时间序列 -> getQfaNetIncAgencyBusinessSeries


# 获取单季度.代理买卖证券业务净收入 -> getQfaNetIncAgencyBusiness


# 获取证券承销业务净收入时间序列 -> getNetIncUnderwritingBusinessSeries


# 获取证券承销业务净收入 -> getNetIncUnderwritingBusiness


# 获取单季度.证券承销业务净收入时间序列 -> getQfaNetIncUnderwritingBusinessSeries


# 获取单季度.证券承销业务净收入 -> getQfaNetIncUnderwritingBusiness


# 获取其他业务收入时间序列 -> getOtherOperIncSeries


# 获取其他业务收入 -> getOtherOperInc


# 获取其他业务收入(附注)时间序列 -> getStmNoteSeg1703Series


# 获取其他业务收入(附注) -> getStmNoteSeg1703


# 获取单季度.其他业务收入时间序列 -> getQfaOtherOperIncSeries


# 获取单季度.其他业务收入 -> getQfaOtherOperInc


# 获取利息净收入合计时间序列 -> getStmNoteSec1530Series


# 获取利息净收入合计 -> getStmNoteSec1530


# 获取利息净收入:金融企业往来业务收入时间序列 -> getStmNoteSec1532Series


# 获取利息净收入:金融企业往来业务收入 -> getStmNoteSec1532


# 获取利息净收入_GSD时间序列 -> getWgsDIntIncNetSeries


# 获取利息净收入_GSD -> getWgsDIntIncNet


# 获取利息净收入时间序列 -> getNetIntIncSeries


# 获取利息净收入 -> getNetIntInc


# 获取单季度.利息净收入_GSD时间序列 -> getWgsDQfaIntIncNetSeries


# 获取单季度.利息净收入_GSD -> getWgsDQfaIntIncNet


# 获取单季度.利息净收入时间序列 -> getQfaNetIntIncSeries


# 获取单季度.利息净收入 -> getQfaNetIntInc


# 获取手续费及佣金净收入合计时间序列 -> getStmNoteSec1520Series


# 获取手续费及佣金净收入合计 -> getStmNoteSec1520


# 获取手续费及佣金净收入:证券经纪业务时间序列 -> getStmNoteSec1521Series


# 获取手续费及佣金净收入:证券经纪业务 -> getStmNoteSec1521


# 获取手续费及佣金净收入:证券承销业务时间序列 -> getStmNoteSec1523Series


# 获取手续费及佣金净收入:证券承销业务 -> getStmNoteSec1523


# 获取手续费及佣金净收入:保荐业务时间序列 -> getStmNoteSec1525Series


# 获取手续费及佣金净收入:保荐业务 -> getStmNoteSec1525


# 获取手续费及佣金净收入:投资咨询业务时间序列 -> getStmNoteSec1526Series


# 获取手续费及佣金净收入:投资咨询业务 -> getStmNoteSec1526


# 获取手续费及佣金净收入:期货经纪业务时间序列 -> getStmNoteSec1527Series


# 获取手续费及佣金净收入:期货经纪业务 -> getStmNoteSec1527


# 获取手续费及佣金净收入:其他业务时间序列 -> getStmNoteSec1554Series


# 获取手续费及佣金净收入:其他业务 -> getStmNoteSec1554


# 获取手续费及佣金净收入_GSD时间序列 -> getWgsDFeeComMIncNetSeries


# 获取手续费及佣金净收入_GSD -> getWgsDFeeComMIncNet


# 获取手续费及佣金净收入时间序列 -> getNetFeeAndCommissionIncSeries


# 获取手续费及佣金净收入 -> getNetFeeAndCommissionInc


# 获取单季度.手续费及佣金净收入_GSD时间序列 -> getWgsDQfaFeeComMIncNetSeries


# 获取单季度.手续费及佣金净收入_GSD -> getWgsDQfaFeeComMIncNet


# 获取单季度.手续费及佣金净收入时间序列 -> getQfaNetFeeAndCommissionIncSeries


# 获取单季度.手续费及佣金净收入 -> getQfaNetFeeAndCommissionInc


# 获取其他业务净收益时间序列 -> getNetOtherOperIncSeries


# 获取其他业务净收益 -> getNetOtherOperInc


# 获取单季度.其他业务净收益时间序列 -> getQfaNetOtherOperIncSeries


# 获取单季度.其他业务净收益 -> getQfaNetOtherOperInc


# 获取营业总成本(TTM)时间序列 -> getGcTtM2Series


# 获取营业总成本(TTM) -> getGcTtM2


# 获取营业总成本(TTM)_GSD时间序列 -> getGcTtM3Series


# 获取营业总成本(TTM)_GSD -> getGcTtM3


# 获取营业总成本时间序列 -> getStm07IsReItsSCostSeries


# 获取营业总成本 -> getStm07IsReItsSCost


# 获取营业总成本2时间序列 -> getOperatingCost2Series


# 获取营业总成本2 -> getOperatingCost2


# 获取营业总成本(TTM)_PIT时间序列 -> getFaGcTtMSeries


# 获取营业总成本(TTM)_PIT -> getFaGcTtM


# 获取营业总成本(TTM,只有最新数据)时间序列 -> getGcTtMSeries


# 获取营业总成本(TTM,只有最新数据) -> getGcTtM


# 获取单季度.营业总成本2时间序列 -> getQfaOperatingCost2Series


# 获取单季度.营业总成本2 -> getQfaOperatingCost2


# 获取单季度.营业总成本时间序列 -> getQfaToTOperCostSeries


# 获取单季度.营业总成本 -> getQfaToTOperCost


# 获取营业成本-非金融类(TTM)时间序列 -> getCostTtM2Series


# 获取营业成本-非金融类(TTM) -> getCostTtM2


# 获取营业成本-非金融类(TTM)_GSD时间序列 -> getCostTtM3Series


# 获取营业成本-非金融类(TTM)_GSD -> getCostTtM3


# 获取营业成本_GSD时间序列 -> getWgsDOperCostSeries


# 获取营业成本_GSD -> getWgsDOperCost


# 获取营业成本时间序列 -> getStm07IsReItsCostSeries


# 获取营业成本 -> getStm07IsReItsCost


# 获取营业成本-非金融类(TTM)_PIT时间序列 -> getFaOcNfTtMSeries


# 获取营业成本-非金融类(TTM)_PIT -> getFaOcNfTtM


# 获取营业成本-非金融类(TTM,只有最新数据)时间序列 -> getCostTtMSeries


# 获取营业成本-非金融类(TTM,只有最新数据) -> getCostTtM


# 获取预测营业成本Surprise(可选类型)时间序列 -> getWestAvgOcSurpriseSeries


# 获取预测营业成本Surprise(可选类型) -> getWestAvgOcSurprise


# 获取预测营业成本Surprise百分比(可选类型)时间序列 -> getWestAvgOcSurprisePctSeries


# 获取预测营业成本Surprise百分比(可选类型) -> getWestAvgOcSurprisePct


# 获取一致预测营业成本(FY1)时间序列 -> getWestAvgOcFy1Series


# 获取一致预测营业成本(FY1) -> getWestAvgOcFy1


# 获取一致预测营业成本(FY2)时间序列 -> getWestAvgOcFy2Series


# 获取一致预测营业成本(FY2) -> getWestAvgOcFy2


# 获取一致预测营业成本(FY3)时间序列 -> getWestAvgOcFy3Series


# 获取一致预测营业成本(FY3) -> getWestAvgOcFy3


# 获取单季度.营业成本_GSD时间序列 -> getWgsDQfaOperCostSeries


# 获取单季度.营业成本_GSD -> getWgsDQfaOperCost


# 获取单季度.营业成本时间序列 -> getQfaOperCostSeries


# 获取单季度.营业成本 -> getQfaOperCost


# 获取利息支出(TTM)_GSD时间序列 -> getInterestExpenseTtM2Series


# 获取利息支出(TTM)_GSD -> getInterestExpenseTtM2


# 获取利息支出_GSD时间序列 -> getWgsDIntExpSeries


# 获取利息支出_GSD -> getWgsDIntExp


# 获取利息支出时间序列 -> getIntExpSeries


# 获取利息支出 -> getIntExp


# 获取利息支出_FUND时间序列 -> getStmIs72Series


# 获取利息支出_FUND -> getStmIs72


# 获取利息支出(TTM)_PIT时间序列 -> getFaInterestExpenseTtMSeries


# 获取利息支出(TTM)_PIT -> getFaInterestExpenseTtM


# 获取存款利息支出_存款总额时间序列 -> getStmNoteBank649Series


# 获取存款利息支出_存款总额 -> getStmNoteBank649


# 获取存款利息支出_个人定期存款时间序列 -> getStmNoteBank631Series


# 获取存款利息支出_个人定期存款 -> getStmNoteBank631


# 获取存款利息支出_个人活期存款时间序列 -> getStmNoteBank632Series


# 获取存款利息支出_个人活期存款 -> getStmNoteBank632


# 获取存款利息支出_公司定期存款时间序列 -> getStmNoteBank633Series


# 获取存款利息支出_公司定期存款 -> getStmNoteBank633


# 获取存款利息支出_公司活期存款时间序列 -> getStmNoteBank634Series


# 获取存款利息支出_公司活期存款 -> getStmNoteBank634


# 获取存款利息支出_其它存款时间序列 -> getStmNoteBank635Series


# 获取存款利息支出_其它存款 -> getStmNoteBank635


# 获取单季度.利息支出_GSD时间序列 -> getWgsDQfaIntExpSeries


# 获取单季度.利息支出_GSD -> getWgsDQfaIntExp


# 获取单季度.利息支出时间序列 -> getQfaInterestExpSeries


# 获取单季度.利息支出 -> getQfaInterestExp


# 获取手续费及佣金支出时间序列 -> getHandlingChrGComMExpSeries


# 获取手续费及佣金支出 -> getHandlingChrGComMExp


# 获取单季度.手续费及佣金支出时间序列 -> getQfaHandlingChrGComMExpSeries


# 获取单季度.手续费及佣金支出 -> getQfaHandlingChrGComMExp


# 获取营业支出-金融类(TTM)时间序列 -> getExpenseTtM2Series


# 获取营业支出-金融类(TTM) -> getExpenseTtM2


# 获取营业支出-金融类(TTM)_GSD时间序列 -> getExpenseTtM3Series


# 获取营业支出-金融类(TTM)_GSD -> getExpenseTtM3


# 获取营业支出时间序列 -> getOperExpSeries


# 获取营业支出 -> getOperExp


# 获取营业支出-金融类(TTM)_PIT时间序列 -> getFaOEfTtMSeries


# 获取营业支出-金融类(TTM)_PIT -> getFaOEfTtM


# 获取营业支出-金融类(TTM,只有最新数据)时间序列 -> getExpenseTtMSeries


# 获取营业支出-金融类(TTM,只有最新数据) -> getExpenseTtM


# 获取总营业支出_GSD时间序列 -> getWgsDOperExpToTSeries


# 获取总营业支出_GSD -> getWgsDOperExpToT


# 获取单季度.营业支出时间序列 -> getQfaOperExpSeries


# 获取单季度.营业支出 -> getQfaOperExp


# 获取单季度.总营业支出_GSD时间序列 -> getWgsDQfaOperExpToTSeries


# 获取单季度.总营业支出_GSD -> getWgsDQfaOperExpToT


# 获取税金及附加时间序列 -> getStm07IsReItsTaxSeries


# 获取税金及附加 -> getStm07IsReItsTax


# 获取税金及附加_FUND时间序列 -> getStmIs26Series


# 获取税金及附加_FUND -> getStmIs26


# 获取单季度.税金及附加时间序列 -> getQfaTaxesSurchargesOpsSeries


# 获取单季度.税金及附加 -> getQfaTaxesSurchargesOps


# 获取销售费用(TTM)时间序列 -> getOperateExpenseTtM2Series


# 获取销售费用(TTM) -> getOperateExpenseTtM2


# 获取销售费用(TTM)_GSD时间序列 -> getOperateExpenseTtM3Series


# 获取销售费用(TTM)_GSD -> getOperateExpenseTtM3


# 获取销售费用_GSD时间序列 -> getWgsDSalesExpSeries


# 获取销售费用_GSD -> getWgsDSalesExp


# 获取销售费用时间序列 -> getStm07IsReItsSalesFeeSeries


# 获取销售费用 -> getStm07IsReItsSalesFee


# 获取销售费用(TTM)_PIT时间序列 -> getFaSellExpenseTtMSeries


# 获取销售费用(TTM)_PIT -> getFaSellExpenseTtM


# 获取销售费用(TTM,只有最新数据)时间序列 -> getOperateExpenseTtMSeries


# 获取销售费用(TTM,只有最新数据) -> getOperateExpenseTtM


# 获取单季度.销售费用时间序列 -> getQfaSellingDistExpSeries


# 获取单季度.销售费用 -> getQfaSellingDistExp


# 获取租赁费(销售费用)时间序列 -> getStmNoteOthers7630Series


# 获取租赁费(销售费用) -> getStmNoteOthers7630


# 获取工资薪酬(销售费用)时间序列 -> getStmNoteOthers7626Series


# 获取工资薪酬(销售费用) -> getStmNoteOthers7626


# 获取折旧摊销(销售费用)时间序列 -> getStmNoteOthers7628Series


# 获取折旧摊销(销售费用) -> getStmNoteOthers7628


# 获取仓储运输费(销售费用)时间序列 -> getStmNoteOthers7632Series


# 获取仓储运输费(销售费用) -> getStmNoteOthers7632


# 获取广告宣传推广费(销售费用)时间序列 -> getStmNoteOthers7633Series


# 获取广告宣传推广费(销售费用) -> getStmNoteOthers7633


# 获取管理费用(TTM)时间序列 -> getAdminExpenseTtM2Series


# 获取管理费用(TTM) -> getAdminExpenseTtM2


# 获取管理费用(TTM)_GSD时间序列 -> getAdminExpenseTtM3Series


# 获取管理费用(TTM)_GSD -> getAdminExpenseTtM3


# 获取管理费用_GSD时间序列 -> getWgsDMgTExpSeries


# 获取管理费用_GSD -> getWgsDMgTExp


# 获取管理费用时间序列 -> getStm07IsReItsManageFeeSeries


# 获取管理费用 -> getStm07IsReItsManageFee


# 获取管理费用(TTM)_PIT时间序列 -> getFaAdminExpenseTtMSeries


# 获取管理费用(TTM)_PIT -> getFaAdminExpenseTtM


# 获取管理费用(TTM,只有最新数据)时间序列 -> getAdminExpenseTtMSeries


# 获取管理费用(TTM,只有最新数据) -> getAdminExpenseTtM


# 获取单季度.管理费用时间序列 -> getQfaGerLAdminExpSeries


# 获取单季度.管理费用 -> getQfaGerLAdminExp


# 获取租赁费(管理费用)时间序列 -> getStmNoteOthers7631Series


# 获取租赁费(管理费用) -> getStmNoteOthers7631


# 获取工资薪酬(管理费用)时间序列 -> getStmNoteOthers7627Series


# 获取工资薪酬(管理费用) -> getStmNoteOthers7627


# 获取折旧摊销(管理费用)时间序列 -> getStmNoteOthers7629Series


# 获取折旧摊销(管理费用) -> getStmNoteOthers7629


# 获取财务费用(TTM)时间序列 -> getFinaExpenseTtM2Series


# 获取财务费用(TTM) -> getFinaExpenseTtM2


# 获取财务费用(TTM)_GSD时间序列 -> getFinaExpenseTtM3Series


# 获取财务费用(TTM)_GSD -> getFinaExpenseTtM3


# 获取财务费用时间序列 -> getStm07IsReItsFinanceFeeSeries


# 获取财务费用 -> getStm07IsReItsFinanceFee


# 获取财务费用:利息费用时间序列 -> getFinIntExpSeries


# 获取财务费用:利息费用 -> getFinIntExp


# 获取财务费用_CS时间序列 -> getFinExpCsSeries


# 获取财务费用_CS -> getFinExpCs


# 获取财务费用(TTM)_PIT时间序列 -> getFaFinaExpenseTtMSeries


# 获取财务费用(TTM)_PIT -> getFaFinaExpenseTtM


# 获取财务费用(TTM,只有最新数据)时间序列 -> getFinaExpenseTtMSeries


# 获取财务费用(TTM,只有最新数据) -> getFinaExpenseTtM


# 获取单季度.财务费用时间序列 -> getQfaFinExpIsSeries


# 获取单季度.财务费用 -> getQfaFinExpIs


# 获取单季度.财务费用:利息费用时间序列 -> getQfaFinIntExpSeries


# 获取单季度.财务费用:利息费用 -> getQfaFinIntExp


# 获取单季度.财务费用_CS时间序列 -> getQfaFinExpCsSeries


# 获取单季度.财务费用_CS -> getQfaFinExpCs


# 获取信用减值损失时间序列 -> getCreditImpairLoss2Series


# 获取信用减值损失 -> getCreditImpairLoss2


# 获取单季度.信用减值损失时间序列 -> getQfaCreditImpairLoss2Series


# 获取单季度.信用减值损失 -> getQfaCreditImpairLoss2


# 获取退保金时间序列 -> getPrepaySurRSeries


# 获取退保金 -> getPrepaySurR


# 获取单季度.退保金时间序列 -> getQfaPrepaySurRSeries


# 获取单季度.退保金 -> getQfaPrepaySurR


# 获取赔付支出净额时间序列 -> getNetClaimExpSeries


# 获取赔付支出净额 -> getNetClaimExp


# 获取单季度.赔付支出净额时间序列 -> getQfaNetClaimExpSeries


# 获取单季度.赔付支出净额 -> getQfaNetClaimExp


# 获取提取保险责任准备金时间序列 -> getNetInSurContRsRvSeries


# 获取提取保险责任准备金 -> getNetInSurContRsRv


# 获取单季度.提取保险责任准备金时间序列 -> getQfaNetInSurContRsRvSeries


# 获取单季度.提取保险责任准备金 -> getQfaNetInSurContRsRv


# 获取保单红利支出时间序列 -> getDvdExpInsuredSeries


# 获取保单红利支出 -> getDvdExpInsured


# 获取单季度.保单红利支出时间序列 -> getQfaDvdExpInsuredSeries


# 获取单季度.保单红利支出 -> getQfaDvdExpInsured


# 获取分保费用时间序列 -> getReinsuranceExpSeries


# 获取分保费用 -> getReinsuranceExp


# 获取摊回分保费用时间序列 -> getReInSurExpRecoverableSeries


# 获取摊回分保费用 -> getReInSurExpRecoverable


# 获取单季度.分保费用时间序列 -> getQfaReinsuranceExpSeries


# 获取单季度.分保费用 -> getQfaReinsuranceExp


# 获取单季度.摊回分保费用时间序列 -> getQfaReInSurExpRecoverableSeries


# 获取单季度.摊回分保费用 -> getQfaReInSurExpRecoverable


# 获取摊回赔付支出时间序列 -> getClaimExpRecoverableSeries


# 获取摊回赔付支出 -> getClaimExpRecoverable


# 获取单季度.摊回赔付支出时间序列 -> getQfaClaimExpRecoverableSeries


# 获取单季度.摊回赔付支出 -> getQfaClaimExpRecoverable


# 获取摊回保险责任准备金时间序列 -> getInSurRsRvRecoverableSeries


# 获取摊回保险责任准备金 -> getInSurRsRvRecoverable


# 获取单季度.摊回保险责任准备金时间序列 -> getQfaInSurRsRvRecoverableSeries


# 获取单季度.摊回保险责任准备金 -> getQfaInSurRsRvRecoverable


# 获取其他业务成本时间序列 -> getOtherOperExpSeries


# 获取其他业务成本 -> getOtherOperExp


# 获取其他业务成本(附注)时间序列 -> getStmNoteSeg1704Series


# 获取其他业务成本(附注) -> getStmNoteSeg1704


# 获取单季度.其他业务成本时间序列 -> getQfaOtherOperExpSeries


# 获取单季度.其他业务成本 -> getQfaOtherOperExp


# 获取其他经营净收益时间序列 -> getNetIncOtherOpsSeries


# 获取其他经营净收益 -> getNetIncOtherOps


# 获取单季度.其他经营净收益时间序列 -> getQfaNetIncOtherOpsSeries


# 获取单季度.其他经营净收益 -> getQfaNetIncOtherOps


# 获取公允价值变动净收益时间序列 -> getNetGainChgFvSeries


# 获取公允价值变动净收益 -> getNetGainChgFv


# 获取单季度.公允价值变动净收益时间序列 -> getQfaNetGainChgFvSeries


# 获取单季度.公允价值变动净收益 -> getQfaNetGainChgFv


# 获取投资净收益时间序列 -> getNetInvestIncSeries


# 获取投资净收益 -> getNetInvestInc


# 获取单季度.投资净收益时间序列 -> getQfaNetInvestIncSeries


# 获取单季度.投资净收益 -> getQfaNetInvestInc


# 获取净敞口套期收益时间序列 -> getNetExposureHedgeBenSeries


# 获取净敞口套期收益 -> getNetExposureHedgeBen


# 获取单季度.净敞口套期收益时间序列 -> getQfaNetExposureHedgeBenSeries


# 获取单季度.净敞口套期收益 -> getQfaNetExposureHedgeBen


# 获取汇兑净收益时间序列 -> getNetGainFxTransSeries


# 获取汇兑净收益 -> getNetGainFxTrans


# 获取单季度.汇兑净收益时间序列 -> getQfaNetGainFxTransSeries


# 获取单季度.汇兑净收益 -> getQfaNetGainFxTrans


# 获取其他收益时间序列 -> getOtherGrantsIncSeries


# 获取其他收益 -> getOtherGrantsInc


# 获取单季度.其他收益时间序列 -> getQfaOtherGrantsIncSeries


# 获取单季度.其他收益 -> getQfaOtherGrantsInc


# 获取营业利润差额(特殊报表科目)时间序列 -> getOpProfitGapSeries


# 获取营业利润差额(特殊报表科目) -> getOpProfitGap


# 获取营业利润差额说明(特殊报表科目)时间序列 -> getOpProfitGapDetailSeries


# 获取营业利润差额说明(特殊报表科目) -> getOpProfitGapDetail


# 获取营业利润差额(合计平衡项目)时间序列 -> getOpProfitNettingSeries


# 获取营业利润差额(合计平衡项目) -> getOpProfitNetting


# 获取营业利润率(OPM)预测机构家数(可选类型)时间序列 -> getWestInStNumOpMSeries


# 获取营业利润率(OPM)预测机构家数(可选类型) -> getWestInStNumOpM


# 获取营业利润/利润总额(TTM)时间序列 -> getTaxToOrTtMSeries


# 获取营业利润/利润总额(TTM) -> getTaxToOrTtM


# 获取营业利润(TTM)时间序列 -> getOpTtM2Series


# 获取营业利润(TTM) -> getOpTtM2


# 获取营业利润/利润总额_GSD时间序列 -> getWgsDOpToEBTSeries


# 获取营业利润/利润总额_GSD -> getWgsDOpToEBT


# 获取营业利润/利润总额(TTM)_GSD时间序列 -> getOpToEBTTtM2Series


# 获取营业利润/利润总额(TTM)_GSD -> getOpToEBTTtM2


# 获取营业利润(TTM)_GSD时间序列 -> getOpTtM3Series


# 获取营业利润(TTM)_GSD -> getOpTtM3


# 获取营业利润_GSD时间序列 -> getWgsDEbItOperSeries


# 获取营业利润_GSD -> getWgsDEbItOper


# 获取营业利润时间序列 -> getStm07IsReItsProfitSeries


# 获取营业利润 -> getStm07IsReItsProfit


# 获取营业利润/利润总额(TTM)_PIT时间序列 -> getFaOpToPbtTtMSeries


# 获取营业利润/利润总额(TTM)_PIT -> getFaOpToPbtTtM


# 获取营业利润(TTM)_PIT时间序列 -> getFaOpTtMSeries


# 获取营业利润(TTM)_PIT -> getFaOpTtM


# 获取营业利润(TTM,只有最新数据)时间序列 -> getOpTtMSeries


# 获取营业利润(TTM,只有最新数据) -> getOpTtM


# 获取非营业利润/利润总额(TTM)_GSD时间序列 -> getNonOpToEBTTtMSeries


# 获取非营业利润/利润总额(TTM)_GSD -> getNonOpToEBTTtM


# 获取非营业利润(TTM)_GSD时间序列 -> getNonOpTtMSeries


# 获取非营业利润(TTM)_GSD -> getNonOpTtM


# 获取预测营业利润率(OPM)平均值(可选类型)时间序列 -> getWestAvGoPmSeries


# 获取预测营业利润率(OPM)平均值(可选类型) -> getWestAvGoPm


# 获取预测营业利润率(OPM)最大值(可选类型)时间序列 -> getWestMaxOpMSeries


# 获取预测营业利润率(OPM)最大值(可选类型) -> getWestMaxOpM


# 获取预测营业利润率(OPM)最小值(可选类型)时间序列 -> getWestMinoPmSeries


# 获取预测营业利润率(OPM)最小值(可选类型) -> getWestMinoPm


# 获取预测营业利润率(OPM)中值(可选类型)时间序列 -> getWestMediaOpMSeries


# 获取预测营业利润率(OPM)中值(可选类型) -> getWestMediaOpM


# 获取预测营业利润率(OPM)标准差值(可选类型)时间序列 -> getWestStDoPmSeries


# 获取预测营业利润率(OPM)标准差值(可选类型) -> getWestStDoPm


# 获取预测营业利润Surprise(可选类型)时间序列 -> getWestAvgOperatingProfitSurpriseSeries


# 获取预测营业利润Surprise(可选类型) -> getWestAvgOperatingProfitSurprise


# 获取预测营业利润Surprise百分比(可选类型)时间序列 -> getWestAvgOperatingProfitSurprisePctSeries


# 获取预测营业利润Surprise百分比(可选类型) -> getWestAvgOperatingProfitSurprisePct


# 获取每股营业利润_PIT时间序列 -> getFaOppSSeries


# 获取每股营业利润_PIT -> getFaOppS


# 获取每股营业利润(TTM)_PIT时间序列 -> getFaOppSTtMSeries


# 获取每股营业利润(TTM)_PIT -> getFaOppSTtM


# 获取一致预测营业利润(FY1)时间序列 -> getWestAvgOperatingProfitFy1Series


# 获取一致预测营业利润(FY1) -> getWestAvgOperatingProfitFy1


# 获取一致预测营业利润(FY2)时间序列 -> getWestAvgOperatingProfitFy2Series


# 获取一致预测营业利润(FY2) -> getWestAvgOperatingProfitFy2


# 获取一致预测营业利润(FY3)时间序列 -> getWestAvgOperatingProfitFy3Series


# 获取一致预测营业利润(FY3) -> getWestAvgOperatingProfitFy3


# 获取单季度.营业利润_GSD时间序列 -> getWgsDQfaEbItOperSeries


# 获取单季度.营业利润_GSD -> getWgsDQfaEbItOper


# 获取单季度.营业利润时间序列 -> getQfaOpProfitSeries


# 获取单季度.营业利润 -> getQfaOpProfit


# 获取营业外收入时间序列 -> getNonOperRevSeries


# 获取营业外收入 -> getNonOperRev


# 获取单季度.营业外收入时间序列 -> getQfaNonOperRevSeries


# 获取单季度.营业外收入 -> getQfaNonOperRev


# 获取政府补助_营业外收入时间序列 -> getStmNoteOthers4504Series


# 获取政府补助_营业外收入 -> getStmNoteOthers4504


# 获取营业外支出时间序列 -> getNonOperExpSeries


# 获取营业外支出 -> getNonOperExp


# 获取单季度.营业外支出时间序列 -> getQfaNonOperExpSeries


# 获取单季度.营业外支出 -> getQfaNonOperExp


# 获取利润总额差额(特殊报表科目)时间序列 -> getProfitGapSeries


# 获取利润总额差额(特殊报表科目) -> getProfitGap


# 获取利润总额差额说明(特殊报表科目)时间序列 -> getProfitGapDetailSeries


# 获取利润总额差额说明(特殊报表科目) -> getProfitGapDetail


# 获取利润总额差额(合计平衡项目)时间序列 -> getProfitNettingSeries


# 获取利润总额差额(合计平衡项目) -> getProfitNetting


# 获取利润总额(TTM)时间序列 -> getEBtTtM2Series


# 获取利润总额(TTM) -> getEBtTtM2


# 获取利润总额(TTM)_GSD时间序列 -> getEBtTtM3Series


# 获取利润总额(TTM)_GSD -> getEBtTtM3


# 获取利润总额时间序列 -> getStm07IsReItsSumProfitSeries


# 获取利润总额 -> getStm07IsReItsSumProfit


# 获取利润总额(TTM)_PIT时间序列 -> getFaEBtTtMSeries


# 获取利润总额(TTM)_PIT -> getFaEBtTtM


# 获取利润总额(TTM,只有最新数据)时间序列 -> getEBtTtMSeries


# 获取利润总额(TTM,只有最新数据) -> getEBtTtM


# 获取预测利润总额Surprise(可选类型)时间序列 -> getWestAvGebTSurpriseSeries


# 获取预测利润总额Surprise(可选类型) -> getWestAvGebTSurprise


# 获取预测利润总额Surprise百分比(可选类型)时间序列 -> getWestAvGebTSurprisePctSeries


# 获取预测利润总额Surprise百分比(可选类型) -> getWestAvGebTSurprisePct


# 获取税项/利润总额(TTM)时间序列 -> getTaxToEBTTtMSeries


# 获取税项/利润总额(TTM) -> getTaxToEBTTtM


# 获取税项/利润总额_GSD时间序列 -> getWgsDTaxToEBTSeries


# 获取税项/利润总额_GSD -> getWgsDTaxToEBT


# 获取税项/利润总额(TTM)_GSD时间序列 -> getTaxToEBTTtM2Series


# 获取税项/利润总额(TTM)_GSD -> getTaxToEBTTtM2


# 获取税项/利润总额(TTM)_PIT时间序列 -> getFaTaxToProfitBtTtMSeries


# 获取税项/利润总额(TTM)_PIT -> getFaTaxToProfitBtTtM


# 获取一致预测利润总额(FY1)时间序列 -> getWestAvGebTFy1Series


# 获取一致预测利润总额(FY1) -> getWestAvGebTFy1


# 获取一致预测利润总额(FY2)时间序列 -> getWestAvGebTFy2Series


# 获取一致预测利润总额(FY2) -> getWestAvGebTFy2


# 获取一致预测利润总额(FY3)时间序列 -> getWestAvGebTFy3Series


# 获取一致预测利润总额(FY3) -> getWestAvGebTFy3


# 获取单季度.利润总额时间序列 -> getQfaToTProfitSeries


# 获取单季度.利润总额 -> getQfaToTProfit


# 获取未确认的投资损失_BS时间序列 -> getUnconfirmedInvestLossBsSeries


# 获取未确认的投资损失_BS -> getUnconfirmedInvestLossBs


# 获取未确认的投资损失时间序列 -> getUnconfirmedInvestLossIsSeries


# 获取未确认的投资损失 -> getUnconfirmedInvestLossIs


# 获取未确认的投资损失_CS时间序列 -> getUnconfirmedInvestLossCsSeries


# 获取未确认的投资损失_CS -> getUnconfirmedInvestLossCs


# 获取单季度.未确认的投资损失时间序列 -> getQfaUnconfirmedInvestLossIsSeries


# 获取单季度.未确认的投资损失 -> getQfaUnconfirmedInvestLossIs


# 获取单季度.未确认的投资损失_CS时间序列 -> getQfaUnconfirmedInvestLossCsSeries


# 获取单季度.未确认的投资损失_CS -> getQfaUnconfirmedInvestLossCs


# 获取净利润差额(特殊报表科目)时间序列 -> getNetProfitIsGapSeries


# 获取净利润差额(特殊报表科目) -> getNetProfitIsGap


# 获取净利润差额说明(特殊报表科目)时间序列 -> getNetProfitIsGapDetailSeries


# 获取净利润差额说明(特殊报表科目) -> getNetProfitIsGapDetail


# 获取净利润差额(合计平衡项目)时间序列 -> getNetProfitIsNettingSeries


# 获取净利润差额(合计平衡项目) -> getNetProfitIsNetting


# 获取净利润(TTM)_PIT时间序列 -> getFaProfitTtMSeries


# 获取净利润(TTM)_PIT -> getFaProfitTtM


# 获取净利润(TTM)时间序列 -> getProfitTtM2Series


# 获取净利润(TTM) -> getProfitTtM2


# 获取净利润(TTM)_GSD时间序列 -> getProfitTtM3Series


# 获取净利润(TTM)_GSD -> getProfitTtM3


# 获取净利润(Non-GAAP)_GSD时间序列 -> getWgsDNoGaapProfitSeries


# 获取净利润(Non-GAAP)_GSD -> getWgsDNoGaapProfit


# 获取净利润_GSD时间序列 -> getWgsDNetIncSeries


# 获取净利润_GSD -> getWgsDNetInc


# 获取净利润_CS_GSD时间序列 -> getWgsDNetIncCfSeries


# 获取净利润_CS_GSD -> getWgsDNetIncCf


# 获取净利润时间序列 -> getStm07IsReItsNetProfitSeries


# 获取净利润 -> getStm07IsReItsNetProfit


# 获取净利润_CS时间序列 -> getNetProfitCsSeries


# 获取净利润_CS -> getNetProfitCs


# 获取净利润_FUND时间序列 -> getStmIs79Series


# 获取净利润_FUND -> getStmIs79


# 获取净利润(合计)_FUND时间序列 -> getStmIs79TotalSeries


# 获取净利润(合计)_FUND -> getStmIs79Total


# 获取备考净利润(FY0,并购后)时间序列 -> getManetProfitFy0Series


# 获取备考净利润(FY0,并购后) -> getManetProfitFy0


# 获取备考净利润(FY1,并购后)时间序列 -> getManetProfitFy1Series


# 获取备考净利润(FY1,并购后) -> getManetProfitFy1


# 获取备考净利润(FY2,并购后)时间序列 -> getManetProfitFy2Series


# 获取备考净利润(FY2,并购后) -> getManetProfitFy2


# 获取备考净利润(FY3,并购后)时间序列 -> getManetProfitFy3Series


# 获取备考净利润(FY3,并购后) -> getManetProfitFy3


# 获取预测净利润Surprise(可选类型)时间序列 -> getWestNetProfitSurpriseSeries


# 获取预测净利润Surprise(可选类型) -> getWestNetProfitSurprise


# 获取预测净利润Surprise百分比(可选类型)时间序列 -> getWestNetProfitSurprisePctSeries


# 获取预测净利润Surprise百分比(可选类型) -> getWestNetProfitSurprisePct


# 获取八季度净利润变化趋势_PIT时间序列 -> getFaEarnMom8QTrSeries


# 获取八季度净利润变化趋势_PIT -> getFaEarnMom8QTr


# 获取一致预测净利润(FY1)时间序列 -> getWestNetProfitFy1Series


# 获取一致预测净利润(FY1) -> getWestNetProfitFy1


# 获取一致预测净利润(FY2)时间序列 -> getWestNetProfitFy2Series


# 获取一致预测净利润(FY2) -> getWestNetProfitFy2


# 获取一致预测净利润(FY3)时间序列 -> getWestNetProfitFy3Series


# 获取一致预测净利润(FY3) -> getWestNetProfitFy3


# 获取持续经营净利润/税后利润(TTM)_GSD时间序列 -> getConnPToProfitTtMSeries


# 获取持续经营净利润/税后利润(TTM)_GSD -> getConnPToProfitTtM


# 获取持续经营净利润(TTM)_GSD时间序列 -> getConnPTtMSeries


# 获取持续经营净利润(TTM)_GSD -> getConnPTtM


# 获取单季度.净利润(Non-GAAP)_GSD时间序列 -> getWgsDQfaNoGaapProfitSeries


# 获取单季度.净利润(Non-GAAP)_GSD -> getWgsDQfaNoGaapProfit


# 获取持续经营净利润_GSD时间序列 -> getWgsDContinueOperSeries


# 获取持续经营净利润_GSD -> getWgsDContinueOper


# 获取单季度.净利润_GSD时间序列 -> getWgsDQfaNetIncSeries


# 获取单季度.净利润_GSD -> getWgsDQfaNetInc


# 获取单季度.净利润_CS_GSD时间序列 -> getWgsDQfaNetIncCfSeries


# 获取单季度.净利润_CS_GSD -> getWgsDQfaNetIncCf


# 获取持续经营净利润时间序列 -> getNetProfitContinuedSeries


# 获取持续经营净利润 -> getNetProfitContinued


# 获取终止经营净利润时间序列 -> getNetProfitDiscontinuedSeries


# 获取终止经营净利润 -> getNetProfitDiscontinued


# 获取单季度.净利润时间序列 -> getQfaNetProfitIsSeries


# 获取单季度.净利润 -> getQfaNetProfitIs


# 获取单季度.净利润_CS时间序列 -> getQfaNetProfitCsSeries


# 获取单季度.净利润_CS -> getQfaNetProfitCs


# 获取本期实现净利润时间序列 -> getStmNoteProfitApr2Series


# 获取本期实现净利润 -> getStmNoteProfitApr2


# 获取一致预测净利润(FY1)变化率_1M_PIT时间序列 -> getWestNetProfitFy11MSeries


# 获取一致预测净利润(FY1)变化率_1M_PIT -> getWestNetProfitFy11M


# 获取一致预测净利润(FY1)变化率_3M_PIT时间序列 -> getWestNetProfitFy13MSeries


# 获取一致预测净利润(FY1)变化率_3M_PIT -> getWestNetProfitFy13M


# 获取一致预测净利润(FY1)变化率_6M_PIT时间序列 -> getWestNetProfitFy16MSeries


# 获取一致预测净利润(FY1)变化率_6M_PIT -> getWestNetProfitFy16M


# 获取一致预测净利润(FY1)的变化_1M_PIT时间序列 -> getWestNetProfitFy1Chg1MSeries


# 获取一致预测净利润(FY1)的变化_1M_PIT -> getWestNetProfitFy1Chg1M


# 获取一致预测净利润(FY1)的变化_3M_PIT时间序列 -> getWestNetProfitFy1Chg3MSeries


# 获取一致预测净利润(FY1)的变化_3M_PIT -> getWestNetProfitFy1Chg3M


# 获取一致预测净利润(FY1)的变化_6M_PIT时间序列 -> getWestNetProfitFy1Chg6MSeries


# 获取一致预测净利润(FY1)的变化_6M_PIT -> getWestNetProfitFy1Chg6M


# 获取一致预测净利润(FY1)标准差_PIT时间序列 -> getWestStdNetProfitFy1Series


# 获取一致预测净利润(FY1)标准差_PIT -> getWestStdNetProfitFy1


# 获取一致预测净利润(FY1)最大与一致预测净利润(FY1)最小值的变化率_PIT时间序列 -> getWestNetProfitMaxMinFy1Series


# 获取一致预测净利润(FY1)最大与一致预测净利润(FY1)最小值的变化率_PIT -> getWestNetProfitMaxMinFy1


# 获取非持续经营净利润(TTM)_GSD时间序列 -> getNonConnPTtMSeries


# 获取非持续经营净利润(TTM)_GSD -> getNonConnPTtM


# 获取非持续经营净利润_GSD时间序列 -> getWgsDDiscOperSeries


# 获取非持续经营净利润_GSD -> getWgsDDiscOper


# 获取归属普通股东净利润_GSD时间序列 -> getWgsDNetIncDilSeries


# 获取归属普通股东净利润_GSD -> getWgsDNetIncDil


# 获取归属母公司股东的净利润(TTM)_VAL_PIT时间序列 -> getNetProfitTtMSeries


# 获取归属母公司股东的净利润(TTM)_VAL_PIT -> getNetProfitTtM


# 获取归属母公司股东的净利润(TTM)时间序列 -> getNetProfitTtM2Series


# 获取归属母公司股东的净利润(TTM) -> getNetProfitTtM2


# 获取归属母公司股东的净利润(TTM)_GSD时间序列 -> getNetProfitTtM3Series


# 获取归属母公司股东的净利润(TTM)_GSD -> getNetProfitTtM3


# 获取扣除非经常损益后净利润_GSD时间序列 -> getWgsDDeductedProfitSeries


# 获取扣除非经常损益后净利润_GSD -> getWgsDDeductedProfit


# 获取单季度.持续经营净利润_GSD时间序列 -> getWgsDQfaContinueOperSeries


# 获取单季度.持续经营净利润_GSD -> getWgsDQfaContinueOper


# 获取归属母公司股东的净利润时间序列 -> getNpBelongToParComShSeries


# 获取归属母公司股东的净利润 -> getNpBelongToParComSh


# 获取单季度.持续经营净利润时间序列 -> getQfaNetProfitContinuedSeries


# 获取单季度.持续经营净利润 -> getQfaNetProfitContinued


# 获取单季度.终止经营净利润时间序列 -> getQfaNetProfitDiscontinuedSeries


# 获取单季度.终止经营净利润 -> getQfaNetProfitDiscontinued


# 获取归属母公司股东的净利润(TTM)_PIT时间序列 -> getFaNetProfitTtMSeries


# 获取归属母公司股东的净利润(TTM)_PIT -> getFaNetProfitTtM


# 获取单季度.非持续经营净利润_GSD时间序列 -> getWgsDQfaDiscOperSeries


# 获取单季度.非持续经营净利润_GSD -> getWgsDQfaDiscOper


# 获取单季度.归属普通股东净利润_GSD时间序列 -> getWgsDQfaNetIncDilSeries


# 获取单季度.归属普通股东净利润_GSD -> getWgsDQfaNetIncDil


# 获取单季度.扣除非经常损益后净利润_GSD时间序列 -> getWgsDQfaDeductedProfitSeries


# 获取单季度.扣除非经常损益后净利润_GSD -> getWgsDQfaDeductedProfit


# 获取单季度.归属母公司股东的净利润时间序列 -> getQfaNpBelongToParComShSeries


# 获取单季度.归属母公司股东的净利润 -> getQfaNpBelongToParComSh


# 获取本期经营活动产生的基金净值变动数(本期净利润)时间序列 -> getStmNavChange6Series


# 获取本期经营活动产生的基金净值变动数(本期净利润) -> getStmNavChange6


# 获取少数股东损益(TTM)时间序列 -> getMinorityInterestTtMSeries


# 获取少数股东损益(TTM) -> getMinorityInterestTtM


# 获取少数股东损益(TTM)_GSD时间序列 -> getMinorityInterestTtM2Series


# 获取少数股东损益(TTM)_GSD -> getMinorityInterestTtM2


# 获取少数股东损益_GSD时间序列 -> getWgsDMinIntExpSeries


# 获取少数股东损益_GSD -> getWgsDMinIntExp


# 获取少数股东损益时间序列 -> getMinorityIntIncSeries


# 获取少数股东损益 -> getMinorityIntInc


# 获取少数股东损益影响数时间序列 -> getStmNoteEoItems23Series


# 获取少数股东损益影响数 -> getStmNoteEoItems23


# 获取少数股东损益(TTM)_PIT时间序列 -> getFaMinInterestTtMSeries


# 获取少数股东损益(TTM)_PIT -> getFaMinInterestTtM


# 获取单季度.少数股东损益_GSD时间序列 -> getWgsDQfaMinIntExpSeries


# 获取单季度.少数股东损益_GSD -> getWgsDQfaMinIntExp


# 获取单季度.少数股东损益时间序列 -> getQfaMinorityIntIncSeries


# 获取单季度.少数股东损益 -> getQfaMinorityIntInc


# 获取基本每股收益_GSD时间序列 -> getWgsDEpsBasicSeries


# 获取基本每股收益_GSD -> getWgsDEpsBasic


# 获取基本每股收益时间序列 -> getEpsBasicIsSeries


# 获取基本每股收益 -> getEpsBasicIs


# 获取基本每股收益_PIT时间序列 -> getFaEpsBasicSeries


# 获取基本每股收益_PIT -> getFaEpsBasic


# 获取上年同期基本每股收益时间序列 -> getProfitNoticeLastYearBasicEarnSeries


# 获取上年同期基本每股收益 -> getProfitNoticeLastYearBasicEarn


# 获取单季度.基本每股收益EPS_GSD时间序列 -> getWgsDQfaEpsBasicSeries


# 获取单季度.基本每股收益EPS_GSD -> getWgsDQfaEpsBasic


# 获取稀释每股收益_GSD时间序列 -> getWgsDEpsDilutedSeries


# 获取稀释每股收益_GSD -> getWgsDEpsDiluted


# 获取稀释每股收益时间序列 -> getEpsDilutedIsSeries


# 获取稀释每股收益 -> getEpsDilutedIs


# 获取稀释每股收益_PIT时间序列 -> getFaEpsDilutedSeries


# 获取稀释每股收益_PIT -> getFaEpsDiluted


# 获取单季度.稀释每股收益EPS_GSD时间序列 -> getWgsDQfaEpsDilutedSeries


# 获取单季度.稀释每股收益EPS_GSD -> getWgsDQfaEpsDiluted


# 获取单季度.保费总收入时间序列 -> getQfaToTPremIncSeries


# 获取单季度.保费总收入 -> getQfaToTPremInc


# 获取单季度.毛利_GSD时间序列 -> getWgsDQfaGrossMargin2Series


# 获取单季度.毛利_GSD -> getWgsDQfaGrossMargin2


# 获取单季度.毛利时间序列 -> getQfaGrossMarginSeries


# 获取单季度.毛利 -> getQfaGrossMargin


# 获取主营收入构成时间序列 -> getSegmentSalesSeries


# 获取主营收入构成 -> getSegmentSales


# 获取海外业务收入时间序列 -> getStmNoteSeg1501Series


# 获取海外业务收入 -> getStmNoteSeg1501


# 获取期初未分配利润时间序列 -> getStmNoteProfitApr1Series


# 获取期初未分配利润 -> getStmNoteProfitApr1


# 获取支付普通股股利时间序列 -> getStmNoteProfitApr4Series


# 获取支付普通股股利 -> getStmNoteProfitApr4


# 获取提取法定盈余公积时间序列 -> getStmNoteProfitApr5Series


# 获取提取法定盈余公积 -> getStmNoteProfitApr5


# 获取提取任意盈余公积时间序列 -> getStmNoteProfitApr6Series


# 获取提取任意盈余公积 -> getStmNoteProfitApr6


# 获取转增股本时间序列 -> getStmNoteProfitApr8Series


# 获取转增股本 -> getStmNoteProfitApr8


# 获取每股转增股本(已宣告)时间序列 -> getDivCapitalization2Series


# 获取每股转增股本(已宣告) -> getDivCapitalization2


# 获取每股转增股本时间序列 -> getDivCapitalizationSeries


# 获取每股转增股本 -> getDivCapitalization


# 获取年末未分配利润时间序列 -> getStmNoteProfitApr9Series


# 获取年末未分配利润 -> getStmNoteProfitApr9


# 获取提取一般风险准备时间序列 -> getStmNoteProfitApr10Series


# 获取提取一般风险准备 -> getStmNoteProfitApr10


# 获取担保发生额合计时间序列 -> getStmNoteGuarantee1Series


# 获取担保发生额合计 -> getStmNoteGuarantee1


# 获取对控股子公司担保发生额合计时间序列 -> getStmNoteGuarantee4Series


# 获取对控股子公司担保发生额合计 -> getStmNoteGuarantee4


# 获取担保余额合计时间序列 -> getStmNoteGuarantee2Series


# 获取担保余额合计 -> getStmNoteGuarantee2


# 获取关联担保余额合计时间序列 -> getStmNoteGuarantee3Series


# 获取关联担保余额合计 -> getStmNoteGuarantee3


# 获取违规担保总额时间序列 -> getStmNoteGuarantee5Series


# 获取违规担保总额 -> getStmNoteGuarantee5


# 获取向关联方销售产品金额时间序列 -> getStmNoteAssociated1Series


# 获取向关联方销售产品金额 -> getStmNoteAssociated1


# 获取向关联方采购产品金额时间序列 -> getStmNoteAssociated2Series


# 获取向关联方采购产品金额 -> getStmNoteAssociated2


# 获取向关联方提供资金发生额时间序列 -> getStmNoteAssociated3Series


# 获取向关联方提供资金发生额 -> getStmNoteAssociated3


# 获取向关联方提供资金余额时间序列 -> getStmNoteAssociated4Series


# 获取向关联方提供资金余额 -> getStmNoteAssociated4


# 获取关联方向上市公司提供资金发生额时间序列 -> getStmNoteAssociated5Series


# 获取关联方向上市公司提供资金发生额 -> getStmNoteAssociated5


# 获取关联方向上市公司提供资金余额时间序列 -> getStmNoteAssociated6Series


# 获取关联方向上市公司提供资金余额 -> getStmNoteAssociated6


# 获取审计单位时间序列 -> getStmNoteAuditAgencySeries


# 获取审计单位 -> getStmNoteAuditAgency


# 获取内控_审计单位时间序列 -> getStmNoteInAuditAgencySeries


# 获取内控_审计单位 -> getStmNoteInAuditAgency


# 获取签字注册会计师时间序列 -> getStmNoteAuditCpaSeries


# 获取签字注册会计师 -> getStmNoteAuditCpa


# 获取当期实付审计费用时间序列 -> getStmNoteAuditExpenseSeries


# 获取当期实付审计费用 -> getStmNoteAuditExpense


# 获取审计报告披露日期时间序列 -> getStmNoteAuditDateSeries


# 获取审计报告披露日期 -> getStmNoteAuditDate


# 获取审计结果说明时间序列 -> getStmNoteAuditInterpretationSeries


# 获取审计结果说明 -> getStmNoteAuditInterpretation


# 获取内控_审计结果说明时间序列 -> getStmNoteInAuditInterpretationSeries


# 获取内控_审计结果说明 -> getStmNoteInAuditInterpretation


# 获取关键审计事项时间序列 -> getStmNoteAuditKamSeries


# 获取关键审计事项 -> getStmNoteAuditKam


# 获取内控_签字审计师时间序列 -> getStmNoteInAuditCpaSeries


# 获取内控_签字审计师 -> getStmNoteInAuditCpa


# 获取内控报告披露日期时间序列 -> getStmNoteInAuditIssuingDateSeries


# 获取内控报告披露日期 -> getStmNoteInAuditIssuingDate


# 获取存货明细-原材料时间序列 -> getStmNoteInv1Series


# 获取存货明细-原材料 -> getStmNoteInv1


# 获取存货明细-在产品时间序列 -> getStmNoteInv2Series


# 获取存货明细-在产品 -> getStmNoteInv2


# 获取存货明细-产成品时间序列 -> getStmNoteInv3Series


# 获取存货明细-产成品 -> getStmNoteInv3


# 获取存货明细-低值易耗品时间序列 -> getStmNoteInv4Series


# 获取存货明细-低值易耗品 -> getStmNoteInv4


# 获取存货明细-包装物时间序列 -> getStmNoteInv5Series


# 获取存货明细-包装物 -> getStmNoteInv5


# 获取存货明细-委托加工材料时间序列 -> getStmNoteInv6Series


# 获取存货明细-委托加工材料 -> getStmNoteInv6


# 获取存货明细-委托代销商品时间序列 -> getStmNoteInv7Series


# 获取存货明细-委托代销商品 -> getStmNoteInv7


# 获取存货明细-已加工未结算时间序列 -> getStmNoteInv8Series


# 获取存货明细-已加工未结算 -> getStmNoteInv8


# 获取存货明细-发出商品时间序列 -> getStmNoteInvGoodsShipSeries


# 获取存货明细-发出商品 -> getStmNoteInvGoodsShip


# 获取存货合计时间序列 -> getStmNoteInvToTSeries


# 获取存货合计 -> getStmNoteInvToT


# 获取应收账款余额时间序列 -> getStmNoteArTotalSeries


# 获取应收账款余额 -> getStmNoteArTotal


# 获取应收账款-金额时间序列 -> getStmNoteAr1Series


# 获取应收账款-金额 -> getStmNoteAr1


# 获取应收账款-比例时间序列 -> getStmNoteAr2Series


# 获取应收账款-比例 -> getStmNoteAr2


# 获取应收账款-坏账准备时间序列 -> getStmNoteAr3Series


# 获取应收账款-坏账准备 -> getStmNoteAr3


# 获取应收账款-坏账准备(按性质)时间序列 -> getStmNoteArCatSeries


# 获取应收账款-坏账准备(按性质) -> getStmNoteArCat


# 获取应收账款-主要欠款人时间序列 -> getStmNoteArDebtorSeries


# 获取应收账款-主要欠款人 -> getStmNoteArDebtor


# 获取应收账款-主要欠款人名称时间序列 -> getStmNoteArDebtorNameSeries


# 获取应收账款-主要欠款人名称 -> getStmNoteArDebtorName


# 获取其他应收款-金额时间序列 -> getStmNoteOrSeries


# 获取其他应收款-金额 -> getStmNoteOr


# 获取坏账准备合计时间序列 -> getStmNoteReserve1Series


# 获取坏账准备合计 -> getStmNoteReserve1


# 获取坏账准备-应收账款时间序列 -> getStmNoteReserve2Series


# 获取坏账准备-应收账款 -> getStmNoteReserve2


# 获取坏账准备-其它应收款时间序列 -> getStmNoteReserve3Series


# 获取坏账准备-其它应收款 -> getStmNoteReserve3


# 获取短期投资跌价准备合计时间序列 -> getStmNoteReserve4Series


# 获取短期投资跌价准备合计 -> getStmNoteReserve4


# 获取短期投资跌价准备-股票投资时间序列 -> getStmNoteReserve5Series


# 获取短期投资跌价准备-股票投资 -> getStmNoteReserve5


# 获取短期投资跌价准备-债券投资时间序列 -> getStmNoteReserve6Series


# 获取短期投资跌价准备-债券投资 -> getStmNoteReserve6


# 获取存货跌价准备合计时间序列 -> getStmNoteReserve7Series


# 获取存货跌价准备合计 -> getStmNoteReserve7


# 获取存货跌价准备-库存商品时间序列 -> getStmNoteReserve8Series


# 获取存货跌价准备-库存商品 -> getStmNoteReserve8


# 获取存货跌价准备-原材料时间序列 -> getStmNoteReserve9Series


# 获取存货跌价准备-原材料 -> getStmNoteReserve9


# 获取存货跌价准备-产成品时间序列 -> getStmNoteReserve10Series


# 获取存货跌价准备-产成品 -> getStmNoteReserve10


# 获取存货跌价准备-低值易耗品时间序列 -> getStmNoteReserve11Series


# 获取存货跌价准备-低值易耗品 -> getStmNoteReserve11


# 获取存货跌价准备-开发成本时间序列 -> getStmNoteReserve12Series


# 获取存货跌价准备-开发成本 -> getStmNoteReserve12


# 获取存货跌价准备-包装物时间序列 -> getStmNoteReserve13Series


# 获取存货跌价准备-包装物 -> getStmNoteReserve13


# 获取存货跌价准备-在途物资时间序列 -> getStmNoteReserve14Series


# 获取存货跌价准备-在途物资 -> getStmNoteReserve14


# 获取存货跌价准备-在产品时间序列 -> getStmNoteReserve15Series


# 获取存货跌价准备-在产品 -> getStmNoteReserve15


# 获取存货跌价准备-开发产品时间序列 -> getStmNoteReserve16Series


# 获取存货跌价准备-开发产品 -> getStmNoteReserve16


# 获取存货跌价准备-自制半成品时间序列 -> getStmNoteReserve17Series


# 获取存货跌价准备-自制半成品 -> getStmNoteReserve17


# 获取长期投资减值准备合计时间序列 -> getStmNoteReserve18Series


# 获取长期投资减值准备合计 -> getStmNoteReserve18


# 获取长期投资减值准备-长期股权投资时间序列 -> getStmNoteReserve19Series


# 获取长期投资减值准备-长期股权投资 -> getStmNoteReserve19


# 获取长期投资减值准备-长期债权投资时间序列 -> getStmNoteReserve20Series


# 获取长期投资减值准备-长期债权投资 -> getStmNoteReserve20


# 获取在建工程减值准备时间序列 -> getStmNoteReserve35Series


# 获取在建工程减值准备 -> getStmNoteReserve35


# 获取委托贷款减值准备时间序列 -> getStmNoteReserve36Series


# 获取委托贷款减值准备 -> getStmNoteReserve36


# 获取自营证券跌价准备时间序列 -> getStmNoteReserve37Series


# 获取自营证券跌价准备 -> getStmNoteReserve37


# 获取贷款呆账准备时间序列 -> getStmNoteReserve38Series


# 获取贷款呆账准备 -> getStmNoteReserve38


# 获取投资性房地产-原值时间序列 -> getStmNoteAssetDetail5Series


# 获取投资性房地产-原值 -> getStmNoteAssetDetail5


# 获取投资性房地产-累计折旧时间序列 -> getStmNoteAssetDetail6Series


# 获取投资性房地产-累计折旧 -> getStmNoteAssetDetail6


# 获取投资性房地产-减值准备时间序列 -> getStmNoteAssetDetail7Series


# 获取投资性房地产-减值准备 -> getStmNoteAssetDetail7


# 获取投资性房地产-净额时间序列 -> getStmNoteAssetDetail8Series


# 获取投资性房地产-净额 -> getStmNoteAssetDetail8


# 获取存放中央银行法定准备金时间序列 -> getStmNoteCashDeposits1Series


# 获取存放中央银行法定准备金 -> getStmNoteCashDeposits1


# 获取存放中央银行超额存款准备金时间序列 -> getStmNoteCashDeposits2Series


# 获取存放中央银行超额存款准备金 -> getStmNoteCashDeposits2


# 获取人民币存款时间序列 -> getStmNoteDpsT4405Series


# 获取人民币存款 -> getStmNoteDpsT4405


# 获取美元存款(折算人民币)时间序列 -> getStmNoteDpsT4406Series


# 获取美元存款(折算人民币) -> getStmNoteDpsT4406


# 获取日元存款(折算人民币)时间序列 -> getStmNoteDpsT4407Series


# 获取日元存款(折算人民币) -> getStmNoteDpsT4407


# 获取欧元存款(折算人民币)时间序列 -> getStmNoteDpsT4408Series


# 获取欧元存款(折算人民币) -> getStmNoteDpsT4408


# 获取港币存款(折算人民币)时间序列 -> getStmNoteDpsT4409Series


# 获取港币存款(折算人民币) -> getStmNoteDpsT4409


# 获取英镑存款(折算人民币)时间序列 -> getStmNoteDpsT4410Series


# 获取英镑存款(折算人民币) -> getStmNoteDpsT4410


# 获取其他货币存款(折算人民币)时间序列 -> getStmNoteDpsT4411Series


# 获取其他货币存款(折算人民币) -> getStmNoteDpsT4411


# 获取一年内到期的应付债券时间序列 -> getStmNoteOthers7637Series


# 获取一年内到期的应付债券 -> getStmNoteOthers7637


# 获取税收返还、减免时间序列 -> getStmNoteEoItems7Series


# 获取税收返还、减免 -> getStmNoteEoItems7


# 获取政府补助时间序列 -> getStmNoteEoItems8Series


# 获取政府补助 -> getStmNoteEoItems8


# 获取资金占用费时间序列 -> getStmNoteEoItems9Series


# 获取资金占用费 -> getStmNoteEoItems9


# 获取企业合并产生的损益时间序列 -> getStmNoteEoItems10Series


# 获取企业合并产生的损益 -> getStmNoteEoItems10


# 获取委托投资损益时间序列 -> getStmNoteEoItems12Series


# 获取委托投资损益 -> getStmNoteEoItems12


# 获取债务重组损益时间序列 -> getStmNoteEoItems14Series


# 获取债务重组损益 -> getStmNoteEoItems14


# 获取企业重组费用时间序列 -> getStmNoteEoItems15Series


# 获取企业重组费用 -> getStmNoteEoItems15


# 获取交易产生的损益时间序列 -> getStmNoteEoItems16Series


# 获取交易产生的损益 -> getStmNoteEoItems16


# 获取同一控制下企业合并产生的子公司当期净损益时间序列 -> getStmNoteEoItems17Series


# 获取同一控制下企业合并产生的子公司当期净损益 -> getStmNoteEoItems17


# 获取单独进行减值测试的应收款项减值准备转回时间序列 -> getStmNoteEoItems29Series


# 获取单独进行减值测试的应收款项减值准备转回 -> getStmNoteEoItems29


# 获取对外委托贷款取得的收益时间序列 -> getStmNoteEoItems30Series


# 获取对外委托贷款取得的收益 -> getStmNoteEoItems30


# 获取公允价值法计量的投资性房地产价值变动损益时间序列 -> getStmNoteEoItems31Series


# 获取公允价值法计量的投资性房地产价值变动损益 -> getStmNoteEoItems31


# 获取法规要求一次性损益调整影响时间序列 -> getStmNoteEoItems32Series


# 获取法规要求一次性损益调整影响 -> getStmNoteEoItems32


# 获取受托经营取得的托管费收入时间序列 -> getStmNoteEoItems33Series


# 获取受托经营取得的托管费收入 -> getStmNoteEoItems33


# 获取其他营业外收支净额时间序列 -> getStmNoteEoItems19Series


# 获取其他营业外收支净额 -> getStmNoteEoItems19


# 获取中国证监会认定的其他项目时间序列 -> getStmNoteEoItems20Series


# 获取中国证监会认定的其他项目 -> getStmNoteEoItems20


# 获取坏账损失时间序列 -> getStmNoteImpairmentLoss4Series


# 获取坏账损失 -> getStmNoteImpairmentLoss4


# 获取存货跌价损失时间序列 -> getStmNoteImpairmentLoss5Series


# 获取存货跌价损失 -> getStmNoteImpairmentLoss5


# 获取发放贷款和垫款减值损失时间序列 -> getStmNoteImpairmentLoss7Series


# 获取发放贷款和垫款减值损失 -> getStmNoteImpairmentLoss7


# 获取持有至到期投资减值损失时间序列 -> getStmNoteImpairmentLoss9Series


# 获取持有至到期投资减值损失 -> getStmNoteImpairmentLoss9


# 获取本期费用化研发支出时间序列 -> getStmNoteRdExpCostSeries


# 获取本期费用化研发支出 -> getStmNoteRdExpCost


# 获取本期资本化研发支出时间序列 -> getStmNoteRdExpCapitalSeries


# 获取本期资本化研发支出 -> getStmNoteRdExpCapital


# 获取研发支出合计时间序列 -> getStmNoteRdExpSeries


# 获取研发支出合计 -> getStmNoteRdExp


# 获取研发人员数量时间序列 -> getStmNoteRdEmployeeSeries


# 获取研发人员数量 -> getStmNoteRdEmployee


# 获取研发人员数量占比时间序列 -> getStmNoteRdEmployeePctSeries


# 获取研发人员数量占比 -> getStmNoteRdEmployeePct


# 获取转融通融入资金时间序列 -> getStmNoteLoans1Series


# 获取转融通融入资金 -> getStmNoteLoans1


# 获取大客户名称时间序列 -> getStmNoteCustomerTop5Series


# 获取大客户名称 -> getStmNoteCustomerTop5


# 获取大客户销售收入时间序列 -> getStmNoteSalesTop5Series


# 获取大客户销售收入 -> getStmNoteSalesTop5


# 获取大客户销售收入占比时间序列 -> getStmNoteSalesPctTop5Series


# 获取大客户销售收入占比 -> getStmNoteSalesPctTop5


# 获取前五大客户销售收入占比时间序列 -> getStmNoteSalesTop5PctSeries


# 获取前五大客户销售收入占比 -> getStmNoteSalesTop5Pct


# 获取大供应商名称时间序列 -> getStmNoteSupplierTop5Series


# 获取大供应商名称 -> getStmNoteSupplierTop5


# 获取大供应商采购金额时间序列 -> getStmNotePurchaseTop5Series


# 获取大供应商采购金额 -> getStmNotePurchaseTop5


# 获取大供应商采购金额占比时间序列 -> getStmNotePurchasePctTop5Series


# 获取大供应商采购金额占比 -> getStmNotePurchasePctTop5


# 获取前五大供应商采购金额占比时间序列 -> getStmNotePurchaseTop5PctSeries


# 获取前五大供应商采购金额占比 -> getStmNotePurchaseTop5Pct


# 获取工资、奖金、津贴和补贴:本期增加时间序列 -> getStmNoteBenAddSeries


# 获取工资、奖金、津贴和补贴:本期增加 -> getStmNoteBenAdd


# 获取工资、奖金、津贴和补贴:期初余额时间序列 -> getStmNoteBenSbSeries


# 获取工资、奖金、津贴和补贴:期初余额 -> getStmNoteBenSb


# 获取工资、奖金、津贴和补贴:期末余额时间序列 -> getStmNoteBenEbSeries


# 获取工资、奖金、津贴和补贴:期末余额 -> getStmNoteBenEb


# 获取工资、奖金、津贴和补贴:本期减少时间序列 -> getStmNoteBenDeSeries


# 获取工资、奖金、津贴和补贴:本期减少 -> getStmNoteBenDe


# 获取工会经费和职工教育经费:本期增加时间序列 -> getStmNoteEduAndUnionFundsAddSeries


# 获取工会经费和职工教育经费:本期增加 -> getStmNoteEduAndUnionFundsAdd


# 获取工会经费和职工教育经费:期初余额时间序列 -> getStmNoteEduAndUnionFundsSbSeries


# 获取工会经费和职工教育经费:期初余额 -> getStmNoteEduAndUnionFundsSb


# 获取工会经费和职工教育经费:期末余额时间序列 -> getStmNoteEduAndUnionFundsEbSeries


# 获取工会经费和职工教育经费:期末余额 -> getStmNoteEduAndUnionFundsEb


# 获取工会经费和职工教育经费:本期减少时间序列 -> getStmNoteEduAndUnionFundsDeSeries


# 获取工会经费和职工教育经费:本期减少 -> getStmNoteEduAndUnionFundsDe


# 获取职工福利费:本期增加时间序列 -> getStmNoteWelfareAddSeries


# 获取职工福利费:本期增加 -> getStmNoteWelfareAdd


# 获取职工福利费:期初余额时间序列 -> getStmNoteWelfareSbSeries


# 获取职工福利费:期初余额 -> getStmNoteWelfareSb


# 获取职工福利费:期末余额时间序列 -> getStmNoteWelfareEbSeries


# 获取职工福利费:期末余额 -> getStmNoteWelfareEb


# 获取职工福利费:本期减少时间序列 -> getStmNoteWelfareDeSeries


# 获取职工福利费:本期减少 -> getStmNoteWelfareDe


# 获取住房公积金:本期增加时间序列 -> getStmNoteHousingFundAddSeries


# 获取住房公积金:本期增加 -> getStmNoteHousingFundAdd


# 获取住房公积金:期初余额时间序列 -> getStmNoteHousingFundSbSeries


# 获取住房公积金:期初余额 -> getStmNoteHousingFundSb


# 获取住房公积金:期末余额时间序列 -> getStmNoteHousingFundEbSeries


# 获取住房公积金:期末余额 -> getStmNoteHousingFundEb


# 获取住房公积金:本期减少时间序列 -> getStmNoteHousingFundDeSeries


# 获取住房公积金:本期减少 -> getStmNoteHousingFundDe


# 获取基本养老保险:本期增加时间序列 -> getStmNoteBasicPenAddSeries


# 获取基本养老保险:本期增加 -> getStmNoteBasicPenAdd


# 获取基本养老保险:期初余额时间序列 -> getStmNoteBasicPenSbSeries


# 获取基本养老保险:期初余额 -> getStmNoteBasicPenSb


# 获取基本养老保险:期末余额时间序列 -> getStmNoteBasicPenEbSeries


# 获取基本养老保险:期末余额 -> getStmNoteBasicPenEb


# 获取基本养老保险:本期减少时间序列 -> getStmNoteBasicPenDeSeries


# 获取基本养老保险:本期减少 -> getStmNoteBasicPenDe


# 获取生育保险费:本期增加时间序列 -> getStmNoteMaternityInSAddSeries


# 获取生育保险费:本期增加 -> getStmNoteMaternityInSAdd


# 获取生育保险费:期初余额时间序列 -> getStmNoteMaternityInSSbSeries


# 获取生育保险费:期初余额 -> getStmNoteMaternityInSSb


# 获取生育保险费:期末余额时间序列 -> getStmNoteMaternityInSEbSeries


# 获取生育保险费:期末余额 -> getStmNoteMaternityInSEb


# 获取生育保险费:本期减少时间序列 -> getStmNoteMaternityInSDeSeries


# 获取生育保险费:本期减少 -> getStmNoteMaternityInSDe


# 获取失业保险费:本期增加时间序列 -> getStmNoteUneMplInSAddSeries


# 获取失业保险费:本期增加 -> getStmNoteUneMplInSAdd


# 获取失业保险费:期初余额时间序列 -> getStmNoteUneMplInSSbSeries


# 获取失业保险费:期初余额 -> getStmNoteUneMplInSSb


# 获取失业保险费:期末余额时间序列 -> getStmNoteUneMplInSEbSeries


# 获取失业保险费:期末余额 -> getStmNoteUneMplInSEb


# 获取失业保险费:本期减少时间序列 -> getStmNoteUneMplInSDeSeries


# 获取失业保险费:本期减少 -> getStmNoteUneMplInSDe


# 获取医疗保险费:本期增加时间序列 -> getStmNoteMedInSAddSeries


# 获取医疗保险费:本期增加 -> getStmNoteMedInSAdd


# 获取医疗保险费:期初余额时间序列 -> getStmNoteMedInSSbSeries


# 获取医疗保险费:期初余额 -> getStmNoteMedInSSb


# 获取医疗保险费:期末余额时间序列 -> getStmNoteMedInSEbSeries


# 获取医疗保险费:期末余额 -> getStmNoteMedInSEb


# 获取医疗保险费:本期减少时间序列 -> getStmNoteMedInSDeSeries


# 获取医疗保险费:本期减少 -> getStmNoteMedInSDe


# 获取工伤保险费:本期增加时间序列 -> getStmNoteEMplInjuryInSAddSeries


# 获取工伤保险费:本期增加 -> getStmNoteEMplInjuryInSAdd


# 获取工伤保险费:期初余额时间序列 -> getStmNoteEMplInjuryInSSbSeries


# 获取工伤保险费:期初余额 -> getStmNoteEMplInjuryInSSb


# 获取工伤保险费:期末余额时间序列 -> getStmNoteEMplInjuryInSEbSeries


# 获取工伤保险费:期末余额 -> getStmNoteEMplInjuryInSEb


# 获取工伤保险费:本期减少时间序列 -> getStmNoteEMplInjuryInSDeSeries


# 获取工伤保险费:本期减少 -> getStmNoteEMplInjuryInSDe


# 获取消费税时间序列 -> getStmNoteTaxConsumptionSeries


# 获取消费税 -> getStmNoteTaxConsumption


# 获取城建税时间序列 -> getStmNoteTaxConstructionSeries


# 获取城建税 -> getStmNoteTaxConstruction


# 获取教育费附加时间序列 -> getStmNoteTaxEdeSupplementTarYSeries


# 获取教育费附加 -> getStmNoteTaxEdeSupplementTarY


# 获取土地使用税时间序列 -> getStmNoteTaxUrbanLandUseSeries


# 获取土地使用税 -> getStmNoteTaxUrbanLandUse


# 获取房产税时间序列 -> getStmNoteTaxBuildingSeries


# 获取房产税 -> getStmNoteTaxBuilding


# 获取印花税时间序列 -> getStmNoteTaxStampSeries


# 获取印花税 -> getStmNoteTaxStamp


# 获取单季度.基金利润时间序列 -> getQAnalIncomeSeries


# 获取单季度.基金利润 -> getQAnalIncome


# 获取单季度.基金利润(合计)时间序列 -> getQAnalTotalIncomeSeries


# 获取单季度.基金利润(合计) -> getQAnalTotalIncome


# 获取单季度.报告期利润扣减当期公允价值变动损益后的净额时间序列 -> getQAnalDeCuteDNetIncomeSeries


# 获取单季度.报告期利润扣减当期公允价值变动损益后的净额 -> getQAnalDeCuteDNetIncome


# 获取单季度.超额收益率时间序列 -> getQAnalBenchDevReturnSeries


# 获取单季度.超额收益率 -> getQAnalBenchDevReturn


# 获取单季度.超额收益率标准差时间序列 -> getQAnalStdBenchDevReturnSeries


# 获取单季度.超额收益率标准差 -> getQAnalStdBenchDevReturn


# 获取报告期利润时间序列 -> getAnalIncomeSeries


# 获取报告期利润 -> getAnalIncome


# 获取报告期利润扣减当期公允价值变动损益后的净额时间序列 -> getAnalNetIncomeSeries


# 获取报告期利润扣减当期公允价值变动损益后的净额 -> getAnalNetIncome


# 获取报告期加权平均份额利润时间序列 -> getAnalAvgNetIncomePerUnitSeries


# 获取报告期加权平均份额利润 -> getAnalAvgNetIncomePerUnit


# 获取报告期末可供分配基金利润时间序列 -> getAnalDIsTriButAbleSeries


# 获取报告期末可供分配基金利润 -> getAnalDIsTriButAble


# 获取基金加权平均净值利润率时间序列 -> getAnalAvgNavReturnSeries


# 获取基金加权平均净值利润率 -> getAnalAvgNavReturn


# 获取基金申购款时间序列 -> getStmNavChange7Series


# 获取基金申购款 -> getStmNavChange7


# 获取基金申购款(实收基金)时间序列 -> getStmNavChange7PaidInCapitalSeries


# 获取基金申购款(实收基金) -> getStmNavChange7PaidInCapital


# 获取基金赎回款时间序列 -> getStmNavChange8Series


# 获取基金赎回款 -> getStmNavChange8


# 获取基金赎回款(实收基金)时间序列 -> getStmNavChange8PaidInCapitalSeries


# 获取基金赎回款(实收基金) -> getStmNavChange8PaidInCapital


# 获取信息披露费时间序列 -> getStmIs18Series


# 获取信息披露费 -> getStmIs18


# 获取首发信息披露费时间序列 -> getIpoIDcSeries


# 获取首发信息披露费 -> getIpoIDc


# 获取应收黄金合约拆借孳息时间序列 -> getStmBsGoldContractInterestSeries


# 获取应收黄金合约拆借孳息 -> getStmBsGoldContractInterest


# 获取交易佣金(合计值)时间序列 -> getCommissionTotalSeries


# 获取交易佣金(合计值) -> getCommissionTotal


# 获取交易佣金(分券商明细)时间序列 -> getCommissionDetailedSeries


# 获取交易佣金(分券商明细) -> getCommissionDetailed


# 获取应收票据及应收账款时间序列 -> getStm07BsReItsNotesSeries


# 获取应收票据及应收账款 -> getStm07BsReItsNotes


# 获取其他应收款(合计)时间序列 -> getStm07BsReItsOthersSeries


# 获取其他应收款(合计) -> getStm07BsReItsOthers


# 获取投资性房地产租金收入时间序列 -> getStmNoteInvestmentIncome0003Series


# 获取投资性房地产租金收入 -> getStmNoteInvestmentIncome0003


# 获取投资性房地产时间序列 -> getStm07BsReItsRealEstateSeries


# 获取投资性房地产 -> getStm07BsReItsRealEstate


# 获取应付票据及应付账款时间序列 -> getStm07BsReItsPayableSeries


# 获取应付票据及应付账款 -> getStm07BsReItsPayable


# 获取预收款项_GSD时间序列 -> getWgsDPaymentUnearnedSeries


# 获取预收款项_GSD -> getWgsDPaymentUnearned


# 获取预收款项时间序列 -> getStm07BsReItsRecIPtsSeries


# 获取预收款项 -> getStm07BsReItsRecIPts


# 获取应交税费时间序列 -> getStm07BsReItsTaxSeries


# 获取应交税费 -> getStm07BsReItsTax


# 获取其他应付款(合计)时间序列 -> getStm07BsReItsOtherPayableSeries


# 获取其他应付款(合计) -> getStm07BsReItsOtherPayable


# 获取实收资本(或股本)时间序列 -> getStm07BsReItsPaidInSeries


# 获取实收资本(或股本) -> getStm07BsReItsPaidIn


# 获取资本公积金时间序列 -> getStm07BsReItsCapitalReserveSeries


# 获取资本公积金 -> getStm07BsReItsCapitalReserve


# 获取盈余公积金时间序列 -> getStm07BsReItsSurplusSeries


# 获取盈余公积金 -> getStm07BsReItsSurplus


# 获取未分配利润时间序列 -> getStm07BsReItsUndIsTriRProfitSeries


# 获取未分配利润 -> getStm07BsReItsUndIsTriRProfit


# 获取未分配利润_FUND时间序列 -> getStmBs75Series


# 获取未分配利润_FUND -> getStmBs75


# 获取经营活动现金流入小计时间序列 -> getStm07CsReItsOperCashInSeries


# 获取经营活动现金流入小计 -> getStm07CsReItsOperCashIn


# 获取单季度.经营活动现金流入小计时间序列 -> getQfaSToTCashInFlowsOperActSeries


# 获取单季度.经营活动现金流入小计 -> getQfaSToTCashInFlowsOperAct


# 获取经营活动现金流出小计时间序列 -> getStm07CsReItsOperCashOutSeries


# 获取经营活动现金流出小计 -> getStm07CsReItsOperCashOut


# 获取单季度.经营活动现金流出小计时间序列 -> getQfaSToTCashOutFlowsOperActSeries


# 获取单季度.经营活动现金流出小计 -> getQfaSToTCashOutFlowsOperAct


# 获取销售商品、提供劳务收到的现金时间序列 -> getStm07CsReItsSalesCashSeries


# 获取销售商品、提供劳务收到的现金 -> getStm07CsReItsSalesCash


# 获取单季度.销售商品、提供劳务收到的现金时间序列 -> getQfaCashRecpSgAndRsSeries


# 获取单季度.销售商品、提供劳务收到的现金 -> getQfaCashRecpSgAndRs


# 获取购买商品、接受劳务支付的现金时间序列 -> getStm07CsReItsBuyCashSeries


# 获取购买商品、接受劳务支付的现金 -> getStm07CsReItsBuyCash


# 获取单季度.购买商品、接受劳务支付的现金时间序列 -> getQfaCashPayGoodsPUrchSerVRecSeries


# 获取单季度.购买商品、接受劳务支付的现金 -> getQfaCashPayGoodsPUrchSerVRec


# 获取支付的各项税费时间序列 -> getStm07CsReItsTaxSeries


# 获取支付的各项税费 -> getStm07CsReItsTax


# 获取单季度.支付的各项税费时间序列 -> getQfaPayAllTyPTaxSeries


# 获取单季度.支付的各项税费 -> getQfaPayAllTyPTax


# 获取支付其他与经营活动有关的现金时间序列 -> getStm07CsReItsPaidCashSeries


# 获取支付其他与经营活动有关的现金 -> getStm07CsReItsPaidCash


# 获取单季度.支付其他与经营活动有关的现金时间序列 -> getQfaOtherCashPayRalOperActSeries


# 获取单季度.支付其他与经营活动有关的现金 -> getQfaOtherCashPayRalOperAct


# 获取投资活动现金流入小计时间序列 -> getStm07CsReItsInvestCashInSeries


# 获取投资活动现金流入小计 -> getStm07CsReItsInvestCashIn


# 获取单季度.投资活动现金流入小计时间序列 -> getQfaSToTCashInFlowsInvActSeries


# 获取单季度.投资活动现金流入小计 -> getQfaSToTCashInFlowsInvAct


# 获取投资活动现金流出小计时间序列 -> getStm07CsReItsInvestCashOutSeries


# 获取投资活动现金流出小计 -> getStm07CsReItsInvestCashOut


# 获取单季度.投资活动现金流出小计时间序列 -> getQfaSToTCashOutFlowsInvActSeries


# 获取单季度.投资活动现金流出小计 -> getQfaSToTCashOutFlowsInvAct


# 获取筹资活动现金流入小计时间序列 -> getStm07CsReItsFinanceCashInSeries


# 获取筹资活动现金流入小计 -> getStm07CsReItsFinanceCashIn


# 获取单季度.筹资活动现金流入小计时间序列 -> getQfaSToTCashInFlowsFncActSeries


# 获取单季度.筹资活动现金流入小计 -> getQfaSToTCashInFlowsFncAct


# 获取筹资活动现金流出小计时间序列 -> getStm07CsReItsFinanceCashOutSeries


# 获取筹资活动现金流出小计 -> getStm07CsReItsFinanceCashOut


# 获取单季度.筹资活动现金流出小计时间序列 -> getQfaSToTCashOutFlowsFncActSeries


# 获取单季度.筹资活动现金流出小计 -> getQfaSToTCashOutFlowsFncAct


# 获取季度报告披露日期时间序列 -> getFundStmIssuingDateQTySeries


# 获取季度报告披露日期 -> getFundStmIssuingDateQTy


# 获取中(年)报披露日期时间序列 -> getFundStmIssuingDateSeries


# 获取中(年)报披露日期 -> getFundStmIssuingDate


# 获取每股股利(税前)(已宣告)时间序列 -> getDivCashBeforeTax2Series


# 获取每股股利(税前)(已宣告) -> getDivCashBeforeTax2


# 获取每股股利(税后)(已宣告)时间序列 -> getDivCashAfterTax2Series


# 获取每股股利(税后)(已宣告) -> getDivCashAfterTax2


# 获取每股红股(已宣告)时间序列 -> getDivStock2Series


# 获取每股红股(已宣告) -> getDivStock2


# 获取每股红股时间序列 -> getDivStockSeries


# 获取每股红股 -> getDivStock


# 获取每股股利(税后)时间序列 -> getDivCashAfterTaxSeries


# 获取每股股利(税后) -> getDivCashAfterTax


# 获取区间每股股利(税后)时间序列 -> getDivCashPaidAfterTaxSeries


# 获取区间每股股利(税后) -> getDivCashPaidAfterTax


# 获取每股股利(税前)时间序列 -> getDivCashBeforeTaxSeries


# 获取每股股利(税前) -> getDivCashBeforeTax


# 获取区间每股股利(税前)时间序列 -> getDivCashPaidBeforeTaxSeries


# 获取区间每股股利(税前) -> getDivCashPaidBeforeTax


# 获取每股分红送转时间序列 -> getDivCashAndStockSeries


# 获取每股分红送转 -> getDivCashAndStock


# 获取分红方案进度时间序列 -> getDivProgressSeries


# 获取分红方案进度 -> getDivProgress


# 获取分红对象时间序列 -> getDivObjectSeries


# 获取分红对象 -> getDivObject


# 获取是否分红时间序列 -> getDivIfDivSeries


# 获取是否分红 -> getDivIfDiv


# 获取分红基准股本时间序列 -> getDivSharesSeries


# 获取分红基准股本 -> getDivShares


# 获取现金分红总额时间序列 -> getStmNoteAuALaCcmDivSeries


# 获取现金分红总额 -> getStmNoteAuALaCcmDiv


# 获取年度现金分红总额时间序列 -> getDivAuAlCashDividendSeries


# 获取年度现金分红总额 -> getDivAuAlCashDividend


# 获取区间现金分红总额时间序列 -> getDivAuALaCcmDiv2Series


# 获取区间现金分红总额 -> getDivAuALaCcmDiv2


# 获取股权登记日时间序列 -> getDivRecordDateSeries


# 获取股权登记日 -> getDivRecordDate


# 获取B股股权登记日时间序列 -> getRightsIssueRecDateShareBSeries


# 获取B股股权登记日 -> getRightsIssueRecDateShareB


# 获取老股东配售股权登记日时间序列 -> getCbListRationChKindAteSeries


# 获取老股东配售股权登记日 -> getCbListRationChKindAte


# 获取向老股东配售股权登记日时间序列 -> getFellowRecordDateSeries


# 获取向老股东配售股权登记日 -> getFellowRecordDate


# 获取除权除息日时间序列 -> getDivExDateSeries


# 获取除权除息日 -> getDivExDate


# 获取派息日时间序列 -> getDivPayDateSeries


# 获取派息日 -> getDivPayDate


# 获取红股上市交易日时间序列 -> getDivTrDDateShareBSeries


# 获取红股上市交易日 -> getDivTrDDateShareB


# 获取预披露公告日时间序列 -> getDivPreDisclosureDateSeries


# 获取预披露公告日 -> getDivPreDisclosureDate


# 获取预案公告日时间序列 -> getRightsIssuePrePlanDateSeries


# 获取预案公告日 -> getRightsIssuePrePlanDate


# 获取董事会预案公告日时间序列 -> getRefRMkdPrePlanDateSeries


# 获取董事会预案公告日 -> getRefRMkdPrePlanDate


# 获取股东大会公告日时间序列 -> getCbWarAnnoDateMeetingSeries


# 获取股东大会公告日 -> getCbWarAnnoDateMeeting


# 获取分红实施公告日时间序列 -> getDivImpDateSeries


# 获取分红实施公告日 -> getDivImpDate


# 获取三年累计分红占比(再融资条件)时间序列 -> getDivDivPct3YearAccUSeries


# 获取三年累计分红占比(再融资条件) -> getDivDivPct3YearAccU


# 获取上市以来分红率时间序列 -> getDivDivPctAccUSeries


# 获取上市以来分红率 -> getDivDivPctAccU


# 获取年度现金分红比例时间序列 -> getDivPayOutRatio2Series


# 获取年度现金分红比例 -> getDivPayOutRatio2


# 获取年度现金分红次数时间序列 -> getDivFrEqSeries


# 获取年度现金分红次数 -> getDivFrEq


# 获取年度累计单位分红时间序列 -> getDivAuALaCcmDivPerShareSeries


# 获取年度累计单位分红 -> getDivAuALaCcmDivPerShare


# 获取现金分红比例时间序列 -> getDivDividendRatioSeries


# 获取现金分红比例 -> getDivDividendRatio


# 获取首发价格时间序列 -> getIpoPrice2Series


# 获取首发价格 -> getIpoPrice2


# 获取发行数量合计时间序列 -> getIpoAmountSeries


# 获取发行数量合计 -> getIpoAmount


# 获取新股发行数量时间序列 -> getIpoNewSharesSeries


# 获取新股发行数量 -> getIpoNewShares


# 获取股东售股数量时间序列 -> getIpoOldSharesSeries


# 获取股东售股数量 -> getIpoOldShares


# 获取老股转让比例时间序列 -> getIpoOldSharesRatioSeries


# 获取老股转让比例 -> getIpoOldSharesRatio


# 获取募集资金总额(含股东售股)时间序列 -> getIpoCollectionTotalSeries


# 获取募集资金总额(含股东售股) -> getIpoCollectionTotal


# 获取首发募集资金时间序列 -> getIpoCollectionSeries


# 获取首发募集资金 -> getIpoCollection


# 获取首发募集资金净额时间序列 -> getIpoNetCollectionTureSeries


# 获取首发募集资金净额 -> getIpoNetCollectionTure


# 获取股东售股金额时间序列 -> getIpoCollectionOldShares2Series


# 获取股东售股金额 -> getIpoCollectionOldShares2


# 获取首发预计募集资金时间序列 -> getIpoExpectedCollection2Series


# 获取首发预计募集资金 -> getIpoExpectedCollection2


# 获取网上发行数量(回拨前)时间序列 -> getIpoPoCOnlineSeries


# 获取网上发行数量(回拨前) -> getIpoPoCOnline


# 获取网下发行数量(回拨前)时间序列 -> getIpoPoCOfflineSeries


# 获取网下发行数量(回拨前) -> getIpoPoCOffline


# 获取网上发行数量时间序列 -> getIssueIssueOlSeries


# 获取网上发行数量 -> getIssueIssueOl


# 获取网上发行数量(不含优先配售)时间序列 -> getCbListIssueVolOnLSeries


# 获取网上发行数量(不含优先配售) -> getCbListIssueVolOnL


# 获取网下发行数量时间序列 -> getFellowOtcAmtSeries


# 获取网下发行数量 -> getFellowOtcAmt


# 获取网上发行有效申购数量时间序列 -> getIpoVsSharesSSeries


# 获取网上发行有效申购数量 -> getIpoVsSharesS


# 获取网上发行有效认购倍数时间序列 -> getIpoSubRatioSeries


# 获取网上发行有效认购倍数 -> getIpoSubRatio


# 获取国际发行有效申购数量时间序列 -> getIpoIntvsSharesSeries


# 获取国际发行有效申购数量 -> getIpoIntvsShares


# 获取国际发行有效申购倍数时间序列 -> getIpoIntSubRatioSeries


# 获取国际发行有效申购倍数 -> getIpoIntSubRatio


# 获取申报预披露日时间序列 -> getIpoWpIpReleasingDateSeries


# 获取申报预披露日 -> getIpoWpIpReleasingDate


# 获取招股公告日时间序列 -> getIpoPubOfFrDateSeries


# 获取招股公告日 -> getIpoPubOfFrDate


# 获取首发主承销商时间序列 -> getIpoLeadUndRSeries


# 获取首发主承销商 -> getIpoLeadUndR


# 获取首发保荐机构时间序列 -> getIpoSponsorSeries


# 获取首发保荐机构 -> getIpoSponsor


# 获取首发保荐机构(上市推荐人)时间序列 -> getIpoNominatorSeries


# 获取首发保荐机构(上市推荐人) -> getIpoNominator


# 获取首发副主承销商时间序列 -> getIpoDeputyUndRSeries


# 获取首发副主承销商 -> getIpoDeputyUndR


# 获取首发保荐人律师时间序列 -> getIpoLegalAdvisorSeries


# 获取首发保荐人律师 -> getIpoLegalAdvisor


# 获取首发承销保荐费用时间序列 -> getIpoUsFees2Series


# 获取首发承销保荐费用 -> getIpoUsFees2


# 获取新股配售经纪佣金费率时间序列 -> getIpoCommissionRateSeries


# 获取新股配售经纪佣金费率 -> getIpoCommissionRate


# 获取首发审计费用时间序列 -> getIpoAuditFeeSeries


# 获取首发审计费用 -> getIpoAuditFee


# 获取首发法律费用时间序列 -> getIpoLawFeeSeries


# 获取首发法律费用 -> getIpoLawFee


# 获取是否行使超额配售权时间序列 -> getIpoGreenShoeSeries


# 获取是否行使超额配售权 -> getIpoGreenShoe


# 获取是否触发回拨机制时间序列 -> getIpoBackMechanismSeries


# 获取是否触发回拨机制 -> getIpoBackMechanism


# 获取计划发行总数时间序列 -> getIpoIsSuVolPlannedSeries


# 获取计划发行总数 -> getIpoIsSuVolPlanned


# 获取申购一手中签率时间序列 -> getIpoDTooRatioPlSeries


# 获取申购一手中签率 -> getIpoDTooRatioPl


# 获取稳购1手最低申购股数时间序列 -> getIpoMinSubscriptionPlSeries


# 获取稳购1手最低申购股数 -> getIpoMinSubscriptionPl


# 获取超额配售数量时间序列 -> getIpoOverAllotVolSeries


# 获取超额配售数量 -> getIpoOverAllotVol


# 获取公开发售甲组申购人数时间序列 -> getIpoSubNumASeries


# 获取公开发售甲组申购人数 -> getIpoSubNumA


# 获取公开发售乙组申购人数时间序列 -> getIpoSubNumBSeries


# 获取公开发售乙组申购人数 -> getIpoSubNumB


# 获取公开发售申购人数时间序列 -> getIpoSubNumSeries


# 获取公开发售申购人数 -> getIpoSubNum


# 获取首日上市数量时间序列 -> getIpoLStNumSeries


# 获取首日上市数量 -> getIpoLStNum


# 获取上市天数时间序列 -> getIpoListDaysSeries


# 获取上市天数 -> getIpoListDays


# 获取上市交易天数时间序列 -> getIpoTradeDaysSeries


# 获取上市交易天数 -> getIpoTradeDays


# 获取新股未开板涨停板天数时间序列 -> getIpoLimitUpDaysSeries


# 获取新股未开板涨停板天数 -> getIpoLimitUpDays


# 获取开板日时间序列 -> getIpoLimitUpOpenDateSeries


# 获取开板日 -> getIpoLimitUpOpenDate


# 获取网上发行中签率时间序列 -> getIpoCashRatioSeries


# 获取网上发行中签率 -> getIpoCashRatio


# 获取网上申购数量上限时间序列 -> getIpoSSharesUpLimitSeries


# 获取网上申购数量上限 -> getIpoSSharesUpLimit


# 获取网上申购资金上限时间序列 -> getIpoSAmtUpLimitSeries


# 获取网上申购资金上限 -> getIpoSAmtUpLimit


# 获取网上发行有效申购户数时间序列 -> getIpoCashEffAccSeries


# 获取网上发行有效申购户数 -> getIpoCashEffAcc


# 获取网上超额认购倍数时间序列 -> getIpoOvRSubRatioSeries


# 获取网上超额认购倍数 -> getIpoOvRSubRatio


# 获取网上冻结资金时间序列 -> getIpoBFundSeries


# 获取网上冻结资金 -> getIpoBFund


# 获取网上申购代码时间序列 -> getIpoPurchaseCodeSeries


# 获取网上申购代码 -> getIpoPurchaseCode


# 获取网上放弃认购数量时间序列 -> getIpoGiveUpSeries


# 获取网上放弃认购数量 -> getIpoGiveUp


# 获取网下申购配售比例时间序列 -> getIpoOtcCashPctSeries


# 获取网下申购配售比例 -> getIpoOtcCashPct


# 获取网下申购总量时间序列 -> getIpoOpVolumeSeries


# 获取网下申购总量 -> getIpoOpVolume


# 获取网下冻结资金时间序列 -> getIpoOpAmountSeries


# 获取网下冻结资金 -> getIpoOpAmount


# 获取网下有效报价下限时间序列 -> getIpoVsPriceMinSeries


# 获取网下有效报价下限 -> getIpoVsPriceMin


# 获取网下有效报价上限时间序列 -> getIpoVsPriceMaxSeries


# 获取网下有效报价上限 -> getIpoVsPriceMax


# 获取网下有效报价申购量时间序列 -> getIpoVsSharesSeries


# 获取网下有效报价申购量 -> getIpoVsShares


# 获取网下超额认购倍数时间序列 -> getFellowAmtToJurSeries


# 获取网下超额认购倍数 -> getFellowAmtToJur


# 获取网下超额认购倍数(回拨前)时间序列 -> getIpoVsRatioSeries


# 获取网下超额认购倍数(回拨前) -> getIpoVsRatio


# 获取网下高于有效报价上限的申购量时间序列 -> getIpoInvsSharesASeries


# 获取网下高于有效报价上限的申购量 -> getIpoInvsSharesA


# 获取网下申购数量上限时间序列 -> getIpoOpUpLimitSeries


# 获取网下申购数量上限 -> getIpoOpUpLimit


# 获取网下申购数量下限时间序列 -> getIpoOpDownLimitSeries


# 获取网下申购数量下限 -> getIpoOpDownLimit


# 获取网下申购步长时间序列 -> getListStepSizeSubsCrOfFlSeries


# 获取网下申购步长 -> getListStepSizeSubsCrOfFl


# 获取网下申购报价数量时间序列 -> getIpoOpNumOffRingSeries


# 获取网下申购报价数量 -> getIpoOpNumOffRing


# 获取网下申购配售对象家数时间序列 -> getIpoOpNumOfPmtSeries


# 获取网下申购配售对象家数 -> getIpoOpNumOfPmt


# 获取网下申购询价对象家数时间序列 -> getIpoOpNumOfInQSeries


# 获取网下申购询价对象家数 -> getIpoOpNumOfInQ


# 获取网下询价机构获配数量时间序列 -> getIpoLotWinningNumberSeries


# 获取网下询价机构获配数量 -> getIpoLotWinningNumber


# 获取网下投资者获配数量时间序列 -> getIpoPSharesAbcSeries


# 获取网下投资者获配数量 -> getIpoPSharesAbc


# 获取网下投资者申购数量时间序列 -> getIpoOpVolumeAbcSeries


# 获取网下投资者申购数量 -> getIpoOpVolumeAbc


# 获取网下投资者获配家数时间序列 -> getIpoNInstitutionalAbcSeries


# 获取网下投资者获配家数 -> getIpoNInstitutionalAbc


# 获取网下投资者中签率时间序列 -> getIpoLotteryRateAbcSeries


# 获取网下投资者中签率 -> getIpoLotteryRateAbc


# 获取网下投资者配售数量占比时间序列 -> getIpoPSharesPctAbcSeries


# 获取网下投资者配售数量占比 -> getIpoPSharesPctAbc


# 获取网下投资者有效申购数量占比时间序列 -> getIpoVsSharesPctAbcSeries


# 获取网下投资者有效申购数量占比 -> getIpoVsSharesPctAbc


# 获取网下公募基金获配数量时间序列 -> getIpoPSharesMfSeries


# 获取网下公募基金获配数量 -> getIpoPSharesMf


# 获取网下社保基金获配数量时间序列 -> getIpoPSharesSSfSeries


# 获取网下社保基金获配数量 -> getIpoPSharesSSf


# 获取网下企业年金获配数量时间序列 -> getIpoPSharesSpSeries


# 获取网下企业年金获配数量 -> getIpoPSharesSp


# 获取网下保险资金获配数量时间序列 -> getIpoPSharesIfSeries


# 获取网下保险资金获配数量 -> getIpoPSharesIf


# 获取战略配售获配股份数时间序列 -> getIpoSiAllotmentSeries


# 获取战略配售获配股份数 -> getIpoSiAllotment


# 获取战略配售获配股份占比时间序列 -> getIpoSiAllotmentRatioSeries


# 获取战略配售获配股份占比 -> getIpoSiAllotmentRatio


# 获取主承销商战略获配股份数时间序列 -> getIpoUnderwriterAllotmentSeries


# 获取主承销商战略获配股份数 -> getIpoUnderwriterAllotment


# 获取主承销商战略获配股份占比时间序列 -> getIpoUnderwriterAllotmentRatioSeries


# 获取主承销商战略获配股份占比 -> getIpoUnderwriterAllotmentRatio


# 获取网下配售对象名称时间序列 -> getIpoAllotmentSubjectsSeries


# 获取网下配售对象名称 -> getIpoAllotmentSubjects


# 获取网下投资者分类限售配售方式时间序列 -> getIpoAllOtwaySeries


# 获取网下投资者分类限售配售方式 -> getIpoAllOtway


# 获取网下投资者分类配售限售比例时间序列 -> getIpoPShareRestrictPctSeries


# 获取网下投资者分类配售限售比例 -> getIpoPShareRestrictPct


# 获取网下申报价格加权平均数时间序列 -> getIpoWGtAvgPriceSeries


# 获取网下申报价格加权平均数 -> getIpoWGtAvgPrice


# 获取网下申报价格中位数时间序列 -> getIpoMedianPriceSeries


# 获取网下申报价格中位数 -> getIpoMedianPrice


# 获取初步询价申报价格时间序列 -> getIpoSubscriptionPriceSeries


# 获取初步询价申报价格 -> getIpoSubscriptionPrice


# 获取初步询价申报数量时间序列 -> getIpoSubscriptionSharesSeries


# 获取初步询价申报数量 -> getIpoSubscriptionShares


# 获取初步询价配售对象家数时间序列 -> getIpoInquirySeries


# 获取初步询价配售对象家数 -> getIpoInquiry


# 获取初步询价询价对象家数时间序列 -> getIpoInquiryInStSeries


# 获取初步询价询价对象家数 -> getIpoInquiryInSt


# 获取初步询价下限时间序列 -> getIpoSPriceMinSeries


# 获取初步询价下限 -> getIpoSPriceMin


# 获取初步询价上限时间序列 -> getIpoSPriceMaxSeries


# 获取初步询价上限 -> getIpoSPriceMax


# 获取初步询价申购总量时间序列 -> getIpoSSharesTSeries


# 获取初步询价申购总量 -> getIpoSSharesT


# 获取初步询价申购倍数(回拨前)时间序列 -> getIpoSRatioSeries


# 获取初步询价申购倍数(回拨前) -> getIpoSRatio


# 获取询价市值计算参考日时间序列 -> getIpoInquiryMvCalDateSeries


# 获取询价市值计算参考日 -> getIpoInquiryMvCalDate


# 获取网下询价市值门槛时间序列 -> getIpoInquiryMvMinSeries


# 获取网下询价市值门槛 -> getIpoInquiryMvMin


# 获取网下询价市值门槛(A类)时间序列 -> getIpoInquiryMvMinASeries


# 获取网下询价市值门槛(A类) -> getIpoInquiryMvMinA


# 获取网下询价市值门槛(主题与战略)时间序列 -> getIpoInquiryMvMinThemEstrTSeries


# 获取网下询价市值门槛(主题与战略) -> getIpoInquiryMvMinThemEstrT


# 获取发行价格下限(底价)时间序列 -> getIpoPriceMinSeries


# 获取发行价格下限(底价) -> getIpoPriceMin


# 获取发行价格上限时间序列 -> getIpoPriceMaxSeries


# 获取发行价格上限 -> getIpoPriceMax


# 获取首发承销方式时间序列 -> getIpoUndRTypeSeries


# 获取首发承销方式 -> getIpoUndRType


# 获取首发分销商时间序列 -> getIpoDistOrSeries


# 获取首发分销商 -> getIpoDistOr


# 获取首发国际协调人时间序列 -> getIpoInterCordTorSeries


# 获取首发国际协调人 -> getIpoInterCordTor


# 获取首发保荐人代表时间序列 -> getIpoSponsorRepresentativeSeries


# 获取首发保荐人代表 -> getIpoSponsorRepresentative


# 获取首发签字会计师时间序列 -> getIpoAuditCpaSeries


# 获取首发签字会计师 -> getIpoAuditCpa


# 获取首发经办律所时间序列 -> getIpoLawFirmSeries


# 获取首发经办律所 -> getIpoLawFirm


# 获取网下投资者报备截止日时间序列 -> getIpoApplicationDeadlineSeries


# 获取网下投资者报备截止日 -> getIpoApplicationDeadline


# 获取网下投资者报备截止时间时间序列 -> getIpoApplicationDeadlineTimeSeries


# 获取网下投资者报备截止时间 -> getIpoApplicationDeadlineTime


# 获取上市公告日时间序列 -> getIssueLiStanceSeries


# 获取上市公告日 -> getIssueLiStance


# 获取初步询价公告日时间序列 -> getIpoInQAnnCeDateSeries


# 获取初步询价公告日 -> getIpoInQAnnCeDate


# 获取初步询价起始日时间序列 -> getIpoInQStartDateSeries


# 获取初步询价起始日 -> getIpoInQStartDate


# 获取初步询价截止日时间序列 -> getIpoInQEnddateSeries


# 获取初步询价截止日 -> getIpoInQEnddate


# 获取初步询价结果公告日时间序列 -> getIpoInQResultDateSeries


# 获取初步询价结果公告日 -> getIpoInQResultDate


# 获取初步配售结果公告日时间序列 -> getIpoPReplacingDateSeries


# 获取初步配售结果公告日 -> getIpoPReplacingDate


# 获取网下申购截止日期时间序列 -> getIpoOpEnddateSeries


# 获取网下申购截止日期 -> getIpoOpEnddate


# 获取网下定价日时间序列 -> getIpoPDateSeries


# 获取网下定价日 -> getIpoPDate


# 获取网下申购缴款日时间序列 -> getIpoOffSubPayDateSeries


# 获取网下申购缴款日 -> getIpoOffSubPayDate


# 获取网上市值申购登记日时间序列 -> getIpoMvRegDateSeries


# 获取网上市值申购登记日 -> getIpoMvRegDate


# 获取网上中签结果公告日时间序列 -> getIpoRefundDateSeries


# 获取网上中签结果公告日 -> getIpoRefundDate


# 获取网上申购缴款日时间序列 -> getIpoCapPayDateSeries


# 获取网上申购缴款日 -> getIpoCapPayDate


# 获取现场推介起始日期时间序列 -> getIpoRsDateSSeries


# 获取现场推介起始日期 -> getIpoRsDateS


# 获取现场推介截止日期时间序列 -> getIpoRsDateESeries


# 获取现场推介截止日期 -> getIpoRsDateE


# 获取网下配售结果公告日时间序列 -> getIpoPlacingDateSeries


# 获取网下配售结果公告日 -> getIpoPlacingDate


# 获取其它发行起始日期时间序列 -> getIpoOtherStartDateSeries


# 获取其它发行起始日期 -> getIpoOtherStartDate


# 获取其它发行截止日期时间序列 -> getIpoOtherEnddateSeries


# 获取其它发行截止日期 -> getIpoOtherEnddate


# 获取提交注册日时间序列 -> getIpoSubmitRegisTDateSeries


# 获取提交注册日 -> getIpoSubmitRegisTDate


# 获取注册成功日(证监会审核批文日)时间序列 -> getIpoRegisTDateSeries


# 获取注册成功日(证监会审核批文日) -> getIpoRegisTDate


# 获取申报基准日时间序列 -> getIpoMrQDateSeries


# 获取申报基准日 -> getIpoMrQDate


# 获取网下报备起始日时间序列 -> getIpoOrStartDateSeries


# 获取网下报备起始日 -> getIpoOrStartDate


# 获取首发市盈率(摊薄)时间序列 -> getIpoDilutedPeSeries


# 获取首发市盈率(摊薄) -> getIpoDilutedPe


# 获取首发市盈率(加权)时间序列 -> getIpoWeightedPeSeries


# 获取首发市盈率(加权) -> getIpoWeightedPe


# 获取发行市净率时间序列 -> getIpoPbSeries


# 获取发行市净率 -> getIpoPb


# 获取首发时所属行业市盈率时间序列 -> getIpoIndustryPeSeries


# 获取首发时所属行业市盈率 -> getIpoIndustryPe


# 获取预计发行股数时间序列 -> getIpoAmountEstSeries


# 获取预计发行股数 -> getIpoAmountEst


# 获取预计募投项目投资总额时间序列 -> getIpoNetCollectionEstSeries


# 获取预计募投项目投资总额 -> getIpoNetCollectionEst


# 获取首发超募资金时间序列 -> getIpoBeyondActualColleCSeries


# 获取首发超募资金 -> getIpoBeyondActualColleC


# 获取售股股东应摊承销与保荐费用时间序列 -> getIpoUnderwritingFeesShareholderSeries


# 获取售股股东应摊承销与保荐费用 -> getIpoUnderwritingFeesShareholder


# 获取承销商认购余额时间序列 -> getIpoSubByDIsTrSeries


# 获取承销商认购余额 -> getIpoSubByDIsTr


# 获取回拨比例时间序列 -> getIpoReallocationPctSeries


# 获取回拨比例 -> getIpoReallocationPct


# 获取向战略投资者配售数量时间序列 -> getIpoAmtToInStInvestorSeries


# 获取向战略投资者配售数量 -> getIpoAmtToInStInvestor


# 获取其它发行数量时间序列 -> getIpoAmtToOtherSeries


# 获取其它发行数量 -> getIpoAmtToOther


# 获取近三年研发投入占比时间序列 -> getIpoRdInvestSeries


# 获取近三年研发投入占比 -> getIpoRdInvest


# 获取近三年研发投入累计额时间序列 -> getIpoInvestAmountSeries


# 获取近三年研发投入累计额 -> getIpoInvestAmount


# 获取研发人员占比时间序列 -> getIpoRdPersonSeries


# 获取研发人员占比 -> getIpoRdPerson


# 获取发明专利个数时间序列 -> getIpoInventionSeries


# 获取发明专利个数 -> getIpoInvention


# 获取近一年营收额时间序列 -> getIpoRevenueSeries


# 获取近一年营收额 -> getIpoRevenue


# 获取被剔除的申报量占比时间序列 -> getPoQeSeries


# 获取被剔除的申报量占比 -> getPoQe


# 获取增发进度时间序列 -> getFellowProgressSeries


# 获取增发进度 -> getFellowProgress


# 获取增发价格时间序列 -> getFellowPriceSeries


# 获取增发价格 -> getFellowPrice


# 获取增发数量时间序列 -> getFellowAmountSeries


# 获取增发数量 -> getFellowAmount


# 获取增发上市日时间序列 -> getFellowListedDateSeries


# 获取增发上市日 -> getFellowListedDate


# 获取增发募集资金时间序列 -> getFellowCollectionSeries


# 获取增发募集资金 -> getFellowCollection


# 获取区间增发募集资金合计时间序列 -> getFellowCollectionTSeries


# 获取区间增发募集资金合计 -> getFellowCollectionT


# 获取增发费用时间序列 -> getFellowExpenseSeries


# 获取增发费用 -> getFellowExpense


# 获取增发实际募集资金时间序列 -> getFellowNetCollectionSeries


# 获取增发实际募集资金 -> getFellowNetCollection


# 获取定向增发基准价格时间序列 -> getFellowBenchmarkPriceSeries


# 获取定向增发基准价格 -> getFellowBenchmarkPrice


# 获取定向增发预案价格相对基准价格比率时间序列 -> getFellowPriceToReservePriceSeries


# 获取定向增发预案价格相对基准价格比率 -> getFellowPriceToReservePrice


# 获取定向增发实际价格相对基准价格比率时间序列 -> getFellowPriceToBenchmarkPriceSeries


# 获取定向增发实际价格相对基准价格比率 -> getFellowPriceToBenchmarkPrice


# 获取区间定增次数时间序列 -> getFellowNSeries


# 获取区间定增次数 -> getFellowN


# 获取总中签率时间序列 -> getFellowTotalRatioSeries


# 获取总中签率 -> getFellowTotalRatio


# 获取公开发行中签率时间序列 -> getFellowPublicRatioSeries


# 获取公开发行中签率 -> getFellowPublicRatio


# 获取增发承销方式时间序列 -> getFellowUndRTypeSeries


# 获取增发承销方式 -> getFellowUndRType


# 获取增发主承销商时间序列 -> getFellowLeadUndRSeries


# 获取增发主承销商 -> getFellowLeadUndR


# 获取增发保荐机构(上市推荐人)时间序列 -> getFellowDeputyUndRSeries


# 获取增发保荐机构(上市推荐人) -> getFellowDeputyUndR


# 获取增发分销商时间序列 -> getFellowNominatorSeries


# 获取增发分销商 -> getFellowNominator


# 获取总有效申购户数时间序列 -> getFellowDistOrSeries


# 获取总有效申购户数 -> getFellowDistOr


# 获取总有效申购股数时间序列 -> getFellowInterCodNatOrSeries


# 获取总有效申购股数 -> getFellowInterCodNatOr


# 获取总超额认购倍数时间序列 -> getFellowCashRatioSeries


# 获取总超额认购倍数 -> getFellowCashRatio


# 获取公开发行认购有效申购户数时间序列 -> getFellowCapRatioSeries


# 获取公开发行认购有效申购户数 -> getFellowCapRatio


# 获取公开发行比例认购有效申购股数时间序列 -> getFellowCashAmtSeries


# 获取公开发行比例认购有效申购股数 -> getFellowCashAmt


# 获取公开发行超额认购倍数时间序列 -> getFellowCashEffAccSeries


# 获取公开发行超额认购倍数 -> getFellowCashEffAcc


# 获取老股东优先配售有效申购户数时间序列 -> getFellowCapeFfAccSeries


# 获取老股东优先配售有效申购户数 -> getFellowCapeFfAcc


# 获取老股东优先配售有效申购股数时间序列 -> getFellowCapeFfAmtSeries


# 获取老股东优先配售有效申购股数 -> getFellowCapeFfAmt


# 获取其它公众投资者有效申购户数时间序列 -> getFellowSubAccByPubSeries


# 获取其它公众投资者有效申购户数 -> getFellowSubAccByPub


# 获取其它公众投资者有效申购股数时间序列 -> getFellowOverSubRatioSeries


# 获取其它公众投资者有效申购股数 -> getFellowOverSubRatio


# 获取网下机构投资者有效申购户数时间序列 -> getFellowAmtByPlacingSeries


# 获取网下机构投资者有效申购户数 -> getFellowAmtByPlacing


# 获取网下机构投资者有效申购股数时间序列 -> getFellowSubAmtByPlacingSeries


# 获取网下机构投资者有效申购股数 -> getFellowSubAmtByPlacing


# 获取网上向老股东优先配售数量时间序列 -> getFellowAmtToInStSeries


# 获取网上向老股东优先配售数量 -> getFellowAmtToInSt


# 获取网上向老股东优先配售比例时间序列 -> getFellowAmtToInCorpSeries


# 获取网上向老股东优先配售比例 -> getFellowAmtToInCorp


# 获取网下向老股东优先配售数量时间序列 -> getFellowOtcPreAmtOrgSeries


# 获取网下向老股东优先配售数量 -> getFellowOtcPreAmtOrg


# 获取向其它公众投资者配售数量时间序列 -> getFellowAmtOtherPubSeries


# 获取向其它公众投资者配售数量 -> getFellowAmtOtherPub


# 获取定向配售数量时间序列 -> getFellowAmtTargetedSeries


# 获取定向配售数量 -> getFellowAmtTargeted


# 获取向原流通股东定向配售数量时间序列 -> getFellowAmtOrgTradableSeries


# 获取向原流通股东定向配售数量 -> getFellowAmtOrgTradable


# 获取向基金配售数量时间序列 -> getFellowAmtFundSeries


# 获取向基金配售数量 -> getFellowAmtFund


# 获取网下发售比例时间序列 -> getFellowOtcAmtPctSeries


# 获取网下发售比例 -> getFellowOtcAmtPct


# 获取承销商认购余股时间序列 -> getRightsIssueSubByDIsTrSeries


# 获取承销商认购余股 -> getRightsIssueSubByDIsTr


# 获取增发公告日时间序列 -> getFellowOfferingDateSeries


# 获取增发公告日 -> getFellowOfferingDate


# 获取公开发行日时间序列 -> getFellowIssueDateSeries


# 获取公开发行日 -> getFellowIssueDate


# 获取向网下增发日期时间序列 -> getFellowOtcDateSeries


# 获取向网下增发日期 -> getFellowOtcDate


# 获取发审委通过公告日时间序列 -> getFellowIecApprovalDateSeries


# 获取发审委通过公告日 -> getFellowIecApprovalDate


# 获取向老股东配售缴款起始日时间序列 -> getFellowPayStartDateSeries


# 获取向老股东配售缴款起始日 -> getFellowPayStartDate


# 获取向老股东配售缴款截止日时间序列 -> getFellowPayEnddateSeries


# 获取向老股东配售缴款截止日 -> getFellowPayEnddate


# 获取增发获准日期时间序列 -> getFellowApprovalDateSeries


# 获取增发获准日期 -> getFellowApprovalDate


# 获取网上路演日时间序列 -> getFellowRoadshowDateSeries


# 获取网上路演日 -> getFellowRoadshowDate


# 获取非公开发行股票受理日时间序列 -> getHandlingDatePiSeries


# 获取非公开发行股票受理日 -> getHandlingDatePi


# 获取股份登记日时间序列 -> getFellowRegisterDateSeries


# 获取股份登记日 -> getFellowRegisterDate


# 获取公开发行数量时间序列 -> getFellowPubAmtSeries


# 获取公开发行数量 -> getFellowPubAmt


# 获取折扣率时间序列 -> getFellowDiscNtRatioSeries


# 获取折扣率 -> getFellowDiscNtRatio


# 获取回拨数量时间序列 -> getFellowTrnFfAmtSeries


# 获取回拨数量 -> getFellowTrnFfAmt


# 获取增发预案价上限时间序列 -> getFellowPriceMaxSeries


# 获取增发预案价上限 -> getFellowPriceMax


# 获取增发预案价下限时间序列 -> getFellowPriceMinSeries


# 获取增发预案价下限 -> getFellowPriceMin


# 获取增发市盈率(摊薄)时间序列 -> getFellowDilutedPeSeries


# 获取增发市盈率(摊薄) -> getFellowDilutedPe


# 获取增发市盈率(加权)时间序列 -> getFellowWeightedPeSeries


# 获取增发市盈率(加权) -> getFellowWeightedPe


# 获取增发预计募集资金时间序列 -> getEstimatedNetCollectionSeries


# 获取增发预计募集资金 -> getEstimatedNetCollection


# 获取配股进度时间序列 -> getRightsIssueProgressSeries


# 获取配股进度 -> getRightsIssueProgress


# 获取配股价格时间序列 -> getRightsIssuePriceSeries


# 获取配股价格 -> getRightsIssuePrice


# 获取配股募集资金时间序列 -> getRightsIssueCollectionSeries


# 获取配股募集资金 -> getRightsIssueCollection


# 获取区间配股募集资金合计时间序列 -> getRightsIssueCollectionTSeries


# 获取区间配股募集资金合计 -> getRightsIssueCollectionT


# 获取配股费用时间序列 -> getRightsIssueExpenseSeries


# 获取配股费用 -> getRightsIssueExpense


# 获取配股实际募集资金时间序列 -> getRightsIssueNetCollectionSeries


# 获取配股实际募集资金 -> getRightsIssueNetCollection


# 获取基准股本时间序列 -> getRightsIssueBaseShareSeries


# 获取基准股本 -> getRightsIssueBaseShare


# 获取每股配股数时间序列 -> getRightsIssuePerShareSeries


# 获取每股配股数 -> getRightsIssuePerShare


# 获取计划配股数时间序列 -> getRightsIssuePlanAmtSeries


# 获取计划配股数 -> getRightsIssuePlanAmt


# 获取实际配股数时间序列 -> getRightsIssueAmountSeries


# 获取实际配股数 -> getRightsIssueAmount


# 获取国有股实际配股数时间序列 -> getRightsIssueActLNumToStateSeries


# 获取国有股实际配股数 -> getRightsIssueActLNumToState


# 获取法人股实际配股数时间序列 -> getRightsIssueActLNumToJurSeries


# 获取法人股实际配股数 -> getRightsIssueActLNumToJur


# 获取职工股实际配股数时间序列 -> getRightsIssueActLNumToEmpSeries


# 获取职工股实际配股数 -> getRightsIssueActLNumToEmp


# 获取转配股实际配股数时间序列 -> getRightsIssueActLNumToTRsfSeries


# 获取转配股实际配股数 -> getRightsIssueActLNumToTRsf


# 获取已流通股实际配股数时间序列 -> getRightsIssueActLNumToTrDSeries


# 获取已流通股实际配股数 -> getRightsIssueActLNumToTrD


# 获取国有股理论配股数时间序列 -> getRightsIssueTheOrNumToStateSeries


# 获取国有股理论配股数 -> getRightsIssueTheOrNumToState


# 获取法人股理论配股数时间序列 -> getRightsIssueTheOrNumToJurSeries


# 获取法人股理论配股数 -> getRightsIssueTheOrNumToJur


# 获取职工股理论配股数时间序列 -> getRightsIssueTheOrNumToEmpSeries


# 获取职工股理论配股数 -> getRightsIssueTheOrNumToEmp


# 获取转配股理论配股数时间序列 -> getRightsIssueTheOrNumToTRsfSeries


# 获取转配股理论配股数 -> getRightsIssueTheOrNumToTRsf


# 获取已流通股理论配股数时间序列 -> getRightsIssueTheOrNumToTrDSeries


# 获取已流通股理论配股数 -> getRightsIssueTheOrNumToTrD


# 获取持股5%以上大股东持股数时间序列 -> getRightsIssueUp5PctNumSeries


# 获取持股5%以上大股东持股数 -> getRightsIssueUp5PctNum


# 获取持股5%以上的大股东理论认购股数时间序列 -> getRightsIssueUp5PctTheOrNumSeries


# 获取持股5%以上的大股东理论认购股数 -> getRightsIssueUp5PctTheOrNum


# 获取持股5%以上大股东认购股数时间序列 -> getRightsIssueUp5PctActLNumSeries


# 获取持股5%以上大股东认购股数 -> getRightsIssueUp5PctActLNum


# 获取配股除权日时间序列 -> getRightsIssueExDividendDateSeries


# 获取配股除权日 -> getRightsIssueExDividendDate


# 获取配股上市日时间序列 -> getRightsIssueListedDateSeries


# 获取配股上市日 -> getRightsIssueListedDate


# 获取缴款起始日时间序列 -> getTenderPaymentDateSeries


# 获取缴款起始日 -> getTenderPaymentDate


# 获取缴款终止日时间序列 -> getRightsIssuePayEnddateSeries


# 获取缴款终止日 -> getRightsIssuePayEnddate


# 获取配股获准公告日时间序列 -> getRightsIssueApprovedDateSeries


# 获取配股获准公告日 -> getRightsIssueApprovedDate


# 获取配股公告日时间序列 -> getRightsIssueAnnCeDateSeries


# 获取配股公告日 -> getRightsIssueAnnCeDate


# 获取配股受理日时间序列 -> getHandlingDateRsSeries


# 获取配股受理日 -> getHandlingDateRs


# 获取配股主承销商时间序列 -> getRightsIssueLeadUndRSeries


# 获取配股主承销商 -> getRightsIssueLeadUndR


# 获取配股方式时间序列 -> getRightsIssueTypeSeries


# 获取配股方式 -> getRightsIssueType


# 获取配股承销方式时间序列 -> getRightsIssueUndRTypeSeries


# 获取配股承销方式 -> getRightsIssueUndRType


# 获取配股分销商时间序列 -> getRightsIssueDeputyUndRSeries


# 获取配股分销商 -> getRightsIssueDeputyUndR


# 获取配股预案价上限时间序列 -> getRightsIssueMaxPricePrePlanSeries


# 获取配股预案价上限 -> getRightsIssueMaxPricePrePlan


# 获取配股预案价下限时间序列 -> getRightsIssueMinPricePrePlanSeries


# 获取配股预案价下限 -> getRightsIssueMinPricePrePlan


# 获取招投标日期时间序列 -> getTenderTenderDateSeries


# 获取招投标日期 -> getTenderTenderDate


# 获取发行起始日期时间序列 -> getIssueFirstIssueSeries


# 获取发行起始日期 -> getIssueFirstIssue


# 获取网上发行起始日期时间序列 -> getIssueFirstIssueOlSeries


# 获取网上发行起始日期 -> getIssueFirstIssueOl


# 获取发行截止日期时间序列 -> getIssueLastIssueSeries


# 获取发行截止日期 -> getIssueLastIssue


# 获取网上发行截止日期时间序列 -> getIssueLastIssueOlSeries


# 获取网上发行截止日期 -> getIssueLastIssueOl


# 获取分销起始日期时间序列 -> getTenderDistRibBeginSeries


# 获取分销起始日期 -> getTenderDistRibBegin


# 获取分销截至日期时间序列 -> getTenderDIsTribeNdSeries


# 获取分销截至日期 -> getTenderDIsTribeNd


# 获取缴款截止日时间序列 -> getTenderPayEnddateSeries


# 获取缴款截止日 -> getTenderPayEnddate


# 获取资金到账确认时间时间序列 -> getTenderConfirmDateSeries


# 获取资金到账确认时间 -> getTenderConfirmDate


# 获取债券过户时间时间序列 -> getTenderTransferDateSeries


# 获取债券过户时间 -> getTenderTransferDate


# 获取证监会/发改委批文日时间序列 -> getIssueOfficialDocDateSeries


# 获取证监会/发改委批文日 -> getIssueOfficialDocDate


# 获取发行注册日期时间序列 -> getIssueRegDateSeries


# 获取发行注册日期 -> getIssueRegDate


# 获取发行注册文件号时间序列 -> getIssueRegNumberSeries


# 获取发行注册文件号 -> getIssueRegNumber


# 获取发行注册额度时间序列 -> getIssueRegAmountSeries


# 获取发行注册额度 -> getIssueRegAmount


# 获取发行年度时间序列 -> getIssueIssueYearSeries


# 获取发行年度 -> getIssueIssueYear


# 获取发行期号时间序列 -> getIssueIssueNumberSeries


# 获取发行期号 -> getIssueIssueNumber


# 获取招标场所时间序列 -> getTenderExchangeSeries


# 获取招标场所 -> getTenderExchange


# 获取承销方式时间序列 -> getAgencyUnderWritTypeSeries


# 获取承销方式 -> getAgencyUnderWritType


# 获取发行价格时间序列 -> getIssueIssuePriceSeries


# 获取发行价格 -> getIssueIssuePrice


# 获取最终发行价格时间序列 -> getTendRstFinalPriceSeries


# 获取最终发行价格 -> getTendRstFinalPrice


# 获取网上发行认购数量限制说明时间序列 -> getIssueRarAIsOlSeries


# 获取网上发行认购数量限制说明 -> getIssueRarAIsOl


# 获取募集资金用途时间序列 -> getFundUseSeries


# 获取募集资金用途 -> getFundUse


# 获取招标方式时间序列 -> getTenderMethodSeries


# 获取招标方式 -> getTenderMethod


# 获取招标标的时间序列 -> getTenderObjectSeries


# 获取招标标的 -> getTenderObject


# 获取招标对象时间序列 -> getTenderAimInvStSeries


# 获取招标对象 -> getTenderAimInvSt


# 获取招标时间时间序列 -> getTenderTimeSeries


# 获取招标时间 -> getTenderTime


# 获取中标确定方式说明时间序列 -> getTenderExplanationSeries


# 获取中标确定方式说明 -> getTenderExplanation


# 获取竞争性招标总额时间序列 -> getTenderCmpTamNtSeries


# 获取竞争性招标总额 -> getTenderCmpTamNt


# 获取基本承销额度时间序列 -> getTenderUnderwritingSeries


# 获取基本承销额度 -> getTenderUnderwriting


# 获取基本承销额追加比例时间序列 -> getTenderAddRatioSeries


# 获取基本承销额追加比例 -> getTenderAddRatio


# 获取基本承销额增加权利时间序列 -> getTenderAdditiveRightsSeries


# 获取基本承销额增加权利 -> getTenderAdditiveRights


# 获取投标利率下限时间序列 -> getTenderThresholdSeries


# 获取投标利率下限 -> getTenderThreshold


# 获取投标利率上限时间序列 -> getTenderCeilingSeries


# 获取投标利率上限 -> getTenderCeiling


# 获取基本投标单位时间序列 -> getTenderTenderUnitSeries


# 获取基本投标单位 -> getTenderTenderUnit


# 获取每标位最低投标量时间序列 -> getTenderLowestAmNtSeries


# 获取每标位最低投标量 -> getTenderLowestAmNt


# 获取每标位最高投标量时间序列 -> getTenderHighestAmNtSeries


# 获取每标位最高投标量 -> getTenderHighestAmNt


# 获取投标说明时间序列 -> getTenderExpLnTenderSeries


# 获取投标说明 -> getTenderExpLnTender


# 获取是否发行失败时间序列 -> getIssueOkSeries


# 获取是否发行失败 -> getIssueOk


# 获取招标书编号时间序列 -> getTendRstDoCumTNumberSeries


# 获取招标书编号 -> getTendRstDoCumTNumber


# 获取缴款总金额时间序列 -> getTendRstPayAmountSeries


# 获取缴款总金额 -> getTendRstPayAmount


# 获取基本承购总额时间序列 -> getTendRstUnderwritingSeries


# 获取基本承购总额 -> getTendRstUnderwriting


# 获取招标总量时间序列 -> getTendRstAmNtSeries


# 获取招标总量 -> getTendRstAmNt


# 获取投标(申购)总量时间序列 -> getTendRstTenderAmountSeries


# 获取投标(申购)总量 -> getTendRstTenderAmount


# 获取应投家数时间序列 -> getTendRstOughtTenderSeries


# 获取应投家数 -> getTendRstOughtTender


# 获取投标家数时间序列 -> getTendRstInvestorTenderedSeries


# 获取投标家数 -> getTendRstInvestorTendered


# 获取有效投标(申购)家数时间序列 -> getTendRstEffectInvestorsSeries


# 获取有效投标(申购)家数 -> getTendRstEffectInvestors


# 获取投标笔数时间序列 -> getTendRstTendersSeries


# 获取投标笔数 -> getTendRstTenders


# 获取有效笔数时间序列 -> getTendRstEffectTenderSeries


# 获取有效笔数 -> getTendRstEffectTender


# 获取无效笔数时间序列 -> getTendRstInEffectTenderSeries


# 获取无效笔数 -> getTendRstInEffectTender


# 获取有效投标总量时间序列 -> getTendRstEffectAmNtSeries


# 获取有效投标总量 -> getTendRstEffectAmNt


# 获取最高投标价位时间序列 -> getTendRstHightestSeries


# 获取最高投标价位 -> getTendRstHightest


# 获取最低投标价位时间序列 -> getTendRstLowestSeries


# 获取最低投标价位 -> getTendRstLowest


# 获取中标总量时间序列 -> getTendRstWinningAmNtSeries


# 获取中标总量 -> getTendRstWinningAmNt


# 获取自营中标总量时间序列 -> getTendRstPrivateTradeSeries


# 获取自营中标总量 -> getTendRstPrivateTrade


# 获取边际中标价位中标总量时间序列 -> getTendRstMarGwInBidderSeries


# 获取边际中标价位中标总量 -> getTendRstMarGwInBidder


# 获取中标家数时间序列 -> getTendRstWinnerBidderSeries


# 获取中标家数 -> getTendRstWinnerBidder


# 获取中标笔数时间序列 -> getTendRstWinningBidderSeries


# 获取中标笔数 -> getTendRstWinningBidder


# 获取最高中标价位时间序列 -> getTendRstHightPriceSeries


# 获取最高中标价位 -> getTendRstHightPrice


# 获取最低中标价位时间序列 -> getTendRstLowPriceSeries


# 获取最低中标价位 -> getTendRstLowPrice


# 获取边际中标价位投标总量时间序列 -> getTendRstMargaMNtSeries


# 获取边际中标价位投标总量 -> getTendRstMargaMNt


# 获取参考收益率时间序列 -> getTendRstReferYieldSeries


# 获取参考收益率 -> getTendRstReferYield


# 获取最终票面利率时间序列 -> getTendRstFinAnCouponSeries


# 获取最终票面利率 -> getTendRstFinAnCoupon


# 获取全场中标利率时间序列 -> getTendRstBidRateSeries


# 获取全场中标利率 -> getTendRstBidRate


# 获取全场中标价格时间序列 -> getTendRstBidPriceSeries


# 获取全场中标价格 -> getTendRstBidPrice


# 获取全场中标利差时间序列 -> getTendRstBidSpreadSeries


# 获取全场中标利差 -> getTendRstBidSpread


# 获取网上发行超额认购倍数(不含优先配售)时间序列 -> getCbListExcessPcHonLSeries


# 获取网上发行超额认购倍数(不含优先配售) -> getCbListExcessPcHonL


# 获取主承销商时间序列 -> getAgencyLeadUnderwriterSeries


# 获取主承销商 -> getAgencyLeadUnderwriter


# 获取主承销商(简称)时间序列 -> getAgencyLeadUnderwritersNSeries


# 获取主承销商(简称) -> getAgencyLeadUnderwritersN


# 获取副主承销商时间序列 -> getAgencyDeputyUnderwriterSeries


# 获取副主承销商 -> getAgencyDeputyUnderwriter


# 获取信用评估机构时间序列 -> getCreditRatingAgencySeries


# 获取信用评估机构 -> getCreditRatingAgency


# 获取簿记管理人时间序列 -> getAgencyBookRunnerSeries


# 获取簿记管理人 -> getAgencyBookRunner


# 获取分销商时间序列 -> getAgencyDistributorSeries


# 获取分销商 -> getAgencyDistributor


# 获取托管人时间序列 -> getAgencyTrusteeSeries


# 获取托管人 -> getAgencyTrustee


# 获取受托管理人时间序列 -> getAgencyBondTrusteeSeries


# 获取受托管理人 -> getAgencyBondTrustee


# 获取会计师事务所时间序列 -> getAgencyExAccountantSeries


# 获取会计师事务所 -> getAgencyExAccountant


# 获取上市保荐机构(上市推荐人)时间序列 -> getAgencyRecommendErSeries


# 获取上市保荐机构(上市推荐人) -> getAgencyRecommendEr


# 获取账簿管理人(海外)时间序列 -> getAgencyBookkeeperSeries


# 获取账簿管理人(海外) -> getAgencyBookkeeper


# 获取牵头经办人(海外)时间序列 -> getAgencyUnderwriterSeries


# 获取牵头经办人(海外) -> getAgencyUnderwriter


# 获取集中簿记建档系统技术支持机构时间序列 -> getAgencyBookSupporterSeries


# 获取集中簿记建档系统技术支持机构 -> getAgencyBookSupporter


# 获取绿色债券认证机构时间序列 -> getAgencyCertificationSeries


# 获取绿色债券认证机构 -> getAgencyCertification


# 获取募集资金专项账户开户行时间序列 -> getAgencyFundBankSeries


# 获取募集资金专项账户开户行 -> getAgencyFundBank


# 获取发行费率时间序列 -> getIssueFeeSeries


# 获取发行费率 -> getIssueFee


# 获取承揽费时间序列 -> getTenderUnderwritingCostSeries


# 获取承揽费 -> getTenderUnderwritingCost


# 获取承销保荐费用时间序列 -> getIssueFeeUnderWRtspOnSeries


# 获取承销保荐费用 -> getIssueFeeUnderWRtspOn


# 获取会计师费用时间序列 -> getIssueFeeAcContSeries


# 获取会计师费用 -> getIssueFeeAcCont


# 获取律师费用时间序列 -> getIssueFeeLegalConsLSeries


# 获取律师费用 -> getIssueFeeLegalConsL


# 获取兑付手续费时间序列 -> getTenderCommissionChargeSeries


# 获取兑付手续费 -> getTenderCommissionCharge


# 获取发审委审批通过日期时间序列 -> getCbListPermitDateSeries


# 获取发审委审批通过日期 -> getCbListPermitDate


# 获取老股东配售日期时间序列 -> getCbListRationDateSeries


# 获取老股东配售日期 -> getCbListRationDate


# 获取老股东配售缴款日时间序列 -> getCbListRationPayMtDateSeries


# 获取老股东配售缴款日 -> getCbListRationPayMtDate


# 获取老股东配售说明时间序列 -> getCbResultExpLnRationSeries


# 获取老股东配售说明 -> getCbResultExpLnRation


# 获取老股东配售代码时间序列 -> getCbListRationCodeSeries


# 获取老股东配售代码 -> getCbListRationCode


# 获取老股东配售简称时间序列 -> getCbListRationNameSeries


# 获取老股东配售简称 -> getCbListRationName


# 获取老股东配售价格时间序列 -> getCbListRationPriceSeries


# 获取老股东配售价格 -> getCbListRationPrice


# 获取老股东配售比例分母时间序列 -> getCbListRationRatioDeSeries


# 获取老股东配售比例分母 -> getCbListRationRatioDe


# 获取每股配售额时间序列 -> getCbResultRationAmtSeries


# 获取每股配售额 -> getCbResultRationAmt


# 获取向老股东配售数量时间序列 -> getCbListRationVolSeries


# 获取向老股东配售数量 -> getCbListRationVol


# 获取老股东配售户数时间序列 -> getCbListOriginalsSeries


# 获取老股东配售户数 -> getCbListOriginals


# 获取网上发行申购代码时间序列 -> getCbListPChaseCodeOnLSeries


# 获取网上发行申购代码 -> getCbListPChaseCodeOnL


# 获取网上发行申购名称时间序列 -> getCbListPChNameOnLSeries


# 获取网上发行申购名称 -> getCbListPChNameOnL


# 获取网上发行申购价格时间序列 -> getCbListPChPriceOnLSeries


# 获取网上发行申购价格 -> getCbListPChPriceOnL


# 获取网下向机构投资者发行数量(不含优先配售)时间序列 -> getCbListVolInStOffSeries


# 获取网下向机构投资者发行数量(不含优先配售) -> getCbListVolInStOff


# 获取定金比例时间序列 -> getCbResultRationCodeSeries


# 获取定金比例 -> getCbResultRationCode


# 获取网下申购下限时间序列 -> getListFloorSubsCrOfFlSeries


# 获取网下申购下限 -> getListFloorSubsCrOfFl


# 获取网下申购上限时间序列 -> getListLimitSubsCrOfFlSeries


# 获取网下申购上限 -> getListLimitSubsCrOfFl


# 获取网上申购下限时间序列 -> getListFloorSubsCroNlSeries


# 获取网上申购下限 -> getListFloorSubsCroNl


# 获取网上申购步长时间序列 -> getListStepSizeSubsCroNlSeries


# 获取网上申购步长 -> getListStepSizeSubsCroNl


# 获取网上申购上限时间序列 -> getListLimitSubsCroNlSeries


# 获取网上申购上限 -> getListLimitSubsCroNl


# 获取原流通股股东可配售额时间序列 -> getCbResultAVaiRationAmtTrAdSeries


# 获取原流通股股东可配售额 -> getCbResultAVaiRationAmtTrAd


# 获取原流通股股东有效申购户数时间序列 -> getCbResultEfInvestorsSeries


# 获取原流通股股东有效申购户数 -> getCbResultEfInvestors


# 获取原流通股股东有效申购金额时间序列 -> getCbResultEfSubsCrPamTSeries


# 获取原流通股股东有效申购金额 -> getCbResultEfSubsCrPamT


# 获取原流通股股东获配金额时间序列 -> getCbResultPlaceAmNttRadSeries


# 获取原流通股股东获配金额 -> getCbResultPlaceAmNttRad


# 获取网上有效申购户数时间序列 -> getCbResultEfSubsCRpoNlSeries


# 获取网上有效申购户数 -> getCbResultEfSubsCRpoNl


# 获取网上有效申购金额时间序列 -> getCbResultEfSubsCrPamToNlSeries


# 获取网上有效申购金额 -> getCbResultEfSubsCrPamToNl


# 获取网上获配金额时间序列 -> getCbResultRationAmToNlSeries


# 获取网上获配金额 -> getCbResultRationAmToNl


# 获取网上获配比例时间序列 -> getCbResultRationRatioOnLSeries


# 获取网上获配比例 -> getCbResultRationRatioOnL


# 获取网上中签率时间序列 -> getCbResultSuCrateOnLSeries


# 获取网上中签率 -> getCbResultSuCrateOnL


# 获取网下有效申购户数时间序列 -> getCbResultEfSubsCRpOffSeries


# 获取网下有效申购户数 -> getCbResultEfSubsCRpOff


# 获取网下有效申购金额时间序列 -> getCbResultEfSubsCrPamToFfSeries


# 获取网下有效申购金额 -> getCbResultEfSubsCrPamToFf


# 获取网下获配金额时间序列 -> getCbResultRationAmtOffSeries


# 获取网下获配金额 -> getCbResultRationAmtOff


# 获取网下中签率时间序列 -> getCbResultSuCrateOffSeries


# 获取网下中签率 -> getCbResultSuCrateOff


# 获取包销余额时间序列 -> getCbResultBalanceSeries


# 获取包销余额 -> getCbResultBalance


# 获取重仓行业投资市值(中信)时间序列 -> getPrtTopIndustryValueCitiCSeries


# 获取重仓行业投资市值(中信) -> getPrtTopIndustryValueCitiC


# 获取重仓行业投资市值(申万)时间序列 -> getPrtTopIndustryValueSwSeries


# 获取重仓行业投资市值(申万) -> getPrtTopIndustryValueSw


# 获取第三方审查机构时间序列 -> getEsGMdc01003Series


# 获取第三方审查机构 -> getEsGMdc01003


# 获取报告范围时间序列 -> getEsGMdc01004Series


# 获取报告范围 -> getEsGMdc01004


# 获取编制依据时间序列 -> getEsGMdc01005Series


# 获取编制依据 -> getEsGMdc01005


# 获取是否遵循/对照联交所标准时间序列 -> getEsGMdc01007Series


# 获取是否遵循/对照联交所标准 -> getEsGMdc01007


# 获取总温室气体排放时间序列 -> getEsGEem01004Series


# 获取总温室气体排放 -> getEsGEem01004


# 获取温室气体减排量时间序列 -> getEsGEem01008Series


# 获取温室气体减排量 -> getEsGEem01008


# 获取是否就气候变化机会进行讨论时间序列 -> getEsGEem01011Series


# 获取是否就气候变化机会进行讨论 -> getEsGEem01011


# 获取是否就气候变化风险进行讨论时间序列 -> getEsGEem01012Series


# 获取是否就气候变化风险进行讨论 -> getEsGEem01012


# 获取氮氧化物排放时间序列 -> getEsGEem02001Series


# 获取氮氧化物排放 -> getEsGEem02001


# 获取二氧化硫排放时间序列 -> getEsGEem02002Series


# 获取二氧化硫排放 -> getEsGEem02002


# 获取悬浮粒子/颗粒物时间序列 -> getEsGEem02003Series


# 获取悬浮粒子/颗粒物 -> getEsGEem02003


# 获取有害废弃物量时间序列 -> getEsGEem03001Series


# 获取有害废弃物量 -> getEsGEem03001


# 获取无害废弃物量时间序列 -> getEsGEem03002Series


# 获取无害废弃物量 -> getEsGEem03002


# 获取废弃物总量时间序列 -> getEsGEem03003Series


# 获取废弃物总量 -> getEsGEem03003


# 获取废弃物回收量时间序列 -> getEsGEem03004Series


# 获取废弃物回收量 -> getEsGEem03004


# 获取总能源消耗时间序列 -> getEsGEre01001Series


# 获取总能源消耗 -> getEsGEre01001


# 获取耗电总量时间序列 -> getEsGEre01002Series


# 获取耗电总量 -> getEsGEre01002


# 获取节省用电量时间序列 -> getEsGEre01003Series


# 获取节省用电量 -> getEsGEre01003


# 获取煤碳使用量时间序列 -> getEsGEre01004Series


# 获取煤碳使用量 -> getEsGEre01004


# 获取天然气消耗时间序列 -> getEsGEre01005Series


# 获取天然气消耗 -> getEsGEre01005


# 获取燃油消耗时间序列 -> getEsGEre01006Series


# 获取燃油消耗 -> getEsGEre01006


# 获取节能量时间序列 -> getEsGEre01007Series


# 获取节能量 -> getEsGEre01007


# 获取纸消耗量时间序列 -> getEsGEre02001Series


# 获取纸消耗量 -> getEsGEre02001


# 获取废纸回收量时间序列 -> getEsGEre02002Series


# 获取废纸回收量 -> getEsGEre02002


# 获取总用水量时间序列 -> getEsGEwa01001Series


# 获取总用水量 -> getEsGEwa01001


# 获取节省水量时间序列 -> getEsGEwa01002Series


# 获取节省水量 -> getEsGEwa01002


# 获取水循环与再利用的总量时间序列 -> getEsGEwa01003Series


# 获取水循环与再利用的总量 -> getEsGEwa01003


# 获取废水/污水排放量时间序列 -> getEsGEwa02002Series


# 获取废水/污水排放量 -> getEsGEwa02002


# 获取废水处理量时间序列 -> getEsGEwa02003Series


# 获取废水处理量 -> getEsGEwa02003


# 获取氨氮时间序列 -> getEsGEwa02004Series


# 获取氨氮 -> getEsGEwa02004


# 获取是否重点排污单位时间序列 -> getEsGEot01003Series


# 获取是否重点排污单位 -> getEsGEot01003


# 获取环保超标或其他违规次数时间序列 -> getEsGEot02002Series


# 获取环保超标或其他违规次数 -> getEsGEot02002


# 获取董事会规模时间序列 -> getEsGGBo01001Series


# 获取董事会规模 -> getEsGGBo01001


# 获取董事会出席率时间序列 -> getEsGGBo01002Series


# 获取董事会出席率 -> getEsGGBo01002


# 获取董事会召开数时间序列 -> getEsGGBo01003Series


# 获取董事会召开数 -> getEsGGBo01003


# 获取参加少于75%会议的董事人数时间序列 -> getEsGGBo01004Series


# 获取参加少于75%会议的董事人数 -> getEsGGBo01004


# 获取监事会召开数时间序列 -> getEsGGBo01005Series


# 获取监事会召开数 -> getEsGGBo01005


# 获取监事出席率时间序列 -> getEsGGBo01006Series


# 获取监事出席率 -> getEsGGBo01006


# 获取是否设有监事委员会主席时间序列 -> getEsGGBo01007Series


# 获取是否设有监事委员会主席 -> getEsGGBo01007


# 获取提名委员会会议数时间序列 -> getEsGGBo01008Series


# 获取提名委员会会议数 -> getEsGGBo01008


# 获取提名委员会会议出席率时间序列 -> getEsGGBo01010Series


# 获取提名委员会会议出席率 -> getEsGGBo01010


# 获取董事会成员受教育背景高于本科的比例时间序列 -> getEsGGBo01014Series


# 获取董事会成员受教育背景高于本科的比例 -> getEsGGBo01014


# 获取女性董事占比时间序列 -> getEsGGBo01015Series


# 获取女性董事占比 -> getEsGGBo01015


# 获取独立董事董事会会议出席率时间序列 -> getEsGGBo03001Series


# 获取独立董事董事会会议出席率 -> getEsGGBo03001


# 获取独立董事占董事会总人数的比例时间序列 -> getEsGGBo03002Series


# 获取独立董事占董事会总人数的比例 -> getEsGGBo03002


# 获取是否有股权激励计划时间序列 -> getEsGGpa02001Series


# 获取是否有股权激励计划 -> getEsGGpa02001


# 获取薪酬委员会会议出席率时间序列 -> getEsGGpa03002Series


# 获取薪酬委员会会议出席率 -> getEsGGpa03002


# 获取薪酬委员会会议数时间序列 -> getEsGGpa03003Series


# 获取薪酬委员会会议数 -> getEsGGpa03003


# 获取审计委员会会议次数时间序列 -> getEsGGad01001Series


# 获取审计委员会会议次数 -> getEsGGad01001


# 获取审计委员会会议出席率时间序列 -> getEsGGad01002Series


# 获取审计委员会会议出席率 -> getEsGGad01002


# 获取是否出具标准无保留意见时间序列 -> getEsGGad02002Series


# 获取是否出具标准无保留意见 -> getEsGGad02002


# 获取雇员总人数时间序列 -> getEsGSem01001Series


# 获取雇员总人数 -> getEsGSem01001


# 获取员工流失率/离职率时间序列 -> getEsGSem01002Series


# 获取员工流失率/离职率 -> getEsGSem01002


# 获取劳动合同签订率时间序列 -> getEsGSem01004Series


# 获取劳动合同签订率 -> getEsGSem01004


# 获取女性员工比例时间序列 -> getEsGSem01005Series


# 获取女性员工比例 -> getEsGSem01005


# 获取少数裔员工比例时间序列 -> getEsGSem01006Series


# 获取少数裔员工比例 -> getEsGSem01006


# 获取人均培训课时时间序列 -> getEsGSem02002Series


# 获取人均培训课时 -> getEsGSem02002


# 获取工伤率时间序列 -> getEsGSem03001Series


# 获取工伤率 -> getEsGSem03001


# 获取因工伤损失工作日数时间序列 -> getEsGSem03002Series


# 获取因工伤损失工作日数 -> getEsGSem03002


# 获取职业病发生率时间序列 -> getEsGSem03003Series


# 获取职业病发生率 -> getEsGSem03003


# 获取死亡事故数时间序列 -> getEsGSem03004Series


# 获取死亡事故数 -> getEsGSem03004


# 获取医保覆盖率时间序列 -> getEsGSem04001Series


# 获取医保覆盖率 -> getEsGSem04001


# 获取客户投诉数量时间序列 -> getEsGSpc01001Series


# 获取客户投诉数量 -> getEsGSpc01001


# 获取客户满意度时间序列 -> getEsGSpc01002Series


# 获取客户满意度 -> getEsGSpc01002


# 获取是否有客户反馈系统时间序列 -> getEsGSpc01003Series


# 获取是否有客户反馈系统 -> getEsGSpc01003


# 获取新增专利数时间序列 -> getEsGSpc02004Series


# 获取新增专利数 -> getEsGSpc02004


# 获取供应商数量时间序列 -> getEsGSch01001Series


# 获取供应商数量 -> getEsGSch01001


# 获取(废弃)接受ESG评估的供应商数量时间序列 -> getEsGSch02002Series


# 获取(废弃)接受ESG评估的供应商数量 -> getEsGSch02002


# 获取供应商本地化比例时间序列 -> getEsGSch01002Series


# 获取供应商本地化比例 -> getEsGSch01002


# 获取本地化采购支出占比时间序列 -> getEsGSch02001Series


# 获取本地化采购支出占比 -> getEsGSch02001


# 获取志愿服务时长时间序列 -> getEsGSco02001Series


# 获取志愿服务时长 -> getEsGSco02001


# 获取注册志愿者人数时间序列 -> getEsGSco02002Series


# 获取注册志愿者人数 -> getEsGSco02002


# 获取被调研总次数时间序列 -> getIrNosSeries


# 获取被调研总次数 -> getIrNos


# 获取特定对象调研次数时间序列 -> getIrNoSfSoSeries


# 获取特定对象调研次数 -> getIrNoSfSo


# 获取媒体(政府)调研家数时间序列 -> getIrNoMiSeries


# 获取媒体(政府)调研家数 -> getIrNoMi


# 获取个人调研家数时间序列 -> getIrNoPiSeries


# 获取个人调研家数 -> getIrNoPi


# 获取证券公司调研次数时间序列 -> getIrNosCbsCSeries


# 获取证券公司调研次数 -> getIrNosCbsC


# 获取证券公司调研家数时间序列 -> getIrNoiIsCSeries


# 获取证券公司调研家数 -> getIrNoiIsC


# 获取调研最多的证券公司时间序列 -> getIrTmsScSeries


# 获取调研最多的证券公司 -> getIrTmsSc


# 获取保险资管调研次数时间序列 -> getIrNoSoIamSeries


# 获取保险资管调研次数 -> getIrNoSoIam


# 获取保险资管调研家数时间序列 -> getIrNoiAmiSeries


# 获取保险资管调研家数 -> getIrNoiAmi


# 获取调研最多的保险资管时间序列 -> getIrTMriAmSeries


# 获取调研最多的保险资管 -> getIrTMriAm


# 获取调研最多的投资机构时间序列 -> getIrTMrIiSeries


# 获取调研最多的投资机构 -> getIrTMrIi


# 获取调研最多的外资机构时间序列 -> getIrTMrFiSeries


# 获取调研最多的外资机构 -> getIrTMrFi


# 获取其他公司调研次数时间序列 -> getIrNosBocSeries


# 获取其他公司调研次数 -> getIrNosBoc


# 获取其他公司调研家数时间序列 -> getIrNoIfOcSeries


# 获取其他公司调研家数 -> getIrNoIfOc


# 获取调研最多的其他公司时间序列 -> getIrOcMrSeries


# 获取调研最多的其他公司 -> getIrOcMr


# 获取出生年份时间序列 -> getFundManagerBirthYearSeries


# 获取出生年份 -> getFundManagerBirthYear


# 获取年龄时间序列 -> getFundManagerAgeSeries


# 获取年龄 -> getFundManagerAge


# 获取学历时间序列 -> getFundManagerEducationSeries


# 获取学历 -> getFundManagerEducation


# 获取国籍时间序列 -> getFundManagerNationalitySeries


# 获取国籍 -> getFundManagerNationality


# 获取简历时间序列 -> getFundManagerResumeSeries


# 获取简历 -> getFundManagerResume


# 获取性别时间序列 -> getFundManagerGenderSeries


# 获取性别 -> getFundManagerGender


# 获取任职日期时间序列 -> getFundManagerStartDateSeries


# 获取任职日期 -> getFundManagerStartDate


# 获取任职天数时间序列 -> getFundManagerOnThePostDaysSeries


# 获取任职天数 -> getFundManagerOnThePostDays


# 获取证券从业日期时间序列 -> getFundManagerStartDateOfManagerCareerSeries


# 获取证券从业日期 -> getFundManagerStartDateOfManagerCareer


# 获取历任基金数时间序列 -> getFundManagerPreviousFundNoSeries


# 获取历任基金数 -> getFundManagerPreviousFundNo


# 获取任职基金数时间序列 -> getFundManagerFundNoSeries


# 获取任职基金数 -> getFundManagerFundNo


# 获取任职基金代码时间序列 -> getFundManagerFundCodesSeries


# 获取任职基金代码 -> getFundManagerFundCodes


# 获取任职基金总规模时间序列 -> getFundManagerTotalNetAssetSeries


# 获取任职基金总规模 -> getFundManagerTotalNetAsset


# 获取任职基金总规模(支持历史)时间序列 -> getFundManagerTotalNetAsset2Series


# 获取任职基金总规模(支持历史) -> getFundManagerTotalNetAsset2


# 获取离职日期时间序列 -> getFundManagerEnddateSeries


# 获取离职日期 -> getFundManagerEnddate


# 获取离任原因时间序列 -> getFundManagerResignationReasonSeries


# 获取离任原因 -> getFundManagerResignationReason


# 获取投资经理背景时间序列 -> getFundManagerBackgroundSeries


# 获取投资经理背景 -> getFundManagerBackground


# 获取任职基金获奖记录时间序列 -> getFundManagerAwardRecordSeries


# 获取任职基金获奖记录 -> getFundManagerAwardRecord


# 获取履任以来获奖总次数时间序列 -> getFundManagerAwardRecordNumSeries


# 获取履任以来获奖总次数 -> getFundManagerAwardRecordNum


# 获取超越基准总回报时间序列 -> getFundManagerTotalReturnOverBenchmarkSeries


# 获取超越基准总回报 -> getFundManagerTotalReturnOverBenchmark


# 获取任职年化回报时间序列 -> getNavPeriodicAnnualIZedReturnSeries


# 获取任职年化回报 -> getNavPeriodicAnnualIZedReturn


# 获取任期最大回报时间序列 -> getFundManagerMaxReturnSeries


# 获取任期最大回报 -> getFundManagerMaxReturn


# 获取现任基金最佳回报时间序列 -> getFundManagerBestPerformanceSeries


# 获取现任基金最佳回报 -> getFundManagerBestPerformance


# 获取资本项目规模维持率时间序列 -> getMaintenanceSeries


# 获取资本项目规模维持率 -> getMaintenance


# 获取毛利(TTM)时间序列 -> getGrossMarginTtM2Series


# 获取毛利(TTM) -> getGrossMarginTtM2


# 获取毛利时间序列 -> getGrossMarginSeries


# 获取毛利 -> getGrossMargin


# 获取毛利(TTM)_GSD时间序列 -> getGrossMarginTtM3Series


# 获取毛利(TTM)_GSD -> getGrossMarginTtM3


# 获取毛利_GSD时间序列 -> getWgsDGrossMargin2Series


# 获取毛利_GSD -> getWgsDGrossMargin2


# 获取毛利(TTM)_PIT时间序列 -> getFaGpTtMSeries


# 获取毛利(TTM)_PIT -> getFaGpTtM


# 获取毛利(TTM,只有最新数据)时间序列 -> getGrossMarginTtMSeries


# 获取毛利(TTM,只有最新数据) -> getGrossMarginTtM


# 获取经营活动净收益(TTM)时间序列 -> getOperateIncomeTtM2Series


# 获取经营活动净收益(TTM) -> getOperateIncomeTtM2


# 获取经营活动净收益时间序列 -> getOperateIncomeSeries


# 获取经营活动净收益 -> getOperateIncome


# 获取经营活动净收益(TTM)_GSD时间序列 -> getOperateIncomeTtM3Series


# 获取经营活动净收益(TTM)_GSD -> getOperateIncomeTtM3


# 获取经营活动净收益_PIT时间序列 -> getFaOAIncomeSeries


# 获取经营活动净收益_PIT -> getFaOAIncome


# 获取经营活动净收益(TTM)_PIT时间序列 -> getFaOperaCtIncomeTtMSeries


# 获取经营活动净收益(TTM)_PIT -> getFaOperaCtIncomeTtM


# 获取经营活动净收益(TTM,只有最新数据)时间序列 -> getOperateIncomeTtMSeries


# 获取经营活动净收益(TTM,只有最新数据) -> getOperateIncomeTtM


# 获取价值变动净收益(TTM)时间序列 -> getInvestIncomeTtM2Series


# 获取价值变动净收益(TTM) -> getInvestIncomeTtM2


# 获取价值变动净收益时间序列 -> getInvestIncomeSeries


# 获取价值变动净收益 -> getInvestIncome


# 获取价值变动净收益(TTM)_GSD时间序列 -> getInvestIncomeTtM3Series


# 获取价值变动净收益(TTM)_GSD -> getInvestIncomeTtM3


# 获取价值变动净收益(TTM)_PIT时间序列 -> getFaChavAlIncomeTtMSeries


# 获取价值变动净收益(TTM)_PIT -> getFaChavAlIncomeTtM


# 获取价值变动净收益(TTM,只有最新数据)时间序列 -> getInvestIncomeTtMSeries


# 获取价值变动净收益(TTM,只有最新数据) -> getInvestIncomeTtM


# 获取研发支出前利润时间序列 -> getEBrSeries


# 获取研发支出前利润 -> getEBr


# 获取全部投入资本时间序列 -> getInvestCapitalSeries


# 获取全部投入资本 -> getInvestCapital


# 获取全部投入资本_GSD时间序列 -> getWgsDInvestCapital2Series


# 获取全部投入资本_GSD -> getWgsDInvestCapital2


# 获取全部投入资本_PIT时间序列 -> getFaInvestCapitalSeries


# 获取全部投入资本_PIT -> getFaInvestCapital


# 获取营运资本时间序列 -> getWorkingCapitalSeries


# 获取营运资本 -> getWorkingCapital


# 获取营运资本_GSD时间序列 -> getWgsDWorkingCapital2Series


# 获取营运资本_GSD -> getWgsDWorkingCapital2


# 获取营运资本变动_GSD时间序列 -> getWgsDWKCapChgSeries


# 获取营运资本变动_GSD -> getWgsDWKCapChg


# 获取净营运资本时间序列 -> getNetworkingCapitalSeries


# 获取净营运资本 -> getNetworkingCapital


# 获取净营运资本_GSD时间序列 -> getWgsDNetworkingCapital2Series


# 获取净营运资本_GSD -> getWgsDNetworkingCapital2


# 获取单季度.营运资本变动_GSD时间序列 -> getWgsDQfaWKCapChgSeries


# 获取单季度.营运资本变动_GSD -> getWgsDQfaWKCapChg


# 获取留存收益时间序列 -> getRetainedEarningsSeries


# 获取留存收益 -> getRetainedEarnings


# 获取留存收益_GSD时间序列 -> getWgsDComEqRetainEarnSeries


# 获取留存收益_GSD -> getWgsDComEqRetainEarn


# 获取留存收益_PIT时间序列 -> getFaRetainEarnSeries


# 获取留存收益_PIT -> getFaRetainEarn


# 获取带息债务时间序列 -> getInterestDebtSeries


# 获取带息债务 -> getInterestDebt


# 获取带息债务_GSD时间序列 -> getWgsDInterestDebt2Series


# 获取带息债务_GSD -> getWgsDInterestDebt2


# 获取带息债务_PIT时间序列 -> getFaInterestDebtSeries


# 获取带息债务_PIT -> getFaInterestDebt


# 获取有形净值/带息债务_PIT时间序列 -> getFaTangibleAToInterestDebtSeries


# 获取有形净值/带息债务_PIT -> getFaTangibleAToInterestDebt


# 获取EBITDA/带息债务时间序列 -> getEbItDatoInterestDebtSeries


# 获取EBITDA/带息债务 -> getEbItDatoInterestDebt


# 获取净债务时间序列 -> getNetDebtSeries


# 获取净债务 -> getNetDebt


# 获取净债务_GSD时间序列 -> getWgsDNetDebt2Series


# 获取净债务_GSD -> getWgsDNetDebt2


# 获取净债务_PIT时间序列 -> getFaNetDebtSeries


# 获取净债务_PIT -> getFaNetDebt


# 获取有形净值/净债务_PIT时间序列 -> getFaTangibleAssetToNetDebtSeries


# 获取有形净值/净债务_PIT -> getFaTangibleAssetToNetDebt


# 获取当期计提折旧与摊销时间序列 -> getDaPerIdSeries


# 获取当期计提折旧与摊销 -> getDaPerId


# 获取当期计提折旧与摊销_GSD时间序列 -> getWgsDDa2Series


# 获取当期计提折旧与摊销_GSD -> getWgsDDa2


# 获取贷款总额时间序列 -> getTotalLoanNSeries


# 获取贷款总额 -> getTotalLoanN


# 获取贷款总额(旧)时间序列 -> getTotalLoanSeries


# 获取贷款总额(旧) -> getTotalLoan


# 获取正常-占贷款总额比时间序列 -> getStmNoteBank9506Series


# 获取正常-占贷款总额比 -> getStmNoteBank9506


# 获取关注-占贷款总额比时间序列 -> getStmNoteBank9507Series


# 获取关注-占贷款总额比 -> getStmNoteBank9507


# 获取次级-占贷款总额比时间序列 -> getStmNoteBank9508Series


# 获取次级-占贷款总额比 -> getStmNoteBank9508


# 获取可疑-占贷款总额比时间序列 -> getStmNoteBank9509Series


# 获取可疑-占贷款总额比 -> getStmNoteBank9509


# 获取损失-占贷款总额比时间序列 -> getStmNoteBank9510Series


# 获取损失-占贷款总额比 -> getStmNoteBank9510


# 获取存款总额时间序列 -> getTotalDepositNSeries


# 获取存款总额 -> getTotalDepositN


# 获取存款总额(旧)时间序列 -> getTotalDepositSeries


# 获取存款总额(旧) -> getTotalDeposit


# 获取存款余额_存款总额时间序列 -> getStmNoteBank647Series


# 获取存款余额_存款总额 -> getStmNoteBank647


# 获取存款平均余额_存款总额时间序列 -> getStmNoteBank648Series


# 获取存款平均余额_存款总额 -> getStmNoteBank648


# 获取存款平均成本率_存款总额时间序列 -> getStmNoteBank646Series


# 获取存款平均成本率_存款总额 -> getStmNoteBank646


# 获取贷款减值准备时间序列 -> getBadDebtProvNSeries


# 获取贷款减值准备 -> getBadDebtProvN


# 获取贷款减值准备(旧)时间序列 -> getBadDebtProvSeries


# 获取贷款减值准备(旧) -> getBadDebtProv


# 获取贷款损失准备充足率时间序列 -> getStmNoteBankArSeries


# 获取贷款损失准备充足率 -> getStmNoteBankAr


# 获取成本收入比时间序列 -> getStmNoteBank129NSeries


# 获取成本收入比 -> getStmNoteBank129N


# 获取成本收入比(旧)时间序列 -> getStmNoteBank129Series


# 获取成本收入比(旧) -> getStmNoteBank129


# 获取存贷款比率时间序列 -> getLoanDePoRatioNSeries


# 获取存贷款比率 -> getLoanDePoRatioN


# 获取存贷款比率(人民币)时间序列 -> getLoanDePoRatioRMbNSeries


# 获取存贷款比率(人民币) -> getLoanDePoRatioRMbN


# 获取存贷款比率(外币)时间序列 -> getLoanDePoRatioNormBNSeries


# 获取存贷款比率(外币) -> getLoanDePoRatioNormBN


# 获取存贷款比率(旧)时间序列 -> getLoanDePoRatioSeries


# 获取存贷款比率(旧) -> getLoanDePoRatio


# 获取存贷款比率(人民币)(旧)时间序列 -> getLoanDePoRatioRMbSeries


# 获取存贷款比率(人民币)(旧) -> getLoanDePoRatioRMb


# 获取存贷款比率(外币)(旧)时间序列 -> getLoanDePoRatioNormBSeries


# 获取存贷款比率(外币)(旧) -> getLoanDePoRatioNormB


# 获取不良贷款比率时间序列 -> getNPlRatioNSeries


# 获取不良贷款比率 -> getNPlRatioN


# 获取不良贷款比率(旧)时间序列 -> getNPlRatioSeries


# 获取不良贷款比率(旧) -> getNPlRatio


# 获取不良贷款拨备覆盖率时间序列 -> getBadDebtProvCoverageNSeries


# 获取不良贷款拨备覆盖率 -> getBadDebtProvCoverageN


# 获取不良贷款拨备覆盖率(旧)时间序列 -> getBadDebtProvCoverageSeries


# 获取不良贷款拨备覆盖率(旧) -> getBadDebtProvCoverage


# 获取拆出资金比率时间序列 -> getLendToBanksRatioNSeries


# 获取拆出资金比率 -> getLendToBanksRatioN


# 获取拆出资金比率(旧)时间序列 -> getLendToBanksRatioSeries


# 获取拆出资金比率(旧) -> getLendToBanksRatio


# 获取拆入资金比率时间序列 -> getLoanFromBanksRatioNSeries


# 获取拆入资金比率 -> getLoanFromBanksRatioN


# 获取拆入资金比率(旧)时间序列 -> getLoanFromBanksRatioSeries


# 获取拆入资金比率(旧) -> getLoanFromBanksRatio


# 获取备付金比率(人民币)时间序列 -> getReserveRatioRMbNSeries


# 获取备付金比率(人民币) -> getReserveRatioRMbN


# 获取备付金比率(人民币)(旧)时间序列 -> getReserveRatioRMbSeries


# 获取备付金比率(人民币)(旧) -> getReserveRatioRMb


# 获取备付金比率(外币)时间序列 -> getReserveRatioFcNSeries


# 获取备付金比率(外币) -> getReserveRatioFcN


# 获取备付金比率(外币)(旧)时间序列 -> getReserveRatioFcSeries


# 获取备付金比率(外币)(旧) -> getReserveRatioFc


# 获取不良贷款余额时间序列 -> getStmNoteBank26Series


# 获取不良贷款余额 -> getStmNoteBank26


# 获取不良贷款余额_企业贷款及垫款时间序列 -> getStmNoteBank691Series


# 获取不良贷款余额_企业贷款及垫款 -> getStmNoteBank691


# 获取不良贷款余额_个人贷款及垫款时间序列 -> getStmNoteBank692Series


# 获取不良贷款余额_个人贷款及垫款 -> getStmNoteBank692


# 获取不良贷款余额_票据贴现时间序列 -> getStmNoteBank693Series


# 获取不良贷款余额_票据贴现 -> getStmNoteBank693


# 获取不良贷款余额_个人住房贷款时间序列 -> getStmNoteBank694Series


# 获取不良贷款余额_个人住房贷款 -> getStmNoteBank694


# 获取不良贷款余额_个人消费贷款时间序列 -> getStmNoteBank695Series


# 获取不良贷款余额_个人消费贷款 -> getStmNoteBank695


# 获取不良贷款余额_信用卡应收账款时间序列 -> getStmNoteBank696Series


# 获取不良贷款余额_信用卡应收账款 -> getStmNoteBank696


# 获取不良贷款余额_经营性贷款时间序列 -> getStmNoteBank697Series


# 获取不良贷款余额_经营性贷款 -> getStmNoteBank697


# 获取不良贷款余额_汽车贷款时间序列 -> getStmNoteBank698Series


# 获取不良贷款余额_汽车贷款 -> getStmNoteBank698


# 获取不良贷款余额_其他个人贷款时间序列 -> getStmNoteBank699Series


# 获取不良贷款余额_其他个人贷款 -> getStmNoteBank699


# 获取不良贷款余额_总计时间序列 -> getStmNoteBank690Series


# 获取不良贷款余额_总计 -> getStmNoteBank690


# 获取不良贷款余额_信用贷款时间序列 -> getStmNoteBank751Series


# 获取不良贷款余额_信用贷款 -> getStmNoteBank751


# 获取不良贷款余额_保证贷款时间序列 -> getStmNoteBank752Series


# 获取不良贷款余额_保证贷款 -> getStmNoteBank752


# 获取不良贷款余额_抵押贷款时间序列 -> getStmNoteBank753Series


# 获取不良贷款余额_抵押贷款 -> getStmNoteBank753


# 获取不良贷款余额_质押贷款时间序列 -> getStmNoteBank754Series


# 获取不良贷款余额_质押贷款 -> getStmNoteBank754


# 获取不良贷款余额_短期贷款时间序列 -> getStmNoteBank811Series


# 获取不良贷款余额_短期贷款 -> getStmNoteBank811


# 获取不良贷款余额_中长期贷款时间序列 -> getStmNoteBank812Series


# 获取不良贷款余额_中长期贷款 -> getStmNoteBank812


# 获取不良贷款余额(按行业)时间序列 -> getStmNoteBank66Series


# 获取不良贷款余额(按行业) -> getStmNoteBank66


# 获取中长期贷款比率(人民币)时间序列 -> getMedLongLoanRatioRMbNSeries


# 获取中长期贷款比率(人民币) -> getMedLongLoanRatioRMbN


# 获取中长期贷款比率(人民币)(旧)时间序列 -> getMedLongLoanRatioRMbSeries


# 获取中长期贷款比率(人民币)(旧) -> getMedLongLoanRatioRMb


# 获取中长期贷款比率(外币)时间序列 -> getMedLongLoanRatioFcNSeries


# 获取中长期贷款比率(外币) -> getMedLongLoanRatioFcN


# 获取中长期贷款比率(外币)(旧)时间序列 -> getMedLongLoanRatioFcSeries


# 获取中长期贷款比率(外币)(旧) -> getMedLongLoanRatioFc


# 获取利息回收率时间序列 -> getIntColRatioNSeries


# 获取利息回收率 -> getIntColRatioN


# 获取利息回收率(旧)时间序列 -> getIntColRatioSeries


# 获取利息回收率(旧) -> getIntColRatio


# 获取境外资金运用比率时间序列 -> getForCaputRatioNSeries


# 获取境外资金运用比率 -> getForCaputRatioN


# 获取境外资金运用比率(旧)时间序列 -> getForCaputRatioSeries


# 获取境外资金运用比率(旧) -> getForCaputRatio


# 获取单一最大客户贷款比例时间序列 -> getLargestCustomerLoanNSeries


# 获取单一最大客户贷款比例 -> getLargestCustomerLoanN


# 获取单一最大客户贷款比例(旧)时间序列 -> getLargestCustomerLoanSeries


# 获取单一最大客户贷款比例(旧) -> getLargestCustomerLoan


# 获取最大十家客户贷款占资本净额比例时间序列 -> getTopTenCustomerLoanNSeries


# 获取最大十家客户贷款占资本净额比例 -> getTopTenCustomerLoanN


# 获取净息差时间序列 -> getStmNoteBank144NSeries


# 获取净息差 -> getStmNoteBank144N


# 获取净息差(公布值)时间序列 -> getStmNoteBank5444Series


# 获取净息差(公布值) -> getStmNoteBank5444


# 获取净息差(旧)时间序列 -> getStmNoteBank144Series


# 获取净息差(旧) -> getStmNoteBank144


# 获取净利差时间序列 -> getStmNoteBank147NSeries


# 获取净利差 -> getStmNoteBank147N


# 获取净利差(旧)时间序列 -> getStmNoteBank147Series


# 获取净利差(旧) -> getStmNoteBank147


# 获取市场风险资本时间序列 -> getStmNoteBank341Series


# 获取市场风险资本 -> getStmNoteBank341


# 获取银行理财产品余额时间序列 -> getStmNoteBank1778Series


# 获取银行理财产品余额 -> getStmNoteBank1778


# 获取拨贷比时间序列 -> getStmNoteBank55Series


# 获取拨贷比 -> getStmNoteBank55


# 获取库存现金时间序列 -> getStmNoteBank5453Series


# 获取库存现金 -> getStmNoteBank5453


# 获取可用的稳定资金时间序列 -> getStmNoteBankAsFSeries


# 获取可用的稳定资金 -> getStmNoteBankAsF


# 获取所需的稳定资金时间序列 -> getStmNoteBankRsfSeries


# 获取所需的稳定资金 -> getStmNoteBankRsf


# 获取绿色信贷余额时间序列 -> getEsGGcbWindSeries


# 获取绿色信贷余额 -> getEsGGcbWind


# 获取最大十家客户贷款比例(旧)时间序列 -> getTopTenCustomerLoanSeries


# 获取最大十家客户贷款比例(旧) -> getTopTenCustomerLoan


# 获取核心资本净额时间序列 -> getStmNoteBank132NSeries


# 获取核心资本净额 -> getStmNoteBank132N


# 获取核心资本净额(旧)时间序列 -> getStmNoteBank132Series


# 获取核心资本净额(旧) -> getStmNoteBank132


# 获取资本净额时间序列 -> getStmNoteBank131NSeries


# 获取资本净额 -> getStmNoteBank131N


# 获取资本净额(2013)时间序列 -> getStmNoteBankNetEquityCapSeries


# 获取资本净额(2013) -> getStmNoteBankNetEquityCap


# 获取资本净额(旧)时间序列 -> getStmNoteBank131Series


# 获取资本净额(旧) -> getStmNoteBank131


# 获取一级资本净额(2013)时间序列 -> getStmNoteBankTier1CapSeries


# 获取一级资本净额(2013) -> getStmNoteBankTier1Cap


# 获取核心一级资本净额(2013)时间序列 -> getStmNoteBankCoreTier1CapSeries


# 获取核心一级资本净额(2013) -> getStmNoteBankCoreTier1Cap


# 获取核心资本充足率时间序列 -> getCoreCapIADeRatioNSeries


# 获取核心资本充足率 -> getCoreCapIADeRatioN


# 获取核心资本充足率(旧)时间序列 -> getCoreCapIADeRatioSeries


# 获取核心资本充足率(旧) -> getCoreCapIADeRatio


# 获取资本充足率时间序列 -> getCapIADeRatioNSeries


# 获取资本充足率 -> getCapIADeRatioN


# 获取资本充足率(2013)时间序列 -> getStmNoteBankCapAdequacyRatioSeries


# 获取资本充足率(2013) -> getStmNoteBankCapAdequacyRatio


# 获取资本充足率(旧)时间序列 -> getCapIADeRatioSeries


# 获取资本充足率(旧) -> getCapIADeRatio


# 获取一级资本充足率(2013)时间序列 -> getStmNoteBankCapAdequacyRatioT1Series


# 获取一级资本充足率(2013) -> getStmNoteBankCapAdequacyRatioT1


# 获取核心一级资本充足率(2013)时间序列 -> getStmNoteBankCapAdequacyRatioCt1Series


# 获取核心一级资本充足率(2013) -> getStmNoteBankCapAdequacyRatioCt1


# 获取杠杆率时间序列 -> getStmNoteBank171Series


# 获取杠杆率 -> getStmNoteBank171


# 获取资本杠杆率时间序列 -> getStmNoteSec34Series


# 获取资本杠杆率 -> getStmNoteSec34


# 获取流动性覆盖率时间序列 -> getStmNoteBank172Series


# 获取流动性覆盖率 -> getStmNoteBank172


# 获取流动性覆盖率(券商)时间序列 -> getStmNoteSec35Series


# 获取流动性覆盖率(券商) -> getStmNoteSec35


# 获取流动性覆盖率:基本情景时间序列 -> getQStmNoteInSur212540Series


# 获取流动性覆盖率:基本情景 -> getQStmNoteInSur212540


# 获取流动性覆盖率:公司整体:压力情景1时间序列 -> getQStmNoteInSur212541Series


# 获取流动性覆盖率:公司整体:压力情景1 -> getQStmNoteInSur212541


# 获取流动性覆盖率:公司整体:压力情景2时间序列 -> getQStmNoteInSur212542Series


# 获取流动性覆盖率:公司整体:压力情景2 -> getQStmNoteInSur212542


# 获取流动性覆盖率:独立账户:压力情景1时间序列 -> getQStmNoteInSur212543Series


# 获取流动性覆盖率:独立账户:压力情景1 -> getQStmNoteInSur212543


# 获取流动性覆盖率:独立账户:压力情景2时间序列 -> getQStmNoteInSur212544Series


# 获取流动性覆盖率:独立账户:压力情景2 -> getQStmNoteInSur212544


# 获取正常-金额时间序列 -> getStmNoteBank31Series


# 获取正常-金额 -> getStmNoteBank31


# 获取正常-迁徙率时间序列 -> getStmNoteBank9501Series


# 获取正常-迁徙率 -> getStmNoteBank9501


# 获取关注-金额时间序列 -> getStmNoteBank340Series


# 获取关注-金额 -> getStmNoteBank340


# 获取关注-迁徙率时间序列 -> getStmNoteBank9502Series


# 获取关注-迁徙率 -> getStmNoteBank9502


# 获取次级-金额时间序列 -> getStmNoteBank37Series


# 获取次级-金额 -> getStmNoteBank37


# 获取次级-迁徙率时间序列 -> getStmNoteBank9503Series


# 获取次级-迁徙率 -> getStmNoteBank9503


# 获取可疑-金额时间序列 -> getStmNoteBank40Series


# 获取可疑-金额 -> getStmNoteBank40


# 获取可疑-迁徙率时间序列 -> getStmNoteBank9504Series


# 获取可疑-迁徙率 -> getStmNoteBank9504


# 获取损失-金额时间序列 -> getStmNoteBank430Series


# 获取损失-金额 -> getStmNoteBank430


# 获取存款余额_个人存款时间序列 -> getStmNoteBank616Series


# 获取存款余额_个人存款 -> getStmNoteBank616


# 获取存款余额_个人定期存款时间序列 -> getStmNoteBank611Series


# 获取存款余额_个人定期存款 -> getStmNoteBank611


# 获取存款余额_个人活期存款时间序列 -> getStmNoteBank612Series


# 获取存款余额_个人活期存款 -> getStmNoteBank612


# 获取存款余额_公司存款时间序列 -> getStmNoteBank617Series


# 获取存款余额_公司存款 -> getStmNoteBank617


# 获取存款余额_公司定期存款时间序列 -> getStmNoteBank613Series


# 获取存款余额_公司定期存款 -> getStmNoteBank613


# 获取存款余额_公司活期存款时间序列 -> getStmNoteBank614Series


# 获取存款余额_公司活期存款 -> getStmNoteBank614


# 获取存款余额_其它存款时间序列 -> getStmNoteBank615Series


# 获取存款余额_其它存款 -> getStmNoteBank615


# 获取存款平均余额_个人定期存款时间序列 -> getStmNoteBank621Series


# 获取存款平均余额_个人定期存款 -> getStmNoteBank621


# 获取存款平均余额_个人活期存款时间序列 -> getStmNoteBank622Series


# 获取存款平均余额_个人活期存款 -> getStmNoteBank622


# 获取存款平均余额_公司定期存款时间序列 -> getStmNoteBank623Series


# 获取存款平均余额_公司定期存款 -> getStmNoteBank623


# 获取存款平均余额_公司活期存款时间序列 -> getStmNoteBank624Series


# 获取存款平均余额_公司活期存款 -> getStmNoteBank624


# 获取存款平均余额_其它存款时间序列 -> getStmNoteBank625Series


# 获取存款平均余额_其它存款 -> getStmNoteBank625


# 获取存款平均余额_企业存款时间序列 -> getStmNoteBank50Series


# 获取存款平均余额_企业存款 -> getStmNoteBank50


# 获取存款平均余额_储蓄存款时间序列 -> getStmNoteBank52Series


# 获取存款平均余额_储蓄存款 -> getStmNoteBank52


# 获取存款平均成本率_个人定期存款时间序列 -> getStmNoteBank641Series


# 获取存款平均成本率_个人定期存款 -> getStmNoteBank641


# 获取存款平均成本率_个人活期存款时间序列 -> getStmNoteBank642Series


# 获取存款平均成本率_个人活期存款 -> getStmNoteBank642


# 获取存款平均成本率_公司定期存款时间序列 -> getStmNoteBank643Series


# 获取存款平均成本率_公司定期存款 -> getStmNoteBank643


# 获取存款平均成本率_公司活期存款时间序列 -> getStmNoteBank644Series


# 获取存款平均成本率_公司活期存款 -> getStmNoteBank644


# 获取存款平均成本率_其它存款时间序列 -> getStmNoteBank645Series


# 获取存款平均成本率_其它存款 -> getStmNoteBank645


# 获取存款平均成本率_企业存款时间序列 -> getStmNoteBank51Series


# 获取存款平均成本率_企业存款 -> getStmNoteBank51


# 获取存款平均成本率_储蓄存款时间序列 -> getStmNoteBank53Series


# 获取存款平均成本率_储蓄存款 -> getStmNoteBank53


# 获取贷款余额_总计时间序列 -> getStmNoteBank680Series


# 获取贷款余额_总计 -> getStmNoteBank680


# 获取贷款余额_企业贷款及垫款时间序列 -> getStmNoteBank681Series


# 获取贷款余额_企业贷款及垫款 -> getStmNoteBank681


# 获取贷款余额_个人贷款及垫款时间序列 -> getStmNoteBank682Series


# 获取贷款余额_个人贷款及垫款 -> getStmNoteBank682


# 获取贷款余额_票据贴现时间序列 -> getStmNoteBank683Series


# 获取贷款余额_票据贴现 -> getStmNoteBank683


# 获取贷款余额_个人住房贷款时间序列 -> getStmNoteBank684Series


# 获取贷款余额_个人住房贷款 -> getStmNoteBank684


# 获取贷款余额_个人消费贷款时间序列 -> getStmNoteBank685Series


# 获取贷款余额_个人消费贷款 -> getStmNoteBank685


# 获取贷款余额_信用卡应收账款时间序列 -> getStmNoteBank686Series


# 获取贷款余额_信用卡应收账款 -> getStmNoteBank686


# 获取贷款余额_经营性贷款时间序列 -> getStmNoteBank687Series


# 获取贷款余额_经营性贷款 -> getStmNoteBank687


# 获取贷款余额_汽车贷款时间序列 -> getStmNoteBank688Series


# 获取贷款余额_汽车贷款 -> getStmNoteBank688


# 获取贷款余额_其他个人贷款时间序列 -> getStmNoteBank689Series


# 获取贷款余额_其他个人贷款 -> getStmNoteBank689


# 获取不良贷款率_企业贷款及垫款时间序列 -> getStmNoteBank701Series


# 获取不良贷款率_企业贷款及垫款 -> getStmNoteBank701


# 获取不良贷款率_个人贷款及垫款时间序列 -> getStmNoteBank702Series


# 获取不良贷款率_个人贷款及垫款 -> getStmNoteBank702


# 获取不良贷款率_票据贴现时间序列 -> getStmNoteBank703Series


# 获取不良贷款率_票据贴现 -> getStmNoteBank703


# 获取不良贷款率_个人住房贷款时间序列 -> getStmNoteBank704Series


# 获取不良贷款率_个人住房贷款 -> getStmNoteBank704


# 获取不良贷款率_个人消费贷款时间序列 -> getStmNoteBank705Series


# 获取不良贷款率_个人消费贷款 -> getStmNoteBank705


# 获取不良贷款率_信用卡应收账款时间序列 -> getStmNoteBank706Series


# 获取不良贷款率_信用卡应收账款 -> getStmNoteBank706


# 获取不良贷款率_经营性贷款时间序列 -> getStmNoteBank707Series


# 获取不良贷款率_经营性贷款 -> getStmNoteBank707


# 获取不良贷款率_汽车贷款时间序列 -> getStmNoteBank708Series


# 获取不良贷款率_汽车贷款 -> getStmNoteBank708


# 获取不良贷款率_其他个人贷款时间序列 -> getStmNoteBank709Series


# 获取不良贷款率_其他个人贷款 -> getStmNoteBank709


# 获取贷款平均余额_总计时间序列 -> getStmNoteBank700Series


# 获取贷款平均余额_总计 -> getStmNoteBank700


# 获取贷款平均余额_企业贷款及垫款时间序列 -> getStmNoteBank711Series


# 获取贷款平均余额_企业贷款及垫款 -> getStmNoteBank711


# 获取贷款平均余额_个人贷款及垫款时间序列 -> getStmNoteBank712Series


# 获取贷款平均余额_个人贷款及垫款 -> getStmNoteBank712


# 获取贷款平均余额_票据贴现时间序列 -> getStmNoteBank713Series


# 获取贷款平均余额_票据贴现 -> getStmNoteBank713


# 获取贷款平均余额_个人住房贷款时间序列 -> getStmNoteBank714Series


# 获取贷款平均余额_个人住房贷款 -> getStmNoteBank714


# 获取贷款平均余额_个人消费贷款时间序列 -> getStmNoteBank715Series


# 获取贷款平均余额_个人消费贷款 -> getStmNoteBank715


# 获取贷款平均余额_信用卡应收账款时间序列 -> getStmNoteBank716Series


# 获取贷款平均余额_信用卡应收账款 -> getStmNoteBank716


# 获取贷款平均余额_经营性贷款时间序列 -> getStmNoteBank717Series


# 获取贷款平均余额_经营性贷款 -> getStmNoteBank717


# 获取贷款平均余额_汽车贷款时间序列 -> getStmNoteBank718Series


# 获取贷款平均余额_汽车贷款 -> getStmNoteBank718


# 获取贷款平均余额_其他个人贷款时间序列 -> getStmNoteBank719Series


# 获取贷款平均余额_其他个人贷款 -> getStmNoteBank719


# 获取贷款余额_信用贷款时间序列 -> getStmNoteBank741Series


# 获取贷款余额_信用贷款 -> getStmNoteBank741


# 获取贷款余额_保证贷款时间序列 -> getStmNoteBank742Series


# 获取贷款余额_保证贷款 -> getStmNoteBank742


# 获取贷款余额_抵押贷款时间序列 -> getStmNoteBank743Series


# 获取贷款余额_抵押贷款 -> getStmNoteBank743


# 获取贷款余额_质押贷款时间序列 -> getStmNoteBank744Series


# 获取贷款余额_质押贷款 -> getStmNoteBank744


# 获取不良贷款率_总计时间序列 -> getStmNoteBank730Series


# 获取不良贷款率_总计 -> getStmNoteBank730


# 获取不良贷款率_信用贷款时间序列 -> getStmNoteBank761Series


# 获取不良贷款率_信用贷款 -> getStmNoteBank761


# 获取不良贷款率_保证贷款时间序列 -> getStmNoteBank762Series


# 获取不良贷款率_保证贷款 -> getStmNoteBank762


# 获取不良贷款率_抵押贷款时间序列 -> getStmNoteBank763Series


# 获取不良贷款率_抵押贷款 -> getStmNoteBank763


# 获取不良贷款率_质押贷款时间序列 -> getStmNoteBank764Series


# 获取不良贷款率_质押贷款 -> getStmNoteBank764


# 获取贷款平均余额_信用贷款时间序列 -> getStmNoteBank771Series


# 获取贷款平均余额_信用贷款 -> getStmNoteBank771


# 获取贷款平均余额_保证贷款时间序列 -> getStmNoteBank772Series


# 获取贷款平均余额_保证贷款 -> getStmNoteBank772


# 获取贷款平均余额_抵押贷款时间序列 -> getStmNoteBank773Series


# 获取贷款平均余额_抵押贷款 -> getStmNoteBank773


# 获取贷款平均余额_质押贷款时间序列 -> getStmNoteBank774Series


# 获取贷款平均余额_质押贷款 -> getStmNoteBank774


# 获取贷款余额_短期贷款时间序列 -> getStmNoteBank801Series


# 获取贷款余额_短期贷款 -> getStmNoteBank801


# 获取贷款余额_中长期贷款时间序列 -> getStmNoteBank802Series


# 获取贷款余额_中长期贷款 -> getStmNoteBank802


# 获取不良贷款率_短期贷款时间序列 -> getStmNoteBank821Series


# 获取不良贷款率_短期贷款 -> getStmNoteBank821


# 获取不良贷款率_中长期贷款时间序列 -> getStmNoteBank822Series


# 获取不良贷款率_中长期贷款 -> getStmNoteBank822


# 获取贷款平均余额_短期贷款时间序列 -> getStmNoteBank46Series


# 获取贷款平均余额_短期贷款 -> getStmNoteBank46


# 获取贷款平均余额_中长期贷款时间序列 -> getStmNoteBank48Series


# 获取贷款平均余额_中长期贷款 -> getStmNoteBank48


# 获取贷款余额(按行业)时间序列 -> getStmNoteBank65Series


# 获取贷款余额(按行业) -> getStmNoteBank65


# 获取不良贷款率(按行业)时间序列 -> getStmNoteBank67Series


# 获取不良贷款率(按行业) -> getStmNoteBank67


# 获取逾期保证贷款_3个月以内时间序列 -> getStmNoteBank0021Series


# 获取逾期保证贷款_3个月以内 -> getStmNoteBank0021


# 获取逾期保证贷款_3个月至1年时间序列 -> getStmNoteBank0022Series


# 获取逾期保证贷款_3个月至1年 -> getStmNoteBank0022


# 获取逾期保证贷款_1年以上3年以内时间序列 -> getStmNoteBank0023Series


# 获取逾期保证贷款_1年以上3年以内 -> getStmNoteBank0023


# 获取逾期保证贷款_3年以上时间序列 -> getStmNoteBank0024Series


# 获取逾期保证贷款_3年以上 -> getStmNoteBank0024


# 获取逾期保证贷款合计时间序列 -> getStmNoteBank0025Series


# 获取逾期保证贷款合计 -> getStmNoteBank0025


# 获取逾期信用贷款_3个月以内时间序列 -> getStmNoteBank0011Series


# 获取逾期信用贷款_3个月以内 -> getStmNoteBank0011


# 获取逾期信用贷款_3个月至1年时间序列 -> getStmNoteBank0012Series


# 获取逾期信用贷款_3个月至1年 -> getStmNoteBank0012


# 获取逾期信用贷款_1年以上3年以内时间序列 -> getStmNoteBank0013Series


# 获取逾期信用贷款_1年以上3年以内 -> getStmNoteBank0013


# 获取逾期信用贷款_3年以上时间序列 -> getStmNoteBank0014Series


# 获取逾期信用贷款_3年以上 -> getStmNoteBank0014


# 获取逾期信用贷款合计时间序列 -> getStmNoteBank0015Series


# 获取逾期信用贷款合计 -> getStmNoteBank0015


# 获取逾期抵押贷款_3个月以内时间序列 -> getStmNoteBank0031Series


# 获取逾期抵押贷款_3个月以内 -> getStmNoteBank0031


# 获取逾期抵押贷款_3个月至1年时间序列 -> getStmNoteBank0032Series


# 获取逾期抵押贷款_3个月至1年 -> getStmNoteBank0032


# 获取逾期抵押贷款_1年以上3年以内时间序列 -> getStmNoteBank0033Series


# 获取逾期抵押贷款_1年以上3年以内 -> getStmNoteBank0033


# 获取逾期抵押贷款_3年以上时间序列 -> getStmNoteBank0034Series


# 获取逾期抵押贷款_3年以上 -> getStmNoteBank0034


# 获取逾期抵押贷款合计时间序列 -> getStmNoteBank0035Series


# 获取逾期抵押贷款合计 -> getStmNoteBank0035


# 获取逾期票据贴现_3个月以内时间序列 -> getStmNoteBank0041Series


# 获取逾期票据贴现_3个月以内 -> getStmNoteBank0041


# 获取逾期票据贴现_3个月至1年时间序列 -> getStmNoteBank0042Series


# 获取逾期票据贴现_3个月至1年 -> getStmNoteBank0042


# 获取逾期票据贴现_1年以上3年以内时间序列 -> getStmNoteBank0043Series


# 获取逾期票据贴现_1年以上3年以内 -> getStmNoteBank0043


# 获取逾期票据贴现_3年以上时间序列 -> getStmNoteBank0044Series


# 获取逾期票据贴现_3年以上 -> getStmNoteBank0044


# 获取逾期票据贴现合计时间序列 -> getStmNoteBank0045Series


# 获取逾期票据贴现合计 -> getStmNoteBank0045


# 获取逾期质押贷款_3个月以内时间序列 -> getStmNoteBank0051Series


# 获取逾期质押贷款_3个月以内 -> getStmNoteBank0051


# 获取逾期质押贷款_3个月至1年时间序列 -> getStmNoteBank0052Series


# 获取逾期质押贷款_3个月至1年 -> getStmNoteBank0052


# 获取逾期质押贷款_1年以上3年以内时间序列 -> getStmNoteBank0053Series


# 获取逾期质押贷款_1年以上3年以内 -> getStmNoteBank0053


# 获取逾期质押贷款_3年以上时间序列 -> getStmNoteBank0054Series


# 获取逾期质押贷款_3年以上 -> getStmNoteBank0054


# 获取逾期质押贷款合计时间序列 -> getStmNoteBank0055Series


# 获取逾期质押贷款合计 -> getStmNoteBank0055


# 获取净资本时间序列 -> getStmNoteSec1Series


# 获取净资本 -> getStmNoteSec1


# 获取净资本比率时间序列 -> getStmNoteSec4Series


# 获取净资本比率 -> getStmNoteSec4


# 获取核心净资本时间序列 -> getStmNoteSec30Series


# 获取核心净资本 -> getStmNoteSec30


# 获取附属净资本时间序列 -> getStmNoteSec31Series


# 获取附属净资本 -> getStmNoteSec31


# 获取自营固定收益类证券/净资本时间序列 -> getStmNoteSec8Series


# 获取自营固定收益类证券/净资本 -> getStmNoteSec8


# 获取自营权益类证券及证券衍生品/净资本时间序列 -> getStmNoteSec7Series


# 获取自营权益类证券及证券衍生品/净资本 -> getStmNoteSec7


# 获取各项风险资本准备之和时间序列 -> getStmNoteSec32Series


# 获取各项风险资本准备之和 -> getStmNoteSec32


# 获取净稳定资金率时间序列 -> getStmNoteSec36Series


# 获取净稳定资金率 -> getStmNoteSec36


# 获取受托资金时间序列 -> getStmNoteSec2Series


# 获取受托资金 -> getStmNoteSec2


# 获取自营股票时间序列 -> getStmNoteSecOp2Series


# 获取自营股票 -> getStmNoteSecOp2


# 获取自营国债时间序列 -> getStmNoteSecOp3Series


# 获取自营国债 -> getStmNoteSecOp3


# 获取自营基金时间序列 -> getStmNoteSecOp4Series


# 获取自营基金 -> getStmNoteSecOp4


# 获取自营证可转债时间序列 -> getStmNoteSecOp5Series


# 获取自营证可转债 -> getStmNoteSecOp5


# 获取自营证券合计时间序列 -> getStmNoteSecOp1Series


# 获取自营证券合计 -> getStmNoteSecOp1


# 获取风险覆盖率时间序列 -> getStmNoteSec5Series


# 获取风险覆盖率 -> getStmNoteSec5


# 获取证券投资业务收入时间序列 -> getStmNoteSec1540Series


# 获取证券投资业务收入 -> getStmNoteSec1540


# 获取证券经纪业务收入时间序列 -> getStmNoteSec1541Series


# 获取证券经纪业务收入 -> getStmNoteSec1541


# 获取投资银行业务收入时间序列 -> getStmNoteSec1542Series


# 获取投资银行业务收入 -> getStmNoteSec1542


# 获取证券投资业务净收入时间序列 -> getStmNoteSec1550Series


# 获取证券投资业务净收入 -> getStmNoteSec1550


# 获取证券经纪业务净收入时间序列 -> getStmNoteSec1551Series


# 获取证券经纪业务净收入 -> getStmNoteSec1551


# 获取投资银行业务净收入时间序列 -> getStmNoteSec1552Series


# 获取投资银行业务净收入 -> getStmNoteSec1552


# 获取评估利率假设:风险贴现率时间序列 -> getStmNoteInSur7Series


# 获取评估利率假设:风险贴现率 -> getStmNoteInSur7


# 获取退保率时间序列 -> getStmNoteInSur8Series


# 获取退保率 -> getStmNoteInSur8


# 获取保单继续率(13个月)时间序列 -> getStmNoteInSur1Series


# 获取保单继续率(13个月) -> getStmNoteInSur1


# 获取保单继续率(14个月)时间序列 -> getStmNoteInSur2Series


# 获取保单继续率(14个月) -> getStmNoteInSur2


# 获取保单继续率(25个月)时间序列 -> getStmNoteInSur3Series


# 获取保单继续率(25个月) -> getStmNoteInSur3


# 获取保单继续率(26个月)时间序列 -> getStmNoteInSur4Series


# 获取保单继续率(26个月) -> getStmNoteInSur4


# 获取偿付能力充足率(产险)时间序列 -> getStmNoteInSur12Series


# 获取偿付能力充足率(产险) -> getStmNoteInSur12


# 获取赔付率(产险)时间序列 -> getStmNoteInSur10Series


# 获取赔付率(产险) -> getStmNoteInSur10


# 获取费用率(产险)时间序列 -> getStmNoteInSur11Series


# 获取费用率(产险) -> getStmNoteInSur11


# 获取实际资本(产险)时间序列 -> getStmNoteInSur13NSeries


# 获取实际资本(产险) -> getStmNoteInSur13N


# 获取实际资本(产险)(旧)时间序列 -> getStmNoteInSur13Series


# 获取实际资本(产险)(旧) -> getStmNoteInSur13


# 获取最低资本(产险)时间序列 -> getStmNoteInSur14NSeries


# 获取最低资本(产险) -> getStmNoteInSur14N


# 获取最低资本(产险)(旧)时间序列 -> getStmNoteInSur14Series


# 获取最低资本(产险)(旧) -> getStmNoteInSur14


# 获取偿付能力充足率(寿险)时间序列 -> getStmNoteInSur15Series


# 获取偿付能力充足率(寿险) -> getStmNoteInSur15


# 获取内含价值(寿险)时间序列 -> getStmNoteInSur16NSeries


# 获取内含价值(寿险) -> getStmNoteInSur16N


# 获取内含价值(寿险)(旧)时间序列 -> getStmNoteInSur16Series


# 获取内含价值(寿险)(旧) -> getStmNoteInSur16


# 获取新业务价值(寿险)时间序列 -> getStmNoteInSur17NSeries


# 获取新业务价值(寿险) -> getStmNoteInSur17N


# 获取新业务价值(寿险)(旧)时间序列 -> getStmNoteInSur17Series


# 获取新业务价值(寿险)(旧) -> getStmNoteInSur17


# 获取有效业务价值(寿险)时间序列 -> getStmNoteInSur18NSeries


# 获取有效业务价值(寿险) -> getStmNoteInSur18N


# 获取有效业务价值(寿险)(旧)时间序列 -> getStmNoteInSur18Series


# 获取有效业务价值(寿险)(旧) -> getStmNoteInSur18


# 获取实际资本(寿险)时间序列 -> getStmNoteInSur19NSeries


# 获取实际资本(寿险) -> getStmNoteInSur19N


# 获取实际资本(寿险)(旧)时间序列 -> getStmNoteInSur19Series


# 获取实际资本(寿险)(旧) -> getStmNoteInSur19


# 获取最低资本(寿险)时间序列 -> getStmNoteInSur20NSeries


# 获取最低资本(寿险) -> getStmNoteInSur20N


# 获取最低资本(寿险)(旧)时间序列 -> getStmNoteInSur20Series


# 获取最低资本(寿险)(旧) -> getStmNoteInSur20


# 获取定期存款(投资)时间序列 -> getStmNoteInSur7801Series


# 获取定期存款(投资) -> getStmNoteInSur7801


# 获取债券投资时间序列 -> getStmNoteInSur7802Series


# 获取债券投资 -> getStmNoteInSur7802


# 获取债券投资成本_FUND时间序列 -> getStmBs8Series


# 获取债券投资成本_FUND -> getStmBs8


# 获取债券投资_FUND时间序列 -> getStmBs7Series


# 获取债券投资_FUND -> getStmBs7


# 获取债券投资公允价值变动收益_FUND时间序列 -> getStmIs102Series


# 获取债券投资公允价值变动收益_FUND -> getStmIs102


# 获取基金投资时间序列 -> getStmNoteInSur7803Series


# 获取基金投资 -> getStmNoteInSur7803


# 获取基金投资_FUND时间序列 -> getStmBs201Series


# 获取基金投资_FUND -> getStmBs201


# 获取基金投资成本_FUND时间序列 -> getStmBs202Series


# 获取基金投资成本_FUND -> getStmBs202


# 获取基金投资公允价值变动收益_FUND时间序列 -> getStmIs104Series


# 获取基金投资公允价值变动收益_FUND -> getStmIs104


# 获取股票投资时间序列 -> getStmNoteInSur7804Series


# 获取股票投资 -> getStmNoteInSur7804


# 获取股票投资成本_FUND时间序列 -> getStmBs5Series


# 获取股票投资成本_FUND -> getStmBs5


# 获取股票投资_FUND时间序列 -> getStmBs4Series


# 获取股票投资_FUND -> getStmBs4


# 获取股票投资公允价值变动收益_FUND时间序列 -> getStmIs101Series


# 获取股票投资公允价值变动收益_FUND -> getStmIs101


# 获取前N大股票占全部股票投资比时间序列 -> getStyleTopNProportionToAllSharesSeries


# 获取前N大股票占全部股票投资比 -> getStyleTopNProportionToAllShares


# 获取股权投资时间序列 -> getStmNoteInSur7805Series


# 获取股权投资 -> getStmNoteInSur7805


# 获取长期股权投资时间序列 -> getLongTermEqYInvestSeries


# 获取长期股权投资 -> getLongTermEqYInvest


# 获取基建投资时间序列 -> getStmNoteInSur7806Series


# 获取基建投资 -> getStmNoteInSur7806


# 获取现金及现金等价物时间序列 -> getStmNoteInSur7807Series


# 获取现金及现金等价物 -> getStmNoteInSur7807


# 获取现金及现金等价物_GSD时间序列 -> getWgsDCCeSeries


# 获取现金及现金等价物_GSD -> getWgsDCCe


# 获取现金及现金等价物期初余额_GSD时间序列 -> getWgsDCashBegBalCfSeries


# 获取现金及现金等价物期初余额_GSD -> getWgsDCashBegBalCf


# 获取现金及现金等价物期末余额_GSD时间序列 -> getWgsDCashEndBalCfSeries


# 获取现金及现金等价物期末余额_GSD -> getWgsDCashEndBalCf


# 获取期初现金及现金等价物余额时间序列 -> getCashCashEquBegPeriodSeries


# 获取期初现金及现金等价物余额 -> getCashCashEquBegPeriod


# 获取期末现金及现金等价物余额时间序列 -> getCashCashEquEndPeriodSeries


# 获取期末现金及现金等价物余额 -> getCashCashEquEndPeriod


# 获取每股现金及现金等价物余额_PIT时间序列 -> getFaCcEpsSeries


# 获取每股现金及现金等价物余额_PIT -> getFaCcEps


# 获取期末现金及现金等价物_PIT时间序列 -> getFaCCeSeries


# 获取期末现金及现金等价物_PIT -> getFaCCe


# 获取单季度.现金及现金等价物期初余额_GSD时间序列 -> getWgsDQfaCashBegBalCfSeries


# 获取单季度.现金及现金等价物期初余额_GSD -> getWgsDQfaCashBegBalCf


# 获取单季度.现金及现金等价物期末余额_GSD时间序列 -> getWgsDQfaCashEndBalCfSeries


# 获取单季度.现金及现金等价物期末余额_GSD -> getWgsDQfaCashEndBalCf


# 获取单季度.期末现金及现金等价物余额时间序列 -> getQfaCashCashEquEndPeriodSeries


# 获取单季度.期末现金及现金等价物余额 -> getQfaCashCashEquEndPeriod


# 获取集团内含价值时间序列 -> getStmNoteInSur30NSeries


# 获取集团内含价值 -> getStmNoteInSur30N


# 获取集团客户数时间序列 -> getStmNoteInSur7810Series


# 获取集团客户数 -> getStmNoteInSur7810


# 获取保险营销员人数时间序列 -> getStmNoteInSur7811Series


# 获取保险营销员人数 -> getStmNoteInSur7811


# 获取保险营销员每月人均首年保险业务收入时间序列 -> getStmNoteInSur7812Series


# 获取保险营销员每月人均首年保险业务收入 -> getStmNoteInSur7812


# 获取保险营销员每月人均寿险新保单件数时间序列 -> getStmNoteInSur7813Series


# 获取保险营销员每月人均寿险新保单件数 -> getStmNoteInSur7813


# 获取证券买卖收益时间序列 -> getStmNoteInvestmentIncome0005Series


# 获取证券买卖收益 -> getStmNoteInvestmentIncome0005


# 获取公允价值变动收益时间序列 -> getStmNoteInvestmentIncome0006Series


# 获取公允价值变动收益 -> getStmNoteInvestmentIncome0006


# 获取公允价值变动收益_FUND时间序列 -> getStmIs24Series


# 获取公允价值变动收益_FUND -> getStmIs24


# 获取权证投资公允价值变动收益_FUND时间序列 -> getStmIs103Series


# 获取权证投资公允价值变动收益_FUND -> getStmIs103


# 获取处置合营企业净收益时间序列 -> getStmNoteInvestmentIncome0008Series


# 获取处置合营企业净收益 -> getStmNoteInvestmentIncome0008


# 获取核心偿付能力溢额时间序列 -> getQStmNoteInSur212505Series


# 获取核心偿付能力溢额 -> getQStmNoteInSur212505


# 获取核心偿付能力充足率时间序列 -> getQStmNoteInSur212506Series


# 获取核心偿付能力充足率 -> getQStmNoteInSur212506


# 获取保险业务收入时间序列 -> getQStmNoteInSur212509Series


# 获取保险业务收入 -> getQStmNoteInSur212509


# 获取实际资本时间序列 -> getQStmNoteInSur212514Series


# 获取实际资本 -> getQStmNoteInSur212514


# 获取核心一级资本时间序列 -> getQStmNoteInSur212515Series


# 获取核心一级资本 -> getQStmNoteInSur212515


# 获取核心二级资本时间序列 -> getQStmNoteInSur212516Series


# 获取核心二级资本 -> getQStmNoteInSur212516


# 获取附属一级资本时间序列 -> getQStmNoteInSur212517Series


# 获取附属一级资本 -> getQStmNoteInSur212517


# 获取附属二级资本时间序列 -> getQStmNoteInSur212518Series


# 获取附属二级资本 -> getQStmNoteInSur212518


# 获取最低资本时间序列 -> getQStmNoteInSur212519Series


# 获取最低资本 -> getQStmNoteInSur212519


# 获取量化风险最低资本时间序列 -> getQStmNoteInSur212520Series


# 获取量化风险最低资本 -> getQStmNoteInSur212520


# 获取控制风险最低资本时间序列 -> getQStmNoteInSur212527Series


# 获取控制风险最低资本 -> getQStmNoteInSur212527


# 获取市场风险最低资本合计时间序列 -> getQStmNoteInSur212523Series


# 获取市场风险最低资本合计 -> getQStmNoteInSur212523


# 获取信用风险最低资本合计时间序列 -> getQStmNoteInSur212524Series


# 获取信用风险最低资本合计 -> getQStmNoteInSur212524


# 获取保险风险最低资本合计时间序列 -> getQStmNoteInSur212546Series


# 获取保险风险最低资本合计 -> getQStmNoteInSur212546


# 获取寿险业务保险风险最低资本合计时间序列 -> getQStmNoteInSur212521Series


# 获取寿险业务保险风险最低资本合计 -> getQStmNoteInSur212521


# 获取非寿险业务保险风险最低资本合计时间序列 -> getQStmNoteInSur212522Series


# 获取非寿险业务保险风险最低资本合计 -> getQStmNoteInSur212522


# 获取附加资本时间序列 -> getQStmNoteInSur212528Series


# 获取附加资本 -> getQStmNoteInSur212528


# 获取风险分散效应的资本要求增加时间序列 -> getQStmNoteInSur212525Series


# 获取风险分散效应的资本要求增加 -> getQStmNoteInSur212525


# 获取风险聚合效应的资本要求减少时间序列 -> getQStmNoteInSur212526Series


# 获取风险聚合效应的资本要求减少 -> getQStmNoteInSur212526


# 获取净现金流时间序列 -> getQStmNoteInSur212530Series


# 获取净现金流 -> getQStmNoteInSur212530


# 获取净现金流:报告日后第1年时间序列 -> getQStmNoteInSur212531Series


# 获取净现金流:报告日后第1年 -> getQStmNoteInSur212531


# 获取净现金流:报告日后第2年时间序列 -> getQStmNoteInSur212532Series


# 获取净现金流:报告日后第2年 -> getQStmNoteInSur212532


# 获取净现金流:报告日后第3年时间序列 -> getQStmNoteInSur212533Series


# 获取净现金流:报告日后第3年 -> getQStmNoteInSur212533


# 获取净现金流:报告日后第1年:未来1季度时间序列 -> getQStmNoteInSur212547Series


# 获取净现金流:报告日后第1年:未来1季度 -> getQStmNoteInSur212547


# 获取净现金流:报告日后第1年:未来2季度时间序列 -> getQStmNoteInSur212548Series


# 获取净现金流:报告日后第1年:未来2季度 -> getQStmNoteInSur212548


# 获取净现金流:报告日后第1年:未来3季度时间序列 -> getQStmNoteInSur212549Series


# 获取净现金流:报告日后第1年:未来3季度 -> getQStmNoteInSur212549


# 获取净现金流:报告日后第1年:未来4季度时间序列 -> getQStmNoteInSur212550Series


# 获取净现金流:报告日后第1年:未来4季度 -> getQStmNoteInSur212550


# 获取市现率PCF(经营性净现金流LYR)时间序列 -> getPcfOcFlyRSeries


# 获取市现率PCF(经营性净现金流LYR) -> getPcfOcFlyR


# 获取受限资金_GSD时间序列 -> getWgsDFundRestrictedSeries


# 获取受限资金_GSD -> getWgsDFundRestricted


# 获取受限资金时间序列 -> getFundRestrictedSeries


# 获取受限资金 -> getFundRestricted


# 获取应收票据时间序列 -> getNotesRcVSeries


# 获取应收票据 -> getNotesRcV


# 获取应收账款及票据_GSD时间序列 -> getWgsDRecEivNetSeries


# 获取应收账款及票据_GSD -> getWgsDRecEivNet


# 获取应收账款时间序列 -> getAccTRcVSeries


# 获取应收账款 -> getAccTRcV


# 获取应收款项融资时间序列 -> getFinancingARSeries


# 获取应收款项融资 -> getFinancingAR


# 获取预付款项时间序列 -> getPrepaySeries


# 获取预付款项 -> getPrepay


# 获取应收股利时间序列 -> getDvdRcVSeries


# 获取应收股利 -> getDvdRcV


# 获取应收股利_FUND时间序列 -> getStmBs11Series


# 获取应收股利_FUND -> getStmBs11


# 获取应收利息时间序列 -> getIntRcVSeries


# 获取应收利息 -> getIntRcV


# 获取应收利息_FUND时间序列 -> getStmBs12Series


# 获取应收利息_FUND -> getStmBs12


# 获取其他应收款时间序列 -> getOThRcVSeries


# 获取其他应收款 -> getOThRcV


# 获取存货_GSD时间序列 -> getWgsDInventoriesSeries


# 获取存货_GSD -> getWgsDInventories


# 获取存货时间序列 -> getInventoriesSeries


# 获取存货 -> getInventories


# 获取存货的减少时间序列 -> getDecrInventoriesSeries


# 获取存货的减少 -> getDecrInventories


# 获取单季度.存货的减少时间序列 -> getQfaDecrInventoriesSeries


# 获取单季度.存货的减少 -> getQfaDecrInventories


# 获取待摊费用时间序列 -> getDeferredExpSeries


# 获取待摊费用 -> getDeferredExp


# 获取待摊费用减少时间序列 -> getDecrDeferredExpSeries


# 获取待摊费用减少 -> getDecrDeferredExp


# 获取长期待摊费用时间序列 -> getLongTermDeferredExpSeries


# 获取长期待摊费用 -> getLongTermDeferredExp


# 获取长期待摊费用摊销时间序列 -> getAMortLtDeferredExpSeries


# 获取长期待摊费用摊销 -> getAMortLtDeferredExp


# 获取单季度.待摊费用减少时间序列 -> getQfaDecrDeferredExpSeries


# 获取单季度.待摊费用减少 -> getQfaDecrDeferredExp


# 获取单季度.长期待摊费用摊销时间序列 -> getQfaAMortLtDeferredExpSeries


# 获取单季度.长期待摊费用摊销 -> getQfaAMortLtDeferredExp


# 获取结算备付金时间序列 -> getSettleRsRvSeries


# 获取结算备付金 -> getSettleRsRv


# 获取结算备付金_FUND时间序列 -> getStmBs2Series


# 获取结算备付金_FUND -> getStmBs2


# 获取拆出资金_GSD时间序列 -> getWgsDLendIbSeries


# 获取拆出资金_GSD -> getWgsDLendIb


# 获取拆出资金时间序列 -> getLoansToOThBanksSeries


# 获取拆出资金 -> getLoansToOThBanks


# 获取融出资金时间序列 -> getMarginAccTSeries


# 获取融出资金 -> getMarginAccT


# 获取融出资金净增加额时间序列 -> getNetInCrLendingFundSeries


# 获取融出资金净增加额 -> getNetInCrLendingFund


# 获取应收保费_GSD时间序列 -> getWgsDRecEivInSurSeries


# 获取应收保费_GSD -> getWgsDRecEivInSur


# 获取应收保费时间序列 -> getPremRcVSeries


# 获取应收保费 -> getPremRcV


# 获取应收分保账款时间序列 -> getRcVFromReInsurerSeries


# 获取应收分保账款 -> getRcVFromReInsurer


# 获取应收分保合同准备金时间序列 -> getRcVFromCededInSurContRsRvSeries


# 获取应收分保合同准备金 -> getRcVFromCededInSurContRsRv


# 获取应收款项合计_GSD时间序列 -> getWgsDRecEivToTSeries


# 获取应收款项合计_GSD -> getWgsDRecEivToT


# 获取应收款项时间序列 -> getToTAccTRcVSeries


# 获取应收款项 -> getToTAccTRcV


# 获取应收款项类投资时间序列 -> getRcVInvestSeries


# 获取应收款项类投资 -> getRcVInvest


# 获取金融投资时间序列 -> getFinInvestSeries


# 获取金融投资 -> getFinInvest


# 获取债权投资时间序列 -> getDebtInvestSeries


# 获取债权投资 -> getDebtInvest


# 获取其他债权投资时间序列 -> getOThDebtInvestSeries


# 获取其他债权投资 -> getOThDebtInvest


# 获取其他权益工具投资时间序列 -> getOThEqYInstrumentsInvestSeries


# 获取其他权益工具投资 -> getOThEqYInstrumentsInvest


# 获取持有至到期投资_GSD时间序列 -> getWgsDInvestHtmSeries


# 获取持有至到期投资_GSD -> getWgsDInvestHtm


# 获取持有至到期投资时间序列 -> getHeldToMTyInvestSeries


# 获取持有至到期投资 -> getHeldToMTyInvest


# 获取长期应收款时间序列 -> getLongTermRecSeries


# 获取长期应收款 -> getLongTermRec


# 获取在建工程(合计)时间序列 -> getConstInProgToTSeries


# 获取在建工程(合计) -> getConstInProgToT


# 获取在建工程时间序列 -> getConstInProgSeries


# 获取在建工程 -> getConstInProg


# 获取工程物资时间序列 -> getProJMAtlSeries


# 获取工程物资 -> getProJMAtl


# 获取开发支出时间序列 -> getRAndDCostsSeries


# 获取开发支出 -> getRAndDCosts


# 获取发放贷款及垫款时间序列 -> getLoansAndAdvGrantedSeries


# 获取发放贷款及垫款 -> getLoansAndAdvGranted


# 获取存放同业和其它金融机构款项时间序列 -> getAssetDepOThBanksFinInStSeries


# 获取存放同业和其它金融机构款项 -> getAssetDepOThBanksFinInSt


# 获取贵金属时间序列 -> getPreciousMetalsSeries


# 获取贵金属 -> getPreciousMetals


# 获取应收分保未到期责任准备金时间序列 -> getRcVCededUnearnedPremRsRvSeries


# 获取应收分保未到期责任准备金 -> getRcVCededUnearnedPremRsRv


# 获取应收分保未决赔款准备金时间序列 -> getRcVCededClaimRsRvSeries


# 获取应收分保未决赔款准备金 -> getRcVCededClaimRsRv


# 获取应收分保寿险责任准备金时间序列 -> getRcVCededLifeInSurRsRvSeries


# 获取应收分保寿险责任准备金 -> getRcVCededLifeInSurRsRv


# 获取应收分保长期健康险责任准备金时间序列 -> getRcVCededLtHealthInSurRsRvSeries


# 获取应收分保长期健康险责任准备金 -> getRcVCededLtHealthInSurRsRv


# 获取保户质押贷款时间序列 -> getInsuredPledgeLoanSeries


# 获取保户质押贷款 -> getInsuredPledgeLoan


# 获取存出资本保证金时间序列 -> getCapMrgnPaidSeries


# 获取存出资本保证金 -> getCapMrgnPaid


# 获取定期存款时间序列 -> getTimeDepositsSeries


# 获取定期存款 -> getTimeDeposits


# 获取应收代位追偿款时间序列 -> getSubRRecSeries


# 获取应收代位追偿款 -> getSubRRec


# 获取存出保证金时间序列 -> getMrgnPaidSeries


# 获取存出保证金 -> getMrgnPaid


# 获取存出保证金_FUND时间序列 -> getStmBs3Series


# 获取存出保证金_FUND -> getStmBs3


# 获取交易席位费时间序列 -> getSeatFeesExchangeSeries


# 获取交易席位费 -> getSeatFeesExchange


# 获取客户资金存款时间序列 -> getClientsCapDepositSeries


# 获取客户资金存款 -> getClientsCapDeposit


# 获取客户备付金时间序列 -> getClientsRsRvSettleSeries


# 获取客户备付金 -> getClientsRsRvSettle


# 获取应付票据时间序列 -> getNotesPayableSeries


# 获取应付票据 -> getNotesPayable


# 获取应付账款及票据_GSD时间序列 -> getWgsDPayAccTSeries


# 获取应付账款及票据_GSD -> getWgsDPayAccT


# 获取应付账款时间序列 -> getAccTPayableSeries


# 获取应付账款 -> getAccTPayable


# 获取预收账款时间序列 -> getAdvFromCuStSeries


# 获取预收账款 -> getAdvFromCuSt


# 获取应付款项时间序列 -> getToTAccTPayableSeries


# 获取应付款项 -> getToTAccTPayable


# 获取应付利息时间序列 -> getIntPayableSeries


# 获取应付利息 -> getIntPayable


# 获取应付利息_FUND时间序列 -> getStmBs29Series


# 获取应付利息_FUND -> getStmBs29


# 获取应付股利时间序列 -> getDvdPayableSeries


# 获取应付股利 -> getDvdPayable


# 获取其他应付款时间序列 -> getOThPayableSeries


# 获取其他应付款 -> getOThPayable


# 获取预提费用时间序列 -> getAccExpSeries


# 获取预提费用 -> getAccExp


# 获取预提费用增加时间序列 -> getInCrAccExpSeries


# 获取预提费用增加 -> getInCrAccExp


# 获取单季度.预提费用增加时间序列 -> getQfaInCrAccExpSeries


# 获取单季度.预提费用增加 -> getQfaInCrAccExp


# 获取应付短期债券时间序列 -> getStBondsPayableSeries


# 获取应付短期债券 -> getStBondsPayable


# 获取吸收存款及同业存放时间序列 -> getDepositReceivedIbDepositsSeries


# 获取吸收存款及同业存放 -> getDepositReceivedIbDeposits


# 获取拆入资金_GSD时间序列 -> getWgsDBorrowIbSeries


# 获取拆入资金_GSD -> getWgsDBorrowIb


# 获取拆入资金时间序列 -> getLoansOThBanksSeries


# 获取拆入资金 -> getLoansOThBanks


# 获取拆入资金净增加额时间序列 -> getNetInCrLoansOtherBankSeries


# 获取拆入资金净增加额 -> getNetInCrLoansOtherBank


# 获取单季度.拆入资金净增加额时间序列 -> getQfaNetInCrLoansOtherBankSeries


# 获取单季度.拆入资金净增加额 -> getQfaNetInCrLoansOtherBank


# 获取向其他金融机构拆入资金净增加额时间序列 -> getNetInCrFundBOrrOfISeries


# 获取向其他金融机构拆入资金净增加额 -> getNetInCrFundBOrrOfI


# 获取单季度.向其他金融机构拆入资金净增加额时间序列 -> getQfaNetInCrFundBOrrOfISeries


# 获取单季度.向其他金融机构拆入资金净增加额 -> getQfaNetInCrFundBOrrOfI


# 获取应付手续费及佣金时间序列 -> getHandlingChargesComMPayableSeries


# 获取应付手续费及佣金 -> getHandlingChargesComMPayable


# 获取应付分保账款时间序列 -> getPayableToReInsurerSeries


# 获取应付分保账款 -> getPayableToReInsurer


# 获取保险合同准备金时间序列 -> getRsRvInSurContSeries


# 获取保险合同准备金 -> getRsRvInSurCont


# 获取代理买卖证券款时间序列 -> getActingTradingSecSeries


# 获取代理买卖证券款 -> getActingTradingSec


# 获取代理承销证券款时间序列 -> getActingUwSecSeries


# 获取代理承销证券款 -> getActingUwSec


# 获取应付债券时间序列 -> getBondsPayableSeries


# 获取应付债券 -> getBondsPayable


# 获取长期应付款(合计)时间序列 -> getLtPayableToTSeries


# 获取长期应付款(合计) -> getLtPayableToT


# 获取长期应付款时间序列 -> getLtPayableSeries


# 获取长期应付款 -> getLtPayable


# 获取专项应付款时间序列 -> getSpecificItemPayableSeries


# 获取专项应付款 -> getSpecificItemPayable


# 获取同业和其它金融机构存放款项时间序列 -> getLiaBDepOThBanksFinInStSeries


# 获取同业和其它金融机构存放款项 -> getLiaBDepOThBanksFinInSt


# 获取吸收存款时间序列 -> getCuStBankDepSeries


# 获取吸收存款 -> getCuStBankDep


# 获取应付赔付款时间序列 -> getClaimsPayableSeries


# 获取应付赔付款 -> getClaimsPayable


# 获取应付保单红利时间序列 -> getDvdPayableInsuredSeries


# 获取应付保单红利 -> getDvdPayableInsured


# 获取存入保证金时间序列 -> getDepositReceivedSeries


# 获取存入保证金 -> getDepositReceived


# 获取保户储金及投资款时间序列 -> getInsuredDepositInvestSeries


# 获取保户储金及投资款 -> getInsuredDepositInvest


# 获取未到期责任准备金变动_GSD时间序列 -> getWgsDChgRsvUnearnedPremiumSeries


# 获取未到期责任准备金变动_GSD -> getWgsDChgRsvUnearnedPremium


# 获取未到期责任准备金时间序列 -> getUnearnedPremRsRvSeries


# 获取未到期责任准备金 -> getUnearnedPremRsRv


# 获取单季度.未到期责任准备金变动_GSD时间序列 -> getWgsDQfaChgRsvUnearnedPremiumSeries


# 获取单季度.未到期责任准备金变动_GSD -> getWgsDQfaChgRsvUnearnedPremium


# 获取未决赔款准备金变动_GSD时间序列 -> getWgsDChgRsvOutstandingLossSeries


# 获取未决赔款准备金变动_GSD -> getWgsDChgRsvOutstandingLoss


# 获取未决赔款准备金时间序列 -> getOutLossRsRvSeries


# 获取未决赔款准备金 -> getOutLossRsRv


# 获取单季度.未决赔款准备金变动_GSD时间序列 -> getWgsDQfaChgRsvOutstandingLossSeries


# 获取单季度.未决赔款准备金变动_GSD -> getWgsDQfaChgRsvOutstandingLoss


# 获取寿险责任准备金时间序列 -> getLifeInSurRsRvSeries


# 获取寿险责任准备金 -> getLifeInSurRsRv


# 获取长期健康险责任准备金时间序列 -> getLtHealthInSurVSeries


# 获取长期健康险责任准备金 -> getLtHealthInSurV


# 获取预收保费时间序列 -> getPremReceivedAdvSeries


# 获取预收保费 -> getPremReceivedAdv


# 获取应付短期融资款时间序列 -> getStFinLInStPayableSeries


# 获取应付短期融资款 -> getStFinLInStPayable


# 获取其他权益工具时间序列 -> getOtherEquityInstrumentsSeries


# 获取其他权益工具 -> getOtherEquityInstruments


# 获取其他权益工具:永续债时间序列 -> getPerpetualDebtSeries


# 获取其他权益工具:永续债 -> getPerpetualDebt


# 获取库存股_GSD时间序列 -> getWgsDTreAsStKSeries


# 获取库存股_GSD -> getWgsDTreAsStK


# 获取库存股时间序列 -> getTSyStKSeries


# 获取库存股 -> getTSyStK


# 获取专项储备时间序列 -> getSpecialRsRvSeries


# 获取专项储备 -> getSpecialRsRv


# 获取一般风险准备时间序列 -> getProvNomRisksSeries


# 获取一般风险准备 -> getProvNomRisks


# 获取外币报表折算差额时间序列 -> getCnVdDiffForeignCurRStatSeries


# 获取外币报表折算差额 -> getCnVdDiffForeignCurRStat


# 获取股东权益差额(特殊报表科目)时间序列 -> getSHrhLDrEqYGapSeries


# 获取股东权益差额(特殊报表科目) -> getSHrhLDrEqYGap


# 获取其他股东权益差额说明(特殊报表科目)时间序列 -> getSHrhLDrEqYGapDetailSeries


# 获取其他股东权益差额说明(特殊报表科目) -> getSHrhLDrEqYGapDetail


# 获取股东权益差额(合计平衡项目)时间序列 -> getSHrhLDrEqYNettingSeries


# 获取股东权益差额(合计平衡项目) -> getSHrhLDrEqYNetting


# 获取归属母公司股东的权益/投入资本_GSD时间序列 -> getWgsDEquityToTotalCapitalSeries


# 获取归属母公司股东的权益/投入资本_GSD -> getWgsDEquityToTotalCapital


# 获取归属母公司股东的权益时间序列 -> getEqYBelongToParComShSeries


# 获取归属母公司股东的权益 -> getEqYBelongToParComSh


# 获取归属母公司股东的权益(MRQ,只有最新数据)时间序列 -> getEquityMrQSeries


# 获取归属母公司股东的权益(MRQ,只有最新数据) -> getEquityMrQ


# 获取少数股东权益_GSD时间序列 -> getWgsDMinIntSeries


# 获取少数股东权益_GSD -> getWgsDMinInt


# 获取少数股东权益时间序列 -> getMinorityIntSeries


# 获取少数股东权益 -> getMinorityInt


# 获取收到的税费返还时间序列 -> getRecpTaxRendsSeries


# 获取收到的税费返还 -> getRecpTaxRends


# 获取单季度.收到的税费返还时间序列 -> getQfaRecpTaxRendsSeries


# 获取单季度.收到的税费返还 -> getQfaRecpTaxRends


# 获取收到其他与经营活动有关的现金时间序列 -> getOtherCashRecpRalOperActSeries


# 获取收到其他与经营活动有关的现金 -> getOtherCashRecpRalOperAct


# 获取单季度.收到其他与经营活动有关的现金时间序列 -> getQfaOtherCashRecpRalOperActSeries


# 获取单季度.收到其他与经营活动有关的现金 -> getQfaOtherCashRecpRalOperAct


# 获取保户储金净增加额时间序列 -> getNetInCrInsuredDepSeries


# 获取保户储金净增加额 -> getNetInCrInsuredDep


# 获取单季度.保户储金净增加额时间序列 -> getQfaNetInCrInsuredDepSeries


# 获取单季度.保户储金净增加额 -> getQfaNetInCrInsuredDep


# 获取客户存款和同业存放款项净增加额时间序列 -> getNetInCrDepCobSeries


# 获取客户存款和同业存放款项净增加额 -> getNetInCrDepCob


# 获取单季度.客户存款和同业存放款项净增加额时间序列 -> getQfaNetInCrDepCobSeries


# 获取单季度.客户存款和同业存放款项净增加额 -> getQfaNetInCrDepCob


# 获取收取利息和手续费净增加额时间序列 -> getNetInCrIntHandlingChrGSeries


# 获取收取利息和手续费净增加额 -> getNetInCrIntHandlingChrG


# 获取单季度.收取利息和手续费净增加额时间序列 -> getQfaNetInCrIntHandlingChrGSeries


# 获取单季度.收取利息和手续费净增加额 -> getQfaNetInCrIntHandlingChrG


# 获取收到原保险合同保费取得的现金时间序列 -> getCashRecpPremOrigInCoSeries


# 获取收到原保险合同保费取得的现金 -> getCashRecpPremOrigInCo


# 获取单季度.收到原保险合同保费取得的现金时间序列 -> getQfaCashRecpPremOrigInCoSeries


# 获取单季度.收到原保险合同保费取得的现金 -> getQfaCashRecpPremOrigInCo


# 获取收到再保业务现金净额时间序列 -> getNetCashReceivedReinsUBusSeries


# 获取收到再保业务现金净额 -> getNetCashReceivedReinsUBus


# 获取单季度.收到再保业务现金净额时间序列 -> getQfaNetCashReceivedReinsUBusSeries


# 获取单季度.收到再保业务现金净额 -> getQfaNetCashReceivedReinsUBus


# 获取回购业务资金净增加额时间序列 -> getNetInCrRepUrchBusFundSeries


# 获取回购业务资金净增加额 -> getNetInCrRepUrchBusFund


# 获取单季度.回购业务资金净增加额时间序列 -> getQfaNetInCrRepUrchBusFundSeries


# 获取单季度.回购业务资金净增加额 -> getQfaNetInCrRepUrchBusFund


# 获取代理买卖证券收到的现金净额时间序列 -> getNetCashFromSeUriTiesSeries


# 获取代理买卖证券收到的现金净额 -> getNetCashFromSeUriTies


# 获取经营活动现金流入差额(特殊报表科目)时间序列 -> getCashInFlowsOperActGapSeries


# 获取经营活动现金流入差额(特殊报表科目) -> getCashInFlowsOperActGap


# 获取经营活动现金流入差额说明(特殊报表科目)时间序列 -> getCashInFlowsOperActGapDetailSeries


# 获取经营活动现金流入差额说明(特殊报表科目) -> getCashInFlowsOperActGapDetail


# 获取经营活动现金流入差额(合计平衡项目)时间序列 -> getCashInFlowsOperActNettingSeries


# 获取经营活动现金流入差额(合计平衡项目) -> getCashInFlowsOperActNetting


# 获取以公允价值计量且其变动计入当期损益的金融工具净额时间序列 -> getNetFinaInstrumentsMeasuredAtFmVSeries


# 获取以公允价值计量且其变动计入当期损益的金融工具净额 -> getNetFinaInstrumentsMeasuredAtFmV


# 获取支付给职工以及为职工支付的现金时间序列 -> getCashPayBehEMplSeries


# 获取支付给职工以及为职工支付的现金 -> getCashPayBehEMpl


# 获取单季度.支付给职工以及为职工支付的现金时间序列 -> getQfaCashPayBehEMplSeries


# 获取单季度.支付给职工以及为职工支付的现金 -> getQfaCashPayBehEMpl


# 获取客户贷款及垫款净增加额时间序列 -> getNetInCrClientsLoanAdvSeries


# 获取客户贷款及垫款净增加额 -> getNetInCrClientsLoanAdv


# 获取单季度.客户贷款及垫款净增加额时间序列 -> getQfaNetInCrClientsLoanAdvSeries


# 获取单季度.客户贷款及垫款净增加额 -> getQfaNetInCrClientsLoanAdv


# 获取存放央行和同业款项净增加额时间序列 -> getNetInCrDepCBobSeries


# 获取存放央行和同业款项净增加额 -> getNetInCrDepCBob


# 获取单季度.存放央行和同业款项净增加额时间序列 -> getQfaNetInCrDepCBobSeries


# 获取单季度.存放央行和同业款项净增加额 -> getQfaNetInCrDepCBob


# 获取支付原保险合同赔付款项的现金时间序列 -> getCashPayClaimsOrigInCoSeries


# 获取支付原保险合同赔付款项的现金 -> getCashPayClaimsOrigInCo


# 获取单季度.支付原保险合同赔付款项的现金时间序列 -> getQfaCashPayClaimsOrigInCoSeries


# 获取单季度.支付原保险合同赔付款项的现金 -> getQfaCashPayClaimsOrigInCo


# 获取支付手续费的现金时间序列 -> getHandlingChrGPaidSeries


# 获取支付手续费的现金 -> getHandlingChrGPaid


# 获取单季度.支付手续费的现金时间序列 -> getQfaHandlingChrGPaidSeries


# 获取单季度.支付手续费的现金 -> getQfaHandlingChrGPaid


# 获取支付保单红利的现金时间序列 -> getComMInSurPlcYPaidSeries


# 获取支付保单红利的现金 -> getComMInSurPlcYPaid


# 获取单季度.支付保单红利的现金时间序列 -> getQfaComMInSurPlcYPaidSeries


# 获取单季度.支付保单红利的现金 -> getQfaComMInSurPlcYPaid


# 获取经营活动现金流出差额(特殊报表科目)时间序列 -> getCashOutFlowsOperActGapSeries


# 获取经营活动现金流出差额(特殊报表科目) -> getCashOutFlowsOperActGap


# 获取经营活动现金流出差额说明(特殊报表科目)时间序列 -> getCashOutFlowsOperActGapDetailSeries


# 获取经营活动现金流出差额说明(特殊报表科目) -> getCashOutFlowsOperActGapDetail


# 获取经营活动现金流出差额(合计平衡项目)时间序列 -> getCashOutFlowsOperActNettingSeries


# 获取经营活动现金流出差额(合计平衡项目) -> getCashOutFlowsOperActNetting


# 获取收回投资收到的现金时间序列 -> getCashRecpDispWithDrWLInvestSeries


# 获取收回投资收到的现金 -> getCashRecpDispWithDrWLInvest


# 获取单季度.收回投资收到的现金时间序列 -> getQfaCashRecpDispWithDrWLInvestSeries


# 获取单季度.收回投资收到的现金 -> getQfaCashRecpDispWithDrWLInvest


# 获取处置子公司及其他营业单位收到的现金净额时间序列 -> getNetCashRecpDispSoBuSeries


# 获取处置子公司及其他营业单位收到的现金净额 -> getNetCashRecpDispSoBu


# 获取单季度.处置子公司及其他营业单位收到的现金净额时间序列 -> getQfaNetCashRecpDispSoBuSeries


# 获取单季度.处置子公司及其他营业单位收到的现金净额 -> getQfaNetCashRecpDispSoBu


# 获取收到其他与投资活动有关的现金时间序列 -> getOtherCashRecpRalInvActSeries


# 获取收到其他与投资活动有关的现金 -> getOtherCashRecpRalInvAct


# 获取单季度.收到其他与投资活动有关的现金时间序列 -> getQfaOtherCashRecpRalInvActSeries


# 获取单季度.收到其他与投资活动有关的现金 -> getQfaOtherCashRecpRalInvAct


# 获取投资活动现金流入差额(特殊报表科目)时间序列 -> getCashInFlowsInvActGapSeries


# 获取投资活动现金流入差额(特殊报表科目) -> getCashInFlowsInvActGap


# 获取投资活动现金流入差额说明(特殊报表科目)时间序列 -> getCashInFlowsInvActGapDetailSeries


# 获取投资活动现金流入差额说明(特殊报表科目) -> getCashInFlowsInvActGapDetail


# 获取投资活动现金流入差额(合计平衡项目)时间序列 -> getCashInFlowsInvActNettingSeries


# 获取投资活动现金流入差额(合计平衡项目) -> getCashInFlowsInvActNetting


# 获取投资支付的现金时间序列 -> getCashPaidInvestSeries


# 获取投资支付的现金 -> getCashPaidInvest


# 获取单季度.投资支付的现金时间序列 -> getQfaCashPaidInvestSeries


# 获取单季度.投资支付的现金 -> getQfaCashPaidInvest


# 获取质押贷款净增加额时间序列 -> getNetInCrPledgeLoanSeries


# 获取质押贷款净增加额 -> getNetInCrPledgeLoan


# 获取单季度.质押贷款净增加额时间序列 -> getQfaNetInCrPledgeLoanSeries


# 获取单季度.质押贷款净增加额 -> getQfaNetInCrPledgeLoan


# 获取取得子公司及其他营业单位支付的现金净额时间序列 -> getNetCashPayAQuisSoBuSeries


# 获取取得子公司及其他营业单位支付的现金净额 -> getNetCashPayAQuisSoBu


# 获取单季度.取得子公司及其他营业单位支付的现金净额时间序列 -> getQfaNetCashPayAQuisSoBuSeries


# 获取单季度.取得子公司及其他营业单位支付的现金净额 -> getQfaNetCashPayAQuisSoBu


# 获取支付其他与投资活动有关的现金时间序列 -> getOtherCashPayRalInvActSeries


# 获取支付其他与投资活动有关的现金 -> getOtherCashPayRalInvAct


# 获取单季度.支付其他与投资活动有关的现金时间序列 -> getQfaOtherCashPayRalInvActSeries


# 获取单季度.支付其他与投资活动有关的现金 -> getQfaOtherCashPayRalInvAct


# 获取投资活动现金流出差额(特殊报表科目)时间序列 -> getCashOutFlowsInvActGapSeries


# 获取投资活动现金流出差额(特殊报表科目) -> getCashOutFlowsInvActGap


# 获取投资活动现金流出差额说明(特殊报表科目)时间序列 -> getCashOutFlowsInvActGapDetailSeries


# 获取投资活动现金流出差额说明(特殊报表科目) -> getCashOutFlowsInvActGapDetail


# 获取投资活动现金流出差额(合计平衡项目)时间序列 -> getCashOutFlowsInvActNettingSeries


# 获取投资活动现金流出差额(合计平衡项目) -> getCashOutFlowsInvActNetting


# 获取吸收投资收到的现金时间序列 -> getCashRecpCapContribSeries


# 获取吸收投资收到的现金 -> getCashRecpCapContrib


# 获取单季度.吸收投资收到的现金时间序列 -> getQfaCashRecpCapContribSeries


# 获取单季度.吸收投资收到的现金 -> getQfaCashRecpCapContrib


# 获取子公司吸收少数股东投资收到的现金时间序列 -> getCashRecSAimsSeries


# 获取子公司吸收少数股东投资收到的现金 -> getCashRecSAims


# 获取单季度.子公司吸收少数股东投资收到的现金时间序列 -> getQfaCashRecSAimsSeries


# 获取单季度.子公司吸收少数股东投资收到的现金 -> getQfaCashRecSAims


# 获取收到其他与筹资活动有关的现金时间序列 -> getOtherCashRecpRalFncActSeries


# 获取收到其他与筹资活动有关的现金 -> getOtherCashRecpRalFncAct


# 获取单季度.收到其他与筹资活动有关的现金时间序列 -> getQfaOtherCashRecpRalFncActSeries


# 获取单季度.收到其他与筹资活动有关的现金 -> getQfaOtherCashRecpRalFncAct


# 获取发行债券收到的现金时间序列 -> getProcIssueBondsSeries


# 获取发行债券收到的现金 -> getProcIssueBonds


# 获取单季度.发行债券收到的现金时间序列 -> getQfaProcIssueBondsSeries


# 获取单季度.发行债券收到的现金 -> getQfaProcIssueBonds


# 获取筹资活动现金流入差额(特殊报表科目)时间序列 -> getCashInFlowsFncActGapSeries


# 获取筹资活动现金流入差额(特殊报表科目) -> getCashInFlowsFncActGap


# 获取筹资活动现金流入差额说明(特殊报表科目)时间序列 -> getCashInFlowsFncActGapDetailSeries


# 获取筹资活动现金流入差额说明(特殊报表科目) -> getCashInFlowsFncActGapDetail


# 获取筹资活动现金流入差额(合计平衡项目)时间序列 -> getCashInFlowsFncActNettingSeries


# 获取筹资活动现金流入差额(合计平衡项目) -> getCashInFlowsFncActNetting


# 获取偿还债务支付的现金时间序列 -> getCashPrepayAmtBOrrSeries


# 获取偿还债务支付的现金 -> getCashPrepayAmtBOrr


# 获取单季度.偿还债务支付的现金时间序列 -> getQfaCashPrepayAmtBOrrSeries


# 获取单季度.偿还债务支付的现金 -> getQfaCashPrepayAmtBOrr


# 获取分配股利、利润或偿付利息支付的现金时间序列 -> getCashPayDistDpcpIntExpSeries


# 获取分配股利、利润或偿付利息支付的现金 -> getCashPayDistDpcpIntExp


# 获取单季度.分配股利、利润或偿付利息支付的现金时间序列 -> getQfaCashPayDistDpcpIntExpSeries


# 获取单季度.分配股利、利润或偿付利息支付的现金 -> getQfaCashPayDistDpcpIntExp


# 获取子公司支付给少数股东的股利、利润时间序列 -> getDvdProfitPaidScMsSeries


# 获取子公司支付给少数股东的股利、利润 -> getDvdProfitPaidScMs


# 获取单季度.子公司支付给少数股东的股利、利润时间序列 -> getQfaDvdProfitPaidScMsSeries


# 获取单季度.子公司支付给少数股东的股利、利润 -> getQfaDvdProfitPaidScMs


# 获取支付其他与筹资活动有关的现金时间序列 -> getOtherCashPayRalFncActSeries


# 获取支付其他与筹资活动有关的现金 -> getOtherCashPayRalFncAct


# 获取单季度.支付其他与筹资活动有关的现金时间序列 -> getQfaOtherCashPayRalFncActSeries


# 获取单季度.支付其他与筹资活动有关的现金 -> getQfaOtherCashPayRalFncAct


# 获取筹资活动现金流出差额(特殊报表科目)时间序列 -> getCashOutFlowsFncActGapSeries


# 获取筹资活动现金流出差额(特殊报表科目) -> getCashOutFlowsFncActGap


# 获取筹资活动现金流出差额说明(特殊报表科目)时间序列 -> getCashOutFlowsFncActGapDetailSeries


# 获取筹资活动现金流出差额说明(特殊报表科目) -> getCashOutFlowsFncActGapDetail


# 获取筹资活动现金流出差额(合计平衡项目)时间序列 -> getCashOutFlowsFncActNettingSeries


# 获取筹资活动现金流出差额(合计平衡项目) -> getCashOutFlowsFncActNetting


# 获取汇率变动对现金的影响时间序列 -> getEffFxFluCashSeries


# 获取汇率变动对现金的影响 -> getEffFxFluCash


# 获取单季度.汇率变动对现金的影响时间序列 -> getQfaEffFxFluCashSeries


# 获取单季度.汇率变动对现金的影响 -> getQfaEffFxFluCash


# 获取公允价值变动损失时间序列 -> getLossFvChgSeries


# 获取公允价值变动损失 -> getLossFvChg


# 获取单季度.公允价值变动损失时间序列 -> getQfaLossFvChgSeries


# 获取单季度.公允价值变动损失 -> getQfaLossFvChg


# 获取投资损失时间序列 -> getInvestLossSeries


# 获取投资损失 -> getInvestLoss


# 获取单季度.投资损失时间序列 -> getQfaInvestLossSeries


# 获取单季度.投资损失 -> getQfaInvestLoss


# 获取经营性应收项目的减少时间序列 -> getDecrOperPayableSeries


# 获取经营性应收项目的减少 -> getDecrOperPayable


# 获取单季度.经营性应收项目的减少时间序列 -> getQfaDecrOperPayableSeries


# 获取单季度.经营性应收项目的减少 -> getQfaDecrOperPayable


# 获取经营性应付项目的增加时间序列 -> getInCrOperPayableSeries


# 获取经营性应付项目的增加 -> getInCrOperPayable


# 获取单季度.经营性应付项目的增加时间序列 -> getQfaInCrOperPayableSeries


# 获取单季度.经营性应付项目的增加 -> getQfaInCrOperPayable


# 获取其他短期投资_GSD时间序列 -> getWgsDInvestStOThSeries


# 获取其他短期投资_GSD -> getWgsDInvestStOTh


# 获取其他长期投资_GSD时间序列 -> getWgsDInvestLtOThSeries


# 获取其他长期投资_GSD -> getWgsDInvestLtOTh


# 获取其他投资_GSD时间序列 -> getWgsDInvestOThSeries


# 获取其他投资_GSD -> getWgsDInvestOTh


# 获取其他储备_GSD时间序列 -> getWgsDRsvOtherSeries


# 获取其他储备_GSD -> getWgsDRsvOther


# 获取其他营业费用合计_GSD时间序列 -> getWgsDToTExpOThSeries


# 获取其他营业费用合计_GSD -> getWgsDToTExpOTh


# 获取其他非经营性损益_GSD时间序列 -> getWgsDNoOperIncSeries


# 获取其他非经营性损益_GSD -> getWgsDNoOperInc


# 获取其他特殊项_GSD时间序列 -> getWgsDExoDSeries


# 获取其他特殊项_GSD -> getWgsDExoD


# 获取其他非现金调整_GSD时间序列 -> getWgsDNonCashChgSeries


# 获取其他非现金调整_GSD -> getWgsDNonCashChg


# 获取其他时间序列 -> getOthersSeries


# 获取其他 -> getOthers


# 获取其他收入_FUND时间序列 -> getStmIs9Series


# 获取其他收入_FUND -> getStmIs9


# 获取其他费用_FUND时间序列 -> getStmIs37Series


# 获取其他费用_FUND -> getStmIs37


# 获取单季度.其他特殊项_GSD时间序列 -> getWgsDQfaExoDSeries


# 获取单季度.其他特殊项_GSD -> getWgsDQfaExoD


# 获取单季度.其他营业费用合计_GSD时间序列 -> getWgsDQfaToTExpOThSeries


# 获取单季度.其他营业费用合计_GSD -> getWgsDQfaToTExpOTh


# 获取单季度.其他非经营性损益_GSD时间序列 -> getWgsDQfaNoOperIncSeries


# 获取单季度.其他非经营性损益_GSD -> getWgsDQfaNoOperInc


# 获取单季度.其他非现金调整_GSD时间序列 -> getWgsDQfaNonCashChgSeries


# 获取单季度.其他非现金调整_GSD -> getWgsDQfaNonCashChg


# 获取单季度.其他时间序列 -> getQfaOthersSeries


# 获取单季度.其他 -> getQfaOthers


# 获取债务转为资本时间序列 -> getConVDebtIntoCapSeries


# 获取债务转为资本 -> getConVDebtIntoCap


# 获取单季度.债务转为资本时间序列 -> getQfaConVDebtIntoCapSeries


# 获取单季度.债务转为资本 -> getQfaConVDebtIntoCap


# 获取一年内到期的可转换公司债券时间序列 -> getConVCorpBondsDueWithin1YSeries


# 获取一年内到期的可转换公司债券 -> getConVCorpBondsDueWithin1Y


# 获取单季度.一年内到期的可转换公司债券时间序列 -> getQfaConVCorpBondsDueWithin1YSeries


# 获取单季度.一年内到期的可转换公司债券 -> getQfaConVCorpBondsDueWithin1Y


# 获取现金的期末余额时间序列 -> getEndBalCashSeries


# 获取现金的期末余额 -> getEndBalCash


# 获取单季度.现金的期末余额时间序列 -> getQfaEndBalCashSeries


# 获取单季度.现金的期末余额 -> getQfaEndBalCash


# 获取现金的期初余额时间序列 -> getBegBalCashSeries


# 获取现金的期初余额 -> getBegBalCash


# 获取现金等价物的期末余额时间序列 -> getEndBalCashEquSeries


# 获取现金等价物的期末余额 -> getEndBalCashEqu


# 获取单季度.现金等价物的期末余额时间序列 -> getQfaEndBalCashEquSeries


# 获取单季度.现金等价物的期末余额 -> getQfaEndBalCashEqu


# 获取现金等价物的期初余额时间序列 -> getBegBalCashEquSeries


# 获取现金等价物的期初余额 -> getBegBalCashEqu


# 获取间接法-现金净增加额差额(特殊报表科目)时间序列 -> getImNetInCrCashCashEquGapSeries


# 获取间接法-现金净增加额差额(特殊报表科目) -> getImNetInCrCashCashEquGap


# 获取间接法-现金净增加额差额说明(特殊报表科目)时间序列 -> getImNetInCrCashCashEquGapDetailSeries


# 获取间接法-现金净增加额差额说明(特殊报表科目) -> getImNetInCrCashCashEquGapDetail


# 获取间接法-现金净增加额差额(合计平衡项目)时间序列 -> getImNetInCrCashCashEquNettingSeries


# 获取间接法-现金净增加额差额(合计平衡项目) -> getImNetInCrCashCashEquNetting


# 获取网下QFII投资账户配售数量时间序列 -> getFundReItSqFsSeries


# 获取网下QFII投资账户配售数量 -> getFundReItSqFs


# 获取网下QFII投资账户配售金额时间序列 -> getFundReItSqFmSeries


# 获取网下QFII投资账户配售金额 -> getFundReItSqFm


# 获取网下QFII投资账户配售份额占比时间序列 -> getFundReItSqFrSeries


# 获取网下QFII投资账户配售份额占比 -> getFundReItSqFr


# 获取Delta时间序列 -> getDeltaSeries


# 获取Delta -> getDelta


# 获取Delta(交易所)时间序列 -> getDeltaExChSeries


# 获取Delta(交易所) -> getDeltaExCh


# 获取Gamma时间序列 -> getGammaSeries


# 获取Gamma -> getGamma


# 获取Gamma(交易所)时间序列 -> getGammaExChSeries


# 获取Gamma(交易所) -> getGammaExCh


# 获取Vega时间序列 -> getVegaSeries


# 获取Vega -> getVega


# 获取Vega(交易所)时间序列 -> getVegaExChSeries


# 获取Vega(交易所) -> getVegaExCh


# 获取Theta时间序列 -> getThetaSeries


# 获取Theta -> getTheta


# 获取Theta(交易所)时间序列 -> getThetaExChSeries


# 获取Theta(交易所) -> getThetaExCh


# 获取Rho时间序列 -> getRhoSeries


# 获取Rho -> getRho


# 获取Rho(交易所)时间序列 -> getRhoExChSeries


# 获取Rho(交易所) -> getRhoExCh


# 获取IOPV时间序列 -> getIoPvSeries


# 获取IOPV -> getIoPv


# 获取IOPV溢折率时间序列 -> getNavIoPvDiscountRatioSeries


# 获取IOPV溢折率 -> getNavIoPvDiscountRatio


# 获取Alpha时间序列 -> getAlpha2Series


# 获取Alpha -> getAlpha2


# 获取Alpha_FUND时间序列 -> getRiskAlphaSeries


# 获取Alpha_FUND -> getRiskAlpha


# 获取Alpha(年化)时间序列 -> getRiskAnnualPhaSeries


# 获取Alpha(年化) -> getRiskAnnualPha


# 获取Alpha同类平均时间序列 -> getRiskSimLAvgAlphaSeries


# 获取Alpha同类平均 -> getRiskSimLAvgAlpha


# 获取Alpha(年化)同类平均时间序列 -> getRiskSimLAvgAnnualPhaSeries


# 获取Alpha(年化)同类平均 -> getRiskSimLAvgAnnualPha


# 获取BETA值(最近100周)时间序列 -> getBeta100WSeries


# 获取BETA值(最近100周) -> getBeta100W


# 获取BETA值(最近24个月)时间序列 -> getBeta24MSeries


# 获取BETA值(最近24个月) -> getBeta24M


# 获取BETA值(最近60个月)时间序列 -> getBeta60MSeries


# 获取BETA值(最近60个月) -> getBeta60M


# 获取Beta时间序列 -> getBetaSeries


# 获取Beta -> getBeta


# 获取Beta(剔除财务杠杆)时间序列 -> getBetaDfSeries


# 获取Beta(剔除财务杠杆) -> getBetaDf


# 获取Beta_FUND时间序列 -> getRiskBetaSeries


# 获取Beta_FUND -> getRiskBeta


# 获取个股20日的beta值_PIT时间序列 -> getRiskBeta20Series


# 获取个股20日的beta值_PIT -> getRiskBeta20


# 获取个股60日的beta值_PIT时间序列 -> getRiskBeta60Series


# 获取个股60日的beta值_PIT -> getRiskBeta60


# 获取个股120日的beta值_PIT时间序列 -> getRiskBeta120Series


# 获取个股120日的beta值_PIT -> getRiskBeta120


# 获取Beta同类平均时间序列 -> getRiskSimLAvgBetaSeries


# 获取Beta同类平均 -> getRiskSimLAvgBeta


# 获取Jensen时间序列 -> getJensenSeries


# 获取Jensen -> getJensen


# 获取Jensen(年化)时间序列 -> getJensenYSeries


# 获取Jensen(年化) -> getJensenY


# 获取Jensen_FUND时间序列 -> getRiskJensenSeries


# 获取Jensen_FUND -> getRiskJensen


# 获取Jensen(年化)_FUND时间序列 -> getRiskAnNuJensenSeries


# 获取Jensen(年化)_FUND -> getRiskAnNuJensen


# 获取IRR时间序列 -> getTBfIRrSeries


# 获取IRR -> getTBfIRr


# 获取IRR(支持历史)时间序列 -> getTBfIRr2Series


# 获取IRR(支持历史) -> getTBfIRr2


# 获取营业外收支净额(TTM)时间序列 -> getNonOperateProfitTtM2Series


# 获取营业外收支净额(TTM) -> getNonOperateProfitTtM2


# 获取营业开支_GSD时间序列 -> getWgsDOperExpSeries


# 获取营业开支_GSD -> getWgsDOperExp


# 获取运营资本_PIT时间序列 -> getFaWorkCapitalSeries


# 获取运营资本_PIT -> getFaWorkCapital


# 获取营业外收支净额(TTM)_PIT时间序列 -> getFaNoOperProfitTtMSeries


# 获取营业外收支净额(TTM)_PIT -> getFaNoOperProfitTtM


# 获取营业外收支净额(TTM,只有最新数据)时间序列 -> getNonOperateProfitTtMSeries


# 获取营业外收支净额(TTM,只有最新数据) -> getNonOperateProfitTtM


# 获取自营业务收入_GSD时间序列 -> getWgsDTradeIncSeries


# 获取自营业务收入_GSD -> getWgsDTradeInc


# 获取留存盈余比率(TTM)_PIT时间序列 -> getFaRetainedEarnTtMSeries


# 获取留存盈余比率(TTM)_PIT -> getFaRetainedEarnTtM


# 获取BR意愿指标_PIT时间序列 -> getTechBrSeries


# 获取BR意愿指标_PIT -> getTechBr


# 获取基金经营业绩_FUND时间序列 -> getStmIs25Series


# 获取基金经营业绩_FUND -> getStmIs25


# 获取单季度.自营业务收入_GSD时间序列 -> getWgsDQfaTradeIncSeries


# 获取单季度.自营业务收入_GSD -> getWgsDQfaTradeInc


# 获取ARBR人气意愿指标_PIT时间序列 -> getTechARbrSeries


# 获取ARBR人气意愿指标_PIT -> getTechARbr


# 获取一致预测每股收益(FY2)与一致预测每股收益(FY1)的变化率_PIT时间序列 -> getWestEpsFyGrowthSeries


# 获取一致预测每股收益(FY2)与一致预测每股收益(FY1)的变化率_PIT -> getWestEpsFyGrowth


# 获取一致预测每股收益(FY1)最大与一致预测每股收益(FY1)最小值的变化率_PIT时间序列 -> getWestEpsMaxMinFy1Series


# 获取一致预测每股收益(FY1)最大与一致预测每股收益(FY1)最小值的变化率_PIT -> getWestEpsMaxMinFy1


# 获取Sharpe(年化)时间序列 -> getSharpeSeries


# 获取Sharpe(年化) -> getSharpe


# 获取Sharpe时间序列 -> getRiskSharpeSeries


# 获取Sharpe -> getRiskSharpe


# 获取Sharpe(年化)_FUND时间序列 -> getRiskAnNuSharpeSeries


# 获取Sharpe(年化)_FUND -> getRiskAnNuSharpe


# 获取Sharpe同类平均时间序列 -> getRiskSimLAvgSharpeSeries


# 获取Sharpe同类平均 -> getRiskSimLAvgSharpe


# 获取Sharpe(年化)同类平均时间序列 -> getRiskSimLAvgAnNuSharpeSeries


# 获取Sharpe(年化)同类平均 -> getRiskSimLAvgAnNuSharpe


# 获取Treynor(年化)时间序列 -> getTreyNorSeries


# 获取Treynor(年化) -> getTreyNor


# 获取Treynor时间序列 -> getRiskTreyNorSeries


# 获取Treynor -> getRiskTreyNor


# 获取20日特诺雷比率_PIT时间序列 -> getRiskTreyNorRatio20Series


# 获取20日特诺雷比率_PIT -> getRiskTreyNorRatio20


# 获取60日特诺雷比率_PIT时间序列 -> getRiskTreyNorRatio60Series


# 获取60日特诺雷比率_PIT -> getRiskTreyNorRatio60


# 获取120日特诺雷比率_PIT时间序列 -> getRiskTreyNorRatio120Series


# 获取120日特诺雷比率_PIT -> getRiskTreyNorRatio120


# 获取Treynor(年化)_FUND时间序列 -> getRiskAnNutReyNorSeries


# 获取Treynor(年化)_FUND -> getRiskAnNutReyNor


# 获取Sortino时间序列 -> getRiskSortInOSeries


# 获取Sortino -> getRiskSortInO


# 获取Sortino(年化)时间序列 -> getRiskAnNuSortInOSeries


# 获取Sortino(年化) -> getRiskAnNuSortInO


# 获取Sortino同类平均时间序列 -> getRiskSimLAvgSortInOSeries


# 获取Sortino同类平均 -> getRiskSimLAvgSortInO


# 获取Sortino(年化)同类平均时间序列 -> getRiskSimLAvgAnNuSortInOSeries


# 获取Sortino(年化)同类平均 -> getRiskSimLAvgAnNuSortInO


# 获取Calmar时间序列 -> getRiskCalmaRSeries


# 获取Calmar -> getRiskCalmaR


# 获取Sterling1时间序列 -> getRiskSterling1Series


# 获取Sterling1 -> getRiskSterling1


# 获取Sterling2时间序列 -> getRiskSterling2Series


# 获取Sterling2 -> getRiskSterling2


# 获取CTD时间序列 -> getTBfCTdSeries


# 获取CTD -> getTBfCTd


# 获取CTD(支持历史)时间序列 -> getTBfCTd2Series


# 获取CTD(支持历史) -> getTBfCTd2


# 获取市盈率PE(TTM)时间序列 -> getPeTtMSeries


# 获取市盈率PE(TTM) -> getPeTtM


# 获取市销率PS(TTM)时间序列 -> getPsTtMSeries


# 获取市销率PS(TTM) -> getPsTtM


# 获取每股收益EPS(TTM)时间序列 -> getEpsTtMSeries


# 获取每股收益EPS(TTM) -> getEpsTtM


# 获取市盈率PE(TTM,剔除负值)时间序列 -> getValPeNonNegativeSeries


# 获取市盈率PE(TTM,剔除负值) -> getValPeNonNegative


# 获取市盈率PE(TTM,中位数)时间序列 -> getValPeMedianSeries


# 获取市盈率PE(TTM,中位数) -> getValPeMedian


# 获取投入资本回报率ROIC(TTM)时间序列 -> getRoiCTtM2Series


# 获取投入资本回报率ROIC(TTM) -> getRoiCTtM2


# 获取息税前利润(TTM反推法)时间序列 -> getEbItTtM2Series


# 获取息税前利润(TTM反推法) -> getEbItTtM2


# 获取投入资本回报率(TTM)_GSD时间序列 -> getRoiCTtM3Series


# 获取投入资本回报率(TTM)_GSD -> getRoiCTtM3


# 获取息税前利润(TTM反推法)_GSD时间序列 -> getEbItTtM3Series


# 获取息税前利润(TTM反推法)_GSD -> getEbItTtM3


# 获取息税前利润(TTM,只有最新数据)时间序列 -> getEbItTtMSeries


# 获取息税前利润(TTM,只有最新数据) -> getEbItTtM


# 获取(废弃)投入资本回报率(TTM)时间序列 -> getRoiCTtMSeries


# 获取(废弃)投入资本回报率(TTM) -> getRoiCTtM


# 获取区间最高PE(TTM)时间序列 -> getValPetTmHighSeries


# 获取区间最高PE(TTM) -> getValPetTmHigh


# 获取区间最低PE(TTM)时间序列 -> getValPetTmLowSeries


# 获取区间最低PE(TTM) -> getValPetTmLow


# 获取区间平均PE(TTM)时间序列 -> getValPetTmAvgSeries


# 获取区间平均PE(TTM) -> getValPetTmAvg


# 获取区间最高PS(TTM)时间序列 -> getValPstTmHighSeries


# 获取区间最高PS(TTM) -> getValPstTmHigh


# 获取区间最低PS(TTM)时间序列 -> getValPstTmLowSeries


# 获取区间最低PS(TTM) -> getValPstTmLow


# 获取区间平均PS(TTM)时间序列 -> getValPstTmAvgSeries


# 获取区间平均PS(TTM) -> getValPstTmAvg


# 获取投入资本回报率(TTM)时间序列 -> getRoiC2TtMSeries


# 获取投入资本回报率(TTM) -> getRoiC2TtM


# 获取EBIT(TTM)时间序列 -> getEbIt2TtMSeries


# 获取EBIT(TTM) -> getEbIt2TtM


# 获取投入资本回报率ROIC(TTM)_GSD时间序列 -> getRoiC2TtM2Series


# 获取投入资本回报率ROIC(TTM)_GSD -> getRoiC2TtM2


# 获取EBIT(TTM)_GSD时间序列 -> getEbIt2TtM3Series


# 获取EBIT(TTM)_GSD -> getEbIt2TtM3


# 获取市盈率PE(TTM,加权)时间序列 -> getValPeTtMwGtSeries


# 获取市盈率PE(TTM,加权) -> getValPeTtMwGt


# 获取发布方市盈率PE(TTM)时间序列 -> getValPeTtMIssuerSeries


# 获取发布方市盈率PE(TTM) -> getValPeTtMIssuer


# 获取市销率PS(TTM,加权)时间序列 -> getValPsTtMwGtSeries


# 获取市销率PS(TTM,加权) -> getValPsTtMwGt


# 获取EBITDA(TTM反推法)时间序列 -> getEbItDaTtMSeries


# 获取EBITDA(TTM反推法) -> getEbItDaTtM


# 获取EBITDA(TTM反推法)_GSD时间序列 -> getEbItDaTtM3Series


# 获取EBITDA(TTM反推法)_GSD -> getEbItDaTtM3


# 获取资本报酬率(TTM)_PIT时间序列 -> getFaRocTtMSeries


# 获取资本报酬率(TTM)_PIT -> getFaRocTtM


# 获取权益回报率(TTM)_PIT时间序列 -> getFaRoeTtMSeries


# 获取权益回报率(TTM)_PIT -> getFaRoeTtM


# 获取市现率PCF(经营现金流TTM)时间序列 -> getPcfOCFTtMSeries


# 获取市现率PCF(经营现金流TTM) -> getPcfOCFTtM


# 获取市现率PCF(现金净流量TTM)时间序列 -> getPcfNCfTtMSeries


# 获取市现率PCF(现金净流量TTM) -> getPcfNCfTtM


# 获取EBITDA(TTM)时间序列 -> getEbItDa2TtMSeries


# 获取EBITDA(TTM) -> getEbItDa2TtM


# 获取EBITDA(TTM)_GSD时间序列 -> getEbItDa2TtM2Series


# 获取EBITDA(TTM)_GSD -> getEbItDa2TtM2


# 获取投入资本回报率(TTM)_PIT时间序列 -> getFaRoiCTtMSeries


# 获取投入资本回报率(TTM)_PIT -> getFaRoiCTtM


# 获取EBIT(TTM)_PIT时间序列 -> getFaEbItTtMSeries


# 获取EBIT(TTM)_PIT -> getFaEbItTtM


# 获取现金净流量(TTM)_PIT时间序列 -> getFaCashFlowTtMSeries


# 获取现金净流量(TTM)_PIT -> getFaCashFlowTtM


# 获取现金净流量(TTM)时间序列 -> getCashFlowTtM2Series


# 获取现金净流量(TTM) -> getCashFlowTtM2


# 获取现金净流量(TTM)_GSD时间序列 -> getCashFlowTtM3Series


# 获取现金净流量(TTM)_GSD -> getCashFlowTtM3


# 获取EBITDA(TTM)_PIT时间序列 -> getFaEbItDaTtMSeries


# 获取EBITDA(TTM)_PIT -> getFaEbItDaTtM


# 获取市现率PCF(经营现金流TTM,加权)时间序列 -> getValPcfOcFtTMwGtSeries


# 获取市现率PCF(经营现金流TTM,加权) -> getValPcfOcFtTMwGt


# 获取营收市值比(TTM)_PIT时间序列 -> getValOrToMvTtMSeries


# 获取营收市值比(TTM)_PIT -> getValOrToMvTtM


# 获取销售商品提供劳务收到的现金(TTM)时间序列 -> getSalesCashInttM2Series


# 获取销售商品提供劳务收到的现金(TTM) -> getSalesCashInttM2


# 获取股利保障倍数(TTM)_PIT时间序列 -> getFaDivCoverTtMSeries


# 获取股利保障倍数(TTM)_PIT -> getFaDivCoverTtM


# 获取投入资本回报率ROIC(TTM)_PIT时间序列 -> getFaRoiCebitTtMSeries


# 获取投入资本回报率ROIC(TTM)_PIT -> getFaRoiCebitTtM


# 获取销售税金率(TTM)_PIT时间序列 -> getFaTaxRatioTtMSeries


# 获取销售税金率(TTM)_PIT -> getFaTaxRatioTtM


# 获取销售商品提供劳务收到的现金(TTM,只有最新数据)时间序列 -> getSalesCashInttMSeries


# 获取销售商品提供劳务收到的现金(TTM,只有最新数据) -> getSalesCashInttM


# 获取扣非后每股收益(TTM)时间序列 -> getEpsDeductedTtMSeries


# 获取扣非后每股收益(TTM) -> getEpsDeductedTtM


# 获取息税前利润(TTM反推法)_PIT时间序列 -> getFaEbItUnVerTtMSeries


# 获取息税前利润(TTM反推法)_PIT -> getFaEbItUnVerTtM


# 获取销售商品提供劳务收到的现金(TTM)_PIT时间序列 -> getFaSalesCashTtMSeries


# 获取销售商品提供劳务收到的现金(TTM)_PIT -> getFaSalesCashTtM


# 获取期间费用(TTM)_GSD时间序列 -> getPeriodExpenseTtMSeries


# 获取期间费用(TTM)_GSD -> getPeriodExpenseTtM


# 获取贝里比率(TTM)_PIT时间序列 -> getFaBerryRatioTtMSeries


# 获取贝里比率(TTM)_PIT -> getFaBerryRatioTtM


# 获取收益市值比(TTM)_PIT时间序列 -> getFaProfitToMvTtMSeries


# 获取收益市值比(TTM)_PIT -> getFaProfitToMvTtM


# 获取期间费用(TTM)_PIT时间序列 -> getFaPerExpenseTtMSeries


# 获取期间费用(TTM)_PIT -> getFaPerExpenseTtM


# 获取投资活动现金净流量(TTM)时间序列 -> getInvestCashFlowTtM2Series


# 获取投资活动现金净流量(TTM) -> getInvestCashFlowTtM2


# 获取投资活动现金净流量(TTM)_GSD时间序列 -> getInvestCashFlowTtM3Series


# 获取投资活动现金净流量(TTM)_GSD -> getInvestCashFlowTtM3


# 获取EBITDA(TTM反推法)_PIT时间序列 -> getFaEbItDaInverTtMSeries


# 获取EBITDA(TTM反推法)_PIT -> getFaEbItDaInverTtM


# 获取投资活动现金净流量(TTM,只有最新数据)时间序列 -> getInvestCashFlowTtMSeries


# 获取投资活动现金净流量(TTM,只有最新数据) -> getInvestCashFlowTtM


# 获取经营活动现金净流量(TTM)_PIT时间序列 -> getFaOperaCtCashFlowTtMSeries


# 获取经营活动现金净流量(TTM)_PIT -> getFaOperaCtCashFlowTtM


# 获取期间费用(TTM)时间序列 -> getPeriodExpenseTTtMSeries


# 获取期间费用(TTM) -> getPeriodExpenseTTtM


# 获取利息费用(TTM)时间序列 -> getInterestExpenseTtMSeries


# 获取利息费用(TTM) -> getInterestExpenseTtM


# 获取经营活动现金净流量(TTM)时间序列 -> getOperateCashFlowTtM2Series


# 获取经营活动现金净流量(TTM) -> getOperateCashFlowTtM2


# 获取筹资活动现金净流量(TTM)时间序列 -> getFinanceCashFlowTtM2Series


# 获取筹资活动现金净流量(TTM) -> getFinanceCashFlowTtM2


# 获取经营活动现金净流量(TTM)_GSD时间序列 -> getOperateCashFlowTtM3Series


# 获取经营活动现金净流量(TTM)_GSD -> getOperateCashFlowTtM3


# 获取筹资活动现金净流量(TTM)_GSD时间序列 -> getFinanceCashFlowTtM3Series


# 获取筹资活动现金净流量(TTM)_GSD -> getFinanceCashFlowTtM3


# 获取现金转换周期(TTM)_PIT时间序列 -> getFaCashCNvCycleTtMSeries


# 获取现金转换周期(TTM)_PIT -> getFaCashCNvCycleTtM


# 获取筹资活动现金净流量(TTM,只有最新数据)时间序列 -> getFinanceCashFlowTtMSeries


# 获取筹资活动现金净流量(TTM,只有最新数据) -> getFinanceCashFlowTtM


# 获取资金现金回收率(TTM)_PIT时间序列 -> getFaCashRecovRatioTtMSeries


# 获取资金现金回收率(TTM)_PIT -> getFaCashRecovRatioTtM


# 获取投资活动现金净流量(TTM)_PIT时间序列 -> getFaInveActCashFlowTtMSeries


# 获取投资活动现金净流量(TTM)_PIT -> getFaInveActCashFlowTtM


# 获取筹资活动现金净流量(TTM)_PIT时间序列 -> getFaFinaActCashFlowTtMSeries


# 获取筹资活动现金净流量(TTM)_PIT -> getFaFinaActCashFlowTtM


# 获取每股EBITDA时间序列 -> getEbItDapSSeries


# 获取每股EBITDA -> getEbItDapS


# 获取已获利息倍数(EBIT/利息费用)时间序列 -> getEbItToInterestSeries


# 获取已获利息倍数(EBIT/利息费用) -> getEbItToInterest


# 获取EBITDA/利息费用时间序列 -> getEbItDatoInterestSeries


# 获取EBITDA/利息费用 -> getEbItDatoInterest


# 获取EBIT(反推法)时间序列 -> getEbItSeries


# 获取EBIT(反推法) -> getEbIt


# 获取EBITDA(反推法)时间序列 -> getEbItDaSeries


# 获取EBITDA(反推法) -> getEbItDa


# 获取EBIT时间序列 -> getEbIt2Series


# 获取EBIT -> getEbIt2


# 获取EBITDA时间序列 -> getEbItDa2Series


# 获取EBITDA -> getEbItDa2


# 获取EBITDA(公布值)_GSD时间序列 -> getIsEbItDaArdSeries


# 获取EBITDA(公布值)_GSD -> getIsEbItDaArd


# 获取利息保障倍数_PIT时间序列 -> getFaEbItToInterestSeries


# 获取利息保障倍数_PIT -> getFaEbItToInterest


# 获取全部债务/EBITDA时间序列 -> getTlToeBitDaSeries


# 获取全部债务/EBITDA -> getTlToeBitDa


# 获取已获利息倍数(EBIT/利息费用)_GSD时间序列 -> getWgsDEbItToInterestSeries


# 获取已获利息倍数(EBIT/利息费用)_GSD -> getWgsDEbItToInterest


# 获取息税前利润_GSD时间序列 -> getWgsDEbIt3Series


# 获取息税前利润_GSD -> getWgsDEbIt3


# 获取息税折旧摊销前利润_GSD时间序列 -> getWgsDEbItDa2Series


# 获取息税折旧摊销前利润_GSD -> getWgsDEbItDa2


# 获取EBIT(反推法)_GSD时间序列 -> getWgsDEbItSeries


# 获取EBIT(反推法)_GSD -> getWgsDEbIt


# 获取EBITDA(反推法)_GSD时间序列 -> getWgsDEbItDaSeries


# 获取EBITDA(反推法)_GSD -> getWgsDEbItDa


# 获取企业倍数(EV2/EBITDA)时间序列 -> getEv2ToEbItDaSeries


# 获取企业倍数(EV2/EBITDA) -> getEv2ToEbItDa


# 获取预测息税前利润(EBIT)平均值时间序列 -> getEstAvGebItSeries


# 获取预测息税前利润(EBIT)平均值 -> getEstAvGebIt


# 获取预测息税前利润(EBIT)最大值时间序列 -> getEstMaxEbItSeries


# 获取预测息税前利润(EBIT)最大值 -> getEstMaxEbIt


# 获取预测息税前利润(EBIT)最小值时间序列 -> getEstMineBitSeries


# 获取预测息税前利润(EBIT)最小值 -> getEstMineBit


# 获取预测息税前利润(EBIT)标准差时间序列 -> getEstStDebitSeries


# 获取预测息税前利润(EBIT)标准差 -> getEstStDebit


# 获取预测息税折旧摊销前利润(EBITDA)平均值时间序列 -> getEstAvGebItDaSeries


# 获取预测息税折旧摊销前利润(EBITDA)平均值 -> getEstAvGebItDa


# 获取预测息税折旧摊销前利润(EBITDA)最大值时间序列 -> getEstMaxEbItDaSeries


# 获取预测息税折旧摊销前利润(EBITDA)最大值 -> getEstMaxEbItDa


# 获取预测息税折旧摊销前利润(EBITDA)最小值时间序列 -> getEstMineBitDaSeries


# 获取预测息税折旧摊销前利润(EBITDA)最小值 -> getEstMineBitDa


# 获取预测息税折旧摊销前利润(EBITDA)标准差时间序列 -> getEstStDebitDaSeries


# 获取预测息税折旧摊销前利润(EBITDA)标准差 -> getEstStDebitDa


# 获取预测息税前利润(EBIT)平均值(币种转换)时间序列 -> getEstAvGebIt1Series


# 获取预测息税前利润(EBIT)平均值(币种转换) -> getEstAvGebIt1


# 获取预测息税前利润(EBIT)最大值(币种转换)时间序列 -> getEstMaxEbIt1Series


# 获取预测息税前利润(EBIT)最大值(币种转换) -> getEstMaxEbIt1


# 获取预测息税前利润(EBIT)最小值(币种转换)时间序列 -> getEstMineBit1Series


# 获取预测息税前利润(EBIT)最小值(币种转换) -> getEstMineBit1


# 获取预测息税前利润(EBIT)标准差(币种转换)时间序列 -> getEstStDebit1Series


# 获取预测息税前利润(EBIT)标准差(币种转换) -> getEstStDebit1


# 获取预测息税折旧摊销前利润(EBITDA)平均值(币种转换)时间序列 -> getEstAvGebItDa1Series


# 获取预测息税折旧摊销前利润(EBITDA)平均值(币种转换) -> getEstAvGebItDa1


# 获取预测息税折旧摊销前利润(EBITDA)最大值(币种转换)时间序列 -> getEstMaxEbItDa1Series


# 获取预测息税折旧摊销前利润(EBITDA)最大值(币种转换) -> getEstMaxEbItDa1


# 获取预测息税折旧摊销前利润(EBITDA)最小值(币种转换)时间序列 -> getEstMineBitDa1Series


# 获取预测息税折旧摊销前利润(EBITDA)最小值(币种转换) -> getEstMineBitDa1


# 获取预测息税折旧摊销前利润(EBITDA)标准差(币种转换)时间序列 -> getEstStDebitDa1Series


# 获取预测息税折旧摊销前利润(EBITDA)标准差(币种转换) -> getEstStDebitDa1


# 获取企业倍数2(EV2/EBITDA)时间序列 -> getValEvToeBitDa2Series


# 获取企业倍数2(EV2/EBITDA) -> getValEvToeBitDa2


# 获取一致预测息税前利润(FY1)时间序列 -> getWestAvGebItFy1Series


# 获取一致预测息税前利润(FY1) -> getWestAvGebItFy1


# 获取一致预测息税前利润(FY2)时间序列 -> getWestAvGebItFy2Series


# 获取一致预测息税前利润(FY2) -> getWestAvGebItFy2


# 获取一致预测息税前利润(FY3)时间序列 -> getWestAvGebItFy3Series


# 获取一致预测息税前利润(FY3) -> getWestAvGebItFy3


# 获取一致预测息税折旧摊销前利润(FY1)时间序列 -> getWestAvGebItDaFy1Series


# 获取一致预测息税折旧摊销前利润(FY1) -> getWestAvGebItDaFy1


# 获取一致预测息税折旧摊销前利润(FY2)时间序列 -> getWestAvGebItDaFy2Series


# 获取一致预测息税折旧摊销前利润(FY2) -> getWestAvGebItDaFy2


# 获取一致预测息税折旧摊销前利润(FY3)时间序列 -> getWestAvGebItDaFy3Series


# 获取一致预测息税折旧摊销前利润(FY3) -> getWestAvGebItDaFy3


# 获取预测息税前利润(EBIT)平均值(可选类型)时间序列 -> getWestAvGebItSeries


# 获取预测息税前利润(EBIT)平均值(可选类型) -> getWestAvGebIt


# 获取预测息税前利润(EBIT)最大值(可选类型)时间序列 -> getWestMaxEbItSeries


# 获取预测息税前利润(EBIT)最大值(可选类型) -> getWestMaxEbIt


# 获取预测息税前利润(EBIT)最小值(可选类型)时间序列 -> getWestMineBitSeries


# 获取预测息税前利润(EBIT)最小值(可选类型) -> getWestMineBit


# 获取预测息税前利润(EBIT)标准差(可选类型)时间序列 -> getWestStDebitSeries


# 获取预测息税前利润(EBIT)标准差(可选类型) -> getWestStDebit


# 获取预测息税折旧摊销前利润(EBITDA)平均值(可选类型)时间序列 -> getWestAvGebItDaSeries


# 获取预测息税折旧摊销前利润(EBITDA)平均值(可选类型) -> getWestAvGebItDa


# 获取预测息税折旧摊销前利润(EBITDA)最大值(可选类型)时间序列 -> getWestMaxEbItDaSeries


# 获取预测息税折旧摊销前利润(EBITDA)最大值(可选类型) -> getWestMaxEbItDa


# 获取预测息税折旧摊销前利润(EBITDA)最小值(可选类型)时间序列 -> getWestMineBitDaSeries


# 获取预测息税折旧摊销前利润(EBITDA)最小值(可选类型) -> getWestMineBitDa


# 获取预测息税折旧摊销前利润(EBITDA)标准差(可选类型)时间序列 -> getWestStDebitDaSeries


# 获取预测息税折旧摊销前利润(EBITDA)标准差(可选类型) -> getWestStDebitDa


# 获取预测息税前利润(EBIT)平均值(可选类型,币种转换)时间序列 -> getWestAvGebIt1Series


# 获取预测息税前利润(EBIT)平均值(可选类型,币种转换) -> getWestAvGebIt1


# 获取预测息税前利润(EBIT)最大值(可选类型,币种转换)时间序列 -> getWestMaxEbIt1Series


# 获取预测息税前利润(EBIT)最大值(可选类型,币种转换) -> getWestMaxEbIt1


# 获取预测息税前利润(EBIT)最小值(可选类型,币种转换)时间序列 -> getWestMineBit1Series


# 获取预测息税前利润(EBIT)最小值(可选类型,币种转换) -> getWestMineBit1


# 获取预测息税前利润(EBIT)标准差(可选类型,币种转换)时间序列 -> getWestStDebit1Series


# 获取预测息税前利润(EBIT)标准差(可选类型,币种转换) -> getWestStDebit1


# 获取预测息税折旧摊销前利润(EBITDA)平均值(可选类型,币种转换)时间序列 -> getWestAvGebItDa1Series


# 获取预测息税折旧摊销前利润(EBITDA)平均值(可选类型,币种转换) -> getWestAvGebItDa1


# 获取预测息税折旧摊销前利润(EBITDA)最大值(可选类型,币种转换)时间序列 -> getWestMaxEbItDa1Series


# 获取预测息税折旧摊销前利润(EBITDA)最大值(可选类型,币种转换) -> getWestMaxEbItDa1


# 获取预测息税折旧摊销前利润(EBITDA)最小值(可选类型,币种转换)时间序列 -> getWestMineBitDa1Series


# 获取预测息税折旧摊销前利润(EBITDA)最小值(可选类型,币种转换) -> getWestMineBitDa1


# 获取预测息税折旧摊销前利润(EBITDA)标准差(可选类型,币种转换)时间序列 -> getWestStDebitDa1Series


# 获取预测息税折旧摊销前利润(EBITDA)标准差(可选类型,币种转换) -> getWestStDebitDa1


# 获取预测息税前利润(EBIT)中值时间序列 -> getEstMedianEbItSeries


# 获取预测息税前利润(EBIT)中值 -> getEstMedianEbIt


# 获取预测息税折旧摊销前利润(EBITDA)中值时间序列 -> getEstMedianEbItDaSeries


# 获取预测息税折旧摊销前利润(EBITDA)中值 -> getEstMedianEbItDa


# 获取预测息税前利润(EBIT)中值(币种转换)时间序列 -> getEstMedianEbIt1Series


# 获取预测息税前利润(EBIT)中值(币种转换) -> getEstMedianEbIt1


# 获取预测息税折旧摊销前利润(EBITDA)中值(币种转换)时间序列 -> getEstMedianEbItDa1Series


# 获取预测息税折旧摊销前利润(EBITDA)中值(币种转换) -> getEstMedianEbItDa1


# 获取预测息税前利润(EBIT)中值(可选类型)时间序列 -> getWestMedianEbItSeries


# 获取预测息税前利润(EBIT)中值(可选类型) -> getWestMedianEbIt


# 获取预测息税折旧摊销前利润(EBITDA)中值(可选类型)时间序列 -> getWestMedianEbItDaSeries


# 获取预测息税折旧摊销前利润(EBITDA)中值(可选类型) -> getWestMedianEbItDa


# 获取预测息税前利润(EBIT)中值(可选类型,币种转换)时间序列 -> getWestMedianEbIt1Series


# 获取预测息税前利润(EBIT)中值(可选类型,币种转换) -> getWestMedianEbIt1


# 获取预测息税折旧摊销前利润(EBITDA)中值(可选类型,币种转换)时间序列 -> getWestMedianEbItDa1Series


# 获取预测息税折旧摊销前利润(EBITDA)中值(可选类型,币种转换) -> getWestMedianEbItDa1


# 获取梅斯线_PIT时间序列 -> getTechMassSeries


# 获取梅斯线_PIT -> getTechMass


# 获取对数市值_PIT时间序列 -> getValLnMvSeries


# 获取对数市值_PIT -> getValLnMv


# 获取每股股利_PIT时间序列 -> getFaDpsSeries


# 获取每股股利_PIT -> getFaDps


# 获取账面杠杆_PIT时间序列 -> getFaBLevSeries


# 获取账面杠杆_PIT -> getFaBLev


# 获取市场杠杆_PIT时间序列 -> getFaMLevSeries


# 获取市场杠杆_PIT -> getFaMLev


# 获取股东权益_PIT时间序列 -> getFaToTEquitySeries


# 获取股东权益_PIT -> getFaToTEquity


# 获取股价偏度_PIT时间序列 -> getTechSkewNessSeries


# 获取股价偏度_PIT -> getTechSkewNess


# 获取下跌波动_PIT时间序列 -> getTechDDnsRSeries


# 获取下跌波动_PIT -> getTechDDnsR


# 获取多空指数_PIT时间序列 -> getTechBbiSeries


# 获取多空指数_PIT -> getTechBbi


# 获取多头力道_PIT时间序列 -> getTechBullPowerSeries


# 获取多头力道_PIT -> getTechBullPower


# 获取空头力道_PIT时间序列 -> getTechBearPowerSeries


# 获取空头力道_PIT -> getTechBearPower


# 获取佳庆指标_PIT时间序列 -> getTechCHaikInSeries


# 获取佳庆指标_PIT -> getTechCHaikIn


# 获取阿隆指标_PIT时间序列 -> getTechAroOnSeries


# 获取阿隆指标_PIT -> getTechAroOn


# 获取估波指标_PIT时间序列 -> getTechCoppockCurveSeries


# 获取估波指标_PIT -> getTechCoppockCurve


# 获取终极指标_PIT时间序列 -> getTechUOsSeries


# 获取终极指标_PIT -> getTechUOs


# 获取折旧和摊销_PIT时间序列 -> getFaDaSeries


# 获取折旧和摊销_PIT -> getFaDa


# 获取5日乖离率_PIT时间序列 -> getTechBias5Series


# 获取5日乖离率_PIT -> getTechBias5


# 获取能量潮指标_PIT时间序列 -> getTechObVSeries


# 获取能量潮指标_PIT -> getTechObV


# 获取心理线指标_PIT时间序列 -> getTechPsySeries


# 获取心理线指标_PIT -> getTechPsy


# 获取累积/派发线_PIT时间序列 -> getTechAdSeries


# 获取累积/派发线_PIT -> getTechAd


# 获取均线价格比_PIT时间序列 -> getTechMa10CloseSeries


# 获取均线价格比_PIT -> getTechMa10Close


# 获取波幅中位数_PIT时间序列 -> getTechDHiloSeries


# 获取波幅中位数_PIT -> getTechDHilo


# 获取加权市净率_PIT时间序列 -> getValPbWGtSeries


# 获取加权市净率_PIT -> getValPbWGt


# 获取对数市值立方_PIT时间序列 -> getValNlSizeSeries


# 获取对数市值立方_PIT -> getValNlSize


# 获取现金流市值比_PIT时间序列 -> getFaCTopSeries


# 获取现金流市值比_PIT -> getFaCTop


# 获取息前税后利润_PIT时间序列 -> getFaEbIAtSeries


# 获取息前税后利润_PIT -> getFaEbIAt


# 获取6日变动速率_PIT时间序列 -> getTechRoc6Series


# 获取6日变动速率_PIT -> getTechRoc6


# 获取下轨线(布林线)_PIT时间序列 -> getTechBollDownSeries


# 获取下轨线(布林线)_PIT -> getTechBollDown


# 获取上轨线(布林线)_PIT时间序列 -> getTechBollUpSeries


# 获取上轨线(布林线)_PIT -> getTechBollUp


# 获取10日乖离率_PIT时间序列 -> getTechBias10Series


# 获取10日乖离率_PIT -> getTechBias10


# 获取20日乖离率_PIT时间序列 -> getTechBias20Series


# 获取20日乖离率_PIT -> getTechBias20


# 获取60日乖离率_PIT时间序列 -> getTechBias60Series


# 获取60日乖离率_PIT -> getTechBias60


# 获取5日顺势指标_PIT时间序列 -> getTechCci5Series


# 获取5日顺势指标_PIT -> getTechCci5


# 获取相对离散指数_PIT时间序列 -> getTechRviSeries


# 获取相对离散指数_PIT -> getTechRvi


# 获取相对强弱指标_PIT时间序列 -> getTechRsiSeries


# 获取相对强弱指标_PIT -> getTechRsi


# 获取资金流量指标_PIT时间序列 -> getTechMfiSeries


# 获取资金流量指标_PIT -> getTechMfi


# 获取AR人气指标_PIT时间序列 -> getTechArSeries


# 获取AR人气指标_PIT -> getTechAr


# 获取CR能量指标_PIT时间序列 -> getTechCr20Series


# 获取CR能量指标_PIT -> getTechCr20


# 获取市场能量指标_PIT时间序列 -> getTechCyFSeries


# 获取市场能量指标_PIT -> getTechCyF


# 获取市场强弱指标_PIT时间序列 -> getTechCrySeries


# 获取市场强弱指标_PIT -> getTechCry


# 获取艾达透视指标_PIT时间序列 -> getTechElderSeries


# 获取艾达透视指标_PIT -> getTechElder


# 获取6日均幅指标_PIT时间序列 -> getTechATr6Series


# 获取6日均幅指标_PIT -> getTechATr6


# 获取5日移动均线_PIT时间序列 -> getTechMa5Series


# 获取5日移动均线_PIT -> getTechMa5


# 获取佳庆离散指标_PIT时间序列 -> getTechCHaikInvolSeries


# 获取佳庆离散指标_PIT -> getTechCHaikInvol


# 获取Ulcer5_PIT时间序列 -> getTechUlcer5Series


# 获取Ulcer5_PIT -> getTechUlcer5


# 获取阶段强势指标_PIT时间序列 -> getTechJdQs20Series


# 获取阶段强势指标_PIT -> getTechJdQs20


# 获取阿隆向上指标_PIT时间序列 -> getTechAroOnUpSeries


# 获取阿隆向上指标_PIT -> getTechAroOnUp


# 获取阿隆向下指标_PIT时间序列 -> getTechAroOnDownSeries


# 获取阿隆向下指标_PIT -> getTechAroOnDown


# 获取20日收益方差_PIT时间序列 -> getRiskVariance20Series


# 获取20日收益方差_PIT -> getRiskVariance20


# 获取60日收益方差_PIT时间序列 -> getRiskVariance60Series


# 获取60日收益方差_PIT -> getRiskVariance60


# 获取20日损失方差_PIT时间序列 -> getRiskLossVariance20Series


# 获取20日损失方差_PIT -> getRiskLossVariance20


# 获取60日损失方差_PIT时间序列 -> getRiskLossVariance60Series


# 获取60日损失方差_PIT -> getRiskLossVariance60


# 获取12月累计收益_PIT时间序列 -> getRiskCumReturn12MSeries


# 获取12月累计收益_PIT -> getRiskCumReturn12M


# 获取20日变动速率_PIT时间序列 -> getTechRoc20Series


# 获取20日变动速率_PIT -> getTechRoc20


# 获取异同离差乖离率_PIT时间序列 -> getTechDBcdSeries


# 获取异同离差乖离率_PIT -> getTechDBcd


# 获取10日顺势指标_PIT时间序列 -> getTechCci10Series


# 获取10日顺势指标_PIT -> getTechCci10


# 获取20日顺势指标_PIT时间序列 -> getTechCci20Series


# 获取20日顺势指标_PIT -> getTechCci20


# 获取88日顺势指标_PIT时间序列 -> getTechCci88Series


# 获取88日顺势指标_PIT -> getTechCci88


# 获取收益相对金额比_PIT时间序列 -> getTechIlLiquiditySeries


# 获取收益相对金额比_PIT -> getTechIlLiquidity


# 获取动态买卖气指标_PIT时间序列 -> getTechADtmSeries


# 获取动态买卖气指标_PIT -> getTechADtm


# 获取6日能量潮指标_PIT时间序列 -> getTechObV6Series


# 获取6日能量潮指标_PIT -> getTechObV6


# 获取20日资金流量_PIT时间序列 -> getTechMoneyFlow20Series


# 获取20日资金流量_PIT -> getTechMoneyFlow20


# 获取12月相对强势_PIT时间序列 -> getTechRStr12Series


# 获取12月相对强势_PIT -> getTechRStr12


# 获取24月相对强势_PIT时间序列 -> getTechRStr24Series


# 获取24月相对强势_PIT -> getTechRStr24


# 获取14日均幅指标_PIT时间序列 -> getTechATr14Series


# 获取14日均幅指标_PIT -> getTechATr14


# 获取10日移动均线_PIT时间序列 -> getTechMa10Series


# 获取10日移动均线_PIT -> getTechMa10


# 获取20日移动均线_PIT时间序列 -> getTechMa20Series


# 获取20日移动均线_PIT -> getTechMa20


# 获取60日移动均线_PIT时间序列 -> getTechMa60Series


# 获取60日移动均线_PIT -> getTechMa60


# 获取Ulcer10_PIT时间序列 -> getTechUlcer10Series


# 获取Ulcer10_PIT -> getTechUlcer10


# 获取120日收益方差_PIT时间序列 -> getRiskVariance120Series


# 获取120日收益方差_PIT -> getRiskVariance120


# 获取20日正收益方差_PIT时间序列 -> getRiskGainVariance20Series


# 获取20日正收益方差_PIT -> getRiskGainVariance20


# 获取60日正收益方差_PIT时间序列 -> getRiskGainVariance60Series


# 获取60日正收益方差_PIT -> getRiskGainVariance60


# 获取120日损失方差_PIT时间序列 -> getRiskLossVariance120Series


# 获取120日损失方差_PIT -> getRiskLossVariance120


# 获取钱德动量摆动指标_PIT时间序列 -> getTechCmOSeries


# 获取钱德动量摆动指标_PIT -> getTechCmO


# 获取随机指标KDJ_K_PIT时间序列 -> getTechKDjKSeries


# 获取随机指标KDJ_K_PIT -> getTechKDjK


# 获取随机指标KDJ_D_PIT时间序列 -> getTechKDjDSeries


# 获取随机指标KDJ_D_PIT -> getTechKDjD


# 获取随机指标KDJ_J_PIT时间序列 -> getTechKDjJSeries


# 获取随机指标KDJ_J_PIT -> getTechKDjJ


# 获取20日能量潮指标_PIT时间序列 -> getTechObV20Series


# 获取20日能量潮指标_PIT -> getTechObV20


# 获取市场促进指数指标_PIT时间序列 -> getTechMktFacIInDSeries


# 获取市场促进指数指标_PIT -> getTechMktFacIInD


# 获取12日变化率指数_PIT时间序列 -> getTechRc12Series


# 获取12日变化率指数_PIT -> getTechRc12


# 获取24日变化率指数_PIT时间序列 -> getTechRc24Series


# 获取24日变化率指数_PIT -> getTechRc24


# 获取6日收集派发指标_PIT时间序列 -> getTechAd6Series


# 获取6日收集派发指标_PIT -> getTechAd6


# 获取6日简易波动指标_PIT时间序列 -> getTechEmV6Series


# 获取6日简易波动指标_PIT -> getTechEmV6


# 获取120日移动均线_PIT时间序列 -> getTechMa120Series


# 获取120日移动均线_PIT -> getTechMa120


# 获取5日指数移动均线_PIT时间序列 -> getTechEma5Series


# 获取5日指数移动均线_PIT -> getTechEma5


# 获取方向标准离差指数_PIT时间序列 -> getTechDDiSeries


# 获取方向标准离差指数_PIT -> getTechDDi


# 获取绝对偏差移动平均_PIT时间序列 -> getTechAPbMaSeries


# 获取绝对偏差移动平均_PIT -> getTechAPbMa


# 获取累计振动升降指标_PIT时间序列 -> getTechAsISeries


# 获取累计振动升降指标_PIT -> getTechAsI


# 获取市值/企业自由现金流_PIT时间序列 -> getValMvTOfCffSeries


# 获取市值/企业自由现金流_PIT -> getValMvTOfCff


# 获取120日正收益方差_PIT时间序列 -> getRiskGainVariance120Series


# 获取120日正收益方差_PIT -> getRiskGainVariance120


# 获取5年平均权益回报率_PIT时间序列 -> getFaRoeAvg5YSeries


# 获取5年平均权益回报率_PIT -> getFaRoeAvg5Y


# 获取过去5日的价格动量_PIT时间序列 -> getTechRevs5Series


# 获取过去5日的价格动量_PIT -> getTechRevs5


# 获取过去1年的价格动量_PIT时间序列 -> getTechRevs250Series


# 获取过去1年的价格动量_PIT -> getTechRevs250


# 获取过去3年的价格动量_PIT时间序列 -> getTechRevs750Series


# 获取过去3年的价格动量_PIT -> getTechRevs750


# 获取6日量变动速率指标_PIT时间序列 -> getTechVRoc6Series


# 获取6日量变动速率指标_PIT -> getTechVRoc6


# 获取20日收集派发指标_PIT时间序列 -> getTechAd20Series


# 获取20日收集派发指标_PIT -> getTechAd20


# 获取14日简易波动指标_PIT时间序列 -> getTechEmV14Series


# 获取14日简易波动指标_PIT -> getTechEmV14


# 获取10日指数移动均线_PIT时间序列 -> getTechEma10Series


# 获取10日指数移动均线_PIT -> getTechEma10


# 获取12日指数移动均线_PIT时间序列 -> getTechEma12Series


# 获取12日指数移动均线_PIT -> getTechEma12


# 获取20日指数移动均线_PIT时间序列 -> getTechEma20Series


# 获取20日指数移动均线_PIT -> getTechEma20


# 获取26日指数移动均线_PIT时间序列 -> getTechEma26Series


# 获取26日指数移动均线_PIT -> getTechEma26


# 获取60日指数移动均线_PIT时间序列 -> getTechEma60Series


# 获取60日指数移动均线_PIT -> getTechEma60


# 获取平滑异同移动平均线_PIT时间序列 -> getTechMacDSeries


# 获取平滑异同移动平均线_PIT -> getTechMacD


# 获取算术平均滚动市盈率_PIT时间序列 -> getValPeAvgSeries


# 获取算术平均滚动市盈率_PIT -> getValPeAvg


# 获取市盈率PE行业相对值_PIT时间序列 -> getValPeInDuSwSeries


# 获取市盈率PE行业相对值_PIT -> getValPeInDuSw


# 获取市净率PB行业相对值_PIT时间序列 -> getValPbInDuSwSeries


# 获取市净率PB行业相对值_PIT -> getValPbInDuSw


# 获取市销率PS行业相对值_PIT时间序列 -> getValPsInDuSwSeries


# 获取市销率PS行业相对值_PIT -> getValPsInDuSw


# 获取账面市值比行业相对值_PIT时间序列 -> getValBTopInDuSwSeries


# 获取账面市值比行业相对值_PIT -> getValBTopInDuSw


# 获取20日收益损失方差比_PIT时间序列 -> getRiskGlVarianceRatio20Series


# 获取20日收益损失方差比_PIT -> getRiskGlVarianceRatio20


# 获取60日收益损失方差比_PIT时间序列 -> getRiskGlVarianceRatio60Series


# 获取60日收益损失方差比_PIT -> getRiskGlVarianceRatio60


# 获取个股收益的20日峰度_PIT时间序列 -> getRiskKurtOsIs20Series


# 获取个股收益的20日峰度_PIT -> getRiskKurtOsIs20


# 获取个股收益的60日峰度_PIT时间序列 -> getRiskKurtOsIs60Series


# 获取个股收益的60日峰度_PIT -> getRiskKurtOsIs60


# 获取过去10日的价格动量_PIT时间序列 -> getTechRevs10Series


# 获取过去10日的价格动量_PIT -> getTechRevs10


# 获取过去20日的价格动量_PIT时间序列 -> getTechRevs20Series


# 获取过去20日的价格动量_PIT -> getTechRevs20


# 获取过去3个月的价格动量_PIT时间序列 -> getTechRevs60Series


# 获取过去3个月的价格动量_PIT -> getTechRevs60


# 获取过去6个月的价格动量_PIT时间序列 -> getTechRevs120Series


# 获取过去6个月的价格动量_PIT -> getTechRevs120


# 获取CMO的中间因子SD_PIT时间序列 -> getTechChAndesDSeries


# 获取CMO的中间因子SD_PIT -> getTechChAndesD


# 获取CMO的中间因子SU_PIT时间序列 -> getTechChanDesuSeries


# 获取CMO的中间因子SU_PIT -> getTechChanDesu


# 获取6日成交金额的标准差_PIT时间序列 -> getTechTvsTd6Series


# 获取6日成交金额的标准差_PIT -> getTechTvsTd6


# 获取12日量变动速率指标_PIT时间序列 -> getTechVRoc12Series


# 获取12日量变动速率指标_PIT -> getTechVRoc12


# 获取120日指数移动均线_PIT时间序列 -> getTechEma120Series


# 获取120日指数移动均线_PIT -> getTechEma120


# 获取市现率PCF行业相对值_PIT时间序列 -> getValPcfInDuSwSeries


# 获取市现率PCF行业相对值_PIT -> getValPcfInDuSw


# 获取120日收益损失方差比_PIT时间序列 -> getRiskGlVarianceRatio120Series


# 获取120日收益损失方差比_PIT -> getRiskGlVarianceRatio120


# 获取个股收益的120日峰度_PIT时间序列 -> getRiskKurtOsIs120Series


# 获取个股收益的120日峰度_PIT -> getRiskKurtOsIs120


# 获取归属于母公司的股东权益_PIT时间序列 -> getFaEquitySeries


# 获取归属于母公司的股东权益_PIT -> getFaEquity


# 获取过去5日收益率/行业均值_PIT时间序列 -> getTechRevs5InDu1Series


# 获取过去5日收益率/行业均值_PIT -> getTechRevs5InDu1


# 获取20日成交金额的标准差_PIT时间序列 -> getTechTvsTd20Series


# 获取20日成交金额的标准差_PIT -> getTechTvsTd20


# 获取DDI的中间因子DIZ_PIT时间序列 -> getTechDizSeries


# 获取DDI的中间因子DIZ_PIT -> getTechDiz


# 获取DDI的中间因子DIF_PIT时间序列 -> getTechDIfSeries


# 获取DDI的中间因子DIF_PIT -> getTechDIf


# 获取5日三重指数移动平均线_PIT时间序列 -> getTechTemA5Series


# 获取5日三重指数移动平均线_PIT -> getTechTemA5


# 获取过去1个月收益率/行业均值_PIT时间序列 -> getTechRevs20InDu1Series


# 获取过去1个月收益率/行业均值_PIT -> getTechRevs20InDu1


# 获取ADTM的中间因子SBM_PIT时间序列 -> getTechSBmSeries


# 获取ADTM的中间因子SBM_PIT -> getTechSBm


# 获取ADTM的中间因子STM_PIT时间序列 -> getTechStmSeries


# 获取ADTM的中间因子STM_PIT -> getTechStm


# 获取6日成交金额的移动平均值_PIT时间序列 -> getTechTvMa6Series


# 获取6日成交金额的移动平均值_PIT -> getTechTvMa6


# 获取MACD的中间因子DEA_PIT时间序列 -> getTechDeASeries


# 获取MACD的中间因子DEA_PIT -> getTechDeA


# 获取10日三重指数移动平均线_PIT时间序列 -> getTechTemA10Series


# 获取10日三重指数移动平均线_PIT -> getTechTemA10


# 获取所属申万一级行业的PE均值_PIT时间序列 -> getValAvgPeSwSeries


# 获取所属申万一级行业的PE均值_PIT -> getValAvgPeSw


# 获取所属申万一级行业的PB均值_PIT时间序列 -> getValAvgPbSwSeries


# 获取所属申万一级行业的PB均值_PIT -> getValAvgPbSw


# 获取所属申万一级行业的PS均值_PIT时间序列 -> getValAvGpsSwSeries


# 获取所属申万一级行业的PS均值_PIT -> getValAvGpsSw


# 获取30日120日回报方差比率_PIT时间序列 -> getRiskRevsVarRatioSeries


# 获取30日120日回报方差比率_PIT -> getRiskRevsVarRatio


# 获取20日成交金额的移动平均值_PIT时间序列 -> getTechTvMa20Series


# 获取20日成交金额的移动平均值_PIT -> getTechTvMa20


# 获取MACD的中间因子DIFF_PIT时间序列 -> getTechDiffSeries


# 获取MACD的中间因子DIFF_PIT -> getTechDiff


# 获取与过去52 周股价最高点差距_PIT时间序列 -> getTechChgMaxSeries


# 获取与过去52 周股价最高点差距_PIT -> getTechChgMax


# 获取归属母公司股东的股东权益(LF)_PIT时间序列 -> getEquityNewSeries


# 获取归属母公司股东的股东权益(LF)_PIT -> getEquityNew


# 获取市盈率PE/过去一年PE的均值_PIT时间序列 -> getValPeToHist250Series


# 获取市盈率PE/过去一年PE的均值_PIT -> getValPeToHist250


# 获取所属申万一级行业的PCF均值_PIT时间序列 -> getValAvgPcfSwSeries


# 获取所属申万一级行业的PCF均值_PIT -> getValAvgPcfSw


# 获取所属申万一级行业的PE标准差_PIT时间序列 -> getValStdPeSwSeries


# 获取所属申万一级行业的PE标准差_PIT -> getValStdPeSw


# 获取所属申万一级行业的PB标准差_PIT时间序列 -> getValStdPbSwSeries


# 获取所属申万一级行业的PB标准差_PIT -> getValStdPbSw


# 获取所属申万一级行业的PS标准差_PIT时间序列 -> getValStDpsSwSeries


# 获取所属申万一级行业的PS标准差_PIT -> getValStDpsSw


# 获取一致预测每股收益(FY1)标准差_PIT时间序列 -> getWestStdEpsFy1Series


# 获取一致预测每股收益(FY1)标准差_PIT -> getWestStdEpsFy1


# 获取过去1个月的日收益率的最大值_PIT时间序列 -> getTechRevs1MMaxSeries


# 获取过去1个月的日收益率的最大值_PIT -> getTechRevs1MMax


# 获取当前股价/过去1个月股价均值-1_PIT时间序列 -> getTechPrice1MSeries


# 获取当前股价/过去1个月股价均值-1_PIT -> getTechPrice1M


# 获取当前股价/过去3个月股价均值-1_PIT时间序列 -> getTechPrice3MSeries


# 获取当前股价/过去3个月股价均值-1_PIT -> getTechPrice3M


# 获取当前股价/过去1年的股价均值-1_PIT时间序列 -> getTechPrice1YSeries


# 获取当前股价/过去1年的股价均值-1_PIT -> getTechPrice1Y


# 获取12M收益率的120D变化率_PIT时间序列 -> getTechRevs12M6MSeries


# 获取12M收益率的120D变化率_PIT -> getTechRevs12M6M


# 获取VMACD的中间变量VDEA_PIT时间序列 -> getTechVDeASeries


# 获取VMACD的中间变量VDEA_PIT -> getTechVDeA


# 获取上涨的股票占指数成份股的比例_PIT时间序列 -> getTechUpPctSeries


# 获取上涨的股票占指数成份股的比例_PIT -> getTechUpPct


# 获取下跌的股票占指数成份股的比例_PIT时间序列 -> getTechDownPctSeries


# 获取下跌的股票占指数成份股的比例_PIT -> getTechDownPct


# 获取涨停的股票占指数成份股的比例_PIT时间序列 -> getTechLimitUpPctSeries


# 获取涨停的股票占指数成份股的比例_PIT -> getTechLimitUpPct


# 获取跌停的股票占指数成份股的比例_PIT时间序列 -> getTechLimitDownPctSeries


# 获取跌停的股票占指数成份股的比例_PIT -> getTechLimitDownPct


# 获取市盈率PE/过去一个月PE的均值_PIT时间序列 -> getValPeToHist20Series


# 获取市盈率PE/过去一个月PE的均值_PIT -> getValPeToHist20


# 获取市盈率PE/过去三个月PE的均值_PIT时间序列 -> getValPeToHist60Series


# 获取市盈率PE/过去三个月PE的均值_PIT -> getValPeToHist60


# 获取市盈率PE/过去六个月PE的均值_PIT时间序列 -> getValPeToHist120Series


# 获取市盈率PE/过去六个月PE的均值_PIT -> getValPeToHist120


# 获取所属申万一级行业的PCF标准差_PIT时间序列 -> getValStdPcfSwSeries


# 获取所属申万一级行业的PCF标准差_PIT -> getValStdPcfSw


# 获取VMACD的中间变量VDIFF_PIT时间序列 -> getTechVDiffSeries


# 获取VMACD的中间变量VDIFF_PIT -> getTechVDiff


# 获取威廉变异离散量(WVAD)6日均值_PIT时间序列 -> getTechMawVAdSeries


# 获取威廉变异离散量(WVAD)6日均值_PIT -> getTechMawVAd


# 获取一致预测每股收益(FY1)变化率_1M_PIT时间序列 -> getWestEpsFy11MSeries


# 获取一致预测每股收益(FY1)变化率_1M_PIT -> getWestEpsFy11M


# 获取一致预测每股收益(FY1)变化率_3M_PIT时间序列 -> getWestEpsFy13MSeries


# 获取一致预测每股收益(FY1)变化率_3M_PIT -> getWestEpsFy13M


# 获取一致预测每股收益(FY1)变化率_6M_PIT时间序列 -> getWestEpsFy16MSeries


# 获取一致预测每股收益(FY1)变化率_6M_PIT -> getWestEpsFy16M


# 获取一致预测每股收益(FY1)的变化_1M_PIT时间序列 -> getWestEpsFy1Chg1MSeries


# 获取一致预测每股收益(FY1)的变化_1M_PIT -> getWestEpsFy1Chg1M


# 获取一致预测每股收益(FY1)的变化_3M_PIT时间序列 -> getWestEpsFy1Chg3MSeries


# 获取一致预测每股收益(FY1)的变化_3M_PIT -> getWestEpsFy1Chg3M


# 获取一致预测每股收益(FY1)的变化_6M_PIT时间序列 -> getWestEpsFy1Chg6MSeries


# 获取一致预测每股收益(FY1)的变化_6M_PIT -> getWestEpsFy1Chg6M


# 获取过去6个月的动量-过去1个月的动量_PIT时间序列 -> getTechRevs6M20Series


# 获取过去6个月的动量-过去1个月的动量_PIT -> getTechRevs6M20


# 获取过去12个月的动量-过去1个月的动量_PIT时间序列 -> getTechRevs12M20Series


# 获取过去12个月的动量-过去1个月的动量_PIT -> getTechRevs12M20


# 获取所属申万一级行业的账面市值比行业均值_PIT时间序列 -> getValAvgBToMvSwSeries


# 获取所属申万一级行业的账面市值比行业均值_PIT -> getValAvgBToMvSw


# 获取1-过去一个月收益率排名/股票总数的比值_PIT时间序列 -> getTechRank1MSeries


# 获取1-过去一个月收益率排名/股票总数的比值_PIT -> getTechRank1M


# 获取所属申万一级行业的账面市值比行业标准差_PIT时间序列 -> getValStDbToMvSwSeries


# 获取所属申万一级行业的账面市值比行业标准差_PIT -> getValStDbToMvSw


# 获取过去5日的价格动量-过去1个月的价格动量_PIT时间序列 -> getTechRevs5M20Series


# 获取过去5日的价格动量-过去1个月的价格动量_PIT -> getTechRevs5M20


# 获取过去5日的价格动量-过去3个月的价格动量_PIT时间序列 -> getTechRevs5M60Series


# 获取过去5日的价格动量-过去3个月的价格动量_PIT -> getTechRevs5M60


# 获取过去1个月交易量/过去3个月的平均交易量_PIT时间序列 -> getTechVolume1M60Series


# 获取过去1个月交易量/过去3个月的平均交易量_PIT -> getTechVolume1M60


# 获取与过去1 个月、3个月、6 个月、12 个月股价平均涨幅_PIT时间序列 -> getTechChgAvgSeries


# 获取与过去1 个月、3个月、6 个月、12 个月股价平均涨幅_PIT -> getTechChgAvg


# 获取当前交易量/过去1个月日均交易量*过去一个月的收益率_PIT时间序列 -> getTechVolUmN1MSeries


# 获取当前交易量/过去1个月日均交易量*过去一个月的收益率_PIT -> getTechVolUmN1M


# 获取第N名持有人持有份额时间序列 -> getFundHolderHoldingSeries


# 获取第N名持有人持有份额 -> getFundHolderHolding


# 获取第N名持有人持有份额(上市公告)时间序列 -> getFundHolderHoldingListingSeries


# 获取第N名持有人持有份额(上市公告) -> getFundHolderHoldingListing


# 获取第N名持有人类别(货币)时间序列 -> getFundHolderNameMmFSeries


# 获取第N名持有人类别(货币) -> getFundHolderNameMmF


# 获取第N名持有人持有份额(货币)时间序列 -> getFundHolderHoldingMmFSeries


# 获取第N名持有人持有份额(货币) -> getFundHolderHoldingMmF


# 获取是否FOF基金时间序列 -> getFundFOfFundOrNotSeries


# 获取是否FOF基金 -> getFundFOfFundOrNot


# 获取Wind产品类型时间序列 -> getFundProdTypeWindSeries


# 获取Wind产品类型 -> getFundProdTypeWind


# 获取关联ETFWind代码时间序列 -> getFundEtFWindCodeSeries


# 获取关联ETFWind代码 -> getFundEtFWindCode


# 获取ETF关联联接基金代码时间序列 -> getFundEtFFeederCodeSeries


# 获取ETF关联联接基金代码 -> getFundEtFFeederCode


# 获取ETF网上现金认购起始日时间序列 -> getFundNetworkCashBuyStartDateSeries


# 获取ETF网上现金认购起始日 -> getFundNetworkCashBuyStartDate


# 获取ETF网上现金认购截止日时间序列 -> getFundNetworkCashBuyEnddateSeries


# 获取ETF网上现金认购截止日 -> getFundNetworkCashBuyEnddate


# 获取ETF网上现金认购份额下限时间序列 -> getFundNetworkCashBuyShareDownLimitSeries


# 获取ETF网上现金认购份额下限 -> getFundNetworkCashBuyShareDownLimit


# 获取ETF网上现金认购份额上限时间序列 -> getFundNetworkCashBuyShareUpLimitSeries


# 获取ETF网上现金认购份额上限 -> getFundNetworkCashBuyShareUpLimit


# 获取ETF网下现金认购起始日时间序列 -> getFundOffNetworkBuyStartDateSeries


# 获取ETF网下现金认购起始日 -> getFundOffNetworkBuyStartDate


# 获取ETF网下现金认购截止日时间序列 -> getFundOffNetworkBuyEnddateSeries


# 获取ETF网下现金认购截止日 -> getFundOffNetworkBuyEnddate


# 获取ETF网下现金认购份额下限时间序列 -> getFundOffNetworkCashBuyShareDownLimitSeries


# 获取ETF网下现金认购份额下限 -> getFundOffNetworkCashBuyShareDownLimit


# 获取ETF网下股票认购起始日时间序列 -> getFundOffNetworkStockBuyStartDateSeries


# 获取ETF网下股票认购起始日 -> getFundOffNetworkStockBuyStartDate


# 获取ETF网下股票认购截止日时间序列 -> getFundOffNetworkStockBuyEnddateSeries


# 获取ETF网下股票认购截止日 -> getFundOffNetworkStockBuyEnddate


# 获取ETF网下股票认购份额下限时间序列 -> getFundOffNetworkStockBuyShareDownLimitSeries


# 获取ETF网下股票认购份额下限 -> getFundOffNetworkStockBuyShareDownLimit


# 获取ETF申购赎回现金差额时间序列 -> getFundEtFPrCashBalanceSeries


# 获取ETF申购赎回现金差额 -> getFundEtFPrCashBalance


# 获取ETF申购赎回最小申购赎回单位时间序列 -> getFundEtFPrMinnaVSeries


# 获取ETF申购赎回最小申购赎回单位 -> getFundEtFPrMinnaV


# 获取ETF申购赎回预估现金部分时间序列 -> getFundEtFPrEstCashSeries


# 获取ETF申购赎回预估现金部分 -> getFundEtFPrEstCash


# 获取ETF申购赎回现金替代比例上限(%)时间序列 -> getFundEtFPrCashRatioSeries


# 获取ETF申购赎回现金替代比例上限(%) -> getFundEtFPrCashRatio


# 获取ETF申赎清单申购上限时间序列 -> getFundEtFPrMaxPurchaseSeries


# 获取ETF申赎清单申购上限 -> getFundEtFPrMaxPurchase


# 获取ETF申赎清单赎回上限时间序列 -> getFundEtFPrMinRedemptionSeries


# 获取ETF申赎清单赎回上限 -> getFundEtFPrMinRedemption


# 获取银行理财风险等级(Wind)时间序列 -> getFundLcRiskLevelWindSeries


# 获取银行理财风险等级(Wind) -> getFundLcRiskLevelWind


# 获取未交税金_FUND时间序列 -> getStmBs127Series


# 获取未交税金_FUND -> getStmBs127


# 获取应付收益_FUND时间序列 -> getStmBs30Series


# 获取应付收益_FUND -> getStmBs30


# 获取实收基金_FUND时间序列 -> getStmBs34Series


# 获取实收基金_FUND -> getStmBs34


# 获取收入合计_FUND时间序列 -> getStmIs10Series


# 获取收入合计_FUND -> getStmIs10


# 获取股利收益_FUND时间序列 -> getStmIs4Series


# 获取股利收益_FUND -> getStmIs4


# 获取汇兑收入_FUND时间序列 -> getStmIs77Series


# 获取汇兑收入_FUND -> getStmIs77


# 获取费用合计_FUND时间序列 -> getStmIs22Series


# 获取费用合计_FUND -> getStmIs22


# 获取交易费用_FUND时间序列 -> getStmIs73Series


# 获取交易费用_FUND -> getStmIs73


# 获取审计费用_FUND时间序列 -> getStmIs19Series


# 获取审计费用_FUND -> getStmIs19


# 获取应收申购款_FUND时间序列 -> getStmBs14Series


# 获取应收申购款_FUND -> getStmBs14


# 获取应付赎回款_FUND时间序列 -> getStmBs26Series


# 获取应付赎回款_FUND -> getStmBs26


# 获取基金管理费_FUND时间序列 -> getStmIs11Series


# 获取基金管理费_FUND -> getStmIs11


# 获取客户维护费_FUND时间序列 -> getStmIs74Series


# 获取客户维护费_FUND -> getStmIs74


# 获取基金托管费_FUND时间序列 -> getStmIs12Series


# 获取基金托管费_FUND -> getStmIs12


# 获取应付交易费用_FUND时间序列 -> getStmBs24Series


# 获取应付交易费用_FUND -> getStmBs24


# 获取衍生工具收益_FUND时间序列 -> getStmIs29Series


# 获取衍生工具收益_FUND -> getStmIs29


# 获取应收证券清算款_FUND时间序列 -> getStmBs10Series


# 获取应收证券清算款_FUND -> getStmBs10


# 获取卖出回购证券款_FUND时间序列 -> getStmBs28Series


# 获取卖出回购证券款_FUND -> getStmBs28


# 获取应付证券清算款_FUND时间序列 -> getStmBs22Series


# 获取应付证券清算款_FUND -> getStmBs22


# 获取应付基金管理费_FUND时间序列 -> getStmBs20Series


# 获取应付基金管理费_FUND -> getStmBs20


# 获取应付基金托管费_FUND时间序列 -> getStmBs21Series


# 获取应付基金托管费_FUND -> getStmBs21


# 获取应付销售服务费_FUND时间序列 -> getStmBs153Series


# 获取应付销售服务费_FUND -> getStmBs153


# 获取持有人权益合计_FUND时间序列 -> getStmBs38Series


# 获取持有人权益合计_FUND -> getStmBs38


# 获取基金销售服务费_FUND时间序列 -> getStmIs16Series


# 获取基金销售服务费_FUND -> getStmIs16


# 获取重仓基金Wind代码时间序列 -> getPrtTopFundWindCodeSeries


# 获取重仓基金Wind代码 -> getPrtTopFundWindCode


# 获取国家/地区投资市值(QDII)时间序列 -> getPrtQdIiCountryRegionInvestmentSeries


# 获取国家/地区投资市值(QDII) -> getPrtQdIiCountryRegionInvestment


# 获取Wind代码时间序列 -> getWindCodeSeries


# 获取Wind代码 -> getWindCode


# 获取指数分类(Wind)时间序列 -> getWindTypeSeries


# 获取指数分类(Wind) -> getWindType


# 获取Wind债券一级分类时间序列 -> getWindL1TypeSeries


# 获取Wind债券一级分类 -> getWindL1Type


# 获取Wind债券二级分类时间序列 -> getWindL2TypeSeries


# 获取Wind债券二级分类 -> getWindL2Type


# 获取同公司可转债Wind代码时间序列 -> getCbWindCodeSeries


# 获取同公司可转债Wind代码 -> getCbWindCode


# 获取所属Wind行业名称时间序列 -> getIndustryGicSSeries


# 获取所属Wind行业名称 -> getIndustryGicS


# 获取所属Wind行业代码时间序列 -> getIndustryGicSCodeSeries


# 获取所属Wind行业代码 -> getIndustryGicSCode


# 获取Wind自定义代码时间序列 -> getPreWindCodeSeries


# 获取Wind自定义代码 -> getPreWindCode


# 获取同公司GDRWind代码时间序列 -> getGdrWindCodeSeries


# 获取同公司GDRWind代码 -> getGdrWindCode


# 获取证券曾用Wind代码时间序列 -> getPreCodeSeries


# 获取证券曾用Wind代码 -> getPreCode


# 获取同公司港股Wind代码时间序列 -> getHshAreCodeSeries


# 获取同公司港股Wind代码 -> getHshAreCode


# 获取同公司A股Wind代码时间序列 -> getAShareWindCodeSeries


# 获取同公司A股Wind代码 -> getAShareWindCode


# 获取同公司B股Wind代码时间序列 -> getBShareWindCodeSeries


# 获取同公司B股Wind代码 -> getBShareWindCode


# 获取同公司美股Wind代码时间序列 -> getUsShareWindCodeSeries


# 获取同公司美股Wind代码 -> getUsShareWindCode


# 获取Wind3年评级时间序列 -> getRatingWind3YSeries


# 获取Wind3年评级 -> getRatingWind3Y


# 获取Wind5年评级时间序列 -> getRatingWind5YSeries


# 获取Wind5年评级 -> getRatingWind5Y


# 获取(停止)Wind1年评级时间序列 -> getRatingWind1YSeries


# 获取(停止)Wind1年评级 -> getRatingWind1Y


# 获取(停止)Wind2年评级时间序列 -> getRatingWind2YSeries


# 获取(停止)Wind2年评级 -> getRatingWind2Y


# 获取重仓行业投资市值(Wind全球行业)时间序列 -> getPrtTopGicSIndustryValueSeries


# 获取重仓行业投资市值(Wind全球行业) -> getPrtTopGicSIndustryValue


# 获取基础证券Wind代码时间序列 -> getUnderlyingWindCode2Series


# 获取基础证券Wind代码 -> getUnderlyingWindCode2


# 获取所属Wind行业指数代码时间序列 -> getIndexCodeWindSeries


# 获取所属Wind行业指数代码 -> getIndexCodeWind


# 获取所属Wind行业指数代码(港股)时间序列 -> getIndexCodeWindHkSeries


# 获取所属Wind行业指数代码(港股) -> getIndexCodeWindHk


# 获取所属Wind主题行业指数代码时间序列 -> getIndexCodeWindThematicSeries


# 获取所属Wind主题行业指数代码 -> getIndexCodeWindThematic


# 获取标的Wind代码时间序列 -> getUnderlyingWindCodeSeries


# 获取标的Wind代码 -> getUnderlyingWindCode


# 获取Wind ESG评级时间序列 -> getEsGRatingWindSeries


# 获取Wind ESG评级 -> getEsGRatingWind


# 获取重仓债券Wind代码时间序列 -> getPrtTopBondWindCodeSeries


# 获取重仓债券Wind代码 -> getPrtTopBondWindCode


# 获取重仓股股票Wind代码时间序列 -> getPrtTopStockWindCodeSeries


# 获取重仓股股票Wind代码 -> getPrtTopStockWindCode


# 获取ESG管理实践得分时间序列 -> getEsGMGmtScoreWindSeries


# 获取ESG管理实践得分 -> getEsGMGmtScoreWind


# 获取ESG争议事件得分时间序列 -> getEsGEventScoreWindSeries


# 获取ESG争议事件得分 -> getEsGEventScoreWind


# 获取所属Wind主题行业名称时间序列 -> getThematicIndustryWindSeries


# 获取所属Wind主题行业名称 -> getThematicIndustryWind


# 获取重仓行业投资市值(Wind)时间序列 -> getPrtTopIndustryValueWindSeries


# 获取重仓行业投资市值(Wind) -> getPrtTopIndustryValueWind


# 获取价格算到期收益率(BC1)时间序列 -> getCalcYieldSeries


# 获取价格算到期收益率(BC1) -> getCalcYield


# 获取每股经营现金净流量_GSD时间序列 -> getWgsDOcFpsSeries


# 获取每股经营现金净流量_GSD -> getWgsDOcFps


# 获取每股派息_GSD时间序列 -> getWgsDDpsSeries


# 获取每股派息_GSD -> getWgsDDps


# 获取每股收益-最新股本摊薄_GSD时间序列 -> getWgsDEpsAdjust2Series


# 获取每股收益-最新股本摊薄_GSD -> getWgsDEpsAdjust2


# 获取每股收益-期末股本摊薄_GSD时间序列 -> getWgsDEpsDiluted3Series


# 获取每股收益-期末股本摊薄_GSD -> getWgsDEpsDiluted3


# 获取投入资本回报率_GSD时间序列 -> getWgsDRoiCSeries


# 获取投入资本回报率_GSD -> getWgsDRoiC


# 获取投入资本回报率(年化)_GSD时间序列 -> getWgsDRoiCYearlySeries


# 获取投入资本回报率(年化)_GSD -> getWgsDRoiCYearly


# 获取投入资本回报率ROIC_GSD时间序列 -> getWgsDRoiC1Series


# 获取投入资本回报率ROIC_GSD -> getWgsDRoiC1


# 获取权益性投资_GSD时间序列 -> getWgsDInvestEqSeries


# 获取权益性投资_GSD -> getWgsDInvestEq


# 获取可供出售投资_GSD时间序列 -> getWgsDInvestAFsSeries


# 获取可供出售投资_GSD -> getWgsDInvestAFs


# 获取抵押担保证券_GSD时间序列 -> getWgsDSecCollaSeries


# 获取抵押担保证券_GSD -> getWgsDSecColla


# 获取客户贷款及垫款净额_GSD时间序列 -> getWgsDLoansNetSeries


# 获取客户贷款及垫款净额_GSD -> getWgsDLoansNet


# 获取可供出售贷款_GSD时间序列 -> getWgsDLoansHfSSeries


# 获取可供出售贷款_GSD -> getWgsDLoansHfS


# 获取递延保单获得成本_GSD时间序列 -> getWgsDDefPlcYAcqCostsSeries


# 获取递延保单获得成本_GSD -> getWgsDDefPlcYAcqCosts


# 获取应收再保_GSD时间序列 -> getWgsDRecEivReInSurSeries


# 获取应收再保_GSD -> getWgsDRecEivReInSur


# 获取其它应收款_GSD时间序列 -> getWgsDRecEivStOThSeries


# 获取其它应收款_GSD -> getWgsDRecEivStOTh


# 获取抵押贷款与票据净额_GSD时间序列 -> getWgsDLoansMtGNetSeries


# 获取抵押贷款与票据净额_GSD -> getWgsDLoansMtGNet


# 获取应交税金_GSD时间序列 -> getWgsDPayTaxSeries


# 获取应交税金_GSD -> getWgsDPayTax


# 获取短期借贷及长期借贷当期到期部分_GSD时间序列 -> getWgsDDebtStSeries


# 获取短期借贷及长期借贷当期到期部分_GSD -> getWgsDDebtSt


# 获取长期借贷_GSD时间序列 -> getWgsDDebtLtSeries


# 获取长期借贷_GSD -> getWgsDDebtLt


# 获取总存款_GSD时间序列 -> getWgsDDepositsSeries


# 获取总存款_GSD -> getWgsDDeposits


# 获取抵押担保融资_GSD时间序列 -> getWgsDFinCollaSeries


# 获取抵押担保融资_GSD -> getWgsDFinColla


# 获取应付再保_GSD时间序列 -> getWgsDPayReInSurSeries


# 获取应付再保_GSD -> getWgsDPayReInSur


# 获取普通股股本_GSD时间序列 -> getWgsDComEqParSeries


# 获取普通股股本_GSD -> getWgsDComEqPar


# 获取储备_GSD时间序列 -> getWgsDRsvSeries


# 获取储备_GSD -> getWgsDRsv


# 获取股本溢价_GSD时间序列 -> getWgsDAPicSeries


# 获取股本溢价_GSD -> getWgsDAPic


# 获取普通股权益总额_GSD时间序列 -> getWgsDComEqPahOlderSeries


# 获取普通股权益总额_GSD -> getWgsDComEqPahOlder


# 获取归属母公司股东权益_GSD时间序列 -> getWgsDComEqSeries


# 获取归属母公司股东权益_GSD -> getWgsDComEq


# 获取股东权益合计_GSD时间序列 -> getWgsDStKhlDrSEqSeries


# 获取股东权益合计_GSD -> getWgsDStKhlDrSEq


# 获取主营收入_GSD时间序列 -> getWgsDSalesOperSeries


# 获取主营收入_GSD -> getWgsDSalesOper


# 获取共同发展公司损益_GSD时间序列 -> getWgsDGainJointlyControlledSeries


# 获取共同发展公司损益_GSD -> getWgsDGainJointlyControlled


# 获取员工薪酬_GSD时间序列 -> getWgsDEMplBenSeries


# 获取员工薪酬_GSD -> getWgsDEMplBen


# 获取交易账户净收入_GSD时间序列 -> getWgsDTradeIncNetSeries


# 获取交易账户净收入_GSD -> getWgsDTradeIncNet


# 获取利息及股息收入_GSD时间序列 -> getWgsDIntInverStIncSeries


# 获取利息及股息收入_GSD -> getWgsDIntInverStInc


# 获取已发生赔款净额_GSD时间序列 -> getWgsDClaimIncurredSeries


# 获取已发生赔款净额_GSD -> getWgsDClaimIncurred


# 获取毛承保保费及保单费收入_GSD时间序列 -> getWgsDPremiumGrossSeries


# 获取毛承保保费及保单费收入_GSD -> getWgsDPremiumGross


# 获取保单持有人利益_GSD时间序列 -> getWgsDPolicyHlDrBenSeries


# 获取保单持有人利益_GSD -> getWgsDPolicyHlDrBen


# 获取保单获取成本和承保费用_GSD时间序列 -> getWgsDCostPolicyAcquisitionSeries


# 获取保单获取成本和承保费用_GSD -> getWgsDCostPolicyAcquisition


# 获取扣除贷款损失准备前收入_GSD时间序列 -> getWgsDRevComMIncSeries


# 获取扣除贷款损失准备前收入_GSD -> getWgsDRevComMInc


# 获取经纪佣金收入_GSD时间序列 -> getWgsDBrokerComMIncSeries


# 获取经纪佣金收入_GSD -> getWgsDBrokerComMInc


# 获取承销与投资银行费收入_GSD时间序列 -> getWgsDUwIbIncSeries


# 获取承销与投资银行费收入_GSD -> getWgsDUwIbInc


# 获取租金收入_GSD时间序列 -> getWgsDRevRentSeries


# 获取租金收入_GSD -> getWgsDRevRent


# 获取房地产销售收入_GSD时间序列 -> getWgsDGainSaleRealEstateSeries


# 获取房地产销售收入_GSD -> getWgsDGainSaleRealEstate


# 获取抵押贷款相关收入_GSD时间序列 -> getWgsDMtGIncSeries


# 获取抵押贷款相关收入_GSD -> getWgsDMtGInc


# 获取销售、行政及一般费用_GSD时间序列 -> getWgsDSgaExpSeries


# 获取销售、行政及一般费用_GSD -> getWgsDSgaExp


# 获取贷款损失准备_GSD时间序列 -> getWgsDProvLoanLossSeries


# 获取贷款损失准备_GSD -> getWgsDProvLoanLoss


# 获取手续费及佣金开支_GSD时间序列 -> getWgsDFeeComMExpSeries


# 获取手续费及佣金开支_GSD -> getWgsDFeeComMExp


# 获取权益性投资损益_GSD时间序列 -> getWgsDInvestGainSeries


# 获取权益性投资损益_GSD -> getWgsDInvestGain


# 获取材料及相关费用_GSD时间序列 -> getWgsDExpMaterialsSeries


# 获取材料及相关费用_GSD -> getWgsDExpMaterials


# 获取非经常项目前利润_GSD时间序列 -> getWgsDEBtExClUnusualItemsSeries


# 获取非经常项目前利润_GSD -> getWgsDEBtExClUnusualItems


# 获取非经常项目损益_GSD时间序列 -> getWgsDUnusualItemsSeries


# 获取非经常项目损益_GSD -> getWgsDUnusualItems


# 获取除税前利润_GSD时间序列 -> getWgsDIncPreTaxSeries


# 获取除税前利润_GSD -> getWgsDIncPreTax


# 获取除税后利润_GSD时间序列 -> getWgsDNetProfitIsSeries


# 获取除税后利润_GSD -> getWgsDNetProfitIs


# 获取折旧及摊销_GSD时间序列 -> getWgsDDaSeries


# 获取折旧及摊销_GSD -> getWgsDDa


# 获取联营公司损益_GSD时间序列 -> getWgsDGainAssociatesSeries


# 获取联营公司损益_GSD -> getWgsDGainAssociates


# 获取折旧与摊销_GSD时间序列 -> getWgsDDepExpCfSeries


# 获取折旧与摊销_GSD -> getWgsDDepExpCf


# 获取资本性支出_GSD时间序列 -> getWgsDCapeXFfSeries


# 获取资本性支出_GSD -> getWgsDCapeXFf


# 获取投资增加_GSD时间序列 -> getWgsDInvestPUrchCfSeries


# 获取投资增加_GSD -> getWgsDInvestPUrchCf


# 获取投资减少_GSD时间序列 -> getWgsDInvestSaleCfSeries


# 获取投资减少_GSD -> getWgsDInvestSaleCf


# 获取债务增加_GSD时间序列 -> getWgsDDebtIsSCfSeries


# 获取债务增加_GSD -> getWgsDDebtIsSCf


# 获取债务减少_GSD时间序列 -> getWgsDDebtReDuctCfSeries


# 获取债务减少_GSD -> getWgsDDebtReDuctCf


# 获取股本增加_GSD时间序列 -> getWgsDStKPUrchCfSeries


# 获取股本增加_GSD -> getWgsDStKPUrchCf


# 获取股本减少_GSD时间序列 -> getWgsDStKSaleCfSeries


# 获取股本减少_GSD -> getWgsDStKSaleCf


# 获取支付的股利合计_GSD时间序列 -> getWgsDDivCfSeries


# 获取支付的股利合计_GSD -> getWgsDDivCf


# 获取汇率变动影响_GSD时间序列 -> getWgsDForExChCfSeries


# 获取汇率变动影响_GSD -> getWgsDForExChCf


# 获取单季度.主营收入_GSD时间序列 -> getWgsDQfaSalesOperSeries


# 获取单季度.主营收入_GSD -> getWgsDQfaSalesOper


# 获取单季度.共同发展公司损益_GSD时间序列 -> getWgsDQfaGainJointlyControlledSeries


# 获取单季度.共同发展公司损益_GSD -> getWgsDQfaGainJointlyControlled


# 获取单季度.员工薪酬_GSD时间序列 -> getWgsDQfaEMplBenSeries


# 获取单季度.员工薪酬_GSD -> getWgsDQfaEMplBen


# 获取单季度.折旧及摊销_GSD时间序列 -> getWgsDQfaDaSeries


# 获取单季度.折旧及摊销_GSD -> getWgsDQfaDa


# 获取单季度.权益性投资损益_GSD时间序列 -> getWgsDQfaInvestGainSeries


# 获取单季度.权益性投资损益_GSD -> getWgsDQfaInvestGain


# 获取单季度.材料及相关费用_GSD时间序列 -> getWgsDQfaExpMaterialsSeries


# 获取单季度.材料及相关费用_GSD -> getWgsDQfaExpMaterials


# 获取单季度.联营公司损益_GSD时间序列 -> getWgsDQfaGainAssociatesSeries


# 获取单季度.联营公司损益_GSD -> getWgsDQfaGainAssociates


# 获取单季度.销售、行政及一般费用_GSD时间序列 -> getWgsDQfaSgaExpSeries


# 获取单季度.销售、行政及一般费用_GSD -> getWgsDQfaSgaExp


# 获取单季度.除税前利润_GSD时间序列 -> getWgsDQfaIncPreTaxSeries


# 获取单季度.除税前利润_GSD -> getWgsDQfaIncPreTax


# 获取单季度.非经常项目前利润_GSD时间序列 -> getWgsDQfaEBtExClUnusualItemsSeries


# 获取单季度.非经常项目前利润_GSD -> getWgsDQfaEBtExClUnusualItems


# 获取单季度.非经常项目损益_GSD时间序列 -> getWgsDQfaUnusualItemsSeries


# 获取单季度.非经常项目损益_GSD -> getWgsDQfaUnusualItems


# 获取单季度.交易账户净收入_GSD时间序列 -> getWgsDQfaTradeIncNetSeries


# 获取单季度.交易账户净收入_GSD -> getWgsDQfaTradeIncNet


# 获取单季度.手续费及佣金开支_GSD时间序列 -> getWgsDQfaFeeComMExpSeries


# 获取单季度.手续费及佣金开支_GSD -> getWgsDQfaFeeComMExp


# 获取单季度.扣除贷款损失准备前收入_GSD时间序列 -> getWgsDQfaRevComMIncSeries


# 获取单季度.扣除贷款损失准备前收入_GSD -> getWgsDQfaRevComMInc


# 获取单季度.保单持有人利益_GSD时间序列 -> getWgsDQfaPolicyHlDrBenSeries


# 获取单季度.保单持有人利益_GSD -> getWgsDQfaPolicyHlDrBen


# 获取单季度.保单获取成本和承保费用_GSD时间序列 -> getWgsDQfaCostPolicyAcquisitionSeries


# 获取单季度.保单获取成本和承保费用_GSD -> getWgsDQfaCostPolicyAcquisition


# 获取单季度.利息及股息收入_GSD时间序列 -> getWgsDQfaIntInverStIncSeries


# 获取单季度.利息及股息收入_GSD -> getWgsDQfaIntInverStInc


# 获取单季度.已发生赔款净额_GSD时间序列 -> getWgsDQfaClaimIncurredSeries


# 获取单季度.已发生赔款净额_GSD -> getWgsDQfaClaimIncurred


# 获取单季度.毛承保保费及保单费收入_GSD时间序列 -> getWgsDQfaPremiumGrossSeries


# 获取单季度.毛承保保费及保单费收入_GSD -> getWgsDQfaPremiumGross


# 获取单季度.房地产销售收入_GSD时间序列 -> getWgsDQfaGainSaleRealEstateSeries


# 获取单季度.房地产销售收入_GSD -> getWgsDQfaGainSaleRealEstate


# 获取单季度.抵押贷款相关收入_GSD时间序列 -> getWgsDQfaMtGIncSeries


# 获取单季度.抵押贷款相关收入_GSD -> getWgsDQfaMtGInc


# 获取单季度.租金收入_GSD时间序列 -> getWgsDQfaRevRentSeries


# 获取单季度.租金收入_GSD -> getWgsDQfaRevRent


# 获取单季度.经纪佣金收入_GSD时间序列 -> getWgsDQfaBrokerComMIncSeries


# 获取单季度.经纪佣金收入_GSD -> getWgsDQfaBrokerComMInc


# 获取单季度.承销与投资银行费收入_GSD时间序列 -> getWgsDQfaUwIbIncSeries


# 获取单季度.承销与投资银行费收入_GSD -> getWgsDQfaUwIbInc


# 获取单季度.贷款损失准备_GSD时间序列 -> getWgsDQfaProvLoanLossSeries


# 获取单季度.贷款损失准备_GSD -> getWgsDQfaProvLoanLoss


# 获取单季度.折旧与摊销_GSD时间序列 -> getWgsDQfaDepExpCfSeries


# 获取单季度.折旧与摊销_GSD -> getWgsDQfaDepExpCf


# 获取单季度.资本性支出_GSD时间序列 -> getWgsDQfaCapeXFfSeries


# 获取单季度.资本性支出_GSD -> getWgsDQfaCapeXFf


# 获取单季度.投资增加_GSD时间序列 -> getWgsDQfaInvestPUrchCfSeries


# 获取单季度.投资增加_GSD -> getWgsDQfaInvestPUrchCf


# 获取单季度.投资减少_GSD时间序列 -> getWgsDQfaInvestSaleCfSeries


# 获取单季度.投资减少_GSD -> getWgsDQfaInvestSaleCf


# 获取单季度.债务增加_GSD时间序列 -> getWgsDQfaDebtIsSCfSeries


# 获取单季度.债务增加_GSD -> getWgsDQfaDebtIsSCf


# 获取单季度.债务减少_GSD时间序列 -> getWgsDQfaDebtReDuctCfSeries


# 获取单季度.债务减少_GSD -> getWgsDQfaDebtReDuctCf


# 获取单季度.股本增加_GSD时间序列 -> getWgsDQfaStKPUrchCfSeries


# 获取单季度.股本增加_GSD -> getWgsDQfaStKPUrchCf


# 获取单季度.股本减少_GSD时间序列 -> getWgsDQfaStKSaleCfSeries


# 获取单季度.股本减少_GSD -> getWgsDQfaStKSaleCf


# 获取单季度.支付的股利合计_GSD时间序列 -> getWgsDQfaDivCfSeries


# 获取单季度.支付的股利合计_GSD -> getWgsDQfaDivCf


# 获取单季度.汇率变动影响_GSD时间序列 -> getWgsDQfaForExChCfSeries


# 获取单季度.汇率变动影响_GSD -> getWgsDQfaForExChCf


# 获取永续债_合计_GSD时间序列 -> getArdBsPerpetualSeries


# 获取永续债_合计_GSD -> getArdBsPerpetual


# 获取股权激励支出_GSD时间序列 -> getIsSharePaymentsSeries


# 获取股权激励支出_GSD -> getIsSharePayments


# 获取市净率PB(MRQ,海外)时间序列 -> getPbMrQGsDSeries


# 获取市净率PB(MRQ,海外) -> getPbMrQGsD


# 获取现金短债比(公告值)_GSD时间序列 -> getStDebtRatioSeries


# 获取现金短债比(公告值)_GSD -> getStDebtRatio


# 获取永续债_归属于少数股东_GSD时间序列 -> getArdBsPerPMinSeries


# 获取永续债_归属于少数股东_GSD -> getArdBsPerPMin


# 获取永续债_归属于母公司股东_GSD时间序列 -> getArdBsPerPParSeries


# 获取永续债_归属于母公司股东_GSD -> getArdBsPerPPar


# 获取投资物业公允价值变动(公布值)_GSD时间序列 -> getArdIsInvestmentPropertySeries


# 获取投资物业公允价值变动(公布值)_GSD -> getArdIsInvestmentProperty


# 获取一致预测ROE(FY1)时间序列 -> getWestAvgRoeFy1Series


# 获取一致预测ROE(FY1) -> getWestAvgRoeFy1


# 获取一致预测ROE(FY2)时间序列 -> getWestAvgRoeFy2Series


# 获取一致预测ROE(FY2) -> getWestAvgRoeFy2


# 获取一致预测ROE(FY3)时间序列 -> getWestAvgRoeFy3Series


# 获取一致预测ROE(FY3) -> getWestAvgRoeFy3


# 获取一致预测ROE同比时间序列 -> getWestAvgRoeYoYSeries


# 获取一致预测ROE同比 -> getWestAvgRoeYoY


# 获取参考市盈率PE(LYR)时间序列 -> getPelYrRefSeries


# 获取参考市盈率PE(LYR) -> getPelYrRef


# 获取市盈率PE(LYR)时间序列 -> getPeLyRSeries


# 获取市盈率PE(LYR) -> getPeLyR


# 获取市净率PB(LYR)时间序列 -> getPbLyRSeries


# 获取市净率PB(LYR) -> getPbLyR


# 获取市销率PS(LYR)时间序列 -> getPsLyRSeries


# 获取市销率PS(LYR) -> getPsLyR


# 获取PER(LYR)时间序列 -> getValPerSeries


# 获取PER(LYR) -> getValPer


# 获取市盈率PE(LYR,加权)时间序列 -> getValPeWGtSeries


# 获取市盈率PE(LYR,加权) -> getValPeWGt


# 获取市现率PCF(现金净流量LYR)时间序列 -> getPcfNflYrSeries


# 获取市现率PCF(现金净流量LYR) -> getPcfNflYr


# 获取区间最高PS(LYR)时间序列 -> getValPSlyRHighSeries


# 获取区间最高PS(LYR) -> getValPSlyRHigh


# 获取区间最低PS(LYR)时间序列 -> getValPSlyRLowSeries


# 获取区间最低PS(LYR) -> getValPSlyRLow


# 获取区间平均PS(LYR)时间序列 -> getValPSlyRAvgSeries


# 获取区间平均PS(LYR) -> getValPSlyRAvg


# 获取市净率PB(LF,内地)时间序列 -> getPbLfSeries


# 获取市净率PB(LF,内地) -> getPbLf


# 获取区间最高PB(LF)时间序列 -> getValPbHighSeries


# 获取区间最高PB(LF) -> getValPbHigh


# 获取区间最低PB(LF)时间序列 -> getValPbLowSeries


# 获取区间最低PB(LF) -> getValPbLow


# 获取区间平均PB(LF)时间序列 -> getValPbAvgSeries


# 获取区间平均PB(LF) -> getValPbAvg


# 获取发布方市净率PB(LF)时间序列 -> getValPbLfIssuerSeries


# 获取发布方市净率PB(LF) -> getValPbLfIssuer


# 获取一致预测每股股利(FY1)时间序列 -> getWestAvgDpsFy1Series


# 获取一致预测每股股利(FY1) -> getWestAvgDpsFy1


# 获取一致预测每股股利(FY2)时间序列 -> getWestAvgDpsFy2Series


# 获取一致预测每股股利(FY2) -> getWestAvgDpsFy2


# 获取一致预测每股股利(FY3)时间序列 -> getWestAvgDpsFy3Series


# 获取一致预测每股股利(FY3) -> getWestAvgDpsFy3


# 获取一致预测每股现金流(FY1)时间序列 -> getWestAvgCpSFy1Series


# 获取一致预测每股现金流(FY1) -> getWestAvgCpSFy1


# 获取一致预测每股现金流(FY2)时间序列 -> getWestAvgCpSFy2Series


# 获取一致预测每股现金流(FY2) -> getWestAvgCpSFy2


# 获取一致预测每股现金流(FY3)时间序列 -> getWestAvgCpSFy3Series


# 获取一致预测每股现金流(FY3) -> getWestAvgCpSFy3
#
# 获取收盘价(总股本加权平均)板块多维 -> getSecCloseTsWavGWsee


# 获取收盘价(流通股本加权平均)(中国)板块多维 -> getSecCloseFfsWavGChNWsee


# 获取换手率(算术平均)板块多维 -> getSecTurnAvgWsee


# 获取换手率(总市值加权平均)板块多维 -> getSecTurnTMcWavGWsee


# 获取换手率(流通市值加权平均)板块多维 -> getSecTurnFfMcWavGWsee


# 获取区间涨跌幅(算术平均)板块多维 -> getSecPqPctChgAvgWsee


# 获取区间涨跌幅(总市值加权平均)板块多维 -> getSecPqPctChgTMcWavGWsee


# 获取区间涨跌幅(流通市值加权平均)(中国)板块多维 -> getSecPqPctChgFfMcWavGChNWsee


# 获取区间成交量(合计)板块多维 -> getSecPqVolSumWsee


# 获取区间成交金额(合计)板块多维 -> getSecPqAmtSumWsee


# 获取区间换手率(算术平均)板块多维 -> getSecPqTurnAvgWsee


# 获取区间日均换手率(算术平均)板块多维 -> getSecPqAvgTurnAvgWsee


# 获取总股本(合计)板块多维 -> getSecShareTotalSumWsee


# 获取总股本(算术平均)板块多维 -> getSecShareTotalAvgWsee


# 获取流通A股(合计)板块多维 -> getSecShareFloatASumWsee


# 获取流通A股(算术平均)板块多维 -> getSecShareFloatAAvgWsee


# 获取流通B股(合计)板块多维 -> getSecShareFloatBSumWsee


# 获取流通B股(算术平均)板块多维 -> getSecShareFloatBAvgWsee


# 获取流通H股(合计)板块多维 -> getSecShareFloatHSumWsee


# 获取流通H股(算术平均)板块多维 -> getSecShareFloatHAvgWsee


# 获取总流通股本(合计)(中国)板块多维 -> getSecShareFloatTotalSumChNWsee


# 获取总流通股本(算术平均)(中国)板块多维 -> getSecShareFloatTotalAvgChNWsee


# 获取非流通股(合计)(中国)板块多维 -> getSecShareTotalNonLiqSumChNWsee


# 获取非流通股(算术平均)(中国)板块多维 -> getSecShareTotalNonLiqAvgChNWsee


# 获取预测每股收益(整体法)板块多维 -> getSecWestEpsOverallChNWsee


# 获取预测每股收益(算术平均)板块多维 -> getSecWestEpsAvgChNWsee


# 获取预测净利润(合计)板块多维 -> getSecWestNpSumChNWsee


# 获取预测净利润(算术平均)板块多维 -> getSecWestNpAvgChNWsee


# 获取预测主营业务收入(合计)板块多维 -> getSecWestRevenueSumChNWsee


# 获取预测主营业务收入(算术平均)板块多维 -> getSecWestRevenueAvgChNWsee


# 获取(日)净流入资金(合计)板块多维 -> getSecNCashInFlowDSumChNWsee


# 获取(日)净流入资金(算术平均)板块多维 -> getSecNCashInFlowDAvgChNWsee


# 获取(日)净流入量(合计)板块多维 -> getSecNVolInFlowDSumChNWsee


# 获取(日)净流入量(算术平均)板块多维 -> getSecNVolInFlowDAvgChNWsee


# 获取(日)尾盘净流入资金(合计)板块多维 -> getSecNClosingInFlowDSumChNWsee


# 获取(日)尾盘净流入资金(算术平均)板块多维 -> getSecNClosingInFlowDAvgChNWsee


# 获取(日)开盘净流入资金(合计)板块多维 -> getSecNOpeningInFlowDSumChNWsee


# 获取(日)开盘净流入资金(算术平均)板块多维 -> getSecNOpeningInFlowDAvgChNWsee


# 获取(日)金额流入率(整体法)板块多维 -> getSecCInFlowRateDOverallChNWsee


# 获取(日)金额流入率(算术平均)板块多维 -> getSecCInFlowRateDAvgChNWsee


# 获取(日)资金流向占比(整体法)板块多维 -> getSecCashDirectionPecDOverallChNWsee


# 获取(日)资金流向占比(算术平均)板块多维 -> getSecCashDirectionPecDAvgChNWsee


# 获取(区间)净流入资金(合计)板块多维 -> getSecPqNCashInFlowSumChNWsee


# 获取(区间)净流入资金(算术平均)板块多维 -> getSecPqNCashInFlowAvgChNWsee


# 获取(区间)净流入量(合计)板块多维 -> getSecPqNVolInFlowSumChNWsee


# 获取(区间)净流入量(算术平均)板块多维 -> getSecPqNVolInFlowAvgChNWsee


# 获取(区间)尾盘净流入资金(合计)板块多维 -> getSecPqNClosingInFlowSumChNWsee


# 获取(区间)尾盘净流入资金(算术平均)板块多维 -> getSecPqNClosingInFlowAvgChNWsee


# 获取(区间)开盘净流入资金(合计)板块多维 -> getSecPqNOpeningInFlowSumChNWsee


# 获取(区间)开盘净流入资金(算术平均)板块多维 -> getSecPqNOpeningInFlowAvgChNWsee


# 获取(区间)金额流入率(整体法)板块多维 -> getSecPqCInFlowRateOverallChNWsee


# 获取(区间)金额流入率(算术平均)板块多维 -> getSecPqCInFlowRateAvgChNWsee


# 获取(区间)资金流向占比(整体法)板块多维 -> getSecPqCashDirectionPecOverallChNWsee


# 获取(区间)资金流向占比(算术平均)板块多维 -> getSecPqCashDirectionPecAvgChNWsee


# 获取总市值(合计)板块多维 -> getSecMktCapSumGLbWsee


# 获取总市值(算术平均)板块多维 -> getSecMktCapAvgGLbWsee


# 获取总市值2(合计)板块多维 -> getSecMvArdSumGLbWsee


# 获取总市值2(算术平均)板块多维 -> getSecMvArdAvgGLbWsee


# 获取市盈率(TTM-算术平均法)板块多维 -> getSecPeTtMAvgChNWsee


# 获取市盈率(TTM-中值)板块多维 -> getSecPetTmMediaChNWsee


# 获取市盈率(算术平均)板块多维 -> getSecPeAvgChNWsee


# 获取市盈率(中值)板块多维 -> getSecPeMediaChNWsee


# 获取市净率(算术平均)板块多维 -> getSecPbAvgChNWsee


# 获取市净率(中值)板块多维 -> getSecPbMediaChNWsee


# 获取市现率(算术平均)板块多维 -> getSecPcfAvgChNWsee


# 获取市现率(中值)板块多维 -> getSecPcfMediaChNWsee


# 获取市销率(算术平均)板块多维 -> getSecPsAvgChNWsee


# 获取市销率(中值)板块多维 -> getSecPsMediaChNWsee


# 获取市盈率(TTM-整体法)板块多维 -> getSecPeTtMOverallChNWsee


# 获取市净率(整体法)板块多维 -> getSecPbOverallChNWsee


# 获取市现率(整体法)板块多维 -> getSecPcfOverallChNWsee


# 获取市销率(整体法)板块多维 -> getSecPsOverallChNWsee


# 获取当日总市值(合计)板块多维 -> getSecMktCapTodaySumChNWsee


# 获取当日总市值(算术平均)板块多维 -> getSecMktCapTodayAvgChNWsee


# 获取流通A股市值(合计)板块多维 -> getSecMktCapFloatASharesSumChNWsee


# 获取流通A股市值(算术平均)板块多维 -> getSecMktCapFloatASharesAvgChNWsee


# 获取流通B股市值(合计)板块多维 -> getSecMktCapFloatBSharesSumChNWsee


# 获取流通B股市值(算术平均)板块多维 -> getSecMktCapFloatBSharesAvgChNWsee


# 获取自由流通市值(合计)板块多维 -> getSecMktCapFloatFreeSharesSumChNWsee


# 获取自由流通市值(算术平均)板块多维 -> getSecMktCapFloatFreeSharesAvgChNWsee


# 获取年化收益率算术平均(最近100周)板块多维 -> getSecRiskAnnualYeIlD100WAvgChNWsee


# 获取年化收益率算术平均(最近24个月)板块多维 -> getSecRiskAnnualYeIlD24MAvgChNWsee


# 获取年化收益率算术平均(最近60个月)板块多维 -> getSecRiskAnnualYeIlD60MAvgChNWsee


# 获取年化波动率算术平均(最近100周)板块多维 -> getSecRiskStDevYearly100WAvgChNWsee


# 获取年化波动率算术平均(最近24个月)板块多维 -> getSecRiskStDevYearly24MAvgChNWsee


# 获取年化波动率算术平均(最近60个月)板块多维 -> getSecRiskStDevYearly60MAvgChNWsee


# 获取BETA值算术平均(最近100周)板块多维 -> getSecRiskBeta100WAvgChNWsee


# 获取BETA值算术平均(最近24个月)板块多维 -> getSecRiskBeta24MAvgChNWsee


# 获取BETA值算术平均(最近60个月)板块多维 -> getSecRiskBeta60MAvgChNWsee


# 获取上市公司家数板块多维 -> getSecCsrCStatListCompNumChNWsee


# 获取上市公司境内总股本板块多维 -> getSecCsrCStatShareTotalChNWsee


# 获取上市公司境内总市值板块多维 -> getSecCsrCStatMvChNWsee


# 获取市场静态市盈率板块多维 -> getSecCsrCStatPeChNWsee


# 获取市场静态市净率板块多维 -> getSecCsrCStatPbChNWsee


# 获取上市公司境内股本对应的归属母公司净利润TTM板块多维 -> getSecCsrCStatNpTtMChNWsee


# 获取市场滚动市盈率板块多维 -> getSecCsrCStatPeTtMChNWsee


# 获取每股收益EPS-基本(算术平均)板块多维 -> getSecEpsBasic2AvgChNWsee


# 获取每股收益EPS-稀释(算术平均)板块多维 -> getSecEpsDiluted4AvgChNWsee


# 获取每股收益EPS-期末股本摊薄(整体法)板块多维 -> getSecEndingSharesEpsBasic2OverallChNWsee


# 获取每股收益EPS-期末股本摊薄(算术平均)板块多维 -> getSecEndingSharesEpsBasic2AvgChNWsee


# 获取每股净资产(整体法)板块多维 -> getSecBpSOverallChNWsee


# 获取每股净资产(算术平均)板块多维 -> getSecBpSAvgChNWsee


# 获取每股营业总收入(整体法)板块多维 -> getSecGrpSOverallChNWsee


# 获取每股营业总收入(算术平均)板块多维 -> getSecGrpSAvgChNWsee


# 获取每股留存收益(整体法)板块多维 -> getSecRetainedPsOverallChNWsee


# 获取每股留存收益(算术平均)板块多维 -> getSecRetainedPsAvgChNWsee


# 获取每股现金流量净额(整体法)板块多维 -> getSecCfpSOverallChNWsee


# 获取每股现金流量净额(算术平均)板块多维 -> getSecCfpSAvgChNWsee


# 获取每股经营活动产生的现金流量净额(整体法)板块多维 -> getSecOcFps2OverallChNWsee


# 获取每股经营活动产生的现金流量净额(算术平均)板块多维 -> getSecOcFps2AvgChNWsee


# 获取每股息税前利润(算术平均)板块多维 -> getSecEbItPsAvgGLbWsee


# 获取每股企业自由现金流量(整体法)板块多维 -> getSecFcFFpsOverallGLbWsee


# 获取每股企业自由现金流量(算术平均)板块多维 -> getSecFcFFpsAvgGLbWsee


# 获取每股股东自由现金流量(整体法)板块多维 -> getSecFcFEpsOverallGLbWsee


# 获取每股股东自由现金流量(算术平均)板块多维 -> getSecFcFEpsAvgGLbWsee


# 获取净资产收益率-平均(整体法)板块多维 -> getSecRoeAvgOverallChNWsee


# 获取净资产收益率-平均(算术平均)板块多维 -> getSecRoeAvgAvgChNWsee


# 获取净资产收益率-摊薄(整体法)板块多维 -> getSecRoeDilutedOverallChNWsee


# 获取净资产收益率-摊薄(算术平均)板块多维 -> getSecRoeDilutedAvgChNWsee


# 获取扣除非经常损益后的净资产收益率-平均(整体法)板块多维 -> getSecDeductedRoeAvgOverallChNWsee


# 获取扣除非经常损益后的净资产收益率-平均(算术平均)板块多维 -> getSecDeductedRoeAvgAvgChNWsee


# 获取扣除非经常损益后的净资产收益率-摊薄(整体法)板块多维 -> getSecDeductedRoeDilutedOverallChNWsee


# 获取扣除非经常损益后的净资产收益率-摊薄(算术平均)板块多维 -> getSecDeductedRoeDilutedAvgChNWsee


# 获取总资产报酬率(整体法)板块多维 -> getSecRoa2OverallGLbWsee


# 获取总资产报酬率(算术平均)板块多维 -> getSecRoa2AvgGLbWsee


# 获取总资产净利率(整体法)板块多维 -> getSecRoaOverallChNWsee


# 获取总资产净利率(算术平均)板块多维 -> getSecRoaAvgChNWsee


# 获取销售毛利率(整体法)板块多维 -> getSecGrossProfitMarginOverallChNWsee


# 获取销售毛利率(算术平均)板块多维 -> getSecGrossProfitMarginAvgChNWsee


# 获取销售净利率(整体法)板块多维 -> getSecNetProfitMarginOverallChNWsee


# 获取销售净利率(算术平均)板块多维 -> getSecNetProfitMarginAvgChNWsee


# 获取营业总成本/营业总收入(整体法)板块多维 -> getSecGcToGrOverallChNWsee


# 获取营业总成本/营业总收入(算术平均)板块多维 -> getSecGcToGrAvgChNWsee


# 获取营业利润/营业总收入(整体法)板块多维 -> getSecOpToGrOverallChNWsee


# 获取营业利润/营业总收入(算术平均)板块多维 -> getSecOpToGrAvgChNWsee


# 获取净利润/营业总收入(整体法)板块多维 -> getSecDupontNpToSalesOverallChNWsee


# 获取净利润/营业总收入(算术平均)板块多维 -> getSecDupontNpToSalesAvgChNWsee


# 获取销售费用/营业总收入(算术平均)板块多维 -> getSecOperateExpenseToGrAvgChNWsee


# 获取管理费用/营业总收入(算术平均)板块多维 -> getSEcfAAdminExpenseToGrAvgChNWsee


# 获取财务费用/营业总收入(算术平均)板块多维 -> getSecFinaExpenseToGrAvgChNWsee


# 获取息税前利润/营业总收入(算术平均)板块多维 -> getSecDupontEbItToSalesAvgGLbWsee


# 获取EBITDA/营业总收入(整体法)板块多维 -> getSecEbItDatoSalesOverallGLbWsee


# 获取EBITDA/营业总收入(算术平均)板块多维 -> getSecEbItDatoSalesAvgGLbWsee


# 获取投入资本回报率(算术平均)板块多维 -> getSecRoiCAvgGLbWsee


# 获取营业利润/利润总额(算术平均)板块多维 -> getSecOpToEBTAvgGLbWsee


# 获取价值变动净收益/利润总额(算术平均)板块多维 -> getSecInvestIncomeToEBTAvgChNWsee


# 获取所得税/利润总额(算术平均)板块多维 -> getSecTaxToEBTAvgChNWsee


# 获取扣除非经常损益后的净利润/净利润(算术平均)板块多维 -> getSecDeductedProfitToProfitAvgChNWsee


# 获取经营活动净收益/利润总额(算术平均)板块多维 -> getSecOperateIncomeToEBTAvgChNWsee


# 获取经营活动产生的现金流量净额/营业收入(整体法)板块多维 -> getSecOCFToOrOverallChNWsee


# 获取经营活动产生的现金流量净额/营业收入(算术平均)板块多维 -> getSecOCFToOrAvgChNWsee


# 获取经营活动产生的现金流量净额/经营活动净收益(整体法)板块多维 -> getSecOCFToOperateIncomeOverallChNWsee


# 获取经营活动产生的现金流量净额/经营活动净收益(算术平均)板块多维 -> getSecOCFToOperateIncomeAvgChNWsee


# 获取资本支出/折旧和摊销(整体法)板块多维 -> getSecCapitalizedTodaOverallGLbWsee


# 获取资本支出/折旧和摊销(算术平均)板块多维 -> getSecCapitalizedTodaAvgChNWsee


# 获取资产负债率(整体法)板块多维 -> getSecDebtToAssetsOverallChNWsee


# 获取资产负债率(算术平均)板块多维 -> getSecDebtToAssetsAvgChNWsee


# 获取流动资产/总资产(整体法)板块多维 -> getSecCatoAssetsOverallChNWsee


# 获取流动资产/总资产(算术平均)板块多维 -> getSecCatoAssetsAvgChNWsee


# 获取非流动资产/总资产(整体法)板块多维 -> getSecNcaToAssetsOverallChNWsee


# 获取非流动资产/总资产(算术平均)板块多维 -> getSecNcaToAssetsAvgChNWsee


# 获取有形资产/总资产(整体法)板块多维 -> getSecTangibleAssetsToAssetsOverallChNWsee


# 获取有形资产/总资产(算术平均)板块多维 -> getSecTangibleAssetsToAssetsAvgChNWsee


# 获取流动负债/负债合计(整体法)板块多维 -> getSecCurrentDebtToDebtOverallChNWsee


# 获取流动负债/负债合计(算术平均)板块多维 -> getSecCurrentDebtToDebtAvgChNWsee


# 获取非流动负债/负债合计(整体法)板块多维 -> getSecLongDebToDebtOverallChNWsee


# 获取非流动负债/负债合计(算术平均)板块多维 -> getSecLongDebToDebtAvgChNWsee


# 获取流动比率(整体法)板块多维 -> getSecCurrentOverallChNWsee


# 获取流动比率(算术平均)板块多维 -> getSecCurrentAvgChNWsee


# 获取速动比率(整体法)板块多维 -> getSecQuickOverallChNWsee


# 获取速动比率(算术平均)板块多维 -> getSecQuickAvgChNWsee


# 获取归属母公司股东的权益/负债合计(整体法)板块多维 -> getSecEquityToDebtOverallGLbWsee


# 获取归属母公司股东的权益/负债合计(算术平均)板块多维 -> getSecEquityToDebtAvgGLbWsee


# 获取归属母公司股东的权益/带息债务(整体法)板块多维 -> getSecEquityToInterestDebtOverallGLbWsee


# 获取归属母公司股东的权益/带息债务(算术平均)板块多维 -> getSecEquityToInterestDebtAvgGLbWsee


# 获取息税折旧摊销前利润/负债合计(整体法)板块多维 -> getSecEbItDatoDebtOverallGLbWsee


# 获取息税折旧摊销前利润/负债合计(算术平均)板块多维 -> getSecEbItDatoDebtAvgGLbWsee


# 获取经营活动产生的现金流量净额/负债合计(整体法)板块多维 -> getSecOCFToDebtOverallChNWsee


# 获取经营活动产生的现金流量净额/负债合计(算术平均)板块多维 -> getSecOCFToDebtAvgChNWsee


# 获取已获利息倍数(算术平均)板块多维 -> getSecInterestCoverageAvgChNWsee


# 获取存货周转率(整体法)板块多维 -> getSecInvTurnOverallChNWsee


# 获取存货周转率(算术平均)板块多维 -> getSecInvTurnAvgChNWsee


# 获取应收账款周转率(整体法)板块多维 -> getSecArturNOverallChNWsee


# 获取应收账款周转率(算术平均)板块多维 -> getSecArturNAvgChNWsee


# 获取固定资产周转率(整体法)板块多维 -> getSecFaTurnOverallChNWsee


# 获取固定资产周转率(算术平均)板块多维 -> getSecFaTurnAvgChNWsee


# 获取总资产周转率(整体法)板块多维 -> getSecAssetsTurnOverallChNWsee


# 获取总资产周转率(算术平均)板块多维 -> getSecAssetsTurnAvgChNWsee


# 获取营业周期(整体法)板块多维 -> getSecTurnDaysOverallChNWsee


# 获取营业周期(算术平均)板块多维 -> getSecTurnDaysAvgChNWsee


# 获取存货周转天数(整体法)板块多维 -> getSecInvTurnDaysOverallChNWsee


# 获取存货周转天数(算术平均)板块多维 -> getSecInvTurnDaysAvgChNWsee


# 获取应收账款周转天数(整体法)板块多维 -> getSecArturNDaysOverallChNWsee


# 获取应收账款周转天数(算术平均)板块多维 -> getSecArturNDaysAvgChNWsee


# 获取营业总收入(合计)板块多维 -> getSecGrSumChNWsee


# 获取营业总收入(算术平均)板块多维 -> getSecGrAvgChNWsee


# 获取主营收入(合计)板块多维 -> getSecRevenueSumGLbWsee


# 获取主营收入(算术平均)板块多维 -> getSecRevenueAvgGLbWsee


# 获取其他营业收入(合计)板块多维 -> getSecOtherRevenueSumGLbWsee


# 获取其他营业收入(算术平均)板块多维 -> getSecOtherRevenueAvgGLbWsee


# 获取总营业支出(合计)板块多维 -> getSecGcSumGLbWsee


# 获取总营业支出(算术平均)板块多维 -> getSecGcAvgGLbWsee


# 获取营业成本(合计)板块多维 -> getSecOcSumChNWsee


# 获取营业成本(算术平均)板块多维 -> getSecOcAvgChNWsee


# 获取营业开支(合计)板块多维 -> getSecExpenseSumGLbWsee


# 获取营业开支(算术平均)板块多维 -> getSecExpenseAvgGLbWsee


# 获取权益性投资损益(合计)板块多维 -> getSecEquityInvpnLSumGLbWsee


# 获取权益性投资损益(算术平均)板块多维 -> getSecEquityInvpnLAvgGLbWsee


# 获取营业利润(合计)板块多维 -> getSecOpSumChNWsee


# 获取营业利润(算术平均)板块多维 -> getSecOpAvgChNWsee


# 获取除税前利润(合计)板块多维 -> getSecEBtSumGLbWsee


# 获取除税前利润(算术平均)板块多维 -> getSecEBtAvgGLbWsee


# 获取所得税(合计)板块多维 -> getSecTaxSumChNWsee


# 获取所得税(算术平均)板块多维 -> getSecTaxAvgChNWsee


# 获取净利润(合计)板块多维 -> getSecNpSumChNWsee


# 获取净利润(算术平均)板块多维 -> getSecNpAvgChNWsee


# 获取归属普通股东净利润(合计)板块多维 -> getSecNpaSpcSumGLbWsee


# 获取归属普通股东净利润(算术平均)板块多维 -> getSecNpaSpcAvgGLbWsee


# 获取毛利(合计)板块多维 -> getSecGrossMargin2SumChNWsee


# 获取毛利(算术平均)板块多维 -> getSecGrossMargin2AvgChNWsee


# 获取EBIT(合计)板块多维 -> getSecEbItSumGLbWsee


# 获取EBIT(算术平均)板块多维 -> getSecEbItAvgGLbWsee


# 获取资产总计(合计)板块多维 -> getSecAssetTotalSumChNWsee


# 获取资产总计(算术平均)板块多维 -> getSecAssetTotalAvgChNWsee


# 获取现金及现金等价物(合计)板块多维 -> getSecCCeSumGLbWsee


# 获取现金及现金等价物(算术平均)板块多维 -> getSecCCeAvgGLbWsee


# 获取交易性金融资产(合计)板块多维 -> getSecTradingFinancialAssetSumChNWsee


# 获取交易性金融资产(算术平均)板块多维 -> getSecTradingFinancialAssetAvgChNWsee


# 获取应收账款及票据(合计)板块多维 -> getSecArSumGLbWsee


# 获取应收账款及票据(算术平均)板块多维 -> getSecArAvgGLbWsee


# 获取存货(合计)板块多维 -> getSecIvNenTorySumChNWsee


# 获取存货(算术平均)板块多维 -> getSecIvNenToryAvgChNWsee


# 获取流动资产(合计)板块多维 -> getSecCurrentAssetSumChNWsee


# 获取流动资产(算术平均)板块多维 -> getSecCurrentAssetAvgChNWsee


# 获取权益性投资(合计)板块多维 -> getSecEquityInvSumGLbWsee


# 获取权益性投资(算术平均)板块多维 -> getSecEquityInvAvgGLbWsee


# 获取固定资产净值(合计)板块多维 -> getSecFixAssetNetValueSumChNWsee


# 获取固定资产净值(算术平均)板块多维 -> getSecFixAssetNetValueAvgChNWsee


# 获取在建工程(合计)板块多维 -> getSecCIpNetValueSumChNWsee


# 获取在建工程(算术平均)板块多维 -> getSecCIpNetValueAvgChNWsee


# 获取非流动资产(合计)板块多维 -> getSecNonCurrentAssetSumChNWsee


# 获取非流动资产(算术平均)板块多维 -> getSecNonCurrentAssetAvgChNWsee


# 获取应付账款及票据(合计)板块多维 -> getSecApSumGLbWsee


# 获取应付账款及票据(算术平均)板块多维 -> getSecApAvgGLbWsee


# 获取短期借贷及长期借贷当期到期部分(合计)板块多维 -> getSecCurrentMaturityOfBorrowingSSumGLbWsee


# 获取短期借贷及长期借贷当期到期部分(算术平均)板块多维 -> getSecCurrentMaturityOfBorrowingSAvgGLbWsee


# 获取流动负债(合计)板块多维 -> getSecCurrentLiabilitySumChNWsee


# 获取流动负债(算术平均)板块多维 -> getSecCurrentLiabilityAvgChNWsee


# 获取长期借款(合计)板块多维 -> getSecLtDebtSumChNWsee


# 获取长期借款(算术平均)板块多维 -> getSecLtDebtAvgChNWsee


# 获取非流动负债(合计)板块多维 -> getSecNonCurrentLiabilitySumChNWsee


# 获取非流动负债(算术平均)板块多维 -> getSecNonCurrentLiabilityAvgChNWsee


# 获取股东权益(合计)板块多维 -> getSecEquitySumChNWsee


# 获取股东权益(算术平均)板块多维 -> getSecEquityAvgChNWsee


# 获取少数股东权益(合计)板块多维 -> getSecMinorityQuitYSumChNWsee


# 获取少数股东权益(算术平均)板块多维 -> getSecMinorityQuitYAvgChNWsee


# 获取留存收益(合计)板块多维 -> getSecReAtAInEarningSumGLbWsee


# 获取留存收益(算术平均)板块多维 -> getSecReAtAInEarningAvgGLbWsee


# 获取营运资本(合计)板块多维 -> getSecWCapSumGLbWsee


# 获取营运资本(算术平均)板块多维 -> getSecWCapAvgGLbWsee


# 获取归属母公司股东的权益(合计)板块多维 -> getSecEAsPcSumChNWsee


# 获取归属母公司股东的权益(算术平均)板块多维 -> getSecEAsPcAvgChNWsee


# 获取经营活动产生的现金流量净额(合计)板块多维 -> getSecNcFoASumGLbWsee


# 获取经营活动产生的现金流量净额(算术平均)板块多维 -> getSecNcFoAAvgGLbWsee


# 获取投资活动产生的现金流量净额(合计)板块多维 -> getSecNcFiaSumGLbWsee


# 获取投资活动产生的现金流量净额(算术平均)板块多维 -> getSecNcFiaAvgGLbWsee


# 获取筹资活动产生的现金流量净额(合计)板块多维 -> getSecNcFfaSumGLbWsee


# 获取筹资活动产生的现金流量净额(算术平均)板块多维 -> getSecNcFfaAvgGLbWsee


# 获取汇率变动对现金的影响(合计)板块多维 -> getSecEffectOfForExonCashSumGLbWsee


# 获取汇率变动对现金的影响(算术平均)板块多维 -> getSecEffectOfForExonCashAvgGLbWsee


# 获取现金及现金等价物净增加额(合计)板块多维 -> getSecNetIncreaseIncCeSumGLbWsee


# 获取现金及现金等价物净增加额(算术平均)板块多维 -> getSecNetIncreaseIncCeAvgGLbWsee


# 获取股权自由现金流量FCFE(合计)板块多维 -> getSecFcFe2SumGLbWsee


# 获取股权自由现金流量FCFE(算术平均)板块多维 -> getSecFcFe2AvgGLbWsee


# 获取企业自由现金流量(合计)板块多维 -> getSecFcFfSumGLbWsee


# 获取企业自由现金流量(算术平均)板块多维 -> getSecFcFfAvgGLbWsee


# 获取销售净利率(TTM)(整体法)板块多维 -> getSecNetProfitMarginTtMOverallChNWsee


# 获取销售净利率(TTM)(算术平均)板块多维 -> getSecNetProfitMarginTtMAvgChNWsee


# 获取销售费用/营业总收入(整体法)板块多维 -> getSecOperateExpenseToGrOverallChNWsee


# 获取管理费用/营业总收入(整体法)板块多维 -> getSecFaAdminExpenseToGrOverallChNWsee


# 获取财务费用/营业总收入(整体法)板块多维 -> getSecFinaExpenseToGrOverallChNWsee


# 获取经营活动净收益/利润总额(整体法)板块多维 -> getSecOperateIncomeToEBTOverallChNWsee


# 获取价值变动净收益/利润总额(整体法)板块多维 -> getSecInvestIncomeToEBTOverallChNWsee


# 获取所得税/利润总额(整体法)板块多维 -> getSecTaxToEBTOverallChNWsee


# 获取扣除非经常损益后的净利润/净利润(整体法)板块多维 -> getSecDeductedProfitToProfitOverallChNWsee


# 获取销售商品提供劳务收到的现金/营业收入(整体法)板块多维 -> getSecSalesCashIntoOrOverallChNWsee


# 获取销售商品提供劳务收到的现金/营业收入(算术平均)板块多维 -> getSecSalesCashIntoOrAvgChNWsee


# 获取资本支出/旧和摊销(整体法)板块多维 -> getSecCapeXTodaOverallChNWsee


# 获取负债合计/归属母公司股东的权益(整体法)板块多维 -> getSecTotalLiabilityToeAsPcOverallChNWsee


# 获取负债合计/归属母公司股东的权益(算术平均)板块多维 -> getSecTotalLiabilityToeAsPcAvgChNWsee


# 获取带息债务/归属母公司股东的权益(整体法)板块多维 -> getSecInterestBearingDebtToeAsPcOverallChNWsee


# 获取净债务/归属母公司股东的权益(整体法)板块多维 -> getSecNetLiabilityToeAsPcOverallChNWsee


# 获取资产周转率(TTM)(整体法)板块多维 -> getSecAssetsTurnTtMOverallChNWsee


# 获取资产周转率(TTM)(算术平均)板块多维 -> getSecAssetsTurnTtMAvgChNWsee


# 获取单季度.每股收益EPS(整体法)板块多维 -> getSecQfaEpsOverallChNWsee


# 获取单季度.每股收益EPS(算术平均)板块多维 -> getSecQfaEpsAvgChNWsee


# 获取单季度.净资产收益率ROE-摊薄(整体法)板块多维 -> getSecQfaRoeDilutedOverallChNWsee


# 获取单季度.净资产收益率ROE-摊薄(算术平均)板块多维 -> getSecQfaRoeDilutedAvgChNWsee


# 获取单季度.扣除非经常损益后的净资产收益率-摊薄(整体法)板块多维 -> getSecQfaDeductedRoeDilutedOverallChNWsee


# 获取单季度.扣除非经常损益后的净资产收益率-摊薄(算术平均)板块多维 -> getSecQfaDeductedRoeDilutedAvgChNWsee


# 获取单季度.总资产净利率(整体法)板块多维 -> getSecQfaRoaOverallChNWsee


# 获取单季度.总资产净利率(算术平均)板块多维 -> getSecQfaRoaAvgChNWsee


# 获取单季度.销售净利率(整体法)板块多维 -> getSecQfaNetProfitMarginOverallChNWsee


# 获取单季度.销售净利率(算术平均)板块多维 -> getSecQfaNetProfitMarginAvgChNWsee


# 获取单季度.销售毛利率(整体法)板块多维 -> getSecQfaGrossProfitMarginOverallChNWsee


# 获取单季度.销售毛利率(算术平均)板块多维 -> getSecQfaGrossProfitMarginAvgChNWsee


# 获取单季度.营业总成本/营业总收入(整体法)板块多维 -> getSecQfaGcToGrOverallChNWsee


# 获取单季度.营业总成本/营业总收入(算术平均)板块多维 -> getSecQfaGcToGrAvgChNWsee


# 获取单季度.营业利润/营业总收入(整体法)板块多维 -> getSecQfaOpToGrOverallChNWsee


# 获取单季度.营业利润/营业总收入(算术平均)板块多维 -> getSecQfaOpToGrAvgChNWsee


# 获取单季度.净利润/营业总收入(整体法)板块多维 -> getSecQfaProfitToGrOverallChNWsee


# 获取单季度.净利润/营业总收入(算术平均)板块多维 -> getSecQfaProfitToGrAvgChNWsee


# 获取单季度.销售费用/营业总收入(整体法)板块多维 -> getSecQfaOperateExpenseToGrOverallChNWsee


# 获取单季度.销售费用/营业总收入(算术平均)板块多维 -> getSecQfaOperateExpenseToGrAvgChNWsee


# 获取单季度.管理费用/营业总收入(整体法)板块多维 -> getSecQfaAdminExpenseToGrOverallChNWsee


# 获取单季度.管理费用/营业总收入(算术平均)板块多维 -> getSecQfaAdminExpenseToGrAvgChNWsee


# 获取单季度.财务费用/营业总收入(整体法)板块多维 -> getSecQfaFinaExpenseToGrOverallChNWsee


# 获取单季度.财务费用/营业总收入(算术平均)板块多维 -> getSecQfaFinaExpenseToGrAvgChNWsee


# 获取单季度.经营活动净收益/利润总额(整体法)板块多维 -> getSecQfaOperateIncomeToEBTOverallChNWsee


# 获取单季度.经营活动净收益/利润总额(算术平均)板块多维 -> getSecQfaOperateIncomeToEBTAvgChNWsee


# 获取单季度.价值变动净收益/利润总额(整体法)板块多维 -> getSecQfaInvestIncomeToEBTOverallChNWsee


# 获取单季度.价值变动净收益/利润总额(算术平均)板块多维 -> getSecQfaInvestIncomeToEBTAvgChNWsee


# 获取单季度.扣除非经常损益后的净利润/净利润(整体法)板块多维 -> getSecQfaDeductedProfitToProfitOverallChNWsee


# 获取单季度.扣除非经常损益后的净利润/净利润(算术平均)板块多维 -> getSecQfaDeductedProfitToProfitAvgChNWsee


# 获取单季度.销售商品提供劳务收到的现金/营业收入(整体法)板块多维 -> getSecQfaSalesCashIntoOrOverallChNWsee


# 获取单季度.销售商品提供劳务收到的现金/营业收入(算术平均)板块多维 -> getSecQfaSalesCashIntoOrAvgChNWsee


# 获取单季度.经营活动产生的现金流量净额/营业收入(整体法)板块多维 -> getSecQfaOCFToOrOverallChNWsee


# 获取单季度.经营活动产生的现金流量净额/营业收入(算术平均)板块多维 -> getSecQfaOCFToOrAvgChNWsee


# 获取单季度.经营活动产生的现金流量净额/经营活动净收益(整体法)板块多维 -> getSecQfaOCFToOperateIncomeOverallChNWsee


# 获取单季度.经营活动产生的现金流量净额/经营活动净收益(算术平均)板块多维 -> getSecQfaOCFToOperateIncomeAvgChNWsee


# 获取单季度.营业总收入合计(同比增长率)板块多维 -> getSecQfaGrTotalYoYChNWsee


# 获取单季度.营业总收入合计(环比增长率)板块多维 -> getSecQfaGrTotalMomChNWsee


# 获取单季度.营业收入合计(同比增长率)板块多维 -> getSecQfaRevenueTotalYoYChNWsee


# 获取单季度.营业收入合计(环比增长率)板块多维 -> getSecQfaRevenueTotalMomChNWsee


# 获取单季度.营业利润合计(同比增长率)板块多维 -> getSecQfaOpTotalYoYChNWsee


# 获取单季度.营业利润合计(环比增长率)板块多维 -> getSecQfaOpTotalMomChNWsee


# 获取单季度.净利润合计(同比增长率)板块多维 -> getSecQfaNpTotalYoYChNWsee


# 获取单季度.净利润合计(环比增长率)板块多维 -> getSecQfaNpTotalMomChNWsee


# 获取单季度.归属母公司股东的净利润合计(同比增长率)板块多维 -> getSecQfaNpaSpcTotalYoYChNWsee


# 获取单季度.归属母公司股东的净利润合计(环比增长率)板块多维 -> getSecQfaNpaSpcTotalMomChNWsee


# 获取营业总成本(合计)板块多维 -> getSecGcSumChNWsee


# 获取营业总成本(算术平均)板块多维 -> getSecGcAvgChNWsee


# 获取营业收入(合计)板块多维 -> getSecOrSumChNWsee


# 获取营业收入(算术平均)板块多维 -> getSecOrAvgChNWsee


# 获取销售费用(合计)板块多维 -> getSecSellingExpSumChNWsee


# 获取销售费用(算术平均)板块多维 -> getSecSellingExpAvgChNWsee


# 获取管理费用(合计)板块多维 -> getSecMNgtExpSumChNWsee


# 获取管理费用(算术平均)板块多维 -> getSecMNgtExpAvgChNWsee


# 获取财务费用(合计)板块多维 -> getSecFineXpSumChNWsee


# 获取财务费用(算术平均)板块多维 -> getSecFineXpAvgChNWsee


# 获取投资净收益(合计)板块多维 -> getSecNiOnInvestmentSumChNWsee


# 获取投资净收益(算术平均)板块多维 -> getSecNiOnInvestmentAvgChNWsee


# 获取汇兑净收益(合计)板块多维 -> getSecNiOnForExSumChNWsee


# 获取汇兑净收益(算术平均)板块多维 -> getSecNiOnForExAvgChNWsee


# 获取公允价值变动净收益(合计)板块多维 -> getSecNiFromChangesInFvSumChNWsee


# 获取公允价值变动净收益(算术平均)板块多维 -> getSecNiFromChangesInFvAvgChNWsee


# 获取利润总额(合计)板块多维 -> getSecEBtSumChNWsee


# 获取利润总额(算术平均)板块多维 -> getSecEBtAvgChNWsee


# 获取归属母公司股东的净利润(合计)板块多维 -> getSecNpaSpcSumChNWsee


# 获取归属母公司股东的净利润(算术平均)板块多维 -> getSecNpaSpcAvgChNWsee


# 获取归属母公司股东的净利润-扣除非经常损益(合计)板块多维 -> getSecExNonRecurringPnLnPasPcSumChNWsee


# 获取归属母公司股东的净利润-扣除非经常损益(算术平均)板块多维 -> getSecExNonRecurringPnLnPasPcAvgChNWsee


# 获取经营活动净收益(合计)板块多维 -> getSecOperateIncomeSumChNWsee


# 获取经营活动净收益(算术平均)板块多维 -> getSecOperateIncomeAvgChNWsee


# 获取价值变动净收益(合计)板块多维 -> getSecInvestIncomeSumChNWsee


# 获取价值变动净收益(算术平均)板块多维 -> getSecInvestIncomeAvgChNWsee


# 获取货币资金(合计)板块多维 -> getSecCashSumChNWsee


# 获取货币资金(算术平均)板块多维 -> getSecCashAvgChNWsee


# 获取应收票据(合计)板块多维 -> getSecNotErSumChNWsee


# 获取应收票据(算术平均)板块多维 -> getSecNotErAvgChNWsee


# 获取应收账款(合计)板块多维 -> getSecArSumChNWsee


# 获取应收账款(算术平均)板块多维 -> getSecArAvgChNWsee


# 获取长期股权投资(合计)板块多维 -> getSecLteQtInvestmentSumChNWsee


# 获取长期股权投资(算术平均)板块多维 -> getSecLteQtInvestmentAvgChNWsee


# 获取投资性房地产(合计)板块多维 -> getSecInvestmentReSumChNWsee


# 获取投资性房地产(算术平均)板块多维 -> getSecInvestmentReAvgChNWsee


# 获取短期借款(合计)板块多维 -> getSecStDebtSumChNWsee


# 获取短期借款(算术平均)板块多维 -> getSecStDebtAvgChNWsee


# 获取应付票据(合计)板块多维 -> getSecNotEpSumChNWsee


# 获取应付票据(算术平均)板块多维 -> getSecNotEpAvgChNWsee


# 获取应付账款(合计)板块多维 -> getSecApSumChNWsee


# 获取应付账款(算术平均)板块多维 -> getSecApAvgChNWsee


# 获取营业总收入合计(同比增长率)板块多维 -> getSecGrYoYTotalChNWsee


# 获取营业收入合计(同比增长率)板块多维 -> getSecRevenueYoYTotalChNWsee


# 获取营业利润合计(同比增长率)板块多维 -> getSecOpYoYTotalChNWsee


# 获取净利润合计(同比增长率)板块多维 -> getSecNpSumYoYGLbWsee


# 获取归属母公司股东的净利润合计(同比增长率)板块多维 -> getSecNpaSpcYoYTotalChNWsee


# 获取经营活动产生的现金流量净额合计(同比增长率)板块多维 -> getSecCfOAYoYTotalChNWsee


# 获取投资活动产生的现金流量净额合计(同比增长率)板块多维 -> getSecCFiaSumYoYGLbWsee


# 获取筹资活动产生的现金流量净额合计(同比增长率)板块多维 -> getSecCffASumYoYGLbWsee


# 获取现金及现金等价物净增加额合计(同比增长率)板块多维 -> getSecCCeNetIncreaseSumYoYGLbWsee


# 获取净资产收益率(整体法)(同比增长率)板块多维 -> getSecDupontRoeOverallYoYChNWsee


# 获取净资产收益率(算术平均)(同比增长率)板块多维 -> getSecDupontRoeAvgYoYChNWsee


# 获取每股净资产(整体法)(相对年初增长率)板块多维 -> getSecBpSOverallGtBYearChNWsee


# 获取每股净资产(算术平均)(相对年初增长率)板块多维 -> getSecBpSAvgGtBgYearChNWsee


# 获取资产总计合计(相对年初增长率)板块多维 -> getSecTotalAssetTotalGtBYearChNWsee


# 获取归属母公司股东的权益合计(相对年初增长率)板块多维 -> getSecTotalEquityAsPcTotalGtBYearChNWsee


# 获取利润总额合计(同比增长率)板块多维 -> getSecEBtYoYTotalChNWsee
#
# 获取收盘价(总股本加权平均)板块序列 -> getSecCloseTsWavGWses


# 获取收盘价(流通股本加权平均)(中国)板块序列 -> getSecCloseFfsWavGChNWses


# 获取换手率(算术平均)板块序列 -> getSecTurnAvgWses


# 获取换手率(总市值加权平均)板块序列 -> getSecTurnTMcWavGWses


# 获取换手率(流通市值加权平均)板块序列 -> getSecTurnFfMcWavGWses


# 获取成交量(合计)板块序列 -> getSecVolumeSumWses


# 获取成交金额(合计)板块序列 -> getSecAmountSumWses


# 获取总股本(合计)板块序列 -> getSecShareTotalSumWses


# 获取总股本(算术平均)板块序列 -> getSecShareTotalAvgWses


# 获取流通A股(合计)板块序列 -> getSecShareFloatASumWses


# 获取流通A股(算术平均)板块序列 -> getSecShareFloatAAvgWses


# 获取流通B股(合计)板块序列 -> getSecShareFloatBSumWses


# 获取流通B股(算术平均)板块序列 -> getSecShareFloatBAvgWses


# 获取流通H股(合计)板块序列 -> getSecShareFloatHSumWses


# 获取流通H股(算术平均)板块序列 -> getSecShareFloatHAvgWses


# 获取总流通股本(合计)(中国)板块序列 -> getSecShareFloatTotalSumChNWses


# 获取总流通股本(算术平均)(中国)板块序列 -> getSecShareFloatTotalAvgChNWses


# 获取非流通股(合计)(中国)板块序列 -> getSecShareTotalNonLiqSumChNWses


# 获取非流通股(算术平均)(中国)板块序列 -> getSecShareTotalNonLiqAvgChNWses


# 获取预测每股收益(整体法)板块序列 -> getSecWestEpsOverallChNWses


# 获取预测每股收益(算术平均)板块序列 -> getSecWestEpsAvgChNWses


# 获取预测净利润(合计)板块序列 -> getSecWestNpSumChNWses


# 获取预测净利润(算术平均)板块序列 -> getSecWestNpAvgChNWses


# 获取预测主营业务收入(合计)板块序列 -> getSecWestRevenueSumChNWses


# 获取预测主营业务收入(算术平均)板块序列 -> getSecWestRevenueAvgChNWses


# 获取(日)净流入资金(合计)板块序列 -> getSecNCashInFlowDSumChNWses


# 获取(日)净流入资金(算术平均)板块序列 -> getSecNCashInFlowDAvgChNWses


# 获取(日)净流入量(合计)板块序列 -> getSecNVolInFlowDSumChNWses


# 获取(日)净流入量(算术平均)板块序列 -> getSecNVolInFlowDAvgChNWses


# 获取(日)尾盘净流入资金(合计)板块序列 -> getSecNClosingInFlowDSumChNWses


# 获取(日)尾盘净流入资金(算术平均)板块序列 -> getSecNClosingInFlowDAvgChNWses


# 获取(日)开盘净流入资金(合计)板块序列 -> getSecNOpeningInFlowDSumChNWses


# 获取(日)开盘净流入资金(算术平均)板块序列 -> getSecNOpeningInFlowDAvgChNWses


# 获取(日)金额流入率(整体法)板块序列 -> getSecCInFlowRateDOverallChNWses


# 获取(日)金额流入率(算术平均)板块序列 -> getSecCInFlowRateDAvgChNWses


# 获取(日)资金流向占比(整体法)板块序列 -> getSecCashDirectionPecDOverallChNWses


# 获取(日)资金流向占比(算术平均)板块序列 -> getSecCashDirectionPecDAvgChNWses


# 获取总市值(合计)板块序列 -> getSecMktCapSumGLbWses


# 获取总市值(算术平均)板块序列 -> getSecMktCapAvgGLbWses


# 获取总市值2(合计)板块序列 -> getSecMvArdSumGLbWses


# 获取总市值2(算术平均)板块序列 -> getSecMvArdAvgGLbWses


# 获取市盈率(TTM-算术平均法)板块序列 -> getSecPeTtMAvgChNWses


# 获取市盈率(TTM-中值)板块序列 -> getSecPetTmMediaChNWses


# 获取市盈率(算术平均)板块序列 -> getSecPeAvgChNWses


# 获取市盈率(中值)板块序列 -> getSecPeMediaChNWses


# 获取市净率(算术平均)板块序列 -> getSecPbAvgChNWses


# 获取市净率(中值)板块序列 -> getSecPbMediaChNWses


# 获取市现率(算术平均)板块序列 -> getSecPcfAvgChNWses


# 获取市现率(中值)板块序列 -> getSecPcfMediaChNWses


# 获取市销率(算术平均)板块序列 -> getSecPsAvgChNWses


# 获取市销率(中值)板块序列 -> getSecPsMediaChNWses


# 获取市盈率(TTM-整体法)板块序列 -> getSecPeTtMOverallChNWses


# 获取市净率(整体法)板块序列 -> getSecPbOverallChNWses


# 获取市现率(整体法)板块序列 -> getSecPcfOverallChNWses


# 获取市净率(最新-中值)板块序列 -> getSecPcfMediaLastEstChNWses


# 获取市销率(整体法)板块序列 -> getSecPsOverallChNWses


# 获取当日总市值(合计)板块序列 -> getSecMktCapTodaySumChNWses


# 获取当日总市值(算术平均)板块序列 -> getSecMktCapTodayAvgChNWses


# 获取流通A股市值(合计)板块序列 -> getSecMktCapFloatASharesSumChNWses


# 获取流通A股市值(算术平均)板块序列 -> getSecMktCapFloatASharesAvgChNWses


# 获取流通B股市值(合计)板块序列 -> getSecMktCapFloatBSharesSumChNWses


# 获取流通B股市值(算术平均)板块序列 -> getSecMktCapFloatBSharesAvgChNWses


# 获取自由流通市值(合计)板块序列 -> getSecMktCapFloatFreeSharesSumChNWses


# 获取自由流通市值(算术平均)板块序列 -> getSecMktCapFloatFreeSharesAvgChNWses


# 获取年化收益率算术平均(最近100周)板块序列 -> getSecRiskAnnualYeIlD100WAvgChNWses


# 获取年化收益率算术平均(最近24个月)板块序列 -> getSecRiskAnnualYeIlD24MAvgChNWses


# 获取年化收益率算术平均(最近60个月)板块序列 -> getSecRiskAnnualYeIlD60MAvgChNWses


# 获取年化波动率算术平均(最近100周)板块序列 -> getSecRiskStDevYearly100WAvgChNWses


# 获取年化波动率算术平均(最近24个月)板块序列 -> getSecRiskStDevYearly24MAvgChNWses


# 获取年化波动率算术平均(最近60个月)板块序列 -> getSecRiskStDevYearly60MAvgChNWses


# 获取BETA值算术平均(最近100周)板块序列 -> getSecRiskBeta100WAvgChNWses


# 获取BETA值算术平均(最近24个月)板块序列 -> getSecRiskBeta24MAvgChNWses


# 获取BETA值算术平均(最近60个月)板块序列 -> getSecRiskBeta60MAvgChNWses


# 获取上市公司家数板块序列 -> getSecCsrCStatListCompNumChNWses


# 获取上市公司境内总股本板块序列 -> getSecCsrCStatShareTotalChNWses


# 获取上市公司境内总市值板块序列 -> getSecCsrCStatMvChNWses


# 获取市场静态市盈率板块序列 -> getSecCsrCStatPeChNWses


# 获取市场静态市净率板块序列 -> getSecCsrCStatPbChNWses


# 获取上市公司境内股本对应的归属母公司净利润TTM板块序列 -> getSecCsrCStatNpTtMChNWses


# 获取市场滚动市盈率板块序列 -> getSecCsrCStatPeTtMChNWses


# 获取每股收益EPS-基本(算术平均)板块序列 -> getSecEpsBasic2AvgChNWses


# 获取每股收益EPS-稀释(算术平均)板块序列 -> getSecEpsDiluted4AvgChNWses


# 获取每股收益EPS-期末股本摊薄(整体法)板块序列 -> getSecEndingSharesEpsBasic2OverallChNWses


# 获取每股收益EPS-期末股本摊薄(算术平均)板块序列 -> getSecEndingSharesEpsBasic2AvgChNWses


# 获取每股净资产(整体法)板块序列 -> getSecBpSOverallChNWses


# 获取每股净资产(算术平均)板块序列 -> getSecBpSAvgChNWses


# 获取每股营业总收入(整体法)板块序列 -> getSecGrpSOverallChNWses


# 获取每股营业总收入(算术平均)板块序列 -> getSecGrpSAvgChNWses


# 获取每股留存收益(整体法)板块序列 -> getSecRetainedPsOverallChNWses


# 获取每股留存收益(算术平均)板块序列 -> getSecRetainedPsAvgChNWses


# 获取每股现金流量净额(整体法)板块序列 -> getSecCfpSOverallChNWses


# 获取每股现金流量净额(算术平均)板块序列 -> getSecCfpSAvgChNWses


# 获取每股经营活动产生的现金流量净额(整体法)板块序列 -> getSecOcFps2OverallChNWses


# 获取每股经营活动产生的现金流量净额(算术平均)板块序列 -> getSecOcFps2AvgChNWses


# 获取每股息税前利润(算术平均)板块序列 -> getSecEbItPsAvgGLbWses


# 获取每股企业自由现金流量(整体法)板块序列 -> getSecFcFFpsOverallGLbWses


# 获取每股企业自由现金流量(算术平均)板块序列 -> getSecFcFFpsAvgGLbWses


# 获取每股股东自由现金流量(整体法)板块序列 -> getSecFcFEpsOverallGLbWses


# 获取每股股东自由现金流量(算术平均)板块序列 -> getSecFcFEpsAvgGLbWses


# 获取净资产收益率-平均(整体法)板块序列 -> getSecRoeAvgOverallChNWses


# 获取净资产收益率-平均(算术平均)板块序列 -> getSecRoeAvgAvgChNWses


# 获取净资产收益率-摊薄(整体法)板块序列 -> getSecRoeDilutedOverallChNWses


# 获取净资产收益率-摊薄(算术平均)板块序列 -> getSecRoeDilutedAvgChNWses


# 获取扣除非经常损益后的净资产收益率-平均(整体法)板块序列 -> getSecDeductedRoeAvgOverallChNWses


# 获取扣除非经常损益后的净资产收益率-平均(算术平均)板块序列 -> getSecDeductedRoeAvgAvgChNWses


# 获取扣除非经常损益后的净资产收益率-摊薄(整体法)板块序列 -> getSecDeductedRoeDilutedOverallChNWses


# 获取扣除非经常损益后的净资产收益率-摊薄(算术平均)板块序列 -> getSecDeductedRoeDilutedAvgChNWses


# 获取总资产报酬率(整体法)板块序列 -> getSecRoa2OverallGLbWses


# 获取总资产报酬率(算术平均)板块序列 -> getSecRoa2AvgGLbWses


# 获取总资产净利率(整体法)板块序列 -> getSecRoaOverallChNWses


# 获取总资产净利率(算术平均)板块序列 -> getSecRoaAvgChNWses


# 获取销售毛利率(整体法)板块序列 -> getSecGrossProfitMarginOverallChNWses


# 获取销售毛利率(算术平均)板块序列 -> getSecGrossProfitMarginAvgChNWses


# 获取销售净利率(整体法)板块序列 -> getSecNetProfitMarginOverallChNWses


# 获取销售净利率(算术平均)板块序列 -> getSecNetProfitMarginAvgChNWses


# 获取营业总成本/营业总收入(整体法)板块序列 -> getSecGcToGrOverallChNWses


# 获取营业总成本/营业总收入(算术平均)板块序列 -> getSecGcToGrAvgChNWses


# 获取营业利润/营业总收入(整体法)板块序列 -> getSecOpToGrOverallChNWses


# 获取营业利润/营业总收入(算术平均)板块序列 -> getSecOpToGrAvgChNWses


# 获取净利润/营业总收入(整体法)板块序列 -> getSecDupontNpToSalesOverallChNWses


# 获取净利润/营业总收入(算术平均)板块序列 -> getSecDupontNpToSalesAvgChNWses


# 获取销售费用/营业总收入(算术平均)板块序列 -> getSecOperateExpenseToGrAvgChNWses


# 获取管理费用/营业总收入(算术平均)板块序列 -> getSEcfAAdminExpenseToGrAvgChNWses


# 获取财务费用/营业总收入(算术平均)板块序列 -> getSecFinaExpenseToGrAvgChNWses


# 获取息税前利润/营业总收入(算术平均)板块序列 -> getSecDupontEbItToSalesAvgGLbWses


# 获取EBITDA/营业总收入(整体法)板块序列 -> getSecEbItDatoSalesOverallGLbWses


# 获取EBITDA/营业总收入(算术平均)板块序列 -> getSecEbItDatoSalesAvgGLbWses


# 获取投入资本回报率(算术平均)板块序列 -> getSecRoiCAvgGLbWses


# 获取营业利润/利润总额(算术平均)板块序列 -> getSecOpToEBTAvgGLbWses


# 获取价值变动净收益/利润总额(算术平均)板块序列 -> getSecInvestIncomeToEBTAvgChNWses


# 获取所得税/利润总额(算术平均)板块序列 -> getSecTaxToEBTAvgChNWses


# 获取扣除非经常损益后的净利润/净利润(算术平均)板块序列 -> getSecDeductedProfitToProfitAvgChNWses


# 获取经营活动净收益/利润总额(算术平均)板块序列 -> getSecOperateIncomeToEBTAvgChNWses


# 获取经营活动产生的现金流量净额/营业收入(整体法)板块序列 -> getSecOCFToOrOverallChNWses


# 获取经营活动产生的现金流量净额/营业收入(算术平均)板块序列 -> getSecOCFToOrAvgChNWses


# 获取经营活动产生的现金流量净额/经营活动净收益(整体法)板块序列 -> getSecOCFToOperateIncomeOverallChNWses


# 获取经营活动产生的现金流量净额/经营活动净收益(算术平均)板块序列 -> getSecOCFToOperateIncomeAvgChNWses


# 获取资本支出/折旧和摊销(整体法)板块序列 -> getSecCapeXTodaOverallChNWses


# 获取资本支出/折旧和摊销(算术平均)板块序列 -> getSecCapitalizedTodaAvgChNWses


# 获取资产负债率(整体法)板块序列 -> getSecDebtToAssetsOverallChNWses


# 获取资产负债率(算术平均)板块序列 -> getSecDebtToAssetsAvgChNWses


# 获取流动资产/总资产(整体法)板块序列 -> getSecCatoAssetsOverallChNWses


# 获取流动资产/总资产(算术平均)板块序列 -> getSecCatoAssetsAvgChNWses


# 获取非流动资产/总资产(整体法)板块序列 -> getSecNcaToAssetsOverallChNWses


# 获取非流动资产/总资产(算术平均)板块序列 -> getSecNcaToAssetsAvgChNWses


# 获取有形资产/总资产(整体法)板块序列 -> getSecTangibleAssetsToAssetsOverallChNWses


# 获取有形资产/总资产(算术平均)板块序列 -> getSecTangibleAssetsToAssetsAvgChNWses


# 获取流动负债/负债合计(整体法)板块序列 -> getSecCurrentDebtToDebtOverallChNWses


# 获取流动负债/负债合计(算术平均)板块序列 -> getSecCurrentDebtToDebtAvgChNWses


# 获取非流动负债/负债合计(整体法)板块序列 -> getSecLongDebToDebtOverallChNWses


# 获取非流动负债/负债合计(算术平均)板块序列 -> getSecLongDebToDebtAvgChNWses


# 获取流动比率(整体法)板块序列 -> getSecCurrentOverallChNWses


# 获取流动比率(算术平均)板块序列 -> getSecCurrentAvgChNWses


# 获取速动比率(整体法)板块序列 -> getSecQuickOverallChNWses


# 获取速动比率(算术平均)板块序列 -> getSecQuickAvgChNWses


# 获取归属母公司股东的权益/负债合计(整体法)板块序列 -> getSecEquityToDebtOverallGLbWses


# 获取归属母公司股东的权益/负债合计(算术平均)板块序列 -> getSecEquityToDebtAvgGLbWses


# 获取归属母公司股东的权益/带息债务(整体法)板块序列 -> getSecEquityToInterestDebtOverallGLbWses


# 获取归属母公司股东的权益/带息债务(算术平均)板块序列 -> getSecEquityToInterestDebtAvgGLbWses


# 获取息税折旧摊销前利润/负债合计(整体法)板块序列 -> getSecEbItDatoDebtOverallGLbWses


# 获取息税折旧摊销前利润/负债合计(算术平均)板块序列 -> getSecEbItDatoDebtAvgGLbWses


# 获取经营活动产生的现金流量净额/负债合计(整体法)板块序列 -> getSecOCFToDebtOverallChNWses


# 获取经营活动产生的现金流量净额/负债合计(算术平均)板块序列 -> getSecOCFToDebtAvgChNWses


# 获取已获利息倍数(算术平均)板块序列 -> getSecInterestCoverageAvgChNWses


# 获取存货周转率(整体法)板块序列 -> getSecInvTurnOverallChNWses


# 获取存货周转率(算术平均)板块序列 -> getSecInvTurnAvgChNWses


# 获取应收账款周转率(整体法)板块序列 -> getSecArturNOverallChNWses


# 获取应收账款周转率(算术平均)板块序列 -> getSecArturNAvgChNWses


# 获取固定资产周转率(整体法)板块序列 -> getSecFaTurnOverallChNWses


# 获取固定资产周转率(算术平均)板块序列 -> getSecFaTurnAvgChNWses


# 获取总资产周转率(整体法)板块序列 -> getSecAssetsTurnOverallChNWses


# 获取总资产周转率(算术平均)板块序列 -> getSecAssetsTurnAvgChNWses


# 获取营业周期(整体法)板块序列 -> getSecTurnDaysOverallChNWses


# 获取营业周期(算术平均)板块序列 -> getSecTurnDaysAvgChNWses


# 获取存货周转天数(整体法)板块序列 -> getSecInvTurnDaysOverallChNWses


# 获取存货周转天数(算术平均)板块序列 -> getSecInvTurnDaysAvgChNWses


# 获取应收账款周转天数(整体法)板块序列 -> getSecArturNDaysOverallChNWses


# 获取应收账款周转天数(算术平均)板块序列 -> getSecArturNDaysAvgChNWses


# 获取营业总收入合计(同比增长率)板块序列 -> getSecGrYoYTotalChNWses


# 获取营业收入合计(同比增长率)板块序列 -> getSecRevenueYoYTotalChNWses


# 获取营业利润合计(同比增长率)板块序列 -> getSecOpYoYTotalChNWses


# 获取净利润合计(同比增长率)板块序列 -> getSecNpSumYoYGLbWses


# 获取归属母公司股东的净利润合计(同比增长率)板块序列 -> getSecNpaSpcYoYTotalChNWses


# 获取经营活动产生的现金流量净额合计(同比增长率)板块序列 -> getSecCfOAYoYTotalChNWses


# 获取投资活动产生的现金流量净额合计(同比增长率)板块序列 -> getSecCFiaSumYoYGLbWses


# 获取筹资活动产生的现金流量净额合计(同比增长率)板块序列 -> getSecCffASumYoYGLbWses


# 获取现金及现金等价物净增加额合计(同比增长率)板块序列 -> getSecCCeNetIncreaseSumYoYGLbWses


# 获取净资产收益率(整体法)(同比增长率)板块序列 -> getSecDupontRoeOverallYoYChNWses


# 获取净资产收益率(算术平均)(同比增长率)板块序列 -> getSecDupontRoeAvgYoYChNWses


# 获取每股净资产(整体法)(相对年初增长率)板块序列 -> getSecBpSOverallGtBYearChNWses


# 获取每股净资产(算术平均)(相对年初增长率)板块序列 -> getSecBpSAvgGtBgYearChNWses


# 获取资产总计合计(相对年初增长率)板块序列 -> getSecTotalAssetTotalGtBYearChNWses


# 获取归属母公司股东的权益合计(相对年初增长率)板块序列 -> getSecTotalEquityAsPcTotalGtBYearChNWses


# 获取营业总收入(合计)板块序列 -> getSecGrSumChNWses


# 获取营业总收入(算术平均)板块序列 -> getSecGrAvgChNWses


# 获取主营收入(合计)板块序列 -> getSecRevenueSumGLbWses


# 获取主营收入(算术平均)板块序列 -> getSecRevenueAvgGLbWses


# 获取其他营业收入(合计)板块序列 -> getSecOtherRevenueSumGLbWses


# 获取其他营业收入(算术平均)板块序列 -> getSecOtherRevenueAvgGLbWses


# 获取总营业支出(合计)板块序列 -> getSecGcSumGLbWses


# 获取总营业支出(算术平均)板块序列 -> getSecGcAvgGLbWses


# 获取营业成本(合计)板块序列 -> getSecOcSumChNWses


# 获取营业成本(算术平均)板块序列 -> getSecOcAvgChNWses


# 获取营业开支(合计)板块序列 -> getSecExpenseSumGLbWses


# 获取营业开支(算术平均)板块序列 -> getSecExpenseAvgGLbWses


# 获取权益性投资损益(合计)板块序列 -> getSecEquityInvpnLSumGLbWses


# 获取权益性投资损益(算术平均)板块序列 -> getSecEquityInvpnLAvgGLbWses


# 获取营业利润(合计)板块序列 -> getSecOpSumChNWses


# 获取营业利润(算术平均)板块序列 -> getSecOpAvgChNWses


# 获取除税前利润(合计)板块序列 -> getSecEBtSumGLbWses


# 获取除税前利润(算术平均)板块序列 -> getSecEBtAvgGLbWses


# 获取所得税(合计)板块序列 -> getSecTaxSumChNWses


# 获取所得税(算术平均)板块序列 -> getSecTaxAvgChNWses


# 获取净利润(合计)板块序列 -> getSecNpSumChNWses


# 获取净利润(算术平均)板块序列 -> getSecNpAvgChNWses


# 获取归属普通股东净利润(合计)板块序列 -> getSecNpaSpcSumGLbWses


# 获取归属普通股东净利润(算术平均)板块序列 -> getSecNpaSpcAvgGLbWses


# 获取毛利(合计)板块序列 -> getSecGrossMargin2SumChNWses


# 获取毛利(算术平均)板块序列 -> getSecGrossMargin2AvgChNWses


# 获取EBIT(合计)板块序列 -> getSecEbItSumGLbWses


# 获取EBIT(算术平均)板块序列 -> getSecEbItAvgGLbWses


# 获取资产总计(合计)板块序列 -> getSecAssetTotalSumChNWses


# 获取资产总计(算术平均)板块序列 -> getSecAssetTotalAvgChNWses


# 获取现金及现金等价物(合计)板块序列 -> getSecCCeSumGLbWses


# 获取现金及现金等价物(算术平均)板块序列 -> getSecCCeAvgGLbWses


# 获取交易性金融资产(合计)板块序列 -> getSecTradingFinancialAssetSumChNWses


# 获取交易性金融资产(算术平均)板块序列 -> getSecTradingFinancialAssetAvgChNWses


# 获取应收账款及票据(合计)板块序列 -> getSecArSumGLbWses


# 获取应收账款及票据(算术平均)板块序列 -> getSecArAvgGLbWses


# 获取存货(合计)板块序列 -> getSecIvNenTorySumChNWses


# 获取存货(算术平均)板块序列 -> getSecIvNenToryAvgChNWses


# 获取流动资产(合计)板块序列 -> getSecCurrentAssetSumChNWses


# 获取流动资产(算术平均)板块序列 -> getSecCurrentAssetAvgChNWses


# 获取权益性投资(合计)板块序列 -> getSecEquityInvSumGLbWses


# 获取权益性投资(算术平均)板块序列 -> getSecEquityInvAvgGLbWses


# 获取固定资产净值(合计)板块序列 -> getSecFixAssetNetValueSumChNWses


# 获取固定资产净值(算术平均)板块序列 -> getSecFixAssetNetValueAvgChNWses


# 获取在建工程(合计)板块序列 -> getSecCIpNetValueSumChNWses


# 获取在建工程(算术平均)板块序列 -> getSecCIpNetValueAvgChNWses


# 获取非流动资产(合计)板块序列 -> getSecNonCurrentAssetSumChNWses


# 获取非流动资产(算术平均)板块序列 -> getSecNonCurrentAssetAvgChNWses


# 获取应付账款及票据(合计)板块序列 -> getSecApSumGLbWses


# 获取应付账款及票据(算术平均)板块序列 -> getSecApAvgGLbWses


# 获取短期借贷及长期借贷当期到期部分(合计)板块序列 -> getSecCurrentMaturityOfBorrowingSSumGLbWses


# 获取短期借贷及长期借贷当期到期部分(算术平均)板块序列 -> getSecCurrentMaturityOfBorrowingSAvgGLbWses


# 获取流动负债(合计)板块序列 -> getSecCurrentLiabilitySumChNWses


# 获取流动负债(算术平均)板块序列 -> getSecCurrentLiabilityAvgChNWses


# 获取长期借款(合计)板块序列 -> getSecLtDebtSumChNWses


# 获取长期借款(算术平均)板块序列 -> getSecLtDebtAvgChNWses


# 获取非流动负债(合计)板块序列 -> getSecNonCurrentLiabilitySumChNWses


# 获取非流动负债(算术平均)板块序列 -> getSecNonCurrentLiabilityAvgChNWses


# 获取股东权益(合计)板块序列 -> getSecEquitySumChNWses


# 获取股东权益(算术平均)板块序列 -> getSecEquityAvgChNWses


# 获取少数股东权益(合计)板块序列 -> getSecMinorityQuitYSumChNWses


# 获取少数股东权益(算术平均)板块序列 -> getSecMinorityQuitYAvgChNWses


# 获取留存收益(合计)板块序列 -> getSecReAtAInEarningSumGLbWses


# 获取留存收益(算术平均)板块序列 -> getSecReAtAInEarningAvgGLbWses


# 获取营运资本(合计)板块序列 -> getSecWCapSumGLbWses


# 获取营运资本(算术平均)板块序列 -> getSecWCapAvgGLbWses


# 获取归属母公司股东的权益(合计)板块序列 -> getSecEAsPcSumChNWses


# 获取归属母公司股东的权益(算术平均)板块序列 -> getSecEAsPcAvgChNWses


# 获取经营活动产生的现金流量净额(合计)板块序列 -> getSecNcFoASumGLbWses


# 获取经营活动产生的现金流量净额(算术平均)板块序列 -> getSecNcFoAAvgGLbWses


# 获取投资活动产生的现金流量净额(合计)板块序列 -> getSecNcFiaSumGLbWses


# 获取投资活动产生的现金流量净额(算术平均)板块序列 -> getSecNcFiaAvgGLbWses


# 获取筹资活动产生的现金流量净额(合计)板块序列 -> getSecNcFfaSumGLbWses


# 获取筹资活动产生的现金流量净额(算术平均)板块序列 -> getSecNcFfaAvgGLbWses


# 获取汇率变动对现金的影响(合计)板块序列 -> getSecEffectOfForExonCashSumGLbWses


# 获取汇率变动对现金的影响(算术平均)板块序列 -> getSecEffectOfForExonCashAvgGLbWses


# 获取现金及现金等价物净增加额(合计)板块序列 -> getSecNetIncreaseIncCeSumGLbWses


# 获取现金及现金等价物净增加额(算术平均)板块序列 -> getSecNetIncreaseIncCeAvgGLbWses


# 获取股权自由现金流量FCFE(合计)板块序列 -> getSecFcFe2SumGLbWses


# 获取股权自由现金流量FCFE(算术平均)板块序列 -> getSecFcFe2AvgGLbWses


# 获取企业自由现金流量(合计)板块序列 -> getSecFcFfSumGLbWses


# 获取企业自由现金流量(算术平均)板块序列 -> getSecFcFfAvgGLbWses


# 获取销售净利率(TTM)(整体法)板块序列 -> getSecNetProfitMarginTtMOverallChNWses


# 获取销售净利率(TTM)(算术平均)板块序列 -> getSecNetProfitMarginTtMAvgChNWses


# 获取销售费用/营业总收入(整体法)板块序列 -> getSecOperateExpenseToGrOverallChNWses


# 获取管理费用/营业总收入(整体法)板块序列 -> getSecFaAdminExpenseToGrOverallChNWses


# 获取财务费用/营业总收入(整体法)板块序列 -> getSecFinaExpenseToGrOverallChNWses


# 获取经营活动净收益/利润总额(整体法)板块序列 -> getSecOperateIncomeToEBTOverallChNWses


# 获取价值变动净收益/利润总额(整体法)板块序列 -> getSecInvestIncomeToEBTOverallChNWses


# 获取所得税/利润总额(整体法)板块序列 -> getSecTaxToEBTOverallChNWses


# 获取扣除非经常损益后的净利润/净利润(整体法)板块序列 -> getSecDeductedProfitToProfitOverallChNWses


# 获取销售商品提供劳务收到的现金/营业收入(整体法)板块序列 -> getSecSalesCashIntoOrOverallChNWses


# 获取销售商品提供劳务收到的现金/营业收入(算术平均)板块序列 -> getSecSalesCashIntoOrAvgChNWses


# 获取负债合计/归属母公司股东的权益(整体法)板块序列 -> getSecTotalLiabilityToeAsPcOverallChNWses


# 获取负债合计/归属母公司股东的权益(算术平均)板块序列 -> getSecTotalLiabilityToeAsPcAvgChNWses


# 获取带息债务/归属母公司股东的权益(整体法)板块序列 -> getSecInterestBearingDebtToeAsPcOverallChNWses


# 获取净债务/归属母公司股东的权益(整体法)板块序列 -> getSecNetLiabilityToeAsPcOverallChNWses


# 获取资产周转率(TTM)(整体法)板块序列 -> getSecAssetsTurnTtMOverallChNWses


# 获取资产周转率(TTM)(算术平均)板块序列 -> getSecAssetsTurnTtMAvgChNWses


# 获取利润总额合计(同比增长率)板块序列 -> getSecEBtYoYTotalChNWses


# 获取单季度.每股收益EPS(整体法)板块序列 -> getSecQfaEpsOverallChNWses


# 获取单季度.每股收益EPS(算术平均)板块序列 -> getSecQfaEpsAvgChNWses


# 获取单季度.净资产收益率ROE-摊薄(整体法)板块序列 -> getSecQfaRoeDilutedOverallChNWses


# 获取单季度.净资产收益率ROE-摊薄(算术平均)板块序列 -> getSecQfaRoeDilutedAvgChNWses


# 获取单季度.扣除非经常损益后的净资产收益率-摊薄(整体法)板块序列 -> getSecQfaDeductedRoeDilutedOverallChNWses


# 获取单季度.扣除非经常损益后的净资产收益率-摊薄(算术平均)板块序列 -> getSecQfaDeductedRoeDilutedAvgChNWses


# 获取单季度.总资产净利率(整体法)板块序列 -> getSecQfaRoaOverallChNWses


# 获取单季度.总资产净利率(算术平均)板块序列 -> getSecQfaRoaAvgChNWses


# 获取单季度.销售净利率(整体法)板块序列 -> getSecQfaNetProfitMarginOverallChNWses


# 获取单季度.销售净利率(算术平均)板块序列 -> getSecQfaNetProfitMarginAvgChNWses


# 获取单季度.销售毛利率(整体法)板块序列 -> getSecQfaGrossProfitMarginOverallChNWses


# 获取单季度.销售毛利率(算术平均)板块序列 -> getSecQfaGrossProfitMarginAvgChNWses


# 获取单季度.营业总成本/营业总收入(整体法)板块序列 -> getSecQfaGcToGrOverallChNWses


# 获取单季度.营业总成本/营业总收入(算术平均)板块序列 -> getSecQfaGcToGrAvgChNWses


# 获取单季度.营业利润/营业总收入(整体法)板块序列 -> getSecQfaOpToGrOverallChNWses


# 获取单季度.营业利润/营业总收入(算术平均)板块序列 -> getSecQfaOpToGrAvgChNWses


# 获取单季度.净利润/营业总收入(整体法)板块序列 -> getSecQfaProfitToGrOverallChNWses


# 获取单季度.净利润/营业总收入(算术平均)板块序列 -> getSecQfaProfitToGrAvgChNWses


# 获取单季度.销售费用/营业总收入(整体法)板块序列 -> getSecQfaOperateExpenseToGrOverallChNWses


# 获取单季度.销售费用/营业总收入(算术平均)板块序列 -> getSecQfaOperateExpenseToGrAvgChNWses


# 获取单季度.管理费用/营业总收入(整体法)板块序列 -> getSecQfaAdminExpenseToGrOverallChNWses


# 获取单季度.管理费用/营业总收入(算术平均)板块序列 -> getSecQfaAdminExpenseToGrAvgChNWses


# 获取单季度.财务费用/营业总收入(整体法)板块序列 -> getSecQfaFinaExpenseToGrOverallChNWses


# 获取单季度.财务费用/营业总收入(算术平均)板块序列 -> getSecQfaFinaExpenseToGrAvgChNWses


# 获取单季度.经营活动净收益/利润总额(整体法)板块序列 -> getSecQfaOperateIncomeToEBTOverallChNWses


# 获取单季度.经营活动净收益/利润总额(算术平均)板块序列 -> getSecQfaOperateIncomeToEBTAvgChNWses


# 获取单季度.价值变动净收益/利润总额(整体法)板块序列 -> getSecQfaInvestIncomeToEBTOverallChNWses


# 获取单季度.价值变动净收益/利润总额(算术平均)板块序列 -> getSecQfaInvestIncomeToEBTAvgChNWses


# 获取单季度.扣除非经常损益后的净利润/净利润(整体法)板块序列 -> getSecQfaDeductedProfitToProfitOverallChNWses


# 获取单季度.扣除非经常损益后的净利润/净利润(算术平均)板块序列 -> getSecQfaDeductedProfitToProfitAvgChNWses


# 获取单季度.销售商品提供劳务收到的现金/营业收入(整体法)板块序列 -> getSecQfaSalesCashIntoOrOverallChNWses


# 获取单季度.销售商品提供劳务收到的现金/营业收入(算术平均)板块序列 -> getSecQfaSalesCashIntoOrAvgChNWses


# 获取单季度.经营活动产生的现金流量净额/营业收入(整体法)板块序列 -> getSecQfaOCFToOrOverallChNWses


# 获取单季度.经营活动产生的现金流量净额/营业收入(算术平均)板块序列 -> getSecQfaOCFToOrAvgChNWses


# 获取单季度.经营活动产生的现金流量净额/经营活动净收益(整体法)板块序列 -> getSecQfaOCFToOperateIncomeOverallChNWses


# 获取单季度.经营活动产生的现金流量净额/经营活动净收益(算术平均)板块序列 -> getSecQfaOCFToOperateIncomeAvgChNWses


# 获取单季度.营业总收入合计(同比增长率)板块序列 -> getSecQfaGrTotalYoYChNWses


# 获取单季度.营业总收入合计(环比增长率)板块序列 -> getSecQfaGrTotalMomChNWses


# 获取单季度.营业收入合计(同比增长率)板块序列 -> getSecQfaRevenueTotalYoYChNWses


# 获取单季度.营业收入合计(环比增长率)板块序列 -> getSecQfaRevenueTotalMomChNWses


# 获取单季度.营业利润合计(同比增长率)板块序列 -> getSecQfaOpTotalYoYChNWses


# 获取单季度.营业利润合计(环比增长率)板块序列 -> getSecQfaOpTotalMomChNWses


# 获取单季度.净利润合计(同比增长率)板块序列 -> getSecQfaNpTotalYoYChNWses


# 获取单季度.净利润合计(环比增长率)板块序列 -> getSecQfaNpTotalMomChNWses


# 获取单季度.归属母公司股东的净利润合计(同比增长率)板块序列 -> getSecQfaNpaSpcTotalYoYChNWses


# 获取单季度.归属母公司股东的净利润合计(环比增长率)板块序列 -> getSecQfaNpaSpcTotalMomChNWses


# 获取营业总成本(合计)板块序列 -> getSecGcSumChNWses


# 获取营业总成本(算术平均)板块序列 -> getSecGcAvgChNWses


# 获取营业收入(合计)板块序列 -> getSecOrSumChNWses


# 获取营业收入(算术平均)板块序列 -> getSecOrAvgChNWses


# 获取销售费用(合计)板块序列 -> getSecSellingExpSumChNWses


# 获取销售费用(算术平均)板块序列 -> getSecSellingExpAvgChNWses


# 获取管理费用(合计)板块序列 -> getSecMNgtExpSumChNWses


# 获取管理费用(算术平均)板块序列 -> getSecMNgtExpAvgChNWses


# 获取财务费用(合计)板块序列 -> getSecFineXpSumChNWses


# 获取财务费用(算术平均)板块序列 -> getSecFineXpAvgChNWses


# 获取投资净收益(合计)板块序列 -> getSecNiOnInvestmentSumChNWses


# 获取投资净收益(算术平均)板块序列 -> getSecNiOnInvestmentAvgChNWses


# 获取汇兑净收益(合计)板块序列 -> getSecNiOnForExSumChNWses


# 获取汇兑净收益(算术平均)板块序列 -> getSecNiOnForExAvgChNWses


# 获取公允价值变动净收益(合计)板块序列 -> getSecNiFromChangesInFvSumChNWses


# 获取公允价值变动净收益(算术平均)板块序列 -> getSecNiFromChangesInFvAvgChNWses


# 获取利润总额(合计)板块序列 -> getSecEBtSumChNWses


# 获取利润总额(算术平均)板块序列 -> getSecEBtAvgChNWses


# 获取归属母公司股东的净利润(合计)板块序列 -> getSecNpaSpcSumChNWses


# 获取归属母公司股东的净利润(算术平均)板块序列 -> getSecNpaSpcAvgChNWses


# 获取归属母公司股东的净利润-扣除非经常损益(合计)板块序列 -> getSecExNonRecurringPnLnPasPcSumChNWses


# 获取归属母公司股东的净利润-扣除非经常损益(算术平均)板块序列 -> getSecExNonRecurringPnLnPasPcAvgChNWses


# 获取经营活动净收益(合计)板块序列 -> getSecOperateIncomeSumChNWses


# 获取经营活动净收益(算术平均)板块序列 -> getSecOperateIncomeAvgChNWses


# 获取价值变动净收益(合计)板块序列 -> getSecInvestIncomeSumChNWses


# 获取价值变动净收益(算术平均)板块序列 -> getSecInvestIncomeAvgChNWses


# 获取货币资金(合计)板块序列 -> getSecCashSumChNWses


# 获取货币资金(算术平均)板块序列 -> getSecCashAvgChNWses


# 获取应收票据(合计)板块序列 -> getSecNotErSumChNWses


# 获取应收票据(算术平均)板块序列 -> getSecNotErAvgChNWses


# 获取应收账款(合计)板块序列 -> getSecArSumChNWses


# 获取应收账款(算术平均)板块序列 -> getSecArAvgChNWses


# 获取长期股权投资(合计)板块序列 -> getSecLteQtInvestmentSumChNWses


# 获取长期股权投资(算术平均)板块序列 -> getSecLteQtInvestmentAvgChNWses


# 获取投资性房地产(合计)板块序列 -> getSecInvestmentReSumChNWses


# 获取投资性房地产(算术平均)板块序列 -> getSecInvestmentReAvgChNWses


# 获取短期借款(合计)板块序列 -> getSecStDebtSumChNWses


# 获取短期借款(算术平均)板块序列 -> getSecStDebtAvgChNWses


# 获取应付票据(合计)板块序列 -> getSecNotEpSumChNWses


# 获取应付票据(算术平均)板块序列 -> getSecNotEpAvgChNWses


# 获取应付账款(合计)板块序列 -> getSecApSumChNWses


# 获取应付账款(算术平均)板块序列 -> getSecApAvgChNWses
#
# 获取最高价分钟序列 -> getHighWsi


# 获取最低价分钟序列 -> getLowWsi


# 获取收盘价分钟序列 -> getCloseWsi


# 获取成交量分钟序列 -> getVolumeWsi


# 获取成交额分钟序列 -> getAmtWsi


# 获取涨跌分钟序列 -> getChgWsi


# 获取涨跌幅分钟序列 -> getPctChgWsi


# 获取持仓量分钟序列 -> getOiWsi


# 获取开始时间分钟序列 -> getBeginTimeWsi


# 获取结束时间分钟序列 -> getEndTimeWsi


# 获取BIAS乖离率分钟序列 -> getBiasWsi


# 获取BOLL布林带分钟序列 -> getBollWsi


# 获取DMI趋向标准分钟序列 -> getDMiWsi


# 获取EXPMA指数平滑移动平均分钟序列 -> getExpMaWsi


# 获取HV历史波动率分钟序列 -> getHvWsi


# 获取KDJ随机指标分钟序列 -> getKDjWsi


# 获取MA简单移动平均分钟序列 -> getMaWsi


# 获取MACD指数平滑异同平均分钟序列 -> getMacDWsi


# 获取RSI相对强弱指标分钟序列 -> getRsiWsi
#
# 获取时间实时行情 -> getRtTimeWsq


# 获取前收实时行情 -> getRtPreCloseWsq


# 获取今开实时行情 -> getRtOpenWsq


# 获取最高实时行情 -> getRtHighWsq


# 获取最低实时行情 -> getRtLowWsq


# 获取现价实时行情 -> getRtLastWsq


# 获取现额实时行情 -> getRtLastAmtWsq


# 获取现量实时行情 -> getRtLastVolWsq


# 获取最新成交价实时行情 -> getRtLatestWsq


# 获取成交量实时行情 -> getRtVolWsq


# 获取成交额实时行情 -> getRtAmtWsq


# 获取涨跌实时行情 -> getRtChgWsq


# 获取涨跌幅实时行情 -> getRtPctChgWsq


# 获取涨停价实时行情 -> getRtHighLimitWsq


# 获取跌停价实时行情 -> getRtLowLimitWsq


# 获取盘前最新价实时行情 -> getRtPreLatestWsq


# 获取振幅实时行情 -> getRtSwingWsq


# 获取均价实时行情 -> getRtVWapWsq


# 获取外盘实时行情 -> getRtUpwardVolWsq


# 获取内盘实时行情 -> getRtDownwardVolWsq


# 获取最小价差实时行情 -> getRtMinSpreadWsq


# 获取交易状态实时行情 -> getRtTradeStatusWsq


# 获取52周最高实时行情 -> getRtHigh52WKWsq


# 获取52周最低实时行情 -> getRtLow52WKWsq


# 获取1分钟涨跌幅实时行情 -> getRtPctChg1MinWsq


# 获取3分钟涨跌幅实时行情 -> getRtPctChg3MinWsq


# 获取5分钟涨跌幅实时行情 -> getRtPctChg5MinWsq


# 获取5日涨跌幅实时行情 -> getRtPctChg5DWsq


# 获取10日涨跌幅实时行情 -> getRtPctChg10DWsq


# 获取20日涨跌幅实时行情 -> getRtPctChg20DWsq


# 获取60日涨跌幅实时行情 -> getRtPctChg60DWsq


# 获取120日涨跌幅实时行情 -> getRtPctChg120DWsq


# 获取250日涨跌幅实时行情 -> getRtPctChg250DWsq


# 获取年初至今涨跌幅实时行情 -> getRtPctChgYTdWsq


# 获取卖1价实时行情 -> getRtAsk1Wsq


# 获取卖2价实时行情 -> getRtAsk2Wsq


# 获取卖3价实时行情 -> getRtAsk3Wsq


# 获取卖4价实时行情 -> getRtAsk4Wsq


# 获取卖5价实时行情 -> getRtAsk5Wsq


# 获取卖6价实时行情 -> getRtAsk6Wsq


# 获取卖7价实时行情 -> getRtAsk7Wsq


# 获取卖8价实时行情 -> getRtAsk8Wsq


# 获取卖9价实时行情 -> getRtAsk9Wsq


# 获取卖10价实时行情 -> getRtAsk10Wsq


# 获取买1价实时行情 -> getRtBid1Wsq


# 获取买2价实时行情 -> getRtBid2Wsq


# 获取买3价实时行情 -> getRtBid3Wsq


# 获取买4价实时行情 -> getRtBid4Wsq


# 获取买5价实时行情 -> getRtBid5Wsq


# 获取买6价实时行情 -> getRtBid6Wsq


# 获取买7价实时行情 -> getRtBid7Wsq


# 获取买8价实时行情 -> getRtBid8Wsq


# 获取买9价实时行情 -> getRtBid9Wsq


# 获取买10价实时行情 -> getRtBid10Wsq


# 获取买1量实时行情 -> getRtBSize1Wsq


# 获取买2量实时行情 -> getRtBSize2Wsq


# 获取买3量实时行情 -> getRtBSize3Wsq


# 获取买4量实时行情 -> getRtBSize4Wsq


# 获取买5量实时行情 -> getRtBSize5Wsq


# 获取买6量实时行情 -> getRtBSize6Wsq


# 获取买7量实时行情 -> getRtBSize7Wsq


# 获取买8量实时行情 -> getRtBSize8Wsq


# 获取买9量实时行情 -> getRtBSize9Wsq


# 获取买10量实时行情 -> getRtBSize10Wsq


# 获取卖1量实时行情 -> getRtASize1Wsq


# 获取卖2量实时行情 -> getRtASize2Wsq


# 获取卖3量实时行情 -> getRtASize3Wsq


# 获取卖4量实时行情 -> getRtASize4Wsq


# 获取卖5量实时行情 -> getRtASize5Wsq


# 获取卖6量实时行情 -> getRtASize6Wsq


# 获取卖7量实时行情 -> getRtASize7Wsq


# 获取卖8量实时行情 -> getRtASize8Wsq


# 获取卖9量实时行情 -> getRtASize9Wsq


# 获取卖10量实时行情 -> getRtASize10Wsq


# 获取盘后时间实时行情 -> getRtPostMktTimeWsq


# 获取盘后现量实时行情 -> getRtPostMktLastVolWsq


# 获取盘后最新成交价实时行情 -> getRtPostMktLatestWsq


# 获取盘后成交量实时行情 -> getRtPostMktVolWsq


# 获取盘后成交额实时行情 -> getRtPostMktAmtWsq


# 获取盘后涨跌实时行情 -> getRtPostMktChgWsq


# 获取盘后涨跌幅实时行情 -> getRtPostMktPctChgWsq


# 获取盘后成交笔数实时行情 -> getRtPostMktDealNumWsq


# 获取当日净流入率实时行情 -> getRtMfRatioWsq


# 获取5日净流入率实时行情 -> getRtMfRatio5DWsq


# 获取10日净流入率实时行情 -> getRtMfRatio10DWsq


# 获取20日净流入率实时行情 -> getRtMfRatio20DWsq


# 获取60日净流入率实时行情 -> getRtMfRatio60DWsq


# 获取5日净流入天数实时行情 -> getRtMfdays5DWsq


# 获取10日净流入天数实时行情 -> getRtMfdays10DWsq


# 获取20日净流入天数实时行情 -> getRtMfdays20DWsq


# 获取60日净流入天数实时行情 -> getRtMfdays60DWsq


# 获取当日净流入额实时行情 -> getRtMfAmtWsq


# 获取5日净流入额实时行情 -> getRtMfAmt5DWsq


# 获取10日净流入额实时行情 -> getRtMfAmt10DWsq


# 获取20日净流入额实时行情 -> getRtMfAmt20DWsq


# 获取60日净流入额实时行情 -> getRtMfAmt60DWsq


# 获取委买总量实时行情 -> getRtBidVolWsq


# 获取委卖总量实时行情 -> getRtAskVolWsq


# 获取委买十档总量实时行情 -> getRtBSizeTotalWsq


# 获取委卖十档总量实时行情 -> getRtASizeTotalWsq


# 获取机构大户买入单总数实时行情 -> getRtInStiVipBidWsq


# 获取机构大户卖出单总数实时行情 -> getRtInStiVipAskWsq


# 获取当日机构大户净流入占比实时行情 -> getRtInStiVipNetInFlowRatioWsq


# 获取逐笔成交累计成交量实时行情 -> getRtTransSumVolWsq


# 获取当日机构买入成交量实时行情 -> getRtInStiBuyVolWsq


# 获取当日机构卖出成交量实时行情 -> getRtInStiSellVolWsq


# 获取当日大户买入成交量实时行情 -> getRtVipBuyVolWsq


# 获取当日大户卖出成交量实时行情 -> getRtVipSellVolWsq


# 获取当日中户买入成交量实时行情 -> getRtMidBuyVolWsq


# 获取当日中户卖出成交量实时行情 -> getRtMidSellVolWsq


# 获取当日散户买入成交量实时行情 -> getRtInDiBuyVolWsq


# 获取当日散户卖出成交量实时行情 -> getRtInDiSellVolWsq


# 获取当日机构净买入成交量实时行情 -> getRtInStiNetBuyVolWsq


# 获取当日大户净买入成交量实时行情 -> getRtVipNetBuyVolWsq


# 获取当日中户净买入成交量实时行情 -> getRtMidNetBuyVolWsq


# 获取当日散户净买入成交量实时行情 -> getRtInDiNetBuyVolWsq


# 获取当日机构买单总数实时行情 -> getRtInStiTotalBidWsq


# 获取当日机构卖单总数实时行情 -> getRtInStiTotalAskWsq


# 获取当日大户买单总数实时行情 -> getRtVipTotalBidWsq


# 获取当日大户卖单总数实时行情 -> getRtVipTotalAskWsq


# 获取当日中户买单总数实时行情 -> getRtMidTotalBidWsq


# 获取当日中户卖单总数实时行情 -> getRtMidTotalAskWsq


# 获取当日散户买单总数实时行情 -> getRtInDiTotalBidWsq


# 获取当日散户卖单总数实时行情 -> getRtInDiTotalAskWsq


# 获取机构资金净流入实时行情 -> getRtInStiInFlowWsq


# 获取大户资金净流入实时行情 -> getRtVipInFlowWsq


# 获取中户资金净流入实时行情 -> getRtMidInFlowWsq


# 获取散户资金净流入实时行情 -> getRtInDiInFlowWsq


# 获取当日机构买入成交额实时行情 -> getRtInStiBuyAmtWsq


# 获取当日机构卖出成交额实时行情 -> getRtInStiSellAmtWsq


# 获取当日大户买入成交额实时行情 -> getRtVipBuyAmtWsq


# 获取当日大户卖出成交额实时行情 -> getRtVipSellAmtWsq


# 获取当日中户买入成交额实时行情 -> getRtMidBuyAmtWsq


# 获取当日中户卖出成交额实时行情 -> getRtMidSellAmtWsq


# 获取当日散户买入成交额实时行情 -> getRtInDiBuyAmtWsq


# 获取当日散户卖出成交额实时行情 -> getRtInDiSellAmtWsq


# 获取机构主买入金额实时行情 -> getRtInStiActiveBuyAmtWsq


# 获取大户主买入金额实时行情 -> getRtVipActiveBuyAmtWsq


# 获取中户主买入金额实时行情 -> getRtMidActiveBuyAmtWsq


# 获取散户主买入金额实时行情 -> getRtInDiActiveBuyAmtWsq


# 获取机构主买入总量实时行情 -> getRtInStiActiveBuyVolWsq


# 获取大户主买入总量实时行情 -> getRtVipActiveBuyVolWsq


# 获取中户主买入总量实时行情 -> getRtMidActiveBuyVolWsq


# 获取散户主买入总量实时行情 -> getRtInDiActiveBuyVolWsq


# 获取机构主卖出金额实时行情 -> getRtInStiActiveSellAmtWsq


# 获取大户主卖出金额实时行情 -> getRtVipActiveSellAmtWsq


# 获取中户主卖出金额实时行情 -> getRtMidActiveSellAmtWsq


# 获取散户主卖出金额实时行情 -> getRtInDiActiveSellAmtWsq


# 获取机构主卖出总量实时行情 -> getRtInStiActiveSellVolWsq


# 获取大户主卖出总量实时行情 -> getRtVipActiveSellVolWsq


# 获取中户主卖出总量实时行情 -> getRtMidActiveSellVolWsq


# 获取散户主卖出总量实时行情 -> getRtInDiActiveSellVolWsq


# 获取主买总额实时行情 -> getRtActiveBuyAmtWsq


# 获取主买总量实时行情 -> getRtActiveBuyVolWsq


# 获取主卖总额实时行情 -> getRtActiveSellAmtWsq


# 获取主卖总量实时行情 -> getRtActiveSellVolWsq


# 获取资金主动净流入量实时行情 -> getRtActiveNetInvolWsq


# 获取资金主动净流入金额实时行情 -> getRtActiveNetInAmtWsq


# 获取资金主动流向占比(量)实时行情 -> getRtActiveInvolPropWsq


# 获取资金主动流向占比(金额)实时行情 -> getRtActiveInFlowPropWsq


# 获取港股通当日可用总额实时行情 -> getRtHkConnectTotalAmountWsq


# 获取港股通当日已用额实时行情 -> getRtHkConnectAmountUsedWsq


# 获取港股通当日剩余可用额实时行情 -> getRtHkConnectAmountRemainWsq


# 获取当日净买入实时行情 -> getRtNetBuyAmountWsq


# 获取港股通当日买入实时行情 -> getRtBuyOrderWsq


# 获取港股通当日卖出实时行情 -> getRtSellOrderWsq


# 获取港股通当日总成交实时行情 -> getRtTotalVolWsq


# 获取最新复权因子实时行情 -> getRtAdjFactorWsq


# 获取当笔成交方向实时行情 -> getRtDirectionWsq


# 获取量比实时行情 -> getRtVolRatioWsq


# 获取委比实时行情 -> getRtCommitteeWsq


# 获取委差实时行情 -> getRtCommissionWsq


# 获取换手率实时行情 -> getRtTurnWsq


# 获取总市值实时行情 -> getRtMktCapWsq


# 获取流通市值实时行情 -> getRtFloatMktCapWsq


# 获取连涨天数实时行情 -> getRtRiseDaysWsq


# 获取停牌标志实时行情 -> getRtSUspFlagWsq


# 获取5日MA实时行情 -> getRtMa5DWsq


# 获取10日MA实时行情 -> getRtMa10DWsq


# 获取20日MA实时行情 -> getRtMa20DWsq


# 获取60日MA实时行情 -> getRtMa60DWsq


# 获取120日MA实时行情 -> getRtMa120DWsq


# 获取250日MA实时行情 -> getRtMa250DWsq


# 获取市盈率TTM实时行情 -> getRtPeTtMWsq


# 获取市净率LF实时行情 -> getRtPbLfWsq


# 获取MACD实时行情 -> getRtMacDWsq


# 获取MACD_DIFF实时行情 -> getRtMacDDiffWsq


# 获取KDJ_K实时行情 -> getRtKDjKWsq


# 获取KDJ_D实时行情 -> getRtKDjDWsq


# 获取KDJ_J实时行情 -> getRtKDjJWsq


# 获取CCI指标实时行情 -> getRtCci14Wsq


# 获取虚拟成交量实时行情 -> getRtVirtualVolumeWsq


# 获取虚拟成交额实时行情 -> getRtVirtualAmountWsq


# 获取全价最新价实时行情 -> getRtLastDpWsq


# 获取净价最新价实时行情 -> getRtLastCpWsq


# 获取收益率最新价实时行情 -> getRtLastYTMWsq


# 获取全价前收价实时行情 -> getRtPreCloseDpWsq


# 获取期现价差实时行情 -> getRtDeliverySpdWsq


# 获取IRR实时行情 -> getRtIRrWsq


# 获取基差实时行情 -> getRtSpreadWsq


# 获取买1价到期收益率实时行情 -> getRtBidPrice1YTMWsq


# 获取卖1价到期收益率实时行情 -> getRtAskPrice1YTMWsq


# 获取买1价行权收益率实时行情 -> getRtBidPrice1YTeWsq


# 获取卖1价行权收益率实时行情 -> getRtAskPrice1YTeWsq


# 获取均价收益率实时行情 -> getRtAvgYTMWsq


# 获取最新收益率BP实时行情 -> getRtYTMBpWsq


# 获取麦氏久期实时行情 -> getRtMacDurationWsq


# 获取债券最优报价组合实时行情 -> getRtBestBaWsq


# 获取债券最优买报价收益率实时行情 -> getRtBestBidYTMWsq


# 获取债券最优买券面总额实时行情 -> getRtBestBidAmtWsq


# 获取债券最优卖报价收益率实时行情 -> getRtBestAskYTMWsq


# 获取债券最优卖券面总额实时行情 -> getRtBestAskAmtWsq


# 获取转股溢价率实时行情 -> getOverflowRatioWsq


# 获取正股换手率实时行情 -> getRtUStockTurnoverWsq


# 获取转股价格实时行情 -> getRtConVPriceWsq


# 获取转股比例实时行情 -> getRtConVRatioWsq


# 获取转股价值实时行情 -> getRtConVValueWsq


# 获取套利空间实时行情 -> getRtArbSpaceWsq


# 获取纯债价值实时行情 -> getRtNBondPriceWsq


# 获取纯债溢价率实时行情 -> getRtNBondPremWsq


# 获取权证价格实时行情 -> getRtWarrantPriceWsq


# 获取到期收益率实时行情 -> getRtYTMWsq


# 获取平价底价溢价率实时行情 -> getRtPjDjWsq


# 获取可转债类型实时行情 -> getRtConVTypeWsq


# 获取当期票息实时行情 -> getRtCurrentCouponWsq


# 获取债券余额实时行情 -> getRtAmtOutstandingWsq


# 获取剩余期限实时行情 -> getRtRemainMaturityWsq


# 获取双低实时行情 -> getRtBiHarmonicStrategyWsq


# 获取昨IOPV实时行情 -> getRtPreIoPvWsq


# 获取IOPV实时行情 -> getRtIoPvWsq


# 获取折价实时行情 -> getRtDiscountWsq


# 获取折价率实时行情 -> getRtDiscountRatioWsq


# 获取贴水率实时行情 -> getRtConTangoRatioWsq


# 获取估算涨跌幅实时行情 -> getRtEstimatedChgWsq


# 获取前持仓量实时行情 -> getRtPreOiWsq


# 获取持仓量实时行情 -> getRtOiWsq


# 获取日增仓实时行情 -> getRtOiChgWsq


# 获取增仓实时行情 -> getRtOiChangeWsq


# 获取性质实时行情 -> getRtNatureWsq


# 获取前结算价实时行情 -> getRtPreSettleWsq


# 获取结算价实时行情 -> getRtSettleWsq


# 获取预估结算价实时行情 -> getRtEstSettleWsq


# 获取Delta实时行情 -> getRtDeltaWsq


# 获取Gamma实时行情 -> getRtGammaWsq


# 获取Vega实时行情 -> getRtVegaWsq


# 获取Theta实时行情 -> getRtThetaWsq


# 获取Rho实时行情 -> getRtRhoWsq


# 获取隐含波动率实时行情 -> getRtImpVolatilityWsq


# 获取中价隐含波动率实时行情 -> getRtMIvWsq


# 获取买一隐含波动率实时行情 -> getRtBid1IvLWsq


# 获取买二隐含波动率实时行情 -> getRtBid2IvLWsq


# 获取买三隐含波动率实时行情 -> getRtBid3IvLWsq


# 获取买四隐含波动率实时行情 -> getRtBid4IvLWsq


# 获取买五隐含波动率实时行情 -> getRtBid5IvLWsq


# 获取买六隐含波动率实时行情 -> getRtBid6IvLWsq


# 获取买七隐含波动率实时行情 -> getRtBid7IvLWsq


# 获取买八隐含波动率实时行情 -> getRtBid8IvLWsq


# 获取买九隐含波动率实时行情 -> getRtBid9IvLWsq


# 获取买十隐含波动率实时行情 -> getRtBid10IvLWsq


# 获取卖一隐含波动率实时行情 -> getRtAsk1IvLWsq


# 获取卖二隐含波动率实时行情 -> getRtAsk2IvLWsq


# 获取卖三隐含波动率实时行情 -> getRtAsk3IvLWsq


# 获取卖四隐含波动率实时行情 -> getRtAsk4IvLWsq


# 获取卖五隐含波动率实时行情 -> getRtAsk5IvLWsq


# 获取卖六隐含波动率实时行情 -> getRtAsk6IvLWsq


# 获取卖七隐含波动率实时行情 -> getRtAsk7IvLWsq


# 获取卖八隐含波动率实时行情 -> getRtAsk8IvLWsq


# 获取卖九隐含波动率实时行情 -> getRtAsk9IvLWsq


# 获取卖十隐含波动率实时行情 -> getRtAsk10IvLWsq


# 获取正股价格实时行情 -> getRtUStockPriceWsq


# 获取正股涨跌幅实时行情 -> getRtUStockChgWsq


# 获取内在价值实时行情 -> getRtIntValueWsq


# 获取时间价值实时行情 -> getRtTimeValueWsq


# 获取时间价值（标的）实时行情 -> getRtTvAssetWsq


# 获取实际杠杆倍数实时行情 -> getRtActLmWsq


# 获取保证金实时行情 -> getRtOptMarginWsq


# 获取指数属性实时行情 -> getRtOptNrWsq


# 获取期权价值状态实时行情 -> getRtOptVsWsq


# 获取理论价格实时行情 -> getRtOptTheoryPriceWsq


# 获取前隐含波动率实时行情 -> getRtPreIvWsq


# 获取隐含波动率涨跌幅实时行情 -> getRtIvChangeWsq


# 获取最优买卖价差实时行情 -> getRtBidAsKspreadWsq


# 获取期权成交量实时行情 -> getRtOptVolWsq


# 获取期权持仓量实时行情 -> getRtOptOiWsq


# 获取成交量PCR实时行情 -> getRtVolPcrWsq


# 获取上涨家数实时行情 -> getRtUpTotalWsq


# 获取平盘家数实时行情 -> getRtSameTotalWsq


# 获取下跌家数实时行情 -> getRtDownTotalWsq


# 获取领先指标实时行情 -> getRtLeadingIndicatorsWsq


# 获取RSI_6指标实时行情 -> getRtRsi6DWsq


# 获取RSI_12指标实时行情 -> getRtRsi12DWsq
#
# 获取开盘价日内跳价 -> getOpenWst


# 获取最高价日内跳价 -> getHighWst


# 获取最低价日内跳价 -> getLowWst


# 获取最新价日内跳价 -> getLastWst


# 获取卖价日内跳价 -> getAskWst


# 获取买价日内跳价 -> getBidWst


# 获取成交量日内跳价 -> getVolumeWst


# 获取成交额日内跳价 -> getAmtWst


# 获取前结算价日内跳价 -> getPreSettleWst


# 获取结算价日内跳价 -> getSettleWst


# 获取前持仓量日内跳价 -> getPreOiWst


# 获取持仓量日内跳价 -> getOiWst


# 获取量比日内跳价 -> getVolRatioWst


# 获取盘后最新成交价日内跳价 -> getAfterPriceWst


# 获取盘后成交量日内跳价 -> getAfterVolumeWst


# 获取盘后成交额日内跳价 -> getAfterTurnoverWst


# 获取卖10价日内跳价 -> getAsk10Wst


# 获取卖9价日内跳价 -> getAsk9Wst


# 获取卖8价日内跳价 -> getAsk8Wst


# 获取卖7价日内跳价 -> getAsk7Wst


# 获取卖6价日内跳价 -> getAsk6Wst


# 获取卖5价日内跳价 -> getAsk5Wst


# 获取卖4价日内跳价 -> getAsk4Wst


# 获取卖3价日内跳价 -> getAsk3Wst


# 获取卖2价日内跳价 -> getAsk2Wst


# 获取卖1价日内跳价 -> getAsk1Wst


# 获取买1价日内跳价 -> getBid1Wst


# 获取买2价日内跳价 -> getBid2Wst


# 获取买3价日内跳价 -> getBid3Wst


# 获取买4价日内跳价 -> getBid4Wst


# 获取买8价日内跳价 -> getBid8Wst


# 获取买9价日内跳价 -> getBid9Wst


# 获取买10价日内跳价 -> getBid10Wst


# 获取卖10量日内跳价 -> getASize10Wst


# 获取卖9量日内跳价 -> getASize9Wst


# 获取卖8量日内跳价 -> getASize8Wst


# 获取卖7量日内跳价 -> getASize7Wst


# 获取卖6量日内跳价 -> getASize6Wst


# 获取卖5量日内跳价 -> getASize5Wst


# 获取卖4量日内跳价 -> getASize4Wst


# 获取卖3量日内跳价 -> getASize3Wst


# 获取卖2量日内跳价 -> getASize2Wst


# 获取卖1量日内跳价 -> getASize1Wst


# 获取买1量日内跳价 -> getBSize1Wst


# 获取买2量日内跳价 -> getBSize2Wst


# 获取买3量日内跳价 -> getBSize3Wst


# 获取买4量日内跳价 -> getBSize4Wst


# 获取买5量日内跳价 -> getBSize5Wst


# 获取买6量日内跳价 -> getBSize6Wst


# 获取买7量日内跳价 -> getBSize7Wst


# 获取买8量日内跳价 -> getBSize8Wst


# 获取买9量日内跳价 -> getBSize9Wst


# 获取买10量日内跳价 -> getBSize10Wst


# 获取IOPV日内跳价 -> getIoPvWst


# 获取涨停价日内跳价 -> getLimitUpWst


# 获取跌停价日内跳价 -> getLimitDownWst


# 获取买5价日内跳价 -> getBid5Wst


# 获取买6价日内跳价 -> getBid6Wst


# 获取买7价日内跳价 -> getBid7Wst

#-<End>









