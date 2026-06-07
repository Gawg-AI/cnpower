# cnpower

面向中国配电网规划、仿真建模、设备选型和工程校核的 Python 参数库。

`cnpower` 汇总了 10kV/0.4kV 配网常用一次设备、新能源接入设备、典型接线方式、标准索引、规划默认口径、合规约束和 `pandapower` 标准类型。它不是一个单纯的静态表格仓库，而是把工程数据整理成可导入、可归一化、可建网、可校核的代码接口，方便在配网规划、台区改造、分布式新能源接入、潮流/短路仿真和设备容量筛选中复用。

English summary: Chinese distribution-grid engineering parameter library for equipment data, standards references, engineering checks, and pandapower integration.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%2B-green.svg)
![Version](https://img.shields.io/badge/Version-1.0.0-informational.svg)
![Models](https://img.shields.io/badge/Models-662-brightgreen.svg)
![Standards](https://img.shields.io/badge/Standards-49-orange.svg)

## 项目定位

`cnpower` 当前版本 `1.0.0` 的基础系统参数为 50Hz、100MVA 基准容量，内置电压等级包括 `0.4 / 10 / 35 / 110 / 220kV`。代码主入口集中在：

- `cnpower.equipment`：设备参数库；
- `cnpower.equipment.new_energy`：光伏、风机、储能和充电桩；
- `cnpower.engineering`：工程字段归一化、规划假设、合规约束和 pandapower 网络构建；
- `cnpower.pandapower_integration`：中国配网线路、变压器、三绕组变压器和熔断器标准类型；
- `cnpower.standards`：GB、GB/T、DL/T、NB/T、Q/GDW 等标准索引；
- `cnpower.topology` 和 `cnpower.validation`：典型接线方式与规划校验规则。

项目适合做：

- 中国 10kV/0.4kV 配电网设备参数查询和工程初筛；
- 基于 `pandapower` 的中文设备标准类型注册、潮流计算和短路计算准备；
- 规划方案中的变压器、线路、电缆、开关、无功补偿、新能源和充电负荷建模；
- 设备运行限值、短时耐受、开断能力、负载率、电压质量、保护配合等规则化校核；
- 为上层规划系统、资产台账系统或自动化建模脚本提供机器可读数据。

## 数据覆盖

当前设备库共 662 个模型，覆盖 12 类常用对象。

| 模块 | 数量 | 分类 |
|---|---:|---|
| 变压器 | 212 | 油浸式 72、干式 90、箱变 20、35kV 主变 13、110kV 主变 9、110kV 三绕组变 8 |
| 电缆 | 178 | 10kV 电缆 44、35kV 电缆 36、0.4kV 电缆 84、110kV 电缆 14 |
| 架空线路 | 82 | 10kV 架空绝缘线 16、0.4kV 架空绝缘线 30、裸导线 36 |
| 开关设备 | 61 | 开关柜 4、中压断路器 21、负荷开关 3、中压熔断器 3、低压断路器 25、重合器 2、分段器 3 |
| 无功补偿 | 29 | 中压电容器组 11、低压电容器组 9、SVG 9 |
| 保护配置 | 10 | 中压线路保护 6、变压器保护 4 |
| 互感器 | 32 | 中压 CT 15、低压 CT 13、中压 PT 4 |
| 避雷器 | 4 | 中压避雷器 3、低压避雷器 1 |
| 光伏 | 17 | 光伏组件 3、组串式逆变器 10、集中式逆变器 4 |
| 充电桩 | 9 | 交流慢充 3、直流快充 4、直流超充 2 |
| 储能 | 19 | 磷酸铁锂电池 8、铅碳电池 5、PCS 6 |
| 风机 | 9 | 小型分布式风机 5、中型分布式风机 4 |

机器可读清单见 [`cnpower_library_manifest.json`](cnpower_library_manifest.json)，运行参数维护规则见 [`docs/OPERATING_PARAMETERS.md`](docs/OPERATING_PARAMETERS.md)。

## 设备数据字段

不同设备模块保留了适配 `pandapower` 的扁平字段，也补充了面向工程校核的结构化字段。

| 设备 | 典型字段 |
|---|---|
| 变压器 | `sn_kva`、`vn_hv_kv`、`vn_lv_kv`、`vk_percent`、`vkr_percent`、`pfe_kw`、`i0_percent`、`rated_current_hv_a`、`rated_current_lv_a`、`loading_limits`、`thermal_model`、`energy_efficiency` |
| 电缆 | `r_ohm_per_km`、`x_ohm_per_km`、`c_nf_per_km`、`max_i_ka_air`、`max_i_ka_ground`、`max_i_ka_duct`、`ampacity_reference`、`derating_factors`、`thermal_limits`、`short_circuit_rating` |
| 架空线路 | `r_ohm_per_km`、`x_ohm_per_km`、`max_i_ka`、`rated_current_a`、`ampacity_reference`、`dynamic_line_rating`、`mechanical_limits`、`lifecycle` |
| 开关与熔断器 | `rated_voltage_kv`、`rated_current_a`、`rated_short_circuit_breaking_ka`、`rated_short_time_duration_s`、`short_time_withstand`、`endurance`、`time_current_curve`、`selection_guide` |
| 新能源与负荷 | `rated_power_kw`、`rated_voltage_v`、`power_factor`、`p_mw`、`q_mvar`、`sn_mva`、`soc_percent`、`max_e_mwh` |

新增运行字段会用 `source_type` 或 `field_source_types` 区分来源，例如 `standard_table`、`derived_formula`、`engineering_policy`、`manufacturer_typical_or_engineering_default` 和 `project_specific_required`。正式工程设计时，应结合现行标准、地方电网要求、厂家试验报告和项目边界复核。

## 安装

从 PyPI 安装：

```bash
pip install cnpower
```

需要 `pandapower` 建模能力时：

```bash
pip install "cnpower[pandapower]"
```

从源码安装：

```bash
git clone https://github.com/Gawg-AI/cnpower.git
cd cnpower
pip install -e ".[pandapower]"
```

开发和测试环境：

```bash
pip install -e ".[dev]"
python -m pytest
```

## 快速查询

```python
from cnpower.equipment import get_all_transformers, get_all_cables

transformers = get_all_transformers()
s13_630 = transformers["oil_immersed"]["S13-630/10"]

print(s13_630["sn_kva"])                 # 630
print(s13_630["rated_current_hv_a"])     # 36.4
print(s13_630["rated_current_lv_a"])     # 909.3
print(s13_630["thermal_model"]["standard"])

cables = get_all_cables()
cable = cables["mv_10kv"]["YJV22-3x70-10kV"]

print(cable["r_ohm_per_km"])
print(cable["max_i_ka_ground"] * 1000)
print(cable["ampacity_reference"]["laying_methods"])
```

顶层包也导出了主要数据入口：

```python
import cnpower

print(cnpower.__version__)
print(cnpower.VOLTAGE_LEVELS_KV)
print(cnpower.get_all_standards().keys())
```

## pandapower 标准类型

`cnpower.pandapower_integration` 可以向 pandapower 网络注册中国配网常用标准类型：

- 线路标准类型：260 个，来自电缆和架空线路；
- 两绕组变压器标准类型：184 个；
- 三绕组变压器标准类型：8 个；
- 熔断器标准类型：18 个。

```python
import pandapower as pp
from cnpower.pandapower_integration import add_chinese_std_types, list_chinese_std_types

net = pp.create_empty_network()
add_chinese_std_types(net)

hv_bus = pp.create_bus(net, vn_kv=10, name="10kV 母线")
lv_bus = pp.create_bus(net, vn_kv=0.4, name="0.4kV 母线")

pp.create_ext_grid(net, hv_bus, vm_pu=1.0)
pp.create_transformer(net, hv_bus, lv_bus, std_type="S13-630/10")
pp.create_load(net, lv_bus, p_mw=0.2, q_mvar=0.06)

pp.runpp(net)
print(net.converged)
print("S13-630/10" in list_chinese_std_types(net)["trafo"])
```

## 工程建网

`build_pandapower_net()` 可以从工程资产字典生成 pandapower 网络。它支持分组输入，也支持扁平 `assets` 列表；支持母线、外部电网、线路、电缆、架空线、两绕组变压器、三绕组变压器、负荷、光伏/风电等静态发电、储能、无功补偿、充电负荷和开关。

分组输入示例：

```python
from cnpower.engineering import build_pandapower_net

net = build_pandapower_net(
    {
        "buses": [
            {"id": "grid", "vn_kv": "10kV"},
            {"id": "load_bus", "rated_voltage_v": 400},
        ],
        "ext_grids": [
            {
                "bus": "grid",
                "vm_pu": 1.0,
                "s_sc_max_mva": 300,
                "s_sc_min_mva": 120,
                "rx_max": 0.1,
                "rx_min": 0.1,
            }
        ],
        "transformers": [
            {"id": "t1", "hv_bus": "grid", "lv_bus": "load_bus", "std_type": "S13-630/10"}
        ],
        "loads": [
            {"id": "load-1", "bus": "load_bus", "p_mw": 0.18, "q_mvar": 0.05}
        ],
    },
    run_powerflow=True,
)

print(net.converged)
print(net["cnpower_bus_lookup"])
```

参数化输入示例，不依赖预置 `std_type`：

```python
net = build_pandapower_net(
    {
        "buses": [
            {"id": "slack", "voltage_rating": "10kV"},
            {"id": "feeder", "rated_voltage_v": 10000},
        ],
        "ext_grids": [{"bus": "slack", "vm_pu": 1.0}],
        "lines": [
            {
                "id": "line-a",
                "from_bus": "slack",
                "to_bus": "feeder",
                "length_km": 0.8,
                "r_ohm_per_km": 0.268,
                "x_ohm_per_km": 0.09,
                "c_nf_per_km": 200,
                "max_i_ka_air": 0.21,
                "max_i_ka_ground": 0.185,
                "laying_method": "air",
            }
        ],
        "sgens": [
            {"id": "pv-1", "bus": "feeder", "equipment_type": "pv_inverter", "rated_power_kw": 80, "power_factor": 0.98}
        ],
    },
    run_powerflow=True,
)
```

扁平资产输入可以用 `class` 或 `equipment_type` 自动路由：

```python
net = build_pandapower_net(
    {
        "assets": [
            {"id": "grid", "class": "busbar", "vn_kv": 10.0},
            {"id": "feeder", "class": "busbar", "vn_kv": 10.0},
            {"id": "source", "class": "source_grid", "bus": "grid", "vm_pu": 1.0},
            {"id": "line-a", "class": "line", "from_bus": "grid", "to_bus": "feeder", "length_km": 1.0, "std_type": "YJV22-3x70-10kV"},
            {"id": "disc-a", "class": "disconnector", "bus": "grid", "element": "line-a", "element_type": "line", "closed": True},
            {"id": "load-a", "class": "load", "bus": "feeder", "p_mw": 0.05, "q_mvar": 0.01},
        ]
    },
    run_powerflow=True,
)
```

构建后的网络会保存 `cnpower_bus_lookup` 和 `cnpower_element_lookup`，便于把工程资产 ID 映射回 pandapower 表索引。

## 归一化与校核

`normalize_equipment()` 会把工程输入转换成统一字段，例如电压单位解析、容量单位转换、负荷有功/无功派生、电缆敷设方式电流选择、变压器分侧额定电流派生等。

```python
from cnpower.engineering import normalize_equipment

trafo = normalize_equipment(
    "transformer",
    {"sn_kva": 630, "vn_hv_kv": 10, "vn_lv_kv": 0.4},
    context={"current_side": "lv"},
)

print(trafo["equipment_type"])      # transformer_2w
print(trafo["sn_mva"])              # 0.63
print(trafo["rated_current_a"])     # 909.3
```

```python
charger = normalize_equipment(
    "ev_charger",
    {"rated_power_kw": 14, "rated_voltage_v": 380, "power_factor": 0.95},
)

print(charger["p_mw"])       # 0.014
print(charger["q_mvar"])     # 由功率因数派生
```

`check_equipment_compliance()` 根据设备字段和计算结果执行规则化检查：

```python
from cnpower.engineering import check_equipment_compliance

result = check_equipment_compliance(
    "transformer",
    {
        "sn_kva": 630,
        "vn_hv_kv": 10,
        "vn_lv_kv": 0.4,
        "rated_current_a": 36.4,
        "normal_loading_limit_percent": 80,
    },
    {
        "operating_voltage_kv": 12,
        "max_current_a": 40,
        "loading_percent": 85,
    },
)

print(result["summary"])
print([item for item in result["findings"] if not item["passed"]])
```

合规约束库覆盖电源、母线、变压器、箱变、电缆、架空线、开关柜、断路器、负荷开关、熔断器、重合器、分段器、低压断路器、环网柜、无功补偿、互感器、避雷器、负荷、光伏、风机、储能和充电桩等类型。

## 标准、接线和规划规则

标准索引包含 49 项标准或规范参考，可通过 `get_all_standards()` 获取。常见条目包括：

| 标准 | 用途 |
|---|---|
| `GB/T 6451-2023` | 油浸式电力变压器技术参数和要求 |
| `GB/T 10228-2023` | 干式电力变压器技术参数和要求 |
| `GB/T 1094.7-2024` | 油浸式变压器负载导则与老化计算参考 |
| `GB/T 1094.11-2022` | 干式变压器技术要求 |
| `GB/T 1094.12-2013` | 干式变压器负载导则 |
| `GB 20052-2024` | 电力变压器能效限定值及能效等级 |
| `GB/T 12706.1~3-2020` | 1kV 到 35kV 挤包绝缘电力电缆 |
| `GB/T 1179-2017` | 圆线同心绞架空导线 |
| `GB/T 1984-2024` | 高压交流断路器 |
| `GB/T 11022-2020` | 高压开关设备和控制设备标准的共用技术要求 |
| `GB/T 3906-2020` | 3.6kV 到 40.5kV 金属封闭开关设备 |
| `GB/T 15166.2-2023` | 高压交流熔断器限流熔断器 |
| `GB/T 45418-2025` | 配电网通用技术导则 |

典型接线方式入口：

```python
from cnpower.topology import get_all_connection_modes

modes = get_all_connection_modes()
print(modes.keys())  # mv_10kv_overhead, mv_10kv_cable, lv_04kv
```

规划假设入口：

```python
from cnpower.engineering import get_planning_assumption_library

planning = get_planning_assumption_library()
print(planning["voltage_limits"]["normal_operation"])
print(planning["planning_scenarios"].keys())
```

校验规则入口：

```python
from cnpower.validation import get_all_validation_rules

rules = get_all_validation_rules()
print(rules.keys())
```

内置校验规则分类包括电压质量、N-1 安全、短路、电气设备选型、可靠性和新能源接入。

## 短路计算入口

`cnpower` 不替代 pandapower 的短路算法，但会为 pandapower 网络注册可用的中文设备类型，并支持录入上级电网短路容量字段。示例：

```python
import pandapower.shortcircuit as sc
from cnpower.engineering import build_pandapower_net

net = build_pandapower_net(
    {
        "buses": [
            {"id": "grid", "vn_kv": 10.0},
            {"id": "feeder", "vn_kv": 10.0},
        ],
        "ext_grids": [
            {
                "bus": "grid",
                "vm_pu": 1.0,
                "s_sc_max_mva": 300,
                "s_sc_min_mva": 120,
                "rx_max": 0.1,
                "rx_min": 0.1,
                "r0x0_max": 0.1,
                "x0x_max": 1.0,
            }
        ],
        "lines": [
            {"from_bus": "grid", "to_bus": "feeder", "length_km": 1.0, "std_type": "YJV22-3x70-10kV"}
        ],
    }
)

sc.calc_sc(net, fault="3ph", case="max", ip=True, ith=True)
print(net.res_bus_sc[["ikss_ka", "ip_ka", "ith_ka"]])
```

## 项目结构

```text
cnpower/
  equipment/                 变压器、电缆、架空线、开关、补偿、保护、互感器、避雷器
  equipment/new_energy/      光伏、风机、储能、充电桩
  engineering/               资产 schema、归一化、合规约束、规划假设、pandapower 建网
  pandapower_integration/    中国配网 pandapower 标准类型注册
  standards/                 标准索引
  topology/                  典型接线方式
  validation/                规划与运行校验规则
docs/
  OPERATING_PARAMETERS.md    运行参数字段和来源类型维护说明
examples/
  pandapower_network_builder.py
tests/
  test_*.py                  归一化、运行参数和 pandapower 集成测试
```

## 验证

本地回归测试：

```bash
python -m pytest
```

项目完整性校验：

```bash
python verify_fixes.py
```

当前代码的预期结果：

- `python -m pytest`：21 passed；
- `python verify_fixes.py`：756 PASS, 0 FAIL；
- GitHub Actions：Python 3.10 和 Python 3.12 上运行 pytest。

## 维护建议

新增或修改设备数据时，建议同步检查：

- 是否保留 `pandapower` 所需字段，例如线路 R/X/C、最大电流、变压器短路电压和空载损耗；
- 是否为运行参数标注 `source_type` 或 `field_source_types`；
- 项目特定字段是否使用 `None` 或说明文本，而不是伪装成标准表值；
- 归一化逻辑是否能处理常见单位写法，例如 `10kV`、`400V`、`6/10kV`；
- 合规约束库和设备库分类映射是否需要同步更新；
- `tests/test_operating_parameters.py`、`tests/test_engineering_normalization.py` 和 `tests/test_pandapower_integration.py` 是否覆盖新增行为。

## 许可证与署名

本项目采用带署名要求的 MIT License，详见 [LICENSE](LICENSE)。

在工程项目、论文或衍生作品中使用本库时，请保留如下数据来源说明：

```text
Data Source: cnpower - https://github.com/Gawg-AI/cnpower
```

## 免责声明

本库设备参数来自公开标准、工程常用口径和典型参数整理，仅供规划研究、仿真建模和工程初步校核参考。正式工程设计应以现行标准、当地电网公司要求、厂家试验报告、项目设计条件和审查意见为准。对 `engineering_policy`、`manufacturer_typical_or_engineering_default` 和 `project_specific_required` 类型字段，应在项目落地前进行专项复核。

## 更新记录

| 日期 | 版本 | 摘要 |
|---|---|---|
| 2026-06-07 | v2026.06.07-readme-code-scan | 根据当前代码重新扫描项目能力，丰富 README 的数据覆盖、pandapower 接入、工程建网、归一化、合规校核和维护说明。 |
| 2026-06-05 | v2026.06.05-manifest-docs-cleanup | 删除 `pyproject.toml`，恢复 README 作为主描述页，并将 JSON 调整为机器可读工程库清单。 |
| 2026-06-05 | v2026.06.05-chinese-first-docs | 将 README 和项目画像说明调整为中文主导，保留少量必要英文。 |
| 2026-06-05 | v2026.06.05-readme-json-refresh | 重写 README，补充运行参数版本说明，并新增机器可读项目画像 JSON。 |
| 2026-06-05 | v2026.06.05-operating-parameters | 新增变压器额定电流派生、动态负载元数据、`GB 20052-2024` 引用、电缆/架空线载流工况、开关/熔断器运行限值、测试和文档。 |
| 2026-06-03 | v2026.06.03-docs | 将升级记录移动到 README 底部，并改为单行追加记录。 |
| 2026-06-03 | v2026.06.03-builder-followups | 强化 `build_pandapower_net` 资产映射和示例。 |
| 2026-06-03 | v2026.06.03-parameterized-assets | 增加参数化工程资产对 pandapower 建模的支持。 |
