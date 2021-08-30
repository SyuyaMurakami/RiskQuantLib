#!/usr/bin/python
#coding = utf-8

from tkinter import *
# import hashlib
# import time

LOG_LINE_NUM = 0

class inputGUI():
	"""
	This GUI is used to input data.
	"""
	def __init__(self,initTkObject,windowTitle,tips):
		self.tkObject = initTkObject
		self.windowTitle = windowTitle
		self.tips = tips

	def setInitWindow(self):
		self.tkObject.title(self.windowTitle)
		self.tkObject.geometry('280x100+500+500')#window size 210*100，position 500,500
		#label
		self.initDataLabel = Label(self.tkObject,text=self.tips)
		self.initDataLabel.grid(row=0,column=0)
		#text box
		self.initDataText = Text(self.tkObject,width=40,height=3)
		self.initDataText.grid(row=0,column=0,rowspan=3,columnspan=3)
		#button
		self.strTansToMD5Button = Button(self.tkObject,text="Submit",bg="lightblue",width=10,command=self.backFunction)#调用内部方法
		self.strTansToMD5Button.grid(row=36,column=0)

	def backFunction(self):
		self.value = self.initDataText.get(1.0,END).strip()
		self.tkObject.destroy()

class confirmGUI():
	"""
	This GUI is used to confirm some information.
	"""
	def __init__(self, initTkObject, windowTitle, tips, valueString):
		self.tkObject = initTkObject
		self.windowTitle = windowTitle
		self.tips = tips
		self.doubtfulValue = valueString

	def setInitWindow(self):
		self.tkObject.title(self.windowTitle)
		self.tkObject.geometry('280x100+500+500')  #window size 210*100，position 500,500
		# label
		self.initDataLabel = Label(self.tkObject, text=self.tips)
		self.initDataLabel.grid(row=0, column=0)
		# button
		self.strTansToMD5Button = Button(self.tkObject, text="Yes", bg="lightblue", width=7, command=self.backFunction)  # 调用内部方法
		self.strTansToMD5Button.grid(row=36, column=0)
		self.strTansToMD5Button = Button(self.tkObject, text="No", bg="lightblue", width=7, command=self.guiStart)  # 调用内部方法
		self.strTansToMD5Button.grid(row=36, column=1)

	def guiStart(self):
		self.tkObject.destroy()
		initWindow = Tk()
		ZMJ_PORTAL = inputGUI(initWindow,"Data Input Window","Input the value you want:")
		# set window default attribute
		ZMJ_PORTAL.setInitWindow()

		initWindow.mainloop()#keep window running
		self.value = ZMJ_PORTAL.value

	def backFunction(self):
		self.value = self.doubtfulValue
		self.tkObject.destroy()

class alertGUI():
	"""
	This class is used to alert some information.
	"""
	def __init__(self,initTkObject,windowTitle,tips):
		self.tkObject = initTkObject
		self.windowTitle = windowTitle
		self.tips = tips

	def setInitWindow(self):
		self.tkObject.title(self.windowTitle)
		self.tkObject.geometry('280x80+500+500')#window size 210*100，position 500,500
		#label
		self.initDataLabel = Label(self.tkObject,text=self.tips)
		self.initDataLabel.grid(row=0,column=0)

def guiAlert(tipString:str):
	"""
	This function will alert some information.
	"""
	initWindow = Tk()
	ZMJ_PORTAL = alertGUI(initWindow,"Alert Window",tipString)
	# set window default attribute
	ZMJ_PORTAL.setInitWindow()
	initWindow.mainloop()

def guiInput(tipString:str):
	"""
	This function will receive some information by GUI.
	"""
	initWindow = Tk()
	ZMJ_PORTAL = inputGUI(initWindow,"Data Input Window",tipString)
	# set window default attribute
	ZMJ_PORTAL.setInitWindow()
	initWindow.mainloop()
	print(ZMJ_PORTAL.value)
	return ZMJ_PORTAL.value

def guiConfirm(tipString:str,doubtfulValueString:str):
	"""
	This function will ask confirmation of some information.
	"""
	initWindow = Tk()
	ZMJ_PORTAL = confirmGUI(initWindow,"Data Confirm Window",tipString,doubtfulValueString)
	# set window default attribute
	ZMJ_PORTAL.setInitWindow()
	initWindow.mainloop()
	print(ZMJ_PORTAL.value)
	return ZMJ_PORTAL.value








