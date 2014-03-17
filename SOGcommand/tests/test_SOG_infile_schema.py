# -*- coding: utf-8 -*-
"""Unit tests for SOG Fortran-ish infile schema and data structure
transformation function.

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
from datetime import datetime
import unittest
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
        self.assertEqual(result, {'value': float(42)})


class TestRealDP_List(unittest.TestCase):
    """Unit tests for _RealDP_List schema type.
    """
    def _make_schema(self):
        from ..SOG_infile_schema import _RealDP_List

        class Schema(colander.MappingSchema):
            value = colander.SchemaNode(_RealDP_List())
        return Schema()

    def test_RealDP_List_serialize_null(self):
        """_RealDP_List serialization of null returns null
        """
        schema = self._make_schema()
        result = schema.serialize({'value': colander.null})
        self.assertEqual(result, {'value': colander.null})

    def test_RealDP_List_serialize_non_list_raises_invalid(self):
        """_RealDP_List serialization of non-list raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(colander.Invalid, schema.serialize, {'value': 'foo'})

    def test_RealDP_List_serialize_non_number_item_raises_invalid(self):
        """_RealDP_List serialization of non-number list item raises Invalid
        """
        schema = self._make_schema()
        self.assertRaises(
            colander.Invalid, schema.serialize, {'value': [42, 'foo']})

    def test_RealDP_List_serialize_list_e_format_with_d(self):
        """_RealDP_List serialization of number list is Fortran real(kind=dp)
        """
        schema = self._make_schema()
        result = schema.serialize({'value': [42, 43]})
        self.assertEqual(result, {'value': '4.200000d+01 4.300000d+01'})

    def test_RealDP_List_deserialize_null(self):
        """_RealDP_List deserialization of null raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(
            colander.Invalid, schema.deserialize, {'value': colander.null})

    def test_RealDP_List_deserialize_raises_invalid(self):
        """_RealDP_List deserialization of non-string raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(
            colander.Invalid, schema.deserialize, {'value': 42})

    def test_RealDP_List_deserialize_d_floats_to_list(self):
        """_RealDP_List deserialization of Fortran floats string is list
        """
        schema = self._make_schema()
        result = schema.deserialize({'value': '42.0d0 24.0d0'})
        self.assertEqual(result, {'value': [float(42), float(24)]})


class TestIntList(unittest.TestCase):
    """Unit tests for _IntList schema type.
    """
    def _make_schema(self):
        from ..SOG_infile_schema import _IntList

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
        """_IntList serialization of non-number list item raises Invalid
        """
        schema = self._make_schema()
        self.assertRaises(
            colander.Invalid, schema.serialize, {'value': [42, 'foo']})

    def test_IntList_serialize_ints_to_integers(self):
        """_IntList serialization of number list is Fortran integer
        """
        schema = self._make_schema()
        result = schema.serialize({'value': [42, 43]})
        self.assertEqual(result, {'value': '42 43'})

    def test_IntList_deserialize_null(self):
        """_IntList deserialization of null raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(
            colander.Invalid, schema.deserialize, {'value': colander.null})

    def test_IntList_deserialize_raises_invalid(self):
        """_IntList deserialization of non-string raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(
            colander.Invalid, schema.deserialize, {'value': 42})

    def test_IntList_deserialize_integers_to_list(self):
        """_IntList deserialization of Fortran integers string is list
        """
        schema = self._make_schema()
        result = schema.deserialize({'value': '42 24'})
        self.assertEqual(result, {'value': [int(42), int(24)]})


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
    def _call_infile_to_yaml(self, *args):
        from ..SOG_infile_schema import infile_to_yaml
        return infile_to_yaml(*args)

    def test_infile_to_yaml_with_units(self):
        """infile_to_yaml returns expected result for element with units
        """
        from ..SOG_infile_schema import SOG_Infile
        from .. SOG_YAML_schema import YAML_Infile
        infile_schema = SOG_Infile().clone()
        infile_schema.children = [child for child in infile_schema.children
                                  if child.name == 'maxdepth']
        yaml_schema = YAML_Infile().clone()
        yaml_schema.children = [child for child in yaml_schema.children
                                if child.name == 'grid']
        grid_schema = yaml_schema.children[0]
        grid_schema.children = [child for child in grid_schema
                                if child.name == 'model_depth']
        infile_struct = {'maxdepth': {
            'value': 40, 'units': 'm',
            'description': 'depth of modelled domain'}}
        result = self._call_infile_to_yaml(
            yaml_schema, infile_schema, infile_struct)
        self.assertEqual(
            result,
            {'grid': {
                'model_depth': {
                    'value': 40, 'units': 'm', 'variable name': 'grid%D',
                    'description': 'depth of modelled domain'}}})

    def test_infile_to_yaml_without_units(self):
        """infile_to_yaml returns expected result for element without units
        """
        from ..SOG_infile_schema import SOG_Infile
        from .. SOG_YAML_schema import YAML_Infile
        infile_schema = SOG_Infile().clone()
        infile_schema.children = [child for child in infile_schema.children
                                  if child.name == 'gridsize']
        yaml_schema = YAML_Infile().clone()
        yaml_schema.children = [child for child in yaml_schema.children
                                if child.name == 'grid']
        grid_schema = yaml_schema.children[0]
        grid_schema.children = [child for child in grid_schema
                                if child.name == 'grid_size']
        infile_struct = {'gridsize': {
            'value': 80, 'units': None,
            'description': 'number of grid points'}}
        result = self._call_infile_to_yaml(
            yaml_schema, infile_schema, infile_struct)
        self.assertEqual(
            result,
            {'grid': {
                'grid_size': {
                    'value': 80, 'variable name': 'grid%M',
                    'description': 'number of grid points'}}})

    def test_infile_to_yaml_unnested_element(self):
        """infile_to_yaml returns expected result for unnested element
        """
        from ..SOG_infile_schema import SOG_Infile
        from .. SOG_YAML_schema import YAML_Infile
        infile_schema = SOG_Infile().clone()
        infile_schema.children = [child for child in infile_schema.children
                                  if child.name == 'end datetime']
        yaml_schema = YAML_Infile().clone()
        yaml_schema.children = [child for child in yaml_schema.children
                                if child.name == 'end_datetime']
        infile_struct = {'end datetime': {
            'value': datetime(2012, 4, 2, 19, 1), 'units': None,
            'description': 'end of run date/time'}}
        result = self._call_infile_to_yaml(
            yaml_schema, infile_schema, infile_struct)
        self.assertEqual(
            result,
            {'end_datetime': {
                'value': datetime(2012, 4, 2, 19, 1),
                'variable name': 'endDatetime',
                'description': 'end of run date/time'}})
