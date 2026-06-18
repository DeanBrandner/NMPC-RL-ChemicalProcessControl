"""Stochastic RL-MPC agents and rollout update utilities.

This module defines the stochastic policy-gradient agent used with the
RL-augmented MPC controller. It handles bounded Gaussian exploration,
log-policy-gradient data collection, replay-buffer interaction, optimizer
updates, and persistence of agent state and RL parameters.
"""

import os, pickle, time
import numpy as np
import casadi as cd

from dataclasses import dataclass, field

from RL_MPC import RL_MPC
from helper import NLP_differentiator
from replay_buffer import ReplayBuffer, EpisodeBuffer, Transition
from optimizer import StochasticGradientAscent, Adam


def gauss_prob_density(x: np.ndarray, mean: np.ndarray, std: np.ndarray) -> np.ndarray:
    """Evaluate a diagonal Gaussian probability density elementwise."""
    var = std ** 2
    denom = (2 * np.pi * var) ** 0.5
    num = np.exp(-0.5 * ((x - mean) ** 2) / var)

    proability_density = num / denom
    return proability_density

def gauss_cdf(x: np.ndarray, mean: np.ndarray, std: np.ndarray) -> np.ndarray:
    """Evaluate a diagonal Gaussian cumulative distribution function elementwise."""
    z = (x - mean) / std
    cdf = 0.5 * (1 + cd.erf(z / np.sqrt(2)).full())
    return cdf

@dataclass
class Flags:
    """Runtime flags for agent state that is not part of user settings."""

    differentiator_initialized: bool = False
    first_run: bool = True

@dataclass
class RL_settings:
    """Configuration values for stochastic RL-MPC training."""

    gamma: float = 1.
    actor_learning_rate: float = 1e-3
    verbose: int = 1

    use_adam: bool = False
    adam_beta_1: float = 0.9
    adam_beta_2: float = 0.999
    adam_epsilon: float = 1e-8

    exploration_seed: int = 0
    exploration_noise_std: np.ndarray = 1.0

    clc_scale: float = 1.0
    baseline: str = "None"


@dataclass()
class Performance_data:
    """Small container for replay-level performance timing data."""

    episode: list = field(default_factory=list)
    # n_samples: list = field(default_factory=list)
    time_replay: list = field(default_factory=list)

    def __init__(self):
        """Initialize empty performance tracking lists."""
        super().__init__()
        self.episode = [0]
        # self.n_samples = []
        self.time_replay = []

    def update(self, agent):
        """Append timing data from the latest agent replay."""
        self.episode.append(self.episode[-1] + 1)
        # self.n_samples.append(agent.observed_states.shape)
        self.time_replay.append(agent._time_replay)
        return

    def to_csv(self, path: str):
        """Write collected performance data to a CSV file."""
        
        episode_to_save = self.episode[:-1]
        n_samples_to_save = self.n_samples
        time_replay_to_save = self.time_replay

        from pandas import DataFrame
        df = DataFrame({
            "episode": episode_to_save,
            # "n_samples": n_samples_to_save,
            "time_replay": time_replay_to_save
        })
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        df.to_csv(path, index = False)

    @classmethod
    def from_csv(cls, path: str):
        """Load performance data from a CSV file."""
        from pandas import read_csv
        df = read_csv(path)
        instance = cls()
        instance.episode = df["episode"].tolist()
        instance.episode.append(instance.episode[-1] + 1)  # Add one more episode for the next update
        # instance.n_samples = df["n_samples"].tolist()
        instance.time_replay = df["time_replay"].tolist()
        return instance



class RL_MPC_agent_stoch():
    """Base class for stochastic policy-gradient MPC agents."""
    policy_type: str = "stochastic"

    def __init__(
        self,
        mpc: RL_MPC = None,
        settings_dict: dict = {},
        **kwargs
        ):
        """Initialize common MPC, optimizer, replay-buffer, and exploration state."""

        self.mpc = mpc
        self.action_shape = mpc.model._u.shape
        self.action_scale = (self.mpc._u_ub.master - self.mpc._u_lb.master).full().T

        # NOTE: The differentiator must be initialied in the child class
        self.differentiator_rlp = None

        self.flags = Flags()
        self.settings = RL_settings(**settings_dict)

        if self.settings.use_adam:
            self.optimizer = Adam(learning_rate = self.settings.actor_learning_rate, beta1 = self.settings.adam_beta_1, beta2 = self.settings.adam_beta_2, epsilon = self.settings.adam_epsilon)
        else:
            self.optimizer = StochasticGradientAscent(learning_rate = self.settings.actor_learning_rate)

        self.replay_buffer = ReplayBuffer(gamma=self.settings.gamma)

        self.performance_data = Performance_data()

        self.exploration_noise_rng = np.random.default_rng(seed = self.settings.exploration_seed + 42)
    

    def _update_parameters(self, update: np.ndarray):
        """Apply an additive update to the MPC reinforcement parameters."""
        rlp_template = self.mpc.get_rlp_template()
        rlp_template.master = self.mpc.rlp_fun(0).master + update

        self.mpc.set_rlp_fun(lambda t_now: rlp_template)
    

    def act(self, state: np.ndarray, old_action: np.ndarray = None, training: bool = False,):
        """Return the deterministic MPC action for evaluation mode."""
        action = self.mpc.make_step(state, old_action)

        if not training:
            return action
        
        raise NotImplementedError("This function can only be used if training = False. The data, required for training changes from method to method and must be implemented in a child class.")

    def rejection_sample_exploration(self, action: np.ndarray) -> np.ndarray:
        """Sample a bounded exploratory action around the deterministic action."""
        
        noise = self.exploration_noise_rng.normal(loc=0.0, scale=self.settings.exploration_noise_std.reshape(self.action_shape), size=self.action_shape)
        exploratory_action = action + noise

        while np.any(self.mpc._u_lb.master.full() > exploratory_action) or np.any(exploratory_action > self.mpc._u_ub.master.full()):
            noise = self.exploration_noise_rng.normal(loc=0.0, scale=self.settings.exploration_noise_std.reshape(self.action_shape), size=self.action_shape)
            exploratory_action = action + noise

        return exploratory_action
    
    def compute_grad_ln_pi(self, action: np.ndarray, policy_action: np.ndarray, jac_mpc_rlp: np.ndarray) -> np.ndarray:
        """Compute the log-policy gradient with truncation-bias correction."""
        action = np.clip(action, self.mpc._u_lb.master.full(), self.mpc._u_ub.master.full())
        grad_ln_pi_biased = self.compute_grad_ln_pi_biased(action, policy_action, jac_mpc_rlp)
        grad_ln_pi_bias_correction = self.compute_grad_ln_pi_bias_correction(action, jac_mpc_rlp)
        grad_ln_pi = grad_ln_pi_biased - grad_ln_pi_bias_correction
        return grad_ln_pi
    
    def compute_grad_ln_pi_biased(self, action: np.ndarray, policy_action: np.ndarray, jac_mpc_rlp: np.ndarray) -> np.ndarray:
        """Compute the uncorrected Gaussian log-policy gradient."""
        # For a Gaussian policy, the log-probability gradient is proportional to the difference between the action and the mean, scaled by the inverse of the covariance matrix.
        # Here we assume a diagonal covariance matrix with standard deviation given by self.settings.exploration_noise_std.
        var_inv = 1 / self.settings.exploration_noise_std.reshape(self.action_shape)**2
        grad_ln_pi_wrt_rlp = (policy_action - action) * var_inv
        grad_ln_pi_wrt_rlp = grad_ln_pi_wrt_rlp.reshape(-1, 1)

        # Chain rule to get the gradient with respect to the policy parameters (rlp)
        grad_ln_pi_wrt_rlp = jac_mpc_rlp.T @ grad_ln_pi_wrt_rlp

        return grad_ln_pi_wrt_rlp
    
    def compute_grad_ln_pi_bias_correction(self, action: np.ndarray, jac_mpc_rlp: np.ndarray) -> np.ndarray:
        """Compute the correction term caused by bounded-action sampling."""

        N_ub = gauss_prob_density(x= self.mpc._u_ub.master.full(), mean=action, std=self.settings.exploration_noise_std.reshape(self.action_shape))
        N_lb = gauss_prob_density(x= self.mpc._u_lb.master.full(), mean=action, std=self.settings.exploration_noise_std.reshape(self.action_shape))

        Phi_ub = gauss_cdf(x= self.mpc._u_ub.master.full(), mean=action, std=self.settings.exploration_noise_std.reshape(self.action_shape))
        Phi_lb = gauss_cdf(x= self.mpc._u_lb.master.full(), mean=action, std=self.settings.exploration_noise_std.reshape(self.action_shape))

        grad_ln_P_wrt_action = (N_ub - N_lb) / (Phi_ub - Phi_lb + 1e-8)

        grad_ln_P_wrt_rlp = -jac_mpc_rlp.T @ grad_ln_P_wrt_action

        return grad_ln_P_wrt_rlp

    def replay(self):
        """Update policy parameters from stored episodes.

        Subclasses must implement the concrete replay/update rule.
        """
        raise NotImplementedError("This is an abstract method. It must be implemented in a child class.")

    def remember_transition(
            self,
            state: np.ndarray,
            det_action: np.ndarray,
            policy_action: np.ndarray,
            grad_ln_pi:np.ndarray,
            reward: float,
            next_state: np.ndarray,
            termination: bool,
            truncation: bool
            ):
        """Store one transition in the active replay-buffer episode."""
        self.replay_buffer.add_transition(
            state=state,
            det_action=det_action,
            policy_action=policy_action,
            grad_ln_pi=grad_ln_pi,
            reward=reward,
            next_state=next_state,
            termination=termination,
            truncation=truncation
        )

    def _compute_observed_clc(self):
        """Return the replay-buffer estimate of the observed closed-loop cost."""
        return self.replay_buffer.get_expected_returns()

    def copy_episode(self, episode_buffer: EpisodeBuffer):
        """Copy a completed worker episode into this agent's replay buffer."""
        self.replay_buffer.add_episode(episode_buffer)
            
    def _scale_actions(self):
        """Scale stored action arrays to normalized MPC input coordinates."""
        self.observed_previous_actions = (self.observed_previous_actions - self.mpc._u_lb.master.T.full()) / self.action_scale
        self.observed_taken_actions = (self.observed_taken_actions - self.mpc._u_lb.master.T.full()) / self.action_scale
        self.observed_jac_taken_action_parameters = self.observed_jac_taken_action_parameters / self.action_scale.reshape(1, self.action_scale.shape[1], 1)

        self.explored_previous_actions = (self.explored_previous_actions - self.mpc._u_lb.master.T.full()) / self.action_scale
        self.explored_taken_actions = (self.explored_taken_actions - self.mpc._u_lb.master.T.full()) / self.action_scale
        return

    def _compute_grad_V_theta(self, jac_action_parameters: list[np.ndarray], d_Q_d_a: list[np.ndarray]) -> np.ndarray:
        """
        This function computes the gradient of the state-value function with respect to the policy parameters along a full episode.
        """
        grad_V_theta = np.zeros((jac_action_parameters[0].T @ d_Q_d_a[0]).shape)
        for idx, (item_jac_action_params, item_dQ_da) in enumerate(zip(jac_action_parameters, d_Q_d_a)):
            grad_V_theta += self.settings.gamma ** idx * item_jac_action_params.T @ item_dQ_da
        return grad_V_theta
    
    
    def compute_policy_gradient(self, jac_action_rlp: list[np.ndarray], grad_Q_a: list[np.ndarray]) -> np.ndarray:
        """Aggregate discounted policy gradients over multiple episodes."""

        pg = np.zeros((jac_action_rlp[0][0].T.shape[0], 1))
        for j_a_rlp_ep_k, g_Q_a_ep_k in zip(jac_action_rlp, grad_Q_a):
            for idx, (j_a_rlp, g_Q_a) in enumerate(zip(j_a_rlp_ep_k, g_Q_a_ep_k)):
                pg += self.settings.gamma ** idx * j_a_rlp.T @ g_Q_a

        E = len(jac_action_rlp)
        policy_gradient = pg / E
        return policy_gradient
    



    # Loading and saving utilities! 
    def save(self, path: str, parameters_only: bool = False):
        """Persist the agent, MPC, differentiator, and RL parameters."""
        if not os.path.exists(path):
            os.makedirs(path)
        
        self.save_rl_parameters(path)

        if parameters_only:
            return
        
        attributes = self.__dict__.copy()

        mpc = attributes.pop("mpc")
        mpc.save(os.path.join(path, "mpc.pkl"))

        if "differentiator_rlp" in attributes:
            differentiator_rlp = attributes.pop("differentiator_rlp")
            with open(os.path.join(path, "differentiator_rlp.pkl"), "wb") as f:
                pickle.dump(differentiator_rlp, f)

        attributes.update({"class": self.__class__})
        
        with open(os.path.join(path, "agent.pkl"), "wb") as f:
            pickle.dump(attributes, f)
        return
    
    def save_rl_parameters(self, path: str):
        """Save the current MPC reinforcement parameters."""
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path, "rl_params.pkl"), "wb") as f:
            pickle.dump(self.mpc.rlp_fun(0), f)
    
    def load_rl_parameters(self, path: str):
        """Load MPC reinforcement parameters from disk and install them."""
        with open(os.path.join(path, "rl_params.pkl"), "rb") as f:
            rl_params = pickle.load(f)

        rlp_template = self.mpc.get_rlp_template()
        rlp_template.master = rl_params.master
        self.mpc.set_rlp_fun(lambda t_now: rlp_template)
        return self.mpc.rlp_fun(0)

    @staticmethod
    def load(path: str, load_differentiator: bool = True):
        """Load a previously saved agent checkpoint."""
        with open(os.path.join(path, "agent.pkl"), "rb") as f:
            agent_attributes = pickle.load(f)

        cls = agent_attributes.pop("class")

        mpc = RL_MPC.load(os.path.join(path, "mpc.pkl"))

        rl_settings = agent_attributes.pop("settings")

        agent = cls(mpc, rl_settings.__dict__, init_differentiator = False)
        if load_differentiator:
            with open(os.path.join(path, "differentiator_rlp.pkl"), "rb") as f:
                agent.differentiator_rlp = pickle.load(f)
        
        for key, value in agent_attributes.items():
            setattr(agent, key, value)
        return agent
 


class RL_MPC_SPG_REINFORCE_agent(RL_MPC_agent_stoch):
    """Stochastic policy-gradient RL-MPC agent using replayed episodes."""

    def __init__(self, mpc: RL_MPC, settings_dict: dict = {}, init_differentiator: bool = True, **kwargs):
        """Initialize the agent and optionally construct the NLP differentiator."""
        super().__init__(mpc, settings_dict, **kwargs)

        if init_differentiator:
            self.differentiator_rlp = NLP_differentiator(self.mpc, ["_rlp"])
            # self.differentiator_s = NLP_differentiator(self.mpc, ["_x0", "_u_prev"])
            self.flags.differentiator_initialized = True
        else:
            self.differentiator_rlp = None
            self.flags.differentiator_initialized = False
           

    def act(self, state: np.ndarray, old_action: np.ndarray = None, deterministic: bool = False, training: bool = False):
        """Compute an MPC action and optionally stochastic training metadata."""
        action = self.mpc.make_step(state, old_action)
        policy_action = action.copy()

        action_dict = {
            "mpc_action": action,
            "policy_action": policy_action,
            "grad_ln_pi": None,
            "success": self.mpc.solver_stats["success"]
        }

        if not deterministic:
            policy_action = self.rejection_sample_exploration(action)
            action_dict["policy_action"] = policy_action


        if training:
            if not self.flags.differentiator_initialized:
                raise ValueError("The differentiator must be initialized before training.")
            
            jac_mpc_rlp = np.zeros((self.mpc.model._u.shape[0], self.mpc.model._rlp.shape[0]))
            if self.mpc.solver_stats["success"]:
                jac_mpc_rlp = self.differentiator_rlp.jac_action_parameters(self.mpc)
            else:
                print("\nThe solver did not converge. The action is not used for training.")


            grad_ln_pi = self.compute_grad_ln_pi(action, policy_action, jac_mpc_rlp)
            action_dict["grad_ln_pi"] = grad_ln_pi

          
        return action_dict
    
    def _compute_policy_gradient(self):
        """Compute the replay-buffer policy gradient for the current batch."""

        N_episodes = len(self.replay_buffer.episodes)
        
        # Average number of steps per episode
        E = 0
        for ep in self.replay_buffer.episodes:
            E += len(ep.transitions)
        E /= N_episodes


        b = 0
        if self.settings.baseline == "None":
            b = 0
        elif self.settings.baseline == "constant":
            for idx, ep in enumerate(self.replay_buffer.episodes):
                b += (np.mean(ep.returns) - b) / (idx + 1)
        else:
            raise ValueError(f"Baseline type {self.settings.baseline} not recognized. Supported types are 'None' and 'constant'.")


        grad_V_list_s0_list = []
        for ep in self.replay_buffer.episodes:
            returns = ep.returns
            grad_ln_pi = np.array([t.grad_ln_pi for t in ep.transitions])
            returns = returns.reshape(-1, 1, 1)

            Phis = (returns - b) * grad_ln_pi

            grad_V_list_s0 = E * np.mean(Phis, axis = 0)
            grad_V_list_s0_list.append(grad_V_list_s0)

        

        policy_gradient = np.mean(grad_V_list_s0_list, axis = 0)
        policy_gradient *= 1 / self.settings.clc_scale

        return policy_gradient
    
    @staticmethod
    def _compute_predicted_clc(local_clc: float, m_hat: np.ndarray, update: np.ndarray):
        """Predict the local closed-loop cost after a candidate parameter update."""
        predicted_clc = local_clc + m_hat.T @ update
        predicted_clc = float(predicted_clc[0, 0])
        return predicted_clc

    def replay(self):
        """Compute a policy update from stored episodes and apply it to the MPC."""
        start_time_replay = time.time()

        observed_clc = self._compute_observed_clc()
        print(f"Observed CLC: {observed_clc:.4f}")
        
        policy_gradient = self._compute_policy_gradient()

        print(f"Policy gradient:")
        print(policy_gradient.T)
        
        update, m_hat, v_hat = self.optimizer.compute_update(policy_gradient)

        print(f"Parameter update:")
        print(update.T)

        predicted_clc = self._compute_predicted_clc(observed_clc, m_hat, update)
        print(f"Predicted CLC after update: {predicted_clc:.4f}")

        self._update_parameters(update)

        self.replay_buffer.clear()

        end_time_replay = time.time()
        self._time_replay = end_time_replay - start_time_replay

        # Track performance metrics
        self.performance_data.update(self)

        return policy_gradient
    
