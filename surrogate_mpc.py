"""Default RL-MPC setup for the learned NARX surrogate model.

This module configures an ``RL_MPC`` controller around a do-mpc-compatible
surrogate model. It sets the prediction horizon, input bounds, soft state
constraints with RL backoff parameters, model scaling, objective terms, parameter
callbacks, and solver options used by the training workflow.
"""

import casadi as cd
from RL_MPC import RL_MPC
from _model_for_rl import RL_Model as do_mpc_Model
from narx_functions import Hyperparameters

def get_default_rlmpc(model: do_mpc_Model, hyperparameters: Hyperparameters) -> RL_MPC:
    """Create the default RL-MPC controller for a surrogate model.

    Parameters
    ----------
    model : RL_Model
        Discrete surrogate model produced by ``transform_to_do_mpc``. The
        model is expected to expose the NARX state ``x_t-1``, input
        ``u_t-1``, and RL parameters for constraint backoffs.
    hyperparameters : Hyperparameters
        Surrogate-model metadata. ``t_step_for_model`` defines the controller
        sampling time and the fixed ``delta_t`` parameter.
    Returns
    -------
    RL_MPC
        Configured and set-up MPC controller.
    """
    mpc = RL_MPC(model)

    dt = hyperparameters.t_step_for_model # seconds
    mpc.settings.t_step = dt

    time_horizon = 15.0 * 60.0 # minutes
    n_horizon = int(time_horizon // dt)

    mpc.settings.n_horizon = n_horizon

    lbu = cd.DM([0.7, 3.0])
    ubu = cd.DM([1.0, 5.0])
    mpc.bounds["lower", "_u", "u_t-1"] = lbu
    mpc.bounds["upper", "_u", "u_t-1"] = ubu

    lbx = cd.SX([30.0, 0.0, 0.85, 0.0, 360.0])
    ubx = cd.SX([56.0, 15e3, 0.8955, 0.2286, 375.5])

    # Add the RL backoff to the lower product-purity constraint.
    lbx[2] = lbx[2] + mpc.model._rlp["x_B_backoff"]
    ubx[1] = 6e3 + mpc.model._rlp["distillate_mass_backoff"]

    penalty = 1e4
    mpc.set_nl_cons(expr_name = "lower_state_bounds", expr = lbx - mpc.model._x["x_t-1"], ub = cd.DM.zeros(lbx.shape).full(), soft_constraint=True, penalty_term_cons = penalty)
    mpc.set_nl_cons(expr_name = "upper_state_bounds", expr = mpc.model._x["x_t-1"] - ubx, ub = cd.DM.zeros(ubx.shape).full(), soft_constraint=True, penalty_term_cons = penalty)

    x_scaling = cd.DM([10, 1e3, 0.1, 0.1, 100.0])
    u_scaling = cd.DM([1.0, 1.0])
    t_scaling = cd.DM([hyperparameters.t_step_for_model])
    for key in mpc.model._x.keys():
        if key.startswith("x_t"):
            mpc.scaling["_x", key] = x_scaling
        elif key.startswith("u_t"):
            mpc.scaling["_x", key] = u_scaling
        elif key == "u_prev":
            mpc.scaling["_x", key] = u_scaling
        elif key in ["numerical_time"]:
            mpc.scaling["_x", key] = t_scaling
        else:
            raise ValueError(f"Unknown variable key: {key}")

    lterm = -mpc.model._x["x_t-1"][1] * 1e-3
    mterm = lterm
    mpc.set_objective(mterm = mterm, lterm = lterm)

    rterm_u = {"u_t-1": cd.DM([100.0, 10.0]).full()}
    mpc.set_rterm(**rterm_u)

    p_template = mpc.get_p_template(1)
    p_template["_p", 0, "delta_t"] = hyperparameters.t_step_for_model
    mpc.set_p_fun(lambda t_now: p_template)

    rlp_template = mpc.get_rlp_template()
    mpc.set_rlp_fun(lambda t_now: rlp_template)

    mpc.settings.nlpsol_opts["ipopt.linear_solver"] = "MA27"

    mpc.settings.nlpsol_opts.update({'ipopt.print_level':0, 'ipopt.sb': 'yes', 'print_time':0})

    mpc.setup()
    return mpc
