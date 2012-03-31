"""Unit tests for SOG infile parser and emitter.
"""
from StringIO import StringIO
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA


class TestLoad(unittest.TestCase):
    """Unit tests for SOG infile parser.
    """
    def _call_load(self, stream):
        from ..SOG_infile import load
        return load(stream)

    def test_load_empty_strem_empty_dict(self):
        """load of empty stream returns empty dict
        """
        stream = StringIO('')
        result = self._call_load(stream)
        self.assertEqual(result, {})

    def test_load_1_line(self):
        """load returns expected dict for 1 SOG infile line
        """
        stream = StringIO(
            '"maxdepth"  40.0d0  "depth of modelled domain [m]"')
        result = self._call_load(stream)
        self.assertEqual(
        result, {'maxdepth': {'value': '40.0d0',
                              'description': 'depth of modelled domain',
                              'units': 'm'}})

    def test_load_ignores_comment(self):
        """load ignores line starting with ! as comment
        """
        stream = StringIO(
            '! This is a comment\n'
            '"maxdepth"  40.0d0  "depth of modelled domain [m]"')
        result = self._call_load(stream)
        self.assertEqual(
        result, {'maxdepth': {'value': '40.0d0',
                              'description': 'depth of modelled domain',
                              'units': 'm'}})

    def test_load_ignores_empty_line(self):
        """load ignores empty line
        """
        stream = StringIO(
            '! This is a comment\n'
            '\n'
            '"maxdepth"  40.0d0  "depth of modelled domain [m]"')
        result = self._call_load(stream)
        self.assertEqual(
        result, {'maxdepth': {'value': '40.0d0',
                              'description': 'depth of modelled domain',
                              'units': 'm'}})

    def test_load_2_lines(self):
        """load returns expected dict for 2 SOG infile lines
        """
        stream = StringIO(
            '"maxdepth"  40.0d0  "depth of modelled domain [m]"\n'
            '"gridsize"  80  "number of grid points"')
        result = self._call_load(stream)
        self.assertEqual(
        result, {'maxdepth': {'value': '40.0d0',
                              'description': 'depth of modelled domain',
                              'units': 'm'},
                 'gridsize': {'value': '80',
                              'description': 'number of grid points',
                              'units': None}})

    def test_load_newline_after_key(self):
        """load handles SOG infile w/ newline between key and value
        """
        stream = StringIO(
            '"maxdepth"\n'
            '  40.0d0  "depth of modelled domain [m]"')
        result = self._call_load(stream)
        self.assertEqual(
        result, {'maxdepth': {'value': '40.0d0',
                              'description': 'depth of modelled domain',
                              'units': 'm'}})

    def test_load_newline_after_value(self):
        """load handles SOG infile w/ newline between value and description
        """
        stream = StringIO(
            '"maxdepth"  40.0d0\n'
            '  "depth of modelled domain [m]"')
        result = self._call_load(stream)
        self.assertEqual(
        result, {'maxdepth': {'value': '40.0d0',
                              'description': 'depth of modelled domain',
                              'units': 'm'}})

    def test_load_newlines_after_key_and_value(self):
        """load handles SOG infile w/ newlines b/t key, value and description
        """
        stream = StringIO(
            '"maxdepth"\n'
            '  40.0d0\n'
            '  "depth of modelled domain [m]"')
        result = self._call_load(stream)
        self.assertEqual(
        result, {'maxdepth': {'value': '40.0d0',
                              'description': 'depth of modelled domain',
                              'units': 'm'}})
