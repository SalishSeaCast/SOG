.. _SOG-YAML-section:

Using YAML for SOG infiles
==========================

One of the key features of the :ref:`SOG_CommandProcessor-section`
is the use of YAML_ syntax for SOG infiles.
The command processor transforms infiles written in YAML to the
key-value-description format that the SOG Fortran code reads.

.. _YAML: http://yaml.org/

YAML is used because it is easily read by both humans and software.
Some of the benefits for humans of using YAML infiles are:

* Richer metadata in the infile

* Relaxes (to a large extent, but not completely) the order of the
  contents of the infile

Some of the software benefits of using YAML
(that should turn out to be human benefits too) are:

* Facilitate use of a base infile with one or more infile snippets that
  are applied to it as edits

* Validation of infile contents independent of SOG Fortran code

* Easier programmatic manipulation of infiles for things like genetic
  algorithm optimization of model parameters

The SOG command processor uses the PyYAML_ library to process YAML
infiles in Python,
so the recommended reference for YAML syntax it the
`PyYAML documentation`_

.. _PyYAML: http://pyyaml.org/
.. _PyYAML documentation: http://pyyaml.org/wiki/PyYAMLDocumentation#YAMLsyntax

If your editor doesn't already include a YAML syntax highlighter,
you probably want to find one on the web.
For emacs,
there's `yaml-mode.el`_

.. _yaml-mode.el: http://emacswiki.org/emacs/YamlMode


SOG YAML Semantics
------------------

This is a brief summary of how YAML is used to write SOG infiles.
It is neither a detailed description of YAML syntax
(see `PyYAML documentation`_ for that),
or an exhaustive list of the infile parameters and their purposes
(see the :ref:`ExampleSOG-YAMLinfile-section`
and the `SOG Fortran code`_ for that).

.. _SOG Fortran code: http://bjossa.eos.ubc.ca:9000/SOG/browser/SOG-code

The basic building block of a SOG YAML infile is a block mapping,
one or more lines of key-value pairs with ": " (colon and space)
as a separator:

.. code-block:: yaml

   value: 40
   units: m
   variable name: grid%D
   description: depth of modelled domain



.. _ExampleSOG-YAMLinfile-section:

Example SOG YAML infile
-----------------------

