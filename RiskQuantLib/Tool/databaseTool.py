#!/usr/bin/python
#coding = utf-8

import pandas as pd
import mysql.connector

class mysqlTool():
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
