#!/usr/bin/python
#coding = utf-8

from RiskQuantLib.Set.Security.Repo.repo import setRepo
from RiskQuantLib.Security.base import base

class repo(base, setRepo):
    """
    repo is one of the five basic classes.
    """
    def __init__(self,codeString,nameString,securityTypeString = 'Repo'):
        base.__init__(self,codeString,nameString,securityTypeString)






