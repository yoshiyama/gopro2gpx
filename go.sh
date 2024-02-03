#gopro2gpx -s -vvv /mnt/f/GoPro-Seto_Danchi/20231006/Back/GH010239.MP4 /mnt/f/GoPro-Seto_Danchi/20231006/Back/GH010239
#gopro2gpx -s -vvv /mnt/f/GoPro-Seto_Danchi/20231006/Back/GH020239.MP4 /mnt/f/GoPro-Seto_Danchi/20231006/Back/GH020239
#!/bin/bash

# 対象ディレクトリを設定
TARGET_DIR="/mnt/f/GoPro-Seto_Danchi/20231006/Back"

# 開始番号と終了番号を設定
START_NUM=100239
END_NUM=130239

# 指定された範囲内でループ
for (( num=$START_NUM; num<=$END_NUM; num++ )); do
    # ファイル名を生成
    FILENAME="GH${num}.MP4"

    # ファイルが存在するか確認
    if [[ -f "$TARGET_DIR/$FILENAME" ]]; then
        # 出力ファイルのパスを設定
        OUTPUT="${TARGET_DIR}/GH${num}"

        # gopro2gpx コマンドを実行
        gopro2gpx -s -vvv "$TARGET_DIR/$FILENAME" "$OUTPUT"
    fi
done
