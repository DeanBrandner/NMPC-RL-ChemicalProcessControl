"""Plot PE results: trajectory fits, search space, convergence, failure count."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from parameter_estimation import (
    WLS_STATE_NAMES,
    load_all_experiments,
    plot_fit,
    wls_total,
)

# ---------------------------------------------------------------------------
# Color scheme (CLAUDE.md)
# ---------------------------------------------------------------------------
_COL_SIM = np.array([0, 175, 240]) / 255.0
_COL_EXP = np.array([210, 0, 30]) / 255.0
_COL_BEST = np.array([140, 180, 15]) / 255.0
_W = 8.4 / 2.54   # single column width in inches


def _fig(nrows: int = 1, ncols: int = 1, row_h: float = 1.8) -> tuple:
    mpl.rcParams.update({"font.size": 8})
    fig, axes = plt.subplots(nrows, ncols, figsize=(_W * ncols, row_h * nrows))
    return fig, axes


# ---------------------------------------------------------------------------
# Search space  (auto-detects param columns; scales to N params via pair matrix)
# ---------------------------------------------------------------------------

_NON_PARAM_COLS = {"iter", "neg_target", "wls", "n_failed"}

_PARAM_LABELS: dict[str, str] = {
    "E_murphree":  r"$E_{murphree}$",
    "rr_err":      r"$rr_{err}$",
    "x_N2":        r"$x_{N_2}$",
    "h_tot":       r"$h_{tot}$",
    "h_weir":      r"$h_{weir}$",
    "log10_kappa": r"$\log_{10}\kappa$",
}


def _param_label(col: str) -> str:
    return _PARAM_LABELS.get(col, col)


def _scatter_pair(ax: "plt.Axes", x: np.ndarray, y: np.ndarray,
                  log_wls: np.ndarray, bx: float, by: float) -> "plt.cm.ScalarMappable":
    sc = ax.scatter(x, y, c=log_wls, cmap="viridis_r",
                    s=2, linewidths=0.3, edgecolors="k", zorder=2, vmin=log_wls.min(), vmax=log_wls.max())
    ax.scatter(bx, by, marker="*", s=20, color=_COL_BEST, zorder=5)
    return sc


def plot_search_space(probes: pd.DataFrame, best: dict, out_path: Path,
                      penalty: float = 1e7) -> None:
    """Pair-matrix scatter of all param columns colored by log10(WLS).

    N=2: single scatter panel (legacy layout).
    N>=3: N×N grid — diagonal=histogram, upper-triangle=scatter, lower hidden.
    Failed sims (wls >= penalty) excluded.
    """
    probes = probes[probes["wls"] < penalty].copy()
    wls = probes["wls"].values
    log_wls = np.log10(np.clip(wls, 1, None))

    param_cols = [c for c in probes.columns if c not in _NON_PARAM_COLS]
    N = len(param_cols)

    if N == 0:
        return

    if N == 1:
        fig, ax = _fig()
        ax.hist(probes[param_cols[0]].values, bins=20, color=_COL_SIM, edgecolor="k", linewidth=0.3)
        ax.set_xlabel(_param_label(param_cols[0]), fontsize=8)
        ax.set_ylabel("Count", fontsize=8)
        fig.tight_layout()
        fig.savefig(out_path, dpi=300, bbox_inches="tight")
        plt.close(fig)
        print(f"  → {out_path}")
        return

    if N == 2:
        # Legacy: single scatter
        fig, ax = _fig()
        sc = _scatter_pair(
            ax,
            probes[param_cols[0]].values, probes[param_cols[1]].values,
            log_wls, best.get(param_cols[0], 0), best.get(param_cols[1], 0),
        )
        cb = fig.colorbar(sc, ax=ax, pad=0.02)
        cb.set_label(r"$\log_{10}$(WLS)", fontsize=8)
        cb.ax.tick_params(labelsize=7)
        ax.set_xlabel(_param_label(param_cols[0]), fontsize=8)
        ax.set_ylabel(_param_label(param_cols[1]), fontsize=8)
        ax.tick_params(labelsize=8)
        fig.tight_layout()
        fig.savefig(out_path, dpi=300, bbox_inches="tight")
        plt.close(fig)
        print(f"  → {out_path}")
        return

    # N >= 3: pair matrix
    mpl.rcParams.update({"font.size": 7})
    panel_size = max(1.4, _W / N)
    # sharex="col" aligns x ranges per column; no sharey — scatter y must be
    # independent of histogram counts
    fig, axes = plt.subplots(N, N, figsize=(panel_size * N, panel_size * N),
                             sharex="col")

    # Data ranges per parameter for scatter ylim
    param_ranges: dict[str, tuple[float, float]] = {}
    for col in param_cols:
        lo, hi = probes[col].values.min(), probes[col].values.max()
        pad = (hi - lo) * 0.05 or 0.01
        param_ranges[col] = (lo - pad, hi + pad)

    sc_ref = None
    for i in range(N):
        for j in range(N):
            ax = axes[i, j]
            if i == j:
                # Diagonal: histogram — x-label here is bottom of this column
                ax.hist(probes[param_cols[i]].values, bins=15,
                        color=_COL_SIM, edgecolor="k", linewidth=0.2)
                ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(integer=True, nbins=3))
                ax.yaxis.set_label_position("left")
                ax.tick_params(axis="y", labelsize=5, left=True)
                ax.set_xlabel(_param_label(param_cols[i]), fontsize=7)
            elif j > i:
                # Upper triangle: scatter
                sc_ref = _scatter_pair(
                    ax,
                    probes[param_cols[j]].values, probes[param_cols[i]].values,
                    log_wls,
                    best.get(param_cols[j], 0), best.get(param_cols[i], 0),
                )
                ax.set_ylim(*param_ranges[param_cols[i]])
                if j == N - 1:
                    # rightmost scatter panel in this row — y-label + ticks on right
                    ax.yaxis.set_label_position("right")
                    ax.yaxis.tick_right()
                    ax.set_ylabel(_param_label(param_cols[i]), fontsize=7)
                else:
                    ax.yaxis.set_ticklabels([])
            else:
                # Lower triangle: hide
                ax.set_visible(False)

            ax.tick_params(labelsize=6)

    if sc_ref is not None:
        fig.subplots_adjust(bottom=0.12, hspace=0.05, wspace=0.05)
        cbar_ax = fig.add_axes([0.15, 0.03, 0.70, 0.02])
        cb = fig.colorbar(sc_ref, cax=cbar_ax, orientation="horizontal")
        cb.set_label(r"$\log_{10}$(WLS)", fontsize=7)
        cb.ax.tick_params(labelsize=6)
    else:
        fig.tight_layout()

    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  → {out_path}")


# ---------------------------------------------------------------------------
# Convergence
# ---------------------------------------------------------------------------

def plot_convergence(probes: pd.DataFrame, out_path: Path) -> None:
    """Best WLS found so far vs iteration."""
    fig, ax = _fig()
    best_so_far = probes["wls"].cummin()
    ax.plot(probes["iter"], probes["wls"], "o", ms=2, color=_COL_EXP, label="WLS")
    ax.plot(probes["iter"], best_so_far, color=_COL_SIM, lw=1.0,
            label="Best so far")
    ax.set_xlabel("Iteration", fontsize=8)
    ax.set_ylabel("WLS", fontsize=8)
    ax.set_yscale("log")
    ax.tick_params(labelsize=8)
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  → {out_path}")


# ---------------------------------------------------------------------------
# Failed experiments over iterations
# ---------------------------------------------------------------------------

def plot_failures(probes: pd.DataFrame, out_path: Path) -> None:
    """n_failed per iteration as bar chart."""
    fig, ax = _fig()
    ax.bar(probes["iter"], probes["n_failed"],
           color=_COL_EXP, width=0.8, linewidth=0)
    ax.set_xlabel("Iteration", fontsize=8)
    ax.set_ylabel("Failed experiments", fontsize=8)
    ax.yaxis.get_major_locator().set_params(integer=True)
    ax.tick_params(labelsize=8)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  → {out_path}")


# ---------------------------------------------------------------------------
# Per-state WLS breakdown at best params
# ---------------------------------------------------------------------------

def plot_state_breakdown(breakdown: dict, out_path: Path) -> None:
    """Bar chart of WLS contribution per state summed across experiments."""
    state_totals = {name: 0.0 for name in WLS_STATE_NAMES}
    for bd in breakdown.values():
        if isinstance(bd, dict):
            for name in WLS_STATE_NAMES:
                state_totals[name] += bd.get(name, 0.0)

    fig, ax = _fig()
    colors = [
        np.array([0, 175, 240]) / 255.0,
        np.array([0, 137, 186]) / 255.0,
        np.array([140, 180, 15]) / 255.0,
        np.array([130, 165, 50]) / 255.0,
        np.array([210, 0, 30]) / 255.0,
    ]
    ax.bar(list(state_totals.keys()), list(state_totals.values()),
           color=colors, linewidth=0)
    ax.set_ylabel("WLS contribution", fontsize=8)
    ax.tick_params(labelsize=8)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  → {out_path}")


# ---------------------------------------------------------------------------
# Per-experiment WLS breakdown at best params
# ---------------------------------------------------------------------------

def plot_experiment_breakdown(breakdown: dict, out_path: Path) -> None:
    """Bar chart of total WLS per experiment at best params."""
    names = list(breakdown.keys())
    totals = [
        bd["total"] if isinstance(bd, dict) else float("nan")
        for bd in breakdown.values()
    ]
    short_names = [n.replace("trained_agent_", "tr_").replace("untrained_agent_", "un_")
                   for n in names]

    fig, ax = _fig(row_h=2.2)
    ax.bar(range(len(names)), totals, color=_COL_SIM, linewidth=0)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(short_names, rotation=30, ha="right", fontsize=7)
    ax.set_ylabel("WLS", fontsize=8)
    ax.tick_params(labelsize=8)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  → {out_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Generate all PE result figures."""
    results_dir = Path("./parameter_estimation/Results/PEresults4_WI")
    data_root = Path("./data/experimentaldata")
    figs_dir = results_dir / "figs"
    traj_dir = figs_dir / "trajectories"
    figs_dir.mkdir(parents=True, exist_ok=True)
    traj_dir.mkdir(parents=True, exist_ok=True)

    with open(results_dir / "best.json") as fh:
        best = json.load(fh)
    with open(results_dir / "breakdown.json") as fh:
        breakdown = json.load(fh)

    E_murphree: float = best["E_murphree"]
    rr_err: float = best["rr_err"]
    x_N2: float = best.get("x_N2", 0.04273159753760128)
    h_tot: float = best.get("h_tot", 0.179372959955645)
    h_weir: float = best.get("h_weir", 0.0428980603490154)
    kappa: float = best.get("kappa", 0.0424670248823593)
    print(f"Best: E_murphree={E_murphree:.4f}, rr_err={rr_err:.4f}, x_N2={x_N2:.4f}, "
          f"h_tot={h_tot:.4f}, h_weir={h_weir:.4f}, kappa={kappa:.4g}, WLS={best['wls']:.6g}")

    # Recover noise_var from config.json (weights = 1/σ² when noise_var was used).
    noise_var: dict[str, float] | None = None
    config_path = results_dir / "config.json"
    if config_path.exists():
        with open(config_path) as fh:
            cfg = json.load(fh)
        if "weights" in cfg:
            noise_var = {name: 1.0 / w for name, w in cfg["weights"].items() if w > 0}

    probes = pd.read_csv(results_dir / "probes.csv")

    print("\n--- BO diagnostics ---")
    plot_search_space(probes, best, figs_dir / "search_space.png")
    plot_convergence(probes, figs_dir / "convergence.png")
    plot_failures(probes, figs_dir / "failures.png")
    plot_state_breakdown(breakdown, figs_dir / "state_breakdown.png")
    plot_experiment_breakdown(breakdown, figs_dir / "experiment_breakdown.png")

    print("\n--- Trajectory fits ---")
    experiments = load_all_experiments(data_root, trained_only=False)
    for exp in experiments:
        print(f"Plotting {exp.name}...")
        plot_fit(E_murphree, rr_err, x_N2, exp,
                 out_path=traj_dir / f"fit_{exp.name}.png",
                 noise_std=noise_var,
                 h_tot=h_tot, h_weir=h_weir, kappa=kappa)

    print("\nDone. Diagnostics in", figs_dir, "| Trajectories in", traj_dir)


if __name__ == "__main__":
    main()
