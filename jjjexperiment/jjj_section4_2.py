# ============================================================================
# 第四章 暖冷房設備
# 第二節 ダクト式セントラル空調機
# Ver.05（エネルギー消費性能計算プログラム（住宅版）Ver.02.01～）
# ============================================================================

import numpy as np

from functools import lru_cache

import datetime

import jjjexperiment.jjj_section3_1 as ld

from pyhees.section3_2_8 import \
    get_r_env

from jjjexperiment.jjj_section3_1 import \
    get_A_NR

from pyhees.section3_1_d import \
    get_V_A

from pyhees.section3_1_e import \
    get_U_s, get_ro_air, get_c_p_air, get_phi

from pyhees.section4_7_i import \
    get_A_A_R

from pyhees.section11_1 import \
    get_Theta_ex, \
    get_X_ex, \
    load_climate, \
    get_climate_df

from pyhees.section11_2 import \
    calc_I_s_d_t

from pyhees.section11_3 import \
    load_schedule, \
    get_schedule_ac

from pyhees.section11_5 import \
    calc_h_ex, \
    get_J

from pyhees.section11_6 import \
    get_table_7

from jjjexperiment.jjj_section3_1_e2 import \
    calc_Theta, get_r_A_uf_i, calc_A_s_ufvnt_i

from jjjexperiment.jjj_section4_3 import \
    get_C_af_H, \
    get_C_af_C

from jjjexperiment.constants import PROCESS_TYPE_3
import jjjexperiment.constants as constants

from jjjexperiment.logger import LimitedLoggerAdapter as _logger  # デバッグ用ロガー
from jjjexperiment.logger import log_res
from jjjexperiment.options import *

from injector import Injector
from jjjexperiment.di_container import *

# NOTE: 旧コード -> 置換版 calc.py
# 未処理負荷と機器の計算に必要な変数を取得
def calc_Q_UT_A(A_A, A_MR, A_OR, r_env, mu_H, mu_C, q_hs_rtd_H, q_hs_rtd_C, V_hs_dsgn_H, V_hs_dsgn_C, Q,
             VAV, general_ventilation, duct_insulation, region, L_H_d_t_i, L_CS_d_t_i, L_CL_d_t_i, type, input_C_af_H, input_C_af_C):
    """

    Args:
      A_A: param A_MR:
      A_OR: param r_env:
      mu_H: param mu_C:
      q_hs_rtd_H: param q_hs_rtd_C:
      V_hs_dsgn_H: param V_hs_dsgn_C:
      Q: param VAV:
      general_ventilation: param duct_insulation:
      region: param L_H_d_t_i:
      L_CS_d_t_i: param L_CL_d_t_i:
      A_MR:
      r_env: 床面積の合計に対する外皮の部位の面積の合計の比 (-)
      mu_C:
      q_hs_rtd_C:
      V_hs_dsgn_C:
      VAV:
      duct_insulation:
      L_H_d_t_i:
      L_CL_d_t_i:
      type:
      input_C_af_H:
      input_C_af_C:

    Returns:

    """
    raise NotImplementedError("置き換え以前のコードであり、現状は使用されることはないはずです。")

    # 外気条件
    climate = load_climate(region)
    X_ex_d_t = get_X_ex(climate)
    Theta_ex_d_t = get_Theta_ex(climate)
    J_d_t = calc_I_s_d_t(0, 0, get_climate_df(climate))
    h_ex_d_t = calc_h_ex(X_ex_d_t, Theta_ex_d_t)

    A_HCZ_i = np.array([ld.get_A_HCZ_i(i, A_A, A_MR, A_OR) for i in range(1, 6)])
    A_HCZ_R_i = [ld.get_A_HCZ_R_i(i) for i in range(1, 6)]

    A_NR = get_A_NR(A_A, A_MR, A_OR)

    # (67)
    L_wtr = get_L_wtr()

    # (66d)
    n_p_NR_d_t = calc_n_p_NR_d_t(A_NR)

    # (66c)
    n_p_OR_d_t = calc_n_p_OR_d_t(A_OR)

    # (66b)
    n_p_MR_d_t = calc_n_p_MR_d_t(A_MR)

    # (66a)
    n_p_d_t = get_n_p_d_t(n_p_MR_d_t, n_p_OR_d_t, n_p_NR_d_t)

    # 人体発熱
    q_p_H = get_q_p_H()
    q_p_CS = get_q_p_CS()
    q_p_CL = get_q_p_CL()

    # (65d)
    w_gen_NR_d_t = calc_w_gen_NR_d_t(A_NR)

    # (65c)
    w_gen_OR_d_t = calc_w_gen_OR_d_t(A_OR)

    # (65b)
    w_gen_MR_d_t = calc_w_gen_MR_d_t(A_MR)

    # (65a)
    w_gen_d_t = get_w_gen_d_t(w_gen_MR_d_t, w_gen_OR_d_t, w_gen_NR_d_t)

    # (64d)
    q_gen_NR_d_t = calc_q_gen_NR_d_t(A_NR)

    # (64c)
    q_gen_OR_d_t = calc_q_gen_OR_d_t(A_OR)

    # (64b)
    q_gen_MR_d_t = calc_q_gen_MR_d_t(A_MR)

    # (64a)
    q_gen_d_t = get_q_gen_d_t(q_gen_MR_d_t, q_gen_OR_d_t, q_gen_NR_d_t)

    # (63)
    V_vent_l_NR_d_t = get_V_vent_l_NR_d_t()
    V_vent_l_OR_d_t = get_V_vent_l_OR_d_t()
    V_vent_l_MR_d_t = get_V_vent_l_MR_d_t()
    V_vent_l_d_t = get_V_vent_l_d_t(V_vent_l_MR_d_t, V_vent_l_OR_d_t, V_vent_l_NR_d_t)

    # (62)
    V_vent_g_i = get_V_vent_g_i(A_HCZ_i, A_HCZ_R_i)

    # (61)
    U_prt = get_U_prt()

    # (60)
    A_prt_i = get_A_prt_i(A_HCZ_i, r_env, A_MR, A_NR, A_OR)

    # (59)
    Theta_SAT_d_t = get_Theta_SAT_d_t(Theta_ex_d_t, J_d_t)

    # (58)
    l_duct_ex_i = get_l_duct_ex_i(A_A)

    # (57)
    l_duct_in_i = get_l_duct_in_i(A_A)

    # (56)
    l_duct_i = get_l_duct__i(l_duct_in_i, l_duct_ex_i)

    # (51)
    X_star_HBR_d_t = get_X_star_HBR_d_t(X_ex_d_t, region)

    # (50)
    Theta_star_HBR_d_t = get_Theta_star_HBR_d_t(Theta_ex_d_t, region)

    # (55)
    Theta_attic_d_t = get_Theta_attic_d_t(Theta_SAT_d_t, Theta_star_HBR_d_t)

    # (54)
    Theta_sur_d_t_i = get_Theta_sur_d_t_i(Theta_star_HBR_d_t, Theta_attic_d_t, l_duct_in_i, l_duct_ex_i, duct_insulation)

    # (40)
    Q_hat_hs_d_t = calc_Q_hat_hs_d_t(Q, A_A, V_vent_l_d_t, V_vent_g_i, mu_H, mu_C, J_d_t, q_gen_d_t, n_p_d_t, q_p_H,
                                     q_p_CS, q_p_CL, X_ex_d_t, w_gen_d_t, Theta_ex_d_t, L_wtr, region)

    # (39)
    V_hs_min = get_V_hs_min(V_vent_g_i)

    # (38)
    Q_hs_rtd_C = get_Q_hs_rtd_C(q_hs_rtd_C)

    # (37)
    Q_hs_rtd_H = get_Q_hs_rtd_H(q_hs_rtd_H)

    # (36)
    V_dash_hs_supply_d_t = get_V_dash_hs_supply_d_t(V_hs_min, V_hs_dsgn_H, V_hs_dsgn_C, Q_hs_rtd_H, Q_hs_rtd_C, Q_hat_hs_d_t, region)

    # (45)
    r_supply_des_i = get_r_supply_des_i(A_HCZ_i)

    # (44)
    V_dash_supply_d_t_i = get_V_dash_supply_d_t_i(r_supply_des_i, V_dash_hs_supply_d_t, V_vent_g_i)

    # (53)
    X_star_NR_d_t = get_X_star_NR_d_t(X_star_HBR_d_t, L_CL_d_t_i, L_wtr, V_vent_l_NR_d_t, V_dash_supply_d_t_i, region)

    # (52)
    Theta_star_NR_d_t = get_Theta_star_NR_d_t(Theta_star_HBR_d_t, Q, A_NR, V_vent_l_NR_d_t, V_dash_supply_d_t_i, U_prt,
                                              A_prt_i, L_H_d_t_i, L_CS_d_t_i, region)

    # (49)
    X_NR_d_t = get_X_NR_d_t(X_star_NR_d_t)

    # (47)
    X_HBR_d_t_i = get_X_HBR_d_t_i(X_star_HBR_d_t)

    # (11)
    Q_star_trs_prt_d_t_i = get_Q_star_trs_prt_d_t_i(U_prt, A_prt_i, Theta_star_HBR_d_t, Theta_star_NR_d_t)

    # (10)
    L_star_CL_d_t_i = get_L_star_CL_d_t_i(L_CS_d_t_i, L_CL_d_t_i, region)

    # (9)
    L_star_CS_d_t_i = get_L_star_CS_d_t_i(L_CS_d_t_i, Q_star_trs_prt_d_t_i, region)

    # (8)
    L_star_H_d_t_i = get_L_star_H_d_t_i(L_H_d_t_i, Q_star_trs_prt_d_t_i, region,
                                        A_A, A_MR, A_OR, Q, r_A_ufvnt, underfloor_insulation, Theta_ex_d_t, Theta_ex_d_t,
                                        L_dash_H_R_d_t, L_dash_CS_R_d_t, R_g)

    # (33)
    L_star_CL_d_t = get_L_star_CL_d_t(L_star_CL_d_t_i)

    # (32)
    L_star_CS_d_t = get_L_star_CS_d_t(L_star_CS_d_t_i)

    # (31)
    L_star_CL_max_d_t = get_L_star_CL_max_d_t(L_star_CS_d_t)

    # (30)
    L_star_dash_CL_d_t = get_L_star_dash_CL_d_t(L_star_CL_max_d_t, L_star_CL_d_t)

    # (29)
    L_star_dash_C_d_t = get_L_star_dash_C_d_t(L_star_CS_d_t, L_star_dash_CL_d_t)

    # (28)
    SHF_dash_d_t = get_SHF_dash_d_t(L_star_CS_d_t, L_star_dash_C_d_t)

    # (27)
    Q_hs_max_C_d_t = get_Q_hs_max_C_d_t(type, q_hs_rtd_C, input_C_af_C)

    # (26)
    Q_hs_max_CL_d_t = get_Q_hs_max_CL_d_t(Q_hs_max_C_d_t, SHF_dash_d_t, L_star_dash_CL_d_t)

    # (25)
    Q_hs_max_CS_d_t = get_Q_hs_max_CS_d_t(Q_hs_max_C_d_t, SHF_dash_d_t)

    # (24)
    C_df_H_d_t = get_C_df_H_d_t(Theta_ex_d_t, h_ex_d_t)

    # (23)
    Q_hs_max_H_d_t = get_Q_hs_max_H_d_t(type, q_hs_rtd_H, C_df_H_d_t, input_C_af_H)

    # (20)
    X_star_hs_in_d_t = get_X_star_hs_in_d_t(X_star_NR_d_t)

    # (19)
    Theta_star_hs_in_d_t = get_Theta_star_hs_in_d_t(Theta_star_NR_d_t)

    # (18)
    X_hs_out_min_C_d_t = get_X_hs_out_min_C_d_t(X_star_hs_in_d_t, Q_hs_max_CL_d_t, V_dash_supply_d_t_i)

    # (22)
    X_req_d_t_i = get_X_req_d_t_i(X_star_HBR_d_t, L_star_CL_d_t_i, V_dash_supply_d_t_i, region)

    # (21)
    Theta_req_d_t_i = get_Theta_req_d_t_i(Theta_sur_d_t_i, Theta_star_HBR_d_t, V_dash_supply_d_t_i,
                        L_star_H_d_t_i, L_star_CS_d_t_i, l_duct_i, region)

    # (15)
    X_hs_out_d_t = get_X_hs_out_d_t(X_NR_d_t, X_req_d_t_i, V_dash_supply_d_t_i, X_hs_out_min_C_d_t, L_star_CL_d_t_i, region)

    # 式(14)(46)(48)の条件に合わせてTheta_NR_d_tを初期化
    Theta_NR_d_t = np.zeros(24 * 365)

    # (17)
    Theta_hs_out_min_C_d_t = get_Theta_hs_out_min_C_d_t(Theta_star_hs_in_d_t, Q_hs_max_CS_d_t, V_dash_supply_d_t_i)

    # (16)
    Theta_hs_out_max_H_d_t = get_Theta_hs_out_max_H_d_t(Theta_star_hs_in_d_t, Q_hs_max_H_d_t, V_dash_supply_d_t_i)

    # L_star_H_d_t_i，L_star_CS_d_t_iの暖冷房区画1～5を合算し0以上だった場合の順序で計算
    # (14)
    Theta_hs_out_d_t = get_Theta_hs_out_d_t(VAV, Theta_req_d_t_i, V_dash_supply_d_t_i,
                                            L_star_H_d_t_i, L_star_CS_d_t_i, region, Theta_NR_d_t,
                                            Theta_hs_out_max_H_d_t, Theta_hs_out_min_C_d_t)

    # (43)
    V_supply_d_t_i = get_V_supply_d_t_i(L_star_H_d_t_i, L_star_CS_d_t_i, Theta_sur_d_t_i, l_duct_i, Theta_star_HBR_d_t,
                                        V_vent_g_i, V_dash_supply_d_t_i, VAV, region, Theta_hs_out_d_t)
    V_supply_d_t_i = cap_V_supply_d_t_i(V_supply_d_t_i, V_dash_supply_d_t_i, V_vent_g_i, region, V_hs_dsgn_H, V_hs_dsgn_C)

    # (41)
    Theta_supply_d_t_i = get_Thata_supply_d_t_i(Theta_sur_d_t_i, Theta_hs_out_d_t, Theta_star_HBR_d_t, l_duct_i,
                                                   V_supply_d_t_i, L_star_H_d_t_i, L_star_CS_d_t_i, region)

    # (46)
    Theta_HBR_d_t_i = get_Theta_HBR_d_t_i(Theta_star_HBR_d_t, V_supply_d_t_i, Theta_supply_d_t_i, U_prt, A_prt_i, Q,
                                             A_HCZ_i, L_star_H_d_t_i, L_star_CS_d_t_i, region)

    # (48)
    Theta_NR_d_t = get_Theta_NR_d_t(Theta_star_NR_d_t, Theta_star_HBR_d_t, Theta_HBR_d_t_i, A_NR, V_vent_l_NR_d_t,
                                        V_dash_supply_d_t_i, V_supply_d_t_i, U_prt, A_prt_i, Q)

     # L_star_H_d_t_i，L_star_CS_d_t_iの暖冷房区画1～5を合算し0以下だった場合の為に再計算
     # (14)
    Theta_hs_out_d_t = get_Theta_hs_out_d_t(VAV, Theta_req_d_t_i, V_dash_supply_d_t_i,
                                            L_star_H_d_t_i, L_star_CS_d_t_i, region, Theta_NR_d_t,
                                            Theta_hs_out_max_H_d_t, Theta_hs_out_min_C_d_t)

    # (42)
    X_supply_d_t_i = get_X_supply_d_t_i(X_star_HBR_d_t, X_hs_out_d_t, L_star_CL_d_t_i, region)

    # (35)
    V_hs_vent_d_t = get_V_hs_vent_d_t(V_vent_g_i, general_ventilation)

    # (34)
    V_hs_supply_d_t = get_V_hs_supply_d_t(V_supply_d_t_i)

    # (13)
    X_hs_in_d_t = get_X_hs_in_d_t(X_NR_d_t)

    # (12)
    Theta_hs_in_d_t = get_Theta_hs_in_d_t(Theta_NR_d_t)

    # (7)
    L_dash_CL_d_t_i = get_L_dash_CL_d_t_i(V_supply_d_t_i, X_HBR_d_t_i, X_supply_d_t_i, region)

    # (6)
    L_dash_CS_d_t_i = get_L_dash_CS_d_t_i(V_supply_d_t_i, Theta_supply_d_t_i, Theta_HBR_d_t_i, region)

    # (5)
    L_dash_H_d_t_i = get_L_dash_H_d_t_i(V_supply_d_t_i, Theta_supply_d_t_i, Theta_HBR_d_t_i, region)

    # (4)
    Q_UT_CL_d_t_i = get_Q_UT_CL_d_t_i(L_star_CL_d_t_i, L_dash_CL_d_t_i)

    # (3)
    Q_UT_CS_d_t_i = get_Q_UT_CS_d_t_i(L_star_CS_d_t_i, L_dash_CS_d_t_i)

    # (2)
    Q_UT_H_d_t_i = get_Q_UT_H_d_t_i(L_star_H_d_t_i, L_dash_H_d_t_i)

    # (1)
    E_C_UT_d_t = get_E_C_UT_d_t(Q_UT_CL_d_t_i, Q_UT_CS_d_t_i, region)

    return E_C_UT_d_t, Q_UT_H_d_t_i, Q_UT_CS_d_t_i, Q_UT_CL_d_t_i, Theta_hs_out_d_t, Theta_hs_in_d_t, \
           X_hs_out_d_t, X_hs_in_d_t, V_hs_supply_d_t, V_hs_vent_d_t, C_df_H_d_t


# ============================================================================
# 5 暖房エネルギー消費量
# ============================================================================

# ============================================================================
# 5.1 消費電力量
# ============================================================================

# 4_2_aで実装

# ============================================================================
# 5.2 ガス消費量
# ============================================================================

# 日付dの時刻tにおける1時間当たりのガス消費量 (MJ/h)
def get_E_G_H_d_t():
    """ガス消費量
    ガス消費量は0とする

    Args:

    Returns:
      ndarray: ガス消費量

    """
    # ガス消費量は0とする
    return np.zeros(24 * 365)

# ============================================================================
# 5.3 灯油消費量
# ============================================================================

# 日付dの時刻tにおける1時間当たりの灯油消費量 (MJ/h)
def get_E_K_H_d_t():
    """灯油消費量
    灯油消費量は0とする

    Args:

    Returns:
      ndarray: 灯油消費量

    """
    # 灯油消費量は0とする
    return np.zeros(24 * 365)

# ============================================================================
# 5.4 その他の燃料による一次エネルギ―消費量
# ============================================================================

# 日付dの時刻tにおける1時間当たりのその他の燃料による一次エネルギー消費量 (MJ/h)
def get_E_M_H_d_t():
    """その他の燃料による一次エネルギー消費量

    Args:

    Returns:
      ndarray: その他の燃料による一次エネルギー消費量

    """
    # その他の燃料による一次エネルギー消費量は0とする
    return np.zeros(24 * 365)


# ============================================================================
# 6 冷房エネルギー消費量
# ============================================================================

# ============================================================================
# 6.1 消費電力量
# ============================================================================

# 4_2_aで実装

# ============================================================================
# 6.2 ガス消費量
# ============================================================================

# 日付dの時刻tにおける1時間当たりのガス消費量 (MJ/h)
def get_E_G_C_d_t():
    """ """
    # ガス消費量は0とする
    return np.zeros(24 * 365)

# ============================================================================
# 6.3 灯油消費量
# ============================================================================

# 日付dの時刻tにおける1時間当たりの灯油消費量 (MJ/h)
def get_E_K_C_d_t():
    """ """
    # 灯油消費量は0とする
    return np.zeros(24 * 365)

# ============================================================================
# 6.4 その他の燃料による一次エネルギ―消費量
# ============================================================================

# 日付dの時刻tにおける1時間当たりのその他の燃料による一次エネルギー消費量 (MJ/h)
def get_E_M_C_d_t():
    """ """
    # その他の燃料による一次エネルギー消費量は0とする
    return np.zeros(24 * 365)


# ============================================================================
# 7 冷房設備の未処理冷房負荷の設計一次エネルギー消費量相当値
# ============================================================================

def get_E_C_UT_d_t(Q_UT_CL_d_t_i, Q_UT_CS_d_t_i, region):
    """(1)

    Args:
      Q_UT_CL_d_t_i: 日付dの時刻tにおける1時間当たりの暖冷房区画iに設置された冷房機器の未処理冷房潜熱負荷（MJ/h）
      Q_UT_CS_d_t_i: 日付dの時刻tにおける1時間当たりの暖冷房区画iに設置された冷房機器の未処理冷房顕熱負荷（MJ/h）
      region: 地域区分

    Returns:
      日付dの時刻tにおける1時間当たりの冷房設備の未処理冷房負荷の設計一次エネルギー消費量相当値（MJ/h）

    """
    # 暖房設備の未処理冷房負荷を未処理暖房負荷の設計一次エネルギー消費量相当値に換算する係数α_(UT,H)（-）を取得
    from pyhees.section4_1 import \
       get_alpha_UT_H_A

    region = 7 if region == 8 else region

    alpha_UT_H_A = get_alpha_UT_H_A(region)

    # 冷房設備の未処理冷房負荷を未処理冷房負荷の設計一次エネルギー消費量相当値に換算する係数（-）
    alpha_UT_C = alpha_UT_H_A

    return np.sum(alpha_UT_C * (Q_UT_CL_d_t_i + Q_UT_CS_d_t_i), axis=0)


# ============================================================================
# 8 未処理負荷
# ============================================================================

# メモ： i=1-5のみ i>=6 の場合はどこで計算するのか要確認
@log_res(['Q_UT_H_d_t_i'])
def get_Q_UT_H_d_t_i(L_star_H_d_t_i, L_dash_H_d_t_i):
    """(2)

    Args:
      L_star_H_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの熱損失を含む負荷バランス時の暖房負荷（MJ/h）
      L_dash_H_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの間仕切りの熱損失を含む実際の暖房負荷（MJ/h）

    Returns:
      日付dの時刻tにおける1時間当たりの暖冷房区画iに設置された暖房設備機器等の未処理暖房負荷（MJ/h）

    """
    return np.clip(L_star_H_d_t_i[:5] - L_dash_H_d_t_i[:5], 0, None)

# メモ： i=1-5のみ i>=6 の場合はどこで計算するのか要確認
@log_res(['Q_UT_CS_d_t_i'])
def get_Q_UT_CS_d_t_i(L_star_CS_d_t_i, L_dash_CS_d_t_i):
    """(3)

    Args:
      L_star_CS_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの熱損失を含む負荷バランス時の冷房顕熱負荷（MJ/h）
      L_dash_CS_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの間仕切りの熱損失を含む実際の冷房顕熱負荷（MJ/h）

    Returns:
      日付dの時刻tにおける1時間当たりの暖冷房区画iに設置された冷房機器の未処理冷房顕熱負荷（MJ/h）

    """
    return np.clip(L_star_CS_d_t_i[:5] - L_dash_CS_d_t_i[:5], 0, None)

# メモ： i=1-5のみ i>=6 の場合はどこで計算するのか要確認
@log_res(['Q_UT_CL_d_t_i'])
def get_Q_UT_CL_d_t_i(L_star_CL_d_t_i, L_dash_CL_d_t_i):
    """(4)

    Args:
      L_star_CL_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの熱損失を含む負荷バランス時の冷房潜熱負荷（MJ/h）
      L_dash_CS_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの間仕切りの熱損失を含む実際の冷房潜熱負荷（MJ/h）
      L_dash_CL_d_t_i: returns: 日付dの時刻tにおける1時間当たりの暖冷房区画iに設置された冷房機器の未処理冷房潜熱負荷（MJ/h）

    Returns:
      日付dの時刻tにおける1時間当たりの暖冷房区画iに設置された冷房機器の未処理冷房潜熱負荷（MJ/h）

    """
    return np.clip(L_star_CL_d_t_i[:5] - L_dash_CL_d_t_i[:5], 0, None)

# メモ： i=1-5のみ i>=6 の場合はどこで計算するのか要確認
@log_res(['L_dash_H_d_t_i'])
def get_L_dash_H_d_t_i(V_supply_d_t_i, Theta_supply_d_t_i, Theta_HBR_d_t_i, region):
    """(5-1)(5-2)(5-3)

    Args:
      V_supply_d_t_i: 日付dの時刻tにおける暖冷房区画iの吹き出し風量（m3/h）
      Theta_supply_d_t_i: 日付dの時刻tにおける暖冷房区画iの吹き出し温度（℃）
      Theta_HBR_d_t_i: 日付dの時刻tにおける暖冷房区画iの実際の居室の室温（℃）
      region: 地域区分

    Returns:
      日付dの時刻tにおける暖冷房区画iの1時間当たりの間仕切りの熱損失を含む実際の暖房負荷（MJ/h）

    """
    c_p_air = get_c_p_air()
    rho_air = get_rho_air()
    H, C, M = get_season_array_d_t(region)

    L_dash_H_d_t_i = np.zeros((5, 24 * 365))

    # 暖房期 (5-1)
    L_dash_H_d_t_i[:, H] = c_p_air * rho_air * V_supply_d_t_i[:, H] * (Theta_supply_d_t_i[:, H] - Theta_HBR_d_t_i[:, H]) * 10 ** -6

    # 冷房期 (5-2)
    L_dash_H_d_t_i[:, C] = 0.0

    # 中間期 (5-3)
    L_dash_H_d_t_i[:, M] = 0.0

    return L_dash_H_d_t_i

@log_res(['L_dash_CS_d_t_i'])
def get_L_dash_CS_d_t_i(V_supply_d_t_i, Theta_supply_d_t_i, Theta_HBR_d_t_i, region):
    """(6-1)(6-2)(6-3)

    Args:
      V_supply_d_t_i: 日付dの時刻tにおける暖冷房区画iの吹き出し風量（m3/h）
      Theta_supply_d_t_i: 日付dの時刻tにおける暖冷房区画iの吹き出し温度（℃）
      Theta_HBR_d_t_i: 日付dの時刻tにおける暖冷房区画iの実際の居室の室温（℃）
      region: 地域区分

    Returns:
      日付dの時刻tにおける暖冷房区画iの1時間当たりの間仕切りの熱損失を含む実際の冷房顕熱および潜熱負荷（MJ/h）

    """
    c_p_air = get_c_p_air()
    rho_air = get_rho_air()
    H, C, M = get_season_array_d_t(region)

    L_dash_CS_d_t_i = np.zeros((5, 24 * 365))

    # 暖房期 (6-1)
    L_dash_CS_d_t_i[:, H] = 0.0

    # 冷房期 (6-2)
    L_dash_CS_d_t_i[:, C] = c_p_air * rho_air * V_supply_d_t_i[:, C] * (Theta_HBR_d_t_i[:, C] - Theta_supply_d_t_i[:, C]) * 10 ** -6

    # 中間期 (6-3)
    L_dash_CS_d_t_i[:, M] = 0.0

    return L_dash_CS_d_t_i

@log_res(['L_dash_CL_d_t_i'])
def get_L_dash_CL_d_t_i(V_supply_d_t_i, X_HBR_d_t_i, X_supply_d_t_i, region):
    """(7-1)(7-2)(7-3)

    Args:
      V_supply_d_t_i: 日付dの時刻tにおける暖冷房区画iの吹き出し風量（m3/h）
      X_HBR_d_t_i: 日付dの時刻tにおける暖冷房区画iの実際の居室の絶対湿度（kg/kg(DA)）
      X_supply_d_t_i: 日付dの時刻tにおける暖冷房区画iの吹き出し絶対湿度（kg/kg(DA)）
      region: 地域区分

    Returns:
      日付dの時刻tにおける暖冷房区画iの1時間当たりの間仕切りの熱損失を含む実際の冷房顕熱および潜熱負荷（MJ/h）

    """
    L_wtr = get_L_wtr()
    rho_air = get_rho_air()
    H, C, M = get_season_array_d_t(region)

    L_dash_CL_d_t_i = np.zeros((5, 24 * 365))

    # 暖房期 (7-1)
    L_dash_CL_d_t_i[:, H] = 0.0

    # 冷房期 (7-2)
    L_dash_CL_d_t_i[:, C] = L_wtr * rho_air * V_supply_d_t_i[:, C] * (X_HBR_d_t_i[:, C] - X_supply_d_t_i[:, C]) * 10 ** -3

    # 中間期 (7-3)
    L_dash_CL_d_t_i[:, M] = 0.0

    return L_dash_CL_d_t_i


@log_res(['L_star_H_d_t_i'])
def get_L_star_H_d_t_i(L_H_d_t_i, Q_star_trs_prt_d_t_i, region,
                       A_A, A_MR, A_OR, Q, r_A_ufac, underfloor_insulation, Theta_uf_d_t_i, Theta_ex_d_t,
                       L_dash_H_R_d_t, L_dash_CS_R_d_t, R_g, di: Injector = None):
    """(8-1)(8-2)(8-3)

    Args:
      L_H_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの暖房負荷（MJ/h）
      Q_star_trs_prt_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの熱損失を含む負荷バランス時の非居室への熱移動（MJ/h）
      region: 地域区分

      A_A(float): 床面積の合計 (m2)
      A_MR(float): 主たる居室の床面積 (m2)
      A_OR(float): その他の居室の床面積 (m2)
      Q(float): 当該住戸の熱損失係数 (W/m2K)
      r_A_ufac(float): 当該住戸において、床下空間全体の面積に対する 空調空気を供給する床下空間の面積の比 (-)
      underfloor_insulation(bool): 床下空間が断熱空間内である場合はTrue
      Theta_uf_d_t_i(ndarray): 床下空間の空気の温度 (℃)
      Theta_ex_d_t(ndarray): 外気温度 (℃)
      V_sa_d_t_A(ndarray): 床下空間または居室へ供給する1時間当たりの空気の風量の合計
      H_OR_C: type H_OR_C: str
      L_dash_H_R_d_t(ndarray): 標準住戸の負荷補正前の暖房負荷 (MJ/h)
      L_dash_CS_R_d_t(ndarray): 標準住戸の負荷補正前の冷房顕熱負荷 （MJ/h）
      R_g: 地盤またはそれを覆う基礎の表面熱伝達抵抗 ((m2・K)/W)
      di: DIコンテナー

    Returns:
      日付dの時刻tにおける暖冷房区画iの1時間当たりの熱損失を含む負荷バランス時の暖房負荷

    """
    H, C, M = get_season_array_d_t(region)
    L_H_d_t_i = L_H_d_t_i[:5]
    f = L_H_d_t_i > 0

    Hf = np.logical_and(H, f)

    if constants.change_underfloor_temperature == 2:
      # FIXME: 新ロジックのみ通っていることを確認したが結果の L_star_H_d_t_i が変わっていない
      # r_A_ufvnt がNoneなのが原因だと理解
      delta_L_star = get_delta_L_star_underfloor_2023(
          region, A_A, A_MR, A_OR, Q, r_A_ufac, underfloor_insulation, Theta_uf_d_t_i, Theta_ex_d_t,
          L_dash_H_R_d_t, L_dash_CS_R_d_t, R_g, di)
    else:
      delta_L_star = np.zeros((5, 24 * 365))
    L_star_H_d_t_i = np.zeros((5, 24 * 365))
    L_star_H_d_t_i[Hf] = np.clip(L_H_d_t_i[Hf] + Q_star_trs_prt_d_t_i[Hf] + delta_L_star[Hf], 0, None)
    return L_star_H_d_t_i

def get_delta_L_star_underfloor_2023(
  region, A_A, A_MR, A_OR, Q, r_A_ufvnt, underfloor_insulation, Theta_uf_d_t, Theta_ex_d_t,
  L_dash_H_R_d_t, L_dash_CS_R_d_t, R_g, di: Injector = None):
  """
    Args:
      region: 地域区分
      A_A(float): 床面積の合計 (m2)
      A_MR(float): 主たる居室の床面積 (m2)
      A_OR(float): その他の居室の床面積 (m2)
      Q(float): 当該住戸の熱損失係数 (W/m2K)
      r_A_ufvnt(float): 当該住戸において、床下空間全体の面積に対する空気を供給する床下空間の面積の比 (-)
      underfloor_insulation(bool): 床下空間が断熱空間内である場合はTrue
      Theta_uf_d_t(ndarray): 床下空間の空気の温度 (℃)
      Theta_ex_d_t(ndarray): 外気温度 (℃)
      L_dash_H_R_d_t(ndarray): 標準住戸の負荷補正前の暖房負荷 (MJ/h)
      L_dash_CS_R_d_t(ndarray): 標準住戸の負荷補正前の冷房顕熱負荷 （MJ/h）
      R_g: 地盤またはそれを覆う基礎の表面熱伝達抵抗 ((m2・K)/W)
      di: DIコンテナー

    Returns:
      日付dの時刻tにおける暖冷房区画iの1時間当たりの床下との熱交換による熱負荷の補正 (MJ/h)
  """
  # 当該住戸の1時間当たりの換気量 (m3/h) D.3.2 (4)
  V_A = get_V_A(A_A)
  Theta_uf_d_t, _, A_s_ufvnt_i, A_s_ufvnt_A, Theta_g_avg, Theta_dash_g_surf_A_m_d_t, L_uf, H_floor, phi, Phi_A_0, _, _ = \
    calc_Theta(
      region=region, A_A=A_A, A_MR=A_MR, A_OR=A_OR, Q=Q, r_A_ufvnt=r_A_ufvnt, underfloor_insulation=underfloor_insulation,
      Theta_sa_d_t=Theta_uf_d_t, Theta_ex_d_t=Theta_ex_d_t, V_sa_d_t_A=np.repeat(V_A, 24 * 365), H_OR_C='H',
      L_dash_H_R_d_t=L_dash_H_R_d_t, L_dash_CS_R_d_t=L_dash_CS_R_d_t, R_g=R_g)
  U_s = get_U_s()

  # 床下→地盤
  underfloor_to_ground = (A_s_ufvnt_A * (np.sum(Theta_dash_g_surf_A_m_d_t, axis=1) + Theta_g_avg - Theta_uf_d_t)) / (R_g + Phi_A_0)
  # 床下→外気
  underfloor_to_outdoor = phi * L_uf * (Theta_ex_d_t - Theta_uf_d_t)
  # それ以外の部分
  delta_L_other = -U_s * np.array(A_s_ufvnt_i[:5]).reshape(-1, 1) * ((Theta_uf_d_t - Theta_ex_d_t) * H_floor).reshape(1, -1) * 3.6

  if di is not None:
    hci = di.get(HaCaInputHolder)
    df_holder = di.get(DtDataFrameHolder)
    df_holder.update_df({
        f"delta_L_{hci.flg_char()}_other_1": delta_L_other[0],
        f"delta_L_{hci.flg_char()}_other_2": delta_L_other[1],
        f"delta_L_{hci.flg_char()}_other_3": delta_L_other[2],
        f"delta_L_{hci.flg_char()}_other_4": delta_L_other[3],
        f"delta_L_{hci.flg_char()}_other_5": delta_L_other[4],
        f"underfloor_to_ground_{hci.flg_char()}": underfloor_to_ground,
        f"underfloor_to_outdoor{hci.flg_char()}": underfloor_to_outdoor,
      })

  delta_L_star = delta_L_other + np.tile(underfloor_to_ground, (5, 1)) + np.tile(underfloor_to_outdoor, (5, 1))
  return delta_L_star / 1000

@log_res(['L_star_H_i'])
def get_L_star_H_i_2023(L_H_d_t_i, Q_star_trs_prt_d_t_i, region, A_HCZ_i, A_HCZ_R_i, Theta_star_HBR_d_t, Theta_HBR_d_t_i, t: int):
    """get_L_star_H_d_t_i のループ用 時点単発計算 \n

    前時刻の値を利用: \n
      theta_star_HBR_d_t: 日付dの時刻tにおける負荷バランス時の居室の室温（℃） \n
      Theta_HBR_d_t_i: xxx \n
    Extended Args: \n
      A_HCZ_i: xxx \n
      A_HCZ_R_i: 標準住戸における暖冷房区画の床面積[m2] \n
      idx: 時系列データにおけるインデックス \n
    Returns: \n
      一時点の 日付dの時刻tにおける暖冷房区画iの1時間当たりの熱損失を含む負荷バランス時の暖房負荷 \n

    """
    H, C, M = get_season_array_d_t(region)
    L_H_d_t_i = L_H_d_t_i[:5]
    f = L_H_d_t_i > 0
    Hf = np.logical_and(H, f)[:, t:t+1]  # 5x1

    A_HCZ_i = A_HCZ_i.reshape(-1,1)
    A_HCZ_R_i = A_HCZ_R_i.reshape(-1,1)

    if 0 < t:
        cbri = get_C_BR_i(A_HCZ_i, A_HCZ_R_i)
        arr_theta = np.clip(Theta_HBR_d_t_i[:, t-1:t] - Theta_star_HBR_d_t[t-1], 0, None)  # 5x1
        carry_over = cbri * arr_theta / 1_000_000  # 過剰熱量: J/h -> MJ/h
    else:
        carry_over = np.zeros((5, 1))
    assert np.all(np.greater_equal(carry_over, 0)), "想定外の計算結果(過剰熱量がマイナス)"

    # <負荷バランス時の暖房負荷> - <過剰熱量>
    arr = L_H_d_t_i[:, t:t+1] + Q_star_trs_prt_d_t_i[:, t:t+1] - carry_over

    L_star_H_i = np.zeros((5, 1))
    L_star_H_i[Hf] = arr[Hf]
    return L_star_H_i

def get_L_star_CS_d_t_i(L_CS_d_t_i, Q_star_trs_prt_d_t_i, region,
                        A_A, A_MR, A_OR, Q, r_A_ufac, underfloor_insulation, Theta_uf_d_t, Theta_ex_d_t,
                        L_dash_H_R_d_t, L_dash_CS_R_d_t, R_g):
    """(9-2)(9-2)(9-3)

    Args:
      L_CS_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの冷房顕熱負荷（MJ/h）
      Q_star_trs_prt_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの熱損失を含む負荷バランス時の非居室への熱移動（MJ/h）
      region: 地域区分

      A_A(float): 床面積の合計 (m2)
      A_MR(float): 主たる居室の床面積 (m2)
      A_OR(float): その他の居室の床面積 (m2)
      Q(float): 当該住戸の熱損失係数 (W/m2K)
      r_A_ufac(float): 当該住戸において、床下空間全体の面積に対する 空調空気を供給する床下空間の面積の比(-)
      underfloor_insulation(bool): 床下空間が断熱空間内である場合はTrue
      Theta_uf_d_t_i(ndarray): 床下空間の空気の温度 (℃)
      Theta_ex_d_t(ndarray): 外気温度 (℃)
      V_sa_d_t_A(ndarray): 床下空間または居室へ供給する1時間当たりの空気の風量の合計
      H_OR_C: type H_OR_C: str
      L_dash_H_R_d_t(ndarray): 標準住戸の負荷補正前の暖房負荷 (MJ/h)
      L_dash_CS_R_d_t(ndarray): 標準住戸の負荷補正前の冷房顕熱負荷 （MJ/h）
      R_g: 地盤またはそれを覆う基礎の表面熱伝達抵抗 ((m2・K)/W)

    Returns:
      日付dの時刻tにおける暖冷房区画iの1時間当たりの熱損失を含む負荷バランス時の冷房顕熱負荷

    """
    H, C, M = get_season_array_d_t(region)
    L_CS_d_t_i = L_CS_d_t_i[:5]
    f = L_CS_d_t_i > 0

    Cf = np.logical_and(C, f)

    L_star_CS_d_t_i = np.zeros((5, 24 * 365))
    if constants.change_underfloor_temperature == 2:
      delta_L_star = get_delta_L_star_underfloor_2023(
          region, A_A, A_MR, A_OR, Q, r_A_ufac, underfloor_insulation, Theta_uf_d_t, Theta_ex_d_t,
          L_dash_H_R_d_t, L_dash_CS_R_d_t, R_g)
    else:
      delta_L_star = np.zeros((5, 24 * 365))
    L_star_CS_d_t_i[Cf] = np.clip(L_CS_d_t_i[Cf] + Q_star_trs_prt_d_t_i[Cf] + delta_L_star[Cf], 0, None)
    return L_star_CS_d_t_i

def get_L_star_CS_i_2023(L_CS_d_t_i, Q_star_trs_prt_d_t_i, region, A_HCZ_i, A_HCZ_R_i, Theta_star_HBR_d_t, Theta_HBR_d_t_i, t: int):
    """get_L_star_CS_d_t_i のループ用 時点単発計算 \n

    前時刻の値を利用: \n
      Theta_star_HBR_d_t: xxx \n
      Theta_HBR_d_t_i: xxx \n
    Extended Args: \n
      A_HCZ_i: xxx  \n
      A_HCZ_R_i: 標準住戸における暖冷房区画の床面積[m2]  \n
      t: 時系列データにおけるインデックス \n

    Returns: \n
      一時点の 日付dの時刻tにおける暖冷房区画iの1時間当たりの熱損失を含む負荷バランス時の冷房顕熱負荷 \n

    """
    H, C, M = get_season_array_d_t(region)
    L_CS_d_t_i = L_CS_d_t_i[:5]
    f = L_CS_d_t_i > 0
    Cf = np.logical_and(C, f)[:, t]  # 5x1

    A_HCZ_i = A_HCZ_i.reshape(-1,1)
    A_HCZ_R_i = A_HCZ_R_i.reshape(-1,1)

    if 0 < t:
        cbri = get_C_BR_i(A_HCZ_i, A_HCZ_R_i)
        arr_theta = np.clip(Theta_star_HBR_d_t[t-1] - Theta_HBR_d_t_i[:, t-1:t], 0, None)  # 5x1
        carry_over = cbri * arr_theta / 1_000_000  # 過剰熱量: J/h -> MJ/h
    else:
        carry_over = np.zeros((5, 1))

    if np.any(carry_over < 0):
        pass
    assert np.all(np.greater_equal(carry_over, 0)), "想定外の計算結果(過剰熱量がマイナス)"

    # <負荷バランス時の暖房負荷> - <過剰熱量>
    # NOTE: MATRIX[:, 0] だと shape(5, ) となりダメ MATRIX[:, 0:1] と書くと shape(5,1)
    arr = L_CS_d_t_i[:, t:t+1] + Q_star_trs_prt_d_t_i[:, t:t+1] - carry_over

    L_star_CS_i = np.zeros((5, 1))
    L_star_CS_i[Cf] = np.clip(arr, 0, None)[Cf]
    return L_star_CS_i

def get_L_star_CL_d_t_i(L_CS_d_t_i, L_CL_d_t_i, region):
    """(10-1)(10-2)(10-3)

    Args:
      L_CL_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの冷房潜熱負荷（MJ/h）
      region: 地域区分
      L_CS_d_t_i: returns: 日付dの時刻tにおける暖冷房区画iの1時間当たりの熱損失を含む負荷バランス時の冷房潜熱負荷

    Returns:
      日付dの時刻tにおける暖冷房区画iの1時間当たりの熱損失を含む負荷バランス時の冷房潜熱負荷

    """
    H, C, M = get_season_array_d_t(region)
    L_CL_d_t_i = L_CL_d_t_i[:5]
    L_CS_d_t_i = L_CS_d_t_i[:5]
    f = L_CS_d_t_i > 0

    Cf = np.logical_and(C, f)

    L_star_CL_d_t_i = np.zeros((5, 24 * 365))

    L_star_CL_d_t_i[Cf] = L_CL_d_t_i[Cf]

    return L_star_CL_d_t_i


def get_Q_star_trs_prt_d_t_i(U_prt, A_prt_i, Theta_star_HBR_d_t, Theta_star_NR_d_t):
    """(11)

    Args:
      U_prt: 間仕切りの熱貫流率（W/(m2・K)）
      A_prt_i: 暖冷房区画iから見た非居室の間仕切りの面積（m2）
      Theta_star_HBR_d_t: 日付dの時刻tにおける負荷バランス時の居室の室温（℃）
      Theta_star_NR_d_t: 日付dの時刻tにおける負荷バランス時の非居室の室温（℃）

    Returns:
      日付dの時刻tにおける暖冷房区画iの1時間当たりの熱損失を含む負荷バランス時の非居室への熱移動（MJ/h）

    """
    return U_prt * A_prt_i[:5, np.newaxis] * (Theta_star_HBR_d_t - Theta_star_NR_d_t) * 3600 * 10 ** -6


# ============================================================================
# 9 熱源機
# ============================================================================


# ============================================================================
# 9.1 熱源機の入り口における空気温度・絶対湿度
# ============================================================================

def get_Theta_hs_in_d_t(Theta_NR_d_t):
    """(12)

    Args:
      Theta_NR_d_t: 日付dの時刻tにおける非居室の室温(℃)

    Returns:
      日付dの時刻tにおける熱源機の入口における空気温度（℃）

    """
    return Theta_NR_d_t


def get_X_hs_in_d_t(X_NR_d_t):
    """(13)

    Args:
      X_NR_d_t: 日付dの時刻tにおける非居室の絶対湿度（kg/kg(DA)）

    Returns:
      日付dの時刻tにおける熱源機の入口における絶対湿度（kg/kg(DA)）

    """
    return X_NR_d_t


# ============================================================================
# 9.2 熱源機の出口における空気温度・絶対湿度
# ============================================================================

def get_Theta_hs_out_d_t(VAV, Theta_req_d_t_i, V_dash_supply_d_t_i, L_star_H_d_t_i, L_star_CS_d_t_i, region, Theta_NR_d_t,
                         Theta_hs_out_max_H_d_t, Theta_hs_out_min_C_d_t):
    """(14-1)(14-2)(14-3)(14-4)(14-5)(14-6)

    Args:
      VAV: VAV有無
      Theta_req_d_t_i: 日付dの時刻tにおける暖冷房区画iの熱源機の出口における要求空気温度（℃）
      V_dash_supply_d_t_i: 日付dの時刻tにおける暖冷房区画iのVAV調整前の吹き出し風量（m3/h）
      L_star_H_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの熱損失を含む負荷バランス時の暖房負荷（MJ/h）
      L_star_CS_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの熱損失を含む負荷バランス時の冷房負荷（MJ/h）
      region: 地域区分
      Theta_NR_d_t: 日付dの時刻tにおける非居室の室温(℃)
      Theta_hs_out_max_H_d_t: param Theta_hs_out_min_C_d_t:
      Theta_hs_out_min_C_d_t:

    Returns:

    """
    H, C, M = get_season_array_d_t(region)
    Theta_hs_out_d_t = np.zeros(24 * 365)

    f1 = np.logical_and(H, np.sum(L_star_H_d_t_i[:5], axis=0) > 0)
    f2 = np.logical_and(H, np.sum(L_star_H_d_t_i[:5], axis=0) <= 0)
    f3 = np.logical_and(C, np.sum(L_star_CS_d_t_i[:5], axis=0) > 0)
    f4 = np.logical_and(C, np.sum(L_star_CS_d_t_i[:5], axis=0) <= 0)

    if VAV == False and constants.change_heat_source_outlet_required_temperature != 熱源機出口の空気温度.式を変更.value:
        # 暖房期および冷房期 (14-1)
        Theta_hs_out_d_t[f1] = np.sum(Theta_req_d_t_i[:5, f1] * V_dash_supply_d_t_i[:5, f1], axis=0) / \
                                       np.sum(V_dash_supply_d_t_i[:5, f1], axis=0)

        Theta_hs_out_d_t[f2] = Theta_NR_d_t[f2]

        # 熱源機の出口における空気温度θ_(hs,out,d,t)は、暖房期においては、暖房時の熱源機の出口における
        # 空気温度の最高値θ_(hs,out,max,H,d,t)を超える場合は、暖房時の熱源機の出口における空気温度の最高値θ_(hs,out,max,H,d,t)に等しい
        Theta_hs_out_d_t[H] = np.clip(Theta_hs_out_d_t[H], None, Theta_hs_out_max_H_d_t[H])

        # 冷房期 (14-2)
        Theta_hs_out_d_t[f3] = np.sum(Theta_req_d_t_i[:5, f3] * V_dash_supply_d_t_i[:5, f3], axis=0) / \
                               np.sum(V_dash_supply_d_t_i[:5, f3], axis=0)

        Theta_hs_out_d_t[f4] = Theta_NR_d_t[f4]

        # 冷房期においては、冷房時の熱源機の出口における空気温度の最低値θ_(hs,out,min,C,d,t)を下回る場合は、
        # 冷房時の熱源機の出口における空気温度の最低値θ_(hs,out,min,C,d,t)に等しい
        Theta_hs_out_d_t[C] = np.clip(Theta_hs_out_d_t[C], Theta_hs_out_min_C_d_t[C], None)

        # 中間期 (14-3)
        Theta_hs_out_d_t[M] = Theta_NR_d_t[M]
    else:
        # 暖房期 (14-4)
        Theta_hs_out_d_t[f1] = np.amax(Theta_req_d_t_i[:5, f1], axis=0)

        Theta_hs_out_d_t[f2] = Theta_NR_d_t[f2]

        # 熱源機の出口における空気温度θ_(hs,out,d,t)は、暖房期においては、暖房時の熱源機の出口における
        # 空気温度の最高値θ_(hs,out,max,H,d,t)を超える場合は、暖房時の熱源機の出口における空気温度の最高値θ_(hs,out,max,H,d,t)に等しい
        Theta_hs_out_d_t[H] = np.clip(Theta_hs_out_d_t[H], None, Theta_hs_out_max_H_d_t[H])

        # 冷房期 (14-5)
        Theta_hs_out_d_t[f3] = np.amin(Theta_req_d_t_i[:5, f3], axis=0)

        Theta_hs_out_d_t[f4] = Theta_NR_d_t[f4]

        # 冷房期においては、冷房時の熱源機の出口における空気温度の最低値θ_(hs,out,min,C,d,t)を下回る場合は、
        # 冷房時の熱源機の出口における空気温度の最低値θ_(hs,out,min,C,d,t)に等しい
        Theta_hs_out_d_t[C] = np.clip(Theta_hs_out_d_t[C], Theta_hs_out_min_C_d_t[C], None)

        # 中間期 (14-6)
        Theta_hs_out_d_t[M] = Theta_NR_d_t[M]

    return Theta_hs_out_d_t


def get_X_hs_out_d_t(X_NR_d_t, X_req_d_t_i, V_dash_supply_d_t_i, X_hs_out_min_C_d_t, L_star_CL_d_t_i, region):
    """(15-1)(15-2)

    Args:
      X_NR_d_t: 日付dの時刻tにおける非居室の絶対湿度（kg/kg(DA)）
      X_req_d_t_i: 日付dの時刻tにおける暖冷房区画iの熱源機の出口における要求絶対湿度（kg/kg(DA)）
      V_dash_supply_d_t_i: 日付dの時刻tにおける暖冷房区画iのVAV調整前の吹き出し風量（m3/h）
      X_hs_out_min_C_d_t: 日付dの時刻tにおける冷房時の熱源機の出口における絶対湿度の最低値（kg/kg(DA)）
      L_star_CL_d_t_i: param region: 地域区分
      region: returns: 日付dの時刻tにおける熱源機の出口における絶対湿度（kg/kg(DA)）

    Returns:
      日付dの時刻tにおける熱源機の出口における絶対湿度（kg/kg(DA)）

    """
    H, C, M = get_season_array_d_t(region)
    X_hs_out_d_t = np.zeros(24 * 365)

    # 暖房期および中間期 (15-1)
    HM = np.logical_or(H, M)
    X_hs_out_d_t[HM] = X_NR_d_t[HM]

    # 冷房期 (15-2)
    f1 = np.logical_and(C, np.sum(L_star_CL_d_t_i[:5], axis=0) > 0)
    f2 = np.logical_and(C, np.sum(L_star_CL_d_t_i[:5], axis=0) <= 0)

    X_hs_out_d_t[f1] = np.sum(X_req_d_t_i[:5, f1] * V_dash_supply_d_t_i[:5, f1], axis=0) / \
                        np.sum(V_dash_supply_d_t_i[:5, f1], axis=0)

    X_hs_out_d_t[f2] = X_NR_d_t[f2]

    # 冷房期に限って判定した方が良い??仕様があいまいな気がする!!
    X_hs_out_d_t = np.clip(X_hs_out_d_t, X_hs_out_min_C_d_t, None)

    return X_hs_out_d_t


# ============================================================================
# 9.3 最大出力時の熱源機の出口の空気温度・絶対湿度
# ============================================================================

def get_Theta_hs_out_max_H_d_t(Theta_star_hs_in_d_t, Q_hs_max_H_d_t, V_dash_supply_d_t_i):
    """(16)

    Args:
      Theta_star_hs_in_d_t: 日付dの時刻tにおける負荷バランス時の熱源機の入口における空気温度（℃）
      Q_hs_max_H_d_t: 日付dの時刻tにおける1時間当たりの熱源機の最大暖房出力（MJ/h）
      V_dash_supply_d_t_i: 日付dの時刻tにおける暖冷房区画iのVAV調整前の吹き出し風量（m3/h）

    Returns:
      日付dの時刻tにおける暖房時の熱源機の出口における空気温度の最高値（℃）

    """
    c_p_air = get_c_p_air()
    rho_air = get_rho_air()
    return np.clip(Theta_star_hs_in_d_t + ((Q_hs_max_H_d_t * 10 ** 6) / \
                                           (c_p_air * rho_air * np.sum(V_dash_supply_d_t_i[:5, :], axis=0))), None, constants.Theta_hs_out_max_H_d_t_limit)


def get_Theta_hs_out_min_C_d_t(Theta_star_hs_in_d_t, Q_hs_max_CS_d_t, V_dash_supply_d_t_i):
    """(17)

    Args:
      Theta_star_hs_in_d_t: 日付dの時刻tにおける負荷バランス時の熱源機の入口における空気温度（℃）
      Q_hs_max_CS_d_t: 日付dの時刻tにおける1時間当たりの熱源機の最大冷房顕熱出力（MJ/h）
      V_dash_supply_d_t_i: 日付dの時刻tにおける暖冷房区画iのVAV調整前の吹き出し風量（m3/h）

    Returns:
      日付dの時刻tにおける冷房時の熱源機の出口における空気温度の最低値（℃）

    """
    c_p_air = get_c_p_air()
    rho_air = get_rho_air()
    return np.clip(Theta_star_hs_in_d_t - ((Q_hs_max_CS_d_t * 10 ** 6) / \
                                           (c_p_air * rho_air * np.sum(V_dash_supply_d_t_i[:5, :], axis=0))), constants.Theta_hs_out_min_C_d_t_limit, None)


def get_X_hs_out_min_C_d_t(X_star_hs_in_d_t, Q_hs_max_CL_d_t, V_dash_supply_d_t_i):
    """(18)

    Args:
      X_star_hs_in_d_t: 日付dの時刻tにおける負荷バランス時の熱源機の入口における絶対湿度（kg/kg(DA)）
      Q_hs_max_CL_d_t: 日付dの時刻tにおける1時間当たりの熱源機の最大冷房潜熱出力（MJ/h）
      V_dash_supply_d_t_i: 日付dの時刻tにおける暖冷房区画iのVAV調整前の吹き出し風量（m3/h）

    Returns:
      日付dの時刻tにおける冷房時の熱源機の出口における空気温度の最低値（℃）

    """
    rho_air = get_rho_air()
    L_wtr = get_L_wtr()
    return X_star_hs_in_d_t - ((Q_hs_max_CL_d_t * 10 ** 3) / (rho_air * L_wtr * np.sum(V_dash_supply_d_t_i[:5, :], axis=0)))


def get_Theta_star_hs_in_d_t(Theta_star_NR_d_t):
    """(19)

    Args:
      Theta_star_NR_d_t: 日付dの時刻tにおける負荷バランス時の非居室の室温（℃）

    Returns:
      日付dの時刻tにおける負荷バランス時の熱源機の入口における空気温度（℃）

    """
    return Theta_star_NR_d_t


def get_X_star_hs_in_d_t(X_star_NR_d_t):
    """(20)

    Args:
      X_star_NR_d_t: 日付dの時刻tにおける負荷バランス時の非居室の絶対湿度（kg/kg(DA)）

    Returns:
      日付dの時刻tにおける負荷バランス時の熱源機の入口における絶対湿度（kg/kg(DA)）

    """
    return X_star_NR_d_t


# ============================================================================
# 9.4 熱源機の出口における要求空気温度・絶対湿度
# ============================================================================

def get_Theta_req_d_t_i(Theta_sur_d_t_i, Theta_star_HBR_d_t, V_dash_supply_d_t_i, L_star_H_d_t_i, L_star_CS_d_t_i,
                        l_duct_i, region):
    """(21-1)(21-2)(21-3)

    Args:
      Theta_sur_d_t_i: 日付dの時刻tにおける負荷バランス時の居室の室温（℃）
      Theta_star_HBR_d_t: 日付dの時刻tにおける負荷バランス時の居室の室温（℃）
      V_dash_supply_d_t_i: 日付dの時刻tにおける暖冷房区画iのVAV調整前の吹き出し風量（m3/h）
      L_star_H_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの熱損失を含む負荷バランス時の暖房負荷（MJ/h）
      L_star_CS_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの熱取得を含む負荷バランス時の冷房顕熱負荷（MJ/h）
      l_duct_i: ダクトの長さ（m）
      region: 地域区分

    Returns:
      日付dの時刻tにおける暖冷房区画iの熱源機の出口における要求空気温度（℃）

    """
    c_p_air = get_c_p_air()
    rho_air = get_rho_air()
    # ダクトiの線熱損失係数（W/(m・K)）
    phi_i = get_phi_i()
    H, C, M = get_season_array_d_t(region)

    Theta_req_d_t_i = np.zeros((5, 24 * 365))

    e_exp_H = (phi_i[:, np.newaxis] * l_duct_i[:, np.newaxis] * 3600) / (c_p_air * rho_air * V_dash_supply_d_t_i[:, H])

    # 暖房期 (21-1)
    Theta_req_d_t_i[:, H] = Theta_sur_d_t_i[:, H] \
                           + (Theta_star_HBR_d_t[H] + (L_star_H_d_t_i[:, H] * 10 ** 6) \
                           / (c_p_air * rho_air * V_dash_supply_d_t_i[:, H]) - Theta_sur_d_t_i[:, H]) \
                           * np.exp(e_exp_H)

    # 暖冷房区画iの熱源機の出口における要求空気温度が負荷バランス時の居室の室温を下回る場合
    Theta_req_d_t_i[:, H] = np.clip(Theta_req_d_t_i[:, H], Theta_star_HBR_d_t[H], None)

    # 冷房期 (21-2)
    e_exp_C = (phi_i[:, np.newaxis] * l_duct_i[:, np.newaxis] * 3600) / (c_p_air * rho_air * V_dash_supply_d_t_i[:, C])
    Theta_req_d_t_i[:, C] = Theta_sur_d_t_i[:, C] \
                            - (Theta_sur_d_t_i[:, C] - Theta_star_HBR_d_t[C] + (L_star_CS_d_t_i[:, C] * 10 ** 6) \
                            / (c_p_air * rho_air * V_dash_supply_d_t_i[:, C])) \
                            * np.exp(e_exp_C)

    # 暖冷房区画iの熱源機の出口における要求空気温度が負荷バランス時の居室の室温を上回る場合
    Theta_req_d_t_i[:, C] = np.clip(Theta_req_d_t_i[:, C], None, Theta_star_HBR_d_t[C])

    #中間期 (10-3)
    Theta_req_d_t_i[:, M] = Theta_star_HBR_d_t[M]

    return Theta_req_d_t_i

def get_Theta_req_d_t_i_2023(
        region, A_A, A_MR, A_OR, Q, r_A_ufvnt, underfloor_insulation, Theta_uf_d_t, Theta_ex_d_t,
        V_dash_supply_d_t_i, H_OR_C, L_dash_H_R_d_t, L_dash_CS_R_d_t, R_g):
    """(21-1)(21-2)(21-3)

    Args:
      region(int): 省エネルギー地域区分
      A_A(float): 床面積の合計 (m2)
      A_MR(float): 主たる居室の床面積 (m2)
      A_OR(float): その他の居室の床面積 (m2)
      Q(float): 当該住戸の熱損失係数 (W/m2K)
      r_A_ufvnt(float): 当該住戸において、床下空間全体の面積に対する空気を供給する床下空間の面積の比 (-)
      underfloor_insulation(bool): 床下空間が断熱空間内である場合はTrue
      Theta_uf_d_t(ndarray): 床下温度 (℃)
      Theta_ex_d_t(ndarray): 外気温度 (℃)
      V_dash_supply_d_t_i(ndarray): 日付dの時刻tにおける暖冷房区画iのVAV調整前の熱源機の風量（m3/h）
      H_OR_C: type H_OR_C: str
      L_dash_H_R_d_t(ndarray): 標準住戸の負荷補正前の暖房負荷 (MJ/h)
      L_dash_CS_R_d_t(ndarray): 標準住戸の負荷補正前の冷房顕熱負荷 （MJ/h）
      R_g: 地盤またはそれを覆う基礎の表面熱伝達抵抗 ((m2・K)/W)
    Returns:
      Theta_req_d_t: 要求床下温度 (℃)

    """

    r_A_uf_i = np.array([get_r_A_uf_i(i) for i in range(1,13)])
    V_sa_d_t_A = np.sum(r_A_uf_i[:5, np.newaxis] * V_dash_supply_d_t_i, axis=0)
    Theta_uf_d_t, Theta_g_surf_d_t, A_s_ufvnt, A_s_ufvnt_A, Theta_g_avg, Theta_dash_g_surf_A_m_d_t, L_uf, H_floor, phi, Phi_A_0, H_star_d_t_i, Theta_star_d_t_i = \
      calc_Theta(region, A_A, A_MR, A_OR, Q, r_A_ufvnt, underfloor_insulation, Theta_uf_d_t, Theta_ex_d_t,
        V_sa_d_t_A, H_OR_C, L_dash_H_R_d_t, L_dash_CS_R_d_t, R_g)
    U_s = get_U_s()
    ro_air = get_ro_air()
    c_p_air = get_c_p_air()
    Theta_req_d_t = (
        Theta_uf_d_t
        + (U_s * np.sum(H_star_d_t_i * np.array(A_s_ufvnt)[:, np.newaxis], axis=0) + phi * L_uf + A_s_ufvnt_A / R_g / (1 + Phi_A_0 / R_g)) * Theta_uf_d_t * 3.6
        - (U_s * np.sum(H_star_d_t_i * Theta_star_d_t_i * np.array(A_s_ufvnt)[:, np.newaxis], axis=0) + phi * L_uf * Theta_ex_d_t
           + A_s_ufvnt_A / R_g * (np.sum(Theta_dash_g_surf_A_m_d_t, axis=1) + Theta_g_avg) / (1 + Phi_A_0 / R_g)) * 3.6
      ) / ( ro_air * c_p_air * V_sa_d_t_A )
    return np.tile(Theta_req_d_t, (5, 1))


def get_X_req_d_t_i(X_star_HBR_d_t, L_star_CL_d_t_i, V_dash_supply_d_t_i, region):
    """(22-1)(22-2)

    Args:
      X_star_HBR_d_t: 日付dの時刻tにおける負荷バランス時の居室の絶対湿度（kg/kg(DA)）
      L_star_CL_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの熱取得を含む負荷バランス時の冷房潜熱負荷（MJ/h）
      V_dash_supply_d_t_i: 日付dの時刻tにおける暖冷房区画iのVAV調整前の吹き出し風量（m3/h）
      region: 地域区分

    Returns:
      日付dの時刻tにおける暖冷房区画iの熱源機の出口における要求絶対湿度（kg/kg(DA)）

    """
    rho_air = get_rho_air()
    L_wtr = get_L_wtr()
    H, C, M = get_season_array_d_t(region)

    # 暖房期および中間期 (22-1)
    HM = np.logical_or(H, M)

    X_req_d_t_i = np.zeros((5, 24 * 365))

    X_req_d_t_i[:, HM] = X_star_HBR_d_t[HM]

    # 冷房期 (22-2)
    X_req_d_t_i[:, C] = X_star_HBR_d_t[C] - (L_star_CL_d_t_i[:, C] * 10 ** 3) / (rho_air * L_wtr * V_dash_supply_d_t_i[:, C])

    return X_req_d_t_i


# ============================================================================
# 9.5 熱源機の最大出力
# ============================================================================

# ============================================================================
# 9.5.1 熱源機の最大暖房出力
# ============================================================================

def get_Q_hs_max_H_d_t(type, q_hs_rtd_H, C_df_H_d_t, input_C_af_H):
    """(23)

    Args:
      type: 暖房設備機器の種類
      q_hs_rtd_H: 熱源機の定格暖房能力 (W)
      C_df_H_d_t: 日付dの時刻tにおけるデフロストに関する暖房出力補正係数（-）
      input_C_af_H(dict): 室内機吹き出し風量に関する暖房出力補正係数に関する入力

    Returns:
      熱源機の最大暖房出力 (MJ/h)

    """
    alpha_max_H = get_alpha_max_H()

    Q_hs_max_H_d_t = np.zeros(24 * 365)

    if q_hs_rtd_H is not None:
        if type == PROCESS_TYPE_3:
            C_af_H = get_C_af_H(input_C_af_H)
            Q_hs_max_H_d_t = q_hs_rtd_H * alpha_max_H * C_df_H_d_t * C_af_H * 3600 * 10 ** -6
        else:
            Q_hs_max_H_d_t = q_hs_rtd_H * alpha_max_H * C_df_H_d_t * 3600 * 10 ** -6

    return Q_hs_max_H_d_t


def get_alpha_max_H():
    """:return: 定格暖房能力に対する最大暖房能力の比（-）"""
    return 1.00


def get_C_df_H_d_t(Theta_ex_d_t, h_ex_d_t):
    """(24-1)(24-2)

    Args:
      Theta_ex_d_t: 日付dの時刻tにおける外気温度（℃）
      h_ex_d_t: 日付dの時刻tにおける外気相対湿度（%）

    Returns:
      日付dの時刻tにおけるデフロストに関する暖房出力補正係数（-）

    """
    C_df_H_d_t = np.ones(24 * 365)
    C_df_H_d_t[np.logical_and(Theta_ex_d_t < constants.defrost_temp_ductcentral, h_ex_d_t > constants.defrost_humid_ductcentral)] = constants.C_df_H_d_t_defrost_ductcentral
    return C_df_H_d_t


# ============================================================================
# 9.5.2 熱源機の最大冷房出力
# ============================================================================

# 1時間当たりの熱源機の最大冷房顕熱出力  (24)
def get_Q_hs_max_CS_d_t(Q_hs_max_C_d_t, SHF_dash_d_t):
    """(25)

    Args:
      Q_hs_max_C_d_t: 日付dの時刻tにおける1時間当たりの熱源機の最大冷房出力（MJ/h）
      SHF_dash_d_t: 日付dの時刻tにおける冷房負荷補正顕熱比(-)

    Returns:
      日付dの時刻tにおける1時間当たりの熱源機の最大冷房顕熱出力(MJ/h)

    """
    return Q_hs_max_C_d_t * SHF_dash_d_t


# 1時間当たりの熱源機の最大冷房潜熱出力  (25)
def get_Q_hs_max_CL_d_t(Q_hs_max_C_d_t, SHF_dash_d_t, L_star_dash_CL_d_t):
    """(26)

    Args:
      Q_hs_max_C_d_t: 日付dの時刻tにおける1時間当たりの熱源機の最大冷房出力（MJ/h）
      SHF_dash_d_t: 日付dの時刻tにおける冷房負荷補正顕熱比(-)
      L_star_dash_CL_d_t: 日付dの時刻tにおける補正冷房潜熱負荷(MJ/h)

    Returns:
      日付dの時刻tにおける1時間当たりの熱源機の最大冷房潜熱出力(MJ/h)

    """
    return np.min([Q_hs_max_C_d_t * (1.0 - SHF_dash_d_t), L_star_dash_CL_d_t], axis=0)


# 最大冷房出力 [MJ/h] (27)
def get_Q_hs_max_C_d_t(type, q_hs_rtd_C, input_C_af_C):
    """(27)

    Args:
      type: 暖房設備機器の種類
      q_hs_rtd_C: 熱源機の冷房時の定格出力[m^3/h]
      input_C_af_C(dict): 室内機吹き出し風量に関する冷房出力補正係数に関する入力

    Returns:
      最大冷房出力 [MJ/h]

    """
    alpha_max_C = get_alpha_max_C()

    Q_hs_max_C_d_t = np.zeros(24 * 365)

    if q_hs_rtd_C is not None:
        if type == PROCESS_TYPE_3:
            C_af_C = get_C_af_C(input_C_af_C)
            Q_hs_max_C_d_t = q_hs_rtd_C * alpha_max_C * C_af_C * 3600 * 10 ** -6
        else:
            Q_hs_max_C_d_t = q_hs_rtd_C * alpha_max_C * 3600 * 10 ** -6

    return Q_hs_max_C_d_t


def get_alpha_max_C():
    """:return: 定格冷房能力に対する最大冷房能力の比(-)"""
    return 1.11


# 冷房負荷補正顕熱比  (28)
def get_SHF_dash_d_t(L_star_CS_d_t, L_star_dash_C_d_t):
    """(28)

    Args:
      L_star_CS_d_t: 日付dの時刻tにおける1時間当たりの熱取得を含む負荷バランス時の冷房顕熱負荷（MJ/h）
      L_star_dash_C_d_t: 日付dの時刻tにおける補正冷房負荷（MJ/h）

    Returns:
      日付dの時刻tにおける冷房負荷補正顕熱比（-）

    """
    SHF_dash_d_t = np.zeros(24 * 365)

    f = L_star_dash_C_d_t > 0
    SHF_dash_d_t[f] = L_star_CS_d_t[f] / L_star_dash_C_d_t[f]

    return SHF_dash_d_t


# 1時間当たりの補正冷房負荷  (29)
def get_L_star_dash_C_d_t(L_star_CS_d_t, L_star_dash_CL_d_t):
    """(29)

    Args:
      L_star_CS_d_t: 日付dの時刻tにおける1時間当たりの熱取得を含む負荷バランス時の冷房顕熱負荷（MJ/h）
      L_star_dash_CL_d_t: 日付dの時刻tにおける補正冷房潜熱負荷（MJ/h）

    Returns:
      日付dの時刻tにおける時間当たりの補正冷房負荷(MJ/h)

    """
    return L_star_CS_d_t + L_star_dash_CL_d_t


def get_L_star_dash_CL_d_t(L_star_CL_max_d_t, L_star_CL_d_t):
    """(30)

    Args:
      L_star_CL_max_d_t: 日付dの時刻tにおける最大冷房潜熱負荷（MJ/h）
      L_star_CL_d_t: 日付dの時刻tにおける1時間当たりの熱取得を含む負荷バランス時の冷房潜熱負荷（MJ/h）

    Returns:
      日付dの時刻tにおける補正冷房潜熱負荷（MJ/h）

    """
    return np.minimum(L_star_CL_max_d_t, L_star_CL_d_t)


# 1時間当たりの最大冷房潜熱負荷 (MJ/h)
def get_L_star_CL_max_d_t(L_star_CS_d_t):
    """(31)

    Args:
      L_star_CS_d_t: 日付dの時刻tにおける1時間当たりの熱取得を含む負荷バランス時の冷房顕熱負荷（MJ/h）

    Returns:
      日付dの時刻tにおける最大冷房潜熱負荷（MJ/h）

    """
    # 冷房負荷最小顕熱比率 [-]
    SHF_L_min_C = get_SHF_L_min_C()

    return L_star_CS_d_t * ((1.0 - SHF_L_min_C) / SHF_L_min_C)


def get_SHF_L_min_C():
    """:return: 冷房負荷最小顕熱比率 (-)"""
    return 0.4


def get_L_star_CS_d_t(L_star_CS_d_t_i):
    """(32)

    Args:
      get_L_star_CS_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの熱取得を含む負荷バランス時の冷房顕熱負荷（MJ/h）
      L_star_CS_d_t_i: returns: 日付dの時刻tにおける1時間当たりの熱取得を含む負荷バランス時の冷房顕熱負荷（MJ/h）

    Returns:
      日付dの時刻tにおける1時間当たりの熱取得を含む負荷バランス時の冷房顕熱負荷（MJ/h）

    """
    return np.sum(L_star_CS_d_t_i[:5, :], axis=0)


def get_L_star_CL_d_t(L_star_CL_d_t_i):
    """(33)

    Args:
      get_L_star_CL_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの熱取得を含む負荷バランス時の冷房潜熱負荷（MJ/h）
      L_star_CL_d_t_i: returns: 日付dの時刻tにおける1時間当たりの熱取得を含む負荷バランス時の冷房潜熱負荷（MJ/h）

    Returns:
      日付dの時刻tにおける1時間当たりの熱取得を含む負荷バランス時の冷房潜熱負荷（MJ/h）

    """
    return np.sum(L_star_CL_d_t_i[:5, :], axis=0)


# ============================================================================
# 9.6 熱源機の風量
# ============================================================================

def get_V_hs_supply_d_t(V_supply_d_t_i):
    """(34)

    Args:
      V_supply_d_t_i: 日付dの時刻tにおける暖冷房区画iの吹き出し風量（m3/h）

    Returns:
      日付dの時刻tにおける熱源機の風量（m3/h）

    """
    return np.sum(V_supply_d_t_i[:5, :], axis=0)


def get_V_hs_vent_d_t(V_vent_g_i, general_ventilation):
    """(35-1)(35-2)

    Args:
      V_vent_g_i: 暖冷房区画iの全般換気量（m3/h）
      general_ventilation: 全版換気の機能

    Returns:
      日付dの時刻tにおける熱源機の風量のうちの全般換気分（m3/h）

    """
    # (35-2)
    V_hs_vent_d_t = np.zeros(24 * 365)

    # 当該システムが全般換気の機能を有する場合 (35-1)
    if general_ventilation == True:
        V_vent_g = np.sum(V_vent_g_i[:5], axis=0)
        V_hs_vent_d_t = np.repeat(V_vent_g, 24 * 365)
    elif general_ventilation == False:
        pass
    else:
        raise ValueError(general_ventilation)

    return V_hs_vent_d_t

# ============================================================================
# 9.7 VAV調整前の熱源機の風量
# ============================================================================
def get_V_dash_hs_supply_d_t_2023(Q_hat_hs_d_t, region, for_cooling):
    """ルームエアコンディショナ活用型全館空調(潜熱評価モデル) \n
    Args:
      Q_hat_hs_d_t: 日付dの時刻tにおける一時間当たりの熱源機の風量を計算するための熱源機の出力 [MJ/h] \n
      region: 地域区分 \n
      cooling: 冷房であるか \n
    Returns:
      日付dの時刻tにおけるVAV調整前の熱源機の風量 [m3/h] \n
    """
    Q_hat_hs_d_t_kw = Q_hat_hs_d_t / 3600 * 1000
    _logger.info(f"Q_hat_hs_d_t_kw: {Q_hat_hs_d_t_kw}")
    del Q_hat_hs_d_t  # NOTE: 誤用を防ぐ目的で単位変換前を削除

    H, C, M = get_season_array_d_t(region)
    V_dash_hs_supply_d_t = np.zeros(24 * 365)

    # 暖房期
    if for_cooling == True:
      V_dash_hs_supply_d_t[H] = constants.airvolume_minimum_C
    else:
      V_dash_hs_supply_d_t[H] = \
        np.clip(
          (constants.airvolume_coeff_a4_H * Q_hat_hs_d_t_kw ** 4
            + constants.airvolume_coeff_a3_H * Q_hat_hs_d_t_kw ** 3
            + constants.airvolume_coeff_a2_H * Q_hat_hs_d_t_kw ** 2
            + constants.airvolume_coeff_a1_H * Q_hat_hs_d_t_kw
            + constants.airvolume_coeff_a0_H)[H],
          constants.airvolume_minimum_H, constants.airvolume_maximum_H
        )

    # 冷房期
    if for_cooling == True:
      V_dash_hs_supply_d_t[C] =  \
        np.clip(
          (constants.airvolume_coeff_a4_C * Q_hat_hs_d_t_kw ** 4
            + constants.airvolume_coeff_a3_C * Q_hat_hs_d_t_kw ** 3
            + constants.airvolume_coeff_a2_C * Q_hat_hs_d_t_kw ** 2
            + constants.airvolume_coeff_a1_C * Q_hat_hs_d_t_kw
            + constants.airvolume_coeff_a0_C)[C],
          constants.airvolume_minimum_C, constants.airvolume_maximum_C
        )
    else:
      V_dash_hs_supply_d_t[C] = constants.airvolume_minimum_H

    # 中間期
    if for_cooling == True:
      V_dash_hs_supply_d_t[M] = constants.airvolume_minimum_C
    else:
      V_dash_hs_supply_d_t[M] = constants.airvolume_minimum_H

    # WARNING: 少数点の扱いの問題で意図しない結果になる
    # assert V_dash_hs_supply_d_t >= constants.airvolume_minimum

    # NOTE: ここまで m3/min ベース 変換-> m3/h
    return V_dash_hs_supply_d_t * 60


def get_V_dash_hs_supply_d_t(V_hs_min, V_hs_dsgn_H, V_hs_dsgn_C, Q_hs_rtd_H, Q_hs_rtd_C, Q_hat_hs_d_t, region):
    """(36-1)(36-2)(36-3)

    Args:
      V_hs_min: 熱源機の最低風量（m3/h）
      V_hs_dsgn_H: 暖房時の設計風量（m3/h）
      V_hs_dsgn_C: 冷房時の設計風量（m3/h）
      Q_hs_rtd_H: 熱源機の暖房時の定格出力（MJ/h）
      Q_hs_rtd_C: 熱源機の冷房時の定格出力（MJ/h）
      Q_hat_hs_d_t: 日付dの時刻tにおける１時間当たりの熱源機の風量を計算するための熱源機の出力（MJ/h）
      region: 地域区分

    Returns:
      日付dの時刻tにおけるVAV調整前の熱源機の風量（m3/h）

    """
    H, C, M = get_season_array_d_t(region)

    V_dash_hs_supply_d_t = np.zeros(24 * 365)

    # 暖房期 (36-1)
    f1 = np.logical_and(H, Q_hat_hs_d_t < 0)
    V_dash_hs_supply_d_t[f1] = V_hs_min

    if Q_hs_rtd_H:
        f2 = np.logical_and(H, np.logical_and(0 <= Q_hat_hs_d_t, Q_hat_hs_d_t < Q_hs_rtd_H))
        V_dash_hs_supply_d_t[f2] = (V_hs_dsgn_H - V_hs_min) / Q_hs_rtd_H * Q_hat_hs_d_t[f2] + V_hs_min

        if V_hs_dsgn_H:
            f3 = np.logical_and(H, Q_hs_rtd_H <= Q_hat_hs_d_t)
            V_dash_hs_supply_d_t[f3] = V_hs_dsgn_H

    # 冷房期 (36-2)
    f4 = np.logical_and(C, Q_hat_hs_d_t < 0)
    V_dash_hs_supply_d_t[f4] = V_hs_min

    if Q_hs_rtd_C:
        f5 = np.logical_and(C, np.logical_and(0 <= Q_hat_hs_d_t, Q_hat_hs_d_t < Q_hs_rtd_C))
        V_dash_hs_supply_d_t[f5] = (V_hs_dsgn_C - V_hs_min) / Q_hs_rtd_C * Q_hat_hs_d_t[f5] + V_hs_min

        if V_hs_dsgn_C:
            f6 = np.logical_and(C, Q_hat_hs_d_t >= Q_hs_rtd_C)
            V_dash_hs_supply_d_t[f6] = V_hs_dsgn_C

    # 中間期 (36-3)
    V_dash_hs_supply_d_t[M] = V_hs_min

    return V_dash_hs_supply_d_t


def get_Q_hs_rtd_H(q_hs_rtd_H):
    """(37)

    Args:
      q_hs_rtd_H: 熱源機の定格暖房能力（W）

    Returns:
      暖房時の熱源機の定格出力（MJ/h）

    """
    if q_hs_rtd_H is not None:
        return q_hs_rtd_H * 3600 * 10 ** -6
    else:
        return None


def get_Q_hs_rtd_C(q_hs_rtd_C):
    """(38)

    Args:
      q_hs_rtd_C: 熱源機の定格冷房能力（W）

    Returns:
      冷房時の熱源機の定格出力（MJ/h）

    """
    if q_hs_rtd_C is not None:
        return q_hs_rtd_C * 3600 * 10 ** -6
    else:
        return None


def get_V_hs_min(V_vent_g_i):
    """(39)

    Args:
      V_vent_g_i: 暖冷房区画iの全般換気量（m3/h）

    Returns:
      熱源機の最低風量（m3/h）

    """
    return np.sum(V_vent_g_i[:5], axis=0)


def calc_Q_hat_hs_d_t(Q, A_A, V_vent_l_d_t, V_vent_g_i, mu_H, mu_C, J_d_t, q_gen_d_t, n_p_d_t, q_p_H, q_p_CS, q_p_CL, X_ex_d_t, w_gen_d_t, Theta_ex_d_t, L_wtr, region):
    """(40-1a)(40-1b)(40-2a)(40-2b)(40-2c)(40-3)

    Args:
      Q: 当該住戸の熱損失係数（W/(m2・K)）
      A_A: 床面積の合計（m2）
      V_vent_l_d_t: 日付dの時刻tにおける局所換気量（m3/h）
      V_vent_g_i: 暖冷房区画iの全般換気量（m3/h）
      mu_H: 当該住戸の暖房期の日射取得係数（(W/m2)/(W/m2)）
      mu_C: 当該住戸の冷房期の日射取得係数（(W/m2)/(W/m2)）
      J_d_t: 日付dの時刻tにおける水平面全天日射量（W/m2）
      q_gen_d_t: 日付dの時刻tにおける内部発熱（W）
      n_p_d_t: 日付dの時刻tにおける在室人数（人）
      q_p_H: 暖房期における人体からの1人当たりの顕熱発熱量（W/人）
      q_p_CS: 冷房期における人体からの1人当たりの顕熱発熱量（W/人）
      q_p_CL: 冷房期における人体からの1人当たりの潜熱発熱量（W/人）
      X_ex_d_t: 日付dの時刻tにおける外気の絶対湿度（kg/kg(DA)）
      w_gen_d_t: param Theta_ex_d_t: 日付dの時刻tにおける外気温度（℃）
      L_wtr: 水の蒸発潜熱（kJ/kg）
      region: 地域区分
      Theta_ex_d_t: returns: 日付dの時刻tにおける１時間当たりの熱源機の風量を計算するための熱源機の暖房出力（MJ/h）

    Returns:
      日付dの時刻tにおける１時間当たりの熱源機の風量を計算するための熱源機の暖房出力（MJ/h）

    """
    H, C, M = get_season_array_d_t(region)
    c_p_air = get_c_p_air()
    rho_air = get_rho_air()
    Theta_set_H = get_Theta_set_H()
    Theta_set_C = get_Theta_set_C()
    X_set_C = get_X_set_C()

    Q_hat_hs_d_t = np.zeros(24 * 365)
    Q_hat_hs_H_d_t = np.zeros(24 * 365)
    Q_hat_hs_CS_d_t = np.zeros(24 * 365)
    Q_hat_hs_CL_d_t = np.zeros(24 * 365)

    # 暖房期 (40-1b)
    if mu_H is not None:
        Q_hat_hs_H_d_t[H] = (((Q - 0.35 * 0.5 * 2.4) * A_A + (c_p_air * rho_air * (V_vent_l_d_t[H] + np.sum(V_vent_g_i[:5]))) / 3600) * (Theta_set_H - Theta_ex_d_t[H]) \
                          - mu_H * A_A * J_d_t[H] - q_gen_d_t[H] - n_p_d_t[H] * q_p_H) * 3600 * 10 ** -6

    # (40-1a)
    Q_hat_hs_d_t[H] = np.clip(Q_hat_hs_H_d_t[H], 0, None)

    # 冷房期 (40-2b)
    Q_hat_hs_CS_d_t[C] = (((Q - 0.35 * 0.5 * 2.4) * A_A + (c_p_air * rho_air * (V_vent_l_d_t[C] + np.sum(V_vent_g_i[:5]))) / 3600) * (Theta_ex_d_t[C] - Theta_set_C) \
                      + mu_C * A_A * J_d_t[C] + q_gen_d_t[C] + n_p_d_t[C] * q_p_CS) * 3600 * 10 ** -6

    # (40-2c)
    Q_hat_hs_CL_d_t[C] = ((rho_air * (V_vent_l_d_t[C] + np.sum(V_vent_g_i[:5])) * (X_ex_d_t[C] - X_set_C) * 10 ** 3 + w_gen_d_t[C]) \
                      * L_wtr + n_p_d_t[C] * q_p_CL * 3600) * 10 ** -6

    # (40-2a)
    Q_hat_hs_d_t[C] = np.clip(Q_hat_hs_CS_d_t[C], 0, None) + np.clip(Q_hat_hs_CL_d_t[C], 0, None)

    # 中間期 (40-3)
    Q_hat_hs_d_t[M] = 0

    return Q_hat_hs_d_t, np.clip(Q_hat_hs_CS_d_t, 0, None)


# ============================================================================
# 10 吹き出し口
# ============================================================================

# ============================================================================
# 10.1 吹き出し空気温度
# ============================================================================

def get_Thata_supply_d_t_i(Theta_sur_d_t_i, Theta_hs_out_d_t, Theta_star_HBR_d_t, l_duct_i,
                                                   V_supply_d_t_i, L_star_H_d_t_i, L_star_CS_d_t_i, region):
    """(41-1)(41-2)(41-3)

    Args:
      Theta_sur_d_t_i: 日付dの時刻tにおけるダクトiの周囲の空気温度（℃）
      Theta_star_HBR_d_t: 日付dの時刻tにおける負荷バランス時の居室の室温（℃）
      l_duct_i: ダクトiの長さ（m）
      V_supply_d_t_i: 日付dの時刻tにおける暖冷房区画iの吹き出し風量（m3/h）
      L_star_H_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの熱損失を含む負荷バランス時の暖房負荷（MJ/h）
      L_star_CS_d_t_i: param region: 地域区分
      Theta_hs_out_d_t: 日付dの時刻tにおける熱源機の出口における空気温度（℃）
      region: returns: 日付dの時刻tにおける暖冷房区画iの吹き出し温度（℃）

    Returns:
      日付dの時刻tにおける暖冷房区画iの吹き出し温度（℃）

    """
    H, C, M = get_season_array_d_t(region)
    c_p_air = get_c_p_air()
    rho_air = get_rho_air()
    phi_i = get_phi_i()

    Thata_supply_d_t_i = np.zeros((5, 24 * 365))

    f1 = np.logical_and(H, np.sum(L_star_H_d_t_i[:5, :], axis=0) > 0)
    f2 = np.logical_and(H, np.sum(L_star_H_d_t_i[:5, :], axis=0) <= 0)
    f3 = np.logical_and(C, np.sum(L_star_CS_d_t_i[:5, :], axis=0) > 0)
    f4 = np.logical_and(C, np.sum(L_star_CS_d_t_i[:5, :], axis=0) <= 0)


    # 暖房期 (41-1)
    e_exp_H = -(phi_i[:, np.newaxis] * l_duct_i[:, np.newaxis] * 3600) / (c_p_air * rho_air * V_supply_d_t_i[:, f1])

    Thata_supply_d_t_i[:, f1] = Theta_sur_d_t_i[:, f1] + (Theta_hs_out_d_t[f1] - Theta_sur_d_t_i[:, f1]) \
                             * np.exp(e_exp_H)

    Thata_supply_d_t_i[:, f2] = Theta_star_HBR_d_t[f2]

    # 冷房期 (41-2)
    e_exp_C = -(phi_i[:, np.newaxis] * l_duct_i[:, np.newaxis] * 3600) / (c_p_air * rho_air * V_supply_d_t_i[:, f3])

    Thata_supply_d_t_i[:, f3] = Theta_sur_d_t_i[:, f3] + (Theta_hs_out_d_t[f3] - Theta_sur_d_t_i[:, f3]) \
                             * np.exp(e_exp_C)

    Thata_supply_d_t_i[:, f4] = Theta_star_HBR_d_t[f4]

    # 中間期 (41-3)
    Thata_supply_d_t_i[:, M] = Theta_star_HBR_d_t[M]

    return Thata_supply_d_t_i


# ============================================================================
# 10.2 吹き出し絶対湿度
# ============================================================================

def get_X_supply_d_t_i(X_star_HBR_d_t, X_hs_out_d_t, L_star_CL_d_t_i, region):
    """(42-1)(42-2)

    Args:
      X_star_HBR_d_t: 日付dの時刻tにおける負荷バランス時の居室の絶対湿度（kg/kg(DA)）
      X_hs_out_d_t: 日付dの時刻tにおける熱源機の出口における絶対湿度（kg/kg(DA)）
      L_star_CL_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの熱取得を含む負荷バランス時の冷房潜熱負荷（MJ/h）
      region: 地域区分

    Returns:
      日付dの時刻tにおける暖冷房区画iの吹き出し絶対湿度（kg/kg(DA)）

    """
    H, C, M = get_season_array_d_t(region)
    X_supply_d_t_i = np.zeros((5, 24 * 365))

    # 暖房期および中間期 (42-1)
    HM = np.logical_or(H, M)
    X_supply_d_t_i[:, HM] = X_star_HBR_d_t[HM]

    # 冷房期 (42-2)
    f1 = np.logical_and(C, np.sum(L_star_CL_d_t_i[:5, :], axis=0) > 0)
    f2 = np.logical_and(C, np.sum(L_star_CL_d_t_i[:5, :], axis=0) <= 0)

    X_supply_d_t_i[:, f1] = X_hs_out_d_t[f1]
    X_supply_d_t_i[:, f2] = X_star_HBR_d_t[f2]

    return X_supply_d_t_i


# ============================================================================
# 10.3 吹き出し風量
# ============================================================================

def cap_V_supply_d_t_i(V_supply_d_t_i, V_dash_supply_d_t_i, V_vent_g_i, region, V_hs_dsgn_H, V_hs_dsgn_C):
    _logger.NDdebug("V_supply_d_t_i_キャップ前:", V_supply_d_t_i[0])
    _logger.NDdebug("V_dash_supply_d_t_i:", V_dash_supply_d_t_i[0])

    V_vent_g_i = np.reshape(V_vent_g_i, (5, 1))
    V_vent_g_i = V_vent_g_i.repeat(24 * 365, axis=1)

    H, C, M = get_season_array_d_t(region)

    # 吹き出し風量V_(supply,d,t,i)は、VAV調整前の吹き出し風量V_(supply,d,t,i)^'を上回る場合はVAV調整前の \
    # 吹き出し風量V_(supply,d,t,i)^'に等しいとし、全般換気量V_(vent,g,i)を下回る場合は全般換気量V_(vent,g,i)に等しいとする
    if constants.change_V_supply_d_t_i_max == Vサプライの上限キャップ.外さない.value:
        new_V_supply_d_t_i = np.clip(V_supply_d_t_i, V_vent_g_i, V_dash_supply_d_t_i)

    elif constants.change_V_supply_d_t_i_max == Vサプライの上限キャップ.全体でキャップ.value:
        # 委員より提案 案1('24/01)

        """ 設計風量をキャップ上限とする """
        V_hs_dsgn_C = V_hs_dsgn_C if V_hs_dsgn_C is not None else float('inf')
        V_hs_dsgn_H = V_hs_dsgn_H if V_hs_dsgn_H is not None else float('inf')

        """ キャップを超える時刻を調べる """
        V_supply_d_t_i = np.clip(V_supply_d_t_i, V_vent_g_i, None)
        V_supply_d_t = np.sum(V_supply_d_t_i, axis=0)  # 1d-shape(5, )

        overflow_mask_H_d_t = np.logical_and(H, V_supply_d_t > V_hs_dsgn_H)
        overflow_mask_C_d_t = np.logical_and(C, V_supply_d_t > V_hs_dsgn_C)

        """ 全体にかける縮小率を算出 """  # 全体適用なので案1では1d-array
        ratios_H = np.divide(
          np.full(len(V_supply_d_t), V_hs_dsgn_H, dtype=float),
          np.ceil(V_supply_d_t * 1000) / 1000,  # NOTE: 計算速度と四捨五入による設計風量超え防止のため
          where=overflow_mask_H_d_t, out=np.ones_like(V_supply_d_t, dtype=float))
        ratios_C = np.divide(
          np.full(len(V_supply_d_t), V_hs_dsgn_C, dtype=float),
          np.ceil(V_supply_d_t * 1000) / 1000,
          where=overflow_mask_C_d_t, out=np.ones_like(V_supply_d_t, dtype=float))

        new_V_supply_d_t_i = V_supply_d_t_i * ratios_H[np.newaxis, :] * ratios_C[np.newaxis, :]

        """ 事後条件を確認 """
        check = np.sum(new_V_supply_d_t_i, axis=0)
        assert all(check[H] <= V_hs_dsgn_H)
        assert all(check[C] <= V_hs_dsgn_C)

    elif constants.change_V_supply_d_t_i_max == Vサプライの上限キャップ.ピンポイントでキャップ.value:
        # 委員より提案 案2('24/01)

        """ 設計風量をキャップ上限とする """
        V_hs_dsgn_C = V_hs_dsgn_C if V_hs_dsgn_C is not None else float('inf')
        V_hs_dsgn_H = V_hs_dsgn_H if V_hs_dsgn_H is not None else float('inf')

        """ キャップを超える時刻を調べる """
        V_supply_d_t_i = np.clip(V_supply_d_t_i, V_vent_g_i, None)
        V_supply_d_t = np.sum(V_supply_d_t_i, axis=0)  # 1d-shape(5, )

        overflow_mask_H_d_t = np.logical_and(H, V_supply_d_t > V_hs_dsgn_H)
        overflow_mask_C_d_t = np.logical_and(C, V_supply_d_t > V_hs_dsgn_C)

        # 二次元と見なして使用
        overflow_mask_H_d_t_i = np.tile(overflow_mask_H_d_t, (5,1))
        overflow_mask_C_d_t_i = np.tile(overflow_mask_C_d_t, (5,1))

        """ 縮小対象のセルを調査 """  # 個別適用なので案2では2d-array
        added_mask_d_t_i = V_supply_d_t_i > V_dash_supply_d_t_i

        target_mask_H_d_t_i = np.logical_and(added_mask_d_t_i, overflow_mask_H_d_t_i)
        target_mask_C_d_t_i = np.logical_and(added_mask_d_t_i, overflow_mask_C_d_t_i)

        """ 縮小対象セルの削減量を計算 """
        # 全体で削減すべき量
        overflow_values_H_d_t = V_supply_d_t - V_hs_dsgn_H
        overflow_values_C_d_t = V_supply_d_t - V_hs_dsgn_C
        # 削減場所では限界値以上になっている

        masked_vs_H_d_t_i = np.where(target_mask_H_d_t_i, V_supply_d_t_i, 0)
        added_sums_H_d_t = np.sum(masked_vs_H_d_t_i, axis=0)
        added_sums_H_d_t_i = np.tile(added_sums_H_d_t, (5,1))

        masked_vs_C_d_t_i = np.where(target_mask_C_d_t_i, V_supply_d_t_i, 0)
        added_sums_C_d_t = np.sum(masked_vs_C_d_t_i, axis=0)
        added_sums_C_d_t_i = np.tile(added_sums_C_d_t, (5,1))

        default_subtract_d_t_i = np.zeros_like(V_supply_d_t_i)

        ratio_H_d_t_i = np.divide(
            masked_vs_H_d_t_i,
            np.floor(added_sums_H_d_t_i * 1000) / 1000,  # 超えない工夫(引くのを大き目に)
            where=target_mask_H_d_t_i, out=default_subtract_d_t_i)
        # 削減量に値の割合を適用
        subtract_H_d_t_i = ratio_H_d_t_i * np.tile(overflow_values_H_d_t, (5,1))

        ratio_C_d_t_i = np.divide(
            masked_vs_C_d_t_i,
            np.floor(added_sums_C_d_t_i * 1000) / 1000,
            where=target_mask_C_d_t_i, out=default_subtract_d_t_i)
        # 削減量に値の割合を適用
        subtract_C_d_t_i = ratio_C_d_t_i * np.tile(overflow_values_C_d_t, (5,1))

        """ 元から制限を超えてしまってないか念のためチェックします """
        added_mask_d_t = np.sum(added_mask_d_t_i, axis=0)
        # NOTE: 増加していないのに、制限を超えてしまっている時刻がないか
        should_be_target = np.logical_or(overflow_values_H_d_t > 0, overflow_values_C_d_t > 0)
        errors = np.logical_and(added_mask_d_t == 0, should_be_target)
        assert not np.any(errors), "元から制限を超えている時刻があるようです."

        """ 減算の実行 """
        new_V_supply_d_t_i = np.where(
            target_mask_H_d_t_i,  # 引き算対象セル
            V_supply_d_t_i - subtract_H_d_t_i,
            V_supply_d_t_i)  # 引き算しない箇所の値

        new_V_supply_d_t_i = np.where(
            target_mask_C_d_t_i,  # 引き算対象セル
            new_V_supply_d_t_i - subtract_C_d_t_i,
            new_V_supply_d_t_i)  # 引き算しない箇所の値

        """ 事後条件の確認"""
        check = np.sum(new_V_supply_d_t_i, axis=0)
        # TODO: バグ修正して有効にする
        assert all(check[H] <= V_hs_dsgn_H)
        assert all(check[C] <= V_hs_dsgn_C)

    else:
        raise ValueError("change_V_supply_d_t_i is out of range")

    return new_V_supply_d_t_i


def get_V_supply_d_t_i(L_star_H_d_t_i, L_star_CS_d_t_i, Theta_sur_d_t_i, l_duct_i, Theta_star_HBR_d_t, V_vent_g_i,
                       V_dash_supply_d_t_i, VAV, region, Theta_hs_out_d_t):
    """(43-1)(43-2)(43-3)(43-4)(43-5)

    Args:
      L_star_H_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの熱取得を含む負荷バランス時の暖房負荷（MJ/h）
      L_star_CS_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの熱取得を含む負荷バランス時の冷房顕熱負荷（MJ/h）
      Theta_sur_d_t_i: 日付dの時刻tにおけるダクトiの周囲の空気温度（℃）
      l_duct_i: ダクトiの長さ（m）
      Theta_HBR_d_t: 日付dの時刻tにおける負荷バランス時の居室の室温（℃）
      V_vent_g_i: 暖冷房区画iの全般換気量（m3/h）
      V_dash_supply_d_t_i: 日付dの時刻tにおける暖冷房区画iのVAV調整前の吹き出し風量（m3/h）
      VAV: VAV
      region: 地域区分
      Theta_hs_out_d_t: 日付dの時刻tにおける熱源機の出口における空気温度（℃）
      Theta_star_HBR_d_t: returns: 日付dの時刻tにおける暖冷房区画iの吹き出し風量（m3/h）

    Returns:
      日付dの時刻tにおける暖冷房区画iの吹き出し風量（m3/h）

    """
    H, C, M = get_season_array_d_t(region)
    c_p_air = get_c_p_air()
    rho_air = get_rho_air()
    phi_i = get_phi_i()
    V_supply_d_t_i = np.zeros((5, 24 * 365))

    V_vent_g_i = np.reshape(V_vent_g_i, (5, 1))
    V_vent_g_i = V_vent_g_i.repeat(24 * 365, axis=1)

    if VAV == True:

        # 暖房期 (43-1)

        f1 = np.logical_and(H, np.logical_and(Theta_hs_out_d_t > Theta_star_HBR_d_t,
                                              np.sum(L_star_H_d_t_i[:5, :], axis=0) > 0))

        term2_H = (Theta_hs_out_d_t[f1] - Theta_sur_d_t_i[:, f1]) * phi_i[:, np.newaxis] * l_duct_i[:, np.newaxis] * 3600

        V_supply_d_t_i[:, f1] = (L_star_H_d_t_i[:, f1] * 10 ** 6 + term2_H) / \
                              (c_p_air * rho_air * (Theta_hs_out_d_t[f1] - Theta_star_HBR_d_t[f1]))

        f2 = np.logical_and(H, np.logical_or(Theta_hs_out_d_t <= Theta_star_HBR_d_t, np.sum(L_star_H_d_t_i[:5, :], axis=0) <= 0))

        V_supply_d_t_i[:, f2] = V_vent_g_i[:, f2]

        # 冷房期 (43-2)
        f3 = np.logical_and(C, np.logical_and(Theta_hs_out_d_t < Theta_star_HBR_d_t,
                                              np.sum(L_star_CS_d_t_i[:5, :], axis=0) > 0))

        term2_C = (Theta_sur_d_t_i[:, f3] - Theta_hs_out_d_t[f3]) * phi_i[:, np.newaxis] * l_duct_i[:, np.newaxis] * 3600

        V_supply_d_t_i[:, f3] = (L_star_CS_d_t_i[:, f3] * 10 ** 6 + term2_C) / \
                              (c_p_air * rho_air * (Theta_star_HBR_d_t[f3] - Theta_hs_out_d_t[f3]))

        f4 = np.logical_and(C, np.logical_or(Theta_hs_out_d_t >= Theta_star_HBR_d_t,
                                             np.sum(L_star_CS_d_t_i[:5, :], axis=0) <= 0))

        V_supply_d_t_i[:, f4] = V_vent_g_i[:, f4]

        # 中間期 (43-3)
        V_supply_d_t_i[:, M] = V_vent_g_i[:, M]

    elif VAV == False:

        # 暖房期および冷房期 (43-4)
        HC = np.logical_or(H, C)
        V_supply_d_t_i[:, HC] = V_dash_supply_d_t_i[:, HC]

        # 中間期 (43-5)
        V_supply_d_t_i[:, M] = V_vent_g_i[:, M]
    else:
        raise ValueError(VAV)

    return V_supply_d_t_i


# ============================================================================
# 10.4 VAV調整前の吹き出し風量
# ============================================================================

def get_V_dash_supply_d_t_i(r_supply_des_i, V_dash_hs_supply_d_t, V_vent_g_i):
    """(44)

    Args:
      r_supply_des_i: 暖冷房区画iの風量バランス（-）
      V_dash_hs_supply_d_t: 日付dの時刻tにおける暖冷房区画iのVAV調整前の吹き出し風量（m3/h）
      V_vent_g_i: 暖冷房区画iの全般換気量（m3/h）

    Returns:
      日付dの時刻tにおけるVAV調整前の熱源機の風量（m3/h）

    """
    return np.maximum(r_supply_des_i[:5, np.newaxis] * V_dash_hs_supply_d_t,
                      V_vent_g_i[:5, np.newaxis])

def get_V_dash_supply_d_t_i_2023(r_supply_des_d_t_i, V_dash_hs_supply_d_t, V_vent_g_i):
    """(44)

    Args:
      r_supply_des_d_t_i: 暖冷房区画iの1時間ごとの風量バランス（-）
      V_dash_hs_supply_d_t: 日付dの時刻tにおける暖冷房区画iのVAV調整前の吹き出し風量（m3/h）
      V_vent_g_i: 暖冷房区画iの全般換気量（m3/h）

    Returns:
      日付dの時刻tにおけるVAV調整前の熱源機の風量（m3/h）

    """
    return np.maximum(r_supply_des_d_t_i * V_dash_hs_supply_d_t,
                      V_vent_g_i[:5, np.newaxis])


def get_r_supply_des_i(A_HCZ_i):
    """(45)

    Args:
      A_HCZ_i: 暖冷房区画iの床面積（m2）

    Returns:
      暖冷房区画iの風量バランス（-）

    """
    return A_HCZ_i / np.sum(A_HCZ_i[:5])

def get_r_supply_des_d_t_i_2023(region, L_CS_d_t_i, L_H_d_t_i):
    """(45)-1

    Args:
      region:
      L_CS_d_t_i: 暖冷房区画iの1時間当たりの冷房顕熱負荷（MJ/h）
      L_H_d_t_i: 暖冷房区画iの1時間当たりの暖房負荷（MJ/h）

    Returns:
      暖冷房区画iの1時間当たりの風量バランス（-）

    """

    from jjjexperiment.jjj_section4_2_a import get_season_array_d_t
    H, C, M = get_season_array_d_t(region)
    r_supply_des_d_t_i = np.zeros((5, 24 * 365))

    # NOTE: よりシンプルに考えるため、どの時刻でとっても合計が1となる配列を作成します

    sum_L_H_d_t = np.sum(L_H_d_t_i[:5, H], axis=0)  # 1d-shape(4056, )
    sum_L_H_d_t = np.reshape(sum_L_H_d_t, (1, len(sum_L_H_d_t)))  # 2d-shape(1, 4056)

    r_supply_des_d_t_i[:, H] \
      = np.divide( \
          L_H_d_t_i[:5, H],  # 2d-shape(5, 4056)
          sum_L_H_d_t,       # 2d-shape(1, 4056)
          where=sum_L_H_d_t!=0,
          out=0.2 * np.ones_like(L_H_d_t_i[:5, H]))  # NOTE: where False 時の値

    sum_L_CS_d_t = np.sum(L_CS_d_t_i[:5, C], axis=0)
    sum_L_CS_d_t = np.reshape(sum_L_CS_d_t, (1, len(sum_L_CS_d_t)))  # 2d-shape(1, 2808)

    r_supply_des_d_t_i[:, C] \
      = np.divide(
          L_CS_d_t_i[:5, C],  # 2d-shape(5, 2808)
          sum_L_CS_d_t,       # 2d-shape(1, 2808)
          where=sum_L_CS_d_t!=0,
          out=0.2 * np.ones_like(L_CS_d_t_i[:5, C]))  # NOTE: where False 時の値

    r_supply_des_d_t_i[:, M] = 0.2  # NOTE: 合計で1となるよう

    # 確認コード: 全ての時刻で合計が1(バランス)
    sum_each_columns = np.sum(r_supply_des_d_t_i, axis=0)
    # NOTE: math ライブラリなど使わないない簡易的なチェックにしています
    sum_each_columns.all()
    condition = (sum_each_columns > 0.9) & (sum_each_columns < 1.1)
    check = sum_each_columns[condition]
    assert len(check) == len(sum_each_columns)

    return r_supply_des_d_t_i


# ============================================================================
# 11 暖冷房区画
# ============================================================================

# ============================================================================
# 11.1 実際の居室の室温・絶対湿度
# ============================================================================

def get_Theta_HBR_d_t_i(Theta_star_HBR_d_t, V_supply_d_t_i, Theta_supply_d_t_i, U_prt, A_prt_i, Q, A_HCZ_i, L_star_H_d_t_i, L_star_CS_d_t_i, region,
                        Theta_uf_d_t, r_A_ufvnt, A_A, A_MR, A_OR):
    """(46-1)(46-2)(46-3)

    Args:
      Theta_star_HBR_d_t: 日付dの時刻tにおける負荷バランス時の居室の室温（℃）
      V_supply_d_t_i: 日付dの時刻tにおける暖冷房区画iの吹き出し風量（m3/h）
      Theta_supply_d_t_i: 日付dの時刻tにおける負荷バランス時の居室の室温（℃）
      U_prt: 間仕切りの熱貫流率（W/(m2・K)）
      A_prt_i: 暖冷房区画iから見た非居室の間仕切りの面積（m2）
      Q: 当該住戸の熱損失係数（W/(m2・K)）
      A_HCZ_i: 暖冷房区画iの床面積（m2）
      L_star_H_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの間仕切りの熱取得を含む実際の暖房負荷（MJ/h）
      L_star_CS_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの間仕切りの熱取得を含む実際の冷房顕熱負荷（MJ/h）
      region: 地域区分
      Theta_uf_d_t: 日付dの時刻tにおける床下温度（℃）
      r_A_ufvnt(float): 当該住戸において、床下空間全体の面積に対する空気を供給する床下空間の面積の比 (-)
      A_A(float): 床面積の合計 (m2)
      A_MR(float): 主たる居室の床面積 (m2)
      A_OR(float): その他の居室の床面積 (m2)

    Returns:

    """
    H, C, M = get_season_array_d_t(region)
    c_p_air = get_c_p_air()
    rho_air = get_rho_air()
    U_s = get_U_s()

    Theta_HBR_d_t_i = np.zeros((5, 24 * 365))
    # A_HCZ_i = np.reshape(A_HCZ_i, (5, 0))

    # 暖房期 (46-1)
    if constants.change_underfloor_temperature == 2:
      # 当該住戸の暖冷房区画iの空気を供給する床下空間に接する床の面積(m2) (7)
      A_s_ufvnt_i = [calc_A_s_ufvnt_i(i, r_A_ufvnt, A_A, A_MR, A_OR) for i in range(1, 13)]

      Theta_HBR_d_t_i[:, H] = Theta_star_HBR_d_t[H] + (c_p_air * rho_air * V_supply_d_t_i[:, H] * \
                                                    (Theta_supply_d_t_i[:, H] - Theta_star_HBR_d_t[H])
                                                      + U_s * np.array(A_s_ufvnt_i)[:5, np.newaxis] * (Theta_uf_d_t[H] - Theta_star_HBR_d_t[H])[np.newaxis, :]
                                                      - L_star_H_d_t_i[:, H] * 10 ** 6) / \
                         (c_p_air * rho_air * V_supply_d_t_i[:, H] + (U_prt * A_prt_i[:, np.newaxis] + Q * A_HCZ_i[:, np.newaxis]) * 3600)
    else:
      Theta_HBR_d_t_i[:, H] = Theta_star_HBR_d_t[H] + (c_p_air * rho_air * V_supply_d_t_i[:, H] * \
                                                    (Theta_supply_d_t_i[:, H] - Theta_star_HBR_d_t[H]) - L_star_H_d_t_i[:, H] * 10 ** 6) / \
                         (c_p_air * rho_air * V_supply_d_t_i[:, H] + (U_prt * A_prt_i[:, np.newaxis] + Q * A_HCZ_i[:, np.newaxis]) * 3600)

    # 暖冷房区画iの実際の居室の室温θ_(HBR,d,t,i)は、暖房期において負荷バランス時の居室の室温θ_(HBR,d,t)^*を下回る場合、
    # 負荷バランス時の居室の室温θ_(HBR,d,t)^*に等しい
    Theta_HBR_d_t_i[:, H] = np.clip(Theta_HBR_d_t_i[:, H], Theta_star_HBR_d_t[H], None)

    # 冷房期 (46-2)
    Theta_HBR_d_t_i[:, C] = Theta_star_HBR_d_t[C] - (c_p_air * rho_air * V_supply_d_t_i[:, C] * \
                                                    (Theta_star_HBR_d_t[C] - Theta_supply_d_t_i[:, C]) - L_star_CS_d_t_i[:, C] * 10 ** 6) / \
                         (c_p_air * rho_air * V_supply_d_t_i[:, C] + (U_prt * A_prt_i[:, np.newaxis] + Q * A_HCZ_i[:, np.newaxis]) * 3600)

    # 冷房期において負荷バランス時の居室の室温θ_(HBR,d,t)^*を上回る場合、負荷バランス時の居室の室温θ_(HBR,d,t)^*に等しい
    Theta_HBR_d_t_i[:, C] = np.clip(Theta_HBR_d_t_i[:, C], None, Theta_star_HBR_d_t[C])

    # 中間期 (46-3)
    Theta_HBR_d_t_i[:, M] = Theta_star_HBR_d_t[M]

    return Theta_HBR_d_t_i

def get_Theta_HBR_i_2023(Theta_star_HBR_d_t, V_supply_d_t_i, Theta_supply_d_t_i, U_prt, A_prt_i, Q, A_HCZ_i, L_star_H_d_t_i, L_star_CS_d_t_i, region,
                         A_HCZ_R_i, Theta_HBR_d_t_i, t: int):
    """ get_Theta_HBR_d_t_i のループ用 時点単発計算

    前時刻の値を利用: \n
      Theta_star_HBR_d_t: 日付dの時刻tにおける負荷バランス時の居室の室温（℃） \n
      Theta_HBR_d_t_i: xxx \n
      V_supply_d_t_i: 日付dの時刻tにおける暖冷房区画iの吹き出し風量（m3/h） \n
      Theta_supply_d_t_i: 日付dの時刻tにおける負荷バランス時の居室の室温（℃） \n
      U_prt: 間仕切りの熱貫流率（W/(m2・K)） \n
      A_prt_i: 暖冷房区画iから見た非居室の間仕切りの面積（m2） \n
      Q: 当該住戸の熱損失係数（W/(m2・K)） \n
      A_HCZ_i: 暖冷房区画iの床面積（m2） \n
      L_star_H_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの間仕切りの熱取得を含む実際の暖房負荷（MJ/h） \n
      L_star_CS_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの間仕切りの熱取得を含む実際の冷房顕熱負荷（MJ/h） \n
      region: 地域区分 \n

    Extended Args: \n
      A_HCZ_R_i: 標準住戸における暖冷房区画の床面積[m2] \n
      idx: 時系列データにおけるインデックス \n

    Returns: \n
      (日付dの時刻tにおける)暖冷房区画iの実際の居室の室温[℃] \n

    """
    H, C, M = get_season_array_d_t(region)
    c_p_air = get_c_p_air()
    rho_air = get_rho_air()

    # NOTE: shape(5,) -> shape(5,1)
    A_prt_i = A_prt_i.reshape(-1,1)
    A_HCZ_i = A_HCZ_i.reshape(-1,1)
    A_HCZ_R_i = A_HCZ_R_i.reshape(-1,1)

    # 暖房期 (46-1)
    if H[t]:
      # NOTE: 時系列データの最初の計算では繰り越し:なしとしています
      cbri = get_C_BR_i(A_HCZ_i, A_HCZ_R_i)
      arr_theta = (Theta_HBR_d_t_i[:, t-1:t] - Theta_star_HBR_d_t[t]) if 0 < t else 0
      capacity = cbri * arr_theta  # 熱容量[J]

      arr_above_1 = c_p_air * rho_air * V_supply_d_t_i[:, t:t+1] * (Theta_supply_d_t_i[:, t:t+1] - Theta_star_HBR_d_t[t])
      arr_above_2 = -1 * L_star_H_d_t_i[:, t:t+1] * 10 ** 6  # MJ/h -> J/h

      arr_below_1 = c_p_air * rho_air * V_supply_d_t_i[:, t:t+1]
      arr_below_2 = (U_prt * A_prt_i + Q * A_HCZ_i) * 3600

      Theta_HBR_i = Theta_star_HBR_d_t[t:t+1] \
        + (arr_above_1 + capacity + arr_above_2) / (arr_below_1 + arr_below_2 + cbri)

      # 暖冷房区画iの実際の居室の室温θ_(HBR,d,t,i)は、暖房期において負荷バランス時の居室の室温θ_(HBR,d,t)^*を下回る場合、
      # 負荷バランス時の居室の室温θ_(HBR,d,t)^*に等しい
      Theta_HBR_i = np.clip(Theta_HBR_i, Theta_star_HBR_d_t[t], None)

    # 冷房期 (46-2)
    elif C[t]:
      cbri = get_C_BR_i(A_HCZ_i, A_HCZ_R_i)
      arr_theta = (Theta_star_HBR_d_t[t] - Theta_HBR_d_t_i[:, t-1:t])
      capacity = cbri * arr_theta  # 熱容量[J]

      arr_above_1 = c_p_air * rho_air * V_supply_d_t_i[:, t:t+1] * (Theta_star_HBR_d_t[t] - Theta_supply_d_t_i[:, t:t+1])
      arr_above_2 = -1 * L_star_CS_d_t_i[:, t:t+1] * 10 ** 6

      arr_below_1 = c_p_air * rho_air * V_supply_d_t_i[:, t:t+1]
      arr_below_2 = (U_prt * A_prt_i + Q * A_HCZ_i) * 3600

      Theta_HBR_i = Theta_star_HBR_d_t[t:t+1] \
        -1 * (arr_above_1 + capacity + arr_above_2) / (arr_below_1 + arr_below_2 + cbri)

      # 冷房期において負荷バランス時の居室の室温θ_(HBR,d,t)^*を上回る場合、負荷バランス時の居室の室温θ_(HBR,d,t)^*に等しい
      Theta_HBR_i = np.clip(Theta_HBR_i, None, Theta_star_HBR_d_t[t])

    # 中間期 (46-3)
    elif M[t]:
      Theta_HBR_i = Theta_star_HBR_d_t[t:t+1]

    return Theta_HBR_i

def get_C_BR_i(A_HCZ_i, A_HCZ_R_i):
    """区画i毎の居室の熱容量[J/K]"""
    Alpha_HCZ_i = np.array([
        [constants.Alpha_HCZ_i[0]],
        [constants.Alpha_HCZ_i[1]],
        [constants.Alpha_HCZ_i[2]],
        [constants.Alpha_HCZ_i[3]],
        [constants.Alpha_HCZ_i[4]]
      ])
    C_BR_R_i = 12.6 * 1000 * A_HCZ_R_i * 2.4 + Alpha_HCZ_i * 1000
    return A_HCZ_i / A_HCZ_R_i * C_BR_R_i  # 5x1

def get_X_HBR_d_t_i(X_star_HBR_d_t):
    """(47)

    Args:
      X_star_HBR_d_t: 日付dの時刻tにおける負荷バランス時の居室の絶対湿度（kg/kg(DA)）

    Returns:
      日付dの時刻tにおける暖冷房区画iの実際の居室の絶対湿度（kg/kg(DA)）

    """
    X_star_HBR_d_t_i = np.tile(X_star_HBR_d_t, (5, 1))
    return X_star_HBR_d_t_i


# ============================================================================
# 11.2 実際の非居室の室温・絶対湿度
# ============================================================================

def get_Theta_NR_d_t(Theta_star_NR_d_t, Theta_star_HBR_d_t, Theta_HBR_d_t_i, A_NR, V_vent_l_NR_d_t, V_dash_supply_d_t_i, V_supply_d_t_i, U_prt, A_prt_i, Q):
    """(48a)(48b)(48c)(48d)

    Args:
      Theta_star_NR_d_t: 日付dの時刻tにおける実際の非居室の室温（℃）
      Theta_star_HBR_d_t: 日付dの時刻tにおける負荷バランス時の居室の室温（℃）
      Theta_HBR_d_t_i: 日付dの時刻tにおける暖冷房区画iの実際の居室の室温（℃）
      A_NR: 非居室の床面積（m2）
      V_vent_l_NR_d_t: 日付dの時刻tにおける非居室の局所換気量（m3/h）
      V_dash_supply_d_t_i: 日付dの時刻tにおける暖冷房区画iのVAV調整前の吹き出し風量（m3/h）
      V_supply_d_t_i: 日付dの時刻tにおける暖冷房区画iの吹き出し風量（m3/h）
      U_prt: 間仕切りの熱貫流率（W/(m2・K)）
      A_prt_i: 暖冷房区画iから見た非居室の間仕切りの面積（m2）
      Q: 当該住戸の熱損失係数（W/(m2・K)）

    Returns:
      日付dの時刻tにおける実際の非居室の室温

    """
    c_p_air = get_c_p_air()
    rho_air = get_rho_air()

    # (48d)
    k_dash_d_t_i = c_p_air * rho_air * (V_dash_supply_d_t_i / 3600) + U_prt * A_prt_i[:, np.newaxis]

    # (48c)
    k_prt_d_t_i = c_p_air * rho_air * (V_supply_d_t_i / 3600) + U_prt * A_prt_i[:, np.newaxis]

    # (48b)
    k_evp_d_t = (Q - 0.35 * 0.5 * 2.4) * A_NR + c_p_air * rho_air * (V_vent_l_NR_d_t / 3600)

    # (48a)
    Theta_NR_d_t = Theta_star_NR_d_t + (-1 * np.sum(k_dash_d_t_i[:5] * (Theta_star_HBR_d_t - Theta_star_NR_d_t), axis=0) + \
                   np.sum(k_prt_d_t_i[:5] * (Theta_HBR_d_t_i[:5] - Theta_star_NR_d_t), axis=0)) / \
                   (k_evp_d_t + np.sum(k_prt_d_t_i[:5], axis=0))

    return Theta_NR_d_t

def get_Theta_NR_2023(Theta_star_NR_d_t, Theta_star_HBR_d_t, Theta_HBR_d_t_i, A_NR, V_vent_l_NR_d_t, V_dash_supply_d_t_i, V_supply_d_t_i, U_prt, A_prt_i, Q, Theta_NR_d_t, t: int):
    """ get_Theta_NR_d_t のループ用 時点単発計算

    前時刻の値を利用: \
      Theta_star_NR_d_t: 日付dの時刻tにおける実際の非居室の室温（℃） \
      Theta_NR_d_t_i: xxx \
    Extended Args:
      idx: 時系列データにおけるインデックス

    Returns:
      (日付dの時刻tにおける)実際の非居室の室温 [℃]

    """
    c_p_air = get_c_p_air()
    rho_air = get_rho_air()

    # NOTE: shape(5,) -> shape(5,1)
    A_prt_i = A_prt_i.reshape(-1,1)

    # (48d)
    k_dash_i = c_p_air * rho_air * (V_dash_supply_d_t_i[:, t:t+1] / 3600) + U_prt * A_prt_i  # 5x1
    # (48c)
    k_prt_i = c_p_air * rho_air * (V_supply_d_t_i[:, t:t+1] / 3600) + U_prt * A_prt_i  # 5x1
    # (48b)
    k_evp = (Q - 0.35 * 0.5 * 2.4) * A_NR + c_p_air * rho_air * (V_vent_l_NR_d_t[t] / 3600)  # 5x1

    # CHECK: 資料 Theta_NR_d_t_i -> Theta_NR_d_t が正かな?
    arr1 = -1 * np.sum(k_dash_i, axis=0) * (Theta_star_HBR_d_t[t] - Theta_star_NR_d_t[t])
    arr2 = np.sum(k_prt_i * (Theta_HBR_d_t_i[:, t:t+1] - Theta_star_NR_d_t[t]), axis=0)
    arr3 = np.sum(get_C_NR_i(A_NR) * (Theta_NR_d_t[t-1:t] - Theta_star_NR_d_t[t]), axis=0)

    # (48a)
    arr_above = arr1 + arr2 + arr3
    arr_below = k_evp + np.sum(k_prt_i, axis=0) + np.sum(get_C_NR_i(A_NR), axis=0)
    Theta_NR = Theta_star_NR_d_t[t] + arr_above / arr_below

    return Theta_NR

def get_C_NR_i(A_NR) -> float:
    """区画i毎の非居室の熱容量[J/K]"""
    C_NR_R_i = 12.6 * 1000 * constants.A_NR_R * 2.4 + constants.Alpha_NR_i * 1000  # 5x1
    return A_NR / constants.A_NR_R * C_NR_R_i

def get_X_NR_d_t(X_star_NR_d_t):
    """(49)

    Args:
      X_star_NR_d_t: 日付dの時刻tにおける非居室の負荷バランス時の絶対湿度（kg/kg(DA)）

    Returns:
      日付dの時刻tにおける実際の非居室の絶対湿度（kg/kg(DA)）

    """
    return X_star_NR_d_t

# ============================================================================
# 11.3 負荷バランス時の居室の室温・絶対湿度
# ============================================================================

def get_Theta_star_HBR_d_t(Theta_ex_d_t, region):
    """(50-1)(50-2)(50-3)

    Args:
      Theta_ex_d_t: 日付dの時刻tにおける外気温度（℃）
      region: 地域区分

    Returns:
      日付dの時刻tにおける負荷バランス時の居室の室温（℃）

    """
    H, C, M = get_season_array_d_t(region)
    Theta_set_H = get_Theta_set_H()
    Theta_set_C = get_Theta_set_C()

    Theta_star_HBR_d_t = np.zeros(24 * 365)

    # 暖房期
    Theta_star_HBR_d_t[H] = Theta_set_H

    # 冷房期
    Theta_star_HBR_d_t[C] = Theta_set_C

    # 中間期
    f1 = np.logical_and(M, np.logical_and(Theta_set_H <= Theta_ex_d_t, Theta_ex_d_t<= Theta_set_C))
    Theta_star_HBR_d_t[f1] = Theta_ex_d_t[f1]

    f2 = np.logical_and(M, Theta_ex_d_t > Theta_set_C)
    Theta_star_HBR_d_t[f2] = Theta_set_C

    f3 = np.logical_and(M, Theta_ex_d_t < Theta_set_H)
    Theta_star_HBR_d_t[f3] = Theta_set_H

    return Theta_star_HBR_d_t


def get_X_star_HBR_d_t(X_ex_d_t, region):
    """(51-1)(51-2)(51-3)

    Args:
      X_ex_d_t: 日付dの時刻tにおける外気絶対湿度（kg/kg(DA)）
      region: 地域区分

    Returns:
      日付dの時刻tにおける負荷バランス時の居室の絶対湿度（kg/kg(DA)）

    """
    H, C, M = get_season_array_d_t(region)
    X_set_C = get_X_set_C()

    X_star_HBR_d_t = np.zeros(24 * 365)

    # 暖房期
    X_star_HBR_d_t[H] = X_ex_d_t[H]

    # 冷房期
    X_star_HBR_d_t[C] = X_set_C

    # 中間期
    X_star_HBR_d_t[M] = X_ex_d_t[M]

    return X_star_HBR_d_t


# ============================================================================
# 11.4 負荷バランス時の非居室の室温・絶対湿度
# ============================================================================

def get_Theta_star_NR_d_t(Theta_star_HBR_d_t, Q, A_NR, V_vent_l_NR_d_t, V_dash_supply_d_t_i, U_prt, A_prt_i, L_H_d_t_i, L_CS_d_t_i, region):
    """(52-1)(52-2)(52-3)

    Args:
      Theta_star_HBR_d_t: 日付dの時刻tにおける負荷バランス時の居室の室温（℃）
      Q: 当該住戸の熱損失係数（W/(m2・K)）
      A_NR: 非居室の床面積（m2）
      V_vent_l_NR_d_t: 日付dの時刻tにおける非居室の局所換気量（m3/h）
      V_dash_supply_d_t_i: 日付dの時刻tにおける暖冷房区画iのVAV調整前の吹き出し風量（m3/h）
      U_prt: 間仕切りの熱貫流率（W/(m2・K)）
      A_prt_i: 暖冷房区画iから見た非居室の間仕切りの面積（m2）
      L_H_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの暖房負荷（MJ/h）
      L_CS_d_t_i: 日付dの時刻tにおける暖冷房区画iの1時間当たりの冷房顕熱負荷（MJ/h）
      region: 地域区分

    Returns:
      日付dの時刻tにおける負荷バランス時の非居室の室温（℃）

    """
    H, C, M = get_season_array_d_t(region)
    c_p_air = get_c_p_air()
    rho_air = get_rho_air()

    Theta_star_NR_d_t = np.zeros(24 * 365)

    # 暖房期 (52-1)
    Theta_star_NR_d_t[H] = Theta_star_HBR_d_t[H] - np.sum(L_H_d_t_i[5:12, H], axis=0) / \
                           ((Q - 0.35 * 0.5 * 2.4) * A_NR + c_p_air * rho_air * (V_vent_l_NR_d_t[H] / 3600) + \
                                                    np.sum(c_p_air * rho_air * (V_dash_supply_d_t_i[:5, H] / 3600) + U_prt * A_prt_i[:5, np.newaxis], axis=0)) * \
                                                    (10 ** 6 / 3600)

    # 冷房期 (52-2)
    Theta_star_NR_d_t[C] = Theta_star_HBR_d_t[C] + np.sum(L_CS_d_t_i[5:12, C], axis=0) / \
                           ((Q - 0.35 * 0.5 * 2.4) * A_NR + c_p_air * rho_air * (V_vent_l_NR_d_t[C] / 3600) + \
                                                    np.sum(c_p_air * rho_air * (V_dash_supply_d_t_i[:5, C] / 3600) + U_prt * A_prt_i[:5, np.newaxis], axis=0)) * \
                                                    (10 ** 6 / 3600)

    # 中間期 (52-3)
    Theta_star_NR_d_t[M] = Theta_star_HBR_d_t[M]

    return Theta_star_NR_d_t


def get_X_star_NR_d_t(X_star_HBR_d_t, L_CL_d_t_i, L_wtr, V_vent_l_NR_d_t, V_dash_supply_d_t_i, region):
    """(53-1)(53-2)(53-3)

    Args:
      X_star_HBR_d_t: param L_CL_d_t_i:
      L_wtr: param V_vent_l_NR_d_t:
      V_dash_supply_d_t_i: param region:
      L_CL_d_t_i: param V_vent_l_NR_d_t:
      region:
      V_vent_l_NR_d_t:

    Returns:

    """
    H, C, M = get_season_array_d_t(region)
    rho_air = get_rho_air()

    X_star_NR_d_t = np.zeros(24 * 365)

    # 暖房期 (53-1)
    X_star_NR_d_t[H] = X_star_HBR_d_t[H]

    # 冷房期 (53-2)
    X_star_NR_d_t[C] = X_star_HBR_d_t[C] + (np.sum(L_CL_d_t_i[5:12, C], axis=0) \
                        / (L_wtr * rho_air * (V_vent_l_NR_d_t[C] + np.sum(V_dash_supply_d_t_i[:5, C], axis=0)))) * 10 ** 3

   # 中間期 (53-3)
    X_star_NR_d_t[M] = X_star_HBR_d_t[M]

    return X_star_NR_d_t


# ============================================================================
# 12 ダクト
# ============================================================================

# ============================================================================
# 12.1 ダクトの周囲の空気温度
# ============================================================================

def get_Theta_sur_d_t_i(Theta_star_HBR_d_t, Theta_attic_d_t, l_duct_in_i, l_duct_ex_i, duct_insulation):
    """(54-1)(54-2)

    Args:
      Theta_star_HBR_d_t: 日付dの時刻tにおける負荷バランス時の居室の室温（℃）
      l_duct_in_i: 断熱区画内を通るダクトiの長さ（m）
      l_duct_ex_i: 断熱区画外を通るダクトiの長さ（m）
      Theta_attic_d_t: 小屋裏の空気温度 (℃)
      duct_insulation: ダクトが通過する空間

    Returns:
      日付dの時刻tにおけるダクトiの周囲の空気温度（℃）

    """
    Theta_sur_H_d_t_i = np.zeros((5, 24 * 365))

    Theta_star_HBR_d_t_i = np.tile(Theta_star_HBR_d_t, (5, 1))
    Theta_attic_d_t_i = np.tile(Theta_attic_d_t, (5, 1))

    if duct_insulation == '全てもしくは一部が断熱区画外である':
        Theta_sur_H_d_t_i = (l_duct_in_i[:, np.newaxis] * Theta_star_HBR_d_t_i + l_duct_ex_i[:, np.newaxis] * Theta_attic_d_t_i) / \
                             (l_duct_in_i[:, np.newaxis] + l_duct_ex_i[:, np.newaxis])
    elif duct_insulation == '全て断熱区画内である':
        Theta_sur_H_d_t_i = Theta_star_HBR_d_t_i
    else:
        raise ValueError(duct_insulation)

    return Theta_sur_H_d_t_i


def get_Theta_attic_d_t(Theta_SAT_d_t, Theta_star_HBR_d_t):
    """(55)

    Args:
      Theta_SAT_d_t: 日付dの時刻tにおける水平面における等価外気温度（℃）
      Theta_star_HBR_d_t: 日付dの時刻tにおける負荷バランス時の居室の室温（℃）

    Returns:
      小屋裏の空気温度 (℃)

    """
    # 温度差係数
    H = get_H()

    return Theta_SAT_d_t * H + Theta_star_HBR_d_t * (1.0 - H)


# 温度差係数 (-)
def get_H():
    """ """
    return 1.0


# ============================================================================
# 12.2 ダクトの長さ
# ============================================================================

def get_l_duct__i(l_duct_in_i, l_duct_ex_i):
    """(56)

    Args:
      l_duct_in_i: 断熱区画内を通るダクトiの長さ（m）
      l_duct_ex_i: 断熱区画外を通るダクトiの長さ（m）

    Returns:
      ダクトiの長さ（m）

    """
    return  l_duct_in_i + l_duct_ex_i


def get_l_duct_in_i(A_A):
    """(57)

    Args:
      A_A: 床面積の合計（m2）
    return: 断熱区画内を通るダクトiの長さ（m）

    Returns:

    """
    # 標準住戸の床面積の合計 [m3]
    A_A_R = get_A_A_R()

    return l_duct_in_R_i * np.sqrt(A_A / A_A_R)


def get_l_duct_ex_i(A_A):
    """(58)

    Args:
      A_A: 床面積の合計（m2）
    return: 断熱区画外を通るダクトiの長さ（m）

    Returns:

    """
    # 標準住戸の床面積の合計 [m3]
    A_A_R = get_A_A_R()

    return l_duct_ex_R_i * np.sqrt(A_A / A_A_R)


# 断熱区画内を通るダクトの長さ [m]
l_duct_in_R_i = np.array([
    25.6,
    8.6,
    0.0,
    0.0,
    0.0,
])


# 断熱区画外を通るダクトの長さ [m]
l_duct_ex_R_i = np.array([
    0.0,
    0.0,
    10.2,
    11.8,
    8.1,
])


# ダクトの長さ(合計) [m]
l_duct_R_i = np.array([
    25.6,
    8.6,
    10.2,
    11.8,
    8.1,
])


# ============================================================================
# 12.3 ダクトの熱損失係数
# ============================================================================

# ダクトiの線熱損失係数 [W/mK]
def get_phi_i():
    """ """
    return np.array([constants.phi_i] * 5)


# ============================================================================
# 13 その他
# ============================================================================

# ============================================================================
# 13.1 外気条件
# ============================================================================

def get_Theta_SAT_d_t(Theta_ex_d_t, J_d_t):
    """(59)

    Args:
      Thate_ex_d_t: 日付dの時刻tにおける外気温度（℃）
      J_d_t: 日付dの時刻tにおける水平面全天日射量（W/m2）
      Theta_ex_d_t: returns: 日付dの時刻tにおける水平面における等価外温度（℃）

    Returns:
      日付dの時刻tにおける水平面における等価外温度（℃）

    """
    return Theta_ex_d_t + 0.034 * J_d_t


# ============================================================================
# 13.2 住宅の仕様
# ============================================================================

# ============================================================================
# 13.2.2 間仕切り
# ============================================================================

def get_A_prt_i(A_HCZ_i, r_env, A_MR, A_NR, A_OR):
    """(60-1)(60-2)

    Args:
      A_HCZ_i: 暖冷房区画iの床面積（m2）
      r_env: 床面積の合計に対しる外皮の部位の面積の合計の比（-）
      A_MR: 主たる居室の床面積（m2）
      A_NR: 非居室の床面積（m2）
      A_OR: その他の居室の床面積（m2）

    Returns:
      居室（i=1～5）に対する暖冷房区画iから見た非居室の間仕切りの面積（m2）

    """
    A_XR = np.array([A_OR, A_MR, A_MR, A_MR, A_MR])
    return np.array([A_HCZ_i[i] * r_env * (A_NR / (A_XR[i] + A_NR)) for i in range(5)])


def get_U_prt():
    """(61)
    :return: 間仕切りの熱貫流率（W/(m2・K)）

    Args:

    Returns:

    """
    R_prt = get_R_prt()
    return 1 / R_prt

def get_R_prt():
    """:return: R_prt:間仕切りの熱抵抗（(m2・K)/W）"""
    return 0.46


# ============================================================================
# 13.2.4 機械換気量
# ============================================================================

# 暖冷房区画iの全般換気量
def get_V_vent_g_i(A_HCZ_i, A_HCZ_R_i):
    """(62)

    Args:
      A_HCZ_i: 暖冷房区画iの床面積 (m2)
      A_HCZ_R_i: 標準住戸における暖冷房区画iの床面積（m2）

    Returns:
      ndarray[5]: 暖冷房区画iの機械換気量 (m3/h)

    """
    # 標準住戸における暖冷房区画iの全般換気量 [m3/h]
    V_vent_g_R_i = get_V_vent_g_R_i()

    return V_vent_g_R_i * (np.array(A_HCZ_i[:5]) / np.array(A_HCZ_R_i[:5]))


# 表2 標準住戸における暖冷房区画iの全般換気量 [m3/h]
def get_V_vent_g_R_i():
    """ """
    return np.array([
        60,
        20,
        40,
        20,
        20
    ])


# 局所換気
@lru_cache()
def calc_V_vent_l_d_t():
    """ """
    V_vent_l_MR_d_t = get_V_vent_l_MR_d_t()
    V_vent_l_OR_d_t = get_V_vent_l_OR_d_t()
    V_vent_l_NR_d_t = get_V_vent_l_NR_d_t()
    return get_V_vent_l_d_t(V_vent_l_MR_d_t, V_vent_l_OR_d_t, V_vent_l_NR_d_t)


# 日付dの時刻tにおける局所換気量
def get_V_vent_l_d_t(V_vent_l_MR_d_t, V_vent_l_OR_d_t, V_vent_l_NR_d_t):
    """(63)

    Args:
      V_vent_l_MR_d_t: 日付dの時刻tにおける主たる居室の局所換気量（m3/h）
      V_vent_l_OR_d_t: 日付dの時刻tにおけるその他の居室の局所換気量（m3/h）
      V_vent_l_NR_d_t: 日付dの時刻tにおける非居室の局所換気量（m3/h）

    Returns:
      日付dの時刻tにおける局所換気量（m3/h）

    """
    return V_vent_l_MR_d_t + V_vent_l_OR_d_t + V_vent_l_NR_d_t


# 日付dの時刻tにおける主たる居室の局所換気量（m3/h）
def get_V_vent_l_MR_d_t():
    """:return: 日付dの時刻tにおける主たる居室の局所換気量（m3/h）"""
    schedule = load_schedule()
    schedule_ac = get_schedule_ac(schedule)

    table_3 = get_table_3()


    # 全日平日とみなした24時間365日の局所換気量
    tmp_a = np.tile(table_3[0], 365)

    # 全日休日とみなした24時間365日の局所換気量
    tmp_b = np.tile(table_3[1], 365)

    # 時間単位に展開した生活パターン
    schedule_extend = np.repeat(np.array(schedule_ac), 24)

    V_vent_l_MR_d_t = tmp_a * (schedule_extend == '平日') \
                    + tmp_b * (schedule_extend == '休日')

    return V_vent_l_MR_d_t


# 日付dの時刻tにおけるその他の居室の局所換気量（m3/h）
def get_V_vent_l_OR_d_t():
    """:return: 日付dの時刻tにおけるその他の居室の局所換気量（m3/h）"""
    schedule = load_schedule()
    schedule_ac = get_schedule_ac(schedule)

    table_3 = get_table_3()

    # 全日平日とみなした24時間365日の局所換気量
    tmp_a = np.tile(table_3[2], 365)

    # 全日休日とみなした24時間365日の局所換気量
    tmp_b = np.tile(table_3[3], 365)

    # 時間単位に展開した生活パターン
    schedule_extend = np.repeat(np.array(schedule_ac), 24)

    V_vent_l_OR_d_t = tmp_a * (schedule_extend == '平日') \
                      + tmp_b * (schedule_extend == '休日')

    return V_vent_l_OR_d_t


# 日付dの時刻tにおける非居室の局所換気量（m3/h）
def get_V_vent_l_NR_d_t():
    """:return: 日付dの時刻tにおける非居室の局所換気量（m3/h）"""
    schedule = load_schedule()
    schedule_ac = get_schedule_ac(schedule)

    table_3 = get_table_3()

    # 全日平日とみなした24時間365日の局所換気量
    tmp_a = np.tile(table_3[4], 365)

    # 全日休日とみなした24時間365日の局所換気量
    tmp_b = np.tile(table_3[5], 365)

    # 時間単位に展開した生活パターン
    schedule_extend = np.repeat(np.array(schedule_ac), 24)

    V_vent_l_NR_d_t = tmp_a * (schedule_extend == '平日') \
                      + tmp_b * (schedule_extend == '休日')

    return V_vent_l_NR_d_t


# 局所換気量
def get_table_3():
    """ """
    return [
        (0, 0, 0, 0, 0, 0, 75, 0, 0, 0, 0, 0, 75, 0, 0, 0, 0, 0, 150, 150, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 75, 0, 0, 0, 75, 0, 0, 0, 0, 150, 150, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 6, 2, 0, 0.8, 0, 0, 0.8, 0, 0, 0, 0.8, 0.8, 0.8, 0.8, 0.8, 52, 25, 102.8),
        (0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 1.2, 1.2, 0, 0, 0, 0, 2, 75.8, 25, 2, 0.8, 25, 27, 100.8),
    ]


# ============================================================================
# 13.2.5 内部発熱・発湿（人体を除く）
# ============================================================================

def get_q_gen_d_t(q_gen_MR_d_t, q_gen_OR_d_t, q_gen_NR_d_t):
    """(64a)

    Args:
      q_gen_MR_d_t: 日付dの時刻tにおける主たる居室の内部発熱（W）
      q_gen_OR_d_t: 日付dの時刻tにおけるその他の居室の内部発熱（W）
      q_gen_NR_d_t: 日付dの時刻tにおける非居室の内部発熱（W）

    Returns:
      日付dの時刻tにおける内部発熱（W）

    """
    return q_gen_MR_d_t + q_gen_OR_d_t + q_gen_NR_d_t


def calc_q_gen_MR_d_t(A_MR):
    """(64b)

    Args:
      A_MR: 主たる居室の床面積（m2）

    Returns:

    """
    q_gen_MR_R_d_t = get_q_gen_MR_R_d_t()

    return q_gen_MR_R_d_t * (A_MR / 29.81)


def calc_q_gen_OR_d_t(A_OR):
    """(64c)

    Args:
      A_OR: その他の居室の床面積（m2）

    Returns:

    """
    q_gen_OR_R_d_t = get_q_gen_OR_R_d_t()

    return q_gen_OR_R_d_t * (A_OR / 51.34)


def calc_q_gen_NR_d_t(A_NR):
    """(64d)

    Args:
      A_NR: 非居室の床面積（m2）

    Returns:

    """
    q_gen_NR_R_d_t = get_q_gen_NR_R_d_t()

    return q_gen_NR_R_d_t * (A_NR / 38.93)


# 日付dの時刻tにおける標準住戸の主たる居室の内部発熱（W）
def get_q_gen_MR_R_d_t():
    """:return: 日付dの時刻tにおける標準住戸の主たる居室の内部発熱（W）"""
    schedule = load_schedule()
    schedule_ac = get_schedule_ac(schedule)

    table_4 = get_table_4()


    # 全日平日とみなした24時間365日の標準住戸における内部発熱
    tmp_a = np.tile(table_4[0], 365)

    # 全日休日とみなした24時間365日の標準住戸における内部発熱
    tmp_b = np.tile(table_4[1], 365)

    # 時間単位に展開した生活パターン
    schedule_extend = np.repeat(np.array(schedule_ac), 24)

    q_gen_MR_R_d_t = tmp_a * (schedule_extend == '平日') \
                    + tmp_b * (schedule_extend == '休日')

    return q_gen_MR_R_d_t


# 日付dの時刻tにおける標準住戸のその他の居室の内部発熱（W）
def get_q_gen_OR_R_d_t():
    """:return: 日日付dの時刻tにおける標準住戸のその他の居室の内部発熱（W）"""
    schedule = load_schedule()
    schedule_ac = get_schedule_ac(schedule)

    table_4 = get_table_4()

    # 全日平日とみなした24時間365日の標準住戸における内部発熱
    tmp_a = np.tile(table_4[2], 365)

    # 全日休日とみなした24時間365日の標準住戸における内部発熱
    tmp_b = np.tile(table_4[3], 365)

    # 時間単位に展開した生活パターン
    schedule_extend = np.repeat(np.array(schedule_ac), 24)

    q_gen_OR_R_d_t = tmp_a * (schedule_extend == '平日') \
                      + tmp_b * (schedule_extend == '休日')

    return q_gen_OR_R_d_t


# 日付dの時刻tにおける標準住戸の非居室の内部発熱（W）
def get_q_gen_NR_R_d_t():
    """:return: 日付dの時刻tにおける標準住戸の非居室の内部発熱（W）"""
    schedule = load_schedule()
    schedule_ac = get_schedule_ac(schedule)

    table_4 = get_table_4()

    # 全日平日とみなした24時間365日の標準住戸における内部発熱
    tmp_a = np.tile(table_4[4], 365)

    # 全日休日とみなした24時間365日の標準住戸における内部発熱
    tmp_b = np.tile(table_4[5], 365)

    # 時間単位に展開した生活パターン
    schedule_extend = np.repeat(np.array(schedule_ac), 24)

    q_gen_NR_R_d_t = tmp_a * (schedule_extend == '平日') \
                      + tmp_b * (schedule_extend == '休日')

    return q_gen_NR_R_d_t


# 標準住戸における内部発熱
def get_table_4():
    """ """
    return [
        (66.9,66.9,66.9,66.9,66.9,66.9,123.9,383.6,323.2,307.3,134.8,66.9,286.7,271.2,66.9,66.9,236.9,288.6,407.8,383.1,423.1,339.1,312.9,278),
        (66.9,66.9,66.9,66.9,66.9,66.9,66.9,66.9,440.5,443.3,515.1,488.9,422.9,174.4,66.9,66.9,237.8,407.8,383.1,326.8,339.1,339.1,312.9,66.9),
        (18,18,18,18,18,18,18,18,18,398.2,18,18,18,18,18,18,18,18,53,53,115.5,103,258.3,137.3),
        (18,18,18,18,18,18,18,18,35.5,654.3,223,223,53,18,18,18,93,93,55.5,18,270,168.8,270,18),
        (41.5,41.5,41.5,41.5,41.5,41.5,126.1,249.9,158.3,191.3,117.5,41.5,42.5,89,41.5,41.5,105.8,105.8,112.1,118.5,155.7,416.1,314.8,174.9),
        (41.5,41.5,41.5,41.5,41.5,41.5,41.5,281.3,311,269.5,100.4,106.7,98.5,55.8,41.5,41.5,158.4,171.3,82.7,101.4,99.5,255.1,232.1,157.8),
    ]


# 日付dの時刻tにおける内部発湿
def get_w_gen_d_t(w_gen_MR_d_t, w_gen_OR_d_t, w_gen_NR_d_t):
    """(65a)

    Args:
      w_gen_MR_d_t: 日付dの時刻tにおける主たる居室の内部発湿（W）
      w_gen_OR_d_t: 日付dの時刻tにおけるその他の居室の内部発湿（W）
      w_gen_NR_d_t: 日付dの時刻tにおける非居室の内部発湿（W）

    Returns:
      日付dの時刻tにおける内部発湿（W）

    """
    return  w_gen_MR_d_t + w_gen_OR_d_t + w_gen_NR_d_t


def calc_w_gen_MR_d_t(A_MR):
    """(65b)

    Args:
      A_MR: 主たる居室の床面積（m2）

    Returns:

    """
    w_gen_MR_R_d_t = get_w_gen_MR_R_d_t()

    return w_gen_MR_R_d_t * (A_MR / 29.81)


def calc_w_gen_OR_d_t(A_OR):
    """(65c)

    Args:
      A_OR: その他の居室の床面積（m2）

    Returns:

    """
    w_gen_OR_R_d_t = get_w_gen_OR_R_d_t()

    return w_gen_OR_R_d_t * (A_OR / 51.34)


def calc_w_gen_NR_d_t(A_NR):
    """(65d)

    Args:
      A_NR: 非居室の床面積（m2）

    Returns:

    """
    w_gen_NR_R_d_t = get_w_gen_NR_R_d_t()

    return w_gen_NR_R_d_t * (A_NR / 38.93)


# 日付dの時刻tにおける標準住戸の主たる居室の内部発湿（W）
def get_w_gen_MR_R_d_t():
    """:return: 日付dの時刻tにおける標準住戸の主たる居室の内部発湿（W）"""
    schedule = load_schedule()
    schedule_ac = get_schedule_ac(schedule)

    table_5 = get_table_5()


    # 全日平日とみなした24時間365日の標準住戸における内部発湿
    tmp_a = np.tile(table_5[0], 365)

    # 全日休日とみなした24時間365日の標準住戸における内部発湿
    tmp_b = np.tile(table_5[1], 365)

    # 時間単位に展開した生活パターン
    schedule_extend = np.repeat(np.array(schedule_ac), 24)

    w_gen_MR_R_d_t = tmp_a * (schedule_extend == '平日') \
                    + tmp_b * (schedule_extend == '休日')

    return w_gen_MR_R_d_t


# 日付dの時刻tにおける標準住戸のその他の居室の内部発湿（W）
def get_w_gen_OR_R_d_t():
    """:return: 日日付dの時刻tにおける標準住戸のその他の居室の内部発湿（W）"""
    schedule = load_schedule()
    schedule_ac = get_schedule_ac(schedule)

    table_5 = get_table_5()

    # 全日平日とみなした24時間365日の標準住戸における内部発湿
    tmp_a = np.tile(table_5[2], 365)

    # 全日休日とみなした24時間365日の標準住戸における内部発湿
    tmp_b = np.tile(table_5[3], 365)

    # 時間単位に展開した生活パターン
    schedule_extend = np.repeat(np.array(schedule_ac), 24)

    w_gen_OR_R_d_t = tmp_a * (schedule_extend == '平日') \
                      + tmp_b * (schedule_extend == '休日')

    return w_gen_OR_R_d_t


# 日付dの時刻tにおける標準住戸の非居室の内部発湿（W）
def get_w_gen_NR_R_d_t():
    """:return: 日付dの時刻tにおける標準住戸の非居室の内部発湿（W）"""
    schedule = load_schedule()
    schedule_ac = get_schedule_ac(schedule)

    table_5 = get_table_5()

    # 全日平日とみなした24時間365日の標準住戸における内部発湿
    tmp_a = np.tile(table_5[4], 365)

    # 全日休日とみなした24時間365日の標準住戸における内部発湿
    tmp_b = np.tile(table_5[5], 365)

    # 時間単位に展開した生活パターン
    schedule_extend = np.repeat(np.array(schedule_ac), 24)

    w_gen_NR_R_d_t = tmp_a * (schedule_extend == '平日') \
                      + tmp_b * (schedule_extend == '休日')

    return w_gen_NR_R_d_t


# 標準住戸における内部発熱
def get_table_5():
    """ """
    return [
        (0, 0, 0, 0, 0, 0, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 25, 0, 0, 0, 0, 0, 0, 0, 0, 50, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ]


# ============================================================================
# 13.2.6 人体発熱および在室人数
# ============================================================================

# 暖房期における人体からの1人当たりの顕熱発熱量（W/人）
def get_q_p_H():
    """ """
    return 79.0


# 冷房期における人体からの1人当たりの顕熱発熱量（W/人）
def get_q_p_CS():
    """ """
    return 51.0


# 冷房期における人体からの1人当たりの潜熱発熱量（W/人）
def get_q_p_CL():
    """ """
    return 40.0


# 日付dの時刻tにおける在室人数（人）
def get_n_p_d_t(n_p_MR_d_t, n_p_OR_d_t, n_p_NR_d_t):
    """(66a)

    Args:
      q_gen_MR_d_t: 日付dの時刻tにおける主たる居室の在室人数（人）
      q_gen_OR_d_t: 日付dの時刻tにおけるその他の居室の在室人数（人）
      q_gen_NR_d_t: 日付dの時刻tにおける非居室の在室人数（人）
      n_p_MR_d_t: param n_p_OR_d_t:
      n_p_NR_d_t: returns: 日付dの時刻tにおける在室人数（人）
      n_p_OR_d_t:

    Returns:
      日付dの時刻tにおける在室人数（人）

    """
    return n_p_MR_d_t + n_p_OR_d_t + n_p_NR_d_t


def calc_n_p_MR_d_t(A_MR):
    """(66b)

    Args:
      A_MR: 主たる居室の床面積（m2）

    Returns:

    """
    n_p_MR_R_d_t = get_n_p_MR_R_d_t()

    return  n_p_MR_R_d_t * (A_MR / 29.81)


def calc_n_p_OR_d_t(A_OR):
    """(66c)

    Args:
      A_OR: その他の居室の床面積（m2）

    Returns:

    """
    n_p_OR_R_d_t = get_n_p_OR_R_d_t()

    return  n_p_OR_R_d_t * (A_OR / 51.34)


def calc_n_p_NR_d_t(A_NR):
    """(66d)

    Args:
      A_NR: 非居室の床面積（m2）

    Returns:

    """
    n_p_NR_R_d_t = get_n_p_NR_R_d_t()

    return  n_p_NR_R_d_t * (A_NR / 38.93)


# 日付dの時刻tにおける標準住戸の主たる居室の在室人数（W）
def get_n_p_MR_R_d_t():
    """:return: 日付dの時刻tにおける標準住戸の主たる居室の在室人数（W）"""
    schedule = load_schedule()
    schedule_ac = get_schedule_ac(schedule)

    table_6 = get_table_6()

    # 全日平日とみなした24時間365日の標準住戸における在室人数
    tmp_a = np.tile(table_6[0], 365)

    # 全日休日とみなした24時間365日の標準住戸における在室人数
    tmp_b = np.tile(table_6[1], 365)

    # 時間単位に展開した生活パターン
    schedule_extend = np.repeat(np.array(schedule_ac), 24)

    n_p_MR_R_d_t = tmp_a * (schedule_extend == '平日') \
                    + tmp_b * (schedule_extend == '休日')

    return n_p_MR_R_d_t


# 日付dの時刻tにおける標準住戸のその他の居室の在室人数（W）
def get_n_p_OR_R_d_t():
    """:return: 日日付dの時刻tにおける標準住戸のその他の居室の在室人数（W）"""
    schedule = load_schedule()
    schedule_ac = get_schedule_ac(schedule)

    table_6 = get_table_6()

    # 全日平日とみなした24時間365日の標準住戸における在室人数
    tmp_a = np.tile(table_6[2], 365)

    # 全日休日とみなした24時間365日の標準住戸における在室人数
    tmp_b = np.tile(table_6[3], 365)

    # 時間単位に展開した生活パターン
    schedule_extend = np.repeat(np.array(schedule_ac), 24)

    n_p_OR_R_d_t = tmp_a * (schedule_extend == '平日') \
                      + tmp_b * (schedule_extend == '休日')

    return n_p_OR_R_d_t


# 日付dの時刻tにおける標準住戸の非居室の在室人数（W）
def get_n_p_NR_R_d_t():
    """:return: 日付dの時刻tにおける標準住戸の非居室の在室人数（W）"""
    schedule = load_schedule()
    schedule_ac = get_schedule_ac(schedule)

    table_6 = get_table_6()

    # 全日平日とみなした24時間365日の標準住戸における在室人数
    tmp_a = np.tile(table_6[4], 365)

    # 全日休日とみなした24時間365日の標準住戸における在室人数
    tmp_b = np.tile(table_6[5], 365)

    # 時間単位に展開した生活パターン
    schedule_extend = np.repeat(np.array(schedule_ac), 24)

    n_p_NR_R_d_t = tmp_a * (schedule_extend == '平日') \
                      + tmp_b * (schedule_extend == '休日')

    return n_p_NR_R_d_t


# 標準住戸における内部発熱
def get_table_6():
    """ """
    return [
        (0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 0, 1, 1, 0, 0, 1, 2, 2, 3, 3, 2, 1, 1),
        (0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 2, 2, 2, 1, 0, 0, 2, 3, 3, 4, 2, 2, 1, 0),
        (4, 4, 4, 4, 4, 4, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 3),
        (4, 4, 4, 4, 4, 4, 4, 3, 1, 2, 2, 2, 1, 0, 0, 0, 1, 1, 1, 0, 2, 2, 2, 3),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ]


# ============================================================================
# 13.3 使い方
# ============================================================================

# ============================================================================
# 13.3.1 暖冷房期間
# ============================================================================

# 暖冷房期間
def get_season_array(region):
    """

    Args:
      region:

    Returns:

    """
    table_7 = get_table_7()[region-1]

    H = get_period_array(table_7[0], table_7[1])
    C = get_period_array(table_7[2], table_7[3])
    M = np.logical_and(np.logical_not(H), np.logical_not(C))
    assert sum(map(np.count_nonzero, [H, C, M])) == 365

    return H, C, M


# 暖冷房期間を24*365の配列で返す
def get_season_array_d_t(region):
    """

    Args:
      region:

    Returns:

    """
    H, C, M = get_season_array(region)

    H = np.repeat(H, 24)
    C = np.repeat(C, 24)
    M = np.repeat(M, 24)

    return H, C, M


def get_period_array(p1, p2):
    """指定月日期間のみTrueのndarrayを作成する

    指定月日期間のみTrueのndarrayを作成する。
    開始月日が終了月日が逆転する場合は、年をまたいだとみなす。

    Args:
      p1: 開始月日をtuple指定 例) 1月2日 であれば (1,2)
      p2: 終了月日をtuple指定 例) 5月4日 であれば (5,4)

    Returns:
      p1からp2の間はTrueである365の長さのndarray

    """

    if p1 is None or p2 is None:
        return np.zeros(365, dtype=bool)

    d_base = datetime.date(2018, 1, 1)   #年初
    d1 = (datetime.date(2018, p1[0], p1[1]) - d_base).days   #年初からの日数1
    d2 = (datetime.date(2018, p2[0], p2[1]) - d_base).days   #年初からの日数2

    if d1 < d2:
        # d1からd2の間はTrue
        # 例) 7月10日～8月31日
        arr = np.zeros(365, dtype=bool)
        arr[d1:d2+1] = True
    else:
        # d1からd2の間はFalse
        # 例) 9月24日～6月7日
        arr = np.ones(365, dtype=bool)
        arr[d2+1:d1] = False

    return arr


# ============================================================================
# 13.3.2 設定温度・設定絶対湿度
# ============================================================================

# 暖房時の設定温度 (℃)
def get_Theta_set_H():
    """ """
    return 20.0


# 冷房時の設定温度 (℃)
def get_Theta_set_C():
    """ """
    return 27.0


# 冷房時の設定絶対湿度(空気温度27℃、60%の時の絶対湿度とする) (kg/kg(DA))
def get_X_set_C():
    """ """
    return 0.013425743


# ============================================================================
# 13.4 暖房負荷・冷房負荷
# ============================================================================


# ============================================================================
# 13.5 空気および水の物性値
# ============================================================================

# 空気の比熱 (J/Kg・K)
def get_c_p_air():
    """ """
    return 1006.0


# 空気の密度 (kg/m3)
def get_rho_air():
    """ """
    return 1.2


# 水の蒸発潜熱 (kJ/kg) (67)
def get_L_wtr():
    """ """
    Theta = get_Theta()
    return 2500.8 - 2.3668 * Theta


# 冷房時を仮定した温度 (℃)
def get_Theta():
    """ """
    return 27
