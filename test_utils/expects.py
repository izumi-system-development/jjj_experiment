import pytest
from jjjexperiment.result import *

@pytest.fixture
def expected_inputs():
    """ テストコードは下記の入力を想定したものになっています """
    inputs = TestInputPickups(
        q_rtd_C = 5600,
        q_rtd_H = 6685.3,
        q_max_C = 5944.619999999999,
        q_max_H = 10047.047813999998,
        e_rtd_C = 2.8512,
        e_rtd_H = 3.855424,
    )
    return inputs

@pytest.fixture
def expected_result_type1():
    """ 上記の入力内容で期待される結果 """
    return ResultSummary(E_C=14746.052998129611, E_H=36310.32799729332)

@pytest.fixture
def expected_result_type2():
    """ 上記の入力内容で期待される結果 """
    return ResultSummary(E_C=14695.841130521072, E_H=40812.21298826678)
