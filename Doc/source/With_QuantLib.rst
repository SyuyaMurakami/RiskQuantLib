With QuantLib
====================

.. toctree::
   :maxdepth: 4

Once upon a time, there is a famous ask in Stack Overflow:

   `Why it is so complicated when using QuantLib for option pricing? Even if I just want to price a vanilla option, it takes several lines to do it.`

It is true, if you use QuantLib to price a vanilla call option, you may do it like:
::

   # Set Evaluation Date
   today = ql.Date(18, 3, 2021)
   ql.Settings.instance().evaluationDate = today

   # Build An Option
   # Set Payoff
   payoff=ql.PlainVanillaPayoff(ql.Option.Call, 100.0)

   # Set Exercise Date
   europeanExercise=ql.EuropeanExercise(ql.Date(18, 11, 2021))
   option = ql.EuropeanOption(payoff, europeanExercise)

   # Set Initial Stock Price, Risk-Free Rate, Volatility
   u = ql.SimpleQuote(100.0)      # Initial Stock Price
   r = ql.SimpleQuote(0.05)       # Risk-Free Rate
   sigma = ql.SimpleQuote(0.20)    # Volatility

   # Set Term Structure Of Curve
   riskFreeCurve = ql.FlatForward(0, ql.TARGET(), ql.QuoteHandle(r), ql.Actual360())
   volatility = ql.BlackConstantVol(0, ql.TARGET(), ql.QuoteHandle(sigma), ql.Actual360())

   # Initialize Stochastic Process And Pricing Enging
   process = ql.BlackScholesProcess(ql.QuoteHandle(u),
                                 ql.YieldTermStructureHandle(riskFreeCurve),
                                 ql.BlackVolTermStructureHandle(volatility))
   engine = ql.AnalyticEuropeanEngine(process)

   # Set Enging To Option
   option.setPricingEngine(engine)

   # Print Result
   print(f'Option Value：{option.NPV():.4f}')
   print("%-12s: %4.4f" %("Delta", option.delta() ))
   print("%-12s: %4.4f" %("Gamma", option.gamma() ))
   print("%-12s: %4.4f" %("Theta", option.vega()))

However, what if you have ten options and you want to price them all? What if you just want a test that show how your option value will be in certain market situation? For research purpose or you are a real derivative trader, you may sometimes have a table looks like:

+----------+------------+------------+------------+----------+------------+-----+
|OptionCode|   PayOff   |ExerciseType|ExerciseDate|StockPrice|RiskFreeRate|Sigma|
+==========+============+============+============+==========+============+=====+
|     A    |PlainVanilla|  European  | 2021-11-18 |   100.0  |     0.05   | 0.20|
+----------+------------+------------+------------+----------+------------+-----+
|     B    |PlainVanilla|  European  | 2022-03-20 |    97.6  |    0.032   | 0.17|
+----------+------------+------------+------------+----------+------------+-----+
|   ...    |    ...     |    ...     |    ...     |    ...   |    ...     | ... |   
+----------+------------+------------+------------+----------+------------+-----+

To do it in RiskQuantLib, we need to build our own european option pricing template first, we create a project by using terminal command:
::

   newRQL yourProjectPath

After it, we open ``config.py``, and edit it like:
::

    #-|instrument: myEuropeanOption
    #-|instrument-ParentQuantLibClassName: myEuropeanOption@EuropeanOption
    #-|instrument-DefaultInstrumentType: myEuropeanOption@myEuropeanOption

Then we continue to add contents into ``config.py``:
::

    #-|attribute: myEuropeanOption.myPayOff@qlPayOff, myEuropeanOption.myExercise@qlExercise, myEuropeanOption.underlyingStockPrice@qlQuote, myEuropeanOption.riskFreeRate@qlQuote, myEuropeanOption.sigma@qlQuote

Then we build it by using terminal command:
::

   cd yourProjectPath
   python build.py

Good, we now have a brand new project for european option pricing. RiskQuantLib has created the instrument class, type class we need. We need to change it a little bit for further use. We open ``RiskQuantLib/Property/QlExercise/qlExercise.py``, and make it look like:
::

   #!/usr/bin/python
   # coding = utf-8

   import QuantLib as ql
   import pandas as pd
   from RiskQuantLib.Property.property import property

   class qlExercise(property):

       def __nullFunction__(self):
           pass

       def __init__(self, value : pd.Timestamp):
           value = ql.EuropeanExercise(ql.Date(value.day, value.month, value.year))
           super(qlExercise,self).__init__(value)

       def setValue(self,value : pd.Timestamp):
           self.value = ql.EuropeanExercise(ql.Date(value.day, value.month, value.year))

In this step, we package the QuantLib code of exercise, so that it can be used even if we only pass a date to it. Once it is finished, we don't need to define it every time we want to price an european option.

Again, we do the similar thing to ``RiskQuantLib/Property/QlPayOff/qlPayOff.py``, and make it look like:
::

   #!/usr/bin/python
   # coding = utf-8

   import QuantLib as ql
   from RiskQuantLib.Property.property import property

   class qlPayOff(property):

       def __nullFunction__(self):
           pass

       def __init__(self, value : float):
           value = ql.PlainVanillaPayoff(ql.Option.Call, value)
           super(qlPayOff,self).__init__(value)

       def setValue(self, value : float):
           self.value = ql.PlainVanillaPayoff(ql.Option.Call, value)

In this step, we package the QuantLib code of payoff, so that it can be used even if we only pass a payoff value to it. Once it is finished, we don't need to define it every time we want to price an european option.

Again, we do the similar thing to ``RiskQuantLib/Property/QlQuote/qlQuote.py``, and make it look like:
::

   #!/usr/bin/python
   # coding = utf-8

   import QuantLib as ql
   from RiskQuantLib.Property.property import property

   class qlQuote(property):

       def __nullFunction__(self):
           pass

       def __init__(self, value : float):
           value = ql.SimpleQuote(value)
           super(qlQuote,self).__init__(value)

       def setValue(self,value):
           self.value.setValue(value)


The final preparation, is to edit ``RiskQuantLib/Instrument/Security/MyEuropeanOption/myEuropeanOption.py``, to make it look like:
::

   #!/usr/bin/python
   # coding = utf-8

   import QuantLib as ql
   from RiskQuantLib.Instrument.Security.security import security
   from QuantLib import EuropeanOption
   from RiskQuantLib.Auto.Instrument.Security.MyEuropeanOption.myEuropeanOption import setMyEuropeanOption

   class myEuropeanOption(security,EuropeanOption,setMyEuropeanOption):

       def __nullFunction__(self):
           pass

       def __init__(self, codeString,nameString,securityTypeString = 'myEuropeanOption'):
           security.__init__(self,codeString,nameString,securityTypeString)

       def iniPricingModule(self, *args):
           EuropeanOption.__init__(self,*args)

       def pricing(self):
           self.iniPricingModule(self.myPayOff,self.myExercise)
           riskFreeCurve = ql.FlatForward(0, ql.TARGET(), ql.QuoteHandle(self.riskFreeRate), ql.Actual360())
           volatility = ql.BlackConstantVol(0, ql.TARGET(), ql.QuoteHandle(self.sigma), ql.Actual360())
           process = ql.BlackScholesProcess(ql.QuoteHandle(self.underlyingStockPrice),
                                            ql.YieldTermStructureHandle(riskFreeCurve),
                                            ql.BlackVolTermStructureHandle(volatility))
           engine = ql.AnalyticEuropeanEngine(process)
           self.setPricingEngine(engine)

           # Calculate Result
           self.npvValue = self.NPV()
           self.deltaValue = self.delta()
           self.gammaValue = self.gamma()
           self.vegaValue = self.vega()


Now everything is ready, we switch to ``main.py`` in your project root path, we can pricing the same option with RiskQuantLib, by:
::

   # With RiskQuantLib

   # Don't Forget to Set Evaluation Date
   today = ql.Date(18, 3, 2021)
   ql.Settings.instance().evaluationDate = today

   from RiskQuantLib.module import *
   vanillaOption = myEuropeanOption("A","A")
   vanillaOption.setMyPayOff(100)
   vanillaOption.setMyExercise(pd.Timestamp("20211118"))
   vanillaOption.setUnderlyingStockPrice(100)
   vanillaOption.setRiskFreeRate(0.05)
   vanillaOption.setSigma(0.20)
   vanillaOption.pricing()

It is more readable, right? More importantly, you can change the value of any parameter and price it again. If you want to price another option, just initialize another object:
::

   # You already set valuation date, don't need to do it again.

   from RiskQuantLib.module import *
   vanillaOption = myEuropeanOption("B","B")
   vanillaOption.setMyPayOff(100)
   vanillaOption.setMyExercise(pd.Timestamp("20220320"))
   vanillaOption.setUnderlyingStockPrice(97.6)
   vanillaOption.setRiskFreeRate(0.032)
   vanillaOption.setSigma(0.17)
   vanillaOption.pricing()

Or do it in a more elegant way, which is to use RiskQuantLib list. Remember you have a dataframe like:

+----------+------------+------------+------------+----------+------------+-----+
|OptionCode|   PayOff   |ExerciseType|ExerciseDate|StockPrice|RiskFreeRate|Sigma|
+==========+============+============+============+==========+============+=====+
|     A    |PlainVanilla|  European  | 2021-11-18 |   100.0  |     0.05   | 0.20|
+----------+------------+------------+------------+----------+------------+-----+
|     B    |PlainVanilla|  European  | 2022-03-20 |    97.6  |    0.032   | 0.17|
+----------+------------+------------+------------+----------+------------+-----+

We save it as an excel file named ``European_Option.xlsx`` in your project root path. Then in ``main.py``, we code like:

::

   # With RiskQuantLib List
   # Set Evaluation Date
   today = ql.Date(18, 3, 2021)
   ql.Settings.instance().evaluationDate = today

   from RiskQuantLib.module import *
   df = pd.read_excel(path+os.sep+'European_Option.xlsx')

   vanillaOptionList = myEuropeanOptionList()
   vanillaOptionList.addMyEuropeanOptionSeries(df['OptionCode'],df['OptionCode'])
   vanillaOptionList.setMyPayOff(df['OptionCode'],[100 for payoff in df['OptionCode']])
   vanillaOptionList.setMyExercise(df['OptionCode'],[pd.Timestamp(date) for date in df['ExerciseDate']])
   vanillaOptionList.setUnderlyingStockPrice(df['OptionCode'],df['StockPrice'])
   vanillaOptionList.setRiskFreeRate(df['OptionCode'],df['RiskFreeRate'])
   vanillaOptionList.setSigma(df['OptionCode'],df['Sigma'])
   vanillaOptionList.execFunc('pricing')

If you want to save the result, the only thing you need to do is to convert it to dataframe by:
::

   result = pd.DataFrame(vanillaOptionList[['code','npvValue','deltaValue','gammaValue','vegaValue']])

**Do not forget to save your work to a template, this project can be used again, this is the most important feature of RiskQuantLib.**

To do this, you should delete the file ``European_Option.xlsx``, and clear the content of ``main.py``, because these data and operation are not repeatable, only the logic behind could be used again. After this, open a terminal and call:
::

   saveRQL yourProjectPath europeanOption

Next time you want to use it, just use terminal command:
::

   tplRQL europeanOption yourNewProjectPath