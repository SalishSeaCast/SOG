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


class _FreshWaterUpwelling(colander.MappingSchema):
    max_upwelling_velocity = _Float(
        infile_key='upwell_const', var_name='upwell_const')
    variation_depth_param = _Float(infile_key='d', var_name='d')


class _FreshWaterFlux(colander.MappingSchema):
    mean_total_flow = _Float(infile_key='Qbar', var_name='Qbar')
    common_exponent = _Float(infile_key='F_SOG', var_name='F_SOG')
    SoG_exponent = _Float(infile_key='F_RI', var_name='F_RI')
    scale_factor = _Float(infile_key='Fw_scale', var_name='Fw_scale')
    add_freshwater_on_surface = _Boolean(
        infile_key='Fw_surface', var_name='Fw_surface')
    distribution_depth = _Float(infile_key='Fw_depth', var_name='Fw_depth')
    northern_return_flow = _Boolean(
        infile_key='northern_return_flow_on', var_name='Northern_return')
    include_fresh_water_nutrients = _Boolean(
        infile_key='use_Fw_nutrients', var_name='use_Fw_nutrients')


class _SalinityFit(colander.MappingSchema):
    bottom_salinity = _Float(infile_key='cbottom', var_name='cbottom')
    alpha = _Float(infile_key='calpha', var_name='calpha')
    alpha2 = _Float(infile_key='calpha2', var_name='calpha2')
    beta = _Float(infile_key='cbeta', var_name='cbeta')
    gamma = _Float(infile_key='cgamma', var_name='cgamma')


class _FreshWater(colander.MappingSchema):
    upwelling = _FreshWaterUpwelling()
    flux = _FreshWaterFlux()
    salinity_fit = _SalinityFit()


class _K_PAR_Fit(colander.MappingSchema):
    ialpha = _Float(infile_key='ialpha', var_name='ialpha')
    ibeta = _Float(infile_key='ibeta', var_name='ibeta')
    igamma = _Float(infile_key='igamma', var_name='igamma')
    isigma = _Float(infile_key='isigma', var_name='isigma')
    itheta = _Float(infile_key='itheta', var_name='itheta')
    idl = _Float(infile_key='idl', var_name='idl')


class _PhysicsParams(colander.MappingSchema):
    bottom_boundary_conditions = _BottomBoundaryConditions()
    turbulence = _Turbulence()
    fresh_water = _FreshWater()
    K_PAR_fit = _K_PAR_Fit()


class _Mesozooplankton(colander.MappingSchema):
    mesozoo_winter_conc = _Float(
        infile_key='Mesozoo, winter conc',
        var_name='rate_mesozoo%winterconc')
    mesozoo_summer_conc = _Float(
        infile_key='Mesozoo, summer conc',
        var_name='rate_mesozoo%summerconc')
    mesozoo_summer_peak_magnitudes = _SOG_FloatList(
        infile_key='Mesozoo, summer peak mag',
        var_name='rate_mesozoo%sumpeakval')
    mesozoo_summer_peak_days = _SOG_FloatList(
        infile_key='Mesozoo, summer peak pos',
        var_name='rate_mesozoo%sumpeakpos')
    mesozoo_summer_peak_widths = _SOG_FloatList(
        infile_key='Mesozoo, summer peak wid',
        var_name='rate_mesozoo%sumpeakwid')
    mesozoo_max_ingestion = _Float(
        infile_key='Mesozoo, max ingestion',
        var_name='rate_mesozoo%R')
    mesozoo_grazing_limit = _Float(
        infile_key='Mesozoo, pred slope',
        var_name='rate_mesozoo%PredSlope')
    mesozoo_grazing_half_saturation = _Float(
        infile_key='Mesozoo, half-sat',
        var_name='rate_mesozoo%HalfSat')
    mesozoo_diatom_preference = _Float(
        infile_key='Mesozoo, pref for diatoms',
        var_name='rate_mesozoo%MicroPref')
    mesozoo_diatom_grazing_limit = _Float(
        infile_key='Mesozoo, micro pred slope',
        var_name='rate_mesozoo%MicroPredSlope')
    mesozoo_diatom_grazing_half_saturation = _Float(
        infile_key='Mesozoo, micro half-sat',
        var_name='rate_mesozoo%MicroHalfSat')
    mesozoo_nano_preference = _Float(
        infile_key='Mesozoo, pref for nano',
        var_name='rate_mesozoo%NanoPref')
    mesozoo_nano_grazing_limit = _Float(
        infile_key='Mesozoo, nano pred slope',
        var_name='rate_mesozoo%NanoPredSlope')
    mesozoo_nano_grazing_half_saturation = _Float(
        infile_key='Mesozoo, nano half-sat',
        var_name='rate_mesozoo%NanoHalfSat')
    mesozoo_PON_preference = _Float(
        infile_key='Mesozoo, pref for PON',
        var_name='rate_mesozoo%PON_Pref')
    mesozoo_PON_grazing_limit = _Float(
        infile_key='Mesozoo, PON pred slope',
        var_name='rate_mesozoo%PON_PredSlope')
    mesozoo_PON_grazing_half_saturation = _Float(
        infile_key='Mesozoo, PON half-sat',
        var_name='rate_mesozoo%PON_HalfSat')
    mesozoo_microzoo_preference = _Float(
        infile_key='Mesozoo, pref for uZoo',
        var_name='rate_mesozoo%Z_Pref')
    mesozoo_microzoo_grazing_limit = _Float(
        infile_key='Mesozoo, uZoo pred slope',
        var_name='rate_mesozoo%Z_PredSlope')
    mesozoo_microzoo_grazing_half_saturation = _Float(
        infile_key='Mesozoo, uZoo half-sat',
        var_name='rate_mesozoo%Z_HalfSat')


class _MesodiniumRubrum(colander.MappingSchema):
    mesorub_max_ingestion = _Float(
        infile_key='Mesorub, max ingestion',
        var_name='rate_mesorub%R')
    mesorub_assimilation_efficiency = _Float(
        infile_key='Mesorub, assimilation eff',
        var_name='rate_mesorub%eff')
    mesorub_grazing_limit = _Float(
        infile_key='Mesorub, nano predslope',
        var_name='rate_mesorub%PicoPredSlope')
    mesorub_grazing_half_saturation = _Float(
        infile_key='Mesorub, nano half-sat',
        var_name='rate_mesorub%PicoHalfSat')


class _Microzooplankton(colander.MappingSchema):
    microzoo_max_ingestion = _Float(
        infile_key='Microzoo, max ingestion',
        var_name='rate_uzoo%R')
    microzoo_assimilation_efficiency = _Float(
        infile_key='Microzoo, assimil. eff',
        var_name='rate_uzoo%eff')
    microzoo_natural_mortality = _Float(
        infile_key='Microzoo, nat mort',
        var_name='rate_uzoo%Rm')
    microzoo_excretion = _Float(
        infile_key='Microzoo, excretion',
        var_name='rate_uzoo%excr')
    microzoo_grazing_limit = _Float(
        infile_key='Microzoo, pred slope',
        var_name='rate_uzoo%PredSlope')
    microzoo_grazing_half_saturation = _Float(
        infile_key='Microzoo, half-sat',
        var_name='Microzoo, half-sat')
    microzoo_pico_preference = _Float(
        infile_key='Microzoo, pref for Pico',
        var_name='rate_uzoo%PicoPref')
    microzoo_pico_grazing_limit = _Float(
        infile_key='uzoo, Pico pred slope',
        var_name='rate_uzoo%PicoPredSlope')
    microzoo_pico_grazing_half_saturation = _Float(
        infile_key='uzoo, Pico half-sat',
        var_name='rate_uzoo%PicoHalfSat')
    microzoo_micro_preference = _Float(
        infile_key='Microzoo, pref for Micro',
        var_name='rate_uzoo%MicroPref')
    microzoo_micro_grazing_limit = _Float(
        infile_key='uzoo, Micro pred slope',
        var_name='rate_uzoo%MicroPredSlope')
    microzoo_micro_grazing_half_saturation = _Float(
        infile_key='Microzoo, Micro half-sat',
        var_name='rate_uzoo%MicroHalfSat')
    microzoo_nano_preference = _Float(
        infile_key='Microzoo, pref for nano',
        var_name='rate_uzoo%NanoPref')
    microzoo_nano_grazing_limit = _Float(
        infile_key='Microzoo, nano pred slope',
        var_name='rate_uzoo%NanoPredSlope')
    microzoo_nano_grazing_half_saturation = _Float(
        infile_key='Microzoo, nano half-sat',
        var_name='rate_uzoo%NanoHalfSat')
    microzoo_PON_preference = _Float(
        infile_key='Microzoo, pref for PON',
        var_name='rate_uzoo%PON_Pref')
    microzoo_PON_grazing_limit = _Float(
        infile_key='Microzoo, PON pred slope',
        var_name='rate_uzoo%PON_PredSlope')
    microzoo_PON_grazing_half_saturation = _Float(
        infile_key='Microzoo, PON half-sat',
        var_name='rate_uzoo%PON_HalfSat')
    microzoo_microzoo_preference = _Float(
        infile_key='Microzoo, pref for uZoo',
        var_name='rate_uzoo%PON_Pref')
    microzoo_microzoo_grazing_limit = _Float(
        infile_key='Microzoo, uZoo pred slope',
        var_name='rate_uzoo%PON_PredSlope')
    microzoo_microzoo_grazing_half_saturation = _Float(
        infile_key='Microzoo, uZoo half-sat',
        var_name='rate_uzoo%PON_HalfSat')


class _PhytoplanktonGrowth(colander.MappingSchema):
    micro_max_growth = _Float(
        infile_key='Micro, max growth',
        var_name='rate_micro%R')
    nano_max_growth = _Float(
        infile_key='Nano, max growth',
        var_name='rate_nano%R')
    pico_max_growth = _Float(
        infile_key='Pico, max growth',
        var_name='rate_pico%R')
    micro_optimal_light = _Float(
        infile_key='Micro, I_opt',
        var_name='rate_micro%Iopt')
    nano_optimal_light = _Float(
        infile_key='Nano, I_opt',
        var_name='rate_nano%Iopt')
    pico_optimal_light = _Float(
        infile_key='Pico, I_opt',
        var_name='rate_pico%Iopt')
    micro_max_temperature = _Float(
        infile_key='Micro, max temp',
        var_name='rate_micro%maxtemp')
    nano_max_temperature = _Float(
        infile_key='Nano, max temp',
        var_name='rate_nano%maxtemp')
    pico_max_temperature = _Float(
        infile_key='Pico, max temp',
        var_name='rate_pico%maxtemp')
    micro_temperature_range = _Float(
        infile_key='Micro, temp range',
        var_name='rate_micro%temprange')
    nano_temperature_range = _Float(
        infile_key='Nano, temp range',
        var_name='rate_nano%temprange')
    pico_temperature_range = _Float(
        infile_key='Pico, temp range',
        var_name='rate_pico%temprange')
    micro_Q10_exponent = _Float(
        infile_key='Micro, Q10 exp',
        var_name='rate_micro%Q10exp')
    nano_Q10_exponent = _Float(
        infile_key='Nano, Q10 exp',
        var_name='rate_nano%Q10exp')
    pico_Q10_exponent = _Float(
        infile_key='Pico, Q10 exp',
        var_name='rate_pico%Q10exp')
    micro_gamma_loss = _Float(
        infile_key='Micro, gamma loss',
        var_name='rate_micro%gamma')
    nano_gamma_loss = _Float(
        infile_key='Nano, gamma loss',
        var_name='rate_nano%gamma')
    pico_gamma_loss = _Float(
        infile_key='Pico, gamma loss',
        var_name='rate_pico%gamma')
    micro_NO3_half_saturation = _Float(
        infile_key='Micro, NO3 k',
        var_name='rate_micro%k')
    nano_NO3_half_saturation = _Float(
        infile_key='Nano, NO3 k',
        var_name='rate_nano%k')
    pico_NO3_half_saturation = _Float(
        infile_key='Pico, NO3 k',
        var_name='rate_pico%k')
    micro_NO3_vs_NH_preference = _Float(
        infile_key='Micro, kapa',
        var_name='rate_micro%kapa')
    nano_NO3_vs_NH_preference = _Float(
        infile_key='Nano, kapa',
        var_name='rate_nano%kapa')
    pico_NO3_vs_NH_preference = _Float(
        infile_key='Pico, kapa',
        var_name='rate_pico%kapa')
    micro_NH_inhibition_exponent = _Float(
        infile_key='Micro, NH inhib',
        var_name='Micro, NH inhib')
    nano_NH_inhibition_exponent = _Float(
        infile_key='Nano, NH inhib',
        var_name='Nano, NH inhib')
    pico_NH_inhibition_exponent = _Float(
        infile_key='Pico, NH inhib',
        var_name='Pico, NH inhib')
    micro_half_saturation = _Float(
        infile_key='Micro, N_o',
        var_name='rate_micro%N_o')
    nano_half_saturation = _Float(
        infile_key='Nano, N_o',
        var_name='rate_nano%N_o')
    pico_half_saturation = _Float(
        infile_key='Pico, N_o',
        var_name='rate_pico%N_o')
    micro_N_inhibition_exponent = _Float(
        infile_key='Micro, N_x',
        var_name='rate_micro%N_x')
    nano_N_inhibition_exponent = _Float(
        infile_key='Nano, N_x',
        var_name='rate_nano%N_x')
    pico_N_inhibition_exponent = _Float(
        infile_key='Pico, N_x',
        var_name='rate_pico%N_x')
    micro_Si_N_ratio = _Float(
        infile_key='Micro, Si_ratio',
        var_name='rate_micro%Si_ratio')
    nano_Si_N_ratio = _Float(
        infile_key='Nano, Si_ratio',
        var_name='rate_nano%Si_ratio')
    pico_Si_N_ratio = _Float(
        infile_key='Pico, Si_ratio',
        var_name='rate_pico%Si_ratio')
    micro_Si_half_saturation = _Float(
        infile_key='Micro, K_Si',
        var_name='rate_micro%K_Si')
    nano_Si_half_saturation = _Float(
        infile_key='Nano, K_Si',
        var_name='rate_nano%K_Si')
    pico_Si_half_saturation = _Float(
        infile_key='Pico, K_Si',
        var_name='rate_pico%K_Si')
    micro_natural_mortality = _Float(
        infile_key='Micro, Rm',
        var_name='rate_micro%Rm')
    nano_natural_mortality = _Float(
        infile_key='Nano, Rm',
        var_name='rate_nano%Rm')
    pico_natural_mortality = _Float(
        infile_key='Pico, Rm',
        var_name='rate_pico%Rm')


class _RemineralizationRates(colander.MappingSchema):
    NH_remin_rate = _Float(
        infile_key='NH remin rate', var_name='remin%NH')
    DON_remin_rate = _Float(
        infile_key='DON remin rate', var_name='remin%D_DON')
    PON_remin_rate = _Float(
        infile_key='PON remin rate', var_name='remin%D_PON')
    bSi_remin_rate = _Float(
        infile_key='bSi remin rate', var_name='remin%D_bSi')


class _PhytoplanktonMortalityWaste(colander.MappingSchema):
    micro_mort_NH = _Float(
        infile_key='Waste, dnm, NH', var_name='frac_waste_DNM%NH')
    micro_mort_DON = _Float(
        infile_key='Waste, dnm, DON', var_name='frac_waste_DNM%DON')
    micro_mort_PON = _Float(
        infile_key='Waste, dnm, PON', var_name='frac_waste_DNM%PON')
    micro_mort_ref = _Float(
        infile_key='Waste, dnm, Ref', var_name='frac_waste_DNM%Ref')
    micro_mort_bSi = _Float(
        infile_key='Waste, dnm, Bsi', var_name='frac_waste_DNM%Bsi')
    nano_mort_NH = _Float(
        infile_key='Waste, nnm, NH', var_name='frac_waste_NNM%NH')
    nano_mort_DON = _Float(
        infile_key='Waste, nnm, DON', var_name='frac_waste_NNM%DON')
    nano_mort_PON = _Float(
        infile_key='Waste, nnm, PON', var_name='frac_waste_NNM%PON')
    nano_mort_ref = _Float(
        infile_key='Waste, nnm, Ref', var_name='frac_waste_NNM%Ref')
    nano_mort_bSi = _Float(
        infile_key='Waste, nnm, Bsi', var_name='frac_waste_NNM%Bsi')
    pico_mort_NH = _Float(
        infile_key='Waste, fnm, NH', var_name='frac_waste_FNM%NH')
    pico_mort_DON = _Float(
        infile_key='Waste, fnm, DON', var_name='frac_waste_FNM%DON')
    pico_mort_PON = _Float(
        infile_key='Waste, fnm, PON', var_name='frac_waste_FNM%PON')
    pico_mort_ref = _Float(
        infile_key='Waste, fnm, Ref', var_name='frac_waste_FNM%Ref')
    pico_mort_bSi = _Float(
        infile_key='Waste, fnm, Bsi', var_name='frac_waste_FNM%Bsi')


class _MicrozooplanktonWaste(colander.MappingSchema):
    microzoo_mort_NH = _Float(
        infile_key='Waste, znm, NH', var_name='frac_waste_ZNM%NH')
    microzoo_mort_DON = _Float(
        infile_key='Waste, znm, DON', var_name='frac_waste_ZNM%DON')
    microzoo_mort_PON = _Float(
        infile_key='Waste, znm, PON', var_name='frac_waste_ZNM%PON')
    microzoo_mort_ref = _Float(
        infile_key='Waste, znm, Ref', var_name='frac_waste_ZNM%Ref')
    microzoo_mort_bSi = _Float(
        infile_key='Waste, znm, Bsi', var_name='frac_waste_ZNM%Bsi')
    microzoo_excrete_NH = _Float(
        infile_key='Waste, zex, NH', var_name='frac_waste_ZEX%NH')
    microzoo_excrete_DON = _Float(
        infile_key='Waste, zex, DON', var_name='frac_waste_ZEX%DON')
    microzoo_excrete_PON = _Float(
        infile_key='Waste, zex, PON', var_name='frac_waste_ZEX%PON')
    microzoo_excrete_ref = _Float(
        infile_key='Waste, zex, Ref', var_name='frac_waste_ZEX%Ref')
    microzoo_excrete_bSi = _Float(
        infile_key='Waste, zex, Bsi', var_name='frac_waste_ZEX%Bsi')


class _SloppyEating(colander.MappingSchema):
    mesozoo_microphyto_grazing_NH = _Float(
        infile_key='Waste, dem, NH', var_name='frac_waste_DEM%NH')
    mesozoo_microphyto_grazing_DON = _Float(
        infile_key='Waste, dem, DON', var_name='frac_waste_DEM%DON')
    mesozoo_microphyto_grazing_PON = _Float(
        infile_key='Waste, dem, PON', var_name='frac_waste_DEM%PON')
    mesozoo_microphyto_grazing_ref = _Float(
        infile_key='Waste, dem, Ref', var_name='frac_waste_DEM%Ref')
    mesozoo_microphyto_grazing_bSi = _Float(
        infile_key='Waste, dem, Bsi', var_name='frac_waste_DEM%Bsi')
    mesozoo_nanophyto_grazing_NH = _Float(
        infile_key='Waste, nem, NH', var_name='frac_waste_NEM%NH')
    mesozoo_nanophyto_grazing_DON = _Float(
        infile_key='Waste, nem, DON', var_name='frac_waste_NEM%DON')
    mesozoo_nanophyto_grazing_PON = _Float(
        infile_key='Waste, nem, PON', var_name='frac_waste_NEM%PON')
    mesozoo_nanophyto_grazing_ref = _Float(
        infile_key='Waste, nem, Ref', var_name='frac_waste_NEM%Ref')
    mesozoo_nanophyto_grazing_bSi = _Float(
        infile_key='Waste, nem, Bsi', var_name='frac_waste_NEM%Bsi')
    mesozoo_PON_grazing_NH = _Float(
        infile_key='Waste, pem, NH', var_name='frac_waste_PEM%NH')
    mesozoo_PON_grazing_DON = _Float(
        infile_key='Waste, pem, DON', var_name='frac_waste_PEM%DON')
    mesozoo_PON_grazing_PON = _Float(
        infile_key='Waste, pem, PON', var_name='frac_waste_PEM%PON')
    mesozoo_PON_grazing_ref = _Float(
        infile_key='Waste, pem, Ref', var_name='frac_waste_PEM%Ref')
    mesozoo_PON_grazing_bSi = _Float(
        infile_key='Waste, pem, Bsi', var_name='frac_waste_PEM%Bsi')
    mesozoo_microzoo_grazing_NH = _Float(
        infile_key='Waste, zem, NH', var_name='frac_waste_ZEM%NH')
    mesozoo_microzoo_grazing_DON = _Float(
        infile_key='Waste, zem, DON', var_name='frac_waste_ZEM%DON')
    mesozoo_microzoo_grazing_PON = _Float(
        infile_key='Waste, zem, PON', var_name='frac_waste_ZEM%PON')
    mesozoo_microzoo_grazing_ref = _Float(
        infile_key='Waste, zem, Ref', var_name='frac_waste_ZEM%Ref')
    mesozoo_microzoo_grazing_bSi = _Float(
        infile_key='Waste, zem, Bsi', var_name='frac_waste_ZEM%Bsi')
    microzoo_microphyto_grazing_NH = _Float(
        infile_key='Waste, dez, NH', var_name='frac_waste_DEZ%NH')
    microzoo_microphyto_grazing_DON = _Float(
        infile_key='Waste, dez, DON', var_name='frac_waste_DEZ%DON')
    microzoo_microphyto_grazing_PON = _Float(
        infile_key='Waste, dez, PON', var_name='frac_waste_DEZ%PON')
    microzoo_microphyto_grazing_ref = _Float(
        infile_key='Waste, dez, Ref', var_name='frac_waste_DEZ%Ref')
    microzoo_microphyto_grazing_bSi = _Float(
        infile_key='Waste, dez, Bsi', var_name='frac_waste_DEZ%Bsi')
    microzoo_nanophyto_grazing_NH = _Float(
        infile_key='Waste, nez, NH', var_name='frac_waste_NEZ%NH')
    microzoo_nanophyto_grazing_DON = _Float(
        infile_key='Waste, nez, DON', var_name='frac_waste_NEZ%DON')
    microzoo_nanophyto_grazing_PON = _Float(
        infile_key='Waste, nez, PON', var_name='frac_waste_NEZ%PON')
    microzoo_nanophyto_grazing_ref = _Float(
        infile_key='Waste, nez, Ref', var_name='frac_waste_NEZ%Ref')
    microzoo_nanophyto_grazing_bSi = _Float(
        infile_key='Waste, nez, Bsi', var_name='frac_waste_NEZ%Bsi')
    microzoo_picophyto_grazing_NH = _Float(
        infile_key='Waste, fez, NH', var_name='frac_waste_FEZ%NH')
    microzoo_picophyto_grazing_DON = _Float(
        infile_key='Waste, fez, DON', var_name='frac_waste_FEZ%DON')
    microzoo_picophyto_grazing_PON = _Float(
        infile_key='Waste, fez, PON', var_name='frac_waste_FEZ%PON')
    microzoo_picophyto_grazing_ref = _Float(
        infile_key='Waste, fez, Ref', var_name='frac_waste_FEZ%Ref')
    microzoo_picophyto_grazing_bSi = _Float(
        infile_key='Waste, fez, Bsi', var_name='frac_waste_FEZ%Bsi')
    microzoo_PON_grazing_NH = _Float(
        infile_key='Waste, pez, NH', var_name='frac_waste_PEZ%NH')
    microzoo_PON_grazing_DON = _Float(
        infile_key='Waste, pez, DON', var_name='frac_waste_PEZ%DON')
    microzoo_PON_grazing_PON = _Float(
        infile_key='Waste, pez, PON', var_name='frac_waste_PEZ%PON')
    microzoo_PON_grazing_ref = _Float(
        infile_key='Waste, pez, Ref', var_name='frac_waste_PEZ%Ref')
    microzoo_PON_grazing_bSi = _Float(
        infile_key='Waste, pez, Bsi', var_name='frac_waste_PEZ%Bsi')
    microzoo_microzoo_grazing_NH = _Float(
        infile_key='Waste, zez, NH', var_name='frac_waste_ZEZ%NH')
    microzoo_microzoo_grazing_DON = _Float(
        infile_key='Waste, zez, DON', var_name='frac_waste_ZEZ%DON')
    microzoo_microzoo_grazing_PON = _Float(
        infile_key='Waste, zez, PON', var_name='frac_waste_ZEZ%PON')
    microzoo_microzoo_grazing_ref = _Float(
        infile_key='Waste, zez, Ref', var_name='frac_waste_ZEZ%Ref')
    microzoo_microzoo_grazing_bSi = _Float(
        infile_key='Waste, zez, Bsi', var_name='frac_waste_ZEZ%Bsi')
    mesorub_picophyto_grazing_NH = _Float(
        infile_key='Waste, fen, NH', var_name='frac_waste_FEN%NH')
    mesorub_picophyto_grazing_DON = _Float(
        infile_key='Waste, fen, DON', var_name='frac_waste_FEN%DON')
    mesorub_picophyto_grazing_PON = _Float(
        infile_key='Waste, fen, PON', var_name='frac_waste_FEN%PON')
    mesorub_picophyto_grazing_ref = _Float(
        infile_key='Waste, fen, Ref', var_name='frac_waste_FEN%Ref')
    mesorub_picophyto_grazing_bSi = _Float(
        infile_key='Waste, fen, Bsi', var_name='frac_waste_FEN%Bsi')


class _BiologyParams(colander.MappingSchema):
    include_flagellates = _Boolean(
        infile_key='flagellates_on', var_name='flagellates')
    include_remineralization = _Boolean(
        infile_key='remineralization', var_name='remineralization')
    include_microzooplankton = _Boolean(
        infile_key='use microzooplankton', var_name='microzooplankton')
    single_species_light = _Boolean(
        infile_key='single species light', var_name='strong_limitation')
    mesozooplankton = _Mesozooplankton()
    mesodinium_rubrum = _MesodiniumRubrum()
    microzooplankton = _Microzooplankton()
    phytoplankton_growth = _PhytoplanktonGrowth()
    remineralization_rates = _RemineralizationRates()
    phytoplankton_mortality_waste = _PhytoplanktonMortalityWaste()
    microzooplankton_waste = _MicrozooplanktonWaste()
    sloppy_eating = _SloppyEating()


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
    biology = _BiologyParams()


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
