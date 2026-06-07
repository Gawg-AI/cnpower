import json
import math
from pathlib import Path

import pytest

import cnpower
import cnpower.equipment as equipment
from cnpower.engineering import check_equipment_compliance, normalize_equipment
from cnpower.engineering.normalization import calc_q_mvar_from_power_factor, parse_voltage_kv
from cnpower.equipment.transformers import _calc_three_phase_current_a, get_all_transformers
from cnpower.pandapower_integration.std_types_cn import (
    chinese_line_std_types,
    _get_max_i_ka,
    _get_x_ohm_per_km_default,
    chinese_trafo3w_std_types,
    chinese_trafo_std_types,
)
from cnpower.standards.references import get_all_standards
from cnpower.standards.references import _normalize_standard_references
from cnpower.validation.rules import get_all_validation_rules
from cnpower.equipment.instrument_transformers import get_all_instrument_transformers
from cnpower.equipment.new_energy.ev_charger import get_all_ev_chargers
from cnpower.equipment.new_energy.photovoltaic import get_all_photovoltaic
from cnpower.equipment.overhead_lines import _calc_capacitance_nf, get_all_overhead_lines
from cnpower.equipment.protection import get_all_protection
from cnpower.equipment.reactive_compensation import get_all_reactive_compensation
from cnpower.equipment.surge_arresters import get_all_surge_arresters


def test_transformer_current_rejects_tiny_voltage():
    assert _calc_three_phase_current_a(630, 10) == 36.4
    assert _calc_three_phase_current_a(100, 1e-300) is None
    assert _calc_three_phase_current_a("bad", 10) is None

    normalized = normalize_equipment(
        "transformer",
        {"sn_mva": 1, "vn_hv_kv": 1e-300, "vn_lv_kv": 0.4},
    )
    assert "rated_current_hv_a" not in normalized
    assert normalized["rated_current_lv_a"] == pytest.approx(1443.4)


def test_normalization_parses_power_factor_and_voltage_units_defensively():
    assert calc_q_mvar_from_power_factor(1.0, "cos0.9") > 0
    assert calc_q_mvar_from_power_factor(1.0, float("nan")) == 0.0
    assert parse_voltage_kv(110) == 110
    assert parse_voltage_kv(10000) == 10
    assert parse_voltage_kv(400, source_unit="v") == 0.4
    assert normalize_equipment("pv_inverter", {"rated_power_kw": 100, "power_factor_range": "0.8leading~0.8lagging"})["sn_mva"] == pytest.approx(0.125)


def test_soc_range_with_percent_suffix_is_evaluated():
    result = check_equipment_compliance(
        "storage",
        {"soc_range_percent": "10~90%", "rated_charge_discharge_power_kw": 100},
        {"soc_percent": 50},
    )
    assert any(item["rule_id"] == "ES_SOC_001" and item["passed"] is True for item in result["findings"])


def test_pandapower_std_type_helpers_do_not_emit_zero_ampacity_defaults():
    assert _get_max_i_ka({}) is None
    assert _get_x_ohm_per_km_default({"x_ohm_per_km_table": {"default": 0.35}}) is None

    trafo_types = chinese_trafo_std_types()
    box = trafo_types["ZBW-630/10"]
    for key in ("sn_mva", "vn_hv_kv", "vn_lv_kv", "vk_percent", "vkr_percent", "pfe_kw", "i0_percent", "shift_degree"):
        assert key in box


def test_deprecated_transformers_and_standard_references_are_consistent():
    transformers = get_all_transformers()
    assert all(
        model.get("deprecated") is True
        for name, model in transformers["main_transformer_35kv"].items()
        if name.startswith("SZ11-")
    )
    assert all(
        model.get("deprecated") is True
        for name, model in transformers["main_transformer_110kv"].items()
        if name.startswith("SFZ11-")
    )

    standards = get_all_standards()
    assert "GB/T 19069-2003" not in standards
    assert "GB/T 12747.1-2017" in standards


def test_second_round_report_data_regressions():
    fuse_result = check_equipment_compliance(
        "fuse_mv",
        {"rated_breaking_current_ka": 31.5, "i_rated_a": 63, "protected_equipment_rated_current_a": 40},
        {"ikss_ka": 20, "max_current_a": 35},
    )
    assert fuse_result["equipment_type"] == "fuse"
    assert fuse_result["rule_count"] > 0
    assert any(item["rule_id"] == "FUSE_BREAK_001" and item["passed"] is True for item in fuse_result["findings"])

    protection = get_all_protection()["transformer_protection"]["fuse_protection_small"]
    assert "GB/T 15166.2-2023" in protection["source_note"]

    for group in get_all_ev_chargers().values():
        assert all(item["standard"] == "GB/T 18487.1-2023" for item in group.values())

    pv = get_all_photovoltaic()
    for module_group in pv["pv_module"].values():
        assert all("GB/T 9535.1-2025" in item["standard"] for item in module_group.values())
    assert all("GB/T 19964-2012" in item["standard"] for item in pv["string_inverter"].values())

    svg = get_all_reactive_compensation()["svg"]["SVG-1000kvar-10kV"]
    assert svg["standard"] == "NB/T 10994-2022"

    lv_ct = next(iter(get_all_instrument_transformers()["ct_lv"].values()))
    assert "dynamic_current_ka" in lv_ct
    assert "thermal_current_ka_1s" in lv_ct

    arrester = get_all_surge_arresters()["arrester_mv"]["HY5WZ-17/45"]
    assert arrester["protected_equipment_bil_kv"] > arrester["residual_voltage_kv"]
    arrester_result = check_equipment_compliance("surge_arrester", arrester, {"max_phase_voltage_kv": 12})
    assert any(item["rule_id"] == "SA_RES_001" and item["passed"] is True for item in arrester_result["findings"])


def test_compliance_aliases_evaluate_existing_library_fields():
    ev = get_all_ev_chargers()["ac_slow"]["AC-7kW"]
    ev_result = check_equipment_compliance("ev_charger", ev, {"p_mw": 0.005, "thd_percent": 3})
    assert any(item["rule_id"] == "EV_PQ_001" and item["passed"] is True for item in ev_result["findings"])

    ct = get_all_instrument_transformers()["ct_lv"]["BH-LMZ/100A"]
    ct_result = check_equipment_compliance("metering_ct_pt", ct, {"ith_ka": 1, "ip_ka": 5})
    assert any(item["rule_id"] == "CT_THERMAL_001" and item["passed"] is True for item in ct_result["findings"])
    assert any(item["rule_id"] == "CT_DYNAMIC_001" and item["passed"] is True for item in ct_result["findings"])

    pv = get_all_photovoltaic()["string_inverter"]["string_100kW"]
    pv_result = check_equipment_compliance(
        "pv_inverter",
        pv,
        {"q_mvar": 0.02, "voltage_rise_percent": 2, "thd_percent": 3},
    )
    assert any(item["rule_id"] == "PV_PQ_001" and item["passed"] is True for item in pv_result["findings"])


def _flatten_validation_rule_ids(rules):
    rule_ids = set()
    metadata_containers = {
        "by_area_class",
        "economic_current_density_table",
        "individual_harmonic_limits",
        "limits",
        "limits_by_voltage_level",
        "parameters",
        "rules_by_area_class",
    }

    def walk(value, parent_key=None):
        if isinstance(value, dict):
            for key, child in value.items():
                if parent_key not in metadata_containers and isinstance(child, dict) and any(
                    marker in child
                    for marker in ("name", "limit", "limits", "check_formula", "pass_criteria", "check_method")
                ):
                    rule_ids.add(key)
                walk(child, key)

    walk(rules)
    return rule_ids


def test_20260607_report_system_level_regressions():
    transformers = get_all_transformers()
    for category in ("oil_immersed", "dry_type", "box_substation", "main_transformer_35kv", "main_transformer_110kv"):
        for model in transformers[category].values():
            if model.get("vector_group") in {"Dyn11", "YNd11"}:
                assert model["shift_degree"] == 330
    for category in ("main_transformer_35kv", "main_transformer_110kv"):
        model = next(iter(transformers[category].values()))
        assert model["tap_step_degree"] == 0
        assert model["tap_changer_type"] == "Ratio"

    trafo3w = next(iter(transformers["trafo3w_110kv"].values()))
    assert trafo3w["shift_lv_degree"] == 330
    for key in (
        "vk0_hv_percent",
        "vk0_mv_percent",
        "vk0_lv_percent",
        "vkr0_hv_percent",
        "vkr0_mv_percent",
        "vkr0_lv_percent",
        "vk0_percent",
        "vkr0_percent",
        "mag0_percent",
        "mag0_rx",
        "si0_hv_partial",
    ):
        assert key in trafo3w

    bare = get_all_overhead_lines()["bare_conductor"]["LJ-50"]
    for key in ("x_ohm_per_km", "r0_ohm_per_km", "x0_ohm_per_km", "c0_nf_per_km"):
        assert key in bare
    with pytest.raises(ValueError):
        _calc_capacitance_nf(math.pi * 1000**2, 1.0)

    assert equipment.get_all_photovoltaic is get_all_photovoltaic
    assert cnpower.BASE_MVA == 100.0
    assert cnpower.BASE_SNR_MVA == cnpower.BASE_MVA
    assert cnpower.__version_date__ == "2026-06-07"

    validation = get_all_validation_rules()
    assert "E" in validation["n1_safety"]["rules_by_area_class"]
    assert "HV" in validation["voltage_quality"]["voltage_fluctuation_flicker"]["limits"]["voltage_fluctuation"]

    rule_ids = _flatten_validation_rule_ids(validation)
    for standard in get_all_standards().values():
        assert all(item.isascii() for item in standard.get("related_equipment", []))
        assert set(standard.get("related_rules", [])).issubset(rule_ids)
        assert "canonical_name" not in standard
        assert "canonical_scope" not in standard
    standards = get_all_standards()
    assert "GB/T 1094.1-2013" in standards
    assert "GB/T 1094-2013" not in standards
    assert "GB/T 12706.1~3-2020" in standards
    assert "GB/T 12706-2020" not in standards
    with pytest.raises(ValueError):
        _normalize_standard_references([{"code": "DUP", "related_equipment": []}, {"code": "DUP", "related_equipment": []}])

    chinese_line_std_types.cache_clear()
    assert chinese_line_std_types() is chinese_line_std_types()
    trafo_types = chinese_trafo_std_types()
    assert trafo_types["S13-630/10"]["shift_degree"] == 330
    trafo3w_types = chinese_trafo3w_std_types()
    assert next(iter(trafo3w_types.values()))["shift_lv_degree"] == 330

    manifest_path = Path(__file__).resolve().parents[1] / "cnpower_library_manifest.json"
    with manifest_path.open(encoding="utf-8") as manifest_file:
        manifest = json.load(manifest_file)
    assert manifest["manifest_version"] == "2026.06.07"
    assert "expected_results" not in manifest["validation"]
    assert manifest["validation"]["success_criteria"]["pytest"] == "exit_code == 0"
