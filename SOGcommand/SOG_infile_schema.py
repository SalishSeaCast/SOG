"""SOG infile schema and infile to YAML data structure transformation function.

The Colander schema that this module defines is for serialization and
validation of the SOG infile format that SOG's Fortran
input_processor.f90 module reads.

The :func:`infile_to_yaml` function transforms elements in a SOG
Fortran-ish infile data structure into those of a SOG YAML infile data
structure that is defined in :mod:`SOG_YAML_schema`.
"""
from datetime import datetime
import colander


class _SOG_InfileBase(colander.MappingSchema):
    """Base class for SOG Fortran-ish infile quantities.
    """
    description = colander.SchemaNode(colander.String())
    units = colander.SchemaNode(colander.String(), default=None, missing=None)


class _RealDP(object):
    """Fortran real(kind=dp) type.

    Text representation must be scientific with d as exponent
    separator so that Fortran list directed input will work properly.
    """
    def serialize(self, node, appstruct):
        if appstruct is colander.null:
            return colander.null
        if not isinstance(appstruct, (int, float)):
            raise colander.Invalid(
                node, '{0!r} is not a number'.format(appstruct))
        return '{0:e}'.format(appstruct).replace('e', 'd')

    def deserialize(self, node, cstruct):
        if cstruct is colander.null:
            return colander.null
        if not isinstance(cstruct, basestring):
            raise colander.Invalid(
                node, '{0!r} is not a string'.format(cstruct))
        return float(cstruct.replace('d', 'e'))


class _SOG_RealDP(_SOG_InfileBase):
    value = colander.SchemaNode(_RealDP())


class _SOG_Int(_SOG_InfileBase):
    value = colander.SchemaNode(colander.Int())


class _Datetime(object):
    """SOG datetime type.

    Text representation has the format `"yyyy-mm-dd hh:mm:ss"` expected
    by SOG.
    """
    def serialize(self, node, appstruct):
        if appstruct is colander.null:
            return colander.null
        if not isinstance(appstruct, datetime):
            raise colander.Invalid(
                node, '{0!r} is not a datetime'.format(appstruct))
        return '"{0:%Y-%m-%d %H:%M:%S}"'.format(appstruct)

    def deserialize(self, node, cstruct):
        if cstruct is colander.null:
            return colander.null
        if not isinstance(cstruct, basestring):
            raise colander.Invalid(
                node, '{0!r} is not a string'.format(cstruct))
        return datetime.strptime(cstruct, '%Y-%m-%d %H:%M:%S')


class _SOG_Datetime(_SOG_InfileBase):
    value = colander.SchemaNode(_Datetime())


class _Boolean(object):
    """SOG boolean type.

    Text representation is Fortran syntax: `.true.` or `.false.`.
    """
    def serialize(self, node, appstruct):
        if appstruct is colander.null:
            return colander.null
        if not isinstance(appstruct, bool):
            raise colander.Invalid(
                node, '{0!r} is not a boolean'.format(appstruct))
        return appstruct and '.true.' or '.false.'

    def deserialize(self, node, cstruct):
        if cstruct is colander.null:
            return colander.null
        if not isinstance(cstruct, basestring):
            raise colander.Invalid(
                node, '{0!r} is not a string'.format(cstruct))
        if cstruct.lower() == '.true.':
            return True
        return False


class _SOG_Boolean(_SOG_InfileBase):
    value = colander.SchemaNode(_Boolean())


class _String(object):
    """Replacement for Colander's String type.

   SOG works with plain ASCII strings, not Unicode. Serialized strings are
   enclosed in double quotes.
    """
    def serialize(self, node, appstruct):
        if appstruct is colander.null:
            return colander.null
        if not isinstance(appstruct, basestring):
            raise colander.Invalid(
                node, '{0!r} is not a string'.format(appstruct))
        return '"{0}"'.format(appstruct)

    def deserialize(self, node, cstruct):
        if cstruct is colander.null:
            return colander.null
        if not isinstance(cstruct, basestring):
            raise colander.Invalid(
                node, '{0!r} is not a string'.format(cstruct))
        return str(cstruct)


class _SOG_String(_SOG_InfileBase):
    value = colander.SchemaNode(_String())


class SOG_Infile(colander.MappingSchema):
    latitude = _SOG_RealDP()
    maxdepth = _SOG_RealDP()
    gridsize = _SOG_Int()
    lambda_factor = _SOG_RealDP(name='lambda')
    init_datetime = _SOG_Datetime(name='init datetime')
    end_datetime = _SOG_Datetime(name='end datetime')
    dt = _SOG_Int()
    chem_dt = _SOG_Int()
    max_iter = _SOG_Int()
    vary_wind = _SOG_Boolean(name='vary%wind%enabled')
    vary_cloud_fraction = _SOG_Boolean(name='vary%cf%enabled')
    vary_river_flows = _SOG_Boolean(name='vary%rivers%enabled')
    vary_temperature = _SOG_Boolean(name='vary%temperature%enabled')
    nitrate_chl_conversion = _SOG_RealDP(name='N2chl')
    ctd_in = _SOG_String()


def infile_to_yaml(nodes, infile_schema, infile_struct):
    """Transform elements in a SOG Fortran-ish infile data structure
    into those of a SOG YAML infile data structure.

    :arg nodes: Iterable of :class:`colander.SchemaNode` instances.
    :type nodes: iterable

    :arg infile_schema: SOG Fortran-ish infile schema instance
    :type infile_schema: :class:`SOG_Infile` instance

    :arg infile_struct: SOG Fortran-ish infile data structure
    :type infile_struct: nested dicts

    :returns: SOG YAML infile data structure.
    :rtype: nested dicts
    """
    def get_element(node, key):
        return infile_schema.get_value(
            infile_struct, '{0.infile_key}.{1}'.format(node, key))

    def transform(node):
        result = {
            'value': get_element(node, 'value'),
            'description': str(get_element(node, 'description')),
            'variable name': node.var_name,
        }
        units = get_element(node, 'units')
        if units is not None:
            result['units'] = str(units)
        return result

    def walk_subnodes(node):
        result = {}
        if not any(child.children for child in node.children):
            return transform(node)
        else:
            for child in node.children:
                result.update({child.name: walk_subnodes(child)})
            return result

    result = {}
    for node in nodes:
        result.update({node.name: walk_subnodes(node)})
    return result
