# 运行参数升级维护指南

本文档说明 `cnpower` 中新增的运行、规划和寿命周期参数，供维护者在扩展设备库时使用。维护目标是把国标/行标表值、公式派生值、工程策略默认值、厂家典型值和项目占位值清楚地区分开，避免用户误把工程默认值当作强制标准限值。

English note: field names and API names remain in English for code compatibility.

## 适用范围

本次运行参数升级主要覆盖三类工程数据：

1. 变压器运行电流、负载率、热模型、能效等级和寿命元数据；
2. 电缆与架空线路载流量参考条件、折减元数据、热稳定限值、短路能量和寿命周期元数据；
3. 开关设备、断路器、负荷开关、重合器、分段器、熔断器和保护配置的运行限值、耐受能力、寿命、内部燃弧占位和时间-电流曲线元数据。

既有扁平字段继续保留，用于兼容已有用户和 `pandapower` 接入；新增结构化字段均为增量字段。

## 来源类型

新增字段应通过 `field_source_types` 或嵌套的 `source_type` 标明来源：

| 来源类型 | 含义 |
|---|---|
| `standard_table` | 标准表格中的直接数值 |
| `derived_formula` | 由铭牌参数或标准公式计算，例如 `S/(sqrt(3)*U)` |
| `standard_reference` | 标准给出方法、要求或约束，但没有具体型号表值 |
| `standard_reference_and_engineering_default` | 有标准依据的校核口径，当前库先采用保守工程默认值 |
| `engineering_policy` | 规划口径、电网公司策略或项目策略默认值 |
| `manufacturer_typical_or_engineering_default` | 厂家样本典型值或工程占位值 |
| `project_specific_required` | 必须由具体项目、现场条件、电网要求或厂家资料补充 |

不得把 `engineering_policy` 直接表述为 GB/GB/T 强制限值。

## 变压器

`cnpower.equipment.transformers` 会在基础表构建完成后补充变压器运行字段。

示例：

```python
from cnpower.equipment.transformers import get_all_transformers

s13 = get_all_transformers()["oil_immersed"]["S13-630/10"]

assert s13["rated_current_hv_a"] == 36.4
assert s13["rated_current_lv_a"] == 909.3
assert s13["rated_current"]["method"] == "S/(sqrt(3)*U)"
```

关键字段：

| 字段 | 含义 |
|---|---|
| `rated_current_hv_a`, `rated_current_mv_a`, `rated_current_lv_a` | 按容量和电压派生的分侧额定电流 |
| `rated_current` | 包含分侧电流、计算方法和来源类型的结构化字段 |
| `normal_loading_limit_percent` | 规划默认正常负载率限值 |
| `economic_loading_range_percent` | 规划比选用的典型经济负载率区间 |
| `n1_loading_limit_percent` | N-1 或检修转供场景下的短时规划限值 |
| `emergency_loading_limit_percent` | 应急短时默认值，正式使用前需做热校核 |
| `loading_limits` | 包含持续时间和来源类型的结构化负载策略 |
| `thermal_model` | 负载导则、温度阈值和老化模型参考 |
| `energy_efficiency` | 当前能效标准和能效等级占位 |
| `design_life_years` | 寿命周期规划默认值 |

主要标准和参考：

- 油浸式参数表：`GB/T 6451-2023`
- 干式参数表：`GB/T 10228-2023`
- 油浸式负载与老化：`GB/T 1094.7-2024`
- 干式变压器本体和温升要求：`GB/T 1094.11-2022`
- 干式变压器负载导则：`GB/T 1094.12-2013`
- 变压器选用：`GB/T 17468-2019`
- 能效等级：`GB 20052-2024`

### 电流侧选择

`normalize_equipment()` 在输入数据足够时会派生额定电流。通用字段 `rated_current_a` 默认采用高压侧；如果要校核低压侧电流，应传入 `context={"current_side": "lv"}`。

```python
from cnpower.engineering import normalize_equipment

trafo = normalize_equipment(
    "transformer",
    {"sn_kva": 630, "vn_hv_kv": 10, "vn_lv_kv": 0.4},
    context={"current_side": "lv"},
)

assert trafo["rated_current_a"] == 909.3
```

## 电缆

电缆条目除 `pandapower` 兼容的 R/X/C 和 `max_i_ka_*` 字段外，还补充了运行工况字段。

关键字段：

| 字段 | 含义 |
|---|---|
| `ampacity_reference` | 空气、土壤、直埋、间距和敷设方式等载流量参考条件 |
| `derating_factors` | 温度、并列回路、土壤热阻、敷设深度、谐波等折减类别 |
| `thermal_limits` | 正常、应急和短路导体温度限值 |
| `short_circuit_i2t_ka2s` | 由 1s 短路电流计算的 `I^2*t` |
| `short_circuit_rating` | 短路电流、持续时间和能量元数据 |
| `lifecycle` | 设计寿命和过载小时策略 |

示例：

```python
from cnpower.equipment.cables import get_all_cables

cable = get_all_cables()["mv_10kv"]["YJV22-3x70-10kV"]
ampacity_ground_a = cable["max_i_ka_ground"] * 1000
normal_temp_c = cable["thermal_limits"]["max_conductor_temp_normal_c"]
```

既有 `max_i_ka_air`、`max_i_ka_ground` 和 `max_i_ka_duct` 仍是 `pandapower` 接入和归一化逻辑使用的兼容字段。

## 架空线路

架空线路条目增加了动态载流和机械设计相关的规划元数据。

关键字段：

| 字段 | 含义 |
|---|---|
| `rated_current_a` | 由 `max_i_ka` 派生的额定电流 |
| `ampacity_reference` | 环境温度、风速、日照、发射率和吸收率等参考条件 |
| `dynamic_line_rating` | 热平衡模型元数据 |
| `mechanical_limits` | 档距、覆冰、风速、净距和弧垂等项目占位字段 |
| `lifecycle` | 设计寿命、巡检周期、故障率和修复时间占位字段 |

使用 `mechanical_limits` 做净距或弧垂校核前，必须结合具体线路路径、气象条件和设计资料补齐。

## 开关设备与熔断器

开关设备条目在 `cnpower.equipment.switchgear` 中增强。

关键字段：

| 字段 | 含义 |
|---|---|
| `rated_current_max_a` | 基础字段为列表时可选额定电流的最大值 |
| `rated_short_time_duration_s` | 与短时耐受电流配套的持续时间 |
| `short_time_withstand` | 短时耐受电流、持续时间和 `I^2*t` 元数据 |
| `internal_arc_class` | 开关柜内部燃弧等级占位 |
| `endurance` | 机械寿命、电气寿命和维护元数据 |
| `time_current_curve` | 熔断器曲线元数据，保留既有曲线点 |
| `selection_guide` | 熔断器与变压器回路选型参考 |

主要标准和参考：

- 中压断路器：`GB/T 1984-2024`
- 高压开关设备共用要求：`GB/T 11022-2020`
- 中压金属封闭开关设备：`GB/T 3906-2020`
- 高压限流熔断器：`GB/T 15166.2-2023`
- 变压器回路熔断器选用：`GB/T 15166.6-2023`
- 低压断路器：`GB/T 14048.2-2020`

## 保护配置

保护配置新增以下结构化元数据：

- `setting_metadata`
- `fuse_coordination`
- `thermal_trip_model`

基础保护说明仍以描述性字段为主。实际定值仍需结合短路电流计算、最大负荷电流、下级保护曲线和电网选择性要求确定。

## 新增设备维护规则

新增设备型号时：

1. 保留既有兼容字段，尤其是 `pandapower` 需要的字段；
2. 补充运行字段，或让模块辅助函数自动派生；
3. 为每个规划字段或动态字段标明来源类型；
4. 项目特定值应设为 `None`，并写清楚需要由项目补充；
5. 在 `tests/test_operating_parameters.py` 中增加聚焦测试；
6. 运行 `python -m pytest`。

## 合并前检查清单

参数更新合并前，应至少确认：

- 变压器各侧额定电流派生正确；
- 能效元数据使用 `GB 20052-2024`；
- 电缆和架空线路的载流量参考条件明确；
- 短时耐受电流始终带有持续时间；
- 熔断器曲线说明点值是电流倍数还是安培值；
- 规划默认值标注为 `engineering_policy`；
- 项目特定字段没有被静默当作标准数值使用。
