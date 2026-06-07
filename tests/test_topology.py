from cnpower.topology.connection_modes import get_all_connection_modes


def test_connection_modes_have_required_metadata_and_templates():
    modes = get_all_connection_modes()

    assert modes
    assert "mv_10kv_overhead" in modes
    assert "mv_10kv_cable" in modes
    assert "lv_04kv" in modes

    required = {"name", "description", "standard", "source_note", "topology_template"}
    template_required = {"bus_count", "line_count", "switch_count", "connection_pattern"}
    for group_name, group in modes.items():
        assert isinstance(group, dict), group_name
        for mode_name, mode in group.items():
            assert required.issubset(mode), f"{group_name}/{mode_name}"
            template = mode["topology_template"]
            assert template_required.issubset(template), f"{group_name}/{mode_name}"
            assert template["bus_count"] >= 2
            assert template["line_count"] >= 1
            assert template["switch_count"] >= 0

