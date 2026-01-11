Build Your Project
====================

.. toctree::
   :maxdepth: 4

After create a project, you should build it to suit for your mission. By ``Build``, RiskQuantLib will generate python source code automatically. It is the core conception of RiskQuantLib. Before moving on, let specify some definition in RiskQuantLib:

``Build`` means generate source code automatically.

``Instrument`` means any class you will use in your mission. For financial analysis, ``Instrument`` refers to stock, bond or other security type, or like interest rate or company, etc.

Then we start to build our first project. The critical thing is to tell RiskQuantLib how to build it. This is done by specify key word in ``config.py`` , which you can find in your project root dictionary once you create a project. The content of building will be written into ``RiskQuantLib.Auto``. 

In last chapter we create a project, it looks like:
::

   --your_project_path
     --Cache
     --Data
     --Result
     --RiskQuantLib
     --Src
     --build.bat
     --build.py
     --config.py
     --debug.bat
     --main.py

We will explain the function of each term as follows:

RiskQuantLib
^^^^^^^^^^^^

``RiskQuantLib`` is a dictionary holding all source files of RiskQuantLib, it looks like:
::

   --RiskQuantLib
     --Auto
     --Build
     --Instrument
     --InstrumentList
     --Model
     --Operation
     --Property
     --Tool
     --__init__.py
     --module.py

Src
^^^^
``Src`` is a dictionary holding all source files that is needed in your project. You can leave ``Src`` alone and never use it. It won't influence your project at all. Or you can put any python source code in it, run or import them as you always know in python, RiskQuantLib is also cool with that. However, if you want to try some new things, ``Src`` will give you a great way to manage your code. 

**In short, any code in** ``Src`` **can be parsed by RiskQuantLib according to the comment in source code, the control comment syntax will help to generate python code as you wish.**

The most simple way to control your code is to tell RiskQuantLib where they should be insert. You can insert any code into any position of any file as long as this file is under ``RiskQuantLib`` directory. If you want to do this, use ``#->`` control comment.

For example, you have a instrument class named as ``stock``, and you want to add a class method to append a string ``_hello`` after the ``name`` attribute, and mark the value as a new attribute named as ``greeting``. You can go to ``RiskQuantLib/Instrument/Security/Stock.stock.py`` to add this function:
::

   def sayHello(self):
       self.greeting = self.name + "_hello"

This is usually what we do. But with ``Src``, you can do it another way. First, create a file named ``greeting.py`` under ``Src``, then open it and write:
::

   #->stock
   def sayHello(self):
       self.greeting = self.name + "_hello"

Then close this file and open your terminal, change working directory into current project, run:
::

   python build.py

And this function will be inserted into ``RiskQuantLib/Instrument/Security/Stock.stock.py`` automatically. Cool, isn't it?

**For the automatically generated instrument by RiskQuantLib, use instrument name will be enough to specify a target destination, like** ``#->stock``. **But if you create the source file by yourself, you should use the absolute import path to tell RiskQuantLib where this file is, like:** ``#->RiskQuantLib.Instrument.Security.Stock.stock``

config.py
^^^^^^^^^^^^^^^^^^^^^

``config.py`` is the file to tell RiskQuantLib how to generate python source code of instrument class. After calling ``build.py``, Any instrument specified will be created, the source file will be added into ``RiskQuantLib`` dictionary besides its first RiskQuantLib parent class. The default ``config.py`` looks like:
::

   #!/usr/bin/python
   # coding = utf-8

   #-|instrument: security, company, index, interest
   #-|instrument: bond@security, stock@security, derivative@security, fund@security
   #-|instrument: future@derivative, option@derivative

   #-|instrument-DefaultInstrumentType: security@Security, company@Company, index@Index, interest@Interest
   #-|instrument-DefaultInstrumentType: bond@Bond, stock@Stock, derivative@Derivative, fund@Fund
   #-|instrument-DefaultInstrumentType: future@Future, option@Option

It might be a little confusing if we write it in above way, but it will be more clear if we see it as a tree:
::

   --instrument
     --security ( DefaultInstrumentType = Security )
       --bond ( DefaultInstrumentType = Bond )
       --stock ( DefaultInstrumentType = Stock )
       --derivative ( DefaultInstrumentType = Derivative )
         --future ( DefaultInstrumentType = Future )
         --option ( DefaultInstrumentType = Option )
       --fund ( DefaultInstrumentType = Fund )
     --company ( DefaultInstrumentType = Company )
     --index ( DefaultInstrumentType = Index )
     --interest ( DefaultInstrumentType = Interest )

There are two basic kinds of keyword in ``config.py``, which is ``instrument`` and ``attribute`` , we will explain them here:

*instrument*
------------------

The *instrument* key word can be used to define instrument by your will, depending on your data. It is just a comment in python, but a little special. To use it, the comment line has to start with ``#-|`` command tag, and followed closely by ``instrument`` keyword, no space or other characters in the middle. Finally, a ``:`` has to follow the ``instrument`` keyword. A validated command comment is like:
::

   #-|instrument: instrument_a

**You can use comma to seperate different instruments declaration, like:**
::

   #-|instrument: instrument_a, instrument_b

**You can use @ to specify what parent instrument the current one is inheriting from, like:**
::

   #-|instrument: instrument_a@parent_instrument_p

**If an instrument has more than two parents, write them seperately like:**
::

   #-|instrument: instrument_a@parent_instrument_p1, instrument_a@parent_instrument_p2

The instrument declared here will tell RiskQuantLib how to build your project and add class files that will be used to form a data graph. For example, if you write this in ``config.py`` :
::

   #-|instrument: treasureBond@bond

RiskQuantLib will create instrument class source file ``treasureBond.py`` under ``RiskQuantLib.Instrument.Security.Bond.TreasureBond``, and create list class source file ``treasureBondList.py`` under  ``RiskQuantLib.InstrumentList.SecurityList.BondList.TreasureBondList`` after your run ``python build.py``.

The @ means this new instrument will inherit from this RiskQuantLib class. It can accept key word like: ``Fund``, ``Stock``, ``Bond``, ``Repo``, etc. 

**However, you should always inherit from a class that you have declared. It doesn't matter if you declare the parent class before or after this line.**

**You can not split this declaration into two lines using \ or /. If you want to start a new line, a new keyword must be used, like:**
::

   #-|instrument: treasureBondOne@bond
   #-|instrument: treasureBondTwo@bond

*attribute*
-----------------

The *attribute* key word can be used to what kind of attributes you need when analysising your data, and which class these attributes belong to. After calling ``build.py``, any attributes specified here will be registered and can be used with ``set`` function. 

This keyword is just a comment in python, but, as always, a little special. To use it, the comment line has to start with ``#-|`` command tag, and followed closely by ``attribute`` keyword, no space or other characters in the middle. Finally, a ``:`` has to follow the ``attribute`` keyword. A validated command comment is like:
::

   #-|attribute: fund.yourAttribute

This declaration will add ``yourAttribute`` to class ``fund`` .

**You can use comma to seperate different attributes declaration, like:**
::

   #-|attribute: fund.yourAttribute, stock.anotherAttribute

**You can use @ to specify what data type this attribute should have, like:**
::

   #-|attribute: fund.yourAttribute@number, stock.anotherAttribute@string

The default data type can be ``number``, ``string``, ``series``. It can also be self-defined, actually you can use any word after @ to specify a data type, if it doesn't exist, RiskQuantLib will create a new data type and use the new one, like:
::

   #-|attribute: fund.yourAttribute@my_new_data_type

Data type tells RiskQuantLib what kind of data will be stored by this attribute. If you add 'sellPrice' to ``stock``, this should be a ``number`` attribute, while an attribute like 'issuerName' is a ``string`` kind. ``series`` is used if it's an attribute like 'sellPriceOfPastSixMonth'. If you specify a kind that is never used before, it will be created as a type class, located in ``RiskQuantLib.Property``.

The data type here is not only a data type in RiskQuantLib. RiskQuantLib is designed to be used to process graph-structure-data. Data type we mentioned above is actually the ending-node of a graph, thus we'd better call it ``property`` . We will explain it in later chapter.

**You should add attribute to an instrument that is already declared, no matter it is before or after.**

**You can not split this declaration into two lines using \ or /. If you want to start a new line, a new keyword must be used, like:**
::

   #-|attribute: fund.yourAttributeOne
   #-|attribute: fund.yourAttributeTwo

*instrument-DefaultInstrumentType*
--------------------------------------------

This key word is a string to mark your new instrument class. It is just a label, does not actually influence the class behavior. An example is like:
::

   #-|instrument-DefaultInstrumentType: instrument_a@another_name_of_instrument_a

*instrument-ParentQuantLibClassName*
-----------------------------------------

This keyword means this new instrument will inherit from this QuantLib class. It can accept key word like: ``Instrument``, ``Bond``, etc. You can refer to QuantLib document to find what class QuantLib has. Like:
::

   #-|instrument-ParentQuantLibClassName: my_bond@Bond

*instrument-LibraryName*
------------------------------------------

The *LibraryName* is other library that you will use in instrument class source file, like numpy and pandas. Like:
::

   #-|instrument-LibraryName: instrument_a@tensorflow as tf

build.py
^^^^^^^^

``build.py`` is used to generate python source code automatically. After you specify what kind of class you want to create, how it inherit from other class, what attributes these class should have in *config.py*, you can call *build.py* by terminal:
::

   python build.py

**Notice: If you do not use control comment syntax in Src, this build.py will only need to be excuted once, at the begin of your project. Do not build your project every time you run main.py, it is not necessary. But if you use control comment in Src, you can use the following command so that the build action will be triggered every time you make change to Src directory:**
::

   python build.py -a

If your project is under development, it will be useful to use ``debug`` mode. With this mode, the python source code in ``Src`` will not be directly inserted into target file, it will be bound dynamically into target file. By this way, the break point in file under ``Src`` will start to effect, you can debug it directly. Surely, the ``auto build`` mode can be run at the same time, it will automatically build the whole project every time you make a change. To build project in automatically debug mode, run:
::

   python build.py -a -d

or just double click the file in windows system:
::

   debug.bat

main.py
^^^^^^^

``main.py`` is entrance of your project. You can start your coding here, by:
::

   from RiskQuantLib.module import *

Then you can use the class directly by:
::

   bondA = treasureBond('firstBond','nameOfFirstBond')

You can also set attributes directly by:
::

   stockA = stock('firstStock','nameOfFirstStock')
   stockA.setAnotherAttribute('valueOfAnotherAttribute')

For more information about the ``Instrument``, we will introduce it in next chapter.

Data
^^^^^^^^^^^

This is a folder just used to hold your data. Default as empty.

Cache
^^^^^^^^^^^

This is a folder just used to hold your cache file. Default as empty.

Result
^^^^^^^^^^^

This is a folder just used to hold your result file. Default as empty.

build.bat
^^^^^^^^^^^^

After specifying all instruments and attributes in ``config.py`` , you can double click ``build.bat`` to build your preoject. This file only exists in windows system.

debug.bat
^^^^^^^^^^^^

After specifying all instruments and attributes in ``config.py`` , you can double click ``debug.bat`` to debug your preoject. This file only exists in windows system.

The difference between build and debug is debug mode import file in ``Src`` as a module, thus leads to different behaviors. You can find more information about ``Src`` above.