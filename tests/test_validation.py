from cnpower.validation.rules import get_all_validation_rules


def test_validation_rules_cover_core_domains_and_voltage_limits():
    rules = get_all_validation_rules()

    for key in ("voltage_quality", "n1_safety", "connection_modes", "short_circuit", "equipment_selection", "reliability", "renewable_connection"):
        assert key in rules

    voltage_limits = rules["voltage_quality"]["voltage_deviation"]["limits"]
    assert voltage_limits["110kV"] == "±5%"
    assert voltage_limits["35kV"] == "±5%"
    assert voltage_limits["10kV"] == "±7%"
    assert voltage_limits["0.4kV_3phase"] == "±7%"
    assert voltage_limits["0.4kV_1phase"] == "+7%/-10%"


def test_validation_rule_entries_have_traceable_criteria():
    rules = get_all_validation_rules()

    assert rules["short_circuit"]["three_phase_max"]["check_formula"]
    assert rules["connection_modes"]["pass_criteria"]
    assert rules["equipment_selection"]["breaker_rating"]["pass_criteria"]
    assert rules["renewable_connection"]["energy_storage_safety"]["pass_criteria"]
    assert rules["renewable_connection"]["storage_grid_connection"]["pass_criteria"]
    assert rules["renewable_connection"]["ev_charger_power_quality"]["pass_criteria"]
    assert rules["renewable_connection"]["voltage_rise_check"]["pass_criteria"]
