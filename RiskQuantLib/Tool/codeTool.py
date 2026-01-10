#!/usr/bin/python
# coding = utf-8

#<import>
#</import>

class codeBuilder(object):
    """
    This class is the basic class used to generate source code of any language.
    """

    def __init__(self, indent = 0, globalIndentStep = 0):
        self.INDENT_STEP = 4
        self.code = []
        self.indentLevel = indent
        self.iniIndentLevel = indent
        self.globalIndentStep = globalIndentStep
        self.source = ''

    def __str__(self):
        return ''.join(str(c) for c in self.code)

    def addLine(self, line:str):
        # Add a line of source to the code.
        # Indentation and new line will be added for you, don't provide them.
        self.code.extend([" " * self.indentLevel*(self.globalIndentStep+1), line, "\n"])

    def indent(self):
        # Increase the current indent for following lines
        self.indentLevel += self.INDENT_STEP

    def dedent(self):
        # Decrease the current indent for following lines
        self.indentLevel -= self.INDENT_STEP

    def addSection(self):
        # Add a section, a sub-CodeBuilder
        section = codeBuilder(self.indentLevel)
        self.code.append(section)
        return section
    
    def getGlobals(self):
        # Turn all blocks into code string.
        # A check that caller really finished all the blocks
        assert self.indentLevel == self.iniIndentLevel
        # Get the Python source as a single string
        self.source = str(self)

    #<codeBuilder>
    #</codeBuilder>


class codeBuilderPython(codeBuilder):

    def addSection(self):
        # Add a section, a sub-CodeBuilder
        section = codeBuilderPython(self.indentLevel)
        self.code.append(section)
        return section

    def getGlobals(self, execute = False):
        super().getGlobals()
        if execute:
            # Execute the source, defining globals, and return them.
            globalNameSpace = {}
            if self.iniIndentLevel == 0:
                exec(self.source, globalNameSpace)
            return globalNameSpace
    
    #<codeBuilderPython>
    #</codeBuilderPython>


class pythonScriptBuilder(object):
    """
    This class is the python source code builder, used to generate python
    source code automatically.
    """
    def __init__(self):
        self.title = ''
        self.importLibrary = ''
        self.className = ''
        self.functionName = ''
        self.source = ''
        self.code = None

    def setTitle(self, title: str = ''):
        """
        Set python source file title, including coding method and python version.
        """
        if title == '':
            self.title = '''#!/usr/bin/python\n# coding = utf-8\n'''
        else:
            self.title = title

    def setImport(self, libraryName: str, libraryAbbr: str = '', importSubModule: bool = False, subModuleName: str = ''):
        """
        Import a module to python source file.

        Parameters
        ----------
        libraryName : str
            The library name you want to import.
        libraryAbbr : str
            If not blank, library will be imported with the form 'import libraryName as libraryAbbr'
        importSubModule : bool
            If True, library will be imported with the form 'from libraryName import subModuleName
            as libraryAbbr'
        subModuleName : str
            If not blank and importSubModule is true, library will be imported with the form 'from
            libraryName import subModuleName as libraryAbbr'

        Returns
        -------
        None
        """
        if importSubModule:
            if libraryAbbr == '':
                self.importLibrary = self.importLibrary + '''from '''+libraryName+''' import ''' + subModuleName+'''\n'''
            else:
                self.importLibrary = self.importLibrary + '''from '''+libraryName+''' import ''' + subModuleName +''' as '''+libraryAbbr+ '''\n'''
        else:
            if libraryAbbr=='':
                self.importLibrary = self.importLibrary + '''import '''+libraryName+'''\n'''
            else:
                self.importLibrary = self.importLibrary + '''import ''' + libraryName + ''' as '''+libraryAbbr+'''\n'''

    def startClass(self, className: str, parentClassName: str = ''):
        """
        Start a new class. This function must be followed by endClass()
        """
        self.className = className
        self.code = codeBuilderPython(indent=0)

        if parentClassName == '':
            self.code.addLine('''class '''+self.className+'''():''')
        elif type(parentClassName)==type(''):
            self.code.addLine('''class ''' + self.className + '''('''+parentClassName+'''):''')
        else:
            parentClassNameList = "".join([i+',' for i in parentClassName]).strip(',')
            self.code.addLine('''class ''' + self.className + '''(''' + parentClassNameList + '''):''')
        self.code.indent()
        self.code.addLine("def __nullFunction__(self):")
        self.code.indent()
        self.code.addLine("pass")
        self.code.dedent()
        return self.code

    def startFunction(self, functionName: str, variableName: str = ''):
        """
        Start a function. This function must be followed by endFunction()
        """
        self.functionName = functionName

        if variableName == '':
            self.code.addLine("def " + self.functionName + "(self):")
        elif type(variableName)==type(''):
            self.code.addLine("def " + self.functionName + "(self, "+variableName+"):")
        else:
            variableNameList = "".join([i+',' for i in variableName]).strip(',')
            self.code.addLine("def " + self.functionName + "(self, "+variableNameList+"):")
        self.code.indent()

    def endFunction(self):
        """
        Specify the end of a function.
        """
        self.functionName = ''
        self.code.dedent()

    def endClass(self):
        """
        Specify the end of a class.
        """
        self.className = ''
        self.code.dedent()

    def getSource(self):
        """
        Get source code string.
        """
        self.code.getGlobals()
        self.source = self.title+self.importLibrary+self.code.source

    def writeToFile(self,filePathString: str):
        """
        Output the source code to a file, use mode 'w+'.
        """
        self.getSource()
        with open(filePathString, 'w+',encoding="utf-8") as f:
            f.truncate()  # clear all contents
            f.write(self.source.strip(' ').strip('\t\n'))

    #<pythonScriptBuilder>
    #</pythonScriptBuilder>


#<codeTool>
#</codeTool>
