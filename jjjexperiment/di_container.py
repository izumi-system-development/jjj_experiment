import pandas as pd
from injector import Module, provider, inject, singleton

# FIXME: DIコンテナライブラリ Injector の導入中 まだ使い慣れていないので随時ブラッシュアップ

class DataFrameHolder:
    def __init__(self):
        self._dataframe = pd.DataFrame()

    def update_df(self, data):
        new_df = pd.DataFrame(data)
        self._dataframe = pd.concat([self._dataframe, new_df], ignore_index=True)

    def get_dataframe(self):
        return self._dataframe

# DIコンテナの設定
class JJJExperimentModule(Module):
    @singleton
    @provider
    def provide_data_frame_holder(self) -> DataFrameHolder:
        return DataFrameHolder()
    # メソッド名は使われない返却型に意味がある
    # 引数をとる場合の例: https://github.com/python-injector/injector/blob/master/README.md

# NOTE: DIコンテナからの取得物への操作

# 関数の定義にinjectデコレータを使用し、DataFrameHolderインスタンスを受け取る
@inject
def some_function(data_frame_holder: DataFrameHolder):
    # 関数内で何らかの処理を行い、途中結果をデータフレームに追加
    intermediate_result = {'x': [1, 2, 3], 'y': [4, 5, 6]}  # 何らかの中間結果
    data_frame_holder.update_df(intermediate_result)

# ネストした関数の例
@inject
def another_function(data_frame_holder: DataFrameHolder):
    # 内部関数も同様にデータフレームを更新
    some_function(data_frame_holder)

# 最終的にメイン関数またはスクリプト終了時にCSVファイルに出力
@inject
def export_to_csv(filename: str, data_frame_holder: DataFrameHolder):
    df = data_frame_holder.get_dataframe()
    df.to_csv(filename, index=False)

