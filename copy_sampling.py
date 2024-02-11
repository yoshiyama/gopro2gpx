# python copy_sampling.py /mnt/f/GoPro-Seto_Danchi/20231006/Front/GH110241 /mnt/f/GoPro-Seto_Danchi/20231006/Front/GH110241_sampling 10



import os
import shutil
import sys


def copy_and_rename_images(source_dir, target_dir, step):
    """
    特定のフォルダから指定されたピッチで画像を選択し、指定されたフォーマットでファイル名を変更して、
    別のフォルダにコピーする。

    :param source_dir: 画像が保存されているソースディレクトリのパス
    :param target_dir: コピー先のターゲットディレクトリのパス
    :param step: 何ピッチで画像を選択するか
    """
    # ソースディレクトリ内の全ファイルをリストアップ
    files = [f for f in os.listdir(source_dir) if f.lower().endswith('.jpg')]
    files.sort()  # ファイル名でソート

    # ステップごとにファイルを選択
    for i in range(0, len(files), step):
        source_path = os.path.join(source_dir, files[i])

        # 新しいファイル名を生成
        new_file_name = '_'.join(source_dir.split(os.sep)[-4:]) + '_' + files[i]
        target_path = os.path.join(target_dir, new_file_name)

        # ファイルをコピー
        shutil.copy2(source_path, target_path)
        print(f"Copied {source_path} to {target_path}")


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python script.py <source_dir> <target_dir> <step>")
        sys.exit(1)

    source_dir = sys.argv[1]
    target_dir = sys.argv[2]
    step = int(sys.argv[3])

    # 関数を実行
    copy_and_rename_images(source_dir, target_dir, step)
