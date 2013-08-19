"""Unit tests for SOG batch processor.

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
try:
    from unittest.mock import (
        mock_open,
        patch,
    )
except ImportError:
    from mock import (
        mock_open,
        patch,
    )
import pytest
from .. import batch_processor


class TestReadConfig(object):
    """Unit tests for batch_processor.read_config function.
    """
    def _call_read_config(self, *args):
        return batch_processor.read_config(*args)

    @patch.object(batch_processor.os.path, 'exists', return_value=False)
    def test_batchfile_not_found(self, mock_os):
        """IOError raised if batchfile doesn't exist
        """
        with pytest.raises(IOError):
            self._call_read_config('foo')

    @patch.object(batch_processor.os.path, 'exists', return_value=True)
    def test_returns_config_dict(self, mock_os):
        """config is returned as a dict
        """
        m = mock_open(read_data='foo: bar')
        with patch.object(batch_processor, 'open', m, create=True):
            config = self._call_read_config('foo')
        assert isinstance(config, dict)

    @patch.object(batch_processor.os.path, 'exists', return_value=True)
    def test_max_concurrent_jobs_default(self, mock_os):
        """max_concurrent_jobs defaults to 1
        """
        m = mock_open(read_data='foo: bar')
        with patch.object(batch_processor, 'open', m, create=True):
            config = self._call_read_config('foo')
        assert config['max_concurrent_jobs'] == 1

    @patch.object(batch_processor.os.path, 'exists', return_value=True)
    def test_max_concurrent_jobs_value(self, mock_os):
        """max_concurrent_jobs value is read from file
        """
        m = mock_open(read_data='max_concurrent_jobs: 16')
        with patch.object(batch_processor, 'open', m, create=True):
            config = self._call_read_config('foo')
        assert config['max_concurrent_jobs'] == 16


class TestBuildJobs(object):
    """Unit tests for batch_processor.build_jobs function.
    """
    def _call_build_jobs(self, *args):
        return batch_processor.build_jobs(*args)

    def test_default_SOG_executable(self):
        """job w/o SOG executable gets default one
        """
        config = {
            'SOG_executable': '../SOG-code/SOG',
            'jobs': [
                {
                    'foo': {}
                }
            ]
        }
        jobs = self._call_build_jobs(config)
        assert jobs[0].SOG_exec == '../SOG-code/SOG'

    def test_job_SOG_executable(self):
        """job w/ SOG executable overrides default
        """
        config = {
            'SOG_executable': '../SOG-code/SOG',
            'jobs': [
                {
                    'foo': {
                        'SOG_executable': 'SOG',
                    }
                }
            ]
        }
        jobs = self._call_build_jobs(config)
        assert jobs[0].SOG_exec == 'SOG'

    def test_misssing_SOG_executable(self):
        """missing SOG executable raises ValueError
        """
        config = {
            'jobs': [
                {
                    'foo': {}
                }
            ]
        }
        with pytest.raises(KeyError):
            self._call_build_jobs(config)
