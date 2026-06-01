def get_all_connection_modes():
    return {
        "mv_10kv_overhead": {
            "radial_single": {
                "name": "单回辐射",
                "description": "单回线路辐射式供电，无联络开关，结构简单，投资少，但供电可靠性低",
                "applicable_area_class": ["C", "D", "E"],
                "max_supply_radius_km": {"C": 10, "D": 15, "E": 15},
                "max_load_mw": {"min": 2, "max": 4},
                "segment_count": 1,
                "tie_point_count": 0,
                "reliability_saifi": {"typical": 2.0, "unit": "次/户·年"},
                "reliability_saidi": {"typical": 6.0, "unit": "小时/户·年"},
                "standard": "Q/GDW 10370-2023",
                "source_note": "《配电网规划设计技术导则》及DL/T 5729-2023",
                "topology_template": {
                    "bus_count": 2,
                    "line_count": 1,
                    "switch_count": 2,
                    "tie_switch_count": 0,
                    "connection_pattern": "源端母线→分段开关→线路→末端开关→负荷母线"
                }
            },
            "single_tie": {
                "name": "单联络",
                "description": "两条线路通过联络开关相连，实现互备供电，N-1校验时可通过联络开关转移部分负荷",
                "applicable_area_class": ["B", "C"],
                "max_supply_radius_km": {"min": 5, "max": 10},
                "max_load_mw": {"min": 4, "max": 6},
                "segment_count": {"min": 2, "max": 3},
                "tie_point_count": 1,
                "reliability_saifi": {"typical": 1.2, "unit": "次/户·年"},
                "reliability_saidi": {"typical": 3.0, "unit": "小时/户·年"},
                "standard": "Q/GDW 10370-2023",
                "source_note": "《配电网规划设计技术导则》及DL/T 5729-2023",
                "topology_template": {
                    "bus_count": 3,
                    "line_count": 2,
                    "switch_count": 4,
                    "tie_switch_count": 1,
                    "connection_pattern": "源端母线A→分段开关→线路A→联络开关↔线路B→分段开关→源端母线B，中间负荷母线分别挂接于线路A和线路B"
                }
            },
            "double_tie": {
                "name": "双联络",
                "description": "一条线路与两条相邻线路分别建立联络，具备两个方向转供能力，N-1通过率较高",
                "applicable_area_class": ["A", "B"],
                "max_supply_radius_km": {"min": 3, "max": 5},
                "max_load_mw": {"min": 6, "max": 10},
                "segment_count": 3,
                "tie_point_count": 2,
                "reliability_saifi": {"typical": 0.8, "unit": "次/户·年"},
                "reliability_saidi": {"typical": 1.5, "unit": "小时/户·年"},
                "standard": "Q/GDW 10370-2023",
                "source_note": "《配电网规划设计技术导则》及DL/T 5729-2023",
                "topology_template": {
                    "bus_count": 4,
                    "line_count": 3,
                    "switch_count": 6,
                    "tie_switch_count": 2,
                    "connection_pattern": "源端母线A→线路A→联络开关1↔线路B→源端母线B；线路A→联络开关2↔线路C→源端母线C，中间负荷母线分别挂接于三条线路"
                }
            },
            "three_segment_three_tie": {
                "name": "三段三联络",
                "description": "线路分为三段，每段均设置联络点，与三条相邻线路联络，转供能力最强，适用于高可靠性要求区域",
                "applicable_area_class": ["A", "B"],
                "max_supply_radius_km": {"min": 3, "max": 5},
                "max_load_mw": {"min": 8, "max": 12},
                "segment_count": 3,
                "tie_point_count": 3,
                "reliability_saifi": {"typical": 0.5, "unit": "次/户·年"},
                "reliability_saidi": {"typical": 1.0, "unit": "小时/户·年"},
                "standard": "Q/GDW 10370-2023",
                "source_note": "《配电网规划设计技术导则》及DL/T 5729-2023",
                "topology_template": {
                    "bus_count": 5,
                    "line_count": 4,
                    "switch_count": 8,
                    "tie_switch_count": 3,
                    "connection_pattern": "源端母线→分段开关1→线路段1→联络开关1↔线路B；分段开关2→线路段2→联络开关2↔线路C；分段开关3→线路段3→联络开关3↔线路D，各段负荷母线分别挂接"
                }
            },
            "multi_segment_multi_tie": {
                "name": "多段多联络",
                "description": "线路分4~5段，设置4~5个联络点，实现多方向转供，适用于A类供电区核心区域，可靠性要求极高",
                "applicable_area_class": ["A"],
                "max_supply_radius_km": {"min": 2, "max": 3},
                "max_load_mw": {"min": 10, "max": 15},
                "segment_count": {"min": 4, "max": 5},
                "tie_point_count": {"min": 4, "max": 5},
                "reliability_saifi": {"typical": 0.3, "unit": "次/户·年"},
                "reliability_saidi": {"typical": 0.5, "unit": "小时/户·年"},
                "standard": "Q/GDW 10370-2023",
                "source_note": "《配电网规划设计技术导则》及DL/T 5729-2023",
                "topology_template": {
                    "bus_count": 6,
                    "line_count": 5,
                    "switch_count": 10,
                    "tie_switch_count": 5,
                    "connection_pattern": "源端母线→分段开关1→线路段1→联络开关1↔线路B；分段开关2→线路段2→联络开关2↔线路C；分段开关3→线路段3→联络开关3↔线路D；分段开关4→线路段4→联络开关4↔线路E；可选分段开关5→线路段5→联络开关5↔线路F"
                }
            }
        },
        "mv_10kv_cable": {
            "single_ring": {
                "name": "单环网",
                "description": "两条电缆线路构成环网，正常运行时联络开关断开（开环运行），故障时可通过联络开关转供",
                "applicable_area_class": ["B", "C"],
                "max_supply_radius_km": {"min": 3, "max": 5},
                "max_load_mw": {"min": 6, "max": 10},
                "segment_count": {"min": 4, "max": 6},
                "tie_point_count": 1,
                "reliability_saifi": {"typical": 0.6, "unit": "次/户·年"},
                "reliability_saidi": {"typical": 1.0, "unit": "小时/户·年"},
                "standard": "Q/GDW 10370-2023",
                "source_note": "《配电网规划设计技术导则》及DL/T 5729-2023",
                "topology_template": {
                    "bus_count": 3,
                    "line_count": 2,
                    "switch_count": 4,
                    "tie_switch_count": 1,
                    "connection_pattern": "源端母线A→环网柜1→环网柜2→…→联络开关↔环网柜n→…→环网柜1'→源端母线B，开环运行"
                }
            },
            "double_ring": {
                "name": "双环网",
                "description": "四条电缆线路构成两个环网，互为备用，具备双方向转供能力，适用于高负荷密度区域",
                "applicable_area_class": ["A", "B"],
                "max_supply_radius_km": {"min": 2, "max": 4},
                "max_load_mw": {"min": 10, "max": 15},
                "segment_count": {"min": 4, "max": 6},
                "tie_point_count": 2,
                "reliability_saifi": {"typical": 0.3, "unit": "次/户·年"},
                "reliability_saidi": {"typical": 0.5, "unit": "小时/户·年"},
                "standard": "Q/GDW 10370-2023",
                "source_note": "《配电网规划设计技术导则》及DL/T 5729-2023",
                "topology_template": {
                    "bus_count": 5,
                    "line_count": 4,
                    "switch_count": 8,
                    "tie_switch_count": 2,
                    "connection_pattern": "源端母线A→环网柜组1→联络开关1↔环网柜组2→源端母线B；源端母线C→环网柜组3→联络开关2↔环网柜组4→源端母线D，双环网独立运行互为备用"
                }
            },
            "n1_single_ring": {
                "name": "单环网(N-1)",
                "description": "单环网接线并满足N-1安全准则，任一元件故障时可通过联络开关转移全部负荷，不中断供电",
                "applicable_area_class": ["A", "B"],
                "max_supply_radius_km": {"min": 3, "max": 5},
                "max_load_mw": {"min": 6, "max": 10},
                "segment_count": {"min": 4, "max": 6},
                "tie_point_count": 1,
                "n1_pass_rate_percent": {"A": 100, "B": 100},
                "reliability_saifi": {"typical": 0.4, "unit": "次/户·年"},
                "reliability_saidi": {"typical": 0.8, "unit": "小时/户·年"},
                "standard": "Q/GDW 10370-2023",
                "source_note": "《配电网规划设计技术导则》及DL/T 5729-2023",
                "topology_template": {
                    "bus_count": 3,
                    "line_count": 2,
                    "switch_count": 4,
                    "tie_switch_count": 1,
                    "connection_pattern": "源端母线A→环网柜1→环网柜2→…→联络开关↔环网柜n→…→环网柜1'→源端母线B，开环运行，N-1校验时联络开关闭合转移全部负荷"
                }
            },
            "n1_double_ring": {
                "name": "双环网(N-1)",
                "description": "双环网接线并满足N-1安全准则，任一元件故障时可通过双方向联络开关转移全部负荷，供电可靠性极高",
                "applicable_area_class": ["A", "B"],
                "max_supply_radius_km": {"min": 2, "max": 4},
                "max_load_mw": {"min": 10, "max": 15},
                "segment_count": {"min": 4, "max": 6},
                "tie_point_count": 2,
                "n1_pass_rate_percent": {"A": 100, "B": 100},
                "reliability_saifi": {"typical": 0.2, "unit": "次/户·年"},
                "reliability_saidi": {"typical": 0.3, "unit": "小时/户·年"},
                "standard": "Q/GDW 10370-2023",
                "source_note": "《配电网规划设计技术导则》及DL/T 5729-2023",
                "topology_template": {
                    "bus_count": 5,
                    "line_count": 4,
                    "switch_count": 8,
                    "tie_switch_count": 2,
                    "connection_pattern": "源端母线A→环网柜组1→联络开关1↔环网柜组2→源端母线B；源端母线C→环网柜组3→联络开关2↔环网柜组4→源端母线D，双环网N-1校验时双方向转移全部负荷"
                }
            }
        },
        "lv_04kv": {
            "radial_single": {
                "name": "单回辐射",
                "description": "0.4kV单回线路辐射式供电，结构简单，适用于分散负荷区域",
                "applicable_area_class": ["C", "D", "E"],
                "max_supply_radius_m": 250,
                "max_load_kw": {"min": 100, "max": 200},
                "reliability_saifi": {"typical": 3.0, "unit": "次/户·年"},
                "reliability_saidi": {"typical": 10.0, "unit": "小时/户·年"},
                "standard": "Q/GDW 10370-2023",
                "source_note": "《配电网规划设计技术导则》",
                "topology_template": {
                    "bus_count": 2,
                    "line_count": 1,
                    "switch_count": 1,
                    "tie_switch_count": 0,
                    "connection_pattern": "配电变压器→低压开关→线路→负荷节点"
                }
            },
            "radial_double": {
                "name": "双回辐射",
                "description": "0.4kV双回线路辐射式供电，两回线路互为备用，可靠性高于单回辐射",
                "applicable_area_class": ["B", "C"],
                "max_supply_radius_m": 250,
                "max_load_kw": {"min": 200, "max": 400},
                "reliability_saifi": {"typical": 1.5, "unit": "次/户·年"},
                "reliability_saidi": {"typical": 4.0, "unit": "小时/户·年"},
                "standard": "Q/GDW 10370-2023",
                "source_note": "《配电网规划设计技术导则》",
                "topology_template": {
                    "bus_count": 3,
                    "line_count": 2,
                    "switch_count": 2,
                    "tie_switch_count": 0,
                    "connection_pattern": "配电变压器→低压开关A→线路A→负荷节点组A；配电变压器→低压开关B→线路B→负荷节点组B，两回线路互备"
                }
            },
            "ring": {
                "name": "环网",
                "description": "0.4kV环网接线，正常运行开环，故障时可转供，适用于负荷密度较高区域",
                "applicable_area_class": ["A", "B"],
                "max_supply_radius_m": 250,
                "max_load_kw": {"min": 200, "max": 400},
                "reliability_saifi": {"typical": 1.0, "unit": "次/户·年"},
                "reliability_saidi": {"typical": 2.0, "unit": "小时/户·年"},
                "standard": "Q/GDW 10370-2023",
                "source_note": "《配电网规划设计技术导则》",
                "topology_template": {
                    "bus_count": 3,
                    "line_count": 2,
                    "switch_count": 3,
                    "tie_switch_count": 1,
                    "connection_pattern": "配电变压器A→低压开关→线路A→联络开关↔线路B→低压开关→配电变压器B，开环运行"
                }
            },
            "chain": {
                "name": "链式",
                "description": "0.4kV链式接线，多个配电箱串联供电，结构紧凑，适用于沿线分布的负荷",
                "applicable_area_class": ["B", "C"],
                "max_supply_radius_m": 250,
                "max_load_kw": {"min": 150, "max": 300},
                "reliability_saifi": {"typical": 1.8, "unit": "次/户·年"},
                "reliability_saidi": {"typical": 5.0, "unit": "小时/户·年"},
                "standard": "Q/GDW 10370-2023",
                "source_note": "《配电网规划设计技术导则》",
                "topology_template": {
                    "bus_count": 4,
                    "line_count": 3,
                    "switch_count": 4,
                    "tie_switch_count": 0,
                    "connection_pattern": "配电变压器→低压开关→主干线→配电箱1→分支线→负荷1；主干线→配电箱2→分支线→负荷2；主干线→配电箱3→分支线→负荷3，链式串联"
                }
            }
        }
    }
