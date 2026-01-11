Instrument
====================

.. toctree::
   :maxdepth: 4

``Instrument`` is any class you will use in your mission. For financial analysis, Instrument refers to stock, bond or other security type, or like interest rate or company, etc.

If you choose to inherit from ``security`` in ``config.py``, Instrument will be like security type. Or you inherit from ``index`` or ``interest``, etc. Instrument will be like what you choose. You can also only declare the name of instrument, which means create a brand new branch of class.

Any type of instrument should be initialized with ``code`` and ``name``, ``code`` behaves like index in pandas, ``name`` is the string to tell you information of detail. 

**Notice: code and name attribute is not totally the same, code will be related to some function in instrument list.**

By ``from RiskQuantLib.module import *``, any registered instrument will be imported automatically. You can use it be create an object of that class. If you create an Instrument called pandaBond, then use it like:
::

   firstPandaBondObject = pandaBond('code','name')


Any instrument class has an optional attribute called type. When initializing, you can pass a string to it, like:
::

   firstPandaBondObject = pandaBond('code','name','type')

The main reason to use instrument class is to package your source code into small block, and use or maintain them independently. This proved to be effective when data processing is complicated or it is a team mission.

The path of any instrument is the path of their first RiskQuantLib parent class. For example, if you inherit from ``Bond``, ``pandaBond`` will be located at ``RiskQuantLib/Instrument/Security/Bond``, you should put all source code about ``pandasBond`` in ``RiskQuantLib/Instrument/Security/Bond/PandaBond/pandaBond.py``

If you change the content of ``RiskQuantLib/Instrument/Security/Bond/PandaBond/pandaBond.py``, your change will be saved and no matter how many times you run ``python build.py``, these content won't be affected. This allows you to build intrument again and add new instrument, if you find mission changes.

**Notice: There is exceptions. If you change code in** ``RiskQuantLib/Instrument/Security/Bond/PandaBond/pandaBond.py`` **, you should make sure your code does not lie between any insert tag. Insert tag is used to specify the position of inserted code. It looks like:**
::

   #<tagName>
   #</tagName>

**This is very similar as the tag in html, actually, RiskQuantLib can help you to generate some code and insert them into target position. Source code can only be inserted between tags. And any content between tags can be dynamically replaced. This is why you should write your own code outside of tags.**

**Notice: However, any created instrument file will remain unless you delete the class file manually.**

**Notice: Instrument file can not be deleted automatically, but instrument class can be un-registered. If you want to cancel the registration of some instrument, you only need to remove its row in** ``config.py`` **and rebuild it. After this operation, you can not use it directly by** ``from RiskQuantLib.module import *`` **or create another instrument inheriting from this.**