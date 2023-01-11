#!/usr/bin/python
# coding = utf-8
import os

from jinja2 import Environment, FileSystemLoader
class render(object):
    """
    render is a class used to set up jinja2 Environment to render code templates.
    """

    def __init__(self, componentPathString:str):
        """
        Initialize a render, find jinja2 template in componentPathString

        Parameters
        ----------
        componentPathString : str
            path of dictionary where templates exist. Any sub-folder will be searched,
            file and sub-file will be added into template dictionary

        Returns
        -------
        None
        """
        self.componentFindList = [componentPathString]
        for root, dirs, files in os.walk(componentPathString):
            self.componentFindList.extend([root+os.sep+dirc for dirc in dirs if dirc[0]!='_' and dirc[0]!='.'])
        self.loader = FileSystemLoader(self.componentFindList,followlinks=True)
        self.env = Environment(loader=self.loader, block_start_string='#%', block_end_string='%#', comment_start_string='#:', comment_end_string=':#')

    def render(self, templateFileName:str, **kwargs):
        """
        Render a jinja2 template will given kwargs.

        Parameters
        ----------
        templateFileName : str
            path of template file. Any sub-folder will be searched, file and sub-file will be added into template dictionary

        Returns
        -------
        str
        """
        template = self.env.get_template(templateFileName)
        return template.render(**kwargs)













