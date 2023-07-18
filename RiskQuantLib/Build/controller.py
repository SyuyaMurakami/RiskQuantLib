#!/usr/bin/python
# coding = utf-8
import re
import numpy as np
import pandas as pd

class controller(object):

    @staticmethod
    def findDeclareTag(sourceCode:str):
        declarePosition = [i.regs[0] for i in re.finditer(r'''^#-\|.*:.*$''', sourceCode, flags=re.MULTILINE)]
        content = [sourceCode[start:end] for start, end in declarePosition]
        return content

    @staticmethod
    def parseDeclareTagByGivenString(content:str, splitLineBy=r',', splitWordBy=r'@'):
        lineSplit = [i.strip(' ') for i in content.split(splitLineBy)]
        wordSplit = [i.split(splitWordBy) for i in lineSplit]
        contentBeforeWordSplit = [i[0].strip(' ') for i in wordSplit]
        contentAfterWordSplit = [splitWordBy.join(i[1:]).strip(' ') if len(i)>=2 else '' for i in wordSplit]
        return contentBeforeWordSplit, contentAfterWordSplit

    @staticmethod
    def parseDeclareTagInstrument(content:str, tagName:str):
        tagNameAdj = 'ParentRQLClassName' if tagName == '' else tagName
        instrumentName, instrumentDeclare = controller.parseDeclareTagByGivenString(content)
        instrumentSeries = pd.Series(instrumentDeclare,index=instrumentName).groupby(level=0).apply(lambda x:",".join(x.replace('',np.nan).dropna().drop_duplicates()).strip(',')).rename(tagNameAdj)
        return instrumentSeries

    @staticmethod
    def parseDeclareTagAttribute(content:str):
        attribute, propertyType = controller.parseDeclareTagByGivenString(content)
        instrumentName, attributeName = controller.parseDeclareTagByGivenString(",".join(attribute),splitWordBy='.')
        attributeDF = pd.DataFrame([instrumentName,attributeName,propertyType],index=['SecurityType','AttrName','AttrType'])
        return attributeDF.T.drop_duplicates(subset=['SecurityType','AttrName'])

    @staticmethod
    def parseDeclareContent(controlSyntaxList:list):
        """
        Find the line of control comment, split whole content by control comment line. Parse the
        target file and tag name for every control comment. Finally, return a dict whose key is target
        file and value is (tag,content) pair.
        """
        declareTagNameOrigin = [i.split(':')[0].replace('#-|','').strip(' ') for i in controlSyntaxList]
        declareTagContentOrigin = [i.split(':')[-1].strip(' ') for i in controlSyntaxList]
        declareTagMerged = pd.Series(declareTagContentOrigin,index=declareTagNameOrigin).groupby(level=0).apply(lambda x:",".join(x))
        declareTagName = declareTagMerged.index.to_list()
        declareTagContent = declareTagMerged.values.tolist()
        declareTagNameType, declareTagNameSubType = controller.parseDeclareTagByGivenString(",".join(declareTagName),splitWordBy='-')
        declareTagParse = {tn:(controller.parseDeclareTagInstrument(tc,tnst) if tnt=='instrument' else controller.parseDeclareTagAttribute(tc) if tnt=='attribute' else None) for tn,tc,tnt,tnst in zip(declareTagName,declareTagContent,declareTagNameType,declareTagNameSubType)}
        declareTagNameTypeDict = dict(zip(declareTagName,declareTagNameType))
        buildInstrument = pd.concat([declareTagParse[i] for i in declareTagParse if declareTagNameTypeDict[i]=='instrument'],axis=1).replace('',np.nan)
        buildInstrument['InstrumentName'] = buildInstrument.index
        buildInstrument = buildInstrument[['InstrumentName']+buildInstrument.columns.to_list()[:-1]]
        buildAttr = declareTagParse['attribute']
        return buildInstrument, buildAttr

    @staticmethod
    def linkController(linkToBuilder, controlSyntaxList:list):
        from RiskQuantLib.Build.builder import validateBuilder
        mimicBuilder = validateBuilder()
        mimicBuilder.projectPath = linkToBuilder.projectPath
        mimicBuilder.targetPath = linkToBuilder.targetPath
        mimicBuilder.buildFromPath = linkToBuilder.buildFromPath
        mimicBuilder.templatePath = linkToBuilder.templatePath
        mimicBuilder.instrumentTree = linkToBuilder.instrumentTree.copy()
        mimicBuilder.propertyTree = linkToBuilder.propertyTree.copy()
        buildInstrument, buildAttr = controller.parseDeclareContent(controlSyntaxList)
        buildInstrument = buildInstrument.replace('',np.nan).dropna(subset=['InstrumentName']).fillna('')
        buildInstrument = buildInstrument.reindex(buildInstrument[['InstrumentName']].drop_duplicates(keep='last').index)
        buildAttr = buildAttr.replace('',np.nan).dropna(subset=['AttrName']).fillna('')
        buildAttr = buildAttr.reindex(buildAttr[['SecurityType','AttrName']].drop_duplicates(keep='last').index)
        dfName = [buildInstrument, buildInstrument, buildInstrument, buildInstrument, buildInstrument, buildAttr, buildAttr, buildAttr]
        dfCol = ['InstrumentName', 'ParentRQLClassName', 'ParentQuantLibClassName', 'LibraryName', 'DefaultInstrumentType', 'SecurityType', 'AttrName', 'AttrType']
        dfNanInstrument = ['' for _ in range(buildInstrument.shape[0])]
        dfNanAttr = ['' for _ in range(buildAttr.shape[0])]
        args = tuple([i[j].to_list() if j in i else dfNanInstrument if i.shape[0]==len(dfNanInstrument) else dfNanAttr if i.shape[0]==len(dfNanAttr) else ['' for k in range(i.shape[0])] for i,j in zip(dfName,dfCol)])
        mimicBuilder.validateTree(*args)
        super(validateBuilder, mimicBuilder).buildProject(dumpCache=False)
        return mimicBuilder
