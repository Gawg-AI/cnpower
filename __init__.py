__version__ = "1.0.0"
__version_date__ = "2026-05-31"
__standard_year__ = "2025"

SYSTEM_FREQ_HZ = 50.0
BASE_SNR_MVA = 100.0
VOLTAGE_LEVELS_KV = [0.4, 10, 35, 110, 220]

from .equipment import (
    get_all_transformers,
    get_all_cables,
    get_all_overhead_lines,
    get_all_switchgear,
    get_all_reactive_compensation,
    get_all_protection,
    get_all_instrument_transformers,
    get_all_surge_arresters,
)
from .equipment.new_energy import (
    get_all_photovoltaic,
    get_all_wind_turbines,
    get_all_energy_storage,
    get_all_ev_chargers,
)
from .topology import get_all_connection_modes
from .validation import get_all_validation_rules
from .standards import get_all_standards
from .engineering import get_all_engineering_parameters
