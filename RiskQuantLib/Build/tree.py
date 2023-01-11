#!/usr/bin/python
# coding = utf-8

class inheritNode(object):
    """
    A link chain node used to hold inherit information.
    """

    def __init__(self, name:str):
        self.name = name
        self.parentNode = []
        self.childNode = []
        self.inheritTree = []
        self.outsideParentNode = []
        self.outsideDependence = []

    def inheritFrom(self, parentNode:list):
        """
        Inherit from one or more node.
        """
        if isinstance(parentNode, inheritNode):
            parentNode = [parentNode]
        if len(parentNode)!=0:
            self.parentNode += parentNode
            [p.childNode.append(self) for p in parentNode]
            inheritTreeNode = [parentNode[0].name] if parentNode[0].name != '' else []
            self.inheritTree = parentNode[0].inheritTree + inheritTreeNode

    def inheritFromOutside(self, outsideParentName:str):
        """
        Inherit from a node which is not a node in current inherit tree.
        """
        self.outsideParentNode.append(outsideParentName) if outsideParentName!='' else None
        return self

    def dependOnOutside(self, outsideDependenceName:str):
        """
        Specify a library which current node depends on.
        """
        self.outsideDependence.append(outsideDependenceName) if outsideDependenceName!='' else None
        return self

    def setAttr(self,attrName:str,attrValue):
        """
        Add an attribute to current node.
        """
        setattr(self,attrName,attrValue)
        return self

    def addAttr(self, dictName:str, attrKey, attrValue):
        """
        Add a (key, value) pair to current attribute dict. If this dict does not exist, it will be created.
        """
        self.setAttr(dictName,{}) if not hasattr(self, dictName) else None
        getattr(self, dictName)[attrKey] = attrValue

    def destroyNode(self, fromDict = {}):
        """
        Delete this node and delete any inherit relationship from its parent nodes and child nodes.
        """
        [setattr(parentNode, 'childNode', [i for i in parentNode.childNode if i is not self]) for parentNode in self.parentNode]
        fromDict.pop(self.name) if self.name in fromDict else None
        [childNode.destroyNode(fromDict=fromDict) for childNode in self.childNode]



class inheritTree(object):
    """
    A link chain used to hold inherit information.
    """

    def __init__(self):
        self.activeNode = None
        self.nodeDict = {}

    def addNode(self, name:str):
        """
        Add a single node into current inherit tree.
        """
        if name not in self.nodeDict:
            self.activeNode = inheritNode(name)
            self.nodeDict[name] = self.activeNode
        return self

    def delNode(self, name:str):
        """
        Delete a node from current inherit tree.
        """
        self.nodeDict[name].destroyNode(fromDict=self.nodeDict) if name in self.nodeDict else None

    def replaceNode(self, name:str):
        """
        Replace a node into a brand new one, and set alive into that node.
        """
        self.activeNode = inheritNode(name)
        self.nodeDict[name] = self.activeNode
        return self

    def inheritFrom(self, parentNode:str or list):
        """
        Select alive node and make it inheriting from one or more nodes in current inherit tree.
        """
        if type(parentNode)==str:
            parentNode = [parentNode]
        if len(parentNode)!=0 and self.activeNode:
            self.activeNode.inheritFrom([self.nodeDict[p] for p in parentNode if p in self.nodeDict])
            deActivitiedNode = self.activeNode
            self.activeNode = None
            return deActivitiedNode

    def getNode(self, name:str):
        """
        Select a node.
        """
        return self.nodeDict[name] if name in self.nodeDict else None

    def getAttr(self, attrName:str, default = None):
        """
        Iterate through nodes and get attribute in every node.
        """
        return [getattr(i,attrName, default) for i in self.nodeDict.values()]

    def getInheritList(self):
        """
        Get the inheritTree attribute of every node.
        """
        return self.getAttr('name'), self.getAttr('inheritTree')

    def getParentInheritListSeries(self):
        """
        Iterate through every node and get the inheritTree of every parent of that node.
        """
        return [[j.name for j in i.parentNode] for i in self.nodeDict.values()], [[j.inheritTree for j in i.parentNode] for i in self.nodeDict.values()]














