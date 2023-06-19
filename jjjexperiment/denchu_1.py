import typing
import numpy as np

class Spec:
    """ 機器特性(メーカー公表値)をまとめるクラス
    """
    def __init__(self, name,
                P_hs_min_C, P_hs_rtd_C, P_hs_max_C,
                P_hs_min_H, P_hs_rtd_H, P_hs_max_H,
                q_hs_min_C, q_hs_rtd_C, q_hs_max_C,
                q_hs_min_H, q_hs_rtd_H, q_hs_max_H):
        self._name = name
        self._p_hs_min_C, self._p_hs_rtd_C, self._p_hs_max_C = P_hs_min_C, P_hs_rtd_C, P_hs_max_C
        self._p_hs_min_H, self._p_hs_rtd_H, self._p_hs_max_H = P_hs_min_H, P_hs_rtd_H, P_hs_max_H
        self._q_hs_min_C, self._q_hs_rtd_C, self._q_hs_max_C = q_hs_min_C, q_hs_rtd_C, q_hs_max_C
        self._q_hs_min_H, self._q_hs_rtd_H, self._q_hs_max_H = q_hs_min_H, q_hs_rtd_H, q_hs_max_H

    @property
    def name(self):
        """ 機器名 """; return self._name

    @property
    def P_hs_min_C(self):
        """ JIS条件での冷房消費電力(最小)[W] """; return self._p_hs_min_C
    @property
    def P_hs_rtd_C(self):
        """ JIS条件での冷房消費電力(定格)[W] """; return self._p_hs_rtd_C
    @property
    def P_hs_max_C(self):
        """ JIS条件での冷房消費電力(最大)[W] """; return self._p_hs_max_C
    # NOTE: 室内から除去するエネルギーQ[W] = 冷房能力 (論文より)
    @property
    def q_hs_min_C(self):
        """ JIS条件での冷房能力(最小)[kW] """; return self._q_hs_min_C
    @property
    def q_hs_rtd_C(self):
        """ JIS条件での冷房能力(定格)[kW] """; return self._q_hs_rtd_C
    @property
    def q_hs_max_C(self):
        """ JIS条件での冷房能力(最大)[kW] """; return self._q_hs_max_C

    @property
    def P_hs_min_H(self):
        """ JIS条件での暖房消費電力(最小)[W] """; return self._p_hs_min_H
    @property
    def P_hs_rtd_H(self):
        """ JIS条件での暖房消費電力(定格)[W] """; return self._p_hs_rtd_H
    @property
    def P_hs_max_H(self):
        """ JIS条件での暖房消費電力(最大)[W] """; return self._p_hs_max_H
    @property
    def q_hs_min_H(self):
        """ JIS条件での暖房能力(最小)[kW] """; return self._q_hs_min_H
    @property
    def q_hs_rtd_H(self):
        """ JIS条件での暖房能力(定格)[kW] """; return self._q_hs_rtd_H
    @property
    def q_hs_max_H(self):
        """ JIS条件での暖房能力(最大)[kW] """; return self._q_hs_max_H


class Condition():
    """ 冷暖房運転時のエアコンの使用条件をまとめるクラス
    """
    def __init__(self, T_ein, T_cin, X_ein, X_cin, M_ein, M_cin):
        self._T_ein, self._T_cin = T_ein, T_cin
        self._X_ein, self._X_cin = X_ein, X_cin
        self._M_ein, self._M_cin = M_ein, M_cin

    @property
    def T_ein(self):
        """ 室内機の吸込み空気の温度[℃]=室内温度 """; return self._T_ein
    @property
    def T_cin(self):
        """ 室外機の吸込み空気の温度[℃]=室外温度 """; return self._T_cin

    @property
    def X_ein(self):
        """ 室内機の吸込み空気の絶対湿度[g/kgDA] """; return self._X_ein
    @property
    def X_cin(self):
        """ 室外機の吸込み空気の絶対湿度[g/kgDA] """; return self._X_cin

    # NOTE: 論文より, 吸込口に入る空気の量=吹出口から出る空気の量
    @property
    def M_ein(self):
        """ 室内機の吸込み空気の流量[kgDA/s] """; return self._M_ein
    @property
    def M_cin(self):
        """ 室外機の吸込み空気の流量[kgDA/s] """; return self._M_cin

def dry_air_density(temperature: float) -> float:
    """ 気温[℃]毎の乾燥空気の密度[kg/m3]
    """
    # HACK: 気圧を変数化してもよい
    air_pressure = 1013.25  # 一般的な 1気圧 [hpa]
    return air_pressure / (2.87 * (temperature + 273.15))

def absolute_humid(rh: float, t: float):
    """ 気温[℃]毎の相対湿度[%]から、重量絶対湿度[g/kgDA]へ変換
    """
    # 数式参考: https://www.2x6satoru.com/article/ab-humidity.html
    e = 6.1078 * 10 ** (7.5 * t / (t + 237.3)) * (rh / 100)
    return 0.622 * e / (1013.25 - e) * 1000

def m3ph_to_kgDAps(m3ph: float, temperature: float) -> float:
    """ 空気の流量を 体積流量[m3/h] -> 質量流量[kg(DA)/s] 変換する
    """
    rho = dry_air_density(temperature)  # ρ[kg/m3]はよさそう
    return rho * m3ph / 3600  # FIXME: この計算が違う?

def get_Ca(humid_abs: float):
    """ 重量絶対湿度[kg/kg(DA)]から湿り空気の比熱[kJ/kg(DA)*K] を取得
    """
    # 数式参考: https://www.jstage.jst.go.jp/article/jsam1937/37/4/37_4_694/_pdf
    C_g = 1.005
    C_v = 1.8695 * humid_abs  # NOTE: 様々な数字が見られる(1.884...etc)
    return C_g + C_v  # NOTE: 乾き空気の比熱+水蒸気の比熱

def solve_mtx(A: np.matrix, Y: np.matrix) -> typing.Tuple[float, float]:
    mtx_ans = np.linalg.inv(A) * Y  # shape(2, 1)
    return (mtx_ans[0, 0], mtx_ans[1, 0])

def calc_reibai_phase_T_C(q: float, P: float, condi: Condition)-> typing.Tuple[float, float]:
    """ q, P [kW]で統一 """
    BF = 0.2  # NOTE: Bypass-Factor: 論文内では0.2に固定

    M_evp = (1-BF) * condi.M_ein  # M_evp: 熱交換機と接する空気[kgDA/s]
    Ca_ein = get_Ca(condi.X_ein / 1000)  # Ca: 湿り空気比熱[kJ/(kgDA*K)]
    T_evp = condi.T_ein - q / (M_evp*Ca_ein)  # 冷媒蒸発温度[℃]

    M_cnd = (1-BF) * condi.M_cin  # M_cnd: 熱交換機と接する空気[kgDA/s]
    Ca_cin = get_Ca(condi.X_cin / 1000)  # Ca: 湿り空気比熱[kJ/(kgDA*K)]
    T_cnd = condi.T_cin + (q+P) / (M_cnd*Ca_cin)  # 冷媒凝縮温度[℃]

    return T_evp, T_cnd

def calc_R_and_Pc_C(spec: Spec, condi: Condition) -> typing.Tuple[float, float, float, float]:
    """ 成績係数比Rの近似式の係数とファン等消費電力Pc[kW]
    """
    def coeffs_for_simultaneous_C(q:float, P:float, condi: Condition) -> typing.Tuple[float, float, float]:
        """ q, P [kW]で統一 """
        T_evp, T_cnd = calc_reibai_phase_T_C(q, P, condi)
        A = (T_cnd - T_evp) / (T_evp + 273.15)  # 冷房と異なる
        B = 1 / q
        COP = q / P; Y = 1 / COP
        return A, B, Y  # A・R' + B・Pc = Y (R'=1/R) の形にする

    def R_minrtd_C(spec: Spec, condi: Condition) -> typing.Tuple[float, float]:
        A1, B1, Y1 = coeffs_for_simultaneous_C(spec.q_hs_min_C, 0.001*spec.P_hs_min_C, condi)
        A2, B2, Y2 = coeffs_for_simultaneous_C(spec.q_hs_rtd_C, 0.001*spec.P_hs_rtd_C, condi)
        mtx_A, mtx_Y = np.matrix([[A1, B1], [A2, B2]]), np.matrix([[Y1], [Y2]])
        R_minrtd_dash, Pc = solve_mtx(mtx_A, mtx_Y)
        R_minrtd = 1 / R_minrtd_dash  # NOTE: 最小・定格時のR同一
        return R_minrtd, Pc

    R_minrtd, Pc = R_minrtd_C(spec, condi)

    def R_max_C(Pc, q, P, condi: Condition) -> float:
        """ Pc, q, P [kW]で統一 """
        T_evp_max, T_cnd_max = calc_reibai_phase_T_C(q, P, condi)
        COP = q / P
        right = COP * q / (q - COP*Pc)  # (7)式右辺
        left = (T_evp_max + 273.15) / (T_cnd_max - T_evp_max)  # (7)式左辺(係数部)
        return right / left

    # NOTE: 論文より最大時のRのみ別に計算する
    R_max = R_max_C(Pc, spec.q_hs_max_C, 0.001*spec.P_hs_max_C, condi)

    Qs = np.array([spec.q_hs_min_C, spec.q_hs_rtd_C, spec.q_hs_max_C])
    Rs = np.array([R_minrtd, R_minrtd, R_max])
    coeffs = np.polyfit(Qs, Rs, 2)  # 二次式に近似し係数を取得

    R_poly_a2 = coeffs[0]
    R_poly_a1 = coeffs[1]
    R_poly_a0 = coeffs[2]
    return R_poly_a2, R_poly_a1, R_poly_a0, Pc

def calc_reibai_phase_T_H(q: float, P: float, condi: Condition)-> typing.Tuple[float, float]:
    """ q, P [kW]で統一 """
    BF = 0.2  # NOTE: Bypass-Factor: 論文内では0.2に固定

    M_evp = (1-BF) * condi.M_ein  # M_evp: 熱交換機と接する空気[kgDA/s]
    Ca_ein = get_Ca(condi.X_ein / 1000)  # Ca: 湿り空気比熱[kJ/(kgDA*K)]
    T_evp = condi.T_ein - (q-P) / (M_evp*Ca_ein)  # 冷媒蒸発温度[℃]

    M_cnd = (1-BF) * condi.M_cin  # M_cnd: 熱交換機と接する空気[kgDA/s]
    Ca_cin = get_Ca(condi.X_cin / 1000)  # Ca: 湿り空気比熱[kJ/(kgDA*K)]
    T_cnd = condi.T_cin + q / (M_cnd*Ca_cin)  # 冷媒凝縮温度[℃]

    return T_evp, T_cnd

def calc_R_and_Pc_H(spec: Spec, condi: Condition) -> typing.Tuple[float, float, float, float]:
    """ 成績係数比Rの近似式の係数とファン等消費電力Pc[kW]
    """
    def coeffs_for_simultaneous_H(q:float, P:float, condi: Condition) -> typing.Tuple[float, float, float]:
        """ q, P [kW]で統一 """
        T_evp, T_cnd = calc_reibai_phase_T_H(q, P, condi)
        A = (T_cnd - T_evp) / (T_cnd + 273.15)  # 冷房と異なる
        B = 1 / q
        COP = q / P; Y = 1 / COP
        return A, B, Y  # A・R' + B・Pc = Y (R'=1/R) の形にする

    def R_minrtd_H(spec: Spec, condi: Condition) -> typing.Tuple[float, float]:
        A1, B1, Y1 = coeffs_for_simultaneous_H(spec.q_hs_min_H, 0.001*spec.P_hs_min_H, condi)
        A2, B2, Y2 = coeffs_for_simultaneous_H(spec.q_hs_rtd_H, 0.001*spec.P_hs_rtd_H, condi)
        mtx_A, mtx_Y = np.matrix([[A1, B1], [A2, B2]]), np.matrix([[Y1], [Y2]])
        R_minrtd_dash, Pc = solve_mtx(mtx_A, mtx_Y)
        R_minrtd = 1 / R_minrtd_dash  # NOTE: 最小・定格時のR同一
        return R_minrtd, Pc

    R_minrtd, Pc = R_minrtd_H(spec, condi)

    def R_max_H(Pc, q, P, condi: Condition) -> float:
        """ Pc, q, P [kW]で統一 """
        T_evp_max, T_cnd_max = calc_reibai_phase_T_H(q, P, condi)
        COP = q / P
        right = COP * q / (q - COP*Pc)  # (7)式右辺
        left = (T_cnd_max + 273.15) / (T_cnd_max - T_evp_max)  # (7)式左辺(係数部)
        return right / left

    # NOTE: 論文より最大時のRのみ別に計算する
    R_max = R_max_H(Pc, spec.q_hs_max_H, 0.001*spec.P_hs_max_H, condi)

    Qs = np.array([spec.q_hs_min_H, spec.q_hs_rtd_H, spec.q_hs_max_H])
    Rs = np.array([R_minrtd, R_minrtd, R_max])

    coeffs = np.polyfit(Qs, Rs, 2)  # 二次式に近似し係数を取得
    R_poly_a2, R_poly_a1, R_poly_a0 = coeffs[0], coeffs[1], coeffs[2]

    return R_poly_a2, R_poly_a1, R_poly_a0, Pc
