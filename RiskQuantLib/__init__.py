#!/usr/bin/python
#coding = utf-8
import sys


def newProject():
    """
    newProject() is a function to create a new RiskQuantLib project.

    Use terminal command 'newRQL' to use this function.
    The terminal command 'newRQL' accept a parameter 'targetPathString', which is the path that you want to build RiskQuantLib project.
    If there is already a RiskQuantLib project in target path, it will be deleted and replaced by a new project.

    Parameters
    ----------
    targetPathString : str
        A terminal command parameter, specify the path where you want to build a new project.

    Returns
    -------
    None

    """
    import sys,os,shutil
    import pandas as pd
    RiskQuantLibDictionary = os.path.abspath(__file__).split('RiskQuantLib'+os.sep+'__init__')[0]

    source_path = os.path.abspath(RiskQuantLibDictionary)+os.sep+r'RiskQuantLib'
    # target_path = os.getcwd()
    target_path = sys.argv[1]+os.sep+r'RiskQuantLib'

    if not os.path.exists(target_path):
        # if there is no target path, create one
        os.makedirs(target_path)

    if os.path.exists(source_path):
        # if there is already a path, clear it
        shutil.rmtree(target_path)

    shutil.copytree(source_path, target_path)

    # create excel file for build
    df_attr = pd.DataFrame(index = ['SecurityType','AttrName','AttrType']).T
    df_instrument = pd.DataFrame(index = ['InstrumentName','ParentRQLClassName','ParentQuantLibClassName','LibraryName','DefaultInstrumentType']).T
    df_attr.to_excel(sys.argv[1]+os.sep+'Build_Attr.xlsx',index=0)
    df_instrument.to_excel(sys.argv[1]+os.sep+'Build_Instrument.xlsx',index=0)

    # create build script
    from RiskQuantLib.Tool.codeBuilderTool import pythonScriptBuilder,codeBuilder
    PYB = pythonScriptBuilder()
    PYB.setTitle()
    PYB.setImport('os')
    PYB.setImport('sys')
    PYB.setImport('time')
    PYB.setImport('RiskQuantLib.Build.build','BA',True,'buildAttr')
    PYB.setImport('RiskQuantLib.Build.build', 'BI', True, 'buildInstrument')
    PYB.code = codeBuilder(indent=0)
    PYB.code.add_line('path = sys.path[0]')
    PYB.code.add_line('BI(path + os.sep + "Build_Instrument.xlsx")')
    PYB.code.add_line('time.sleep(2)')
    PYB.code.add_line('BA(path + os.sep + "Build_Attr.xlsx")')

    PYB.writeToFile(sys.argv[1]+os.sep+'build.py')

    # create program start point
    PYB = pythonScriptBuilder()
    PYB.setTitle()
    PYB.setImport('os')
    PYB.setImport('sys')
    PYB.setImport('RiskQuantLib.Module','',True,'*')
    PYB.code = codeBuilder(indent=0)
    PYB.code.add_line('path = sys.path[0]')
    PYB.code.add_line('print("Write Your Code Here : "+path+os.sep+"main.py")')
    PYB.writeToFile(sys.argv[1]+os.sep+'main.py')

    print('New RiskQuantLib Project Created!')


def packProject():
    """
    packProject() is a function to pack a RiskQuantLib project into '.zip' file.

    Use terminal command 'pkgRQL' to use this function.
    The terminal command 'pkgRQL' accept a parameter 'targetPathString',
    which is the RiskQuantLib project path that you want to package.
    It doesn't need to have a dictionary named 'RiskQuantLib' to be packaged.

    Parameters
    ----------
    targetPathString : str
        A terminal command parameter, specify the RiskQuantLib project path which you want to package.

    Returns
    -------
    None
    """
    projectPath = sys.argv[1]
    try:
        name = sys.argv[2]
    except:
        name = ''
    import os, shutil
    if name=='':
        name = projectPath.split(os.sep)[-1]
    else:
        nameList = name.split('.')
        if len(nameList)>1:
            name = "".join(nameList[0:-1])
        else:
            name = nameList[0]
    parentProjectPath = os.path.dirname(projectPath)
    shutil.make_archive(parentProjectPath+os.sep+name,"zip",projectPath)
    print('RiskQuantLib Project Packaged!')

def checkAndCreateTemplatePath():
    import os
    RiskQuantLibDictionary = os.path.abspath(__file__).split('RiskQuantLib'+os.sep+'__init__')[0]
    source_path = os.path.abspath(RiskQuantLibDictionary) + os.sep + r'RQLTemplate'
    if os.path.exists(source_path):
        pass
    else:
        os.makedirs(source_path)
    return source_path

def addProjectTemplate():
    """
    addProjectTemplate() is a function to add a RiskQuantLib project '.zip' file to library.

    Use terminal command 'addRQL' to use this function.
    The terminal command 'addRQL' accept a parameter 'targetPathString',
    which is the RiskQuantLib project '.zip' file path that you want to add to library.
    It have to be a '.zip' file to be added to library.

    Parameters
    ----------
    targetPathString : str
        A terminal command parameter, specify the RiskQuantLib project '.zip' file path which you want to add to library.

    Returns
    -------
    None
    """
    import os, shutil
    projectPackPath = os.path.splitext(sys.argv[1])[0]
    try:
        name = sys.argv[2]
    except:
        name = ''

    if name=='':
        name = projectPackPath.split(os.sep)[-1]
    else:
        nameList = name.split('.')
        if len(nameList)>1:
            name = "".join(nameList[0:-1])
        else:
            name = nameList[0]
    source_path = checkAndCreateTemplatePath()
    parentProjectPath = os.path.dirname(projectPackPath)
    shutil.copy(parentProjectPath+os.sep+name+'.zip',source_path+os.sep+name+'.zip')
    os.remove(parentProjectPath+os.sep+name+'.zip')
    print('RiskQuantLib Project Template added!')

def saveProject():
    """
    saveProject() is a function to save a RiskQuantLib project and add it to library.

    Use terminal command 'saveRQL' to use this function.
    The terminal command 'saveRQL' accept a parameter 'targetPathString',
    which is the RiskQuantLib project path that you want to save,
    and an optional parameter 'projectName',
    which is the name you want to give to this project.
    After calling this function, a '.zip' file will be created in RiskQuantLib project dictionary,
    and this project will be stored as a template.

    Parameters
    ----------
    targetPathString : str
        A terminal command parameter, specify the RiskQuantLib project path which you want to save as template.
    projectName : str
        A terminal command parameter, specify the name you want to save this project as.

    Returns
    -------
    None
    """
    packProject()
    addProjectTemplate()

def unpackProject():
    """
    unpackProject() is a function to unpack a RiskQuantLib project from library and use it again.

    Use terminal command 'tplRQL' to use this function.
    The terminal command 'tplRQL' accept a parameter 'projectName',
    which is the project name you want to unpack from library.
    and a parameter 'targetPathString',
    which is the path where you want to unpack RiskQuantLib project,
    After calling this function, the content of existing RiskQuantLib project will be unpacked to the location you choose,
    and you can start a project at the fundation of this unpakced project.

    Parameters
    ----------
    projectName : str
        A terminal command parameter, specify the project name you want to unpack from library.

    targetPathString : str
        A terminal command parameter, specify the path where you want to unpack RiskQuantLib project.

    Returns
    -------
    None
    """
    import sys,os,shutil
    RiskQuantLibDictionary = os.path.abspath(__file__).split('RiskQuantLib'+os.sep+'__init__')[0]
    source_path = os.path.abspath(RiskQuantLibDictionary)+os.sep+r'RQLTemplate'
    projectName = sys.argv[1]
    target_path = sys.argv[2]
    shutil.unpack_archive(source_path+os.sep+projectName+'.zip',target_path,"zip")
    if os.path.exists(target_path+os.sep+projectName+'.zip'):
        os.remove(target_path+os.sep+projectName+'.zip')
    print('RiskQuantLib Project Template '+projectName+' Unpack Finished!')

def listProjectTemplate():
    """
    listProjectTemplate() is a function to show all RiskQuantLib projects from library.

    Use terminal command 'listRQL' to use this function.

    Returns
    -------
    None
    """
    import os
    source_path = checkAndCreateTemplatePath()
    projectNameList = [i.replace('.zip','') for i in os.listdir(source_path)]
    hints = "Show All RiskQuantLib Template Projects:"
    print(hints,'\n',"".join(['-' for i in range(len(hints))]))
    [print(index,"->",name) for index,name in enumerate(projectNameList)]

def delProjectTemplate():
    """
    delProject() is a function to delete a RiskQuantLib project from library.

    Use terminal command 'delRQL' to use this function.
    The terminal command 'delRQL' accept a parameter 'projectName',
    which is the project name you want to delete from library.
    After calling this function, the existing RiskQuantLib project will be removed from library.

    Parameters
    ----------
    projectName : str
        A terminal command parameter, specify the project name you want to delete from library.

    Returns
    -------
    None
    """
    import os
    source_path = checkAndCreateTemplatePath()
    projectNameList = [i.replace('.zip','') for i in os.listdir(source_path)]
    targetName = sys.argv[1]
    if targetName in projectNameList:
        os.remove(source_path+os.sep+targetName+'.zip')
        print("Delete RiskQuantLib Project: ",targetName)
    else:
        print("There Is No RiskQuantLib Project Named As ",targetName)

def clearAllProjectTemplate():
    """
    clearAllProjectTemplate() is a function to delete all RiskQuantLib projects from library.

    Use terminal command 'clearRQL' to use this function.
    After calling this function, all existing RiskQuantLib projects will be removed.

    Returns
    -------
    None
    """
    confirm = input("This action can not be canceled, are you sure to move on? (y/n)")
    if confirm.lower() != 'y':
        return None
    else:
        import os
        source_path = checkAndCreateTemplatePath()
        projectNameList = [i.replace('.zip','') for i in os.listdir(source_path)]
        [os.remove(source_path+os.sep+targetName+'.zip') for targetName in projectNameList]
        print("Delete All RiskQuantLib Project Templates Finished! ")

def addProjectTemplateFromGithub():
    """
    addProjectTemplateFromGithub() is a function to download template from Github to local disk.
    Use terminal command 'getRQL' to use this function.
    After this function is called, the target repository will be saved as template project.

    Returns
    -------
    None
    """
    import os
    name = sys.argv[1]
    source_path = checkAndCreateTemplatePath()
    from RiskQuantLib.Tool.githubTool import Github
    link = Github()
    link.downloadRepositories(name,source_path)

def receiveProjectTemplate():
    """
    receiveProjectTemplate() is a function to receive any file or dictionary from your friend by
    LOCAL AREA NETWORK (LAN).

    Use terminal command 'recvRQL' to use this function. You can also specify a path where your want to
    save the shared file or dictionary, like 'recvRQL targetPath'. If you do not give a path, the file will
    be stored in current working dictionary.

    After this function is called, you can receive the file shared from your friend, who is also in the
    same LAN. You can not receive files or project from people outside your local network by this function. If you
    want to share with friends who is across ocean, maybe you should use Github and getRQL command.

    Returns
    -------
    None
    """
    import os
    numberOfArgv = len(sys.argv)
    if numberOfArgv == 1:
        targetPath = os.getcwd()
    else:
        targetPath = sys.argv[1]
    from RiskQuantLib.Tool.fileTool import fileReceiver
    receive = fileReceiver(targetPath)
    receive.run()

def sendProjectTemplate():
    """
    sendProjectTemplate() is a function to send any file or dictionary to your friend by
    LOCAL AREA NETWORK (LAN).

    Use terminal command 'sendRQL targetProjectPath' or 'sendRQL targetFilePath' to use this function. If
    you send a dictionary, it will be packed into a zip file at first, and sent to your friend.

    After this function is called, you can send to your friend who is also in the same LAN.
    You can not send files or project to people outside your local network by this function. If you
    want to share with friends who is across ocean, maybe you should use Github and getRQL command.

    Returns
    -------
    None
    """
    import os
    from RiskQuantLib.Tool.fileTool import fileSender
    numberOfArgv = len(sys.argv)
    targetPath = sys.argv[1]
    if os.path.isdir(targetPath):
        packProject()
        name = targetPath.split(os.sep)[-1]
        parentProjectPath = os.path.dirname(targetPath)
        filePath = parentProjectPath + os.sep + name + ".zip"
        send = fileSender(filePath)
        send.run()
        os.remove(parentProjectPath + os.sep + name + '.zip')
    else:
        filePath = targetPath
        send = fileSender(filePath)
        send.run()


