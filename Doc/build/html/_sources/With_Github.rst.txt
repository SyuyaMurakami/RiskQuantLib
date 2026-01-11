With Github
====================

.. toctree::
   :maxdepth: 4

In **Project Management**, we know that RiskQuantLib can save a project as a template, which can then be used to initialize the next data analysis project. Such usage is limited to just one computer. If you are trying to use RiskQuantLib in a team, you may need to share code and template projects with your team members. RiskQuantLib accomplishes this through Github, and with preconfigured commands, RiskQuantLib can fetch all public projects on Github and save them as projects on the local computer templates.

Get Repository From Github
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the terminal, use the following command to get the Github project, below we will use `hub project <https://github.com/github/hub>`_ as an example.
::

   getRQL https://github.com/github/hub

After run this command, you can see：
::

   Successfully Installed hub

You can also view the projects that have been saved as template projects by using terminal command ``listRQL`` .

Fuzzy Searching
^^^^^^^^^^^^^^^^^^^^^^^

If you don't know the exact URL of a Github repository, you can fuzzy-search it by roughly keywording it. Entering a keyword after the ``getRQL`` command triggers the fuzzy query function.
::

   getRQL hub

Running this command will tell RiskQuantLib to query Github for all relevant projects and rank them by relevance and number of stars in the project. You can see the following interface:
::

   Total repositories:  266905
   Show Top Github Repositories:
   ------------------------------
   0 -> ohmyzsh
   1 -> HelloGitHub
   2 -> GitHub-Chinese-Top-Charts
   3 -> rclone
   4 -> CodeHub
   5 -> hub
   6 -> hubot
   Choose One From Above:

Enter the number in front of the corresponding repository to download this repository as a local project template, in this example, we choose ``HelloGitHub``, so you should enter 1, and then you will see the following:
::

   Successfully Installed HelloGitHub

Then you can use the saved template project to initialize the new project.