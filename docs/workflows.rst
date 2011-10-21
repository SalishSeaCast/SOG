.. _workflows-section:

Workflows for Running & Developing SOG
======================================

Set Up Your Mercurial Configuration
-----------------------------------

Before you use Mercurial_ to track changes that you make the the SOG
code, documentation, or initialization and forcing data you need to do
some initial setup of your Mercurial configuration.

.. _Mercurial: http://mercurial.selenic.com/

.. note::

   It is *essential* that these configuration steps be completed
   before you push changes to the central, shared repositories so that
   the email notification and buildbot hooks will work properly.

These instructions assume that you use :command:`emacs` as your
editor.

#. Set the :envvar:`EDITOR` and :envvar:`VISUAL` environment variables
   to :command:`emacs` to ensure that Mercurial will take you into
   :command:`emacs`, not :command:`vi` for creation of commit
   messages, etc.  If you use :command:`bash` as your shell use:

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

#. If you have not already done so, you should create a :file:`.hgrc`
   file in your home directory containing:

   .. code-block:: cfg

      [ui]
      username = Your Name <your_userid@eos.ubc.ca>
      ignore = ~/.hgignore
      merge = emacs-merge.sh

   These lines:

   * Set how your changes will be attributed to you in commit messages,
     etc.
   * Tell Mercurial to find your list of globally ignored files in
     :file:`~/.hgignore` (see below)
   * Tell Mercurial to use the :file:`emacs-merge.sh` shell script (see
     below) to hook into :command:`emacs` as your merge resolution tool

#. Create a :file:`.hgignore` file in your home directory containing:

   .. code-block:: cfg

      syntax: glob
      *~

      syntax: regexp
      (.*/)?\#[^/]*\#$

   These lines will cause Mercurial to ignore :command:`emacs` temporary
   and backup files in all of your Mercurial repositories (not just the
   SOG ones).

#. If you don't already have one, create a :file:`bin` directory in
   your home directory:

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

#. Create an :file:`emacs-merge.sh` file in your :file:`~/bin`
   directory containing:

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

   Make :file:`emacs-merge.sh` executable with:

   .. code-block:: sh

      $ chmod u+x ~/bin/emacs-merge.sh

#. Add :file:`/ocean/dlatorne/.virtualenvs/SOG-hg-buildbot` to your
   :envvar:`PYTHONPATH` environment variable, and make the Mercurial
   instance installed there your default. This ensures that the email
   notification and buildbot hooks will work properly when you push
   changes to any of the SOG repositories.  If you use :command:`bash`
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


Using Mercurial
---------------

If you're not familiar with Mercurial you should read at least
`Chapter 2`_ of the `Mercurial - The Definitive Guide`_ book *right
now*.

.. _Chapter 2: http://hgbook.red-bean.com/read/a-tour-of-mercurial-the-basics.html
.. _Mercurial - The Definitive Guide: http://hgbook.red-bean.com/


.. _SharedRepos-section:

Shared Repositories in the SOG Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Your SOG working environment includes clones of 4 shared Mercurial
repositories from the EOS ocean file server:

* :file:`SOG`
    The top level repository that contains the Makefile for managing
    your SOG environment, the source files for this documentation, and
    the other 3 repository clones as sub-directories.
* :file:`SOG-code`
    The SOG source code which is cloned to :file:`SOG-code-ocean` in
    tour environment.
* :file:`SOG-initial`
    The SOG initial conditions data repository that contains CTD and
    nutrient data files used to initialize SOG runs.
* :file:`SOG-forcing`
    The SOG forcing data repository that contains meteorological,
    river flow, wind, and bottom conditions data files used provide
    forcing terms at each time-step in SOG runs.


.. _SubscribingToEmailNotifications-section:

Subscribing to Email Notifications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To keep tabs on changes that other users are making to
:ref:`SharedRepos-section` you should subscribe to email notifications
for each repository. You can ask Doug or Susan to do that for you, or
you can do it yourself with the following commands:

.. code-block:: sh

   $ cd SOG
   $ hg clone /ocean/sallen/hg_repos/notify
   $ cd notify
   $ emacs notify.conf

Add your email address to the comma separated list of addresses for
each repository in the :kbd:`[reposubs]` section of
:file:`notify.conf` and save the file. Commit the change in your local
repository and push it to ocean:

.. code-block:: sh

   $ hg commit
   $ hg push

A Mercurial hook in the :file:`/ocean/sallen/hg_repos/notify`
repository will update the :file:`notify.conf` file there and you
should start to receive an changeset notification messages.

:file:`notify.conf` also contains a subscription list for changes to
the :ref:`SOGbuildbot-section` code and docs that you can join if you
are interested.

Once subscribed you will receive an message from
:kbd:`hg_repos@eos.ubc.ca` for each changeset that you or any other
user pushes to the shared repositories on ocean. The subject of the
message will indicate that it is a Mercurial update message, tell you
which repositories it applies to, and give you 50 characters (or so)
of the commit message; example::

  HG update: SOG-code: Delete unused new_year.f90 source code file.

The message contains details of the changeset and a link to the
changeset in the :ref:`SOGtrac-section`.


Keeping Your Repository Clones Up To Date
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Mercurial commands that you need to help you keep your repository
clones up to date are:

* :command:`hg incoming`
    Gives you a list of changesets in a remote repository that have
    not been pulled into your local repository
* :command:`hg pull`
    Pull changes from a remote repository to your local one
* :command:`hg update`
    Update the files in your local repository with all of the changes
    you have pulled in
* :command:`hg merge`
    Merge the changesets pull into your local repository with changes
    that you have made since you last updated from the remote
    repository
* :command:`hg status`
    Show that status of files in your local repository

You can shorten Mercurial commands to the fewest letters that make
them unique; e.g. :command:`hg inco`, :command:`hg up`, :command:`hg
stat`.

You may not need to use :command:`hg incoming` if you know from having
received changeset notification messages that there have been changes
to the remote repository. On the other hand, you may want to use it
just to check.

To update your local clone of the :file:`SOG-code` repository with
changes that other users have pushed to the shared repository on
ocean, recall that :file:`SOG-code` is cloned to
:file:`SOG-code-ocean` in your local SOG environment and use the
commands:

.. code-block:: sh

   $ cd SOG-code-ocean
   $ hg incoming
   ... list of changesets that will be pulled ...
   $ hg pull
   ... status of pull request ...
   $ hg update
   ... status of update request ...

From the :command:`hg pull` command onward Mercurial will tell you
what you need to do next.

:command:`hg incoming` and :command:`hg pull` look at the remote
repository that your local repository was cloned from by default. You
can check where that repository is with the :command:`hg paths`
command. You can operate against a different remote repository by
giving its path explicitly; e.g.:

.. code-block:: sh

   $ hg incoming /ocean/dlatornell/SoG/SOG/SOG-code-dev

If there are changes in your local repository that you have made, or
pulled from another repository since you last updated from the remote
repository Mercurial will tell you that you need to do a merge. It
will refuse to do the merge if you have any uncommitted changes in
your repository, so clean up before you pull. Mercurial is pretty good
at merging files automatically, but sometimes it needs help and it
will open :command:`emacs` in :kbd:`ediff` mode for you to manually
merge the changes in a file where it find unresolvable conflicts. Once
a merge is finished, Mercurial will remind you to commit the result of
the merge. Use a commit message something like::

  Merge changes from ocean repository.

For more information about merging see `Chapter 3`_ of the
`Mercurial - The Definitive Guide`_ book.

.. _Chapter 3: http://hgbook.red-bean.com/read/a-tour-of-mercurial-merging-work.html

..
  Local variables:
  mode: rst
  End:
