pymato
======

The Simple Python Tomato (Pomodoro) timer.


Usage
-----

.. code::

  $ python -m pip install --user pymato
  $ pymato pom doing something cool
  Task - doing something cool
  0:24:59

When the timer runs out it will emit a visual bell, so your terminal should
blink or notify you of activity. Want to see what you've been working on?

.. code::

  $ pymato log
  2018-02-28
              25m writing pymato documentation
              25m doing something cool
  -----------------------------------------
              50m total pomodoro time


Right now that's pretty much all it does. It saves your logs to ``pymato.log``
in the current folder. You can delete or edit entries that way. If you start a
task and you get called away in the middle of your pom, you can just hit
ctrl+c. Then it will ask if you'd like to save that pom.

.. code::

  $ pymato pom a task that will get interrupted
  Task - a task that will get interrupted
  ^C0:23:59Aborted - save to log anyway?
  y/[n]: y
  $ pymato log
  2018-02-28
              25m writing pymato documentation
              25m doing something cool
               7m doing something cool
  -----------------------------------------
              57m total pomodoro time


Future Goals
------------

I'd like to have ``pymato sum`` that would give you a summary - probably with
the option to group by either task or day. Might be nice to see some kinds of
ascii graphs or something too. I'd also be down with the ability to add notes
to entries if you need to keep a record of things you've done. Or the ability
to link work to your git/hg/svn commit history.
