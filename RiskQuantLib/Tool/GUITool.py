#!/usr/bin/python
#coding = utf-8

import easygui

#<import>
#</import>


def guiAlert(tipString:str):
    """
    This function will alert some information.
    """
    easygui.msgbox(msg=tipString, title="Alert Window", ok_button="OK")


def guiInput(tipString:str):
    """
    This function will receive some information by GUI.
    """
    value = easygui.enterbox(msg=tipString, title="Data Input Window")
    result = "" if value is None else value 
    return result

def guiConfirm(tipString:str,doubtfulValueString:str):
    """
    This function will ask confirmation of some information, if rejected, it will ask user to input a new one.
    """
    choice = easygui.ynbox(msg=tipString, title="Data Confirm Window", choices=["Yes", "No"])
    result = doubtfulValueString if choice else guiInput("Input the value you want:")
    return result

def guiSelect(tipString:str,doubtfulValueList:list):
    """
    This function will give some options to user to choose.
    """
    choice = easygui.choicebox(tipString, title="Choice Select Window", choices=doubtfulValueList)
    return "" if choice is None else choice

#<guiTool>
#</guiTool>






