.. :Author: Doug Latornell <djl@douglatornell.ca>
.. :License: Apache License, Version 2.0
..
..
.. Copyright 2010-2014 Doug Latornell and The University of British Columbia
..
.. Licensed under the Apache License, Version 2.0 (the "License");
.. you may not use this file except in compliance with the License.
.. You may obtain a copy of the License at
..
..    http://www.apache.org/licenses/LICENSE-2.0
..
.. Unless required by applicable law or agreed to in writing, software
.. distributed under the License is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.


Getting Started with SOG
========================

SOG_ is maintained in a set of Mercurial_ distributed version control repositories.
The central, reference copies of those repositories are stored in :file:`/ocean/sallen/hg_repos/`.

.. _SOG: http://bjossa.eos.ubc.ca:9000/SOG/
.. _Mercurial: http://mercurial.selenic.com/


SOG Run & Code Development Environment
--------------------------------------

If you're impatient, you can get a fresh SOG environment set up on one
of the :kbd:`ocean` machines with the commands:

.. code-block:: sh

   $ hg clone /ocean/sallen/hg_repos/SOG
   $ cd SOG
   $ make env

This will create a SOG environment in a directory called
:file:`SOG`. The environment looks like this::

  SOG/
       SOG-code-ocean/ - reference copy of the SOG-code repository
       SOG-code-dev/ - clone of SOG-code-ocean for code development work
       SOG-initial/ - SOG initialization data repository
       SOG-forcing/ - SOG forcing data repository
       SOG-test/ - directory for reference test results
         SOG-dev-yyyy-mm-dd/ - ref test results from SOG-code-dev on yyyy-mm-dd
                                 profiles/ - profile output files
                                 timeseries/ - timeseries output file
         SOG-ocean-yyyy-mm-dd/ - ref test results from SOG-code-ocean on yyyy-mm-dd
                                 profiles/ - profile output files
                                 timeseries/ - timeseries output file
       SOG-project/ - directory for doing SOG runs in
                        profiles/ - profile output files
                        timeseries/ - timeseries output file

Feel free to to rename the default :file:`SOG-project` directory to
something more appropriate to you project.

For details of how to customize this process, and links to other
documentation like the recommended workflow in this environment, read
on...


Create a SOG Environment with a Different Name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create a fresh SOG environment called something other than :file:`SOG`
use the commands:

.. code-block:: sh

   $ hg clone /ocean/sallen/hg_repos/SOG newSOG
   $ cd newSOG
   $ make env


Create a SOG Project Directory with a Different Name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create a fresh SOG project directory called something other than
:file:`SOG-project` (:file:`SOG-hindcast`, for example) use the
commands:

.. code-block:: sh

   $ cd SOG
   $ make project PROJECT_NAME=SOG-hindcast


Create a SOG Environment on a non-:kbd:`ocean` Computer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to run SOG or work on the code on your own computer there
are a few pre-requisites. It's pretty easy to get them set up on Linux
or OS/X and probably a bit more of a challenge on
Windows. Pre-requisites:

* Mercurial_ >1.0; it's probably already installed
* an account on :kbd:`ocean` with :command:`ssh` key access set up
* g95_ FORTRAN compiler; not required to create the SOG environment,
  but needed to compile and run the code. You'll probably need to use
  your OS's package installer, or download and install the appropriate
  binary.

  .. _g95: http://www.g95.org/

With the above in place, you can set up a fresh SOG environment with
the commands:

.. code-block:: sh

   $ hg clone ssh://<user>@<host>.eos.ubc.ca//ocean/sallen/hg_repos/SOG
   $ cd SOG
   $ make env HG_REPOS=ssh://<user>@<host>.eos.ubc.ca//ocean/sallen/hg_repos

where :kbd:`<user>` is your :kbd:`ocean` user id, and :kbd:`<host>` is
the name of one of the :kbd:`ocean` computers; e.g. :kbd:`nerka`,
:kbd:`grinder`, :kbd:`herring`.


SOG Command Processor
~~~~~~~~~~~~~~~~~~~~~

The SOG command processor, :command:`SOG`, is a command line tool for
doing various operations associated with SOG.

At the very least you will want to use :command:`SOG run` to run SOG.


.. _SOG_CommandProcessorInstallation-section:

Installation
++++++++++++

The SOG command processor is a Python package called
``SOGcommand``. To install it so that you can use it:

#. Confirm that you are using Python 2.6 by default. The response to
   the commmand:

   .. code-block:: sh

      $ python --version

   should be something like :kbd:`Python 2.6.5`. If not, create an
   alias:

   .. code-block:: sh

      $ alias python '/usr/local/python26/bin/python2.6'

   if you use :command:`csh`, or

   .. code-block:: sh

      $ alias python='/usr/local/python26/bin/python2.6'

   if you use :command:`bash`. Add the same command to your
   :file:`~/.cshrc` or :file:`~/.bashrc` file so that the alias takes
   effect every time you log in or create a new shell.

#. Create your personal Python 2.6 packages directory:

   .. code-block:: sh

      $ mkdir -p ~/.local/lib/python2.6/site-packages

#. Install ``SOGcommand`` in development mode so that updates will
   take effect automatically:

   .. code-block:: sh

      $ cd SOG
      $ python setup.py develop --user

#. Test it with :kbd:`~/.local/bin/SOG help` or :kbd:`~/.local/bin/SOG
   --version`.

#. Add :file:`~/.local/bin` to your path, both at the command line,
   and in your :file:`~/.cshrc` or :file:`~/.bashrc` file so that the
   :command:`SOG` command is available every time you log in or create
   a new shell.


Use
+++

Use :command:`SOG help` to get a list of the commands available for
doing things with and related to SOG. Use :command:`SOG help
<command>` to get a synopsis of what a command does, what its required
arguments are, and what options are available to control the command.

See :ref:`SOG_CommandProcessor-section` for more details.


SOG Documentation
~~~~~~~~~~~~~~~~~

More documentation about SOG can be found online at
http://eos.ubc.ca/~sallen/SOG-docs/. The source files for the
documentation are in :file:`SOG/docs/`. The documentation includes:

* :ref:`recommended workflows<workflows-section>` for the environment
  described above
* detailed documentation for the :ref:`SOG_CommandProcessor-section`
* information about the :ref:`SOG buildbot automated testing
  system<SOGbuildbot-section>`
* information about the :ref:`SOG trac code browser and issue
  tracker<SOGtrac-section>`

