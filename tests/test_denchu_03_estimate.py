import pytest
import math

from jjjexperiment.denchu_1 import *
from jjjexperiment.denchu_2 import *

R_ronbun_C = simu_R(-0.018, 0.052, 0.513)
Pc_ronbun_C = 0.0361  # kW

R_ronbun_H = simu_R(-0.006, 0.019, 0.636)
Pc_ronbun_H = 0.0303  # kW
# TODO: 暖房時のCOP推計のテストがありません

""" AFTER_R_&_Pc_Modeled """

class Test_COP推計_室内温度固定_外気温25:
    """ 論文掲載グラフと同一条件で整合するか確認
        室内温度を固定し、冷房負荷を変化させて COP の変化を見る
    """
    @classmethod
    def setup_class(cls):
        t_ein = 27  # JIS利用条件
        t_cin = 25  # {25, 30, 35} から選択
        cls._cdtn = Condition(
            T_ein = t_ein,
            T_cin = t_cin,
            X_ein = absolute_humid(47.1, t_ein),  # 論文より
            X_cin = absolute_humid(40.5, t_cin),  # 論文より
            M_ein = m3ph_to_kgDAps(12.1 * 60, t_ein),  # NOTE: [m3/min]->[m3/h]
            M_cin = m3ph_to_kgDAps(28.2 * 60, t_cin),
        )

    def test_05(self):
        q = 0.5; COP = simu_COP_C(q, Pc_ronbun_C, R_ronbun_C(q), self._cdtn)
        assert math.isclose(COP, 12.0, abs_tol=1e-1), "論文掲載値と不整合"
    def test_10(self):
        q = 1.0; COP = simu_COP_C(q, Pc_ronbun_C, R_ronbun_C(q), self._cdtn)
        assert math.isclose(COP, 14.0, abs_tol=1e-1), "論文掲載値と不整合"
    def test_16(self):
        q = 1.6; COP = simu_COP_C(q, Pc_ronbun_C, R_ronbun_C(q), self._cdtn)
        assert math.isclose(COP, 12.0, abs_tol=1e-1), "論文掲載値と不整合"
    def test_20(self):
        q = 2.0; COP = simu_COP_C(q, Pc_ronbun_C, R_ronbun_C(q), self._cdtn)
        assert math.isclose(COP, 10.0, abs_tol=1e-1), "論文掲載値と不整合"
    def test_25(self):
        q = 2.5; COP = simu_COP_C(q, Pc_ronbun_C, R_ronbun_C(q), self._cdtn)
        assert math.isclose(COP, 8.0, abs_tol=1e-1), "論文掲載値と不整合"


class Test_COP推計_室内温度固定_外気温30:
    """ 論文掲載グラフと同一条件で整合するか確認
        室内温度を固定し、冷房負荷を変化させて COP の変化を見る
    """
    @classmethod
    def setup_class(cls):
        t_ein = 27  # JIS利用条件
        t_cin = 30  # {25, 30, 35} から選択
        cls._cdtn = Condition(
            T_ein = t_ein,
            T_cin = t_cin,
            X_ein = absolute_humid(47.1, t_ein),  # 利用時想定
            X_cin = absolute_humid(40.5, t_cin),  # 利用時想定
            M_ein = m3ph_to_kgDAps(12.1 * 60, t_ein),  # NOTE: [m3/min]->[m3/h]
            M_cin = m3ph_to_kgDAps(28.2 * 60, t_cin),
        )

    def test_05(self):
        q = 0.5; COP = simu_COP_C(q, Pc_ronbun_C, R_ronbun_C(q), self._cdtn)
        assert math.isclose(COP, 8.0, abs_tol=1e-1), "論文掲載値と不整合"
    def test_10(self):
        q = 1.0; COP = simu_COP_C(q, Pc_ronbun_C, R_ronbun_C(q), self._cdtn)
        assert math.isclose(COP, 10.0, abs_tol=1e-1), "論文掲載値と不整合"
    def test_18(self):
        q = 1.8; COP = simu_COP_C(q, Pc_ronbun_C, R_ronbun_C(q), self._cdtn)
        assert math.isclose(COP, 8.0, abs_tol=1e-1), "論文掲載値と不整合"
    def test_27(self):
        q = 2.7; COP = simu_COP_C(q, Pc_ronbun_C, R_ronbun_C(q), self._cdtn)
        assert math.isclose(COP, 6.0, abs_tol=1e-1), "論文掲載値と不整合"

class Test_COP推計_室内温度固定_外気温35:
    """ 論文掲載グラフと同一条件で整合するか確認
        室内温度を固定し、冷房負荷を変化させて COP の変化を見る
    """
    @classmethod
    def setup_class(cls):
        t_ein = 27  # JIS利用条件
        t_cin = 35  # {25, 30, 35} から選択
        cls._cdtn = Condition(
            T_ein = t_ein,
            T_cin = t_cin,
            X_ein = absolute_humid(47.1, t_ein),  # 利用時想定
            X_cin = absolute_humid(40.5, t_cin),  # 利用時想定
            M_ein = m3ph_to_kgDAps(12.1 * 60, t_ein),  # NOTE: [m3/min]->[m3/h]
            M_cin = m3ph_to_kgDAps(28.2 * 60, t_cin),
        )

    def test_04(self):
        q = 0.4; COP = simu_COP_C(q, Pc_ronbun_C, R_ronbun_C(q), self._cdtn)
        assert math.isclose(COP, 6.0, abs_tol=1e-1), "論文掲載値と不整合"
    def test_14(self):
        q = 1.4; COP = simu_COP_C(q, Pc_ronbun_C, R_ronbun_C(q), self._cdtn)
        assert math.isclose(COP, 7.0, abs_tol=1e-1), "論文掲載値と不整合"
    def test_20(self):
        q = 2.0; COP = simu_COP_C(q, Pc_ronbun_C, R_ronbun_C(q), self._cdtn)
        assert math.isclose(COP, 6.0, abs_tol=1e-1), "論文掲載値と不整合"
    def test_27(self):
        q = 2.7; COP = simu_COP_C(q, Pc_ronbun_C, R_ronbun_C(q), self._cdtn)
        assert math.isclose(COP, 5.0, abs_tol=1e-1), "論文掲載値と不整合"
    def test_33(self):
        q = 3.3; COP = simu_COP_C(q, Pc_ronbun_C, R_ronbun_C(q), self._cdtn)
        assert math.isclose(COP, 4.0, abs_tol=1e-1), "論文掲載値と不整合"


def cdtn_factory(t_ein: float, t_cin: float) -> Condition:
    """ 論文内で検証している使用条件をベースに一部変数化したもの
    """
    return Condition(
        T_ein = t_ein,
        T_cin = t_cin,
        X_ein = absolute_humid(47.1, t_ein),  # 論文より
        X_cin = absolute_humid(40.5, t_cin),  # 論文より
        # NOTE: [m3/min] -> [m3/h]
        M_ein = m3ph_to_kgDAps(12.1 * 60, t_ein),
        M_cin = m3ph_to_kgDAps(28.2 * 60, t_cin),
    )

class Test_COP推計_冷房能力固定_外気温25:
    """ 論文掲載グラフと同一条件で整合するか確認
        冷房負荷を固定し、室内温度を変化させて COP の変化を見る
    """
    _q = 2.2  # 論文より固定(kW)
    _R = R_ronbun_C(_q)
    _t_cin = 25  # 外気温 {25, 30, 35}

    def test_T_cin_19(self):
        cdtn = cdtn_factory(19, self._t_cin)
        COP = simu_COP_C(self._q, Pc_ronbun_C, self._R, cdtn)
        assert math.isclose(COP, 6.0, abs_tol=1e-1), "論文掲載値と不整合"
    def test_T_cin_25(self):
        cdtn = cdtn_factory(25, self._t_cin)
        COP = simu_COP_C(self._q, Pc_ronbun_C, self._R, cdtn)
        assert math.isclose(COP, 8.0, abs_tol=1e-1), "論文掲載値と不整合"
    def test_T_cin_29(self):
        cdtn = cdtn_factory(29, self._t_cin)
        COP = simu_COP_C(self._q, Pc_ronbun_C, self._R, cdtn)
        assert math.isclose(COP, 10.0, abs_tol=1e-1), "論文掲載値と不整合"

class Test_COP推計_冷房能力固定_外気温30:
    """ 論文掲載グラフと同一条件で整合するか確認
        冷房負荷を固定し、室内温度を変化させて COP の変化を見る
    """
    _q = 2.2  # 論文より固定(kW)
    _R = R_ronbun_C(_q)
    _t_cin = 30  # 外気温 {25, 30, 35}

    def test_T_cin_19(self):
        cdtn = cdtn_factory(19, self._t_cin)
        COP = simu_COP_C(self._q, Pc_ronbun_C, self._R, cdtn)
        assert math.isclose(COP, 5.0, abs_tol=1e-1), "論文掲載値と不整合"
    def test_T_cin_24(self):
        cdtn = cdtn_factory(24, self._t_cin)
        COP = simu_COP_C(self._q, Pc_ronbun_C, self._R, cdtn)
        assert math.isclose(COP, 6.0, abs_tol=1e-1), "論文掲載値と不整合"
    def test_T_cin_27(self):
        cdtn = cdtn_factory(27, self._t_cin)
        COP = simu_COP_C(self._q, Pc_ronbun_C, self._R, cdtn)
        assert math.isclose(COP, 7.0, abs_tol=1e-1), "論文掲載値と不整合"
    def test_T_cin_30(self):
        cdtn = cdtn_factory(30, self._t_cin)
        COP = simu_COP_C(self._q, Pc_ronbun_C, self._R, cdtn)
        assert math.isclose(COP, 8.0, abs_tol=1e-1), "論文掲載値と不整合"

class Test_COP推計_冷房能力固定_外気温35:
    """ 論文掲載グラフと同一条件で整合するか確認
        冷房負荷を固定し、室内温度を変化させて COP の変化を見る
    """
    _q = 2.2  # 論文より固定(kW)
    _R = R_ronbun_C(_q)
    _t_cin = 35  # 外気温 {25, 30, 35}

    def test_T_cin_17(self):
        cdtn = cdtn_factory(17, self._t_cin)
        COP = simu_COP_C(self._q, Pc_ronbun_C, self._R, cdtn)
        assert math.isclose(COP, 4.0, abs_tol=1e-1), "論文掲載値と不整合"
    def test_T_cin_24(self):
        cdtn = cdtn_factory(24, self._t_cin)
        COP = simu_COP_C(self._q, Pc_ronbun_C, self._R, cdtn)
        assert math.isclose(COP, 5.0, abs_tol=1e-1), "論文掲載値と不整合"
    def test_T_cin_29(self):
        cdtn = cdtn_factory(29, self._t_cin)
        COP = simu_COP_C(self._q, Pc_ronbun_C, self._R, cdtn)
        assert math.isclose(COP, 6.0, abs_tol=1e-1), "論文掲載値と不整合"

""" 論文外の機器データで試す """
# TODO: 未作成のテストです

t_ein = 27  # JIS利用条件より
t_cin = 35  # JIS利用条件より

urusara_x = Spec(
    # 機器仕様より https://www.ac.daikin.co.jp/roomaircon/products/r_series
    name = "DAIKIN Rシリーズ うるさらX AN563ARP-W",
    P_hs_min_C = 85,
    P_hs_rtd_C = 1500,
    P_hs_max_C = 1620,
    q_hs_min_C = 0.5,
    q_hs_rtd_C = 5.6,
    q_hs_max_C = 6.0,

    P_hs_min_H = None,
    P_hs_rtd_H = None,
    P_hs_max_H = None,
    q_hs_min_H = None,
    q_hs_rtd_H = None,
    q_hs_max_H = None,
    )

cdtn = Condition(
    # https://www.ac.daikin.co.jp/roomaircon/products/r_series
    T_ein = t_ein,
    T_cin = t_cin,
    X_ein = absolute_humid(60, t_ein),
    X_cin = absolute_humid(80, t_cin),
    M_ein = m3ph_to_kgDAps(35.0, t_ein),  # NOTE: 強風量 https://www.ac.daikin.co.jp/roomaircon/products/r_series
    M_cin = m3ph_to_kgDAps(70.0, t_cin),  # FIXME: カタログにないため仮定値(室内機の倍近くあることが多い?)
    )
