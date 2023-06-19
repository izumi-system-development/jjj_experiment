import math
from jjjexperiment.denchu_1 import *

def simu_R(a2, a1, a0):
    """ 二次関数 R(q) を得る """
    return lambda x: a2*x**2 + a1*x + a0

def simu_P(q: float, COP: float) -> float:
    return q / COP

def simu_COP_C(q: float, Pc: float, R: float, M_ein: float, M_cin: float, cdtn: Condition) -> float:
    """ 推計モデルと実使用条件から COPを推計する """
    def fix_T_evp(q, M_ein, cdtn: Condition):
        """ q [kW] """
        Ca = get_Ca(cdtn.X_ein / 1000)
        T_evp = cdtn.T_ein - q / ((1-BF) * M_ein * Ca)  #★
        return T_evp

    def simu_T_cnd(q, P, M_cin, cdtn: Condition):
        """ q, P [kW] """
        Ca = get_Ca(cdtn.X_cin / 1000)
        T_cnd = cdtn.T_cin + (q+P) / ((1-BF) * M_cin * Ca)  #★
        return T_cnd

    def recalc_COP(q, R, Pc, T_evp, T_cnd) -> float:
        left = R * (T_evp + 273.15) / (T_cnd - T_evp)  #★
        return left * q / (q + Pc * left)

    T_evp = fix_T_evp(q, M_ein, cdtn)  #★
    COP = 5
    while True:
        P = simu_P(q, COP)
        T_cnd = simu_T_cnd(q, P, M_cin, cdtn)
        test_COP = recalc_COP(q, R, Pc, T_evp, T_cnd)

        # FIXME: 精度コントロール
        if math.isclose(test_COP, COP, abs_tol=1e-2):
            break
        else:
            COP = test_COP
    return COP

def simu_COP_H(q: float, Pc: float, R: float, M_ein: float, M_cin: float, cdtn: Condition) -> float:
    """ 推計モデルと実使用条件から COPを推計する """
    def fix_T_cnd(q, M_cin, cdtn: Condition):
        """ q [kW] """
        Ca = get_Ca(cdtn.X_cin / 1000)
        T_cnd = cdtn.T_cin + q / ((1-BF) * M_cin * Ca)  #★
        return T_cnd

    def simu_T_evp(q, P, M_ein, cdtn: Condition):
        """ q, P [kW] """
        Ca = get_Ca(cdtn.X_ein / 1000)
        T_evp = cdtn.T_ein - (q-P) / ((1-BF) * M_ein * Ca)  #★
        return T_evp

    def recalc_COP(q, R, Pc, T_evp, T_cnd) -> float:
        left = R * (T_cnd + 273.15) / (T_cnd - T_evp)  #★
        return left * q / (q + Pc * left)

    T_cnd = fix_T_cnd(q, M_cin, cdtn)  #★
    COP = 5
    while True:
        P = simu_P(q, COP)
        T_evp = simu_T_evp(q, P, M_ein, cdtn)
        test_COP = recalc_COP(q, R, Pc, T_evp, T_cnd)

        # FIXME: 精度コントロール
        if math.isclose(test_COP, COP, abs_tol=1e-2):
            break
        else:
            COP = test_COP
    return COP
