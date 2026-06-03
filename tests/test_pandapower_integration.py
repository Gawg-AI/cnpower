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
