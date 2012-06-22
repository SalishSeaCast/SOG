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

The command :program:`SOG` or :program:`SOG --help` produces a list of
the available :program:`SOG` options and sub-commands:

.. code-block:: none

   $ SOG --help
   usage: SOG [-h] [--version] {run,read_infile} ...

   optional arguments:
     -h, --help         show this help message and exit
     --version          show program's version number and exit

   sub-commands:
     {run,read_infile}
       run              Run SOG with a specified infile.
       read_infile      Print infile value for specified key.

   Use `SOG <sub-command> --help` to get detailed help about a sub-command.

For details of the arguments and options for a command use
:program:`SOG <command> --help`.
For example:

.. code-block:: none

   $ SOG run --help
   usage: SOG run [-h] [--dry-run] [-e EDITFILE] [--legacy-infile] [--nice NICE]
                  [-o OUTFILE] [--version] [--watch]
                  EXEC INFILE

   Run SOG with INFILE. Stdout from the run is stored in OUTFILE which defaults
   to INFILE.out. The run is executed WITHOUT showing output.

   positional arguments:
     EXEC                  SOG executable to run. May include relative or
                           absolute path elements. Defaults to ./SOG.
     INFILE                infile for run

   optional arguments:
     -h, --help            show this help message and exit
     --dry-run             Don't do anything, just report what would be done.
     -e EDITFILE, --editfile EDITFILE
                           YAML infile snippet to be merged into INFILE to change
                           1 or more values. This option may be repeated, if so,
                           the edits are applied in the order in which they
                           appear on the command line.
     --legacy-infile       INFILE is a legacy, Fortran-style infile.
     --nice NICE           Priority to use for run. Defaults to 19.
     -o OUTFILE, --outfile OUTFILE
                           File to receive stdout from run. Defaults to
                           ./INFILE.out; i.e. INFILE.out in the directory that
                           the run is started in.
     --version             show program's version number and exit
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

   $ SOG run --help
   usage: SOG run [-h] [--dry-run] [-e EDITFILE] [--legacy-infile] [--nice NICE]
                  [-o OUTFILE] [--version] [--watch]
                  EXEC INFILE

   Run SOG with INFILE. Stdout from the run is stored in OUTFILE which defaults
   to INFILE.out. The run is executed WITHOUT showing output.

   positional arguments:
     EXEC                  SOG executable to run. May include relative or
                           absolute path elements. Defaults to ./SOG.
     INFILE                infile for run

   optional arguments:
     -h, --help            show this help message and exit
     --dry-run             Don't do anything, just report what would be done.
     -e EDITFILE, --editfile EDITFILE
                           YAML infile snippet to be merged into INFILE to change
                           1 or more values. This option may be repeated, if so,
                           the edits are applied in the order in which they
                           appear on the command line.
     --legacy-infile       INFILE is a legacy, Fortran-style infile.
     --nice NICE           Priority to use for run. Defaults to 19.
     -o OUTFILE, --outfile OUTFILE
                           File to receive stdout from run. Defaults to
                           ./INFILE.out; i.e. INFILE.out in the directory that
                           the run is started in.
     --version             show program's version number and exit
     --watch               Show OUTFILE contents on screen while SOG run is in
                           progress.

The :option:`--dry-run` option tells you what the :program:`SOG`
command you have given would do, but doesn't actually do anything.
That is useful for debugging when things don't turn out like you expected,
or for checking beforehand.

The :option:`--editfile` option allows 1 or more YAML infile snippets to be
merged into the YAML infile for the run. See :ref:`YAML_InfileEditing-section`
for details.

The :option:`--legacy-infile` option skips the YAML processing of the infile,
allowing the run to be done with a legacy, Fortran-style infile.

The :option:`--nice` option allows you to set the priority that the
operating system will assign to your SOG run.
It defaults to 19, the lowest priority, because SOG is CPU-intensive.
Setting it to run at low priority preserves the responsiveness of your
workstation,
and allows the operating system to share resources efficiently between
one or more SOG runs and other processes.

The :option:`-o` or :option:`--outfile` option allows you to specify
the name of the file to receive the screen output (stdout) from the run.

The :option:`--version` option just returns the version of :program:`SOG`
that is installed.

The :option:`--watch` option causes the contents of the output file
that is receiving stdout to be displayed while the run is in progress.


:program:`SOG read_infile` Command
----------------------------------

The :program:`SOG read_infile` command prints the value associated with a
key in the specified YAML infile.
It is primarily for use by the SOG buildbot where it is used to get output
file paths/names from the infile.
Example:

.. code-block:: sh

   $ cd SOG-code-ocean
   $ SOG read_infile infile.yaml timeseries_results.std_physics
   timeseries/std_phys_SOG.out


.. _YAML_InfileEditing-section:

YAML Infile Editing
-------------------

The :option:`--editfile` option (:option:`-e` for short) of the
:program:`SOG run` command allows 1 or more YAML infile snippets to be
merged into the YAML infile for the run.
For example,

.. code-block:: sh

   $ cd SOG/SOG-test-RI
   $ SOG run ../SOG-code-code/SOG ../SOG-code-ocean/infile.yaml -e ../SOG-code-ocean/infileRI.yaml

would run the repository version of the Rivers Inlet model by applying
the :file:`SOG-code-ocean/infileRI.yaml` edits to the base
:file:`SOG-code-ocean/infile.yaml` infile.

The :option:`--editfile` option may be used multiple times,
if so,
the edits are applied to the infile in the order that they appear on
the command line.
The commands

.. code-block:: sh

   $ cd SOG/SOG-test-RI
   $ SOG run ../SOG-code-code/SOG ../SOG-code-ocean/infile.yaml -e ../SOG-code-ocean/infileRI.yaml -e tweaks.yaml

would run the repository version of the Rivers Inlet model with the
extra value changed defined in :file:`SOG-test-RI/tweaks.yaml`.

The intent of the YAML infile editing feature is that runs can generally
use the respository :file:`infile.yaml` as their base infile and adjust
the parameter values for the case of interest by supplying 1 or more YAML
edit files.

YAML edit files need only contain the "key paths" and values for the
parameters that are to be changed. Example:

.. code-block:: yaml

   # edits to create a SOG code infile for a 300 hr run starting at
   # cruise 04-14 station S3 CTD cast (2004-10-19 12:22 LST).
   #
   # This file is primarily used for quick tests during code
   # development and refactoring.

   end_datetime:
     value: 2004-11-01 00:22:00

   timeseries_results:
     std_physics:
       value: timeseries/std_phys_SOG-short.out
     user_physics:
       value: timeseries/user_phys_SOG-short.out
     std_biology:
       value: timeseries/std_bio_SOG-short.out
     user_biology:
       value: timeseries/user_bio_SOG-short.out
     std_chemistry:
       value: timeseries/std_chem_SOG-short.out

   profiles_results:
     profile_file_base:
       value: profiles/SOG-short
     halocline_file:
       value: profiles/halo-SOG-short.out
     hoffmueller_file:
       value: profiles/hoff-SOG-short.dat


Source Code and Issue Tracker
-----------------------------

Code repository: :file:`/ocean/sallen/hg_repos/SOG`

Source browser: http://bjossa.eos.ubc.ca:9000/SOG/browser/SOG (login required)

Issue tracker: http://bjossa.eos.ubc.ca:9000/SOG/report (login required)
