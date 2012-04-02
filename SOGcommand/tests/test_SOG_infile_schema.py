"""Unit tests for SOG Fortran-ish infile schema and data structure
transformation function.
"""
import colander
from mock import Mock
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA


class TestRealDP(unittest.TestCase):
    """Unit tests for RealDP schema type.
    """
    def _make_schema(self):
        from ..SOG_infile_schema import _RealDP

        class Schema(colander.MappingSchema):
            value = colander.SchemaNode(_RealDP())
        return Schema()

    def test_RealDP_serialize_null(self):
        """RealDP serialization of null returns null
        """
        schema = self._make_schema()
        result = schema.serialize({'value': colander.null})
        self.assertEqual(result, {'value': colander.null})

    def test_RealDP_serialize_raises_invalid(self):
        """RealDP serialization of non-number raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(colander.Invalid, schema.serialize, {'value': 'foo'})

    def test_RealDP_serialize_e_format_with_d(self):
        """RealDP serialization of nummber is Fortran real(kind=dp) notation
        """
        schema = self._make_schema()
        result = schema.serialize({'value': 42})
        self.assertEqual(result, {'value': '4.200000d+01'})

    def test_RealDP_deserialize_null(self):
        """RealDP deserialization of null raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(
            colander.Invalid, schema.deserialize, {'value': colander.null})

    def test_RealDP_deserialize_raises_invalid(self):
        """RealDP deserialization of non-string raises Invalid exception
        """
        schema = self._make_schema()
        self.assertRaises(
            colander.Invalid, schema.deserialize, {'value': 42})

    def test_RealDP_deserialize_d_format_to_float(self):
        """RealDP deserialization of Fortran real(kind=dp) string is float
        """
        schema = self._make_schema()
        result = schema.deserialize({'value': '42.0d0'})
        self.assertEqual(result, {'value': 42.0})
        self.assertTrue(isinstance(result['value'], float))


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
        mock_node = Mock(spec=colander.SchemaNode)
        mock_node.configure_mock(name='grid')
        mock_child = Mock(spec=colander.SchemaNode)
        mock_child.configure_mock(
            name='model_depth', infile_key='maxdepth', var_name='grid%D')
        mock_node.children = [mock_child]
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
        mock_node = Mock(spec=colander.SchemaNode)
        mock_node.configure_mock(name='grid')
        mock_child = Mock(spec=colander.SchemaNode)
        mock_child.configure_mock(
            name='grid_size', infile_key='gridsize', var_name='grid%M')
        mock_node.children = [mock_child]
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
