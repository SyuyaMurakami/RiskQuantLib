#!/usr/bin/python
#coding = utf-8

import numpy as np
import pandas as pd
from typing import Union, List

#<import>
#</import>


class sqlConnector(object):
    def __init__(self, engine):
        self.engine = engine

    def readSql(self, sql: str, *args, **kwargs):
        """Execute sql and return a dataframe."""
        from sqlalchemy import text
        with self.engine.connect() as conn:
            df = pd.read_sql(text(sql), con=conn, *args, **kwargs)
        return df

    def writeTable(self, df: pd.DataFrame, tableNameString: str, ifExists: str = 'append'):
        """Write df into database, ifExists can be 'fail', 'replace', 'append'."""
        df.to_sql(tableNameString, con=self.engine, if_exists=ifExists, index=False, method='multi', chunksize=1000)

    def executeSql(self, sql: str, params: dict = None):
        """Execute DDL or DML (like UPDATE, DELETE, CREATE)."""
        from sqlalchemy import text
        with self.engine.begin() as conn:
            conn.execute(text(sql), params or {})

    def getAllTables(self, *args, **kwargs):
        """
        Get names of all tables.
        You may need to specify schema=some if you are connecting
        to oracle or sqlserver.
        """
        from sqlalchemy import inspect
        inspector = inspect(self.engine)
        return inspector.get_table_names(*args, **kwargs)

    def getColNames(self, tableName: str, *args, **kwargs):
        """
        Get all names of columns of a table.
        You may need to specify schema=some if you are connecting
        to oracle or sqlserver.
        """
        from sqlalchemy import inspect
        inspector = inspect(self.engine)
        columns = inspector.get_columns(tableName, *args, **kwargs)
        return [col['name'] for col in columns]

    #<sqlConnector>
    #</sqlConnector>


class mysqlConnector(sqlConnector):
    """This is the API to connect with mysql database using PyMySQL."""
    def __init__(self, databaseName: str, hostAddress: str, port: int, userName: str, passWord: str, charset: str = 'utf8mb4'):
        from sqlalchemy import create_engine
        from sqlalchemy.engine import URL
        url = URL.create(drivername='mysql+pymysql', username=userName, password=passWord, host=hostAddress, port=port, database=databaseName, query={"charset": charset})
        super().__init__(create_engine(url, pool_recycle=3600))

    #<mysqlConnector>
    #</mysqlConnector>


class oracleConnector(sqlConnector):
    """
    This is the API to connect with oracle database.
    Notice that this driver (oracledb) supports only sqlalchemy>=2.0.0.
    If you are using 1.4.0<=sqlalchemy<2.0.0, you can fix it by adding at
    the beginning of your python script:
        import sys, oracledb
        oracledb.version = "8.3.0"
        sys.modules["cx_Oracle"] = oracledb
    Then change the following code into:
        url = URL.create(drivername='oracle+cx_oracle', username=userName, password=passWord, host=hostAddress, port=port, database=databaseName)
    """
    def __init__(self,databaseName: str, hostAddress: str, port: int, userName: str, passWord: str):
        from sqlalchemy import create_engine
        from sqlalchemy.engine import URL
        url = URL.create(drivername='oracle+oracledb', username=userName, password=passWord, host=hostAddress, port=port, database=databaseName)
        super().__init__(create_engine(url))

    #<oracleConnector>
    #</oracleConnector>


class sqlServerConnector(sqlConnector):
    """
    This is the API to connect with sql server database.
    """

    def __init__(self, databaseName: str, hostAddress: str, port: int, userName: str, passWord: str, charset: str = 'cp936'):
        from sqlalchemy import create_engine
        from sqlalchemy.engine import URL
        url = URL.create(drivername='mssql+pymssql', username=userName, password=passWord, host=hostAddress, port=port, database=databaseName, query={"charset": charset})
        super().__init__(create_engine(url))

    #<sqlServerConnector>
    #</sqlServerConnector>


class neo4jConnector(object):
    """This is the API to connect with neo4j database."""

    def __init__(self, hostAddress:str,port:int,userName:str,password:str):
        from py2neo import Graph
        self.engine = Graph(hostAddress+":"+str(port),auth=(userName,password))

    def readCypher(self,cypher:str):
        data = self.engine.run(cypher)
        return data

    def convertDataType(self, x):
        if isinstance(x, np.floating):
            return float(x)
        elif pd.isna(x):
            return None
        elif isinstance(x, str):
            return x
        elif isinstance(x, np.integer):
            return int(x)
        elif hasattr(x, 'strftime'):
            return x.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(x, (list, tuple, np.ndarray)):
            return [self.convertDataType(i) for i in x]
        elif isinstance(x, dict):
            return {self.convertDataType(k): self.convertDataType(v) for k, v in x.items()}
        else:
            return x

    def updateDFToNode(self, nodeList: list, df: pd.DataFrame, colAsName: str):
        nameWaitedToBeUpdated = df[colAsName].to_list()
        nameList = [i for i in nodeList if i['name'] in nameWaitedToBeUpdated]
        tmp = df.set_index(colAsName, drop=True)
        [[node.update({j: self.convertDataType(tmp.loc[node['name']][j])}) for j in tmp.columns if j!= colAsName] for node in nameList]

    def convertDFToNode(self, nodeType: str, df: pd.DataFrame, colAsName: str):
        from py2neo import Node
        nodeList = [Node(nodeType, name=df.iloc[i][colAsName]) for i in range(df.shape[0])]
        [[nodeList[i].update({j: self.convertDataType(df.iloc[i][j])}) for j in df.columns if j!=colAsName] for i in range(df.shape[0])]
        return nodeList

    def addNodeFromDF(self, nodeType: str, df: pd.DataFrame, colAsName: str):
        nodeList = self.convertDFToNode(nodeType, df, colAsName)
        [self.engine.create(i) for i in nodeList]
        return nodeList

    def selectAllLabel(self):
        labelList = self.readCypher("MATCH (res) RETURN distinct labels(res)")
        return [i[0][0] for i in labelList]

    def selectAllNode(self, nodeType: str):
        nodeList = self.readCypher(f'''MATCH (res:`{nodeType}`) RETURN res''')
        return [i['res'] for i in nodeList]

    def selectAttrFromNode(self, nodeType: str, attrList: Union[List[str], str]):
        attrList = [attrList] if type(attrList) is str else attrList
        attr = "'],res['".join(attrList)
        nodeList = self.readCypher(f"MATCH (res:`{nodeType}`) RETURN res['"+attr+"']")
        return nodeList.to_data_frame().rename(columns=dict(zip(["res['"+i+"']" for i in attrList],attrList)))

    def selectAllNodeWithCondition(self, nodeType: str, conditionString: str, resultVariableName: str = 'res'):
        nodeList = self.readCypher(f'''MATCH ({resultVariableName}:`{nodeType}`) WHERE {conditionString} RETURN {resultVariableName}''')
        return [i[resultVariableName] for i in nodeList]

    def selectAttrFromNodeWithCondition(self, nodeType: str, attrList: Union[List[str], str], conditionString: str, resultVariableName: str = 'res'):
        attrList = [attrList] if type(attrList) is str else attrList
        attr = "'],res['".join(attrList)
        nodeList = self.readCypher(f"MATCH ({resultVariableName}:`{nodeType}`) WHERE {conditionString} RETURN {resultVariableName}['" + attr + "']")
        return nodeList.to_data_frame().rename(columns=dict(zip([f"{resultVariableName}['" + i + "']" for i in attrList], attrList)))

    def connectNodeByAttr(self, nodeTypeLeft: str, nodeTypeRight: str, attrNameLeft: str, attrNameRight: str, relationName: str):
        from py2neo import Relationship
        leftNode = self.selectAllNode(nodeTypeLeft)
        rightNode = self.selectAllNode(nodeTypeRight)
        pair = [(left,right) for left in leftNode for right in rightNode if left[attrNameLeft]==right[attrNameRight]]
        relation = [Relationship(i[0],relationName,i[1]) for i in pair]
        [self.engine.create(i) for i in relation]

    def replaceNode(self, nodeObj):
        self.engine.push(nodeObj)

    def replaceNodeFromDF(self, nodeType: str, df: pd.DataFrame, colAsName: str):
        nodeList = self.selectAllNodeWithCondition(nodeType,"res.name IN ['"+"','".join(df[colAsName].to_list())+"']")
        self.updateDFToNode(nodeList,df,colAsName)
        oldNode = [i['name'] for i in nodeList]
        tmp = df[[(i not in oldNode) for i in df[colAsName]]]
        self.addNodeFromDF(nodeType, tmp, colAsName)
        [self.engine.push(i) for i in nodeList]

    def deleteAllNode(self):
        self.engine.delete_all()
        print("All Nodes Have Been Deleted")

    def deleteNode(self, nodeObj):
        self.engine.delete(nodeObj)

    #<neo4jConnector>
    #</neo4jConnector>

#<databaseTool>
#</databaseTool>
