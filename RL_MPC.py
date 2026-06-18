import pickle
import os

import casadi.tools as castools
import numpy as np


from do_mpc.controller import MPC
from _model_for_rl import RL_Model
from do_mpc.data import MPCData
from typing import Union, Callable

import copy
import time
import warnings

class RL_MPC_Data(MPCData):
    
    def __init__(self, model: RL_Model):
        self.dtype = 'default'
        assert model.flags['setup'] == True, 'Model was not setup. After the complete model creation call model.setup().'
        # As discussed here: https://groups.google.com/forum/#!topic/casadi-users/dqAb4tnA2ik
        # struct_SX cannot be unpickled (seems like a bug)
        # TODO: Find better workaround.
        self.model = model.__dict__.copy()
        self.model.pop('_rhs')
        self.model.pop('_aux_expression')
        self.model.pop('_y_expression')
        self.model.pop('_alg')
        self.model.pop('sv')


        # TODO: n_aux not existing
        #self._aux = np.empty((0, model.n_aux))
        # Dictionary with possible data_fields in the class and their respective dimension. All data is numpy ndarray.
        self.data_fields = {
            '_time': 1,
            '_x':    model.n_x,
            '_y':    model.n_y,
            '_u':    model.n_u,
            '_z':    model.n_z,
            '_tvp':  model.n_tvp,
            '_p':    model.n_p,
            '_rlp':  model.n_rlp,
            '_aux':  model.n_aux,
        }

        self.init_storage()
        self.meta_data = {}

        # Accelerate __getitem__ calls (to retrieve results) by saving indices of previous queries.
        self.result_queries = {'ind':[], 'f_ind':[]}

class RL_MPC(MPC):
    
    def __init__(self, model: RL_Model = None):

        if model is None:
            return
        
        super().__init__(model)

        self.data = RL_MPC_Data(self.model)
           
        # Updating the data fields
        self.settings.gamma = 1.0  # Discount factor

        # Default Parameters (param. details in set_param method):
        self.settings.nlpsol_opts.update(
            {
                "ipopt.fixed_variable_treatment": "make_constraint", # This is necessary because otherwise some Lagrange multiplier are wrong so we get wrong NLP sensitivities.
            }
        )


    def _check_validity(self):
        """Private method to be called in :py:func:`setup`. Checks if the configuration is valid and
        if the optimization problem can be constructed.
        Furthermore, default values are set if they were not configured by the user (if possible).
        Specifically, we set dummy values for the ``tvp_fun`` and ``p_fun`` if they are not present in the model.
        """
        # Objective mus be defined.
        if self.flags['set_objective'] == False:
            raise Exception('Objective is undefined. Please call .set_objective() prior to .setup().')
        # rterm should have been set (throw warning if not)
        if self.flags['set_rterm'] == False:
            warnings.warn('rterm was not set and defaults to zero. Changes in the control inputs are not penalized. Can lead to oscillatory behavior.')
            time.sleep(2)
        # tvp_fun must be set, if tvp are defined in model.
        if self.flags['set_tvp_fun'] == False and self.model._tvp.size > 0:
            raise Exception('You have not supplied a function to obtain the time-varying parameters defined in model. Use .set_tvp_fun() prior to setup.')
        # p_fun must be set, if p are defined in model.
        if self.flags['set_p_fun'] == False and self.model._p.size > 0:
            raise Exception('You have not supplied a function to obtain the parameters defined in model. Use .set_p_fun() (low-level API) or .set_uncertainty_values() (high-level API) prior to setup.')
        # rlp_fun must be set, if rlp are defined in model.
        if self.flags['set_rlp_fun'] == False and self.model._rlp.size > 0:
            raise Exception('You have not supplied a function to obtain the reinforcement learning parameters defined in model. Use .set_rlp_fun() prior to setup.')

        if np.any(self.rterm_factor.cat.full() < 0):
            warnings.warn('You have selected negative values for the rterm penalizing changes in the control input.')
            time.sleep(2)

        # Lower bounds should be lower than upper bounds:
        for lb, ub in zip([self._x_lb, self._u_lb, self._z_lb], [self._x_ub, self._u_ub, self._z_ub]):
            bound_check = lb.cat > ub.cat
            bound_fail = [label_i for i,label_i in enumerate(lb.labels()) if bound_check[i]]
            if np.any(bound_check):
                raise Exception('Your bounds are inconsistent. For {} you have lower bound > upper bound.'.format(bound_fail))

        # Are terminal bounds for the states set? If not use default values (unless MPC is setup to not use terminal bounds)
        if np.all(self._x_terminal_ub.cat == np.inf) and self._settings.use_terminal_bounds:
            self._x_terminal_ub = self._x_ub
        if np.all(self._x_terminal_lb.cat == -np.inf) and self._settings.use_terminal_bounds:
            self._x_terminal_lb = self._x_lb

        # Set dummy functions for tvp and p in case these parameters are unused.
        if 'tvp_fun' not in self.__dict__:
            _tvp = self.get_tvp_template()

            def tvp_fun(t): return _tvp
            self.set_tvp_fun(tvp_fun)

        if 'p_fun' not in self.__dict__:
            _p = self.get_p_template(1)

            def p_fun(t): return _p
            self.set_p_fun(p_fun)

        if 'rlp_fun' not in self.__dict__:
            _rlp = self.get_rlp_template()
            
            def rlp_fun(t): return _rlp
            self.set_rlp_fun(rlp_fun)

    def get_rlp_template(self)->Union[castools.structure3.SXStruct,castools.structure3.MXStruct]:
        """Obtain output template for :py:func:`set_p_fun`.
        Use this method in conjunction with :py:func:`set_p_fun`
        to define the function for retrieving the parameters at each sampling time.

        See :py:func:`set_p_fun` for more details.

        Returns:
            numerical CasADi structure
        """
        return self.model._rlp(0)

    def set_rlp_fun(self, rlp_fun:Callable[[float],Union[castools.structure3.SXStruct,castools.structure3.MXStruct]])->None:
        """Set function which returns parameters.
        The ``rlp_fun`` is called at each optimization step to get the current values of the reinforcement learning parameters.

        The method takes as input a function, which MUST
        return a structured object, based on the defined reinforcement learning parameters.
        The defined function has time as a single input.

        Obtain this structured object first, by calling :py:func:`get_rlp_template`.

        Use the combination of :py:func:`get_rlp_template` and :py:func:`set_rlp_fun`.

        **Example:**

        ::

            # in model definition:
            alpha = model.set_variable(var_type='_rlp', var_name='alpha')
            beta = model.set_variable(var_type='_rlp', var_name='beta')

            ...
            # in MPC configuration:
            rlp_template = MPC.get_rlp_template()
            rlp_template['alpha'] = np.array([1])
            rlp_template['beta'] = np.array([0.9])

            def rlp_fun(t_now):
                return rlp_template

            MPC.set_rlp_fun(rlp_fun)

        Args:
            rlp_fun: Function which returns a structure with numerical values. Must be the same structure as obtained from :py:func:`get_rlp_template`. Function must have a single input (time).
        """
        assert self.get_rlp_template().labels() == rlp_fun(0).labels(), 'Incorrect output of rlp_fun. Use get_rlp_template to obtain the required structure.'
        self.flags['set_rlp_fun'] = True
        self.rlp_fun = rlp_fun
    
    def set_objective(self, mterm:Union[castools.SX,castools.MX]=None, lterm:Union[castools.SX,castools.MX]=None)->None:
        """Sets the objective of the optimal control problem (OCP). We introduce the following cost function:

        .. math::
           J(x,u,z) =  \\sum_{k=0}^{N}\\left(\\underbrace{l(x_k,z_k,u_k,p_k,p_{\\text{tv},k})}_{\\text{lagrange term}}
           + \\underbrace{\\Delta u_k^T R \\Delta u_k}_{\\text{r-term}}\\right)
           + \\underbrace{m(x_{N+1})}_{\\text{meyer term}}

        which is applied to the discrete-time model **AND** the discretized continuous-time model.
        For discretization we use `orthogonal collocation on finite elements`_ .
        The cost function is evaluated only on the first collocation point of each interval.

        .. _`orthogonal collocation on finite elements`: ../theory_orthogonal_collocation.html

        :py:func:`set_objective` is used to set the :math:`l(x_k,z_k,u_k,p_k,p_{\\text{tv},k})` (``lterm``) and :math:`m(x_{N+1})` (``mterm``), where ``N`` is the prediction horizon.
        Please see :py:func:`set_rterm` for the penalization of the control inputs.

        Args:
            lterm: Stage cost - **scalar** symbolic expression with respect to ``_x``, ``_u``, ``_z``, ``_tvp``, ``_p``
            mterm: Terminal cost - **scalar** symbolic expression with respect to ``_x`` and ``_p``

        Raises:
            assertion: mterm must have ``shape=(1,1)`` (scalar expression)
            assertion: lterm must have ``shape=(1,1)`` (scalar expression)
        """
        assert mterm.shape == (1,1), 'mterm must have shape=(1,1). You have {}'.format(mterm.shape)
        assert lterm.shape == (1,1), 'lterm must have shape=(1,1). You have {}'.format(lterm.shape)
        assert self.flags['setup'] == False, 'Cannot call .set_objective after .setup().'

        _x, _u, _z, _tvp, _p, _rlp = self.model['x','u','z','tvp','p', 'rlp']


        # Check if mterm is valid:
        if not isinstance(mterm, (castools.DM, castools.SX, castools.MX)):
            raise Exception('mterm must be of type casadi.DM, casadi.SX or casadi.MX. You have: {}.'.format(type(mterm)))

        # Check if lterm is valid:
        if not isinstance(lterm, (castools.DM, castools.SX, castools.MX)):
            raise Exception('lterm must be of type casadi.DM, casadi.SX or casadi.MX. You have: {}.'.format(type(lterm)))

        if mterm is None:
            self.mterm = castools.DM(0)
        else:
            self.mterm = mterm
        # TODO: This function should be evaluated with scaled variables.
        self.mterm_fun = castools.Function('mterm', [_x, _tvp, _p, _rlp], [mterm], ['_x', '_tvp', '_p', '_rlp'], ['mterm'])

        if lterm is None:
            self.lterm = castools.DM(0)
        else:
            self.lterm = lterm

        self.lterm_fun = castools.Function('lterm', [_x, _u, _z, _tvp, _p, _rlp], [lterm], ['_x', '_u', '_z', '_tvp', '_p', '_rlp'], ['lterm'])

        # Check if lterm and mterm use invalid variables as inputs.
        # For the check we evaluate the function with dummy inputs and expect a DM output.
        err_msg = '{} contains invalid symbolic variables as inputs. Must contain only: {}'
        try:
            self.mterm_fun(_x(0),_tvp(0),_p(0), _rlp(0))
        except:
            raise Exception(err_msg.format('mterm','_x, _tvp, _p, _rlp'))
        try:
            self.lterm_fun(_x(0),_u(0), _z(0), _tvp(0), _p(0), _rlp(0))
        except:
            err_msg.format('lterm', '_x, _u, _z, _tvp, _p, _rlp')

        self.flags['set_objective'] = True

    def _setup_discretization(self):
        """Private method that creates the discretization for the optimizer (MHE or MPC).
        Returns the integrator function (``ifcn``) and the total number of collocation points.

        The following discretization methods are available:

        * orthogonal collocation

        * discrete dynamics

        Discretization parameters can be set with the :py:func:`do_mpc.controller.MPC.set_param` and
        :py:func:`do_mpc.estimator.MHE.set_param` methods.

        There is no point in calling this method as part of the public API.
        """
        # Scaled variables
        _x, _u, _z, _tvp, _p, _rlp, _w = self.model['x', 'u', 'z', 'tvp', 'p', 'rlp', 'w']

        # Unscale variables
        _x_unscaled = _x*self._x_scaling.cat
        _u_unscaled = _u*self._u_scaling.cat
        _z_unscaled = _z*self._z_scaling.cat
        _p_unscaled = _p*self._p_scaling.cat

        # Create _rhs and _alg
        _rhs = self.model._rhs_fun(_x_unscaled, _u_unscaled, _z_unscaled, _tvp, _p_unscaled, _rlp, _w)
        _alg = self.model._alg_fun(_x_unscaled, _u_unscaled, _z_unscaled, _tvp, _p_unscaled, _rlp, _w)

        # Scale (only _rhs)
        _rhs_scaled = _rhs/self._x_scaling.cat

        if self.model.model_type == 'discrete':
            _i = self.model.sv.sym('i', 0)
            # discrete integrator ifcs mimics the API the collocation ifcn.
            ifcn = castools.Function('ifcn', [_x, _i, _u, _z, _tvp, _p, _rlp, _w], [_alg, _rhs_scaled], ['_x', '_i', '_u', '_z', '_tvp', '_p', '_rlp', '_w'], ['alg', 'x_next'])
            n_total_coll_points = 0
        elif self.settings.state_discretization == 'collocation':
            ffcn = castools.Function('ffcn', [_x, _u, _z, _tvp, _p, _rlp, _w], [_rhs_scaled])
            afcn = castools.Function('afcn', [_x, _u, _z, _tvp, _p, _rlp, _w], [_alg])
            # Get collocation information
            coll = self.settings.collocation_type # Collocation type
            deg = self.settings.collocation_deg # Degree of polynomial
            ni = self.settings.collocation_ni # Number of finite elements
            nk = self.settings.n_horizon # Number of control intervals
            t_step = self.settings.t_step # Time step
            n_x = self.model.n_x # Number of states
            n_u = self.model.n_u # Number of inputs
            n_p = self.model.n_p # Number of parameters
            n_z = self.model.n_z # Number of algebraic variables
            n_w = self.model.n_w # Number of disturbances
            n_tvp = self.model.n_tvp # Number of time-varying parameters
            n_rlp = self.model.n_rlp # Number of reinforcement learning parameters
            n_total_coll_points = (deg + 1) * ni # (Number of collocation points
            # + 1 at the beginning of the finite interval) * number of finite elements

            # Choose collocation points
            if coll == 'legendre':    # Legendre collocation points
                tau_root = [0] + castools.collocation_points(deg, 'legendre')
            elif coll == 'radau':     # Radau collocation points
                tau_root = [0] + castools.collocation_points(deg, 'radau')
            else:
                raise Exception('Unknown collocation scheme')

            # Size of the finite elements
            h = t_step / ni

            # Coefficients of the collocation equation
            C = np.zeros((deg + 1, deg + 1))

            # Coefficients of the continuity equation
            D = np.zeros(deg + 1)

            # Dimensionless time inside one control interval
            tau = self.model.sv.sym("tau")

            # All collocation time points
            T = np.zeros((nk, ni, deg + 1))
            # For all control intervals
            for k in range(nk):
                # For all finite elements
                for i in range(ni):
                    # For all collocation points
                    for j in range(deg + 1):
                        T[k, i, j] = h * (k * ni + i + tau_root[j]) # Actual time points for each collocation point

            # For all collocation points
            for j in range(deg + 1):
                # Construct Lagrange polynomials to get the polynomial basis at the
                # collocation point
                L = 1
                # For all collocation points
                for r in range(deg + 1): 
                    if r != j:
                        L *= (tau - tau_root[r]) / (tau_root[j] - tau_root[r]) # Lagrange polynomial
                lfcn = castools.Function('lfcn', [tau], [L]) # Lagrange polynomial function
                D[j] = lfcn(1.0)
                # Evaluate the time derivative of the polynomial at all collocation
                # points to get the coefficients of the continuity equation
                tfcn = castools.Function('tfcn', [tau], [castools.tangent(L, tau)])
                for r in range(deg + 1):
                    C[j, r] = tfcn(tau_root[r]) # Coefficients of the continuity equation

            # Define symbolic variables for collocation
            xk0 = self.model.sv.sym("xk0", n_x)
            #zk = self.model.sv.sym("zk", n_z)
            pk = self.model.sv.sym("pk", n_p)
            tv_pk = self.model.sv.sym("tv_pk", n_tvp)
            rlp_k = self.model.sv.sym("rlp_k", n_rlp)
            uk = self.model.sv.sym("uk", n_u)
            wk = self.model.sv.sym("wk", n_w)

            # State trajectory
            n_ik = ni * (deg + 1) * n_x # Total number of state variables for the control interval
            ik = self.model.sv.sym("ik", n_ik)

            ik_split = np.resize(np.array([], dtype=self.model.sv.dtype), (ni, deg + 1)) # A 2D array to reorganize 
            # the state variables by finite element and collocation point
            offset = 0

            # Algebraic trajectory
            n_zk = ni * (deg +1) * n_z # Total number of algebraic variables for the control interval
            zk = self.model.sv.sym("zk", n_zk)
            zk_split = np.resize(np.array([], dtype=self.model.sv.dtype), (ni, deg + 1)) # A 2D array to reorganize 
            # the algebraic variables by finite element and collocation point
            offset_z = 0

            # Store initial condition
            ik_split[0, 0] = xk0
            zk_split[0, 0] = zk[offset_z:offset_z + n_z]
            offset_z += n_z
            first_j = 1  # Skip allocating x for the first collocation point for the first finite element
            # For each finite element
            for i in range(ni):
                # For each collocation point
                for j in range(first_j, deg + 1):
                    # Get the expression for the state vector
                    ik_split[i, j] = ik[offset:offset + n_x]
                    zk_split[i, j] = zk[offset_z:offset_z + n_z]
                    offset_z += n_z
                    offset += n_x

                # All collocation points in subsequent finite elements
                first_j = 0

            # Get the state at the end of the control interval
            xkf = ik[offset:offset + n_x]
            zkf = zk[offset_z - n_z:offset_z]
            offset += n_x
            # Check offset for consistency
            assert(offset == n_ik)
            assert(offset_z == n_zk)
            # Constraints in the control interval
            gk = []
            lbgk = []
            ubgk = []

            # For all finite elements
            for i in range(ni):
                # for the first point:
                a_i0 = afcn(ik_split[i, 0], uk, zk_split[i,0], tv_pk, pk, wk)
                gk.append(a_i0)
                lbgk.append(np.zeros(n_z))
                ubgk.append(np.zeros(n_z))

                # For all collocation points
                for j in range(1, deg + 1):
                    # Get an expression for the state derivative at the coll point
                    xp_ij = 0
                    # For all collocation points
                    for r in range(deg + 1): 
                        xp_ij += C[r, j] * ik_split[i, r] # State derivative at the collocation point
                        # (multiplication with h happens later when adding the collocation equation to gk)

                    # Add collocation equations to the NLP
                    f_ij = ffcn(ik_split[i, j], uk, zk_split[i,j], tv_pk, pk, wk)
                    gk.append(h * f_ij - xp_ij)
                    lbgk.append(np.zeros(n_x))  # equality constraints
                    ubgk.append(np.zeros(n_x))  # equality constraints

                    # algebraic constraints
                    a_ij = afcn(ik_split[i, j], uk, zk_split[i,j], tv_pk, pk, wk)
                    gk.append(a_ij)
                    lbgk.append(np.zeros(n_z))
                    ubgk.append(np.zeros(n_z))


                # Get an expression for the state at the end of the finite element
                xf_i = 0
                # For all collocation points
                for r in range(deg + 1): 
                    xf_i += D[r] * ik_split[i, r] # State at the end of the finite element
                    # (can be computed from collocation equations)

                # Add continuity equation to NLP
                x_next = ik_split[i + 1, 0] if i + 1 < ni else xkf
                gk.append(x_next - xf_i)
                lbgk.append(np.zeros(n_x))
                ubgk.append(np.zeros(n_x))

            # Concatenate constraints
            gk = castools.vertcat(*gk)
            lbgk = np.concatenate(lbgk)
            ubgk = np.concatenate(ubgk)

            assert(gk.shape[0] == ik.shape[0] + zk.shape[0])

            # Create the integrator function
            ifcn = castools.Function("ifcn", [xk0, ik, uk, zk, tv_pk, pk, wk], [gk, xkf, zkf], ["xk", "ik", "uk", "zk", "tv_pk", "pk", "wk"], ["gk", "xkf", "zkf"])

            cok = castools.vertcat(ik, zk)
            jac_gk_cok = castools.jacobian(gk, cok)
            jac_gk_p = castools.jacobian(gk, pk)
            
            self.xkf_zkf_extractor = castools.Function("xkf_zkf_extractor", [cok], [xkf, zkf], ["all_collocation_states"], ["xkf", "zkf"])

            ifcn_jac = castools.Function("ifcn_jac", [xk0, ik, uk, zk, tv_pk, pk, wk], [jac_gk_cok, jac_gk_p], ["xk", "ik", "uk", "zk", "tv_pk", "pk", "wk"], ["jac_gk_cok", "jac_gk_p"])

            # Return the integration function and the number of collocation points
        return ifcn, n_total_coll_points

    def _prepare_nlp(self)->None:
        """Internal method. See detailed documentation with optimizer.prepare_nlp
        """
        self._settings.check_for_mandatory_settings()
        nl_cons_input = self.model['x', 'u', 'z', 'tvp', 'p', 'rlp']
        self._setup_nl_cons(nl_cons_input)
        self._check_validity()

        # Obtain an integrator (collocation, discrete-time) and the amount of intermediate (collocation) points
        ifcn, n_total_coll_points = self._setup_discretization()
        n_branches, n_scenarios, child_scenario, parent_scenario, branch_offset = self._setup_scenario_tree()

        # How many scenarios arise from the scenario tree (robust multi-stage MPC)
        n_max_scenarios = self.n_combinations ** self._settings.n_robust

        # If open_loop option is active, all scenarios (at a given stage) have the same input.
        if self._settings.open_loop:
            n_u_scenarios = 1
        else:
            # Else: Each scenario has its own input.
            n_u_scenarios = n_max_scenarios

        # How many slack variables (for soft constraints) are introduced over the horizon.
        if self._settings.nl_cons_single_slack:
            n_eps = 1
        else:
            n_eps = self._settings.n_horizon

        # Create struct for optimization variables:
        self._opt_x = opt_x = self.model.sv.sym_struct([
            # One additional point (in the collocation dimension) for the final point.
            castools.entry('_x', repeat=[self._settings.n_horizon+1, n_max_scenarios,
                                1+n_total_coll_points], struct=self.model._x),
            castools.entry('_z', repeat=[self._settings.n_horizon, n_max_scenarios,
                                max(n_total_coll_points,1)], struct=self.model._z),
            castools.entry('_u', repeat=[self._settings.n_horizon, n_u_scenarios], struct=self.model._u),
            castools.entry('_eps', repeat=[n_eps, n_max_scenarios], struct=self._eps),
        ])


        # Create integer list for MINLP if any input is discrete
        if self.flags['MINLP']:
            # Create a Sym_Struct with similar structure, but with only booleans of value 'False'
            opt_x_integer_flag = opt_x(False)
            # Set all integer variables to true
            for u_int in self.integer_u:
                opt_x_integer_flag['_u', :, :, u_int] = True
            # Convert Sym_Struct to list with boolean entries
            self.opt_x_integer_flag = np.ndarray.flatten(np.array(opt_x_integer_flag.cat, dtype=bool)).tolist()

        self.n_opt_x = self._opt_x.shape[0]
        # NOTE: The entry _x[k,child_scenario[k,s,b],:] starts with the collocation points from s to b at time k
        #       and the last point contains the child node
        # NOTE: Currently there exist dummy collocation points for the initial state (for each branch)

        # Create scaling struct as assign values for _x, _u, _z.
        self.opt_x_scaling = opt_x_scaling = opt_x(1)
        opt_x_scaling['_x'] = self._x_scaling
        opt_x_scaling['_z'] = self._z_scaling
        opt_x_scaling['_u'] = self._u_scaling

        # opt_x are unphysical (scaled) variables. opt_x_unscaled are physical (unscaled) variables.
        self.opt_x_unscaled = opt_x_unscaled = opt_x(opt_x.cat * opt_x_scaling)

        # Create struct for optimization parameters:
        self._opt_p = opt_p = self.model.sv.sym_struct([
            castools.entry('_x0', struct=self.model._x),
            castools.entry('_tvp', repeat=self._settings.n_horizon+1, struct=self.model._tvp),
            castools.entry('_p', repeat=self.n_combinations, struct=self.model._p),
            castools.entry('_rlp', struct=self.model._rlp),
            castools.entry('_u_prev', struct=self.model._u),
        ])
        _w = self.model._w(0)

        self.n_opt_p = opt_p.shape[0]

        # Dummy struct with symbolic variables
        self.aux_struct = self.model.sv.sym_struct([
            castools.entry('_aux', repeat=[self._settings.n_horizon, n_max_scenarios], struct=self.model._aux_expression)
        ])
        # Create mutable symbolic expression from the struct defined above.
        self._opt_aux = opt_aux = self.model.sv.struct(self.aux_struct)

        self.n_opt_aux = opt_aux.shape[0]

        self._lb_opt_x = opt_x(-np.inf)
        self._ub_opt_x = opt_x(np.inf)

        # Initialize objective function and constraints
        obj = castools.DM(0)
        cons = []
        cons_lb = []
        cons_ub = []

        # Initial condition:
        cons.append(opt_x['_x', 0, 0, -1]-opt_p['_x0']/self._x_scaling)

        cons_lb.append(np.zeros((self.model.n_x, 1)))
        cons_ub.append(np.zeros((self.model.n_x, 1)))

        # NOTE: Weigthing factors for the tree assumed equal. They could be set from outside
        # Weighting factor for every scenario
        omega = [1. / n_scenarios[k + 1] for k in range(self._settings.n_horizon)]
        omega_delta_u = [1. / n_scenarios[k + 1] for k in range(self._settings.n_horizon)]

        # For all control intervals
        for k in range(self._settings.n_horizon):
            # For all scenarios (grows exponentially with n_robust)
            for s in range(n_scenarios[k]):
                # For all childen nodes of each node at stage k, discretize the model equations

                # Scenario index for u is always 0 if self.open_loop = True
                s_u = 0 if self._settings.open_loop else s
                for b in range(n_branches[k]):
                    # Obtain the index of the parameter values that should be used for this scenario
                    current_scenario = b + branch_offset[k][s]

                    # Compute constraints and predicted next state of the discretization scheme
                    col_xk = castools.vertcat(*opt_x['_x', k+1, child_scenario[k][s][b], :-1])
                    col_zk = castools.vertcat(*opt_x['_z', k, child_scenario[k][s][b]])
                    # col_jxpk = castools.vertcat(*[jac_x_p_restorator(opt_x['_jac_x_p', k+1, child_scenario[k][s][b], idx]) for idx in range(n_total_coll_points)])
                    # col_jzpk = castools.vertcat(*[jac_z_p_restorator(opt_x['_jac_z_p', k, child_scenario[k][s][b], idx]) for idx in range(n_total_coll_points)])
                    [g_ksb, xf_ksb] = ifcn(opt_x['_x', k, s, -1], col_xk,
                                           opt_x['_u', k, s_u], col_zk, opt_p['_tvp', k],
                                           opt_p['_p', current_scenario], opt_p["_rlp"], _w)

                    # Add the collocation equations
                    cons.append(g_ksb)
                    cons_lb.append(np.zeros(g_ksb.shape[0]))
                    cons_ub.append(np.zeros(g_ksb.shape[0]))

                    # Add continuity constraints
                    cons.append(xf_ksb - opt_x['_x', k+1, child_scenario[k][s][b], -1])
                    cons_lb.append(np.zeros((self.model.n_x, 1)))
                    cons_ub.append(np.zeros((self.model.n_x, 1)))


                    k_eps = min(k, n_eps-1)
                    if self._settings.nl_cons_check_colloc_points:
                        # Ensure nonlinear constraints on all collocation points
                        for i in range(n_total_coll_points):
                            nl_cons_k = self._nl_cons_fun(
                                opt_x_unscaled['_x', k+1, s, i], opt_x_unscaled['_u', k, s_u], opt_x_unscaled['_z', k, s, i],
                                opt_p['_tvp', k], opt_p['_p', current_scenario], opt_x_unscaled['_eps', k_eps, s])
                            cons.append(nl_cons_k)
                            cons_lb.append(self._nl_cons_lb)
                            cons_ub.append(self._nl_cons_ub)
                    else:
                        # Ensure nonlinear constraints only on the beginning of the FE
                        nl_cons_k = self._nl_cons_fun(
                                opt_x_unscaled['_x', k, s, -1], opt_x_unscaled['_u', k, s_u], opt_x_unscaled['_z', k, s, 0],
                                opt_p['_tvp', k], opt_p['_p', current_scenario], opt_p["_rlp"], opt_x_unscaled['_eps', k_eps, s])
                        cons.append(nl_cons_k)
                        cons_lb.append(self._nl_cons_lb)
                        cons_ub.append(self._nl_cons_ub)

                    # Add terminal constraints
                    # TODO: Add terminal constraints with an additional nl_cons

                    # Add contribution to the cost
                    obj += omega[k] * self.lterm_fun(opt_x_unscaled['_x', k, s, -1], opt_x_unscaled['_u', k, s_u],
                                                     opt_x_unscaled['_z', k, s, -1], opt_p['_tvp', k], opt_p['_p', current_scenario], opt_p["_rlp"])
                    
                    # Add slack variables to the cost
                    obj += self.epsterm_fun(opt_x_unscaled['_eps', k_eps, s])

                    # In the last step add the terminal cost too
                    if k == self._settings.n_horizon - 1:

                        obj += omega[k] * self.mterm_fun(opt_x_unscaled['_x', k + 1, s, -1], opt_p['_tvp', k+1],
                                                         opt_p['_p', current_scenario], opt_p["_rlp"])

                    # U regularization:
                    # For user defined penalty term
                    if self.flags['rterm_fun'] == True:
                        if k==0:
                            obj += omega_delta_u[k] * self.rterm_fun(opt_x_unscaled['_x', k, s, -1], opt_x_unscaled['_u', k, s_u], opt_p['_u_prev']/self._u_scaling,
                                                     opt_x_unscaled['_z', k, s, -1], opt_p['_tvp', k], opt_p['_p', current_scenario])
                        else:
                            obj += omega_delta_u[k] * self.rterm_fun(opt_x_unscaled['_x', k, s, -1], opt_x_unscaled['_u', k, s_u], opt_x['_u', k-1, parent_scenario[k][s_u]],
                                                     opt_x_unscaled['_z', k, s, -1], opt_p['_tvp', k], opt_p['_p', current_scenario])
                    # Default penalty term
                    if self.flags['rterm_fun'] == False:
                        if k == 0:
                            obj += omega_delta_u[k] * self.rterm_factor.cat.T@((opt_x['_u', 0, s_u]-opt_p['_u_prev']/self._u_scaling)**2)
                        else:
                            obj += omega_delta_u[k] * self.rterm_factor.cat.T@((opt_x['_u', k, s_u]-opt_x['_u', k-1, parent_scenario[k][s_u]])**2)

                    # Calculate the auxiliary expressions for the current scenario:
                    opt_aux['_aux', k, s] = self.model._aux_expression_fun(
                        opt_x_unscaled['_x', k, s, -1], opt_x_unscaled['_u', k, s_u], opt_x_unscaled['_z', k, s, -1], opt_p['_tvp', k], opt_p['_p', current_scenario], opt_p["_rlp"])

                    # For some reason when working with MX, the "unused" aux values in the scenario tree must be set explicitly (they are not ever used...)
                for s_ in range(n_scenarios[k],n_max_scenarios):
                    opt_aux['_aux', k, s_] = self.model._aux_expression_fun(
                        opt_x_unscaled['_x', k, s, -1], opt_x_unscaled['_u', k, s_u], opt_x_unscaled['_z', k, s, -1], opt_p['_tvp', k], opt_p['_p', current_scenario], opt_p["_rlp"])

        # Set bounds for all optimization variables
        self._update_bounds()

        # Write all created elements to self:       
        self._nlp_obj = obj
        self._nlp_cons = cons
        self._nlp_cons_lb = cons_lb
        self._nlp_cons_ub = cons_ub

        # Initialize copies of structures with numerical values (all zero):
        self._opt_x_num = self._opt_x(1)
        self.opt_x_num_unscaled = self._opt_x(1)
        self._opt_p_num = self._opt_p(0)
        self.opt_aux_num = self._opt_aux(0)

        self.flags['prepare_nlp'] = True

    def set_initial_guess(self)->None:
        """Initial guess for optimization variables.
        Uses the current class attributes :py:attr:`x0`, :py:attr:`z0` and :py:attr:`u0` to create the initial guess.
        The initial guess is simply the initial values for all :math:`k=0,\dots,N` instances of :math:`x_k`, :math:`u_k` and :math:`z_k`.

        Warnings:
            If no initial values for :py:attr:`x0`, :py:attr:`z0` and :py:attr:`u0` were supplied during setup, these default to zero.

        Note:
            The initial guess is fully customizable by directly setting values on the class attribute:
            :py:attr:`opt_x_num`.
        """
        assert self.flags['setup'] == True, 'MPC was not setup yet. Please call MPC.setup().'

        self.opt_x_num['_x'] = self._x0.cat/self._x_scaling
        self.opt_x_num['_u'] = self._u0.cat/self._u_scaling
        self.opt_x_num['_z'] = self._z0.cat/self._z_scaling

        self.flags['set_initial_guess'] = True

    def make_step(self, x0:Union[np.ndarray,castools.DM], old_action: Union[np.ndarray, castools.DM] = None)->np.ndarray:
        """Main method of the class during runtime. This method is called at each timestep
        and returns the control input for the current initial state :py:obj:`x0`.

        The method prepares the MHE by setting the current parameters, calls :py:func:`solve`
        and updates the :py:class:`do_mpc.data.Data` object.

        Args:
            x0: Current state of the system.

        Returns:
            u0
        """
        # Check setup.
        assert self.flags['setup'] == True, 'MPC was not setup yet. Please call MPC.setup().'

        # Check input type.
        if isinstance(x0, (np.ndarray, castools.DM)):
            pass
        elif isinstance(x0, castools.structure3.DMStruct):
            x0 = x0.cat
        else:
            raise Exception('Invalid type {} for x0. Must be {}'.format(type(x0), (np.ndarray, castools.DM, castools.structure3.DMStruct)))

        # Check input shape.
        n_val = np.prod(x0.shape)
        assert n_val == self.model.n_x, 'Wrong input with shape {}. Expected vector with {} elements'.format(n_val, self.model.n_x)
        # Check (once) if the initial guess was supplied.
        if not self.flags['set_initial_guess']:
            warnings.warn('Intial guess for the MPC was not set. The solver call is likely to fail.')
            time.sleep(5)
            # Since do-mpc is warmstarting, the initial guess will exist after the first call.
            self.flags['set_initial_guess'] = True

        # Get current tvp, p and time (as well as previous u)
        if old_action is not None:
            self._u0.master = castools.DM(old_action)
        u_prev = self._u0
        tvp0 = self.tvp_fun(self._t0)
        p0 = self.p_fun(self._t0)
        rlp0 = self.rlp_fun(self._t0)
        t0 = self._t0

        # Set the current parameter struct for the optimization problem:
        self.opt_p_num['_x0'] = x0
        self.opt_p_num['_u_prev'] = u_prev
        self.opt_p_num['_tvp'] = tvp0['_tvp']
        self.opt_p_num['_p'] = p0['_p']
        self.opt_p_num['_rlp'] = rlp0
        # Solve the optimization problem (method inherited from optimizer)
        self.solve()

        # Extract solution:
        u0 = self.opt_x_num['_u', 0, 0]*self._u_scaling
        z0 = self.opt_x_num['_z', 0, 0, 0]*self._z_scaling
        aux0 = self.opt_aux_num['_aux', 0, 0]

        # Store solution:
        self.data.update(_x = x0)
        self.data.update(_u = u0)
        self.data.update(_z = z0)
        self.data.update(_tvp = tvp0['_tvp', 0])
        self.data.update(_p = p0['_p', 0])
        self.data.update(_rlp = rlp0)
        self.data.update(_time = t0)
        self.data.update(_aux = aux0)

        # Store additional information
        self.data.update(opt_p_num = self.opt_p_num)
        if self._settings.store_full_solution == True:
            opt_x_num_unscaled = self.opt_x_num_unscaled
            opt_aux_num = self.opt_aux_num
            self.data.update(_opt_x_num = opt_x_num_unscaled)
            self.data.update(_opt_aux_num = opt_aux_num)
        if self._settings.store_lagr_multiplier == True:
            lam_g_num = self.lam_g_num
            self.data.update(_lam_g_num = lam_g_num)
        if len(self._settings.store_solver_stats) > 0:
            solver_stats = self.solver_stats
            store_solver_stats = self._settings.store_solver_stats
            self.data.update(**{stat_i: value for stat_i, value in solver_stats.items() if stat_i in store_solver_stats})

        # Update initial
        self._t0 = self._t0 + self._settings.t_step
        self._x0.master = castools.DM(x0)
        self._u0.master = castools.DM(u0)
        self._z0.master = castools.DM(z0)

        # Return control input:
        return u0.full()
    
    def solve(self):
        """Solves the optmization problem.

        The current problem is defined by the parameters in the
        :py:attr:`opt_p_num` CasADi structured Data.

        Typically, :py:attr:`opt_p_num` is prepared for the current iteration in the :py:func:`make_step` method.
        It is, however, valid and possible to directly set paramters in :py:attr:`opt_p_num` before calling :py:func:`solve`.

        The method updates the :py:attr:`opt_p_num` and :py:attr:`opt_x_num` attributes of the class.
        By resetting :py:attr:`opt_x_num` to the current solution, the method implicitly
        enables **warmstarting the optimizer** for the next iteration, since this vector is always used as the initial guess.

        .. warning::

            The method is part of the public API but it is generally not advised to use it.
            Instead we recommend to call :py:func:`make_step` at each iterations, which acts as a wrapper
            for :py:func:`solve`.

        :raises asssertion: Optimizer was not setup yet.

        :return: None
        :rtype: None
        """
        assert self.flags['setup'] == True, 'optimizer was not setup yet. Please call optimizer.setup().'

        solver_call_kwargs = {
            'x0': self.opt_x_num,
            'lbx': self._lb_opt_x,
            'ubx': self._ub_opt_x,
            'lbg': self.nlp_cons_lb,
            'ubg': self.nlp_cons_ub,
            'p': self.opt_p_num,
        }

        # Warmstarting the optimizer after the initial run:
        if self.flags['initial_run']:
            solver_call_kwargs.update({
                'lam_x0': self.lam_x_num,
                'lam_g0': self.lam_g_num,
            })



        r = self.S(**solver_call_kwargs)
        self.r_prev = copy.copy(r)
        # Note: .master accesses the underlying vector of the structure.
        self.opt_x_num.master = r['x']
        self.opt_f_num = r["f"]
        self.opt_x_num_unscaled.master = r['x']*self.opt_x_scaling
        self.opt_g_num = r['g']
        # Values of lagrange multipliers:
        self.lam_g_num = r['lam_g']
        self.lam_x_num = r['lam_x']
        self.solver_stats = self.S.stats()

        # Calculate values of auxiliary expressions (defined in model)
        self.opt_aux_num.master = self.opt_aux_expression_fun(
                self.opt_x_num,
                self.opt_p_num
            )
        
        # For warmstarting purposes: Flag that initial run has been completed.
        self.flags['initial_run'] = True
    
    def get_solution_dict(self):
        r = copy.copy(self.r_prev)
        r["p"] = self.opt_p_num.master.full()
        return r
    
    def save(self, path):
        if not path.endswith(".pkl"):
            path = os.path.join(path, "mpc.pkl")

        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        attributes = self.__dict__.copy()

        
        attributes.pop("nlp")
        attributes.pop("slack_cost")
        attributes.pop("mterm") if "mterm" in attributes else None
        attributes.pop("lterm") if "lterm" in attributes else None
        attributes.pop("_eps")
        attributes.pop("_opt_x")
        attributes.pop("opt_x_unscaled")
        attributes.pop("_opt_p")
        attributes.pop("_opt_aux")
        attributes.pop("_nlp_obj")
        attributes.pop("_nlp_cons")
        attributes.pop("_nl_cons")
        attributes.pop("aux_struct")

        nl_cons_list = copy.deepcopy(attributes["nl_cons_list"])

        func_input = attributes["model"]["x", "u", "z", "tvp", "p", "rlp"]
        for idx, item in enumerate(nl_cons_list):
            if item["expr_name"] == "default":
                continue
            nl_cons_list[idx]["expr"] = castools.Function(item["expr_name"], func_input, [item["expr"]])

        attributes["nl_cons_list"] = nl_cons_list


        p_template = self.get_p_template(attributes["n_combinations"])
        p_template.master = self.p_fun(0).master
        attributes["p_fun"] = p_template.master

        tvp_template = self.get_tvp_template()
        tvp_template.master = self.tvp_fun(0).master
        attributes["tvp_fun"] = tvp_template.master

        rlp_template = self.get_rlp_template()
        rlp_template.master = self.rlp_fun(0).master
        attributes["rlp_fun"] = rlp_template.master        

        DMStruct_list = []
        for key, value in attributes.items():
            if isinstance(value, (castools.structure3.DMStruct)):
                DMStruct_list.append(key)

        for key in DMStruct_list:
            attributes[key] = attributes[key].master

        with open(path, "wb") as f:
            pickle.dump(attributes, f)

        return
    
    @classmethod
    def load(cls, path):
        
        if not path.endswith(".pkl"):
            path = os.path.join(path, "mpc.pkl")

        with open(path, "rb") as f:
            attributes = pickle.load(f)

        model = attributes.pop("model")
        mpc = cls(model)

        _settings = attributes.pop("_settings")
        mpc._settings = _settings


        lterm = attributes.pop("lterm_fun")(model._x, model._u, model._z, model._tvp, model._p, model._rlp,)
        mterm = attributes.pop("mterm_fun")(model._x, model._tvp, model._p, model._rlp,)
        mpc.set_objective(mterm = mterm, lterm = lterm)

        mpc._x_scaling.master = attributes.pop("_x_scaling")
        mpc._z_scaling.master = attributes.pop("_z_scaling")
        mpc._u_scaling.master = attributes.pop("_u_scaling")

        mpc._x_lb.master = attributes.pop("_x_lb")
        mpc._x_ub.master = attributes.pop("_x_ub")

        mpc._z_lb.master = attributes.pop("_z_lb")
        mpc._z_ub.master = attributes.pop("_z_ub")

        mpc._u_lb.master = attributes.pop("_u_lb")
        mpc._u_ub.master = attributes.pop("_u_ub")

        mpc._x_terminal_lb.master = attributes.pop("_x_terminal_lb")
        mpc._x_terminal_ub.master = attributes.pop("_x_terminal_ub")

        mpc.rterm_factor.master = attributes.pop("rterm_factor")
        mpc.flags["set_rterm"] = True

        p_template = mpc.get_p_template(attributes.pop("n_combinations"))
        p_template.master = attributes.pop("p_fun")
        mpc.set_p_fun(lambda tnow: p_template)

        tvp_template = mpc.get_tvp_template()
        tvp_template.master = attributes.pop("tvp_fun")
        mpc.set_tvp_fun(lambda tnow: tvp_template)

        rlp_template = mpc.get_rlp_template()
        rlp_template.master = attributes.pop("rlp_fun")
        mpc.set_rlp_fun(lambda tnow: rlp_template)

        nl_cons_list = attributes.pop("nl_cons_list")
        nl_cons_input = mpc.model['x', 'u', 'z', 'tvp', 'p', 'rlp']
        for nl_cons in nl_cons_list:
            if nl_cons["expr_name"] == "default":
                continue
            try:
                nl_cons["expr"] = nl_cons["expr"](*nl_cons_input)
            except Exception:
                nl_cons["expr"] = nl_cons["expr"](*mpc.model['x', 'u', 'z', 'tvp', 'p'])
            mpc.nl_cons_list.append(nl_cons)

        mpc.slack_vars_list = attributes.pop("slack_vars_list")

        mpc.prepare_nlp()

        mpc.create_nlp()
        mpc.S = attributes.pop("S")
        mpc.data = attributes.pop("data")

        mpc._nlp_cons_lb = attributes.pop("_nlp_cons_lb")
        mpc._nlp_cons_ub = attributes.pop("_nlp_cons_ub")
        return mpc