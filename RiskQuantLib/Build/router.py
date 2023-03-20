#!/usr/bin/python
# coding = utf-8
import os,re
class router(object):

    @staticmethod
    def formatTag(tagName:str):
        tagStart = '#<'+tagName+'>'
        tagEnd = '#</'+tagName+'>'
        return tagStart, tagEnd

    @staticmethod
    def stripTag(content:str):
        """
        Delete the row of tag
        """
        return re.sub(r'''#<.*>''', '', content, flags=re.MULTILINE)

    @staticmethod
    def indent(num:int = 0):
        return ''.join(['    ' for i in range(num)])

    @staticmethod
    def readContent(pythonSourceFilePath:str, encoding = 'utf-8'):
        with open(pythonSourceFilePath, 'r', encoding=encoding) as f:
            content = f.read()
        return content

    @staticmethod
    def contentSplit(content:str, tagStart:str, tagEnd:str):
        """
        Split content by given tagStart and tagEnd, return content
        before tagStart and content after tagEnd
        """
        former = content.split(tagStart)[0].strip(' ').strip('\n\t')
        ender = content.split(tagEnd)[-1].strip('\n')
        return former, ender

    @staticmethod
    def writeContent(content:str, pythonSourceFilePath:str, encoding = 'utf-8'):
        with open(pythonSourceFilePath, 'w', encoding=encoding) as f:
            f.truncate()  # clear all contents of file
            f.write(content.strip(' ').strip('\t\n'))

    @staticmethod
    def findIndentOfLine(content:str, startTextOfLine:str):
        """
        Find the blank before given text.
        """
        tagLine = re.findall(r'''^([ \f\r\t\v]*)'''+startTextOfLine, content, flags=re.MULTILINE)
        indentOfLine = tagLine[0] if len(tagLine)!=0 else ''
        return indentOfLine.lstrip('\n')

    @staticmethod
    def insertToContent(sourceCode:str, tagName:str, content:str):
        """
        Insert some content to given tag position
        """
        tagStart, tagEnd = router.formatTag(tagName)
        if content.find(tagStart) == -1 or content.find(tagEnd) == -1:
            return content
        else:
            indent = router.findIndentOfLine(content,tagStart)
            indentedSourceCode = re.sub(r'''^''',indent,sourceCode,flags = re.MULTILINE)
            former, ender = router.contentSplit(content, tagStart, tagEnd)
            newContent = former + '\n' + indent + tagStart + '\n' + indentedSourceCode + '\n' + indent + tagEnd + '\n' + ender
            return newContent

    @staticmethod
    def injectToContent(content:str, **kwargs):
        """
        Insert several contents into related tag. Contents will be between tagStart and tagEnd.
        kwargs is a dict whose key is tag name and value is content to be inserted.
        """
        for tagName in kwargs.keys():
            tagStart, tagEnd = router.formatTag(tagName)
            if content.find(tagStart) == -1 or content.find(tagEnd) == -1:
                continue
            else:
                indent = router.findIndentOfLine(content,tagStart)
                strippedSourceCode = router.stripTag(kwargs[tagName])
                indentedSourceCode = re.sub(r'''^''',indent,strippedSourceCode,flags = re.MULTILINE)
                former, ender = router.contentSplit(content, tagStart, tagEnd)
                content = former + '\n' + indent + tagStart + '\n' + indentedSourceCode + '\n' + indent + tagEnd + '\n' + ender
        return content

    @staticmethod
    def persistToContent(content:str, **kwargs):
        """
        Insert several contents right before related tag. Contents will be before tagStart.
        kwargs is a dict whose key is tag name and value is content to be inserted.
        """
        for tagName in kwargs.keys():
            tagStart, tagEnd = router.formatTag(tagName)
            if content.find(tagStart) == -1 or content.find(tagEnd) == -1:
                continue
            else:
                indent = router.findIndentOfLine(content,tagStart)
                strippedSourceCode = router.stripTag(kwargs[tagName])
                indentedSourceCode = re.sub(r'''^''',indent,strippedSourceCode,flags = re.MULTILINE)
                former, ender = router.contentSplit(content, tagStart, tagEnd)
                content = former + '\n' + indentedSourceCode + '\n' + indent + tagStart + '\n' + indent + tagEnd + '\n' + ender
        return content

    @staticmethod
    def insertToFile(sourceCode:str, tagName:str, pythonSourceFilePath:str):
        """
        Read a .py file and insert some code into tag position.
        """
        content = router.readContent(pythonSourceFilePath)
        newContent = router.insertToContent(sourceCode, tagName, content)
        router.writeContent(newContent,pythonSourceFilePath)

    @staticmethod
    def injectToFile(pythonSourceFilePath:str, **kwargs):
        """
        Read a .py file and insert several contents into related tag position.
        """
        content = router.readContent(pythonSourceFilePath)
        newContent = router.injectToContent(content,**kwargs)
        router.writeContent(newContent, pythonSourceFilePath)

    @staticmethod
    def persistToFile(pythonSourceFilePath:str, **kwargs):
        """
        Read a .py file and insert several contents before related tag position.
        """
        content = router.readContent(pythonSourceFilePath)
        newContent = router.persistToContent(content,**kwargs)
        router.writeContent(newContent, pythonSourceFilePath)

    @staticmethod
    def validateInjectTag(injectTag:str, injectPath:str, syntacticSugarPathMap:dict = {}):
        """
        Parse a single tag information. If user does not specify @, use file name as tag name.
        Then convert dirA.dirB.dirC into dirA/dirB/dirC. Return target file path and target
        tag name.
        """
        targetPath = injectTag.split('@')[0]
        if injectTag.find('@')!=-1:
            targetTag = injectTag.split('@')[-1]
        else:
            targetTag = targetPath.split('.')[-1]
        if targetPath.find('.') == -1 and targetPath in syntacticSugarPathMap:
            filePath = injectPath + os.sep + syntacticSugarPathMap[targetPath]
        else:
            filePath = injectPath + os.sep + targetPath.replace('.', os.sep) + '.py'
        if os.path.exists(filePath):
            return filePath, targetTag
        else:
            return '', targetTag

    @staticmethod
    def convertInjectTagToFilePath(injectTag:str, injectPath:str, syntacticSugarPathMap:dict = {}):
        """
        Parse a line of tag information. Split the line by comma, parse every sub-string into
        (filePath,tagName) and reform them into a list.
        """
        tagList = [i.replace(' ','') for i in injectTag.split(',')]
        pathList = [router.validateInjectTag(i, injectPath, syntacticSugarPathMap) for i in tagList]
        return pathList

    @staticmethod
    def parseInjectTarget(sourceCode:str, injectPath:str, syntacticSugarPathMap:dict = {}):
        """
        Find the line of control comment, split whole content by control comment line. Parse the
        target file and tag name for every control comment. Finally, return a dict whose key is target
        file and value is (tag,content) pair.
        """
        import pandas as pd
        tagPosition = [i.regs[0] for i in re.finditer(r'''^#->.*$''', sourceCode, flags=re.MULTILINE)]
        tagStart = [i[1] for i in tagPosition]
        tagEnd = [i[0] for i in tagPosition[1:]] + [len(sourceCode)]
        tag = [sourceCode[start:end] for start, end in tagPosition]
        content = [sourceCode[start:end] for start, end in zip(tagStart, tagEnd)]
        targetPathAndTargetTag = [router.convertInjectTagToFilePath(i.replace('#->',''), injectPath, syntacticSugarPathMap) for i in tag]
        injectInfoList = [pd.DataFrame([(j[0],j[1],contentId) for j in pathTag]) for contentId,pathTag in enumerate(targetPathAndTargetTag)]
        injectInfo = pd.concat(injectInfoList).rename(columns = {0:'path',1:'tag',2:'contentId'}) if len(injectInfoList)!=0 else pd.DataFrame(columns = ['path','tag','contentId'])
        injectInfo = injectInfo[injectInfo['path']!='']
        injectContentAfterMerge = injectInfo.groupby(by=['path','tag'], group_keys=False).apply(lambda x:"".join([content[id] for id in x['contentId']]))
        if injectContentAfterMerge.empty:
            return {}
        else:
            injectContentAfterMerge = injectContentAfterMerge.rename('mergedContent').reset_index()
            injectContentDict = injectContentAfterMerge.groupby(by='path').apply(lambda x:dict(zip(x['tag'],x['mergedContent']))).to_dict()
            return injectContentDict













