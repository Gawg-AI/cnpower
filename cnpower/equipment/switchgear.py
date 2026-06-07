from functools import lru_cache


def _max_number(value, default=None):
    if isinstance(value, (list, tuple)):
        numbers = [_max_number(item, None) for item in value]
        numbers = [item for item in numbers if item is not None]
        return max(numbers) if numbers else default
    if isinstance(value, (int, float)):
        return value
    return default


def _enhance_switchgear_entry(entry, category):
    rated_current = _max_number(entry.get("rated_current_a"), entry.get("frame_current_a"))
    if rated_current is None:
        rated_current = _max_number(entry.get("frame_current_a"), None)
    if rated_current is not None:
        entry.setdefault("rated_current_max_a", rated_current)
    if "rated_current_a" not in entry:
        if "rated_current_series" in entry:
            series_max = _max_number(entry["rated_current_series"])
            if series_max is not None:
                entry["rated_current_a"] = series_max
        elif "frame_current_a" in entry:
            entry["rated_current_a"] = entry["frame_current_a"]
    if "breaking_capacity_ka" in entry:
        entry.setdefault("rated_short_circuit_breaking_ka", entry["breaking_capacity_ka"])

    if "rated_short_time_withstand_ka_4s" in entry:
        entry.setdefault("rated_short_time_duration_s", 4)
        entry.setdefault("short_time_withstand", {
            "current_ka": entry["rated_short_time_withstand_ka_4s"],
            "duration_s": 4,
            "i2t_ka2s": round(entry["rated_short_time_withstand_ka_4s"] ** 2 * 4, 3),
            "source_type": "standard_table_or_manufacturer_typical",
        })
    elif category in ("circuit_breaker_lv", "recloser"):
        breaking = _max_number(entry.get("rated_short_circuit_breaking_ka"), _max_number(entry.get("breaking_capacity_ka"), None))
        if breaking is not None:
            entry.setdefault("rated_short_time_duration_s", 1)
            entry.setdefault("short_time_withstand", {
                "current_ka": breaking,
                "duration_s": 1,
                "i2t_ka2s": round(breaking ** 2, 3),
                "source_type": "engineering_default",
            })

    if category == "switchgear_cabinet":
        entry.setdefault("internal_arc_class", {
            "iac_class": None,
            "iac_current_ka": entry.get("rated_short_circuit_breaking_ka"),
            "iac_duration_s": 1,
            "standard": "GB/T 3906-2020",
            "source_type": "project_specific_required",
        })
        entry.setdefault("loss_of_service_continuity_class", None)
        entry.setdefault("partition_class", None)
    if category in ("circuit_breaker_mv", "circuit_breaker_lv", "load_switch", "recloser", "sectionalizer"):
        entry.setdefault("endurance", {
            "mechanical_life_cycles": entry.get("mechanical_life_cycles"),
            "electrical_life_cycles": None,
            "maintenance_interval_years": 3,
            "operation_count_limit": entry.get("mechanical_life_cycles"),
            "source_type": "manufacturer_typical_or_engineering_default",
        })
        entry.setdefault("temperature_rise_limit_c", None)
        entry.setdefault("operating_sequence", entry.get("reclose_sequence"))
    if category == "fuse_mv":
        curve = entry.get("time_current_curve_data", [])
        entry.setdefault("time_current_curve", {
            "x_axis": "multiple_of_rated_current",
            "y_axis": "clearing_time_s",
            "points": curve,
            "curve_type": "typical_minimum_melting_or_total_clearing",
            "standard": "GB/T 15166.2-2023",
        })
        entry.setdefault("selection_guide", {
            "standard": "GB/T 15166.6-2023",
            "protected_equipment": entry.get("type"),
            "coordination_margin_s": 0.3,
            "source_type": "standard_reference_and_engineering_default",
        })
        if entry.get("rated_current_a"):
            entry.setdefault("minimum_melting_current_a", round(entry["rated_current_a"] * 2, 2))
    entry.setdefault("field_source_types", {
        "short_time_withstand": "standard_table_or_engineering_default",
        "endurance": "manufacturer_typical_or_engineering_default",
        "internal_arc_class": "project_specific_required",
    })
    return entry


def _enhance_all_switchgear(data):
    for category, models in data.items():
        for entry in models.values():
            _enhance_switchgear_entry(entry, category)
    return data


@lru_cache(maxsize=1)
def get_all_switchgear():
    return _enhance_all_switchgear({
        "switchgear_cabinet": {
            "KYN28A-12": {
                "type": "metal_clad_withdrawable",
                "rated_voltage_kv": 12,
                "rated_current_a": [630, 1250, 2000, 2500, 3150],
                "rated_short_circuit_breaking_ka": 25,
                "rated_short_circuit_making_ka": 63,
                "rated_short_time_withstand_ka_4s": 25,
                "protection_class": "IP4X",
                "operation_type": "manual/electric",
                "dimension_l_mm": 800,
                "dimension_w_mm": 1200,
                "dimension_h_mm": 2300,
                "standard": "GB/T 11022-2020",
                "source_note": "参数依据GB/T 11022-2020及主流厂家产品手册"
            },
            "XGN66-12": {
                "type": "fixed",
                "rated_voltage_kv": 12,
                "rated_current_a": [630, 1250],
                "rated_short_circuit_breaking_ka": 25,
                "rated_short_circuit_making_ka": 63,
                "rated_short_time_withstand_ka_4s": 25,
                "protection_class": "IP3X",
                "operation_type": "manual/electric",
                "dimension_l_mm": 900,
                "dimension_w_mm": 1100,
                "dimension_h_mm": 2350,
                "standard": "GB/T 11022-2020",
                "source_note": "参数依据GB/T 11022-2020及主流厂家产品手册"
            },
            "RMU_SF6": {
                "type": "ring_main_unit_sf6",
                "rated_voltage_kv": 12,
                "rated_current_a": [630],
                "rated_short_circuit_breaking_ka": 20,
                "rated_short_circuit_making_ka": 50,
                "rated_short_time_withstand_ka_4s": 20,
                "protection_class": "IP3X",
                "operation_type": "manual/electric",
                "dimension_l_mm": 750,
                "dimension_w_mm": 850,
                "dimension_h_mm": 1600,
                "standard": "GB/T 11022-2020",
                "source_note": "参数依据GB/T 11022-2020及主流厂家产品手册"
            },
            "RMU_VCB": {
                "type": "ring_main_unit_vacuum",
                "rated_voltage_kv": 12,
                "rated_current_a": [630],
                "rated_short_circuit_breaking_ka": 20,
                "rated_short_circuit_making_ka": 50,
                "rated_short_time_withstand_ka_4s": 20,
                "protection_class": "IP3X",
                "operation_type": "manual/electric",
                "dimension_l_mm": 800,
                "dimension_w_mm": 900,
                "dimension_h_mm": 1700,
                "standard": "GB/T 11022-2020",
                "source_note": "参数依据GB/T 11022-2020及主流厂家产品手册"
            }
        },
        "circuit_breaker_mv": {
            "VS1-12/630": {
                "type": "vacuum",
                "rated_voltage_kv": 12,
                "rated_current_a": 630,
                "rated_short_circuit_breaking_ka": 20,
                "rated_short_circuit_making_ka": 50,
                "rated_short_time_withstand_ka_4s": 20,
                "closing_time_ms": 60,
                "opening_time_ms": 40,
                "mechanical_life_cycles": 10000,
                "standard": "GB/T 1984-2024",
                "source_note": "参数依据GB/T 1984-2024及主流厂家产品手册"
            },
            "VS1-12/1000": {
                "type": "vacuum",
                "rated_voltage_kv": 12,
                "rated_current_a": 1000,
                "rated_short_circuit_breaking_ka": 25,
                "rated_short_circuit_making_ka": 63,
                "rated_short_time_withstand_ka_4s": 25,
                "closing_time_ms": 60,
                "opening_time_ms": 40,
                "mechanical_life_cycles": 10000,
                "standard": "GB/T 1984-2024",
                "source_note": "参数依据GB/T 1984-2024及主流厂家产品手册"
            },
            "VS1-12/1250": {
                "type": "vacuum",
                "rated_voltage_kv": 12,
                "rated_current_a": 1250,
                "rated_short_circuit_breaking_ka": 25,
                "rated_short_circuit_making_ka": 63,
                "rated_short_time_withstand_ka_4s": 25,
                "closing_time_ms": 60,
                "opening_time_ms": 40,
                "mechanical_life_cycles": 10000,
                "standard": "GB/T 1984-2024",
                "source_note": "参数依据GB/T 1984-2024及主流厂家产品手册"
            },
            "VS1-12/2000": {
                "type": "vacuum",
                "rated_voltage_kv": 12,
                "rated_current_a": 2000,
                "rated_short_circuit_breaking_ka": 31.5,
                "rated_short_circuit_making_ka": 80,
                "rated_short_time_withstand_ka_4s": 31.5,
                "closing_time_ms": 60,
                "opening_time_ms": 40,
                "mechanical_life_cycles": 10000,
                "standard": "GB/T 1984-2024",
                "source_note": "参数依据GB/T 1984-2024及主流厂家产品手册"
            },
            "VS1-12/2500": {
                "type": "vacuum",
                "rated_voltage_kv": 12,
                "rated_current_a": 2500,
                "rated_short_circuit_breaking_ka": 31.5,
                "rated_short_circuit_making_ka": 80,
                "rated_short_time_withstand_ka_4s": 31.5,
                "closing_time_ms": 60,
                "opening_time_ms": 40,
                "mechanical_life_cycles": 10000,
                "standard": "GB/T 1984-2024",
                "source_note": "参数依据GB/T 1984-2024及主流厂家产品手册"
            },
            "VS1-12/3150": {
                "type": "vacuum",
                "rated_voltage_kv": 12,
                "rated_current_a": 3150,
                "rated_short_circuit_breaking_ka": 31.5,
                "rated_short_circuit_making_ka": 80,
                "rated_short_time_withstand_ka_4s": 31.5,
                "closing_time_ms": 60,
                "opening_time_ms": 40,
                "mechanical_life_cycles": 10000,
                "standard": "GB/T 1984-2024",
                "source_note": "参数依据GB/T 1984-2024及主流厂家产品手册"
            },
            "VD4-12/630": {
                "type": "vacuum",
                "rated_voltage_kv": 12,
                "rated_current_a": 630,
                "rated_short_circuit_breaking_ka": 25,
                "rated_short_circuit_making_ka": 63,
                "rated_short_time_withstand_ka_4s": 25,
                "closing_time_ms": 55,
                "opening_time_ms": 35,
                "mechanical_life_cycles": 10000,
                "standard": "GB/T 1984-2024",
                "source_note": "参数依据GB/T 1984-2024及ABB产品手册"
            },
            "VD4-12/1000": {
                "type": "vacuum",
                "rated_voltage_kv": 12,
                "rated_current_a": 1000,
                "rated_short_circuit_breaking_ka": 25,
                "rated_short_circuit_making_ka": 63,
                "rated_short_time_withstand_ka_4s": 25,
                "closing_time_ms": 55,
                "opening_time_ms": 35,
                "mechanical_life_cycles": 10000,
                "standard": "GB/T 1984-2024",
                "source_note": "参数依据GB/T 1984-2024及ABB产品手册"
            },
            "VD4-12/1250": {
                "type": "vacuum",
                "rated_voltage_kv": 12,
                "rated_current_a": 1250,
                "rated_short_circuit_breaking_ka": 25,
                "rated_short_circuit_making_ka": 63,
                "rated_short_time_withstand_ka_4s": 25,
                "closing_time_ms": 55,
                "opening_time_ms": 35,
                "mechanical_life_cycles": 10000,
                "standard": "GB/T 1984-2024",
                "source_note": "参数依据GB/T 1984-2024及ABB产品手册"
            },
            "VD4-12/2000": {
                "type": "vacuum",
                "rated_voltage_kv": 12,
                "rated_current_a": 2000,
                "rated_short_circuit_breaking_ka": 31.5,
                "rated_short_circuit_making_ka": 80,
                "rated_short_time_withstand_ka_4s": 31.5,
                "closing_time_ms": 55,
                "opening_time_ms": 35,
                "mechanical_life_cycles": 10000,
                "standard": "GB/T 1984-2024",
                "source_note": "参数依据GB/T 1984-2024及ABB产品手册"
            },
            "VD4-12/2500": {
                "type": "vacuum",
                "rated_voltage_kv": 12,
                "rated_current_a": 2500,
                "rated_short_circuit_breaking_ka": 31.5,
                "rated_short_circuit_making_ka": 80,
                "rated_short_time_withstand_ka_4s": 31.5,
                "closing_time_ms": 55,
                "opening_time_ms": 35,
                "mechanical_life_cycles": 10000,
                "standard": "GB/T 1984-2024",
                "source_note": "参数依据GB/T 1984-2024及ABB产品手册"
            },
            "VD4-12/3150": {
                "type": "vacuum",
                "rated_voltage_kv": 12,
                "rated_current_a": 3150,
                "rated_short_circuit_breaking_ka": 31.5,
                "rated_short_circuit_making_ka": 80,
                "rated_short_time_withstand_ka_4s": 31.5,
                "closing_time_ms": 55,
                "opening_time_ms": 35,
                "mechanical_life_cycles": 10000,
                "standard": "GB/T 1984-2024",
                "source_note": "参数依据GB/T 1984-2024及ABB产品手册"
            },
            "ZN28-12/630": {
                "type": "vacuum",
                "rated_voltage_kv": 12,
                "rated_current_a": 630,
                "rated_short_circuit_breaking_ka": 20,
                "rated_short_circuit_making_ka": 50,
                "rated_short_time_withstand_ka_4s": 20,
                "closing_time_ms": 70,
                "opening_time_ms": 50,
                "mechanical_life_cycles": 10000,
                "standard": "GB/T 1984-2024",
                "source_note": "参数依据GB/T 1984-2024及主流厂家产品手册"
            },
            "ZN28-12/1000": {
                "type": "vacuum",
                "rated_voltage_kv": 12,
                "rated_current_a": 1000,
                "rated_short_circuit_breaking_ka": 20,
                "rated_short_circuit_making_ka": 50,
                "rated_short_time_withstand_ka_4s": 20,
                "closing_time_ms": 70,
                "opening_time_ms": 50,
                "mechanical_life_cycles": 10000,
                "standard": "GB/T 1984-2024",
                "source_note": "参数依据GB/T 1984-2024及主流厂家产品手册"
            },
            "ZN28-12/1250": {
                "type": "vacuum",
                "rated_voltage_kv": 12,
                "rated_current_a": 1250,
                "rated_short_circuit_breaking_ka": 25,
                "rated_short_circuit_making_ka": 63,
                "rated_short_time_withstand_ka_4s": 25,
                "closing_time_ms": 70,
                "opening_time_ms": 50,
                "mechanical_life_cycles": 10000,
                "standard": "GB/T 1984-2024",
                "source_note": "参数依据GB/T 1984-2024及主流厂家产品手册"
            },
            "ZN28-12/2000": {
                "type": "vacuum",
                "rated_voltage_kv": 12,
                "rated_current_a": 2000,
                "rated_short_circuit_breaking_ka": 31.5,
                "rated_short_circuit_making_ka": 80,
                "rated_short_time_withstand_ka_4s": 31.5,
                "closing_time_ms": 70,
                "opening_time_ms": 50,
                "mechanical_life_cycles": 10000,
                "standard": "GB/T 1984-2024",
                "source_note": "参数依据GB/T 1984-2024及主流厂家产品手册"
            },
            "ZN28-12/2500": {
                "type": "vacuum",
                "rated_voltage_kv": 12,
                "rated_current_a": 2500,
                "rated_short_circuit_breaking_ka": 31.5,
                "rated_short_circuit_making_ka": 80,
                "rated_short_time_withstand_ka_4s": 31.5,
                "closing_time_ms": 70,
                "opening_time_ms": 50,
                "mechanical_life_cycles": 10000,
                "standard": "GB/T 1984-2024",
                "source_note": "参数依据GB/T 1984-2024及主流厂家产品手册"
            },
            "ZN28-12/3150": {
                "type": "vacuum",
                "rated_voltage_kv": 12,
                "rated_current_a": 3150,
                "rated_short_circuit_breaking_ka": 31.5,
                "rated_short_circuit_making_ka": 80,
                "rated_short_time_withstand_ka_4s": 31.5,
                "closing_time_ms": 70,
                "opening_time_ms": 50,
                "mechanical_life_cycles": 10000,
                "standard": "GB/T 1984-2024",
                "source_note": "参数依据GB/T 1984-2024及主流厂家产品手册"
            },
            "LW3-12/630": {
                "type": "sf6",
                "rated_voltage_kv": 12,
                "rated_current_a": 630,
                "rated_short_circuit_breaking_ka": 20,
                "rated_short_circuit_making_ka": 50,
                "rated_short_time_withstand_ka_4s": 20,
                "closing_time_ms": 100,
                "opening_time_ms": 60,
                "mechanical_life_cycles": 5000,
                "standard": "GB/T 1984-2024",
                "source_note": "参数依据GB/T 1984-2024及主流厂家产品手册"
            },
            "LW3-12/1000": {
                "type": "sf6",
                "rated_voltage_kv": 12,
                "rated_current_a": 1000,
                "rated_short_circuit_breaking_ka": 25,
                "rated_short_circuit_making_ka": 63,
                "rated_short_time_withstand_ka_4s": 25,
                "closing_time_ms": 100,
                "opening_time_ms": 60,
                "mechanical_life_cycles": 5000,
                "standard": "GB/T 1984-2024",
                "source_note": "参数依据GB/T 1984-2024及主流厂家产品手册"
            },
            "LW3-12/1250": {
                "type": "sf6",
                "rated_voltage_kv": 12,
                "rated_current_a": 1250,
                "rated_short_circuit_breaking_ka": 25,
                "rated_short_circuit_making_ka": 63,
                "rated_short_time_withstand_ka_4s": 25,
                "closing_time_ms": 100,
                "opening_time_ms": 60,
                "mechanical_life_cycles": 5000,
                "standard": "GB/T 1984-2024",
                "source_note": "参数依据GB/T 1984-2024及主流厂家产品手册"
            }
        },
        "load_switch": {
            "FN7-12/400": {
                "type": "vacuum",
                "rated_voltage_kv": 12,
                "rated_current_a": 400,
                "rated_short_circuit_making_ka": 40,
                "rated_short_time_withstand_ka_4s": 12.5,
                "standard": "GB/T 3804-2017",
                "source_note": "参数依据GB/T 3804-2017及主流厂家产品手册"
            },
            "FN7-12/630": {
                "type": "vacuum",
                "rated_voltage_kv": 12,
                "rated_current_a": 630,
                "rated_short_circuit_making_ka": 50,
                "rated_short_time_withstand_ka_4s": 20,
                "standard": "GB/T 3804-2017",
                "source_note": "参数依据GB/T 3804-2017及主流厂家产品手册"
            },
            "FLN36-12/630": {
                "type": "sf6",
                "rated_voltage_kv": 12,
                "rated_current_a": 630,
                "rated_short_circuit_making_ka": 50,
                "rated_short_time_withstand_ka_4s": 20,
                "standard": "GB/T 3804-2017",
                "source_note": "参数依据GB/T 3804-2017及主流厂家产品手册"
            }
        },
        "fuse_mv": {
            "XRNT-12": {
                "type": "transformer_protection",
                "rated_voltage_kv": 12,
                "rated_current_a": 125,
                "rated_breaking_current_ka": 40,
                "fuse_element_current_series": [10, 16, 20, 25, 31.5, 40, 50, 63, 80, 100, 125],
                "time_current_curve_data": [
                    [2.0, 300.0],
                    [3.0, 30.0],
                    [5.0, 3.0],
                    [8.0, 0.5],
                    [10.0, 0.2],
                    [20.0, 0.02]
                ],
                "standard": "GB/T 15166.2-2023",
                "source_note": "参数依据GB/T 15166.2-2023及主流厂家产品手册"
            },
            "XRNP-12": {
                "type": "pt_protection",
                "rated_voltage_kv": 12,
                "rated_current_a": 3.15,
                "rated_breaking_current_ka": 50,
                "fuse_element_current_series": [0.5, 1, 2, 3.15],
                "time_current_curve_data": [
                    [2.0, 60.0],
                    [3.0, 5.0],
                    [5.0, 0.5],
                    [8.0, 0.05],
                    [10.0, 0.02]
                ],
                "standard": "GB/T 15166.2-2023",
                "source_note": "参数依据GB/T 15166.2-2023及主流厂家产品手册"
            },
            "RW11-12": {
                "type": "drop_out",
                "rated_voltage_kv": 12,
                "rated_current_a": 200,
                "rated_breaking_current_ka": 12.5,
                "fuse_element_current_series": [50, 100, 200],
                "time_current_curve_data": [
                    [2.0, 300.0],
                    [3.0, 30.0],
                    [5.0, 3.0],
                    [8.0, 0.5],
                    [10.0, 0.1],
                    [20.0, 0.01]
                ],
                "standard": "GB/T 15166.2-2023",
                "source_note": "参数依据GB/T 15166.2-2023及主流厂家产品手册"
            }
        },
        "circuit_breaker_lv": {
            "DW45-2000": {
                "type": "acb",
                "rated_voltage_v": 400,
                "frame_current_a": 2000,
                "rated_current_series": [630, 800, 1000, 1250, 1600, 2000],
                "breaking_capacity_ka": 65,
                "pole_count": 3,
                "trip_type": "electronic",
                "standard": "GB 50054-2023",
                "source_note": "参数依据GB 50054-2023及主流厂家产品手册"
            },
            "DW45-3200": {
                "type": "acb",
                "rated_voltage_v": 400,
                "frame_current_a": 3200,
                "rated_current_series": [2000, 2500, 3200],
                "breaking_capacity_ka": 80,
                "pole_count": 3,
                "trip_type": "electronic",
                "standard": "GB 50054-2023",
                "source_note": "参数依据GB 50054-2023及主流厂家产品手册"
            },
            "DW45-4000": {
                "type": "acb",
                "rated_voltage_v": 400,
                "frame_current_a": 4000,
                "rated_current_series": [2500, 3200, 4000],
                "breaking_capacity_ka": 100,
                "pole_count": 3,
                "trip_type": "electronic",
                "standard": "GB 50054-2023",
                "source_note": "参数依据GB 50054-2023及主流厂家产品手册"
            },
            "DW45-5000": {
                "type": "acb",
                "rated_voltage_v": 400,
                "frame_current_a": 5000,
                "rated_current_series": [3200, 4000, 5000],
                "breaking_capacity_ka": 100,
                "pole_count": 3,
                "trip_type": "electronic",
                "standard": "GB 50054-2023",
                "source_note": "参数依据GB 50054-2023及主流厂家产品手册"
            },
            "DW45-6300": {
                "type": "acb",
                "rated_voltage_v": 400,
                "frame_current_a": 6300,
                "rated_current_series": [4000, 5000, 6300],
                "breaking_capacity_ka": 120,
                "pole_count": 3,
                "trip_type": "electronic",
                "standard": "GB 50054-2023",
                "source_note": "参数依据GB 50054-2023及主流厂家产品手册"
            },
            "DW15-200": {
                "type": "acb",
                "rated_voltage_v": 400,
                "frame_current_a": 200,
                "rated_current_series": [100, 160, 200],
                "breaking_capacity_ka": 20,
                "pole_count": 3,
                "trip_type": "thermal_magnetic",
                "standard": "GB 50054-2023",
                "source_note": "参数依据GB 50054-2023及主流厂家产品手册"
            },
            "DW15-400": {
                "type": "acb",
                "rated_voltage_v": 400,
                "frame_current_a": 400,
                "rated_current_series": [200, 315, 400],
                "breaking_capacity_ka": 25,
                "pole_count": 3,
                "trip_type": "thermal_magnetic",
                "standard": "GB 50054-2023",
                "source_note": "参数依据GB 50054-2023及主流厂家产品手册"
            },
            "DW15-630": {
                "type": "acb",
                "rated_voltage_v": 400,
                "frame_current_a": 630,
                "rated_current_series": [315, 400, 630],
                "breaking_capacity_ka": 30,
                "pole_count": 3,
                "trip_type": "thermal_magnetic",
                "standard": "GB 50054-2023",
                "source_note": "参数依据GB 50054-2023及主流厂家产品手册"
            },
            "DW15-1000": {
                "type": "acb",
                "rated_voltage_v": 400,
                "frame_current_a": 1000,
                "rated_current_series": [630, 800, 1000],
                "breaking_capacity_ka": 40,
                "pole_count": 3,
                "trip_type": "electronic",
                "standard": "GB 50054-2023",
                "source_note": "参数依据GB 50054-2023及主流厂家产品手册"
            },
            "DW15-1600": {
                "type": "acb",
                "rated_voltage_v": 400,
                "frame_current_a": 1600,
                "rated_current_series": [1000, 1250, 1600],
                "breaking_capacity_ka": 40,
                "pole_count": 3,
                "trip_type": "electronic",
                "standard": "GB 50054-2023",
                "source_note": "参数依据GB 50054-2023及主流厂家产品手册"
            },
            "DW15-2500": {
                "type": "acb",
                "rated_voltage_v": 400,
                "frame_current_a": 2500,
                "rated_current_series": [1600, 2000, 2500],
                "breaking_capacity_ka": 60,
                "pole_count": 3,
                "trip_type": "electronic",
                "standard": "GB 50054-2023",
                "source_note": "参数依据GB 50054-2023及主流厂家产品手册"
            },
            "DW15-4000": {
                "type": "acb",
                "rated_voltage_v": 400,
                "frame_current_a": 4000,
                "rated_current_series": [2500, 3200, 4000],
                "breaking_capacity_ka": 80,
                "pole_count": 3,
                "trip_type": "electronic",
                "standard": "GB 50054-2023",
                "source_note": "参数依据GB 50054-2023及主流厂家产品手册"
            },
            "DZ20-100": {
                "type": "mccb",
                "rated_voltage_v": 400,
                "frame_current_a": 100,
                "rated_current_series": [16, 20, 32, 40, 50, 63, 80, 100],
                "breaking_capacity_ka": 14,
                "pole_count": 3,
                "trip_type": "thermal_magnetic",
                "standard": "GB 50054-2023",
                "source_note": "参数依据GB 50054-2023及主流厂家产品手册"
            },
            "DZ20-225": {
                "type": "mccb",
                "rated_voltage_v": 400,
                "frame_current_a": 225,
                "rated_current_series": [100, 125, 160, 180, 200, 225],
                "breaking_capacity_ka": 25,
                "pole_count": 3,
                "trip_type": "thermal_magnetic",
                "standard": "GB 50054-2023",
                "source_note": "参数依据GB 50054-2023及主流厂家产品手册"
            },
            "DZ20-400": {
                "type": "mccb",
                "rated_voltage_v": 400,
                "frame_current_a": 400,
                "rated_current_series": [200, 250, 315, 350, 400],
                "breaking_capacity_ka": 30,
                "pole_count": 3,
                "trip_type": "thermal_magnetic",
                "standard": "GB 50054-2023",
                "source_note": "参数依据GB 50054-2023及主流厂家产品手册"
            },
            "DZ20-630": {
                "type": "mccb",
                "rated_voltage_v": 400,
                "frame_current_a": 630,
                "rated_current_series": [400, 500, 630],
                "breaking_capacity_ka": 30,
                "pole_count": 3,
                "trip_type": "thermal_magnetic",
                "standard": "GB 50054-2023",
                "source_note": "参数依据GB 50054-2023及主流厂家产品手册"
            },
            "CM1-63": {
                "type": "mccb",
                "rated_voltage_v": 400,
                "frame_current_a": 63,
                "rated_current_series": [10, 16, 20, 25, 32, 40, 50, 63],
                "breaking_capacity_ka": 25,
                "pole_count": 3,
                "trip_type": "thermal_magnetic",
                "standard": "GB 50054-2023",
                "source_note": "参数依据GB 50054-2023及主流厂家产品手册"
            },
            "CM1-100": {
                "type": "mccb",
                "rated_voltage_v": 400,
                "frame_current_a": 100,
                "rated_current_series": [16, 20, 32, 40, 50, 63, 80, 100],
                "breaking_capacity_ka": 35,
                "pole_count": 3,
                "trip_type": "thermal_magnetic",
                "standard": "GB 50054-2023",
                "source_note": "参数依据GB 50054-2023及主流厂家产品手册"
            },
            "CM1-225": {
                "type": "mccb",
                "rated_voltage_v": 400,
                "frame_current_a": 225,
                "rated_current_series": [100, 125, 160, 180, 200, 225],
                "breaking_capacity_ka": 35,
                "pole_count": 3,
                "trip_type": "thermal_magnetic",
                "standard": "GB 50054-2023",
                "source_note": "参数依据GB 50054-2023及主流厂家产品手册"
            },
            "CM1-400": {
                "type": "mccb",
                "rated_voltage_v": 400,
                "frame_current_a": 400,
                "rated_current_series": [200, 250, 315, 350, 400],
                "breaking_capacity_ka": 50,
                "pole_count": 3,
                "trip_type": "thermal_magnetic",
                "standard": "GB 50054-2023",
                "source_note": "参数依据GB 50054-2023及主流厂家产品手册"
            },
            "CM1-630": {
                "type": "mccb",
                "rated_voltage_v": 400,
                "frame_current_a": 630,
                "rated_current_series": [400, 500, 630],
                "breaking_capacity_ka": 50,
                "pole_count": 3,
                "trip_type": "thermal_magnetic",
                "standard": "GB 50054-2023",
                "source_note": "参数依据GB 50054-2023及主流厂家产品手册"
            },
            "CM1-800": {
                "type": "mccb",
                "rated_voltage_v": 400,
                "frame_current_a": 800,
                "rated_current_series": [630, 700, 800],
                "breaking_capacity_ka": 50,
                "pole_count": 3,
                "trip_type": "thermal_magnetic",
                "standard": "GB 50054-2023",
                "source_note": "参数依据GB 50054-2023及主流厂家产品手册"
            },
            "MCB-1P": {
                "type": "mcb",
                "rated_voltage_v": 400,
                "frame_current_a": 63,
                "rated_current_series": [6, 10, 16, 20, 25, 32, 40, 50, 63],
                "breaking_capacity_ka": 6,
                "pole_count": 1,
                "trip_type": "thermal_magnetic",
                "standard": "GB/T 10963.1-2023",
                "source_note": "参数依据GB/T 10963.1-2023及主流厂家产品手册"
            },
            "MCB-2P": {
                "type": "mcb",
                "rated_voltage_v": 400,
                "frame_current_a": 63,
                "rated_current_series": [6, 10, 16, 20, 25, 32, 40, 50, 63],
                "breaking_capacity_ka": 6,
                "pole_count": 2,
                "trip_type": "thermal_magnetic",
                "standard": "GB/T 10963.1-2023",
                "source_note": "参数依据GB/T 10963.1-2023及主流厂家产品手册"
            },
            "MCB-3P": {
                "type": "mcb",
                "rated_voltage_v": 400,
                "frame_current_a": 63,
                "rated_current_series": [6, 10, 16, 20, 25, 32, 40, 50, 63],
                "breaking_capacity_ka": 6,
                "pole_count": 3,
                "trip_type": "thermal_magnetic",
                "standard": "GB/T 10963.1-2023",
                "source_note": "参数依据GB/T 10963.1-2023及主流厂家产品手册"
            }
        },
        "recloser": {
            "CH4-12/400": {
                "type": "auto_recloser",
                "rated_voltage_kv": 12,
                "rated_current_a": 400,
                "rated_short_circuit_breaking_ka": 16,
                "reclose_sequence": [0.5, 2.0],
                "standard": "GB/T 25289-2010",
                "source_note": "参数依据GB/T 25289-2010及主流厂家产品手册"
            },
            "CH4-12/630": {
                "type": "auto_recloser",
                "rated_voltage_kv": 12,
                "rated_current_a": 630,
                "rated_short_circuit_breaking_ka": 20,
                "reclose_sequence": [0.5, 2.0],
                "standard": "GB/T 25289-2010",
                "source_note": "参数依据GB/T 25289-2010及主流厂家产品手册"
            }
        },
        "sectionalizer": {
            "FDW-12/200": {
                "type": "auto_sectionalizer",
                "rated_voltage_kv": 12,
                "rated_current_a": 200,
                "rated_short_circuit_making_ka": 40,
                "counting_times": 2,
                "standard": "GB/T 25289-2010",
                "source_note": "参数依据GB/T 25289-2010及主流厂家产品手册"
            },
            "FDW-12/400": {
                "type": "auto_sectionalizer",
                "rated_voltage_kv": 12,
                "rated_current_a": 400,
                "rated_short_circuit_making_ka": 50,
                "counting_times": 2,
                "standard": "GB/T 25289-2010",
                "source_note": "参数依据GB/T 25289-2010及主流厂家产品手册"
            },
            "FDW-12/630": {
                "type": "auto_sectionalizer",
                "rated_voltage_kv": 12,
                "rated_current_a": 630,
                "rated_short_circuit_making_ka": 50,
                "counting_times": 3,
                "standard": "GB/T 25289-2010",
                "source_note": "参数依据GB/T 25289-2010及主流厂家产品手册"
            }
        }
    })
