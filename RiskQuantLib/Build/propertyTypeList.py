#!/usr/bin/python
#coding = utf-8
import os,importlib

class propertyTypeList():
    """
    propertyTypeList() is a class used to format propertyType building information and commit building.
    This is the entrance of new propertyType building action.
    """

    def __init__(self):
        """
        Any 'RiskQuantLib List' object should have self.all, which is a list to contain elements.
        """
        self.all = []

    def addPropertyType(self,propertyTypeNameSeries):
        """
        addPropertyType(self,propertyTypeNameSeries) is a function to add new propertyType registrations.

        Parameters
        ----------
        propertyTypeNameSeries : iterable object
            This variable must be an iterable object and each element should be a string, specifying
            the name of propertyTypes.

        Returns
        -------
        None
        """
        import RiskQuantLib.Build.pathObj as POJ
        importlib.reload(POJ)
        RQLpathObj = POJ.pathObj()
        from RiskQuantLib.Build.propertyTypeObj import propertyTypeObj
        self.all += [propertyTypeObj(i) for i in propertyTypeNameSeries if i[0].capitalize()+i[1:] not in RQLpathObj.attributeTypeDefaultList]
        del RQLpathObj

    def setLibraryName(self,propertyTypeNameSeries,libraryNameSeries):
        """
        setLibraryName(self,propertyTypeNameSeries,libraryNameSeries) is a function to
        set other library you want to use in new propertyType class.

        Parameters
        ----------
        propertyTypeNameSeries : iterable object
            This variable must be an iterable object and each element should be a string, specifying
            the name of propertyTypes.
        libraryNameSeries : iterable object
            This variable must be an iterable object and each element should be a string, specifying
            the library you want to include in propertyType class file. If multiple classes are included,
            they should be within one string, separated by ','. Note: The length of libraryNameSeries
            must be equal to that of propertyTypeNameSeries.

        Returns
        -------
        None
        """
        tmpDict = dict(zip(propertyTypeNameSeries,libraryNameSeries))
        [i.setLibraryName(tmpDict[i.name]) if i.name in tmpDict.keys() else i.setLibraryName('') for i in self.all]

    def commit(self,targetProjectPath:str = ''):
        """
        commit(self,targetProjectPath:str = '') is a function to
        commit building of new propertyTypes.

        Parameters
        ----------
        targetProjectPath : str
            The RiskQuantLib project path where you want to build new propertyTypes.

        Returns
        -------
        None
        """
        from RiskQuantLib.Build.buildPropertyType import clearPropertyTypePath
        clearPropertyTypePath(targetProjectPath)
        [i.commit(targetProjectPath) for i in self.all]















