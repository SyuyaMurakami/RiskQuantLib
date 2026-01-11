Component
====================

.. toctree::
   :maxdepth: 4

This section deals with the ``Src`` folder, which can be like any folder where you can put all your python source code. You can then import and run it from the main function, or run the code in the ``Src`` folder directly. You can write comments between codes, just like the old way.

However, there is something very special about the source code files in the ``Src`` folder, **the comments in any .py file under Src folder have the ability to control code generation** . RiskQuantLib is a scaffolding for easier development of some large projects. It uses code to generate code, which is one of the core concepts of RiskQuantLib. The Instrument, Instrument List, the Set function family, and the Get function family, which appeared frequently in the previous tutorials, can all be seen as special cases of code generation. Now you may get it, RiskQuantLib can actually generate code with arbitrary rules and arbitrary logic, as long as you declare how the code is generated.

If you use RiskQuantLib for every data analysis project, your data processing logic will turn into a number of building blocks under ``Src``, more and more project experience will result in more and more building blocks. When you need to start a new project again, you can use comments to tell RiskQuantLib how to quickly build a project from the blocks you already have, and then add parts that you need, but can't be found in the existing program blocks. Of course, the written parts will become new building blocks.

**Here, we formally name the Src folder as component folder, and the individual files in it as components.**

Why Component Is Needed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you just want to learn how to use the components folder, you can skip this part and go to :ref:`how_to_use_src`.

Main Reason
-------------------

The src folder helps you to keep logically related code in the same file, making it a building block that can be reused.

One of the most significant problems with OOP (Object-Oriented-Programming) is that the code needed to accomplish a certain logic is placed in separate classes and seperate files. This does make the project easier to maintain. However data analysis is a very different task, it is unlike some application on industry production, it does not have a stable program runtime environment. For data analysis projects, exploratory analysis is usually required, which means frequent changes to analysis logic. This makes the user to keep traveling between class files to modify their code. And if, after a while, you need to rework the code for a new, similar project, you'll have trouble finding the place of code that accomplish that certain logic.

Of course, writing comments can solve this problem to some extent, but for most programmers, writing comments is very painful. the solution given by RiskQuantLib is to put the code related to the same logic all into the same .py file, and then use a very simple commen to tell RiskQuantLib which class file to put them into. You already know the core concept of RiskQuantLib, which is **Generate code with code** , and by now, you should have figured out another core concept of RiskQuantLib, which is **Control the location of code with code** .

Subtle Reason
--------------------

You may still have some questions about why I would need a component folder. Python or any language's import mechanism of function and library already provides the ability to encapsulate a program into components, which can be easily used by user. For example, as we said at the beginning, you can put all the python source code in Src in it and then import it from the main function.

You are right. If your project isn't complex enough, or if you don't usually open a new data analysis project very often, you won't need to use features like components. But data analytics is very different from other projects, data analytics projects are not **stable** enough. Again and again, data analysts create a data project, analyze it, get conclusions, and then delete or archive the project. Then all of these are repeated. Any data analysis process is unique in its own way, forcing the data analyst to paste a portion of the code from the past and make minor changes before it can continue to run.

**Then you start to think about the question, why is code reuse so difficult in the field of data analytics?**

Of course you may have many answers, some people blame python's datatype mechanism, which does not do type checking, making the code much more generalizable and at the same time much more buggy, and you have to modify the code because of minor bugs. Others believe that this is the essence of data analysis, after all, the process of washing data may have the same meaning with constantly fine-tuning the data to suit your code.

The answer given by RiskQuantLib is that **the low reuse rate is due to the fact that the packaging unit of the code is not small enough** . Think about it, the smallest unit of code that is almost reusable in python and other computer languages is a function (you can say it's a variable, but a variable can't perform a whole logic, for functional languages a variable can be a function and thus perform a whole logic, so in general a function is the smallest reusable unit of code in most languages). And function, on the other hand, has been defined by modern mathematics in a number of ways, such as the concepts of input, output, and mapping. (Variables are even more restrictive; consider data types, which are the biggest restriction on variables.) These definition can also be limitation.

Code is actually letters, and the repetition of letters makes up a complete function. Maybe, letters are the most basic particles of code. After that it comes to functions and variables. This is the second-tier particles in programming languages. The recurring problem of low code reuse in such a system leads us to wonder if there is a zone where the scale of packaging unit of code is larger than letters but smaller than functions?

The answer is of course yes, and this is the solution given by RiskQuantLib. This kind of code that can recur inside a function is what we might call a ``chunk``, or ``code block`` . This concept has been used by programming languages such as Haskell, whose lazy mechanism is largely implemented using ``chunks``. In the Src folder of RiskQuantLib, you can write all sorts of ``chunks``, not just functions.

Let's summarize why we might need the Src component folder:

**A code block is a collection of code statements that can be repeated, and the code within the block can be incomplete and unable to perform any function on its own.**

**A code block can be large or small, in terms of how much it contains, usually a block is larger than a word and smaller than a function, and a function should consist of multiple blocks.**

**The smallest repeatable logical unit of code has changed from a function to something smaller: a code block.**

**Finally, code blocks can be reused, and this reuse can be automated by the program, thus increasing code reuse.**

.. _how_to_use_src:

How To Use Component
^^^^^^^^^^^^^^^^^^^^^^^^^^

Comment Control Syntax
------------------------

*Distribute*
>>>>>>>>>>>>>>

In the previous tutorial on how to build your project, you should have noticed to how to use comment control syntax with the Src folder. Let's review this example:
::

   #->stock
   def sayHello(self):
       self.greeting = self.name + "_hello"

These codes are in ``Src/test.py`` , and written just from the beginning of line, it should not be written within any classes. It is actually all contents of ``Src/test.py`` .

What it means is that it defines a ``sayHello`` function and binds it to the ``stock`` Instrument. You should notice the comment on the line above the function definition, starting with the normal ``#``, but immediately followed by a ``->`` symbol. This is one of the comment control syntax, called **distribute**. When you need to add a class function to an instrument, you can use a comment to tell RiskQuantLib exactly where to put the function into.

**Note: The distribution syntax takes effect for a number of lines after it. The distribute syntax must be at the beginning of the line until you run into the next distribute syntax or the end of the file, and the distribute syntax puts all the code in between into the target location.**

*Tag*
>>>>>>>>>>>>

Let's see another example:
::

   #->bond@import
   import os

It means to distribute the ``import os`` statement to the ``import`` tag of the ``bond`` instrument. The ``@`` here splits the name of the destination file you want to distribute into and the name of the destination tag. Here we meet the so-called ``Tag``, which are not difficult to understand because there are many locations in a destination .py file where code can be inserted, so how do we know whether we should insert code into the third or fifth line of the destination file? The tags are there to help us determine the location.

You can open the target file, which is located at ``RiskQuantLib/Instrument/Security/Bond/bond.py``, and you can see the style of the tag, which looks like this:
::

   #<import>
   #</import>

Tags are very similar to elements in html. A tag starts with ``#<tagName>`` and ends with ``#</tagName>``. Code can be automatically inserted between the beginning and the end of the tag. The content between these tags is rebuilt every time you do a build action of the project.

**Note: The distributed code can only be inserted in the middle of the tags. The code in the middle of the tags is automatically generated by the RiskQuantLib; user-defined code should not be written between the tags.**

**Note: You can define your own tags, and custom tags can also be used in comment control statements.** 

For example, if you added another new tag in ``RiskQuantLib/Instrument/Security/Bond/bond.py`` called ``ifItIsConvertibleBond``, your file would then look like this:
::

   #!/usr/bin/python
   #coding = utf-8
   import numpy as np
   import pandas as pd
   from RiskQuantLib.Instrument.Security.security import security
   from RiskQuantLib.Auto.Instrument.Security.Bond.bond import bondAuto
   from QuantLib import Bond
   #<import>
   #</import>

   class bond(security,Bond,bondAuto):
       """
       bond is an instrument class, used as nodes of data graph.
       """
       #<init>
       def __init__(self,codeString,nameString,instrumentTypeString = 'Bond'):
           security.__init__(self,codeString,nameString,instrumentTypeString)
       #</init>

       #<initQuantLib>
       def iniPricingModule(self,*args):
           Bond.__init__(self,*args)
       #</initQuantLib>

       #<bond>
       #</bond>

       #<ifItIsConvertibleBond>
       #</ifItIsConvertibleBond>

Then you can add code in ``Src/test.py`` :
::

   #->bond@ifItIsConvertibleBond
   def ifItIsConvertibleBond(self):
       if self.bondType == 'convertibleBond':
           return True
       else:
           return False

After run ``build.py``, your code will be inserted between tags. 

**Notice: You can define Tag anywhere, including inside functions. The generated code will keep the indentation level of the Tag.**

Let's look at an example of defining a Tag inside a function:
::

   class bond(security,Bond,bondAuto):
       """
       bond is an instrument class, used as nodes of data graph.
       """
       #<init>
       def __init__(self,codeString,nameString,instrumentTypeString = 'Bond'):
           security.__init__(self,codeString,nameString,instrumentTypeString)
       #</init>

       #<initQuantLib>
       def iniPricingModule(self,*args):
           Bond.__init__(self,*args)
       #</initQuantLib>

       #<bond>
       #</bond>

       def ifItIsConvertibleBond(self):
           if self.bondType == 'convertibleBond':
               #<ifItIsConvertibleBond>
               #</ifItIsConvertibleBond>
           else:
               return False

Then you can write code in ``Src/test.py`` :
::

   #->bond@ifItIsConvertibleBond
   print("This is a convertible bond!")
   return True

After run build action, ``chunk`` will appear between tags.

*Multi-Destination*
>>>>>>>>>>>>>>>>>>>>>>>

**If you have more than one destination, you can use commas to split them.**

For example, if you need to control imported libraries by a separate file ``import.py`` in the Src folder, you can do such:
::

   #->stock@import,bond@import,future@import,option
   import numpy as np
   import pandas as pd

You can always add new destinations after the control syntax to tell RiskQuantLib that it needs to put this ``chunk`` into another target location. Of course, these destinations can have different Tags from each other or have no Tag.

Multi-Logic Project
-----------------------

Usually a data analyst creates more than one project when dealing with the same problem. For example, if you want to know if a stock trading strategy is working and apply it in trading. Most likely, you would start with a data project to analyze past data and get a conclusion on whether it works or not. If it works, you would then start a production project to send you those filtered trade targets every day.

The question is, why does such thing happen again and again?

With the component functionality provided by the Src folder, we can solve this problem very well, RiskQuantLib separates the data structure from the data processing logic. All our **processing logic** is put into the Src folder, while the **data structure** is defined by the user, and the **project structure** is kept by ``config.py``. When we need to move from backtesting to production, we simply replace the contents of the Src folder while keeping the rest of it just as the same.

The only valid source files under the src folder are the ones with extension name ``.py`` or ``.pyt``. So if we need to remove the entire code logic, we can change the filename suffix of the file, and after build the project, the entire processing logic will disappear from the project.

You can even do this by changing the folder name. Assuming that all the code for your backtesting framework is located in the ``Src`` folder, changing the name of the folder to ``Back_Test`` and creating a new blank Src folder and build it will change the project to a production environment once and for all, while preserving the **data structure** and **project structure**.

Of course, RiskQuantLib provides convenient ways to switch between the two sets of processing logic, and if you are in production logic and want to revert back to backtesting logic, then run the command below:
::

   python build.py -r Back_Test

``-r`` means build this project from the given folder.