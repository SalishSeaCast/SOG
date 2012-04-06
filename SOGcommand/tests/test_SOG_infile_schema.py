"""Unit tests for SOG Fortran-ish infile schema and data structure
transformation function.
"""
from datetime import datetime
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA
from mock import Mock
import colander


class TestRealDP(unittest.TestCase):
    """Unit tests for _RealDP schema type.
    """
    def _make_schema(self):
        from ..SOG_infile_schema import _RealDP

        class Schema(colander.MappingSchema):
            value = colander.SchemaNode(_RealDP())
        return Schema()

    def test_RealDP_serialize_null(self):
        """_RealDP serialization of null returns null
        """
        schema = self._make_schema()
        result = schema.serialize({'value': colander.null})
        self.assertEqual(result, {'value': colander.null})

    def test_RealDP_serialize_raises_invalid(self):
        """_RealDP serialization of non-number raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(colander.Invalid, schema.serialize, {'value': 'foo'})

    def test_RealDP_serialize_e_format_with_d(self):
        """_RealDP serialization of number is Fortran real(kind=dp) notation
        """
        schema = self._make_schema()
        result = schema.serialize({'value': 42})
        self.assertEqual(result, {'value': '4.200000d+01'})

    def test_RealDP_deserialize_null(self):
        """_RealDP deserialization of null raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(
            colander.Invalid, schema.deserialize, {'value': colander.null})

    def test_RealDP_deserialize_raises_invalid(self):
        """_RealDP deserialization of non-string raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(
            colander.Invalid, schema.deserialize, {'value': 42})

    def test_RealDP_deserialize_d_format_to_float(self):
        """_RealDP deserialization of Fortran real(kind=dp) string is float
        """
        schema = self._make_schema()
        result = schema.deserialize({'value': '42.0d0'})
        self.assertEqual(result, {'value': 42.0})
        self.assertTrue(isinstance(result['value'], float))


class TestDatetime(unittest.TestCase):
    """Unit tests for _Datetime schema type.
    """
    def _make_schema(self):
        from ..SOG_infile_schema import _Datetime

        class Schema(colander.MappingSchema):
            value = colander.SchemaNode(_Datetime())
        return Schema()

    def test_Datetime_serialize_null(self):
        """_Datetime serialization of null returns null
        """
        schema = self._make_schema()
        result = schema.serialize({'value': colander.null})
        self.assertEqual(result, {'value': colander.null})

    def test_Datetime_serialize_raises_invalid(self):
        """_Datetime serialization of non-datetime raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(colander.Invalid, schema.serialize, {'value': 'foo'})

    def test_Datetime_serialize_datetime_to_string(self):
        """_Datetime serialization of datetime is SOG datetime format string
        """
        schema = self._make_schema()
        result = schema.serialize({'value': datetime(2012, 4, 1, 19, 9)})
        self.assertEqual(result, {'value': '"2012-04-01 19:09:00"'})

    def test_Datetime_deserialize_null(self):
        """_Datetime deserialization of null raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(
            colander.Invalid, schema.deserialize, {'value': colander.null})

    def test_Datetime_deserialize_raises_invalid(self):
        """_Datetime deserialization of non-datetime raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(
            colander.Invalid, schema.deserialize, {'value': 42})

    def test_Datetime_deserialize_string_to_datetime(self):
        """_Datetime deserialization of SOG datetime string is datetime object
        """
        schema = self._make_schema()
        result = schema.deserialize({'value': '2012-04-01 19:14:00'})
        self.assertEqual(result, {'value': datetime(2012, 4, 1, 19, 14)})


class TestBoolean(unittest.TestCase):
    """Unit tests for _Boolean schema type.
    """
    def _make_schema(self):
        from ..SOG_infile_schema import _Boolean

        class Schema(colander.MappingSchema):
            value = colander.SchemaNode(_Boolean())
        return Schema()

    def test_Boolean_serialize_null(self):
        """_Boolean serialization of null returns null
        """
        schema = self._make_schema()
        result = schema.serialize({'value': colander.null})
        self.assertEqual(result, {'value': colander.null})

    def test_Boolean_serialize_raises_invalid(self):
        """_Boolean serialization of non-number raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(colander.Invalid, schema.serialize, {'value': 'foo'})

    def test_Boolean_serialize_true(self):
        """_Boolean serialization of True is '.true.'
        """
        schema = self._make_schema()
        result = schema.serialize({'value': True})
        self.assertEqual(result, {'value': '.true.'})

    def test_Boolean_serialize_false(self):
        """_Boolean serialization of False is '.false.'
        """
        schema = self._make_schema()
        result = schema.serialize({'value': False})
        self.assertEqual(result, {'value': '.false.'})

    def test_Boolean_deserialize_null(self):
        """_Boolean deserialization of null raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(
            colander.Invalid, schema.deserialize, {'value': colander.null})

    def test_Boolean_deserialize_raises_invalid(self):
        """_Boolean deserialization of non-boolean raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(
            colander.Invalid, schema.deserialize, {'value': 42})

    def test_Boolean_deserialize_true(self):
        """_Boolean deserialization of .true. is True
        """
        schema = self._make_schema()
        result = schema.deserialize({'value': '.true.'})
        self.assertEqual(result, {'value': True})

    def test_Boolean_deserialize_flase(self):
        """_Boolean deserialization of .false. is False
        """
        schema = self._make_schema()
        result = schema.deserialize({'value': '.faLSe.'})
        self.assertEqual(result, {'value': False})


class TestString(unittest.TestCase):
    """Unit tests for _String schema type.
    """
    def _make_schema(self):
        from ..SOG_infile_schema import _String

        class Schema(colander.MappingSchema):
            value = colander.SchemaNode(_String())
        return Schema()

    def test_String_serialize_null(self):
        """_String serialization of null returns null
        """
        schema = self._make_schema()
        result = schema.serialize({'value': colander.null})
        self.assertEqual(result, {'value': colander.null})

    def test_String_serialize_raises_invalid(self):
        """_String serialization of non-string raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(colander.Invalid, schema.serialize, {'value': 42})

    def test_String_serialize_str_to_double_quoted_string(self):
        """_String serialization of datetime is SOG datetime format string
        """
        schema = self._make_schema()
        result = schema.serialize({'value': 'foo bar'})
        self.assertEqual(result, {'value': '"foo bar"'})

    def test_String_deserialize_null(self):
        """_String deserialization of null raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(
            colander.Invalid, schema.deserialize, {'value': colander.null})

    def test_String_deserialize_raises_invalid(self):
        """_String deserialization of non-string raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(
            colander.Invalid, schema.deserialize, {'value': 42})

    def test_String_deserialize_string_to_datetime(self):
        """_String deserialization of SOG double quoted string is str
        """
        schema = self._make_schema()
        result = schema.deserialize({'value': "foo bar"})
        self.assertEqual(result, {'value': 'foo bar'})


class TestInfileToYAML(unittest.TestCase):
    """Unit tests for infile_to_yaml data structure transformation function.
    """
    def _make_schema(self):
        from ..SOG_infile_schema import SOG_Infile
        return SOG_Infile()

    def _call_infile_to_yaml(self, *args):
        from ..SOG_infile_schema import infile_to_yaml
        return infile_to_yaml(*args)

    def test_infile_to_yaml_with_units(self):
        """infile_to_yaml returns expected result for element with units
        """
        mock_child = Mock()
        mock_child.configure_mock(
            name='model_depth', infile_key='maxdepth', var_name='grid%D',
            children=[Mock(children=[])])
        mock_node = Mock()
        mock_node.configure_mock(name='grid', children=[mock_child])
        nodes = [mock_node]
        schema = self._make_schema()
        infile_struct = {'maxdepth': {
            'value': 40, 'units': 'm',
            'description': 'depth of modelled domain'}}
        result = self._call_infile_to_yaml(nodes, schema, infile_struct)
        self.assertEqual(
            result,
            {'grid': {
                'model_depth': {
                    'value': 40, 'units': 'm', 'variable name': 'grid%D',
                    'description': 'depth of modelled domain'}}})

    def test_infile_to_yaml_without_units(self):
        """infile_to_yaml returns expected result for element without units
        """
        mock_child = Mock()
        mock_child.configure_mock(
            name='grid_size', infile_key='gridsize', var_name='grid%M',
            children=[Mock(children=[])])
        mock_node = Mock()
        mock_node.configure_mock(name='grid', children=[mock_child])
        nodes = [mock_node]
        schema = self._make_schema()
        infile_struct = {'gridsize': {
            'value': 80, 'units': None,
            'description': 'number of grid points'}}
        result = self._call_infile_to_yaml(nodes, schema, infile_struct)
        self.assertEqual(
            result,
            {'grid': {
                'grid_size': {
                    'value': 80, 'variable name': 'grid%M',
                    'description': 'number of grid points'}}})

    def test_infile_to_yaml_unnested_element(self):
        """infile_to_yaml returns expected result for unnested element
        """
        mock_node = Mock()
        mock_node.configure_mock(
            name='end_datetime', infile_key='end datetime',
            var_name='endDatetime', children=[Mock(children=[])])
        nodes = [mock_node]
        schema = self._make_schema()
        infile_struct = {'end datetime': {
            'value': datetime(2012, 4, 2, 19, 1), 'units': None,
            'description': 'end of run date/time'}}
        result = self._call_infile_to_yaml(nodes, schema, infile_struct)
        self.assertEqual(
            result,
            {'end_datetime': {
                'value': datetime(2012, 4, 2, 19, 1),
                'variable name': 'endDatetime',
                'description': 'end of run date/time'}})
