"""Multiprocessing rollout utilities for RL-MPC training.

Worker processes use this module to construct local MPC agents and
environments, execute complete episodes, and send trajectory summaries plus
episode buffers back to the training coordinator.
"""

from multiprocessing import Queue
import casadi as cd
import numpy as np


def run_episode_loop(
        model,
        hyperparameters,
        prepare_mpc,
        Agent_class,
        n_narx_steps: int,
        rl_settings: dict,
        Environment,
        env_settings: dict,
        agent_path: str,
        task_queue: Queue,
        environment_queue: Queue,
        progress_counter):
    """Run the worker loop for parallel episode collection.

    Parameters
    ----------
    model
        do-mpc surrogate model used to construct the worker-local MPC.
    hyperparameters
        Surrogate-model metadata used for MPC setup and environment timing.
    prepare_mpc : callable
        Factory function that receives ``model`` and ``hyperparameters`` and
        returns a configured MPC instance.
    Agent_class
        Agent class instantiated in the worker.
    n_narx_steps : int
        Number of NARX steps used to set the environment history length.
    rl_settings : dict
        Agent settings dictionary.
    Environment
        Environment class instantiated in the worker.
    env_settings : dict
        Base environment settings updated with worker-specific rollout values.
    agent_path : str
        Agent artifact path forwarded by the trainer. Currently unused in this
        function.
    task_queue : multiprocessing.Queue
        Queue receiving ``"STOP"``, ``"GET_ENVIRONMENT_CONFIG"``, or episode
        task dictionaries.
    environment_queue : multiprocessing.Queue
        Queue used to return environment configuration and rollout results.
    progress_counter : multiprocessing.Value
        Shared counter incremented after each completed episode.
    """
    
    mpc = prepare_mpc(model, hyperparameters)
    agent = Agent_class(mpc, rl_settings, init_differentiator = True)

    environment_config = env_settings.copy()
    environment_config.pop("version", None)
    environment_config.update({
        "t_step": hyperparameters.t_step_for_model,
        "n_history": n_narx_steps - 1,
        "meas_noise_bool": True,
        "parametric_uncertainty_bool": True,
        "scale_observations": False,
        "rescale_actions": False,
        "t_max": 2.0 * 3600.0 
    })
    environment = Environment(seed = 0, config = environment_config)
    
    while True:
        task = task_queue.get()
        if task == "STOP":
            break

        if task == "GET_ENVIRONMENT_CONFIG":
            env_config = {}
            for key, value  in environment.settings.__dict__.items():
                env_config[key] = value
                if isinstance(value, np.ndarray):
                    env_config[key] = value.tolist()
            environment_queue.put(env_config)
            continue

        if "episode" in task:
            episode = task["episode"]

        seed = task["seed"]

        if "training" in task:
            training = task["training"]
        else:
            training = False

        if "testing" in task:
            testing = task["testing"]
        else:
            testing = False


        if "rlp" in task:
            rlp = task["rlp"]
            rlp_template = agent.mpc.get_rlp_template()
            rlp_template.master = rlp
            agent.mpc.set_rlp_fun(lambda t: rlp_template)


        run_episode(
            seed,
            agent,
            environment,
            training,
            testing,
            environment_queue,
            progress_counter
            )
        
def run_episode(seed:int, agent, environment, training:bool, testing:bool,  environment_queue: Queue, progress_counter):
    """Execute one complete environment episode with the given agent.

    Parameters
    ----------
    seed : int
        Base seed for the rollout. Training episodes use this seed directly;
        testing episodes use an offset seed range.
    agent
        MPC agent used to compute actions and store transition data.
    environment
        Environment instance used for rollout simulation.
    training : bool
        Whether the episode is part of training data collection.
    testing : bool
        Whether the episode is part of testing/evaluation data collection.
    environment_queue : multiprocessing.Queue
        Queue receiving a trajectory summary and the collected episode buffer.
    progress_counter : multiprocessing.Value
        Shared completion counter incremented after the episode.

    Notes
    -----
    The stochastic-agent path expects ``agent.act`` to return ``mpc_action``,
    ``policy_action``, and ``grad_ln_pi`` entries, and stores the resulting
    transition in the agent replay buffer before sending it to the parent
    process.
    """

    if training and not testing:
        observation, info = environment.reset(seed = 0 + seed)
    elif not training and testing:
        observation, info = environment.reset(seed = int(1e5) + seed)
    else:
        raise(ValueError("Either training or testing must be True. You have training =", training, " and testing =", testing))

    u_prev = environment.get_old_action()


    agent.mpc.x0.master = cd.DM(observation)
    agent.mpc.u0.master = cd.DM(u_prev)
    agent.mpc.set_initial_guess()

    

    termination, truncation = False, False

    reward_list = []
    counter = 0
    while not (termination or truncation):
        if "policy_type" not in agent.__dir__():
            agent.policy_type = "deterministic"

        if agent.policy_type == "deterministic":
            action_dict = agent.act(state = observation, old_action = u_prev, training = True)
            action = action_dict["action"]
            jac_action_rlp = action_dict["jac_action_rlp"]

            explored_action = agent.explore(action = action)
        elif agent.policy_type == "stochastic":
            action_dict = agent.act(state = observation, old_action = u_prev, deterministic = False, training = True)
            mpc_action = action_dict["mpc_action"]
            policy_action = action_dict["policy_action"]
            grad_ln_pi = action_dict["grad_ln_pi"]

            explored_action = policy_action.copy()


        env_results = environment.step(action = explored_action)

        next_observation, reward, termination, truncation, info = env_results

        agent.remember_transition(
            state = observation,
            det_action = mpc_action,
            policy_action = policy_action,
            grad_ln_pi = grad_ln_pi,
            reward = reward,
            next_state = next_observation,
            termination = termination,
            truncation = truncation,
        )

        observation = next_observation.copy()
        u_prev = explored_action.copy()

        counter += 1

    agent.mpc.reset_history()

    environment_queue.put(
        {
            "trajectory_results": {
                "episode": 0,
                "seed": seed,
                "rewards": environment.reward_list,
                "termination": termination,
                "truncation": truncation,
            },
            "episode_buffer": agent.replay_buffer.current_episode
        }
    )

    agent.replay_buffer.clear()

    with progress_counter.get_lock():
        progress_counter.value += 1

    return
