#!/usr/bin/python
#coding = utf-8
import argparse

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
    from RiskQuantLib.Tool.codeTool import pythonScriptBuilder, codeBuilderPython
    PYB = pythonScriptBuilder()
    PYB.setTitle()
    PYB.setImport('os,sys,argparse')
    PYB.setImport('RiskQuantLib','',True,'autoBuildProject,buildProject')
    PYB.code = codeBuilderPython(indent=0)
    PYB.code.addLine(r'path = sys.path[0] if not getattr(sys, "frozen", False) else os.path.dirname(sys.executable)')
    PYB.code.addLine(r'parser = argparse.ArgumentParser()')
    PYB.code.addLine(r'parser.add_argument("-a","--auto", help="use auto build model to build project dynamically", action="store_true")')
    PYB.code.addLine(r'parser.add_argument("-t", "--targetPath", type=str, help="the RiskQuantLib project you want to build")')
    PYB.code.addLine(r'parser.add_argument("-r", "--renderFromPath", type=str, help="the directory of source code where the template code exists")')
    PYB.code.addLine(r'parser.add_argument("-c", "--channel", type=str, help="if given a channel name, render action in this channel will not delete the result of render in other channel unless it is overwritten by current render")')
    PYB.code.addLine(r'parser.add_argument("-d", "--debug", help="use debug mode, break point in Src will start to effect", action="store_true")')
    PYB.code.addLine(r'parser.add_argument("-f", "--force", help="force to build, cached building information will be neglected, if auto-build mode is on, building information will be deleted for one time before auto-building", action="store_true")')
    PYB.code.addLine(r'args = parser.parse_args()')
    PYB.code.addLine(r'targetPath = args.targetPath if args.targetPath else path')
    PYB.code.addLine(r'renderFromPath = args.renderFromPath if args.renderFromPath else targetPath+os.sep+"Src"')
    PYB.code.addLine(r'bindType = args.channel if args.channel else "renderedSourceCode"')
    PYB.code.addLine(r'autoBuildProject(targetPath,renderFromPath,bindType,args.debug,args.force) if args.auto else buildProject(targetPath,renderFromPath,bindType,args.debug,args.force)')
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
    from RiskQuantLib.Tool.codeTool import pythonScriptBuilder, codeBuilderPython
    PYB = pythonScriptBuilder()
    PYB.setTitle()
    PYB.setImport('os,sys')
    PYB.setImport('RiskQuantLib.module','',True,'*')
    PYB.code = codeBuilderPython(indent=0)
    PYB.code.addLine(r'path = sys.path[0] if not getattr(sys, "frozen", False) else os.path.dirname(sys.executable)')
    PYB.code.addLine('print("Write Your Code Here : "+path+os.sep+"main.py")')
    return PYB

def initiateConfigFile():
    """
    initiateConfigFile() is a function to generate content of config.py source file.

    config.py will be created in every RiskQuantLib project when initiating it. It is the declaration file
    of all instruments to be used in project and their inheritance relationship, it also contains the attribute
    the would be used in this project.

    Returns
    -------
    PYB : pythonScriptBuilder

    """
    from RiskQuantLib.Tool.codeTool import pythonScriptBuilder, codeBuilderPython
    PYB = pythonScriptBuilder()
    PYB.setTitle()
    PYB.code = codeBuilderPython(indent=0)
    PYB.code.addLine('')
    PYB.code.addLine(r'#-|instrument: security, company, index, interest')
    PYB.code.addLine(r'#-|instrument: bond@security, stock@security, derivative@security, fund@security')
    PYB.code.addLine(r'#-|instrument: future@derivative, option@derivative')
    PYB.code.addLine('')
    PYB.code.addLine(r'#-|instrument-DefaultInstrumentType: security@Security, company@Company, index@Index, interest@Interest')
    PYB.code.addLine(r'#-|instrument-DefaultInstrumentType: bond@Bond, stock@Stock, derivative@Derivative, fund@Fund')
    PYB.code.addLine(r'#-|instrument-DefaultInstrumentType: future@Future, option@Option')
    return PYB

def initiateExecutableBuildShortcutFile():
    """
    initiateExecutableBuildShortcutFile() is a function to generate executable shortcut for different system.

    build.bat or build.sh will be created in every RiskQuantLib project when initiating it on Windows or linux. It is the shortcut
    of run build.py by console.

    Returns
    -------
    PYB : pythonScriptBuilder

    """
    import sys
    from RiskQuantLib.Tool.codeTool import pythonScriptBuilder, codeBuilderPython
    PYB = pythonScriptBuilder()
    PYB.code = codeBuilderPython(indent=0)
    if sys.platform in {'win32'}:
        PYB.code.addLine(r'''cd %~dp0''')
        PYB.code.addLine(r'''python build.py''')
        PYB.code.addLine(r'''pause''')
    elif sys.platform in {'darwin','linux','linux2'}:
        PYB.code.addLine(r'''DIR=$(cd $(dirname $0) && pwd)''')
        PYB.code.addLine(r'''cd $DIR''')
        PYB.code.addLine(r'''python build.py''')
        PYB.code.addLine(r'''sleep 3''')
    else:
        PYB.code.addLine('')
    return PYB

def initiateExecutableDebugShortcutFile():
    """
    initiateExecutableDebugShortcutFile() is a function to generate executable shortcut for different system.

    debug.bat or debug.sh will be created in every RiskQuantLib project when initiating it on Windows or linux. It is the shortcut
    of run build.py by console.

    Returns
    -------
    PYB : pythonScriptBuilder

    """
    import sys
    from RiskQuantLib.Tool.codeTool import pythonScriptBuilder, codeBuilderPython
    PYB = pythonScriptBuilder()
    PYB.code = codeBuilderPython(indent=0)
    if sys.platform in {'win32'}:
        PYB.code.addLine(r'''cd %~dp0''')
        PYB.code.addLine(r'''python build.py -a -d''')
        PYB.code.addLine(r'''pause''')
    elif sys.platform in {'darwin','linux','linux2'}:
        PYB.code.addLine(r'''DIR=$(cd $(dirname $0) && pwd)''')
        PYB.code.addLine(r'''cd $DIR''')
        PYB.code.addLine(r'''python build.py -a -d''')
        PYB.code.addLine(r'''sleep 3''')
    else:
        PYB.code.addLine('')
    return PYB

def parseBuildPath(targetPath: str, checkExist:bool = False):
    """
    parseBuildPath() is a function to generate the paths of project related file.

    Parameters
    ----------
    targetPath : str
        The path of target RiskQuantLib project directory.
    checkExist : bool
        If true, this function will check the existence of related path of
        target project. It will raise exception iin case of absence.


    Returns
    -------
    rqlPath : str
        the path of RiskQuantLib directory
    configFilePath : str
        The path of config.py used as default build config file.
    buildCachePath : str
        the path of building cache

    """
    import os
    rqlPath = targetPath + os.sep + "RiskQuantLib"
    configFilePath = targetPath + os.sep + "config.py"
    buildCachePath = rqlPath + os.sep + "Build" + os.sep + "buildInfo.pkl"
    if checkExist and (not os.path.isdir(rqlPath) or not os.path.exists(configFilePath)):
        raise Exception("The target directory should be a RiskQuantLib project, with directory named as RiskQuantLib and config.py in it!")
    return rqlPath, configFilePath, buildCachePath

def buildProjectFromConfig(targetPath: str, buildCachePath: str, configFilePath:str, renderFromPath: str, bindType: str = 'renderedSourceCode', debug: bool = False, force: bool = False):
    """
    buildProjectFromConfig() is a function to build project according to config.py declaration.

    Parameters
    ----------
    targetPath : str
        The path of target RiskQuantLib project directory.
    buildCachePath : str
        The path of building cache.
    configFilePath : str
        The path of config.py used as default build config file.
    renderFromPath : str
        The path of source code directory
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
    force : bool
        If True, the cached building file buildInfo.pkl will be neglected, a new builder object will be created.
        This is useful when there are some mistakes in buildInfo.pkl, or error happens when caching buildInfo.pkl.
        In these cases, old buildInfo.pkl exists but can not be used. The traditional way to solve this problem is manually
        deleting this file and build whole project again. With this parameter specified as True, users can choose to build
        project no matter buildInfo.pkl exists or not. However, any information in old building will be deleted. If you use
        guardian projects, there could be problems, you will have to build all guardian projects again.

    Returns
    -------
    None

    """
    import os, time
    from RiskQuantLib.Build.builder import configBuilder
    if os.path.isfile(buildCachePath) and not force:
        buildObj = configBuilder.loadInfo(buildCachePath)
    else:
        buildObj = configBuilder(targetProjectPath=targetPath)
    buildObj.buildProject(configFilePath=configFilePath)
    buildObj.renderProject(renderFromPath,bindType,persist=False, debug=debug)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "- Build Project Finished")

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
        parser.add_argument("target", type=str, help="the target directory where you want to create a RiskQuantLib project")
        args = parser.parse_args()
        targetPath = args.target

    import os,shutil,sys

    RiskQuantLibDirectory = os.path.abspath(__file__).split('RiskQuantLib'+os.sep+'__init__')[0]
    sourcePath = os.path.abspath(RiskQuantLibDirectory)+os.sep+r'RiskQuantLib'
    rqlPath, configFilePath, buildCachePath = parseBuildPath(targetPath)

    if not os.path.exists(rqlPath):
        # if there is no target path, create one
        os.makedirs(rqlPath)

    if os.path.exists(sourcePath):
        # if there is already a path, clear it
        shutil.rmtree(rqlPath)

    shutil.copytree(sourcePath, rqlPath)

    # create config.py for build
    PYB = initiateConfigFile()
    PYB.writeToFile(configFilePath)

    # create build script
    PYB = initiateBuildFile()
    PYB.writeToFile(targetPath + os.sep + 'build.py')

    # create program start point
    PYB = initiateMainFile()
    PYB.writeToFile(targetPath+os.sep+'main.py')

    # decide file extension depending on operating system
    shortCutFileType = '.bat' if sys.platform in {'win32'} else '.sh' if sys.platform in {'darwin', 'linux', 'linux2'} else ''

    # create build.bat or build.sh shortcut
    PYB = initiateExecutableBuildShortcutFile()
    PYB.writeToFile(targetPath + os.sep + 'build'+shortCutFileType)

    # create debug.bat or debug.sh shortcut
    PYB = initiateExecutableDebugShortcutFile()
    PYB.writeToFile(targetPath + os.sep + 'debug'+shortCutFileType)

    # create python source file directory and other useful directory
    renderFromPath = targetPath+os.sep+'Src'
    cachePath = targetPath+os.sep+'Cache'
    dataPath = targetPath+os.sep+'Data'
    resultPath = targetPath+os.sep+'Result'
    [os.makedirs(p) if not os.path.exists(p) else None for p in [renderFromPath, cachePath, dataPath, resultPath]]

    print('RiskQuantLib project created!')


def packModule(targetPath: str = '', targetName: str = '', keepTop: bool = False):
    """
    packModule() is a function to pack a RiskQuantLib project into '.zip' file.

    Use terminal command 'pkgRQL' to use this function.
    The terminal command 'pkgRQL' accept a parameter 'targetPathString',
    which is the path that you want to package.
    It doesn't need to have a directory named 'RiskQuantLib' to be packaged.

    Parameters
    ----------
    targetPath : str
        A terminal command parameter, specify the path which you want to package.
    targetName : str
        A terminal command parameter, specify the name you want to mark the zip file with.
    keepTop : bool
        A terminal command parameter, specify if this function will keep the top level directory.


    Returns
    -------
    None
    """
    if targetPath == '' and targetName == '' and not keepTop:
        parser = argparse.ArgumentParser()
        parser.add_argument("target", type=str, help="the file or directory which you want to package into a zip file")
        parser.add_argument("-n", "--name", type=str, help="the name which you want to name the module by")
        parser.add_argument("-t", "--top", help="keep top level directory", action="store_true")
        args = parser.parse_args()
        targetPath = args.target
        targetName = args.name if args.name else ''
        keepTop = args.top

    import os, shutil, logging
    if targetName == '':
        name = os.path.splitext(os.path.basename(targetPath))[0]
    else:
        nameList = targetName.split('.')
        if len(nameList)>1:
            name = "".join(nameList[0:-1])
        else:
            name = nameList[0]
    parentDirectory = os.path.dirname(targetPath)
    logger = logging.getLogger("nameOfTheLogger")
    ConsoleOutputHandler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    ConsoleOutputHandler.setFormatter(formatter)
    logger.addHandler(ConsoleOutputHandler)
    logger.setLevel(logging.INFO)
    zipAS = parentDirectory + os.sep + name
    try:
        if os.path.isdir(targetPath) and not keepTop:
            shutil.make_archive(zipAS, "zip", targetPath, logger=logger)
            print(f'RiskQuantLib module packaged: {targetPath}')
        elif os.path.isfile(targetPath) or keepTop:
            shutil.make_archive(zipAS, "zip", parentDirectory, os.path.basename(targetPath), logger=logger)
            print(f'RiskQuantLib module packaged: {targetPath}')
        else:
            raise FileExistsError(f'Target does not exist: {targetPath}')
    except Exception as e:
        failedFile = zipAS + '.zip'
        os.remove(failedFile) if os.path.isfile(failedFile) else None
        raise e

def checkAndCreateLibraryPath(moduleName: tuple = ('Template', 'Model', 'Tool')):
    """
    checkAndCreateLibraryPath() is a function to check whether the Template path exists.

    Parameters
    ----------
    moduleName : tuple
        The parameter tells how many sub-categories the library has. By default, it has Template, Model and Tool.

    Returns
    -------
    sourcePath : str
        The path of RiskQuantLib template directory.
    """
    import os
    RiskQuantLibDirectory = os.path.abspath(__file__).split('RiskQuantLib'+os.sep+'__init__')[0]
    RiskQuantLibDirectoryABS = os.path.abspath(RiskQuantLibDirectory) + os.sep + 'RQL'
    modulePath = tuple(RiskQuantLibDirectoryABS + os.sep + i for i in moduleName)
    [None if os.path.exists(s) else os.makedirs(s) for s in modulePath]
    return moduleName, modulePath, RiskQuantLibDirectoryABS

def checkModuleCategory(moduleCategory: str = ''):
    """This function will check the parameter value of moduleCategory is validated or not."""
    import os
    _, _, RiskQuantLibDirectoryABS = checkAndCreateLibraryPath()
    moduleCategoryName = moduleCategory[0].upper() + moduleCategory[1:]
    sourcePath = RiskQuantLibDirectoryABS + os.sep + moduleCategoryName
    if not os.path.exists(sourcePath):
        existCategory = [i.lower() for i in os.listdir(RiskQuantLibDirectoryABS) if os.path.isdir(RiskQuantLibDirectoryABS+os.sep+i)]
        raise ValueError('No sub-category of RiskQuantLib library named as: ', moduleCategory, 'Existed categories are: ', existCategory)
    else:
        return moduleCategoryName, sourcePath

def addModule(moduleCategory: str = '', targetPath:str = '', targetName:str = ''):
    """
    addModule() is a function to add a RiskQuantLib module '.zip' file to library.

    Use terminal command 'addRQL' to use this function.

    The terminal command 'addRQL' accept two parameters: 'moduleCategory' and 'targetPathString'.
    'moduleCategory' is the sub-category of your library, by default, it can be template, model or tool.
    'targetPathString' is the RiskQuantLib module '.zip' file path that you want to add to library.
    It has to be a '.zip' file to be added to library.

    Parameters
    ----------
    moduleCategory : str
        A terminal command parameter, specify the library sub-category you want to add '.zip' file into.
    targetPath : str
        A terminal command parameter, specify the RiskQuantLib module '.zip' file path which you want to add to library.
    targetName : str
        The name you want to use to save the .zip file as, it is not necessary to add .zip behind it.

    Returns
    -------
    None
    """
    if moduleCategory == '' and targetPath == '' and targetName == '':
        parser = argparse.ArgumentParser()
        parser.add_argument("category", type=str, help="the sub-category of your library where you want to add module into")
        parser.add_argument("target", type=str, help="the zipped module file you want to add into RiskQuantLib library")
        parser.add_argument("-n", "--name", type=str, help="the name which you want to store the .zip file as")
        args = parser.parse_args()
        moduleCategory = args.category
        targetPath = args.target
        targetName = args.name if args.name else ''

    import os
    moduleCategoryName, sourcePath = checkModuleCategory(moduleCategory)
    if targetName == '':
        modulePackPath = os.path.splitext(targetPath)[0]
        name = modulePackPath.split(os.sep)[-1]
    else:
        nameList = targetName.split('.')
        if len(nameList) > 1:
            name = "".join(nameList[0:-1])
        else:
            name = nameList[0]
    import shutil
    shutil.copy(targetPath,sourcePath+os.sep+name+'.zip')
    os.remove(targetPath)
    print(f'RiskQuantLib module added: {moduleCategoryName} -> {name}')


def saveModule(moduleCategory: str = '', targetPath: str = '', targetName: str = ''):
    """
    saveModule() is a function to save a RiskQuantLib module and add it to library.

    Use terminal command 'saveRQL' to use this function.
    The terminal command 'saveRQL' accept two parameters: 'moduleCategory' and 'targetPath'.
    'moduleCategory' is the sub-category of your library where you want to save file into,
    by default, it can be template, model or tool.
    'targetPath' is the file or directory path that you want to save.
    There is also an optional parameter 'targetName',
    which is the name you want to give to this module.
    After calling this function, a '.zip' file will be created in the target directory,
    and this file will be stored as a module.

    Parameters
    ----------
    moduleCategory : str
        A terminal command parameter, specify the library sub-category you want to save '.zip' file into.
    targetPath : str
        A terminal command parameter, specify the file or directory path which you want to save as template.
    targetName : str
        A terminal command parameter, specify the name you want to save this module as.

    Returns
    -------
    None
    """
    if moduleCategory == '' and targetPath == '' and targetName == '':
        parser = argparse.ArgumentParser()
        parser.add_argument("category", type=str, help="the sub-category of your library where you want to save module into")
        parser.add_argument("target", type=str, help="the path of file or directory which you want to save into RiskQuantLib library")
        parser.add_argument("-n", "--name", type=str, help="the name which you want to store the module as")
        args = parser.parse_args()
        moduleCategory = args.category
        targetPath = args.target
        targetName = args.name if args.name else ''

    import os
    checkModuleCategory(moduleCategory)
    parentDir = os.path.dirname(targetPath)
    name = os.path.splitext(os.path.basename(targetPath))[0] if targetName == '' else targetName
    keepTop = False if moduleCategory in {'template', 'Template'} else True

    packModule(targetPath=targetPath, targetName=name, keepTop=keepTop)
    addModule(moduleCategory=moduleCategory, targetPath=parentDir+os.sep+name+'.zip', targetName=name)

def unpackModule(moduleCategory: str = '', moduleName: str = '', targetPath: str = ''):
    """
    unpackModule() is a function to unpack a RiskQuantLib module from library and use it again.

    Use terminal command 'tplRQL' to use this function.
    The terminal command 'tplRQL' accept two parameters: 'moduleCategory' and 'moduleName',
    'moduleCategory' is the sub-category of your library where you want to unpack module from,
    by default, it can be template, model or tool.
    'moduleName' is the module name you want to unpack from library.
    'targetPathString' is the path where you want to unpack RiskQuantLib module into.
    After calling this function, the content of existing RiskQuantLib module will be unpacked to the location you choose,
    and you can start a project at the foundation of this un-packed module, or use the functions or models of un-packed module.

    Parameters
    ----------
    moduleCategory : str
        A terminal command parameter, specify the library sub-category you want to un-pack '.zip' file from.
    moduleName : str
        A terminal command parameter, specify the module name you want to unpack from library.
    targetPath : str
        A terminal command parameter, specify the path where you want to un-pack module into.

    Returns
    -------
    None
    """
    if moduleCategory == '' and moduleName == '' and targetPath == '':
        parser = argparse.ArgumentParser()
        parser.add_argument("category", type=str, help="the sub-category of your library where you want to un-pack module from")
        parser.add_argument("module", type=str, help="the name of saved RiskQuantLib module")
        parser.add_argument("target", type=str, help="the path where you want to unpack the module into")
        args = parser.parse_args()
        moduleCategory = args.category
        moduleName = args.module
        targetPath = args.target

    import os
    moduleCategoryName, sourcePath = checkModuleCategory(moduleCategory)

    # use index number to locate template
    if str.isdigit(moduleName):
        moduleNameDict = {idx:i.replace('.zip', '') for idx, i in enumerate(os.listdir(sourcePath))}
        templateIndex = int(moduleName)
        moduleName = moduleNameDict[templateIndex] if templateIndex in moduleNameDict else moduleName

    # change targetPath
    targetPath = targetPath + os.sep + 'RiskQuantLib' + os.sep + 'Model' if moduleCategoryName == 'Model' else targetPath + os.sep + 'RiskQuantLib' + os.sep + 'Tool' if moduleCategoryName == 'Tool' else targetPath
    os.makedirs(targetPath) if not os.path.exists(targetPath) else None

    import shutil
    shutil.unpack_archive(sourcePath+os.sep+moduleName+'.zip',targetPath,"zip")
    if os.path.exists(targetPath+os.sep+moduleName+'.zip'):
        os.remove(targetPath+os.sep+moduleName+'.zip')
    print(f'RiskQuantLib module unpack finished: {moduleCategoryName} -> {moduleName}')

def listItem(hints: str, itemList: list):
    print(hints)
    print("".join(['-' for i in range(len(hints))]))
    [print(index,"->",name) for index,name in enumerate(itemList)]

def listModule(moduleCategory: str = ''):
    """
    listModule() is a function to show all RiskQuantLib modules from library.

    Use terminal command 'listRQL' to use this function.

    Parameters
    ----------
    moduleCategory : str
        A terminal command parameter, specify the library sub-category you want to show.

    Returns
    -------
    None
    """
    if moduleCategory == '':
        parser = argparse.ArgumentParser()
        parser.add_argument("-c", "--category", type=str, help="the sub-category of your library that you want to show")
        args = parser.parse_args()
        moduleCategory = args.category if args.category else ''
    import os
    _, _, RiskQuantLibDirectoryABS = checkAndCreateLibraryPath()
    moduleCategoryList = [i for i in os.listdir(RiskQuantLibDirectoryABS) if os.path.isdir(RiskQuantLibDirectoryABS+os.sep+i)] if moduleCategory == '' else [moduleCategory[0].upper() + moduleCategory[1:]]
    sourcePathList = [(i, RiskQuantLibDirectoryABS + os.sep + i) for i in moduleCategoryList]
    moduleFileList = [(moduleCategoryName, [i.replace('.zip','') for i in os.listdir(sourcePath)]) for moduleCategoryName, sourcePath in sourcePathList if os.path.isdir(sourcePath)]
    [listItem(f"\nShow all RiskQuantLib {moduleCategoryName}:", moduleFile) for moduleCategoryName, moduleFile in moduleFileList]

def deleteModule(moduleCategory: str = '', targetName: str = ''):
    """
    deleteModule() is a function to delete a RiskQuantLib module from library.

    Use terminal command 'delRQL' to use this function.
    The terminal command 'delRQL' accept two parameters: 'moduleCategory' and 'targetName'.
    'moduleCategory' is the sub-category of your library where you want to delete module from,
    by default, it can be template, model or tool.
    'targetName' is the module name you want to delete.
    After calling this function, the existing RiskQuantLib module will be removed from library.

    Parameters
    ----------
    moduleCategory : str
        A terminal command parameter, specify the library sub-category you want to delete module from.
    targetName : str
        A terminal command parameter, specify the module name you want to delete from library.

    Returns
    -------
    None
    """
    if moduleCategory == '' and targetName == '':
        parser = argparse.ArgumentParser()
        parser.add_argument("category", type=str, help="the sub-category of your library where you want to delete module from")
        parser.add_argument("target", type=str, help="the name of module which you will delete")
        args = parser.parse_args()
        moduleCategory = args.category
        targetName = args.target

    import os
    moduleCategoryName, sourcePath = checkModuleCategory(moduleCategory)
    # use index number to locate template
    if str.isdigit(targetName):
        moduleNameDict = {idx: i.replace('.zip', '') for idx, i in enumerate(os.listdir(sourcePath))}
        templateIndex = int(targetName)
        targetName = moduleNameDict[templateIndex] if templateIndex in moduleNameDict else targetName
    moduleNameList = [i.replace('.zip','') for i in os.listdir(sourcePath)]
    if targetName in moduleNameList:
        os.remove(sourcePath+os.sep+targetName+'.zip')
        print(f"Delete RiskQuantLib module succeeded: {moduleCategoryName} -> {targetName}")
    else:
        print(f"There is no RiskQuantLib module: {moduleCategoryName} -> {targetName}")

def clearAllModule():
    """
    clearAllModule() is a function to delete all RiskQuantLib modules from library.

    Use terminal command 'clearRQL' to use this function.
    After calling this function, all existing RiskQuantLib modules will be removed.

    Returns
    -------
    None
    """
    confirm = input("This action can not be canceled, are you sure to move on? (y/n)")
    if confirm.lower() != 'y':
        return None
    else:
        import os
        _, _, RiskQuantLibDirectoryABS = checkAndCreateLibraryPath()
        absPathList = [(i, RiskQuantLibDirectoryABS + os.sep + i) for i in os.listdir(RiskQuantLibDirectoryABS)]
        sourcePathList = [(n, p) for n, p in absPathList if os.path.isdir(p)]
        for moduleCategory, sourcePath in sourcePathList:
            moduleNameList = [i.replace('.zip','') for i in os.listdir(sourcePath)]
            [os.remove(sourcePath+os.sep+targetName+'.zip') for targetName in moduleNameList]
            print(f"Delete all RiskQuantLib module finished: {moduleCategory}")

def setDefaultModule(moduleCategory: str = '', moduleName: str = ''):
    """
    setDefaultModule() is a function to set a module into default initialization one.

    Use terminal command 'dftRQL' to use this function.
    The terminal command 'dftRQL' accept two parameters: 'moduleCategory' and 'moduleName'.
    'moduleCategory' is the sub-category of your library where you want to set module as default from,
    by default, it can be model or tool.
    'moduleName' is the module name you want to set as default one.
    After calling this function, the existing RiskQuantLib module will be set as default, which means every new
    RiskQuantLib project created by 'newRQL' command will use this module.

    Parameters
    ----------
    moduleCategory : str
        A terminal command parameter, specify the library sub-category you want to set module as default from.
    moduleName : str
        A terminal command parameter, specify the module name you want to set as default.

    Returns
    -------
    None
    """
    if moduleCategory == '' and moduleName == '':
        parser = argparse.ArgumentParser()
        parser.add_argument("category", type=str, help="the sub-category of your library where you want to set module as default from")
        parser.add_argument("module", type=str, help="the name of module which you will set as default")
        args = parser.parse_args()
        moduleCategory = args.category
        moduleName = args.module

    import os
    defaultCategory = {'Model', 'Tool'}
    moduleCategoryName = moduleCategory[0].upper() + moduleCategory[1:]
    if moduleCategoryName not in defaultCategory:
        raise ValueError('Given sub-category is not supported to set default value: ', moduleCategory, 'Current supported sub-category of default is: ', [i.lower() for i in defaultCategory])
    else:
        RiskQuantLibDirectory = os.path.abspath(__file__).split('RiskQuantLib' + os.sep + '__init__')[0]
        targetPath = os.path.abspath(RiskQuantLibDirectory)
        unpackModule(moduleCategory, moduleName, targetPath)

def removeDefaultModule(moduleCategory: str = '', moduleName: str = ''):
    """
    setDefaultModule() is a function to remove a module from default initialization.

    Use terminal command 'udftRQL' to use this function.
    The terminal command 'udftRQL' accept two parameters: 'moduleCategory' and 'moduleName'.
    'moduleCategory' is the sub-category of your library where you want to remove module from,
    by default, it can be model or tool.
    'moduleName' is the module name you want to set as default one.
    After calling this function, the RiskQuantLib module will be removed from default, which means every new
    RiskQuantLib project created by 'newRQL' command will not use this module anymore.

    Parameters
    ----------
    moduleCategory : str
        A terminal command parameter, specify the library sub-category you want to remove module from.
    moduleName : str
        A terminal command parameter, specify the module name you want to remove from default.

    Returns
    -------
    None
    """
    if moduleCategory == '' and moduleName == '':
        parser = argparse.ArgumentParser()
        parser.add_argument("category", type=str, help="the sub-category of your library where you want to remove module from")
        parser.add_argument("module", type=str, help="the name of module which you will remove from default")
        args = parser.parse_args()
        moduleCategory = args.category
        moduleName = args.module

    import os, shutil
    defaultCategory = {'Model', 'Tool'}
    moduleCategoryName = moduleCategory[0].upper() + moduleCategory[1:]
    if moduleCategoryName not in defaultCategory:
        raise ValueError('Given sub-category is not supported to remove default value: ', moduleCategory, 'Current supported sub-category of default is: ', [i.lower() for i in defaultCategory])
    else:
        RiskQuantLibDirectory = os.path.abspath(__file__).split('RiskQuantLib' + os.sep + '__init__')[0]
        sourcePath = os.path.abspath(RiskQuantLibDirectory) + os.sep + 'RiskQuantLib' + os.sep + moduleCategoryName
        modulePath = sourcePath + os.sep + moduleName
        if not os.path.exists(modulePath):
            moduleList = [i for i in os.listdir(sourcePath)]
            moduleDict = {os.path.splitext(i)[0]: i for i in moduleList}
            moduleName = moduleDict[moduleName] if moduleName in moduleDict else moduleName
            modulePath = sourcePath + os.sep + moduleName
        saveModule(moduleCategory, modulePath)
        shutil.rmtree(modulePath) if os.path.isdir(modulePath) else os.remove(modulePath)
        print(f'RiskQuantLib module removed from default: {moduleCategoryName} -> {moduleName}')

def initDefaultModule():
    """This function is used to initialize default module when installing or upgrading RiskQuantLib."""
    initialModule = [
    ('model', 'Copula'), ('model', 'KMV'), 
    ('tool', 'excelTool'), ('tool', 'frameTool'), 
    ('tool', 'guiTool'), ('tool', 'mailTool'), 
    ('tool', 'pptTool'), ('tool', 'stringTool'), 
    ('tool', 'threadTool'), ('tool', 'wordTool')
    ]
    for moduleCategory, moduleName in initialModule:
        try:
            removeDefaultModule(moduleCategory, moduleName)
        except Exception as e:
            print(f'RiskQuantLib default module initialization failed: {moduleCategory} -> {moduleName}')


def addModuleFromGithub(targetGithub:str = ''):
    """
    addModuleFromGithub() is a function to download template from Github to local disk.
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

    import os
    _, _, RiskQuantLibDirectoryABS = checkAndCreateLibraryPath()
    sourcePath = RiskQuantLibDirectoryABS + os.sep + 'Template'
    from RiskQuantLib.Tool.githubTool import Github
    link = Github()
    link.downloadRepositories(targetGithub,sourcePath)

def receiveModule(targetPath: str = ''):
    """
    receiveModule() is a function to receive any file or directory from your friend by
    LOCAL AREA NETWORK (LAN).

    Use terminal command 'recvRQL' to use this function. You can also specify a path where your want to
    save the shared file or directory, like 'recvRQL targetPath'. If you do not give a path, the file will
    be stored in current working directory.

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
        parser.add_argument("-t","--targetPath", type=str, help="the path where you want to save the received files into, default as current working directory")
        args = parser.parse_args()
        targetPath = args.targetPath if args.targetPath else os.getcwd()

    from RiskQuantLib.Tool.fileTool import fileReceiver
    receive = fileReceiver(targetPath)
    receive.run()

def sendModule(targetPath: str = '') -> None:
    """
    sendModule() is a function to send any file or directory to your friend by
    LOCAL AREA NETWORK (LAN).

    Use terminal command 'sendRQL targetProjectPath' or 'sendRQL targetFilePath' to use this function. If
    you send a directory, it will be packed into a zip file at first, and sent to your friend.

    After this function is called, you can send to your friend who is also in the same LAN.
    You can not send files or project to people outside your local network by this function. If you
    want to share with friends who is across ocean, maybe you should use Github and getRQL command.

    Parameters
    ----------
    targetPath : str
        A terminal command parameter, specify the path of file or directory you want to send.

    Returns
    -------
    None
    """
    if targetPath == '':
        parser = argparse.ArgumentParser()
        parser.add_argument("targetPath", type=str, help="the path of directory or file you want to send, if it's a directory, it will be packaged into a zip file first")
        args = parser.parse_args()
        targetPath = args.targetPath

    import os
    from RiskQuantLib.Tool.fileTool import fileSender
    if os.path.isdir(targetPath):
        packModule(targetPath=targetPath)
        name = targetPath.split(os.sep)[-1]
        parentModulePath = os.path.dirname(targetPath)
        filePath = parentModulePath + os.sep + name + ".zip"
        send = fileSender(filePath)
        send.run()
        os.remove(parentModulePath + os.sep + name + '.zip')
    else:
        filePath = targetPath
        send = fileSender(filePath)
        send.run()


def buildProject(targetPath:str = '', renderFromPath:str = '', channel:str = '', debug: bool = False, force: bool = False):
    """
    buildProject() is a function to build RiskQuantLib project.

    Use terminal command 'bldRQL targetProjectPath' to use this function. The project
    will be built according to the targetProjectPath/config.py in the targetProjectPath.

    After this function is called, the instrument class file and attribute API will be
    automatically generated.

    For old version user of RiskQuantLib, this function is totally the same as
    command 'python build.py' in terminal with working directory as targetProjectPath.

    Parameters
    ----------
    targetPath : str
        A terminal command parameter, specify the RiskQuantLib project path you want to build and render.
    renderFromPath : str
        The path of directory of source file used to render target project.
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
    force : bool
        If True, the cached building file buildInfo.pkl will be neglected, a new builder object will be created.
        This is useful when there are some mistakes in buildInfo.pkl, or error happens when caching buildInfo.pkl.
        In these cases, old buildInfo.pkl exists but can not be used. The traditional way to solve this problem is manually
        deleting this file and build whole project again. With this parameter specified as True, users can choose to build
        project no matter buildInfo.pkl exists or not. However, any information in old building will be deleted. If you use
        guardian projects, there could be problems, you will have to build all guardian projects again.

    Returns
    -------
    None
    """

    if targetPath == '' and renderFromPath == '':
        parser = argparse.ArgumentParser()
        parser.add_argument("targetPath", type=str, help="the RiskQuantLib project you want to build")
        parser.add_argument("-r","--renderFromPath", type=str, help="the directory of source code where the template code exists")
        parser.add_argument("-c", "--channel", type=str, help="if given a channel name, render action in this channel will not delete the result of render in other channel unless it is overwritten by current render")
        parser.add_argument("-d", "--debug", help="use debug mode, break point in Src will start to effect", action="store_true")
        parser.add_argument("-f", "--force", help="force to build, cached building information will be neglected", action="store_true")
        args = parser.parse_args()
        targetPath = args.targetPath
        renderFromPath = args.renderFromPath
        channel = args.channel
        debug = args.debug
        force = args.force

    import os
    renderFromPath = renderFromPath if renderFromPath else (targetPath + os.sep + "Src")
    bindType = channel if channel else 'renderedSourceCode'
    rqlPath, configFilePath, buildCachePath = parseBuildPath(targetPath, checkExist=True)
    buildProjectFromConfig(targetPath, buildCachePath, configFilePath, renderFromPath, bindType, debug, force)

def autoBuildProject(targetPath:str = '', renderFromPath:str = '', channel:str = '', debug: bool = False, force: bool = False):
    """
    autoBuildProject() is a function to build RiskQuantLib project. This function keeps
    running until catch a KeyboardInterrupt Exception.

    Use terminal command 'autoRQL targetProjectPath' to use this function. The project
    will be built according to the targetProjectPath/config.py in the targetProjectPath.

    After this function is called, the instrument class file and attribute API will be
    automatically generated and updated.

    Parameters
    ----------
    targetPath : str
        A terminal command parameter, specify the RiskQuantLib project path you want to build and render.
    renderFromPath : str
        The path of directory of source file used to render target project.
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
    force : bool
        If True, the cached building file buildInfo.pkl will be deleted, a new builder object will be created.
        This is useful when there are some mistakes in buildInfo.pkl, or error happens when caching buildInfo.pkl.
        In these cases, old buildInfo.pkl exists but can not be used. If this parameter is specified as True, buildInfo.pkl
        will be deleted before auto-building. However, any information in old building will be deleted. If you use
        guardian projects, there could be problems, you will have to build all guardian projects again. Another thing to
        notice is the action of parameter force in autoBuildProject is different with that in buildProject or persistProject.
        buildInfo.pkl will be neglected in buildProject and persistProject, but will be deleted for a single time before
        auto-building.

    Returns
    -------
    None
    """
    if targetPath == '' and renderFromPath == '':
        parser = argparse.ArgumentParser()
        parser.add_argument("targetPath", type=str, help="the RiskQuantLib project you want to build automatically")
        parser.add_argument("-r", "--renderFromPath", type=str, help="the directory of source code where the template code exists")
        parser.add_argument("-c", "--channel", type=str, help="if given a channel name, render action in this channel will not delete the result of render in other channel unless it is overwritten by current render")
        parser.add_argument("-d", "--debug", help="use debug mode, break point in Src will start to effect", action="store_true")
        parser.add_argument("-f", "--force", help="force to build, cached building information will be neglected", action="store_true")
        args = parser.parse_args()
        targetPath = args.targetPath
        renderFromPath = args.renderFromPath
        channel = args.channel
        debug = args.debug
        force = args.force

    import os
    renderFromPath = renderFromPath if renderFromPath else (targetPath + os.sep + "Src")
    bindType = channel if channel else 'renderedSourceCode'
    rqlPath, configFilePath, buildCachePath = parseBuildPath(targetPath, checkExist=True)

    # Delete cached build information if force auto-building
    os.remove(buildCachePath) if force and os.path.isfile(buildCachePath) else None

    # The call back function must be a single parameter function
    def build(projectPath=targetPath):
        try:
            buildProjectFromConfig(targetPath,buildCachePath,configFilePath,renderFromPath, bindType, debug, force=False)
        except Exception as e:
            import time
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "- Build Project Failed: ", e)

    from RiskQuantLib.Tool.fileTool import systemWatcher
    watchObj = systemWatcher([configFilePath, renderFromPath], call_back_function_on_any_change=build, withFormat=True, monitorFormat={'.py','.pyt'})
    watchObj.start()

def unBuildProject(targetPath:str = ''):
    """
    unBuildProject() is a function to un-build RiskQuantLib project.

    Use terminal command 'ubldRQL targetProjectPath' to use this function. The project
    will be un-built and return to the initial status.

    After this function is called, the attribute API will be automatically removed, any all registration
    of instrument will be deleted. But, python source file will not be deleted until you do it by yourself.

    After a project is un-built, you can not use instrument directly in main.py or create new instrument
    inherited from those un-registered instrument. The file config.py will not be
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
    rqlPath, configFilePath, buildCachePath = parseBuildPath(targetPath, checkExist=True)
    from RiskQuantLib.Build.builder import configBuilder
    buildObj = configBuilder.loadInfo(buildCachePath) if os.path.isfile(buildCachePath) else configBuilder(targetProjectPath=targetPath)
    buildObj.clearProject()
    print("Project un-build finished!")


def persistProject(targetPath: str = '', renderFromPath: str = '', channel: str = '', force: bool = False):
    """
    persistProject() is a function to persist RiskQuantLib project.

    Use terminal command 'pstRQL targetProjectPath' to use this function. The project
    will be changed into a permanent project, where all current attribute APIs and instrument registrations
    will not be influenced by build.py anymore.

    This function is like a snapshot of your project, it freezes all effective APIs into permanent ones.

    Surely, you can still build the persisted project with new config.py file.
    Just remember, no matter how many times you build it, the persisted API will remain effective and will not be influenced.

    This command is used when you want to distribute your project to someone else, but you do not want him to change your
    current API. Or this command is used when you are quite sure your current code is stable and can be settled down so that
    you can move on to next stage.

    This command can not be cancelled or un-done, use it carefully.

    Parameters
    ----------
    targetPath : str
        A terminal command parameter, specify the RiskQuantLib project path you want to persist.
    renderFromPath : str
        The path of directory of source file used to render target project.
    channel : str
        render action in this channel will not delete the result of render in other channel
        unless it is overwritten by current render.
    force : bool
        If True, the cached building file buildInfo.pkl will be neglected, a new builder object will be created.
        This is useful when there are some mistakes in buildInfo.pkl, or error happens when caching buildInfo.pkl.
        In these cases, old buildInfo.pkl exists but can not be used. The traditional way to solve this problem is manually
        deleting this file and build whole project again. With this parameter specified as True, users can choose to build
        project no matter buildInfo.pkl exists or not. However, any information in old building will be deleted. If you use
        guardian projects, there could be problems, you will have to build all guardian projects again.

    Returns
    -------
    None
    """
    if targetPath == '' and renderFromPath == '':
        parser = argparse.ArgumentParser()
        parser.add_argument("targetPath", type=str, help="the RiskQuantLib project whose code you want to change into permanent")
        parser.add_argument("-r", "--renderFromPath", type=str, help="the directory of source code where the template code exists")
        parser.add_argument("-c", "--channel", type=str, help="if given a channel name, render action in this channel will not delete the result of render in other channel unless it is overwritten by current render")
        parser.add_argument("-f", "--force", help="force to persist, cached building information will be neglected", action="store_true")
        args = parser.parse_args()
        targetPath = args.targetPath
        renderFromPath = args.renderFromPath
        channel = args.channel
        force = args.force

    import os
    rqlPath, configFilePath, buildCachePath = parseBuildPath(targetPath, checkExist=True)
    renderFromPath = renderFromPath if renderFromPath else (targetPath + os.sep + "Src")
    bindType = channel if channel else 'renderedSourceCode'
    confirm = input("This action can not be Un-Done or Cancelled, do you confirm to continue? (y/n)")
    if confirm.lower()=='y':
        from RiskQuantLib.Build.builder import configBuilder
        buildProject(targetPath,renderFromPath,channel,False,force) if not os.path.isfile(buildCachePath) or force else None
        buildObj = configBuilder.loadInfo(buildCachePath)
        buildObj.persistProject(sourceCodeDirPath=renderFromPath,bindType=bindType)
        configFile = initiateConfigFile()
        configFile.writeToFile(configFilePath)
        print("Project persisted!")
    else:
        print("Action cancelled, nothing changed!")

def copyProject(fromProjectPath: str = '', toProjectPath: str = ''):
    """
    copyProject() is a function to copy RiskQuantLib project to another directory.

    Use terminal command 'copyRQL fromProjectPath toProjectPath' to use this function. The project
    will be copied into the specified directory, if toProjectPath does not exist, it will be created.

    This function will copy every file in current project into new directory except those files which 
    are under path fromProjectPath/RiskQuantLib. If files with the same name already exist in toProjectPath,
    then they will be overwritten, so use it carefully.

    Parameters
    ----------
    fromProjectPath : str
        A terminal command parameter, specify the RiskQuantLib project path you want to copy from.
    toProjectPath : str
        The path where you want to copy RiskQuantLib project to.

    Returns
    -------
    None
    """

    if fromProjectPath == '' and toProjectPath == '':
        parser = argparse.ArgumentParser()
        parser.add_argument("fromProjectPath", type=str, help="the path of RiskQuantLib project which you want to copy files from")
        parser.add_argument("toProjectPath", type=str, help="the path of RiskQuantLib project which you want to copy files into")
        args = parser.parse_args()
        fromProjectPath = args.fromProjectPath
        toProjectPath = args.toProjectPath
    
    import os
    fromProjectPath = os.path.abspath(fromProjectPath)
    toProjectPath = os.path.abspath(toProjectPath)
    if os.path.isdir(fromProjectPath):
        import shutil
        newProject(toProjectPath)
        dirsAndFiles = [(i, fromProjectPath+os.sep+i, toProjectPath+os.sep+i) for i in os.listdir(fromProjectPath)]
        [shutil.copy(f, t) for i, f, t in dirsAndFiles if os.path.isfile(f)]
        [shutil.copytree(f, t, dirs_exist_ok=True) for i, f, t in dirsAndFiles if os.path.isdir(f) and i != 'RiskQuantLib']
        print("Project copied from ", fromProjectPath, " to ", toProjectPath)
    else:
        print("You must specify a validated path which you want to copy files from")
