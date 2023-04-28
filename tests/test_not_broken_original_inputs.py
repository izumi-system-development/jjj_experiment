import pytest
import json
import copy

import sys, pprint
# sys.path.append("./jjjexperiment")  # '../'
# pprint.pprint(sys.path)

# FIXME:カレントディレクトリが jjj_experiment/jjjexperiment で実行時のみ動く
from jjjexperiment.main import calc
from jjjexperiment.result import ResultSummary
import numpy as np

class Test既存計算維持_デフォルト入力時:

    # FIXME: スマートなパスの指定方法があれば
    _inputs: dict = json.load(open('./tests/inputs/default_testinput.json', 'r'))

    def test_インプットデータ_前提確認(self, expected_inputs):
        """ テストコードが想定しているインプットデータかどうか確認
        """
        expected = ResultSummary(
            q_rtd_C = 5600,
            q_rtd_H = 6685.3,
            q_max_C = 5944.619999999999,
            q_max_H = 10047.047813999998,
            e_rtd_C = 2.8512,
            e_rtd_H = 3.855424,
            E_C = 14746.052998129611,
            E_H = 36310.32799729332)

        inputs = copy.deepcopy(self._inputs)
        inputs["H_A"]["type"] = 1
        inputs["C_A"]["type"] = 1

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == expected.q_rtd_C
        assert result.q_rtd_H == expected.q_rtd_H
        assert result.q_max_C == expected.q_max_C
        assert result.q_max_H == expected.q_max_H
        assert result.e_rtd_C == expected.e_rtd_C
        assert result.e_rtd_H == expected.e_rtd_H
        assert result.E_C == expected.E_C
        assert result.E_H == expected.E_H

    def test_計算結果一致_方式2(self, expected_result_type2):
        """ ipynbのサンプル入力で計算結果が意図しない変化がないことを確認
        """
        expected = ResultSummary(
            q_rtd_C = 5600,
            q_rtd_H = 6685.3,
            q_max_C = 5944.619999999999,
            q_max_H = 10047.047813999998,
            e_rtd_C = 2.8512,
            e_rtd_H = 3.855424,
            E_C = 14695.841130521072,
            E_H = 40812.21298826678)

        inputs = copy.deepcopy(self._inputs)
        inputs["H_A"]["type"] = 2
        inputs["C_A"]["type"] = 2

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == expected.q_rtd_C
        assert result.q_rtd_H == expected.q_rtd_H
        assert result.q_max_C == expected.q_max_C
        assert result.q_max_H == expected.q_max_H
        assert result.e_rtd_C == expected.e_rtd_C
        assert result.e_rtd_H == expected.e_rtd_H
        assert result.E_C == expected.E_C
        assert result.E_H == expected.E_H

    def test_未定義の方式(self):
        """ 定義されていないタイプで計算されたとき例外で検知できる
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["H_A"]["type"] = 4
        inputs["C_A"]["type"] = 4

        with pytest.raises(Exception):
            calc(inputs, test_mode=True)
