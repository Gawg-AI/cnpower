# cnpower

Chinese 10kV/0.4kV distribution-grid engineering parameter library.

`cnpower` 是面向中国配电网规划、潮流计算、设备选型和工程校验的
10kV/0.4kV 工程参数库。当前版本在静态设备参数基础上，补充了变压器
额定电流派生、线路/电缆载流工况、开关设备短时耐受、保护配合、寿命与
运行策略等动态工程参量。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%2B-green.svg)
![Models](https://img.shields.io/badge/Models-662-brightgreen.svg)
![Standards](https://img.shields.io/badge/Standards-GB%2FGB--T%202025-orange.svg)

## Overview

`cnpower` provides Chinese distribution-grid equipment parameters, typical
connection modes, standards references, compliance checks, and pandapower
integration for planning and simulation workflows.

The current library contains 662 equipment models across transformers, cables,
overhead lines, switchgear, compensation devices, protection schemes,
instrument transformers, surge arresters, photovoltaics, EV chargers, energy
storage, and wind turbines.

The project now includes additive operating and planning metadata beyond static
nameplate data:

- transformer side-current derivation, loading limits, thermal/loading-guide
  metadata, design life, and `GB 20052-2024` energy-efficiency references;
- cable and overhead-line ampacity reference conditions, derating metadata,
  thermal limits, short-circuit `I^2t`, dynamic rating metadata, and life-cycle
  fields;
- switchgear, circuit-breaker, fuse, and protection operating limits,
  short-time withstand duration, endurance metadata, internal-arc placeholders,
  time-current curve metadata, and coordination metadata.

For a machine-readable summary of the current library, see
[`cnpower_project_profile.json`](cnpower_project_profile.json).

## Model Coverage

| Module | Count | Contents |
|---|---:|---|
| Transformers | 212 | Oil-immersed, dry-type, box substations, 35kV/110kV main transformers, three-winding transformers |
| Cables | 178 | 10kV, 35kV, 0.4kV, and 110kV power cables |
| Overhead lines | 82 | 10kV insulated lines, 0.4kV insulated lines, bare conductors |
| Switchgear | 61 | Switchgear cabinets, MV/LV breakers, load switches, MV fuses, reclosers, sectionalizers |
| Reactive compensation | 29 | MV/LV capacitors and SVG devices |
| Protection | 10 | Line and transformer protection schemes |
| Instrument transformers | 32 | MV/LV CTs and MV PTs |
| Surge arresters | 4 | MV and LV arresters |
| Photovoltaic | 17 | PV modules, string inverters, central inverters |
| EV chargers | 9 | AC slow chargers, DC fast chargers, DC super-fast chargers |
| Energy storage | 19 | LFP batteries, lead-carbon batteries, PCS |
| Wind turbines | 9 | Small and medium distributed wind turbines |

Total: 662 models.

## Standards

The standards index currently exposes 49 standards and planning references.
Key references include:

| Standard | Use |
|---|---|
| `GB/T 6451-2023` | Oil-immersed transformer technical parameters |
| `GB/T 10228-2023` | Dry-type transformer technical parameters |
| `GB/T 1094.7-2024` | Oil-immersed transformer loading and aging guide |
| `GB/T 1094.11-2022` | Dry-type transformer requirements |
| `GB/T 1094.12-2013` | Dry-type transformer loading guide |
| `GB/T 17468-2019` | Transformer selection guide |
| `GB 20052-2024` | Power transformer energy-efficiency limits and grades |
| `GB/T 12706.1~3-2020` | 1kV to 35kV extruded-insulation power cables |
| `GB/T 1179-2017` | Round-wire concentric-lay overhead conductors |
| `GB/T 14049-2008` | 10kV aerial insulated cables |
| `GB/T 12527-2008` | Aerial insulated cables up to and including 1kV |
| `GB/T 1984-2024` | High-voltage AC circuit breakers |
| `GB/T 11022-2020` | Common specifications for HV switchgear and controlgear |
| `GB/T 3906-2020` | 3.6kV to 40.5kV metal-enclosed switchgear |
| `GB/T 15166.2-2023` | HV current-limiting fuses |
| `GB/T 15166.6-2023` | Fuse-link selection for transformer circuits |
| `GB/T 45418-2025` | Distribution network general technical guide |

Use `cnpower.standards.get_all_standards()` for the full index.

## Installation

```bash
pip install cnpower
```

Install with pandapower integration:

```bash
pip install "cnpower[pandapower]"
```

Install from source:

```bash
git clone https://github.com/Gawg-AI/cnpower.git
cd cnpower
pip install -e ".[pandapower]"
```

## Quick Start

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

## Pandapower Integration

```python
import pandapower as pp
from cnpower.pandapower_integration import add_chinese_std_types

net = pp.create_empty_network()
add_chinese_std_types(net)

hv_bus = pp.create_bus(net, vn_kv=10, name="HV Bus")
lv_bus = pp.create_bus(net, vn_kv=0.4, name="LV Bus")
from_bus = pp.create_bus(net, vn_kv=10, name="Line From")
to_bus = pp.create_bus(net, vn_kv=10, name="Line To")

pp.create_transformer(net, hv_bus, lv_bus, std_type="S13-630/10")
pp.create_line(net, from_bus, to_bus, length_km=2.0, std_type="YJV22-3x70-10kV")
pp.runpp(net)
```

## Engineering Normalization And Checks

`cnpower.engineering.normalize_equipment()` derives common fields from existing
equipment records. For transformers, it derives side-specific rated current from
capacity and voltage:

```python
from cnpower.engineering import normalize_equipment

trafo = normalize_equipment(
    "transformer",
    {"sn_kva": 630, "vn_hv_kv": 10, "vn_lv_kv": 0.4},
    context={"current_side": "lv"},
)

print(trafo["rated_current_a"])  # 909.3
```

`cnpower.engineering.check_equipment_compliance()` can then compare equipment
limits with power-flow, short-circuit, or planning results.

## Operating Parameter Guide

Detailed field definitions and maintenance rules are in
[`docs/OPERATING_PARAMETERS.md`](docs/OPERATING_PARAMETERS.md).

Important source-type rules:

- `standard_table`: direct standard table value.
- `derived_formula`: calculated from nameplate parameters.
- `standard_reference`: standard-backed method or requirement.
- `standard_reference_and_engineering_default`: standard-backed check with a
  conservative default.
- `engineering_policy`: planning or utility-policy default.
- `manufacturer_typical_or_engineering_default`: manufacturer catalogue or
  typical placeholder.
- `project_specific_required`: must be filled by the project or site.

Planning defaults should not be treated as mandatory GB/GB/T limits.

## Project Structure

```text
cnpower/
  equipment/                 Equipment parameter libraries
  equipment/new_energy/      PV, EV charging, storage, wind
  engineering/               Normalization, compliance, network building
  pandapower_integration/    Chinese pandapower standard types
  standards/                 GB/GB-T/DL/T/NB/T/Q/GDW reference index
  topology/                  Typical connection modes
  validation/                Power-quality and planning validation rules
docs/
  OPERATING_PARAMETERS.md    Operating-parameter maintainer guide
tests/
  test_*.py                  Regression and integration tests
```

## Data Format

Equipment libraries use `dict[str, dict]`, with model names as keys:

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

## Validation

Run the regression tests:

```bash
python -m pytest
```

Run the project validation script:

```bash
python verify_fixes.py
```

Current expected local result:

- `python -m pytest`: 21 passed
- `python verify_fixes.py`: 756 PASS, 0 FAIL

GitHub Actions also run pytest on Python 3.10 and 3.12.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). New operating, planning, dynamic-limit,
and life-cycle fields must include `source_type` or `field_source_types`
metadata so users can distinguish standard values, derived values, engineering
policy defaults, manufacturer values, and project-specific placeholders.

## License And Attribution

MIT License with attribution requirement. See [LICENSE](LICENSE).

If you use this library in a project, paper, or derivative work, include:

```text
Data Source: cnpower - https://github.com/Gawg-AI/cnpower
```

## Disclaimer

The equipment parameters in this library are compiled from published standards
and typical engineering values for reference. Actual engineering design should
use current standards, local utility requirements, manufacturer test reports,
and project-specific design conditions.

## Upgrade Notes

| Date | Version | Summary |
|---|---|---|
| 2026-06-05 | v2026.06.05-readme-json-refresh | Rewrote README for the operating-parameter release and added a machine-readable project profile JSON. |
| 2026-06-05 | v2026.06.05-operating-parameters | Added transformer rated-current derivation, dynamic loading metadata, GB 20052-2024 references, cable/overhead ampacity context, switchgear/fuse operating limits, tests, and docs. |
| 2026-06-03 | v2026.06.03-docs | Moved upgrade notes to the bottom of README and switched to one-line append-only records. |
| 2026-06-03 | v2026.06.03-builder-followups | Strengthened `build_pandapower_net` asset mapping and examples. |
| 2026-06-03 | v2026.06.03-parameterized-assets | Added parameterized engineering asset to pandapower modeling support. |
| 2026-06-03 | v2026.06.03-engineering-core | Added engineering normalization, compliance constraints, checker, pandapower bridge, and network builder. |
| 2026-06-03 | v2026.06.03-stability | Fixed package structure, compliance checker, stale data, and verification scripts. |
| 2026-06-03 | v2026.06.03-branding | Renamed project to `cnpower`, attribution wording, and README branding. |
| 2026-06-03 | v1.0.0-initial | Initial Chinese distribution-grid engineering parameter library. |
