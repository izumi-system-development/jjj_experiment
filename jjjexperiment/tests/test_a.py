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

