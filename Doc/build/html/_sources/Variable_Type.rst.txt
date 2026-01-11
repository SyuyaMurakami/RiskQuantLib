Variable Type
====================

.. toctree::
   :maxdepth: 4

Variable is the type of attribute, ususally it should be ``string``, ``number``, ``series``, ``any``. However, RiskQuantLib allows to build your own variable type, for example, ``timeList``, or ``blank``, or whatever you like.

This is a powerful design when you deal with some complicated situations. Somtimes, you may wonder why list in python doesn't have ``reduce`` function any more, or you want to reload the ``__add__`` function of list so that list objects can be added as you like. In RiskQuantLib, this is done by defining your own variable type class.

The way to build your own type is to use ``config.py``, remember we have a config file like:
::

   #-|attribute: fund.yourAttribute@number, stock.anotherAttribute@string

You specified variable type of *yourAttribute* is ``number``, and variable type of *anotherAttribute* is ``string``. Now, we want to create a type named ``yourNewType``, and let variable type of *anotherAttribute* be ``yourNewType``. All we need to do is to change ``string`` to ``yourNewType``, and run ``build.py``, which is in your project root path.

The modified file should look like:
::

   #-|attribute: fund.yourAttribute@number, stock.anotherAttribute@yourNewType

Notice here that we don't have any pre-defined type class named ``yourNewType``, don't worry, RiskQuantLib will scan and create it if it doesn't exist. After run ``build.py``, you could find the created file ``RiskQuantLib/Property/YourNewType/yourNewType.py``.

Same with instrument building, once the type class file is created, RiskQuantLib can **not** delete it automatically. It can only be deleted by your own hand. However, If it doesn't show in ``config.py``, after a second building or after clear command, it will be un-registered from RiskQuantLib, so that you can't use it with automatical building any more.