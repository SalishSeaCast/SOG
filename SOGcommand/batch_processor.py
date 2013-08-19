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
    for job in config['jobs']:
        jobname = list(six.iterkeys(job))[0]
        SOG_exec = _job_or_default(jobname, job, config, 'SOG_executable')
        jobs.append(Args(SOG_exec, 'foo', jobname=jobname))
    return jobs


def _job_or_default(jobname, job, config, key):
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
            raise KeyError(
                'No SOG_executable key found for job: {}'.format(jobname))
    return value


def dry_run(config, jobs):
    """Dry-run handler for `SOG batch` command.
    """
    wrapper = TextWrapper()
    print(wrapper.fill('The following SOG jobs would have been run:'))
    for job in jobs:
        print('  {}'.format(job))
    print(wrapper.fill(
        '{[max_concurrent_jobs]} job(s) would have been run concurrently.'
        .format(config)))
