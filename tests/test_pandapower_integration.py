import pytest

pp = pytest.importorskip("pandapower")

from cnpower.engineering import build_pandapower_net
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
                    "vn_hv_kv": "10kV",
                    "vn_lv_kv": "400V",
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
