from ..equipment.transformers import get_all_transformers as _get_all_transformers
from ..equipment.cables import get_all_cables as _get_all_cables
from ..equipment.overhead_lines import get_all_overhead_lines as _get_all_overhead_lines
from ..equipment.switchgear import get_all_switchgear as _get_all_switchgear


def _get_x_ohm_per_km_default(model):
    if "x_ohm_per_km" in model:
        return model["x_ohm_per_km"]
    if "x_ohm_per_km_table" in model:
        table = model["x_ohm_per_km_table"]
        if isinstance(table, dict):
            if "1.5" in table:
                return table["1.5"]
            if 1.5 in table:
                return table[1.5]
            keys = sorted(table.keys(), key=lambda k: float(k) if isinstance(k, str) else k)
            for k in keys:
                target = float(k) if isinstance(k, str) else k
                if target >= 1.5:
                    return table[k]
            if keys:
                return table[keys[0]]
    return 0.0


def _get_max_i_ka(model):
    for key in ("max_i_ka_ground", "max_i_ka"):
        if key in model:
            val = model[key]
            if isinstance(val, list):
                return val[0] if val else 0.0
            return val
    return 0.0


def chinese_line_std_types():
    result = {}
    cable_data = _get_all_cables() if _get_all_cables else {}

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
            entry = {
                "c_nf_per_km": float(m.get("c_nf_per_km", 0.0)),
                "r_ohm_per_km": float(m.get("r_ohm_per_km", 0.0)),
                "x_ohm_per_km": float(m.get("x_ohm_per_km", 0.0)),
                "max_i_ka": float(_get_max_i_ka(m)),
            }
            for ext_key in ("r0_ohm_per_km", "x0_ohm_per_km", "c0_nf_per_km"):
                if ext_key in m:
                    entry[ext_key] = float(m[ext_key])
            entry["type"] = m.get("type", "cs")
            if "q_mm2" in m:
                entry["q_mm2"] = float(m["q_mm2"])
            elif "cross_section_mm2" in m:
                entry["q_mm2"] = float(m["cross_section_mm2"])
            if "alpha" in m:
                entry["alpha"] = float(m["alpha"])
            for ext_key in ("endtemp_degree", "conductor_material", "insulation_type",
                            "armor_type", "voltage_rating", "standard", "source_note"):
                if ext_key in m:
                    entry[ext_key] = m[ext_key]
            result[name] = entry

    ohl_data = _get_all_overhead_lines() if _get_all_overhead_lines else {}

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
            entry = {
                "c_nf_per_km": float(m.get("c_nf_per_km", 0.0)),
                "r_ohm_per_km": float(m.get("r_ohm_per_km", 0.0)),
                "x_ohm_per_km": float(_get_x_ohm_per_km_default(m)),
                "max_i_ka": float(_get_max_i_ka(m)),
            }
            for ext_key in ("r0_ohm_per_km", "x0_ohm_per_km", "c0_nf_per_km"):
                if ext_key in m:
                    entry[ext_key] = float(m[ext_key])
            entry["type"] = m.get("type", "ol")
            if "q_mm2" in m:
                entry["q_mm2"] = float(m["q_mm2"])
            elif "cross_section_mm2" in m:
                entry["q_mm2"] = float(m["cross_section_mm2"])
            if "alpha" in m:
                entry["alpha"] = float(m["alpha"])
            for ext_key in ("endtemp_degree", "conductor_material", "insulation_type",
                            "voltage_rating", "standard", "source_note"):
                if ext_key in m:
                    entry[ext_key] = m[ext_key]
            if "x_ohm_per_km_table" in m:
                entry["x_ohm_per_km_table"] = m["x_ohm_per_km_table"]
            result[name] = entry

    return result


def chinese_trafo_std_types():
    result = {}
    trafo_data = _get_all_transformers() if _get_all_transformers else {}

    for category in ("oil_immersed", "dry_type", "main_transformer_35kv", "main_transformer_110kv"):
        models = trafo_data.get(category, {})
        if not isinstance(models, dict):
            continue
        for name, m in models.items():
            entry = {
                "sn_mva": float(m.get("sn_kva", 0.0)) / 1000.0,
                "vn_hv_kv": float(m.get("vn_hv_kv", 0.0)),
                "vn_lv_kv": float(m.get("vn_lv_kv", 0.0)),
                "vk_percent": float(m.get("vk_percent", 0.0)),
                "vkr_percent": float(m.get("vkr_percent", 0.0)),
                "pfe_kw": float(m.get("pfe_kw", 0.0)),
                "i0_percent": float(m.get("i0_percent", 0.0)),
                "shift_degree": float(m.get("shift_degree", 0.0)),
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


def chinese_trafo3w_std_types():
    result = {}
    trafo_data = _get_all_transformers() if _get_all_transformers else {}

    models = trafo_data.get("trafo3w_110kv", {})
    if not isinstance(models, dict):
        return result
    for name, m in models.items():
        entry = {
            "sn_hv_mva": float(m.get("sn_hv_mva", 0.0)),
            "sn_mv_mva": float(m.get("sn_mv_mva", 0.0)),
            "sn_lv_mva": float(m.get("sn_lv_mva", 0.0)),
            "vn_hv_kv": float(m.get("vn_hv_kv", 0.0)),
            "vn_mv_kv": float(m.get("vn_mv_kv", 0.0)),
            "vn_lv_kv": float(m.get("vn_lv_kv", 0.0)),
            "vk_hv_percent": float(m.get("vk_hv_percent", 0.0)),
            "vk_mv_percent": float(m.get("vk_mv_percent", 0.0)),
            "vk_lv_percent": float(m.get("vk_lv_percent", 0.0)),
            "vkr_hv_percent": float(m.get("vkr_hv_percent", 0.0)),
            "vkr_mv_percent": float(m.get("vkr_mv_percent", 0.0)),
            "vkr_lv_percent": float(m.get("vkr_lv_percent", 0.0)),
            "pfe_kw": float(m.get("pfe_kw", 0.0)),
            "i0_percent": float(m.get("i0_percent", 0.0)),
            "shift_mv_degree": float(m.get("shift_mv_degree", 0.0)),
            "shift_lv_degree": float(m.get("shift_lv_degree", 0.0)),
        }
        for ext_key in ("vector_group", "tap_side", "tap_neutral", "tap_min", "tap_max",
                        "tap_step_percent", "tap_changer_type", "standard", "source_note"):
            if ext_key in m:
                entry[ext_key] = m[ext_key]
        result[name] = entry

    return result


def chinese_fuse_std_types():
    result = {}
    sw_data = _get_all_switchgear() if _get_all_switchgear else {}

    fuse_dict = sw_data.get("fuse_mv", {})
    for fuse_key, fuse in fuse_dict.items():
        current_series = fuse.get("fuse_element_current_series", [])
        for i_a in current_series:
            i_val = float(i_a)
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
