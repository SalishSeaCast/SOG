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

    def _call_legacy_infile_default_rules(self, *args):
        return batch_processor._legacy_infile_default_rules(*args)

    def _call_legacy_infile_job_rules(self, *args):
        return batch_processor._legacy_infile_job_rules(*args)

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

    def test_outfile_from_config(self):
        """outfile name from job config
        """
        job = {
            'foo': {
                'edit_files': ['R3no_remin.yaml'],
                'outfile': '/foo/bar.yaml.out'
            }}
        config = {
            'SOG_executable': '../SOG-code/SOG',
            'base_infile': '../SOG-code/infile.yaml',
            'edit_files': ['R3base.yaml'],
            'jobs': [job]
        }
        jobs = self._call_build_jobs(config)
        assert jobs[0].outfile == '/foo/bar.yaml.out'

    def test_outfile_from_last_edit_file(self):
        """outfile is name of last edit file with .out appended
        """
        job = {
            'foo': {
                'edit_files': ['/foo/bar.yaml'],
            }}
        config = {
            'SOG_executable': '../SOG-code/SOG',
            'base_infile': '../SOG-code/infile.yaml',
            'edit_files': ['R3base.yaml.out'],
            'jobs': [job]
        }
        jobs = self._call_build_jobs(config)
        assert jobs[0].outfile == '/foo/bar.yaml.out'

    def test_outfile_from_base_infile(self):
        """outfile is base infile w/ .out appended if no edit files
        """
        job = {
            'foo': {}
        }
        config = {
            'SOG_executable': '../SOG-code/SOG',
            'base_infile': '/infile.yaml',
            'jobs': [job]
        }
        jobs = self._call_build_jobs(config)
        assert jobs[0].outfile == '/infile.yaml.out'

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

    def test_legacy_infile_default_false(self):
        """top level legacy_infile defaults to False
        """
        job = {
            'foo': {}
        }
        config = {
            'SOG_executable': '../SOG-code/SOG',
            'base_infile': '/infile.yaml',
            'jobs': [job]
        }
        legacy_infile = self._call_legacy_infile_default_rules(config)
        assert legacy_infile is False

    def test_legacy_infile_default_precludes_default_base_infile(self):
        """default base_infile with legacy_infile==True raises KeyError
        """
        job = {
            'foo': {}
        }
        config = {
            'SOG_executable': '../SOG-code/SOG',
            'base_infile': '/infile.yaml',
            'legacy_infile': True,
            'jobs': [job]
        }
        with pytest.raises(KeyError):
            self._call_legacy_infile_default_rules(config)

    def test_legacy_infile_default_precludes_default_edit_files(self):
        """default edit_files with legacy_infile==True raises KeyError
        """
        job = {
            'foo': {}
        }
        config = {
            'SOG_executable': '../SOG-code/SOG',
            'edit_files': ['R3base.yaml'],
            'legacy_infile': True,
            'jobs': [job]
        }
        with pytest.raises(KeyError):
            self._call_legacy_infile_default_rules(config)

    def test_legacy_infile_job_default_false(self):
        """job level legacy_infile defaults to False
        """
        job = {
            'foo': {}
        }
        legacy_infile = self._call_legacy_infile_job_rules('foo', job)
        assert legacy_infile is False

    def test_legacy_infile_job_base_infile_reqd(self):
        """job level legacy_infile==True means job base_infile is required
        """
        job = {
            'foo': {
                'legacy_infile': True,
            }
        }
        with pytest.raises(KeyError):
            self._call_legacy_infile_job_rules('foo', job)

    def test_legacy_infile_job_precludes_edit_files(self):
        """job level edit_files with legacy_infile==True raises KeyError
        """
        job = {
            'foo': {
                'legacy_infile': True,
                'base_infile': 'foo',
                'edit_files': ['bar']
            }
        }
        with pytest.raises(KeyError):
            self._call_legacy_infile_job_rules('foo', job)


class TestDryRun(object):
    """Unit tests for batch_processor.dry_run function.
    """
    @patch('sys.stdout', new_callable=six.StringIO)
    def test_dry_run_no_edit_files(self, mock_stdout):
        """dry run command for job without edit files has no -e options
        """
        jobs = [
            Mock(jobname='foo', SOG_exec='SOG', infile='infile.yaml',
                 editfile=[], outfile='infile.yaml.out', legacy_infile=False,
                 nice=19)
        ]
        batch_processor.dry_run(jobs, 1)
        expected = (
            '  foo: SOG run SOG infile.yaml -o infile.yaml.out --nice 19')
        assert expected in mock_stdout.getvalue()

    @patch('sys.stdout', new_callable=six.StringIO)
    def test_dry_run_edit_files(self, mock_stdout):
        """dry run command for job with edit files has -e option
        """
        jobs = [
            Mock(jobname='foo', SOG_exec='SOG', infile='infile.yaml',
                 editfile=['R3base.yaml'], outfile='R3base.yaml.out',
                 legacy_infile=False, nice=19)
        ]
        batch_processor.dry_run(jobs, 1)
        expected = (
            '  foo: SOG run SOG infile.yaml -e R3base.yaml -o R3base.yaml.out '
            '--nice 19')
        assert expected in mock_stdout.getvalue()

    @patch('sys.stdout', new_callable=six.StringIO)
    def test_dry_run_legacy_infile(self, mock_stdout):
        """legacy_infile option shown when True
        """
        jobs = [
            Mock(jobname='foo', SOG_exec='SOG', infile='infile',
                 editfile=[], outfile='infile.out', legacy_infile=True,
                 nice=19)
        ]
        batch_processor.dry_run(jobs, 1)
        expected = (
            '  foo: SOG run SOG infile -o infile.out --legacy_infile '
            '--nice 19')
        assert expected in mock_stdout.getvalue()
