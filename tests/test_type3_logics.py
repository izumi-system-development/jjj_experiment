from jjjexperiment.jjj_section4_2_a import get_A_f_hex, get_A_e_hex
from jjjexperiment.constants import PROCESS_TYPE_1, PROCESS_TYPE_2, PROCESS_TYPE_3

import jjjexperiment.constants as consts


class Testコイル特性:

    expected_T1T2 = {
        'A_f_hex': 0.23559,
        'A_e_hex': 6.396,
    }
    expected_T3 = {
        'A_f_hex_upper': 0.3,
        'A_f_hex_lower': 0.2,
        'A_f_hex_custom': 0.23456,  # ユーザーの独自入力を想定
        'A_e_hex_upper': 10.6,
        'A_e_hex_lower': 6.2,
        'A_e_hex_custom': 6.66666,  # ユーザーの独自入力を想定
    }

    def test_有効面積_方式1_定格低(self):
        """ 定格能力 5.6 kW 未満で 仕様書通り """
        assert self.expected_T1T2['A_f_hex'] == get_A_f_hex(PROCESS_TYPE_1, 5500)
        assert self.expected_T1T2['A_e_hex'] == get_A_e_hex(PROCESS_TYPE_1, 5500)
    def test_有効面積_方式1_定格BVA(self):
        """ 定格能力 5.6 kW 丁度で 仕様書通り """
        assert self.expected_T1T2['A_f_hex'] == get_A_f_hex(PROCESS_TYPE_1, 5600)
        assert self.expected_T1T2['A_e_hex'] == get_A_e_hex(PROCESS_TYPE_1, 5600)
    def test_有効面積_方式1_定格高(self):
        """ 定格能力 5.6 kW 以上で 仕様書通り """
        assert self.expected_T1T2['A_f_hex'] == get_A_f_hex(PROCESS_TYPE_1, 5700)
        assert self.expected_T1T2['A_e_hex'] == get_A_e_hex(PROCESS_TYPE_1, 5700)

    def test_有効面積_方式2_定格低(self):
        """ 定格能力 5.6 kW 未満で 仕様書通り """
        assert self.expected_T1T2['A_f_hex'] == get_A_f_hex(PROCESS_TYPE_2, 5500)
        assert self.expected_T1T2['A_e_hex'] == get_A_e_hex(PROCESS_TYPE_2, 5500)
    def test_有効面積_方式2_定格BVA(self):
        """ 定格能力 5.6 kW 丁度で 仕様書通り """
        assert self.expected_T1T2['A_f_hex'] == get_A_f_hex(PROCESS_TYPE_2, 5600)
        assert self.expected_T1T2['A_e_hex'] == get_A_e_hex(PROCESS_TYPE_2, 5600)
    def test_有効面積_方式2_定格高(self):
        """ 定格能力 5.6 kW 以上で 仕様書通り """
        assert self.expected_T1T2['A_f_hex'] == get_A_f_hex(PROCESS_TYPE_2, 5700)
        assert self.expected_T1T2['A_e_hex'] == get_A_e_hex(PROCESS_TYPE_2, 5700)

    def test_有効面積_方式3_定格低(self):
        """ 定格能力 5.6 kW 未満で 仕様書通り """
        assert self.expected_T3['A_f_hex_lower'] == get_A_f_hex(PROCESS_TYPE_3, 5500)
        assert self.expected_T3['A_e_hex_lower'] == get_A_e_hex(PROCESS_TYPE_3, 5500)
    def test_有効面積_方式3_定格BVA(self):
        """ 定格能力 5.6 kW 丁度で 仕様書通り """
        assert self.expected_T3['A_f_hex_upper'] == get_A_f_hex(PROCESS_TYPE_3, 5600)
        assert self.expected_T3['A_e_hex_upper'] == get_A_e_hex(PROCESS_TYPE_3, 5600)
    def test_有効面積_方式3_定格高(self):
        """ 定格能力 5.6 kW 以上で 仕様書通り """
        assert self.expected_T3['A_f_hex_upper'] == get_A_f_hex(PROCESS_TYPE_3, 5700)
        assert self.expected_T3['A_e_hex_upper'] == get_A_e_hex(PROCESS_TYPE_3, 5700)

    def test_有効面積_方式3_定格低_上書き(self):
        """ 定格能力 5.6 kW 未満で 仕様書通り """
        consts.A_f_hex_small_H = self.expected_T3['A_f_hex_custom']
        consts.A_e_hex_small_H = self.expected_T3['A_e_hex_custom']
        assert self.expected_T3['A_f_hex_custom'] == get_A_f_hex(PROCESS_TYPE_3, 5500)
        assert self.expected_T3['A_e_hex_custom'] == get_A_e_hex(PROCESS_TYPE_3, 5500)
    def test_有効面積_方式3_定格BVA_上書き(self):
        """ 定格能力 5.6 kW 丁度で 仕様書通り """
        consts.A_f_hex_large_H = self.expected_T3['A_f_hex_custom']
        consts.A_e_hex_large_H = self.expected_T3['A_e_hex_custom']
        assert self.expected_T3['A_f_hex_custom'] == get_A_f_hex(PROCESS_TYPE_3, 5600)
        assert self.expected_T3['A_e_hex_custom'] == get_A_e_hex(PROCESS_TYPE_3, 5600)
    def test_有効面積_方式3_定格高_上書き(self):
        """ 定格能力 5.6 kW 以上で 仕様書通り """
        consts.A_f_hex_large_H = self.expected_T3['A_f_hex_custom']
        consts.A_e_hex_large_H = self.expected_T3['A_e_hex_custom']
        assert self.expected_T3['A_f_hex_custom'] == get_A_f_hex(PROCESS_TYPE_3, 5700)
        assert self.expected_T3['A_e_hex_custom'] == get_A_e_hex(PROCESS_TYPE_3, 5700)
