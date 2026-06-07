# cnpower

面向中国配电网规划、仿真建模、设备选型和工程校核的 Python 工程参数库。

`cnpower` 把常用配电设备参数、标准索引、典型接线方式、工程字段归一化、合规约束和 `pandapower` 建网能力整理成稳定接口。它适合作为配网规划系统、资产台账转换、分布式电源接入分析、仿真建模脚本和初步工程校核工具的参数底座。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%2B-green.svg)
![Version](https://img.shields.io/badge/Version-1.0.0-informational.svg)
![Models](https://img.shields.io/badge/Models-662-brightgreen.svg)
![Standards](https://img.shields.io/badge/Standards-49-orange.svg)

English summary: `cnpower` is a Chinese distribution-grid engineering parameter library for equipment data, standards references, validation rules, normalization, compliance checks, and pandapower integration.

## 适合做什么

- 查询 10kV/0.4kV 配网常用设备参数。
- 将工程资产字段归一化为 `p_mw`、`q_mvar`、`sn_mva`、`rated_current_a` 等统一字段。
- 向 `pandapower` 注册中文线路、变压器、三绕组变压器和熔断器标准类型。
- 从工程资产字典构建可运行的 `pandapower` 网络。
- 对设备选型、电压质量、短路、N-1、可靠性、新能源接入等规则做初步校核。
- 为上层规划平台、建模流水线或自动化引擎提供机器可读数据。

不建议直接替代：

- 正式施工图设计。
- 厂家试验报告。
- 地方电网公司审查要求。
- 完整潮流、短路、保护整定或暂态仿真引擎。

## 当前覆盖

基础参数：

- 版本：`1.0.0`
- 日期：`2026-06-07`
- Python：`>=3.10`
- 系统频率：`50Hz`
- 基准容量：`BASE_MVA = 100.0`
- 电压等级：`0.4 / 10 / 35 / 110 / 220kV`

设备模型共 662 个：

| 模块 | 数量 | 分类 |
|---|---:|---|
| 变压器 | 212 | 油浸式、干式、箱变、35kV 主变、110kV 主变、110kV 三绕组变 |
| 电缆 | 178 | 10kV、35kV、0.4kV、110kV |
| 架空线路 | 82 | 10kV 架空绝缘线、0.4kV 架空绝缘线、裸导线 |
| 开关设备 | 61 | 开关柜、断路器、负荷开关、熔断器、重合器、分段器 |
| 无功补偿 | 29 | 中压电容器、低压电容器、SVG |
| 保护配置 | 10 | 中压线路保护、变压器保护 |
| 互感器 | 32 | 中压 CT、低压 CT、中压 PT |
| 避雷器 | 4 | 中压、低压避雷器 |
| 光伏 | 17 | 光伏组件、组串式逆变器、集中式逆变器 |
| 充电桩 | 9 | 交流慢充、直流快充、直流超充 |
| 储能 | 19 | 磷酸铁锂电池、铅碳电池、PCS |
| 风机 | 9 | 小型分布式风机、中型分布式风机 |

更多机器可读信息见 [`cnpower_library_manifest.json`](cnpower_library_manifest.json)。项目交接和使用说明见 [`docs/cnpower_project_guide.md`](docs/cnpower_project_guide.md)。

## 安装

基础安装：

```bash
pip install cnpower
```

需要 `pandapower` 建模能力时：

```bash
pip install "cnpower[pandapower]"
```

源码开发：

```bash
git clone https://github.com/Gawg-AI/cnpower.git
cd cnpower
pip install -e ".[dev]"
python -m pytest -q
python verify_fixes.py
```

## 快速开始

### 查询设备参数

```python
from cnpower.equipment import get_all_transformers

transformers = get_all_transformers()
trafo = transformers["oil_immersed"]["S13-630/10"]

print(trafo["sn_kva"])
print(trafo["rated_current_hv_a"])
print(trafo["rated_current_lv_a"])
print(trafo["thermal_model"]["standard"])
```

### 归一化工程字段

```python
from cnpower.engineering import normalize_equipment

charger = normalize_equipment(
    "ev_charger",
    {"rated_power_kw": 14, "rated_voltage_v": 380, "power_factor": 0.95},
)

print(charger["p_mw"])
print(charger["q_mvar"])
print(charger["rated_voltage_kv"])
```

### 做设备合规检查

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
        "operating_voltage_kv": 10,
        "max_current_a": 35,
        "loading_percent": 70,
    },
)

print(result["summary"])
print(result["findings"])
```

### 注册 pandapower 标准类型

```python
import pandapower as pp
from cnpower.pandapower_integration import add_chinese_std_types, list_chinese_std_types

net = pp.create_empty_network()
add_chinese_std_types(net)

print("S13-630/10" in net.std_types["trafo"])
print(list_chinese_std_types(net).keys())
```

### 从工程资产字典建网

```python
from cnpower.engineering import build_pandapower_net

net = build_pandapower_net(
    {
        "buses": [
            {"id": "grid", "vn_kv": 10.0},
            {"id": "load_bus", "vn_kv": 0.4},
        ],
        "ext_grids": [{"bus": "grid", "vm_pu": 1.0}],
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

## 主要入口

| 入口 | 说明 |
|---|---|
| `cnpower.equipment` | 变压器、电缆、架空线、开关、无功补偿、保护、互感器、避雷器 |
| `cnpower.equipment.new_energy` | 光伏、风机、储能、充电桩 |
| `cnpower.engineering.normalize_equipment` | 工程字段归一化 |
| `cnpower.engineering.check_equipment_compliance` | 设备合规检查 |
| `cnpower.engineering.build_pandapower_net` | 从工程资产字典构建 pandapower 网络 |
| `cnpower.pandapower_integration.add_chinese_std_types` | 注册中文 pandapower 标准类型 |
| `cnpower.standards.get_all_standards` | 标准索引 |
| `cnpower.topology.get_all_connection_modes` | 典型接线方式 |
| `cnpower.validation.get_all_validation_rules` | 规划与运行校验规则 |

## 标准与规则

标准索引包含 49 项标准或规范引用。常见条目包括：

- `GB/T 6451-2023`：油浸式电力变压器技术参数和要求。
- `GB/T 10228-2023`：干式电力变压器技术参数和要求。
- `GB/T 1094.1-2013`：电力变压器总则。
- `GB/T 12706.1~3-2020`：1kV 到 35kV 挤包绝缘电力电缆。
- `GB/T 1179-2017`：圆线同心绞架空导线。
- `GB/T 1984-2024`：高压交流断路器。
- `GB/T 15166.2-2023`：高压交流熔断器。
- `GB/T 18487.1-2023`：电动车导电充电系统。
- `GB/T 34131-2023`：电化学储能站接入电网。
- `GB/T 45418-2025`：配电网通用技术导则。

校验规则覆盖：

- 电压质量：电压偏差、电压波动、闪变、谐波、三相不平衡。
- N-1 安全与典型接线模式。
- 短路电流与电缆热稳定。
- 设备选型：变压器、导体、断路器等。
- 可靠性：SAIDI、SAIFI。
- 新能源接入：光伏、储能、充电设施和电能质量。

## 项目结构

```text
cnpower/
  equipment/                 设备参数库
  equipment/new_energy/      光伏、风机、储能、充电桩
  engineering/               归一化、建网、合规检查、规划假设
  pandapower_integration/    pandapower 中文标准类型
  standards/                 标准索引
  topology/                  典型接线方式
  validation/                校验规则
docs/
  cnpower_project_guide.md   项目交接与使用说明
  OPERATING_PARAMETERS.md    运行参数字段和来源说明
examples/
  pandapower_network_builder.py
tests/
  test_*.py
```

## 验证

```bash
python -m pytest -q
python verify_fixes.py
```

当前期望：

- `python -m pytest -q`：全部测试通过。
- `python verify_fixes.py`：`756 PASS, 0 FAIL`。

## 维护原则

- 新增设备数据时，同步检查 `pandapower` 必需字段、工程运行字段、标准来源和测试覆盖。
- 新增标准条目时，`code` 必须唯一，`related_rules` 必须指向真实存在的规则 ID。
- 对外程序优先使用包级入口，不直接依赖内部 helper。
- `source_type` 为工程默认或项目特定的字段，正式工程落地前必须复核。
- 修改归一化、合规检查、标准索引或建网逻辑时，应补充回归测试。

## 文档

- [`docs/cnpower_project_guide.md`](docs/cnpower_project_guide.md)：完整项目说明、模块关系、使用流程、维护清单。
- [`docs/OPERATING_PARAMETERS.md`](docs/OPERATING_PARAMETERS.md)：运行字段、来源类型和维护边界。
- [`cnpower_library_manifest.json`](cnpower_library_manifest.json)：机器可读项目清单。

## 许可证与署名

本项目采用带署名要求的 MIT License，详见 [LICENSE](LICENSE)。

在工程项目、论文或衍生作品中使用本库时，请保留如下数据来源说明：

```text
Data Source: cnpower - https://github.com/Gawg-AI/cnpower
```

## 免责声明

本库设备参数来自公开标准、工程常用口径和典型参数整理，仅供规划研究、仿真建模和工程初步校核参考。正式工程设计应以现行标准、当地电网公司要求、厂家试验报告、项目设计条件和审查意见为准。
