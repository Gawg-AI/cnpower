from functools import lru_cache


def _enhance_protection_entry(name, entry):
    if not isinstance(entry, dict):
        return entry
    entry.setdefault("field_source_types", {
        "setting_parameter": "engineering_policy",
        "coordination_notes": "engineering_practice",
        "standard": "standard_reference",
    })
    if "setting_parameter" in entry:
        entry.setdefault("setting_metadata", {
            "requires_fault_study": True,
            "requires_load_current": True,
            "requires_downstream_coordination": True,
            "coordination_margin_s": 0.3,
        })
    if "fuse" in name or "熔断" in str(entry.get("protection_scheme", "")):
        values = entry.get("setting_formulas_or_values", {})
        entry.setdefault("standard", "DL/T 584-2021 / GB/T 15166.6-2023")
        entry.setdefault("fuse_coordination", {
            "standard": "GB/T 15166.6-2023",
            "rated_current_formula": values.get("rated_current_formula", "In = Sn/(sqrt(3)*Un)"),
            "fuse_element_current_formula": values.get("fuse_element_current_formula", "1.5~2.0 * In"),
            "coordination_margin_s": 0.3,
            "maximum_clearing_time_s_at_short_circuit": 0.1,
            "source_type": "standard_reference_and_engineering_default",
        })
    if "temperature" in name or "温度" in str(entry.get("protection_scheme", "")):
        entry.setdefault("standard", "GB/T 6451-2023 / GB/T 1094.7-2024 / GB/T 1094.12-2013")
        entry.setdefault("thermal_trip_model", {
            "oil_loading_guide": "GB/T 1094.7-2024",
            "dry_loading_guide": "GB/T 1094.12-2013",
            "requires_hot_spot_or_winding_temperature": True,
            "source_type": "standard_reference",
        })
    return entry


def _enhance_all_protection(data):
    for group in data.values():
        for name, entry in group.items():
            _enhance_protection_entry(name, entry)
    return data


@lru_cache(maxsize=1)
def get_all_protection():
    return _enhance_all_protection({
        "line_protection_mv": {
            "overcurrent_protection": {
                "protection_type": "定时限过电流保护",
                "setting_parameter": {
                    "current_setting_range_a": (0.1, 20),
                    "time_setting_range_s": (0.1, 10),
                },
                "sensitivity_coefficient": 1.5,
                "coordination_notes": "与下游分支线保护配合，级差时间不小于0.3s；动作电流按最大负荷电流的1.3~1.5倍整定",
                "standard": "DL/T 584",
                "source_note": "DL/T 584-2021《3kV~110kV电网继电保护装置运行整定规程》",
            },
            "instantaneous_overcurrent": {
                "protection_type": "瞬时过电流保护",
                "setting_parameter": {
                    "current_setting_range_a": (1, 40),
                    "time_setting_s": (0.0, 0.1),
                },
                "sensitivity_coefficient": 2.0,
                "coordination_notes": "动作电流按躲过线路末端最大短路电流整定，保护范围不小于线路全长的15%~20%；不与下游保护配合",
                "standard": "DL/T 584",
                "source_note": "DL/T 584-2021《3kV~110kV电网继电保护装置运行整定规程》",
            },
            "zero_sequence_overcurrent": {
                "protection_type": "零序过电流保护",
                "setting_parameter": {
                    "current_setting_range_a": (0.01, 5),
                    "time_setting_range_s": (0.1, 10),
                },
                "sensitivity_coefficient": 1.5,
                "coordination_notes": "用于中性点非有效接地系统的单相接地故障检测；小电流接地系统零序电流整定应躲过本线路电容电流，一般取0.05~0.1A；经消弧线圈接地系统应采用方向性零序保护",
                "standard": "DL/T 584",
                "source_note": "DL/T 584-2021《3kV~110kV电网继电保护装置运行整定规程》",
            },
            "auto_reclosing": {
                "protection_type": "自动重合闸",
                "setting_parameter": {
                    "reclose_count": (1, 3),
                    "dead_time_range_s": (0.3, 5),
                    "reclaim_time_s": (10, 180),
                },
                "sensitivity_coefficient": None,
                "coordination_notes": "架空线路宜采用三相一次重合闸；电缆线路不宜装设重合闸；架空电缆混合线路根据架空线比例确定；重合闸时间应大于故障点去游离时间，一般取0.5~1.0s",
                "standard": "DL/T 584",
                "source_note": "DL/T 584-2021《3kV~110kV电网继电保护装置运行整定规程》",
            },
            "overvoltage_protection": {
                "protection_type": "过电压保护",
                "setting_parameter": {
                    "voltage_setting_range_percent_rated": (100, 130),
                    "time_setting_range_s": (0.1, 10),
                },
                "sensitivity_coefficient": None,
                "coordination_notes": "电压整定值以额定电压百分数表示；一般整定为110%~120%Un，延时2~5s发信号；与电容器过电压保护配合",
                "standard": "DL/T 584",
                "source_note": "DL/T 584-2021《3kV~110kV电网继电保护装置运行整定规程》",
            },
            "undervoltage_protection": {
                "protection_type": "低电压保护",
                "setting_parameter": {
                    "voltage_setting_range_percent_rated": (50, 90),
                    "time_setting_range_s": (0.1, 10),
                },
                "sensitivity_coefficient": None,
                "coordination_notes": "一般整定为60%~70%Un，延时0.5~2s；应防止因PT断线或系统振荡引起误动；需与过电流保护配合构成复合电压闭锁过电流保护",
                "standard": "DL/T 584",
                "source_note": "DL/T 584-2021《3kV~110kV电网继电保护装置运行整定规程》",
            },
        },
        "transformer_protection": {
            "fuse_protection_small": {
                "protection_scheme": "熔断器保护",
                "applicable_range": {
                    "applicable_range_kva": (30, 400),
                    "voltage_level_kv": 10,
                },
                "setting_formulas_or_values": {
                    "fuse_type": "XRNT-12",
                    "fuse_element_current_formula": "1.5~2.0 * In",
                    "fuse_element_current_table": {
                        30: 6.3,
                        50: 10,
                        80: 16,
                        100: 20,
                        160: 31.5,
                        200: 40,
                        250: 50,
                        315: 63,
                        400: 80,
                    },
                    "rated_current_formula": "In = Sn / (√3 * Un)",
                },
                "sensitivity_requirements": "熔断器额定电流应大于变压器最大负荷电流的1.5~2.0倍，且应躲过变压器励磁涌流；熔断时间特性应与低压侧保护选择性配合，允许短路电流下熔断时间不超过0.1s",
                "coordination_notes": "高压熔断器与低压侧断路器保护配合，熔断器安秒特性曲线应位于低压保护曲线之上，确保低压侧故障由低压保护切除；熔断器最小熔断电流应大于变压器满载电流的1.5倍",
                "standard": "DL/T 584",
                "source_note": "DL/T 584-2021《3kV~110kV电网继电保护装置运行整定规程》及GB/T 15166.2-2023《高压交流熔断器》",
            },
            "breaker_protection_large": {
                "protection_scheme": "断路器保护",
                "applicable_range": {
                    "applicable_range_kva": (500, 2500),
                    "voltage_level_kv": 10,
                },
                "setting_formulas_or_values": {
                    "protection_list": ["overcurrent", "instantaneous", "overload", "temperature"],
                    "current_setting_formulas": {
                        "overcurrent": {
                            "formula": "Idz = Kk * Kfh * In / Kf",
                            "typical_multiplier": "1.3~1.5 * In",
                            "time_delay_s": (0.5, 1.5),
                            "description": "可靠系数Kk取1.2~1.3，返回系数Kf取0.85~0.95",
                        },
                        "instantaneous": {
                            "formula": "Idz = Kk * In",
                            "typical_multiplier": "8~15 * In",
                            "time_delay_s": (0.0, 0.06),
                            "description": "应躲过变压器励磁涌流，可靠系数Kk取8~15；二次谐波制动比一般取15%~20%",
                        },
                        "overload": {
                            "formula": "Idz = Kk * In / Kf",
                            "typical_multiplier": "1.05~1.1 * In",
                            "time_delay_s": (5, 30),
                            "description": "可靠系数Kk取1.05，返回系数Kf取0.85~0.95；动作于信号",
                        },
                        "temperature": {
                            "description": "由温度继电器直接动作，不通过电流整定",
                            "alarm_threshold_celsius": 80,
                            "trip_threshold_celsius": 95,
                        },
                    },
                    "rated_current_formula": "In = Sn / (√3 * Un)",
                },
                "sensitivity_requirements": "过电流保护灵敏系数不小于1.5；瞬时保护灵敏系数不小于2.0；过负荷保护仅动作于信号",
                "coordination_notes": "过电流保护与下游馈线保护配合，级差时间不小于0.3s；瞬时保护不与下游保护配合，应躲过变压器励磁涌流及低压侧电动机自启动电流；过负荷保护动作于信号，不跳闸",
                "standard": "DL/T 584",
                "source_note": "DL/T 584-2021《3kV~110kV电网继电保护装置运行整定规程》",
            },
            "temperature_protection": {
                "protection_scheme": "温度保护",
                "applicable_range": {
                    "oil_immersed": "所有油浸式变压器",
                    "dry_type": "所有干式变压器",
                },
                "setting_formulas_or_values": {
                    "oil_immersed": {
                        "alarm_threshold_celsius": 80,
                        "trip_threshold_celsius": 95,
                        "top_oil_temperature_limit_celsius": 105,
                        "winding_hotspot_limit_celsius": 115,
                    },
                    "dry_type": {
                        "alarm_threshold_celsius": 100,
                        "trip_threshold_celsius": 130,
                        "insulation_class": "F级(155°C)",
                        "reference_standard": "GB/T 17211",
                    },
                },
                "sensitivity_requirements": "温度保护动作值应根据变压器绝缘等级和冷却方式确定；油浸式变压器顶层油温报警值不超过80°C，跳闸值不超过95°C；干式变压器绕组温度报警值不超过100°C，跳闸值不超过130°C",
                "coordination_notes": "温度报警应先于温度跳闸动作；温度保护应与过负荷保护配合，过负荷时先发信号，温度升高至报警值再发报警，达到跳闸值时跳闸；温度传感器应安装在绕组最热点位置",
                "standard": "GB/T 6451",
                "source_note": "GB/T 6451-2023《油浸式电力变压器技术参数和要求》及GB/T 17211-1998《干式电力变压器负载导则》",
            },
            "gas_protection": {
                "protection_scheme": "瓦斯保护",
                "applicable_range": {
                    "applicable_range_kva": (800, float("inf")),
                    "voltage_level_kv": 10,
                    "note": "800kVA及以上油浸式变压器应装设瓦斯保护",
                },
                "setting_formulas_or_values": {
                    "light_gas": {
                        "action": "报警",
                        "setting_description": "轻瓦斯动作容积250~300mL",
                        "gas_volume_threshold_ml": (250, 300),
                    },
                    "heavy_gas": {
                        "action": "跳闸",
                        "setting_description": "重瓦斯动作油流速0.6~1.2m/s（管径80mm）或0.8~1.4m/s（管径50mm）",
                        "oil_flow_velocity_m_per_s": {
                            "pipe_diameter_80mm": (0.6, 1.2),
                            "pipe_diameter_50mm": (0.8, 1.4),
                        },
                    },
                },
                "sensitivity_requirements": "轻瓦斯应能可靠检测变压器内部轻微故障产生的气体；重瓦斯应能可靠检测变压器内部严重故障产生的油流冲击；瓦斯继电器安装坡度应为1%~1.5%",
                "coordination_notes": "瓦斯保护与差动保护共同构成变压器主保护；轻瓦斯动作于信号，重瓦斯动作于跳闸；变压器注油或滤油后应将重瓦斯改接信号，待气体排尽后方可投入跳闸；瓦斯保护应在变压器带电前投入",
                "standard": "GB/T 6451",
                "source_note": "GB/T 6451-2023《油浸式电力变压器技术参数和要求》及GB/T 50062-2008《电力装置的继电保护和自动装置设计规范》",
            },
        },
    })
