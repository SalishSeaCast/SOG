"""SOG command processor.

A command processer wrapper around various operations associated with
the SOG bio-physical model of deep estuaries.

:Author: Doug Latornell <djl@douglatornell.ca>
"""
from argparse import ArgumentParser
from cmd import Cmd
import os
from subprocess import Popen
import sys
from textwrap import TextWrapper
from time import sleep
from __version__ import version


class SOGcommand(Cmd):

    def __init__(self):
        Cmd.__init__(self)
        self.wrapper = TextWrapper()

    def emptyline(self):
        self.do_help(None)

    def default(self, line):
        if line.startswith('--version'):
            print version
        else:
            print '*** Unknown command: {0[0]}'.format(line.split())
            self.do_help(None)

    def fill_print(self, text):
        print self.wrapper.fill(text)

    def do_run(self, line):
        parser = self.run_parser()
        args = parser.parse_args(line.split())
        if not args.outfile:
            args.outfile = args.infile + '.out'
        cmd = (
            'nice -n {0.nice} {0.SOG_exec} < {0.infile} > {0.outfile}'
            .format(args))
        if args.dry_run:
            self.run_dry_run(cmd, args)
        else:
            proc = Popen(cmd, shell=True)
            if args.watch:
                for line in self.watch_outfile(proc, args.outfile):
                    print line,
            else:
                proc.wait()

    def run_dry_run(self, cmd, args):
        self.fill_print('Command that would have been used to run SOG:')
        print '  {0}'.format(cmd)
        if args.watch:
            self.fill_print(
                'Contents of {0} would have been shown on screen while '
                'SOG run was in progress.'.format(args.outfile))

    def watch_outfile(self, proc, outfile_name):
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

    def help_run(self):
        parser = self.run_parser()
        parser.print_help()

    def run_parser(self):
        """Build argument parser for run command.
        """
        parser = ArgumentParser(add_help=False)
        parser.add_argument('--version', action='version', version=version)
        parser.add_argument(
            '--dry-run', action='store_true',
            help="Don't do anything, just report what would be done.")
        parser.prog = '{0} run'.format(os.path.basename(sys.argv[0]))
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
        return parser


def run():
    """Entry point to start the command processor.
    """
    cmd_processor = SOGcommand()
    cmd_processor.onecmd(' '.join(sys.argv[1:]))

if __name__ == '__main__':
    run()
