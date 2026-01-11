Guardian
====================

.. toctree::
   :maxdepth: 4


This section deals mainly with ``Guardian``, ``Guardian`` is another RiskQuantLib project in addition to the current one. However, it does not perform any data processing logic, and it cannot perform any data analysis tasks on its own. Its only role is to provide source code to the ``Guarded Project`` .

Why Guardian Is Needed
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Usually, a data project has many tool functions in addition to the data processing logic. These tool functions have nothing to do with the specific data processing, but are indispensable. For example, the function to calculate the date, the function to calculate the volatility surface interpolation for options. To meet the needs of exploratory data analysis, each project may have a date calculation function of its own. But if you want a stable application to run every day, having so many of the same functions is not a wise choice.

That is why we need ``Guardian Project``, also called ``Guardian``. Generally speaking, RiskQuantLib project only generates and modifies its own source code when built, but ``Guardian`` can generate and modify the code of other RiskQuantLib projects that located in other paths. You can put functions that will be used in several similar projects in the ``Guardian`` and distribute the code by build the ``Guardian``. If there is a need to make changes someday, then just change the ``Guardian`` and build it again.

For example, if you are working on a multi-factor stock investment model, you can have three separate data projects for ``backtesting``, ``parameter search``, and ``daily update``. It is very convenient to create a new ``multifactor guard project`` and put all the common date functions, matrix eigenfunctions, and other utility functions into the ``guard project`` and control them in a unified way.

**Of course, using a Guardian will make it necessary to make a corresponding change to the Guardian every time you change the name of the project, or when you change the location of the guarded project. However, once the guarded project is built, the code becomes native to the guarded project, and unless the channel is overwritten by an update, the code is unaffected no matter how you change the name of the file or the directory of the project.**

How To Use Guardian
^^^^^^^^^^^^^^^^^^^^^^^^^^^

As we learned in the previous section, the ``Src`` folder allows you to aggregate source code in one place, categorize the source code by data process logic, and use ``Comment Control Syntax`` to tell RiskQuantLib which source file to insert that source code into. Typically, the ``Src`` folder is located under the current data engineering project. The ``Src`` folder is created when you create a project using the ``newRQL`` command.

**In practice, however, the** ``Src`` **folder can be located anywhere and does not necessarily need to be in the current data project directory. The** ``Src`` **folder can also have a different name.**

If you put the ``Src`` folder outside the root path of current project, you need to specify the location of the ``Src`` folder at build time, using ``-r yourSrcPath`` to tell RiskQuantLib to use the ``yourSrcPath`` folder as the component folder instead of the default ``Src`` folder. The specific command is as follows:
::

   python build.py -r yourSrcPath

**More critically, the same data project can have more than one component folder. When there is more than one component folder, different components make changes to the target data project via different** ``channels`` **, and the** ``-c`` **parameter needs to be used at compile time to specify the name of the channel.**

Imagine that your data project ``A`` may need a lot of logic to handle data, and they are located inside the ``A/Src`` . But at the same time, your project also needs a lot of tool functions, such as a function that calculates what day the third Friday of each month is, and so on. These functions are located in the ``Src`` component folder under the ``B`` project.

For the ``A`` project to work properly, you need the code in both ``A/Src`` and ``B/Src``. In this case, ``A``, which handles the data-process logic, is called the ``guarded project``, and ``B``, which provides the tool functions, is called the ``guard project`` or ``Guardian``. Go to the ``A`` project directory and run each of the following two commands to make the code in both component folders work at the same time:
::

   python build.py
   python build.py -r B/Src -c guardian

The first command means to use the ``Src`` component folder under ``A`` project and the default channel to build it. The second command means to use the ``B/Src`` component folder and the ``guardian`` channel to build it.

**When different channels make changes to the same Tag, the last channel in effect overwrites the previous channel. If components from different channels make changes to different Tags, they do not affect each other.**

If you are not sure what a ``Tag`` is, you can refer to :doc:`Src`.