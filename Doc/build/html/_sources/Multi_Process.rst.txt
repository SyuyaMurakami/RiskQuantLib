Multi-Process
====================

.. toctree::
   :maxdepth: 4


This section deals with ``Multiprocess Programming``. For data analysts, it seems to be accepted that python is a very slow language. Its strength lies in its rich ecosystem of applications, while speed is a huge drawback. RiskQuantLib provides an easy way to run your project by multi-process. For tasks that are computationally intensive, multi-process running can increase speed by roughly an order of magnitude.

First Thing To Consider
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Multi-process programming is a double-edged sword, and almost programmers will agree that there is no easy way to write multi-process codes very generically for all types of task. Good multi-process programs often require careful debugging and optimization, and will vary slightly from one project to another. It is also critical that the overhead of turning on multiprocessing must outweigh the benefits of multi-processing.

For scaffolding such as RiskQuantLib, the requirements for multi-process programming are reduced because it focuses on data processing, and the graph-structure data store makes the data more tractable. The tricky part is that the OOP (object-oriented programming) style is not well suited for multiprocessing, and serializing the entire graph and transferring it to another process is very resource intensive.

So it is important to remind users who need to use this feature, before changing your code to multiprocessing, you need to consider whether the function you want to call is sufficiently computationally intensive, and you need to consider the memory constraints.

How To Use Multi-Process
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using multiprocessing in RiskQuantLib is very simple and almost identical to using ``execFunc``. If you are not familiar with ``execFunc``, you can refer to the **Iteration** section in :doc:`Instrument_List`.

In short, ``paraFunc`` allows you to parallelize operations on instances of Instrument List. Use:
::

   instrumentListA.paraFunc('someFunc',someParameter)

It is almost totally the same with:
::

   instrumentListA.execFunc('someFunc',someParameter)

They are almost the same with:
::

   for instrumentA in instrumentListA:
       instrumentA.someFunc(someParameter)

The difference is that ``execFunc`` is executed immediately, and the function called by ``execFunc`` can make direct changes to the data graph. Whereas ``paraFunc`` is delayed and you have to use ``paraRun`` to trigger the multiprocessing after you call ``paraFunc`` one or more times. Otherwise the multiprocessing program will not be executed.

In addition, the functions called by ``paraFunc`` do not make direct changes to the datatagram. If changes are made to attributes inside these functions, these changes are not preserved (Any effect on the original data graph is not preserved, because it occurs in another process). This requires functions called by ``paraFunc`` to have a return value, and only the return value can carry data and return it to the main data graph.

**You don't need to optimize the function to use** ``paraFunc`` **, you can still make changes to the properties inside the function, you can treat each process as a pipeline, and these changes will be passed along the pipeline, and successive calls inside the pipeline will be able to access the properties that are changed, except that you can't pass the properties between pipelines, you have to catch the output data at the end of the pipeline and send them back to the main process by yourself.**

A good example is:
::

   instrumentListA.paraFunc('someFuncX',someParameterX)
   instrumentListA.paraFunc('someFuncY',someParameterY)
   instrumentListA.paraFunc('someFuncZ',someParameterZ)
   result = instrumentListA.paraRun()

This is the same with:
::

   instrumentListA.execFunc('someFuncX',someParameterX)
   instrumentListA.execFunc('someFuncY',someParameterY)
   instrumentListA.execFunc('someFuncZ',someParameterZ)

Notice that ``result`` is used here to hold return values, ``result`` should be a list, each element of which is a tuple, (since you're calling three functions in parallel, the return value of each function is packaged and returned.) The first element of the tuple is the return value of the first function ``someFuncX``, the second element is the return value of the second function ``someFuncY``, and so on.

If you define the three functions in the above example this way:
::

   def someFuncX(self):
       self.codeX = self.code + 1
       return self.codeX
   def someFuncY(self):
       self.codeY = self.codeX + 2
       return self.codeY
   def someFuncZ(self):
       self.codeZ = self.codeY + 3
       return self.codeZ

Both the multiprocess and non-multi-process versions work fine. When the non-multi-process version is run, each element of your ``instrumentListA`` will have the additional attributes ``codeX``, ``codeY``, and ``codeZ``, but not when the multi-process version is run. The ``result`` variable in multiprocessing will be a list, and each element will be a tuple of ``(self.codeX, self.codeY, self.codeZ)``.

As we just said, the multi-process version of ``someFuncY`` has no problem accessing the ``codeX`` generated in ``someFuncX``, except that ``codeX`` cannot be accessed in ``instrumentListA``.