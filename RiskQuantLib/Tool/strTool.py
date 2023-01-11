#!/usr/bin/python
#coding = utf-8

import QuantLib as ql
import pandas as pd
#<import>
#</import>

def getDigitsFromStr(string:str,withDigitPoint:bool = False):
    """
    Extract number from a string. Return a list whose element is strings that is number.

    Parameters
    ----------
    string : str
        The string that may contain numbers.
    withDigitPoint : bool
        Use true is the numbers are float. False if all numbers are int.

    Returns
    -------
    strList : list
        A list whose elements are string that can be converted into numbers.
    """
    import re
    if withDigitPoint:
        strList = re.findall(r"\d+\.?\d*",string)
    else:
        strList = re.findall(r"\d+\d*",string)
    return strList

def getNumbersFromStr(string:str,withDigitPoint:bool = False):
    """
    Extract number from a string. Return a list whose element is number.

    Parameters
    ----------
    string : str
        The string that may contain numbers.
    withDigitPoint : bool
        Use true is the numbers are float. False if all numbers are int.

    Returns
    -------
    strList : list
        A list whose elements are numbers.
    """
    strList = getDigitsFromStr(string,withDigitPoint)
    result = [i for i in strList]
    return result

def getNthWeekday(n:int,weekdayCode:int,TimeStamp:pd.Timestamp):
    """
    This function will return the n-th weekday of the month, which contains the given day.

    Parameters
    ----------
    n : int
        The n-th weekday you want to get
    weekdayCode : int
        The weekday code, use int from 1 to 7
    TimeStamp : pd.Timestamp
        The standing point, calculation will be done based on this day.

    Returns
    -------
    result : pd.Timestamp
    """
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

def convertNumberOfDaysToChineseStr(numberOfDays:int):
    """
    This function will convert number of days into Chinese string, such as
    '一个月','三个月',etc.
    """
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

def changeSeriesIndexTypeFromStrToTimestamp(pdSeries:pd.Series):
    """
    This function will change the data type of pd.Series.index into pd.Timestamp
    """
    import pandas as pd
    pdSeries.index = [pd.Timestamp(i) for i in pdSeries.index]
    return pdSeries

def generateBusinessDateList(startDateString:str,endDateString:str,freq:str='D'):
    """
    This function will generate a list of business day.

    Parameters
    ----------
    startDateString : str
        The range start.
    endDateString : str
        The range end
    freq : str
        The frequency used to generate date list.

    Returns
    -------
    list
    """
    import pandas as pd
    startDate = pd.Timestamp(startDateString).strftime("%Y-%m-%d")
    endDate = pd.Timestamp(endDateString).strftime("%Y-%m-%d")
    return [i for i in pd.date_range(startDate,endDate,freq=freq).to_list() if i.dayofweek<5]

def generateTradingDateList(startDateString:str,endDateString:str,freq:str='D',qlExchangeObject = ql.China.SSE):
    """
    This function will return a list of trading day, using the trading calendar of China exchange.
    """
    import pandas as pd
    startDate = pd.Timestamp(startDateString).strftime("%Y-%m-%d")
    endDate = pd.Timestamp(endDateString).strftime("%Y-%m-%d")
    calendar = ql.China(qlExchangeObject)
    dateList = [i for i in pd.date_range(startDate,endDate,freq=freq).to_list()]
    dateList = [i for i in dateList if calendar.isBusinessDay(ql.Date(i.strftime("%Y-%m-%d"), '%Y-%m-%d'))]
    return dateList

def isTradingDate(dateString:str, qlExchangeObject = ql.China.SSE):
    """
    This function will return a bool value, telling whether the given date is a trading day,
    using China exchange trading calendar.
    """
    import pandas as pd
    date = pd.Timestamp(dateString)
    calendar = ql.China(qlExchangeObject)
    targetDate = ql.Date(date.strftime("%Y-%m-%d"), '%Y-%m-%d')
    return calendar.isBusinessDay(targetDate)

def generateNextNWeekday(startDateString:str,n:int):
    """
    This function will return a list, whose elements are the next n weekdays.
    """
    import pandas as pd
    startDate = pd.Timestamp(startDateString)
    startDate_FormedStr = startDate.strftime("%Y-%m-%d")
    endDate_FormedStr = (startDate + pd.Timedelta(days=int(n/5*7)+10)).strftime("%Y-%m-%d")
    return [i for i in pd.date_range(startDate_FormedStr,endDate_FormedStr,freq='D').to_list() if i.dayofweek<5][:n]

def changeSecurityListToStr(securityList:list):
    """
    This function will convert a list of string into a single string.
    """
    securityListFormed = [i+',' for i in securityList]
    return "".join(securityListFormed).strip(',')

def getStringSimilarity(string1:str,string2:str):
    """
    This function will return a similarity of two strings.
    """
    import difflib
    return difflib.SequenceMatcher(None,string1,string2).quick_ratio()

def getMostSimilarStringFromList(string:str,stringList:list):
    """
    This function will return the most similar string of a given string, after specifying
    the list where you choose string from.
    """
    similarRatioList = [getStringSimilarity(string,i) for i in stringList]
    return stringList[similarRatioList.index(max(similarRatioList))]

def getLastTradingDate(presentTradingDateString:str):
    """
    This function will return the last trading date given standing point,
    using China exchange trading calendar.
    """
    import pandas as pd
    import QuantLib as ql
    calendar = ql.China(ql.China.SSE)
    presentTradingDate = pd.Timestamp(presentTradingDateString)
    standingPoint = ql.Date(presentTradingDate.strftime("%Y-%m-%d"),'%Y-%m-%d') + ql.Period(-1,ql.Days)
    while not calendar.isBusinessDay(standingPoint):
        standingPoint = standingPoint + ql.Period(-1,ql.Days)
    return pd.Timestamp(standingPoint.year(),standingPoint.month(),standingPoint.dayOfMonth())

def getNextTradingDate(presentTradingDateString:str):
    """
    This function will return the next trading date given standing point,
    using China exchange trading calendar.
    """
    import pandas as pd
    import QuantLib as ql
    calendar = ql.China(ql.China.SSE)
    presentTradingDate = pd.Timestamp(presentTradingDateString)
    standingPoint = ql.Date(presentTradingDate.strftime("%Y-%m-%d"),'%Y-%m-%d') + ql.Period(1,ql.Days)
    while not calendar.isBusinessDay(standingPoint):
        standingPoint = standingPoint + ql.Period(1,ql.Days)
    return pd.Timestamp(standingPoint.year(),standingPoint.month(),standingPoint.dayOfMonth())

def getNTradingDaysBeforeTradingDate(days:int,presentTradingDateString:str):
    """
    This function will return the N-th trading day before standing point.
    """
    import pandas as pd
    i = days
    while i!=0:
        presentTradingDateString = getLastTradingDate(presentTradingDateString).strftime("%Y-%m-%d")
        i = i - 1
    return pd.Timestamp(presentTradingDateString)

def getNTradingDaysAfterTradingDate(days:int,presentTradingDateString:str):
    """
    This function will return the N-th trading day after standing point.
    """
    import pandas as pd
    i = 0
    while i!=days:
        presentTradingDateString = getNextTradingDate(presentTradingDateString).strftime("%Y-%m-%d")
        i = i + 1
    return pd.Timestamp(presentTradingDateString)

def convertTimeToString(time,formatString = "%Y-%m-%d"):
    """
    This function will convert pd.Timestamp into string.
    """
    try:
        return time.strftime(formatString)
    except Exception as e:
        return ''

#<strTool>
#</strTool>




