"""Gymnasium environment for batch distillation control.

This module exposes :class:`BatchDistillationEnv`, a reinforcement-learning
environment that couples a high-fidelity do-mpc batch distillation simulator
with a discrete NARX state wrapper. The physical simulator provides the process
evolution and measured outputs, while the NARX simulator stores lagged
measurements and actions so that partially observed process data can be used as
Markovian observations.

The environment supports measurement noise, parametric uncertainty, optional
observation and action scaling, a fixed reward/termination definition, and
manual parameter setting for data generation or evaluation workflows.
"""

from dataclasses import dataclass
import gymnasium as gym
import numpy as np
import casadi as cd

from models.batchcol_model_dompc import template_model as batchcol_model_dompc
from models.batchcol_model_dompc import template_simulator as batchcol_simulator
from models.simulate_init_recipe import simulate_init_recipe
from narx_system_handler import NARX_model, NARX_simulator

@dataclass
class EnvConfig:
    """Configuration settings for :class:`BatchDistillationEnv`.

    Attributes
    ----------
    t_step : float
        Environment and simulator sampling time in seconds.
    n_history : int
        Number of previous transitions retained by the NARX observation model.
        The observation contains ``n_history + 1`` measurement vectors,
        ``n_history + 1`` action vectors, and the elapsed time state.
    meas_noise_bool : bool
        Whether stochastic measurement noise is injected into measured outputs.
    parametric_uncertainty_bool : bool
        Whether uncertain physical model parameters are sampled during rollouts.
    parametric_uncertainty_sampling_frequency : str
        Sampling mode for uncertain parameters. Supported values are
        ``"transition"`` for sampling before every step and ``"episode"`` for
        sampling once after each reset.
    scale_observations : bool
        Whether observations returned by the environment are linearly scaled
        with the configured observation bounds.
    rescale_actions : bool
        Whether external actions are interpreted as normalized values in
        ``[0, 1]`` and transformed to physical input bounds before simulation.
    enable_sensitivity : bool
        Whether the physical simulator factory also exposes state and algebraic
        sensitivities with respect to initial conditions and parameters.
    t_max : float
        Maximum episode duration in seconds. During environment initialization
        one additional ``t_step`` is added internally to align the terminal
        transition with the simulator time grid.
    seed : int
        Effective random seed stored by the environment. If no seed is supplied
        at construction time, one is sampled randomly.
    diverse_initial_conditions : bool
        Whether initial physical states, algebraic variables, and inputs are
        loaded from ``initial_condition_path`` and sampled per reset.
    initial_condition_path : str
        Path to a pickle file containing ``x_init``, ``z_init``, and ``u_init``
        arrays used when ``diverse_initial_conditions`` is enabled.
    """

    t_step: float = 30.0  # Time step for the environment in seconds
    n_history: int = 1 # Number of steps to consider for NARX models. This is used to convert the POMDP as a MDP.
    meas_noise_bool: bool = True  # Whether to add measurement noise
    parametric_uncertainty_bool: bool = True  # Whether to add parametric uncertainty
    parametric_uncertainty_sampling_frequency: str = "transition"  # Whether to sample new parameters at every transition or at the beginning of each episode
    scale_observations: bool = True  # Whether to scale the observations
    rescale_actions: bool = True  # Whether the actions are scaled
    enable_sensitivity: bool = False  # Whether to enable sensitivity analysis

    t_max: float = 3.0 * 3600.0  # Maximum time for an episode in seconds
    seed: int = None  # Random seed for reproducibility
    diverse_initial_conditions: bool = False  # Whether to use diverse initial conditions for training
    initial_condition_path: str = None


class BatchDistillationEnv(gym.Env):
    """Gymnasium environment for the batch distillation case study.

    The environment wraps a continuous-time do-mpc model of the batch
    distillation column and exposes a discrete Gymnasium interface. The
    physical simulator advances the plant, while an auxiliary NARX simulator
    stores filtered measurement and action histories as the RL observation.

    Actions are two-dimensional manipulated inputs. If
    ``settings.rescale_actions`` is true, callers should provide normalized
    actions in ``[0, 1]`` and the environment maps them to the physical bounds
    defined by ``lba`` and ``uba``. If it is false, actions are expected in
    physical units directly. Observations are the augmented NARX state and can
    be returned either scaled or unscaled depending on
    ``settings.scale_observations``.

    Attributes
    ----------
    settings : EnvConfig
        Runtime configuration.
    physical_system : do_mpc.simulator.Simulator
        High-fidelity physical simulator for the batch column.
    narx_system : NARX_simulator
        Discrete NARX simulator holding the observation history.
    action_space : gymnasium.spaces.Box
        External action space. It is normalized to ``[0, 1]`` regardless of
        whether actions are later rescaled internally.
    observation_space : gymnasium.spaces.Box
        Continuous observation space matching the NARX state dimension.
    reward_list : list[float]
        Rewards collected during the current episode.
    """

    def __init__(self, seed: int = None, config: dict = {}):
        """Initialize the environment and construct both simulator layers.

        Parameters
        ----------
        seed : int, optional
            Base seed for measurement noise, parameter uncertainty, and initial
            condition sampling. If omitted, a random seed in ``[0, 10000)`` is
            generated.
        config : dict, optional
            Keyword overrides for :class:`EnvConfig`.

        Notes
        -----
        The physical simulator is initialized first, followed by the NARX
        wrapper. Initial NARX states are generated by simulating the physical
        system for the configured history length and then resetting both
        simulator histories.
        """

        self.settings = EnvConfig(**config)
        self.settings.t_max += self.settings.t_step

        if seed is None:
            seed = np.random.randint(0, 10000)

        self.settings.seed = seed

        self.measurement_noise_rng = np.random.default_rng(seed)
        self.measurement_noise_std = np.array([0.025, 10, 0.00025, 0.0025, 0.18]).reshape(-1, 1)  # Standard deviation of measurement noise

        self.parametric_uncertainty_rng = np.random.default_rng(seed + 1)
        self.parametric_uncertainty_lb = np.array([-0.200, 0.40, 0.043]).reshape(-1, 1)
        self.parametric_uncertainty_ub = np.array([-0.100, 0.60, 0.055]).reshape(-1, 1)

        self.ic_selector_rng = np.random.default_rng(seed + 1)  # Random number generator for selecting initial conditions


        self.physical_system = self._setup_physical_system(initial_setup=True)
        self.narx_system = self._setup_narx_system(self.physical_system)
        self._initialize_narx_states()



        self.n_y = self.physical_system.model.y.shape[0]
        self.n_u = self.physical_system.model.u.shape[0]

        self.n_o = self.narx_system.model._x.shape[0]

        # Define action and observation spaces for RL
        self.action_space = gym.spaces.Box(low=0.0, high=1.0, shape=(self.n_u,), dtype=float)
        self.observation_space = gym.spaces.Box(low=-float('inf'), high=float('inf'), shape=(self.n_o,), dtype=float)

        self._prepare_bounds()

        self._prepare_measurement_scaling()
        self._prepare_action_scaling()
        self._prepare_observation_scaling()

        self.reward_list = []

    
    def _setup_physical_system(self, initial_setup: bool = False):
        """Create and initialize the high-fidelity physical simulator.

        Parameters
        ----------
        initial_setup : bool, optional
            If true, construct the underlying model, store nominal initial
            conditions, and optionally load diverse initial conditions from
            disk. On reset this is false so that the existing model instance is
            reused.

        Returns
        -------
        do_mpc.simulator.Simulator
            Configured simulator with initialized algebraic variables.
        """

        if initial_setup:
            self.model =  batchcol_model_dompc(self.settings.meas_noise_bool)

        self.physical_system = batchcol_simulator(self.model)

        self.physical_system.settings.t_step = self.settings.t_step
        self.physical_system.settings.integration_tool = "collocation"
        self.physical_system.settings.integration_opts = {
            "collocation_scheme": "radau",
            "number_of_finite_elements": 4,
            "interpolation_order":3,
            "rootfinder": "kinsol",
            "rootfinder_options": {
                "abstol": 1e-6,
                "use_preconditioner": True,
            },
        }

        self.physical_system.setup()
        if self.settings.enable_sensitivity:
            self.physical_system.simulator = self.physical_system.simulator.factory("simulator", ["x0", "z0", "p"], ["xf", "zf", "jac:xf:x0", "jac:xf:z0", "jac:xf:p", "jac:zf:x0", "jac:zf:z0", "jac:zf:p"])
        else:
            self.physical_system.simulator = self.physical_system.simulator.factory("simulator", ["x0", "z0", "p"], ["xf", "zf"])

        if initial_setup:
            self.x_init = self.physical_system.x0.master
            self.z_init = self.physical_system.z0.master
            self.u_init = self.physical_system.u0.master

            if self.settings.diverse_initial_conditions:
                # Load the initial conditions from a file and set them in the physical system
                import os, pickle
                with open(self.settings.initial_condition_path, "rb") as f:
                    initial_conditions = pickle.load(f)
                
                self.x_init = initial_conditions["x_init"]
                self.z_init = initial_conditions["z_init"]
                self.u_init = initial_conditions["u_init"]

        if self.settings.seed == 0:
            ic_idx = 0
        else:
            ic_idx = self.ic_selector_rng.integers(0, self.x_init.shape[1])


        if self.settings.diverse_initial_conditions:
            self.physical_system.x0 = self.x_init[:, ic_idx]
            self.physical_system.z0 = self.z_init[:, ic_idx]
            self.physical_system.u0 = self.u_init[:, ic_idx]

        self.physical_system.set_initial_guess()
        self.physical_system.init_algebraic_variables()

        return self.physical_system
    
    def _setup_narx_system(self, physical_system):
        """Create the NARX simulator used for augmented observations.

        Parameters
        ----------
        physical_system : do_mpc.simulator.Simulator
            Physical simulator whose model dimensions and sampling time define
            the NARX state and input layout.

        Returns
        -------
        NARX_simulator
            Configured discrete simulator for measurement/action histories.
        """

        narx_model = NARX_model(physical_system.model)

        narx_model.narx_settings.n_history = self.settings.n_history
        narx_model.narx_settings.EMA_alpha = np.array([0.4, 0.4, 0.4, 0.4, 0.4]).reshape(5, 1)

        narx_model.setup()

        narx_simulator = NARX_simulator(narx_model)
        narx_simulator.settings.t_step = physical_system.settings.t_step

        p_template = narx_simulator.get_p_template()
        p_template["delta_time"] = self.settings.t_step
        narx_simulator.set_p_fun(lambda t_now: p_template)

        narx_simulator.setup()

        return narx_simulator

    def _initialize_narx_states(self):
        """Warm-start the NARX state from physical simulator measurements.

        The current physical state is measured, optionally with noise, and used
        to populate the NARX history. The physical model is then simulated for
        ``n_history`` steps under the initial input so that the history contains
        consistent filtered measurements. Simulator data buffers are reset
        afterward to start the episode from a clean history.
        """

        x0 = self.physical_system.x0.master
        u0 = self.physical_system.u0.master
        z0 = self.physical_system.z0.master
        tvp0 = self.physical_system.tvp_fun(0).master
        p0 = self.physical_system.p_fun(0).master
        v0 = self.physical_system.model.v(0).master

        if self.settings.meas_noise_bool:
            v0 = self.physical_system.model.v(self.measurement_noise_rng.normal(0, self.measurement_noise_std, size = self.physical_system.model.y.shape)).master
            
        y_measured_0 = self.physical_system.model._meas_fun(x0, u0, z0, tvp0, p0, v0)

        self.narx_system.set_initial_guess(y_measured_0, u0)

        for idx in range(self.settings.n_history):
            if self.settings.meas_noise_bool:
                v0 = self.physical_system.model.v(self.measurement_noise_rng.normal(0, self.measurement_noise_std, size = self.physical_system.model.y.shape)).master

            y_measured = self.physical_system.make_step(u0=u0, v0 = v0)
            Y, U, num_time = self.narx_system.make_step(u0, y_measured)

        self.y_old = self.narx_system.get_current_filtered_measurement()
        self.y_old_no_noise = self.physical_system.model._meas_fun(self.physical_system.sim_x_num_unscaled, self.physical_system.u0, self.physical_system.sim_z_num_unscaled, self.physical_system.tvp_fun(0), self.physical_system.p_fun(0), self.physical_system.model._v(0)).full()
        self.a_old = u0.full().copy()

        self.physical_system.reset_history()
        self.narx_system.reset_history()

        self.narx_system.data.update(_y = self.y_old)
        return
    
    def _prepare_bounds(self):
        """Define physical measurement, action, and observation bounds.

        Measurement bounds are stored in ``lby``/``uby`` and action bounds in
        ``lba``/``uba``. The observation bounds ``lbo``/``ubo`` are assembled
        by stacking measurement and action bounds according to the NARX history
        length.
        """

        self.lby = np.array([30.0,    0.0, 0.85, 0.00, 26.85 + 273.15]).reshape(-1, 1)
        self.uby = np.array([60.0, 9000.0, 1.00, 1.00, 100 + 273.15]).reshape(-1, 1)

        self.lba = np.array([0.7, 3.0]).reshape(-1, 1)
        self.uba = np.array([1.0, 5.0]).reshape(-1, 1)

        self.lbo = np.concatenate([self.lby for _ in range(self.settings.n_history + 1)] + [self.lba for _ in range(self.settings.n_history)]).reshape(-1, 1)
        self.ubo = np.concatenate([self.uby for _ in range(self.settings.n_history + 1)] + [self.uba for _ in range(self.settings.n_history)]).reshape(-1, 1)

    def _sample_new_parameters(self):
        """Sample uncertain model parameters and reinitialize the plant state.

        The reflux-ratio error, Murphree efficiency, and nitrogen mole fraction
        are sampled from configured uniform ranges. A short initialization
        recipe is simulated with the sampled values, and the resulting
        consistent state, algebraic variables, inputs, and dependent parameters
        are copied back into the physical simulator.
        """

        p_template = self.physical_system.p_fun(0)
        parametric_noise = self.parametric_uncertainty_rng.uniform(self.parametric_uncertainty_lb, self.parametric_uncertainty_ub)
        rr_err = parametric_noise[0, 0]
        E_murphree = parametric_noise[1, 0] 
        xN2 = parametric_noise[2, 0]
        p_template["e0_rr_err"] = parametric_noise[0, 0]
        p_template["e0_E_murphree"] = parametric_noise[1, 0]
        p_template["e0_x_N2"] = parametric_noise[2, 0]
        self.physical_system.set_p_fun(lambda t_now: p_template)

        homo_res = simulate_init_recipe(
            E_murphree=E_murphree,
            rr_err=rr_err,
            x_N2 = xN2,
            h_tot = 0.179372959955645,
            h_weir= 0.04326133478330423,
            kappa = 0.0424670248823593,
            LI=self.physical_system.sim_z_num_unscaled["_z", "e0_LI"],
            w_L_B_c1=self.physical_system.sim_z_num_unscaled["_z", "e0_w_L_B_c1"],
            t_settle = 300,
        )


        x_idx = {}
        for key in self.physical_system.x0.keys():
            x_idx[key] = [idx for idx, lkey in enumerate(homo_res["x_labels"]) if lkey == key][0]
        for key in self.physical_system.x0.keys():
            self.physical_system.x0[key] = cd.DM(homo_res["x_unscaled"][x_idx[key], -1])

        z_idx = {}
        for key in self.physical_system.z0.keys()[1:]:
            z_idx[key] = [idx for idx, lkey in enumerate(homo_res["z_labels"]) if lkey == key][0]
        for key in self.physical_system.z0.keys()[1:]:
            self.physical_system.z0[key] = cd.DM(homo_res["z_unscaled"][z_idx[key], -1])

        u_idx = {}
        for key in self.physical_system.u0.keys()[1:]:
            u_idx[key] = [idx for idx, lkey in enumerate(homo_res["u_labels"]) if lkey == key][0]
        for key in self.physical_system.u0.keys()[1:]:
            self.physical_system.u0[key] = cd.DM(homo_res["u"][u_idx[key], -1])


        p_idx = {}
        for key in self.physical_system.p_fun(0).keys()[1:]:
            if key in homo_res["u_labels"]:
                p_idx[key] = [idx for idx, lkey in enumerate(homo_res["u_labels"]) if lkey == key][0]
        
        p_template = self.physical_system.p_fun(0)
        for key in self.physical_system.p_fun(0).keys()[1:]:
            if key in homo_res["u_labels"]:
                p_template[key] = homo_res["u"][p_idx[key], -1]

        self.physical_system.set_p_fun(lambda t: p_template)


        self.physical_system.set_initial_guess()
        self.physical_system.init_algebraic_variables()

    def set_new_parameters(
        self,
        rr_err: float,
        E_murphree: float,
        xN2: float,
        h_tot: float = 0.19750085122346095,
        h_weir: float = 0.03999668977987875,
        kappa: float = 0.08374466568559812,
        ):
        """Set physical model parameters and recompute consistent initials.

        Parameters
        ----------
        rr_err : float
            Reflux-ratio actuator error.
        E_murphree : float
            Murphree tray efficiency.
        xN2 : float
            Nitrogen mole fraction parameter.
        h_tot : float, optional
            Total tray holdup or geometric holdup parameter.
        h_weir : float, optional
            Tray weir height.
        kappa : float, optional
            Hydrodynamic parameter used by the initialization recipe.

        Notes
        -----
        This method is intended for deterministic evaluation and data
        generation. It updates the simulator parameter function and then runs
        the initialization recipe so that states and algebraic variables remain
        consistent with the new parameter set.
        """

        p_template = self.physical_system.p_fun(0)
        p_template["e0_rr_err"] = rr_err
        p_template["e0_E_murphree"] = E_murphree
        p_template["e0_x_N2"] = xN2
        p_template["e0_h_tot"] = h_tot
        p_template["e0_h_weir"] = h_weir
        p_template["e0_greek_kappa"] = kappa

        self.physical_system.set_p_fun(lambda t_now: p_template)

        homo_res = simulate_init_recipe(
            E_murphree=E_murphree,
            rr_err=rr_err,
            x_N2 = xN2,
            h_tot=h_tot,
            h_weir=h_weir,
            kappa=kappa,
            LI=self.physical_system.sim_z_num_unscaled["_z", "e0_LI"],
            w_L_B_c1=self.physical_system.sim_z_num_unscaled["_z", "e0_w_L_B_c1"],
            t_settle = 300,
        )


        x_idx = {}
        for key in self.physical_system.x0.keys():
            x_idx[key] = [idx for idx, lkey in enumerate(homo_res["x_labels"]) if lkey == key][0]
        for key in self.physical_system.x0.keys():
            self.physical_system.x0[key] = cd.DM(homo_res["x_unscaled"][x_idx[key], -1])

        z_idx = {}
        for key in self.physical_system.z0.keys()[1:]:
            z_idx[key] = [idx for idx, lkey in enumerate(homo_res["z_labels"]) if lkey == key][0]
        for key in self.physical_system.z0.keys()[1:]:
            self.physical_system.z0[key] = cd.DM(homo_res["z_unscaled"][z_idx[key], -1])

        u_idx = {}
        for key in self.physical_system.u0.keys()[1:]:
            u_idx[key] = [idx for idx, lkey in enumerate(homo_res["u_labels"]) if lkey == key][0]
        for key in self.physical_system.u0.keys()[1:]:
            self.physical_system.u0[key] = cd.DM(homo_res["u"][u_idx[key], -1])


        p_idx = {}
        for key in self.physical_system.p_fun(0).keys()[1:]:
            if key in homo_res["u_labels"]:
                p_idx[key] = [idx for idx, lkey in enumerate(homo_res["u_labels"]) if lkey == key][0]
        
        p_template = self.physical_system.p_fun(0)
        for key in self.physical_system.p_fun(0).keys()[1:]:
            if key in homo_res["u_labels"]:
                p_template[key] = homo_res["u"][p_idx[key], -1]

        self.physical_system.set_p_fun(lambda t: p_template)


        self.physical_system.set_initial_guess()
        self.physical_system.init_algebraic_variables()
        pass
    


    def _prepare_measurement_scaling(self):
        """Prepare affine scaling coefficients for measured outputs."""

        y_scale = 1 / (self.uby - self.lby)
        y_min = - self.lby * y_scale

        self.y_scale = y_scale
        self.y_min = y_min
    
    def _prepare_action_scaling(self):
        """Prepare affine scaling coefficients for manipulated inputs."""

        u_scale = 1 / (self.uba - self.lba)
        u_min = - self.lba * u_scale

        if u_scale.ndim >= 2:
            u_scale = u_scale.flatten()
        if u_min.ndim >= 2:
            u_min = u_min.flatten()

        self.u_scale = u_scale
        self.u_min = u_min

    def _prepare_observation_scaling(self):
        """Prepare affine scaling coefficients for NARX observations."""

        o_scale = 1 / (self.ubo - self.lbo)
        o_min = - self.lbo * o_scale

        self.o_scale = o_scale
        self.o_min = o_min

    def step(self, action: np.ndarray) -> tuple[np.ndarray, float, bool, bool, dict]:
        """Advance the environment by one control interval.

        Parameters
        ----------
        action : numpy.ndarray or casadi.DM
            External action. If ``settings.rescale_actions`` is true, the
            action is interpreted in normalized coordinates and mapped to
            physical bounds before simulation. Otherwise it is used directly in
            physical coordinates.

        Returns
        -------
        observation : numpy.ndarray
            Next NARX observation, scaled if ``settings.scale_observations`` is
            true.
        reward : float
            Scalar reward computed by the batch-distillation reward definition.
        terminated : bool
            Whether the episode reached a terminal process condition.
        truncated : bool
            Whether the episode ended because the configured time limit was
            reached.
        info : dict
            Auxiliary information dictionary. Currently empty.
        """

        info = {}

        if isinstance(action, cd.DM):
            action = action.full()

        if self.settings.rescale_actions:
            action = self._inverse_scale_action(action)

        if action.ndim == 1 and action.shape[0] == self.n_u:
            action = action.reshape((self.n_u, 1))


        # Integrate the system
        measurement_noise = self.measurement_noise_rng.normal(loc = np.zeros(self.measurement_noise_std.shape), scale = self.measurement_noise_std)
        measurement_noise = self.physical_system.model._v(measurement_noise).master
        additive_process_noise = self.physical_system.model._w(0)

        if self.settings.parametric_uncertainty_bool and self.settings.parametric_uncertainty_sampling_frequency == "transition":
            self._sample_new_parameters()

        self.physical_system.u0 = action
        sim_p_num = cd.vertcat(action, self.physical_system.p_fun(0).master, self.physical_system.tvp_fun(0).master)
        min_alg_error = cd.Function("alg", [self.physical_system.dae["x"], self.physical_system.dae["z"], self.physical_system.dae["p"]], [self.physical_system.dae["alg"]])(self.physical_system.sim_x_num, self.physical_system.sim_z_num, sim_p_num).full().min()
        max_alg_error = cd.Function("alg", [self.physical_system.dae["x"], self.physical_system.dae["z"], self.physical_system.dae["p"]], [self.physical_system.dae["alg"]])(self.physical_system.sim_x_num, self.physical_system.sim_z_num, sim_p_num).full().max()
        alg_error = max(abs(min_alg_error), abs(max_alg_error))
        if alg_error > 1e-6:
            self.physical_system.init_algebraic_variables()

        y_next = self.physical_system.make_step(u0 = action, v0 = measurement_noise, w0 = additive_process_noise)
        Y, U, num_time = self.narx_system.make_step(u_physical=action, y_physical_measured=y_next)

        y_next = self.narx_system.get_current_filtered_measurement()
        y_next_no_noise = self.physical_system.model._meas_fun(self.physical_system.sim_x_num_unscaled, self.physical_system.u0, self.physical_system.sim_z_num_unscaled, self.physical_system.tvp_fun(0), self.physical_system.p_fun(0), self.physical_system.model._v(0)).full()

        observation = self.get_observation()


        # Check if the sytsem should be terminated or truncated
        terminated, truncated = self._done_check(y_old = self.y_old, a_old = self.a_old, y_next = y_next, action = action)

        # Compute the reward
        reward = self._get_reward(y_old = self.y_old, a_old = self.a_old, y_next = y_next, action = action, terminated=terminated, truncated=truncated)
        self.reward_list.append(reward)        
        


        self.y_old = y_next.copy()
        self.y_old_no_noise = y_next_no_noise.copy()
        self.a_old = action.copy()
        
        return observation, reward, terminated, truncated, info
    
    def get_measurement(self) -> np.ndarray:
        """Return the current physical measurement.

        Returns
        -------
        numpy.ndarray
            Current measured output of the physical simulator, optionally with
            measurement noise.

        Notes
        -----
        This method contains legacy EMA references (``y_deque`` and
        ``ema_alpha``) that are not initialized in this class. The NARX
        simulator is the active filtering path used by :meth:`step`.
        """

        v = self.physical_system.model._v(0)
        if self.settings.meas_noise_bool:
            v = self.measurement_noise_rng.normal(loc = np.zeros((self.n_y,)), scale = self.measurement_noise_std)
        y_meas = self.physical_system.model._meas_fun(self.physical_system.sim_x_num_unscaled, self.physical_system.u0, self.physical_system.sim_z_num_unscaled, self.physical_system.tvp_fun(0), self.physical_system.p_fun(0), v)
        y_meas = y_meas.full()
        # NOTE: Maybe I need to add a truncation to the measurements here to avoid unphysical values
        if len(self.y_deque) > 0:
            y_meas = (1 - self.ema_alpha) * self.y_deque[-1] + self.ema_alpha * y_meas
        return y_meas
    
    def get_observation(self) -> np.ndarray:
        """Return the current NARX observation.

        Returns
        -------
        numpy.ndarray
            Augmented NARX state containing measurement history, action
            history, and elapsed time. The returned values are scaled if
            ``settings.scale_observations`` is true.
        """

        observation = self.narx_system.x0.master.full()
        if self.settings.scale_observations:
            observation = self._scale_observation(observation)
        return observation
    
    def get_old_action(self) -> np.ndarray:
        """Return the most recent physical input in external action coordinates.

        Returns
        -------
        numpy.ndarray
            Last applied action, normalized if ``settings.rescale_actions`` is
            true and physical otherwise.
        """

        u_old = self.physical_system.u0.master.full()
        if self.settings.rescale_actions:
            u_old = self._scale_action(u_old)
        return u_old.flatten()

    def _scale_observation(self, o: np.ndarray) -> np.ndarray:
        """Map an observation from physical coordinates to scaled coordinates.

        Parameters
        ----------
        o : numpy.ndarray
            Observation vector with shape ``(n_o,)`` or ``(n_o, 1)``.

        Returns
        -------
        numpy.ndarray
            Scaled observation with the same shape as the input.
        """

        original_shape = o.shape
        if o.ndim == 2 and o.shape[1] == 1:
            o = o.flatten()
        o_scaled = o * self.o_scale + self.o_min
        o_scaled = o_scaled.reshape(original_shape)
        return o_scaled

    def _scale_measurement(self, y: np.ndarray) -> np.ndarray:
        """Map measured outputs from physical coordinates to scaled values.

        Parameters
        ----------
        y : numpy.ndarray
            Measurement vector with shape ``(n_y,)`` or ``(n_y, 1)``.

        Returns
        -------
        numpy.ndarray
            Scaled measurement with the same shape as the input.
        """

        original_shape = y.shape
        if y.ndim == 2 and y.shape[1] == 1:
            y = y.flatten()
        y_scaled = y * self.y_scale + self.y_min
        y_scaled = y_scaled.reshape(original_shape)
        return y_scaled
    
    def _scale_action(self, u: np.ndarray) -> np.ndarray:
        """Map a physical action to normalized external action coordinates.

        Parameters
        ----------
        u : numpy.ndarray or casadi.DM
            Physical action vector.

        Returns
        -------
        numpy.ndarray
            Scaled action with the same shape convention as the input.
        """

        if isinstance(u, cd.DM):
            u = u.full()
        original_shape = u.shape
        if u.ndim == 2 and u.shape[1] == 1:
            u = u.T
        u_scaled = u * self.u_scale.T + self.u_min.T
        u_scaled = u_scaled.reshape(original_shape)
        return u_scaled
    
    def _inverse_scale_action(self, u_scaled: np.ndarray) -> np.ndarray:
        """Map a normalized action to physical input coordinates.

        Parameters
        ----------
        u_scaled : numpy.ndarray
            Action in normalized external coordinates.

        Returns
        -------
        numpy.ndarray
            Physical action with the same shape convention as the input.
        """

        original_shape = u_scaled.shape
        if u_scaled.ndim == 2 and u_scaled.shape[1] == 1:
            u_scaled = u_scaled.flatten()
        u = (u_scaled - self.u_min) / self.u_scale
        u = u.reshape(original_shape)
        return u
    
    def _get_reward(self, y_old: np.ndarray, a_old: np.ndarray, y_next: np.ndarray, action: np.ndarray, terminated: bool, truncated: bool) -> float:
        """Compute the reward for one transition.

        Parameters
        ----------
        y_old : numpy.ndarray
            Filtered measurement before applying ``action``.
        a_old : numpy.ndarray
            Previously applied physical action.
        y_next : numpy.ndarray
            Filtered measurement after applying ``action``.
        action : numpy.ndarray
            Current physical action.
        terminated : bool
            Whether the transition ends the episode through a terminal process
            condition.
        truncated : bool
            Whether the transition ends the episode through time-limit
            truncation.

        Returns
        -------
        float
            Transition reward.

        Notes
        -----
        The reward combines an action-move penalty, a distillate-mass
        incentive, state-bound penalties, and terminal corrections. The
        action-move penalty is currently configured with a zero-valued weight
        matrix.
        """

        reward = 0.0

        # Penalize large steps in action
        delta_a = action - a_old
        R_mat = np.diag([0.0, 0.0])
        action_penalty = delta_a.T @ R_mat @ delta_a

        reward -= float(action_penalty[0, 0])


        # Reward for a high distillate mass
        product_index = 1  # Index of distillate mass in the measurement vector
        distillate_mass = float(y_old[product_index, 0])

        target_mass = 6e3
        reward += min(distillate_mass, target_mass) * 1e-3


        penalty_weight_state = np.array([1e4, 0.0, 1e3, 1e4, 1e4]).reshape(-1, 1)
        state_violation_lower = np.maximum(self.lby - y_old, 0.0).reshape(-1, 1)
        state_violation_upper = np.maximum(y_old - self.uby, 0.0).reshape(-1, 1)
        state_penalty = penalty_weight_state.T @ (state_violation_lower + state_violation_upper)

        penalty = max(float(state_penalty[0, 0]), 0.0)

        reward -= penalty

        if terminated:
            reward += min(distillate_mass, target_mass) * 1e-3 * (self.settings.t_max - self.physical_system.t0[0]) / self.settings.t_step
            reward -= 1 * penalty  * (self.settings.t_max - self.physical_system.t0[0]) / self.settings.t_step

        if self.settings.t_max - self.physical_system.t0 < self.settings.t_step:
            reward -= ((distillate_mass - target_mass) * 1e-3) ** 2

        return reward

    def _done_check(self, y_old: np.ndarray, a_old: np.ndarray, y_next: np.ndarray, action: np.ndarray) -> tuple[bool, bool]:
        """Evaluate Gymnasium termination and truncation flags.

        Parameters
        ----------
        y_old : numpy.ndarray
            Filtered measurement before the current transition.
        a_old : numpy.ndarray
            Previous physical action. Present for signature symmetry with the
            reward function and future termination variants.
        y_next : numpy.ndarray
            Filtered measurement after the current transition. Present for
            future termination variants.
        action : numpy.ndarray
            Current physical action. Present for future termination variants.

        Returns
        -------
        terminated : bool
            True if the episode should end because product specifications,
            purity constraints, or the time limit are reached.
        truncated : bool
            True if the configured time limit is reached.
        """

        terminated = False
        truncated = False

        if y_old.ndim == 2 and y_old.shape[1] == 1:
            y_old = y_old.flatten()

        # Check if an episode is too long
        if self.physical_system.t0 >= self.settings.t_max:
            terminated = True
            truncated = True
            return terminated, truncated

        product_idx = 1
        product_purity_idx = 2

        distillate_mass = y_old[product_idx]
        distillate_purity = y_old[product_purity_idx]

        target_distillate_mass = 6000.0  # grams

        # Terminate if distillate purity drops significantly.
        if distillate_purity < 0.83:
            terminated = True
            return terminated, truncated
        
        if distillate_mass > target_distillate_mass and not truncated:
            terminated = True
            
        return terminated, truncated

    def reset(self, seed: int = None) -> tuple[np.ndarray, dict]:
        """Reset the environment to the start of a new episode.

        Parameters
        ----------
        seed : int, optional
            New seed for all environment random number generators. If omitted,
            the existing generators continue from their current state.

        Returns
        -------
        observation : numpy.ndarray
            Initial NARX observation for the new episode.
        info : dict
            Auxiliary information dictionary. Currently empty.

        Notes
        -----
        Reset reconstructs the physical and NARX simulators, reinitializes the
        NARX history, and clears ``reward_list``. If episode-level parametric
        uncertainty is enabled, new parameters are sampled after the initial
        observation is generated.
        """

        info = {}

        if seed is not None:
            self.measurement_noise_rng = np.random.default_rng(seed)
            self.parametric_uncertainty_rng = np.random.default_rng(seed + 1)
            self.ic_selector_rng = np.random.default_rng(seed + 1)
            self.settings.seed = seed

        self.physical_system = self._setup_physical_system(initial_setup = False)
        self.narx_system = self._setup_narx_system(self.physical_system)
        self._initialize_narx_states()
        
        observation = self.get_observation()

        if self.settings.parametric_uncertainty_bool and self.settings.parametric_uncertainty_sampling_frequency == "episode":
            self._sample_new_parameters()

        self.reward_list = []
        
        return observation, info
    
if __name__ == "__main__":
    import os
    config = {
        "t_step": 120.0,
        "n_history": 0,
        "scale_observations": False,
        "rescale_actions": True,
        "diverse_initial_conditions": True,
        "initial_condition_path": os.path.join("data", "LVcolumn_DAE_init", "IC_sample_1000_cleaned.pkl"),
        "parametric_uncertainty_bool": True,
        "parametric_uncertainty_sampling_frequency": "episode",
    }
    
    env = BatchDistillationEnv(config=config)
    observation, _ = env.reset(seed = 99)

    from tqdm import trange
    for i in trange(100):
        observation, reward, done, truncated, info = env.step(env.action_space.sample())

    print("Success!")
