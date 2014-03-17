"""Unit tests for SOG batch processor.

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
from .. import batch_processor


class TestJob(object):
    """Unit tests for SOG Job object.
    """
    def _get_target_class(self):
        from ..batch_processor import Job
        return Job

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_job_defaults(self):
        """Job instance has expected default attribute values
        """
        job = self._make_one(
            'jobname', 'SOG executable', 'infile', 'edit_files', 'outfile')
        assert job.nice is 19
        assert job.legacy_infile is False
        assert job.dry_run is False
        assert job.process is None
        assert job.pid is None
        assert job.returncode is None

    @patch('SOGcommand.batch_processor.run_processor.prepare')
    @patch('SOGcommand.batch_processor.subprocess.Popen')
    def test_job_start_prepares_command(self, mock_popen, mock_prepare):
        """job.start calls run_processor.prepare with job instance as arg
        """
        job = self._make_one(
            'jobname', 'SOG executable', 'infile', 'edit_files', 'outfile')
        job.start()
        mock_prepare.assert_called_once_with(job)

    @patch('SOGcommand.batch_processor.run_processor.prepare')
    @patch('SOGcommand.batch_processor.subprocess.Popen')
    def test_job_start_spawns_subprocess(self, mock_popen, mock_prepare):
        """job.start spawns subprocess to run SOG job & caches process info
        """
        mock_prepare.return_value = 'cmd'
        mock_process = Mock('process', pid=12345)
        mock_popen.return_value = mock_process
        job = self._make_one(
            'jobname', 'SOG executable', 'infile', 'edit_files', 'outfile')
        job.start()
        mock_popen.assert_called_once_with('cmd', shell=True)
        assert job.process == mock_process
        assert job.pid == mock_process.pid

    def test_job_not_done(self):
        """job.done polls job, caches returncode & returns False when not done
        """
        job = self._make_one(
            'jobname', 'SOG executable', 'infile', 'edit_files', 'outfile')
        job.process = Mock('process', poll=Mock(return_value=None))
        result = job.done
        assert job.process.poll.called
        assert result is False
        assert job.returncode is None

    def test_job_done(self):
        """job.done polls job, caches returncode & returns True when job done
        """
        job = self._make_one(
            'jobname', 'SOG executable', 'infile', 'edit_files', 'outfile')
        job.process = Mock('process', poll=Mock(return_value=0))
        result = job.done
        assert job.process.poll.called
        assert result is True
        assert job.returncode is 0


class TestBatchProcessorInit(object):
    """Unit tests for BatchProcessor instance initialization.
    """
    def _get_target_class(self):
        from ..batch_processor import BatchProcessor
        return BatchProcessor

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_init_defaults(self):
        """BatchProcessor instance has expected default attribute values
        """
        batch = self._make_one('batchfile')
        assert batch.batchfile is 'batchfile'
        assert batch.max_concurrent_jobs is 1

    @patch('SOGcommand.batch_processor.log')
    def test_init_debug_sets_logging_level(self, mock_log):
        """debug==True sets logging level to logging.DEBUG
        """
        import logging
        self._make_one('batchfile', debug=True)
        mock_log.setLevel.assert_called_once_with(logging.DEBUG)


class TestBatchProcessorPrepare(object):
    """Unit tests for BatchProcessor prepare method and its helpers.
    """
    def _get_target_class(self):
        from ..batch_processor import BatchProcessor
        return BatchProcessor

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    @patch('SOGcommand.batch_processor.os.path.exists', return_value=False)
    def test_batchfile_not_found(self, mock_os):
        """IOError raised if batchfile doesn't exist
        """
        batch = self._make_one('batchfile')
        with pytest.raises(IOError):
            batch.prepare()

    @patch('SOGcommand.batch_processor.os.path.exists', return_value=True)
    def test_read_config_sets_config_attr_dict(self, mock_os):
        """_read_config sets config attribute w/ data from batchfile
        """
        batch = self._make_one('batchfile')
        m = mock_open(read_data='foo: bar')
        with patch('SOGcommand.batch_processor.open', m, create=True):
            batch._read_config()
        assert batch.config == {'foo': 'bar'}

    @patch('SOGcommand.batch_processor.os.path.exists', return_value=True)
    def test_max_concurrent_jobs_value(self, mock_os):
        """max_concurrent_jobs value is read from file
        """
        batch = self._make_one('batchfile')
        m = mock_open(read_data='max_concurrent_jobs: 16')
        with patch('SOGcommand.batch_processor.open', m, create=True):
            batch._read_config()
        assert batch.max_concurrent_jobs is 16

    def test_jobname_set(self):
        """job name is set to job's key in config jobs list
        """
        batch = self._make_one('batchfile')
        job = {'foo': {}}
        batch.config = {
            'SOG_executable': '../SOG-code/SOG',
            'base_infile': '../SOG-code/infile.yaml',
            'jobs': [job]
        }
        batch._build_jobs()
        assert batch.jobs[0].jobname == 'foo'

    def test_edit_files_list_initialized_empty(self):
        """edit files list initialized w/ empty list if not in defaults
        """
        batch = self._make_one('batchfile')
        job = {'foo': {}}
        batch.config = {
            'SOG_executable': '../SOG-code/SOG',
            'base_infile': '../SOG-code/infile.yaml',
            'jobs': [job]
        }
        batch._build_jobs()
        assert batch.jobs[0].editfile == []

    def test_edit_files_list_initialized_w_default(self):
        """edit files list initialized w/ list from defaults
        """
        batch = self._make_one('batchfile')
        job = {'foo': {}}
        batch.config = {
            'SOG_executable': '../SOG-code/SOG',
            'base_infile': '../SOG-code/infile.yaml',
            'edit_files': ['R3base.yaml'],
            'jobs': [job]
        }
        batch._build_jobs()
        assert batch.jobs[0].editfile == ['R3base.yaml']

    def test_job_edit_files_appended_to_list(self):
        """edit files list from job are appended to list from defaults
        """
        batch = self._make_one('batchfile')
        job = {
            'foo': {
                'edit_files': ['R3no_remin.yaml'],
            }}
        batch.config = {
            'SOG_executable': '../SOG-code/SOG',
            'base_infile': '../SOG-code/infile.yaml',
            'edit_files': ['R3base.yaml'],
            'jobs': [job]
        }
        batch._build_jobs()
        assert batch.jobs[0].editfile == ['R3base.yaml', 'R3no_remin.yaml']

    def test_outfile_from_config(self):
        """outfile name from job config
        """
        batch = self._make_one('batchfile')
        job = {
            'foo': {
                'edit_files': ['R3no_remin.yaml'],
                'outfile': '/foo/bar.yaml.out'
            }}
        batch.config = {
            'SOG_executable': '../SOG-code/SOG',
            'base_infile': '../SOG-code/infile.yaml',
            'edit_files': ['R3base.yaml'],
            'jobs': [job]
        }
        batch._build_jobs()
        assert batch.jobs[0].outfile == '/foo/bar.yaml.out'

    def test_outfile_from_last_edit_file(self):
        """outfile is name of last edit file with .out appended
        """
        batch = self._make_one('batchfile')
        job = {
            'foo': {
                'edit_files': ['/foo/bar.yaml'],
            }}
        batch.config = {
            'SOG_executable': '../SOG-code/SOG',
            'base_infile': '../SOG-code/infile.yaml',
            'edit_files': ['R3base.yaml'],
            'jobs': [job]
        }
        batch._build_jobs()
        assert batch.jobs[0].outfile == '/foo/bar.yaml.out'

    def test_outfile_from_base_infile(self):
        """outfile is base infile w/ .out appended if no edit files
        """
        batch = self._make_one('batchfile')
        job = {
            'foo': {}
        }
        batch.config = {
            'SOG_executable': '../SOG-code/SOG',
            'base_infile': '/infile.yaml',
            'jobs': [job]
        }
        batch._build_jobs()
        assert batch.jobs[0].outfile == '/infile.yaml.out'

    def test_job_or_default_returns_top_level_value(self):
        """job without key gets top level value
        """
        batch = self._make_one('batchfile')
        job = {'foo': {}}
        batch.config = {
            'SOG_executable': '../SOG-code/SOG',
            'base_infile': '../SOG-code/infile.yaml',
            'jobs': [job]
        }
        value = batch._job_or_default('foo', job, 'SOG_executable')
        assert value is '../SOG-code/SOG'

    def test_jobs_or_default_returns_job_value(self):
        """value from job with key overrides default
        """
        batch = self._make_one('batchfile')
        job = {'foo': {'SOG_executable': 'SOG'}}
        batch.config = {
            'SOG_executable': '../SOG-code/SOG',
            'base_infile': '../SOG-code/infile.yaml',
            'jobs': [job]
        }
        value = batch._job_or_default('foo', job, 'SOG_executable')
        assert value is 'SOG'

    def test_job_or_default_misssing_key_w_default(self):
        """missing key with default returns default value
        """
        batch = self._make_one('batchfile')
        job = {'foo': {}}
        batch.config = {'jobs': [job]}
        value = batch._job_or_default('foo', job, 'nice', default=19)
        assert value is 19

    def test_job_or_default_misssing_key_wo_default(self):
        """missing key without default raises KeyError
        """
        batch = self._make_one('batchfile')
        job = {'foo': {}}
        batch.config = {'jobs': [job]}
        with pytest.raises(KeyError):
            batch._job_or_default('foo', job, 'SOG_executable')

    def test_legacy_infile_default_false(self):
        """top level legacy_infile defaults to False
        """
        batch = self._make_one('batchfile')
        job = {'foo': {}}
        batch.config = {
            'SOG_executable': '../SOG-code/SOG',
            'base_infile': '../SOG-code/infile.yaml',
            'jobs': [job]
        }
        legacy_infile = batch._legacy_infile_default_rules()
        assert legacy_infile is False

    def test_legacy_infile_default_precludes_default_base_infile(self):
        """default base_infile with legacy_infile==True raises KeyError
        """
        batch = self._make_one('batchfile')
        job = {'foo': {}}
        batch.config = {
            'SOG_executable': '../SOG-code/SOG',
            'base_infile': '/infile.yaml',
            'legacy_infile': True,
            'jobs': [job]
        }
        with pytest.raises(KeyError):
            batch._legacy_infile_default_rules()

    def test_legacy_infile_default_precludes_default_edit_files(self):
        """default edit_files with legacy_infile==True raises KeyError
        """
        batch = self._make_one('batchfile')
        job = {'foo': {}}
        batch.config = {
            'SOG_executable': '../SOG-code/SOG',
            'edit_files': ['R3base.yaml'],
            'legacy_infile': True,
            'jobs': [job]
        }
        with pytest.raises(KeyError):
            batch._legacy_infile_default_rules()

    def test_legacy_infile_job_default_false(self):
        """job level legacy_infile defaults to False
        """
        batch = self._make_one('batchfile')
        job = {'foo': {}}
        legacy_infile = batch._legacy_infile_job_rules('foo', job)
        assert legacy_infile is False

    def test_legacy_infile_job_base_infile_reqd(self):
        """job level legacy_infile==True means job base_infile is required
        """
        batch = self._make_one('batchfile')
        job = {
            'foo': {
                'legacy_infile': True,
            }
        }
        with pytest.raises(KeyError):
            batch._legacy_infile_job_rules('foo', job)

    def test_legacy_infile_job_precludes_edit_files(self):
        """job level edit_files with legacy_infile==True raises KeyError
        """
        batch = self._make_one('batchfile')
        job = {
            'foo': {
                'legacy_infile': True,
                'base_infile': 'foo',
                'edit_files': ['bar']
            }
        }
        with pytest.raises(KeyError):
            batch._legacy_infile_job_rules('foo', job)


class TestBatchProcessorRun(object):
    """Unit tests for BatchProcessor run method and its helpers.
    """
    def _get_target_class(self):
        from ..batch_processor import BatchProcessor
        return BatchProcessor

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_dry_run(self):
        """dry_run=True calls _dry_run method & returns 0
        """
        batch = self._make_one('batchfile')
        mock_dry_run = Mock()
        batch._dry_run = mock_dry_run
        returncode = batch.run(dry_run=True)
        assert mock_dry_run.called
        assert returncode is 0

    def test_dry_run_no_edit_files(self, capsys):
        """dry run command for job without edit files has no -e options
        """
        batch = self._make_one('batchfile')
        batch.jobs = [
            Mock(jobname='foo', SOG_exec='SOG', infile='infile.yaml',
                 editfile=[], outfile='infile.yaml.out', legacy_infile=False,
                 nice=19)
        ]
        batch._dry_run()
        expected = (
            '  foo: SOG run SOG infile.yaml -o infile.yaml.out --nice 19')
        assert expected in capsys.readouterr()[0]

    def test_dry_run_edit_files(self, capsys):
        """dry run command for job with edit files has -e option
        """
        batch = self._make_one('batchfile')
        batch.jobs = [
            Mock(jobname='foo', SOG_exec='SOG', infile='infile.yaml',
                 editfile=['R3base.yaml'], outfile='R3base.yaml.out',
                 legacy_infile=False, nice=19)
        ]
        batch._dry_run()
        expected = (
            '  foo: SOG run SOG infile.yaml -e R3base.yaml -o R3base.yaml.out '
            '--nice 19')
        assert expected in capsys.readouterr()[0]

    def test_dry_run_legacy_infile(self, capsys):
        """legacy_infile option shown when True
        """
        batch = self._make_one('batchfile')
        batch.jobs = [
            Mock(jobname='foo', SOG_exec='SOG', infile='infile',
                 editfile=[], outfile='infile.out', legacy_infile=True,
                 nice=19)
        ]
        batch._dry_run()
        expected = (
            '  foo: SOG run SOG infile -o infile.out --legacy_infile '
            '--nice 19')
        assert expected in capsys.readouterr()[0]

    def test_launch_initial_jobs(self):
        """launch allowed number of jobs & move them from jobs to in_progress
        """
        mock_job_1 = Mock(spec=batch_processor.Job, pid=123)
        mock_job_2 = Mock(spec=batch_processor.Job, pid=456)
        mock_job_3 = Mock(spec=batch_processor.Job, pid=789)
        batch = self._make_one('batchfile')
        batch.max_concurrent_jobs = 2
        batch.jobs = [mock_job_1, mock_job_2, mock_job_3]
        batch._launch_initial_jobs()
        assert batch.in_progress == {123: mock_job_1, 456: mock_job_2}
        assert mock_job_1.start.called
        assert mock_job_2.start.called
        assert batch.jobs == [mock_job_3]
        assert mock_job_3.start.called is False

    def test_launch_initial_jobs_excess_capacity(self):
        """launch all jobs when allowed number exceeds number of jobs
        """
        mock_job_1 = Mock(spec=batch_processor.Job, pid=123)
        mock_job_2 = Mock(spec=batch_processor.Job, pid=456)
        batch = self._make_one('batchfile')
        batch.max_concurrent_jobs = 4
        batch.jobs = [mock_job_1, mock_job_2]
        batch._launch_initial_jobs()
        assert batch.in_progress == {123: mock_job_1, 456: mock_job_2}
        assert mock_job_1.start.called
        assert mock_job_2.start.called
        assert batch.jobs == []

    def test_poll_and_launch(self):
        """when a job finishes capture its returncode & launch a new job
        """
        mock_job_1 = Mock(spec=batch_processor.Job, pid=123, done=False)
        mock_job_2 = Mock(
            spec=batch_processor.Job, pid=456, done=True, returncode=2)
        mock_job_3 = Mock(spec=batch_processor.Job, pid=789)
        batch = self._make_one('batchfile')
        batch.max_concurrent_jobs = 2
        batch.jobs = [mock_job_3]
        batch.in_progress = {123: mock_job_1, 456: mock_job_2}
        batch._poll_and_launch()
        assert batch.returncode is 2
        assert batch.in_progress == {123: mock_job_1, 789: mock_job_3}
        assert mock_job_3.start.called
        assert batch.jobs == []
