With ORM
====================

.. toctree::
   :maxdepth: 4

For convience, RiskQuantLib provides with functions to interact with ORM. However, these functions can be used to any iterable objects. We shall introduce them as follows:

From Iterable
^^^^^^^^^^^^^^^^^^^^^^

If you use ORM to get a list, whose elements is the record in database and all columns in database are mapped into element attributes, you may want to change this list into RiskQuantLib list.

Let's suppose you have a ORM list object ``ORM`` whose element has attributes named: ``OptionCode``, ``PayOff``, ``ExerciseType``, ``ExerciseDate``, ``StockPrice``, ``RiskFreeRate``, ``Sigma``.

Now we build our project by edit ``config.py`` to:
::

    #-|instrument: myEuropeanOption
    #-|instrument-ParentQuantLibClassName: myEuropeanOption@EuropeanOption
    #-|instrument-DefaultInstrumentType: myEuropeanOption@myEuropeanOption

    #-|attribute: myEuropeanOption.PayOff@qlPayOff, myEuropeanOption.ExerciseDate@qlExercise, myEuropeanOption.StockPrice@qlQuote, myEuropeanOption.RiskFreeRate@qlQuote, myEuropeanOption.Sigma@qlQuote


**Noticed here, we have all attribute names that are the same with ORM list element attribute names. This will help RiskQuantLib to identify attribute and set them automatically.**

After building it, you can open the ``main.py`` and use it directly:
::

   from RiskQuantLib.module import *
   vanillaOptionList = myEuropeanOptionList().fromIterable(ORM, code = 'OptionCode')

You can generate RiskQuantLib list from another RiskQuantLib list in this way:
::

    stockListA = stockList().fromDF(df1)
    stockListB = subStockList().fromIterable(stockListA, code = 'code', name = 'name')

Here, if ``subStockList`` is a class inheriting from ``stockList``, all attributes of stockListA will be kept in stockListB. If ``subStockList`` doesn't have any relation with ``stockList``, then only the attributes registered in both classes will be kept.
