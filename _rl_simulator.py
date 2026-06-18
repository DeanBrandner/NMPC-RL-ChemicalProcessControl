# This file contains code derived from do-mpc.
# do-mpc is licensed under the GNU Lesser General Public License v3.0.
# Modifications Copyright (C) 2026 Dean Brandner.
#
# This file is licensed under the GNU Lesser General Public License v3.0.

"""Simulator extensions that propagate reinforcement-learning parameters.

This module extends do-mpc's simulator with support for the ``_rlp``
parameter namespace used by reinforcement-learning-aware models. It keeps the
standard ``_tvp`` and ``_p`` handling intact and adds a matching callback for
RL-specific symbolic parameters.
"""

from do_mpc.simulator import Simulator
import casadi.tools as castools
import numpy as np
from do_mpc import CASADI_LEGACY_MODE

from RL_MPC import RL_MPC_Data

class RL_Simulator(Simulator):
    """do-mpc simulator variant with reinforcement-learning parameter support."""

    def __init__(self, model):
        """Initialize the simulator and add bookkeeping for RL parameters."""
        super().__init__(model)
        self.data = RL_MPC_Data(model)
        self.flags.update({
            'set_rlp_fun': False,
        })

    def _check_validity(self):
        """Validate that all required parameter callbacks are available.

        In addition to do-mpc's ``_tvp`` and ``_p`` callbacks, this simulator
        requires an ``_rlp`` callback whenever the model exposes reinforcement-
        learning parameters. If a callback is missing and the corresponding
        structure is unused, a constant template callback is installed.
        """
        # tvp_fun must be set, if tvp are defined in model.
        if self.flags['set_tvp_fun'] == False and self.model._tvp.size > 0:
            raise Exception('You have not supplied a function to obtain the time-varying parameters defined in model. Use .set_tvp_fun() prior to setup.')
        # p_fun must be set, if p are defined in model.
        if self.flags['set_p_fun'] == False and self.model._p.size > 0:
            raise Exception('You have not supplied a function to obtain the parameters defined in model. Use .set_p_fun() prior to setup.')
        if self.flags['set_rlp_fun'] == False and self.model._rlp.size > 0:
            raise Exception('You have not supplied a function to obtain the RL parameters defined in model. Use .set_rlp_fun() prior to setup.')

        # Set dummy functions for tvp and p in case these parameters are unused.
        if not self.flags['set_tvp_fun']:
            _tvp = self.get_tvp_template()
            def tvp_fun(t): return _tvp
            self.set_tvp_fun(tvp_fun)

        if not self.flags['set_p_fun']:
            _p = self.get_p_template()
            def p_fun(t): return _p
            self.set_p_fun(p_fun)

        if not self.flags['set_rlp_fun']:
            _rlp = self.get_rlp_template()
            def rlp_fun(t): return _rlp
            self.set_rlp_fun(rlp_fun)

        self._settings.check_for_mandatory_settings()

    def get_rlp_template(self):
        """Return the reinforcement-learning parameter template structure."""
        return self.model._rlp(0)
    
    def set_rlp_fun(self, rlp_fun):
        """Register the callback that provides RL parameters over time.

        Parameters
        ----------
        rlp_fun : callable
            Function taking the current time ``t`` and returning a CasADi
            ``DMStruct`` with the exact labels and shape of ``model._rlp(0)``.
        """
        assert isinstance(rlp_fun(0), castools.structure3.DMStruct), 'p_fun has incorrect return type.'
        assert self.get_rlp_template().labels() == rlp_fun(0).labels(), 'Incorrect output of p_fun. Use get_p_template to obtain the required structure.'
        self.rlp_fun = rlp_fun
        self.flags['set_rlp_fun'] = True

    def setup(self)->None:
        """Sets up the simulator and finalizes the simulator configuration.
        Only after the setup, the :py:func:`make_step` method becomes available.

        Raises:
            assertion: t_step must be set
        """

        self._check_validity()

        self.sim_x = sim_x =  self.model.sv.sym_struct([
            castools.entry('_x', struct=self.model._x)
            ])
        self.sim_z = sim_z =  self.model.sv.sym_struct([
            castools.entry('_z', struct=self.model._z)
            ])

        self.sim_p = sim_p = self.model.sv.sym_struct([
            castools.entry('_u', struct=self.model._u),
            castools.entry('_p', struct=self.model._p),
            castools.entry('_tvp', struct=self.model._tvp),
            castools.entry('_rlp', struct=self.model._rlp),
            castools.entry('_w', struct=self.model._w)
        ])

        # Create scaling struct and assign values for _x and _z
        self.sim_x_scaling = sim_x_scaling = sim_x(1.0)
        self.sim_z_scaling = sim_z_scaling = sim_z(1.0)
        sim_x_scaling["_x"] = self._x_scaling
        sim_z_scaling["_z"] = self._z_scaling

        # Create the unscaled (physical) variables
        self.sim_x_unscaled = sim_x_unscaled = sim_x(sim_x.cat * sim_x_scaling)
        self.sim_z_unscaled = sim_z_unscaled = sim_z(sim_z.cat * sim_z_scaling)

        # Initiate numerical structures to store the solutions (updated at each iteration)
        self.sim_x_num = self.sim_x(0)
        self.sim_x_num_unscaled = self.sim_x(0)
        self.sim_z_num = self.sim_z(0)
        self.sim_z_num_unscaled = self.sim_z(0)
        self.sim_p_num = self.sim_p(0)
        self.sim_aux_num = self.model._aux_expression(0)

        if self.model.model_type == 'discrete':

            # Build the rhs expression with the newly created variables
            # NOTE: _alg_fun is evaluated with the unscaled variables to introduce the scaling factors. 
            #       During evaluation the scaled variables can then be used.
            alg = self.model._alg_fun(sim_x_unscaled['_x'], sim_p['_u'], sim_z_unscaled['_z'], sim_p['_tvp'], sim_p['_p'], sim_p['_rlp'], sim_p['_w'])
            
            # Do the same for the ode expression but also divide by the scaling factor of the states.
            x_next = self.model._rhs_fun(sim_x_unscaled['_x'], sim_p['_u'], sim_z_unscaled['_z'], sim_p['_tvp'], sim_p['_p'], sim_p['_rlp'], sim_p['_w']) / sim_x_scaling

            # Build the DAE function
            nlp = {'x': sim_z['_z'], 'p': castools.vertcat(sim_x['_x'], sim_p), 'f': castools.DM(0), 'g': alg}
            self.discrete_dae_solver = castools.nlpsol('dae_roots', 'ipopt', nlp)

            # Build the simulator function:
            self.simulator = castools.Function('simulator',[sim_x['_x'], sim_z['_z'], sim_p],[x_next])


        elif self.model.model_type == 'continuous':

            # Define the ODE
            # NOTE: We evaluate here with the unscaled variables to introduce the scaling factors in the equations.
            # We have to divide the dynamics by the scaling factor of the states to get the correct result.
            # From now on we can use the scaled variables.
            xdot = self.model._rhs_fun(sim_x_unscaled['_x'], sim_p['_u'], sim_z_unscaled['_z'], sim_p['_tvp'], sim_p['_p'], sim_p['_rlp'], sim_p['_w']) / self._x_scaling
            alg = self.model._alg_fun(sim_x_unscaled['_x'], sim_p['_u'], sim_z_unscaled['_z'], sim_p['_tvp'], sim_p['_p'], sim_p['_rlp'], sim_p['_w'])

            # Now setup the dae system with the scaled variables
            self.dae = dae = {
                'x': sim_x,
                'z': sim_z,
                'p': sim_p,
                'ode': xdot,
                'alg': alg,
            }

            opts = {}
            # Set the integrator options, note that 'abstol' and 'reltol' are not needed for collocation
            if self._settings.integration_tool != 'collocation':
                opts = {
                    'abstol': self._settings.abstol,
                    'reltol': self._settings.reltol,
                }

            # Add further options for the CasADi integrator call defined by the user 
            opts.update(self._settings.integration_opts)

            if CASADI_LEGACY_MODE:
                opts['tf'] = self._settings.t_step
                self.simulator = castools.integrator('simulator', self._settings.integration_tool, dae, opts)
            else:
                # Build the simulator
                t0 = 0.0
                self.simulator = castools.integrator('simulator', self._settings.integration_tool, dae, t0, self._settings.t_step, opts)

        # Evaluate symbolically with unscaled variables such that the scaled variables can be used during evaluation.
        sim_aux = self.model._aux_expression_fun(sim_x_unscaled['_x'], sim_p['_u'], sim_z_unscaled['_z'], sim_p['_tvp'], sim_p['_p'], sim_p['_rlp'])
        # Create function to caculate all auxiliary expressions:
        self.sim_aux_expression_fun = castools.Function('sim_aux_expression_fun', [sim_x, sim_z, sim_p], [sim_aux])

        self.flags['setup'] = True

    def make_step(self, u0:np.ndarray=None, v0:np.ndarray=None, w0:np.ndarray=None)-> np.ndarray:
        """Main method of the simulator class during control runtime. This method is called at each timestep
        and computes the next state or the current control input :py:obj:`u0`. The method returns the resulting measurement,
        as defined in :py:class:`do_mpc.model.Model.set_meas`.

        The initial state :py:attr:`x0` is stored as a class attribute. Use this attribute :py:attr:`x0` to change the initial state.
        It is also possible to supply an initial guess for the algebraic states through the attribute :py:attr:`z0` and by calling
        :py:func:`set_initial_guess`.

        Finally, the method can be called with values for the process noise ``w0`` and the measurement noise ``v0``
        that were (optionally) defined in the :py:class:`do_mpc.model.Model`.
        Typically, these values should be sampled from a random distribution, e.g. ``np.random.randn`` for a random normal distribution.

        The method prepares the simulator by setting the current parameters, calls :py:func:`simulator.simulate`
        and updates the :py:class:`do_mpc.data` object.

        Args:
            u0: Current input to the system. Optional parameter for autonomous systems.
            v0: Additive measurement noise
            w0: Additive process noise
        
        Returns:
            y_next
        """
        # Generate dummy input if system is autnomous

        if u0 is None:
            assert self.model.n_u == 0, 'No input u0 provided. Please provide an input u0.'
            u0 = self.model._u(0)

        assert self.flags['setup'] == True, 'Simulator is not setup. Call simulator.setup() first.'
        assert isinstance(u0, (np.ndarray, castools.DM, castools.structure3.DMStruct)), 'u0 is wrong input type. You have: {}'.format(type(u0))
        assert u0.shape == self.model._u.shape, 'u0 has incorrect shape. You have: {}, expected: {}'.format(u0.shape, self.model._u.shape)
        assert isinstance(u0, (np.ndarray, castools.DM, castools.structure3.DMStruct)), 'u0 is wrong input type. You have: {}'.format(type(u0))
        assert u0.shape == self.model._u.shape, 'u0 has incorrect shape. You have: {}, expected: {}'.format(u0.shape, self.model._u.shape)

        if w0 is None:
            w0 = self.model._w(0)
        else:
            input_types = (np.ndarray, castools.DM, castools.structure3.DMStruct)
            assert isinstance(w0, input_types), 'w0 is wrong input type. You have: {}. Must be of type'.format(type(w0), input_types)
            assert w0.shape == self.model._w.shape, 'w0 has incorrect shape. You have: {}, expected: {}'.format(w0.shape, self.model._w.shape)

        if v0 is None:
            v0 = self.model._v(0)
        else:
            input_types = (np.ndarray, castools.DM, castools.structure3.DMStruct)
            assert isinstance(v0, input_types), 'v0 is wrong input type. You have: {}. Must be of type'.format(type(v0), input_types)
            assert v0.shape == self.model._v.shape, 'v0 has incorrect shape. You have: {}, expected: {}'.format(v0.shape, self.model._v.shape)

        tvp0 = self.tvp_fun(self._t0)
        p0 = self.p_fun(self._t0)
        rlp0 = self.rlp_fun(self._t0)
        t0 = self._t0
        x0 = self._x0

        z0 = self.sim_z_num['_z']
        z0_unscaled = self.sim_z_num_unscaled["_z"]
        self.sim_x_num['_x'] = x0.cat / self._x_scaling
        self.sim_p_num['_u'] = u0
        self.sim_p_num['_p'] = p0
        self.sim_p_num['_tvp'] = tvp0
        self.sim_p_num['_rlp'] = rlp0
        self.sim_p_num['_w'] = w0


        # This new line makes sure that simulate() is computed with the curret tvp and p values. In the previous version there was a bug that the
        # auxiliary expressions were computed with the previous values of tvp and p.
        aux0 = self.sim_aux_expression_fun(self.sim_x_num, self.sim_z_num, self.sim_p_num)

        x_next, z_next = self.simulate()

        # Call measurement function
        x_next_unscaled = x_next * self._x_scaling.cat
        z_next_unscaled = z_next * self._z_scaling.cat

        y_next = self.model._meas_fun(x_next_unscaled, u0, z_next_unscaled, tvp0, p0, rlp0, v0)

        # Update data object
        self.data.update(_x = x0.cat)
        self.data.update(_u = u0)
        self.data.update(_z = z0_unscaled)
        self.data.update(_tvp = tvp0)
        self.data.update(_p = p0)
        self.data.update(_rlp = rlp0)
        self.data.update(_y = y_next)
        self.data.update(_aux = aux0)
        self.data.update(_time = t0)

        self._x0.master = x_next_unscaled
        self._z0.master = z_next_unscaled
        self._u0.master = u0
        self._t0 = self._t0 + self._settings.t_step 

        self.flags['first_step'] = False

        return y_next.full()
