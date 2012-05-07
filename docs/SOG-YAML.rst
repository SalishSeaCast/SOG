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


SOG YAML Grammar
----------------

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

Block mappings can be nested:

.. code-block:: yaml

   grid:
     model_depth:
       value: 40
       units: m
       variable name: grid%D
       description: depth of modelled domain

You can think of this as a tree where :kbd:`grid` is the parent node,
and :kbd:`model_depth` is a child node.
Indentation defines the nesting levels of the tree.
By convention,
each level is indented by 2 spaces.

In the context of SOG,
only "value nodes" (the deepest nodes in any tree branch) can have
:kbd:`value`, :kbd:`units`, :kbd:`variable name`, and :kbd:`description`
as children:

.. code-block:: yaml

   grid:
     model_depth:
       value: 40
       units: m
       variable name: grid%D
       description: depth of modelled domain
     grid_size:
       value: 80
       variable_name: grid%M
       description: number of grid points

Notice that :kbd:`units` is optional in values nodes.
It may be omitted if the value has no units.

The order of elements in a tree and the in value node block mappings
doesn't matter:

.. code-block:: yaml

   grid:
     grid_size:
       value: 80
       description: number of grid points
       variable_name: grid%M
     model_depth:
       variable name: grid%D
       description: depth of modelled domain
       value: 40
       units: m

is equivalent to the previous YAML snippet.
The YAML infile itself is an implicit,
top-level node,
so,
the high level blocks like :kbd:`grid` and :kbd:`location`
(see :ref:`ExampleSOG-YAMLinfile-section`)
can be arranged in whatever order is logical for a given infile.

Lines starting with the :kbd:`#` character are treated as comments in YAML.
Blank lines are ignored,
so they may be used to provide semantic separations to improve the readability
of the infile.

In the SOG context
The :kbd:`value` element of a value node can be one of several types:

* A number,
  expressed as an integer,
  float,
  or in scientific notation with :kbd:`e` as the exponent separator;
  e.g.
  :kbd:`value: 40`,
  :kbd:`value: 49.1253`,
  :kbd:`value: 30e3`,
  :kbd:`value: 11.67e-10`.
  The SOG command processor takes care of transforming numbers to the format
  expected by the SOG infile processor,
  so,
  trailing decimals and zeros
  (:kbd:`40.` or :kbd:`40.0`),
  and explicit indication of double precision
  (:kbd:`49.1253d0`)
  are not required.

* A string such as a file path and name;
  e.g.
  :kbd:`value: ../SOG-initial/chem/Chem-SOGS-2010-73.sog`.
  Only use quotes in strings if the are part of the string.
  They are not required as delimiters.

* A date/time in the format :kbd:`yyyy-mm-dd hh:mm:ss`;
  e.g.
  :kbd:`value: 2005-10-11 00:22:00`

* A Boolean value;
  :kbd:`value: True` or :kbd:`value: False`.

* A list of 1 or more numbers,
  enclosed in square brackets,
  and separated by commas;
  e.g.
  :kbd:`value: [0.33, 0.33, 0.33]`.
  The expression rules above for single numbers apply to each number in the
  list,
  and expression formats may be mixed within a list;
  e.g.
  :kbd:`value: [42, 0.33, 1.2e-4]`.

The :kbd:`value` element of a value node (unsurprisingly) specifies the value
that will be read by SOG.
The :kbd:`description` element
and the :kbd:`units` element (if present)
are combined to produce the descriptive string that SOG writes to stdout
as it read the infile.
So,
the YAML fragment:

.. code-block:: yaml

   grid:
     model_depth:
       value: 40
       units: m
       variable name: grid%D
       description: depth of modelled domain

is transformed by the SOG command processor into the SOG infile line::

  "maxdepth"  40.d0  "depth of modelled domain [m]"

The :kbd:`variable name` element of a value node is purely informational,
that is,
it is metadata provided in the infile to document the SOG variable name
in which the value is stored.


.. _ExampleSOG-YAMLinfile-section:

Example SOG YAML infile
-----------------------

This is a snapshot of :file:`SOG-code/infile.yaml` as of |today|.

.. literalinclude:: ../SOG-code-ocean/infile.yaml
   :language: yaml
