import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT_DIR)

from cn_dist_grid_lib.engineering import get_all_engineering_parameters
from cn_dist_grid_lib.engineering.compliance_checker import check_basic_equipment_compliance


params = get_all_engineering_parameters()
asset_classes = params["asset_schema"]["classes"]
planning = params["planning_assumptions"]
bridge = params["pandapower_bridge"]
constraints = params["compliance_constraints"]

required_asset_keys = ["display_name", "palette_group", "pandapower_element", "ports", "required_fields", "calculations", "connection_rules"]
missing = []
for class_name, spec in asset_classes.items():
    for key in required_asset_keys:
        if key not in spec:
            missing.append(f"{class_name}.{key}")

print("=== Engineering Parameter Library Verification ===")
print("Asset classes: %d" % len(asset_classes))
print("Planning scenarios: %d" % len(planning["planning_scenarios"]))
print("Comparison metric groups: %d" % len(planning["comparison_metrics"]))
print("Pandapower mapped elements: %d" % len(bridge["element_mapping"]))
print("Completeness requirement groups: %d" % len(bridge["data_completeness_requirements"]))
print("Compliance equipment types: %d" % len(constraints["constraints_by_equipment_type"]))
print("Equipment library mappings: %d" % len(constraints["equipment_library_mapping"]))

if missing:
    raise SystemExit("Missing required schema keys: " + ", ".join(missing))

for must_have in ("transformer_2w", "line_cable", "pv_inverter", "storage", "ev_charger", "ring_main_unit"):
    if must_have not in asset_classes:
        raise SystemExit("Missing key asset class: " + must_have)

for must_have in ("switch_breaker", "line_cable", "transformer_2w", "pv_inverter", "storage", "ev_charger"):
    if must_have not in constraints["constraints_by_equipment_type"]:
        raise SystemExit("Missing compliance type: " + must_have)

sample = check_basic_equipment_compliance(
    "switch_breaker",
    {
        "rated_voltage_kv": 12,
        "rated_current_a": 630,
        "rated_short_circuit_breaking_ka": 25,
        "rated_short_circuit_making_ka": 63,
        "rated_short_time_withstand_ka_4s": 25,
    },
    {
        "operating_voltage_kv": 10,
        "max_current_a": 400,
        "ikss_ka": 20,
        "ip_ka": 50,
        "ith_ka": 20,
    },
)
if not all(f["passed"] for f in sample["basic_findings"]):
    raise SystemExit("Sample switch breaker compliance check failed")

print("=== ENGINEERING LIBRARY VERIFIED OK ===")
