#!/usr/bin/python
#coding = utf-8
import sys,os,importlib
from RiskQuantLib.Tool.codeBuilderTool import pythonScriptBuilder


def clearInstrumentPath(targetProjectPath = ''):
    # add path to pathObj
    if targetProjectPath == '':
        pathObjPath = sys.path[0]+os.sep+'RiskQuantLib'+os.sep+'Build'+os.sep+'pathObj.py'
    else:
        pathObjPath = targetProjectPath + os.sep + 'Build' + os.sep + 'pathObj.py'
    # write file path
    with open(pathObjPath, 'r') as f:
        content = f.read()

    if content.find('#-<pathDictBegin>') == -1 or content.find('#-<pathDictEnd>') == -1:
        print("Source file must have a #-<Begin> and #-<End> tag to be built")
        exit(-1)

    former = content.split('#-<pathDictBegin>')[0]
    ender = content.split('#-<pathDictEnd>')[-1]

    newContent = former + '#-<pathDictBegin>\n    #-<pathDictEnd>' + ender
    with open(pathObjPath, 'w') as f:
        f.truncate()  # 清空文件内容
        f.write(newContent.strip(' ').strip('\t\n'))

    # write list file path
    with open(pathObjPath, 'r') as f:
        content = f.read()

    if content.find('#-<listPathDictBegin>') == -1 or content.find('#-<listPathDictEnd>') == -1:
        print("Source file must have a #-<Begin> and #-<End> tag to be built")
        exit(-1)

    former = content.split('#-<listPathDictBegin>')[0]
    ender = content.split('#-<listPathDictEnd>')[-1]

    newContent = former + '#-<listPathDictBegin>\n    #-<listPathDictEnd>' + ender
    with open(pathObjPath, 'w') as f:
        f.truncate()  # 清空文件内容
        f.write(newContent.strip(' ').strip('\t\n'))

    # write class import path
    with open(pathObjPath, 'r') as f:
        content = f.read()

    if content.find('#-<classPathDictBegin>') == -1 or content.find('#-<classPathDictEnd>') == -1:
        print("Source file must have a #-<Begin> and #-<End> tag to be built")
        exit(-1)

    former = content.split('#-<classPathDictBegin>')[0]
    ender = content.split('#-<classPathDictEnd>')[-1]

    newContent = former + '#-<classPathDictBegin>\n    #-<classPathDictEnd>' + ender
    with open(pathObjPath, 'w') as f:
        f.truncate()  # 清空文件内容
        f.write(newContent.strip(' ').strip('\t\n'))

    # write class name path
    with open(pathObjPath, 'r') as f:
        content = f.read()

    if content.find('#-<classNameDictBegin>') == -1 or content.find('#-<classNameDictEnd>') == -1:
        print("Source file must have a #-<Begin> and #-<End> tag to be built")
        exit(-1)

    former = content.split('#-<classNameDictBegin>')[0]
    ender = content.split('#-<classNameDictEnd>')[-1]

    newContent = former + '#-<classNameDictBegin>\n    #-<classNameDictEnd>' + ender
    with open(pathObjPath, 'w') as f:
        f.truncate()  # 清空文件内容
        f.write(newContent.strip(' ').strip('\t\n'))

def buildInstrumentPath(instrumentNameString,parentRQLClassName = '',targetProjectPath = ''):
    # create a dictionary path to hold new python script. this new dictionary should be besides its parent RQL class script
    c_instrumentNameString = instrumentNameString[0].capitalize()+instrumentNameString[1:]
    if targetProjectPath == '':
        targetProjectPath = sys.path[0]+os.sep+'RiskQuantLib'
    else:
        pass

    # find security path
    if parentRQLClassName == '':
        filePath = targetProjectPath+os.sep+c_instrumentNameString+os.sep+instrumentNameString+'.py'
        setFilePath = targetProjectPath+os.sep+'Set'+os.sep+c_instrumentNameString+os.sep+instrumentNameString+'.py'
        listFilePath = targetProjectPath+os.sep+c_instrumentNameString+'List'+os.sep+instrumentNameString+'List'+'.py'
        setListFilePath = targetProjectPath+os.sep+'Set'+os.sep+c_instrumentNameString+'List'+os.sep+instrumentNameString+'List'+'.py'
    elif type(parentRQLClassName)==type(''):
        import RiskQuantLib.Build.pathObj as POJ
        importlib.reload(POJ)
        RQLpathObj = POJ.pathObj()
        parentSetFilePath = "".join([i+os.sep for i in RQLpathObj.pathDict[parentRQLClassName].split(os.sep)[:-1]]).strip(os.sep)
        parentFilePath = "".join([i+os.sep for i in parentSetFilePath.split(os.sep)[1:]]).strip(os.sep)
        filePath = targetProjectPath+os.sep + parentFilePath + os.sep+c_instrumentNameString+os.sep+instrumentNameString+'.py'
        setFilePath = targetProjectPath+os.sep + parentSetFilePath + os.sep+c_instrumentNameString+os.sep+instrumentNameString+'.py'

        parentListSetFilePath = "".join([i+os.sep for i in RQLpathObj.listPathDict[parentRQLClassName].split(os.sep)[:-1]]).strip(os.sep)
        parentListFilePath = "".join([i+os.sep for i in parentListSetFilePath.split(os.sep)[1:]]).strip(os.sep)
        listFilePath = targetProjectPath+os.sep + parentListFilePath + os.sep+c_instrumentNameString+'List'+os.sep+instrumentNameString+'List'+'.py'
        setListFilePath = targetProjectPath+os.sep + parentListSetFilePath + os.sep+c_instrumentNameString+'List'+os.sep+instrumentNameString+'List'+'.py'
        del RQLpathObj
    else:
        import RiskQuantLib.Build.pathObj as POJ
        importlib.reload(POJ)
        RQLpathObj = POJ.pathObj()
        parentSetFilePath = "".join([i + os.sep for i in RQLpathObj.pathDict[parentRQLClassName[0]].split(os.sep)[:-1]]).strip(os.sep)
        parentFilePath = "".join([i + os.sep for i in parentSetFilePath.split(os.sep)[1:]]).strip(os.sep)
        filePath = targetProjectPath + os.sep + parentFilePath + os.sep + c_instrumentNameString + os.sep + instrumentNameString + '.py'
        setFilePath = targetProjectPath + os.sep + parentSetFilePath + os.sep + c_instrumentNameString + os.sep + instrumentNameString + '.py'

        parentListSetFilePath = "".join([i + os.sep for i in RQLpathObj.listPathDict[parentRQLClassName[0]].split(os.sep)[:-1]]).strip(os.sep)
        parentListFilePath = "".join([i + os.sep for i in parentListSetFilePath.split(os.sep)[1:]]).strip(os.sep)
        listFilePath = targetProjectPath + os.sep + parentListFilePath + os.sep + c_instrumentNameString +'List'+ os.sep + instrumentNameString +'List'+ '.py'
        setListFilePath = targetProjectPath + os.sep + parentListSetFilePath + os.sep + c_instrumentNameString +'List'+ os.sep + instrumentNameString +'List'+ '.py'

        del RQLpathObj

    # create security base dictionary
    filePathWD = "".join([i+os.sep for i in filePath.split(os.sep)[:-1]]).strip(os.sep)
    setFilePathWD = "".join([i+os.sep for i in setFilePath.split(os.sep)[:-1]]).strip(os.sep)
    listFilePathWD = "".join([i+os.sep for i in listFilePath.split(os.sep)[:-1]]).strip(os.sep)
    setListFilePathWD = "".join([i+os.sep for i in setListFilePath.split(os.sep)[:-1]]).strip(os.sep)
    if os.path.exists(filePathWD):
        with open(filePathWD + os.sep + '__init__.py', 'w+') as f:
            f.truncate()  # 清空文件内容
    else:
        os.mkdir(filePathWD)
        with open(filePathWD+os.sep+'__init__.py', 'w+') as f:
            f.truncate()  # 清空文件内容

    if os.path.exists(setFilePathWD):
        with open(setFilePathWD + os.sep + '__init__.py', 'w+') as f:
            f.truncate()  # 清空文件内容
    else:
        os.mkdir(setFilePathWD)
        with open(setFilePathWD+os.sep+'__init__.py', 'w+') as f:
            f.truncate()  # 清空文件内容

    if os.path.exists(listFilePathWD):
        with open(listFilePathWD + os.sep + '__init__.py', 'w+') as f:
            f.truncate()  # 清空文件内容
    else:
        os.mkdir(listFilePathWD)
        with open(listFilePathWD+os.sep+'__init__.py', 'w+') as f:
            f.truncate()  # 清空文件内容

    if os.path.exists(setListFilePathWD):
        with open(setListFilePathWD + os.sep + '__init__.py', 'w+') as f:
            f.truncate()  # 清空文件内容
    else:
        os.mkdir(setListFilePathWD)
        with open(setListFilePathWD+os.sep+'__init__.py', 'w+') as f:
            f.truncate()  # 清空文件内容

    # add path to pathObj
    pathObjPath = targetProjectPath+os.sep+'Build'+os.sep+'pathObj.py'
    # write file path
    with open(pathObjPath, 'r') as f:
        content = f.read()

    if content.find('#-<pathDictBegin>') == -1 or content.find('#-<pathDictEnd>') == -1:
        print("Source file must have a #-<Begin> and #-<End> tag to be built")
        exit(-1)

    former = content.split('#-<pathDictBegin>')[0]
    middle = content.split('#-<pathDictBegin>')[-1].split('#-<pathDictEnd>')[0]
    ender = content.split('#-<pathDictEnd>')[-1]

    add_code = r'''    pathDict["'''+c_instrumentNameString+'''"] = "'''+setFilePath.split('RiskQuantLib')[-1].strip(os.sep).replace(os.sep,'" + os.sep + "')+'''"'''
    newContent = former + '#-<pathDictBegin>\n' + middle.strip('\t').strip('    ') + add_code + '\n    #-<pathDictEnd>' + ender
    with open(pathObjPath, 'w') as f:
        f.truncate()  # 清空文件内容
        f.write(newContent.strip(' ').strip('\t\n'))

    # write list file path
    with open(pathObjPath, 'r') as f:
        content = f.read()

    if content.find('#-<listPathDictBegin>') == -1 or content.find('#-<listPathDictEnd>') == -1:
        print("Source file must have a #-<Begin> and #-<End> tag to be built")
        exit(-1)

    former = content.split('#-<listPathDictBegin>')[0]
    middle = content.split('#-<listPathDictBegin>')[-1].split('#-<listPathDictEnd>')[0]
    ender = content.split('#-<listPathDictEnd>')[-1]

    add_code = r'''    listPathDict["''' + c_instrumentNameString + '''"] = "''' + setListFilePath.split('RiskQuantLib')[-1].strip(os.sep).replace(os.sep, '" + os.sep + "') + '''"'''
    newContent = former + '#-<listPathDictBegin>\n' + middle.strip('\t').strip('    ') +add_code + '\n    #-<listPathDictEnd>' + ender
    with open(pathObjPath, 'w') as f:
        f.truncate()  # 清空文件内容
        f.write(newContent.strip(' ').strip('\t\n'))

    # write class import path
    with open(pathObjPath, 'r') as f:
        content = f.read()

    if content.find('#-<classPathDictBegin>') == -1 or content.find('#-<classPathDictEnd>') == -1:
        print("Source file must have a #-<Begin> and #-<End> tag to be built")
        exit(-1)

    former = content.split('#-<classPathDictBegin>')[0]
    middle = content.split('#-<classPathDictBegin>')[-1].split('#-<classPathDictEnd>')[0]
    ender = content.split('#-<classPathDictEnd>')[-1]

    add_code = r'''    classPathDict["'''+c_instrumentNameString+'''"] = "RiskQuantLib.'''+filePath.split('RiskQuantLib')[-1].strip(os.sep).replace(os.sep,'.').strip('.py')+'''"'''
    newContent = former + '#-<classPathDictBegin>\n' + middle.strip('\t').strip('    ') +add_code + '\n    #-<classPathDictEnd>' + ender
    with open(pathObjPath, 'w') as f:
        f.truncate()  # 清空文件内容
        f.write(newContent.strip(' ').strip('\t\n'))

    # write class name path
    with open(pathObjPath, 'r') as f:
        content = f.read()

    if content.find('#-<classNameDictBegin>') == -1 or content.find('#-<classNameDictEnd>') == -1:
        print("Source file must have a #-<Begin> and #-<End> tag to be built")
        exit(-1)

    former = content.split('#-<classNameDictBegin>')[0]
    middle = content.split('#-<classNameDictBegin>')[-1].split('#-<classNameDictEnd>')[0]
    ender = content.split('#-<classNameDictEnd>')[-1]

    add_code = r'''    classNameDict["'''+c_instrumentNameString+'''"] = "'''+instrumentNameString+'''"'''
    newContent = former + '#-<classNameDictBegin>\n' + middle.strip('\t').strip('    ') +add_code + '\n    #-<classNameDictEnd>' + ender
    with open(pathObjPath, 'w') as f:
        f.truncate()  # 清空文件内容
        f.write(newContent.strip(' ').strip('\t\n'))

    return [filePath,setFilePath,listFilePath,setListFilePath]


def buildInstrumentObj(instrumentNameString, parentRQLClassName = '', parentQuantLibClassName = '', libraryName = '', defaultInstrumentType = ''):
    c_instrumentNameString = instrumentNameString[0].capitalize() + instrumentNameString[1:]
    import RiskQuantLib.Build.pathObj as POJ
    importlib.reload(POJ)
    RQLpathObj = POJ.pathObj()


    psb = pythonScriptBuilder()
    psb.setTitle()
    
    # parent class list
    parentClassList = []
    
    # import
    if libraryName=='':
        pass
    elif type(libraryName)==type(''):
        psb.setImport(libraryName)
    else:
        [psb.setImport(i) for i in libraryName]

    if parentRQLClassName=='':
        pass
    elif type(parentRQLClassName)==type(''):
        classPath = RQLpathObj.classPathDict[parentRQLClassName]
        className = RQLpathObj.classNameDict[parentRQLClassName]
        psb.setImport(classPath,'',True,className)
        if className not in parentClassList:
            parentClassList.append(className)
    else:
        for i in parentRQLClassName:
            classPath = RQLpathObj.classPathDict[i]
            className = RQLpathObj.classNameDict[i]
            psb.setImport(classPath, '', True, className)
            if className not in parentClassList:
                parentClassList.append(className)

    if parentQuantLibClassName=='':
        pass
    elif type(parentQuantLibClassName) == type(''):
        psb.setImport('QuantLib','',True,parentQuantLibClassName)
        parentClassList.append(parentQuantLibClassName)
    else:
        [psb.setImport('QuantLib','',True,i) for i in parentQuantLibClassName]
        parentClassList += parentQuantLibClassName

    # import set module
    setPath = 'RiskQuantLib.'+ RQLpathObj.pathDict[c_instrumentNameString].replace(os.sep,'.').strip('.py')
    psb.setImport(setPath,'',True,'set'+c_instrumentNameString)
    parentClassList.append('set'+c_instrumentNameString)

    # class start
    psb.startClass(instrumentNameString,parentClassList)
    
    # __init__
    if defaultInstrumentType == '':
        psb.startFunction(r'__init__',["codeString","nameString","securityTypeString = '"+instrumentNameString.capitalize()+"'"])
    else:
        psb.startFunction(r'__init__', ["codeString", "nameString","securityTypeString = '" + defaultInstrumentType + "'"])

    if parentRQLClassName=='':
        psb.code.add_line('self.code = codeString')
        psb.code.add_line('self.name = nameString')
        psb.code.add_line('self.securityType = securityTypeString')
    elif type(parentRQLClassName)==type(''):
        className = RQLpathObj.classNameDict[parentRQLClassName]
        psb.code.add_line(className+ '.__init__(self,codeString,nameString,securityTypeString)')
    else:
        for i in parentRQLClassName:
            className = RQLpathObj.classNameDict[i]
            psb.code.add_line(className+'.__init__(self,codeString,nameString,securityTypeString)')
    psb.endFunction()

    # init_pricing_module
    if parentQuantLibClassName=='':
        pass
    elif type(parentQuantLibClassName) == type(''):
        psb.startFunction('iniPricingModule','*args')
        psb.code.add_line(parentQuantLibClassName+r'.__init__(self,*args)')
        psb.endFunction()
    else:
        for i in parentQuantLibClassName:
            psb.startFunction('iniPricingModule_'+i, '*args')
            psb.code.add_line(i + r'.__init__(self,*args)')
            psb.endFunction()

    psb.endClass()
    return psb


def buildInstrumentSet(instrumentNameString, parentRQLClassName=''):
    c_instrumentNameString = instrumentNameString[0].capitalize() + instrumentNameString[1:]
    import RiskQuantLib.Build.pathObj as POJ
    importlib.reload(POJ)
    RQLpathObj = POJ.pathObj()

    psb = pythonScriptBuilder()
    psb.setTitle()

    # parent class list
    parentClassList = []

    psb.setImport('numpy','np')
    psb.setImport('pandas', 'pd')

    if parentRQLClassName == '':
        pass
    elif type(parentRQLClassName) == type(''):
        classPath = 'RiskQuantLib.' + RQLpathObj.pathDict[parentRQLClassName].replace(os.sep, '.').strip('.py')
        className = 'set' + RQLpathObj.classNameDict[parentRQLClassName][0].capitalize() + RQLpathObj.classNameDict[parentRQLClassName][1:]
        psb.setImport(classPath, '', True, className)
        if className not in parentClassList:
            parentClassList.append(className)
    else:
        for i in parentRQLClassName:
            classPath = 'RiskQuantLib.'+RQLpathObj.pathDict[i].replace(os.sep,'.').strip('.py')
            className = 'set'+RQLpathObj.classNameDict[i][0].capitalize()+RQLpathObj.classNameDict[i][1:]
            psb.setImport(classPath, '', True, className)
            if className not in parentClassList:
                parentClassList.append(className)

    psb.startClass('set'+c_instrumentNameString,parentClassList)
    psb.endClass()
    psb.code.add_line(r'''    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here''')
    psb.code.add_line(r'''    #-<Begin>''')
    psb.code.add_line(r'''    #-<End>''')
    return psb

def buildInstrumentList(instrumentNameString, parentRQLClassName='',securityType = ''):
    c_instrumentNameString = instrumentNameString[0].capitalize() + instrumentNameString[1:]
    import RiskQuantLib.Build.pathObj as POJ
    importlib.reload(POJ)
    RQLpathObj = POJ.pathObj()

    psb = pythonScriptBuilder()
    psb.setTitle()

    # parent class list
    parentClassList = []

    psb.setImport('numpy','np')
    psb.setImport('pandas', 'pd')
    psb.setImport(RQLpathObj.classPathDict[c_instrumentNameString],'',True,RQLpathObj.classNameDict[c_instrumentNameString])

    if parentRQLClassName == '':
        psb.setImport('RiskQuantLib.Operation.listBaseOperation','',True,'listBase')
        if 'listBase' not in parentClassList:
            parentClassList.append('listBase')
    elif type(parentRQLClassName) == type(''):
        classPath = 'RiskQuantLib.' + "".join([i+'.' for i in RQLpathObj.listPathDict[parentRQLClassName].split(os.sep)[1:]]).strip('.py.')
        className = RQLpathObj.classNameDict[parentRQLClassName] + 'List'
        psb.setImport(classPath, '', True, className)
        if className not in parentClassList:
            parentClassList.append(className)
    else:
        for i in parentRQLClassName:
            classPath = 'RiskQuantLib.' + "".join([i + '.' for i in RQLpathObj.listPathDict[i].split(os.sep)[1:]]).strip('.py.')
            className = RQLpathObj.classNameDict[i] + 'List'
            psb.setImport(classPath, '', True, className)
            if className not in parentClassList:
                parentClassList.append(className)

    setPath = 'RiskQuantLib.' + RQLpathObj.listPathDict[c_instrumentNameString].replace(os.sep,'.').strip('.py')
    psb.setImport(setPath,'',True,'set'+c_instrumentNameString+'List')
    parentClassList.append('set'+c_instrumentNameString+'List')
    psb.startClass(instrumentNameString+'List',parentClassList)

    if parentRQLClassName == '':# add self.__init__ to independent class
        psb.startFunction('__init__')
        psb.code.add_line('self.all = []')
        psb.endFunction()
    elif type(parentRQLClassName) == type(''):
        psb.startFunction('__init__')
        psb.code.add_line("super("+instrumentNameString+"List,self).__init__()")
        psb.code.add_line("self.listType = '"+securityType+" List'")
        psb.endFunction()
    else:
        psb.startFunction('__init__')
        psb.code.add_line("super("+instrumentNameString+"List,self).__init__()")
        psb.code.add_line("self.listType = '"+securityType+" List'")
        psb.endFunction()

    psb.startFunction('add'+c_instrumentNameString,['securityCode','securityName','securityTypeString = "'+securityType+'"'])
    psb.code.add_line(r'''securitySeries = '''+r'''self.all+['''+RQLpathObj.classNameDict[c_instrumentNameString]+'''(securityCode,securityName,securityTypeString)]''')
    psb.code.add_line(r'''self.setAll(securitySeries)''')
    psb.endFunction()
    psb.startFunction('add'+c_instrumentNameString+'Series',['securityCodeSeries','securityNameSeries','securityTypeString = "'+securityType+'"'])
    psb.code.add_line(r'''securitySeries = ['''+RQLpathObj.classNameDict[c_instrumentNameString]+r'''(i,j,securityTypeString) for i,j in zip(securityCodeSeries,securityNameSeries)]''')
    psb.code.add_line(r'''self.setAll(self.all + securitySeries)''')
    psb.endFunction()
    psb.endClass()
    return psb

def buildInstrumentListSet(instrumentNameString, parentRQLClassName=''):
    c_instrumentNameString = instrumentNameString[0].capitalize() + instrumentNameString[1:]
    import RiskQuantLib.Build.pathObj as POJ
    importlib.reload(POJ)
    RQLpathObj = POJ.pathObj()

    psb = pythonScriptBuilder()
    psb.setTitle()

    # parent class list
    parentClassList = []

    psb.setImport('numpy','np')
    psb.setImport('pandas', 'pd')

    if parentRQLClassName == '':
        pass
    elif type(parentRQLClassName) == type(''):
        classPath = 'RiskQuantLib.' + RQLpathObj.listPathDict[parentRQLClassName].replace(os.sep,'.').strip('.py')
        className = 'set'+RQLpathObj.classNameDict[parentRQLClassName][0].capitalize()+RQLpathObj.classNameDict[parentRQLClassName][1:] + 'List'
        psb.setImport(classPath, '', True, className)
        if className not in parentClassList:
            parentClassList.append(className)
    else:
        for i in parentRQLClassName:
            classPath = 'RiskQuantLib.' + RQLpathObj.listPathDict[i].replace(os.sep, '.').strip('.py')
            className = 'set' + RQLpathObj.classNameDict[i][0].capitalize() + RQLpathObj.classNameDict[i][1:] + 'List'
            psb.setImport(classPath, '', True, className)
            if className not in parentClassList:
                parentClassList.append(className)
    psb.startClass('set'+c_instrumentNameString+'List',parentClassList)
    psb.endClass()
    psb.code.add_line(r'''    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here''')
    psb.code.add_line(r'''    #-<Begin>''')
    psb.code.add_line(r'''    #-<End>''')
    return psb

def commitBuildInstrument(sourcePSBObj,targetPath):
    if os.path.exists(targetPath):
        pass
    else:
        sourcePSBObj.writeToFile(targetPath)


def buildInstrument(instrumentNameString, parentRQLClassName = '', parentQuantLibClassName = '', libraryName = '', defaultInstrumentType = '',targetProjectPath=''):
    pathList = buildInstrumentPath(instrumentNameString, parentRQLClassName=parentRQLClassName)
    IO = buildInstrumentObj(instrumentNameString, parentRQLClassName, parentQuantLibClassName, libraryName, defaultInstrumentType)
    IOS = buildInstrumentSet(instrumentNameString, parentRQLClassName)
    IL = buildInstrumentList(instrumentNameString, parentRQLClassName,defaultInstrumentType)
    ILS = buildInstrumentListSet(instrumentNameString, parentRQLClassName)
    if targetProjectPath == '':
        [commitBuildInstrument(source, path) for path, source in zip(pathList, [IO, IOS, IL, ILS])]
    else:
        [commitBuildInstrument(source,targetProjectPath + os.sep + path.split('RiskQuantLib')[-1]) for path,source in zip(pathList,[IO,IOS,IL,ILS])]

    return None










