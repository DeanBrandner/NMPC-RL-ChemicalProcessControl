"""Initialization recipe using raw CasADi IDAS integrators.

Provides truly continuous ramps and embedded sigmoid level control,
bypassing do_mpc's piecewise-constant ``make_step`` limitation.

The do_mpc model is used only for building the symbolic DAE and for
computing consistent initial conditions.  All integration is performed
with CasADi's IDAS interface directly.
"""

from __future__ import annotations

import sys
import warnings
from typing import Any

import casadi as ca
import numpy as np

# Suppress do-mpc optional-dependency warnings in every process that imports this module.
warnings.filterwarnings("ignore", message=".*ONNX.*")
warnings.filterwarnings("ignore", message=".*opcua.*")
warnings.filterwarnings("ignore", message=".*approximateMPC.*")

# Ensure the project root is importable.
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))

from models.batchcol_model_dompc_pe_init import (  # noqa: E402
    template_model_for_pe_initialization,
    template_simulator,
)

# ---------------------------------------------------------------------------
# Module-level model cache (B) — built once per process, reused across calls.
# Joblib loky workers each build once; subsequent calls are free.
# ---------------------------------------------------------------------------
_MODEL_CACHE: dict[str, Any] | None = None
_INTEG_CACHE: dict[tuple, ca.Function] = {}

_IDAS_OPTS: dict[str, Any] = {
    "abstol": 1e-8,
    "reltol": 1e-8,
    "max_num_steps": 100000,
}
_IDAS_OPTS_RELAXED: dict[str, Any] = {
    "abstol": 1e-6,
    "reltol": 1e-6,
    "max_num_steps": 100000,
}
_COLL_OPTS: dict[str, Any] = {
    "collocation_scheme": "radau",
    "number_of_finite_elements": 4,
    "interpolation_order": 3,
}

# P gains for phase 8 (w_L_B_c1 control via F_feed_tr9).
# Edit here; debug_pi_wB_tuning.py imports these for plot annotations.
PI_WB_KP: float = 50.0
PI_WB_KI: float = 0.0       # unused — kept for debug script import compat
PI_WB_T_RAMP: float = 400.0  # ramp-in duration [s]; alpha = min(1, t/t_ramp)

# P gains for phase 9 (LI control via F_feed_tr9 or F_B).
# Edit here; debug_pi_LI_tuning.py imports these for plot annotations.
PI_LI_KP: float = 0.5
PI_LI_KI: float = 0.0        # unused — kept for debug script import compat
PI_LI_T_RAMP: float = 400.0  # ramp-in duration [s]


def _strip_labels(labels: list[str]) -> list[str]:
    """Strip do_mpc bracket/index notation from symbolic variable labels.

    do_mpc labels have the form ``"['e0_LI', 0]"``; this function returns
    the bare name ``"e0_LI"`` for each entry.

    Parameters
    ----------
    labels : list[str]
        Raw labels from a do_mpc ``struct_symSX.labels()`` call.

    Returns
    -------
    list[str]
        Cleaned variable names, one per entry in ``labels``.
    """
    return [l.strip("[]").split(",")[0] for l in labels]


def _get_model_cache() -> dict[str, Any]:
    """Build and cache model symbolics and default ICs.

    Compiles the do_mpc model and runs ``sim.set_initial_guess()`` /
    ``sim.init_algebraic_variables()`` once per worker process.  Subsequent
    calls return the already-built ``_MODEL_CACHE`` dict immediately.

    Returns
    -------
    dict[str, Any]
        Keys: ``"x_sym"``, ``"z_sym"``, ``"u_sym"``, ``"p_sym"``,
        ``"rhs_sym"``, ``"alg_sym"``, ``"x_labels"``, ``"z_labels"``,
        ``"u_labels"``, ``"u_idx"``, ``"z_idx"``, ``"x0_unscaled"``,
        ``"x0"``, ``"z0_unscaled"``, ``"z0"``, ``"u0"``, ``"p0"``,
        ``"x_scaling"``, ``"z_scaling"``.
    """
    global _MODEL_CACHE
    if _MODEL_CACHE is not None:
        return _MODEL_CACHE

    model = template_model_for_pe_initialization()
    sim = template_simulator(model)
    sim.set_param(integration_tool="idas", abstol=1e-10, reltol=1e-10, t_step=1.0)
    sim.setup()
    sim.set_initial_guess()
    sim.init_algebraic_variables()

    x_labels = _strip_labels(model._x.labels())
    z_labels = _strip_labels(model._z.labels())
    u_labels = _strip_labels(model._u.labels())

    _MODEL_CACHE = {
        "x_sym": sim.sim_x["_x"],
        "z_sym": sim.sim_z["_z"],
        "u_sym": sim.sim_p["_u"],
        "p_sym": sim.sim_p["_p"],
        "rhs_sym": sim.dae["ode"],
        "alg_sym": sim.dae["alg"],
        "x_labels": x_labels,
        "z_labels": z_labels,
        "u_labels": u_labels,
        "u_idx": {name: i for i, name in enumerate(u_labels)},
        "z_idx": {name: i for i, name in enumerate(z_labels)},
        "x0_unscaled": np.array(sim.x0.master).flatten().copy(),
        "x0": np.array(sim.x0.master).flatten().copy()/sim._x_scaling.cat.full().flatten(),
        "z0_unscaled": np.array(sim.z0.master).flatten().copy(),
        "z0": np.array(sim.z0.master).flatten().copy()/sim._z_scaling.cat.full().flatten(),
        "u0": np.array(sim.u0.master).flatten().copy(),
        "p0": np.array(sim.p_fun(0).master).flatten().copy(),
        "x_scaling": sim._x_scaling,
        "z_scaling": sim._z_scaling,
    }
    return _MODEL_CACHE


def _get_step_integ(dt_report: float, relaxed: bool = False) -> ca.Function:
    """Return a cached parameterized IDAS integrator for one PE_sim step.

    The integrator treats ``vertcat(u_sym, p_sym)`` as its parameter vector so
    a single compiled function handles all control values without recompilation.

    Parameters
    ----------
    dt_report : float
        Integration horizon in seconds (one reporting interval).
    relaxed : bool
        If ``True``, use ``_IDAS_OPTS_RELAXED`` (looser tolerances).

    Returns
    -------
    ca.Function
        Compiled IDAS integrator, cached in ``_INTEG_CACHE``.
    """
    key = ("step", dt_report, relaxed)
    if key not in _INTEG_CACHE:
        mc = _get_model_cache()
        dae: dict[str, ca.SX] = {
            "x": mc["x_sym"],
            "z": mc["z_sym"],
            "p": ca.vertcat(mc["u_sym"], mc["p_sym"]),
            "ode": mc["rhs_sym"],
            "alg": mc["alg_sym"],
        }
        opts = _IDAS_OPTS_RELAXED if relaxed else _IDAS_OPTS
        _INTEG_CACHE[key] = ca.integrator(
            "step", "idas", dae, 0, [dt_report], opts,
        )
    return _INTEG_CACHE[key]


def _get_step_coll_integ(dt_report: float) -> ca.Function:
    """Return a cached collocation integrator for one PE_sim step.

    Used as a fallback when ``_get_step_integ`` / IDAS fails to converge.

    Parameters
    ----------
    dt_report : float
        Integration horizon in seconds (one reporting interval).

    Returns
    -------
    ca.Function
        Compiled Radau collocation integrator, cached in ``_INTEG_CACHE``.
    """
    key = ("step_coll", dt_report)
    if key not in _INTEG_CACHE:
        mc = _get_model_cache()
        dae: dict[str, ca.SX] = {
            "x": mc["x_sym"],
            "z": mc["z_sym"],
            "p": ca.vertcat(mc["u_sym"], mc["p_sym"]),
            "ode": mc["rhs_sym"],
            "alg": mc["alg_sym"],
        }
        _INTEG_CACHE[key] = ca.integrator(
            "step_coll", "collocation", dae, 0, [dt_report], _COLL_OPTS,
        )
    return _INTEG_CACHE[key]



def simulate_init_recipe(
    E_murphree: float,
    rr_err: float,
    LI: float,
    w_L_B_c1: float,
    x_N2: float,
    h_tot: float,
    h_weir: float,
    kappa: float,
    dt: float = 1.0,
    t_settle: float = 2000.0,
    dt_coarse: float = 100.0,
    relaxed: bool = False,
) -> dict[str, Any]:
    """Run an initialization recipe using raw CasADi integrators.

    Uses IDAS directly (not do_mpc ``make_step``) so that ramps are truly
    continuous and feedback control phases are embedded in the DAE.

    Pattern: change / settle / change / settle / ...

    Phases:
        1. Hold at default u0 (*t_settle*).
        2. Continuous linear ramp of ``e0_x_N2`` (*t_settle*).
        3. Hold (*t_settle*).
        4. Continuous linear ramp of ``e0_E_murphree`` (*t_settle*).
        5. Hold (*t_settle*).
        6. Continuous linear ramp of ``e0_rr_err`` and ``e0_rr_PLS`` (*t_settle*).
        7. Hold (*t_settle*).
        8. Continuous linear ramp of physical parameters h_tot via their u-parameters (*t_settle*).
        9. Hold (*t_settle*).
        10. Continuous linear ramp of physical parameters h_weir via their u-parameters (*t_settle*).
        11. Hold (*t_settle*).
        12. Continuous linear ramp of physical parameters kappa via their u-parameters (*t_settle*).
        13. Hold (*t_settle*).
        14. Drive ``e0_w_L_B_c1`` to *w_L_B_c1* via feed composition.
        15. Hold (*t_settle*).
        16. Drive ``e0_LI`` to *LI* via feed/bottoms.
        17. Hold (*t_settle*).

    Parameters
    ----------
    x_N2 : float
        Target mole fraction of N2.
    E_murphree : float
        Target Murphree efficiency.
    rr_err : float
        Target reflux-ratio error.
    h_tot: float
        Target theoretical stage height.
    h_weir: float
        Target weir height.
    kappa: float
        Target pressure loss coefficient.
    LI : float
        Target level indicator value.
    w_L_B_c1 : float
        Target bottoms mass fraction of component 1.
    dt : float
        Output sampling interval in seconds (default 1.0).
    t_settle : float
        Settle / hold / ramp duration in seconds (default 2000.0).
    dt_coarse : float
        Output grid spacing used for phase integration in seconds (default 100.0).
        Coarser than *dt* to keep trajectory size manageable; the IDAS integrator
        still uses its internal adaptive step.
    relaxed : bool
        Unused — present for API symmetry with :func:`PE_sim`.  IDAS tolerances
        inside the init recipe always use ``_IDAS_OPTS`` regardless of this flag.

    Returns
    -------
    dict[str, Any]
        ``"t"`` — 1-D time vector.
        ``"x"`` — array (n_x, n_t) of differential states.
        ``"z"`` — array (n_z, n_t) of algebraic states.
        ``"u"`` — array (n_u, n_t) of input values.
        ``"x_labels"`` — list of x variable names.
        ``"z_labels"`` — list of z variable names.
        ``"u_labels"`` — list of u variable names.
    """
    # ------------------------------------------------------------------
    # 1. Obtain model symbolics + consistent ICs from cache (B)
    # ------------------------------------------------------------------
    mc = _get_model_cache()
    rhs_sym: ca.SX = mc["rhs_sym"]
    alg_sym: ca.SX = mc["alg_sym"]
    x_sym: ca.SX = mc["x_sym"]
    z_sym: ca.SX = mc["z_sym"]
    u_sym: ca.SX = mc["u_sym"]
    p_sym: ca.SX = mc["p_sym"]
    t_sym: ca.SX = ca.SX.sym("t")

    x_labels: list[str] = mc["x_labels"]
    z_labels: list[str] = mc["z_labels"]
    u_labels: list[str] = mc["u_labels"]
    u_idx: dict[str, int] = mc["u_idx"]
    z_idx: dict[str, int] = mc["z_idx"]

    x0: np.ndarray = mc["x0"].copy()
    z0: np.ndarray = mc["z0"].copy()
    u0_num: np.ndarray = mc["u0"].copy()
    p0_num: np.ndarray = mc["p0"]

    # Initial u values for ramped inputs.
    x_N2_0: float = float(u0_num[u_idx["e0_x_N2"]])
    E_murphree_0: float = float(u0_num[u_idx["e0_E_murphree"]])
    rr_err_0: float = float(u0_num[u_idx["e0_rr_err"]])
    rr_PLS_0: float = float(u0_num[u_idx["e0_rr_PLS"]])
    h_tot_0: float = float(u0_num[u_idx["e0_h_tot"]])
    h_weir_0: float = float(u0_num[u_idx["e0_h_weir"]])
    kappa_0: float = float(u0_num[u_idx["e0_greek_kappa"]])

    # ------------------------------------------------------------------
    # 3. Helpers
    # ------------------------------------------------------------------
    _phase_counter: int = 0

    def _integrate_phase(
        u_expr: ca.SX,
        duration: float,
        x_init: np.ndarray,
        z_init: np.ndarray,
        dt_grid: float | None = None,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Integrate one phase.

        Parameters
        ----------
        dt_grid : float or None
            Output grid spacing.  Falls back to *dt* (function argument).

        Returns
        -------
        xf : np.ndarray, shape (n_x, n_grid)
        zf : np.ndarray, shape (n_z, n_grid)
        grid : np.ndarray, 1-D local output times (starts at 0).
        """
        nonlocal _phase_counter
        _phase_counter += 1
        step = dt_grid if dt_grid is not None else dt

        rhs_sub = ca.substitute(
            rhs_sym,
            ca.vertcat(u_sym, p_sym),
            ca.vertcat(u_expr, ca.DM(p0_num)),
        )
        alg_sub = ca.substitute(
            alg_sym,
            ca.vertcat(u_sym, p_sym),
            ca.vertcat(u_expr, ca.DM(p0_num)),
        )

        dae: dict[str, ca.SX] = {
            "x": x_sym, "z": z_sym, "t": t_sym,
            "ode": rhs_sub, "alg": alg_sub,
        }

        n_out = max(int(round(duration / step)), 1) + 1
        grid = np.linspace(0.0, duration, n_out).tolist()

        integ = ca.integrator(
            f"phase{_phase_counter}", "collocation", dae, 0, grid, _COLL_OPTS,
        )
        res = integ(x0=ca.DM(x_init), z0=ca.DM(z_init))
        return (
            np.array(res["xf"]),
            np.array(res["zf"]),
            np.array(grid),
        )

    def _u_const(vals: np.ndarray) -> ca.SX:
        """Constant SX u-vector from numeric values."""
        return ca.SX(ca.DM(vals))

    def _u_ramp(
        vals: np.ndarray,
        idx: int,
        val_start: float,
        val_end: float,
        duration: float,
    ) -> ca.SX:
        """SX u-vector with a linear ramp on entry *idx*."""
        u_e = ca.SX(ca.DM(vals))
        u_e[idx] = val_start + (val_end - val_start) * t_sym / duration
        return u_e

    # ------------------------------------------------------------------
    # 4. Trajectory collection
    # ------------------------------------------------------------------
    all_t: list[np.ndarray] = []
    all_x: list[np.ndarray] = []
    all_z: list[np.ndarray] = []
    all_u: list[np.ndarray] = []
    t_offset: float = 0.0
    x_cur: np.ndarray = x0.copy()
    z_cur: np.ndarray = z0.copy()
    u_cur: np.ndarray = u0_num.copy()

    def _append(
        t_local: np.ndarray,
        xf: np.ndarray,
        zf: np.ndarray,
        u_vals: np.ndarray,
        skip_first: bool = True,
    ) -> None:
        """Append constant-u phase, avoiding duplicate boundary points."""
        nonlocal t_offset, x_cur, z_cur
        start = 1 if (skip_first and len(all_t) > 0) else 0
        all_t.append(t_local[start:] + t_offset)
        all_x.append(xf[:, start:])
        all_z.append(zf[:, start:])
        n_pts = xf.shape[1] - start
        all_u.append(np.tile(u_vals.reshape(-1, 1), (1, n_pts)))
        t_offset += t_local[-1]
        x_cur = xf[:, -1].flatten()
        z_cur = zf[:, -1].flatten()

    def _append_ramp(
        t_local: np.ndarray,
        xf: np.ndarray,
        zf: np.ndarray,
        u_base: np.ndarray,
        ramp_idx: int,
        val_start: float,
        val_end: float,
        duration: float,
    ) -> None:
        """Append ramp phase with linearly interpolated u."""
        nonlocal t_offset, x_cur, z_cur
        start = 1 if len(all_t) > 0 else 0
        all_t.append(t_local[start:] + t_offset)
        all_x.append(xf[:, start:])
        all_z.append(zf[:, start:])
        n_pts = xf.shape[1] - start
        u_traj = np.tile(u_base.reshape(-1, 1), (1, n_pts))
        alphas = t_local[start:] / duration
        u_traj[ramp_idx, :] = val_start + alphas * (val_end - val_start)
        all_u.append(u_traj)
        t_offset += t_local[-1]
        x_cur = xf[:, -1].flatten()
        z_cur = zf[:, -1].flatten()

    # ------------------------------------------------------------------
    # 5. Run phases
    # ------------------------------------------------------------------

    # --- Phase 1: hold ---
    xf, zf, tg = _integrate_phase(_u_const(u_cur), t_settle, x_cur, z_cur, dt_coarse)
    _append(tg, xf, zf, u_cur, skip_first=False)

    # --- Phase 2: ramp x_N2 ---
    u_ramp_expr = _u_ramp(u_cur, u_idx["e0_x_N2"], x_N2_0, x_N2, t_settle)
    xf, zf, tg = _integrate_phase(u_ramp_expr, t_settle, x_cur, z_cur, dt_coarse)
    _append_ramp(tg, xf, zf, u_cur, u_idx["e0_x_N2"], x_N2_0, x_N2, t_settle)
    u_cur[u_idx["e0_x_N2"]] = x_N2

    # --- Phase 3: hold ---
    xf, zf, tg = _integrate_phase(_u_const(u_cur), t_settle, x_cur, z_cur, dt_coarse)
    _append(tg, xf, zf, u_cur)

    # --- Phase 4: ramp E_murphree ---
    u_ramp_expr = _u_ramp(
        u_cur, u_idx["e0_E_murphree"], E_murphree_0, E_murphree, t_settle,
    )
    xf, zf, tg = _integrate_phase(u_ramp_expr, t_settle, x_cur, z_cur, dt_coarse)
    _append_ramp(
        tg, xf, zf, u_cur,
        u_idx["e0_E_murphree"], E_murphree_0, E_murphree, t_settle,
    )
    u_cur[u_idx["e0_E_murphree"]] = E_murphree

    # --- Phase 5: hold ---
    xf, zf, tg = _integrate_phase(_u_const(u_cur), t_settle, x_cur, z_cur, dt_coarse)
    _append(tg, xf, zf, u_cur)

    # --- Phase 6: ramp rr_err AND rr_PLS (keep sum = 1) ---
    rr_PLS_target: float = 1.0 - rr_err
    u_p4 = ca.SX(ca.DM(u_cur))
    u_p4[u_idx["e0_rr_err"]] = (
        rr_err_0 + (rr_err - rr_err_0) * t_sym / t_settle
    )
    u_p4[u_idx["e0_rr_PLS"]] = (
        rr_PLS_0 + (rr_PLS_target - rr_PLS_0) * t_sym / t_settle
    )
    xf, zf, tg = _integrate_phase(u_p4, t_settle, x_cur, z_cur, dt_coarse)

    # Log u trajectory with both ramps interpolated.
    start = 1 if len(all_t) > 0 else 0
    all_t.append(tg[start:] + t_offset)
    all_x.append(xf[:, start:])
    all_z.append(zf[:, start:])
    n_pts = xf.shape[1] - start
    u_traj = np.tile(u_cur.reshape(-1, 1), (1, n_pts))
    alphas = tg[start:] / t_settle
    u_traj[u_idx["e0_rr_err"], :] = rr_err_0 + alphas * (rr_err - rr_err_0)
    u_traj[u_idx["e0_rr_PLS"], :] = rr_PLS_0 + alphas * (rr_PLS_target - rr_PLS_0)
    all_u.append(u_traj)
    t_offset += tg[-1]
    x_cur = xf[:, -1].flatten()
    z_cur = zf[:, -1].flatten()

    u_cur[u_idx["e0_rr_err"]] = rr_err
    u_cur[u_idx["e0_rr_PLS"]] = rr_PLS_target

    # --- Phase 7: hold ---
    xf, zf, tg = _integrate_phase(_u_const(u_cur), t_settle, x_cur, z_cur, dt_coarse)
    _append(tg, xf, zf, u_cur)

    # --- Phase 7a: ramp h_tot ---
    u_ramp_expr = _u_ramp(
        u_cur,
        u_idx["e0_h_tot"],
        h_tot_0,
        h_tot,
        t_settle,
    )
    xf, zf, tg = _integrate_phase(
        u_ramp_expr, t_settle, x_cur, z_cur, dt_coarse
    )
    _append_ramp(
        tg,
        xf,
        zf,
        u_cur,
        u_idx["e0_h_tot"],
        h_tot_0,
        h_tot,
        t_settle,
    )
    u_cur[u_idx["e0_h_tot"]] = h_tot


    # --- Phase 7b: hold ---
    xf, zf, tg = _integrate_phase(
        _u_const(u_cur),
        t_settle,
        x_cur,
        z_cur,
        dt_coarse,
    )
    _append(tg, xf, zf, u_cur)


    # --- Phase 7c: ramp h_weir ---
    u_ramp_expr = _u_ramp(
        u_cur,
        u_idx["e0_h_weir"],
        h_weir_0,
        h_weir,
        t_settle,
    )
    xf, zf, tg = _integrate_phase(
        u_ramp_expr, t_settle, x_cur, z_cur, dt_coarse
    )
    _append_ramp(
        tg,
        xf,
        zf,
        u_cur,
        u_idx["e0_h_weir"],
        h_weir_0,
        h_weir,
        t_settle,
    )
    u_cur[u_idx["e0_h_weir"]] = h_weir


    # --- Phase 7d: hold ---
    xf, zf, tg = _integrate_phase(
        _u_const(u_cur),
        t_settle,
        x_cur,
        z_cur,
        dt_coarse,
    )
    _append(tg, xf, zf, u_cur)


    # --- Phase 7e: ramp kappa (log-space) ---
    log10_k0: float = float(np.log10(kappa_0))
    log10_kt: float = float(np.log10(kappa))

    u_p7e = ca.SX(ca.DM(u_cur))
    u_p7e[u_idx["e0_greek_kappa"]] = ca.power(
        10.0,
        log10_k0 + (log10_kt - log10_k0) * t_sym / t_settle
    )

    xf, zf, tg = _integrate_phase(
        u_p7e,
        t_settle,
        x_cur,
        z_cur,
        dt_coarse,
    )

    start = 1 if len(all_t) > 0 else 0
    all_t.append(tg[start:] + t_offset)
    all_x.append(xf[:, start:])
    all_z.append(zf[:, start:])

    n_pts = xf.shape[1] - start
    u_traj = np.tile(u_cur.reshape(-1, 1), (1, n_pts))
    alphas = tg[start:] / t_settle
    u_traj[u_idx["e0_greek_kappa"], :] = (
        10.0 ** (
            log10_k0 +
            alphas * (log10_kt - log10_k0)
        )
    )
    all_u.append(u_traj)

    t_offset += tg[-1]
    x_cur = xf[:, -1].flatten()
    z_cur = zf[:, -1].flatten()

    u_cur[u_idx["e0_greek_kappa"]] = kappa


    # --- Phase 7f: hold ---
    xf, zf, tg = _integrate_phase(
        _u_const(u_cur),
        t_settle,
        x_cur,
        z_cur,
        dt_coarse,
    )
    _append(tg, xf, zf, u_cur)

    # --- Phase 8: drive w_L_B_c1 to target via feed composition ---
    wB_z_idx: int = z_idx["e0_w_L_B_c1"]
    current_wB: float = float(z_cur[wB_z_idx]*mc["z_scaling"]["e0_w_L_B_c1"])  # unscale for control logic
    wB_tol: float = 0.0001
    phase8_max: float = 5000.0  # seconds

    if abs(current_wB - w_L_B_c1) > wB_tol:
        x_feed_c1_val = 1.0 if current_wB < w_L_B_c1 else 0.0
        direction: float = 1.0 if current_wB < w_L_B_c1 else -1.0

        Kp: float = PI_WB_KP
        F_max: float = 1.0
        t_ramp_wb: float = PI_WB_T_RAMP

        # Ramped P controller: F_feed = alpha(t) * clip(Kp*err, 0, F_max)
        # alpha = min(1, t/t_ramp) — zero at t=0, full at t=t_ramp.
        alpha_expr = ca.fmin(1.0, t_sym / t_ramp_wb)
        err_expr = direction * (w_L_B_c1 - z_sym[wB_z_idx])
        F_feed_expr = alpha_expr * ca.fmax(0.0, ca.fmin(F_max, Kp * err_expr))

        u_p8_sx = ca.SX(ca.DM(u_cur))
        u_p8_sx[u_idx["e0_F_feed_tr9"]]    = F_feed_expr
        u_p8_sx[u_idx["e0_x_feed_tr9_c1"]] = ca.SX(x_feed_c1_val)
        u_p8_sx[u_idx["e0_x_feed_tr9_c2"]] = ca.SX(1.0 - x_feed_c1_val)
        xf, zf, tg = _integrate_phase(u_p8_sx, phase8_max, x_cur, z_cur, dt_coarse)

        t_offset += tg[-1]
        x_cur = xf[:, -1].flatten()
        z_cur = zf[:, -1].flatten()

    # Reset feed for Phase 8a hold; match current tray-9 liquid composition.
    u_cur[u_idx["e0_F_feed_tr9"]] = 0.0
    _x_L_tr9_c1_cur = float(z_cur[z_idx["e0_x_L_tr9_c1"]] * mc["z_scaling"]["e0_x_L_tr9_c1"])
    u_cur[u_idx["e0_x_feed_tr9_c1"]] = _x_L_tr9_c1_cur
    u_cur[u_idx["e0_x_feed_tr9_c2"]] = 1.0 - _x_L_tr9_c1_cur

    # --- Phase 8a: hold ---
    xf, zf, tg = _integrate_phase(_u_const(u_cur), t_settle, x_cur, z_cur, dt_coarse)
    _append(tg, xf, zf, u_cur)

    # --- Phase 9: drive LI to target via smooth sigmoid control ---
    li_z_idx: int = z_idx["e0_LI"]
    current_li: float = float(z_cur[li_z_idx]*mc["z_scaling"]["e0_LI"])  # unscale for control logic
    li_tol: float = 0.01
    phase9_max: float = 3000.0  # seconds

    if abs(current_li - LI) > li_tol:
        li_going_up: bool = current_li < LI
        direction_li: float = 1.0 if li_going_up else -1.0
        mv_idx: int = u_idx["e0_F_feed_tr9"] if li_going_up else u_idx["e0_F_B"]

        Kp_li: float = PI_LI_KP
        F_max_li: float = 1.0
        t_ramp_li: float = PI_LI_T_RAMP

        alpha_li = ca.fmin(1.0, t_sym / t_ramp_li)
        err_expr_li = direction_li * (LI - z_sym[li_z_idx]*mc["z_scaling"]["e0_LI"])
        F_mv_expr = alpha_li * ca.fmax(0.0, ca.fmin(F_max_li, Kp_li * err_expr_li))

        u_p9_sx = ca.SX(ca.DM(u_cur))
        u_p9_sx[mv_idx] = F_mv_expr
        u_p9_sx[u_idx["e0_x_feed_tr9_c1"]] = z_sym[z_idx["e0_x_L_tr9_c1"]]
        u_p9_sx[u_idx["e0_x_feed_tr9_c2"]] = 1.0 - z_sym[z_idx["e0_x_L_tr9_c1"]]

        xf, zf, tg = _integrate_phase(u_p9_sx, phase9_max, x_cur, z_cur, dt_coarse)

        t_offset += tg[-1]
        x_cur = xf[:, -1].flatten()
        z_cur = zf[:, -1].flatten()

    # Reset flows for Phase 10.
    u_cur[u_idx["e0_F_feed_tr9"]] = 0.0
    u_cur[u_idx["e0_F_B"]] = 0.0

    # --- Phase 10: hold ---
    xf, zf, tg = _integrate_phase(_u_const(u_cur), 2*t_settle, x_cur, z_cur, dt_coarse)
    _append(tg, xf, zf, u_cur)

    # ------------------------------------------------------------------
    # 6. Assemble output
    # ------------------------------------------------------------------
    return {
        "t": np.concatenate(all_t),
        "x": np.hstack(all_x),
        "x_unscaled": np.hstack(all_x)*mc["x_scaling"].cat.full().flatten()[:, None],
        "z": np.hstack(all_z),
        "z_unscaled": np.hstack(all_z)*mc["z_scaling"].cat.full().flatten()[:, None],
        "u": np.hstack(all_u),
        "x_labels": x_labels,
        "z_labels": z_labels,
        "u_labels": u_labels,
    }


def extract_final_state(
    result: dict[str, Any],
) -> dict[str, dict[str, float]]:
    """Extract final x, z, u values from a CasADi recipe result.

    Returns a dict with keys ``"x"``, ``"z"``, ``"u"``, each mapping
    variable names to their final scalar values.  Same structure as
    :func:`~models.batchcol_model_dompc_pe_init.extract_final_state`.

    Seed a do_mpc simulator via::

        state = extract_final_state(result)
        for name, val in state["x"].items():
            sim.x0[name] = val
        for name, val in state["z"].items():
            sim.z0[name] = val
        for name, val in state["u"].items():
            sim.u0[name] = val

    Parameters
    ----------
    result : dict
        Output of :func:`simulate_init_recipe`.

    Returns
    -------
    dict[str, dict[str, float]]
        ``{"x": {name: value, ...}, "z": {...}, "u": {...}}``.
    """
    out: dict[str, dict[str, float]] = {}
    for category, label_key in (
        ("x", "x_labels"),
        ("z", "z_labels"),
        ("u", "u_labels"),
    ):
        vals = result[category][:, -1]
        labels = result[label_key]
        out[category] = {
            name: float(vals[i]) for i, name in enumerate(labels)
        }
    return out


def PE_sim(
    E_murphree: float,
    rr_err: float,
    LI: float,
    w_L_B_c1: float,
    U: np.ndarray,
    x_N2: float,
    h_tot: float,
    h_weir: float,
    kappa: float,
    outputs: list[str] | None = None,
    dt_report: float = 120.0,
    relaxed: bool = False,
) -> dict[str, Any]:
    """Run init recipe then simulate with piecewise-constant controls.

    Parameters
    ----------
    E_murphree : float
        Murphree tray efficiency (passed to :func:`simulate_init_recipe`).
    rr_err : float
        Reflux-ratio error target (passed to :func:`simulate_init_recipe`).
    LI : float
        Target level indicator value (passed to :func:`simulate_init_recipe`).
    w_L_B_c1 : float
        Target bottoms mass fraction of component 1 (passed to
        :func:`simulate_init_recipe`).
    U : np.ndarray
        Control trajectory, shape ``(N, 2)`` where column 0 is ``rr_PLS``
        and column 1 is ``Q_PLS_R``.  Each row is held constant for
        *dt_report* seconds.
    x_N2 : float
        Target N2 mole fraction (passed to :func:`simulate_init_recipe`).
    h_tot : float
        Total tray height parameter (passed to :func:`simulate_init_recipe`).
    h_weir : float
        Weir height parameter (passed to :func:`simulate_init_recipe`).
    kappa : float
        Pressure loss coefficient (passed to :func:`simulate_init_recipe`).
    outputs : list[str] or None
        Variable names to include in ``"y"``.  Names are looked up in
        both x and z labels.  If *None*, ``"y"`` is omitted from the
        result.
    dt_report : float
        Reporting / step interval in seconds (default 120.0).
    relaxed : bool
        If ``True``, use relaxed IDAS tolerances for the PE_sim steps
        (passed to :func:`_get_step_integ` and :func:`_get_step_coll_integ`).
        Does not affect the init-recipe phases.

    Returns
    -------
    dict[str, Any]
        ``"t"`` — 1-D time array, length N+1 (includes t=0).
        ``"x"`` — array (n_x, N+1) differential states.
        ``"z"`` — array (n_z, N+1) algebraic states.
        ``"u"`` — array (n_u, N) applied inputs (one per interval).
        ``"y"`` — array (N+1, len(outputs)) selected outputs (if *outputs* given).
        ``"x_labels"`` — list of x variable names.
        ``"z_labels"`` — list of z variable names.
        ``"u_labels"`` — list of u variable names.
    """
    U = np.asarray(U)
    if U.ndim != 2 or U.shape[1] != 2:
        raise ValueError("U must be shape (N, 2): columns [rr_PLS, Q_PLS_R]")
    n_intervals: int = U.shape[0]

    # --- 1. Init recipe ---
    recipe = simulate_init_recipe(
        E_murphree=E_murphree, rr_err=rr_err, LI=LI, w_L_B_c1=w_L_B_c1,
        x_N2=x_N2, h_tot=h_tot, h_weir=h_weir, kappa=kappa, relaxed=relaxed,
    )
    state = extract_final_state(recipe)

    # --- 2. Load symbolics + ICs from cache (B+C) ---
    mc = _get_model_cache()
    x_labels: list[str] = mc["x_labels"]
    z_labels: list[str] = mc["z_labels"]
    u_labels: list[str] = mc["u_labels"]
    u_idx: dict[str, int] = mc["u_idx"]
    p0_num: np.ndarray = mc["p0"]

    # Base u from recipe final state.
    u_base = np.array([state["u"][name] for name in u_labels])

    # --- 3. Simulate N intervals (A) ---
    # One parameterized integrator compiled once; called N times with different p.
    x_init = np.array([state["x"][name] for name in x_labels])
    z_init = np.array([state["z"][name] for name in z_labels])

    integ = _get_step_integ(dt_report, relaxed=relaxed)
    coll_integ = _get_step_coll_integ(dt_report)
    p0_dm = ca.DM(p0_num)

    # Collect trajectories (include initial point).
    xs: list[np.ndarray] = [x_init.copy()]
    zs: list[np.ndarray] = [z_init.copy()]
    us: list[np.ndarray] = []

    for k in range(n_intervals):
        u_k = u_base.copy()
        u_k[u_idx["e0_rr_PLS"]] = U[k, 0]
        u_k[u_idx["e0_Q_PLS_R"]] = U[k, 1]
        u_k[u_idx["e0_x_N2"]] = x_N2
        u_k[u_idx["e0_h_tot"]] = h_tot
        u_k[u_idx["e0_h_weir"]] = h_weir
        u_k[u_idx["e0_greek_kappa"]] = kappa
        p_k = ca.vertcat(ca.DM(u_k), p0_dm)
        x0_dm, z0_dm = ca.DM(x_init), ca.DM(z_init)
        use_coll = True
        try:
            res = coll_integ(x0=x0_dm, z0=z0_dm, p=p_k)
            xf_arr = np.array(res["xf"]).flatten()
            if not np.all(np.isfinite(xf_arr)):
                use_coll = False
        except Exception:
            use_coll = False
        if not use_coll:
            res = integ(x0=x0_dm, z0=z0_dm, p=p_k)
            xf_arr = np.array(res["xf"]).flatten()

        x_init = xf_arr
        z_init = np.array(res["zf"]).flatten()

        xs.append(x_init.copy())
        zs.append(z_init.copy())
        us.append(u_k.copy())

    t = np.arange(n_intervals + 1) * dt_report

    x_full_scaled = np.column_stack(xs)
    z_full_scaled = np.column_stack(zs)

    x_full = x_full_scaled * mc["x_scaling"].master.full()
    z_full = z_full_scaled * mc["z_scaling"].master.full()

    result: dict[str, Any] = {
        "t": t,
        "x_scaled": x_full_scaled,
        "x": x_full,
        "z_scaled": z_full_scaled,
        "z": z_full,
        "u": np.column_stack(us),
        "x_labels": x_labels,
        "z_labels": z_labels,
        "u_labels": u_labels,
    }

    if outputs is not None:
        x_idx_map = {name: i for i, name in enumerate(x_labels)}
        z_idx_map = {name: i for i, name in enumerate(z_labels)}
        y_cols: list[np.ndarray] = []
        for name in outputs:
            if name in x_idx_map:
                y_cols.append(x_full[x_idx_map[name], :])
            elif name in z_idx_map:
                y_cols.append(z_full[z_idx_map[name], :])
            else:
                raise ValueError(f"Output '{name}' not found in x or z labels")
        result["y"] = np.column_stack(y_cols)
    return result
