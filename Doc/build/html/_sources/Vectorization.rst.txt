Vectorization
====================

.. toctree::
   :maxdepth: 4


This section deals primarily with ``Vectorized Programming``. This term is not new to data analysts, simply speaking, it is ``Use matrices for operations whenever possible``. Because modern CPUs are basically multi-bit, vectorized data can take advantage of this feature to multiply the speed of operations.

First Thing To Consider
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pure Mathematical Function
-----------------------------

Vectorization turned out to be a double-edged sword just like multiprocess programming. Almost all programmers would agree that functions that can be vectorized are only a very small part of the large family. Because it uses basic CPU parallel instructions, vectorization has strict restrictions on data types, ensuring that only the correct type of data is processed.

**On the user's side, roughly speaking, functions that can be vectorized must be pure mathematical function.**

What is a pure mathematical function? Here it is necessary to make a distinction between a function of programming and a function in mathematics. A programming function is a block of code defined by a keyword that accomplishes a particular computer task, which often involves logical judgment, loops, input and output. Mathematical functions, on the other hand, are variable-to-variable mappings that must yield the same output given the same input.

**Programming functions tend to be state-dependent, such as the function to read a file** ``pandas.read_csv`` **which takes a file path and returns the contents of that file. If you change the contents of file, the returned contents will change as well. However, notice that the value of the parameter received by this function does not change at all; it remains the path of that file. The reason why it returns a different value even if the parameter value remains the same is that it depends on the state of that file.**

**Mathematic functions are pure, state-free. For example, the function** ``numpy.exp`` **must return the value of the natural logarithm** ``e`` **when it receives a parameter of** ``1`` **, no matter when and in what context the function is called.**

Therefore, when using this function, extra care needs to be taken to make sure that your function is not state-dependent and is a purely mathematical function. Also, the process of vectorization involves wrapping and unwrapping of data, which can consume some computational resources. Of course, for functions that can be vectorized, this extra resource consumption is often negligible compared to the speedup of vectorization.

Based on the requirements of pure mathematical functions, **many of python's logical keywords are not allowed**. Keywords such as ``if`` , ``for`` , ``is`` , ``in`` , etc. are not allowed to be used in functions to be vectorized. If you want to perform logical operations, you must be familiar with how to use logical matrices, which we will demonstrate below.

How To Use Vectorization
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using Vectorization in RiskQuantLib is very simple and almost identical to using ``execFunc``. If you are not familiar with ``execFunc``, you can refer to the **Iteration** subsection in :doc:`Instrument_List`.

To vectorize a function of Instrument, you can use ``vecFunc`` with instance of its Instrument List:
::

   instrumentListA.vecFunc('someFunc',someParameter)

It is almost totally the same with:
::

   instrumentListA.execFunc('someFunc',someParameter)

They are almost the same with:
::

   for instrumentA in instrumentListA:
       instrumentA.someFunc(someParameter)

The difference is that ``execFunc`` is sequential, where the first element executes ``someFunc`` firstly, and the second element executes that function after that. If you use ``vecFunc`` , then very inaccurately, ``someFunc`` of every element are called almost at the same time, which makes it impossible to make the next element's operation depend on the result of the previous element's operation, like ``fold`` function.

Fortunately, the function called in ``vecFunc`` can use almost any ``numpy`` function internally. Because ``numpy`` functions are almost always purely mathematical. In fact, ``RiskQuantLib`` uses ``numpy`` for vectorization.

In addition, ``vecFunc`` can modify the data graph. Assignments will still work. But assignment operations cannot be truely vectorized; they just don't cause vectorization exceptions, and are thus compatible with vectorization. Assignment operations tend to slow down vectorization.

**You don't need to optimize the function specifically to use** ``vecFunc`` , **the function can still make changes to attributes internally. You just need to make sure that the function being called is purely mathematical, with no logical judgment keywords.**

A good example is:
::

   instrumentListA.vecFunc('someFuncX',someParameterX)
   instrumentListA.vecFunc('someFuncY',someParameterY)
   instrumentListA.vecFunc('someFuncZ',someParameterZ)

This is almost the same with:
::

   instrumentListA.execFunc('someFuncX',someParameterX)
   instrumentListA.execFunc('someFuncY',someParameterY)
   instrumentListA.execFunc('someFuncZ',someParameterZ)

If you define above functions like:
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

Both the vectorized version and the non-vectorized version work fine. The vectorized version tends to be 3-5 times faster than the non-vectorized version. Notice that the second function is able to access the data graph node variables generated by the first function.

Also, notice that all three of our functions here are purely mathematical. And functions like the one below are not vectorizable:
::

   def wrongFuncX(self):
       self.codeX = self.code if self.code >= 1 else 3
       return self.codeX

To use logical judgment, you must use a logical matrix. To implement the functionality of the above function while using vectorization, you should change the function to:
::

   def rightFuncX(self):
       logicMatrix = (self.code >= 1) 
       self.codeX = self.code * logicMatrix + 3 * (1 - logicMatrix)
       return self.codeX

**For functions that can be vectorized, its parameter can also be high-dimensional.** For example, the ``self.code`` property in the code above is a numeric variable by default. However, it can actually be a higher dimensional variable, such as a numeric matrix, which does not affect vectorization.

High Dimensional Vectorization And Manual Vectorization
-----------------------------------------------------------------------------

**It is possible to use constants as parameter of the vectorized function, but when passing in a vector of constants or a sequence of constants, you need to make sure that the parameter are already vectorized, because only the attributes of nodes will be automatically vectorized, and the constants will not be automatically vectorized.** Let's illustrate this with an example:
::

   def someFuncWithPara(self, para):
       self.codeX = self.code + para
       return self.codeX

For this function, if you want to call it by vectorization, then by default ``self.code`` , ``para`` , ``self.codeX`` should be numeric variables, such as ``float`` variables. But in fact, ``self.code`` , ``self.codeX`` can all be numeric vectors or matrices, such as ``numpy.ndarray`` variables whose elements are ``float``. This is because all attributes of data graph nodes are automatically vectorized by ``RiskQuantLib``.

But the problem is with the ``para`` variable. If ``para`` is a ``float`` variable, then when ``self.code`` is a vector, there is no problem because constants are automatically broadcast to each element of the vector. What happens if ``para`` is also a ``numpy.ndarray`` whose elements are ``float``?

Since ``RiskQuantLib`` can't tell if the passed parameter is vectorized or not, ``RiskQuantLib`` will use ``para`` directly on the vectorized attribute variable. That is, ``para`` will not be processed additionally. So if ``para`` is also a ``numpy.ndarray`` whose elements are of type ``float``, then an error is likely to occur, unless these two ``numpy.ndarray`` can be added.

If you want the program to work correctly, then you need to make sure that you vectorize the ``para`` constant manually before vectorizing the call to ``someFuncWithPara``, i.e., ``para`` should be an iterable object and its length should be equal to the length of the current list. The first element of ``para`` should be the parameter passed to the first element of the ``RiskQuantLib`` list, the second element of ``para`` should be the parameter passed to the second element of the ``RiskQuantLib`` list, and so on.

**The good thing is that this is very rare, and if you need to use a different parameter on each element, why not set it as an attribute? It makes more sense to consider changing the link structure of the data graph, using** ``match`` , ``link`` , ``join`` , ``connect`` **to change the data graph**.

How To Combine Multiprocessing And Vectorization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Multi-processing and Vectorization give ``RiskQuantLib`` a very flexible and powerful data handling capability as two ways to increase speed. With careful debugging and design, programs written in ``RiskQuantLib`` can often be up to 50% as fast as matrix programs written in ``pandas`` and ``numpy``. In cases involving very high data IO, network interactions, etc., ``RiskQuantLib`` can be even faster than matrix programs. (Of course, very few programmers use numerical libraries such as ``pandas`` to handle high IO data.) The advantages of ``RiskQuantLib`` such as simplicity of coding, low maintenance cost, and high code reuse rate become even more significant when considering code modification, such as in the area of data exploration.

Usually, ``numpy`` does the CPU scheduling automatically, but you can use both multiprocessing and vectorization if you need to:
::

   result = instrumentListA.groupByFunc(lambda x:int(numpy.random.uniform(0,4))).paraFunc('vecFunc','someFuncX',someParameterX).paraRun()

The meaning of the above code is that ``instrumentListA`` is randomly divided into four groups, a new process is started for each group, and each process performs vectorization operations, calls the ``someFuncX`` function, and then collects all the results and stores them in the ``result`` variable. Notice that because of the use of multiprocessing, which is pipelined and changes to the data graph are not preserved, ``someFuncX`` must have a return value and must receive it via a variable for subsequent processing.

The above code demonstrates the amazing abstraction and flexibility of ``RiskQuantLib``. You can change the way your program works with a single line of code without making any changes to the data processing logic or the data graph. The use of chained calls makes the program even more readable. In ``paraFunc`` we use ``Tunneling Index``, which we mentioned in the previous section, so that for multi-layer graphs we can nest any number of function calls (up to the depth of the graph) in ``paraFunc`` or ``execFunc`` or ``vecFunc``, as if we were tunneling through a graph node in the upper level to get to the next level of the graph, and then calling the functions in the next layer. Finally, we use ``paraRun`` to trigger multiprocessing.

**Unfortunately, if** ``someFuncX`` **is defined as we have showed above, then on most computers the above code should not run as fast as if it were vectorized directly:**
::

   result = instrumentListA.vecFunc('someFuncX',someParameterX)

Using both multiprocessing and vectorization is not even as fast as direct iteration:
::

   result = instrumentListA.execFunc('someFuncX',someParameterX)

The reason for this is simply that ``someFuncX``, which we defined above, is so simple that the overhead of using multiprocessing already far outweighs the benefits. So in this case, it's not a good idea to use multiprocessing. Typically, the number of operations in the ``someFuncX`` function should be more than 100,000 to ensure that the use of multiprocessing has efficiency gain. This is what we mean when we say that before using multiprocessing and vectorization, you need to think about the environment where your program is running and make sure that the overhead is worthy.