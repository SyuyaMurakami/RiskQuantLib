..
   Note: Items in this toctree form the top-level navigation. See `api.rst` for the `autosummary` directive, and for why `api.rst` isn't called directly.

.. toctree::
   :hidden:

   Home page <self>
   modules.rst

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

Quick Start
^^^^^^^^^^^

Suppose you are employeed by a bank. One day, your bose calls you to his office, he tells you your company want to invest in a new family fund, Archegos, we suppose it is. Your mission, if you accept, is to tell your boss how risky this deal is.

 Take adventure after second thought, this is far from recklessness.

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
| Date       | HIYJ US Equity  | U7HJ US Equity   |  KIHS US Equity |
+============+=================+==================+=================+
| 2020-01-01 |       23.9      |       nan        |        9.8      |
+------------+-----------------+------------------+-----------------+
| 2020-01-02 |        nan      |      12.8        |        9.8      |
+------------+-----------------+------------------+-----------------+
| 2020-01-03 |       21.9      |      13.1        |        9.8      |
+------------+-----------------+------------------+-----------------+
| 2020-01-04 |       22.1      |      13.2        |        9.8      |
+------------+-----------------+------------------+-----------------+
| 2020-01-05 |       22.4      |      12.9        |        9.8      |
+------------+-----------------+------------------+-----------------+
|    ...     |       ...       |      ...         |        ...      |
+------------+-----------------+------------------+-----------------+

You decide to calculate the volatility of stocks of Archegos holdings. So you start coding like:

``df_stock_holding = pd.read_excel(path_one)``
``df_stock_close = pd.read_excel(path_two)``

If you don't use RiskQuantLib, you may do it like:

``df_std = df_stock_close.std()``
``archegos_stock_holdings = df_std[df_stock_holding.columns.to_list()]``