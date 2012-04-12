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
    separator so that Fortran list directed input will convert number
    properly to real(kind=dp).
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


class _RealDP_List(object):
    """List of Fortran real(kind=dp) type values.

    Text representation must be a whitespace separated numbers in
    scientific notation with d as exponent separator so that Fortran
    list directed input will convert numbers properly to real(kind=dp).

    Python representation is a list of floats.
    """
    def serialize(self, node, appstruct):
        if appstruct is colander.null:
            return colander.null
        if not isinstance(appstruct, list):
            raise colander.Invalid(
                node, '{0!r} is not a list'.format(appstruct))
        if not all(isinstance(item, (int, float)) for item in appstruct):
            raise colander.Invalid(
                node, '{0!r} contains item that is not a number'
                .format(appstruct))
        return ' '.join(
            '{0:e}'.format(item).replace('e', 'd') for item in appstruct)

    def deserialize(self, node, cstruct):
        if cstruct is colander.null:
            return colander.null
        if not isinstance(cstruct, basestring):
            raise colander.Invalid(
                node, '{0!r} is not a string'.format(cstruct))
        return [float(item.replace('d', 'e')) for item in cstruct.split()]


class _SOG_RealDP_List(_SOG_InfileBase):
    value = colander.SchemaNode(_RealDP_List())


class _SOG_Int(_SOG_InfileBase):
    value = colander.SchemaNode(colander.Int())


class _IntList(object):
    """List of Fortran integer type values.

    Text representation must be a whitespace separated integers so
    that Fortran list directed input will convert numbers properly to
    integer.

    Python representation is a list of ints.
    """
    def serialize(self, node, appstruct):
        if appstruct is colander.null:
            return colander.null
        if not isinstance(appstruct, list):
            raise colander.Invalid(
                node, '{0!r} is not a list'.format(appstruct))
        if not all(isinstance(item, int) for item in appstruct):
            raise colander.Invalid(
                node, '{0!r} contains item that is not an integer'
                .format(appstruct))
        return ' '.join('{0:d}'.format(item) for item in appstruct)

    def deserialize(self, node, cstruct):
        if cstruct is colander.null:
            return colander.null
        if not isinstance(cstruct, basestring):
            raise colander.Invalid(
                node, '{0!r} is not a string'.format(cstruct))
        return [int(item) for item in cstruct.split()]


class _SOG_IntList(_SOG_InfileBase):
    value = colander.SchemaNode(_IntList())


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
    nuts_in = _SOG_String()
    botl_in = _SOG_String()
    chem_in = _SOG_String()
    init_chl_split = _SOG_RealDP_List(name='initial chl split')
    std_phys_ts_out = _SOG_String()
    user_phys_ts_out = _SOG_String()
    std_bio_ts_out = _SOG_String()
    user_bio_ts_out = _SOG_String()
    std_chem_ts_out = _SOG_String()
    num_profiles = _SOG_Int(name='noprof')
    profile_days = _SOG_IntList(name='profday')
    profile_times = _SOG_RealDP_List(name='proftime')
    halocline_file = _SOG_String(name='haloclinefile')
    profile_file_base = _SOG_String(name='profile_base')
    hoffmueller_file = _SOG_String(name='Hoffmueller file')
    hoffmueller_start_year = _SOG_Int(name='Hoffmueller start yr')
    hoffmueller_start_day = _SOG_Int(name='Hoffmueller start day')
    hoffmueller_start_sec = _SOG_Int(name='Hoffmueller start sec')
    hoffmueller_end_year = _SOG_Int(name='Hoffmueller end yr')
    hoffmueller_end_day = _SOG_Int(name='Hoffmueller end day')
    hoffmueller_end_sec = _SOG_Int(name='Hoffmueller end sec')
    hoffmueller_interval = _SOG_RealDP(name='Hoffmueller interval')
    constant_temperature = _SOG_Boolean(name='temp_constant')
    salinity_fit_coefficients = _SOG_RealDP_List(name='salinity')
    temperature_fit_coefficients = _SOG_RealDP_List(name='temperature')
    phyto_fluor_fit_coefficients = _SOG_RealDP_List(name='Phytoplankton')
    nitrate_fit_coefficients = _SOG_RealDP_List(name='Nitrate')
    silicon_fit_coefficients = _SOG_RealDP_List(name='Silicon')
    DIC_fit_coefficients = _SOG_RealDP_List(name='DIC')
    dissolved_oxygen_fit_coefficients = _SOG_RealDP_List(name='Oxy')
    alkalinity_fit_coefficients = _SOG_RealDP_List(name='Alk')
    ammonium_fit_coefficients = _SOG_RealDP_List(name='Ammonium')
    phyto_ratio_fit_coefficients = _SOG_RealDP_List(name='Ratio')


# List of keys, in order, to create a SOG infile
SOG_KEYS = [
    'latitude', 'maxdepth',  'gridsize', 'lambda',
    'init datetime', 'end datetime', 'dt', 'chem_dt', 'max_iter',
    'vary%wind%enabled', 'vary%cf%enabled', 'vary%rivers%enabled',
    'vary%temperature%enabled',
    'N2chl', 'ctd_in', 'nuts_in', 'botl_in', 'chem_in',
    'initial chl split',
    'std_phys_ts_out', 'user_phys_ts_out', 'std_bio_ts_out',
    'user_bio_ts_out', 'std_chem_ts_out',
    'noprof', 'profday', 'proftime', 'haloclinefile', 'profile_base',
    'Hoffmueller file', 'Hoffmueller start yr', 'Hoffmueller start day',
    'Hoffmueller start sec', 'Hoffmueller end yr', 'Hoffmueller end day',
    'Hoffmueller end sec', 'Hoffmueller interval',
    'temp_constant', 'salinity', 'temperature', 'Phytoplankton', 'Nitrate',
    'Silicon', 'DIC', 'Oxy', 'Alk', 'Ammonium', 'Ratio',
    ]


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
