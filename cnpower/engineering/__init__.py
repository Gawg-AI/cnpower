from .asset_schema import get_engineering_asset_schema
from .compliance_checker import check_basic_equipment_compliance
from .compliance_constraints import get_compliance_constraint_library
from .planning_library import get_planning_assumption_library
from .pandapower_bridge import get_pandapower_bridge_spec


def get_all_engineering_parameters():
    return {
        "asset_schema": get_engineering_asset_schema(),
        "compliance_constraints": get_compliance_constraint_library(),
        "planning_assumptions": get_planning_assumption_library(),
        "pandapower_bridge": get_pandapower_bridge_spec(),
    }
