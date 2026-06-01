from .compliance_constraints import get_compliance_constraint_library


def _first_number(value):
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, list) and value:
        nums = [v for v in value if isinstance(v, (int, float))]
        return float(max(nums)) if nums else None
    return None


def _get(data, *names):
    for name in names:
        if name in data and data[name] is not None:
            return data[name]
    return None


def _pass_le(left, right):
    if left is None or right is None:
        return None
    return float(left) <= float(right)


def check_basic_equipment_compliance(equipment_type, equipment, results=None):
    results = results or {}
    constraints = get_compliance_constraint_library()["constraints_by_equipment_type"].get(equipment_type, [])
    findings = []

    def add(rule_id, passed, message, severity="error"):
        findings.append({
            "rule_id": rule_id,
            "passed": passed,
            "severity": severity,
            "message": message,
        })

    rated_voltage = _get(equipment, "rated_voltage_kv", "vn_hv_kv", "vn_kv", "voltage_rating")
    operating_voltage = _get(results, "operating_voltage_kv", "vn_kv")
    if rated_voltage is not None and operating_voltage is not None:
        add("GEN_VOLTAGE", _pass_le(operating_voltage, rated_voltage), "运行电压不得超过设备额定电压。")

    rated_current = _get(equipment, "rated_current_a", "frame_current_a", "max_i_ka")
    rated_current = _first_number(rated_current)
    if rated_current is not None and isinstance(rated_current, (int, float)) and rated_current < 1:
        rated_current = rated_current * 1000
    max_current = _get(results, "max_current_a")
    if max_current is None and _get(results, "i_ka") is not None:
        max_current = float(results["i_ka"]) * 1000
    if rated_current is not None and max_current is not None:
        add("GEN_CURRENT", _pass_le(max_current, rated_current), "最大工作电流不得超过设备额定电流。")

    breaking = _get(equipment, "rated_short_circuit_breaking_ka", "rated_breaking_current_ka", "breaking_capacity_ka")
    ikss = _get(results, "ikss_ka")
    if breaking is not None and ikss is not None:
        add("GEN_BREAKING", _pass_le(ikss, breaking), "最大短路电流不得超过设备额定开断/分断能力。")

    making = _get(equipment, "rated_short_circuit_making_ka", "rated_peak_withstand_ka", "dynamic_current_ka")
    ip = _get(results, "ip_ka")
    if making is not None and ip is not None:
        add("GEN_PEAK", _pass_le(ip, making), "短路峰值电流不得超过设备关合/动稳定能力。")

    withstand = _get(equipment, "rated_short_time_withstand_ka_4s", "thermal_current_ka_1s", "short_circuit_current_1s_ka")
    ith = _get(results, "ith_ka")
    if withstand is not None and ith is not None:
        add("GEN_THERMAL", _pass_le(ith, withstand), "短时热电流不得超过设备短时耐受/热稳定能力。")

    loading = _get(results, "loading_percent")
    limit = _get(equipment, "normal_loading_limit_percent")
    if loading is not None and limit is not None:
        add("GEN_LOADING", _pass_le(loading, limit), "设备负载率不得超过正常运行限值。")

    return {
        "equipment_type": equipment_type,
        "rule_count": len(constraints),
        "basic_findings": findings,
        "constraint_definitions": constraints,
    }

