import math
import re


_VOLTAGE_RE = re.compile(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")


ALIASES = {
    "transformer": "transformer_2w",
    "trafo": "transformer_2w",
    "trafo_2w": "transformer_2w",
    "line": "line_cable",
    "cable": "line_cable",
    "overhead_line": "line_overhead",
    "switch": "switch_breaker",
    "breaker": "switch_breaker",
    "disconnector": "switch_disconnector",
    "switchgear": "switchgear_cabinet",
    "capacitor": "reactive_compensation",
    "sgen": "pv_inverter",
    "pv": "pv_inverter",
    "battery": "storage",
    "metering": "metering_ct_pt",
    "ct_pt": "metering_ct_pt",
}


LINE_LAYING_CURRENT_FIELDS = {
    "air": "max_i_ka_air",
    "ground": "max_i_ka_ground",
    "direct_buried": "max_i_ka_ground",
    "buried": "max_i_ka_ground",
    "duct": "max_i_ka_duct",
    "pipe": "max_i_ka_duct",
}


def canonical_equipment_type(equipment_type):
    if equipment_type is None:
        return "unknown"
    key = str(equipment_type).strip()
    return ALIASES.get(key, key)


def first_number(value, default=None, prefer="max"):
    if value is None:
        return default
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, (int, float)):
        number = float(value)
        return number if math.isfinite(number) else default
    if isinstance(value, (list, tuple)):
        nums = [first_number(v, None, prefer=prefer) for v in value]
        nums = [v for v in nums if v is not None]
        if not nums:
            return default
        return min(nums) if prefer == "min" else max(nums)
    if isinstance(value, str):
        matches = [float(m.group(0)) for m in _VOLTAGE_RE.finditer(value)]
        if not matches:
            return default
        return min(matches) if prefer == "min" else max(matches)
    return default


def parse_voltage_kv(value, *, source_unit=None, default=None):
    number = first_number(value, default=None)
    if number is None:
        return default
    text = str(value).lower() if isinstance(value, str) else ""
    source_unit = str(source_unit).lower() if source_unit is not None else None
    if "kv" in text:
        return number
    if source_unit == "v" or text.endswith("v") or "dc" in text:
        return number / 1000.0 if number > 2 else number
    if source_unit == "kv":
        return number
    if number > 1000:
        return number / 1000.0
    return number


def parse_percent_range_midpoint(value, default=None):
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return float(value)
    nums = [float(m.group(0)) for m in _VOLTAGE_RE.finditer(str(value))]
    if not nums:
        return default
    return sum(nums) / len(nums)


def _first_not_none(*values):
    for value in values:
        if value is not None:
            return value
    return None


def calc_q_mvar_from_power_factor(p_mw, power_factor, sign=1):
    if p_mw is None or power_factor in (None, 0):
        return 0.0
    pf = first_number(power_factor)
    p = first_number(p_mw)
    if pf is None or p is None:
        return 0.0
    pf = max(min(pf, 1.0), -1.0)
    if abs(pf) == 1.0:
        return 0.0
    return sign * abs(p) * math.tan(math.acos(abs(pf)))


def apparent_power_mva_from_kw(power_kw, power_factor=None):
    power = first_number(power_kw)
    if power is None:
        return None
    pf = first_number(power_factor, 0.95, prefer="min")
    if pf is None:
        pf = 0.95
    pf = abs(pf)
    if pf <= 0 or not math.isfinite(pf):
        return None
    return power / (min(pf, 1.0) * 1000.0)


def select_line_current_ka(data, laying_method=None):
    method = (laying_method or data.get("laying_method") or "ground")
    method = str(method).lower()
    field = LINE_LAYING_CURRENT_FIELDS.get(method)
    if field and field in data:
        return first_number(data[field])
    for key in ("max_i_ka", "max_i_ka_ground", "max_i_ka_air", "max_i_ka_duct"):
        if key in data:
            return first_number(data[key])
    return None


def select_reactance_ohm_per_km(data, spacing_m=1.5):
    if "x_ohm_per_km" in data:
        return first_number(data["x_ohm_per_km"])
    table = data.get("x_ohm_per_km_table")
    if not isinstance(table, dict) or not table:
        return None
    if spacing_m in table:
        return first_number(table[spacing_m])
    spacing_key = str(spacing_m)
    if spacing_key in table:
        return first_number(table[spacing_key])
    ordered = [
        (first_number(key), value)
        for key, value in table.items()
        if first_number(key) is not None
    ]
    if not ordered:
        return None
    ordered = sorted(ordered, key=lambda item: item[0])
    for key, value in ordered:
        if key >= spacing_m:
            return first_number(value)
    return first_number(ordered[-1][1])


def _copy_alias(target, data, source_key, dest_key, converter=lambda value: value):
    if dest_key not in target and source_key in data and data[source_key] is not None:
        converted = converter(data[source_key])
        if converted is not None:
            target[dest_key] = converted


def normalize_equipment(equipment_type, equipment, *, context=None):
    context = context or {}
    data = dict(equipment or {})
    canonical = canonical_equipment_type(equipment_type)
    normalized = dict(data)
    normalized["equipment_type"] = canonical

    for key in (
        "rated_voltage_kv",
        "rated_voltage_hv_kv",
        "rated_voltage_mv_kv",
        "rated_voltage_lv_kv",
        "vn_kv",
        "vn_hv_kv",
        "vn_mv_kv",
        "vn_lv_kv",
    ):
        if key in normalized:
            value = parse_voltage_kv(normalized[key], source_unit="kv")
            if value is not None:
                normalized[key] = value

    _copy_alias(normalized, data, "sn_kva", "sn_mva", lambda value: first_number(value) / 1000.0)
    _copy_alias(normalized, data, "rated_capacity_kva", "sn_mva", lambda value: first_number(value) / 1000.0)
    _copy_alias(normalized, data, "rated_power_kw", "p_mw", lambda value: first_number(value) / 1000.0)
    _copy_alias(
        normalized,
        data,
        "rated_power_kw",
        "sn_mva",
        lambda value: apparent_power_mva_from_kw(
            value,
            _first_not_none(data.get("power_factor"), data.get("power_factor_range"), context.get("power_factor")),
        ),
    )
    _copy_alias(normalized, data, "rated_charge_discharge_power_kw", "p_mw", lambda value: first_number(value) / 1000.0)
    _copy_alias(
        normalized,
        data,
        "rated_charge_discharge_power_kw",
        "sn_mva",
        lambda value: apparent_power_mva_from_kw(
            value,
            _first_not_none(data.get("power_factor"), data.get("power_factor_range"), context.get("power_factor")),
        ),
    )
    _copy_alias(normalized, data, "rated_capacity_kwh", "max_e_mwh", lambda value: first_number(value) / 1000.0)

    if "rated_voltage_kv" not in normalized:
        for key in ("rated_voltage_kv", "vn_kv", "vn_hv_kv", "voltage_rating"):
            if key in data:
                value = parse_voltage_kv(data[key])
                if value is not None:
                    normalized["rated_voltage_kv"] = value
                    break
        if "rated_voltage_v" in data and "rated_voltage_kv" not in normalized:
            value = parse_voltage_kv(data["rated_voltage_v"], source_unit="v")
            if value is not None:
                normalized["rated_voltage_kv"] = value

    if canonical in ("line_cable", "line_overhead"):
        current = select_line_current_ka(data, context.get("laying_method"))
        if current is not None:
            normalized["max_i_ka"] = current
            normalized["rated_current_a"] = current * 1000.0
        x_value = select_reactance_ohm_per_km(data, context.get("spacing_m", 1.5))
        if x_value is not None:
            normalized["x_ohm_per_km"] = x_value

    if canonical in ("transformer_2w", "transformer_3w"):
        sn_mva = first_number(normalized.get("sn_mva"))
        if sn_mva is not None:
            for side in ("hv", "mv", "lv"):
                voltage = first_number(normalized.get(f"vn_{side}_kv"))
                if voltage and voltage > 0 and voltage >= 1e-6 and math.isfinite(voltage):
                    normalized.setdefault(
                        f"rated_current_{side}_a",
                        round(sn_mva * 1000.0 / (math.sqrt(3) * voltage), 1),
                    )
        rated_current = {"method": "S/(sqrt(3)*U)", "source_type": "derived_formula"}
        for side in ("hv", "mv", "lv"):
            value = normalized.get(f"rated_current_{side}_a")
            if value is not None:
                rated_current[f"{side}_a"] = value
        if len(rated_current) > 2:
            normalized.setdefault("rated_current", rated_current)
        current_side = str(context.get("current_side", "hv")).lower()
        side_current = normalized.get(f"rated_current_{current_side}_a")
        if side_current is not None:
            normalized.setdefault("rated_current_a", side_current)

    if "rated_current_a" not in normalized:
        for key in ("frame_current_a", "max_i_ka", "rated_primary_a"):
            if key in normalized:
                value = first_number(normalized[key])
                if value is not None:
                    normalized["rated_current_a"] = value * 1000.0 if key == "max_i_ka" else value
                    break

    _copy_alias(normalized, normalized, "rated_short_circuit_breaking_ka", "rated_short_circuit_breaking_current_ka", first_number)
    _copy_alias(normalized, normalized, "rated_breaking_current_ka", "rated_short_circuit_breaking_current_ka", first_number)
    _copy_alias(normalized, normalized, "breaking_capacity_ka", "rated_short_circuit_breaking_current_ka", first_number)
    _copy_alias(normalized, normalized, "rated_short_circuit_making_ka", "rated_peak_withstand_ka", first_number)
    _copy_alias(normalized, normalized, "rated_short_time_withstand_ka_4s", "short_time_thermal_current_ka", first_number)
    _copy_alias(normalized, normalized, "short_circuit_current_1s_ka", "short_time_thermal_current_ka", first_number)

    if "q_mvar" not in normalized and "p_mw" in normalized:
        normalized["q_mvar"] = calc_q_mvar_from_power_factor(
            normalized["p_mw"], data.get("power_factor", context.get("power_factor", 0.95))
        )
    if canonical == "storage":
        normalized.setdefault("soc_percent", parse_percent_range_midpoint(data.get("soc_range_percent"), 50.0))
        normalized.setdefault("min_e_mwh", 0.0)
    if canonical == "reactive_compensation" and "rated_capacity_kvar" in data:
        normalized.setdefault("q_mvar", first_number(data["rated_capacity_kvar"]) / 1000.0)
        normalized.setdefault("p_mw", 0.0)

    return normalized


def normalize_results(results):
    data = dict(results or {})
    if "max_current_a" not in data and "i_ka" in data:
        value = first_number(data["i_ka"])
        if value is not None:
            data["max_current_a"] = value * 1000.0
    if "operating_voltage_kv" not in data and "vn_kv" in data:
        value = parse_voltage_kv(data["vn_kv"])
        if value is not None:
            data["operating_voltage_kv"] = value
    if "soc_percent" in data:
        data["soc_percent"] = parse_percent_range_midpoint(data["soc_percent"], data["soc_percent"])
    return data
