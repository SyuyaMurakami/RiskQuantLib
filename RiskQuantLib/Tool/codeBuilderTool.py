#!/usr/bin/python
# coding = utf-8

class codeBuilder(object):
    # Build source code conveniently

    def __init__(self, indent = 0, global_indent_step = 0):
        self.INDENT_STEP = 4
        self.code = []
        self.indent_level = indent
        self.ini_indent_level = indent
        self.global_indent_step = global_indent_step

    def __str__(self):
        return ''.join(str(c) for c in self.code)

    def get_globals(self, execute = False):
        # Execute the code, and return a dict of globals if defined

        # A check that caller really finished all the blocks
        assert self.indent_level == self.ini_indent_level
        # Get the Python source as a single string
        self.python_source = str(self)
        if execute:
            # Execute the source, defining globals, and return them.
            global_namespace = {}
            if self.ini_indent_level == 0:
                exec(self.python_source, global_namespace)
            return global_namespace

    def add_line(self, line):
        # Add a line of source to the code.
        # Indentation and new line will be added for you, don't provide them.
        self.code.extend([" " * self.indent_level*(self.global_indent_step+1), line, "\n"])

    def indent(self):
        # Increase the current indent for following lines
        self.indent_level += self.INDENT_STEP

    def dedent(self):
        # Decrease the current indent for following lines
        self.indent_level -= self.INDENT_STEP

    def add_section(self):
        # Add a secton, a sub-CodeBuilder
        section = codeBuilder(self.indent_level)
        self.code.append(section)
        return section

class pythonScriptBuilder():

    def __init__(self):
        self.title = ''
        self.importLibrary = ''

    def setTitle(self, titleString=''):
        if titleString == '':
            self.title = '''#!/usr/bin/python\n# coding = utf-8\n'''
        else:
            self.title = titleString

    def setImport(self, libraryNameString, libraryAbbrString='', importSubModule = False, subModuleName = ''):
        if importSubModule:
            if libraryAbbrString == '':
                self.importLibrary = self.importLibrary + '''from '''+libraryNameString+''' import ''' + subModuleName+'''\n'''
            else:
                self.importLibrary = self.importLibrary + '''from '''+libraryNameString+''' import ''' + subModuleName +''' as '''+libraryAbbrString+ '''\n'''
        else:
            if libraryAbbrString=='':
                self.importLibrary = self.importLibrary + '''import '''+libraryNameString+'''\n'''
            else:
                self.importLibrary = self.importLibrary + '''import ''' + libraryNameString + ''' as '''+libraryAbbrString+'''\n'''

    def startClass(self, classNameString, parentClassName = ''):
        self.classNameString = classNameString
        self.code = codeBuilder(indent=0)

        if parentClassName == '':
            self.code.add_line('''class '''+self.classNameString+'''():''')
        elif type(parentClassName)==type(''):
            self.code.add_line('''class ''' + self.classNameString + '''('''+parentClassName+'''):''')
        else:
            parentClassNameList = "".join([i+',' for i in parentClassName]).strip(',')
            self.code.add_line('''class ''' + self.classNameString + '''(''' + parentClassNameList + '''):''')
        self.code.indent()

        vars_code = self.code.add_section()
        self.code.add_line("def __nullFunction__(self):")
        self.code.indent()
        self.code.add_line("pass")
        self.code.dedent()
        return self.code

    def startFunction(self, functionName, variableName = ''):
        self.functionName = functionName

        if variableName == '':
            self.code.add_line("def " + self.functionName + "(self):")
        elif type(variableName)==type(''):
            self.code.add_line("def " + self.functionName + "(self, "+variableName+"):")
        else:
            variableNameList = "".join([i+',' for i in variableName]).strip(',')
            self.code.add_line("def " + self.functionName + "(self, "+variableNameList+"):")
        self.code.indent()

    def endFunction(self):
        self.functionName = ''
        self.code.dedent()

    def endClass(self):
        self.classNameString = ''
        self.code.dedent()


    def writeToFile(self,filePathString):
        self.code.get_globals()
        content = self.title+self.importLibrary+self.code.python_source
        with open(filePathString, 'w+',encoding="utf-8") as f:
            f.truncate()  # 清空文件内容
            f.write(content.strip(' ').strip('\t\n'))
        print()
