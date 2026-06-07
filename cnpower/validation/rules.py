def get_all_validation_rules():
    return {
        "voltage_quality": {
            "voltage_deviation": {
                "name": "电压偏差",
                "standard": "GB/T 12325-2008",
                "description": "用电单位端电压偏离额定电压的百分数不得超过规定限值",
                "limits": {
                    "110kV": "±5%",
                    "35kV": "±5%",
                    "10kV": "±7%",
                    "0.4kV_3phase": "±7%",
                    "0.4kV_1phase": "+7%/-10%"
                },
                "check_formula": "(V_actual - V_rated) / V_rated * 100",
                "applicable_condition": "电力系统正常运行时，用户受电端电压偏差",
                "pass_criteria": "电压偏差百分数在标准规定限值范围内"
            },
            "voltage_fluctuation_flicker": {
                "name": "电压波动和闪变",
                "standard": "GB/T 12326-2008",
                "description": "电压波动和闪变不得超过规定限值，保证用电质量",
                "limits": {
                    "voltage_fluctuation": {
                        "LV": "≤4%",
                        "MV": "≤3%",
                        "HV": "≤2%"
                    },
                    "flicker_plt": {
                        "LV": "≤1.0",
                        "MV": "≤1.0",
                        "HV": "≤0.8"
                    }
                },
                "check_formula": "dU/U * 100, Plt = sqrt(sum(Pst_i^3) / N)^(1/3)",
                "applicable_condition": "波动负荷接入点及其他用户受电端",
                "pass_criteria": "电压波动值和闪变值均在标准规定限值范围内"
            },
            "three_phase_unbalance": {
                "name": "三相电压不平衡",
                "standard": "GB/T 15543-2008",
                "description": "三相电压不平衡度不得超过规定限值",
                "limits": {
                    "normal": "≤2%",
                    "short_time": "≤4%"
                },
                "check_formula": "ε = (V_max - V_min) / V_avg * 100",
                "applicable_condition": "电力系统正常运行时的三相电压不平衡度",
                "pass_criteria": "正常运行时不平衡度≤2%，短时≤4%"
            },
            "harmonic": {
                "name": "谐波",
                "standard": "GB/T 14549-1993",
                "description": "公用电网谐波电压含有率和总谐波畸变率不得超过规定限值",
                "limits_by_voltage_level": {
                    "0.4kV": {
                        "THD_limit": "5.0%",
                        "individual_harmonic_limits": {
                            "3rd": "4.0%",
                            "5th": "4.0%",
                            "7th": "3.0%",
                            "11th": "2.0%",
                            "13th": "1.5%"
                        }
                    },
                    "10kV": {
                        "THD_limit": "4.0%",
                        "individual_harmonic_limits": {
                            "3rd": "3.2%",
                            "5th": "3.2%",
                            "7th": "2.4%",
                            "11th": "1.6%",
                            "13th": "1.2%"
                        }
                    }
                },
                "check_formula": "THD = sqrt(sum(V_h^2 for h>=2)) / V_1 * 100",
                "applicable_condition": "公用电网谐波电压监测",
                "pass_criteria": "THD及各次谐波含有率均在标准规定限值范围内"
            }
        },
        "n1_safety": {
            "name": "N-1安全准则",
            "standard": "DL/T 5729-2023",
            "description": "任一元件发生故障时，系统应能通过负荷转移保证用户供电不中断或快速恢复",
            "rules_by_area_class": {
                "A": {"n1_pass_rate": "100%", "description": "A类供电区，任一元件故障时不允许中断供电"},
                "B": {"n1_pass_rate": "100%", "description": "B类供电区，任一元件故障时不允许中断供电"},
                "C": {"n1_pass_rate": "≥90%", "description": "C类供电区，N-1通过率不低于90%"},
                "D": {"n1_pass_rate": "计划检修可行", "description": "D类供电区，计划检修时不中断供电即可"},
                "E": {"n1_pass_rate": "不强制", "description": "E类供电区以辐射接线和快速抢修为主，N-1不作强制要求"}
            },
            "check_method": "逐一断开网络中每个元件（线路、变压器、开关等），检验剩余网络是否能通过联络开关转移全部负荷",
            "pass_criteria": "断开任一元件后，剩余网络能转移全部负荷，不出现过载或电压越限"
        },
        "connection_modes": {
            "name": "典型接线模式匹配",
            "standard": "Q/GDW 10370-2023 / DL/T 5729-2023",
            "description": "按供电区域、负荷水平、供电半径和可靠性要求选择单联络、环网、双环网等典型接线模式",
            "check_method": "将供电区类别、负荷规模、供电半径和联络点数量与 topology.connection_modes 参数库比对",
            "pass_criteria": "所选接线模式适用供电区类别且满足供电半径、负荷规模和可靠性要求"
        },
        "short_circuit": {
            "name": "短路电流校验",
            "standard": "GB/T 15544-2023",
            "description": "配电网短路电流计算及设备校验",
            "three_phase_max": {
                "name": "三相最大短路电流",
                "check_formula": "I_sc3max = U_rated / (sqrt(3) * Z_total)",
                "purpose": "校验断路器开断能力和设备动热稳定性",
                "pass_criteria": "断路器额定开断电流 ≥ I_sc3max"
            },
            "single_phase_min": {
                "name": "单相最小短路电流",
                "check_formula": "I_sc1min = U_phase / (Z1 + Z2 + Z0 + 3*Z_n)",
                "purpose": "校验保护灵敏度，保证保护可靠动作",
                "pass_criteria": "I_sc1min ≥ 保护整定值×1.5（变压器保护）或 1.2（线路保护）"
            },
            "cable_thermal_stability": {
                "name": "电缆热稳定校验",
                "check_formula": "S_min = I_sc * sqrt(t) / C",
                "purpose": "校验电缆截面积是否满足短路电流热稳定要求",
                "parameters": {
                    "S_min": "最小允许截面积(mm²)",
                    "I_sc": "短路电流(A)",
                    "t": "短路持续时间(s)",
                    "C": "热稳定系数(铜芯电缆取142, 铝芯电缆取87)"
                },
                "pass_criteria": "电缆实际截面积 ≥ S_min"
            }
        },
        "equipment_selection": {
            "name": "设备选型校验",
            "standard": "GB 50052-2009",
            "description": "配电网主要设备选型校验规则",
            "transformer_loading": {
                "name": "变压器负荷率",
                "limit": "≤80%~90%",
                "check_formula": "β = S_load / S_rated * 100",
                "pass_criteria": "正常运行时变压器负荷率不超过80%~90%，N-1时允许短时过载"
            },
            "transformer_dynamic_loading": {
                "name": "变压器动态负载",
                "check_formula": "hot_spot_temperature, top_oil_temperature, aging_rate",
                "pass_criteria": "动态负载下热点温度、顶层油温和相对老化率不超过标准或厂家限值"
            },
            "transformer_life_loss": {
                "name": "变压器寿命损失",
                "check_formula": "loss_of_life = sum(relative_aging_rate * duration)",
                "pass_criteria": "累计寿命损失不超过规划寿命或运行策略限值"
            },
            "transformer_temperature": {
                "name": "变压器温升",
                "check_formula": "winding_temperature, hot_spot_temperature",
                "pass_criteria": "绕组温升、热点温度和冷却方式满足对应标准要求"
            },
            "transformer_selection": {
                "name": "变压器选型",
                "check_formula": "voltage_level, capacity, vector_group, impedance",
                "pass_criteria": "电压等级、容量、联结组别、阻抗和调压范围满足接入和运行要求"
            },
            "transformer_economy": {
                "name": "变压器经济性",
                "check_formula": "no_load_loss + load_loss * load_factor^2",
                "pass_criteria": "能效等级、空载损耗、负载损耗和经济负载率满足规划口径"
            },
            "conductor_economy": {
                "name": "导体经济截面积",
                "check_formula": "S = I_max / J_ec",
                "economic_current_density_table": {
                    "铜芯电缆": {
                        "T_max_3000h": {"J_ec": "2.25 A/mm²"},
                        "T_max_3000_5000h": {"J_ec": "1.75 A/mm²"},
                        "T_max_5000h": {"J_ec": "1.25 A/mm²"}
                    },
                    "铝芯电缆": {
                        "T_max_3000h": {"J_ec": "1.53 A/mm²"},
                        "T_max_3000_5000h": {"J_ec": "1.18 A/mm²"},
                        "T_max_5000h": {"J_ec": "0.85 A/mm²"}
                    },
                    "架空裸导线(LJ)": {
                        "T_max_3000h": {"J_ec": "1.65 A/mm²"},
                        "T_max_3000_5000h": {"J_ec": "1.15 A/mm²"},
                        "T_max_5000h": {"J_ec": "0.90 A/mm²"}
                    },
                    "架空钢芯铝线(LGJ)": {
                        "T_max_3000h": {"J_ec": "1.85 A/mm²"},
                        "T_max_3000_5000h": {"J_ec": "1.35 A/mm²"},
                        "T_max_5000h": {"J_ec": "1.05 A/mm²"}
                    }
                },
                "pass_criteria": "导体截面积≥经济截面积，且满足载流和热稳定要求"
            },
            "conductor_ampacity": {
                "name": "导体载流校验",
                "check_formula": "I_max ≤ I_allowable(T_ambient, laying_method)",
                "pass_criteria": "导体最大工作电流不超过允许载流量"
            },
            "conductor_voltage_drop": {
                "name": "导体电压降校验",
                "check_formula": "ΔU% = (P*R + Q*X) / (10*U_rated^2) * 100",
                "limits": {
                    "10kV": "≤5%",
                    "0.4kV": "≤4%"
                },
                "pass_criteria": "线路末端电压降在允许范围内"
            },
            "breaker_rating": {
                "name": "断路器额定值校验",
                "check_formula": "I_breaker_rated ≥ I_max_working, I_breaker_breaking ≥ I_sc_max",
                "pass_criteria": "断路器额定电流≥最大工作电流，额定开断电流≥最大短路电流"
            }
        },
        "reliability": {
            "name": "供电可靠性指标",
            "standard": "DL/T 5729-2023",
            "description": "配电网供电可靠性目标指标",
            "saidi_target": {
                "name": "系统平均停电时间指标(SAIDI)",
                "by_area_class": {
                    "A": "≤5min/户·年",
                    "B": "≤15min/户·年",
                    "C": "≤60min/户·年",
                    "D": "≤120min/户·年",
                    "E": "≤240min/户·年"
                }
            },
            "saifi_target": {
                "name": "系统平均停电频率指标(SAIFI)",
                "by_area_class": {
                    "A": "≤0.5次/户·年",
                    "B": "≤1.0次/户·年",
                    "C": "≤3.0次/户·年",
                    "D": "≤5.0次/户·年",
                    "E": "≤8.0次/户·年"
                }
            }
        },
        "renewable_connection": {
            "name": "分布式电源接入校验",
            "standard": "NB/T 10994-2022",
            "description": "分布式光伏等新能源接入配电网的校验规则",
            "pv_penetration_limit": {
                "name": "光伏渗透率限制",
                "limit": {
                    "380V": "≤30%变压器容量",
                    "10kV": "≤80%变压器容量"
                },
                "description": "接入变压器的光伏容量占变压器额定容量的比例"
            },
            "voltage_rise_check": {
                "name": "电压升高校验",
                "limit": "≤+5%在PCC点",
                "check_formula": "ΔU% = (P*R - Q*X) / (10*U_rated^2) * 100",
                "pass_criteria": "PCC点电压升高不超过5%"
            },
            "reverse_power_flow": {
                "name": "反向潮流校验",
                "check_condition": "光伏最大出力时变压器低压侧是否存在反向潮流",
                "pass_criteria": "A/B类供电区不允许反向潮流，C/D类可限量允许"
            },
            "power_quality": {
                "name": "电能质量校验",
                "reference": "谐波规则参见电压质量校验中的谐波规则",
                "description": "光伏接入后谐波电流含有率应满足GB/T 14549要求"
            },
            "energy_storage_safety": {
                "name": "储能系统安全校验",
                "reference": "GB/T 36558-2018",
                "description": "储能系统应具备电池管理、绝缘监测、过充过放、过温和消防联动等安全保护",
                "pass_criteria": "安全保护配置完整，运行边界和故障隔离策略满足储能系统通用技术条件"
            },
            "storage_grid_connection": {
                "name": "储能并网接入校验",
                "reference": "GB/T 34131-2023",
                "description": "电化学储能站接入电网时应校核功率控制、无功支撑、电压适应性和并离网保护",
                "pass_criteria": "储能站有功/无功控制、保护配置、电压频率适应性和电能质量满足并网要求"
            },
            "ev_charger_power_quality": {
                "name": "充电设施电能质量校验",
                "reference": "GB/T 18487.1-2023 / GB/T 14549-1993",
                "description": "电动车导电充电设施接入后应满足功率因数、谐波和负荷接入要求",
                "pass_criteria": "功率因数、谐波电流、接地和保护配置满足充电系统通用要求"
            }
        }
    }
