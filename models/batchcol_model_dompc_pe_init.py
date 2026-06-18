#   This file is part of do-mpc
#
#   do-mpc: An environment for the easy, modular and efficient implementation of
#        robust nonlinear model predictive control
#
#   Copyright (c) 2014-2019 Sergio Lucia, Alexandru Tatulea-Codrean
#                        TU Dortmund. All rights reserved
#
#   do-mpc is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as
#   published by the Free Software Foundation, either version 3
#   of the License, or (at your option) any later version.
#
#   do-mpc is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with do-mpc.  If not, see <http://www.gnu.org/licenses/>.

import casadi as ca
import do_mpc


def template_model_for_pe_initialization(
    meas_noise_bool: bool = False,
) -> do_mpc.model.Model:
    """
    Variant of ``template_model_for_pe`` intended for initialization runs of the
    parameter estimator. The quantities

        ``e0_E_murphree``, ``e0_rr_err``,
        ``e0_x_feed_tr9_c1``, ``e0_x_feed_tr9_c2``,
        ``e0_F_feed_tr9``, ``e0_F_B``

    are lifted from ``_p`` (parameters) to ``_u`` (control inputs), so that
    time-varying trajectories for these quantities can be fed into a simulator
    via ``make_step``. All remaining ``_p`` entries are kept as before.
    """
    model_type = "continuous"  # either 'discrete' or 'continuous'
    symvar_type = "SX"
    model = do_mpc.model.Model(model_type, symvar_type)

    # fmt:off
    def fun_210593__vaporenthalpy(std_T,std_greek_Deltah_f,std_T_ref,std_c_V_p):  # noqa: E501,E231,E306
        std_h_V = ((std_c_V_p*((std_T-std_T_ref)))+std_greek_Deltah_f)  # noqa: E501,E226
        return std_h_V
    def fun_213932__liquid_enthalpy_adj(std_T,std_greek_Deltah_f,std_A_LV,std_B_LV,std_C_LV,std_T_ref,std_c_V_p):  # noqa: E501,E231,E306
        std_h_L = (((std_c_V_p*((std_T-std_T_ref)))+std_greek_Deltah_f)-(((std_A_LV+(std_B_LV*((std_T/std_T_ref))))+(std_C_LV*(((std_T/std_T_ref)))**(1.0*2.0)))))  # noqa: E501,E226
        return std_h_L

    # Constants
    e0_greek_Deltah_f_c1 = -234.0
    e0_greek_Deltah_f_c2 = -241.0
    e0_greek_epsiv_weir = 1.0E-4
    e0_greek_lambda_c1 = 95.68
    e0_greek_lambda_c2 = 506.7
    e0_greek_pi = 3.1415926
    e0_A_c1 = 5.24677
    e0_A_LV_c1 = 44.27270632
    e0_A_c2 = 5.08354
    e0_A_LV_c2 = 52.28384694
    e0_B_c1 = 1598.673
    e0_B_LV_c1 = 13.09430159
    e0_B_c2 = 1663.125
    e0_B_LV_c2 = -4.49906401
    e0_C_c1 = -46.424
    e0_C_LV_c1 = -14.78454201
    e0_C_c2 = -45.622
    e0_C_LV_c2 = -3.79895861
    # e0_E_murphree = 0.7000000001071379
    # e0_E_murphree = 0.5
    # e0_E_murphree = 0.475
    # e0_E_murphree = 0.65
    e0_M_c1 = 0.046
    e0_M_c2 = 0.018
    # e0_Q_err_R = 0.98647356893109
    e0_R = 8.314
    e0_T_ref = 298.15
    e0_c_V_p_c1 = 0.075
    e0_c_V_p_c2 = 0.036
    e0_d_col = 0.05
    # e0_rr_err = -0.146549383828861
    e0_v_L_c1 = 5.869E-5
    e0_v_L_c2 = 1.813E-5
    # Dynamic/Differential states
    e0_HU_tr1_c1 = model.set_variable(var_type='_x', var_name="e0_HU_tr1_c1", shape=(1,1))  # noqa: E501
    e0_HU_tr2_c1 = model.set_variable(var_type='_x', var_name="e0_HU_tr2_c1", shape=(1,1))  # noqa: E501
    e0_HU_tr3_c1 = model.set_variable(var_type='_x', var_name="e0_HU_tr3_c1", shape=(1,1))  # noqa: E501
    e0_HU_tr4_c1 = model.set_variable(var_type='_x', var_name="e0_HU_tr4_c1", shape=(1,1))  # noqa: E501
    e0_HU_tr5_c1 = model.set_variable(var_type='_x', var_name="e0_HU_tr5_c1", shape=(1,1))  # noqa: E501
    e0_HU_tr6_c1 = model.set_variable(var_type='_x', var_name="e0_HU_tr6_c1", shape=(1,1))  # noqa: E501
    e0_HU_tr7_c1 = model.set_variable(var_type='_x', var_name="e0_HU_tr7_c1", shape=(1,1))  # noqa: E501
    e0_HU_tr8_c1 = model.set_variable(var_type='_x', var_name="e0_HU_tr8_c1", shape=(1,1))  # noqa: E501
    e0_HU_tr1_c2 = model.set_variable(var_type='_x', var_name="e0_HU_tr1_c2", shape=(1,1))  # noqa: E501
    e0_HU_tr2_c2 = model.set_variable(var_type='_x', var_name="e0_HU_tr2_c2", shape=(1,1))  # noqa: E501
    e0_HU_tr3_c2 = model.set_variable(var_type='_x', var_name="e0_HU_tr3_c2", shape=(1,1))  # noqa: E501
    e0_HU_tr4_c2 = model.set_variable(var_type='_x', var_name="e0_HU_tr4_c2", shape=(1,1))  # noqa: E501
    e0_HU_tr5_c2 = model.set_variable(var_type='_x', var_name="e0_HU_tr5_c2", shape=(1,1))  # noqa: E501
    e0_HU_tr6_c2 = model.set_variable(var_type='_x', var_name="e0_HU_tr6_c2", shape=(1,1))  # noqa: E501
    e0_HU_tr7_c2 = model.set_variable(var_type='_x', var_name="e0_HU_tr7_c2", shape=(1,1))  # noqa: E501
    e0_HU_tr8_c2 = model.set_variable(var_type='_x', var_name="e0_HU_tr8_c2", shape=(1,1))  # noqa: E501
    e0_U_tr1 = model.set_variable(var_type='_x', var_name="e0_U_tr1", shape=(1,1))  # noqa: E501
    e0_U_tr2 = model.set_variable(var_type='_x', var_name="e0_U_tr2", shape=(1,1))  # noqa: E501
    e0_U_tr3 = model.set_variable(var_type='_x', var_name="e0_U_tr3", shape=(1,1))  # noqa: E501
    e0_U_tr4 = model.set_variable(var_type='_x', var_name="e0_U_tr4", shape=(1,1))  # noqa: E501
    e0_U_tr5 = model.set_variable(var_type='_x', var_name="e0_U_tr5", shape=(1,1))  # noqa: E501
    e0_U_tr6 = model.set_variable(var_type='_x', var_name="e0_U_tr6", shape=(1,1))  # noqa: E501
    e0_U_tr7 = model.set_variable(var_type='_x', var_name="e0_U_tr7", shape=(1,1))  # noqa: E501
    e0_U_tr8 = model.set_variable(var_type='_x', var_name="e0_U_tr8", shape=(1,1))  # noqa: E501
    e0_HU_tr9_c1 = model.set_variable(var_type='_x', var_name="e0_HU_tr9_c1", shape=(1,1))  # noqa: E501
    e0_HU_tr9_c2 = model.set_variable(var_type='_x', var_name="e0_HU_tr9_c2", shape=(1,1))  # noqa: E501
    e0_U_tr9 = model.set_variable(var_type='_x', var_name="e0_U_tr9", shape=(1,1))  # noqa: E501
    e0_HU_D_c1 = model.set_variable(var_type='_x', var_name="e0_HU_D_c1", shape=(1,1))  # noqa: E501
    e0_HU_D_c2 = model.set_variable(var_type='_x', var_name="e0_HU_D_c2", shape=(1,1))  # noqa: E501

    # Algebraic states
    e0_h_L_tr0_c1 = model.set_variable(var_type='_z', var_name="e0_h_L_tr0_c1", shape=(1,1))  # noqa: E501
    e0_h_L_tr0_c2 = model.set_variable(var_type='_z', var_name="e0_h_L_tr0_c2", shape=(1,1))  # noqa: E501
    e0_h_L_tr1_c1 = model.set_variable(var_type='_z', var_name="e0_h_L_tr1_c1", shape=(1,1))  # noqa: E501
    e0_h_L_tr1_c2 = model.set_variable(var_type='_z', var_name="e0_h_L_tr1_c2", shape=(1,1))  # noqa: E501
    e0_h_L_tr2_c1 = model.set_variable(var_type='_z', var_name="e0_h_L_tr2_c1", shape=(1,1))  # noqa: E501
    e0_h_L_tr2_c2 = model.set_variable(var_type='_z', var_name="e0_h_L_tr2_c2", shape=(1,1))  # noqa: E501
    e0_h_L_tr3_c1 = model.set_variable(var_type='_z', var_name="e0_h_L_tr3_c1", shape=(1,1))  # noqa: E501
    e0_h_L_tr3_c2 = model.set_variable(var_type='_z', var_name="e0_h_L_tr3_c2", shape=(1,1))  # noqa: E501
    e0_h_L_tr4_c1 = model.set_variable(var_type='_z', var_name="e0_h_L_tr4_c1", shape=(1,1))  # noqa: E501
    e0_h_L_tr4_c2 = model.set_variable(var_type='_z', var_name="e0_h_L_tr4_c2", shape=(1,1))  # noqa: E501
    e0_h_L_tr5_c1 = model.set_variable(var_type='_z', var_name="e0_h_L_tr5_c1", shape=(1,1))  # noqa: E501
    e0_h_L_tr5_c2 = model.set_variable(var_type='_z', var_name="e0_h_L_tr5_c2", shape=(1,1))  # noqa: E501
    e0_h_L_tr6_c1 = model.set_variable(var_type='_z', var_name="e0_h_L_tr6_c1", shape=(1,1))  # noqa: E501
    e0_h_L_tr6_c2 = model.set_variable(var_type='_z', var_name="e0_h_L_tr6_c2", shape=(1,1))  # noqa: E501
    e0_h_L_tr7_c1 = model.set_variable(var_type='_z', var_name="e0_h_L_tr7_c1", shape=(1,1))  # noqa: E501
    e0_h_L_tr7_c2 = model.set_variable(var_type='_z', var_name="e0_h_L_tr7_c2", shape=(1,1))  # noqa: E501
    e0_h_L_tr8_c1 = model.set_variable(var_type='_z', var_name="e0_h_L_tr8_c1", shape=(1,1))  # noqa: E501
    e0_h_L_tr8_c2 = model.set_variable(var_type='_z', var_name="e0_h_L_tr8_c2", shape=(1,1))  # noqa: E501
    e0_h_L_tr9_c1 = model.set_variable(var_type='_z', var_name="e0_h_L_tr9_c1", shape=(1,1))  # noqa: E501
    e0_h_L_tr9_c2 = model.set_variable(var_type='_z', var_name="e0_h_L_tr9_c2", shape=(1,1))  # noqa: E501
    e0_h_V_tr1_c1 = model.set_variable(var_type='_z', var_name="e0_h_V_tr1_c1", shape=(1,1))  # noqa: E501
    e0_h_V_tr1_c2 = model.set_variable(var_type='_z', var_name="e0_h_V_tr1_c2", shape=(1,1))  # noqa: E501
    e0_h_V_tr2_c1 = model.set_variable(var_type='_z', var_name="e0_h_V_tr2_c1", shape=(1,1))  # noqa: E501
    e0_h_V_tr2_c2 = model.set_variable(var_type='_z', var_name="e0_h_V_tr2_c2", shape=(1,1))  # noqa: E501
    e0_h_V_tr3_c1 = model.set_variable(var_type='_z', var_name="e0_h_V_tr3_c1", shape=(1,1))  # noqa: E501
    e0_h_V_tr3_c2 = model.set_variable(var_type='_z', var_name="e0_h_V_tr3_c2", shape=(1,1))  # noqa: E501
    e0_h_V_tr4_c1 = model.set_variable(var_type='_z', var_name="e0_h_V_tr4_c1", shape=(1,1))  # noqa: E501
    e0_h_V_tr4_c2 = model.set_variable(var_type='_z', var_name="e0_h_V_tr4_c2", shape=(1,1))  # noqa: E501
    e0_h_V_tr5_c1 = model.set_variable(var_type='_z', var_name="e0_h_V_tr5_c1", shape=(1,1))  # noqa: E501
    e0_h_V_tr5_c2 = model.set_variable(var_type='_z', var_name="e0_h_V_tr5_c2", shape=(1,1))  # noqa: E501
    e0_h_V_tr6_c1 = model.set_variable(var_type='_z', var_name="e0_h_V_tr6_c1", shape=(1,1))  # noqa: E501
    e0_h_V_tr6_c2 = model.set_variable(var_type='_z', var_name="e0_h_V_tr6_c2", shape=(1,1))  # noqa: E501
    e0_h_V_tr7_c1 = model.set_variable(var_type='_z', var_name="e0_h_V_tr7_c1", shape=(1,1))  # noqa: E501
    e0_h_V_tr7_c2 = model.set_variable(var_type='_z', var_name="e0_h_V_tr7_c2", shape=(1,1))  # noqa: E501
    e0_h_V_tr8_c1 = model.set_variable(var_type='_z', var_name="e0_h_V_tr8_c1", shape=(1,1))  # noqa: E501
    e0_h_V_tr8_c2 = model.set_variable(var_type='_z', var_name="e0_h_V_tr8_c2", shape=(1,1))  # noqa: E501
    e0_h_V_tr9_c1 = model.set_variable(var_type='_z', var_name="e0_h_V_tr9_c1", shape=(1,1))  # noqa: E501
    e0_h_V_tr9_c2 = model.set_variable(var_type='_z', var_name="e0_h_V_tr9_c2", shape=(1,1))  # noqa: E501
    e0_h_feed_tr9_c1 = model.set_variable(var_type='_z', var_name="e0_h_feed_tr9_c1", shape=(1,1))  # noqa: E501
    e0_h_feed_tr9_c2 = model.set_variable(var_type='_z', var_name="e0_h_feed_tr9_c2", shape=(1,1))  # noqa: E501
    e0_greek_alpha_tr0_c1 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr0_c1", shape=(1,1))  # noqa: E501
    e0_greek_alpha_tr0_c2 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr0_c2", shape=(1,1))  # noqa: E501
    e0_Q_C = model.set_variable(var_type='_z', var_name="e0_Q_C", shape=(1,1))  # noqa: E501
    e0_H_tr3 = model.set_variable(var_type='_z', var_name="e0_H_tr3", shape=(1,1))  # noqa: E501
    e0_H_tr4 = model.set_variable(var_type='_z', var_name="e0_H_tr4", shape=(1,1))  # noqa: E501
    e0_H_tr5 = model.set_variable(var_type='_z', var_name="e0_H_tr5", shape=(1,1))  # noqa: E501
    e0_H_tr6 = model.set_variable(var_type='_z', var_name="e0_H_tr6", shape=(1,1))  # noqa: E501
    e0_H_tr7 = model.set_variable(var_type='_z', var_name="e0_H_tr7", shape=(1,1))  # noqa: E501
    e0_H_tr8 = model.set_variable(var_type='_z', var_name="e0_H_tr8", shape=(1,1))  # noqa: E501
    e0_T_tr0 = model.set_variable(var_type='_z', var_name="e0_T_tr0", shape=(1,1))  # noqa: E501
    e0_HU_L_tr1 = model.set_variable(var_type='_z', var_name="e0_HU_L_tr1", shape=(1,1))  # noqa: E501
    e0_HU_L_tr2 = model.set_variable(var_type='_z', var_name="e0_HU_L_tr2", shape=(1,1))  # noqa: E501
    e0_HU_L_tr3 = model.set_variable(var_type='_z', var_name="e0_HU_L_tr3", shape=(1,1))  # noqa: E501
    e0_HU_L_tr4 = model.set_variable(var_type='_z', var_name="e0_HU_L_tr4", shape=(1,1))  # noqa: E501
    e0_HU_L_tr5 = model.set_variable(var_type='_z', var_name="e0_HU_L_tr5", shape=(1,1))  # noqa: E501
    e0_HU_L_tr6 = model.set_variable(var_type='_z', var_name="e0_HU_L_tr6", shape=(1,1))  # noqa: E501
    e0_HU_L_tr7 = model.set_variable(var_type='_z', var_name="e0_HU_L_tr7", shape=(1,1))  # noqa: E501
    e0_HU_L_tr8 = model.set_variable(var_type='_z', var_name="e0_HU_L_tr8", shape=(1,1))  # noqa: E501
    e0_HU_V_tr1 = model.set_variable(var_type='_z', var_name="e0_HU_V_tr1", shape=(1,1))  # noqa: E501
    e0_HU_V_tr2 = model.set_variable(var_type='_z', var_name="e0_HU_V_tr2", shape=(1,1))  # noqa: E501
    e0_HU_V_tr3 = model.set_variable(var_type='_z', var_name="e0_HU_V_tr3", shape=(1,1))  # noqa: E501
    e0_HU_V_tr4 = model.set_variable(var_type='_z', var_name="e0_HU_V_tr4", shape=(1,1))  # noqa: E501
    e0_HU_V_tr5 = model.set_variable(var_type='_z', var_name="e0_HU_V_tr5", shape=(1,1))  # noqa: E501
    e0_HU_V_tr6 = model.set_variable(var_type='_z', var_name="e0_HU_V_tr6", shape=(1,1))  # noqa: E501
    e0_HU_V_tr7 = model.set_variable(var_type='_z', var_name="e0_HU_V_tr7", shape=(1,1))  # noqa: E501
    e0_HU_V_tr8 = model.set_variable(var_type='_z', var_name="e0_HU_V_tr8", shape=(1,1))  # noqa: E501
    e0_K_tr1_c1 = model.set_variable(var_type='_z', var_name="e0_K_tr1_c1", shape=(1,1))  # noqa: E501
    e0_K_tr2_c1 = model.set_variable(var_type='_z', var_name="e0_K_tr2_c1", shape=(1,1))  # noqa: E501
    e0_h_L_tr0 = model.set_variable(var_type='_z', var_name="e0_h_L_tr0", shape=(1,1))  # noqa: E501
    e0_K_tr3_c1 = model.set_variable(var_type='_z', var_name="e0_K_tr3_c1", shape=(1,1))  # noqa: E501
    e0_K_tr4_c1 = model.set_variable(var_type='_z', var_name="e0_K_tr4_c1", shape=(1,1))  # noqa: E501
    e0_K_tr5_c1 = model.set_variable(var_type='_z', var_name="e0_K_tr5_c1", shape=(1,1))  # noqa: E501
    e0_K_tr6_c1 = model.set_variable(var_type='_z', var_name="e0_K_tr6_c1", shape=(1,1))  # noqa: E501
    e0_K_tr7_c1 = model.set_variable(var_type='_z', var_name="e0_K_tr7_c1", shape=(1,1))  # noqa: E501
    e0_K_tr8_c1 = model.set_variable(var_type='_z', var_name="e0_K_tr8_c1", shape=(1,1))  # noqa: E501
    e0_K_tr1_c2 = model.set_variable(var_type='_z', var_name="e0_K_tr1_c2", shape=(1,1))  # noqa: E501
    e0_K_tr2_c2 = model.set_variable(var_type='_z', var_name="e0_K_tr2_c2", shape=(1,1))  # noqa: E501
    e0_K_tr3_c2 = model.set_variable(var_type='_z', var_name="e0_K_tr3_c2", shape=(1,1))  # noqa: E501
    e0_K_tr4_c2 = model.set_variable(var_type='_z', var_name="e0_K_tr4_c2", shape=(1,1))  # noqa: E501
    e0_h_V_tr1 = model.set_variable(var_type='_z', var_name="e0_h_V_tr1", shape=(1,1))  # noqa: E501
    e0_K_tr5_c2 = model.set_variable(var_type='_z', var_name="e0_K_tr5_c2", shape=(1,1))  # noqa: E501
    e0_K_tr6_c2 = model.set_variable(var_type='_z', var_name="e0_K_tr6_c2", shape=(1,1))  # noqa: E501
    e0_K_tr7_c2 = model.set_variable(var_type='_z', var_name="e0_K_tr7_c2", shape=(1,1))  # noqa: E501
    e0_K_tr8_c2 = model.set_variable(var_type='_z', var_name="e0_K_tr8_c2", shape=(1,1))  # noqa: E501
    e0_L_tr1 = model.set_variable(var_type='_z', var_name="e0_L_tr1", shape=(1,1))  # noqa: E501
    e0_L_tr2 = model.set_variable(var_type='_z', var_name="e0_L_tr2", shape=(1,1))  # noqa: E501
    e0_L_tr3 = model.set_variable(var_type='_z', var_name="e0_L_tr3", shape=(1,1))  # noqa: E501
    e0_L_tr4 = model.set_variable(var_type='_z', var_name="e0_L_tr4", shape=(1,1))  # noqa: E501
    e0_L_tr5 = model.set_variable(var_type='_z', var_name="e0_L_tr5", shape=(1,1))  # noqa: E501
    e0_L_tr6 = model.set_variable(var_type='_z', var_name="e0_L_tr6", shape=(1,1))  # noqa: E501
    e0_L_tr7 = model.set_variable(var_type='_z', var_name="e0_L_tr7", shape=(1,1))  # noqa: E501
    e0_L_tr8 = model.set_variable(var_type='_z', var_name="e0_L_tr8", shape=(1,1))  # noqa: E501
    e0_L_weir = model.set_variable(var_type='_z', var_name="e0_L_weir", shape=(1,1))  # noqa: E501
    e0_T_tr1 = model.set_variable(var_type='_z', var_name="e0_T_tr1", shape=(1,1))  # noqa: E501
    e0_T_tr2 = model.set_variable(var_type='_z', var_name="e0_T_tr2", shape=(1,1))  # noqa: E501
    e0_T_tr3 = model.set_variable(var_type='_z', var_name="e0_T_tr3", shape=(1,1))  # noqa: E501
    e0_T_tr4 = model.set_variable(var_type='_z', var_name="e0_T_tr4", shape=(1,1))  # noqa: E501
    e0_T_tr5 = model.set_variable(var_type='_z', var_name="e0_T_tr5", shape=(1,1))  # noqa: E501
    e0_T_tr6 = model.set_variable(var_type='_z', var_name="e0_T_tr6", shape=(1,1))  # noqa: E501
    e0_T_tr7 = model.set_variable(var_type='_z', var_name="e0_T_tr7", shape=(1,1))  # noqa: E501
    e0_p_LV_o_tr0_c1 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr0_c1", shape=(1,1))  # noqa: E501
    e0_T_tr8 = model.set_variable(var_type='_z', var_name="e0_T_tr8", shape=(1,1))  # noqa: E501
    e0_V_L_tr1 = model.set_variable(var_type='_z', var_name="e0_V_L_tr1", shape=(1,1))  # noqa: E501
    e0_p_LV_o_tr0_c2 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr0_c2", shape=(1,1))  # noqa: E501
    e0_V_L_tr2 = model.set_variable(var_type='_z', var_name="e0_V_L_tr2", shape=(1,1))  # noqa: E501
    e0_V_L_tr3 = model.set_variable(var_type='_z', var_name="e0_V_L_tr3", shape=(1,1))  # noqa: E501
    e0_V_L_tr4 = model.set_variable(var_type='_z', var_name="e0_V_L_tr4", shape=(1,1))  # noqa: E501
    e0_V_L_tr5 = model.set_variable(var_type='_z', var_name="e0_V_L_tr5", shape=(1,1))  # noqa: E501
    e0_V_L_tr6 = model.set_variable(var_type='_z', var_name="e0_V_L_tr6", shape=(1,1))  # noqa: E501
    e0_V_L_tr7 = model.set_variable(var_type='_z', var_name="e0_V_L_tr7", shape=(1,1))  # noqa: E501
    e0_V_L_tr8 = model.set_variable(var_type='_z', var_name="e0_V_L_tr8", shape=(1,1))  # noqa: E501
    e0_V_V_tr1 = model.set_variable(var_type='_z', var_name="e0_V_V_tr1", shape=(1,1))  # noqa: E501
    e0_V_V_tr2 = model.set_variable(var_type='_z', var_name="e0_V_V_tr2", shape=(1,1))  # noqa: E501
    e0_V_V_tr3 = model.set_variable(var_type='_z', var_name="e0_V_V_tr3", shape=(1,1))  # noqa: E501
    e0_V_V_tr4 = model.set_variable(var_type='_z', var_name="e0_V_V_tr4", shape=(1,1))  # noqa: E501
    e0_V_V_tr5 = model.set_variable(var_type='_z', var_name="e0_V_V_tr5", shape=(1,1))  # noqa: E501
    e0_V_V_tr6 = model.set_variable(var_type='_z', var_name="e0_V_V_tr6", shape=(1,1))  # noqa: E501
    e0_V_V_tr7 = model.set_variable(var_type='_z', var_name="e0_V_V_tr7", shape=(1,1))  # noqa: E501
    e0_V_V_tr8 = model.set_variable(var_type='_z', var_name="e0_V_V_tr8", shape=(1,1))  # noqa: E501
    e0_V_tot = model.set_variable(var_type='_z', var_name="e0_V_tot", shape=(1,1))  # noqa: E501
    e0_greek_gamma_tr0_c1 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr0_c1", shape=(1,1))  # noqa: E501
    e0_x_L_tr0_c1 = model.set_variable(var_type='_z', var_name="e0_x_L_tr0_c1", shape=(1,1))  # noqa: E501
    e0_x_L_tr0_c2 = model.set_variable(var_type='_z', var_name="e0_x_L_tr0_c2", shape=(1,1))  # noqa: E501
    e0_h_L_tr1 = model.set_variable(var_type='_z', var_name="e0_h_L_tr1", shape=(1,1))  # noqa: E501
    e0_h_L_tr2 = model.set_variable(var_type='_z', var_name="e0_h_L_tr2", shape=(1,1))  # noqa: E501
    e0_h_L_tr3 = model.set_variable(var_type='_z', var_name="e0_h_L_tr3", shape=(1,1))  # noqa: E501
    e0_h_L_tr4 = model.set_variable(var_type='_z', var_name="e0_h_L_tr4", shape=(1,1))  # noqa: E501
    e0_h_L_tr5 = model.set_variable(var_type='_z', var_name="e0_h_L_tr5", shape=(1,1))  # noqa: E501
    e0_h_L_tr6 = model.set_variable(var_type='_z', var_name="e0_h_L_tr6", shape=(1,1))  # noqa: E501
    e0_h_L_tr7 = model.set_variable(var_type='_z', var_name="e0_h_L_tr7", shape=(1,1))  # noqa: E501
    e0_h_L_tr8 = model.set_variable(var_type='_z', var_name="e0_h_L_tr8", shape=(1,1))  # noqa: E501
    e0_x_V_tr0_c1 = model.set_variable(var_type='_z', var_name="e0_x_V_tr0_c1", shape=(1,1))  # noqa: E501
    e0_x_V_tr1_c1 = model.set_variable(var_type='_z', var_name="e0_x_V_tr1_c1", shape=(1,1))  # noqa: E501
    e0_h_V_tr2 = model.set_variable(var_type='_z', var_name="e0_h_V_tr2", shape=(1,1))  # noqa: E501
    e0_h_V_tr3 = model.set_variable(var_type='_z', var_name="e0_h_V_tr3", shape=(1,1))  # noqa: E501
    e0_h_V_tr4 = model.set_variable(var_type='_z', var_name="e0_h_V_tr4", shape=(1,1))  # noqa: E501
    e0_h_V_tr5 = model.set_variable(var_type='_z', var_name="e0_h_V_tr5", shape=(1,1))  # noqa: E501
    e0_x_V_tr0_c2 = model.set_variable(var_type='_z', var_name="e0_x_V_tr0_c2", shape=(1,1))  # noqa: E501
    e0_h_V_tr6 = model.set_variable(var_type='_z', var_name="e0_h_V_tr6", shape=(1,1))  # noqa: E501
    e0_h_V_tr7 = model.set_variable(var_type='_z', var_name="e0_h_V_tr7", shape=(1,1))  # noqa: E501
    e0_h_V_tr8 = model.set_variable(var_type='_z', var_name="e0_h_V_tr8", shape=(1,1))  # noqa: E501
    e0_h_V_tr9 = model.set_variable(var_type='_z', var_name="e0_h_V_tr9", shape=(1,1))  # noqa: E501
    e0_p_tr1 = model.set_variable(var_type='_z', var_name="e0_p_tr1", shape=(1,1))  # noqa: E501
    e0_p_tr2 = model.set_variable(var_type='_z', var_name="e0_p_tr2", shape=(1,1))  # noqa: E501
    e0_p_tr3 = model.set_variable(var_type='_z', var_name="e0_p_tr3", shape=(1,1))  # noqa: E501
    e0_p_tr4 = model.set_variable(var_type='_z', var_name="e0_p_tr4", shape=(1,1))  # noqa: E501
    e0_p_tr5 = model.set_variable(var_type='_z', var_name="e0_p_tr5", shape=(1,1))  # noqa: E501
    e0_p_tr6 = model.set_variable(var_type='_z', var_name="e0_p_tr6", shape=(1,1))  # noqa: E501
    e0_x_V_tr1_c2 = model.set_variable(var_type='_z', var_name="e0_x_V_tr1_c2", shape=(1,1))  # noqa: E501
    e0_p_tr7 = model.set_variable(var_type='_z', var_name="e0_p_tr7", shape=(1,1))  # noqa: E501
    e0_p_tr8 = model.set_variable(var_type='_z', var_name="e0_p_tr8", shape=(1,1))  # noqa: E501
    e0_p_LV_o_tr1_c1 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr1_c1", shape=(1,1))  # noqa: E501
    e0_p_LV_o_tr2_c1 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr2_c1", shape=(1,1))  # noqa: E501
    e0_p_LV_o_tr3_c1 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr3_c1", shape=(1,1))  # noqa: E501
    e0_p_LV_o_tr4_c1 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr4_c1", shape=(1,1))  # noqa: E501
    e0_p_LV_o_tr5_c1 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr5_c1", shape=(1,1))  # noqa: E501
    e0_p_LV_o_tr6_c1 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr6_c1", shape=(1,1))  # noqa: E501
    e0_p_LV_o_tr7_c1 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr7_c1", shape=(1,1))  # noqa: E501
    e0_p_LV_o_tr8_c1 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr8_c1", shape=(1,1))  # noqa: E501
    e0_p_LV_o_tr1_c2 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr1_c2", shape=(1,1))  # noqa: E501
    e0_p_LV_o_tr2_c2 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr2_c2", shape=(1,1))  # noqa: E501
    e0_p_LV_o_tr3_c2 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr3_c2", shape=(1,1))  # noqa: E501
    e0_p_LV_o_tr4_c2 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr4_c2", shape=(1,1))  # noqa: E501
    e0_p_LV_o_tr5_c2 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr5_c2", shape=(1,1))  # noqa: E501
    e0_p_LV_o_tr6_c2 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr6_c2", shape=(1,1))  # noqa: E501
    e0_p_LV_o_tr7_c2 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr7_c2", shape=(1,1))  # noqa: E501
    e0_p_LV_o_tr8_c2 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr8_c2", shape=(1,1))  # noqa: E501
    e0_v_L_tr1 = model.set_variable(var_type='_z', var_name="e0_v_L_tr1", shape=(1,1))  # noqa: E501
    e0_v_L_tr2 = model.set_variable(var_type='_z', var_name="e0_v_L_tr2", shape=(1,1))  # noqa: E501
    e0_v_L_tr3 = model.set_variable(var_type='_z', var_name="e0_v_L_tr3", shape=(1,1))  # noqa: E501
    e0_v_L_tr4 = model.set_variable(var_type='_z', var_name="e0_v_L_tr4", shape=(1,1))  # noqa: E501
    e0_v_L_tr5 = model.set_variable(var_type='_z', var_name="e0_v_L_tr5", shape=(1,1))  # noqa: E501
    e0_v_L_tr6 = model.set_variable(var_type='_z', var_name="e0_v_L_tr6", shape=(1,1))  # noqa: E501
    e0_v_L_tr7 = model.set_variable(var_type='_z', var_name="e0_v_L_tr7", shape=(1,1))  # noqa: E501
    e0_v_L_tr8 = model.set_variable(var_type='_z', var_name="e0_v_L_tr8", shape=(1,1))  # noqa: E501
    e0_x_L_tr1_c1 = model.set_variable(var_type='_z', var_name="e0_x_L_tr1_c1", shape=(1,1))  # noqa: E501
    e0_x_L_tr2_c1 = model.set_variable(var_type='_z', var_name="e0_x_L_tr2_c1", shape=(1,1))  # noqa: E501
    e0_x_L_tr3_c1 = model.set_variable(var_type='_z', var_name="e0_x_L_tr3_c1", shape=(1,1))  # noqa: E501
    e0_x_L_tr4_c1 = model.set_variable(var_type='_z', var_name="e0_x_L_tr4_c1", shape=(1,1))  # noqa: E501
    e0_x_L_tr5_c1 = model.set_variable(var_type='_z', var_name="e0_x_L_tr5_c1", shape=(1,1))  # noqa: E501
    e0_x_L_tr6_c1 = model.set_variable(var_type='_z', var_name="e0_x_L_tr6_c1", shape=(1,1))  # noqa: E501
    e0_x_L_tr7_c1 = model.set_variable(var_type='_z', var_name="e0_x_L_tr7_c1", shape=(1,1))  # noqa: E501
    e0_x_L_tr8_c1 = model.set_variable(var_type='_z', var_name="e0_x_L_tr8_c1", shape=(1,1))  # noqa: E501
    e0_x_L_tr1_c2 = model.set_variable(var_type='_z', var_name="e0_x_L_tr1_c2", shape=(1,1))  # noqa: E501
    e0_x_L_tr2_c2 = model.set_variable(var_type='_z', var_name="e0_x_L_tr2_c2", shape=(1,1))  # noqa: E501
    e0_x_L_tr3_c2 = model.set_variable(var_type='_z', var_name="e0_x_L_tr3_c2", shape=(1,1))  # noqa: E501
    e0_x_L_tr4_c2 = model.set_variable(var_type='_z', var_name="e0_x_L_tr4_c2", shape=(1,1))  # noqa: E501
    e0_x_L_tr5_c2 = model.set_variable(var_type='_z', var_name="e0_x_L_tr5_c2", shape=(1,1))  # noqa: E501
    e0_x_L_tr6_c2 = model.set_variable(var_type='_z', var_name="e0_x_L_tr6_c2", shape=(1,1))  # noqa: E501
    e0_x_L_tr7_c2 = model.set_variable(var_type='_z', var_name="e0_x_L_tr7_c2", shape=(1,1))  # noqa: E501
    e0_x_L_tr8_c2 = model.set_variable(var_type='_z', var_name="e0_x_L_tr8_c2", shape=(1,1))  # noqa: E501
    e0_x_V_tr2_c1 = model.set_variable(var_type='_z', var_name="e0_x_V_tr2_c1", shape=(1,1))  # noqa: E501
    e0_x_V_tr3_c1 = model.set_variable(var_type='_z', var_name="e0_x_V_tr3_c1", shape=(1,1))  # noqa: E501
    e0_x_V_tr4_c1 = model.set_variable(var_type='_z', var_name="e0_x_V_tr4_c1", shape=(1,1))  # noqa: E501
    e0_x_V_tr5_c1 = model.set_variable(var_type='_z', var_name="e0_x_V_tr5_c1", shape=(1,1))  # noqa: E501
    e0_x_V_tr6_c1 = model.set_variable(var_type='_z', var_name="e0_x_V_tr6_c1", shape=(1,1))  # noqa: E501
    e0_x_V_tr7_c1 = model.set_variable(var_type='_z', var_name="e0_x_V_tr7_c1", shape=(1,1))  # noqa: E501
    e0_x_V_tr8_c1 = model.set_variable(var_type='_z', var_name="e0_x_V_tr8_c1", shape=(1,1))  # noqa: E501
    e0_greek_gamma_tr0_c2 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr0_c2", shape=(1,1))  # noqa: E501
    e0_x_V_tr9_c1 = model.set_variable(var_type='_z', var_name="e0_x_V_tr9_c1", shape=(1,1))  # noqa: E501
    e0_x_V_tr2_c2 = model.set_variable(var_type='_z', var_name="e0_x_V_tr2_c2", shape=(1,1))  # noqa: E501
    e0_x_V_tr3_c2 = model.set_variable(var_type='_z', var_name="e0_x_V_tr3_c2", shape=(1,1))  # noqa: E501
    e0_x_V_tr4_c2 = model.set_variable(var_type='_z', var_name="e0_x_V_tr4_c2", shape=(1,1))  # noqa: E501
    e0_x_V_tr5_c2 = model.set_variable(var_type='_z', var_name="e0_x_V_tr5_c2", shape=(1,1))  # noqa: E501
    e0_x_V_tr6_c2 = model.set_variable(var_type='_z', var_name="e0_x_V_tr6_c2", shape=(1,1))  # noqa: E501
    e0_x_V_tr7_c2 = model.set_variable(var_type='_z', var_name="e0_x_V_tr7_c2", shape=(1,1))  # noqa: E501
    e0_x_V_tr8_c2 = model.set_variable(var_type='_z', var_name="e0_x_V_tr8_c2", shape=(1,1))  # noqa: E501
    e0_x_V_tr9_c2 = model.set_variable(var_type='_z', var_name="e0_x_V_tr9_c2", shape=(1,1))  # noqa: E501
    e0_greek_alpha_tr9_c1 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr9_c1", shape=(1,1))  # noqa: E501
    e0_greek_alpha_tr9_c2 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr9_c2", shape=(1,1))  # noqa: E501
    e0_greek_gamma_tr9_c1 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr9_c1", shape=(1,1))  # noqa: E501
    e0_greek_gamma_tr9_c2 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr9_c2", shape=(1,1))  # noqa: E501
    e0_H_tr9 = model.set_variable(var_type='_z', var_name="e0_H_tr9", shape=(1,1))  # noqa: E501
    e0_HU_L_tr9 = model.set_variable(var_type='_z', var_name="e0_HU_L_tr9", shape=(1,1))  # noqa: E501
    e0_HU_V_tr9 = model.set_variable(var_type='_z', var_name="e0_HU_V_tr9", shape=(1,1))  # noqa: E501
    e0_K_tr9_c1 = model.set_variable(var_type='_z', var_name="e0_K_tr9_c1", shape=(1,1))  # noqa: E501
    e0_K_tr9_c2 = model.set_variable(var_type='_z', var_name="e0_K_tr9_c2", shape=(1,1))  # noqa: E501
    e0_T_tr9 = model.set_variable(var_type='_z', var_name="e0_T_tr9", shape=(1,1))  # noqa: E501
    e0_V_L_tr9 = model.set_variable(var_type='_z', var_name="e0_V_L_tr9", shape=(1,1))  # noqa: E501
    e0_V_V_tr9 = model.set_variable(var_type='_z', var_name="e0_V_V_tr9", shape=(1,1))  # noqa: E501
    e0_h_L_tr9 = model.set_variable(var_type='_z', var_name="e0_h_L_tr9", shape=(1,1))  # noqa: E501
    e0_h_feed_tr9 = model.set_variable(var_type='_z', var_name="e0_h_feed_tr9", shape=(1,1))  # noqa: E501
    e0_p_tr9 = model.set_variable(var_type='_z', var_name="e0_p_tr9", shape=(1,1))  # noqa: E501
    e0_p_LV_o_tr9_c1 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr9_c1", shape=(1,1))  # noqa: E501
    e0_p_LV_o_tr9_c2 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr9_c2", shape=(1,1))  # noqa: E501
    e0_v_L_tr9 = model.set_variable(var_type='_z', var_name="e0_v_L_tr9", shape=(1,1))  # noqa: E501
    e0_x_L_tr9_c1 = model.set_variable(var_type='_z', var_name="e0_x_L_tr9_c1", shape=(1,1))  # noqa: E501
    e0_x_L_tr9_c2 = model.set_variable(var_type='_z', var_name="e0_x_L_tr9_c2", shape=(1,1))  # noqa: E501
    e0_LI = model.set_variable(var_type='_z', var_name="e0_LI", shape=(1,1))  # noqa: E501
    e0_M_D = model.set_variable(var_type='_z', var_name="e0_M_D", shape=(1,1))  # noqa: E501
    e0_M_D_c1 = model.set_variable(var_type='_z', var_name="e0_M_D_c1", shape=(1,1))  # noqa: E501
    e0_M_D_c2 = model.set_variable(var_type='_z', var_name="e0_M_D_c2", shape=(1,1))  # noqa: E501
    e0_PDI = model.set_variable(var_type='_z', var_name="e0_PDI", shape=(1,1))  # noqa: E501
    e0_PI_B = model.set_variable(var_type='_z', var_name="e0_PI_B", shape=(1,1))  # noqa: E501
    e0_PI_C = model.set_variable(var_type='_z', var_name="e0_PI_C", shape=(1,1))  # noqa: E501
    e0_WI = model.set_variable(var_type='_z', var_name="e0_WI", shape=(1,1))  # noqa: E501
    e0_w_L_B_c1 = model.set_variable(var_type='_z', var_name="e0_w_L_B_c1", shape=(1,1))  # noqa: E501
    e0_w_L_B_c2 = model.set_variable(var_type='_z', var_name="e0_w_L_B_c2", shape=(1,1))  # noqa: E501
    e0_w_L_C_c1 = model.set_variable(var_type='_z', var_name="e0_w_L_C_c1", shape=(1,1))  # noqa: E501
    e0_w_L_C_c2 = model.set_variable(var_type='_z', var_name="e0_w_L_C_c2", shape=(1,1))  # noqa: E501
    e0_w_L_D_c1 = model.set_variable(var_type='_z', var_name="e0_w_L_D_c1", shape=(1,1))  # noqa: E501
    e0_w_L_D_c2 = model.set_variable(var_type='_z', var_name="e0_w_L_D_c2", shape=(1,1))  # noqa: E501
    # e0_Q_PLS_R = model.set_variable(var_type='_z', var_name="e0_Q_PLS_R", shape=(1,1))  # noqa: E501
    # e0_rr_PLS = model.set_variable(var_type='_z', var_name="e0_rr_PLS", shape=(1,1))  # noqa: E501
    e0_greek_alpha_tr1_c1 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr1_c1", shape=(1,1))  # noqa: E501
    e0_greek_alpha_tr2_c1 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr2_c1", shape=(1,1))  # noqa: E501
    e0_F_L_tr0 = model.set_variable(var_type='_z', var_name="e0_F_L_tr0", shape=(1,1))  # noqa: E501
    e0_greek_alpha_tr3_c1 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr3_c1", shape=(1,1))  # noqa: E501
    e0_greek_alpha_tr4_c1 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr4_c1", shape=(1,1))  # noqa: E501
    e0_greek_alpha_tr5_c1 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr5_c1", shape=(1,1))  # noqa: E501
    e0_greek_alpha_tr6_c1 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr6_c1", shape=(1,1))  # noqa: E501
    e0_greek_alpha_tr7_c1 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr7_c1", shape=(1,1))  # noqa: E501
    e0_greek_alpha_tr8_c1 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr8_c1", shape=(1,1))  # noqa: E501
    e0_greek_alpha_tr1_c2 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr1_c2", shape=(1,1))  # noqa: E501
    e0_greek_alpha_tr2_c2 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr2_c2", shape=(1,1))  # noqa: E501
    e0_greek_alpha_tr3_c2 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr3_c2", shape=(1,1))  # noqa: E501
    e0_greek_alpha_tr4_c2 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr4_c2", shape=(1,1))  # noqa: E501
    e0_F_V_tr1 = model.set_variable(var_type='_z', var_name="e0_F_V_tr1", shape=(1,1))  # noqa: E501
    e0_greek_alpha_tr5_c2 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr5_c2", shape=(1,1))  # noqa: E501
    e0_greek_alpha_tr6_c2 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr6_c2", shape=(1,1))  # noqa: E501
    e0_greek_alpha_tr7_c2 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr7_c2", shape=(1,1))  # noqa: E501
    e0_greek_alpha_tr8_c2 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr8_c2", shape=(1,1))  # noqa: E501
    e0_greek_gamma_tr1_c1 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr1_c1", shape=(1,1))  # noqa: E501
    e0_greek_gamma_tr2_c1 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr2_c1", shape=(1,1))  # noqa: E501
    e0_greek_gamma_tr3_c1 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr3_c1", shape=(1,1))  # noqa: E501
    e0_greek_gamma_tr4_c1 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr4_c1", shape=(1,1))  # noqa: E501
    e0_greek_gamma_tr5_c1 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr5_c1", shape=(1,1))  # noqa: E501
    e0_greek_gamma_tr6_c1 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr6_c1", shape=(1,1))  # noqa: E501
    e0_F_D = model.set_variable(var_type='_z', var_name="e0_F_D", shape=(1,1))  # noqa: E501
    e0_greek_gamma_tr7_c1 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr7_c1", shape=(1,1))  # noqa: E501
    e0_greek_gamma_tr8_c1 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr8_c1", shape=(1,1))  # noqa: E501
    e0_greek_gamma_tr1_c2 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr1_c2", shape=(1,1))  # noqa: E501
    e0_greek_gamma_tr2_c2 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr2_c2", shape=(1,1))  # noqa: E501
    e0_greek_gamma_tr3_c2 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr3_c2", shape=(1,1))  # noqa: E501
    e0_greek_gamma_tr4_c2 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr4_c2", shape=(1,1))  # noqa: E501
    e0_greek_gamma_tr5_c2 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr5_c2", shape=(1,1))  # noqa: E501
    e0_greek_gamma_tr6_c2 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr6_c2", shape=(1,1))  # noqa: E501
    e0_greek_gamma_tr7_c2 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr7_c2", shape=(1,1))  # noqa: E501
    e0_greek_gamma_tr8_c2 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr8_c2", shape=(1,1))  # noqa: E501
    e0_K_tr0_c1 = model.set_variable(var_type='_z', var_name="e0_K_tr0_c1", shape=(1,1))  # noqa: E501
    e0_A_col = model.set_variable(var_type='_z', var_name="e0_A_col", shape=(1,1))  # noqa: E501
    e0_A_active = model.set_variable(var_type='_z', var_name="e0_A_active", shape=(1,1))  # noqa: E501
    e0_F_L_tr1 = model.set_variable(var_type='_z', var_name="e0_F_L_tr1", shape=(1,1))  # noqa: E501
    e0_F_L_tr2 = model.set_variable(var_type='_z', var_name="e0_F_L_tr2", shape=(1,1))  # noqa: E501
    e0_F_L_tr3 = model.set_variable(var_type='_z', var_name="e0_F_L_tr3", shape=(1,1))  # noqa: E501
    e0_F_L_tr4 = model.set_variable(var_type='_z', var_name="e0_F_L_tr4", shape=(1,1))  # noqa: E501
    e0_F_L_tr5 = model.set_variable(var_type='_z', var_name="e0_F_L_tr5", shape=(1,1))  # noqa: E501
    e0_F_L_tr6 = model.set_variable(var_type='_z', var_name="e0_F_L_tr6", shape=(1,1))  # noqa: E501
    e0_F_L_tr7 = model.set_variable(var_type='_z', var_name="e0_F_L_tr7", shape=(1,1))  # noqa: E501
    e0_F_L_tr8 = model.set_variable(var_type='_z', var_name="e0_F_L_tr8", shape=(1,1))  # noqa: E501
    e0_K_tr0_c2 = model.set_variable(var_type='_z', var_name="e0_K_tr0_c2", shape=(1,1))  # noqa: E501
    e0_F_V_tr2 = model.set_variable(var_type='_z', var_name="e0_F_V_tr2", shape=(1,1))  # noqa: E501
    e0_F_V_tr3 = model.set_variable(var_type='_z', var_name="e0_F_V_tr3", shape=(1,1))  # noqa: E501
    e0_F_V_tr4 = model.set_variable(var_type='_z', var_name="e0_F_V_tr4", shape=(1,1))  # noqa: E501
    e0_F_V_tr5 = model.set_variable(var_type='_z', var_name="e0_F_V_tr5", shape=(1,1))  # noqa: E501
    e0_F_V_tr6 = model.set_variable(var_type='_z', var_name="e0_F_V_tr6", shape=(1,1))  # noqa: E501
    e0_F_V_tr7 = model.set_variable(var_type='_z', var_name="e0_F_V_tr7", shape=(1,1))  # noqa: E501
    e0_F_V_tr8 = model.set_variable(var_type='_z', var_name="e0_F_V_tr8", shape=(1,1))  # noqa: E501
    e0_F_V_tr9 = model.set_variable(var_type='_z', var_name="e0_F_V_tr9", shape=(1,1))  # noqa: E501
    e0_H_tr1 = model.set_variable(var_type='_z', var_name="e0_H_tr1", shape=(1,1))  # noqa: E501
    e0_H_tr2 = model.set_variable(var_type='_z', var_name="e0_H_tr2", shape=(1,1))  # noqa: E501

    # Control inputs
    e0_rr = model.set_variable(var_type='_z', var_name="e0_rr")  # noqa: E501
    e0_rr_PLS = model.set_variable(var_type='_u', var_name="e0_rr_PLS", shape=(1,1))  # noqa: E501
    e0_Q_R = model.set_variable(var_type='_z', var_name="e0_Q_R")  # noqa: E501
    e0_Q_PLS_R = model.set_variable(var_type='_u', var_name="e0_Q_PLS_R", shape=(1,1))  # noqa: E501

    # Additional control inputs (were "_p" in template_model_for_pe, now "_u"
    # so they can be driven by an externally supplied trajectory).
    e0_F_feed_tr9 = model.set_variable(var_type='_u', var_name="e0_F_feed_tr9", shape=(1,1))  # noqa: E501
    e0_F_B = model.set_variable(var_type='_u', var_name="e0_F_B", shape=(1,1))  # noqa: E501
    e0_x_feed_tr9_c1 = model.set_variable(var_type='_u', var_name="e0_x_feed_tr9_c1", shape=(1,1))  # noqa: E501
    e0_x_feed_tr9_c2 = model.set_variable(var_type='_u', var_name="e0_x_feed_tr9_c2", shape=(1,1))  # noqa: E501
    e0_rr_err = model.set_variable(var_type='_u', var_name="e0_rr_err", shape=(1,1))  # noqa: E501
    e0_E_murphree = model.set_variable(var_type='_u', var_name="e0_E_murphree", shape=(1,1))  # noqa: E501
    e0_x_N2 = model.set_variable(var_type='_u', var_name="e0_x_N2", shape=(1,1))  # noqa: E501

    # Remaining parameters (kept as "_p").
    e0_p_tr0 = model.set_variable(var_type='_p', var_name="e0_p_tr0")  # noqa: E501
    e0_T_feed = model.set_variable(var_type='_p', var_name="e0_T_feed")  # noqa: E501
    e0_V_tot_tr9 = model.set_variable(var_type='_p', var_name="e0_V_tot_tr9")  # noqa: E501
    e0_greek_lambda_activity = model.set_variable(var_type='_p', var_name="e0_greek_lambda_activity")  # noqa: E501

    e0_greek_kappa = model.set_variable(var_type='_u', var_name="e0_greek_kappa", shape=(1,1))  # noqa: E501
    e0_greek_kappa_hyst = model.set_variable(var_type='_p', var_name="e0_greek_kappa_hyst")  # noqa: E501
    e0_h_tot = model.set_variable(var_type='_u', var_name="e0_h_tot", shape=(1,1))  # noqa: E501
    e0_h_weir = model.set_variable(var_type='_u', var_name="e0_h_weir", shape=(1,1))  # noqa: E501

    # Uncertain parameters
    # e0_Q_err_R = 0.98647356893109
    e0_Q_err_R = model.set_variable(var_type='_p', var_name="e0_Q_err_R")  # noqa: E501

    # Measurements
    e0_LI_meas = model.set_meas(meas_name = "LI_meas", expr = e0_LI, meas_noise = meas_noise_bool)
    e0_WI_meas = model.set_meas(meas_name = "WI_meas", expr = e0_WI, meas_noise = meas_noise_bool)
    e0_w_L_D_c1_meas = model.set_meas(meas_name = "w_L_D_c1_meas", expr = e0_w_L_D_c1, meas_noise = meas_noise_bool)
    e0_w_L_B_c1_meas = model.set_meas(meas_name = "w_L_B_c1_meas", expr = e0_w_L_B_c1, meas_noise = meas_noise_bool)
    e0_T_tr9_meas = model.set_meas(meas_name = "T_tr9_meas", expr = e0_T_tr9, meas_noise = meas_noise_bool)

    e0_Q_PLS_R_meas = model.set_meas(meas_name = "e0_Q_PLS_R", expr = e0_Q_PLS_R, meas_noise = False)
    e0_rr_PLS_meas = model.set_meas(meas_name = "e0_rr_PLS", expr = e0_rr_PLS, meas_noise = False)


    # Differential equations
    EQ_diff1 = ((((e0_F_L_tr0*e0_x_L_tr0_c1)-(e0_F_L_tr1*e0_x_L_tr1_c1))+(e0_F_V_tr2*e0_x_V_tr2_c1))-(e0_F_V_tr1*e0_x_V_tr1_c1))  # noqa: E501,E226
    EQ_diff2 = ((((e0_F_L_tr1*e0_x_L_tr1_c1)-(e0_F_L_tr2*e0_x_L_tr2_c1))+(e0_F_V_tr3*e0_x_V_tr3_c1))-(e0_F_V_tr2*e0_x_V_tr2_c1))  # noqa: E501,E226
    EQ_diff3 = ((((e0_F_L_tr2*e0_x_L_tr2_c1)-(e0_F_L_tr3*e0_x_L_tr3_c1))+(e0_F_V_tr4*e0_x_V_tr4_c1))-(e0_F_V_tr3*e0_x_V_tr3_c1))  # noqa: E501,E226
    EQ_diff4 = ((((e0_F_L_tr3*e0_x_L_tr3_c1)-(e0_F_L_tr4*e0_x_L_tr4_c1))+(e0_F_V_tr5*e0_x_V_tr5_c1))-(e0_F_V_tr4*e0_x_V_tr4_c1))  # noqa: E501,E226
    EQ_diff5 = ((((e0_F_L_tr4*e0_x_L_tr4_c1)-(e0_F_L_tr5*e0_x_L_tr5_c1))+(e0_F_V_tr6*e0_x_V_tr6_c1))-(e0_F_V_tr5*e0_x_V_tr5_c1))  # noqa: E501,E226
    EQ_diff6 = ((((e0_F_L_tr5*e0_x_L_tr5_c1)-(e0_F_L_tr6*e0_x_L_tr6_c1))+(e0_F_V_tr7*e0_x_V_tr7_c1))-(e0_F_V_tr6*e0_x_V_tr6_c1))  # noqa: E501,E226
    EQ_diff7 = ((((e0_F_L_tr6*e0_x_L_tr6_c1)-(e0_F_L_tr7*e0_x_L_tr7_c1))+(e0_F_V_tr8*e0_x_V_tr8_c1))-(e0_F_V_tr7*e0_x_V_tr7_c1))  # noqa: E501,E226
    EQ_diff8 = ((((e0_F_L_tr7*e0_x_L_tr7_c1)-(e0_F_L_tr8*e0_x_L_tr8_c1))+(e0_F_V_tr9*e0_x_V_tr9_c1))-(e0_F_V_tr8*e0_x_V_tr8_c1))  # noqa: E501,E226
    EQ_diff9 = ((((e0_F_L_tr0*e0_x_L_tr0_c2)-(e0_F_L_tr1*e0_x_L_tr1_c2))+(e0_F_V_tr2*e0_x_V_tr2_c2))-(e0_F_V_tr1*e0_x_V_tr1_c2))  # noqa: E501,E226
    EQ_diff10 = ((((e0_F_L_tr1*e0_x_L_tr1_c2)-(e0_F_L_tr2*e0_x_L_tr2_c2))+(e0_F_V_tr3*e0_x_V_tr3_c2))-(e0_F_V_tr2*e0_x_V_tr2_c2))  # noqa: E501,E226
    EQ_diff11 = ((((e0_F_L_tr2*e0_x_L_tr2_c2)-(e0_F_L_tr3*e0_x_L_tr3_c2))+(e0_F_V_tr4*e0_x_V_tr4_c2))-(e0_F_V_tr3*e0_x_V_tr3_c2))  # noqa: E501,E226
    EQ_diff12 = ((((e0_F_L_tr3*e0_x_L_tr3_c2)-(e0_F_L_tr4*e0_x_L_tr4_c2))+(e0_F_V_tr5*e0_x_V_tr5_c2))-(e0_F_V_tr4*e0_x_V_tr4_c2))  # noqa: E501,E226
    EQ_diff13 = ((((e0_F_L_tr4*e0_x_L_tr4_c2)-(e0_F_L_tr5*e0_x_L_tr5_c2))+(e0_F_V_tr6*e0_x_V_tr6_c2))-(e0_F_V_tr5*e0_x_V_tr5_c2))  # noqa: E501,E226
    EQ_diff14 = ((((e0_F_L_tr5*e0_x_L_tr5_c2)-(e0_F_L_tr6*e0_x_L_tr6_c2))+(e0_F_V_tr7*e0_x_V_tr7_c2))-(e0_F_V_tr6*e0_x_V_tr6_c2))  # noqa: E501,E226
    EQ_diff15 = ((((e0_F_L_tr6*e0_x_L_tr6_c2)-(e0_F_L_tr7*e0_x_L_tr7_c2))+(e0_F_V_tr8*e0_x_V_tr8_c2))-(e0_F_V_tr7*e0_x_V_tr7_c2))  # noqa: E501,E226
    EQ_diff16 = ((((e0_F_L_tr7*e0_x_L_tr7_c2)-(e0_F_L_tr8*e0_x_L_tr8_c2))+(e0_F_V_tr9*e0_x_V_tr9_c2))-(e0_F_V_tr8*e0_x_V_tr8_c2))  # noqa: E501,E226
    EQ_diff17 = ((((e0_F_L_tr0*e0_h_L_tr0)-(e0_F_L_tr1*e0_h_L_tr1))+(e0_F_V_tr2*e0_h_V_tr2))-(e0_F_V_tr1*e0_h_V_tr1))  # noqa: E501,E226
    EQ_diff18 = ((((e0_F_L_tr1*e0_h_L_tr1)-(e0_F_L_tr2*e0_h_L_tr2))+(e0_F_V_tr3*e0_h_V_tr3))-(e0_F_V_tr2*e0_h_V_tr2))  # noqa: E501,E226
    EQ_diff19 = ((((e0_F_L_tr2*e0_h_L_tr2)-(e0_F_L_tr3*e0_h_L_tr3))+(e0_F_V_tr4*e0_h_V_tr4))-(e0_F_V_tr3*e0_h_V_tr3))  # noqa: E501,E226
    EQ_diff20 = ((((e0_F_L_tr3*e0_h_L_tr3)-(e0_F_L_tr4*e0_h_L_tr4))+(e0_F_V_tr5*e0_h_V_tr5))-(e0_F_V_tr4*e0_h_V_tr4))  # noqa: E501,E226
    EQ_diff21 = ((((e0_F_L_tr4*e0_h_L_tr4)-(e0_F_L_tr5*e0_h_L_tr5))+(e0_F_V_tr6*e0_h_V_tr6))-(e0_F_V_tr5*e0_h_V_tr5))  # noqa: E501,E226
    EQ_diff22 = ((((e0_F_L_tr5*e0_h_L_tr5)-(e0_F_L_tr6*e0_h_L_tr6))+(e0_F_V_tr7*e0_h_V_tr7))-(e0_F_V_tr6*e0_h_V_tr6))  # noqa: E501,E226
    EQ_diff23 = ((((e0_F_L_tr6*e0_h_L_tr6)-(e0_F_L_tr7*e0_h_L_tr7))+(e0_F_V_tr8*e0_h_V_tr8))-(e0_F_V_tr7*e0_h_V_tr7))  # noqa: E501,E226
    EQ_diff24 = ((((e0_F_L_tr7*e0_h_L_tr7)-(e0_F_L_tr8*e0_h_L_tr8))+(e0_F_V_tr9*e0_h_V_tr9))-(e0_F_V_tr8*e0_h_V_tr8))  # noqa: E501,E226
    EQ_diff25 = ((((e0_F_feed_tr9*e0_x_feed_tr9_c1)+(e0_F_L_tr8*e0_x_L_tr8_c1))-(e0_F_V_tr9*e0_x_V_tr9_c1))-(e0_F_B*e0_x_L_tr9_c1))  # noqa: E501,E226
    EQ_diff26 = ((((e0_F_feed_tr9*e0_x_feed_tr9_c2)+(e0_F_L_tr8*e0_x_L_tr8_c2))-(e0_F_V_tr9*e0_x_V_tr9_c2))-(e0_F_B*e0_x_L_tr9_c2))  # noqa: E501,E226
    EQ_diff27 = (((((e0_F_feed_tr9*e0_h_feed_tr9)+(e0_F_L_tr8*e0_h_L_tr8))-(e0_F_B*e0_h_L_tr9))-(e0_F_V_tr9*e0_h_V_tr9))+e0_Q_R)  # noqa: E501,E226
    EQ_diff28 = (e0_F_D*e0_x_L_tr0_c1)  # noqa: E501,E226
    EQ_diff29 = (e0_F_D*e0_x_L_tr0_c2)  # noqa: E501,E226

    EQ_alg30 = ((e0_F_V_tr1*e0_x_V_tr1_c1)-((((e0_F_L_tr0+e0_F_D))*e0_x_L_tr0_c1)))  # noqa: E501,E226
    EQ_alg31 = ((e0_F_V_tr1*e0_x_V_tr1_c2)-((((e0_F_L_tr0+e0_F_D))*e0_x_L_tr0_c2)))  # noqa: E501,E226
    EQ_alg32 = (0.0-((e0_Q_C+(e0_F_V_tr1*((e0_h_V_tr1-e0_h_L_tr0))))))  # noqa: E501,E226
    EQ_alg33 = (e0_h_L_tr0-((((e0_x_L_tr0_c1*e0_h_L_tr0_c1)+(e0_x_L_tr0_c2*e0_h_L_tr0_c2)))))  # noqa: E501,E226
    EQ_alg34 = ((e0_rr*((e0_F_L_tr0+e0_F_D)))-(e0_F_L_tr0))  # noqa: E501,E226
    EQ_alg35 = (0.0-((e0_x_V_tr0_c1-(e0_K_tr0_c1*e0_x_L_tr0_c1))))  # noqa: E501,E226
    EQ_alg36 = (0.0-((e0_x_V_tr0_c2-(e0_K_tr0_c2*e0_x_L_tr0_c2))))  # noqa: E501,E226
    EQ_alg37 = (1.0-(((e0_x_L_tr0_c1+e0_x_L_tr0_c2))))  # noqa: E501,E226
    EQ_alg38 = ((1.0-e0_x_N2)-(((e0_x_V_tr0_c1+e0_x_V_tr0_c2))))  # noqa: E501,E226
    EQ_alg39 = (0.0-((e0_p_LV_o_tr0_c1-((10.0))**(1.0*(e0_A_c1-(e0_B_c1/(e0_T_tr0+e0_C_c1)))))))  # noqa: E501,E226
    EQ_alg40 = (0.0-((e0_p_LV_o_tr0_c2-((10.0))**(1.0*(e0_A_c2-(e0_B_c2/(e0_T_tr0+e0_C_c2)))))))  # noqa: E501,E226
    EQ_alg41 = ((e0_p_tr0*e0_K_tr0_c1)-((e0_p_LV_o_tr0_c1*(((e0_greek_lambda_activity*e0_greek_gamma_tr0_c1)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
    EQ_alg42 = ((e0_p_tr0*e0_K_tr0_c2)-((e0_p_LV_o_tr0_c2*(((e0_greek_lambda_activity*e0_greek_gamma_tr0_c2)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
    EQ_alg43 = (e0_greek_alpha_tr0_c1-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c1)/e0_v_L_c1)*ca.exp(((-e0_greek_lambda_c1)/e0_T_tr0)))))  # noqa: E501,E226
    EQ_alg44 = (e0_greek_alpha_tr0_c2-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c2)/e0_v_L_c2)*ca.exp(((-e0_greek_lambda_c2)/e0_T_tr0)))))  # noqa: E501,E226
    EQ_alg45 = (e0_greek_gamma_tr0_c1-(((1.0/(e0_x_L_tr0_c1+(e0_greek_alpha_tr0_c1*((1.0-e0_x_L_tr0_c1)))))*ca.exp((((1.0-e0_x_L_tr0_c1))*(((e0_greek_alpha_tr0_c1/(e0_x_L_tr0_c1+(e0_greek_alpha_tr0_c1*((1.0-e0_x_L_tr0_c1)))))-((((e0_greek_alpha_tr0_c1+e0_greek_alpha_tr0_c2))-e0_greek_alpha_tr0_c1)/((((((e0_greek_alpha_tr0_c1+e0_greek_alpha_tr0_c2))-e0_greek_alpha_tr0_c1))*e0_x_L_tr0_c1)+((1.0-e0_x_L_tr0_c1)))))))))))  # noqa: E501,E226
    EQ_alg46 = (e0_greek_gamma_tr0_c2-(((1.0/(e0_x_L_tr0_c2+(e0_greek_alpha_tr0_c2*((1.0-e0_x_L_tr0_c2)))))*ca.exp((((1.0-e0_x_L_tr0_c2))*(((e0_greek_alpha_tr0_c2/(e0_x_L_tr0_c2+(e0_greek_alpha_tr0_c2*((1.0-e0_x_L_tr0_c2)))))-((((e0_greek_alpha_tr0_c1+e0_greek_alpha_tr0_c2))-e0_greek_alpha_tr0_c2)/((((((e0_greek_alpha_tr0_c1+e0_greek_alpha_tr0_c2))-e0_greek_alpha_tr0_c2))*e0_x_L_tr0_c2)+((1.0-e0_x_L_tr0_c2)))))))))))  # noqa: E501,E226
    EQ_alg47 = (0.0-((1.0-((e0_x_L_tr1_c1+e0_x_L_tr1_c2)))))  # noqa: E501,E226
    EQ_alg48 = (0.0-((1.0-((e0_x_L_tr2_c1+e0_x_L_tr2_c2)))))  # noqa: E501,E226
    EQ_alg49 = (0.0-((1.0-((e0_x_L_tr3_c1+e0_x_L_tr3_c2)))))  # noqa: E501,E226
    EQ_alg50 = (0.0-((1.0-((e0_x_L_tr4_c1+e0_x_L_tr4_c2)))))  # noqa: E501,E226
    EQ_alg51 = (0.0-((1.0-((e0_x_L_tr5_c1+e0_x_L_tr5_c2)))))  # noqa: E501,E226
    EQ_alg52 = (0.0-((1.0-((e0_x_L_tr6_c1+e0_x_L_tr6_c2)))))  # noqa: E501,E226
    EQ_alg53 = (0.0-((1.0-((e0_x_L_tr7_c1+e0_x_L_tr7_c2)))))  # noqa: E501,E226
    EQ_alg54 = (0.0-((1.0-((e0_x_L_tr8_c1+e0_x_L_tr8_c2)))))  # noqa: E501,E226
    EQ_alg55 = ((1.0-e0_x_N2)-(((e0_x_V_tr1_c1+e0_x_V_tr1_c2))))  # noqa: E501,E226
    EQ_alg56 = ((1.0-e0_x_N2)-(((e0_x_V_tr2_c1+e0_x_V_tr2_c2))))  # noqa: E501,E226
    EQ_alg57 = ((1.0-e0_x_N2)-(((e0_x_V_tr3_c1+e0_x_V_tr3_c2))))  # noqa: E501,E226
    EQ_alg58 = ((1.0-e0_x_N2)-(((e0_x_V_tr4_c1+e0_x_V_tr4_c2))))  # noqa: E501,E226
    EQ_alg59 = ((1.0-e0_x_N2)-(((e0_x_V_tr5_c1+e0_x_V_tr5_c2))))  # noqa: E501,E226
    EQ_alg60 = ((1.0-e0_x_N2)-(((e0_x_V_tr6_c1+e0_x_V_tr6_c2))))  # noqa: E501,E226
    EQ_alg61 = ((1.0-e0_x_N2)-(((e0_x_V_tr7_c1+e0_x_V_tr7_c2))))  # noqa: E501,E226
    EQ_alg62 = ((1.0-e0_x_N2)-(((e0_x_V_tr8_c1+e0_x_V_tr8_c2))))  # noqa: E501,E226
    EQ_alg63 = (e0_HU_tr1_c1-(((e0_HU_L_tr1*e0_x_L_tr1_c1)+(e0_HU_V_tr1*e0_x_V_tr1_c1))))  # noqa: E501,E226
    EQ_alg64 = (e0_HU_tr2_c1-(((e0_HU_L_tr2*e0_x_L_tr2_c1)+(e0_HU_V_tr2*e0_x_V_tr2_c1))))  # noqa: E501,E226
    EQ_alg65 = (e0_HU_tr3_c1-(((e0_HU_L_tr3*e0_x_L_tr3_c1)+(e0_HU_V_tr3*e0_x_V_tr3_c1))))  # noqa: E501,E226
    EQ_alg66 = (e0_HU_tr4_c1-(((e0_HU_L_tr4*e0_x_L_tr4_c1)+(e0_HU_V_tr4*e0_x_V_tr4_c1))))  # noqa: E501,E226
    EQ_alg67 = (e0_HU_tr5_c1-(((e0_HU_L_tr5*e0_x_L_tr5_c1)+(e0_HU_V_tr5*e0_x_V_tr5_c1))))  # noqa: E501,E226
    EQ_alg68 = (e0_HU_tr6_c1-(((e0_HU_L_tr6*e0_x_L_tr6_c1)+(e0_HU_V_tr6*e0_x_V_tr6_c1))))  # noqa: E501,E226
    EQ_alg69 = (e0_HU_tr7_c1-(((e0_HU_L_tr7*e0_x_L_tr7_c1)+(e0_HU_V_tr7*e0_x_V_tr7_c1))))  # noqa: E501,E226
    EQ_alg70 = (e0_HU_tr8_c1-(((e0_HU_L_tr8*e0_x_L_tr8_c1)+(e0_HU_V_tr8*e0_x_V_tr8_c1))))  # noqa: E501,E226
    EQ_alg71 = (e0_HU_tr1_c2-(((e0_HU_L_tr1*e0_x_L_tr1_c2)+(e0_HU_V_tr1*e0_x_V_tr1_c2))))  # noqa: E501,E226
    EQ_alg72 = (e0_HU_tr2_c2-(((e0_HU_L_tr2*e0_x_L_tr2_c2)+(e0_HU_V_tr2*e0_x_V_tr2_c2))))  # noqa: E501,E226
    EQ_alg73 = (e0_HU_tr3_c2-(((e0_HU_L_tr3*e0_x_L_tr3_c2)+(e0_HU_V_tr3*e0_x_V_tr3_c2))))  # noqa: E501,E226
    EQ_alg74 = (e0_HU_tr4_c2-(((e0_HU_L_tr4*e0_x_L_tr4_c2)+(e0_HU_V_tr4*e0_x_V_tr4_c2))))  # noqa: E501,E226
    EQ_alg75 = (e0_HU_tr5_c2-(((e0_HU_L_tr5*e0_x_L_tr5_c2)+(e0_HU_V_tr5*e0_x_V_tr5_c2))))  # noqa: E501,E226
    EQ_alg76 = (e0_HU_tr6_c2-(((e0_HU_L_tr6*e0_x_L_tr6_c2)+(e0_HU_V_tr6*e0_x_V_tr6_c2))))  # noqa: E501,E226
    EQ_alg77 = (e0_HU_tr7_c2-(((e0_HU_L_tr7*e0_x_L_tr7_c2)+(e0_HU_V_tr7*e0_x_V_tr7_c2))))  # noqa: E501,E226
    EQ_alg78 = (e0_HU_tr8_c2-(((e0_HU_L_tr8*e0_x_L_tr8_c2)+(e0_HU_V_tr8*e0_x_V_tr8_c2))))  # noqa: E501,E226
    EQ_alg79 = (e0_H_tr1-((e0_U_tr1+(e0_p_tr1*(((10.0))**(1.0*2.0)*e0_V_tot)))))  # noqa: E501,E226
    EQ_alg80 = (e0_H_tr2-((e0_U_tr2+(e0_p_tr2*(((10.0))**(1.0*2.0)*e0_V_tot)))))  # noqa: E501,E226
    EQ_alg81 = (e0_H_tr3-((e0_U_tr3+(e0_p_tr3*(((10.0))**(1.0*2.0)*e0_V_tot)))))  # noqa: E501,E226
    EQ_alg82 = (e0_H_tr4-((e0_U_tr4+(e0_p_tr4*(((10.0))**(1.0*2.0)*e0_V_tot)))))  # noqa: E501,E226
    EQ_alg83 = (e0_H_tr5-((e0_U_tr5+(e0_p_tr5*(((10.0))**(1.0*2.0)*e0_V_tot)))))  # noqa: E501,E226
    EQ_alg84 = (e0_H_tr6-((e0_U_tr6+(e0_p_tr6*(((10.0))**(1.0*2.0)*e0_V_tot)))))  # noqa: E501,E226
    EQ_alg85 = (e0_H_tr7-((e0_U_tr7+(e0_p_tr7*(((10.0))**(1.0*2.0)*e0_V_tot)))))  # noqa: E501,E226
    EQ_alg86 = (e0_H_tr8-((e0_U_tr8+(e0_p_tr8*(((10.0))**(1.0*2.0)*e0_V_tot)))))  # noqa: E501,E226
    EQ_alg87 = (e0_H_tr1-(((e0_HU_L_tr1*e0_h_L_tr1)+(e0_HU_V_tr1*e0_h_V_tr1))))  # noqa: E501,E226
    EQ_alg88 = (e0_H_tr2-(((e0_HU_L_tr2*e0_h_L_tr2)+(e0_HU_V_tr2*e0_h_V_tr2))))  # noqa: E501,E226
    EQ_alg89 = (e0_H_tr3-(((e0_HU_L_tr3*e0_h_L_tr3)+(e0_HU_V_tr3*e0_h_V_tr3))))  # noqa: E501,E226
    EQ_alg90 = (e0_H_tr4-(((e0_HU_L_tr4*e0_h_L_tr4)+(e0_HU_V_tr4*e0_h_V_tr4))))  # noqa: E501,E226
    EQ_alg91 = (e0_H_tr5-(((e0_HU_L_tr5*e0_h_L_tr5)+(e0_HU_V_tr5*e0_h_V_tr5))))  # noqa: E501,E226
    EQ_alg92 = (e0_H_tr6-(((e0_HU_L_tr6*e0_h_L_tr6)+(e0_HU_V_tr6*e0_h_V_tr6))))  # noqa: E501,E226
    EQ_alg93 = (e0_H_tr7-(((e0_HU_L_tr7*e0_h_L_tr7)+(e0_HU_V_tr7*e0_h_V_tr7))))  # noqa: E501,E226
    EQ_alg94 = (e0_H_tr8-(((e0_HU_L_tr8*e0_h_L_tr8)+(e0_HU_V_tr8*e0_h_V_tr8))))  # noqa: E501,E226
    EQ_alg95 = (e0_V_tot-((e0_V_L_tr1+e0_V_V_tr1)))  # noqa: E501,E226
    EQ_alg96 = (e0_V_tot-((e0_V_L_tr2+e0_V_V_tr2)))  # noqa: E501,E226
    EQ_alg97 = (e0_V_tot-((e0_V_L_tr3+e0_V_V_tr3)))  # noqa: E501,E226
    EQ_alg98 = (e0_V_tot-((e0_V_L_tr4+e0_V_V_tr4)))  # noqa: E501,E226
    EQ_alg99 = (e0_V_tot-((e0_V_L_tr5+e0_V_V_tr5)))  # noqa: E501,E226
    EQ_alg100 = (e0_V_tot-((e0_V_L_tr6+e0_V_V_tr6)))  # noqa: E501,E226
    EQ_alg101 = (e0_V_tot-((e0_V_L_tr7+e0_V_V_tr7)))  # noqa: E501,E226
    EQ_alg102 = (e0_V_tot-((e0_V_L_tr8+e0_V_V_tr8)))  # noqa: E501,E226
    EQ_alg103 = (e0_V_L_tr1-((e0_HU_L_tr1*e0_v_L_tr1)))  # noqa: E501,E226
    EQ_alg104 = (e0_V_L_tr2-((e0_HU_L_tr2*e0_v_L_tr2)))  # noqa: E501,E226
    EQ_alg105 = (e0_V_L_tr3-((e0_HU_L_tr3*e0_v_L_tr3)))  # noqa: E501,E226
    EQ_alg106 = (e0_V_L_tr4-((e0_HU_L_tr4*e0_v_L_tr4)))  # noqa: E501,E226
    EQ_alg107 = (e0_V_L_tr5-((e0_HU_L_tr5*e0_v_L_tr5)))  # noqa: E501,E226
    EQ_alg108 = (e0_V_L_tr6-((e0_HU_L_tr6*e0_v_L_tr6)))  # noqa: E501,E226
    EQ_alg109 = (e0_V_L_tr7-((e0_HU_L_tr7*e0_v_L_tr7)))  # noqa: E501,E226
    EQ_alg110 = (e0_V_L_tr8-((e0_HU_L_tr8*e0_v_L_tr8)))  # noqa: E501,E226
    EQ_alg111 = ((e0_p_tr1*(((10.0))**(1.0*5.0)*e0_V_V_tr1))-((e0_HU_V_tr1*(e0_R*e0_T_tr1))))  # noqa: E501,E226
    EQ_alg112 = ((e0_p_tr2*(((10.0))**(1.0*5.0)*e0_V_V_tr2))-((e0_HU_V_tr2*(e0_R*e0_T_tr2))))  # noqa: E501,E226
    EQ_alg113 = ((e0_p_tr3*(((10.0))**(1.0*5.0)*e0_V_V_tr3))-((e0_HU_V_tr3*(e0_R*e0_T_tr3))))  # noqa: E501,E226
    EQ_alg114 = ((e0_p_tr4*(((10.0))**(1.0*5.0)*e0_V_V_tr4))-((e0_HU_V_tr4*(e0_R*e0_T_tr4))))  # noqa: E501,E226
    EQ_alg115 = ((e0_p_tr5*(((10.0))**(1.0*5.0)*e0_V_V_tr5))-((e0_HU_V_tr5*(e0_R*e0_T_tr5))))  # noqa: E501,E226
    EQ_alg116 = ((e0_p_tr6*(((10.0))**(1.0*5.0)*e0_V_V_tr6))-((e0_HU_V_tr6*(e0_R*e0_T_tr6))))  # noqa: E501,E226
    EQ_alg117 = ((e0_p_tr7*(((10.0))**(1.0*5.0)*e0_V_V_tr7))-((e0_HU_V_tr7*(e0_R*e0_T_tr7))))  # noqa: E501,E226
    EQ_alg118 = ((e0_p_tr8*(((10.0))**(1.0*5.0)*e0_V_V_tr8))-((e0_HU_V_tr8*(e0_R*e0_T_tr8))))  # noqa: E501,E226
    EQ_alg119 = ((0.82*e0_A_col)-(e0_A_active))  # noqa: E501,E226
    EQ_alg120 = (e0_A_col-((0.25*(e0_greek_pi*((e0_d_col))**(1.0*2.0)))))  # noqa: E501,E226
    EQ_alg121 = ((e0_h_tot*e0_A_col)-(e0_V_tot))  # noqa: E501,E226
    EQ_alg122 = (e0_L_weir-((0.7*e0_d_col)))  # noqa: E501,E226
    EQ_alg123 = (e0_x_V_tr1_c1-((e0_x_V_tr2_c1+(e0_E_murphree*(((e0_K_tr1_c1*e0_x_L_tr1_c1)-e0_x_V_tr2_c1))))))  # noqa: E501,E226
    EQ_alg124 = (e0_x_V_tr2_c1-((e0_x_V_tr3_c1+(e0_E_murphree*(((e0_K_tr2_c1*e0_x_L_tr2_c1)-e0_x_V_tr3_c1))))))  # noqa: E501,E226
    EQ_alg125 = (e0_x_V_tr3_c1-((e0_x_V_tr4_c1+(e0_E_murphree*(((e0_K_tr3_c1*e0_x_L_tr3_c1)-e0_x_V_tr4_c1))))))  # noqa: E501,E226
    EQ_alg126 = (e0_x_V_tr4_c1-((e0_x_V_tr5_c1+(e0_E_murphree*(((e0_K_tr4_c1*e0_x_L_tr4_c1)-e0_x_V_tr5_c1))))))  # noqa: E501,E226
    EQ_alg127 = (e0_x_V_tr5_c1-((e0_x_V_tr6_c1+(e0_E_murphree*(((e0_K_tr5_c1*e0_x_L_tr5_c1)-e0_x_V_tr6_c1))))))  # noqa: E501,E226
    EQ_alg128 = (e0_x_V_tr6_c1-((e0_x_V_tr7_c1+(e0_E_murphree*(((e0_K_tr6_c1*e0_x_L_tr6_c1)-e0_x_V_tr7_c1))))))  # noqa: E501,E226
    EQ_alg129 = (e0_x_V_tr7_c1-((e0_x_V_tr8_c1+(e0_E_murphree*(((e0_K_tr7_c1*e0_x_L_tr7_c1)-e0_x_V_tr8_c1))))))  # noqa: E501,E226
    EQ_alg130 = (e0_x_V_tr8_c1-((e0_x_V_tr9_c1+(e0_E_murphree*(((e0_K_tr8_c1*e0_x_L_tr8_c1)-e0_x_V_tr9_c1))))))  # noqa: E501,E226
    EQ_alg131 = (e0_x_V_tr1_c2-((e0_x_V_tr2_c2+(e0_E_murphree*(((e0_K_tr1_c2*e0_x_L_tr1_c2)-e0_x_V_tr2_c2))))))  # noqa: E501,E226
    EQ_alg132 = (e0_x_V_tr2_c2-((e0_x_V_tr3_c2+(e0_E_murphree*(((e0_K_tr2_c2*e0_x_L_tr2_c2)-e0_x_V_tr3_c2))))))  # noqa: E501,E226
    EQ_alg133 = (e0_x_V_tr3_c2-((e0_x_V_tr4_c2+(e0_E_murphree*(((e0_K_tr3_c2*e0_x_L_tr3_c2)-e0_x_V_tr4_c2))))))  # noqa: E501,E226
    EQ_alg134 = (e0_x_V_tr4_c2-((e0_x_V_tr5_c2+(e0_E_murphree*(((e0_K_tr4_c2*e0_x_L_tr4_c2)-e0_x_V_tr5_c2))))))  # noqa: E501,E226
    EQ_alg135 = (e0_x_V_tr5_c2-((e0_x_V_tr6_c2+(e0_E_murphree*(((e0_K_tr5_c2*e0_x_L_tr5_c2)-e0_x_V_tr6_c2))))))  # noqa: E501,E226
    EQ_alg136 = (e0_x_V_tr6_c2-((e0_x_V_tr7_c2+(e0_E_murphree*(((e0_K_tr6_c2*e0_x_L_tr6_c2)-e0_x_V_tr7_c2))))))  # noqa: E501,E226
    EQ_alg137 = (e0_x_V_tr7_c2-((e0_x_V_tr8_c2+(e0_E_murphree*(((e0_K_tr7_c2*e0_x_L_tr7_c2)-e0_x_V_tr8_c2))))))  # noqa: E501,E226
    EQ_alg138 = (e0_x_V_tr8_c2-((e0_x_V_tr9_c2+(e0_E_murphree*(((e0_K_tr8_c2*e0_x_L_tr8_c2)-e0_x_V_tr9_c2))))))  # noqa: E501,E226
    EQ_alg139 = (0.0-((e0_p_LV_o_tr1_c1-((10.0))**(1.0*(e0_A_c1-(e0_B_c1/(e0_T_tr1+e0_C_c1)))))))  # noqa: E501,E226
    EQ_alg140 = (0.0-((e0_p_LV_o_tr2_c1-((10.0))**(1.0*(e0_A_c1-(e0_B_c1/(e0_T_tr2+e0_C_c1)))))))  # noqa: E501,E226
    EQ_alg141 = (0.0-((e0_p_LV_o_tr3_c1-((10.0))**(1.0*(e0_A_c1-(e0_B_c1/(e0_T_tr3+e0_C_c1)))))))  # noqa: E501,E226
    EQ_alg142 = (0.0-((e0_p_LV_o_tr4_c1-((10.0))**(1.0*(e0_A_c1-(e0_B_c1/(e0_T_tr4+e0_C_c1)))))))  # noqa: E501,E226
    EQ_alg143 = (0.0-((e0_p_LV_o_tr5_c1-((10.0))**(1.0*(e0_A_c1-(e0_B_c1/(e0_T_tr5+e0_C_c1)))))))  # noqa: E501,E226
    EQ_alg144 = (0.0-((e0_p_LV_o_tr6_c1-((10.0))**(1.0*(e0_A_c1-(e0_B_c1/(e0_T_tr6+e0_C_c1)))))))  # noqa: E501,E226
    EQ_alg145 = (0.0-((e0_p_LV_o_tr7_c1-((10.0))**(1.0*(e0_A_c1-(e0_B_c1/(e0_T_tr7+e0_C_c1)))))))  # noqa: E501,E226
    EQ_alg146 = (0.0-((e0_p_LV_o_tr8_c1-((10.0))**(1.0*(e0_A_c1-(e0_B_c1/(e0_T_tr8+e0_C_c1)))))))  # noqa: E501,E226
    EQ_alg147 = (0.0-((e0_p_LV_o_tr1_c2-((10.0))**(1.0*(e0_A_c2-(e0_B_c2/(e0_T_tr1+e0_C_c2)))))))  # noqa: E501,E226
    EQ_alg148 = (0.0-((e0_p_LV_o_tr2_c2-((10.0))**(1.0*(e0_A_c2-(e0_B_c2/(e0_T_tr2+e0_C_c2)))))))  # noqa: E501,E226
    EQ_alg149 = (0.0-((e0_p_LV_o_tr3_c2-((10.0))**(1.0*(e0_A_c2-(e0_B_c2/(e0_T_tr3+e0_C_c2)))))))  # noqa: E501,E226
    EQ_alg150 = (0.0-((e0_p_LV_o_tr4_c2-((10.0))**(1.0*(e0_A_c2-(e0_B_c2/(e0_T_tr4+e0_C_c2)))))))  # noqa: E501,E226
    EQ_alg151 = (0.0-((e0_p_LV_o_tr5_c2-((10.0))**(1.0*(e0_A_c2-(e0_B_c2/(e0_T_tr5+e0_C_c2)))))))  # noqa: E501,E226
    EQ_alg152 = (0.0-((e0_p_LV_o_tr6_c2-((10.0))**(1.0*(e0_A_c2-(e0_B_c2/(e0_T_tr6+e0_C_c2)))))))  # noqa: E501,E226
    EQ_alg153 = (0.0-((e0_p_LV_o_tr7_c2-((10.0))**(1.0*(e0_A_c2-(e0_B_c2/(e0_T_tr7+e0_C_c2)))))))  # noqa: E501,E226
    EQ_alg154 = (0.0-((e0_p_LV_o_tr8_c2-((10.0))**(1.0*(e0_A_c2-(e0_B_c2/(e0_T_tr8+e0_C_c2)))))))  # noqa: E501,E226


    # EQ_alg155 = (e0_F_L_tr1-((((((((e0_L_tr1-e0_h_weir)/0.664)+(((((((e0_L_tr1-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir/e0_v_L_tr1))))  # noqa: E501,E226
    # EQ_alg156 = (e0_F_L_tr2-((((((((e0_L_tr2-e0_h_weir)/0.664)+(((((((e0_L_tr2-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir/e0_v_L_tr2))))  # noqa: E501,E226
    # EQ_alg157 = (e0_F_L_tr3-((((((((e0_L_tr3-e0_h_weir)/0.664)+(((((((e0_L_tr3-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir/e0_v_L_tr3))))  # noqa: E501,E226
    # EQ_alg158 = (e0_F_L_tr4-((((((((e0_L_tr4-e0_h_weir)/0.664)+(((((((e0_L_tr4-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir/e0_v_L_tr4))))  # noqa: E501,E226
    # EQ_alg159 = (e0_F_L_tr5-((((((((e0_L_tr5-e0_h_weir)/0.664)+(((((((e0_L_tr5-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir/e0_v_L_tr5))))  # noqa: E501,E226
    # EQ_alg160 = (e0_F_L_tr6-((((((((e0_L_tr6-e0_h_weir)/0.664)+(((((((e0_L_tr6-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir/e0_v_L_tr6))))  # noqa: E501,E226
    # EQ_alg161 = (e0_F_L_tr7-((((((((e0_L_tr7-e0_h_weir)/0.664)+(((((((e0_L_tr7-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir/e0_v_L_tr7))))  # noqa: E501,E226
    # EQ_alg162 = (e0_F_L_tr8-((((((((e0_L_tr8-e0_h_weir)/0.664)+(((((((e0_L_tr8-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir/e0_v_L_tr8))))  # noqa: E501,E226
    EQ_alg155 = 1e3 * (e0_v_L_tr1 * e0_F_L_tr1-((((((((e0_L_tr1-e0_h_weir)/0.664)+(((((((e0_L_tr1-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir))))  # noqa: E501,E226
    EQ_alg156 = 1e3 * (e0_v_L_tr2 * e0_F_L_tr2-((((((((e0_L_tr2-e0_h_weir)/0.664)+(((((((e0_L_tr2-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir))))  # noqa: E501,E226
    EQ_alg157 = 1e3 * (e0_v_L_tr3 * e0_F_L_tr3-((((((((e0_L_tr3-e0_h_weir)/0.664)+(((((((e0_L_tr3-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir))))  # noqa: E501,E226
    EQ_alg158 = 1e3 * (e0_v_L_tr4 * e0_F_L_tr4-((((((((e0_L_tr4-e0_h_weir)/0.664)+(((((((e0_L_tr4-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir))))  # noqa: E501,E226
    EQ_alg159 = 1e3 * (e0_v_L_tr5 * e0_F_L_tr5-((((((((e0_L_tr5-e0_h_weir)/0.664)+(((((((e0_L_tr5-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir))))  # noqa: E501,E226
    EQ_alg160 = 1e3 * (e0_v_L_tr6 * e0_F_L_tr6-((((((((e0_L_tr6-e0_h_weir)/0.664)+(((((((e0_L_tr6-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir))))  # noqa: E501,E226
    EQ_alg161 = 1e3 * (e0_v_L_tr7 * e0_F_L_tr7-((((((((e0_L_tr7-e0_h_weir)/0.664)+(((((((e0_L_tr7-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir))))  # noqa: E501,E226
    EQ_alg162 = 1e3 * (e0_v_L_tr8 * e0_F_L_tr8-((((((((e0_L_tr8-e0_h_weir)/0.664)+(((((((e0_L_tr8-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir))))  # noqa: E501,E226


    EQ_alg163 = (e0_L_tr1-(((e0_HU_L_tr1*e0_v_L_tr1)/e0_A_active)))  # noqa: E501,E226
    EQ_alg164 = (e0_L_tr2-(((e0_HU_L_tr2*e0_v_L_tr2)/e0_A_active)))  # noqa: E501,E226
    EQ_alg165 = (e0_L_tr3-(((e0_HU_L_tr3*e0_v_L_tr3)/e0_A_active)))  # noqa: E501,E226
    EQ_alg166 = (e0_L_tr4-(((e0_HU_L_tr4*e0_v_L_tr4)/e0_A_active)))  # noqa: E501,E226
    EQ_alg167 = (e0_L_tr5-(((e0_HU_L_tr5*e0_v_L_tr5)/e0_A_active)))  # noqa: E501,E226
    EQ_alg168 = (e0_L_tr6-(((e0_HU_L_tr6*e0_v_L_tr6)/e0_A_active)))  # noqa: E501,E226
    EQ_alg169 = (e0_L_tr7-(((e0_HU_L_tr7*e0_v_L_tr7)/e0_A_active)))  # noqa: E501,E226
    EQ_alg170 = (e0_L_tr8-(((e0_HU_L_tr8*e0_v_L_tr8)/e0_A_active)))  # noqa: E501,E226
    EQ_alg171 = ((e0_p_tr1-e0_p_tr0)-(((e0_greek_kappa*((e0_F_V_tr1))**(1.0*2.0))+e0_greek_kappa_hyst)))  # noqa: E501,E226
    EQ_alg172 = ((e0_p_tr2-e0_p_tr1)-(((e0_greek_kappa*((e0_F_V_tr2))**(1.0*2.0))+e0_greek_kappa_hyst)))  # noqa: E501,E226
    EQ_alg173 = ((e0_p_tr3-e0_p_tr2)-(((e0_greek_kappa*((e0_F_V_tr3))**(1.0*2.0))+e0_greek_kappa_hyst)))  # noqa: E501,E226
    EQ_alg174 = ((e0_p_tr4-e0_p_tr3)-(((e0_greek_kappa*((e0_F_V_tr4))**(1.0*2.0))+e0_greek_kappa_hyst)))  # noqa: E501,E226
    EQ_alg175 = ((e0_p_tr5-e0_p_tr4)-(((e0_greek_kappa*((e0_F_V_tr5))**(1.0*2.0))+e0_greek_kappa_hyst)))  # noqa: E501,E226
    EQ_alg176 = ((e0_p_tr6-e0_p_tr5)-(((e0_greek_kappa*((e0_F_V_tr6))**(1.0*2.0))+e0_greek_kappa_hyst)))  # noqa: E501,E226
    EQ_alg177 = ((e0_p_tr7-e0_p_tr6)-(((e0_greek_kappa*((e0_F_V_tr7))**(1.0*2.0))+e0_greek_kappa_hyst)))  # noqa: E501,E226
    EQ_alg178 = ((e0_p_tr8-e0_p_tr7)-(((e0_greek_kappa*((e0_F_V_tr8))**(1.0*2.0))+e0_greek_kappa_hyst)))  # noqa: E501,E226
    EQ_alg179 = (e0_h_L_tr1-((((e0_x_L_tr1_c1*e0_h_L_tr1_c1)+(e0_x_L_tr1_c2*e0_h_L_tr1_c2)))))  # noqa: E501,E226
    EQ_alg180 = (e0_h_L_tr2-((((e0_x_L_tr2_c1*e0_h_L_tr2_c1)+(e0_x_L_tr2_c2*e0_h_L_tr2_c2)))))  # noqa: E501,E226
    EQ_alg181 = (e0_h_L_tr3-((((e0_x_L_tr3_c1*e0_h_L_tr3_c1)+(e0_x_L_tr3_c2*e0_h_L_tr3_c2)))))  # noqa: E501,E226
    EQ_alg182 = (e0_h_L_tr4-((((e0_x_L_tr4_c1*e0_h_L_tr4_c1)+(e0_x_L_tr4_c2*e0_h_L_tr4_c2)))))  # noqa: E501,E226
    EQ_alg183 = (e0_h_L_tr5-((((e0_x_L_tr5_c1*e0_h_L_tr5_c1)+(e0_x_L_tr5_c2*e0_h_L_tr5_c2)))))  # noqa: E501,E226
    EQ_alg184 = (e0_h_L_tr6-((((e0_x_L_tr6_c1*e0_h_L_tr6_c1)+(e0_x_L_tr6_c2*e0_h_L_tr6_c2)))))  # noqa: E501,E226
    EQ_alg185 = (e0_h_L_tr7-((((e0_x_L_tr7_c1*e0_h_L_tr7_c1)+(e0_x_L_tr7_c2*e0_h_L_tr7_c2)))))  # noqa: E501,E226
    EQ_alg186 = (e0_h_L_tr8-((((e0_x_L_tr8_c1*e0_h_L_tr8_c1)+(e0_x_L_tr8_c2*e0_h_L_tr8_c2)))))  # noqa: E501,E226
    EQ_alg187 = (0.0-((e0_h_V_tr1-(((e0_x_V_tr1_c1*e0_h_V_tr1_c1)+(e0_x_V_tr1_c2*e0_h_V_tr1_c2))))))  # noqa: E501,E226
    EQ_alg188 = (0.0-((e0_h_V_tr2-(((e0_x_V_tr2_c1*e0_h_V_tr2_c1)+(e0_x_V_tr2_c2*e0_h_V_tr2_c2))))))  # noqa: E501,E226
    EQ_alg189 = (0.0-((e0_h_V_tr3-(((e0_x_V_tr3_c1*e0_h_V_tr3_c1)+(e0_x_V_tr3_c2*e0_h_V_tr3_c2))))))  # noqa: E501,E226
    EQ_alg190 = (0.0-((e0_h_V_tr4-(((e0_x_V_tr4_c1*e0_h_V_tr4_c1)+(e0_x_V_tr4_c2*e0_h_V_tr4_c2))))))  # noqa: E501,E226
    EQ_alg191 = (0.0-((e0_h_V_tr5-(((e0_x_V_tr5_c1*e0_h_V_tr5_c1)+(e0_x_V_tr5_c2*e0_h_V_tr5_c2))))))  # noqa: E501,E226
    EQ_alg192 = (0.0-((e0_h_V_tr6-(((e0_x_V_tr6_c1*e0_h_V_tr6_c1)+(e0_x_V_tr6_c2*e0_h_V_tr6_c2))))))  # noqa: E501,E226
    EQ_alg193 = (0.0-((e0_h_V_tr7-(((e0_x_V_tr7_c1*e0_h_V_tr7_c1)+(e0_x_V_tr7_c2*e0_h_V_tr7_c2))))))  # noqa: E501,E226
    EQ_alg194 = (0.0-((e0_h_V_tr8-(((e0_x_V_tr8_c1*e0_h_V_tr8_c1)+(e0_x_V_tr8_c2*e0_h_V_tr8_c2))))))  # noqa: E501,E226
    EQ_alg195 = ((e0_p_tr1*e0_K_tr1_c1)-((e0_p_LV_o_tr1_c1*(((e0_greek_lambda_activity*e0_greek_gamma_tr1_c1)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
    EQ_alg196 = ((e0_p_tr2*e0_K_tr2_c1)-((e0_p_LV_o_tr2_c1*(((e0_greek_lambda_activity*e0_greek_gamma_tr2_c1)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
    EQ_alg197 = ((e0_p_tr3*e0_K_tr3_c1)-((e0_p_LV_o_tr3_c1*(((e0_greek_lambda_activity*e0_greek_gamma_tr3_c1)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
    EQ_alg198 = ((e0_p_tr4*e0_K_tr4_c1)-((e0_p_LV_o_tr4_c1*(((e0_greek_lambda_activity*e0_greek_gamma_tr4_c1)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
    EQ_alg199 = ((e0_p_tr5*e0_K_tr5_c1)-((e0_p_LV_o_tr5_c1*(((e0_greek_lambda_activity*e0_greek_gamma_tr5_c1)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
    EQ_alg200 = ((e0_p_tr6*e0_K_tr6_c1)-((e0_p_LV_o_tr6_c1*(((e0_greek_lambda_activity*e0_greek_gamma_tr6_c1)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
    EQ_alg201 = ((e0_p_tr7*e0_K_tr7_c1)-((e0_p_LV_o_tr7_c1*(((e0_greek_lambda_activity*e0_greek_gamma_tr7_c1)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
    EQ_alg202 = ((e0_p_tr8*e0_K_tr8_c1)-((e0_p_LV_o_tr8_c1*(((e0_greek_lambda_activity*e0_greek_gamma_tr8_c1)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
    EQ_alg203 = ((e0_p_tr1*e0_K_tr1_c2)-((e0_p_LV_o_tr1_c2*(((e0_greek_lambda_activity*e0_greek_gamma_tr1_c2)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
    EQ_alg204 = ((e0_p_tr2*e0_K_tr2_c2)-((e0_p_LV_o_tr2_c2*(((e0_greek_lambda_activity*e0_greek_gamma_tr2_c2)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
    EQ_alg205 = ((e0_p_tr3*e0_K_tr3_c2)-((e0_p_LV_o_tr3_c2*(((e0_greek_lambda_activity*e0_greek_gamma_tr3_c2)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
    EQ_alg206 = ((e0_p_tr4*e0_K_tr4_c2)-((e0_p_LV_o_tr4_c2*(((e0_greek_lambda_activity*e0_greek_gamma_tr4_c2)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
    EQ_alg207 = ((e0_p_tr5*e0_K_tr5_c2)-((e0_p_LV_o_tr5_c2*(((e0_greek_lambda_activity*e0_greek_gamma_tr5_c2)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
    EQ_alg208 = ((e0_p_tr6*e0_K_tr6_c2)-((e0_p_LV_o_tr6_c2*(((e0_greek_lambda_activity*e0_greek_gamma_tr6_c2)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
    EQ_alg209 = ((e0_p_tr7*e0_K_tr7_c2)-((e0_p_LV_o_tr7_c2*(((e0_greek_lambda_activity*e0_greek_gamma_tr7_c2)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
    EQ_alg210 = ((e0_p_tr8*e0_K_tr8_c2)-((e0_p_LV_o_tr8_c2*(((e0_greek_lambda_activity*e0_greek_gamma_tr8_c2)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
    EQ_alg211 = (e0_greek_alpha_tr1_c1-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c1)/e0_v_L_c1)*ca.exp(((-e0_greek_lambda_c1)/e0_T_tr1)))))  # noqa: E501,E226
    EQ_alg212 = (e0_greek_alpha_tr2_c1-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c1)/e0_v_L_c1)*ca.exp(((-e0_greek_lambda_c1)/e0_T_tr2)))))  # noqa: E501,E226
    EQ_alg213 = (e0_greek_alpha_tr3_c1-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c1)/e0_v_L_c1)*ca.exp(((-e0_greek_lambda_c1)/e0_T_tr3)))))  # noqa: E501,E226
    EQ_alg214 = (e0_greek_alpha_tr4_c1-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c1)/e0_v_L_c1)*ca.exp(((-e0_greek_lambda_c1)/e0_T_tr4)))))  # noqa: E501,E226
    EQ_alg215 = (e0_greek_alpha_tr5_c1-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c1)/e0_v_L_c1)*ca.exp(((-e0_greek_lambda_c1)/e0_T_tr5)))))  # noqa: E501,E226
    EQ_alg216 = (e0_greek_alpha_tr6_c1-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c1)/e0_v_L_c1)*ca.exp(((-e0_greek_lambda_c1)/e0_T_tr6)))))  # noqa: E501,E226
    EQ_alg217 = (e0_greek_alpha_tr7_c1-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c1)/e0_v_L_c1)*ca.exp(((-e0_greek_lambda_c1)/e0_T_tr7)))))  # noqa: E501,E226
    EQ_alg218 = (e0_greek_alpha_tr8_c1-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c1)/e0_v_L_c1)*ca.exp(((-e0_greek_lambda_c1)/e0_T_tr8)))))  # noqa: E501,E226
    EQ_alg219 = (e0_greek_alpha_tr1_c2-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c2)/e0_v_L_c2)*ca.exp(((-e0_greek_lambda_c2)/e0_T_tr1)))))  # noqa: E501,E226
    EQ_alg220 = (e0_greek_alpha_tr2_c2-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c2)/e0_v_L_c2)*ca.exp(((-e0_greek_lambda_c2)/e0_T_tr2)))))  # noqa: E501,E226
    EQ_alg221 = (e0_greek_alpha_tr3_c2-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c2)/e0_v_L_c2)*ca.exp(((-e0_greek_lambda_c2)/e0_T_tr3)))))  # noqa: E501,E226
    EQ_alg222 = (e0_greek_alpha_tr4_c2-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c2)/e0_v_L_c2)*ca.exp(((-e0_greek_lambda_c2)/e0_T_tr4)))))  # noqa: E501,E226
    EQ_alg223 = (e0_greek_alpha_tr5_c2-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c2)/e0_v_L_c2)*ca.exp(((-e0_greek_lambda_c2)/e0_T_tr5)))))  # noqa: E501,E226
    EQ_alg224 = (e0_greek_alpha_tr6_c2-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c2)/e0_v_L_c2)*ca.exp(((-e0_greek_lambda_c2)/e0_T_tr6)))))  # noqa: E501,E226
    EQ_alg225 = (e0_greek_alpha_tr7_c2-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c2)/e0_v_L_c2)*ca.exp(((-e0_greek_lambda_c2)/e0_T_tr7)))))  # noqa: E501,E226
    EQ_alg226 = (e0_greek_alpha_tr8_c2-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c2)/e0_v_L_c2)*ca.exp(((-e0_greek_lambda_c2)/e0_T_tr8)))))  # noqa: E501,E226
    EQ_alg227 = (e0_greek_gamma_tr1_c1-(((1.0/(e0_x_L_tr1_c1+(e0_greek_alpha_tr1_c1*((1.0-e0_x_L_tr1_c1)))))*ca.exp((((1.0-e0_x_L_tr1_c1))*(((e0_greek_alpha_tr1_c1/(e0_x_L_tr1_c1+(e0_greek_alpha_tr1_c1*((1.0-e0_x_L_tr1_c1)))))-((((e0_greek_alpha_tr1_c1+e0_greek_alpha_tr1_c2))-e0_greek_alpha_tr1_c1)/((((((e0_greek_alpha_tr1_c1+e0_greek_alpha_tr1_c2))-e0_greek_alpha_tr1_c1))*e0_x_L_tr1_c1)+((1.0-e0_x_L_tr1_c1)))))))))))  # noqa: E501,E226
    EQ_alg228 = (e0_greek_gamma_tr2_c1-(((1.0/(e0_x_L_tr2_c1+(e0_greek_alpha_tr2_c1*((1.0-e0_x_L_tr2_c1)))))*ca.exp((((1.0-e0_x_L_tr2_c1))*(((e0_greek_alpha_tr2_c1/(e0_x_L_tr2_c1+(e0_greek_alpha_tr2_c1*((1.0-e0_x_L_tr2_c1)))))-((((e0_greek_alpha_tr2_c1+e0_greek_alpha_tr2_c2))-e0_greek_alpha_tr2_c1)/((((((e0_greek_alpha_tr2_c1+e0_greek_alpha_tr2_c2))-e0_greek_alpha_tr2_c1))*e0_x_L_tr2_c1)+((1.0-e0_x_L_tr2_c1)))))))))))  # noqa: E501,E226
    EQ_alg229 = (e0_greek_gamma_tr3_c1-(((1.0/(e0_x_L_tr3_c1+(e0_greek_alpha_tr3_c1*((1.0-e0_x_L_tr3_c1)))))*ca.exp((((1.0-e0_x_L_tr3_c1))*(((e0_greek_alpha_tr3_c1/(e0_x_L_tr3_c1+(e0_greek_alpha_tr3_c1*((1.0-e0_x_L_tr3_c1)))))-((((e0_greek_alpha_tr3_c1+e0_greek_alpha_tr3_c2))-e0_greek_alpha_tr3_c1)/((((((e0_greek_alpha_tr3_c1+e0_greek_alpha_tr3_c2))-e0_greek_alpha_tr3_c1))*e0_x_L_tr3_c1)+((1.0-e0_x_L_tr3_c1)))))))))))  # noqa: E501,E226
    EQ_alg230 = (e0_greek_gamma_tr4_c1-(((1.0/(e0_x_L_tr4_c1+(e0_greek_alpha_tr4_c1*((1.0-e0_x_L_tr4_c1)))))*ca.exp((((1.0-e0_x_L_tr4_c1))*(((e0_greek_alpha_tr4_c1/(e0_x_L_tr4_c1+(e0_greek_alpha_tr4_c1*((1.0-e0_x_L_tr4_c1)))))-((((e0_greek_alpha_tr4_c1+e0_greek_alpha_tr4_c2))-e0_greek_alpha_tr4_c1)/((((((e0_greek_alpha_tr4_c1+e0_greek_alpha_tr4_c2))-e0_greek_alpha_tr4_c1))*e0_x_L_tr4_c1)+((1.0-e0_x_L_tr4_c1)))))))))))  # noqa: E501,E226
    EQ_alg231 = (e0_greek_gamma_tr5_c1-(((1.0/(e0_x_L_tr5_c1+(e0_greek_alpha_tr5_c1*((1.0-e0_x_L_tr5_c1)))))*ca.exp((((1.0-e0_x_L_tr5_c1))*(((e0_greek_alpha_tr5_c1/(e0_x_L_tr5_c1+(e0_greek_alpha_tr5_c1*((1.0-e0_x_L_tr5_c1)))))-((((e0_greek_alpha_tr5_c1+e0_greek_alpha_tr5_c2))-e0_greek_alpha_tr5_c1)/((((((e0_greek_alpha_tr5_c1+e0_greek_alpha_tr5_c2))-e0_greek_alpha_tr5_c1))*e0_x_L_tr5_c1)+((1.0-e0_x_L_tr5_c1)))))))))))  # noqa: E501,E226
    EQ_alg232 = (e0_greek_gamma_tr6_c1-(((1.0/(e0_x_L_tr6_c1+(e0_greek_alpha_tr6_c1*((1.0-e0_x_L_tr6_c1)))))*ca.exp((((1.0-e0_x_L_tr6_c1))*(((e0_greek_alpha_tr6_c1/(e0_x_L_tr6_c1+(e0_greek_alpha_tr6_c1*((1.0-e0_x_L_tr6_c1)))))-((((e0_greek_alpha_tr6_c1+e0_greek_alpha_tr6_c2))-e0_greek_alpha_tr6_c1)/((((((e0_greek_alpha_tr6_c1+e0_greek_alpha_tr6_c2))-e0_greek_alpha_tr6_c1))*e0_x_L_tr6_c1)+((1.0-e0_x_L_tr6_c1)))))))))))  # noqa: E501,E226
    EQ_alg233 = (e0_greek_gamma_tr7_c1-(((1.0/(e0_x_L_tr7_c1+(e0_greek_alpha_tr7_c1*((1.0-e0_x_L_tr7_c1)))))*ca.exp((((1.0-e0_x_L_tr7_c1))*(((e0_greek_alpha_tr7_c1/(e0_x_L_tr7_c1+(e0_greek_alpha_tr7_c1*((1.0-e0_x_L_tr7_c1)))))-((((e0_greek_alpha_tr7_c1+e0_greek_alpha_tr7_c2))-e0_greek_alpha_tr7_c1)/((((((e0_greek_alpha_tr7_c1+e0_greek_alpha_tr7_c2))-e0_greek_alpha_tr7_c1))*e0_x_L_tr7_c1)+((1.0-e0_x_L_tr7_c1)))))))))))  # noqa: E501,E226
    EQ_alg234 = (e0_greek_gamma_tr8_c1-(((1.0/(e0_x_L_tr8_c1+(e0_greek_alpha_tr8_c1*((1.0-e0_x_L_tr8_c1)))))*ca.exp((((1.0-e0_x_L_tr8_c1))*(((e0_greek_alpha_tr8_c1/(e0_x_L_tr8_c1+(e0_greek_alpha_tr8_c1*((1.0-e0_x_L_tr8_c1)))))-((((e0_greek_alpha_tr8_c1+e0_greek_alpha_tr8_c2))-e0_greek_alpha_tr8_c1)/((((((e0_greek_alpha_tr8_c1+e0_greek_alpha_tr8_c2))-e0_greek_alpha_tr8_c1))*e0_x_L_tr8_c1)+((1.0-e0_x_L_tr8_c1)))))))))))  # noqa: E501,E226
    EQ_alg235 = (e0_greek_gamma_tr1_c2-(((1.0/(e0_x_L_tr1_c2+(e0_greek_alpha_tr1_c2*((1.0-e0_x_L_tr1_c2)))))*ca.exp((((1.0-e0_x_L_tr1_c2))*(((e0_greek_alpha_tr1_c2/(e0_x_L_tr1_c2+(e0_greek_alpha_tr1_c2*((1.0-e0_x_L_tr1_c2)))))-((((e0_greek_alpha_tr1_c1+e0_greek_alpha_tr1_c2))-e0_greek_alpha_tr1_c2)/((((((e0_greek_alpha_tr1_c1+e0_greek_alpha_tr1_c2))-e0_greek_alpha_tr1_c2))*e0_x_L_tr1_c2)+((1.0-e0_x_L_tr1_c2)))))))))))  # noqa: E501,E226
    EQ_alg236 = (e0_greek_gamma_tr2_c2-(((1.0/(e0_x_L_tr2_c2+(e0_greek_alpha_tr2_c2*((1.0-e0_x_L_tr2_c2)))))*ca.exp((((1.0-e0_x_L_tr2_c2))*(((e0_greek_alpha_tr2_c2/(e0_x_L_tr2_c2+(e0_greek_alpha_tr2_c2*((1.0-e0_x_L_tr2_c2)))))-((((e0_greek_alpha_tr2_c1+e0_greek_alpha_tr2_c2))-e0_greek_alpha_tr2_c2)/((((((e0_greek_alpha_tr2_c1+e0_greek_alpha_tr2_c2))-e0_greek_alpha_tr2_c2))*e0_x_L_tr2_c2)+((1.0-e0_x_L_tr2_c2)))))))))))  # noqa: E501,E226
    EQ_alg237 = (e0_greek_gamma_tr3_c2-(((1.0/(e0_x_L_tr3_c2+(e0_greek_alpha_tr3_c2*((1.0-e0_x_L_tr3_c2)))))*ca.exp((((1.0-e0_x_L_tr3_c2))*(((e0_greek_alpha_tr3_c2/(e0_x_L_tr3_c2+(e0_greek_alpha_tr3_c2*((1.0-e0_x_L_tr3_c2)))))-((((e0_greek_alpha_tr3_c1+e0_greek_alpha_tr3_c2))-e0_greek_alpha_tr3_c2)/((((((e0_greek_alpha_tr3_c1+e0_greek_alpha_tr3_c2))-e0_greek_alpha_tr3_c2))*e0_x_L_tr3_c2)+((1.0-e0_x_L_tr3_c2)))))))))))  # noqa: E501,E226
    EQ_alg238 = (e0_greek_gamma_tr4_c2-(((1.0/(e0_x_L_tr4_c2+(e0_greek_alpha_tr4_c2*((1.0-e0_x_L_tr4_c2)))))*ca.exp((((1.0-e0_x_L_tr4_c2))*(((e0_greek_alpha_tr4_c2/(e0_x_L_tr4_c2+(e0_greek_alpha_tr4_c2*((1.0-e0_x_L_tr4_c2)))))-((((e0_greek_alpha_tr4_c1+e0_greek_alpha_tr4_c2))-e0_greek_alpha_tr4_c2)/((((((e0_greek_alpha_tr4_c1+e0_greek_alpha_tr4_c2))-e0_greek_alpha_tr4_c2))*e0_x_L_tr4_c2)+((1.0-e0_x_L_tr4_c2)))))))))))  # noqa: E501,E226
    EQ_alg239 = (e0_greek_gamma_tr5_c2-(((1.0/(e0_x_L_tr5_c2+(e0_greek_alpha_tr5_c2*((1.0-e0_x_L_tr5_c2)))))*ca.exp((((1.0-e0_x_L_tr5_c2))*(((e0_greek_alpha_tr5_c2/(e0_x_L_tr5_c2+(e0_greek_alpha_tr5_c2*((1.0-e0_x_L_tr5_c2)))))-((((e0_greek_alpha_tr5_c1+e0_greek_alpha_tr5_c2))-e0_greek_alpha_tr5_c2)/((((((e0_greek_alpha_tr5_c1+e0_greek_alpha_tr5_c2))-e0_greek_alpha_tr5_c2))*e0_x_L_tr5_c2)+((1.0-e0_x_L_tr5_c2)))))))))))  # noqa: E501,E226
    EQ_alg240 = (e0_greek_gamma_tr6_c2-(((1.0/(e0_x_L_tr6_c2+(e0_greek_alpha_tr6_c2*((1.0-e0_x_L_tr6_c2)))))*ca.exp((((1.0-e0_x_L_tr6_c2))*(((e0_greek_alpha_tr6_c2/(e0_x_L_tr6_c2+(e0_greek_alpha_tr6_c2*((1.0-e0_x_L_tr6_c2)))))-((((e0_greek_alpha_tr6_c1+e0_greek_alpha_tr6_c2))-e0_greek_alpha_tr6_c2)/((((((e0_greek_alpha_tr6_c1+e0_greek_alpha_tr6_c2))-e0_greek_alpha_tr6_c2))*e0_x_L_tr6_c2)+((1.0-e0_x_L_tr6_c2)))))))))))  # noqa: E501,E226
    EQ_alg241 = (e0_greek_gamma_tr7_c2-(((1.0/(e0_x_L_tr7_c2+(e0_greek_alpha_tr7_c2*((1.0-e0_x_L_tr7_c2)))))*ca.exp((((1.0-e0_x_L_tr7_c2))*(((e0_greek_alpha_tr7_c2/(e0_x_L_tr7_c2+(e0_greek_alpha_tr7_c2*((1.0-e0_x_L_tr7_c2)))))-((((e0_greek_alpha_tr7_c1+e0_greek_alpha_tr7_c2))-e0_greek_alpha_tr7_c2)/((((((e0_greek_alpha_tr7_c1+e0_greek_alpha_tr7_c2))-e0_greek_alpha_tr7_c2))*e0_x_L_tr7_c2)+((1.0-e0_x_L_tr7_c2)))))))))))  # noqa: E501,E226
    EQ_alg242 = (e0_greek_gamma_tr8_c2-(((1.0/(e0_x_L_tr8_c2+(e0_greek_alpha_tr8_c2*((1.0-e0_x_L_tr8_c2)))))*ca.exp((((1.0-e0_x_L_tr8_c2))*(((e0_greek_alpha_tr8_c2/(e0_x_L_tr8_c2+(e0_greek_alpha_tr8_c2*((1.0-e0_x_L_tr8_c2)))))-((((e0_greek_alpha_tr8_c1+e0_greek_alpha_tr8_c2))-e0_greek_alpha_tr8_c2)/((((((e0_greek_alpha_tr8_c1+e0_greek_alpha_tr8_c2))-e0_greek_alpha_tr8_c2))*e0_x_L_tr8_c2)+((1.0-e0_x_L_tr8_c2)))))))))))  # noqa: E501,E226
    EQ_alg243 = (e0_v_L_tr1-((((e0_x_L_tr1_c1*e0_v_L_c1)+(e0_x_L_tr1_c2*e0_v_L_c2)))))  # noqa: E501,E226
    EQ_alg244 = (e0_v_L_tr2-((((e0_x_L_tr2_c1*e0_v_L_c1)+(e0_x_L_tr2_c2*e0_v_L_c2)))))  # noqa: E501,E226
    EQ_alg245 = (e0_v_L_tr3-((((e0_x_L_tr3_c1*e0_v_L_c1)+(e0_x_L_tr3_c2*e0_v_L_c2)))))  # noqa: E501,E226
    EQ_alg246 = (e0_v_L_tr4-((((e0_x_L_tr4_c1*e0_v_L_c1)+(e0_x_L_tr4_c2*e0_v_L_c2)))))  # noqa: E501,E226
    EQ_alg247 = (e0_v_L_tr5-((((e0_x_L_tr5_c1*e0_v_L_c1)+(e0_x_L_tr5_c2*e0_v_L_c2)))))  # noqa: E501,E226
    EQ_alg248 = (e0_v_L_tr6-((((e0_x_L_tr6_c1*e0_v_L_c1)+(e0_x_L_tr6_c2*e0_v_L_c2)))))  # noqa: E501,E226
    EQ_alg249 = (e0_v_L_tr7-((((e0_x_L_tr7_c1*e0_v_L_c1)+(e0_x_L_tr7_c2*e0_v_L_c2)))))  # noqa: E501,E226
    EQ_alg250 = (e0_v_L_tr8-((((e0_x_L_tr8_c1*e0_v_L_c1)+(e0_x_L_tr8_c2*e0_v_L_c2)))))  # noqa: E501,E226
    EQ_alg251 = (0.0-((1.0-((e0_x_L_tr9_c1+e0_x_L_tr9_c2)))))  # noqa: E501,E226
    # EQ_alg252 = (0.0-((1.0-((e0_x_V_tr9_c1+e0_x_V_tr9_c2)))))  # noqa: E501,E226
    EQ_alg252 = ((1.0-e0_x_N2)-(((e0_x_V_tr9_c1+e0_x_V_tr9_c2))))
    EQ_alg253 = (e0_HU_tr9_c1-(((e0_HU_L_tr9*e0_x_L_tr9_c1)+(e0_HU_V_tr9*e0_x_V_tr9_c1))))  # noqa: E501,E226
    EQ_alg254 = (e0_HU_tr9_c2-(((e0_HU_L_tr9*e0_x_L_tr9_c2)+(e0_HU_V_tr9*e0_x_V_tr9_c2))))  # noqa: E501,E226
    # EQ_alg255 = (e0_H_tr9-((e0_U_tr9+(e0_p_tr9*(((10.0))**(1.0*2.0)*e0_V_tot_tr9)))))  # noqa: E501,E226
    EQ_alg255 = 1e-3 * (e0_H_tr9-((e0_U_tr9+(e0_p_tr9*(((10.0))**(1.0*2.0)*e0_V_tot_tr9)))))  # noqa: E501,E226
    EQ_alg256 = (1/300.0) * (e0_H_tr9-(((e0_HU_L_tr9*e0_h_L_tr9)+(e0_HU_V_tr9*e0_h_V_tr9))))  # noqa: E501,E226
    EQ_alg257 = (e0_V_tot_tr9-((e0_V_L_tr9+e0_V_V_tr9)))  # noqa: E501,E226
    EQ_alg258 = (e0_V_L_tr9-((e0_HU_L_tr9*e0_v_L_tr9)))  # noqa: E501,E226
    EQ_alg259 = 1e-2 * ((e0_p_tr9*(((10.0))**(1.0*5.0)*e0_V_V_tr9))-((e0_HU_V_tr9*(e0_R*e0_T_tr9))))  # noqa: E501,E226
    EQ_alg260 = (0.0-((e0_x_V_tr9_c1-(e0_K_tr9_c1*e0_x_L_tr9_c1))))  # noqa: E501,E226
    EQ_alg261 = (0.0-((e0_x_V_tr9_c2-(e0_K_tr9_c2*e0_x_L_tr9_c2))))  # noqa: E501,E226
    EQ_alg262 = (e0_p_LV_o_tr9_c1-(((10.0))**(1.0*(e0_A_c1-(e0_B_c1/(e0_T_tr9+e0_C_c1))))))  # noqa: E501,E226
    EQ_alg263 = (e0_p_LV_o_tr9_c2-(((10.0))**(1.0*(e0_A_c2-(e0_B_c2/(e0_T_tr9+e0_C_c2))))))  # noqa: E501,E226
    EQ_alg264 = (e0_h_feed_tr9-((((e0_x_feed_tr9_c1*e0_h_feed_tr9_c1)+(e0_x_feed_tr9_c2*e0_h_feed_tr9_c2)))))  # noqa: E501,E226
    EQ_alg265 = (e0_h_L_tr9-((((e0_x_L_tr9_c1*e0_h_L_tr9_c1)+(e0_x_L_tr9_c2*e0_h_L_tr9_c2)))))  # noqa: E501,E226
    EQ_alg266 = (e0_h_V_tr9-((((e0_x_V_tr9_c1*e0_h_V_tr9_c1)+(e0_x_V_tr9_c2*e0_h_V_tr9_c2)))))  # noqa: E501,E226
    EQ_alg267 = (((e0_p_tr9-e0_p_tr8))-(((e0_greek_kappa*((e0_F_V_tr9))**(1.0*2.0))+e0_greek_kappa_hyst)))  # noqa: E501,E226
    EQ_alg268 = ((e0_p_tr9*e0_K_tr9_c1)-((e0_p_LV_o_tr9_c1*(((e0_greek_lambda_activity*e0_greek_gamma_tr9_c1)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
    EQ_alg269 = ((e0_p_tr9*e0_K_tr9_c2)-((e0_p_LV_o_tr9_c2*(((e0_greek_lambda_activity*e0_greek_gamma_tr9_c2)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
    EQ_alg270 = (e0_v_L_tr9-((((e0_x_L_tr9_c1*e0_v_L_c1)+(e0_x_L_tr9_c2*e0_v_L_c2)))))  # noqa: E501,E226
    EQ_alg271 = (e0_greek_alpha_tr9_c1-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c1)/e0_v_L_c1)*ca.exp(((-e0_greek_lambda_c1)/e0_T_tr9)))))  # noqa: E501,E226
    EQ_alg272 = (e0_greek_alpha_tr9_c2-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c2)/e0_v_L_c2)*ca.exp(((-e0_greek_lambda_c2)/e0_T_tr9)))))  # noqa: E501,E226
    EQ_alg273 = (e0_greek_gamma_tr9_c1-(((1.0/(e0_x_L_tr9_c1+(e0_greek_alpha_tr9_c1*((1.0-e0_x_L_tr9_c1)))))*ca.exp((((1.0-e0_x_L_tr9_c1))*(((e0_greek_alpha_tr9_c1/(e0_x_L_tr9_c1+(e0_greek_alpha_tr9_c1*((1.0-e0_x_L_tr9_c1)))))-((((e0_greek_alpha_tr9_c1+e0_greek_alpha_tr9_c2))-e0_greek_alpha_tr9_c1)/((((((e0_greek_alpha_tr9_c1+e0_greek_alpha_tr9_c2))-e0_greek_alpha_tr9_c1))*e0_x_L_tr9_c1)+((1.0-e0_x_L_tr9_c1)))))))))))  # noqa: E501,E226
    EQ_alg274 = (e0_greek_gamma_tr9_c2-(((1.0/(e0_x_L_tr9_c2+(e0_greek_alpha_tr9_c2*((1.0-e0_x_L_tr9_c2)))))*ca.exp((((1.0-e0_x_L_tr9_c2))*(((e0_greek_alpha_tr9_c2/(e0_x_L_tr9_c2+(e0_greek_alpha_tr9_c2*((1.0-e0_x_L_tr9_c2)))))-((((e0_greek_alpha_tr9_c1+e0_greek_alpha_tr9_c2))-e0_greek_alpha_tr9_c2)/((((((e0_greek_alpha_tr9_c1+e0_greek_alpha_tr9_c2))-e0_greek_alpha_tr9_c2))*e0_x_L_tr9_c2)+((1.0-e0_x_L_tr9_c2)))))))))))  # noqa: E501,E226
    EQ_alg275 = (e0_M_D_c1-((e0_HU_D_c1*e0_M_c1)))  # noqa: E501,E226
    EQ_alg276 = (e0_M_D_c2-((e0_HU_D_c2*e0_M_c2)))  # noqa: E501,E226
    EQ_alg277 = (e0_M_D-(((e0_M_D_c1+e0_M_D_c2))))  # noqa: E501,E226
    EQ_alg278 = ((e0_LI*e0_V_tot_tr9)-((e0_V_L_tr9*100.0)))  # noqa: E501,E226
    EQ_alg279 = (e0_PDI-((((e0_p_tr9-e0_p_tr0))*1000.0)))  # noqa: E501,E226
    EQ_alg280 = (e0_PI_C-((e0_p_tr0*1000.0)))  # noqa: E501,E226
    EQ_alg281 = (e0_PI_B-((e0_p_tr9*1000.0)))  # noqa: E501,E226
    EQ_alg282 = ((e0_w_L_C_c1*(((e0_x_L_tr0_c1*e0_M_c1)+(e0_x_L_tr0_c2*e0_M_c2))))-((e0_x_L_tr0_c1*e0_M_c1)))  # noqa: E501,E226
    EQ_alg283 = ((e0_w_L_C_c2*(((e0_x_L_tr0_c1*e0_M_c1)+(e0_x_L_tr0_c2*e0_M_c2))))-((e0_x_L_tr0_c2*e0_M_c2)))  # noqa: E501,E226
    EQ_alg284 = ((e0_w_L_D_c1*e0_M_D)-(e0_M_D_c1))  # noqa: E501,E226
    EQ_alg285 = ((e0_w_L_D_c2*e0_M_D)-(e0_M_D_c2))  # noqa: E501,E226
    EQ_alg286 = ((e0_w_L_B_c1*(((e0_x_L_tr9_c1*e0_M_c1)+(e0_x_L_tr9_c2*e0_M_c2))))-((e0_x_L_tr9_c1*e0_M_c1)))  # noqa: E501,E226
    EQ_alg287 = ((e0_w_L_B_c2*(((e0_x_L_tr9_c1*e0_M_c1)+(e0_x_L_tr9_c2*e0_M_c2))))-((e0_x_L_tr9_c2*e0_M_c2)))  # noqa: E501,E226
    EQ_alg288 = (e0_WI-((e0_M_D*1000.0)))  # noqa: E501,E226
    EQ_alg289 = (e0_Q_R-((e0_Q_PLS_R+e0_Q_err_R)))  # noqa: E501,E226
    EQ_alg290 = (e0_rr-((e0_rr_PLS+e0_rr_err)))  # noqa: E501,E226

    order_state_var = ["e0_HU_tr1_c1", "e0_HU_tr2_c1", "e0_HU_tr3_c1", "e0_HU_tr4_c1", "e0_HU_tr5_c1", "e0_HU_tr6_c1", "e0_HU_tr7_c1", "e0_HU_tr8_c1", "e0_HU_tr1_c2", "e0_HU_tr2_c2", "e0_HU_tr3_c2", "e0_HU_tr4_c2", "e0_HU_tr5_c2", "e0_HU_tr6_c2", "e0_HU_tr7_c2", "e0_HU_tr8_c2", "e0_U_tr1", "e0_U_tr2", "e0_U_tr3", "e0_U_tr4", "e0_U_tr5", "e0_U_tr6", "e0_U_tr7", "e0_U_tr8", "e0_HU_tr9_c1", "e0_HU_tr9_c2", "e0_U_tr9", "e0_HU_D_c1", "e0_HU_D_c2", ]  # noqa: E501
    order_eqs_diff = {"e0_HU_tr1_c1": EQ_diff1, "e0_HU_tr2_c1": EQ_diff2, "e0_HU_tr3_c1": EQ_diff3, "e0_HU_tr4_c1": EQ_diff4, "e0_HU_tr5_c1": EQ_diff5, "e0_HU_tr6_c1": EQ_diff6, "e0_HU_tr7_c1": EQ_diff7, "e0_HU_tr8_c1": EQ_diff8, "e0_HU_tr1_c2": EQ_diff9, "e0_HU_tr2_c2": EQ_diff10, "e0_HU_tr3_c2": EQ_diff11, "e0_HU_tr4_c2": EQ_diff12, "e0_HU_tr5_c2": EQ_diff13, "e0_HU_tr6_c2": EQ_diff14, "e0_HU_tr7_c2": EQ_diff15, "e0_HU_tr8_c2": EQ_diff16, "e0_U_tr1": EQ_diff17, "e0_U_tr2": EQ_diff18, "e0_U_tr3": EQ_diff19, "e0_U_tr4": EQ_diff20, "e0_U_tr5": EQ_diff21, "e0_U_tr6": EQ_diff22, "e0_U_tr7": EQ_diff23, "e0_U_tr8": EQ_diff24, "e0_HU_tr9_c1": EQ_diff25, "e0_HU_tr9_c2": EQ_diff26, "e0_U_tr9": EQ_diff27, "e0_HU_D_c1": EQ_diff28, "e0_HU_D_c2": EQ_diff29, }  # noqa: E501

    for state_var_name in order_state_var:
        model.set_rhs(state_var_name, order_eqs_diff[state_var_name])

    dict_algebraic_equations = {"EQ_alg30": EQ_alg30,"EQ_alg31": EQ_alg31,"EQ_alg32": EQ_alg32,"EQ_alg33": EQ_alg33,"EQ_alg34": EQ_alg34,"EQ_alg35": EQ_alg35,"EQ_alg36": EQ_alg36,"EQ_alg37": EQ_alg37,"EQ_alg38": EQ_alg38,"EQ_alg39": EQ_alg39,"EQ_alg40": EQ_alg40,"EQ_alg41": EQ_alg41,"EQ_alg42": EQ_alg42,"EQ_alg43": EQ_alg43,"EQ_alg44": EQ_alg44,"EQ_alg45": EQ_alg45,"EQ_alg46": EQ_alg46,"EQ_alg47": EQ_alg47,"EQ_alg48": EQ_alg48,"EQ_alg49": EQ_alg49,"EQ_alg50": EQ_alg50,"EQ_alg51": EQ_alg51,"EQ_alg52": EQ_alg52,"EQ_alg53": EQ_alg53,"EQ_alg54": EQ_alg54,"EQ_alg55": EQ_alg55,"EQ_alg56": EQ_alg56,"EQ_alg57": EQ_alg57,"EQ_alg58": EQ_alg58,"EQ_alg59": EQ_alg59,"EQ_alg60": EQ_alg60,"EQ_alg61": EQ_alg61,"EQ_alg62": EQ_alg62,"EQ_alg63": EQ_alg63,"EQ_alg64": EQ_alg64,"EQ_alg65": EQ_alg65,"EQ_alg66": EQ_alg66,"EQ_alg67": EQ_alg67,"EQ_alg68": EQ_alg68,"EQ_alg69": EQ_alg69,"EQ_alg70": EQ_alg70,"EQ_alg71": EQ_alg71,"EQ_alg72": EQ_alg72,"EQ_alg73": EQ_alg73,"EQ_alg74": EQ_alg74,"EQ_alg75": EQ_alg75,"EQ_alg76": EQ_alg76,"EQ_alg77": EQ_alg77,"EQ_alg78": EQ_alg78,"EQ_alg79": EQ_alg79,"EQ_alg80": EQ_alg80,"EQ_alg81": EQ_alg81,"EQ_alg82": EQ_alg82,"EQ_alg83": EQ_alg83,"EQ_alg84": EQ_alg84,"EQ_alg85": EQ_alg85,"EQ_alg86": EQ_alg86,"EQ_alg87": EQ_alg87,"EQ_alg88": EQ_alg88,"EQ_alg89": EQ_alg89,"EQ_alg90": EQ_alg90,"EQ_alg91": EQ_alg91,"EQ_alg92": EQ_alg92,"EQ_alg93": EQ_alg93,"EQ_alg94": EQ_alg94,"EQ_alg95": EQ_alg95,"EQ_alg96": EQ_alg96,"EQ_alg97": EQ_alg97,"EQ_alg98": EQ_alg98,"EQ_alg99": EQ_alg99,"EQ_alg100": EQ_alg100,"EQ_alg101": EQ_alg101,"EQ_alg102": EQ_alg102,"EQ_alg103": EQ_alg103,"EQ_alg104": EQ_alg104,"EQ_alg105": EQ_alg105,"EQ_alg106": EQ_alg106,"EQ_alg107": EQ_alg107,"EQ_alg108": EQ_alg108,"EQ_alg109": EQ_alg109,"EQ_alg110": EQ_alg110,"EQ_alg111": EQ_alg111,"EQ_alg112": EQ_alg112,"EQ_alg113": EQ_alg113,"EQ_alg114": EQ_alg114,"EQ_alg115": EQ_alg115,"EQ_alg116": EQ_alg116,"EQ_alg117": EQ_alg117,"EQ_alg118": EQ_alg118,"EQ_alg119": EQ_alg119,"EQ_alg120": EQ_alg120,"EQ_alg121": EQ_alg121,"EQ_alg122": EQ_alg122,"EQ_alg123": EQ_alg123,"EQ_alg124": EQ_alg124,"EQ_alg125": EQ_alg125,"EQ_alg126": EQ_alg126,"EQ_alg127": EQ_alg127,"EQ_alg128": EQ_alg128,"EQ_alg129": EQ_alg129,"EQ_alg130": EQ_alg130,"EQ_alg131": EQ_alg131,"EQ_alg132": EQ_alg132,"EQ_alg133": EQ_alg133,"EQ_alg134": EQ_alg134,"EQ_alg135": EQ_alg135,"EQ_alg136": EQ_alg136,"EQ_alg137": EQ_alg137,"EQ_alg138": EQ_alg138,"EQ_alg139": EQ_alg139,"EQ_alg140": EQ_alg140,"EQ_alg141": EQ_alg141,"EQ_alg142": EQ_alg142,"EQ_alg143": EQ_alg143,"EQ_alg144": EQ_alg144,"EQ_alg145": EQ_alg145,"EQ_alg146": EQ_alg146,"EQ_alg147": EQ_alg147,"EQ_alg148": EQ_alg148,"EQ_alg149": EQ_alg149,"EQ_alg150": EQ_alg150,"EQ_alg151": EQ_alg151,"EQ_alg152": EQ_alg152,"EQ_alg153": EQ_alg153,"EQ_alg154": EQ_alg154,"EQ_alg155": EQ_alg155,"EQ_alg156": EQ_alg156,"EQ_alg157": EQ_alg157,"EQ_alg158": EQ_alg158,"EQ_alg159": EQ_alg159,"EQ_alg160": EQ_alg160,"EQ_alg161": EQ_alg161,"EQ_alg162": EQ_alg162,"EQ_alg163": EQ_alg163,"EQ_alg164": EQ_alg164,"EQ_alg165": EQ_alg165,"EQ_alg166": EQ_alg166,"EQ_alg167": EQ_alg167,"EQ_alg168": EQ_alg168,"EQ_alg169": EQ_alg169,"EQ_alg170": EQ_alg170,"EQ_alg171": EQ_alg171,"EQ_alg172": EQ_alg172,"EQ_alg173": EQ_alg173,"EQ_alg174": EQ_alg174,"EQ_alg175": EQ_alg175,"EQ_alg176": EQ_alg176,"EQ_alg177": EQ_alg177,"EQ_alg178": EQ_alg178,"EQ_alg179": EQ_alg179,"EQ_alg180": EQ_alg180,"EQ_alg181": EQ_alg181,"EQ_alg182": EQ_alg182,"EQ_alg183": EQ_alg183,"EQ_alg184": EQ_alg184,"EQ_alg185": EQ_alg185,"EQ_alg186": EQ_alg186,"EQ_alg187": EQ_alg187,"EQ_alg188": EQ_alg188,"EQ_alg189": EQ_alg189,"EQ_alg190": EQ_alg190,"EQ_alg191": EQ_alg191,"EQ_alg192": EQ_alg192,"EQ_alg193": EQ_alg193,"EQ_alg194": EQ_alg194,"EQ_alg195": EQ_alg195,"EQ_alg196": EQ_alg196,"EQ_alg197": EQ_alg197,"EQ_alg198": EQ_alg198,"EQ_alg199": EQ_alg199,"EQ_alg200": EQ_alg200,"EQ_alg201": EQ_alg201,"EQ_alg202": EQ_alg202,"EQ_alg203": EQ_alg203,"EQ_alg204": EQ_alg204,"EQ_alg205": EQ_alg205,"EQ_alg206": EQ_alg206,"EQ_alg207": EQ_alg207,"EQ_alg208": EQ_alg208,"EQ_alg209": EQ_alg209,"EQ_alg210": EQ_alg210,"EQ_alg211": EQ_alg211,"EQ_alg212": EQ_alg212,"EQ_alg213": EQ_alg213,"EQ_alg214": EQ_alg214,"EQ_alg215": EQ_alg215,"EQ_alg216": EQ_alg216,"EQ_alg217": EQ_alg217,"EQ_alg218": EQ_alg218,"EQ_alg219": EQ_alg219,"EQ_alg220": EQ_alg220,"EQ_alg221": EQ_alg221,"EQ_alg222": EQ_alg222,"EQ_alg223": EQ_alg223,"EQ_alg224": EQ_alg224,"EQ_alg225": EQ_alg225,"EQ_alg226": EQ_alg226,"EQ_alg227": EQ_alg227,"EQ_alg228": EQ_alg228,"EQ_alg229": EQ_alg229,"EQ_alg230": EQ_alg230,"EQ_alg231": EQ_alg231,"EQ_alg232": EQ_alg232,"EQ_alg233": EQ_alg233,"EQ_alg234": EQ_alg234,"EQ_alg235": EQ_alg235,"EQ_alg236": EQ_alg236,"EQ_alg237": EQ_alg237,"EQ_alg238": EQ_alg238,"EQ_alg239": EQ_alg239,"EQ_alg240": EQ_alg240,"EQ_alg241": EQ_alg241,"EQ_alg242": EQ_alg242,"EQ_alg243": EQ_alg243,"EQ_alg244": EQ_alg244,"EQ_alg245": EQ_alg245,"EQ_alg246": EQ_alg246,"EQ_alg247": EQ_alg247,"EQ_alg248": EQ_alg248,"EQ_alg249": EQ_alg249,"EQ_alg250": EQ_alg250,"EQ_alg251": EQ_alg251,"EQ_alg252": EQ_alg252,"EQ_alg253": EQ_alg253,"EQ_alg254": EQ_alg254,"EQ_alg255": EQ_alg255,"EQ_alg256": EQ_alg256,"EQ_alg257": EQ_alg257,"EQ_alg258": EQ_alg258,"EQ_alg259": EQ_alg259,"EQ_alg260": EQ_alg260,"EQ_alg261": EQ_alg261,"EQ_alg262": EQ_alg262,"EQ_alg263": EQ_alg263,"EQ_alg264": EQ_alg264,"EQ_alg265": EQ_alg265,"EQ_alg266": EQ_alg266,"EQ_alg267": EQ_alg267,"EQ_alg268": EQ_alg268,"EQ_alg269": EQ_alg269,"EQ_alg270": EQ_alg270,"EQ_alg271": EQ_alg271,"EQ_alg272": EQ_alg272,"EQ_alg273": EQ_alg273,"EQ_alg274": EQ_alg274,"EQ_alg275": EQ_alg275,"EQ_alg276": EQ_alg276,"EQ_alg277": EQ_alg277,"EQ_alg278": EQ_alg278,"EQ_alg279": EQ_alg279,"EQ_alg280": EQ_alg280,"EQ_alg281": EQ_alg281,"EQ_alg282": EQ_alg282,"EQ_alg283": EQ_alg283,"EQ_alg284": EQ_alg284,"EQ_alg285": EQ_alg285,"EQ_alg286": EQ_alg286,"EQ_alg287": EQ_alg287,"EQ_alg288": EQ_alg288,"EQ_alg289": EQ_alg289,"EQ_alg290": EQ_alg290,}  # noqa: E501
    try:
        Eq_fun_e0_h_L_tr1_c1 = e0_h_L_tr1_c1 - fun_213932__liquid_enthalpy_adj(e0_T_tr1,e0_greek_Deltah_f_c1,e0_A_LV_c1,e0_B_LV_c1,e0_C_LV_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_L_tr1_c1"] = Eq_fun_e0_h_L_tr1_c1  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_L_tr0_c2 = e0_h_L_tr0_c2 - fun_213932__liquid_enthalpy_adj(e0_T_tr0,e0_greek_Deltah_f_c2,e0_A_LV_c2,e0_B_LV_c2,e0_C_LV_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_L_tr0_c2"] = Eq_fun_e0_h_L_tr0_c2  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_L_tr6_c1 = e0_h_L_tr6_c1 - fun_213932__liquid_enthalpy_adj(e0_T_tr6,e0_greek_Deltah_f_c1,e0_A_LV_c1,e0_B_LV_c1,e0_C_LV_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_L_tr6_c1"] = Eq_fun_e0_h_L_tr6_c1  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_V_tr9_c1 = e0_h_V_tr9_c1 - fun_210593__vaporenthalpy(e0_T_tr9,e0_greek_Deltah_f_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_V_tr9_c1"] = Eq_fun_e0_h_V_tr9_c1  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_V_tr2_c1 = e0_h_V_tr2_c1 - fun_210593__vaporenthalpy(e0_T_tr2,e0_greek_Deltah_f_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_V_tr2_c1"] = Eq_fun_e0_h_V_tr2_c1  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_V_tr4_c1 = e0_h_V_tr4_c1 - fun_210593__vaporenthalpy(e0_T_tr4,e0_greek_Deltah_f_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_V_tr4_c1"] = Eq_fun_e0_h_V_tr4_c1  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_V_tr8_c2 = e0_h_V_tr8_c2 - fun_210593__vaporenthalpy(e0_T_tr8,e0_greek_Deltah_f_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_V_tr8_c2"] = Eq_fun_e0_h_V_tr8_c2  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_V_tr4_c2 = e0_h_V_tr4_c2 - fun_210593__vaporenthalpy(e0_T_tr4,e0_greek_Deltah_f_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_V_tr4_c2"] = Eq_fun_e0_h_V_tr4_c2  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_V_tr7_c2 = e0_h_V_tr7_c2 - fun_210593__vaporenthalpy(e0_T_tr7,e0_greek_Deltah_f_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_V_tr7_c2"] = Eq_fun_e0_h_V_tr7_c2  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_L_tr0_c1 = e0_h_L_tr0_c1 - fun_213932__liquid_enthalpy_adj(e0_T_tr0,e0_greek_Deltah_f_c1,e0_A_LV_c1,e0_B_LV_c1,e0_C_LV_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_L_tr0_c1"] = Eq_fun_e0_h_L_tr0_c1  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_V_tr1_c1 = e0_h_V_tr1_c1 - fun_210593__vaporenthalpy(e0_T_tr1,e0_greek_Deltah_f_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_V_tr1_c1"] = Eq_fun_e0_h_V_tr1_c1  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_V_tr3_c2 = e0_h_V_tr3_c2 - fun_210593__vaporenthalpy(e0_T_tr3,e0_greek_Deltah_f_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_V_tr3_c2"] = Eq_fun_e0_h_V_tr3_c2  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_L_tr2_c1 = e0_h_L_tr2_c1 - fun_213932__liquid_enthalpy_adj(e0_T_tr2,e0_greek_Deltah_f_c1,e0_A_LV_c1,e0_B_LV_c1,e0_C_LV_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_L_tr2_c1"] = Eq_fun_e0_h_L_tr2_c1  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_V_tr3_c1 = e0_h_V_tr3_c1 - fun_210593__vaporenthalpy(e0_T_tr3,e0_greek_Deltah_f_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_V_tr3_c1"] = Eq_fun_e0_h_V_tr3_c1  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_L_tr5_c1 = e0_h_L_tr5_c1 - fun_213932__liquid_enthalpy_adj(e0_T_tr5,e0_greek_Deltah_f_c1,e0_A_LV_c1,e0_B_LV_c1,e0_C_LV_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_L_tr5_c1"] = Eq_fun_e0_h_L_tr5_c1  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_L_tr9_c1 = e0_h_L_tr9_c1 - fun_213932__liquid_enthalpy_adj(e0_T_tr9,e0_greek_Deltah_f_c1,e0_A_LV_c1,e0_B_LV_c1,e0_C_LV_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_L_tr9_c1"] = Eq_fun_e0_h_L_tr9_c1  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_L_tr1_c2 = e0_h_L_tr1_c2 - fun_213932__liquid_enthalpy_adj(e0_T_tr1,e0_greek_Deltah_f_c2,e0_A_LV_c2,e0_B_LV_c2,e0_C_LV_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_L_tr1_c2"] = Eq_fun_e0_h_L_tr1_c2  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_V_tr5_c1 = e0_h_V_tr5_c1 - fun_210593__vaporenthalpy(e0_T_tr5,e0_greek_Deltah_f_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_V_tr5_c1"] = Eq_fun_e0_h_V_tr5_c1  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_L_tr6_c2 = e0_h_L_tr6_c2 - fun_213932__liquid_enthalpy_adj(e0_T_tr6,e0_greek_Deltah_f_c2,e0_A_LV_c2,e0_B_LV_c2,e0_C_LV_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_L_tr6_c2"] = Eq_fun_e0_h_L_tr6_c2  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_V_tr7_c1 = e0_h_V_tr7_c1 - fun_210593__vaporenthalpy(e0_T_tr7,e0_greek_Deltah_f_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_V_tr7_c1"] = Eq_fun_e0_h_V_tr7_c1  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_L_tr3_c2 = e0_h_L_tr3_c2 - fun_213932__liquid_enthalpy_adj(e0_T_tr3,e0_greek_Deltah_f_c2,e0_A_LV_c2,e0_B_LV_c2,e0_C_LV_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_L_tr3_c2"] = Eq_fun_e0_h_L_tr3_c2  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_L_tr5_c2 = e0_h_L_tr5_c2 - fun_213932__liquid_enthalpy_adj(e0_T_tr5,e0_greek_Deltah_f_c2,e0_A_LV_c2,e0_B_LV_c2,e0_C_LV_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_L_tr5_c2"] = Eq_fun_e0_h_L_tr5_c2  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_feed_tr9_c2 = e0_h_feed_tr9_c2 - fun_213932__liquid_enthalpy_adj(e0_T_feed,e0_greek_Deltah_f_c2,e0_A_LV_c2,e0_B_LV_c2,e0_C_LV_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_feed_tr9_c2"] = Eq_fun_e0_h_feed_tr9_c2  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_L_tr2_c2 = e0_h_L_tr2_c2 - fun_213932__liquid_enthalpy_adj(e0_T_tr2,e0_greek_Deltah_f_c2,e0_A_LV_c2,e0_B_LV_c2,e0_C_LV_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_L_tr2_c2"] = Eq_fun_e0_h_L_tr2_c2  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_L_tr4_c2 = e0_h_L_tr4_c2 - fun_213932__liquid_enthalpy_adj(e0_T_tr4,e0_greek_Deltah_f_c2,e0_A_LV_c2,e0_B_LV_c2,e0_C_LV_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_L_tr4_c2"] = Eq_fun_e0_h_L_tr4_c2  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_L_tr7_c1 = e0_h_L_tr7_c1 - fun_213932__liquid_enthalpy_adj(e0_T_tr7,e0_greek_Deltah_f_c1,e0_A_LV_c1,e0_B_LV_c1,e0_C_LV_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_L_tr7_c1"] = Eq_fun_e0_h_L_tr7_c1  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_L_tr8_c1 = e0_h_L_tr8_c1 - fun_213932__liquid_enthalpy_adj(e0_T_tr8,e0_greek_Deltah_f_c1,e0_A_LV_c1,e0_B_LV_c1,e0_C_LV_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_L_tr8_c1"] = Eq_fun_e0_h_L_tr8_c1  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_V_tr6_c2 = e0_h_V_tr6_c2 - fun_210593__vaporenthalpy(e0_T_tr6,e0_greek_Deltah_f_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_V_tr6_c2"] = Eq_fun_e0_h_V_tr6_c2  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_L_tr8_c2 = e0_h_L_tr8_c2 - fun_213932__liquid_enthalpy_adj(e0_T_tr8,e0_greek_Deltah_f_c2,e0_A_LV_c2,e0_B_LV_c2,e0_C_LV_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_L_tr8_c2"] = Eq_fun_e0_h_L_tr8_c2  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_L_tr4_c1 = e0_h_L_tr4_c1 - fun_213932__liquid_enthalpy_adj(e0_T_tr4,e0_greek_Deltah_f_c1,e0_A_LV_c1,e0_B_LV_c1,e0_C_LV_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_L_tr4_c1"] = Eq_fun_e0_h_L_tr4_c1  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_V_tr2_c2 = e0_h_V_tr2_c2 - fun_210593__vaporenthalpy(e0_T_tr2,e0_greek_Deltah_f_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_V_tr2_c2"] = Eq_fun_e0_h_V_tr2_c2  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_feed_tr9_c1 = e0_h_feed_tr9_c1 - fun_213932__liquid_enthalpy_adj(e0_T_feed,e0_greek_Deltah_f_c1,e0_A_LV_c1,e0_B_LV_c1,e0_C_LV_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_feed_tr9_c1"] = Eq_fun_e0_h_feed_tr9_c1  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_V_tr5_c2 = e0_h_V_tr5_c2 - fun_210593__vaporenthalpy(e0_T_tr5,e0_greek_Deltah_f_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_V_tr5_c2"] = Eq_fun_e0_h_V_tr5_c2  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_V_tr6_c1 = e0_h_V_tr6_c1 - fun_210593__vaporenthalpy(e0_T_tr6,e0_greek_Deltah_f_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_V_tr6_c1"] = Eq_fun_e0_h_V_tr6_c1  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_V_tr8_c1 = e0_h_V_tr8_c1 - fun_210593__vaporenthalpy(e0_T_tr8,e0_greek_Deltah_f_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_V_tr8_c1"] = Eq_fun_e0_h_V_tr8_c1  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_V_tr9_c2 = e0_h_V_tr9_c2 - fun_210593__vaporenthalpy(e0_T_tr9,e0_greek_Deltah_f_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_V_tr9_c2"] = Eq_fun_e0_h_V_tr9_c2  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_L_tr3_c1 = e0_h_L_tr3_c1 - fun_213932__liquid_enthalpy_adj(e0_T_tr3,e0_greek_Deltah_f_c1,e0_A_LV_c1,e0_B_LV_c1,e0_C_LV_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_L_tr3_c1"] = Eq_fun_e0_h_L_tr3_c1  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_L_tr9_c2 = e0_h_L_tr9_c2 - fun_213932__liquid_enthalpy_adj(e0_T_tr9,e0_greek_Deltah_f_c2,e0_A_LV_c2,e0_B_LV_c2,e0_C_LV_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_L_tr9_c2"] = Eq_fun_e0_h_L_tr9_c2  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_L_tr7_c2 = e0_h_L_tr7_c2 - fun_213932__liquid_enthalpy_adj(e0_T_tr7,e0_greek_Deltah_f_c2,e0_A_LV_c2,e0_B_LV_c2,e0_C_LV_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_L_tr7_c2"] = Eq_fun_e0_h_L_tr7_c2  # noqa: E501
    except KeyError:
        pass
    try:
        Eq_fun_e0_h_V_tr1_c2 = e0_h_V_tr1_c2 - fun_210593__vaporenthalpy(e0_T_tr1,e0_greek_Deltah_f_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
        dict_algebraic_equations["Eq_fun_e0_h_V_tr1_c2"] = Eq_fun_e0_h_V_tr1_c2  # noqa: E501
    except KeyError:
        pass

    # fmt:on

    for alg_var_name, alg_eq in dict_algebraic_equations.items():
        model.set_alg(alg_var_name, alg_eq)

    # Build the model
    model.setup()

    return model


def template_simulator(model: do_mpc.model.Model) -> do_mpc.simulator.Simulator:
    """
    Here could be the doc
    """
    simulator = do_mpc.simulator.Simulator(model)

    # tvp_num = simulator.get_tvp_template()
    # def tvp_fun(t_now):
    #     return tvp_num
    # simulator.set_tvp_fun(tvp_fun)

    # fmt:off
    # Parameters
    p_template = simulator.get_p_template()
    p_template["e0_greek_kappa_hyst"] = 0.0

    p_template["e0_p_tr0"] = 1.028
    p_template["e0_T_feed"] = 369.0
    p_template["e0_V_tot_tr9"] = 0.06
    p_template["e0_greek_lambda_activity"] = 1.0

    # p_template["e0_Q_err_R"] = 0.98647356893109
    p_template["e0_Q_err_R"] = -0

    # NOTE: e0_F_feed_tr9, e0_F_B, e0_x_feed_tr9_c1, e0_x_feed_tr9_c2,
    # e0_rr_err and e0_E_murphree are now control inputs (_u). Their
    # default values are set on simulator.u0 below and will be overwritten
    # by whatever trajectory is passed to ``simulator.make_step(...)``.

    simulator.set_p_fun(lambda t_now: p_template)

    # Initial conditions (x0)
    simulator.x0["e0_HU_tr1_c1"] = 1.1362999244585050e+00
    simulator.x0["e0_HU_tr2_c1"] = 1.1252709483857797e+00
    simulator.x0["e0_HU_tr3_c1"] = 1.1108408860487660e+00
    simulator.x0["e0_HU_tr4_c1"] = 1.0913641540464472e+00
    simulator.x0["e0_HU_tr5_c1"] = 1.0640161712667540e+00
    simulator.x0["e0_HU_tr6_c1"] = 1.0235983793037953e+00
    simulator.x0["e0_HU_tr7_c1"] = 9.5968637336650575e-01
    simulator.x0["e0_HU_tr8_c1"] = 8.4912365725964278e-01
    simulator.x0["e0_HU_tr9_c1"] = 1.3766987944853224e+02

    simulator.x0["e0_HU_tr1_c2"] = 3.4296563376484207e-01
    simulator.x0["e0_HU_tr2_c2"] = 3.7631053409642373e-01
    simulator.x0["e0_HU_tr3_c2"] = 4.2002729693882218e-01
    simulator.x0["e0_HU_tr4_c2"] = 4.7918764113028522e-01
    simulator.x0["e0_HU_tr5_c2"] = 5.6253834942384440e-01
    simulator.x0["e0_HU_tr6_c2"] = 6.8627101036983595e-01
    simulator.x0["e0_HU_tr7_c2"] = 8.8308401102521428e-01
    simulator.x0["e0_HU_tr8_c2"] = 1.2255852815105432e+00
    simulator.x0["e0_HU_tr9_c2"] = 1.4043319579677097e+03

    simulator.x0["e0_U_tr1"] = -4.0198709467893099e+02
    simulator.x0["e0_U_tr2"] = -4.0836630630917102e+02
    simulator.x0["e0_U_tr3"] = -4.1673697240841551e+02
    simulator.x0["e0_U_tr4"] = -4.2807695226701838e+02
    simulator.x0["e0_U_tr5"] = -4.4407606109049510e+02
    simulator.x0["e0_U_tr6"] = -4.6787015499520584e+02
    simulator.x0["e0_U_tr7"] = -5.0581103748194334e+02
    simulator.x0["e0_U_tr8"] = -5.7199520623273929e+02
    simulator.x0["e0_U_tr9"] = -4.3014163837181707e+05

    # The idea is to be not fully empty because otherwise the numerics are difficult.
    # We assume m_EtOH + m_W = 1.0 g and an initial mass fraction of 0.95 g EtOH per g total liquid.
    simulator.x0["e0_HU_D_c1"] = 0.95 * 1e-3 / 0.046
    simulator.x0["e0_HU_D_c2"] = 0.05 * 1e-3 / 0.018

    # Scaling of differential states
    simulator.scaling["_x", "e0_HU_tr1_c1"] = 1.0
    simulator.scaling["_x", "e0_HU_tr2_c1"] = 1.0
    simulator.scaling["_x", "e0_HU_tr3_c1"] = 1.0
    simulator.scaling["_x", "e0_HU_tr4_c1"] = 1.0
    simulator.scaling["_x", "e0_HU_tr5_c1"] = 1.0
    simulator.scaling["_x", "e0_HU_tr6_c1"] = 1.0
    simulator.scaling["_x", "e0_HU_tr7_c1"] = 1.0
    simulator.scaling["_x", "e0_HU_tr8_c1"] = 1.0
    simulator.scaling["_x", "e0_HU_tr9_c1"] = 100.0

    simulator.scaling["_x", "e0_HU_tr1_c2"] = 1.0
    simulator.scaling["_x", "e0_HU_tr2_c2"] = 1.0
    simulator.scaling["_x", "e0_HU_tr3_c2"] = 1.0
    simulator.scaling["_x", "e0_HU_tr4_c2"] = 1.0
    simulator.scaling["_x", "e0_HU_tr5_c2"] = 1.0
    simulator.scaling["_x", "e0_HU_tr6_c2"] = 1.0
    simulator.scaling["_x", "e0_HU_tr7_c2"] = 1.0
    simulator.scaling["_x", "e0_HU_tr8_c2"] = 1.0
    simulator.scaling["_x", "e0_HU_tr9_c2"] = 1000.0

    simulator.scaling["_x", "e0_U_tr1"] = 100.0
    simulator.scaling["_x", "e0_U_tr2"] = 100.0
    simulator.scaling["_x", "e0_U_tr3"] = 100.0
    simulator.scaling["_x", "e0_U_tr4"] = 100.0
    simulator.scaling["_x", "e0_U_tr5"] = 100.0
    simulator.scaling["_x", "e0_U_tr6"] = 100.0
    simulator.scaling["_x", "e0_U_tr7"] = 100.0
    simulator.scaling["_x", "e0_U_tr8"] = 100.0
    simulator.scaling["_x", "e0_U_tr9"] = 100000.0

    simulator.scaling["_x", "e0_HU_D_c1"] = 10.0
    simulator.scaling["_x", "e0_HU_D_c2"] = 10.0

    # Initial condition (z0)
    # Values sourced from helper/initials_guess.txt (gSTORE snapshot).
    simulator.z0["e0_h_L_tr0_c1"] = -269.306856064154
    simulator.z0["e0_h_L_tr0_c2"] = -280.85960352775083
    simulator.z0["e0_h_L_tr1_c1"] = -269.29800287324554
    simulator.z0["e0_h_L_tr1_c2"] = -280.85474471174234
    simulator.z0["e0_h_L_tr2_c1"] = -269.28654277436306
    simulator.z0["e0_h_L_tr2_c2"] = -280.8484556882103
    simulator.z0["e0_h_L_tr3_c1"] = -269.27109279075296
    simulator.z0["e0_h_L_tr3_c2"] = -280.8399780376111
    simulator.z0["e0_h_L_tr4_c1"] = -269.24934862958764
    simulator.z0["e0_h_L_tr4_c2"] = -280.8280484694383
    simulator.z0["e0_h_L_tr5_c1"] = -269.21732078315495
    simulator.z0["e0_h_L_tr5_c2"] = -280.8104807535815
    simulator.z0["e0_h_L_tr6_c1"] = -269.1677764571861
    simulator.z0["e0_h_L_tr6_c2"] = -280.78331396463966
    simulator.z0["e0_h_L_tr7_c1"] = -269.0867386885604
    simulator.z0["e0_h_L_tr7_c2"] = -280.73890167876436
    simulator.z0["e0_h_L_tr8_c1"] = -268.94371015151273
    simulator.z0["e0_h_L_tr8_c2"] = -280.66058627128336
    simulator.z0["e0_h_L_tr9_c1"] = -267.84109229040223
    simulator.z0["e0_h_L_tr9_c2"] = -280.05981164568755
    simulator.z0["e0_h_V_tr1_c1"] = -230.0688095816222
    simulator.z0["e0_h_V_tr1_c2"] = -239.11302859917865
    simulator.z0["e0_h_V_tr2_c1"] = -230.0629904986973
    simulator.z0["e0_h_V_tr2_c2"] = -239.1102354393747
    simulator.z0["e0_h_V_tr3_c1"] = -230.05514708485848
    simulator.z0["e0_h_V_tr3_c2"] = -239.10647060073205
    simulator.z0["e0_h_V_tr4_c1"] = -230.04411146552084
    simulator.z0["e0_h_V_tr4_c2"] = -239.10117350345
    simulator.z0["e0_h_V_tr5_c1"] = -230.02786331191606
    simulator.z0["e0_h_V_tr5_c2"] = -239.0933743897197
    simulator.z0["e0_h_V_tr6_c1"] = -230.002744401111
    simulator.z0["e0_h_V_tr6_c2"] = -239.0813173125333
    simulator.z0["e0_h_V_tr7_c1"] = -229.96169906539686
    simulator.z0["e0_h_V_tr7_c2"] = -239.0616155513905
    simulator.z0["e0_h_V_tr8_c1"] = -229.88937841314586
    simulator.z0["e0_h_V_tr8_c2"] = -239.02690163831002
    simulator.z0["e0_h_V_tr9_c1"] = -229.33701177096233
    simulator.z0["e0_h_V_tr9_c2"] = -238.76176565006193
    simulator.z0["e0_h_feed_tr9_c1"] = -266.518911067034
    simulator.z0["e0_h_feed_tr9_c2"] = -279.3460703110792
    simulator.z0["e0_greek_alpha_tr0_c1"] = 0.23511555303424886
    simulator.z0["e0_greek_alpha_tr0_c2"] = 0.7626749859310874
    simulator.z0["e0_Q_C"] = -6.524991119284783
    simulator.z0["e0_H_tr3"] = -416.7006892538991
    simulator.z0["e0_H_tr4"] = -428.04064350272404
    simulator.z0["e0_H_tr5"] = -444.039726808843
    simulator.z0["e0_H_tr6"] = -467.83379531838807
    simulator.z0["e0_H_tr7"] = -505.77465257599346
    simulator.z0["e0_H_tr8"] = -571.9587963305338
    simulator.z0["e0_T_tr0"] = 350.5059246161485
    simulator.z0["e0_HU_L_tr1"] = 1.469813086796753
    simulator.z0["e0_HU_L_tr2"] = 1.4921231301920612
    simulator.z0["e0_HU_L_tr3"] = 1.5214043512501003
    simulator.z0["e0_HU_L_tr4"] = 1.5610831708145279
    simulator.z0["e0_HU_L_tr5"] = 1.6170823056731654
    simulator.z0["e0_HU_L_tr6"] = 1.7003957573449795
    simulator.z0["e0_HU_L_tr7"] = 1.833299467238853
    simulator.z0["e0_HU_L_tr8"] = 2.0652490100214025
    simulator.z0["e0_HU_V_tr1"] = 0.009874421220087701
    simulator.z0["e0_HU_V_tr2"] = 0.009880564600076958
    simulator.z0["e0_HU_V_tr3"] = 0.009886288645006605
    simulator.z0["e0_HU_V_tr4"] = 0.009891295208165745
    simulator.z0["e0_HU_V_tr5"] = 0.00989504614700263
    simulator.z0["e0_HU_V_tr6"] = 0.009896526725714996
    simulator.z0["e0_HU_V_tr7"] = 0.00989369034693403
    simulator.z0["e0_HU_V_tr8"] = 0.009882211430409387
    simulator.z0["e0_K_tr1_c1"] = 0.99489855007515
    simulator.z0["e0_K_tr2_c1"] = 1.0052619286571094
    simulator.z0["e0_h_L_tr0"] = -271.81205737018973
    simulator.z0["e0_K_tr3_c1"] = 1.020053281383547
    simulator.z0["e0_K_tr4_c1"] = 1.0420791334966997
    simulator.z0["e0_K_tr5_c1"] = 1.0766957875528014
    simulator.z0["e0_K_tr6_c1"] = 1.1351204969006057
    simulator.z0["e0_K_tr7_c1"] = 1.244050749986186
    simulator.z0["e0_K_tr8_c1"] = 1.4800610707912343
    simulator.z0["e0_K_tr1_c2"] = 0.8326612139677334
    simulator.z0["e0_K_tr2_c2"] = 0.8138450593790028
    simulator.z0["e0_K_tr3_c2"] = 0.7913446260515792
    simulator.z0["e0_K_tr4_c2"] = 0.7642783599882293
    simulator.z0["e0_h_V_tr1"] = -222.1150248484753
    simulator.z0["e0_K_tr5_c2"] = 0.7316138551561198
    simulator.z0["e0_K_tr6_c2"] = 0.6923352258535767
    simulator.z0["e0_K_tr7_c2"] = 0.6461092419523693
    simulator.z0["e0_K_tr8_c2"] = 0.5958231787389643
    simulator.z0["e0_L_tr1"] = 0.0449893189677759
    simulator.z0["e0_L_tr2"] = 0.04496618348360572
    simulator.z0["e0_L_tr3"] = 0.04493675880360852
    simulator.z0["e0_L_tr4"] = 0.0448984945811128
    simulator.z0["e0_L_tr5"] = 0.04484740833284662
    simulator.z0["e0_L_tr6"] = 0.04477707655522141
    simulator.z0["e0_L_tr7"] = 0.04467689236158418
    simulator.z0["e0_L_tr8"] = 0.044522238395394216
    simulator.z0["e0_L_weir"] = 0.034999999999999996
    simulator.z0["e0_T_tr1"] = 350.56587224503727
    simulator.z0["e0_T_tr2"] = 350.64346001736936
    simulator.z0["e0_T_tr3"] = 350.7480388685537
    simulator.z0["e0_T_tr4"] = 350.8951804597218
    simulator.z0["e0_T_tr5"] = 351.11182250778563
    simulator.z0["e0_T_tr6"] = 351.44674131852
    simulator.z0["e0_T_tr7"] = 351.994012461375
    simulator.z0["e0_p_LV_o_tr0_c1"] = 0.9758746601807994
    simulator.z0["e0_T_tr8"] = 352.95828782472194
    simulator.z0["e0_V_L_tr1"] = 7.243578216845477e-05
    simulator.z0["e0_p_LV_o_tr0_c2"] = 0.4252018366095084
    simulator.z0["e0_V_L_tr2"] = 7.23985325071982e-05
    simulator.z0["e0_V_L_tr3"] = 7.235115682426821e-05
    simulator.z0["e0_V_L_tr4"] = 7.22895488926716e-05
    simulator.z0["e0_V_L_tr5"] = 7.220729665067026e-05
    simulator.z0["e0_V_L_tr6"] = 7.20940578322025e-05
    simulator.z0["e0_V_L_tr7"] = 7.193275464750158e-05
    simulator.z0["e0_V_L_tr8"] = 7.168375152268325e-05
    simulator.z0["e0_V_V_tr1"] = 0.00027976219510451444
    simulator.z0["e0_V_V_tr2"] = 0.000279799444765771
    simulator.z0["e0_V_V_tr3"] = 0.000279846820448701
    simulator.z0["e0_V_V_tr4"] = 0.0002799084283802976
    simulator.z0["e0_V_V_tr5"] = 0.00027999068062229895
    simulator.z0["e0_V_V_tr6"] = 0.0002801039194407667
    simulator.z0["e0_V_V_tr7"] = 0.0002802652226254676
    simulator.z0["e0_V_V_tr8"] = 0.00028051422575028597
    simulator.z0["e0_V_tot"] = 0.0003521979772729692
    simulator.z0["e0_greek_gamma_tr0_c1"] = 1.040124604718417
    simulator.z0["e0_x_L_tr0_c1"] = 0.7831510371078606
    simulator.z0["e0_x_L_tr0_c2"] = 0.2168489628921393
    simulator.z0["e0_h_L_tr1"] = -271.97853197794655
    simulator.z0["e0_h_L_tr2"] = -272.1854355019705
    simulator.z0["e0_h_L_tr3"] = -272.4469719826549
    simulator.z0["e0_h_L_tr4"] = -272.7842487864244
    simulator.z0["e0_h_L_tr5"] = -273.2295296246518
    simulator.z0["e0_h_L_tr6"] = -273.8333509665667
    simulator.z0["e0_h_L_tr7"] = -274.6753031403721
    simulator.z0["e0_h_L_tr8"] = -275.8711410883291
    simulator.z0["e0_x_V_tr0_c1"] = 0.7732711793345317
    simulator.z0["e0_x_V_tr1_c1"] = 0.7496857421790125
    simulator.z0["e0_h_V_tr2"] = -222.24082438458947
    simulator.z0["e0_h_V_tr3"] = -222.39696548657437
    simulator.z0["e0_h_V_tr4"] = -222.5940498809549
    simulator.z0["e0_h_V_tr5"] = -222.84777985443122
    simulator.z0["e0_x_V_tr0_c2"] = 0.183997223127867
    simulator.z0["e0_h_V_tr6"] = -223.18204926787843
    simulator.z0["e0_h_V_tr7"] = -223.63401193008406
    simulator.z0["e0_h_V_tr8"] = -224.26106949785049
    simulator.z0["e0_h_V_tr9"] = -224.87121111065326
    simulator.z0["e0_p_tr1"] = 1.0287320669020144
    simulator.z0["e0_p_tr2"] = 1.0294628451813748
    simulator.z0["e0_p_tr3"] = 1.0301920186301785
    simulator.z0["e0_p_tr4"] = 1.0309191601671102
    simulator.z0["e0_p_tr5"] = 1.0316436776086708
    simulator.z0["e0_p_tr6"] = 1.0323647256388873
    simulator.z0["e0_x_V_tr1_c2"] = 0.20758266028338615
    simulator.z0["e0_p_tr7"] = 1.033081059454164
    simulator.z0["e0_p_tr8"] = 1.0337907811812048
    simulator.z0["e0_p_LV_o_tr1_c1"] = 0.9782059313248017
    simulator.z0["e0_p_LV_o_tr2_c1"] = 0.9812301010060752
    simulator.z0["e0_p_LV_o_tr3_c1"] = 0.9853186578750001
    simulator.z0["e0_p_LV_o_tr4_c1"] = 0.9910952939165962
    simulator.z0["e0_p_LV_o_tr5_c1"] = 0.9996518742093902
    simulator.z0["e0_p_LV_o_tr6_c1"] = 1.0130012240359512
    simulator.z0["e0_p_LV_o_tr7_c1"] = 1.0351345544672228
    simulator.z0["e0_p_LV_o_tr8_c1"] = 1.075114139663069
    simulator.z0["e0_p_LV_o_tr1_c2"] = 0.4262530468380868
    simulator.z0["e0_p_LV_o_tr2_c2"] = 0.42761682861806954
    simulator.z0["e0_p_LV_o_tr3_c2"] = 0.4294608429665033
    simulator.z0["e0_p_LV_o_tr4_c2"] = 0.4320666721197372
    simulator.z0["e0_p_LV_o_tr5_c2"] = 0.4359275128983566
    simulator.z0["e0_p_LV_o_tr6_c2"] = 0.44195324013854514
    simulator.z0["e0_p_LV_o_tr7_c2"] = 0.4519501064440809
    simulator.z0["e0_p_LV_o_tr8_c2"] = 0.4700265501639175
    simulator.z0["e0_v_L_tr1"] = 4.928230862763522e-05  # from initials_guess.txt (_1 suffix: gPROMS case collision)
    simulator.z0["e0_v_L_tr2"] = 4.8520481347862566e-05  # from initials_guess.txt (_1 suffix: gPROMS case collision)
    simulator.z0["e0_v_L_tr3"] = 4.7555508017851434e-05  # from initials_guess.txt (_1 suffix: gPROMS case collision)
    simulator.z0["e0_v_L_tr4"] = 4.6307301394424116e-05  # from initials_guess.txt (_1 suffix: gPROMS case collision)
    simulator.z0["e0_v_L_tr5"] = 4.4652827130287295e-05  # from initials_guess.txt (_1 suffix: gPROMS case collision)
    simulator.z0["e0_v_L_tr6"] = 4.239839903198249e-05  # from initials_guess.txt (_1 suffix: gPROMS case collision)
    simulator.z0["e0_v_L_tr7"] = 3.923677278750322e-05  # from initials_guess.txt (_1 suffix: gPROMS case collision)
    simulator.z0["e0_v_L_tr8"] = 3.470949564669704e-05  # from initials_guess.txt (_1 suffix: gPROMS case collision)
    simulator.z0["e0_x_L_tr1_c1"] = 0.7680549464407105
    simulator.z0["e0_x_L_tr2_c1"] = 0.7492722225804378
    simulator.z0["e0_x_L_tr3_c1"] = 0.7254809669095521
    simulator.z0["e0_x_L_tr4_c1"] = 0.6947066418743618
    simulator.z0["e0_x_L_tr5_c1"] = 0.6539158562694107
    simulator.z0["e0_x_L_tr6_c1"] = 0.5983333094670237
    simulator.z0["e0_x_L_tr7_c1"] = 0.5203839444650695
    simulator.z0["e0_x_L_tr8_c1"] = 0.4087646855694537
    simulator.z0["e0_x_L_tr1_c2"] = 0.23194505355928952
    simulator.z0["e0_x_L_tr2_c2"] = 0.2507277774195622
    simulator.z0["e0_x_L_tr3_c2"] = 0.27451903309044795
    simulator.z0["e0_x_L_tr4_c2"] = 0.3052933581256382
    simulator.z0["e0_x_L_tr5_c2"] = 0.34608414373058916
    simulator.z0["e0_x_L_tr6_c2"] = 0.40166669053297627
    simulator.z0["e0_x_L_tr7_c2"] = 0.4796160555349304
    simulator.z0["e0_x_L_tr8_c2"] = 0.5912353144305463
    simulator.z0["e0_x_V_tr2_c1"] = 0.7352347317315737
    simulator.z0["e0_x_V_tr3_c1"] = 0.7172546238597607
    simulator.z0["e0_x_V_tr4_c1"] = 0.6944800067876874
    simulator.z0["e0_x_V_tr5_c1"] = 0.6650207181061228
    simulator.z0["e0_x_V_tr6_c1"] = 0.625972988259654
    simulator.z0["e0_x_V_tr7_c1"] = 0.5727655728377369
    simulator.z0["e0_x_V_tr8_c1"] = 0.49814710910457743
    simulator.z0["e0_greek_gamma_tr0_c2"] = 2.051407326378184
    simulator.z0["e0_x_V_tr9_c1"] = 0.3912975197281897
    simulator.z0["e0_x_V_tr2_c2"] = 0.22203367073082497
    simulator.z0["e0_x_V_tr3_c2"] = 0.24001377860263798
    simulator.z0["e0_x_V_tr4_c2"] = 0.26278839567471135
    simulator.z0["e0_x_V_tr5_c2"] = 0.29224768435627596
    simulator.z0["e0_x_V_tr6_c2"] = 0.3312954142027448
    simulator.z0["e0_x_V_tr7_c2"] = 0.3845028296246618
    simulator.z0["e0_x_V_tr8_c2"] = 0.45912129335782126
    simulator.z0["e0_x_V_tr9_c2"] = 0.5659708825443007
    simulator.z0["e0_greek_alpha_tr9_c1"] = 0.23687073001589976
    simulator.z0["e0_greek_alpha_tr9_c2"] = 0.7933139186590011
    simulator.z0["e0_greek_gamma_tr9_c1"] = 3.18816089398837
    simulator.z0["e0_greek_gamma_tr9_c2"] = 1.021599256783003
    simulator.z0["e0_H_tr9"] = -430135.4314841213
    simulator.z0["e0_HU_L_tr9"] = 1541.126175890857
    simulator.z0["e0_HU_V_tr9"] = 0.914750265762603
    simulator.z0["e0_K_tr9_c1"] = 4.391743722249875
    simulator.z0["e0_K_tr9_c2"] = 0.6213304577932718
    simulator.z0["e0_T_tr9"] = 360.3231763871688
    simulator.z0["e0_V_L_tr9"] = 0.03350998985280147
    simulator.z0["e0_V_V_tr9"] = 0.026490010147198526
    simulator.z0["e0_h_L_tr9"] = -278.9711427978777
    simulator.z0["e0_h_feed_tr9"] = -279.3460703110792
    simulator.z0["e0_p_tr9"] = 1.0344812826286272
    simulator.z0["e0_p_LV_o_tr9_c1"] = 1.425014869022431
    simulator.z0["e0_p_LV_o_tr9_c2"] = 0.6291652276042551
    simulator.z0["e0_v_L_tr9"] = 2.1743832774387096e-05  # from initials_guess.txt (_1 suffix: gPROMS case collision)
    simulator.z0["e0_x_L_tr9_c1"] = 0.08909844118311379
    simulator.z0["e0_x_L_tr9_c2"] = 0.9109015588168863
    simulator.z0["e0_LI"] = 55.84998308800245
    simulator.z0["e0_M_D"] = 4.6e-11
    simulator.z0["e0_M_D_c1"] = 4.6e-11
    simulator.z0["e0_M_D_c2"] = 0.0
    simulator.z0["e0_PDI"] = 6.4812826286271275
    simulator.z0["e0_PI_B"] = 1034.4812826286272
    simulator.z0["e0_PI_C"] = 1028.0
    simulator.z0["e0_WI"] = 4.6e-08
    simulator.z0["e0_w_L_B_c1"] = 0.19997936173551345
    simulator.z0["e0_w_L_B_c2"] = 0.8000206382644863
    simulator.z0["e0_w_L_C_c1"] = 0.9022425630687501
    simulator.z0["e0_w_L_C_c2"] = 0.09775743693124987
    simulator.z0["e0_w_L_D_c1"] = 1.0
    simulator.z0["e0_w_L_D_c2"] = 0.0
    simulator.z0["e0_greek_alpha_tr1_c1"] = 0.23512652841697929
    simulator.z0["e0_greek_alpha_tr2_c1"] = 0.23514072859591423
    simulator.z0["e0_F_L_tr0"] = 0.12568492539488962
    simulator.z0["e0_greek_alpha_tr3_c1"] = 0.23515986011984272
    simulator.z0["e0_greek_alpha_tr4_c1"] = 0.23518676134086977
    simulator.z0["e0_greek_alpha_tr5_c1"] = 0.2352263335658058
    simulator.z0["e0_greek_alpha_tr6_c1"] = 0.23528742749605283
    simulator.z0["e0_greek_alpha_tr7_c1"] = 0.23538704130751228
    simulator.z0["e0_greek_alpha_tr8_c1"] = 0.2355619081202511
    simulator.z0["e0_greek_alpha_tr1_c2"] = 0.7628635465955349
    simulator.z0["e0_greek_alpha_tr2_c2"] = 0.7631075664264907
    simulator.z0["e0_greek_alpha_tr3_c2"] = 0.7634364279762558
    simulator.z0["e0_greek_alpha_tr4_c2"] = 0.7638990412888568
    simulator.z0["e0_F_V_tr1"] = 0.1312953870320884
    simulator.z0["e0_greek_alpha_tr5_c2"] = 0.7645799678185233
    simulator.z0["e0_greek_alpha_tr6_c2"] = 0.7656321890352836
    simulator.z0["e0_greek_alpha_tr7_c2"] = 0.7673503572832293
    simulator.z0["e0_greek_alpha_tr8_c2"] = 0.7703740752087221
    simulator.z0["e0_greek_gamma_tr1_c1"] = 1.0462868901137248
    simulator.z0["e0_greek_gamma_tr2_c1"] = 1.054675966592118
    simulator.z0["e0_greek_gamma_tr3_c1"] = 1.0665085256024522
    simulator.z0["e0_greek_gamma_tr4_c1"] = 1.0839516156783338
    simulator.z0["e0_greek_gamma_tr5_c1"] = 1.1111532230309928
    simulator.z0["e0_greek_gamma_tr6_c1"] = 1.1568183063797384
    simulator.z0["e0_F_D"] = 0.0
    simulator.z0["e0_greek_gamma_tr7_c1"] = 1.2415828080166478
    simulator.z0["e0_greek_gamma_tr8_c1"] = 1.4231730698367258
    simulator.z0["e0_greek_gamma_tr1_c2"] = 2.0095698975719993
    simulator.z0["e0_greek_gamma_tr2_c2"] = 1.959285028778471
    simulator.z0["e0_greek_gamma_tr3_c2"] = 1.8982799738224472
    simulator.z0["e0_greek_gamma_tr4_c2"] = 1.8235824604277995
    simulator.z0["e0_greek_gamma_tr5_c2"] = 1.7313997987979761
    simulator.z0["e0_greek_gamma_tr6_c2"] = 1.6172354913936249
    simulator.z0["e0_greek_gamma_tr7_c2"] = 1.4768958136795285
    simulator.z0["e0_greek_gamma_tr8_c2"] = 1.3104717365000196
    simulator.z0["e0_K_tr0_c1"] = 0.987384479742484
    simulator.z0["e0_A_col"] = 0.0019634953750000002
    simulator.z0["e0_A_active"] = 0.0016100662075
    simulator.z0["e0_F_L_tr1"] = 0.12557425808102898
    simulator.z0["e0_F_L_tr2"] = 0.12543629822085414
    simulator.z0["e0_F_L_tr3"] = 0.12526140617550446
    simulator.z0["e0_F_L_tr4"] = 0.12503518136410655
    simulator.z0["e0_F_L_tr5"] = 0.12473545153067245
    simulator.z0["e0_F_L_tr6"] = 0.12432702246583055
    simulator.z0["e0_F_L_tr7"] = 0.12375189468402154
    simulator.z0["e0_F_L_tr8"] = 0.1220647042915842
    simulator.z0["e0_K_tr0_c2"] = 0.8485040494262693
    simulator.z0["e0_F_V_tr2"] = 0.1311797796131301
    simulator.z0["e0_F_V_tr3"] = 0.13103566132791547
    simulator.z0["e0_F_V_tr4"] = 0.13085296223206716
    simulator.z0["e0_F_V_tr5"] = 0.13061663891484857
    simulator.z0["e0_F_V_tr6"] = 0.1303035293694644
    simulator.z0["e0_F_V_tr7"] = 0.1298768683467901
    simulator.z0["e0_F_V_tr8"] = 0.12927606731345495
    simulator.z0["e0_F_V_tr9"] = 0.12751356220600688
    simulator.z0["e0_H_tr1"] = -401.95086294361914
    simulator.z0["e0_H_tr2"] = -408.33004883599597
    simulator.z0["e0_rr"] = 1.0
    simulator.z0["e0_Q_R"] = 5.0

    # fmt:off
    # Scaling of algebraic states
    # NOTE: Scaling factors represent the order of magnitude of the initial guess (z0).
    # If z0 is 0, we use 1.0 as a default scaling factor.
    
    # Enthalpy states (liquid, vapor and total)
    simulator.scaling["_z", "e0_h_L_tr0_c1"] = 300.0
    simulator.scaling["_z", "e0_h_L_tr0_c2"] = 300.0
    simulator.scaling["_z", "e0_h_L_tr1_c1"] = 300.0  
    simulator.scaling["_z", "e0_h_L_tr1_c2"] = 300.0  
    simulator.scaling["_z", "e0_h_L_tr2_c1"] = 300.0  
    simulator.scaling["_z", "e0_h_L_tr2_c2"] = 300.0  
    simulator.scaling["_z", "e0_h_L_tr3_c1"] = 300.0 
    simulator.scaling["_z", "e0_h_L_tr3_c2"] = 300.0  
    simulator.scaling["_z", "e0_h_L_tr4_c1"] = 300.0  
    simulator.scaling["_z", "e0_h_L_tr4_c2"] = 300.0  
    simulator.scaling["_z", "e0_h_L_tr5_c1"] = 300.0  
    simulator.scaling["_z", "e0_h_L_tr5_c2"] = 300.0  
    simulator.scaling["_z", "e0_h_L_tr6_c1"] = 300.0  
    simulator.scaling["_z", "e0_h_L_tr6_c2"] = 300.0  
    simulator.scaling["_z", "e0_h_L_tr7_c1"] = 300.0  
    simulator.scaling["_z", "e0_h_L_tr7_c2"] = 300.0  
    simulator.scaling["_z", "e0_h_L_tr8_c1"] = 300.0  
    simulator.scaling["_z", "e0_h_L_tr8_c2"] = 300.0  
    simulator.scaling["_z", "e0_h_L_tr9_c1"] = 300.0  
    simulator.scaling["_z", "e0_h_L_tr9_c2"] = 300.0

    simulator.scaling["_z", "e0_h_L_tr0"] = 300.0
    simulator.scaling["_z", "e0_h_L_tr1"] = 300.0
    simulator.scaling["_z", "e0_h_L_tr2"] = 300.0
    simulator.scaling["_z", "e0_h_L_tr3"] = 300.0
    simulator.scaling["_z", "e0_h_L_tr4"] = 300.0
    simulator.scaling["_z", "e0_h_L_tr5"] = 300.0
    simulator.scaling["_z", "e0_h_L_tr6"] = 300.0
    simulator.scaling["_z", "e0_h_L_tr7"] = 300.0
    simulator.scaling["_z", "e0_h_L_tr8"] = 300.0
    simulator.scaling["_z", "e0_h_L_tr9"] = 300.0

    simulator.scaling["_z", "e0_h_V_tr1_c1"] = 300.0  
    simulator.scaling["_z", "e0_h_V_tr1_c2"] = 300.0  
    simulator.scaling["_z", "e0_h_V_tr2_c1"] = 300.0  
    simulator.scaling["_z", "e0_h_V_tr2_c2"] = 300.0  
    simulator.scaling["_z", "e0_h_V_tr3_c1"] = 300.0  
    simulator.scaling["_z", "e0_h_V_tr3_c2"] = 300.0  
    simulator.scaling["_z", "e0_h_V_tr4_c1"] = 300.0  
    simulator.scaling["_z", "e0_h_V_tr4_c2"] = 300.0  
    simulator.scaling["_z", "e0_h_V_tr5_c1"] = 300.0  
    simulator.scaling["_z", "e0_h_V_tr5_c2"] = 300.0  
    simulator.scaling["_z", "e0_h_V_tr6_c1"] = 300.0  
    simulator.scaling["_z", "e0_h_V_tr6_c2"] = 300.0  
    simulator.scaling["_z", "e0_h_V_tr7_c1"] = 300.0  
    simulator.scaling["_z", "e0_h_V_tr7_c2"] = 300.0  
    simulator.scaling["_z", "e0_h_V_tr8_c1"] = 300.0  
    simulator.scaling["_z", "e0_h_V_tr8_c2"] = 300.0  
    simulator.scaling["_z", "e0_h_V_tr9_c1"] = 300.0  
    simulator.scaling["_z", "e0_h_V_tr9_c2"] = 300.0

    simulator.scaling["_z", "e0_h_V_tr1"] = 300.0
    simulator.scaling["_z", "e0_h_V_tr2"] = 300.0
    simulator.scaling["_z", "e0_h_V_tr3"] = 300.0
    simulator.scaling["_z", "e0_h_V_tr4"] = 300.0
    simulator.scaling["_z", "e0_h_V_tr5"] = 300.0
    simulator.scaling["_z", "e0_h_V_tr6"] = 300.0
    simulator.scaling["_z", "e0_h_V_tr7"] = 300.0
    simulator.scaling["_z", "e0_h_V_tr8"] = 300.0
    simulator.scaling["_z", "e0_h_V_tr9"] = 300.0

    simulator.scaling["_z", "e0_h_feed_tr9_c1"] = 300.0  # z0=-266.518911067034
    simulator.scaling["_z", "e0_h_feed_tr9_c2"] = 300.0  # z0=-266.518911067034
    
    # Activity coefficients and related properties
    simulator.scaling["_z", "e0_Q_C"] = 1.0  # z0=-6.523701526549227
    
    # Enthalpy and internal energy states
    simulator.scaling["_z", "e0_H_tr1"] = 100.0
    simulator.scaling["_z", "e0_H_tr2"] = 100.0
    simulator.scaling["_z", "e0_H_tr3"] = 100.0
    simulator.scaling["_z", "e0_H_tr4"] = 100.0
    simulator.scaling["_z", "e0_H_tr5"] = 100.0
    simulator.scaling["_z", "e0_H_tr6"] = 100.0
    simulator.scaling["_z", "e0_H_tr7"] = 100.0
    simulator.scaling["_z", "e0_H_tr8"] = 100.0
    simulator.scaling["_z", "e0_H_tr9"] = 1e5
    
    
    # Hold-up states (liquid and vapor)
    simulator.scaling["_z", "e0_HU_L_tr1"] = 1.0  # z0=1.531452265249518
    simulator.scaling["_z", "e0_HU_L_tr2"] = 1.0  # z0=1.559456739563267
    simulator.scaling["_z", "e0_HU_L_tr3"] = 1.0  # z0=1.5946752189871898
    simulator.scaling["_z", "e0_HU_L_tr4"] = 1.0  # z0=1.639938968554021
    simulator.scaling["_z", "e0_HU_L_tr5"] = 1.0  # z0=1.6996504734289253
    simulator.scaling["_z", "e0_HU_L_tr6"] = 1.0  # z0=1.78095389570281
    simulator.scaling["_z", "e0_HU_L_tr7"] = 1.0  # z0=1.8961714684634854
    simulator.scaling["_z", "e0_HU_L_tr8"] = 1.0  # z0=2.0481797816092135
    simulator.scaling["_z", "e0_HU_L_tr9"] = 1000.0  # z0=1528.0029186928748
    
    simulator.scaling["_z", "e0_HU_V_tr1"] = 1.0  # z0=0.009872927021616044
    simulator.scaling["_z", "e0_HU_V_tr2"] = 1.0  # z0=0.009878324766557745
    simulator.scaling["_z", "e0_HU_V_tr3"] = 1.0  # z0=0.009883161936084081
    simulator.scaling["_z", "e0_HU_V_tr4"] = 1.0  # z0=0.009887174119314049
    simulator.scaling["_z", "e0_HU_V_tr5"] = 1.0  # z0=0.009889951129046556
    simulator.scaling["_z", "e0_HU_V_tr6"] = 1.0  # z0=0.009890833343322277
    simulator.scaling["_z", "e0_HU_V_tr7"] = 1.0  # z0=0.009888490118108982
    simulator.scaling["_z", "e0_HU_V_tr8"] = 1.0  # z0=0.00994531915762383
    simulator.scaling["_z", "e0_HU_V_tr9"] = 1.0  # z0=0.9124037471174476
    
    # Equilibrium constants
    simulator.scaling["_z", "e0_K_tr0_c1"] = 1.0
    simulator.scaling["_z", "e0_K_tr1_c1"] = 1.0
    simulator.scaling["_z", "e0_K_tr2_c1"] = 1.0
    simulator.scaling["_z", "e0_K_tr3_c1"] = 1.0
    simulator.scaling["_z", "e0_K_tr4_c1"] = 1.0
    simulator.scaling["_z", "e0_K_tr5_c1"] = 1.0
    simulator.scaling["_z", "e0_K_tr6_c1"] = 1.0
    simulator.scaling["_z", "e0_K_tr7_c1"] = 1.0
    simulator.scaling["_z", "e0_K_tr8_c1"] = 1.0
    simulator.scaling["_z", "e0_K_tr9_c1"] = 1.0

    simulator.scaling["_z", "e0_K_tr0_c2"] = 1.0
    simulator.scaling["_z", "e0_K_tr1_c2"] = 1.0
    simulator.scaling["_z", "e0_K_tr2_c2"] = 1.0
    simulator.scaling["_z", "e0_K_tr3_c2"] = 1.0
    simulator.scaling["_z", "e0_K_tr4_c2"] = 1.0
    simulator.scaling["_z", "e0_K_tr5_c2"] = 1.0
    simulator.scaling["_z", "e0_K_tr6_c2"] = 1.0
    simulator.scaling["_z", "e0_K_tr7_c2"] = 1.0
    simulator.scaling["_z", "e0_K_tr8_c2"] = 1.0
    simulator.scaling["_z", "e0_K_tr9_c2"] = 1.0
    
    # Liquid level and related properties
    simulator.scaling["_z", "e0_L_tr1"] = 0.1
    simulator.scaling["_z", "e0_L_tr2"] = 0.1
    simulator.scaling["_z", "e0_L_tr3"] = 0.1
    simulator.scaling["_z", "e0_L_tr4"] = 0.1
    simulator.scaling["_z", "e0_L_tr5"] = 0.1
    simulator.scaling["_z", "e0_L_tr6"] = 0.1
    simulator.scaling["_z", "e0_L_tr7"] = 0.1
    simulator.scaling["_z", "e0_L_tr8"] = 0.1
    simulator.scaling["_z", "e0_L_weir"] = 0.1
    
    # Temperatures for all trays
    simulator.scaling["_z", "e0_T_tr0"] = 100.0
    simulator.scaling["_z", "e0_T_tr1"] = 100.0
    simulator.scaling["_z", "e0_T_tr2"] = 100.0
    simulator.scaling["_z", "e0_T_tr3"] = 100.0
    simulator.scaling["_z", "e0_T_tr4"] = 100.0
    simulator.scaling["_z", "e0_T_tr5"] = 100.0
    simulator.scaling["_z", "e0_T_tr6"] = 100.0
    simulator.scaling["_z", "e0_T_tr7"] = 100.0
    simulator.scaling["_z", "e0_T_tr8"] = 100.0
    simulator.scaling["_z", "e0_T_tr9"] = 100.0
    
    # Pressures
    simulator.scaling["_z", "e0_p_LV_o_tr0_c1"] = 1.0
    simulator.scaling["_z", "e0_p_LV_o_tr0_c2"] = 1.0
    simulator.scaling["_z", "e0_p_LV_o_tr1_c1"] = 1.0
    simulator.scaling["_z", "e0_p_LV_o_tr2_c1"] = 1.0
    simulator.scaling["_z", "e0_p_LV_o_tr3_c1"] = 1.0
    simulator.scaling["_z", "e0_p_LV_o_tr4_c1"] = 1.0
    simulator.scaling["_z", "e0_p_LV_o_tr5_c1"] = 1.0
    simulator.scaling["_z", "e0_p_LV_o_tr6_c1"] = 1.0
    simulator.scaling["_z", "e0_p_LV_o_tr7_c1"] = 1.0
    simulator.scaling["_z", "e0_p_LV_o_tr8_c1"] = 1.0
    simulator.scaling["_z", "e0_p_LV_o_tr1_c2"] = 1.0
    simulator.scaling["_z", "e0_p_LV_o_tr2_c2"] = 1.0
    simulator.scaling["_z", "e0_p_LV_o_tr3_c2"] = 1.0
    simulator.scaling["_z", "e0_p_LV_o_tr4_c2"] = 1.0
    simulator.scaling["_z", "e0_p_LV_o_tr5_c2"] = 1.0
    simulator.scaling["_z", "e0_p_LV_o_tr6_c2"] = 1.0
    simulator.scaling["_z", "e0_p_LV_o_tr7_c2"] = 1.0
    simulator.scaling["_z", "e0_p_LV_o_tr8_c2"] = 1.0
    simulator.scaling["_z", "e0_p_LV_o_tr9_c1"] = 1.0
    simulator.scaling["_z", "e0_p_LV_o_tr9_c2"] = 1.0
    
    # Liquid molar volumes and compositions
    simulator.scaling["_z", "e0_v_L_tr1"] = 1.0e-5
    simulator.scaling["_z", "e0_v_L_tr2"] = 1.0e-5
    simulator.scaling["_z", "e0_v_L_tr3"] = 1.0e-5
    simulator.scaling["_z", "e0_v_L_tr4"] = 1.0e-5
    simulator.scaling["_z", "e0_v_L_tr5"] = 1.0e-5
    simulator.scaling["_z", "e0_v_L_tr6"] = 1.0e-5
    simulator.scaling["_z", "e0_v_L_tr7"] = 1.0e-5
    simulator.scaling["_z", "e0_v_L_tr8"] = 1.0e-5
    simulator.scaling["_z", "e0_v_L_tr9"] = 1.0e-5
    
    # Liquid compositions for component 1
    simulator.scaling["_z", "e0_x_L_tr1_c1"] = 1.0
    simulator.scaling["_z", "e0_x_L_tr2_c1"] = 1.0
    simulator.scaling["_z", "e0_x_L_tr3_c1"] = 1.0
    simulator.scaling["_z", "e0_x_L_tr4_c1"] = 1.0
    simulator.scaling["_z", "e0_x_L_tr5_c1"] = 1.0
    simulator.scaling["_z", "e0_x_L_tr6_c1"] = 1.0
    simulator.scaling["_z", "e0_x_L_tr7_c1"] = 1.0
    simulator.scaling["_z", "e0_x_L_tr8_c1"] = 1.0
    simulator.scaling["_z", "e0_x_L_tr9_c1"] = 1.0
    
    # Liquid compositions for component 2
    simulator.scaling["_z", "e0_x_L_tr1_c2"] = 1.0
    simulator.scaling["_z", "e0_x_L_tr2_c2"] = 1.0
    simulator.scaling["_z", "e0_x_L_tr3_c2"] = 1.0
    simulator.scaling["_z", "e0_x_L_tr4_c2"] = 1.0
    simulator.scaling["_z", "e0_x_L_tr5_c2"] = 1.0
    simulator.scaling["_z", "e0_x_L_tr6_c2"] = 1.0
    simulator.scaling["_z", "e0_x_L_tr7_c2"] = 1.0
    simulator.scaling["_z", "e0_x_L_tr8_c2"] = 1.0
    simulator.scaling["_z", "e0_x_L_tr0_c1"] = 1.0
    simulator.scaling["_z", "e0_x_L_tr0_c2"] = 1.0
    simulator.scaling["_z", "e0_x_L_tr9_c2"] = 1.0
    
    # Vapor compositions for component 1
    simulator.scaling["_z", "e0_x_V_tr0_c1"] = 1.0
    simulator.scaling["_z", "e0_x_V_tr1_c1"] = 1.0
    simulator.scaling["_z", "e0_x_V_tr2_c1"] = 1.0
    simulator.scaling["_z", "e0_x_V_tr3_c1"] = 1.0
    simulator.scaling["_z", "e0_x_V_tr4_c1"] = 1.0
    simulator.scaling["_z", "e0_x_V_tr5_c1"] = 1.0
    simulator.scaling["_z", "e0_x_V_tr6_c1"] = 1.0
    simulator.scaling["_z", "e0_x_V_tr7_c1"] = 1.0
    simulator.scaling["_z", "e0_x_V_tr8_c1"] = 1.0
    simulator.scaling["_z", "e0_x_V_tr9_c1"] = 1.0
    
    # Vapor compositions for component 2
    simulator.scaling["_z", "e0_x_V_tr0_c2"] = 1.0
    simulator.scaling["_z", "e0_x_V_tr1_c2"] = 1.0
    simulator.scaling["_z", "e0_x_V_tr2_c2"] = 1.0
    simulator.scaling["_z", "e0_x_V_tr3_c2"] = 1.0
    simulator.scaling["_z", "e0_x_V_tr4_c2"] = 1.0
    simulator.scaling["_z", "e0_x_V_tr5_c2"] = 1.0
    simulator.scaling["_z", "e0_x_V_tr6_c2"] = 1.0
    simulator.scaling["_z", "e0_x_V_tr7_c2"] = 1.0
    simulator.scaling["_z", "e0_x_V_tr8_c2"] = 1.0
    simulator.scaling["_z", "e0_x_V_tr9_c2"] = 1.0
    
    # Activity coefficient gamma
    simulator.scaling["_z", "e0_greek_gamma_tr0_c1"] = 1.0
    simulator.scaling["_z", "e0_greek_gamma_tr1_c1"] = 1.0
    simulator.scaling["_z", "e0_greek_gamma_tr2_c1"] = 1.0
    simulator.scaling["_z", "e0_greek_gamma_tr3_c1"] = 1.0
    simulator.scaling["_z", "e0_greek_gamma_tr4_c1"] = 1.0
    simulator.scaling["_z", "e0_greek_gamma_tr5_c1"] = 1.0
    simulator.scaling["_z", "e0_greek_gamma_tr6_c1"] = 1.0
    simulator.scaling["_z", "e0_greek_gamma_tr7_c1"] = 1.0
    simulator.scaling["_z", "e0_greek_gamma_tr8_c1"] = 1.0
    simulator.scaling["_z", "e0_greek_gamma_tr9_c1"] = 1.0

    simulator.scaling["_z", "e0_greek_gamma_tr0_c2"] = 1.0
    simulator.scaling["_z", "e0_greek_gamma_tr1_c2"] = 1.0
    simulator.scaling["_z", "e0_greek_gamma_tr2_c2"] = 1.0
    simulator.scaling["_z", "e0_greek_gamma_tr3_c2"] = 1.0
    simulator.scaling["_z", "e0_greek_gamma_tr4_c2"] = 1.0
    simulator.scaling["_z", "e0_greek_gamma_tr5_c2"] = 1.0
    simulator.scaling["_z", "e0_greek_gamma_tr6_c2"] = 1.0
    simulator.scaling["_z", "e0_greek_gamma_tr7_c2"] = 1.0
    simulator.scaling["_z", "e0_greek_gamma_tr8_c2"] = 1.0
    simulator.scaling["_z", "e0_greek_gamma_tr9_c2"] = 1.0
    
    # Alpha coefficients
    simulator.scaling["_z", "e0_greek_alpha_tr0_c1"] = 1.0
    simulator.scaling["_z", "e0_greek_alpha_tr1_c1"] = 1.0
    simulator.scaling["_z", "e0_greek_alpha_tr2_c1"] = 1.0
    simulator.scaling["_z", "e0_greek_alpha_tr3_c1"] = 1.0
    simulator.scaling["_z", "e0_greek_alpha_tr4_c1"] = 1.0
    simulator.scaling["_z", "e0_greek_alpha_tr5_c1"] = 1.0
    simulator.scaling["_z", "e0_greek_alpha_tr6_c1"] = 1.0
    simulator.scaling["_z", "e0_greek_alpha_tr7_c1"] = 1.0
    simulator.scaling["_z", "e0_greek_alpha_tr8_c1"] = 1.0
    simulator.scaling["_z", "e0_greek_alpha_tr9_c1"] = 1.0

    simulator.scaling["_z", "e0_greek_alpha_tr0_c2"] = 1.0
    simulator.scaling["_z", "e0_greek_alpha_tr1_c2"] = 1.0
    simulator.scaling["_z", "e0_greek_alpha_tr2_c2"] = 1.0
    simulator.scaling["_z", "e0_greek_alpha_tr3_c2"] = 1.0
    simulator.scaling["_z", "e0_greek_alpha_tr4_c2"] = 1.0
    simulator.scaling["_z", "e0_greek_alpha_tr5_c2"] = 1.0
    simulator.scaling["_z", "e0_greek_alpha_tr6_c2"] = 1.0
    simulator.scaling["_z", "e0_greek_alpha_tr7_c2"] = 1.0
    simulator.scaling["_z", "e0_greek_alpha_tr8_c2"] = 1.0
    simulator.scaling["_z", "e0_greek_alpha_tr9_c2"] = 1.0
    
    # Volume states
    simulator.scaling["_z", "e0_V_L_tr1"] = 1e-5
    simulator.scaling["_z", "e0_V_L_tr2"] = 1e-5
    simulator.scaling["_z", "e0_V_L_tr3"] = 1e-5
    simulator.scaling["_z", "e0_V_L_tr4"] = 1e-5
    simulator.scaling["_z", "e0_V_L_tr5"] = 1e-5
    simulator.scaling["_z", "e0_V_L_tr6"] = 1e-5
    simulator.scaling["_z", "e0_V_L_tr7"] = 1e-5
    simulator.scaling["_z", "e0_V_L_tr8"] = 1e-5
    simulator.scaling["_z", "e0_V_L_tr9"] = 0.1

    simulator.scaling["_z", "e0_V_V_tr1"] = 1e-4
    simulator.scaling["_z", "e0_V_V_tr2"] = 1e-4
    simulator.scaling["_z", "e0_V_V_tr3"] = 1e-4
    simulator.scaling["_z", "e0_V_V_tr4"] = 1e-4
    simulator.scaling["_z", "e0_V_V_tr5"] = 1e-4
    simulator.scaling["_z", "e0_V_V_tr6"] = 1e-4
    simulator.scaling["_z", "e0_V_V_tr7"] = 1e-4
    simulator.scaling["_z", "e0_V_V_tr8"] = 1e-4
    simulator.scaling["_z", "e0_V_V_tr9"] = 0.1

    simulator.scaling["_z", "e0_V_tot"] = 1e-4
    
    # Pressure states
    simulator.scaling["_z", "e0_p_tr1"] = 1.0
    simulator.scaling["_z", "e0_p_tr2"] = 1.0
    simulator.scaling["_z", "e0_p_tr3"] = 1.0
    simulator.scaling["_z", "e0_p_tr4"] = 1.0
    simulator.scaling["_z", "e0_p_tr5"] = 1.0
    simulator.scaling["_z", "e0_p_tr6"] = 1.0
    simulator.scaling["_z", "e0_p_tr7"] = 1.0
    simulator.scaling["_z", "e0_p_tr8"] = 1.0
    simulator.scaling["_z", "e0_p_tr9"] = 1.0
    
    # Flow rates
    simulator.scaling["_z", "e0_F_L_tr0"] = 1.0
    simulator.scaling["_z", "e0_F_L_tr1"] = 1.0
    simulator.scaling["_z", "e0_F_L_tr2"] = 1.0
    simulator.scaling["_z", "e0_F_L_tr3"] = 1.0
    simulator.scaling["_z", "e0_F_L_tr4"] = 1.0
    simulator.scaling["_z", "e0_F_L_tr5"] = 1.0
    simulator.scaling["_z", "e0_F_L_tr6"] = 1.0
    simulator.scaling["_z", "e0_F_L_tr7"] = 1.0
    simulator.scaling["_z", "e0_F_L_tr8"] = 1.0

    simulator.scaling["_z", "e0_F_V_tr1"] = 1.0
    simulator.scaling["_z", "e0_F_V_tr2"] = 1.0
    simulator.scaling["_z", "e0_F_V_tr3"] = 1.0
    simulator.scaling["_z", "e0_F_V_tr4"] = 1.0
    simulator.scaling["_z", "e0_F_V_tr5"] = 1.0
    simulator.scaling["_z", "e0_F_V_tr6"] = 1.0
    simulator.scaling["_z", "e0_F_V_tr7"] = 1.0
    simulator.scaling["_z", "e0_F_V_tr8"] = 1.0
    simulator.scaling["_z", "e0_F_V_tr9"] = 1.0

    simulator.scaling["_z", "e0_F_D"] = 1.0
    
    # Column geometry
    simulator.scaling["_z", "e0_A_col"] = 1e-3
    simulator.scaling["_z", "e0_A_active"] = 1e-3
    
    
    # Product quality indicators
    simulator.scaling["_z", "e0_LI"] = 10.0
    simulator.scaling["_z", "e0_WI"] = 1e3
    simulator.scaling["_z", "e0_M_D"] = 1.0
    simulator.scaling["_z", "e0_M_D_c1"] = 1.0
    simulator.scaling["_z", "e0_M_D_c2"] = 1.0
    simulator.scaling["_z", "e0_PDI"] = 10.0
    simulator.scaling["_z", "e0_PI_B"] = 1e3
    simulator.scaling["_z", "e0_PI_C"] = 1e3
    simulator.scaling["_z", "e0_w_L_B_c1"] = 1.0
    simulator.scaling["_z", "e0_w_L_B_c2"] = 1.0
    simulator.scaling["_z", "e0_w_L_C_c1"] = 1.0
    simulator.scaling["_z", "e0_w_L_C_c2"] = 1.0
    simulator.scaling["_z", "e0_w_L_D_c1"] = 1.0 
    simulator.scaling["_z", "e0_w_L_D_c2"] = 1.0 
    
    
    # Control and error states
    simulator.scaling["_z", "e0_Q_R"] = 5.0
    simulator.scaling["_z", "e0_rr"] = 1.0
    
    # fmt:on

    # Default control inputs (overwritten at every make_step call).
    # Values sourced from helper/initials_guess.txt (gSTORE snapshot).
    simulator.u0["e0_rr_PLS"] = 1.15
    simulator.u0["e0_Q_PLS_R"] = 5.0
    simulator.u0["e0_F_feed_tr9"] = 0.0
    simulator.u0["e0_F_B"] = 0.0
    simulator.u0["e0_x_feed_tr9_c1"] = 0.0
    simulator.u0["e0_x_feed_tr9_c2"] = 1.0
    simulator.u0["e0_rr_err"] = -0.15
    simulator.u0["e0_E_murphree"] = 0.5000000005975629
    simulator.u0["e0_x_N2"] = 0.04273159753760128
    simulator.u0["e0_h_tot"] = 0.179372959955645
    simulator.u0["e0_h_weir"] = 0.0428980603490154
    simulator.u0["e0_greek_kappa"] = 0.0424670248823593

    # fmt:on
    return simulator


def simulate_init_recipe(
    E_murphree: float,
    rr_err: float,
    LI: float,
    w_L_B_c1: float,
    t_settle: float = 1000.0,
    t_step: float = 1.0,
) -> do_mpc.simulator.Simulator:
    """Run initialization recipe via do_mpc (piecewise-constant steps).

    Pattern: change / settle / change / settle / ...

    Phases:
        1. Hold at default u0 (*t_settle*).
        2. Staircase ramp of ``e0_E_murphree`` (*t_settle*).
        3. Hold (*t_settle*).
        4. Staircase ramp of ``e0_rr_err`` and ``e0_rr_PLS`` (*t_settle*,
           keeps ``rr_PLS + rr_err = 1``).
        5. Hold (*t_settle*).
        6. Drive ``e0_w_L_B_c1`` to *w_L_B_c1* via feed composition
           (up to 1000 steps).
        6a. Hold (*t_settle*).
        7. Drive ``e0_LI`` to *LI* via feed/bottoms (up to 1000 steps).
        8. Hold (*t_settle*).

    Parameters
    ----------
    E_murphree : float
        Target Murphree efficiency.
    rr_err : float
        Target reflux-ratio error.
    LI : float
        Target level indicator value.
    w_L_B_c1 : float
        Target bottoms mass fraction of component 1.
    t_settle : float
        Settle / hold / ramp duration in seconds (default 1000.0).
    t_step : float
        Integration time step in seconds (default 1.0).

    Returns
    -------
    do_mpc.simulator.Simulator
        Simulator with full trajectory in ``simulator.data`` and final
        state in ``simulator.x0`` / ``simulator.z0``.
    """
    model = template_model_for_pe_initialization()
    simulator = template_simulator(model)

    simulator.set_param(
        integration_tool="idas", abstol=1e-10, reltol=1e-10, t_step=t_step,
    )
    simulator.setup()
    simulator.set_initial_guess()
    simulator.init_algebraic_variables()

    n_steps: int = max(int(round(t_settle / t_step)), 1)
    u0 = simulator.u0

    # Store initial ramp start values.
    E_murphree_0: float = float(u0["e0_E_murphree"])
    rr_err_0: float = float(u0["e0_rr_err"])
    rr_PLS_0: float = float(u0["e0_rr_PLS"])

    # --- Phase 1: hold ---
    for _ in range(n_steps):
        simulator.make_step(u0.master)

    # --- Phase 2: ramp e0_E_murphree ---
    for k in range(n_steps):
        alpha = (k + 1) / n_steps
        u0["e0_E_murphree"] = E_murphree_0 + alpha * (E_murphree - E_murphree_0)
        simulator.make_step(u0.master)

    # --- Phase 3: hold ---
    for _ in range(n_steps):
        simulator.make_step(u0.master)

    # --- Phase 4: ramp e0_rr_err AND e0_rr_PLS (keep sum = 1) ---
    rr_PLS_target: float = 1.0 - rr_err
    for k in range(n_steps):
        alpha = (k + 1) / n_steps
        u0["e0_rr_err"] = rr_err_0 + alpha * (rr_err - rr_err_0)
        u0["e0_rr_PLS"] = rr_PLS_0 + alpha * (rr_PLS_target - rr_PLS_0)
        simulator.make_step(u0.master)

    # --- Phase 5: hold ---
    for _ in range(n_steps):
        simulator.make_step(u0.master)

    # --- Phase 6: drive e0_w_L_B_c1 to target ---
    wB_tol: float = 0.0001
    max_ctrl_steps: int = 1000
    current_wB: float = float(simulator.data["_z", "e0_w_L_B_c1"][-1].item())

    if abs(current_wB - w_L_B_c1) > wB_tol:
        u0["e0_F_feed_tr9"] = 1.0
        going_up: bool = current_wB < w_L_B_c1
        if going_up:
            u0["e0_x_feed_tr9_c1"] = 1.0
            u0["e0_x_feed_tr9_c2"] = 0.0
        else:
            u0["e0_x_feed_tr9_c1"] = 0.0
            u0["e0_x_feed_tr9_c2"] = 1.0

        prev_wB: float = current_wB
        for _ in range(max_ctrl_steps):
            simulator.make_step(u0.master)
            current_wB = float(simulator.data["_z", "e0_w_L_B_c1"][-1].item())
            # Break on tolerance OR target crossing.
            crossed: bool = (going_up and current_wB >= w_L_B_c1) or (
                not going_up and current_wB <= w_L_B_c1
            )
            if abs(current_wB - w_L_B_c1) <= wB_tol or crossed:
                break
            prev_wB = current_wB

        u0["e0_F_feed_tr9"] = 0.0
        u0["e0_x_feed_tr9_c1"] = 0.0
        u0["e0_x_feed_tr9_c2"] = 1.0

    # --- Phase 6a: hold ---
    for _ in range(n_steps):
        simulator.make_step(u0.master)

    # --- Phase 7: drive e0_LI to target ---
    li_tol: float = 0.01
    current_li: float = float(simulator.data["_z", "e0_LI"][-1].item())

    if abs(current_li - LI) > li_tol:
        li_going_up: bool = current_li < LI
        if li_going_up:
            u0["e0_F_feed_tr9"] = 1.0
        else:
            u0["e0_F_B"] = 1.0

        for _ in range(max_ctrl_steps):
            simulator.make_step(u0.master)
            current_li = float(simulator.data["_z", "e0_LI"][-1].item())
            li_crossed: bool = (li_going_up and current_li >= LI) or (
                not li_going_up and current_li <= LI
            )
            if abs(current_li - LI) <= li_tol or li_crossed:
                break

        u0["e0_F_feed_tr9"] = 0.0
        u0["e0_F_B"] = 0.0

    # --- Phase 8: hold ---
    for _ in range(n_steps):
        simulator.make_step(u0.master)

    return simulator


def extract_final_state(
    simulator: "do_mpc.simulator.Simulator",
) -> dict[str, dict[str, float]]:
    """Extract final x, z, u values from a do_mpc simulator trajectory.

    Returns a dict with keys ``"x"``, ``"z"``, ``"u"``, each mapping
    variable names to their final scalar values.  Use to seed another
    simulator via::

        state = extract_final_state(sim_done)
        for name, val in state["x"].items():
            sim_new.x0[name] = val
        for name, val in state["z"].items():
            sim_new.z0[name] = val
        for name, val in state["u"].items():
            sim_new.u0[name] = val

    Parameters
    ----------
    simulator : do_mpc.simulator.Simulator
        Simulator that has been run (has trajectory data).

    Returns
    -------
    dict[str, dict[str, float]]
        ``{"x": {name: value, ...}, "z": {...}, "u": {...}}``.
    """
    import numpy as np

    model = simulator.model

    def _extract(
        category: str,
        labels: list[str],
    ) -> dict[str, float]:
        out: dict[str, float] = {}
        for lbl in labels:
            name = lbl.strip("[]").split(",")[0]
            val = float(
                np.array(simulator.data[f"_{category}", name][-1]).flatten()[0]
            )
            out[name] = val
        return out

    return {
        "x": _extract("x", model._x.labels()),
        "z": _extract("z", model._z.labels()),
        "u": _extract("u", model._u.labels()),
    }


if __name__ == "__main__":
    from matplotlib import pyplot as plt

    simulator = simulate_init_recipe(
        E_murphree=0.65,
        rr_err=-0.10,
        LI=60.0,
        w_L_B_c1=0.25,
    )

    fig, ax, graphics = do_mpc.graphics.default_plot(
        simulator.data, dae_states_list=[], inputs_list=[]
    )
    plt.show()
