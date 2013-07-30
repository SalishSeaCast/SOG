# -*- coding: utf-8 -*-
"""SOG command processor API.

API for SOG command processer.

Intended for use by software that runs SOG (e.g. SoG-bloomcast) so that
SOG commands can be used dirctly,
rather than by way of a subprocess.

:Author: Doug Latornell <djl@douglatornell.ca>
:License: Apache License, Version 2.0


Copyright 2010-2013 Doug Latornell and The University of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from subprocess import Popen
from .command_processor import prepare_run_cmd
from .infile_processor import read_infile


class Args(object):
    """Container for SOG command arguments.
    """
    def __init__(self, SOG_exec, infile, editfiles, outfile, legacy_infile,
                 dry_run, nice):
        self.SOG_exec = SOG_exec
        self.infile = infile
        self.editfile = editfiles
        self.outfile = outfile
        self.legacy_infile = legacy_infile
        self.dry_run = dry_run
        self.nice = nice


def run(SOG_exec,
        infile,
        editfiles=[],
        outfile='',
        legacy_infile=False,
        dry_run=False,
        nice=19):
    """Launch SOG with the specified args,
    and return the run's subprocess instance.

    :arg SOG_exec: Path/filename of the SOG executable.
    :type SOG_exec: str

    :arg infile: Path/filename of the infile to use.
    :type infile: str

    :arg editfiles: Path/filename of YAML infile(s) to apply to the infile
                    as edits.
    :type editfiles: list

    :arg outfile: Path/filename of the file to receive stdout from the run.
                  Defaults to the path/filename of the infile with :kbd:`.out`
                  appended.
    :type outfile: str

    :arg legacy_infile: infile is a legacy, Fortran-style infile.
                        Defaults to :kbd:`False`.
    :type legacy_infile: boolean

    :arg dry_run: Don't do anything.
                  Defaults to :kbd:`False`.
    :type dry_run: boolean

    :arg nice: Priority to use for the run.
               Defaults to :kbd:`19`.
    :type nice: int

    :returns: Process object for the launched :program:`SOG` run.
    :rtype: :class:`subprocess.Popen` instance
    """
    args = Args(SOG_exec, infile, editfiles, outfile, legacy_infile, dry_run,
                nice)
    cmd = prepare_run_cmd(args)
    proc = Popen(cmd, shell=True)
    return proc
