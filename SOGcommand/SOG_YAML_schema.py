"""SOG YAML infile schema and YAML to infile data structure
transformation function.

The Colander schema that this module defines is for serialization and
validation of the SOG infile written in YAML.

The :func:`yaml_to_infile` function transforms elements in a SOG YAML
infile data structure into those of a SOG Fortran-ish infile data
structure that is defined in :mod:`SOG_infile_schema`.
"""
from datetime import datetime
import colander


class _SOG_YAML_Base(colander.MappingSchema):
    """Base class for SOG YAML infile quantities.
    """
    units = colander.SchemaNode(colander.String(), default=None, missing=None)
    var_name = colander.SchemaNode(colander.String(), name='variable name')
    description = colander.SchemaNode(colander.String())


class _Float(_SOG_YAML_Base):
    value = colander.SchemaNode(colander.Float())


class _Int(_SOG_YAML_Base):
    value = colander.SchemaNode(colander.Int())


class _DateTime(object):
    """Replacement for Colander's ISO8601 DateTime type.

    We don't care about time zone, and want the string representation
    of a datetime to be `yyy-mm-dd hh:mm:ss`.
    """
    def serialize(self, node, appstruct):
        if appstruct is colander.null:
            return colander.null
        if not isinstance(appstruct, datetime):
            raise colander.Invalid(node, '{0} is not a datetime'.format(node))
        return '{0:%Y-%m-%d %H:%M:%S}'.format(appstruct)

    def deserialize(self, node, cstruct):
        if cstruct is colander.null:
            return colander.null
        if not isinstance(cstruct, datetime):
            raise colander.Invalid(node, '{0} is not a datetime'.format(node))
        return cstruct


class _SOG_Datetime(_SOG_YAML_Base):
    value = colander.SchemaNode(_DateTime())


class _Grid(colander.MappingSchema):
    model_depth = _Float(infile_key='maxdepth', var_name='grid%D')
    grid_size = _Int(infile_key='gridsize', var_name='grid%M')
    lambda_factor = _Float(infile_key='lambda', var_name='lambda')


class _InitialConditions(colander.MappingSchema):
    init_datetime = _SOG_Datetime(
        infile_key='init datetime', var_name='initDatetime')


class YAML_Infile(colander.MappingSchema):
    grid = _Grid()
    init_conditions = _InitialConditions(name='initial conditions')


def yaml_to_infile(nodes, yaml_schema, yaml_struct):
    """Transform elements in a SOG YAML infile data structure
    into those of a SOG Fortran-sh infile data structure.

    :arg nodes: Iterable of :class:`colander.SchemaNode` instances.
    :type nodes: iterable

    :arg yaml_schema: SOG YAML infile schema instance
    :type yaml_schema: :class:`YAML_Infile` instance

    :arg yaml_struct: SOG YAML infile data structure
    :type yaml_struct: nested dicts

    :returns: SOG YAML infile data structure.
    :rtype: nested dicts
    """
    def get_element(part):
        value = yaml_schema.get_value(
            yaml_struct, '{0.name}.{1.name}.{2}'.format(node, child, part))
        if isinstance(value, datetime):
            value = '"{0}"'.format(value)
        return value

    result = {}
    for node in nodes:
        for child in node.children:
            result[child.infile_key] = {
                'value': get_element('value'),
                'description': get_element('description'),
                'units': get_element('units'),
            }
    return result
