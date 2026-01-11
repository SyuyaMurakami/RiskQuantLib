Process Graph-Structure Data
=========================================

.. toctree::
   :maxdepth: 4

Fundamentals of Graph-Structure Data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generally when we talk about databases, the first impression is usually SQL. As a common query language for **relational** databases, SQL has been widely developed and used in the past decades. But as its name suggests, it is only a query method for relational databases, while other types of databases, such as graph databases, use Cypher as a query language. If we open our minds, we realize that data is not only handled in a relational way.

In many cases, relational data is indeed the easiest data structure for people to understand and manipulate. Any table-like data, for example, excel document, can be seen as relational data. They are typically characterized by data stored in the form of rows and columns, with fixed relationships between the data in each row, and these relationships are usually identified by column names.

However, as data science advances, in more and more cases, the relationships between data become less standardized. You may have noticed that it is not always the most convenient way to save data in a matrix form like rows and columns at all times. You may find that certain rows have a lot of null values, or that the length of the previous row is not equal to the length of the next row (Excel may deal with this by merging cells). But if we think carefully, we will find that the so-called null value often comes from the lack of relationship, that is, in that line does not actually exist in such a relationship. And further thinking will allow us to realize that the null value comes from the way we use data, that is, to force the data to be presented as rows and columns. By this, the relationship that should never exist must occupy a position, the value of this position can only be null.

**So it's time we start recognizing that data doesn't always behave in a relational form like a matrix, nor should it.**

Graph data structures are a good alternative to relational data structures. It origins from Set Theory. The most basic concepts in graph data structures are **Node** and **Edge**, a node is a unit used to store static data, while an edge usually represents a relationship between nodes. For example, if we have a node called ``human`` , and nodes named as ``father`` and ``son`` , then we can use two edges to link them. These links represent the truth that ``human`` includes ``father`` and ``son``.

You can find a lot of information about graph-structure data, so we won't go into it here. The well-known graph-structure database Neo4j provides a lot of material for introducing graph-structure data. You may find them in official website.

One More Step With RiskQuantLib
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

RiskQuantLib uses ``Instrument`` and ``Instrument List`` to process and analyze data, but if we stop there, then RiskQuantLib's functionality will be very limited. To realize the full potential of RiskQuantLib, we need to treat ``Instrument`` and ``Instrument List`` in a different way:

    `The Instrument and Instrument List are not just a python class file, they are also node of graph-structure data in RiskQuantLib.`

This is the core design of RiskQuantLib. There are two layers of any type of node (you can also call these two layers together as one node), the top-level ``Instrument List`` and the bottom-level ``Instrument`` . The top-level ``Instrument List`` is typically used to handle relationships within nodes of the ``Instrument`` , while the bottom-level ``Instrument`` acts as a specific standalone node, responsible for interacting with other types of nodes or performing operations under its own scope.

RiskQuantLib add edges between nodes through four key functions: ``join``, ``match``, ``connect`` , ``link`` :

*Join*
-------------

``join`` is a function used to build **one-way link** between two nodes.

If ``stockListA`` is an instance of ``stockList`` , while ``companyListB`` is an instance of ``companyList`` , and we still have a dictionary named as ``stockIPODetail``, whose key is name of company and value is name of stock issued by that company, for example, company A issued a stock named 123.HK. Notice here, the same company may issue shares with different name on two different exchanges, for example, it was once a popular thing to be listed on both the New York Stock Exchange and the Hong Kong Stock Exchange. The return value of ``stockIPODetail[companyName]`` is a python list, whose element is the stock code that issued by that company, and sorted by ascending order.

``join`` is the attribute function of any InstrumentList, you can use it with any instance of InstrumentList, only need to pass parameters like:
::

    riskQuantLibList.join(anotherList, targetAttrName, filterFunction)

When you call this function, for every element ``Ai`` of ``riskQuantLibList`` , RiskQuntLib will find those element from ``anotherList`` , which satisfy given conditions, and then use these element to initialize a new instance of InstrumentList, then set this instance as an attribute of element ``Ai`` . The name of attribute is ``targetAttrName`` , and the condition used to filter element is ``filterFunction`` , which is a function that return a bool value. For example:
::

    companyListB.join(stockListA, 'issuedStock', lambda company, stock: stockIPODetail[company.name]==stock.stockBelongToSameCompany)

After you call this function, every element of ``companyListB`` , which is an instance of ``company`` , will be added one more attribute named as ``issuedStock``, the value of this attribute is an instance of ``stockList`` , which contains all stock that issued by that company. If that company never issued shares, then the length of ``stockList`` will be 0.

*Match*
------------

``match`` is a vectorized version of ``join`` , so that it is usually faster. Use the same example:
::

    riskQuantLibList.match(anotherList, targetAttrName, matchFunctionOnLeft, matchFunctionOnRight)

When you call this function, first, for every element ``Ai`` of ``riskQuantLibList`` , which is an instance of ``company`` , this element will be passed to ``matchFunctionOnLeft`` and get result as P. Second, for every element of ``anotherList`` , which is an instance of ``stock`` , that element will be passed to ``matchFunctionOnRight`` and get result as Q. Finally, those element from ``anotherList`` that satisfy P==Q will be used to initialized a new instance of  ``stockList`` , and setted as an attribute of ``Ai`` . The name of attribute is ``targetAttrName`` . For example:
::

    companyListB.match(stockListA, 'issuedStock', lambda company:stockIPODetail[company.name], lambda stock: stock.stockBelongToSameCompany)

When you run this, each element of ``companyListB``, which is an instance of ``company`` , will have an additional attribute called ``issuedStock`` , whose value is an instance of ``stockList`` , which contains all stock issued by that company. If that company never issued shares, then the length of ``stockList`` will be 0.

``match`` **sacrifices flexibility, notice that not every matching condition can be rewritten in a decoupled form.**

*Connect*
-----------------

``connect`` is a function used to build **both-way link** between two nodes.

Just like ``join`` , ``connect`` is also the attribute function of any InstrumentList, you can use it with any instance of InstrumentList, only need to pass parameters like:
::

    riskQuantLibList.connect(anotherList, targetAttrNameOnLeft, targetAttrNameOnRight, filterFunction)

When you call this function, for every element ``Ai`` of ``riskQuantLibList`` , RiskQuntLib will find those element from ``anotherList`` , which satisfy given conditions, and then use these element to initialize a new instance of InstrumentList, then set this instance as an attribute of element ``Ai`` . The name of attribute is ``targetAttrNameOnLeft`` , and the condition used to filter element is ``filterFunction`` , which is a function that return a bool value. 

Then, for every element ``Bi`` of ``anotherList`` , RiskQuntLib will find those element from ``riskQuantLibList`` , which satisfy given conditions, and then use these element to initialize a new instance of InstrumentList, then set this instance as an attribute of element ``Bi`` . The name of attribute is ``targetAttrNameOnRight`` , and the condition used to filter element is also ``filterFunction`` .

For example:
::

    companyListB.connect(stockListA, 'issuedStock', 'issuedBy', lambda company, stock: stockIPODetail[company.name]==stock.stockBelongToSameCompany)

After you call this function, every element of ``companyListB`` , which is an instance of ``company`` , will be added one more attribute named as ``issuedStock``, the value of this attribute is an instance of ``stockList`` , which contains all stock that issued by that company. If that company never issued shares, then the length of ``stockList`` will be 0.

At the same time, every element of ``stockListA`` , which is an instance of ``stock`` , will be added one more attribute named as ``issuedBy``, the value of this attribute is an instance of ``companyList`` , which contains the issuer of that stock. Usually one stock can only be issued by one issuer, so the length of ``stockList`` will be 1.

*Link*
--------------
``link`` is a vectorized version of ``connect`` , so that it is usually faster. Use the same example:
::

    riskQuantLibList.link(anotherList, targetAttrNameOnLeft, targetAttrNameOnRight, matchFunctionOnLeft, matchFunctionOnRight)

When you call this function, first, for every element ``Ai`` of ``riskQuantLibList`` , which is an instance of ``company`` , this element will be passed to ``matchFunctionOnLeft`` and get result as P. Second, for every element ``Bi`` of ``anotherList`` , which is an instance of ``stock`` , that element will be passed to ``matchFunctionOnRight`` and get result as Q. 

Finally, those element from ``anotherList`` that satisfy P==Q will be used to initialized a new instance of  ``stockList`` , and setted as an attribute of ``Ai`` . The name of attribute is ``targetAttrNameOnLeft`` . Those element from ``riskQuantLibList`` that satisfy P==Q will be used to initialized a new instance of  ``companyList`` , and setted as an attribute of ``Bi`` . The name of attribute is ``targetAttrNameOnRight`` .

``link`` **sacrifices flexibility, notice that not every matching condition can be rewritten in a decoupled form.**

**Let's work together on a task with more complex data relationships. This will give you an idea of how RQL uses graph structure data, two-layer nodes, string puppets (pointers), and other designs to make problems simple.**

A Text Counting Project
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's say you're an ESG researcher of company. ESG means Environment, Society, Government. You are reviewing ESG reports of some company and you know some key words in these report will lead to higher ESG ratings for companies. Prior to the analysis, your strict supervisor makes some head-scratching demands. He believes that only a subset of words, rather than all of them, can reflect the behavior of a company in conducting environmental protection, and these words should meet the following criteria:
::

    1.In more than 75% of all companies, the word appears at least 1 time. This implies that the word may have some relevance to embodying ESG behaviors.
    2.The word is not specific to a particular industry. This means that the word should not appear significantly more often in any one industry than in others.


You have now gathered some industry information on Japanese listed companies, saved as ``JP.xlsx`` . You still have a file showing which words are used in ESG report of that company, saved in some ``.txt`` files. Your data may be like:

+---------+-------------------+---------------------------------+
| Company |     Industry      |     	  E Using Words         |   
+=========+===================+=================================+
|  Asahi  |  Chemical Product | fuel, air, efficiency, coast,...|     
+---------+-------------------+---------------------------------+
|  Chubu  |  Electric Power   | carbon, nature, cloud,...       |
+---------+-------------------+---------------------------------+
|  ...    |       ...         |      ...                        |
+---------+-------------------+---------------------------------+

To finish a task that is complicated like this, you decide to use RiskQuantLib. You open terminal and type ``newRQL path\myESG`` to start a new project. Then you edit ``config.py`` and `Build Your Project <https://riskquantlib-doc.readthedocs.io/en/latest/Build_Project.html>`_ to generate ``company`` and ``industry`` class.

``config.py`` looks like:
::

    #-|instrument: industry, company

You want to add attribute of ``industry`` and ``usedWords`` to ``company`` . After ``build`` , any instance of  ``company`` will have method of ``set`` .

To do this, add declaration to ``config.py`` and make it look like:
::

    #-|instrument: industry, company
    #-|attribute: company.industry@string, company.usedWords

Run ``build.py`` with python to automatically create classes you need and add attributes you want. Then open ``main.py`` to start your data analyse. By this time, ``main.py`` looks like:

``main.py``
::

    import os
    import sys
    from RiskQuantLib.module import *
    path = sys.path[0]

A common design framework for an RQL project is Data Input, Data Analysis and Data Output. You try to design code using such a framework.

*Data Input*
-------------------

Let's start by importing the data. To make it easier to set the values of the instances in bulk later, we often import the properties as iterative objects in the same order as the instances (i.e., if company A appears in the 3rd position of the list of companies, then company A's ``usedWords`` property should also appear in the 3rd position of the ``usedWords`` list). So we design the ``usedWords`` for companies as a list as follows.

``main.py``
::

    import pandas as pd
    df = pd.read_excel(r".\Data\JP.xlsx")
    def input_text(dirpath): 
        words = []
        with open(dirpath + os.sep + "noun.txt", 'r') as f:
            for item in f:
                words.append(item[:-1])
        return words

    companies = df["Name"]
    industries = df["Industry"]
    companies_words = [input_text(r".\Data\{0}".format(i)) for i in companies]

Instantiate ``company_list`` and ``industry_list`` and add elements to them using the ``add`` function family, which also adds the ``code`` attribute to the elements for identification purposes. The ``set`` function family can be used to add ``industry`` attribute and the ``usedWords`` attribute to the ``company`` element of the ``company_list``.
``main.py``
::

    company_list = companyList()
    company_list.addCompanySeries(companies, companies)
    company_list.setIndustry(companies, industries)
    company_list.setUsedWords(companies, companies_words)

    industry_list = industryList()
    industry_list.addIndustrySeries(industries, industries)

You can use ``company_list[code]`` or ``company_list[0]`` during debug to find the corresponding ``company`` element (returning an instance of ``company``).

``main.py``
::

    company_list["Asahi"]
    # or company_list[0]

When examining the property of ``company`` , you find that there are some company for which the ``wordsList`` has a length of 0, which indicates that there is missing data for this company. You decide to filter out these elements with the ``filter`` function of the ``Instrument List`` . When ``filter``'s parameter ``useObj`` is ``True``, his result is still an ``Instrument List`` . so you continue typing in ``main.py``:

``main.py``
::

    company_list = company_list.filter(lambda company:len(company.usedWords) != 0, useObj=True)

*Data Analysis*
--------------------

Let's then move on to the (complicated) process of analyzing. You decided to start by counting the frequency of words used for each company. You opened ``RiskQuantLib/Instrument/Company/company.py`` and added a ``countUsedWords`` method to the ``Company`` class as follows:

``RiskQuantLib.Instrument.Company.company``
::

    class company(setCompany):
        ...
        def countUsedWordsDict(self):
            from collections import Counter
            self.usedWordsDict = Counter(self.usedWords)

You write ``company_list.exec("countUsedWords") `` in ``main.py``, calling ``countUsedWords`` method for each element in the list. Each of your ``Company`` elements gets the additional attribute ``usedWordsDict`` as a result.

``main.py``
::

    company_list.execFunc("countUsedWordsDict")

To fulfill boss's requirement 1, you need to count which words appear at least once in at least 75% of companies. You open ``RiskQuantLib/InstrumentList/CompanyList/companyList.py`` and add a method to ``Company_list`` as follows.

``RiskQuantLib.InstrumentList.CompanyList.companyList``
::

    class companyList(listBase,setCompanyList):
    ...
    def rule_one(self):
        threshold = len(self.all) * 0.75

        from collections import Counter
        word_dict = Counter()
        for company in self.all:
            word_dict.update({word:1 for word in company.usedWordsDict.keys()})

        self.rule_one = [word for word in word_dict.keys() if word_dict[word] > threshold]

Calling the ``rule_one`` method of ``company_list`` in ``main.py`` adds an attribute ``rule_one`` to ``company_list``.

``main.py``
::

    company_list.rule_one()

After that, you decide to use RQL's ``connect`` function to link certain related elements in ``company_list`` and ``industry_list``, making them callable as attributes of each other, which is one of the core ideas of RQL (graph-structured data stores). You enter the code as follows:

``main.py``
::

    company_list.connect(industry_list, 
                         targetAttrNameOnLeft="industryObj",
                         targetAttrNameOnRight="companiesObj",
                         filterFunction=lambda x,y:x.industry == y.name)

We can see that each ``company`` element has a new attribute ``industryObj``, and the ``industry`` element has a new attribute ``companiesObj``, and they are both RQL lists.

You decide to start by counting the average word usage by companies in each industry, and you add a method to the ``RiskQuantLib/Instrument/Industry/industry.py``, in the ``industry`` class as follows:

``RiskQuantLib.Instrument.Industry.industry``
::

    class industry(setIndustry):
        ...
        def countAvgWords(self):
            from collections import Counter
            countWords = Counter()
            [countWords.update(company.usedWords) for company in self.CompaniesObj]
            self.avgWords = {word:countWords[word]/len(self.CompaniesObj.all) for word in countWords.keys()}

You write ``industry_list.execFunc("avgCountWords")`` in ``main.py``, calling its ``countAvgWords`` method for each element in the list. Each of your ``Industry`` elements will thus get the new attribute ``avgWords``.

``main.py``
::

    industry_list.execFunc("countAvgWords")

You want to fulfill boss's request 2, for each word in ``company_list.rule_one``, you need to go through and check if it occurs significantly more often in a particular industry. You decide to count how often each word is used in each industry, and you open ``RiskQuantLib/InstrumentList/IndustryList/industryList.py`` and add a method ``removeBiasWords`` to ``Industrylist`` as follows. ``RemoveBiasWords`` as follows:

``RiskQuantLib.InstrumentList.IndustryList.industryList``
::

    class industryList(listBase,setIndustryList):
        ...
        def rule_two(self, rule_one, n_sigma=2):
            self.rule_two = []
            for word in rule_one:
                frequency_list = [industry.avgWords[word] if industry.avgWords.get(word, -1) != -1 else 0 for industry in self.all]
                if max(frequency_list) < np.mean(frequency_list) + n_sigma * np.std(frequency_list):
                    self.rule_two.append(word)

After the calling of ``Industry_list.rule_two``, ``industry_list`` adds an attribute ``rule_two``.

``main.py``
::

    industry_list.rule_two(rule_one = company_list.rule_one)

So you can use this list of words that satisfy the leader's requirements to do the filtering! You define the following function ``findUsefulWords`` in the ``company`` class:

``RiskQuantLib.Instrument.Company.company``
::

    class company(setCompany):
        ...
        def findUsefulWordsDict(self, rule_two):
            self.usefulWordsDict = {word:self.usedWordsDict[word] for word in self.usedWordsDict.keys() if word in rule_two}

After calling ``company_list.execFunc("findUsefulWords", industry.rule_two)``, each business gets the property ``usefulWordsDict``.

``main.py``
::

    company_list.execFunc("findUsefulWords", industry.rule_two)

*Data Output*
-----------------

This is the word list that satisfies the leader's requirements, and we can use him for following research now!

Summary
^^^^^^^^^^^

Let's review the whole process of the project:
::
    1. Think about the structural relationships and attributes of the node classes, modify the config.py file and run build.py.
    2. Import data. Instantiate RQLlist (Instrument List) and add elements, use set function family to set properties of element nodes.
    3. Start analyzing. **Roundtrip** or **Jump** Between main.py and each node (company and industry in this project), design various methods for element nodes and list nodes. And the result of calling the methods is setted as an attribute on that node (or any other location).
    4. Repeat the process of 3 until you get the final result.
    5. Export the data.

RiskQuantLib is designed to provide the user with a customized data analysis model, and what design to use depends on the data problem the user is facing.

