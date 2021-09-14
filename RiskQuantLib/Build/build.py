#!/usr/bin/python
#coding = utf-8
import os

def buildAttr(filePath:str, targetProjectPath:str = ''):
    """
    buildAttr(filePath, targetProjectPath = '') is a function to automatically build attributes to instrument classes.

    Parameters
    ----------
    filePath : str
        The excel file path that tells RiskQuantLib how to build attributes,
        including the name of attributes, which instrument it belongs to,
        and value type of attributes.
    targetProjectPath : str
        The RiskQuantLib project path where you want to build attributes.
        You can leave this parameter empty to build attributes in this project.
        Or specify a path to build attributes to another RiskQuantLib project.

    Returns
    -------
    None


    """
    import pandas as pd
    df = pd.read_excel(filePath)
    df.fillna('Any',inplace=True)
    # Build Attr Type
    buildPropertyType(list(set([i for i in df['AttrType'] if i not in ['Any','Number','String','Series']])),targetProjectPath=targetProjectPath)
    # Build Attr
    from RiskQuantLib.Build.propertyList import propertyList
    plist = propertyList()
    plist.addProperty(df['AttrName'],df['SecurityType'])
    plist.setPropertyType(df['AttrName'],df['SecurityType'],df['AttrType'])
    plist.buildFunction()
    plist.buildTargetSourceFile()
    if targetProjectPath == '':
        RiskQuantLibDictionary = os.path.abspath(__file__).split('RiskQuantLib' + os.sep + 'Build')[0]
        source_path = os.path.abspath(RiskQuantLibDictionary) + os.sep + r'RiskQuantLib'
        plist.commit(source_path)
    else:
        plist.commit(targetProjectPath)
    print("Build Attr Finished")

def clearAttr(targetProjectPath:str = ''):
    """
    clearAttr(targetProjectPath = '') is a function to automatically clear all attributes of all instrument classes.
    Once attributes are cleared, you can not use them directly any more. The setAttr function will also be removed.

    Parameters
    ----------
    targetProjectPath : str
        The RiskQuantLib project path where you want to clear attributes.
        You can leave this parameter empty to clear attributes in this project.
        Or specify a path to clear attributes to another RiskQuantLib project.

    Returns
    -------
    None
    """
    from RiskQuantLib.Build.buildFuction import clearBuiltFunction
    from RiskQuantLib.Build.propertyObj import propertyObj
    tmpObj = propertyObj('Tmp')
    if targetProjectPath == '':
        RiskQuantLibDictionary = os.path.abspath(__file__).split('RiskQuantLib' + os.sep + 'Build')[0]
        source_path = os.path.abspath(RiskQuantLibDictionary) + os.sep + r'RiskQuantLib'
    else:
        source_path = targetProjectPath
    targetSourcePathList = [source_path + os.sep + i for i in tmpObj.pathDict.values()] + [source_path + os.sep + j for j in tmpObj.listPathDict.values()]
    [clearBuiltFunction(i) for i in targetSourcePathList]
    from RiskQuantLib.Build.buildPropertyType import clearPropertyTypePath
    clearPropertyTypePath(targetProjectPath)
    print("Clear Attr Finished")

def buildInstrument(filePath:str, targetProjectPath:str = ''):
    """
    buildInstrument(filePath, targetProjectPath = '') is a function to automatically build instrument classes.
    If instrument already exists, it will skip this instrument.
    Any instrument that doesn't exist in excel file won't be built and added into RiskQuantLib path,
    regardless of whether it used to exist in target project.

    Parameters
    ----------
    filePath : str
        The excel file path that tells RiskQuantLib how to build instruments,
        including the name of instruments, which instrument class it inherits from,
        which QuantLib class it inherits from, and instrument default type string.
    targetProjectPath : str
        The RiskQuantLib project path where you want to build instruments.
        You can leave this parameter empty to build instruments in this project.
        Or specify a path to build instruments to another RiskQuantLib project.

    Returns
    -------
    None
    """
    import pandas as pd
    df = pd.read_excel(filePath)
    df.fillna('',inplace=True)
    from RiskQuantLib.Build.instrumentList import instrumentList
    ilist = instrumentList()
    ilist.addInstrument(df['InstrumentName'])
    ilist.setParentRQLClassName(df['InstrumentName'],df['ParentRQLClassName'])
    ilist.setParentQuantLibClassName(df['InstrumentName'],df['ParentQuantLibClassName'])
    ilist.setLibraryName(df['InstrumentName'],df['LibraryName'])
    ilist.setDefaultInstrumentType(df['InstrumentName'],df['DefaultInstrumentType'])
    ilist.commit(targetProjectPath)
    print("Build Instrument Finished")

def buildPropertyType(propertyNameList : list, targetProjectPath:str = ''):
    """
    buildPropertyType(propertyNameList : list, targetProjectPath = '') is a function to automatically build propertyType classes.
    If propertyType already exists, it will skip this propertyType.
    Any propertyType that doesn't exist in excel file won't be built and added into RiskQuantLib path,
    regardless of whether it used to exist in target project.

    Parameters
    ----------
    propertyNameList : list
        A list contains the types of variables you may use.
    targetProjectPath : str
        The RiskQuantLib project path where you want to build propertyTypes.
        You can leave this parameter empty to build propertyTypes in this project.
        Or specify a path to build propertyTypes to another RiskQuantLib project.

    Returns
    -------
    None
    """
    from RiskQuantLib.Build.propertyTypeList import propertyTypeList
    ptlist = propertyTypeList()
    ptlist.addPropertyType(propertyNameList)
    ptlist.commit(targetProjectPath)
    print("Build PropertyType Finished")

def clearInstrumentPath(targetProjectPath:str = ''):
    """
    clearInstrumentPath(targetProjectPath:str = '') is a function to automatically clear instrument path.
    This function won't clear instrument class files. It only remove instrument path from RiskQuantLib project,
    so that you can't use these instruments class directly any more.

    Parameters
    ----------
    targetProjectPath : str
        The RiskQuantLib project path where you want to clear instrument paths.
        You can leave this parameter empty to clear instrument paths in this project.
        Or specify a path to clear instrument paths of another RiskQuantLib project.

    Returns
    -------
    None
    """
    from RiskQuantLib.Build.buildInstrument import clearInstrumentPath
    from RiskQuantLib.Build.buildShortcut import clearShortcut
    clearInstrumentPath(targetProjectPath)
    clearShortcut(targetProjectPath)
    print('Clear Instrument Path Finished')











