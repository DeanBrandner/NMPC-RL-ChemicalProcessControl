"""Generate training, validation, and test data for surrogate model training.

This module implements a parallelized data generation pipeline for training a
surrogate model of a batch distillation column. Input-output trajectories are
collected by simulating the high-fidelity environment under Amplitude-modulated
Pseudo-Random Binary Sequence (APRBS) excitation signals across a fixed set of
model parameters. The resulting dataset covers the relevant operating space
and is used to fit a data-driven surrogate that replaces the high-fidelity
model within the NMPC optimization loop.
"""

from APRBS import APRBS_Sampler
import numpy as np
import tqdm
import os
import pickle
from multiprocessing import Process, Queue
from datetime import datetime

import pandas as pd

from environment import BatchDistillationEnv as Environment


def simulation(task_queue: Queue, result_queue: Queue) -> None:
    """Execute simulation rollouts received from a task queue and return results.

    This function is intended to run as a worker process. It instantiates a
    single ``Environment`` and processes tasks from ``task_queue`` until a
    ``"STOP"`` sentinel is received. For each task, the environment is reset,
    the physical model parameters are set, and a full APRBS input trajectory is
    applied. The resulting input, state, and parameter trajectories are returned
    via ``result_queue``.

    The geometric parameter ``h_tot`` and the hydrodynamic parameter ``kappa``
    are fixed at their nominal identified values and are not varied across
    trajectories, as they are treated as known constants in the surrogate
    modeling framework.

    Parameters
    ----------
    task_queue:
        Queue supplying task dictionaries. Each task must contain the keys
        ``seed``, ``rr_err``, ``E_murphree``, ``xN2``, ``h_weir``, and
        ``u_aprbs``. A string value ``"STOP"`` terminates the worker.
    result_queue:
        Queue to which result dictionaries are written. Each result contains
        three ``pandas.DataFrame`` objects under the keys ``"u"``, ``"x"``,
        and ``"p"``, holding the input, state, and parameter trajectories,
        respectively.
    """
    config = {
        "t_step": 120.0,               # Integration step size in seconds
        "scale_observations": False,
        "rescale_actions": False,
        "diverse_initial_conditions": True,
        "initial_condition_path": os.path.join(
            "data", "LVcolumn_DAE_init", "IC_sample_1000_cleaned.pkl"
        ),
        "parametric_uncertainty_bool": False,  # Surrogate model is not uncertainty-aware
    }
    environment = Environment(seed=42, config=config)

    while True:
        task = task_queue.get()

        if task == "STOP":
            break

        # Unpack uncertain model parameters from the task
        seed = task["seed"]
        rr_err = task["rr_err"]
        E_murphree = task["E_murphree"]
        xN2 = task["xN2"]
        h_weir = task["h_weir"]
        u_aprbs = task["u_aprbs"]

        # Nominal values of the geometric parameter h_tot and hydrodynamic parameter kappa,
        # held constant during data generation
        h_tot = 0.179372959955645
        kappa = 0.0424670248823593

        # Reset environment and apply the selected parameter configuration
        environment.reset(seed=seed)
        environment.set_new_parameters(
            rr_err=rr_err,
            E_murphree=E_murphree,
            xN2=xN2,
            h_tot=h_tot,
            h_weir=h_weir,
            kappa=kappa,
        )

        # Apply the full APRBS input trajectory step by step
        for u in u_aprbs:
            environment.step(u)

        # Flush the internal simulation buffers to make trajectory data accessible
        environment.physical_system.data.update(
            _x=environment.physical_system.sim_x_num_unscaled,
            _z=environment.physical_system.sim_z_num_unscaled,
        )

        # Column identifiers for inputs, parameters, and selected state variables
        u_columns = ["u_dummy_rr", "u_dummy_Q"]
        p_columns = [
            "e0_rr_err", "e0_E_murphree", "e0_x_N2",
            "e0_h_tot", "e0_h_weir", "e0_greek_kappa",
        ]
        x_columns = [
            "x_e0_LI", "x_e0_PDI", "x_e0_WI", "x_e0_PI_C", "x_e0_PI_B",
            "x_e0_w_L_C_c1", "x_e0_w_L_D_c1", "x_e0_w_L_B_c1",
            "x_e0_T_tr0", "x_e0_T_tr1", "x_e0_T_tr2",
            "x_e0_T_tr4", "x_e0_T_tr7", "x_e0_T_tr9",
        ]

        # Strip the leading "x_" prefix to match keys in the model's state dictionary
        x_columns_for_comparison = [item.split("_", 1)[-1] for item in x_columns]

        # Resolve indices of the selected state variables within the model's full state vector
        x_indices = []
        x_key_list = (
            list(environment.physical_system.model._x.keys())
            + list(environment.physical_system.model._z.keys()[1:])
        )
        for col in x_columns_for_comparison:
            for idx, key in enumerate(x_key_list):
                if col == key:
                    x_indices.append(idx)
                    break

        # Resolve indices of the selected parameters within the model's parameter vector
        p_indices = []
        p_key_list = list(environment.physical_system.model._p.keys()[1:])
        for col in p_columns:
            for idx, key in enumerate(p_key_list):
                if col == key:
                    p_indices.append(idx)
                    break

        # Extract and slice trajectory arrays to the selected variables
        u_data = environment.physical_system.data._u
        x_data = np.hstack([
            environment.physical_system.data._x,
            environment.physical_system.data._z,
        ])[:, x_indices]
        p_data = environment.physical_system.data._p[:, p_indices]

        # Package trajectories as labeled DataFrames for downstream processing
        u_data = pd.DataFrame(u_data, columns=u_columns)
        x_data = pd.DataFrame(x_data, columns=x_columns)
        p_data = pd.DataFrame(p_data, columns=p_columns)

        result_queue.put({"u": u_data, "x": x_data, "p": p_data})


def sample_data_for_surrogate(
    rr_err: float,
    E_murphree: float,
    xN2: float,
    h_weir: float,
    n_trajectories: int,
    n_processes: int = 1,
    seed: int = 0,
) -> dict:
    """Sample a dataset of input-state trajectories for surrogate model training.

    APRBS excitation signals are generated and dispatched to a pool of worker
    processes, each running an independent instance of the high-fidelity
    environment. Simulation results are collected asynchronously and assembled
    into a dataset of input (``u``), state (``x``), and parameter (``p``)
    trajectory lists.

    The uncertain model parameters ``rr_err``, ``E_murphree``, ``xN2``, and
    ``h_weir`` are held constant across all trajectories within a single call.
    Input diversity is achieved exclusively through the APRBS signals. To
    generate datasets covering parameter uncertainty, this function should be
    called repeatedly with different parameter values.

    Parameters
    ----------
    rr_err:
        Reflux ratio error, representing a systematic bias in the reflux
        ratio actuator.
    E_murphree:
        Murphree tray efficiency, characterizing the deviation from
        theoretical equilibrium separation on each tray.
    xN2:
        Mole fraction of nitrogen in the feed or relevant stream.
    h_weir:
        Weir height of the distillation column trays in meters.
    n_trajectories:
        Number of independent APRBS trajectories to simulate.
    n_processes:
        Number of parallel worker processes. Defaults to 1.
    seed:
        Base random seed. Individual trajectories receive seeds derived from
        this value to ensure reproducibility.

    Returns
    -------
    dict
        A dictionary with keys ``"x"``, ``"u"``, and ``"p"``, each mapping to
        a list of ``pandas.DataFrame`` objects of length ``n_trajectories``.
        The ``i``-th entry in each list corresponds to the same simulated
        trajectory.
    """
    # Instantiate the APRBS sampler with the operating range of the two inputs:
    # normalized reflux ratio (u1) and reboiler heat duty (u2)
    sampler = APRBS_Sampler(
        u_min=np.array([0.7, 3.0]),
        u_max=np.array([1.0, 6.0]),
        min_hold_time=120.0,          # Minimum time each input value is held (s)
        max_batch_time=180.0 * 60.0,  # Maximum trajectory duration (s)
        delta_t=120.0,                # Sampling interval matching the environment step (s)
        seed=seed + 42,
    )

    # Pre-generate all APRBS trajectories before launching workers
    aprbs_u_trajectories = []
    for _ in tqdm.tqdm(range(n_trajectories), desc="Sampling trajectories"):
        aprbs_u_trajectories.append(sampler.sample_trajectory())

    # Launch worker processes sharing the task and result queues
    task_queue: Queue = Queue()
    result_queue: Queue = Queue()

    workers = []
    for _ in range(n_processes):
        worker = Process(target=simulation, args=(task_queue, result_queue))
        worker.start()
        workers.append(worker)

    # Dispatch one task per trajectory; each task carries its own seed and parameters
    for idx, u_aprbs in enumerate(aprbs_u_trajectories):
        task_queue.put({
            "seed": seed + idx,
            "rr_err": rr_err,
            "E_murphree": E_murphree,
            "xN2": xN2,
            "h_weir": h_weir,
            "u_aprbs": u_aprbs,
        })

    # Collect results; ordering is not guaranteed due to parallel execution
    u_list = []
    x_list = []
    p_list = []

    for _ in tqdm.tqdm(
        iterable=enumerate(aprbs_u_trajectories),
        desc="Processing trajectories",
        total=n_trajectories,
    ):
        result = result_queue.get()
        x_list.append(result["x"])
        u_list.append(result["u"])
        p_list.append(result["p"])

    # Signal all workers to terminate and wait for clean shutdown
    for _ in workers:
        task_queue.put("STOP")
    for worker in workers:
        worker.join()

    return {"x": x_list, "u": u_list, "p": p_list}


if __name__ == "__main__":
    # Experiment configuration
    n_trajectories = 1000       # Trajectories for training and validation
    n_trajectories_test = 100   # Trajectories reserved for testing
    n_processes = min(int(os.cpu_count() // 2) - 1, 50)
    print(f"Using {n_processes} parallel processes for data generation.")
    print("Note: Adjust n_processes if you encounter memory issues or want to speed up data generation.")
    print()

    seed = 0

    # Identified nominal model parameters used throughout data generation
    E_murphree = 0.4454079860264417
    rr_err = -0.1732064536037636
    xN2 = 0.045842587810941714
    h_weir = 0.04326133478330423

    # --- Training and validation dataset ---
    print("Sampling training and validation data for surrogate model...")
    data = sample_data_for_surrogate(
        rr_err=rr_err,
        E_murphree=E_murphree,
        xN2=xN2,
        h_weir=h_weir,
        n_trajectories=n_trajectories,
        n_processes=n_processes,
        seed=seed,
    )

    print("Saving training and validation dataset...")
    timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
    save_path = os.path.join(
        "data", "LVcolumn_Sampling", f"{timestamp}_Sampling_{n_trajectories}.pkl"
    )
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as f:
        pickle.dump(data, f)

    print()

    # --- Test dataset (disjoint seed range to avoid overlap with training data) ---
    print("Sampling test data for surrogate model...")
    test_data = sample_data_for_surrogate(
        rr_err=rr_err,
        E_murphree=E_murphree,
        xN2=xN2,
        h_weir=h_weir,
        n_trajectories=n_trajectories_test,
        n_processes=n_processes,
        seed=seed + n_trajectories,
    )

    print("Saving test dataset...")
    timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
    save_path = os.path.join(
        "data", "LVcolumn_Sampling",
        f"{timestamp}_Sampling_{n_trajectories_test}_test.pkl",
    )
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as f:
        pickle.dump(test_data, f)
