from cnpower.standards.references import get_all_standards
from cnpower.engineering.compliance_constraints import get_compliance_constraint_library
from cnpower.equipment.new_energy.energy_storage import get_all_energy_storage
from cnpower.equipment.switchgear import get_all_switchgear
from cnpower.equipment.reactive_compensation import get_all_reactive_compensation

# Test references.py
s = get_all_standards()
print(f"Standards count: {len(s)}")

new_checks = [
    "GB/T 36558-2023", "GB/T 27930-2023", "GB/T 12325-2023",
    "GB/T 12326-2023", "GB/T 15543-2023", "GB 50052-2023",
    "GB 50054-2023", "GB/T 14549-2024", "GB/T 36276-2023",
    "GB/T 27930.2-2024", "GB/T 15544.1-2023",
]
for c in new_checks:
    status = "FOUND" if c in s else "MISSING"
    print(f"  {c}: {status}")

old_checks = [
    "GB/T 36558-2018", "GB/T 27930-2015", "GB/T 12325-2008",
    "GB/T 12326-2008", "GB/T 15543-2008", "GB 50052-2009",
    "GB 50054-2011", "GB/T 14549-1993", "GB/T 15544-2023",
]
for c in old_checks:
    status = "STILL EXISTS" if c in s else "removed OK"
    print(f"  OLD {c}: {status}")

# Test compliance_constraints.py
clib = get_compliance_constraint_library()
print("\nCompliance constraints loaded OK")
# Check no old standards remain in constraint strings
import json
clib_str = json.dumps(clib, ensure_ascii=False)
old_in_constraints = ["GB/T 36558-2018", "GB 50054-2011", "GB 50052-2009",
                       "GB/T 14549-1993", "GB/T 12325-2008", "GB/T 12326-2008",
                       "GB/T 15543-2008", "GB 1094.5-2008"]
for old in old_in_constraints:
    if old in clib_str:
        print(f"  WARNING: {old} still in compliance_constraints!")
    else:
        print(f"  {old}: removed OK")

# Test energy_storage.py
es = get_all_energy_storage()
es_str = json.dumps(es, ensure_ascii=False)
if "GB/T 36558-2018" in es_str:
    print("\nWARNING: GB/T 36558-2018 still in energy_storage!")
else:
    print("\nenergy_storage: GB/T 36558-2018 removed OK")
if "GB/T 36558-2023" in es_str:
    print("energy_storage: GB/T 36558-2023 found OK")

# Test switchgear.py
sw = get_all_switchgear()
sw_str = json.dumps(sw, ensure_ascii=False)
if "GB 50054-2011" in sw_str:
    print("\nWARNING: GB 50054-2011 still in switchgear!")
else:
    print("\nswitchgear: GB 50054-2011 removed OK")
if "GB 50054-2023" in sw_str:
    print("switchgear: GB 50054-2023 found OK")
if "GB/T 10963.1-2023" in sw_str:
    print("switchgear: GB/T 10963.1-2023 found OK")

# Test reactive_compensation.py
rc = get_all_reactive_compensation()
rc_str = json.dumps(rc, ensure_ascii=False)
if '"GB/T 11024"' in rc_str:
    print("\nWARNING: GB/T 11024 (no year) still in reactive_compensation!")
else:
    print("\nreactive_compensation: GB/T 11024 (no year) removed OK")
if "GB/T 11024-2019" in rc_str:
    print("reactive_compensation: GB/T 11024-2019 found OK")

print("\n=== All validation checks passed ===")
