# -*- coding: utf-8 -*-
"""SOG batch processor.

Do various operations related to running batch jobs of the SOG bio-physical
model of deep estuaries.

This module provides services to the SOG command processor.

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
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
import logging
import os
import subprocess
import sys
from textwrap import TextWrapper
import time
import six
import yaml
from . import run_processor


__all__ = ['BatchProcessor', 'Job']


log = logging.getLogger('batch')
log.setLevel(logging.INFO)
console = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s [%(levelname)-5s] %(message)s', '%Y-%m-%d %H:%M:%S')
console.setFormatter(formatter)
log.addHandler(console)


class Job(object):
    """SOG job object.

    :arg jobname: Descriptive job name used for logging.
    :type: string

    :arg SOG_exec: Path/filename of the SOG executable.
    :type SOG_exec: str

    :arg infile: Path/filename of the infile to use.
    :type infile: str

    :arg editfiles: Path/filename of YAML infile(s) to apply to the infile
                    as edits.
    :type editfiles: list

    :arg outfile: Path/filename of the file to receive stdout from the run.
    :type outfile: str

    :arg nice: Priority to use for the run.
               Defaults to :kbd:`19`.
    :type nice: int

    :arg legacy_infile: infile is a legacy, Fortran-style infile.
                        Defaults to :kbd:`False`.
    :type legacy_infile: boolean
    """
    def __init__(self, jobname, SOG_exec, infile, editfiles, outfile,
                 nice=19, legacy_infile=False):
        self.jobname = jobname
        self.SOG_exec = SOG_exec
        self.infile = infile
        self.editfile = editfiles
        self.outfile = outfile
        self.nice = nice
        self.legacy_infile = legacy_infile
        self.dry_run = False
        self.process = None
        self.pid = None
        self.returncode = None

    def start(self):
        """Start the job in a subprocess.

        Cache the subprocess object and its process id as job attributes.
        """
        cmd = run_processor.prepare(self)
        self.process = subprocess.Popen(cmd, shell=True)
        self.pid = self.process.pid
        log.info('{0.jobname}: started job as process {0.pid}'.format(self))

    @property
    def done(self):
        """Return a boolean indicating whether or not the job has finished.

        Cache the subprocess return code as a job attribute.

        :returns: Done
        :rtype: boolean
        """
        finished = False
        self.returncode = self.process.poll()
        if self.returncode is not None:
            finished = True
            log.info(
                '{0.jobname}: finished job with return code {0.returncode}'
                .format(self))
        return finished


class BatchProcessor(object):
    """SOG batch processor.

    :arg batchfile: Path/filename for YAML file that described the jobs
                    to be run in the batch.
    :type batchfile: str

    :arg debug: Turn debug level logging output on/off.
                Defaults to :kbd:`False`.
    :type debug: boolean
    """
    def __init__(self, batchfile, debug=False):
        self.batchfile = batchfile
        if debug:
            log.setLevel(logging.DEBUG)
        self.max_concurrent_jobs = 1
        self.jobs = []
        self.in_progress = {}
        self.returncode = 0

    def prepare(self):
        """Read the batch description file and build the list of jobs to run.
        """
        if not os.path.exists(self.batchfile):
            raise IOError('batchfile not found: {.batchfile}'.format(self))
        self._read_config()
        self._build_jobs()

    def _read_config(self):
        log.info('building jobs described in {.batchfile}'.format(self))
        with open(self.batchfile, 'rt') as f:
            self.config = yaml.safe_load(f.read())
        if 'max_concurrent_jobs' in self.config:
            self.max_concurrent_jobs = self.config['max_concurrent_jobs']
        log.info(
            'max concurrent jobs: {.max_concurrent_jobs}'.format(self))

    def _build_jobs(self):
        try:
            default_editfiles = self.config['edit_files']
        except KeyError:
            default_editfiles = []
        log.debug(
            'YAML edit files that will be used in all jobs (in order): {}'
            .format(default_editfiles))
        default_legacy_infile = self._legacy_infile_default_rules()
        for job in self.config['jobs']:
            jobname = list(six.iterkeys(job))[0]
            log.info('building command for job: {}'.format(jobname))
            SOG_exec = self._job_or_default(jobname, job, 'SOG_executable')
            infile = self._job_or_default(jobname, job, 'base_infile')
            try:
                job_editfiles = job[jobname]['edit_files']
            except KeyError:
                job_editfiles = []
            log.debug(
                '{}: YAML edit files (in order): {}'
                .format(jobname, default_editfiles + job_editfiles))
            try:
                outfile = job[jobname]['outfile']
            except KeyError:
                if job_editfiles:
                    outfile = '.'.join((job_editfiles[-1], 'out'))
                else:
                    outfile = '.'.join((infile, 'out'))
            log.debug('{}: stdout stored in: {}'.format(jobname, outfile))
            legacy_infile = (default_legacy_infile or
                             self._legacy_infile_job_rules(jobname, job))
            log.debug('{}: legacy infile: {}'.format(jobname, legacy_infile))
            nice = self._job_or_default(jobname, job, 'nice', default=19)
            self.jobs.append(Job(
                jobname,
                SOG_exec, infile,
                editfiles=default_editfiles + job_editfiles,
                outfile=outfile,
                nice=nice,
                legacy_infile=legacy_infile,
            ))

    def _job_or_default(self, jobname, job, key, default=None):
        """Return the value for `key` from either the job or the defaults
        section of the config.
        The value from the job section take priority.
        """
        try:
            value = job[jobname][key]
            log.debug(
                '{}: {} from job description: {}'.format(jobname, key, value))
        except KeyError:
            try:
                value = self.config[key]
                log.debug(
                    '{}: {} from top level defaults: {}'
                    .format(jobname, key, value))
            except KeyError:
                if default is not None:
                    value = default
                    log.debug(
                        '{}: {} from hard-coded default: {}'
                        .format(jobname, key, value))
                else:
                    raise KeyError(
                        'No {0} key found for job: {1}'.format(key, jobname))
        return value

    def _legacy_infile_default_rules(self):
        """Return legacy_infile value and enforce rules for its use at the top
        level of the batch config file.
        """
        try:
            legacy_infile = self.config['legacy_infile']
        except KeyError:
            legacy_infile = False
        if legacy_infile and 'base_infile' in self.config:
            raise KeyError(
                'Default base_infile not allowed with legacy_infile = True')
        if legacy_infile and 'edit_files' in self.config:
            raise KeyError(
                'Default edit_files not allowed with legacy_infile = True')
        return legacy_infile

    def _legacy_infile_job_rules(self, jobname, job):
        """Return legacy_infile value and enforce rules for its use at the job
        level of the batch config file.
        """
        try:
            legacy_infile = job[jobname]['legacy_infile']
        except KeyError:
            legacy_infile = False
        if legacy_infile and 'base_infile' not in job[jobname]:
            raise KeyError(
                '{} job with legacy_infile = True requires base_infile'
                .format(jobname))
        if legacy_infile and 'edit_files' in job[jobname]:
            raise KeyError(
                '{} job with legacy_infile = True cannot have edit_files'
                .format(jobname))
        return legacy_infile

    def run(self, dry_run=False):
        """Run the jobs, or, if :kbd:`dry_run=True`, display information
        about the jobs that would be run.
        """
        if dry_run:
            self._dry_run()
            self.returncode = 0
            return self.returncode
        self._launch_initial_jobs()
        while self.jobs or self.in_progress:
            time.sleep(15)
            self._poll_and_launch()
        log.info('all jobs completed')
        return self.returncode

    def _dry_run(self):
        """Dry-run handler for `SOG batch` command.
        """
        wrapper = TextWrapper()
        print(wrapper.fill('The following SOG jobs would have been run:'))
        print('  job name: command\n')
        for job in self.jobs:
            cmd = '  {0.jobname}: SOG run {0.SOG_exec} {0.infile}'.format(job)
            for edit_file in job.editfile:
                cmd = ' '.join((cmd, '-e {}'.format(edit_file)))
            cmd = ' '.join((cmd, '-o {0.outfile}'.format(job)))
            if job.legacy_infile:
                cmd = ' '.join((cmd, '--legacy_infile'))
            cmd = ' '.join((cmd, '--nice {0.nice}\n'.format(job)))
            print(cmd)
        print(wrapper.fill(
            '{} job(s) would have been run concurrently.'
            .format(self.max_concurrent_jobs)))

    def _launch_initial_jobs(self):
        """Start running the batch by launching jobs up to the number of
        concurrent jobs allowed.
        """
        log.info('starting {.max_concurrent_jobs} jobs'.format(self))
        for process in range(self.max_concurrent_jobs):
            try:
                job = self.jobs.pop(0)
            except IndexError:
                break
            else:
                job.start()
                self.in_progress[job.pid] = job

    def _poll_and_launch(self):
        """Poll the in-progress jobs and launch new jobs as existing ones
        finish.
        """
        for running_job in six.itervalues(self.in_progress.copy()):
            if running_job.done:
                self.in_progress.pop(running_job.pid)
                self.returncode = max(
                    self.returncode, abs(running_job.returncode))
                try:
                    job = self.jobs.pop(0)
                except IndexError:
                    continue
                else:
                    job.start()
                    self.in_progress[job.pid] = job
