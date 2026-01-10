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

def loadCsv(filePath:str, index_col=0):
    """
    Use pandas.read_csv to load csv file, default set the first column as index.
    """
    return pd.read_csv(filePath, index_col=index_col)

def loadCsvTimeSeries(filePath:str, index_col=0, converters=None):
    """
    Use pandas.read_csv to load csv file, default set the first column as index, and set its datatype as pandas.Timestamp.
    """
    converters = {0: pd.Timestamp} if converters is None else converters
    return pd.read_csv(filePath, index_col=index_col, converters=converters)

def loadCsvDict(dirPath:str, index_col=0):
    """
    Read all csv file in the target directory, return a dict whose keys are file names and values are pandas.DataFrames.
    """
    return {i:loadCsv(dirPath+os.sep+i, index_col=index_col) for i in os.listdir(dirPath) if os.path.splitext(i)[-1] == '.csv'}

def loadCsvTimeSeriesDict(dirPath:str, index_col=0, converters=None):
    """
    Read all csv file in the target directory, return a dict whose keys are file names and values are pandas.DataFrames.
    Default set the first column of each file as index, and set its datatype as pandas.Timestamp.
    """
    converters = {0: pd.Timestamp} if converters is None else converters
    return {i:loadCsvTimeSeries(dirPath+os.sep+i, index_col=index_col, converters=converters) for i in os.listdir(dirPath) if os.path.splitext(i)[-1] == '.csv'}

def loadExcel(filePath:str):
    """
    Use pandas.read_excel to load csv file.
    """
    return pd.read_excel(filePath)

def loadExcelDict(dirPath:str):
    """
    Read all excel file in the target directory, return a dict whose keys are file names and values are pandas.DataFrames.
    """
    return {i:loadExcel(dirPath+os.sep+i) for i in os.listdir(dirPath) if os.path.splitext(i)[-1] in {'.xlsx', '.xls'}}

def dumpDictToJson(dictVariable:dict,filePath:str):
    """
    Dump dict to json file.
    """
    import json
    json.dump(dictVariable,open(filePath,"w",encoding='UTF-8'),ensure_ascii=False)


def deleteFile(filePath:str):
    """
    Delete a file if it exists.
    """
    if os.path.isfile(filePath):
        os.remove(filePath)
        print('Delete File: ', filePath)
    else:
        print('Delete Failed, File Does Not Exist: ', filePath)

def deleteFileWithConfirm(filePath:str):
    """
    Before Delete a file, ask for confirmation.
    """
    from RiskQuantLib.Tool.decoratorTool import confirmer
    confirmer()(deleteFile)(filePath)

def clearCachePklFile(filePath:str):
    """
    Delete all '.pkl' files in filePath.
    """
    print("Clearing Cache in "+filePath)
    fileListInPath = [i for i in os.listdir(filePath) if i.find('.pkl')!=-1]
    while len(fileListInPath)!=0:
        [deleteFile(i) for i in fileListInPath]
        fileListInPath  = [i for i in os.listdir(filePath) if i.find('.pkl')!=-1]
    time.sleep(2)


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
        if hasattr(self, 'path') and (os.path.isdir(self.path) or os.path.isfile(self.path)):
            stamp = os.stat(self.path).st_mtime
            if stamp != self._cachedStamp:
                self._cachedStamp = stamp
                return self.call_back_function(self.path)

    def tryWatch(self):
        try:
            return self.watch()
        except Exception as e:
            pass

    def start(self):
        try:
            while True:
                self.watch()
        except KeyboardInterrupt:
            pass

    #<systemGuardian>
    #</systemGuardian>

class systemWatcher:
    def __init__(self, monitorPath: str or list, call_back_function_on_file = lambda x:x, call_back_function_on_dir = lambda x:x, call_back_function_on_any_change = lambda x:x, withFormat:bool = False, monitorFormat:set = {}):
        self.monitorPath = monitorPath
        self.call_back_function_on_file = call_back_function_on_file
        self.call_back_function_on_dir = call_back_function_on_dir
        self.call_back_function_on_any_change = call_back_function_on_any_change
        self.withFormat = withFormat
        self.monitorFormat = monitorFormat
        self.fileGuardian = []
        self.dirGuardian = []
        self.validatedFilePath = []
        self.validatedDirPath = []
        self.scanMonitorPath(monitorPath)
        self.createGuardian()

    def scanMonitorPath(self, monitorPath):
        monitorPath = [monitorPath] if type(monitorPath)==str else monitorPath
        self.validatedFilePath = [i for i in monitorPath if os.path.isfile(i) and (not self.withFormat or os.path.splitext(i)[-1] in self.monitorFormat)]
        self.validatedDirPath = [i for i in monitorPath if os.path.isdir(i)]
        recursivePath = [([os.path.join(dirPath,dir) for dir in dirs],[os.path.join(dirPath,file) for file in files if not self.withFormat or os.path.splitext(file)[-1] in self.monitorFormat]) for rootPath in self.validatedDirPath for dirPath, dirs, files in os.walk(rootPath)]
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
        fileInfo = [i.tryWatch() for i in self.fileGuardian]
        updatedFile = [i for i in fileInfo if type(i)==str and os.path.isfile(i)]
        self.call_back_function_on_file_result = [self.call_back_function_on_file(i) for i in updatedFile]
        dirInfo = [i.tryWatch() for i in self.dirGuardian]
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
