def get_all_wind_turbines():
    return {
        "small_wind": {
            "SW-10kW": {
                "rated_power_kw": 10,
                "rated_wind_speed_ms": 9,
                "cut_in_wind_speed_ms": 3,
                "cut_out_wind_speed_ms": 25,
                "rated_voltage_v": 380,
                "power_factor": 0.95,
                "efficiency_percent": 22,
                "rotor_diameter_m": 7,
                "generator_type": "PMSG",
                "standard": "GB/T 19068-2017",
                "source_note": "参数依据GB/T 19068-2017及主流厂家产品手册"
            },
            "SW-20kW": {
                "rated_power_kw": 20,
                "rated_wind_speed_ms": 9,
                "cut_in_wind_speed_ms": 3,
                "cut_out_wind_speed_ms": 25,
                "rated_voltage_v": 380,
                "power_factor": 0.95,
                "efficiency_percent": 24,
                "rotor_diameter_m": 10,
                "generator_type": "PMSG",
                "standard": "GB/T 19068-2017",
                "source_note": "参数依据GB/T 19068-2017及主流厂家产品手册"
            },
            "SW-30kW": {
                "rated_power_kw": 30,
                "rated_wind_speed_ms": 10,
                "cut_in_wind_speed_ms": 3,
                "cut_out_wind_speed_ms": 25,
                "rated_voltage_v": 380,
                "power_factor": 0.95,
                "efficiency_percent": 26,
                "rotor_diameter_m": 12,
                "generator_type": "PMSG",
                "standard": "GB/T 19068-2017",
                "source_note": "参数依据GB/T 19068-2017及主流厂家产品手册"
            },
            "SW-50kW": {
                "rated_power_kw": 50,
                "rated_wind_speed_ms": 10,
                "cut_in_wind_speed_ms": 3,
                "cut_out_wind_speed_ms": 25,
                "rated_voltage_v": 400,
                "power_factor": 0.95,
                "efficiency_percent": 28,
                "rotor_diameter_m": 16,
                "generator_type": "PMSG",
                "standard": "GB/T 19068-2017",
                "source_note": "参数依据GB/T 19068-2017及主流厂家产品手册"
            },
            "SW-100kW": {
                "rated_power_kw": 100,
                "rated_wind_speed_ms": 10,
                "cut_in_wind_speed_ms": 3,
                "cut_out_wind_speed_ms": 25,
                "rated_voltage_v": 400,
                "power_factor": 0.95,
                "efficiency_percent": 30,
                "rotor_diameter_m": 21,
                "generator_type": "PMSG",
                "standard": "GB/T 19068-2017",
                "source_note": "参数依据GB/T 19069-2003及主流厂家产品手册"
            }
        },
        "medium_wind": {
            "MW-100kW": {
                "rated_power_kw": 100,
                "rated_wind_speed_ms": 11,
                "cut_in_wind_speed_ms": 3,
                "cut_out_wind_speed_ms": 25,
                "rated_voltage_v": 690,
                "power_factor": 0.95,
                "efficiency_percent": 30,
                "rotor_diameter_m": 22,
                "generator_type": "PMSG",
                "standard": "GB/T 25383-2017",
                "source_note": "参数依据GB/T 25383-2017及主流厂家产品手册"
            },
            "MW-200kW": {
                "rated_power_kw": 200,
                "rated_wind_speed_ms": 11,
                "cut_in_wind_speed_ms": 3,
                "cut_out_wind_speed_ms": 25,
                "rated_voltage_v": 690,
                "power_factor": 0.95,
                "efficiency_percent": 32,
                "rotor_diameter_m": 30,
                "generator_type": "PMSG",
                "standard": "GB/T 25383-2017",
                "source_note": "参数依据GB/T 25383-2017及主流厂家产品手册"
            },
            "MW-300kW": {
                "rated_power_kw": 300,
                "rated_wind_speed_ms": 11,
                "cut_in_wind_speed_ms": 3,
                "cut_out_wind_speed_ms": 25,
                "rated_voltage_v": 690,
                "power_factor": 0.95,
                "efficiency_percent": 33,
                "rotor_diameter_m": 35,
                "generator_type": "PMSG",
                "standard": "GB/T 25383-2017",
                "source_note": "参数依据GB/T 25383-2017及主流厂家产品手册"
            },
            "MW-500kW": {
                "rated_power_kw": 500,
                "rated_wind_speed_ms": 12,
                "cut_in_wind_speed_ms": 3,
                "cut_out_wind_speed_ms": 25,
                "rated_voltage_v": 690,
                "power_factor": 0.95,
                "efficiency_percent": 34,
                "rotor_diameter_m": 40,
                "generator_type": "PMSG",
                "standard": "GB/T 25383-2017",
                "source_note": "参数依据GB/T 25383-2017及主流厂家产品手册"
            }
        }
    }
