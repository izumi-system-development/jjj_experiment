import numpy as np

def get_E_E_fan_H_d_t(P_fan_rtd_H, V_hs_vent_d_t, V_hs_supply_d_t, V_hs_dsgn_H, q_hs_H_d_t, f_SFP = None):
    """(37)

    Args:
      P_fan_rtd_H: 定格暖房能力運転時の送風機の消費電力（W）
      V_hs_vent_d_t: 日付dの時刻tにおける熱源機の風量のうちの全般換気分（m3/h）
      V_hs_supply_d_t: param V_hs_dsgn_H:暖房時の設計風量（m3/h）
      q_hs_H_d_t: 日付dの時刻tにおける1時間当たりの熱源機の平均暖房能力（-）
      V_hs_dsgn_H: returns: 日付dの時刻tにおける1時間当たりの送風機の消費電力量のうちの暖房設備への付加分（kWh/h）
      f_SFP: ファンの比消費電力 (W/(m3・h))

    Returns:
      日付dの時刻tにおける1時間当たりの送風機の消費電力量のうちの暖房設備への付加分（kWh/h）

    """
    f_SFP = get_f_SFP(f_SFP)
    E_E_fan_H_d_t = np.zeros(24 * 365)

    a = (P_fan_rtd_H - f_SFP * V_hs_vent_d_t) \
        * ((V_hs_supply_d_t - V_hs_vent_d_t) / (V_hs_dsgn_H - V_hs_vent_d_t)) * 10 ** (-3)

    E_E_fan_H_d_t[q_hs_H_d_t > 0] = np.clip(a[q_hs_H_d_t > 0], 0, None)

    return E_E_fan_H_d_t

def get_E_E_fan_C_d_t(P_fan_rtd_C, V_hs_vent_d_t, V_hs_supply_d_t, V_hs_dsgn_C, q_hs_C_d_t, f_SFP = None):
    """(38)

    Args:
      P_fan_rtd_C: 定格冷房能力運転時の送風機の消費電力（W）
      V_hs_vent_d_t: 日付dの時刻tにおける熱源機の風量のうちの全般換気分（m3/h）
      V_hs_supply_d_t: param V_hs_dsgn_C:冷房時の設計風量（m3/h）
      q_hs_C_d_t: 日付dの時刻tにおける1時間当たりの熱源機の平均冷房能力（-）
      V_hs_dsgn_C: returns: 日付dの時刻tにおける1時間当たりの送風機の消費電力量のうちの暖房設備への付加分（kWh/h）
      f_SFP: ファンの比消費電力 (W/(m3・h))

    Returns:
      日付dの時刻tにおける1時間当たりの送風機の消費電力量のうちの暖房設備への付加分（kWh/h）

    """
    f_SFP = get_f_SFP(f_SFP)
    E_E_fan_C_d_t = np.zeros(24 * 365)

    a = (P_fan_rtd_C - f_SFP * V_hs_vent_d_t) \
        * ((V_hs_supply_d_t - V_hs_vent_d_t) / (V_hs_dsgn_C - V_hs_vent_d_t)) * 10 ** (-3)

    E_E_fan_C_d_t[q_hs_C_d_t > 0] = np.clip(a[q_hs_C_d_t > 0], 0, None)

    return E_E_fan_C_d_t

# 全般換気設備の比消費電力（W/(m3/h)）
def get_f_SFP(f_SFP):
    """ """
    if f_SFP is not None:
      return f_SFP
    return 0.4 * 0.36