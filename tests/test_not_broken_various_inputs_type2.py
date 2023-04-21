import pytest
import json
import copy

# HACK:カレントディレクトリが jjj_experiment/jjjexperiment で実行時のみ動く
from jjjexperiment.main import calc
from jjjexperiment.result import ResultSummary

class TestNotBrokenVariousInputsType2:
    """ 既存計算が壊れていないことのテスト
        暖房・冷房ともに「ルームエアコンディショナ活用型全館空調」
    """
    def setup_inputs() -> dict:
        inputs: dict = json.load(open('./tests/inputs/default_testinput.json', 'r'))
        inputs['H_A']['type'] = 2
        inputs['C_A']['type'] = 2
        return inputs

    _inputs: dict = setup_inputs()

    _base_output = ResultSummary(
            q_rtd_C = 5600,
            q_rtd_H = 6685.3,
            q_max_C = 5944.619999999999,
            q_max_H = 10047.047813999998,
            e_rtd_C = 2.8512,
            e_rtd_H = 3.855424,
            E_C = 14695.841130521072,
            E_H = 40812.21298826678)

    def test_output_not_changed_base(self):
        """ ベースとしている結果が確かであることを確認
        """
        result = calc(self._inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_H == self._base_output.E_H
        assert result.E_C == self._base_output.E_C

    def test_output_not_changed_01(self):
        """ 入力内容変更時の挙動が壊れていない
            最大暖房出力時の熱源機の出口における空気温度の最大値の上限値
            Theta_hs_out_max_H_d_t_limit
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["Theta_hs_out_max_H_d_t_limit"] = 47.5

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_C == self._base_output.E_C

        assert result.E_H == 40813.23277369657
        assert result.E_H != self._base_output.E_H

    def test_output_not_changed_02(self):
        """ 入力内容変更時の挙動が壊れていない
            最大冷房出力時の熱源機の出口における空気温度の最低値の下限値
            Theta_hs_out_min_C_d_t_limit
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["Theta_hs_out_min_C_d_t_limit"] = 18.2

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_H == self._base_output.E_H

        assert result.E_C != self._base_output.E_C
        assert result.E_C == 14178.967016020626

    def test_output_not_changed_03(self):
        """ 入力内容変更時の挙動が壊れていない
            デフロストに関する暖房出力補正係数（ダクトセントラル空調機）
            C_df_H_d_t_defrost_ductcentral
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["C_df_H_d_t_defrost_ductcentral"] = 0.88

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_C == self._base_output.E_C

        assert result.E_H != self._base_output.E_H
        assert result.E_H == 40379.49973723975

    def test_output_not_changed_04(self):
        """ 入力内容変更時の挙動が壊れていない
            デフロスト発生外気温度（ダクトセントラル空調機）
            defrost_temp_ductcentral
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["defrost_temp_ductcentral"] = 6.2

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_C == self._base_output.E_C

        assert result.E_H == 41330.46136603447
        assert result.E_H != self._base_output.E_H

    def test_output_not_changed_05(self):
        """ 入力内容変更時の挙動が壊れていない
            デフロスト発生外気相対湿度（ダクトセントラル空調機）
            defrost_humid_ductcentral
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["defrost_humid_ductcentral"] = 77

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_C == self._base_output.E_C

        assert result.E_H == 41565.19129722995
        assert result.E_H != self._base_output.E_H

    def test_output_not_changed_06(self):
        """ 入力内容変更時の挙動が壊れていない
            ダクトiの線熱損失係数
            phi_i
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["phi_i"] = 0.52

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H

        assert result.E_H == 41236.578091305644
        assert result.E_H != self._base_output.E_H
        assert result.E_C == 14785.070861211718
        assert result.E_C != self._base_output.E_C

    def test_output_not_changed_07(self):
        """ 入力内容変更時の挙動が壊れていない
            暖房時の送風機の設計風量に関する係数
            C_V_fan_dsgn_H
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["C_V_fan_dsgn_H"] = 0.82

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_C == self._base_output.E_C

        assert result.E_H == 40775.15329048871
        assert result.E_H != self._base_output.E_H

    def test_output_not_changed_08(self):
        """ 入力内容変更時の挙動が壊れていない
            冷房時の送風機の設計風量に関する係数
            C_V_fan_dsgn_C
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["C_V_fan_dsgn_C"] = 0.81

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_H == self._base_output.E_H

        assert result.E_C == 14788.362569150617
        assert result.E_C != self._base_output.E_C

    def test_output_not_changed_09(self):
        """ 入力内容変更時の挙動が壊れていない
            デフロストに関する暖房出力補正係数（ルームエアコンディショナー）
            C_df_H_d_t_defrost_rac
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["C_df_H_d_t_defrost_rac"] = 0.88

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_C == self._base_output.E_C

        assert result.E_H != self._base_output.E_H
        assert result.E_H == 40228.03332635408

    def test_output_not_changed_10(self):
        """ 入力内容変更時の挙動が壊れていない
            デフロスト発生外気温度（ルームエアコンディショナー）
            defrost_temp_rac
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["defrost_temp_rac"] = 5.2

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_C == self._base_output.E_C

        assert result.E_H != self._base_output.E_H
        assert result.E_H == 40925.918843796484

    def test_output_not_changed_11(self):
        """ 入力内容変更時の挙動が壊れていない
            デフロスト発生外気相対湿度（ルームエアコンディショナー）
            defrost_humid_rac
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["defrost_humid_rac"] = 82

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_C == self._base_output.E_C

        assert result.E_H != self._base_output.E_H
        assert result.E_H == 40481.81864211065

    def test_output_not_changed_12(self):
        """ 入力内容変更時の挙動が壊れていない
            室内機吸い込み湿度に関する冷房出力補正係数
            C_hm_C
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["C_hm_C"] = 1.32

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_H == self._base_output.E_H

        assert result.E_C != self._base_output.E_C
        assert result.E_C == 12824.79767377771

    def test_output_not_changed_13(self):
        """ 入力内容変更時の挙動が壊れていない
            定格冷房能力の最大値
            q_rtd_C_limit
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["q_rtd_C_limit"] = 3500

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H

        assert result.E_C != self._base_output.E_C
        assert result.E_C == 17002.04875326623
        assert result.E_H != self._base_output.E_H
        assert result.E_H == 43487.16595274875

    def test_output_not_changed_14(self):
        """ 入力内容変更時の挙動が壊れていない
            面積の合計 [m2]
            A_A
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["A_A"] = 135.92

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H

        assert result.E_H == 40822.38807655774
        assert result.E_H != self._base_output.E_H
        assert result.E_C == 14184.472397667007
        assert result.E_C != self._base_output.E_C

    def test_output_not_changed_15(self):
        """ 入力内容変更時の挙動が壊れていない
            主たる居室の面積 [m2]
            A_MR
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["A_MR"] = 68.29

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H

        assert result.E_H != self._base_output.E_H
        assert result.E_H == 47702.33872845253
        assert result.E_C != self._base_output.E_C
        assert result.E_C == 22378.09180122358

    def test_output_not_changed_16(self):
        """ 入力内容変更時の挙動が壊れていない
            その他の居室の面積[m2]
            A_OR
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["A_OR"] = 123.456

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H

        assert result.E_H != self._base_output.E_H
        assert result.E_H == 58567.764449747614
        assert result.E_C != self._base_output.E_C
        assert result.E_C == 25009.231072133218

    def test_output_not_changed_17(self):
        """ 入力内容変更時の挙動が壊れていない
            地域区分
            region
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["region"] = 1

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H

        assert result.E_H == 174560.6036239345
        assert result.E_H != self._base_output.E_H
        assert result.E_C == 2884.2632006293015
        assert result.E_C != self._base_output.E_C

    def test_output_not_changed_18(self):
        """ 入力内容変更時の挙動が壊れていない
            外皮面積 [m2]
            A_env
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["A_env"] = 333.332

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H

        assert result.E_H != self._base_output.E_H
        assert result.E_H == 45819.9093469388
        assert result.E_C != self._base_output.E_C
        assert result.E_C == 15119.878587850431

    def test_output_not_changed_19(self):
        """ 入力内容変更時の挙動が壊れていない
            外皮平均熱貫流率 UA [W/(m2・K)]
            U_A
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["U_A"] = 1.03

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H

        assert result.E_H != self._base_output.E_H
        assert result.E_H == 51145.64313095035
        assert result.E_C != self._base_output.E_C
        assert result.E_C == 14057.66109771598

    def test_output_not_changed_20(self):
        """ 入力内容変更時の挙動が壊れていない
            冷房期平均日射熱取得率ηAC
            eta_A_C
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["eta_A_C"] = 3.3

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_H == self._base_output.E_H

        assert result.E_C == 16690.55292080024
        assert result.E_C != self._base_output.E_C

    def test_output_not_changed_21(self):
        """ 入力内容変更時の挙動が壊れていない
            暖房期平均日射熱取得率ηAH
            eta_A_H
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["eta_A_H"] = 3.9

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_C == self._base_output.E_C

        assert result.E_H == 43202.66151700742
        assert result.E_H != self._base_output.E_H

    def test_output_not_changed_22(self):
        """ 入力内容変更時の挙動が壊れていない
            床下空間を経由して外気を導入する換気方式の利用 （☐：評価しない or ☑：評価する）
            underfloor_ventilation
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["underfloor_ventilation"] = "2"

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H

        assert result.E_H == 38306.56455225713
        assert result.E_H != self._base_output.E_H
        assert result.E_C == 12647.872661178222
        assert result.E_C != self._base_output.E_C

    def test_output_not_changed_23(self):
        """ 入力内容変更時の挙動が壊れていない
            外気が経由する床下の面積の割合 [%]
            r_A_ufvnt
        """
        inputs = copy.deepcopy(self._inputs)
        # WARNING: 値変更しても変わらないけど大丈夫? 100 -> 85.0
        inputs["r_A_ufvnt"] = 85.0

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_H == self._base_output.E_H
        assert result.E_C == self._base_output.E_C

    def test_output_not_changed_24(self):
        """ 入力内容変更時の挙動が壊れていない
            床下空間の断熱 （☐：断熱区画外 or ☑：断熱区画内）
            underfloor_insulation
        """
        inputs = copy.deepcopy(self._inputs)
        # WARNING: 値変更しても変わらないけど大丈夫? '1' -> '2'
        inputs["underfloor_insulation"] = '2'

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_H == self._base_output.E_H
        assert result.E_C == self._base_output.E_C

    def test_output_not_changed_25(self):
        """ 入力内容変更時の挙動が壊れていない
            空調空気を床下を通して給気する （☐：床下を通して給気しない or ☑：床下を通して給気する）
            underfloor_air_conditioning_air_supply
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["underfloor_air_conditioning_air_supply"] = "2"

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H

        assert result.E_H != self._base_output.E_H
        assert result.E_H == 67493.42767621638
        assert result.E_C != self._base_output.E_C
        assert result.E_C == 18872.3162663047

    def test_output_not_changed_26(self):
        """ 入力内容変更時の挙動が壊れていない
            地盤またはそれを覆う基礎の表面熱伝達抵抗 [(m2・K)/W]
            R_g
        """
        inputs = copy.deepcopy(self._inputs)
        # WARNING: 値変更しても変わらないけど大丈夫? 0.15 -> 0.19
        inputs["R_g"] = 0.19

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_H == self._base_output.E_H
        assert result.E_C == self._base_output.E_C

    def test_output_not_changed_27(self):
        """ 入力内容変更時の挙動が壊れていない
            全体風量を固定する （☐：固定しない or ☑：固定する）
            hs_CAV
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["hs_CAV"] = "2"

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_C == self._base_output.E_C

        assert result.E_H == 41606.24726343731
        assert result.E_H != self._base_output.E_H

    def test_output_not_changed_H1(self):
        """ 入力内容変更時の挙動が壊れていない
            ダクトが通過する空間 （全てもしくは一部が断熱区画外である or 全て断熱区画内である）
            H_A_duct_insulation
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["H_A"]["duct_insulation"] = 2

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_C == self._base_output.E_C

        assert result.E_H == 38430.15407789486
        assert result.E_H != self._base_output.E_H

    def test_output_not_changed_H2(self):
        """ 入力内容変更時の挙動が壊れていない
            VAV方式 （採用しない or 採用する）
            H_A_VAV
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["H_A"]["VAV"] = 2

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_C == self._base_output.E_C

        assert result.E_H == 39572.83185804524
        assert result.E_H != self._base_output.E_H

    def test_output_not_changed_H3(self):
        """ 入力内容変更時の挙動が壊れていない
            全般換気機能 （あり or なし）
            H_A_general_ventilation
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["H_A"]["general_ventilation"] = 2

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_C == self._base_output.E_C

        assert result.E_H == 41467.93507466678
        assert result.E_H != self._base_output.E_H

    def test_output_not_changed_H4(self):
        """ 入力内容変更時の挙動が壊れていない
            設計風量 [m3/h]（入力する場合のみ）
            H_A_V_hs_dsgn_H
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["H_A"]["input_V_hs_dsgn_H"] = 2
        inputs["H_A"]["V_hs_dsgn_H"] = 1820

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_C == self._base_output.E_C

        assert result.E_H == 40896.18678654383
        assert result.E_H != self._base_output.E_H

    def test_output_not_changed_type2_H1(self):
        """ 入力内容変更時の挙動が壊れていない
            暖房の機器仕様を入力する1
        """
        inputs = copy.deepcopy(self._inputs)

        # 暖房能力の入力（面積から能力を算出 or 性能を直接入力）
        inputs["H_A"]["input_rac_performance"] = 1  # ★ 面積から能力を算出
        # ▼ 入力する場合
        inputs["H_A"]["q_rac_rtd_H"] = 1  # 暖房定格能力 [W]
        inputs["H_A"]["q_rac_max_H"] = 1  # 暖房最大能力 [W]
        inputs["H_A"]["e_rac_rtd_H"] = 1  # 定格エネルギー効率 [-]

        # 小能力時高効率型コンプレッサー（評価しない or 搭載する）
        inputs["H_A"]["dualcompressor"] = 2

        # 設置方法の入力（設置方法を入力する or 補正係数を直接入力する）
        inputs["H_A"]["input_C_af_H"] = 1
        # ▼ 入力する場合
        inputs["H_A"]["C_af_H"] = 1  # 室内機吹き出し風量に関する暖房出力補正係数の入力

        # 専用チャンバーに格納される方式（該当しない or 該当する）
        inputs["H_A"]["dedicated_chamber"] = 2
        # フィン向きが中央位置に固定される方式（該当しない or 該当する）
        inputs["H_A"]["fixed_fin_direction"] = 2

        # ファンの比消費電力（入力しない or 入力する）
        inputs["H_A"]["input_f_SFP_H"] = 1
        # ▼ 入力する場合
        inputs["H_A"]["f_SFP_H"] = 1  # ファンの比消費電力 [W/(m3/h)]

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_C == self._base_output.E_C

        assert result.E_H == 31577.30541426199
        assert result.E_H != self._base_output.E_H

    def test_output_not_changed_type2_H2(self):
        """ 入力内容変更時の挙動が壊れていない
            暖房の機器仕様を入力する1
        """
        inputs = copy.deepcopy(self._inputs)

        # 暖房能力の入力（面積から能力を算出 or 性能を直接入力）
        inputs["H_A"]["input_rac_performance"] = 2  # ★ 性能を直接入力
        # ▼ 入力する場合のみ
        inputs["H_A"]["q_rac_rtd_H"] = 3600  # 暖房定格能力 [W]
        inputs["H_A"]["q_rac_max_H"] = 4700  # 暖房最大能力 [W]
        inputs["H_A"]["e_rac_rtd_H"] = 3.93  # 定格エネルギー効率 [-]

        # 小能力時高効率型コンプレッサー（評価しない or 搭載する）
        inputs["H_A"]["dualcompressor"] = 1

        # 設置方法の入力（設置方法を入力する or 補正係数を直接入力する）
        inputs["H_A"]["input_C_af_H"] = 2  # ★ 補正係数を直接入力する
        # ▼ 入力する場合のみ
        inputs["H_A"]["C_af_H"] = 0.914  # 室内機吹き出し風量に関する暖房出力補正係数の入力

        # 専用チャンバーに格納される方式（該当しない or 該当する）
        inputs["H_A"]["dedicated_chamber"] = 1
        # フィン向きが中央位置に固定される方式（該当しない or 該当する）
        inputs["H_A"]["fixed_fin_direction"] = 1

        # ファンの比消費電力（入力しない or 入力する）
        inputs["H_A"]["input_f_SFP_H"] = 2  # ★ 入力する
        # ▼ 入力する場合のみ
        inputs["H_A"]["f_SFP_H"] = 0.3  # ファンの比消費電力 [W/(m3/h)]

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_max_C == self._base_output.q_max_C
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.E_C == self._base_output.E_C

        assert result.q_rtd_H == 3600.0
        assert result.q_max_H == 4700.0
        assert result.e_rtd_H == 3.93
        assert result.E_H == 40540.29726496144

    def test_output_not_changed_R1(self):
        """ 入力内容変更時の挙動が壊れていない
            ダクトが通過する空間（全てもしくは一部が断熱区画外である or 全て断熱区画内である）
            C_A_duct_insulation
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["C_A"]["duct_insulation"] = 2

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_H == self._base_output.E_H

        assert result.E_C == 14407.53084233618
        assert result.E_C != self._base_output.E_C

    def test_output_not_changed_R2(self):
        """ 入力内容変更時の挙動が壊れていない
            VAV方式 (採用しない or 採用する）
            C_A_VAV
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["C_A"]["VAV"] = 2

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_H == self._base_output.E_H

        assert result.E_C == 12126.41287275799
        assert result.E_C != self._base_output.E_C

    def test_output_not_changed_R3(self):
        """ 入力内容変更時の挙動が壊れていない
            全般換気機能（あり or なし）
            C_A_general_ventilation
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["C_A"]["general_ventilation"] = 2

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_H == self._base_output.E_H

        assert result.E_C == 15141.75913372107
        assert result.E_C != self._base_output.E_C

    def test_output_not_changed_R4(self):
        """ 入力内容変更時の挙動が壊れていない
            設計風量 [m3/h]（入力する場合のみ）
            C_A_V_hs_dsgn_C
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["C_A"]["input_V_hs_dsgn_C"] = 2
        inputs["C_A"]["V_hs_dsgn_C"] = 1650

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_H == self._base_output.E_H

        assert result.E_C == 16296.897277400154
        assert result.E_C != self._base_output.E_C

    def test_output_not_changed_type2_R1(self):
        """ 入力内容変更時の挙動が壊れていない
            冷房の機器仕様を入力する1
        """
        inputs = copy.deepcopy(self._inputs)

        # 冷房能力の入力（面積から能力を算出 or 性能を直接入力）
        inputs["C_A"]["input_rac_performance"] = 1  # ★ 面積から能力を算出
        # ▼ 入力する場合のみ
        # inputs["C_A"]["q_rac_rtd_C"] = 1  # 冷房定格能力 [W]
        # inputs["C_A"]["q_rac_max_C"] = 1  # 冷房最大能力 [W]
        # inputs["C_A"]["e_rac_rtd_C"] = 1  # 定格エネルギー効率 [-]

        # 小能力時高効率型コンプレッサー（評価しない or 搭載する）
        inputs["C_A"]["dualcompressor"] = 2

        # 設置方法の入力（設置方法を入力する or 補正係数を直接入力する）
        inputs["C_A"]["input_C_af_C"] = 1  # ★ 設置方法を入力する
        # ▼ 入力する場合のみ
        # inputs["C_A"]["C_af_C"] = 1  # 室内機吹き出し風量に関する暖房出力補正係数の入力

        # 専用チャンバーに格納される方式（該当しない or 該当する）
        inputs["C_A"]["dedicated_chamber"] = 2
        # フィン向きが中央位置に固定される方式（該当しない or 該当する）
        inputs["C_A"]["fixed_fin_direction"] = 2

        # ファンの比消費電力（入力しない or 入力する）
        inputs["C_A"]["input_f_SFP_C"] = 1  # ★ 入力しない
        # ▼ 入力する場合のみ
        # inputs["C_A"]["f_SFP_C"] = 1  # ファンの比消費電力W [(m3/h)/W]

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H

        assert result.E_C != self._base_output.E_C
        assert result.E_C == 14046.978599922277

    def test_output_not_changed_type2_R2(self):
        """ 入力内容変更時の挙動が壊れていない
            冷房の機器仕様を入力する2
        """
        inputs = copy.deepcopy(self._inputs)

        # 冷房能力の入力（面積から能力を算出 or 性能を直接入力）
        inputs["C_A"]["input_rac_performance"] = 2  # ★ 面積から能力を算出
        # ▼ 入力する場合のみ
        inputs["C_A"]["q_rac_rtd_C"] = 2800  # 冷房定格能力 [W]
        inputs["C_A"]["q_rac_max_C"] = 3400  # 冷房最大能力 [W]
        inputs["C_A"]["e_rac_rtd_C"] = 2.59  # 定格エネルギー効率 [-]

        # 小能力時高効率型コンプレッサー（評価しない or 搭載する）
        inputs["C_A"]["dualcompressor"] = 1

        # 設置方法の入力（設置方法を入力する or 補正係数を直接入力する）
        inputs["C_A"]["input_C_af_C"] = 2  # ★ 補正係数を直接入力する
        # ▼ 入力する場合のみ
        inputs["C_A"]["C_af_C"] = 0.980  # 室内機吹き出し風量に関する冷房出力補正係数の入力

        # 専用チャンバーに格納される方式（該当しない or 該当する）
        inputs["C_A"]["dedicated_chamber"] = 1
        # フィン向きが中央位置に固定される方式（該当しない or 該当する）
        inputs["C_A"]["fixed_fin_direction"] = 1

        # ファンの比消費電力（入力しない or 入力する）
        inputs["C_A"]["input_f_SFP_C"] = 2  # ★ 入力する
        # ▼ 入力する場合のみ
        inputs["C_A"]["f_SFP_C"] = 0.3  # ファンの比消費電力W [(m3/h)/W]

        result = calc(inputs, test_mode=True)

        # WARNING: 暖房についても結果が変わるのは大丈夫?
        assert result.q_rtd_C == 2800.0
        assert result.q_rtd_H == 3300.1000000000004
        assert result.q_max_C == 3400.0
        assert result.q_max_H == 5569.280000000001
        assert result.e_rtd_C == 2.59
        assert result.e_rtd_H == 3.6543
        assert result.E_C == 21336.043883848488
        assert result.E_H == 46940.16551587674

    def test_output_not_changed_HEX1(self):
        """ 入力内容変更時の挙動が壊れていない
            温度交換効率（設置する場合のみ）
            etr_t
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["HEX"]["install"] = 2
        inputs["HEX"]["etr_t"] = 0.3

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._base_output.q_rtd_C
        assert result.q_rtd_H == self._base_output.q_rtd_H
        assert result.q_max_C == self._base_output.q_max_C
        assert result.q_max_H == self._base_output.q_max_H
        assert result.e_rtd_C == self._base_output.e_rtd_C
        assert result.e_rtd_H == self._base_output.e_rtd_H
        assert result.E_C == self._base_output.E_C

        assert result.E_H == 38022.75810040755
        assert result.E_H != self._base_output.E_H

