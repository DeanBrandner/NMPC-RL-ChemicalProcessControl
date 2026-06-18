import casadi as ca
import do_mpc
from matplotlib import pyplot as plt


def template_model(meas_noise_bool: bool = False) -> do_mpc.model.Model:
    """
    Here could be the doc
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
    e0_M_c1 = 0.046
    e0_M_c2 = 0.018
    e0_R = 8.314
    e0_T_ref = 298.15
    e0_c_V_p_c1 = 0.075
    e0_c_V_p_c2 = 0.036
    e0_d_col = 0.05
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

    # Parameters
    e0_p_tr0 = model.set_variable(var_type='_p', var_name="e0_p_tr0")  # noqa: E501
    e0_F_feed_tr9 = model.set_variable(var_type='_p', var_name="e0_F_feed_tr9")  # noqa: E501
    e0_F_B = model.set_variable(var_type='_p', var_name="e0_F_B")  # noqa: E501
    e0_T_feed = model.set_variable(var_type='_p', var_name="e0_T_feed")  # noqa: E501
    e0_V_tot_tr9 = model.set_variable(var_type='_p', var_name="e0_V_tot_tr9")  # noqa: E501
    e0_x_feed_tr9_c1 = model.set_variable(var_type='_p', var_name="e0_x_feed_tr9_c1")  # noqa: E501
    e0_x_feed_tr9_c2 = model.set_variable(var_type='_p', var_name="e0_x_feed_tr9_c2")  # noqa: E501
    e0_greek_lambda_activity = model.set_variable(var_type='_p', var_name="e0_greek_lambda_activity")  # noqa: E501
    e0_greek_kappa = model.set_variable(var_type='_p', var_name="e0_greek_kappa")  # noqa: E501
    e0_greek_kappa_hyst = model.set_variable(var_type='_p', var_name="e0_greek_kappa_hyst")  # noqa: E501
    e0_h_tot = model.set_variable(var_type='_p', var_name="e0_h_tot")  # noqa: E501

    # Uncertain parameters
    e0_Q_err_R = model.set_variable(var_type='_p', var_name="e0_Q_err_R")  # noqa: E501
    e0_rr_err = model.set_variable(var_type='_p', var_name="e0_rr_err")  # noqa: E501
    e0_E_murphree = model.set_variable(var_type='_p', var_name="e0_E_murphree")  # noqa: E501
    e0_x_N2 = model.set_variable(var_type='_p', var_name="e0_x_N2")  # noqa: E501
    e0_h_weir = model.set_variable(var_type='_p', var_name="e0_h_weir")  # noqa: E501

    # Measurements
    e0_LI_meas = model.set_meas(meas_name = "LI_meas", expr = e0_LI, meas_noise = meas_noise_bool)
    e0_WI_meas = model.set_meas(meas_name = "WI_meas", expr = e0_WI, meas_noise = meas_noise_bool)
    e0_w_L_D_c1_meas = model.set_meas(meas_name = "w_L_D_c1_meas", expr = e0_w_L_D_c1, meas_noise = meas_noise_bool)
    e0_w_L_B_c1_meas = model.set_meas(meas_name = "w_L_B_c1_meas", expr = e0_w_L_B_c1, meas_noise = meas_noise_bool)
    e0_T_tr9_meas = model.set_meas(meas_name = "T_tr9_meas", expr = e0_T_tr9, meas_noise = meas_noise_bool)


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
    EQ_alg255 = (e0_H_tr9-((e0_U_tr9+(e0_p_tr9*(((10.0))**(1.0*2.0)*e0_V_tot_tr9)))))  # noqa: E501,E226
    EQ_alg256 = (e0_H_tr9-(((e0_HU_L_tr9*e0_h_L_tr9)+(e0_HU_V_tr9*e0_h_V_tr9))))  # noqa: E501,E226
    EQ_alg257 = (e0_V_tot_tr9-((e0_V_L_tr9+e0_V_V_tr9)))  # noqa: E501,E226
    EQ_alg258 = (e0_V_L_tr9-((e0_HU_L_tr9*e0_v_L_tr9)))  # noqa: E501,E226
    EQ_alg259 = ((e0_p_tr9*(((10.0))**(1.0*5.0)*e0_V_V_tr9))-((e0_HU_V_tr9*(e0_R*e0_T_tr9))))  # noqa: E501,E226
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

# def template_model_for_pe(meas_noise_bool: bool = False) -> do_mpc.model.Model:
#     """
#     Here could be the doc
#     """
#     model_type = "continuous"  # either 'discrete' or 'continuous'
#     symvar_type = "SX"
#     model = do_mpc.model.Model(model_type, symvar_type)

#     # fmt:off
#     def fun_210593__vaporenthalpy(std_T,std_greek_Deltah_f,std_T_ref,std_c_V_p):  # noqa: E501,E231,E306
#         std_h_V = ((std_c_V_p*((std_T-std_T_ref)))+std_greek_Deltah_f)  # noqa: E501,E226
#         return std_h_V
#     def fun_213932__liquid_enthalpy_adj(std_T,std_greek_Deltah_f,std_A_LV,std_B_LV,std_C_LV,std_T_ref,std_c_V_p):  # noqa: E501,E231,E306
#         std_h_L = (((std_c_V_p*((std_T-std_T_ref)))+std_greek_Deltah_f)-(((std_A_LV+(std_B_LV*((std_T/std_T_ref))))+(std_C_LV*(((std_T/std_T_ref)))**(1.0*2.0)))))  # noqa: E501,E226
#         return std_h_L

#     # Constants
#     e0_greek_Deltah_f_c1 = -234.0
#     e0_greek_Deltah_f_c2 = -241.0
#     e0_greek_epsiv_weir = 1.0E-4
#     e0_greek_lambda_c1 = 95.68
#     e0_greek_lambda_c2 = 506.7
#     e0_greek_pi = 3.1415926
#     e0_A_c1 = 5.24677
#     e0_A_LV_c1 = 44.27270632
#     e0_A_c2 = 5.08354
#     e0_A_LV_c2 = 52.28384694
#     e0_B_c1 = 1598.673
#     e0_B_LV_c1 = 13.09430159
#     e0_B_c2 = 1663.125
#     e0_B_LV_c2 = -4.49906401
#     e0_C_c1 = -46.424
#     e0_C_LV_c1 = -14.78454201
#     e0_C_c2 = -45.622
#     e0_C_LV_c2 = -3.79895861
#     # e0_E_murphree = 0.7000000001071379
#     # e0_E_murphree = 0.5
#     # e0_E_murphree = 0.475
#     # e0_E_murphree = 0.65
#     e0_M_c1 = 0.046
#     e0_M_c2 = 0.018
#     # e0_Q_err_R = 0.98647356893109
#     e0_R = 8.314
#     e0_T_ref = 298.15
#     e0_c_V_p_c1 = 0.075
#     e0_c_V_p_c2 = 0.036
#     e0_d_col = 0.05
#     # e0_rr_err = -0.146549383828861
#     e0_v_L_c1 = 5.869E-5
#     e0_v_L_c2 = 1.813E-5
#     # e0_x_N2 = 0.04273159753760128
#     # e0_x_N2 = 0.04

#     # Dynamic/Differential states
#     e0_HU_tr1_c1 = model.set_variable(var_type='_x', var_name="e0_HU_tr1_c1", shape=(1,1))  # noqa: E501
#     e0_HU_tr2_c1 = model.set_variable(var_type='_x', var_name="e0_HU_tr2_c1", shape=(1,1))  # noqa: E501
#     e0_HU_tr3_c1 = model.set_variable(var_type='_x', var_name="e0_HU_tr3_c1", shape=(1,1))  # noqa: E501
#     e0_HU_tr4_c1 = model.set_variable(var_type='_x', var_name="e0_HU_tr4_c1", shape=(1,1))  # noqa: E501
#     e0_HU_tr5_c1 = model.set_variable(var_type='_x', var_name="e0_HU_tr5_c1", shape=(1,1))  # noqa: E501
#     e0_HU_tr6_c1 = model.set_variable(var_type='_x', var_name="e0_HU_tr6_c1", shape=(1,1))  # noqa: E501
#     e0_HU_tr7_c1 = model.set_variable(var_type='_x', var_name="e0_HU_tr7_c1", shape=(1,1))  # noqa: E501
#     e0_HU_tr8_c1 = model.set_variable(var_type='_x', var_name="e0_HU_tr8_c1", shape=(1,1))  # noqa: E501
#     e0_HU_tr1_c2 = model.set_variable(var_type='_x', var_name="e0_HU_tr1_c2", shape=(1,1))  # noqa: E501
#     e0_HU_tr2_c2 = model.set_variable(var_type='_x', var_name="e0_HU_tr2_c2", shape=(1,1))  # noqa: E501
#     e0_HU_tr3_c2 = model.set_variable(var_type='_x', var_name="e0_HU_tr3_c2", shape=(1,1))  # noqa: E501
#     e0_HU_tr4_c2 = model.set_variable(var_type='_x', var_name="e0_HU_tr4_c2", shape=(1,1))  # noqa: E501
#     e0_HU_tr5_c2 = model.set_variable(var_type='_x', var_name="e0_HU_tr5_c2", shape=(1,1))  # noqa: E501
#     e0_HU_tr6_c2 = model.set_variable(var_type='_x', var_name="e0_HU_tr6_c2", shape=(1,1))  # noqa: E501
#     e0_HU_tr7_c2 = model.set_variable(var_type='_x', var_name="e0_HU_tr7_c2", shape=(1,1))  # noqa: E501
#     e0_HU_tr8_c2 = model.set_variable(var_type='_x', var_name="e0_HU_tr8_c2", shape=(1,1))  # noqa: E501
#     e0_U_tr1 = model.set_variable(var_type='_x', var_name="e0_U_tr1", shape=(1,1))  # noqa: E501
#     e0_U_tr2 = model.set_variable(var_type='_x', var_name="e0_U_tr2", shape=(1,1))  # noqa: E501
#     e0_U_tr3 = model.set_variable(var_type='_x', var_name="e0_U_tr3", shape=(1,1))  # noqa: E501
#     e0_U_tr4 = model.set_variable(var_type='_x', var_name="e0_U_tr4", shape=(1,1))  # noqa: E501
#     e0_U_tr5 = model.set_variable(var_type='_x', var_name="e0_U_tr5", shape=(1,1))  # noqa: E501
#     e0_U_tr6 = model.set_variable(var_type='_x', var_name="e0_U_tr6", shape=(1,1))  # noqa: E501
#     e0_U_tr7 = model.set_variable(var_type='_x', var_name="e0_U_tr7", shape=(1,1))  # noqa: E501
#     e0_U_tr8 = model.set_variable(var_type='_x', var_name="e0_U_tr8", shape=(1,1))  # noqa: E501
#     e0_HU_tr9_c1 = model.set_variable(var_type='_x', var_name="e0_HU_tr9_c1", shape=(1,1))  # noqa: E501
#     e0_HU_tr9_c2 = model.set_variable(var_type='_x', var_name="e0_HU_tr9_c2", shape=(1,1))  # noqa: E501
#     e0_U_tr9 = model.set_variable(var_type='_x', var_name="e0_U_tr9", shape=(1,1))  # noqa: E501
#     e0_HU_D_c1 = model.set_variable(var_type='_x', var_name="e0_HU_D_c1", shape=(1,1))  # noqa: E501
#     e0_HU_D_c2 = model.set_variable(var_type='_x', var_name="e0_HU_D_c2", shape=(1,1))  # noqa: E501

#     # Algebraic states
#     e0_h_L_tr0_c1 = model.set_variable(var_type='_z', var_name="e0_h_L_tr0_c1", shape=(1,1))  # noqa: E501
#     e0_h_L_tr0_c2 = model.set_variable(var_type='_z', var_name="e0_h_L_tr0_c2", shape=(1,1))  # noqa: E501
#     e0_h_L_tr1_c1 = model.set_variable(var_type='_z', var_name="e0_h_L_tr1_c1", shape=(1,1))  # noqa: E501
#     e0_h_L_tr1_c2 = model.set_variable(var_type='_z', var_name="e0_h_L_tr1_c2", shape=(1,1))  # noqa: E501
#     e0_h_L_tr2_c1 = model.set_variable(var_type='_z', var_name="e0_h_L_tr2_c1", shape=(1,1))  # noqa: E501
#     e0_h_L_tr2_c2 = model.set_variable(var_type='_z', var_name="e0_h_L_tr2_c2", shape=(1,1))  # noqa: E501
#     e0_h_L_tr3_c1 = model.set_variable(var_type='_z', var_name="e0_h_L_tr3_c1", shape=(1,1))  # noqa: E501
#     e0_h_L_tr3_c2 = model.set_variable(var_type='_z', var_name="e0_h_L_tr3_c2", shape=(1,1))  # noqa: E501
#     e0_h_L_tr4_c1 = model.set_variable(var_type='_z', var_name="e0_h_L_tr4_c1", shape=(1,1))  # noqa: E501
#     e0_h_L_tr4_c2 = model.set_variable(var_type='_z', var_name="e0_h_L_tr4_c2", shape=(1,1))  # noqa: E501
#     e0_h_L_tr5_c1 = model.set_variable(var_type='_z', var_name="e0_h_L_tr5_c1", shape=(1,1))  # noqa: E501
#     e0_h_L_tr5_c2 = model.set_variable(var_type='_z', var_name="e0_h_L_tr5_c2", shape=(1,1))  # noqa: E501
#     e0_h_L_tr6_c1 = model.set_variable(var_type='_z', var_name="e0_h_L_tr6_c1", shape=(1,1))  # noqa: E501
#     e0_h_L_tr6_c2 = model.set_variable(var_type='_z', var_name="e0_h_L_tr6_c2", shape=(1,1))  # noqa: E501
#     e0_h_L_tr7_c1 = model.set_variable(var_type='_z', var_name="e0_h_L_tr7_c1", shape=(1,1))  # noqa: E501
#     e0_h_L_tr7_c2 = model.set_variable(var_type='_z', var_name="e0_h_L_tr7_c2", shape=(1,1))  # noqa: E501
#     e0_h_L_tr8_c1 = model.set_variable(var_type='_z', var_name="e0_h_L_tr8_c1", shape=(1,1))  # noqa: E501
#     e0_h_L_tr8_c2 = model.set_variable(var_type='_z', var_name="e0_h_L_tr8_c2", shape=(1,1))  # noqa: E501
#     e0_h_L_tr9_c1 = model.set_variable(var_type='_z', var_name="e0_h_L_tr9_c1", shape=(1,1))  # noqa: E501
#     e0_h_L_tr9_c2 = model.set_variable(var_type='_z', var_name="e0_h_L_tr9_c2", shape=(1,1))  # noqa: E501
#     e0_h_V_tr1_c1 = model.set_variable(var_type='_z', var_name="e0_h_V_tr1_c1", shape=(1,1))  # noqa: E501
#     e0_h_V_tr1_c2 = model.set_variable(var_type='_z', var_name="e0_h_V_tr1_c2", shape=(1,1))  # noqa: E501
#     e0_h_V_tr2_c1 = model.set_variable(var_type='_z', var_name="e0_h_V_tr2_c1", shape=(1,1))  # noqa: E501
#     e0_h_V_tr2_c2 = model.set_variable(var_type='_z', var_name="e0_h_V_tr2_c2", shape=(1,1))  # noqa: E501
#     e0_h_V_tr3_c1 = model.set_variable(var_type='_z', var_name="e0_h_V_tr3_c1", shape=(1,1))  # noqa: E501
#     e0_h_V_tr3_c2 = model.set_variable(var_type='_z', var_name="e0_h_V_tr3_c2", shape=(1,1))  # noqa: E501
#     e0_h_V_tr4_c1 = model.set_variable(var_type='_z', var_name="e0_h_V_tr4_c1", shape=(1,1))  # noqa: E501
#     e0_h_V_tr4_c2 = model.set_variable(var_type='_z', var_name="e0_h_V_tr4_c2", shape=(1,1))  # noqa: E501
#     e0_h_V_tr5_c1 = model.set_variable(var_type='_z', var_name="e0_h_V_tr5_c1", shape=(1,1))  # noqa: E501
#     e0_h_V_tr5_c2 = model.set_variable(var_type='_z', var_name="e0_h_V_tr5_c2", shape=(1,1))  # noqa: E501
#     e0_h_V_tr6_c1 = model.set_variable(var_type='_z', var_name="e0_h_V_tr6_c1", shape=(1,1))  # noqa: E501
#     e0_h_V_tr6_c2 = model.set_variable(var_type='_z', var_name="e0_h_V_tr6_c2", shape=(1,1))  # noqa: E501
#     e0_h_V_tr7_c1 = model.set_variable(var_type='_z', var_name="e0_h_V_tr7_c1", shape=(1,1))  # noqa: E501
#     e0_h_V_tr7_c2 = model.set_variable(var_type='_z', var_name="e0_h_V_tr7_c2", shape=(1,1))  # noqa: E501
#     e0_h_V_tr8_c1 = model.set_variable(var_type='_z', var_name="e0_h_V_tr8_c1", shape=(1,1))  # noqa: E501
#     e0_h_V_tr8_c2 = model.set_variable(var_type='_z', var_name="e0_h_V_tr8_c2", shape=(1,1))  # noqa: E501
#     e0_h_V_tr9_c1 = model.set_variable(var_type='_z', var_name="e0_h_V_tr9_c1", shape=(1,1))  # noqa: E501
#     e0_h_V_tr9_c2 = model.set_variable(var_type='_z', var_name="e0_h_V_tr9_c2", shape=(1,1))  # noqa: E501
#     e0_h_feed_tr9_c1 = model.set_variable(var_type='_z', var_name="e0_h_feed_tr9_c1", shape=(1,1))  # noqa: E501
#     e0_h_feed_tr9_c2 = model.set_variable(var_type='_z', var_name="e0_h_feed_tr9_c2", shape=(1,1))  # noqa: E501
#     e0_greek_alpha_tr0_c1 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr0_c1", shape=(1,1))  # noqa: E501
#     e0_greek_alpha_tr0_c2 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr0_c2", shape=(1,1))  # noqa: E501
#     e0_Q_C = model.set_variable(var_type='_z', var_name="e0_Q_C", shape=(1,1))  # noqa: E501
#     e0_H_tr3 = model.set_variable(var_type='_z', var_name="e0_H_tr3", shape=(1,1))  # noqa: E501
#     e0_H_tr4 = model.set_variable(var_type='_z', var_name="e0_H_tr4", shape=(1,1))  # noqa: E501
#     e0_H_tr5 = model.set_variable(var_type='_z', var_name="e0_H_tr5", shape=(1,1))  # noqa: E501
#     e0_H_tr6 = model.set_variable(var_type='_z', var_name="e0_H_tr6", shape=(1,1))  # noqa: E501
#     e0_H_tr7 = model.set_variable(var_type='_z', var_name="e0_H_tr7", shape=(1,1))  # noqa: E501
#     e0_H_tr8 = model.set_variable(var_type='_z', var_name="e0_H_tr8", shape=(1,1))  # noqa: E501
#     e0_T_tr0 = model.set_variable(var_type='_z', var_name="e0_T_tr0", shape=(1,1))  # noqa: E501
#     e0_HU_L_tr1 = model.set_variable(var_type='_z', var_name="e0_HU_L_tr1", shape=(1,1))  # noqa: E501
#     e0_HU_L_tr2 = model.set_variable(var_type='_z', var_name="e0_HU_L_tr2", shape=(1,1))  # noqa: E501
#     e0_HU_L_tr3 = model.set_variable(var_type='_z', var_name="e0_HU_L_tr3", shape=(1,1))  # noqa: E501
#     e0_HU_L_tr4 = model.set_variable(var_type='_z', var_name="e0_HU_L_tr4", shape=(1,1))  # noqa: E501
#     e0_HU_L_tr5 = model.set_variable(var_type='_z', var_name="e0_HU_L_tr5", shape=(1,1))  # noqa: E501
#     e0_HU_L_tr6 = model.set_variable(var_type='_z', var_name="e0_HU_L_tr6", shape=(1,1))  # noqa: E501
#     e0_HU_L_tr7 = model.set_variable(var_type='_z', var_name="e0_HU_L_tr7", shape=(1,1))  # noqa: E501
#     e0_HU_L_tr8 = model.set_variable(var_type='_z', var_name="e0_HU_L_tr8", shape=(1,1))  # noqa: E501
#     e0_HU_V_tr1 = model.set_variable(var_type='_z', var_name="e0_HU_V_tr1", shape=(1,1))  # noqa: E501
#     e0_HU_V_tr2 = model.set_variable(var_type='_z', var_name="e0_HU_V_tr2", shape=(1,1))  # noqa: E501
#     e0_HU_V_tr3 = model.set_variable(var_type='_z', var_name="e0_HU_V_tr3", shape=(1,1))  # noqa: E501
#     e0_HU_V_tr4 = model.set_variable(var_type='_z', var_name="e0_HU_V_tr4", shape=(1,1))  # noqa: E501
#     e0_HU_V_tr5 = model.set_variable(var_type='_z', var_name="e0_HU_V_tr5", shape=(1,1))  # noqa: E501
#     e0_HU_V_tr6 = model.set_variable(var_type='_z', var_name="e0_HU_V_tr6", shape=(1,1))  # noqa: E501
#     e0_HU_V_tr7 = model.set_variable(var_type='_z', var_name="e0_HU_V_tr7", shape=(1,1))  # noqa: E501
#     e0_HU_V_tr8 = model.set_variable(var_type='_z', var_name="e0_HU_V_tr8", shape=(1,1))  # noqa: E501
#     e0_K_tr1_c1 = model.set_variable(var_type='_z', var_name="e0_K_tr1_c1", shape=(1,1))  # noqa: E501
#     e0_K_tr2_c1 = model.set_variable(var_type='_z', var_name="e0_K_tr2_c1", shape=(1,1))  # noqa: E501
#     e0_h_L_tr0 = model.set_variable(var_type='_z', var_name="e0_h_L_tr0", shape=(1,1))  # noqa: E501
#     e0_K_tr3_c1 = model.set_variable(var_type='_z', var_name="e0_K_tr3_c1", shape=(1,1))  # noqa: E501
#     e0_K_tr4_c1 = model.set_variable(var_type='_z', var_name="e0_K_tr4_c1", shape=(1,1))  # noqa: E501
#     e0_K_tr5_c1 = model.set_variable(var_type='_z', var_name="e0_K_tr5_c1", shape=(1,1))  # noqa: E501
#     e0_K_tr6_c1 = model.set_variable(var_type='_z', var_name="e0_K_tr6_c1", shape=(1,1))  # noqa: E501
#     e0_K_tr7_c1 = model.set_variable(var_type='_z', var_name="e0_K_tr7_c1", shape=(1,1))  # noqa: E501
#     e0_K_tr8_c1 = model.set_variable(var_type='_z', var_name="e0_K_tr8_c1", shape=(1,1))  # noqa: E501
#     e0_K_tr1_c2 = model.set_variable(var_type='_z', var_name="e0_K_tr1_c2", shape=(1,1))  # noqa: E501
#     e0_K_tr2_c2 = model.set_variable(var_type='_z', var_name="e0_K_tr2_c2", shape=(1,1))  # noqa: E501
#     e0_K_tr3_c2 = model.set_variable(var_type='_z', var_name="e0_K_tr3_c2", shape=(1,1))  # noqa: E501
#     e0_K_tr4_c2 = model.set_variable(var_type='_z', var_name="e0_K_tr4_c2", shape=(1,1))  # noqa: E501
#     e0_h_V_tr1 = model.set_variable(var_type='_z', var_name="e0_h_V_tr1", shape=(1,1))  # noqa: E501
#     e0_K_tr5_c2 = model.set_variable(var_type='_z', var_name="e0_K_tr5_c2", shape=(1,1))  # noqa: E501
#     e0_K_tr6_c2 = model.set_variable(var_type='_z', var_name="e0_K_tr6_c2", shape=(1,1))  # noqa: E501
#     e0_K_tr7_c2 = model.set_variable(var_type='_z', var_name="e0_K_tr7_c2", shape=(1,1))  # noqa: E501
#     e0_K_tr8_c2 = model.set_variable(var_type='_z', var_name="e0_K_tr8_c2", shape=(1,1))  # noqa: E501
#     e0_L_tr1 = model.set_variable(var_type='_z', var_name="e0_L_tr1", shape=(1,1))  # noqa: E501
#     e0_L_tr2 = model.set_variable(var_type='_z', var_name="e0_L_tr2", shape=(1,1))  # noqa: E501
#     e0_L_tr3 = model.set_variable(var_type='_z', var_name="e0_L_tr3", shape=(1,1))  # noqa: E501
#     e0_L_tr4 = model.set_variable(var_type='_z', var_name="e0_L_tr4", shape=(1,1))  # noqa: E501
#     e0_L_tr5 = model.set_variable(var_type='_z', var_name="e0_L_tr5", shape=(1,1))  # noqa: E501
#     e0_L_tr6 = model.set_variable(var_type='_z', var_name="e0_L_tr6", shape=(1,1))  # noqa: E501
#     e0_L_tr7 = model.set_variable(var_type='_z', var_name="e0_L_tr7", shape=(1,1))  # noqa: E501
#     e0_L_tr8 = model.set_variable(var_type='_z', var_name="e0_L_tr8", shape=(1,1))  # noqa: E501
#     e0_L_weir = model.set_variable(var_type='_z', var_name="e0_L_weir", shape=(1,1))  # noqa: E501
#     e0_T_tr1 = model.set_variable(var_type='_z', var_name="e0_T_tr1", shape=(1,1))  # noqa: E501
#     e0_T_tr2 = model.set_variable(var_type='_z', var_name="e0_T_tr2", shape=(1,1))  # noqa: E501
#     e0_T_tr3 = model.set_variable(var_type='_z', var_name="e0_T_tr3", shape=(1,1))  # noqa: E501
#     e0_T_tr4 = model.set_variable(var_type='_z', var_name="e0_T_tr4", shape=(1,1))  # noqa: E501
#     e0_T_tr5 = model.set_variable(var_type='_z', var_name="e0_T_tr5", shape=(1,1))  # noqa: E501
#     e0_T_tr6 = model.set_variable(var_type='_z', var_name="e0_T_tr6", shape=(1,1))  # noqa: E501
#     e0_T_tr7 = model.set_variable(var_type='_z', var_name="e0_T_tr7", shape=(1,1))  # noqa: E501
#     e0_p_LV_o_tr0_c1 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr0_c1", shape=(1,1))  # noqa: E501
#     e0_T_tr8 = model.set_variable(var_type='_z', var_name="e0_T_tr8", shape=(1,1))  # noqa: E501
#     e0_V_L_tr1 = model.set_variable(var_type='_z', var_name="e0_V_L_tr1", shape=(1,1))  # noqa: E501
#     e0_p_LV_o_tr0_c2 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr0_c2", shape=(1,1))  # noqa: E501
#     e0_V_L_tr2 = model.set_variable(var_type='_z', var_name="e0_V_L_tr2", shape=(1,1))  # noqa: E501
#     e0_V_L_tr3 = model.set_variable(var_type='_z', var_name="e0_V_L_tr3", shape=(1,1))  # noqa: E501
#     e0_V_L_tr4 = model.set_variable(var_type='_z', var_name="e0_V_L_tr4", shape=(1,1))  # noqa: E501
#     e0_V_L_tr5 = model.set_variable(var_type='_z', var_name="e0_V_L_tr5", shape=(1,1))  # noqa: E501
#     e0_V_L_tr6 = model.set_variable(var_type='_z', var_name="e0_V_L_tr6", shape=(1,1))  # noqa: E501
#     e0_V_L_tr7 = model.set_variable(var_type='_z', var_name="e0_V_L_tr7", shape=(1,1))  # noqa: E501
#     e0_V_L_tr8 = model.set_variable(var_type='_z', var_name="e0_V_L_tr8", shape=(1,1))  # noqa: E501
#     e0_V_V_tr1 = model.set_variable(var_type='_z', var_name="e0_V_V_tr1", shape=(1,1))  # noqa: E501
#     e0_V_V_tr2 = model.set_variable(var_type='_z', var_name="e0_V_V_tr2", shape=(1,1))  # noqa: E501
#     e0_V_V_tr3 = model.set_variable(var_type='_z', var_name="e0_V_V_tr3", shape=(1,1))  # noqa: E501
#     e0_V_V_tr4 = model.set_variable(var_type='_z', var_name="e0_V_V_tr4", shape=(1,1))  # noqa: E501
#     e0_V_V_tr5 = model.set_variable(var_type='_z', var_name="e0_V_V_tr5", shape=(1,1))  # noqa: E501
#     e0_V_V_tr6 = model.set_variable(var_type='_z', var_name="e0_V_V_tr6", shape=(1,1))  # noqa: E501
#     e0_V_V_tr7 = model.set_variable(var_type='_z', var_name="e0_V_V_tr7", shape=(1,1))  # noqa: E501
#     e0_V_V_tr8 = model.set_variable(var_type='_z', var_name="e0_V_V_tr8", shape=(1,1))  # noqa: E501
#     e0_V_tot = model.set_variable(var_type='_z', var_name="e0_V_tot", shape=(1,1))  # noqa: E501
#     e0_greek_gamma_tr0_c1 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr0_c1", shape=(1,1))  # noqa: E501
#     e0_x_L_tr0_c1 = model.set_variable(var_type='_z', var_name="e0_x_L_tr0_c1", shape=(1,1))  # noqa: E501
#     e0_x_L_tr0_c2 = model.set_variable(var_type='_z', var_name="e0_x_L_tr0_c2", shape=(1,1))  # noqa: E501
#     e0_h_L_tr1 = model.set_variable(var_type='_z', var_name="e0_h_L_tr1", shape=(1,1))  # noqa: E501
#     e0_h_L_tr2 = model.set_variable(var_type='_z', var_name="e0_h_L_tr2", shape=(1,1))  # noqa: E501
#     e0_h_L_tr3 = model.set_variable(var_type='_z', var_name="e0_h_L_tr3", shape=(1,1))  # noqa: E501
#     e0_h_L_tr4 = model.set_variable(var_type='_z', var_name="e0_h_L_tr4", shape=(1,1))  # noqa: E501
#     e0_h_L_tr5 = model.set_variable(var_type='_z', var_name="e0_h_L_tr5", shape=(1,1))  # noqa: E501
#     e0_h_L_tr6 = model.set_variable(var_type='_z', var_name="e0_h_L_tr6", shape=(1,1))  # noqa: E501
#     e0_h_L_tr7 = model.set_variable(var_type='_z', var_name="e0_h_L_tr7", shape=(1,1))  # noqa: E501
#     e0_h_L_tr8 = model.set_variable(var_type='_z', var_name="e0_h_L_tr8", shape=(1,1))  # noqa: E501
#     e0_x_V_tr0_c1 = model.set_variable(var_type='_z', var_name="e0_x_V_tr0_c1", shape=(1,1))  # noqa: E501
#     e0_x_V_tr1_c1 = model.set_variable(var_type='_z', var_name="e0_x_V_tr1_c1", shape=(1,1))  # noqa: E501
#     e0_h_V_tr2 = model.set_variable(var_type='_z', var_name="e0_h_V_tr2", shape=(1,1))  # noqa: E501
#     e0_h_V_tr3 = model.set_variable(var_type='_z', var_name="e0_h_V_tr3", shape=(1,1))  # noqa: E501
#     e0_h_V_tr4 = model.set_variable(var_type='_z', var_name="e0_h_V_tr4", shape=(1,1))  # noqa: E501
#     e0_h_V_tr5 = model.set_variable(var_type='_z', var_name="e0_h_V_tr5", shape=(1,1))  # noqa: E501
#     e0_x_V_tr0_c2 = model.set_variable(var_type='_z', var_name="e0_x_V_tr0_c2", shape=(1,1))  # noqa: E501
#     e0_h_V_tr6 = model.set_variable(var_type='_z', var_name="e0_h_V_tr6", shape=(1,1))  # noqa: E501
#     e0_h_V_tr7 = model.set_variable(var_type='_z', var_name="e0_h_V_tr7", shape=(1,1))  # noqa: E501
#     e0_h_V_tr8 = model.set_variable(var_type='_z', var_name="e0_h_V_tr8", shape=(1,1))  # noqa: E501
#     e0_h_V_tr9 = model.set_variable(var_type='_z', var_name="e0_h_V_tr9", shape=(1,1))  # noqa: E501
#     e0_p_tr1 = model.set_variable(var_type='_z', var_name="e0_p_tr1", shape=(1,1))  # noqa: E501
#     e0_p_tr2 = model.set_variable(var_type='_z', var_name="e0_p_tr2", shape=(1,1))  # noqa: E501
#     e0_p_tr3 = model.set_variable(var_type='_z', var_name="e0_p_tr3", shape=(1,1))  # noqa: E501
#     e0_p_tr4 = model.set_variable(var_type='_z', var_name="e0_p_tr4", shape=(1,1))  # noqa: E501
#     e0_p_tr5 = model.set_variable(var_type='_z', var_name="e0_p_tr5", shape=(1,1))  # noqa: E501
#     e0_p_tr6 = model.set_variable(var_type='_z', var_name="e0_p_tr6", shape=(1,1))  # noqa: E501
#     e0_x_V_tr1_c2 = model.set_variable(var_type='_z', var_name="e0_x_V_tr1_c2", shape=(1,1))  # noqa: E501
#     e0_p_tr7 = model.set_variable(var_type='_z', var_name="e0_p_tr7", shape=(1,1))  # noqa: E501
#     e0_p_tr8 = model.set_variable(var_type='_z', var_name="e0_p_tr8", shape=(1,1))  # noqa: E501
#     e0_p_LV_o_tr1_c1 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr1_c1", shape=(1,1))  # noqa: E501
#     e0_p_LV_o_tr2_c1 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr2_c1", shape=(1,1))  # noqa: E501
#     e0_p_LV_o_tr3_c1 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr3_c1", shape=(1,1))  # noqa: E501
#     e0_p_LV_o_tr4_c1 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr4_c1", shape=(1,1))  # noqa: E501
#     e0_p_LV_o_tr5_c1 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr5_c1", shape=(1,1))  # noqa: E501
#     e0_p_LV_o_tr6_c1 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr6_c1", shape=(1,1))  # noqa: E501
#     e0_p_LV_o_tr7_c1 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr7_c1", shape=(1,1))  # noqa: E501
#     e0_p_LV_o_tr8_c1 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr8_c1", shape=(1,1))  # noqa: E501
#     e0_p_LV_o_tr1_c2 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr1_c2", shape=(1,1))  # noqa: E501
#     e0_p_LV_o_tr2_c2 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr2_c2", shape=(1,1))  # noqa: E501
#     e0_p_LV_o_tr3_c2 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr3_c2", shape=(1,1))  # noqa: E501
#     e0_p_LV_o_tr4_c2 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr4_c2", shape=(1,1))  # noqa: E501
#     e0_p_LV_o_tr5_c2 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr5_c2", shape=(1,1))  # noqa: E501
#     e0_p_LV_o_tr6_c2 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr6_c2", shape=(1,1))  # noqa: E501
#     e0_p_LV_o_tr7_c2 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr7_c2", shape=(1,1))  # noqa: E501
#     e0_p_LV_o_tr8_c2 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr8_c2", shape=(1,1))  # noqa: E501
#     e0_v_L_tr1 = model.set_variable(var_type='_z', var_name="e0_v_L_tr1", shape=(1,1))  # noqa: E501
#     e0_v_L_tr2 = model.set_variable(var_type='_z', var_name="e0_v_L_tr2", shape=(1,1))  # noqa: E501
#     e0_v_L_tr3 = model.set_variable(var_type='_z', var_name="e0_v_L_tr3", shape=(1,1))  # noqa: E501
#     e0_v_L_tr4 = model.set_variable(var_type='_z', var_name="e0_v_L_tr4", shape=(1,1))  # noqa: E501
#     e0_v_L_tr5 = model.set_variable(var_type='_z', var_name="e0_v_L_tr5", shape=(1,1))  # noqa: E501
#     e0_v_L_tr6 = model.set_variable(var_type='_z', var_name="e0_v_L_tr6", shape=(1,1))  # noqa: E501
#     e0_v_L_tr7 = model.set_variable(var_type='_z', var_name="e0_v_L_tr7", shape=(1,1))  # noqa: E501
#     e0_v_L_tr8 = model.set_variable(var_type='_z', var_name="e0_v_L_tr8", shape=(1,1))  # noqa: E501
#     e0_x_L_tr1_c1 = model.set_variable(var_type='_z', var_name="e0_x_L_tr1_c1", shape=(1,1))  # noqa: E501
#     e0_x_L_tr2_c1 = model.set_variable(var_type='_z', var_name="e0_x_L_tr2_c1", shape=(1,1))  # noqa: E501
#     e0_x_L_tr3_c1 = model.set_variable(var_type='_z', var_name="e0_x_L_tr3_c1", shape=(1,1))  # noqa: E501
#     e0_x_L_tr4_c1 = model.set_variable(var_type='_z', var_name="e0_x_L_tr4_c1", shape=(1,1))  # noqa: E501
#     e0_x_L_tr5_c1 = model.set_variable(var_type='_z', var_name="e0_x_L_tr5_c1", shape=(1,1))  # noqa: E501
#     e0_x_L_tr6_c1 = model.set_variable(var_type='_z', var_name="e0_x_L_tr6_c1", shape=(1,1))  # noqa: E501
#     e0_x_L_tr7_c1 = model.set_variable(var_type='_z', var_name="e0_x_L_tr7_c1", shape=(1,1))  # noqa: E501
#     e0_x_L_tr8_c1 = model.set_variable(var_type='_z', var_name="e0_x_L_tr8_c1", shape=(1,1))  # noqa: E501
#     e0_x_L_tr1_c2 = model.set_variable(var_type='_z', var_name="e0_x_L_tr1_c2", shape=(1,1))  # noqa: E501
#     e0_x_L_tr2_c2 = model.set_variable(var_type='_z', var_name="e0_x_L_tr2_c2", shape=(1,1))  # noqa: E501
#     e0_x_L_tr3_c2 = model.set_variable(var_type='_z', var_name="e0_x_L_tr3_c2", shape=(1,1))  # noqa: E501
#     e0_x_L_tr4_c2 = model.set_variable(var_type='_z', var_name="e0_x_L_tr4_c2", shape=(1,1))  # noqa: E501
#     e0_x_L_tr5_c2 = model.set_variable(var_type='_z', var_name="e0_x_L_tr5_c2", shape=(1,1))  # noqa: E501
#     e0_x_L_tr6_c2 = model.set_variable(var_type='_z', var_name="e0_x_L_tr6_c2", shape=(1,1))  # noqa: E501
#     e0_x_L_tr7_c2 = model.set_variable(var_type='_z', var_name="e0_x_L_tr7_c2", shape=(1,1))  # noqa: E501
#     e0_x_L_tr8_c2 = model.set_variable(var_type='_z', var_name="e0_x_L_tr8_c2", shape=(1,1))  # noqa: E501
#     e0_x_V_tr2_c1 = model.set_variable(var_type='_z', var_name="e0_x_V_tr2_c1", shape=(1,1))  # noqa: E501
#     e0_x_V_tr3_c1 = model.set_variable(var_type='_z', var_name="e0_x_V_tr3_c1", shape=(1,1))  # noqa: E501
#     e0_x_V_tr4_c1 = model.set_variable(var_type='_z', var_name="e0_x_V_tr4_c1", shape=(1,1))  # noqa: E501
#     e0_x_V_tr5_c1 = model.set_variable(var_type='_z', var_name="e0_x_V_tr5_c1", shape=(1,1))  # noqa: E501
#     e0_x_V_tr6_c1 = model.set_variable(var_type='_z', var_name="e0_x_V_tr6_c1", shape=(1,1))  # noqa: E501
#     e0_x_V_tr7_c1 = model.set_variable(var_type='_z', var_name="e0_x_V_tr7_c1", shape=(1,1))  # noqa: E501
#     e0_x_V_tr8_c1 = model.set_variable(var_type='_z', var_name="e0_x_V_tr8_c1", shape=(1,1))  # noqa: E501
#     e0_greek_gamma_tr0_c2 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr0_c2", shape=(1,1))  # noqa: E501
#     e0_x_V_tr9_c1 = model.set_variable(var_type='_z', var_name="e0_x_V_tr9_c1", shape=(1,1))  # noqa: E501
#     e0_x_V_tr2_c2 = model.set_variable(var_type='_z', var_name="e0_x_V_tr2_c2", shape=(1,1))  # noqa: E501
#     e0_x_V_tr3_c2 = model.set_variable(var_type='_z', var_name="e0_x_V_tr3_c2", shape=(1,1))  # noqa: E501
#     e0_x_V_tr4_c2 = model.set_variable(var_type='_z', var_name="e0_x_V_tr4_c2", shape=(1,1))  # noqa: E501
#     e0_x_V_tr5_c2 = model.set_variable(var_type='_z', var_name="e0_x_V_tr5_c2", shape=(1,1))  # noqa: E501
#     e0_x_V_tr6_c2 = model.set_variable(var_type='_z', var_name="e0_x_V_tr6_c2", shape=(1,1))  # noqa: E501
#     e0_x_V_tr7_c2 = model.set_variable(var_type='_z', var_name="e0_x_V_tr7_c2", shape=(1,1))  # noqa: E501
#     e0_x_V_tr8_c2 = model.set_variable(var_type='_z', var_name="e0_x_V_tr8_c2", shape=(1,1))  # noqa: E501
#     e0_x_V_tr9_c2 = model.set_variable(var_type='_z', var_name="e0_x_V_tr9_c2", shape=(1,1))  # noqa: E501
#     e0_greek_alpha_tr9_c1 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr9_c1", shape=(1,1))  # noqa: E501
#     e0_greek_alpha_tr9_c2 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr9_c2", shape=(1,1))  # noqa: E501
#     e0_greek_gamma_tr9_c1 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr9_c1", shape=(1,1))  # noqa: E501
#     e0_greek_gamma_tr9_c2 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr9_c2", shape=(1,1))  # noqa: E501
#     e0_H_tr9 = model.set_variable(var_type='_z', var_name="e0_H_tr9", shape=(1,1))  # noqa: E501
#     e0_HU_L_tr9 = model.set_variable(var_type='_z', var_name="e0_HU_L_tr9", shape=(1,1))  # noqa: E501
#     e0_HU_V_tr9 = model.set_variable(var_type='_z', var_name="e0_HU_V_tr9", shape=(1,1))  # noqa: E501
#     e0_K_tr9_c1 = model.set_variable(var_type='_z', var_name="e0_K_tr9_c1", shape=(1,1))  # noqa: E501
#     e0_K_tr9_c2 = model.set_variable(var_type='_z', var_name="e0_K_tr9_c2", shape=(1,1))  # noqa: E501
#     e0_T_tr9 = model.set_variable(var_type='_z', var_name="e0_T_tr9", shape=(1,1))  # noqa: E501
#     e0_V_L_tr9 = model.set_variable(var_type='_z', var_name="e0_V_L_tr9", shape=(1,1))  # noqa: E501
#     e0_V_V_tr9 = model.set_variable(var_type='_z', var_name="e0_V_V_tr9", shape=(1,1))  # noqa: E501
#     e0_h_L_tr9 = model.set_variable(var_type='_z', var_name="e0_h_L_tr9", shape=(1,1))  # noqa: E501
#     e0_h_feed_tr9 = model.set_variable(var_type='_z', var_name="e0_h_feed_tr9", shape=(1,1))  # noqa: E501
#     e0_p_tr9 = model.set_variable(var_type='_z', var_name="e0_p_tr9", shape=(1,1))  # noqa: E501
#     e0_p_LV_o_tr9_c1 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr9_c1", shape=(1,1))  # noqa: E501
#     e0_p_LV_o_tr9_c2 = model.set_variable(var_type='_z', var_name="e0_p_LV_o_tr9_c2", shape=(1,1))  # noqa: E501
#     e0_v_L_tr9 = model.set_variable(var_type='_z', var_name="e0_v_L_tr9", shape=(1,1))  # noqa: E501
#     e0_x_L_tr9_c1 = model.set_variable(var_type='_z', var_name="e0_x_L_tr9_c1", shape=(1,1))  # noqa: E501
#     e0_x_L_tr9_c2 = model.set_variable(var_type='_z', var_name="e0_x_L_tr9_c2", shape=(1,1))  # noqa: E501
#     e0_LI = model.set_variable(var_type='_z', var_name="e0_LI", shape=(1,1))  # noqa: E501
#     e0_M_D = model.set_variable(var_type='_z', var_name="e0_M_D", shape=(1,1))  # noqa: E501
#     e0_M_D_c1 = model.set_variable(var_type='_z', var_name="e0_M_D_c1", shape=(1,1))  # noqa: E501
#     e0_M_D_c2 = model.set_variable(var_type='_z', var_name="e0_M_D_c2", shape=(1,1))  # noqa: E501
#     e0_PDI = model.set_variable(var_type='_z', var_name="e0_PDI", shape=(1,1))  # noqa: E501
#     e0_PI_B = model.set_variable(var_type='_z', var_name="e0_PI_B", shape=(1,1))  # noqa: E501
#     e0_PI_C = model.set_variable(var_type='_z', var_name="e0_PI_C", shape=(1,1))  # noqa: E501
#     e0_WI = model.set_variable(var_type='_z', var_name="e0_WI", shape=(1,1))  # noqa: E501
#     e0_w_L_B_c1 = model.set_variable(var_type='_z', var_name="e0_w_L_B_c1", shape=(1,1))  # noqa: E501
#     e0_w_L_B_c2 = model.set_variable(var_type='_z', var_name="e0_w_L_B_c2", shape=(1,1))  # noqa: E501
#     e0_w_L_C_c1 = model.set_variable(var_type='_z', var_name="e0_w_L_C_c1", shape=(1,1))  # noqa: E501
#     e0_w_L_C_c2 = model.set_variable(var_type='_z', var_name="e0_w_L_C_c2", shape=(1,1))  # noqa: E501
#     e0_w_L_D_c1 = model.set_variable(var_type='_z', var_name="e0_w_L_D_c1", shape=(1,1))  # noqa: E501
#     e0_w_L_D_c2 = model.set_variable(var_type='_z', var_name="e0_w_L_D_c2", shape=(1,1))  # noqa: E501
#     # e0_Q_PLS_R = model.set_variable(var_type='_z', var_name="e0_Q_PLS_R", shape=(1,1))  # noqa: E501
#     # e0_rr_PLS = model.set_variable(var_type='_z', var_name="e0_rr_PLS", shape=(1,1))  # noqa: E501
#     e0_greek_alpha_tr1_c1 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr1_c1", shape=(1,1))  # noqa: E501
#     e0_greek_alpha_tr2_c1 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr2_c1", shape=(1,1))  # noqa: E501
#     e0_F_L_tr0 = model.set_variable(var_type='_z', var_name="e0_F_L_tr0", shape=(1,1))  # noqa: E501
#     e0_greek_alpha_tr3_c1 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr3_c1", shape=(1,1))  # noqa: E501
#     e0_greek_alpha_tr4_c1 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr4_c1", shape=(1,1))  # noqa: E501
#     e0_greek_alpha_tr5_c1 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr5_c1", shape=(1,1))  # noqa: E501
#     e0_greek_alpha_tr6_c1 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr6_c1", shape=(1,1))  # noqa: E501
#     e0_greek_alpha_tr7_c1 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr7_c1", shape=(1,1))  # noqa: E501
#     e0_greek_alpha_tr8_c1 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr8_c1", shape=(1,1))  # noqa: E501
#     e0_greek_alpha_tr1_c2 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr1_c2", shape=(1,1))  # noqa: E501
#     e0_greek_alpha_tr2_c2 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr2_c2", shape=(1,1))  # noqa: E501
#     e0_greek_alpha_tr3_c2 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr3_c2", shape=(1,1))  # noqa: E501
#     e0_greek_alpha_tr4_c2 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr4_c2", shape=(1,1))  # noqa: E501
#     e0_F_V_tr1 = model.set_variable(var_type='_z', var_name="e0_F_V_tr1", shape=(1,1))  # noqa: E501
#     e0_greek_alpha_tr5_c2 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr5_c2", shape=(1,1))  # noqa: E501
#     e0_greek_alpha_tr6_c2 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr6_c2", shape=(1,1))  # noqa: E501
#     e0_greek_alpha_tr7_c2 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr7_c2", shape=(1,1))  # noqa: E501
#     e0_greek_alpha_tr8_c2 = model.set_variable(var_type='_z', var_name="e0_greek_alpha_tr8_c2", shape=(1,1))  # noqa: E501
#     e0_greek_gamma_tr1_c1 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr1_c1", shape=(1,1))  # noqa: E501
#     e0_greek_gamma_tr2_c1 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr2_c1", shape=(1,1))  # noqa: E501
#     e0_greek_gamma_tr3_c1 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr3_c1", shape=(1,1))  # noqa: E501
#     e0_greek_gamma_tr4_c1 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr4_c1", shape=(1,1))  # noqa: E501
#     e0_greek_gamma_tr5_c1 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr5_c1", shape=(1,1))  # noqa: E501
#     e0_greek_gamma_tr6_c1 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr6_c1", shape=(1,1))  # noqa: E501
#     e0_F_D = model.set_variable(var_type='_z', var_name="e0_F_D", shape=(1,1))  # noqa: E501
#     e0_greek_gamma_tr7_c1 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr7_c1", shape=(1,1))  # noqa: E501
#     e0_greek_gamma_tr8_c1 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr8_c1", shape=(1,1))  # noqa: E501
#     e0_greek_gamma_tr1_c2 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr1_c2", shape=(1,1))  # noqa: E501
#     e0_greek_gamma_tr2_c2 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr2_c2", shape=(1,1))  # noqa: E501
#     e0_greek_gamma_tr3_c2 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr3_c2", shape=(1,1))  # noqa: E501
#     e0_greek_gamma_tr4_c2 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr4_c2", shape=(1,1))  # noqa: E501
#     e0_greek_gamma_tr5_c2 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr5_c2", shape=(1,1))  # noqa: E501
#     e0_greek_gamma_tr6_c2 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr6_c2", shape=(1,1))  # noqa: E501
#     e0_greek_gamma_tr7_c2 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr7_c2", shape=(1,1))  # noqa: E501
#     e0_greek_gamma_tr8_c2 = model.set_variable(var_type='_z', var_name="e0_greek_gamma_tr8_c2", shape=(1,1))  # noqa: E501
#     e0_K_tr0_c1 = model.set_variable(var_type='_z', var_name="e0_K_tr0_c1", shape=(1,1))  # noqa: E501
#     e0_A_col = model.set_variable(var_type='_z', var_name="e0_A_col", shape=(1,1))  # noqa: E501
#     e0_A_active = model.set_variable(var_type='_z', var_name="e0_A_active", shape=(1,1))  # noqa: E501
#     e0_F_L_tr1 = model.set_variable(var_type='_z', var_name="e0_F_L_tr1", shape=(1,1))  # noqa: E501
#     e0_F_L_tr2 = model.set_variable(var_type='_z', var_name="e0_F_L_tr2", shape=(1,1))  # noqa: E501
#     e0_F_L_tr3 = model.set_variable(var_type='_z', var_name="e0_F_L_tr3", shape=(1,1))  # noqa: E501
#     e0_F_L_tr4 = model.set_variable(var_type='_z', var_name="e0_F_L_tr4", shape=(1,1))  # noqa: E501
#     e0_F_L_tr5 = model.set_variable(var_type='_z', var_name="e0_F_L_tr5", shape=(1,1))  # noqa: E501
#     e0_F_L_tr6 = model.set_variable(var_type='_z', var_name="e0_F_L_tr6", shape=(1,1))  # noqa: E501
#     e0_F_L_tr7 = model.set_variable(var_type='_z', var_name="e0_F_L_tr7", shape=(1,1))  # noqa: E501
#     e0_F_L_tr8 = model.set_variable(var_type='_z', var_name="e0_F_L_tr8", shape=(1,1))  # noqa: E501
#     e0_K_tr0_c2 = model.set_variable(var_type='_z', var_name="e0_K_tr0_c2", shape=(1,1))  # noqa: E501
#     e0_F_V_tr2 = model.set_variable(var_type='_z', var_name="e0_F_V_tr2", shape=(1,1))  # noqa: E501
#     e0_F_V_tr3 = model.set_variable(var_type='_z', var_name="e0_F_V_tr3", shape=(1,1))  # noqa: E501
#     e0_F_V_tr4 = model.set_variable(var_type='_z', var_name="e0_F_V_tr4", shape=(1,1))  # noqa: E501
#     e0_F_V_tr5 = model.set_variable(var_type='_z', var_name="e0_F_V_tr5", shape=(1,1))  # noqa: E501
#     e0_F_V_tr6 = model.set_variable(var_type='_z', var_name="e0_F_V_tr6", shape=(1,1))  # noqa: E501
#     e0_F_V_tr7 = model.set_variable(var_type='_z', var_name="e0_F_V_tr7", shape=(1,1))  # noqa: E501
#     e0_F_V_tr8 = model.set_variable(var_type='_z', var_name="e0_F_V_tr8", shape=(1,1))  # noqa: E501
#     e0_F_V_tr9 = model.set_variable(var_type='_z', var_name="e0_F_V_tr9", shape=(1,1))  # noqa: E501
#     e0_H_tr1 = model.set_variable(var_type='_z', var_name="e0_H_tr1", shape=(1,1))  # noqa: E501
#     e0_H_tr2 = model.set_variable(var_type='_z', var_name="e0_H_tr2", shape=(1,1))  # noqa: E501

#     # Control inputs
#     e0_rr = model.set_variable(var_type='_z', var_name="e0_rr")  # noqa: E501
#     e0_rr_PLS = model.set_variable(var_type='_u', var_name="e0_rr_PLS", shape=(1,1))  # noqa: E501
#     e0_Q_R = model.set_variable(var_type='_z', var_name="e0_Q_R")  # noqa: E501
#     e0_Q_PLS_R = model.set_variable(var_type='_u', var_name="e0_Q_PLS_R", shape=(1,1))  # noqa: E501

#     # Previously implement as control inputs. Now they are treated as parameters
#     e0_p_tr0 = model.set_variable(var_type='_p', var_name="e0_p_tr0")  # noqa: E501
#     e0_F_feed_tr9 = model.set_variable(var_type='_p', var_name="e0_F_feed_tr9")  # noqa: E501
#     e0_F_B = model.set_variable(var_type='_p', var_name="e0_F_B")  # noqa: E501
#     e0_T_feed = model.set_variable(var_type='_p', var_name="e0_T_feed")  # noqa: E501
#     e0_V_tot_tr9 = model.set_variable(var_type='_p', var_name="e0_V_tot_tr9")  # noqa: E501
#     e0_x_feed_tr9_c1 = model.set_variable(var_type='_p', var_name="e0_x_feed_tr9_c1")  # noqa: E501
#     e0_x_feed_tr9_c2 = model.set_variable(var_type='_p', var_name="e0_x_feed_tr9_c2")  # noqa: E501
#     e0_greek_lambda_activity = model.set_variable(var_type='_p', var_name="e0_greek_lambda_activity")  # noqa: E501

#     # Parameters 
#     e0_greek_kappa = model.set_variable(var_type='_p', var_name="e0_greek_kappa")  # noqa: E501
#     e0_greek_kappa_hyst = model.set_variable(var_type='_p', var_name="e0_greek_kappa_hyst")  # noqa: E501
#     e0_h_tot = model.set_variable(var_type='_p', var_name="e0_h_tot")  # noqa: E501
#     e0_h_weir = model.set_variable(var_type='_p', var_name="e0_h_weir")  # noqa: E501

#     # Uncertain parameters
#     # e0_Q_err_R = 0.98647356893109
#     # e0_rr_err = -0.146549383828861
#     e0_Q_err_R = model.set_variable(var_type='_p', var_name="e0_Q_err_R")  # noqa: E501
#     e0_rr_err = model.set_variable(var_type='_p', var_name="e0_rr_err")  # noqa: E501
#     e0_E_murphree = model.set_variable(var_type='_p', var_name="e0_E_murphree")  # noqa: E501
#     e0_x_N2 = model.set_variable(var_type='_p', var_name="e0_x_N2")  # noqa: E501

#     # Measurements
#     e0_LI_meas = model.set_meas(meas_name = "LI_meas", expr = e0_LI, meas_noise = meas_noise_bool)
#     e0_WI_meas = model.set_meas(meas_name = "WI_meas", expr = e0_WI, meas_noise = meas_noise_bool)
#     e0_w_L_D_c1_meas = model.set_meas(meas_name = "w_L_D_c1_meas", expr = e0_w_L_D_c1, meas_noise = meas_noise_bool)
#     e0_w_L_B_c1_meas = model.set_meas(meas_name = "w_L_B_c1_meas", expr = e0_w_L_B_c1, meas_noise = meas_noise_bool)
#     e0_T_tr9_meas = model.set_meas(meas_name = "T_tr9_meas", expr = e0_T_tr9, meas_noise = meas_noise_bool)

#     e0_Q_PLS_R_meas = model.set_meas(meas_name = "e0_Q_PLS_R", expr = e0_Q_PLS_R, meas_noise = False)
#     e0_rr_PLS_meas = model.set_meas(meas_name = "e0_rr_PLS", expr = e0_rr_PLS, meas_noise = False)


#     # Differential equations
#     EQ_diff1 = ((((e0_F_L_tr0*e0_x_L_tr0_c1)-(e0_F_L_tr1*e0_x_L_tr1_c1))+(e0_F_V_tr2*e0_x_V_tr2_c1))-(e0_F_V_tr1*e0_x_V_tr1_c1))  # noqa: E501,E226
#     EQ_diff2 = ((((e0_F_L_tr1*e0_x_L_tr1_c1)-(e0_F_L_tr2*e0_x_L_tr2_c1))+(e0_F_V_tr3*e0_x_V_tr3_c1))-(e0_F_V_tr2*e0_x_V_tr2_c1))  # noqa: E501,E226
#     EQ_diff3 = ((((e0_F_L_tr2*e0_x_L_tr2_c1)-(e0_F_L_tr3*e0_x_L_tr3_c1))+(e0_F_V_tr4*e0_x_V_tr4_c1))-(e0_F_V_tr3*e0_x_V_tr3_c1))  # noqa: E501,E226
#     EQ_diff4 = ((((e0_F_L_tr3*e0_x_L_tr3_c1)-(e0_F_L_tr4*e0_x_L_tr4_c1))+(e0_F_V_tr5*e0_x_V_tr5_c1))-(e0_F_V_tr4*e0_x_V_tr4_c1))  # noqa: E501,E226
#     EQ_diff5 = ((((e0_F_L_tr4*e0_x_L_tr4_c1)-(e0_F_L_tr5*e0_x_L_tr5_c1))+(e0_F_V_tr6*e0_x_V_tr6_c1))-(e0_F_V_tr5*e0_x_V_tr5_c1))  # noqa: E501,E226
#     EQ_diff6 = ((((e0_F_L_tr5*e0_x_L_tr5_c1)-(e0_F_L_tr6*e0_x_L_tr6_c1))+(e0_F_V_tr7*e0_x_V_tr7_c1))-(e0_F_V_tr6*e0_x_V_tr6_c1))  # noqa: E501,E226
#     EQ_diff7 = ((((e0_F_L_tr6*e0_x_L_tr6_c1)-(e0_F_L_tr7*e0_x_L_tr7_c1))+(e0_F_V_tr8*e0_x_V_tr8_c1))-(e0_F_V_tr7*e0_x_V_tr7_c1))  # noqa: E501,E226
#     EQ_diff8 = ((((e0_F_L_tr7*e0_x_L_tr7_c1)-(e0_F_L_tr8*e0_x_L_tr8_c1))+(e0_F_V_tr9*e0_x_V_tr9_c1))-(e0_F_V_tr8*e0_x_V_tr8_c1))  # noqa: E501,E226
#     EQ_diff9 = ((((e0_F_L_tr0*e0_x_L_tr0_c2)-(e0_F_L_tr1*e0_x_L_tr1_c2))+(e0_F_V_tr2*e0_x_V_tr2_c2))-(e0_F_V_tr1*e0_x_V_tr1_c2))  # noqa: E501,E226
#     EQ_diff10 = ((((e0_F_L_tr1*e0_x_L_tr1_c2)-(e0_F_L_tr2*e0_x_L_tr2_c2))+(e0_F_V_tr3*e0_x_V_tr3_c2))-(e0_F_V_tr2*e0_x_V_tr2_c2))  # noqa: E501,E226
#     EQ_diff11 = ((((e0_F_L_tr2*e0_x_L_tr2_c2)-(e0_F_L_tr3*e0_x_L_tr3_c2))+(e0_F_V_tr4*e0_x_V_tr4_c2))-(e0_F_V_tr3*e0_x_V_tr3_c2))  # noqa: E501,E226
#     EQ_diff12 = ((((e0_F_L_tr3*e0_x_L_tr3_c2)-(e0_F_L_tr4*e0_x_L_tr4_c2))+(e0_F_V_tr5*e0_x_V_tr5_c2))-(e0_F_V_tr4*e0_x_V_tr4_c2))  # noqa: E501,E226
#     EQ_diff13 = ((((e0_F_L_tr4*e0_x_L_tr4_c2)-(e0_F_L_tr5*e0_x_L_tr5_c2))+(e0_F_V_tr6*e0_x_V_tr6_c2))-(e0_F_V_tr5*e0_x_V_tr5_c2))  # noqa: E501,E226
#     EQ_diff14 = ((((e0_F_L_tr5*e0_x_L_tr5_c2)-(e0_F_L_tr6*e0_x_L_tr6_c2))+(e0_F_V_tr7*e0_x_V_tr7_c2))-(e0_F_V_tr6*e0_x_V_tr6_c2))  # noqa: E501,E226
#     EQ_diff15 = ((((e0_F_L_tr6*e0_x_L_tr6_c2)-(e0_F_L_tr7*e0_x_L_tr7_c2))+(e0_F_V_tr8*e0_x_V_tr8_c2))-(e0_F_V_tr7*e0_x_V_tr7_c2))  # noqa: E501,E226
#     EQ_diff16 = ((((e0_F_L_tr7*e0_x_L_tr7_c2)-(e0_F_L_tr8*e0_x_L_tr8_c2))+(e0_F_V_tr9*e0_x_V_tr9_c2))-(e0_F_V_tr8*e0_x_V_tr8_c2))  # noqa: E501,E226
#     EQ_diff17 = ((((e0_F_L_tr0*e0_h_L_tr0)-(e0_F_L_tr1*e0_h_L_tr1))+(e0_F_V_tr2*e0_h_V_tr2))-(e0_F_V_tr1*e0_h_V_tr1))  # noqa: E501,E226
#     EQ_diff18 = ((((e0_F_L_tr1*e0_h_L_tr1)-(e0_F_L_tr2*e0_h_L_tr2))+(e0_F_V_tr3*e0_h_V_tr3))-(e0_F_V_tr2*e0_h_V_tr2))  # noqa: E501,E226
#     EQ_diff19 = ((((e0_F_L_tr2*e0_h_L_tr2)-(e0_F_L_tr3*e0_h_L_tr3))+(e0_F_V_tr4*e0_h_V_tr4))-(e0_F_V_tr3*e0_h_V_tr3))  # noqa: E501,E226
#     EQ_diff20 = ((((e0_F_L_tr3*e0_h_L_tr3)-(e0_F_L_tr4*e0_h_L_tr4))+(e0_F_V_tr5*e0_h_V_tr5))-(e0_F_V_tr4*e0_h_V_tr4))  # noqa: E501,E226
#     EQ_diff21 = ((((e0_F_L_tr4*e0_h_L_tr4)-(e0_F_L_tr5*e0_h_L_tr5))+(e0_F_V_tr6*e0_h_V_tr6))-(e0_F_V_tr5*e0_h_V_tr5))  # noqa: E501,E226
#     EQ_diff22 = ((((e0_F_L_tr5*e0_h_L_tr5)-(e0_F_L_tr6*e0_h_L_tr6))+(e0_F_V_tr7*e0_h_V_tr7))-(e0_F_V_tr6*e0_h_V_tr6))  # noqa: E501,E226
#     EQ_diff23 = ((((e0_F_L_tr6*e0_h_L_tr6)-(e0_F_L_tr7*e0_h_L_tr7))+(e0_F_V_tr8*e0_h_V_tr8))-(e0_F_V_tr7*e0_h_V_tr7))  # noqa: E501,E226
#     EQ_diff24 = ((((e0_F_L_tr7*e0_h_L_tr7)-(e0_F_L_tr8*e0_h_L_tr8))+(e0_F_V_tr9*e0_h_V_tr9))-(e0_F_V_tr8*e0_h_V_tr8))  # noqa: E501,E226
#     EQ_diff25 = ((((e0_F_feed_tr9*e0_x_feed_tr9_c1)+(e0_F_L_tr8*e0_x_L_tr8_c1))-(e0_F_V_tr9*e0_x_V_tr9_c1))-(e0_F_B*e0_x_L_tr9_c1))  # noqa: E501,E226
#     EQ_diff26 = ((((e0_F_feed_tr9*e0_x_feed_tr9_c2)+(e0_F_L_tr8*e0_x_L_tr8_c2))-(e0_F_V_tr9*e0_x_V_tr9_c2))-(e0_F_B*e0_x_L_tr9_c2))  # noqa: E501,E226
#     EQ_diff27 = (((((e0_F_feed_tr9*e0_h_feed_tr9)+(e0_F_L_tr8*e0_h_L_tr8))-(e0_F_B*e0_h_L_tr9))-(e0_F_V_tr9*e0_h_V_tr9))+e0_Q_R)  # noqa: E501,E226
#     EQ_diff28 = (e0_F_D*e0_x_L_tr0_c1)  # noqa: E501,E226
#     EQ_diff29 = (e0_F_D*e0_x_L_tr0_c2)  # noqa: E501,E226

#     EQ_alg30 = ((e0_F_V_tr1*e0_x_V_tr1_c1)-((((e0_F_L_tr0+e0_F_D))*e0_x_L_tr0_c1)))  # noqa: E501,E226
#     EQ_alg31 = ((e0_F_V_tr1*e0_x_V_tr1_c2)-((((e0_F_L_tr0+e0_F_D))*e0_x_L_tr0_c2)))  # noqa: E501,E226
#     EQ_alg32 = (0.0-((e0_Q_C+(e0_F_V_tr1*((e0_h_V_tr1-e0_h_L_tr0))))))  # noqa: E501,E226
#     EQ_alg33 = (e0_h_L_tr0-((((e0_x_L_tr0_c1*e0_h_L_tr0_c1)+(e0_x_L_tr0_c2*e0_h_L_tr0_c2)))))  # noqa: E501,E226
#     EQ_alg34 = ((e0_rr*((e0_F_L_tr0+e0_F_D)))-(e0_F_L_tr0))  # noqa: E501,E226
#     EQ_alg35 = (0.0-((e0_x_V_tr0_c1-(e0_K_tr0_c1*e0_x_L_tr0_c1))))  # noqa: E501,E226
#     EQ_alg36 = (0.0-((e0_x_V_tr0_c2-(e0_K_tr0_c2*e0_x_L_tr0_c2))))  # noqa: E501,E226
#     EQ_alg37 = (1.0-(((e0_x_L_tr0_c1+e0_x_L_tr0_c2))))  # noqa: E501,E226
#     EQ_alg38 = ((1.0-e0_x_N2)-(((e0_x_V_tr0_c1+e0_x_V_tr0_c2))))  # noqa: E501,E226
#     EQ_alg39 = (0.0-((e0_p_LV_o_tr0_c1-((10.0))**(1.0*(e0_A_c1-(e0_B_c1/(e0_T_tr0+e0_C_c1)))))))  # noqa: E501,E226
#     EQ_alg40 = (0.0-((e0_p_LV_o_tr0_c2-((10.0))**(1.0*(e0_A_c2-(e0_B_c2/(e0_T_tr0+e0_C_c2)))))))  # noqa: E501,E226
#     EQ_alg41 = ((e0_p_tr0*e0_K_tr0_c1)-((e0_p_LV_o_tr0_c1*(((e0_greek_lambda_activity*e0_greek_gamma_tr0_c1)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
#     EQ_alg42 = ((e0_p_tr0*e0_K_tr0_c2)-((e0_p_LV_o_tr0_c2*(((e0_greek_lambda_activity*e0_greek_gamma_tr0_c2)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
#     EQ_alg43 = (e0_greek_alpha_tr0_c1-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c1)/e0_v_L_c1)*ca.exp(((-e0_greek_lambda_c1)/e0_T_tr0)))))  # noqa: E501,E226
#     EQ_alg44 = (e0_greek_alpha_tr0_c2-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c2)/e0_v_L_c2)*ca.exp(((-e0_greek_lambda_c2)/e0_T_tr0)))))  # noqa: E501,E226
#     EQ_alg45 = (e0_greek_gamma_tr0_c1-(((1.0/(e0_x_L_tr0_c1+(e0_greek_alpha_tr0_c1*((1.0-e0_x_L_tr0_c1)))))*ca.exp((((1.0-e0_x_L_tr0_c1))*(((e0_greek_alpha_tr0_c1/(e0_x_L_tr0_c1+(e0_greek_alpha_tr0_c1*((1.0-e0_x_L_tr0_c1)))))-((((e0_greek_alpha_tr0_c1+e0_greek_alpha_tr0_c2))-e0_greek_alpha_tr0_c1)/((((((e0_greek_alpha_tr0_c1+e0_greek_alpha_tr0_c2))-e0_greek_alpha_tr0_c1))*e0_x_L_tr0_c1)+((1.0-e0_x_L_tr0_c1)))))))))))  # noqa: E501,E226
#     EQ_alg46 = (e0_greek_gamma_tr0_c2-(((1.0/(e0_x_L_tr0_c2+(e0_greek_alpha_tr0_c2*((1.0-e0_x_L_tr0_c2)))))*ca.exp((((1.0-e0_x_L_tr0_c2))*(((e0_greek_alpha_tr0_c2/(e0_x_L_tr0_c2+(e0_greek_alpha_tr0_c2*((1.0-e0_x_L_tr0_c2)))))-((((e0_greek_alpha_tr0_c1+e0_greek_alpha_tr0_c2))-e0_greek_alpha_tr0_c2)/((((((e0_greek_alpha_tr0_c1+e0_greek_alpha_tr0_c2))-e0_greek_alpha_tr0_c2))*e0_x_L_tr0_c2)+((1.0-e0_x_L_tr0_c2)))))))))))  # noqa: E501,E226
#     EQ_alg47 = (0.0-((1.0-((e0_x_L_tr1_c1+e0_x_L_tr1_c2)))))  # noqa: E501,E226
#     EQ_alg48 = (0.0-((1.0-((e0_x_L_tr2_c1+e0_x_L_tr2_c2)))))  # noqa: E501,E226
#     EQ_alg49 = (0.0-((1.0-((e0_x_L_tr3_c1+e0_x_L_tr3_c2)))))  # noqa: E501,E226
#     EQ_alg50 = (0.0-((1.0-((e0_x_L_tr4_c1+e0_x_L_tr4_c2)))))  # noqa: E501,E226
#     EQ_alg51 = (0.0-((1.0-((e0_x_L_tr5_c1+e0_x_L_tr5_c2)))))  # noqa: E501,E226
#     EQ_alg52 = (0.0-((1.0-((e0_x_L_tr6_c1+e0_x_L_tr6_c2)))))  # noqa: E501,E226
#     EQ_alg53 = (0.0-((1.0-((e0_x_L_tr7_c1+e0_x_L_tr7_c2)))))  # noqa: E501,E226
#     EQ_alg54 = (0.0-((1.0-((e0_x_L_tr8_c1+e0_x_L_tr8_c2)))))  # noqa: E501,E226
#     EQ_alg55 = ((1.0-e0_x_N2)-(((e0_x_V_tr1_c1+e0_x_V_tr1_c2))))  # noqa: E501,E226
#     EQ_alg56 = ((1.0-e0_x_N2)-(((e0_x_V_tr2_c1+e0_x_V_tr2_c2))))  # noqa: E501,E226
#     EQ_alg57 = ((1.0-e0_x_N2)-(((e0_x_V_tr3_c1+e0_x_V_tr3_c2))))  # noqa: E501,E226
#     EQ_alg58 = ((1.0-e0_x_N2)-(((e0_x_V_tr4_c1+e0_x_V_tr4_c2))))  # noqa: E501,E226
#     EQ_alg59 = ((1.0-e0_x_N2)-(((e0_x_V_tr5_c1+e0_x_V_tr5_c2))))  # noqa: E501,E226
#     EQ_alg60 = ((1.0-e0_x_N2)-(((e0_x_V_tr6_c1+e0_x_V_tr6_c2))))  # noqa: E501,E226
#     EQ_alg61 = ((1.0-e0_x_N2)-(((e0_x_V_tr7_c1+e0_x_V_tr7_c2))))  # noqa: E501,E226
#     EQ_alg62 = ((1.0-e0_x_N2)-(((e0_x_V_tr8_c1+e0_x_V_tr8_c2))))  # noqa: E501,E226
#     EQ_alg63 = (e0_HU_tr1_c1-(((e0_HU_L_tr1*e0_x_L_tr1_c1)+(e0_HU_V_tr1*e0_x_V_tr1_c1))))  # noqa: E501,E226
#     EQ_alg64 = (e0_HU_tr2_c1-(((e0_HU_L_tr2*e0_x_L_tr2_c1)+(e0_HU_V_tr2*e0_x_V_tr2_c1))))  # noqa: E501,E226
#     EQ_alg65 = (e0_HU_tr3_c1-(((e0_HU_L_tr3*e0_x_L_tr3_c1)+(e0_HU_V_tr3*e0_x_V_tr3_c1))))  # noqa: E501,E226
#     EQ_alg66 = (e0_HU_tr4_c1-(((e0_HU_L_tr4*e0_x_L_tr4_c1)+(e0_HU_V_tr4*e0_x_V_tr4_c1))))  # noqa: E501,E226
#     EQ_alg67 = (e0_HU_tr5_c1-(((e0_HU_L_tr5*e0_x_L_tr5_c1)+(e0_HU_V_tr5*e0_x_V_tr5_c1))))  # noqa: E501,E226
#     EQ_alg68 = (e0_HU_tr6_c1-(((e0_HU_L_tr6*e0_x_L_tr6_c1)+(e0_HU_V_tr6*e0_x_V_tr6_c1))))  # noqa: E501,E226
#     EQ_alg69 = (e0_HU_tr7_c1-(((e0_HU_L_tr7*e0_x_L_tr7_c1)+(e0_HU_V_tr7*e0_x_V_tr7_c1))))  # noqa: E501,E226
#     EQ_alg70 = (e0_HU_tr8_c1-(((e0_HU_L_tr8*e0_x_L_tr8_c1)+(e0_HU_V_tr8*e0_x_V_tr8_c1))))  # noqa: E501,E226
#     EQ_alg71 = (e0_HU_tr1_c2-(((e0_HU_L_tr1*e0_x_L_tr1_c2)+(e0_HU_V_tr1*e0_x_V_tr1_c2))))  # noqa: E501,E226
#     EQ_alg72 = (e0_HU_tr2_c2-(((e0_HU_L_tr2*e0_x_L_tr2_c2)+(e0_HU_V_tr2*e0_x_V_tr2_c2))))  # noqa: E501,E226
#     EQ_alg73 = (e0_HU_tr3_c2-(((e0_HU_L_tr3*e0_x_L_tr3_c2)+(e0_HU_V_tr3*e0_x_V_tr3_c2))))  # noqa: E501,E226
#     EQ_alg74 = (e0_HU_tr4_c2-(((e0_HU_L_tr4*e0_x_L_tr4_c2)+(e0_HU_V_tr4*e0_x_V_tr4_c2))))  # noqa: E501,E226
#     EQ_alg75 = (e0_HU_tr5_c2-(((e0_HU_L_tr5*e0_x_L_tr5_c2)+(e0_HU_V_tr5*e0_x_V_tr5_c2))))  # noqa: E501,E226
#     EQ_alg76 = (e0_HU_tr6_c2-(((e0_HU_L_tr6*e0_x_L_tr6_c2)+(e0_HU_V_tr6*e0_x_V_tr6_c2))))  # noqa: E501,E226
#     EQ_alg77 = (e0_HU_tr7_c2-(((e0_HU_L_tr7*e0_x_L_tr7_c2)+(e0_HU_V_tr7*e0_x_V_tr7_c2))))  # noqa: E501,E226
#     EQ_alg78 = (e0_HU_tr8_c2-(((e0_HU_L_tr8*e0_x_L_tr8_c2)+(e0_HU_V_tr8*e0_x_V_tr8_c2))))  # noqa: E501,E226
#     EQ_alg79 = (e0_H_tr1-((e0_U_tr1+(e0_p_tr1*(((10.0))**(1.0*2.0)*e0_V_tot)))))  # noqa: E501,E226
#     EQ_alg80 = (e0_H_tr2-((e0_U_tr2+(e0_p_tr2*(((10.0))**(1.0*2.0)*e0_V_tot)))))  # noqa: E501,E226
#     EQ_alg81 = (e0_H_tr3-((e0_U_tr3+(e0_p_tr3*(((10.0))**(1.0*2.0)*e0_V_tot)))))  # noqa: E501,E226
#     EQ_alg82 = (e0_H_tr4-((e0_U_tr4+(e0_p_tr4*(((10.0))**(1.0*2.0)*e0_V_tot)))))  # noqa: E501,E226
#     EQ_alg83 = (e0_H_tr5-((e0_U_tr5+(e0_p_tr5*(((10.0))**(1.0*2.0)*e0_V_tot)))))  # noqa: E501,E226
#     EQ_alg84 = (e0_H_tr6-((e0_U_tr6+(e0_p_tr6*(((10.0))**(1.0*2.0)*e0_V_tot)))))  # noqa: E501,E226
#     EQ_alg85 = (e0_H_tr7-((e0_U_tr7+(e0_p_tr7*(((10.0))**(1.0*2.0)*e0_V_tot)))))  # noqa: E501,E226
#     EQ_alg86 = (e0_H_tr8-((e0_U_tr8+(e0_p_tr8*(((10.0))**(1.0*2.0)*e0_V_tot)))))  # noqa: E501,E226
#     EQ_alg87 = (e0_H_tr1-(((e0_HU_L_tr1*e0_h_L_tr1)+(e0_HU_V_tr1*e0_h_V_tr1))))  # noqa: E501,E226
#     EQ_alg88 = (e0_H_tr2-(((e0_HU_L_tr2*e0_h_L_tr2)+(e0_HU_V_tr2*e0_h_V_tr2))))  # noqa: E501,E226
#     EQ_alg89 = (e0_H_tr3-(((e0_HU_L_tr3*e0_h_L_tr3)+(e0_HU_V_tr3*e0_h_V_tr3))))  # noqa: E501,E226
#     EQ_alg90 = (e0_H_tr4-(((e0_HU_L_tr4*e0_h_L_tr4)+(e0_HU_V_tr4*e0_h_V_tr4))))  # noqa: E501,E226
#     EQ_alg91 = (e0_H_tr5-(((e0_HU_L_tr5*e0_h_L_tr5)+(e0_HU_V_tr5*e0_h_V_tr5))))  # noqa: E501,E226
#     EQ_alg92 = (e0_H_tr6-(((e0_HU_L_tr6*e0_h_L_tr6)+(e0_HU_V_tr6*e0_h_V_tr6))))  # noqa: E501,E226
#     EQ_alg93 = (e0_H_tr7-(((e0_HU_L_tr7*e0_h_L_tr7)+(e0_HU_V_tr7*e0_h_V_tr7))))  # noqa: E501,E226
#     EQ_alg94 = (e0_H_tr8-(((e0_HU_L_tr8*e0_h_L_tr8)+(e0_HU_V_tr8*e0_h_V_tr8))))  # noqa: E501,E226
#     EQ_alg95 = (e0_V_tot-((e0_V_L_tr1+e0_V_V_tr1)))  # noqa: E501,E226
#     EQ_alg96 = (e0_V_tot-((e0_V_L_tr2+e0_V_V_tr2)))  # noqa: E501,E226
#     EQ_alg97 = (e0_V_tot-((e0_V_L_tr3+e0_V_V_tr3)))  # noqa: E501,E226
#     EQ_alg98 = (e0_V_tot-((e0_V_L_tr4+e0_V_V_tr4)))  # noqa: E501,E226
#     EQ_alg99 = (e0_V_tot-((e0_V_L_tr5+e0_V_V_tr5)))  # noqa: E501,E226
#     EQ_alg100 = (e0_V_tot-((e0_V_L_tr6+e0_V_V_tr6)))  # noqa: E501,E226
#     EQ_alg101 = (e0_V_tot-((e0_V_L_tr7+e0_V_V_tr7)))  # noqa: E501,E226
#     EQ_alg102 = (e0_V_tot-((e0_V_L_tr8+e0_V_V_tr8)))  # noqa: E501,E226
#     EQ_alg103 = (e0_V_L_tr1-((e0_HU_L_tr1*e0_v_L_tr1)))  # noqa: E501,E226
#     EQ_alg104 = (e0_V_L_tr2-((e0_HU_L_tr2*e0_v_L_tr2)))  # noqa: E501,E226
#     EQ_alg105 = (e0_V_L_tr3-((e0_HU_L_tr3*e0_v_L_tr3)))  # noqa: E501,E226
#     EQ_alg106 = (e0_V_L_tr4-((e0_HU_L_tr4*e0_v_L_tr4)))  # noqa: E501,E226
#     EQ_alg107 = (e0_V_L_tr5-((e0_HU_L_tr5*e0_v_L_tr5)))  # noqa: E501,E226
#     EQ_alg108 = (e0_V_L_tr6-((e0_HU_L_tr6*e0_v_L_tr6)))  # noqa: E501,E226
#     EQ_alg109 = (e0_V_L_tr7-((e0_HU_L_tr7*e0_v_L_tr7)))  # noqa: E501,E226
#     EQ_alg110 = (e0_V_L_tr8-((e0_HU_L_tr8*e0_v_L_tr8)))  # noqa: E501,E226
#     EQ_alg111 = ((e0_p_tr1*(((10.0))**(1.0*5.0)*e0_V_V_tr1))-((e0_HU_V_tr1*(e0_R*e0_T_tr1))))  # noqa: E501,E226
#     EQ_alg112 = ((e0_p_tr2*(((10.0))**(1.0*5.0)*e0_V_V_tr2))-((e0_HU_V_tr2*(e0_R*e0_T_tr2))))  # noqa: E501,E226
#     EQ_alg113 = ((e0_p_tr3*(((10.0))**(1.0*5.0)*e0_V_V_tr3))-((e0_HU_V_tr3*(e0_R*e0_T_tr3))))  # noqa: E501,E226
#     EQ_alg114 = ((e0_p_tr4*(((10.0))**(1.0*5.0)*e0_V_V_tr4))-((e0_HU_V_tr4*(e0_R*e0_T_tr4))))  # noqa: E501,E226
#     EQ_alg115 = ((e0_p_tr5*(((10.0))**(1.0*5.0)*e0_V_V_tr5))-((e0_HU_V_tr5*(e0_R*e0_T_tr5))))  # noqa: E501,E226
#     EQ_alg116 = ((e0_p_tr6*(((10.0))**(1.0*5.0)*e0_V_V_tr6))-((e0_HU_V_tr6*(e0_R*e0_T_tr6))))  # noqa: E501,E226
#     EQ_alg117 = ((e0_p_tr7*(((10.0))**(1.0*5.0)*e0_V_V_tr7))-((e0_HU_V_tr7*(e0_R*e0_T_tr7))))  # noqa: E501,E226
#     EQ_alg118 = ((e0_p_tr8*(((10.0))**(1.0*5.0)*e0_V_V_tr8))-((e0_HU_V_tr8*(e0_R*e0_T_tr8))))  # noqa: E501,E226
#     EQ_alg119 = ((0.82*e0_A_col)-(e0_A_active))  # noqa: E501,E226
#     EQ_alg120 = (e0_A_col-((0.25*(e0_greek_pi*((e0_d_col))**(1.0*2.0)))))  # noqa: E501,E226
#     EQ_alg121 = ((e0_h_tot*e0_A_col)-(e0_V_tot))  # noqa: E501,E226
#     EQ_alg122 = (e0_L_weir-((0.7*e0_d_col)))  # noqa: E501,E226
#     EQ_alg123 = (e0_x_V_tr1_c1-((e0_x_V_tr2_c1+(e0_E_murphree*(((e0_K_tr1_c1*e0_x_L_tr1_c1)-e0_x_V_tr2_c1))))))  # noqa: E501,E226
#     EQ_alg124 = (e0_x_V_tr2_c1-((e0_x_V_tr3_c1+(e0_E_murphree*(((e0_K_tr2_c1*e0_x_L_tr2_c1)-e0_x_V_tr3_c1))))))  # noqa: E501,E226
#     EQ_alg125 = (e0_x_V_tr3_c1-((e0_x_V_tr4_c1+(e0_E_murphree*(((e0_K_tr3_c1*e0_x_L_tr3_c1)-e0_x_V_tr4_c1))))))  # noqa: E501,E226
#     EQ_alg126 = (e0_x_V_tr4_c1-((e0_x_V_tr5_c1+(e0_E_murphree*(((e0_K_tr4_c1*e0_x_L_tr4_c1)-e0_x_V_tr5_c1))))))  # noqa: E501,E226
#     EQ_alg127 = (e0_x_V_tr5_c1-((e0_x_V_tr6_c1+(e0_E_murphree*(((e0_K_tr5_c1*e0_x_L_tr5_c1)-e0_x_V_tr6_c1))))))  # noqa: E501,E226
#     EQ_alg128 = (e0_x_V_tr6_c1-((e0_x_V_tr7_c1+(e0_E_murphree*(((e0_K_tr6_c1*e0_x_L_tr6_c1)-e0_x_V_tr7_c1))))))  # noqa: E501,E226
#     EQ_alg129 = (e0_x_V_tr7_c1-((e0_x_V_tr8_c1+(e0_E_murphree*(((e0_K_tr7_c1*e0_x_L_tr7_c1)-e0_x_V_tr8_c1))))))  # noqa: E501,E226
#     EQ_alg130 = (e0_x_V_tr8_c1-((e0_x_V_tr9_c1+(e0_E_murphree*(((e0_K_tr8_c1*e0_x_L_tr8_c1)-e0_x_V_tr9_c1))))))  # noqa: E501,E226
#     EQ_alg131 = (e0_x_V_tr1_c2-((e0_x_V_tr2_c2+(e0_E_murphree*(((e0_K_tr1_c2*e0_x_L_tr1_c2)-e0_x_V_tr2_c2))))))  # noqa: E501,E226
#     EQ_alg132 = (e0_x_V_tr2_c2-((e0_x_V_tr3_c2+(e0_E_murphree*(((e0_K_tr2_c2*e0_x_L_tr2_c2)-e0_x_V_tr3_c2))))))  # noqa: E501,E226
#     EQ_alg133 = (e0_x_V_tr3_c2-((e0_x_V_tr4_c2+(e0_E_murphree*(((e0_K_tr3_c2*e0_x_L_tr3_c2)-e0_x_V_tr4_c2))))))  # noqa: E501,E226
#     EQ_alg134 = (e0_x_V_tr4_c2-((e0_x_V_tr5_c2+(e0_E_murphree*(((e0_K_tr4_c2*e0_x_L_tr4_c2)-e0_x_V_tr5_c2))))))  # noqa: E501,E226
#     EQ_alg135 = (e0_x_V_tr5_c2-((e0_x_V_tr6_c2+(e0_E_murphree*(((e0_K_tr5_c2*e0_x_L_tr5_c2)-e0_x_V_tr6_c2))))))  # noqa: E501,E226
#     EQ_alg136 = (e0_x_V_tr6_c2-((e0_x_V_tr7_c2+(e0_E_murphree*(((e0_K_tr6_c2*e0_x_L_tr6_c2)-e0_x_V_tr7_c2))))))  # noqa: E501,E226
#     EQ_alg137 = (e0_x_V_tr7_c2-((e0_x_V_tr8_c2+(e0_E_murphree*(((e0_K_tr7_c2*e0_x_L_tr7_c2)-e0_x_V_tr8_c2))))))  # noqa: E501,E226
#     EQ_alg138 = (e0_x_V_tr8_c2-((e0_x_V_tr9_c2+(e0_E_murphree*(((e0_K_tr8_c2*e0_x_L_tr8_c2)-e0_x_V_tr9_c2))))))  # noqa: E501,E226
#     EQ_alg139 = (0.0-((e0_p_LV_o_tr1_c1-((10.0))**(1.0*(e0_A_c1-(e0_B_c1/(e0_T_tr1+e0_C_c1)))))))  # noqa: E501,E226
#     EQ_alg140 = (0.0-((e0_p_LV_o_tr2_c1-((10.0))**(1.0*(e0_A_c1-(e0_B_c1/(e0_T_tr2+e0_C_c1)))))))  # noqa: E501,E226
#     EQ_alg141 = (0.0-((e0_p_LV_o_tr3_c1-((10.0))**(1.0*(e0_A_c1-(e0_B_c1/(e0_T_tr3+e0_C_c1)))))))  # noqa: E501,E226
#     EQ_alg142 = (0.0-((e0_p_LV_o_tr4_c1-((10.0))**(1.0*(e0_A_c1-(e0_B_c1/(e0_T_tr4+e0_C_c1)))))))  # noqa: E501,E226
#     EQ_alg143 = (0.0-((e0_p_LV_o_tr5_c1-((10.0))**(1.0*(e0_A_c1-(e0_B_c1/(e0_T_tr5+e0_C_c1)))))))  # noqa: E501,E226
#     EQ_alg144 = (0.0-((e0_p_LV_o_tr6_c1-((10.0))**(1.0*(e0_A_c1-(e0_B_c1/(e0_T_tr6+e0_C_c1)))))))  # noqa: E501,E226
#     EQ_alg145 = (0.0-((e0_p_LV_o_tr7_c1-((10.0))**(1.0*(e0_A_c1-(e0_B_c1/(e0_T_tr7+e0_C_c1)))))))  # noqa: E501,E226
#     EQ_alg146 = (0.0-((e0_p_LV_o_tr8_c1-((10.0))**(1.0*(e0_A_c1-(e0_B_c1/(e0_T_tr8+e0_C_c1)))))))  # noqa: E501,E226
#     EQ_alg147 = (0.0-((e0_p_LV_o_tr1_c2-((10.0))**(1.0*(e0_A_c2-(e0_B_c2/(e0_T_tr1+e0_C_c2)))))))  # noqa: E501,E226
#     EQ_alg148 = (0.0-((e0_p_LV_o_tr2_c2-((10.0))**(1.0*(e0_A_c2-(e0_B_c2/(e0_T_tr2+e0_C_c2)))))))  # noqa: E501,E226
#     EQ_alg149 = (0.0-((e0_p_LV_o_tr3_c2-((10.0))**(1.0*(e0_A_c2-(e0_B_c2/(e0_T_tr3+e0_C_c2)))))))  # noqa: E501,E226
#     EQ_alg150 = (0.0-((e0_p_LV_o_tr4_c2-((10.0))**(1.0*(e0_A_c2-(e0_B_c2/(e0_T_tr4+e0_C_c2)))))))  # noqa: E501,E226
#     EQ_alg151 = (0.0-((e0_p_LV_o_tr5_c2-((10.0))**(1.0*(e0_A_c2-(e0_B_c2/(e0_T_tr5+e0_C_c2)))))))  # noqa: E501,E226
#     EQ_alg152 = (0.0-((e0_p_LV_o_tr6_c2-((10.0))**(1.0*(e0_A_c2-(e0_B_c2/(e0_T_tr6+e0_C_c2)))))))  # noqa: E501,E226
#     EQ_alg153 = (0.0-((e0_p_LV_o_tr7_c2-((10.0))**(1.0*(e0_A_c2-(e0_B_c2/(e0_T_tr7+e0_C_c2)))))))  # noqa: E501,E226
#     EQ_alg154 = (0.0-((e0_p_LV_o_tr8_c2-((10.0))**(1.0*(e0_A_c2-(e0_B_c2/(e0_T_tr8+e0_C_c2)))))))  # noqa: E501,E226


#     # EQ_alg155 = (e0_F_L_tr1-((((((((e0_L_tr1-e0_h_weir)/0.664)+(((((((e0_L_tr1-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir/e0_v_L_tr1))))  # noqa: E501,E226
#     # EQ_alg156 = (e0_F_L_tr2-((((((((e0_L_tr2-e0_h_weir)/0.664)+(((((((e0_L_tr2-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir/e0_v_L_tr2))))  # noqa: E501,E226
#     # EQ_alg157 = (e0_F_L_tr3-((((((((e0_L_tr3-e0_h_weir)/0.664)+(((((((e0_L_tr3-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir/e0_v_L_tr3))))  # noqa: E501,E226
#     # EQ_alg158 = (e0_F_L_tr4-((((((((e0_L_tr4-e0_h_weir)/0.664)+(((((((e0_L_tr4-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir/e0_v_L_tr4))))  # noqa: E501,E226
#     # EQ_alg159 = (e0_F_L_tr5-((((((((e0_L_tr5-e0_h_weir)/0.664)+(((((((e0_L_tr5-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir/e0_v_L_tr5))))  # noqa: E501,E226
#     # EQ_alg160 = (e0_F_L_tr6-((((((((e0_L_tr6-e0_h_weir)/0.664)+(((((((e0_L_tr6-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir/e0_v_L_tr6))))  # noqa: E501,E226
#     # EQ_alg161 = (e0_F_L_tr7-((((((((e0_L_tr7-e0_h_weir)/0.664)+(((((((e0_L_tr7-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir/e0_v_L_tr7))))  # noqa: E501,E226
#     # EQ_alg162 = (e0_F_L_tr8-((((((((e0_L_tr8-e0_h_weir)/0.664)+(((((((e0_L_tr8-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir/e0_v_L_tr8))))  # noqa: E501,E226
#     EQ_alg155 = 1e3 * (e0_v_L_tr1 * e0_F_L_tr1-((((((((e0_L_tr1-e0_h_weir)/0.664)+(((((((e0_L_tr1-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir))))  # noqa: E501,E226
#     EQ_alg156 = 1e3 * (e0_v_L_tr2 * e0_F_L_tr2-((((((((e0_L_tr2-e0_h_weir)/0.664)+(((((((e0_L_tr2-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir))))  # noqa: E501,E226
#     EQ_alg157 = 1e3 * (e0_v_L_tr3 * e0_F_L_tr3-((((((((e0_L_tr3-e0_h_weir)/0.664)+(((((((e0_L_tr3-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir))))  # noqa: E501,E226
#     EQ_alg158 = 1e3 * (e0_v_L_tr4 * e0_F_L_tr4-((((((((e0_L_tr4-e0_h_weir)/0.664)+(((((((e0_L_tr4-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir))))  # noqa: E501,E226
#     EQ_alg159 = 1e3 * (e0_v_L_tr5 * e0_F_L_tr5-((((((((e0_L_tr5-e0_h_weir)/0.664)+(((((((e0_L_tr5-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir))))  # noqa: E501,E226
#     EQ_alg160 = 1e3 * (e0_v_L_tr6 * e0_F_L_tr6-((((((((e0_L_tr6-e0_h_weir)/0.664)+(((((((e0_L_tr6-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir))))  # noqa: E501,E226
#     EQ_alg161 = 1e3 * (e0_v_L_tr7 * e0_F_L_tr7-((((((((e0_L_tr7-e0_h_weir)/0.664)+(((((((e0_L_tr7-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir))))  # noqa: E501,E226
#     EQ_alg162 = 1e3 * (e0_v_L_tr8 * e0_F_L_tr8-((((((((e0_L_tr8-e0_h_weir)/0.664)+(((((((e0_L_tr8-e0_h_weir)/0.664)))**(1.0*2.0)+((e0_greek_epsiv_weir))**(1.0*2.0))))**(1.0*0.5))/2.0)))**(1.0*1.5)*(e0_L_weir))))  # noqa: E501,E226


#     EQ_alg163 = (e0_L_tr1-(((e0_HU_L_tr1*e0_v_L_tr1)/e0_A_active)))  # noqa: E501,E226
#     EQ_alg164 = (e0_L_tr2-(((e0_HU_L_tr2*e0_v_L_tr2)/e0_A_active)))  # noqa: E501,E226
#     EQ_alg165 = (e0_L_tr3-(((e0_HU_L_tr3*e0_v_L_tr3)/e0_A_active)))  # noqa: E501,E226
#     EQ_alg166 = (e0_L_tr4-(((e0_HU_L_tr4*e0_v_L_tr4)/e0_A_active)))  # noqa: E501,E226
#     EQ_alg167 = (e0_L_tr5-(((e0_HU_L_tr5*e0_v_L_tr5)/e0_A_active)))  # noqa: E501,E226
#     EQ_alg168 = (e0_L_tr6-(((e0_HU_L_tr6*e0_v_L_tr6)/e0_A_active)))  # noqa: E501,E226
#     EQ_alg169 = (e0_L_tr7-(((e0_HU_L_tr7*e0_v_L_tr7)/e0_A_active)))  # noqa: E501,E226
#     EQ_alg170 = (e0_L_tr8-(((e0_HU_L_tr8*e0_v_L_tr8)/e0_A_active)))  # noqa: E501,E226
#     EQ_alg171 = ((e0_p_tr1-e0_p_tr0)-(((e0_greek_kappa*((e0_F_V_tr1))**(1.0*2.0))+e0_greek_kappa_hyst)))  # noqa: E501,E226
#     EQ_alg172 = ((e0_p_tr2-e0_p_tr1)-(((e0_greek_kappa*((e0_F_V_tr2))**(1.0*2.0))+e0_greek_kappa_hyst)))  # noqa: E501,E226
#     EQ_alg173 = ((e0_p_tr3-e0_p_tr2)-(((e0_greek_kappa*((e0_F_V_tr3))**(1.0*2.0))+e0_greek_kappa_hyst)))  # noqa: E501,E226
#     EQ_alg174 = ((e0_p_tr4-e0_p_tr3)-(((e0_greek_kappa*((e0_F_V_tr4))**(1.0*2.0))+e0_greek_kappa_hyst)))  # noqa: E501,E226
#     EQ_alg175 = ((e0_p_tr5-e0_p_tr4)-(((e0_greek_kappa*((e0_F_V_tr5))**(1.0*2.0))+e0_greek_kappa_hyst)))  # noqa: E501,E226
#     EQ_alg176 = ((e0_p_tr6-e0_p_tr5)-(((e0_greek_kappa*((e0_F_V_tr6))**(1.0*2.0))+e0_greek_kappa_hyst)))  # noqa: E501,E226
#     EQ_alg177 = ((e0_p_tr7-e0_p_tr6)-(((e0_greek_kappa*((e0_F_V_tr7))**(1.0*2.0))+e0_greek_kappa_hyst)))  # noqa: E501,E226
#     EQ_alg178 = ((e0_p_tr8-e0_p_tr7)-(((e0_greek_kappa*((e0_F_V_tr8))**(1.0*2.0))+e0_greek_kappa_hyst)))  # noqa: E501,E226
#     EQ_alg179 = (e0_h_L_tr1-((((e0_x_L_tr1_c1*e0_h_L_tr1_c1)+(e0_x_L_tr1_c2*e0_h_L_tr1_c2)))))  # noqa: E501,E226
#     EQ_alg180 = (e0_h_L_tr2-((((e0_x_L_tr2_c1*e0_h_L_tr2_c1)+(e0_x_L_tr2_c2*e0_h_L_tr2_c2)))))  # noqa: E501,E226
#     EQ_alg181 = (e0_h_L_tr3-((((e0_x_L_tr3_c1*e0_h_L_tr3_c1)+(e0_x_L_tr3_c2*e0_h_L_tr3_c2)))))  # noqa: E501,E226
#     EQ_alg182 = (e0_h_L_tr4-((((e0_x_L_tr4_c1*e0_h_L_tr4_c1)+(e0_x_L_tr4_c2*e0_h_L_tr4_c2)))))  # noqa: E501,E226
#     EQ_alg183 = (e0_h_L_tr5-((((e0_x_L_tr5_c1*e0_h_L_tr5_c1)+(e0_x_L_tr5_c2*e0_h_L_tr5_c2)))))  # noqa: E501,E226
#     EQ_alg184 = (e0_h_L_tr6-((((e0_x_L_tr6_c1*e0_h_L_tr6_c1)+(e0_x_L_tr6_c2*e0_h_L_tr6_c2)))))  # noqa: E501,E226
#     EQ_alg185 = (e0_h_L_tr7-((((e0_x_L_tr7_c1*e0_h_L_tr7_c1)+(e0_x_L_tr7_c2*e0_h_L_tr7_c2)))))  # noqa: E501,E226
#     EQ_alg186 = (e0_h_L_tr8-((((e0_x_L_tr8_c1*e0_h_L_tr8_c1)+(e0_x_L_tr8_c2*e0_h_L_tr8_c2)))))  # noqa: E501,E226
#     EQ_alg187 = (0.0-((e0_h_V_tr1-(((e0_x_V_tr1_c1*e0_h_V_tr1_c1)+(e0_x_V_tr1_c2*e0_h_V_tr1_c2))))))  # noqa: E501,E226
#     EQ_alg188 = (0.0-((e0_h_V_tr2-(((e0_x_V_tr2_c1*e0_h_V_tr2_c1)+(e0_x_V_tr2_c2*e0_h_V_tr2_c2))))))  # noqa: E501,E226
#     EQ_alg189 = (0.0-((e0_h_V_tr3-(((e0_x_V_tr3_c1*e0_h_V_tr3_c1)+(e0_x_V_tr3_c2*e0_h_V_tr3_c2))))))  # noqa: E501,E226
#     EQ_alg190 = (0.0-((e0_h_V_tr4-(((e0_x_V_tr4_c1*e0_h_V_tr4_c1)+(e0_x_V_tr4_c2*e0_h_V_tr4_c2))))))  # noqa: E501,E226
#     EQ_alg191 = (0.0-((e0_h_V_tr5-(((e0_x_V_tr5_c1*e0_h_V_tr5_c1)+(e0_x_V_tr5_c2*e0_h_V_tr5_c2))))))  # noqa: E501,E226
#     EQ_alg192 = (0.0-((e0_h_V_tr6-(((e0_x_V_tr6_c1*e0_h_V_tr6_c1)+(e0_x_V_tr6_c2*e0_h_V_tr6_c2))))))  # noqa: E501,E226
#     EQ_alg193 = (0.0-((e0_h_V_tr7-(((e0_x_V_tr7_c1*e0_h_V_tr7_c1)+(e0_x_V_tr7_c2*e0_h_V_tr7_c2))))))  # noqa: E501,E226
#     EQ_alg194 = (0.0-((e0_h_V_tr8-(((e0_x_V_tr8_c1*e0_h_V_tr8_c1)+(e0_x_V_tr8_c2*e0_h_V_tr8_c2))))))  # noqa: E501,E226
#     EQ_alg195 = ((e0_p_tr1*e0_K_tr1_c1)-((e0_p_LV_o_tr1_c1*(((e0_greek_lambda_activity*e0_greek_gamma_tr1_c1)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
#     EQ_alg196 = ((e0_p_tr2*e0_K_tr2_c1)-((e0_p_LV_o_tr2_c1*(((e0_greek_lambda_activity*e0_greek_gamma_tr2_c1)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
#     EQ_alg197 = ((e0_p_tr3*e0_K_tr3_c1)-((e0_p_LV_o_tr3_c1*(((e0_greek_lambda_activity*e0_greek_gamma_tr3_c1)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
#     EQ_alg198 = ((e0_p_tr4*e0_K_tr4_c1)-((e0_p_LV_o_tr4_c1*(((e0_greek_lambda_activity*e0_greek_gamma_tr4_c1)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
#     EQ_alg199 = ((e0_p_tr5*e0_K_tr5_c1)-((e0_p_LV_o_tr5_c1*(((e0_greek_lambda_activity*e0_greek_gamma_tr5_c1)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
#     EQ_alg200 = ((e0_p_tr6*e0_K_tr6_c1)-((e0_p_LV_o_tr6_c1*(((e0_greek_lambda_activity*e0_greek_gamma_tr6_c1)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
#     EQ_alg201 = ((e0_p_tr7*e0_K_tr7_c1)-((e0_p_LV_o_tr7_c1*(((e0_greek_lambda_activity*e0_greek_gamma_tr7_c1)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
#     EQ_alg202 = ((e0_p_tr8*e0_K_tr8_c1)-((e0_p_LV_o_tr8_c1*(((e0_greek_lambda_activity*e0_greek_gamma_tr8_c1)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
#     EQ_alg203 = ((e0_p_tr1*e0_K_tr1_c2)-((e0_p_LV_o_tr1_c2*(((e0_greek_lambda_activity*e0_greek_gamma_tr1_c2)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
#     EQ_alg204 = ((e0_p_tr2*e0_K_tr2_c2)-((e0_p_LV_o_tr2_c2*(((e0_greek_lambda_activity*e0_greek_gamma_tr2_c2)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
#     EQ_alg205 = ((e0_p_tr3*e0_K_tr3_c2)-((e0_p_LV_o_tr3_c2*(((e0_greek_lambda_activity*e0_greek_gamma_tr3_c2)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
#     EQ_alg206 = ((e0_p_tr4*e0_K_tr4_c2)-((e0_p_LV_o_tr4_c2*(((e0_greek_lambda_activity*e0_greek_gamma_tr4_c2)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
#     EQ_alg207 = ((e0_p_tr5*e0_K_tr5_c2)-((e0_p_LV_o_tr5_c2*(((e0_greek_lambda_activity*e0_greek_gamma_tr5_c2)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
#     EQ_alg208 = ((e0_p_tr6*e0_K_tr6_c2)-((e0_p_LV_o_tr6_c2*(((e0_greek_lambda_activity*e0_greek_gamma_tr6_c2)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
#     EQ_alg209 = ((e0_p_tr7*e0_K_tr7_c2)-((e0_p_LV_o_tr7_c2*(((e0_greek_lambda_activity*e0_greek_gamma_tr7_c2)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
#     EQ_alg210 = ((e0_p_tr8*e0_K_tr8_c2)-((e0_p_LV_o_tr8_c2*(((e0_greek_lambda_activity*e0_greek_gamma_tr8_c2)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
#     EQ_alg211 = (e0_greek_alpha_tr1_c1-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c1)/e0_v_L_c1)*ca.exp(((-e0_greek_lambda_c1)/e0_T_tr1)))))  # noqa: E501,E226
#     EQ_alg212 = (e0_greek_alpha_tr2_c1-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c1)/e0_v_L_c1)*ca.exp(((-e0_greek_lambda_c1)/e0_T_tr2)))))  # noqa: E501,E226
#     EQ_alg213 = (e0_greek_alpha_tr3_c1-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c1)/e0_v_L_c1)*ca.exp(((-e0_greek_lambda_c1)/e0_T_tr3)))))  # noqa: E501,E226
#     EQ_alg214 = (e0_greek_alpha_tr4_c1-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c1)/e0_v_L_c1)*ca.exp(((-e0_greek_lambda_c1)/e0_T_tr4)))))  # noqa: E501,E226
#     EQ_alg215 = (e0_greek_alpha_tr5_c1-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c1)/e0_v_L_c1)*ca.exp(((-e0_greek_lambda_c1)/e0_T_tr5)))))  # noqa: E501,E226
#     EQ_alg216 = (e0_greek_alpha_tr6_c1-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c1)/e0_v_L_c1)*ca.exp(((-e0_greek_lambda_c1)/e0_T_tr6)))))  # noqa: E501,E226
#     EQ_alg217 = (e0_greek_alpha_tr7_c1-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c1)/e0_v_L_c1)*ca.exp(((-e0_greek_lambda_c1)/e0_T_tr7)))))  # noqa: E501,E226
#     EQ_alg218 = (e0_greek_alpha_tr8_c1-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c1)/e0_v_L_c1)*ca.exp(((-e0_greek_lambda_c1)/e0_T_tr8)))))  # noqa: E501,E226
#     EQ_alg219 = (e0_greek_alpha_tr1_c2-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c2)/e0_v_L_c2)*ca.exp(((-e0_greek_lambda_c2)/e0_T_tr1)))))  # noqa: E501,E226
#     EQ_alg220 = (e0_greek_alpha_tr2_c2-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c2)/e0_v_L_c2)*ca.exp(((-e0_greek_lambda_c2)/e0_T_tr2)))))  # noqa: E501,E226
#     EQ_alg221 = (e0_greek_alpha_tr3_c2-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c2)/e0_v_L_c2)*ca.exp(((-e0_greek_lambda_c2)/e0_T_tr3)))))  # noqa: E501,E226
#     EQ_alg222 = (e0_greek_alpha_tr4_c2-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c2)/e0_v_L_c2)*ca.exp(((-e0_greek_lambda_c2)/e0_T_tr4)))))  # noqa: E501,E226
#     EQ_alg223 = (e0_greek_alpha_tr5_c2-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c2)/e0_v_L_c2)*ca.exp(((-e0_greek_lambda_c2)/e0_T_tr5)))))  # noqa: E501,E226
#     EQ_alg224 = (e0_greek_alpha_tr6_c2-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c2)/e0_v_L_c2)*ca.exp(((-e0_greek_lambda_c2)/e0_T_tr6)))))  # noqa: E501,E226
#     EQ_alg225 = (e0_greek_alpha_tr7_c2-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c2)/e0_v_L_c2)*ca.exp(((-e0_greek_lambda_c2)/e0_T_tr7)))))  # noqa: E501,E226
#     EQ_alg226 = (e0_greek_alpha_tr8_c2-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c2)/e0_v_L_c2)*ca.exp(((-e0_greek_lambda_c2)/e0_T_tr8)))))  # noqa: E501,E226
#     EQ_alg227 = (e0_greek_gamma_tr1_c1-(((1.0/(e0_x_L_tr1_c1+(e0_greek_alpha_tr1_c1*((1.0-e0_x_L_tr1_c1)))))*ca.exp((((1.0-e0_x_L_tr1_c1))*(((e0_greek_alpha_tr1_c1/(e0_x_L_tr1_c1+(e0_greek_alpha_tr1_c1*((1.0-e0_x_L_tr1_c1)))))-((((e0_greek_alpha_tr1_c1+e0_greek_alpha_tr1_c2))-e0_greek_alpha_tr1_c1)/((((((e0_greek_alpha_tr1_c1+e0_greek_alpha_tr1_c2))-e0_greek_alpha_tr1_c1))*e0_x_L_tr1_c1)+((1.0-e0_x_L_tr1_c1)))))))))))  # noqa: E501,E226
#     EQ_alg228 = (e0_greek_gamma_tr2_c1-(((1.0/(e0_x_L_tr2_c1+(e0_greek_alpha_tr2_c1*((1.0-e0_x_L_tr2_c1)))))*ca.exp((((1.0-e0_x_L_tr2_c1))*(((e0_greek_alpha_tr2_c1/(e0_x_L_tr2_c1+(e0_greek_alpha_tr2_c1*((1.0-e0_x_L_tr2_c1)))))-((((e0_greek_alpha_tr2_c1+e0_greek_alpha_tr2_c2))-e0_greek_alpha_tr2_c1)/((((((e0_greek_alpha_tr2_c1+e0_greek_alpha_tr2_c2))-e0_greek_alpha_tr2_c1))*e0_x_L_tr2_c1)+((1.0-e0_x_L_tr2_c1)))))))))))  # noqa: E501,E226
#     EQ_alg229 = (e0_greek_gamma_tr3_c1-(((1.0/(e0_x_L_tr3_c1+(e0_greek_alpha_tr3_c1*((1.0-e0_x_L_tr3_c1)))))*ca.exp((((1.0-e0_x_L_tr3_c1))*(((e0_greek_alpha_tr3_c1/(e0_x_L_tr3_c1+(e0_greek_alpha_tr3_c1*((1.0-e0_x_L_tr3_c1)))))-((((e0_greek_alpha_tr3_c1+e0_greek_alpha_tr3_c2))-e0_greek_alpha_tr3_c1)/((((((e0_greek_alpha_tr3_c1+e0_greek_alpha_tr3_c2))-e0_greek_alpha_tr3_c1))*e0_x_L_tr3_c1)+((1.0-e0_x_L_tr3_c1)))))))))))  # noqa: E501,E226
#     EQ_alg230 = (e0_greek_gamma_tr4_c1-(((1.0/(e0_x_L_tr4_c1+(e0_greek_alpha_tr4_c1*((1.0-e0_x_L_tr4_c1)))))*ca.exp((((1.0-e0_x_L_tr4_c1))*(((e0_greek_alpha_tr4_c1/(e0_x_L_tr4_c1+(e0_greek_alpha_tr4_c1*((1.0-e0_x_L_tr4_c1)))))-((((e0_greek_alpha_tr4_c1+e0_greek_alpha_tr4_c2))-e0_greek_alpha_tr4_c1)/((((((e0_greek_alpha_tr4_c1+e0_greek_alpha_tr4_c2))-e0_greek_alpha_tr4_c1))*e0_x_L_tr4_c1)+((1.0-e0_x_L_tr4_c1)))))))))))  # noqa: E501,E226
#     EQ_alg231 = (e0_greek_gamma_tr5_c1-(((1.0/(e0_x_L_tr5_c1+(e0_greek_alpha_tr5_c1*((1.0-e0_x_L_tr5_c1)))))*ca.exp((((1.0-e0_x_L_tr5_c1))*(((e0_greek_alpha_tr5_c1/(e0_x_L_tr5_c1+(e0_greek_alpha_tr5_c1*((1.0-e0_x_L_tr5_c1)))))-((((e0_greek_alpha_tr5_c1+e0_greek_alpha_tr5_c2))-e0_greek_alpha_tr5_c1)/((((((e0_greek_alpha_tr5_c1+e0_greek_alpha_tr5_c2))-e0_greek_alpha_tr5_c1))*e0_x_L_tr5_c1)+((1.0-e0_x_L_tr5_c1)))))))))))  # noqa: E501,E226
#     EQ_alg232 = (e0_greek_gamma_tr6_c1-(((1.0/(e0_x_L_tr6_c1+(e0_greek_alpha_tr6_c1*((1.0-e0_x_L_tr6_c1)))))*ca.exp((((1.0-e0_x_L_tr6_c1))*(((e0_greek_alpha_tr6_c1/(e0_x_L_tr6_c1+(e0_greek_alpha_tr6_c1*((1.0-e0_x_L_tr6_c1)))))-((((e0_greek_alpha_tr6_c1+e0_greek_alpha_tr6_c2))-e0_greek_alpha_tr6_c1)/((((((e0_greek_alpha_tr6_c1+e0_greek_alpha_tr6_c2))-e0_greek_alpha_tr6_c1))*e0_x_L_tr6_c1)+((1.0-e0_x_L_tr6_c1)))))))))))  # noqa: E501,E226
#     EQ_alg233 = (e0_greek_gamma_tr7_c1-(((1.0/(e0_x_L_tr7_c1+(e0_greek_alpha_tr7_c1*((1.0-e0_x_L_tr7_c1)))))*ca.exp((((1.0-e0_x_L_tr7_c1))*(((e0_greek_alpha_tr7_c1/(e0_x_L_tr7_c1+(e0_greek_alpha_tr7_c1*((1.0-e0_x_L_tr7_c1)))))-((((e0_greek_alpha_tr7_c1+e0_greek_alpha_tr7_c2))-e0_greek_alpha_tr7_c1)/((((((e0_greek_alpha_tr7_c1+e0_greek_alpha_tr7_c2))-e0_greek_alpha_tr7_c1))*e0_x_L_tr7_c1)+((1.0-e0_x_L_tr7_c1)))))))))))  # noqa: E501,E226
#     EQ_alg234 = (e0_greek_gamma_tr8_c1-(((1.0/(e0_x_L_tr8_c1+(e0_greek_alpha_tr8_c1*((1.0-e0_x_L_tr8_c1)))))*ca.exp((((1.0-e0_x_L_tr8_c1))*(((e0_greek_alpha_tr8_c1/(e0_x_L_tr8_c1+(e0_greek_alpha_tr8_c1*((1.0-e0_x_L_tr8_c1)))))-((((e0_greek_alpha_tr8_c1+e0_greek_alpha_tr8_c2))-e0_greek_alpha_tr8_c1)/((((((e0_greek_alpha_tr8_c1+e0_greek_alpha_tr8_c2))-e0_greek_alpha_tr8_c1))*e0_x_L_tr8_c1)+((1.0-e0_x_L_tr8_c1)))))))))))  # noqa: E501,E226
#     EQ_alg235 = (e0_greek_gamma_tr1_c2-(((1.0/(e0_x_L_tr1_c2+(e0_greek_alpha_tr1_c2*((1.0-e0_x_L_tr1_c2)))))*ca.exp((((1.0-e0_x_L_tr1_c2))*(((e0_greek_alpha_tr1_c2/(e0_x_L_tr1_c2+(e0_greek_alpha_tr1_c2*((1.0-e0_x_L_tr1_c2)))))-((((e0_greek_alpha_tr1_c1+e0_greek_alpha_tr1_c2))-e0_greek_alpha_tr1_c2)/((((((e0_greek_alpha_tr1_c1+e0_greek_alpha_tr1_c2))-e0_greek_alpha_tr1_c2))*e0_x_L_tr1_c2)+((1.0-e0_x_L_tr1_c2)))))))))))  # noqa: E501,E226
#     EQ_alg236 = (e0_greek_gamma_tr2_c2-(((1.0/(e0_x_L_tr2_c2+(e0_greek_alpha_tr2_c2*((1.0-e0_x_L_tr2_c2)))))*ca.exp((((1.0-e0_x_L_tr2_c2))*(((e0_greek_alpha_tr2_c2/(e0_x_L_tr2_c2+(e0_greek_alpha_tr2_c2*((1.0-e0_x_L_tr2_c2)))))-((((e0_greek_alpha_tr2_c1+e0_greek_alpha_tr2_c2))-e0_greek_alpha_tr2_c2)/((((((e0_greek_alpha_tr2_c1+e0_greek_alpha_tr2_c2))-e0_greek_alpha_tr2_c2))*e0_x_L_tr2_c2)+((1.0-e0_x_L_tr2_c2)))))))))))  # noqa: E501,E226
#     EQ_alg237 = (e0_greek_gamma_tr3_c2-(((1.0/(e0_x_L_tr3_c2+(e0_greek_alpha_tr3_c2*((1.0-e0_x_L_tr3_c2)))))*ca.exp((((1.0-e0_x_L_tr3_c2))*(((e0_greek_alpha_tr3_c2/(e0_x_L_tr3_c2+(e0_greek_alpha_tr3_c2*((1.0-e0_x_L_tr3_c2)))))-((((e0_greek_alpha_tr3_c1+e0_greek_alpha_tr3_c2))-e0_greek_alpha_tr3_c2)/((((((e0_greek_alpha_tr3_c1+e0_greek_alpha_tr3_c2))-e0_greek_alpha_tr3_c2))*e0_x_L_tr3_c2)+((1.0-e0_x_L_tr3_c2)))))))))))  # noqa: E501,E226
#     EQ_alg238 = (e0_greek_gamma_tr4_c2-(((1.0/(e0_x_L_tr4_c2+(e0_greek_alpha_tr4_c2*((1.0-e0_x_L_tr4_c2)))))*ca.exp((((1.0-e0_x_L_tr4_c2))*(((e0_greek_alpha_tr4_c2/(e0_x_L_tr4_c2+(e0_greek_alpha_tr4_c2*((1.0-e0_x_L_tr4_c2)))))-((((e0_greek_alpha_tr4_c1+e0_greek_alpha_tr4_c2))-e0_greek_alpha_tr4_c2)/((((((e0_greek_alpha_tr4_c1+e0_greek_alpha_tr4_c2))-e0_greek_alpha_tr4_c2))*e0_x_L_tr4_c2)+((1.0-e0_x_L_tr4_c2)))))))))))  # noqa: E501,E226
#     EQ_alg239 = (e0_greek_gamma_tr5_c2-(((1.0/(e0_x_L_tr5_c2+(e0_greek_alpha_tr5_c2*((1.0-e0_x_L_tr5_c2)))))*ca.exp((((1.0-e0_x_L_tr5_c2))*(((e0_greek_alpha_tr5_c2/(e0_x_L_tr5_c2+(e0_greek_alpha_tr5_c2*((1.0-e0_x_L_tr5_c2)))))-((((e0_greek_alpha_tr5_c1+e0_greek_alpha_tr5_c2))-e0_greek_alpha_tr5_c2)/((((((e0_greek_alpha_tr5_c1+e0_greek_alpha_tr5_c2))-e0_greek_alpha_tr5_c2))*e0_x_L_tr5_c2)+((1.0-e0_x_L_tr5_c2)))))))))))  # noqa: E501,E226
#     EQ_alg240 = (e0_greek_gamma_tr6_c2-(((1.0/(e0_x_L_tr6_c2+(e0_greek_alpha_tr6_c2*((1.0-e0_x_L_tr6_c2)))))*ca.exp((((1.0-e0_x_L_tr6_c2))*(((e0_greek_alpha_tr6_c2/(e0_x_L_tr6_c2+(e0_greek_alpha_tr6_c2*((1.0-e0_x_L_tr6_c2)))))-((((e0_greek_alpha_tr6_c1+e0_greek_alpha_tr6_c2))-e0_greek_alpha_tr6_c2)/((((((e0_greek_alpha_tr6_c1+e0_greek_alpha_tr6_c2))-e0_greek_alpha_tr6_c2))*e0_x_L_tr6_c2)+((1.0-e0_x_L_tr6_c2)))))))))))  # noqa: E501,E226
#     EQ_alg241 = (e0_greek_gamma_tr7_c2-(((1.0/(e0_x_L_tr7_c2+(e0_greek_alpha_tr7_c2*((1.0-e0_x_L_tr7_c2)))))*ca.exp((((1.0-e0_x_L_tr7_c2))*(((e0_greek_alpha_tr7_c2/(e0_x_L_tr7_c2+(e0_greek_alpha_tr7_c2*((1.0-e0_x_L_tr7_c2)))))-((((e0_greek_alpha_tr7_c1+e0_greek_alpha_tr7_c2))-e0_greek_alpha_tr7_c2)/((((((e0_greek_alpha_tr7_c1+e0_greek_alpha_tr7_c2))-e0_greek_alpha_tr7_c2))*e0_x_L_tr7_c2)+((1.0-e0_x_L_tr7_c2)))))))))))  # noqa: E501,E226
#     EQ_alg242 = (e0_greek_gamma_tr8_c2-(((1.0/(e0_x_L_tr8_c2+(e0_greek_alpha_tr8_c2*((1.0-e0_x_L_tr8_c2)))))*ca.exp((((1.0-e0_x_L_tr8_c2))*(((e0_greek_alpha_tr8_c2/(e0_x_L_tr8_c2+(e0_greek_alpha_tr8_c2*((1.0-e0_x_L_tr8_c2)))))-((((e0_greek_alpha_tr8_c1+e0_greek_alpha_tr8_c2))-e0_greek_alpha_tr8_c2)/((((((e0_greek_alpha_tr8_c1+e0_greek_alpha_tr8_c2))-e0_greek_alpha_tr8_c2))*e0_x_L_tr8_c2)+((1.0-e0_x_L_tr8_c2)))))))))))  # noqa: E501,E226
#     EQ_alg243 = (e0_v_L_tr1-((((e0_x_L_tr1_c1*e0_v_L_c1)+(e0_x_L_tr1_c2*e0_v_L_c2)))))  # noqa: E501,E226
#     EQ_alg244 = (e0_v_L_tr2-((((e0_x_L_tr2_c1*e0_v_L_c1)+(e0_x_L_tr2_c2*e0_v_L_c2)))))  # noqa: E501,E226
#     EQ_alg245 = (e0_v_L_tr3-((((e0_x_L_tr3_c1*e0_v_L_c1)+(e0_x_L_tr3_c2*e0_v_L_c2)))))  # noqa: E501,E226
#     EQ_alg246 = (e0_v_L_tr4-((((e0_x_L_tr4_c1*e0_v_L_c1)+(e0_x_L_tr4_c2*e0_v_L_c2)))))  # noqa: E501,E226
#     EQ_alg247 = (e0_v_L_tr5-((((e0_x_L_tr5_c1*e0_v_L_c1)+(e0_x_L_tr5_c2*e0_v_L_c2)))))  # noqa: E501,E226
#     EQ_alg248 = (e0_v_L_tr6-((((e0_x_L_tr6_c1*e0_v_L_c1)+(e0_x_L_tr6_c2*e0_v_L_c2)))))  # noqa: E501,E226
#     EQ_alg249 = (e0_v_L_tr7-((((e0_x_L_tr7_c1*e0_v_L_c1)+(e0_x_L_tr7_c2*e0_v_L_c2)))))  # noqa: E501,E226
#     EQ_alg250 = (e0_v_L_tr8-((((e0_x_L_tr8_c1*e0_v_L_c1)+(e0_x_L_tr8_c2*e0_v_L_c2)))))  # noqa: E501,E226
#     EQ_alg251 = (0.0-((1.0-((e0_x_L_tr9_c1+e0_x_L_tr9_c2)))))  # noqa: E501,E226
#     # EQ_alg252 = (0.0-((1.0-((e0_x_V_tr9_c1+e0_x_V_tr9_c2)))))  # noqa: E501,E226
#     EQ_alg252 = ((1.0-e0_x_N2)-(((e0_x_V_tr9_c1+e0_x_V_tr9_c2))))
#     EQ_alg253 = (e0_HU_tr9_c1-(((e0_HU_L_tr9*e0_x_L_tr9_c1)+(e0_HU_V_tr9*e0_x_V_tr9_c1))))  # noqa: E501,E226
#     EQ_alg254 = (e0_HU_tr9_c2-(((e0_HU_L_tr9*e0_x_L_tr9_c2)+(e0_HU_V_tr9*e0_x_V_tr9_c2))))  # noqa: E501,E226
#     # EQ_alg255 = (e0_H_tr9-((e0_U_tr9+(e0_p_tr9*(((10.0))**(1.0*2.0)*e0_V_tot_tr9)))))  # noqa: E501,E226
#     EQ_alg255 = 1e-3 * (e0_H_tr9-((e0_U_tr9+(e0_p_tr9*(((10.0))**(1.0*2.0)*e0_V_tot_tr9)))))  # noqa: E501,E226
#     EQ_alg256 = (1/300.0) * (e0_H_tr9-(((e0_HU_L_tr9*e0_h_L_tr9)+(e0_HU_V_tr9*e0_h_V_tr9))))  # noqa: E501,E226
#     EQ_alg257 = (e0_V_tot_tr9-((e0_V_L_tr9+e0_V_V_tr9)))  # noqa: E501,E226
#     EQ_alg258 = (e0_V_L_tr9-((e0_HU_L_tr9*e0_v_L_tr9)))  # noqa: E501,E226
#     EQ_alg259 = 1e-2 * ((e0_p_tr9*(((10.0))**(1.0*5.0)*e0_V_V_tr9))-((e0_HU_V_tr9*(e0_R*e0_T_tr9))))  # noqa: E501,E226
#     EQ_alg260 = (0.0-((e0_x_V_tr9_c1-(e0_K_tr9_c1*e0_x_L_tr9_c1))))  # noqa: E501,E226
#     EQ_alg261 = (0.0-((e0_x_V_tr9_c2-(e0_K_tr9_c2*e0_x_L_tr9_c2))))  # noqa: E501,E226
#     EQ_alg262 = (e0_p_LV_o_tr9_c1-(((10.0))**(1.0*(e0_A_c1-(e0_B_c1/(e0_T_tr9+e0_C_c1))))))  # noqa: E501,E226
#     EQ_alg263 = (e0_p_LV_o_tr9_c2-(((10.0))**(1.0*(e0_A_c2-(e0_B_c2/(e0_T_tr9+e0_C_c2))))))  # noqa: E501,E226
#     EQ_alg264 = (e0_h_feed_tr9-((((e0_x_feed_tr9_c1*e0_h_feed_tr9_c1)+(e0_x_feed_tr9_c2*e0_h_feed_tr9_c2)))))  # noqa: E501,E226
#     EQ_alg265 = (e0_h_L_tr9-((((e0_x_L_tr9_c1*e0_h_L_tr9_c1)+(e0_x_L_tr9_c2*e0_h_L_tr9_c2)))))  # noqa: E501,E226
#     EQ_alg266 = (e0_h_V_tr9-((((e0_x_V_tr9_c1*e0_h_V_tr9_c1)+(e0_x_V_tr9_c2*e0_h_V_tr9_c2)))))  # noqa: E501,E226
#     EQ_alg267 = (((e0_p_tr9-e0_p_tr8))-(((e0_greek_kappa*((e0_F_V_tr9))**(1.0*2.0))+e0_greek_kappa_hyst)))  # noqa: E501,E226
#     EQ_alg268 = ((e0_p_tr9*e0_K_tr9_c1)-((e0_p_LV_o_tr9_c1*(((e0_greek_lambda_activity*e0_greek_gamma_tr9_c1)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
#     EQ_alg269 = ((e0_p_tr9*e0_K_tr9_c2)-((e0_p_LV_o_tr9_c2*(((e0_greek_lambda_activity*e0_greek_gamma_tr9_c2)+(((1.0-e0_greek_lambda_activity))*1.0))))))  # noqa: E501,E226
#     EQ_alg270 = (e0_v_L_tr9-((((e0_x_L_tr9_c1*e0_v_L_c1)+(e0_x_L_tr9_c2*e0_v_L_c2)))))  # noqa: E501,E226
#     EQ_alg271 = (e0_greek_alpha_tr9_c1-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c1)/e0_v_L_c1)*ca.exp(((-e0_greek_lambda_c1)/e0_T_tr9)))))  # noqa: E501,E226
#     EQ_alg272 = (e0_greek_alpha_tr9_c2-((((((e0_v_L_c1+e0_v_L_c2))-e0_v_L_c2)/e0_v_L_c2)*ca.exp(((-e0_greek_lambda_c2)/e0_T_tr9)))))  # noqa: E501,E226
#     EQ_alg273 = (e0_greek_gamma_tr9_c1-(((1.0/(e0_x_L_tr9_c1+(e0_greek_alpha_tr9_c1*((1.0-e0_x_L_tr9_c1)))))*ca.exp((((1.0-e0_x_L_tr9_c1))*(((e0_greek_alpha_tr9_c1/(e0_x_L_tr9_c1+(e0_greek_alpha_tr9_c1*((1.0-e0_x_L_tr9_c1)))))-((((e0_greek_alpha_tr9_c1+e0_greek_alpha_tr9_c2))-e0_greek_alpha_tr9_c1)/((((((e0_greek_alpha_tr9_c1+e0_greek_alpha_tr9_c2))-e0_greek_alpha_tr9_c1))*e0_x_L_tr9_c1)+((1.0-e0_x_L_tr9_c1)))))))))))  # noqa: E501,E226
#     EQ_alg274 = (e0_greek_gamma_tr9_c2-(((1.0/(e0_x_L_tr9_c2+(e0_greek_alpha_tr9_c2*((1.0-e0_x_L_tr9_c2)))))*ca.exp((((1.0-e0_x_L_tr9_c2))*(((e0_greek_alpha_tr9_c2/(e0_x_L_tr9_c2+(e0_greek_alpha_tr9_c2*((1.0-e0_x_L_tr9_c2)))))-((((e0_greek_alpha_tr9_c1+e0_greek_alpha_tr9_c2))-e0_greek_alpha_tr9_c2)/((((((e0_greek_alpha_tr9_c1+e0_greek_alpha_tr9_c2))-e0_greek_alpha_tr9_c2))*e0_x_L_tr9_c2)+((1.0-e0_x_L_tr9_c2)))))))))))  # noqa: E501,E226
#     EQ_alg275 = (e0_M_D_c1-((e0_HU_D_c1*e0_M_c1)))  # noqa: E501,E226
#     EQ_alg276 = (e0_M_D_c2-((e0_HU_D_c2*e0_M_c2)))  # noqa: E501,E226
#     EQ_alg277 = (e0_M_D-(((e0_M_D_c1+e0_M_D_c2))))  # noqa: E501,E226
#     EQ_alg278 = ((e0_LI*e0_V_tot_tr9)-((e0_V_L_tr9*100.0)))  # noqa: E501,E226
#     EQ_alg279 = (e0_PDI-((((e0_p_tr9-e0_p_tr0))*1000.0)))  # noqa: E501,E226
#     EQ_alg280 = (e0_PI_C-((e0_p_tr0*1000.0)))  # noqa: E501,E226
#     EQ_alg281 = (e0_PI_B-((e0_p_tr9*1000.0)))  # noqa: E501,E226
#     EQ_alg282 = ((e0_w_L_C_c1*(((e0_x_L_tr0_c1*e0_M_c1)+(e0_x_L_tr0_c2*e0_M_c2))))-((e0_x_L_tr0_c1*e0_M_c1)))  # noqa: E501,E226
#     EQ_alg283 = ((e0_w_L_C_c2*(((e0_x_L_tr0_c1*e0_M_c1)+(e0_x_L_tr0_c2*e0_M_c2))))-((e0_x_L_tr0_c2*e0_M_c2)))  # noqa: E501,E226
#     EQ_alg284 = ((e0_w_L_D_c1*e0_M_D)-(e0_M_D_c1))  # noqa: E501,E226
#     EQ_alg285 = ((e0_w_L_D_c2*e0_M_D)-(e0_M_D_c2))  # noqa: E501,E226
#     EQ_alg286 = ((e0_w_L_B_c1*(((e0_x_L_tr9_c1*e0_M_c1)+(e0_x_L_tr9_c2*e0_M_c2))))-((e0_x_L_tr9_c1*e0_M_c1)))  # noqa: E501,E226
#     EQ_alg287 = ((e0_w_L_B_c2*(((e0_x_L_tr9_c1*e0_M_c1)+(e0_x_L_tr9_c2*e0_M_c2))))-((e0_x_L_tr9_c2*e0_M_c2)))  # noqa: E501,E226
#     EQ_alg288 = (e0_WI-((e0_M_D*1000.0)))  # noqa: E501,E226
#     EQ_alg289 = (e0_Q_R-((e0_Q_PLS_R+e0_Q_err_R)))  # noqa: E501,E226
#     EQ_alg290 = (e0_rr-((e0_rr_PLS+e0_rr_err)))  # noqa: E501,E226

#     order_state_var = ["e0_HU_tr1_c1", "e0_HU_tr2_c1", "e0_HU_tr3_c1", "e0_HU_tr4_c1", "e0_HU_tr5_c1", "e0_HU_tr6_c1", "e0_HU_tr7_c1", "e0_HU_tr8_c1", "e0_HU_tr1_c2", "e0_HU_tr2_c2", "e0_HU_tr3_c2", "e0_HU_tr4_c2", "e0_HU_tr5_c2", "e0_HU_tr6_c2", "e0_HU_tr7_c2", "e0_HU_tr8_c2", "e0_U_tr1", "e0_U_tr2", "e0_U_tr3", "e0_U_tr4", "e0_U_tr5", "e0_U_tr6", "e0_U_tr7", "e0_U_tr8", "e0_HU_tr9_c1", "e0_HU_tr9_c2", "e0_U_tr9", "e0_HU_D_c1", "e0_HU_D_c2", ]  # noqa: E501
#     order_eqs_diff = {"e0_HU_tr1_c1": EQ_diff1, "e0_HU_tr2_c1": EQ_diff2, "e0_HU_tr3_c1": EQ_diff3, "e0_HU_tr4_c1": EQ_diff4, "e0_HU_tr5_c1": EQ_diff5, "e0_HU_tr6_c1": EQ_diff6, "e0_HU_tr7_c1": EQ_diff7, "e0_HU_tr8_c1": EQ_diff8, "e0_HU_tr1_c2": EQ_diff9, "e0_HU_tr2_c2": EQ_diff10, "e0_HU_tr3_c2": EQ_diff11, "e0_HU_tr4_c2": EQ_diff12, "e0_HU_tr5_c2": EQ_diff13, "e0_HU_tr6_c2": EQ_diff14, "e0_HU_tr7_c2": EQ_diff15, "e0_HU_tr8_c2": EQ_diff16, "e0_U_tr1": EQ_diff17, "e0_U_tr2": EQ_diff18, "e0_U_tr3": EQ_diff19, "e0_U_tr4": EQ_diff20, "e0_U_tr5": EQ_diff21, "e0_U_tr6": EQ_diff22, "e0_U_tr7": EQ_diff23, "e0_U_tr8": EQ_diff24, "e0_HU_tr9_c1": EQ_diff25, "e0_HU_tr9_c2": EQ_diff26, "e0_U_tr9": EQ_diff27, "e0_HU_D_c1": EQ_diff28, "e0_HU_D_c2": EQ_diff29, }  # noqa: E501

#     for state_var_name in order_state_var:
#         model.set_rhs(state_var_name, order_eqs_diff[state_var_name])

#     dict_algebraic_equations = {"EQ_alg30": EQ_alg30,"EQ_alg31": EQ_alg31,"EQ_alg32": EQ_alg32,"EQ_alg33": EQ_alg33,"EQ_alg34": EQ_alg34,"EQ_alg35": EQ_alg35,"EQ_alg36": EQ_alg36,"EQ_alg37": EQ_alg37,"EQ_alg38": EQ_alg38,"EQ_alg39": EQ_alg39,"EQ_alg40": EQ_alg40,"EQ_alg41": EQ_alg41,"EQ_alg42": EQ_alg42,"EQ_alg43": EQ_alg43,"EQ_alg44": EQ_alg44,"EQ_alg45": EQ_alg45,"EQ_alg46": EQ_alg46,"EQ_alg47": EQ_alg47,"EQ_alg48": EQ_alg48,"EQ_alg49": EQ_alg49,"EQ_alg50": EQ_alg50,"EQ_alg51": EQ_alg51,"EQ_alg52": EQ_alg52,"EQ_alg53": EQ_alg53,"EQ_alg54": EQ_alg54,"EQ_alg55": EQ_alg55,"EQ_alg56": EQ_alg56,"EQ_alg57": EQ_alg57,"EQ_alg58": EQ_alg58,"EQ_alg59": EQ_alg59,"EQ_alg60": EQ_alg60,"EQ_alg61": EQ_alg61,"EQ_alg62": EQ_alg62,"EQ_alg63": EQ_alg63,"EQ_alg64": EQ_alg64,"EQ_alg65": EQ_alg65,"EQ_alg66": EQ_alg66,"EQ_alg67": EQ_alg67,"EQ_alg68": EQ_alg68,"EQ_alg69": EQ_alg69,"EQ_alg70": EQ_alg70,"EQ_alg71": EQ_alg71,"EQ_alg72": EQ_alg72,"EQ_alg73": EQ_alg73,"EQ_alg74": EQ_alg74,"EQ_alg75": EQ_alg75,"EQ_alg76": EQ_alg76,"EQ_alg77": EQ_alg77,"EQ_alg78": EQ_alg78,"EQ_alg79": EQ_alg79,"EQ_alg80": EQ_alg80,"EQ_alg81": EQ_alg81,"EQ_alg82": EQ_alg82,"EQ_alg83": EQ_alg83,"EQ_alg84": EQ_alg84,"EQ_alg85": EQ_alg85,"EQ_alg86": EQ_alg86,"EQ_alg87": EQ_alg87,"EQ_alg88": EQ_alg88,"EQ_alg89": EQ_alg89,"EQ_alg90": EQ_alg90,"EQ_alg91": EQ_alg91,"EQ_alg92": EQ_alg92,"EQ_alg93": EQ_alg93,"EQ_alg94": EQ_alg94,"EQ_alg95": EQ_alg95,"EQ_alg96": EQ_alg96,"EQ_alg97": EQ_alg97,"EQ_alg98": EQ_alg98,"EQ_alg99": EQ_alg99,"EQ_alg100": EQ_alg100,"EQ_alg101": EQ_alg101,"EQ_alg102": EQ_alg102,"EQ_alg103": EQ_alg103,"EQ_alg104": EQ_alg104,"EQ_alg105": EQ_alg105,"EQ_alg106": EQ_alg106,"EQ_alg107": EQ_alg107,"EQ_alg108": EQ_alg108,"EQ_alg109": EQ_alg109,"EQ_alg110": EQ_alg110,"EQ_alg111": EQ_alg111,"EQ_alg112": EQ_alg112,"EQ_alg113": EQ_alg113,"EQ_alg114": EQ_alg114,"EQ_alg115": EQ_alg115,"EQ_alg116": EQ_alg116,"EQ_alg117": EQ_alg117,"EQ_alg118": EQ_alg118,"EQ_alg119": EQ_alg119,"EQ_alg120": EQ_alg120,"EQ_alg121": EQ_alg121,"EQ_alg122": EQ_alg122,"EQ_alg123": EQ_alg123,"EQ_alg124": EQ_alg124,"EQ_alg125": EQ_alg125,"EQ_alg126": EQ_alg126,"EQ_alg127": EQ_alg127,"EQ_alg128": EQ_alg128,"EQ_alg129": EQ_alg129,"EQ_alg130": EQ_alg130,"EQ_alg131": EQ_alg131,"EQ_alg132": EQ_alg132,"EQ_alg133": EQ_alg133,"EQ_alg134": EQ_alg134,"EQ_alg135": EQ_alg135,"EQ_alg136": EQ_alg136,"EQ_alg137": EQ_alg137,"EQ_alg138": EQ_alg138,"EQ_alg139": EQ_alg139,"EQ_alg140": EQ_alg140,"EQ_alg141": EQ_alg141,"EQ_alg142": EQ_alg142,"EQ_alg143": EQ_alg143,"EQ_alg144": EQ_alg144,"EQ_alg145": EQ_alg145,"EQ_alg146": EQ_alg146,"EQ_alg147": EQ_alg147,"EQ_alg148": EQ_alg148,"EQ_alg149": EQ_alg149,"EQ_alg150": EQ_alg150,"EQ_alg151": EQ_alg151,"EQ_alg152": EQ_alg152,"EQ_alg153": EQ_alg153,"EQ_alg154": EQ_alg154,"EQ_alg155": EQ_alg155,"EQ_alg156": EQ_alg156,"EQ_alg157": EQ_alg157,"EQ_alg158": EQ_alg158,"EQ_alg159": EQ_alg159,"EQ_alg160": EQ_alg160,"EQ_alg161": EQ_alg161,"EQ_alg162": EQ_alg162,"EQ_alg163": EQ_alg163,"EQ_alg164": EQ_alg164,"EQ_alg165": EQ_alg165,"EQ_alg166": EQ_alg166,"EQ_alg167": EQ_alg167,"EQ_alg168": EQ_alg168,"EQ_alg169": EQ_alg169,"EQ_alg170": EQ_alg170,"EQ_alg171": EQ_alg171,"EQ_alg172": EQ_alg172,"EQ_alg173": EQ_alg173,"EQ_alg174": EQ_alg174,"EQ_alg175": EQ_alg175,"EQ_alg176": EQ_alg176,"EQ_alg177": EQ_alg177,"EQ_alg178": EQ_alg178,"EQ_alg179": EQ_alg179,"EQ_alg180": EQ_alg180,"EQ_alg181": EQ_alg181,"EQ_alg182": EQ_alg182,"EQ_alg183": EQ_alg183,"EQ_alg184": EQ_alg184,"EQ_alg185": EQ_alg185,"EQ_alg186": EQ_alg186,"EQ_alg187": EQ_alg187,"EQ_alg188": EQ_alg188,"EQ_alg189": EQ_alg189,"EQ_alg190": EQ_alg190,"EQ_alg191": EQ_alg191,"EQ_alg192": EQ_alg192,"EQ_alg193": EQ_alg193,"EQ_alg194": EQ_alg194,"EQ_alg195": EQ_alg195,"EQ_alg196": EQ_alg196,"EQ_alg197": EQ_alg197,"EQ_alg198": EQ_alg198,"EQ_alg199": EQ_alg199,"EQ_alg200": EQ_alg200,"EQ_alg201": EQ_alg201,"EQ_alg202": EQ_alg202,"EQ_alg203": EQ_alg203,"EQ_alg204": EQ_alg204,"EQ_alg205": EQ_alg205,"EQ_alg206": EQ_alg206,"EQ_alg207": EQ_alg207,"EQ_alg208": EQ_alg208,"EQ_alg209": EQ_alg209,"EQ_alg210": EQ_alg210,"EQ_alg211": EQ_alg211,"EQ_alg212": EQ_alg212,"EQ_alg213": EQ_alg213,"EQ_alg214": EQ_alg214,"EQ_alg215": EQ_alg215,"EQ_alg216": EQ_alg216,"EQ_alg217": EQ_alg217,"EQ_alg218": EQ_alg218,"EQ_alg219": EQ_alg219,"EQ_alg220": EQ_alg220,"EQ_alg221": EQ_alg221,"EQ_alg222": EQ_alg222,"EQ_alg223": EQ_alg223,"EQ_alg224": EQ_alg224,"EQ_alg225": EQ_alg225,"EQ_alg226": EQ_alg226,"EQ_alg227": EQ_alg227,"EQ_alg228": EQ_alg228,"EQ_alg229": EQ_alg229,"EQ_alg230": EQ_alg230,"EQ_alg231": EQ_alg231,"EQ_alg232": EQ_alg232,"EQ_alg233": EQ_alg233,"EQ_alg234": EQ_alg234,"EQ_alg235": EQ_alg235,"EQ_alg236": EQ_alg236,"EQ_alg237": EQ_alg237,"EQ_alg238": EQ_alg238,"EQ_alg239": EQ_alg239,"EQ_alg240": EQ_alg240,"EQ_alg241": EQ_alg241,"EQ_alg242": EQ_alg242,"EQ_alg243": EQ_alg243,"EQ_alg244": EQ_alg244,"EQ_alg245": EQ_alg245,"EQ_alg246": EQ_alg246,"EQ_alg247": EQ_alg247,"EQ_alg248": EQ_alg248,"EQ_alg249": EQ_alg249,"EQ_alg250": EQ_alg250,"EQ_alg251": EQ_alg251,"EQ_alg252": EQ_alg252,"EQ_alg253": EQ_alg253,"EQ_alg254": EQ_alg254,"EQ_alg255": EQ_alg255,"EQ_alg256": EQ_alg256,"EQ_alg257": EQ_alg257,"EQ_alg258": EQ_alg258,"EQ_alg259": EQ_alg259,"EQ_alg260": EQ_alg260,"EQ_alg261": EQ_alg261,"EQ_alg262": EQ_alg262,"EQ_alg263": EQ_alg263,"EQ_alg264": EQ_alg264,"EQ_alg265": EQ_alg265,"EQ_alg266": EQ_alg266,"EQ_alg267": EQ_alg267,"EQ_alg268": EQ_alg268,"EQ_alg269": EQ_alg269,"EQ_alg270": EQ_alg270,"EQ_alg271": EQ_alg271,"EQ_alg272": EQ_alg272,"EQ_alg273": EQ_alg273,"EQ_alg274": EQ_alg274,"EQ_alg275": EQ_alg275,"EQ_alg276": EQ_alg276,"EQ_alg277": EQ_alg277,"EQ_alg278": EQ_alg278,"EQ_alg279": EQ_alg279,"EQ_alg280": EQ_alg280,"EQ_alg281": EQ_alg281,"EQ_alg282": EQ_alg282,"EQ_alg283": EQ_alg283,"EQ_alg284": EQ_alg284,"EQ_alg285": EQ_alg285,"EQ_alg286": EQ_alg286,"EQ_alg287": EQ_alg287,"EQ_alg288": EQ_alg288,"EQ_alg289": EQ_alg289,"EQ_alg290": EQ_alg290,}  # noqa: E501
#     try:
#         Eq_fun_e0_h_L_tr1_c1 = e0_h_L_tr1_c1 - fun_213932__liquid_enthalpy_adj(e0_T_tr1,e0_greek_Deltah_f_c1,e0_A_LV_c1,e0_B_LV_c1,e0_C_LV_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_L_tr1_c1"] = Eq_fun_e0_h_L_tr1_c1  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_L_tr0_c2 = e0_h_L_tr0_c2 - fun_213932__liquid_enthalpy_adj(e0_T_tr0,e0_greek_Deltah_f_c2,e0_A_LV_c2,e0_B_LV_c2,e0_C_LV_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_L_tr0_c2"] = Eq_fun_e0_h_L_tr0_c2  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_L_tr6_c1 = e0_h_L_tr6_c1 - fun_213932__liquid_enthalpy_adj(e0_T_tr6,e0_greek_Deltah_f_c1,e0_A_LV_c1,e0_B_LV_c1,e0_C_LV_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_L_tr6_c1"] = Eq_fun_e0_h_L_tr6_c1  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_V_tr9_c1 = e0_h_V_tr9_c1 - fun_210593__vaporenthalpy(e0_T_tr9,e0_greek_Deltah_f_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_V_tr9_c1"] = Eq_fun_e0_h_V_tr9_c1  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_V_tr2_c1 = e0_h_V_tr2_c1 - fun_210593__vaporenthalpy(e0_T_tr2,e0_greek_Deltah_f_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_V_tr2_c1"] = Eq_fun_e0_h_V_tr2_c1  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_V_tr4_c1 = e0_h_V_tr4_c1 - fun_210593__vaporenthalpy(e0_T_tr4,e0_greek_Deltah_f_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_V_tr4_c1"] = Eq_fun_e0_h_V_tr4_c1  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_V_tr8_c2 = e0_h_V_tr8_c2 - fun_210593__vaporenthalpy(e0_T_tr8,e0_greek_Deltah_f_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_V_tr8_c2"] = Eq_fun_e0_h_V_tr8_c2  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_V_tr4_c2 = e0_h_V_tr4_c2 - fun_210593__vaporenthalpy(e0_T_tr4,e0_greek_Deltah_f_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_V_tr4_c2"] = Eq_fun_e0_h_V_tr4_c2  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_V_tr7_c2 = e0_h_V_tr7_c2 - fun_210593__vaporenthalpy(e0_T_tr7,e0_greek_Deltah_f_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_V_tr7_c2"] = Eq_fun_e0_h_V_tr7_c2  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_L_tr0_c1 = e0_h_L_tr0_c1 - fun_213932__liquid_enthalpy_adj(e0_T_tr0,e0_greek_Deltah_f_c1,e0_A_LV_c1,e0_B_LV_c1,e0_C_LV_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_L_tr0_c1"] = Eq_fun_e0_h_L_tr0_c1  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_V_tr1_c1 = e0_h_V_tr1_c1 - fun_210593__vaporenthalpy(e0_T_tr1,e0_greek_Deltah_f_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_V_tr1_c1"] = Eq_fun_e0_h_V_tr1_c1  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_V_tr3_c2 = e0_h_V_tr3_c2 - fun_210593__vaporenthalpy(e0_T_tr3,e0_greek_Deltah_f_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_V_tr3_c2"] = Eq_fun_e0_h_V_tr3_c2  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_L_tr2_c1 = e0_h_L_tr2_c1 - fun_213932__liquid_enthalpy_adj(e0_T_tr2,e0_greek_Deltah_f_c1,e0_A_LV_c1,e0_B_LV_c1,e0_C_LV_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_L_tr2_c1"] = Eq_fun_e0_h_L_tr2_c1  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_V_tr3_c1 = e0_h_V_tr3_c1 - fun_210593__vaporenthalpy(e0_T_tr3,e0_greek_Deltah_f_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_V_tr3_c1"] = Eq_fun_e0_h_V_tr3_c1  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_L_tr5_c1 = e0_h_L_tr5_c1 - fun_213932__liquid_enthalpy_adj(e0_T_tr5,e0_greek_Deltah_f_c1,e0_A_LV_c1,e0_B_LV_c1,e0_C_LV_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_L_tr5_c1"] = Eq_fun_e0_h_L_tr5_c1  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_L_tr9_c1 = e0_h_L_tr9_c1 - fun_213932__liquid_enthalpy_adj(e0_T_tr9,e0_greek_Deltah_f_c1,e0_A_LV_c1,e0_B_LV_c1,e0_C_LV_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_L_tr9_c1"] = Eq_fun_e0_h_L_tr9_c1  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_L_tr1_c2 = e0_h_L_tr1_c2 - fun_213932__liquid_enthalpy_adj(e0_T_tr1,e0_greek_Deltah_f_c2,e0_A_LV_c2,e0_B_LV_c2,e0_C_LV_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_L_tr1_c2"] = Eq_fun_e0_h_L_tr1_c2  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_V_tr5_c1 = e0_h_V_tr5_c1 - fun_210593__vaporenthalpy(e0_T_tr5,e0_greek_Deltah_f_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_V_tr5_c1"] = Eq_fun_e0_h_V_tr5_c1  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_L_tr6_c2 = e0_h_L_tr6_c2 - fun_213932__liquid_enthalpy_adj(e0_T_tr6,e0_greek_Deltah_f_c2,e0_A_LV_c2,e0_B_LV_c2,e0_C_LV_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_L_tr6_c2"] = Eq_fun_e0_h_L_tr6_c2  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_V_tr7_c1 = e0_h_V_tr7_c1 - fun_210593__vaporenthalpy(e0_T_tr7,e0_greek_Deltah_f_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_V_tr7_c1"] = Eq_fun_e0_h_V_tr7_c1  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_L_tr3_c2 = e0_h_L_tr3_c2 - fun_213932__liquid_enthalpy_adj(e0_T_tr3,e0_greek_Deltah_f_c2,e0_A_LV_c2,e0_B_LV_c2,e0_C_LV_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_L_tr3_c2"] = Eq_fun_e0_h_L_tr3_c2  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_L_tr5_c2 = e0_h_L_tr5_c2 - fun_213932__liquid_enthalpy_adj(e0_T_tr5,e0_greek_Deltah_f_c2,e0_A_LV_c2,e0_B_LV_c2,e0_C_LV_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_L_tr5_c2"] = Eq_fun_e0_h_L_tr5_c2  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_feed_tr9_c2 = e0_h_feed_tr9_c2 - fun_213932__liquid_enthalpy_adj(e0_T_feed,e0_greek_Deltah_f_c2,e0_A_LV_c2,e0_B_LV_c2,e0_C_LV_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_feed_tr9_c2"] = Eq_fun_e0_h_feed_tr9_c2  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_L_tr2_c2 = e0_h_L_tr2_c2 - fun_213932__liquid_enthalpy_adj(e0_T_tr2,e0_greek_Deltah_f_c2,e0_A_LV_c2,e0_B_LV_c2,e0_C_LV_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_L_tr2_c2"] = Eq_fun_e0_h_L_tr2_c2  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_L_tr4_c2 = e0_h_L_tr4_c2 - fun_213932__liquid_enthalpy_adj(e0_T_tr4,e0_greek_Deltah_f_c2,e0_A_LV_c2,e0_B_LV_c2,e0_C_LV_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_L_tr4_c2"] = Eq_fun_e0_h_L_tr4_c2  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_L_tr7_c1 = e0_h_L_tr7_c1 - fun_213932__liquid_enthalpy_adj(e0_T_tr7,e0_greek_Deltah_f_c1,e0_A_LV_c1,e0_B_LV_c1,e0_C_LV_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_L_tr7_c1"] = Eq_fun_e0_h_L_tr7_c1  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_L_tr8_c1 = e0_h_L_tr8_c1 - fun_213932__liquid_enthalpy_adj(e0_T_tr8,e0_greek_Deltah_f_c1,e0_A_LV_c1,e0_B_LV_c1,e0_C_LV_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_L_tr8_c1"] = Eq_fun_e0_h_L_tr8_c1  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_V_tr6_c2 = e0_h_V_tr6_c2 - fun_210593__vaporenthalpy(e0_T_tr6,e0_greek_Deltah_f_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_V_tr6_c2"] = Eq_fun_e0_h_V_tr6_c2  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_L_tr8_c2 = e0_h_L_tr8_c2 - fun_213932__liquid_enthalpy_adj(e0_T_tr8,e0_greek_Deltah_f_c2,e0_A_LV_c2,e0_B_LV_c2,e0_C_LV_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_L_tr8_c2"] = Eq_fun_e0_h_L_tr8_c2  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_L_tr4_c1 = e0_h_L_tr4_c1 - fun_213932__liquid_enthalpy_adj(e0_T_tr4,e0_greek_Deltah_f_c1,e0_A_LV_c1,e0_B_LV_c1,e0_C_LV_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_L_tr4_c1"] = Eq_fun_e0_h_L_tr4_c1  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_V_tr2_c2 = e0_h_V_tr2_c2 - fun_210593__vaporenthalpy(e0_T_tr2,e0_greek_Deltah_f_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_V_tr2_c2"] = Eq_fun_e0_h_V_tr2_c2  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_feed_tr9_c1 = e0_h_feed_tr9_c1 - fun_213932__liquid_enthalpy_adj(e0_T_feed,e0_greek_Deltah_f_c1,e0_A_LV_c1,e0_B_LV_c1,e0_C_LV_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_feed_tr9_c1"] = Eq_fun_e0_h_feed_tr9_c1  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_V_tr5_c2 = e0_h_V_tr5_c2 - fun_210593__vaporenthalpy(e0_T_tr5,e0_greek_Deltah_f_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_V_tr5_c2"] = Eq_fun_e0_h_V_tr5_c2  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_V_tr6_c1 = e0_h_V_tr6_c1 - fun_210593__vaporenthalpy(e0_T_tr6,e0_greek_Deltah_f_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_V_tr6_c1"] = Eq_fun_e0_h_V_tr6_c1  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_V_tr8_c1 = e0_h_V_tr8_c1 - fun_210593__vaporenthalpy(e0_T_tr8,e0_greek_Deltah_f_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_V_tr8_c1"] = Eq_fun_e0_h_V_tr8_c1  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_V_tr9_c2 = e0_h_V_tr9_c2 - fun_210593__vaporenthalpy(e0_T_tr9,e0_greek_Deltah_f_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_V_tr9_c2"] = Eq_fun_e0_h_V_tr9_c2  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_L_tr3_c1 = e0_h_L_tr3_c1 - fun_213932__liquid_enthalpy_adj(e0_T_tr3,e0_greek_Deltah_f_c1,e0_A_LV_c1,e0_B_LV_c1,e0_C_LV_c1,e0_T_ref,e0_c_V_p_c1)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_L_tr3_c1"] = Eq_fun_e0_h_L_tr3_c1  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_L_tr9_c2 = e0_h_L_tr9_c2 - fun_213932__liquid_enthalpy_adj(e0_T_tr9,e0_greek_Deltah_f_c2,e0_A_LV_c2,e0_B_LV_c2,e0_C_LV_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_L_tr9_c2"] = Eq_fun_e0_h_L_tr9_c2  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_L_tr7_c2 = e0_h_L_tr7_c2 - fun_213932__liquid_enthalpy_adj(e0_T_tr7,e0_greek_Deltah_f_c2,e0_A_LV_c2,e0_B_LV_c2,e0_C_LV_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_L_tr7_c2"] = Eq_fun_e0_h_L_tr7_c2  # noqa: E501
#     except KeyError:
#         pass
#     try:
#         Eq_fun_e0_h_V_tr1_c2 = e0_h_V_tr1_c2 - fun_210593__vaporenthalpy(e0_T_tr1,e0_greek_Deltah_f_c2,e0_T_ref,e0_c_V_p_c2)  # noqa: E501,E231
#         dict_algebraic_equations["Eq_fun_e0_h_V_tr1_c2"] = Eq_fun_e0_h_V_tr1_c2  # noqa: E501
#     except KeyError:
#         pass

#     # fmt:on

#     for alg_var_name, alg_eq in dict_algebraic_equations.items():
#         model.set_alg(alg_var_name, alg_eq)

#     # Build the model
#     model.setup()

#     return model

def template_simulator(model: do_mpc.model.Model) -> do_mpc.simulator.Simulator:
    """
    Here could be the doc
    """
    simulator = do_mpc.simulator.Simulator(model)

    # fmt:off
    # Parameters
    p_template = simulator.get_p_template()
    p_template["e0_greek_kappa"] = 0.0424670248823593
    p_template["e0_greek_kappa_hyst"] = 0.0
    p_template["e0_h_tot"] = 0.179372959955645
    

    p_template["e0_p_tr0"] = 1.028
    p_template["e0_F_feed_tr9"] = 0.0
    p_template["e0_F_B"] = 0.0
    p_template["e0_T_feed"] = 369.0
    p_template["e0_V_tot_tr9"] = 0.06
    p_template["e0_x_feed_tr9_c1"] = 1.0
    p_template["e0_x_feed_tr9_c2"] = 0.0
    p_template["e0_greek_lambda_activity"] = 1.0
    p_template["e0_Q_err_R"] = -0

    
    p_template["e0_rr_err"] = -0.15
    p_template["e0_E_murphree"] = 0.5
    p_template["e0_x_N2"] = 0.04273159753760128
    p_template["e0_h_weir"] = 0.0428980603490154

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
    simulator.z0["e0_h_L_tr0_c1"] = -268.58667967377306
    simulator.z0["e0_h_L_tr0_c2"] = -279.74980624341106
    simulator.z0["e0_h_L_tr1_c1"] = -268.5840016424736
    simulator.z0["e0_h_L_tr1_c2"] = -279.74852078838734
    simulator.z0["e0_h_L_tr2_c1"] = -268.58101702763827
    simulator.z0["e0_h_L_tr2_c2"] = -279.7470881732664
    simulator.z0["e0_h_L_tr3_c1"] = -268.57745799568966
    simulator.z0["e0_h_L_tr3_c2"] = -279.745379837931
    simulator.z0["e0_h_L_tr4_c1"] = -273.40470068980386
    simulator.z0["e0_h_L_tr4_c2"] = -279.745379837931
    simulator.z0["e0_h_L_tr5_c1"] = -273.830357160426
    simulator.z0["e0_h_L_tr5_c2"] = -279.7470881732664
    simulator.z0["e0_h_L_tr6_c1"] = -274.361043998245
    simulator.z0["e0_h_L_tr6_c2"] = -279.74852078838734
    simulator.z0["e0_h_L_tr7_c1"] = -275.02965626035314
    simulator.z0["e0_h_L_tr7_c2"] = -279.74980624341106
    simulator.z0["e0_h_L_tr8_c1"] = -276.0327214865629
    simulator.z0["e0_h_L_tr8_c2"] = -279.1064
    simulator.z0["e0_h_L_tr9_c1"] = -276.0327214865629
    simulator.z0["e0_h_L_tr9_c2"] = -279.1064
    simulator.z0["e0_h_V_tr1_c1"] = -222.5154794722554
    simulator.z0["e0_h_V_tr1_c2"] = -224.66731843303066
    simulator.z0["e0_h_V_tr2_c1"] = -222.66551036577548
    simulator.z0["e0_h_V_tr2_c2"] = -224.04399213560927
    simulator.z0["e0_h_V_tr3_c1"] = -222.84419813230258
    simulator.z0["e0_h_V_tr3_c2"] = -224.66731843303066
    simulator.z0["e0_h_V_tr4_c1"] = -223.05919971756836
    simulator.z0["e0_h_V_tr4_c2"] = -224.66731843303066
    simulator.z0["e0_h_V_tr5_c1"] = -223.32078817261953
    simulator.z0["e0_h_V_tr5_c2"] = -224.66731843303066
    simulator.z0["e0_h_V_tr6_c1"] = -223.64283440315705
    simulator.z0["e0_h_V_tr6_c2"] = -224.66731843303066
    simulator.z0["e0_h_V_tr7_c1"] = -224.04399213560927
    simulator.z0["e0_h_V_tr7_c2"] = -224.66731843303066
    simulator.z0["e0_h_V_tr8_c1"] = -224.66731843303066
    simulator.z0["e0_h_V_tr8_c2"] = -224.66731843303066
    simulator.z0["e0_h_V_tr9_c1"] = -234.7950341801212
    simulator.z0["e0_h_V_tr9_c2"] = -234.7950341801212
    simulator.z0["e0_h_feed_tr9_c1"] = -267.24625000000003
    simulator.z0["e0_h_feed_tr9_c2"] = -279.1064
    simulator.z0["e0_greek_alpha_tr0_c1"] = 0.2351429354392572
    simulator.z0["e0_greek_alpha_tr0_c2"] = 0.7631454951212454
    simulator.z0["e0_Q_C"] = -6.523701526549227
    simulator.z0["e0_H_tr3"] = -437.6430827846278
    simulator.z0["e0_H_tr4"] = -450.57244799358017
    simulator.z0["e0_H_tr5"] = -467.62452786805704
    simulator.z0["e0_H_tr6"] = -490.8363841412743
    simulator.z0["e0_H_tr7"] = -523.718843984456
    simulator.z0["e0_H_tr8"] = -567.5990273974493
    simulator.z0["e0_T_tr0"] = 350.65552056045817
    simulator.z0["e0_HU_L_tr1"] = 1.531452265249518
    simulator.z0["e0_HU_L_tr2"] = 1.559456739563267
    simulator.z0["e0_HU_L_tr3"] = 1.5946752189871898
    simulator.z0["e0_HU_L_tr4"] = 1.639938968554021
    simulator.z0["e0_HU_L_tr5"] = 1.6996504734289253
    simulator.z0["e0_HU_L_tr6"] = 1.78095389570281
    simulator.z0["e0_HU_L_tr7"] = 1.8961714684634854
    simulator.z0["e0_HU_L_tr8"] = 2.0481797816092135
    simulator.z0["e0_HU_V_tr1"] = 0.009872927021616044
    simulator.z0["e0_HU_V_tr2"] = 0.009878324766557745
    simulator.z0["e0_HU_V_tr3"] = 0.009883161936084081
    simulator.z0["e0_HU_V_tr4"] = 0.009887174119314049
    simulator.z0["e0_HU_V_tr5"] = 0.009889951129046556
    simulator.z0["e0_HU_V_tr6"] = 0.009890833343322277
    simulator.z0["e0_HU_V_tr7"] = 0.009888490118108982
    simulator.z0["e0_HU_V_tr8"] = 0.00994531915762383
    simulator.z0["e0_K_tr1_c1"] = 1.025420063583459
    simulator.z0["e0_K_tr2_c1"] = 1.0411322516446555
    simulator.z0["e0_h_L_tr0"] = -272.341630830957
    simulator.z0["e0_K_tr3_c1"] = 1.0623703906173516
    simulator.z0["e0_K_tr4_c1"] = 1.0919271122264025
    simulator.z0["e0_K_tr5_c1"] = 1.1345580581470547
    simulator.z0["e0_K_tr6_c1"] = 1.198892032128109
    simulator.z0["e0_K_tr7_c1"] = 1.301940671871093
    simulator.z0["e0_K_tr8_c1"] = 1.3444118979951032
    simulator.z0["e0_K_tr1_c2"] = 0.7841467084089263
    simulator.z0["e0_K_tr2_c2"] = 0.7653201825636156
    simulator.z0["e0_K_tr3_c2"] = 0.7439878686148155
    simulator.z0["e0_K_tr4_c2"] = 0.7198440502546042
    simulator.z0["e0_h_V_tr1"] = -222.5154794722554
    simulator.z0["e0_K_tr5_c2"] = 0.6926441585426342
    simulator.z0["e0_K_tr6_c2"] = 0.662341353240467
    simulator.z0["e0_K_tr7_c2"] = 0.6294079353975278
    simulator.z0["e0_K_tr8_c2"] = 0.548176644972168
    simulator.z0["e0_L_tr1"] = 0.04492692427772357
    simulator.z0["e0_L_tr2"] = 0.04490010771008785
    simulator.z0["e0_L_tr3"] = 0.04486760576397996
    simulator.z0["e0_L_tr4"] = 0.04482770582700153
    simulator.z0["e0_L_tr5"] = 0.04477803372371564
    simulator.z0["e0_L_tr6"] = 0.0447152683529458
    simulator.z0["e0_L_tr7"] = 0.04463833444907638
    simulator.z0["e0_L_tr8"] = 0.044524003948311894
    simulator.z0["e0_L_weir"] = 0.034999999999999996
    simulator.z0["e0_T_tr1"] = 350.74344133801816
    simulator.z0["e0_T_tr2"] = 350.8534679443456
    simulator.z0["e0_T_tr3"] = 350.9942260460794
    simulator.z0["e0_T_tr4"] = 351.1784453225865
    simulator.z0["e0_T_tr5"] = 351.4253644221073
    simulator.z0["e0_T_tr6"] = 351.7650323018968
    simulator.z0["e0_T_tr7"] = 352.2469792638617
    simulator.z0["e0_p_LV_o_tr0_c1"] = 0.9817008896971963
    simulator.z0["e0_T_tr8"] = 350.7057830907694
    simulator.z0["e0_V_L_tr1"] = 7.233532258647407E-5
    simulator.z0["e0_p_LV_o_tr0_c2"] = 0.42782914918567516
    simulator.z0["e0_V_L_tr2"] = 7.229214613712267E-5
    simulator.z0["e0_V_L_tr3"] = 7.223981585201635E-5
    simulator.z0["e0_V_L_tr4"] = 7.217557431180602E-5
    simulator.z0["e0_V_L_tr5"] = 7.209559893684995E-5
    simulator.z0["e0_V_L_tr6"] = 7.199454253437222E-5
    simulator.z0["e0_V_L_tr7"] = 7.187067385554102E-5
    simulator.z0["e0_V_L_tr8"] = 7.168659417977357E-5
    simulator.z0["e0_V_V_tr1"] = 2.7986265468649515E-4
    simulator.z0["e0_V_V_tr2"] = 2.7990583113584656E-4
    simulator.z0["e0_V_V_tr3"] = 2.7995816142095285E-4
    simulator.z0["e0_V_V_tr4"] = 2.800224029611632E-4
    simulator.z0["e0_V_V_tr5"] = 2.801023783361193E-4
    simulator.z0["e0_V_V_tr6"] = 2.80203434738597E-4
    simulator.z0["e0_V_V_tr7"] = 2.8032730341742815E-4
    simulator.z0["e0_V_V_tr8"] = 2.805113830931956E-4
    simulator.z0["e0_V_tot"] = 3.521979772729692E-4
    simulator.z0["e0_greek_gamma_tr0_c1"] = 1.0613090669250131
    simulator.z0["e0_x_L_tr0_c1"] = 0.7356270437444828
    simulator.z0["e0_x_L_tr0_c2"] = 0.26437295625551716
    simulator.z0["e0_h_L_tr1"] = -272.5395090155686
    simulator.z0["e0_h_L_tr2"] = -272.775304948304
    simulator.z0["e0_h_L_tr3"] = -273.05916107765603
    simulator.z0["e0_h_L_tr4"] = -273.40470068980386
    simulator.z0["e0_h_L_tr5"] = -273.830357160426
    simulator.z0["e0_h_L_tr6"] = -274.361043998245
    simulator.z0["e0_h_L_tr7"] = -275.02965626035314
    simulator.z0["e0_h_L_tr8"] = -276.0327214865629
    simulator.z0["e0_x_V_tr0_c1"] = 0.7455652042722005
    simulator.z0["e0_x_V_tr1_c1"] = 0.7041925249734182
    simulator.z0["e0_h_V_tr2"] = -222.66551036577548
    simulator.z0["e0_h_V_tr3"] = -222.84419813230258
    simulator.z0["e0_h_V_tr4"] = -223.05919971756836
    simulator.z0["e0_h_V_tr5"] = -223.32078817261953
    simulator.z0["e0_x_V_tr0_c2"] = 0.2117031981901982
    simulator.z0["e0_h_V_tr6"] = -223.64283440315705
    simulator.z0["e0_h_V_tr7"] = -224.04399213560927
    simulator.z0["e0_h_V_tr8"] = -224.66731843303066
    simulator.z0["e0_h_V_tr9"] = -234.7950341801212
    simulator.z0["e0_p_tr1"] = 1.0287279898371606
    simulator.z0["e0_p_tr2"] = 1.0294544801464822
    simulator.z0["e0_p_tr3"] = 1.0301791861328784
    simulator.z0["e0_p_tr4"] = 1.030901748803911
    simulator.z0["e0_p_tr5"] = 1.0316217101830152
    simulator.z0["e0_p_tr6"] = 1.0323384791673296
    simulator.z0["e0_x_V_tr1_c2"] = 0.2530758774889805
    simulator.z0["e0_p_tr7"] = 1.0330512846427424
    simulator.z0["e0_p_tr8"] = 1.0337634730725649
    simulator.z0["e0_p_LV_o_tr1_c1"] = 0.9851386170393878
    simulator.z0["e0_p_LV_o_tr2_c1"] = 0.9894548379638869
    simulator.z0["e0_p_LV_o_tr3_c1"] = 0.9949996216364193
    simulator.z0["e0_p_LV_o_tr4_c1"] = 1.0022955950194359
    simulator.z0["e0_p_LV_o_tr5_c1"] = 1.0121447537667205
    simulator.z0["e0_p_LV_o_tr6_c1"] = 1.0258253221481428
    simulator.z0["e0_p_LV_o_tr7_c1"] = 1.0455007737785422
    simulator.z0["e0_p_LV_o_tr8_c1"] = 0.9836649407717356
    simulator.z0["e0_p_LV_o_tr1_c2"] = 0.4293796355465061
    simulator.z0["e0_p_LV_o_tr2_c2"] = 0.4313266110360318
    simulator.z0["e0_p_LV_o_tr3_c2"] = 0.43382821045895337
    simulator.z0["e0_p_LV_o_tr4_c2"] = 0.4371206306027115
    simulator.z0["e0_p_LV_o_tr5_c2"] = 0.4415665557682198
    simulator.z0["e0_p_LV_o_tr6_c2"] = 0.44774451644497654
    simulator.z0["e0_p_LV_o_tr7_c2"] = 0.45663477806745884
    simulator.z0["e0_p_LV_o_tr8_c2"] = 0.4287149535530157
    simulator.z0["e0_v_L_tr1"] = 4.723315523953895E-5
    simulator.z0["e0_v_L_tr2"] = 4.635726295130727E-5
    simulator.z0["e0_v_L_tr3"] = 4.53006449162089E-5
    simulator.z0["e0_v_L_tr4"] = 4.4011134374985425E-5
    simulator.z0["e0_v_L_tr5"] = 4.241789712881505E-5
    simulator.z0["e0_v_L_tr6"] = 4.0424708751913724E-5
    simulator.z0["e0_v_L_tr7"] = 3.7903045716524566E-5
    simulator.z0["e0_v_L_tr8"] = 3.500014736179597E-5
    simulator.z0["e0_x_L_tr1_c1"] = 0.7175334132036232
    simulator.z0["e0_x_L_tr2_c1"] = 0.695938435683118
    simulator.z0["e0_x_L_tr3_c1"] = 0.6698876951728031
    simulator.z0["e0_x_L_tr4_c1"] = 0.6380950289690687
    simulator.z0["e0_x_L_tr5_c1"] = 0.5988140317755188
    simulator.z0["e0_x_L_tr6_c1"] = 0.5496723065067487
    simulator.z0["e0_x_L_tr7_c1"] = 0.48750112713324867
    simulator.z0["e0_x_L_tr8_c1"] = 0.4159306548766263
    simulator.z0["e0_x_L_tr1_c2"] = 0.2824665867963769
    simulator.z0["e0_x_L_tr2_c2"] = 0.304061564316882
    simulator.z0["e0_x_L_tr3_c2"] = 0.3301123048271969
    simulator.z0["e0_x_L_tr4_c2"] = 0.3619049710309314
    simulator.z0["e0_x_L_tr5_c2"] = 0.40118596822448116
    simulator.z0["e0_x_L_tr6_c2"] = 0.4503276934932513
    simulator.z0["e0_x_L_tr7_c2"] = 0.5124988728667512
    simulator.z0["e0_x_L_tr8_c2"] = 0.5840693451233736
    simulator.z0["e0_x_V_tr2_c1"] = 0.6868720643218674
    simulator.z0["e0_x_V_tr3_c1"] = 0.6661998748889054
    simulator.z0["e0_x_V_tr4_c1"] = 0.6412623243886181
    simulator.z0["e0_x_V_tr5_c1"] = 0.6108282099062736
    simulator.z0["e0_x_V_tr6_c1"] = 0.5732257528354027
    simulator.z0["e0_x_V_tr7_c1"] = 0.5261839324067579
    simulator.z0["e0_x_V_tr8_c1"] = 0.46666942729471883
    simulator.z0["e0_greek_gamma_tr0_c2"] = 1.9241243481807733
    simulator.z0["e0_x_V_tr9_c1"] = 0.41593065765714077
    simulator.z0["e0_x_V_tr2_c2"] = 0.2703963381405313
    simulator.z0["e0_x_V_tr3_c2"] = 0.2910685275734934
    simulator.z0["e0_x_V_tr4_c2"] = 0.3160060780737806
    simulator.z0["e0_x_V_tr5_c2"] = 0.3464401925561252
    simulator.z0["e0_x_V_tr6_c2"] = 0.3840426496269961
    simulator.z0["e0_x_V_tr7_c2"] = 0.43108447005564093
    simulator.z0["e0_x_V_tr8_c2"] = 0.49059897516767986
    simulator.z0["e0_x_V_tr9_c2"] = 0.5840693423428592
    simulator.z0["e0_greek_alpha_tr9_c1"] = 0.23702645798528302
    simulator.z0["e0_greek_alpha_tr9_c2"] = 0.7960798622139318
    simulator.z0["e0_greek_gamma_tr9_c1"] = 3.116511731054789
    simulator.z0["e0_greek_gamma_tr9_c2"] = 1.0236263794943494
    simulator.z0["e0_H_tr9"] = -426276.21643741714
    simulator.z0["e0_HU_L_tr9"] = 1528.0029186928748
    simulator.z0["e0_HU_V_tr9"] = 0.9124037471174476
    simulator.z0["e0_K_tr9_c1"] = 4.438835316196634
    simulator.z0["e0_K_tr9_c2"] = 0.6444566411475581
    simulator.z0["e0_T_tr9"] = 361.2172061152755
    simulator.z0["e0_V_L_tr9"] = 0.033509989817832174
    simulator.z0["e0_V_V_tr9"] = 0.02649001018216783
    simulator.z0["e0_h_L_tr9"] = -278.8358473378441
    simulator.z0["e0_h_feed_tr9"] = -266.518911067034
    simulator.z0["e0_p_tr9"] = 1.0343877873160434
    simulator.z0["e0_p_LV_o_tr9_c1"] = 1.4732744289805553
    simulator.z0["e0_p_LV_o_tr9_c2"] = 0.6512318287333
    simulator.z0["e0_v_L_tr9"] = 2.1930579718066366E-5
    simulator.z0["e0_x_L_tr9_c1"] = 0.09370265577086699
    simulator.z0["e0_x_L_tr9_c2"] = 0.906297344229133
    simulator.z0["e0_LI"] = 55.849983029720285
    simulator.z0["e0_M_D"] = 4.6E-11
    simulator.z0["e0_M_D_c1"] = 4.6E-11
    simulator.z0["e0_M_D_c2"] = 0.0
    simulator.z0["e0_PDI"] = 6.387787316043392
    simulator.z0["e0_PI_B"] = 1034.3877873160434
    simulator.z0["e0_PI_C"] = 1028.0
    simulator.z0["e0_WI"] = 4.6E-8
    simulator.z0["e0_w_L_B_c1"] = 0.20899875016882152
    simulator.z0["e0_w_L_B_c2"] = 0.7910012498311784
    simulator.z0["e0_w_L_C_c1"] = 0.8767094719264747
    simulator.z0["e0_w_L_C_c2"] = 0.1232905280735251
    simulator.z0["e0_w_L_D_c1"] = 1.0
    simulator.z0["e0_w_L_D_c2"] = 0.0
    # simulator.z0["e0_Q_PLS_R"] = 4.01352643106891
    simulator.z0["e0_Q_R"] = 5.0
    # simulator.z0["e0_rr_PLS"] = 1.14654938382886
    simulator.z0["e0_rr"] = 1.0
    simulator.z0["e0_greek_alpha_tr1_c1"] = 0.23515901926041946
    simulator.z0["e0_greek_alpha_tr2_c1"] = 0.23517913721246883
    simulator.z0["e0_F_L_tr0"] = 0.12533445125038103
    simulator.z0["e0_greek_alpha_tr3_c1"] = 0.23520485842055386
    simulator.z0["e0_greek_alpha_tr4_c1"] = 0.23523849452985698
    simulator.z0["e0_greek_alpha_tr5_c1"] = 0.2352835310531188
    simulator.z0["e0_greek_alpha_tr6_c1"] = 0.23534539512417524
    simulator.z0["e0_greek_alpha_tr7_c1"] = 0.23543299570585924
    simulator.z0["e0_greek_alpha_tr8_c1"] = 0.2351521310871577
    simulator.z0["e0_greek_alpha_tr1_c2"] = 0.7634219715986589
    simulator.z0["e0_greek_alpha_tr2_c2"] = 0.7637679080483655
    simulator.z0["e0_greek_alpha_tr3_c2"] = 0.7642103799889578
    simulator.z0["e0_greek_alpha_tr4_c2"] = 0.7647893226287549
    simulator.z0["e0_F_V_tr1"] = 0.13092926803807683
    simulator.z0["e0_greek_alpha_tr5_c2"] = 0.7655650455203697
    simulator.z0["e0_greek_alpha_tr6_c2"] = 0.7666316516402236
    simulator.z0["e0_greek_alpha_tr7_c2"] = 0.7681440457791607
    simulator.z0["e0_greek_alpha_tr8_c2"] = 0.7633035558428382
    simulator.z0["e0_greek_gamma_tr1_c1"] = 1.0707917672734264
    simulator.z0["e0_greek_gamma_tr2_c1"] = 1.0832210018661845
    simulator.z0["e0_greek_gamma_tr3_c1"] = 1.0999319402533052
    simulator.z0["e0_greek_gamma_tr4_c1"] = 1.123091406521421
    simulator.z0["e0_greek_gamma_tr5_c1"] = 1.1563906446106496
    simulator.z0["e0_greek_gamma_tr6_c1"] = 1.2065040220894707
    simulator.z0["e0_F_D"] = 0.0
    simulator.z0["e0_greek_gamma_tr7_c1"] = 1.2864375783713762
    simulator.z0["e0_greek_gamma_tr8_c1"] = 1.412883447712515
    simulator.z0["e0_greek_gamma_tr1_c2"] = 1.8786956816250082
    simulator.z0["e0_greek_gamma_tr2_c2"] = 1.8266025571531963
    simulator.z0["e0_greek_gamma_tr3_c2"] = 1.7666919727776953
    simulator.z0["e0_greek_gamma_tr4_c2"] = 1.6976743679435904
    simulator.z0["e0_greek_gamma_tr5_c2"] = 1.6182084943930775
    simulator.z0["e0_greek_gamma_tr6_c2"] = 1.5271219192651402
    simulator.z0["e0_greek_gamma_tr7_c2"] = 1.423918429907011
    simulator.z0["e0_greek_gamma_tr8_c2"] = 1.32182231496065
    simulator.z0["e0_K_tr0_c1"] = 1.0135097813657457
    simulator.z0["e0_A_col"] = 0.0019634953750000002
    simulator.z0["e0_A_active"] = 0.0016100662075
    simulator.z0["e0_F_L_tr1"] = 0.12520530153713902
    simulator.z0["e0_F_L_tr2"] = 0.1250514495170773
    simulator.z0["e0_F_L_tr3"] = 0.12486639301129202
    simulator.z0["e0_F_L_tr4"] = 0.12464142515250536
    simulator.z0["e0_F_L_tr5"] = 0.12436478070354529
    simulator.z0["e0_F_L_tr6"] = 0.12402045487778747
    simulator.z0["e0_F_L_tr7"] = 0.12396676369586346
    simulator.z0["e0_F_L_tr8"] = 0.1212483129923828
    simulator.z0["e0_K_tr0_c2"] = 0.8007747887253132
    simulator.z0["e0_F_V_tr2"] = 0.13079435318159413
    simulator.z0["e0_F_V_tr3"] = 0.13063363332332983
    simulator.z0["e0_F_V_tr4"] = 0.13044031603194287
    simulator.z0["e0_F_V_tr5"] = 0.13020530577222736
    simulator.z0["e0_F_V_tr6"] = 0.1299163121155942
    simulator.z0["e0_F_V_tr7"] = 0.1295566158335842
    simulator.z0["e0_F_V_tr8"] = 0.12950052784786692
    simulator.z0["e0_F_V_tr9"] = 0.12124831261297246
    simulator.z0["e0_H_tr1"] = -419.5781275418934
    simulator.z0["e0_H_tr2"] = -427.5808499137625

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

    simulator.u0["e0_rr_PLS"] = 1.14654938382886 # Given the defined rr_err, this refers to closed manual valve position (rr_act=1)
    simulator.u0["e0_Q_PLS_R"] = 4.01352643106891

    # fmt:on
    return simulator


if __name__ == "__main__":
    model = template_model()
    simulator = template_simulator(model)

    params_simulator = {
        "integration_tool": "idas",
        "abstol": 1e-10,
        "reltol": 1e-10,
        "t_step": 30.0,
    }
    simulator.set_param(**params_simulator)
    simulator.setup()
    simulator.set_initial_guess()

    for idx in range(100):
        u0 = simulator.u0.master
        simulator.make_step(u0)

    fig, ax, graphics = do_mpc.graphics.default_plot(
        simulator.data, dae_states_list=[], inputs_list=[]
    )

    plt.show()