"""Replay buffers for episodic reinforcement-learning rollouts.

This module stores per-transition training data, groups transitions into
episodes, and computes discounted returns for policy-gradient style updates.
It is used by the RL agents and multiprocessing utilities in the repository to
collect, archive, and reuse full episodes of interaction with the environment.
"""

from dataclasses import dataclass
import numpy as np


@dataclass
class Transition:
    """Single environment transition stored in the replay buffer.

    Attributes
    ----------
    state : numpy.ndarray
        State or observation before the action is applied.
    det_action : numpy.ndarray
        Deterministic action proposed by the policy or controller.
    policy_action : numpy.ndarray
        Action actually used for the rollout, after any exploration noise or
        stochastic sampling.
    grad_ln_pi : numpy.ndarray
        Gradient of the log policy probability with respect to policy
        parameters or reinforcement parameters.
    reward : float
        Scalar reward observed for the transition.
    next_state : numpy.ndarray
        State or observation after the transition.
    termination : bool
        True if the episode ended because a terminal condition was reached.
    truncation : bool
        True if the episode ended because of a time-limit truncation.
    """

    state: np.ndarray
    det_action: np.ndarray
    policy_action: np.ndarray
    grad_ln_pi: np.ndarray
    reward: float
    next_state: np.ndarray
    termination: bool
    truncation: bool

class EpisodeBuffer:
    """Container for the transitions and returns of one episode."""

    def __init__(self):
        """Create an empty episode buffer."""
        self.transitions = []
        self.returns = None

    def __repr__(self):
        return f"EpisodeBuffer: {len(self.transitions)} transitions"

    def add(self, transition: Transition):
        """Append one transition to the episode."""
        self.transitions.append(transition)

    def compute_returns(self, gamma: float = 1.0):
        """Compute discounted returns for all transitions in the episode.

        Parameters
        ----------
        gamma : float, optional
            Discount factor used for backward return accumulation. Defaults to
            ``1.0`` for undiscounted returns.
        """
        rewards = [t.reward for t in self.transitions]
        G = 0.0
        returns = []

        # backward return computation
        for r in reversed(rewards):
            G = r + gamma * G
            returns.insert(0, G)

        self.returns = np.array(returns)

    def clear(self):
        """Remove all stored transitions and returns."""
        self.transitions = []
        self.returns = None



class ReplayBuffer:
    """Replay buffer that stores full episodes and discounted returns."""

    def __init__(self, gamma: float = 1.0):
        """Initialize the replay buffer.

        Parameters
        ----------
        gamma : float, optional
            Discount factor used when computing episode returns.
        """
        self.gamma = gamma
        self.episodes = []
        self.current_episode = EpisodeBuffer()

    def __repr__(self):
        return f"ReplayBuffer (gamma = {self.gamma}): {len(self.episodes)} episodes stored, current episode length: {len(self.current_episode.transitions)}"

    def add_transition(
        self,
        state,
        det_action,
        policy_action,
        grad_ln_pi,
        reward,
        next_state,
        termination,
        truncation
    ):
        """Add one transition to the currently open episode."""
        transition = Transition(
            state,
            det_action,
            policy_action,
            grad_ln_pi,
            reward,
            next_state,
            termination,
            truncation
        )

        self.current_episode.add(transition)

    def add_episode(self, episode_buffer: EpisodeBuffer):
        """Store a completed episode buffer after computing its returns."""
        episode_buffer.compute_returns(self.gamma)
        self.episodes.append(episode_buffer)

    def end_episode(self):
        """Finalize the current episode and start a new empty one."""
        self.current_episode.compute_returns(self.gamma)
        self.episodes.append(self.current_episode)
        self.current_episode = EpisodeBuffer()

    def get_expected_returns(self) -> float:
        """Return the mean initial return across all stored episodes."""
        expected_returns = []
        for ep in self.episodes:
            expected_returns.append(ep.returns[0])
        expected_returns = float(np.mean(expected_returns))
        return expected_returns

    def clear(self):
        """Remove all stored episodes and reset the active episode buffer."""
        self.episodes = []
        self.current_episode = EpisodeBuffer()




    def get_all_data(self):
        """Flatten all stored episodes into arrays for downstream training."""
        states = []
        actions = []
        returns = []
        jacobians = []

        for ep in self.episodes:
            for t, G in zip(ep.transitions, ep.returns):
                states.append(t.state)
                actions.append(t.policy_action)
                jacobians.append(t.jac_action_rlp)
                returns.append(G)

        return (
            np.array(states),
            np.array(actions),
            np.array(jacobians),
            np.array(returns)
        )
