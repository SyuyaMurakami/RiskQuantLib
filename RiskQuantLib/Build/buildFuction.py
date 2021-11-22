#!/usr/bin/python
#coding = utf-8

def buildStringFunction(variableNameString:str):
    """
    buildStringFunction(variableNameString:str) is a function to automatically build a set function,
    given the variable type as 'String'.
    This function returns a codeBuilder object.

    Parameters
    ----------
    variableNameString : str
        The variable name you want to use.
        This name will be used as attribute name of class.

    Returns
    -------
    code : codeBuilder Object
    """
    from RiskQuantLib.Tool.codeBuilderTool import codeBuilder

    code = codeBuilder(indent=4)

    code.add_line("def set"+variableNameString[0].capitalize()+variableNameString[1:]+"(self, "+variableNameString+"String):")
    code.indent()
    vars_code = code.add_section()
    code.add_line("self."+variableNameString+" = "+variableNameString+"String")
    code.dedent()
    code.get_globals()
    return code


def buildNumberFunction(variableNameString:str):
    """
    buildNumberFunction(variableNameString:str) is a function to automatically build a set function,
    given the variable type as 'Number'.
    This function will import a number instance from RiskQuantLib.Property.NumberProperty.numberProperty,
    and returns a codeBuilder object.

    Parameters
    ----------
    variableNameString : str
        The variable name you want to use.
        This name will be used as attribute name of class.

    Returns
    -------
    code : codeBuilder Object
    """
    from RiskQuantLib.Tool.codeBuilderTool import codeBuilder

    code = codeBuilder(indent=4)

    code.add_line("def set"+variableNameString[0].capitalize()+variableNameString[1:]+"(self, "+variableNameString+"Num):")
    code.indent()
    vars_code = code.add_section()
    code.add_line("from RiskQuantLib.Property.NumberProperty.numberProperty import numberProperty")
    code.add_line("if not hasattr(self, '_"+variableNameString+"'):")
    code.indent()
    code.add_line("self._"+variableNameString+" = numberProperty("+variableNameString+"Num)")
    code.add_line("self._"+variableNameString+".setBelongTo(self,'"+variableNameString+"')")
    code.add_line("self."+variableNameString+" = self._"+variableNameString+".value")
    code.dedent()
    code.add_line("else:")
    code.indent()
    code.add_line("self._"+variableNameString+".setValue("+variableNameString+"Num)")
    code.add_line("self."+variableNameString+" = self._"+variableNameString+".value")
    code.dedent()

    code.dedent()
    code.get_globals()
    return code

def buildBaseFunction(variableNameString:str):
    """
    buildBaseFunction(variableNameString:str) is a function to automatically build a set function,
    given the variable type as 'Any'.
    This function will import a property instance from RiskQuantLib.Property.base,
    and returns a codeBuilder object.

    Parameters
    ----------
    variableNameString : str
        The variable name you want to use.
        This name will be used as attribute name of class.

    Returns
    -------
    code : codeBuilder Object
    """
    from RiskQuantLib.Tool.codeBuilderTool import codeBuilder

    code = codeBuilder(indent=4)

    code.add_line("def set"+variableNameString[0].capitalize()+variableNameString[1:]+"(self, "+variableNameString+"):")
    code.indent()
    vars_code = code.add_section()
    code.add_line("from RiskQuantLib.Property.base import base")
    code.add_line("if not hasattr(self, '_"+variableNameString+"'):")
    code.indent()
    code.add_line("self._"+variableNameString+" = base("+variableNameString+")")
    code.add_line("self._" + variableNameString + ".setBelongTo(self,'" + variableNameString + "')")
    code.add_line("self."+variableNameString+" = self._"+variableNameString+".value")
    code.dedent()
    code.add_line("else:")
    code.indent()
    code.add_line("self._"+variableNameString+".setValue("+variableNameString+")")
    code.add_line("self."+variableNameString+" = self._"+variableNameString+".value")
    code.dedent()

    code.dedent()
    code.get_globals()
    return code

def buildSelfDefinedTypeFunction(variableNameString:str, variableTypeString : str):
    """
    buildSelfDefinedTypeFunction(variableNameString:str, variableTypeString : str)
    is a function to automatically build a set function,
    given the variable type as self-defined string.
    This function will import a property instance from RiskQuantLib.Property.selfDefinedType,
    and returns a codeBuilder object.

    Parameters
    ----------
    variableNameString : str
        The variable name you want to use.
        This name will be used as attribute name of class.
    variableTypeString : str
        The variable type you want to set your variable to, usually, it should be
        'String', 'Number' or 'Any', but after defining your own type class, you
        can use it as a variable type.

    Returns
    -------
    code : codeBuilder Object
    """
    c_variableTypeString = variableTypeString[0].capitalize()+variableTypeString[1:]
    from RiskQuantLib.Tool.codeBuilderTool import codeBuilder

    code = codeBuilder(indent=4)

    code.add_line("def set"+variableNameString[0].capitalize()+variableNameString[1:]+"(self, "+variableNameString+"):")
    code.indent()
    vars_code = code.add_section()
    code.add_line("from RiskQuantLib.Property."+c_variableTypeString+"."+variableTypeString+" import "+variableTypeString)
    code.add_line("if not hasattr(self, '_"+variableNameString+"'):")
    code.indent()
    code.add_line("self._"+variableNameString+" = "+variableTypeString+"("+variableNameString+")")
    code.add_line("self._" + variableNameString + ".setBelongTo(self,'" + variableNameString + "')")
    code.add_line("self."+variableNameString+" = self._"+variableNameString+".value")
    code.dedent()
    code.add_line("else:")
    code.indent()
    code.add_line("self._"+variableNameString+".setValue("+variableNameString+")")
    code.add_line("self."+variableNameString+" = self._"+variableNameString+".value")
    code.dedent()

    code.dedent()
    code.get_globals()
    return code

def commitObjectFunctionBuild(codeList:list,sourceFilePath:str):
    """
    commitObjectFunctionBuild(codeList:list,sourceFilePath:str) is a function to commit creations of variable set function.
    This function clear any contents between '#-<Begin>' and '#-<End>', replace it with new source code generated by 'codeList',

    Parameters
    ----------
    codeList : list
        A list of codeBuilder objects, contains multiple of set functions.
    sourceFilePath : str
        The file where your want to rewrite set function.

    Returns
    -------
    None
    """
    sourceCodeList = [i.python_source for i in codeList]
    sourceCode = "".join(sourceCodeList)

    with open(sourceFilePath, 'r') as f:
        content = f.read()

    if content.find('#-<Begin>') == -1 or content.find('#-<End>') == -1:
        print("Source file must have a #-<Begin> and #-<End> tag to be built")
        exit(-1)

    former = content.split('#-<Begin>')[0]
    ender = content.split('#-<End>')[-1]
    newContent = former + '#-<Begin>\n' + sourceCode + '    #-<End>\n\t' + ender
    with open(sourceFilePath, 'w') as f:
        f.truncate()  # clear all contents of file
        f.write(newContent.strip(' ').strip('\t\n'))


def buildListSetFunction1D(variableNameString:str,variableType:str = 'Base'):
    """
    buildListSetFunction1D(variableNameString:str,variableType:str = 'Base') is a function
    to generate set function of RiskQuantLib list object,
    given the condition that variable is a one-dimension variable.
    This function returns a codeBuilder object

    Parameters
    ----------
    variableNameString : str
        The variable name you used.
    variableType : str
        The variable type you specified.

    Returns
    -------
    code : codeBuilder object
    """
    defaultValueDict = {
        "Str":"''",
        "Num":"np.nan",
        "Base":"np.nan"
    }
    if variableType not in defaultValueDict.keys():
        print("Variable type must be set as 'Str', 'Num' or 'Base'")
        exit(-1)
    else:
        from RiskQuantLib.Tool.codeBuilderTool import codeBuilder

        code = codeBuilder(indent=4)

        code.add_line("def set"+variableNameString[0].capitalize()+variableNameString[1:]+"(self,codeSeries,"+variableNameString+"Series,byAttr='code',update=False):")
        code.indent()
        vars_code = code.add_section()
        code.add_line(variableNameString+"Dict = dict(zip(codeSeries,"+variableNameString+"Series))")

        code.add_line("if byAttr=='code' and not update:")
        code.indent()
        code.add_line("[i.set"+variableNameString[0].capitalize()+variableNameString[1:]+"("+variableNameString+"Dict[i.code]) if i.code in "+variableNameString+"Dict.keys() else i.set"+variableNameString[0].capitalize() + variableNameString[1:]+"("+defaultValueDict[variableType]+") for i in self.all]")
        code.dedent()

        code.add_line("elif not update:")
        code.indent()
        code.add_line("[i.set"+variableNameString[0].capitalize()+variableNameString[1:]+"("+variableNameString+"Dict[getattr(i,byAttr)]) if hasattr(i,byAttr) and getattr(i,byAttr) in "+variableNameString+"Dict.keys() else i.set"+variableNameString[0].capitalize() + variableNameString[1:]+"("+defaultValueDict[variableType]+") for i in self.all]")
        code.dedent()

        code.add_line("else:")
        code.indent()
        code.add_line("[i.set"+variableNameString[0].capitalize()+variableNameString[1:]+"("+variableNameString+"Dict[getattr(i,byAttr)]) if hasattr(i,byAttr) and getattr(i,byAttr) in "+variableNameString+"Dict.keys() else None for i in self.all]")
        code.dedent()

        code.dedent()
        code.get_globals()
        return code

def buildListSetFunction2D(variableNameString:str):
    """
    buildListSetFunction2D(variableNameString:str) is a function
    to generate set function of RiskQuantLib list object,
    given the condition that variable is a two-dimension variable, like a time series.
    This function returns a codeBuilder object

    Parameters
    ----------
    variableNameString : str
        The variable name you used.

    Returns
    -------
    code : codeBuilder object
    """
    from RiskQuantLib.Tool.codeBuilderTool import codeBuilder

    code = codeBuilder(indent=4)

    code.add_line("def set"+variableNameString[0].capitalize()+variableNameString[1:]+"(self,"+variableNameString+"DataFrame,byAttr='code',update=False):")
    code.indent()
    vars_code = code.add_section()
    code.add_line("import pandas as pd")
    code.add_line(variableNameString+"CodeList = "+variableNameString+"DataFrame.columns.to_list()")

    code.add_line("if byAttr=='code' and not update:")
    code.indent()
    code.add_line("[i.set"+variableNameString[0].capitalize()+variableNameString[1:]+"("+variableNameString+"DataFrame[i.code]) if hasattr(i,'code') and i.code in "+variableNameString+"CodeList else i.set"+variableNameString[0].capitalize()+variableNameString[1:]+"(pd.Series()) for i in self.all]")
    code.dedent()

    code.add_line("elif not update:")
    code.indent()
    code.add_line("[i.set" + variableNameString[0].capitalize() + variableNameString[1:] + "(" + variableNameString + "DataFrame[getattr(i,byAttr)]) if hasattr(i,byAttr) and getattr(i,byAttr) in " + variableNameString + "CodeList else i.set" +variableNameString[0].capitalize() + variableNameString[1:] + "(pd.Series()) for i in self.all]")
    code.dedent()

    code.add_line("else:")
    code.indent()
    code.add_line("[i.set" + variableNameString[0].capitalize() + variableNameString[1:] + "(" + variableNameString + "DataFrame[getattr(i,byAttr)]) if hasattr(i,byAttr) and getattr(i,byAttr) in " + variableNameString + "CodeList else None for i in self.all]")
    code.dedent()

    code.dedent()
    code.get_globals()
    return code


def commitListFunctionBuild(codeList:list,sourceFilePath:str):
    """
    commitListFunctionBuild(codeList:list,sourceFilePath:str) is a function to commit creations of set function
    of RiskQuantLib list object.
    This function clear any contents between '#-<Begin>' and '#-<End>', replace it with new source code generated by 'codeList',

    Parameters
    ----------
    codeList : list
        A list of codeBuilder objects, contains multiple of list set functions.
    sourceFilePath : str
        The file where your want to rewrite set function.

    Returns
    -------
    None
    """
    sourceCodeList = [i.python_source for i in codeList]
    sourceCode = "".join(sourceCodeList)

    with open(sourceFilePath, 'r') as f:
        content = f.read()

    if content.find('#-<Begin>') == -1 or content.find('#-<End>') == -1:
        print("Source file must have a #-<Begin> and #-<End> tag to be built")
        exit(-1)

    former = content.split('#-<Begin>')[0]
    ender = content.split('#-<End>')[-1]
    newContent = former + '#-<Begin>\n' + sourceCode + '    #-<End>\n\t' + ender
    with open(sourceFilePath, 'w') as f:
        f.truncate()  # clear all contents of file
        f.write(newContent.strip(' ').strip('\t\n'))

def clearBuiltFunction(sourceFilePath:str):
    """
    clearBuiltFunction(sourceFilePath:str) is a function to clear creations of set function
    of both RiskQuantLib instrument class object and instrument list class object.
    This function clear any contents between '#-<Begin>' and '#-<End>',

    Parameters
    ----------
    sourceFilePath : str
        The file where your want to clear all set functions.

    Returns
    -------
    None
    """
    with open(sourceFilePath, 'r') as f:
        content = f.read()

    if content.find('#-<Begin>') == -1 or content.find('#-<End>') == -1:
        print("Source file must have a #-<Begin> and #-<End> tag to be built")
        exit(-1)

    former = content.split('#-<Begin>')[0]
    ender = content.split('#-<End>')[-1]
    newContent = former + '#-<Begin>\n    #-<End>\n\t' + ender
    with open(sourceFilePath, 'w') as f:
        f.truncate()  # clear all contents of file
        f.write(newContent.strip(' ').strip('\t\n'))



















