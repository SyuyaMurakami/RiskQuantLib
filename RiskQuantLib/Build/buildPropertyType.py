#!/usr/bin/python
#coding = utf-8
import sys,os,importlib
from RiskQuantLib.Tool.codeBuilderTool import pythonScriptBuilder


def clearPropertyTypePath(targetProjectPath:str = ''):
    """
    clearPropertyTypePath(targetProjectPath:str = '') is a function to clear all propertyType path registration
    of RiskQuantLib.
    This function won't delete propertyType class files, it only remove path registration,
    so that you can not use it directly through RiskQuantLib.Module,
    or build new propertyType classes inherited from it.
    This function won't clear default propertyType registration.

    Parameters
    ----------
    targetProjectPath : str
        The location of RiskQuantLib project where you want to clear all propertyType registration.

    Returns
    -------
    None
    """
    # add path to pathObj
    if targetProjectPath == '':
        pathObjPath = sys.path[0]+os.sep+'RiskQuantLib'+os.sep+'Build'+os.sep+'pathObj.py'
    else:
        pathObjPath = targetProjectPath + os.sep + 'Build' + os.sep + 'pathObj.py'
    # write file path
    with open(pathObjPath, 'r') as f:
        content = f.read()

    if content.find('#-<attributeTypeDictBegin>') == -1 or content.find('#-<attributeTypeDictEnd>') == -1:
        print("Source file must have a #-<Begin> and #-<End> tag to be built")
        exit(-1)

    former = content.split('#-<attributeTypeDictBegin>')[0]
    ender = content.split('#-<attributeTypeDictEnd>')[-1]

    newContent = former + '#-<attributeTypeDictBegin>\n    #-<attributeTypeDictEnd>' + ender
    with open(pathObjPath, 'w') as f:
        f.truncate()  # clear all contents
        f.write(newContent.strip(' ').strip('\t\n'))


def buildPropertyTypePath(propertyTypeNameString:str,targetProjectPath:str = ''):
    """
    buildPropertyTypePath(propertyTypeNameString:str,parentRQLClassName:str = '',targetProjectPath:str = '')
    is a function to create new propertyType class file paths. The created path will be in the path:
    RiskQuantLib.Property. If path already exists, it won't be overwritten.

    Parameters
    ----------
    propertyTypeNameString : str
        The propertyType name that you want to create attribute type class by.
    targetProjectPath : str
        The location of RiskQuantLib project where you want to create propertyType class.

    Returns
    -------
    filePath : str
    """
    # create a dictionary path to hold new python script.
    c_propertyTypeNameString = propertyTypeNameString[0].capitalize()+propertyTypeNameString[1:]
    if targetProjectPath == '':
        targetProjectPath = sys.path[0]+os.sep+'RiskQuantLib'
    else:
        pass

    # find type class path
    filePath = targetProjectPath+os.sep+'Property'+os.sep+c_propertyTypeNameString+os.sep+propertyTypeNameString+'.py'

    # create type class base dictionary
    filePathWD = "".join([i+os.sep for i in filePath.split(os.sep)[:-1]]).strip(os.sep)

    if os.path.exists(filePathWD):
        with open(filePathWD + os.sep + '__init__.py', 'w+') as f:
            f.truncate()  # clear all contents
    else:
        os.mkdir(filePathWD)
        with open(filePathWD+os.sep+'__init__.py', 'w+') as f:
            f.truncate()  # clear all contents

    # add type path to pathObj
    pathObjPath = targetProjectPath+os.sep+'Build'+os.sep+'pathObj.py'
    # write file path
    with open(pathObjPath, 'r') as f:
        content = f.read()

    if content.find('#-<attributeTypeDictBegin>') == -1 or content.find('#-<attributeTypeDictEnd>') == -1:
        print("Source file must have a #-<Begin> and #-<End> tag to be built")
        exit(-1)

    former = content.split('#-<attributeTypeDictBegin>')[0]
    middle = content.split('#-<attributeTypeDictBegin>')[-1].split('#-<attributeTypeDictEnd>')[0]
    ender = content.split('#-<attributeTypeDictEnd>')[-1]

    add_code = r'''    attributeTypeDict["'''+c_propertyTypeNameString+'''"] = "'''+filePath.split('RiskQuantLib')[-1].strip(os.sep).replace(os.sep,'" + os.sep + "')+'''"'''
    newContent = former + '#-<attributeTypeDictBegin>\n' + middle.strip('\t').strip('    ') + add_code + '\n    #-<attributeTypeDictEnd>' + ender
    with open(pathObjPath, 'w') as f:
        f.truncate()  # clear all contents
        f.write(newContent.strip(' ').strip('\t\n'))

    return filePath


def buildPropertyTypeObj(propertyTypeNameString:str, libraryName:str = ''):
    """
    buildPropertyTypeObj(propertyTypeNameString:str, parentRQLClassName:str = '',
    parentQuantLibClassName:str = '', libraryName:str = '', defaultPropertyTypeType:str = '')
    is a function to generate source code of new propertyType file, given propertyType name and which class it
    inherited from.

    Parameters
    ----------
    propertyTypeNameString : str
        The propertyType name you want to create python source file by.
    libraryName : str or list
        Other library you want to use in new propertyType class file.

    Returns
    -------
    psb : pythonScriptBuilder
        A pythonScriptBuilder object.

    """
    psb = pythonScriptBuilder()
    psb.setTitle()
    
    # import
    if libraryName=='':
        pass
    elif type(libraryName)==type(''):
        psb.setImport(libraryName)
    else:
        [psb.setImport(i) for i in libraryName]

    psb.setImport("RiskQuantLib.Property.base",'',True,"base")

    # class start
    psb.startClass(propertyTypeNameString,"base")
    
    # __init__
    psb.startFunction(r'__init__',"value")
    psb.code.add_line('super('+propertyTypeNameString+',self).__init__(value)')
    psb.endFunction()
    psb.endClass()
    return psb

def commitBuildPropertyType(sourcePSBObj:pythonScriptBuilder,targetPath:str):
    """
    commitBuildPropertyType(sourcePSBObj:pythonScriptBuilder,targetPath:str)
    is a function to commit generated source code change to target files.
    If the file already exists, it will skip.

    Parameters
    ----------
    sourcePSBObj : pythonScriptBuilder
        The pythonScriptBuilder object, which contains source code.
    targetPath : str
        The file path where you want to overwrite contents with new contents.

    Returns
    -------
    None
    """
    if os.path.exists(targetPath):
        pass
    else:
        sourcePSBObj.writeToFile(targetPath)


def buildPropertyType(propertyTypeNameString:str, libraryName:str = '', targetProjectPath:str=''):
    """
    buildPropertyType(propertyTypeNameString:str, libraryName:str = '', targetProjectPath:str='')
    is the entrance of build propertyTypes.
    It call function to generate source code of propertyType class. Then it commit change to target files.

    Parameters
    ----------
    propertyTypeNameString : str
        The name you want to create new propertyType by.
    libraryName : str
        Other library you want to include in your source file.
    targetProjectPath : str
        The RiskQuantLib project path where you want to build propertyTypes. A ''(blank string) will
        specify this project.

    Returns
    -------
    None

    """
    path = buildPropertyTypePath(propertyTypeNameString, targetProjectPath=targetProjectPath)
    TO = buildPropertyTypeObj(propertyTypeNameString, libraryName)
    if targetProjectPath == '':
        commitBuildPropertyType(TO, path)
    else:
        commitBuildPropertyType(TO,targetProjectPath + os.sep+'RiskQuantLib'+os.sep + path.split('RiskQuantLib')[-1])
    return None










