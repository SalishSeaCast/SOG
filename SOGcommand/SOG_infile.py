"""SOG infile parser and emitter.

Parse (aka load) a SOG infile into a Python dict of dicts, or emit
(aka dump) a dict of dicts to produce a validly formatted SOG infile.

Neither the parser not the emitter validate the data beyond ensuring
that each line contains a key, value, and description, in that order,
and the the keys and descriptions are enclosed in double quotes.

Both the parser and emitter can be used to process fragments of infile
content.

To be clear, the SOG infile format this module handles is the one that
SOG's Fortran input_processor.f90 module reads.
"""
import re


def load(stream):
    """Load the parameter keys, values and descriptions from a SOG
    infile into a Python data structure.

    Comments (lines starting with !) and empty lines are ignored.

    :arg stream: An iterable (tyically a file object) containing SOG
                 infile formatted lines separated by newlines.
    :type stream: A file object or other iterable.

    :returns: Python data structure containing the infile content.
    :rtype: dict of dicts

    Given a SOG infile line that looks like::

      "maxdepth"  40.0d0  "depth of modelled domain [m]"

    the resulting dict item would be::

      'maxdepth': {'value': '40.0d0', 'description': 'depth of modelled domain'
                   'units': 'm'}

    The SOG infile line may separated over up to 3 lines (i.e. have
    newlines between the key and value, and/or the value and
    description.

    The units are the contents of a [] pair in the description, and
    the units item in the dict is an empty string if the description
    does not contain a [] pair.
    """
    key_value_separator = re.compile(r'"\s+')
    value_desc_separator = re.compile(r'\s+"')
    units_container = re.compile(r'\[.+\]')

    def get_line():
        line = stream.next().strip()
        if line == '' or line.startswith('!'):
            line = get_line()
        return line

    result = {}
    while True:
        try:
            line = get_line()
            try:
                key, line = key_value_separator.split(line, 1)
            except ValueError:
                line = ' '.join((line, get_line()))
                key, line = key_value_separator.split(line, 1)
            key = key.strip('"')
            try:
                value, description = value_desc_separator.split(line, 1)
            except ValueError:
                line = ' '.join((line, get_line()))
                value, description = value_desc_separator.split(line, 1)
            value = value.strip('"')
            description = description.strip('"')
            m = units_container.search(description)
            if m:
                units = m.group()
                description = description.replace(units, '').strip()
                units = units.strip('[]')
            else:
                units = None
            result[key] = {
                'value': value, 'description': description, 'units': units}
        except StopIteration:
            return result

def dump(data, key_order, stream):
    """Dump the Python data structure to the stream using the
    key_order to control the order of the lines in the stream.

    :arg data: Python data structure containing the infile content.
    :type data: dict of dicts

    :arg key_order: Iterable of infile key strings that defines the
                    order in which the SOG infile lines are written.
    :type key_order: iterable

    :arg stream: File-like object to which the SOG infile lines are
                 written.
    :type stream: file-like obejct

    Given a dict item that looks like::

      'maxdepth': {'value': '40.0d0', 'description': 'depth of modelled domain'
                   'units': 'm'}

    the resulting SOG infile line would be::

      "maxdepth"  40.0d0  "depth of modelled domain [m]"

    If the units item in the dict is None the square bracketed term
    will be excluded from the description phrase in the SOG infile
    line.
    """
    for key in key_order:
        line = '"{0}"  {1[value]}  "{1[description]}'.format(key, data[key])
        if data[key]['units'] is not None:
            line = '{0} [{1[units]}]'.format(line, data[key])
        stream.write('{0}"\n'.format(line))
