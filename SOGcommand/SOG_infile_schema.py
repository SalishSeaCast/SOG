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
    minor_axis = _SOG_RealDP(name='Lx')
    major_axis = _SOG_RealDP(name='Ly')
    open_ended_estuary = _SOG_Boolean(name='openEnd')
    momentum_wave_break_diffusivity = _SOG_RealDP(name='nu_w_m')
    scalar_wave_break_diffusivity = _SOG_RealDP(name='nu_w_s')
    shear_diffusivity_smoothing = _SOG_RealDP_List(name='shear smooth')
    max_upwelling_velocity = _SOG_RealDP(name='upwell_const')
    variation_depth_param = _SOG_RealDP(name='d')
    mean_total_flow = _SOG_RealDP(name='Qbar')
    common_exponent = _SOG_RealDP(name='F_SOG')
    SoG_exponent = _SOG_RealDP(name='F_RI')
    scale_factor = _SOG_RealDP(name='Fw_scale')
    add_freshwater_on_surface = _SOG_Boolean(name='Fw_surface')
    distribution_depth = _SOG_RealDP(name='Fw_depth')
    northern_return_flow = _SOG_Boolean(name='northern_return_flow_on')
    include_fresh_water_nutrients = _SOG_Boolean(name='use_Fw_nutrients')
    bottom_salinity = _SOG_RealDP(name='cbottom')
    alpha = _SOG_RealDP(name='calpha')
    alpha2 = _SOG_RealDP(name='calpha2')
    gamma = _SOG_RealDP(name='cgamma')
    beta = _SOG_RealDP(name='cbeta')
    ialpha = _SOG_RealDP()
    ibeta = _SOG_RealDP()
    igamma = _SOG_RealDP()
    isigma = _SOG_RealDP()
    itheta = _SOG_RealDP()
    idl = _SOG_RealDP()
    include_flagellates = _SOG_Boolean(name='flagellates_on')
    include_remineralization = _SOG_Boolean(name='remineralization')
    include_microzooplankton = _SOG_Boolean(name='use microzooplankton')
    single_species_light = _SOG_Boolean(name='single species light')
    mesozoo_winter_conc = _SOG_RealDP(name='Mesozoo, winter conc')
    mesozoo_summer_conc = _SOG_RealDP(name='Mesozoo, summer conc')
    mesozoo_summer_peak_magnitudes = _SOG_RealDP_List(
        name='Mesozoo, summer peak mag')
    mesozoo_summer_peak_days = _SOG_RealDP_List(
        name='Mesozoo, summer peak pos')
    mesozoo_summer_peak_widths = _SOG_RealDP_List(
        name='Mesozoo, summer peak wid')
    mesozoo_max_ingestion = _SOG_RealDP(name='Mesozoo, max ingestion')
    mesozoo_grazing_limit = _SOG_RealDP(name='Mesozoo, pred slope')
    mesozoo_grazing_half_saturation = _SOG_RealDP(
        name='Mesozoo, half-sat')
    mesozoo_diatom_preference = _SOG_RealDP(
        name='Mesozoo, pref for diatoms')
    mesozoo_diatom_grazing_limit = _SOG_RealDP(
        name='Mesozoo, micro pred slope')
    mesozoo_diatom_grazing_half_saturation = _SOG_RealDP(
        name='Mesozoo, micro half-sat')
    mesozoo_nano_preference = _SOG_RealDP(name='Mesozoo, pref for nano')
    mesozoo_nano_grazing_limit = _SOG_RealDP(
        name='Mesozoo, nano pred slope')
    mesozoo_nano_grazing_half_saturation = _SOG_RealDP(
        name='Mesozoo, nano half-sat')
    mesozoo_PON_preference = _SOG_RealDP(
        name='Mesozoo, pref for PON')
    mesozoo_PON_grazing_limit = _SOG_RealDP(
        name='Mesozoo, PON pred slope')
    mesozoo_PON_grazing_half_saturation = _SOG_RealDP(
        name='Mesozoo, PON half-sat')
    mesozoo_microzoo_preference = _SOG_RealDP(
        name='Mesozoo, pref for uZoo')
    mesozoo_microzoo_grazing_limit = _SOG_RealDP(
        name='Mesozoo, uZoo pred slope')
    mesozoo_microzoo_grazing_half_saturation = _SOG_RealDP(
        name='Mesozoo, uZoo half-sat')
    mesorub_max_ingestion = _SOG_RealDP(name='Mesorub, max ingestion')
    mesorub_assimilation_efficiency = _SOG_RealDP(
        name='Mesorub, assimilation eff')
    mesorub_grazing_limit = _SOG_RealDP(
        name='Mesorub, nano predslope')
    mesorub_grazing_half_saturation = _SOG_RealDP(
        name='Mesorub, nano half-sat')
    microzoo_max_ingestion = _SOG_RealDP(
        name='Microzoo, max ingestion')
    microzoo_assimilation_efficiency = _SOG_RealDP(
        name='Microzoo, assimil. eff')
    microzoo_natural_mortality = _SOG_RealDP(
        name='Microzoo, nat mort')
    microzoo_excretion = _SOG_RealDP(
       name='Microzoo, excretion')
    microzoo_grazing_limit = _SOG_RealDP(
        name='Microzoo, pred slope')
    microzoo_grazing_half_saturation = _SOG_RealDP(
        name='Microzoo, half-sat')
    microzoo_pico_preference = _SOG_RealDP(
        name='Microzoo, pref for Pico')
    microzoo_pico_grazing_limit = _SOG_RealDP(
        name='uzoo, Pico pred slope')
    microzoo_pico_grazing_half_saturation = _SOG_RealDP(
        name='uzoo, Pico half-sat')
    microzoo_micro_preference = _SOG_RealDP(
        name='Microzoo, pref for Micro')
    microzoo_micro_grazing_limit = _SOG_RealDP(
        name='uzoo, Micro pred slope')
    microzoo_micro_grazing_half_saturation = _SOG_RealDP(
        name='Microzoo, Micro half-sat')
    microzoo_nano_preference = _SOG_RealDP(
        name='Microzoo, pref for nano')
    microzoo_nano_grazing_limit = _SOG_RealDP(
        name='Microzoo, nano pred slope')
    microzoo_nano_grazing_half_saturation = _SOG_RealDP(
        name='Microzoo, nano half-sat')
    microzoo_PON_preference = _SOG_RealDP(
        name='Microzoo, pref for PON')
    microzoo_PON_grazing_limit = _SOG_RealDP(
        name='Microzoo, PON pred slope')
    microzoo_PON_grazing_half_saturation = _SOG_RealDP(
        name='Microzoo, PON half-sat')
    microzoo_microzoo_preference = _SOG_RealDP(
        name='Microzoo, pref for uZoo')
    microzoo_microzoo_grazing_limit = _SOG_RealDP(
        name='Microzoo, uZoo pred slope')
    microzoo_microzoo_grazing_half_saturation = _SOG_RealDP(
        name='Microzoo, uZoo half-sat')

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
    'Lx', 'Ly', 'openEnd',
    'nu_w_m', 'nu_w_s', 'shear smooth',
    'upwell_const', 'Qbar', 'F_SOG', 'F_RI', 'Fw_scale', 'Fw_surface',
    'Fw_depth', 'use_Fw_nutrients', 'northern_return_flow_on',
    'cbottom', 'calpha', 'calpha2', 'cgamma', 'cbeta',
    'ialpha', 'ibeta', 'igamma', 'isigma', 'itheta', 'idl',
    'd',
    'flagellates_on', 'remineralization', 'use microzooplankton',
    'single species light',
    'Mesozoo, winter conc',
    'Mesozoo, summer conc', 'Mesozoo, summer peak mag',
    'Mesozoo, summer peak pos', 'Mesozoo, summer peak wid',
    'Mesozoo, max ingestion', 'Mesozoo, pred slope', 'Mesozoo, half-sat',
    'Mesozoo, pref for diatoms', 'Mesozoo, micro pred slope',
    'Mesozoo, micro half-sat',
    'Mesozoo, pref for nano', 'Mesozoo, nano pred slope',
    'Mesozoo, nano half-sat',
    'Mesozoo, pref for PON', 'Mesozoo, PON pred slope',
    'Mesozoo, PON half-sat',
    'Mesozoo, pref for uZoo', 'Mesozoo, uZoo pred slope',
    'Mesozoo, uZoo half-sat',
    'Mesorub, max ingestion', 'Mesorub, assimilation eff',
    'Mesorub, nano half-sat', 'Mesorub, nano predslope',
    'Microzoo, max ingestion', 'Microzoo, assimil. eff',
    'Microzoo, nat mort', 'Microzoo, excretion',
    'Microzoo, pred slope', 'Microzoo, half-sat',
    'Microzoo, pref for Pico', 'uzoo, Pico pred slope', 'uzoo, Pico half-sat',
    'Microzoo, pref for Micro', 'uzoo, Micro pred slope',
    'Microzoo, Micro half-sat',
    'Microzoo, pref for nano', 'Microzoo, nano pred slope',
    'Microzoo, nano half-sat',
    'Microzoo, pref for PON', 'Microzoo, PON pred slope',
    'Microzoo, PON half-sat',
    'Microzoo, pref for uZoo', 'Microzoo, uZoo pred slope',
    'Microzoo, uZoo half-sat',
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
