import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from cn_dist_grid_lib.pandapower_integration.std_types_cn import (
    chinese_line_std_types, chinese_trafo_std_types,
    chinese_trafo3w_std_types, chinese_fuse_std_types
)

line_types = chinese_line_std_types()
trafo_types = chinese_trafo_std_types()
trafo3w_types = chinese_trafo3w_std_types()
fuse_types = chinese_fuse_std_types()

print("=== Pandapower Integration Verification ===")
print("Line types: %d" % len(line_types))
print("Trafo types: %d" % len(trafo_types))
print("Trafo3w types: %d" % len(trafo3w_types))
print("Fuse types: %d" % len(fuse_types))

cable_names = [n for n in line_types if "YJV" in n or "VV" in n or "VLV" in n]
ohl_names = [n for n in line_types if "JKL" in n or "LJ" in n or "LGJ" in n or "TJ" in n or "BLV" in n]
print("  Cable line types: %d" % len(cable_names))
print("  Overhead line types: %d" % len(ohl_names))

if "YJV22-3x120-10kV" in line_types:
    t = line_types["YJV22-3x120-10kV"]
    print("  YJV22-3x120-10kV: r=%.3f x=%.3f c=%.0f max_i=%.3f" % (
        t["r_ohm_per_km"], t["x_ohm_per_km"], t["c_nf_per_km"], t["max_i_ka"]))
else:
    print("  ERROR: YJV22-3x120-10kV not found!")

if "S11-315/10" in trafo_types:
    t = trafo_types["S11-315/10"]
    print("  S11-315/10: sn_mva=%.3f vk=%.1f vkr=%.2f pfe=%.2f i0=%.2f vg=%s" % (
        t["sn_mva"], t["vk_percent"], t["vkr_percent"], t["pfe_kw"], t["i0_percent"], t.get("vector_group","?")))
else:
    print("  ERROR: S11-315/10 not found!")

sample_cable = cable_names[0] if cable_names else None
if sample_cable:
    t = line_types[sample_cable]
    has_required = all(k in t for k in ("r_ohm_per_km", "x_ohm_per_km", "c_nf_per_km", "max_i_ka"))
    print("  Sample cable '%s' has required keys: %s" % (sample_cable, has_required))

print("=== Verification Complete ===")
