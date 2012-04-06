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
    var_name = colander.SchemaNode(colander.String(), name='variable_name')
    description = colander.SchemaNode(colander.String())


class _Float(_SOG_YAML_Base):
    value = colander.SchemaNode(colander.Float())


class _Int(_SOG_YAML_Base):
    value = colander.SchemaNode(colander.Int())


class _Boolean(_SOG_YAML_Base):
    value = colander.SchemaNode(colander.Boolean())


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
        return appstruct

    def deserialize(self, node, cstruct):
        if cstruct is colander.null:
            return colander.null
        if not isinstance(cstruct, datetime):
            raise colander.Invalid(node, '{0} is not a datetime'.format(node))
        return cstruct


class _SOG_Datetime(_SOG_YAML_Base):
    value = colander.SchemaNode(_DateTime())


class _InitialConditions(colander.MappingSchema):
    init_datetime = _SOG_Datetime(
        infile_key='init datetime', var_name='initDatetime')


class _Location(colander.MappingSchema):
    latitude = _Float(infile_key='latitude', var_name='latitude')


class _Grid(colander.MappingSchema):
    model_depth = _Float(infile_key='maxdepth', var_name='grid%D')
    grid_size = _Int(infile_key='gridsize', var_name='grid%M')
    lambda_factor = _Float(infile_key='lambda', var_name='lambda')


class _Numerics(colander.MappingSchema):
    dt = _Int(infile_key='dt', var_name='dt')
    chem_dt = _Int(infile_key='chem_dt', var_name='chem_dt')
    max_iter = _Int(infile_key='max_iter', var_name='max_iter')


class _ForcingVariation(colander.MappingSchema):
    wind = _Boolean(
        infile_key='vary%wind%enabled', var_name='vary%wind%enabled')
    cloud_fraction = _Boolean(
        infile_key='vary%cf%enabled', var_name='vary%cf%enabled')
    river_flows = _Boolean(
        infile_key='vary%rivers%enabled', var_name='vary%rivers%enabled')
    temperature = _Boolean(
        infile_key='vary%temperature%enabled',
        var_name='vary%temperature%enabled')


class YAML_Infile(colander.MappingSchema):
    initial_conditions = _InitialConditions()
    end_datetime = _SOG_Datetime(
        infile_key='end datetime', var_name='endDatetime')
    location = _Location()
    grid = _Grid()
    numerics = _Numerics()
    vary = _ForcingVariation()


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
    def get_element(key, path):
        return yaml_schema.get_value(yaml_struct, '.'.join((path, key)))

    def transform(node, path):
        return {
            node.infile_key: {
                'value': get_element('value', path),
                'description': get_element('description', path),
                'units': get_element('units', path),
        }}

    def walk_subnodes(node, path):
        result = {}
        if not any(child.children for child in node.children):
            return transform(node, path)
        else:
            for child in node.children:
                result.update(
                    walk_subnodes(child, '.'.join((path, child.name))))
            return result

    result = {}
    for node in nodes:
        result.update(walk_subnodes(node, node.name))
    return result
