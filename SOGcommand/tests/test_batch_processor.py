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
        Mock,
        mock_open,
        patch,
    )
except ImportError:
    from mock import (
        Mock,
        mock_open,
        patch,
    )
import pytest
import six
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
    """Unit tests for batch_processor.build_jobs and its _job_or_default
    helper functions.
    """
    def _call_build_jobs(self, *args):
        return batch_processor.build_jobs(*args)

    def _call_job_or_default(self, *args, **kwargs):
        return batch_processor._job_or_default(*args, **kwargs)

    def test_jobname_set(self):
        """job name is set to job's key in config jobs list
        """
        job = {'foo': {}}
        config = {
            'SOG_executable': '../SOG-code/SOG',
            'base_infile': '../SOG-code/infile.yaml',
            'jobs': [job]
        }
        jobs = self._call_build_jobs(config)
        assert jobs[0].jobname == 'foo'

    def test_edit_files_list_initialized_empty(self):
        """edit files list initialized w/ empty list if not in defaults
        """
        job = {'foo': {}}
        config = {
            'SOG_executable': '../SOG-code/SOG',
            'base_infile': '../SOG-code/infile.yaml',
            'jobs': [job]
        }
        jobs = self._call_build_jobs(config)
        assert jobs[0].editfile == []

    def test_edit_files_list_initialized_w_default(self):
        """edit files list initialized w/ list from defaults
        """
        job = {'foo': {}}
        config = {
            'SOG_executable': '../SOG-code/SOG',
            'base_infile': '../SOG-code/infile.yaml',
            'edit_files': ['R3base.yaml'],
            'jobs': [job]
        }
        jobs = self._call_build_jobs(config)
        assert jobs[0].editfile == ['R3base.yaml']

    def test_job_edit_files_appended_to_list(self):
        """edit files list from job are appended to list from defaults
        """
        job = {
            'foo': {
                'edit_files': ['R3no_remin.yaml'],
            }}
        config = {
            'SOG_executable': '../SOG-code/SOG',
            'base_infile': '../SOG-code/infile.yaml',
            'edit_files': ['R3base.yaml'],
            'jobs': [job]
        }
        jobs = self._call_build_jobs(config)
        assert jobs[0].editfile == ['R3base.yaml', 'R3no_remin.yaml']

    def test_job_or_default_returns_default_value(self):
        """job without key gets default value
        """
        job = {'foo': {}}
        config = {
            'SOG_executable': '../SOG-code/SOG',
            'base_infile': '../SOG-code/infile.yaml',
            'jobs': [job]
        }
        value = self._call_job_or_default('foo', job, config, 'SOG_executable')
        assert value == '../SOG-code/SOG'

    def test_jobs_or_default_returns_job_value(self):
        """value from job with key overrides default
        """
        job = {'foo': {'SOG_executable': 'SOG'}}
        config = {
            'SOG_executable': '../SOG-code/SOG',
            'base_infile': '../SOG-code/infile.yaml',
            'jobs': [job]
        }
        value = self._call_job_or_default('foo', job, config, 'SOG_executable')
        assert value == 'SOG'

    def test_job_or_default_misssing_key_w_default(self):
        """missing key with default returns default value
        """
        job = {'foo': {}}
        config = {'jobs': [job]}
        value = self._call_job_or_default(
            'foo', job, config, 'nice', default=19)
        assert value == 19

    def test_job_or_default_misssing_key_wo_default(self):
        """missing key without default raises KeyError
        """
        job = {'foo': {}}
        config = {'jobs': [job]}
        with pytest.raises(KeyError):
            self._call_job_or_default('foo', job, config, 'SOG_executable')


class TestDryRun(object):
    """Unit tests for batch_processor.dry_run function.
    """
    @patch('sys.stdout', new_callable=six.StringIO)
    def test_dry_run_no_edit_files(self, mock_stdout):
        """dry run command for job without edit files has no -e options
        """
        jobs = [
            Mock(jobname='foo', SOG_exec='SOG', infile='infile.yaml',
                 editfile=[], nice=19)
        ]
        batch_processor.dry_run(jobs, 1)
        expected = '  foo: SOG run SOG infile.yaml --nice 19'
        assert expected in mock_stdout.getvalue()

    @patch('sys.stdout', new_callable=six.StringIO)
    def test_dry_run_edit_files(self, mock_stdout):
        """dry run command for job with edit files has -e option
        """
        jobs = [
            Mock(jobname='foo', SOG_exec='SOG', infile='infile.yaml',
                 editfile=['R3base.yaml'], nice=19)
        ]
        batch_processor.dry_run(jobs, 1)
        expected = '  foo: SOG run SOG infile.yaml -e R3base.yaml --nice 19'
        assert expected in mock_stdout.getvalue()

