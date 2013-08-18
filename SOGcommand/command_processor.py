# -*- coding: utf-8 -*-
"""SOG command processor.

A command processer wrapper around various operations associated with
the SOG bio-physical model of deep estuaries.

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
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from argparse import ArgumentParser
from subprocess import Popen
import sys
from .__version__ import (
    version,
    release,
)
from .infile_processor import read_infile
from .run_processor import (
    prepare_run_cmd,
    run_dry_run,
    watch_outfile,
)


def run():
    """Entry point to start the command processor.
    """
    cmd_processor = build_parser()
    if len(sys.argv) == 1:
        cmd_processor.print_help()
    else:
        args = cmd_processor.parse_args()
        args.func(args)


def build_parser():
    parser = ArgumentParser(
        epilog='''
            Use `%(prog)s <sub-command> --help` to get detailed
            help about a sub-command.''')
    add_version_arg(parser)
    subparsers = parser.add_subparsers(title='sub-commands')
    add_run_subparser(subparsers)
    add_read_infile_subparser(subparsers)
    return parser


def add_version_arg(parser):
    parser.add_argument(
        '--version', action='version', version=version + release)


def add_run_subparser(subparsers):
    """Add a sub-parser for the `SOG run` command.
    """
    parser = subparsers.add_parser(
        'run', help='Run SOG with a specified infile.',
        description='''
            Run SOG with INFILE. Stdout from the run is stored in
            OUTFILE which defaults to INFILE.out.
            The run is executed WITHOUT showing output.
            ''')
    parser.add_argument(
        'SOG_exec', metavar='EXEC', default='./SOG',
        help='''
             SOG executable to run. May include relative or absolute
             path elements. Defaults to %(default)s.
             ''')
    parser.add_argument('infile', metavar='INFILE', help='infile for run')
    parser.add_argument(
        '--dry-run', action='store_true',
        help="Don't do anything, just report what would be done.")
    parser.add_argument(
        '-e', '--editfile', metavar='EDITFILE', action='append', default=[],
        help='''
            YAML infile snippet to be merged into INFILE to change
            1 or more values.
            This option may be repeated,
            if so,
            the edits are applied in the order in which they appear
            on the command line.
            ''')
    parser.add_argument(
        '--legacy-infile', action='store_true',
        help='INFILE is a legacy, Fortran-style infile.')
    parser.add_argument(
        '--nice', default=19,
        help='Priority to use for run. Defaults to %(default)s.')
    parser.add_argument(
        '-o', '--outfile', metavar='OUTFILE',
        help='''
            File to receive stdout from run. Defaults to ./INFILE.out;
            i.e. INFILE.out in the directory that the run is started in.
            ''')
    add_version_arg(parser)
    parser.add_argument(
        '--watch', action='store_true',
        help='''
             Show OUTFILE contents on screen while SOG run is in
             progress.
             ''')
    parser.set_defaults(func=do_run)


def do_run(args):
    """Execute the `SOG run` command with the specified options.
    """
    cmd = prepare_run_cmd(args)
    if args.dry_run:
        run_dry_run(cmd, args)
        returncode = 0
    else:
        proc = Popen(cmd, shell=True)
        if args.watch:
            for line in watch_outfile(proc, args.outfile):
                print(line, end='')
            returncode = proc.poll()
        else:
            returncode = proc.wait()
    sys.exit(returncode)


def add_read_infile_subparser(subparsers):
    """Add a sub-parser for the `SOG read_infile` command.
    """
    parser = subparsers.add_parser(
        'read_infile', help='Print infile value for specified key.')
    parser.add_argument('infile', help='infile for run')
    parser.add_argument(
        '-e', '--editfile', metavar='EDITFILE', action='append', default=[],
        help='''
            YAML infile snippet to be merged into INFILE to change
            1 or more values.
            This option may be repeated,
            if so,
            the edits are applied in the order in which they appear
            on the command line.
            ''')
    parser.add_argument(
        'key',
        help='''
             Key to print infile value for;
             e.g. timeseries_results.std_physics.
             ''')
    add_version_arg(parser)
    parser.set_defaults(func=do_read_infile)


def do_read_infile(args):
    """Print the infile value for the specified key.
    """
    value = read_infile(args.infile, args.editfile, args.key)
    print(value)
    sys.exit(0)
