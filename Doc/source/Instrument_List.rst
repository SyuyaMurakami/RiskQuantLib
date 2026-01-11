Instrument List
====================

.. toctree::
   :maxdepth: 4

``Instrument List`` is a collection of any class in RiskQuantLib, it behaves like list in python. However, the difference is instrument list is defined for each kind of instrument, any change to one won't influence the others. For example, ``bond`` will have ``bondList``, ``stock`` will have ``stockList``, if you build a new instrument called ``pandaBond``, ``pandaBondList`` will be created, too.

Any ``Instrument List`` has an atrribute named ``all`` to hold its elements. It also owns default function to allow you to add new element into this list, such as ``addBond`` and ``addBondSeries``. With these function, you can add a single bond object into this list or add several bonds into it.

``Instrument List`` allows duplicate elements. You can add one element twice.

Usually, ``Instrument List`` will inherit from ``RiskQuantLib.Operation.operation.operation``, which is a class containing all kinds of operations that can be done to list. You can read `Operation Of List <https://riskquantlib-doc.readthedocs.io/en/latest/RiskQuantLib.Operation.html#module-RiskQuantLib.Operation.operation>`_ to know details.

Useful functions of instrument list includes ``groupBy``, ``filter``, ``execFunc``, ``apply``, ``join``, ``merge``, ``sort``, etc.

It is necessary to introduce some important properties of instrument list here:

Add Element
^^^^^^^^^^^

If ``pandaBondList`` is an instrument list, you can add instruments by using ``addPandaBondSeries`` function:
::

   listA = pandaBondList()
   listA.addPandaBondSeries(codeSeries,nameSeries)

You can also add one element by ``addPandaBond``:
::

   listA = pandaBondList()
   listA.addPandaBond(code,name)

**Notice: The name of add function will change if you build different instrument class, for example, if you built an instrument named samuraiBond, this function will be** ``addSamuraiBond``.

Mixed Index
^^^^^^^^^^^

For python list, you can index an element if you know the number of its position, for example, ``listA[2]`` will give you the third element. However, in RiskQuantLib, index can be the number of position, or the value of ``code`` attribute of that element, or any attribute name, or a list of value of ``code`` attribute, or a list of attribute name. For example:
::

   rqlListA = stockList()
   rqlListA.addStockSeries(['A','B','C'],['TC US','HU China','JI UK'])
   rqlListA.setIssuer(['A','B','C'],['Tencent','HU JI FA','JIK&'])

   # This will give you the third element
   theThirdElement = rqlListA[2]

   # This will give you the first stock whose code is 'C'
   theThirdElement = rqlListA['C']

   # This will give you the last element
   theThirdElement = rqlListA[-1]

   # This will give you the first two element
   theFirstTwoElement = rqlListA[:2]

   # This will give you all the elements whose code is 'A' or 'B'
   theFirstTwoElement = rqlListA[['A','B']]

   # This will give you a list whose element is the value of attribute issuer
   theValueListOfIssuer = rqlListA['issuer']

   # This will give you an dict whose element is the value of attribute issuer and name
   theValueDictOfIssuerAndName = rqlListA[['issuer','name']]

You may ask, what if the value of attribute ``code`` is the same with some attribute name? Well, the best practice is not to let this happen. If it happens, RiskQuantLib will treat it as the value of attribute ``code``, and gives you an single element whose attribute ``code`` equals this value.

Set Function
^^^^^^^^^^^^

Set function is a series of function used to set values of instrument list. As you see above, we used ``rqlListA.setIssuer(['A','B','C'],['Tencent','HU JI FA','JIK&'])`` to set the value of ``issuer`` attribtue. This function has two parameters, ``codeSeries`` and ``issuerNameSeries``, when you passed the value of these two series, they are used as a dict. In this example, stock 'A' is related to 'Tencent', stock 'B' is related to 'HU JI FA'. Here, the length of passing paramter of set function **do not** have to be the same with the length of instrument list. RiskQuantLib will skip those elements whose ``code`` are not in the passed ``codeSeries``.

Addition And Substraction
^^^^^^^^^^^^^^^^^^^^^^^^^

You can add or substract a instrument list to another, by:
::

   rqlListC = rqlListA + rqlListB
   rqlListD = rqlListA - rqlListB

After this, all elements in B will be added to A or deleted from A. However, any attribute of A won't be kept in C or D, only elements will be changed. If you want C to keep the attribute of A, you should use:
::

   rqlListC = rqlListA.copy(deep = False)
   rqlListC.setAll(rqlListA.all + rqlListB.all)

Iteration
^^^^^^^^^

If ``rqlListA`` is a stockList, and in ``RiskQuantLib.Instrument.Security.Stock.stock``, you defined an attribute function like:
::

   class stock(base):
      ...
      def calTradingAmount(self):
         self.tradingAmount = self.tradingPrice * self.tradingShare

If you need to iterate all elements and call this attribute function, you should use ``execFunc`` like:
::

   rqlListA.execFunc('calTradingAmount')

This is totally the same with:
::

   for element in rqlListA:
      element.calTradingAmount()

You can also call it with parameters, like:
::
   rqlListA.execFunc('calTradingAmount',tradingAmountType)

This is totally the same with:
::

   for element in rqlListA:
      element.calTradingAmount(tradingAmountType)

Selection
^^^^^^^^^

If ``stockListA`` is a stockList, you want to select all elements whose name contains letter 'HG', you can do it like:
::

   selectedElements = stockListA.filter(lambda x:x.name.find('HG')!=-1)

Here, ``filter`` is a function to select those elements you need, you can pass a function to it, and it will return the elements which are justified as ``True`` by the passed function.