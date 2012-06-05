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
    micro_max_growth = _SOG_RealDP(name='Micro, max growth')
    nano_max_growth = _SOG_RealDP(name='Nano, max growth')
    pico_max_growth = _SOG_RealDP(name='Pico, max growth')
    micro_optimal_light = _SOG_RealDP(name='Micro, I_opt')
    nano_optimal_light = _SOG_RealDP(name='Nano, I_opt')
    pico_optimal_light = _SOG_RealDP(name='Pico, I_opt')
    micro_max_temperature = _SOG_RealDP(name='Micro, max temp')
    nano_max_temperature = _SOG_RealDP(name='Nano, max temp')
    pico_max_temperature = _SOG_RealDP(name='Pico, max temp')
    micro_temperature_range = _SOG_RealDP(name='Micro, temp range')
    nano_temperature_range = _SOG_RealDP(name='Nano, temp range')
    pico_temperature_range = _SOG_RealDP(name='Pico, temp range')
    micro_Q10_exponent = _SOG_RealDP(name='Micro, Q10 exp')
    nano_Q10_exponent = _SOG_RealDP(name='Nano, Q10 exp')
    pico_Q10_exponent = _SOG_RealDP(name='Pico, Q10 exp')
    micro_gamma_loss = _SOG_RealDP(name='Micro, gamma loss')
    nano_gamma_loss = _SOG_RealDP(name='Nano, gamma loss')
    pico_gamma_loss = _SOG_RealDP(name='Pico, gamma loss')
    micro_NO3_half_saturation = _SOG_RealDP(name='Micro, NO3 k')
    nano_NO3_half_saturation = _SOG_RealDP(name='Nano, NO3 k')
    pico_NO3_half_saturation = _SOG_RealDP(name='Pico, NO3 k')
    micro_NO3_vs_NH_preference = _SOG_RealDP(name='Micro, kapa')
    nano_NO3_vs_NH_preference = _SOG_RealDP(name='Nano, kapa')
    pico_NO3_vs_NH_preference = _SOG_RealDP(name='Pico, kapa')
    micro_NH_inhibition_exponent = _SOG_RealDP(name='Micro, NH inhib')
    nano_NH_inhibition_exponent = _SOG_RealDP(name='Nano, NH inhib')
    pico_NH_inhibition_exponent = _SOG_RealDP(name='Pico, NH inhib')
    micro_half_saturation = _SOG_RealDP(name='Micro, N_o')
    nano_half_saturation = _SOG_RealDP(name='Nano, N_o')
    pico_half_saturation = _SOG_RealDP(name='Pico, N_o')
    micro_N_inhibition_exponent = _SOG_RealDP(name='Micro, N_x')
    nano_N_inhibition_exponent = _SOG_RealDP(name='Nano, N_x')
    pico_N_inhibition_exponent = _SOG_RealDP(name='Pico, N_x')
    micro_Si_N_ratio = _SOG_RealDP(name='Micro, Si ratio')
    nano_Si_N_ratio = _SOG_RealDP(name='Nano, Si ratio')
    pico_Si_N_ratio = _SOG_RealDP(name='Pico, Si ratio')
    micro_Si_half_saturation = _SOG_RealDP(name='Micro, K Si')
    nano_Si_half_saturation = _SOG_RealDP(name='Nano, K Si')
    pico_Si_half_saturation = _SOG_RealDP(name='Pico, K Si')
    micro_natural_mortality = _SOG_RealDP(name='Micro, nat mort')
    nano_natural_mortality = _SOG_RealDP(name='Nano, nat mort')
    pico_natural_mortality = _SOG_RealDP(name='Pico, nat mort')
    NH_remin_rate = _SOG_RealDP(name='NH remin rate')
    DON_remin_rate = _SOG_RealDP(name='DON remin rate')
    PON_remin_rate = _SOG_RealDP(name='PON remin rate')
    bSi_remin_rate = _SOG_RealDP(name='bSi remin rate')
    micro_mort_NH = _SOG_RealDP(name='Waste, dnm, NH')
    micro_mort_DON = _SOG_RealDP(name='Waste, dnm, DON')
    micro_mort_PON = _SOG_RealDP(name='Waste, dnm, PON')
    micro_mort_refr = _SOG_RealDP(name='Waste, dnm, Ref')
    micro_mort_bSi = _SOG_RealDP(name='Waste, dnm, Bsi')
    nano_mort_NH = _SOG_RealDP(name='Waste, nnm, NH')
    nano_mort_DON = _SOG_RealDP(name='Waste, nnm, DON')
    nano_mort_PON = _SOG_RealDP(name='Waste, nnm, PON')
    nano_mort_refr = _SOG_RealDP(name='Waste, nnm, Ref')
    nano_mort_bSi = _SOG_RealDP(name='Waste, nnm, Bsi')
    pico_mort_NH = _SOG_RealDP(name='Waste, fnm, NH')
    pico_mort_DON = _SOG_RealDP(name='Waste, fnm, DON')
    pico_mort_PON = _SOG_RealDP(name='Waste, fnm, PON')
    pico_mort_refr = _SOG_RealDP(name='Waste, fnm, Ref')
    pico_mort_bSi = _SOG_RealDP(name='Waste, fnm, Bsi')
    microzoo_mort_NH = _SOG_RealDP(name='Waste, znm, NH')
    microzoo_mort_DON = _SOG_RealDP(name='Waste, znm, DON')
    microzoo_mort_PON = _SOG_RealDP(name='Waste, znm, PON')
    microzoo_mort_refr = _SOG_RealDP(name='Waste, znm, Ref')
    microzoo_mort_bSi = _SOG_RealDP(name='Waste, znm, Bsi')
    microzoo_excrete_NH = _SOG_RealDP(name='Waste, zex, NH')
    microzoo_excrete_DON = _SOG_RealDP(name='Waste, zex, DON')
    microzoo_excrete_PON = _SOG_RealDP(name='Waste, zex, PON')
    microzoo_excrete_refr = _SOG_RealDP(name='Waste, zex, Ref')
    microzoo_excrete_bSi = _SOG_RealDP(name='Waste, zex, Bsi')
    mesozoo_microphyto_grazing_NH = _SOG_RealDP(name='Waste, dem, NH')
    mesozoo_microphyto_grazing_DON = _SOG_RealDP(name='Waste, dem, DON')
    mesozoo_microphyto_grazing_PON = _SOG_RealDP(name='Waste, dem, PON')
    mesozoo_microphyto_grazing_refr = _SOG_RealDP(name='Waste, dem, Ref')
    mesozoo_microphyto_grazing_bSi = _SOG_RealDP(name='Waste, dem, Bsi')
    mesozoo_nanophyto_grazing_NH = _SOG_RealDP(name='Waste, nem, NH')
    mesozoo_nanophyto_grazing_DON = _SOG_RealDP(name='Waste, nem, DON')
    mesozoo_nanophyto_grazing_PON = _SOG_RealDP(name='Waste, nem, PON')
    mesozoo_nanophyto_grazing_refr = _SOG_RealDP(name='Waste, nem, Ref')
    mesozoo_nanophyto_grazing_bSi = _SOG_RealDP(name='Waste, nem, Bsi')
    mesozoo_PON_grazing_NH = _SOG_RealDP(name='Waste, pem, NH')
    mesozoo_PON_grazing_DON = _SOG_RealDP(name='Waste, pem, DON')
    mesozoo_PON_grazing_PON = _SOG_RealDP(name='Waste, pem, PON')
    mesozoo_PON_grazing_refr = _SOG_RealDP(name='Waste, pem, Ref')
    mesozoo_PON_grazing_bSi = _SOG_RealDP(name='Waste, pem, Bsi')
    mesozoo_microzoo_grazing_NH = _SOG_RealDP(name='Waste, zem, NH')
    mesozoo_microzoo_grazing_DON = _SOG_RealDP(name='Waste, zem, DON')
    mesozoo_microzoo_grazing_PON = _SOG_RealDP(name='Waste, zem, PON')
    mesozoo_microzoo_grazing_refr = _SOG_RealDP(name='Waste, zem, Ref')
    mesozoo_microzoo_grazing_bSi = _SOG_RealDP(name='Waste, zem, Bsi')
    microzoo_microphyto_grazing_NH = _SOG_RealDP(name='Waste, dez, NH')
    microzoo_microphyto_grazing_DON = _SOG_RealDP(name='Waste, dez, DON')
    microzoo_microphyto_grazing_PON = _SOG_RealDP(name='Waste, dez, PON')
    microzoo_microphyto_grazing_refr = _SOG_RealDP(name='Waste, dez, Ref')
    microzoo_microphyto_grazing_bSi = _SOG_RealDP(name='Waste, dez, Bsi')
    microzoo_nanophyto_grazing_NH = _SOG_RealDP(name='Waste, nez, NH')
    microzoo_nanophyto_grazing_DON = _SOG_RealDP(name='Waste, nez, DON')
    microzoo_nanophyto_grazing_PON = _SOG_RealDP(name='Waste, nez, PON')
    microzoo_nanophyto_grazing_refr = _SOG_RealDP(name='Waste, nez, Ref')
    microzoo_nanophyto_grazing_bSi = _SOG_RealDP(name='Waste, nez, Bsi')
    microzoo_picophyto_grazing_NH = _SOG_RealDP(name='Waste, fez, NH')
    microzoo_picophyto_grazing_DON = _SOG_RealDP(name='Waste, fez, DON')
    microzoo_picophyto_grazing_PON = _SOG_RealDP(name='Waste, fez, PON')
    microzoo_picophyto_grazing_refr = _SOG_RealDP(name='Waste, fez, Ref')
    microzoo_picophyto_grazing_bSi = _SOG_RealDP(name='Waste, fez, Bsi')
    microzoo_PON_grazing_NH = _SOG_RealDP(name='Waste, pez, NH')
    microzoo_PON_grazing_DON = _SOG_RealDP(name='Waste, pez, DON')
    microzoo_PON_grazing_PON = _SOG_RealDP(name='Waste, pez, PON')
    microzoo_PON_grazing_refr = _SOG_RealDP(name='Waste, pez, Ref')
    microzoo_PON_grazing_bSi = _SOG_RealDP(name='Waste, pez, Bsi')
    microzoo_microzoo_grazing_NH = _SOG_RealDP(name='Waste, zez, NH')
    microzoo_microzoo_grazing_DON = _SOG_RealDP(name='Waste, zez, DON')
    microzoo_microzoo_grazing_PON = _SOG_RealDP(name='Waste, zez, PON')
    microzoo_microzoo_grazing_refr = _SOG_RealDP(name='Waste, zez, Ref')
    microzoo_microzoo_grazing_bSi = _SOG_RealDP(name='Waste, zez, Bsi')
    mesorub_picophyto_grazing_NH = _SOG_RealDP(name='Waste, fen, NH')
    mesorub_picophyto_grazing_DON = _SOG_RealDP(name='Waste, fen, DON')
    mesorub_picophyto_grazing_PON = _SOG_RealDP(name='Waste, fen, PON')
    mesorub_picophyto_grazing_refr = _SOG_RealDP(name='Waste, fen, Ref')
    mesorub_picophyto_grazing_bSi = _SOG_RealDP(name='Waste, fen, Bsi')
    microphyto_min_sink_rate = _SOG_RealDP(name='Micro min sink rate')
    microphyto_max_sink_rate = _SOG_RealDP(name='Micro max sink rate')
    PON_sink_rate = _SOG_RealDP(name='PON sink rate')
    refr_sink_rate = _SOG_RealDP(name='refr sink rate')
    bSi_sink_rate = _SOG_RealDP(name='bSi sink rate')
    use_average_forcing_data = _SOG_String(name='use average/hist forcing')
    wind_forcing_file = _SOG_String(name='wind')
    air_temperature_forcing_file = _SOG_String(name='air temp')
    cloud_fraction_forcing_file = _SOG_String(name='cloud')
    humidity_forcing_file = _SOG_String(name='humidity')
    major_river_forcing_file = _SOG_String(name='major river')
    use_river_temperature = _SOG_Boolean(name='use river temp')
    minor_river_forcing_file = _SOG_String(name='minor river')
    minor_river_integration_days = _SOG_Int(name='minor river integ days')
    alt_minor_river_forcing_file = _SOG_String(name='alt minor river')

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
    'Micro, max growth', 'Nano, max growth', 'Pico, max growth',
    'Micro, I_opt', 'Nano, I_opt', 'Pico, I_opt',
    'Micro, max temp', 'Nano, max temp', 'Pico, max temp',
    'Micro, temp range', 'Nano, temp range', 'Pico, temp range',
    'Micro, Q10 exp', 'Nano, Q10 exp', 'Pico, Q10 exp',
    'Micro, gamma loss', 'Nano, gamma loss', 'Pico, gamma loss',
    'Micro, NO3 k', 'Nano, NO3 k', 'Pico, NO3 k',
    'Micro, kapa', 'Nano, kapa', 'Pico, kapa',
    'Micro, NH inhib', 'Nano, NH inhib', 'Pico, NH inhib',
    'Micro, N_o', 'Nano, N_o', 'Pico, N_o',
    'Micro, N_x', 'Nano, N_x', 'Pico, N_x',
    'Micro, Si ratio', 'Nano, Si ratio', 'Pico, Si ratio',
    'Micro, K Si', 'Nano, K Si', 'Pico, K Si',
    'Micro, nat mort', 'Nano, nat mort', 'Pico, nat mort',
    'NH remin rate', 'DON remin rate', 'PON remin rate', 'bSi remin rate',
    'Waste, dnm, NH', 'Waste, dnm, DON', 'Waste, dnm, PON', 'Waste, dnm, Ref',
    'Waste, dnm, Bsi',
    'Waste, nnm, NH', 'Waste, nnm, DON', 'Waste, nnm, PON', 'Waste, nnm, Ref',
    'Waste, nnm, Bsi',
    'Waste, fnm, NH', 'Waste, fnm, DON', 'Waste, fnm, PON', 'Waste, fnm, Ref',
    'Waste, fnm, Bsi',
    'Waste, znm, NH', 'Waste, znm, DON', 'Waste, znm, PON', 'Waste, znm, Ref',
    'Waste, znm, Bsi',
    'Waste, zex, NH', 'Waste, zex, DON', 'Waste, zex, PON', 'Waste, zex, Ref',
    'Waste, zex, Bsi',
    'Waste, dem, NH', 'Waste, dem, DON', 'Waste, dem, PON', 'Waste, dem, Ref',
    'Waste, dem, Bsi',
    'Waste, nem, NH', 'Waste, nem, DON', 'Waste, nem, PON', 'Waste, nem, Ref',
    'Waste, nem, Bsi',
    'Waste, pem, NH', 'Waste, pem, DON', 'Waste, pem, PON', 'Waste, pem, Ref',
    'Waste, pem, Bsi',
    'Waste, zem, NH', 'Waste, zem, DON', 'Waste, zem, PON', 'Waste, zem, Ref',
    'Waste, zem, Bsi',
    'Waste, dez, NH', 'Waste, dez, DON', 'Waste, dez, PON', 'Waste, dez, Ref',
    'Waste, dez, Bsi',
    'Waste, nez, NH', 'Waste, nez, DON', 'Waste, nez, PON', 'Waste, nez, Ref',
    'Waste, nez, Bsi',
    'Waste, fez, NH', 'Waste, fez, DON', 'Waste, fez, PON', 'Waste, fez, Ref',
    'Waste, fez, Bsi',
    'Waste, pez, NH', 'Waste, pez, DON', 'Waste, pez, PON', 'Waste, pez, Ref',
    'Waste, pez, Bsi',
    'Waste, zez, NH', 'Waste, zez, DON', 'Waste, zez, PON', 'Waste, zez, Ref',
    'Waste, zez, Bsi',
    'Waste, fen, NH', 'Waste, fen, DON', 'Waste, fen, PON', 'Waste, fen, Ref',
    'Waste, fen, Bsi',
    'Micro min sink rate', 'Micro max sink rate', 'PON sink rate',
    'refr sink rate',  'bSi sink rate',
    'use average/hist forcing',
    'wind', 'air temp', 'cloud', 'humidity',
    'major river', 'use river temp',
    'minor river', 'minor river integ days', 'alt minor river',
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
