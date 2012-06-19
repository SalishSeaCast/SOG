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
    data = _read_yaml_infile(yaml_infile)
    YAML = YAML_Infile()
    yaml_struct = _deserialize_yaml(data, YAML, yaml_infile)
    infile_struct = yaml_to_infile(YAML_Infile.nodes, YAML, yaml_struct)
    SOG = SOG_Infile()
    data = SOG.serialize(infile_struct)
    with NamedTemporaryFile(mode='wt', suffix='.infile', delete=False) as f:
        SOG_infile.dump(data, SOG_KEYS, f)
        infile_name = f.name
    return infile_name


def read_infile(yaml_infile, key):
    """Return value for specified infile key.

    :arg yaml_infile: Path/name of a SOG YAML infile.
    :type yaml_infile: str

    :arg key: Infile key to return value for.
    :type key: str

    :returns value: Infile value associated with key
    :rtype: str
    """
    data = _read_yaml_infile(yaml_infile)
    YAML = YAML_Infile()
    yaml_struct = _deserialize_yaml(data, YAML, yaml_infile)
    try:
        value = YAML.get_value(yaml_struct, key)['value']
    except KeyError:
        print('KeyError: {0}'.format(key), file=sys.stderr)
        sys.exit(2)
    return value


def _read_yaml_infile(yaml_infile):
    """Read `yaml_infile` and return the resulting Python dict.

    :arg yaml_infile: Path/name of a SOG YAML infile.
    :type yaml_infile: str

    :returns data: Content of `yaml_infile` as a Python dict.
    :rtype: dict
    """
    with open(yaml_infile, 'rt') as f:
        try:
            data = yaml.load(f)
        except yaml.scanner.ScannerError:
            print('Unable to parse {0}: Are you sure that it is YAML?'
                  .format(yaml_infile), file=sys.stderr)
            sys.exit(2)
    return data


def _deserialize_yaml(data, yaml_schema, yaml_infile):
    """Deserialize `data` according to `yaml_schema` and return the
    resulting YAML schema data structure.

    :arg data: Content of `yaml_infile` as a Python dict.
    :type data: dict

    :arg yaml_schema: SOG YAML infile schema instance
    :type yaml_schema: :class:`YAML_Infile` instance

    :arg yaml_infile: Path/name of a SOG YAML infile.
    :type yaml_infile: str

    :returns yaml_struct: SOG YAML infile data structure
    :rtype: nested dicts
    """
    try:
        yaml_struct = yaml_schema.deserialize(data)
    except colander.Invalid as e:
        print('Invalid SOG YAML in {0}. '
              'The following parameters are missing or misspelled:'
              .format(yaml_infile), file=sys.stderr)
        pprint.pprint(e.asdict(), sys.stderr)
        sys.exit(2)
    return yaml_struct
