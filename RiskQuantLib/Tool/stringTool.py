#!/usr/bin/python
#coding = utf-8

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
    result = [float(i) for i in strList]
    return result


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


#<strTool>
#</strTool>




