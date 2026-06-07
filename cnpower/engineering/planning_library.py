def get_planning_assumption_library():
    return {
        "metadata": {
            "name": "中国配网规划参数与方案比较库",
            "version": "1.0.0",
            "scope": "10kV-0.4kV配电网规划、改造、新能源接入、可靠性与投资对比。",
        },
        "voltage_limits": {
            "normal_operation": {
                "10kV": {"min_vm_pu": 0.93, "max_vm_pu": 1.07, "standard": "GB/T 12325"},
                "0.4kV_3phase": {"min_vm_pu": 0.93, "max_vm_pu": 1.07, "standard": "GB/T 12325"},
                "0.4kV_1phase": {"min_vm_pu": 0.90, "max_vm_pu": 1.07, "standard": "GB/T 12325"},
            },
            "planning_target": {
                "10kV": {"min_vm_pu": 0.95, "max_vm_pu": 1.05},
                "0.4kV": {"min_vm_pu": 0.92, "max_vm_pu": 1.05},
            },
        },
        "loading_limits": {
            "transformer": {
                "normal_percent": {"urban": 80, "rural": 70, "industrial": 85},
                "short_time_emergency_percent": 120,
                "n_1_transfer_target_percent": 100,
            },
            "line": {
                "normal_percent": 80,
                "emergency_percent": 100,
                "planning_margin_percent": 15,
            },
            "switchgear": {
                "rated_current_margin_percent": 20,
                "short_circuit_breaking_margin_percent": 10,
            },
        },
        "supply_radius": {
            "10kV_overhead_km": {"A": 3, "B": 5, "C": 10, "D": 15, "E": 15},
            "10kV_cable_km": {"A": 2, "B": 4, "C": 5, "D": 8, "E": 8},
            "0.4kV_m": {"urban": 200, "rural": 250, "strict_voltage_drop": 150},
        },
        "load_model": {
            "cos_phi_default": {
                "residential": 0.92,
                "commercial": 0.90,
                "industrial": 0.88,
                "agricultural": 0.85,
                "ev_charging": 0.98,
            },
            "simultaneity_factor": {
                "residential_lv": {"households_0_20": 0.85, "households_21_100": 0.65, "households_101_plus": 0.50},
                "commercial": 0.75,
                "industrial": 0.85,
                "ev_public_fast": 0.60,
            },
            "annual_growth_rate_percent": {
                "mature_urban": 2.0,
                "new_urban": 5.0,
                "industrial_park": 6.0,
                "rural": 1.5,
                "ev_charging": 15.0,
            },
            "typical_profiles": ["summer_peak_day", "winter_peak_day", "spring_light_load", "evening_ev_peak", "low_load_high_pv"],
        },
        "renewable_hosting": {
            "pv_connection_voltage": {
                "household_rooftop_kw": {"max": 50, "preferred_voltage_kv": 0.4},
                "village_or_commercial_kw": {"min": 50, "max": 400, "preferred_voltage_kv": 0.4},
                "large_distributed_kw": {"min": 400, "preferred_voltage_kv": 10},
            },
            "screening_limits": {
                "pv_capacity_to_transformer_capacity_percent": {"conservative": 30, "detailed_study": 50},
                "voltage_rise_percent_at_pcc": 5,
                "reverse_power_flow_flag": "需要按台区、馈线和主变三级记录并可配置是否允许。",
                "power_factor_range": "0.95 leading to 0.95 lagging, or Volt/Var curve",
            },
            "study_cases": ["peak_load_peak_pv", "low_load_peak_pv", "evening_peak_no_pv", "n_1_with_pv_trip"],
        },
        "storage_planning": {
            "applications": {
                "peak_shaving": {"duration_h": [2, 4], "dispatch": "daily_peak_valley"},
                "pv_smoothing": {"duration_h": [1, 2], "dispatch": "ramp_rate_limit"},
                "backup_supply": {"duration_h": [1, 4], "dispatch": "critical_load_support"},
                "voltage_support": {"duration_h": [0.5, 2], "dispatch": "volt_var"},
            },
            "soc_constraints_percent": {"min": 10, "max": 90, "reserve_for_backup": 20},
            "round_trip_efficiency_default_percent": 90,
        },
        "planning_scenarios": {
            "base_year_peak": {"description": "现状年最大负荷潮流与越限检查。", "required_calculations": ["power_flow", "loading", "voltage"]},
            "target_year_peak": {"description": "规划年最大负荷，校核扩容必要性。", "required_calculations": ["power_flow", "n_1", "short_circuit"]},
            "low_load_high_pv": {"description": "低负荷高光伏出力，校核电压抬升和反送。", "required_calculations": ["power_flow", "hosting_capacity", "power_quality"]},
            "n_1_transfer": {"description": "馈线、主变、开关站N-1转供能力校核。", "required_calculations": ["topology_switching", "power_flow", "loading"]},
            "short_circuit_max_min": {"description": "最大/最小短路电流，校核开断能力和保护灵敏度。", "required_calculations": ["short_circuit"]},
            "ev_evening_peak": {"description": "充电负荷晚高峰叠加居民负荷。", "required_calculations": ["time_series", "power_flow", "loading"]},
        },
        "comparison_metrics": {
            "technical": ["voltage_violation_count", "max_loading_percent", "loss_mwh_per_year", "n_1_pass_rate_percent", "short_circuit_margin_percent", "hosting_capacity_kw"],
            "economic": ["capex_cny", "opex_cny_per_year", "loss_cost_cny_per_year", "npv_cny", "payback_year", "asset_utilization_percent"],
            "reliability": ["saidi_min_per_customer_year", "saifi_times_per_customer_year", "eens_mwh_per_year", "critical_load_restoration_percent"],
            "new_energy": ["pv_curtailed_mwh_per_year", "reverse_power_hours", "carbon_reduction_ton_per_year", "storage_cycle_count_per_year"],
        },
        "candidate_generation": {
            "transformer_upgrade": {
                "trigger": ["loading_over_limit", "voltage_low", "new_load_access"],
                "candidate_actions": ["replace_larger_capacity", "add_parallel_transformer", "split_service_area", "install_voltage_regulation"],
            },
            "feeder_reinforcement": {
                "trigger": ["line_overload", "voltage_drop", "n_1_transfer_fail"],
                "candidate_actions": ["increase_conductor_section", "new_feeder", "add_tie_point", "convert_overhead_to_cable", "install_recloser_or_sectionalizer"],
            },
            "renewable_access": {
                "trigger": ["pv_connection_request", "voltage_rise", "reverse_power_flow"],
                "candidate_actions": ["volt_var_control", "curtailment", "storage", "transformer_tap_adjustment", "feeder_reconfiguration"],
            },
            "ev_charging_access": {
                "trigger": ["charging_station_request", "evening_peak_overload"],
                "candidate_actions": ["managed_charging", "dedicated_transformer", "feeder_upgrade", "storage_buffer"],
            },
        },
        "cost_model_placeholders": {
            "note": "以下为规划系统字段结构，不作为招标价格。项目落地时应接入地区造价库。",
            "required_cost_fields": ["equipment_cost_cny", "installation_cost_cny", "civil_cost_cny", "land_or_corridor_cost_cny", "annual_maintenance_cny", "salvage_value_cny"],
            "line_cost_drivers": ["voltage_level", "conductor_type", "cross_section_mm2", "laying_method", "urban_road_excavation", "terrain"],
            "station_cost_drivers": ["capacity_kva", "switchgear_scheme", "automation_level", "building_or_box_type", "fire_protection"],
        },
    }
