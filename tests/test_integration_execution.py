import pytest
import json
import copy

from jjjexperiment.main import calc

from test_utils.utils import  \
    expected_result_type1, expected_result_type2, expected_inputs, INPUT_SAMPLE_TYPE1_PATH, INPUT_SAMPLE_TYPE2_PATH, INPUT_SAMPLE_TYPE3_PATH

from logs.app_logger import LimitedLoggerAdapter as _logger

class Test既存計算維持_デフォルト入力時:

    _inputs1: dict = json.load(open(INPUT_SAMPLE_TYPE1_PATH, 'r'))
    _inputs2: dict = json.load(open(INPUT_SAMPLE_TYPE2_PATH, 'r'))
    _inputs3: dict = json.load(open(INPUT_SAMPLE_TYPE3_PATH, 'r'))

    def test_インプットデータ_前提確認(self, expected_inputs):
        """ テストコードが想定しているインプットデータかどうか確認
        """
        result = calc(self._inputs1, test_mode=True)

        assert result['TInput'].q_rtd_C == expected_inputs.q_rtd_C
        assert result['TInput'].q_rtd_H == expected_inputs.q_rtd_H
        assert result['TInput'].q_max_C == expected_inputs.q_max_C
        assert result['TInput'].q_max_H == expected_inputs.q_max_H
        assert result['TInput'].e_rtd_C == expected_inputs.e_rtd_C
        assert result['TInput'].e_rtd_H == expected_inputs.e_rtd_H

    def test_計算結果一致_方式1(self, expected_result_type1):
        """ ipynbのサンプル入力で計算結果が意図しない変化がないことを確認
        """
        _logger.init_logger()
        result = calc(self._inputs1, test_mode=True)

        assert result['TValue'].E_C == expected_result_type1.E_C
        assert result['TValue'].E_H == expected_result_type1.E_H

    def test_計算結果一致_方式2(self, expected_result_type2):
        """ ipynbのサンプル入力で計算結果が意図しない変化がないことを確認
        """
        _logger.init_logger()
        result = calc(self._inputs2, test_mode=True)

        assert result['TValue'].E_C == expected_result_type2.E_C
        assert result['TValue'].E_H == expected_result_type2.E_H

    def test_計算結果一致_方式3(self, expected_result_type1, expected_result_type2):
        """ 方式3で全体が実行され結果が変わることを確認
        """
        _logger.init_logger()
        result = calc(self._inputs3, test_mode=True)

        assert result['TValue'].E_C != expected_result_type1.E_C
        assert result['TValue'].E_C != expected_result_type2.E_C

        assert result['TValue'].E_H != expected_result_type1.E_H
        assert result['TValue'].E_H != expected_result_type2.E_H
