#!/usr/bin/python
#coding = utf-8

import pandas as pd
from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt,RGBColor
#<import>
#</import>

def replaceParagraphContent(paragraph,paraDict:dict):
    """
    This function will replace the paragraph content of word Document object.
    This replace is inplace, so this function returns None. This function is very
    like the str.format() function in python, it replace any symbol like {symbolName}
    according to key->value relation in paraDict, if there is a {code} showed in
    word, and paraDict declares '{code}':'000001', then the content of {code} will
    be replaced to 000001.

    Parameters
    ----------
    paragraph : Object
        The python-docx paragraph object.
    paraDict : dict
        A python dict used to declare which symbol should be replaced and how should
        it be replaced.

    Returns
    -------
    None
    """
    text = paragraph.text.strip()
    replacePara = [i for i in paraDict.keys() if text.find(i) != -1]
    if len(replacePara) != 0:
        for i in replacePara:
            if type(paraDict[i]) == type(''):
                replaceTo = paraDict[i]
            elif hasattr(paraDict[i], 'strftime'):
                replaceTo = str(paraDict[i].year) + '年' + str(paraDict[i].month) + '月' + str(paraDict[i].day) + '日'
            else:
                replaceTo = str(paraDict[i])
            text = text.replace(i, replaceTo)
        text = text.replace('{', '').replace('}', '')
        stack = []
        for line in paragraph.runs:
            if len(stack) != 0 and line.text.find('}') == -1:
                stack.append(line.text)
                line.text = ''
            elif len(stack) != 0 and line.text.find('}') != -1:
                endIndex = line.text.index('}')
                stack.append(line.text[:endIndex])
                line.text = line.text[endIndex + 1:]
                paraToBeReplaced = '{' + ''.join(stack) + '}'
                line.text = paraDict[paraToBeReplaced] + line.text
                stack = []
                text = text[len(paraDict[paraToBeReplaced]):]

            elif line.text.find('{') == -1:
                text = text[len(line.text):]
            elif line.text.find('}') != -1 and len(stack) == 0:
                startIndex = line.text.index('{')
                endIndex = line.text.index('}')
                paraToBeReplaced = line.text[startIndex:endIndex + 1]
                line.text = line.text[:startIndex] + paraDict[paraToBeReplaced] + line.text[endIndex + 1:]
                text = text[len(paraDict[paraToBeReplaced]):]
            else:
                content = line.text.split('{')
                line.text = content[0]
                stack.append(content[-1])

def formatWordWithTemplate(originFilePath:str,targetFilePath:str,paraDict:dict):
    """
    This function will iterate across the whole docx file and check for each paragraph
    and table, if it find any symbol like {symbolName}, it will replace it into the
    value declared by paraDict.

    Parameters
    ----------
    originFilePath : str
        The docx template file whose content you want to check and replace.
    targetFilePath : str
        The path you want to save the after-replacement docx file.
    paraDict : dict
        The key->value pairs that declare what the symbols should be replaced to.
        The key of this dict should be string type and like '{symbolName}', and
        the value of this dict should be string type.

    Returns
    -------
    None
    """
    document = Document(originFilePath)
    for num, paragraph in enumerate(document.paragraphs):
        replaceParagraphContent(paragraph,paraDict)
    for table in document.tables:
        for row in range(len(table.rows)):
            for col in range(len(table.columns)):
                for num,paragraph in enumerate(table.cell(row,col).paragraphs):
                    replaceParagraphContent(paragraph,paraDict)
    document.save(targetFilePath)

def formatTableWithTemplate(targetFilePath:str,tableIndex:int,dfInput:pd.DataFrame):
    """
    This function will change the table in docx file into the given dataframe.
    This change is inplace. A new file will be generated and replace the original
    docx file.

    Parameters
    ----------
    targetFilePath : str
        The docx file path that you want to change one of its table into the given
        dataframe.
    tableIndex : int
        The table index that showed which table you want to change.
    dfInput : pd.DataFrame
        The dataframe that the original table should be changed to.

    Returns
    -------
    None
    """
    document = Document(targetFilePath)
    table = document.tables[tableIndex]
    if len(table.rows)-2 > dfInput.shape[0]:
        [row._element.getparent().remove(row._element) for row in table.rows[1:(len(table.rows)-2-dfInput.shape[0]+1)]]
    else:
        originFinalRow = table.rows[-1]
        [table.add_row() for i in range(2+dfInput.shape[0]-len(table.rows))]
        newFinalRow = table.rows[-1]
        for col in range(len(table.columns)):
            for num,paragraph in enumerate(table.cell(newFinalRow,col).paragraphs):
                paragraph.text = table.cell(originFinalRow,col).paragraphs[num]
    for row in range(dfInput.shape[0]):
        for col in range(dfInput.shape[1]):
            for num,paragraph in enumerate(table.cell(row+1,col).paragraphs):
                try:
                    value = dfInput.iloc[row,col]
                    if isinstance(value,str):
                        paragraph.text = value
                    elif isinstance(value,float):
                        paragraph.text = format(round(value,2),",")
                    else:
                        paragraph.text = str(value)
                except Exception as e:
                    print(e)
    document.save(targetFilePath)

#<wordTool>
#</wordTool>






