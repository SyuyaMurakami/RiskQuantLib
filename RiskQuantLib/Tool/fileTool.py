#!/usr/bin/python
#coding = utf-8

import time, os, datetime
import pandas as pd
#<import>
#</import>


def modifyDateIsToday(filePath:str,mode='M'):
    """
    This function will return a bool value, showing whether the target
    file is modified on today.
    """
    if mode == 'M':
        modifyDate = os.path.getmtime(filePath)
    elif mode=='C':
        modifyDate = os.path.getctime(filePath)
    else:
        print("Mode Error")
        return
    datetimeModifyDate = datetime.datetime.utcfromtimestamp(modifyDate).strftime("%Y--%m--%d")
    datetimeDateNow = datetime.datetime.now().strftime("%Y--%m--%d")
    if datetimeModifyDate == datetimeDateNow:
        return True
    else:
        return False

def waitForFile(filePath:str,fileNameKeyWord:str):
    """
    This function will wait for the change or modification of a file.
    """
    fileListInPath = [i for i in os.listdir(filePath) if i.find(fileNameKeyWord)!=-1]
    while len(fileListInPath)==0:
        time.sleep(2)
        fileListInPath = [i for i in os.listdir(filePath) if i.find(fileNameKeyWord)!=-1]
    return 0

def dumpVariable(variable,filePath:str):
    """
    Use python module pickle to dump variable.
    """
    import pickle as pkl
    pkl.dump(variable,open(filePath,"wb"))

def loadVariable(filePath:str):
    """
    Use python module pickle to load variable.
    """
    import pickle as pkl
    return pkl.load(open(filePath,"rb"))

def dumpDictToJson(dictVariable:dict,filePath:str):
    """
    Dump dict to json file.
    """
    import json
    json.dump(dictVariable,open(filePath,"w",encoding='UTF-8'),ensure_ascii=False)

def clearCachePklFile(filePath:str):
    """
    Delete all '.pkl' files in filePath.
    """
    print("Clearing Cache in "+filePath)
    fileListInPath = [i for i in os.listdir(filePath) if i.find('.pkl')!=-1]
    while len(fileListInPath)!=0:
        os.system('del "'+filePath+os.sep+'*.pkl"')
        fileListInPath  = [i for i in os.listdir(filePath) if i.find('.pkl')!=-1]
    time.sleep(2)

def findFirstNotNanValueOfSeries(x):
    """
    Return the first not nan value of a pandas.Series object.
    """
    import numpy as np
    for i in x.values:
        if type(i)==type(np.nan) and np.isnan(i):
            pass
        else:
            return i
    return np.nan

def resetIndexByFirstNotNanValue(df:pd.DataFrame,dropFirst = False):
    """
    Reset index by the first not nan value.
    """
    df.dropna(axis=0,how='all',inplace=True)
    df.index = df.apply(findFirstNotNanValueOfSeries,axis=1)
    if dropFirst:
        df.drop(columns=[df.columns[0]],inplace=True)

def louverBox(target_df:pd.DataFrame,groupBy:str = '',insertTo:str = ''):
    """
    This function is like pandas.DataFrame.sum, however, this function will
    sum the value for each column, and insert it as a new row before the dataframe.

    Parameters
    -----------
    target_df : pd.DataFrame
        The dataframe you want to louverBox
    groupBy : str
        The column name that you want to groupby.
    insertTo : str
        The index name of the insert row.

    Returns
    -------
    tmp_df : pd.DataFrame
        The louverBox-ed dataframe.
    """
    import numpy as np
    tmp_df = target_df.copy()
    groupName  = tmp_df[groupBy].unique()[0]
    tmp_df.reset_index(drop=True, inplace=True)
    tmp_df = tmp_df.drop(columns=[groupBy])
    tmp_df['IF_ASSEMBLE'] = False

    insertList = [np.nansum(tmp_df[i]) if tmp_df[i].dtypes!=np.object else np.nan for i in tmp_df.columns]
    insertList[tmp_df.columns.to_list().index(insertTo)] = groupName
    insertList[tmp_df.columns.to_list().index("IF_ASSEMBLE")] = True
    if tmp_df.shape[0]!=1:
        tmp_df.loc[-1] = insertList
    else:
        tmp_df[insertTo] = groupName
        tmp_df['IF_ASSEMBLE'] = True

    tmp_df.drop_duplicates(inplace=True,keep='first')
    tmp_df.sort_index(inplace=True)
    tmp_df.reset_index(drop=True,inplace=True)
    return tmp_df

def dataFrameLouverBox(df:pd.DataFrame,groupBy:str='',insertTo:str=''):
    """
    This function is like pandas.DataFrame.groupby, however, this function will
    sum the value for each group, and insert it as a new row before that group.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe that you want to louverBox
    groupBy : str
        The column you want to group by.
    insertTo :str
        The column you want to record the result

    Returns
    -------
    result : pd.DataFrame
    """
    if insertTo not in df.columns.to_list():
        df[insertTo] = ''
    result = df.groupby(groupBy).apply(lambda x:louverBox(x,groupBy=groupBy,insertTo=insertTo))
    result.reset_index(drop=True,inplace=True)
    return result

def generateFileDictFromPath(filePathString:str, targetDict:dict = {}, onlyExcel:bool = True):
    """
    This function generate a dict of file.

    Parameters
    ----------
    filePathString :str
        The path you want to read files from.
    targetDict : dict
        The dict to hold result.
    onlyExcel : bool
        If true, only excel will be read and loaded.

    Returns
    -------
    targetDict : dict
        The dict holding excel dataframe or paths.
    """
    import pandas as pd
    fileList = os.listdir(filePathString)
    if onlyExcel:
        fileList = [i for i in fileList if i.find('.xlsx')!=-1 or i.find('.xls')!=-1]
        excelList = [pd.read_excel(filePathString+os.sep+i,index_col=None) for i in fileList]
        fileDict = dict(zip(fileList,excelList))
        [resetIndexByFirstNotNanValue(fileDict[i]) for i in fileList]
        targetDict[filePathString] = dict(zip(fileList,[fileDict[i].to_dict(orient='dict') for i in fileList]))
        return targetDict
    else:
        targetDict[filePathString] = fileList
        return targetDict

def generateDataFrameFromDict(inputDict:dict, dateString:str, fileNameString:str, columnNameString:str):
    """
    Generate a dataframe from a dict.
    """
    import pandas as pd
    df = pd.DataFrame([inputDict.keys(),inputDict.values()], index=['ROW','VALUE']).T
    df['PATH'] = dateString
    df['FILE'] = fileNameString
    df['COLUMN'] = columnNameString
    return df

def compressExcel(filePathString:str, outputPathString:str, subDictionary:bool = True):
    """
    Re-format excel in form of ['PATH','FILE','COLUMN','ROW','VALUE']

    Parameters
    ----------
    filePathString : str
        The path where you hold your excel files.
    outputPathString : str
        The path of return file.
    subDictionary : bool
        If there are still other dictionaries in filePathString.

    Returns
    -------
    None
    """
    import pandas as pd
    import operator
    from functools import reduce
    if subDictionary:
        dirList = [i for i in os.listdir(filePathString) if i.find('.')==-1]
        subDictionaryDict = {}
        [generateFileDictFromPath(filePathString+os.sep+i,subDictionaryDict) for i in dirList]
        dfArray = [[[generateDataFrameFromDict(subDictionaryDict[i][j][k],dateString=i,fileNameString=j,columnNameString=k) for k in subDictionaryDict[i][j].keys()] for j in subDictionaryDict[i].keys()] for i in subDictionaryDict.keys()]
        dfList = reduce(operator.add,dfArray)
        dfList = reduce(operator.add,dfList)
        result = pd.concat(dfList)
        result.reset_index(drop=True,inplace=True)
        result[['PATH','FILE','COLUMN','ROW','VALUE']].to_excel(outputPathString,index=0)
    else:
        dictionaryDict = {}
        generateFileDictFromPath(filePathString,dictionaryDict)
        dfArray = [[[generateDataFrameFromDict(dictionaryDict[i][j][k],dateString=i,fileNameString=j,columnNameString=k) for k in dictionaryDict[i][j].keys()] for j in dictionaryDict[i].keys()] for i in dictionaryDict.keys()]
        dfList = reduce(operator.add,dfArray)
        dfList = reduce(operator.add,dfList)
        result = pd.concat(dfList)
        result.reset_index(drop=True,inplace=True)
        result[['PATH','FILE','COLUMN','ROW','VALUE']].to_excel(outputPathString,index=0)

#<fileTool>
#</fileTool>

class fileReceiver:
    def __init__(self, targetFilePath):
        import socket
        self.broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.listen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listen.settimeout(1)
        self.listen.bind(('',9004))
        self.hostname = socket.gethostname()
        self.fileAlreadyReceived = []
        self.fileNeglected = []
        self.fileReceiveFinished = False
        self.targetFilePath = targetFilePath

    def __del__(self):
        self.broadcast.close()
        self.listen.close()

    def sendOnLineInfo(self):
        self.broadcast.sendto(('OnLine->'+self.hostname).encode('utf-8'), ('255.255.255.255', 9003))

    def sendIPInfo(self):
        self.broadcast.sendto(('IPInfo->' + self.hostname).encode('utf-8'), ('255.255.255.255', 9006))

    def receiveFileInfo(self):
        try:
            fileInfo, address = self.listen.recvfrom(1024)
        except:
            fileInfo = None
            address = None

        if fileInfo and address:
            fileInfo = fileInfo.decode("utf-8")
            fileInfoList = fileInfo.split('->')
            senderName = fileInfoList[1]
            fileName = fileInfoList[2]
            fileSize = int(fileInfoList[3])
            return address,senderName,fileName,fileSize
        else:
            return '','','',0

    def receiveFileContent(self,address,fileName,fileSize):
        import socket
        self.receive = socket.socket()
        self.receive.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.receive.settimeout(15)
        self.receive.bind(('', 9005))
        self.receive.listen(5)
        connectEstablished = False
        while not connectEstablished:
            self.sendIPInfo()
            connect, _ = self.receive.accept()
            connectEstablished = True if connect else False
        totalFileSize = fileSize
        with open(self.targetFilePath+os.sep+fileName, 'wb') as targetFile:
            chunkSize = 4096
            while fileSize > 0:
                if fileSize < chunkSize:
                    chunkSize = fileSize
                data = connect.recv(chunkSize)
                targetFile.write(data)
                fileSize -= len(data)
                percentage = min(1 - fileSize / totalFileSize, 1)
                print("\r"+"Download "+fileName+": "+"".join(["=" for i in range(int(50*percentage))])+">"+str(int(100*percentage))+"%",end="")
            print("")
        if os.path.exists(self.targetFilePath+os.sep+fileName) and os.path.getsize(self.targetFilePath+os.sep+fileName)!=0:
            print('File Received Successfully')
            self.fileReceiveFinished = True
            self.fileAlreadyReceived.append((address,fileName))
        else:
            print('File Received Failed')
        self.receive.close()

    def receiveFile(self):
        address, senderName, fileName, fileSize = self.receiveFileInfo()
        if address and senderName and fileName and fileSize and senderName!=self.hostname and ((address[0],fileName) not in self.fileAlreadyReceived + self.fileNeglected):
            receiveFile = input("Do you want to receive " + fileName + " from " + senderName + " ? (Y/N)")
            if receiveFile.lower() == 'y' or receiveFile == '':
                print("Preparing File, This May Take A While, Please Wait Until All Processes Finish...")
                self.receiveFileContent(address[0], fileName, fileSize)
            else:
                self.fileNeglected.append((address[0],fileName))

    def run(self, timeOut = 100):
        print("Start Receiving File")
        startTime = time.time()
        while time.time() - startTime <= timeOut and not self.fileReceiveFinished:
            try:
                self.receiveFile()
            except:
                pass
        if len(self.fileNeglected)+len(self.fileAlreadyReceived)==0:
            print("Can Not Find Any Sender")

    #<fileReceiver>
    #</fileReceiver>

class fileSender:
    def __init__(self, fileName):
        import socket
        self.broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.listen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listen.settimeout(1)
        self.listen.bind(('',9006))
        self.hostname = socket.gethostname()
        self.filePath = fileName
        self.fileName = os.path.basename(fileName)
        self.fileSize = os.path.getsize(fileName)
        self.fileAlreadySent = []
        self.fileNeglected = []
        self.fileSendFinished = False

    def __del__(self):
        self.broadcast.close()
        self.listen.close()

    def sendOnLineInfo(self):
        self.broadcast.sendto(('OnLine->'+self.hostname).encode('utf-8'), ('255.255.255.255', 9003))

    def receiveIPInfo(self):
        try:
            IPInfo, address = self.listen.recvfrom(1024)
        except:
            IPInfo = None
            address = None

        if IPInfo and address:
            IPInfo = IPInfo.decode("utf-8")
            IPInfoList = IPInfo.split('->')
            receiverName = IPInfoList[1]
            return address,receiverName
        else:
            return '',''

    def sendFileInfo(self):
        self.broadcast.sendto(('FileInfo->'+self.hostname+'->'+self.fileName+'->'+str(self.fileSize)).encode('utf-8'),('255.255.255.255', 9004))

    def sendFileContent(self,address):
        import socket
        self.send = socket.socket()
        self.send.connect((address, 9005))
        with open(self.filePath, 'rb') as targetFile:
            line = targetFile.read()
            self.send.sendall(line)
        print('File Sent: ' + self.fileName)
        self.fileSendFinished = True
        self.fileAlreadySent.append((address,self.fileName))
        self.send.close()


    def sendFile(self):
        self.sendFileInfo()
        address,receiverName = self.receiveIPInfo()
        if address and receiverName and receiverName!=self.hostname and ((address[0],self.fileName) not in self.fileAlreadySent + self.fileNeglected):
            sendFile = input("Do you confirm to send " + self.fileName + " to " + receiverName + " ? (Y/N)")
            if sendFile.lower() == 'y' or sendFile == '':
                print("Preparing File, This May Take A While, Please Wait Until Receiver Has Finished All Processes...")
                self.sendFileContent(address[0])
            else:
                self.fileNeglected.append((address[0],self.fileName))

    def run(self, timeOut = 100):
        print("Start Sending File")
        startTime = time.time()
        while time.time() - startTime <= timeOut and not self.fileSendFinished:
            try:
                self.sendFile()
            except:
                pass
        if len(self.fileNeglected)+len(self.fileAlreadySent)==0:
            print("Can Not Find Any Receiver")

    #<fileSender>
    #</fileSender>

class systemGuardian:
    def __init__(self, path:str, call_back_function = lambda x:x):
        if os.path.isdir(path) or os.path.isfile(path):
            self._cachedStamp = 0
            self.path = path
            self.call_back_function = call_back_function

    def watch(self):
        if os.path.isdir(self.path) or os.path.isfile(self.path):
            stamp = os.stat(self.path).st_mtime
            if stamp != self._cachedStamp:
                self._cachedStamp = stamp
                return self.call_back_function(self.path)

    def start(self):
        try:
            while True:
                self.watch()
        except KeyboardInterrupt:
            pass

    #<systemGuardian>
    #</systemGuardian>

class systemWatcher:
    def __init__(self, monitorPath: str or list, call_back_function_on_file = lambda x:x, call_back_function_on_dir = lambda x:x, call_back_function_on_any_change = lambda x:x):
        self.monitorPath = monitorPath
        self.call_back_function_on_file = call_back_function_on_file
        self.call_back_function_on_dir = call_back_function_on_dir
        self.call_back_function_on_any_change = call_back_function_on_any_change
        self.fileGuardian = []
        self.dirGuardian = []
        self.validatedFilePath = []
        self.validatedDirPath = []
        self.scanMonitorPath(monitorPath)
        self.createGuardian()


    def scanMonitorPath(self, monitorPath):
        monitorPath = [monitorPath] if type(monitorPath)==str else monitorPath
        self.validatedFilePath = [i for i in monitorPath if os.path.isfile(i)]
        self.validatedDirPath = [i for i in monitorPath if os.path.isdir(i)]
        recursivePath = [([os.path.join(dirPath,dir) for dir in dirs],[os.path.join(dirPath,file) for file in files]) for rootPath in self.validatedDirPath for dirPath, dirs, files in os.walk(rootPath)]
        [self.validatedDirPath.extend(i[0]) for i in recursivePath]
        [self.validatedFilePath.extend(i[1]) for i in recursivePath]

    def createGuardian(self):
        fileGuardianAlreadyExist = set([i.path for i in self.fileGuardian])
        dirGuardianAlreadyExist = set([i.path for i in self.dirGuardian])
        newFileGuardian = [systemGuardian(path) for path in self.validatedFilePath if path not in fileGuardianAlreadyExist]
        newDirGuardian = [systemGuardian(path) for path in self.validatedDirPath if path not in dirGuardianAlreadyExist]
        self.fileGuardian.extend(newFileGuardian)
        self.dirGuardian.extend(newDirGuardian)
        self.allGuardian = self.fileGuardian + self.dirGuardian

    def watch(self):
        fileInfo = [i.watch() for i in self.fileGuardian]
        updatedFile = [i for i in fileInfo if type(i)==str and os.path.isfile(i)]
        self.call_back_function_on_file_result = [self.call_back_function_on_file(i) for i in updatedFile]
        dirInfo = [i.watch() for i in self.dirGuardian]
        updatedDir = [i for i in dirInfo if type(i)==str and os.path.isdir(i)]
        self.call_back_function_on_dir_result = [self.call_back_function_on_dir(i) for i in updatedDir]
        self.call_back_function_on_any_change_result = self.call_back_function_on_any_change(updatedDir+updatedFile) if len(updatedDir+updatedFile)!=0 else None

    def start(self):
        try:
            while True:
                self.scanMonitorPath(self.monitorPath)
                self.createGuardian()
                self.watch()
        except KeyboardInterrupt:
            pass

    #<systemWatcher>
    #</systemWatcher>
