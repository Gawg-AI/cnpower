def get_all_ev_chargers():
    return {
        "ac_slow": {
            "AC-7kW": {
                "rated_power_kw": 7,
                "rated_voltage_v": 220,
                "rated_current_a": 32,
                "charging_mode": "AC_Mode2",
                "communication_protocol": "GB/T 27930-2015",
                "efficiency_percent": 90,
                "power_factor": 0.95,
                "harmonic_current_limit_percent": 5,
                "protection_class": "IP54",
                "standard": "GB/T 18487.1-2023",
                "source_note": "参数依据GB/T 18487.1-2023及主流厂家产品手册"
            },
            "AC-14kW": {
                "rated_power_kw": 14,
                "rated_voltage_v": 380,
                "rated_current_a": 22,
                "charging_mode": "AC_Mode3",
                "communication_protocol": "GB/T 27930-2015",
                "efficiency_percent": 90,
                "power_factor": 0.95,
                "harmonic_current_limit_percent": 5,
                "protection_class": "IP54",
                "standard": "GB/T 18487.1-2023",
                "source_note": "参数依据GB/T 18487.1-2023及主流厂家产品手册"
            },
            "AC-21kW": {
                "rated_power_kw": 21,
                "rated_voltage_v": 380,
                "rated_current_a": 32,
                "charging_mode": "AC_Mode3",
                "communication_protocol": "GB/T 27930-2015",
                "efficiency_percent": 90,
                "power_factor": 0.95,
                "harmonic_current_limit_percent": 5,
                "protection_class": "IP54",
                "standard": "GB/T 18487.1-2023",
                "source_note": "参数依据GB/T 18487.1-2023及主流厂家产品手册"
            }
        },
        "dc_fast": {
            "DC-30kW": {
                "rated_power_kw": 30,
                "rated_voltage_v": "200~1000DC",
                "rated_current_a": 75,
                "charging_mode": "DC_Mode4",
                "communication_protocol": "GB/T 27930-2015",
                "efficiency_percent": 94,
                "power_factor": 0.99,
                "harmonic_current_limit_percent": 3,
                "protection_class": "IP54",
                "standard": "GB/T 18487.1-2023",
                "source_note": "参数依据GB/T 18487.1-2023及主流厂家产品手册"
            },
            "DC-60kW": {
                "rated_power_kw": 60,
                "rated_voltage_v": "200~1000DC",
                "rated_current_a": 150,
                "charging_mode": "DC_Mode4",
                "communication_protocol": "GB/T 27930-2015",
                "efficiency_percent": 94,
                "power_factor": 0.99,
                "harmonic_current_limit_percent": 3,
                "protection_class": "IP54",
                "standard": "GB/T 18487.1-2023",
                "source_note": "参数依据GB/T 18487.1-2023及主流厂家产品手册"
            },
            "DC-120kW": {
                "rated_power_kw": 120,
                "rated_voltage_v": "200~1000DC",
                "rated_current_a": 250,
                "charging_mode": "DC_Mode4",
                "communication_protocol": "GB/T 27930-2015",
                "efficiency_percent": 94,
                "power_factor": 0.99,
                "harmonic_current_limit_percent": 3,
                "protection_class": "IP54",
                "standard": "GB/T 18487.1-2023",
                "source_note": "参数依据GB/T 18487.1-2023及主流厂家产品手册"
            },
            "DC-240kW": {
                "rated_power_kw": 240,
                "rated_voltage_v": "200~1000DC",
                "rated_current_a": 500,
                "charging_mode": "DC_Mode4",
                "communication_protocol": "GB/T 27930-2015",
                "efficiency_percent": 94,
                "power_factor": 0.99,
                "harmonic_current_limit_percent": 3,
                "protection_class": "IP54",
                "standard": "GB/T 18487.1-2023",
                "source_note": "参数依据GB/T 18487.1-2023及主流厂家产品手册"
            }
        },
        "dc_superfast": {
            "DC-480kW": {
                "rated_power_kw": 480,
                "rated_voltage_v": "200~1000DC",
                "rated_current_a": 600,
                "charging_mode": "DC_Mode4",
                "communication_protocol": "GB/T 27930-2015",
                "efficiency_percent": 95,
                "power_factor": 0.99,
                "harmonic_current_limit_percent": 3,
                "protection_class": "IP55",
                "liquid_cooled": True,
                "standard": "GB/T 18487.1-2023",
                "source_note": "参数依据GB/T 18487.1-2023及主流厂家产品手册"
            },
            "DC-600kW": {
                "rated_power_kw": 600,
                "rated_voltage_v": "200~1000DC",
                "rated_current_a": 750,
                "charging_mode": "DC_Mode4",
                "communication_protocol": "GB/T 27930-2015",
                "efficiency_percent": 95,
                "power_factor": 0.99,
                "harmonic_current_limit_percent": 3,
                "protection_class": "IP55",
                "liquid_cooled": True,
                "standard": "GB/T 18487.1-2023",
                "source_note": "参数依据GB/T 18487.1-2023及主流厂家产品手册"
            }
        }
    }
