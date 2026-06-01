import json
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from cn_dist_grid_lib.equipment.transformers import get_all_transformers
from cn_dist_grid_lib.equipment.cables import get_all_cables
from cn_dist_grid_lib.equipment.overhead_lines import get_all_overhead_lines
from cn_dist_grid_lib.equipment.switchgear import get_all_switchgear
from cn_dist_grid_lib.equipment.reactive_compensation import get_all_reactive_compensation
from cn_dist_grid_lib.equipment.protection import get_all_protection
from cn_dist_grid_lib.equipment.instrument_transformers import get_all_instrument_transformers
from cn_dist_grid_lib.equipment.surge_arresters import get_all_surge_arresters
from cn_dist_grid_lib.equipment.new_energy.photovoltaic import get_all_photovoltaic
from cn_dist_grid_lib.equipment.new_energy.wind_turbine import get_all_wind_turbines
from cn_dist_grid_lib.equipment.new_energy.energy_storage import get_all_energy_storage
from cn_dist_grid_lib.equipment.new_energy.ev_charger import get_all_ev_chargers
from cn_dist_grid_lib.topology.connection_modes import get_all_connection_modes
from cn_dist_grid_lib.validation.rules import get_all_validation_rules
from cn_dist_grid_lib.standards.references import get_all_standards
from cn_dist_grid_lib.engineering import get_all_engineering_parameters

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
VERSION = "1.0.0"
TIMESTAMP = datetime.now().isoformat()

def _convert(obj):
    if isinstance(obj, dict):
        return {str(k): _convert(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [_convert(i) for i in obj]
    elif isinstance(obj, (int, float, str, bool, type(None))):
        return obj
    elif isinstance(obj, set):
        return list(obj)
    return str(obj)

def _write_json(filename, data):
    filepath = os.path.join(DATA_DIR, filename)
    payload = {
        "version": VERSION,
        "generated_at": TIMESTAMP,
        "data": _convert(data)
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=str)
    print(f"  OK: {filename} ({os.path.getsize(filepath)} bytes)")

def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    print("Generating JSON data files...")

    _write_json("transformers.json", get_all_transformers())
    _write_json("cables.json", get_all_cables())
    _write_json("overhead_lines.json", get_all_overhead_lines())
    _write_json("switchgear.json", get_all_switchgear())
    _write_json("reactive_compensation.json", get_all_reactive_compensation())
    _write_json("protection.json", get_all_protection())
    _write_json("instrument_transformers.json", get_all_instrument_transformers())
    _write_json("surge_arresters.json", get_all_surge_arresters())
    _write_json("photovoltaic.json", get_all_photovoltaic())
    _write_json("wind_turbine.json", get_all_wind_turbines())
    _write_json("energy_storage.json", get_all_energy_storage())
    _write_json("ev_charger.json", get_all_ev_chargers())
    _write_json("connection_modes.json", get_all_connection_modes())
    _write_json("validation_rules.json", get_all_validation_rules())
    _write_json("standards.json", get_all_standards())
    _write_json("engineering_parameters.json", get_all_engineering_parameters())

    print(f"\nDone! 16 JSON files generated in {DATA_DIR}")

if __name__ == "__main__":
    main()
