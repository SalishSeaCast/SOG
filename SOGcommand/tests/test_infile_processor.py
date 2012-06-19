# -*- coding: utf-8 -*-
"""Unit tests for the SOG infile processor.
"""
from contextlib import nested
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

    def test_create_infile_returns_temp_file_name(self):
        """create_infile returns name of temp file
        """
        context_mgr = nested(
            patch.object(infile_processor, '_read_yaml_infile'),
            patch.object(infile_processor, '_deserialize_yaml'),
            patch.object(infile_processor, 'yaml_to_infile'),
            patch.object(infile_processor, 'SOG_Infile'),
            patch.object(infile_processor, 'SOG_infile'),
            patch.object(infile_processor, 'NamedTemporaryFile'),
        )
        with context_mgr as mocks:
            mock_NTF = mocks[5]
            handle = mock_NTF.return_value = MagicMock(spec=file)
            handle.__enter__.return_value.name = '/tmp/foo.infile'
            infile_name = self._call_fut('foo.yaml')
        self.assertEqual(infile_name, '/tmp/foo.infile')


class TestReadInfile(unittest.TestCase):
    """Unit tests for read_infile function.
    """
    def _call_fut(self, *args):
        """Call function under test.
        """
        return infile_processor.read_infile(*args)

    def test_read_infile_returns_value(self):
        """read_infile returns value associated with key
        """
        context_mgr = nested(
            patch.object(infile_processor, '_read_yaml_infile'),
            patch.object(infile_processor, '_deserialize_yaml',
        return_value={'bar': {'value': 42}}),
        )
        with context_mgr:
            value = self._call_fut('foo.yaml', 'bar')
        self.assertEqual(value, 42)

    @patch('sys.stderr', new_callable=StringIO)
    def test_read_infile_handles_bad_key(self, mock_stderr):
        """read_infile raises SystemExit w/ msg for bad infile key
        """
        context_mgr = nested(
            patch.object(infile_processor, '_read_yaml_infile'),
            patch.object(infile_processor, '_deserialize_yaml',
                         return_value={}),
        )
        with context_mgr:
            self.assertRaises(SystemExit, self._call_fut, 'foo.yaml', 'bar')
        self.assertEqual(mock_stderr.getvalue(), 'KeyError: bar\n')


class TestReadYamlInfile(unittest.TestCase):
    """Unit tests for _read_yaml_infile function.
    """
    def _call_fut(self, *args):
        """Call function under test.
        """
        return infile_processor._read_yaml_infile(*args)

    @patch.object(infile_processor.yaml, 'load')
    def test_read_yaml_infile_loads_yaml_file(self, mock_load):
        """
        """
        with patch.object(infile_processor, 'open', create=True) as mock_open:
            mock_open.return_value = MagicMock(spec=file)
            mock_file_obj = mock_open.return_value.__enter__.return_value
            self._call_fut('foo.yaml')
        mock_load.assert_called_once_with(mock_file_obj)

    @patch('sys.stderr', new_callable=StringIO)
    def test_read_yaml_infile_handles_invalid_yaml_file(self, mock_stderr):
        """_read_yaml_infile raises SystemExit w/ msg for bad yaml_infile
        """
        mock_data = '! -*- mode: f90 -*-\n! SOG'
        with patch.object(infile_processor, 'open', create=True) as mock_open:
            mock_open.return_value = MagicMock(spec=file)
            mock_open.return_value.__enter__.return_value = mock_data
            self.assertRaises(SystemExit, self._call_fut, 'foo.yaml')
        self.assertEqual(
            mock_stderr.getvalue(),
            'Unable to parse foo.yaml: Are you sure that it is YAML?\n')


class TestDeserializeYaml(unittest.TestCase):
    """Unit tests for _deserialize_yaml function.
    """
    def _call_fut(self, *args):
        """Call function under test.
        """
        return infile_processor._deserialize_yaml(*args)

    @patch.object(infile_processor, 'YAML_Infile')
    def test_deserialize_yaml_deserializes_data(self, mock_schema):
        """_deserialize_yaml calls YAML schema deserialize method with data
        """
        mock_data = {'foo': 'bar'}
        self._call_fut(mock_data, mock_schema, 'foo.yaml')
        mock_schema.deserialize.assert_valled_once_with(mock_data)

    @patch('sys.stderr', new_callable=StringIO)
    def test_deserialize_yaml_handles_error(self, mock_stderr):
        """_deserialize_yaml raises SystemExit w/ msg if data is incomplete
        """
        from ..SOG_YAML_schema import YAML_Infile
        mock_data = {'foo': 'bar'}
        self.assertRaises(SystemExit, self._call_fut,
                          mock_data, YAML_Infile(), 'foo.yaml')
        self.assertTrue(
            mock_stderr.getvalue().startswith(
            'Invalid SOG YAML in foo.yaml. '
            'The following parameters are missing or misspelled:\n'))
        self.assertTrue(
            mock_stderr.getvalue().endswith(" 'vary': u'Required'}\n"))
