# -*- coding: utf-8 -*-
"""SOG batch processor.

Do various operations related to running batch jobs of the SOG bio-physical
model of deep estuaries.

This module provides services to the SOG command processor.

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
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
import os
from textwrap import TextWrapper
import six
import yaml


class Args(object):
    """Container for SOG command arguments.
    """
    def __init__(
            self,
            SOG_exec,
            infile,
            editfiles=[],
            outfile='',
            jobname=None,
            legacy_infile=False,
            dry_run=False,
            nice=19):
        self.SOG_exec = SOG_exec
        self.infile = infile
        self.editfile = editfiles
        self.outfile = outfile
        self.jobname = jobname
        self.legacy_infile = legacy_infile
        self.dry_run = dry_run
        self.nice = nice


def read_config(batchfile):
    if not os.path.exists(batchfile):
        raise IOError('batchfile not found: {}'.format(batchfile))
    else:
        with open(batchfile, 'rt') as f:
            config = yaml.safe_load(f.read())
            if 'max_concurrent_jobs' not in config:
                config['max_concurrent_jobs'] = 1
        return config


def build_jobs(config):
    """Build list of jobs to run as a batch from config dict.
    """
    jobs = []
    try:
        default_editfiles = config['edit_files']
    except KeyError:
        default_editfiles = []
    default_legacy_infile = _legacy_infile_default_rules(config)
    for job in config['jobs']:
        jobname = list(six.iterkeys(job))[0]
        SOG_exec = _job_or_default(jobname, job, config, 'SOG_executable')
        infile = _job_or_default(jobname, job, config, 'base_infile')
        try:
            job_editfiles = job[jobname]['edit_files']
        except KeyError:
            job_editfiles = []
        try:
            outfile = job[jobname]['outfile']
        except KeyError:
            if job_editfiles:
                outfile = '.'.join((job_editfiles[-1], 'out'))
            else:
                outfile = '.'.join((infile, 'out'))
        legacy_infile = (
            default_legacy_infile or _legacy_infile_job_rules(jobname, job))
        nice = _job_or_default(jobname, job, config, 'nice', default=19)
        jobs.append(Args(
            SOG_exec, infile,
            editfiles=default_editfiles + job_editfiles,
            outfile=outfile,
            jobname=jobname,
            legacy_infile=legacy_infile,
            nice=nice))
    return jobs


def _job_or_default(jobname, job, config, key, default=None):
    """Return the value for `key` from either the job or the defaults
    section of the config.
    The value from the job section take priority.
    """
    try:
        value = job[jobname][key]
    except KeyError:
        try:
            value = config[key]
        except KeyError:
            if default is not None:
                value = default
            else:
                raise KeyError(
                    'No {0} key found for job: {1}'.format(key, jobname))
    return value


def _legacy_infile_default_rules(config):
    """Return legacy_infile value and enforce rules for its use at the top
    level of the batch config file.
    """
    try:
        legacy_infile = config['legacy_infile']
    except KeyError:
        legacy_infile = False
    if legacy_infile and 'base_infile' in config:
        raise KeyError(
            'Default base_infile not allowed with legacy_infile = True')
    if legacy_infile and 'edit_files' in config:
        raise KeyError(
            'Default edit_files not allowed with legacy_infile = True')
    return legacy_infile


def _legacy_infile_job_rules(jobname, job):
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


def dry_run(jobs, max_concurrent_jobs):
    """Dry-run handler for `SOG batch` command.
    """
    wrapper = TextWrapper()
    print(wrapper.fill('The following SOG jobs would have been run:'))
    print('  job name: command\n')
    for job in jobs:
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
        .format(max_concurrent_jobs)))
