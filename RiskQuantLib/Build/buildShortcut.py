#!/usr/bin/python
#coding = utf-8
import sys,os,importlib
from RiskQuantLib.Tool.codeBuilderTool import pythonScriptBuilder

def convertPathToImportPath(pathString:str):
    """
    convertPathToImportPath(pathString:str) is a function to convert file path to class import path.

    Parameters
    ----------
    pathString : str
        The relative path of RiskQuantLib files. This path must be relative to RiskQuantLib.__init__.py

    Returns
    -------
    classImportPath : str
        The import path of RiskQuantLib files.
    """
    listPathDict = pathString.split(os.sep)
    className = listPathDict[-1].split('.py')[0]
    classImportPath = 'RiskQuantLib.'+"".join([i+'.' for i in listPathDict[1:-1]])+className
    return classImportPath


def clearShortcut(targetProjectPath:str=''):
    """
    clearShortcut(targetProjectPath:str='') is a function to clear all registration of class paths.
    To simplify usage of class, a shortcut will be inserted to RiskQuantLib.module for every auto-built instrument class.
    After calling this function, these shortcuts will be removed, but the original source files still exist.

    Parameters
    ----------
    targetProjectPath :str
        The RiskQuantLib project path where you want to remove all instrument class shortcuts.

    Returns
    -------
    None
    """
    projectPath = os.path.abspath(__file__).split('RiskQuantLib'+os.sep+'Build'+os.sep+'buildShortcut.py')[0]
    if targetProjectPath == '':
        path = projectPath + os.sep + 'RiskQuantLib' + os.sep + 'Module.py'
    else:
        path = targetProjectPath + os.sep + 'RiskQuantLib' + os.sep + 'Module.py'
    # write shortcut path
    with open(path, 'r') as f:
        content = f.read()

    if content.find('#-<moduleImportBegin>') == -1 or content.find('#-<moduleImportEnd>') == -1:
        print("Source file must have a #-<Begin> and #-<End> tag to be built")
        exit(-1)

    former = content.split('#-<moduleImportBegin>')[0]
    ender = content.split('#-<moduleImportEnd>')[-1]
    newContent = former + '#-<moduleImportBegin>\n#-<moduleImportEnd>' + ender
    with open(path, 'w') as f:
        f.truncate()  # clear all contents
        f.write(newContent.strip(' ').strip('\t\n'))

def commitShortcut(psb:pythonScriptBuilder,targetProjectPath:str):
    """
    commitShortcut(psb:pythonScriptBuilder,targetProjectPath:str) is a function to commit the change
    of shortcut files. It makes modification to RiskQuantLib.module.

    Parameters
    ----------
    psb : pythonScriptBuilder
        A pythonScriptBuilder object, contains the source code of shortcuts map relation.
    targetProjectPath : str
        The RiskQuantLib project path where you want to commit shortcut change.

    Returns
    -------
    None
    """
    projectPath = os.path.abspath(__file__).split('RiskQuantLib'+os.sep+'Build'+os.sep+'buildShortcut.py')[0]
    if targetProjectPath == '':
        path = projectPath + os.sep + 'RiskQuantLib' + os.sep + 'Module.py'
    else:
        path = targetProjectPath + os.sep + 'RiskQuantLib' + os.sep + 'Module.py'
    # write shortcut path
    with open(path, 'r') as f:
        content = f.read()

    if content.find('#-<moduleImportBegin>') == -1 or content.find('#-<moduleImportEnd>') == -1:
        print("Source file must have a #-<Begin> and #-<End> tag to be built")
        exit(-1)

    former = content.split('#-<moduleImportBegin>')[0]
    ender = content.split('#-<moduleImportEnd>')[-1]
    newContent = former + '#-<moduleImportBegin>\n'+psb.importLibrary+'#-<moduleImportEnd>' + ender
    with open(path, 'w') as f:
        f.truncate()  # clear all contents
        f.write(newContent.strip(' ').strip('\t\n'))

def buildShortcut(instrumentNameList:list):
    """
    buildShortcut(instrumentNameList:list) is the function to generate source code of shortcut map.
    It joins class name to class import path, making it easy to use instrument class.

    Parameters
    ----------
    instrumentNameList : list
        The instruments whose shortcut you want to add to RiskQuantLib.module.

    Returns
    -------
    psb : pythonScriptBuilder
        A pythonScriptBuilder object contains map relation from instrument name to import path.
    """
    c_instrumentNameList = [i[0].capitalize()+i[1:] for i in instrumentNameList]
    psb = pythonScriptBuilder()
    import RiskQuantLib.Build.pathObj as POJ
    importlib.reload(POJ)
    RQLpathObj = POJ.pathObj()
    pathWaitedToBeAdded = [convertPathToImportPath(RQLpathObj.listPathDict[i]) for i in c_instrumentNameList]
    [psb.setImport(classPath,'',True,className+'List,'+className) for classPath,className in zip(pathWaitedToBeAdded,instrumentNameList)]
    return psb










