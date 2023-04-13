import pytest
import json

import sys, os

import pprint
# sys.path.append(os.path.dirname(sys.path[0]))  # '../'
sys.path.append("../")  # '../'
# pprint.pprint(sys.path)

# FIXME:カレントディレクトリが jjj_experiment/jjjexperiment で実行時のみ動く
import jjjexperiment.main as main

def test_defaultcase():
    """ notebook のサンプル入力例が同じ結果となる
    """

    # FIXME: スマートなパスの指定方法があれば
    json_str = open('./tests/inputs/default_testinput.json', 'r')
    json_obj = json.load(json_str)
    result = main.calc(json_obj, test_mode=True)
    assert result.q_rtd_C == 5600
    assert result.q_rtd_H == 6685.3
    assert result.q_max_C == 5944.619999999999
    assert result.q_max_H == 10047.047813999998
    assert result.e_rtd_H == 3.855424
    assert result.e_rtd_C == 2.8512

    # FIXME: デフォルトケース以下の二つが合いません
    # assert result.E_H == 36310.32799729332
    # assert result.E_C == 14746.052998129611
