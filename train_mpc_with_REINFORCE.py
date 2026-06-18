"""Train an RL-MPC agent with multiprocessing rollouts.

This script coordinates repeated batches of environment rollouts, collects
episode buffers from worker processes, updates the RL-MPC agent, and stores
training artifacts under the configured agent directory. Algorithmic details
are discussed in the accompanying paper; this module documents the operational
training flow and file outputs.
"""

import os, pickle, time, json
import numpy as np
import pandas as pd

from multiprocessing import Process, Queue, Value
from tqdm import tqdm

from mp_utils import run_episode_loop

from surrogate_mpc import get_default_rlmpc as get_rl_mpc
from rl_mpc_agents_stoch import RL_MPC_SPG_REINFORCE_agent as Agent
from environment import BatchDistillationEnv as Environment

def train(
        n_processes:int,
        agent_path:str,
        mpc_model_path: str,
        n_narx_steps: int = 1,
        rl_settings: dict = {},
        env_settings: dict = {},
        n_replays: int = 101,
        n_episodes_per_replay: int = 50,
        resume_training_at: int = 0,
    ):
    """Run the batched RL-MPC training loop.

    Parameters
    ----------
    n_processes : int
        Number of worker processes used for parallel episode rollouts. The
        value is capped at ``n_episodes_per_replay``.
    agent_path : str
        Directory where agent checkpoints, configuration files, replay
        summaries, gradients, and timing data are written.
    mpc_model_path : str
        Path to a pickled do-mpc surrogate model used to construct the RL-MPC
        controller. The corresponding ``hyperparams.pkl`` is loaded from the
        same directory.
    n_narx_steps : int, optional
        Number of NARX steps used by the surrogate model. The worker
        environment receives ``n_history = n_narx_steps - 1``.
    rl_settings : dict, optional
        Keyword overrides for the agent settings.
    env_settings : dict, optional
        Keyword overrides for the environment settings passed to each worker.
    n_replays : int, optional
        Number of replay/update iterations to execute.
    n_episodes_per_replay : int, optional
        Number of rollout episodes collected before each agent update.
    resume_training_at : int, optional
        Replay index from which to resume. When nonzero, existing result and
        timing pickles are loaded from ``agent_path``.

    Notes
    -----
    The function writes ``agent_config.json``, ``training_config.json``,
    ``environment_config.json``, replay result pickles, policy-gradient
    pickles, RL-parameter checkpoints, and final agent state into
    ``agent_path``.
    """

    n_processes = min(n_processes, n_episodes_per_replay)

    
    with open(mpc_model_path, "rb") as f:
        dist_model_do_mpc_rl = pickle.load(f)

    with open(os.path.join(os.path.dirname(mpc_model_path), "hyperparams.pkl"), "rb") as f:
        hyperparameters = pickle.load(f)


    # Start the workers
    task_queue = Queue()
    environment_queue = Queue()
    progress_counter = Value("i", 0)

    process_args = (
        dist_model_do_mpc_rl,
        hyperparameters,
        get_rl_mpc,
        Agent,
        n_narx_steps,
        rl_settings,
        Environment,
        env_settings,
        agent_path,
        task_queue,
        environment_queue,
        progress_counter
        )

    workers = []
    for i in range(n_processes):
        worker = Process(target = run_episode_loop, args = process_args)
        workers.append(worker)
        worker.start()

    if resume_training_at == 0:
        mpc = get_rl_mpc(dist_model_do_mpc_rl, hyperparameters)
        agent = Agent(mpc, rl_settings, init_differentiator = False)
    else:
        agent = Agent.load(os.path.join(agent_path, f"agent_update_{resume_training_at}"))

    agent_config = {}
    for key, value in agent.settings.__dict__.items():
        agent_config[key] = value
        if isinstance(value, np.ndarray):
            agent_config[key] = value.tolist()

    os.makedirs(agent_path, exist_ok = True)
    with open(os.path.join(agent_path, "agent_config.json"), "w") as f:
        json.dump(agent_config, f, sort_keys = True, indent = 4)

    training_config = {}
    training_config["n_processes"] = n_processes
    training_config["mpc_model_path"] = mpc_model_path
    training_config["n_narx_steps"] = n_narx_steps
    training_config["n_replays"] = n_replays
    training_config["n_episodes_per_replay"] = n_episodes_per_replay
    training_config["resume_training_at"] = resume_training_at
    with open(os.path.join(agent_path, "training_config.json"), "w") as f:
        json.dump(training_config, f, sort_keys = True, indent = 4)

    task_queue.put("GET_ENVIRONMENT_CONFIG")
    env_config = environment_queue.get()
    with open(os.path.join(agent_path, "environment_config.json"), "w") as f:
        json.dump(env_config, f, sort_keys = True, indent = 4)


    time_per_replay = []
    if resume_training_at != 0:
        with open(os.path.join(agent_path, "training_time.pkl"), "rb") as f:
            time_per_replay = pickle.load(f)
    

    if resume_training_at == 0:
        agent.save(os.path.join(agent_path, f"agent_update"))
        agent.save_rl_parameters(os.path.join(agent_path, f"agent_update_0"))


    # Do the training
    unprocessed_results_list = []
    processed_results_list = []

    if resume_training_at != 0:
        with open(os.path.join(agent_path, f"unprocessed_results_list.pkl"), "rb") as f:
            unprocessed_results_list = pickle.load(f)
        with open(os.path.join(agent_path, f"processed_results_list.pkl"), "rb") as f:
            processed_results_list = pickle.load(f)

    pbar_replays = tqdm(desc = "Replays".rjust(20), total = n_replays + resume_training_at, initial = resume_training_at)
    pbar_episodes = tqdm(desc = "Episodes".rjust(20), total = n_episodes_per_replay)

    for replay_idx in range(resume_training_at, resume_training_at + n_replays):
        start_time = time.time()
        pbar_replays.update(1)
        pbar_replays.refresh()

        with progress_counter.get_lock():
            progress_counter.value = 0
        pbar_episodes.n = 0
        pbar_episodes.reset()

        for seed in range(n_episodes_per_replay):
            task_queue.put({
                "episode": seed,
                "seed": seed,
                "training": True,
                "rlp": agent.mpc.rlp_fun(0).master
            })

        gathered_results = []
        for seed in range(n_episodes_per_replay):
            env_results = environment_queue.get()

            agent.copy_episode(env_results["episode_buffer"])

            gathered_results.append(env_results["trajectory_results"])

            with progress_counter.get_lock():
                completed = progress_counter.value
            pbar_episodes.n = completed
            pbar_episodes.refresh()

        cum_reward_list = []
        termination_list = []
        truncation_list = []

        for result in gathered_results:

            cum_reward = [agent.settings.gamma ** k * item for k, item in enumerate(result["rewards"])]
            cum_reward_list.append(np.sum(cum_reward))
            termination_list.append(int(result["termination"]))
            truncation_list.append(int(result["truncation"]))

        unprocessed_results = pd.DataFrame(
            data = {
                "cum_reward": cum_reward_list,
                "termination": termination_list,
                "truncation": truncation_list,
            }
        )
        processed_results = unprocessed_results.describe()

        unprocessed_results_list.append(unprocessed_results)
        processed_results_list.append(processed_results)

        with open(os.path.join(agent_path, f"unprocessed_results_list.pkl"), "wb") as f:
            pickle.dump(unprocessed_results_list, f)
        with open(os.path.join(agent_path, f"processed_results_list.pkl"), "wb") as f:
            pickle.dump(processed_results_list, f)
        

        policy_gradient = agent.replay()

        print(f"New policy paramameters after replay {replay_idx + 1}:")
        print(agent.mpc.rlp_fun(0).master)

        agent.save_rl_parameters(os.path.join(agent_path, f"agent_update_{replay_idx + 1}"))
        with open(os.path.join(agent_path, f"agent_update_{replay_idx}", "policy_gradients.pkl"), "wb") as f:
            pickle.dump(policy_gradient, f)


        end_time = time.time()

        replay_time = end_time - start_time
        time_per_replay.append(replay_time)

        with open(os.path.join(agent_path, "training_time.pkl"), "wb") as f:
            pickle.dump(time_per_replay, f)

    pbar_replays.close()
    pbar_episodes.close()

    agent.save(os.path.join(agent_path, f"agent_update_{replay_idx + 1}"))

    
    for worker in workers:
        task_queue.put("STOP")
    for worker in workers: 
        worker.join()

    return

if __name__ == "__main__":

    resume_training_at = 0

    n_narx_steps = 1
    surrogate_version = ""

    n_mpc_processes = min(int(os.cpu_count() // 2) - 1, 50)
    print(f"Using {n_mpc_processes} parallel processes for MPC rollouts.")
    print("Note: Adjust n_mpc_processes if you encounter memory issues or want to speed up data generation.\n")
    n_replays = 1501
    n_episodes_per_replay = 100

    
    rl_settings = {
        "use_adam": True,
        "actor_learning_rate": 1e-4,
        "adam_beta_1": 0.9,
        "adam_beta_2": 0.999,
        "adam_epsilon": 1e-5,
        "gamma": 1.0,
        "clc_scale": 1e0,
        "exploration_noise_std": np.array([5e-3, 5e-2]),
        "baseline": "constant",
    }            

    env_settings = {
        "diverse_initial_conditions": True,
        "initial_condition_path": os.path.join("data", "LVcolumn_DAE_init", "IC_sample_1000_cleaned.pkl"),
        "parametric_uncertainty_sampling_frequency": "episode",
    }

    mpc_model_path = os.path.join("surr_models", "260506_141325_Sampling_1000", f"narx_{n_narx_steps}step{surrogate_version}", "do_mpc_model_rl_with_num_time.pkl")
    
    # Environment config folder
    ic_file = os.path.basename(env_settings["initial_condition_path"]).replace(".pkl", "")
    diverse_ic_str = "diverse" if env_settings["diverse_initial_conditions"] else "fixed"
    pus_freq = env_settings["parametric_uncertainty_sampling_frequency"][0]
    env_config = f"narx{n_narx_steps}_IC{ic_file}_{diverse_ic_str}_pus{pus_freq}" if env_settings["diverse_initial_conditions"] else f"narx{n_narx_steps}_{diverse_ic_str}_pus{pus_freq}"
    
    if resume_training_at == 0:
        agent_name = f"agent_{time.strftime('%y%m%d_%H%M%S')}"
    else:
        raise NotImplementedError("Resuming training is not implemented yet. Please set resume_training_at to 0.")
    
    agent_path = os.path.join(
        "agents",
        "rl_mpc_spg_agent",
        "260506_141325_Sampling_1000",
        env_config,
        agent_name
    )

    start_time = time.time()
    train(
        n_processes=n_mpc_processes,
        agent_path=agent_path,
        mpc_model_path = mpc_model_path,
        n_narx_steps = n_narx_steps,
        rl_settings = rl_settings,
        env_settings = env_settings,
        n_replays=n_replays,
        n_episodes_per_replay=n_episodes_per_replay,
        resume_training_at = resume_training_at,
    )
    end_time = time.time()

    print(f"Training time: {end_time - start_time:.2f} seconds")
    print(f"Training time: {(end_time - start_time) / 60:.2f} minutes")
    print(f"Training time: {(end_time - start_time) / 3600:.2f} hours")
    print(f"Training time: {(end_time - start_time) / 86400:.2f} days")

    with open(os.path.join(agent_path, "training_time.txt"), "w") as f:
        f.write(f"Training time: {end_time - start_time:.2f} seconds\n")
        f.write(f"Training time: {(end_time - start_time) / 60:.2f} minutes\n")
        f.write(f"Training time: {(end_time - start_time) / 3600:.2f} hours\n")
        f.write(f"Training time: {(end_time - start_time) / 86400:.2f} days\n")
