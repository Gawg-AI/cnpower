import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from cn_dist_grid_lib.equipment.transformers import get_all_transformers
from cn_dist_grid_lib.equipment.cables import get_all_cables
from cn_dist_grid_lib.equipment.overhead_lines import get_all_overhead_lines
from cn_dist_grid_lib.equipment.switchgear import get_all_switchgear
from cn_dist_grid_lib.equipment.reactive_compensation import get_all_reactive_compensation
from cn_dist_grid_lib.equipment.protection import get_all_protection
from cn_dist_grid_lib.equipment.instrument_transformers import get_all_instrument_transformers
from cn_dist_grid_lib.equipment.surge_arresters import get_all_surge_arresters
from cn_dist_grid_lib.equipment.new_energy.photovoltaic import get_all_photovoltaic
from cn_dist_grid_lib.equipment.new_energy.wind_turbine import get_all_wind_turbines
from cn_dist_grid_lib.equipment.new_energy.energy_storage import get_all_energy_storage
from cn_dist_grid_lib.equipment.new_energy.ev_charger import get_all_ev_chargers
from cn_dist_grid_lib.topology.connection_modes import get_all_connection_modes
from cn_dist_grid_lib.validation.rules import get_all_validation_rules
from cn_dist_grid_lib.standards.references import get_all_standards
from cn_dist_grid_lib.engineering import get_all_engineering_parameters

t = get_all_transformers()
c = get_all_cables()
o = get_all_overhead_lines()
s = get_all_switchgear()
rc = get_all_reactive_compensation()
p = get_all_protection()
it = get_all_instrument_transformers()
sa = get_all_surge_arresters()
pv = get_all_photovoltaic()
wt = get_all_wind_turbines()
es = get_all_energy_storage()
ev = get_all_ev_chargers()
cm = get_all_connection_modes()
vr = get_all_validation_rules()
st = get_all_standards()
ep = get_all_engineering_parameters()

print("=== cn_dist_grid_lib Verification ===")
print("Transformers: oil=%d dry=%d box=%d main35=%d main110=%d trafo3w=%d" % (
    len(t["oil_immersed"]), len(t["dry_type"]), len(t["box_substation"]),
    len(t["main_transformer_35kv"]), len(t["main_transformer_110kv"]), len(t["trafo3w_110kv"])))
print("Cables: 10kV=%d 35kV=%d 0.4kV=%d 110kV=%d" % (
    len(c["mv_10kv"]), len(c["mv_35kv"]), len(c["lv_04kv"]), len(c["hv_110kv"])))
print("Overhead: 10kV=%d 0.4kV=%d bare=%d" % (
    len(o["mv_10kv_insulated"]), len(o["lv_04kv_insulated"]), len(o["bare_conductor"])))
print("Switchgear categories: %d" % len(s))
print("Reactive comp categories: %d" % len(rc))
print("Protection categories: %d" % len(p))
print("Instrument transformers categories: %d" % len(it))
print("Surge arresters categories: %d" % len(sa))
print("PV: modules=%d string_inv=%d central_inv=%d" % (
    len(pv["pv_module"]), len(pv["string_inverter"]), len(pv["central_inverter"])))
print("Wind: small=%d medium=%d" % (len(wt["small_wind"]), len(wt["medium_wind"])))
print("Storage: lfp=%d lead_carbon=%d pcs=%d" % (
    len(es["lfp_battery"]), len(es["lead_carbon_battery"]), len(es["pcs"])))
print("EV charger: ac=%d dc=%d super=%d" % (
    len(ev["ac_slow"]), len(ev["dc_fast"]), len(ev["dc_superfast"])))
print("Connection modes: 10kV_oh=%d 10kV_cable=%d 0.4kV=%d" % (
    len(cm["mv_10kv_overhead"]), len(cm["mv_10kv_cable"]), len(cm["lv_04kv"])))
print("Validation rule categories: %d" % len(vr))
print("Standards: %d" % len(st))
print("Engineering asset classes: %d" % len(ep["asset_schema"]["classes"]))
print("Planning scenarios: %d" % len(ep["planning_assumptions"]["planning_scenarios"]))

total_models = (
    len(t["oil_immersed"]) + len(t["dry_type"]) + len(t["box_substation"]) +
    len(t["main_transformer_35kv"]) + len(t["main_transformer_110kv"]) + len(t["trafo3w_110kv"]) +
    len(c["mv_10kv"]) + len(c["mv_35kv"]) + len(c["lv_04kv"]) + len(c["hv_110kv"]) +
    len(o["mv_10kv_insulated"]) + len(o["lv_04kv_insulated"]) + len(o["bare_conductor"]) +
    len(pv["pv_module"]) + len(pv["string_inverter"]) + len(pv["central_inverter"]) +
    len(wt["small_wind"]) + len(wt["medium_wind"]) +
    len(es["lfp_battery"]) + len(es["lead_carbon_battery"]) + len(es["pcs"]) +
    len(ev["ac_slow"]) + len(ev["dc_fast"]) + len(ev["dc_superfast"])
)
print("Total equipment models: %d" % total_models)
print("=== ALL MODULES VERIFIED OK ===")
