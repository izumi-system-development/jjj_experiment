import pytest
import json
import copy

from jjjexperiment.main import calc

from test_utils.expects import  \
    expected_result_type1, expected_result_type2, expected_inputs

class Test既存計算維持_デフォルト入力時:

    _inputs: dict = json.load(open('./tests/inputs/default_testinput.json', 'r'))

    def test_インプットデータ_前提確認(self, expected_inputs):
        """ テストコードが想定しているインプットデータかどうか確認
        """
        result = calc(self._inputs, test_mode=True)

        assert result['TInput'].q_rtd_C == expected_inputs.q_rtd_C
        assert result['TInput'].q_rtd_H == expected_inputs.q_rtd_H
        assert result['TInput'].q_max_C == expected_inputs.q_max_C
        assert result['TInput'].q_max_H == expected_inputs.q_max_H
        assert result['TInput'].e_rtd_C == expected_inputs.e_rtd_C
        assert result['TInput'].e_rtd_H == expected_inputs.e_rtd_H

    def test_計算結果一致_方式1(self, expected_result_type1):
        """ ipynbのサンプル入力で計算結果が意図しない変化がないことを確認
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["H_A"]["type"] = 1
        inputs["C_A"]["type"] = 1

        result = calc(inputs, test_mode=True)

        assert result['TValue'].E_C == expected_result_type1.E_C
        assert result['TValue'].E_H == expected_result_type1.E_H

    def test_計算結果一致_方式2(self, expected_result_type2):
        """ ipynbのサンプル入力で計算結果が意図しない変化がないことを確認
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["H_A"]["type"] = 2
        inputs["C_A"]["type"] = 2

        result = calc(inputs, test_mode=True)

        assert result['TValue'].E_C == expected_result_type2.E_C
        assert result['TValue'].E_H == expected_result_type2.E_H

    def test_未定義の方式(self):
        """ 定義されていないタイプで計算されたとき例外で検知できる
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["H_A"]["type"] = 4  # 未定義の暖房方式
        inputs["C_A"]["type"] = 4  # 未定義の冷房方式

        with pytest.raises(Exception):
            calc(inputs, test_mode=True)
