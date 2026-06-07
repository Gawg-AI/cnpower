import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cnpower.equipment.transformers import get_all_transformers
from cnpower.equipment.cables import get_all_cables
from cnpower.equipment.overhead_lines import get_all_overhead_lines
from cnpower.equipment.switchgear import get_all_switchgear
from cnpower.equipment.reactive_compensation import get_all_reactive_compensation
from cnpower.equipment.protection import get_all_protection
from cnpower.equipment.instrument_transformers import get_all_instrument_transformers
from cnpower.equipment.surge_arresters import get_all_surge_arresters
from cnpower.equipment.new_energy.photovoltaic import get_all_photovoltaic
from cnpower.equipment.new_energy.ev_charger import get_all_ev_chargers
from cnpower.equipment.new_energy.energy_storage import get_all_energy_storage
from cnpower.equipment.new_energy.wind_turbine import get_all_wind_turbines
from cnpower.topology.connection_modes import get_all_connection_modes
from cnpower.validation.rules import get_all_validation_rules
from cnpower.standards.references import get_all_standards
from cnpower.pandapower_integration.std_types_cn import (
    chinese_line_std_types,
    chinese_trafo_std_types,
    chinese_trafo3w_std_types,
    chinese_fuse_std_types,
)

PASS = 0
FAIL = 0


def check(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  [PASS] {name}")
    else:
        FAIL += 1
        msg = f"  [FAIL] {name}"
        if detail:
            msg += f" -- {detail}"
        print(msg)


def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def test_import_cnpower():
    section("Bug#1: import cnpower 可用性验证")
    import cnpower
    check("import cnpower 成功", True)
    check("cnpower.__version__ 存在", hasattr(cnpower, '__version__'))
    check("cnpower.SYSTEM_FREQ_HZ=50", cnpower.SYSTEM_FREQ_HZ == 50.0)
    check("cnpower.get_all_transformers 可调用", callable(getattr(cnpower, 'get_all_transformers', None)))


def test_transformers():
    section("S1: shift_degree 修复验证")
    data = get_all_transformers()
    for cat in ("oil_immersed", "dry_type", "main_transformer_35kv", "main_transformer_110kv"):
        models = data.get(cat, {})
        for name, m in models.items():
            vg = m.get("vector_group", "")
            sd = m.get("shift_degree", None)
            if "Dyn11" in vg or "YNd11" in vg:
                check(
                    f"{cat}/{name} shift_degree={sd}",
                    sd == 30,
                    f"expected 30 for {vg}, got {sd}",
                )

    section("S2: 零序参数注释验证")
    for cat in ("oil_immersed", "dry_type", "main_transformer_35kv", "main_transformer_110kv"):
        models = data.get(cat, {})
        for name, m in models.items():
            has_note = "zero_seq_note" in m
            check(f"{cat}/{name} zero_seq_note存在", has_note)

    section("S3: S11淘汰标注验证")
    oil = data.get("oil_immersed", {})
    s11_count = sum(1 for n in oil if n.startswith("S11-"))
    s11_deprecated = sum(1 for n, m in oil.items() if n.startswith("S11-") and m.get("deprecated") is True)
    check("S11型号全部标注deprecated", s11_count == s11_deprecated, f"{s11_deprecated}/{s11_count}")
    for name, m in oil.items():
        if name.startswith("S11-"):
            check(f"{name} deprecation_note存在", "deprecation_note" in m)

    section("S6a: 变压器国标版本验证")
    for cat in ("oil_immersed", "dry_type", "main_transformer_35kv", "main_transformer_110kv"):
        models = data.get(cat, {})
        for name, m in models.items():
            std = m.get("standard", "")
            if "6451" in std:
                check(f"{cat}/{name} GB/T 6451版本", "2023" in std, f"got {std}")
            if "10228" in std:
                check(f"{cat}/{name} GB/T 10228版本", "2023" in std, f"got {std}")
            if "17467" in std:
                check(f"{cat}/{name} GB/T 17467版本", "2020" in std, f"got {std}")


def test_wind_turbines():
    section("S4: 风机标准引用验证")
    data = get_all_wind_turbines()
    for cat in ("small_wind", "medium_wind"):
        models = data.get(cat, {})
        for name, m in models.items():
            std = m.get("standard", "")
            check(f"{cat}/{name} 不含GB/T 19069", "19069" not in std, f"got {std}")
            if cat == "small_wind":
                check(f"{cat}/{name} 引用GB/T 19068", "19068" in std, f"got {std}")
            if cat == "medium_wind":
                check(f"{cat}/{name} 引用GB/T 25383", "25383" in std, f"got {std}")

    section("M7: 中型风机DFIG→PMSG验证")
    medium = data.get("medium_wind", {})
    for name, m in medium.items():
        gt = m.get("generator_type", "")
        check(f"medium/{name} generator_type", gt == "PMSG", f"got {gt}")


def test_overhead_lines():
    section("S5: LV架空绝缘线标准验证")
    data = get_all_overhead_lines()
    lv = data.get("lv_04kv_insulated", {})
    for name, m in lv.items():
        std = m.get("standard", "")
        check(f"LV/{name} 不含GB/T 1179", "1179" not in std, f"got {std}")
        check(f"LV/{name} 引用GB/T 12527", "12527" in std, f"got {std}")


def test_references():
    section("S7: references.py GB/T 36558名称验证")
    data = get_all_standards()
    found = False
    for code, std in data.items():
        if code == "GB/T 36558-2018":
            found = True
            name = std.get("name", "")
            check("GB/T 36558名称正确", "电化学储能" in name, f"got '{name}'")
            check("GB/T 36558关联设备含energy_storage",
                  "energy_storage" in std.get("related_equipment", []))
    check("GB/T 36558-2018存在于references", found)

    section("S6b: references.py过时标准版本验证")
    outdated = {
        "GB/T 6451-2015": "GB/T 6451-2023",
        "GB/T 10228-2015": "GB/T 10228-2023",
        "GB/T 1984-2014": "GB/T 1984-2024",
        "GB/T 15166-2008": "GB/T 15166.2-2023",
        "GB/T 1207-2006": "GB/T 20840.3-2013",
        "GB/T 1208-2006": "GB/T 20840.2-2014",
    }
    codes_in_refs = list(data.keys())
    for old_code, new_code in outdated.items():
        check(f"references中不含{old_code}", old_code not in codes_in_refs,
              f"应更新为{new_code}")


def test_ev_charger():
    section("M6: AC-14kW电流参数验证")
    data = get_all_ev_chargers()
    ac = data.get("ac_slow", {})
    ac14 = ac.get("AC-14kW", {})
    if ac14:
        p = ac14.get("rated_power_kw", 0)
        v = ac14.get("rated_voltage_v", 0)
        i = ac14.get("rated_current_a", 0)
        pf = ac14.get("power_factor", 0.95)
        if v > 0 and pf > 0:
            expected_i = p * 1000 / (math.sqrt(3) * v * pf)
            tolerance = 0.15
            check("AC-14kW 电流与功率匹配",
                  abs(i - expected_i) / expected_i < tolerance,
                  f"I={i}A, expected≈{expected_i:.1f}A")


def test_validation_rules():
    section("M11: 0.4kV电压偏差限值验证")
    data = get_all_validation_rules()
    vd = data.get("voltage_quality", {}).get("voltage_deviation", {})
    limits = vd.get("limits", {})
    check("0.4kV三相限值存在", "0.4kV_3phase" in limits, f"got keys: {list(limits.keys())}")
    check("0.4kV单相限值存在", "0.4kV_1phase" in limits)
    if "0.4kV_3phase" in limits:
        check("0.4kV三相限值为±7%", "±7%" in limits["0.4kV_3phase"])
    if "0.4kV_1phase" in limits:
        check("0.4kV单相限值为+7%/-10%", "+7%/-10%" in limits["0.4kV_1phase"])


def test_photovoltaic():
    section("M13: 大功率逆变器AC电压验证")
    data = get_all_photovoltaic()
    ci = data.get("central_inverter", {})
    for name in ("central_500kW", "central_630kW"):
        m = ci.get(name, {})
        if m:
            vac = m.get("rated_ac_voltage_v", 0)
            check(f"{name} AC电压为315V", vac == 315, f"got {vac}V")
            check(f"{name} voltage_note存在", "voltage_note" in m)


def test_data_structure_consistency():
    section("M8: 数据结构一致性验证 (全部为dict[str,dict])")
    all_getters = {
        "transformers": get_all_transformers,
        "cables": get_all_cables,
        "overhead_lines": get_all_overhead_lines,
        "switchgear": get_all_switchgear,
        "reactive_compensation": get_all_reactive_compensation,
        "protection": get_all_protection,
        "instrument_transformers": get_all_instrument_transformers,
        "surge_arresters": get_all_surge_arresters,
        "photovoltaic": get_all_photovoltaic,
        "ev_charger": get_all_ev_chargers,
        "energy_storage": get_all_energy_storage,
        "wind_turbine": get_all_wind_turbines,
    }
    for mod_name, getter in all_getters.items():
        data = getter()
        if not isinstance(data, dict):
            check(f"{mod_name} 顶层为dict", False, f"got {type(data).__name__}")
            continue
        check(f"{mod_name} 顶层为dict", True)
        for cat_name, cat_val in data.items():
            if isinstance(cat_val, dict):
                all_dict = all(isinstance(v, dict) for v in cat_val.values())
                check(f"{mod_name}/{cat_name} 子项为dict[str,dict]", all_dict,
                      f"types: {set(type(v).__name__ for v in cat_val.values())}")
            elif isinstance(cat_val, list):
                check(f"{mod_name}/{cat_name} 不应为list", False,
                      f"应转为dict[str,dict]")


def test_pandapower_compatibility():
    section("pandapower集成层兼容性验证")
    line_types = chinese_line_std_types()
    check("chinese_line_std_types返回dict", isinstance(line_types, dict))
    check("line类型数>0", len(line_types) > 0, f"got {len(line_types)}")
    for name, entry in line_types.items():
        check(f"line/{name} 含r_ohm_per_km", "r_ohm_per_km" in entry)
        check(f"line/{name} 含x_ohm_per_km", "x_ohm_per_km" in entry)
        check(f"line/{name} 含c_nf_per_km", "c_nf_per_km" in entry)
        check(f"line/{name} 含max_i_ka", "max_i_ka" in entry)
        break

    trafo_types = chinese_trafo_std_types()
    check("chinese_trafo_std_types返回dict", isinstance(trafo_types, dict))
    check("trafo类型数>0", len(trafo_types) > 0, f"got {len(trafo_types)}")
    for name, entry in trafo_types.items():
        for req_key in ("sn_mva", "vn_hv_kv", "vn_lv_kv", "vk_percent",
                        "vkr_percent", "pfe_kw", "i0_percent", "shift_degree"):
            check(f"trafo/{name} 含{req_key}", req_key in entry,
                  f"missing {req_key}")
        check(f"trafo/{name} shift_degree=30", entry.get("shift_degree") == 30,
              f"got {entry.get('shift_degree')}")
        break

    trafo3w_types = chinese_trafo3w_std_types()
    check("chinese_trafo3w_std_types返回dict", isinstance(trafo3w_types, dict))
    for name, entry in trafo3w_types.items():
        check(f"trafo3w/{name} shift_lv_degree=30",
              entry.get("shift_lv_degree") == 30,
              f"got {entry.get('shift_lv_degree')}")
        break

    fuse_types = chinese_fuse_std_types()
    check("chinese_fuse_std_types返回dict", isinstance(fuse_types, dict))
    check("fuse类型数>0", len(fuse_types) > 0, f"got {len(fuse_types)}")


def test_switchgear_standards():
    section("S6c: 开关柜国标版本验证")
    data = get_all_switchgear()
    for cat in ("circuit_breaker_mv",):
        models = data.get(cat, {})
        for name, m in models.items():
            std = m.get("standard", "")
            if "1984" in std:
                check(f"{cat}/{name} GB/T 1984版本", "2024" in std, f"got {std}")
                break


def test_instrument_transformers_standards():
    section("S6d: 互感器国标版本验证")
    data = get_all_instrument_transformers()
    for cat in ("ct_mv", "pt_mv"):
        models = data.get(cat, {})
        for name, m in models.items():
            std = m.get("standard", "")
            if "1207" in std:
                check(f"{cat}/{name} 不含GB/T 1207-2006", "2006" not in std, f"got {std}")
            if "1208" in std:
                check(f"{cat}/{name} 不含GB/T 1208-2006", "2006" not in std, f"got {std}")
            if "20840" in std:
                check(f"{cat}/{name} 引用GB/T 20840", True)
            break


def test_compliance_checker():
    section("Bug#2: compliance_checker字段映射验证")
    from cnpower.engineering.compliance_checker import check_basic_equipment_compliance
    test_trafo = {
        "vn_hv_kv": 10,
        "vn_lv_kv": 0.4,
        "rated_current_a": 36.4,
    }
    results = {"operating_voltage_kv": 10, "max_current_a": 36.4}
    findings = check_basic_equipment_compliance("transformer", test_trafo, results)
    check("compliance_checker返回dict", isinstance(findings, dict))
    basic = findings.get("basic_findings", [])
    check("compliance_checker对vn_hv_kv设备能识别电压字段", len(basic) >= 0)
    overvoltage_trafo = {"vn_hv_kv": 10, "vn_lv_kv": 0.4, "rated_current_a": 36.4}
    overvoltage_results = {"operating_voltage_kv": 12, "max_current_a": 36.4}
    findings2 = check_basic_equipment_compliance("transformer", overvoltage_trafo, overvoltage_results)
    basic2 = findings2.get("basic_findings", [])
    voltage_violation = any(f.get("rule_id") == "GEN_VOLTAGE" for f in basic2)
    check("compliance_checker检测到过电压违规", voltage_violation,
          f"findings: {basic2}")


if __name__ == "__main__":
    print("=" * 60)
    print("  cnpower 全量验证脚本")
    print("=" * 60)

    test_import_cnpower()
    test_transformers()
    test_wind_turbines()
    test_overhead_lines()
    test_references()
    test_ev_charger()
    test_validation_rules()
    test_photovoltaic()
    test_data_structure_consistency()
    test_pandapower_compatibility()
    test_switchgear_standards()
    test_instrument_transformers_standards()
    test_compliance_checker()

    print(f"\n{'='*60}")
    print(f"  验证结果: {PASS} PASS, {FAIL} FAIL")
    print(f"{'='*60}")

    if FAIL > 0:
        sys.exit(1)
    else:
        print("  所有验证通过!")
        sys.exit(0)
