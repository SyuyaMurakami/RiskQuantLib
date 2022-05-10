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
def convertInputSecurityType(func):
    def convertedFunc(*args):
        args = tuple((i.strftime("%Y-%m-%d") if hasattr(i,"strftime") else i for i in args))
        if type(args[0])==type(''):
            return func(*args)[1].fillna(np.nan)
        else:
            security = args[0]
            args = args[1:]
            return func(",".join(security),*args)[1].fillna(np.nan)
    return convertedFunc
@convertInputSecurityType
def getDoubleLowSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取双低时间序列
    return w.wsd(security,"doublelow",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDoubleLow(security:list,*args,**kwargs):
    # 获取双低
    return w.wss(security,"doublelow",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getVolRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取量比时间序列
    return w.wsd(security,"vol_ratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getVolRatio(security:list,*args,**kwargs):
    # 获取量比
    return w.wss(security,"vol_ratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskDownsideSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取回撤(相对前期高点)时间序列
    return w.wsd(security,"risk_downside",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskDownside(security:list,*args,**kwargs):
    # 获取回撤(相对前期高点)
    return w.wss(security,"risk_downside",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTaxRateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取税率时间序列
    return w.wsd(security,"taxrate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTaxRate(security:list,*args,**kwargs):
    # 获取税率
    return w.wss(security,"taxrate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGoodwillSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取商誉时间序列
    return w.wsd(security,"goodwill",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGoodwill(security:list,*args,**kwargs):
    # 获取商誉
    return w.wss(security,"goodwill",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOthersSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他时间序列
    return w.wsd(security,"others",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOthers(security:list,*args,**kwargs):
    # 获取其他
    return w.wss(security,"others",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBaseValueSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基点时间序列
    return w.wsd(security,"basevalue",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBaseValue(security:list,*args,**kwargs):
    # 获取基点
    return w.wss(security,"basevalue",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBaseDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基期时间序列
    return w.wsd(security,"basedate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBaseDate(security:list,*args,**kwargs):
    # 获取基期
    return w.wss(security,"basedate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getProvinceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取省份时间序列
    return w.wsd(security,"province",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getProvince(security:list,*args,**kwargs):
    # 获取省份
    return w.wss(security,"province",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechLnHighLow20DSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取LN(最近一个月最高价/最近一个月最低价)_PIT时间序列
    return w.wsd(security,"tech_lnhighlow20d",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechLnHighLow20D(security:list,*args,**kwargs):
    # 获取LN(最近一个月最高价/最近一个月最低价)_PIT
    return w.wss(security,"tech_lnhighlow20d",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCitySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取城市时间序列
    return w.wsd(security,"city",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCity(security:list,*args,**kwargs):
    # 获取城市
    return w.wss(security,"city",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthGp3YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取毛利(近3年增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_gp_3y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthGp3Y(security:list,*args,**kwargs):
    # 获取毛利(近3年增长率)_GSD
    return w.wss(security,"wgsd_growth_gp_3y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthGp1YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取毛利(近1年增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_gp_1y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthGp1Y(security:list,*args,**kwargs):
    # 获取毛利(近1年增长率)_GSD
    return w.wss(security,"wgsd_growth_gp_1y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRsvSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取储备_GSD时间序列
    return w.wsd(security,"wgsd_rsv",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRsv(security:list,*args,**kwargs):
    # 获取储备_GSD
    return w.wss(security,"wgsd_rsv",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEwa02004Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取氨氮时间序列
    return w.wsd(security,"esg_ewa02004",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEwa02004(security:list,*args,**kwargs):
    # 获取氨氮
    return w.wss(security,"esg_ewa02004",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrossMarginTtM2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取毛利(TTM)时间序列
    return w.wsd(security,"grossmargin_ttm2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrossMarginTtM2(security:list,*args,**kwargs):
    # 获取毛利(TTM)
    return w.wss(security,"grossmargin_ttm2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrossMarginSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取毛利时间序列
    return w.wsd(security,"grossmargin",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrossMargin(security:list,*args,**kwargs):
    # 获取毛利
    return w.wss(security,"grossmargin",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrossMarginTtM3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取毛利(TTM)_GSD时间序列
    return w.wsd(security,"grossmargin_ttm3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrossMarginTtM3(security:list,*args,**kwargs):
    # 获取毛利(TTM)_GSD
    return w.wss(security,"grossmargin_ttm3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrossMargin2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取毛利_GSD时间序列
    return w.wsd(security,"wgsd_grossmargin2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrossMargin2(security:list,*args,**kwargs):
    # 获取毛利_GSD
    return w.wss(security,"wgsd_grossmargin2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getZipCodeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取邮编时间序列
    return w.wsd(security,"zipcode",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getZipCode(security:list,*args,**kwargs):
    # 获取邮编
    return w.wss(security,"zipcode",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaGpTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取毛利(TTM)_PIT时间序列
    return w.wsd(security,"fa_gp_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaGpTtM(security:list,*args,**kwargs):
    # 获取毛利(TTM)_PIT
    return w.wss(security,"fa_gp_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCalcConVSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取凸性时间序列
    return w.wsd(security,"calc_conv",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCalcConV(security:list,*args,**kwargs):
    # 获取凸性
    return w.wss(security,"calc_conv",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalBasisSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基差(商品期货)时间序列
    return w.wsd(security,"anal_basis",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalBasis(security:list,*args,**kwargs):
    # 获取基差(商品期货)
    return w.wss(security,"anal_basis",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerAgeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取年龄时间序列
    return w.wsd(security,"fund_manager_age",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerAge(security:list,*args,**kwargs):
    # 获取年龄
    return w.wss(security,"fund_manager_age",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDQChangeCnBdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取涨跌(中债)时间序列
    return w.wsd(security,"dq_change_cnbd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDQChangeCnBd(security:list,*args,**kwargs):
    # 获取涨跌(中债)
    return w.wss(security,"dq_change_cnbd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerEducationSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取学历时间序列
    return w.wsd(security,"fund_manager_education",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerEducation(security:list,*args,**kwargs):
    # 获取学历
    return w.wss(security,"fund_manager_education",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getChgSettlementSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取涨跌(结算价)时间序列
    return w.wsd(security,"chg_settlement",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getChgSettlement(security:list,*args,**kwargs):
    # 获取涨跌(结算价)
    return w.wss(security,"chg_settlement",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getChgSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取涨跌时间序列
    return w.wsd(security,"chg",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getChg(security:list,*args,**kwargs):
    # 获取涨跌
    return w.wss(security,"chg",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInAuditAgencySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取内控_审计单位时间序列
    return w.wsd(security,"stmnote_InAudit_agency",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInAuditAgency(security:list,*args,**kwargs):
    # 获取内控_审计单位
    return w.wss(security,"stmnote_InAudit_agency",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInAuditInterpretationSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取内控_审计结果说明时间序列
    return w.wsd(security,"stmnote_InAudit_interpretation",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInAuditInterpretation(security:list,*args,**kwargs):
    # 获取内控_审计结果说明
    return w.wss(security,"stmnote_InAudit_interpretation",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInAuditCpaSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取内控_签字审计师时间序列
    return w.wsd(security,"stmnote_InAudit_cpa",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInAuditCpa(security:list,*args,**kwargs):
    # 获取内控_签字审计师
    return w.wss(security,"stmnote_InAudit_cpa",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEstRpTAbstractInStSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取内容时间序列
    return w.wsd(security,"est_rptabstract_inst",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEstRpTAbstractInSt(security:list,*args,**kwargs):
    # 获取内容
    return w.wss(security,"est_rptabstract_inst",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerNationalitySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取国籍时间序列
    return w.wsd(security,"fund_manager_nationality",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerNationality(security:list,*args,**kwargs):
    # 获取国籍
    return w.wss(security,"fund_manager_nationality",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDInventoriesSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取存货_GSD时间序列
    return w.wsd(security,"wgsd_inventories",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDInventories(security:list,*args,**kwargs):
    # 获取存货_GSD
    return w.wss(security,"wgsd_inventories",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSwingSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取振幅时间序列
    return w.wsd(security,"swing",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSwing(security:list,*args,**kwargs):
    # 获取振幅
    return w.wss(security,"swing",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerResumeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取简历时间序列
    return w.wsd(security,"fund_manager_resume",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerResume(security:list,*args,**kwargs):
    # 获取简历
    return w.wss(security,"fund_manager_resume",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerGenderSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取性别时间序列
    return w.wsd(security,"fund_manager_gender",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerGender(security:list,*args,**kwargs):
    # 获取性别
    return w.wss(security,"fund_manager_gender",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getVWapSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取均价时间序列
    return w.wsd(security,"vwap",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getVWap(security:list,*args,**kwargs):
    # 获取均价
    return w.wss(security,"vwap",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfBasisSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基差时间序列
    return w.wsd(security,"tbf_basis",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfBasis(security:list,*args,**kwargs):
    # 获取基差
    return w.wss(security,"tbf_basis",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIfBasisSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基差(股指期货)时间序列
    return w.wsd(security,"if_basis",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIfBasis(security:list,*args,**kwargs):
    # 获取基差(股指期货)
    return w.wss(security,"if_basis",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInAuditCategorySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取内控_审计意见类别时间序列
    return w.wsd(security,"stmnote_InAudit_category",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInAuditCategory(security:list,*args,**kwargs):
    # 获取内控_审计意见类别
    return w.wss(security,"stmnote_InAudit_category",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInventoriesSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取存货时间序列
    return w.wsd(security,"inventories",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInventories(security:list,*args,**kwargs):
    # 获取存货
    return w.wss(security,"inventories",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrossMarginTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取毛利(TTM,只有最新数据)时间序列
    return w.wsd(security,"grossmargin_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrossMarginTtM(security:list,*args,**kwargs):
    # 获取毛利(TTM,只有最新数据)
    return w.wss(security,"grossmargin_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDiscountSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取贴水时间序列
    return w.wsd(security,"discount",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDiscount(security:list,*args,**kwargs):
    # 获取贴水
    return w.wss(security,"discount",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisSwingSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取振幅_期货历史同月时间序列
    return w.wsd(security,"His_swing",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisSwing(security:list,*args,**kwargs):
    # 获取振幅_期货历史同月
    return w.wss(security,"His_swing",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundParValueSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取面值时间序列
    return w.wsd(security,"fund_parvalue",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundParValue(security:list,*args,**kwargs):
    # 获取面值
    return w.wss(security,"fund_parvalue",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisChangeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取涨跌_期货历史同月时间序列
    return w.wsd(security,"His_change",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisChange(security:list,*args,**kwargs):
    # 获取涨跌_期货历史同月
    return w.wss(security,"His_change",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisChangeSettlementSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取涨跌(结算价)_期货历史同月时间序列
    return w.wsd(security,"His_change_settlement",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisChangeSettlement(security:list,*args,**kwargs):
    # 获取涨跌(结算价)_期货历史同月
    return w.wss(security,"His_change_settlement",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMktCapCsrCSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总市值(证监会算法)时间序列
    return w.wsd(security,"mkt_cap_CSRC",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMktCapCsrC(security:list,*args,**kwargs):
    # 获取总市值(证监会算法)
    return w.wss(security,"mkt_cap_CSRC",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfNetBasisSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净基差时间序列
    return w.wsd(security,"tbf_netbasis",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfNetBasis(security:list,*args,**kwargs):
    # 获取净基差
    return w.wss(security,"tbf_netbasis",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechBollUpSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取上轨线(布林线)_PIT时间序列
    return w.wsd(security,"tech_bollup",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechBollUp(security:list,*args,**kwargs):
    # 获取上轨线(布林线)_PIT
    return w.wss(security,"tech_bollup",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareOtcTradableOthersSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取流通股(其他)时间序列
    return w.wsd(security,"share_otctradable_others",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareOtcTradableOthers(security:list,*args,**kwargs):
    # 获取流通股(其他)
    return w.wss(security,"share_otctradable_others",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOiNvOiSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净持仓(品种)时间序列
    return w.wsd(security,"oi_nvoi",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOiNvOi(security:list,*args,**kwargs):
    # 获取净持仓(品种)
    return w.wss(security,"oi_nvoi",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareOtcTradableBackboneSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取流通股(核心员工)时间序列
    return w.wsd(security,"share_otctradable_backbone",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareOtcTradableBackbone(security:list,*args,**kwargs):
    # 获取流通股(核心员工)
    return w.wss(security,"share_otctradable_backbone",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur11Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取费用率(产险)时间序列
    return w.wsd(security,"stmnote_insur_11",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur11(security:list,*args,**kwargs):
    # 获取费用率(产险)
    return w.wss(security,"stmnote_insur_11",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur10Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取赔付率(产险)时间序列
    return w.wsd(security,"stmnote_insur_10",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur10(security:list,*args,**kwargs):
    # 获取赔付率(产险)
    return w.wss(security,"stmnote_insur_10",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareOtcTradableControllerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取流通股(控股股东或实际控制人)时间序列
    return w.wsd(security,"share_otctradable_controller",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareOtcTradableController(security:list,*args,**kwargs):
    # 获取流通股(控股股东或实际控制人)
    return w.wss(security,"share_otctradable_controller",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoYProfitSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净利润(同比增长率)时间序列
    return w.wsd(security,"yoyprofit",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoYProfit(security:list,*args,**kwargs):
    # 获取净利润(同比增长率)
    return w.wss(security,"yoyprofit",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDividendYield2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取股息率(近12个月)_PIT时间序列
    return w.wsd(security,"dividendyield2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDividendYield2(security:list,*args,**kwargs):
    # 获取股息率(近12个月)_PIT
    return w.wss(security,"dividendyield2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDQuantityGoldSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取交收量(黄金现货)时间序列
    return w.wsd(security,"dquantity_gold",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDQuantityGold(security:list,*args,**kwargs):
    # 获取交收量(黄金现货)
    return w.wss(security,"dquantity_gold",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur8Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取退保率时间序列
    return w.wsd(security,"stmnote_insur_8",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur8(security:list,*args,**kwargs):
    # 获取退保率
    return w.wss(security,"stmnote_insur_8",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs79TotalSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净利润(合计)_FUND时间序列
    return w.wsd(security,"stm_is_79_total",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs79Total(security:list,*args,**kwargs):
    # 获取净利润(合计)_FUND
    return w.wss(security,"stm_is_79_total",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs79Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取净利润_FUND时间序列
    return w.wsd(security,"stm_is_79",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs79(security:list,*args,**kwargs):
    # 获取净利润_FUND
    return w.wss(security,"stm_is_79",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetProfitCsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净利润_CS时间序列
    return w.wsd(security,"net_profit_cs",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetProfitCs(security:list,*args,**kwargs):
    # 获取净利润_CS
    return w.wss(security,"net_profit_cs",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDiscountRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取贴水率时间序列
    return w.wsd(security,"discount_ratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDiscountRatio(security:list,*args,**kwargs):
    # 获取贴水率
    return w.wss(security,"discount_ratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMaxDownSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取跌停价时间序列
    return w.wsd(security,"maxdown",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMaxDown(security:list,*args,**kwargs):
    # 获取跌停价
    return w.wss(security,"maxdown",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMaxUpSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取涨停价时间序列
    return w.wsd(security,"maxup",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMaxUp(security:list,*args,**kwargs):
    # 获取涨停价
    return w.wss(security,"maxup",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisOpenSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取开盘价_期货历史同月时间序列
    return w.wsd(security,"His_open",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisOpen(security:list,*args,**kwargs):
    # 获取开盘价_期货历史同月
    return w.wss(security,"His_open",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalBasisPercent2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取基差率(商品期货)时间序列
    return w.wsd(security,"anal_basispercent2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalBasisPercent2(security:list,*args,**kwargs):
    # 获取基差率(商品期货)
    return w.wss(security,"anal_basispercent2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRhoSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取Rho时间序列
    return w.wsd(security,"rho",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRho(security:list,*args,**kwargs):
    # 获取Rho
    return w.wss(security,"rho",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPctChangeCloseSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取涨跌幅(收盘价)时间序列
    return w.wsd(security,"pctchange_close",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPctChangeClose(security:list,*args,**kwargs):
    # 获取涨跌幅(收盘价)
    return w.wss(security,"pctchange_close",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07IsReItsNetProfitSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净利润时间序列
    return w.wsd(security,"stm07_is_reits_netprofit",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07IsReItsNetProfit(security:list,*args,**kwargs):
    # 获取净利润
    return w.wss(security,"stm07_is_reits_netprofit",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthDebt3YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总负债(近3年增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_debt_3y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthDebt3Y(security:list,*args,**kwargs):
    # 获取总负债(近3年增长率)_GSD
    return w.wss(security,"wgsd_growth_debt_3y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoLimitUpOpenDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取开板日时间序列
    return w.wsd(security,"ipo_limitupopendate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoLimitUpOpenDate(security:list,*args,**kwargs):
    # 获取开板日
    return w.wss(security,"ipo_limitupopendate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOiSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取持仓量时间序列
    return w.wsd(security,"oi",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOi(security:list,*args,**kwargs):
    # 获取持仓量
    return w.wss(security,"oi",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getVolumEBTInSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取成交量(含大宗交易)时间序列
    return w.wsd(security,"volume_btin",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getVolumEBTIn(security:list,*args,**kwargs):
    # 获取成交量(含大宗交易)
    return w.wss(security,"volume_btin",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyDistributorSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取分销商时间序列
    return w.wsd(security,"agency_distributor",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyDistributor(security:list,*args,**kwargs):
    # 获取分销商
    return w.wss(security,"agency_distributor",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMktSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取上市板时间序列
    return w.wsd(security,"mkt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMkt(security:list,*args,**kwargs):
    # 获取上市板
    return w.wss(security,"mkt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfIRr2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取IRR(支持历史)时间序列
    return w.wsd(security,"tbf_IRR2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfIRr2(security:list,*args,**kwargs):
    # 获取IRR(支持历史)
    return w.wss(security,"tbf_IRR2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getVolumeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取成交量时间序列
    return w.wsd(security,"volume",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getVolume(security:list,*args,**kwargs):
    # 获取成交量
    return w.wss(security,"volume",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyTrusteeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取托管人时间序列
    return w.wsd(security,"agency_trustee",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyTrustee(security:list,*args,**kwargs):
    # 获取托管人
    return w.wss(security,"agency_trustee",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRhoExChSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取Rho(交易所)时间序列
    return w.wsd(security,"rho_exch",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRhoExCh(security:list,*args,**kwargs):
    # 获取Rho(交易所)
    return w.wss(security,"rho_exch",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTurnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取换手率时间序列
    return w.wsd(security,"turn",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTurn(security:list,*args,**kwargs):
    # 获取换手率
    return w.wss(security,"turn",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFreeTurnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取换手率(基准.自由流通股本)时间序列
    return w.wsd(security,"free_turn",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFreeTurn(security:list,*args,**kwargs):
    # 获取换手率(基准.自由流通股本)
    return w.wss(security,"free_turn",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoYEquitySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净资产(同比增长率)时间序列
    return w.wsd(security,"yoy_equity",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoYEquity(security:list,*args,**kwargs):
    # 获取净资产(同比增长率)
    return w.wss(security,"yoy_equity",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStDeVrSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取波动率时间序列
    return w.wsd(security,"stdevr",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStDeVr(security:list,*args,**kwargs):
    # 获取波动率
    return w.wss(security,"stdevr",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisCloseNightSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取收盘价(夜盘)_期货历史同月时间序列
    return w.wsd(security,"His_close_night",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisCloseNight(security:list,*args,**kwargs):
    # 获取收盘价(夜盘)_期货历史同月
    return w.wss(security,"His_close_night",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalBasisPercentSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基差率(股指期货)时间序列
    return w.wsd(security,"anal_basispercent",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalBasisPercent(security:list,*args,**kwargs):
    # 获取基差率(股指期货)
    return w.wss(security,"anal_basispercent",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechBollDownSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取下轨线(布林线)_PIT时间序列
    return w.wsd(security,"tech_bolldown",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechBollDown(security:list,*args,**kwargs):
    # 获取下轨线(布林线)_PIT
    return w.wss(security,"tech_bolldown",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisCloseSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取收盘价_期货历史同月时间序列
    return w.wsd(security,"His_close",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisClose(security:list,*args,**kwargs):
    # 获取收盘价_期货历史同月
    return w.wss(security,"His_close",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDTreAsStKSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取库存股_GSD时间序列
    return w.wsd(security,"wgsd_treas_stk",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDTreAsStK(security:list,*args,**kwargs):
    # 获取库存股_GSD
    return w.wss(security,"wgsd_treas_stk",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTSyStKSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取库存股时间序列
    return w.wsd(security,"tsy_stk",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTSyStK(security:list,*args,**kwargs):
    # 获取库存股
    return w.wss(security,"tsy_stk",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfIRrSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取IRR时间序列
    return w.wsd(security,"tbf_IRR",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfIRr(security:list,*args,**kwargs):
    # 获取IRR
    return w.wss(security,"tbf_IRR",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDAssetsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总资产_GSD时间序列
    return w.wsd(security,"wgsd_assets",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDAssets(security:list,*args,**kwargs):
    # 获取总资产_GSD
    return w.wss(security,"wgsd_assets",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCleanPriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取收盘价(净价)时间序列
    return w.wsd(security,"cleanprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCleanPrice(security:list,*args,**kwargs):
    # 获取收盘价(净价)
    return w.wss(security,"cleanprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDirtyPriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取收盘价(全价)时间序列
    return w.wsd(security,"dirtyprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDirtyPrice(security:list,*args,**kwargs):
    # 获取收盘价(全价)
    return w.wss(security,"dirtyprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLow3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取最低价(不前推)时间序列
    return w.wsd(security,"low3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLow3(security:list,*args,**kwargs):
    # 获取最低价(不前推)
    return w.wss(security,"low3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLowSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最低价时间序列
    return w.wsd(security,"low",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLow(security:list,*args,**kwargs):
    # 获取最低价
    return w.wss(security,"low",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisVolumeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取成交量_期货历史同月时间序列
    return w.wsd(security,"His_volume",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisVolume(security:list,*args,**kwargs):
    # 获取成交量_期货历史同月
    return w.wss(security,"His_volume",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisLowSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最低价_期货历史同月时间序列
    return w.wsd(security,"His_low",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisLow(security:list,*args,**kwargs):
    # 获取最低价_期货历史同月
    return w.wss(security,"His_low",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaProfitTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净利润(TTM)_PIT时间序列
    return w.wsd(security,"fa_profit_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaProfitTtM(security:list,*args,**kwargs):
    # 获取净利润(TTM)_PIT
    return w.wss(security,"fa_profit_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDLiAbsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总负债_GSD时间序列
    return w.wsd(security,"wgsd_liabs",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDLiAbs(security:list,*args,**kwargs):
    # 获取总负债_GSD
    return w.wss(security,"wgsd_liabs",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisSettleSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取结算价_期货历史同月时间序列
    return w.wsd(security,"His_settle",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisSettle(security:list,*args,**kwargs):
    # 获取结算价_期货历史同月
    return w.wss(security,"His_settle",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSec1Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取净资本时间序列
    return w.wsd(security,"stmnote_sec_1",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSec1(security:list,*args,**kwargs):
    # 获取净资本
    return w.wss(security,"stmnote_sec_1",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHigh3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取最高价(不前推)时间序列
    return w.wsd(security,"high3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHigh3(security:list,*args,**kwargs):
    # 获取最高价(不前推)
    return w.wss(security,"high3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHighSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最高价时间序列
    return w.wsd(security,"high",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHigh(security:list,*args,**kwargs):
    # 获取最高价
    return w.wss(security,"high",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSettle3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取结算价(不前推)时间序列
    return w.wsd(security,"settle3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSettle3(security:list,*args,**kwargs):
    # 获取结算价(不前推)
    return w.wss(security,"settle3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSettleSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取结算价时间序列
    return w.wsd(security,"settle",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSettle(security:list,*args,**kwargs):
    # 获取结算价
    return w.wss(security,"settle",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOiAmountSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取持仓额时间序列
    return w.wsd(security,"oiamount",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOiAmount(security:list,*args,**kwargs):
    # 获取持仓额
    return w.wss(security,"oiamount",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOiAmountNoMarginSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取持仓额(不计保证金)时间序列
    return w.wsd(security,"oiamount_nomargin",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOiAmountNoMargin(security:list,*args,**kwargs):
    # 获取持仓额(不计保证金)
    return w.wss(security,"oiamount_nomargin",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisPctChangeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取涨跌幅_期货历史同月时间序列
    return w.wsd(security,"His_pctchange",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisPctChange(security:list,*args,**kwargs):
    # 获取涨跌幅_期货历史同月
    return w.wss(security,"His_pctchange",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDividendYield2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取股息率(近12个月)时间序列
    return w.wsd(security,"dividendyield2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDividendYield2(security:list,*args,**kwargs):
    # 获取股息率(近12个月)
    return w.wss(security,"dividendyield2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOpen3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取开盘价(不前推)时间序列
    return w.wsd(security,"open3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOpen3(security:list,*args,**kwargs):
    # 获取开盘价(不前推)
    return w.wss(security,"open3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOpenSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取开盘价时间序列
    return w.wsd(security,"open",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOpen(security:list,*args,**kwargs):
    # 获取开盘价
    return w.wss(security,"open",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDividendYieldSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取股息率(报告期)时间序列
    return w.wsd(security,"dividendyield",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDividendYield(security:list,*args,**kwargs):
    # 获取股息率(报告期)
    return w.wss(security,"dividendyield",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOi3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取持仓量(不前推)时间序列
    return w.wsd(security,"oi3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOi3(security:list,*args,**kwargs):
    # 获取持仓量(不前推)
    return w.wss(security,"oi3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowDiscNtRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取折扣率时间序列
    return w.wsd(security,"fellow_discntratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowDiscNtRatio(security:list,*args,**kwargs):
    # 获取折扣率
    return w.wss(security,"fellow_discntratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRepurchaseDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取回售日时间序列
    return w.wsd(security,"repurchasedate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRepurchaseDate(security:list,*args,**kwargs):
    # 获取回售日
    return w.wss(security,"repurchasedate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthDebt1YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总负债(近1年增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_debt_1y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthDebt1Y(security:list,*args,**kwargs):
    # 获取总负债(近1年增长率)_GSD
    return w.wss(security,"wgsd_growth_debt_1y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValMvArdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总市值时间序列
    return w.wsd(security,"val_mv_ARD",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValMvArd(security:list,*args,**kwargs):
    # 获取总市值
    return w.wss(security,"val_mv_ARD",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTaxTtM2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取所得税(TTM)_GSD时间序列
    return w.wsd(security,"tax_ttm2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTaxTtM2(security:list,*args,**kwargs):
    # 获取所得税(TTM)_GSD
    return w.wss(security,"tax_ttm2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDNetIncCfSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净利润_CS_GSD时间序列
    return w.wsd(security,"wgsd_net_inc_cf",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDNetIncCf(security:list,*args,**kwargs):
    # 获取净利润_CS_GSD
    return w.wss(security,"wgsd_net_inc_cf",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCloseNightSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取收盘价(夜盘)时间序列
    return w.wsd(security,"close_night",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCloseNight(security:list,*args,**kwargs):
    # 获取收盘价(夜盘)
    return w.wss(security,"close_night",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisOiSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取持仓量_期货历史同月时间序列
    return w.wsd(security,"His_oi",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisOi(security:list,*args,**kwargs):
    # 获取持仓量_期货历史同月
    return w.wss(security,"His_oi",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCloseUsdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取收盘价(美元)时间序列
    return w.wsd(security,"close_usd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCloseUsd(security:list,*args,**kwargs):
    # 获取收盘价(美元)
    return w.wss(security,"close_usd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCloseFxSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取收盘价(23:30)时间序列
    return w.wsd(security,"close_FX",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCloseFx(security:list,*args,**kwargs):
    # 获取收盘价(23:30)
    return w.wss(security,"close_FX",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRedemptionBeginningSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取兑付日时间序列
    return w.wsd(security,"redemption_beginning",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRedemptionBeginning(security:list,*args,**kwargs):
    # 获取兑付日
    return w.wss(security,"redemption_beginning",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClose3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取收盘价(不前推)时间序列
    return w.wsd(security,"close3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClose3(security:list,*args,**kwargs):
    # 获取收盘价(不前推)
    return w.wss(security,"close3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClose2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取收盘价(支持定点复权)时间序列
    return w.wsd(security,"close2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClose2(security:list,*args,**kwargs):
    # 获取收盘价(支持定点复权)
    return w.wss(security,"close2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisTurnoverSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取成交额_期货历史同月时间序列
    return w.wsd(security,"His_turnover",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisTurnover(security:list,*args,**kwargs):
    # 获取成交额_期货历史同月
    return w.wss(security,"His_turnover",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCloseSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取收盘价时间序列
    return w.wsd(security,"close",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClose(security:list,*args,**kwargs):
    # 获取收盘价
    return w.wss(security,"close",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDNetIncSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净利润_GSD时间序列
    return w.wsd(security,"wgsd_net_inc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDNetInc(security:list,*args,**kwargs):
    # 获取净利润_GSD
    return w.wss(security,"wgsd_net_inc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDNoGaapProfitSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净利润(Non-GAAP)_GSD时间序列
    return w.wsd(security,"wgsd_nogaapprofit",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDNoGaapProfit(security:list,*args,**kwargs):
    # 获取净利润(Non-GAAP)_GSD
    return w.wss(security,"wgsd_nogaapprofit",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getProfitTtM3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取净利润(TTM)_GSD时间序列
    return w.wsd(security,"profit_ttm3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getProfitTtM3(security:list,*args,**kwargs):
    # 获取净利润(TTM)_GSD
    return w.wss(security,"profit_ttm3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMktCapSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总市值(不可回测)时间序列
    return w.wsd(security,"mkt_cap",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMktCap(security:list,*args,**kwargs):
    # 获取总市值(不可回测)
    return w.wss(security,"mkt_cap",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisHighSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最高价_期货历史同月时间序列
    return w.wsd(security,"His_high",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisHigh(security:list,*args,**kwargs):
    # 获取最高价_期货历史同月
    return w.wss(security,"His_high",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getProfitTtM2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取净利润(TTM)时间序列
    return w.wsd(security,"profit_ttm2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getProfitTtM2(security:list,*args,**kwargs):
    # 获取净利润(TTM)
    return w.wss(security,"profit_ttm2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRedemptionDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取赎回日时间序列
    return w.wsd(security,"redemptiondate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRedemptionDate(security:list,*args,**kwargs):
    # 获取赎回日
    return w.wss(security,"redemptiondate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaTaxTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取所得税(TTM)_PIT时间序列
    return w.wsd(security,"fa_tax_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaTaxTtM(security:list,*args,**kwargs):
    # 获取所得税(TTM)_PIT
    return w.wss(security,"fa_tax_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDQCloseCnBdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取指数值(中债)时间序列
    return w.wsd(security,"dq_close_cnbd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDQCloseCnBd(security:list,*args,**kwargs):
    # 获取指数值(中债)
    return w.wss(security,"dq_close_cnbd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTaxSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取所得税时间序列
    return w.wsd(security,"tax",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTax(security:list,*args,**kwargs):
    # 获取所得税
    return w.wss(security,"tax",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDIncTaxSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取所得税_GSD时间序列
    return w.wsd(security,"wgsd_inc_tax",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDIncTax(security:list,*args,**kwargs):
    # 获取所得税_GSD
    return w.wss(security,"wgsd_inc_tax",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTaxTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取所得税(TTM)时间序列
    return w.wsd(security,"tax_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTaxTtM(security:list,*args,**kwargs):
    # 获取所得税(TTM)
    return w.wss(security,"tax_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthAsset3YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总资产(近3年增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_asset_3y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthAsset3Y(security:list,*args,**kwargs):
    # 获取总资产(近3年增长率)_GSD
    return w.wss(security,"wgsd_growth_asset_3y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStDeVrySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取波动率(年化)时间序列
    return w.wsd(security,"stdevry",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStDeVry(security:list,*args,**kwargs):
    # 获取波动率(年化)
    return w.wss(security,"stdevry",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOiIndexSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取持仓量(商品指数)时间序列
    return w.wsd(security,"oi_index",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOiIndex(security:list,*args,**kwargs):
    # 获取持仓量(商品指数)
    return w.wss(security,"oi_index",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank5444Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取净息差(公布值)时间序列
    return w.wsd(security,"stmnote_bank_5444",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank5444(security:list,*args,**kwargs):
    # 获取净息差(公布值)
    return w.wss(security,"stmnote_bank_5444",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank144NSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净息差时间序列
    return w.wsd(security,"stmnote_bank_144_n",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank144N(security:list,*args,**kwargs):
    # 获取净息差
    return w.wss(security,"stmnote_bank_144_n",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdBuyAmtDSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取流入额时间序列
    return w.wsd(security,"mfd_buyamt_d",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdBuyAmtD(security:list,*args,**kwargs):
    # 获取流入额
    return w.wss(security,"mfd_buyamt_d",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoYDebtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总负债(同比增长率)时间序列
    return w.wsd(security,"yoydebt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoYDebt(security:list,*args,**kwargs):
    # 获取总负债(同比增长率)
    return w.wss(security,"yoydebt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCeoSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总经理时间序列
    return w.wsd(security,"ceo",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCeo(security:list,*args,**kwargs):
    # 获取总经理
    return w.wss(security,"ceo",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsRecommendCprSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取早偿率时间序列
    return w.wsd(security,"abs_recommendcpr",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsRecommendCpr(security:list,*args,**kwargs):
    # 获取早偿率
    return w.wss(security,"abs_recommendcpr",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteTaxBuildingSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取房产税时间序列
    return w.wsd(security,"stmnote_tax_building",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteTaxBuilding(security:list,*args,**kwargs):
    # 获取房产税
    return w.wss(security,"stmnote_tax_building",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteTaxStampSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取印花税时间序列
    return w.wsd(security,"stmnote_tax_stamp",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteTaxStamp(security:list,*args,**kwargs):
    # 获取印花税
    return w.wss(security,"stmnote_tax_stamp",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getArdBsPerpetualSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取永续债_合计_GSD时间序列
    return w.wsd(security,"ard_bs_perpetual",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getArdBsPerpetual(security:list,*args,**kwargs):
    # 获取永续债_合计_GSD
    return w.wss(security,"ard_bs_perpetual",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdSellAmtDSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取流出额时间序列
    return w.wsd(security,"mfd_sellamt_d",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdSellAmtD(security:list,*args,**kwargs):
    # 获取流出额
    return w.wss(security,"mfd_sellamt_d",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdBuyVolDSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取流入量时间序列
    return w.wsd(security,"mfd_buyvol_d",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdBuyVolD(security:list,*args,**kwargs):
    # 获取流入量
    return w.wss(security,"mfd_buyvol_d",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNeEqListingDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取挂牌日时间序列
    return w.wsd(security,"neeq_listingdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNeEqListingDate(security:list,*args,**kwargs):
    # 获取挂牌日
    return w.wss(security,"neeq_listingdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoYAssetsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总资产(同比增长率)时间序列
    return w.wsd(security,"yoy_assets",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoYAssets(security:list,*args,**kwargs):
    # 获取总资产(同比增长率)
    return w.wss(security,"yoy_assets",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getConVPriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取转股价时间序列
    return w.wsd(security,"convprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getConVPrice(security:list,*args,**kwargs):
    # 获取转股价
    return w.wss(security,"convprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPreciousMetalsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取贵金属时间序列
    return w.wsd(security,"precious_metals",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPreciousMetals(security:list,*args,**kwargs):
    # 获取贵金属
    return w.wss(security,"precious_metals",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEre01007Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取节能量时间序列
    return w.wsd(security,"esg_ere01007",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEre01007(security:list,*args,**kwargs):
    # 获取节能量
    return w.wss(security,"esg_ere01007",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdSellVolDSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取流出量时间序列
    return w.wsd(security,"mfd_sellvol_d",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdSellVolD(security:list,*args,**kwargs):
    # 获取流出量
    return w.wss(security,"mfd_sellvol_d",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPctChgSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取涨跌幅时间序列
    return w.wsd(security,"pct_chg",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPctChg(security:list,*args,**kwargs):
    # 获取涨跌幅
    return w.wss(security,"pct_chg",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPctChgBSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取涨跌幅(债券)时间序列
    return w.wsd(security,"pct_chg_b",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPctChgB(security:list,*args,**kwargs):
    # 获取涨跌幅(债券)
    return w.wss(security,"pct_chg_b",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivPayDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取派息日时间序列
    return w.wsd(security,"div_paydate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivPayDate(security:list,*args,**kwargs):
    # 获取派息日
    return w.wss(security,"div_paydate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsDprFSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取派息率(预测)时间序列
    return w.wsd(security,"fund_reitsdprf",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsDprF(security:list,*args,**kwargs):
    # 获取派息率(预测)
    return w.wss(security,"fund_reitsdprf",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTotalSharesSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总股本时间序列
    return w.wsd(security,"total_shares",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTotalShares(security:list,*args,**kwargs):
    # 获取总股本
    return w.wss(security,"total_shares",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteOthers7630Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取租赁费(销售费用)时间序列
    return w.wsd(security,"stmnote_others_7630",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteOthers7630(security:list,*args,**kwargs):
    # 获取租赁费(销售费用)
    return w.wss(security,"stmnote_others_7630",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank144Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取净息差(旧)时间序列
    return w.wsd(security,"stmnote_bank_144",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank144(security:list,*args,**kwargs):
    # 获取净息差(旧)
    return w.wss(security,"stmnote_bank_144",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBoardChairmenSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取董事长时间序列
    return w.wsd(security,"boardchairmen",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBoardChairmen(security:list,*args,**kwargs):
    # 获取董事长
    return w.wss(security,"boardchairmen",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechMassSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取梅斯线_PIT时间序列
    return w.wsd(security,"tech_mass",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechMass(security:list,*args,**kwargs):
    # 获取梅斯线_PIT
    return w.wss(security,"tech_mass",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDQPctChangeCnBdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取涨跌幅(中债)时间序列
    return w.wsd(security,"dq_pctchange_cnbd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDQPctChangeCnBd(security:list,*args,**kwargs):
    # 获取涨跌幅(中债)
    return w.wss(security,"dq_pctchange_cnbd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAmountBtInSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取成交额(含大宗交易)时间序列
    return w.wsd(security,"amount_btin",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAmountBtIn(security:list,*args,**kwargs):
    # 获取成交额(含大宗交易)
    return w.wss(security,"amount_btin",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAmtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取成交额时间序列
    return w.wsd(security,"amt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAmt(security:list,*args,**kwargs):
    # 获取成交额
    return w.wss(security,"amt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthAsset1YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总资产(近1年增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_asset_1y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthAsset1Y(security:list,*args,**kwargs):
    # 获取总资产(近1年增长率)_GSD
    return w.wss(security,"wgsd_growth_asset_1y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGSem03001Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取工伤率时间序列
    return w.wsd(security,"esg_sem03001",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGSem03001(security:list,*args,**kwargs):
    # 获取工伤率
    return w.wss(security,"esg_sem03001",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPctChgSettlementSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取涨跌幅(结算价)时间序列
    return w.wsd(security,"pct_chg_settlement",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPctChgSettlement(security:list,*args,**kwargs):
    # 获取涨跌幅(结算价)
    return w.wss(security,"pct_chg_settlement",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank147NSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净利差时间序列
    return w.wsd(security,"stmnote_bank_147_n",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank147N(security:list,*args,**kwargs):
    # 获取净利差
    return w.wss(security,"stmnote_bank_147_n",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteTaxConstructionSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取城建税时间序列
    return w.wsd(security,"stmnote_tax_construction",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteTaxConstruction(security:list,*args,**kwargs):
    # 获取城建税
    return w.wss(security,"stmnote_tax_construction",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank147Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取净利差(旧)时间序列
    return w.wsd(security,"stmnote_bank_147",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank147(security:list,*args,**kwargs):
    # 获取净利差(旧)
    return w.wss(security,"stmnote_bank_147",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfCTdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取CTD时间序列
    return w.wsd(security,"tbf_CTD",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfCTd(security:list,*args,**kwargs):
    # 获取CTD
    return w.wss(security,"tbf_CTD",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPrepaySurRSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取退保金时间序列
    return w.wsd(security,"prepay_surr",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPrepaySurR(security:list,*args,**kwargs):
    # 获取退保金
    return w.wss(security,"prepay_surr",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthNp3YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净利润(近3年增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_np_3y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthNp3Y(security:list,*args,**kwargs):
    # 获取净利润(近3年增长率)_GSD
    return w.wss(security,"wgsd_growth_np_3y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfCTd2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取CTD(支持历史)时间序列
    return w.wsd(security,"tbf_CTD2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfCTd2(security:list,*args,**kwargs):
    # 获取CTD(支持历史)
    return w.wss(security,"tbf_CTD2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthNp1YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净利润(近1年增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_np_1y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthNp1Y(security:list,*args,**kwargs):
    # 获取净利润(近1年增长率)_GSD
    return w.wss(security,"wgsd_growth_np_1y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getArdBsPerPParSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取永续债_归属于母公司股东_GSD时间序列
    return w.wsd(security,"ard_bs_perp_par",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getArdBsPerPPar(security:list,*args,**kwargs):
    # 获取永续债_归属于母公司股东_GSD
    return w.wss(security,"ard_bs_perp_par",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getArdBsPerPMinSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取永续债_归属于少数股东_GSD时间序列
    return w.wsd(security,"ard_bs_perp_min",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getArdBsPerPMin(security:list,*args,**kwargs):
    # 获取永续债_归属于少数股东_GSD
    return w.wss(security,"ard_bs_perp_min",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsPaymentDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取支付日时间序列
    return w.wsd(security,"abs_paymentdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsPaymentDate(security:list,*args,**kwargs):
    # 获取支付日
    return w.wss(security,"abs_paymentdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrowthProfitSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净利润(N年,增长率)时间序列
    return w.wsd(security,"growth_profit",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrowthProfit(security:list,*args,**kwargs):
    # 获取净利润(N年,增长率)
    return w.wss(security,"growth_profit",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderUnderwritingCostSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取承揽费时间序列
    return w.wsd(security,"tender_underwritingcost",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderUnderwritingCost(security:list,*args,**kwargs):
    # 获取承揽费
    return w.wss(security,"tender_underwritingcost",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank171Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取杠杆率时间序列
    return w.wsd(security,"stmnote_bank_171",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank171(security:list,*args,**kwargs):
    # 获取杠杆率
    return w.wss(security,"stmnote_bank_171",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundIssuingPlaceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行地(信托)时间序列
    return w.wsd(security,"fund_issuingplace",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundIssuingPlace(security:list,*args,**kwargs):
    # 获取发行地(信托)
    return w.wss(security,"fund_issuingplace",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundTrusteeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取受托人(信托)时间序列
    return w.wsd(security,"fund_trustee",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundTrustee(security:list,*args,**kwargs):
    # 获取受托人(信托)
    return w.wss(security,"fund_trustee",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaNetDebtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净债务_PIT时间序列
    return w.wsd(security,"fa_netdebt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaNetDebt(security:list,*args,**kwargs):
    # 获取净债务_PIT
    return w.wss(security,"fa_netdebt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValPerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取PER(LYR)时间序列
    return w.wsd(security,"val_per",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValPer(security:list,*args,**kwargs):
    # 获取PER(LYR)
    return w.wss(security,"val_per",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisPctChangeSettlementSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取涨跌幅(结算价)_期货历史同月时间序列
    return w.wsd(security,"His_pctchange_settlement",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisPctChangeSettlement(security:list,*args,**kwargs):
    # 获取涨跌幅(结算价)_期货历史同月
    return w.wss(security,"His_pctchange_settlement",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyGuarantorSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取担保人时间序列
    return w.wsd(security,"agency_guarantor",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyGuarantor(security:list,*args,**kwargs):
    # 获取担保人
    return w.wss(security,"agency_guarantor",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank55Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取拨贷比时间序列
    return w.wsd(security,"stmnote_bank_55",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank55(security:list,*args,**kwargs):
    # 获取拨贷比
    return w.wss(security,"stmnote_bank_55",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareNtrDPrFShareSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取优先股时间序列
    return w.wsd(security,"share_ntrd_prfshare",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareNtrDPrFShare(security:list,*args,**kwargs):
    # 获取优先股
    return w.wss(security,"share_ntrd_prfshare",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetDebtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净债务时间序列
    return w.wsd(security,"netdebt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetDebt(security:list,*args,**kwargs):
    # 获取净债务
    return w.wss(security,"netdebt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteOthers7631Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取租赁费(管理费用)时间序列
    return w.wsd(security,"stmnote_others_7631",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteOthers7631(security:list,*args,**kwargs):
    # 获取租赁费(管理费用)
    return w.wss(security,"stmnote_others_7631",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundWarrantOrSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取保证人时间序列
    return w.wsd(security,"fund_warrantor",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundWarrantOr(security:list,*args,**kwargs):
    # 获取保证人
    return w.wss(security,"fund_warrantor",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDDepositsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总存款_GSD时间序列
    return w.wsd(security,"wgsd_deposits",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDDeposits(security:list,*args,**kwargs):
    # 获取总存款_GSD
    return w.wss(security,"wgsd_deposits",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDPfDStKSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取优先股_GSD时间序列
    return w.wsd(security,"wgsd_pfd_stk",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDPfDStK(security:list,*args,**kwargs):
    # 获取优先股_GSD
    return w.wss(security,"wgsd_pfd_stk",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDNetDebt2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取净债务_GSD时间序列
    return w.wsd(security,"wgsd_netdebt2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDNetDebt2(security:list,*args,**kwargs):
    # 获取净债务_GSD
    return w.wss(security,"wgsd_netdebt2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteTaxConsumptionSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取消费税时间序列
    return w.wsd(security,"stmnote_tax_consumption",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteTaxConsumption(security:list,*args,**kwargs):
    # 获取消费税
    return w.wss(security,"stmnote_tax_consumption",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getConstInProgSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取在建工程时间序列
    return w.wsd(security,"const_in_prog",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getConstInProg(security:list,*args,**kwargs):
    # 获取在建工程
    return w.wss(security,"const_in_prog",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNatureSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取公司属性(旧)时间序列
    return w.wsd(security,"nature",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNature(security:list,*args,**kwargs):
    # 获取公司属性(旧)
    return w.wss(security,"nature",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getProJMAtlSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取工程物资时间序列
    return w.wsd(security,"proj_matl",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getProJMAtl(security:list,*args,**kwargs):
    # 获取工程物资
    return w.wss(security,"proj_matl",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowExpenseSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取增发费用时间序列
    return w.wsd(security,"fellow_expense",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowExpense(security:list,*args,**kwargs):
    # 获取增发费用
    return w.wss(security,"fellow_expense",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEv2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取企业价值(剔除货币资金)时间序列
    return w.wsd(security,"ev2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEv2(security:list,*args,**kwargs):
    # 获取企业价值(剔除货币资金)
    return w.wss(security,"ev2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskMaxUpsideSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最大上涨时间序列
    return w.wsd(security,"risk_maxupside",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskMaxUpside(security:list,*args,**kwargs):
    # 获取最大上涨
    return w.wss(security,"risk_maxupside",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRAndDCostsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取开发支出时间序列
    return w.wsd(security,"r_and_d_costs",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRAndDCosts(security:list,*args,**kwargs):
    # 获取开发支出
    return w.wss(security,"r_and_d_costs",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDYoYOrSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业收入(同比增长率)_GSD时间序列
    return w.wsd(security,"wgsd_yoy_or",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDYoYOr(security:list,*args,**kwargs):
    # 获取营业收入(同比增长率)_GSD
    return w.wss(security,"wgsd_yoy_or",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYOyEBTSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取利润总额(同比增长率)时间序列
    return w.wsd(security,"yoyebt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYOyEBT(security:list,*args,**kwargs):
    # 获取利润总额(同比增长率)
    return w.wss(security,"yoyebt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration3YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取3年久期时间序列
    return w.wsd(security,"duration_3y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration3Y(security:list,*args,**kwargs):
    # 获取3年久期
    return w.wss(security,"duration_3y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerBirthYearSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取出生年份时间序列
    return w.wsd(security,"fund_manager_birthyear",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerBirthYear(security:list,*args,**kwargs):
    # 获取出生年份
    return w.wss(security,"fund_manager_birthyear",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration5YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取5年久期时间序列
    return w.wsd(security,"duration_5y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration5Y(security:list,*args,**kwargs):
    # 获取5年久期
    return w.wss(security,"duration_5y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPutCodeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取回售代码时间序列
    return w.wsd(security,"putcode",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPutCode(security:list,*args,**kwargs):
    # 获取回售代码
    return w.wss(security,"putcode",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration4YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取4年久期时间序列
    return w.wsd(security,"duration_4y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration4Y(security:list,*args,**kwargs):
    # 获取4年久期
    return w.wss(security,"duration_4y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNature1Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取公司属性时间序列
    return w.wsd(security,"nature1",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNature1(security:list,*args,**kwargs):
    # 获取公司属性
    return w.wss(security,"nature1",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowAmountSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取增发数量时间序列
    return w.wsd(security,"fellow_amount",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowAmount(security:list,*args,**kwargs):
    # 获取增发数量
    return w.wss(security,"fellow_amount",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowPriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取增发价格时间序列
    return w.wsd(security,"fellow_price",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowPrice(security:list,*args,**kwargs):
    # 获取增发价格
    return w.wss(security,"fellow_price",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowProgressSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取增发进度时间序列
    return w.wsd(security,"fellow_progress",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowProgress(security:list,*args,**kwargs):
    # 获取增发进度
    return w.wss(security,"fellow_progress",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEv1Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取企业价值(含货币资金)时间序列
    return w.wsd(security,"ev1",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEv1(security:list,*args,**kwargs):
    # 获取企业价值(含货币资金)
    return w.wss(security,"ev1",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTimeDepositsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取定期存款时间序列
    return w.wsd(security,"time_deposits",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTimeDeposits(security:list,*args,**kwargs):
    # 获取定期存款
    return w.wss(security,"time_deposits",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCuStBankDepSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取吸收存款时间序列
    return w.wsd(security,"cust_bank_dep",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCuStBankDep(security:list,*args,**kwargs):
    # 获取吸收存款
    return w.wss(security,"cust_bank_dep",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration7YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取7年久期时间序列
    return w.wsd(security,"duration_7y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration7Y(security:list,*args,**kwargs):
    # 获取7年久期
    return w.wss(security,"duration_7y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLoansOThBanksSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取拆入资金时间序列
    return w.wsd(security,"loans_oth_banks",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLoansOThBanks(security:list,*args,**kwargs):
    # 获取拆入资金
    return w.wss(security,"loans_oth_banks",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getConVRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取转股比例时间序列
    return w.wsd(security,"convratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getConVRatio(security:list,*args,**kwargs):
    # 获取转股比例
    return w.wss(security,"convratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getConVValueSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取转换价值时间序列
    return w.wsd(security,"convvalue",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getConVValue(security:list,*args,**kwargs):
    # 获取转换价值
    return w.wss(security,"convvalue",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSpecialRsRvSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取专项储备时间序列
    return w.wsd(security,"special_rsrv",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSpecialRsRv(security:list,*args,**kwargs):
    # 获取专项储备
    return w.wss(security,"special_rsrv",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getConVPremiumSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取转股溢价时间序列
    return w.wsd(security,"convpremium",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getConVPremium(security:list,*args,**kwargs):
    # 获取转股溢价
    return w.wss(security,"convpremium",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBondsPayableSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取应付债券时间序列
    return w.wsd(security,"bonds_payable",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBondsPayable(security:list,*args,**kwargs):
    # 获取应付债券
    return w.wss(security,"bonds_payable",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPremReceivedAdvSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取预收保费时间序列
    return w.wsd(security,"prem_received_adv",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPremReceivedAdv(security:list,*args,**kwargs):
    # 获取预收保费
    return w.wss(security,"prem_received_adv",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfCVf2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取转换因子时间序列
    return w.wsd(security,"tbf_cvf2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfCVf2(security:list,*args,**kwargs):
    # 获取转换因子
    return w.wss(security,"tbf_cvf2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfCVfSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取转换因子(指定合约)时间序列
    return w.wsd(security,"tbf_cvf",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfCVf(security:list,*args,**kwargs):
    # 获取转换因子(指定合约)
    return w.wss(security,"tbf_cvf",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfSpreadSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取期现价差时间序列
    return w.wsd(security,"tbf_spread",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfSpread(security:list,*args,**kwargs):
    # 获取期现价差
    return w.wss(security,"tbf_spread",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfInvoicePriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发票价格时间序列
    return w.wsd(security,"tbf_invoiceprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfInvoicePrice(security:list,*args,**kwargs):
    # 获取发票价格
    return w.wss(security,"tbf_invoiceprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfDeliverPriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取交割成本时间序列
    return w.wsd(security,"tbf_deliverprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfDeliverPrice(security:list,*args,**kwargs):
    # 获取交割成本
    return w.wss(security,"tbf_deliverprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfPaymentSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间利息时间序列
    return w.wsd(security,"tbf_payment",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfPayment(security:list,*args,**kwargs):
    # 获取区间利息
    return w.wss(security,"tbf_payment",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfInterestSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取交割利息时间序列
    return w.wsd(security,"tbf_interest",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfInterest(security:list,*args,**kwargs):
    # 获取交割利息
    return w.wss(security,"tbf_interest",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfCVf3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取转换因子(主力合约)时间序列
    return w.wsd(security,"tbf_cvf3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfCVf3(security:list,*args,**kwargs):
    # 获取转换因子(主力合约)
    return w.wss(security,"tbf_cvf3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTimeValueSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取时间价值时间序列
    return w.wsd(security,"timevalue",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTimeValue(security:list,*args,**kwargs):
    # 获取时间价值
    return w.wss(security,"timevalue",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDBorrowIbSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取拆入资金_GSD时间序列
    return w.wsd(security,"wgsd_borrow_ib",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDBorrowIb(security:list,*args,**kwargs):
    # 获取拆入资金_GSD
    return w.wss(security,"wgsd_borrow_ib",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIntrInCtValueSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取内在价值时间序列
    return w.wsd(security,"intrinctvalue",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIntrInCtValue(security:list,*args,**kwargs):
    # 获取内在价值
    return w.wss(security,"intrinctvalue",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEstRpTTitleInStSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取报告标题时间序列
    return w.wsd(security,"est_rpttitle_inst",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEstRpTTitleInSt(security:list,*args,**kwargs):
    # 获取报告标题
    return w.wss(security,"est_rpttitle_inst",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoYOrSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业收入(同比增长率)时间序列
    return w.wsd(security,"yoy_or",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoYOr(security:list,*args,**kwargs):
    # 获取营业收入(同比增长率)
    return w.wss(security,"yoy_or",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCalcAccruedSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取应计利息(债券计算器)时间序列
    return w.wsd(security,"calc_accrued",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCalcAccrued(security:list,*args,**kwargs):
    # 获取应计利息(债券计算器)
    return w.wss(security,"calc_accrued",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTheoryValueSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取理论价格时间序列
    return w.wsd(security,"theoryvalue",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTheoryValue(security:list,*args,**kwargs):
    # 获取理论价格
    return w.wss(security,"theoryvalue",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNotesPayableSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取应付票据时间序列
    return w.wsd(security,"notes_payable",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNotesPayable(security:list,*args,**kwargs):
    # 获取应付票据
    return w.wss(security,"notes_payable",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCalcMDurationSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取修正久期时间序列
    return w.wsd(security,"calc_mduration",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCalcMDuration(security:list,*args,**kwargs):
    # 获取修正久期
    return w.wss(security,"calc_mduration",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration9YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取9年久期时间序列
    return w.wsd(security,"duration_9y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration9Y(security:list,*args,**kwargs):
    # 获取9年久期
    return w.wss(security,"duration_9y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAccTPayableSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取应付账款时间序列
    return w.wsd(security,"acct_payable",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAccTPayable(security:list,*args,**kwargs):
    # 获取应付账款
    return w.wss(security,"acct_payable",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoyoPSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业利润(同比增长率)时间序列
    return w.wsd(security,"yoyop",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoyoP(security:list,*args,**kwargs):
    # 获取营业利润(同比增长率)
    return w.wss(security,"yoyop",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAdvFromCuStSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取预收账款时间序列
    return w.wsd(security,"adv_from_cust",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAdvFromCuSt(security:list,*args,**kwargs):
    # 获取预收账款
    return w.wss(security,"adv_from_cust",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIntPayableSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取应付利息时间序列
    return w.wsd(security,"int_payable",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIntPayable(security:list,*args,**kwargs):
    # 获取应付利息
    return w.wss(security,"int_payable",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs29Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取应付利息_FUND时间序列
    return w.wsd(security,"stm_bs_29",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs29(security:list,*args,**kwargs):
    # 获取应付利息_FUND
    return w.wss(security,"stm_bs_29",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDvdPayableSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取应付股利时间序列
    return w.wsd(security,"dvd_payable",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDvdPayable(security:list,*args,**kwargs):
    # 获取应付股利
    return w.wss(security,"dvd_payable",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDurationShortSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取短边久期时间序列
    return w.wsd(security,"duration_short",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDurationShort(security:list,*args,**kwargs):
    # 获取短边久期
    return w.wss(security,"duration_short",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDurationLongSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取长边久期时间序列
    return w.wsd(security,"duration_long",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDurationLong(security:list,*args,**kwargs):
    # 获取长边久期
    return w.wss(security,"duration_long",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAccExpSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取预提费用时间序列
    return w.wsd(security,"acc_exp",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAccExp(security:list,*args,**kwargs):
    # 获取预提费用
    return w.wss(security,"acc_exp",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStrBPremiumSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取纯债溢价时间序列
    return w.wsd(security,"strbpremium",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStrBPremium(security:list,*args,**kwargs):
    # 获取纯债溢价
    return w.wss(security,"strbpremium",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getToTAccTPayableSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取应付款项时间序列
    return w.wsd(security,"tot_acct_payable",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getToTAccTPayable(security:list,*args,**kwargs):
    # 获取应付款项
    return w.wss(security,"tot_acct_payable",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStrBValueSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取纯债价值时间序列
    return w.wsd(security,"strbvalue",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStrBValue(security:list,*args,**kwargs):
    # 获取纯债价值
    return w.wss(security,"strbvalue",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechBullPowerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取多头力道_PIT时间序列
    return w.wsd(security,"tech_bullpower",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechBullPower(security:list,*args,**kwargs):
    # 获取多头力道_PIT
    return w.wss(security,"tech_bullpower",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskCorreCoefficientTrackIndexSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取相关系数(跟踪指数)时间序列
    return w.wsd(security,"risk_correcoefficient_trackindex",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskCorreCoefficientTrackIndex(security:list,*args,**kwargs):
    # 获取相关系数(跟踪指数)
    return w.wss(security,"risk_correcoefficient_trackindex",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsNameProSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取项目简称时间序列
    return w.wsd(security,"abs_namepro",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsNamePro(security:list,*args,**kwargs):
    # 获取项目简称
    return w.wss(security,"abs_namepro",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsProjectCodeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取项目代码时间序列
    return w.wsd(security,"abs_projectcode",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsProjectCode(security:list,*args,**kwargs):
    # 获取项目代码
    return w.wss(security,"abs_projectcode",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaPerExpenseTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取期间费用(TTM)_PIT时间序列
    return w.wsd(security,"fa_perexpense_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaPerExpenseTtM(security:list,*args,**kwargs):
    # 获取期间费用(TTM)_PIT
    return w.wss(security,"fa_perexpense_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaBerryRatioTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取贝里比率(TTM)_PIT时间序列
    return w.wsd(security,"fa_berryratio_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaBerryRatioTtM(security:list,*args,**kwargs):
    # 获取贝里比率(TTM)_PIT
    return w.wss(security,"fa_berryratio_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPeriodExpenseTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取期间费用(TTM)_GSD时间序列
    return w.wsd(security,"periodexpense_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPeriodExpenseTtM(security:list,*args,**kwargs):
    # 获取期间费用(TTM)_GSD
    return w.wss(security,"periodexpense_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaQuickSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取速动比率_PIT时间序列
    return w.wsd(security,"fa_quick",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaQuick(security:list,*args,**kwargs):
    # 获取速动比率_PIT
    return w.wss(security,"fa_quick",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDQuickSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取速动比率_GSD时间序列
    return w.wsd(security,"wgsd_quick",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDQuick(security:list,*args,**kwargs):
    # 获取速动比率_GSD
    return w.wss(security,"wgsd_quick",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getQuickSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取速动比率时间序列
    return w.wsd(security,"quick",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getQuick(security:list,*args,**kwargs):
    # 获取速动比率
    return w.wss(security,"quick",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaCurrentSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取流动比率_PIT时间序列
    return w.wsd(security,"fa_current",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaCurrent(security:list,*args,**kwargs):
    # 获取流动比率_PIT
    return w.wss(security,"fa_current",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaEbItTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取EBIT(TTM)_PIT时间序列
    return w.wsd(security,"fa_ebit_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaEbItTtM(security:list,*args,**kwargs):
    # 获取EBIT(TTM)_PIT
    return w.wss(security,"fa_ebit_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDCurrentSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取流动比率_GSD时间序列
    return w.wsd(security,"wgsd_current",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDCurrent(security:list,*args,**kwargs):
    # 获取流动比率_GSD
    return w.wss(security,"wgsd_current",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCurrentSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取流动比率时间序列
    return w.wsd(security,"current",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCurrent(security:list,*args,**kwargs):
    # 获取流动比率
    return w.wss(security,"current",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsPayBackSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取还本方式时间序列
    return w.wsd(security,"abs_payback",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsPayBack(security:list,*args,**kwargs):
    # 获取还本方式
    return w.wss(security,"abs_payback",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechAroOnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取阿隆指标_PIT时间序列
    return w.wsd(security,"tech_aroon",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechAroOn(security:list,*args,**kwargs):
    # 获取阿隆指标_PIT
    return w.wss(security,"tech_aroon",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoPrice2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取首发价格时间序列
    return w.wsd(security,"ipo_price2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoPrice2(security:list,*args,**kwargs):
    # 获取首发价格
    return w.wss(security,"ipo_price2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEbIt2TtM3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取EBIT(TTM)_GSD时间序列
    return w.wsd(security,"ebit2_ttm3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEbIt2TtM3(security:list,*args,**kwargs):
    # 获取EBIT(TTM)_GSD
    return w.wss(security,"ebit2_ttm3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEbIt2TtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取EBIT(TTM)时间序列
    return w.wsd(security,"ebit2_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEbIt2TtM(security:list,*args,**kwargs):
    # 获取EBIT(TTM)
    return w.wss(security,"ebit2_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsCreditSupportSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取信用支持时间序列
    return w.wsd(security,"abs_creditsupport",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsCreditSupport(security:list,*args,**kwargs):
    # 获取信用支持
    return w.wss(security,"abs_creditsupport",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechCoppockCurveSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取估波指标_PIT时间序列
    return w.wsd(security,"tech_coppockcurve",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechCoppockCurve(security:list,*args,**kwargs):
    # 获取估波指标_PIT
    return w.wss(security,"tech_coppockcurve",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDAssetsToEquitySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取权益乘数_GSD时间序列
    return w.wsd(security,"wgsd_assetstoequity",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDAssetsToEquity(security:list,*args,**kwargs):
    # 获取权益乘数_GSD
    return w.wss(security,"wgsd_assetstoequity",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAssetsToEquitySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取权益乘数时间序列
    return w.wsd(security,"assetstoequity",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAssetsToEquity(security:list,*args,**kwargs):
    # 获取权益乘数
    return w.wss(security,"assetstoequity",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsDealOutStStandingAmountSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取项目余额时间序列
    return w.wsd(security,"abs_dealoutststandingamount",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsDealOutStStandingAmount(security:list,*args,**kwargs):
    # 获取项目余额
    return w.wss(security,"abs_dealoutststandingamount",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechUOsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取终极指标_PIT时间序列
    return w.wsd(security,"tech_uos",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechUOs(security:list,*args,**kwargs):
    # 获取终极指标_PIT
    return w.wss(security,"tech_uos",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsSelfSustainingProportionSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取自持比例时间序列
    return w.wsd(security,"abs_selfsustainingproportion",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsSelfSustainingProportion(security:list,*args,**kwargs):
    # 获取自持比例
    return w.wss(security,"abs_selfsustainingproportion",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueAdditionalSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取是否增发时间序列
    return w.wsd(security,"issueadditional",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueAdditional(security:list,*args,**kwargs):
    # 获取是否增发
    return w.wss(security,"issueadditional",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoListDaysSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取上市天数时间序列
    return w.wsd(security,"ipo_listdays",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoListDays(security:list,*args,**kwargs):
    # 获取上市天数
    return w.wss(security,"ipo_listdays",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBaseRateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基准利率时间序列
    return w.wsd(security,"baserate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBaseRate(security:list,*args,**kwargs):
    # 获取基准利率
    return w.wss(security,"baserate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBaseRate2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取基准利率(发行时)时间序列
    return w.wsd(security,"baserate2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBaseRate2(security:list,*args,**kwargs):
    # 获取基准利率(发行时)
    return w.wss(security,"baserate2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWebsiteSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取公司网站时间序列
    return w.wsd(security,"website",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWebsite(security:list,*args,**kwargs):
    # 获取公司网站
    return w.wss(security,"website",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCashToCurrentDebtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取现金比率时间序列
    return w.wsd(security,"cashtocurrentdebt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCashToCurrentDebt(security:list,*args,**kwargs):
    # 获取现金比率
    return w.wss(security,"cashtocurrentdebt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDebtToEquitySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取产权比率时间序列
    return w.wsd(security,"debttoequity",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDebtToEquity(security:list,*args,**kwargs):
    # 获取产权比率
    return w.wss(security,"debttoequity",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDDebtToEquitySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取产权比率_GSD时间序列
    return w.wsd(security,"wgsd_debttoequity",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDDebtToEquity(security:list,*args,**kwargs):
    # 获取产权比率_GSD
    return w.wss(security,"wgsd_debttoequity",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaDebtToEquitySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取产权比率_PIT时间序列
    return w.wsd(security,"fa_debttoequity",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaDebtToEquity(security:list,*args,**kwargs):
    # 获取产权比率_PIT
    return w.wss(security,"fa_debttoequity",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechBbiSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取多空指数_PIT时间序列
    return w.wsd(security,"tech_bbi",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechBbi(security:list,*args,**kwargs):
    # 获取多空指数_PIT
    return w.wss(security,"tech_bbi",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechDDnsRSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取下跌波动_PIT时间序列
    return w.wsd(security,"tech_ddnsr",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechDDnsR(security:list,*args,**kwargs):
    # 获取下跌波动_PIT
    return w.wss(security,"tech_ddnsr",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechBearPowerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取空头力道_PIT时间序列
    return w.wsd(security,"tech_bearpower",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechBearPower(security:list,*args,**kwargs):
    # 获取空头力道_PIT
    return w.wss(security,"tech_bearpower",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechSkewNessSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取股价偏度_PIT时间序列
    return w.wsd(security,"tech_skewness",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechSkewNess(security:list,*args,**kwargs):
    # 获取股价偏度_PIT
    return w.wss(security,"tech_skewness",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechCHaikInSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取佳庆指标_PIT时间序列
    return w.wsd(security,"tech_chaikin",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechCHaikIn(security:list,*args,**kwargs):
    # 获取佳庆指标_PIT
    return w.wss(security,"tech_chaikin",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaToTEquitySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取股东权益_PIT时间序列
    return w.wsd(security,"fa_totequity",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaToTEquity(security:list,*args,**kwargs):
    # 获取股东权益_PIT
    return w.wss(security,"fa_totequity",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaMLevSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取市场杠杆_PIT时间序列
    return w.wsd(security,"fa_mlev",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaMLev(security:list,*args,**kwargs):
    # 获取市场杠杆_PIT
    return w.wss(security,"fa_mlev",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaBLevSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取账面杠杆_PIT时间序列
    return w.wsd(security,"fa_blev",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaBLev(security:list,*args,**kwargs):
    # 获取账面杠杆_PIT
    return w.wss(security,"fa_blev",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaDpsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股股利_PIT时间序列
    return w.wsd(security,"fa_dps",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaDps(security:list,*args,**kwargs):
    # 获取每股股利_PIT
    return w.wss(security,"fa_dps",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValLnMvSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取对数市值_PIT时间序列
    return w.wsd(security,"val_lnmv",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValLnMv(security:list,*args,**kwargs):
    # 获取对数市值_PIT
    return w.wss(security,"val_lnmv",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsIndustrySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取主体行业时间序列
    return w.wsd(security,"abs_industry",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsIndustry(security:list,*args,**kwargs):
    # 获取主体行业
    return w.wss(security,"abs_industry",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEv2ToEbItDaSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取企业倍数(EV2/EBITDA)时间序列
    return w.wsd(security,"ev2_to_ebitda",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEv2ToEbItDa(security:list,*args,**kwargs):
    # 获取企业倍数(EV2/EBITDA)
    return w.wss(security,"ev2_to_ebitda",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsIndustry1Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取主体性质时间序列
    return w.wsd(security,"abs_industry1",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsIndustry1(security:list,*args,**kwargs):
    # 获取主体性质
    return w.wss(security,"abs_industry1",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDEbItSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取EBIT(反推法)_GSD时间序列
    return w.wsd(security,"wgsd_ebit",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDEbIt(security:list,*args,**kwargs):
    # 获取EBIT(反推法)_GSD
    return w.wss(security,"wgsd_ebit",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBaseRate3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取基准利率(指定日期)时间序列
    return w.wsd(security,"baserate3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBaseRate3(security:list,*args,**kwargs):
    # 获取基准利率(指定日期)
    return w.wss(security,"baserate3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaTurnDaysTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业周期(TTM)_PIT时间序列
    return w.wsd(security,"fa_turndays_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaTurnDaysTtM(security:list,*args,**kwargs):
    # 获取营业周期(TTM)_PIT
    return w.wss(security,"fa_turndays_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTurnDaysSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业周期时间序列
    return w.wsd(security,"turndays",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTurnDays(security:list,*args,**kwargs):
    # 获取营业周期
    return w.wss(security,"turndays",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivObjectSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取分红对象时间序列
    return w.wsd(security,"div_object",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivObject(security:list,*args,**kwargs):
    # 获取分红对象
    return w.wss(security,"div_object",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEbIt2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取EBIT时间序列
    return w.wsd(security,"ebit2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEbIt2(security:list,*args,**kwargs):
    # 获取EBIT
    return w.wss(security,"ebit2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsProvinceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取主体地区时间序列
    return w.wsd(security,"abs_province",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsProvince(security:list,*args,**kwargs):
    # 获取主体地区
    return w.wss(security,"abs_province",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEbItSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取EBIT(反推法)时间序列
    return w.wsd(security,"ebit",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEbIt(security:list,*args,**kwargs):
    # 获取EBIT(反推法)
    return w.wss(security,"ebit",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivIfDivSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取是否分红时间序列
    return w.wsd(security,"div_ifdiv",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivIfDiv(security:list,*args,**kwargs):
    # 获取是否分红
    return w.wss(security,"div_ifdiv",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsAgencyTrustee1Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取受托机构时间序列
    return w.wsd(security,"abs_agency_trustee1",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsAgencyTrustee1(security:list,*args,**kwargs):
    # 获取受托机构
    return w.wss(security,"abs_agency_trustee1",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIndustryGicS2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取废弃行业时间序列
    return w.wsd(security,"industry_gics2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIndustryGicS2(security:list,*args,**kwargs):
    # 获取废弃行业
    return w.wss(security,"industry_gics2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsFullNameProSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取项目名称时间序列
    return w.wsd(security,"abs_fullnamepro",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsFullNamePro(security:list,*args,**kwargs):
    # 获取项目名称
    return w.wss(security,"abs_fullnamepro",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDNetDebtRatioArdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净负债率(公告值)_GSD时间序列
    return w.wsd(security,"wgsd_netdebtratio_ard",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDNetDebtRatioArd(security:list,*args,**kwargs):
    # 获取净负债率(公告值)_GSD
    return w.wss(security,"wgsd_netdebtratio_ard",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDNetDebtRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净负债率_GSD时间序列
    return w.wsd(security,"wgsd_netdebtratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDNetDebtRatio(security:list,*args,**kwargs):
    # 获取净负债率_GSD
    return w.wss(security,"wgsd_netdebtratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaNetDebtRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净负债率时间序列
    return w.wsd(security,"fa_netdebtratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaNetDebtRatio(security:list,*args,**kwargs):
    # 获取净负债率
    return w.wss(security,"fa_netdebtratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInterestExpenseTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取利息费用(TTM)时间序列
    return w.wsd(security,"interestexpense_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInterestExpenseTtM(security:list,*args,**kwargs):
    # 获取利息费用(TTM)
    return w.wss(security,"interestexpense_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPeriodExpenseTTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取期间费用(TTM)时间序列
    return w.wsd(security,"periodexpense_t_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPeriodExpenseTTtM(security:list,*args,**kwargs):
    # 获取期间费用(TTM)
    return w.wss(security,"periodexpense_t_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDTurnDaysSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业周期_GSD时间序列
    return w.wsd(security,"wgsd_turndays",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDTurnDays(security:list,*args,**kwargs):
    # 获取营业周期_GSD
    return w.wss(security,"wgsd_turndays",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskCorreCoefficientSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取相关系数时间序列
    return w.wsd(security,"risk_correcoefficient",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskCorreCoefficient(security:list,*args,**kwargs):
    # 获取相关系数
    return w.wss(security,"risk_correcoefficient",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaWorkCapitalSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取运营资本_PIT时间序列
    return w.wsd(security,"fa_workcapital",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaWorkCapital(security:list,*args,**kwargs):
    # 获取运营资本_PIT
    return w.wss(security,"fa_workcapital",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaxSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取公司传真时间序列
    return w.wsd(security,"fax",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFax(security:list,*args,**kwargs):
    # 获取公司传真
    return w.wss(security,"fax",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWRatingAvgCnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取综合评级(中文)(可选类型)时间序列
    return w.wsd(security,"wrating_avg_cn",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWRatingAvgCn(security:list,*args,**kwargs):
    # 获取综合评级(中文)(可选类型)
    return w.wss(security,"wrating_avg_cn",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRatingAvGengSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取综合评级(英文)时间序列
    return w.wsd(security,"rating_avgeng",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRatingAvGeng(security:list,*args,**kwargs):
    # 获取综合评级(英文)
    return w.wss(security,"rating_avgeng",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWRatingAvgEnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取综合评级(英文)(可选类型)时间序列
    return w.wsd(security,"wrating_avg_en",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWRatingAvgEn(security:list,*args,**kwargs):
    # 获取综合评级(英文)(可选类型)
    return w.wss(security,"wrating_avg_en",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsoluteAvgIncomeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取平均收益时间序列
    return w.wsd(security,"absolute_avgincome",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsoluteAvgIncome(security:list,*args,**kwargs):
    # 获取平均收益
    return w.wss(security,"absolute_avgincome",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoReallocationPctSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取回拨比例时间序列
    return w.wsd(security,"ipo_ReallocationPct",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoReallocationPct(security:list,*args,**kwargs):
    # 获取回拨比例
    return w.wss(security,"ipo_ReallocationPct",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsoluteCondOwnsMonthSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取连跌月数时间序列
    return w.wsd(security,"absolute_condownsmonth",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsoluteCondOwnsMonth(security:list,*args,**kwargs):
    # 获取连跌月数
    return w.wss(security,"absolute_condownsmonth",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsoluteConUpsMonthSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取连涨月数时间序列
    return w.wsd(security,"absolute_conupsmonth",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsoluteConUpsMonth(security:list,*args,**kwargs):
    # 获取连涨月数
    return w.wss(security,"absolute_conupsmonth",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRegCapitalSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取注册资本时间序列
    return w.wsd(security,"regcapital",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRegCapital(security:list,*args,**kwargs):
    # 获取注册资本
    return w.wss(security,"regcapital",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFoundDate1Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取成立日期时间序列
    return w.wsd(security,"founddate1",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFoundDate1(security:list,*args,**kwargs):
    # 获取成立日期
    return w.wss(security,"founddate1",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseCallOptionRedemptionPriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取赎回价格时间序列
    return w.wsd(security,"clause_calloption_redemptionprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseCallOptionRedemptionPrice(security:list,*args,**kwargs):
    # 获取赎回价格
    return w.wss(security,"clause_calloption_redemptionprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStyleMarketValueAttributeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取市值属性时间序列
    return w.wsd(security,"style_marketvalueattribute",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStyleMarketValueAttribute(security:list,*args,**kwargs):
    # 获取市值属性
    return w.wss(security,"style_marketvalueattribute",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStyleStyleAttributeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取风格属性时间序列
    return w.wsd(security,"style_styleattribute",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStyleStyleAttribute(security:list,*args,**kwargs):
    # 获取风格属性
    return w.wss(security,"style_styleattribute",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStyleStyleCoefficientSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取风格系数时间序列
    return w.wsd(security,"style_stylecoefficient",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStyleStyleCoefficient(security:list,*args,**kwargs):
    # 获取风格系数
    return w.wss(security,"style_stylecoefficient",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskAnNuInfoRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取信息比率(年化)时间序列
    return w.wsd(security,"risk_annuinforatio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskAnNuInfoRatio(security:list,*args,**kwargs):
    # 获取信息比率(年化)
    return w.wss(security,"risk_annuinforatio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskInfoRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取信息比率时间序列
    return w.wsd(security,"risk_inforatio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskInfoRatio(security:list,*args,**kwargs):
    # 获取信息比率
    return w.wss(security,"risk_inforatio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskAnNuTrackErrorSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取跟踪误差(年化)时间序列
    return w.wsd(security,"risk_annutrackerror",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskAnNuTrackError(security:list,*args,**kwargs):
    # 获取跟踪误差(年化)
    return w.wss(security,"risk_annutrackerror",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskTrackErrorTrackIndexSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取跟踪误差(跟踪指数)时间序列
    return w.wsd(security,"risk_trackerror_trackindex",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskTrackErrorTrackIndex(security:list,*args,**kwargs):
    # 获取跟踪误差(跟踪指数)
    return w.wss(security,"risk_trackerror_trackindex",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEstEventDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取大事日期(大事后预测)时间序列
    return w.wsd(security,"est_event_date",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEstEventDate(security:list,*args,**kwargs):
    # 获取大事日期(大事后预测)
    return w.wss(security,"est_event_date",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskTrackErrorSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取跟踪误差时间序列
    return w.wsd(security,"risk_trackerror",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskTrackError(security:list,*args,**kwargs):
    # 获取跟踪误差
    return w.wss(security,"risk_trackerror",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskStockSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取选股能力时间序列
    return w.wsd(security,"risk_stock",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskStock(security:list,*args,**kwargs):
    # 获取选股能力
    return w.wss(security,"risk_stock",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRsvOtherSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他储备_GSD时间序列
    return w.wsd(security,"wgsd_rsv_other",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRsvOther(security:list,*args,**kwargs):
    # 获取其他储备_GSD
    return w.wss(security,"wgsd_rsv_other",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDInvestOThSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他投资_GSD时间序列
    return w.wsd(security,"wgsd_invest_oth",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDInvestOTh(security:list,*args,**kwargs):
    # 获取其他投资_GSD
    return w.wss(security,"wgsd_invest_oth",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskTimeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取选时能力时间序列
    return w.wsd(security,"risk_time",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskTime(security:list,*args,**kwargs):
    # 获取选时能力
    return w.wss(security,"risk_time",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCorpScaleSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取企业规模时间序列
    return w.wsd(security,"corpscale",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCorpScale(security:list,*args,**kwargs):
    # 获取企业规模
    return w.wss(security,"corpscale",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWinRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间胜率时间序列
    return w.wsd(security,"win_ratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWinRatio(security:list,*args,**kwargs):
    # 获取区间胜率
    return w.wss(security,"win_ratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInvestLossSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取投资损失时间序列
    return w.wsd(security,"invest_loss",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInvestLoss(security:list,*args,**kwargs):
    # 获取投资损失
    return w.wss(security,"invest_loss",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskDownsideRiskSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取下行风险时间序列
    return w.wsd(security,"risk_downsiderisk",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskDownsideRisk(security:list,*args,**kwargs):
    # 获取下行风险
    return w.wss(security,"risk_downsiderisk",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskR2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取可决系数时间序列
    return w.wsd(security,"risk_r2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskR2(security:list,*args,**kwargs):
    # 获取可决系数
    return w.wss(security,"risk_r2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClausePutOptionResellingPriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取回售价格时间序列
    return w.wsd(security,"clause_putoption_resellingprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClausePutOptionResellingPrice(security:list,*args,**kwargs):
    # 获取回售价格
    return w.wss(security,"clause_putoption_resellingprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRatingAvgChNSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取综合评级(中文)时间序列
    return w.wsd(security,"rating_avgchn",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRatingAvgChN(security:list,*args,**kwargs):
    # 获取综合评级(中文)
    return w.wss(security,"rating_avgchn",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWRatingAvgDataSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取综合评级(数值)(可选类型)时间序列
    return w.wsd(security,"wrating_avg_data",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWRatingAvgData(security:list,*args,**kwargs):
    # 获取综合评级(数值)(可选类型)
    return w.wss(security,"wrating_avg_data",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRatingAvgSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取综合评级(数值)时间序列
    return w.wsd(security,"rating_avg",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRatingAvg(security:list,*args,**kwargs):
    # 获取综合评级(数值)
    return w.wss(security,"rating_avg",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsoluteAvgLossSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取平均损失时间序列
    return w.wsd(security,"absolute_avgloss",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsoluteAvgLoss(security:list,*args,**kwargs):
    # 获取平均损失
    return w.wss(security,"absolute_avgloss",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPhoneSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取公司电话时间序列
    return w.wsd(security,"phone",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPhone(security:list,*args,**kwargs):
    # 获取公司电话
    return w.wss(security,"phone",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueFeeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行费率时间序列
    return w.wsd(security,"issue_fee",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueFee(security:list,*args,**kwargs):
    # 获取发行费率
    return w.wss(security,"issue_fee",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSpreadSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取固定利差时间序列
    return w.wsd(security,"spread",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSpread(security:list,*args,**kwargs):
    # 获取固定利差
    return w.wss(security,"spread",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOfficeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取办公地址时间序列
    return w.wsd(security,"office",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOffice(security:list,*args,**kwargs):
    # 获取办公地址
    return w.wss(security,"office",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAddressSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取注册地址时间序列
    return w.wsd(security,"address",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAddress(security:list,*args,**kwargs):
    # 获取注册地址
    return w.wss(security,"address",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCouponRate2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取票面利率(当期)时间序列
    return w.wsd(security,"couponrate2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCouponRate2(security:list,*args,**kwargs):
    # 获取票面利率(当期)
    return w.wss(security,"couponrate2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskBetaSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取Beta_FUND时间序列
    return w.wsd(security,"risk_beta",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskBeta(security:list,*args,**kwargs):
    # 获取Beta_FUND
    return w.wss(security,"risk_beta",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBetaDfSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取Beta(剔除财务杠杆)时间序列
    return w.wsd(security,"betadf",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBetaDf(security:list,*args,**kwargs):
    # 获取Beta(剔除财务杠杆)
    return w.wss(security,"betadf",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBetaSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取Beta时间序列
    return w.wsd(security,"beta",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBeta(security:list,*args,**kwargs):
    # 获取Beta
    return w.wss(security,"beta",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCouponRate3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取票面利率(指定日期)时间序列
    return w.wsd(security,"couponrate3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCouponRate3(security:list,*args,**kwargs):
    # 获取票面利率(指定日期)
    return w.wss(security,"couponrate3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInterestFloorSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取保底利率时间序列
    return w.wsd(security,"interestfloor",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInterestFloor(security:list,*args,**kwargs):
    # 获取保底利率
    return w.wss(security,"interestfloor",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEmployeeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取员工总数时间序列
    return w.wsd(security,"employee",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEmployee(security:list,*args,**kwargs):
    # 获取员工总数
    return w.wss(security,"employee",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取特殊条款时间序列
    return w.wsd(security,"clause",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClause(security:list,*args,**kwargs):
    # 获取特殊条款
    return w.wss(security,"clause",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIoPvSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取IOPV时间序列
    return w.wsd(security,"iopv",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIoPv(security:list,*args,**kwargs):
    # 获取IOPV
    return w.wss(security,"iopv",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDOperExpSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业开支_GSD时间序列
    return w.wsd(security,"wgsd_oper_exp",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDOperExp(security:list,*args,**kwargs):
    # 获取营业开支_GSD
    return w.wss(security,"wgsd_oper_exp",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getVegaExChSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取Vega(交易所)时间序列
    return w.wsd(security,"vega_exch",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getVegaExCh(security:list,*args,**kwargs):
    # 获取Vega(交易所)
    return w.wss(security,"vega_exch",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOiSvOiSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取持卖单量(品种)时间序列
    return w.wsd(security,"oi_svoi",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOiSvOi(security:list,*args,**kwargs):
    # 获取持卖单量(品种)
    return w.wss(security,"oi_svoi",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOiSoISeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取持卖单量时间序列
    return w.wsd(security,"oi_soi",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOiSoI(security:list,*args,**kwargs):
    # 获取持卖单量
    return w.wss(security,"oi_soi",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOiLvOiSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取持买单量(品种)时间序列
    return w.wsd(security,"oi_lvoi",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOiLvOi(security:list,*args,**kwargs):
    # 获取持买单量(品种)
    return w.wss(security,"oi_lvoi",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOiLoiSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取持买单量时间序列
    return w.wsd(security,"oi_loi",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOiLoi(security:list,*args,**kwargs):
    # 获取持买单量
    return w.wss(security,"oi_loi",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalDownDiscountThresholdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取下折阈值时间序列
    return w.wsd(security,"anal_downdiscount_threshold",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalDownDiscountThreshold(security:list,*args,**kwargs):
    # 获取下折阈值
    return w.wss(security,"anal_downdiscount_threshold",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalUpDiscountThresholdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取上折阈值时间序列
    return w.wsd(security,"anal_updiscount_threshold",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalUpDiscountThreshold(security:list,*args,**kwargs):
    # 获取上折阈值
    return w.wss(security,"anal_updiscount_threshold",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getConstInProgToTSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取在建工程(合计)时间序列
    return w.wsd(security,"const_in_prog_tot",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getConstInProgToT(security:list,*args,**kwargs):
    # 获取在建工程(合计)
    return w.wss(security,"const_in_prog_tot",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs37Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他费用_FUND时间序列
    return w.wsd(security,"stm_is_37",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs37(security:list,*args,**kwargs):
    # 获取其他费用_FUND
    return w.wss(security,"stm_is_37",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs9Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他收入_FUND时间序列
    return w.wsd(security,"stm_is_9",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs9(security:list,*args,**kwargs):
    # 获取其他收入_FUND
    return w.wss(security,"stm_is_9",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseAbbrSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取特殊条款(缩写)时间序列
    return w.wsd(security,"clauseabbr",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseAbbr(security:list,*args,**kwargs):
    # 获取特殊条款(缩写)
    return w.wss(security,"clauseabbr",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalPriceLeverSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取价格杠杆时间序列
    return w.wsd(security,"anal_pricelever",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalPriceLever(security:list,*args,**kwargs):
    # 获取价格杠杆
    return w.wss(security,"anal_pricelever",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalNavLeverSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净值杠杆时间序列
    return w.wsd(security,"anal_navlever",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalNavLever(security:list,*args,**kwargs):
    # 获取净值杠杆
    return w.wss(security,"anal_navlever",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBriefingSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取公司简介时间序列
    return w.wsd(security,"briefing",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBriefing(security:list,*args,**kwargs):
    # 获取公司简介
    return w.wss(security,"briefing",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBusinessSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取经营范围时间序列
    return w.wsd(security,"business",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBusiness(security:list,*args,**kwargs):
    # 获取经营范围
    return w.wss(security,"business",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getVegaSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取Vega时间序列
    return w.wsd(security,"vega",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getVega(security:list,*args,**kwargs):
    # 获取Vega
    return w.wss(security,"vega",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration2YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取2年久期时间序列
    return w.wsd(security,"duration_2y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration2Y(security:list,*args,**kwargs):
    # 获取2年久期
    return w.wss(security,"duration_2y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs4Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取股票投资_FUND时间序列
    return w.wsd(security,"stm_bs_4",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs4(security:list,*args,**kwargs):
    # 获取股票投资_FUND
    return w.wss(security,"stm_bs_4",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration6MSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取6月久期时间序列
    return w.wsd(security,"duration_6m",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration6M(security:list,*args,**kwargs):
    # 获取6月久期
    return w.wss(security,"duration_6m",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSecNameSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取证券简称时间序列
    return w.wsd(security,"sec_name",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSecName(security:list,*args,**kwargs):
    # 获取证券简称
    return w.wss(security,"sec_name",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank615Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取存款余额_其它存款时间序列
    return w.wsd(security,"stmnote_bank_615",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank615(security:list,*args,**kwargs):
    # 获取存款余额_其它存款
    return w.wss(security,"stmnote_bank_615",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank614Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取存款余额_公司活期存款时间序列
    return w.wsd(security,"stmnote_bank_614",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank614(security:list,*args,**kwargs):
    # 获取存款余额_公司活期存款
    return w.wss(security,"stmnote_bank_614",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank613Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取存款余额_公司定期存款时间序列
    return w.wsd(security,"stmnote_bank_613",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank613(security:list,*args,**kwargs):
    # 获取存款余额_公司定期存款
    return w.wss(security,"stmnote_bank_613",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank617Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取存款余额_公司存款时间序列
    return w.wsd(security,"stmnote_bank_617",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank617(security:list,*args,**kwargs):
    # 获取存款余额_公司存款
    return w.wss(security,"stmnote_bank_617",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank612Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取存款余额_个人活期存款时间序列
    return w.wsd(security,"stmnote_bank_612",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank612(security:list,*args,**kwargs):
    # 获取存款余额_个人活期存款
    return w.wss(security,"stmnote_bank_612",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank611Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取存款余额_个人定期存款时间序列
    return w.wsd(security,"stmnote_bank_611",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank611(security:list,*args,**kwargs):
    # 获取存款余额_个人定期存款
    return w.wss(security,"stmnote_bank_611",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank616Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取存款余额_个人存款时间序列
    return w.wsd(security,"stmnote_bank_616",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank616(security:list,*args,**kwargs):
    # 获取存款余额_个人存款
    return w.wss(security,"stmnote_bank_616",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClausePutOptionInterestDisposingSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取利息处理时间序列
    return w.wsd(security,"clause_putoption_interestdisposing",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClausePutOptionInterestDisposing(security:list,*args,**kwargs):
    # 获取利息处理
    return w.wss(security,"clause_putoption_interestdisposing",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoLeadUndRNSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取(废弃)主办券商(持续督导)时间序列
    return w.wsd(security,"ipo_leadundr_n",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoLeadUndRN(security:list,*args,**kwargs):
    # 获取(废弃)主办券商(持续督导)
    return w.wss(security,"ipo_leadundr_n",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundTargetScaleSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取目标规模时间序列
    return w.wsd(security,"fund_targetscale",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundTargetScale(security:list,*args,**kwargs):
    # 获取目标规模
    return w.wss(security,"fund_targetscale",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFoundDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取(废弃)成立日期时间序列
    return w.wsd(security,"founddate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFoundDate(security:list,*args,**kwargs):
    # 获取(废弃)成立日期
    return w.wss(security,"founddate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank131Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取资本净额(旧)时间序列
    return w.wsd(security,"stmnote_bank_131",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank131(security:list,*args,**kwargs):
    # 获取资本净额(旧)
    return w.wss(security,"stmnote_bank_131",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBankNetEquityCapSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资本净额(2013)时间序列
    return w.wsd(security,"stmnote_bank_NetEquityCap",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBankNetEquityCap(security:list,*args,**kwargs):
    # 获取资本净额(2013)
    return w.wss(security,"stmnote_bank_NetEquityCap",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank131NSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资本净额时间序列
    return w.wsd(security,"stmnote_bank_131_n",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank131N(security:list,*args,**kwargs):
    # 获取资本净额
    return w.wss(security,"stmnote_bank_131_n",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTrustTypeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取信托类别(信托)时间序列
    return w.wsd(security,"trust_type",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTrustType(security:list,*args,**kwargs):
    # 获取信托类别(信托)
    return w.wss(security,"trust_type",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPlanTypeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取计划类型(券商集合理财)时间序列
    return w.wsd(security,"fund_plantype",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPlanType(security:list,*args,**kwargs):
    # 获取计划类型(券商集合理财)
    return w.wss(security,"fund_plantype",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDirtyCsiSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取估价全价(中证指数)(旧)时间序列
    return w.wsd(security,"dirty_csi",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDirtyCsi(security:list,*args,**kwargs):
    # 获取估价全价(中证指数)(旧)
    return w.wss(security,"dirty_csi",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderTimeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取招标时间时间序列
    return w.wsd(security,"tender_time",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderTime(security:list,*args,**kwargs):
    # 获取招标时间
    return w.wss(security,"tender_time",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCNvXTyCsiSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取估价凸性(中证指数)(旧)时间序列
    return w.wsd(security,"cnvxty_csi",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCNvXTyCsi(security:list,*args,**kwargs):
    # 获取估价凸性(中证指数)(旧)
    return w.wss(security,"cnvxty_csi",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderAimInvStSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取招标对象时间序列
    return w.wsd(security,"tender_aiminvst",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderAimInvSt(security:list,*args,**kwargs):
    # 获取招标对象
    return w.wss(security,"tender_aiminvst",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderObjectSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取招标标的时间序列
    return w.wsd(security,"tender_object",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderObject(security:list,*args,**kwargs):
    # 获取招标标的
    return w.wss(security,"tender_object",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderMethodSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取招标方式时间序列
    return w.wsd(security,"tender_method",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderMethod(security:list,*args,**kwargs):
    # 获取招标方式
    return w.wss(security,"tender_method",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSecName1Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取证券简称(支持历史)时间序列
    return w.wsd(security,"sec_name1",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSecName1(security:list,*args,**kwargs):
    # 获取证券简称(支持历史)
    return w.wss(security,"sec_name1",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSplitRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取拆分比率时间序列
    return w.wsd(security,"fund_splitratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSplitRatio(security:list,*args,**kwargs):
    # 获取拆分比率
    return w.wss(security,"fund_splitratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoPriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取首发价格(旧)时间序列
    return w.wsd(security,"ipo_price",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoPrice(security:list,*args,**kwargs):
    # 获取首发价格(旧)
    return w.wss(security,"ipo_price",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyLeadUnderwriterSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取主承销商时间序列
    return w.wsd(security,"agency_leadunderwriter",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyLeadUnderwriter(security:list,*args,**kwargs):
    # 获取主承销商
    return w.wss(security,"agency_leadunderwriter",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyLeadUnderwritersNSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取主承销商(简称)时间序列
    return w.wsd(security,"agency_leadunderwriterSN",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyLeadUnderwritersN(security:list,*args,**kwargs):
    # 获取主承销商(简称)
    return w.wss(security,"agency_leadunderwriterSN",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundGuaranteedCycleSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取保本周期时间序列
    return w.wsd(security,"fund_guaranteedcycle",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundGuaranteedCycle(security:list,*args,**kwargs):
    # 获取保本周期
    return w.wss(security,"fund_guaranteedcycle",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundGuaranteedFeeRateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取保本费率时间序列
    return w.wsd(security,"fund_guaranteedfeerate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundGuaranteedFeeRate(security:list,*args,**kwargs):
    # 获取保本费率
    return w.wss(security,"fund_guaranteedfeerate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank5453Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取库存现金时间序列
    return w.wsd(security,"stmnote_bank_5453",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank5453(security:list,*args,**kwargs):
    # 获取库存现金
    return w.wss(security,"stmnote_bank_5453",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInitialLeverSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取初始杠杆时间序列
    return w.wsd(security,"fund_initiallever",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInitialLever(security:list,*args,**kwargs):
    # 获取初始杠杆
    return w.wss(security,"fund_initiallever",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetCsiSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取估价净价(中证指数)(旧)时间序列
    return w.wsd(security,"net_csi",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetCsi(security:list,*args,**kwargs):
    # 获取估价净价(中证指数)(旧)
    return w.wss(security,"net_csi",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInvestmentAdvisorSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取投资顾问时间序列
    return w.wsd(security,"fund_investmentadvisor",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInvestmentAdvisor(security:list,*args,**kwargs):
    # 获取投资顾问
    return w.wss(security,"fund_investmentadvisor",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundGuaranteedOrNotSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取是否保本时间序列
    return w.wsd(security,"fund_guaranteedornot",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundGuaranteedOrNot(security:list,*args,**kwargs):
    # 获取是否保本
    return w.wss(security,"fund_guaranteedornot",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueUnitSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行份额时间序列
    return w.wsd(security,"issue_unit",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueUnit(security:list,*args,**kwargs):
    # 获取发行份额
    return w.wss(security,"issue_unit",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsIssueSizeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行规模时间序列
    return w.wsd(security,"fund_reitsissuesize",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsIssueSize(security:list,*args,**kwargs):
    # 获取发行规模
    return w.wss(security,"fund_reitsissuesize",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerResignationReasonSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取离任原因时间序列
    return w.wsd(security,"fund_manager_resignationreason",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerResignationReason(security:list,*args,**kwargs):
    # 获取离任原因
    return w.wss(security,"fund_manager_resignationreason",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTunItSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取交易单位时间序列
    return w.wsd(security,"tunit",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTunIt(security:list,*args,**kwargs):
    # 获取交易单位
    return w.wss(security,"tunit",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLotSizeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每手股数时间序列
    return w.wsd(security,"lotsize",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLotSize(security:list,*args,**kwargs):
    # 获取每手股数
    return w.wss(security,"lotsize",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank687Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款余额_经营性贷款时间序列
    return w.wsd(security,"stmnote_bank_687",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank687(security:list,*args,**kwargs):
    # 获取贷款余额_经营性贷款
    return w.wss(security,"stmnote_bank_687",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank686Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款余额_信用卡应收账款时间序列
    return w.wsd(security,"stmnote_bank_686",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank686(security:list,*args,**kwargs):
    # 获取贷款余额_信用卡应收账款
    return w.wss(security,"stmnote_bank_686",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank685Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款余额_个人消费贷款时间序列
    return w.wsd(security,"stmnote_bank_685",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank685(security:list,*args,**kwargs):
    # 获取贷款余额_个人消费贷款
    return w.wss(security,"stmnote_bank_685",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getParValueSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股面值时间序列
    return w.wsd(security,"parvalue",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getParValue(security:list,*args,**kwargs):
    # 获取每股面值
    return w.wss(security,"parvalue",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValBsHrMarketValue2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取B股市值(不含限售股,交易币种)时间序列
    return w.wsd(security,"val_bshrmarketvalue2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValBsHrMarketValue2(security:list,*args,**kwargs):
    # 获取B股市值(不含限售股,交易币种)
    return w.wss(security,"val_bshrmarketvalue2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank684Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款余额_个人住房贷款时间序列
    return w.wsd(security,"stmnote_bank_684",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank684(security:list,*args,**kwargs):
    # 获取贷款余额_个人住房贷款
    return w.wss(security,"stmnote_bank_684",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank683Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款余额_票据贴现时间序列
    return w.wsd(security,"stmnote_bank_683",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank683(security:list,*args,**kwargs):
    # 获取贷款余额_票据贴现
    return w.wss(security,"stmnote_bank_683",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank682Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款余额_个人贷款及垫款时间序列
    return w.wsd(security,"stmnote_bank_682",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank682(security:list,*args,**kwargs):
    # 获取贷款余额_个人贷款及垫款
    return w.wss(security,"stmnote_bank_682",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank681Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款余额_企业贷款及垫款时间序列
    return w.wsd(security,"stmnote_bank_681",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank681(security:list,*args,**kwargs):
    # 获取贷款余额_企业贷款及垫款
    return w.wss(security,"stmnote_bank_681",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank680Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款余额_总计时间序列
    return w.wsd(security,"stmnote_bank_680",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank680(security:list,*args,**kwargs):
    # 获取贷款余额_总计
    return w.wss(security,"stmnote_bank_680",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsAsNameSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资产名称时间序列
    return w.wsd(security,"fund__reitsasname",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsAsName(security:list,*args,**kwargs):
    # 获取资产名称
    return w.wss(security,"fund__reitsasname",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValBsHrMarketValue4Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取B股市值(含限售股,交易币种)时间序列
    return w.wsd(security,"val_bshrmarketvalue4",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValBsHrMarketValue4(security:list,*args,**kwargs):
    # 获取B股市值(含限售股,交易币种)
    return w.wss(security,"val_bshrmarketvalue4",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取上市日期时间序列
    return w.wsd(security,"ipo_date",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoDate(security:list,*args,**kwargs):
    # 获取上市日期
    return w.wss(security,"ipo_date",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundBusinessModeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取业务模式时间序列
    return w.wsd(security,"fund_businessmode",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundBusinessMode(security:list,*args,**kwargs):
    # 获取业务模式
    return w.wss(security,"fund_businessmode",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivClauseSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取分红条款时间序列
    return w.wsd(security,"div_clause",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivClause(security:list,*args,**kwargs):
    # 获取分红条款
    return w.wss(security,"div_clause",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseResetResetTriggerRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取触发比例时间序列
    return w.wsd(security,"clause_reset_resettriggerratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseResetResetTriggerRatio(security:list,*args,**kwargs):
    # 获取触发比例
    return w.wss(security,"clause_reset_resettriggerratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsTypeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资产类型时间序列
    return w.wsd(security,"fund__reitstype",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsType(security:list,*args,**kwargs):
    # 获取资产类型
    return w.wss(security,"fund__reitstype",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsInfoSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取项目介绍时间序列
    return w.wsd(security,"fund__reitsinfo",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsInfo(security:list,*args,**kwargs):
    # 获取项目介绍
    return w.wss(security,"fund__reitsinfo",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueIssuePriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行价格时间序列
    return w.wsd(security,"issue_issueprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueIssuePrice(security:list,*args,**kwargs):
    # 获取发行价格
    return w.wss(security,"issue_issueprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueOEfDaysSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取认购天数时间序列
    return w.wsd(security,"issue_oef_days",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueOEfDays(security:list,*args,**kwargs):
    # 获取认购天数
    return w.wss(security,"issue_oef_days",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderExchangeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取招标场所时间序列
    return w.wsd(security,"tender_exchange",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderExchange(security:list,*args,**kwargs):
    # 获取招标场所
    return w.wss(security,"tender_exchange",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDeListDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取摘牌日期时间序列
    return w.wsd(security,"delist_date",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDeListDate(security:list,*args,**kwargs):
    # 获取摘牌日期
    return w.wss(security,"delist_date",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueIssueNumberSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行期号时间序列
    return w.wsd(security,"issue_issuenumber",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueIssueNumber(security:list,*args,**kwargs):
    # 获取发行期号
    return w.wss(security,"issue_issuenumber",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueCurrencyCodeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行币种时间序列
    return w.wsd(security,"issuecurrencycode",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueCurrencyCode(security:list,*args,**kwargs):
    # 获取发行币种
    return w.wss(security,"issuecurrencycode",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCurRSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取交易币种时间序列
    return w.wsd(security,"curr",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCurR(security:list,*args,**kwargs):
    # 获取交易币种
    return w.wss(security,"curr",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueIssueYearSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行年度时间序列
    return w.wsd(security,"issue_issueyear",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueIssueYear(security:list,*args,**kwargs):
    # 获取发行年度
    return w.wss(security,"issue_issueyear",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyUnderWritTypeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取承销方式时间序列
    return w.wsd(security,"agency_underwrittype",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyUnderWritType(security:list,*args,**kwargs):
    # 获取承销方式
    return w.wss(security,"agency_underwrittype",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueObjectSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行对象时间序列
    return w.wsd(security,"issue_object",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueObject(security:list,*args,**kwargs):
    # 获取发行对象
    return w.wss(security,"issue_object",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareNonTradableSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取非流通股(沪深)时间序列
    return w.wsd(security,"share_nontradable",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareNonTradable(security:list,*args,**kwargs):
    # 获取非流通股(沪深)
    return w.wss(security,"share_nontradable",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPrtFundNetAssetTotalSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资产净值(合计)时间序列
    return w.wsd(security,"prt_fundnetasset_total",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPrtFundNetAssetTotal(security:list,*args,**kwargs):
    # 获取资产净值(合计)
    return w.wss(security,"prt_fundnetasset_total",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstOughtTenderSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取应投家数时间序列
    return w.wsd(security,"tendrst_oughttender",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstOughtTender(security:list,*args,**kwargs):
    # 获取应投家数
    return w.wss(security,"tendrst_oughttender",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstInvestorTenderedSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取投标家数时间序列
    return w.wsd(security,"tendrst_investortendered",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstInvestorTendered(security:list,*args,**kwargs):
    # 获取投标家数
    return w.wss(security,"tendrst_investortendered",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInStYyBondRatingSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取(废弃)债项评级(YY)时间序列
    return w.wsd(security,"inst_yybondrating",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInStYyBondRating(security:list,*args,**kwargs):
    # 获取(废弃)债项评级(YY)
    return w.wss(security,"inst_yybondrating",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLatestIsSurerCreditRating2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取主体评级时间序列
    return w.wsd(security,"latestissurercreditrating2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLatestIsSurerCreditRating2(security:list,*args,**kwargs):
    # 获取主体评级
    return w.wss(security,"latestissurercreditrating2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInStYyIssuerRatingSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取主体评级(YY)时间序列
    return w.wsd(security,"inst_yyissuerrating",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInStYyIssuerRating(security:list,*args,**kwargs):
    # 获取主体评级(YY)
    return w.wss(security,"inst_yyissuerrating",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTotalLoanSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款总额(旧)时间序列
    return w.wsd(security,"total_loan",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTotalLoan(security:list,*args,**kwargs):
    # 获取贷款总额(旧)
    return w.wss(security,"total_loan",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTotalLoanNSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款总额时间序列
    return w.wsd(security,"total_loan_n",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTotalLoanN(security:list,*args,**kwargs):
    # 获取贷款总额
    return w.wss(security,"total_loan_n",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstWinningBidderSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取中标笔数时间序列
    return w.wsd(security,"tendrst_winningbidder",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstWinningBidder(security:list,*args,**kwargs):
    # 获取中标笔数
    return w.wss(security,"tendrst_winningbidder",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInvestmentRegionSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取投资区域时间序列
    return w.wsd(security,"fund_investmentregion",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInvestmentRegion(security:list,*args,**kwargs):
    # 获取投资区域
    return w.wss(security,"fund_investmentregion",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInvestConceptionSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取投资理念时间序列
    return w.wsd(security,"fund_investconception",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInvestConception(security:list,*args,**kwargs):
    # 获取投资理念
    return w.wss(security,"fund_investconception",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstWinnerBidderSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取中标家数时间序列
    return w.wsd(security,"tendrst_winnerbidder",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstWinnerBidder(security:list,*args,**kwargs):
    # 获取中标家数
    return w.wss(security,"tendrst_winnerbidder",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInvestScopeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取投资范围时间序列
    return w.wsd(security,"fund_investscope",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInvestScope(security:list,*args,**kwargs):
    # 获取投资范围
    return w.wss(security,"fund_investscope",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInvestObjectSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取投资目标时间序列
    return w.wsd(security,"fund_investobject",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInvestObject(security:list,*args,**kwargs):
    # 获取投资目标
    return w.wss(security,"fund_investobject",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstTendersSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取投标笔数时间序列
    return w.wsd(security,"tendrst_tenders",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstTenders(security:list,*args,**kwargs):
    # 获取投标笔数
    return w.wss(security,"tendrst_tenders",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaInterestDebtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取带息债务_PIT时间序列
    return w.wsd(security,"fa_interestdebt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaInterestDebt(security:list,*args,**kwargs):
    # 获取带息债务_PIT
    return w.wss(security,"fa_interestdebt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDInterestDebt2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取带息债务_GSD时间序列
    return w.wsd(security,"wgsd_interestdebt2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDInterestDebt2(security:list,*args,**kwargs):
    # 获取带息债务_GSD
    return w.wss(security,"wgsd_interestdebt2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInterestDebtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取带息债务时间序列
    return w.wsd(security,"interestdebt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInterestDebt(security:list,*args,**kwargs):
    # 获取带息债务
    return w.wss(security,"interestdebt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInfoNameSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金简称时间序列
    return w.wsd(security,"fund_info_name",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInfoName(security:list,*args,**kwargs):
    # 获取基金简称
    return w.wss(security,"fund_info_name",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNameOfficialSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金简称(官方)时间序列
    return w.wsd(security,"name_official",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNameOfficial(security:list,*args,**kwargs):
    # 获取基金简称(官方)
    return w.wss(security,"name_official",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundFullNameSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金全称时间序列
    return w.wsd(security,"fund_fullname",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundFullName(security:list,*args,**kwargs):
    # 获取基金全称
    return w.wss(security,"fund_fullname",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundFullNameEnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金全称(英文)时间序列
    return w.wsd(security,"fund_fullnameen",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundFullNameEn(security:list,*args,**kwargs):
    # 获取基金全称(英文)
    return w.wss(security,"fund_fullnameen",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundExistingYearSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取成立年限时间序列
    return w.wsd(security,"fund_existingyear",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundExistingYear(security:list,*args,**kwargs):
    # 获取成立年限
    return w.wss(security,"fund_existingyear",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDComPrIncSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取综合收益_GSD时间序列
    return w.wsd(security,"wgsd_compr_inc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDComPrInc(security:list,*args,**kwargs):
    # 获取综合收益_GSD
    return w.wss(security,"wgsd_compr_inc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInvestStyleSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取(停止)投资风格时间序列
    return w.wsd(security,"fund_investstyle",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInvestStyle(security:list,*args,**kwargs):
    # 获取(停止)投资风格
    return w.wss(security,"fund_investstyle",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWorkingCapitalSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营运资本时间序列
    return w.wsd(security,"workingcapital",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWorkingCapital(security:list,*args,**kwargs):
    # 获取营运资本
    return w.wss(security,"workingcapital",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRetainedEarningsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取留存收益时间序列
    return w.wsd(security,"retainedearnings",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRetainedEarnings(security:list,*args,**kwargs):
    # 获取留存收益
    return w.wss(security,"retainedearnings",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstInEffectTenderSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取无效笔数时间序列
    return w.wsd(security,"tendrst_ineffecttender",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstInEffectTender(security:list,*args,**kwargs):
    # 获取无效笔数
    return w.wss(security,"tendrst_ineffecttender",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstEffectTenderSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取有效笔数时间序列
    return w.wsd(security,"tendrst_effecttender",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstEffectTender(security:list,*args,**kwargs):
    # 获取有效笔数
    return w.wss(security,"tendrst_effecttender",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsEValueSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资产估值时间序列
    return w.wsd(security,"fund_reitsevalue",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsEValue(security:list,*args,**kwargs):
    # 获取资产估值
    return w.wss(security,"fund_reitsevalue",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDComEqRetainEarnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取留存收益_GSD时间序列
    return w.wsd(security,"wgsd_com_eq_retain_earn",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDComEqRetainEarn(security:list,*args,**kwargs):
    # 获取留存收益_GSD
    return w.wss(security,"wgsd_com_eq_retain_earn",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaRetainEarnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取留存收益_PIT时间序列
    return w.wsd(security,"fa_retainearn",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaRetainEarn(security:list,*args,**kwargs):
    # 获取留存收益_PIT
    return w.wss(security,"fa_retainearn",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDWorkingCapital2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取营运资本_GSD时间序列
    return w.wsd(security,"wgsd_workingcapital2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDWorkingCapital2(security:list,*args,**kwargs):
    # 获取营运资本_GSD
    return w.wss(security,"wgsd_workingcapital2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundRedMStatusSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取赎回状态时间序列
    return w.wsd(security,"fund_redmstatus",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundRedMStatus(security:list,*args,**kwargs):
    # 获取赎回状态
    return w.wss(security,"fund_redmstatus",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstTenderAmountSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取投标(申购)总量时间序列
    return w.wsd(security,"tendrst_tenderamount",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstTenderAmount(security:list,*args,**kwargs):
    # 获取投标(申购)总量
    return w.wss(security,"tendrst_tenderamount",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBondScoreSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取(停止)债券评分时间序列
    return w.wsd(security,"bondscore",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBondScore(security:list,*args,**kwargs):
    # 获取(停止)债券评分
    return w.wss(security,"bondscore",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPcHmStatusSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取申购状态时间序列
    return w.wsd(security,"fund_pchmstatus",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPcHmStatus(security:list,*args,**kwargs):
    # 获取申购状态
    return w.wss(security,"fund_pchmstatus",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundMarketOutlookSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取市场展望时间序列
    return w.wsd(security,"fund_marketoutlook",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundMarketOutlook(security:list,*args,**kwargs):
    # 获取市场展望
    return w.wss(security,"fund_marketoutlook",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundMarketAnalysisSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取市场分析时间序列
    return w.wsd(security,"fund_marketanalysis",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundMarketAnalysis(security:list,*args,**kwargs):
    # 获取市场分析
    return w.wss(security,"fund_marketanalysis",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundRedemptionFee2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取赎回费率(支持历史)时间序列
    return w.wsd(security,"fund_redemptionfee2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundRedemptionFee2(security:list,*args,**kwargs):
    # 获取赎回费率(支持历史)
    return w.wss(security,"fund_redemptionfee2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundRedemptionFeeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取赎回费率时间序列
    return w.wsd(security,"fund_redemptionfee",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundRedemptionFee(security:list,*args,**kwargs):
    # 获取赎回费率
    return w.wss(security,"fund_redemptionfee",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPurchaseFee2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取申购费率(支持历史)时间序列
    return w.wsd(security,"fund_purchasefee2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPurchaseFee2(security:list,*args,**kwargs):
    # 获取申购费率(支持历史)
    return w.wss(security,"fund_purchasefee2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPurchaseFeeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取申购费率时间序列
    return w.wsd(security,"fund_purchasefee",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPurchaseFee(security:list,*args,**kwargs):
    # 获取申购费率
    return w.wss(security,"fund_purchasefee",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSubscriptionFee2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取认购费率(支持历史)时间序列
    return w.wsd(security,"fund_subscriptionfee2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSubscriptionFee2(security:list,*args,**kwargs):
    # 获取认购费率(支持历史)
    return w.wss(security,"fund_subscriptionfee2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSubscriptionFeeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取认购费率时间序列
    return w.wsd(security,"fund_subscriptionfee",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSubscriptionFee(security:list,*args,**kwargs):
    # 获取认购费率
    return w.wss(security,"fund_subscriptionfee",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCustodianFeeRatio2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取托管费率(支持历史)时间序列
    return w.wsd(security,"fund_custodianfeeratio2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCustodianFeeRatio2(security:list,*args,**kwargs):
    # 获取托管费率(支持历史)
    return w.wss(security,"fund_custodianfeeratio2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCustodianFeeRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取托管费率时间序列
    return w.wsd(security,"fund_custodianfeeratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCustodianFeeRatio(security:list,*args,**kwargs):
    # 获取托管费率
    return w.wss(security,"fund_custodianfeeratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagementFeeRatio2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取管理费率(支持历史)时间序列
    return w.wsd(security,"fund_managementfeeratio2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagementFeeRatio2(security:list,*args,**kwargs):
    # 获取管理费率(支持历史)
    return w.wss(security,"fund_managementfeeratio2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank647Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取存款余额_存款总额时间序列
    return w.wsd(security,"stmnote_bank_647",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank647(security:list,*args,**kwargs):
    # 获取存款余额_存款总额
    return w.wss(security,"stmnote_bank_647",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDAssetsOThSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他资产_GSD时间序列
    return w.wsd(security,"wgsd_assets_oth",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDAssetsOTh(security:list,*args,**kwargs):
    # 获取其他资产_GSD
    return w.wss(security,"wgsd_assets_oth",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPrtOtherSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他资产时间序列
    return w.wsd(security,"prt_other",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPrtOther(security:list,*args,**kwargs):
    # 获取其他资产
    return w.wss(security,"prt_other",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs18Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他资产_FUND时间序列
    return w.wsd(security,"stm_bs_18",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs18(security:list,*args,**kwargs):
    # 获取其他资产_FUND
    return w.wss(security,"stm_bs_18",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTotalDepositSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取存款总额(旧)时间序列
    return w.wsd(security,"total_deposit",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTotalDeposit(security:list,*args,**kwargs):
    # 获取存款总额(旧)
    return w.wss(security,"total_deposit",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderExpLnTenderSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取投标说明时间序列
    return w.wsd(security,"tender_explntender",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderExpLnTender(security:list,*args,**kwargs):
    # 获取投标说明
    return w.wss(security,"tender_explntender",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRateRateBondSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取债项评级时间序列
    return w.wsd(security,"rate_ratebond",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRateRateBond(security:list,*args,**kwargs):
    # 获取债项评级
    return w.wss(security,"rate_ratebond",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyFAdvisorSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取财务顾问时间序列
    return w.wsd(security,"agency_fadvisor",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyFAdvisor(security:list,*args,**kwargs):
    # 获取财务顾问
    return w.wss(security,"agency_fadvisor",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowNetPriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取(废弃)净值价格时间序列
    return w.wsd(security,"fellow_netprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowNetPrice(security:list,*args,**kwargs):
    # 获取(废弃)净值价格
    return w.wss(security,"fellow_netprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundTypeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金类型时间序列
    return w.wsd(security,"fund_type",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundType(security:list,*args,**kwargs):
    # 获取基金类型
    return w.wss(security,"fund_type",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundFirstInvestTypeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取投资类型(一级分类)时间序列
    return w.wsd(security,"fund_firstinvesttype",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundFirstInvestType(security:list,*args,**kwargs):
    # 获取投资类型(一级分类)
    return w.wss(security,"fund_firstinvesttype",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstAmNtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取招标总量时间序列
    return w.wsd(security,"tendrst_amnt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstAmNt(security:list,*args,**kwargs):
    # 获取招标总量
    return w.wss(security,"tendrst_amnt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInvestTypeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取投资类型(二级分类)时间序列
    return w.wsd(security,"fund_investtype",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInvestType(security:list,*args,**kwargs):
    # 获取投资类型(二级分类)
    return w.wss(security,"fund_investtype",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInvestTypeAnytimeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取投资类型(支持历史)时间序列
    return w.wsd(security,"fund_investtype_anytime",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInvestTypeAnytime(security:list,*args,**kwargs):
    # 获取投资类型(支持历史)
    return w.wss(security,"fund_investtype_anytime",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInvestTypeEngSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取投资类型(英文)时间序列
    return w.wsd(security,"fund_investtypeeng",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInvestTypeEng(security:list,*args,**kwargs):
    # 获取投资类型(英文)
    return w.wss(security,"fund_investtypeeng",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDefaultSourceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取(废弃)估值来源时间序列
    return w.wsd(security,"defaultsource",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDefaultSource(security:list,*args,**kwargs):
    # 获取(废弃)估值来源
    return w.wss(security,"defaultsource",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPrtGovernmentBondSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取国债市值时间序列
    return w.wsd(security,"prt_governmentbond",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPrtGovernmentBond(security:list,*args,**kwargs):
    # 获取国债市值
    return w.wss(security,"prt_governmentbond",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTotalDepositNSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取存款总额时间序列
    return w.wsd(security,"total_deposit_n",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTotalDepositN(security:list,*args,**kwargs):
    # 获取存款总额
    return w.wss(security,"total_deposit_n",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagementFeeRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取管理费率时间序列
    return w.wsd(security,"fund_managementfeeratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagementFeeRatio(security:list,*args,**kwargs):
    # 获取管理费率
    return w.wss(security,"fund_managementfeeratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInvestType2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取投资类型时间序列
    return w.wsd(security,"fund_investtype2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInvestType2(security:list,*args,**kwargs):
    # 获取投资类型
    return w.wss(security,"fund_investtype2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueTypeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行方式时间序列
    return w.wsd(security,"issue_type",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueType(security:list,*args,**kwargs):
    # 获取发行方式
    return w.wss(security,"issue_type",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank688Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款余额_汽车贷款时间序列
    return w.wsd(security,"stmnote_bank_688",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank688(security:list,*args,**kwargs):
    # 获取贷款余额_汽车贷款
    return w.wss(security,"stmnote_bank_688",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssueTypeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取配股方式时间序列
    return w.wsd(security,"rightsissue_type",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssueType(security:list,*args,**kwargs):
    # 获取配股方式
    return w.wss(security,"rightsissue_type",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDDupontAssetsToEquitySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取权益乘数(杜邦分析)_GSD时间序列
    return w.wsd(security,"wgsd_dupont_assetstoequity",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDDupontAssetsToEquity(security:list,*args,**kwargs):
    # 获取权益乘数(杜邦分析)_GSD
    return w.wss(security,"wgsd_dupont_assetstoequity",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur7806Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取基建投资时间序列
    return w.wsd(security,"stmnote_insur_7806",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur7806(security:list,*args,**kwargs):
    # 获取基建投资
    return w.wss(security,"stmnote_insur_7806",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur7805Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取股权投资时间序列
    return w.wsd(security,"stmnote_insur_7805",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur7805(security:list,*args,**kwargs):
    # 获取股权投资
    return w.wss(security,"stmnote_insur_7805",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDYoyoP2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业利润(同比增长率)_GSD时间序列
    return w.wsd(security,"wgsd_yoyop2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDYoyoP2(security:list,*args,**kwargs):
    # 获取营业利润(同比增长率)_GSD
    return w.wss(security,"wgsd_yoyop2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowTotalRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总中签率时间序列
    return w.wsd(security,"fellow_totalratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowTotalRatio(security:list,*args,**kwargs):
    # 获取总中签率
    return w.wss(security,"fellow_totalratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur7804Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取股票投资时间序列
    return w.wsd(security,"stmnote_insur_7804",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur7804(security:list,*args,**kwargs):
    # 获取股票投资
    return w.wss(security,"stmnote_insur_7804",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs201Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金投资_FUND时间序列
    return w.wsd(security,"stm_bs_201",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs201(security:list,*args,**kwargs):
    # 获取基金投资_FUND
    return w.wss(security,"stm_bs_201",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur7803Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金投资时间序列
    return w.wsd(security,"stmnote_insur_7803",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur7803(security:list,*args,**kwargs):
    # 获取基金投资
    return w.wss(security,"stmnote_insur_7803",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs7Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取债券投资_FUND时间序列
    return w.wsd(security,"stm_bs_7",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs7(security:list,*args,**kwargs):
    # 获取债券投资_FUND
    return w.wss(security,"stm_bs_7",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur7802Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取债券投资时间序列
    return w.wsd(security,"stmnote_insur_7802",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur7802(security:list,*args,**kwargs):
    # 获取债券投资
    return w.wss(security,"stmnote_insur_7802",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur7801Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取定期存款(投资)时间序列
    return w.wsd(security,"stmnote_insur_7801",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur7801(security:list,*args,**kwargs):
    # 获取定期存款(投资)
    return w.wss(security,"stmnote_insur_7801",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur20Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取最低资本(寿险)(旧)时间序列
    return w.wsd(security,"stmnote_insur_20",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur20(security:list,*args,**kwargs):
    # 获取最低资本(寿险)(旧)
    return w.wss(security,"stmnote_insur_20",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur20NSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最低资本(寿险)时间序列
    return w.wsd(security,"stmnote_insur_20n",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur20N(security:list,*args,**kwargs):
    # 获取最低资本(寿险)
    return w.wss(security,"stmnote_insur_20n",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur19Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取实际资本(寿险)(旧)时间序列
    return w.wsd(security,"stmnote_insur_19",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur19(security:list,*args,**kwargs):
    # 获取实际资本(寿险)(旧)
    return w.wss(security,"stmnote_insur_19",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur19NSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取实际资本(寿险)时间序列
    return w.wsd(security,"stmnote_insur_19n",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur19N(security:list,*args,**kwargs):
    # 获取实际资本(寿险)
    return w.wss(security,"stmnote_insur_19n",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNeEqParkSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取挂牌园区时间序列
    return w.wsd(security,"neeq_park",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNeEqPark(security:list,*args,**kwargs):
    # 获取挂牌园区
    return w.wss(security,"neeq_park",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskMaxDownsideSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最大回撤时间序列
    return w.wsd(security,"risk_maxdownside",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskMaxDownside(security:list,*args,**kwargs):
    # 获取最大回撤
    return w.wss(security,"risk_maxdownside",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSec2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取受托资金时间序列
    return w.wsd(security,"stmnote_sec_2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSec2(security:list,*args,**kwargs):
    # 获取受托资金
    return w.wss(security,"stmnote_sec_2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUpDaysSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取连涨天数时间序列
    return w.wsd(security,"up_days",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUpDays(security:list,*args,**kwargs):
    # 获取连涨天数
    return w.wss(security,"up_days",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSecOp2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取自营股票时间序列
    return w.wsd(security,"stmnote_sec_op_2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSecOp2(security:list,*args,**kwargs):
    # 获取自营股票
    return w.wss(security,"stmnote_sec_op_2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSecOp3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取自营国债时间序列
    return w.wsd(security,"stmnote_sec_op_3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSecOp3(security:list,*args,**kwargs):
    # 获取自营国债
    return w.wss(security,"stmnote_sec_op_3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSecOp4Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取自营基金时间序列
    return w.wsd(security,"stmnote_sec_op_4",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSecOp4(security:list,*args,**kwargs):
    # 获取自营基金
    return w.wss(security,"stmnote_sec_op_4",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDownDaysSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取连跌天数时间序列
    return w.wsd(security,"down_days",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDownDays(security:list,*args,**kwargs):
    # 获取连跌天数
    return w.wss(security,"down_days",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDupontAssetsToEquitySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取权益乘数(杜邦分析)时间序列
    return w.wsd(security,"dupont_assetstoequity",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDupontAssetsToEquity(security:list,*args,**kwargs):
    # 获取权益乘数(杜邦分析)
    return w.wss(security,"dupont_assetstoequity",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMarketMakeDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取做市首日时间序列
    return w.wsd(security,"marketmakedate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMarketMakeDate(security:list,*args,**kwargs):
    # 获取做市首日
    return w.wss(security,"marketmakedate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur13NSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取实际资本(产险)时间序列
    return w.wsd(security,"stmnote_insur_13n",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur13N(security:list,*args,**kwargs):
    # 获取实际资本(产险)
    return w.wss(security,"stmnote_insur_13n",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur13Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取实际资本(产险)(旧)时间序列
    return w.wsd(security,"stmnote_insur_13",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur13(security:list,*args,**kwargs):
    # 获取实际资本(产险)(旧)
    return w.wss(security,"stmnote_insur_13",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur14NSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最低资本(产险)时间序列
    return w.wsd(security,"stmnote_insur_14n",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur14N(security:list,*args,**kwargs):
    # 获取最低资本(产险)
    return w.wss(security,"stmnote_insur_14n",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur14Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取最低资本(产险)(旧)时间序列
    return w.wsd(security,"stmnote_insur_14",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur14(security:list,*args,**kwargs):
    # 获取最低资本(产险)(旧)
    return w.wss(security,"stmnote_insur_14",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur16NSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取内含价值(寿险)时间序列
    return w.wsd(security,"stmnote_insur_16n",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur16N(security:list,*args,**kwargs):
    # 获取内含价值(寿险)
    return w.wss(security,"stmnote_insur_16n",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur16Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取内含价值(寿险)(旧)时间序列
    return w.wsd(security,"stmnote_insur_16",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur16(security:list,*args,**kwargs):
    # 获取内含价值(寿险)(旧)
    return w.wss(security,"stmnote_insur_16",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTransferTypeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取交易类型时间序列
    return w.wsd(security,"transfertype",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTransferType(security:list,*args,**kwargs):
    # 获取交易类型
    return w.wss(security,"transfertype",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoLeadUndRN1Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取主办券商(持续督导)时间序列
    return w.wsd(security,"ipo_leadundr_n1",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoLeadUndRN1(security:list,*args,**kwargs):
    # 获取主办券商(持续督导)
    return w.wss(security,"ipo_leadundr_n1",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDaySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取剩余期限(天)时间序列
    return w.wsd(security,"day",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDay(security:list,*args,**kwargs):
    # 获取剩余期限(天)
    return w.wss(security,"day",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerOnThePostDaysSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取任职天数时间序列
    return w.wsd(security,"fund_manager_onthepostdays",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerOnThePostDays(security:list,*args,**kwargs):
    # 获取任职天数
    return w.wss(security,"fund_manager_onthepostdays",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration3MSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取3月久期时间序列
    return w.wsd(security,"duration_3m",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration3M(security:list,*args,**kwargs):
    # 获取3月久期
    return w.wss(security,"duration_3m",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDebtInvestSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取债权投资时间序列
    return w.wsd(security,"debt_invest",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDebtInvest(security:list,*args,**kwargs):
    # 获取债权投资
    return w.wss(security,"debt_invest",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFinInvestSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取金融投资时间序列
    return w.wsd(security,"fin_invest",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFinInvest(security:list,*args,**kwargs):
    # 获取金融投资
    return w.wss(security,"fin_invest",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration1MSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取1月久期时间序列
    return w.wsd(security,"duration_1m",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration1M(security:list,*args,**kwargs):
    # 获取1月久期
    return w.wss(security,"duration_1m",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getToTAccTRcVSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取应收款项时间序列
    return w.wsd(security,"tot_acct_rcv",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getToTAccTRcV(security:list,*args,**kwargs):
    # 获取应收款项
    return w.wss(security,"tot_acct_rcv",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getConvexityIfExeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取行权凸性时间序列
    return w.wsd(security,"convexity_ifexe",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getConvexityIfExe(security:list,*args,**kwargs):
    # 获取行权凸性
    return w.wss(security,"convexity_ifexe",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPremRcVSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取应收保费时间序列
    return w.wsd(security,"prem_rcv",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPremRcV(security:list,*args,**kwargs):
    # 获取应收保费
    return w.wss(security,"prem_rcv",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRecEivInSurSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取应收保费_GSD时间序列
    return w.wsd(security,"wgsd_receiv_insur",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRecEivInSur(security:list,*args,**kwargs):
    # 获取应收保费_GSD
    return w.wss(security,"wgsd_receiv_insur",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMarginAccTSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取融出资金时间序列
    return w.wsd(security,"margin_acct",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMarginAccT(security:list,*args,**kwargs):
    # 获取融出资金
    return w.wss(security,"margin_acct",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLoansToOThBanksSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取拆出资金时间序列
    return w.wsd(security,"loans_to_oth_banks",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLoansToOThBanks(security:list,*args,**kwargs):
    # 获取拆出资金
    return w.wss(security,"loans_to_oth_banks",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDLendIbSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取拆出资金_GSD时间序列
    return w.wsd(security,"wgsd_lend_ib",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDLendIb(security:list,*args,**kwargs):
    # 获取拆出资金_GSD
    return w.wss(security,"wgsd_lend_ib",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDurationIfExerciseSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取行权久期时间序列
    return w.wsd(security,"durationifexercise",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDurationIfExercise(security:list,*args,**kwargs):
    # 获取行权久期
    return w.wss(security,"durationifexercise",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDeferredExpSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取待摊费用时间序列
    return w.wsd(security,"deferred_exp",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDeferredExp(security:list,*args,**kwargs):
    # 获取待摊费用
    return w.wss(security,"deferred_exp",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs12Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取应收利息_FUND时间序列
    return w.wsd(security,"stm_bs_12",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs12(security:list,*args,**kwargs):
    # 获取应收利息_FUND
    return w.wss(security,"stm_bs_12",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIntRcVSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取应收利息时间序列
    return w.wsd(security,"int_rcv",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIntRcV(security:list,*args,**kwargs):
    # 获取应收利息
    return w.wss(security,"int_rcv",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs11Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取应收股利_FUND时间序列
    return w.wsd(security,"stm_bs_11",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs11(security:list,*args,**kwargs):
    # 获取应收股利_FUND
    return w.wss(security,"stm_bs_11",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDvdRcVSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取应收股利时间序列
    return w.wsd(security,"dvd_rcv",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDvdRcV(security:list,*args,**kwargs):
    # 获取应收股利
    return w.wss(security,"dvd_rcv",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerStartDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取任职日期时间序列
    return w.wsd(security,"fund_manager_startdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerStartDate(security:list,*args,**kwargs):
    # 获取任职日期
    return w.wss(security,"fund_manager_startdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAccruedInterestSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取应计利息时间序列
    return w.wsd(security,"accruedinterest",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAccruedInterest(security:list,*args,**kwargs):
    # 获取应计利息
    return w.wss(security,"accruedinterest",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getQStmNoteInSur212514Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取实际资本时间序列
    return w.wsd(security,"qstmnote_insur_212514",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getQStmNoteInSur212514(security:list,*args,**kwargs):
    # 获取实际资本
    return w.wss(security,"qstmnote_insur_212514",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getQStmNoteInSur212519Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取最低资本时间序列
    return w.wsd(security,"qstmnote_insur_212519",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getQStmNoteInSur212519(security:list,*args,**kwargs):
    # 获取最低资本
    return w.wss(security,"qstmnote_insur_212519",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBDurationSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基准久期时间序列
    return w.wsd(security,"bduration",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBDuration(security:list,*args,**kwargs):
    # 获取基准久期
    return w.wss(security,"bduration",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getQStmNoteInSur212528Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取附加资本时间序列
    return w.wsd(security,"qstmnote_insur_212528",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getQStmNoteInSur212528(security:list,*args,**kwargs):
    # 获取附加资本
    return w.wss(security,"qstmnote_insur_212528",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPtMYearSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取剩余期限(年)时间序列
    return w.wsd(security,"ptmyear",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPtMYear(security:list,*args,**kwargs):
    # 获取剩余期限(年)
    return w.wss(security,"ptmyear",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getQStmNoteInSur212530Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取净现金流时间序列
    return w.wsd(security,"qstmnote_insur_212530",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getQStmNoteInSur212530(security:list,*args,**kwargs):
    # 获取净现金流
    return w.wss(security,"qstmnote_insur_212530",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDFundRestrictedSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取受限资金_GSD时间序列
    return w.wsd(security,"wgsd_fund_restricted",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDFundRestricted(security:list,*args,**kwargs):
    # 获取受限资金_GSD
    return w.wss(security,"wgsd_fund_restricted",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundRestrictedSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取受限资金时间序列
    return w.wsd(security,"fund_restricted",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundRestricted(security:list,*args,**kwargs):
    # 获取受限资金
    return w.wss(security,"fund_restricted",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNotesRcVSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取应收票据时间序列
    return w.wsd(security,"notes_rcv",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNotesRcV(security:list,*args,**kwargs):
    # 获取应收票据
    return w.wss(security,"notes_rcv",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSDurationSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取利差久期时间序列
    return w.wsd(security,"sduration",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSDuration(security:list,*args,**kwargs):
    # 获取利差久期
    return w.wss(security,"sduration",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAccTRcVSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取应收账款时间序列
    return w.wsd(security,"acct_rcv",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAccTRcV(security:list,*args,**kwargs):
    # 获取应收账款
    return w.wss(security,"acct_rcv",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPrepaySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取预付款项时间序列
    return w.wsd(security,"prepay",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPrepay(security:list,*args,**kwargs):
    # 获取预付款项
    return w.wss(security,"prepay",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNeEqLevelSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取所属分层时间序列
    return w.wsd(security,"neeq_level",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNeEqLevel(security:list,*args,**kwargs):
    # 获取所属分层
    return w.wss(security,"neeq_level",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDepositAryBankSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取存托机构时间序列
    return w.wsd(security,"depositarybank",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDepositAryBank(security:list,*args,**kwargs):
    # 获取存托机构
    return w.wss(security,"depositarybank",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyReGuarantorSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取再担保人时间序列
    return w.wsd(security,"agency_reguarantor",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyReGuarantor(security:list,*args,**kwargs):
    # 获取再担保人
    return w.wss(security,"agency_reguarantor",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOfficialStyleSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取指数风格时间序列
    return w.wsd(security,"officialstyle",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOfficialStyle(security:list,*args,**kwargs):
    # 获取指数风格
    return w.wss(security,"officialstyle",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank741Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款余额_信用贷款时间序列
    return w.wsd(security,"stmnote_bank_741",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank741(security:list,*args,**kwargs):
    # 获取贷款余额_信用贷款
    return w.wss(security,"stmnote_bank_741",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCNvXTyShcSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取估价凸性(上清所)时间序列
    return w.wsd(security,"cnvxty_shc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCNvXTyShc(security:list,*args,**kwargs):
    # 获取估价凸性(上清所)
    return w.wss(security,"cnvxty_shc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAccruedInterestShcSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取应计利息(上清所)时间序列
    return w.wsd(security,"accruedinterest_shc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAccruedInterestShc(security:list,*args,**kwargs):
    # 获取应计利息(上清所)
    return w.wss(security,"accruedinterest_shc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getExChCitySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取上市地点时间序列
    return w.wsd(security,"exch_city",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getExChCity(security:list,*args,**kwargs):
    # 获取上市地点
    return w.wss(security,"exch_city",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDirtyShcSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取估价全价(上清所)时间序列
    return w.wsd(security,"dirty_shc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDirtyShc(security:list,*args,**kwargs):
    # 获取估价全价(上清所)
    return w.wss(security,"dirty_shc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetShcSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取估价净价(上清所)时间序列
    return w.wsd(security,"net_shc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetShc(security:list,*args,**kwargs):
    # 获取估价净价(上清所)
    return w.wss(security,"net_shc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRateLatestMirCsiSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取隐含评级(中证指数)时间序列
    return w.wsd(security,"rate_latestMIR_csi",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRateLatestMirCsi(security:list,*args,**kwargs):
    # 获取隐含评级(中证指数)
    return w.wss(security,"rate_latestMIR_csi",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLaunchDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发布日期时间序列
    return w.wsd(security,"launchdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLaunchDate(security:list,*args,**kwargs):
    # 获取发布日期
    return w.wss(security,"launchdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCNvXTyCsi1Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取估价凸性(中证指数)时间序列
    return w.wsd(security,"cnvxty_csi1",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCNvXTyCsi1(security:list,*args,**kwargs):
    # 获取估价凸性(中证指数)
    return w.wss(security,"cnvxty_csi1",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskBetaUnIncomeTaxRateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取Beta(剔除所得税率)时间序列
    return w.wsd(security,"risk_betaunincometaxrate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskBetaUnIncomeTaxRate(security:list,*args,**kwargs):
    # 获取Beta(剔除所得税率)
    return w.wss(security,"risk_betaunincometaxrate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAccruedInterestCsiSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取应计利息(中证指数)时间序列
    return w.wsd(security,"accruedinterest_csi",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAccruedInterestCsi(security:list,*args,**kwargs):
    # 获取应计利息(中证指数)
    return w.wss(security,"accruedinterest_csi",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRepoBriefingSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取证券简介时间序列
    return w.wsd(security,"repo_briefing",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRepoBriefing(security:list,*args,**kwargs):
    # 获取证券简介
    return w.wss(security,"repo_briefing",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDirtyCsi1Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取估价全价(中证指数)时间序列
    return w.wsd(security,"dirty_csi1",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDirtyCsi1(security:list,*args,**kwargs):
    # 获取估价全价(中证指数)
    return w.wss(security,"dirty_csi1",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetCsi1Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取估价净价(中证指数)时间序列
    return w.wsd(security,"net_csi1",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetCsi1(security:list,*args,**kwargs):
    # 获取估价净价(中证指数)
    return w.wss(security,"net_csi1",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLatestParCnBdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取剩余本金(中债)时间序列
    return w.wsd(security,"latestpar_cnbd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLatestParCnBd(security:list,*args,**kwargs):
    # 获取剩余本金(中债)
    return w.wss(security,"latestpar_cnbd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMethodologySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取加权方式时间序列
    return w.wsd(security,"methodology",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMethodology(security:list,*args,**kwargs):
    # 获取加权方式
    return w.wss(security,"methodology",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNumberOfConstituents2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取成份个数(支持历史)时间序列
    return w.wsd(security,"numberofconstituents2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNumberOfConstituents2(security:list,*args,**kwargs):
    # 获取成份个数(支持历史)
    return w.wss(security,"numberofconstituents2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsLimitedShareSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取限售份额时间序列
    return w.wsd(security,"fund_reitslimitedshare",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsLimitedShare(security:list,*args,**kwargs):
    # 获取限售份额
    return w.wss(security,"fund_reitslimitedshare",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行日期时间序列
    return w.wsd(security,"issue_date",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueDate(security:list,*args,**kwargs):
    # 获取发行日期
    return w.wss(security,"issue_date",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetCnBdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取估价净价(中债)时间序列
    return w.wsd(security,"net_cnbd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetCnBd(security:list,*args,**kwargs):
    # 获取估价净价(中债)
    return w.wss(security,"net_cnbd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDirtyCnBdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取估价全价(中债)时间序列
    return w.wsd(security,"dirty_cnbd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDirtyCnBd(security:list,*args,**kwargs):
    # 获取估价全价(中债)
    return w.wss(security,"dirty_cnbd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCalcPvbPSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基点价值时间序列
    return w.wsd(security,"calc_pvbp",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCalcPvbP(security:list,*args,**kwargs):
    # 获取基点价值
    return w.wss(security,"calc_pvbp",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMatUCnBdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取待偿年限(年)(中债)时间序列
    return w.wsd(security,"matu_cnbd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMatUCnBd(security:list,*args,**kwargs):
    # 获取待偿年限(年)(中债)
    return w.wss(security,"matu_cnbd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank742Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款余额_保证贷款时间序列
    return w.wsd(security,"stmnote_bank_742",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank742(security:list,*args,**kwargs):
    # 获取贷款余额_保证贷款
    return w.wss(security,"stmnote_bank_742",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAccruedInterestCnBdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取应计利息(中债)时间序列
    return w.wsd(security,"accruedinterest_cnbd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAccruedInterestCnBd(security:list,*args,**kwargs):
    # 获取应计利息(中债)
    return w.wss(security,"accruedinterest_cnbd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseConversionCodeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取转股代码时间序列
    return w.wsd(security,"clause_conversion_code",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseConversionCode(security:list,*args,**kwargs):
    # 获取转股代码
    return w.wss(security,"clause_conversion_code",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseConversion2SwapSharePriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取转股价格时间序列
    return w.wsd(security,"clause_conversion2_swapshareprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseConversion2SwapSharePrice(security:list,*args,**kwargs):
    # 获取转股价格
    return w.wss(security,"clause_conversion2_swapshareprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCNvXTyCnBdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取估价凸性(中债)时间序列
    return w.wsd(security,"cnvxty_cnbd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCNvXTyCnBd(security:list,*args,**kwargs):
    # 获取估价凸性(中债)
    return w.wss(security,"cnvxty_cnbd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerEnddateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取离职日期时间序列
    return w.wsd(security,"fund_manager_enddate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerEnddate(security:list,*args,**kwargs):
    # 获取离职日期
    return w.wss(security,"fund_manager_enddate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNumberOfConstituentsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取成份个数时间序列
    return w.wsd(security,"numberofconstituents",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNumberOfConstituents(security:list,*args,**kwargs):
    # 获取成份个数
    return w.wss(security,"numberofconstituents",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank689Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款余额_其他个人贷款时间序列
    return w.wsd(security,"stmnote_bank_689",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank689(security:list,*args,**kwargs):
    # 获取贷款余额_其他个人贷款
    return w.wss(security,"stmnote_bank_689",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseConversion2ConversionProportionSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取转换比例时间序列
    return w.wsd(security,"clause_conversion2_conversionproportion",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseConversion2ConversionProportion(security:list,*args,**kwargs):
    # 获取转换比例
    return w.wss(security,"clause_conversion2_conversionproportion",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07IsReItsRdFeeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取研发费用时间序列
    return w.wsd(security,"stm07_is_reits_rdfee",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07IsReItsRdFee(security:list,*args,**kwargs):
    # 获取研发费用
    return w.wss(security,"stm07_is_reits_rdfee",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRdExpSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取研发费用_GSD时间序列
    return w.wsd(security,"wgsd_rd_exp",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRdExp(security:list,*args,**kwargs):
    # 获取研发费用_GSD
    return w.wss(security,"wgsd_rd_exp",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTradeCodeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取证券代码时间序列
    return w.wsd(security,"trade_code",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTradeCode(security:list,*args,**kwargs):
    # 获取证券代码
    return w.wss(security,"trade_code",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs70Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取短期借款_FUND时间序列
    return w.wsd(security,"stm_bs_70",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs70(security:list,*args,**kwargs):
    # 获取短期借款_FUND
    return w.wss(security,"stm_bs_70",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPledgeLoanSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取质押借款时间序列
    return w.wsd(security,"pledge_loan",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPledgeLoan(security:list,*args,**kwargs):
    # 获取质押借款
    return w.wss(security,"pledge_loan",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLtBorrowSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取长期借款时间序列
    return w.wsd(security,"lt_borrow",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLtBorrow(security:list,*args,**kwargs):
    # 获取长期借款
    return w.wss(security,"lt_borrow",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStBorrowSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取短期借款时间序列
    return w.wsd(security,"st_borrow",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStBorrow(security:list,*args,**kwargs):
    # 获取短期借款
    return w.wss(security,"st_borrow",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBorrow4512Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取借款合计时间序列
    return w.wsd(security,"stmnote_Borrow_4512",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBorrow4512(security:list,*args,**kwargs):
    # 获取借款合计
    return w.wss(security,"stmnote_Borrow_4512",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowTrnFfAmtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取回拨数量时间序列
    return w.wsd(security,"fellow_trnffamt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowTrnFfAmt(security:list,*args,**kwargs):
    # 获取回拨数量
    return w.wss(security,"fellow_trnffamt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssueProgressSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取配股进度时间序列
    return w.wsd(security,"rightsissue_progress",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssueProgress(security:list,*args,**kwargs):
    # 获取配股进度
    return w.wss(security,"rightsissue_progress",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsCashSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取货币资金时间序列
    return w.wsd(security,"stm07_bs_reits_cash",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsCash(security:list,*args,**kwargs):
    # 获取货币资金
    return w.wss(security,"stm07_bs_reits_cash",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSecTypeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取证券类型时间序列
    return w.wsd(security,"sec_type",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSecType(security:list,*args,**kwargs):
    # 获取证券类型
    return w.wss(security,"sec_type",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGuarTermSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取担保期限时间序列
    return w.wsd(security,"guarterm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGuarTerm(security:list,*args,**kwargs):
    # 获取担保期限
    return w.wss(security,"guarterm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPrtCashSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取银行存款时间序列
    return w.wsd(security,"prt_cash",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPrtCash(security:list,*args,**kwargs):
    # 获取银行存款
    return w.wss(security,"prt_cash",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs1Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取银行存款_FUND时间序列
    return w.wsd(security,"stm_bs_1",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs1(security:list,*args,**kwargs):
    # 获取银行存款_FUND
    return w.wss(security,"stm_bs_1",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getListSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取是否上市时间序列
    return w.wsd(security,"list",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getList(security:list,*args,**kwargs):
    # 获取是否上市
    return w.wss(security,"list",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyGrNtTypeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取担保方式时间序列
    return w.wsd(security,"agency_grnttype",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyGrNtType(security:list,*args,**kwargs):
    # 获取担保方式
    return w.wss(security,"agency_grnttype",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGuarRangeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取担保范围时间序列
    return w.wsd(security,"guarrange",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGuarRange(security:list,*args,**kwargs):
    # 获取担保范围
    return w.wss(security,"guarrange",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration1YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取1年久期时间序列
    return w.wsd(security,"duration_1y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration1Y(security:list,*args,**kwargs):
    # 获取1年久期
    return w.wss(security,"duration_1y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssuePriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取配股价格时间序列
    return w.wsd(security,"rightsissue_price",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssuePrice(security:list,*args,**kwargs):
    # 获取配股价格
    return w.wss(security,"rightsissue_price",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssueBaseShareSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基准股本时间序列
    return w.wsd(security,"rightsissue_baseshare",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssueBaseShare(security:list,*args,**kwargs):
    # 获取基准股本
    return w.wss(security,"rightsissue_baseshare",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank743Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款余额_抵押贷款时间序列
    return w.wsd(security,"stmnote_bank_743",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank743(security:list,*args,**kwargs):
    # 获取贷款余额_抵押贷款
    return w.wss(security,"stmnote_bank_743",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank744Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款余额_质押贷款时间序列
    return w.wsd(security,"stmnote_bank_744",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank744(security:list,*args,**kwargs):
    # 获取贷款余额_质押贷款
    return w.wss(security,"stmnote_bank_744",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUnderlyingNameSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取正股简称时间序列
    return w.wsd(security,"underlyingname",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUnderlyingName(security:list,*args,**kwargs):
    # 获取正股简称
    return w.wss(security,"underlyingname",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUnderlyingCodeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取正股代码时间序列
    return w.wsd(security,"underlyingcode",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUnderlyingCode(security:list,*args,**kwargs):
    # 获取正股代码
    return w.wss(security,"underlyingcode",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNavSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取单位净值时间序列
    return w.wsd(security,"nav",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNav(security:list,*args,**kwargs):
    # 获取单位净值
    return w.wss(security,"nav",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank801Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款余额_短期贷款时间序列
    return w.wsd(security,"stmnote_bank_801",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank801(security:list,*args,**kwargs):
    # 获取贷款余额_短期贷款
    return w.wss(security,"stmnote_bank_801",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssueExpenseSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取配股费用时间序列
    return w.wsd(security,"rightsissue_expense",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssueExpense(security:list,*args,**kwargs):
    # 获取配股费用
    return w.wss(security,"rightsissue_expense",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank802Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款余额_中长期贷款时间序列
    return w.wsd(security,"stmnote_bank_802",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank802(security:list,*args,**kwargs):
    # 获取贷款余额_中长期贷款
    return w.wss(security,"stmnote_bank_802",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNav2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取单位净值(不前推)时间序列
    return w.wsd(security,"nav2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNav2(security:list,*args,**kwargs):
    # 获取单位净值(不前推)
    return w.wss(security,"nav2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank65Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款余额(按行业)时间序列
    return w.wsd(security,"stmnote_bank_65",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank65(security:list,*args,**kwargs):
    # 获取贷款余额(按行业)
    return w.wss(security,"stmnote_bank_65",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNavUnitTransformSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取单位净值(支持转型基金)时间序列
    return w.wsd(security,"NAV_unit_transform",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNavUnitTransform(security:list,*args,**kwargs):
    # 获取单位净值(支持转型基金)
    return w.wss(security,"NAV_unit_transform",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseInterestCompensationInterestSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取补偿利率时间序列
    return w.wsd(security,"clause_interest_compensationinterest",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseInterestCompensationInterest(security:list,*args,**kwargs):
    # 获取补偿利率
    return w.wss(security,"clause_interest_compensationinterest",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStockClassSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取股票种类时间序列
    return w.wsd(security,"stockclass",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStockClass(security:list,*args,**kwargs):
    # 获取股票种类
    return w.wss(security,"stockclass",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoIssuingSystemSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行制度时间序列
    return w.wsd(security,"ipo_issuingsystem",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoIssuingSystem(security:list,*args,**kwargs):
    # 获取发行制度
    return w.wss(security,"ipo_issuingsystem",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseCompensationInterestSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取补偿利率(公布)时间序列
    return w.wsd(security,"clause_compensationinterest",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseCompensationInterest(security:list,*args,**kwargs):
    # 获取补偿利率(公布)
    return w.wss(security,"clause_compensationinterest",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDYOyEBTSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取利润总额(同比增长率)_GSD时间序列
    return w.wsd(security,"wgsd_yoyebt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDYOyEBT(security:list,*args,**kwargs):
    # 获取利润总额(同比增长率)_GSD
    return w.wss(security,"wgsd_yoyebt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAccountTreatmentSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取会计处理时间序列
    return w.wsd(security,"accounttreatment",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAccountTreatment(security:list,*args,**kwargs):
    # 获取会计处理
    return w.wss(security,"accounttreatment",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstWinningAmNtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取中标总量时间序列
    return w.wsd(security,"tendrst_winningamnt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstWinningAmNt(security:list,*args,**kwargs):
    # 获取中标总量
    return w.wss(security,"tendrst_winningamnt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCrmSubjectSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取标的实体时间序列
    return w.wsd(security,"crm_subject",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCrmSubject(security:list,*args,**kwargs):
    # 获取标的实体
    return w.wss(security,"crm_subject",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCrmRegisterAgencySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取登记机构时间序列
    return w.wsd(security,"crm_registeragency",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCrmRegisterAgency(security:list,*args,**kwargs):
    # 获取登记机构
    return w.wss(security,"crm_registeragency",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPaymentDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取年付息日时间序列
    return w.wsd(security,"paymentdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPaymentDate(security:list,*args,**kwargs):
    # 获取年付息日
    return w.wss(security,"paymentdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCrmCreditEventSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取信用事件时间序列
    return w.wsd(security,"crm_creditevent",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCrmCreditEvent(security:list,*args,**kwargs):
    # 获取信用事件
    return w.wss(security,"crm_creditevent",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRepoDaysSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取回购天数时间序列
    return w.wsd(security,"repo_days",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRepoDays(security:list,*args,**kwargs):
    # 获取回购天数
    return w.wss(security,"repo_days",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRepoTypeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取回购类型时间序列
    return w.wsd(security,"repo_type",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRepoType(security:list,*args,**kwargs):
    # 获取回购类型
    return w.wss(security,"repo_type",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareOtcRestrictedControllerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取限售股份(控股股东或实际控制人)时间序列
    return w.wsd(security,"share_otcrestricted_controller",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareOtcRestrictedController(security:list,*args,**kwargs):
    # 获取限售股份(控股股东或实际控制人)
    return w.wss(security,"share_otcrestricted_controller",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRepoUBondSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取标的债券时间序列
    return w.wsd(security,"repo_ubond",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRepoUBond(security:list,*args,**kwargs):
    # 获取标的债券
    return w.wss(security,"repo_ubond",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPreSettleSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取前结算价时间序列
    return w.wsd(security,"pre_settle",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPreSettle(security:list,*args,**kwargs):
    # 获取前结算价
    return w.wss(security,"pre_settle",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCrmIssuerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发布机构时间序列
    return w.wsd(security,"crm_issuer",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCrmIssuer(security:list,*args,**kwargs):
    # 获取发布机构
    return w.wss(security,"crm_issuer",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteDpsT4406Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取美元存款(折算人民币)时间序列
    return w.wsd(security,"stmnote_DPST_4406",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteDpsT4406(security:list,*args,**kwargs):
    # 获取美元存款(折算人民币)
    return w.wss(security,"stmnote_DPST_4406",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteDpsT4407Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取日元存款(折算人民币)时间序列
    return w.wsd(security,"stmnote_DPST_4407",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteDpsT4407(security:list,*args,**kwargs):
    # 获取日元存款(折算人民币)
    return w.wss(security,"stmnote_DPST_4407",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteDpsT4408Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取欧元存款(折算人民币)时间序列
    return w.wsd(security,"stmnote_DPST_4408",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteDpsT4408(security:list,*args,**kwargs):
    # 获取欧元存款(折算人民币)
    return w.wss(security,"stmnote_DPST_4408",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteDpsT4409Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取港币存款(折算人民币)时间序列
    return w.wsd(security,"stmnote_DPST_4409",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteDpsT4409(security:list,*args,**kwargs):
    # 获取港币存款(折算人民币)
    return w.wss(security,"stmnote_DPST_4409",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareRestrictedMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取限售股份(高管持股)时间序列
    return w.wsd(security,"share_restricted_m",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareRestrictedM(security:list,*args,**kwargs):
    # 获取限售股份(高管持股)
    return w.wss(security,"share_restricted_m",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteDpsT4410Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取英镑存款(折算人民币)时间序列
    return w.wsd(security,"stmnote_DPST_4410",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteDpsT4410(security:list,*args,**kwargs):
    # 获取英镑存款(折算人民币)
    return w.wss(security,"stmnote_DPST_4410",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTaxFreeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取是否免税时间序列
    return w.wsd(security,"taxfree",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTaxFree(security:list,*args,**kwargs):
    # 获取是否免税
    return w.wss(security,"taxfree",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteEoItems8Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取政府补助时间序列
    return w.wsd(security,"stmnote_Eoitems_8",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteEoItems8(security:list,*args,**kwargs):
    # 获取政府补助
    return w.wss(security,"stmnote_Eoitems_8",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOrTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业收入(TTM)_VAL_PIT时间序列
    return w.wsd(security,"or_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOrTtM(security:list,*args,**kwargs):
    # 获取营业收入(TTM)_VAL_PIT
    return w.wss(security,"or_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAssetMrQSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资产总计(MRQ,只有最新数据)时间序列
    return w.wsd(security,"asset_mrq",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAssetMrQ(security:list,*args,**kwargs):
    # 获取资产总计(MRQ,只有最新数据)
    return w.wss(security,"asset_mrq",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRepoCodeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取回购代码时间序列
    return w.wsd(security,"repo_code",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRepoCode(security:list,*args,**kwargs):
    # 获取回购代码
    return w.wss(security,"repo_code",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaToTAssetsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资产总计_PIT时间序列
    return w.wsd(security,"fa_totassets",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaToTAssets(security:list,*args,**kwargs):
    # 获取资产总计_PIT
    return w.wss(security,"fa_totassets",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFormSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取凭证类别时间序列
    return w.wsd(security,"form",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getForm(security:list,*args,**kwargs):
    # 获取凭证类别
    return w.wss(security,"form",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getActualBenchmarkSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取计息基准时间序列
    return w.wsd(security,"actualbenchmark",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getActualBenchmark(security:list,*args,**kwargs):
    # 获取计息基准
    return w.wss(security,"actualbenchmark",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOpTtM3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业利润(TTM)_GSD时间序列
    return w.wsd(security,"op_ttm3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOpTtM3(security:list,*args,**kwargs):
    # 获取营业利润(TTM)_GSD
    return w.wss(security,"op_ttm3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEmployeePhdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取博士人数时间序列
    return w.wsd(security,"employee_PHD",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEmployeePhd(security:list,*args,**kwargs):
    # 获取博士人数
    return w.wss(security,"employee_PHD",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOpTtM2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业利润(TTM)时间序列
    return w.wsd(security,"op_ttm2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOpTtM2(security:list,*args,**kwargs):
    # 获取营业利润(TTM)
    return w.wss(security,"op_ttm2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOtherGrantsIncSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他收益时间序列
    return w.wsd(security,"other_grants_inc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOtherGrantsInc(security:list,*args,**kwargs):
    # 获取其他收益
    return w.wss(security,"other_grants_inc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBondBalanceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取国债余额(做市后)时间序列
    return w.wsd(security,"tbondbalance",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBondBalance(security:list,*args,**kwargs):
    # 获取国债余额(做市后)
    return w.wss(security,"tbondbalance",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCarryDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取起息日期时间序列
    return w.wsd(security,"carrydate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCarryDate(security:list,*args,**kwargs):
    # 获取起息日期
    return w.wss(security,"carrydate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInceptionFundManagerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金经理(成立)时间序列
    return w.wsd(security,"fund_inceptionfundmanager",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInceptionFundManager(security:list,*args,**kwargs):
    # 获取基金经理(成立)
    return w.wss(security,"fund_inceptionfundmanager",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPRedFundManagerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金经理(历任)时间序列
    return w.wsd(security,"fund_predfundmanager",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPRedFundManager(security:list,*args,**kwargs):
    # 获取基金经理(历任)
    return w.wss(security,"fund_predfundmanager",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMaturityDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取到期日期时间序列
    return w.wsd(security,"maturitydate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMaturityDate(security:list,*args,**kwargs):
    # 获取到期日期
    return w.wss(security,"maturitydate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCouponSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取息票品种时间序列
    return w.wsd(security,"coupon",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCoupon(security:list,*args,**kwargs):
    # 获取息票品种
    return w.wss(security,"coupon",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundFundManagerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金经理(现任)时间序列
    return w.wsd(security,"fund_fundmanager",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundFundManager(security:list,*args,**kwargs):
    # 获取基金经理(现任)
    return w.wss(security,"fund_fundmanager",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTermSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取债券期限(年)时间序列
    return w.wsd(security,"term",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTerm(security:list,*args,**kwargs):
    # 获取债券期限(年)
    return w.wss(security,"term",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTerm2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取债券期限(文字)时间序列
    return w.wsd(security,"term2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTerm2(security:list,*args,**kwargs):
    # 获取债券期限(文字)
    return w.wss(security,"term2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInterestTypeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取利率类型时间序列
    return w.wsd(security,"interesttype",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInterestType(security:list,*args,**kwargs):
    # 获取利率类型
    return w.wss(security,"interesttype",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDDpsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股派息_GSD时间序列
    return w.wsd(security,"wgsd_dps",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDDps(security:list,*args,**kwargs):
    # 获取每股派息_GSD
    return w.wss(security,"wgsd_dps",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCouponRateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取票面利率(发行时)时间序列
    return w.wsd(security,"couponrate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCouponRate(security:list,*args,**kwargs):
    # 获取票面利率(发行时)
    return w.wss(security,"couponrate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCouponTxtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取利率说明时间序列
    return w.wsd(security,"coupontxt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCouponTxt(security:list,*args,**kwargs):
    # 获取利率说明
    return w.wss(security,"coupontxt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCrmStartingPriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取创设价格时间序列
    return w.wsd(security,"crm_startingprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCrmStartingPrice(security:list,*args,**kwargs):
    # 获取创设价格
    return w.wss(security,"crm_startingprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCrmPaymentTermsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取付费方式时间序列
    return w.wsd(security,"crm_paymentterms",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCrmPaymentTerms(security:list,*args,**kwargs):
    # 获取付费方式
    return w.wss(security,"crm_paymentterms",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPaymentTypeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取计息方式时间序列
    return w.wsd(security,"paymenttype",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPaymentType(security:list,*args,**kwargs):
    # 获取计息方式
    return w.wss(security,"paymenttype",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundFundManagerOfTradeDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金经理时间序列
    return w.wsd(security,"fund_fundmanageroftradedate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundFundManagerOfTradeDate(security:list,*args,**kwargs):
    # 获取基金经理
    return w.wss(security,"fund_fundmanageroftradedate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAdjFactorSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取复权因子时间序列
    return w.wsd(security,"adjfactor",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAdjFactor(security:list,*args,**kwargs):
    # 获取复权因子
    return w.wss(security,"adjfactor",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMktPriceTypeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取市价类型时间序列
    return w.wsd(security,"mktpricetype",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMktPriceType(security:list,*args,**kwargs):
    # 获取市价类型
    return w.wss(security,"mktpricetype",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOrTtM2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业收入(TTM)时间序列
    return w.wsd(security,"or_ttm2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOrTtM2(security:list,*args,**kwargs):
    # 获取营业收入(TTM)
    return w.wss(security,"or_ttm2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReinsuranceExpSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取分保费用时间序列
    return w.wsd(security,"reinsurance_exp",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReinsuranceExp(security:list,*args,**kwargs):
    # 获取分保费用
    return w.wss(security,"reinsurance_exp",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCbResultBalanceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取包销余额时间序列
    return w.wsd(security,"cb_result_balance",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCbResultBalance(security:list,*args,**kwargs):
    # 获取包销余额
    return w.wss(security,"cb_result_balance",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDirectionGoldSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取交收方向(黄金现货)时间序列
    return w.wsd(security,"direction_gold",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDirectionGold(security:list,*args,**kwargs):
    # 获取交收方向(黄金现货)
    return w.wss(security,"direction_gold",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFinaExpenseTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取财务费用(TTM,只有最新数据)时间序列
    return w.wsd(security,"finaexpense_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFinaExpenseTtM(security:list,*args,**kwargs):
    # 获取财务费用(TTM,只有最新数据)
    return w.wss(security,"finaexpense_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseCallOptionRedeemItemSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取赎回条款时间序列
    return w.wsd(security,"clause_calloption_redeemitem",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseCallOptionRedeemItem(security:list,*args,**kwargs):
    # 获取赎回条款
    return w.wss(security,"clause_calloption_redeemitem",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseConversion2ToSharePriceAdjustItemSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取转股条款时间序列
    return w.wsd(security,"clause_conversion2_tosharepriceadjustitem",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseConversion2ToSharePriceAdjustItem(security:list,*args,**kwargs):
    # 获取转股条款
    return w.wss(security,"clause_conversion2_tosharepriceadjustitem",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaFinaExpenseTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取财务费用(TTM)_PIT时间序列
    return w.wsd(security,"fa_finaexpense_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaFinaExpenseTtM(security:list,*args,**kwargs):
    # 获取财务费用(TTM)_PIT
    return w.wss(security,"fa_finaexpense_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFinExpCsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取财务费用_CS时间序列
    return w.wsd(security,"fin_exp_cs",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFinExpCs(security:list,*args,**kwargs):
    # 获取财务费用_CS
    return w.wss(security,"fin_exp_cs",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07IsReItsFinanceFeeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取财务费用时间序列
    return w.wsd(security,"stm07_is_reits_financefee",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07IsReItsFinanceFee(security:list,*args,**kwargs):
    # 获取财务费用
    return w.wss(security,"stm07_is_reits_financefee",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSUspReasonSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取停牌原因时间序列
    return w.wsd(security,"susp_reason",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSUspReason(security:list,*args,**kwargs):
    # 获取停牌原因
    return w.wss(security,"susp_reason",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFinaExpenseTtM3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取财务费用(TTM)_GSD时间序列
    return w.wsd(security,"finaexpense_ttm3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFinaExpenseTtM3(security:list,*args,**kwargs):
    # 获取财务费用(TTM)_GSD
    return w.wss(security,"finaexpense_ttm3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthTotalEquitySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取股东权益(N年,增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_totalequity",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthTotalEquity(security:list,*args,**kwargs):
    # 获取股东权益(N年,增长率)_GSD
    return w.wss(security,"wgsd_growth_totalequity",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthAssetsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资产总计(N年,增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_assets",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthAssets(security:list,*args,**kwargs):
    # 获取资产总计(N年,增长率)_GSD
    return w.wss(security,"wgsd_growth_assets",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFinaExpenseTtM2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取财务费用(TTM)时间序列
    return w.wsd(security,"finaexpense_ttm2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFinaExpenseTtM2(security:list,*args,**kwargs):
    # 获取财务费用(TTM)
    return w.wss(security,"finaexpense_ttm2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDPayTaxSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取应交税金_GSD时间序列
    return w.wsd(security,"wgsd_pay_tax",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDPayTax(security:list,*args,**kwargs):
    # 获取应交税金_GSD
    return w.wss(security,"wgsd_pay_tax",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthEBtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取利润总额(N年,增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_ebt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthEBt(security:list,*args,**kwargs):
    # 获取利润总额(N年,增长率)_GSD
    return w.wss(security,"wgsd_growth_ebt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthOpSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业利润(N年,增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_op",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthOp(security:list,*args,**kwargs):
    # 获取营业利润(N年,增长率)_GSD
    return w.wss(security,"wgsd_growth_op",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDDebtLtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取长期借贷_GSD时间序列
    return w.wsd(security,"wgsd_debt_lt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDDebtLt(security:list,*args,**kwargs):
    # 获取长期借贷_GSD
    return w.wss(security,"wgsd_debt_lt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteOthers7629Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取折旧摊销(管理费用)时间序列
    return w.wsd(security,"stmnote_others_7629",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteOthers7629(security:list,*args,**kwargs):
    # 获取折旧摊销(管理费用)
    return w.wss(security,"stmnote_others_7629",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDPayReInSurSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取应付再保_GSD时间序列
    return w.wsd(security,"wgsd_pay_reinsur",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDPayReInSur(security:list,*args,**kwargs):
    # 获取应付再保_GSD
    return w.wss(security,"wgsd_pay_reinsur",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderNumSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取股东户数时间序列
    return w.wsd(security,"holder_num",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderNum(security:list,*args,**kwargs):
    # 获取股东户数
    return w.wss(security,"holder_num",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs19Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取资产合计_FUND时间序列
    return w.wsd(security,"stm_bs_19",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs19(security:list,*args,**kwargs):
    # 获取资产合计_FUND
    return w.wss(security,"stm_bs_19",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRepaymentMethodSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取偿还方式时间序列
    return w.wsd(security,"repaymentmethod",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRepaymentMethod(security:list,*args,**kwargs):
    # 获取偿还方式
    return w.wss(security,"repaymentmethod",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareOtcRestrictedOthersSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取限售股份(其他)时间序列
    return w.wsd(security,"share_otcrestricted_others",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareOtcRestrictedOthers(security:list,*args,**kwargs):
    # 获取限售股份(其他)
    return w.wss(security,"share_otcrestricted_others",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07IsReItsSumProfitSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取利润总额时间序列
    return w.wsd(security,"stm07_is_reits_sumprofit",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07IsReItsSumProfit(security:list,*args,**kwargs):
    # 获取利润总额
    return w.wss(security,"stm07_is_reits_sumprofit",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTradeStatusSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取交易状态时间序列
    return w.wsd(security,"trade_status",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTradeStatus(security:list,*args,**kwargs):
    # 获取交易状态
    return w.wss(security,"trade_status",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEvSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总市值1时间序列
    return w.wsd(security,"ev",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEv(security:list,*args,**kwargs):
    # 获取总市值1
    return w.wss(security,"ev",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMktCapArdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总市值2时间序列
    return w.wsd(security,"mkt_cap_ard",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMktCapArd(security:list,*args,**kwargs):
    # 获取总市值2
    return w.wss(security,"mkt_cap_ard",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEv3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取总市值1(币种可选)时间序列
    return w.wsd(security,"ev3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEv3(security:list,*args,**kwargs):
    # 获取总市值1(币种可选)
    return w.wss(security,"ev3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsAllAssetsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资产总计时间序列
    return w.wsd(security,"stm07_bs_reits_allassets",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsAllAssets(security:list,*args,**kwargs):
    # 获取资产总计
    return w.wss(security,"stm07_bs_reits_allassets",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAssetsNettingSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资产差额(合计平衡项目)时间序列
    return w.wsd(security,"assets_netting",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAssetsNetting(security:list,*args,**kwargs):
    # 获取资产差额(合计平衡项目)
    return w.wss(security,"assets_netting",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCloSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取法律顾问时间序列
    return w.wsd(security,"clo",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClo(security:list,*args,**kwargs):
    # 获取法律顾问
    return w.wss(security,"clo",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAssetsGapSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资产差额(特殊报表科目)时间序列
    return w.wsd(security,"assets_gap",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAssetsGap(security:list,*args,**kwargs):
    # 获取资产差额(特殊报表科目)
    return w.wss(security,"assets_gap",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRedemptionFeeRationSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取兑付费率时间序列
    return w.wsd(security,"redemption_feeration",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRedemptionFeeRation(security:list,*args,**kwargs):
    # 获取兑付费率
    return w.wss(security,"redemption_feeration",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteImpairmentLoss4Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取坏账损失时间序列
    return w.wsd(security,"stmnote_ImpairmentLoss_4",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteImpairmentLoss4(security:list,*args,**kwargs):
    # 获取坏账损失
    return w.wss(security,"stmnote_ImpairmentLoss_4",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValMvCSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取流通市值时间序列
    return w.wsd(security,"val_mvc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValMvC(security:list,*args,**kwargs):
    # 获取流通市值
    return w.wss(security,"val_mvc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOrTtM3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业收入(TTM)_GSD时间序列
    return w.wsd(security,"or_ttm3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOrTtM3(security:list,*args,**kwargs):
    # 获取营业收入(TTM)_GSD
    return w.wss(security,"or_ttm3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07IsReItsIncomeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业收入时间序列
    return w.wsd(security,"stm07_is_reits_income",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07IsReItsIncome(security:list,*args,**kwargs):
    # 获取营业收入
    return w.wss(security,"stm07_is_reits_income",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaOrTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业收入(TTM)_PIT时间序列
    return w.wsd(security,"fa_or_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaOrTtM(security:list,*args,**kwargs):
    # 获取营业收入(TTM)_PIT
    return w.wss(security,"fa_or_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMktCapFloatSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取流通市值(含限售股)时间序列
    return w.wsd(security,"mkt_cap_float",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMktCapFloat(security:list,*args,**kwargs):
    # 获取流通市值(含限售股)
    return w.wss(security,"mkt_cap_float",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAuditorSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取审计机构时间序列
    return w.wsd(security,"auditor",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAuditor(security:list,*args,**kwargs):
    # 获取审计机构
    return w.wss(security,"auditor",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareOtcRestrictedBackboneSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取限售股份(核心员工)时间序列
    return w.wsd(security,"share_otcrestricted_backbone",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareOtcRestrictedBackbone(security:list,*args,**kwargs):
    # 获取限售股份(核心员工)
    return w.wss(security,"share_otcrestricted_backbone",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRecEivReInSurSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取应收再保_GSD时间序列
    return w.wsd(security,"wgsd_receiv_reinsur",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRecEivReInSur(security:list,*args,**kwargs):
    # 获取应收再保_GSD
    return w.wss(security,"wgsd_receiv_reinsur",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEmployeeMGmtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取高管人数时间序列
    return w.wsd(security,"employee_mgmt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEmployeeMGmt(security:list,*args,**kwargs):
    # 获取高管人数
    return w.wss(security,"employee_mgmt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAuditor2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取审计机构(支持历史)时间序列
    return w.wsd(security,"auditor2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAuditor2(security:list,*args,**kwargs):
    # 获取审计机构(支持历史)
    return w.wss(security,"auditor2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDAPicSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取股本溢价_GSD时间序列
    return w.wsd(security,"wgsd_apic",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDAPic(security:list,*args,**kwargs):
    # 获取股本溢价_GSD
    return w.wss(security,"wgsd_apic",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTangibleAssetSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取有形资产时间序列
    return w.wsd(security,"tangibleasset",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTangibleAsset(security:list,*args,**kwargs):
    # 获取有形资产
    return w.wss(security,"tangibleasset",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur7808Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取其它资产时间序列
    return w.wsd(security,"stmnote_insur_7808",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur7808(security:list,*args,**kwargs):
    # 获取其它资产
    return w.wss(security,"stmnote_insur_7808",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareIssuingMktSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取流通股本时间序列
    return w.wsd(security,"share_issuing_mkt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareIssuingMkt(security:list,*args,**kwargs):
    # 获取流通股本
    return w.wss(security,"share_issuing_mkt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareRTdFrgNNpSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取限售股份(境外自然人持股)时间序列
    return w.wsd(security,"share_rtd_frgnnp",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareRTdFrgNNp(security:list,*args,**kwargs):
    # 获取限售股份(境外自然人持股)
    return w.wss(security,"share_rtd_frgnnp",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSharePledgedAPctSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取质押比例时间序列
    return w.wsd(security,"share_pledgeda_pct",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSharePledgedAPct(security:list,*args,**kwargs):
    # 获取质押比例
    return w.wss(security,"share_pledgeda_pct",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOptionsTradeCodeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取期权代码(指定行权价)时间序列
    return w.wsd(security,"options_tradecode",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOptionsTradeCode(security:list,*args,**kwargs):
    # 获取期权代码(指定行权价)
    return w.wss(security,"options_tradecode",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs19Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取审计费用_FUND时间序列
    return w.wsd(security,"stm_is_19",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs19(security:list,*args,**kwargs):
    # 获取审计费用_FUND
    return w.wss(security,"stm_is_19",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs73Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取交易费用_FUND时间序列
    return w.wsd(security,"stm_is_73",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs73(security:list,*args,**kwargs):
    # 获取交易费用_FUND
    return w.wss(security,"stm_is_73",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs22Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取费用合计_FUND时间序列
    return w.wsd(security,"stm_is_22",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs22(security:list,*args,**kwargs):
    # 获取费用合计_FUND
    return w.wss(security,"stm_is_22",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs77Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取汇兑收入_FUND时间序列
    return w.wsd(security,"stm_is_77",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs77(security:list,*args,**kwargs):
    # 获取汇兑收入_FUND
    return w.wss(security,"stm_is_77",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs4Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取股利收益_FUND时间序列
    return w.wsd(security,"stm_is_4",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs4(security:list,*args,**kwargs):
    # 获取股利收益_FUND
    return w.wss(security,"stm_is_4",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareRTdStateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取限售股份(国家持股)时间序列
    return w.wsd(security,"share_rtd_state",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareRTdState(security:list,*args,**kwargs):
    # 获取限售股份(国家持股)
    return w.wss(security,"share_rtd_state",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs33Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取负债合计_FUND时间序列
    return w.wsd(security,"stm_bs_33",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs33(security:list,*args,**kwargs):
    # 获取负债合计_FUND
    return w.wss(security,"stm_bs_33",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaOpTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业利润(TTM)_PIT时间序列
    return w.wsd(security,"fa_op_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaOpTtM(security:list,*args,**kwargs):
    # 获取营业利润(TTM)_PIT
    return w.wss(security,"fa_op_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getExeRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取合约乘数时间序列
    return w.wsd(security,"exe_ratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getExeRatio(security:list,*args,**kwargs):
    # 获取合约乘数
    return w.wss(security,"exe_ratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaToTliAbSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取负债合计_PIT时间序列
    return w.wsd(security,"fa_totliab",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaToTliAb(security:list,*args,**kwargs):
    # 获取负债合计_PIT
    return w.wss(security,"fa_totliab",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDebtMrQSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取负债合计(MRQ,只有最新数据)时间序列
    return w.wsd(security,"debt_mrq",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDebtMrQ(security:list,*args,**kwargs):
    # 获取负债合计(MRQ,只有最新数据)
    return w.wss(security,"debt_mrq",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs10Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取收入合计_FUND时间序列
    return w.wsd(security,"stm_is_10",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs10(security:list,*args,**kwargs):
    # 获取收入合计_FUND
    return w.wss(security,"stm_is_10",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs34Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取实收基金_FUND时间序列
    return w.wsd(security,"stm_bs_34",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs34(security:list,*args,**kwargs):
    # 获取实收基金_FUND
    return w.wss(security,"stm_bs_34",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPunItSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取报价单位时间序列
    return w.wsd(security,"punit",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPunIt(security:list,*args,**kwargs):
    # 获取报价单位
    return w.wss(security,"punit",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs30Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取应付收益_FUND时间序列
    return w.wsd(security,"stm_bs_30",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs30(security:list,*args,**kwargs):
    # 获取应付收益_FUND
    return w.wss(security,"stm_bs_30",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs127Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取未交税金_FUND时间序列
    return w.wsd(security,"stm_bs_127",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs127(security:list,*args,**kwargs):
    # 获取未交税金_FUND
    return w.wss(security,"stm_bs_127",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOpTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业利润(TTM,只有最新数据)时间序列
    return w.wsd(security,"op_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOpTtM(security:list,*args,**kwargs):
    # 获取营业利润(TTM,只有最新数据)
    return w.wss(security,"op_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareNonTradable2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取非流通股时间序列
    return w.wsd(security,"share_nontradable2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareNonTradable2(security:list,*args,**kwargs):
    # 获取非流通股
    return w.wss(security,"share_nontradable2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUsCodeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取标的代码时间序列
    return w.wsd(security,"us_code",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUsCode(security:list,*args,**kwargs):
    # 获取标的代码
    return w.wss(security,"us_code",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsAllDebtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取负债合计时间序列
    return w.wsd(security,"stm07_bs_reits_alldebt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsAllDebt(security:list,*args,**kwargs):
    # 获取负债合计
    return w.wss(security,"stm07_bs_reits_alldebt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEBtTtM3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取利润总额(TTM)_GSD时间序列
    return w.wsd(security,"ebt_ttm3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEBtTtM3(security:list,*args,**kwargs):
    # 获取利润总额(TTM)_GSD
    return w.wss(security,"ebt_ttm3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEBtTtM2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取利润总额(TTM)时间序列
    return w.wsd(security,"ebt_ttm2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEBtTtM2(security:list,*args,**kwargs):
    # 获取利润总额(TTM)
    return w.wss(security,"ebt_ttm2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaEBtTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取利润总额(TTM)_PIT时间序列
    return w.wsd(security,"fa_ebt_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaEBtTtM(security:list,*args,**kwargs):
    # 获取利润总额(TTM)_PIT
    return w.wss(security,"fa_ebt_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEBtTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取利润总额(TTM,只有最新数据)时间序列
    return w.wsd(security,"ebt_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEBtTtM(security:list,*args,**kwargs):
    # 获取利润总额(TTM,只有最新数据)
    return w.wss(security,"ebt_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareRTdDomeSnpSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取限售股份(境内自然人持股)时间序列
    return w.wsd(security,"share_rtd_domesnp",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareRTdDomeSnp(security:list,*args,**kwargs):
    # 获取限售股份(境内自然人持股)
    return w.wss(security,"share_rtd_domesnp",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareRTdSubFrgNSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取限售股份(外资持股合计)时间序列
    return w.wsd(security,"share_rtd_subfrgn",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareRTdSubFrgN(security:list,*args,**kwargs):
    # 获取限售股份(外资持股合计)
    return w.wss(security,"share_rtd_subfrgn",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPreCloseSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取前收盘价时间序列
    return w.wsd(security,"pre_close",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPreClose(security:list,*args,**kwargs):
    # 获取前收盘价
    return w.wss(security,"pre_close",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSettlementMethodSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取交割方式时间序列
    return w.wsd(security,"settlementmethod",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSettlementMethod(security:list,*args,**kwargs):
    # 获取交割方式
    return w.wss(security,"settlementmethod",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteOthers4504Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取政府补助_营业外收入时间序列
    return w.wsd(security,"stmnote_others_4504",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteOthers4504(security:list,*args,**kwargs):
    # 获取政府补助_营业外收入
    return w.wss(security,"stmnote_others_4504",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUsNameSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取标的简称时间序列
    return w.wsd(security,"us_name",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUsName(security:list,*args,**kwargs):
    # 获取标的简称
    return w.wss(security,"us_name",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLiaBGapSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取负债差额(特殊报表科目)时间序列
    return w.wsd(security,"liab_gap",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLiaBGap(security:list,*args,**kwargs):
    # 获取负债差额(特殊报表科目)
    return w.wss(security,"liab_gap",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareRTdFrgNJurSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取限售股份(境外法人持股)时间序列
    return w.wsd(security,"share_rtd_frgnjur",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareRTdFrgNJur(security:list,*args,**kwargs):
    # 获取限售股份(境外法人持股)
    return w.wss(security,"share_rtd_frgnjur",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLiaBNettingSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取负债差额(合计平衡项目)时间序列
    return w.wsd(security,"liab_netting",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLiaBNetting(security:list,*args,**kwargs):
    # 获取负债差额(合计平衡项目)
    return w.wss(security,"liab_netting",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getExePriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取行权价格时间序列
    return w.wsd(security,"exe_price",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getExePrice(security:list,*args,**kwargs):
    # 获取行权价格
    return w.wss(security,"exe_price",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getExeTypeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取行权类型时间序列
    return w.wsd(security,"exe_type",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getExeType(security:list,*args,**kwargs):
    # 获取行权类型
    return w.wss(security,"exe_type",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getExeModeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取行权方式时间序列
    return w.wsd(security,"exe_mode",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getExeMode(security:list,*args,**kwargs):
    # 获取行权方式
    return w.wss(security,"exe_mode",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareRTdInStSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取限售股份(机构配售股份)时间序列
    return w.wsd(security,"share_rtd_inst",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareRTdInSt(security:list,*args,**kwargs):
    # 获取限售股份(机构配售股份)
    return w.wss(security,"share_rtd_inst",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareRTdDomesJurSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取限售股份(境内法人持股)时间序列
    return w.wsd(security,"share_rtd_domesjur",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareRTdDomesJur(security:list,*args,**kwargs):
    # 获取限售股份(境内法人持股)
    return w.wss(security,"share_rtd_domesjur",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareRTdSubOtherDomesSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取限售股份(其他内资持股合计)时间序列
    return w.wsd(security,"share_rtd_subotherdomes",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareRTdSubOtherDomes(security:list,*args,**kwargs):
    # 获取限售股份(其他内资持股合计)
    return w.wss(security,"share_rtd_subotherdomes",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareRTdStateJurSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取限售股份(国有法人持股)时间序列
    return w.wsd(security,"share_rtd_statejur",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareRTdStateJur(security:list,*args,**kwargs):
    # 获取限售股份(国有法人持股)
    return w.wss(security,"share_rtd_statejur",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTotalTmSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总存续期时间序列
    return w.wsd(security,"totaltm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTotalTm(security:list,*args,**kwargs):
    # 获取总存续期
    return w.wss(security,"totaltm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank351Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取生息资产时间序列
    return w.wsd(security,"stmnote_bank_351",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank351(security:list,*args,**kwargs):
    # 获取生息资产
    return w.wss(security,"stmnote_bank_351",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank381Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取计息负债时间序列
    return w.wsd(security,"stmnote_bank_381",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank381(security:list,*args,**kwargs):
    # 获取计息负债
    return w.wss(security,"stmnote_bank_381",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSec1853Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取权益乘数(剔除客户交易保证金)时间序列
    return w.wsd(security,"stmnote_sec_1853",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSec1853(security:list,*args,**kwargs):
    # 获取权益乘数(剔除客户交易保证金)
    return w.wss(security,"stmnote_sec_1853",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07IsReItsProfitSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业利润时间序列
    return w.wsd(security,"stm07_is_reits_profit",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07IsReItsProfit(security:list,*args,**kwargs):
    # 获取营业利润
    return w.wss(security,"stm07_is_reits_profit",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIntangAssetsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取无形资产时间序列
    return w.wsd(security,"intang_assets",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIntangAssets(security:list,*args,**kwargs):
    # 获取无形资产
    return w.wss(security,"intang_assets",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOilAndNaturalGasAssetsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取油气资产时间序列
    return w.wsd(security,"oil_and_natural_gas_assets",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOilAndNaturalGasAssets(security:list,*args,**kwargs):
    # 获取油气资产
    return w.wss(security,"oil_and_natural_gas_assets",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTrancheRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取各级占比时间序列
    return w.wsd(security,"trancheratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTrancheRatio(security:list,*args,**kwargs):
    # 获取各级占比
    return w.wss(security,"trancheratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDEbItOperSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业利润_GSD时间序列
    return w.wsd(security,"wgsd_ebit_oper",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDEbItOper(security:list,*args,**kwargs):
    # 获取营业利润_GSD
    return w.wss(security,"wgsd_ebit_oper",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFixAssetsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取固定资产时间序列
    return w.wsd(security,"fix_assets",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFixAssets(security:list,*args,**kwargs):
    # 获取固定资产
    return w.wss(security,"fix_assets",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFixAssetsToTSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取固定资产(合计)时间序列
    return w.wsd(security,"fix_assets_tot",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFixAssetsToT(security:list,*args,**kwargs):
    # 获取固定资产(合计)
    return w.wss(security,"fix_assets_tot",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEmployeeCollSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取专科人数时间序列
    return w.wsd(security,"employee_coll",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEmployeeColl(security:list,*args,**kwargs):
    # 获取专科人数
    return w.wss(security,"employee_coll",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSwingPerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间振幅时间序列
    return w.wsd(security,"swing_per",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSwingPer(security:list,*args,**kwargs):
    # 获取区间振幅
    return w.wss(security,"swing_per",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInvToTSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取存货合计时间序列
    return w.wsd(security,"stmnote_invtot",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInvToT(security:list,*args,**kwargs):
    # 获取存货合计
    return w.wss(security,"stmnote_invtot",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSwingNdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取N日振幅时间序列
    return w.wsd(security,"swing_nd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSwingNd(security:list,*args,**kwargs):
    # 获取N日振幅
    return w.wss(security,"swing_nd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOutstandingBalanceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取债券余额时间序列
    return w.wsd(security,"outstandingbalance",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOutstandingBalance(security:list,*args,**kwargs):
    # 获取债券余额
    return w.wss(security,"outstandingbalance",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEmployeeBaSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取本科人数时间序列
    return w.wsd(security,"employee_BA",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEmployeeBa(security:list,*args,**kwargs):
    # 获取本科人数
    return w.wss(security,"employee_BA",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUsAvgPriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取标的均价时间序列
    return w.wsd(security,"us_avgprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUsAvgPrice(security:list,*args,**kwargs):
    # 获取标的均价
    return w.wss(security,"us_avgprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerIndexWeightBetaSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取Beta(基金经理指数,规模加权)时间序列
    return w.wsd(security,"fund_managerindex_weight_beta",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerIndexWeightBeta(security:list,*args,**kwargs):
    # 获取Beta(基金经理指数,规模加权)
    return w.wss(security,"fund_managerindex_weight_beta",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerIndexBetaSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取Beta(基金经理指数,算术平均)时间序列
    return w.wsd(security,"fund_managerindex_beta",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerIndexBeta(security:list,*args,**kwargs):
    # 获取Beta(基金经理指数,算术平均)
    return w.wss(security,"fund_managerindex_beta",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getContAssetsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取合同资产时间序列
    return w.wsd(security,"cont_assets",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getContAssets(security:list,*args,**kwargs):
    # 获取合同资产
    return w.wss(security,"cont_assets",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEmployeeMsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取硕士人数时间序列
    return w.wsd(security,"employee_MS",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEmployeeMs(security:list,*args,**kwargs):
    # 获取硕士人数
    return w.wss(security,"employee_MS",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDTangibleAsset2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取有形资产_GSD时间序列
    return w.wsd(security,"wgsd_tangibleasset2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDTangibleAsset2(security:list,*args,**kwargs):
    # 获取有形资产_GSD
    return w.wss(security,"wgsd_tangibleasset2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getQStmNoteInSur212512Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取认可资产时间序列
    return w.wsd(security,"qstmnote_insur_212512",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getQStmNoteInSur212512(security:list,*args,**kwargs):
    # 获取认可资产
    return w.wss(security,"qstmnote_insur_212512",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUsSwingSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取标的振幅时间序列
    return w.wsd(security,"us_swing",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUsSwing(security:list,*args,**kwargs):
    # 获取标的振幅
    return w.wss(security,"us_swing",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaNoneInterestDebtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取无息负债时间序列
    return w.wsd(security,"fa_noneinterestdebt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaNoneInterestDebt(security:list,*args,**kwargs):
    # 获取无息负债
    return w.wss(security,"fa_noneinterestdebt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs32Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他负债_FUND时间序列
    return w.wsd(security,"stm_bs_32",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs32(security:list,*args,**kwargs):
    # 获取其他负债_FUND
    return w.wss(security,"stm_bs_32",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWindTypeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取指数分类(Wind)时间序列
    return w.wsd(security,"windtype",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWindType(security:list,*args,**kwargs):
    # 获取指数分类(Wind)
    return w.wss(security,"windtype",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getQStmNoteInSur212513Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取认可负债时间序列
    return w.wsd(security,"qstmnote_insur_212513",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getQStmNoteInSur212513(security:list,*args,**kwargs):
    # 获取认可负债
    return w.wss(security,"qstmnote_insur_212513",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getScCodeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取交易品种时间序列
    return w.wsd(security,"sccode",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getScCode(security:list,*args,**kwargs):
    # 获取交易品种
    return w.wss(security,"sccode",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDLiAbsContractSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取合同负债_GSD时间序列
    return w.wsd(security,"wgsd_liabs_contract",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDLiAbsContract(security:list,*args,**kwargs):
    # 获取合同负债_GSD
    return w.wss(security,"wgsd_liabs_contract",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDLiAbsOThSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他负债_GSD时间序列
    return w.wsd(security,"wgsd_liabs_oth",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDLiAbsOTh(security:list,*args,**kwargs):
    # 获取其他负债_GSD
    return w.wss(security,"wgsd_liabs_oth",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareTotalOtcSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取三板合计时间序列
    return w.wsd(security,"share_totalotc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareTotalOtc(security:list,*args,**kwargs):
    # 获取三板合计
    return w.wss(security,"share_totalotc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDlMonthSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取交割月份时间序列
    return w.wsd(security,"dlmonth",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDlMonth(security:list,*args,**kwargs):
    # 获取交割月份
    return w.wss(security,"dlmonth",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDealNumSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取成交笔数时间序列
    return w.wsd(security,"dealnum",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDealNum(security:list,*args,**kwargs):
    # 获取成交笔数
    return w.wss(security,"dealnum",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFullNameSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取证券全称时间序列
    return w.wsd(security,"fullname",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFullName(security:list,*args,**kwargs):
    # 获取证券全称
    return w.wss(security,"fullname",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getChgPerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间涨跌时间序列
    return w.wsd(security,"chg_per",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getChgPer(security:list,*args,**kwargs):
    # 获取区间涨跌
    return w.wss(security,"chg_per",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaTangibleAssetSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取有形资产_PIT时间序列
    return w.wsd(security,"fa_tangibleasset",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaTangibleAsset(security:list,*args,**kwargs):
    # 获取有形资产_PIT
    return w.wss(security,"fa_tangibleasset",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getContLiaBSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取合同负债时间序列
    return w.wsd(security,"cont_liab",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getContLiaB(security:list,*args,**kwargs):
    # 获取合同负债
    return w.wss(security,"cont_liab",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUsChangeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取标的涨跌时间序列
    return w.wsd(security,"us_change",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUsChange(security:list,*args,**kwargs):
    # 获取标的涨跌
    return w.wss(security,"us_change",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCbResultRationCodeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取定金比例时间序列
    return w.wsd(security,"cb_result_rationcode",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCbResultRationCode(security:list,*args,**kwargs):
    # 获取定金比例
    return w.wss(security,"cb_result_rationcode",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteProfitApr8Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取转增股本时间序列
    return w.wsd(security,"stmnote_profitapr_8",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteProfitApr8(security:list,*args,**kwargs):
    # 获取转增股本
    return w.wss(security,"stmnote_profitapr_8",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssuerUpdatedSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取债务主体时间序列
    return w.wsd(security,"issuerupdated",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssuerUpdated(security:list,*args,**kwargs):
    # 获取债务主体
    return w.wss(security,"issuerupdated",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLeaseObligationSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取租赁负债时间序列
    return w.wsd(security,"lease_obligation",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLeaseObligation(security:list,*args,**kwargs):
    # 获取租赁负债
    return w.wss(security,"lease_obligation",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getProvisionsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取预计负债时间序列
    return w.wsd(security,"provisions",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getProvisions(security:list,*args,**kwargs):
    # 获取预计负债
    return w.wss(security,"provisions",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOThLiaBSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他负债时间序列
    return w.wsd(security,"oth_liab",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOThLiaB(security:list,*args,**kwargs):
    # 获取其他负债
    return w.wss(security,"oth_liab",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteAuditAgencySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取审计单位时间序列
    return w.wsd(security,"stmnote_audit_agency",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteAuditAgency(security:list,*args,**kwargs):
    # 获取审计单位
    return w.wss(security,"stmnote_audit_agency",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueAmountSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行总额时间序列
    return w.wsd(security,"issueamount",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueAmount(security:list,*args,**kwargs):
    # 获取发行总额
    return w.wss(security,"issueamount",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFsPqChangeSettlementSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间涨跌(结算价)时间序列
    return w.wsd(security,"fs_pq_change_settlement",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFsPqChangeSettlement(security:list,*args,**kwargs):
    # 获取区间涨跌(结算价)
    return w.wss(security,"fs_pq_change_settlement",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteOthers7627Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取工资薪酬(管理费用)时间序列
    return w.wsd(security,"stmnote_others_7627",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteOthers7627(security:list,*args,**kwargs):
    # 获取工资薪酬(管理费用)
    return w.wss(security,"stmnote_others_7627",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLiCSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取经办律师时间序列
    return w.wsd(security,"lic",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLiC(security:list,*args,**kwargs):
    # 获取经办律师
    return w.wss(security,"lic",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAdminExpenseTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取管理费用(TTM,只有最新数据)时间序列
    return w.wsd(security,"adminexpense_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAdminExpenseTtM(security:list,*args,**kwargs):
    # 获取管理费用(TTM,只有最新数据)
    return w.wss(security,"adminexpense_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSUcSupervisorSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取公司监事(历任)时间序列
    return w.wsd(security,"sucsupervisor",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSUcSupervisor(security:list,*args,**kwargs):
    # 获取公司监事(历任)
    return w.wss(security,"sucsupervisor",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdNetBuyAmtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净买入额时间序列
    return w.wsd(security,"mfd_netbuyamt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdNetBuyAmt(security:list,*args,**kwargs):
    # 获取净买入额
    return w.wss(security,"mfd_netbuyamt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDStKPUrchCfSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取股本增加_GSD时间序列
    return w.wsd(security,"wgsd_stk_purch_cf",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDStKPUrchCf(security:list,*args,**kwargs):
    # 获取股本增加_GSD
    return w.wss(security,"wgsd_stk_purch_cf",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSupervisorSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取公司监事时间序列
    return w.wsd(security,"supervisor",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSupervisor(security:list,*args,**kwargs):
    # 获取公司监事
    return w.wss(security,"supervisor",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDStKSaleCfSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取股本减少_GSD时间序列
    return w.wsd(security,"wgsd_stk_sale_cf",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDStKSaleCf(security:list,*args,**kwargs):
    # 获取股本减少_GSD
    return w.wss(security,"wgsd_stk_sale_cf",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdNetBuyVolSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净买入量时间序列
    return w.wsd(security,"mfd_netbuyvol",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdNetBuyVol(security:list,*args,**kwargs):
    # 获取净买入量
    return w.wss(security,"mfd_netbuyvol",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSUcDirectorSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取公司董事(历任)时间序列
    return w.wsd(security,"sucdirector",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSUcDirector(security:list,*args,**kwargs):
    # 获取公司董事(历任)
    return w.wss(security,"sucdirector",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdBuyOrDSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取流入单数时间序列
    return w.wsd(security,"mfd_buyord",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdBuyOrD(security:list,*args,**kwargs):
    # 获取流入单数
    return w.wss(security,"mfd_buyord",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdSelLordSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取流出单数时间序列
    return w.wsd(security,"mfd_sellord",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdSelLord(security:list,*args,**kwargs):
    # 获取流出单数
    return w.wss(security,"mfd_sellord",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDirectorSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取公司董事时间序列
    return w.wsd(security,"director",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDirector(security:list,*args,**kwargs):
    # 获取公司董事
    return w.wss(security,"director",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteOthers7626Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取工资薪酬(销售费用)时间序列
    return w.wsd(security,"stmnote_others_7626",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteOthers7626(security:list,*args,**kwargs):
    # 获取工资薪酬(销售费用)
    return w.wss(security,"stmnote_others_7626",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs81Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取投资收益_FUND时间序列
    return w.wsd(security,"stm_is_81",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs81(security:list,*args,**kwargs):
    # 获取投资收益_FUND
    return w.wss(security,"stm_is_81",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCommissionTotalSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取交易佣金(合计值)时间序列
    return w.wsd(security,"commission_total",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCommissionTotal(security:list,*args,**kwargs):
    # 获取交易佣金(合计值)
    return w.wss(security,"commission_total",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOperateExpenseTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售费用(TTM,只有最新数据)时间序列
    return w.wsd(security,"operateexpense_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOperateExpenseTtM(security:list,*args,**kwargs):
    # 获取销售费用(TTM,只有最新数据)
    return w.wss(security,"operateexpense_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaSellExpenseTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售费用(TTM)_PIT时间序列
    return w.wsd(security,"fa_sellexpense_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaSellExpenseTtM(security:list,*args,**kwargs):
    # 获取销售费用(TTM)_PIT
    return w.wss(security,"fa_sellexpense_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDDebtReDuctCfSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取债务减少_GSD时间序列
    return w.wsd(security,"wgsd_debt_reduct_cf",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDDebtReDuctCf(security:list,*args,**kwargs):
    # 获取债务减少_GSD
    return w.wss(security,"wgsd_debt_reduct_cf",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAdminExpenseTtM2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取管理费用(TTM)时间序列
    return w.wsd(security,"adminexpense_ttm2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAdminExpenseTtM2(security:list,*args,**kwargs):
    # 获取管理费用(TTM)
    return w.wss(security,"adminexpense_ttm2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getExecutivesSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取公司高管时间序列
    return w.wsd(security,"executives",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getExecutives(security:list,*args,**kwargs):
    # 获取公司高管
    return w.wss(security,"executives",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAdminExpenseTtM3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取管理费用(TTM)_GSD时间序列
    return w.wsd(security,"adminexpense_ttm3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAdminExpenseTtM3(security:list,*args,**kwargs):
    # 获取管理费用(TTM)_GSD
    return w.wss(security,"adminexpense_ttm3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGMdc01005Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取编制依据时间序列
    return w.wsd(security,"esg_mdc01005",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGMdc01005(security:list,*args,**kwargs):
    # 获取编制依据
    return w.wss(security,"esg_mdc01005",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaAdminExpenseTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取管理费用(TTM)_PIT时间序列
    return w.wsd(security,"fa_adminexpense_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaAdminExpenseTtM(security:list,*args,**kwargs):
    # 获取管理费用(TTM)_PIT
    return w.wss(security,"fa_adminexpense_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMrgShortBalSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取融券余额时间序列
    return w.wsd(security,"mrg_short_bal",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMrgShortBal(security:list,*args,**kwargs):
    # 获取融券余额
    return w.wss(security,"mrg_short_bal",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSUcExecutivesSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取公司高管(历任)时间序列
    return w.wsd(security,"sucexecutives",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSUcExecutives(security:list,*args,**kwargs):
    # 获取公司高管(历任)
    return w.wss(security,"sucexecutives",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDSalaryPpSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取人均薪酬时间序列
    return w.wsd(security,"wgsd_salarypp",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDSalaryPp(security:list,*args,**kwargs):
    # 获取人均薪酬
    return w.wss(security,"wgsd_salarypp",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDProfitPpSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取人均创利时间序列
    return w.wsd(security,"wgsd_profitpp",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDProfitPp(security:list,*args,**kwargs):
    # 获取人均创利
    return w.wss(security,"wgsd_profitpp",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRevenuePpSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取人均创收时间序列
    return w.wsd(security,"wgsd_revenuepp",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRevenuePp(security:list,*args,**kwargs):
    # 获取人均创收
    return w.wss(security,"wgsd_revenuepp",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCommissionDetailedSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取交易佣金(分券商明细)时间序列
    return w.wsd(security,"commission_detailed",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCommissionDetailed(security:list,*args,**kwargs):
    # 获取交易佣金(分券商明细)
    return w.wss(security,"commission_detailed",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfNetInFlowSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净流入额时间序列
    return w.wsd(security,"mf_netinflow",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfNetInFlow(security:list,*args,**kwargs):
    # 获取净流入额
    return w.wss(security,"mf_netinflow",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDInvestPUrchCfSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取投资增加_GSD时间序列
    return w.wsd(security,"wgsd_invest_purch_cf",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDInvestPUrchCf(security:list,*args,**kwargs):
    # 获取投资增加_GSD
    return w.wss(security,"wgsd_invest_purch_cf",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDMgTExpSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取管理费用_GSD时间序列
    return w.wsd(security,"wgsd_mgt_exp",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDMgTExp(security:list,*args,**kwargs):
    # 获取管理费用_GSD
    return w.wss(security,"wgsd_mgt_exp",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDInvestSaleCfSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取投资减少_GSD时间序列
    return w.wsd(security,"wgsd_invest_sale_cf",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDInvestSaleCf(security:list,*args,**kwargs):
    # 获取投资减少_GSD
    return w.wss(security,"wgsd_invest_sale_cf",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDDebtIsSCfSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取债务增加_GSD时间序列
    return w.wsd(security,"wgsd_debt_iss_cf",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDDebtIsSCf(security:list,*args,**kwargs):
    # 获取债务增加_GSD
    return w.wss(security,"wgsd_debt_iss_cf",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetAssetTotalSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金规模(合计)时间序列
    return w.wsd(security,"netasset_total",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetAssetTotal(security:list,*args,**kwargs):
    # 获取基金规模(合计)
    return w.wss(security,"netasset_total",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundFundScaleSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金规模时间序列
    return w.wsd(security,"fund_fundscale",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundFundScale(security:list,*args,**kwargs):
    # 获取基金规模
    return w.wss(security,"fund_fundscale",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInSurPremUnearnedSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取已赚保费时间序列
    return w.wsd(security,"insur_prem_unearned",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInSurPremUnearned(security:list,*args,**kwargs):
    # 获取已赚保费
    return w.wss(security,"insur_prem_unearned",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07IsReItsManageFeeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取管理费用时间序列
    return w.wsd(security,"stm07_is_reits_managefee",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07IsReItsManageFee(security:list,*args,**kwargs):
    # 获取管理费用
    return w.wss(security,"stm07_is_reits_managefee",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMrgShortVolBalSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取融券余量时间序列
    return w.wsd(security,"mrg_short_vol_bal",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMrgShortVolBal(security:list,*args,**kwargs):
    # 获取融券余量
    return w.wss(security,"mrg_short_vol_bal",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDPremiumReInsurersSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取分出保费_GSD时间序列
    return w.wsd(security,"wgsd_premium_reinsurers",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDPremiumReInsurers(security:list,*args,**kwargs):
    # 获取分出保费_GSD
    return w.wss(security,"wgsd_premium_reinsurers",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDPaymentUnearnedSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取预收款项_GSD时间序列
    return w.wsd(security,"wgsd_payment_unearned",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDPaymentUnearned(security:list,*args,**kwargs):
    # 获取预收款项_GSD
    return w.wss(security,"wgsd_payment_unearned",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisPreSettleSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取前结算价_期货历史同月时间序列
    return w.wsd(security,"His_preSettle",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisPreSettle(security:list,*args,**kwargs):
    # 获取前结算价_期货历史同月
    return w.wss(security,"His_preSettle",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivCashAfterTax2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股股利(税后)(已宣告)时间序列
    return w.wsd(security,"div_cashaftertax2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivCashAfterTax2(security:list,*args,**kwargs):
    # 获取每股股利(税后)(已宣告)
    return w.wss(security,"div_cashaftertax2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInStYyBondValSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取债券估值(YY)时间序列
    return w.wsd(security,"inst_yybondval",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInStYyBondVal(security:list,*args,**kwargs):
    # 获取债券估值(YY)
    return w.wss(security,"inst_yybondval",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivStock2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股红股(已宣告)时间序列
    return w.wsd(security,"div_stock2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivStock2(security:list,*args,**kwargs):
    # 获取每股红股(已宣告)
    return w.wss(security,"div_stock2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaInterestExpenseTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取利息支出(TTM)_PIT时间序列
    return w.wsd(security,"fa_interestexpense_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaInterestExpenseTtM(security:list,*args,**kwargs):
    # 获取利息支出(TTM)_PIT
    return w.wss(security,"fa_interestexpense_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivStockSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股红股时间序列
    return w.wsd(security,"div_stock",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivStock(security:list,*args,**kwargs):
    # 获取每股红股
    return w.wss(security,"div_stock",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs72Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取利息支出_FUND时间序列
    return w.wsd(security,"stm_is_72",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs72(security:list,*args,**kwargs):
    # 获取利息支出_FUND
    return w.wss(security,"stm_is_72",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivCashAfterTaxSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股股利(税后)时间序列
    return w.wsd(security,"div_cashaftertax",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivCashAfterTax(security:list,*args,**kwargs):
    # 获取每股股利(税后)
    return w.wss(security,"div_cashaftertax",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivCashBeforeTaxSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股股利(税前)时间序列
    return w.wsd(security,"div_cashbeforetax",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivCashBeforeTax(security:list,*args,**kwargs):
    # 获取每股股利(税前)
    return w.wss(security,"div_cashbeforetax",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDOperCostSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业成本_GSD时间序列
    return w.wsd(security,"wgsd_oper_cost",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDOperCost(security:list,*args,**kwargs):
    # 获取营业成本_GSD
    return w.wss(security,"wgsd_oper_cost",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReturnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间回报时间序列
    return w.wsd(security,"return",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReturn(security:list,*args,**kwargs):
    # 获取区间回报
    return w.wss(security,"return",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07IsReItsCostSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业成本时间序列
    return w.wsd(security,"stm07_is_reits_cost",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07IsReItsCost(security:list,*args,**kwargs):
    # 获取营业成本
    return w.wss(security,"stm07_is_reits_cost",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIntExpSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取利息支出时间序列
    return w.wsd(security,"int_exp",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIntExp(security:list,*args,**kwargs):
    # 获取利息支出
    return w.wss(security,"int_exp",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDIntExpSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取利息支出_GSD时间序列
    return w.wsd(security,"wgsd_int_exp",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDIntExp(security:list,*args,**kwargs):
    # 获取利息支出_GSD
    return w.wss(security,"wgsd_int_exp",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInterestExpenseTtM2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取利息支出(TTM)_GSD时间序列
    return w.wsd(security,"interestexpense_ttm2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInterestExpenseTtM2(security:list,*args,**kwargs):
    # 获取利息支出(TTM)_GSD
    return w.wss(security,"interestexpense_ttm2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisAvgPriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取成交均价_期货历史同月时间序列
    return w.wsd(security,"His_avgprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisAvgPrice(security:list,*args,**kwargs):
    # 获取成交均价_期货历史同月
    return w.wss(security,"His_avgprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisOiChangeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取持仓变化_期货历史同月时间序列
    return w.wsd(security,"His_oichange",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHisOiChange(security:list,*args,**kwargs):
    # 获取持仓变化_期货历史同月
    return w.wss(security,"His_oichange",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEre01002Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取耗电总量时间序列
    return w.wsd(security,"esg_ere01002",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEre01002(security:list,*args,**kwargs):
    # 获取耗电总量
    return w.wss(security,"esg_ere01002",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivCashBeforeTax2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股股利(税前)(已宣告)时间序列
    return w.wsd(security,"div_cashbeforetax2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivCashBeforeTax2(security:list,*args,**kwargs):
    # 获取每股股利(税前)(已宣告)
    return w.wss(security,"div_cashbeforetax2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsRecIPtsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取预收款项时间序列
    return w.wsd(security,"stm07_bs_reits_recipts",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsRecIPts(security:list,*args,**kwargs):
    # 获取预收款项
    return w.wss(security,"stm07_bs_reits_recipts",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCfOSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取财务总监时间序列
    return w.wsd(security,"cfo",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCfO(security:list,*args,**kwargs):
    # 获取财务总监
    return w.wss(security,"cfo",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueFeeLegalConsLSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取律师费用时间序列
    return w.wsd(security,"issuefee_legalconsl",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueFeeLegalConsL(security:list,*args,**kwargs):
    # 获取律师费用
    return w.wss(security,"issuefee_legalconsl",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07IsReItsSalesFeeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售费用时间序列
    return w.wsd(security,"stm07_is_reits_salesfee",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07IsReItsSalesFee(security:list,*args,**kwargs):
    # 获取销售费用
    return w.wss(security,"stm07_is_reits_salesfee",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDSalesExpSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售费用_GSD时间序列
    return w.wsd(security,"wgsd_sales_exp",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDSalesExp(security:list,*args,**kwargs):
    # 获取销售费用_GSD
    return w.wss(security,"wgsd_sales_exp",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOperateExpenseTtM3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售费用(TTM)_GSD时间序列
    return w.wsd(security,"operateexpense_ttm3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOperateExpenseTtM3(security:list,*args,**kwargs):
    # 获取销售费用(TTM)_GSD
    return w.wss(security,"operateexpense_ttm3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank0004Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取逾期贷款_3年以上时间序列
    return w.wsd(security,"stmnote_bank_0004",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank0004(security:list,*args,**kwargs):
    # 获取逾期贷款_3年以上
    return w.wss(security,"stmnote_bank_0004",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPremCededSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取分出保费时间序列
    return w.wsd(security,"prem_ceded",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPremCeded(security:list,*args,**kwargs):
    # 获取分出保费
    return w.wss(security,"prem_ceded",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOperateExpenseTtM2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售费用(TTM)时间序列
    return w.wsd(security,"operateexpense_ttm2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOperateExpenseTtM2(security:list,*args,**kwargs):
    # 获取销售费用(TTM)
    return w.wss(security,"operateexpense_ttm2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank0002Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取逾期贷款_3个月至1年时间序列
    return w.wsd(security,"stmnote_bank_0002",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank0002(security:list,*args,**kwargs):
    # 获取逾期贷款_3个月至1年
    return w.wss(security,"stmnote_bank_0002",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank0001Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取逾期贷款_3个月以内时间序列
    return w.wsd(security,"stmnote_bank_0001",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank0001(security:list,*args,**kwargs):
    # 获取逾期贷款_3个月以内
    return w.wss(security,"stmnote_bank_0001",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsTaxSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取应交税费时间序列
    return w.wsd(security,"stm07_bs_reits_tax",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsTax(security:list,*args,**kwargs):
    # 获取应交税费
    return w.wss(security,"stm07_bs_reits_tax",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsPaidInSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取实收资本(或股本)时间序列
    return w.wsd(security,"stm07_bs_reits_paidin",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsPaidIn(security:list,*args,**kwargs):
    # 获取实收资本(或股本)
    return w.wss(security,"stm07_bs_reits_paidin",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOperExpSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业支出时间序列
    return w.wsd(security,"oper_exp",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOperExp(security:list,*args,**kwargs):
    # 获取营业支出
    return w.wss(security,"oper_exp",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDYoYAssetsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资产总计(相对年初增长率)_GSD时间序列
    return w.wsd(security,"wgsd_yoyassets",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDYoYAssets(security:list,*args,**kwargs):
    # 获取资产总计(相对年初增长率)_GSD
    return w.wss(security,"wgsd_yoyassets",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoYAssetsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资产总计(相对年初增长率)时间序列
    return w.wsd(security,"yoyassets",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoYAssets(security:list,*args,**kwargs):
    # 获取资产总计(相对年初增长率)
    return w.wss(security,"yoyassets",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank0003Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取逾期贷款_1年以上3年以内时间序列
    return w.wsd(security,"stmnote_bank_0003",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank0003(security:list,*args,**kwargs):
    # 获取逾期贷款_1年以上3年以内
    return w.wss(security,"stmnote_bank_0003",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEre01006Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取燃油消耗时间序列
    return w.wsd(security,"esg_ere01006",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEre01006(security:list,*args,**kwargs):
    # 获取燃油消耗
    return w.wss(security,"esg_ere01006",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteOthers7628Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取折旧摊销(销售费用)时间序列
    return w.wsd(security,"stmnote_others_7628",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteOthers7628(security:list,*args,**kwargs):
    # 获取折旧摊销(销售费用)
    return w.wss(security,"stmnote_others_7628",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUnitFundShareTotalSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金份额(合计)时间序列
    return w.wsd(security,"unit_fundshare_total",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUnitFundShareTotal(security:list,*args,**kwargs):
    # 获取基金份额(合计)
    return w.wss(security,"unit_fundshare_total",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthOp3YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业利润(近3年增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_op_3y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthOp3Y(security:list,*args,**kwargs):
    # 获取营业利润(近3年增长率)_GSD
    return w.wss(security,"wgsd_growth_op_3y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGMdc01004Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取报告范围时间序列
    return w.wsd(security,"esg_mdc01004",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGMdc01004(security:list,*args,**kwargs):
    # 获取报告范围
    return w.wss(security,"esg_mdc01004",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRevRentSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取租金收入_GSD时间序列
    return w.wsd(security,"wgsd_rev_rent",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRevRent(security:list,*args,**kwargs):
    # 获取租金收入_GSD
    return w.wss(security,"wgsd_rev_rent",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEwa01002Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取节省水量时间序列
    return w.wsd(security,"esg_ewa01002",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEwa01002(security:list,*args,**kwargs):
    # 获取节省水量
    return w.wss(security,"esg_ewa01002",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEwa01001Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取总用水量时间序列
    return w.wsd(security,"esg_ewa01001",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEwa01001(security:list,*args,**kwargs):
    # 获取总用水量
    return w.wss(security,"esg_ewa01001",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthEBt3YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取税前利润(近3年增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_ebt_3y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthEBt3Y(security:list,*args,**kwargs):
    # 获取税前利润(近3年增长率)_GSD
    return w.wss(security,"wgsd_growth_ebt_3y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs80Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取利息收入_FUND时间序列
    return w.wsd(security,"stm_is_80",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs80(security:list,*args,**kwargs):
    # 获取利息收入_FUND
    return w.wss(security,"stm_is_80",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPaymentOrderSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取偿付顺序时间序列
    return w.wsd(security,"paymentorder",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPaymentOrder(security:list,*args,**kwargs):
    # 获取偿付顺序
    return w.wss(security,"paymentorder",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrowthAssetsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资产总计(N年,增长率)时间序列
    return w.wsd(security,"growth_assets",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrowthAssets(security:list,*args,**kwargs):
    # 获取资产总计(N年,增长率)
    return w.wss(security,"growth_assets",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrowthTotalEquitySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取股东权益(N年,增长率)时间序列
    return w.wsd(security,"growth_totalequity",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrowthTotalEquity(security:list,*args,**kwargs):
    # 获取股东权益(N年,增长率)
    return w.wss(security,"growth_totalequity",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrowthEBtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取利润总额(N年,增长率)时间序列
    return w.wsd(security,"growth_ebt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrowthEBt(security:list,*args,**kwargs):
    # 获取利润总额(N年,增长率)
    return w.wss(security,"growth_ebt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIntIncSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取利息收入时间序列
    return w.wsd(security,"int_inc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIntInc(security:list,*args,**kwargs):
    # 获取利息收入
    return w.wss(security,"int_inc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthOp1YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业利润(近1年增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_op_1y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthOp1Y(security:list,*args,**kwargs):
    # 获取营业利润(近1年增长率)_GSD
    return w.wss(security,"wgsd_growth_op_1y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthOrSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业收入(N年,增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_or",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthOr(security:list,*args,**kwargs):
    # 获取营业收入(N年,增长率)_GSD
    return w.wss(security,"wgsd_growth_or",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDEMplBenSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取员工薪酬_GSD时间序列
    return w.wsd(security,"wgsd_empl_ben",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDEMplBen(security:list,*args,**kwargs):
    # 获取员工薪酬_GSD
    return w.wss(security,"wgsd_empl_ben",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMrgLongBalSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取融资余额时间序列
    return w.wsd(security,"mrg_long_bal",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMrgLongBal(security:list,*args,**kwargs):
    # 获取融资余额
    return w.wss(security,"mrg_long_bal",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUnitTotalSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金份额时间序列
    return w.wsd(security,"unit_total",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUnitTotal(security:list,*args,**kwargs):
    # 获取基金份额
    return w.wss(security,"unit_total",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrowthOpSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业利润(N年,增长率)时间序列
    return w.wsd(security,"growth_op",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrowthOp(security:list,*args,**kwargs):
    # 获取营业利润(N年,增长率)
    return w.wss(security,"growth_op",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDSalesOperSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取主营收入_GSD时间序列
    return w.wsd(security,"wgsd_sales_oper",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDSalesOper(security:list,*args,**kwargs):
    # 获取主营收入_GSD
    return w.wss(security,"wgsd_sales_oper",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEre02001Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取纸消耗量时间序列
    return w.wsd(security,"esg_ere02001",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEre02001(security:list,*args,**kwargs):
    # 获取纸消耗量
    return w.wss(security,"esg_ere02001",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDIntIncSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取利息收入_GSD时间序列
    return w.wsd(security,"wgsd_int_inc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDIntInc(security:list,*args,**kwargs):
    # 获取利息收入_GSD
    return w.wss(security,"wgsd_int_inc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrowthOrSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业收入(N年,增长率)时间序列
    return w.wsd(security,"growth_or",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrowthOr(security:list,*args,**kwargs):
    # 获取营业收入(N年,增长率)
    return w.wss(security,"growth_or",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthEBt1YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取税前利润(近1年增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_ebt_1y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthEBt1Y(security:list,*args,**kwargs):
    # 获取税前利润(近1年增长率)_GSD
    return w.wss(security,"wgsd_growth_ebt_1y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank764Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取不良贷款率_质押贷款时间序列
    return w.wsd(security,"stmnote_bank_764",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank764(security:list,*args,**kwargs):
    # 获取不良贷款率_质押贷款
    return w.wss(security,"stmnote_bank_764",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank763Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取不良贷款率_抵押贷款时间序列
    return w.wsd(security,"stmnote_bank_763",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank763(security:list,*args,**kwargs):
    # 获取不良贷款率_抵押贷款
    return w.wss(security,"stmnote_bank_763",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank761Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取不良贷款率_信用贷款时间序列
    return w.wsd(security,"stmnote_bank_761",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank761(security:list,*args,**kwargs):
    # 获取不良贷款率_信用贷款
    return w.wss(security,"stmnote_bank_761",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseConversion2RelativeSwapShareMonthSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取相对转股期时间序列
    return w.wsd(security,"clause_conversion_2_relativeswapsharemonth",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseConversion2RelativeSwapShareMonth(security:list,*args,**kwargs):
    # 获取相对转股期
    return w.wss(security,"clause_conversion_2_relativeswapsharemonth",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank762Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取不良贷款率_保证贷款时间序列
    return w.wsd(security,"stmnote_bank_762",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank762(security:list,*args,**kwargs):
    # 获取不良贷款率_保证贷款
    return w.wss(security,"stmnote_bank_762",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundOperatePeriodClsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取封闭运作期时间序列
    return w.wsd(security,"fund_operateperiod_cls",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundOperatePeriodCls(security:list,*args,**kwargs):
    # 获取封闭运作期
    return w.wss(security,"fund_operateperiod_cls",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareCategorySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取(废弃)大股东类型时间序列
    return w.wsd(security,"sharecategory",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareCategory(security:list,*args,**kwargs):
    # 获取(废弃)大股东类型
    return w.wss(security,"sharecategory",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnchorBondSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取主证券代码时间序列
    return w.wsd(security,"anchorbond",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnchorBond(security:list,*args,**kwargs):
    # 获取主证券代码
    return w.wss(security,"anchorbond",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMajorIndexCodeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取主指数代码时间序列
    return w.wsd(security,"majorindexcode",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMajorIndexCode(security:list,*args,**kwargs):
    # 获取主指数代码
    return w.wss(security,"majorindexcode",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSubIndexCodeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取副指数代码时间序列
    return w.wsd(security,"subindexcode",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSubIndexCode(security:list,*args,**kwargs):
    # 获取副指数代码
    return w.wss(security,"subindexcode",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRelationCodeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取跨市场代码时间序列
    return w.wsd(security,"relationCode",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRelationCode(security:list,*args,**kwargs):
    # 获取跨市场代码
    return w.wss(security,"relationCode",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getChangeLtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取涨跌幅限制时间序列
    return w.wsd(security,"changelt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getChangeLt(security:list,*args,**kwargs):
    # 获取涨跌幅限制
    return w.wss(security,"changelt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getChangeLtNewSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取涨跌幅限制(支持历史)时间序列
    return w.wsd(security,"changelt_new",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getChangeLtNew(security:list,*args,**kwargs):
    # 获取涨跌幅限制(支持历史)
    return w.wss(security,"changelt_new",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getQtVolMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取报价总笔数时间序列
    return w.wsd(security,"qtvolm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getQtVolM(security:list,*args,**kwargs):
    # 获取报价总笔数
    return w.wss(security,"qtvolm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPeLyRSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取市盈率PE(LYR)时间序列
    return w.wsd(security,"pe_lyr",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPeLyR(security:list,*args,**kwargs):
    # 获取市盈率PE(LYR)
    return w.wss(security,"pe_lyr",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPbLyRSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取市净率PB(LYR)时间序列
    return w.wsd(security,"pb_lyr",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPbLyR(security:list,*args,**kwargs):
    # 获取市净率PB(LYR)
    return w.wss(security,"pb_lyr",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank821Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取不良贷款率_短期贷款时间序列
    return w.wsd(security,"stmnote_bank_821",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank821(security:list,*args,**kwargs):
    # 获取不良贷款率_短期贷款
    return w.wss(security,"stmnote_bank_821",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMaturityCallPriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取到期赎回价时间序列
    return w.wsd(security,"maturitycallprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMaturityCallPrice(security:list,*args,**kwargs):
    # 获取到期赎回价
    return w.wss(security,"maturitycallprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank730Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取不良贷款率_总计时间序列
    return w.wsd(security,"stmnote_bank_730",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank730(security:list,*args,**kwargs):
    # 获取不良贷款率_总计
    return w.wss(security,"stmnote_bank_730",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPriorityToGeneralSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取委托资金比(优先/一般)(信托)时间序列
    return w.wsd(security,"fund_prioritytogeneral",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPriorityToGeneral(security:list,*args,**kwargs):
    # 获取委托资金比(优先/一般)(信托)
    return w.wss(security,"fund_prioritytogeneral",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDOperExpToTSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总营业支出_GSD时间序列
    return w.wsd(security,"wgsd_oper_exp_tot",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDOperExpToT(security:list,*args,**kwargs):
    # 获取总营业支出_GSD
    return w.wss(security,"wgsd_oper_exp_tot",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderNumFundSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取持股基金数时间序列
    return w.wsd(security,"holder_num_fund",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderNumFund(security:list,*args,**kwargs):
    # 获取持股基金数
    return w.wss(security,"holder_num_fund",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLastTradingDaySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取(废弃)最后交易日时间序列
    return w.wsd(security,"lasttradingday",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLastTradingDay(security:list,*args,**kwargs):
    # 获取(废弃)最后交易日
    return w.wss(security,"lasttradingday",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank31Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取正常-金额时间序列
    return w.wsd(security,"stmnote_bank_31",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank31(security:list,*args,**kwargs):
    # 获取正常-金额
    return w.wss(security,"stmnote_bank_31",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundMaturityDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取(废弃)基金到期日时间序列
    return w.wsd(security,"fund_maturitydate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundMaturityDate(security:list,*args,**kwargs):
    # 获取(废弃)基金到期日
    return w.wss(security,"fund_maturitydate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssueRegDateShareBSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取股权登记日(B股最后交易日)时间序列
    return w.wsd(security,"rightsissue_regdateshareb",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssueRegDateShareB(security:list,*args,**kwargs):
    # 获取股权登记日(B股最后交易日)
    return w.wss(security,"rightsissue_regdateshareb",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLastDeliveryDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最后交割日时间序列
    return w.wsd(security,"lastdelivery_date",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLastDeliveryDate(security:list,*args,**kwargs):
    # 获取最后交割日
    return w.wss(security,"lastdelivery_date",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLdDateNewSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最后交割日(支持历史)时间序列
    return w.wsd(security,"lddate_new",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLdDateNew(security:list,*args,**kwargs):
    # 获取最后交割日(支持历史)
    return w.wss(security,"lddate_new",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs78Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取所得税费用_FUND时间序列
    return w.wsd(security,"stm_is_78",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs78(security:list,*args,**kwargs):
    # 获取所得税费用_FUND
    return w.wss(security,"stm_is_78",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseConversion2ForceConvertDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取强制转股日时间序列
    return w.wsd(security,"clause_conversion_2_forceconvertdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseConversion2ForceConvertDate(security:list,*args,**kwargs):
    # 获取强制转股日
    return w.wss(security,"clause_conversion_2_forceconvertdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs26Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取税金及附加_FUND时间序列
    return w.wsd(security,"stm_is_26",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs26(security:list,*args,**kwargs):
    # 获取税金及附加_FUND
    return w.wss(security,"stm_is_26",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderNameSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取大股东名称时间序列
    return w.wsd(security,"holder_name",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderName(security:list,*args,**kwargs):
    # 获取大股东名称
    return w.wss(security,"holder_name",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLPriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取挂牌基准价时间序列
    return w.wsd(security,"lprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLPrice(security:list,*args,**kwargs):
    # 获取挂牌基准价
    return w.wss(security,"lprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07IsReItsTaxSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取税金及附加时间序列
    return w.wsd(security,"stm07_is_reits_tax",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07IsReItsTax(security:list,*args,**kwargs):
    # 获取税金及附加
    return w.wss(security,"stm07_is_reits_tax",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getExpectedYieldSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取预期收益率(文字)时间序列
    return w.wsd(security,"expectedyield",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getExpectedYield(security:list,*args,**kwargs):
    # 获取预期收益率(文字)
    return w.wss(security,"expectedyield",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGSem01001Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取雇员总人数时间序列
    return w.wsd(security,"esg_sem01001",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGSem01001(security:list,*args,**kwargs):
    # 获取雇员总人数
    return w.wss(security,"esg_sem01001",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDQAmountCnBdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取现券结算量(中债)时间序列
    return w.wsd(security,"dq_amount_cnbd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDQAmountCnBd(security:list,*args,**kwargs):
    # 获取现券结算量(中债)
    return w.wss(security,"dq_amount_cnbd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderPaymentDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取缴款起始日时间序列
    return w.wsd(security,"tender_paymentdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderPaymentDate(security:list,*args,**kwargs):
    # 获取缴款起始日
    return w.wss(security,"tender_paymentdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssueListedDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取配股上市日时间序列
    return w.wsd(security,"rightsissue_listeddate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssueListedDate(security:list,*args,**kwargs):
    # 获取配股上市日
    return w.wss(security,"rightsissue_listeddate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalIpRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取平均派息率时间序列
    return w.wsd(security,"anal_ipratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalIpRatio(security:list,*args,**kwargs):
    # 获取平均派息率
    return w.wss(security,"anal_ipratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalPeriodSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取平均待偿期时间序列
    return w.wsd(security,"anal_period",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalPeriod(security:list,*args,**kwargs):
    # 获取平均待偿期
    return w.wss(security,"anal_period",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssueExDividendDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取配股除权日时间序列
    return w.wsd(security,"rightsissue_exdividenddate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssueExDividendDate(security:list,*args,**kwargs):
    # 获取配股除权日
    return w.wss(security,"rightsissue_exdividenddate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStDebtRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取现金短债比(公告值)_GSD时间序列
    return w.wsd(security,"stdebtratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStDebtRatio(security:list,*args,**kwargs):
    # 获取现金短债比(公告值)_GSD
    return w.wss(security,"stdebtratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMarginSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取交易保证金时间序列
    return w.wsd(security,"margin",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMargin(security:list,*args,**kwargs):
    # 获取交易保证金
    return w.wss(security,"margin",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDIntIncNetSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取利息净收入_GSD时间序列
    return w.wsd(security,"wgsd_int_inc_net",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDIntIncNet(security:list,*args,**kwargs):
    # 获取利息净收入_GSD
    return w.wss(security,"wgsd_int_inc_net",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseCallOptionTimeRedemptionTimesSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取时点赎回数时间序列
    return w.wsd(security,"clause_calloption_timeredemptiontimes",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseCallOptionTimeRedemptionTimes(security:list,*args,**kwargs):
    # 获取时点赎回数
    return w.wss(security,"clause_calloption_timeredemptiontimes",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValPeDeductedTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取市盈率PE(TTM,扣除非经常性损益)时间序列
    return w.wsd(security,"val_pe_deducted_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValPeDeductedTtM(security:list,*args,**kwargs):
    # 获取市盈率PE(TTM,扣除非经常性损益)
    return w.wss(security,"val_pe_deducted_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSec34Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取资本杠杆率时间序列
    return w.wsd(security,"stmnote_sec_34",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSec34(security:list,*args,**kwargs):
    # 获取资本杠杆率
    return w.wss(security,"stmnote_sec_34",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetIntIncSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取利息净收入时间序列
    return w.wsd(security,"net_int_inc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetIntInc(security:list,*args,**kwargs):
    # 获取利息净收入
    return w.wss(security,"net_int_inc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPbMrQGsDSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取市净率PB(MRQ,海外)时间序列
    return w.wsd(security,"pb_mrq_gsd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPbMrQGsD(security:list,*args,**kwargs):
    # 获取市净率PB(MRQ,海外)
    return w.wss(security,"pb_mrq_gsd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank822Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取不良贷款率_中长期贷款时间序列
    return w.wsd(security,"stmnote_bank_822",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank822(security:list,*args,**kwargs):
    # 获取不良贷款率_中长期贷款
    return w.wss(security,"stmnote_bank_822",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCapIADeRatioNSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资本充足率时间序列
    return w.wsd(security,"capi_ade_ratio_n",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCapIADeRatioN(security:list,*args,**kwargs):
    # 获取资本充足率
    return w.wss(security,"capi_ade_ratio_n",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPsLyRSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取市销率PS(LYR)时间序列
    return w.wsd(security,"ps_lyr",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPsLyR(security:list,*args,**kwargs):
    # 获取市销率PS(LYR)
    return w.wss(security,"ps_lyr",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReturn5YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取近5年回报时间序列
    return w.wsd(security,"return_5y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReturn5Y(security:list,*args,**kwargs):
    # 获取近5年回报
    return w.wss(security,"return_5y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCounterGuarSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取反担保情况时间序列
    return w.wsd(security,"counterguar",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCounterGuar(security:list,*args,**kwargs):
    # 获取反担保情况
    return w.wss(security,"counterguar",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerFundNoSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取任职基金数时间序列
    return w.wsd(security,"fund_manager_fundno",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerFundNo(security:list,*args,**kwargs):
    # 获取任职基金数
    return w.wss(security,"fund_manager_fundno",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReturnMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取单月度回报时间序列
    return w.wsd(security,"return_m",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReturnM(security:list,*args,**kwargs):
    # 获取单月度回报
    return w.wss(security,"return_m",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDNetworkingCapital2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取净营运资本_GSD时间序列
    return w.wsd(security,"wgsd_networkingcapital2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDNetworkingCapital2(security:list,*args,**kwargs):
    # 获取净营运资本_GSD
    return w.wss(security,"wgsd_networkingcapital2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReturnQSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取单季度回报时间序列
    return w.wsd(security,"return_q",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReturnQ(security:list,*args,**kwargs):
    # 获取单季度回报
    return w.wss(security,"return_q",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReturnYSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取单年度回报时间序列
    return w.wsd(security,"return_y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReturnY(security:list,*args,**kwargs):
    # 获取单年度回报
    return w.wss(security,"return_y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowWeightedPeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取增发市盈率(加权)时间序列
    return w.wsd(security,"fellow_weightedpe",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowWeightedPe(security:list,*args,**kwargs):
    # 获取增发市盈率(加权)
    return w.wss(security,"fellow_weightedpe",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetworkingCapitalSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净营运资本时间序列
    return w.wsd(security,"networkingcapital",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetworkingCapital(security:list,*args,**kwargs):
    # 获取净营运资本
    return w.wss(security,"networkingcapital",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderNatureSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取大股东性质时间序列
    return w.wsd(security,"holder_nature",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderNature(security:list,*args,**kwargs):
    # 获取大股东性质
    return w.wss(security,"holder_nature",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIntColRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取利息回收率(旧)时间序列
    return w.wsd(security,"intcolratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIntColRatio(security:list,*args,**kwargs):
    # 获取利息回收率(旧)
    return w.wss(security,"intcolratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyDeputyUnderwriterSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取副主承销商时间序列
    return w.wsd(security,"agency_deputyunderwriter",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyDeputyUnderwriter(security:list,*args,**kwargs):
    # 获取副主承销商
    return w.wss(security,"agency_deputyunderwriter",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowDilutedPeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取增发市盈率(摊薄)时间序列
    return w.wsd(security,"fellow_dilutedpe",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowDilutedPe(security:list,*args,**kwargs):
    # 获取增发市盈率(摊薄)
    return w.wss(security,"fellow_dilutedpe",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReturn3YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取近3年回报时间序列
    return w.wsd(security,"return_3y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReturn3Y(security:list,*args,**kwargs):
    # 获取近3年回报
    return w.wss(security,"return_3y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPtMDaySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取剩余存续期时间序列
    return w.wsd(security,"fund_ptmday",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPtMDay(security:list,*args,**kwargs):
    # 获取剩余存续期
    return w.wss(security,"fund_ptmday",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowRegisterDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取股份登记日时间序列
    return w.wsd(security,"fellow_registerdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowRegisterDate(security:list,*args,**kwargs):
    # 获取股份登记日
    return w.wss(security,"fellow_registerdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowRoadshowDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取网上路演日时间序列
    return w.wsd(security,"fellow_roadshowdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowRoadshowDate(security:list,*args,**kwargs):
    # 获取网上路演日
    return w.wss(security,"fellow_roadshowdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPtMYearSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金存续期时间序列
    return w.wsd(security,"fund_ptmyear",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPtMYear(security:list,*args,**kwargs):
    # 获取基金存续期
    return w.wss(security,"fund_ptmyear",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowIssueDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取公开发行日时间序列
    return w.wsd(security,"fellow_issuedate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowIssueDate(security:list,*args,**kwargs):
    # 获取公开发行日
    return w.wss(security,"fellow_issuedate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowOfferingDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取增发公告日时间序列
    return w.wsd(security,"fellow_offeringdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowOfferingDate(security:list,*args,**kwargs):
    # 获取增发公告日
    return w.wss(security,"fellow_offeringdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNonOperExpSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业外支出时间序列
    return w.wsd(security,"non_oper_exp",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNonOperExp(security:list,*args,**kwargs):
    # 获取营业外支出
    return w.wss(security,"non_oper_exp",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClausePutOptionPutBackPeriodObSSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取相对回售期时间序列
    return w.wsd(security,"clause_putoption_putbackperiodobs",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClausePutOptionPutBackPeriodObS(security:list,*args,**kwargs):
    # 获取相对回售期
    return w.wss(security,"clause_putoption_putbackperiodobs",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOpenPerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间开盘价时间序列
    return w.wsd(security,"open_per",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOpenPer(security:list,*args,**kwargs):
    # 获取区间开盘价
    return w.wss(security,"open_per",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundMgNtFeeExplainSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取管理费说明时间序列
    return w.wsd(security,"fund_mgntfeeexplain",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundMgNtFeeExplain(security:list,*args,**kwargs):
    # 获取管理费说明
    return w.wss(security,"fund_mgntfeeexplain",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUsOpenSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取标的开盘价时间序列
    return w.wsd(security,"us_open",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUsOpen(security:list,*args,**kwargs):
    # 获取标的开盘价
    return w.wss(security,"us_open",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundWarrantOrIntroductionSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取保证人简介时间序列
    return w.wsd(security,"fund_warrantorintroduction",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundWarrantOrIntroduction(security:list,*args,**kwargs):
    # 获取保证人简介
    return w.wss(security,"fund_warrantorintroduction",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerPreviousFundNoSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取历任基金数时间序列
    return w.wsd(security,"fund_manager_previousfundno",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerPreviousFundNo(security:list,*args,**kwargs):
    # 获取历任基金数
    return w.wss(security,"fund_manager_previousfundno",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDComEqParSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取普通股股本_GSD时间序列
    return w.wsd(security,"wgsd_com_eq_par",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDComEqPar(security:list,*args,**kwargs):
    # 获取普通股股本_GSD
    return w.wss(security,"wgsd_com_eq_par",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNonOperRevSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业外收入时间序列
    return w.wsd(security,"non_oper_rev",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNonOperRev(security:list,*args,**kwargs):
    # 获取营业外收入
    return w.wss(security,"non_oper_rev",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReturn2YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取近2年回报时间序列
    return w.wsd(security,"return_2y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReturn2Y(security:list,*args,**kwargs):
    # 获取近2年回报
    return w.wss(security,"return_2y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReturn1YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取近1年回报时间序列
    return w.wsd(security,"return_1y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReturn1Y(security:list,*args,**kwargs):
    # 获取近1年回报
    return w.wss(security,"return_1y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReturn6MSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取近6月回报时间序列
    return w.wsd(security,"return_6m",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReturn6M(security:list,*args,**kwargs):
    # 获取近6月回报
    return w.wss(security,"return_6m",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBankCapAdequacyRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资本充足率(2013)时间序列
    return w.wsd(security,"stmnote_bank_CapAdequacyRatio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBankCapAdequacyRatio(security:list,*args,**kwargs):
    # 获取资本充足率(2013)
    return w.wss(security,"stmnote_bank_CapAdequacyRatio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank67Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取不良贷款率(按行业)时间序列
    return w.wsd(security,"stmnote_bank_67",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank67(security:list,*args,**kwargs):
    # 获取不良贷款率(按行业)
    return w.wss(security,"stmnote_bank_67",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValPeWGtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取市盈率PE(LYR,加权)时间序列
    return w.wsd(security,"val_pe_wgt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValPeWGt(security:list,*args,**kwargs):
    # 获取市盈率PE(LYR,加权)
    return w.wss(security,"val_pe_wgt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank340Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取关注-金额时间序列
    return w.wsd(security,"stmnote_bank_340",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank340(security:list,*args,**kwargs):
    # 获取关注-金额
    return w.wss(security,"stmnote_bank_340",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTradeHisCodeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取月合约代码时间序列
    return w.wsd(security,"trade_hiscode",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTradeHisCode(security:list,*args,**kwargs):
    # 获取月合约代码
    return w.wss(security,"trade_hiscode",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEre01001Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取总能源消耗时间序列
    return w.wsd(security,"esg_ere01001",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEre01001(security:list,*args,**kwargs):
    # 获取总能源消耗
    return w.wss(security,"esg_ere01001",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGcTtM2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业总成本(TTM)时间序列
    return w.wsd(security,"gc_ttm2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGcTtM2(security:list,*args,**kwargs):
    # 获取营业总成本(TTM)
    return w.wss(security,"gc_ttm2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSecuritiesBrokerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取证券经纪人(信托)时间序列
    return w.wsd(security,"fund_securitiesbroker",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSecuritiesBroker(security:list,*args,**kwargs):
    # 获取证券经纪人(信托)
    return w.wss(security,"fund_securitiesbroker",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNonOpTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取非营业利润(TTM)_GSD时间序列
    return w.wsd(security,"nonop_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNonOpTtM(security:list,*args,**kwargs):
    # 获取非营业利润(TTM)_GSD
    return w.wss(security,"nonop_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank411Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取非利息收入时间序列
    return w.wsd(security,"stmnote_bank_411",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank411(security:list,*args,**kwargs):
    # 获取非利息收入
    return w.wss(security,"stmnote_bank_411",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseCallOptionTriggerPriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取赎回触发价时间序列
    return w.wsd(security,"clause_calloption_triggerprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseCallOptionTriggerPrice(security:list,*args,**kwargs):
    # 获取赎回触发价
    return w.wss(security,"clause_calloption_triggerprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPledGableOrNotSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取是否可质押时间序列
    return w.wsd(security,"fund_pledgableornot",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPledGableOrNot(security:list,*args,**kwargs):
    # 获取是否可质押
    return w.wss(security,"fund_pledgableornot",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssueAmountSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取实际配股数时间序列
    return w.wsd(security,"rightsissue_amount",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssueAmount(security:list,*args,**kwargs):
    # 获取实际配股数
    return w.wss(security,"rightsissue_amount",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssuePlanAmtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取计划配股数时间序列
    return w.wsd(security,"rightsissue_planamt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssuePlanAmt(security:list,*args,**kwargs):
    # 获取计划配股数
    return w.wss(security,"rightsissue_planamt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssuePerShareSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股配股数时间序列
    return w.wsd(security,"rightsissue_pershare",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssuePerShare(security:list,*args,**kwargs):
    # 获取每股配股数
    return w.wss(security,"rightsissue_pershare",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGcTtM3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业总成本(TTM)_GSD时间序列
    return w.wsd(security,"gc_ttm3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGcTtM3(security:list,*args,**kwargs):
    # 获取营业总成本(TTM)_GSD
    return w.wss(security,"gc_ttm3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCollateralNameSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取质押券简称时间序列
    return w.wsd(security,"collateralname",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCollateralName(security:list,*args,**kwargs):
    # 获取质押券简称
    return w.wss(security,"collateralname",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07IsReItsSCostSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业总成本时间序列
    return w.wsd(security,"stm07_is_reits_scost",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07IsReItsSCost(security:list,*args,**kwargs):
    # 获取营业总成本
    return w.wss(security,"stm07_is_reits_scost",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEem03003Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取废弃物总量时间序列
    return w.wsd(security,"esg_eem03003",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEem03003(security:list,*args,**kwargs):
    # 获取废弃物总量
    return w.wss(security,"esg_eem03003",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaGcTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业总成本(TTM)_PIT时间序列
    return w.wsd(security,"fa_gc_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaGcTtM(security:list,*args,**kwargs):
    # 获取营业总成本(TTM)_PIT
    return w.wss(security,"fa_gc_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCollateralCodeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取质押券代码时间序列
    return w.wsd(security,"collateralcode",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCollateralCode(security:list,*args,**kwargs):
    # 获取质押券代码
    return w.wss(security,"collateralcode",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPbLfSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取市净率PB(LF,内地)时间序列
    return w.wsd(security,"pb_lf",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPbLf(security:list,*args,**kwargs):
    # 获取市净率PB(LF,内地)
    return w.wss(security,"pb_lf",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGcTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业总成本(TTM,只有最新数据)时间序列
    return w.wsd(security,"gc_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGcTtM(security:list,*args,**kwargs):
    # 获取营业总成本(TTM,只有最新数据)
    return w.wss(security,"gc_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIntColRatioNSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取利息回收率时间序列
    return w.wsd(security,"intcolratio_n",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIntColRatioN(security:list,*args,**kwargs):
    # 获取利息回收率
    return w.wss(security,"intcolratio_n",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReturn1WSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取近1周回报时间序列
    return w.wsd(security,"return_1w",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReturn1W(security:list,*args,**kwargs):
    # 获取近1周回报
    return w.wss(security,"return_1w",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseCallOptionNoticeDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取赎回公告日时间序列
    return w.wsd(security,"clause_calloption_noticedate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseCallOptionNoticeDate(security:list,*args,**kwargs):
    # 获取赎回公告日
    return w.wss(security,"clause_calloption_noticedate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur9Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取综合成本率(产险)时间序列
    return w.wsd(security,"stmnote_insur_9",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur9(security:list,*args,**kwargs):
    # 获取综合成本率(产险)
    return w.wss(security,"stmnote_insur_9",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReturn1MSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取近1月回报时间序列
    return w.wsd(security,"return_1m",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReturn1M(security:list,*args,**kwargs):
    # 获取近1月回报
    return w.wss(security,"return_1m",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReturn3MSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取近3月回报时间序列
    return w.wsd(security,"return_3m",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReturn3M(security:list,*args,**kwargs):
    # 获取近3月回报
    return w.wss(security,"return_3m",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCapIADeRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资本充足率(旧)时间序列
    return w.wsd(security,"capi_ade_ratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCapIADeRatio(security:list,*args,**kwargs):
    # 获取资本充足率(旧)
    return w.wss(security,"capi_ade_ratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYieldShcSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取估价收益率(上清所)时间序列
    return w.wsd(security,"yield_shc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYieldShc(security:list,*args,**kwargs):
    # 获取估价收益率(上清所)
    return w.wss(security,"yield_shc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSetUpdateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金成立日时间序列
    return w.wsd(security,"fund_setupdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSetUpdate(security:list,*args,**kwargs):
    # 获取基金成立日
    return w.wss(security,"fund_setupdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderNumISeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取持股机构数时间序列
    return w.wsd(security,"holder_num_i",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderNumI(security:list,*args,**kwargs):
    # 获取持股机构数
    return w.wss(security,"holder_num_i",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDInvestEqSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取权益性投资_GSD时间序列
    return w.wsd(security,"wgsd_invest_eq",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDInvestEq(security:list,*args,**kwargs):
    # 获取权益性投资_GSD
    return w.wss(security,"wgsd_invest_eq",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCrmBookkeepingDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取簿记建档日时间序列
    return w.wsd(security,"crm_bookkeepingdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCrmBookkeepingDate(security:list,*args,**kwargs):
    # 获取簿记建档日
    return w.wss(security,"crm_bookkeepingdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDDaSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取折旧及摊销_GSD时间序列
    return w.wsd(security,"wgsd_da",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDDa(security:list,*args,**kwargs):
    # 获取折旧及摊销_GSD
    return w.wss(security,"wgsd_da",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyBookRunnerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取簿记管理人时间序列
    return w.wsd(security,"agency_Bookrunner",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyBookRunner(security:list,*args,**kwargs):
    # 获取簿记管理人
    return w.wss(security,"agency_Bookrunner",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDDepExpCfSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取折旧与摊销_GSD时间序列
    return w.wsd(security,"wgsd_dep_exp_cf",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDDepExpCf(security:list,*args,**kwargs):
    # 获取折旧与摊销_GSD
    return w.wss(security,"wgsd_dep_exp_cf",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDCapeXFfSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资本性支出_GSD时间序列
    return w.wsd(security,"wgsd_capex_ff",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDCapeXFf(security:list,*args,**kwargs):
    # 获取资本性支出_GSD
    return w.wss(security,"wgsd_capex_ff",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReturnEnddateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取收益终止日时间序列
    return w.wsd(security,"fund_returnenddate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReturnEnddate(security:list,*args,**kwargs):
    # 获取收益终止日
    return w.wss(security,"fund_returnenddate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareOtcRestrictedSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取限售三板股时间序列
    return w.wsd(security,"share_otcrestricted",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareOtcRestricted(security:list,*args,**kwargs):
    # 获取限售三板股
    return w.wss(security,"share_otcrestricted",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCrmDateOfRecordSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取凭证登记日时间序列
    return w.wsd(security,"crm_dateofrecord",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCrmDateOfRecord(security:list,*args,**kwargs):
    # 获取凭证登记日
    return w.wss(security,"crm_dateofrecord",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetInvestIncSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取投资净收益时间序列
    return w.wsd(security,"net_invest_inc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetInvestInc(security:list,*args,**kwargs):
    # 获取投资净收益
    return w.wss(security,"net_invest_inc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReturnStartDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取收益起始日时间序列
    return w.wsd(security,"fund_returnstartdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReturnStartDate(security:list,*args,**kwargs):
    # 获取收益起始日
    return w.wss(security,"fund_returnstartdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundRedMStartDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取赎回起始日时间序列
    return w.wsd(security,"fund_redmstartdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundRedMStartDate(security:list,*args,**kwargs):
    # 获取赎回起始日
    return w.wss(security,"fund_redmstartdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPChConfirmDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取申购确认日时间序列
    return w.wsd(security,"fund_pchconfirmdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPChConfirmDate(security:list,*args,**kwargs):
    # 获取申购确认日
    return w.wss(security,"fund_pchconfirmdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundRedMConfirmDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取赎回确认日时间序列
    return w.wsd(security,"fund_redmconfirmdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundRedMConfirmDate(security:list,*args,**kwargs):
    # 获取赎回确认日
    return w.wss(security,"fund_redmconfirmdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseConversion2BondProportionSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取未转股比例时间序列
    return w.wsd(security,"clause_conversion2_bondproportion",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseConversion2BondProportion(security:list,*args,**kwargs):
    # 获取未转股比例
    return w.wss(security,"clause_conversion2_bondproportion",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderPayEnddateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取缴款截止日时间序列
    return w.wsd(security,"tender_payenddate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderPayEnddate(security:list,*args,**kwargs):
    # 获取缴款截止日
    return w.wss(security,"tender_payenddate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTheOPricePerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取(废弃)区间理论价时间序列
    return w.wsd(security,"theo_price_per",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTheOPricePer(security:list,*args,**kwargs):
    # 获取(废弃)区间理论价
    return w.wss(security,"theo_price_per",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPrtFoundLeverageSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金杠杆率时间序列
    return w.wsd(security,"prt_foundleverage",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPrtFoundLeverage(security:list,*args,**kwargs):
    # 获取基金杠杆率
    return w.wss(security,"prt_foundleverage",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundRedMarriAlDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取赎回划款日时间序列
    return w.wsd(security,"fund_redmarrialdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundRedMarriAlDate(security:list,*args,**kwargs):
    # 获取赎回划款日
    return w.wss(security,"fund_redmarrialdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueOeClsPeriodSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行封闭期时间序列
    return w.wsd(security,"issue_oeclsperiod",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueOeClsPeriod(security:list,*args,**kwargs):
    # 获取发行封闭期
    return w.wss(security,"issue_oeclsperiod",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDPremiumsEarnedSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净已赚保费_GSD时间序列
    return w.wsd(security,"wgsd_premiums_earned",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDPremiumsEarned(security:list,*args,**kwargs):
    # 获取净已赚保费_GSD
    return w.wss(security,"wgsd_premiums_earned",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCorpFundNoSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取旗下基金数时间序列
    return w.wsd(security,"fund_corp_fundno",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCorpFundNo(security:list,*args,**kwargs):
    # 获取旗下基金数
    return w.wss(security,"fund_corp_fundno",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetGainFxTransSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取汇兑净收益时间序列
    return w.wsd(security,"net_gain_fx_trans",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetGainFxTrans(security:list,*args,**kwargs):
    # 获取汇兑净收益
    return w.wss(security,"net_gain_fx_trans",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYieldCsiSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取估价收益率(中证指数)(旧)时间序列
    return w.wsd(security,"yield_csi",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYieldCsi(security:list,*args,**kwargs):
    # 获取估价收益率(中证指数)(旧)
    return w.wss(security,"yield_csi",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueInitiatorSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金发起人时间序列
    return w.wsd(security,"issue_initiator",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueInitiator(security:list,*args,**kwargs):
    # 获取基金发起人
    return w.wss(security,"issue_initiator",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueTotalSizeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行总规模时间序列
    return w.wsd(security,"issue_totalsize",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueTotalSize(security:list,*args,**kwargs):
    # 获取发行总规模
    return w.wss(security,"issue_totalsize",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDSalesSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总营业收入_GSD时间序列
    return w.wsd(security,"wgsd_sales",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDSales(security:list,*args,**kwargs):
    # 获取总营业收入_GSD
    return w.wss(security,"wgsd_sales",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReserveRatioFcSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取备付金比率(外币)(旧)时间序列
    return w.wsd(security,"reserveratio_fc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReserveRatioFc(security:list,*args,**kwargs):
    # 获取备付金比率(外币)(旧)
    return w.wss(security,"reserveratio_fc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteOthers7639Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取短期融资债(其他流动负债)时间序列
    return w.wsd(security,"stmnote_others_7639",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteOthers7639(security:list,*args,**kwargs):
    # 获取短期融资债(其他流动负债)
    return w.wss(security,"stmnote_others_7639",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClausePutOptionNoticeDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取回售公告日时间序列
    return w.wsd(security,"clause_putoption_noticedate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClausePutOptionNoticeDate(security:list,*args,**kwargs):
    # 获取回售公告日
    return w.wss(security,"clause_putoption_noticedate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseCallOptionRelativeCallOptionPeriodSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取相对赎回期时间序列
    return w.wsd(security,"clause_calloption_relativecalloptionperiod",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseCallOptionRelativeCallOptionPeriod(security:list,*args,**kwargs):
    # 获取相对赎回期
    return w.wss(security,"clause_calloption_relativecalloptionperiod",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundActualMaturityDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取实际到期日时间序列
    return w.wsd(security,"fund_actualmaturitydate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundActualMaturityDate(security:list,*args,**kwargs):
    # 获取实际到期日
    return w.wss(security,"fund_actualmaturitydate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundMainRiskSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取主要风险点时间序列
    return w.wsd(security,"fund_mainrisk",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundMainRisk(security:list,*args,**kwargs):
    # 获取主要风险点
    return w.wss(security,"fund_mainrisk",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEre01005Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取天然气消耗时间序列
    return w.wsd(security,"esg_ere01005",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEre01005(security:list,*args,**kwargs):
    # 获取天然气消耗
    return w.wss(security,"esg_ere01005",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClausePutOptionTimePutBackTimesSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取时点回售数时间序列
    return w.wsd(security,"clause_putoption_timeputbacktimes",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClausePutOptionTimePutBackTimes(security:list,*args,**kwargs):
    # 获取时点回售数
    return w.wss(security,"clause_putoption_timeputbacktimes",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEre01004Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取煤碳使用量时间序列
    return w.wsd(security,"esg_ere01004",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEre01004(security:list,*args,**kwargs):
    # 获取煤碳使用量
    return w.wss(security,"esg_ere01004",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEre01003Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取节省用电量时间序列
    return w.wsd(security,"esg_ere01003",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEre01003(security:list,*args,**kwargs):
    # 获取节省用电量
    return w.wss(security,"esg_ere01003",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLoanDePoRatioNormBSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取存贷款比率(外币)(旧)时间序列
    return w.wsd(security,"loan_depo_ratio_normb",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLoanDePoRatioNormB(security:list,*args,**kwargs):
    # 获取存贷款比率(外币)(旧)
    return w.wss(security,"loan_depo_ratio_normb",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEre02002Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取废纸回收量时间序列
    return w.wsd(security,"esg_ere02002",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEre02002(security:list,*args,**kwargs):
    # 获取废纸回收量
    return w.wss(security,"esg_ere02002",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPChRedMPChStartDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取申购起始日时间序列
    return w.wsd(security,"fund_pchredm_pchstartdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPChRedMPChStartDate(security:list,*args,**kwargs):
    # 获取申购起始日
    return w.wss(security,"fund_pchredm_pchstartdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLoanDePoRatioRMbSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取存贷款比率(人民币)(旧)时间序列
    return w.wsd(security,"loan_depo_ratio_rmb",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLoanDePoRatioRMb(security:list,*args,**kwargs):
    # 获取存贷款比率(人民币)(旧)
    return w.wss(security,"loan_depo_ratio_rmb",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLoanDePoRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取存贷款比率(旧)时间序列
    return w.wsd(security,"loan_depo_ratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLoanDePoRatio(security:list,*args,**kwargs):
    # 获取存贷款比率(旧)
    return w.wss(security,"loan_depo_ratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLoanDePoRatioNormBNSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取存贷款比率(外币)时间序列
    return w.wsd(security,"loan_depo_ratio_normb_n",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLoanDePoRatioNormBN(security:list,*args,**kwargs):
    # 获取存贷款比率(外币)
    return w.wss(security,"loan_depo_ratio_normb_n",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLoanDePoRatioRMbNSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取存贷款比率(人民币)时间序列
    return w.wsd(security,"loan_depo_ratio_rmb_n",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLoanDePoRatioRMbN(security:list,*args,**kwargs):
    # 获取存贷款比率(人民币)
    return w.wss(security,"loan_depo_ratio_rmb_n",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLoanDePoRatioNSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取存贷款比率时间序列
    return w.wsd(security,"loan_depo_ratio_n",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLoanDePoRatioN(security:list,*args,**kwargs):
    # 获取存贷款比率
    return w.wss(security,"loan_depo_ratio_n",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank129Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取成本收入比(旧)时间序列
    return w.wsd(security,"stmnote_bank_129",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank129(security:list,*args,**kwargs):
    # 获取成本收入比(旧)
    return w.wss(security,"stmnote_bank_129",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank129NSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取成本收入比时间序列
    return w.wsd(security,"stmnote_bank_129_n",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank129N(security:list,*args,**kwargs):
    # 获取成本收入比
    return w.wss(security,"stmnote_bank_129_n",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReserveRatioRMbNSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取备付金比率(人民币)时间序列
    return w.wsd(security,"reserveratio_rmb_n",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReserveRatioRMbN(security:list,*args,**kwargs):
    # 获取备付金比率(人民币)
    return w.wss(security,"reserveratio_rmb_n",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDNetProfitIsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取除税后利润_GSD时间序列
    return w.wsd(security,"wgsd_net_profit_is",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDNetProfitIs(security:list,*args,**kwargs):
    # 获取除税后利润_GSD
    return w.wss(security,"wgsd_net_profit_is",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCrmCarryDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取凭证起始日时间序列
    return w.wsd(security,"crm_carrydate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCrmCarryDate(security:list,*args,**kwargs):
    # 获取凭证起始日
    return w.wss(security,"crm_carrydate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyBondTrusteeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取受托管理人时间序列
    return w.wsd(security,"agency_bondtrustee",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyBondTrustee(security:list,*args,**kwargs):
    # 获取受托管理人
    return w.wss(security,"agency_bondtrustee",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07IsReItsSIncomeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业总收入时间序列
    return w.wsd(security,"stm07_is_reits_sincome",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07IsReItsSIncome(security:list,*args,**kwargs):
    # 获取营业总收入
    return w.wss(security,"stm07_is_reits_sincome",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrTtM3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业总收入(TTM)_GSD时间序列
    return w.wsd(security,"gr_ttm3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrTtM3(security:list,*args,**kwargs):
    # 获取营业总收入(TTM)_GSD
    return w.wss(security,"gr_ttm3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClausePutOptionTriggerPriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取回售触发价时间序列
    return w.wsd(security,"clause_putoption_triggerprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClausePutOptionTriggerPrice(security:list,*args,**kwargs):
    # 获取回售触发价
    return w.wss(security,"clause_putoption_triggerprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrTtM2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业总收入(TTM)时间序列
    return w.wsd(security,"gr_ttm2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrTtM2(security:list,*args,**kwargs):
    # 获取营业总收入(TTM)
    return w.wss(security,"gr_ttm2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReserveRatioRMbSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取备付金比率(人民币)(旧)时间序列
    return w.wsd(security,"reserveratio_rmb",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReserveRatioRMb(security:list,*args,**kwargs):
    # 获取备付金比率(人民币)(旧)
    return w.wss(security,"reserveratio_rmb",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaGrTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业总收入(TTM)_PIT时间序列
    return w.wsd(security,"fa_gr_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaGrTtM(security:list,*args,**kwargs):
    # 获取营业总收入(TTM)_PIT
    return w.wss(security,"fa_gr_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReserveRatioFcNSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取备付金比率(外币)时间序列
    return w.wsd(security,"reserveratio_fc_n",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReserveRatioFcN(security:list,*args,**kwargs):
    # 获取备付金比率(外币)
    return w.wss(security,"reserveratio_fc_n",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsLocationSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资产所在地时间序列
    return w.wsd(security,"fund__reitslocation",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsLocation(security:list,*args,**kwargs):
    # 获取资产所在地
    return w.wss(security,"fund__reitslocation",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueTotalUnitSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行总份额时间序列
    return w.wsd(security,"issue_totalunit",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueTotalUnit(security:list,*args,**kwargs):
    # 获取发行总份额
    return w.wss(security,"issue_totalunit",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPrtFinancialBondSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取金融债市值时间序列
    return w.wsd(security,"prt_financialbond",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPrtFinancialBond(security:list,*args,**kwargs):
    # 获取金融债市值
    return w.wss(security,"prt_financialbond",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderTenderDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取招投标日期时间序列
    return w.wsd(security,"tender_tenderdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderTenderDate(security:list,*args,**kwargs):
    # 获取招投标日期
    return w.wss(security,"tender_tenderdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstDoCumTNumberSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取招标书编号时间序列
    return w.wsd(security,"tendrst_documtnumber",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstDoCumTNumber(security:list,*args,**kwargs):
    # 获取招标书编号
    return w.wss(security,"tendrst_documtnumber",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank702Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取不良贷款率_个人贷款及垫款时间序列
    return w.wsd(security,"stmnote_bank_702",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank702(security:list,*args,**kwargs):
    # 获取不良贷款率_个人贷款及垫款
    return w.wss(security,"stmnote_bank_702",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank703Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取不良贷款率_票据贴现时间序列
    return w.wsd(security,"stmnote_bank_703",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank703(security:list,*args,**kwargs):
    # 获取不良贷款率_票据贴现
    return w.wss(security,"stmnote_bank_703",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundMGrCompSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金管理人时间序列
    return w.wsd(security,"fund_mgrcomp",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundMGrComp(security:list,*args,**kwargs):
    # 获取基金管理人
    return w.wss(security,"fund_mgrcomp",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstPayAmountSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取缴款总金额时间序列
    return w.wsd(security,"tendrst_payamount",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstPayAmount(security:list,*args,**kwargs):
    # 获取缴款总金额
    return w.wss(security,"tendrst_payamount",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank704Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取不良贷款率_个人住房贷款时间序列
    return w.wsd(security,"stmnote_bank_704",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank704(security:list,*args,**kwargs):
    # 获取不良贷款率_个人住房贷款
    return w.wss(security,"stmnote_bank_704",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHandlingDateRsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取配股受理日时间序列
    return w.wsd(security,"handlingDate_rs",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHandlingDateRs(security:list,*args,**kwargs):
    # 获取配股受理日
    return w.wss(security,"handlingDate_rs",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank705Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取不良贷款率_个人消费贷款时间序列
    return w.wsd(security,"stmnote_bank_705",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank705(security:list,*args,**kwargs):
    # 获取不良贷款率_个人消费贷款
    return w.wss(security,"stmnote_bank_705",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank706Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取不良贷款率_信用卡应收账款时间序列
    return w.wsd(security,"stmnote_bank_706",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank706(security:list,*args,**kwargs):
    # 获取不良贷款率_信用卡应收账款
    return w.wss(security,"stmnote_bank_706",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank707Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取不良贷款率_经营性贷款时间序列
    return w.wsd(security,"stmnote_bank_707",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank707(security:list,*args,**kwargs):
    # 获取不良贷款率_经营性贷款
    return w.wss(security,"stmnote_bank_707",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank708Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取不良贷款率_汽车贷款时间序列
    return w.wsd(security,"stmnote_bank_708",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank708(security:list,*args,**kwargs):
    # 获取不良贷款率_汽车贷款
    return w.wss(security,"stmnote_bank_708",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank709Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取不良贷款率_其他个人贷款时间序列
    return w.wsd(security,"stmnote_bank_709",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank709(security:list,*args,**kwargs):
    # 获取不良贷款率_其他个人贷款
    return w.wss(security,"stmnote_bank_709",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRecEivStOThSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取其它应收款_GSD时间序列
    return w.wsd(security,"wgsd_receiv_st_oth",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRecEivStOTh(security:list,*args,**kwargs):
    # 获取其它应收款_GSD
    return w.wss(security,"wgsd_receiv_st_oth",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYieldCsi1Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取估价收益率(中证指数)时间序列
    return w.wsd(security,"yield_csi1",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYieldCsi1(security:list,*args,**kwargs):
    # 获取估价收益率(中证指数)
    return w.wss(security,"yield_csi1",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank430Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取损失-金额时间序列
    return w.wsd(security,"stmnote_bank_430",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank430(security:list,*args,**kwargs):
    # 获取损失-金额
    return w.wss(security,"stmnote_bank_430",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank40Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取可疑-金额时间序列
    return w.wsd(security,"stmnote_bank_40",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank40(security:list,*args,**kwargs):
    # 获取可疑-金额
    return w.wss(security,"stmnote_bank_40",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundMaturityDate2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金到期日时间序列
    return w.wsd(security,"fund_maturitydate_2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundMaturityDate2(security:list,*args,**kwargs):
    # 获取基金到期日
    return w.wss(security,"fund_maturitydate_2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFtDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取开始交易日时间序列
    return w.wsd(security,"ftdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFtDate(security:list,*args,**kwargs):
    # 获取开始交易日
    return w.wss(security,"ftdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFtDateNewSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取开始交易日(支持历史)时间序列
    return w.wsd(security,"ftdate_new",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFtDateNew(security:list,*args,**kwargs):
    # 获取开始交易日(支持历史)
    return w.wss(security,"ftdate_new",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLastTradeDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最后交易日时间序列
    return w.wsd(security,"lasttrade_date",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLastTradeDate(security:list,*args,**kwargs):
    # 获取最后交易日
    return w.wss(security,"lasttrade_date",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLtDateNewSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最后交易日(支持历史)时间序列
    return w.wsd(security,"ltdate_new",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLtDateNew(security:list,*args,**kwargs):
    # 获取最后交易日(支持历史)
    return w.wss(security,"ltdate_new",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDIncPreTaxSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取除税前利润_GSD时间序列
    return w.wsd(security,"wgsd_inc_pretax",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDIncPreTax(security:list,*args,**kwargs):
    # 获取除税前利润_GSD
    return w.wss(security,"wgsd_inc_pretax",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRateDefaultCsiSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取隐含违约率(中证指数)时间序列
    return w.wsd(security,"rate_default_csi",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRateDefaultCsi(security:list,*args,**kwargs):
    # 获取隐含违约率(中证指数)
    return w.wss(security,"rate_default_csi",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank37Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取次级-金额时间序列
    return w.wsd(security,"stmnote_bank_37",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank37(security:list,*args,**kwargs):
    # 获取次级-金额
    return w.wss(security,"stmnote_bank_37",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPreNameSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取证券曾用名时间序列
    return w.wsd(security,"prename",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPreName(security:list,*args,**kwargs):
    # 获取证券曾用名
    return w.wss(security,"prename",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteIncomeTax5Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取递延所得税时间序列
    return w.wsd(security,"stmnote_incometax_5",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteIncomeTax5(security:list,*args,**kwargs):
    # 获取递延所得税
    return w.wss(security,"stmnote_incometax_5",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssueAnnCeDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取配股公告日时间序列
    return w.wsd(security,"rightsissue_anncedate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssueAnnCeDate(security:list,*args,**kwargs):
    # 获取配股公告日
    return w.wss(security,"rightsissue_anncedate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLatelyRdBtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最新报告期时间序列
    return w.wsd(security,"latelyrd_bt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLatelyRdBt(security:list,*args,**kwargs):
    # 获取最新报告期
    return w.wss(security,"latelyrd_bt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank701Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取不良贷款率_企业贷款及垫款时间序列
    return w.wsd(security,"stmnote_bank_701",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank701(security:list,*args,**kwargs):
    # 获取不良贷款率_企业贷款及垫款
    return w.wss(security,"stmnote_bank_701",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReInSurIncSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取分保费收入时间序列
    return w.wsd(security,"reinsur_inc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReInSurInc(security:list,*args,**kwargs):
    # 获取分保费收入
    return w.wss(security,"reinsur_inc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank431Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取非计息负债时间序列
    return w.wsd(security,"stmnote_bank_431",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank431(security:list,*args,**kwargs):
    # 获取非计息负债
    return w.wss(security,"stmnote_bank_431",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getArdIsSalesSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总营业收入(公布值)_GSD时间序列
    return w.wsd(security,"ard_is_sales",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getArdIsSales(security:list,*args,**kwargs):
    # 获取总营业收入(公布值)_GSD
    return w.wss(security,"ard_is_sales",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCorpTeamStabilitySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取团队稳定性时间序列
    return w.wsd(security,"fund_corp_teamstability",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCorpTeamStability(security:list,*args,**kwargs):
    # 获取团队稳定性
    return w.wss(security,"fund_corp_teamstability",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteOthers7632Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取仓储运输费(销售费用)时间序列
    return w.wsd(security,"stmnote_others_7632",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteOthers7632(security:list,*args,**kwargs):
    # 获取仓储运输费(销售费用)
    return w.wss(security,"stmnote_others_7632",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssueDeputyUndRSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取配股分销商时间序列
    return w.wsd(security,"rightsissue_deputyundr",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssueDeputyUndR(security:list,*args,**kwargs):
    # 获取配股分销商
    return w.wss(security,"rightsissue_deputyundr",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPrtCorporateBondsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取企业债市值时间序列
    return w.wsd(security,"prt_corporatebonds",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPrtCorporateBonds(security:list,*args,**kwargs):
    # 获取企业债市值
    return w.wss(security,"prt_corporatebonds",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareOtcTradableSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取流通三板股时间序列
    return w.wsd(security,"share_otctradable",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareOtcTradable(security:list,*args,**kwargs):
    # 获取流通三板股
    return w.wss(security,"share_otctradable",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCloseDayIllUsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取封闭期说明时间序列
    return w.wsd(security,"fund_closedayillus",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCloseDayIllUs(security:list,*args,**kwargs):
    # 获取封闭期说明
    return w.wss(security,"fund_closedayillus",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGGBo01006Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取监事出席率时间序列
    return w.wsd(security,"esg_gbo01006",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGGBo01006(security:list,*args,**kwargs):
    # 获取监事出席率
    return w.wss(security,"esg_gbo01006",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundOpenDayIllUsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取开放日说明时间序列
    return w.wsd(security,"fund_opendayillus",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundOpenDayIllUs(security:list,*args,**kwargs):
    # 获取开放日说明
    return w.wss(security,"fund_opendayillus",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCorpFundManagersNoSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金经理数时间序列
    return w.wsd(security,"fund_corp_fundmanagersno",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCorpFundManagersNo(security:list,*args,**kwargs):
    # 获取基金经理数
    return w.wss(security,"fund_corp_fundmanagersno",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCbResultSuCrateOnLSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取网上中签率时间序列
    return w.wsd(security,"cb_result_sucrateonl",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCbResultSuCrateOnL(security:list,*args,**kwargs):
    # 获取网上中签率
    return w.wss(security,"cb_result_sucrateonl",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYieldCnBdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取估价收益率(%)(中债)时间序列
    return w.wsd(security,"yield_cnbd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYieldCnBd(security:list,*args,**kwargs):
    # 获取估价收益率(%)(中债)
    return w.wss(security,"yield_cnbd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPrimaryDealersSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取一级交易商时间序列
    return w.wsd(security,"fund_primarydealers",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPrimaryDealers(security:list,*args,**kwargs):
    # 获取一级交易商
    return w.wss(security,"fund_primarydealers",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssuePayEnddateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取缴款终止日时间序列
    return w.wsd(security,"rightsissue_payenddate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssuePayEnddate(security:list,*args,**kwargs):
    # 获取缴款终止日
    return w.wss(security,"rightsissue_payenddate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCounselorSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取律师事务所时间序列
    return w.wsd(security,"fund_counselor",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCounselor(security:list,*args,**kwargs):
    # 获取律师事务所
    return w.wss(security,"fund_counselor",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerIndexAlphaSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取Alpha(基金经理指数,算术平均)时间序列
    return w.wsd(security,"fund_managerindex_alpha",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerIndexAlpha(security:list,*args,**kwargs):
    # 获取Alpha(基金经理指数,算术平均)
    return w.wss(security,"fund_managerindex_alpha",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseConversion2BondLotSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取未转股余额时间序列
    return w.wsd(security,"clause_conversion2_bondlot",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseConversion2BondLot(security:list,*args,**kwargs):
    # 获取未转股余额
    return w.wss(security,"clause_conversion2_bondlot",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerIndexWeightAlphaSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取Alpha(基金经理指数,规模加权)时间序列
    return w.wsd(security,"fund_managerindex_weight_alpha",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundManagerIndexWeightAlpha(security:list,*args,**kwargs):
    # 获取Alpha(基金经理指数,规模加权)
    return w.wss(security,"fund_managerindex_weight_alpha",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareRTdBAnceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取未流通数量时间序列
    return w.wsd(security,"share_rtd_bance",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareRTdBAnce(security:list,*args,**kwargs):
    # 获取未流通数量
    return w.wss(security,"share_rtd_bance",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundForeignCustodianSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取境外托管人时间序列
    return w.wsd(security,"fund_foreigncustodian",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundForeignCustodian(security:list,*args,**kwargs):
    # 获取境外托管人
    return w.wss(security,"fund_foreigncustodian",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPrtConvertibleBondSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取可转债市值时间序列
    return w.wsd(security,"prt_convertiblebond",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPrtConvertibleBond(security:list,*args,**kwargs):
    # 获取可转债市值
    return w.wss(security,"prt_convertiblebond",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGGBo01001Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取董事会规模时间序列
    return w.wsd(security,"esg_gbo01001",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGGBo01001(security:list,*args,**kwargs):
    # 获取董事会规模
    return w.wss(security,"esg_gbo01001",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEwa02003Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取废水处理量时间序列
    return w.wsd(security,"esg_ewa02003",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEwa02003(security:list,*args,**kwargs):
    # 获取废水处理量
    return w.wss(security,"esg_ewa02003",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSpreadYieldCnBdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取点差收益率(中债)时间序列
    return w.wsd(security,"spreadyield_cnbd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSpreadYieldCnBd(security:list,*args,**kwargs):
    # 获取点差收益率(中债)
    return w.wss(security,"spreadyield_cnbd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstReferYieldSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取参考收益率时间序列
    return w.wsd(security,"tendrst_referyield",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstReferYield(security:list,*args,**kwargs):
    # 获取参考收益率
    return w.wss(security,"tendrst_referyield",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCustodianBankSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金托管人时间序列
    return w.wsd(security,"fund_custodianbank",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCustodianBank(security:list,*args,**kwargs):
    # 获取基金托管人
    return w.wss(security,"fund_custodianbank",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCbResultSuCrateOffSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取网下中签率时间序列
    return w.wsd(security,"cb_result_sucrateoff",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCbResultSuCrateOff(security:list,*args,**kwargs):
    # 获取网下中签率
    return w.wss(security,"cb_result_sucrateoff",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssuersCoreSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取(停止)发行人评分时间序列
    return w.wsd(security,"issuerscore",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssuersCore(security:list,*args,**kwargs):
    # 获取(停止)发行人评分
    return w.wss(security,"issuerscore",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueAnnouncedAteSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行公告日时间序列
    return w.wsd(security,"issue_announcedate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueAnnouncedAte(security:list,*args,**kwargs):
    # 获取发行公告日
    return w.wss(security,"issue_announcedate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHighPerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间最高价时间序列
    return w.wsd(security,"high_per",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHighPer(security:list,*args,**kwargs):
    # 获取区间最高价
    return w.wss(security,"high_per",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoYCfSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取现金净流量(同比增长率)时间序列
    return w.wsd(security,"yoycf",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoYCf(security:list,*args,**kwargs):
    # 获取现金净流量(同比增长率)
    return w.wss(security,"yoycf",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUsHighSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取标的最高价时间序列
    return w.wsd(security,"us_high",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUsHigh(security:list,*args,**kwargs):
    # 获取标的最高价
    return w.wss(security,"us_high",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrossProfitMarginTtM2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售毛利率(TTM)时间序列
    return w.wsd(security,"grossprofitmargin_ttm2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrossProfitMarginTtM2(security:list,*args,**kwargs):
    # 获取销售毛利率(TTM)
    return w.wss(security,"grossprofitmargin_ttm2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrossProfitMarginSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售毛利率时间序列
    return w.wsd(security,"grossprofitmargin",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrossProfitMargin(security:list,*args,**kwargs):
    # 获取销售毛利率
    return w.wss(security,"grossprofitmargin",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoTutoringStartDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取辅导备案日时间序列
    return w.wsd(security,"ipo_tutoring_startdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoTutoringStartDate(security:list,*args,**kwargs):
    # 获取辅导备案日
    return w.wss(security,"ipo_tutoring_startdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoSubmitRegisTDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取提交注册日时间序列
    return w.wsd(security,"ipo_submit_regist_date",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoSubmitRegisTDate(security:list,*args,**kwargs):
    # 获取提交注册日
    return w.wss(security,"ipo_submit_regist_date",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetProfitMarginTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售净利率(TTM,只有最新数据)时间序列
    return w.wsd(security,"netprofitmargin_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetProfitMarginTtM(security:list,*args,**kwargs):
    # 获取销售净利率(TTM,只有最新数据)
    return w.wss(security,"netprofitmargin_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaNetProfitMarginTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售净利率(TTM)_PIT时间序列
    return w.wsd(security,"fa_netprofitmargin_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaNetProfitMarginTtM(security:list,*args,**kwargs):
    # 获取销售净利率(TTM)_PIT
    return w.wss(security,"fa_netprofitmargin_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetProfitMarginTtM3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售净利率(TTM)_GSD时间序列
    return w.wsd(security,"netprofitmargin_ttm3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetProfitMarginTtM3(security:list,*args,**kwargs):
    # 获取销售净利率(TTM)_GSD
    return w.wss(security,"netprofitmargin_ttm3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDNetProfitMarginSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售净利率_GSD时间序列
    return w.wsd(security,"wgsd_netprofitmargin",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDNetProfitMargin(security:list,*args,**kwargs):
    # 获取销售净利率_GSD
    return w.wss(security,"wgsd_netprofitmargin",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetProfitMarginTtM2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售净利率(TTM)时间序列
    return w.wsd(security,"netprofitmargin_ttm2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetProfitMarginTtM2(security:list,*args,**kwargs):
    # 获取销售净利率(TTM)
    return w.wss(security,"netprofitmargin_ttm2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrossProfitMarginSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售毛利率_GSD时间序列
    return w.wsd(security,"wgsd_grossprofitmargin",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrossProfitMargin(security:list,*args,**kwargs):
    # 获取销售毛利率_GSD
    return w.wss(security,"wgsd_grossprofitmargin",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetProfitMarginSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售净利率时间序列
    return w.wsd(security,"netprofitmargin",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetProfitMargin(security:list,*args,**kwargs):
    # 获取销售净利率
    return w.wss(security,"netprofitmargin",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfSellVolSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间流出量时间序列
    return w.wsd(security,"mf_sell_vol",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfSellVol(security:list,*args,**kwargs):
    # 获取区间流出量
    return w.wss(security,"mf_sell_vol",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfSellAmtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间流出额时间序列
    return w.wsd(security,"mf_sell_amt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfSellAmt(security:list,*args,**kwargs):
    # 获取区间流出额
    return w.wss(security,"mf_sell_amt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfBuyVolSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间流入量时间序列
    return w.wsd(security,"mf_buy_vol",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfBuyVol(security:list,*args,**kwargs):
    # 获取区间流入量
    return w.wss(security,"mf_buy_vol",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfBuyAmtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间流入额时间序列
    return w.wsd(security,"mf_buy_amt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfBuyAmt(security:list,*args,**kwargs):
    # 获取区间流入额
    return w.wss(security,"mf_buy_amt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBeta60MSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取BETA值(最近60个月)时间序列
    return w.wsd(security,"beta_60m",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBeta60M(security:list,*args,**kwargs):
    # 获取BETA值(最近60个月)
    return w.wss(security,"beta_60m",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBeta24MSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取BETA值(最近24个月)时间序列
    return w.wsd(security,"beta_24m",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBeta24M(security:list,*args,**kwargs):
    # 获取BETA值(最近24个月)
    return w.wss(security,"beta_24m",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBeta100WSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取BETA值(最近100周)时间序列
    return w.wsd(security,"beta_100w",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBeta100W(security:list,*args,**kwargs):
    # 获取BETA值(最近100周)
    return w.wss(security,"beta_100w",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskAnnualPhaSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取Alpha(年化)时间序列
    return w.wsd(security,"risk_annualpha",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskAnnualPha(security:list,*args,**kwargs):
    # 获取Alpha(年化)
    return w.wss(security,"risk_annualpha",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskAlphaSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取Alpha_FUND时间序列
    return w.wsd(security,"risk_alpha",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskAlpha(security:list,*args,**kwargs):
    # 获取Alpha_FUND
    return w.wss(security,"risk_alpha",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueFirstPriceDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取首个定价日时间序列
    return w.wsd(security,"issue_firstpricedate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueFirstPriceDate(security:list,*args,**kwargs):
    # 获取首个定价日
    return w.wss(security,"issue_firstpricedate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSpread2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取行权后利差时间序列
    return w.wsd(security,"spread2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSpread2(security:list,*args,**kwargs):
    # 获取行权后利差
    return w.wss(security,"spread2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrossProfitMarginTtM3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售毛利率(TTM)_GSD时间序列
    return w.wsd(security,"grossprofitmargin_ttm3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrossProfitMarginTtM3(security:list,*args,**kwargs):
    # 获取销售毛利率(TTM)_GSD
    return w.wss(security,"grossprofitmargin_ttm3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrossProfitMarginTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售毛利率(TTM,只有最新数据)时间序列
    return w.wsd(security,"grossprofitmargin_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrossProfitMarginTtM(security:list,*args,**kwargs):
    # 获取销售毛利率(TTM,只有最新数据)
    return w.wss(security,"grossprofitmargin_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoPubOfFrDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取招股公告日时间序列
    return w.wsd(security,"ipo_puboffrdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoPubOfFrDate(security:list,*args,**kwargs):
    # 获取招股公告日
    return w.wss(security,"ipo_puboffrdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMunicipalBondWindSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取是否城投债(Wind)时间序列
    return w.wsd(security,"municipalbondWind",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMunicipalBondWind(security:list,*args,**kwargs):
    # 获取是否城投债(Wind)
    return w.wss(security,"municipalbondWind",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMunicipalBondSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取是否城投债时间序列
    return w.wsd(security,"municipalbond",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMunicipalBond(security:list,*args,**kwargs):
    # 获取是否城投债
    return w.wss(security,"municipalbond",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMunicipalBondyYSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取是否城投债(YY)时间序列
    return w.wsd(security,"municipalbondYY",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMunicipalBondyY(security:list,*args,**kwargs):
    # 获取是否城投债(YY)
    return w.wss(security,"municipalbondYY",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSubordinateOrNotSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取是否次级债时间序列
    return w.wsd(security,"subordinateornot",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSubordinateOrNot(security:list,*args,**kwargs):
    # 获取是否次级债
    return w.wss(security,"subordinateornot",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCompPreNameSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取公司曾用名时间序列
    return w.wsd(security,"compprename",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCompPreName(security:list,*args,**kwargs):
    # 获取公司曾用名
    return w.wss(security,"compprename",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMrgShortVolRepaySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取融券偿还量时间序列
    return w.wsd(security,"mrg_short_vol_repay",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMrgShortVolRepay(security:list,*args,**kwargs):
    # 获取融券偿还量
    return w.wss(security,"mrg_short_vol_repay",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMrgShortVolSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取融券卖出量时间序列
    return w.wsd(security,"mrg_short_vol",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMrgShortVol(security:list,*args,**kwargs):
    # 获取融券卖出量
    return w.wss(security,"mrg_short_vol",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPerpetualOrNotSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取是否永续债时间序列
    return w.wsd(security,"perpetualornot",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPerpetualOrNot(security:list,*args,**kwargs):
    # 获取是否永续债
    return w.wss(security,"perpetualornot",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaGrossProfitMarginTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售毛利率(TTM)_PIT时间序列
    return w.wsd(security,"fa_grossprofitmargin_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaGrossProfitMarginTtM(security:list,*args,**kwargs):
    # 获取销售毛利率(TTM)_PIT
    return w.wss(security,"fa_grossprofitmargin_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGSpc01002Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取客户满意度时间序列
    return w.wsd(security,"esg_spc01002",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGSpc01002(security:list,*args,**kwargs):
    # 获取客户满意度
    return w.wss(security,"esg_spc01002",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDIsCloserSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取信息披露人时间序列
    return w.wsd(security,"discloser",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDIsCloser(security:list,*args,**kwargs):
    # 获取信息披露人
    return w.wss(security,"discloser",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMrgLongRepaySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取融资偿还额时间序列
    return w.wsd(security,"mrg_long_repay",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMrgLongRepay(security:list,*args,**kwargs):
    # 获取融资偿还额
    return w.wss(security,"mrg_long_repay",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMrgLongAmtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取融资买入额时间序列
    return w.wsd(security,"mrg_long_amt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMrgLongAmt(security:list,*args,**kwargs):
    # 获取融资买入额
    return w.wss(security,"mrg_long_amt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoDistOrSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取首发分销商时间序列
    return w.wsd(security,"ipo_distor",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoDistOr(security:list,*args,**kwargs):
    # 获取首发分销商
    return w.wss(security,"ipo_distor",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueLiStanceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取上市公告日时间序列
    return w.wsd(security,"issue_listance",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueLiStance(security:list,*args,**kwargs):
    # 获取上市公告日
    return w.wss(security,"issue_listance",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoPDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取网下定价日时间序列
    return w.wsd(security,"ipo_pDate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoPDate(security:list,*args,**kwargs):
    # 获取网下定价日
    return w.wss(security,"ipo_pDate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaSalesToCostTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售成本率(TTM)_PIT时间序列
    return w.wsd(security,"fa_salestocost_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaSalesToCostTtM(security:list,*args,**kwargs):
    # 获取销售成本率(TTM)_PIT
    return w.wss(security,"fa_salestocost_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDCogsToSalesSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售成本率_GSD时间序列
    return w.wsd(security,"wgsd_cogstosales",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDCogsToSales(security:list,*args,**kwargs):
    # 获取销售成本率_GSD
    return w.wss(security,"wgsd_cogstosales",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCogsToSalesSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售成本率时间序列
    return w.wsd(security,"cogstosales",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCogsToSales(security:list,*args,**kwargs):
    # 获取销售成本率
    return w.wss(security,"cogstosales",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReportCurSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取记账本位币时间序列
    return w.wsd(security,"report_cur",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReportCur(security:list,*args,**kwargs):
    # 获取记账本位币
    return w.wss(security,"report_cur",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsEnddateOfAssetClearingSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取清算结束日时间序列
    return w.wsd(security,"abs_enddateofassetclearing",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsEnddateOfAssetClearing(security:list,*args,**kwargs):
    # 获取清算结束日
    return w.wss(security,"abs_enddateofassetclearing",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrowthGrSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业总收入(N年,增长率)时间序列
    return w.wsd(security,"growth_gr",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrowthGr(security:list,*args,**kwargs):
    # 获取营业总收入(N年,增长率)
    return w.wss(security,"growth_gr",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPeTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取市盈率PE(TTM)_PIT时间序列
    return w.wsd(security,"pe_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPeTtM(security:list,*args,**kwargs):
    # 获取市盈率PE(TTM)_PIT
    return w.wss(security,"pe_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyBookkeeperSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取账簿管理人(海外)时间序列
    return w.wsd(security,"agency_bookkeeper",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyBookkeeper(security:list,*args,**kwargs):
    # 获取账簿管理人(海外)
    return w.wss(security,"agency_bookkeeper",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoWeightedPeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取首发市盈率(加权)时间序列
    return w.wsd(security,"ipo_weightedpe",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoWeightedPe(security:list,*args,**kwargs):
    # 获取首发市盈率(加权)
    return w.wss(security,"ipo_weightedpe",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFiscalDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取会计年结日时间序列
    return w.wsd(security,"fiscaldate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFiscalDate(security:list,*args,**kwargs):
    # 获取会计年结日
    return w.wss(security,"fiscaldate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLegalRepresentativeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取法定代表人(支持历史)时间序列
    return w.wsd(security,"legalrepresentative",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLegalRepresentative(security:list,*args,**kwargs):
    # 获取法定代表人(支持历史)
    return w.wss(security,"legalrepresentative",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoPbSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行市净率时间序列
    return w.wsd(security,"ipo_pb",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoPb(security:list,*args,**kwargs):
    # 获取发行市净率
    return w.wss(security,"ipo_pb",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getChairmanSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取法定代表人时间序列
    return w.wsd(security,"chairman",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getChairman(security:list,*args,**kwargs):
    # 获取法定代表人
    return w.wss(security,"chairman",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMamVSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取备考总市值(并购后)时间序列
    return w.wsd(security,"mamv",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMamV(security:list,*args,**kwargs):
    # 获取备考总市值(并购后)
    return w.wss(security,"mamv",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValMvSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取指数总市值时间序列
    return w.wsd(security,"val_mv",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValMv(security:list,*args,**kwargs):
    # 获取指数总市值
    return w.wss(security,"val_mv",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMvRefSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取参考总市值时间序列
    return w.wsd(security,"mv_ref",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMvRef(security:list,*args,**kwargs):
    # 获取参考总市值
    return w.wss(security,"mv_ref",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalImpliedYieldSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取隐含收益率时间序列
    return w.wsd(security,"anal_impliedyield",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalImpliedYield(security:list,*args,**kwargs):
    # 获取隐含收益率
    return w.wss(security,"anal_impliedyield",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsoluteProfitMonthPerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取盈利百分比时间序列
    return w.wsd(security,"absolute_profitmonthper",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsoluteProfitMonthPer(security:list,*args,**kwargs):
    # 获取盈利百分比
    return w.wss(security,"absolute_profitmonthper",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStyleInvConcentrationSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取投资集中度时间序列
    return w.wsd(security,"style_invconcentration",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStyleInvConcentration(security:list,*args,**kwargs):
    # 获取投资集中度
    return w.wss(security,"style_invconcentration",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaRoaTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资产回报率(TTM)_PIT时间序列
    return w.wsd(security,"fa_roa_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaRoaTtM(security:list,*args,**kwargs):
    # 获取资产回报率(TTM)_PIT
    return w.wss(security,"fa_roa_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteEoItems9Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取资金占用费时间序列
    return w.wsd(security,"stmnote_Eoitems_9",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteEoItems9(security:list,*args,**kwargs):
    # 获取资金占用费
    return w.wss(security,"stmnote_Eoitems_9",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDExoDSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他特殊项_GSD时间序列
    return w.wsd(security,"wgsd_exod",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDExoD(security:list,*args,**kwargs):
    # 获取其他特殊项_GSD
    return w.wss(security,"wgsd_exod",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSettlePerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间结算价时间序列
    return w.wsd(security,"settle_per",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSettlePer(security:list,*args,**kwargs):
    # 获取区间结算价
    return w.wss(security,"settle_per",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCouponDateTxtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取付息日说明时间序列
    return w.wsd(security,"coupondatetxt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCouponDateTxt(security:list,*args,**kwargs):
    # 获取付息日说明
    return w.wss(security,"coupondatetxt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPutOiSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取认沽持仓量时间序列
    return w.wsd(security,"putoi",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPutOi(security:list,*args,**kwargs):
    # 获取认沽持仓量
    return w.wss(security,"putoi",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCallOiSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取认购持仓量时间序列
    return w.wsd(security,"calloi",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCallOi(security:list,*args,**kwargs):
    # 获取认购持仓量
    return w.wss(security,"calloi",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOptionOiSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取品种持仓量时间序列
    return w.wsd(security,"optionoi",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOptionOi(security:list,*args,**kwargs):
    # 获取品种持仓量
    return w.wss(security,"optionoi",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStyleComMisAccountSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取佣金规模比时间序列
    return w.wsd(security,"style_commisaccount",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStyleComMisAccount(security:list,*args,**kwargs):
    # 获取佣金规模比
    return w.wss(security,"style_commisaccount",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEmbeddedOptSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取是否含权债时间序列
    return w.wsd(security,"embeddedopt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEmbeddedOpt(security:list,*args,**kwargs):
    # 获取是否含权债
    return w.wss(security,"embeddedopt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPrepaymentDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取提前还本日时间序列
    return w.wsd(security,"prepaymentdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPrepaymentDate(security:list,*args,**kwargs):
    # 获取提前还本日
    return w.wss(security,"prepaymentdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAvgDiscountPerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间均贴水时间序列
    return w.wsd(security,"avg_discount_per",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAvgDiscountPer(security:list,*args,**kwargs):
    # 获取区间均贴水
    return w.wss(security,"avg_discount_per",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAlpha2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取Alpha时间序列
    return w.wsd(security,"alpha2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAlpha2(security:list,*args,**kwargs):
    # 获取Alpha
    return w.wss(security,"alpha2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPsTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取市销率PS(TTM)_PIT时间序列
    return w.wsd(security,"ps_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPsTtM(security:list,*args,**kwargs):
    # 获取市销率PS(TTM)_PIT
    return w.wss(security,"ps_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrowthGcSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业总成本(N年,增长率)时间序列
    return w.wsd(security,"growth_gc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrowthGc(security:list,*args,**kwargs):
    # 获取营业总成本(N年,增长率)
    return w.wss(security,"growth_gc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrowthProfitToSalesSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售利润率(N年,增长率)时间序列
    return w.wsd(security,"growth_profittosales",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrowthProfitToSales(security:list,*args,**kwargs):
    # 获取销售利润率(N年,增长率)
    return w.wss(security,"growth_profittosales",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthSales1YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总营业收入(近1年增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_sales_1y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthSales1Y(security:list,*args,**kwargs):
    # 获取总营业收入(近1年增长率)_GSD
    return w.wss(security,"wgsd_growth_sales_1y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getThetaExChSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取Theta(交易所)时间序列
    return w.wsd(security,"theta_exch",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getThetaExCh(security:list,*args,**kwargs):
    # 获取Theta(交易所)
    return w.wss(security,"theta_exch",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getThetaSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取Theta时间序列
    return w.wsd(security,"theta",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTheta(security:list,*args,**kwargs):
    # 获取Theta
    return w.wss(security,"theta",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthSales3YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总营业收入(近3年增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_sales_3y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthSales3Y(security:list,*args,**kwargs):
    # 获取总营业收入(近3年增长率)_GSD
    return w.wss(security,"wgsd_growth_sales_3y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthBpS1YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股净资产(近1年增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_bps_1y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthBpS1Y(security:list,*args,**kwargs):
    # 获取每股净资产(近1年增长率)_GSD
    return w.wss(security,"wgsd_growth_bps_1y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRedemptionRegBeginningSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取兑付登记日时间序列
    return w.wsd(security,"redemption_regbeginning",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRedemptionRegBeginning(security:list,*args,**kwargs):
    # 获取兑付登记日
    return w.wss(security,"redemption_regbeginning",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGammaExChSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取Gamma(交易所)时间序列
    return w.wsd(security,"gamma_exch",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGammaExCh(security:list,*args,**kwargs):
    # 获取Gamma(交易所)
    return w.wss(security,"gamma_exch",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDeltaExChSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取Delta(交易所)时间序列
    return w.wsd(security,"delta_exch",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDeltaExCh(security:list,*args,**kwargs):
    # 获取Delta(交易所)
    return w.wss(security,"delta_exch",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDeltaSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取Delta时间序列
    return w.wsd(security,"delta",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDelta(security:list,*args,**kwargs):
    # 获取Delta
    return w.wss(security,"delta",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthBpS3YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股净资产(近3年增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_bps_3y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthBpS3Y(security:list,*args,**kwargs):
    # 获取每股净资产(近3年增长率)_GSD
    return w.wss(security,"wgsd_growth_bps_3y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoRegisTDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取注册成功日(证监会审核批文日)时间序列
    return w.wsd(security,"ipo_regist_date",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoRegisTDate(security:list,*args,**kwargs):
    # 获取注册成功日(证监会审核批文日)
    return w.wss(security,"ipo_regist_date",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthGrSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业总收入(N年,增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_gr",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthGr(security:list,*args,**kwargs):
    # 获取营业总收入(N年,增长率)_GSD
    return w.wss(security,"wgsd_growth_gr",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthGcSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业总成本(N年,增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_gc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthGc(security:list,*args,**kwargs):
    # 获取营业总成本(N年,增长率)_GSD
    return w.wss(security,"wgsd_growth_gc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoMrQDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取申报基准日时间序列
    return w.wsd(security,"ipo_mrqdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoMrQDate(security:list,*args,**kwargs):
    # 获取申报基准日
    return w.wss(security,"ipo_mrqdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthProfitToSalesSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售利润率(N年,增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_profittosales",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthProfitToSales(security:list,*args,**kwargs):
    # 获取销售利润率(N年,增长率)_GSD
    return w.wss(security,"wgsd_growth_profittosales",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEmployeeBoardSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取董事会人数时间序列
    return w.wsd(security,"employee_board",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEmployeeBoard(security:list,*args,**kwargs):
    # 获取董事会人数
    return w.wss(security,"employee_board",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGammaSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取Gamma时间序列
    return w.wsd(security,"gamma",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGamma(security:list,*args,**kwargs):
    # 获取Gamma
    return w.wss(security,"gamma",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsStartDateOfAssetClearingSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取清算起始日时间序列
    return w.wsd(security,"abs_startdateofassetclearing",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsStartDateOfAssetClearing(security:list,*args,**kwargs):
    # 获取清算起始日
    return w.wss(security,"abs_startdateofassetclearing",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsCutoffDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取初始起算日时间序列
    return w.wsd(security,"abs_cutoffdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsCutoffDate(security:list,*args,**kwargs):
    # 获取初始起算日
    return w.wss(security,"abs_cutoffdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsFirstPaymentDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取首次支付日时间序列
    return w.wsd(security,"abs_firstpaymentdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsFirstPaymentDate(security:list,*args,**kwargs):
    # 获取首次支付日
    return w.wss(security,"abs_firstpaymentdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoYbPsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股净资产(相对年初增长率)时间序列
    return w.wsd(security,"yoybps",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoYbPs(security:list,*args,**kwargs):
    # 获取每股净资产(相对年初增长率)
    return w.wss(security,"yoybps",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDYoYbPsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股净资产(相对年初增长率)_GSD时间序列
    return w.wsd(security,"wgsd_yoybps",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDYoYbPs(security:list,*args,**kwargs):
    # 获取每股净资产(相对年初增长率)_GSD
    return w.wss(security,"wgsd_yoybps",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs75Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取未分配利润_FUND时间序列
    return w.wsd(security,"stm_bs_75",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs75(security:list,*args,**kwargs):
    # 获取未分配利润_FUND
    return w.wss(security,"stm_bs_75",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsUndIsTriRProfitSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取未分配利润时间序列
    return w.wsd(security,"stm07_bs_reits_undistrirprofit",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsUndIsTriRProfit(security:list,*args,**kwargs):
    # 获取未分配利润
    return w.wss(security,"stm07_bs_reits_undistrirprofit",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsSurplusSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取盈余公积金时间序列
    return w.wsd(security,"stm07_bs_reits_surplus",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsSurplus(security:list,*args,**kwargs):
    # 获取盈余公积金
    return w.wss(security,"stm07_bs_reits_surplus",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsCapitalReserveSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资本公积金时间序列
    return w.wsd(security,"stm07_bs_reits_capitalreserve",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsCapitalReserve(security:list,*args,**kwargs):
    # 获取资本公积金
    return w.wss(security,"stm07_bs_reits_capitalreserve",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsOtherPayableSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他应付款(合计)时间序列
    return w.wsd(security,"stm07_bs_reits_otherpayable",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsOtherPayable(security:list,*args,**kwargs):
    # 获取其他应付款(合计)
    return w.wss(security,"stm07_bs_reits_otherpayable",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsCumulativeDefaultRateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取累计违约率时间序列
    return w.wsd(security,"abs_cumulativedefaultrate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsCumulativeDefaultRate(security:list,*args,**kwargs):
    # 获取累计违约率
    return w.wss(security,"abs_cumulativedefaultrate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsDelinquencyRateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取严重拖欠率时间序列
    return w.wsd(security,"abs_delinquencyrate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsDelinquencyRate(security:list,*args,**kwargs):
    # 获取严重拖欠率
    return w.wss(security,"abs_delinquencyrate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssuerBankTypeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行人(银行)类型时间序列
    return w.wsd(security,"issuer_banktype",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssuerBankType(security:list,*args,**kwargs):
    # 获取发行人(银行)类型
    return w.wss(security,"issuer_banktype",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaInvTurnTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取存货周转率(TTM)_PIT时间序列
    return w.wsd(security,"fa_invturn_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaInvTurnTtM(security:list,*args,**kwargs):
    # 获取存货周转率(TTM)_PIT
    return w.wss(security,"fa_invturn_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInvTurnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取存货周转率时间序列
    return w.wsd(security,"invturn",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInvTurn(security:list,*args,**kwargs):
    # 获取存货周转率
    return w.wss(security,"invturn",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsCreditNormalSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取承销团成员时间序列
    return w.wsd(security,"abs_creditnormal",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsCreditNormal(security:list,*args,**kwargs):
    # 获取承销团成员
    return w.wss(security,"abs_creditnormal",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValEvToeBitDa2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取企业倍数2(EV2/EBITDA)时间序列
    return w.wsd(security,"val_evtoebitda2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValEvToeBitDa2(security:list,*args,**kwargs):
    # 获取企业倍数2(EV2/EBITDA)
    return w.wss(security,"val_evtoebitda2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdSellVolAtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取主动卖出量(全单)时间序列
    return w.wsd(security,"mfd_sellvol_at",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdSellVolAt(security:list,*args,**kwargs):
    # 获取主动卖出量(全单)
    return w.wss(security,"mfd_sellvol_at",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetTurnDaysSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净营业周期时间序列
    return w.wsd(security,"netturndays",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetTurnDays(security:list,*args,**kwargs):
    # 获取净营业周期
    return w.wss(security,"netturndays",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDEbIt3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取息税前利润_GSD时间序列
    return w.wsd(security,"wgsd_ebit3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDEbIt3(security:list,*args,**kwargs):
    # 获取息税前利润_GSD
    return w.wss(security,"wgsd_ebit3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdSellVolASeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取主动卖出量时间序列
    return w.wsd(security,"mfd_sellvol_a",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdSellVolA(security:list,*args,**kwargs):
    # 获取主动卖出量
    return w.wss(security,"mfd_sellvol_a",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsOriginalSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取原始权益人时间序列
    return w.wsd(security,"fund__reitsoriginal",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsOriginal(security:list,*args,**kwargs):
    # 获取原始权益人
    return w.wss(security,"fund__reitsoriginal",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsOthersSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他应收款(合计)时间序列
    return w.wsd(security,"stm07_bs_reits_others",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsOthers(security:list,*args,**kwargs):
    # 获取其他应收款(合计)
    return w.wss(security,"stm07_bs_reits_others",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDInvTurnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取存货周转率_GSD时间序列
    return w.wsd(security,"wgsd_invturn",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDInvTurn(security:list,*args,**kwargs):
    # 获取存货周转率_GSD
    return w.wss(security,"wgsd_invturn",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdBuyVolAtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取主动买入量(全单)时间序列
    return w.wsd(security,"mfd_buyvol_at",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdBuyVolAt(security:list,*args,**kwargs):
    # 获取主动买入量(全单)
    return w.wss(security,"mfd_buyvol_at",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaDaSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取折旧和摊销_PIT时间序列
    return w.wsd(security,"fa_da",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaDa(security:list,*args,**kwargs):
    # 获取折旧和摊销_PIT
    return w.wss(security,"fa_da",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechObVSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取能量潮指标_PIT时间序列
    return w.wsd(security,"tech_obv",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechObV(security:list,*args,**kwargs):
    # 获取能量潮指标_PIT
    return w.wss(security,"tech_obv",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDYoYTrSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业总收入(同比增长率)_GSD时间序列
    return w.wsd(security,"wgsd_yoy_tr",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDYoYTr(security:list,*args,**kwargs):
    # 获取营业总收入(同比增长率)_GSD
    return w.wss(security,"wgsd_yoy_tr",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGSpc02004Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取新增专利数时间序列
    return w.wsd(security,"esg_spc02004",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGSpc02004(security:list,*args,**kwargs):
    # 获取新增专利数
    return w.wss(security,"esg_spc02004",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoyoP2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业利润(同比增长率)2时间序列
    return w.wsd(security,"yoyop2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoyoP2(security:list,*args,**kwargs):
    # 获取营业利润(同比增长率)2
    return w.wss(security,"yoyop2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteMGmtBenBcSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取董事长薪酬时间序列
    return w.wsd(security,"stmnote_mgmt_ben_bc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteMGmtBenBc(security:list,*args,**kwargs):
    # 获取董事长薪酬
    return w.wss(security,"stmnote_mgmt_ben_bc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteMGmtBenCeoSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总经理薪酬时间序列
    return w.wsd(security,"stmnote_mgmt_ben_ceo",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteMGmtBenCeo(security:list,*args,**kwargs):
    # 获取总经理薪酬
    return w.wss(security,"stmnote_mgmt_ben_ceo",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPtMTradeDaySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取剩余存续期(交易日)时间序列
    return w.wsd(security,"ptmtradeday",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPtMTradeDay(security:list,*args,**kwargs):
    # 获取剩余存续期(交易日)
    return w.wss(security,"ptmtradeday",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPtMDaySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取剩余存续期(日历日)时间序列
    return w.wsd(security,"ptmday",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPtMDay(security:list,*args,**kwargs):
    # 获取剩余存续期(日历日)
    return w.wss(security,"ptmday",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInSHdTtlExSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取合计买卖超时间序列
    return w.wsd(security,"inshd_ttl_ex",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInSHdTtlEx(security:list,*args,**kwargs):
    # 获取合计买卖超
    return w.wss(security,"inshd_ttl_ex",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInSHdDlrExSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取自营买卖超时间序列
    return w.wsd(security,"inshd_dlr_ex",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInSHdDlrEx(security:list,*args,**kwargs):
    # 获取自营买卖超
    return w.wss(security,"inshd_dlr_ex",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechBias5Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取5日乖离率_PIT时间序列
    return w.wsd(security,"tech_bias5",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechBias5(security:list,*args,**kwargs):
    # 获取5日乖离率_PIT
    return w.wss(security,"tech_bias5",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDIsCloser1Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取董事会秘书时间序列
    return w.wsd(security,"discloser1",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDIsCloser1(security:list,*args,**kwargs):
    # 获取董事会秘书
    return w.wss(security,"discloser1",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getVolatilityRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取历史波动率时间序列
    return w.wsd(security,"volatilityratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getVolatilityRatio(security:list,*args,**kwargs):
    # 获取历史波动率
    return w.wss(security,"volatilityratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInSHdQFIiExSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取外资买卖超时间序列
    return w.wsd(security,"inshd_qfii_ex",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInSHdQFIiEx(security:list,*args,**kwargs):
    # 获取外资买卖超
    return w.wss(security,"inshd_qfii_ex",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaCashTurnRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取现金周转率时间序列
    return w.wsd(security,"fa_cashturnratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaCashTurnRatio(security:list,*args,**kwargs):
    # 获取现金周转率
    return w.wss(security,"fa_cashturnratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueFeeAcContSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取会计师费用时间序列
    return w.wsd(security,"issuefee_accont",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueFeeAcCont(security:list,*args,**kwargs):
    # 获取会计师费用
    return w.wss(security,"issuefee_accont",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGSch01001Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取供应商数量时间序列
    return w.wsd(security,"esg_sch01001",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGSch01001(security:list,*args,**kwargs):
    # 获取供应商数量
    return w.wss(security,"esg_sch01001",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValPbWGtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取加权市净率_PIT时间序列
    return w.wsd(security,"val_pb_wgt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValPbWGt(security:list,*args,**kwargs):
    # 获取加权市净率_PIT
    return w.wss(security,"val_pb_wgt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechDHiloSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取波幅中位数_PIT时间序列
    return w.wsd(security,"tech_dhilo",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechDHilo(security:list,*args,**kwargs):
    # 获取波幅中位数_PIT
    return w.wss(security,"tech_dhilo",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechMa10CloseSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取均线价格比_PIT时间序列
    return w.wsd(security,"tech_ma10close",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechMa10Close(security:list,*args,**kwargs):
    # 获取均线价格比_PIT
    return w.wss(security,"tech_ma10close",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechPsySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取心理线指标_PIT时间序列
    return w.wsd(security,"tech_psy",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechPsy(security:list,*args,**kwargs):
    # 获取心理线指标_PIT
    return w.wss(security,"tech_psy",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInSHdFundExSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取投信买卖超时间序列
    return w.wsd(security,"inshd_fund_ex",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInSHdFundEx(security:list,*args,**kwargs):
    # 获取投信买卖超
    return w.wss(security,"inshd_fund_ex",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdBuyVolASeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取主动买入量时间序列
    return w.wsd(security,"mfd_buyvol_a",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdBuyVolA(security:list,*args,**kwargs):
    # 获取主动买入量
    return w.wss(security,"mfd_buyvol_a",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivRecordDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取股权登记日时间序列
    return w.wsd(security,"div_recorddate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivRecordDate(security:list,*args,**kwargs):
    # 获取股权登记日
    return w.wss(security,"div_recorddate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivExDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取除权除息日时间序列
    return w.wsd(security,"div_exdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivExDate(security:list,*args,**kwargs):
    # 获取除权除息日
    return w.wss(security,"div_exdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsBorrowerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基础债务人时间序列
    return w.wsd(security,"abs_borrower",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsBorrower(security:list,*args,**kwargs):
    # 获取基础债务人
    return w.wss(security,"abs_borrower",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteTaxUrbanLandUseSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取土地使用税时间序列
    return w.wsd(security,"stmnote_tax_urbanlanduse",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteTaxUrbanLandUse(security:list,*args,**kwargs):
    # 获取土地使用税
    return w.wss(security,"stmnote_tax_urbanlanduse",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValPsTtMwGtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取市销率PS(TTM,加权)时间序列
    return w.wsd(security,"val_ps_ttmwgt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValPsTtMwGt(security:list,*args,**kwargs):
    # 获取市销率PS(TTM,加权)
    return w.wss(security,"val_ps_ttmwgt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValPeTtMwGtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取市盈率PE(TTM,加权)时间序列
    return w.wsd(security,"val_pe_ttmwgt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValPeTtMwGt(security:list,*args,**kwargs):
    # 获取市盈率PE(TTM,加权)
    return w.wss(security,"val_pe_ttmwgt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteTaxEdeSupplementTarYSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取教育费附加时间序列
    return w.wsd(security,"stmnote_tax_edesupplementtary",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteTaxEdeSupplementTarY(security:list,*args,**kwargs):
    # 获取教育费附加
    return w.wss(security,"stmnote_tax_edesupplementtary",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEquityToAssetSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取股东权益比时间序列
    return w.wsd(security,"equity_to_asset",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEquityToAsset(security:list,*args,**kwargs):
    # 获取股东权益比
    return w.wss(security,"equity_to_asset",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteCustomerTop5Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取大客户名称时间序列
    return w.wsd(security,"stmnote_customertop5",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteCustomerTop5(security:list,*args,**kwargs):
    # 获取大客户名称
    return w.wss(security,"stmnote_customertop5",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaDebtToAssetSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资产负债率_PIT时间序列
    return w.wsd(security,"fa_debttoasset",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaDebtToAsset(security:list,*args,**kwargs):
    # 获取资产负债率_PIT
    return w.wss(security,"fa_debttoasset",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEbItTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取息税前利润(TTM,只有最新数据)时间序列
    return w.wsd(security,"ebit_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEbItTtM(security:list,*args,**kwargs):
    # 获取息税前利润(TTM,只有最新数据)
    return w.wss(security,"ebit_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaRocTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资本报酬率(TTM)_PIT时间序列
    return w.wsd(security,"fa_roc_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaRocTtM(security:list,*args,**kwargs):
    # 获取资本报酬率(TTM)_PIT
    return w.wss(security,"fa_roc_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDDebtToAssetsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资产负债率_GSD时间序列
    return w.wsd(security,"wgsd_debttoassets",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDDebtToAssets(security:list,*args,**kwargs):
    # 获取资产负债率_GSD
    return w.wss(security,"wgsd_debttoassets",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDebtToAssetsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资产负债率时间序列
    return w.wsd(security,"debttoassets",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDebtToAssets(security:list,*args,**kwargs):
    # 获取资产负债率
    return w.wss(security,"debttoassets",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsLegalMaturitySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取法定到期日时间序列
    return w.wsd(security,"abs_legalmaturity",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsLegalMaturity(security:list,*args,**kwargs):
    # 获取法定到期日
    return w.wss(security,"abs_legalmaturity",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEbItTtM2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取息税前利润(TTM反推法)时间序列
    return w.wsd(security,"ebit_ttm2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEbItTtM2(security:list,*args,**kwargs):
    # 获取息税前利润(TTM反推法)
    return w.wss(security,"ebit_ttm2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValPeMedianSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取市盈率PE(TTM,中位数)时间序列
    return w.wsd(security,"val_pe_median",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValPeMedian(security:list,*args,**kwargs):
    # 获取市盈率PE(TTM,中位数)
    return w.wss(security,"val_pe_median",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValPeNonNegativeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取市盈率PE(TTM,剔除负值)时间序列
    return w.wsd(security,"val_pe_nonnegative",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValPeNonNegative(security:list,*args,**kwargs):
    # 获取市盈率PE(TTM,剔除负值)
    return w.wss(security,"val_pe_nonnegative",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPsTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取市销率PS(TTM)时间序列
    return w.wsd(security,"ps_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPsTtM(security:list,*args,**kwargs):
    # 获取市销率PS(TTM)
    return w.wss(security,"ps_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPeTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取市盈率PE(TTM)时间序列
    return w.wsd(security,"pe_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPeTtM(security:list,*args,**kwargs):
    # 获取市盈率PE(TTM)
    return w.wss(security,"pe_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMarginSaleRepayAmountSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取融券偿还额时间序列
    return w.wsd(security,"margin_salerepayamount",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMarginSaleRepayAmount(security:list,*args,**kwargs):
    # 获取融券偿还额
    return w.wss(security,"margin_salerepayamount",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMarginSaleTradingAmountSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取融券卖出额时间序列
    return w.wsd(security,"margin_saletradingamount",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMarginSaleTradingAmount(security:list,*args,**kwargs):
    # 获取融券卖出额
    return w.wss(security,"margin_saletradingamount",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEbItTtM3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取息税前利润(TTM反推法)_GSD时间序列
    return w.wsd(security,"ebit_ttm3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEbItTtM3(security:list,*args,**kwargs):
    # 获取息税前利润(TTM反推法)_GSD
    return w.wss(security,"ebit_ttm3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalIncomeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取报告期利润时间序列
    return w.wsd(security,"anal_income",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalIncome(security:list,*args,**kwargs):
    # 获取报告期利润
    return w.wss(security,"anal_income",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaRoeTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取权益回报率(TTM)_PIT时间序列
    return w.wsd(security,"fa_roe_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaRoeTtM(security:list,*args,**kwargs):
    # 获取权益回报率(TTM)_PIT
    return w.wss(security,"fa_roe_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNavChange7Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金申购款时间序列
    return w.wsd(security,"stm_navchange_7",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNavChange7(security:list,*args,**kwargs):
    # 获取基金申购款
    return w.wss(security,"stm_navchange_7",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdSellAmtAtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取主动卖出额(全单)时间序列
    return w.wsd(security,"mfd_sellamt_at",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdSellAmtAt(security:list,*args,**kwargs):
    # 获取主动卖出额(全单)
    return w.wss(security,"mfd_sellamt_at",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdSellAmtASeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取主动卖出额时间序列
    return w.wsd(security,"mfd_sellamt_a",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdSellAmtA(security:list,*args,**kwargs):
    # 获取主动卖出额
    return w.wss(security,"mfd_sellamt_a",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssuePrePlanDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取预案公告日时间序列
    return w.wsd(security,"rightsissue_preplandate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssuePrePlanDate(security:list,*args,**kwargs):
    # 获取预案公告日
    return w.wss(security,"rightsissue_preplandate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsSPvSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取计划管理人时间序列
    return w.wsd(security,"abs_spv",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsSPv(security:list,*args,**kwargs):
    # 获取计划管理人
    return w.wss(security,"abs_spv",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInvestmentIncome0004Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取净投资收益时间序列
    return w.wsd(security,"stmnote_InvestmentIncome_0004",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInvestmentIncome0004(security:list,*args,**kwargs):
    # 获取净投资收益
    return w.wss(security,"stmnote_InvestmentIncome_0004",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInvestmentIncome0010Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取总投资收益时间序列
    return w.wsd(security,"stmnote_InvestmentIncome_0010",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInvestmentIncome0010(security:list,*args,**kwargs):
    # 获取总投资收益
    return w.wss(security,"stmnote_InvestmentIncome_0010",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdBuyAmtAtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取主动买入额(全单)时间序列
    return w.wsd(security,"mfd_buyamt_at",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdBuyAmtAt(security:list,*args,**kwargs):
    # 获取主动买入额(全单)
    return w.wss(security,"mfd_buyamt_at",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdBuyAmtASeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取主动买入额时间序列
    return w.wsd(security,"mfd_buyamt_a",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMfdBuyAmtA(security:list,*args,**kwargs):
    # 获取主动买入额
    return w.wss(security,"mfd_buyamt_a",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs18Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取信息披露费时间序列
    return w.wsd(security,"stm_is_18",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs18(security:list,*args,**kwargs):
    # 获取信息披露费
    return w.wss(security,"stm_is_18",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaProfitToMvTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取收益市值比(TTM)_PIT时间序列
    return w.wsd(security,"fa_profittomv_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaProfitToMvTtM(security:list,*args,**kwargs):
    # 获取收益市值比(TTM)_PIT
    return w.wss(security,"fa_profittomv_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaEbItUnVerTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取息税前利润(TTM反推法)_PIT时间序列
    return w.wsd(security,"fa_ebitunver_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaEbItUnVerTtM(security:list,*args,**kwargs):
    # 获取息税前利润(TTM反推法)_PIT
    return w.wss(security,"fa_ebitunver_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaSuperQuickSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取超速动比率_PIT时间序列
    return w.wsd(security,"fa_superquick",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaSuperQuick(security:list,*args,**kwargs):
    # 获取超速动比率_PIT
    return w.wss(security,"fa_superquick",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaTaxRatioTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售税金率(TTM)_PIT时间序列
    return w.wsd(security,"fa_taxratio_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaTaxRatioTtM(security:list,*args,**kwargs):
    # 获取销售税金率(TTM)_PIT
    return w.wss(security,"fa_taxratio_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValOrToMvTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营收市值比(TTM)_PIT时间序列
    return w.wsd(security,"val_ortomv_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValOrToMvTtM(security:list,*args,**kwargs):
    # 获取营收市值比(TTM)_PIT
    return w.wss(security,"val_ortomv_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCashFlowTtM3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取现金净流量(TTM)_GSD时间序列
    return w.wsd(security,"cashflow_ttm3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCashFlowTtM3(security:list,*args,**kwargs):
    # 获取现金净流量(TTM)_GSD
    return w.wss(security,"cashflow_ttm3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCashFlowTtM2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取现金净流量(TTM)时间序列
    return w.wsd(security,"cashflow_ttm2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCashFlowTtM2(security:list,*args,**kwargs):
    # 获取现金净流量(TTM)
    return w.wss(security,"cashflow_ttm2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaCashFlowTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取现金净流量(TTM)_PIT时间序列
    return w.wsd(security,"fa_cashflow_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaCashFlowTtM(security:list,*args,**kwargs):
    # 获取现金净流量(TTM)_PIT
    return w.wss(security,"fa_cashflow_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNavChange8PaidInCapitalSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金赎回款(实收基金)时间序列
    return w.wsd(security,"stm_navchange_8_paidincapital",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNavChange8PaidInCapital(security:list,*args,**kwargs):
    # 获取基金赎回款(实收基金)
    return w.wss(security,"stm_navchange_8_paidincapital",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNavChange8Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金赎回款时间序列
    return w.wsd(security,"stm_navchange_8",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNavChange8(security:list,*args,**kwargs):
    # 获取基金赎回款
    return w.wss(security,"stm_navchange_8",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNavChange7PaidInCapitalSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金申购款(实收基金)时间序列
    return w.wsd(security,"stm_navchange_7_paidincapital",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNavChange7PaidInCapital(security:list,*args,**kwargs):
    # 获取基金申购款(实收基金)
    return w.wss(security,"stm_navchange_7_paidincapital",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIbDebtRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取有息负债率时间序列
    return w.wsd(security,"ibdebtratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIbDebtRatio(security:list,*args,**kwargs):
    # 获取有息负债率
    return w.wss(security,"ibdebtratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskUpsideStDevSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取上行标准差时间序列
    return w.wsd(security,"risk_upsidestdev",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskUpsideStDev(security:list,*args,**kwargs):
    # 获取上行标准差
    return w.wss(security,"risk_upsidestdev",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskDownsideStDevSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取下行标准差时间序列
    return w.wsd(security,"risk_downsidestdev",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskDownsideStDev(security:list,*args,**kwargs):
    # 获取下行标准差
    return w.wss(security,"risk_downsidestdev",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoDilutedPeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取首发市盈率(摊薄)时间序列
    return w.wsd(security,"ipo_dilutedpe",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoDilutedPe(security:list,*args,**kwargs):
    # 获取首发市盈率(摊薄)
    return w.wss(security,"ipo_dilutedpe",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskStDevSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取收益标准差时间序列
    return w.wsd(security,"risk_stdev",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskStDev(security:list,*args,**kwargs):
    # 获取收益标准差
    return w.wss(security,"risk_stdev",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYTcSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取赎回收益率时间序列
    return w.wsd(security,"ytc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYTc(security:list,*args,**kwargs):
    # 获取赎回收益率
    return w.wss(security,"ytc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNxcUpnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取下一付息日时间序列
    return w.wsd(security,"nxcupn",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNxcUpn(security:list,*args,**kwargs):
    # 获取下一付息日
    return w.wss(security,"nxcupn",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalPreCupNSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取上一付息日时间序列
    return w.wsd(security,"anal_precupn",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalPreCupN(security:list,*args,**kwargs):
    # 获取上一付息日
    return w.wss(security,"anal_precupn",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAccruedDaysSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取已计息天数时间序列
    return w.wsd(security,"accrueddays",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAccruedDays(security:list,*args,**kwargs):
    # 获取已计息天数
    return w.wss(security,"accrueddays",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPutVolumeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取认沽成交量时间序列
    return w.wsd(security,"putvolume",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPutVolume(security:list,*args,**kwargs):
    # 获取认沽成交量
    return w.wss(security,"putvolume",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCallVolumeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取认购成交量时间序列
    return w.wsd(security,"callvolume",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCallVolume(security:list,*args,**kwargs):
    # 获取认购成交量
    return w.wss(security,"callvolume",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOptionVolumeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取品种成交量时间序列
    return w.wsd(security,"optionvolume",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOptionVolume(security:list,*args,**kwargs):
    # 获取品种成交量
    return w.wss(security,"optionvolume",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOiVolumeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取会员成交量时间序列
    return w.wsd(security,"oi_volume",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOiVolume(security:list,*args,**kwargs):
    # 获取会员成交量
    return w.wss(security,"oi_volume",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUsVolumeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取标的成交量时间序列
    return w.wsd(security,"us_volume",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUsVolume(security:list,*args,**kwargs):
    # 获取标的成交量
    return w.wss(security,"us_volume",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getVolNdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取N日成交量时间序列
    return w.wsd(security,"vol_nd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getVolNd(security:list,*args,**kwargs):
    # 获取N日成交量
    return w.wss(security,"vol_nd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPqBlockTradeVolumeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间成交量(含大宗交易)时间序列
    return w.wsd(security,"pq_blocktradevolume",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPqBlockTradeVolume(security:list,*args,**kwargs):
    # 获取区间成交量(含大宗交易)
    return w.wss(security,"pq_blocktradevolume",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getVolPerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间成交量时间序列
    return w.wsd(security,"vol_per",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getVolPer(security:list,*args,**kwargs):
    # 获取区间成交量
    return w.wss(security,"vol_per",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskNonSYsRiskSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取非系统风险_FUND时间序列
    return w.wsd(security,"risk_nonsysrisk",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskNonSYsRisk(security:list,*args,**kwargs):
    # 获取非系统风险_FUND
    return w.wss(security,"risk_nonsysrisk",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur7810Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取集团客户数时间序列
    return w.wsd(security,"stmnote_insur_7810",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur7810(security:list,*args,**kwargs):
    # 获取集团客户数
    return w.wss(security,"stmnote_insur_7810",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskNonSYsRisk1Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取非系统风险时间序列
    return w.wsd(security,"risk_nonsysrisk1",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskNonSYsRisk1(security:list,*args,**kwargs):
    # 获取非系统风险
    return w.wss(security,"risk_nonsysrisk1",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStDcOfSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取标准差系数时间序列
    return w.wsd(security,"stdcof",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStDcOf(security:list,*args,**kwargs):
    # 获取标准差系数
    return w.wss(security,"stdcof",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyUnderwriterSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取牵头经办人(海外)时间序列
    return w.wsd(security,"agency_underwriter",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyUnderwriter(security:list,*args,**kwargs):
    # 获取牵头经办人(海外)
    return w.wss(security,"agency_underwriter",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getVolumeAHtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取盘后成交量时间序列
    return w.wsd(security,"volume_aht",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getVolumeAHt(security:list,*args,**kwargs):
    # 获取盘后成交量
    return w.wss(security,"volume_aht",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNeEqListAnnDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取挂牌公告日时间序列
    return w.wsd(security,"neeq_listanndate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNeEqListAnnDate(security:list,*args,**kwargs):
    # 获取挂牌公告日
    return w.wss(security,"neeq_listanndate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechVosCSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取成交量震荡_PIT时间序列
    return w.wsd(security,"tech_vosc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechVosC(security:list,*args,**kwargs):
    # 获取成交量震荡_PIT
    return w.wss(security,"tech_vosc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechVrSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取成交量比率_PIT时间序列
    return w.wsd(security,"tech_vr",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechVr(security:list,*args,**kwargs):
    # 获取成交量比率_PIT
    return w.wss(security,"tech_vr",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYTPSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取回售收益率时间序列
    return w.wsd(security,"ytp",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYTP(security:list,*args,**kwargs):
    # 获取回售收益率
    return w.wss(security,"ytp",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskStDevYearlySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取年化波动率时间序列
    return w.wsd(security,"risk_stdevyearly",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskStDevYearly(security:list,*args,**kwargs):
    # 获取年化波动率
    return w.wss(security,"risk_stdevyearly",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderCommissionChargeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取兑付手续费时间序列
    return w.wsd(security,"tender_commissioncharge",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderCommissionCharge(security:list,*args,**kwargs):
    # 获取兑付手续费
    return w.wss(security,"tender_commissioncharge",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareTotalTradableSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取流通股合计时间序列
    return w.wsd(security,"share_totaltradable",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareTotalTradable(security:list,*args,**kwargs):
    # 获取流通股合计
    return w.wss(security,"share_totaltradable",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValLnToTAssetsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取对数总资产_PIT时间序列
    return w.wsd(security,"val_lntotassets",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValLnToTAssets(security:list,*args,**kwargs):
    # 获取对数总资产_PIT
    return w.wss(security,"val_lntotassets",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取结算备付金_FUND时间序列
    return w.wsd(security,"stm_bs_2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs2(security:list,*args,**kwargs):
    # 获取结算备付金_FUND
    return w.wss(security,"stm_bs_2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSettleRsRvSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取结算备付金时间序列
    return w.wsd(security,"settle_rsrv",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSettleRsRv(security:list,*args,**kwargs):
    # 获取结算备付金
    return w.wss(security,"settle_rsrv",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaBpSSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股净资产_PIT时间序列
    return w.wsd(security,"fa_bps",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaBpS(security:list,*args,**kwargs):
    # 获取每股净资产_PIT
    return w.wss(security,"fa_bps",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYTMIfExeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取行权收益率时间序列
    return w.wsd(security,"YTM_ifexe",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYTMIfExe(security:list,*args,**kwargs):
    # 获取行权收益率
    return w.wss(security,"YTM_ifexe",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNxOptionDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取下一行权日时间序列
    return w.wsd(security,"nxoptiondate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNxOptionDate(security:list,*args,**kwargs):
    # 获取下一行权日
    return w.wss(security,"nxoptiondate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareHSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取香港上市股时间序列
    return w.wsd(security,"share_h",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareH(security:list,*args,**kwargs):
    # 获取香港上市股
    return w.wss(security,"share_h",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDecrInventoriesSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取存货的减少时间序列
    return w.wsd(security,"decr_inventories",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDecrInventories(security:list,*args,**kwargs):
    # 获取存货的减少
    return w.wss(security,"decr_inventories",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareOverSeaSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取海外上市股时间序列
    return w.wsd(security,"share_oversea",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareOverSea(security:list,*args,**kwargs):
    # 获取海外上市股
    return w.wss(security,"share_oversea",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPutAmountSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取认沽成交额时间序列
    return w.wsd(security,"putamount",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPutAmount(security:list,*args,**kwargs):
    # 获取认沽成交额
    return w.wss(security,"putamount",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOThRcVSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他应收款时间序列
    return w.wsd(security,"oth_rcv",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOThRcV(security:list,*args,**kwargs):
    # 获取其他应收款
    return w.wss(security,"oth_rcv",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCallAmountSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取认购成交额时间序列
    return w.wsd(security,"callamount",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCallAmount(security:list,*args,**kwargs):
    # 获取认购成交额
    return w.wss(security,"callamount",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskAnnUstDevSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取收益标准差(年化)时间序列
    return w.wsd(security,"risk_annustdev",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskAnnUstDev(security:list,*args,**kwargs):
    # 获取收益标准差(年化)
    return w.wss(security,"risk_annustdev",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOptionAmountSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取品种成交额时间序列
    return w.wsd(security,"optionamount",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOptionAmount(security:list,*args,**kwargs):
    # 获取品种成交额
    return w.wss(security,"optionamount",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUsAmountSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取标的成交额时间序列
    return w.wsd(security,"us_amount",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUsAmount(security:list,*args,**kwargs):
    # 获取标的成交额
    return w.wss(security,"us_amount",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAmtNdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取N日成交额时间序列
    return w.wsd(security,"amt_nd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAmtNd(security:list,*args,**kwargs):
    # 获取N日成交额
    return w.wss(security,"amt_nd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPqBlockTradeAmountsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间成交额(含大宗交易)时间序列
    return w.wsd(security,"pq_blocktradeamounts",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPqBlockTradeAmounts(security:list,*args,**kwargs):
    # 获取区间成交额(含大宗交易)
    return w.wss(security,"pq_blocktradeamounts",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRateRateGuarantorSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取担保人评级时间序列
    return w.wsd(security,"rate_rateguarantor",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRateRateGuarantor(security:list,*args,**kwargs):
    # 获取担保人评级
    return w.wss(security,"rate_rateguarantor",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAmtPerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间成交额时间序列
    return w.wsd(security,"amt_per",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAmtPer(security:list,*args,**kwargs):
    # 获取区间成交额
    return w.wss(security,"amt_per",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAmountAHtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取盘后成交额时间序列
    return w.wsd(security,"amount_aht",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAmountAHt(security:list,*args,**kwargs):
    # 获取盘后成交额
    return w.wss(security,"amount_aht",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechAmount1M60Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取成交额惯性_PIT时间序列
    return w.wsd(security,"tech_amount1m60",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechAmount1M60(security:list,*args,**kwargs):
    # 获取成交额惯性_PIT
    return w.wss(security,"tech_amount1m60",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareTotalRestrictedSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取限售股合计时间序列
    return w.wsd(security,"share_totalrestricted",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareTotalRestricted(security:list,*args,**kwargs):
    # 获取限售股合计
    return w.wss(security,"share_totalrestricted",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMaxUpOrDownSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取涨跌停状态时间序列
    return w.wsd(security,"maxupordown",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMaxUpOrDown(security:list,*args,**kwargs):
    # 获取涨跌停状态
    return w.wss(security,"maxupordown",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs14Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取应收申购款_FUND时间序列
    return w.wsd(security,"stm_bs_14",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs14(security:list,*args,**kwargs):
    # 获取应收申购款_FUND
    return w.wss(security,"stm_bs_14",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs11Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金管理费_FUND时间序列
    return w.wsd(security,"stm_is_11",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs11(security:list,*args,**kwargs):
    # 获取基金管理费_FUND
    return w.wss(security,"stm_is_11",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur1Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取保单继续率(13个月)时间序列
    return w.wsd(security,"stmnote_insur_1",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur1(security:list,*args,**kwargs):
    # 获取保单继续率(13个月)
    return w.wss(security,"stmnote_insur_1",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUsCloseSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取标的收盘价时间序列
    return w.wsd(security,"us_close",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUsClose(security:list,*args,**kwargs):
    # 获取标的收盘价
    return w.wss(security,"us_close",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnnualStDeVr100WSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取年化波动率(最近100周)时间序列
    return w.wsd(security,"annualstdevr_100w",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnnualStDeVr100W(security:list,*args,**kwargs):
    # 获取年化波动率(最近100周)
    return w.wss(security,"annualstdevr_100w",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnnualYeIlD60MSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取平均收益率(年化,最近60个月)时间序列
    return w.wsd(security,"annualyeild_60m",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnnualYeIlD60M(security:list,*args,**kwargs):
    # 获取平均收益率(年化,最近60个月)
    return w.wss(security,"annualyeild_60m",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnnualYeIlD24MSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取平均收益率(年化,最近24个月)时间序列
    return w.wsd(security,"annualyeild_24m",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnnualYeIlD24M(security:list,*args,**kwargs):
    # 获取平均收益率(年化,最近24个月)
    return w.wss(security,"annualyeild_24m",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnnualYeIlD100WSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取平均收益率(年化,最近100周)时间序列
    return w.wsd(security,"annualyeild_100w",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnnualYeIlD100W(security:list,*args,**kwargs):
    # 获取平均收益率(年化,最近100周)
    return w.wss(security,"annualyeild_100w",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNeEqMarketMakerNumSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取做市商家数时间序列
    return w.wsd(security,"neeq_marketmakernum",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNeEqMarketMakerNum(security:list,*args,**kwargs):
    # 获取做市商家数
    return w.wss(security,"neeq_marketmakernum",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClosePerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间收盘价时间序列
    return w.wsd(security,"close_per",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClosePer(security:list,*args,**kwargs):
    # 获取区间收盘价
    return w.wss(security,"close_per",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSec5Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取风险覆盖率时间序列
    return w.wsd(security,"stmnote_sec_5",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSec5(security:list,*args,**kwargs):
    # 获取风险覆盖率
    return w.wss(security,"stmnote_sec_5",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getConvexitySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取收盘价凸性时间序列
    return w.wsd(security,"convexity",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getConvexity(security:list,*args,**kwargs):
    # 获取收盘价凸性
    return w.wss(security,"convexity",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDurationSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取收盘价久期时间序列
    return w.wsd(security,"duration",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration(security:list,*args,**kwargs):
    # 获取收盘价久期
    return w.wss(security,"duration",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEstPctChangeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取预测涨跌幅(评级日,最低价)时间序列
    return w.wsd(security,"est_pctchange",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEstPctChange(security:list,*args,**kwargs):
    # 获取预测涨跌幅(评级日,最低价)
    return w.wss(security,"est_pctchange",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUsLowSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取标的最低价时间序列
    return w.wsd(security,"us_low",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUsLow(security:list,*args,**kwargs):
    # 获取标的最低价
    return w.wss(security,"us_low",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLowPerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间最低价时间序列
    return w.wsd(security,"low_per",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLowPer(security:list,*args,**kwargs):
    # 获取区间最低价
    return w.wss(security,"low_per",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetProfitIsNettingSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净利润差额(合计平衡项目)时间序列
    return w.wsd(security,"net_profit_is_netting",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetProfitIsNetting(security:list,*args,**kwargs):
    # 获取净利润差额(合计平衡项目)
    return w.wss(security,"net_profit_is_netting",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowNominatorSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取增发分销商时间序列
    return w.wsd(security,"fellow_nominator",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowNominator(security:list,*args,**kwargs):
    # 获取增发分销商
    return w.wss(security,"fellow_nominator",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoMarketMakerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取做市商名称时间序列
    return w.wsd(security,"ipo_marketMaker",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoMarketMaker(security:list,*args,**kwargs):
    # 获取做市商名称
    return w.wss(security,"ipo_marketMaker",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetProfitIsGapSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净利润差额(特殊报表科目)时间序列
    return w.wsd(security,"net_profit_is_gap",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetProfitIsGap(security:list,*args,**kwargs):
    # 获取净利润差额(特殊报表科目)
    return w.wss(security,"net_profit_is_gap",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSec31Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取附属净资本时间序列
    return w.wsd(security,"stmnote_sec_31",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSec31(security:list,*args,**kwargs):
    # 获取附属净资本
    return w.wss(security,"stmnote_sec_31",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSec30Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取核心净资本时间序列
    return w.wsd(security,"stmnote_sec_30",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSec30(security:list,*args,**kwargs):
    # 获取核心净资本
    return w.wss(security,"stmnote_sec_30",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSec4Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取净资本比率时间序列
    return w.wsd(security,"stmnote_sec_4",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSec4(security:list,*args,**kwargs):
    # 获取净资本比率
    return w.wss(security,"stmnote_sec_4",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnnualStDeVr24MSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取年化波动率(最近24个月)时间序列
    return w.wsd(security,"annualstdevr_24m",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnnualStDeVr24M(security:list,*args,**kwargs):
    # 获取年化波动率(最近24个月)
    return w.wss(security,"annualstdevr_24m",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs26Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取应付赎回款_FUND时间序列
    return w.wsd(security,"stm_bs_26",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs26(security:list,*args,**kwargs):
    # 获取应付赎回款_FUND
    return w.wss(security,"stm_bs_26",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteLandUseRights22Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取土地使用权_账面价值时间序列
    return w.wsd(security,"stmnote_LandUseRights_22",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteLandUseRights22(security:list,*args,**kwargs):
    # 获取土地使用权_账面价值
    return w.wss(security,"stmnote_LandUseRights_22",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteLandUseRights20Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取土地使用权_累计摊销时间序列
    return w.wsd(security,"stmnote_LandUseRights_20",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteLandUseRights20(security:list,*args,**kwargs):
    # 获取土地使用权_累计摊销
    return w.wss(security,"stmnote_LandUseRights_20",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs74Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取客户维护费_FUND时间序列
    return w.wsd(security,"stm_is_74",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs74(security:list,*args,**kwargs):
    # 获取客户维护费_FUND
    return w.wss(security,"stm_is_74",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs12Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金托管费_FUND时间序列
    return w.wsd(security,"stm_is_12",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs12(security:list,*args,**kwargs):
    # 获取基金托管费_FUND
    return w.wss(security,"stm_is_12",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBondHolderNameSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取持有人名称时间序列
    return w.wsd(security,"bondholder_name",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBondHolderName(security:list,*args,**kwargs):
    # 获取持有人名称
    return w.wss(security,"bondholder_name",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCbResultRationAmtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股配售额时间序列
    return w.wsd(security,"cb_result_rationamt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCbResultRationAmt(security:list,*args,**kwargs):
    # 获取每股配售额
    return w.wss(security,"cb_result_rationamt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareIssuingSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取已发行数量时间序列
    return w.wsd(security,"share_issuing",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getShareIssuing(security:list,*args,**kwargs):
    # 获取已发行数量
    return w.wss(security,"share_issuing",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskAnnualIntervalYieldSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间收益率(年化)时间序列
    return w.wsd(security,"risk_annualintervalyield",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskAnnualIntervalYield(security:list,*args,**kwargs):
    # 获取区间收益率(年化)
    return w.wss(security,"risk_annualintervalyield",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskAvgReturnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取平均收益率_FUND时间序列
    return w.wsd(security,"risk_avgreturn",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskAvgReturn(security:list,*args,**kwargs):
    # 获取平均收益率_FUND
    return w.wss(security,"risk_avgreturn",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoYTrSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业总收入(同比增长率)时间序列
    return w.wsd(security,"yoy_tr",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoYTr(security:list,*args,**kwargs):
    # 获取营业总收入(同比增长率)
    return w.wss(security,"yoy_tr",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur17NSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取新业务价值(寿险)时间序列
    return w.wsd(security,"stmnote_insur_17n",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur17N(security:list,*args,**kwargs):
    # 获取新业务价值(寿险)
    return w.wss(security,"stmnote_insur_17n",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAvgReturnYSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取平均收益率(年化)时间序列
    return w.wsd(security,"avgreturny",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAvgReturnY(security:list,*args,**kwargs):
    # 获取平均收益率(年化)
    return w.wss(security,"avgreturny",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getManetProfitFy3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取备考净利润(FY3,并购后)时间序列
    return w.wsd(security,"manetprofit_fy3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getManetProfitFy3(security:list,*args,**kwargs):
    # 获取备考净利润(FY3,并购后)
    return w.wss(security,"manetprofit_fy3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getManetProfitFy2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取备考净利润(FY2,并购后)时间序列
    return w.wsd(security,"manetprofit_fy2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getManetProfitFy2(security:list,*args,**kwargs):
    # 获取备考净利润(FY2,并购后)
    return w.wss(security,"manetprofit_fy2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAvgReturnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取平均收益率时间序列
    return w.wsd(security,"avgreturn",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAvgReturn(security:list,*args,**kwargs):
    # 获取平均收益率
    return w.wss(security,"avgreturn",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getManetProfitFy1Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取备考净利润(FY1,并购后)时间序列
    return w.wsd(security,"manetprofit_fy1",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getManetProfitFy1(security:list,*args,**kwargs):
    # 获取备考净利润(FY1,并购后)
    return w.wss(security,"manetprofit_fy1",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getManetProfitFy0Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取备考净利润(FY0,并购后)时间序列
    return w.wsd(security,"manetprofit_fy0",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getManetProfitFy0(security:list,*args,**kwargs):
    # 获取备考净利润(FY0,并购后)
    return w.wss(security,"manetprofit_fy0",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnnualStDeVr60MSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取年化波动率(最近60个月)时间序列
    return w.wsd(security,"annualstdevr_60m",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnnualStDeVr60M(security:list,*args,**kwargs):
    # 获取年化波动率(最近60个月)
    return w.wss(security,"annualstdevr_60m",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur4Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取保单继续率(26个月)时间序列
    return w.wsd(security,"stmnote_insur_4",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur4(security:list,*args,**kwargs):
    # 获取保单继续率(26个月)
    return w.wss(security,"stmnote_insur_4",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取保单继续率(25个月)时间序列
    return w.wsd(security,"stmnote_insur_3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur3(security:list,*args,**kwargs):
    # 获取保单继续率(25个月)
    return w.wss(security,"stmnote_insur_3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取保单继续率(14个月)时间序列
    return w.wsd(security,"stmnote_insur_2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur2(security:list,*args,**kwargs):
    # 获取保单继续率(14个月)
    return w.wss(security,"stmnote_insur_2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDLandUseRightsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取土地使用权_GSD时间序列
    return w.wsd(security,"wgsd_land_use_rights",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDLandUseRights(security:list,*args,**kwargs):
    # 获取土地使用权_GSD
    return w.wss(security,"wgsd_land_use_rights",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteLandUseRights19Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取土地使用权_原值时间序列
    return w.wsd(security,"stmnote_LandUseRights_19",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteLandUseRights19(security:list,*args,**kwargs):
    # 获取土地使用权_原值
    return w.wss(security,"stmnote_LandUseRights_19",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteLandUseRights21Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取土地使用权_减值准备时间序列
    return w.wsd(security,"stmnote_LandUseRights_21",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteLandUseRights21(security:list,*args,**kwargs):
    # 获取土地使用权_减值准备
    return w.wss(security,"stmnote_LandUseRights_21",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPctChgPerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间涨跌幅时间序列
    return w.wsd(security,"pct_chg_per",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPctChgPer(security:list,*args,**kwargs):
    # 获取区间涨跌幅
    return w.wss(security,"pct_chg_per",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur17Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取新业务价值(寿险)(旧)时间序列
    return w.wsd(security,"stmnote_insur_17",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur17(security:list,*args,**kwargs):
    # 获取新业务价值(寿险)(旧)
    return w.wss(security,"stmnote_insur_17",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration10YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取10年久期时间序列
    return w.wsd(security,"duration_10y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration10Y(security:list,*args,**kwargs):
    # 获取10年久期
    return w.wss(security,"duration_10y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCarryEnddateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取计息截止日时间序列
    return w.wsd(security,"carryenddate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCarryEnddate(security:list,*args,**kwargs):
    # 获取计息截止日
    return w.wss(security,"carryenddate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getConVPremiumRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取转股溢价率时间序列
    return w.wsd(security,"convpremiumratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getConVPremiumRatio(security:list,*args,**kwargs):
    # 获取转股溢价率
    return w.wss(security,"convpremiumratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEstEstAnalystSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取预测研究员时间序列
    return w.wsd(security,"est_estanalyst",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEstEstAnalyst(security:list,*args,**kwargs):
    # 获取预测研究员
    return w.wss(security,"est_estanalyst",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStrBPremiumRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取纯债溢价率时间序列
    return w.wsd(security,"strbpremiumratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStrBPremiumRatio(security:list,*args,**kwargs):
    # 获取纯债溢价率
    return w.wss(security,"strbpremiumratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEstRatingAnalystSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取评级研究员时间序列
    return w.wsd(security,"est_ratinganalyst",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEstRatingAnalyst(security:list,*args,**kwargs):
    # 获取评级研究员
    return w.wss(security,"est_ratinganalyst",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCalcDirtySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净价算全价时间序列
    return w.wsd(security,"calc_dirty",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCalcDirty(security:list,*args,**kwargs):
    # 获取净价算全价
    return w.wss(security,"calc_dirty",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCurYieldSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取当期收益率时间序列
    return w.wsd(security,"curyield",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCurYield(security:list,*args,**kwargs):
    # 获取当期收益率
    return w.wss(security,"curyield",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCalcDurationSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取麦考利久期时间序列
    return w.wsd(security,"calc_duration",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCalcDuration(security:list,*args,**kwargs):
    # 获取麦考利久期
    return w.wss(security,"calc_duration",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOThPayableSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他应付款时间序列
    return w.wsd(security,"oth_payable",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOThPayable(security:list,*args,**kwargs):
    # 获取其他应付款
    return w.wss(security,"oth_payable",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration30YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取30年久期时间序列
    return w.wsd(security,"duration_30y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration30Y(security:list,*args,**kwargs):
    # 获取30年久期
    return w.wss(security,"duration_30y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration20YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取20年久期时间序列
    return w.wsd(security,"duration_20y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration20Y(security:list,*args,**kwargs):
    # 获取20年久期
    return w.wss(security,"duration_20y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCalcChinaBondSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取收益率曲线(中债样本券)时间序列
    return w.wsd(security,"calc_chinabond",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCalcChinaBond(security:list,*args,**kwargs):
    # 获取收益率曲线(中债样本券)
    return w.wss(security,"calc_chinabond",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseCallOptionRecordDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取赎回登记日时间序列
    return w.wsd(security,"clause_calloption_recorddate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseCallOptionRecordDate(security:list,*args,**kwargs):
    # 获取赎回登记日
    return w.wss(security,"clause_calloption_recorddate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskReturnYearlySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取年化收益率时间序列
    return w.wsd(security,"risk_returnyearly",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskReturnYearly(security:list,*args,**kwargs):
    # 获取年化收益率
    return w.wss(security,"risk_returnyearly",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskReturnYearlyTradeDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取年化收益率(工作日)时间序列
    return w.wsd(security,"risk_returnyearly_tradedate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskReturnYearlyTradeDate(security:list,*args,**kwargs):
    # 获取年化收益率(工作日)
    return w.wss(security,"risk_returnyearly_tradedate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getConVpESeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取转股市盈率时间序列
    return w.wsd(security,"convpe",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getConVpE(security:list,*args,**kwargs):
    # 获取转股市盈率
    return w.wss(security,"convpe",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getConVpBSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取转股市净率时间序列
    return w.wsd(security,"convpb",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getConVpB(security:list,*args,**kwargs):
    # 获取转股市净率
    return w.wss(security,"convpb",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUnderlyingPeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取正股市盈率时间序列
    return w.wsd(security,"underlyingpe",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUnderlyingPe(security:list,*args,**kwargs):
    # 获取正股市盈率
    return w.wss(security,"underlyingpe",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUnderlyingPbSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取正股市净率时间序列
    return w.wsd(security,"underlyingpb",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUnderlyingPb(security:list,*args,**kwargs):
    # 获取正股市净率
    return w.wss(security,"underlyingpb",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTurnNdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取N日换手率时间序列
    return w.wsd(security,"turn_nd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTurnNd(security:list,*args,**kwargs):
    # 获取N日换手率
    return w.wss(security,"turn_nd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGSem03004Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取死亡事故数时间序列
    return w.wsd(security,"esg_sem03004",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGSem03004(security:list,*args,**kwargs):
    # 获取死亡事故数
    return w.wss(security,"esg_sem03004",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTurnFreePerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间换手率(基准.自由流通股本)时间序列
    return w.wsd(security,"turn_free_per",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTurnFreePer(security:list,*args,**kwargs):
    # 获取区间换手率(基准.自由流通股本)
    return w.wss(security,"turn_free_per",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGSem04001Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取医保覆盖率时间序列
    return w.wsd(security,"esg_sem04001",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGSem04001(security:list,*args,**kwargs):
    # 获取医保覆盖率
    return w.wss(security,"esg_sem04001",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTurnPerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间换手率时间序列
    return w.wsd(security,"turn_per",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTurnPer(security:list,*args,**kwargs):
    # 获取区间换手率
    return w.wss(security,"turn_per",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDepositReceivedSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取存入保证金时间序列
    return w.wsd(security,"deposit_received",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDepositReceived(security:list,*args,**kwargs):
    # 获取存入保证金
    return w.wss(security,"deposit_received",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClaimsPayableSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取应付赔付款时间序列
    return w.wsd(security,"claims_payable",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClaimsPayable(security:list,*args,**kwargs):
    # 获取应付赔付款
    return w.wss(security,"claims_payable",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowListedDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取增发上市日时间序列
    return w.wsd(security,"fellow_listeddate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowListedDate(security:list,*args,**kwargs):
    # 获取增发上市日
    return w.wss(security,"fellow_listeddate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteProfitApr3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取可分配利润时间序列
    return w.wsd(security,"stmnote_profitapr_3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteProfitApr3(security:list,*args,**kwargs):
    # 获取可分配利润
    return w.wss(security,"stmnote_profitapr_3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfFyTmSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取远期收益率时间序列
    return w.wsd(security,"tbf_FYTM",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTBfFyTm(security:list,*args,**kwargs):
    # 获取远期收益率
    return w.wss(security,"tbf_FYTM",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLtPayableSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取长期应付款时间序列
    return w.wsd(security,"lt_payable",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLtPayable(security:list,*args,**kwargs):
    # 获取长期应付款
    return w.wss(security,"lt_payable",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLtPayableToTSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取长期应付款(合计)时间序列
    return w.wsd(security,"lt_payable_tot",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLtPayableToT(security:list,*args,**kwargs):
    # 获取长期应付款(合计)
    return w.wss(security,"lt_payable_tot",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPctChgPer2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间涨跌幅(包含上市首日涨跌幅)时间序列
    return w.wsd(security,"pct_chg_per2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPctChgPer2(security:list,*args,**kwargs):
    # 获取区间涨跌幅(包含上市首日涨跌幅)
    return w.wss(security,"pct_chg_per2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCalcCleanSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取全价算净价时间序列
    return w.wsd(security,"calc_clean",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCalcClean(security:list,*args,**kwargs):
    # 获取全价算净价
    return w.wss(security,"calc_clean",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoPrePriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行前均价时间序列
    return w.wsd(security,"ipo_preprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoPrePrice(security:list,*args,**kwargs):
    # 获取发行前均价
    return w.wss(security,"ipo_preprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDiluteRateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取转股稀释率时间序列
    return w.wsd(security,"diluterate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDiluteRate(security:list,*args,**kwargs):
    # 获取转股稀释率
    return w.wss(security,"diluterate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSpecificItemPayableSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取专项应付款时间序列
    return w.wsd(security,"specific_item_payable",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSpecificItemPayable(security:list,*args,**kwargs):
    # 获取专项应付款
    return w.wss(security,"specific_item_payable",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClientsRsRvSettleSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取客户备付金时间序列
    return w.wsd(security,"clients_rsrv_settle",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClientsRsRvSettle(security:list,*args,**kwargs):
    # 获取客户备付金
    return w.wss(security,"clients_rsrv_settle",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUsTurnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取标的换手率时间序列
    return w.wsd(security,"us_turn",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUsTurn(security:list,*args,**kwargs):
    # 获取标的换手率
    return w.wss(security,"us_turn",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur7809Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取总投资资产时间序列
    return w.wsd(security,"stmnote_insur_7809",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur7809(security:list,*args,**kwargs):
    # 获取总投资资产
    return w.wss(security,"stmnote_insur_7809",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDBpSNewSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股净资产(最新公告)_GSD时间序列
    return w.wsd(security,"wgsd_bps_new",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDBpSNew(security:list,*args,**kwargs):
    # 获取每股净资产(最新公告)_GSD
    return w.wss(security,"wgsd_bps_new",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskAnnualIntervalYieldTradeDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间收益率(工作日年化)时间序列
    return w.wsd(security,"risk_annualintervalyield_tradedate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskAnnualIntervalYieldTradeDate(security:list,*args,**kwargs):
    # 获取区间收益率(工作日年化)
    return w.wss(security,"risk_annualintervalyield_tradedate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLongTermRecSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取长期应收款时间序列
    return w.wsd(security,"long_term_rec",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLongTermRec(security:list,*args,**kwargs):
    # 获取长期应收款
    return w.wss(security,"long_term_rec",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOiChgSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取持仓量变化时间序列
    return w.wsd(security,"oi_chg",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOiChg(security:list,*args,**kwargs):
    # 获取持仓量变化
    return w.wss(security,"oi_chg",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank421Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取非生息资产时间序列
    return w.wsd(security,"stmnote_bank_421",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank421(security:list,*args,**kwargs):
    # 获取非生息资产
    return w.wss(security,"stmnote_bank_421",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValPeDeductedTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取市盈率PE(TTM,扣除非经常性损益)_PIT时间序列
    return w.wsd(security,"val_pe_deducted_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getValPeDeductedTtM(security:list,*args,**kwargs):
    # 获取市盈率PE(TTM,扣除非经常性损益)_PIT
    return w.wss(security,"val_pe_deducted_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssuerActualSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取实际发行人时间序列
    return w.wsd(security,"issuer_actual",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssuerActual(security:list,*args,**kwargs):
    # 获取实际发行人
    return w.wss(security,"issuer_actual",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOiChangeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取持仓量变化(商品指数)时间序列
    return w.wsd(security,"oichange",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOiChange(security:list,*args,**kwargs):
    # 获取持仓量变化(商品指数)
    return w.wss(security,"oichange",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDBpSSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股净资产_GSD时间序列
    return w.wsd(security,"wgsd_bps",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDBpS(security:list,*args,**kwargs):
    # 获取每股净资产_GSD
    return w.wss(security,"wgsd_bps",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration15YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取15年久期时间序列
    return w.wsd(security,"duration_15y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDuration15Y(security:list,*args,**kwargs):
    # 获取15年久期
    return w.wss(security,"duration_15y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMrgnPaidSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取存出保证金时间序列
    return w.wsd(security,"mrgn_paid",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMrgnPaid(security:list,*args,**kwargs):
    # 获取存出保证金
    return w.wss(security,"mrgn_paid",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteDpsT4405Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取人民币存款时间序列
    return w.wsd(security,"stmnote_DPST_4405",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteDpsT4405(security:list,*args,**kwargs):
    # 获取人民币存款
    return w.wss(security,"stmnote_DPST_4405",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUsPctChangeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取标的涨跌幅时间序列
    return w.wsd(security,"us_pctchange",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getUsPctChange(security:list,*args,**kwargs):
    # 获取标的涨跌幅
    return w.wss(security,"us_pctchange",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPropRightUseSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取使用权资产时间序列
    return w.wsd(security,"prop_right_use",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPropRightUse(security:list,*args,**kwargs):
    # 获取使用权资产
    return w.wss(security,"prop_right_use",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSeatFeesExchangeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取交易席位费时间序列
    return w.wsd(security,"seat_fees_exchange",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSeatFeesExchange(security:list,*args,**kwargs):
    # 获取交易席位费
    return w.wss(security,"seat_fees_exchange",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWestReturnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取估算涨跌幅时间序列
    return w.wsd(security,"west_return",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWestReturn(security:list,*args,**kwargs):
    # 获取估算涨跌幅
    return w.wss(security,"west_return",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPctChgNdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取N日涨跌幅时间序列
    return w.wsd(security,"pct_chg_nd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPctChgNd(security:list,*args,**kwargs):
    # 获取N日涨跌幅
    return w.wss(security,"pct_chg_nd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFsPqPctChangeSettlementSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间涨跌幅(结算价)时间序列
    return w.wsd(security,"fs_pq_pctchange_settlement",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFsPqPctChangeSettlement(security:list,*args,**kwargs):
    # 获取区间涨跌幅(结算价)
    return w.wss(security,"fs_pq_pctchange_settlement",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取存出保证金_FUND时间序列
    return w.wsd(security,"stm_bs_3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs3(security:list,*args,**kwargs):
    # 获取存出保证金_FUND
    return w.wss(security,"stm_bs_3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOiPerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间持仓量时间序列
    return w.wsd(security,"oi_per",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOiPer(security:list,*args,**kwargs):
    # 获取区间持仓量
    return w.wss(security,"oi_per",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMaTotalSharesSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取备考总股本(并购后)时间序列
    return w.wsd(security,"matotalshares",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMaTotalShares(security:list,*args,**kwargs):
    # 获取备考总股本(并购后)
    return w.wss(security,"matotalshares",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstHightPriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最高中标价位时间序列
    return w.wsd(security,"tendrst_hightprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstHightPrice(security:list,*args,**kwargs):
    # 获取最高中标价位
    return w.wss(security,"tendrst_hightprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInterestFrequencySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每年付息次数时间序列
    return w.wsd(security,"interestfrequency",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInterestFrequency(security:list,*args,**kwargs):
    # 获取每年付息次数
    return w.wss(security,"interestfrequency",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCreditLineSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最新授信额度时间序列
    return w.wsd(security,"credit_line",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCreditLine(security:list,*args,**kwargs):
    # 获取最新授信额度
    return w.wss(security,"credit_line",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGuarFormerOutwardsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取对外担保余额时间序列
    return w.wsd(security,"guar_formeroutwards",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGuarFormerOutwards(security:list,*args,**kwargs):
    # 获取对外担保余额
    return w.wss(security,"guar_formeroutwards",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyGrNtRangeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取担保条款文字时间序列
    return w.wsd(security,"agency_grntrange",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyGrNtRange(security:list,*args,**kwargs):
    # 获取担保条款文字
    return w.wss(security,"agency_grntrange",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseItemSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取指定条款文字时间序列
    return w.wsd(security,"clauseitem",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseItem(security:list,*args,**kwargs):
    # 获取指定条款文字
    return w.wss(security,"clauseitem",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstLowPriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最低中标价位时间序列
    return w.wsd(security,"tendrst_lowprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstLowPrice(security:list,*args,**kwargs):
    # 获取最低中标价位
    return w.wss(security,"tendrst_lowprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsCurrentLoanSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取当前贷款笔数时间序列
    return w.wsd(security,"abs_currentloan",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsCurrentLoan(security:list,*args,**kwargs):
    # 获取当前贷款笔数
    return w.wss(security,"abs_currentloan",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseCallOptionRedemptionMemoSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取赎回价格说明时间序列
    return w.wsd(security,"clause_calloption_redemptionmemo",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseCallOptionRedemptionMemo(security:list,*args,**kwargs):
    # 获取赎回价格说明
    return w.wss(security,"clause_calloption_redemptionmemo",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInStYyIssuerRatingHisSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取主体评级历史(YY)时间序列
    return w.wsd(security,"inst_yyissuerratinghis",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInStYyIssuerRatingHis(security:list,*args,**kwargs):
    # 获取主体评级历史(YY)
    return w.wss(security,"inst_yyissuerratinghis",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseResetResetTimesLimitSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取修正次数限制时间序列
    return w.wsd(security,"clause_reset_resettimeslimit",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseResetResetTimesLimit(security:list,*args,**kwargs):
    # 获取修正次数限制
    return w.wss(security,"clause_reset_resettimeslimit",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClausePutOptionResellingPriceExplainAtionSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取回售价格说明时间序列
    return w.wsd(security,"clause_putoption_resellingpriceexplaination",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClausePutOptionResellingPriceExplainAtion(security:list,*args,**kwargs):
    # 获取回售价格说明
    return w.wss(security,"clause_putoption_resellingpriceexplaination",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseResetResetRangeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取特别修正幅度时间序列
    return w.wsd(security,"clause_reset_resetrange",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseResetResetRange(security:list,*args,**kwargs):
    # 获取特别修正幅度
    return w.wss(security,"clause_reset_resetrange",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsCurrentLoansSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取当前贷款余额时间序列
    return w.wsd(security,"abs_currentloans",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsCurrentLoans(security:list,*args,**kwargs):
    # 获取当前贷款余额
    return w.wss(security,"abs_currentloans",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPrepayPortionSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取提前还本比例时间序列
    return w.wsd(security,"prepayportion",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPrepayPortion(security:list,*args,**kwargs):
    # 获取提前还本比例
    return w.wss(security,"prepayportion",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClausePutOptionRedeemTriggerProportionSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取回售触发比例时间序列
    return w.wsd(security,"clause_putoption_redeem_triggerproportion",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClausePutOptionRedeemTriggerProportion(security:list,*args,**kwargs):
    # 获取回售触发比例
    return w.wss(security,"clause_putoption_redeem_triggerproportion",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyExAccountantSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取会计师事务所时间序列
    return w.wsd(security,"agency_exaccountant",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyExAccountant(security:list,*args,**kwargs):
    # 获取会计师事务所
    return w.wss(security,"agency_exaccountant",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFinaMatSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取存量债券余额(按期限)时间序列
    return w.wsd(security,"fina_mat",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFinaMat(security:list,*args,**kwargs):
    # 获取存量债券余额(按期限)
    return w.wss(security,"fina_mat",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueFeeUnderWRtspOnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取承销保荐费用时间序列
    return w.wsd(security,"issuefee_underwrtspon",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueFeeUnderWRtspOn(security:list,*args,**kwargs):
    # 获取承销保荐费用
    return w.wss(security,"issuefee_underwrtspon",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCreditFormerLineSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取历史授信额度时间序列
    return w.wsd(security,"credit_formerline",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCreditFormerLine(security:list,*args,**kwargs):
    # 获取历史授信额度
    return w.wss(security,"credit_formerline",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEem02001Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取氮氧化物排放时间序列
    return w.wsd(security,"esg_eem02001",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEem02001(security:list,*args,**kwargs):
    # 获取氮氧化物排放
    return w.wss(security,"esg_eem02001",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEem02002Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取二氧化硫排放时间序列
    return w.wsd(security,"esg_eem02002",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEsGEem02002(security:list,*args,**kwargs):
    # 获取二氧化硫排放
    return w.wss(security,"esg_eem02002",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseCallOptionTriggerProportionSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取赎回触发比例时间序列
    return w.wsd(security,"clause_calloption_triggerproportion",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseCallOptionTriggerProportion(security:list,*args,**kwargs):
    # 获取赎回触发比例
    return w.wss(security,"clause_calloption_triggerproportion",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseInterest6Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取补偿利率说明时间序列
    return w.wsd(security,"clause_interest_6",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseInterest6(security:list,*args,**kwargs):
    # 获取补偿利率说明
    return w.wss(security,"clause_interest_6",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGuarLatestBalanceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最新担保余额时间序列
    return w.wsd(security,"guar_latestbalance",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGuarLatestBalance(security:list,*args,**kwargs):
    # 获取最新担保余额
    return w.wss(security,"guar_latestbalance",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRepoLastEstDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最新交易日期时间序列
    return w.wsd(security,"repo_lastestdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRepoLastEstDate(security:list,*args,**kwargs):
    # 获取最新交易日期
    return w.wss(security,"repo_lastestdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCreditRatingAgencySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取信用评估机构时间序列
    return w.wsd(security,"creditratingagency",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCreditRatingAgency(security:list,*args,**kwargs):
    # 获取信用评估机构
    return w.wss(security,"creditratingagency",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderAvgPctSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取户均持股比例时间序列
    return w.wsd(security,"holder_avgpct",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderAvgPct(security:list,*args,**kwargs):
    # 获取户均持股比例
    return w.wss(security,"holder_avgpct",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGuarFormerBalanceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取历史担保余额时间序列
    return w.wsd(security,"guar_formerbalance",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGuarFormerBalance(security:list,*args,**kwargs):
    # 获取历史担保余额
    return w.wss(security,"guar_formerbalance",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGuarFormerInwardsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取对内担保余额时间序列
    return w.wsd(security,"guar_formerinwards",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGuarFormerInwards(security:list,*args,**kwargs):
    # 获取对内担保余额
    return w.wss(security,"guar_formerinwards",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCreditLineDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最新授信日期时间序列
    return w.wsd(security,"credit_linedate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCreditLineDate(security:list,*args,**kwargs):
    # 获取最新授信日期
    return w.wss(security,"credit_linedate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundHoldFundsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取持有基金家数时间序列
    return w.wsd(security,"fundhold_funds",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundHoldFunds(security:list,*args,**kwargs):
    # 获取持有基金家数
    return w.wss(security,"fundhold_funds",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderTotalByBySecSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取券商持股数量时间序列
    return w.wsd(security,"holder_totalbybysec",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderTotalByBySec(security:list,*args,**kwargs):
    # 获取券商持股数量
    return w.wss(security,"holder_totalbybysec",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderPriceFellowOnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取定向增发价格时间序列
    return w.wsd(security,"holder_price_fellowon",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderPriceFellowOn(security:list,*args,**kwargs):
    # 获取定向增发价格
    return w.wss(security,"holder_price_fellowon",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsWeightedAverageMaturityWithPrepaySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取加权平均期限时间序列
    return w.wsd(security,"abs_weightedaveragematuritywithprepay",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsWeightedAverageMaturityWithPrepay(security:list,*args,**kwargs):
    # 获取加权平均期限
    return w.wss(security,"abs_weightedaveragematuritywithprepay",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAmountSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最新债项评级时间序列
    return w.wsd(security,"amount",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAmount(security:list,*args,**kwargs):
    # 获取最新债项评级
    return w.wss(security,"amount",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTrancheSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取各级发行总额时间序列
    return w.wsd(security,"tranche",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTranche(security:list,*args,**kwargs):
    # 获取各级发行总额
    return w.wss(security,"tranche",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstBidPriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取全场中标价格时间序列
    return w.wsd(security,"tendrst_bidprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstBidPrice(security:list,*args,**kwargs):
    # 获取全场中标价格
    return w.wss(security,"tendrst_bidprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstBidSpreadSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取全场中标利差时间序列
    return w.wsd(security,"tendrst_bidspread",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstBidSpread(security:list,*args,**kwargs):
    # 获取全场中标利差
    return w.wss(security,"tendrst_bidspread",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsFiExdCapitalCostRateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取固定资金成本时间序列
    return w.wsd(security,"abs_fiexdcapitalcostrate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsFiExdCapitalCostRate(security:list,*args,**kwargs):
    # 获取固定资金成本
    return w.wss(security,"abs_fiexdcapitalcostrate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLatestParSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取债券最新面值时间序列
    return w.wsd(security,"latestpar",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLatestPar(security:list,*args,**kwargs):
    # 获取债券最新面值
    return w.wss(security,"latestpar",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseConversion2IsForcedSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取是否强制转股时间序列
    return w.wsd(security,"clause_conversion_2_isforced",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseConversion2IsForced(security:list,*args,**kwargs):
    # 获取是否强制转股
    return w.wss(security,"clause_conversion_2_isforced",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getParSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取债券初始面值时间序列
    return w.wsd(security,"par",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPar(security:list,*args,**kwargs):
    # 获取债券初始面值
    return w.wss(security,"par",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getListFloorSubsCrOfFlSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取网下申购下限时间序列
    return w.wsd(security,"list_floorsubscroffl",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getListFloorSubsCrOfFl(security:list,*args,**kwargs):
    # 获取网下申购下限
    return w.wss(security,"list_floorsubscroffl",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getConditionalPutPriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取有条件回售价时间序列
    return w.wsd(security,"conditionalputprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getConditionalPutPrice(security:list,*args,**kwargs):
    # 获取有条件回售价
    return w.wss(security,"conditionalputprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClausePutOptionPutBackTimesPerYearSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每年回售次数时间序列
    return w.wsd(security,"clause_putoption_putbacktimesperyear",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClausePutOptionPutBackTimesPerYear(security:list,*args,**kwargs):
    # 获取每年回售次数
    return w.wss(security,"clause_putoption_putbacktimesperyear",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClausePutOptionPutBackAdditionalConditionSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取附加回售条件时间序列
    return w.wsd(security,"clause_putoption_putbackadditionalcondition",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClausePutOptionPutBackAdditionalCondition(security:list,*args,**kwargs):
    # 获取附加回售条件
    return w.wss(security,"clause_putoption_putbackadditionalcondition",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderPctByBankSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取银行持股比例时间序列
    return w.wsd(security,"holder_pctbybank",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderPctByBank(security:list,*args,**kwargs):
    # 获取银行持股比例
    return w.wss(security,"holder_pctbybank",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderPctBySecSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取券商持股比例时间序列
    return w.wsd(security,"holder_pctbysec",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderPctBySec(security:list,*args,**kwargs):
    # 获取券商持股比例
    return w.wss(security,"holder_pctbysec",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderPctByFundSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金持股比例时间序列
    return w.wsd(security,"holder_pctbyfund",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderPctByFund(security:list,*args,**kwargs):
    # 获取基金持股比例
    return w.wss(security,"holder_pctbyfund",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClausePutOptionPutBackPriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取无条件回售价时间序列
    return w.wsd(security,"clause_putoption_putbackprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClausePutOptionPutBackPrice(security:list,*args,**kwargs):
    # 获取无条件回售价
    return w.wss(security,"clause_putoption_putbackprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsAssetServiceAgencySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资产服务机构时间序列
    return w.wsd(security,"abs_assetserviceagency",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsAssetServiceAgency(security:list,*args,**kwargs):
    # 获取资产服务机构
    return w.wss(security,"abs_assetserviceagency",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstPrivateTradeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取自营中标总量时间序列
    return w.wsd(security,"tendrst_privatetrade",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstPrivateTrade(security:list,*args,**kwargs):
    # 获取自营中标总量
    return w.wss(security,"tendrst_privatetrade",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClausePutOptionPutBackPeriodSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取无条件回售期时间序列
    return w.wsd(security,"clause_putoption_putbackperiod",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClausePutOptionPutBackPeriod(security:list,*args,**kwargs):
    # 获取无条件回售期
    return w.wss(security,"clause_putoption_putbackperiod",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoOvRSubRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取超额认购倍数时间序列
    return w.wsd(security,"ipo_ovrsubratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoOvRSubRatio(security:list,*args,**kwargs):
    # 获取超额认购倍数
    return w.wss(security,"ipo_ovrsubratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCityInvestmentBondGeoWindSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取城投行政级别(Wind)时间序列
    return w.wsd(security,"cityinvestmentbondgeoWind",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCityInvestmentBondGeoWind(security:list,*args,**kwargs):
    # 获取城投行政级别(Wind)
    return w.wss(security,"cityinvestmentbondgeoWind",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCityInvestmentBondGeoSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取城投行政级别时间序列
    return w.wsd(security,"cityinvestmentbondgeo",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCityInvestmentBondGeo(security:list,*args,**kwargs):
    # 获取城投行政级别
    return w.wss(security,"cityinvestmentbondgeo",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundHoldBondValueSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金持债市值时间序列
    return w.wsd(security,"fundholdbond_value",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundHoldBondValue(security:list,*args,**kwargs):
    # 获取基金持债市值
    return w.wss(security,"fundholdbond_value",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderTotalByFundSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金持股数量时间序列
    return w.wsd(security,"holder_totalbyfund",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderTotalByFund(security:list,*args,**kwargs):
    # 获取基金持股数量
    return w.wss(security,"holder_totalbyfund",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCbIssueAmountSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取转债发行总额时间序列
    return w.wsd(security,"cb_issueamount",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCbIssueAmount(security:list,*args,**kwargs):
    # 获取转债发行总额
    return w.wss(security,"cb_issueamount",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderAmountPlanSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取计划发行总额(文字)时间序列
    return w.wsd(security,"tender_amountplan",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderAmountPlan(security:list,*args,**kwargs):
    # 获取计划发行总额(文字)
    return w.wss(security,"tender_amountplan",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRateFwdIssuerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取主体评级展望时间序列
    return w.wsd(security,"rate_fwdissuer",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRateFwdIssuer(security:list,*args,**kwargs):
    # 获取主体评级展望
    return w.wss(security,"rate_fwdissuer",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsPenetrateActRuAlDebtorSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取穿透信用主体时间序列
    return w.wsd(security,"abs_penetrateactrualdebtor",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsPenetrateActRuAlDebtor(security:list,*args,**kwargs):
    # 获取穿透信用主体
    return w.wss(security,"abs_penetrateactrualdebtor",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFinalTotalAmOutAnytimeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取存量债券余额(支持历史)时间序列
    return w.wsd(security,"final_totalamout_anytime",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFinalTotalAmOutAnytime(security:list,*args,**kwargs):
    # 获取存量债券余额(支持历史)
    return w.wss(security,"final_totalamout_anytime",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRateFormerSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取历史债项评级时间序列
    return w.wsd(security,"rate_former",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRateFormer(security:list,*args,**kwargs):
    # 获取历史债项评级
    return w.wss(security,"rate_former",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCbResultRationAmtOffSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取网下获配金额时间序列
    return w.wsd(security,"cb_result_rationamtoff",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCbResultRationAmtOff(security:list,*args,**kwargs):
    # 获取网下获配金额
    return w.wss(security,"cb_result_rationamtoff",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFinaTotalAmountSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取存量债券余额时间序列
    return w.wsd(security,"fina_totalamount",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFinaTotalAmount(security:list,*args,**kwargs):
    # 获取存量债券余额
    return w.wss(security,"fina_totalamount",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRateAgencyBondSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取债项评级机构时间序列
    return w.wsd(security,"rate_agencybond",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRateAgencyBond(security:list,*args,**kwargs):
    # 获取债项评级机构
    return w.wss(security,"rate_agencybond",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundHoldBondNamesSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取持有基金名称时间序列
    return w.wsd(security,"fundholdbond_names",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundHoldBondNames(security:list,*args,**kwargs):
    # 获取持有基金名称
    return w.wss(security,"fundholdbond_names",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyRecommendErSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取上市保荐机构(上市推荐人)时间序列
    return w.wsd(security,"agency_recommender",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyRecommendEr(security:list,*args,**kwargs):
    # 获取上市保荐机构(上市推荐人)
    return w.wss(security,"agency_recommender",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCbResultRationRatioOnLSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取网上获配比例时间序列
    return w.wsd(security,"cb_result_rationratioonl",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCbResultRationRatioOnL(security:list,*args,**kwargs):
    # 获取网上获配比例
    return w.wss(security,"cb_result_rationratioonl",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getConditionalCallPriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取有条件赎回价时间序列
    return w.wsd(security,"conditionalcallprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getConditionalCallPrice(security:list,*args,**kwargs):
    # 获取有条件赎回价
    return w.wss(security,"conditionalcallprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIsAssetOutSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资产是否出表时间序列
    return w.wsd(security,"isassetout",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIsAssetOut(security:list,*args,**kwargs):
    # 获取资产是否出表
    return w.wss(security,"isassetout",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCbResultRationAmToNlSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取网上获配金额时间序列
    return w.wsd(security,"cb_result_rationamtonl",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCbResultRationAmToNl(security:list,*args,**kwargs):
    # 获取网上获配金额
    return w.wss(security,"cb_result_rationamtonl",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getListLimitSubsCroNlSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取网上申购上限时间序列
    return w.wsd(security,"list_limitsubscronl",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getListLimitSubsCroNl(security:list,*args,**kwargs):
    # 获取网上申购上限
    return w.wss(security,"list_limitsubscronl",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getListStepSizeSubsCroNlSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取网上申购步长时间序列
    return w.wsd(security,"list_stepsizesubscronl",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getListStepSizeSubsCroNl(security:list,*args,**kwargs):
    # 获取网上申购步长
    return w.wss(security,"list_stepsizesubscronl",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getListFloorSubsCroNlSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取网上申购下限时间序列
    return w.wsd(security,"list_floorsubscronl",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getListFloorSubsCroNl(security:list,*args,**kwargs):
    # 获取网上申购下限
    return w.wss(security,"list_floorsubscronl",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseProcessModeInterestSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取利息处理方式时间序列
    return w.wsd(security,"clause_processmodeinterest",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseProcessModeInterest(security:list,*args,**kwargs):
    # 获取利息处理方式
    return w.wss(security,"clause_processmodeinterest",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getListLimitSubsCrOfFlSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取网下申购上限时间序列
    return w.wsd(security,"list_limitsubscroffl",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getListLimitSubsCrOfFl(security:list,*args,**kwargs):
    # 获取网下申购上限
    return w.wss(security,"list_limitsubscroffl",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstAmountActSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取实际发行总额时间序列
    return w.wsd(security,"tendrst_amountact",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstAmountAct(security:list,*args,**kwargs):
    # 获取实际发行总额
    return w.wss(security,"tendrst_amountact",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstFinAnCouponSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最终票面利率时间序列
    return w.wsd(security,"tendrst_financoupon",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstFinAnCoupon(security:list,*args,**kwargs):
    # 获取最终票面利率
    return w.wss(security,"tendrst_financoupon",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPrepayMethodSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取提前还本方式时间序列
    return w.wsd(security,"prepaymethod",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPrepayMethod(security:list,*args,**kwargs):
    # 获取提前还本方式
    return w.wss(security,"prepaymethod",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstBidRateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取全场中标利率时间序列
    return w.wsd(security,"tendrst_bidrate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstBidRate(security:list,*args,**kwargs):
    # 获取全场中标利率
    return w.wss(security,"tendrst_bidrate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseConversion2ForceConvertPriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取强制转股价格时间序列
    return w.wsd(security,"clause_conversion_2_forceconvertprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClauseConversion2ForceConvertPrice(security:list,*args,**kwargs):
    # 获取强制转股价格
    return w.wss(security,"clause_conversion_2_forceconvertprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueAmountPlanSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取计划发行总额时间序列
    return w.wsd(security,"issue_amountplan",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueAmountPlan(security:list,*args,**kwargs):
    # 获取计划发行总额
    return w.wss(security,"issue_amountplan",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderTotalByBankSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取银行持股数量时间序列
    return w.wsd(security,"holder_totalbybank",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderTotalByBank(security:list,*args,**kwargs):
    # 获取银行持股数量
    return w.wss(security,"holder_totalbybank",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsoluteHighestQuatreTurnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最高季度回报时间序列
    return w.wsd(security,"absolute_highestquatreturn",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsoluteHighestQuatreTurn(security:list,*args,**kwargs):
    # 获取最高季度回报
    return w.wss(security,"absolute_highestquatreturn",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundExchangeShortnameSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金场内简称时间序列
    return w.wsd(security,"fund_exchangeshortname",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundExchangeShortname(security:list,*args,**kwargs):
    # 获取基金场内简称
    return w.wss(security,"fund_exchangeshortname",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteEoItems15Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取企业重组费用时间序列
    return w.wsd(security,"stmnote_Eoitems_15",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteEoItems15(security:list,*args,**kwargs):
    # 获取企业重组费用
    return w.wss(security,"stmnote_Eoitems_15",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteImpairmentLoss5Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取存货跌价损失时间序列
    return w.wsd(security,"stmnote_ImpairmentLoss_5",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteImpairmentLoss5(security:list,*args,**kwargs):
    # 获取存货跌价损失
    return w.wss(security,"stmnote_ImpairmentLoss_5",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthRoeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净资产收益率(N年,增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_roe",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthRoe(security:list,*args,**kwargs):
    # 获取净资产收益率(N年,增长率)_GSD
    return w.wss(security,"wgsd_growth_roe",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthEps3YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基本每股收益(近3年增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_eps_3y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthEps3Y(security:list,*args,**kwargs):
    # 获取基本每股收益(近3年增长率)_GSD
    return w.wss(security,"wgsd_growth_eps_3y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthEps1YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基本每股收益(近1年增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_eps_1y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthEps1Y(security:list,*args,**kwargs):
    # 获取基本每股收益(近1年增长率)_GSD
    return w.wss(security,"wgsd_growth_eps_1y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthTotalEquity3YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取股东权益合计(近3年增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_totalequity_3y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthTotalEquity3Y(security:list,*args,**kwargs):
    # 获取股东权益合计(近3年增长率)_GSD
    return w.wss(security,"wgsd_growth_totalequity_3y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthTotalEquity1YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取股东权益合计(近1年增长率)_GSD时间序列
    return w.wsd(security,"wgsd_growth_totalequity_1y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDGrowthTotalEquity1Y(security:list,*args,**kwargs):
    # 获取股东权益合计(近1年增长率)_GSD
    return w.wss(security,"wgsd_growth_totalequity_1y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrowthRoeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净资产收益率(N年,增长率)时间序列
    return w.wsd(security,"growth_roe",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGrowthRoe(security:list,*args,**kwargs):
    # 获取净资产收益率(N年,增长率)
    return w.wss(security,"growth_roe",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteRdExpSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取研发支出合计时间序列
    return w.wsd(security,"stmnote_RDexp",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteRdExp(security:list,*args,**kwargs):
    # 获取研发支出合计
    return w.wss(security,"stmnote_RDexp",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteRdEmployeeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取研发人员数量时间序列
    return w.wsd(security,"stmnote_RDemployee",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteRdEmployee(security:list,*args,**kwargs):
    # 获取研发人员数量
    return w.wss(security,"stmnote_RDemployee",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSupplierTop5Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取大供应商名称时间序列
    return w.wsd(security,"stmnote_suppliertop5",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSupplierTop5(security:list,*args,**kwargs):
    # 获取大供应商名称
    return w.wss(security,"stmnote_suppliertop5",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs201Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取权证投资收益_FUND时间序列
    return w.wsd(security,"stm_is_201",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs201(security:list,*args,**kwargs):
    # 获取权证投资收益_FUND
    return w.wss(security,"stm_is_201",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取债券投资收益_FUND时间序列
    return w.wsd(security,"stm_is_2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs2(security:list,*args,**kwargs):
    # 获取债券投资收益_FUND
    return w.wss(security,"stm_is_2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs75Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金投资收益_FUND时间序列
    return w.wsd(security,"stm_is_75",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs75(security:list,*args,**kwargs):
    # 获取基金投资收益_FUND
    return w.wss(security,"stm_is_75",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs1Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取股票投资收益_FUND时间序列
    return w.wsd(security,"stm_is_1",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs1(security:list,*args,**kwargs):
    # 获取股票投资收益_FUND
    return w.wss(security,"stm_is_1",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInvestmentIncome0009Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他投资收益时间序列
    return w.wsd(security,"stmnote_InvestmentIncome_0009",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInvestmentIncome0009(security:list,*args,**kwargs):
    # 获取其他投资收益
    return w.wss(security,"stmnote_InvestmentIncome_0009",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur6Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取总投资收益率时间序列
    return w.wsd(security,"stmnote_insur_6",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur6(security:list,*args,**kwargs):
    # 获取总投资收益率
    return w.wss(security,"stmnote_insur_6",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur5Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取净投资收益率时间序列
    return w.wsd(security,"stmnote_insur_5",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteInSur5(security:list,*args,**kwargs):
    # 获取净投资收益率
    return w.wss(security,"stmnote_insur_5",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsRealEstateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取投资性房地产时间序列
    return w.wsd(security,"stm07_bs_reits_realestate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsRealEstate(security:list,*args,**kwargs):
    # 获取投资性房地产
    return w.wss(security,"stm07_bs_reits_realestate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSeg1702Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取主营业务成本时间序列
    return w.wsd(security,"stmnote_seg_1702",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSeg1702(security:list,*args,**kwargs):
    # 获取主营业务成本
    return w.wss(security,"stmnote_seg_1702",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSeg1701Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取主营业务收入时间序列
    return w.wsd(security,"stmnote_seg_1701",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSeg1701(security:list,*args,**kwargs):
    # 获取主营业务收入
    return w.wss(security,"stmnote_seg_1701",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAssetsGapDetailSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资产差额说明(特殊报表科目)时间序列
    return w.wsd(security,"assets_gap_detail",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAssetsGapDetail(security:list,*args,**kwargs):
    # 获取资产差额说明(特殊报表科目)
    return w.wss(security,"assets_gap_detail",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGainAssetDispositionsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资产处置收益时间序列
    return w.wsd(security,"gain_asset_dispositions",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getGainAssetDispositions(security:list,*args,**kwargs):
    # 获取资产处置收益
    return w.wss(security,"gain_asset_dispositions",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteEoItems14Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取债务重组损益时间序列
    return w.wsd(security,"stmnote_Eoitems_14",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteEoItems14(security:list,*args,**kwargs):
    # 获取债务重组损益
    return w.wss(security,"stmnote_Eoitems_14",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteEoItems12Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取委托投资损益时间序列
    return w.wsd(security,"stmnote_Eoitems_12",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteEoItems12(security:list,*args,**kwargs):
    # 获取委托投资损益
    return w.wss(security,"stmnote_Eoitems_12",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaNaTurnTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净资产周转率(TTM)_PIT时间序列
    return w.wsd(security,"fa_naturn_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaNaTurnTtM(security:list,*args,**kwargs):
    # 获取净资产周转率(TTM)_PIT
    return w.wss(security,"fa_naturn_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaRoaEbItTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总资产报酬率(TTM)_PIT时间序列
    return w.wsd(security,"fa_roaebit_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaRoaEbItTtM(security:list,*args,**kwargs):
    # 获取总资产报酬率(TTM)_PIT
    return w.wss(security,"fa_roaebit_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaRoeNpTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净资产收益率(TTM)_PIT时间序列
    return w.wsd(security,"fa_roenp_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaRoeNpTtM(security:list,*args,**kwargs):
    # 获取净资产收益率(TTM)_PIT
    return w.wss(security,"fa_roenp_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaRoeExDilutedSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净资产收益率(扣除/摊薄)_PIT时间序列
    return w.wsd(security,"fa_roe_exdiluted",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaRoeExDiluted(security:list,*args,**kwargs):
    # 获取净资产收益率(扣除/摊薄)_PIT
    return w.wss(security,"fa_roe_exdiluted",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaRoeExBasicSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净资产收益率(扣除/加权)_PIT时间序列
    return w.wsd(security,"fa_roe_exbasic",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaRoeExBasic(security:list,*args,**kwargs):
    # 获取净资产收益率(扣除/加权)_PIT
    return w.wss(security,"fa_roe_exbasic",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaRoeDilutedSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净资产收益率(摊薄)_PIT时间序列
    return w.wsd(security,"fa_roe_diluted",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaRoeDiluted(security:list,*args,**kwargs):
    # 获取净资产收益率(摊薄)_PIT
    return w.wss(security,"fa_roe_diluted",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaRoeWGtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净资产收益率(加权)_PIT时间序列
    return w.wsd(security,"fa_roe_wgt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaRoeWGt(security:list,*args,**kwargs):
    # 获取净资产收益率(加权)_PIT
    return w.wss(security,"fa_roe_wgt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaRoeAvgSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净资产收益率(平均)_PIT时间序列
    return w.wsd(security,"fa_roe_avg",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaRoeAvg(security:list,*args,**kwargs):
    # 获取净资产收益率(平均)_PIT
    return w.wss(security,"fa_roe_avg",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRoa2TtM3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取总资产报酬率(TTM)_GSD时间序列
    return w.wsd(security,"roa2_ttm3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRoa2TtM3(security:list,*args,**kwargs):
    # 获取总资产报酬率(TTM)_GSD
    return w.wss(security,"roa2_ttm3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRoaTtM2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取总资产净利率(TTM)_GSD时间序列
    return w.wsd(security,"roa_ttm2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRoaTtM2(security:list,*args,**kwargs):
    # 获取总资产净利率(TTM)_GSD
    return w.wss(security,"roa_ttm2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank0005Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取逾期贷款合计时间序列
    return w.wsd(security,"stmnote_bank_0005",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank0005(security:list,*args,**kwargs):
    # 获取逾期贷款合计
    return w.wss(security,"stmnote_bank_0005",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRoeTtM3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取净资产收益率(TTM)_GSD时间序列
    return w.wsd(security,"roe_ttm3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRoeTtM3(security:list,*args,**kwargs):
    # 获取净资产收益率(TTM)_GSD
    return w.wss(security,"roe_ttm3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteReserve38Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款呆账准备时间序列
    return w.wsd(security,"stmnote_reserve_38",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteReserve38(security:list,*args,**kwargs):
    # 获取贷款呆账准备
    return w.wss(security,"stmnote_reserve_38",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRoaYearlySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总资产净利率(年化)_GSD时间序列
    return w.wsd(security,"wgsd_roa_yearly",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRoaYearly(security:list,*args,**kwargs):
    # 获取总资产净利率(年化)_GSD
    return w.wss(security,"wgsd_roa_yearly",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRoaSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总资产净利率_GSD时间序列
    return w.wsd(security,"wgsd_roa",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRoa(security:list,*args,**kwargs):
    # 获取总资产净利率_GSD
    return w.wss(security,"wgsd_roa",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRoeYearlySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净资产收益率(年化)_GSD时间序列
    return w.wsd(security,"wgsd_roe_yearly",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRoeYearly(security:list,*args,**kwargs):
    # 获取净资产收益率(年化)_GSD
    return w.wss(security,"wgsd_roe_yearly",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRoeDeductedSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净资产收益率(扣除)_GSD时间序列
    return w.wsd(security,"wgsd_roe_deducted",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRoeDeducted(security:list,*args,**kwargs):
    # 获取净资产收益率(扣除)_GSD
    return w.wss(security,"wgsd_roe_deducted",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRoeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净资产收益率_GSD时间序列
    return w.wsd(security,"wgsd_roe",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRoe(security:list,*args,**kwargs):
    # 获取净资产收益率_GSD
    return w.wss(security,"wgsd_roe",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRoa2TtM2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取总资产报酬率(TTM)时间序列
    return w.wsd(security,"roa2_ttm2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRoa2TtM2(security:list,*args,**kwargs):
    # 获取总资产报酬率(TTM)
    return w.wss(security,"roa2_ttm2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaRoeTtMAvgSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净资产收益率(TTM,平均)时间序列
    return w.wsd(security,"fa_roe_ttmavg",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaRoeTtMAvg(security:list,*args,**kwargs):
    # 获取净资产收益率(TTM,平均)
    return w.wss(security,"fa_roe_ttmavg",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRoeTtM2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取净资产收益率(TTM)时间序列
    return w.wsd(security,"roe_ttm2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRoeTtM2(security:list,*args,**kwargs):
    # 获取净资产收益率(TTM)
    return w.wss(security,"roe_ttm2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteDpsT4411Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他货币存款(折算人民币)时间序列
    return w.wsd(security,"stmnote_DPST_4411",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteDpsT4411(security:list,*args,**kwargs):
    # 获取其他货币存款(折算人民币)
    return w.wss(security,"stmnote_DPST_4411",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRoa2YearlySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总资产报酬率(年化)_GSD时间序列
    return w.wsd(security,"wgsd_roa2_yearly",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRoa2Yearly(security:list,*args,**kwargs):
    # 获取总资产报酬率(年化)_GSD
    return w.wss(security,"wgsd_roa2_yearly",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteReserve1Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取坏账准备合计时间序列
    return w.wsd(security,"stmnote_reserve_1",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteReserve1(security:list,*args,**kwargs):
    # 获取坏账准备合计
    return w.wss(security,"stmnote_reserve_1",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundStmIssuingDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取中(年)报披露日期时间序列
    return w.wsd(security,"fund_stm_issuingdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundStmIssuingDate(security:list,*args,**kwargs):
    # 获取中(年)报披露日期
    return w.wss(security,"fund_stm_issuingdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoYRoeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净资产收益率(摊薄)(同比增长率)时间序列
    return w.wsd(security,"yoyroe",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoYRoe(security:list,*args,**kwargs):
    # 获取净资产收益率(摊薄)(同比增长率)
    return w.wss(security,"yoyroe",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaEquityAssetRadioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取股东权益比率_PIT时间序列
    return w.wsd(security,"fa_equityassetradio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaEquityAssetRadio(security:list,*args,**kwargs):
    # 获取股东权益比率_PIT
    return w.wss(security,"fa_equityassetradio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoOldSharesRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取老股转让比例时间序列
    return w.wsd(security,"ipo_oldsharesratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoOldSharesRatio(security:list,*args,**kwargs):
    # 获取老股转让比例
    return w.wss(security,"ipo_oldsharesratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoCollectionTotalSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取募集资金总额(含股东售股)时间序列
    return w.wsd(security,"ipo_collection_total",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoCollectionTotal(security:list,*args,**kwargs):
    # 获取募集资金总额(含股东售股)
    return w.wss(security,"ipo_collection_total",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoCollectionSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取首发募集资金时间序列
    return w.wsd(security,"ipo_collection",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoCollection(security:list,*args,**kwargs):
    # 获取首发募集资金
    return w.wss(security,"ipo_collection",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaDebtToEqYSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净资产负债率时间序列
    return w.wsd(security,"fa_debttoeqy",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaDebtToEqY(security:list,*args,**kwargs):
    # 获取净资产负债率
    return w.wss(security,"fa_debttoeqy",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoCollectionOldShares2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取股东售股金额时间序列
    return w.wsd(security,"ipo_collection_oldshares2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoCollectionOldShares2(security:list,*args,**kwargs):
    # 获取股东售股金额
    return w.wss(security,"ipo_collection_oldshares2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOCFToOpSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取现金营运指数时间序列
    return w.wsd(security,"ocftoop",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOCFToOp(security:list,*args,**kwargs):
    # 获取现金营运指数
    return w.wss(security,"ocftoop",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoPoCOnlineSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取网上发行数量(回拨前)时间序列
    return w.wsd(security,"ipo_poc_online",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoPoCOnline(security:list,*args,**kwargs):
    # 获取网上发行数量(回拨前)
    return w.wss(security,"ipo_poc_online",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoPoCOfflineSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取网下发行数量(回拨前)时间序列
    return w.wsd(security,"ipo_poc_offline",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoPoCOffline(security:list,*args,**kwargs):
    # 获取网下发行数量(回拨前)
    return w.wss(security,"ipo_poc_offline",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueIssueOlSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取网上发行数量时间序列
    return w.wsd(security,"issue_issueol",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueIssueOl(security:list,*args,**kwargs):
    # 获取网上发行数量
    return w.wss(security,"issue_issueol",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCbListIssueVolOnLSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取网上发行数量(不含优先配售)时间序列
    return w.wsd(security,"cb_list_issuevolonl",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCbListIssueVolOnL(security:list,*args,**kwargs):
    # 获取网上发行数量(不含优先配售)
    return w.wss(security,"cb_list_issuevolonl",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowOtcAmtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取网下发行数量时间序列
    return w.wsd(security,"fellow_otcamt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowOtcAmt(security:list,*args,**kwargs):
    # 获取网下发行数量
    return w.wss(security,"fellow_otcamt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoWpIpReleasingDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取申报预披露日时间序列
    return w.wsd(security,"ipo_WpipReleasingdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoWpIpReleasingDate(security:list,*args,**kwargs):
    # 获取申报预披露日
    return w.wss(security,"ipo_WpipReleasingdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoLeadUndRSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取首发主承销商时间序列
    return w.wsd(security,"ipo_leadundr",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoLeadUndR(security:list,*args,**kwargs):
    # 获取首发主承销商
    return w.wss(security,"ipo_leadundr",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoSponsorSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取首发保荐机构时间序列
    return w.wsd(security,"ipo_sponsor",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoSponsor(security:list,*args,**kwargs):
    # 获取首发保荐机构
    return w.wss(security,"ipo_sponsor",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoNominatorSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取首发保荐机构(上市推荐人)时间序列
    return w.wsd(security,"ipo_nominator",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoNominator(security:list,*args,**kwargs):
    # 获取首发保荐机构(上市推荐人)
    return w.wss(security,"ipo_nominator",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoAuditFeeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取首发审计费用时间序列
    return w.wsd(security,"ipo_auditfee",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoAuditFee(security:list,*args,**kwargs):
    # 获取首发审计费用
    return w.wss(security,"ipo_auditfee",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoLawFeeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取首发法律费用时间序列
    return w.wsd(security,"ipo_lawfee",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoLawFee(security:list,*args,**kwargs):
    # 获取首发法律费用
    return w.wss(security,"ipo_lawfee",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoIsSuVolPlannedSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取计划发行总数时间序列
    return w.wsd(security,"ipo_issuvolplanned",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoIsSuVolPlanned(security:list,*args,**kwargs):
    # 获取计划发行总数
    return w.wss(security,"ipo_issuvolplanned",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoOverAllotVolSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取超额配售数量时间序列
    return w.wsd(security,"ipo_overallot_vol",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoOverAllotVol(security:list,*args,**kwargs):
    # 获取超额配售数量
    return w.wss(security,"ipo_overallot_vol",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoLStNumSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取首日上市数量时间序列
    return w.wsd(security,"ipo_lstnum",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoLStNum(security:list,*args,**kwargs):
    # 获取首日上市数量
    return w.wss(security,"ipo_lstnum",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoOldSharesSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取股东售股数量时间序列
    return w.wsd(security,"ipo_oldshares",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoOldShares(security:list,*args,**kwargs):
    # 获取股东售股数量
    return w.wss(security,"ipo_oldshares",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoNewSharesSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取新股发行数量时间序列
    return w.wsd(security,"ipo_newshares",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoNewShares(security:list,*args,**kwargs):
    # 获取新股发行数量
    return w.wss(security,"ipo_newshares",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoAmountSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行数量合计时间序列
    return w.wsd(security,"ipo_amount",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoAmount(security:list,*args,**kwargs):
    # 获取发行数量合计
    return w.wss(security,"ipo_amount",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取首发上市日期时间序列
    return w.wsd(security,"ipo_date",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoDate(security:list,*args,**kwargs):
    # 获取首发上市日期
    return w.wss(security,"ipo_date",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivCashPaidAfterTaxSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间每股股利(税后)时间序列
    return w.wsd(security,"div_cashpaidaftertax",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivCashPaidAfterTax(security:list,*args,**kwargs):
    # 获取区间每股股利(税后)
    return w.wss(security,"div_cashpaidaftertax",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDYoYepsDilutedSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取稀释每股收益(同比增长率)_GSD时间序列
    return w.wsd(security,"wgsd_yoyeps_diluted",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDYoYepsDiluted(security:list,*args,**kwargs):
    # 获取稀释每股收益(同比增长率)_GSD
    return w.wss(security,"wgsd_yoyeps_diluted",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDYoYepsBasicSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基本每股收益(同比增长率)_GSD时间序列
    return w.wsd(security,"wgsd_yoyeps_basic",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDYoYepsBasic(security:list,*args,**kwargs):
    # 获取基本每股收益(同比增长率)_GSD
    return w.wss(security,"wgsd_yoyeps_basic",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivCashPaidBeforeTaxSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间每股股利(税前)时间序列
    return w.wsd(security,"div_cashpaidbeforetax",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivCashPaidBeforeTax(security:list,*args,**kwargs):
    # 获取区间每股股利(税前)
    return w.wss(security,"div_cashpaidbeforetax",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoYepsDilutedSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取稀释每股收益(同比增长率)时间序列
    return w.wsd(security,"yoyeps_diluted",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoYepsDiluted(security:list,*args,**kwargs):
    # 获取稀释每股收益(同比增长率)
    return w.wss(security,"yoyeps_diluted",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoYepsBasicSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基本每股收益(同比增长率)时间序列
    return w.wsd(security,"yoyeps_basic",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getYoYepsBasic(security:list,*args,**kwargs):
    # 获取基本每股收益(同比增长率)
    return w.wss(security,"yoyeps_basic",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivCashAndStockSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股分红送转时间序列
    return w.wsd(security,"div_cashandstock",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivCashAndStock(security:list,*args,**kwargs):
    # 获取每股分红送转
    return w.wss(security,"div_cashandstock",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaTaTurnTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总资产周转率(TTM)_PIT时间序列
    return w.wsd(security,"fa_taturn_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaTaTurnTtM(security:list,*args,**kwargs):
    # 获取总资产周转率(TTM)_PIT
    return w.wss(security,"fa_taturn_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDAssetsTurnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总资产周转率_GSD时间序列
    return w.wsd(security,"wgsd_assetsturn",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDAssetsTurn(security:list,*args,**kwargs):
    # 获取总资产周转率_GSD
    return w.wss(security,"wgsd_assetsturn",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTurnoverTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总资产周转率(TTM)时间序列
    return w.wsd(security,"turnover_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTurnoverTtM(security:list,*args,**kwargs):
    # 获取总资产周转率(TTM)
    return w.wss(security,"turnover_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDYoYRoeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取净资产收益率(摊薄)(同比增长率)_GSD时间序列
    return w.wsd(security,"wgsd_yoyroe",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDYoYRoe(security:list,*args,**kwargs):
    # 获取净资产收益率(摊薄)(同比增长率)_GSD
    return w.wss(security,"wgsd_yoyroe",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAssetsTurnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取总资产周转率时间序列
    return w.wsd(security,"assetsturn",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAssetsTurn(security:list,*args,**kwargs):
    # 获取总资产周转率
    return w.wss(security,"assetsturn",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaInvTurnDaysTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取存货周转天数(TTM)_PIT时间序列
    return w.wsd(security,"fa_invturndays_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaInvTurnDaysTtM(security:list,*args,**kwargs):
    # 获取存货周转天数(TTM)_PIT
    return w.wss(security,"fa_invturndays_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDInvTurnDaysSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取存货周转天数_GSD时间序列
    return w.wsd(security,"wgsd_invturndays",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDInvTurnDays(security:list,*args,**kwargs):
    # 获取存货周转天数_GSD
    return w.wss(security,"wgsd_invturndays",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInvTurnDaysSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取存货周转天数时间序列
    return w.wsd(security,"invturndays",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInvTurnDays(security:list,*args,**kwargs):
    # 获取存货周转天数
    return w.wss(security,"invturndays",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLongDebtToDebtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取长期负债占比时间序列
    return w.wsd(security,"longdebttodebt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLongDebtToDebt(security:list,*args,**kwargs):
    # 获取长期负债占比
    return w.wss(security,"longdebttodebt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivSharesSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取分红基准股本时间序列
    return w.wsd(security,"div_shares",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivShares(security:list,*args,**kwargs):
    # 获取分红基准股本
    return w.wss(security,"div_shares",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteAuALaCcmDivSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取现金分红总额时间序列
    return w.wsd(security,"stmnote_aualaccmdiv",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteAuALaCcmDiv(security:list,*args,**kwargs):
    # 获取现金分红总额
    return w.wss(security,"stmnote_aualaccmdiv",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivPreDisclosureDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取预披露公告日时间序列
    return w.wsd(security,"div_preDisclosureDate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivPreDisclosureDate(security:list,*args,**kwargs):
    # 获取预披露公告日
    return w.wss(security,"div_preDisclosureDate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDCashRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取保守速动比率_GSD时间序列
    return w.wsd(security,"wgsd_cashratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDCashRatio(security:list,*args,**kwargs):
    # 获取保守速动比率_GSD
    return w.wss(security,"wgsd_cashratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCashRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取保守速动比率时间序列
    return w.wsd(security,"cashratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCashRatio(security:list,*args,**kwargs):
    # 获取保守速动比率
    return w.wss(security,"cashratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivDividendRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取现金分红比例时间序列
    return w.wsd(security,"div_dividendratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivDividendRatio(security:list,*args,**kwargs):
    # 获取现金分红比例
    return w.wss(security,"div_dividendratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivProgressSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取分红方案进度时间序列
    return w.wsd(security,"div_progress",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivProgress(security:list,*args,**kwargs):
    # 获取分红方案进度
    return w.wss(security,"div_progress",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoTradeDaysSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取上市交易天数时间序列
    return w.wsd(security,"ipo_tradedays",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoTradeDays(security:list,*args,**kwargs):
    # 获取上市交易天数
    return w.wss(security,"ipo_tradedays",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDAssetsCurRSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取流动资产合计_GSD时间序列
    return w.wsd(security,"wgsd_assets_curr",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDAssetsCurR(security:list,*args,**kwargs):
    # 获取流动资产合计_GSD
    return w.wss(security,"wgsd_assets_curr",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCurAssetsGapSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取流动资产差额(特殊报表科目)时间序列
    return w.wsd(security,"cur_assets_gap",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCurAssetsGap(security:list,*args,**kwargs):
    # 获取流动资产差额(特殊报表科目)
    return w.wss(security,"cur_assets_gap",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank722Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款利息收入_个人贷款及垫款时间序列
    return w.wsd(security,"stmnote_bank_722",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank722(security:list,*args,**kwargs):
    # 获取贷款利息收入_个人贷款及垫款
    return w.wss(security,"stmnote_bank_722",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank721Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款利息收入_企业贷款及垫款时间序列
    return w.wsd(security,"stmnote_bank_721",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank721(security:list,*args,**kwargs):
    # 获取贷款利息收入_企业贷款及垫款
    return w.wss(security,"stmnote_bank_721",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank710Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款利息收入_总计时间序列
    return w.wsd(security,"stmnote_bank_710",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank710(security:list,*args,**kwargs):
    # 获取贷款利息收入_总计
    return w.wss(security,"stmnote_bank_710",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSec1510Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取利息收入合计时间序列
    return w.wsd(security,"stmnote_sec_1510",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSec1510(security:list,*args,**kwargs):
    # 获取利息收入合计
    return w.wss(security,"stmnote_sec_1510",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCreditImpairLoss2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取信用减值损失时间序列
    return w.wsd(security,"credit_impair_loss2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCreditImpairLoss2(security:list,*args,**kwargs):
    # 获取信用减值损失
    return w.wss(security,"credit_impair_loss2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetClaimExpSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取赔付支出净额时间序列
    return w.wsd(security,"net_claim_exp",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetClaimExp(security:list,*args,**kwargs):
    # 获取赔付支出净额
    return w.wss(security,"net_claim_exp",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDvdExpInsuredSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取保单红利支出时间序列
    return w.wsd(security,"dvd_exp_insured",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDvdExpInsured(security:list,*args,**kwargs):
    # 获取保单红利支出
    return w.wss(security,"dvd_exp_insured",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDSalesOThSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他营业收入_GSD时间序列
    return w.wsd(security,"wgsd_sales_oth",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDSalesOTh(security:list,*args,**kwargs):
    # 获取其他营业收入_GSD
    return w.wss(security,"wgsd_sales_oth",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReInSurExpRecoverableSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取摊回分保费用时间序列
    return w.wsd(security,"reinsur_exp_recoverable",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReInSurExpRecoverable(security:list,*args,**kwargs):
    # 获取摊回分保费用
    return w.wss(security,"reinsur_exp_recoverable",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClaimExpRecoverableSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取摊回赔付支出时间序列
    return w.wsd(security,"claim_exp_recoverable",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getClaimExpRecoverable(security:list,*args,**kwargs):
    # 获取摊回赔付支出
    return w.wss(security,"claim_exp_recoverable",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOtherOperExpSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他业务成本时间序列
    return w.wsd(security,"other_oper_exp",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOtherOperExp(security:list,*args,**kwargs):
    # 获取其他业务成本
    return w.wss(security,"other_oper_exp",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSeg1704Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他业务成本(附注)时间序列
    return w.wsd(security,"stmnote_seg_1704",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSeg1704(security:list,*args,**kwargs):
    # 获取其他业务成本(附注)
    return w.wss(security,"stmnote_seg_1704",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOpProfitGapSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业利润差额(特殊报表科目)时间序列
    return w.wsd(security,"opprofit_gap",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOpProfitGap(security:list,*args,**kwargs):
    # 获取营业利润差额(特殊报表科目)
    return w.wss(security,"opprofit_gap",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOpProfitNettingSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业利润差额(合计平衡项目)时间序列
    return w.wsd(security,"opprofit_netting",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOpProfitNetting(security:list,*args,**kwargs):
    # 获取营业利润差额(合计平衡项目)
    return w.wss(security,"opprofit_netting",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaNicuRDebtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取无息流动负债_PIT时间序列
    return w.wsd(security,"fa_nicurdebt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaNicuRDebt(security:list,*args,**kwargs):
    # 获取无息流动负债_PIT
    return w.wss(security,"fa_nicurdebt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs74Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取衍生金融负债_FUND时间序列
    return w.wsd(security,"stm_bs_74",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs74(security:list,*args,**kwargs):
    # 获取衍生金融负债_FUND
    return w.wss(security,"stm_bs_74",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDerivativeFinLiaBSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取衍生金融负债时间序列
    return w.wsd(security,"derivative_fin_liab",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDerivativeFinLiaB(security:list,*args,**kwargs):
    # 获取衍生金融负债
    return w.wss(security,"derivative_fin_liab",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIndependentAccTLiaBSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取独立账户负债时间序列
    return w.wsd(security,"independent_acct_liab",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIndependentAccTLiaB(security:list,*args,**kwargs):
    # 获取独立账户负债
    return w.wss(security,"independent_acct_liab",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyBusLiaBSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取代理业务负债时间序列
    return w.wsd(security,"agency_bus_liab",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyBusLiaB(security:list,*args,**kwargs):
    # 获取代理业务负债
    return w.wss(security,"agency_bus_liab",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOThCurLiaBSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他流动负债时间序列
    return w.wsd(security,"oth_cur_liab",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOThCurLiaB(security:list,*args,**kwargs):
    # 获取其他流动负债
    return w.wss(security,"oth_cur_liab",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDLiAbsInvestContractSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取投资合同负债_GSD时间序列
    return w.wsd(security,"wgsd_liabs_invest_contract",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDLiAbsInvestContract(security:list,*args,**kwargs):
    # 获取投资合同负债_GSD
    return w.wss(security,"wgsd_liabs_invest_contract",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank723Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款利息收入_票据贴现时间序列
    return w.wsd(security,"stmnote_bank_723",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank723(security:list,*args,**kwargs):
    # 获取贷款利息收入_票据贴现
    return w.wss(security,"stmnote_bank_723",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank724Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款利息收入_个人住房贷款时间序列
    return w.wsd(security,"stmnote_bank_724",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank724(security:list,*args,**kwargs):
    # 获取贷款利息收入_个人住房贷款
    return w.wss(security,"stmnote_bank_724",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank725Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款利息收入_个人消费贷款时间序列
    return w.wsd(security,"stmnote_bank_725",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank725(security:list,*args,**kwargs):
    # 获取贷款利息收入_个人消费贷款
    return w.wss(security,"stmnote_bank_725",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank726Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款利息收入_信用卡应收账款时间序列
    return w.wsd(security,"stmnote_bank_726",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank726(security:list,*args,**kwargs):
    # 获取贷款利息收入_信用卡应收账款
    return w.wss(security,"stmnote_bank_726",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank649Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取存款利息支出_存款总额时间序列
    return w.wsd(security,"stmnote_bank_649",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank649(security:list,*args,**kwargs):
    # 获取存款利息支出_存款总额
    return w.wss(security,"stmnote_bank_649",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank631Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取存款利息支出_个人定期存款时间序列
    return w.wsd(security,"stmnote_bank_631",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank631(security:list,*args,**kwargs):
    # 获取存款利息支出_个人定期存款
    return w.wss(security,"stmnote_bank_631",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOperatingCost2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取营业总成本2时间序列
    return w.wsd(security,"operating_cost2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOperatingCost2(security:list,*args,**kwargs):
    # 获取营业总成本2
    return w.wss(security,"operating_cost2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank632Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取存款利息支出_个人活期存款时间序列
    return w.wsd(security,"stmnote_bank_632",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank632(security:list,*args,**kwargs):
    # 获取存款利息支出_个人活期存款
    return w.wss(security,"stmnote_bank_632",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank633Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取存款利息支出_公司定期存款时间序列
    return w.wsd(security,"stmnote_bank_633",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank633(security:list,*args,**kwargs):
    # 获取存款利息支出_公司定期存款
    return w.wss(security,"stmnote_bank_633",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank634Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取存款利息支出_公司活期存款时间序列
    return w.wsd(security,"stmnote_bank_634",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank634(security:list,*args,**kwargs):
    # 获取存款利息支出_公司活期存款
    return w.wss(security,"stmnote_bank_634",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank635Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取存款利息支出_其它存款时间序列
    return w.wsd(security,"stmnote_bank_635",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank635(security:list,*args,**kwargs):
    # 获取存款利息支出_其它存款
    return w.wss(security,"stmnote_bank_635",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSeg1703Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他业务收入(附注)时间序列
    return w.wsd(security,"stmnote_seg_1703",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSeg1703(security:list,*args,**kwargs):
    # 获取其他业务收入(附注)
    return w.wss(security,"stmnote_seg_1703",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOtherOperIncSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他业务收入时间序列
    return w.wsd(security,"other_oper_inc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOtherOperInc(security:list,*args,**kwargs):
    # 获取其他业务收入
    return w.wss(security,"other_oper_inc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getToTPremIncSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取保费业务收入时间序列
    return w.wsd(security,"tot_prem_inc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getToTPremInc(security:list,*args,**kwargs):
    # 获取保费业务收入
    return w.wss(security,"tot_prem_inc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDLiAbsInSurContractSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取保险合同负债_GSD时间序列
    return w.wsd(security,"wgsd_liabs_insur_contract",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDLiAbsInSurContract(security:list,*args,**kwargs):
    # 获取保险合同负债_GSD
    return w.wss(security,"wgsd_liabs_insur_contract",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs76Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他利息收入_FUND时间序列
    return w.wsd(security,"stm_is_76",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs76(security:list,*args,**kwargs):
    # 获取其他利息收入_FUND
    return w.wss(security,"stm_is_76",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs6Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取存款利息收入_FUND时间序列
    return w.wsd(security,"stm_is_6",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs6(security:list,*args,**kwargs):
    # 获取存款利息收入_FUND
    return w.wss(security,"stm_is_6",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank842Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款利息收入_中长期贷款时间序列
    return w.wsd(security,"stmnote_bank_842",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank842(security:list,*args,**kwargs):
    # 获取贷款利息收入_中长期贷款
    return w.wss(security,"stmnote_bank_842",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank841Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款利息收入_短期贷款时间序列
    return w.wsd(security,"stmnote_bank_841",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank841(security:list,*args,**kwargs):
    # 获取贷款利息收入_短期贷款
    return w.wss(security,"stmnote_bank_841",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank784Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款利息收入_质押贷款时间序列
    return w.wsd(security,"stmnote_bank_784",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank784(security:list,*args,**kwargs):
    # 获取贷款利息收入_质押贷款
    return w.wss(security,"stmnote_bank_784",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank783Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款利息收入_抵押贷款时间序列
    return w.wsd(security,"stmnote_bank_783",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank783(security:list,*args,**kwargs):
    # 获取贷款利息收入_抵押贷款
    return w.wss(security,"stmnote_bank_783",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank782Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款利息收入_保证贷款时间序列
    return w.wsd(security,"stmnote_bank_782",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank782(security:list,*args,**kwargs):
    # 获取贷款利息收入_保证贷款
    return w.wss(security,"stmnote_bank_782",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank781Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款利息收入_信用贷款时间序列
    return w.wsd(security,"stmnote_bank_781",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank781(security:list,*args,**kwargs):
    # 获取贷款利息收入_信用贷款
    return w.wss(security,"stmnote_bank_781",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank729Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款利息收入_其他个人贷款时间序列
    return w.wsd(security,"stmnote_bank_729",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank729(security:list,*args,**kwargs):
    # 获取贷款利息收入_其他个人贷款
    return w.wss(security,"stmnote_bank_729",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank728Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款利息收入_汽车贷款时间序列
    return w.wsd(security,"stmnote_bank_728",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank728(security:list,*args,**kwargs):
    # 获取贷款利息收入_汽车贷款
    return w.wss(security,"stmnote_bank_728",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank727Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取贷款利息收入_经营性贷款时间序列
    return w.wsd(security,"stmnote_bank_727",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteBank727(security:list,*args,**kwargs):
    # 获取贷款利息收入_经营性贷款
    return w.wss(security,"stmnote_bank_727",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs5Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取债券利息收入_FUND时间序列
    return w.wsd(security,"stm_is_5",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmIs5(security:list,*args,**kwargs):
    # 获取债券利息收入_FUND
    return w.wss(security,"stm_is_5",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDPpeNetSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取固定资产净值_GSD时间序列
    return w.wsd(security,"wgsd_ppe_net",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDPpeNet(security:list,*args,**kwargs):
    # 获取固定资产净值_GSD
    return w.wss(security,"wgsd_ppe_net",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDLiAbsCurROThSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他流动负债_GSD时间序列
    return w.wsd(security,"wgsd_liabs_curr_oth",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDLiAbsCurROTh(security:list,*args,**kwargs):
    # 获取其他流动负债_GSD
    return w.wss(security,"wgsd_liabs_curr_oth",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getExInterestDebtCurrentSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取无息流动负债时间序列
    return w.wsd(security,"exinterestdebt_current",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getExInterestDebtCurrent(security:list,*args,**kwargs):
    # 获取无息流动负债
    return w.wss(security,"exinterestdebt_current",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDAssetsCurROThSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他流动资产_GSD时间序列
    return w.wsd(security,"wgsd_assets_curr_oth",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDAssetsCurROTh(security:list,*args,**kwargs):
    # 获取其他流动资产_GSD
    return w.wss(security,"wgsd_assets_curr_oth",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDQfaGrossMargin2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取单季度.毛利_GSD时间序列
    return w.wsd(security,"wgsd_qfa_grossmargin2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDQfaGrossMargin2(security:list,*args,**kwargs):
    # 获取单季度.毛利_GSD
    return w.wss(security,"wgsd_qfa_grossmargin2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getQfaGrossMarginSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取单季度.毛利时间序列
    return w.wsd(security,"qfa_grossmargin",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getQfaGrossMargin(security:list,*args,**kwargs):
    # 获取单季度.毛利
    return w.wss(security,"qfa_grossmargin",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaDebtsAssetRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取债务总资产比_PIT时间序列
    return w.wsd(security,"fa_debtsassetratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaDebtsAssetRatio(security:list,*args,**kwargs):
    # 获取债务总资产比_PIT
    return w.wss(security,"fa_debtsassetratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSegmentSalesSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取主营收入构成时间序列
    return w.wsd(security,"segment_sales",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSegmentSales(security:list,*args,**kwargs):
    # 获取主营收入构成
    return w.wss(security,"segment_sales",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSeg1501Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取海外业务收入时间序列
    return w.wsd(security,"stmnote_seg_1501",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSeg1501(security:list,*args,**kwargs):
    # 获取海外业务收入
    return w.wss(security,"stmnote_seg_1501",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivCapitalization2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股转增股本(已宣告)时间序列
    return w.wsd(security,"div_capitalization2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivCapitalization2(security:list,*args,**kwargs):
    # 获取每股转增股本(已宣告)
    return w.wss(security,"div_capitalization2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivCapitalizationSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股转增股本时间序列
    return w.wsd(security,"div_capitalization",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDivCapitalization(security:list,*args,**kwargs):
    # 获取每股转增股本
    return w.wss(security,"div_capitalization",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteGuarantee2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取担保余额合计时间序列
    return w.wsd(security,"stmnote_guarantee_2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteGuarantee2(security:list,*args,**kwargs):
    # 获取担保余额合计
    return w.wss(security,"stmnote_guarantee_2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteGuarantee5Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取违规担保总额时间序列
    return w.wsd(security,"stmnote_guarantee_5",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteGuarantee5(security:list,*args,**kwargs):
    # 获取违规担保总额
    return w.wss(security,"stmnote_guarantee_5",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteAuditInterpretationSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取审计结果说明时间序列
    return w.wsd(security,"stmnote_audit_interpretation",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteAuditInterpretation(security:list,*args,**kwargs):
    # 获取审计结果说明
    return w.wss(security,"stmnote_audit_interpretation",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteAuditKamSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取关键审计事项时间序列
    return w.wsd(security,"stmnote_audit_kam",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteAuditKam(security:list,*args,**kwargs):
    # 获取关键审计事项
    return w.wss(security,"stmnote_audit_kam",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaFixAssetsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取固定资产合计_PIT时间序列
    return w.wsd(security,"fa_fixassets",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaFixAssets(security:list,*args,**kwargs):
    # 获取固定资产合计_PIT
    return w.wss(security,"fa_fixassets",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaIntangAssetRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取无形资产比率_PIT时间序列
    return w.wsd(security,"fa_intangassetratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaIntangAssetRatio(security:list,*args,**kwargs):
    # 获取无形资产比率_PIT
    return w.wss(security,"fa_intangassetratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaFixedAssetToAssetSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取固定资产比率_PIT时间序列
    return w.wsd(security,"fa_fixedassettoasset",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaFixedAssetToAsset(security:list,*args,**kwargs):
    # 获取固定资产比率_PIT
    return w.wss(security,"fa_fixedassettoasset",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaCurAssetsRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取流动资产比率_PIT时间序列
    return w.wsd(security,"fa_curassetsratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaCurAssetsRatio(security:list,*args,**kwargs):
    # 获取流动资产比率_PIT
    return w.wss(security,"fa_curassetsratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAMortIntangAssetsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取无形资产摊销时间序列
    return w.wsd(security,"amort_intang_assets",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAMortIntangAssets(security:list,*args,**kwargs):
    # 获取无形资产摊销
    return w.wss(security,"amort_intang_assets",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteArTotalSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取应收账款余额时间序列
    return w.wsd(security,"stmnote_ar_total",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteArTotal(security:list,*args,**kwargs):
    # 获取应收账款余额
    return w.wss(security,"stmnote_ar_total",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFixAssetsDispSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取固定资产清理时间序列
    return w.wsd(security,"fix_assets_disp",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFixAssetsDisp(security:list,*args,**kwargs):
    # 获取固定资产清理
    return w.wss(security,"fix_assets_disp",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsLiquidAssetSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取流动资产合计时间序列
    return w.wsd(security,"stm07_bs_reits_liquidasset",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsLiquidAsset(security:list,*args,**kwargs):
    # 获取流动资产合计
    return w.wss(security,"stm07_bs_reits_liquidasset",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCurAssetsNettingSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取流动资产差额(合计平衡项目)时间序列
    return w.wsd(security,"cur_assets_netting",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCurAssetsNetting(security:list,*args,**kwargs):
    # 获取流动资产差额(合计平衡项目)
    return w.wss(security,"cur_assets_netting",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOThCurAssetsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他流动资产时间序列
    return w.wsd(security,"oth_cur_assets",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOThCurAssets(security:list,*args,**kwargs):
    # 获取其他流动资产
    return w.wss(security,"oth_cur_assets",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyBusAssetsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取代理业务资产时间序列
    return w.wsd(security,"agency_bus_assets",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAgencyBusAssets(security:list,*args,**kwargs):
    # 获取代理业务资产
    return w.wss(security,"agency_bus_assets",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIndependentAccTAssetsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取独立账户资产时间序列
    return w.wsd(security,"independent_acct_assets",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIndependentAccTAssets(security:list,*args,**kwargs):
    # 获取独立账户资产
    return w.wss(security,"independent_acct_assets",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDerivativeFinAssetsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取衍生金融资产时间序列
    return w.wsd(security,"derivative_fin_assets",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDerivativeFinAssets(security:list,*args,**kwargs):
    # 获取衍生金融资产
    return w.wss(security,"derivative_fin_assets",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSec3Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取净资本负债率时间序列
    return w.wsd(security,"stmnote_sec_3",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmNoteSec3(security:list,*args,**kwargs):
    # 获取净资本负债率
    return w.wss(security,"stmnote_sec_3",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsLiquidDebtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取流动负债合计时间序列
    return w.wsd(security,"stm07_bs_reits_liquiddebt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStm07BsReItsLiquidDebt(security:list,*args,**kwargs):
    # 获取流动负债合计
    return w.wss(security,"stm07_bs_reits_liquiddebt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCurLiaBNettingSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取流动负债差额(合计平衡项目)时间序列
    return w.wsd(security,"cur_liab_netting",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCurLiaBNetting(security:list,*args,**kwargs):
    # 获取流动负债差额(合计平衡项目)
    return w.wss(security,"cur_liab_netting",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCurLiaBGapSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取流动负债差额(特殊报表科目)时间序列
    return w.wsd(security,"cur_liab_gap",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getCurLiaBGap(security:list,*args,**kwargs):
    # 获取流动负债差额(特殊报表科目)
    return w.wss(security,"cur_liab_gap",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDLiAbsCurRSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取流动负债合计_GSD时间序列
    return w.wsd(security,"wgsd_liabs_curr",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDLiAbsCurR(security:list,*args,**kwargs):
    # 获取流动负债合计_GSD
    return w.wss(security,"wgsd_liabs_curr",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaOppSSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股营业利润_PIT时间序列
    return w.wsd(security,"fa_opps",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaOppS(security:list,*args,**kwargs):
    # 获取每股营业利润_PIT
    return w.wss(security,"fa_opps",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaOppSTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股营业利润(TTM)_PIT时间序列
    return w.wsd(security,"fa_opps_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaOppSTtM(security:list,*args,**kwargs):
    # 获取每股营业利润(TTM)_PIT
    return w.wss(security,"fa_opps_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLiaBGapDetailSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取负债差额说明(特殊报表科目)时间序列
    return w.wsd(security,"liab_gap_detail",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLiaBGapDetail(security:list,*args,**kwargs):
    # 获取负债差额说明(特殊报表科目)
    return w.wss(security,"liab_gap_detail",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getProfitGapSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取利润总额差额(特殊报表科目)时间序列
    return w.wsd(security,"profit_gap",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getProfitGap(security:list,*args,**kwargs):
    # 获取利润总额差额(特殊报表科目)
    return w.wss(security,"profit_gap",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getProfitNettingSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取利润总额差额(合计平衡项目)时间序列
    return w.wsd(security,"profit_netting",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getProfitNetting(security:list,*args,**kwargs):
    # 获取利润总额差额(合计平衡项目)
    return w.wss(security,"profit_netting",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDExInterestDebtCurrentSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取无息流动负债_GSD时间序列
    return w.wsd(security,"wgsd_exinterestdebt_current",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDExInterestDebtCurrent(security:list,*args,**kwargs):
    # 获取无息流动负债_GSD
    return w.wss(security,"wgsd_exinterestdebt_current",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMinorityInterestTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取少数股东损益(TTM)时间序列
    return w.wsd(security,"minorityinterest_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMinorityInterestTtM(security:list,*args,**kwargs):
    # 获取少数股东损益(TTM)
    return w.wss(security,"minorityinterest_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDMinIntExpSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取少数股东损益_GSD时间序列
    return w.wsd(security,"wgsd_min_int_exp",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDMinIntExp(security:list,*args,**kwargs):
    # 获取少数股东损益_GSD
    return w.wss(security,"wgsd_min_int_exp",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMinorityIntIncSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取少数股东损益时间序列
    return w.wsd(security,"minority_int_inc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMinorityIntInc(security:list,*args,**kwargs):
    # 获取少数股东损益
    return w.wss(security,"minority_int_inc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaMinInterestTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取少数股东损益(TTM)_PIT时间序列
    return w.wsd(security,"fa_mininterest_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaMinInterestTtM(security:list,*args,**kwargs):
    # 获取少数股东损益(TTM)_PIT
    return w.wss(security,"fa_mininterest_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDEpsBasicSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基本每股收益_GSD时间序列
    return w.wsd(security,"wgsd_eps_basic",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDEpsBasic(security:list,*args,**kwargs):
    # 获取基本每股收益_GSD
    return w.wss(security,"wgsd_eps_basic",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs109Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取衍生金融资产_FUND时间序列
    return w.wsd(security,"stm_bs_109",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStmBs109(security:list,*args,**kwargs):
    # 获取衍生金融资产_FUND
    return w.wss(security,"stm_bs_109",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEpsBasicIsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基本每股收益时间序列
    return w.wsd(security,"eps_basic_is",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEpsBasicIs(security:list,*args,**kwargs):
    # 获取基本每股收益
    return w.wss(security,"eps_basic_is",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaEpsBasicSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基本每股收益_PIT时间序列
    return w.wsd(security,"fa_eps_basic",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaEpsBasic(security:list,*args,**kwargs):
    # 获取基本每股收益_PIT
    return w.wss(security,"fa_eps_basic",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDEpsDilutedSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取稀释每股收益_GSD时间序列
    return w.wsd(security,"wgsd_eps_diluted",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDEpsDiluted(security:list,*args,**kwargs):
    # 获取稀释每股收益_GSD
    return w.wss(security,"wgsd_eps_diluted",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEpsDilutedIsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取稀释每股收益时间序列
    return w.wsd(security,"eps_diluted_is",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEpsDilutedIs(security:list,*args,**kwargs):
    # 获取稀释每股收益
    return w.wss(security,"eps_diluted_is",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaEpsDilutedSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取稀释每股收益_PIT时间序列
    return w.wsd(security,"fa_eps_diluted",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaEpsDiluted(security:list,*args,**kwargs):
    # 获取稀释每股收益_PIT
    return w.wss(security,"fa_eps_diluted",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMinorityInterestTtM2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取少数股东损益(TTM)_GSD时间序列
    return w.wsd(security,"minorityinterest_ttm2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMinorityInterestTtM2(security:list,*args,**kwargs):
    # 获取少数股东损益(TTM)_GSD
    return w.wss(security,"minorityinterest_ttm2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoBFundSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取网上冻结资金时间序列
    return w.wsd(security,"ipo_Bfund",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoBFund(security:list,*args,**kwargs):
    # 获取网上冻结资金
    return w.wss(security,"ipo_Bfund",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoPurchaseCodeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取网上申购代码时间序列
    return w.wsd(security,"ipo_purchasecode",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoPurchaseCode(security:list,*args,**kwargs):
    # 获取网上申购代码
    return w.wss(security,"ipo_purchasecode",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoOpVolumeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取网下申购总量时间序列
    return w.wsd(security,"ipo_op_volume",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoOpVolume(security:list,*args,**kwargs):
    # 获取网下申购总量
    return w.wss(security,"ipo_op_volume",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInterestPayMethodSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取付息方式说明时间序列
    return w.wsd(security,"fund_interestpaymethod",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInterestPayMethod(security:list,*args,**kwargs):
    # 获取付息方式说明
    return w.wss(security,"fund_interestpaymethod",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundMaxSubScripAmountSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取委托金额上限时间序列
    return w.wsd(security,"fund_maxsubscripamount",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundMaxSubScripAmount(security:list,*args,**kwargs):
    # 获取委托金额上限
    return w.wss(security,"fund_maxsubscripamount",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundActualDurationSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取实际运作期限时间序列
    return w.wsd(security,"fund_actualduration",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundActualDuration(security:list,*args,**kwargs):
    # 获取实际运作期限
    return w.wss(security,"fund_actualduration",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundOperationModeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取产品运作方式时间序列
    return w.wsd(security,"fund_operationmode",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundOperationMode(security:list,*args,**kwargs):
    # 获取产品运作方式
    return w.wss(security,"fund_operationmode",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueChannelSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取产品发行渠道时间序列
    return w.wsd(security,"issue_channel",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueChannel(security:list,*args,**kwargs):
    # 获取产品发行渠道
    return w.wss(security,"issue_channel",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSecondInvestStrategySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取投资策略分类(二级)(私募)时间序列
    return w.wsd(security,"fund_secondinveststrategy",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSecondInvestStrategy(security:list,*args,**kwargs):
    # 获取投资策略分类(二级)(私募)
    return w.wss(security,"fund_secondinveststrategy",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundFirstInvestStrategySeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取投资策略分类(一级)(私募)时间序列
    return w.wsd(security,"fund_firstinveststrategy",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundFirstInvestStrategy(security:list,*args,**kwargs):
    # 获取投资策略分类(一级)(私募)
    return w.wss(security,"fund_firstinveststrategy",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundMinBuyAmountSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最低参与金额时间序列
    return w.wsd(security,"fund_minbuyamount",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundMinBuyAmount(security:list,*args,**kwargs):
    # 获取最低参与金额
    return w.wss(security,"fund_minbuyamount",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundEffSubsCrHoleDerNoSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取有效认购户数时间序列
    return w.wsd(security,"fund_effsubscrholederno",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundEffSubsCrHoleDerNo(security:list,*args,**kwargs):
    # 获取有效认购户数
    return w.wss(security,"fund_effsubscrholederno",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSubEnddateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售截止日期时间序列
    return w.wsd(security,"fund_subenddate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSubEnddate(security:list,*args,**kwargs):
    # 获取销售截止日期
    return w.wss(security,"fund_subenddate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSubStartDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售起始日期时间序列
    return w.wsd(security,"fund_substartdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSubStartDate(security:list,*args,**kwargs):
    # 获取销售起始日期
    return w.wss(security,"fund_substartdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstFinalPriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最终发行价格时间序列
    return w.wsd(security,"tendrst_finalprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstFinalPrice(security:list,*args,**kwargs):
    # 获取最终发行价格
    return w.wss(security,"tendrst_finalprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAdvanceCreditDescSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取信用增级情况时间序列
    return w.wsd(security,"advancecredit_desc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAdvanceCreditDesc(security:list,*args,**kwargs):
    # 获取信用增级情况
    return w.wss(security,"advancecredit_desc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundFloatingRateNoteSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取浮动收益说明(信托)时间序列
    return w.wsd(security,"fund_floatingratenote",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundFloatingRateNote(security:list,*args,**kwargs):
    # 获取浮动收益说明(信托)
    return w.wss(security,"fund_floatingratenote",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundExpectedRateOfReturnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取预计年收益率(信托)时间序列
    return w.wsd(security,"fund_expectedrateofreturn",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundExpectedRateOfReturn(security:list,*args,**kwargs):
    # 获取预计年收益率(信托)
    return w.wss(security,"fund_expectedrateofreturn",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTrustSourceTypeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取信托产品类别时间序列
    return w.wsd(security,"trust_sourcetype",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTrustSourceType(security:list,*args,**kwargs):
    # 获取信托产品类别
    return w.wss(security,"trust_sourcetype",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTrustInvestFieldSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取信托投资领域时间序列
    return w.wsd(security,"trust_investfield",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTrustInvestField(security:list,*args,**kwargs):
    # 获取信托投资领域
    return w.wss(security,"trust_investfield",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundDiscountMethodSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取定期折算条款时间序列
    return w.wsd(security,"fund_discountmethod",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundDiscountMethod(security:list,*args,**kwargs):
    # 获取定期折算条款
    return w.wss(security,"fund_discountmethod",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundDiscountPeriodSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取定期折算周期时间序列
    return w.wsd(security,"fund_discountperiod",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundDiscountPeriod(security:list,*args,**kwargs):
    # 获取定期折算周期
    return w.wss(security,"fund_discountperiod",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPairConversionSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取是否配对转换时间序列
    return w.wsd(security,"fund_pairconversion",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPairConversion(security:list,*args,**kwargs):
    # 获取是否配对转换
    return w.wss(security,"fund_pairconversion",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundUseSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取募集资金用途时间序列
    return w.wsd(security,"funduse",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundUse(security:list,*args,**kwargs):
    # 获取募集资金用途
    return w.wss(security,"funduse",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundFundArrivalDaysSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取资金到账天数时间序列
    return w.wsd(security,"fund_fundarrivaldays",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundFundArrivalDays(security:list,*args,**kwargs):
    # 获取资金到账天数
    return w.wss(security,"fund_fundarrivaldays",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCNdPreTerminationSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取提前终止条件时间序列
    return w.wsd(security,"fund_cndpretermination",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCNdPreTermination(security:list,*args,**kwargs):
    # 获取提前终止条件
    return w.wss(security,"fund_cndpretermination",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCNdpUrchRedemptionSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取申购赎回条件时间序列
    return w.wsd(security,"fund_cndpurchredemption",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCNdpUrchRedemption(security:list,*args,**kwargs):
    # 获取申购赎回条件
    return w.wss(security,"fund_cndpurchredemption",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundUnderlyingTargetSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取收益挂钩标的时间序列
    return w.wsd(security,"fund_underlyingtarget",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundUnderlyingTarget(security:list,*args,**kwargs):
    # 获取收益挂钩标的
    return w.wss(security,"fund_underlyingtarget",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInterestDurationCnBdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取估价利率久期(中债)时间序列
    return w.wsd(security,"interestduration_cnbd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInterestDurationCnBd(security:list,*args,**kwargs):
    # 获取估价利率久期(中债)
    return w.wss(security,"interestduration_cnbd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSprDuraCnBdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取估价利差久期(中债)时间序列
    return w.wsd(security,"sprdura_cnbd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSprDuraCnBd(security:list,*args,**kwargs):
    # 获取估价利差久期(中债)
    return w.wss(security,"sprdura_cnbd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAccRIntDayEndCnBdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取日终应计利息(中债)时间序列
    return w.wsd(security,"accrint_dayend_cnbd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAccRIntDayEndCnBd(security:list,*args,**kwargs):
    # 获取日终应计利息(中债)
    return w.wss(security,"accrint_dayend_cnbd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getModiDuraCnBdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取估价修正久期(中债)时间序列
    return w.wsd(security,"modidura_cnbd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getModiDuraCnBd(security:list,*args,**kwargs):
    # 获取估价修正久期(中债)
    return w.wss(security,"modidura_cnbd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPriceCnBdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取日终估价全价(中债)时间序列
    return w.wsd(security,"price_cnbd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPriceCnBd(security:list,*args,**kwargs):
    # 获取日终估价全价(中债)
    return w.wss(security,"price_cnbd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssueUndRTypeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取配股承销方式时间序列
    return w.wsd(security,"rightsissue_undrtype",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssueUndRType(security:list,*args,**kwargs):
    # 获取配股承销方式
    return w.wss(security,"rightsissue_undrtype",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueFirstIssueSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行起始日期时间序列
    return w.wsd(security,"issue_firstissue",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueFirstIssue(security:list,*args,**kwargs):
    # 获取发行起始日期
    return w.wss(security,"issue_firstissue",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueLastIssueSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行截止日期时间序列
    return w.wsd(security,"issue_lastissue",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueLastIssue(security:list,*args,**kwargs):
    # 获取发行截止日期
    return w.wss(security,"issue_lastissue",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderDistRibBeginSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取分销起始日期时间序列
    return w.wsd(security,"tender_distribbegin",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderDistRibBegin(security:list,*args,**kwargs):
    # 获取分销起始日期
    return w.wss(security,"tender_distribbegin",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderDIsTribeNdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取分销截至日期时间序列
    return w.wsd(security,"tender_distribend",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderDIsTribeNd(security:list,*args,**kwargs):
    # 获取分销截至日期
    return w.wss(security,"tender_distribend",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSubShareProportionSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取分级份额占比时间序列
    return w.wsd(security,"fund_subshareproportion",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSubShareProportion(security:list,*args,**kwargs):
    # 获取分级份额占比
    return w.wss(security,"fund_subshareproportion",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderTransferDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取债券过户时间时间序列
    return w.wsd(security,"tender_transferdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderTransferDate(security:list,*args,**kwargs):
    # 获取债券过户时间
    return w.wss(security,"tender_transferdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueRegAmountSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行注册额度时间序列
    return w.wsd(security,"issue_regamount",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueRegAmount(security:list,*args,**kwargs):
    # 获取发行注册额度
    return w.wss(security,"issue_regamount",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsComNameSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取项目公司名称时间序列
    return w.wsd(security,"fund__reitscomname",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsComName(security:list,*args,**kwargs):
    # 获取项目公司名称
    return w.wss(security,"fund__reitscomname",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsOpRiskSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取项目运营风险时间序列
    return w.wsd(security,"fund__reitsoprisk",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsOpRisk(security:list,*args,**kwargs):
    # 获取项目运营风险
    return w.wss(security,"fund__reitsoprisk",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsPbShareSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取公众配售份额时间序列
    return w.wsd(security,"fund__reitspbshare",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsPbShare(security:list,*args,**kwargs):
    # 获取公众配售份额
    return w.wss(security,"fund__reitspbshare",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsPiShareSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取公众认购份额时间序列
    return w.wsd(security,"fund_reitspishare",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsPiShare(security:list,*args,**kwargs):
    # 获取公众认购份额
    return w.wss(security,"fund_reitspishare",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsOffShareSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取网下配售份额时间序列
    return w.wsd(security,"fund__reitsoffshare",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsOffShare(security:list,*args,**kwargs):
    # 获取网下配售份额
    return w.wss(security,"fund__reitsoffshare",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItSoIsHareSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取网下认购份额时间序列
    return w.wsd(security,"fund_reitsoishare",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItSoIsHare(security:list,*args,**kwargs):
    # 获取网下认购份额
    return w.wss(security,"fund_reitsoishare",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsSiShareSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取战略配售份额时间序列
    return w.wsd(security,"fund__reitssishare",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsSiShare(security:list,*args,**kwargs):
    # 获取战略配售份额
    return w.wss(security,"fund__reitssishare",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsPriceMinSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取询价区间下限时间序列
    return w.wsd(security,"fund__reitspricemin",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsPriceMin(security:list,*args,**kwargs):
    # 获取询价区间下限
    return w.wss(security,"fund__reitspricemin",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsPriceMaxSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取询价区间上限时间序列
    return w.wsd(security,"fund__reitspricemax",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundReItsPriceMax(security:list,*args,**kwargs):
    # 获取询价区间上限
    return w.wss(security,"fund__reitspricemax",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueRegDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行注册日期时间序列
    return w.wsd(security,"issue_regdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueRegDate(security:list,*args,**kwargs):
    # 获取发行注册日期
    return w.wss(security,"issue_regdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSPrcNxtCnBdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取估价利差凸性(中债)时间序列
    return w.wsd(security,"sprcnxt_cnbd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSPrcNxtCnBd(security:list,*args,**kwargs):
    # 获取估价利差凸性(中债)
    return w.wss(security,"sprcnxt_cnbd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSMfTypeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取分级基金类别时间序列
    return w.wsd(security,"fund_smftype",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSMfType(security:list,*args,**kwargs):
    # 获取分级基金类别
    return w.wss(security,"fund_smftype",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundTrackIndexCodeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取跟踪指数代码时间序列
    return w.wsd(security,"fund_trackindexcode",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundTrackIndexCode(security:list,*args,**kwargs):
    # 获取跟踪指数代码
    return w.wss(security,"fund_trackindexcode",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundRelatedCodeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取关联基金代码时间序列
    return w.wsd(security,"fund_relatedcode",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundRelatedCode(security:list,*args,**kwargs):
    # 获取关联基金代码
    return w.wss(security,"fund_relatedcode",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInitialCodeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金初始代码时间序列
    return w.wsd(security,"fund_initialcode",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInitialCode(security:list,*args,**kwargs):
    # 获取基金初始代码
    return w.wss(security,"fund_initialcode",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundBackendCodeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金后端代码时间序列
    return w.wsd(security,"fund_backendcode",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundBackendCode(security:list,*args,**kwargs):
    # 获取基金后端代码
    return w.wss(security,"fund_backendcode",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundFrontendCodeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金前端代码时间序列
    return w.wsd(security,"fund_frontendcode",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundFrontendCode(security:list,*args,**kwargs):
    # 获取基金前端代码
    return w.wss(security,"fund_frontendcode",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOtherRisksSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取其他风险提示时间序列
    return w.wsd(security,"otherrisks",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOtherRisks(security:list,*args,**kwargs):
    # 获取其他风险提示
    return w.wss(security,"otherrisks",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRedemptionRiskSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取赎回风险提示时间序列
    return w.wsd(security,"redemptionrisk",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRedemptionRisk(security:list,*args,**kwargs):
    # 获取赎回风险提示
    return w.wss(security,"redemptionrisk",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechnicalRiskSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取技术风险提示时间序列
    return w.wsd(security,"technicalrisk",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechnicalRisk(security:list,*args,**kwargs):
    # 获取技术风险提示
    return w.wss(security,"technicalrisk",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getManagementRiskSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取管理风险提示时间序列
    return w.wsd(security,"managementrisk",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getManagementRisk(security:list,*args,**kwargs):
    # 获取管理风险提示
    return w.wss(security,"managementrisk",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMarketRiskSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取市场风险提示时间序列
    return w.wsd(security,"marketrisk",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getMarketRisk(security:list,*args,**kwargs):
    # 获取市场风险提示
    return w.wss(security,"marketrisk",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundRiskReturnCharactersSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取风险收益特征时间序列
    return w.wsd(security,"fund_riskreturn_characters",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundRiskReturnCharacters(security:list,*args,**kwargs):
    # 获取风险收益特征
    return w.wss(security,"fund_riskreturn_characters",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundValuationMethodSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金估值方法时间序列
    return w.wsd(security,"fund_valuationmethod",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundValuationMethod(security:list,*args,**kwargs):
    # 获取基金估值方法
    return w.wss(security,"fund_valuationmethod",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundFundTransitionSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金转型说明时间序列
    return w.wsd(security,"fund_fundtransition",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundFundTransition(security:list,*args,**kwargs):
    # 获取基金转型说明
    return w.wss(security,"fund_fundtransition",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundExceptionStatusSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取产品异常状态时间序列
    return w.wsd(security,"fund_exceptionstatus",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundExceptionStatus(security:list,*args,**kwargs):
    # 获取产品异常状态
    return w.wss(security,"fund_exceptionstatus",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundStructuredFundOrNotSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取是否分级基金时间序列
    return w.wsd(security,"fund_structuredfundornot",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundStructuredFundOrNot(security:list,*args,**kwargs):
    # 获取是否分级基金
    return w.wss(security,"fund_structuredfundornot",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInitialSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取是否初始基金时间序列
    return w.wsd(security,"fund_initial",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundInitial(security:list,*args,**kwargs):
    # 获取是否初始基金
    return w.wss(security,"fund_initial",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstEffectInvestorsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取有效投标(申购)家数时间序列
    return w.wsd(security,"tendrst_effectinvestors",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstEffectInvestors(security:list,*args,**kwargs):
    # 获取有效投标(申购)家数
    return w.wss(security,"tendrst_effectinvestors",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundBenchIndexCodeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基准指数代码时间序列
    return w.wsd(security,"fund_benchindexcode",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundBenchIndexCode(security:list,*args,**kwargs):
    # 获取基准指数代码
    return w.wss(security,"fund_benchindexcode",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstEffectAmNtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取有效投标总量时间序列
    return w.wsd(security,"tendrst_effectamnt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstEffectAmNt(security:list,*args,**kwargs):
    # 获取有效投标总量
    return w.wss(security,"tendrst_effectamnt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstHightestSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最高投标价位时间序列
    return w.wsd(security,"tendrst_hightest",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstHightest(security:list,*args,**kwargs):
    # 获取最高投标价位
    return w.wss(security,"tendrst_hightest",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstLowestSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最低投标价位时间序列
    return w.wsd(security,"tendrst_lowest",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstLowest(security:list,*args,**kwargs):
    # 获取最低投标价位
    return w.wss(security,"tendrst_lowest",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundBenchmarkSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取业绩比较基准时间序列
    return w.wsd(security,"fund_benchmark",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundBenchmark(security:list,*args,**kwargs):
    # 获取业绩比较基准
    return w.wss(security,"fund_benchmark",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCuStStartDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取开始托管日期时间序列
    return w.wsd(security,"fund_custstartdate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCuStStartDate(security:list,*args,**kwargs):
    # 获取开始托管日期
    return w.wss(security,"fund_custstartdate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCusTendDateSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取托管结束日期时间序列
    return w.wsd(security,"fund_custenddate",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCusTendDate(security:list,*args,**kwargs):
    # 获取托管结束日期
    return w.wss(security,"fund_custenddate",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstUnderwritingSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基本承购总额时间序列
    return w.wsd(security,"tendrst_underwriting",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTendRstUnderwriting(security:list,*args,**kwargs):
    # 获取基本承购总额
    return w.wss(security,"tendrst_underwriting",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueOkSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取是否发行失败时间序列
    return w.wsd(security,"issueok",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIssueOk(security:list,*args,**kwargs):
    # 获取是否发行失败
    return w.wss(security,"issueok",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCorpFourStarFundsPropSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取四星基金占比时间序列
    return w.wsd(security,"fund_corp_fourstarfundsprop",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCorpFourStarFundsProp(security:list,*args,**kwargs):
    # 获取四星基金占比
    return w.wss(security,"fund_corp_fourstarfundsprop",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCorpFiveStarFundsPropSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取五星基金占比时间序列
    return w.wsd(security,"fund_corp_fivestarfundsprop",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundCorpFiveStarFundsProp(security:list,*args,**kwargs):
    # 获取五星基金占比
    return w.wss(security,"fund_corp_fivestarfundsprop",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPChRedMPcHmInAmtFloorSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取申购金额下限(场内)时间序列
    return w.wsd(security,"fund_pchredm_pchminamt_floor",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPChRedMPcHmInAmtFloor(security:list,*args,**kwargs):
    # 获取申购金额下限(场内)
    return w.wss(security,"fund_pchredm_pchminamt_floor",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPChRedMPcHmInAmtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取申购金额下限(场外)时间序列
    return w.wsd(security,"fund_pchredm_pchminamt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPChRedMPcHmInAmt(security:list,*args,**kwargs):
    # 获取申购金额下限(场外)
    return w.wss(security,"fund_pchredm_pchminamt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundDQStatusSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取申购赎回状态时间序列
    return w.wsd(security,"fund_dq_status",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundDQStatus(security:list,*args,**kwargs):
    # 获取申购赎回状态
    return w.wss(security,"fund_dq_status",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPurchaseAndRedemptionAbbreviationSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取申购赎回简称时间序列
    return w.wsd(security,"fund_purchaseandredemptionabbreviation",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPurchaseAndRedemptionAbbreviation(security:list,*args,**kwargs):
    # 获取申购赎回简称
    return w.wss(security,"fund_purchaseandredemptionabbreviation",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundIndexUsageFeeRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取指数使用费率时间序列
    return w.wsd(security,"fund_indexusagefeeratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundIndexUsageFeeRatio(security:list,*args,**kwargs):
    # 获取指数使用费率
    return w.wss(security,"fund_indexusagefeeratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPChRedMMaxRedMFeeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取赎回费率上限时间序列
    return w.wsd(security,"fund_pchredm_maxredmfee",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPChRedMMaxRedMFee(security:list,*args,**kwargs):
    # 获取赎回费率上限
    return w.wss(security,"fund_pchredm_maxredmfee",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPChRedMPChMaxFeeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取申购费率上限时间序列
    return w.wsd(security,"fund_pchredm_pchmaxfee",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPChRedMPChMaxFee(security:list,*args,**kwargs):
    # 获取申购费率上限
    return w.wss(security,"fund_pchredm_pchmaxfee",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundRedemptionFeeRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最高赎回费率时间序列
    return w.wsd(security,"fund_redemptionfeeratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundRedemptionFeeRatio(security:list,*args,**kwargs):
    # 获取最高赎回费率
    return w.wss(security,"fund_redemptionfeeratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundTrackIndexNameSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取跟踪指数名称时间序列
    return w.wsd(security,"fund_trackindexname",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundTrackIndexName(security:list,*args,**kwargs):
    # 获取跟踪指数名称
    return w.wss(security,"fund_trackindexname",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPurchaseFeeRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最高申购费率时间序列
    return w.wsd(security,"fund_purchasefeeratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundPurchaseFeeRatio(security:list,*args,**kwargs):
    # 获取最高申购费率
    return w.wss(security,"fund_purchasefeeratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSaleFeeRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售服务费率时间序列
    return w.wsd(security,"fund_salefeeratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSaleFeeRatio(security:list,*args,**kwargs):
    # 获取销售服务费率
    return w.wss(security,"fund_salefeeratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderUnderwritingSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基本承销额度时间序列
    return w.wsd(security,"tender_underwriting",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderUnderwriting(security:list,*args,**kwargs):
    # 获取基本承销额度
    return w.wss(security,"tender_underwriting",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSimilarFundNoSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取同类基金数量时间序列
    return w.wsd(security,"fund_similarfundno",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSimilarFundNo(security:list,*args,**kwargs):
    # 获取同类基金数量
    return w.wss(security,"fund_similarfundno",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSMfType2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金分级类型时间序列
    return w.wsd(security,"fund_smftype2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSMfType2(security:list,*args,**kwargs):
    # 获取基金分级类型
    return w.wss(security,"fund_smftype2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundRiskLevelFilingSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金风险等级(公告口径)时间序列
    return w.wsd(security,"fund_risklevelfiling",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundRiskLevelFiling(security:list,*args,**kwargs):
    # 获取基金风险等级(公告口径)
    return w.wss(security,"fund_risklevelfiling",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundRiskLevelSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金风险等级时间序列
    return w.wsd(security,"fund_risklevel",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundRiskLevel(security:list,*args,**kwargs):
    # 获取基金风险等级
    return w.wss(security,"fund_risklevel",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundForeignInvestmentAdvisorSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取境外投资顾问时间序列
    return w.wsd(security,"fund_foreigninvestmentadvisor",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundForeignInvestmentAdvisor(security:list,*args,**kwargs):
    # 获取境外投资顾问
    return w.wss(security,"fund_foreigninvestmentadvisor",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderThresholdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取投标利率下限时间序列
    return w.wsd(security,"tender_threshold",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderThreshold(security:list,*args,**kwargs):
    # 获取投标利率下限
    return w.wss(security,"tender_threshold",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderCeilingSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取投标利率上限时间序列
    return w.wsd(security,"tender_ceiling",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderCeiling(security:list,*args,**kwargs):
    # 获取投标利率上限
    return w.wss(security,"tender_ceiling",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderTenderUnitSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基本投标单位时间序列
    return w.wsd(security,"tender_tenderunit",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTenderTenderUnit(security:list,*args,**kwargs):
    # 获取基本投标单位
    return w.wss(security,"tender_tenderunit",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSaleFeeRatio2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取销售服务费率(支持历史)时间序列
    return w.wsd(security,"fund_salefeeratio2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundSaleFeeRatio2(security:list,*args,**kwargs):
    # 获取销售服务费率(支持历史)
    return w.wss(security,"fund_salefeeratio2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInterestCNvXTyCnBdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取估价利率凸性(中债)时间序列
    return w.wsd(security,"interestcnvxty_cnbd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getInterestCNvXTyCnBd(security:list,*args,**kwargs):
    # 获取估价利率凸性(中债)
    return w.wss(security,"interestcnvxty_cnbd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssueLeadUndRSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取配股主承销商时间序列
    return w.wsd(security,"rightsissue_leadundr",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssueLeadUndR(security:list,*args,**kwargs):
    # 获取配股主承销商
    return w.wss(security,"rightsissue_leadundr",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRateLatestMirCnBdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取市场隐含评级(中债)时间序列
    return w.wsd(security,"rate_latestMIR_cnbd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRateLatestMirCnBd(security:list,*args,**kwargs):
    # 获取市场隐含评级(中债)
    return w.wss(security,"rate_latestMIR_cnbd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsoluteMonthlyCompositeReturnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取月度复合回报时间序列
    return w.wsd(security,"absolute_monthlycompositereturn",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsoluteMonthlyCompositeReturn(security:list,*args,**kwargs):
    # 获取月度复合回报
    return w.wss(security,"absolute_monthlycompositereturn",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoAmountEstSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取预计发行股数时间序列
    return w.wsd(security,"ipo_amount_est",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoAmountEst(security:list,*args,**kwargs):
    # 获取预计发行股数
    return w.wss(security,"ipo_amount_est",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoBeyondActualColleCSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取首发超募资金时间序列
    return w.wsd(security,"ipo_beyondactualcollec",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoBeyondActualColleC(security:list,*args,**kwargs):
    # 获取首发超募资金
    return w.wss(security,"ipo_beyondactualcollec",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoAmtToOtherSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取其它发行数量时间序列
    return w.wsd(security,"ipo_amttoother",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoAmtToOther(security:list,*args,**kwargs):
    # 获取其它发行数量
    return w.wss(security,"ipo_amttoother",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsoluteLowestMonthlyReturnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最低单月回报时间序列
    return w.wsd(security,"absolute_lowestmonthlyreturn",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsoluteLowestMonthlyReturn(security:list,*args,**kwargs):
    # 获取最低单月回报
    return w.wss(security,"absolute_lowestmonthlyreturn",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsoluteHighestMonthlyReturnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最高单月回报时间序列
    return w.wsd(security,"absolute_highestmonthlyreturn",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsoluteHighestMonthlyReturn(security:list,*args,**kwargs):
    # 获取最高单月回报
    return w.wss(security,"absolute_highestmonthlyreturn",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStyleHyAveragePositionTimeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取平均持仓时间(半年)时间序列
    return w.wsd(security,"style_hy_averagepositiontime",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStyleHyAveragePositionTime(security:list,*args,**kwargs):
    # 获取平均持仓时间(半年)
    return w.wss(security,"style_hy_averagepositiontime",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStyleAveragePositionTimeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取平均持仓时间时间序列
    return w.wsd(security,"style_averagepositiontime",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getStyleAveragePositionTime(security:list,*args,**kwargs):
    # 获取平均持仓时间
    return w.wss(security,"style_averagepositiontime",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskDurationSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金组合久期时间序列
    return w.wsd(security,"risk_duration",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskDuration(security:list,*args,**kwargs):
    # 获取基金组合久期
    return w.wss(security,"risk_duration",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoRdPersonSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取研发人员占比时间序列
    return w.wsd(security,"ipo_rdperson",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoRdPerson(security:list,*args,**kwargs):
    # 获取研发人员占比
    return w.wss(security,"ipo_rdperson",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechDdNcrSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取下跌相关系数_PIT时间序列
    return w.wsd(security,"tech_ddncr",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getTechDdNcr(security:list,*args,**kwargs):
    # 获取下跌相关系数_PIT
    return w.wss(security,"tech_ddncr",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoInventionSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发明专利个数时间序列
    return w.wsd(security,"ipo_invention",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoInvention(security:list,*args,**kwargs):
    # 获取发明专利个数
    return w.wss(security,"ipo_invention",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoRevenueSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取近一年营收额时间序列
    return w.wsd(security,"ipo_revenue",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoRevenue(security:list,*args,**kwargs):
    # 获取近一年营收额
    return w.wss(security,"ipo_revenue",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskTrackDeviationTrackIndexSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取日跟踪偏离度(跟踪指数)时间序列
    return w.wsd(security,"risk_trackdeviation_trackindex",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRiskTrackDeviationTrackIndex(security:list,*args,**kwargs):
    # 获取日跟踪偏离度(跟踪指数)
    return w.wss(security,"risk_trackdeviation_trackindex",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowCollectionSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取增发募集资金时间序列
    return w.wsd(security,"fellow_collection",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFellowCollection(security:list,*args,**kwargs):
    # 获取增发募集资金
    return w.wss(security,"fellow_collection",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRating5YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金5年评级时间序列
    return w.wsd(security,"rating_5y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRating5Y(security:list,*args,**kwargs):
    # 获取基金5年评级
    return w.wss(security,"rating_5y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRating3YSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取基金3年评级时间序列
    return w.wsd(security,"rating_3y",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRating3Y(security:list,*args,**kwargs):
    # 获取基金3年评级
    return w.wss(security,"rating_3y",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderAvgNumSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取户均持股数量时间序列
    return w.wsd(security,"holder_avgnum",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getHolderAvgNum(security:list,*args,**kwargs):
    # 获取户均持股数量
    return w.wss(security,"holder_avgnum",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSConvexityIfExeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取行权利差凸性时间序列
    return w.wsd(security,"Sconvexity_ifexe",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSConvexityIfExe(security:list,*args,**kwargs):
    # 获取行权利差凸性
    return w.wss(security,"Sconvexity_ifexe",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBConvexityIfExeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取行权基准凸性时间序列
    return w.wsd(security,"Bconvexity_ifexe",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBConvexityIfExe(security:list,*args,**kwargs):
    # 获取行权基准凸性
    return w.wss(security,"Bconvexity_ifexe",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getModiDurationIfExeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取行权修正久期时间序列
    return w.wsd(security,"modiduration_ifexe",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getModiDurationIfExe(security:list,*args,**kwargs):
    # 获取行权修正久期
    return w.wss(security,"modiduration_ifexe",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsoluteAvgMonthlyReturnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取平均月度回报时间序列
    return w.wsd(security,"absolute_avgmonthlyreturn",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsoluteAvgMonthlyReturn(security:list,*args,**kwargs):
    # 获取平均月度回报
    return w.wss(security,"absolute_avgmonthlyreturn",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsoluteLowestQuatreTurnSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最低季度回报时间序列
    return w.wsd(security,"absolute_lowestquatreturn",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAbsoluteLowestQuatreTurn(security:list,*args,**kwargs):
    # 获取最低季度回报
    return w.wss(security,"absolute_lowestquatreturn",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundDaysToConversionSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取剩余折算天数时间序列
    return w.wsd(security,"fund_daystoconversion",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundDaysToConversion(security:list,*args,**kwargs):
    # 获取剩余折算天数
    return w.wss(security,"fund_daystoconversion",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalTDiscountRatioSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取整体折溢价率时间序列
    return w.wsd(security,"anal_tdiscountratio",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalTDiscountRatio(security:list,*args,**kwargs):
    # 获取整体折溢价率
    return w.wss(security,"anal_tdiscountratio",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoOpAmountSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取网下冻结资金时间序列
    return w.wsd(security,"ipo_op_amount",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoOpAmount(security:list,*args,**kwargs):
    # 获取网下冻结资金
    return w.wss(security,"ipo_op_amount",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getListStepSizeSubsCrOfFlSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取网下申购步长时间序列
    return w.wsd(security,"list_stepsizesubscroffl",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getListStepSizeSubsCrOfFl(security:list,*args,**kwargs):
    # 获取网下申购步长
    return w.wss(security,"list_stepsizesubscroffl",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoSPriceMinSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取初步询价下限时间序列
    return w.wsd(security,"ipo_SPrice_min",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoSPriceMin(security:list,*args,**kwargs):
    # 获取初步询价下限
    return w.wss(security,"ipo_SPrice_min",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoSPriceMaxSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取初步询价上限时间序列
    return w.wsd(security,"ipo_SPrice_max",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoSPriceMax(security:list,*args,**kwargs):
    # 获取初步询价上限
    return w.wss(security,"ipo_SPrice_max",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoPriceMinSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行价格下限(底价)时间序列
    return w.wsd(security,"ipo_price_min",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoPriceMin(security:list,*args,**kwargs):
    # 获取发行价格下限(底价)
    return w.wss(security,"ipo_price_min",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoPriceMaxSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取发行价格上限时间序列
    return w.wsd(security,"ipo_price_max",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoPriceMax(security:list,*args,**kwargs):
    # 获取发行价格上限
    return w.wss(security,"ipo_price_max",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoUndRTypeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取首发承销方式时间序列
    return w.wsd(security,"ipo_undrtype",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoUndRType(security:list,*args,**kwargs):
    # 获取首发承销方式
    return w.wss(security,"ipo_undrtype",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoLawFirmSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取首发经办律所时间序列
    return w.wsd(security,"ipo_lawfirm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getIpoLawFirm(security:list,*args,**kwargs):
    # 获取首发经办律所
    return w.wss(security,"ipo_lawfirm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOpToEBTSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取主营业务比率时间序列
    return w.wsd(security,"optoebt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOpToEBT(security:list,*args,**kwargs):
    # 获取主营业务比率
    return w.wss(security,"optoebt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaRetainedPsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股留存收益_PIT时间序列
    return w.wsd(security,"fa_retainedps",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaRetainedPs(security:list,*args,**kwargs):
    # 获取每股留存收益_PIT
    return w.wss(security,"fa_retainedps",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDailyCfSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取指定日现金流时间序列
    return w.wsd(security,"dailycf",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getDailyCf(security:list,*args,**kwargs):
    # 获取指定日现金流
    return w.wss(security,"dailycf",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRetainedPs2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股留存收益_GSD时间序列
    return w.wsd(security,"wgsd_retainedps2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDRetainedPs2(security:list,*args,**kwargs):
    # 获取每股留存收益_GSD
    return w.wss(security,"wgsd_retainedps2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaSppSSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股盈余公积_PIT时间序列
    return w.wsd(security,"fa_spps",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaSppS(security:list,*args,**kwargs):
    # 获取每股盈余公积_PIT
    return w.wss(security,"fa_spps",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSurplusReservePsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股盈余公积时间序列
    return w.wsd(security,"surplusreserveps",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSurplusReservePs(security:list,*args,**kwargs):
    # 获取每股盈余公积
    return w.wss(security,"surplusreserveps",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaCapSurPpSSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股资本公积_PIT时间序列
    return w.wsd(security,"fa_capsurpps",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaCapSurPpS(security:list,*args,**kwargs):
    # 获取每股资本公积_PIT
    return w.wss(security,"fa_capsurpps",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSurplusCapitalPsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股资本公积时间序列
    return w.wsd(security,"surpluscapitalps",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSurplusCapitalPs(security:list,*args,**kwargs):
    # 获取每股资本公积
    return w.wss(security,"surpluscapitalps",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaOrPsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股营业收入_PIT时间序列
    return w.wsd(security,"fa_orps",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFaOrPs(security:list,*args,**kwargs):
    # 获取每股营业收入_PIT
    return w.wss(security,"fa_orps",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDOrPsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股营业收入_GSD时间序列
    return w.wsd(security,"wgsd_orps",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWgsDOrPs(security:list,*args,**kwargs):
    # 获取每股营业收入_GSD
    return w.wss(security,"wgsd_orps",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOrPsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股营业收入时间序列
    return w.wsd(security,"orps",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOrPs(security:list,*args,**kwargs):
    # 获取每股营业收入
    return w.wss(security,"orps",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOrPsTtMSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股营业收入(TTM)_PIT时间序列
    return w.wsd(security,"orps_ttm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getOrPsTtM(security:list,*args,**kwargs):
    # 获取每股营业收入(TTM)_PIT
    return w.wss(security,"orps_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalSmFbFactualCostSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取实际资金成本时间序列
    return w.wsd(security,"anal_smfbfactualcost",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalSmFbFactualCost(security:list,*args,**kwargs):
    # 获取实际资金成本
    return w.wss(security,"anal_smfbfactualcost",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalSmFbNamedCostSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取名义资金成本时间序列
    return w.wsd(security,"anal_smfbnamedcost",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getAnalSmFbNamedCost(security:list,*args,**kwargs):
    # 获取名义资金成本
    return w.wss(security,"anal_smfbnamedcost",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRetainedPsSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取每股留存收益时间序列
    return w.wsd(security,"retainedps",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRetainedPs(security:list,*args,**kwargs):
    # 获取每股留存收益
    return w.wss(security,"retainedps",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSDurationIfExeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取行权利差久期时间序列
    return w.wsd(security,"Sduration_ifexe",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getSDurationIfExe(security:list,*args,**kwargs):
    # 获取行权利差久期
    return w.wss(security,"Sduration_ifexe",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBDurationIfExeSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取行权基准久期时间序列
    return w.wsd(security,"Bduration_ifexe",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBDurationIfExe(security:list,*args,**kwargs):
    # 获取行权基准久期
    return w.wss(security,"Bduration_ifexe",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWeightedRt2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取加权剩余期限(按本金)时间序列
    return w.wsd(security,"weightedrt2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWeightedRt2(security:list,*args,**kwargs):
    # 获取加权剩余期限(按本金)
    return w.wss(security,"weightedrt2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNavAdjustedTransformSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取复权单位净值(支持转型基金)时间序列
    return w.wsd(security,"NAV_adjusted_transform",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNavAdjustedTransform(security:list,*args,**kwargs):
    # 获取复权单位净值(支持转型基金)
    return w.wss(security,"NAV_adjusted_transform",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNavAccumulatedTransformSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取累计单位净值(支持转型基金)时间序列
    return w.wsd(security,"NAV_accumulated_transform",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNavAccumulatedTransform(security:list,*args,**kwargs):
    # 获取累计单位净值(支持转型基金)
    return w.wss(security,"NAV_accumulated_transform",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNavAccSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取累计单位净值时间序列
    return w.wsd(security,"NAV_acc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNavAcc(security:list,*args,**kwargs):
    # 获取累计单位净值
    return w.wss(security,"NAV_acc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNavAdj2Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取复权单位净值(不前推)时间序列
    return w.wsd(security,"NAV_adj2",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNavAdj2(security:list,*args,**kwargs):
    # 获取复权单位净值(不前推)
    return w.wss(security,"NAV_adj2",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNavAdjSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取复权单位净值时间序列
    return w.wsd(security,"NAV_adj",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNavAdj(security:list,*args,**kwargs):
    # 获取复权单位净值
    return w.wss(security,"NAV_adj",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundNavCurSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取单位净值币种时间序列
    return w.wsd(security,"fund_navcur",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFundNavCur(security:list,*args,**kwargs):
    # 获取单位净值币种
    return w.wss(security,"fund_navcur",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPqAmountSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取区间成交金额时间序列
    return w.wsd(security,"pq_amount",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getPqAmount(security:list,*args,**kwargs):
    # 获取区间成交金额
    return w.wss(security,"pq_amount",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNeTaskBstSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取报价卖出净价(最优)时间序列
    return w.wsd(security,"netask_bst",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNeTaskBst(security:list,*args,**kwargs):
    # 获取报价卖出净价(最优)
    return w.wss(security,"netask_bst",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetBidBstSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取报价买入净价(最优)时间序列
    return w.wsd(security,"netbid_bst",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetBidBst(security:list,*args,**kwargs):
    # 获取报价买入净价(最优)
    return w.wss(security,"netbid_bst",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNeTaskAvgSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取报价卖出净价(算术平均)时间序列
    return w.wsd(security,"netask_avg",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNeTaskAvg(security:list,*args,**kwargs):
    # 获取报价卖出净价(算术平均)
    return w.wss(security,"netask_avg",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNavSellPriceSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取投连险卖出价时间序列
    return w.wsd(security,"NAV_sellprice",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNavSellPrice(security:list,*args,**kwargs):
    # 获取投连险卖出价
    return w.wss(security,"NAV_sellprice",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetBidAvgSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取报价买入净价(算术平均)时间序列
    return w.wsd(security,"netbid_avg",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getNetBidAvg(security:list,*args,**kwargs):
    # 获取报价买入净价(算术平均)
    return w.wss(security,"netbid_avg",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBinetAskBstSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取双边卖出净价(最优)时间序列
    return w.wsd(security,"binetask_bst",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBinetAskBst(security:list,*args,**kwargs):
    # 获取双边卖出净价(最优)
    return w.wss(security,"binetask_bst",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBinetBidBstSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取双边买入净价(最优)时间序列
    return w.wsd(security,"binetbid_bst",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBinetBidBst(security:list,*args,**kwargs):
    # 获取双边买入净价(最优)
    return w.wss(security,"binetbid_bst",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBinetAskWtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取双边卖出净价(加权平均)时间序列
    return w.wsd(security,"binetask_wt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBinetAskWt(security:list,*args,**kwargs):
    # 获取双边卖出净价(加权平均)
    return w.wss(security,"binetask_wt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBinetBidWtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取双边买入净价(加权平均)时间序列
    return w.wsd(security,"binetbid_wt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBinetBidWt(security:list,*args,**kwargs):
    # 获取双边买入净价(加权平均)
    return w.wss(security,"binetbid_wt",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLastDateShcSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最新估值日期(上清所)时间序列
    return w.wsd(security,"lastdate_shc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLastDateShc(security:list,*args,**kwargs):
    # 获取最新估值日期(上清所)
    return w.wss(security,"lastdate_shc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getModiDuraShcSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取估价修正久期(上清所)时间序列
    return w.wsd(security,"modidura_shc",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getModiDuraShc(security:list,*args,**kwargs):
    # 获取估价修正久期(上清所)
    return w.wss(security,"modidura_shc",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEbValCsiSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取可交换债估值(中证指数)时间序列
    return w.wsd(security,"ebval_csi",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getEbValCsi(security:list,*args,**kwargs):
    # 获取可交换债估值(中证指数)
    return w.wss(security,"ebval_csi",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLastDateCsiSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最新估值日期(中证指数)时间序列
    return w.wsd(security,"lastdate_csi",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLastDateCsi(security:list,*args,**kwargs):
    # 获取最新估值日期(中证指数)
    return w.wss(security,"lastdate_csi",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getModiDuraCsi1Series(security:list, startDate,endDate,*args,**kwargs):
    # 获取估价修正久期(中证指数)时间序列
    return w.wsd(security,"modidura_csi1",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getModiDuraCsi1(security:list,*args,**kwargs):
    # 获取估价修正久期(中证指数)
    return w.wss(security,"modidura_csi1",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLastDateCnBdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取最新估值日期(中债)时间序列
    return w.wsd(security,"lastdate_cnbd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getLastDateCnBd(security:list,*args,**kwargs):
    # 获取最新估值日期(中债)
    return w.wss(security,"lastdate_cnbd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBIqTvOlmSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取双边报价笔数时间序列
    return w.wsd(security,"biqtvolm",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getBIqTvOlm(security:list,*args,**kwargs):
    # 获取双边报价笔数
    return w.wss(security,"biqtvolm",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFinaRemainingNumberSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取存量债券数目时间序列
    return w.wsd(security,"fina_remainingnumber",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getFinaRemainingNumber(security:list,*args,**kwargs):
    # 获取存量债券数目
    return w.wss(security,"fina_remainingnumber",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssueCollectionSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取配股募集资金时间序列
    return w.wsd(security,"rightsissue_collection",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getRightsIssueCollection(security:list,*args,**kwargs):
    # 获取配股募集资金
    return w.wss(security,"rightsissue_collection",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReturnYTdSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取今年以来回报时间序列
    return w.wsd(security,"return_ytd",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getReturnYTd(security:list,*args,**kwargs):
    # 获取今年以来回报
    return w.wss(security,"return_ytd",*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWeightedRtSeries(security:list, startDate,endDate,*args,**kwargs):
    # 获取加权剩余期限(按本息)时间序列
    return w.wsd(security,"weightedrt",startDate,endDate,*args,**kwargs,usedf=True)
@convertInputSecurityType
def getWeightedRt(security:list,*args,**kwargs):
    # 获取加权剩余期限(按本息)
    return w.wss(security,"weightedrt",*args,**kwargs,usedf=True)
#-<End>









