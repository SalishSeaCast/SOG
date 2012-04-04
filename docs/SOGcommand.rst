.. _SOG_CommandProcessor-section:

SOG Command Processor
=====================

The SOG command processor, :program:`SOG`, is a command line tool for
doing various operations associated with SOG.


Installation
------------

See :ref:`SOG_CommandProcessorInstallation-section`.


Available Commands
------------------

The command :program:`SOG` or :program:`SOG help` produces a list of
the available :program:`SOG` commands:

.. code-block:: none

   $ SOG help

   Documented commands (type help <topic>):
   ========================================
   run

For details of the arguments and options for a command use
:program:`SOG help <command>`.
For example:

.. code-block:: none

   $ SOG help run

   usage: SOG run [--version] [--dry-run] [-o OUTFILE] [--nice NICE] [--watch]
                  EXEC INFILE

   Run SOG with INFILE. Stdout from the run is stored in OUTFILE which defaults
   to INFILE.out. The run is executed WITHOUT showing output.

   positional arguments:
     EXEC                  SOG executable to run. May include relative or
                           absolute path elements. Defaults to ./SOG.
     INFILE                infile for run

   optional arguments:
     --version             show program's version number and exit
     --dry-run             Don't do anything, just report what would be done.
     -o OUTFILE, --outfile OUTFILE
                           File to receive stdout from run. Defaults to
                           INFILE.out
     --nice NICE           Priority to use for run. Defaults to 19.
     --watch               Show OUTFILE contents on screen while SOG run is in
                           progress.

You can check what version of :program:`SOG` you have installed with:

.. code-block:: sh

   $ SOG --version


:program:`SOG run` Command
--------------------------

The :program:`SOG run` command runs the SOG code executable with a
specified infile.
If you have compiled and linked SOG in :file:`SOG-code-dev`,
and you want to run a test case using your test infile
:file:`SOG-test/infile.short`,
use:

.. code-block:: sh

   $ cd SOG-test
   $ SOG run ../SOG-code-dev/SOG infile.short

That will run SOG using :file:`infile.short` as the infile.
The screen output (stdout) will be stored in :file:`infile.short.out`.
It *will not* be displayed while the run is in progress.
The command prompt will not come back until the run is finished;
i.e. the :program:`SOG run` command will wait until the end of the run before
letting you do anything else in that shell.

:program:`SOG run` has some options that let you change how it acts:

.. code-block:: none

   $ SOG help run

   usage: SOG run [--version] [--dry-run] [-o OUTFILE] [--nice NICE] [--watch]
                  EXEC INFILE

   Run SOG with INFILE. Stdout from the run is stored in OUTFILE which defaults
   to INFILE.out. The run is executed WITHOUT showing output.

   positional arguments:
     EXEC                  SOG executable to run. May include relative or
                           absolute path elements. Defaults to ./SOG.
     INFILE                infile for run

   optional arguments:
     --version             show program's version number and exit
     --dry-run             Don't do anything, just report what would be done.
     -o OUTFILE, --outfile OUTFILE
                           File to receive stdout from run. Defaults to
                           INFILE.out
     --nice NICE           Priority to use for run. Defaults to 19.
     --watch               Show OUTFILE contents on screen while SOG run is in
                           progress.

The :option:`-o` or :option:`--outfile` option allows you to specify
the name of the file to receive the screen output (stdout) from the run.

The :option:`--watch` option causes the contents of the output file
that is receiving stdout to be displayed while the run is in progress.

The :option:`--dry-run` options tells you what the :program:`SOG`
command you have given would do, but doesn't actually do anything.
That is useful for debugging when things don't turn out like you expected,
or for checking beforehand.

The :option:`--nice` option allows you to set the priority that the
operating system will assign to your SOG run.
It defaults to 19, the lowest priority, because SOG is CPU-intensive.
Setting it to run at low priority preserves the responsiveness of your
workstation,
and allows the operating system to share resources efficiently between
one or more SOG runs and other processes.

The :option:`--version` option just returns the version of :program:`SOG`
that is installed.


Source Code and Issue Tracker
-----------------------------

Code repository: :file:`/ocean/sallen/hg_repos/SOG`

Source browser: http://bjossa.eos.ubc.ca:9000/SOG/browser/SOG (login required)

Issue tracker: http://bjossa.eos.ubc.ca:9000/SOG/report (login required)
