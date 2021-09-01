..
   Note: Items in this toctree form the top-level navigation. See `api.rst` for the `autosummary` directive, and for why `api.rst` isn't called directly.

.. toctree::
   :hidden:

   Home page <self>
   modules.rst
   Install.rst
   Create_Project.rst

Welcome to Use RiskQuantLib
===========================

RiskQuantLib is a derivative of Quantlib, a famous quantitative library of financial engineering. Unlike QuantLib, however, RiskQuantLib is a scaffolding of financial analysis. RiskQuantLib provides default class of financial instruments and allows you to create new classes you want automatically, given the inheritance rules and other information. It also provides automation building tools to add attributes to classes automatically.

Why Should I Use RiskQuantLib?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* RiskQuantLib provides with convenient way of object oriented coding in fields of finance.
* RiskQuantLib is designed on the base of QuantLib, you can use the functions of QuantLib and combine it with RiskQuantLib easily.
* RiskQuantLib is a scaffolding, which means it creates an independent project for every mission. After creation, RiskQuantLib will be a part of your code. You have full access to your project and can change any source code of RiskQuantLib.
* RiskQuantLib is suitable for applying to different markets, since all financial instruments are defined by your self.
* RiskQuantLib allows you to seperate data analysis process. With RiskQuantLib, data storage, data input, data analysis, data output can be operated independently from each other. You don't have to wait for data input to analysis your data, instead of that, starting coding the analysis logic part before you know the data patterns.
* RiskQuantLib provides template management function. You can code a template of any mission, such as stock return analysis, and save this template into RiskQuantLib, or share it with other users. Next time you meet with a similar data process problem, you can start a new RiskQuantLib project based on this template.

Who Can Use RiskQuantLib?
^^^^^^^^^^^^^^^^^^^^^^^^^

RiskQuantLib is designed to allow analyst to code easily, it's recommanded to be used by financial analyst, students in business school or quant-traders. It's very useful when dealing with analysis of multiple kinds of financial instruments.

**Notice: RiskQuantLib is not designed to dealing with heavy data prcoess mission. RiskQuantLib sacrifice memory and speed to accelerate coding.**

Slow Start
^^^^^^^^^^^

Suppose you are employeed by a bank. One day, your bose calls you to his office, he tells you your company want to invest in a new family fund, Archegos, we suppose it is. Your mission, if you accept, is to tell your boss how risky this deal is.

 `Take adventure after second thought, this is far from recklessness.`

After some investigation, you find some data from Bloomberg, however, it only tells you about some stock holdings of the whole fund, like Tencent or Alibaba, etc. The first dataframe you have is like this:

+------------+--------------------+------------------+
| Index      | Holding Mkt Value  | Stock            |
+============+====================+==================+
| 0          |    239018292       | TCEHY US Equity  |
+------------+--------------------+------------------+
| 1          |    710281723       | ABC US Equity    |
+------------+--------------------+------------------+
| 2          |      7497233       | HIYJ US Equity   |
+------------+--------------------+------------------+
| 3          |    179321234       | SPACEX US Equity |
+------------+--------------------+------------------+
| 4          |        83249       | HE US Equity     |
+------------+--------------------+------------------+

After this, you decided to download the close price of these stocks over past three years, you get your second dataframe like this:

+------------+-----------------+------------------+-----------------+
| Date       | HIYJ US Equity  | U7HJ US Equity   |  HE US Equity   |
+============+=================+==================+=================+
| 2020-01-01 |       23.9      |       nan        |        9.8      |
+------------+-----------------+------------------+-----------------+
| 2020-01-02 |        nan      |      12.8        |        9.5      |
+------------+-----------------+------------------+-----------------+
| 2020-01-03 |       21.9      |      13.1        |        9.3      |
+------------+-----------------+------------------+-----------------+
| 2020-01-04 |       22.1      |      13.2        |        9.7      |
+------------+-----------------+------------------+-----------------+
| 2020-01-05 |       22.4      |      12.9        |        9.8      |
+------------+-----------------+------------------+-----------------+
|    ...     |       ...       |      ...         |        ...      |
+------------+-----------------+------------------+-----------------+

You decide to calculate the volatility of stocks of Archegos holdings. So you start coding like:
::

   df_stock_holding = pd.read_excel(path_one)
   df_stock_close = pd.read_excel(path_two)

If you don't use RiskQuantLib, you may do it like:
::

   df_std = df_stock_close.std()
   std_of_archegos_stock_holdings = df_std[df_stock_holding.columns.to_list()]

Now you are satisfied with what you have done, it seems the risk of stocks can be revealed, at least to some extend. In the afternoon, your boss tells you that he knows Archegos holds two famous fund, called H and JK. He says this is a material non-public information, you may not find net asset value of these two funds by yourself, luckily, your boss has his own way. He gives you the data, which is the third dataframe and it looks like:

+------------+--------------------+------------------+
| Index      |   Net Asset Value  |    Fund          |
+============+====================+==================+
| 0          |        2.39        |         H        |
+------------+--------------------+------------------+
| 1          |        7.22        |        JK        |
+------------+--------------------+------------------+
| 2          |        0.98        |       UIH        |
+------------+--------------------+------------------+
| ...        |         ...        |       ...        |
+------------+--------------------+------------------+

Archegos holding shares of these funds are the fourth dataframe, which looks like:

+------------+--------------------+------------------+
| Index      | Holding Shares     | Fund             |
+============+====================+==================+
| 0          |      20000000      | H                |
+------------+--------------------+------------------+
| 1          |      45000000      | JK               |
+------------+--------------------+------------------+
| ...        |         ...        |       ...        |
+------------+--------------------+------------------+

Your colleague who used to finish a project, focusing on the historical NAV extreme dropdown of all mutual funds, and he tells you that you can use 1.5% as a one-day 99% VaR. So you calculate risk indicator by:
::

   df_fund_holding = pd.read_excel(path_four)
   df_fund_nav = pd.read_excel(path_three)

   df_fund = pd.merge(df_fund_holding, df_fund_nav, on = 'Fund', how = 'left')
   df_fund['Total Holding'] = df_fund['Holding Shares'] * df_fund['Net Asset Value']
   df_fund['VaR'] = df_fund['Total Holding'] * 0.015

Now you have used all kinds of information you can get, since Archegos barely publish their holdings. You give your boss the analysis result and waiting to be praised. However, your boss is pissed off. He takes a long time to calm down and tells you that you forget sever important things:


* `The price of stock contains nan, you have to deal with it. And don't fill nan with last non-nan value, because this will lead to a smaller std than true value.`
* `He wants a conclusion of risk of Archegos, not all kinds of risk indicators.`
* `The stock price you used is wrong, cause it is a divident-included price.`
* `The only reason Archegos buys these two funds is that Archegos can use it as a bridge to buy more shares of stocks, like TCEHY US Equity, this is a trick to use leverage. So you have to take a closer look, dig down to the holdings of these two funds.`

Things get to complicated now. You decide to use RiskQuantLib. First of all, you make a dictionary to hold this analysis project, named 'Archegos_Risk'. Then you open a command terminal, and create a RiskQuantLib project by:
::

   newRQL Archegos_Risk

After this, the dictionary looks like:
::

   --Archegos_Risk
     --RiskQuantLib
     --build.py
     --main.py
     --Build_Attr.xlsx
     --Build_Instrument.xlsx

Open ``Build_Attr.xlsx``, you edit it and make it looks like:

+--------------+----------------+----------------+
| SecurityType |    AttrName    |    AttrType    |
+==============+================+================+
|     Fund     | netAssetValue  |     Number     |
+--------------+----------------+----------------+
|     Fund     |        amount  |     Number     |
+--------------+----------------+----------------+
|     Fund     | varPercentage  |     Number     |
+--------------+----------------+----------------+
|    Stock     |      mktValue  |     Number     |
+--------------+----------------+----------------+
|    Stock     |   closeSeries  |     Series     |
+--------------+----------------+----------------+

You close this file and build this project in command terminal:
::

   python build.py

After this, you open ``RiskQuantLib.Security.Fund.fund`` to add class function:
::

   def calVaR(self):
      self.VaR = self.netAssetValue * self.amount * self.varPercentage

You open ``RiskQuantLib.Security.Stock.stock`` to add class function:
::

   def calVaRPercentage(self):
      from RiskQuantLib.Tool.mathTool import percentageOfSeries
      self.varPercentage = percentageOfSeries(self.closeSeries.dropna().values(),99)

   def calVaR(self):
      self.VaR = self.mktValue * self.varPercentage

**Notice: All these coding are done before you input your data.**

Turn into root path of this project and open ``main.py``, we start analysis:
::

   from RiskQuantLib.Module import *

   # Read files
   df_stock_holding = pd.read_excel(path_one)
   df_stock_close = pd.read_excel(path_two)
   df_fund_holding = pd.read_excel(path_four)
   df_fund_nav = pd.read_excel(path_three)

   # Initialize RQL list object
   fund_holdings = fundList()
   stock_holdings = stockList()

   # Add securities to list
   fund_holdings.addFundSeries(df_fund_holding['Fund'],df_fund_holding['Fund'])
   stock_holdings.addStockSeries(df_stock_holding['Stock'],df_stock_holding['Stock'])

   # Set input
   fund_holdings.setNetAssetValue(df_fund_nav['Fund'],df_fund_nav['Net Asset Value'])
   fund_holdings.setAmount(df_fund_holding['Fund'],df_fund_holding['Holding Shares'])
   stock_holdings.setMktValue(df_stock_holding['Stock'],df_stock_holding['Holding Mkt Value'])
   stock_holdings.setCloseSeries(df_stock_close)
   [fund.setVarPercentage(0.15) for fund in fund_holdings]

   # Calculation
   fund_holdings.execFunc('calVaR')
   stock_holdings.execFunc('calVaRPercentage')
   stock_holdings.execFunc('calVaR')

Now it's more easy to read and modify, isn't it? You decide to continue and save your result into excel, so you code:
::
   
   # Data output
   result = stock_holdings + fund_holdings
   df_result = pd.DataFrame(result[['code','VaR']])
   df_result.to_excel(path)

Till now, the process looks more complicated than a pandas way, however, if you noticed, with RiskQuantLib, data input, data process, data output is independent, change to any of them won't influence the others. Let's take a closer look:

*Data Input*:

``main.py``:
::

   from RiskQuantLib.Module import *

   # Read files
   df_stock_holding = pd.read_excel(path_one)
   df_stock_close = pd.read_excel(path_two)
   df_fund_holding = pd.read_excel(path_four)
   df_fund_nav = pd.read_excel(path_three)

   # Initialize RQL list object
   fund_holdings = fundList()
   stock_holdings = stockList()

   # Add securities to list
   fund_holdings.addFundSeries(df_fund_holding['Fund'],df_fund_holding['Fund'])
   stock_holdings.addStockSeries(df_stock_holding['Stock'],df_stock_holding['Stock'])

   # Set input
   fund_holdings.setNetAssetValue(df_fund_nav['Fund'],df_fund_nav['Net Asset Value'])
   fund_holdings.setAmount(df_fund_holding['Fund'],df_fund_holding['Holding Shares'])
   stock_holdings.setMktValue(df_stock_holding['Stock'],df_stock_holding['Holding Mkt Value'])
   stock_holdings.setCloseSeries(df_stock_close)
   [fund.setVarPercentage(0.15) for fund in fund_holdings]

*Data Analysis*

``RiskQuantLib.Security.Fund.fund``:
::

   def calVaR(self):
      self.VaR = self.netAssetValue * self.amount * self.varPercentage

``RiskQuantLib.Security.Stock.stock``
::

   def calVaRPercentage(self):
      from RiskQuantLib.Tool.mathTool import percentageOfSeries
      self.varPercentage = percentageOfSeries(self.closeSeries.dropna().values(),99)

   def calVaR(self):
      self.VaR = self.mktValue * self.varPercentage

``main.py``
::

   # Calculation
   fund_holdings.execFunc('calVaR')
   stock_holdings.execFunc('calVaRPercentage')
   stock_holdings.execFunc('calVaR')

*Data Output*

``main.py``
::

   # Data output
   result = stock_holdings + fund_holdings
   df_result = pd.DataFrame(result[['code','VaR']])
   df_result.to_excel(path)

After all these are done, you can save this project as a template by using terminal command:
::

   saveRQL Archegos_Risk

Next time your boss wants you to analysis another fund, you may start a RiskQuantLib project by calling:
::

   tplRQL Archegos_Risk target_path

This is a simple introduction to RiskQuantLib, about how to *start a project*, *start coding with build*, *seperate stages of analysis*, *save project as template* and *use it again*. You may noticed that we have not solved all problems that boss gave to us. More functions can be used to do this. You can refer to RiskQuantLib Class Details for further information.