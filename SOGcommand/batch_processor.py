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
import yaml


def read_config(batchfile):
    if not os.path.exists(batchfile):
        raise IOError('batchfile not found: {}'.format(batchfile))
    else:
        with open(batchfile, 'rt') as f:
            return yaml.safe_load(f.read())


def build_jobs(config):
    """Build list of jobs to run as a batch from config dict.
    """
    jobs = []
    for job in config['jobs']:
        pass
    return jobs


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
