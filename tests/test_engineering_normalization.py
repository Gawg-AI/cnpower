from cnpower.engineering import check_equipment_compliance, normalize_equipment


def test_line_normalization_selects_laying_method_current():
    normalized = normalize_equipment(
        "line_cable",
        {
            "voltage_rating": "6/10kV",
            "max_i_ka_air": 0.21,
            "max_i_ka_ground": 0.185,
            "max_i_ka_duct": 0.165,
            "r_ohm_per_km": 0.268,
            "x_ohm_per_km": 0.11,
            "c_nf_per_km": 200,
        },
        context={"laying_method": "duct"},
    )

    assert normalized["rated_voltage_kv"] == 10
    assert normalized["max_i_ka"] == 0.165
    assert normalized["rated_current_a"] == 165


def test_transformer_normalization_converts_capacity():
    normalized = normalize_equipment(
        "transformer",
        {
            "sn_kva": 630,
            "vn_hv_kv": 10,
            "vn_lv_kv": 0.4,
            "rated_short_circuit_breaking_ka": 25,
        },
    )

    assert normalized["equipment_type"] == "transformer_2w"
    assert normalized["sn_mva"] == 0.63
    assert normalized["rated_voltage_kv"] == 10
    assert normalized["rated_short_circuit_breaking_current_ka"] == 25


def test_ev_charger_normalization_derives_pq():
    normalized = normalize_equipment(
        "ev_charger",
        {
            "rated_power_kw": 14,
            "rated_voltage_v": 380,
            "power_factor": 0.95,
        },
    )

    assert normalized["p_mw"] == 0.014
    assert normalized["rated_voltage_kv"] == 0.38
    assert normalized["q_mvar"] > 0


def test_voltage_fields_are_normalized_when_present():
    normalized = normalize_equipment(
        "transformer",
        {
            "rated_voltage_kv": "6/10kV",
            "rated_voltage_hv_kv": 110,
            "vn_hv_kv": 110,
            "vn_lv_kv": "400V",
        },
    )

    assert normalized["rated_voltage_kv"] == 10
    assert normalized["rated_voltage_hv_kv"] == 110
    assert normalized["vn_hv_kv"] == 110
    assert normalized["vn_lv_kv"] == 0.4


def test_compliance_executor_detects_violation_and_maps_type_alias():
    result = check_equipment_compliance(
        "transformer",
        {
            "sn_kva": 630,
            "vn_hv_kv": 10,
            "vn_lv_kv": 0.4,
            "vk_percent": 4.5,
            "vkr_percent": 0.98,
            "vk0_percent": 4.5,
            "vkr0_percent": 0.98,
            "rated_current_a": 36.4,
            "normal_loading_limit_percent": 80,
        },
        {
            "operating_voltage_kv": 12,
            "max_current_a": 40,
            "loading_percent": 85,
        },
    )

    assert result["equipment_type"] == "transformer_2w"
    assert result["rule_count"] > 0
    assert any(item["rule_id"] == "GEN_VOLTAGE" and item["passed"] is False for item in result["findings"])
    assert any(item["rule_id"] == "GEN_CURRENT" and item["passed"] is False for item in result["findings"])
    assert result["summary"]["failed"] >= 2
