import pytest
import math

from jjjexperiment.denchu_1 import *

class Test_計算式_乾燥空気密度:
    """ 乾燥空気の密度[kg/m3]の計算が正しい
    """
    # 目標値参考: http://www.es.ris.ac.jp/~nakagawa/met_cal/dens.html

    def test_0度(self):
        sut = dry_air_density(0)
        assert math.isclose(sut, 1.2925, abs_tol=1e-3)
    def test_10度(self):
        sut = dry_air_density(10)
        assert math.isclose(sut, 1.2469, abs_tol=1e-3)
    def test_20度(self):
        sut = dry_air_density(20)
        assert math.isclose(sut, 1.2043, abs_tol=1e-3)
    def test_30度(self):
        sut = dry_air_density(30)
        assert math.isclose(sut, 1.1646, abs_tol=1e-3)
    def test_40度(self):
        sut = dry_air_density(40)
        assert math.isclose(sut, 1.1274, abs_tol=1e-3)


class Test_計算式_重量絶対湿度変換:
    """ 空気の相対湿度[%]から重量絶対湿度[g/kg(DA)]への変換が正しい
    """
    # 目標値参考: https://www.techno-ryowa.co.jp/rrlab/

    def test_20C_50RH(self):
        sut = absolute_humid(50, 20)
        assert math.isclose(sut, 7.3, abs_tol=1e-2)
    def test_23C_50RH(self):
        sut = absolute_humid(50, 23)
        assert math.isclose(sut, 8.8, abs_tol=1e-2)
    def test_25C_50RH(self):
        sut = absolute_humid(50, 25)
        assert math.isclose(sut, 9.9, abs_tol=1e-2)

    def test_20C_60RH(self):
        sut = absolute_humid(60, 20)
        assert math.isclose(sut, 8.7, abs_tol=1e-2)
    def test_23C_60RH(self):
        sut = absolute_humid(60, 23)
        assert math.isclose(sut, 10.5, abs_tol=1e-2)
    def test_25C_60RH(self):
        sut = absolute_humid(60, 25)
        assert math.isclose(sut, 11.9, abs_tol=1e-2)


class Test_計算式_湿り空気の比熱:
    """ 湿り空気の比熱が適切な範囲の数値になる
    """
    # 目標値参考: https://www.jstage.jst.go.jp/article/jsam1937/37/4/37_4_694/_pdf

    def test_x_0005(self):
        sut = get_Ca(0.005)
        assert math.isclose(sut, 1.014, abs_tol=1e-2)
    def test_x_0010(self):
        sut = get_Ca(0.010)
        assert math.isclose(sut, 1.024, abs_tol=1e-2)
    def test_x_0015(self):
        sut = get_Ca(0.015)
        assert math.isclose(sut, 1.033, abs_tol=1e-2)
