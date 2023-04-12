#!/usr/bin/python
#coding = utf-8

import numpy as np
import pandas as pd
import mysql.connector
#<import>
#</import>

class mysqlTool(object):
    """
    This is the API to connect with mysql database.
    """
    def __init__(self,databaseNameString:str,hostAddress:str,userName:str,passWord:str):
        self.targetDB = mysql.connector.connect(
            host = hostAddress,
            user = userName,
            passwd = passWord,
            database = databaseNameString
            # buffered = True
        )
        self.targetCursor = self.targetDB.cursor(buffered=True)

    def getAllTables(self):
        self.targetCursor.execute("SHOW TABLES")
        return [i for i in self.targetCursor]

    def getColNameOfTable(self,tableNameString:str):
        sql = "SELECT * FROM "+tableNameString
        self.targetCursor.execute(sql)
        return [i for i in self.targetCursor.column_names]

    def selectAllFromTable(self,tableNameString:str):
        sql = "SELECT * FROM "+tableNameString
        self.targetCursor.execute(sql)
        result = self.targetCursor.fetchall()
        df = pd.DataFrame(result,columns = self.targetCursor.column_names)
        return df

    def selectDictFromTable(self,tableNameString:str,colNameAsKey:str,colNameAsValue:str):
        try:
            sql = "SELECT "+colNameAsKey+","+colNameAsValue+" FROM "+tableNameString
            self.targetCursor.execute(sql)
            result = self.targetCursor.fetchall()
            resultDict = dict(zip([i[0] for i in result],[i[1] for i in result]))
            return resultDict
        except Exception as e:
            print(e)
            return {}

    def selectColFromTable(self,tableNameString:str,colNameList:list):
        colNameString = "".join(["`"+i+"`," for i in colNameList]).strip(",")
        sql = "SELECT "+colNameString+" FROM "+tableNameString
        self.targetCursor.execute(sql)
        result = self.targetCursor.fetchall()
        df = pd.DataFrame(result,columns = self.targetCursor.column_names)
        return df

    def selectColFromTableWithCondition(self,tableNameString:str,colNameList:list,conditionString:str):
        colNameString = "".join(["`"+i+"`," for i in colNameList]).strip(",")
        sql = "SELECT "+colNameString+" FROM "+tableNameString+" WHERE "+conditionString
        self.targetCursor.execute(sql)
        result = self.targetCursor.fetchall()
        df = pd.DataFrame(result,columns = self.targetCursor.column_names)
        return df

    def selectAllFromTableWithCondition(self,tableNameString:str,conditionString:str):
        sql = "SELECT * FROM "+tableNameString+" WHERE "+conditionString
        self.targetCursor.execute(sql)
        result = self.targetCursor.fetchall()
        df = pd.DataFrame(result,columns = self.targetCursor.column_names)
        return df

    def insertRowIntoTable(self,tableNameString:str,valuesTuple:tuple):

        sql = "SELECT * FROM "+tableNameString
        self.targetCursor.execute(sql)
        colNameString = "".join(["`"+i+"`," for i in self.targetCursor.column_names]).strip(", ")
        sql = "INSERT INTO "+tableNameString+" ("+colNameString+") VALUES (" + "".join(["%s, " for i in range(len(self.targetCursor.column_names))]).strip(", ")+")"
        val = valuesTuple
        self.targetCursor.execute(sql,val)
        self.targetDB.commit()
        print("Insert Finished")

    def replaceRowsIntoTable(self,tableNameString:str,valuesTupleList:list):
        sql = "SELECT * FROM "+tableNameString
        self.targetCursor.execute(sql)
        colNameString = "".join(["`"+i+"`," for i in self.targetCursor.column_names]).strip(", ")
        sql = "REPLACE INTO "+tableNameString+" ("+colNameString+") VALUES (" + "".join(["%s, " for i in range(len(self.targetCursor.column_names))]).strip(", ")+")"
        val = valuesTupleList
        self.targetCursor.executemany(sql, val)
        self.targetDB.commit()
        print("Insert Finished")

    def replaceDFIntoTable(self,tableNameString:str,dataFrame:pd.DataFrame):
        try:
            import numpy as np
            DBTableColNameList = self.getColNameOfTable(tableNameString)
            df = dataFrame[DBTableColNameList]
            # convert to tuple
            valuesTapleList = df.apply(lambda x: tuple([None if type(i)==type(np.nan) and np.isnan(i) else i for i in x]),axis=1).to_list()
            sql = "SELECT * FROM "+tableNameString
            self.targetCursor.execute(sql)
            colNameString = "".join(["`"+i+"`," for i in self.targetCursor.column_names]).strip(", ")
            sql = "REPLACE INTO "+tableNameString+" ("+colNameString+") VALUES (" + "".join(["%s, " for i in range(len(self.targetCursor.column_names))]).strip(", ")+")"
            val = valuesTapleList
            self.targetCursor.executemany(sql, val)
            self.targetDB.commit()
            print("Replace Finished")
        except Exception as e:
            print("Replace Failed, Error:",e)

    #<mysqlTool>
    #</mysqlTool>

class oracleTool(object):
    """
    This is the API to connect with oracle database.
    """
    def __init__(self,databaseNameString:str,hostAddress:str,port:int,userName:str,passWord:str):
        from sqlalchemy import create_engine
        uri = f'oracle+cx_oracle://{userName}:{passWord}@{hostAddress}:{port}/{databaseNameString}'
        self.engine = create_engine(uri)

    def readSql(self,sql:str):
        data = pd.read_sql(sql,con=self.engine)
        return data

    #<oracleTool>
    #</oracleTool>

class sqlServerTool(object):
    """
    This is the API to connect with sql server database.
    """
    def __init__(self,databaseNameString:str,hostAddress:str,userName:str,passWord:str):
        import pymssql
        self.engine = pymssql.connect(hostAddress,userName,passWord,databaseNameString,charset='cp936')
        self.cursor = self.engine.cursor()

    def readSql(self,sql:str):
        data = pd.read_sql(sql,con=self.engine)
        return data

    #<sqlServerTool>
    #</sqlServerTool>

class neo4jTool(object):
    """
    This is the API to connect with neo4j database.
    """

    def __init__(self, hostAddress:str,port:int,userName:str,password:str):
        from py2neo import Graph
        self.engine = Graph(hostAddress+":"+str(port),auth=(userName,password))

    def readCypher(self,cypher:str):
        data = self.engine.run(cypher)
        return data

    def convertDataType(self,x):
        if isinstance(x,np.float64):
            return float(x)
        elif hasattr(x,'strftime'):
            return x.strftime("%Y-%m-%d")
        elif isinstance(x,list):
            return [self.convertDataType(i) for i in x]
        else:
            return x

    def updateDFToNode(self,nodeList:list,df:pd.DataFrame,colAsName:str):
        nameWaitedToBeUpdated = df[colAsName].to_list()
        nameList = [i for i in nodeList if i['name'] in nameWaitedToBeUpdated]
        tmp = df.set_index(colAsName,drop=True)
        [[node.update({j:self.convertDataType(tmp.loc[node['name']][j])}) for j in tmp.columns if j!= colAsName] for node in nameList]

    def convertDFToNode(self, nodeType:str, df:pd.DataFrame, colAsName:str):
        from py2neo import Node
        nodeList = [Node(nodeType, name=df.iloc[i][colAsName]) for i in range(df.shape[0])]
        [[nodeList[i].update({j:self.convertDataType(df.iloc[i][j])}) for j in df.columns if j!=colAsName] for i in range(df.shape[0])]
        return nodeList

    def addNodeFromDF(self, nodeType:str, df:pd.DataFrame, colAsName:str):
        nodeList = self.convertDFToNode(nodeType, df, colAsName)
        [self.engine.create(i) for i in nodeList]
        return nodeList

    def selectAllLabel(self):
        labelList = self.readCypher("MATCH (res) RETURN distinct labels(res)")
        return [i[0][0] for i in labelList]

    def selectAllNode(self, nodeType:str):
        nodeList = self.readCypher(f'''MATCH (res:`{nodeType}`) RETURN res''')
        return [i['res'] for i in nodeList]

    def selectAttrFromNode(self, nodeType:str, attrList:list):
        if type(attrList)==type(''):
            attrList = [attrList]
        else:
            pass
        attr = "'],res['".join(attrList)
        nodeList = self.readCypher(f"MATCH (res:`{nodeType}`) RETURN res['"+attr+"']")
        return nodeList.to_data_frame().rename(columns=dict(zip(["res['"+i+"']" for i in attrList],attrList)))

    def selectAllNodeWithCondition(self, nodeType: str, conditionString:str, resultVariableName:str = 'res'):
        nodeList = self.readCypher(f'''MATCH ({resultVariableName}:`{nodeType}`) WHERE {conditionString} RETURN {resultVariableName}''')
        return [i[resultVariableName] for i in nodeList]

    def selectAttrFromNodeWithCondition(self, nodeType: str, attrList: list, conditionString:str, resultVariableName:str = 'res'):
        if type(attrList) == type(''):
            attrList = [attrList]
        else:
            pass
        attr = "'],res['".join(attrList)
        nodeList = self.readCypher(f"MATCH ({resultVariableName}:`{nodeType}`) WHERE {conditionString} RETURN {resultVariableName}['" + attr + "']")
        return nodeList.to_data_frame().rename(columns=dict(zip([f"{resultVariableName}['" + i + "']" for i in attrList], attrList)))

    def connectNodeByAttr(self, nodeTypeLeft:str, nodeTypeRight:str, attrNameLeft:str, attrNameRight:str, relationName:str):
        from py2neo import Relationship
        leftNode = self.selectAllNode(nodeTypeLeft)
        rightNode = self.selectAllNode(nodeTypeRight)
        pair = [(left,right) for left in leftNode for right in rightNode if left[attrNameLeft]==right[attrNameRight]]
        relation = [Relationship(i[0],relationName,i[1]) for i in pair]
        [self.engine.create(i) for i in relation]

    def replaceNode(self, nodeObj):
        self.engine.push(nodeObj)

    def replaceNodeFromDF(self, nodeType:str, df:pd.DataFrame, colAsName:str):
        nodeList = self.selectAllNodeWithCondition(nodeType,"res.name IN ['"+"','".join(df[colAsName].to_list())+"']")
        self.updateDFToNode(nodeList,df,colAsName)
        oldNode = [i['name'] for i in nodeList]
        tmp = df[[(i not in oldNode) for i in df[colAsName]]]
        self.addNodeFromDF(nodeType,tmp,colAsName)
        [self.engine.push(i) for i in nodeList]

    def deleteAllNode(self):
        self.engine.delete_all()
        print("All Nodes Have Been Deleted")

    def deleteNode(self, nodeObj):
        self.engine.delete(nodeObj)

    #<neo4jTool>
    #</neo4jTool>