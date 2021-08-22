#!/usr/bin/python
#coding = utf-8
import QuantLib as ql

def getDigitsFromStr(string,withDigitPoint = False):# 字符串提取数字
	import re
	if withDigitPoint:
		strList = re.findall(r"\d+\.?\d*",string)
	else:
		strList = re.findall(r"\d+\d*",string)
	return strList

def getNumbersFromStr(string,withDigitPoint = False):
	strList = getDigitsFromStr(string,withDigitPoint)
	result = [i for i in strList]
	return result

def getNthWeekday(n,weekdayCode,TimeStamp):# 获得某个日期所在月份的第n个星期三
	import pandas as pd
	firstDayAtThatMonth = pd.Timestamp(TimeStamp.year,TimeStamp.month,1)
	weekdayCodeBenchMark = firstDayAtThatMonth.dayofweek + 1
	if n == 0:
		print("Error: N can't be 0!\n")
		exit(-1)
	elif n<0:
		n = n+1
	else:
		pass
	if weekdayCode>=weekdayCodeBenchMark:
		days = (n-1)*7 + weekdayCode-weekdayCodeBenchMark
	else:
		days = n * 7 + weekdayCode - weekdayCodeBenchMark
	resultDay = firstDayAtThatMonth + pd.Timedelta(days=days)
	return resultDay

def convertFutureCodeToExpirationDate(futureCodeString):
	import pandas as pd
	simplifiedStr = getDigitsFromStr(futureCodeString)[0]
	tmpExpirationDay = pd.Timestamp(int('20'+simplifiedStr[:2]),int(simplifiedStr[2:]),12)
	return getNthWeekday(3,6,tmpExpirationDay)

def getFutureTypeByExpirationDate(baseDateTimestamp,expirationDateTimestamp,futureIndexType='Stock_Index'):
	baseMonthNum = (expirationDateTimestamp.year - baseDateTimestamp.year)*12 + (expirationDateTimestamp.month - baseDateTimestamp.month)
	if futureIndexType=='Stock_Index':
		n = 3
		weekday = 6
		if baseDateTimestamp >= getNthWeekday(n,weekday,baseDateTimestamp):
			modifiedBaseMonthNum = baseMonthNum - 1
		else:
			modifiedBaseMonthNum = baseMonthNum
		if modifiedBaseMonthNum < 0:
			return 'Expired'
		elif modifiedBaseMonthNum <1:
			return 'Current'
		elif modifiedBaseMonthNum <2:
			return 'Month'
		elif modifiedBaseMonthNum <3:
			return 'Season'
		elif modifiedBaseMonthNum <6:
			return 'Half Year'
		elif modifiedBaseMonthNum <12:
			return 'Year'
		elif modifiedBaseMonthNum <36:
			return 'Three Year'
		elif modifiedBaseMonthNum <60:
			return 'Five Year'
		elif modifiedBaseMonthNum <120:
			return 'Ten Year'
		else:
			return ''
	elif futureIndexType == 'Bond_Index':
		n = 2
		weekday = 6
		if baseDateTimestamp >= getNthWeekday(n,weekday,baseDateTimestamp):
			modifiedBaseMonthNum = baseMonthNum - 1
		else:
			modifiedBaseMonthNum = baseMonthNum
		if modifiedBaseMonthNum < 0:
			return 'Expired'
		elif modifiedBaseMonthNum <3:
			return 'Three Month'
		elif modifiedBaseMonthNum <6:
			return 'Six Month'
		elif modifiedBaseMonthNum <9:
			return 'Nine Month'
		else:
			return ''
	else:
		pass

def convertNumberOfDaysToChineseStr(numberOfDays):
	try:
		if round(numberOfDays/30)==1:
			return '一个月'
		elif round(numberOfDays/30)<=3:
			return '三个月'
		elif round(numberOfDays/30)<=7:
			return '六个月'
		elif round(numberOfDays/30)<=10:
			return '九个月'
		elif round(numberOfDays/30)<=13:
			return '一年'
		elif round(numberOfDays/365)<=2:
			return '两年'
		elif round(numberOfDays/365)<=3:
			return '三年'
		elif round(numberOfDays/365)<=4:
			return '四年'
		elif round(numberOfDays/365)<=5:
			return '五年'
		elif round(numberOfDays/365)<=6:
			return '六年'
		elif round(numberOfDays/365)<=7:
			return '七年'
		elif round(numberOfDays/365)<=8:
			return '八年'
		elif round(numberOfDays/365)<=9:
			return '九年'
		elif round(numberOfDays/365)<=10:
			return '十年'
		elif round(numberOfDays/365)<=16:
			return '十五年'
		elif round(numberOfDays/365)<=21:
			return '二十年'
		else:
			return str(numberOfDays)
	except Exception as e:
		print(e)
		return numberOfDays

def changeSeriesIndexTypeFromStrToTimestamp(pdSeries):
	import pandas as pd
	pdSeries.index = [pd.Timestamp(i) for i in pdSeries.index]
	return pdSeries

def generateBusinessDateList(startDateString,endDateString,freq='D'):
	import pandas as pd
	startDate = pd.Timestamp(startDateString).strftime("%Y-%m-%d")
	endDate = pd.Timestamp(endDateString).strftime("%Y-%m-%d")
	return [i for i in pd.date_range(startDate,endDate,freq=freq).to_list() if i.dayofweek<5]

def generateTradingDateList(startDateString,endDateString,freq='D',qlExchangeObject = ql.China.SSE):
	import pandas as pd
	startDate = pd.Timestamp(startDateString).strftime("%Y-%m-%d")
	endDate = pd.Timestamp(endDateString).strftime("%Y-%m-%d")
	calendar = ql.China(qlExchangeObject)
	dateList = [i for i in pd.date_range(startDate,endDate,freq=freq).to_list()]
	dateList = [i for i in dateList if calendar.isBusinessDay(ql.Date(i.strftime("%Y-%m-%d"), '%Y-%m-%d'))]
	return dateList

def isTradingDate(dateString, qlExchangeObject = ql.China.SSE):
	import pandas as pd
	date = pd.Timestamp(dateString)
	calendar = ql.China(qlExchangeObject)
	targetDate = ql.Date(date.strftime("%Y-%m-%d"), '%Y-%m-%d')
	return calendar.isBusinessDay(targetDate)

def generateNextNWeekday(startDateString,n):
	import pandas as pd
	startDate = pd.Timestamp(startDateString)
	startDate_FormedStr = startDate.strftime("%Y-%m-%d")
	endDate_FormedStr = (startDate + pd.Timedelta(days=int(n/5*7)+10)).strftime("%Y-%m-%d")
	return [i for i in pd.date_range(startDate_FormedStr,endDate_FormedStr,freq='D').to_list() if i.dayofweek<5][:n]

def changeSecurityListToStr(securityList):
	securityListFormed = [i+',' for i in securityList]
	return "".join(securityListFormed).strip(',')

def getStringSimilarity(string1,string2):
	import difflib
	return difflib.SequenceMatcher(None,string1,string2).quick_ratio()

def getMostSimilarStringFromList(string,stringList):
	similarRatioList = [getStringSimilarity(string,i) for i in stringList]
	return stringList[similarRatioList.index(max(similarRatioList))]

def getLastTradingDate(presentTradingDateString):
	import pandas as pd
	import QuantLib as ql
	calendar = ql.China(ql.China.SSE)
	presentTradingDate = pd.Timestamp(presentTradingDateString)
	standingPoint = ql.Date(presentTradingDate.strftime("%Y-%m-%d"),'%Y-%m-%d') + ql.Period(-1,ql.Days)
	while not calendar.isBusinessDay(standingPoint):
		standingPoint = standingPoint + ql.Period(-1,ql.Days)
	return pd.Timestamp(standingPoint.year(),standingPoint.month(),standingPoint.dayOfMonth())

def getNTradingDaysBeforeTradingDate(days,presentTradingDateString):
	import pandas as pd
	i = days
	while i!=0:
		presentTradingDateString = getLastTradingDate(presentTradingDateString).strftime("%Y-%m-%d")
		i = i - 1
	return pd.Timestamp(presentTradingDateString)

def convertTimeToString(time,formatString = "%Y-%m-%d"):
	try:
		return time.strftime(formatString)
	except Exception as e:
		return ''






