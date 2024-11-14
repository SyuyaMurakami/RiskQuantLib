#!/usr/bin/python
# coding = utf-8
import re
import numpy as np
import pandas as pd

class controller(object):

    @staticmethod
    def findDeclareTag(sourceCode:str):
        """
        Find the line start with #-|, return a list whose element is each line string.
        """
        declarePosition = [i.regs[0] for i in re.finditer(r'''^#-\|.*:.*$''', sourceCode, flags=re.MULTILINE)]
        content = [sourceCode[start:end] for start, end in declarePosition]
        return content

    @staticmethod
    def parseDeclareTagByGivenString(content:str, splitLineBy=r',', splitWordBy=r'@'):
        """
        Split content by given string, and split each element of line by given string.
        Return the list whose element is the first part of word of each line, and the list
        whose element if the last part of word of each line.
        """
        lineSplit = [i.strip(' ') for i in content.split(splitLineBy)]
        wordSplit = [i.split(splitWordBy) for i in lineSplit]
        contentBeforeWordSplit = [i[0].strip(' ') for i in wordSplit]
        contentAfterWordSplit = [splitWordBy.join(i[1:]).strip(' ') if len(i)>=2 else '' for i in wordSplit]
        return contentBeforeWordSplit, contentAfterWordSplit

    @staticmethod
    def parseDeclareTagAsSeries(content:str, tagName:str, defaultTagName:str = ''):
        """
        Transform each declaration line about instrument into Series, which contains instrument build information.
        """
        tagNameAdj = defaultTagName if tagName == '' else tagName
        controlCommandIndex, controlCommandValue = controller.parseDeclareTagByGivenString(content)
        controlCommandIndexRoot, controlCommandIndexRest = controller.parseDeclareTagByGivenString(",".join(controlCommandIndex), splitWordBy='.')
        controlCommandSeries = pd.Series(controlCommandValue,index=pd.MultiIndex.from_arrays([controlCommandIndexRoot,controlCommandIndexRest],names=['Root','Rest'])).groupby(level=[0,1]).apply(lambda x:",".join(x.where(x != '', np.nan).dropna().drop_duplicates()).strip(',')).rename(tagNameAdj)
        return controlCommandSeries

    @staticmethod
    def parseDeclareTagAsDF(controlSyntaxList:list, instrumentColDefault=['InstrumentName','ParentRQLClassName','ParentQuantLibClassName','LibraryName','DefaultInstrumentType'],attributeColDefault=['SecurityType','AttrName','AttrType']):
        """
        Given the list whose element is line string of declaration content, transfer instrument declaration and attribute declaration into series, and
        merge all series into a build dataframe. Return the buildInstrument dataframe and buildAttr dataframe.
        """
        declareTagNameOrigin = [i.split(':')[0].replace('#-|','').strip(' ') for i in controlSyntaxList]
        declareTagContentOrigin = [i.split(':')[-1].strip(' ') for i in controlSyntaxList]
        declareTagMerged = pd.Series(declareTagContentOrigin,index=declareTagNameOrigin,dtype=str).groupby(level=0,group_keys=False).apply(lambda x:",".join(x))
        declareTagName = declareTagMerged.index.to_list()
        declareTagContent = declareTagMerged.values.tolist()
        declareTagNameType, declareTagNameSubType = controller.parseDeclareTagByGivenString(",".join(declareTagName),splitWordBy='-')
        declareTagDefaultCol = ['ParentRQLClassName' if tnt=='instrument' else 'AttrType' if tnt == 'attribute' else tn for tnt,tn in zip(declareTagNameType,declareTagName)]
        declareTagParse = {tn:(controller.parseDeclareTagAsSeries(tc,tnst,tdc)) for tn,tc,tnst,tdc in zip(declareTagName,declareTagContent,declareTagNameSubType,declareTagDefaultCol)}
        declareTagNameTypeDict = dict(zip(declareTagName,declareTagNameType))

        instrumentInfo = [declareTagParse[i] for i in declareTagParse if declareTagNameTypeDict[i] == 'instrument']
        attributeInfo = [declareTagParse[i] for i in declareTagParse if declareTagNameTypeDict[i] == 'attribute']
        otherInfo = [declareTagParse[i] for i in declareTagParse if declareTagNameTypeDict[i] not in {'instrument','attribute'}]

        buildInstrumentTotal = pd.concat(instrumentInfo,axis=1).replace('',np.nan) if len(instrumentInfo) != 0 else pd.DataFrame(dtype=str, columns=instrumentColDefault)
        buildInstrumentTotal['InstrumentName'] = buildInstrumentTotal.index.get_level_values(0)
        buildInstrumentDefault = buildInstrumentTotal.T.reindex(instrumentColDefault).T
        buildInstrumentOption = buildInstrumentTotal[[i for i in buildInstrumentTotal.columns if i not in instrumentColDefault]]
        buildInstrument = pd.concat([buildInstrumentDefault,buildInstrumentOption],axis=1)

        buildAttributeTotal = pd.concat(attributeInfo, axis=1).replace('', np.nan) if len(attributeInfo) != 0 else pd.DataFrame(dtype=str, columns=attributeColDefault, index=pd.MultiIndex(levels=[[],[]],codes=[[],[]]))
        buildAttributeTotal['SecurityType'] = buildAttributeTotal.index.get_level_values(0)
        buildAttributeTotal['AttrName'] = buildAttributeTotal.index.get_level_values(1)
        buildAttributeDefault = buildAttributeTotal.T.reindex(attributeColDefault).T
        buildAttributeOption = buildAttributeTotal[[i for i in buildAttributeTotal.columns if i not in attributeColDefault]]
        buildAttr = pd.concat([buildAttributeDefault, buildAttributeOption], axis=1)

        buildOtherTotal = pd.concat(otherInfo, axis=1).replace('', np.nan) if len(otherInfo) != 0 else pd.DataFrame(dtype=str)
        return buildInstrument, buildAttr, buildOtherTotal

    @staticmethod
    def linkController(linkToBuilder, controlSyntaxList:list):
        """
        Given original builder, create a new builder, this new builder will copy all build path of original builder, but use
        additional build information declared by declaration content to modify itself. Then the new builder will trigger a
        build action. This function will return the new builder as a mimic one of original builder.
        """
        from RiskQuantLib.Build.builder import validateBuilder,builder
        [linkToBuilder.mimicBuilder.bindContent("", bindType=bt, persist=False) for bt in linkToBuilder.mimicBuilder.bindType] if hasattr(linkToBuilder,'mimicBuilder') and isinstance(linkToBuilder.mimicBuilder,builder) and (linkToBuilder.buildFromPath, linkToBuilder.projectPath, linkToBuilder.targetPath, linkToBuilder.templatePath) == (linkToBuilder.mimicBuilder.buildFromPath, linkToBuilder.mimicBuilder.projectPath, linkToBuilder.mimicBuilder.targetPath, linkToBuilder.mimicBuilder.templatePath) else None
        mimicBuilder = validateBuilder()
        mimicBuilder.projectPath = linkToBuilder.projectPath
        mimicBuilder.targetPath = linkToBuilder.targetPath
        mimicBuilder.buildFromPath = linkToBuilder.buildFromPath
        mimicBuilder.templatePath = linkToBuilder.templatePath
        mimicBuilder.instrumentTree = linkToBuilder.instrumentTree.copy()
        mimicBuilder.propertyTree = linkToBuilder.propertyTree.copy()
        buildInstrument, buildAttr, buildOther = controller.parseDeclareTagAsDF(controlSyntaxList)
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
        mimicBuilder.delRender()
        linkToBuilder.mimicBuilder = mimicBuilder
