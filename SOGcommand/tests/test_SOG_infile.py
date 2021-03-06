# -*- coding: utf-8 -*-
"""Unit tests for SOG infile parser and emitter.

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
import six
import unittest


class TestLoad(unittest.TestCase):
    """Unit tests for SOG infile parser.
    """
    def _call_load(self, stream):
        from ..SOG_infile import load
        return load(stream)

    def test_load_empty_strem_empty_dict(self):
        """load of empty stream returns empty dict
        """
        stream = six.StringIO('')
        result = self._call_load(stream)
        self.assertEqual(result, {})

    def test_load_1_line(self):
        """load returns expected dict for 1 SOG infile line
        """
        stream = six.StringIO(
            '"maxdepth"  40.0d0  "depth of modelled domain [m]"')
        result = self._call_load(stream)
        self.assertEqual(
            result,
            {'maxdepth': {'value': '40.0d0',
                          'description': 'depth of modelled domain',
                          'units': 'm'}})

    def test_load_ignores_comment(self):
        """load ignores line starting with ! as comment
        """
        stream = six.StringIO(
            '! This is a comment\n'
            '"maxdepth"  40.0d0  "depth of modelled domain [m]"')
        result = self._call_load(stream)
        self.assertEqual(
            result,
            {'maxdepth': {'value': '40.0d0',
                          'description': 'depth of modelled domain',
                          'units': 'm'}})

    def test_load_ignores_empty_line(self):
        """load ignores empty line
        """
        stream = six.StringIO(
            '! This is a comment\n'
            '\n'
            '"maxdepth"  40.0d0  "depth of modelled domain [m]"')
        result = self._call_load(stream)
        self.assertEqual(
            result,
            {'maxdepth': {'value': '40.0d0',
                          'description': 'depth of modelled domain',
                          'units': 'm'}})

    def test_load_2_lines(self):
        """load returns expected dict for 2 SOG infile lines
        """
        stream = six.StringIO(
            '"maxdepth"  40.0d0  "depth of modelled domain [m]"\n'
            '"gridsize"  80  "number of grid points"')
        result = self._call_load(stream)
        self.assertEqual(
            result,
            {'maxdepth': {'value': '40.0d0',
                          'description': 'depth of modelled domain',
                          'units': 'm'},
             'gridsize': {'value': '80',
                          'description': 'number of grid points',
                          'units': None}})

    def test_load_newline_after_key(self):
        """load handles SOG infile w/ newline between key and value
        """
        stream = six.StringIO(
            '"maxdepth"\n'
            '  40.0d0  "depth of modelled domain [m]"')
        result = self._call_load(stream)
        self.assertEqual(
            result,
            {'maxdepth': {'value': '40.0d0',
                          'description': 'depth of modelled domain',
                          'units': 'm'}})

    def test_load_newline_after_value(self):
        """load handles SOG infile w/ newline between value and description
        """
        stream = six.StringIO(
            '"maxdepth"  40.0d0\n'
            '  "depth of modelled domain [m]"')
        result = self._call_load(stream)
        self.assertEqual(
            result,
            {'maxdepth': {'value': '40.0d0',
                          'description': 'depth of modelled domain',
                          'units': 'm'}})

    def test_load_newlines_after_key_and_value(self):
        """load handles SOG infile w/ newlines b/t key, value and description
        """
        stream = six.StringIO(
            '"maxdepth"\n'
            '  40.0d0\n'
            '  "depth of modelled domain [m]"')
        result = self._call_load(stream)
        self.assertEqual(
            result,
            {'maxdepth': {'value': '40.0d0',
                          'description': 'depth of modelled domain',
                          'units': 'm'}})


class TestDump(unittest.TestCase):
    """Unit tests for SOG infile emitter.
    """
    def _call_dump(self, *args):
        from ..SOG_infile import dump
        return dump(*args)

    def test_dump_line_w_units(self):
        """dump produces expected line for data structure w/ units
        """
        data = {
            'maxdepth': {
                'value': '40.0d0', 'description': 'depth of modelled domain',
                'units': 'm'}}
        key_order = ['maxdepth']
        extra_keys = {}
        avg_hist_forcing_keys = {}
        stream = six.StringIO()
        self._call_dump(
            data, key_order, extra_keys, avg_hist_forcing_keys, stream)
        self.assertEqual(
            stream.getvalue(),
            '"maxdepth"  40.0d0  "depth of modelled domain [m]"\n')

    def test_dump_line_wo_units(self):
        """dump produces expected line for data structure w/o units
        """
        data = {
            'gridsize': {
                'value': '80', 'description': 'number of grid points',
                'units': 'None'}}
        key_order = ['gridsize']
        extra_keys = {}
        avg_hist_forcing_keys = {}
        stream = six.StringIO()
        self._call_dump(
            data, key_order, extra_keys, avg_hist_forcing_keys, stream)
        self.assertEqual(
            stream.getvalue(), '"gridsize"  80  "number of grid points"\n')

    def test_dump_line_order(self):
        """dump produces lines in correct order
        """
        data = {
            'gridsize': {
                'value': '80', 'description': 'number of grid points',
                'units': 'None'},
            'maxdepth': {
                'value': '40.0d0', 'description': 'depth of modelled domain',
                'units': 'm'}}
        key_order = 'maxdepth gridsize'.split()
        extra_keys = {}
        avg_hist_forcing_keys = {}
        stream = six.StringIO()
        self._call_dump(
            data, key_order, extra_keys, avg_hist_forcing_keys, stream)
        self.assertEqual(
            stream.getvalue(),
            '"maxdepth"  40.0d0  "depth of modelled domain [m]"\n'
            '"gridsize"  80  "number of grid points"\n')

    def test_dump_line_length_limit(self):
        """dump breaks values list so that line length < 240
        """
        import colander
        data = {
            'profile_times': {
                'value': '46200. 43620. 40860. 40800. 41400. 41400. 40680. '
                         '50880. 44280. 47100. 45780. 44880. 44460. 44040. '
                         '40800. 40260. 40980. 49500. 37620. 39600. 38520. '
                         '42420. 41760. 42120. 43020. 42600. 43620. 48480. '
                         '42360. 48120. 34560. 48300. 64920. 24600. 21240. '
                         '43800. 40620. 44520. 42900. 40380. 43260. 41760. '
                         '40860. 48300. 53100. 38580. 37620. 36840.',
                'description': 'list of day-seconds to output profiles for',
                'units': colander.null}}
        key_order = ['profile_times']
        extra_keys = {}
        avg_hist_forcing_keys = {}
        stream = six.StringIO()
        self._call_dump(
            data, key_order, extra_keys, avg_hist_forcing_keys, stream)
        for line in stream.getvalue().split('\n'):
            self.assertLessEqual(len(line), 240)

    def test_dump_long_line_key_first(self):
        """dump starts broken long line with key
        """
        import colander
        data = {
            'profile_times': {
                'value': '46200. 43620. 40860. 40800. 41400. 41400. 40680. '
                         '50880. 44280. 47100. 45780. 44880. 44460. 44040. '
                         '40800. 40260. 40980. 49500. 37620. 39600. 38520. '
                         '42420. 41760. 42120. 43020. 42600. 43620. 48480. '
                         '42360. 48120. 34560. 48300. 64920. 24600. 21240. '
                         '43800. 40620. 44520. 42900. 40380. 43260. 41760. '
                         '40860. 48300. 53100. 38580. 37620. 36840.',
                'description': 'list of day-seconds to output profiles for',
                'units': colander.null}}
        key_order = ['profile_times']
        extra_keys = {}
        avg_hist_forcing_keys = {}
        stream = six.StringIO()
        self._call_dump(
            data, key_order, extra_keys, avg_hist_forcing_keys, stream)
        self.assertEqual(stream.getvalue().split('\n')[0], '"profile_times"')

    def test_dump_long_line_value_per_line(self):
        """dump prints long line values 1 per line
        """
        import colander
        data = {
            'profile_times': {
                'value': '46200. 43620. 40860. 40800. 41400. 41400. 40680. '
                         '50880. 44280. 47100. 45780. 44880. 44460. 44040. '
                         '40800. 40260. 40980. 49500. 37620. 39600. 38520. '
                         '42420. 41760. 42120. 43020. 42600. 43620. 48480. '
                         '42360. 48120. 34560. 48300. 64920. 24600. 21240. '
                         '43800. 40620. 44520. 42900. 40380. 43260. 41760. '
                         '40860. 48300. 53100. 38580. 37620. 36840.',
                'description': 'list of day-seconds to output profiles for',
                'units': colander.null}}
        key_order = ['profile_times']
        extra_keys = {}
        avg_hist_forcing_keys = {}
        stream = six.StringIO()
        self._call_dump(
            data, key_order, extra_keys, avg_hist_forcing_keys, stream)
        self.assertEqual(stream.getvalue().split('\n')[1], '  46200.')

    def test_dump_long_line_description_last(self):
        """dump ends broken long line with description
        """
        data = {
            'profile_times': {
                'value': '46200. 43620. 40860. 40800. 41400. 41400. 40680. '
                         '50880. 44280. 47100. 45780. 44880. 44460. 44040. '
                         '40800. 40260. 40980. 49500. 37620. 39600. 38520. '
                         '42420. 41760. 42120. 43020. 42600. 43620. 48480. '
                         '42360. 48120. 34560. 48300. 64920. 24600. 21240. '
                         '43800. 40620. 44520. 42900. 40380. 43260. 41760. '
                         '40860. 48300. 53100. 38580. 37620. 36840.',
                'description': 'list of day-seconds to output profiles for',
                'units': 'None'}}
        key_order = ['profile_times']
        extra_keys = {}
        avg_hist_forcing_keys = {}
        stream = six.StringIO()
        self._call_dump(
            data, key_order, extra_keys, avg_hist_forcing_keys, stream)
        self.assertEqual(
            stream.getvalue().split('\n')[-2],
            '  "list of day-seconds to output profiles for"')

    def test_dump_extra_keys(self):
        """dump handles extra keys for optional parameters
        """
        data = {
            'northern_return_flow': {
                'value': '.true.',
                'description': 'include fresh water return flow from north?',
                'units': 'None'},
            'northern_influence_strength': {
                'value': '0.8863d0',
                'description': 'strength of northen influence',
                'units': 'm'}}
        key_order = ['northern_return_flow']
        extra_keys = {
            'northern_return_flow': {
                '.true.': ['northern_influence_strength'],
                '.false.': []}
        }
        avg_hist_forcing_keys = {}
        stream = six.StringIO()
        self._call_dump(
            data, key_order, extra_keys, avg_hist_forcing_keys, stream)
        self.assertEqual(
            stream.getvalue(),
            '"northern_return_flow"  .true.  '
            '"include fresh water return flow from north?"\n'
            '"northern_influence_strength"  0.8863d0  '
            '"strength of northen influence [m]"\n')

    def test_avg_hist_forcing_keys(self):
        """dump handles average/historical forcing keys for optional parameters
        """
        data = {
            'use average/hist forcing': {
                'value': '"yes"',
                'description': 'yes=avg only; no=fail if data runs out; '
                'fill=historic then avg',
                'units': 'None'},
            'average/hist wind': {
                'value': '"../SOG-forcing/wind/SHavg"',
                'description': 'average wind forcing data',
                'units': 'None'},
            'wind': {
                'value': '"Sandheads_wind"',
                'description': 'wind forcing data',
                'units': 'None'},
        }
        key_order = ['use average/hist forcing', 'wind']
        extra_keys = {}
        avg_hist_forcing_keys = {
            'wind': {
                'trigger': 'use average/hist forcing',
                'yes': ['average/hist wind'],
                'no': [],
                'fill': ['average/hist wind'],
                'histfill': ['average/hist wind'],
            }}
        stream = six.StringIO()
        self._call_dump(
            data, key_order, extra_keys, avg_hist_forcing_keys, stream)
        self.assertEqual(
            stream.getvalue(),
            '"use average/hist forcing"  "yes"  '
            '"yes=avg only; no=fail if data runs out; fill=historic then '
            'avg"\n'
            '"average/hist wind"  "../SOG-forcing/wind/SHavg"  '
            '"average wind forcing data"\n'
            '"wind"  "Sandheads_wind"  "wind forcing data"\n')
