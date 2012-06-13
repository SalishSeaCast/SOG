# -*- coding: utf-8 -*-
"""SOG infile processor.

Do various operations on input files for the the SOG bio-physical
model of deep estuaries. Most notably, convert new YAML infiles into
the old Fortran-style infiles that SOG reads.

This module provides services to the SOG command processor.

:Author: Doug Latornell <djl@douglatornell.ca>
"""
from __future__ import print_function
import pprint
import sys
from tempfile import NamedTemporaryFile
import colander
import yaml
import SOG_infile
from SOG_infile_schema import (
    SOG_Infile,
    SOG_KEYS,
    )
from SOG_YAML_schema import (
    YAML_Infile,
    yaml_to_infile,
    )


def create_infile(yaml_infile):
    """Create a SOG Fortran-style infile for SOG to read from
    `yaml_infile`.

    :arg yaml_infile: Path/name of a SOG YAML infile.
    :type yaml_infile: str

    :returns infile_name: Path/name of the SOG Fortran-style temporary
                          infile that is created.
    :rtype: str
    """
    YAML = YAML_Infile()
    with open(yaml_infile, 'rt') as f:
        try:
            data = yaml.load(f)
        except yaml.scanner.ScannerError:
            print('Unable to parse {0}: Are you sure that it is YAML?'
                  .format(yaml_infile), file=sys.stderr)
            sys.exit(2)
    try:
        yaml_struct = YAML.deserialize(data)
    except colander.Invalid as e:
        print('Invalid SOG YAML in {0}. '
              'The following parameters are missing or misspelled:'
              .format(yaml_infile), file=sys.stderr)
        pprint.pprint(e.asdict(), sys.stderr)
        sys.exit(2)
    infile_struct = yaml_to_infile(YAML_Infile.nodes, YAML, yaml_struct)
    SOG = SOG_Infile()
    data = SOG.serialize(infile_struct)
    with NamedTemporaryFile(mode='wt', suffix='.infile', delete=False) as f:
        SOG_infile.dump(data, SOG_KEYS, f)
        infile_name = f.name
    return infile_name
