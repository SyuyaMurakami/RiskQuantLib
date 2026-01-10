#!/usr/bin/python
#coding = utf-8

import pandas as pd
import QuantLib as ql
from typing import List, Optional, Sequence
from RiskQuantLib.Tool.decoratorTool import stringTimestampConverter

#<import>
#</import>

class calendar(object):
    unitKey = ['W', 'w', 'M', 'm', 'D', 'd', 'Y', 'y']
    unitValue = [ql.Weeks, ql.Weeks, ql.Months, ql.Months, ql.Days, ql.Days, ql.Years, ql.Years]
    unitMap = dict(zip(unitKey, unitValue))

    @staticmethod
    def parsePeriod(period: str) -> (int, int):
        n, unit = int(period[:-1]), period[-1]
        assert n > 0
        assert unit in set(calendar.unitKey)
        return n, calendar.unitMap[unit]

    @staticmethod
    def timestampToDate(date: pd.Timestamp) -> ql.Date:
        return ql.Date(date.day, date.month, date.year)

    @staticmethod
    def dateToTimestamp(date: ql.Date) -> pd.Timestamp:
        return pd.Timestamp(date.to_date())

    @stringTimestampConverter(argIterableIndexList=[2], argIterableKeyList=['otherHolidays'])
    def __init__(self, holidayRule: ql.Calendar, otherHolidays: Optional[Sequence[pd.Timestamp]] = None) -> None:
        self.updateCalendar(holidayRule, otherHolidays)

    @stringTimestampConverter(argIterableIndexList=[2], argIterableKeyList=['otherHolidays'])
    def updateCalendar(self, holidayRule: ql.Calendar, otherHolidays: Optional[Sequence[pd.Timestamp]] = None) -> None:
        """Create a custom calendar using QuantLib."""
        otherHolidays = otherHolidays if otherHolidays else []
        self.addHolidayRule(holidayRule)
        self.addHolidays(otherHolidays)

    def addHolidayRule(self, holidayRule: ql.Calendar) -> None:
        """Add customized holiday rule, this will overwrite current holiday settings."""
        self._otherHolidays = []
        self._qlCalendar = holidayRule
        self._holidayRule = self._qlCalendar.isHoliday

    @stringTimestampConverter(argIterableIndexList=[1], argIterableKeyList=['holidays'])
    def addHolidays(self, holidays: Sequence[pd.Timestamp]) -> None:
        """Add customized holiday."""
        self._otherHolidays.extend(holidays)
        [self._qlCalendar.addHoliday(calendar.timestampToDate(i)) for i in holidays]
        self._holidayRule = self._qlCalendar.isHoliday

    @stringTimestampConverter(argIndexList=[1],argKeyList=['date'])
    def isTrading(self, date: pd.Timestamp) -> bool:
        """Return True if a day is trading day."""
        return not self._holidayRule(calendar.timestampToDate(date))

    @stringTimestampConverter(argIndexList=[1,2], argKeyList=['start', 'end'])
    def tradingDaysBetween(self, start: pd.Timestamp, end: pd.Timestamp, startPoint: bool = True, endPoint: bool = True) -> List[pd.Timestamp]:
        """
        Return a list of trading days between *start* and *end*. Endpoints
        are counted only if they are trading.
        """
        startAdjust = start if startPoint else start + pd.Timedelta(days=1)
        startQlDate = calendar.timestampToDate(startAdjust)
        endAdjust = end if endPoint else end + pd.Timedelta(days=-1)
        endQlDate = calendar.timestampToDate(endAdjust)
        return [calendar.dateToTimestamp(i) for i in self._qlCalendar.businessDayList(startQlDate, endQlDate)]

    @stringTimestampConverter(argIndexList=[1], argKeyList=['date'])
    def offset(self, date: pd.Timestamp, n: int, period: int = ql.Days) -> pd.Timestamp:
        """Return date of trading day *n* days before or after *date*."""
        qlDate = calendar.timestampToDate(date)
        offsetDate = self._qlCalendar.advance(qlDate, n, period)
        return calendar.dateToTimestamp(offsetDate)

    @stringTimestampConverter(argIndexList=[1, 2], argKeyList=['start', 'end'])
    def makeSchedule(self, start: pd.Timestamp, end: pd.Timestamp, period: str, forwardAdjust: bool = True, forwardScale: bool = True, forwardAdjustEndDay: bool = False):
        """Generate periodical trading dates between start and end, given period."""
        n, periodQl = calendar.parsePeriod(period)
        convention = ql.Following if forwardAdjust else ql.Preceding
        terminalDateConvention = ql.Following if forwardAdjustEndDay else ql.Preceding
        forwards, backwards = (True, False) if forwardScale else (False, True)
        startQlDate, endQlDate = calendar.timestampToDate(start), calendar.timestampToDate(end)
        schedule = ql.MakeSchedule(startQlDate, endQlDate, ql.Period(n, periodQl), calendar=self._qlCalendar, convention=convention, terminalDateConvention=terminalDateConvention,forwards=forwards, backwards=backwards)
        return [calendar.dateToTimestamp(i) for i in schedule]

    @stringTimestampConverter(argIndexList=[1], argKeyList=['start'])
    def makeScheduleByPeriod(self, start: pd.Timestamp, period: str, count: int, forwardAdjust: bool = True) -> List[pd.Timestamp]:
        """
        Generate periodical trading dates.
        Warnings: If the first day is not a trading day, the next trading day will be used, thus leading
        to duplicated elements. So make sure the given start date is a trading day.
        """
        n, periodQl = calendar.parsePeriod(period)
        convention = ql.Following if forwardAdjust else ql.Preceding
        dateQl = calendar.timestampToDate(start)
        tradingDates = [self._qlCalendar.advance(dateQl, i*n, periodQl, convention) for i in range(count)]
        return [calendar.dateToTimestamp(i) for i in tradingDates]

    @stringTimestampConverter(argIndexList=[1, 2], argKeyList=['start', 'end'])
    def numTradingDaysBetween(self, start: pd.Timestamp, end: pd.Timestamp, countStart: bool = True, countEnd: bool = True) -> int:
        """Return number of trading days between two dates."""
        startQlDate, endQlDate = calendar.timestampToDate(start), calendar.timestampToDate(end)
        return self._qlCalendar.businessDaysBetween(startQlDate, endQlDate, countStart, countEnd)

    @stringTimestampConverter(argIndexList=[1], argKeyList=['start'], argIterableIndexList=[2], argIterableKeyList=['dateList'])
    def numTradingDaysBetweenGrid(self, start: pd.Timestamp, dateList: Sequence[pd.Timestamp], countStart: bool = True, countEnd: bool = True) -> List[int]:
        """Return number of trading days between a date and a date list."""
        return [self.numTradingDaysBetween(start, end, countStart, countEnd) for end in dateList]

    #<calendar>
    #</calendar>


@stringTimestampConverter(argIndexList=[2], argKeyList=['on'])
def getNthWeekday(count:int, weekdayCode:int, on:pd.Timestamp):
    """
    This function will return the n-th weekday of the month, which contains the given day.

    Parameters
    ----------
    count : int
        The n-th weekday you want to get
    weekdayCode : int
        The weekday code, use int from 1 to 7
    on : pd.Timestamp
        The standing point, calculation will be done based on this day.

    Returns
    -------
    result : pd.Timestamp
    """
    firstDayAtThatMonth = pd.Timestamp(on.year, on.month, 1)
    weekdayCodeBenchMark = firstDayAtThatMonth.dayofweek + 1
    if count == 0:
        raise Exception("Error: N can't be 0!\n")
    elif count<0:
        count = count+1
    else:
        pass
    if weekdayCode>=weekdayCodeBenchMark:
        days = (count-1)*7 + weekdayCode-weekdayCodeBenchMark
    else:
        days = count * 7 + weekdayCode - weekdayCodeBenchMark
    resultDay = firstDayAtThatMonth + pd.Timedelta(days=days)
    return resultDay

@stringTimestampConverter(argIndexList=[0,1], argKeyList=['start', 'end'])
def generateBusinessDateList(start: pd.Timestamp, end: pd.Timestamp, freq:str='D'):
    """
    This function will generate a list of business day.

    Parameters
    ----------
    start : pd.Timestamp
        The range start.
    end : pd.Timestamp
        The range end
    freq : str
        The frequency used to generate date list.

    Returns
    -------
    list
    """
    businessList = pd.date_range(start.strftime("%Y-%m-%d"),end.strftime("%Y-%m-%d"),freq=freq).to_list()
    return [i for i in businessList if i.dayofweek<5]

@stringTimestampConverter(argIndexList=[0], argKeyList=['start'])
def generateNextNWeekday(start: pd.Timestamp, count: int):
    """
    This function will return a list, whose elements are the next n weekdays.
    """
    startDate_FormedStr = start.strftime("%Y-%m-%d")
    endDate_FormedStr = (start + pd.Timedelta(days=int(count/5*7)+10)).strftime("%Y-%m-%d")
    return [i for i in pd.date_range(startDate_FormedStr,endDate_FormedStr,freq='D').to_list() if i.dayofweek<5][:count]


#<dateTool>
#</dateTool>

# Quick link for non-QuantLib users.

class null(calendar):
    holidayRule = ql.NullCalendar()
    """Quick way to initialize a null calendar."""
    @stringTimestampConverter(argIterableIndexList=[1], argIterableKeyList=['otherHolidays'])
    def __init__(self, otherHolidays: Optional[Sequence[pd.Timestamp]] = None) -> None:
        super().__init__(self.holidayRule, otherHolidays)


class argentinaMerval(null):
    """Quick way to initialize calendar of Argentina Merval."""
    holidayRule = ql.Argentina(ql.Argentina.Merval)


class australiaSettlement(null):
    """Quick way to initialize calendar of Australia Settlement."""
    holidayRule = ql.Australia(ql.Australia.Settlement)


class australiaASX(null):
    """Quick way to initialize calendar of Australia ASX."""
    holidayRule = ql.Australia(ql.Australia.ASX)


class austriaSettlement(null):
    """Quick way to initialize calendar of Austria Settlement."""
    holidayRule = ql.Austria(ql.Austria.Settlement)


class austriaExchange(null):
    """Quick way to initialize calendar of Austria Exchange."""
    holidayRule = ql.Austria(ql.Austria.Exchange)


class botswana(null):
    """Quick way to initialize calendar of Botswana."""
    holidayRule = ql.Botswana()


class brazilSettlement(null):
    """Quick way to initialize calendar of Brazil Settlement."""
    holidayRule = ql.Brazil(ql.Brazil.Settlement)


class brazilExchange(null):
    """Quick way to initialize calendar of Brazil Exchange."""
    holidayRule = ql.Brazil(ql.Brazil.Exchange)


class canadaSettlement(null):
    """Quick way to initialize calendar of Canada Settlement."""
    holidayRule = ql.Canada(ql.Canada.Settlement)


class canadaTSX(null):
    """Quick way to initialize calendar of Canada TSX."""
    holidayRule = ql.Canada(ql.Canada.TSX)


class chileSSE(null):
    """Quick way to initialize calendar of Chile SSE."""
    holidayRule = ql.Chile(ql.Chile.SSE)


class chinaSSE(null):
    """Quick way to initialize calendar of China SSE."""
    holidayRule = ql.China(ql.China.SSE)


class chinaIB(null):
    """Quick way to initialize calendar of China IB."""
    holidayRule = ql.China(ql.China.IB)
    

class czechRepublicPSE(null):
    """Quick way to initialize calendar of CzechRepublic PSE."""
    holidayRule = ql.CzechRepublic(ql.CzechRepublic.PSE)


class denmark(null):
    """Quick way to initialize calendar of Denmark."""
    holidayRule = ql.Denmark()


class finland(null):
    """Quick way to initialize calendar of Finland."""
    holidayRule = ql.Finland()


class franceSettlement(null):
    """Quick way to initialize calendar of France Settlement."""
    holidayRule = ql.France(ql.France.Settlement)


class franceExchange(null):
    """Quick way to initialize calendar of France Exchange."""
    holidayRule = ql.France(ql.France.Exchange)


class germanySettlement(null):
    """Quick way to initialize calendar of Germany Settlement."""
    holidayRule = ql.Germany(ql.Germany.Settlement)


class germanyFrankfurtStockExchange(null):
    """Quick way to initialize calendar of Germany FrankfurtStockExchange."""
    holidayRule = ql.Germany(ql.Germany.FrankfurtStockExchange)


class germanyXetra(null):
    """Quick way to initialize calendar of Germany Xetra."""
    holidayRule = ql.Germany(ql.Germany.Xetra)


class germanyEurex(null):
    """Quick way to initialize calendar of Germany Eurex."""
    holidayRule = ql.Germany(ql.Germany.Eurex)


class hongKongHKEx(null):
    """Quick way to initialize calendar of HongKong HKEx."""
    holidayRule = ql.HongKong(ql.HongKong.HKEx)


class hungary(null):
    """Quick way to initialize calendar of Hungary."""
    holidayRule = ql.Hungary()


class icelandICEX(null):
    """Quick way to initialize calendar of Iceland ICEX."""
    holidayRule = ql.Iceland(ql.Iceland.ICEX)


class indiaNSE(null):
    """Quick way to initialize calendar of India NSE."""
    holidayRule = ql.India(ql.India.NSE)


class indonesiaBEJ(null):
    """Quick way to initialize calendar of Indonesia BEJ."""
    holidayRule = ql.Indonesia(ql.Indonesia.BEJ)
    
    
class indonesiaJSX(null):
    """Quick way to initialize calendar of Indonesia JSX."""
    holidayRule = ql.Indonesia(ql.Indonesia.JSX)


class israelSettlement(null):
    """Quick way to initialize calendar of Israel Settlement."""
    holidayRule = ql.Israel(ql.Israel.Settlement)


class israelTASE(null):
    """Quick way to initialize calendar of Israel TASE."""
    holidayRule = ql.Israel(ql.Israel.TASE)


class israelSHIR(null):
    """Quick way to initialize calendar of Israel SHIR."""
    holidayRule = ql.Israel(ql.Israel.SHIR)


class italySettlement(null):
    """Quick way to initialize calendar of Italy Settlement."""
    holidayRule = ql.Italy(ql.Italy.Settlement)


class italyExchange(null):
    """Quick way to initialize calendar of Italy Exchange."""
    holidayRule = ql.Italy(ql.Italy.Exchange)


class japan(null):
    """Quick way to initialize calendar of Japan."""
    holidayRule = ql.Japan()


class mexicoBMV(null):
    """Quick way to initialize calendar of Mexico BMV."""
    holidayRule = ql.Mexico(ql.Mexico.BMV)


class newZealandWellington(null):
    """Quick way to initialize calendar of NewZealand Wellington."""
    holidayRule = ql.NewZealand(ql.NewZealand.Wellington)


class newZealandAuckland(null):
    """Quick way to initialize calendar of NewZealand Auckland."""
    holidayRule = ql.NewZealand(ql.NewZealand.Auckland)


class norway(null):
    """Quick way to initialize calendar of Norway."""
    holidayRule = ql.Norway()


class polandSettlement(null):
    """Quick way to initialize calendar of Poland Settlement."""
    holidayRule = ql.Poland(ql.Poland.Settlement)


class polandWSE(null):
    """Quick way to initialize calendar of Poland WSE."""
    holidayRule = ql.Poland(ql.Poland.WSE)


class romaniaPublic(null):
    """Quick way to initialize calendar of Romania Public."""
    holidayRule = ql.Romania(ql.Romania.Public)


class romaniaBVB(null):
    """Quick way to initialize calendar of Romania BVB."""
    holidayRule = ql.Romania(ql.Romania.BVB)


class russiaSettlement(null):
    """Quick way to initialize calendar of Russia Settlement."""
    holidayRule = ql.Russia(ql.Russia.Settlement)


class russiaMOEX(null):
    """Quick way to initialize calendar of Russia MOEX."""
    holidayRule = ql.Russia(ql.Russia.MOEX)


class saudiArabiaTadawul(null):
    """Quick way to initialize calendar of SaudiArabia Tadawul."""
    holidayRule = ql.SaudiArabia(ql.SaudiArabia.Tadawul)


class singaporeSGX(null):
    """Quick way to initialize calendar of Singapore SGX."""
    holidayRule = ql.Singapore(ql.Singapore.SGX)


class slovakiaBSSE(null):
    """Quick way to initialize calendar of Slovakia BSSE."""
    holidayRule = ql.Slovakia(ql.Slovakia.BSSE)


class southAfrica(null):
    """Quick way to initialize calendar of SouthAfrica."""
    holidayRule = ql.SouthAfrica()


class southKoreaSettlement(null):
    """Quick way to initialize calendar of SouthKorea Settlement."""
    holidayRule = ql.SouthKorea(ql.SouthKorea.Settlement)


class southKoreaKRX(null):
    """Quick way to initialize calendar of SouthKorea KRX."""
    holidayRule = ql.SouthKorea(ql.SouthKorea.KRX)


class sweden(null):
    """Quick way to initialize calendar of Sweden."""
    holidayRule = ql.Sweden()


class switzerland(null):
    """Quick way to initialize calendar of Switzerland."""
    holidayRule = ql.Switzerland()


class taiwanTSEC(null):
    """Quick way to initialize calendar of Taiwan TSEC."""
    holidayRule = ql.Taiwan(ql.Taiwan.TSEC)


class thailand(null):
    """Quick way to initialize calendar of Thailand."""
    holidayRule = ql.Thailand()


class turkey(null):
    """Quick way to initialize calendar of Turkey."""
    holidayRule = ql.Turkey()


class ukraineUSE(null):
    """Quick way to initialize calendar of Ukraine USE."""
    holidayRule = ql.Ukraine(ql.Ukraine.USE)


class unitedKingdomSettlement(null):
    """Quick way to initialize calendar of UnitedKingdom Settlement."""
    holidayRule = ql.UnitedKingdom(ql.UnitedKingdom.Settlement)


class unitedKingdomExchange(null):
    """Quick way to initialize calendar of UnitedKingdom Exchange."""
    holidayRule = ql.UnitedKingdom(ql.UnitedKingdom.Exchange)


class unitedKingdomMetals(null):
    """Quick way to initialize calendar of UnitedKingdom Metals."""
    holidayRule = ql.UnitedKingdom(ql.UnitedKingdom.Metals)


class unitedStatesSettlement(null):
    """Quick way to initialize calendar of UnitedStates Settlement."""
    holidayRule = ql.UnitedStates(ql.UnitedStates.Settlement)


class unitedStatesNYSE(null):
    """Quick way to initialize calendar of UnitedStates NYSE."""
    holidayRule = ql.UnitedStates(ql.UnitedStates.NYSE)


class unitedStatesGovernmentBond(null):
    """Quick way to initialize calendar of UnitedStates GovernmentBond."""
    holidayRule = ql.UnitedStates(ql.UnitedStates.GovernmentBond)


class unitedStatesNERC(null):
    """Quick way to initialize calendar of UnitedStates NERC."""
    holidayRule = ql.UnitedStates(ql.UnitedStates.NERC)


class unitedStatesLiborImpact(null):
    """Quick way to initialize calendar of UnitedStates LiborImpact."""
    holidayRule = ql.UnitedStates(ql.UnitedStates.LiborImpact)


class unitedStatesFederalReserve(null):
    """Quick way to initialize calendar of UnitedStates FederalReserve."""
    holidayRule = ql.UnitedStates(ql.UnitedStates.FederalReserve)


class unitedStatesSOFR(null):
    """Quick way to initialize calendar of UnitedStates SOFR."""
    holidayRule = ql.UnitedStates(ql.UnitedStates.SOFR)


