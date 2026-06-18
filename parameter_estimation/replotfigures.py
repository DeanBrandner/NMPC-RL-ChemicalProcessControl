import sys
from parameter_estimation import load_all_experiments, plot_fit
from pathlib import Path
import json
import time
from plot_pe_results import (  # noqa: E402
        plot_convergence, plot_experiment_breakdown, plot_failures,
        plot_search_space, plot_state_breakdown,
    )


make_plots = True
if make_plots:
    import pandas as pd
    _pe_dir = str(Path(__file__).parent)
    if _pe_dir not in sys.path:
        sys.path.insert(0, _pe_dir)

    results_dir = Path("./parameter_estimation/Results/PEresults_trainedagents_BO_20260429_173511")
    figs_dir = results_dir / "figs"
    traj_dir = figs_dir / "trajectories"
    data_root = Path("./data/experimentaldata")
    figs_dir.mkdir(parents=True, exist_ok=True)
    traj_dir.mkdir(parents=True, exist_ok=True)

    with open(results_dir / "best.json") as fh:
        best = json.load(fh)
    with open(results_dir / "breakdown.json") as fh:
        breakdown = json.load(fh)
    probes = pd.read_csv(results_dir / "probes.csv")

    print("\n--- Diagnostics plots ---")
    plot_search_space(probes, best, figs_dir / "search_space.png")
    plot_convergence(probes, figs_dir / "convergence.png")
    plot_failures(probes, figs_dir / "failures.png")
    plot_state_breakdown(breakdown, figs_dir / "state_breakdown.png")
    plot_experiment_breakdown(breakdown, figs_dir / "experiment_breakdown.png")
    print("  Diagnostic plots done.")

    print("\n--- Trajectory fits (runs PE_sim per experiment) ---")
    experiments = load_all_experiments(data_root, trained_only=False)
    for i, exp in enumerate(experiments):
        print(f"  [{i+1}/{len(experiments)}] {exp.name} ...", flush=True)
        t0 = time.perf_counter()
        try:
            plot_fit(
                E_murphree=best["E_murphree"],
                rr_err=best["rr_err"],
                x_N2=best["x_N2"],
                h_tot=best["h_tot"],
                h_weir=best["h_weir"],
                kappa=best["kappa"],
                exp=exp,
                out_path=traj_dir / f"fit_{exp.name}.png",
                noise_std=None,
            )
            print(f"        done ({time.perf_counter()-t0:.1f}s)", flush=True)
        except Exception as exc:
            print(f"        WARN: {exc}", flush=True)

    print(f"\n  Diagnostics → {figs_dir}")
    print(f"  Trajectories → {traj_dir}")
