import math
from jjjexperiment.denchu_1 import *

def simu_R(a2, a1, a0):
    return lambda x: a2*x**2 + a1*x + a0

def simu_P(q: float, COP: float) -> float:
    return q / COP

def simu_COP_C(q: float, Pc: float, R: float, cdtn: Condition) -> float:
    """ COPを再計算
    """
    def fix_T_evp(q: float, cdtn: Condition):
        """ q [kW] """
        Ca = get_Ca(cdtn.X_ein / 1000)
        T_evp = cdtn.T_ein - q / (0.8 * cdtn.M_ein * Ca)  #★
        return T_evp

    def simu_T_cnd(q: float, P: float, cdtn: Condition):
        """ q, P [kW] """
        Ca = get_Ca(cdtn.X_cin / 1000)
        T_cnd = cdtn.T_cin + (q+P) / (0.8 * cdtn.M_cin * Ca)  #★
        return T_cnd

    def recalc_COP(q, R, Pc, T_evp, T_cnd) -> float:
        left = R * (T_evp + 273.15) / (T_cnd - T_evp)  #★
        return left * q / (q + Pc * left)

    T_evp = fix_T_evp(q, cdtn)  #★
    COP = 5
    while True:
        P = simu_P(q, COP)
        T_cnd = simu_T_cnd(q, P, cdtn)
        test_COP = recalc_COP(q, R, Pc, T_evp, T_cnd)
        if math.isclose(test_COP, COP, abs_tol=1e-2):
            break
        else:
            COP = test_COP
    return COP

def simu_COP_H(q: float, Pc: float, R: float, cdtn: Condition) -> float:
    """ COPを再計算
    """
    def fix_T_cnd(q: float, cdtn: Condition):
        """ q [kW] """
        Ca = get_Ca(cdtn.X_cin / 1000)
        T_cnd = cdtn.T_cin + q / (0.8 * cdtn.M_cin * Ca)  #★
        return T_cnd

    def simu_T_evp(q: float, P: float, cdtn: Condition):
        """ q, P [kW] """
        Ca = get_Ca(cdtn.X_ein / 1000)
        T_evp = cdtn.T_ein - (q-P) / (0.8 * cdtn.M_ein * Ca)  #★
        return T_evp

    def recalc_COP(q, R, Pc, T_evp, T_cnd) -> float:
        left = R * (T_cnd + 273.15) / (T_cnd - T_evp)  #★
        return left * q / (q + Pc * left)

    T_cnd = fix_T_cnd(q, cdtn)  #★
    COP = 5
    while True:
        P = simu_P(q, COP)
        T_evp = simu_T_evp(q, P, cdtn)
        test_COP = recalc_COP(q, R, Pc, T_evp, T_cnd)
        if math.isclose(test_COP, COP, abs_tol=1e-2):
            break
        else:
            COP = test_COP
    return COP
