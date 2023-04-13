import pytest
import json
import copy

import sys, pprint
# sys.path.append("./jjjexperiment")  # '../'
# pprint.pprint(sys.path)

# FIXME:カレントディレクトリが jjj_experiment/jjjexperiment で実行時のみ動く
from jjjexperiment.main import calc
from jjjexperiment.result import ResultSummary

class TestNotBrokenOriginalInputs:

    # FIXME: スマートなパスの指定方法があれば
    _inputs: dict = json.load(open('./tests/inputs/default_testinput.json', 'r'))

    _original_output = ResultSummary(
            q_rtd_C = 5600,
            q_rtd_H = 6685.3,
            q_max_C = 5944.619999999999,
            q_max_H = 10047.047813999998,
            e_rtd_C = 2.8512,
            e_rtd_H = 3.855424,
            E_C = 14746.052998129611,
            E_H = 36310.32799729332)

    def test_output_not_changed_when_type1(self):
        """ notebook のサンプル入力例が同じ結果となる
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["H_A"]["type"] = 1
        inputs["C_A"]["type"] = 1

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._original_output.q_rtd_C
        assert result.q_rtd_H == self._original_output.q_rtd_H
        assert result.q_max_C == self._original_output.q_max_C
        assert result.q_max_H == self._original_output.q_max_H
        assert result.e_rtd_C == self._original_output.e_rtd_C
        assert result.e_rtd_H == self._original_output.e_rtd_H
        assert result.E_H == self._original_output.E_H
        assert result.E_C == self._original_output.E_C

    # BUG: type の文字列が一致しないエラーがあります
    def test_output_not_changed_when_type2(self):
        """ notebook のサンプル入力例が同じ結果となる
        """
        inputs = copy.deepcopy(self._inputs)
        inputs["H_A"]["type"] = 2
        inputs["C_A"]["type"] = 2

        result = calc(inputs, test_mode=True)

        assert result.q_rtd_C == self._original_output.q_rtd_C
        assert result.q_rtd_H == self._original_output.q_rtd_H
        assert result.q_max_C == self._original_output.q_max_C
        assert result.q_max_H == self._original_output.q_max_H
        assert result.e_rtd_C == self._original_output.e_rtd_C
        assert result.e_rtd_H == self._original_output.e_rtd_H
        assert result.E_H == self._original_output.E_H
        assert result.E_C == self._original_output.E_C
