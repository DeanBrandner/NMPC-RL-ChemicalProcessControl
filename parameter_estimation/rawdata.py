"""Utilities for loading and aligning raw 1Hz CSV data with pkl trajectories."""

from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np
import pandas as pd

# Suppress do-mpc optional-dependency warnings in every process that imports this module.
warnings.filterwarnings("ignore", message=".*ONNX.*")
warnings.filterwarnings("ignore", message=".*opcua.*")
warnings.filterwarnings("ignore", message=".*approximateMPC.*")


_RR_COL = "VRR_refluxratio ValueY"
_RR_TIME_COL = "VRR_refluxratio Time"
_Q_COL = "Q_ist ValueY"
_Q_TIME_COL = "Q_ist Time"
_TIMESTAMP_FMT = "%d.%m.%Y %H:%M:%S"

# CSV unit → pkl unit conversion factors
_RR_SCALE = 100.0    # CSV VRR [%] / 100 = rr_PLS [fraction]
_Q_SCALE = 1000.0    # CSV Q_ist [W] / 1000 = Q_PLS_R [kW]


def _load_csv_signals(
    csv_path: Path,
    cols: list[str],
    time_col: str,
    timestamp_fmt: str,
) -> tuple[np.ndarray, pd.DatetimeIndex]:
    """Load selected ValueY columns from raw CSV; return (values, timestamps)."""
    usecols = [time_col] + cols
    df = pd.read_csv(
        csv_path,
        sep=";",
        decimal=",",
        encoding="utf-16",
        usecols=usecols,
        low_memory=False,
    )
    ts = pd.to_datetime(df[time_col], format=timestamp_fmt)
    return df[cols].values.astype(float), pd.DatetimeIndex(ts)


def locate_raw_segment(
    csv_path: str | Path,
    ref_rr: np.ndarray,
    ref_q: np.ndarray,
    dt_ref: float = 120.0,
    *,
    rr_col: str = _RR_COL,
    rr_time_col: str = _RR_TIME_COL,
    q_col: str = _Q_COL,
    q_time_col: str = _Q_TIME_COL,
    timestamp_fmt: str = _TIMESTAMP_FMT,
    rr_scale: float = _RR_SCALE,
    q_scale: float = _Q_SCALE,
    max_mse: float | None = None,
    segment_index: int = 0,
) -> dict:
    """Find 1Hz index in raw CSV where pkl control trajectory starts.

    Expands pkl signals (dt_ref steps) to 1Hz piecewise-constant, scales CSV
    signals by rr_scale/q_scale, then finds offset via sliding-window MSE.

    Parameters
    ----------
    csv_path : path to raw CSV (UTF-16, ';'-delimited, ','-decimal, 1Hz).
    ref_rr   : pkl U[:,0], shape (N,), fraction (0–1), dt=dt_ref s.
    ref_q    : pkl U[:,1], shape (N,), kW, dt=dt_ref s.
    dt_ref   : step size of ref signals in seconds (default 120).
    rr_scale : divide CSV rr column by this to match ref_rr units (default 100).
    q_scale  : divide CSV Q column by this to match ref_q units (default 1000).
    max_mse  : raise ValueError if best MSE exceeds this (default: no check).
    segment_index : 0=best match, 1=second non-overlapping match, etc.

    Returns
    -------
    dict:
        idx_start : int          — 1Hz row index of segment start
        idx_end   : int          — 1Hz row index of segment end (inclusive)
        t_start   : datetime     — absolute timestamp of idx_start
        t_end     : datetime     — absolute timestamp of idx_end
        mse       : float        — combined MSE at best offset
    """
    csv_path = Path(csv_path)
    dt = int(dt_ref)

    ref_rr = np.asarray(ref_rr, dtype=float)
    ref_q = np.asarray(ref_q, dtype=float)
    N = len(ref_rr)
    if len(ref_q) != N:
        raise ValueError(f"ref_rr and ref_q must have same length: {N} vs {len(ref_q)}")

    # --- Expand pkl signals to 1Hz piecewise-constant ---
    ref_rr_1hz = np.repeat(ref_rr, dt)   # shape (N*dt,)
    ref_q_1hz = np.repeat(ref_q, dt)     # shape (N*dt,)
    N_1hz = N * dt

    # --- Load and scale CSV signals ---
    # rr and Q may have separate time columns; use rr time as master 1Hz index
    rr_vals, ts_rr = _load_csv_signals(csv_path, [rr_col], rr_time_col, timestamp_fmt)
    q_vals, ts_q = _load_csv_signals(csv_path, [q_col], q_time_col, timestamp_fmt)

    csv_rr = rr_vals[:, 0] / rr_scale
    csv_q = q_vals[:, 0] / q_scale
    M = len(csv_rr)

    dts_rr = pd.Series(ts_rr).diff().dt.total_seconds().dropna().values
    if not np.allclose(dts_rr, 1.0, atol=0.5):
        warnings.warn(
            f"CSV rr timestamps not uniform 1Hz: min={dts_rr.min():.3f}s max={dts_rr.max():.3f}s",
            stacklevel=2,
        )

    if M < N_1hz:
        raise ValueError(f"CSV too short: {M} rows < {N_1hz} needed.")

    # --- Sliding-window MSE (vectorized via stride tricks) ---
    from numpy.lib.stride_tricks import sliding_window_view

    wins_rr = sliding_window_view(csv_rr, N_1hz)  # (M-N_1hz+1, N_1hz)
    wins_q = sliding_window_view(csv_q, N_1hz)

    mse_rr = np.mean((wins_rr - ref_rr_1hz) ** 2, axis=1)
    mse_q = np.mean((wins_q - ref_q_1hz) ** 2, axis=1)
    mse_combined = mse_rr + mse_q                  # shape (M-N_1hz+1,)

    # --- Greedy non-overlapping minimum search ---
    mse_work = mse_combined.copy()
    peaks: list[tuple[int, float]] = []
    for _ in range(segment_index + 1):
        k = int(np.argmin(mse_work))
        s = float(mse_work[k])
        peaks.append((k, s))
        lo = max(0, k - N_1hz + 1)
        hi = min(len(mse_work), k + N_1hz)
        mse_work[lo:hi] = np.inf

    best_k, mse_best = peaks[segment_index]

    if max_mse is not None and mse_best > max_mse:
        raise ValueError(
            f"No reliable match: best MSE={mse_best:.4g} > max_mse={max_mse}."
        )

    idx_start = best_k
    idx_end = min(idx_start + N_1hz - 1, M - 1)
    t_start = ts_rr[idx_start].to_pydatetime()
    t_end = ts_rr[idx_end].to_pydatetime()

    return {
        "idx_start": idx_start,
        "idx_end": idx_end,
        "t_start": t_start,
        "t_end": t_end,
        "mse": mse_best,
    }


def extract_raw_segment(
    csv_path: str | Path,
    result: dict,
    out_pkl: str | Path,
    *,
    timestamp_fmt: str = _TIMESTAMP_FMT,
) -> pd.DataFrame:
    """Slice raw CSV to located segment, clean timestamps, save as pickle.

    Loads all columns, slices [idx_start:idx_end+1], keeps one time column
    renamed to "Time" (parsed as datetime), drops all other "*Time" columns.

    Parameters
    ----------
    csv_path : raw CSV path.
    result   : dict from locate_raw_segment (needs idx_start, idx_end).
    out_pkl  : output pickle path (e.g. experiment_dir/results/rawdata.pkl).

    Returns
    -------
    Cleaned DataFrame with "Time" + all "ValueY" columns.
    """
    csv_path = Path(csv_path)
    out_pkl = Path(out_pkl)

    df = pd.read_csv(
        csv_path,
        sep=";",
        decimal=",",
        encoding="utf-16",
        low_memory=False,
    )

    # Slice to segment
    df = df.iloc[result["idx_start"] : result["idx_end"] + 1].reset_index(drop=True)

    # Identify time cols: any col whose name ends with " Time"
    time_cols = [c for c in df.columns if c.endswith(" Time")]
    value_cols = [c for c in df.columns if c not in time_cols]

    if not time_cols:
        raise ValueError("No '* Time' columns found in CSV.")

    # Parse first time col → "Time"; drop the rest
    master_time = time_cols[0]
    df["Time"] = pd.to_datetime(df[master_time], format=timestamp_fmt)
    df = df.drop(columns=time_cols)[["Time"] + value_cols]
    df.columns = ["Time"] + [c.replace(" ValueY", "") for c in value_cols]

    out_pkl.parent.mkdir(parents=True, exist_ok=True)
    df.to_pickle(out_pkl)
    print(f"Saved {len(df)} rows → {out_pkl}")
    return df


if __name__ == "__main__":
    import pickle
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

    pkl_path = Path(
        sys.argv[1] if len(sys.argv) > 1
        else "data/experimentaldata/untrained_agent_260318/results/trajectories.pkl"
    )
    csv_path = Path(
        sys.argv[2] if len(sys.argv) > 2
        else "data/experimentaldata/untrained_agent_260318/results/260318_rawdata_untrainedagent.csv"
    )
    seg_idx = int(sys.argv[3]) if len(sys.argv) > 3 else 0

    with open(pkl_path, "rb") as fh:
        data = pickle.load(fh)
    u = np.asarray(data._u, dtype=float)
    ref_rr = u[:-1, 0]
    ref_q = u[:-1, 1]
    dt_ref = float(np.round(np.diff(np.asarray(data._time).flatten())[0]))

    print(f"pkl : N={len(ref_rr)}, dt={dt_ref}s")
    print(f"      rr [{ref_rr.min():.3f}, {ref_rr.max():.3f}]")
    print(f"      Q  [{ref_q.min():.3f}, {ref_q.max():.3f}]")

    result = locate_raw_segment(csv_path, ref_rr, ref_q, dt_ref, segment_index=seg_idx)

    print(f"\nSegment {seg_idx}:")
    print(f"  t_start = {result['t_start']}")
    print(f"  t_end   = {result['t_end']}")
    print(f"  idx     = {result['idx_start']} – {result['idx_end']}")
    print(f"  MSE     = {result['mse']:.6g}")

    out_pkl = pkl_path.parent / "rawdata.pkl"
    df = extract_raw_segment(csv_path, result, out_pkl)
    print(f"  cols    = {list(df.columns)}")
