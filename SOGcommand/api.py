# -*- coding: utf-8 -*-
"""SOG command processor API.

API for SOG command processer.

Intended for use by software that runs SOG (e.g. SoG-bloomcast) so that
SOG commands can be used dirctly,
rather than by way of a subprocess.

:Author: Doug Latornell <djl@douglatornell.ca>
"""
from subprocess import Popen
from .command_processor import prepare_run_cmd


class Args(object):
    """Container for SOG command arguments.
    """
    def __init__(self, SOG_exec, infile, outfile, legacy_infile, dry_run,
                 nice):
        self.SOG_exec = SOG_exec
        self.infile = infile
        self.outfile = outfile
        self.legacy_infile = legacy_infile
        self.dry_run = dry_run
        self.nice = nice


def run(SOG_exec, infile, outfile='', legacy_infile=False, dry_run=False,
        nice=19):
    """Launch SOG with the specified args,
    and return the run's subprocess instance.

    :arg SOG_exec: Path/filename of the SOG executable.
    :type SOG_exec: str

    :arg infile: Path/filename of the infile to use.
    :type infile: str

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
    args = Args(SOG_exec, infile, outfile, legacy_infile, dry_run, nice)
    cmd = prepare_run_cmd(args)
    proc = Popen(cmd, shell=True)
    return proc
