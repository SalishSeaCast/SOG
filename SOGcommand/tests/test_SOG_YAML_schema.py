# -*- coding: utf-8 -*-
"""Unit tests for SOG YAML infile schema and data structure
transformation function.
"""
from datetime import datetime
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA
from mock import Mock
import colander


class TestDeferredAllowMissing(unittest.TestCase):
    """Unit tests for deferred_allow_missing schema binding function.
    """
    def _call_fut(self, *args):
        """Call function under test.
        """
        from ..SOG_YAML_schema import deferred_allow_missing
        return deferred_allow_missing(*args)

    def test_deferred_allow_missing_allow_missing_true(self):
        """deferred_allow_missing returns None if allow_missing arg == True
        """
        result = self._call_fut(Mock(), {'allow_missing': True})
        self.assertIsNone(result)

    def test_deferred_allow_missing_allow_missing_false(self):
        """deferred_allow_missing returns reqd if allow_missing arg == False
        """
        result = self._call_fut(Mock(), {'allow_missing': False})
        self.assertEqual(result, colander.required)


class TestDateTime(unittest.TestCase):
    """Unit tests for _DateTime schema type.
    """
    def _make_schema(self):
        from ..SOG_YAML_schema import _DateTime

        class Schema(colander.MappingSchema):
            value = colander.SchemaNode(_DateTime())
        return Schema()

    def test_DateTime_serialize_null(self):
        """_DateTime serialization of null returns null
        """
        schema = self._make_schema()
        result = schema.serialize({'value': colander.null})
        self.assertEqual(result, {'value': colander.null})

    def test_DateTime_serialize_raises_invalid(self):
        """_DateTime serialization of non-datetime raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(colander.Invalid, schema.serialize, {'value': 'foo'})

    def test_DateTime_serialize_datetime_to_datetime(self):
        """_DateTime serialization of datetime is yyyy-mm-dd hh:mm:ss
        """
        schema = self._make_schema()
        result = schema.serialize({'value': datetime(2012, 4, 1, 20, 47)})
        self.assertEqual(result, {'value': datetime(2012, 4, 1, 20, 47)})

    def test_DateTime_deserialize_null(self):
        """_DateTime deserialization of null raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(
            colander.Invalid, schema.deserialize, {'value': colander.null})

    def test_DateTime_deserialize_raises_invalid(self):
        """_DateTime deserialization of non-datetime raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(
            colander.Invalid, schema.deserialize, {'value': 42})

    def test_DateTime_deserialize_datetime_to_datetime(self):
        """_DateTime deserialization of datetime is datetime object
        """
        schema = self._make_schema()
        result = schema.deserialize({'value': datetime(2012, 4, 1, 20, 49)})
        self.assertEqual(result, {'value': datetime(2012, 4, 1, 20, 49)})


class TestFloatList(unittest.TestCase):
    """Unit tests for _FloatList schema type.
    """
    def _make_schema(self):
        from ..SOG_YAML_schema import _FloatList

        class Schema(colander.MappingSchema):
            value = colander.SchemaNode(_FloatList())
        return Schema()

    def test_FloatList_serialize_null(self):
        """_FloatList serialization of null returns null
        """
        schema = self._make_schema()
        result = schema.serialize({'value': colander.null})
        self.assertEqual(result, {'value': colander.null})

    def test_FloatList_serialize_non_list_raises_invalid(self):
        """_FloatList serialization of non-list raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(colander.Invalid, schema.serialize, {'value': 'foo'})

    def test_FloatList_serialize_non_number_item_raises_invalid(self):
        """_FloatList serialization of non-number item raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(
            colander.Invalid, schema.serialize, {'value': ['foo', 42]})

    def test_FloatList_serialize_list_to_list(self):
        """_FloatList serialization of list of numbers is passed unchanged
        """
        schema = self._make_schema()
        result = schema.serialize({'value': [42, 43]})
        self.assertEqual(result, {'value': [42, 43]})

    def test_FloatList_deserialize_null(self):
        """_FloatList deserialization of null raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(
            colander.Invalid, schema.deserialize, {'value': colander.null})

    def test_FloatList_deserialize_non_list_raises_invalid(self):
        """_FloatList deserialization of non-list raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(
            colander.Invalid, schema.deserialize, {'value': 42})

    def test_FloatList_deserialize_non_number_item_raises_invalid(self):
        """_FloatList deserialization of non-number item raises Invalid
        """
        schema = self._make_schema()
        self.assertRaises(
            colander.Invalid, schema.deserialize, {'value': [42, 'foo']})

    def test_FloatList_deserialize_list_to_list(self):
        """_FloatList deserialization of list of numbers is passed unchanged
        """
        schema = self._make_schema()
        result = schema.deserialize({'value': [42, 24]})
        self.assertEqual(result, {'value': [42, 24]})


class TestIntList(unittest.TestCase):
    """Unit tests for _IntList schema type.
    """
    def _make_schema(self):
        from ..SOG_YAML_schema import _IntList

        class Schema(colander.MappingSchema):
            value = colander.SchemaNode(_IntList())
        return Schema()

    def test_IntList_serialize_null(self):
        """_IntList serialization of null returns null
        """
        schema = self._make_schema()
        result = schema.serialize({'value': colander.null})
        self.assertEqual(result, {'value': colander.null})

    def test_IntList_serialize_non_list_raises_invalid(self):
        """_IntList serialization of non-list raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(colander.Invalid, schema.serialize, {'value': 'foo'})

    def test_IntList_serialize_non_number_item_raises_invalid(self):
        """_IntList serialization of non-number item raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(
            colander.Invalid, schema.serialize, {'value': ['foo', 42]})

    def test_IntList_serialize_list_to_list(self):
        """_IntList serialization of list of numbers is passed unchanged
        """
        schema = self._make_schema()
        result = schema.serialize({'value': [42, 43]})
        self.assertEqual(result, {'value': [42, 43]})

    def test_IntList_deserialize_null(self):
        """_IntList deserialization of null raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(
            colander.Invalid, schema.deserialize, {'value': colander.null})

    def test_IntList_deserialize_non_list_raises_invalid(self):
        """_IntList deserialization of non-list raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(
            colander.Invalid, schema.deserialize, {'value': 42})

    def test_IntList_deserialize_non_number_item_raises_invalid(self):
        """_IntList deserialization of non-number item raises Invalid
        """
        schema = self._make_schema()
        self.assertRaises(
            colander.Invalid, schema.deserialize, {'value': [42, 'foo']})

    def test_IntList_deserialize_list_to_list(self):
        """_IntList deserialization of list of numbers is passed unchanged
        """
        schema = self._make_schema()
        result = schema.deserialize({'value': [42, 24]})
        self.assertEqual(result, {'value': [42, 24]})


class TestYAMLtoInfile(unittest.TestCase):
    """Unit tests for yaml_to_infile data structure transformation function.
    """
    def _make_schema(self):
        from ..SOG_YAML_schema import YAML_Infile
        return YAML_Infile()

    def _call_yaml_to_infile(self, *args):
        from ..SOG_YAML_schema import yaml_to_infile
        return yaml_to_infile(*args)

    def test_yaml_to_infile_number(self):
        """yaml_to_infile returns expected result for number value
        """
        mock_child = Mock()
        mock_child.configure_mock(
            name='model_depth', infile_key='maxdepth', var_name='grid%D',
            children=[Mock(children=[])])
        mock_node = Mock()
        mock_node.configure_mock(name='grid', children=[mock_child])
        nodes = [mock_node]
        schema = self._make_schema()
        yaml_struct = {
            'grid': {
                'model_depth': {
                    'value': 40, 'units': 'm', 'variable_name': 'grid%D',
                    'description': 'depth of modelled domain'}}}
        result = self._call_yaml_to_infile(nodes, schema, yaml_struct)
        self.assertEqual(
            result,
            {'maxdepth': {
                'value': 40, 'units': 'm',
                'description': 'depth of modelled domain'}})

    def test_yaml_to_infile_datetime(self):
        """yaml_to_infile returns expected result for datetime value
        """
        mock_child = Mock()
        mock_child.configure_mock(
            name='init_datetime', infile_key='init datetime',
            var_name='initDatetime', children=[Mock(children=[])])
        mock_node = Mock()
        mock_node.configure_mock(
            name='initial_conditions', children=[mock_child])
        nodes = [mock_node]
        schema = self._make_schema()
        yaml_struct = {
            'initial_conditions': {
                'init_datetime': {
                    'value': datetime(2012, 4, 1, 21, 4), 'units': None,
                    'variable_name': 'initDatetime',
                    'description': 'initialization CTD profile date/time'}}}
        result = self._call_yaml_to_infile(nodes, schema, yaml_struct)
        self.assertEqual(
            result,
            {'init datetime': {
                'value': datetime(2012, 4, 1, 21, 4), 'units': None,
                'description': 'initialization CTD profile date/time'}})

    def test_yaml_to_infile_unnested_element(self):
        """yaml_to_infile returns expected result for unnested element
        """
        mock_node = Mock()
        mock_node.configure_mock(
            name='end_datetime', infile_key='end datetime',
            var_name='endDatetime', children=[Mock(children=[])])
        nodes = [mock_node]
        schema = self._make_schema()
        yaml_struct = {
            'end_datetime': {
                'value': datetime(2012, 4, 2, 21, 21), 'units': None,
                'variable_name': 'initDatetime',
                'description': 'end of run date/time'}}
        result = self._call_yaml_to_infile(nodes, schema, yaml_struct)
        self.assertEqual(
            result,
            {'end datetime': {
                'value': datetime(2012, 4, 2, 21, 21), 'units': None,
                'description': 'end of run date/time'}})
