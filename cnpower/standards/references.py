def get_all_standards():
    _standards_list = [
        {
            "code": "GB/T 6451-2023",
            "name": "油浸式电力变压器技术参数和要求",
            "year": 2023,
            "scope": "电压等级为6kV、110kV的油浸式电力变压器",
            "related_equipment": ["变压器"],
            "related_rules": ["transformer_loading"]
        },
        {
            "code": "GB/T 10228-2023",
            "name": "干式电力变压器技术参数和要求",
            "year": 2023,
            "scope": "电压等级为6kV、35kV的干式电力变压器",
            "related_equipment": ["变压器"],
            "related_rules": ["transformer_loading"]
        },
        {
            "code": "GB/T 12706-2020",
            "name": "额定电压1kV到35kV挤包绝缘电力电缆及其附件",
            "year": 2020,
            "scope": "额定电压1kV到35kV的挤包绝缘电力电缆及附件",
            "related_equipment": ["电缆"],
            "related_rules": ["conductor_economy", "conductor_ampacity", "cable_thermal_stability"]
        },
        {
            "code": "GB/T 11017-2014",
            "name": "额定电压110kV交联聚乙烯绝缘电力电缆及其附件",
            "year": 2014,
            "scope": "额定电压110kV交联聚乙烯绝缘电力电缆",
            "related_equipment": ["电缆"],
            "related_rules": ["conductor_economy", "conductor_ampacity"]
        },
        {
            "code": "GB/T 14049-2008",
            "name": "额定电压10kV架空绝缘电缆",
            "year": 2008,
            "scope": "额定电压10kV架空聚乙烯绝缘电缆",
            "related_equipment": ["架空绝缘电缆"],
            "related_rules": ["conductor_economy", "conductor_ampacity"]
        },
        {
            "code": "GB/T 1179-2017",
            "name": "架空导线技术参数和要求",
            "year": 2017,
            "scope": "架空输电线路用铝线、钢芯铝线等",
            "related_equipment": ["架空导线"],
            "related_rules": ["conductor_economy", "conductor_ampacity", "conductor_voltage_drop"]
        },
        {
            "code": "GB/T 12325-2008",
            "name": "电能质量 供电电压偏差",
            "year": 2008,
            "scope": "电力系统供电电压偏差的允许值",
            "related_equipment": [],
            "related_rules": ["voltage_deviation"]
        },
        {
            "code": "GB/T 12326-2008",
            "name": "电能质量 电压波动和闪变",
            "year": 2008,
            "scope": "电力系统电压波动和闪变的允许值",
            "related_equipment": [],
            "related_rules": ["voltage_fluctuation_flicker"]
        },
        {
            "code": "GB/T 14549-1993",
            "name": "电能质量 公用电网谐波",
            "year": 1993,
            "scope": "公用电网谐波电压含有率和总谐波畸变率的允许值",
            "related_equipment": [],
            "related_rules": ["harmonic"]
        },
        {
            "code": "GB/T 15543-2008",
            "name": "电能质量 三相电压不平衡",
            "year": 2008,
            "scope": "电力系统三相电压不平衡度的允许值",
            "related_equipment": [],
            "related_rules": ["three_phase_unbalance"]
        },
        {
            "code": "GB/T 15544-2023",
            "name": "三相交流系统短路电流计算",
            "year": 2023,
            "scope": "三相交流系统短路电流计算方法",
            "related_equipment": ["断路器", "电缆"],
            "related_rules": ["three_phase_max", "single_phase_min", "cable_thermal_stability"]
        },
        {
            "code": "GB 50052-2009",
            "name": "供配电系统设计规范",
            "year": 2009,
            "scope": "供配电系统的设计原则和要求",
            "related_equipment": ["变压器", "导体", "断路器"],
            "related_rules": ["transformer_loading", "conductor_economy", "conductor_ampacity", "breaker_rating"]
        },
        {
            "code": "GB 50054-2011",
            "name": "低压配电设计规范",
            "year": 2011,
            "scope": "低压配电网络的设计原则和要求",
            "related_equipment": ["低压导体", "低压开关"],
            "related_rules": ["conductor_ampacity", "conductor_voltage_drop"]
        },
        {
            "code": "GB 50065-2011",
            "name": "交流电气装置的接地设计规范",
            "year": 2011,
            "scope": "交流电气装置接地设计的原则和要求",
            "related_equipment": ["接地装置"],
            "related_rules": []
        },
        {
            "code": "GB 50060-2008",
            "name": "3~110kV高压配电装置设计规范",
            "year": 2008,
            "scope": "3~110kV高压配电装置的设计原则和要求",
            "related_equipment": ["变压器", "断路器", "互感器"],
            "related_rules": ["breaker_rating"]
        },
        {
            "code": "DL/T 599-2016",
            "name": "城市中低压配电网络改造技术导则",
            "year": 2016,
            "scope": "城市中低压配电网络改造的技术要求",
            "related_equipment": ["变压器", "导体", "开关"],
            "related_rules": ["transformer_loading", "conductor_ampacity"]
        },
        {
            "code": "DL/T 5729-2023",
            "name": "配电网规划设计技术导则",
            "year": 2023,
            "scope": "配电网规划设计的总体原则和技术要求",
            "related_equipment": ["变压器", "导体", "开关"],
            "related_rules": ["n1_safety", "saidi_target", "saifi_target"]
        },
        {
            "code": "Q/GDW 10370-2023",
            "name": "配电网规划设计技术导则",
            "year": 2023,
            "scope": "国家电网配电网规划设计的技术导则",
            "related_equipment": ["变压器", "导体", "开关"],
            "related_rules": ["n1_safety", "connection_modes"]
        },
        {
            "code": "GB/T 45418-2025",
            "name": "配电网规划设计规范",
            "year": 2025,
            "scope": "配电网规划设计的总体规范要求",
            "related_equipment": ["变压器", "导体", "开关"],
            "related_rules": ["n1_safety", "connection_modes"]
        },
        {
            "code": "NB/T 10994-2022",
            "name": "分布式电源接入配电网技术规定",
            "year": 2022,
            "scope": "分布式电源接入配电网的技术要求",
            "related_equipment": ["光伏逆变器", "光伏组件"],
            "related_rules": ["pv_penetration_limit", "voltage_rise_check", "reverse_power_flow"]
        },
        {
            "code": "GB/T 19964-2012",
            "name": "光伏发电站接入电力系统技术规定",
            "year": 2012,
            "scope": "光伏发电站接入电力系统的技术要求",
            "related_equipment": ["光伏逆变器"],
            "related_rules": ["pv_penetration_limit", "voltage_rise_check"]
        },
        {
            "code": "GB/T 36558-2018",
            "name": "电力系统电化学储能系统通用技术条件",
            "year": 2018,
            "scope": "电力系统电化学储能系统的通用技术要求",
            "related_equipment": ["energy_storage"],
            "related_rules": ["energy_storage_safety"]
        },
        {
            "code": "GB/T 34131-2023",
            "name": "电化学储能站接入电网技术规定",
            "year": 2023,
            "scope": "电化学储能站接入电网的技术要求",
            "related_equipment": ["储能系统"],
            "related_rules": ["pv_penetration_limit", "voltage_rise_check"]
        },
        {
            "code": "GB/T 18487.1-2023",
            "name": "电动车导电充电系统 通用要求",
            "year": 2023,
            "scope": "电动车导电充电系统的通用技术要求",
            "related_equipment": ["充电桩"],
            "related_rules": ["pv_penetration_limit"]
        },
        {
            "code": "GB/T 27930-2015",
            "name": "电动车非车载充电机与充电设备之间的通信协议",
            "year": 2015,
            "scope": "电动车充电通信协议规定",
            "related_equipment": ["充电桩"],
            "related_rules": []
        },
        {
            "code": "GB/T 15166.2-2023",
            "name": "交流高压熔断器",
            "year": 2023,
            "scope": "交流高压熔断器的技术要求",
            "related_equipment": ["熔断器"],
            "related_rules": ["breaker_rating"]
        },
        {
            "code": "GB/T 12527-2008",
            "name": "额定电压1kV及以下架空绝缘电缆",
            "year": 2008,
            "scope": "额定电压1kV及以下架空聚乙烯绝缘电缆",
            "related_equipment": ["架空绝缘电缆"],
            "related_rules": ["conductor_economy", "conductor_ampacity"]
        },
        {
            "code": "GB 20052-2020",
            "name": "电力变压器能效限定值及能效等级",
            "year": 2020,
            "scope": "电力变压器能效限定值及能效等级",
            "related_equipment": ["变压器"],
            "related_rules": ["transformer_loading"]
        },
        {
            "code": "GB/T 19068-2017",
            "name": "离网型风力发电机组",
            "year": 2017,
            "scope": "离网型风力发电机组的技术要求",
            "related_equipment": ["风机"],
            "related_rules": []
        },
        {
            "code": "GB/T 25383-2017",
            "name": "风力发电机组",
            "year": 2017,
            "scope": "风力发电机组的技术要求",
            "related_equipment": ["风机"],
            "related_rules": []
        },
        {
            "code": "GB/T 1984-2024",
            "name": "高压交流断路器",
            "year": 2024,
            "scope": "额定电压3.6kV及以上的交流断路器",
            "related_equipment": ["断路器"],
            "related_rules": ["breaker_rating"]
        },
        {
            "code": "GB/T 3804-2017",
            "name": "3.6kV~40.5kV高压交流负荷开关",
            "year": 2017,
            "scope": "3.6kV~40.5kV高压交流负荷开关的技术要求",
            "related_equipment": ["负荷开关"],
            "related_rules": ["breaker_rating"]
        },
        {
            "code": "GB/T 11022-2020",
            "name": "高压交流开关设备和控制设备的共同技术规范",
            "year": 2020,
            "scope": "高压交流开关设备的共同技术要求",
            "related_equipment": ["断路器", "负荷开关"],
            "related_rules": ["breaker_rating"]
        },
        {
            "code": "GB/T 20840.3-2013",
            "name": "电磁式电压互感器",
            "year": 2013,
            "scope": "电磁式电压互感器的技术要求",
            "related_equipment": ["电压互感器"],
            "related_rules": ["voltage_deviation"]
        },
        {
            "code": "GB/T 20840.2-2014",
            "name": "电磁式电流互感器",
            "year": 2014,
            "scope": "电磁式电流互感器的技术要求",
            "related_equipment": ["电流互感器"],
            "related_rules": ["transformer_loading"]
        },
        {
            "code": "GB/T 11032-2020",
            "name": "交流系统用无间隙金属氧化物避雷器",
            "year": 2020,
            "scope": "交流系统用无间隙金属氧化物避雷器的技术要求",
            "related_equipment": ["避雷器"],
            "related_rules": []
        },
        {
            "code": "GB/T 1094-2013",
            "name": "电力变压器 第1部分：总则",
            "year": 2013,
            "scope": "电力变压器的总则技术要求",
            "related_equipment": ["变压器"],
            "related_rules": ["transformer_loading"]
        },
        {
            "code": "GB/T 17467-2020",
            "name": "高压/低压预装式变电站",
            "year": 2020,
            "scope": "高压/低压预装式变电站的技术要求",
            "related_equipment": ["箱式变电站"],
            "related_rules": ["transformer_loading"]
        },
        {
            "code": "GB/T 11024-2019",
            "name": "标称电压1kV及以上交流电力系统用并联电容器",
            "year": 2019,
            "scope": "交流电力系统用并联电容器的技术要求",
            "related_equipment": ["并联电容器"],
            "related_rules": ["voltage_deviation", "voltage_rise_check"]
        },
        {
            "code": "GB/T 12747-2004",
            "name": "标称电压1kV及以下交流电力系统用自愈式串联电容器",
            "year": 2004,
            "scope": "低压自愈式串联电容器的技术要求",
            "related_equipment": ["电容器"],
            "related_rules": ["voltage_deviation"]
        },
        {
            "code": "GB/T 36287-2018",
            "name": "电力系统用蓄电池",
            "year": 2018,
            "scope": "电力系统用蓄电池的技术要求",
            "related_equipment": ["蓄电池"],
            "related_rules": []
        },
        {
            "code": "DL/T 584-2021",
            "name": "3kV~110kV电网继电保护装置运行管理规程",
            "year": 2021,
            "scope": "3kV~110kV电网继电保护装置的运行管理",
            "related_equipment": ["继电保护装置"],
            "related_rules": ["single_phase_min"]
        },
        {
            "code": "GB/T 19069-2003",
            "name": "电力系统远动保护技术规定",
            "year": 2003,
            "scope": "电力系统远动保护的技术要求",
            "related_equipment": ["保护装置"],
            "related_rules": ["single_phase_min"]
        },
        {
            "code": "GB/T 2900-2007",
            "name": "电工术语 变压器、互感器、调压器和电抗器",
            "year": 2007,
            "scope": "变压器、互感器等设备的术语定义",
            "related_equipment": ["变压器", "互感器"],
            "related_rules": []
        },
        {
            "code": "DL/T 698-2018",
            "name": "电能质量管理终端技术规范",
            "year": 2018,
            "scope": "电能质量管理终端的技术规范",
            "related_equipment": ["电能质量终端"],
            "related_rules": ["voltage_deviation", "harmonic"]
        }
    ]
    return {s["code"]: s for s in _standards_list}
