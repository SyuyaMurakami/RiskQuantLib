#!/usr/bin/python
#coding = utf-8
import sys,argparse

def initiateBuildFile():
    """
    initiateBuildFile() is a function to generate content of build.py source file.

    build.py will be created in every RiskQuantLib project when initiating it. It is
    the entrance of build and render action. Users can either call 'python build.py'
    directly or add some parameter from command line.

    Returns
    -------
    PYB : pythonScriptBuilder

    """
    from RiskQuantLib.Tool.codeBuilderTool import pythonScriptBuilder, codeBuilder
    PYB = pythonScriptBuilder()
    PYB.setTitle()
    PYB.setImport('os,sys,argparse')
    PYB.setImport('RiskQuantLib','',True,'autoBuildProject,buildProject')
    PYB.code = codeBuilder(indent=0)
    PYB.code.addLine(r'path = sys.path[0] if not getattr(sys, "frozen", False) else os.path.dirname(sys.executable)')
    PYB.code.addLine(r'parser = argparse.ArgumentParser()')
    PYB.code.addLine(r'parser.add_argument("-a","--auto", help="use auto build model to build project dynamically", action="store_true")')
    PYB.code.addLine(r'parser.add_argument("-t", "--targetPath", type=str, help="the RiskQuantLib project you want to build")')
    PYB.code.addLine(r'parser.add_argument("-r", "--renderFromPath", type=str, help="the dictionary of source code where the template code exists")')
    PYB.code.addLine(r'parser.add_argument("-c", "--channel", type=str, help="if given a channel name, render action in this channel will not delete the result of render in other channel unless it is overwritten by current render")')
    PYB.code.addLine(r'parser.add_argument("-d", "--debug", help="use debug mode, break point in Src will start to effect", action="store_true")')
    PYB.code.addLine(r'args = parser.parse_args()')
    PYB.code.addLine(r'targetPath = args.targetPath if args.targetPath else path')
    PYB.code.addLine(r'renderFromPath = args.renderFromPath if args.renderFromPath else targetPath+os.sep+"Src"')
    PYB.code.addLine(r'bindType = args.channel if args.channel else "renderedSourceCode"')
    PYB.code.addLine(r'autoBuildProject(targetPath,renderFromPath,bindType,args.debug) if args.auto else buildProject(targetPath,renderFromPath,bindType,args.debug)')
    return PYB

def initiateMainFile():
    """
    initiateMainFile() is a function to generate content of main.py source file.

    main.py will be created in every RiskQuantLib project when initiating it. It is
    the entrance of all project. Users should call 'python main.py' to run the project.

    Returns
    -------
    PYB : pythonScriptBuilder

    """
    from RiskQuantLib.Tool.codeBuilderTool import pythonScriptBuilder, codeBuilder
    PYB = pythonScriptBuilder()
    PYB.setTitle()
    PYB.setImport('os,sys')
    PYB.setImport('RiskQuantLib.module','',True,'*')
    PYB.code = codeBuilder(indent=0)
    PYB.code.addLine(r'path = sys.path[0] if not getattr(sys, "frozen", False) else os.path.dirname(sys.executable)')
    PYB.code.addLine('print("Write Your Code Here : "+path+os.sep+"main.py")')
    return PYB

def initiateInstrumentFile():
    """
    initiateInstrumentFile() is a function to generate content of Build_Instrument.xlsx.

    Build_Instrument.xlsx will be created in every RiskQuantLib project when initiating it. It is
    the declaration file of all instruments to be used in project and their inheritance relationship.

    Returns
    -------
    dfInstrument : pandas.DataFrame

    """
    import pandas as pd
    dfInstrument = pd.DataFrame(
        index=['InstrumentName', 'ParentRQLClassName', 'ParentQuantLibClassName', 'LibraryName',
               'DefaultInstrumentType']).T
    return dfInstrument

def initiateAttributeFile():
    """
    initiateAttributeFile() is a function to generate content of Build_Attr.xlsx.

    Build_Attr.xlsx will be created in every RiskQuantLib project when initiating it. It is
    the declaration file of all attributes which will be bound into instruments.

    Returns
    -------
    dfAttr : pandas.DataFrame

    """
    import pandas as pd
    dfAttr = pd.DataFrame(index=['SecurityType', 'AttrName', 'AttrType']).T
    return dfAttr

def parseBuildPath(targetPath: str, checkExist:bool = False):
    """
    parseBuildPath() is a function to generate the paths of project related file.

    Parameters
    ----------
    targetPath : str
        The path of target RiskQuantLib project dictionary.
    checkExist : bool
        If true, this function will check the existence of related path of
        target project. It will raise exception iin case of absence.


    Returns
    -------
    rqlPath : str
        the path of RiskQuantLib dictionary
    instrumentExcelPath : str
        the path of instrument declaration file
    attributeExcelPath : str
        the path of attribute declaration file
    buildCachePath : str
        the path of building cache

    """
    import os
    rqlPath = targetPath + os.sep + "RiskQuantLib"
    instrumentExcelPath = targetPath + os.sep + "Build_Instrument.xlsx"
    attributeExcelPath = targetPath + os.sep + "Build_Attr.xlsx"
    buildCachePath = rqlPath + os.sep + "Build" + os.sep + "buildInfo.pkl"
    if checkExist and (not os.path.isdir(rqlPath) or not os.path.exists(instrumentExcelPath) or not os.path.exists(attributeExcelPath)):
        raise Exception("The target dictionary should be a RiskQuantLib project, with Build_Instrument.xlsx and Build_Attr.xlsx in it!")
    return rqlPath, instrumentExcelPath, attributeExcelPath, buildCachePath

def buildProjectFromExcel(targetPath: str, buildCachePath: str, instrumentExcelPath: str, attributeExcelPath: str,
                          renderFromPath: str, bindType: str = 'renderedSourceCode', debug: bool = False):
    """
    buildProjectFromExcel() is a function to build project according to excel declaration.

    Parameters
    ----------
    targetPath : str
        The path of target RiskQuantLib project dictionary.
    buildCachePath : str
        The path of building cache.
    instrumentExcelPath : str
        The path of Build_Instrument.xlsx.
    attributeExcelPath : str
        The path of Build_Attr.xlsx
    renderFromPath : str
        The path of source code dictionary
    bindType : str
        The channel of binding action. Source code are rendered and injected into project by different channels,
        The source code injected by channel A will be not influenced by source code injected by channel B, unless
        the content of tag is overwritten by code in channel B. This is used when you have several builders and
        you want them to build into the same project. In this case, you should give a bindType for each render action
        to make sure they do not conflict with each other.
    debug : bool
        If false, the break point in Src will not be effective, only break point within instrument class will effect.
        If true, the class method defined in Src directory will be dynamically bound to instrument node class.
        Then the program will take .py file under .Src directory as a module and import it, bind the class method into
        specified class. This mode is useful when your code is still under development. You will not have to change between
        ./Src/somecode.py and target instrument class .py file to edit any code error. The break point will stop right
        under ./Src/somecode.py.

    Returns
    -------
    None

    """
    import os
    from RiskQuantLib.Build.builder import excelBuilder
    if os.path.isfile(buildCachePath):
        buildObj = excelBuilder.loadInfo(buildCachePath)
    else:
        buildObj = excelBuilder(targetProjectPath=targetPath)
    buildObj.buildProject(instrumentExcelPath=instrumentExcelPath, attributeExcelPath=attributeExcelPath)
    buildObj.renderProject(renderFromPath,bindType,persist=False, debug=debug)
    print("Build Project Finished")

def newProject(targetPath:str = ''):
    """
    newProject() is a function to create a new RiskQuantLib project.

    Use terminal command 'newRQL' to use this function.
    The terminal command 'newRQL' accept a parameter 'targetPathString', which is the path that you want to build RiskQuantLib project.
    If there is already a RiskQuantLib project in target path, it will be deleted and replaced by a new project.

    Parameters
    ----------
    targetPath : str
        A terminal command parameter, specify the path where you want to build a new project.

    Returns
    -------
    None

    """
    if targetPath == '':
        parser = argparse.ArgumentParser()
        parser.add_argument("target", type=str, help="the target dictionary where you want to create a RiskQuantLib project")
        args = parser.parse_args()
        targetPath = args.target

    import os,shutil

    RiskQuantLibDictionary = os.path.abspath(__file__).split('RiskQuantLib'+os.sep+'__init__')[0]
    sourcePath = os.path.abspath(RiskQuantLibDictionary)+os.sep+r'RiskQuantLib'
    rqlPath, instrumentExcelPath, attributeExcelPath, buildCachePath = parseBuildPath(targetPath)

    if not os.path.exists(rqlPath):
        # if there is no target path, create one
        os.makedirs(rqlPath)

    if os.path.exists(sourcePath):
        # if there is already a path, clear it
        shutil.rmtree(rqlPath)

    shutil.copytree(sourcePath, rqlPath)

    # create excel file for build
    dfAttr = initiateAttributeFile()
    dfInstrument = initiateInstrumentFile()
    dfAttr.to_excel(attributeExcelPath,index=0)
    dfInstrument.to_excel(instrumentExcelPath,index=0)

    # create build script
    from RiskQuantLib.Tool.codeBuilderTool import pythonScriptBuilder,codeBuilder
    PYB = initiateBuildFile()
    PYB.writeToFile(targetPath + os.sep + 'build.py')

    # create program start point
    PYB = initiateMainFile()
    PYB.writeToFile(targetPath+os.sep+'main.py')

    # create python source file dictionary
    renderFromPath = targetPath+os.sep+'Src'
    os.makedirs(renderFromPath) if not os.path.exists(renderFromPath) else None

    print('RiskQuantLib project created!')


def packProject(targetPath:str = '', targetName:str = ''):
    """
    packProject() is a function to pack a RiskQuantLib project into '.zip' file.

    Use terminal command 'pkgRQL' to use this function.
    The terminal command 'pkgRQL' accept a parameter 'targetPathString',
    which is the RiskQuantLib project path that you want to package.
    It doesn't need to have a dictionary named 'RiskQuantLib' to be packaged.

    Parameters
    ----------
    targetPath : str
        A terminal command parameter, specify the RiskQuantLib project path which you want to package.
    targetName : str
        A terminal command parameter, specify the name you want to mark the project zip file with.

    Returns
    -------
    None
    """
    if targetPath == '' and targetName == '':
        parser = argparse.ArgumentParser()
        parser.add_argument("target", type=str, help="the RiskQuantLib project which you want to package into a zip file")
        parser.add_argument("-n", "--name", type=str, help="the name which you want to name the project by")
        args = parser.parse_args()
        targetPath = args.target
        targetName = args.name if args.name else ''

    import os, shutil, logging
    if targetName=='':
        name = targetPath.split(os.sep)[-1]
    else:
        nameList = targetName.split('.')
        if len(nameList)>1:
            name = "".join(nameList[0:-1])
        else:
            name = nameList[0]
    parentProjectPath = os.path.dirname(targetPath)
    logger = logging.getLogger("nameOfTheLogger")
    ConsoleOutputHandler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    ConsoleOutputHandler.setFormatter(formatter)
    logger.addHandler(ConsoleOutputHandler)
    logger.setLevel(logging.INFO)
    shutil.make_archive(parentProjectPath + os.sep + name, "zip", targetPath, logger=logger)
    print('RiskQuantLib project packaged!')

def checkAndCreateTemplatePath():
    """
    checkAndCreateTemplatePath() is a function to check whether the Template path exists.

    Returns
    -------
    sourcePath : str
        The path of RiskQuantLib template dictionary.
    """
    import os
    RiskQuantLibDictionary = os.path.abspath(__file__).split('RiskQuantLib'+os.sep+'__init__')[0]
    sourcePath = os.path.abspath(RiskQuantLibDictionary) + os.sep + r'RQLTemplate'
    if os.path.exists(sourcePath):
        pass
    else:
        os.makedirs(sourcePath)
    return sourcePath

def addProjectTemplate(targetPath:str = '', targetName:str = ''):
    """
    addProjectTemplate() is a function to add a RiskQuantLib project '.zip' file to library.

    Use terminal command 'addRQL' to use this function.
    The terminal command 'addRQL' accept a parameter 'targetPathString',
    which is the RiskQuantLib project '.zip' file path that you want to add to library.
    It have to be a '.zip' file to be added to library.

    Parameters
    ----------
    targetPath : str
        A terminal command parameter, specify the RiskQuantLib project '.zip' file path which you want to add to library.
    targetName : str
        The name you want to use to save the .zip file as, it is not necessary to add .zip behind it.

    Returns
    -------
    None
    """
    if targetPath == '' and targetName == '':
        parser = argparse.ArgumentParser()
        parser.add_argument("target", type=str, help="the zipped RiskQuantLib project file you want to add into RiskQuantLib library")
        parser.add_argument("-n", "--name", type=str, help="the name which you want to store the .zip file as")
        args = parser.parse_args()
        targetPath = args.target
        targetName = args.name if args.name else ''

    import os, shutil
    projectPackPath = os.path.splitext(targetPath)[0]

    if targetName=='':
        name = projectPackPath.split(os.sep)[-1]
    else:
        nameList = targetName.split('.')
        if len(nameList)>1:
            name = "".join(nameList[0:-1])
        else:
            name = nameList[0]
    sourcePath = checkAndCreateTemplatePath()
    shutil.copy(targetPath,sourcePath+os.sep+name+'.zip')
    os.remove(targetPath)
    print('RiskQuantLib project template added!')

def saveProject(targetPath:str = '', targetName:str = ''):
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
    targetPath : str
        A terminal command parameter, specify the RiskQuantLib project path which you want to save as template.
    targetName : str
        A terminal command parameter, specify the name you want to save this project as.

    Returns
    -------
    None
    """
    if targetPath == '' and targetName == '':
        parser = argparse.ArgumentParser()
        parser.add_argument("target", type=str, help="the path of RiskQuantLib project which you want to save into RiskQuantLib library")
        parser.add_argument("-n", "--name", type=str, help="the name which you want to store the RiskQuantLib project as")
        args = parser.parse_args()
        targetPath = args.target
        targetName = args.name if args.name else ''

    import os

    parentDir = os.path.dirname(targetPath)
    name = targetPath.split(os.sep)[-1] if targetName == '' else targetName

    packProject(targetPath=targetPath,targetName=name)
    addProjectTemplate(targetPath=parentDir+os.sep+name+'.zip',targetName=name)

def unpackProject(templateName:str = '', targetPath:str = ''):
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
    templateName : str
        A terminal command parameter, specify the project name you want to unpack from library.

    targetPath : str
        A terminal command parameter, specify the path where you want to unpack RiskQuantLib project.

    Returns
    -------
    None
    """
    if templateName == '' and targetPath == '':
        parser = argparse.ArgumentParser()
        parser.add_argument("template", type=str, help="the name of saved RiskQuantLib project")
        parser.add_argument("target", type=str, help="the path where you want to unpack the template project into")
        args = parser.parse_args()
        templateName = args.template
        targetPath = args.target

    # use index number to locate template
    if str.isdigit(templateName):
        import os
        sourcePath = checkAndCreateTemplatePath()
        projectNameDict = {idx:i.replace('.zip', '') for idx, i in enumerate(os.listdir(sourcePath))}
        templateIndex = int(templateName)
        templateName = projectNameDict[templateIndex] if templateIndex in projectNameDict else templateName

    import sys,os,shutil
    RiskQuantLibDictionary = os.path.abspath(__file__).split('RiskQuantLib'+os.sep+'__init__')[0]
    sourcePath = os.path.abspath(RiskQuantLibDictionary)+os.sep+r'RQLTemplate'
    shutil.unpack_archive(sourcePath+os.sep+templateName+'.zip',targetPath,"zip")
    if os.path.exists(targetPath+os.sep+templateName+'.zip'):
        os.remove(targetPath+os.sep+templateName+'.zip')
    print('RiskQuantLib project template '+templateName+' unpack finished!')

def listProjectTemplate():
    """
    listProjectTemplate() is a function to show all RiskQuantLib projects from library.

    Use terminal command 'listRQL' to use this function.

    Returns
    -------
    None
    """
    import os
    sourcePath = checkAndCreateTemplatePath()
    projectNameList = [i.replace('.zip','') for i in os.listdir(sourcePath)]
    hints = "Show all RiskQuantLib template projects:"
    print(hints)
    print("".join(['-' for i in range(len(hints))]))
    [print(index,"->",name) for index,name in enumerate(projectNameList)]

def delProjectTemplate(targetName:str = ''):
    """
    delProject() is a function to delete a RiskQuantLib project from library.

    Use terminal command 'delRQL' to use this function.
    The terminal command 'delRQL' accept a parameter 'projectName',
    which is the project name you want to delete from library.
    After calling this function, the existing RiskQuantLib project will be removed from library.

    Parameters
    ----------
    targetName : str
        A terminal command parameter, specify the project name you want to delete from library.

    Returns
    -------
    None
    """
    if targetName == '':
        parser = argparse.ArgumentParser()
        parser.add_argument("targetName", type=str, help="the name of template project which you saved in RiskQuantLib library")
        args = parser.parse_args()
        targetName = args.targetName

    import os
    sourcePath = checkAndCreateTemplatePath()
    projectNameList = [i.replace('.zip','') for i in os.listdir(sourcePath)]
    if targetName in projectNameList:
        os.remove(sourcePath+os.sep+targetName+'.zip')
        print("Delete RiskQuantLib project succeeded: ",targetName)
    else:
        print("There is no RiskQuantLib project named as: ",targetName)

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
        sourcePath = checkAndCreateTemplatePath()
        projectNameList = [i.replace('.zip','') for i in os.listdir(sourcePath)]
        [os.remove(sourcePath+os.sep+targetName+'.zip') for targetName in projectNameList]
        print("Delete all RiskQuantLib project templates finished!")

def addProjectTemplateFromGithub(targetGithub:str = ''):
    """
    addProjectTemplateFromGithub() is a function to download template from Github to local disk.
    Use terminal command 'getRQL' to use this function.
    After this function is called, the target repository will be saved as template project.

    Parameters
    ----------
    targetGithub : str
        A terminal command parameter, specify the project name you want to download from Github.

    Returns
    -------
    None
    """
    if targetGithub == '':
        parser = argparse.ArgumentParser()
        parser.add_argument("targetGithub", type=str, help="the name of Github repository or the link of Github repository")
        args = parser.parse_args()
        targetGithub = args.targetGithub

    sourcePath = checkAndCreateTemplatePath()
    from RiskQuantLib.Tool.githubTool import Github
    link = Github()
    link.downloadRepositories(targetGithub,sourcePath)

def receiveProjectTemplate(targetPath:str = ''):
    """
    receiveProjectTemplate() is a function to receive any file or dictionary from your friend by
    LOCAL AREA NETWORK (LAN).

    Use terminal command 'recvRQL' to use this function. You can also specify a path where your want to
    save the shared file or dictionary, like 'recvRQL targetPath'. If you do not give a path, the file will
    be stored in current working dictionary.

    After this function is called, you can receive the file shared from your friend, who is also in the
    same LAN. You can not receive files or project from people outside your local network by this function. If you
    want to share with friends who is across ocean, maybe you should use Github and getRQL command.

    Parameters
    ----------
    targetPath : str
        A terminal command parameter, specify the path where you want to hold the received file.

    Returns
    -------
    None
    """
    import os
    if targetPath == '':
        parser = argparse.ArgumentParser()
        parser.add_argument("-t","--targetPath", type=str, help="the path where you want to save the received files into, default as current working dictionary")
        args = parser.parse_args()
        targetPath = args.targetPath if args.targetPath else os.getcwd()

    from RiskQuantLib.Tool.fileTool import fileReceiver
    receive = fileReceiver(targetPath)
    receive.run()

def sendProjectTemplate(targetPath:str = ''):
    """
    sendProjectTemplate() is a function to send any file or dictionary to your friend by
    LOCAL AREA NETWORK (LAN).

    Use terminal command 'sendRQL targetProjectPath' or 'sendRQL targetFilePath' to use this function. If
    you send a dictionary, it will be packed into a zip file at first, and sent to your friend.

    After this function is called, you can send to your friend who is also in the same LAN.
    You can not send files or project to people outside your local network by this function. If you
    want to share with friends who is across ocean, maybe you should use Github and getRQL command.

    Parameters
    ----------
    targetPath : str
        A terminal command parameter, specify the path of file or dictionary you want to send.

    Returns
    -------
    None
    """
    if targetPath == '':
        parser = argparse.ArgumentParser()
        parser.add_argument("targetPath", type=str, help="the path of dictionary or file you want to send, if it's a dictionary, it will be packaged into a zip file first")
        args = parser.parse_args()
        targetPath = args.targetPath

    import os
    from RiskQuantLib.Tool.fileTool import fileSender
    if os.path.isdir(targetPath):
        packProject(targetPath=targetPath)
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


def buildProject(targetPath:str = '', renderFromPath:str = '', channel:str = '', debug:bool = False):
    """
    buildProject() is a function to build RiskQuantLib project.

    Use terminal command 'bldRQL targetProjectPath' to use this function. The project
    will be built according to the Build_Instrument.xlsx and Build_Attr.xlsx in
    the targetProjectPath.

    After this function is called, the instrument class file and attribute API will be
    automatically generated.

    For old version user of RiskQuantLib, this function is totally the same as
    command 'python build.py' in terminal with working dictionary as targetProjectPath.

    Parameters
    ----------
    targetPath : str
        A terminal command parameter, specify the RiskQuantLib project path you want to build and render.
    renderFromPath : str
        The path of dictionary of source file used to render target project.
    channel : str
        render action in this channel will not delete the result of render in other channel
        unless it is overwritten by current render.
    debug : bool
        If false, the break point in Src will not be effective, only break point within instrument class will effect.
        If true, the class method defined in Src directory will be dynamically bound to instrument node class.
        Then the program will take .py file under .Src directory as a module and import it, bind the class method into
        specified class. This mode is useful when your code is still under development. You will not have to change between
        ./Src/somecode.py and target instrument class .py file to edit any code error. The break point will stop right
        under ./Src/somecode.py.

    Returns
    -------
    None
    """

    if targetPath == '' and renderFromPath == '':
        parser = argparse.ArgumentParser()
        parser.add_argument("targetPath", type=str, help="the RiskQuantLib project you want to build")
        parser.add_argument("-r","--renderFromPath", type=str, help="the dictionary of source code where the template code exists")
        parser.add_argument("-c", "--channel", type=str, help="if given a channel name, render action in this channel will not delete the result of render in other channel unless it is overwritten by current render")
        parser.add_argument("-d", "--debug", help="use debug mode, break point in Src will start to effect", action="store_true")
        args = parser.parse_args()
        targetPath = args.targetPath
        renderFromPath = args.renderFromPath
        channel = args.channel
        debug = args.debug

    import os
    renderFromPath = renderFromPath if renderFromPath else (targetPath + os.sep + "Src")
    bindType = channel if channel else 'renderedSourceCode'
    rqlPath,instrumentExcelPath,attributeExcelPath,buildCachePath = parseBuildPath(targetPath, checkExist=True)
    buildProjectFromExcel(targetPath, buildCachePath,instrumentExcelPath,attributeExcelPath, renderFromPath, bindType, debug)

def autoBuildProject(targetPath:str = '', renderFromPath:str = '', channel:str = '', debug:bool = False):
    """
    autoBuildProject() is a function to build RiskQuantLib project. This function keeps
    running until catch a KeyboardInterrupt Exception.

    Use terminal command 'autoRQL targetProjectPath' to use this function. The project
    will be built according to the Build_Instrument.xlsx and Build_Attr.xlsx in
    the targetProjectPath.

    After this function is called, the instrument class file and attribute API will be
    automatically generated and updated.

    Parameters
    ----------
    targetPath : str
        A terminal command parameter, specify the RiskQuantLib project path you want to build and render.
    renderFromPath : str
        The path of dictionary of source file used to render target project.
    channel : str
        render action in this channel will not delete the result of render in other channel
        unless it is overwritten by current render.
    debug : bool
        If false, the break point in Src will not be effective, only break point within instrument class will effect.
        If true, the class method defined in Src directory will be dynamically bound to instrument node class.
        Then the program will take .py file under .Src directory as a module and import it, bind the class method into
        specified class. This mode is useful when your code is still under development. You will not have to change between
        ./Src/somecode.py and target instrument class .py file to edit any code error. The break point will stop right
        under ./Src/somecode.py.

    Returns
    -------
    None
    """
    if targetPath == '' and renderFromPath == '':
        parser = argparse.ArgumentParser()
        parser.add_argument("targetPath", type=str, help="the RiskQuantLib project you want to build automatically")
        parser.add_argument("-r", "--renderFromPath", type=str, help="the dictionary of source code where the template code exists")
        parser.add_argument("-c", "--channel", type=str, help="if given a channel name, render action in this channel will not delete the result of render in other channel unless it is overwritten by current render")
        parser.add_argument("-d", "--debug", help="use debug mode, break point in Src will start to effect", action="store_true")
        args = parser.parse_args()
        targetPath = args.targetPath
        renderFromPath = args.renderFromPath
        channel = args.channel
        debug = args.debug

    import os
    renderFromPath = renderFromPath if renderFromPath else (targetPath + os.sep + "Src")
    bindType = channel if channel else 'renderedSourceCode'
    rqlPath, instrumentExcelPath, attributeExcelPath, buildCachePath = parseBuildPath(targetPath, checkExist=True)

    # The call back function must be a single parameter function
    def build(projectPath=targetPath):
        buildProjectFromExcel(targetPath,buildCachePath,instrumentExcelPath,attributeExcelPath, renderFromPath, bindType, debug)

    from RiskQuantLib.Tool.fileTool import systemWatcher
    watchObj = systemWatcher([instrumentExcelPath, attributeExcelPath, renderFromPath], call_back_function_on_any_change=build)
    watchObj.start()

def unBuildProject(targetPath:str = ''):
    """
    unBuildProject() is a function to un-build RiskQuantLib project.

    Use terminal command 'ubldRQL targetProjectPath' to use this function. The project
    will be un-built and return to the initial status.

    After this function is called, the attribute API will be automatically removed, any all registration
    of instrument will be deleted. But, python source file will not be deleted until you do it by yourself.

    After a project is un-built, you can not use instrument directly in main.py or create new instrument
    inherited from those un-registered instrument. The file Build_Instrument.xlsx and Build_Attr.xlsx will not be
    changed after you call this function.

    Parameters
    ----------
    targetPath : str
        A terminal command parameter, specify the RiskQuantLib project path you want to un-build and un-render.

    Returns
    -------
    None
    """
    if targetPath == '':
        parser = argparse.ArgumentParser()
        parser.add_argument("targetPath", type=str, help="the RiskQuantLib project you want to un-build")
        args = parser.parse_args()
        targetPath = args.targetPath

    import os
    rqlPath, instrumentExcelPath, attributeExcelPath, buildCachePath = parseBuildPath(targetPath, checkExist=True)
    from RiskQuantLib.Build.builder import excelBuilder
    buildObj = excelBuilder.loadInfo(buildCachePath) if os.path.isfile(buildCachePath) else excelBuilder(targetProjectPath=targetPath)
    buildObj.clearProject()
    print("Project un-build finished!")


def persistProject(targetPath:str = '', renderFromPath:str = '', channel:str = ''):
    """
    persistProject() is a function to persist RiskQuantLib project.

    Use terminal command 'pstRQL targetProjectPath' to use this function. The project
    will be changed into a permanent project, where all current attribute APIs and instrument registrations
    will not be influenced by build.py anymore.

    This function is like a snapshot of your project, it freezes all effective APIs into permanent ones.

    Surely, you can still build the persisted project with new Build_Instrument.xlsx and Build_Attr.xlsx file.
    Just remember, no matter how many times you build it, the persisted API will remain effective and will not be influenced.

    This command is used when you want to distribute your project to someone else, but you do not want him to change your
    current API. Or this command is used when you are quite sure your current code is stable and can be settled down so that
    you can move on to next stage.

    This function will remove the file Build_Instrument.xlsx and Build_Attr.xlsx and replace them with new ones.

    This command can not be cancelled or un-done, use it carefully.

    Parameters
    ----------
    targetPath : str
        A terminal command parameter, specify the RiskQuantLib project path you want to persist.
    renderFromPath : str
        The path of dictionary of source file used to render target project.
    channel : str
        render action in this channel will not delete the result of render in other channel
        unless it is overwritten by current render.

    Returns
    -------
    None
    """
    if targetPath == '' and renderFromPath == '':
        parser = argparse.ArgumentParser()
        parser.add_argument("targetPath", type=str, help="the RiskQuantLib project whose code you want to change into permanent")
        parser.add_argument("-r", "--renderFromPath", type=str, help="the dictionary of source code where the template code exists")
        parser.add_argument("-c", "--channel", type=str, help="if given a channel name, render action in this channel will not delete the result of render in other channel unless it is overwritten by current render")
        args = parser.parse_args()
        targetPath = args.targetPath
        renderFromPath = args.renderFromPath
        channel = args.channel

    import os
    rqlPath, instrumentExcelPath, attributeExcelPath, buildCachePath = parseBuildPath(targetPath, checkExist=True)
    renderFromPath = renderFromPath if renderFromPath else (targetPath + os.sep + "Src")
    bindType = channel if channel else 'renderedSourceCode'
    confirm = input("This action can not be Un-Done or Cancelled, do you confirm to continue? (y/n)")
    if confirm.lower()=='y':
        from RiskQuantLib.Build.builder import excelBuilder
        buildObj = excelBuilder.loadInfo(buildCachePath) if os.path.isfile(buildCachePath) else excelBuilder(targetProjectPath=targetPath)
        buildObj.persistProject(sourceCodeDirPath=renderFromPath,bindType=bindType)
        dfAttr = initiateAttributeFile()
        dfInstrument = initiateInstrumentFile()
        dfAttr.to_excel(attributeExcelPath, index=0)
        dfInstrument.to_excel(instrumentExcelPath, index=0)
        print("Project persisted!")
    else:
        print("Action cancelled, nothing changed!")
