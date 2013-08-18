# -*- coding: utf-8 -*-
"""SOG run processor.

Do various operations related to running the the SOG bio-physical
model of deep estuaries. Most notably, run the model.

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
from tempfile import NamedTemporaryFile
from textwrap import TextWrapper
from time import sleep
from .infile_processor import create_infile


def prepare(args):
    """Return the command line string that will execute the requested SOG run.
    """
    if not args.outfile:
        args.outfile = os.path.abspath(os.path.basename(args.infile) + '.out')
    if not os.path.exists(args.infile):
        raise IOError('infile not found: {0.infile}'.format(args))
    else:
        if args.legacy_infile:
            infile = args.infile
        else:
            if args.dry_run:
                infile = NamedTemporaryFile(suffix='.infile').name
            else:
                infile = create_infile(args.infile, args.editfile)
    if not os.path.exists(args.SOG_exec):
        raise IOError('SOG executable not found: {0.SOG_exec}'.format(args))
    else:
        cmd = (
            'nice -n {0.nice} {0.SOG_exec} < {infile} > {0.outfile} 2>&1'
            .format(args, infile=infile))
    return cmd


def dry_run(cmd, args):
    """Dry-run handler for `SOG run` command.
    """
    wrapper = TextWrapper()
    print(wrapper.fill('Command that would have been used to run SOG:'))
    print('  {0}'.format(cmd))
    if args.watch:
        print(wrapper.fill(
            'Contents of {0} would have been shown on screen while '
            'SOG run was in progress.'.format(args.outfile))
        )


def watch_outfile(proc, outfile_name):
    """Generator that yields lines from SOG run outfile while run is
    in progress, and continues yielding the lines that are flushed
    when the run finishes.
    """
    # Wait for the SOG process to create the outfile
    sleep(0.1)
    with open(outfile_name) as outfile:
        while proc.poll() is None:
            # Echo lines flushed to outfile while SOG is running
            line = outfile.readline()
            if not line:
                sleep(0.1)
                continue
            yield line
        else:
            # Echo lines flushed to outfile when SOG run finishes
            for line in outfile:
                yield line
