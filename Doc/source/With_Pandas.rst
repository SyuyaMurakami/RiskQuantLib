With Pandas
====================

.. toctree::
   :maxdepth: 4

When I am inspired to start RiskQuantLib project, my friend asked me one question:

   `Are you trying to design another pandas?`

Well, I admit that in some way, RiskQuantLib is very similar to pandas, but at the very beginning, RiskQuantLib is designed to be based on pandas. It lies behind pandas because it is a data analysis core concentrating on dealing with data process, rather than an integrated tool to do things from data input to data output.

But later after the day we discussed this issue, I realized that to jump out of the curse of pandas, I should get rid of more conventions. This leads me to this place, where RiskQuantLib has its own functions for iteration or merge, etc.

However, there is one thing need to be noticed, that is:

**RiskQuantLib is still based on pandas, it is not a substitute of pandas, the best practice is to code your data process logic with RiskQuantLib, and leave the rest to pandas.**

For convience, RiskQuantLib provides with functions to interact with pandas, we shall introduce them as follows:

From Pandas Series
^^^^^^^^^^^^^^^^^^^^^^

The most simple way to use pandas with RiskQuantLib is to use pandas.Series, remember what we have shown before, if you have a dataframe looks like:

+----------+------------+------------+------------+----------+------------+-----+
|OptionCode|   PayOff   |ExerciseType|ExerciseDate|StockPrice|RiskFreeRate|Sigma|
+==========+============+============+============+==========+============+=====+
|     A    |PlainVanilla|  European  | 2021-11-18 |   100.0  |     0.05   | 0.20|
+----------+------------+------------+------------+----------+------------+-----+
|     B    |PlainVanilla|  European  | 2022-03-20 |    97.6  |    0.032   | 0.17|
+----------+------------+------------+------------+----------+------------+-----+
|   ...    |    ...     |    ...     |    ...     |    ...   |    ...     | ... |   
+----------+------------+------------+------------+----------+------------+-----+

After creating a project and building it with ``config.py``:
::

    #-|instrument: myEuropeanOption
    #-|instrument-ParentQuantLibClassName: myEuropeanOption@EuropeanOption
    #-|instrument-DefaultInstrumentType: myEuropeanOption@myEuropeanOption

    #-|attribute: myEuropeanOption.myPayOff@qlPayOff, myEuropeanOption.myExercise@qlExercise, myEuropeanOption.underlyingStockPrice@qlQuote, myEuropeanOption.riskFreeRate@qlQuote, myEuropeanOption.sigma@qlQuote

You can open the ``main.py`` and use it directly:
::

   from RiskQuantLib.module import *
   df = pd.read_excel(path+os.sep+'European_Option.xlsx')

   vanillaOptionList = myEuropeanOptionList()
   vanillaOptionList.addMyEuropeanOptionSeries(df['OptionCode'],df['OptionCode'])
   vanillaOptionList.setMyPayOff(df['OptionCode'],[100 for payoff in df['OptionCode']])
   vanillaOptionList.setMyExercise(df['OptionCode'],[pd.Timestamp(date) for date in df['ExerciseDate']])
   vanillaOptionList.setUnderlyingStockPrice(df['OptionCode'],df['StockPrice'])
   vanillaOptionList.setRiskFreeRate(df['OptionCode'],df['RiskFreeRate'])
   vanillaOptionList.setSigma(df['OptionCode'],df['Sigma'])

We see here that ``set`` function in RiskQuantLib accept any iterable object as parameters, including pandas.Series. Usually, ``set`` function has two parameters, the first one should be the code used to identify elements, the second one should be the value you want to set.

From Pandas DataFrame
^^^^^^^^^^^^^^^^^^^^^^

You may ask, what if I have a dataframe that has thousands of columns? I can't set them one by one, right?

True, luckily, RiskQuantLib provides functions to read from pandas.DataFrame. Suppose we still want to import the dataframe mentioned before:

+----------+------------+------------+------------+----------+------------+-----+
|OptionCode|   PayOff   |ExerciseType|ExerciseDate|StockPrice|RiskFreeRate|Sigma|
+==========+============+============+============+==========+============+=====+
|     A    |PlainVanilla|  European  | 2021-11-18 |   100.0  |     0.05   | 0.20|
+----------+------------+------------+------------+----------+------------+-----+
|     B    |PlainVanilla|  European  | 2022-03-20 |    97.6  |    0.032   | 0.17|
+----------+------------+------------+------------+----------+------------+-----+
|   ...    |    ...     |    ...     |    ...     |    ...   |    ...     | ... |   
+----------+------------+------------+------------+----------+------------+-----+

Now we build it by change ``Build_Attr.xlsx`` to:
::

    #-|instrument: myEuropeanOption
    #-|instrument-ParentQuantLibClassName: myEuropeanOption@EuropeanOption
    #-|instrument-DefaultInstrumentType: myEuropeanOption@myEuropeanOption

    #-|attribute: myEuropeanOption.PayOff@qlPayOff, myEuropeanOption.ExerciseDate@qlExercise, myEuropeanOption.StockPrice@qlQuote, myEuropeanOption.RiskFreeRate@qlQuote, myEuropeanOption.Sigma@qlQuote

**Noticed here, we have all attribute names that are the same with dataframe column names. This will help RiskQuantLib to identify column and set them automatically.**

After building it, you can open the ``main.py`` and use it directly:
::

   from RiskQuantLib.module import *
   df = pd.read_excel(path+os.sep+'European_Option.xlsx')

   vanillaOptionList = myEuropeanOptionList().fromDF(df,code = 'OptionCode')

Cool, isn't it? However, I won't suggest doing this, cause RiskQuantLib is not meant to be bonded with single excel file. If you do it like this, you will find that you may have another dataframe, whose column name is not the same with this one, but its meaning is the same. For example, in another dataframe ``df2``, it may looks like:

+----------+------------+------------+------------+----------+------------+-----+
|   Code   |     Pay    |     Type   |    KDate   |   Price  |      RF    |  Vol|
+==========+============+============+============+==========+============+=====+
|     C    |PlainVanilla|  European  | 2021-11-18 |   103.5  |     0.03   | 0.16|
+----------+------------+------------+------------+----------+------------+-----+
|     D    |PlainVanilla|  European  | 2022-03-20 |    88.1  |    0.019   | 0.10|
+----------+------------+------------+------------+----------+------------+-----+
|   ...    |    ...     |    ...     |    ...     |    ...   |    ...     | ... |   
+----------+------------+------------+------------+----------+------------+-----+

If you want to add these contracts to your RiskQuantLib list, you should use ``addFromDF``, rather than ``fromDF``:
::

    vanillaOptionList.addFromDF(df2,code = 'Code')

**However, because the column name in df2 is not the same with your registered attribute, you will find the new elements that you added just now don't have any attribute value.**

There are two ways to solve this problem, you can change the name of columns of df2 and update the elements, or mannually set the attribute value by set function. We explain the first one as follows.

Update With DataFrame
^^^^^^^^^^^^^^^^^^^^^^^

After you rename your df2, it looks like:

+----------+------------+------------+------------+----------+------------+-----+
|OptionCode|   PayOff   |ExerciseType|ExerciseDate|StockPrice|RiskFreeRate|Sigma|
+==========+============+============+============+==========+============+=====+
|     C    |PlainVanilla|  European  | 2021-11-18 |   103.5  |     0.03   | 0.16|
+----------+------------+------------+------------+----------+------------+-----+
|     D    |PlainVanilla|  European  | 2022-03-20 |    88.1  |    0.019   | 0.10|
+----------+------------+------------+------------+----------+------------+-----+
|   ...    |    ...     |    ...     |    ...     |    ...   |    ...     | ... |   
+----------+------------+------------+------------+----------+------------+-----+

Good, remember you have already added element C and D into ``vanillaOptionList``, we should update the attribute value of them. Here, it is simple:
::

    vanillaOptionList.updateAttrFromDF(df2, code = 'OptionCode')

After doing this, the information of contract C and D is updated, while A and B are not changed. But it is necessary to mention here:

**Try not to build your project based on data pattern, build it based on analysis logic.**

That is, when you design your project, you should forget all your input files, forget what name the column is given, forget how many files you would have, forget how you get these data or how you want to output and show these data. You should try to think, what kind of intrument you would use, how they are related with each other, what kind of attribute you should use, could less attribute be used, what type of variable you should use, why using self-defined types can simplicify your task, etc.

To Pandas DataFrame
^^^^^^^^^^^^^^^^^^^^

The most straight forward way to do it is:
::

    result = pd.DataFrame(vanillaOptionList[attributeList])

Where ``attributeList`` is a python list whose elements is the name string of attribute. You can also pass an index when converting to pandas.DataFrame, like:
::

    result = pd.DataFrame(vanillaOptionList[attributeList],index = vanillaOptionList['code'])

Or, there is another easy way:
::

    result = vanillaOptionList[attributeList].toDF(index=vanillaOptionList['code'])