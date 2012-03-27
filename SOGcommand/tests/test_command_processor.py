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
from ..command_processor import SOGcommand


class TestEntryPoint(unittest.TestCase):
    """Unit tests for the SOG command processor entry point function.
    """
    def _call_entry_point(self):
        from ..command_processor import run
        run()

    @patch.object(SOGcommand, 'onecmd')
    def test_run_calls_onecmd_w_1_arg(self, mock_onecmd):
        """run call SOGcommand.onecmd w/ empty str when 1 cmd line arg
        """
        with patch.object(command_processor, 'sys') as mock_sys:
            mock_sys.argv = ['SOG']
            self._call_entry_point()
        mock_onecmd.assert_called_once_with('')

    @patch.object(SOGcommand, 'onecmd')
    def test_run_calls_onecmd_w_2_args(self, mock_onecmd):
        """run call SOGcommand.onecmd w/ 2nd arg when 2 cmd line arg
        """
        with patch.object(command_processor, 'sys') as mock_sys:
            mock_sys.argv = 'SOG run'.split()
            self._call_entry_point()
        mock_onecmd.assert_called_once_with('run')

    @patch.object(SOGcommand, 'onecmd')
    def test_run_calls_onecmd_w_3_args(self, mock_onecmd):
        """run call SOGcommand.onecmd w/ spaced args when >2 cmd line arg
        """
        with patch.object(command_processor, 'sys') as mock_sys:
            mock_sys.argv = 'SOG run infile'.split()
            self._call_entry_point()
        mock_onecmd.assert_called_once_with('run infile')

    @patch.object(SOGcommand, 'emptyline')
    def test_run_w_1_arg_calls_emptyline(self, mock_emptyline):
        """run called w/ 1 arg passes through to SOGcommand.emptyline method
        """
        with patch.object(command_processor, 'sys') as mock_sys:
            mock_sys.argv = ['SOG']
            self._call_entry_point()
        mock_emptyline.assert_called_once()

    @patch.object(SOGcommand, 'default')
    def test_run_unknown_command_calls_default(self, mock_default):
        """run called with an unknown SOG command passes to SOGcommand.default
        """
        with patch.object(command_processor, 'sys') as mock_sys:
            mock_sys.argv = 'SOG foo'.split()
            self._call_entry_point()
        mock_default.assert_called_once_with('foo')


class TestSOGcommand(unittest.TestCase):
    """Unit tests for generic elements of SOG command processor.
    """
    def _get_target_class(self):
        from ..command_processor import SOGcommand
        return SOGcommand

    def _make_one(self):
        return self._get_target_class()()

    def test_SOGcommand_has_text_wrapper(self):
        """SOGcommand instance has text wrapper attribute
        """
        from textwrap import TextWrapper
        processor = self._make_one()
        self.assertIsInstance(processor.wrapper, TextWrapper)

    @patch.object(SOGcommand, 'do_help')
    def test_SOGcommand_emptyline_calls_do_help(self, mock_do_help):
        """emptyline method calls do_help method
        """
        processor = self._make_one()
        processor.emptyline()
        mock_do_help.assert_called_once()

    @patch('sys.stdout', new_callable=StringIO)
    def test_SOGcommand_default_version_arg(self, mock_stdout):
        """default method called w/ --version prints SOGcommand version str
        """
        from ..__version__ import version
        processor = self._make_one()
        processor.default('--version')
        self.assertEqual(mock_stdout.getvalue().strip(), version)

    @patch('sys.stdout', new_callable=StringIO)
    def test_SOGcommand_default_unknown_arg_error_msg(self, mock_stdout):
        """default method called w/ unknown command prints error message
        """
        processor = self._make_one()
        processor.default('foo bar')
        self.assertTrue(
            mock_stdout.getvalue().startswith('*** Unknown command: foo'))

    @patch.object(SOGcommand, 'do_help')
    @patch('sys.stdout', new_callable=StringIO)
    def test_default_unknown_arg_help(self, mock_stdout, mock_do_help):
        """default method called w/ unknown command calls do_help method
        """
        processor = self._make_one()
        processor.default('foo bar')
        mock_do_help.assert_called_once()


class Test_run(unittest.TestCase):
    """Unit tests for run command.
    """
    def _get_target_class(self):
        from ..command_processor import SOGcommand
        return SOGcommand

    def _make_one(self):
        return self._get_target_class()()

    @patch('sys.stderr', new_callable=StringIO)
    def test_run_parser_too_few_args_raises_SystemExit(self, mock_stderr):
        """run arg parser raises error for <2 positional args
        """
        processor = self._make_one()
        parser = processor.run_parser()
        self.assertRaises(SystemExit, parser.parse_args, '')

    @patch('sys.stderr', new_callable=StringIO)
    def test_run_parser_too_few_args_error_message(self, mock_stderr):
        """run arg parser has error message for <2 positional args
        """
        processor = self._make_one()
        parser = processor.run_parser()
        with self.assertRaises(SystemExit):
            parser.parse_args(['foo'])
        self.assertTrue(
            mock_stderr.getvalue().endswith('run: error: too few arguments\n'))

    def test_run_parser_SOG_exec_arg(self):
        """run arg parser captures SOG executable
        """
        processor = self._make_one()
        parser = processor.run_parser()
        args = parser.parse_args('./SOG infile'.split())
        self.assertEqual(args.SOG_exec, './SOG')

    def test_run_parser_infile_arg(self):
        """run arg parser captures infile
        """
        processor = self._make_one()
        parser = processor.run_parser()
        args = parser.parse_args('./SOG infile'.split())
        self.assertEqual(args.infile, 'infile')

    def test_run_parser_outfile_option(self):
        """run arg parser captures outfile option value
        """
        processor = self._make_one()
        parser = processor.run_parser()
        args = parser.parse_args('./SOG infile --outfile=foo'.split())
        self.assertEqual(args.outfile, 'foo')

    def test_run_parser_default_outfile_option(self):
        """run outfile option value defaults to None
        """
        processor = self._make_one()
        parser = processor.run_parser()
        args = parser.parse_args('./SOG infile'.split())
        self.assertIsNone(args.outfile)

    def test_run_parser_default_nice_option(self):
        """run nice option value defaults to 19
        """
        processor = self._make_one()
        parser = processor.run_parser()
        args = parser.parse_args('./SOG infile'.split())
        self.assertEqual(args.nice, 19)

    def test_run_parser_default_watch_option(self):
        """run watch option value defaults to False
        """
        processor = self._make_one()
        parser = processor.run_parser()
        args = parser.parse_args('./SOG infile'.split())
        self.assertFalse(args.watch)

    @patch.object(command_processor, 'Popen')
    def test_do_run_default(self, mock_Popen):
        """do_run spawns expected command for default args
        """
        processor = self._make_one()
        processor.do_run('./SOG infile')
        mock_Popen.assert_called_once_with(
            'nice -n 19 ./SOG < infile > infile.out', shell=True)

    @patch.object(SOGcommand, 'run_dry_run')
    def test_do_run_dry_run(self, mock_run_dry_run):
        """do_run calls run_dry_run when --dry-run option is used
        """
        processor = self._make_one()
        processor.do_run('./SOG infile --dry-run')
        mock_run_dry_run.assert_called_once()

    @patch.object(command_processor, 'Popen', return_value=Mock(name='proc'))
    def test_do_run_default_waits_for_end_of_run(self, mock_Popen):
        """do_run waits for end of run by default
        """
        processor = self._make_one()
        processor.do_run('./SOG infile')
        mock_Popen().wait.assert_called_once()

    @patch.object(SOGcommand, 'watch_outfile')
    @patch.object(command_processor, 'Popen')
    def test_do_run_watch_calls_watch_outfile(self, mock_Popen, mock_watch):
        """do_run calls watch_outfile when --watch option is used
        """
        processor = self._make_one()
        processor.do_run('./SOG infile --watch')
        mock_watch.assert_called_once()
