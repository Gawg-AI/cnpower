import pytest

pp = pytest.importorskip("pandapower")

from cnpower.engineering import build_pandapower_net
import cnpower.engineering.network_builder as network_builder
from cnpower.pandapower_integration import add_chinese_std_types, list_chinese_std_types


def test_chinese_std_types_can_run_powerflow():
    net = pp.create_empty_network()
    add_chinese_std_types(net)

    hv = pp.create_bus(net, vn_kv=10.0, name="10kV")
    lv = pp.create_bus(net, vn_kv=0.4, name="0.4kV")
    pp.create_ext_grid(net, hv, vm_pu=1.0)
    pp.create_transformer(net, hv, lv, std_type="S13-630/10")
    pp.create_load(net, lv, p_mw=0.2, q_mvar=0.06)

    pp.runpp(net)

    assert net.converged
    assert "S13-630/10" in list_chinese_std_types(net)["trafo"]


def test_engineering_builder_creates_runnable_network():
    net = build_pandapower_net(
        {
            "buses": [
                {"id": "grid", "vn_kv": 10.0},
                {"id": "load_bus", "vn_kv": 0.4},
            ],
            "ext_grids": [
                {"bus": "grid", "vm_pu": 1.0, "s_sc_max_mva": 300, "s_sc_min_mva": 120, "rx_max": 0.1, "rx_min": 0.1},
            ],
            "transformers": [
                {"hv_bus": "grid", "lv_bus": "load_bus", "std_type": "S13-630/10"},
            ],
            "loads": [
                {"bus": "load_bus", "p_mw": 0.18, "q_mvar": 0.05},
            ],
        },
        run_powerflow=True,
    )

    assert net.converged
    assert len(net.bus) == 2
    assert len(net.trafo) == 1
    assert net["cnpower_bus_lookup"]["grid"] == 0


def test_engineering_builder_supports_lines_and_sgens():
    net = build_pandapower_net(
        {
            "buses": [
                {"id": "slack", "vn_kv": 10.0},
                {"id": "feeder", "vn_kv": 10.0},
            ],
            "ext_grids": [{"bus": "slack", "vm_pu": 1.0}],
            "lines": [
                {"from_bus": "slack", "to_bus": "feeder", "length_km": 1.2, "std_type": "YJV22-3x70-10kV"},
            ],
            "sgens": [
                {"bus": "feeder", "equipment_type": "pv_inverter", "rated_power_kw": 80, "power_factor": 0.98},
            ],
            "loads": [
                {"bus": "feeder", "p_mw": 0.12, "q_mvar": 0.03},
            ],
        },
        run_powerflow=True,
    )

    assert net.converged
    assert len(net.line) == 1
    assert len(net.sgen) == 1


def test_engineering_builder_defaults_wind_turbines_to_wind_type(monkeypatch):
    seen_equipment_types = []
    real_normalize_equipment = network_builder.normalize_equipment

    def spy_normalize_equipment(equipment_type, equipment, **kwargs):
        if equipment.get("id") == "wind-a":
            seen_equipment_types.append(equipment_type)
        return real_normalize_equipment(equipment_type, equipment, **kwargs)

    monkeypatch.setattr(network_builder, "normalize_equipment", spy_normalize_equipment)

    net = network_builder.build_pandapower_net(
        {
            "buses": [{"id": "feeder", "vn_kv": 10.0}],
            "wind_turbines": [
                {"id": "wind-a", "bus": "feeder", "rated_power_kw": 50, "power_factor": 0.95},
            ],
        },
        add_std_types=False,
    )

    assert seen_equipment_types == ["wind_turbine"]
    assert len(net.sgen) == 1


def test_engineering_builder_supports_parameterized_lines_and_voltage_aliases():
    net = build_pandapower_net(
        {
            "buses": [
                {"id": "slack", "voltage_rating": "10kV"},
                {"id": "feeder", "rated_voltage_v": 10000},
            ],
            "ext_grids": [{"bus": "slack", "vm_pu": 1.0}],
            "lines": [
                {
                    "from_bus": "slack",
                    "to_bus": "feeder",
                    "length_km": 0.8,
                    "r_ohm_per_km": 0.268,
                    "x_ohm_per_km": 0.09,
                    "c_nf_per_km": 200,
                    "max_i_ka_air": 0.21,
                    "max_i_ka_ground": 0.185,
                    "laying_method": "air",
                },
            ],
            "loads": [{"bus": "feeder", "p_mw": 0.05, "q_mvar": 0.01}],
        },
        run_powerflow=True,
    )

    assert net.converged
    assert len(net.line) == 1
    assert net.line.at[0, "std_type"] is None
    assert net.line.at[0, "max_i_ka"] == 0.21


def test_engineering_builder_resolves_switch_element_references_by_asset_id():
    net = build_pandapower_net(
        {
            "buses": [
                {"id": "slack", "vn_kv": 10.0},
                {"id": "feeder", "vn_kv": 10.0},
            ],
            "ext_grids": [{"bus": "slack", "vm_pu": 1.0}],
            "lines": [
                {
                    "id": "line-1",
                    "from_bus": "slack",
                    "to_bus": "feeder",
                    "length_km": 1.0,
                    "std_type": "YJV22-3x70-10kV",
                },
            ],
            "switches": [
                {
                    "id": "sw-line-1",
                    "bus": "slack",
                    "element": "line-1",
                    "element_type": "line",
                    "switch_type": "CB",
                    "closed": True,
                    "in_ka": 25,
                },
            ],
            "loads": [{"bus": "feeder", "p_mw": 0.05, "q_mvar": 0.01}],
        },
        run_powerflow=True,
    )

    assert net.converged
    assert net.switch.at[0, "et"] == "l"
    assert net.switch.at[0, "element"] == 0
    assert net.switch.at[0, "in_ka"] == 25
    assert net["cnpower_element_lookup"]["line"]["line-1"] == 0
    assert net["cnpower_element_lookup"]["switch"]["sw-line-1"] == 0


def test_engineering_builder_routes_flat_assets_with_class_aliases():
    net = build_pandapower_net(
        {
            "assets": [
                {"id": "grid", "class": "busbar", "vn_kv": 10.0},
                {"id": "feeder", "class": "busbar", "vn_kv": 10.0},
                {"id": "source", "class": "source_grid", "bus": "grid", "vm_pu": 1.0},
                {
                    "id": "line-a",
                    "class": "line",
                    "from_bus": "grid",
                    "to_bus": "feeder",
                    "length_km": 1.0,
                    "std_type": "YJV22-3x70-10kV",
                },
                {
                    "id": "disc-a",
                    "class": "disconnector",
                    "bus": "grid",
                    "element": "line-a",
                    "element_type": "line",
                    "closed": True,
                },
                {"id": "load-a", "class": "load", "bus": "feeder", "p_mw": 0.05, "q_mvar": 0.01},
            ],
        },
        run_powerflow=True,
    )

    assert net.converged
    assert len(net.line) == 1
    assert len(net.switch) == 1
    assert net.switch.at[0, "type"] == "LS"
    assert net["cnpower_element_lookup"]["line"]["line-a"] == 0


def test_engineering_builder_rejects_duplicate_asset_references():
    with pytest.raises(ValueError, match="Duplicate bus reference"):
        build_pandapower_net(
            {
                "buses": [
                    {"id": "dup", "vn_kv": 10.0},
                    {"id": "dup", "vn_kv": 10.0},
                ],
            }
        )


def test_engineering_builder_supports_parameterized_transformers():
    net = build_pandapower_net(
        {
            "buses": [
                {"id": "grid", "vn_kv": "10kV"},
                {"id": "load_bus", "vn_kv": "0.4kV"},
            ],
            "ext_grids": [{"bus": "grid", "vm_pu": 1.0}],
            "transformers": [
                {
                    "hv_bus": "grid",
                    "lv_bus": "load_bus",
                    "sn_kva": 630,
                    "vn_hv_v": 10000,
                    "rated_voltage_lv_v": 400,
                    "vk_percent": 4.5,
                    "vkr_percent": 0.98,
                    "pfe_kw": 1.2,
                    "i0_percent": 0.4,
                }
            ],
            "loads": [{"bus": "load_bus", "p_mw": 0.18, "q_mvar": 0.05}],
        },
        run_powerflow=True,
    )

    assert net.converged
    assert len(net.trafo) == 1
    assert net.trafo.at[0, "std_type"] is None
    assert net.trafo.at[0, "sn_mva"] == 0.63


def test_engineering_builder_supports_parameterized_three_winding_transformers():
    net = build_pandapower_net(
        {
            "buses": [
                {"id": "grid", "vn_kv": "110kV"},
                {"id": "mv", "vn_kv": "20kV"},
                {"id": "lv", "vn_kv": "10kV"},
            ],
            "ext_grids": [{"bus": "grid", "vm_pu": 1.0}],
            "transformers_3w": [
                {
                    "hv_bus": "grid",
                    "mv_bus": "mv",
                    "lv_bus": "lv",
                    "sn_hv_mva": 40,
                    "sn_mv_mva": 15,
                    "sn_lv_mva": 25,
                    "vn_hv_kv": "110kV",
                    "vn_mv_kv": "20kV",
                    "vn_lv_kv": "10kV",
                    "vk_hv_percent": 10.1,
                    "vk_mv_percent": 10.1,
                    "vk_lv_percent": 10.1,
                    "vkr_hv_percent": 0.266667,
                    "vkr_mv_percent": 0.033333,
                    "vkr_lv_percent": 0.04,
                    "shift_mv_degree": 30,
                    "shift_lv_degree": 30,
                }
            ],
            "loads": [
                {"bus": "mv", "p_mw": 2.0, "q_mvar": 0.5},
                {"bus": "lv", "p_mw": 1.0, "q_mvar": 0.2},
            ],
        },
        run_powerflow=True,
    )

    assert net.converged
    assert len(net.trafo3w) == 1
    assert net.trafo3w.at[0, "std_type"] is None
    assert net.trafo3w.at[0, "sn_hv_mva"] == 40


def test_short_circuit_entrypoint_runs_with_chinese_types():
    sc = pytest.importorskip("pandapower.shortcircuit")
    net = build_pandapower_net(
        {
            "buses": [
                {"id": "grid", "vn_kv": 10.0},
                {"id": "feeder", "vn_kv": 10.0},
            ],
            "ext_grids": [
                {
                    "bus": "grid",
                    "vm_pu": 1.0,
                    "s_sc_max_mva": 300,
                    "s_sc_min_mva": 120,
                    "rx_max": 0.1,
                    "rx_min": 0.1,
                    "r0x0_max": 0.1,
                    "x0x_max": 1.0,
                }
            ],
            "lines": [
                {"from_bus": "grid", "to_bus": "feeder", "length_km": 1.0, "std_type": "YJV22-3x70-10kV"},
            ],
        }
    )

    sc.calc_sc(net, fault="3ph", case="max", ip=True, ith=True)

    assert "ikss_ka" in net.res_bus_sc.columns
    assert float(net.res_bus_sc["ikss_ka"].max()) > 0
