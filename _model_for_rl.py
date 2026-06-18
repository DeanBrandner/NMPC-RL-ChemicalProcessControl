# This file contains code derived from do-mpc.
# do-mpc is licensed under the GNU Lesser General Public License v3.0.
# Modifications Copyright (C) 2026 Dean Brandner.
#
# This file is licensed under the GNU Lesser General Public License v3.0.

"""do-mpc model extensions for reinforcement-learning use cases.

This module adds a reinforcement-learning parameter structure to the standard
do-mpc ``Model`` class so that models can expose additional symbolic variables
through the ``_rlp`` namespace. The rest of the model API follows the native
do-mpc behavior.
"""

from do_mpc.model import Model
from typing import Union, Tuple
import casadi.tools as castools 

class RL_Model(Model):
    """do-mpc model with an additional reinforcement-learning parameter set.

    The class behaves like a regular do-mpc model, but it predefines the
    ``_rlp`` symbolic structure so that RL-specific corrective terms and
    backoff parameters can be embedded in the symbolic model.
    """

    def __init__(self, model_type: str = "discrete", symvar_type: str = "SX") -> None:
        """Initialize the model and create the reinforcement-learning parameter slot."""
        super().__init__(model_type = model_type, symvar_type = symvar_type)
        self._rlp =   {'name': ['default'], 'var': [self.sv.sym('default', (0,0))]}

    def set_variable(self, var_type:str, var_name:str, shape:Union[int,Tuple]=(1,1), input_type_integer:bool=False)->Union[castools.SX,castools.MX]:
        """Introduce new variables to the model class. Define variable type, name and shape (optional).

        **Example:**

        ::

            # States struct (optimization variables):
            C_a = model.set_variable(var_type='_x', var_name='C_a', shape=(1,1))
            T_K = model.set_variable(var_type='_x', var_name='T_K', shape=(1,1))

            # Input struct (optimization variables):
            Q_dot = model.set_variable(var_type='_u', var_name='Q_dot')

            # Fixed parameters:
            alpha = model.set_variable(var_type='_p', var_name='alpha')

        Note: 
            ``var_type`` allows a shorthand notation e.g. ``_x`` which is equivalent to ``states``.

            ``input_type_integer`` can be set to `True` for inputs that are treated as integer decision variables.

        Args:
            var_type : Declare the type of the variable.
            var_name : Set a user-defined name for the parameter. The names are reused throughout do_mpc.
            shape : Shape of the current variable (optional), defaults to ``1``.
            input_type_integer : define an integer input variable, defaults to ``False``.
               
        The following types of **var_type** are valid (long or short name is possible):

        ===========================  ===========  ============================
        Long name                    short name   Remark
        ===========================  ===========  ============================
        ``states``                   ``_x``       Required
        ``inputs``                   ``_u``       Optional
        ``algebraic``                ``_z``       Optional
        ``parameter``                ``_p``       Optional
        ``timevarying_parameter``    ``_tvp``     Optional
        ``reinforcement_parameter``  ``_rlp``     Optional
        ===========================  ===========  ============================

        Raises:
            assertion: **var_type** must be string
            assertion: **var_name** must be string
            assertion: **shape** must be tuple or int
            assertion: **input_type_integer** must be boolean
            assertion: Cannot call after :py:func:`setup`.

        Returns:
            Returns the newly created symbolic variable.
        """
        assert self.flags['setup'] == False, 'Cannot call .set_variable after setup.'
        assert isinstance(var_type, str), 'var_type must be str, you have: {}'.format(type(var_type))
        assert isinstance(var_name, str), 'var_name must be str, you have: {}'.format(type(var_name))
        assert isinstance(input_type_integer, bool), 'integer must be boolean, you have: {}'.format(
            type(input_type_integer))
        assert isinstance(shape, (tuple,int)), 'shape must be tuple or int, you have: {}'.format(type(shape))
        if input_type_integer == True:
            assert var_type == '_u', 'Only inputs can be declared as integer variables, you tried to declare {} as integer variable'.format(
                var_type)

        # Get short names:
        var_type =var_type.replace('states', '_x'
            ).replace('inputs', '_u'
            ).replace('algebraic', '_z'
            ).replace('parameter', '_p'
            ).replace('timevarying_parameter', '_tvp'
            ).replace('reinforcement_parameter', '_rlp')

        # Check validity of var_type:
        assert var_type in ['_x','_u','_z','_p','_tvp', '_rlp'], 'Trying to set non-existing variable var_type: {} with var_name {}'.format(var_type, var_name)
        # Check validity of var_name:
        assert var_name not in getattr(self,var_type)['name'], 'The variable name {} for type {} already exists.'.format(var_name, var_type)

        # Create variable:
        var = self.sv.sym(var_name, shape)


        # Extend var list with new entry:
        getattr(self, var_type)['var'].append(var)
        getattr(self, var_type)['name'].append(var_name)

        # Update list of integer_inputs with the name of the current input
        if var_type == '_u' and input_type_integer == True: self.integer += [var_name]


        return var
    
    def __setstate__(self, state):
        """
        Sets the state of the :py:class:`Model` for unpickling. Please see :py:func:`__getstate__` for details and restrictions on pickling.
        """
        self.__dict__.update(state)

        # Update expressions with new symbolic variables created when unpickling:
        self._rhs = self._rhs(self._rhs_fun(self._x, self._u, self._z, self._tvp, self._p, self._rlp, self._w))
        self._alg = self._alg(self._alg_fun(self._x, self._u, self._z, self._tvp, self._p, self._rlp, self._w))
        self._aux_expression = self._aux_expression(self._aux_expression_fun(self._x, self._u, self._z, self._tvp, self._p, self._rlp))
        self._y_expression = self._y_expression(self._meas_fun(self._x, self._u, self._z, self._tvp, self._p, self._rlp, self._v))

    def __getitem__(self, ind):
        """The :py:class:`Model` class supports the ``__getitem__`` method,
        which can be used to retrieve the model variables (see attribute list).

        ::

            # Query the states like this:
            x = model.x
            # or like this:
            x = model['x']

        This also allows to retrieve multiple variables simultaneously:

        ::

            x, u, z = model['x','u','z']
        """
        var_names = ['x','u','z','p','tvp','rlp', 'y','aux', 'w']
        if isinstance(ind, tuple):
            val = []
            for ind_i in ind:
                assert ind_i in var_names, 'The queried variable {} is not valid. Choose from {}.'.format(ind_i, var_names)
                val.append(getattr(self, ind_i))
            return val
        else:
            val = getattr(self,ind)

        return val
    
    @property
    def rlp(self):
        """ Reinforcement learning parameters.
            CasADi symbolic structure, can be indexed with user-defined variable names.

            Note:
                Variables are introduced with :py:func:`Model.set_variable` Use this property only to query
                variables.

            **Example:**

            ::

                model = do_mpc.model.Model('continuous')
                model.set_variable('_rlp','temperature', shape=(4,1))
                # Query:
                model.rlp['temperature', 0] # 0th element of variable
                model.rlp['temperature']    # all elements of variable
                model.rlp['temperature', 0:2]    # 0th and 1st element
            Useful CasADi symbolic structure methods:

            * ``.shape``

            * ``.keys()``

            * ``.labels()``

            Raises:
                assertion: Cannot set model variables directly Use set_variable instead.
        """
        return self._getvar('_rlp')
    
    @rlp.setter
    def rlp(self, val):
        raise Exception('Cannot set model variables directly Use set_variable instead.')
    
    def set_expression(self, expr_name:str, expr:Union[castools.SX,castools.MX])->Union[castools.SX,castools.MX]:
        """Introduce new expression to the model class. Expressions are not required but can be used
        to extract further information from the model.
        Expressions must be formulated with respect to ``_x``, ``_u``, ``_z``, ``_tvp``, ``_rlp``, ``_p``.

        **Example:**

        Maybe you are interested in monitoring the product of two states?

        ::

            Introduce two scalar states:
            x_1 = model.set_variable('_x', 'x_1')
            x_2 = model.set_variable('_x', 'x_2')

            # Introduce expression:
            model.set_expression('x1x2', x_1*x_2)

        This new expression ``x1x2`` is then available in all **do-mpc** modules utilizing
        this model instance. It can be set, e.g. as the cost function in :py:class:`do_mpc.controller.MPC`
        or simply used in a graphical representation of the simulated / controlled system.

        Args:
            expr_name : Arbitrary name for the given expression. Names are used for key word indexing.
            expr : CasADi SX or MX function depending on ``_x``, ``_u``, ``_z``, ``_tvp``, ``_rlp``, ``_p``.

        Raises:
            assertion: expr_name must be str
            assertion: expr must be a casadi SX or MX type
            assertion: Cannot call after :py:func:`setup`.

        Returns:
            Returns the newly created expression. Expression can be used e.g. for the RHS.
        """
        assert self.flags['setup'] == False, 'Cannot call .set_expression after setup'
        assert isinstance(expr_name, str), 'expr_name must be str, you have: {}'.format(type(expr_name))
        assert isinstance(expr, (castools.SX, castools.MX)), 'expr must be a casadi SX or MX type, you have:{}'.format(type(expr))

        self._aux_expression.append(castools.entry(expr_name, expr = expr))

        # Create variable:
        var = self.sv.sym(expr_name, expr.shape)
        self._aux['var'].append(var)
        self._aux['name'].append(expr_name)

        return expr
    
    def set_meas(self, meas_name:str, expr:Union[castools.SX,castools.MX], meas_noise:bool=True)->Union[castools.SX,castools.MX]:
        """Introduce new measurable output to the model class.

        .. math::

            y = h(x(t),u(t),z(t),p(t),p_{\\text{tv}}(t), p_{\\text{RL}}(t)) + v(t)

        or in case of discrete dynamics:

        .. math::

            y_k = h(x_k,u_k,z_k,p_k,p_{\\text{tv},k}, p_{\\text{RL},k}) + v_k

        By default, the model assumes state-feedback (all states are measured outputs).
        Expressions must be formulated with respect to ``_x``, ``_u``, ``_z``, ``_tvp``, ``_rlp``, ``_p``.

        Be default, it is assumed that the measurements experience additive noise :math:`v_k`.
        This can be deactivated for individual measured variables by changing the boolean variable
        ``meas_noise`` to ``False``.
        Note that measurement noise is only meaningful for state-estimation and will not affect the controller.
        Furthermore, it can be set with each :py:class:`do_mpc.simulator.Simulator` call to obtain imperfect outputs.

        Note:
            For moving horizon estimation it is suggested to declare all inputs (``_u``) and e.g. a subset of states (``_x``) as
            measurable output. Some other MHE formulations treat inputs separately.

        Note:
            It is often suggested to deactivate measurement noise for "measured" inputs (``_u``).
            These can typically seen as certain variables.

        **Example:**

        ::

            # Introduce states:
            x_meas = model.set_variable('_x', 'x', 3) # 3 measured states (vector)
            x_est = model.set_variable('_x', 'x', 3) # 3 estimated states (vector)
            # and inputs:
            u = model.set_variable('_u', 'u', 2) # 2 inputs (vector)

            # define measurements:
            model.set_meas('x_meas', x_meas)
            model.set_meas('u', u)

        Args:
            meas_name : Arbitrary name for the given expression. Names are used for key word indexing.
            expr : CasADi SX or MX function depending on ``_x``, ``_u``, ``_z``, ``_tvp``,  ``_rlp``, ``_p``.
            meas_noise : Set if the measurement equation is disturbed by additive noise.

        Raises:
            assertion: expr_name must be str
            assertion: expr must be a casadi SX or MX type
            assertion: Cannot call after :py:func:`setup`.

        Returns:
            Returns the newly created measurement expression.
        """
        assert self.flags['setup'] == False, 'Cannot call .set_meas after setup'
        assert isinstance(meas_name, str), 'meas_name must be str, you have: {}'.format(type(meas_name))
        assert isinstance(expr, (castools.SX, castools.MX)), 'expr must be a casadi SX or MX type, you have:{}'.format(type(expr))
        assert isinstance(meas_noise, bool), 'meas_noise must be of type boolean. You have: {}'.format(type(meas_noise))

        # Create a new process noise variable and add it to the rhs equation.
        if meas_noise:
            var = self.sv.sym(meas_name+'_noise', expr.shape[0])

            self._v['name'].append(meas_name+'_noise')
            self._v['var'].append(var)
            expr += var

        self._y_expression.append(castools.entry(meas_name, expr = expr))

        # Create variable:
        var = self.sv.sym(meas_name, expr.shape)
        self._y['var'].append(var)
        self._y['name'].append(meas_name)

        return expr
    
    def set_rhs(self, var_name:str, expr:Union[castools.SX,castools.MX], process_noise:bool=False)->None:
        """Formulate the right hand side (rhs) of the ODE:

        .. math::

            \\dot{x}(t) = f(x(t),u(t),z(t),p(t),p_{\\text{tv}}(t), p_{\\text{RL}}(t)) + w(t),

        or the update equation in case of discrete dynamics:

        .. math::

            x_{k+1} = f(x_k,u_k,z_k,p_k,p_{\\text{tv},k}, p_{\\text{RL},k}) + w_k,

        Each defined state variable must have a respective equation (of matching dimension)
        for the rhs. Match the rhs with the state by choosing the corresponding names.
        rhs must be formulated with respect to ``_x``, ``_u``, ``_z``, ``_tvp``, ``_rlp``, ``_p``.

        **Example**:

        ::

            tank_level = model.set_variable('states', 'tank_level')
            tank_temp = model.set_variable('states', 'tank_temp')

            tank_level_next = 0.5*tank_level
            tank_temp_next = ...

            model.set_rhs('tank_level', tank_level_next)
            model.set_rhs('tank_temp', tank_temp_next)

        Optionally, set ``process_noise = True`` to introduce an additive process noise variable.
        This is  meaningful for the :py:class:`do_mpc.estimator.MHE` (See :py:func:`do_mpc.estimator.MHE.set_default_objective` for more details).
        Furthermore, it can be set with each :py:class:`do_mpc.simulator.Simulator` call to obtain imperfect (realistic) simulation results.

        Args:
            var_name : Reference to previously introduced state names (with :py:func:`Model.set_variable`)
            expr : CasADi SX or MX function depending on ``_x``, ``_u``, ``_z``, ``_tvp``, ``_rlp``, ``_p``.
            process_noise : Make the respective state variable non-deterministic.

        Raises:
            assertion: var_name must be str
            assertion: expr must be a casadi SX or MX type
            assertion: var_name must refer to the previously defined states
            assertion: Cannot call after :py:func`setup`.
        """
        assert self.flags['setup'] == False, 'Cannot call .set_rhs after .setup.'
        assert isinstance(var_name, str), 'var_name must be str, you have: {}'.format(type(var_name))
        assert isinstance(expr, (castools.SX, castools.MX, castools.DM)), 'expr must be a casadi SX, MX or DM type, you have:{}'.format(type(expr))
        assert var_name in self._x['name'], 'var_name must refer to the previously defined states ({}). You have: {}'.format(self._x['name'], var_name)

        # Create a new process noise variable and add it to the rhs equation.
        if process_noise:
            if self.symvar_type == 'MX':
                var = castools.MX.sym(var_name+'_noise', expr.shape[0])
            else:
                var = castools.SX.sym(var_name+'_noise', expr.shape[0])

            self._w['name'].append(var_name + '_noise')
            self._w['var'].append(var)
            expr += var
        self.rhs_list.extend([{'var_name': var_name, 'expr': expr}])

    def set_alg(self, expr_name:str, expr:Union[castools.SX,castools.MX])->None:
        """ Introduce new algebraic equation to model.

        For the continous time model, the expression must be formulated as

        .. math::

           0 = g(x(t),u(t),z(t),p(t),p_{\\text{tv}}(t), p_{\\text{RL}}(t))


        or for a ``discrete`` model:

        .. math::

           0 = g(x_k,u_k,z_k,p_k,p_{\\text{tv},k}, p_{\\text{RL},k})

        Note:
            For the introduced algebraic variables :math:`z \in \mathbb{R}^{n_z}`
            it is required to introduce exactly :math:`n_z` algebraic equations.
            Otherwise :py:meth:`setup` will throw an error message.

        Args:
            expr_name : Name of the introduced expression
            expr : CasADi SX or MX function depending on ``_x``, ``_u``, ``_z``, ``_tvp``, ``_rlp``, ``_p``.
        """
        assert self.flags['setup'] == False, 'Cannot call .set_alg after .setup.'
        assert isinstance(expr_name, str), 'expr_name must be str, you have: {}'.format(type(expr_name))
        assert isinstance(expr, (castools.SX, castools.MX, castools.DM)), 'expr must be a casadi SX, MX or DM type, you have:{}'.format(type(expr))

        self.alg_list.append(castools.entry(expr_name, expr = expr))

    def setup(self)->None:
        """Setup method must be called to finalize the modelling process.
        All required model variables must be declared.
        The right hand side expression for ``_x`` must have been set with :py:func:`set_rhs`.

        Sets default measurement function (state feedback) if :py:func:`set_meas` was not called.

        Warnings:
            After calling :py:func:`setup`, the model is locked and no further variables,
            expressions etc. can be set.

        Raises:
            assertion: Definition of right hand side (rhs) is incomplete
        """
        # Set all states as measurements if set_meas was not called by user.
        if not self._y_expression:
            for name, var in zip(self._x['name'], self._x['var']):
                self.set_meas(name, var)

        # Write self._y_expression (measurement equations) as struct symbolic expression structures.
        self._y_expression = self.sv.struct(self._y_expression)

        # Create structure from listed symbolic variables:
        _x =  self._convert2struct(self._x)
        _w =  self._convert2struct(self._w)
        _v =  self._convert2struct(self._v)
        _u =  self._convert2struct(self._u)
        _z =  self._convert2struct(self._z)
        _p =  self._convert2struct(self._p)
        _tvp =  self._convert2struct(self._tvp)
        _rlp = self._convert2struct(self._rlp)
        _aux =  self._convert2struct(self._aux)
        _y =  self._convert2struct(self._y)

        # Write self._aux_expression.
        self._aux_expression = self.sv.struct(self._aux_expression)


        # Create alg equations:
        self._alg = self.sv.struct(self.alg_list)

        # Create mutable struct with identical structure as _x to hold the right hand side.
        self._rhs = self.sv.struct(_x)

        # Set the expressions in self._rhs with the previously defined SX.sym variables.
        # Check if an expression is set for every state of the system.
        _x_names = set(self._x['name'])
        for rhs_i in self.rhs_list:
            self._rhs[rhs_i['var_name']] = rhs_i['expr']
            _x_names -= set([rhs_i['var_name']])
        assert len(_x_names) == 0, 'Definition of right hand side (rhs) is incomplete. Missing: {}. Use: set_rhs to define expressions.'.format(_x_names)

        var_dict_list = [self._x, self._w, self._v, self._u, self._z, self._p, self._tvp, self._rlp]
        sym_struct_list = [_x, _w, _v, _u, _z, _p, _tvp, _rlp]

        self._rhs = self._substitute_struct_vars(var_dict_list, sym_struct_list, self._rhs)
        self._alg = self._substitute_struct_vars(var_dict_list, sym_struct_list, self._alg)
        self._aux_expression = self._substitute_struct_vars(var_dict_list, sym_struct_list, self._aux_expression)
        self._y_expression = self._substitute_struct_vars(var_dict_list, sym_struct_list, self._y_expression)

        self._substitute_exported_vars(var_dict_list, sym_struct_list)

        self._x = _x
        self._w = _w
        self._v = _v
        self._u = _u
        self._z = _z
        self._p = _p
        self._tvp = _tvp
        self._rlp = _rlp
        self._y = _y
        self._aux = _aux
        
        A_lin_expr = castools.jacobian(self._rhs,self._x)
        B_lin_expr = castools.jacobian(self._rhs,self._u)
        C_lin_expr = castools.jacobian(self._y_expression,self._x)
        D_lin_expr = castools.jacobian(self._y_expression,self._u)

        # Declare functions for the right hand side and the aux_expressions.
        self._rhs_fun = castools.Function('rhs_fun',
                                 [_x, _u, _z, _tvp, _p, _rlp, _w], [self._rhs],
                                 ["_x", "_u", "_z", "_tvp", "_p", "_rlp", "_w"], ["_rhs"])
        self._alg_fun = castools.Function('alg_fun',
                                 [_x, _u, _z, _tvp, _p, _rlp, _w], [self._alg],
                                 ["_x", "_u", "_z", "_tvp", "_p", "_rlp", "_w"], ["_alg"])
        self._aux_expression_fun = castools.Function('aux_expression_fun',
                                            [_x, _u, _z, _tvp, _p, _rlp], [self._aux_expression],
                                            ["_x", "_u", "_z", "_tvp", "_p", "_rlp"], ["_aux_expression"])
        self._meas_fun = castools.Function('meas_fun',
                                  [_x, _u, _z, _tvp, _p, _rlp, _v], [self._y_expression],
                                  ["_x", "_u", "_z", "_tvp", "_p", "_rlp", "_v"], ["_y_expression"])
        self.A_fun = castools.Function('A_fun',
                              [_x, _u, _z, _tvp, _p, _rlp, _w],[A_lin_expr],
                              ["_x", "_u", "_z", "_tvp", "_p", "_rlp", "_w"],["A_lin_expr"])
        self.B_fun = castools.Function('B_fun',
                              [_x, _u, _z, _tvp, _p, _rlp, _w],[B_lin_expr],
                              ["_x", "_u", "_z", "_tvp", "_p", "_rlp", "_w"],["B_lin_expr"])
        self.C_fun = castools.Function('C_fun',
                              [_x, _u, _z, _tvp, _p, _rlp, _v],[C_lin_expr],
                              ["_x", "_u", "_z", "_tvp", "_p", "_rlp", "_v"],["C_lin_expr"])
        self.D_fun = castools.Function('D_fun',
                              [_x, _u, _z, _tvp, _p, _rlp, _v],[D_lin_expr],
                              ["_x", "_u", "_z", "_tvp", "_p", "_rlp", "_v"],["D_lin_expr"]) 

        # Create and store some information about the model regarding number of variables for
        # _x, _y, _u, _z, _tvp, _p, _aux
        self.n_x = self._x.shape[0]
        self.n_y = self._y.shape[0]
        self.n_u = self._u.shape[0]
        self.n_z = self._z.shape[0]
        self.n_tvp = self._tvp.shape[0]
        self.n_p = self._p.shape[0]
        self.n_rlp = self._rlp.shape[0]
        self.n_aux = self._aux_expression.shape[0]
        self.n_w = self._w.shape[0]
        self.n_v = self._v.shape[0]

        msg = 'Must have the same number of algebraic equations (you have {}) and variables (you have {}).'
        assert self.n_z == self._alg.shape[0], msg.format(self._alg.shape[0], self.n_z)

        # Remove temporary storage for the symbolic variables. This allows to pickle the class.
        delattr(self, 'rhs_list')
        delattr(self, 'alg_list')

        self.flags['setup'] = True
