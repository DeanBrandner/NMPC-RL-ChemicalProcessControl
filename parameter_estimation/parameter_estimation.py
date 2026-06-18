"""Parameter estimation for a binary distillation column via Bayesian Optimization.

Estimates four model parameters — ``E_murphree``, ``rr_err``, ``x_N2``, and
``h_weir`` — by minimizing a weighted least-squares (WLS) criterion between
``PE_sim`` output and experimental state trajectories from multiple experiments.

The module provides:

- A CasADi Wilson VLE softsensor (``_get_ca_wilson_solver``) precomputed on an
  x_N2 grid so that per-iteration composition recalculation is a cheap
  ``np.interp`` call.
- Parallel experiment simulation via joblib (loky backend).
- Bayesian Optimization via ``bayes_opt``.
- Checkpoint/recovery via ``probes.csv`` and ``bo_state.json``.

Usage (CLI):
    conda run -n PE_ca python parameter_estimation/parameter_estimation.py \\
        --data-root ./data/experimentaldata --init-points 5 --n-iter 25
"""

from __future__ import annotations

import csv
import dataclasses
import json
import logging
import pickle
import sys
import time
import warnings
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

import casadi as ca
import numpy as np
import pandas as pd
from bayes_opt import BayesianOptimization

sys.path.insert(0, str(Path(__file__).parent.parent))
from models.simulate_init_recipe import PE_sim  # noqa: E402

try:
    from joblib import Parallel, delayed

    _JOBLIB_AVAILABLE = True
except ImportError:
    _JOBLIB_AVAILABLE = False
    warnings.warn("joblib not installed; experiments run sequentially", stacklevel=1)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

WLS_OUTPUTS: list[str] = ["e0_LI", "e0_WI", "e0_w_L_D_c1", "e0_w_L_B_c1", "e0_T_tr9"]
WLS_STATE_NAMES: list[str] = ["LI", "WI", "w_L_D_c1", "w_L_B_c1", "T_tr9"]
EXP_STATE_COLS: list[int] = [0, 1, 2, 3, 4]

DEFAULT_WEIGHTS: dict[str, float] = {name: 1.0 for name in WLS_STATE_NAMES}

# Known sensor noise std devs (sigma) — fill these in before running PE.
# Weights are computed as w_i = 1/sigma ** 2_i when passed as noise_std to run_pe().
DEFAULT_NOISE_STD: dict[str, float] = {
    "LI":       1e6,  # [−]    level indicator std dev
    "WI":       20.0,     # [g]    weight indicator std dev
    "w_L_D_c1": 0.001,   # [−]    distillate composition std dev
    "w_L_B_c1": 1e6,   # [−]    bottoms composition std dev
    "T_tr9":    0.05,  # [K]    stage-9 temperature std dev
}

_DT_TOL: float = 1.0

_FIXED_H_TOT: float = 0.179372959955645
_FIXED_KAPPA: float = 0.0424670248823593

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Softsensor — Wilson VLE (CasADi) + cumulative mass balance (numpy)
# Precomputed on x_N2 grid before optimisation; workers do np.interp (ns-fast).
# ---------------------------------------------------------------------------

_SS_X_N2_GRID: np.ndarray = np.linspace(0.043, 0.15, 100)

# Wilson VLE initial guess: [x1, y1] — ethanol(1) mole fractions in liquid/vapor
_SS_X0: np.ndarray = np.array([0.12443, 0.47181])

# Module-level cached CasADi Wilson VLE rootfinder + residual function.
_CA_WILSON_SOLVER: ca.Function | None = None
_CA_WILSON_RESID:  ca.Function | None = None


def _get_ca_wilson_solver() -> ca.Function:
    r"""Build (or return cached) CasADi Wilson VLE rootfinder.

    Solves the isothermal binary VLE system with an inert N2 vapour correction:

    .. math::

        y_i P = x_i \gamma_i(T, \mathbf{x}) P_i^{\text{sat}}(T), \quad i \in \{1, 2\}

    Activity coefficients :math:`\gamma_i` follow the Wilson model with
    temperature-dependent interaction parameters.  Vapour pressures follow
    the VDI extended Antoine equation.

    The rootfinder is constructed once and stored in the module-level
    ``_CA_WILSON_SOLVER`` / ``_CA_WILSON_RESID`` globals; subsequent calls
    return the cached object immediately.

    Returns
    -------
    ca.Function
        CasADi rootfinder ``wilson_vle(X0, p) → X`` with unknowns
        ``X = [x1, y1]`` (ethanol mole fractions in liquid and vapour) and
        parameters ``p = [T (K), P (bar), x_N2]``.
    """
    global _CA_WILSON_SOLVER
    if _CA_WILSON_SOLVER is not None:
        return _CA_WILSON_SOLVER
    global _CA_WILSON_RESID

    X     = ca.SX.sym("X", 2)
    x1, y1 = X[0], X[1]
    p_sym = ca.SX.sym("p", 3)
    T_K, P, xN2 = p_sym[0], p_sym[1], p_sym[2]

    x2 = 1.0 - x1
    y2 = 1.0 - y1 - xN2

    # Fixed physical constants — ethanol(1) / water(2)
    Tc1 = 513.9;     Pc1 = 61.48
    Tc2 = 647.1;     Pc2 = 220.64
    VDI_A1=-8.33801; VDI_B1=0.08719;  VDI_C1=-3.30578; VDI_D1=-0.25986
    VDI_A2=-7.86975; VDI_B2=1.90561;  VDI_C2=-2.30891; VDI_D2=-2.06472
    WilA12=-2.5035;  WilB12=346.151   # Λ12 = exp(A12 + B12/T)
    WilA21=-0.0503;  WilB21=-69.6372  # Λ21 = exp(A21 + B21/T)

    def _vp(T, A, B, C, D, Tc, Pc):
        tau = 1.0 - T / Tc
        return Pc * ca.exp((Tc / T) * (A*tau + B*tau**1.5 + C*tau**2.5 + D*tau**5.0))

    PLV1 = _vp(T_K, VDI_A1, VDI_B1, VDI_C1, VDI_D1, Tc1, Pc1)
    PLV2 = _vp(T_K, VDI_A2, VDI_B2, VDI_C2, VDI_D2, Tc2, Pc2)

    L12 = ca.exp(WilA12 + WilB12 / T_K)
    L21 = ca.exp(WilA21 + WilB21 / T_K)
    d1 = x1 + L12 * x2
    d2 = L21 * x1 + x2
    ln_g1 = -ca.log(d1) + x2 * (L12 / d1 - L21 / d2)
    ln_g2 = -ca.log(d2) + x1 * (L21 / d2 - L12 / d1)

    gamma1 = ca.exp(ln_g1)
    gamma2 = ca.exp(ln_g2)

    Y = ca.vertcat(
        y1 * P - x1 * gamma1 * PLV1,
        y2 * P - x2 * gamma2 * PLV2,
    )

    resid_fn = ca.Function("wilson_resid", [X, p_sym], [Y])
    _CA_WILSON_RESID  = resid_fn
    _CA_WILSON_SOLVER = ca.rootfinder(
        "wilson_vle",
        "newton",
        resid_fn,
        {"abstol": 1e-8, "max_iter": 200, "error_on_fail": False},
    )

    return _CA_WILSON_SOLVER


def _ca_wilson_solve_batch(
    T_C_arr: np.ndarray,
    p_mbar_arr: np.ndarray,
    xN2_arr: np.ndarray,
) -> np.ndarray:
    """Batch Wilson VLE solve over arrays of temperature, pressure, and N2 mole fraction.

    Iterates the CasADi Newton rootfinder point-by-point, warm-starting each
    solve from the last accepted solution.  Columns where the solver diverges,
    produces non-finite iterates, or yields a residual above 1e-4 are set to
    NaN in the output.

    Parameters
    ----------
    T_C_arr : np.ndarray
        Temperature in degrees Celsius, shape ``(n,)``.
    p_mbar_arr : np.ndarray
        Total pressure in mbar, shape ``(n,)``.
    xN2_arr : np.ndarray
        Inert N2 mole fraction in the vapour phase, shape ``(n,)``.

    Returns
    -------
    np.ndarray
        Solution matrix of shape ``(4, n)`` with rows
        ``[x1, y1, wL1, wV1]`` — ethanol mole fraction in liquid (``x1``),
        ethanol mole fraction in vapour (``y1``), ethanol mass fraction in
        liquid (``wL1``), ethanol mass fraction in vapour (``wV1``).
        Columns with no valid VLE solution contain ``np.nan``.
    """
    solver = _get_ca_wilson_solver()
    n = len(T_C_arr)
    X_sol = np.full((4, n), np.nan)
    M1, M2 = 0.046069, 0.018015
    x0 = _SS_X0.copy()

    for i in range(n):
        xN2 = float(xN2_arr[i])
        p_i = np.array([float(T_C_arr[i]) + 273.15, float(p_mbar_arr[i]) / 1000.0, xN2])
        x_i = np.asarray(solver(ca.DM(x0), ca.DM(p_i))).flatten()
        if not np.all(np.isfinite(x_i)):
            continue
        r = np.array(_CA_WILSON_RESID(ca.DM(x_i), ca.DM(p_i))).flatten()
        if np.max(np.abs(r)) <= 1e-4:
            x1, y1 = x_i[0], x_i[1]
            if not (0.0 <= x1 <= 1.0 and 0.0 <= y1 <= 1.0 - xN2):
                continue
            x2 = 1.0 - x1
            y2 = 1.0 - y1 - xN2
            wL1 = x1 * M1 / (x1 * M1 + x2 * M2)
            wV1 = y1 * M1 / (y1 * M1 + y2 * M2) if y2 > 0.0 else np.nan
            X_sol[:, i] = [x1, y1, wL1, wV1]
            x0 = x_i  # warm-start next solve

    return X_sol


def _ss_mass_balance_w_L_D(w_L_C: np.ndarray, WI: np.ndarray,
                           ic_w_L_D: float = 0.0) -> np.ndarray:
    """Compute distillate product-tank composition via cumulative mass balance.

    Integrates the differential mass balance ``dM·w_D = dm · w_C`` to track
    the accumulated ethanol mass ``ME`` and the resulting tank composition
    ``w_D = ME / WI``.  When the tank weight is at or below 1 g the
    measurement is unreliable and the default purity 0.95 is returned.

    Parameters
    ----------
    w_L_C : np.ndarray
        Condenser outlet ethanol mass fraction at 1 Hz, shape ``(N,)``.
    WI : np.ndarray
        Distillate tank weight in grams at 1 Hz, shape ``(N,)``.
    ic_w_L_D : float, optional
        Known ethanol mass fraction in the tank at ``t = 0`` (from the
        experiment initial condition).  Default is ``0.0``.

    Returns
    -------
    np.ndarray
        Product-tank ethanol mass fraction, shape ``(N,)``.
    """
    N = len(WI)
    ME = ic_w_L_D * WI[0]   # initialise from known IC
    w_D = np.zeros(N)
    for t in range(N):
        if t > 0:
            ME += (WI[t] - WI[t - 1]) * w_L_C[t]
        w_D[t] = ME / WI[t] if WI[t] > 1.0 else 0.95
    return w_D


def precompute_softsensor(
    raw_df: pd.DataFrame,
    idx: list[int],
    ic_w_L_D: float = 0.0,
    x_N2_grid: np.ndarray = _SS_X_N2_GRID,
) -> np.ndarray:
    """Precompute distillate composition ``w_L_D_c1`` over an x_N2 grid.

    For each value in ``x_N2_grid`` the Wilson VLE is solved at every
    trajectory timestep using raw sensor readings (condenser vapour temperature
    TI17 and column pressure PIC02).  The resulting condenser-outlet composition
    is then forward-integrated via ``_ss_mass_balance_w_L_D`` on the 1 Hz
    tank-weight signal WI01.

    Parameters
    ----------
    raw_df : pd.DataFrame
        Raw sensor data at 1 Hz.  Required columns: ``TI17`` (condenser vapour
        temperature, °C), ``PIC02`` (column pressure, mbar), ``WI01`` (product
        tank weight, g).
    idx : list[int]
        Row indices into ``raw_df`` that correspond to each trajectory
        timestep, length ``n_traj``.
    ic_w_L_D : float, optional
        Initial ethanol mass fraction in the product tank at ``t = 0``.
        Default is ``0.0``.
    x_N2_grid : np.ndarray, optional
        Grid of N2 mole fractions at which to evaluate the softsensor.
        Defaults to ``_SS_X_N2_GRID`` (100 points, 0.043-0.15).

    Returns
    -------
    np.ndarray
        Distillate composition grid, shape ``(len(x_N2_grid), n_traj)``.
    """
    n_traj = len(idx)
    print(f"[precompute_softsensor] n_traj={n_traj}  G={len(x_N2_grid)}", flush=True)
    sub   = raw_df.iloc[idx].reset_index(drop=True)
    T_arr = sub["TI17"].values.astype(float)
    p_arr = sub["PIC02"].values.astype(float)

    WI_1hz = raw_df["WI01"].values.astype(float)
    t_idx  = np.array(idx, dtype=float)
    t_1hz  = np.arange(len(WI_1hz), dtype=float)

    G = len(x_N2_grid)

    # Loop: one Wilson solve per point
    T_flat   = np.tile(T_arr, G)             # (G*n_traj,)
    p_flat   = np.tile(p_arr, G)             # (G*n_traj,)
    xN2_flat = np.repeat(x_N2_grid, n_traj)  # (G*n_traj,)
    X_flat   = _ca_wilson_solve_batch(T_flat, p_flat, xN2_flat)  # (4, G*n_traj): [x1, y1, wL1, wV1]
    wV1_grid = X_flat[3, :].reshape(G, n_traj)  # wV1 = X[3]: vapor wf c1

    w_L_D_grid = np.empty((G, n_traj), dtype=float)
    for i in range(G):
        w_L_C_1hz = np.interp(t_1hz, t_idx, wV1_grid[i])
        w_L_D_1hz = _ss_mass_balance_w_L_D(w_L_C_1hz, WI_1hz, ic_w_L_D=ic_w_L_D)
        w_L_D_grid[i] = w_L_D_1hz[idx]

    return w_L_D_grid


def precompute_softsensor_wLB(
    raw_df: pd.DataFrame,
    idx: list[int],
    x_N2_grid: np.ndarray = _SS_X_N2_GRID,
) -> np.ndarray:
    """Precompute bottoms composition ``w_L_B_c1`` over an x_N2 grid.

    Solves the Wilson VLE at each trajectory timestep using the reboiler
    temperature (TI12) and bottoms pressure (PI01) from the raw sensor data
    to obtain the liquid-phase ethanol mass fraction.

    Parameters
    ----------
    raw_df : pd.DataFrame
        Raw sensor data at 1 Hz.  Required columns: ``TI12`` (reboiler
        temperature, °C), ``PI01`` (bottoms pressure, mbar).
    idx : list[int]
        Row indices into ``raw_df`` aligned to trajectory timesteps,
        length ``n_traj``.
    x_N2_grid : np.ndarray, optional
        Grid of N2 mole fractions.  Defaults to ``_SS_X_N2_GRID``.

    Returns
    -------
    np.ndarray
        Bottoms composition grid, shape ``(len(x_N2_grid), n_traj)``.
    """
    n_traj = len(idx)
    sub   = raw_df.iloc[idx].reset_index(drop=True)
    T_arr = sub["TI12"].values.astype(float)
    p_arr = sub["PI01"].values.astype(float)

    G = len(x_N2_grid)

    T_flat   = np.tile(T_arr, G)
    p_flat   = np.tile(p_arr, G)
    xN2_flat = np.repeat(x_N2_grid, n_traj)
    X_flat   = _ca_wilson_solve_batch(T_flat, p_flat, xN2_flat)
    w_L_B_grid = X_flat[2, :].reshape(G, n_traj)   # wL1 = X[2]: liquid wf c1

    return w_L_B_grid


def _load_or_compute_softsensor_grids(
    raw_df: pd.DataFrame,
    idx: list[int],
    ic_w_L_D: float,
    x_N2_grid: np.ndarray,
    cache_path: Path,
) -> tuple[np.ndarray, np.ndarray]:
    """Return cached softsensor grids, recomputing if the cache is stale or missing.

    The cache is stored as a pickle at ``cache_path`` and is considered valid
    when ``idx``, ``x_N2_grid``, and ``ic_w_L_D`` all match the cached values
    and the arrays have the expected shape.  Any mismatch or load failure
    triggers a full recompute followed by a cache write.

    Parameters
    ----------
    raw_df : pd.DataFrame
        Raw 1 Hz sensor data passed through to ``precompute_softsensor*``.
    idx : list[int]
        Trajectory timestep indices into ``raw_df``.
    ic_w_L_D : float
        Initial product-tank ethanol mass fraction (cache key).
    x_N2_grid : np.ndarray
        N2 mole-fraction grid, shape ``(G,)`` (cache key).
    cache_path : Path
        Path to the pickle file used for caching.

    Returns
    -------
    w_L_D_grid : np.ndarray
        Distillate composition grid, shape ``(G, n_traj)``.
    w_L_B_grid : np.ndarray
        Bottoms composition grid, shape ``(G, n_traj)``.
    """
    n_traj = len(idx)
    print(f"[softsensor_cache] checking {cache_path}  exists={cache_path.exists()}", flush=True)
    if cache_path.exists():
        try:
            with open(cache_path, "rb") as fh:
                cache = pickle.load(fh)
            if (
                cache.get("idx") == idx
                and np.allclose(cache["x_N2_grid"], x_N2_grid)
                and np.isclose(cache["ic_w_L_D"], ic_w_L_D)
                and cache["w_L_D"].shape == (len(x_N2_grid), n_traj)
                and cache["w_L_B"].shape == (len(x_N2_grid), n_traj)
            ):
                print(f"[softsensor_cache] HIT {cache_path}", flush=True)
                logger.info("Softsensor cache hit: %s", cache_path)
                return cache["w_L_D"], cache["w_L_B"]
            logger.info("Softsensor cache stale, recomputing …")
        except Exception as exc:  # noqa: BLE001
            logger.warning("Softsensor cache load failed (%s), recomputing …", exc)

    w_L_D = precompute_softsensor(raw_df, idx, ic_w_L_D=ic_w_L_D, x_N2_grid=x_N2_grid)
    w_L_B = precompute_softsensor_wLB(raw_df, idx, x_N2_grid=x_N2_grid)

    cache = {"idx": idx, "x_N2_grid": x_N2_grid, "ic_w_L_D": ic_w_L_D,
             "w_L_D": w_L_D, "w_L_B": w_L_B}
    with open(cache_path, "wb") as fh:
        pickle.dump(cache, fh)
    logger.info("Softsensor cache saved: %s", cache_path)

    return w_L_D, w_L_B


def _recalc_exp_states(exp: "Experiment", x_N2: float) -> np.ndarray:
    """Return ``exp_states`` with compositions recalculated for a given ``x_N2``.

    Interpolates the precomputed softsensor grids stored in ``exp`` at the
    requested ``x_N2`` value and overwrites columns 2 (``w_L_D_c1``) and 3
    (``w_L_B_c1``) in a copy of ``exp.exp_states``.  The remaining columns
    (LI, WI, T_tr9) are unchanged.

    Parameters
    ----------
    exp : Experiment
        Experiment whose ``ss_w_L_D`` / ``ss_w_L_B`` grids are used.
    x_N2 : float
        N2 mole fraction at which to interpolate the softsensor grids.

    Returns
    -------
    np.ndarray
        Updated experimental state matrix, shape ``(N, 5)``.
    """
    states = exp.exp_states.copy()
    N = len(exp.time)
    w_L_D = np.array([np.interp(x_N2, exp.ss_x_N2_grid, exp.ss_w_L_D[:, t]) for t in range(N)])
    w_L_B = np.array([np.interp(x_N2, exp.ss_x_N2_grid, exp.ss_w_L_B[:, t]) for t in range(N)])
    states[:, 2] = w_L_D   # w_L_D_c1
    states[:, 3] = w_L_B   # w_L_B_c1
    return states


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class Experiment:
    """Parsed experimental trajectory ready for parameter estimation.

    Attributes
    ----------
    name : str
        Experiment identifier derived from the directory name (e.g.
        ``"trained_agent_1IC_260414_1"``).
    ic_LI : float
        Initial liquid level indicator (%) at ``t = 0``.
    ic_w_L_B_c1 : float
        Initial ethanol mass fraction in the bottoms stream at ``t = 0``.
    U : np.ndarray
        Control input trajectory, shape ``(N-1, 2)``.  Columns are
        ``rr_PLS`` (reflux ratio) and ``Q_PLS_R`` (reboiler duty, kW).
    exp_states : np.ndarray
        Measured state trajectory, shape ``(N, 5)``.  Columns in order:
        LI, WI (g), w_L_D_c1, w_L_B_c1, T_tr9 (K).
    time : np.ndarray
        Absolute time stamps in seconds, shape ``(N,)``.
    dt_report : float
        Uniform sampling interval in seconds.
    ss_x_N2_grid : np.ndarray
        N2 mole-fraction grid used for the softsensor, shape ``(G,)``.
    ss_w_L_D : np.ndarray
        Precomputed distillate ethanol mass fraction on the grid,
        shape ``(G, N)``.
    ss_w_L_B : np.ndarray
        Precomputed bottoms ethanol mass fraction on the grid,
        shape ``(G, N)``.
    """

    name: str
    ic_LI: float
    ic_w_L_B_c1: float
    U: np.ndarray           # shape (N-1, 2): rr_PLS, Q_PLS_R
    exp_states: np.ndarray  # shape (N, 5): LI, WI, w_L_D_c1, w_L_B_c1, T_tr9
    time: np.ndarray        # shape (N,), seconds
    dt_report: float        # sampling interval in seconds
    ss_x_N2_grid: np.ndarray  # shape (G,) — x_N2 values for softsensor grid
    ss_w_L_D: np.ndarray      # shape (G, N) — precomputed w_L_D_c1 per grid point
    ss_w_L_B: np.ndarray      # shape (G, N) — precomputed w_L_B_c1 per grid point


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


def load_experiment(path: str | Path) -> Experiment:
    """Load a single ``trajectories.pkl`` file into an :class:`Experiment`.

    Validates uniform time spacing (tolerance ``_DT_TOL`` seconds), loads
    ``rawdata.pkl`` from the same directory to compute the softsensor grids,
    and returns a fully populated :class:`Experiment` with cached or freshly
    computed ``ss_w_L_D`` / ``ss_w_L_B`` grids.

    Parameters
    ----------
    path : str or Path
        Path to ``trajectories.pkl``.  ``rawdata.pkl`` must exist in the
        same parent directory.

    Returns
    -------
    Experiment
        Parsed experiment.  ``U`` has shape ``(N-1, 2)`` — one fewer row
        than the state trajectory, as required by ``PE_sim``.

    Raises
    ------
    ValueError
        If the trajectory has fewer than 2 rows or non-uniform time spacing.
    FileNotFoundError
        If ``rawdata.pkl`` is missing from the experiment directory.
    """
    path = Path(path)
    with open(path, "rb") as fh:
        data = pickle.load(fh)

    x = np.asarray(data._x, dtype=float)   # (N, 8)
    u = np.asarray(data._u, dtype=float)   # (N, 2)
    t = np.asarray(data._time, dtype=float).flatten()  # (N,)

    n = x.shape[0]
    if n < 2:
        raise ValueError(f"{path.name}: need N >= 2 rows, got {n}")

    dts = np.diff(t)
    if not np.allclose(dts, dts[0], atol=_DT_TOL):
        raise ValueError(
            f"{path.name}: non-uniform _time spacing (range "
            f"{dts.min():.1f}-{dts.max():.1f} s)"
        )
    dt = float(np.round(dts[0]))

    raw_path = path.parent / "rawdata.pkl"
    if not raw_path.exists():
        raise FileNotFoundError(f"rawdata.pkl required but missing: {raw_path}")
    raw_df = pd.read_pickle(raw_path)
    n_raw = len(raw_df)
    dt_int = int(np.round(dt))
    # Build idx: regular steps for first n-1 points, last raw row for final point.
    idx = [i * dt_int for i in range(n - 1)] + [n_raw - 1]
    ic_w_L_D = float(x[0, 2])   # w_L_D_c1 at t=0 from trajectories
    cache_path = path.parent / "softsensor_grid.pkl"
    logger.info("Loading/computing softsensor grids for %s …", path.parts[-3])
    ss_w_L_D, ss_w_L_B = _load_or_compute_softsensor_grids(
        raw_df, idx=idx, ic_w_L_D=ic_w_L_D,
        x_N2_grid=_SS_X_N2_GRID, cache_path=cache_path,
    )

    return Experiment(
        name=path.parts[-3],
        ic_LI=float(x[0, 0]),
        ic_w_L_B_c1=float(x[0, 3]),
        U=u[: n - 1, :],
        exp_states=x[:, EXP_STATE_COLS],
        time=t,
        dt_report=dt,
        ss_x_N2_grid=_SS_X_N2_GRID.copy(),
        ss_w_L_D=ss_w_L_D,
        ss_w_L_B=ss_w_L_B,
    )


def load_all_experiments(
    root: str | Path,
    glob_pattern: str = "*/results/trajectories.pkl"
) -> list[Experiment]:
    """Load all experiments from a fixed experiment list.

    .. note::
        The ``glob_pattern`` / ``trained_only`` parameters are currently
        overridden by a hardcoded experiment list that includes both trained
        and untrained agent runs.  Pass ``trained_only=False`` (as the CLI
        plot step does) to load all experiments from that fixed list.

    Parameters
    ----------
    root : str or Path
        Root directory (kept for interface compatibility; not used by the
        hardcoded path list).
    glob_pattern : str, optional
        Glob pattern relative to ``root`` (unused while hardcoded list is
        active).
    trained_only : bool, optional
        Filter flag (unused while hardcoded list is active).

    Returns
    -------
    list[Experiment]
        Successfully loaded experiments.  Entries that fail to parse emit a
        warning and are skipped.

    Raises
    ------
    FileNotFoundError
        If the hardcoded list yields no loadable pkl files.
    """
    root = Path(root)
    paths = [p for p in root.glob(glob_pattern)]

    if not paths:
        raise FileNotFoundError(f"No pkl files matching {root / glob_pattern}")

    experiments: list[Experiment] = []
    for p in paths:
        try:
            exp = load_experiment(p)
            logger.info(
                "Loaded %-40s  N=%d, dt=%.0f s", exp.name, len(exp.time), exp.dt_report
            )
            experiments.append(exp)
        except (ValueError, AttributeError, KeyError, FileNotFoundError) as exc:
            warnings.warn(f"Skipping {p}: {exc}", stacklevel=1)

    return experiments


# ---------------------------------------------------------------------------
# Simulation
# ---------------------------------------------------------------------------


def simulate_experiment(
    E_murphree: float,
    rr_err: float,
    x_N2: float,
    h_weir: float,
    exp: Experiment,
) -> np.ndarray | None:
    """Simulate one experiment and return the EMA-smoothed output trajectory.

    Calls ``PE_sim`` with the supplied parameters, then applies an exponential
    moving average (alpha = 0.4, initialised at the experimental IC) to match
    the NARX environment warm-start.  ``h_tot`` and ``kappa`` are fixed at the
    module-level constants ``_FIXED_H_TOT`` / ``_FIXED_KAPPA``.

    If the first ``PE_sim`` call raises an exception, a second attempt is made
    with the relaxed integrator.  Both failures are logged at WARNING level.

    Parameters
    ----------
    E_murphree : float
        Murphree tray efficiency.
    rr_err : float
        Reflux-ratio error (additive correction to the nominal rr).
    x_N2 : float
        N2 mole fraction (physical units, not scaled).
    h_weir : float
        Weir height in metres.
    exp : Experiment
        Experiment providing initial conditions, input trajectory, and
        softsensor grids.

    Returns
    -------
    np.ndarray or None
        EMA-smoothed output trajectory, shape ``(N, 5)`` with columns
        per ``WLS_OUTPUTS``, or ``None`` if both simulation attempts fail or
        ``x_N2`` is outside the two-phase region for this experiment.
    """
    exp_states = _recalc_exp_states(exp, x_N2)
    if np.any(np.isnan(exp_states)):
        return None  # x_N2 outside two-phase region for this experiment

    for attempt in range(2):
        try:
            result = PE_sim(
                E_murphree=E_murphree,
                rr_err=rr_err,
                x_N2=x_N2,
                h_tot=_FIXED_H_TOT,
                h_weir=h_weir,
                kappa=_FIXED_KAPPA,
                LI=exp.ic_LI,
                w_L_B_c1=exp.ic_w_L_B_c1,
                U=exp.U,
                outputs=WLS_OUTPUTS,
                dt_report=exp.dt_report,
                relaxed=(attempt > 0),
            )
            y = result["y"]  # shape (N, 5), raw states
            # EMA matching NARX (alpha=0.4); init at exp IC to match env warmstart
            alpha = 0.4
            y_ema = np.empty_like(y)
            y_ema[0] = exp_states[0]
            for t in range(1, len(y)):
                y_ema[t] = (1 - alpha) * y_ema[t - 1] + alpha * y[t]
            return y_ema
        except Exception as exc:  # noqa: BLE001
            if attempt == 0:
                logger.warning(
                    "PE_sim attempt 1 failed [%s] E_murphree=%.4f rr_err=%.4f x_N2=%.4f h_weir=%.4f: %s — retrying",
                    exp.name, E_murphree, rr_err, x_N2, h_weir, exc,
                )
            else:
                logger.warning(
                    "PE_sim attempt 2 failed [%s] E_murphree=%.4f rr_err=%.4f x_N2=%.4f h_weir=%.4f: %s",
                    exp.name, E_murphree, rr_err, x_N2, h_weir, exc,
                )
    return None


# ---------------------------------------------------------------------------
# WLS
# ---------------------------------------------------------------------------


def wls_single(
    sim_states: np.ndarray,
    exp_states: np.ndarray,
    weights_norm: np.ndarray,
) -> dict[str, float]:
    """Compute the weighted least-squares criterion for one experiment.

    Parameters
    ----------
    sim_states : np.ndarray
        Simulated output trajectory, shape ``(N, n_states)``.
    exp_states : np.ndarray
        Experimental state trajectory, shape ``(N, n_states)``.
    weights_norm : np.ndarray
        Per-state weights, shape ``(n_states,)``.  Typically
        ``w_raw / (n_exp * N_t)`` so contributions are normalised across
        experiments and time steps.

    Returns
    -------
    dict[str, float]
        Per-state WLS contributions keyed by ``WLS_STATE_NAMES``, plus
        ``"total"`` for the sum.  Contribution formula:
        ``weights_norm[i] * sum_t (sim[t, i] - exp[t, i])^2``.
    """
    residuals = sim_states - exp_states  # (N, 4)
    breakdown: dict[str, float] = {}
    total = 0.0
    for i, name in enumerate(WLS_STATE_NAMES):
        val = float(weights_norm[i] * np.sum(residuals[:, i] ** 2))
        breakdown[name] = val
        total += val
    breakdown["total"] = total
    return breakdown


def wls_total(
    E_murphree: float,
    rr_err: float,
    x_N2: float,
    h_weir: float,
    experiments: list[Experiment],
    weights_norm: np.ndarray,
    penalty: float = 1e6,
    n_jobs: int = -1,
    failures_log: Path | None = None,
) -> tuple[float, list[dict[str, float] | None]]:
    """Evaluate the aggregate WLS criterion across all experiments.

    Runs ``simulate_experiment`` for every experiment in parallel (joblib loky
    backend) when ``n_jobs != 1`` and joblib is available.  Failed simulations
    contribute ``penalty`` to the total WLS.  ``h_tot`` and ``kappa`` are
    fixed at ``_FIXED_H_TOT`` / ``_FIXED_KAPPA``.

    Parameters
    ----------
    E_murphree : float
        Murphree tray efficiency.
    rr_err : float
        Reflux-ratio error.
    x_N2 : float
        N2 mole fraction (physical units).
    h_weir : float
        Weir height in metres.
    experiments : list[Experiment]
        Experiments to evaluate.
    weights_norm : np.ndarray
        Pre-normalised per-state weights, shape ``(n_states,)``.
    penalty : float, optional
        WLS penalty added for each failed simulation.  Default ``1e6``.
    n_jobs : int, optional
        Joblib worker count.  ``-1`` uses all cores; ``1`` disables
        parallelism.  Default ``-1``.
    failures_log : Path or None, optional
        If provided, failed parameter combinations are appended to this file.

    Returns
    -------
    total_wls : float
        Sum of per-experiment WLS contributions (penalties included).
    breakdowns : list[dict[str, float] or None]
        Per-experiment WLS breakdown dicts (``None`` for failed simulations),
        in the same order as ``experiments``.
    """
    if _JOBLIB_AVAILABLE and n_jobs != 1:
        sim_results: list[np.ndarray | None] = Parallel(
            n_jobs=n_jobs, backend="loky"
        )(delayed(simulate_experiment)(E_murphree, rr_err, x_N2, h_weir, exp) for exp in experiments)
    else:
        sim_results = [simulate_experiment(E_murphree, rr_err, x_N2, h_weir, exp) for exp in experiments]

    total_wls = 0.0
    breakdowns: list[dict[str, float] | None] = []
    for exp, y_sim in zip(experiments, sim_results):
        if y_sim is None:
            total_wls += penalty
            breakdowns.append(None)
            if failures_log is not None:
                try:
                    with open(failures_log, "a") as _fh:
                        _fh.write(
                            f"exp={exp.name}"
                            f" E_murphree={repr(E_murphree)}"
                            f" rr_err={repr(rr_err)}"
                            f" x_N2={repr(x_N2)}"
                            f" h_weir={repr(h_weir)}"
                            f" h_tot={repr(_FIXED_H_TOT)}"
                            f" kappa={repr(_FIXED_KAPPA)}\n"
                        )
                except OSError:
                    pass
        else:
            w_e = weights_norm / len(exp.time)
            exp_states = _recalc_exp_states(exp, x_N2)
            bd = wls_single(y_sim, exp_states, w_e)
            total_wls += bd["total"]
            breakdowns.append(bd)

    return total_wls, breakdowns


# ---------------------------------------------------------------------------
# Objective closure
# ---------------------------------------------------------------------------


def make_objective(
    experiments: list[Experiment],
    weights_norm: np.ndarray,
    penalty: float,
    n_jobs: int,
    failures_log: Path | None = None,
) -> tuple[Callable[..., float], list[dict[str, Any]]]:
    """Create the Bayesian Optimization objective closure and a shared probe-history list.

    The returned ``objective`` accepts parameters in the BO-scaled space
    (``x_N2`` and ``h_weir`` multiplied by 10) and returns ``-WLS`` so that
    ``BayesianOptimization`` can maximise the negative WLS.  Each
    call appends a record to ``all_probes``.

    Parameters
    ----------
    experiments : list[Experiment]
        Experiments passed through to ``wls_total``.
    weights_norm : np.ndarray
        Pre-normalised per-state weights.
    penalty : float
        WLS penalty per failed simulation.
    n_jobs : int
        Joblib worker count passed through to ``wls_total``.
    failures_log : Path or None, optional
        Failure log path passed through to ``wls_total``.

    Returns
    -------
    objective : Callable
        Closure ``objective(E_murphree, rr_err, x_N2, h_weir) → float``
        returning ``-WLS``.
    all_probes : list[dict[str, Any]]
        Mutable list that grows with each ``objective`` call.  Each entry
        contains keys ``iter``, ``E_murphree``, ``rr_err``, ``x_N2``,
        ``h_weir``, ``wls``, ``n_failed``.
    """
    all_probes: list[dict[str, Any]] = []

    def objective(E_murphree: float, rr_err: float, x_N2: float,
                  h_weir: float) -> float:
        x_N2_phys  = x_N2  / 10.0
        h_weir_phys = h_weir / 10.0
        t0 = time.perf_counter()
        wls, breakdowns = wls_total(E_murphree, rr_err, x_N2_phys, h_weir_phys, experiments, weights_norm, penalty,
                                    n_jobs, failures_log=failures_log)
        elapsed = time.perf_counter() - t0
        n_failed = sum(1 for bd in breakdowns if bd is None)
        all_probes.append({
            "iter": len(all_probes),
            "E_murphree": E_murphree,
            "rr_err": rr_err,
            "x_N2": x_N2_phys,
            "h_weir": h_weir_phys,
            "wls": wls,
            "n_failed": n_failed,
        })
        logger.info(
            "Eval %3d | E_murphree=%.4f  rr_err=%.4f  x_N2=%.4f  h_weir=%.4f | WLS=%.6g  failed=%d/%d (%.1f s)",
            len(all_probes), E_murphree, rr_err, x_N2_phys, h_weir_phys, wls, n_failed, len(experiments), elapsed,
        )
        return -wls

    return objective, all_probes


# ---------------------------------------------------------------------------
# Checkpointing
# ---------------------------------------------------------------------------


def _save_checkpoint(all_probes: list[dict[str, Any]], out_dir: Path) -> None:
    """Write current probe history to ``probes.csv`` and ``bo_state.json``.

    ``probes.csv`` contains one row per objective evaluation with columns
    ``iter``, ``neg_target``, ``wls``, ``n_failed``, and the four parameter
    values.  ``bo_state.json`` stores the same data in a format suitable for
    replaying into a ``BayesianOptimization`` instance.  No-ops when
    ``all_probes`` is empty.

    Parameters
    ----------
    all_probes : list[dict[str, Any]]
        Probe history accumulated by the objective closure.
    out_dir : Path
        Directory where ``probes.csv`` and ``bo_state.json`` are written.
    """
    if not all_probes:
        return

    rows = [
        {"iter": p["iter"], "neg_target": -p["wls"], "wls": p["wls"],
         "n_failed": p["n_failed"], "E_murphree": p["E_murphree"], "rr_err": p["rr_err"],
         "x_N2": p["x_N2"], "h_weir": p["h_weir"]}
        for p in all_probes
    ]
    with open(out_dir / "probes.csv", "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    bo_state = [
        {"iter": p["iter"],
         "params": {"E_murphree": p["E_murphree"], "rr_err": p["rr_err"],
                    "x_N2": p["x_N2"], "h_weir": p["h_weir"]},
         "target": -p["wls"], "n_failed": p["n_failed"]}
        for p in all_probes
    ]
    with open(out_dir / "bo_state.json", "w") as fh:
        json.dump(bo_state, fh, indent=2)


# ---------------------------------------------------------------------------
# Results saving
# ---------------------------------------------------------------------------


def save_results(
    all_probes: list[dict[str, Any]],
    experiments: list[Experiment],
    weights_norm: np.ndarray,
    config: dict[str, Any],
    out_dir: Path,
    penalty: float,
    n_jobs: int,
) -> None:
    """Save all parameter-estimation artifacts to ``out_dir``.

    Writes the following files:

    - ``config.json`` — run configuration (bounds, weights, and execution settings).
    - ``probes.csv`` / ``bo_state.json`` — full probe history (via
      ``_save_checkpoint``).
    - ``best.json`` — best parameter set and WLS found.
    - ``breakdown.json`` — per-experiment per-state WLS at the best parameters.

    Parameters
    ----------
    all_probes : list[dict[str, Any]]
        Complete probe history from the objective closure.
    experiments : list[Experiment]
        Experiments used during optimisation.
    weights_norm : np.ndarray
        Per-state normalised weights used during optimisation.
    config : dict[str, Any]
        Run configuration dict to serialise as ``config.json``.
    out_dir : Path
        Output directory (must exist).
    penalty : float
        WLS penalty used for the breakdown re-evaluation.
    n_jobs : int
        Joblib workers for the breakdown re-evaluation (sequential with
        ``n_jobs=1`` to avoid nested pools).
    """
    print("save_results: writing config.json...", flush=True)
    with open(out_dir / "config.json", "w") as fh:
        json.dump(config, fh, indent=2)

    print("save_results: checkpointing probes...", flush=True)
    _save_checkpoint(all_probes, out_dir)

    print("save_results: finding best probe...", flush=True)
    best_probe = min(all_probes, key=lambda p: p["wls"])
    best_E     = best_probe["E_murphree"]
    best_rr    = best_probe["rr_err"]
    best_xN2   = best_probe["x_N2"]
    best_h_weir = best_probe["h_weir"]
    best_wls   = best_probe["wls"]
    best_iter  = best_probe["iter"]

    print("save_results: writing best.json...", flush=True)
    with open(out_dir / "best.json", "w") as fh:
        json.dump(
            {
                "E_murphree": best_E,
                "rr_err": best_rr,
                "x_N2": best_xN2,
                "h_weir": best_h_weir,
                "h_tot": _FIXED_H_TOT,
                "kappa": _FIXED_KAPPA,
                "wls": best_wls,
                "neg_target": -best_wls,
                "iteration": best_iter,
            },
            fh,
            indent=2,
        )
    logger.info(
        "Best params: E_murphree=%.4f  rr_err=%.4f  x_N2=%.4f  h_weir=%.4f  WLS=%.6g  (iter %d)",
        best_E, best_rr, best_xN2, best_h_weir, best_wls, best_iter,
    )

    print("save_results: computing breakdown (n_jobs=1)...", flush=True)
    logger.info("Computing breakdown at best params...")
    _, breakdowns = wls_total(best_E, best_rr, best_xN2, best_h_weir, experiments, weights_norm, penalty, n_jobs=1)
    bd_out = {
        exp.name: (bd if bd is not None else "failed")
        for exp, bd in zip(experiments, breakdowns)
    }
    with open(out_dir / "breakdown.json", "w") as fh:
        json.dump(bd_out, fh, indent=2)
    logger.info("breakdown.json saved.")


# ---------------------------------------------------------------------------
# Periodic figure snapshots
# ---------------------------------------------------------------------------


def _save_periodic_figs(
    all_probes: list[dict[str, Any]],
    experiments: list[Experiment],
    out_dir: Path,
    every: int = 500,
) -> None:
    """Save trajectory fit plots for the best-so-far parameters every ``every`` evaluations.

    No-ops when ``len(all_probes) % every != 0`` or ``all_probes`` is empty.
    Figures are written to ``out_dir/figs_periodic/iter_NNNNNN/``.

    Parameters
    ----------
    all_probes : list[dict[str, Any]]
        Current probe history.
    experiments : list[Experiment]
        Experiments to plot.
    out_dir : Path
        Base output directory.
    every : int, optional
        Snapshot frequency in number of objective evaluations.  Default 500.
    """
    n = len(all_probes)
    if n == 0 or n % every != 0:
        return
    best = min(all_probes, key=lambda p: p["wls"])
    snap_dir = out_dir / "figs_periodic" / f"iter_{n:06d}"
    snap_dir.mkdir(parents=True, exist_ok=True)
    for exp in experiments:
        try:
            plot_fit(
                E_murphree=best["E_murphree"],
                rr_err=best["rr_err"],
                x_N2=best["x_N2"],
                h_tot=_FIXED_H_TOT,
                h_weir=best["h_weir"],
                kappa=_FIXED_KAPPA,
                exp=exp,
                out_path=snap_dir / f"fit_{exp.name}.png",
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("Periodic fig failed [%s] iter=%d: %s", exp.name, n, exc)
    logger.info("Periodic figs saved: %s", snap_dir)


# ---------------------------------------------------------------------------
# Main PE runner
# ---------------------------------------------------------------------------


def run_pe(
    data_root: str | Path,
    *,
    E_murphree_bounds: tuple[float, float] = (0.3, 0.7),
    rr_err_bounds: tuple[float, float] = (-0.20, -0.1),
    x_N2_bounds: tuple[float, float] = (0.043, 0.10),
    h_weir_bounds: tuple[float, float] = (0.005, 0.05),
    weights: dict[str, float] | None = None,
    noise_std: dict[str, float] | None = None,
    init_points: int = 5,
    n_iter: int = 25,
    random_state: int = 42,
    penalty: float = 1e7,
    out_dir: str | Path | None = None,
    n_jobs: int = -1,
) -> dict[str, Any]:
    """Run full parameter estimation via Bayesian Optimization.

    Parameters
    ----------
    data_root:
        Root directory containing experiment folders with trajectories.pkl.
    E_murphree_bounds:
        (min, max) search bounds for Murphree efficiency.
    rr_err_bounds:
        (min, max) search bounds for reflux-ratio error.
    noise_std:
        Known sensor noise std devs sigma keyed by WLS_STATE_NAMES. When provided,
        weights are computed as w_i = 1/sigma ** 2_i. Takes precedence over weights.
        Use DEFAULT_NOISE_STD as template.
    weights:
        Manual per-state WLS weights. Used only when noise_var is None.
        Defaults to 1.0 each.
    init_points:
        Random exploration probes before Bayesian Optimization starts.
    n_iter:
        Number of Bayesian Optimization iterations after random probes.
    random_state:
        RNG seed for reproducibility.
    penalty:
        WLS contribution applied when a simulation fails.
    out_dir:
        Output directory. Defaults to ./results/pe_<timestamp>/.
    n_jobs:
        Joblib parallel workers for experiment simulations (-1 = all cores).

    Returns
    -------
    dict with keys: best_E_murphree, best_rr_err, best_wls, out_dir.
    """
    if out_dir is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_dir = Path("results") / f"pe_{ts}"
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(out_dir / "pe.log"),
        ],
        force=True,
    )

    experiments = load_all_experiments(data_root)
    logger.info("Loaded %d experiments from %s", len(experiments), data_root)
    if not experiments:
        raise RuntimeError(f"No experiments loaded from {data_root}")

    # Compute w_i: from noise_std (1/sigma ** 2_i) if provided, else manual weights.
    # Final weights_norm divided by N_exp; per-experiment N_t applied in wls_total.
    if noise_std is not None:
        ns = {**DEFAULT_NOISE_STD, **noise_std}
        w_raw = np.array([1.0 / ns[name] ** 2 for name in WLS_STATE_NAMES])
        w_dict = {name: 1.0 / ns[name] ** 2 for name in WLS_STATE_NAMES}
        logger.info("Weights from noise_std (1/sigma ** 2): %s", {n: f"{w_raw[i]:.4g}" for i, n in enumerate(WLS_STATE_NAMES)})
    else:
        w_dict = {**DEFAULT_WEIGHTS, **(weights or {})}
        w_raw = np.array([w_dict[name] for name in WLS_STATE_NAMES])
        logger.info("Weights (manual): %s", w_dict)
    n_exp = len(experiments)
    weights_norm = w_raw / n_exp
    logger.info("Divided by N_exp=%d; per-experiment N_t applied in wls_total", n_exp)

    failures_log = out_dir / "failures.log"
    objective, all_probes = make_objective(experiments, weights_norm, penalty, n_jobs, failures_log=failures_log)

    pbounds = {
        "E_murphree": E_murphree_bounds, "rr_err": rr_err_bounds,
        "x_N2": (x_N2_bounds[0] * 10, x_N2_bounds[1] * 10),
        "h_weir": (h_weir_bounds[0] * 10, h_weir_bounds[1] * 10),
    }
    config: dict[str, Any] = {
        "pbounds": {"E_murphree": list(E_murphree_bounds), "rr_err": list(rr_err_bounds),
                    "x_N2": list(x_N2_bounds), "h_weir": list(h_weir_bounds)},
        "fixed": {"h_tot": _FIXED_H_TOT, "kappa": _FIXED_KAPPA},
        "weights": w_dict,
        "weights_norm": dict(zip(WLS_STATE_NAMES, weights_norm.tolist())),
        "init_points": init_points,
        "n_iter": n_iter,
        "random_state": random_state,
        "penalty": penalty,
        "n_experiments": n_exp,
        "experiments": [exp.name for exp in experiments],
        "n_t_per_experiment": {exp.name: len(exp.time) for exp in experiments},
    }

    optimizer = BayesianOptimization(
        f=objective,
        pbounds=pbounds,
        random_state=random_state,
        verbose=2,
        allow_duplicate_points=False,
    )
    logger.info("Running %d random probes...", init_points)
    optimizer.maximize(init_points=init_points, n_iter=0)
    _save_checkpoint(all_probes, out_dir)
    _save_periodic_figs(all_probes, experiments, out_dir)

    logger.info("Running %d BO iterations...", n_iter)
    for i in range(n_iter):
        next_point = optimizer.suggest()
        objective(**next_point)
        optimizer.register(params=next_point, target=all_probes[-1]["wls"] * -1)
        logger.info("BO iter %d/%d complete", i + 1, n_iter)
        _save_checkpoint(all_probes, out_dir)
        _save_periodic_figs(all_probes, experiments, out_dir)

    save_results(all_probes, experiments, weights_norm, config, out_dir, penalty, n_jobs)

    best_probe = min(all_probes, key=lambda p: p["wls"])
    return {
        "best_E_murphree": best_probe["E_murphree"],
        "best_rr_err": best_probe["rr_err"],
        "best_x_N2": best_probe["x_N2"],
        "best_h_weir": best_probe["h_weir"],
        "best_h_tot": _FIXED_H_TOT,
        "best_kappa": _FIXED_KAPPA,
        "best_wls": best_probe["wls"],
        "out_dir": str(out_dir),
    }


# ---------------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------------


def plot_fit(
    E_murphree: float,
    rr_err: float,
    x_N2: float,
    h_tot: float,
    h_weir: float,
    kappa: float,
    exp: Experiment,
    out_path: str | Path | None = None,
    noise_std: dict[str, float] | None = None,
) -> None:
    """Plot control inputs and simulated vs experimental state trajectories.

    Produces a 4 x 2 subplot figure (single journal column, 8.4 cm wide,
    8 pt font):

    - Row 0: control inputs ``rr_PLS`` and ``Q_PLS_R`` (step plot).
    - Rows 1-3: five states ``LI``, ``WI``, ``w_L_D_c1``, ``w_L_B_c1``,
      ``T_tr9`` — simulation as a solid line (RGB 0/175/240) and experimental
      measurements as markers with ±1sigma error bars (RGB 210/0/30).

    The last panel (row 3, col 1) is hidden.

    Parameters
    ----------
    E_murphree : float
        Murphree tray efficiency used for the simulation.
    rr_err : float
        Reflux-ratio error used for the simulation.
    x_N2 : float
        N2 mole fraction used for the simulation.
    h_tot : float
        Total tray holdup (passed to ``simulate_experiment`` via module constants).
    h_weir : float
        Weir height in metres.
    kappa : float
        Heat-loss coefficient (passed to ``simulate_experiment`` via module constants).
    exp : Experiment
        Experiment providing inputs, measured states, and softsensor grids.
    out_path : str or Path or None, optional
        If provided, the figure is saved at 300 dpi and the plot window is
        not shown.  If ``None``, ``plt.show()`` is called.
    noise_std : dict[str, float] or None, optional
        Sensor noise standard deviations keyed by ``WLS_STATE_NAMES``.
        Merged with ``DEFAULT_NOISE_STD``; used for the ±1sigma error bars.
    """
    import matplotlib as mpl
    import matplotlib.pyplot as plt

    mpl.rcParams.update({"font.size": 8})

    ns = {**DEFAULT_NOISE_STD, **(noise_std or {})}
    sigmas = np.array([ns[name] for name in WLS_STATE_NAMES])

    y_sim = simulate_experiment(E_murphree, rr_err, x_N2, h_weir, exp)
    if y_sim is None:
        raise RuntimeError(f"Simulation failed for experiment {exp.name}")
    exp_states = _recalc_exp_states(exp, x_N2)

    t_min = exp.time / 60.0                      # state time axis (N,)
    t_u_min = exp.time[: len(exp.U)] / 60.0     # control time axis (N-1,)

    col_sim = np.array([0, 175, 240]) / 255.0
    col_exp = np.array([210, 0, 30]) / 255.0
    col_u = np.array([140, 180, 15]) / 255.0

    ctrl_labels = ["rr$_{PLS}$", "Q$_{PLS}$ (kW)"]
    state_labels = ["LI", "WI (g)", r"$w_{L,D,c1}$", r"$w_{L,B,c1}$", r"$T_{tr9}$ (K)"]

    fig, axes = plt.subplots(4, 2, figsize=(8.4 / 2.54, 16.0 / 2.54))
    axes_flat = axes.flatten()

    # Row 0: controls (experimental only — same U fed to sim)
    for j in range(2):
        ax = axes_flat[j]
        ax.step(t_u_min, exp.U[:, j], color=col_u, lw=0.8, where="post")
        ax.set_ylabel(ctrl_labels[j], fontsize=8)
        ax.tick_params(labelsize=8)
        if j == 0:
            ax.set_xlabel("Time (min)", fontsize=8)

    # Rows 1-3: states — sim line + exp markers with ±1sigma error bars
    for i in range(len(WLS_STATE_NAMES)):
        ax = axes_flat[i + 2]
        ax.plot(t_min, y_sim[:, i], color=col_sim, lw=0.8, label="Sim")
        ax.errorbar(
            t_min, exp_states[:, i],
            yerr=sigmas[i],
            fmt="o", ms=1.2, lw=0.0,
            elinewidth=0.6, capsize=1.5, capthick=0.6,
            color=col_exp, label=r"Exp ($\pm1\sigma$)",
        )
        ax.set_ylabel(state_labels[i], fontsize=8)
        ax.tick_params(labelsize=8)
        if i == 0:
            ax.legend(fontsize=7, loc="best")

    axes_flat[-1].set_visible(False)
    for ax in axes_flat[:-1]:
        ax.set_xlabel("Time (min)", fontsize=8)

    fig.suptitle(
        f"{exp.name}\n$E_{{murphree}}$={E_murphree:.3f},  $rr_{{err}}$={rr_err:.3f},  $x_{{N2}}$={x_N2:.4f}",
        fontsize=8,
    )
    fig.tight_layout()

    if out_path is not None:
        fig.savefig(out_path, dpi=300, bbox_inches="tight")
        logger.info("Saved figure: %s", out_path)
    else:
        plt.show()
    plt.close(fig)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    """CLI entry point: parse arguments, run PE, and optionally generate diagnostic plots."""
    import argparse
    import datetime

    parser = argparse.ArgumentParser(description="Distillation column parameter estimation")
    parser.add_argument("--data-root", default="./data/experimentaldata")
    parser.add_argument("--out-dir", default=f"./parameter_estimation/Results/BO_PEresults_BO_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}")
    parser.add_argument("--init-points", type=int, default=81)
    parser.add_argument("--n-iter", type=int, default=500)
    parser.add_argument("--random-state", type=int, default=44)
    parser.add_argument("--penalty", type=float, default=1e5)
    parser.add_argument("--n-jobs", type=int, default=5)        #num experiments
    parser.add_argument("--noise-std-LI", type=float, default=DEFAULT_NOISE_STD["LI"])
    parser.add_argument("--noise-std-WI", type=float, default=DEFAULT_NOISE_STD["WI"])
    parser.add_argument("--noise-std-w-L-D-c1", type=float, default=DEFAULT_NOISE_STD["w_L_D_c1"])
    parser.add_argument("--noise-std-w-L-B-c1", type=float, default=DEFAULT_NOISE_STD["w_L_B_c1"])
    parser.add_argument("--noise-std-T-tr9", type=float, default=DEFAULT_NOISE_STD["T_tr9"])
    args = parser.parse_args()

    noise_std = {
        "LI":        args.noise_std_LI,
        "WI":        args.noise_std_WI,
        "w_L_D_c1":  args.noise_std_w_L_D_c1,
        "w_L_B_c1":  args.noise_std_w_L_B_c1,
        "T_tr9":     args.noise_std_T_tr9,
    }

    E_murphree_bounds = (0.3, 0.7)
    rr_err_bounds = (-0.20, -0.10)
    x_N2_bounds = (0.043, 0.080)
    h_weir_bounds = (0.005, 0.06)

    result = run_pe(
        E_murphree_bounds=E_murphree_bounds,
        rr_err_bounds=rr_err_bounds,
        x_N2_bounds=x_N2_bounds,
        h_weir_bounds=h_weir_bounds,
        data_root=args.data_root,
        noise_std=noise_std,
        init_points=args.init_points,
        n_iter=args.n_iter,
        random_state=args.random_state,
        penalty=args.penalty,
        out_dir=args.out_dir,
        n_jobs=args.n_jobs,
    )
    print(f"\nBest parameters:")
    print(f"  E_murphree = {result['best_E_murphree']:.4f}")
    print(f"  rr_err     = {result['best_rr_err']:.4f}")
    print(f"  x_N2       = {result['best_x_N2']:.4f}")
    print(f"  WLS        = {result['best_wls']:.6g}")
    print(f"  Results    → {result['out_dir']}")

if __name__ == "__main__":
    main()
