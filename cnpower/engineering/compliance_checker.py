from .compliance_constraints import get_compliance_constraint_library
from .normalization import (
    canonical_equipment_type,
    first_number,
    normalize_equipment,
    normalize_results,
)


FIELD_ALIASES = {
    "rated_short_circuit_breaking_ka": "rated_short_circuit_breaking_current_ka",
    "rated_breaking_current_ka": "rated_short_circuit_breaking_current_ka",
    "breaking_capacity_ka": "rated_short_circuit_breaking_current_ka",
    "rated_short_time_withstand_ka_4s": "short_time_thermal_current_ka",
    "thermal_current_ka_1s": "short_time_thermal_current_ka",
    "short_circuit_current_1s_ka": "short_time_thermal_current_ka",
    "rated_short_circuit_making_ka": "rated_peak_withstand_ka",
    "dynamic_current_ka": "rated_peak_withstand_ka",
    "max_i_ka": "rated_current_a",
    "frame_current_a": "rated_current_a",
    "vn_kv": "rated_voltage_kv",
    "vn_hv_kv": "rated_voltage_kv",
    "voltage_rating": "rated_voltage_kv",
    "rated_capacity_kvar": "q_mvar",
}


TYPE_ALIASES_FOR_CONSTRAINTS = {
    "transformer": "transformer_2w",
    "trafo": "transformer_2w",
    "line": "line_cable",
    "cable": "line_cable",
    "overhead_line": "line_overhead",
    "switch": "switch_breaker",
    "breaker": "switch_breaker",
    "pv": "pv_inverter",
    "sgen": "pv_inverter",
    "battery": "storage",
}


def _canonical_type(equipment_type):
    canonical = canonical_equipment_type(equipment_type)
    return TYPE_ALIASES_FOR_CONSTRAINTS.get(canonical, canonical)


def _has_field(data, field):
    if field in data and data[field] is not None:
        return True
    alias = FIELD_ALIASES.get(field)
    if alias is None:
        return False
    return alias in data and data[alias] is not None


def _get(data, *names):
    for name in names:
        if name in data and data[name] is not None:
            return data[name]
        alias = FIELD_ALIASES.get(name)
        if alias is not None and alias in data and data[alias] is not None:
            return data[alias]
    return None


def _le(left, right):
    if left is None or right is None:
        return None
    left_num = first_number(left)
    right_num = first_number(right)
    if left_num is None or right_num is None:
        return None
    return left_num <= right_num


def _summary(findings):
    failed = sum(1 for item in findings if item["passed"] is False)
    inconclusive = sum(1 for item in findings if item["passed"] is None)
    passed = sum(1 for item in findings if item["passed"] is True)
    return {
        "passed": passed,
        "failed": failed,
        "inconclusive": inconclusive,
        "total": len(findings),
    }


def _finding(rule_id, passed, message, severity="error", missing_equipment_fields=None, missing_result_fields=None):
    status = "passed" if passed is True else "failed" if passed is False else "inconclusive"
    return {
        "rule_id": rule_id,
        "passed": passed,
        "status": status,
        "severity": severity,
        "message": message,
        "missing_equipment_fields": missing_equipment_fields or [],
        "missing_result_fields": missing_result_fields or [],
    }


def _evaluate_generic(equipment, results):
    findings = []
    rated_voltage = _get(equipment, "rated_voltage_kv")
    operating_voltage = _get(results, "operating_voltage_kv")
    if rated_voltage is not None and operating_voltage is not None:
        findings.append(_finding("GEN_VOLTAGE", _le(operating_voltage, rated_voltage), "Operating voltage must not exceed equipment rated voltage."))

    rated_current = _get(equipment, "rated_current_a")
    max_current = _get(results, "max_current_a")
    if rated_current is not None and max_current is not None:
        findings.append(_finding("GEN_CURRENT", _le(max_current, rated_current), "Maximum operating current must not exceed equipment rated current."))

    breaking = _get(equipment, "rated_short_circuit_breaking_current_ka")
    ikss = _get(results, "ikss_ka")
    if breaking is not None and ikss is not None:
        findings.append(_finding("GEN_BREAKING", _le(ikss, breaking), "Maximum short-circuit current must not exceed breaking capacity."))

    peak = _get(equipment, "rated_peak_withstand_ka")
    ip = _get(results, "ip_ka")
    if peak is not None and ip is not None:
        findings.append(_finding("GEN_PEAK", _le(ip, peak), "Short-circuit peak current must not exceed making or dynamic withstand capacity."))

    thermal = _get(equipment, "short_time_thermal_current_ka")
    ith = _get(results, "ith_ka")
    if thermal is not None and ith is not None:
        findings.append(_finding("GEN_THERMAL", _le(ith, thermal), "Thermal short-circuit current must not exceed short-time withstand capacity."))

    loading = _get(results, "loading_percent")
    limit = _get(equipment, "normal_loading_limit_percent")
    if loading is not None and limit is not None:
        findings.append(_finding("GEN_LOADING", _le(loading, limit), "Loading must not exceed the normal loading limit."))

    return findings


def _evaluate_rule(rule, equipment, results):
    rule_id = rule.get("rule_id", "UNKNOWN")
    severity = rule.get("severity", "error")
    missing_equipment = [field for field in rule.get("required_equipment_fields", []) if not _has_field(equipment, field)]
    missing_results = [field for field in rule.get("required_result_fields", []) if not _has_field(results, field)]
    if missing_equipment or missing_results:
        return _finding(
            rule_id,
            None,
            "Required data is missing; rule could not be evaluated.",
            severity=severity,
            missing_equipment_fields=missing_equipment,
            missing_result_fields=missing_results,
        )

    checks = []
    if rule_id.endswith("_V_001") or "VOLTAGE" in rule_id or rule_id.startswith("RC_V") or rule_id.startswith("SWG_V"):
        checks.append(("operating voltage", _get(results, "operating_voltage_kv"), _get(equipment, "rated_voltage_kv")))
    if "_I_" in rule_id or rule_id.endswith("LOAD_001") or rule_id.endswith("CAB_LOAD_001") or rule_id.endswith("OHL_LOAD_001"):
        current_val = _get(results, "max_current_a", "i_ka")
        if "max_current_a" not in results and "i_ka" in results:
            cv = first_number(current_val)
            if cv is not None:
                current_val = cv * 1000.0
        checks.append(("operating current", current_val, _get(equipment, "rated_current_a")))
    if "BREAK" in rule_id:
        checks.append(("short-circuit breaking", _get(results, "ikss_ka"), _get(equipment, "rated_short_circuit_breaking_current_ka")))
    if "MAKE" in rule_id or "PEAK" in rule_id or "DYNAMIC" in rule_id:
        checks.append(("peak withstand", _get(results, "ip_ka"), _get(equipment, "rated_peak_withstand_ka")))
    if "THERMAL" in rule_id or "SC_001" in rule_id:
        checks.append(("thermal withstand", _get(results, "ith_ka"), _get(equipment, "short_time_thermal_current_ka")))
    if "SOC" in rule_id:
        soc = first_number(_get(results, "soc_percent"))
        soc_range = _get(equipment, "soc_range_percent")
        if soc is not None and soc_range is not None:
            nums = [float(x) for x in str(soc_range).replace("~", " ").split() if x.replace(".", "", 1).isdigit()]
            if len(nums) >= 2:
                passed = min(nums) <= soc <= max(nums)
                return _finding(rule_id, passed, "SOC must remain inside equipment operating range.", severity=severity)
    if "_P_" in rule_id:
        checks.append(("active power", abs(first_number(_get(results, "p_mw"), 0.0) * 1000.0), _get(equipment, "rated_charge_discharge_power_kw", "rated_power_kw")))
    if "_Q_" in rule_id or rule_id.startswith("RC_Q"):
        checks.append(("reactive power", abs(first_number(_get(results, "q_mvar"), 0.0)), abs(first_number(_get(equipment, "q_mvar"), 0.0))))

    evaluated = []
    for label, left, right in checks:
        passed = _le(left, right)
        if passed is not None:
            evaluated.append((label, passed))
    if evaluated:
        passed = all(item[1] for item in evaluated)
        failed_labels = [label for label, ok in evaluated if not ok]
        message = "Rule evaluated successfully." if passed else "Limit exceeded: " + ", ".join(failed_labels)
        return _finding(rule_id, passed, message, severity=severity)

    return _finding(
        rule_id,
        None,
        "Required data is present, but this rule needs domain-specific evaluation logic.",
        severity=severity,
    )


def check_equipment_compliance(equipment_type, equipment, results=None, *, context=None):
    canonical_type = _canonical_type(equipment_type)
    normalized_equipment = normalize_equipment(canonical_type, equipment, context=context)
    normalized_results = normalize_results(results or {})
    library = get_compliance_constraint_library()
    constraints = library["constraints_by_equipment_type"].get(canonical_type, [])

    basic_findings = _evaluate_generic(normalized_equipment, normalized_results)
    rule_findings = [_evaluate_rule(rule, normalized_equipment, normalized_results) for rule in constraints]
    findings = basic_findings + rule_findings

    return {
        "equipment_type": canonical_type,
        "rule_count": len(constraints),
        "basic_findings": basic_findings,
        "rule_findings": rule_findings,
        "findings": findings,
        "summary": _summary(findings),
        "normalized_equipment": normalized_equipment,
        "normalized_results": normalized_results,
        "constraint_definitions": constraints,
    }


def check_basic_equipment_compliance(equipment_type, equipment, results=None):
    return check_equipment_compliance(equipment_type, equipment, results)
