"""Parallel convergence study: approach 1 (continuation-based initialization) vs approach 2 (steady-state initialization).

This module runs a Monte-Carlo convergence study that compares two strategies
for computing initial conditions (ICs) for a distillation-column DAE model:

- **Approach 1** - Full initialization recipe (``simulate_init_recipe``):
  integrates a continuation path to reach a physically consistent IC.
- **Approach 2** - Steady-state rootfinder: solves a pinned algebraic system
  directly to obtain the IC in a single Newton solve.

For each random parameter sample the module records whether each approach
produces an IC from which the closed-loop simulator converges over a fixed
experiment horizon, together with wall-clock timing.

Usage:
    conda run -n PE_ca python3 initialization_convergence_study/convergence_study_parallel.py
"""

from __future__ import annotations

import csv
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
from joblib import Parallel, delayed

_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_root))
sys.path.insert(0, str(_root / "parameter_estimation"))

from models.simulate_init_recipe import (
    _get_model_cache,
    _get_step_coll_integ,
    _get_step_integ,
    extract_final_state,
    simulate_init_recipe,
)
from parameter_estimation import (
    _FIXED_H_TOT,
    _FIXED_KAPPA,
    load_experiment,
)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

BOUNDS = {
    "E_murphree": (0.15, 1.0),
    "rr_err":     (-0.25, 0.0),
    "x_N2":       (0.043, 0.15),
    "h_weir":     (0.005, 0.04),
}

_Z_RES_TOL = 1e-4


# ---------------------------------------------------------------------------
# Helpers (module-level → picklable by loky)
# ---------------------------------------------------------------------------

def _build_ss_rootfinder(mc: dict) -> tuple:
    """Build a pinned steady-state rootfinder for the DAE model.

    Constructs a CasADi ``rootfinder`` that simultaneously solves the
    differential and algebraic residuals of the model while pinning three
    state/algebraic variables to externally supplied values.  The pins are:

    - ``e0_HU_tr9_c1`` (holdup tray 9, component 1) - supplied as a parameter.
    - ``e0_HU_D_c1`` / ``e0_HU_D_c2`` (distillate holdups) - fixed to their
      nominal steady-state values from ``mc["x0"]``.
    - ``e0_LI`` (level indicator) and ``e0_w_L_B_c1`` (bottom mass fraction) -
      supplied as parameters.

    The resulting system has the same dimension as the original DAE; the pinned
    equations replace the corresponding ODE rows and algebraic equations.

    Parameters
    ----------
    mc : dict
        Model cache returned by ``_get_model_cache()``.  Must contain CasADi
        symbolic expressions ``x_sym``, ``z_sym``, ``u_sym``, ``p_sym``,
        ``alg_sym``, ``rhs_sym`` and the label lists ``x_labels``,
        ``z_labels``, together with the nominal arrays ``x0``.

    Returns
    -------
    rf_ss : casadi.Function
        CasADi rootfinder (Newton method) for the pinned steady-state system.
    fg_fn : casadi.Function
        Residual function ``fg(xz, up_hu)`` — useful for evaluating convergence
        of the rootfinder solution.
    SS_HU_D_c1 : float
        Nominal steady-state value for ``e0_HU_D_c1`` (used as a pin value).
    SS_HU_D_c2 : float
        Nominal steady-state value for ``e0_HU_D_c2`` (used as a pin value).
    """
    import casadi as ca

    x_sym    = mc["x_sym"];  z_sym    = mc["z_sym"]
    u_sym    = mc["u_sym"];  p_sym    = mc["p_sym"]
    alg_sym  = mc["alg_sym"]; rhs_sym = mc["rhs_sym"]
    x_labels = mc["x_labels"]; z_labels = mc["z_labels"]

    HU_tr9_c1_p = ca.SX.sym("HU_tr9_c1_param")
    LI_p        = ca.SX.sym("LI_param")
    wB_p        = ca.SX.sym("wB_param")

    SS_HU_D_c1 = float(mc["x0"][x_labels.index("e0_HU_D_c1")])
    SS_HU_D_c2 = float(mc["x0"][x_labels.index("e0_HU_D_c2")])

    x_pin = {
        x_labels.index("e0_HU_tr9_c1"): HU_tr9_c1_p,
        x_labels.index("e0_HU_D_c1"):   SS_HU_D_c1,
        x_labels.index("e0_HU_D_c2"):   SS_HU_D_c2,
    }
    f_rows = [x_sym[i] - x_pin[i] if i in x_pin else fi
              for i, fi in enumerate(ca.vertsplit(rhs_sym))]
    g_rows = list(ca.vertsplit(alg_sym))
    g_rows[z_labels.index("e0_LI")]       = z_sym[z_labels.index("e0_LI")]       - LI_p
    g_rows[z_labels.index("e0_w_L_B_c1")] = z_sym[z_labels.index("e0_w_L_B_c1")] - wB_p

    xz_sym    = ca.vertcat(x_sym, z_sym)
    up_hu_sym = ca.vertcat(u_sym, p_sym, HU_tr9_c1_p, LI_p, wB_p)
    fg_pinned = ca.vertcat(*f_rows, *g_rows)
    fg_fn     = ca.Function("fg_ss", [xz_sym, up_hu_sym], [fg_pinned])
    rf_ss     = ca.rootfinder("rf_ss", "newton", fg_fn, {"error_on_fail": False})

    return rf_ss, fg_fn, SS_HU_D_c1, SS_HU_D_c2


def _compute_HU_tr9_c1_scaled(
    p_tr9_sc: float, LI_sc: float, T_tr9_sc: float, w_L_B_c1: float,
) -> float:
    """Compute scaled holdup of component 1 on tray 9 from physical quantities.

    Derives the total molar holdup on tray 9 (liquid + vapour, component 1)
    from first principles using Wilson activity coefficients and Antoine
    vapour-pressure correlation, then returns the value on the model's internal
    scaling (divided by 100).

    Parameters
    ----------
    p_tr9_sc : float
        Scaled pressure on tray 9 (model units, i.e. ``p [bar] / 1``; used
        directly as bar).
    LI_sc : float
        Scaled liquid level indicator (``LI [%] / 10``).
    T_tr9_sc : float
        Scaled temperature on tray 9 (``T [K] / 100``).
    w_L_B_c1 : float
        Mass fraction of component 1 in the liquid bottom stream (unscaled).

    Returns
    -------
    float
        Scaled holdup of component 1 on tray 9 (model internal units).
    """
    p  = p_tr9_sc
    LI = LI_sc * 10.0
    T  = T_tr9_sc * 100.0
    w  = w_L_B_c1
    M1, M2   = 0.046, 0.018
    v1, v2   = 5.869e-5, 1.813e-5
    R        = 8.314
    A1,B1,C1 = 5.24677, 1598.673, -46.424
    lc1, lc2 = 95.68, 506.7
    V_tot    = 0.06
    x1  = w * M2 / (M1 * (1.0 - w) + w * M2)
    x2  = 1.0 - x1
    v_L = x1 * v1 + x2 * v2
    V_L = LI * V_tot / 100.0
    V_V = V_tot - V_L
    HU_L = V_L / v_L
    HU_V = p * 1e5 * V_V / (R * T)
    a1 = (v2 / v1) * np.exp(-lc1 / T)
    a2 = (v1 / v2) * np.exp(-lc2 / T)
    d1 = x1 + a1 * x2
    d2 = x2 + a2 * x1
    g1 = (1.0 / d1) * np.exp(x2 * (a1 / d1 - a2 / d2))
    pLV1 = 10.0 ** (A1 - B1 / (T + C1))
    y1   = pLV1 * g1 / p * x1
    return (HU_L * x1 + HU_V * y1) / 100.0


def _converges(
    x_init: np.ndarray, z_init: np.ndarray, u_phys: np.ndarray,
    exp_U: np.ndarray, n_steps: int,
    step_i: Any, coll_i: Any, mc: dict,
) -> bool:
    """Check whether a given initial condition yields a converging simulation.

    Steps the DAE model forward for ``n_steps`` time steps using the
    experiment input sequence ``exp_U``.  At each step a collocation
    integrator is attempted first; if it fails or produces non-finite states,
    a simpler explicit step integrator is used as a fallback.  The IC is
    considered non-converging if the fallback also fails.

    Parameters
    ----------
    x_init : np.ndarray
        Initial differential state vector, shape ``(n_x,)``, in model-scaled
        units.
    z_init : np.ndarray
        Initial algebraic state vector, shape ``(n_z,)``, in model-scaled
        units.
    u_phys : np.ndarray
        Base physical input vector, shape ``(n_u,)``.  The experiment inputs
        ``e0_rr_PLS`` and ``e0_Q_PLS_R`` are overwritten at each step from
        ``exp_U``.
    exp_U : np.ndarray
        Experiment input trajectory, shape ``(n_steps, 2)``.  Column 0 is
        ``e0_rr_PLS``, column 1 is ``e0_Q_PLS_R``.
    n_steps : int
        Number of simulation steps to attempt.
    step_i : casadi.Function
        Explicit step integrator (used as fallback).
    coll_i : casadi.Function
        Collocation integrator (attempted first at each step).
    mc : dict
        Model cache returned by ``_get_model_cache()``.

    Returns
    -------
    bool
        ``True`` if the simulation completes all ``n_steps`` with finite
        states; ``False`` if any step fails irreversibly.
    """
    import casadi as ca
    u_idx = mc["u_idx"]
    p0    = ca.DM(mc["p0"])
    x_cur, z_cur = x_init.copy(), z_init.copy()
    for k in range(n_steps):
        u_k = u_phys.copy()
        u_k[u_idx["e0_rr_PLS"]]  = exp_U[k, 0]
        u_k[u_idx["e0_Q_PLS_R"]] = exp_U[k, 1]
        p_k = ca.vertcat(ca.DM(u_k), p0)
        try:
            res = coll_i(x0=ca.DM(x_cur), z0=ca.DM(z_cur), p=p_k)
            xf  = np.array(res["xf"]).flatten()
            if not np.all(np.isfinite(xf)):
                raise ValueError
        except Exception:
            try:
                res = step_i(x0=ca.DM(x_cur), z0=ca.DM(z_cur), p=p_k)
                xf  = np.array(res["xf"]).flatten()
                if not np.all(np.isfinite(xf)):
                    return False
            except Exception:
                return False
        x_cur = xf
        z_cur = np.array(res["zf"]).flatten()
    return True


# ---------------------------------------------------------------------------
# Per-sample worker (module-level → loky can pickle it)
# ---------------------------------------------------------------------------

def _run_sample(
    s: int,
    E: float, rr: float, xN2: float, hw: float,
    ic_LI: float, ic_w_L_B_c1: float,
    exp_U: np.ndarray,
    dt_report: float,
    T_tr9_t0: float,
) -> dict[str, Any]:
    """Evaluate both initialization approaches for one parameter sample.

    Builds model and integrator objects locally (required for loky
    pickling), then runs approach 1 (initialization recipe) and approach 2
    (steady-state rootfinder) in sequence.  Each approach's result — whether
    the simulation converges and wall-clock time — is recorded in the returned
    dictionary.

    Parameters
    ----------
    s : int
        Zero-based sample index; stored as ``s + 1`` in the result row.
    E : float
        Murphree efficiency sample value.
    rr : float
        Reflux-ratio error sample value.
    xN2 : float
        Nitrogen mole fraction sample value.
    hw : float
        Weir height sample value (m).
    ic_LI : float
        Initial liquid level indicator (%) from the experiment.
    ic_w_L_B_c1 : float
        Initial bottom mass fraction of component 1 from the experiment.
    exp_U : np.ndarray
        Experiment input trajectory, shape ``(n_steps, 2)``.
    dt_report : float
        Reporting interval (s) used to build the step integrators.
    T_tr9_t0 : float
        Initial temperature on tray 9 (K), used to compute the tray-9 holdup
        initial guess for approach 2.

    Returns
    -------
    dict[str, Any]
        Row dictionary with keys: ``sample``, ``E_murphree``, ``rr_err``,
        ``x_N2``, ``h_weir``, ``h_tot``, ``kappa``, ``recipe_ok``,
        ``approach_1``, ``approach_2``, ``time_1``, ``time_2``.
    """
    import casadi as ca

    mc       = _get_model_cache()
    x_labels = mc["x_labels"]; z_labels = mc["z_labels"]; u_labels = mc["u_labels"]
    u_idx    = mc["u_idx"];    p0_num   = mc["p0"]
    ht, kap  = _FIXED_H_TOT, _FIXED_KAPPA
    n_steps  = exp_U.shape[0]

    step_i = _get_step_integ(dt_report, relaxed=False)
    coll_i = _get_step_coll_integ(dt_report)
    rf_ss, fg_fn, SS_HU_D_c1, SS_HU_D_c2 = _build_ss_rootfinder(mc)

    row: dict[str, Any] = {
        "sample": s + 1,
        "E_murphree": E, "rr_err": rr, "x_N2": xN2, "h_weir": hw,
        "h_tot": ht, "kappa": kap,
        "recipe_ok": 0, "approach_1": 0, "approach_2": 0,
        "time_1": float("nan"), "time_2": float("nan"),
    }

    # --- Approach 1: full init recipe ---
    try:
        t0   = time.perf_counter()
        rec  = simulate_init_recipe(
            E_murphree=E, rr_err=rr, LI=ic_LI, w_L_B_c1=ic_w_L_B_c1,
            x_N2=xN2, h_tot=ht, h_weir=hw, kappa=kap,
        )
        row["time_1"] = time.perf_counter() - t0
        fs   = extract_final_state(rec)
        x_ic = np.array([fs["x"][n] for n in x_labels])
        z_ic = np.array([fs["z"][n] for n in z_labels])
        u_b  = np.array([fs["u"][n] for n in u_labels])
        row["recipe_ok"] = 1
        row["approach_1"] = int(_converges(x_ic, z_ic, u_b, exp_U, n_steps, step_i, coll_i, mc))
    except Exception:
        pass

    # --- Approach 2: steady-state rootfinder ---
    u2 = mc["u0"].copy()
    u2[u_idx["e0_E_murphree"]]  = E
    u2[u_idx["e0_rr_err"]]      = rr
    u2[u_idx["e0_rr_PLS"]]      = 1.0 - rr
    u2[u_idx["e0_x_N2"]]        = xN2
    u2[u_idx["e0_h_tot"]]       = ht
    u2[u_idx["e0_h_weir"]]      = hw
    u2[u_idx["e0_greek_kappa"]] = kap

    LI_sc       = ic_LI / 10.0
    w_L_B_c1_sc = ic_w_L_B_c1
    T_tr9_sc    = T_tr9_t0 / 100.0
    hu_tr9_c1   = _compute_HU_tr9_c1_scaled(
        float(mc["z0"][z_labels.index("e0_p_tr9")]),
        LI_sc, T_tr9_sc, w_L_B_c1_sc,
    )
    x_g = mc["x0"].copy()
    x_g[x_labels.index("e0_HU_tr9_c1")] = hu_tr9_c1
    x_g[x_labels.index("e0_HU_D_c1")]   = SS_HU_D_c1
    x_g[x_labels.index("e0_HU_D_c2")]   = SS_HU_D_c2
    z_g = mc["z0"].copy()
    z_g[z_labels.index("e0_LI")]        = LI_sc
    z_g[z_labels.index("e0_w_L_B_c1")]  = w_L_B_c1_sc
    z_g[z_labels.index("e0_T_tr9")]     = T_tr9_sc

    p_val  = ca.vertcat(ca.DM(u2), ca.DM(p0_num),
                        ca.DM([hu_tr9_c1, LI_sc, w_L_B_c1_sc]))
    t0     = time.perf_counter()
    xz_sol = np.array(rf_ss(ca.DM(np.concatenate([x_g, z_g])), p_val)).flatten()
    row["time_2"] = time.perf_counter() - t0
    resid  = float(np.max(np.abs(np.array(fg_fn(ca.DM(xz_sol), p_val)).flatten())))

    if resid <= _Z_RES_TOL:
        nx   = len(x_labels)
        x_ss = xz_sol[:nx];  z_ss = xz_sol[nx:]
        row["approach_2"] = int(_converges(x_ss, z_ss, u2, exp_U, n_steps, step_i, coll_i, mc))

    return row


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

def run_study(
    exp_path: Path,
    n_samples: int = 100,
    seed: int = 123,
    n_jobs: int = -1,
) -> None:
    """Run the parallel convergence study and write results to CSV files.

    Draws ``n_samples`` parameter vectors uniformly from ``BOUNDS``, dispatches
    one ``_run_sample`` call per vector using ``joblib.Parallel`` (loky
    backend), and writes three CSV files to a timestamped output directory:

    - ``samples.csv``  - per-sample results (parameters + convergence flags + timing).
    - ``summary.csv``  - aggregate converged counts per approach.
    - ``timing_stats.csv`` - min / max / mean / std of wall-clock time per approach.

    Parameters
    ----------
    exp_path : Path
        Path to the experiment trajectories pickle file (``trajectories.pkl``).
        Loaded via ``load_experiment`` to extract the input trajectory,
        reporting interval, and initial condition values.
    n_samples : int, optional
        Number of random parameter samples to draw.  Default is ``100``.
    seed : int, optional
        Seed for the NumPy ``default_rng`` used to draw parameter samples.
        Default is ``123``.
    n_jobs : int, optional
        Number of parallel workers passed to ``joblib.Parallel``.  ``-1``
        uses all available CPUs.  Default is ``-1``.
    """
    exp = load_experiment(exp_path)

    _ts       = datetime.now().strftime("%y%m%d%H%M%S")
    figs_dir  = Path(__file__).parent / f"figs_{_ts}"
    figs_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output dir: {figs_dir}")

    rng    = np.random.default_rng(seed)
    params = np.column_stack([
        rng.uniform(*BOUNDS["E_murphree"], n_samples),
        rng.uniform(*BOUNDS["rr_err"],     n_samples),
        rng.uniform(*BOUNDS["x_N2"],       n_samples),
        rng.uniform(*BOUNDS["h_weir"],     n_samples),
    ])

    print(f"Dispatching {n_samples} samples to {n_jobs} workers...")
    results: list[dict] = Parallel(n_jobs=n_jobs, backend="loky", verbose=5)(
        delayed(_run_sample)(
            s=s,
            E=float(params[s, 0]), rr=float(params[s, 1]),
            xN2=float(params[s, 2]), hw=float(params[s, 3]),
            ic_LI=exp.ic_LI,
            ic_w_L_B_c1=exp.ic_w_L_B_c1,
            exp_U=exp.U,
            dt_report=exp.dt_report,
            T_tr9_t0=float(exp.exp_states[0, 4]),
        )
        for s in range(n_samples)
    )

    results.sort(key=lambda r: r["sample"])

    # --- samples.csv ---
    _FIELDS = ["sample", "E_murphree", "rr_err", "x_N2", "h_weir",
               "h_tot", "kappa", "recipe_ok", "approach_1", "approach_2",
               "time_1", "time_2"]
    sample_path = figs_dir / "samples.csv"
    with open(sample_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=_FIELDS)
        w.writeheader(); w.writerows(results)
    print(f"Sample log: {sample_path}")

    # --- summary.csv ---
    counts = [sum(r["approach_1"] for r in results),
              sum(r["approach_2"] for r in results)]
    summary_path = figs_dir / "summary.csv"
    with open(summary_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["approach", "converged", "n_samples"])
        w.writeheader()
        w.writerow({"approach": "approach_1", "converged": counts[0], "n_samples": n_samples})
        w.writerow({"approach": "approach_2", "converged": counts[1], "n_samples": n_samples})
    print(f"Summary:    {summary_path}")
    print(f"approach_1: {counts[0]}/{n_samples}  approach_2: {counts[1]}/{n_samples}")

    # --- timing_stats.csv ---
    timing_path = figs_dir / "timing_stats.csv"
    with open(timing_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["approach", "min", "max", "mean", "std", "n"])
        w.writeheader()
        for key, label in [("time_1", "approach_1"), ("time_2", "approach_2")]:
            t = np.array([r[key] for r in results], dtype=float)
            t = t[np.isfinite(t)]
            w.writerow({
                "approach": label,
                "min":  float(np.min(t))  if t.size else float("nan"),
                "max":  float(np.max(t))  if t.size else float("nan"),
                "mean": float(np.mean(t)) if t.size else float("nan"),
                "std":  float(np.std(t))  if t.size else float("nan"),
                "n": t.size,
            })
    print(f"Timing:     {timing_path}")


if __name__ == "__main__":
    EXP_PATH = (
        _root / "data/experimentaldata"
        / "trained_agent_1IC_260414_1/results/trajectories.pkl"
    )
    run_study(
        exp_path=EXP_PATH,
        n_samples=1000,
        seed=67,
        n_jobs=50,
    )
