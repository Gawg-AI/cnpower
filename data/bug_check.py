import sys, os, traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

errors = []
warnings = []

def check(label, func):
    try:
        result = func()
        return result
    except Exception as e:
        errors.append(f"[{label}] {type(e).__name__}: {e}")
        traceback.print_exc()
        return None

print("=" * 60)
print("PHASE 1: Module Import & Syntax Check")
print("=" * 60)

modules_to_test = [
    ("transformers", "cn_dist_grid_lib.equipment.transformers", "get_all_transformers"),
    ("cables", "cn_dist_grid_lib.equipment.cables", "get_all_cables"),
    ("overhead_lines", "cn_dist_grid_lib.equipment.overhead_lines", "get_all_overhead_lines"),
    ("switchgear", "cn_dist_grid_lib.equipment.switchgear", "get_all_switchgear"),
    ("reactive_compensation", "cn_dist_grid_lib.equipment.reactive_compensation", "get_all_reactive_compensation"),
    ("protection", "cn_dist_grid_lib.equipment.protection", "get_all_protection"),
    ("instrument_transformers", "cn_dist_grid_lib.equipment.instrument_transformers", "get_all_instrument_transformers"),
    ("surge_arresters", "cn_dist_grid_lib.equipment.surge_arresters", "get_all_surge_arresters"),
    ("photovoltaic", "cn_dist_grid_lib.equipment.new_energy.photovoltaic", "get_all_photovoltaic"),
    ("wind_turbine", "cn_dist_grid_lib.equipment.new_energy.wind_turbine", "get_all_wind_turbines"),
    ("energy_storage", "cn_dist_grid_lib.equipment.new_energy.energy_storage", "get_all_energy_storage"),
    ("ev_charger", "cn_dist_grid_lib.equipment.new_energy.ev_charger", "get_all_ev_chargers"),
    ("connection_modes", "cn_dist_grid_lib.topology.connection_modes", "get_all_connection_modes"),
    ("validation_rules", "cn_dist_grid_lib.validation.rules", "get_all_validation_rules"),
    ("standards", "cn_dist_grid_lib.standards.references", "get_all_standards"),
]

data = {}
for label, module_path, func_name in modules_to_test:
    result = check(label, lambda m=module_path, f=func_name: getattr(__import__(m, fromlist=[f]), f)())
    if result is not None:
        data[label] = result
        print(f"  OK: {label}")
    else:
        print(f"  FAIL: {label}")

print()
print("=" * 60)
print("PHASE 2: Data Integrity Check")
print("=" * 60)

def check_dict_fields(data_dict, required_fields, label):
    missing_count = 0
    for name, params in data_dict.items():
        if not isinstance(params, dict):
            warnings.append(f"[{label}] {name}: value is not dict, got {type(params)}")
            continue
        for field in required_fields:
            if field not in params:
                missing_count += 1
                if missing_count <= 3:
                    warnings.append(f"[{label}] {name}: missing field '{field}'")
    if missing_count > 3:
        warnings.append(f"[{label}] ... and {missing_count - 3} more missing fields")
    return missing_count

if "transformers" in data:
    t = data["transformers"]
    print("  Transformers:")
    for cat in ["oil_immersed", "dry_type", "box_substation", "main_transformer_35kv", "main_transformer_110kv", "trafo3w_110kv"]:
        if cat in t:
            trafo_required = ["sn_kva", "vn_hv_kv", "vn_lv_kv", "vk_percent", "vkr_percent", "pfe_kw", "i0_percent", "standard", "source_note"]
            if cat == "trafo3w_110kv":
                trafo_required = ["sn_hv_mva", "sn_mv_mva", "sn_lv_mva", "vn_hv_kv", "vn_mv_kv", "vn_lv_kv", "standard", "source_note"]
            if cat == "box_substation":
                trafo_required = ["sn_kva", "vn_hv_kv", "vn_lv_kv", "standard", "source_note"]
            mc = check_dict_fields(t[cat], trafo_required, f"trafo.{cat}")
            print(f"    {cat}: {len(t[cat])} models, {mc} missing fields")
        else:
            errors.append(f"[transformers] Missing category: {cat}")
            print(f"    {cat}: MISSING CATEGORY!")

    for cat in ["oil_immersed", "dry_type"]:
        if cat in t:
            zero_seq_required = ["vk0_percent", "vkr0_percent", "mag0_percent", "mag0_rx", "si0_hv_partial"]
            mc = check_dict_fields(t[cat], zero_seq_required, f"trafo.{cat}.zero_seq")
            if mc > 0:
                print(f"    {cat} zero-seq: {mc} missing fields")
            tap_required = ["vector_group", "tap_side", "tap_neutral", "tap_min", "tap_max", "tap_step_percent"]
            mc2 = check_dict_fields(t[cat], tap_required, f"trafo.{cat}.tap")
            if mc2 > 0:
                print(f"    {cat} tap: {mc2} missing fields")

if "cables" in data:
    c = data["cables"]
    print("  Cables:")
    cable_required = ["r_ohm_per_km", "x_ohm_per_km", "c_nf_per_km", "max_i_ka_air", "max_i_ka_ground", "max_i_ka_duct", "standard", "source_note"]
    for cat in ["mv_10kv", "mv_35kv", "lv_04kv", "hv_110kv"]:
        if cat in c:
            mc = check_dict_fields(c[cat], cable_required, f"cable.{cat}")
            zero_seq_required = ["r0_ohm_per_km", "x0_ohm_per_km", "c0_nf_per_km"]
            mc2 = check_dict_fields(c[cat], zero_seq_required, f"cable.{cat}.zero_seq")
            print(f"    {cat}: {len(c[cat])} models, {mc} missing req, {mc2} missing zero-seq")
        else:
            errors.append(f"[cables] Missing category: {cat}")

if "overhead_lines" in data:
    o = data["overhead_lines"]
    print("  Overhead lines:")
    ohl_required = ["r_ohm_per_km", "c_nf_per_km", "max_i_ka", "standard", "source_note"]
    for cat in ["mv_10kv_insulated", "lv_04kv_insulated"]:
        if cat in o:
            mc = check_dict_fields(o[cat], ohl_required + ["x_ohm_per_km"], f"ohl.{cat}")
            print(f"    {cat}: {len(o[cat])} models, {mc} missing fields")
    if "bare_conductor" in o:
        bare_required = ["r_ohm_per_km", "x_ohm_per_km_table", "c_nf_per_km", "max_i_ka", "standard", "source_note"]
        mc = check_dict_fields(o["bare_conductor"], bare_required, f"ohl.bare_conductor")
        print(f"    bare_conductor: {len(o['bare_conductor'])} models, {mc} missing fields")

if "switchgear" in data:
    s = data["switchgear"]
    print("  Switchgear: %d categories" % len(s))

if "photovoltaic" in data:
    pv = data["photovoltaic"]
    print("  Photovoltaic:")
    for cat in ["pv_module", "string_inverter", "central_inverter"]:
        if cat in pv:
            if isinstance(pv[cat], dict):
                pv_req = ["standard", "source_note"]
                mc = check_dict_fields(pv[cat], pv_req, f"pv.{cat}")
                print(f"    {cat}: {len(pv[cat])} types, {mc} missing fields")
            else:
                print(f"    {cat}: {len(pv[cat])} items (list)")

print()
print("=" * 60)
print("PHASE 3: Pandapower Integration Check")
print("=" * 60)

from cn_dist_grid_lib.pandapower_integration.std_types_cn import (
    chinese_line_std_types, chinese_trafo_std_types,
    chinese_trafo3w_std_types, chinese_fuse_std_types
)

line_types = check("line_std_types", chinese_line_std_types)
trafo_types = check("trafo_std_types", chinese_trafo_std_types)
trafo3w_types = check("trafo3w_std_types", chinese_trafo3w_std_types)
fuse_types = check("fuse_std_types", chinese_fuse_std_types)

if line_types:
    print(f"  Line types: {len(line_types)}")
    line_required = ["r_ohm_per_km", "x_ohm_per_km", "c_nf_per_km", "max_i_ka"]
    bad_lines = []
    for name, params in line_types.items():
        for field in line_required:
            if field not in params:
                bad_lines.append(f"{name}.{field}")
            elif params[field] == 0.0 and field in ("r_ohm_per_km", "max_i_ka"):
                bad_lines.append(f"{name}.{field}=0.0")
    if bad_lines:
        for bl in bad_lines[:10]:
            warnings.append(f"[line_std] suspicious: {bl}")
        print(f"    {len(bad_lines)} suspicious entries (first 10 shown)")
    else:
        print(f"    All line types have required fields with non-zero values")

    cable_count = sum(1 for n in line_types if "YJV" in n or "VV" in n or "VLV" in n)
    ohl_count = sum(1 for n in line_types if "JKL" in n or "LJ" in n or "LGJ" in n or "TJ" in n or "BLV" in n)
    print(f"    Cable types: {cable_count}, Overhead types: {ohl_count}")
    if cable_count == 0:
        errors.append("[line_std] NO cable types found! Bug in chinese_line_std_types()")

if trafo_types:
    print(f"  Trafo types: {len(trafo_types)}")
    trafo_required = ["sn_mva", "vn_hv_kv", "vn_lv_kv", "vk_percent", "vkr_percent", "pfe_kw", "i0_percent", "shift_degree"]
    bad_trafos = []
    for name, params in trafo_types.items():
        for field in trafo_required:
            if field not in params:
                bad_trafos.append(f"{name}.{field}")
        if params.get("sn_mva", 0) == 0:
            bad_trafos.append(f"{name}.sn_mva=0")
        if params.get("vn_hv_kv", 0) == 0:
            bad_trafos.append(f"{name}.vn_hv_kv=0")
    if bad_trafos:
        for bt in bad_trafos[:10]:
            warnings.append(f"[trafo_std] issue: {bt}")
        print(f"    {len(bad_trafos)} issues found")
    else:
        print(f"    All trafo types OK")

    has_zero_seq = sum(1 for p in trafo_types.values() if "vk0_percent" in p)
    print(f"    {has_zero_seq}/{len(trafo_types)} have zero-sequence params")

if trafo3w_types:
    print(f"  Trafo3w types: {len(trafo3w_types)}")
    trafo3w_required = ["sn_hv_mva", "sn_mv_mva", "sn_lv_mva", "vn_hv_kv", "vn_mv_kv", "vn_lv_kv",
                        "vk_hv_percent", "vk_mv_percent", "vk_lv_percent"]
    bad = [f"{n}.{f}" for n, p in trafo3w_types.items() for f in trafo3w_required if f not in p]
    if bad:
        for b in bad[:10]:
            warnings.append(f"[trafo3w_std] missing: {b}")
    else:
        print(f"    All trafo3w types OK")

if fuse_types:
    print(f"  Fuse types: {len(fuse_types)}")
    bad_fuses = [f"{n}.{f}" for n, p in fuse_types.items() for f in ["fuse_type", "i_rated_a"] if f not in p]
    if bad_fuses:
        for bf in bad_fuses[:5]:
            warnings.append(f"[fuse_std] missing: {bf}")
    else:
        print(f"    All fuse types OK")

print()
print("=" * 60)
print("PHASE 4: __init__.py Import Chain Check")
print("=" * 60)

try:
    import cn_dist_grid_lib
    print("  cn_dist_grid_lib: OK")
    print(f"    version: {cn_dist_grid_lib.__version__}")
except Exception as e:
    errors.append(f"[__init__] {e}")
    print(f"  cn_dist_grid_lib: FAIL - {e}")

try:
    from cn_dist_grid_lib.equipment import get_all_transformers, get_all_cables, get_all_overhead_lines
    from cn_dist_grid_lib.equipment import get_all_switchgear, get_all_reactive_compensation, get_all_protection
    from cn_dist_grid_lib.equipment import get_all_instrument_transformers, get_all_surge_arresters
    print("  equipment sub-imports: OK")
except Exception as e:
    errors.append(f"[equipment.__init__] {e}")
    print(f"  equipment sub-imports: FAIL - {e}")

try:
    from cn_dist_grid_lib.equipment.new_energy import get_all_photovoltaic, get_all_wind_turbines
    from cn_dist_grid_lib.equipment.new_energy import get_all_energy_storage, get_all_ev_chargers
    print("  new_energy sub-imports: OK")
except Exception as e:
    errors.append(f"[new_energy.__init__] {e}")
    print(f"  new_energy sub-imports: FAIL - {e}")

try:
    from cn_dist_grid_lib.topology import get_all_connection_modes
    from cn_dist_grid_lib.validation import get_all_validation_rules
    from cn_dist_grid_lib.standards import get_all_standards
    print("  topology/validation/standards imports: OK")
except Exception as e:
    errors.append(f"[topology/validation/standards] {e}")
    print(f"  topology/validation/standards imports: FAIL - {e}")

try:
    from cn_dist_grid_lib.pandapower_integration import add_chinese_std_types
    print("  pandapower_integration import: OK")
except Exception as e:
    errors.append(f"[pandapower_integration.__init__] {e}")
    print(f"  pandapower_integration import: FAIL - {e}")

print()
print("=" * 60)
print("PHASE 5: Value Sanity Check")
print("=" * 60)

if "transformers" in data:
    t = data["transformers"]
    for cat in ["oil_immersed", "dry_type"]:
        if cat in t:
            for name, p in t[cat].items():
                if isinstance(p, dict):
                    if p.get("vk_percent", 0) <= 0:
                        errors.append(f"[sanity] {name}: vk_percent={p.get('vk_percent')}")
                    if p.get("pfe_kw", 0) < 0:
                        errors.append(f"[sanity] {name}: pfe_kw={p.get('pfe_kw')} negative!")
                    if p.get("sn_kva", 0) <= 0:
                        errors.append(f"[sanity] {name}: sn_kva={p.get('sn_kva')}")

if "cables" in data:
    c = data["cables"]
    for cat in ["mv_10kv", "mv_35kv", "lv_04kv", "hv_110kv"]:
        if cat in c:
            for name, p in c[cat].items():
                if isinstance(p, dict):
                    if p.get("r_ohm_per_km", 0) <= 0:
                        errors.append(f"[sanity] {name}: r_ohm_per_km={p.get('r_ohm_per_km')}")
                    if p.get("max_i_ka_ground", 0) <= 0 and p.get("max_i_ka_air", 0) <= 0:
                        errors.append(f"[sanity] {name}: all ampacity=0")

if line_types:
    for name, p in line_types.items():
        if p.get("r_ohm_per_km", 0) <= 0:
            errors.append(f"[sanity.line] {name}: r_ohm_per_km=0")
        if p.get("max_i_ka", 0) <= 0:
            errors.append(f"[sanity.line] {name}: max_i_ka=0")

if trafo_types:
    for name, p in trafo_types.items():
        if p.get("sn_mva", 0) <= 0:
            errors.append(f"[sanity.trafo] {name}: sn_mva=0 or missing")

print("  Sanity checks complete")

print()
print("=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"  ERRORS:   {len(errors)}")
print(f"  WARNINGS: {len(warnings)}")

if errors:
    print("\n  --- ERRORS ---")
    for e in errors:
        print(f"    {e}")

if warnings:
    print("\n  --- WARNINGS (first 30) ---")
    for w in warnings[:30]:
        print(f"    {w}")

if not errors and not warnings:
    print("\n  ALL CHECKS PASSED - NO BUGS FOUND!")
