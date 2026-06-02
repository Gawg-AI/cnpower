<h1 align="center">🔌 cnpower</h1>

<p align="center">
<strong>中国 10kV/0.4kV 配电网工程参数库</strong><br>
<strong>Chinese 10kV/0.4kV Distribution Grid Engineering Parameter Library</strong>
</p>

<p align="center">
<a href="https://github.com/Gawg-AI/cnpower/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.8+-green.svg" alt="Python 3.8+"></a>
<img src="https://img.shields.io/badge/Standards-GB%2FT%202023-orange.svg" alt="GB/T 2023">
<img src="https://img.shields.io/badge/Models-662-brightgreen.svg" alt="662 Models">
</p>

---

## 中文说明

### 概述

`cnpower` 是一套面向中国 10kV/0.4kV 配电网规划的工程参数库，涵盖 **662** 种设备型号参数、典型接线模式、国标合规校验规则，并提供与 [pandapower](https://github.com/e2nIEE/pandapower) 的零侵入集成接口。

### 核心特性

| 模块 | 内容 | 型号数 |
|------|------|--------|
| 🔌 变压器 | 油浸(S11/S13/S15/SH15)、干式(SCB10-13/SCBH15)、箱变、35kV/110kV主变、三绕组 | 212 |
| 🔗 电缆 | 10kV/35kV/0.4kV/110kV 交联聚乙烯电缆(YJV/YJV22) | 178 |
| 📡 架空线 | 10kV绝缘线、0.4kV绝缘线、裸导线(LJ/LGJ) | 82 |
| ⚡ 开关柜 | KYN28A/XGN66、VS1/VD4断路器、FN7负荷开关、XRNT熔断器、低压断路器 | 61 |
| 🔋 无功补偿 | MV/LV电容器、SVG | 29 |
| 🛡️ 保护 | 线路保护、变压器保护 | 10 |
| 📊 互感器 | CT(LZZBJ9/BH-LMZ)、PT(JDZ/JDZJ) | 32 |
| ⚡ 避雷器 | HY5WZ/HY10WZ/HY1.5W | 4 |
| ☀️ 光伏 | 组件(单晶/多晶/薄膜)、组串式/集中式逆变器 | 17 |
| 🚗 充电桩 | AC慢充/DC快充/DC超充 | 9 |
| 🔋 储能 | LFP/铅碳电池、PCS | 19 |
| 💨 风机 | 小型/中型风力发电机 | 9 |

### 国标依据（最新版本）

- **GB/T 6451-2023** 油浸式电力变压器技术参数和要求
- **GB/T 10228-2023** 干式电力变压器技术参数和要求
- **GB/T 12706-2020** 额定电压1kV到35kV挤包绝缘电力电缆
- **GB/T 1179-2017** 圆线同心绞架空导线
- **GB/T 12527-2008** 额定电压1kV及以下架空绝缘电缆
- **GB/T 14049-2008** 额定电压10kV架空绝缘电缆
- **GB/T 1984-2024** 高压交流断路器
- **GB/T 17467-2020** 高压/低压预装式变电站
- **GB 20052-2020** 电力变压器能效限定值及能效等级
- **GB/T 19068-2017** 离网型风力发电机组
- **GB/T 25383-2017** 风力发电机组
- 更多见 `standards/references.py`（41+项标准索引）

### 快速开始

```python
# 导入设备参数
from cnpower.equipment import (
    get_all_transformers,
    get_all_cables,
    get_all_overhead_lines,
)

# 获取10kV油浸式变压器参数
transformers = get_all_transformers()
s13_630 = transformers["oil_immersed"]["S13-630/10"]
print(f"S13-630/10: {s13_630['sn_kva']}kVA, Vk={s13_630['vk_percent']}%")

# 获取10kV电缆参数
cables = get_all_cables()
yJV_70 = cables["mv_10kv"]["YJV22-3x70-10kV"]
print(f"YJV22-3x70: R={yJV_70['r_ohm_per_km']}Ω/km, I={yJV_70['max_i_ka']*1000}A")
```

### Pandapower 集成

```python
import pandapower as pp
from cnpower.pandapower_integration import add_chinese_std_types

net = pp.create_empty_network()
add_chinese_std_types(net)  # 一行注入全部中国标准类型

# 使用中国标准变压器创建网络
pp.create_transformer(net, hv_bus, lv_bus, std_type="S13-630/10")
pp.create_line(net, from_bus, to_bus, length_km=2.0, std_type="YJV22-3x70-10kV")
pp.runpp(net)
```

### 项目结构

```
cnpower/
├── __init__.py                          # 版本与全局常量
├── equipment/                           # 设备参数库
│   ├── transformers.py                  # 变压器 (212型号)
│   ├── cables.py                        # 电缆 (178型号)
│   ├── overhead_lines.py                # 架空线 (82型号)
│   ├── switchgear.py                    # 开关柜/断路器 (61型号)
│   ├── reactive_compensation.py         # 无功补偿 (29型号)
│   ├── protection.py                    # 继电保护 (10型号)
│   ├── instrument_transformers.py       # 互感器 (32型号)
│   ├── surge_arresters.py               # 避雷器 (4型号)
│   └── new_energy/                      # 新能源
│       ├── photovoltaic.py              # 光伏 (17型号)
│       ├── ev_charger.py                # 充电桩 (9型号)
│       ├── energy_storage.py            # 储能 (19型号)
│       └── wind_turbine.py              # 风机 (9型号)
├── topology/
│   └── connection_modes.py              # 13种典型接线模式
├── validation/
│   └── rules.py                         # 国标合规校验规则
├── standards/
│   └── references.py                    # 41+项国标/行标索引
├── engineering/                         # 工程计算模块
│   ├── compliance_constraints.py        # 合规约束定义
│   ├── compliance_checker.py            # 合规检查器
│   ├── pandapower_bridge.py             # Pandapower桥接
│   ├── asset_schema.py                  # 资产数据模式
│   └── planning_library.py              # 规划库
├── pandapower_integration/
│   └── std_types_cn.py                  # Pandapower标准类型注入
└── verify_fixes.py                      # 修复验证脚本
```

### 数据格式约定

所有设备参数库统一使用 `dict[str, dict]` 格式（型号名为 key）：

```python
{
    "S13-630/10": {
        "sn_kva": 630,
        "vn_hv_kv": 10,
        "vn_lv_kv": 0.4,
        "vk_percent": 4.5,
        "vkr_percent": 0.98,
        "pfe_kw": 0.81,
        "i0_percent": 0.6,
        "vector_group": "Dyn11",
        "shift_degree": 30,
        ...
    }
}
```

---

## English Documentation

### Overview

`cnpower` is an engineering parameter library for Chinese 10kV/0.4kV distribution grid planning, covering **662+** equipment models, typical connection modes, GB/T compliance validation rules, and a zero-invasion integration interface with [pandapower](https://github.com/e2nIEE/pandapower).

### Key Features

| Module | Content | Models |
|--------|---------|--------|
| 🔌 Transformers | Oil-immersed (S11/S13/S15/SH15), Dry-type (SCB10-13/SCBH15), Box substation, 35kV/110kV main, Three-winding | 212 |
| 🔗 Cables | 10kV/35kV/0.4kV/110kV XLPE cables (YJV/YJV22) | 178 |
| 📡 Overhead Lines | 10kV insulated, 0.4kV insulated, Bare conductors (LJ/LGJ) | 82 |
| ⚡ Switchgear | KYN28A/XGN66, VS1/VD4 breakers, FN7 load switches, XRNT fuses, LV breakers | 61 |
| 🔋 Reactive Compensation | MV/LV capacitors, SVG | 29 |
| 🛡️ Protection | Line protection, Transformer protection | 10 |
| 📊 Instrument Transformers | CT (LZZBJ9/BH-LMZ), PT (JDZ/JDZJ) | 32 |
| ⚡ Surge Arresters | HY5WZ/HY10WZ/HY1.5W | 4 |
| ☀️ Photovoltaic | Modules (mono-Si/poly-Si/thin-film), String/central inverters | 17 |
| 🚗 EV Chargers | AC slow / DC fast / DC super-fast | 9 |
| 🔋 Energy Storage | LFP/Lead-carbon batteries, PCS | 19 |
| 💨 Wind Turbines | Small/Medium wind generators | 9 |

### Chinese National Standards (Latest Versions)

- **GB/T 6451-2023** Technical parameters and requirements for oil-immersed power transformers
- **GB/T 10228-2023** Technical parameters and requirements for dry-type power transformers
- **GB/T 12706-2020** Extruded insulation power cables rated 1kV to 35kV
- **GB/T 1179-2017** Round wire concentric lay overhead electrical stranded conductors
- **GB/T 12527-2008** Aerial insulated cables for rated voltages up to and including 1kV
- **GB/T 14049-2008** Aerial insulated cables for rated voltage 10kV
- **GB/T 1984-2024** High-voltage alternating-current circuit-breakers
- **GB/T 17467-2020** High-voltage/low-voltage prefabricated substation
- **GB 20052-2020** Minimum allowable values of energy efficiency for power transformers
- See `standards/references.py` for 41+ standards index

### Quick Start

```python
from cnpower.equipment import (
    get_all_transformers,
    get_all_cables,
    get_all_overhead_lines,
)

# Get 10kV oil-immersed transformer parameters
transformers = get_all_transformers()
s13_630 = transformers["oil_immersed"]["S13-630/10"]
print(f"S13-630/10: {s13_630['sn_kva']}kVA, Vk={s13_630['vk_percent']}%")

# Get 10kV cable parameters
cables = get_all_cables()
yJV_70 = cables["mv_10kv"]["YJV22-3x70-10kV"]
print(f"YJV22-3x70: R={yJV_70['r_ohm_per_km']}Ω/km, I={yJV_70['max_i_ka']*1000}A")
```

### Pandapower Integration

```python
import pandapower as pp
from cnpower.pandapower_integration import add_chinese_std_types

net = pp.create_empty_network()
add_chinese_std_types(net)  # One-line injection of all Chinese standard types

# Use Chinese standard types to build the network
pp.create_transformer(net, hv_bus, lv_bus, std_type="S13-630/10")
pp.create_line(net, from_bus, to_bus, length_km=2.0, std_type="YJV22-3x70-10kV")
pp.runpp(net)
```

### Data Format Convention

All equipment parameter libraries use `dict[str, dict]` format (model name as key):

```python
{
    "S13-630/10": {
        "sn_kva": 630,
        "vn_hv_kv": 10,
        "vn_lv_kv": 0.4,
        "vk_percent": 4.5,
        "vkr_percent": 0.98,
        "pfe_kw": 0.81,
        "i0_percent": 0.6,
        "vector_group": "Dyn11",
        "shift_degree": 30,
        ...
    }
}
```

### Pandapower Compatibility

| Parameter | pandapower field | Unit | Notes |
|-----------|-----------------|------|-------|
| Rated power | `sn_mva` | MVA | Converted from kVA |
| HV voltage | `vn_hv_kv` | kV | |
| LV voltage | `vn_lv_kv` | kV | |
| Short-circuit voltage | `vk_percent` | % | |
| Resistive component | `vkr_percent` | % | |
| No-load loss | `pfe_kw` | kW | |
| No-load current | `i0_percent` | % | |
| Phase shift | `shift_degree` | ° | Dyn11→30° |
| Resistance | `r_ohm_per_km` | Ω/km | |
| Reactance | `x_ohm_per_km` | Ω/km | |
| Capacitance | `c_nf_per_km` | nF/km | |
| Max current | `max_i_ka` | kA | |

---

## 📜 License

MIT License with Attribution Requirement — 使用本库需注明来源：https://github.com/Gawg-AI/cnpower

详见 [LICENSE](LICENSE) 文件。

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📣 Attribution / 引用声明

If you use this library in your project, paper, or any derivative work, please include the following attribution:

如在项目、论文或衍生作品中使用本库，请注明以下归属：

```
数据来源 / Data Source: cnpower - https://github.com/Gawg-AI/cnpower
```

## ⚠️ Disclaimer

本库中的设备参数基于公开国标和典型工程值整理，仅供参考。实际工程设计请以设备厂家最新产品手册和现行国标为准。

The equipment parameters in this library are compiled from published national standards and typical engineering values for reference only. Actual engineering design should be based on the latest manufacturer product manuals and current national standards.

## 📧 Contact / 联系方式

Email: ahx@qq.com
