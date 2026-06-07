def _cable_operating_metadata(insulation_type, laying_methods, short_circuit_1s):
    is_pvc = insulation_type == "PVC"
    normal_temp = 70 if is_pvc else 90
    emergency_temp = 90 if is_pvc else 105
    short_temp = 160 if is_pvc else 250
    return {
        "ampacity_reference": {
            "ambient_air_c": 40,
            "soil_temperature_c": 25,
            "soil_thermal_resistivity_k_m_per_w": 1.2,
            "burial_depth_m": 0.7,
            "laying_spacing_m": 0.1,
            "laying_methods": laying_methods,
            "source_type": "standard_reference_and_engineering_default",
        },
        "derating_factors": {
            "temperature": "apply by ambient and conductor temperature",
            "grouping": "apply by number of circuits and spacing",
            "soil": "apply by soil thermal resistivity",
            "depth": "apply by burial depth",
            "harmonic": "apply when neutral or sheath harmonic heating is material",
        },
        "thermal_limits": {
            "max_conductor_temp_normal_c": normal_temp,
            "max_conductor_temp_emergency_c": emergency_temp,
            "max_conductor_temp_short_circuit_c": short_temp,
        },
        "short_circuit_rating": {
            "current_1s_ka": short_circuit_1s,
            "i2t_ka2s": round(short_circuit_1s ** 2, 3),
            "reference_duration_s": 1,
            "duration_range_s": [0.1, 5],
        },
        "lifecycle": {
            "design_life_years": 30,
            "emergency_overload_hours_per_year_limit": 100,
            "thermal_aging_model": "Arrhenius-style cable insulation aging; project-specific constants required",
            "source_type": "engineering_policy",
        },
    }


def _make_cable(conductor_material, cross_section_mm2, voltage_rating,
                insulation_type, armor_type, r, x, c,
                max_i_air, max_i_ground, max_i_duct,
                short_circuit_1s, outer_diameter, weight,
                voltage_rating_category, standard, source_note):
    alpha = 3.93e-3 if conductor_material == "Cu" else 4.03e-3
    metadata = _cable_operating_metadata(insulation_type, ["air", "ground", "duct"], short_circuit_1s)
    return {
        "conductor_material": conductor_material,
        "cross_section_mm2": cross_section_mm2,
        "voltage_rating": voltage_rating,
        "insulation_type": insulation_type,
        "armor_type": armor_type,
        "r_ohm_per_km": r,
        "x_ohm_per_km": x,
        "c_nf_per_km": c,
        "r0_ohm_per_km": round(3.5 * r, 4),
        "x0_ohm_per_km": round(1.8 * x, 4),
        "c0_nf_per_km": round(0.5 * c, 1),
        "max_i_ka_air": max_i_air,
        "max_i_ka_ground": max_i_ground,
        "max_i_ka_duct": max_i_duct,
        "max_i_ka": max_i_ground,
        "short_circuit_current_1s_ka": short_circuit_1s,
        "short_circuit_i2t_ka2s": metadata["short_circuit_rating"]["i2t_ka2s"],
        "max_conductor_temp_normal_c": metadata["thermal_limits"]["max_conductor_temp_normal_c"],
        "max_conductor_temp_emergency_c": metadata["thermal_limits"]["max_conductor_temp_emergency_c"],
        "max_conductor_temp_short_circuit_c": metadata["thermal_limits"]["max_conductor_temp_short_circuit_c"],
        "ampacity_reference": metadata["ampacity_reference"],
        "derating_factors": metadata["derating_factors"],
        "thermal_limits": metadata["thermal_limits"],
        "short_circuit_rating": metadata["short_circuit_rating"],
        "lifecycle": metadata["lifecycle"],
        "design_life_years": metadata["lifecycle"]["design_life_years"],
        "outer_diameter_mm": outer_diameter,
        "weight_kg_per_km": weight,
        "alpha": alpha,
        "type": "cs",
        "q_mm2": cross_section_mm2,
        "voltage_rating_category": voltage_rating_category,
        "standard": standard,
        "source_note": source_note,
    }


def _build_mv_10kv():
    _CU_R = {
        25: 0.727, 35: 0.524, 50: 0.387, 70: 0.268, 95: 0.193,
        120: 0.153, 150: 0.124, 185: 0.0991, 240: 0.0754,
        300: 0.0601, 400: 0.0470,
    }
    _AL_R = {
        25: 1.200, 35: 0.868, 50: 0.641, 70: 0.443, 95: 0.320,
        120: 0.253, 150: 0.206, 185: 0.164, 240: 0.125,
        300: 0.100, 400: 0.0778,
    }
    _X = {
        25: 0.126, 35: 0.120, 50: 0.115, 70: 0.110, 95: 0.107,
        120: 0.105, 150: 0.102, 185: 0.100, 240: 0.098,
        300: 0.096, 400: 0.094,
    }
    _C = {
        25: 150, 35: 165, 50: 180, 70: 200, 95: 215, 120: 230,
        150: 245, 185: 260, 240: 290, 300: 310, 400: 340,
    }
    _CU_YJV22_AIR = {
        25: 0.110, 35: 0.135, 50: 0.165, 70: 0.210, 95: 0.255,
        120: 0.295, 150: 0.335, 185: 0.385, 240: 0.455,
        300: 0.520, 400: 0.600,
    }
    _CU_YJV22_GND = {
        25: 0.100, 35: 0.120, 50: 0.145, 70: 0.185, 95: 0.225,
        120: 0.260, 150: 0.295, 185: 0.335, 240: 0.395,
        300: 0.450, 400: 0.520,
    }
    _CU_YJV22_DCT = {
        25: 0.085, 35: 0.105, 50: 0.130, 70: 0.165, 95: 0.200,
        120: 0.230, 150: 0.265, 185: 0.300, 240: 0.355,
        300: 0.405, 400: 0.470,
    }
    _CU_SC = {
        25: 3.3, 35: 4.6, 50: 6.6, 70: 9.2, 95: 12.5,
        120: 15.8, 150: 19.7, 185: 24.4, 240: 31.7,
        300: 39.6, 400: 52.8,
    }
    _YJV22_CU_OD = {
        25: 36, 35: 39, 50: 42, 70: 46, 95: 50, 120: 54,
        150: 58, 185: 62, 240: 68, 300: 74, 400: 82,
    }
    _YJV22_CU_WT = {
        25: 1850, 35: 2200, 50: 2600, 70: 3200, 95: 3900,
        120: 4250, 150: 4900, 185: 5700, 240: 7000,
        300: 8400, 400: 10500,
    }
    sections = [25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400]
    d = {}
    for s in sections:
        r_cu = _CU_R[s]
        r_al = _AL_R[s]
        xi = _X[s]
        ci = _C[s]
        air = _CU_YJV22_AIR[s]
        gnd = _CU_YJV22_GND[s]
        dct = _CU_YJV22_DCT[s]
        sc_cu = _CU_SC[s]
        od = _YJV22_CU_OD[s]
        wt = _YJV22_CU_WT[s]
        d[f"YJV22-3x{s}-10kV"] = _make_cable(
            "Cu", s, "6/10kV", "XLPE", "steel_tape",
            r_cu, xi, ci, air, gnd, dct,
            sc_cu, od, wt,
            "MV", "GB/T 12706.1~3-2020", "国标表值",
        )
        d[f"YJV-3x{s}-10kV"] = _make_cable(
            "Cu", s, "6/10kV", "XLPE", "none",
            r_cu, xi, ci,
            round(air * 1.05, 3), round(gnd * 1.05, 3), round(dct * 1.05, 3),
            sc_cu, od - 3, round(wt * 0.90),
            "MV", "GB/T 12706.1~3-2020", "国标表值",
        )
        d[f"YJLV22-3x{s}-10kV"] = _make_cable(
            "Al", s, "6/10kV", "XLPE", "steel_tape",
            r_al, xi, ci,
            round(air * 0.78, 3), round(gnd * 0.78, 3), round(dct * 0.78, 3),
            round(sc_cu * 0.61, 2), od - 1, round(wt * 0.75),
            "MV", "GB/T 12706.1~3-2020", "国标表值",
        )
        d[f"YJLV-3x{s}-10kV"] = _make_cable(
            "Al", s, "6/10kV", "XLPE", "none",
            r_al, xi, ci,
            round(air * 0.78 * 1.05, 3), round(gnd * 0.78 * 1.05, 3),
            round(dct * 0.78 * 1.05, 3),
            round(sc_cu * 0.61, 2), od - 4, round(wt * 0.90 * 0.75),
            "MV", "GB/T 12706.1~3-2020", "国标表值",
        )
    return d


def _build_mv_35kv():
    _CU_R = {
        50: 0.387, 70: 0.268, 95: 0.193, 120: 0.153,
        150: 0.124, 185: 0.0991, 240: 0.0754,
        300: 0.0601, 400: 0.0470,
    }
    _AL_R = {
        50: 0.641, 70: 0.443, 95: 0.320, 120: 0.253,
        150: 0.206, 185: 0.164, 240: 0.125,
        300: 0.100, 400: 0.0778,
    }
    _X = {
        50: 0.134, 70: 0.128, 95: 0.122, 120: 0.118,
        150: 0.115, 185: 0.112, 240: 0.108,
        300: 0.105, 400: 0.102,
    }
    _C = {
        50: 105, 70: 115, 95: 125, 120: 135,
        150: 145, 185: 155, 240: 170,
        300: 185, 400: 200,
    }
    _CU_YJV22_AIR_10KV = {
        50: 0.165, 70: 0.210, 95: 0.255, 120: 0.295,
        150: 0.335, 185: 0.385, 240: 0.455,
        300: 0.520, 400: 0.600,
    }
    _CU_YJV22_GND_10KV = {
        50: 0.145, 70: 0.185, 95: 0.225, 120: 0.260,
        150: 0.295, 185: 0.335, 240: 0.395,
        300: 0.450, 400: 0.520,
    }
    _CU_YJV22_DCT_10KV = {
        50: 0.130, 70: 0.165, 95: 0.200, 120: 0.230,
        150: 0.265, 185: 0.300, 240: 0.355,
        300: 0.405, 400: 0.470,
    }
    _CU_SC = {
        50: 6.6, 70: 9.2, 95: 12.5, 120: 15.8,
        150: 19.7, 185: 24.4, 240: 31.7,
        300: 39.6, 400: 52.8,
    }
    _YJV22_CU_OD_10KV = {
        50: 42, 70: 46, 95: 50, 120: 54,
        150: 58, 185: 62, 240: 68, 300: 74, 400: 82,
    }
    _YJV22_CU_WT_10KV = {
        50: 2600, 70: 3200, 95: 3900, 120: 4250,
        150: 4900, 185: 5700, 240: 7000,
        300: 8400, 400: 10500,
    }
    sections = [50, 70, 95, 120, 150, 185, 240, 300, 400]
    d = {}
    for s in sections:
        r_cu = _CU_R[s]
        r_al = _AL_R[s]
        xi = _X[s]
        ci = _C[s]
        sc_cu = _CU_SC[s]
        air = round(_CU_YJV22_AIR_10KV[s] * 0.80, 3)
        gnd = round(_CU_YJV22_GND_10KV[s] * 0.80, 3)
        dct = round(_CU_YJV22_DCT_10KV[s] * 0.80, 3)
        od = _YJV22_CU_OD_10KV[s] + 10
        wt = round(_YJV22_CU_WT_10KV[s] * 1.30)
        d[f"YJV22-3x{s}-35kV"] = _make_cable(
            "Cu", s, "21/35kV", "XLPE", "steel_tape",
            r_cu, xi, ci, air, gnd, dct,
            sc_cu, od, wt,
            "MV", "GB/T 12706.1~3-2020", "国标表值",
        )
        d[f"YJV-3x{s}-35kV"] = _make_cable(
            "Cu", s, "21/35kV", "XLPE", "none",
            r_cu, xi, ci,
            round(air * 1.05, 3), round(gnd * 1.05, 3), round(dct * 1.05, 3),
            sc_cu, od - 3, round(wt * 0.90),
            "MV", "GB/T 12706.1~3-2020", "国标表值",
        )
        d[f"YJLV22-3x{s}-35kV"] = _make_cable(
            "Al", s, "21/35kV", "XLPE", "steel_tape",
            r_al, xi, ci,
            round(air * 0.78, 3), round(gnd * 0.78, 3), round(dct * 0.78, 3),
            round(sc_cu * 0.61, 2), od - 1, round(wt * 0.75),
            "MV", "GB/T 12706.1~3-2020", "国标表值",
        )
        d[f"YJLV-3x{s}-35kV"] = _make_cable(
            "Al", s, "21/35kV", "XLPE", "none",
            r_al, xi, ci,
            round(air * 0.78 * 1.05, 3), round(gnd * 0.78 * 1.05, 3),
            round(dct * 0.78 * 1.05, 3),
            round(sc_cu * 0.61, 2), od - 4, round(wt * 0.90 * 0.75),
            "MV", "GB/T 12706.1~3-2020", "国标表值",
        )
    return d


def _build_lv_04kv():
    _CU_R = {
        16: 1.15, 25: 0.727, 35: 0.524, 50: 0.387, 70: 0.268,
        95: 0.193, 120: 0.153, 150: 0.124, 185: 0.0991,
        240: 0.0754, 300: 0.0601, 400: 0.0470,
    }
    _AL_R = {
        16: 1.91, 25: 1.200, 35: 0.868, 50: 0.641, 70: 0.443,
        95: 0.320, 120: 0.253, 150: 0.206, 185: 0.164,
        240: 0.125, 300: 0.100, 400: 0.0778,
    }
    _X = {
        16: 0.095, 25: 0.088, 35: 0.082, 50: 0.078, 70: 0.074,
        95: 0.070, 120: 0.068, 150: 0.066, 185: 0.064,
        240: 0.062, 300: 0.060, 400: 0.058,
    }
    _C = {
        16: 200, 25: 230, 35: 260, 50: 290, 70: 320, 95: 350,
        120: 380, 150: 410, 185: 440, 240: 490, 300: 540, 400: 600,
    }
    _CU_YJV22_AIR = {
        16: 0.080, 25: 0.105, 35: 0.130, 50: 0.160,
        70: 0.200, 95: 0.245, 120: 0.285, 150: 0.325,
        185: 0.375, 240: 0.445, 300: 0.510, 400: 0.590,
    }
    _CU_YJV22_GND = {
        16: 0.070, 25: 0.092, 35: 0.115, 50: 0.140,
        70: 0.175, 95: 0.215, 120: 0.250, 150: 0.285,
        185: 0.325, 240: 0.385, 300: 0.440, 400: 0.510,
    }
    _CU_YJV22_DCT = {
        16: 0.060, 25: 0.078, 35: 0.096, 50: 0.120,
        70: 0.150, 95: 0.185, 120: 0.215, 150: 0.245,
        185: 0.280, 240: 0.335, 300: 0.385, 400: 0.445,
    }
    _CU_SC_XLPE = {
        16: 2.1, 25: 3.3, 35: 4.6, 50: 6.6, 70: 9.2,
        95: 12.5, 120: 15.8, 150: 19.7, 185: 24.4,
        240: 31.7, 300: 39.6, 400: 52.8,
    }
    _YJV22_CU_OD = {
        16: 22, 25: 25, 35: 28, 50: 31, 70: 35, 95: 39,
        120: 42, 150: 46, 185: 50, 240: 55, 300: 60, 400: 66,
    }
    _YJV22_CU_WT = {
        16: 700, 25: 950, 35: 1200, 50: 1500, 70: 1900,
        95: 2400, 120: 2800, 150: 3300, 185: 3900,
        240: 4800, 300: 5700, 400: 7000,
    }
    PVC_DERATE = 0.87
    AL_DERATE = 0.78
    UNARMOR_BOOST = 1.05
    PVC_SC_FACTOR = 0.80
    sections = [16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400]
    d = {}
    for s in sections:
        r_cu = _CU_R[s]
        r_al = _AL_R[s]
        xi = _X[s]
        ci = _C[s]
        air = _CU_YJV22_AIR[s]
        gnd = _CU_YJV22_GND[s]
        dct = _CU_YJV22_DCT[s]
        sc_cu_xlpe = _CU_SC_XLPE[s]
        sc_cu_pvc = round(sc_cu_xlpe * PVC_SC_FACTOR, 2)
        sc_al_xlpe = round(sc_cu_xlpe * 0.61, 2)
        sc_al_pvc = round(sc_cu_xlpe * PVC_SC_FACTOR * 0.61, 2)
        od_yjv22 = _YJV22_CU_OD[s]
        wt_yjv22 = _YJV22_CU_WT[s]
        od_vv22 = od_yjv22 - 1
        wt_vv22 = round(wt_yjv22 * 0.93)
        d[f"YJV22-3x{s}-0.4kV"] = _make_cable(
            "Cu", s, "0.6/1kV", "XLPE", "steel_tape",
            r_cu, xi, ci, air, gnd, dct,
            sc_cu_xlpe, od_yjv22, wt_yjv22,
            "LV", "GB/T 12706.1~3-2020", "国标表值",
        )
        d[f"YJV-3x{s}-0.4kV"] = _make_cable(
            "Cu", s, "0.6/1kV", "XLPE", "none",
            r_cu, xi, ci,
            round(air * UNARMOR_BOOST, 3), round(gnd * UNARMOR_BOOST, 3),
            round(dct * UNARMOR_BOOST, 3),
            sc_cu_xlpe, od_yjv22 - 3, round(wt_yjv22 * 0.90),
            "LV", "GB/T 12706.1~3-2020", "国标表值",
        )
        d[f"VV22-3x{s}-0.4kV"] = _make_cable(
            "Cu", s, "0.6/1kV", "PVC", "steel_tape",
            r_cu, xi, ci,
            round(air * PVC_DERATE, 3), round(gnd * PVC_DERATE, 3),
            round(dct * PVC_DERATE, 3),
            sc_cu_pvc, od_vv22, wt_vv22,
            "LV", "GB/T 12706.1~3-2020", "国标表值",
        )
        d[f"VV-3x{s}-0.4kV"] = _make_cable(
            "Cu", s, "0.6/1kV", "PVC", "none",
            r_cu, xi, ci,
            round(air * PVC_DERATE * UNARMOR_BOOST, 3),
            round(gnd * PVC_DERATE * UNARMOR_BOOST, 3),
            round(dct * PVC_DERATE * UNARMOR_BOOST, 3),
            sc_cu_pvc, od_vv22 - 3, round(wt_vv22 * 0.90),
            "LV", "GB/T 12706.1~3-2020", "国标表值",
        )
        d[f"VLV22-3x{s}-0.4kV"] = _make_cable(
            "Al", s, "0.6/1kV", "PVC", "steel_tape",
            r_al, xi, ci,
            round(air * PVC_DERATE * AL_DERATE, 3),
            round(gnd * PVC_DERATE * AL_DERATE, 3),
            round(dct * PVC_DERATE * AL_DERATE, 3),
            sc_al_pvc, od_vv22 - 1, round(wt_vv22 * 0.75),
            "LV", "GB/T 12706.1~3-2020", "国标表值",
        )
        d[f"VLV-3x{s}-0.4kV"] = _make_cable(
            "Al", s, "0.6/1kV", "PVC", "none",
            r_al, xi, ci,
            round(air * PVC_DERATE * UNARMOR_BOOST * AL_DERATE, 3),
            round(gnd * PVC_DERATE * UNARMOR_BOOST * AL_DERATE, 3),
            round(dct * PVC_DERATE * UNARMOR_BOOST * AL_DERATE, 3),
            sc_al_pvc, od_vv22 - 4, round(wt_vv22 * 0.90 * 0.75),
            "LV", "GB/T 12706.1~3-2020", "国标表值",
        )
    unequal_specs = [
        (70, 35), (95, 50), (120, 70), (150, 70), (185, 95), (240, 120),
    ]
    for main_s, neutral_s in unequal_specs:
        r_cu = _CU_R[main_s]
        xi = _X[main_s]
        ci = _C[main_s]
        air = _CU_YJV22_AIR[main_s]
        gnd = _CU_YJV22_GND[main_s]
        dct = _CU_YJV22_DCT[main_s]
        sc_cu_xlpe = _CU_SC_XLPE[main_s]
        sc_cu_pvc = round(sc_cu_xlpe * PVC_SC_FACTOR, 2)
        od_yjv = _YJV22_CU_OD[main_s] - 3 + 1
        wt_yjv = round(_YJV22_CU_WT[main_s] * 0.90 * 1.05)
        od_vv = _YJV22_CU_OD[main_s] - 1 - 3 + 1
        wt_vv = round(_YJV22_CU_WT[main_s] * 0.93 * 0.90 * 1.05)
        name = f"3x{main_s}+1x{neutral_s}"
        d[f"YJV-{name}-0.4kV"] = _make_cable(
            "Cu", main_s, "0.6/1kV", "XLPE", "none",
            r_cu, xi, ci,
            round(air * UNARMOR_BOOST, 3), round(gnd * UNARMOR_BOOST, 3),
            round(dct * UNARMOR_BOOST, 3),
            sc_cu_xlpe, od_yjv, wt_yjv,
            "LV", "GB/T 12706.1~3-2020", "国标表值",
        )
        d[f"VV-{name}-0.4kV"] = _make_cable(
            "Cu", main_s, "0.6/1kV", "PVC", "none",
            r_cu, xi, ci,
            round(air * PVC_DERATE * UNARMOR_BOOST, 3),
            round(gnd * PVC_DERATE * UNARMOR_BOOST, 3),
            round(dct * PVC_DERATE * UNARMOR_BOOST, 3),
            sc_cu_pvc, od_vv, wt_vv,
            "LV", "GB/T 12706.1~3-2020", "国标表值",
        )
    return d


def _build_hv_110kv():
    _CU_R = {
        240: 0.0754, 300: 0.0601, 400: 0.0470,
        500: 0.0366, 630: 0.0283, 800: 0.0221, 1000: 0.0176,
    }
    _X = {
        240: 0.160, 300: 0.155, 400: 0.148, 500: 0.143,
        630: 0.138, 800: 0.133, 1000: 0.128,
    }
    _C = {
        240: 130, 300: 145, 400: 165, 500: 185,
        630: 210, 800: 240, 1000: 270,
    }
    _AIR = {
        240: 0.510, 300: 0.580, 400: 0.680, 500: 0.770,
        630: 0.870, 800: 0.980, 1000: 1.100,
    }
    _GND = {
        240: 0.460, 300: 0.525, 400: 0.615, 500: 0.700,
        630: 0.790, 800: 0.890, 1000: 1.000,
    }
    _SC = {
        240: 31.7, 300: 39.6, 400: 52.8, 500: 66.0,
        630: 83.2, 800: 105.6, 1000: 132.0,
    }
    _YJV22_OD = {
        240: 72, 300: 76, 400: 80, 500: 84,
        630: 89, 800: 95, 1000: 102,
    }
    _YJV22_WT = {
        240: 7200, 300: 8400, 400: 9800, 500: 11500,
        630: 13800, 800: 16500, 1000: 20000,
    }
    sections = [240, 300, 400, 500, 630, 800, 1000]
    d = {}
    for s in sections:
        r_cu = _CU_R[s]
        xi = _X[s]
        ci = _C[s]
        air = _AIR[s]
        gnd = _GND[s]
        dct = round(gnd * 0.87, 3)
        sc = _SC[s]
        od22 = _YJV22_OD[s]
        wt22 = _YJV22_WT[s]
        d[f"YJV22-1x{s}-110kV"] = _make_cable(
            "Cu", s, "64/110kV", "XLPE", "steel_tape",
            r_cu, xi, ci, air, gnd, dct,
            sc, od22, wt22,
            "HV", "GB/T 11017-2014", "国标表值",
        )
        d[f"YJV-1x{s}-110kV"] = _make_cable(
            "Cu", s, "64/110kV", "XLPE", "none",
            r_cu, xi, ci,
            round(air * 1.05, 3), round(gnd * 1.05, 3), round(dct * 1.05, 3),
            sc, od22 - 5, round(wt22 * 0.88),
            "HV", "GB/T 11017-2014", "国标表值",
        )
    return d


def get_all_cables():
    return {
        "mv_10kv": _build_mv_10kv(),
        "mv_35kv": _build_mv_35kv(),
        "lv_04kv": _build_lv_04kv(),
        "hv_110kv": _build_hv_110kv(),
    }
