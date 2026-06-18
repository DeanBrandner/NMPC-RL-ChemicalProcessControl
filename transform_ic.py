"""Transform raw initial-condition samples into environment-ready arrays.

This script converts a raw pickle file of labeled initial-condition samples
into the compact format expected by :class:`environment.BatchDistillationEnv`
when ``diverse_initial_conditions`` is enabled. The raw data is cleaned,
filtered for sufficiently large bottom-product mass, reordered according to the
do-mpc simulator variable ordering, and written next to the input file with the
suffix ``"_cleaned.pkl"``.
"""

import os, pickle
import numpy as np
from casadi import DM
from models.batchcol_model_dompc import template_model as batchcol_model_dompc
from models.batchcol_model_dompc import template_simulator as batchcol_simulator

def transform_initial_conditions(initial_condition_path: str) -> None:
    """Clean and convert raw initial-condition samples.

    Parameters
    ----------
    initial_condition_path : str
        Path to a pickle file containing a dictionary of raw initial-condition
        arrays. Keys must correspond to model state, algebraic, and input
        variable names, except for the legacy naming conventions corrected by
        this function.

    Output
    ------
    Creates a pickle file next to ``initial_condition_path`` with
    ``"_cleaned.pkl"`` appended before the extension. The output dictionary has
    the keys ``"x_init"``, ``"z_init"``, and ``"u_init"``. Values are CasADi
    ``DM`` matrices ordered according to the simulator's ``x0``, ``z0``, and
    ``u0`` structures.

    Notes
    -----
    The transformation performs three preprocessing steps:

    - Removes the component suffix from tray liquid-volume keys starting with
      ``"e0_v_L_tr"``.
    - Replaces distillate holdup composition values with fixed nominal
      component holdups for ``e0_HU_D_c1`` and ``e0_HU_D_c2``.
    - Keeps only samples where the mass derived from ``e0_HU_tr9_c1`` exceeds
      ``6.0``.
    """

    with open(initial_condition_path, "rb") as f:
        initial_conditions = pickle.load(f)
    
    cleaned_initial_conditions = {}
    for key, value in initial_conditions.items():
        cleaned_key = key
        if key.startswith("e0_v_L_tr"):
            cleaned_key = key[:-2]
        if key == "e0_HU_D_c1":
            value = np.array([0.95 * 1e-3 / 0.046] * value.shape[0])
        if key == "e0_HU_D_c2":
            value = np.array([0.05 * 1e-3 / 0.018] * value.shape[0])

        cleaned_initial_conditions[cleaned_key] = value

    initial_conditions = cleaned_initial_conditions
    del cleaned_initial_conditions

    # Filter out samples that do not contain enough bottom-product component.
    e0_M_tr9_c1 = initial_conditions["e0_HU_tr9_c1"] * 0.046

    geq_6 = np.where(e0_M_tr9_c1 > 6.0)

    cleaned_initial_conditions = {}
    for key, value in initial_conditions.items():
        value = value[geq_6]
        cleaned_initial_conditions[key] = value
    
    initial_conditions = cleaned_initial_conditions
    del cleaned_initial_conditions

    # Use simulator templates to preserve the exact variable ordering expected
    # by the environment when loading diverse initial conditions.
    model =  batchcol_model_dompc()
    simulator = batchcol_simulator(model)

    x_init = DM([initial_conditions[key] for key in simulator.x0.keys()])
    z_init = DM([initial_conditions[key] for key in simulator.z0.keys() if key not in ["default"]])
    u_init = DM([initial_conditions[key] for key in simulator.u0.keys() if key not in ["default"]])

    initial_conditions = {
        "x_init": x_init,
        "z_init": z_init,
        "u_init": u_init,
    }
    with open(initial_condition_path.replace(".pkl", "_cleaned.pkl"), "wb") as f:
        pickle.dump(initial_conditions, f)

if __name__ == "__main__":
    initial_condition_path = os.path.join("data", "LVcolumn_DAE_init", "IC_sample_1000.pkl")
    transform_initial_conditions(initial_condition_path)
