import math


def get_all_overhead_lines():
    return _enhance_all_overhead_lines({
        "mv_10kv_insulated": _build_mv_10kv_insulated(),
        "lv_04kv_insulated": _build_lv_04kv_insulated(),
        "bare_conductor": _build_bare_conductor(),
    })


def _enhance_overhead_entry(entry, category):
    insulated = entry.get("insulation_type") is not None
    normal_temp = 90 if entry.get("insulation_type") == "XLPE" else 70 if insulated else 70
    emergency_temp = 105 if entry.get("insulation_type") == "XLPE" else 90 if insulated else 90
    entry.setdefault("rated_current_a", round(entry.get("max_i_ka", 0) * 1000, 1))
    entry.setdefault("max_conductor_temp_normal_c", normal_temp)
    entry.setdefault("max_conductor_temp_emergency_c", emergency_temp)
    entry.setdefault("ampacity_reference", {
        "ambient_air_c": 40,
        "wind_speed_m_s": 0.5,
        "solar_radiation_w_m2": 1000,
        "emissivity": 0.5,
        "absorptivity": 0.5,
        "source_type": "standard_reference_and_engineering_default",
    })
    entry.setdefault("dynamic_line_rating", {
        "model": "heat_balance",
        "inputs": ["ambient_air_c", "wind_speed_m_s", "solar_radiation_w_m2", "max_conductor_temp_c"],
        "standard": entry.get("standard"),
        "source_type": "engineering_model",
    })
    entry.setdefault("mechanical_limits", {
        "span_m": None,
        "ice_thickness_mm": None,
        "wind_pressure_pa": None,
        "minimum_clearance_m": None,
        "sag_limit_note": "Fill from line design and local meteorological conditions.",
    })
    entry.setdefault("lifecycle", {
        "design_life_years": 30,
        "inspection_interval_years": 1,
        "failure_rate_per_100km_year": None,
        "repair_time_h": None,
        "source_type": "engineering_policy",
    })
    entry.setdefault("field_source_types", {
        "rated_current_a": "derived_formula",
        "ampacity_reference": "engineering_default",
        "dynamic_line_rating": "engineering_model",
        "mechanical_limits": "project_specific",
    })
    return entry


def _enhance_all_overhead_lines(data):
    for category, models in data.items():
        for entry in models.values():
            _enhance_overhead_entry(entry, category)
    return data


def _calc_reactance_bare(cross_section, dm_m):
    r_eq = math.sqrt(cross_section / math.pi)
    return round(0.1445 * math.log10(dm_m * 1000 / r_eq) + 0.0157, 4)


def _calc_reactance_table(cross_section):
    dm_list = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]
    return {str(d): _calc_reactance_bare(cross_section, d) for d in dm_list}


def _calc_capacitance_nf(cross_section, dm_m=1.5):
    r_eq = math.sqrt(cross_section / math.pi)
    return round(55.63 / math.log(dm_m * 1000 / r_eq), 2)


def _build_mv_10kv_insulated():
    al_r = {
        50: 0.641, 70: 0.443, 95: 0.320, 120: 0.253,
        150: 0.206, 185: 0.164, 240: 0.125, 300: 0.100,
    }
    cu_r = {
        50: 0.387, 70: 0.268, 95: 0.193, 120: 0.153,
        150: 0.124, 185: 0.0991, 240: 0.0754, 300: 0.0601,
    }
    x_map = {
        50: 0.355, 70: 0.348, 95: 0.340, 120: 0.328,
        150: 0.322, 185: 0.316, 240: 0.308, 300: 0.302,
    }
    c_map = {
        50: 9.5, 70: 10.0, 95: 10.3, 120: 10.8,
        150: 11.0, 185: 11.3, 240: 11.8, 300: 12.2,
    }
    al_i = {
        50: 0.195, 70: 0.240, 95: 0.300, 120: 0.350,
        150: 0.400, 185: 0.460, 240: 0.550, 300: 0.630,
    }
    al_bf = {
        50: 8.0, 70: 11.2, 95: 15.2, 120: 19.0,
        150: 23.7, 185: 29.2, 240: 37.9, 300: 47.4,
    }
    al_w = {
        50: 195, 70: 265, 95: 355, 120: 440,
        150: 545, 185: 670, 240: 860, 300: 1070,
    }
    sections = [50, 70, 95, 120, 150, 185, 240, 300]
    models = {}
    for s in sections:
        models[f"JKLYJ-{s}-10kV"] = {
            "conductor_material": "Al",
            "cross_section_mm2": s,
            "voltage_rating": "10kV",
            "insulation_type": "XLPE",
            "r_ohm_per_km": al_r[s],
            "x_ohm_per_km": x_map[s],
            "c_nf_per_km": c_map[s],
            "r0_ohm_per_km": round(3.0 * al_r[s], 4),
            "x0_ohm_per_km": round(2.0 * x_map[s], 4),
            "c0_nf_per_km": round(0.6 * c_map[s], 2),
            "max_i_ka": al_i[s],
            "breaking_force_kn": al_bf[s],
            "weight_kg_per_km": al_w[s],
            "alpha": 0.00403,
            "type": "ol",
            "q_mm2": s,
            "voltage_rating_category": "MV",
            "standard": "GB/T 14049-2008",
            "source_note": "GB/T 14049-2008 典型参数",
        }
        models[f"JKYJ-{s}-10kV"] = {
            "conductor_material": "Cu",
            "cross_section_mm2": s,
            "voltage_rating": "10kV",
            "insulation_type": "XLPE",
            "r_ohm_per_km": cu_r[s],
            "x_ohm_per_km": x_map[s],
            "c_nf_per_km": c_map[s],
            "r0_ohm_per_km": round(3.0 * cu_r[s], 4),
            "x0_ohm_per_km": round(2.0 * x_map[s], 4),
            "c0_nf_per_km": round(0.6 * c_map[s], 2),
            "max_i_ka": round(1.3 * al_i[s], 4),
            "breaking_force_kn": round(1.3 * al_bf[s], 2),
            "weight_kg_per_km": round(1.15 * al_w[s], 1),
            "alpha": 0.00393,
            "type": "ol",
            "q_mm2": s,
            "voltage_rating_category": "MV",
            "standard": "GB/T 14049-2008",
            "source_note": "GB/T 14049-2008 典型参数",
        }
    return models


def _build_lv_04kv_insulated():
    al_r = {
        16: 2.06, 25: 1.31, 35: 0.946, 50: 0.641, 70: 0.443,
        95: 0.320, 120: 0.253, 150: 0.206, 185: 0.164, 240: 0.125,
    }
    x_map = {
        16: 0.362, 25: 0.348, 35: 0.338, 50: 0.328, 70: 0.318,
        95: 0.310, 120: 0.304, 150: 0.298, 185: 0.292, 240: 0.286,
    }
    al_i = {
        16: 0.085, 25: 0.115, 35: 0.145, 50: 0.180, 70: 0.230,
        95: 0.290, 120: 0.340, 150: 0.390, 185: 0.450, 240: 0.540,
    }
    sections = [16, 25, 35, 50, 70, 95, 120, 150, 185, 240]
    models = {}
    for s in sections:
        c_val = _calc_capacitance_nf(s, 0.8)
        models[f"JKLY-{s}-0.4kV"] = {
            "conductor_material": "Al",
            "cross_section_mm2": s,
            "voltage_rating": "0.6/1kV",
            "insulation_type": "XLPE",
            "r_ohm_per_km": al_r[s],
            "x_ohm_per_km": x_map[s],
            "c_nf_per_km": c_val,
            "r0_ohm_per_km": round(3.0 * al_r[s], 4),
            "x0_ohm_per_km": round(2.0 * x_map[s], 4),
            "c0_nf_per_km": round(0.6 * c_val, 2),
            "max_i_ka": al_i[s],
            "breaking_force_kn": round(s * 0.16, 2),
            "weight_kg_per_km": round(s * 2.8 + 30, 1),
            "alpha": 0.00403,
            "type": "ol",
            "q_mm2": s,
            "voltage_rating_category": "LV",
            "standard": "GB/T 12527-2008",
            "source_note": "GB/T 12527-2008 典型参数",
        }
        models[f"JKLGY-{s}-0.4kV"] = {
            "conductor_material": "Al/Steel",
            "cross_section_mm2": s,
            "voltage_rating": "0.6/1kV",
            "insulation_type": "XLPE",
            "r_ohm_per_km": al_r[s],
            "x_ohm_per_km": x_map[s],
            "c_nf_per_km": c_val,
            "r0_ohm_per_km": round(3.0 * al_r[s], 4),
            "x0_ohm_per_km": round(2.0 * x_map[s], 4),
            "c0_nf_per_km": round(0.6 * c_val, 2),
            "max_i_ka": al_i[s],
            "breaking_force_kn": round(s * 0.25, 2),
            "weight_kg_per_km": round(s * 3.5 + 40, 1),
            "alpha": 0.00403,
            "type": "ol",
            "q_mm2": s,
            "voltage_rating_category": "LV",
            "standard": "GB/T 12527-2008",
            "source_note": "GB/T 12527-2008 典型参数",
        }
        models[f"BLV-{s}-0.4kV"] = {
            "conductor_material": "Al",
            "cross_section_mm2": s,
            "voltage_rating": "0.6/1kV",
            "insulation_type": "PVC",
            "r_ohm_per_km": al_r[s],
            "x_ohm_per_km": x_map[s],
            "c_nf_per_km": c_val,
            "r0_ohm_per_km": round(3.0 * al_r[s], 4),
            "x0_ohm_per_km": round(2.0 * x_map[s], 4),
            "c0_nf_per_km": round(0.6 * c_val, 2),
            "max_i_ka": al_i[s],
            "breaking_force_kn": round(s * 0.14, 2),
            "weight_kg_per_km": round(s * 2.8 + 45, 1),
            "alpha": 0.00403,
            "type": "ol",
            "q_mm2": s,
            "voltage_rating_category": "LV",
            "standard": "GB/T 12527-2008",
            "source_note": "GB/T 12527-2008 典型参数",
        }
    return models


def _build_bare_conductor():
    lj_r = {
        16: 1.96, 25: 1.27, 35: 0.906, 50: 0.641, 70: 0.443,
        95: 0.320, 120: 0.253, 150: 0.206, 185: 0.164, 240: 0.125,
        300: 0.100, 400: 0.0778,
    }
    lgj_r = {
        16: 2.06, 25: 1.34, 35: 0.96, 50: 0.68, 70: 0.47,
        95: 0.34, 120: 0.27, 150: 0.21, 185: 0.17, 240: 0.132,
        300: 0.107, 400: 0.080,
    }
    tj_r = {
        16: 1.20, 25: 0.74, 35: 0.54, 50: 0.39, 70: 0.28,
        95: 0.20, 120: 0.158, 150: 0.123, 185: 0.103, 240: 0.078,
        300: 0.062, 400: 0.047,
    }
    lj_i = {
        16: 0.105, 25: 0.135, 35: 0.170, 50: 0.215, 70: 0.265,
        95: 0.325, 120: 0.375, 150: 0.440, 185: 0.500, 240: 0.610,
        300: 0.700, 400: 0.830,
    }
    sections = [16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400]
    models = {}
    for s in sections:
        x_table = _calc_reactance_table(s)
        c_val = _calc_capacitance_nf(s, 1.5)
        models[f"LJ-{s}"] = {
            "conductor_material": "Al",
            "cross_section_mm2": s,
            "r_ohm_per_km": lj_r[s],
            "x_ohm_per_km_table": x_table,
            "c_nf_per_km": c_val,
            "max_i_ka": lj_i[s],
            "breaking_force_kn": round(s * 0.16, 2),
            "weight_kg_per_km": round(s * 2.7, 1),
            "alpha": 0.00403,
            "type": "ol",
            "q_mm2": s,
            "standard": "GB/T 1179-2017",
            "source_note": "GB/T 1179-2017 典型参数",
        }
        models[f"LGJ-{s}"] = {
            "conductor_material": "Al/Steel",
            "cross_section_mm2": s,
            "r_ohm_per_km": lgj_r[s],
            "x_ohm_per_km_table": x_table,
            "c_nf_per_km": c_val,
            "max_i_ka": lj_i[s],
            "breaking_force_kn": round(s * 0.28, 2),
            "weight_kg_per_km": round(s * 3.5, 1),
            "alpha": 0.00403,
            "type": "ol",
            "q_mm2": s,
            "standard": "GB/T 1179-2017",
            "source_note": "GB/T 1179-2017 典型参数",
        }
        models[f"TJ-{s}"] = {
            "conductor_material": "Cu",
            "cross_section_mm2": s,
            "r_ohm_per_km": tj_r[s],
            "x_ohm_per_km_table": x_table,
            "c_nf_per_km": c_val,
            "max_i_ka": round(1.3 * lj_i[s], 4),
            "breaking_force_kn": round(s * 0.22, 2),
            "weight_kg_per_km": round(s * 8.9, 1),
            "alpha": 0.00393,
            "type": "ol",
            "q_mm2": s,
            "standard": "GB/T 1179-2017",
            "source_note": "GB/T 1179-2017 典型参数",
        }
    return models
