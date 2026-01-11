Project Management
====================

.. toctree::
   :maxdepth: 4

One of the most important use of RiskQuantLib is project management. It's necessary to introduce a conception named module. Here in RiskQuantLib, you can define and build a project before you know your data. You can also code some data process logic in instrument class file. If we stop right in this step, close all files, and save this project, it is called module.

In short, *a module is a data process project or model or tool which is suitable for more than one situations*, it could deal with data regardless of data paterns.

There are three kinds of modules in RiskQuantLib, they are *template*, *model* and *tool*.

Initialize Module
^^^^^^^^^^^^^^^^^^^

If you are a new user and just installed RiskQuantLib, then it is recommended that run the following the initialize default modules:
::

    initRQL

Show All Module
^^^^^^^^^^^^^^^^^

You can show all saved modules in your library by using terminal command:
::

   listRQL

After run this command, you will see all modules in your library. Or you can specify the sub-category of modules, use one the following:
::

    listRQL -c template
    listRQL -c model
    listRQL -c tool

Save Project As Template
^^^^^^^^^^^^^^^^^^^^^^^^^^

You can just save any project, no matter it is a RiskQuantLib project or not, in case you would use it some day later.

You can do this by using terminal command:
::

   saveRQL template your_project_path

After run this command, a template will be added into RiskQuantLib template library.

Save Module As Model
^^^^^^^^^^^^^^^^^^^^^^^^

Model is a kind of RiskQuantLib module which is used to calculate statistic models. It is an independent file or directory. By default, RiskQuantLib provides models Copula and KMV, you may define your own models and save them into library.

You can save a module as a RiskQuantLib model by using terminal command:
::

   saveRQL model your_model_path

After run this command, a model will be added into RiskQuantLib model library.

Save Module As Tool
^^^^^^^^^^^^^^^^^^^^^^^^

Tool is a kind of RiskQuantLib module which is used to operate some data-independent logic. It is a file or directory. By default, RiskQuantLib provides tools like *pptTool*, *wordTool*, *excelTool*, *threadTool*, etc. You may define your own tools and save them into library.

You can save a module as a RiskQuantLib tool by using terminal command:
::

   saveRQL tool your_tool_path

After run this command, a tool will be added into RiskQuantLib tool library.

Set Module As Default
^^^^^^^^^^^^^^^^^^^^^^^^^

You can specify a model or tool as default module, after doing this, any new project created by ``newRQL`` will be equipped with this module. Use:
::

    dftRQL module_category module_name

``module_category`` can be ``model`` or ``tool``. ``module_name`` should be the name of module which you see by ``listRQL``, or the index number of it.

Remove Module From Default
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can remove a model or tool from default, after doing this, any new project created by ``newRQL`` will **Not** be equipped with this module anymore. Use:
::

    udftRQL module_category module_name

Again, ``module_category`` can be ``model`` or ``tool``. ``module_name`` should be the name of module which you see in the ``model`` or ``Tool`` directory of your RiskQuantLib project, like ``mailTool``, etc.

Unpack Module
^^^^^^^^^^^^^^^

You can unpack a module by using terminal command:
::

   tplRQL module_category module_name your_new_project_path

After run this command, you will unpack the contents of this module into ``your_new_project_path``, and you can use them as the fundation of another project.

``module_category`` can be ``template`` or ``model`` or ``tool``. ``module_name`` should be the name of module which you see by ``listRQL``, or the index number of it.

Delete Module
^^^^^^^^^^^^^^^

If you want to delete some module, use terminal command:
::

   delRQL module_category module_name

``module_category`` can be ``template`` or ``model`` or ``tool``. ``module_name`` should be the name of module which you see by ``listRQL``, or the index number of it.

Or if you want to delete all modules, you should use:
::

   clearRQL

**Notice: Use this command carefully, cause it can not be un-done.**
