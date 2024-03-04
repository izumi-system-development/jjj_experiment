import pandas as pd
from injector import Module, provider, inject, singleton

# FIXME: DIコンテナライブラリ Injector の導入中 まだ使い慣れていないので随時ブラッシュアップ

# NOTE: DIコンテナで管理するもの毎に型を定義する必要があるはず...

class DtDataFrameHolder:
    """d_t 長のデータフレーム"""
    @inject
    def __init__(self):
        self._dataframe = pd.DataFrame()

    def update_df(self, data):
        new_df = pd.DataFrame(data)
        self._dataframe = pd.concat([self._dataframe, new_df], ignore_index=True)

    def get_dataframe(self):
        return self._dataframe


class HaCaInputHolder:
    """暖房時・冷房時の判別に使用したい"""
    @inject
    def __init__(self):
        self.__q_hs_rtd_C = None
        self.__q_hs_rtd_H = None

    @property
    def q_hs_rtd_C(self):
        return self.__q_hs_rtd_C
    @q_hs_rtd_C.setter
    def q_hs_rtd_C(self, value):
        self.__q_hs_rtd_C = value

    @property
    def q_hs_rtd_H(self):
        return self.__q_hs_rtd_H
    @q_hs_rtd_H.setter
    def q_hs_rtd_H(self, value):
        self.__q_hs_rtd_H = value

    def flg_char(self):
        if self.isH:
          ch_flg = 'H'
        elif self.isC:
          ch_flg = 'C'
        else:
          raise ValueError()
        return ch_flg

    # もう少し情報持たせてもよさそう
    def isH(self) -> bool:
        return (self.q_hs_rtd_H is not None) and (self.q_hs_rtd_C is None)
    def isC(self) -> bool:
        return (self.q_hs_rtd_C is not None) and (self.q_hs_rtd_H is None)

# DIコンテナインスタンスを使いまわしている間はシングルトンが得られるが、
# DIコンテナインスタンス自体を再生成したときには中身はリセットされる

# @provider で get() できるようになる
# REF: https://zenn.dev/ktnyt/articles/cc5056ce81e9d3

# DIコンテナの設定
class JJJExperimentModule(Module):
    # メソッド名は使われない返却型に意味がある
    # 引数をとる場合の例: https://github.com/python-injector/injector/blob/master/README.md
    @singleton
    @provider
    def provide_dt_data_frame_holder(self) -> DtDataFrameHolder:
        return DtDataFrameHolder()

    # NOTE: シングルトンを暖房用・冷房用に切替えるのは悪手、それぞれのインスタンスとする
    @provider
    def provide_ha_ca_input_holder(self) -> HaCaInputHolder:
        return HaCaInputHolder()

# NOTE: DIコンテナからの取得物への操作

# 関数の定義にinjectデコレータを使用し、DataFrameHolderインスタンスを受け取る
@inject
def some_function(data_frame_holder: DtDataFrameHolder):
    # 関数内で何らかの処理を行い、途中結果をデータフレームに追加
    intermediate_result = {'x': [1, 2, 3], 'y': [4, 5, 6]}  # 何らかの中間結果
    data_frame_holder.update_df(intermediate_result)

# ネストした関数の例
@inject
def another_function(data_frame_holder: DtDataFrameHolder):
    # 内部関数も同様にデータフレームを更新
    some_function(data_frame_holder)

@inject  # 不要?必要?よくわかっていない
# 最終的にメイン関数またはスクリプト終了時にCSVファイルに出力
def export_to_csv(data_frame_holder: DtDataFrameHolder, filename: str, encoding: str = 'cp932'):
    df = data_frame_holder.get_dataframe()
    df.to_csv(filename, index=False, encoding=encoding)
