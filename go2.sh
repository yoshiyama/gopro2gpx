#!/bin/bash

# 対象ディレクトリを設定
TARGET_DIR="/mnt/f/GoPro-Seto_Danchi/20231006/Front/"

# 対象ディレクトリ内のすべての MP4 ファイルに対してループ処理
for file in "$TARGET_DIR"/*.MP4; do
    # 出力ファイルのパスを設定（拡張子を除外）
    output="${file%.MP4}"

    # gopro2gpx コマンドを実行
    gopro2gpx -s -vvv "$file" "$output"
done
