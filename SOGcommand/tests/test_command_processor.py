"""Unit tests for SOG command processor
"""
from mock import Mock
from mock import patch
from StringIO import StringIO
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA
from .. import command_processor


class TestEntryPoint(unittest.TestCase):
    """Unit tests for the SOG command processor entry point function.
    """
    def _call_entry_point(self):
        from ..command_processor import run
        run()

    @patch.object(command_processor, 'build_parser', return_value=Mock())
    def test_entry_w_1_arg_print_help(self, mock_build_parser):
        """run w/ 1 cmd line arg calls parser print_help
        """
        with patch.object(command_processor, 'sys') as mock_sys:
            mock_sys.argv = ['SOG']
            self._call_entry_point()
        mock_build_parser.print_help.assert_called_once()

    @patch.object(command_processor, 'build_parser', return_value=Mock())
    def test_entry_w_2_args_parse_args(self, mock_build_parser):
        """run w/ 2 cmd line args calls parser parse_args
        """
        with patch.object(command_processor, 'sys') as mock_sys:
            mock_sys.argv = 'SOG foo'.split()
            self._call_entry_point()
        mock_build_parser.parse_args.assert_called_once()


class TestParser(unittest.TestCase):
    """Unit tests for the SOG command processor parser.
    """
    def test_build_parser(self):
        from argparse import ArgumentParser
        parser = command_processor.build_parser()
        self.assertIsInstance(parser, ArgumentParser)


class TestRunCommand(unittest.TestCase):
    """Unit tests for the SOG command processor run command.
    """
    @patch.object(command_processor, 'Popen')
    def test_do_run_default_args(self, mock_Popen):
        """do_run spawns expected command for default args
        """
        args = Mock(
            SOG_exec='./SOG', infile='infile', outfile=None,
            nice=19, dry_run=False, watch=False, legacy_infile=False)
        with patch.object(command_processor, 'create_infile',
                          return_value='/tmp/foo.infile'):
            with self.assertRaises(SystemExit):
                command_processor.do_run(args)
        mock_Popen.assert_called_once_with(
            'nice -n 19 ./SOG < /tmp/foo.infile > ./infile.out', shell=True)

    @patch.object(command_processor, 'Popen')
    def test_do_run_legacy_infile(self, mock_Popen):
        """do_run spawns expected command w/ legacy_infile==True
        """
        args = Mock(
            SOG_exec='./SOG', infile='infile', outfile=None,
            nice=19, dry_run=False, watch=False, legacy_infile=True)
        with self.assertRaises(SystemExit):
            command_processor.do_run(args)
        mock_Popen.assert_called_once_with(
            'nice -n 19 ./SOG < infile > ./infile.out', shell=True)

    @patch.object(command_processor, 'Popen')
    @patch.object(command_processor, 'run_dry_run')
    def test_do_run_dry_run(self, mock_run_dry_run, mock_Popen):
        """do_run calls run_dry_run when --dry-run option is used
        """
        args = Mock(
            SOG_exec='./SOG', infile='infile', outfile=None,
            nice=19, dry_run=True, watch=False, legacy_infile=False)
        with self.assertRaises(SystemExit):
            command_processor.do_run(args)
        mock_run_dry_run.assert_called_once()

    @patch.object(command_processor, 'Popen', return_value=Mock(name='proc'))
    def test_do_run_default_waits_for_end_of_run(self, mock_Popen):
        """do_run waits for end of run by default
        """
        args = Mock(
            SOG_exec='./SOG', infile='infile', outfile=None,
            nice=19, dry_run=False, watch=False, legacy_infile=False)
        with patch.object(command_processor, 'create_infile',
                          return_value='/tmp/foo.infile'):
            with self.assertRaises(SystemExit):
                command_processor.do_run(args)
        mock_Popen().wait.assert_called_once()

    @patch.object(command_processor, 'Popen')
    def test_do_run_outfile_relative_path(self, mock_Popen):
        """do_run spawns expected command when outfile arg is relative path
        """
        args = Mock(
            SOG_exec='./SOG', infile='infile', outfile='../foo/bar',
            nice=19, dry_run=False, watch=False, legacy_infile=False)
        with patch.object(command_processor, 'create_infile',
                          return_value='/tmp/foo.infile'):
            with self.assertRaises(SystemExit):
                command_processor.do_run(args)
        mock_Popen.assert_called_once_with(
            'nice -n 19 ./SOG < /tmp/foo.infile > ../foo/bar', shell=True)

    @patch.object(command_processor, 'Popen')
    def test_do_run_outfile_absolute_path(self, mock_Popen):
        """do_run spawns expected command when outfile arg is absolute path
        """
        args = Mock(
            SOG_exec='./SOG', infile='infile', outfile='/foo/bar',
            nice=19, dry_run=False, watch=False, legacy_infile=False)
        with patch.object(command_processor, 'create_infile',
                          return_value='/tmp/foo.infile'):
            with self.assertRaises(SystemExit):
                command_processor.do_run(args)
        mock_Popen.assert_called_once_with(
            'nice -n 19 ./SOG < /tmp/foo.infile > /foo/bar', shell=True)

    @patch.object(command_processor, 'Popen')
    @patch.object(command_processor, 'watch_outfile')
    def test_do_run_watch_calls_watch_outfile(self, mock_watch, mock_Popen):
        """do_run calls watch_outfile when --watch option is used
        """
        args = Mock(
            SOG_exec='./SOG', infile='infile', outfile=None,
            nice=19, dry_run=False, watch=True, legacy_infile=False)
        with patch.object(command_processor, 'create_infile',
                          return_value='/tmp/foo.infile'):
            with self.assertRaises(SystemExit):
                command_processor.do_run(args)
        mock_watch.assert_called_once()

    @patch('sys.stdout', new_callable=StringIO)
    @patch.object(command_processor, 'Popen')
    @patch.object(command_processor, 'watch_outfile', return_value=['foo'])
    def test_do_run_watch_prints_outfile(self, mock_watch, mock_Popen,
                                         mock_stdout):
        """do_run prints outfile line when --watch option is used
        """
        args = Mock(
            SOG_exec='./SOG', infile='infile', outfile=None,
            nice=19, dry_run=False, watch=True, legacy_infile=False)
        with patch.object(command_processor, 'create_infile',
                          return_value='/tmp/foo.infile'):
            with self.assertRaises(SystemExit):
                command_processor.do_run(args)
        self.assertEqual(mock_stdout.getvalue(), 'foo')

    @patch('sys.stdout', new_callable=StringIO)
    def test_run_dry_run_std_msg(self, mock_stdout):
        """run_dry_run prints intro msg and command that would be run
        """
        cmd = 'nice -n 19 ./SOG < infile > ./infile.out'
        args = Mock(watch=False)
        command_processor.run_dry_run(cmd, args)
        self.assertEqual(
            mock_stdout.getvalue(),
            'Command that would have been used to run SOG:\n  {0}\n'
            .format(cmd))

    @patch('sys.stdout', new_callable=StringIO)
    def test_run_dry_run_watch_msg(self, mock_stdout):
        """run_dry_run w/ watch prints suffix msg about outfile
        """
        cmd = 'nice -n 19 ./SOG < infile > ./infile.out'
        args = Mock(outfile='./infile.out', watch=True, legacy_infile=False)
        command_processor.run_dry_run(cmd, args)
        self.assertEqual(
            mock_stdout.getvalue(),
            'Command that would have been used to run SOG:\n  {0}\n'
            'Contents of {1.outfile} would have been shown on screen while '
            'SOG run\nwas in progress.\n'.format(cmd, args))
