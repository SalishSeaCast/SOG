**************************************
SOG Run & Code Development Environment
**************************************

:Author: Doug Latornell <djl@douglatornell.ca>
:License: Apache License, Version 2.0

This is the root repository for running the SOG_ coupled physics-biogeochemical model for deep estuaries,
and for doing development work on the model.

.. _SOG: http://bjossa.eos.ubc.ca:9000/SOG/

SOG_ is maintained in a set of Mercurial_ distributed version control repositories.
The central, reference copies of those repositories are stored in :file:`/ocean/sallen/hg_repos/`

.. _Mercurial: http://mercurial.selenic.com/

This repository contains 2 components of the SOG_ project:

* The SOG_ command processor Python package (:file:`SOGcommand/`)
* The SOG_ documentation source files (:file:`docs/`)


SOG Command Processor
=====================

The SOG command processor, :command:`SOG`, is a command line tool for doing various operations associated with the SOG model.

Use :command:`SOG help` to get a list of the commands available for doing things with and related to SOG.
Use :command:`SOG help <command>` to get a synopsis of what a command does,
what its required arguments are,
and what options are available to control the command.

Documentation for the command processor is in :file:`docs/SOGcommand.rst` and is rendered at http://www.eos.ubc.ca/~sallen/SOG-docs/SOGcommand.html.


Installation
------------

Documentation on how to set up a fresh SOG_ environment,
including how to install the SOG command processor,
are in :file:`docs/quickstart.rst` and are rendered at http://eos.ubc.ca/~sallen/SOG-docs/quickstart.html.


Source Code and Issue Tracker
=============================

Code repository:

* :file:`/ocean/sallen/hg_repos/SOG`
* https://bitbucket.org/douglatornell/sog (public mirror)

Source browser: http://bjossa.eos.ubc.ca:9000/SOG/browser/SOG (login required)

Issue tracker: http://bjossa.eos.ubc.ca:9000/SOG/report (login required)


License
=======

The SOG command processor code and the SOG documentation are copyright 2010-2014 by Doug Latornell and The University of British Columbia.

They are licensed under the Apache License, Version 2.0.
http://www.apache.org/licenses/LICENSE-2.0
Please see the LICENSE and NOTICE files for details of the license,
and how to cite the SOG project.
