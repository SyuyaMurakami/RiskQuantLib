#!/usr/bin/python
#coding = utf-8
import sys,os,importlib
from RiskQuantLib.Tool.codeBuilderTool import pythonScriptBuilder

def convertPathToImportPath(pathString):
    listPathDict = pathString.split(os.sep)
    className = listPathDict[-1].split('.py')[0]
    return 'RiskQuantLib.'+"".join([i+'.' for i in listPathDict[1:-1]])+className


def clearShortcut(targetProjectPath=''):
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
        f.truncate()  # 清空文件内容
        f.write(newContent.strip(' ').strip('\t\n'))

def commitShortcut(psb,targetProjectPath):
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
        f.truncate()  # 清空文件内容
        f.write(newContent.strip(' ').strip('\t\n'))
    # print()

def buildShortcut(instrumentNameList):
    c_instrumentNameList = [i[0].capitalize()+i[1:] for i in instrumentNameList]
    psb = pythonScriptBuilder()
    import RiskQuantLib.Build.pathObj as POJ
    importlib.reload(POJ)
    RQLpathObj = POJ.pathObj()
    pathWaitedToBeAdded = [convertPathToImportPath(RQLpathObj.listPathDict[i]) for i in c_instrumentNameList]
    [psb.setImport(classPath,'',True,className+'List,'+className) for classPath,className in zip(pathWaitedToBeAdded,instrumentNameList)]
    return psb










