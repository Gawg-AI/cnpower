import math


def get_all_reactive_compensation():
    omega = 2 * math.pi * 50

    capacitor_mv = {}
    mv_delta_capacities = [30, 50, 75, 100]
    for q in mv_delta_capacities:
        v_kv = 10
        c_uf = round(q * 1000 / (omega * (v_kv * 1000) ** 2) * 1e6, 2)
        key = f"MV-{q}kvar-{v_kv:g}kV"
        capacitor_mv[key] = {
            "model_series": "BSMJ",
            "rated_voltage_kv": v_kv,
            "rated_capacity_kvar": q,
            "rated_capacitance_uf": c_uf,
            "dielectric_loss_percent": 0.05,
            "phase_count": 3,
            "connection_type": "delta",
            "standard": "GB/T 11024",
            "source_note": "BSMJ系列10kV并联电容器典型参数(角型接法)"
        }

    mv_star_capacities = [150, 200, 250, 300, 400, 500, 600]
    for q in mv_star_capacities:
        v_kv = round(11 / math.sqrt(3), 2)
        c_uf = round(q * 1000 / (omega * (v_kv * 1000) ** 2) * 1e6, 2)
        key = f"MV-{q}kvar-{v_kv:g}kV"
        capacitor_mv[key] = {
            "model_series": "BSMJ",
            "rated_voltage_kv": v_kv,
            "rated_capacity_kvar": q,
            "rated_capacitance_uf": c_uf,
            "dielectric_loss_percent": 0.05,
            "phase_count": 3,
            "connection_type": "star",
            "standard": "GB/T 11024",
            "source_note": "BSMJ系列10kV并联电容器典型参数(星型接法)"
        }

    capacitor_lv = {}
    lv_capacities = [5, 10, 15, 20, 25, 30, 40, 50, 60]
    for q in lv_capacities:
        v_kv = 0.45
        c_uf = round(q * 1000 / (omega * (v_kv * 1000) ** 2) * 1e6, 2)
        key = f"LV-{q}kvar-{v_kv:g}kV"
        capacitor_lv[key] = {
            "model_series": "BSMJ",
            "rated_voltage_kv": v_kv,
            "rated_capacity_kvar": q,
            "rated_capacitance_uf": c_uf,
            "dielectric_loss_percent": 0.10,
            "phase_count": 3,
            "connection_type": "delta",
            "standard": "GB/T 12747.1-2017",
            "source_note": "BSMJ系列0.4kV自愈式并联电容器典型参数"
        }

    svg = {}
    svg_specs = [
        (50, 0.4, 5, 97.0, 5.0),
        (100, 0.4, 5, 97.0, 5.0),
        (200, 0.4, 5, 97.5, 5.0),
        (300, 0.4, 5, 97.5, 5.0),
        (500, 0.4, 3, 98.0, 3.0),
        (1000, 10, 3, 98.0, 3.0),
        (2000, 10, 3, 98.5, 3.0),
        (5000, 10, 2, 99.0, 3.0),
        (10000, 10, 2, 99.0, 3.0),
    ]
    for cap, v_kv, resp_ms, eff_pct, harm_pct in svg_specs:
        key = f"SVG-{cap}kvar-{v_kv:g}kV"
        svg[key] = {
            "rated_capacity_kvar": cap,
            "rated_voltage_kv": v_kv,
            "response_time_ms": resp_ms,
            "efficiency_percent": eff_pct,
            "harmonic_content_percent": harm_pct,
            "standard": "NB/T 10994-2022",
            "source_note": "SVG静止无功发生器典型参数"
        }

    return {
        "capacitor_mv": capacitor_mv,
        "capacitor_lv": capacitor_lv,
        "svg": svg,
    }
