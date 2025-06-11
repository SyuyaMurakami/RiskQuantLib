#!/usr/bin/python
#coding = utf-8
import os,json

import pandas as pd


class builder(object):
    """
    builder is a class to use default render and router to re-construct the whole project.
    Any RiskQuantLib project should have a default builder. You can also add other builders
    to achieve different project mode or use other builder to assist your current project by
    specifying render channel.
    """

    @staticmethod
    def validateStringForJson(string:str):
        """
        This function will parse json like string into a validated json string. All escape character
        will be kept as original form, which is to say, any '\' will not be treated as an escape sign.

        This function is used to parse .pyt file when .pyt file is in a json form and contains file path.
        In windows, these file paths will have '\', and it will be wrongly seen as escape character. This
        function will keep the string as raw string, validateStringForJson(string) equals r'stringContent'.
        """
        escapes = ''.join([chr(char) for char in range(1, 32)])
        translator = str.maketrans('', '', escapes)
        stringWithoutEscape = string.translate(translator)
        return repr(stringWithoutEscape).strip("'")

    @staticmethod
    def checkAndMakeDir(dir:str):
        """
        Make directory recursively if it does not exist.
        """
        if not os.path.exists(dir):
            os.makedirs(dir)

    @staticmethod
    def checkAndMakeDirAndInitiate(dir:str):
        """
        Make directory recursively if it does not exist, then add an __init__.py file in it.
        """
        builder.checkAndMakeDir(dir)
        builder.checkAndMakeFile(dir+os.sep+'__init__.py','')

    @staticmethod
    def checkAndMakeFile(file:str, content:str = ''):
        """
        Make a file is it does not exist, and write content into it.
        """
        if not os.path.exists(file):
            with open(file, 'w+', encoding="utf-8") as f:
                f.truncate()  # clear all contents
                f.write(content)

    @staticmethod
    def formatWarning(message:str, category, filename, lineno, file=None, line=None):
        """
        Make the warning message more readable and neglect the redundant line.
        """
        return '%s:%s: %s: %s\n' % (filename, lineno, category.__name__, message)

    @staticmethod
    def loadInfo(savePath:str = ''):
        """
        Load building cache from a RiskQuantLib project or a .pkl file. If there is not building cache
        in specified path, an exception will be raised.

        Parameters
        ----------
        savePath : str
            The path of building cache .pkl file, or the path of RiskQuantLib project.

        Returns
        -------
        None
        """
        if savePath == '':
            filePath = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'buildInfo.pkl'
        elif os.path.isdir(savePath):
            filePath = savePath + os.sep + "RiskQuantLib" + os.sep + 'Build' + os.sep + 'buildInfo.pkl'
        else:
            filePath = savePath
        if os.path.exists(filePath):
            from RiskQuantLib.Tool.fileTool import loadVariable
            cachedBuilder = loadVariable(filePath)
            cachedBuilder.checkPath() if hasattr(cachedBuilder, 'checkPath') else None
            cachedBuilder.checkRender() if hasattr(cachedBuilder,'checkRender') else None
            return cachedBuilder
        else:
            raise Exception('Load Cache Error: savePath should either be an empty string or a validated RiskQuantLib project dir path or a .pkl file path. If it is a RiskQuantLib project path, make sure there exists savePath/RiskQuantLib/Build/buildInfo.pkl')

    def __init__(self, buildFromProjectPath = '', targetProjectPath:str = '', templateSearchPath:str = ''):
        """
        builder is a class to combine router and render to re-construct the whole project, a project must
        have a default builder. It may also have other builders to construct project by another form.

        Parameters
        ----------
        buildFromProjectPath : str
            The path of builder class, default as Build directory in current project.
        targetProjectPath : str
            The path of target RiskQuantLib project which will be changed according to build information,
            default as current project.
        templateSearchPath : str
            The path of directory where .pyt file for building exists, default as Build/Component in
            current project. If buildFromProjectPath is specified, the default will be
            buildFromProjectPath/Build/Component.

        Returns
        -------
        None
        """
        if targetProjectPath == '':
            self.projectPath = os.path.abspath(__file__).split(os.sep+'RiskQuantLib' + os.sep + 'Build')[0]
            self.targetPath = os.path.abspath(self.projectPath) + os.sep + r'RiskQuantLib'
        else:
            self.projectPath = targetProjectPath
            self.targetPath = targetProjectPath + os.sep + r'RiskQuantLib'
        if buildFromProjectPath == '':
            self.buildFromPath = os.path.abspath(__file__).split(os.sep+os.path.basename(__file__))[0]
        else:
            self.buildFromPath = buildFromProjectPath + os.sep + r'RiskQuantLib' + r'Build'
        if templateSearchPath == '':
            self.templatePath = self.buildFromPath + os.sep + "Component"
        else:
            self.templatePath = templateSearchPath
        self.updateRender()
        from RiskQuantLib.Build.tree import inheritTree
        self.instrumentTree = inheritTree()
        self.propertyTree = inheritTree()
        self.pathRel = {}
        self.pathAbs = {}
        self.dirAbs = {}
        self.instrumentNameList = []
        self.instrumentInheritTreeSeries = []
        self.propertyNameList = []
        self.propertyInheritTreeSeries = []
        self.parentInstrumentNameSeries = []
        self.parentInstrumentInheritListSeries = []
        self.parentPropertyNameSeries = []
        self.parentPropertyInheritListSeries = []
        self.instrumentType = []
        self.parentQuantLibNameSeries = []
        self.dependenceSeries = []
        self.attributeToPropertyDict = []
        self.bindType = {}
        self.linkType = {}

    def initiateInstrumentTree(self):
        """
        Initialize a new inherit tree object to store instrument information, and add default nodes into it.

        Returns
        -------
        None
        """
        from RiskQuantLib.Build.tree import inheritTree
        self.instrumentTree = inheritTree()
        self.instrumentTree.addNode('')
        self.instrumentTree.getNode('').setAttr('type','Instrument')

    def initiatePropertyTree(self):
        """
        Initialize a new inherit tree object to store property type information, and add default nodes into it.

        Returns
        -------
        None
        """
        from RiskQuantLib.Build.tree import inheritTree
        self.propertyTree = inheritTree()
        self.propertyTree.addNode('')
        self.propertyTree.addNode('string').inheritFrom('')
        self.propertyTree.addNode('series').inheritFrom('')
        self.propertyTree.addNode('number').inheritFrom('')

    def initiateProject(self):
        """
        Initialize the project will brand new instrument inherit tree and property inherit tree.
        It will also replace the render object into a new one.

        This function will clear up all current instrument inherit information and property information,
        all current attributes will be removed.

        Returns
        -------
        None
        """
        self.initiateInstrumentTree()
        self.initiatePropertyTree()
        self.updateRender()
        builder.buildProject(self)

    def buildProject(self, dumpCache=True):
        """
        Trigger of building. Call this function will parse instrument inherit tree into validated
        building information, create directory that is needed but does not exist yet, create file that
        is needed but does not exist yet. Generate set attribute function and write them into related
        instrument. And finally, write these change into building cache .pkl file.

        Returns
        -------
        None
        """
        self.updateBuildInfo()
        self.updatePathInfo()
        self.buildDir()
        self.buildFile()
        self.buildContent()
        self.dumpInfo() if dumpCache else None

    def checkPath(self):
        """
        In old versions of RiskQuantLib, if the project and built, and then, the project dir name is changed,
        the builder can not recognize the new project path and will raise an error when you build it again. This function
        is used to check whether the path has been changed. If changed, it will replace the old path into
        the default project path.

        This is the default behavior of RiskQuantLib, if your project does not use many guardians, this default
        setting will be helpful and make it convenient to change project location or run your old project in
        a new computer.

        However, it may cause problem when you use guardian projects. The best way is always un-build a project
        when you want to change its location or rename it, and build it again when rename action is finished. It is
        safer.
        """
        import warnings
        warnings.formatwarning = builder.formatWarning
        pathName = ['Project_Path', 'Target_Path', 'Build_From_Path', 'Template_Path']
        pathAttr = ['projectPath', 'targetPath', 'buildFromPath', 'templatePath']
        pathToBeCheck = [self.projectPath, self.targetPath, self.buildFromPath, self.templatePath]
        pathAlternative = [os.path.abspath(__file__).split(os.sep+'RiskQuantLib' + os.sep + 'Build')[0],
                           os.path.abspath(__file__).split(os.sep+'RiskQuantLib' + os.sep + 'Build')[0] + os.sep + r'RiskQuantLib',
                           os.path.abspath(__file__).split(os.sep + os.path.basename(__file__))[0],
                           os.path.abspath(__file__).split(os.sep + os.path.basename(__file__))[0] + os.sep + "Component"]
        [None if os.path.exists(ptc) else (warnings.warn("\n"+pn+" does NOT exist, it is changed from " + ptc + " into : "+pa), setattr(self, pan, pa)) for pn, ptc, pa, pan in zip(pathName, pathToBeCheck, pathAlternative, pathAttr)]
        self.bindType = {bindType:{pair if os.path.exists(pair[0]) else (self.targetPath+os.sep+pair[0].replace('\\', os.sep).replace('/',os.sep).split(os.sep+'RiskQuantLib'+os.sep)[-1],pair[1]) for pair in self.bindType[bindType]} for bindType in self.bindType}

    def updateRender(self, templateSearchPath:str = ''):
        """
        Change the render into a new one, use specified templateSearchPath.
        templateSearchPath is default as current templateSearchPath.

        Parameters
        ----------
        templateSearchPath : str
            The path of directory where .pyt file for building exists, default as Build/Component in
            current project. If buildFromProjectPath is specified, the default will be
            buildFromProjectPath/Build/Component.

        Returns
        -------
        None
        """
        from RiskQuantLib.Build.render import render
        self.templatePath = self.templatePath if templateSearchPath=='' else templateSearchPath
        self.render = render(self.templatePath)

    def checkRender(self, templateSearchPath:str = ''):
        """
        Change the render into a new one if it does not exist, use specified templateSearchPath.
        templateSearchPath is default as current templateSearchPath.

        Parameters
        ----------
        templateSearchPath : str
            The path of directory where .pyt file for building exists, default as Build/Component in
            current project. If buildFromProjectPath is specified, the default will be
            buildFromProjectPath/Build/Component.

        Returns
        -------
        None
        """
        self.updateRender(templateSearchPath) if not hasattr(self,'render') else None

    def delRender(self):
        """
        Delete the render from current builder. This is the preparation for dumping current
        builder into .pkl file, since render object can not be serialized.

        Returns
        -------
        None
        """
        delattr(self, 'render') if hasattr(self, 'render') else None

    def updateBuildInfo(self):
        """
        Parse instrument inherit tree, property type tree, attribute information and instrument dependency.
        This function will change these information into list to prepare for further render.

        Returns
        -------
        None
        """
        self.instrumentNameList, self.instrumentInheritTreeSeries = self.instrumentTree.getInheritList()
        self.propertyNameList, self.propertyInheritTreeSeries = self.propertyTree.getInheritList()
        self.parentInstrumentNameSeries, self.parentInstrumentInheritListSeries = self.instrumentTree.getParentInheritListSeries()
        self.parentPropertyNameSeries, self.parentPropertyInheritListSeries = self.propertyTree.getParentInheritListSeries()
        self.instrumentType = self.instrumentTree.getAttr('type')
        self.parentQuantLibNameSeries = self.instrumentTree.getAttr('outsideParentNode',[])
        self.dependenceSeries = self.instrumentTree.getAttr('outsideDependence',[])
        self.attributeToPropertyDict = self.instrumentTree.getAttr('attribute',{})

    def updatePathInfo(self):
        """
        Render the filePath.pyt according to current parsed information to generate absolute file path
        and relative file path.

        Returns
        -------
        None
        """
        self.checkRender()
        pathDict = self.render.render('filePath.pyt', instrumentNameList=self.instrumentNameList, instrumentInheritTreeSeries=self.instrumentInheritTreeSeries, propertyNameList=self.propertyNameList, propertyInheritTreeSeries=self.propertyInheritTreeSeries, sep = os.sep)
        self.pathRel = json.loads(builder.validateStringForJson(pathDict))
        self.pathAbs = {pathType:{instrument:self.targetPath+os.sep+self.pathRel[pathType][instrument] for instrument in self.pathRel[pathType]} for pathType in self.pathRel}
        self.dirAbs = {pathType:{instrument:os.path.dirname(self.pathAbs[pathType][instrument]) for instrument in self.pathAbs[pathType]} for pathType in self.pathAbs}

    def buildDir(self):
        """
        Iterate through all instrument and make directory that does not exist yet, then add __init__.py into it.

        Returns
        -------
        None
        """
        [builder.checkAndMakeDirAndInitiate(self.dirAbs[pathType][instrument]) for pathType in self.dirAbs for instrument in self.dirAbs[pathType]]

    def buildFile(self):
        """
        Render initiate .pyt file and write them into related .py file. If .py file already exists, it will be skipped
        and not change. If .py file does not exist, it will be created and initialized.

        Returns
        -------
        None
        """
        self.checkRender()
        if 'instrumentFilePath' in self.pathAbs:
            [builder.checkAndMakeFile(self.pathAbs['instrumentFilePath'][instrument],
                                           self.render.render('instrument.pyt',
                                                              instrumentName=self.instrumentNameList[instrumentId],
                                                              parentInstrumentNameSeries=
                                                              self.parentInstrumentNameSeries[instrumentId],
                                                              inheritList=self.instrumentInheritTreeSeries[
                                                                  instrumentId],
                                                              parentInheritListSeries=self.parentInstrumentInheritListSeries[
                                                                  instrumentId],
                                                              instrumentType=self.instrumentType[instrumentId],
                                                              parentQuantLibInstrumentNameSeries=self.parentQuantLibNameSeries[instrumentId],
                                                              dependenceList = self.dependenceSeries[instrumentId]
                                                              )
                                           ) for instrumentId, instrument in enumerate(self.pathAbs['instrumentFilePath'])]
        if 'instrumentListFilePath' in self.pathAbs:
            [builder.checkAndMakeFile(self.pathAbs['instrumentListFilePath'][instrument],
                                           self.render.render('instrumentList.pyt',
                                                              instrumentName=self.instrumentNameList[instrumentId],
                                                              parentInstrumentNameSeries=
                                                              self.parentInstrumentNameSeries[instrumentId],
                                                              inheritList=self.instrumentInheritTreeSeries[
                                                                  instrumentId],
                                                              parentInheritListSeries=self.parentInstrumentInheritListSeries[
                                                                  instrumentId],
                                                              instrumentType=self.instrumentType[instrumentId],
                                                              dependenceList=self.dependenceSeries[instrumentId]
                                                              )) for instrumentId, instrument in enumerate(self.pathAbs['instrumentListFilePath'])]
        if 'instrumentAutoFilePath' in self.pathAbs:
            [builder.checkAndMakeFile(self.pathAbs['instrumentAutoFilePath'][instrument],
                                           self.render.render('instrumentAuto.pyt',
                                                              instrumentName=self.instrumentNameList[instrumentId],
                                                              parentInstrumentNameSeries=
                                                              self.parentInstrumentNameSeries[instrumentId],
                                                              inheritList=self.instrumentInheritTreeSeries[
                                                                  instrumentId],
                                                              parentInheritListSeries=self.parentInstrumentInheritListSeries[
                                                                  instrumentId],
                                                              instrumentType=self.instrumentType[instrumentId],
                                                              dependenceList=self.dependenceSeries[instrumentId]
                                                              )) for instrumentId, instrument in enumerate(self.pathAbs['instrumentAutoFilePath'])]
        if 'instrumentListAutoFilePath' in self.pathAbs:
            [builder.checkAndMakeFile(self.pathAbs['instrumentListAutoFilePath'][instrument],
                                           self.render.render('instrumentListAuto.pyt',
                                                              instrumentName=self.instrumentNameList[instrumentId],
                                                              parentInstrumentNameSeries=
                                                              self.parentInstrumentNameSeries[instrumentId],
                                                              inheritList=self.instrumentInheritTreeSeries[
                                                                  instrumentId],
                                                              parentInheritListSeries=self.parentInstrumentInheritListSeries[
                                                                  instrumentId],
                                                              instrumentType=self.instrumentType[instrumentId],
                                                              dependenceList=self.dependenceSeries[instrumentId]
                                                              )) for instrumentId, instrument in enumerate(self.pathAbs['instrumentListAutoFilePath'])]
        if 'propertyFilePath' in self.pathAbs:
            [builder.checkAndMakeFile(self.pathAbs['propertyFilePath'][property],
                                           self.render.render('property.pyt',
                                                              propertyName=self.propertyNameList[propertyId],
                                                              parentPropertyNameSeries=
                                                              self.parentPropertyNameSeries[propertyId],
                                                              inheritList=self.propertyInheritTreeSeries[
                                                                  propertyId],
                                                              parentInheritListSeries=self.parentPropertyInheritListSeries[
                                                                  propertyId]
                                                              )) for propertyId, property in enumerate(self.pathAbs['propertyFilePath'])]

    def buildContent(self, persist: bool = False):
        """
        Render set attribute functions and write them into related .py file.

        Parameters
        ----------
        persist : bool
            If true, the current set attribute function will be saved as permanent source code. It will not
            be influenced by building action any more. This action can not be cancelled.

        Returns
        -------
        None
        """
        self.checkRender()
        setAttribute = [self.render.render('setAttribute.pyt', instrumentName=name,
                                           attributeNameList=self.attributeToPropertyDict[idx].keys(),
                                           propertyNameList=list(self.attributeToPropertyDict[idx].values()),
                                           propertyInheritTreeSeries=[self.propertyTree.getNode(prop).inheritTree for
                                                                      prop in
                                                                      self.attributeToPropertyDict[idx].values()]) for
                        idx, name in enumerate(self.instrumentNameList)]
        setAttributeList = [self.render.render('setAttributeList.pyt', instrumentName=name,
                                           attributeNameList=self.attributeToPropertyDict[idx].keys(),
                                           propertyNameList=list(self.attributeToPropertyDict[idx].values()),
                                           defaultValueList=['pd.Series(dtype=float)' if prop=='series' else 'np.nan' for prop in self.attributeToPropertyDict[idx].values()]) for
                        idx, name in enumerate(self.instrumentNameList)]
        shortcutAutoImport = [self.render.render('module.pyt',instrumentNameList = self.instrumentNameList,
                                                 instrumentInheritTreeSeries=self.instrumentInheritTreeSeries,
                                                 propertyNameList = self.propertyNameList,
                                                 propertyInheritTreeSeries = self.propertyInheritTreeSeries)]
        sourceCodeToBeInjected = "\n".join([i for i in setAttribute+setAttributeList+shortcutAutoImport if i!=''])
        self.bindContent(sourceCodeToBeInjected, bindType="setAttribute",persist=persist)


    def bindContent(self, sourceCodeToBeInjected:str, bindType:str, persist:bool = False):
        """
        Parse the source code, find where the code should be injected into, and inject them.

        Parameters
        ----------
        sourceCodeToBeInjected : str
            Content of python source code, with comment used as control syntax
        bindType : str
            The type of binding action. Different bind type will be saved into different channel.
            Binding action in one channel will not influence one in another channel, unless it
            overwrites the same tag.
        persist : bool
            If true, the current source code will be saved as permanent source code. It will not
            be influenced by building action any more. This action can not be cancelled.

        Returns
        -------
        None
        """
        from RiskQuantLib.Build.router import router
        syntacticSugarPathMap = {}
        [syntacticSugarPathMap.update(self.pathRel[dictType]) for dictType in self.pathRel]
        injectDict = router.parseInjectTarget(sourceCodeToBeInjected, self.targetPath, syntacticSugarPathMap)

        alreadyBoundTag = self.bindType[bindType] if bindType in self.bindType else set()
        aliveRenderTag = set([(file, tag) for file in injectDict for tag in injectDict[file]])
        deprecatedRenderTag = alreadyBoundTag - aliveRenderTag
        deprecatedRenderTagDF = pd.DataFrame([(i[0],i[1],'') for i in deprecatedRenderTag],columns=['file','tag','content'])
        deprecatedInjectDict = deprecatedRenderTagDF.groupby('file').apply(lambda x:dict(zip(x['tag'],x['content']))).to_dict() if deprecatedRenderTagDF.shape[0]!=0 else {}
        [injectDict[file].update(deprecatedInjectDict[file]) for file in injectDict if file in deprecatedInjectDict]
        [injectDict.update({file:deprecatedInjectDict[file]}) for file in deprecatedInjectDict if file not in injectDict]
        self.bindType[bindType] = set() if persist else aliveRenderTag

        [router.persistToFile(file, **(injectDict[file])) if persist else router.injectToFile(file, **(injectDict[file])) for file in injectDict]

    def linkContent(self, content:str, linkType:str):
        """
        This function will use control declaration in source code to build the whole project again. Any instrument that
        is required by source code will be created, any attribute this is needed will be added. These actions will be operated
        on an independent builder named as mimicBuilder, which is the update version of base builder.
        """
        from RiskQuantLib.Build.controller import controller
        controlSyntaxListUpdate = controller.findDeclareTag(content)
        if len(controlSyntaxListUpdate)!=0:
            self.linkType[linkType] = controlSyntaxListUpdate
            controlSyntaxListSorted = [self.linkType[i] for i in self.linkType if i!=linkType]+[controlSyntaxListUpdate]
            controlSyntaxListMerged = [j for i in controlSyntaxListSorted for j in i]
            controller.linkController(self, controlSyntaxListMerged)

    def renderProject(self, sourceCodeDirPath: str = '', bindType: str = 'renderedSourceCode', persist: bool = False, debug: bool = False, **kwargs):
        """
        Render and inject source code into target project.

        Parameters
        ----------
        sourceCodeDirPath : str
            The path of directory where source code exist. Any sub file in this folder or sub-folder
            will be rendered and parsed.
        bindType : str
            The channel of binding action. Source code are rendered and injected into project by different channels,
            The source code injected by channel A will be not influenced by source code injected by channel B, unless
            the content of tag is overwritten by code in channel B. This is used when you have several builders and
            you want them to build into the same project. In this case, you should give a bindType for each render action
            to make sure they do not conflict with each other.
        persist : bool
            If true, the current source code will be saved as permanent source code. It will not
            be influenced by building action any more. This action can not be cancelled.
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
        self.checkRender()
        sourceCodeDirPath = self.projectPath+os.sep+"Src" if sourceCodeDirPath == '' else sourceCodeDirPath
        if os.path.isdir(sourceCodeDirPath):
            from RiskQuantLib.Build.render import render
            from RiskQuantLib.Build.router import router
            from RiskQuantLib.Build.debugger import debugger
            sourceCodeRender = render(sourceCodeDirPath)
            content = []
            for root, dirs, files in os.walk(sourceCodeDirPath):
                contentAndType = [(router.readContent(root+os.sep+file), file, os.path.splitext(file)[-1]) for file in files if os.path.splitext(file)[-1] in {'.pyt','.py'}]
                contentRendered = [sourceCodeRender.render(file,**kwargs) if ext == '.pyt' else self.render.render('sourceCodeDebugger.pyt',srcPath=root+os.sep+file, **(debugger.splitSrcByChunkAndFindThoseCanBeDebugged(content))) if debug else content for content, file, ext in contentAndType]
                contentMerged = "#-><FileStart>\n"+"\n#-><FileEnd>\n#-><FileStart>\n".join(contentRendered)+"\n#-><FileEnd>"
                content.append(contentMerged)
            contentBind = "\n".join(content)
            self.linkContent(contentBind, linkType=bindType)
            self.mimicBuilder.bindContent(contentBind, bindType=bindType, persist=persist) if hasattr(self,'mimicBuilder') and isinstance(self.mimicBuilder,builder) else self.bindContent(contentBind, bindType=bindType, persist=persist)
            self.dumpInfo()

    def clearProject(self):
        """
        Clear any code generated by building and render action. But it will not delete .py file.

        Returns
        -------
        None
        """
        self.initiateProject()
        [self.bindContent("", bindType=bt, persist=False) for bt in self.bindType]
        [self.mimicBuilder.bindContent("", bindType=bt, persist=False) for bt in self.mimicBuilder.bindType] if hasattr(self,'mimicBuilder') and isinstance(self.mimicBuilder,builder) else None
        self.dumpInfo()

    def persistProject(self, sourceCodeDirPath: str = '', bindType: str = 'renderedSourceCode'):
        """
        Build and render current project according to current information, and turn the generated
        code into permanent code. These code will not be influenced by any building action any more.

        Parameters
        ----------
        sourceCodeDirPath : str
            The path of directory where source code exist. Any sub file in this folder or sub-folder
            will be rendered and parsed and injected to target project.
        bindType : str
            The channel of binding action. Source code are rendered and injected into project by different channels,
            The source code injected by channel A will be not influenced by source code injected by channel B, unless
            the content of tag is overwritten by code in channel B. This is used when you have several builders and
            you want them to build into the same project. In this case, you should give a bindType for each render action
            to make sure they do not conflict with each other.

        Returns
        -------
        None
        """
        self.updateBuildInfo()
        self.updatePathInfo()
        self.buildDir()
        self.buildFile()
        self.buildContent(persist=True)
        self.renderProject(sourceCodeDirPath=sourceCodeDirPath,bindType=bindType,persist=True)
        self.dumpInfo()

    def dumpInfo(self, savePath:str = ''):
        """
        Dump current builder into disk.

        Returns
        -------
        None
        """
        from RiskQuantLib.Tool.fileTool import dumpVariable
        targetPath = self.targetPath+os.sep+'Build'+os.sep+'buildInfo.pkl' if savePath=='' else savePath
        builder.checkAndMakeDir(os.path.dirname(targetPath))
        self.delRender()
        dumpVariable(self,targetPath)
        
        
class validateBuilder(builder):
    """
    validateBuilder is a child class of builder, it will parse the information, screen out those
    wrong syntax and pass validated information to base builder.
    """
    @staticmethod
    def lowerCaseFirstLetter(string:str):
        return string[0].lower() + string[1:] if string else string

    @staticmethod
    def upperCaseFirstLetter(string:str):
        return string[0].upper() + string[1:] if string else string

    @staticmethod
    def isString(string, allowComma:bool = True, allowEmpty:bool = True, allowSpace:bool = True):
        return (type(string)==str) and (True if allowComma else string.find(',')==-1) and (True if allowEmpty else string!='') and (True if allowSpace else string.find(' ')==-1)

    @staticmethod
    def validateString(string:str, lowerCaseFirstLetter = True):
        """
        Strip any blank in string, if comma exists in string, split string according to comma, then
        strip any blank in every sub-string.

        If lowerCaseFirstLetter is True, the first letter of every sub-string will be changed into
        lower-case letter.
        """
        if type(string)!=str:
            return ''
        stringList = [i.strip(' ') for i in string.split(',')]
        stringList = [validateBuilder.lowerCaseFirstLetter(i) if lowerCaseFirstLetter else i for i in stringList]
        if len(stringList)==0:
            return ''
        elif len(stringList)==1:
            return stringList[0]
        else:
            return stringList

    @staticmethod
    def validateParentClassName(parentClass:str or list, inheritTreeNodeDict:dict):
        """
        If class name in inheritTreeNodeDict, return it. Otherwise, parent class will
        be root instrument, and parent class is defaulted as blank string.
        """
        classList = [parentClass] if type(parentClass)==str else parentClass
        validatedClass = [i for i in classList if i in inheritTreeNodeDict]
        return '' if len(validatedClass)==0 else validatedClass

    @staticmethod
    def validateRootInstrumentName(instrumentName:str, rootInstrumentName:set):
        """
        You can have some words who have the same meaning with root instrument name. This function
        is used to identify those words.

        If instrumentName in rootInstrumentName, return default root instrument name, which is blank string.
        otherwise, return instrumentName itself.
        """
        return '' if validateBuilder.isString(instrumentName,allowComma=False) and (validateBuilder.validateString(instrumentName) in rootInstrumentName) else instrumentName

    def __init__(self, buildFromProjectPath = '', targetProjectPath:str = '', templateSearchPath:str = ''):
        super(validateBuilder, self).__init__(buildFromProjectPath = buildFromProjectPath, targetProjectPath= targetProjectPath, templateSearchPath = templateSearchPath)

    def initiateTree(self):
        self.initiateInstrumentTree()
        self.initiatePropertyTree()

    def validateTree(self, instrumentName:list = [], parentRQLClassName:list = [], parentQuantLibClassName:list = [], libraryName:list = [], defaultInstrumentType:list = [], attributeBelongTo:list = [], attributeName:list = [], propertyName:list = []):
        # change some word into empty string, because these words have the same meaning with root instrument.
        rootInstrumentName = set(['instrument','any'])
        instrumentName = [validateBuilder.validateRootInstrumentName(ins,rootInstrumentName) for ins in instrumentName]
        attributeBelongTo = [validateBuilder.validateRootInstrumentName(ins,rootInstrumentName) for ins in attributeBelongTo]
        # add new instrument
        validatedInstrument = [(validateBuilder.validateString(ins),validateBuilder.validateString(prc),validateBuilder.validateString(pqc, lowerCaseFirstLetter=False),validateBuilder.validateString(ln, lowerCaseFirstLetter=False),validateBuilder.validateString(dt, lowerCaseFirstLetter=False) if dt else validateBuilder.upperCaseFirstLetter(ins)) for ins,prc,pqc,ln,dt in zip(instrumentName,parentRQLClassName,parentQuantLibClassName,libraryName,defaultInstrumentType) if validateBuilder.isString(ins,allowEmpty=False,allowComma=False) and validateBuilder.validateString(ins) not in self.instrumentTree.nodeDict]
        [self.instrumentTree.addNode(ins).inheritFrom(prc).setAttr('type', dt).inheritFromOutside(pqc).dependOnOutside(ln) for ins,prc,pqc,ln,dt in validatedInstrument]
        # add new property
        validatedProperty = [validateBuilder.validateString(property) for property in propertyName if type(property)==str and property!='' and property.find(',')==-1]
        [self.propertyTree.addNode(name).inheritFrom('') for name in validatedProperty]
        # set attribute to instrument
        validatedAttribute = [(validateBuilder.validateString(instrument),validateBuilder.validateString(attribute),validateBuilder.validateString(attributeType)) for instrument,attribute,attributeType in zip(attributeBelongTo,attributeName,propertyName) if validateBuilder.isString(instrument,allowComma=False) and validateBuilder.isString(attribute,allowEmpty=False,allowComma=False) and validateBuilder.isString(attributeType,allowComma=False)]
        [self.instrumentTree.getNode(instrument).addAttr('attribute',attribute,attributeType) if instrument in self.instrumentTree.nodeDict and attributeType in self.propertyTree.nodeDict else None for instrument,attribute,attributeType in validatedAttribute]

    def buildProject(self, instrumentName:list = [], parentRQLClassName:list = [], parentQuantLibClassName:list = [], libraryName:list = [], defaultInstrumentType:list = [], attributeBelongTo:list = [], attributeName:list = [], propertyName:list = []):
        self.initiateTree()
        self.validateTree(instrumentName=instrumentName,parentRQLClassName=parentRQLClassName,parentQuantLibClassName=parentQuantLibClassName,libraryName=libraryName,defaultInstrumentType=defaultInstrumentType,attributeBelongTo=attributeBelongTo,attributeName=attributeName,propertyName=propertyName)
        super(validateBuilder, self).buildProject()

class dataframeBuilder(validateBuilder):
    """
    dataframeBuilder is a child class of validatedBuilder, it takes two pandas.DataFrame as information of building.
    """
    def __init__(self, buildFromProjectPath = '', targetProjectPath:str = '', templateSearchPath:str = ''):
        super(dataframeBuilder, self).__init__(buildFromProjectPath = buildFromProjectPath, targetProjectPath= targetProjectPath, templateSearchPath = templateSearchPath)
        self.buildFileInfo = {}
        self.buildContentInfo = {}

    def setInstrumentInfo(self, df:pd.DataFrame, colAsInstrumentName:str = 'InstrumentName', colAsParentRQLClassName:str = 'ParentRQLClassName', colAsParentQuantLibClassName:str = 'ParentQuantLibClassName', colAsLibraryName:str = 'LibraryName', colAsDefaultInstrumentType:str = 'DefaultInstrumentType'):
        """
        Pass a pandas.DataFrame into this function to use it as instrument building information.
        """
        buildInstrumentInfo = df.dropna(subset=[colAsInstrumentName]).fillna('')
        self.buildFileInfo = {'instrumentName':buildInstrumentInfo[colAsInstrumentName].to_list(),
                                    'parentRQLClassName':buildInstrumentInfo[colAsParentRQLClassName].to_list(),
                                    'parentQuantLibClassName':buildInstrumentInfo[colAsParentQuantLibClassName].to_list(),
                                    'libraryName':buildInstrumentInfo[colAsLibraryName].to_list(),
                                    'defaultInstrumentType':buildInstrumentInfo[colAsDefaultInstrumentType].to_list()}

    def setAttributeInfo(self, df:pd.DataFrame, colAsInstrumentName:str = 'SecurityType', colAsAttributeName:str = 'AttrName', colAsPropertyName:str = 'AttrType'):
        """
        Pass a pandas.DataFrame into this function to use it as attribute building information.
        """
        buildAttributeInfo = df.dropna(subset=[colAsAttributeName]).fillna('')
        self.buildContentInfo = {'attributeBelongTo':buildAttributeInfo[colAsInstrumentName].to_list(),
                                  'attributeName':buildAttributeInfo[colAsAttributeName].to_list(),
                                  'propertyName':buildAttributeInfo[colAsPropertyName].to_list()}

    def buildProject(self):
        super(dataframeBuilder, self).buildProject(**self.buildFileInfo,**self.buildContentInfo)


class stringBuilder(dataframeBuilder):
    """
    stringBuilder is a child class of validatedBuilder, it takes string as information of building.
    """
    def __init__(self, buildFromProjectPath='', targetProjectPath: str = '', templateSearchPath: str = ''):
        super(stringBuilder, self).__init__(buildFromProjectPath=buildFromProjectPath, targetProjectPath=targetProjectPath, templateSearchPath=templateSearchPath)

    def buildProject(self, content: str):
        from RiskQuantLib.Build.controller import controller
        controlSyntaxList = controller.findDeclareTag(content)
        buildInstrument, buildAttr, buildOther = controller.parseDeclareTagAsDF(controlSyntaxList)
        self.setInstrumentInfo(buildInstrument)
        self.setAttributeInfo(buildAttr)
        super(stringBuilder, self).buildProject()

class configBuilder(stringBuilder):
    """
    configBuilder is a child class of stringBuilder, it takes config.py as information of building.
    """
    def __init__(self, buildFromProjectPath='', targetProjectPath: str = '', templateSearchPath: str = ''):
        super(stringBuilder, self).__init__(buildFromProjectPath=buildFromProjectPath, targetProjectPath=targetProjectPath, templateSearchPath=templateSearchPath)

    def buildProject(self, configFilePath: str):
        from RiskQuantLib.Build.router import router
        content = router.readContent(configFilePath)
        super(configBuilder, self).buildProject(content)

class excelBuilder(dataframeBuilder):
    """
    excelBuilder is a child class of dataframeBuilder, it takes two xlsx file as information of building.
    """
    def __init__(self, buildFromProjectPath = '', targetProjectPath:str = '', templateSearchPath:str = ''):
        super(excelBuilder, self).__init__(buildFromProjectPath = buildFromProjectPath, targetProjectPath= targetProjectPath, templateSearchPath = templateSearchPath)

    def buildProject(self, instrumentExcelPath:str, attributeExcelPath:str, colAsInstrumentNameForInstrumentDF:str = 'InstrumentName', colAsParentRQLClassNameForInstrumentDF:str = 'ParentRQLClassName', colAsParentQuantLibClassNameForInstrumentDF:str = 'ParentQuantLibClassName', colAsLibraryNameForInstrumentDF:str = 'LibraryName', colAsDefaultInstrumentTypeForInstrumentDF:str = 'DefaultInstrumentType', colAsInstrumentNameForAttributeDF:str = 'SecurityType', colAsAttributeNameForAttributeDF:str = 'AttrName', colAsPropertyNameForAttributeDF:str = 'AttrType'):
        buildInstrumentInfo = pd.read_excel(instrumentExcelPath,dtype=str)
        buildAttributeInfo = pd.read_excel(attributeExcelPath,dtype=str)
        self.setInstrumentInfo(buildInstrumentInfo,colAsInstrumentNameForInstrumentDF,colAsParentRQLClassNameForInstrumentDF,colAsParentQuantLibClassNameForInstrumentDF,colAsLibraryNameForInstrumentDF,colAsDefaultInstrumentTypeForInstrumentDF)
        self.setAttributeInfo(buildAttributeInfo,colAsInstrumentNameForAttributeDF,colAsAttributeNameForAttributeDF,colAsPropertyNameForAttributeDF)
        super(excelBuilder, self).buildProject()

class databaseBuilder(dataframeBuilder):
    """
    databaseBuilder is a child class of dataframeBuilder, you should pass two
    sql syntax and a connection object into this class to classify building information.
    """
    def __init__(self, buildFromProjectPath = '', targetProjectPath:str = '', templateSearchPath:str = ''):
        super(databaseBuilder, self).__init__(buildFromProjectPath = buildFromProjectPath, targetProjectPath= targetProjectPath, templateSearchPath = templateSearchPath)

    def buildProject(self, instrumentSql:str, attributeSql:str, con, colAsInstrumentNameForInstrumentDF:str = 'InstrumentName', colAsParentRQLClassNameForInstrumentDF:str = 'ParentRQLClassName', colAsParentQuantLibClassNameForInstrumentDF:str = 'ParentQuantLibClassName', colAsLibraryNameForInstrumentDF:str = 'LibraryName', colAsDefaultInstrumentTypeForInstrumentDF:str = 'DefaultInstrumentType', colAsInstrumentNameForAttributeDF:str = 'SecurityType', colAsAttributeNameForAttributeDF:str = 'AttrName', colAsPropertyNameForAttributeDF:str = 'AttrType'):
        buildInstrumentInfo = pd.read_sql(instrumentSql, con)
        buildAttributeInfo = pd.read_sql(attributeSql, con)
        self.setInstrumentInfo(buildInstrumentInfo,colAsInstrumentNameForInstrumentDF,colAsParentRQLClassNameForInstrumentDF,colAsParentQuantLibClassNameForInstrumentDF,colAsLibraryNameForInstrumentDF,colAsDefaultInstrumentTypeForInstrumentDF)
        self.setAttributeInfo(buildAttributeInfo,colAsInstrumentNameForAttributeDF,colAsAttributeNameForAttributeDF,colAsPropertyNameForAttributeDF)
        super(databaseBuilder, self).buildProject()
