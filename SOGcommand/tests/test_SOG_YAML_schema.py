"""Unit tests for SOG YAML infile schema and data structure
transformation function.
"""
import colander
from mock import Mock
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA


class TestYAMLtoInfile(unittest.TestCase):
    """Unit tests for yaml_to_infile data structure transformation function.
    """
    def _make_schema(self):
        from ..SOG_YAML_schema import YAML_Infile
        return YAML_Infile()

    def _call_yaml_to_infile(self, *args):
        from ..SOG_YAML_schema import yaml_to_infile
        return yaml_to_infile(*args)

    def test_yaml_to_infile(self):
        """yaml_to_infile returns expected result
        """
        mock_node = Mock(spec=colander.SchemaNode)
        mock_node.configure_mock(name='grid')
        mock_child = Mock(spec=colander.SchemaNode)
        mock_child.configure_mock(
            name='model_depth', infile_key='maxdepth', var_name='grid%D')
        mock_node.children = [mock_child]
        nodes = [mock_node]
        schema = self._make_schema()
        yaml_struct = {'grid': {
                'model_depth': {
                    'value': 40, 'units': 'm', 'variable name': 'grid%D',
                    'description': 'depth of modelled domain'}}}
        result = self._call_yaml_to_infile(nodes, schema, yaml_struct)
        self.assertEqual(
            result,
            {'maxdepth': {
                'value': 40, 'units': 'm',
                'description': 'depth of modelled domain'}})
