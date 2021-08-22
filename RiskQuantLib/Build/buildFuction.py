#!/usr/bin/python
#coding = utf-8

def buildStringFunction(variableNameString):
    from RiskQuantLib.Tool.codeBuilderTool import codeBuilder

    code = codeBuilder(indent=4)

    code.add_line("def set"+variableNameString[0].capitalize()+variableNameString[1:]+"(self, "+variableNameString+"String):")
    code.indent()
    vars_code = code.add_section()
    code.add_line("self."+variableNameString+" = "+variableNameString+"String")
    code.dedent()
    code.get_globals()
    return code


def buildNumberFunction(variableNameString):
    from RiskQuantLib.Tool.codeBuilderTool import codeBuilder

    code = codeBuilder(indent=4)

    code.add_line("def set"+variableNameString[0].capitalize()+variableNameString[1:]+"(self, "+variableNameString+"Num):")
    code.indent()
    vars_code = code.add_section()
    code.add_line("from RiskQuantLib.Property.NumberProperty.numberProperty import numberProperty")
    code.add_line("if not hasattr(self, '__"+variableNameString+"'):")
    code.indent()
    code.add_line("self.__"+variableNameString+" = numberProperty("+variableNameString+"Num)")
    code.add_line("self."+variableNameString+" = self.__"+variableNameString+".value")
    code.dedent()
    code.add_line("else:")
    code.indent()
    code.add_line("self.__"+variableNameString+".setValue("+variableNameString+"Num)")
    code.add_line("self."+variableNameString+" = self.__"+variableNameString+".value")
    code.dedent()

    code.dedent()
    code.get_globals()
    return code

def buildBaseFunction(variableNameString):
    from RiskQuantLib.Tool.codeBuilderTool import codeBuilder

    code = codeBuilder(indent=4)

    code.add_line("def set"+variableNameString[0].capitalize()+variableNameString[1:]+"(self, "+variableNameString+"):")
    code.indent()
    vars_code = code.add_section()
    code.add_line("from RiskQuantLib.Property.base import base")
    code.add_line("if not hasattr(self, '__"+variableNameString+"'):")
    code.indent()
    code.add_line("self.__"+variableNameString+" = base("+variableNameString+")")
    code.add_line("self."+variableNameString+" = self.__"+variableNameString+".value")
    code.dedent()
    code.add_line("else:")
    code.indent()
    code.add_line("self.__"+variableNameString+".setValue("+variableNameString+")")
    code.add_line("self."+variableNameString+" = self.__"+variableNameString+".value")
    code.dedent()

    code.dedent()
    code.get_globals()
    return code

def commitObjectFunctionBuild(codeList,sourceFilePath):
    sourceCodeList = [i.python_source for i in codeList]
    sourceCode = "".join(sourceCodeList)

    with open(sourceFilePath, 'r') as f:
        content = f.read()

    if content.find('#-<End>') == -1 or content.find('#-<End>') == -1:
        print("Source file must have a #-<Begin> and #-<End> tag to be built")
        exit(-1)

    former = content.split('#-<Begin>')[0]
    ender = content.split('#-<End>')[-1]
    newContent = former + '#-<Begin>\n' + sourceCode + '    #-<End>\n\t' + ender
    with open(sourceFilePath, 'w') as f:
        f.truncate()  # 清空文件内容
        f.write(newContent.strip(' ').strip('\t\n'))
    print()


def buildListSetFunction1D(variableNameString,variableType = 'Base'):
    from RiskQuantLib.Tool.codeBuilderTool import codeBuilder

    code = codeBuilder(indent=4)

    code.add_line("def set"+variableNameString[0].capitalize()+variableNameString[1:]+"(self,codeSeries,"+variableNameString+"Series):")
    code.indent()
    vars_code = code.add_section()
    code.add_line(variableNameString+"Dict = dict(zip(codeSeries,"+variableNameString+"Series))")
    if variableType == 'Str':
        code.add_line("[i.set"+variableNameString[0].capitalize()+variableNameString[1:]+"("+variableNameString+"Dict[i.code]) if i.code in "+variableNameString+"Dict.keys() else i.set"+variableNameString[0].capitalize() + variableNameString[1:]+"('') for i in self.all]")
    elif variableType == 'Num':
        code.add_line("import numpy as np")
        code.add_line("[i.set" + variableNameString[0].capitalize() + variableNameString[1:] + "(" + variableNameString + "Dict[i.code]) if i.code in " + variableNameString + "Dict.keys() else i.set" + variableNameString[0].capitalize() + variableNameString[1:] + "(np.nan) for i in self.all]")
    elif variableType == 'Base':
        code.add_line("[i.set" + variableNameString[0].capitalize() + variableNameString[1:] + "(" + variableNameString + "Dict[i.code]) if i.code in " + variableNameString + "Dict.keys() else i.set" + variableNameString[0].capitalize() + variableNameString[1:] + "(np.nan) for i in self.all]")
    else:
        print("Variable type must be set as 'Str', 'Num' or 'Base'")
        exit(-1)
    code.dedent()
    code.get_globals()
    return code

def buildListSetFunction2D(variableNameString):
    from RiskQuantLib.Tool.codeBuilderTool import codeBuilder

    code = codeBuilder(indent=4)

    code.add_line("def set"+variableNameString[0].capitalize()+variableNameString[1:]+"(self,"+variableNameString+"DataFrame):")
    code.indent()
    vars_code = code.add_section()
    code.add_line("import pandas as pd")
    code.add_line(variableNameString+"CodeList = "+variableNameString+"DataFrame.columns.to_list()")
    code.add_line("[i.set"+variableNameString[0].capitalize()+variableNameString[1:]+"("+variableNameString+"DataFrame[i.code]) if hasattr(i,'code') and i.code in "+variableNameString+"CodeList else i.set"+variableNameString[0].capitalize()+variableNameString[1:]+"(pd.Series()) for i in self.all]")
    code.dedent()
    code.get_globals()
    return code


def commitListFunctionBuild(codeList,sourceFilePath):
    sourceCodeList = [i.python_source for i in codeList]
    sourceCode = "".join(sourceCodeList)

    with open(sourceFilePath, 'r') as f:
        content = f.read()

    if content.find('#-<End>') == -1 or content.find('#-<End>') == -1:
        print("Source file must have a #-<Begin> and #-<End> tag to be built")
        exit(-1)

    former = content.split('#-<Begin>')[0]
    ender = content.split('#-<End>')[-1]
    newContent = former + '#-<Begin>\n' + sourceCode + '    #-<End>\n\t' + ender
    with open(sourceFilePath, 'w') as f:
        f.truncate()  # 清空文件内容
        f.write(newContent.strip(' ').strip('\t\n'))
    # print()

def clearBuiltFunction(sourceFilePath):
    with open(sourceFilePath, 'r') as f:
        content = f.read()

    if content.find('#-<End>') == -1 or content.find('#-<End>') == -1:
        print("Source file must have a #-<Begin> and #-<End> tag to be built")
        exit(-1)

    former = content.split('#-<Begin>')[0]
    ender = content.split('#-<End>')[-1]
    newContent = former + '#-<Begin>\n    #-<End>\n\t' + ender
    with open(sourceFilePath, 'w') as f:
        f.truncate()  # 清空文件内容
        f.write(newContent.strip(' ').strip('\t\n'))
    # print()



















