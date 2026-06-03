from .normalization import normalize_equipment
from ..pandapower_integration import add_chinese_std_types


BUS_CLASSES = {"bus", "busbar"}
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


def _split_assets(model):
    grouped = {"buses": _as_list(model.get("buses") or model.get("busbars"))}
    for group_name, _canonical in ELEMENT_GROUPS.values():
        grouped[group_name] = _as_list(model.get(group_name))

    for asset in _as_list(model.get("assets")):
        if not isinstance(asset, dict):
            continue
        asset_class = asset.get("class") or asset.get("equipment_type") or asset.get("type")
        if asset_class in BUS_CLASSES:
            grouped["buses"].append(asset)
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


def _set_extra_columns(table, index, values, keys):
    for key in keys:
        if key in values and values[key] is not None:
            table.loc[index, key] = values[key]


def build_pandapower_net(model, *, add_std_types=True, run_powerflow=False):
    pp = _require_pandapower()
    net = pp.create_empty_network(sn_mva=model.get("sn_mva", 100.0))
    if add_std_types:
        add_chinese_std_types(net)

    grouped = _split_assets(model)
    bus_lookup = {}
    for bus in grouped["buses"]:
        if not isinstance(bus, dict):
            continue
        vn_kv = bus.get("vn_kv") or bus.get("rated_voltage_kv")
        if vn_kv is None:
            raise ValueError(f"Bus {bus!r} is missing vn_kv")
        idx = pp.create_bus(
            net,
            vn_kv=float(vn_kv),
            name=bus.get("name") or bus.get("id"),
            in_service=bus.get("in_service", True),
            type=bus.get("bus_type", "b"),
            zone=bus.get("zone"),
        )
        identifier = _bus_id(bus)
        if identifier is not None:
            bus_lookup[identifier] = idx

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

    for item in grouped["lines"] + grouped["overhead_lines"]:
        equipment_type = item.get("equipment_type") or item.get("class") or "line_cable"
        data = normalize_equipment(equipment_type, item, context=item)
        pp.create_line(
            net,
            from_bus=_resolve_bus(bus_lookup, item.get("from_bus") or item.get("from")),
            to_bus=_resolve_bus(bus_lookup, item.get("to_bus") or item.get("to")),
            length_km=float(data["length_km"]),
            std_type=data["std_type"],
            name=data.get("name"),
            in_service=data.get("in_service", True),
            df=float(data.get("df", 1.0)),
            parallel=int(data.get("parallel", 1)),
        )

    for item in grouped["transformers"]:
        data = normalize_equipment("transformer_2w", item)
        pp.create_transformer(
            net,
            hv_bus=_resolve_bus(bus_lookup, item.get("hv_bus")),
            lv_bus=_resolve_bus(bus_lookup, item.get("lv_bus")),
            std_type=data["std_type"],
            name=data.get("name"),
            in_service=data.get("in_service", True),
        )

    for item in grouped["transformers_3w"]:
        data = normalize_equipment("transformer_3w", item)
        pp.create_transformer3w(
            net,
            hv_bus=_resolve_bus(bus_lookup, item.get("hv_bus")),
            mv_bus=_resolve_bus(bus_lookup, item.get("mv_bus")),
            lv_bus=_resolve_bus(bus_lookup, item.get("lv_bus")),
            std_type=data["std_type"],
            name=data.get("name"),
            in_service=data.get("in_service", True),
        )

    for item in grouped["loads"] + grouped["ev_chargers"]:
        data = normalize_equipment(item.get("equipment_type") or item.get("class") or "load", item)
        pp.create_load(
            net,
            bus=_resolve_bus(bus_lookup, item.get("bus")),
            p_mw=float(data.get("p_mw", 0.0)),
            q_mvar=float(data.get("q_mvar", 0.0)),
            name=data.get("name"),
            in_service=data.get("in_service", True),
        )

    for item in grouped["sgens"] + grouped["wind_turbines"]:
        data = normalize_equipment(item.get("equipment_type") or item.get("class") or "pv_inverter", item)
        pp.create_sgen(
            net,
            bus=_resolve_bus(bus_lookup, item.get("bus")),
            p_mw=float(data.get("p_mw", 0.0)),
            q_mvar=float(data.get("q_mvar", 0.0)),
            sn_mva=data.get("sn_mva"),
            name=data.get("name"),
            in_service=data.get("in_service", True),
        )

    for item in grouped["storages"]:
        data = normalize_equipment("storage", item)
        pp.create_storage(
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

    for item in grouped["shunts"]:
        data = normalize_equipment("reactive_compensation", item)
        pp.create_shunt(
            net,
            bus=_resolve_bus(bus_lookup, item.get("bus")),
            q_mvar=float(data.get("q_mvar", 0.0)),
            p_mw=float(data.get("p_mw", 0.0)),
            name=data.get("name"),
            in_service=data.get("in_service", True),
        )

    for item in grouped["switches"]:
        data = normalize_equipment(item.get("equipment_type") or item.get("class") or "switch_breaker", item)
        pp.create_switch(
            net,
            bus=_resolve_bus(bus_lookup, item.get("bus")),
            element=_resolve_bus(bus_lookup, item.get("element")) if item.get("et", "b") == "b" else int(item.get("element")),
            et=item.get("et", "b"),
            closed=item.get("closed", True),
            type=data.get("switch_type") or data.get("type"),
            name=data.get("name"),
        )

    net.cnpower_bus_lookup = bus_lookup
    if run_powerflow:
        pp.runpp(net)
    return net


create_pandapower_net = build_pandapower_net
