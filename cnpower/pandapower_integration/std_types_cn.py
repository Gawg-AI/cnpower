from functools import lru_cache

from ..equipment.transformers import get_all_transformers as _get_all_transformers
from ..equipment.cables import get_all_cables as _get_all_cables
from ..equipment.overhead_lines import get_all_overhead_lines as _get_all_overhead_lines
from ..equipment.switchgear import get_all_switchgear as _get_all_switchgear
import math
import re


_NUMBER_RE = re.compile(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")
LINE_LAYING_CURRENT_FIELDS = {
    "air": "max_i_ka_air",
    "ground": "max_i_ka_ground",
    "direct_buried": "max_i_ka_ground",
    "buried": "max_i_ka_ground",
    "duct": "max_i_ka_duct",
    "pipe": "max_i_ka_duct",
}


def _to_float(value, default=None):
    if value is None:
        return default
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, (int, float)):
        number = float(value)
        return number if math.isfinite(number) else default
    if isinstance(value, (list, tuple)):
        for item in value:
            number = _to_float(item)
            if number is not None:
                return number
        return default
    match = _NUMBER_RE.search(str(value))
    if not match:
        return default
    number = float(match.group(0))
    return number if math.isfinite(number) else default


def _get_x_ohm_per_km_default(model):
    if "x_ohm_per_km" in model:
        return _to_float(model["x_ohm_per_km"])
    if "x_ohm_per_km_table" in model:
        table = model["x_ohm_per_km_table"]
        if isinstance(table, dict):
            if "1.5" in table:
                return _to_float(table["1.5"])
            if 1.5 in table:
                return _to_float(table[1.5])
            keyed_values = [
                (_to_float(k), v)
                for k, v in table.items()
                if _to_float(k) is not None
            ]
            keyed_values = sorted(keyed_values, key=lambda item: item[0])
            for target, value in keyed_values:
                if target >= 1.5:
                    return _to_float(value)
            if keyed_values:
                return _to_float(keyed_values[-1][1])
    return None


def _get_max_i_ka(model):
    method = str(model.get("laying_method") or "ground").lower()
    field = LINE_LAYING_CURRENT_FIELDS.get(method)
    if field and field in model:
        return _to_float(model[field])
    for key in ("max_i_ka", "max_i_ka_ground", "max_i_ka_air", "max_i_ka_duct"):
        if key in model:
            return _to_float(model[key])
    return None


@lru_cache(maxsize=1)
def chinese_line_std_types():
    result = {}
    cable_data = _get_all_cables()

    cable_categories = ["mv_10kv", "mv_35kv", "lv_04kv", "hv_110kv"]
    for cat in cable_categories:
        models = cable_data.get(cat, {})
        if not isinstance(models, dict):
            continue
        for key, m in models.items():
            name = m.get("name", key) if isinstance(m, dict) else key
            if not name:
                name = key
            if not name:
                continue
            c_nf = _to_float(m.get("c_nf_per_km", 0.0))
            r_ohm = _to_float(m.get("r_ohm_per_km", 0.0))
            x_ohm = _get_x_ohm_per_km_default(m)
            max_i = _get_max_i_ka(m)
            if None in (c_nf, r_ohm, x_ohm, max_i):
                continue
            entry = {
                "c_nf_per_km": c_nf,
                "r_ohm_per_km": r_ohm,
                "x_ohm_per_km": x_ohm,
                "max_i_ka": max_i,
            }
            for ext_key in ("r0_ohm_per_km", "x0_ohm_per_km", "c0_nf_per_km"):
                number = _to_float(m.get(ext_key))
                if number is not None:
                    entry[ext_key] = number
            entry["type"] = m.get("type", "cs")
            if "q_mm2" in m:
                q_mm2 = _to_float(m["q_mm2"])
                if q_mm2 is not None:
                    entry["q_mm2"] = q_mm2
            elif "cross_section_mm2" in m:
                q_mm2 = _to_float(m["cross_section_mm2"])
                if q_mm2 is not None:
                    entry["q_mm2"] = q_mm2
            if "alpha" in m:
                alpha = _to_float(m["alpha"])
                if alpha is not None:
                    entry["alpha"] = alpha
            for ext_key in ("endtemp_degree", "conductor_material", "insulation_type",
                            "armor_type", "voltage_rating", "standard", "source_note"):
                if ext_key in m:
                    entry[ext_key] = m[ext_key]
            result[name] = entry

    ohl_data = _get_all_overhead_lines()

    ohl_categories = ["mv_10kv_insulated", "lv_04kv_insulated", "bare_conductor"]
    for cat in ohl_categories:
        models = ohl_data.get(cat, {})
        if not isinstance(models, dict):
            continue
        for key, m in models.items():
            name = m.get("name", key) if isinstance(m, dict) else key
            if not name:
                name = key
            if not name:
                continue
            c_nf = _to_float(m.get("c_nf_per_km", 0.0))
            r_ohm = _to_float(m.get("r_ohm_per_km", 0.0))
            x_ohm = _get_x_ohm_per_km_default(m)
            max_i = _get_max_i_ka(m)
            if None in (c_nf, r_ohm, x_ohm, max_i):
                continue
            entry = {
                "c_nf_per_km": c_nf,
                "r_ohm_per_km": r_ohm,
                "x_ohm_per_km": x_ohm,
                "max_i_ka": max_i,
            }
            for ext_key in ("r0_ohm_per_km", "x0_ohm_per_km", "c0_nf_per_km"):
                number = _to_float(m.get(ext_key))
                if number is not None:
                    entry[ext_key] = number
            entry["type"] = m.get("type", "ol")
            if "q_mm2" in m:
                q_mm2 = _to_float(m["q_mm2"])
                if q_mm2 is not None:
                    entry["q_mm2"] = q_mm2
            elif "cross_section_mm2" in m:
                q_mm2 = _to_float(m["cross_section_mm2"])
                if q_mm2 is not None:
                    entry["q_mm2"] = q_mm2
            if "alpha" in m:
                alpha = _to_float(m["alpha"])
                if alpha is not None:
                    entry["alpha"] = alpha
            for ext_key in ("endtemp_degree", "conductor_material", "insulation_type",
                            "voltage_rating", "standard", "source_note"):
                if ext_key in m:
                    entry[ext_key] = m[ext_key]
            result[name] = entry

    return result


@lru_cache(maxsize=1)
def chinese_trafo_std_types():
    result = {}
    trafo_data = _get_all_transformers()

    for category in ("oil_immersed", "dry_type", "box_substation", "main_transformer_35kv", "main_transformer_110kv"):
        models = trafo_data.get(category, {})
        if not isinstance(models, dict):
            continue
        for name, m in models.items():
            sn_kva = _to_float(m.get("sn_kva"))
            required_values = (
                sn_kva,
                _to_float(m.get("vn_hv_kv")),
                _to_float(m.get("vn_lv_kv")),
                _to_float(m.get("vk_percent")),
                _to_float(m.get("vkr_percent")),
                _to_float(m.get("pfe_kw")),
                _to_float(m.get("i0_percent")),
                _to_float(m.get("shift_degree")),
            )
            if None in required_values:
                continue
            entry = {
                "sn_mva": sn_kva / 1000.0,
                "vn_hv_kv": required_values[1],
                "vn_lv_kv": required_values[2],
                "vk_percent": required_values[3],
                "vkr_percent": required_values[4],
                "pfe_kw": required_values[5],
                "i0_percent": required_values[6],
                "shift_degree": required_values[7],
            }
            for ext_key in ("vector_group", "tap_side", "tap_neutral", "tap_min", "tap_max",
                            "tap_step_percent", "tap_step_degree", "tap_changer_type",
                            "vk0_percent", "vkr0_percent", "mag0_percent", "mag0_rx",
                            "si0_hv_partial"):
                if ext_key in m:
                    entry[ext_key] = m[ext_key]
            for ext_key in ("cooling_type", "winding_type", "insulation_class", "installation",
                            "standard", "source_note"):
                if ext_key in m:
                    entry[ext_key] = m[ext_key]
            result[name] = entry

    return result


@lru_cache(maxsize=1)
def chinese_trafo3w_std_types():
    result = {}
    trafo_data = _get_all_transformers()

    models = trafo_data.get("trafo3w_110kv", {})
    if not isinstance(models, dict):
        return result
    for name, m in models.items():
        required_values = (
            _to_float(m.get("sn_hv_mva")),
            _to_float(m.get("sn_mv_mva")),
            _to_float(m.get("sn_lv_mva")),
            _to_float(m.get("vn_hv_kv")),
            _to_float(m.get("vn_mv_kv")),
            _to_float(m.get("vn_lv_kv")),
            _to_float(m.get("vk_hv_percent")),
            _to_float(m.get("vk_mv_percent")),
            _to_float(m.get("vk_lv_percent")),
            _to_float(m.get("vkr_hv_percent")),
            _to_float(m.get("vkr_mv_percent")),
            _to_float(m.get("vkr_lv_percent")),
            _to_float(m.get("pfe_kw")),
            _to_float(m.get("i0_percent")),
            _to_float(m.get("shift_mv_degree")),
            _to_float(m.get("shift_lv_degree")),
        )
        if None in required_values:
            continue
        entry = {
            "sn_hv_mva": required_values[0],
            "sn_mv_mva": required_values[1],
            "sn_lv_mva": required_values[2],
            "vn_hv_kv": required_values[3],
            "vn_mv_kv": required_values[4],
            "vn_lv_kv": required_values[5],
            "vk_hv_percent": required_values[6],
            "vk_mv_percent": required_values[7],
            "vk_lv_percent": required_values[8],
            "vkr_hv_percent": required_values[9],
            "vkr_mv_percent": required_values[10],
            "vkr_lv_percent": required_values[11],
            "pfe_kw": required_values[12],
            "i0_percent": required_values[13],
            "shift_mv_degree": required_values[14],
            "shift_lv_degree": required_values[15],
        }
        for ext_key in ("vector_group", "tap_side", "tap_neutral", "tap_min", "tap_max",
                        "tap_step_percent", "tap_step_degree", "tap_changer_type",
                        "vk0_hv_percent", "vk0_mv_percent", "vk0_lv_percent",
                        "vkr0_hv_percent", "vkr0_mv_percent", "vkr0_lv_percent",
                        "zero_seq_note", "standard", "source_note"):
            if ext_key in m:
                entry[ext_key] = m[ext_key]
        result[name] = entry

    return result


@lru_cache(maxsize=1)
def chinese_fuse_std_types():
    result = {}
    sw_data = _get_all_switchgear()

    fuse_dict = sw_data.get("fuse_mv", {})
    for fuse_key, fuse in fuse_dict.items():
        current_series = fuse.get("fuse_element_current_series", [])
        for i_a in current_series:
            i_val = _to_float(i_a)
            if i_val is None:
                continue
            if i_val == int(i_val):
                suffix = f"{int(i_val)}A"
            else:
                suffix = f"{i_val}A"
            entry_name = f"{fuse_key}/{suffix}"
            entry = {
                "fuse_type": "HV",
                "i_rated_a": i_val,
            }
            for ext_key in ("rated_voltage_kv", "rated_breaking_current_ka", "type",
                            "standard", "source_note"):
                if ext_key in fuse:
                    entry[ext_key] = fuse[ext_key]
            result[entry_name] = entry

    return result


def add_chinese_std_types(net):
    try:
        import pandapower as pp
    except ImportError:
        raise ImportError(
            "pandapower is required for add_chinese_std_types. "
            "Install it with: pip install pandapower"
        )

    pp.create_std_types(net, data=chinese_line_std_types(), element="line")
    pp.create_std_types(net, data=chinese_trafo_std_types(), element="trafo")
    pp.create_std_types(net, data=chinese_trafo3w_std_types(), element="trafo3w")
    pp.create_std_types(net, data=chinese_fuse_std_types(), element="fuse")
    return net


def remove_chinese_std_types(net):
    line_types = chinese_line_std_types()
    trafo_types = chinese_trafo_std_types()
    trafo3w_types = chinese_trafo3w_std_types()
    fuse_types = chinese_fuse_std_types()

    for name in line_types:
        if name in net.std_types.get("line", {}):
            del net.std_types["line"][name]
    for name in trafo_types:
        if name in net.std_types.get("trafo", {}):
            del net.std_types["trafo"][name]
    for name in trafo3w_types:
        if name in net.std_types.get("trafo3w", {}):
            del net.std_types["trafo3w"][name]
    for name in fuse_types:
        if name in net.std_types.get("fuse", {}):
            del net.std_types["fuse"][name]

    return net


def list_chinese_std_types(net):
    line_types = chinese_line_std_types()
    trafo_types = chinese_trafo_std_types()
    trafo3w_types = chinese_trafo3w_std_types()
    fuse_types = chinese_fuse_std_types()

    result = {}
    available_line = [n for n in line_types if n in net.std_types.get("line", {})]
    available_trafo = [n for n in trafo_types if n in net.std_types.get("trafo", {})]
    available_trafo3w = [n for n in trafo3w_types if n in net.std_types.get("trafo3w", {})]
    available_fuse = [n for n in fuse_types if n in net.std_types.get("fuse", {})]

    if available_line:
        result["line"] = available_line
    if available_trafo:
        result["trafo"] = available_trafo
    if available_trafo3w:
        result["trafo3w"] = available_trafo3w
    if available_fuse:
        result["fuse"] = available_fuse

    return result
