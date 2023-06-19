import pytest
import math

from jjjexperiment.denchu_1 import *
from jjjexperiment.denchu_2 import *

ronbun_model = Spec(
    # 論文内で使用している条件と同一
    name = "論文内使用モデル",
    P_hs_min_C = 95,
    P_hs_rtd_C = 395,
    P_hs_max_C = 780,
    q_hs_min_C = 0.7,
    q_hs_rtd_C = 2.2,
    q_hs_max_C = 3.3,

    P_hs_min_H = 95,
    P_hs_rtd_H = 395,
    P_hs_max_H = 1360,
    q_hs_min_H = 0.7,
    q_hs_rtd_H = 2.5,
    q_hs_max_H = 5.4,
    )

""" 論文におけるエアコンの使用条件 """

# エアコン吸込空気温度(冷房時)
t_ein_C = 27  # 室内機(JIS利用条件)
t_cin_C = 35  # 室外機(JIS利用条件)

# 冷房時
ronbun_cdtn_C = Condition(
    T_ein = t_ein_C,
    T_cin = t_cin_C,
    X_ein = absolute_humid(46.6, t_ein_C),
    X_cin = absolute_humid(40.0, t_cin_C),
    # NOTE: [m3/min] -> [m3/h]
    M_ein = m3ph_to_kgDAps(12.1 * 60, t_ein_C),  # NOTE: 論文より
    M_cin = m3ph_to_kgDAps(28.2 * 60, t_cin_C),  # NOTE: 論文より
    )

# エアコン吸込空気温度(暖房時)
t_ein_H = 7   # 室外機(JIS利用条件) ※逆向
t_cin_H = 20  # 室内機(JIS利用条件) ※逆向

# 暖房時
ronbun_cdtn_H = Condition(
    T_ein = t_ein_H,
    T_cin = t_cin_H,
    X_ein = absolute_humid(86.7, t_ein_H),
    X_cin = absolute_humid(58.6, t_cin_H),
    # NOTE: [m3/min] -> [m3/h]
    M_ein = m3ph_to_kgDAps(25.5 * 60, t_ein_H),  # NOTE: 論文より
    M_cin = m3ph_to_kgDAps(13.1 * 60, t_cin_H),  # NOTE: 論文より
    )

ronbun_cdtn_H.M_ein
ronbun_model.P_hs_min_C
ronbun_model.q_hs_min_C
ronbun_cdtn_C.X_ein

class Test冷媒_状態変化温度_冷房時:
    """ 冷媒の状態推移の温度が適切な範囲の値となる
    """
    T_min_evp, T_min_cnd = calc_reibai_phase_T_C(
        ronbun_model.q_hs_min_C,
        ronbun_model.P_hs_min_C / 1000,  # kW
        ronbun_cdtn_C)
    T_rtd_evp, T_rtd_cnd = calc_reibai_phase_T_C(
        ronbun_model.q_hs_rtd_C,
        ronbun_model.P_hs_rtd_C / 1000,  # kW
        ronbun_cdtn_C)
    T_max_evp, T_max_cnd = calc_reibai_phase_T_C(
        ronbun_model.q_hs_max_C,
        ronbun_model.P_hs_max_C / 1000,  # kW
        ronbun_cdtn_C)

    def test_出力レベル別_冷媒蒸発温度(self):
        """ 出力レベルを上げると冷媒蒸発温度は下がる """
        assert self.T_max_evp < self.T_rtd_evp and self.T_rtd_evp < self.T_min_evp

    def test_出力レベル別_冷媒凝縮温度(self):
        """ 出力レベルを上げると冷媒凝縮温度は上がる """
        assert self.T_min_cnd < self.T_rtd_cnd and self.T_rtd_cnd < self.T_max_cnd

    def test_状態変化温度_適正範囲(self):
        """ 冷媒が室内温度で蒸発し、外気温度で凝縮することを確認 """
        assert self.T_min_evp < 30
        assert 28 < self.T_min_cnd


class Test冷媒_状態変化温度_暖房時:
    """ 冷媒の状態推移の温度が適切な範囲の値となる
    """
    T_min_evp, T_min_cnd = calc_reibai_phase_T_H(
        ronbun_model.q_hs_min_H,
        ronbun_model.P_hs_min_H / 1000,  # kW
        ronbun_cdtn_H)
    T_rtd_evp, T_rtd_cnd = calc_reibai_phase_T_H(
        ronbun_model.q_hs_rtd_H,
        ronbun_model.P_hs_rtd_H / 1000,  # kW
        ronbun_cdtn_H)
    T_max_evp, T_max_cnd = calc_reibai_phase_T_H(
        ronbun_model.q_hs_max_H,
        ronbun_model.P_hs_max_H / 1000,  # kW
        ronbun_cdtn_H)

    def test_出力レベル別_冷媒蒸発温度(self):
        """ 出力レベルを上げると冷媒蒸発温度は下がる """
        assert self.T_max_evp < self.T_rtd_evp and self.T_rtd_evp < self.T_min_evp

    def test_出力レベル別_冷媒凝縮温度(self):
        """ 出力レベルを上げると冷媒凝縮温度は上がる """
        assert self.T_min_cnd < self.T_rtd_cnd and self.T_rtd_cnd < self.T_max_cnd

    def test_状態変化温度_適正範囲(self):
        """ 冷媒が室内温度で蒸発し、外気温度で凝縮することを確認 """
        assert self.T_min_evp < 30
        assert 28 < self.T_min_cnd


class Test成績係数比R_モデリング:

    def test_論文掲載値_曲線条件_冷房(self):
        """ 論文掲載値が論文で言っていることと矛盾しない
        """
        a2, a1, a0 = -0.018, 0.052, 0.513  # 論文掲載値
        R_ronbun_C = simu_R(a2, a1, a0)

        R1 = R_ronbun_C(ronbun_model.q_hs_min_C)
        R2 = R_ronbun_C(ronbun_model.q_hs_rtd_C)
        assert math.isclose(R1, R2, abs_tol=1e-2), "最小・定格でrは共通にします"

        R3 = R_ronbun_C(ronbun_model.q_hs_max_C)
        assert R1 > R3 and R2 > R3, "論文より曲線が下に凸にならないようにする"
        # {R1, R2, R3} = {0.54058, 0.54028, 0.48858}

    def test_論文掲載値_曲線条件_暖房(self):
        """ 論文掲載値が論文で言っていることと矛盾しない
        """
        a2, a1, a0 = -0.006, 0.019, 0.636  # 論文掲載値
        R_ronbun_H = simu_R(a2, a1, a0)

        R1 = R_ronbun_H(ronbun_model.q_hs_min_H)
        R2 = R_ronbun_H(ronbun_model.q_hs_rtd_H)
        assert math.isclose(R1, R2, abs_tol=1e-2), "最小・定格でRは共通にします"

        R3 = R_ronbun_H(ronbun_model.q_hs_max_H)
        assert R1 > R3 and R2 > R3, "論文より曲線が下に凸にならないようにする"
        # {R1, R2, R3} = {0.64636, 0.646, 0.56364}

    def test_再現計算_曲線条件_冷房(self):
        """ 再現計算値が論文内で言っていることと矛盾しない
        """
        a2, a1, a0, _ = calc_R_and_Pc_C(ronbun_model, ronbun_cdtn_C)
        R_ronbun_C = simu_R(a2, a1, a0)

        R1 = R_ronbun_C(ronbun_model.q_hs_min_C)
        R2 = R_ronbun_C(ronbun_model.q_hs_rtd_C)
        R3 = R_ronbun_C(ronbun_model.q_hs_max_C)

        assert math.isclose(R1, R2, abs_tol=1e-2), "最小・定格でrは共通にします"
        assert R1 > R3 and R2 > R3, "論文より曲線が下に凸にならないようにする"

    def test_再現計算_曲線条件_暖房(self):
        """ 再現計算値が論文内で言っていることと矛盾しない
        """
        a2, a1, a0, _ = calc_R_and_Pc_H(ronbun_model, ronbun_cdtn_H)
        R_ronbun_H = simu_R(a2, a1, a0)

        R1 = R_ronbun_H(ronbun_model.q_hs_min_H)
        R2 = R_ronbun_H(ronbun_model.q_hs_rtd_H)
        R3 = R_ronbun_H(ronbun_model.q_hs_max_H)

        assert math.isclose(R1, R2, abs_tol=1e-2), "最小・定格でrは共通にします"
        assert R1 > R3 and R2 > R3, "論文より曲線が下に凸にならないようにする"

    def test_再現計算_プロット一致_冷房(self):
        """ 再現計算値が論文内で言っていることと矛盾しない
        """
        a2, a1, a0, _ = calc_R_and_Pc_C(ronbun_model, ronbun_cdtn_C)
        R_C_repro = simu_R(a2, a1, a0)

        R1 = R_C_repro(ronbun_model.q_hs_min_C)
        R2 = R_C_repro(ronbun_model.q_hs_rtd_C)
        R3 = R_C_repro(ronbun_model.q_hs_max_C)

        _R1, _R2, _R3 = 0.54058, 0.54028, 0.48858
        assert math.isclose(_R1, R1, abs_tol=1e-2)
        assert math.isclose(_R2, R2, abs_tol=1e-2)
        assert math.isclose(_R3, R3, abs_tol=1e-2)

    def test_再現計算_プロット一致_暖房(self):
        """ 再現計算値が論文内で言っていることと矛盾しない
        """
        a2, a1, a0, _ = calc_R_and_Pc_H(ronbun_model, ronbun_cdtn_H)
        R_ronbun_H = simu_R(a2, a1, a0)

        R1 = R_ronbun_H(ronbun_model.q_hs_min_H)
        R2 = R_ronbun_H(ronbun_model.q_hs_rtd_H)
        R3 = R_ronbun_H(ronbun_model.q_hs_max_H)

        _R1, _R2, _R3 = 0.64636, 0.646, 0.56364
        assert math.isclose(_R1, R1, abs_tol=1e-2)
        assert math.isclose(_R2, R2, abs_tol=1e-2)
        assert math.isclose(_R3, R3, abs_tol=1e-2)
