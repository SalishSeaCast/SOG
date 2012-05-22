"""SOG command processor.

A command processer wrapper around various operations associated with
the SOG bio-physical model of deep estuaries.

:Author: Doug Latornell <djl@douglatornell.ca>
"""
from argparse import ArgumentParser
from subprocess import Popen
import sys
from textwrap import TextWrapper
from time import sleep
from __version__ import version


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
    return parser


def add_version_arg(parser):
    parser.add_argument('--version', action='version', version=version)


def add_run_subparser(subparsers):
    """Add a sub-parser for the `SOG run` command.
    """
    parser = subparsers.add_parser(
        'run', help='Run SOG with a specified infile.')
    add_version_arg(parser)
    parser.add_argument(
        '--dry-run', action='store_true',
        help="Don't do anything, just report what would be done.")
    parser.description = '''
        Run SOG with INFILE. Stdout from the run is stored in
        OUTFILE which defaults to INFILE.out. The run is executed
        WITHOUT showing output.
        '''
    parser.add_argument(
        'SOG_exec', metavar='EXEC', default='./SOG',
        help='''
             SOG executable to run. May include relative or absolute
             path elements. Defaults to %(default)s.
             ''')
    parser.add_argument('infile', metavar='INFILE', help='infile for run')
    parser.add_argument(
        '-o', '--outfile', metavar='OUTFILE',
        help='File to receive stdout from run. Defaults to INFILE.out')
    parser.add_argument(
        '--nice', default=19,
        help='Priority to use for run. Defaults to %(default)s.')
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
    if not args.outfile:
        args.outfile = args.infile + '.out'
    cmd = (
        'nice -n {0.nice} {0.SOG_exec} < {0.infile} > {0.outfile}'
        .format(args))
    if args.dry_run:
        run_dry_run(cmd, args)
    else:
        proc = Popen(cmd, shell=True)
        if args.watch:
            for line in watch_outfile(proc, args.outfile):
                print line,
        else:
            proc.wait()


def run_dry_run(cmd, args):
    """Dry-run handler for `SOG run` command.
    """
    wrapper = TextWrapper()
    print wrapper.fill('Command that would have been used to run SOG:')
    print '  {0}'.format(cmd)
    if args.watch:
        print wrapper.fill(
            'Contents of {0} would have been shown on screen while '
            'SOG run was in progress.'.format(args.outfile))


def watch_outfile(proc, outfile_name):
    """Generator that yields lines from SOG run outfile while run is
    in progress, and continues yielding the lines that are flushed
    when the run finishes.
    """
    with open(outfile_name) as outfile:
        while proc.poll() is None:
            # Echo lines flushed to outfile while SOG is running
            line = outfile.readline()
            if not line:
                sleep(0.1)
                continue
            yield line
        else:
            # Echo lines flushed to outfile when SOG run finishes
            for line in outfile:
                yield line
