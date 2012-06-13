# -*- coding: utf-8 -*-
"""Unit tests for the SOG infile processor.
"""
from cStringIO import StringIO
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA
from mock import MagicMock
from mock import patch

from .. import infile_processor


class TestCreateInfile(unittest.TestCase):
    """Unit tests for create_infile function.
    """
    def _call_fut(self, *args):
        """Call function under test.
        """
        return infile_processor.create_infile(*args)

    @patch('sys.stderr', new_callable=StringIO)
    def test_create_infile_handles_invalid_yaml_file(self, mock_stderr):
        """create_file raises SystemExit w/ msg if yaml_infile isn't parsable
        """
        mock_data = '! -*- mode: f90 -*-\n! SOG'
        with patch.object(infile_processor, 'open', create=True) as mock_open:
            mock_open.return_value = MagicMock(spec=file)
            mock_open.return_value.__enter__.return_value = mock_data
            self.assertRaises(SystemExit, self._call_fut, 'foo.yaml')
        self.assertEqual(
            mock_stderr.getvalue(),
            'Unable to parse foo.yaml: Are you sure that it is YAML?\n')

    @patch('sys.stderr', new_callable=StringIO)
    @patch.object(infile_processor.yaml, 'load')
    def test_create_infile_handles_yaml_deserialization_error(self, mock_load,
                                                              mock_stderr):
        """create_file raises SystemExit w/ msg if yaml_infile is incomplete
        """
        mock_yaml_data = {'foo': 'bar'}
        mock_load.return_value = mock_yaml_data
        with patch.object(infile_processor, 'open', create=True) as mock_open:
            mock_open.return_value = MagicMock(spec=file)
            self.assertRaises(SystemExit, self._call_fut, 'foo.yaml')
        self.assertTrue(
            mock_stderr.getvalue().startswith(
            'Invalid SOG YAML in foo.yaml. '
            'The following parameters are missing or misspelled:\n'))
        self.assertTrue(
            mock_stderr.getvalue().endswith(" 'vary': u'Required'}\n"))
