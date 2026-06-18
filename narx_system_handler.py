"""Nonlinear AutoRegressive with eXogenous inputs (NARX) model and simulator.

This module provides a NARX representation built on top of the
do-mpc framework. Lagged measurements and control inputs are maintained as
explicit state variables, enabling their use within an NMPC formulation.
An optional exponential moving average (EMA) filter is applied to incoming
measurements before they enter the state history.
"""

from do_mpc.model import Model
from do_mpc.simulator import Simulator
from dataclasses import dataclass, field
import casadi as cd

@dataclass
class NARXSettings:
    """Configuration settings for the NARX model.

    Attributes
    ----------
    n_history : int
        Number of past time steps retained as lagged state variables.
        A value of ``0`` means only the current measurement is stored,
        i.e., no history beyond the present step is maintained.
        Default is ``0``.
    EMA_alpha : list of float
        Per-measurement smoothing factors for the exponential moving average
        filter applied to incoming measurements. Each element must lie in
        ``[0, 1]``, where ``1.0`` corresponds to no filtering (pass-through)
        and smaller values increase smoothing. The list length must match the
        number of measurements of the physical model; if not, all factors are
        reset to ``1.0`` with a warning. Default is ``[1.0]``.
    """

    n_history: int = 0
    EMA_alpha: list = field(default_factory=lambda: [1.0])

class NARX_model(Model):
    """NARX model built on the do-mpc ``Model`` base class.

    Constructs a discrete-time augmented NARX representation in which lagged
    measurements and control inputs are explicit state variables. The model
    structure is derived from a physical do-mpc model and must be finalised
    by calling :meth:`setup` before use.

    After :meth:`setup` is called, the reference to the physical model is
    removed. All subsequent access to the NARX state decomposition is provided
    through the CasADi function ``split_narx_states``.

    Attributes
    ----------
    narx_settings : NARXSettings
        Settings controlling the history length and EMA filter coefficients.
        Must be configured before calling :meth:`setup`.
    split_narx_states : casadi.Function
        CasADi function with signature ``(x) -> (Y, U, num_time)`` that
        decomposes the augmented state vector into the measurement history
        ``Y``, the control input history ``U``, and the elapsed time
        ``num_time``. Available after :meth:`setup` is called.
    """

    def __init__(self, physical_model: Model):
        """Initialise the NARX model from a physical do-mpc model.

        Parameters
        ----------
        physical_model : Model
            A configured do-mpc ``Model`` instance providing the measurement
            and control input dimensions as well as the symbolic variable type.
            The model need not be set up prior to passing it here.
        """
        super().__init__(model_type = "discrete", symvar_type = physical_model.symvar_type)

        self.narx_settings = NARXSettings()

        self.physical_model = physical_model


    def setup(self):
        """Construct the augmented NARX state-space representation.

        Registers lagged measurement and control input states, defines their
        shift-register dynamics, applies the EMA filter to the most recent
        measurement lag, and exposes a time counter as an additional state.
        Finalises the model by calling the parent ``setup`` method and
        constructs the ``split_narx_states`` CasADi function for state
        decomposition.

        If the length of ``narx_settings.EMA_alpha`` does not match the
        number of measurements in the physical model, all smoothing factors
        are reset to ``1.0`` and a warning is printed.

        Notes
        -----
        This method deletes the reference to the physical model upon
        completion. Reconfiguring and re-calling :meth:`setup` is therefore
        not supported without reinstantiating the object.
        """

        if len(self.narx_settings.EMA_alpha) != self.physical_model.y.shape[0]:
            print("Warning: Length of EMA_alpha does not match number of measurements. Using default value of 1.0 for all measurements.")
            self.narx_settings.EMA_alpha = [1.0 for _ in range(self.physical_model.y.shape[0])]

        # First create the history of the measurements
        Y = []
        for idx in range(self.narx_settings.n_history + 1):
            y_list = []
            for y in cd.vertsplit(self.physical_model.y):
                y_loc = self.set_variable(var_type = '_x', var_name = f"{y.name()}_lag{self.narx_settings.n_history - idx}")
                y_list.append(y_loc)
            Y.append(y_list)

        for measurement in Y[-1]:
            self.set_meas(meas_name=measurement.name(), expr = measurement)

        # Second create the history of the control inputs
        U = []
        for idx in range(self.narx_settings.n_history + 1): # NOTE that we add this +1 because we penalize the delta u term.
            u_list = []
            for u in cd.vertsplit(self.physical_model.u):
                u_loc = self.set_variable(var_type = '_x', var_name = f"{u.name()}_lag{self.narx_settings.n_history - idx}")
                u_list.append(u_loc)
            U.append(u_list)

        # Define the actual control action
        u_list = []
        for u in cd.vertsplit(self.physical_model.u):
            u_loc = self.set_variable(var_type = '_u', var_name = f"{u.name()}")
            u_list.append(u_loc)

        # Define the current measurement that comes from the physical system as a control input
        y_measured = []
        for y in cd.vertsplit(self.physical_model.y):
            y_loc = self.set_variable(var_type = '_u', var_name = f"{y.name()}_measured")
            y_measured.append(y_loc)

        # Define the dynamics of the history states
        for y_past, y_next in zip(Y[:-1], Y[1:]):
            for y_i_past, y_i_next in zip(y_past, y_next):
                self.set_rhs(var_name = y_i_past.name(), expr = y_i_next)
        
        # Define the dynamics of the current state
        for y_i_past, y_i_meas, alpha in zip(Y[-1], y_measured, self.narx_settings.EMA_alpha):
            expr = (1 - alpha) * y_i_past + alpha * y_i_meas
            self.set_rhs(var_name = y_i_past.name(), expr = expr)

        # Define the dynamics of the control input history states
        for u_past, u_next in zip(U[:-1], U[1:]):
            for u_i_past, u_i_next in zip(u_past, u_next):
                self.set_rhs(var_name = u_i_past.name(), expr = u_i_next)

        # The current control input remains the same
        if len(U) > 0:
            for u_i_past, u_i_next in zip(U[-1], u_list):
                self.set_rhs(var_name = u_i_past.name(), expr = u_i_next)

        num_time = self.set_variable(var_type = '_x', var_name = "num_time", shape = (1, 1))
        self.set_variable(var_type = "_p", var_name = "delta_time", shape = (1, 1))
        self.set_rhs(var_name = "num_time", expr = self.x["num_time"] + self.p["delta_time"])

        super().setup()

        Y_history = cd.vertcat(*[cd.vertcat(*y_list) for y_list in Y])
        U_history = cd.vertcat(*[cd.vertcat(*u_list) for u_list in U])

        self.split_narx_states = cd.Function('split_narx_states', [self.x], [Y_history, U_history, num_time], ['x'], ['Y', 'U', 'num_time'])

        delattr(self, "physical_model")
        return 
        
class NARX_simulator(Simulator):
    """NARX simulator built on the do-mpc ``Simulator`` base class.

    Wraps the do-mpc ``Simulator`` to handle the augmented NARX input
    convention, in which the physical control input and the current
    measurement are concatenated before being passed to the base simulator.
    Provides convenience methods for state initialisation and filtered
    measurement retrieval.
    """

    def make_step(self, u_physical: cd.DM, y_physical_measured: cd.DM):
        """Advance the NARX simulator by one time step.

        Concatenates the physical control input and the current measurement
        into the augmented NARX input vector, delegates to the parent
        ``make_step``, and returns the decomposed state history.

        Parameters
        ----------
        u_physical : cd.DM
            Physical control input at the current time step,
            shape ``(n_inputs, 1)``.
        y_physical_measured : cd.DM
            Measured output of the physical system at the current time step,
            shape ``(n_measurements, 1)``.

        Returns
        -------
        Y : cd.DM
            Stacked measurement history over ``n_history + 1`` steps,
            shape ``((n_history + 1) * n_measurements, 1)``.
        U : cd.DM
            Stacked control input history over ``n_history + 1`` steps,
            shape ``((n_history + 1) * n_inputs, 1)``.
        num_time : cd.DM
            Elapsed simulation time, shape ``(1, 1)``.
        """

        # Perform the simulation step
        u_narx = cd.vertcat(u_physical, y_physical_measured)
        s = super().make_step(u_narx)

        Y, U, num_time = self.model.split_narx_states(self.x0)

        return Y, U, num_time
    
    def get_current_filtered_measurement(self) -> cd.DM:
        """Return the EMA-filtered measurement at the current time step.

        Evaluates the do-mpc measurement function at the current state,
        applying the EMA filter defined by ``narx_settings.EMA_alpha``.

        Returns
        -------
        cd.DM
            Filtered measurement vector, shape ``(n_measurements, 1)``.
        """
        y_now = self.model._meas_fun(self.x0, self.u0, self.z0, self.tvp_fun(0), self.p_fun(0), 0).full()
        return y_now
    
    def set_initial_guess(self, y_measured: cd.DM, u: cd.DM) -> None:
        """Initialise the augmented state vector from a steady-state guess.

        Populates the full measurement and control input history by repeating
        the provided values across all ``n_history + 1`` lag positions and
        sets the elapsed time to zero.

        Parameters
        ----------
        y_measured : cd.DM
            Initial measurement vector, shape ``(n_measurements, 1)``.
            Replicated across all history positions.
        u : cd.DM
            Initial control input vector, shape ``(n_inputs, 1)``.
            Replicated across all history positions.
        """

        Y = cd.vertcat(*[y_measured for _ in range(self.model.narx_settings.n_history + 1)])
        U = cd.vertcat(*[u for _ in range(self.model.narx_settings.n_history + 1)])

        x0 = cd.vertcat(Y, U, 0.0)

        self.x0.master = x0

        return

if __name__ == "__main__":
    from models.batchcol_model_dompc import template_model

    physical_model = template_model(meas_noise = False)
    narx_model = NARX_model(physical_model)

    narx_model.narx_settings.n_history = 5
    narx_model.narx_settings.EMA_alpha = [0.1 for _ in range(physical_model.y.shape[0])]

    narx_model.setup()

    narx_simulator = NARX_simulator(narx_model)
    narx_simulator.settings.t_step = 30.0
    narx_simulator.setup()

    from numpy.random import default_rng
    rng = default_rng(1234)

    u_0 = cd.DM([[350.0], [350.0]])
    y_measured_0 = cd.DM([[0.9], [273.15 + 60.0]])

    narx_simulator.set_initial_guess(y_measured_0, u_0)

    for idx in range (10):
        u = u_0 + rng.normal(0, 5.0, size = u_0.shape)
        y = y_measured_0 + rng.normal(cd.DM.zeros(cd.DM([[0.9], [273.15 + 60.0]]).shape), cd.DM([[0.9], [273.15 + 60.0]]) * 0.1, size = y_measured_0.shape)

        print("===================================")
        print(f"Step {idx + 1}:")
        print(f"  Input u: {u.T}")
        print(f"  Measured y: {y.T}")

        Y_history, U_history, num_time = narx_simulator.make_step(u, y)

        print(f"  Y history: {Y_history.T}")
        print(f"  U history: {U_history.T}")
        print()