from .normalization import canonical_equipment_type, first_number, normalize_equipment, parse_voltage_kv
from ..pandapower_integration import add_chinese_std_types


BUS_CLASSES = {"bus", "busbar"}
SWITCH_CLASSES = {
    "switch_breaker",
    "switch_disconnector",
    "load_switch",
    "circuit_breaker_lv",
    "recloser",
    "sectionalizer",
}
ELEMENT_GROUPS = {
    "ext_grid": ("ext_grids", "source_grid"),
    "line": ("lines", "line_cable"),
    "overhead_line": ("overhead_lines", "line_overhead"),
    "trafo": ("transformers", "transformer_2w"),
    "trafo3w": ("transformers_3w", "transformer_3w"),
    "load": ("loads", "load"),
    "sgen": ("sgens", "pv_inverter"),
    "wind": ("wind_turbines", "wind_turbine"),
    "storage": ("storages", "storage"),
    "ev_charger": ("ev_chargers", "ev_charger"),
    "shunt": ("shunts", "reactive_compensation"),
    "switch": ("switches", "switch_breaker"),
}
SWITCH_ET_ALIASES = {
    "b": "b",
    "bus": "b",
    "busbar": "b",
    "l": "l",
    "line": "l",
    "line_cable": "l",
    "line_overhead": "l",
    "t": "t",
    "trafo": "t",
    "transformer": "t",
    "transformer_2w": "t",
    "t3": "t3",
    "trafo3w": "t3",
    "transformer_3w": "t3",
}


def _require_pandapower():
    try:
        import pandapower as pp
    except ImportError as exc:
        raise ImportError(
            "pandapower is required for build_pandapower_net. "
            "Install cnpower with the pandapower extra: pip install cnpower[pandapower]"
        ) from exc
    return pp


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, dict):
        return [dict(item, id=key) if isinstance(item, dict) and "id" not in item else item for key, item in value.items()]
    return list(value)


def _first_present(data, *keys):
    for key in keys:
        if key in data and data[key] is not None:
            return data[key]
    return None


def _split_assets(model):
    grouped = {"buses": _as_list(model.get("buses") or model.get("busbars"))}
    for group_name, _canonical in ELEMENT_GROUPS.values():
        grouped[group_name] = _as_list(model.get(group_name))

    for asset in _as_list(model.get("assets")):
        if not isinstance(asset, dict):
            continue
        asset_class = asset.get("class") or asset.get("equipment_type") or asset.get("type")
        asset_class = canonical_equipment_type(asset_class)
        if asset_class in BUS_CLASSES:
            grouped["buses"].append(asset)
            continue
        if asset_class in SWITCH_CLASSES:
            grouped["switches"].append(asset)
            continue
        for group_name, canonical in ELEMENT_GROUPS.values():
            if asset_class == canonical or asset_class == group_name:
                grouped[group_name].append(asset)
                break
    return grouped


def _bus_id(bus):
    return bus.get("id") or bus.get("name") or bus.get("bus")


def _resolve_bus(bus_lookup, value):
    if value in bus_lookup:
        return bus_lookup[value]
    if isinstance(value, int):
        return value
    raise KeyError(f"Unknown bus reference: {value!r}")


def _item_keys(item):
    keys = []
    for key in ("id", "name"):
        value = item.get(key)
        if value is not None and value not in keys:
            keys.append(value)
    return keys


def _register_lookup(lookup, item, index, label):
    for key in _item_keys(item):
        if key in lookup and lookup[key] != index:
            raise ValueError(f"Duplicate {label} reference: {key!r}")
        lookup[key] = index


def _switch_et(item):
    raw = _first_present(item, "et", "element_type", "element_class", "target_type", "target_class")
    key = str(raw or "b").strip()
    return SWITCH_ET_ALIASES.get(key, key)


def _switch_type(data):
    raw = _first_present(data, "switch_type", "switch_kind")
    if raw is not None:
        return raw
    raw_type = data.get("type")
    if raw_type in {"CB", "LS", "LBS", "DS"}:
        return raw_type
    equipment_type = data.get("equipment_type")
    if equipment_type == "switch_breaker":
        return "CB"
    if equipment_type in {"switch_disconnector", "load_switch", "sectionalizer"}:
        return "LS"
    return None


def _resolve_element(element_lookup, et, value):
    lookup_key = {"b": "bus", "l": "line", "t": "trafo", "t3": "trafo3w"}.get(et)
    if lookup_key is None:
        raise ValueError(f"Unsupported switch element type: {et!r}")
    if isinstance(value, int):
        return value
    table_lookup = element_lookup.get(lookup_key, {})
    if value in table_lookup:
        return table_lookup[value]
    available = sorted(str(key) for key in table_lookup)
    raise KeyError(f"Unknown {lookup_key} reference for switch: {value!r}. Available references: {available}")


def _set_extra_columns(table, index, values, keys):
    for key in keys:
        if key in values and values[key] is not None:
            table.loc[index, key] = values[key]


def _number(data, key, default=None):
    return first_number(data.get(key), default)


def _required_number(data, key, label):
    value = _number(data, key)
    if value is None:
        raise ValueError(f"{label} is missing required numeric field {key!r}")
    return float(value)


def _voltage_kv(data, *keys):
    for key in keys:
        if key in data and data[key] is not None:
            if key.endswith("_kv"):
                source_unit = "kv"
            elif key.endswith("_v"):
                source_unit = "v"
            else:
                source_unit = None
            value = parse_voltage_kv(data[key], source_unit=source_unit)
            if value is not None:
                return float(value)
    return None


def _required_voltage_kv(data, keys, label):
    value = _voltage_kv(data, *keys)
    if value is None:
        joined = ", ".join(repr(key) for key in keys)
        raise ValueError(f"{label} is missing required voltage field: {joined}")
    return value


def _line_type(equipment_type, data):
    if data.get("line_type"):
        return data["line_type"]
    if data.get("type") in {"ol", "cs"}:
        return data["type"]
    return "ol" if equipment_type == "line_overhead" else "cs"


def _create_line(pp, net, item, data):
    equipment_type = data.get("equipment_type") or "line_cable"
    common = {
        "from_bus": _resolve_bus(net["cnpower_bus_lookup"], _first_present(item, "from_bus", "from")),
        "to_bus": _resolve_bus(net["cnpower_bus_lookup"], _first_present(item, "to_bus", "to")),
        "length_km": float(_required_number(data, "length_km", "Line")),
        "name": data.get("name"),
        "in_service": data.get("in_service", True),
        "df": float(data.get("df", 1.0)),
        "parallel": int(data.get("parallel", 1)),
    }
    if data.get("std_type"):
        return pp.create_line(net, std_type=data["std_type"], **common)

    kwargs = {
        "r_ohm_per_km": _required_number(data, "r_ohm_per_km", "Line"),
        "x_ohm_per_km": _required_number(data, "x_ohm_per_km", "Line"),
        "c_nf_per_km": _required_number(data, "c_nf_per_km", "Line"),
        "max_i_ka": _required_number(data, "max_i_ka", "Line"),
        "type": _line_type(equipment_type, data),
    }
    for key in ("g_us_per_km", "r0_ohm_per_km", "x0_ohm_per_km", "c0_nf_per_km", "g0_us_per_km", "endtemp_degree"):
        if key in data and data[key] is not None:
            kwargs[key] = first_number(data[key])
    return pp.create_line_from_parameters(net, **common, **kwargs)


def _create_transformer(pp, net, item, data):
    hv_bus = _resolve_bus(net["cnpower_bus_lookup"], _first_present(item, "hv_bus", "high_voltage_bus"))
    lv_bus = _resolve_bus(net["cnpower_bus_lookup"], _first_present(item, "lv_bus", "low_voltage_bus"))
    if data.get("std_type"):
        return pp.create_transformer(
            net,
            hv_bus=hv_bus,
            lv_bus=lv_bus,
            std_type=data["std_type"],
            name=data.get("name"),
            in_service=data.get("in_service", True),
        )

    kwargs = {
        "sn_mva": _required_number(data, "sn_mva", "Transformer"),
        "vn_hv_kv": _required_voltage_kv(data, ("vn_hv_kv", "rated_voltage_hv_kv", "vn_hv_v", "rated_voltage_hv_v"), "Transformer"),
        "vn_lv_kv": _required_voltage_kv(data, ("vn_lv_kv", "rated_voltage_lv_kv", "vn_lv_v", "rated_voltage_lv_v"), "Transformer"),
        "vkr_percent": _required_number(data, "vkr_percent", "Transformer"),
        "vk_percent": _required_number(data, "vk_percent", "Transformer"),
        "pfe_kw": _number(data, "pfe_kw", 0.0),
        "i0_percent": _number(data, "i0_percent", 0.0),
        "shift_degree": _number(data, "shift_degree", 0.0),
        "name": data.get("name"),
        "in_service": data.get("in_service", True),
    }
    for key in ("vector_group", "vk0_percent", "vkr0_percent", "mag0_percent", "mag0_rx", "si0_hv_partial", "xn_ohm"):
        if key in data and data[key] is not None:
            kwargs[key] = data[key] if key == "vector_group" else first_number(data[key])
    return pp.create_transformer_from_parameters(net, hv_bus=hv_bus, lv_bus=lv_bus, **kwargs)


def _transformer3w_power(data, side):
    value = _number(data, f"sn_{side}_mva")
    if value is not None:
        return float(value)
    value = _number(data, f"sn_{side}_kva")
    if value is not None:
        return float(value) / 1000.0
    value = _number(data, "sn_mva")
    if value is not None:
        return float(value)
    value = _number(data, "sn_kva")
    if value is not None:
        return float(value) / 1000.0
    raise ValueError(f"Three-winding transformer is missing sn_{side}_mva")


def _create_transformer3w(pp, net, item, data):
    hv_bus = _resolve_bus(net["cnpower_bus_lookup"], _first_present(item, "hv_bus", "high_voltage_bus"))
    mv_bus = _resolve_bus(net["cnpower_bus_lookup"], _first_present(item, "mv_bus", "medium_voltage_bus"))
    lv_bus = _resolve_bus(net["cnpower_bus_lookup"], _first_present(item, "lv_bus", "low_voltage_bus"))
    if data.get("std_type"):
        return pp.create_transformer3w(
            net,
            hv_bus=hv_bus,
            mv_bus=mv_bus,
            lv_bus=lv_bus,
            std_type=data["std_type"],
            name=data.get("name"),
            in_service=data.get("in_service", True),
        )

    kwargs = {
        "vn_hv_kv": _required_voltage_kv(data, ("vn_hv_kv", "rated_voltage_hv_kv", "vn_hv_v", "rated_voltage_hv_v"), "Three-winding transformer"),
        "vn_mv_kv": _required_voltage_kv(data, ("vn_mv_kv", "rated_voltage_mv_kv", "vn_mv_v", "rated_voltage_mv_v"), "Three-winding transformer"),
        "vn_lv_kv": _required_voltage_kv(data, ("vn_lv_kv", "rated_voltage_lv_kv", "vn_lv_v", "rated_voltage_lv_v"), "Three-winding transformer"),
        "sn_hv_mva": _transformer3w_power(data, "hv"),
        "sn_mv_mva": _transformer3w_power(data, "mv"),
        "sn_lv_mva": _transformer3w_power(data, "lv"),
        "vk_hv_percent": _required_number(data, "vk_hv_percent", "Three-winding transformer"),
        "vk_mv_percent": _required_number(data, "vk_mv_percent", "Three-winding transformer"),
        "vk_lv_percent": _required_number(data, "vk_lv_percent", "Three-winding transformer"),
        "vkr_hv_percent": _required_number(data, "vkr_hv_percent", "Three-winding transformer"),
        "vkr_mv_percent": _required_number(data, "vkr_mv_percent", "Three-winding transformer"),
        "vkr_lv_percent": _required_number(data, "vkr_lv_percent", "Three-winding transformer"),
        "pfe_kw": _number(data, "pfe_kw", 0.0),
        "i0_percent": _number(data, "i0_percent", 0.0),
        "shift_mv_degree": _number(data, "shift_mv_degree", 0.0),
        "shift_lv_degree": _number(data, "shift_lv_degree", 0.0),
        "name": data.get("name"),
        "in_service": data.get("in_service", True),
    }
    for key in ("vector_group", "vk0_hv_percent", "vk0_mv_percent", "vk0_lv_percent", "vkr0_hv_percent", "vkr0_mv_percent", "vkr0_lv_percent"):
        if key in data and data[key] is not None:
            kwargs[key] = data[key] if key == "vector_group" else first_number(data[key])
    return pp.create_transformer3w_from_parameters(net, hv_bus=hv_bus, mv_bus=mv_bus, lv_bus=lv_bus, **kwargs)


def build_pandapower_net(model, *, add_std_types=True, run_powerflow=False):
    if not isinstance(model, dict):
        raise TypeError("model must be a dict of engineering assets")
    pp = _require_pandapower()
    net = pp.create_empty_network(sn_mva=model.get("sn_mva", 100.0))
    if add_std_types:
        add_chinese_std_types(net)

    grouped = _split_assets(model)
    bus_lookup = {}
    element_lookup = {
        "bus": bus_lookup,
        "line": {},
        "trafo": {},
        "trafo3w": {},
        "load": {},
        "sgen": {},
        "storage": {},
        "shunt": {},
        "switch": {},
        "ext_grid": {},
    }
    for bus in grouped["buses"]:
        if not isinstance(bus, dict):
            continue
        vn_kv = _voltage_kv(bus, "vn_kv", "rated_voltage_kv", "rated_voltage_v", "voltage_rating")
        if vn_kv is None:
            raise ValueError(f"Bus {bus!r} is missing vn_kv")
        idx = pp.create_bus(
            net,
            vn_kv=vn_kv,
            name=bus.get("name") or bus.get("id"),
            in_service=bus.get("in_service", True),
            type=bus.get("bus_type", "b"),
            zone=bus.get("zone"),
        )
        identifier = _bus_id(bus)
        if identifier is not None:
            if identifier in bus_lookup and bus_lookup[identifier] != idx:
                raise ValueError(f"Duplicate bus reference: {identifier!r}")
            bus_lookup[identifier] = idx
        _register_lookup(bus_lookup, bus, idx, "bus")
    net["cnpower_bus_lookup"] = bus_lookup
    net["cnpower_element_lookup"] = element_lookup

    for item in grouped["ext_grids"]:
        data = normalize_equipment("source_grid", item)
        idx = pp.create_ext_grid(
            net,
            bus=_resolve_bus(bus_lookup, item.get("bus")),
            vm_pu=float(data.get("vm_pu", 1.0)),
            va_degree=float(data.get("va_degree", 0.0)),
            name=data.get("name"),
            in_service=data.get("in_service", True),
        )
        _set_extra_columns(net.ext_grid, idx, data, ("s_sc_max_mva", "s_sc_min_mva", "rx_max", "rx_min", "r0x0_max", "x0x_max"))
        _register_lookup(element_lookup["ext_grid"], item, idx, "ext_grid")

    for item in grouped["lines"] + grouped["overhead_lines"]:
        equipment_type = item.get("equipment_type") or item.get("class") or "line_cable"
        data = normalize_equipment(equipment_type, item, context=item)
        idx = _create_line(pp, net, item, data)
        _register_lookup(element_lookup["line"], item, idx, "line")

    for item in grouped["transformers"]:
        data = normalize_equipment("transformer_2w", item)
        idx = _create_transformer(pp, net, item, data)
        _register_lookup(element_lookup["trafo"], item, idx, "trafo")

    for item in grouped["transformers_3w"]:
        data = normalize_equipment("transformer_3w", item)
        idx = _create_transformer3w(pp, net, item, data)
        _register_lookup(element_lookup["trafo3w"], item, idx, "trafo3w")

    for item in grouped["loads"] + grouped["ev_chargers"]:
        data = normalize_equipment(item.get("equipment_type") or item.get("class") or "load", item)
        idx = pp.create_load(
            net,
            bus=_resolve_bus(bus_lookup, item.get("bus")),
            p_mw=float(data.get("p_mw", 0.0)),
            q_mvar=float(data.get("q_mvar", 0.0)),
            name=data.get("name"),
            in_service=data.get("in_service", True),
        )
        _register_lookup(element_lookup["load"], item, idx, "load")

    for item in grouped["sgens"] + grouped["wind_turbines"]:
        data = normalize_equipment(item.get("equipment_type") or item.get("class") or "pv_inverter", item)
        idx = pp.create_sgen(
            net,
            bus=_resolve_bus(bus_lookup, item.get("bus")),
            p_mw=float(data.get("p_mw", 0.0)),
            q_mvar=float(data.get("q_mvar", 0.0)),
            sn_mva=data.get("sn_mva"),
            name=data.get("name"),
            in_service=data.get("in_service", True),
        )
        _register_lookup(element_lookup["sgen"], item, idx, "sgen")

    for item in grouped["storages"]:
        data = normalize_equipment("storage", item)
        idx = pp.create_storage(
            net,
            bus=_resolve_bus(bus_lookup, item.get("bus")),
            p_mw=float(data.get("p_mw", 0.0)),
            max_e_mwh=float(data.get("max_e_mwh", 0.0)),
            q_mvar=float(data.get("q_mvar", 0.0)),
            sn_mva=data.get("sn_mva"),
            soc_percent=float(data.get("soc_percent", 50.0)),
            min_e_mwh=float(data.get("min_e_mwh", 0.0)),
            name=data.get("name"),
            in_service=data.get("in_service", True),
        )
        _register_lookup(element_lookup["storage"], item, idx, "storage")

    for item in grouped["shunts"]:
        data = normalize_equipment("reactive_compensation", item)
        idx = pp.create_shunt(
            net,
            bus=_resolve_bus(bus_lookup, item.get("bus")),
            q_mvar=float(data.get("q_mvar", 0.0)),
            p_mw=float(data.get("p_mw", 0.0)),
            name=data.get("name"),
            in_service=data.get("in_service", True),
        )
        _register_lookup(element_lookup["shunt"], item, idx, "shunt")

    for item in grouped["switches"]:
        data = normalize_equipment(item.get("equipment_type") or item.get("class") or "switch_breaker", item)
        et = _switch_et(item)
        element_ref = _first_present(item, "element", "target", "target_element", "to_bus", "bus2")
        idx = pp.create_switch(
            net,
            bus=_resolve_bus(bus_lookup, item.get("bus")),
            element=_resolve_element(element_lookup, et, element_ref),
            et=et,
            closed=item.get("closed", True),
            type=_switch_type(data),
            name=data.get("name"),
            in_ka=first_number(data.get("in_ka"), float("nan")),
            z_ohm=first_number(data.get("z_ohm"), 0.0),
        )
        _register_lookup(element_lookup["switch"], item, idx, "switch")

    net["cnpower_bus_lookup"] = bus_lookup
    net["cnpower_element_lookup"] = element_lookup
    if run_powerflow:
        pp.runpp(net)
    return net


create_pandapower_net = build_pandapower_net
