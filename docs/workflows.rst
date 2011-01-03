.. _workflows-section:

Workflows for Running & Developing SOG
======================================

Set Up Your Mercurial Configuration
-----------------------------------

Before you use Mercurial_ to track changes that you make the the SOG
code, documentation, or intialization and forcing data you need to do
some intial setup of your Mercurial configuration. 

.. _Mercurial: http://mercurial.selenic.com/

.. note::

   It is *essential* that these configurations steps be completed
   before you push changes to the central, shared repositories so that
   the email notification and buildbot hooks will work properly.

These instructions assume that you use :command:`emacs` as your
editor.

Set the :envvar:`EDITOR` and :envvar:`VISUAL` environment variables to
:command:`emacs` to ensure that Mercurial will take you into
:command:`emacs`, not :command:`vi` for creations of commit messages,
etc.  If you use :command:`bash` as your shell use:

.. code-block:: sh

   $ export EDITOR=emacs 
   $ export VISUAL=emacs

and add the same commands to your :file:`~/.bash_profile` file so that
the environment variables are set whenever you log in. If you use
:command:`csh` as your shell use:

.. code-block:: csh

   $ setenv EDITOR emacs 
   $ setenv VISUAL emacs

and add the same commands to your :file:`~/.cshrc` file so that
the environment variables are set whenever you log in.

If you have not already done so, you should create a :file:`.hgrc`
file in your home directory containing:

.. code-block:: cfg

   [ui]
   username = Your Name <your_userid@eos.ubc.ca>
   ignore = ~/.hgignore
   merge = emacs-merge.sh

Those lines:

* Set how your changes will be attributed to you in commit messages,
  etc.
* Tell Mercurial to find your list of globally ignored files in
  :file:`~/.hgignore` (see below)
* Tell Mercurial to use the :file:`emacs-merge.sh` shell script (see
  below) to hook into :command:`emacs` as your merge resolution tool

Create a :file:`.hgignore` file in your home directory containing:

.. code-block:: cfg

   syntax: glob
   *~

   syntax: regexp
   (.*/)?\#[^/]*\#$

Those lines will cause Mercurial to ignore :command:`emacs` temporary
and backup files in all of your Mercurial repositories (not just the
SOG ones).

If you don't already have one, create a :file:`bin` directory in your
home directory:

.. code-block:: sh

   $ mkdir ~/bin

Add :file:`~/bin` to your path. If you use :command:`bash` as your
shell use:

.. code-block:: sh

   $ export PATH=$PATH:$HOME/bin

and add the same command to your :file:`~/.bash_profile` file so that
:file:`~/bin` is added to your path whenever you log in. If you use
:command:`csh` as your shell use:

.. code-block:: csh

   $ setenv PATH ${PATH}:${HOME}/bin

and add the same command to your :file:`~/.cshrc` file so that
:file:`~/bin` is added to your path whenever you log in.

Create an :file:`emacs-merge.sh` file in your :file:`~/bin` directory
containing:

.. code-block:: sh

   #!/bin/sh

   # Enable use of emacs ediff mode as merger program for mercurial

   # Hook to mercurial in ~/.hgrc is:
   #  [ui]
   #  merge = emacs-merge.sh

   # Copied from http://www.selenic.com/mercurial/wiki/index.cgi/MergingWithEmacs

   # bail out quickly on failure
   set -e

   LOCAL="$1"
   BASE="$2"
   OTHER="$3"

   BACKUP="$LOCAL.orig"

   Restore ()
   {
       cp "$BACKUP" "$LOCAL" 
   }

   ExitOK ()
   {
       exit $?
   }

   # Back up our file
   cp "$LOCAL" "$BACKUP"

   # Attempt to do a non-interactive merge
   if which merge > /dev/null 2>&1 ; then
       if merge "$LOCAL" "$BASE" "$OTHER" 2> /dev/null; then
       # success!
       ExitOK 
       fi
       Restore
   elif which diff3 > /dev/null 2>&1 ; then
       if diff3 -m "$BACKUP" "$BASE" "$OTHER" > "$LOCAL" ; then
       # success
       ExitOK
       fi
       Restore
   fi

   if emacs -q --no-site-file --eval "(ediff-merge-with-ancestor \"$BACKUP\" \"$OTHER\" \"$BASE\" nil \"$LOCAL\")" 
   then       
       ExitOK
   fi

   echo "emacs-merge: failed to merge files"
   exit 1

Add :file:`/ocean/dlatorne/.virtualenvs/SOG-hg-buildbot` to your
:envvar:`PYTHONPATH` environment variable, and make the Mercurial
instance installed there your default. This ensures that the email
notification and buildbot hooks will work properly when you push
changes to any of the SOG respositories.  If you use :command:`bash`
as your shell use:

.. code-block:: sh

   $ export PYTHONPATH=$PYTHONPATH:/ocean/dlatorne/.virtualenvs/SOG-hg-buildbot/lib/python2.6/site-packages
   $ alias hg="/ocean/dlatorne/.virtualenvs/SOG-hg-buildbot/bin/hg"

and add the same 1st command to your :file:`~/.bash_profile`, and the
end to your :file:`~/.bashrc` file so that they take effect whenever
you log in. If you use :command:`csh` as your shell use:

.. code-block:: csh

   $ setenv PYTHONPATH ${PYTHONPATH}:/ocean/dlatorne/.virtualenvs/SOG-hg-buildbot/lib/python2.6/site-packages
   $ alias hg "/ocean/dlatorne/.virtualenvs/SOG-hg-buildbot/bin/hg"

and add the same commands to your :file:`~/.cshrc` file so that they
take effect whenever you log in.


..
  Local variables:
  mode: rst
  End:
