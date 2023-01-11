#!/usr/bin/python
#coding = utf-8
import requests,os
#<import>
#</import>

def downloadRepo(url:str, targetPath:str, name:str = ''):
    """
    This function will use Github api to download zip file of repositories.

    Parameters
    ----------
    url : str
        The total github api link of some repository
    targetPath : str
        The file path where you want to save the zip clone
    name : str
        The repository name you want to download

    Returns
    -------
    None
    """
    headers = {
        'Accept': 'application/vnd.github.v3+json',
    }
    response = requests.get(url+r'/zipball',headers=headers)
    if response.status_code==200:
        with open(targetPath, "wb") as file:
            file.write(response.content)
        print("Successfully Installed " + name)
    else:
        print("Failed to Install " + name)

#<githubTool>
#</githubTool>

class Github(object):
    """
    This class is used to do operations of Github with github api.
    """
    def __init__(self):
        """
        For basic use of search, establish url.
        """
        self.URLformer = r'https://api.github.com/search/repositories?q='
        self.URLender = r'sort=stars&order=desc'

    def searchRepositories(self, repositoryKeyWord = '', output = True):
        """
        This function will send request to search Github and find all repositories that
        can be related to given key words. All repositories are sorted by star numbers.
        The first one is the most starred one.

        Parameters
        ----------
        repositoryKeyWord : str
            The key words used to search Github.
        output : bool
            Whether to print all repositories names.

        Returns
        -------
        None
        """
        if repositoryKeyWord == '':
            pass
        else:
            repositoryKeyWord = repositoryKeyWord.replace(' ','+') + '&'
        self.URL = self.URLformer + repositoryKeyWord +self.URLender
        response = requests.get(self.URL)
        dataDict = response.json()
        print("Total repositories: ", dataDict['total_count'])
        repoDicts = dataDict['items']
        data = {}
        for repoDict in repoDicts:
            data[repoDict['name']] = [repoDict['stargazers_count'], repoDict['html_url'], repoDict['created_at'], repoDict['default_branch'], repoDict['size'], repoDict['url']]
        self.data = data
        if output:
            hints = "Show Top Github Repositories: "
            print(hints, '\n', "".join(['-' for i in range(len(hints))]))
            [print(index, "->", name) for index, name in enumerate(list(self.data.keys()))]

    def downloadRepositories(self, repositoryIndex, targetPath: str):
        """
        This function will download the repository specified by repositoryIndex. The downloaded
        file is in zip form and will be saved to targetPath.

        Parameters
        ----------
        repositoryIndex : int or str
            The number of repository index. Or a string to specify the link of github web page.
            Or the name of a repository. Or any key word that can be used to search github.
        targetPath : str
            The path where zip file will be saved.

        Returns
        -------
        None
        """
        if type(repositoryIndex) == int:
            name = list(self.data.keys())[repositoryIndex]
            downloadRepo(self.data[name][5], targetPath+os.sep+name+'.zip', name)
        elif type(repositoryIndex) == str and repositoryIndex.find(r'https://github.com')!=-1:
            user = repositoryIndex.split(r'/')[3]
            name = repositoryIndex.split(r'/')[4]
            url = r"https://api.github.com/repos/" + user + r"/" + name
            downloadRepo(url, targetPath + os.sep + name + '.zip', name)
        else:
            self.searchRepositories(repositoryIndex, False)
            if len(self.data.keys()) == 0:
                print("There Is No Such Project Found In Github")
            else:
                name = list(self.data.keys())[0]
                if repositoryIndex == name:
                    downloadRepo(self.data[name][5], targetPath + os.sep + name + '.zip', name)
                else:
                    hints = "Show Top Github Repositories: "
                    print(hints, '\n', "".join(['-' for i in range(len(hints))]))
                    [print(index, "->", name) for index, name in enumerate(list(self.data.keys()))]
                    answer = input("Choose One From Above:")
                    name = list(self.data.keys())[int(answer)]
                    downloadRepo(self.data[name][5], targetPath + os.sep+ name + '.zip', name)

    #<Github>
    #</Github>









