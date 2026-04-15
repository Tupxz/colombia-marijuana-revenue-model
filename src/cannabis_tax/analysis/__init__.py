"""Analysis helpers for the simplified project scope."""

from .consumption import build_consumption_scenarios
from .eda import categorical_summary
from .eda import missing_summary
from .eda import numeric_summary
from .eda import plot_histograms
from .eda import plot_target_rate_by_category
from .modeling import build_propensity_dataset
from .modeling import coefficient_table
from .modeling import comparative_results_table
from .modeling import export_propensity_results
from .modeling import fit_lpm
from .modeling import fit_probit
from .modeling import model_fit_summary
from .modeling import prepare_propensity_regression_data
from .modeling import run_propensity_specifications
from .validation import cleanup_artifacts
from .validation import run_target_validation
from .validation import validate_consumption_target
