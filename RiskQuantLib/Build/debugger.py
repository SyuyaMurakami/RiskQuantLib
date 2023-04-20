#!/usr/bin/python
# coding = utf-8
import os, re, ast, sys

class debugger(object):
    """
    debugger is a class used to render .py file. It will parse the functions in .py file and bound them into
    the class which is specified by #-> comment command. This is different with the normal render, the normal render
    will take .py file as a text file and take the content as it be. This debugger takes .py file as an executable
    file and will execute it by import the file and bind its functions into class dynamically.
    """

    @staticmethod
    def findFunction(sourceCode:str):
        """
        Use python ast module to parse source code. This aims at finding functions that can be treated as validated
        python functions. ast module can be used in python>=3.5, it is the abstract-syntax-tree, used as interface to
        python interpreter.
        """
        astObject = ast.parse(sourceCode)
        content = sourceCode.splitlines()
        function = [i for i in astObject.body if type(i)==ast.FunctionDef]
        return function

    @staticmethod
    def findFunctionStart(functionObject:ast.FunctionDef):
        """
        Find function start line index. For some functions with decorators, the start line will be the start line of first
        decorator.
        """
        return min([functionObject.lineno] + [j.lineno for j in functionObject.decorator_list])-1

    @staticmethod
    def findFunctionEnd(functionObject:ast.FunctionDef):
        """
        Find function end line index.
        """
        return functionObject.end_lineno

    @staticmethod
    def unParseSourceCode(sourceCodeByLine:list, startLine:int, endLine:int):
        """
        Given a list of source code, whose element is each line of source code, given start line and end line, this
        function will merge the content between start and end line, and return the merged source code.
        """
        sourceCode = "\n".join(sourceCodeByLine[startLine:endLine])
        return sourceCode

    @staticmethod
    def findClassMethodFunction(function:list):
        """
        For all possible definition parsed from ast module, only those with first argument as 'self' can be treated as
        class method. For python, this is not a restriction, you can use any key word to replace 'self', however, for
        RiskQuantLib, it takes 'self' as the only possible one in order to debug.

        Parameters
        ----------
        function : list
            The list whose element is the parsed ast function definition object, which is ast.FunctionDef.
        """
        functionOfClassMethod = [i for i in function if type(i) == ast.FunctionDef and len(i.args.args)>=1 and i.args.args[0].arg == 'self']
        return functionOfClassMethod

    @staticmethod
    def findFunctionUnderControlComment(function:list, controlCommentLineRange:list):
        """
        For all possible class method, it can not be debugged unless it is distributed into a RiskQuantLib instrument
        node. Only those functions which is under some control comment can be debugged, this function is to find those.

        Parameters
        ----------
        function : list
            The list whose element is the parsed ast function definition object, which is ast.FunctionDef.
        controlCommentLineRange : list
            The list whose element is a tuple, which is (line index where control comment start effective, line index
            where that control comment end effective).
        """
        functionChunk = [(debugger.findFunctionStart(i), debugger.findFunctionEnd(i)) for i in function]
        underControlComment = [[j for j in controlCommentLineRange if j[0] <= i[0] and i[1] <= j[1]] for i in functionChunk]
        functionUnderControlComment = [(i, k) for i, j, k in zip(function, underControlComment,functionChunk) if len(j) == 1]

        functionValidated = [i[0] for i in functionUnderControlComment]
        functionChunkValidated = [i[1] for i in functionUnderControlComment]
        functionNameValidated = [i.name for i in functionValidated]
        functionNameValidatedDict = dict(zip(functionChunkValidated, functionNameValidated))
        return functionChunkValidated, functionNameValidatedDict

    @staticmethod
    def findOtherChunkOutsideGivenChunk(functionChunk:list, endLineNum:int):
        """
        Given a list whose element is a tuple: (start line of chunk, end line of chunk), and given the total line number,
        this function will find those chunk which does not belong to given chunk and not cross with given chunk.
        In short, this function is to find replenishment of given set.

        Parameters
        ----------
        functionChunk : list
            The list whose element is the start and end of a chunk.
        endLineNum : int
            The total line number of source code.
        """
        chunkOfGiven = sorted(functionChunk) if len(functionChunk)!=0 else [(0, 0)]
        chunkOfGivenNum = len(chunkOfGiven)
        chunkOfOthersBody = [(chunkOfGiven[i][1],chunkOfGiven[i+1][0]) for i in range(chunkOfGivenNum) if i<chunkOfGivenNum-1]
        chunkOfOthersHead = [(0,chunkOfGiven[0][0])]
        chunkOfOthersTail = [(chunkOfGiven[-1][1],endLineNum)]
        chunkOfOthers = [j for j in chunkOfOthersHead + chunkOfOthersBody + chunkOfOthersTail if j[0]!=j[1]]
        chunkOfGiven = [i for i in chunkOfGiven if i[0]!=i[1]]
        return chunkOfGiven,chunkOfOthers

    @staticmethod
    def findControlCommentLineId(sourceCodeByLine:list):
        """
        Find the line index of control comment.
        """
        commentLineMatch = [[j for j in re.finditer(r'''^#->.*$''', i, flags=re.MULTILINE)] for i in sourceCodeByLine]
        controlCommentLineId = [idx for idx,i in enumerate(commentLineMatch) if len(i)!=0]
        return controlCommentLineId

    @staticmethod
    def findControlCommentLineRange(controlCommentLineId:list, numberOfLine:int):
        """
        For every control comment, find the line index where it starts effective and line index where it stops effective.

        Parameters
        ----------
        controlCommentLineId : list
            The list whose element is the line index number where the control comments lie.
        numberOfLine : int
            The total line number of source code.
        """
        endOfChunk = controlCommentLineId[1:] + [numberOfLine]
        range = zip(controlCommentLineId, endOfChunk)
        return list(range)

    @staticmethod
    def importModuleFromFile(filePath:str):
        """
        Import module from given file and cache it into sys.modules. If this file has already been imported, it will load
        the cached one.
        """
        if filePath not in sys.modules:
            import importlib.util as util
            spec = util.spec_from_file_location("tmp", filePath)
            tmp = util.module_from_spec(spec)
            spec.loader.exec_module(tmp)
            sys.modules[filePath] = tmp
        else:
            tmp = sys.modules[filePath]
        return tmp

    @staticmethod
    def splitSrcByChunkAndFindThoseCanBeDebugged(sourceCode:str):
        """
        This function will check the while source code and find those functions can be treated as class method,
        the definition of these functions are wrapped into a chunk. Then the other source code are packed into
        chunks according to class-method chunk. All these source code chunk are then labelled as 'can be debugged'
        and 'can not be debugged', if it can be debugged, its function name will be found and returned.
        """

        # collect source code and split them into lines
        lineOfContent = sourceCode.splitlines()
        lineNum = len(lineOfContent)

        # collect all control comment that can be debugged
        controlCommentLineId = debugger.findControlCommentLineId(lineOfContent)
        controlCommentLineRange = debugger.findControlCommentLineRange(controlCommentLineId,lineNum)

        # find function definition from source code, and find those which can be treated as class method
        function = debugger.findFunction(sourceCode)
        functionOfPossibleClassMethod = debugger.findClassMethodFunction(function)

        functionChunkOfClassMethod, functionNameOfClassMethodDict = debugger.findFunctionUnderControlComment(functionOfPossibleClassMethod,controlCommentLineRange)
        chunkOfClassMethod, chunkOfNonClassMethod = debugger.findOtherChunkOutsideGivenChunk(functionChunkOfClassMethod, lineNum)

        # collect all chunks, and whether it can be debugged, and the class method name if it can be debugged
        chunk = sorted(chunkOfClassMethod + chunkOfNonClassMethod)
        srcOfChunk = [debugger.unParseSourceCode(lineOfContent,i[0],i[1]) for i in chunk]
        canBeDebugged = [i in set(chunkOfClassMethod) for i in chunk]
        functionName = [functionNameOfClassMethodDict[i] if i in functionNameOfClassMethodDict else '' for i in chunk]

        return {"srcOfChunk":srcOfChunk, "canBeDebugged":canBeDebugged, "functionName":functionName}













