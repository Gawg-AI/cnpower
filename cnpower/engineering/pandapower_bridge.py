def get_pandapower_bridge_spec():
    return {
        "metadata": {
            "name": "pandapower融合适配说明",
            "validated_with_pandapower": "3.4.0",
            "target_project": "e2nIEE/pandapower",
            "target_url": "https://github.com/e2nIEE/pandapower",
        },
        "supported_core_functions": {
            "power_flow": {"api": "pandapower.runpp", "status": "直接支持"},
            "dc_power_flow": {"api": "pandapower.rundcpp", "status": "可用于高层筛选，配网主计算仍建议AC潮流"},
            "optimal_power_flow": {"api": "pandapower.runopp", "status": "可用于无功、电压、储能和分布式电源调度的优化雏形"},
            "short_circuit": {"api": "pandapower.shortcircuit.calc_sc", "status": "直接支持，需要外部电网和设备零序/短路参数完整"},
            "state_estimation": {"api": "pandapower.estimation.estimate", "status": "支持，需测量点和量测精度库"},
            "time_series": {"api": "pandapower.timeseries.run_timeseries", "status": "支持，适合负荷、光伏、储能和EV时序仿真"},
            "control": {"api": "pandapower.control", "status": "支持，适合OLTC、无功、电压控制器"},
        },
        "element_mapping": {
            "source_grid": {"pandapower": "ext_grid", "required": ["bus", "vm_pu"], "recommended": ["s_sc_max_mva", "rx_max", "s_sc_min_mva", "rx_min"]},
            "busbar": {"pandapower": "bus", "required": ["vn_kv"], "recommended": ["min_vm_pu", "max_vm_pu", "geodata"]},
            "line_cable": {"pandapower": "line", "std_type": "chinese_line_std_types", "required": ["from_bus", "to_bus", "length_km", "std_type"]},
            "line_overhead": {"pandapower": "line", "std_type": "chinese_line_std_types", "required": ["from_bus", "to_bus", "length_km", "std_type"]},
            "transformer_2w": {"pandapower": "trafo", "std_type": "chinese_trafo_std_types", "required": ["hv_bus", "lv_bus", "std_type"]},
            "transformer_3w": {"pandapower": "trafo3w", "std_type": "chinese_trafo3w_std_types", "required": ["hv_bus", "mv_bus", "lv_bus", "std_type"]},
            "switch_breaker": {"pandapower": "switch", "required": ["bus", "element", "et", "closed"], "note": "保护开断能力需由工程参数库单独校验"},
            "load": {"pandapower": "load", "required": ["bus", "p_mw", "q_mvar"]},
            "pv_inverter": {"pandapower": "sgen", "required": ["bus", "p_mw", "q_mvar", "sn_mva"], "note": "光伏组件阵列作为工程对象，电气等值映射到sgen"},
            "wind_turbine": {"pandapower": "sgen", "required": ["bus", "p_mw", "q_mvar", "sn_mva"]},
            "storage": {"pandapower": "storage", "required": ["bus", "p_mw", "max_e_mwh", "soc_percent"]},
            "ev_charger": {"pandapower": "load", "required": ["bus", "p_mw", "q_mvar"], "note": "可通过时序profile表达充电行为"},
            "reactive_compensation": {"pandapower": "shunt", "required": ["bus", "q_mvar", "p_mw"]},
            "metering_ct_pt": {"pandapower": "measurement", "required": ["measurement_type", "element_type", "element", "value", "std_dev"]},
        },
        "data_completeness_requirements": {
            "power_flow_minimum": ["bus.vn_kv", "line.r/x/c/max_i", "trafo.sn/vn/vk/vkr/pfe/i0", "load.p/q", "source.vm_pu"],
            "short_circuit_minimum": ["ext_grid.s_sc_max/min_mva", "ext_grid.rx_max/min", "line.r0/x0/c0", "trafo.vk0/vkr0/mag0", "switchgear.breaking_current"],
            "n_1_minimum": ["topology switch status", "tie switch normal open point", "asset loading limit", "transfer target load", "operation constraints"],
            "planning_comparison_minimum": ["capex", "opex", "loss cost", "reliability target", "construction feasibility", "new energy hosting capacity"],
            "drag_drop_modeling_minimum": ["asset class", "ports", "allowed connections", "default parameter template", "pandapower element mapping", "validation rules"],
        },
        "known_gaps_to_keep_outside_pandapower": [
            "图元库、端口连接、画布坐标和拓扑编辑属于前端/工程对象层，不是pandapower职责。",
            "国家/企业标准条文解释、工程选型规则、造价库、施工可行性和可靠性指标需要工程参数库补充。",
            "保护定值配合、继电保护曲线、电能质量谐波详细计算需外部专业模型或扩展模块。",
            "配网规划方案生成、排序、投资估算和多目标决策需要在pandapower计算结果之上构建。",
        ],
    }

