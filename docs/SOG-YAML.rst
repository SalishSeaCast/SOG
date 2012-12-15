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
so the recommended reference for YAML syntax is the
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


.. _AddingNewInfileLine-section:

Adding a New infile Line
------------------------

This section describes,
by example,
the code changes required to add an new line to the SOG infile;
i.e. a new quantity to be read into SOG on startup.
The example used is the addition of file names for the user profiles output
base filename,
and the user Hoffmueller data output filename.

The files that need to be changed are:

* Fortran source file:

  * :file:`SOG-code/user_output.f90`

* Legacy infiles:

  * :file:`SOG-code/infile`
  * :file:`SOG-code/infile_RI`
  * :file:`SOG-code/infile_SoG_spring_diatoms`

* YAML infile:

  * :file:`SOG-code/infile.yaml`

* SOG command processor Python modules:

  * :file:`SOGcommand/SOG_YAML_schema.py`
  * :file:`SOGcommand/SOG_infile_schema.py`

#. Edit the appropriate Fortran source file(s) to add :func:`getpar*` calls
   to read values form the infile,
   and add code to do whatever it is that you want to do with those values.

   In the example at hand,
   we'll add 2 :func:`getpars` calls to the :meth:`init_user_profiles`
   subroutine in :file:`SOG-code/user_output.f90`:

   .. code-block:: fortran

      ...
      if (noprof > 0) then
         ! Read the user profiles results file base-name
         userprofilesBase_fn = getpars("user_profile_base")
      endif

      ! Read the user Hoffmueller results file name
      userHoffmueller_fn = getpars("user Hoffmueller file")
      ...

#. Edit :file:`SOG-code/infile` to add the lines for the :func:`getpar*` calls
   to read.

   In our example,
   we add 2 lines at the end of the "Profiles output" section:

   .. code-block:: text

      ...
      ! User profiles and Hoffmueller data files
      "user_profile_base"  "profiles/SOG-user"
          "user profile file base (datetime will be added)"
      "user Hoffmueller file"  "profiles/hoff-SOG-user.dat"
          "file for user Hoffmueller results"
      ...

#. Test that the code and legacy infile changes have been made correctly
   by compiling the code and running it with the legacy infile:

   .. code-block:: sh

      $ cd SOG-code-dev
      $ make
      $ cd ../SOG-dev-test
      $ SOG run ../SOG-code-dev/SOG ../SOG-code-dev/infile --legacy-infile --watch

#. Once you are happy with the edits to the Fortran source file(s)
   and legacy infile,
   edit :file:`SOG-code/infile_RI`
   and :file:`SOG-code/infile_SoG_spring_diatoms`
   to add the lines for the :func:`getpar*` calls to read.

   In our example:

   :file:`SOG-code/infile_RI`:

   .. code-block:: text

      ...
      ! User profiles and Hoffmueller data files
      "user_profile_base"  "profiles/RI-test-user"
          "user profile file base (datetime will be added)"
      "user Hoffmueller file"  "profiles/hoff-TI-test-user.dat"
          "file for user Hoffmueller results"
      ...

   :file:`SOG-code/infile_SoG_spring_diatoms`

   .. code-block:: text

      ...
      ! User profiles and Hoffmueller data files
      "user_profile_base"
          "profiles/2002_spring_diatoms_user"
          "user profile file base (datetime will be added)"
      "user Hoffmueller file"
          "profiles/hoff_2002_spring_diatoms_user.dat"
          "file for user Hoffmueller results"
      ...

#. Edit :file:`SOG-code/infile.yaml` to add block mappings for the new input
   quantities.

   In our example,
   we add 2 blocks to the :kbd:`profile_results` section:

   .. code-block:: yaml

      ...
      user_profile_file_base:
        value: profiles/SOG-user
        variable_name: userprofilesBase_fn
        description: path/filename base for user profiles (datetime appended)
      ...
      user_hoffmueller_file:
        value: profiles/hoff-SOG-user.dat
        variable_name: userHoffmueller_fn
        description: path/filename for user Hoffmueller results
      ...

   Recall that,
   so long as the block mappings in the YAML file are nested correctly,
   their order relative to their sibling "value nodes" does not matter.

#. Edit :file:`SOGcommand/SOG_YAML_schema.py` to add nodes to the appropriate
   schema classes.

   In the example at hand,
   we add 2 nodes to the :class:`_ProfilesResults` class:

   .. code-block:: python

      ...
      user_profile_file_base = _SOG_String(
          infile_key='user_profile_base', var_name='userprofilesBase_fn',
          missing=deferred_allow_missing)
      ...
      user_hoffmueller_file = _SOG_String(
          infile_key='user Hoffmueller file', var_name='userHoffmueller_fn',
          missing=deferred_allow_missing)
      ...

   Here again,
   so long as the node declarations are in the correct schema class,
   order does not matter,
   but for code readability and maintainability,
   the nodes should be in the same order as they appear in
   :file:`SOG-code/infile.yaml`.

   What is important is that:

   * The variable name to which the node declaration is assigned is the
     same as the key for the corresponding block mapping that was added
     to :file:`SOG-code/infile.yaml`

   * The value assigned to the :obj:`infile_key` argument in the node
     declaration is the same as the first element
     (i.e. the :func:`getpar*` argument) of the corresponding
     line that was added to :file:`SOG-code/infile`

   So,
   for the :file:`SOG-code/infile` item:

   .. code-block:: text

      "user Hoffmueller file"  "profiles/hoff-SOG-user.dat"
          "file for user Hoffmueller results"

   and the :file:`SOG-code/infile.yaml` block:

   .. code-block:: yaml

      user_hoffmueller_file:
        value: profiles/hoff-SOG-user.dat
        variable_name: userHoffmueller_fn
        description: path/filename for user Hoffmueller results

   we have the node declaration:

   .. code-block:: python

      user_hoffmueller_file = _SOG_String(
          infile_key='user Hoffmueller file', var_name='userHoffmueller_fn',
          missing=deferred_allow_missing)

#. Edit :file:`SOGcommand/SOG_infile_schema.py` to:

   * Add nodes to the :class:`SOG_Infile` class:

     .. code-block:: python

        ...
        user_profile_file_base = _SOG_String(name='user_profile_base')
        user_hoffmueller_file = _SOG_String(name='user Hoffmueller file')
        ...

     The variable names to which the node declarations are assigned are the
     same as the keys for the corresponding block mappings that were added
     to :file:`SOG-code/infile.yaml`.

     The values assigned to the :obj:`name` argument in the node
     declarations are the same as the first element
     (i.e. the :func:`getpar*` argument) of the corresponding
     items that were added to :file:`SOG-code/infile`.

     While the order of the node declarations in the :class:`SOG_Infile` class,
     strictly speaking,
     doesn't matter,
     code readability and maintability is greatly improved if the nodes are
     in the same order as their corresponding lines appear in
     :file:`SOG-code/infile`.

   * Add keys to the :data:`SOG_KEYS` list:

     .. code-block:: python

        ...
        'user_profile_base', 'user Hoffmueller file',
        ...

     The keys are the same as the first element
     (i.e. the :func:`getpar*` argument)
     of the corresponding items that were added to :file:`SOG-code/infile`.

     The keys must appear in the order in which the items are arranged in
     :file:`SOG-code/infile`.
     The :data:`SOG_KEYS` list order defines the order of items in the
     generated infile,
     and the values in the list are the first element
     (i.e. the :func:`getpar*` argument) of the infile items.

#. Test that the YAML infile changes have been made correctly
   by running to code with it:

   .. code-block:: sh

      $ cd ../SOG-dev-test
      $ SOG run ../SOG-code-dev/SOG ../SOG-code-dev/infile.yaml --watch


.. _ExampleSOG-YAMLinfile-section:

Example SOG YAML infile
-----------------------

This is a snapshot of :file:`SOG-code/infile.yaml` as of |today|.

.. literalinclude:: ../SOG-code-ocean/infile.yaml
   :language: yaml
