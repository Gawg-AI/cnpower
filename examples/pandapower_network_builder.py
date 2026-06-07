import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cnpower.engineering import build_pandapower_net


def main():
    net = build_pandapower_net(
        {
            "buses": [
                {"id": "grid", "vn_kv": 10.0},
                {"id": "load_bus", "vn_kv": 0.4},
            ],
            "ext_grids": [{"bus": "grid", "vm_pu": 1.0}],
            "transformers": [
                {
                    "id": "t1",
                    "hv_bus": "grid",
                    "lv_bus": "load_bus",
                    "sn_kva": 630,
                    "vn_hv_kv": 10.0,
                    "vn_lv_kv": 0.4,
                    "vk_percent": 4.5,
                    "vkr_percent": 0.98,
                    "pfe_kw": 1.2,
                    "i0_percent": 0.4,
                }
            ],
            "loads": [{"id": "load-1", "bus": "load_bus", "p_mw": 0.18, "q_mvar": 0.05}],
            "switches": [
                {
                    "id": "sw-t1",
                    "bus": "grid",
                    "element": "t1",
                    "element_type": "transformer",
                    "closed": True,
                    "switch_type": "CB",
                }
            ],
        },
        run_powerflow=True,
    )
    print(f"converged={net.converged}")
    print(net.res_bus[["vm_pu", "va_degree"]])


if __name__ == "__main__":
    main()
