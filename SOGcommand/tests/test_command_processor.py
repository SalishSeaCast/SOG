"""Unit tests for SOG command processor

:Author: Doug Latornell <djl@douglatornell.ca>
:License: Apache License, Version 2.0


Copyright 2010-2014 Doug Latornell and The University of British Columbia

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
import unittest
try:
    from unittest.mock import (
        Mock,
        patch,
    )
except ImportError:
    from mock import (
        Mock,
        patch,
    )
import six
from .. import command_processor


class TestEntryPoint(unittest.TestCase):
    """Unit tests for the SOG command processor entry point function.
    """
    def _call_entry_point(self):
        from ..command_processor import run
        run()

    @patch.object(command_processor, '_build_parser', return_value=Mock())
    def test_entry_w_1_arg_print_help(self, mock_build_parser):
        """run w/ 1 cmd line arg calls parser print_help
        """
        with patch.object(command_processor, 'sys') as mock_sys:
            mock_sys.argv = ['SOG']
            self._call_entry_point()
        mock_build_parser.print_help.assert_called_once()

    @patch.object(command_processor, '_build_parser', return_value=Mock())
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
        parser = command_processor._build_parser()
        self.assertIsInstance(parser, ArgumentParser)


class TestRunCommand(unittest.TestCase):
    """Unit tests for the SOG command processor run command.
    """
    @patch.object(command_processor, 'Popen')
    @patch.object(command_processor.run_processor, 'prepare')
    def test__do_run_prepare_run_cmd(self, mock_prepare, mock_Popen):
        """_do_run calls run_processor.prepare
        """
        args = Mock(
            SOG_exec='./SOG', infile='infile.yaml', outfile=None, editfile=[],
            nice=19, dry_run=False, watch=False, legacy_infile=False)
        with self.assertRaises(SystemExit):
            command_processor._do_run(args)
        mock_prepare.assert_called_once()

    @patch.object(command_processor, 'Popen')
    @patch.object(command_processor.run_processor, 'prepare')
    @patch.object(command_processor.run_processor, 'dry_run')
    def test__do_run_dry_run(
            self, mock_dry_run, mock_prepare, mock_Popen):
        """_do_run calls run_processor.dry_run when --dry-run option is used
        """
        args = Mock(
            SOG_exec='./SOG', infile='infile', outfile=None,
            nice=19, dry_run=True, watch=False, legacy_infile=False)
        with self.assertRaises(SystemExit):
            command_processor._do_run(args)
        mock_dry_run.assert_called_once()

    @patch.object(command_processor.run_processor, 'prepare')
    @patch.object(command_processor, 'Popen', return_value=Mock(name='proc'))
    def test__do_run_default_waits_for_end_of_run(
            self, mock_Popen, mock_prepare):
        """_do_run waits for end of run by default
        """
        args = Mock(
            SOG_exec='./SOG', infile='infile', outfile=None,
            nice=19, dry_run=False, watch=False, legacy_infile=False)
        with self.assertRaises(SystemExit):
            command_processor._do_run(args)
        mock_Popen().wait.assert_called_once()

    @patch.object(command_processor.run_processor, 'prepare')
    @patch.object(command_processor, 'Popen')
    @patch.object(command_processor.run_processor, 'watch_outfile')
    def test__do_run_watch_calls_watch_outfile(
            self, mock_watch, mock_Popen, mock_prepare):
        """_do_run calls watch_outfile when --watch option is used
        """
        args = Mock(
            SOG_exec='./SOG', infile='infile', outfile=None,
            nice=19, dry_run=False, watch=True, legacy_infile=False)
        with self.assertRaises(SystemExit):
            command_processor._do_run(args)
        mock_watch.assert_called_once()

    @patch('sys.stdout', new_callable=six.StringIO)
    @patch.object(command_processor.run_processor, 'prepare')
    @patch.object(command_processor, 'Popen')
    @patch.object(
        command_processor.run_processor, 'watch_outfile', return_value=['foo'])
    def test__do_run_watch_prints_outfile(
            self, mock_watch, mock_Popen, mock_prepare, mock_stdout):
        """_do_run prints outfile line when --watch option is used
        """
        args = Mock(
            SOG_exec='./SOG', infile='infile', outfile=None,
            nice=19, dry_run=False, watch=True, legacy_infile=False)
        with self.assertRaises(SystemExit):
            command_processor._do_run(args)
        self.assertEqual(mock_stdout.getvalue(), 'foo')
