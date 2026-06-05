# Operating Parameter Upgrade Guide

This guide explains the operating, planning, and life-cycle parameters added to
`cnpower`. It is intended for maintainers who need to extend the equipment
library without mixing national-standard values, derived values, and engineering
policy defaults.

## Scope

The upgrade adds three engineering parameter groups:

1. Transformer operating current, loading, thermal, energy-efficiency, and life
   metadata.
2. Cable and overhead-line ampacity reference conditions, derating metadata,
   thermal limits, short-circuit energy, and life-cycle metadata.
3. Switchgear, circuit-breaker, load-switch, recloser, sectionalizer, fuse, and
   protection operating limits, endurance, IAC placeholders, and time-current
   curve metadata.

Existing flat fields are kept for backward compatibility. New structured fields
are additive.

## Source Types

Use `field_source_types` or nested `source_type` fields to identify where a
value comes from:

| Source type | Meaning |
|---|---|
| `standard_table` | A direct value from a standard table. |
| `derived_formula` | Calculated from nameplate parameters, such as `S/(sqrt(3)*U)`. |
| `standard_reference` | A standard defines the method or requirement, but not a model-specific table value. |
| `standard_reference_and_engineering_default` | A standard-backed check with a conservative default used until project data is supplied. |
| `engineering_policy` | A planning default, utility rule, or project policy. |
| `manufacturer_typical_or_engineering_default` | A manufacturer catalogue value or typical engineering placeholder. |
| `project_specific_required` | A field that must be filled by the project, site, or utility. |

Do not present `engineering_policy` as a mandatory GB/GB/T limit.

## Transformers

Each transformer entry is enhanced by `cnpower.equipment.transformers` after the
base tables are built.

Example:

```python
from cnpower.equipment.transformers import get_all_transformers

s13 = get_all_transformers()["oil_immersed"]["S13-630/10"]

assert s13["rated_current_hv_a"] == 36.4
assert s13["rated_current_lv_a"] == 909.3
assert s13["rated_current"]["method"] == "S/(sqrt(3)*U)"
```

Key fields:

| Field | Meaning |
|---|---|
| `rated_current_hv_a`, `rated_current_mv_a`, `rated_current_lv_a` | Side-specific rated current, derived from rated power and voltage. |
| `rated_current` | Structured form with side currents, method, and source type. |
| `normal_loading_limit_percent` | Default planning loading limit. |
| `economic_loading_range_percent` | Typical economic loading range for planning comparison. |
| `n1_loading_limit_percent` | Short-time planning limit for N-1 or maintenance transfer scenarios. |
| `emergency_loading_limit_percent` | Short emergency default, requiring thermal validation. |
| `loading_limits` | Structured loading policy with durations and source type. |
| `thermal_model` | Loading guide, temperature thresholds, and aging model reference. |
| `energy_efficiency` | Current energy-efficiency standard and grade placeholder. |
| `design_life_years` | Default life-cycle planning value. |

Standards and guidance:

- Oil-immersed parameter tables: `GB/T 6451-2023`
- Dry-type parameter tables: `GB/T 10228-2023`
- Oil-immersed loading and aging: `GB/T 1094.7-2024`
- Dry-type body and temperature requirements: `GB/T 1094.11-2022`
- Dry-type loading guide: `GB/T 1094.12-2013`
- Transformer selection: `GB/T 17468-2019`
- Energy efficiency: `GB 20052-2024`

### Current Side Selection

`normalize_equipment()` derives side currents when it receives enough data.
The generic `rated_current_a` defaults to the high-voltage side. Pass
`context={"current_side": "lv"}` when validating low-voltage-side current.

```python
from cnpower.engineering import normalize_equipment

trafo = normalize_equipment(
    "transformer",
    {"sn_kva": 630, "vn_hv_kv": 10, "vn_lv_kv": 0.4},
    context={"current_side": "lv"},
)

assert trafo["rated_current_a"] == 909.3
```

## Cables

Cable entries now include operating context in addition to pandapower-compatible
R/X/C and `max_i_ka_*` fields.

Key fields:

| Field | Meaning |
|---|---|
| `ampacity_reference` | Air, soil, burial, spacing, and laying-method assumptions. |
| `derating_factors` | Required correction categories for temperature, grouping, soil, depth, and harmonics. |
| `thermal_limits` | Normal, emergency, and short-circuit conductor temperature limits. |
| `short_circuit_i2t_ka2s` | `I^2*t` from the 1s short-circuit current. |
| `short_circuit_rating` | Structured current, duration, and energy metadata. |
| `lifecycle` | Design life and overload-hours policy. |

Example:

```python
from cnpower.equipment.cables import get_all_cables

cable = get_all_cables()["mv_10kv"]["YJV22-3x70-10kV"]
ampacity_ground_a = cable["max_i_ka_ground"] * 1000
normal_temp_c = cable["thermal_limits"]["max_conductor_temp_normal_c"]
```

The existing `max_i_ka_air`, `max_i_ka_ground`, and `max_i_ka_duct` values are
still the compatibility fields used by pandapower integration and normalization.

## Overhead Lines

Overhead-line entries now carry planning metadata for dynamic rating and
mechanical design inputs.

Key fields:

| Field | Meaning |
|---|---|
| `rated_current_a` | Derived from `max_i_ka`. |
| `ampacity_reference` | Ambient air, wind, solar radiation, emissivity, and absorptivity assumptions. |
| `dynamic_line_rating` | Heat-balance model metadata. |
| `mechanical_limits` | Project-specific span, ice, wind, clearance, and sag placeholders. |
| `lifecycle` | Design life, inspection interval, failure-rate, and repair-time placeholders. |

Fill `mechanical_limits` from project route design and local meteorological
conditions before using it for clearance or sag compliance.

## Switchgear And Fuses

Switchgear entries are enhanced in `cnpower.equipment.switchgear`.

Key fields:

| Field | Meaning |
|---|---|
| `rated_current_max_a` | Maximum selectable rated current when the base field is a list. |
| `rated_short_time_duration_s` | Duration paired with short-time withstand current. |
| `short_time_withstand` | Current, duration, and `I^2*t` metadata. |
| `internal_arc_class` | IAC placeholder for switchgear cabinets. |
| `endurance` | Mechanical/electrical life and maintenance metadata. |
| `time_current_curve` | Fuse curve metadata, preserving existing curve points. |
| `selection_guide` | Fuse-transformer selection reference. |

Standards and guidance:

- MV circuit breakers: `GB/T 1984-2024`
- Common HV switchgear requirements: `GB/T 11022-2020`
- MV metal-enclosed switchgear: `GB/T 3906-2020`
- HV current-limiting fuses: `GB/T 15166.2-2023`
- Fuse selection for transformer circuits: `GB/T 15166.6-2023`
- LV circuit breakers: `GB/T 14048.2-2020`

## Protection

Protection entries now include structured metadata for settings and coordination:

- `setting_metadata`
- `fuse_coordination`
- `thermal_trip_model`

The base protection notes remain descriptive. Actual settings still require a
fault-current study, maximum load current, downstream protection curves, and
utility selectivity rules.

## Adding New Equipment

When adding a new model:

1. Keep existing compatibility fields, especially pandapower fields.
2. Add or let the module helper derive operating fields.
3. Mark source type for every planning or dynamic field.
4. If a value is project-specific, set it to `None` and include a note.
5. Add a focused test in `tests/test_operating_parameters.py`.
6. Run `python -m pytest`.

## Validation Checklist

Before merging a parameter update:

- Transformer side currents are derived correctly.
- `GB 20052-2024` is used for energy-efficiency metadata.
- Cable and overhead-line ampacity assumptions are explicit.
- Short-time withstand current always has a duration.
- Fuse curves state whether points are current multiples or amperes.
- Planning defaults are labelled `engineering_policy`.
- Project-specific fields are not silently treated as standard values.
