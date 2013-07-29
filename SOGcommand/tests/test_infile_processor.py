# -*- coding: utf-8 -*-
"""Unit tests for the SOG infile processor.
"""
from cStringIO import StringIO
import unittest
from mock import call
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

    @patch.object(infile_processor, '_read_yaml_infile')
    @patch.object(infile_processor, '_deserialize_yaml')
    @patch.object(infile_processor, 'yaml_to_infile')
    @patch.object(infile_processor, 'SOG_Infile')
    @patch.object(infile_processor, 'SOG_infile')
    @patch.object(infile_processor, 'NamedTemporaryFile')
    def test_create_infile_returns_temp_file_name(
            self, mock_NTF, mock_Si, mock_SI, mock_yti, mock_dy, mock_ryi):
        """create_infile returns name of temp file
        """
        handle = mock_NTF.return_value = MagicMock()
        handle.__enter__.return_value.name = '/tmp/foo.infile'
        infile_name = self._call_fut('foo.yaml', [])
        self.assertEqual(infile_name, '/tmp/foo.infile')

    @patch.object(infile_processor, '_read_yaml_infile')
    @patch.object(infile_processor, '_deserialize_yaml')
    @patch.object(infile_processor, 'yaml_to_infile')
    @patch.object(infile_processor, 'SOG_Infile')
    @patch.object(infile_processor, 'SOG_infile')
    @patch.object(infile_processor, 'NamedTemporaryFile')
    def test_create_infile_reads_edit_files(
            self, mock_NTF, mock_Si, mock_SI, mock_yti, mock_dy, mock_ryi):
        """create_infile reads infile and edit files in expected order
        """
        mock_NTF.return_value = MagicMock()
        self._call_fut('foo.yaml', ['bar.yaml', 'bax.yaml'])
        self.assertEqual(
            mock_ryi.call_args_list,
            [call('foo.yaml'), call('bar.yaml'), call('bax.yaml')])


class TestReadInfile(unittest.TestCase):
    """Unit tests for read_infile function.
    """
    def _call_fut(self, *args):
        """Call function under test.
        """
        return infile_processor.read_infile(*args)

    @patch.object(infile_processor, '_read_yaml_infile')
    @patch.object(infile_processor, '_deserialize_yaml',
                  return_value={'bar': {'value': 42}})
    def test_read_infile_returns_value(self, mock_dy, mock_ryi):
        """read_infile returns value associated with key
        """
        edit_files = []
        value = self._call_fut('foo.yaml', edit_files, 'bar')
        self.assertEqual(value, 42)

    @patch('sys.stderr', new_callable=StringIO)
    @patch.object(infile_processor, '_read_yaml_infile')
    @patch.object(infile_processor, '_deserialize_yaml', return_value={})
    def test_read_infile_handles_bad_key(self, mock_dy, mock_ryi, mock_stderr):
        """read_infile raises SystemExit w/ msg for bad infile key
        """
        edit_files = []
        with self.assertRaises(SystemExit):
            self._call_fut('foo.yaml', edit_files, 'bar')
        self.assertEqual(mock_stderr.getvalue(), 'KeyError: bar\n')


class TestReadYamlInfile(unittest.TestCase):
    """Unit tests for _read_yaml_infile function.
    """
    def _call_fut(self, *args):
        """Call function under test.
        """
        return infile_processor._read_yaml_infile(*args)

    @patch.object(infile_processor.yaml, 'safe_load')
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
            with self.assertRaises(SystemExit):
                self._call_fut('foo.yaml')
        self.assertEqual(
            mock_stderr.getvalue(),
            'Unable to parse foo.yaml: Are you sure that it is YAML?\n')


class TestDeserializeYaml(unittest.TestCase):
    """Unit tests for _deserialize_yaml function.
    """
    def _call_fut(self, *args, **kwargs):
        """Call function under test.
        """
        return infile_processor._deserialize_yaml(*args, **kwargs)

    @patch.object(infile_processor, 'YAML_Infile')
    def test_deserialize_yaml_binds_schema(self, mock_schema):
        """_deserialize_yaml binds schema with edit_mode
        """
        mock_data = {'foo': 'bar'}
        self._call_fut(mock_data, mock_schema, 'foo.yaml', edit_mode=True)
        mock_schema.bind.assert_valled_once_with(allow_missing=True)

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
        with self.assertRaises(SystemExit):
            self._call_fut(mock_data, YAML_Infile(), 'foo.yaml')
        self.assertTrue(
            mock_stderr.getvalue().startswith(
            'Invalid SOG YAML in foo.yaml. '
            'The following parameters are missing or misspelled:\n'))
        self.assertTrue(
            mock_stderr.getvalue().endswith(" 'vary': u'Required'}\n"))


class TestMergeYamlStructs(unittest.TestCase):
    """Unit tests for _merge_yaml_structs function.
    """
    def _call_fut(self, *args):
        """Call function under test.
        """
        return infile_processor._merge_yaml_structs(*args)

    def test_merge_yaml_structs_ignores_empty_blocks(self):
        """_merge_yaml_structs ignores empty/missing blocks in edit_struct
        """
        import colander
        from datetime import datetime
        from ..SOG_YAML_schema import _SOG_Datetime
        class MockSchema(colander.MappingSchema): # NOQA
            end_datetime = _SOG_Datetime(
                infile_key='end datetime', var_name='endDatetime')
        mock_schema = MockSchema()
        yaml_struct = mock_schema.deserialize(
            {
                'end_datetime': {
                    'value': datetime(2012, 6, 22, 12, 55),
                    'variable_name': 'endDatetime',
                    'description': 'end of run date/time',
            }})
        edit_struct = {'end_datetime': None}
        self._call_fut(edit_struct, yaml_struct, mock_schema)
        self.assertEqual(
            yaml_struct['end_datetime']['value'],
            datetime(2012, 6, 22, 12, 55))

    def test_merge_yaml_structs_updates_yaml_struct(self):
        """_merge_yaml_structs updates yaml_struct w/ value from edit_struct
        """
        import colander
        from datetime import datetime
        from ..SOG_YAML_schema import _SOG_Datetime
        class MockSchema(colander.MappingSchema): # NOQA
            end_datetime = _SOG_Datetime(
                infile_key='end datetime', var_name='endDatetime')
        mock_schema = MockSchema()
        yaml_struct = mock_schema.deserialize(
            {
                'end_datetime': {
                    'value': datetime(2012, 6, 22, 12, 55),
                    'variable_name': 'endDatetime',
                    'description': 'end of run date/time',
            }})
        edit_struct = mock_schema.deserialize(
            {
                'end_datetime': {
                    'value': datetime(2012, 6, 22, 12, 58),
                    'variable_name': 'endDatetime',
                    'description': 'end of run date/time',
            }})
        self._call_fut(edit_struct, yaml_struct, mock_schema)
        self.assertEqual(
            yaml_struct['end_datetime']['value'],
            datetime(2012, 6, 22, 12, 58))

    def test_merge_yaml_structs_handles_zero_values(self):
        """_merge_yaml_structs handle change value to 0 properly
        """
        import colander
        from ..SOG_YAML_schema import _Float
        class MockSchema(colander.MappingSchema): # NOQA
            mesozoo_grazing_limit = _Float(
                infile_key='Mesozoo, pred slope',
                var_name='rate_mesozoo%PredSlope')
        mock_schema = MockSchema()
        yaml_struct = mock_schema.deserialize(
            {
                'mesozoo_grazing_limit': {
                    'value': 0.2,
                    'variable_name': 'Mesozoo, pred slope',
                    'description': 'mesozooplankton total grazing limit',
            }})
        edit_struct = mock_schema.deserialize(
            {
                'mesozoo_grazing_limit': {
                    'value': 0,
                    'variable_name': 'Mesozoo, pred slope',
                    'description': 'mesozooplankton total grazing limit',
            }})
        self._call_fut(edit_struct, yaml_struct, mock_schema)
        self.assertEqual(yaml_struct['mesozoo_grazing_limit']['value'], 0)
