from cnpower.equipment.cables import get_all_cables
from cnpower.equipment.overhead_lines import get_all_overhead_lines
from cnpower.equipment.protection import get_all_protection
from cnpower.equipment.switchgear import get_all_switchgear
from cnpower.equipment.transformers import get_all_transformers
from cnpower.standards.references import get_all_standards


def test_transformers_include_operating_current_and_thermal_metadata():
    s13 = get_all_transformers()["oil_immersed"]["S13-630/10"]

    assert s13["rated_current_hv_a"] == 36.4
    assert s13["rated_current_lv_a"] == 909.3
    assert s13["normal_loading_limit_percent"] == 80
    assert s13["thermal_model"]["standard"] == "GB/T 1094.7-2024"
    assert s13["energy_efficiency"]["standard"] == "GB 20052-2024"


def test_cables_include_reference_conditions_and_thermal_limits():
    cable = get_all_cables()["mv_10kv"]["YJV22-3x70-10kV"]

    assert cable["ampacity_reference"]["laying_methods"] == ["air", "ground", "duct"]
    assert cable["thermal_limits"]["max_conductor_temp_normal_c"] == 90
    assert cable["short_circuit_i2t_ka2s"] == round(cable["short_circuit_current_1s_ka"] ** 2, 3)
    assert cable["lifecycle"]["design_life_years"] == 30


def test_overhead_lines_include_dynamic_rating_metadata():
    line = get_all_overhead_lines()["bare_conductor"]["LGJ-120"]

    assert line["rated_current_a"] == line["max_i_ka"] * 1000
    assert line["dynamic_line_rating"]["model"] == "heat_balance"
    assert "wind_speed_m_s" in line["ampacity_reference"]


def test_switchgear_and_fuses_include_operating_life_and_curves():
    switchgear = get_all_switchgear()
    breaker = switchgear["circuit_breaker_mv"]["VS1-12/1250"]
    fuse = switchgear["fuse_mv"]["XRNT-12"]

    assert breaker["short_time_withstand"]["duration_s"] == 4
    assert breaker["endurance"]["mechanical_life_cycles"] == 10000
    assert fuse["time_current_curve"]["standard"] == "GB/T 15166.2-2023"
    assert fuse["selection_guide"]["standard"] == "GB/T 15166.6-2023"


def test_protection_and_standard_index_track_latest_operating_references():
    protection = get_all_protection()["transformer_protection"]["fuse_protection_small"]
    standards = get_all_standards()

    assert protection["fuse_coordination"]["standard"] == "GB/T 15166.6-2023"
    assert "GB/T 1094.7-2024" in standards
    assert standards["GB 20052-2024"]["year"] == 2024
