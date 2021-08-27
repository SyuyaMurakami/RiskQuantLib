#!/usr/bin/python
#coding = utf-8

import pandas as pd
from RiskQuantLib.SecurityList.base import baseList
from RiskQuantLib.Security.Repo.repo import repo
from RiskQuantLib.Set.SecurityList.RepoList.repoList import setRepoList


class repoList(baseList,setRepoList):
    """
    repoList is one of the five basic list classes.
    """
    def __init__(self):
        super(repoList, self).__init__()
        self.listType = 'Repo List'

    def addRepo(self, codeString, nameString, securityTypeString = 'Repo'):
        tmpList = self.all + [repo(codeString,nameString,securityTypeString)]
        self.setAll(tmpList)

    def addRepoSeries(self, repoCodeSeries, repoNameSeries, securityTypeString = 'Repo'):
        repoSeries = [repo(i,j,securityTypeString) for i,j in zip(repoCodeSeries,repoNameSeries)]
        tmpList = self.all + repoSeries
        self.setAll(tmpList)


