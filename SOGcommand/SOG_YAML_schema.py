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


class _SOG_String(_SOG_YAML_Base):
    value = colander.SchemaNode(colander.String())


class _DateTime(object):
    """Replacement for Colander's ISO8601 DateTime type.

    We don't care about time zone, and want the string representation
    of a datetime to be `yyy-mm-dd hh:mm:ss`.
    """
    def serialize(self, node, appstruct):
        if appstruct is colander.null:
            return colander.null
        if not isinstance(appstruct, datetime):
            raise colander.Invalid(
                node, '{0!r} is not a datetime'.format(appstruct))
        return appstruct

    def deserialize(self, node, cstruct):
        if cstruct is colander.null:
            return colander.null
        if not isinstance(cstruct, datetime):
            raise colander.Invalid(
                node, '{0!r} is not a datetime'.format(cstruct))
        return cstruct


class _SOG_Datetime(_SOG_YAML_Base):
    value = colander.SchemaNode(_DateTime())


class _FloatList(object):
    """SOG list of floats type.

    Validates that we're working with a list of numbers.
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
        return appstruct

    def deserialize(self, node, cstruct):
        if cstruct is colander.null:
            return colander.null
        if not isinstance(cstruct, list):
            raise colander.Invalid(
                node, '{0!r} is not a list'.format(cstruct))
        if not all(isinstance(item, (int, float)) for item in cstruct):
            raise colander.Invalid(
                node, '{0!r} contains item that is not a number'
                .format(cstruct))
        return cstruct


class _SOG_FloatList(_SOG_YAML_Base):
    value = colander.SchemaNode(_FloatList())


class _IntList(object):
    """SOG list of ints type.

    Validates that we're working with a list of integers.
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
        return appstruct

    def deserialize(self, node, cstruct):
        if cstruct is colander.null:
            return colander.null
        if not isinstance(cstruct, list):
            raise colander.Invalid(
                node, '{0!r} is not a list'.format(cstruct))
        if not all(isinstance(item, int) for item in cstruct):
            raise colander.Invalid(
                node, '{0!r} contains item that is not an integer'
                .format(cstruct))
        return cstruct


class _SOG_IntList(_SOG_YAML_Base):
    value = colander.SchemaNode(_IntList())


class _InitialConditions(colander.MappingSchema):
    init_datetime = _SOG_Datetime(
        infile_key='init datetime', var_name='initDatetime')
    CTD_file = _SOG_String(infile_key='ctd_in', var_name='ctd_in')
    nutrients_file = _SOG_String(infile_key='nuts_in', var_name='nuts_in')
    bottle_file = _SOG_String(infile_key='botl_in', var_name='botl_in')
    chemistry_file = _SOG_String(infile_key='chem_in', var_name='chem_in')
    init_chl_ratios = _SOG_FloatList(
        infile_key='initial chl split', var_name='Psplit')
    nitrate_chl_conversion = _Float(infile_key='N2chl', var_name='N2chl')


class _TimeSeriesResults(colander.MappingSchema):
    std_physics = _SOG_String(
        infile_key='std_phys_ts_out', var_name='std_phys_ts_out')
    user_physics = _SOG_String(
        infile_key='user_phys_ts_out', var_name='user_phys_ts_out')
    std_biology = _SOG_String(
        infile_key='std_bio_ts_out', var_name='std_bio_ts_out')
    user_biology = _SOG_String(
        infile_key='user_bio_ts_out', var_name='user_bio_ts_out')
    std_chemistry = _SOG_String(
        infile_key='std_chem_ts_out', var_name='std_chem_ts_out')


class _ProfilesResults(colander.MappingSchema):
    num_profiles = _Int(infile_key='noprof', var_name='noprof')
    profile_days = _SOG_IntList(
        infile_key='profday', var_name='profileDatetime%yr_day')
    profile_times = _SOG_FloatList(
        infile_key='proftime', var_name='profileDatetime%day_sec')
    profile_file_base = _SOG_String(
        infile_key='profile_base', var_name='profilesBase_fn')
    halocline_file = _SOG_String(
        infile_key='haloclinefile', var_name='haloclines_fn')
    hoffmueller_file = _SOG_String(
        infile_key='Hoffmueller file', var_name='Hoffmueller_fn')
    hoffmueller_start_year = _Int(
        infile_key='Hoffmueller start yr', var_name='Hoff_startyr')
    hoffmueller_start_day = _Int(
        infile_key='Hoffmueller start day', var_name='Hoff_startday')
    hoffmueller_start_sec = _Int(
        infile_key='Hoffmueller start sec', var_name='Hoff_startsec')
    hoffmueller_end_year = _Int(
        infile_key='Hoffmueller end yr', var_name='Hoff_endyr')
    hoffmueller_end_day = _Int(
        infile_key='Hoffmueller end day', var_name='Hoff_endday')
    hoffmueller_end_sec = _Int(
        infile_key='Hoffmueller end sec', var_name='Hoff_endsec')
    hoffmueller_interval = _Float(
        infile_key='Hoffmueller interval', var_name='Hoff_interval')


class _BottomBoundaryConditions(colander.MappingSchema):
    constant_temperature = _Boolean(
        infile_key='temp_constant', var_name='temp_constant')
    temperature_fit_coefficients = _SOG_FloatList(
        infile_key='temperature', var_name='c(:,2)')
    salinity_fit_coefficients = _SOG_FloatList(
        infile_key='salinity', var_name='c(:,1)')
    phyto_fluor_fit_coefficients = _SOG_FloatList(
        infile_key='Phytoplankton', var_name='c(:,3)')
    nitrate_fit_coefficients = _SOG_FloatList(
        infile_key='Nitrate', var_name='c(:,4)')
    silicon_fit_coefficients = _SOG_FloatList(
        infile_key='Silicon', var_name='c(:,5)')
    DIC_fit_coefficients = _SOG_FloatList(
        infile_key='DIC', var_name='c(:,6)')
    dissolved_oxygen_fit_coefficients = _SOG_FloatList(
        infile_key='Oxy', var_name='c(:,7)')
    alkalinity_fit_coefficients = _SOG_FloatList(
        infile_key='Alk', var_name='c(:,8)')
    ammonium_fit_coefficients = _SOG_FloatList(
        infile_key='Ammonium', var_name='c(:,9)')
    phyto_ratio_fit_coefficients = _SOG_FloatList(
        infile_key='Ratio', var_name='c(:,10)')


class _Turbulence(colander.MappingSchema):
    momentum_wave_break_diffusivity = _Float(
        infile_key='nu_w_m', var_name='nu%m%int_wave')
    scalar_wave_break_diffusivity = _Float(
        infile_key='nu_w_s', var_name='nu%T%int_wave, nu%S%int_wave')
    shear_diffusivity_smoothing = _SOG_FloatList(
        infile_key='shear smooth', var_name='shear_diff_smooth')


class _PhysicsParams(colander.MappingSchema):
    bottom_boundary_conditions = _BottomBoundaryConditions()
    turbulence = _Turbulence()


class _Location(colander.MappingSchema):
    latitude = _Float(infile_key='latitude', var_name='latitude')
    minor_axis = _Float(infile_key='Lx', var_name='Lx')
    major_axis = _Float(infile_key='Ly', var_name='Ly')
    open_ended_estuary = _Boolean(infile_key='openEnd', var_name='openEnd')


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
    timeseries_results = _TimeSeriesResults()
    profiles_results = _ProfilesResults()
    physics = _PhysicsParams()


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
