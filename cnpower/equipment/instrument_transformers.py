def get_all_instrument_transformers():
    ct_mv_specs = [
        (30, 5, "0.5", 10, 7.5, 3.0),
        (50, 5, "0.5", 10, 12.5, 5.0),
        (75, 5, "0.5", 10, 18.75, 7.5),
        (100, 5, "0.5S", 10, 25.0, 10.0),
        (150, 5, "0.5S", 15, 22.5, 9.0),
        (200, 5, "0.5S", 15, 30.0, 12.0),
        (300, 5, "0.5S", 15, 45.0, 18.0),
        (400, 5, "0.2", 20, 60.0, 24.0),
        (500, 5, "0.2", 20, 75.0, 30.0),
        (600, 5, "0.2", 20, 75.0, 30.0),
        (800, 5, "0.2", 30, 80.0, 40.0),
        (1000, 5, "0.2", 30, 80.0, 40.0),
        (1200, 5, "0.2", 30, 80.0, 40.0),
        (1500, 5, "0.2", 40, 80.0, 40.0),
        (2000, 5, "0.2", 40, 100.0, 50.0),
    ]
    ct_mv = {}
    for pri_a, sec_a, acc, burden_va, dyn_ka, therm_ka in ct_mv_specs:
        key = f"LZZBJ9-10/{pri_a}A"
        ct_mv[key] = {
            "rated_voltage_kv": 10,
            "rated_primary_a": pri_a,
            "rated_secondary_a": sec_a,
            "accuracy_class": acc,
            "rated_secondary_burden_va": burden_va,
            "dynamic_current_ka": dyn_ka,
            "thermal_current_ka_1s": therm_ka,
            "standard": "GB/T 20840.2-2014",
            "source_note": "LZZBJ9-10系列10kV电流互感器典型参数"
        }

    ct_lv_specs = [
        (50, 5, "0.5", 5),
        (75, 5, "0.5", 5),
        (100, 5, "0.5", 5),
        (150, 5, "0.5", 5),
        (200, 5, "0.5", 5),
        (250, 5, "0.5", 5),
        (300, 5, "0.5S", 10),
        (400, 5, "0.5S", 10),
        (500, 5, "0.5S", 10),
        (600, 5, "0.5S", 10),
        (800, 5, "0.5S", 10),
        (1000, 5, "0.5S", 10),
        (1500, 5, "0.5S", 10),
    ]
    ct_lv = {}
    for pri_a, sec_a, acc, burden_va in ct_lv_specs:
        key = f"BH-LMZ/{pri_a}A"
        ct_lv[key] = {
            "rated_voltage_kv": 0.4,
            "rated_primary_a": pri_a,
            "rated_secondary_a": sec_a,
            "accuracy_class": acc,
            "rated_secondary_burden_va": burden_va,
            "standard": "GB/T 20840.2-2014",
            "source_note": "BH/LMZ系列0.4kV电流互感器典型参数"
        }

    pt_mv = {
        "JDZ-10/0.5": {
            "rated_voltage_ratio": "10/0.1",
            "accuracy_class": "0.5",
            "rated_secondary_burden_va": 80,
            "standard": "GB/T 20840.3-2013",
            "source_note": "JDZ-10型10kV双绕组电压互感器(全绝缘,V/V接线)"
        },
        "JDZ-10/0.2": {
            "rated_voltage_ratio": "10/0.1",
            "accuracy_class": "0.2",
            "rated_secondary_burden_va": 50,
            "standard": "GB/T 20840.3-2013",
            "source_note": "JDZ-10型10kV双绕组电压互感器(全绝缘,V/V接线)"
        },
        "JDZJ-10/0.5": {
            "rated_voltage_ratio": "10/\u221a3:0.1/\u221a3",
            "accuracy_class": "0.5",
            "rated_secondary_burden_va": 60,
            "standard": "GB/T 20840.3-2013",
            "source_note": "JDZJ-10型10kV电压互感器(半绝缘,Y/Y接线)"
        },
        "JDZJ-10/0.2": {
            "rated_voltage_ratio": "10/\u221a3:0.1/\u221a3",
            "accuracy_class": "0.2",
            "rated_secondary_burden_va": 40,
            "standard": "GB/T 20840.3-2013",
            "source_note": "JDZJ-10型10kV电压互感器(半绝缘,Y/Y接线)"
        },
    }

    return {
        "ct_mv": ct_mv,
        "ct_lv": ct_lv,
        "pt_mv": pt_mv,
    }
