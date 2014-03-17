"""Unit tests for SOG run processor.

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
import os
import six
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
from .. import run_processor


class TestPrepare(object):
    """Unit tests for the run processor prepare function.
    """
    def _call_prepare(self, args):
        return run_processor.prepare(args)

    @patch.object(run_processor, 'os')
    @patch.object(
        run_processor, 'create_infile', return_value='/tmp/foo.infile')
    def test_prepare_run_cmd_defaults(self, mock_create_infile, mock_os):
        """prepare_run_cmd returns expected command for default args
        """
        mock_os.path.exists.return_value = True
        mock_os.path.basename = os.path.basename
        mock_os.path.abspath = os.path.abspath
        args = Mock(
            SOG_exec='./SOG', infile='infile', outfile=None,
            nice=19, dry_run=False, watch=False, legacy_infile=False)
        cmd = self._call_prepare(args)
        outfile = os.path.abspath(os.path.basename(args.infile) + '.out')
        expected = (
            'nice -n 19 ./SOG < /tmp/foo.infile > {} 2>&1'.format(outfile))
        assert cmd == expected

    @patch.object(run_processor, 'os')
    @patch.object(run_processor, 'create_infile')
    def test_prepare_run_cmd_legacy_infile(self, mock_create_infile, mock_os):
        """prepare_run_cmd returns expected command w/ legacy_infle=True
        """
        mock_os.path.exists.return_value = True
        mock_os.path.basename = os.path.basename
        mock_os.path.abspath = os.path.abspath
        args = Mock(
            SOG_exec='./SOG', infile='infile', outfile=None,
            nice=19, dry_run=False, watch=False, legacy_infile=True)
        cmd = self._call_prepare(args)
        outfile = os.path.abspath(os.path.basename(args.infile) + '.out')
        expected = (
            'nice -n 19 ./SOG < infile > {} 2>&1'.format(outfile))
        assert cmd == expected

    @patch.object(run_processor, 'os')
    @patch.object(run_processor, 'create_infile')
    def test_prepare_run_cmd_editfile_list(self, mock_create_infile, mock_os):
        """prepare_run_cmd calls create_infile with editfile list
        """
        mock_os.path.exists.return_value = True
        mock_os.path.basename = os.path.basename
        mock_os.path.abspath = os.path.abspath
        args = Mock(
            SOG_exec='./SOG', infile='infile.yaml', outfile=None, editfile=[],
            nice=19, dry_run=False, watch=False, legacy_infile=False)
        self._call_prepare(args)
        mock_create_infile.assert_called_once_with(args.infile, args.editfile)

    @patch.object(run_processor, 'os')
    @patch.object(run_processor, 'create_infile')
    def test_prepare_run_cmd_outfile_relative_path(
            self, mock_create_infile, mock_os):
        """prepare_run_cmd returns exp cmd when outfile arg is relative path
        """
        mock_os.path.exists.return_value = True
        mock_create_infile.return_value = '/tmp/foo.infile'
        args = Mock(
            SOG_exec='./SOG', infile='infile', outfile='../foo/bar',
            nice=19, dry_run=False, watch=False, legacy_infile=False)
        cmd = self._call_prepare(args)
        expected = 'nice -n 19 ./SOG < /tmp/foo.infile > ../foo/bar 2>&1'
        assert cmd == expected

    @patch.object(run_processor, 'os')
    @patch.object(
        run_processor, 'create_infile', return_value='/tmp/foo.infile')
    def test_prepare_run_cmd_outfile_absolute_path(
            self, mock_create_infile, mock_os):
        """prepare_run_cmd returns exp cmd when outfile arg is absolute path
        """
        mock_os.path.exists.return_value = True
        args = Mock(
            SOG_exec='./SOG', infile='infile', outfile='/foo/bar',
            nice=19, dry_run=False, watch=False, legacy_infile=False)
        cmd = self._call_prepare(args)
        expected = 'nice -n 19 ./SOG < /tmp/foo.infile > /foo/bar 2>&1'
        assert cmd == expected


class TestDryRun(unittest.TestCase):
    """Unit tests for the run processor dry_run function.
    """
    @patch('sys.stdout', new_callable=six.StringIO)
    def test_run_dry_run_std_msg(self, mock_stdout):
        """run_dry_run prints intro msg and command that would be run
        """
        cmd = 'nice -n 19 ./SOG < infile > ./infile.out'
        args = Mock(watch=False)
        run_processor.dry_run(cmd, args)
        self.assertEqual(
            mock_stdout.getvalue(),
            'Command that would have been used to run SOG:\n  {0}\n'
            .format(cmd))

    @patch('sys.stdout', new_callable=six.StringIO)
    def test_run_dry_run_watch_msg(self, mock_stdout):
        """run_dry_run w/ watch prints suffix msg about outfile
        """
        cmd = 'nice -n 19 ./SOG < infile > ./infile.out'
        args = Mock(outfile='./infile.out', watch=True, legacy_infile=False)
        run_processor.dry_run(cmd, args)
        self.assertEqual(
            mock_stdout.getvalue(),
            'Command that would have been used to run SOG:\n  {0}\n'
            'Contents of {1.outfile} would have been shown on screen while '
            'SOG run\nwas in progress.\n'.format(cmd, args))
