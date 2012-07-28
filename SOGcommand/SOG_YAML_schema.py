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


@colander.deferred
def deferred_allow_missing(node, kw):
    allow_missing = kw.get('allow_missing')
    return None if allow_missing else colander.required


class _SOG_YAML_Base(colander.MappingSchema):
    """Base class for SOG YAML infile quantities.
    """
    units = colander.SchemaNode(
        colander.String(), default=None,
        missing=None)
    var_name = colander.SchemaNode(
        colander.String(), name='variable_name',
        missing=deferred_allow_missing)
    description = colander.SchemaNode(
        colander.String(),
        missing=deferred_allow_missing)


class _Float(_SOG_YAML_Base):
    value = colander.SchemaNode(colander.Float())


class _Int(_SOG_YAML_Base):
    value = colander.SchemaNode(colander.Int())


class _Boolean(_SOG_YAML_Base):
    value = colander.SchemaNode(colander.Boolean())


class _SOG_String(_SOG_YAML_Base):
    value = colander.SchemaNode(colander.String())


class _DateTime(colander.SchemaType):
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


class _FloatList(colander.SchemaType):
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


class _IntList(colander.SchemaType):
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
        infile_key='init datetime', var_name='initDatetime',
        missing=deferred_allow_missing)
    CTD_file = _SOG_String(
        infile_key='ctd_in', var_name='ctd_in',
        missing=deferred_allow_missing)
    nutrients_file = _SOG_String(
        infile_key='nuts_in', var_name='nuts_in',
        missing=deferred_allow_missing)
    bottle_file = _SOG_String(
        infile_key='botl_in', var_name='botl_in',
        missing=deferred_allow_missing)
    chemistry_file = _SOG_String(
        infile_key='chem_in', var_name='chem_in',
        missing=deferred_allow_missing)
    init_chl_ratios = _SOG_FloatList(
        infile_key='initial chl split', var_name='Psplit',
        missing=deferred_allow_missing)
    nitrate_chl_conversion = _Float(
        infile_key='N2chl', var_name='N2chl',
        missing=deferred_allow_missing)


class _TimeSeriesResults(colander.MappingSchema):
    std_physics = _SOG_String(
        infile_key='std_phys_ts_out', var_name='std_phys_ts_out',
        missing=deferred_allow_missing)
    user_physics = _SOG_String(
        infile_key='user_phys_ts_out', var_name='user_phys_ts_out',
        missing=deferred_allow_missing)
    std_biology = _SOG_String(
        infile_key='std_bio_ts_out', var_name='std_bio_ts_out',
        missing=deferred_allow_missing)
    user_biology = _SOG_String(
        infile_key='user_bio_ts_out', var_name='user_bio_ts_out',
        missing=deferred_allow_missing)
    std_chemistry = _SOG_String(
        infile_key='std_chem_ts_out', var_name='std_chem_ts_out',
        missing=deferred_allow_missing)
    user_chemistry = _SOG_String(
        infile_key='user_chem_ts_out', var_name='user_chem_ts_out',
        missing=deferred_allow_missing)


class _ProfilesResults(colander.MappingSchema):
    num_profiles = _Int(
        infile_key='noprof', var_name='noprof',
        missing=deferred_allow_missing)
    profile_days = _SOG_IntList(
        infile_key='profday', var_name='profileDatetime%yr_day',
        missing=deferred_allow_missing)
    profile_times = _SOG_FloatList(
        infile_key='proftime', var_name='profileDatetime%day_sec',
        missing=deferred_allow_missing)
    profile_file_base = _SOG_String(
        infile_key='profile_base', var_name='profilesBase_fn',
        missing=deferred_allow_missing)
    halocline_file = _SOG_String(
        infile_key='haloclinefile', var_name='haloclines_fn',
        missing=deferred_allow_missing)
    hoffmueller_file = _SOG_String(
        infile_key='Hoffmueller file', var_name='Hoffmueller_fn',
        missing=deferred_allow_missing)
    hoffmueller_start_year = _Int(
        infile_key='Hoffmueller start yr', var_name='Hoff_startyr',
        missing=deferred_allow_missing)
    hoffmueller_start_day = _Int(
        infile_key='Hoffmueller start day', var_name='Hoff_startday',
        missing=deferred_allow_missing)
    hoffmueller_start_sec = _Int(
        infile_key='Hoffmueller start sec', var_name='Hoff_startsec',
        missing=deferred_allow_missing)
    hoffmueller_end_year = _Int(
        infile_key='Hoffmueller end yr', var_name='Hoff_endyr',
        missing=deferred_allow_missing)
    hoffmueller_end_day = _Int(
        infile_key='Hoffmueller end day', var_name='Hoff_endday',
        missing=deferred_allow_missing)
    hoffmueller_end_sec = _Int(
        infile_key='Hoffmueller end sec', var_name='Hoff_endsec',
        missing=deferred_allow_missing)
    hoffmueller_interval = _Float(
        infile_key='Hoffmueller interval', var_name='Hoff_interval',
        missing=deferred_allow_missing)


class _BottomBoundaryConditions(colander.MappingSchema):
    constant_temperature = _Boolean(
        infile_key='temp_constant', var_name='temp_constant',
        missing=deferred_allow_missing)
    temperature_fit_coefficients = _SOG_FloatList(
        infile_key='temperature', var_name='c(:,2)',
        missing=deferred_allow_missing)
    salinity_fit_coefficients = _SOG_FloatList(
        infile_key='salinity', var_name='c(:,1)',
        missing=deferred_allow_missing)
    phyto_fluor_fit_coefficients = _SOG_FloatList(
        infile_key='Phytoplankton', var_name='c(:,3)',
        missing=deferred_allow_missing)
    nitrate_fit_coefficients = _SOG_FloatList(
        infile_key='Nitrate', var_name='c(:,4)',
        missing=deferred_allow_missing)
    silicon_fit_coefficients = _SOG_FloatList(
        infile_key='Silicon', var_name='c(:,5)',
        missing=deferred_allow_missing)
    DIC_fit_coefficients = _SOG_FloatList(
        infile_key='DIC', var_name='c(:,6)',
        missing=deferred_allow_missing)
    dissolved_oxygen_fit_coefficients = _SOG_FloatList(
        infile_key='Oxy', var_name='c(:,7)',
        missing=deferred_allow_missing)
    alkalinity_fit_coefficients = _SOG_FloatList(
        infile_key='Alk', var_name='c(:,8)',
        missing=deferred_allow_missing)
    ammonium_fit_coefficients = _SOG_FloatList(
        infile_key='Ammonium', var_name='c(:,9)',
        missing=deferred_allow_missing)
    phyto_ratio_fit_coefficients = _SOG_FloatList(
        infile_key='Ratio', var_name='c(:,10)',
        missing=deferred_allow_missing)


class _Turbulence(colander.MappingSchema):
    momentum_wave_break_diffusivity = _Float(
        infile_key='nu_w_m', var_name='nu%m%int_wave',
        missing=deferred_allow_missing)
    scalar_wave_break_diffusivity = _Float(
        infile_key='nu_w_s', var_name='nu%T%int_wave, nu%S%int_wave',
        missing=deferred_allow_missing)
    shear_diffusivity_smoothing = _SOG_FloatList(
        infile_key='shear smooth', var_name='shear_diff_smooth',
        missing=deferred_allow_missing)


class _FreshWaterUpwelling(colander.MappingSchema):
    max_upwelling_velocity = _Float(
        infile_key='upwell_const', var_name='upwell_const',
        missing=deferred_allow_missing)
    variation_depth_param = _Float(
        infile_key='d', var_name='d',
        missing=deferred_allow_missing)


class _FreshWaterFlux(colander.MappingSchema):
    mean_total_flow = _Float(
        infile_key='Qbar', var_name='Qbar',
        missing=deferred_allow_missing)
    common_exponent = _Float(
        infile_key='F_SOG', var_name='F_SOG',
        missing=deferred_allow_missing)
    SoG_exponent = _Float(
        infile_key='F_RI', var_name='F_RI',
        missing=deferred_allow_missing)
    scale_factor = _Float(
        infile_key='Fw_scale', var_name='Fw_scale',
        missing=deferred_allow_missing)
    add_freshwater_on_surface = _Boolean(
        infile_key='Fw_surface', var_name='Fw_surface',
        missing=deferred_allow_missing)
    distribution_depth = _Float(
        infile_key='Fw_depth', var_name='Fw_depth',
        missing=deferred_allow_missing)
    include_fresh_water_nutrients = _Boolean(
        infile_key='use_Fw_nutrients', var_name='use_Fw_nutrients',
        missing=deferred_allow_missing)
    northern_return_flow = _Boolean(
        infile_key='northern_return_flow_on', var_name='Northern_return',
        missing=deferred_allow_missing)
    # The next 5 "northern" parameters are only used when
    # northern_return_flow == True
    northern_influence_strength = _Float(
        infile_key='strength_northern', var_name='strength',
        missing=None)
    northern_influence_integration_time_scale = _Float(
        infile_key='tau_northern', var_name='tauN',
        missing=None)
    northern_water_depth_peak = _Float(
        infile_key='depth_northern', var_name='central_depth',
        missing=None)
    northern_water_upper_extension = _Float(
        infile_key='upper_northern', var_name='upper_width',
        missing=None)
    northern_water_lower_extension = _Float(
        infile_key='lower_northern', var_name='lower_width',
        missing=None)


class _SalinityFit(colander.MappingSchema):
    bottom_salinity = _Float(
        infile_key='cbottom', var_name='cbottom',
        missing=deferred_allow_missing)
    alpha = _Float(
        infile_key='calpha', var_name='calpha',
        missing=deferred_allow_missing)
    alpha2 = _Float(
        infile_key='calpha2', var_name='calpha2',
        missing=deferred_allow_missing)
    beta = _Float(
        infile_key='cbeta', var_name='cbeta',
        missing=deferred_allow_missing)
    gamma = _Float(
        infile_key='cgamma', var_name='cgamma',
        missing=deferred_allow_missing)


class _RiverAlkalinityFit(colander.MappingSchema):
    river_alkalinity_zero = _Float(
        infile_key='river_Alk_0', var_name='river_Alk_0',
        missing=deferred_allow_missing)
    river_alkalinity_decay = _Float(
        infile_key='river_Alk_decay', var_name='river_Alk_decay',
        missing=deferred_allow_missing)
    river_pH = _Float(
        infile_key='pH_riv', var_name='pH_riv',
        missing=deferred_allow_missing)


class _FreshWater(colander.MappingSchema):
    upwelling = _FreshWaterUpwelling(
        missing=deferred_allow_missing)
    flux = _FreshWaterFlux(
        missing=deferred_allow_missing)
    salinity_fit = _SalinityFit(
        missing=deferred_allow_missing)
    river_alkalinity_fit = _RiverAlkalinityFit(
        missing=deferred_allow_missing)


class _K_PAR_Fit(colander.MappingSchema):
    ialpha = _Float(
        infile_key='ialpha', var_name='ialpha',
        missing=deferred_allow_missing)
    ibeta = _Float(
        infile_key='ibeta', var_name='ibeta',
        missing=deferred_allow_missing)
    igamma = _Float(
        infile_key='igamma', var_name='igamma',
        missing=deferred_allow_missing)
    isigma = _Float(
        infile_key='isigma', var_name='isigma',
        missing=deferred_allow_missing)
    itheta = _Float(
        infile_key='itheta', var_name='itheta',
        missing=deferred_allow_missing)
    idl = _Float(
        infile_key='idl', var_name='idl',
        missing=deferred_allow_missing)


class _PhysicsParams(colander.MappingSchema):
    bottom_boundary_conditions = _BottomBoundaryConditions(
        missing=deferred_allow_missing)
    turbulence = _Turbulence(
        missing=deferred_allow_missing)
    fresh_water = _FreshWater(
        missing=deferred_allow_missing)
    K_PAR_fit = _K_PAR_Fit(
        missing=deferred_allow_missing)


class _Mesozooplankton(colander.MappingSchema):
    mesozoo_winter_conc = _Float(
        infile_key='Mesozoo, winter conc',
        var_name='rate_mesozoo%winterconc',
        missing=deferred_allow_missing)
    mesozoo_summer_conc = _Float(
        infile_key='Mesozoo, summer conc',
        var_name='rate_mesozoo%summerconc',
        missing=deferred_allow_missing)
    mesozoo_summer_peak_magnitudes = _SOG_FloatList(
        infile_key='Mesozoo, summer peak mag',
        var_name='rate_mesozoo%sumpeakval',
        missing=deferred_allow_missing)
    mesozoo_summer_peak_days = _SOG_FloatList(
        infile_key='Mesozoo, summer peak pos',
        var_name='rate_mesozoo%sumpeakpos',
        missing=deferred_allow_missing)
    mesozoo_summer_peak_widths = _SOG_FloatList(
        infile_key='Mesozoo, summer peak wid',
        var_name='rate_mesozoo%sumpeakwid',
        missing=deferred_allow_missing)
    mesozoo_max_ingestion = _Float(
        infile_key='Mesozoo, max ingestion',
        var_name='rate_mesozoo%R',
        missing=deferred_allow_missing)
    mesozoo_grazing_limit = _Float(
        infile_key='Mesozoo, pred slope',
        var_name='rate_mesozoo%PredSlope',
        missing=deferred_allow_missing)
    mesozoo_grazing_half_saturation = _Float(
        infile_key='Mesozoo, half-sat',
        var_name='rate_mesozoo%HalfSat',
        missing=deferred_allow_missing)
    mesozoo_diatom_preference = _Float(
        infile_key='Mesozoo, pref for diatoms',
        var_name='rate_mesozoo%MicroPref',
        missing=deferred_allow_missing)
    mesozoo_diatom_grazing_limit = _Float(
        infile_key='Mesozoo, micro pred slope',
        var_name='rate_mesozoo%MicroPredSlope',
        missing=deferred_allow_missing)
    mesozoo_diatom_grazing_half_saturation = _Float(
        infile_key='Mesozoo, micro half-sat',
        var_name='rate_mesozoo%MicroHalfSat',
        missing=deferred_allow_missing)
    mesozoo_nano_preference = _Float(
        infile_key='Mesozoo, pref for nano',
        var_name='rate_mesozoo%NanoPref',
        missing=deferred_allow_missing)
    mesozoo_nano_grazing_limit = _Float(
        infile_key='Mesozoo, nano pred slope',
        var_name='rate_mesozoo%NanoPredSlope',
        missing=deferred_allow_missing)
    mesozoo_nano_grazing_half_saturation = _Float(
        infile_key='Mesozoo, nano half-sat',
        var_name='rate_mesozoo%NanoHalfSat',
        missing=deferred_allow_missing)
    mesozoo_PON_preference = _Float(
        infile_key='Mesozoo, pref for PON',
        var_name='rate_mesozoo%PON_Pref',
        missing=deferred_allow_missing)
    mesozoo_PON_grazing_limit = _Float(
        infile_key='Mesozoo, PON pred slope',
        var_name='rate_mesozoo%PON_PredSlope',
        missing=deferred_allow_missing)
    mesozoo_PON_grazing_half_saturation = _Float(
        infile_key='Mesozoo, PON half-sat',
        var_name='rate_mesozoo%PON_HalfSat',
        missing=deferred_allow_missing)
    mesozoo_microzoo_preference = _Float(
        infile_key='Mesozoo, pref for uZoo',
        var_name='rate_mesozoo%Z_Pref',
        missing=deferred_allow_missing)
    mesozoo_microzoo_grazing_limit = _Float(
        infile_key='Mesozoo, uZoo pred slope',
        var_name='rate_mesozoo%Z_PredSlope',
        missing=deferred_allow_missing)
    mesozoo_microzoo_grazing_half_saturation = _Float(
        infile_key='Mesozoo, uZoo half-sat',
        var_name='rate_mesozoo%Z_HalfSat',
        missing=deferred_allow_missing)


class _MesodiniumRubrum(colander.MappingSchema):
    mesorub_max_ingestion = _Float(
        infile_key='Mesorub, max ingestion',
        var_name='rate_mesorub%R',
        missing=deferred_allow_missing)
    mesorub_assimilation_efficiency = _Float(
        infile_key='Mesorub, assimilation eff',
        var_name='rate_mesorub%eff',
        missing=deferred_allow_missing)
    mesorub_grazing_limit = _Float(
        infile_key='Mesorub, nano predslope',
        var_name='rate_mesorub%PicoPredSlope',
        missing=deferred_allow_missing)
    mesorub_grazing_half_saturation = _Float(
        infile_key='Mesorub, nano half-sat',
        var_name='rate_mesorub%PicoHalfSat',
        missing=deferred_allow_missing)


class _Microzooplankton(colander.MappingSchema):
    microzoo_max_ingestion = _Float(
        infile_key='Microzoo, max ingestion',
        var_name='rate_uzoo%R',
        missing=deferred_allow_missing)
    microzoo_assimilation_efficiency = _Float(
        infile_key='Microzoo, assimil. eff',
        var_name='rate_uzoo%eff',
        missing=deferred_allow_missing)
    microzoo_natural_mortality = _Float(
        infile_key='Microzoo, nat mort',
        var_name='rate_uzoo%Rm',
        missing=deferred_allow_missing)
    microzoo_excretion = _Float(
        infile_key='Microzoo, excretion',
        var_name='rate_uzoo%excr',
        missing=deferred_allow_missing)
    microzoo_grazing_limit = _Float(
        infile_key='Microzoo, pred slope',
        var_name='rate_uzoo%PredSlope',
        missing=deferred_allow_missing)
    microzoo_grazing_half_saturation = _Float(
        infile_key='Microzoo, half-sat',
        var_name='Microzoo, half-sat',
        missing=deferred_allow_missing)
    microzoo_pico_preference = _Float(
        infile_key='Microzoo, pref for Pico',
        var_name='rate_uzoo%PicoPref',
        missing=deferred_allow_missing)
    microzoo_pico_grazing_limit = _Float(
        infile_key='uzoo, Pico pred slope',
        var_name='rate_uzoo%PicoPredSlope',
        missing=deferred_allow_missing)
    microzoo_pico_grazing_half_saturation = _Float(
        infile_key='uzoo, Pico half-sat',
        var_name='rate_uzoo%PicoHalfSat',
        missing=deferred_allow_missing)
    microzoo_micro_preference = _Float(
        infile_key='Microzoo, pref for Micro',
        var_name='rate_uzoo%MicroPref',
        missing=deferred_allow_missing)
    microzoo_micro_grazing_limit = _Float(
        infile_key='uzoo, Micro pred slope',
        var_name='rate_uzoo%MicroPredSlope',
        missing=deferred_allow_missing)
    microzoo_micro_grazing_half_saturation = _Float(
        infile_key='Microzoo, Micro half-sat',
        var_name='rate_uzoo%MicroHalfSat',
        missing=deferred_allow_missing)
    microzoo_nano_preference = _Float(
        infile_key='Microzoo, pref for nano',
        var_name='rate_uzoo%NanoPref',
        missing=deferred_allow_missing)
    microzoo_nano_grazing_limit = _Float(
        infile_key='Microzoo, nano pred slope',
        var_name='rate_uzoo%NanoPredSlope',
        missing=deferred_allow_missing)
    microzoo_nano_grazing_half_saturation = _Float(
        infile_key='Microzoo, nano half-sat',
        var_name='rate_uzoo%NanoHalfSat',
        missing=deferred_allow_missing)
    microzoo_PON_preference = _Float(
        infile_key='Microzoo, pref for PON',
        var_name='rate_uzoo%PON_Pref',
        missing=deferred_allow_missing)
    microzoo_PON_grazing_limit = _Float(
        infile_key='Microzoo, PON pred slope',
        var_name='rate_uzoo%PON_PredSlope',
        missing=deferred_allow_missing)
    microzoo_PON_grazing_half_saturation = _Float(
        infile_key='Microzoo, PON half-sat',
        var_name='rate_uzoo%PON_HalfSat',
        missing=deferred_allow_missing)
    microzoo_microzoo_preference = _Float(
        infile_key='Microzoo, pref for uZoo',
        var_name='rate_uzoo%PON_Pref',
        missing=deferred_allow_missing)
    microzoo_microzoo_grazing_limit = _Float(
        infile_key='Microzoo, uZoo pred slope',
        var_name='rate_uzoo%PON_PredSlope',
        missing=deferred_allow_missing)
    microzoo_microzoo_grazing_half_saturation = _Float(
        infile_key='Microzoo, uZoo half-sat',
        var_name='rate_uzoo%PON_HalfSat',
        missing=deferred_allow_missing)


class _PhytoplanktonGrowth(colander.MappingSchema):
    micro_max_growth = _Float(
        infile_key='Micro, max growth',
        var_name='rate_micro%R',
        missing=deferred_allow_missing)
    nano_max_growth = _Float(
        infile_key='Nano, max growth',
        var_name='rate_nano%R',
        missing=deferred_allow_missing)
    pico_max_growth = _Float(
        infile_key='Pico, max growth',
        var_name='rate_pico%R',
        missing=deferred_allow_missing)
    micro_optimal_light = _Float(
        infile_key='Micro, I_opt',
        var_name='rate_micro%Iopt',
        missing=deferred_allow_missing)
    nano_optimal_light = _Float(
        infile_key='Nano, I_opt',
        var_name='rate_nano%Iopt',
        missing=deferred_allow_missing)
    pico_optimal_light = _Float(
        infile_key='Pico, I_opt',
        var_name='rate_pico%Iopt',
        missing=deferred_allow_missing)
    micro_max_temperature = _Float(
        infile_key='Micro, max temp',
        var_name='rate_micro%maxtemp',
        missing=deferred_allow_missing)
    nano_max_temperature = _Float(
        infile_key='Nano, max temp',
        var_name='rate_nano%maxtemp',
        missing=deferred_allow_missing)
    pico_max_temperature = _Float(
        infile_key='Pico, max temp',
        var_name='rate_pico%maxtemp',
        missing=deferred_allow_missing)
    micro_temperature_range = _Float(
        infile_key='Micro, temp range',
        var_name='rate_micro%temprange',
        missing=deferred_allow_missing)
    nano_temperature_range = _Float(
        infile_key='Nano, temp range',
        var_name='rate_nano%temprange',
        missing=deferred_allow_missing)
    pico_temperature_range = _Float(
        infile_key='Pico, temp range',
        var_name='rate_pico%temprange',
        missing=deferred_allow_missing)
    micro_Q10_exponent = _Float(
        infile_key='Micro, Q10 exp',
        var_name='rate_micro%Q10exp',
        missing=deferred_allow_missing)
    nano_Q10_exponent = _Float(
        infile_key='Nano, Q10 exp',
        var_name='rate_nano%Q10exp',
        missing=deferred_allow_missing)
    pico_Q10_exponent = _Float(
        infile_key='Pico, Q10 exp',
        var_name='rate_pico%Q10exp',
        missing=deferred_allow_missing)
    micro_gamma_loss = _Float(
        infile_key='Micro, gamma loss',
        var_name='rate_micro%gamma',
        missing=deferred_allow_missing)
    nano_gamma_loss = _Float(
        infile_key='Nano, gamma loss',
        var_name='rate_nano%gamma',
        missing=deferred_allow_missing)
    pico_gamma_loss = _Float(
        infile_key='Pico, gamma loss',
        var_name='rate_pico%gamma',
        missing=deferred_allow_missing)
    micro_NO3_half_saturation = _Float(
        infile_key='Micro, NO3 k',
        var_name='rate_micro%k',
        missing=deferred_allow_missing)
    nano_NO3_half_saturation = _Float(
        infile_key='Nano, NO3 k',
        var_name='rate_nano%k',
        missing=deferred_allow_missing)
    pico_NO3_half_saturation = _Float(
        infile_key='Pico, NO3 k',
        var_name='rate_pico%k',
        missing=deferred_allow_missing)
    micro_NO3_vs_NH_preference = _Float(
        infile_key='Micro, kapa',
        var_name='rate_micro%kapa',
        missing=deferred_allow_missing)
    nano_NO3_vs_NH_preference = _Float(
        infile_key='Nano, kapa',
        var_name='rate_nano%kapa',
        missing=deferred_allow_missing)
    pico_NO3_vs_NH_preference = _Float(
        infile_key='Pico, kapa',
        var_name='rate_pico%kapa',
        missing=deferred_allow_missing)
    micro_NH_inhibition_exponent = _Float(
        infile_key='Micro, NH inhib',
        var_name='Micro, NH inhib',
        missing=deferred_allow_missing)
    nano_NH_inhibition_exponent = _Float(
        infile_key='Nano, NH inhib',
        var_name='Nano, NH inhib',
        missing=deferred_allow_missing)
    pico_NH_inhibition_exponent = _Float(
        infile_key='Pico, NH inhib',
        var_name='Pico, NH inhib',
        missing=deferred_allow_missing)
    micro_half_saturation = _Float(
        infile_key='Micro, N_o',
        var_name='rate_micro%N_o',
        missing=deferred_allow_missing)
    nano_half_saturation = _Float(
        infile_key='Nano, N_o',
        var_name='rate_nano%N_o',
        missing=deferred_allow_missing)
    pico_half_saturation = _Float(
        infile_key='Pico, N_o',
        var_name='rate_pico%N_o',
        missing=deferred_allow_missing)
    micro_N_inhibition_exponent = _Float(
        infile_key='Micro, N_x',
        var_name='rate_micro%N_x',
        missing=deferred_allow_missing)
    nano_N_inhibition_exponent = _Float(
        infile_key='Nano, N_x',
        var_name='rate_nano%N_x',
        missing=deferred_allow_missing)
    pico_N_inhibition_exponent = _Float(
        infile_key='Pico, N_x',
        var_name='rate_pico%N_x',
        missing=deferred_allow_missing)
    micro_Si_N_ratio = _Float(
        infile_key='Micro, Si ratio',
        var_name='rate_micro%Si_ratio',
        missing=deferred_allow_missing)
    nano_Si_N_ratio = _Float(
        infile_key='Nano, Si ratio',
        var_name='rate_nano%Si_ratio',
        missing=deferred_allow_missing)
    pico_Si_N_ratio = _Float(
        infile_key='Pico, Si ratio',
        var_name='rate_pico%Si_ratio',
        missing=deferred_allow_missing)
    micro_Si_half_saturation = _Float(
        infile_key='Micro, K Si',
        var_name='rate_micro%K_Si',
        missing=deferred_allow_missing)
    nano_Si_half_saturation = _Float(
        infile_key='Nano, K Si',
        var_name='rate_nano%K_Si',
        missing=deferred_allow_missing)
    pico_Si_half_saturation = _Float(
        infile_key='Pico, K Si',
        var_name='rate_pico%K_Si',
        missing=deferred_allow_missing)
    micro_natural_mortality = _Float(
        infile_key='Micro, nat mort',
        var_name='rate_micro%Rm',
        missing=deferred_allow_missing)
    nano_natural_mortality = _Float(
        infile_key='Nano, nat mort',
        var_name='rate_nano%Rm',
        missing=deferred_allow_missing)
    pico_natural_mortality = _Float(
        infile_key='Pico, nat mort',
        var_name='rate_pico%Rm',
        missing=deferred_allow_missing)


class _RemineralizationRates(colander.MappingSchema):
    NH_remin_rate = _Float(
        infile_key='NH remin rate', var_name='remin%NH',
        missing=deferred_allow_missing)
    DON_remin_rate = _Float(
        infile_key='DON remin rate', var_name='remin%D_DON',
        missing=deferred_allow_missing)
    PON_remin_rate = _Float(
        infile_key='PON remin rate', var_name='remin%D_PON',
        missing=deferred_allow_missing)
    bSi_remin_rate = _Float(
        infile_key='bSi remin rate', var_name='remin%D_bSi',
        missing=deferred_allow_missing)


class _PhytoplanktonMortalityWaste(colander.MappingSchema):
    micro_mort_NH = _Float(
        infile_key='Waste, dnm, NH', var_name='frac_waste_DNM%NH',
        missing=deferred_allow_missing)
    micro_mort_DON = _Float(
        infile_key='Waste, dnm, DON', var_name='frac_waste_DNM%DON',
        missing=deferred_allow_missing)
    micro_mort_PON = _Float(
        infile_key='Waste, dnm, PON', var_name='frac_waste_DNM%PON',
        missing=deferred_allow_missing)
    micro_mort_refr = _Float(
        infile_key='Waste, dnm, Ref', var_name='frac_waste_DNM%Ref',
        missing=deferred_allow_missing)
    micro_mort_bSi = _Float(
        infile_key='Waste, dnm, Bsi', var_name='frac_waste_DNM%Bsi',
        missing=deferred_allow_missing)
    nano_mort_NH = _Float(
        infile_key='Waste, nnm, NH', var_name='frac_waste_NNM%NH',
        missing=deferred_allow_missing)
    nano_mort_DON = _Float(
        infile_key='Waste, nnm, DON', var_name='frac_waste_NNM%DON',
        missing=deferred_allow_missing)
    nano_mort_PON = _Float(
        infile_key='Waste, nnm, PON', var_name='frac_waste_NNM%PON',
        missing=deferred_allow_missing)
    nano_mort_refr = _Float(
        infile_key='Waste, nnm, Ref', var_name='frac_waste_NNM%Ref',
        missing=deferred_allow_missing)
    nano_mort_bSi = _Float(
        infile_key='Waste, nnm, Bsi', var_name='frac_waste_NNM%Bsi',
        missing=deferred_allow_missing)
    pico_mort_NH = _Float(
        infile_key='Waste, fnm, NH', var_name='frac_waste_FNM%NH',
        missing=deferred_allow_missing)
    pico_mort_DON = _Float(
        infile_key='Waste, fnm, DON', var_name='frac_waste_FNM%DON',
        missing=deferred_allow_missing)
    pico_mort_PON = _Float(
        infile_key='Waste, fnm, PON', var_name='frac_waste_FNM%PON',
        missing=deferred_allow_missing)
    pico_mort_refr = _Float(
        infile_key='Waste, fnm, Ref', var_name='frac_waste_FNM%Ref',
        missing=deferred_allow_missing)
    pico_mort_bSi = _Float(
        infile_key='Waste, fnm, Bsi', var_name='frac_waste_FNM%Bsi',
        missing=deferred_allow_missing)


class _MicrozooplanktonWaste(colander.MappingSchema):
    microzoo_mort_NH = _Float(
        infile_key='Waste, znm, NH', var_name='frac_waste_ZNM%NH',
        missing=deferred_allow_missing)
    microzoo_mort_DON = _Float(
        infile_key='Waste, znm, DON', var_name='frac_waste_ZNM%DON',
        missing=deferred_allow_missing)
    microzoo_mort_PON = _Float(
        infile_key='Waste, znm, PON', var_name='frac_waste_ZNM%PON',
        missing=deferred_allow_missing)
    microzoo_mort_refr = _Float(
        infile_key='Waste, znm, Ref', var_name='frac_waste_ZNM%Ref',
        missing=deferred_allow_missing)
    microzoo_mort_bSi = _Float(
        infile_key='Waste, znm, Bsi', var_name='frac_waste_ZNM%Bsi',
        missing=deferred_allow_missing)
    microzoo_excrete_NH = _Float(
        infile_key='Waste, zex, NH', var_name='frac_waste_ZEX%NH',
        missing=deferred_allow_missing)
    microzoo_excrete_DON = _Float(
        infile_key='Waste, zex, DON', var_name='frac_waste_ZEX%DON',
        missing=deferred_allow_missing)
    microzoo_excrete_PON = _Float(
        infile_key='Waste, zex, PON', var_name='frac_waste_ZEX%PON',
        missing=deferred_allow_missing)
    microzoo_excrete_refr = _Float(
        infile_key='Waste, zex, Ref', var_name='frac_waste_ZEX%Ref',
        missing=deferred_allow_missing)
    microzoo_excrete_bSi = _Float(
        infile_key='Waste, zex, Bsi', var_name='frac_waste_ZEX%Bsi',
        missing=deferred_allow_missing)


class _SloppyEating(colander.MappingSchema):
    mesozoo_microphyto_grazing_NH = _Float(
        infile_key='Waste, dem, NH', var_name='frac_waste_DEM%NH',
        missing=deferred_allow_missing)
    mesozoo_microphyto_grazing_DON = _Float(
        infile_key='Waste, dem, DON', var_name='frac_waste_DEM%DON',
        missing=deferred_allow_missing)
    mesozoo_microphyto_grazing_PON = _Float(
        infile_key='Waste, dem, PON', var_name='frac_waste_DEM%PON',
        missing=deferred_allow_missing)
    mesozoo_microphyto_grazing_refr = _Float(
        infile_key='Waste, dem, Ref', var_name='frac_waste_DEM%Ref',
        missing=deferred_allow_missing)
    mesozoo_microphyto_grazing_bSi = _Float(
        infile_key='Waste, dem, Bsi', var_name='frac_waste_DEM%Bsi',
        missing=deferred_allow_missing)
    mesozoo_nanophyto_grazing_NH = _Float(
        infile_key='Waste, nem, NH', var_name='frac_waste_NEM%NH',
        missing=deferred_allow_missing)
    mesozoo_nanophyto_grazing_DON = _Float(
        infile_key='Waste, nem, DON', var_name='frac_waste_NEM%DON',
        missing=deferred_allow_missing)
    mesozoo_nanophyto_grazing_PON = _Float(
        infile_key='Waste, nem, PON', var_name='frac_waste_NEM%PON',
        missing=deferred_allow_missing)
    mesozoo_nanophyto_grazing_refr = _Float(
        infile_key='Waste, nem, Ref', var_name='frac_waste_NEM%Ref',
        missing=deferred_allow_missing)
    mesozoo_nanophyto_grazing_bSi = _Float(
        infile_key='Waste, nem, Bsi', var_name='frac_waste_NEM%Bsi',
        missing=deferred_allow_missing)
    mesozoo_PON_grazing_NH = _Float(
        infile_key='Waste, pem, NH', var_name='frac_waste_PEM%NH',
        missing=deferred_allow_missing)
    mesozoo_PON_grazing_DON = _Float(
        infile_key='Waste, pem, DON', var_name='frac_waste_PEM%DON',
        missing=deferred_allow_missing)
    mesozoo_PON_grazing_PON = _Float(
        infile_key='Waste, pem, PON', var_name='frac_waste_PEM%PON',
        missing=deferred_allow_missing)
    mesozoo_PON_grazing_refr = _Float(
        infile_key='Waste, pem, Ref', var_name='frac_waste_PEM%Ref',
        missing=deferred_allow_missing)
    mesozoo_PON_grazing_bSi = _Float(
        infile_key='Waste, pem, Bsi', var_name='frac_waste_PEM%Bsi',
        missing=deferred_allow_missing)
    mesozoo_microzoo_grazing_NH = _Float(
        infile_key='Waste, zem, NH', var_name='frac_waste_ZEM%NH',
        missing=deferred_allow_missing)
    mesozoo_microzoo_grazing_DON = _Float(
        infile_key='Waste, zem, DON', var_name='frac_waste_ZEM%DON',
        missing=deferred_allow_missing)
    mesozoo_microzoo_grazing_PON = _Float(
        infile_key='Waste, zem, PON', var_name='frac_waste_ZEM%PON',
        missing=deferred_allow_missing)
    mesozoo_microzoo_grazing_refr = _Float(
        infile_key='Waste, zem, Ref', var_name='frac_waste_ZEM%Ref',
        missing=deferred_allow_missing)
    mesozoo_microzoo_grazing_bSi = _Float(
        infile_key='Waste, zem, Bsi', var_name='frac_waste_ZEM%Bsi',
        missing=deferred_allow_missing)
    microzoo_microphyto_grazing_NH = _Float(
        infile_key='Waste, dez, NH', var_name='frac_waste_DEZ%NH',
        missing=deferred_allow_missing)
    microzoo_microphyto_grazing_DON = _Float(
        infile_key='Waste, dez, DON', var_name='frac_waste_DEZ%DON',
        missing=deferred_allow_missing)
    microzoo_microphyto_grazing_PON = _Float(
        infile_key='Waste, dez, PON', var_name='frac_waste_DEZ%PON',
        missing=deferred_allow_missing)
    microzoo_microphyto_grazing_refr = _Float(
        infile_key='Waste, dez, Ref', var_name='frac_waste_DEZ%Ref',
        missing=deferred_allow_missing)
    microzoo_microphyto_grazing_bSi = _Float(
        infile_key='Waste, dez, Bsi', var_name='frac_waste_DEZ%Bsi',
        missing=deferred_allow_missing)
    microzoo_nanophyto_grazing_NH = _Float(
        infile_key='Waste, nez, NH', var_name='frac_waste_NEZ%NH',
        missing=deferred_allow_missing)
    microzoo_nanophyto_grazing_DON = _Float(
        infile_key='Waste, nez, DON', var_name='frac_waste_NEZ%DON',
        missing=deferred_allow_missing)
    microzoo_nanophyto_grazing_PON = _Float(
        infile_key='Waste, nez, PON', var_name='frac_waste_NEZ%PON',
        missing=deferred_allow_missing)
    microzoo_nanophyto_grazing_refr = _Float(
        infile_key='Waste, nez, Ref', var_name='frac_waste_NEZ%Ref',
        missing=deferred_allow_missing)
    microzoo_nanophyto_grazing_bSi = _Float(
        infile_key='Waste, nez, Bsi', var_name='frac_waste_NEZ%Bsi',
        missing=deferred_allow_missing)
    microzoo_picophyto_grazing_NH = _Float(
        infile_key='Waste, fez, NH', var_name='frac_waste_FEZ%NH',
        missing=deferred_allow_missing)
    microzoo_picophyto_grazing_DON = _Float(
        infile_key='Waste, fez, DON', var_name='frac_waste_FEZ%DON',
        missing=deferred_allow_missing)
    microzoo_picophyto_grazing_PON = _Float(
        infile_key='Waste, fez, PON', var_name='frac_waste_FEZ%PON',
        missing=deferred_allow_missing)
    microzoo_picophyto_grazing_refr = _Float(
        infile_key='Waste, fez, Ref', var_name='frac_waste_FEZ%Ref',
        missing=deferred_allow_missing)
    microzoo_picophyto_grazing_bSi = _Float(
        infile_key='Waste, fez, Bsi', var_name='frac_waste_FEZ%Bsi',
        missing=deferred_allow_missing)
    microzoo_PON_grazing_NH = _Float(
        infile_key='Waste, pez, NH', var_name='frac_waste_PEZ%NH',
        missing=deferred_allow_missing)
    microzoo_PON_grazing_DON = _Float(
        infile_key='Waste, pez, DON', var_name='frac_waste_PEZ%DON',
        missing=deferred_allow_missing)
    microzoo_PON_grazing_PON = _Float(
        infile_key='Waste, pez, PON', var_name='frac_waste_PEZ%PON',
        missing=deferred_allow_missing)
    microzoo_PON_grazing_refr = _Float(
        infile_key='Waste, pez, Ref', var_name='frac_waste_PEZ%Ref',
        missing=deferred_allow_missing)
    microzoo_PON_grazing_bSi = _Float(
        infile_key='Waste, pez, Bsi', var_name='frac_waste_PEZ%Bsi',
        missing=deferred_allow_missing)
    microzoo_microzoo_grazing_NH = _Float(
        infile_key='Waste, zez, NH', var_name='frac_waste_ZEZ%NH',
        missing=deferred_allow_missing)
    microzoo_microzoo_grazing_DON = _Float(
        infile_key='Waste, zez, DON', var_name='frac_waste_ZEZ%DON',
        missing=deferred_allow_missing)
    microzoo_microzoo_grazing_PON = _Float(
        infile_key='Waste, zez, PON', var_name='frac_waste_ZEZ%PON',
        missing=deferred_allow_missing)
    microzoo_microzoo_grazing_refr = _Float(
        infile_key='Waste, zez, Ref', var_name='frac_waste_ZEZ%Ref',
        missing=deferred_allow_missing)
    microzoo_microzoo_grazing_bSi = _Float(
        infile_key='Waste, zez, Bsi', var_name='frac_waste_ZEZ%Bsi',
        missing=deferred_allow_missing)
    mesorub_picophyto_grazing_NH = _Float(
        infile_key='Waste, fen, NH', var_name='frac_waste_FEN%NH',
        missing=deferred_allow_missing)
    mesorub_picophyto_grazing_DON = _Float(
        infile_key='Waste, fen, DON', var_name='frac_waste_FEN%DON',
        missing=deferred_allow_missing)
    mesorub_picophyto_grazing_PON = _Float(
        infile_key='Waste, fen, PON', var_name='frac_waste_FEN%PON',
        missing=deferred_allow_missing)
    mesorub_picophyto_grazing_refr = _Float(
        infile_key='Waste, fen, Ref', var_name='frac_waste_FEN%Ref',
        missing=deferred_allow_missing)
    mesorub_picophyto_grazing_bSi = _Float(
        infile_key='Waste, fen, Bsi', var_name='frac_waste_FEN%Bsi',
        missing=deferred_allow_missing)


class _SinkingRates(colander.MappingSchema):
    microphyto_min_sink_rate = _Float(
        infile_key='Micro min sink rate', var_name='w_sink%Pmicro_min',
        missing=deferred_allow_missing)
    microphyto_max_sink_rate = _Float(
        infile_key='Micro max sink rate', var_name='w_sink%Pmicro_max',
        missing=deferred_allow_missing)
    PON_sink_rate = _Float(
        infile_key='PON sink rate', var_name='w_sink%D_PON',
        missing=deferred_allow_missing)
    refr_sink_rate = _Float(
        infile_key='refr sink rate', var_name='w_sink%D_refr',
        missing=deferred_allow_missing)
    bSi_sink_rate = _Float(
        infile_key='bSi sink rate', var_name='w_sink%D_bSi',
        missing=deferred_allow_missing)


class _BiologyParams(colander.MappingSchema):
    include_phytoplankton = _Boolean(
        infile_key='biology', var_name='biology',
        missing=deferred_allow_missing)
    include_flagellates = _Boolean(
        infile_key='flagellates_on', var_name='flagellates',
        missing=deferred_allow_missing)
    include_remineralization = _Boolean(
        infile_key='remineralization', var_name='remineralization',
        missing=deferred_allow_missing)
    include_microzooplankton = _Boolean(
        infile_key='use microzooplankton', var_name='microzooplankton',
        missing=deferred_allow_missing)
    single_species_light = _Boolean(
        infile_key='single species light', var_name='strong_limitation',
        missing=deferred_allow_missing)
    mesozooplankton = _Mesozooplankton(
        missing=deferred_allow_missing)
    mesodinium_rubrum = _MesodiniumRubrum(
        missing=deferred_allow_missing)
    microzooplankton = _Microzooplankton(
        missing=deferred_allow_missing)
    phytoplankton_growth = _PhytoplanktonGrowth(
        missing=deferred_allow_missing)
    remineralization_rates = _RemineralizationRates(
        missing=deferred_allow_missing)
    phytoplankton_mortality_waste = _PhytoplanktonMortalityWaste(
        missing=deferred_allow_missing)
    microzooplankton_waste = _MicrozooplanktonWaste(
        missing=deferred_allow_missing)
    sloppy_eating = _SloppyEating(
        missing=deferred_allow_missing)
    sinking_rates = _SinkingRates(
        missing=deferred_allow_missing)


class _Location(colander.MappingSchema):
    latitude = _Float(
        infile_key='latitude', var_name='latitude',
        missing=deferred_allow_missing)
    minor_axis = _Float(
        infile_key='Lx', var_name='Lx',
        missing=deferred_allow_missing)
    major_axis = _Float(
        infile_key='Ly', var_name='Ly',
        missing=deferred_allow_missing)
    open_ended_estuary = _Boolean(
        infile_key='openEnd', var_name='openEnd',
        missing=deferred_allow_missing)


class _Grid(colander.MappingSchema):
    model_depth = _Float(
        infile_key='maxdepth', var_name='grid%D',
        missing=deferred_allow_missing)
    grid_size = _Int(
        infile_key='gridsize', var_name='grid%M',
        missing=deferred_allow_missing)
    lambda_factor = _Float(
        infile_key='lambda', var_name='lambda',
        missing=deferred_allow_missing)


class _Numerics(colander.MappingSchema):
    dt = _Int(
        infile_key='dt', var_name='dt',
        missing=deferred_allow_missing)
    chem_dt = _Int(
        infile_key='chem_dt', var_name='chem_dt',
        missing=deferred_allow_missing)
    max_iter = _Int(
        infile_key='max_iter', var_name='max_iter',
        missing=deferred_allow_missing)


class _ForcingData(colander.MappingSchema):
    use_average_forcing_data = _SOG_String(
        infile_key='use average/hist forcing',
        var_name='use_average_forcing_data',
        missing=deferred_allow_missing)
    wind_forcing_file = _SOG_String(
        infile_key='wind', var_name='n/a',
        missing=deferred_allow_missing)
    air_temperature_forcing_file = _SOG_String(
        infile_key='air temp', var_name='n/a',
        missing=deferred_allow_missing)
    cloud_fraction_forcing_file = _SOG_String(
        infile_key='cloud', var_name='n/a',
        missing=deferred_allow_missing)
    humidity_forcing_file = _SOG_String(
        infile_key='humidity', var_name='n/a',
        missing=deferred_allow_missing)
    humidity_forcing_file = _SOG_String(
        infile_key='humidity', var_name='n/a',
        missing=deferred_allow_missing)
    major_river_forcing_file = _SOG_String(
        infile_key='major river', var_name='n/a',
        missing=deferred_allow_missing)
    use_river_temperature = _Boolean(
        infile_key='use river temp', var_name='UseRiverTemp',
        missing=deferred_allow_missing)
    minor_river_forcing_file = _SOG_String(
        infile_key='minor river', var_name='n/a',
        missing=deferred_allow_missing)
    minor_river_integration_days = _Int(
        infile_key='minor river integ days', var_name='integ_days',
        missing=deferred_allow_missing)
    alt_minor_river_forcing_file = _SOG_String(
        infile_key='alt minor river', var_name='n/a',
        missing=deferred_allow_missing)


class _ForcingVariation(colander.MappingSchema):
    wind = _Boolean(
        infile_key='vary%wind%enabled', var_name='vary%wind%enabled',
        missing=deferred_allow_missing)
    # Selector for type of wind variation; only used when wind == True
    wind_fixed = _Boolean(
        infile_key='vary%wind%fixed', var_name='vary%wind%fixed',
        missing=None)
    # Fixed value for wind variation is only used when wind == True
    # and wind_fixed == True
    wind_value = _Float(
        infile_key='vary%wind%value', var_name='vary%wind%value',
        missing=None)
    # Shift, fraction and addition values for wind variation are only
    # used when wind == True and wind_fixed == False
    wind_shift = _Float(
        infile_key='vary%wind%shift', var_name='vary%wind%shift',
        missing=None)
    wind_fraction = _Float(
        infile_key='vary%wind%fraction', var_name='vary%wind%fraction',
        missing=None)
    wind_addition = _Float(
        infile_key='vary%wind%addition', var_name='vary%wind%addition',
        missing=None)
    cloud_fraction = _Boolean(
        infile_key='vary%cf%enabled', var_name='vary%cf%enabled',
        missing=deferred_allow_missing)
    river_flows = _Boolean(
        infile_key='vary%rivers%enabled', var_name='vary%rivers%enabled',
        missing=deferred_allow_missing)
    temperature = _Boolean(
        infile_key='vary%temperature%enabled',
        var_name='vary%temperature%enabled',
        missing=deferred_allow_missing)


class YAML_Infile(colander.MappingSchema):
    initial_conditions = _InitialConditions(
        missing=deferred_allow_missing)
    end_datetime = _SOG_Datetime(
        infile_key='end datetime', var_name='endDatetime',
        missing=deferred_allow_missing)
    location = _Location(
        missing=deferred_allow_missing)
    grid = _Grid(
        missing=deferred_allow_missing)
    numerics = _Numerics(
        missing=deferred_allow_missing)
    vary = _ForcingVariation(
        missing=deferred_allow_missing)
    timeseries_results = _TimeSeriesResults(
        missing=deferred_allow_missing)
    profiles_results = _ProfilesResults(
        missing=deferred_allow_missing)
    physics = _PhysicsParams(
        missing=deferred_allow_missing)
    biology = _BiologyParams(
        missing=deferred_allow_missing)
    forcing_data = _ForcingData(
        missing=deferred_allow_missing)


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
