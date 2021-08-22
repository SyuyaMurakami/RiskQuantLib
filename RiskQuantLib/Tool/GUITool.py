#!/usr/bin/python
#coding = utf-8

from tkinter import *
# import hashlib
# import time

LOG_LINE_NUM = 0

class inputGUI():
	def __init__(self,initTkObject,windowTitle,tips):
		self.tkObject = initTkObject
		self.windowTitle = windowTitle
		self.tips = tips

	def setInitWindow(self):
		self.tkObject.title(self.windowTitle)
		self.tkObject.geometry('280x100+500+500')#窗口大小210*100，位置500,500
		#标签
		self.initDataLabel = Label(self.tkObject,text=self.tips)
		self.initDataLabel.grid(row=0,column=0)
		#文本框
		self.initDataText = Text(self.tkObject,width=40,height=3)
		self.initDataText.grid(row=0,column=0,rowspan=3,columnspan=3)
		#按钮
		self.strTansToMD5Button = Button(self.tkObject,text="Submit",bg="lightblue",width=10,command=self.backFunction)#调用内部方法
		self.strTansToMD5Button.grid(row=36,column=0)

	def backFunction(self):
		self.value = self.initDataText.get(1.0,END).strip()
		self.tkObject.destroy()

class confirmGUI():
	def __init__(self, initTkObject, windowTitle, tips, valueString):
		self.tkObject = initTkObject
		self.windowTitle = windowTitle
		self.tips = tips
		self.doubtfulValue = valueString

	def setInitWindow(self):
		self.tkObject.title(self.windowTitle)
		self.tkObject.geometry('280x100+500+500')  # 窗口大小210*100，位置500,500
		# 标签
		self.initDataLabel = Label(self.tkObject, text=self.tips)
		self.initDataLabel.grid(row=0, column=0)
		# 按钮
		self.strTansToMD5Button = Button(self.tkObject, text="Yes", bg="lightblue", width=7, command=self.backFunction)  # 调用内部方法
		self.strTansToMD5Button.grid(row=36, column=0)
		self.strTansToMD5Button = Button(self.tkObject, text="No", bg="lightblue", width=7, command=self.guiStart)  # 调用内部方法
		self.strTansToMD5Button.grid(row=36, column=1)

	def guiStart(self):
		self.tkObject.destroy()
		initWindow = Tk()
		ZMJ_PORTAL = inputGUI(initWindow,"Data Input Window","Input the value you want:")
		# 设置窗口默认属性
		ZMJ_PORTAL.setInitWindow()

		initWindow.mainloop()#保持窗口运行
		self.value = ZMJ_PORTAL.value

	def backFunction(self):
		self.value = self.doubtfulValue
		self.tkObject.destroy()

class alertGUI():
	def __init__(self,initTkObject,windowTitle,tips):
		self.tkObject = initTkObject
		self.windowTitle = windowTitle
		self.tips = tips

	def setInitWindow(self):
		self.tkObject.title(self.windowTitle)
		self.tkObject.geometry('280x80+500+500')#窗口大小210*100，位置500,500
		#标签
		self.initDataLabel = Label(self.tkObject,text=self.tips)
		self.initDataLabel.grid(row=0,column=0)

def guiAlert(tipString):
	initWindow = Tk()
	ZMJ_PORTAL = alertGUI(initWindow,"Alert Window",tipString)
	#设置跟窗口默认属性
	ZMJ_PORTAL.setInitWindow()
	initWindow.mainloop()

def guiInput(tipString):
	initWindow = Tk()
	ZMJ_PORTAL = inputGUI(initWindow,"Data Input Window",tipString)
	#设置跟窗口默认属性
	ZMJ_PORTAL.setInitWindow()
	initWindow.mainloop()
	print(ZMJ_PORTAL.value)
	return ZMJ_PORTAL.value

def guiConfirm(tipString,doubtfulValueString):
	initWindow = Tk()
	ZMJ_PORTAL = confirmGUI(initWindow,"Data Confirm Window",tipString,doubtfulValueString)
	#设置跟窗口默认属性
	ZMJ_PORTAL.setInitWindow()
	initWindow.mainloop()
	print(ZMJ_PORTAL.value)
	return ZMJ_PORTAL.value








