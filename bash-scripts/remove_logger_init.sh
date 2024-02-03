#!/bin/bash

# NOTE: init_logger() をしているとログファイルへの書き込み処理を行います
# テスト実行を速くするために調査時以外には有効化されないようにするため
# シェルスクリプトでテストディレクトリ内から削除します

# ターゲットコードを含んでいる行ごと消すので注意
target_code="init_logger"
# 削除対象のディレクトリを指定
dir="tests/*"

# NOTE: テストを階層的に置かないことを前提としています
find $dir -maxdepth 0 -type f -iname '*.py' | while read file
do
  filename="${file}"

  # ファイル名にスペース含んでいる時 $filename ではなく "${filename}" を使用する
  line_numbers=$(grep -n $target_code "${filename}" | cut -d: -f1)
  #echo ${line_numbers}

  # 削除行指定のテキストを生成 ex. 49d; 60d;
  delete_row_command=""
  target_row_count=0
  for num in $line_numbers; do
    target_row_count=`expr $target_row_count + 1`  # インクリメント
    delete_row_command+="${num}d; "
  done

  if [ $target_row_count -gt 0 ]; then
    # 指定行を削除してファイルを上書き
    sed -i "${delete_row_command}" "${filename}"
    echo "Deleted ${target_row_count} rows"
  else
    echo "No need to delete"
  fi
done
