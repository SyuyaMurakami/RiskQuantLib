About
====================

.. toctree::
   :maxdepth: 4

This project was started in 2019, when I tried to find a better way to deal with all kinds of annoying data project in my job. By that time, I was a little bit of tired about using pandas and numpy in python, or OOP something. Honestly speaking, I loved pandas, it's like my friend who companied me through my whole university life. But one day, suddenly, I realized that no shinning points exists on it any more. It stopped to surprise me. The only thing left is the sense of familiarity.

It is also at that time, my friend Daniel came to my town and visited me. Daniel is a creative guy, who always inspires me with some greaaaaaaat ideas. We even designed a blueprint about how to use models in thermodynamics to explain stock movement, which is a little crazy and we both agreed that our parents or grandparents would never use this to decide which stock they would buy.

 `You should talk this with Prof. Wang, I am pretty sure he will curse you like you are the most shameful apostate of Physics School.`

That was what Daniel told me. Prof. Wang is our favourite professor in our University, who thinks I should never changed my major. I said maybe he was right, I was really fed up with data which keep pouring in. 

 `Do you remember what you said when you are applying for your graduate degree in finance?`

 `Of course not, that's many years ago.`

 `Let me walk you through it, you said you are done playing with god, and wanted to play with human. Now you are done, too?`

 `No, I just start to believe in god again. Game of human is much worse.`

 `Worse by what?`

 `Every day is the same thing, price, amount, volume, blabla...and you deal with them in the same way, machine learning or something, matrix here, matrix there, matrix everywhere...`

 `Then why stick with matrix?`

 `It is fast, and our computer tech is all about semiconductor lattice, by nature, it is matrix.`

 `That doesn't sounds like you, since what time you are the one who consider limits? I'm the one who tell you limits, you are the one who gives shitty ideas.`

 `Are you kidding? The tree or graph computer is never invented, are you saying I can do it? There was indeed a team which made a water drop computer, too slow to use.`

 `Then do it with a software? You still use matrix computer, but you can do something in software by tree or graph, then convert it somehow to matrix automatically.`

That is the beginning of this story.

A Road Of Madness
^^^^^^^^^^^^^^^^^^^^^^^^^

I took it serious. In the following two weeks I talked a lot with Yanki, my colleague, about which language I should use. Using classes in python to form tree and graph was not the first choice in our mind, it is slow and primary. I thought framework with struct in C++ could be better. Yanki insisted the core should not be how fast it could run, it should be how fast you can write your code and keep evolving it. Graph computation could never be as fast as matrix as long as you use semiconductor computer, he said, so why not be mad, just give it up at the very beginning.

Both Yanki and I knew there already exist many graph library like NetworkX in python or Boost Graph Library in C++. They are not like we I had in my mind. After reading their documents, I still had the question: How exactly does these library make data processing more joyful? You could not even write a proper function easily to calculate the data you want. They are more like enhanced graph database for adding, deleting, filtering, altering data, or apply some graph algorithm. They are suitable for natural graph data, such as human relationship, etc. The thing we want is something we can use for any data, but dealing with it by graph structure.

These two things gave us the fundamentation of RiskQuantLib:

**Generalizability is the first, Speed is the last.**

A month later I began to write the first line of RiskQuantLib. The 0.0.1 version used excel file to hold information about instrument and instrument list, making it a real toy project. To speed up coding and make it as joyful as we expect, we finally gave up using C++ and SFINAE (Substitution Failure Is Not An Error) and turned into python and inspection. Daniel also agreed with this, but the reason was the prototype needs to be iterted as fast as we could.

There is one thing we worry about, that is using class in python will make user to take RiskQuantLib as an OOP library, which is far from what it should be. But if we add too many new things into it, we are afraid that it will be like another model in thermodynamics to explain stock movement, and no body understands or uses it.

 `Do you know how many stars we have in Github?`

 `Three, by now, it's great!`

 `You know we do have three people involved in this project, right?`

 `Easy, man, Daniel never stars our project, means we still have a fan from this planet.`

 `If you are going to start your own business, don't forget to tell me. I will short your company for sure.`

 `Thanks, I will.`

The Way You Dance
^^^^^^^^^^^^^^^^^^^^^

There was a discuss between Daniel and I, about how to make our project not be like a graph database. This lead to another question: Should we store data by graph structure or calculate by computation graph? We do the first, we would be another graph database, we do the second, we would be another tensorflow. It came to a dead end.

Luckily, like Daniel said, I am always the crazy guy among us.

 `We do both, we hold data by graph, and do calculation by graph.`

 `That is impossible. If data is formed into graph, and all calculation is formed into another computation graph, how could you combine them and make it work?`

 `Think data as island, edges bwtween them are like bridges, if we do computation, we will use some data, so we can go across bridges to one island, get data, and then go to another one, untill we get all of them.`

 `That, my friend, is interesting.`

 `So any function should be like a traveler, goes from one island to another, remind your of what?`

 `Seven Bridges of Königsberg!`

 `Right! That is what we will do. We will make every call of function as the problem of Seven Bridges of Königsberg`

I still remember how Daniel looked like when he heard about my idea. It was like he saw his grandma fighting with a honey badger with her dust catcher. And I continued to say:

 `To do this, any function should have memory, it should take one parameter from one node, remembers it, and becomes into a new function, goes to next node, and so on. Function, no matter how many parameters it needs, can only get one parameter at one time.`

 `Bro, do you know what you are talking?`

 `What?`

 `Do you know Curry? Haskell Curry?`

 `Never heard about him.`

 `You are not the first one to think about this, it has been come up with by this man 100 years ago.`

 `I'm not finished. That is one way, another way is we can stand on one island, and send messagers to different islands, get the data we need and come back, and do calculation, make one messager to carry the result and send it to the island where we want to store this result.`

This is how ``apply``, ``execFunc``, ``tunneling index`` is born. ``apply`` is the first way, while ``execFunc`` is the second way. When I deal with my data, I imagine myself dance with it, it should be enjoyable and elegant. These two ways are exactly what in my dream about how I should dance with data. They make me understand what I realy need:

**Data, once created, should never be changed or removed or copied or deleted, it remains there and can only be linked to. The same data should never appear twice.**

**The way you call your function matters. Any call of function should depend on the visit order of data graph.**

Our Mentor
^^^^^^^^^^^^^^^^^

Not long after that, I started to read some research of Haskell Curry. I'm surprised that there is a language named after him. And this language, Haskell, has so many things just like what I'm thinking about. One thing, I should mention here, is the way that it deals with exception. I can not agree more with it:

**Any exception should be considered in Monad like Maybe, passed through data pipe, and not cause interruption of program.**

This is why you barely see error when running RiskQuantLib project. It does not mean you have a right program, on the contrary, it requires more caution when coding.

Another thing appear a lot in RiskQuantLib is lambda function, it is just like Haskell, it is the certainty of making function to travel through nodes. 

The lazyness of Haskell gives me inspiration, that code is actually block of strings, doesn't need to be run just when they are put down. I make a bold move, I think maybe they are not necessarily written by hand, we can somehow generate them by machine and insert them to the place we want them be.

This is how ``Src`` component folder is born. Like component in web deveploment, I think we can try it in python with data analysis project.

In late 2023, we found a way to use multi-processes and vectorization in RiskQuantLib, making it faster. Finally, speed is not the flaw any more. These work is inspired by numpy, dask, joblib, etc.

What Is Next
^^^^^^^^^^^^^^^^^^^^

Daniel thinks it is time to give up python and turn into a more basic way, an interpreter, he is talking about. He thinks we should have our own python interpreter, embedded with RiskQuantLib, along with CPython. That is definitely mountains of work.

Yanki is cool with what we have now. He thinks adding UI to RiskQuantLib to allow users to see what they are doing is critical. Why not, I would like a UI, too, if it will not be developped by myself.

As for me, I always get shitty ideas. I plan to get a Meta Quest or Apple Vision or any VR device, to make an IDE in VR world, which is embeded with RiskQuantLib. I want users to see and feel how they travel across bridges and link islands. I want to analyse data like taking a tour in California. I'm pretty sure Yanki is preparing his money to short my company which will never be created.