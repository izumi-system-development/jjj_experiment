from jjjexperiment.jjj_section4_2_a import get_A_f_hex, get_A_e_hex
from jjjexperiment.constants import PROCESS_TYPE_1, PROCESS_TYPE_2, PROCESS_TYPE_3

import jjjexperiment.constants as consts


class Testコイル特性:

    def test_有効面積_TYPE1_低定格(self):
        """ 定格能力 5.6 kW 未満で 仕様書通り """
        assert 0.23559 == get_A_f_hex(PROCESS_TYPE_1, 5500)
        assert 6.396   == get_A_e_hex(PROCESS_TYPE_1, 5500)
    def test_有効面積_TYPE1_閾定格(self):
        """ 定格能力 5.6 kW 丁度で 仕様書通り """
        assert 0.23559 == get_A_f_hex(PROCESS_TYPE_1, 5600)
        assert 6.396   == get_A_e_hex(PROCESS_TYPE_1, 5600)
    def test_有効面積_TYPE1_高定格(self):
        """ 定格能力 5.6 kW 以上で 仕様書通り """
        assert 0.23559 == get_A_f_hex(PROCESS_TYPE_1, 5700)
        assert 6.396   == get_A_e_hex(PROCESS_TYPE_1, 5700)

    def test_有効面積_TYPE2_低定格(self):
        """ 定格能力 5.6 kW 未満で 仕様書通り """
        assert 0.23559 == get_A_f_hex(PROCESS_TYPE_2, 5500)
        assert 6.396   == get_A_e_hex(PROCESS_TYPE_2, 5500)
    def test_有効面積_TYPE2_閾定格(self):
        """ 定格能力 5.6 kW 丁度で 仕様書通り """
        assert 0.23559 == get_A_f_hex(PROCESS_TYPE_2, 5600)
        assert 6.396   == get_A_e_hex(PROCESS_TYPE_2, 5600)
    def test_有効面積_TYPE2_高定格(self):
        """ 定格能力 5.6 kW 以上で 仕様書通り """
        assert 0.23559 == get_A_f_hex(PROCESS_TYPE_2, 5700)
        assert 6.396   == get_A_e_hex(PROCESS_TYPE_2, 5700)

    def test_有効面積_TYPE3_低定格(self):
        """ 定格能力 5.6 kW 未満で 仕様書通り """
        assert 0.2 == get_A_f_hex(PROCESS_TYPE_3, 5500)
        assert 6.2 == get_A_e_hex(PROCESS_TYPE_3, 5500)
    def test_有効面積_TYPE3_閾定格(self):
        """ 定格能力 5.6 kW 丁度で 仕様書通り """
        assert 0.3 == get_A_f_hex(PROCESS_TYPE_3, 5600)
        assert 10.6 == get_A_e_hex(PROCESS_TYPE_3, 5600)
    def test_有効面積_TYPE3_高定格(self):
        """ 定格能力 5.6 kW 以上で 仕様書通り """
        assert 0.3 == get_A_f_hex(PROCESS_TYPE_3, 5700)
        assert 10.6 == get_A_e_hex(PROCESS_TYPE_3, 5700)

    def test_有効面積_TYPE3_低定格_上書き(self):
        """ 定格能力 5.6 kW 未満で 仕様書通り """
        consts.A_f_hex_small_H = 0.23456  # ユーザー入力時に上書きした場合
        consts.A_e_hex_small_H = 6.66666  # ユーザー入力時に上書きした場合
        assert 0.23456 == get_A_f_hex(PROCESS_TYPE_3, 5500)
        assert 6.66666 == get_A_e_hex(PROCESS_TYPE_3, 5500)
    def test_有効面積_TYPE3_閾定格_上書き(self):
        """ 定格能力 5.6 kW 丁度で 仕様書通り """
        consts.A_f_hex_large_H = 0.34567  # ユーザー入力時に上書きした場合
        consts.A_e_hex_large_H = 9.99999  # ユーザー入力時に上書きした場合
        assert 0.34567 == get_A_f_hex(PROCESS_TYPE_3, 5600)
        assert 9.99999 == get_A_e_hex(PROCESS_TYPE_3, 5600)
    def test_有効面積_TYPE3_高定格_上書き(self):
        """ 定格能力 5.6 kW 以上で 仕様書通り """
        consts.A_f_hex_large_H = 0.34567  # ユーザー入力時に上書きした場合
        consts.A_e_hex_large_H = 9.99999  # ユーザー入力時に上書きした場合
        assert 0.34567 == get_A_f_hex(PROCESS_TYPE_3, 5700)
        assert 9.99999 == get_A_e_hex(PROCESS_TYPE_3, 5700)
