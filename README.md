# cnpower

面向中国配电网规划、潮流计算、设备选型和工程校验的 10kV/0.4kV 工程参数库。

`cnpower` 以中文用户和国内配电工程场景为主要对象，提供常用电力设备参数、典型接线方式、国标/行标/企标参考、工程归一化、合规校核和 `pandapower` 标准类型接入。当前版本在静态铭牌参数基础上，补充了变压器额定电流派生、线路/电缆载流工况、开关设备短时耐受、保护配合、寿命与运行策略等工程运行参量。

English summary: Chinese distribution-grid engineering parameter library for planning and simulation.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%2B-green.svg)
![Models](https://img.shields.io/badge/Models-662-brightgreen.svg)
![Standards](https://img.shields.io/badge/Standards-GB%2FGB--T%202025-orange.svg)

## 项目概览

README.md 是本项目的主要说明页和包长描述来源。仓库中的 JSON 文件只作为机器可读的工程库清单使用，不作为项目介绍页或摘要页。

当前参数库共包含 662 个设备模型，覆盖变压器、电缆、架空线、开关设备、无功补偿、保护配置、互感器、避雷器、光伏、充电桩、储能和风机等配网规划常用对象。

相比只提供静态设备表的工具，本项目进一步补充了面向潮流计算、短路校核和配网规划的数据层：

- 变压器：高压侧/中压侧/低压侧额定电流派生、负载率限值、热模型与寿命元数据、`GB 20052-2024` 能效等级参考；
- 电缆与架空线：载流量参考敷设条件、折减系数、热稳定限值、短路 `I^2t`、动态载流能力和寿命周期字段；
- 开关、断路器、熔断器与保护：额定短时耐受持续时间、开断/耐受能力、机械/电气寿命、内部燃弧占位、时间-电流曲线和保护配合元数据。

机器可读工程库清单见 [`cnpower_library_manifest.json`](cnpower_library_manifest.json)。

## 模型覆盖

| 模块 | 数量 | 覆盖内容 |
|---|---:|---|
| 变压器 | 212 | 油浸式、干式、箱变、35kV/110kV 主变、110kV 三绕组变压器 |
| 电缆 | 178 | 10kV、35kV、0.4kV、110kV 电力电缆 |
| 架空线路 | 82 | 10kV 架空绝缘线、0.4kV 架空绝缘线、裸导线 |
| 开关设备 | 61 | 开关柜、中压/低压断路器、负荷开关、中压熔断器、重合器、分段器 |
| 无功补偿 | 29 | 中压/低压电容器组、SVG |
| 保护配置 | 10 | 线路保护、变压器保护 |
| 互感器 | 32 | 中压/低压电流互感器、中压电压互感器 |
| 避雷器 | 4 | 中压和低压避雷器 |
| 光伏 | 17 | 光伏组件、组串式逆变器、集中式逆变器 |
| 充电桩 | 9 | 交流慢充、直流快充、直流超充 |
| 储能 | 19 | 磷酸铁锂电池、铅碳电池、PCS |
| 风机 | 9 | 小型和中型分布式风机 |

合计：662 个模型。

## 标准索引

当前标准索引包含 49 项国标、行标、企标和规划参考。主要参考包括：

| 标准 | 用途 |
|---|---|
| `GB/T 6451-2023` | 油浸式电力变压器技术参数 |
| `GB/T 10228-2023` | 干式电力变压器技术参数 |
| `GB/T 1094.7-2024` | 油浸式变压器负载导则与老化计算参考 |
| `GB/T 1094.11-2022` | 干式变压器技术要求 |
| `GB/T 1094.12-2013` | 干式变压器负载导则 |
| `GB/T 17468-2019` | 电力变压器选用导则 |
| `GB 20052-2024` | 电力变压器能效限定值及能效等级 |
| `GB/T 12706.1~3-2020` | 1kV 到 35kV 挤包绝缘电力电缆 |
| `GB/T 1179-2017` | 圆线同心绞架空导线 |
| `GB/T 14049-2008` | 10kV 架空绝缘电缆 |
| `GB/T 12527-2008` | 额定电压 1kV 及以下架空绝缘电缆 |
| `GB/T 1984-2024` | 高压交流断路器 |
| `GB/T 11022-2020` | 高压开关设备和控制设备标准的共用技术要求 |
| `GB/T 3906-2020` | 3.6kV 到 40.5kV 金属封闭开关设备 |
| `GB/T 15166.2-2023` | 高压交流熔断器限流熔断器 |
| `GB/T 15166.6-2023` | 变压器回路熔断件选用导则 |
| `GB/T 45418-2025` | 配电网通用技术导则 |

完整索引可通过 `cnpower.standards.get_all_standards()` 获取。

## 安装

```bash
pip install cnpower
```

安装时同时启用 `pandapower` 接入：

```bash
pip install "cnpower[pandapower]"
```

从源码安装：

```bash
git clone https://github.com/Gawg-AI/cnpower.git
cd cnpower
pip install -e ".[pandapower]"
```

## 快速开始

```python
from cnpower.equipment import get_all_transformers, get_all_cables

transformers = get_all_transformers()
s13_630 = transformers["oil_immersed"]["S13-630/10"]

print(s13_630["sn_kva"])                 # 630
print(s13_630["rated_current_hv_a"])     # 36.4
print(s13_630["rated_current_lv_a"])     # 909.3
print(s13_630["thermal_model"]["standard"])

cables = get_all_cables()
yjv_70 = cables["mv_10kv"]["YJV22-3x70-10kV"]

print(yjv_70["r_ohm_per_km"])
print(yjv_70["max_i_ka_ground"] * 1000)
print(yjv_70["ampacity_reference"]["laying_methods"])
```

## pandapower 接入

```python
import pandapower as pp
from cnpower.pandapower_integration import add_chinese_std_types

net = pp.create_empty_network()
add_chinese_std_types(net)

hv_bus = pp.create_bus(net, vn_kv=10, name="10kV 母线")
lv_bus = pp.create_bus(net, vn_kv=0.4, name="0.4kV 母线")
from_bus = pp.create_bus(net, vn_kv=10, name="线路首端")
to_bus = pp.create_bus(net, vn_kv=10, name="线路末端")

pp.create_transformer(net, hv_bus, lv_bus, std_type="S13-630/10")
pp.create_line(net, from_bus, to_bus, length_km=2.0, std_type="YJV22-3x70-10kV")
pp.runpp(net)
```

## 工程归一化与校核

`cnpower.engineering.normalize_equipment()` 可基于已有设备记录派生通用字段。例如，变压器可根据容量和电压派生指定侧额定电流：

```python
from cnpower.engineering import normalize_equipment

trafo = normalize_equipment(
    "transformer",
    {"sn_kva": 630, "vn_hv_kv": 10, "vn_lv_kv": 0.4},
    context={"current_side": "lv"},
)

print(trafo["rated_current_a"])  # 909.3
```

`cnpower.engineering.check_equipment_compliance()` 可将设备限值与潮流结果、短路结果或规划边界进行比较，用于工程校核。

## 运行参数维护说明

详细字段定义、来源类型和维护规则见 [`docs/OPERATING_PARAMETERS.md`](docs/OPERATING_PARAMETERS.md)。

字段来源类型用于区分数据可信度和使用边界：

- `standard_table`：来自标准表格的直接数值；
- `derived_formula`：由铭牌参数或标准公式派生；
- `standard_reference`：有标准依据的方法、要求或引用；
- `standard_reference_and_engineering_default`：有标准依据，但当前库采用保守工程默认值；
- `engineering_policy`：规划口径或工程策略默认值；
- `manufacturer_typical_or_engineering_default`：厂家样本典型值或工程占位值；
- `project_specific_required`：必须由具体项目、厂家资料或现场条件补充。

工程默认值不能直接等同于 GB/GB/T 的强制限值；在正式设计中应结合现行标准、地方电网要求、厂家试验报告和项目边界复核。

## 项目结构

```text
cnpower/
  equipment/                 设备参数库
  equipment/new_energy/      光伏、充电、储能、风电
  engineering/               归一化、合规校核、网络构建
  pandapower_integration/    中国配网 pandapower 标准类型
  standards/                 GB/GB-T/DL/T/NB/T/Q/GDW 标准索引
  topology/                  典型接线方式
  validation/                电能质量与规划校验规则
docs/
  OPERATING_PARAMETERS.md    运行参数维护说明
tests/
  test_*.py                  回归测试与集成测试
```

## 数据格式

设备库采用 `dict[str, dict]` 结构，型号名称作为键：

```python
{
    "S13-630/10": {
        "sn_kva": 630,
        "vn_hv_kv": 10,
        "vn_lv_kv": 0.4,
        "vk_percent": 4.5,
        "vkr_percent": 0.98,
        "pfe_kw": 0.65,
        "i0_percent": 0.6,
        "rated_current_hv_a": 36.4,
        "rated_current_lv_a": 909.3,
        "loading_limits": {...},
        "thermal_model": {...},
        "energy_efficiency": {...},
    }
}
```

## 验证

运行回归测试：

```bash
python -m pytest
```

运行项目校验脚本：

```bash
python verify_fixes.py
```

当前本地预期结果：

- `python -m pytest`：21 passed
- `python verify_fixes.py`：756 PASS, 0 FAIL

GitHub Actions 会在 Python 3.10 和 3.12 上运行 pytest。

## 贡献

贡献说明见 [CONTRIBUTING.md](CONTRIBUTING.md)。新增运行、规划、动态限值和寿命周期字段时，应补充 `source_type` 或 `field_source_types` 元数据，帮助用户区分标准表值、公式派生值、工程策略默认值、厂家典型值和项目占位值。

## 许可证与署名

本项目采用带署名要求的 MIT License，详见 [LICENSE](LICENSE)。

在工程项目、论文或衍生作品中使用本库时，请保留如下数据来源说明：

```text
Data Source: cnpower - https://github.com/Gawg-AI/cnpower
```

## 免责声明

本库设备参数来自公开标准、工程常用口径和典型参数整理，仅供规划研究、仿真建模和工程初步校核参考。正式工程设计应以现行标准、当地电网公司要求、厂家试验报告、项目设计条件和审查意见为准。

## 更新记录

| 日期 | 版本 | 摘要 |
|---|---|---|
| 2026-06-05 | v2026.06.05-manifest-docs-cleanup | 删除 `pyproject.toml`，恢复 README 作为主描述页，并将 JSON 调整为机器可读工程库清单。 |
| 2026-06-05 | v2026.06.05-chinese-first-docs | 将 README 和项目画像说明调整为中文主导，保留少量必要英文。 |
| 2026-06-05 | v2026.06.05-readme-json-refresh | 重写 README，补充运行参数版本说明，并新增机器可读项目画像 JSON。 |
| 2026-06-05 | v2026.06.05-operating-parameters | 新增变压器额定电流派生、动态负载元数据、`GB 20052-2024` 引用、电缆/架空线载流工况、开关/熔断器运行限值、测试和文档。 |
| 2026-06-03 | v2026.06.03-docs | 将升级记录移动到 README 底部，并改为单行追加记录。 |
| 2026-06-03 | v2026.06.03-builder-followups | 强化 `build_pandapower_net` 资产映射和示例。 |
| 2026-06-03 | v2026.06.03-parameterized-assets | 增加参数化工程资产对 pandapower 建模的支持。 |
