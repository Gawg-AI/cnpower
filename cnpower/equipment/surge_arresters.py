def get_all_surge_arresters():
    arrester_mv = {
        "HY5WZ-17/45": {
            "rated_voltage_kv": 17,
            "continuous_operating_voltage_kv": 13.6,
            "nominal_discharge_current_ka": 5,
            "residual_voltage_kv": 45.0,
            "standard": "GB/T 11032-2020",
            "source_note": "HY5WZ-17/45型10kV系统复合外套无间隙金属氧化物避雷器"
        },
        "HY5WZ-51/134": {
            "rated_voltage_kv": 51,
            "continuous_operating_voltage_kv": 40.8,
            "nominal_discharge_current_ka": 5,
            "residual_voltage_kv": 134.0,
            "standard": "GB/T 11032-2020",
            "source_note": "HY5WZ-51/134型35kV系统复合外套无间隙金属氧化物避雷器(5kA级)"
        },
        "HY10WZ-51/134": {
            "rated_voltage_kv": 51,
            "continuous_operating_voltage_kv": 40.8,
            "nominal_discharge_current_ka": 10,
            "residual_voltage_kv": 134.0,
            "standard": "GB/T 11032-2020",
            "source_note": "HY10WZ-51/134型35kV系统复合外套无间隙金属氧化物避雷器(10kA级)"
        },
    }

    arrester_lv = {
        "HY1.5W-0.28/1.3": {
            "rated_voltage_kv": 0.28,
            "continuous_operating_voltage_kv": 0.25,
            "nominal_discharge_current_ka": 1.5,
            "residual_voltage_kv": 1.3,
            "standard": "GB/T 11032-2020",
            "source_note": "HY1.5W-0.28/1.3型0.4kV系统复合外套无间隙金属氧化物避雷器"
        },
    }

    return {
        "arrester_mv": arrester_mv,
        "arrester_lv": arrester_lv,
    }
