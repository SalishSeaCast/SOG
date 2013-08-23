# -*- coding: utf-8 -*-
"""Unit tests for SOG YAML infile schema and data structure
transformation function.

:Author: Doug Latornell <djl@douglatornell.ca>
:License: Apache License, Version 2.0


Copyright 2010-2013 Doug Latornell and The University of British Columbia

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
from datetime import datetime
import unittest
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock
import colander


class TestDeferredAllowMissing(unittest.TestCase):
    """Unit tests for _deferred_allow_missing schema binding function.
    """
    def _call_fut(self, *args):
        """Call function under test.
        """
        from ..SOG_YAML_schema import _deferred_allow_missing
        return _deferred_allow_missing(*args)

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
    def _call_yaml_to_infile(self, *args):
        from ..SOG_YAML_schema import yaml_to_infile
        return yaml_to_infile(*args)

    def test_yaml_to_infile_number(self):
        """yaml_to_infile returns expected result for number value
        """
        from ..SOG_YAML_schema import YAML_Infile
        schema = YAML_Infile().clone()
        schema.children = [child for child in schema.children
                           if child.name == 'grid']
        grid_schema = schema.children[0]
        grid_schema.children = [child for child in grid_schema
                                if child.name == 'model_depth']
        yaml_struct = {
            'grid': {
                'model_depth': {
                    'value': 40, 'units': 'm', 'variable_name': 'grid%D',
                    'description': 'depth of modelled domain'}}}
        result = self._call_yaml_to_infile(schema, yaml_struct)
        self.assertEqual(
            result,
            {'maxdepth': {
                'value': 40, 'units': 'm',
                'description': 'depth of modelled domain'}})

    def test_yaml_to_infile_datetime(self):
        """yaml_to_infile returns expected result for datetime value
        """
        from ..SOG_YAML_schema import YAML_Infile
        schema = YAML_Infile().clone()
        schema.children = [child for child in schema.children
                           if child.name == 'initial_conditions']
        init_cond_schema = schema.children[0]
        init_cond_schema.children = [child for child in init_cond_schema
                                     if child.name == 'init_datetime']
        yaml_struct = {
            'initial_conditions': {
                'init_datetime': {
                    'value': datetime(2012, 4, 1, 21, 4), 'units': None,
                    'variable_name': 'initDatetime',
                    'description': 'initialization CTD profile date/time'}}}
        result = self._call_yaml_to_infile(schema, yaml_struct)
        self.assertEqual(
            result,
            {'init datetime': {
                'value': datetime(2012, 4, 1, 21, 4), 'units': None,
                'description': 'initialization CTD profile date/time'}})

    def test_yaml_to_infile_unnested_element(self):
        """yaml_to_infile returns expected result for unnested element
        """
        from ..SOG_YAML_schema import YAML_Infile
        schema = YAML_Infile().clone()
        schema.children = [child for child in schema.children
                           if child.name == 'end_datetime']
        yaml_struct = {
            'end_datetime': {
                'value': datetime(2012, 4, 2, 21, 21), 'units': None,
                'variable_name': 'initDatetime',
                'description': 'end of run date/time'}}
        result = self._call_yaml_to_infile(schema, yaml_struct)
        self.assertEqual(
            result,
            {'end datetime': {
                'value': datetime(2012, 4, 2, 21, 21), 'units': None,
                'description': 'end of run date/time'}})
